"""Split a session into *moments* — deterministic, no model involved.

A moment is a coherent span of a session: a conversation, a task, a walk.  The
segmenter only looks at *when* things happened:

* utterances (speech with a start and an end), and
* keyframes (points in time, each knowing why it was picked and how novel it was).

How it works
------------
1. **Atoms.**  Everything is put on one timeline, sorted by start time, and
   grouped into the smallest units that may never be torn apart: an utterance
   together with whatever starts while it is still running.  A moment boundary
   can only fall *between* atoms, so a moment never starts in the middle of an
   utterance.  Speech-to-text often reports the next utterance a few hundred
   milliseconds before the previous one ended; an overlap of up to
   :data:`OVERLAP_TOLERANCE` seconds does not glue two utterances together.
2. **Boundaries that are always there.**
   A *coverage hole* — a stretch with neither speech nor a keyframe that is at
   least :func:`coverage_hole_seconds` long (recording was evidently off, e.g.
   between two imported clips) — is always a boundary and is never merged away.
   A *pause in speech* of at least ``moment_gap_seconds`` is a boundary too.
   Keyframes seen during such a pause stay with the speech they are close to
   (within half the gap, and not beyond a strong visual change); a longer silent
   stretch in between becomes a span of its own.
3. **Too long.**  A span longer than ``moment_max_seconds`` is cut by a small
   dynamic programme that uses as few cuts as possible, prefers the longest
   internal pauses and strong visual changes (a keyframe whose reason is
   ``"scene"`` or whose novelty is at least :data:`HIGH_NOVELTY`) and otherwise
   cuts evenly between utterances.
4. **Too short.**  A moment shorter than ``moment_min_seconds`` is merged into
   the neighbour that is closer in time, unless that would cross a coverage
   hole or exceed the maximum.  (When one of the two joins would undo a strong
   visual change and the other would not, the other one wins: frames taken
   after walking somewhere else go with what happened there.)  A short moment
   with no neighbour it may join stays as it is.

Guarantees (tested property-style in ``tests/test_moments.py``)
----------------------------------------------------------------
* Moments are ordered, ``idx`` is ``0..n-1``, ``ts0`` strictly increases and
  ``ts1 <= next.ts0``.
* Every utterance and every keyframe belongs to exactly one moment: the one
  whose ``[ts0, next.ts0)`` contains its start time.  Ids are listed in time order.
* ``ts0`` is the start of the first thing in the moment, ``ts1`` the end of the
  last (shortened to the next moment's ``ts0`` in the rare case of a tolerated
  overlap), so the bounds are tight.
* ``title`` / ``summary`` / ``tags`` are left empty; ``notes/summarize.py`` fills them.
"""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass, field

from ..config import NotesSettings
from ..models import Keyframe, Moment, Session, Utterance

log = logging.getLogger("videonotes.moments")

__all__ = ["HIGH_NOVELTY", "OVERLAP_TOLERANCE", "coverage_hole_seconds", "segment_moments"]

#: Two utterances may overlap by this many seconds and still be separable.
OVERLAP_TOLERANCE = 1.0
#: Keyframe novelty (0..1) from which a frame counts as a strong visual change.
HIGH_NOVELTY = 0.5
#: A stretch without any material is never called a coverage hole below this length (s).
MIN_HOLE_SECONDS = 120.0
#: How many wide keyframe spacings inside single clips it takes to conclude frames are sampled sparsely.
SPARSE_EVIDENCE = 3

_DEFAULT_GAP_SECONDS = 120.0

# Cost model of the long-span splitter (see _split_long). The magnitudes encode a
# strict order of priorities: never exceed the maximum if it can be avoided (OVER)
# > use as few pieces as possible (PIECE) > do not leave slivers (SHORT) > cut at
# the best pause / visual change (gains, at most 5 per cut) > keep pieces even (EVEN).
_COST_OVER = 1000.0
_COST_PIECE = 10.0
_COST_SHORT = 8.0
_COST_EVEN = 2.0
_GAIN_PAUSE = 2.0  # x (speech pause / gap), capped at 1
_GAIN_EMPTY = 1.0  # x (stretch with nothing at all / gap), capped at 1
_GAIN_SCENE = 2.0  # the piece would start on a scene-change keyframe
_GAIN_NOVEL = 1.0  # x novelty, for keyframes at or above HIGH_NOVELTY


@dataclass(slots=True)
class _Item:
    start: float
    end: float
    speech: bool
    ref: int | None
    clip_id: int | None = None
    scene: bool = False
    novelty: float = 0.0


@dataclass(slots=True)
class _Atom:
    """Items that must stay together; boundaries only ever fall between atoms."""

    start: float
    end: float  # end of the last thing in this atom
    speech: bool = False
    visual: float = 0.0  # strength of the visual change this atom starts with (speech-free atoms only)
    utterance_ids: list[int] = field(default_factory=list)
    keyframe_ids: list[int] = field(default_factory=list)


@dataclass(slots=True)
class _Piece:
    lo: int  # first atom (inclusive)
    hi: int  # last atom (exclusive)
    end: float  # latest end of anything inside


def coverage_hole_seconds(cfg: NotesSettings, keyframes: list[Keyframe]) -> float:
    """How long a stretch without speech *and* without keyframes must be to count as a hole.

    Normally ``moment_gap_seconds``, and never less than two minutes.  The
    exception is footage whose keyframes were evidently sampled more sparsely
    than that (``frames.max_gap_s`` raised by the user): when at least
    :data:`SPARSE_EVIDENCE` pairs of neighbouring keyframes *of the same clip* —
    one continuous file, so the camera was certainly running — are that far
    apart, the threshold grows to 1.5 times their typical (median) spacing.
    Otherwise every lone keyframe of a quiet stretch would become a moment.
    """
    gap_s, _, _ = _limits(cfg)
    base = max(gap_s, MIN_HOLE_SECONDS)
    wide: list[float] = []
    previous: Keyframe | None = None
    for kf in sorted((k for k in keyframes if _finite(k.ts)), key=lambda k: k.ts):
        if previous is not None and kf.clip_id == previous.clip_id and 1.5 * (kf.ts - previous.ts) >= base:
            wide.append(kf.ts - previous.ts)
        previous = kf
    if len(wide) >= SPARSE_EVIDENCE:
        wide.sort()
        base = max(base, 1.5 * wide[len(wide) // 2])
    return base


def segment_moments(
    session: Session, utterances: list[Utterance], keyframes: list[Keyframe], cfg: NotesSettings
) -> list[Moment]:
    """Split a session into moments at long speech pauses and strong visual changes,
    honouring ``moment_min_seconds`` / ``moment_max_seconds``. Deterministic; no LLM.

    ``utterances`` and ``keyframes`` are everything recognised in the session
    (any order; gaps, overlaps and empty lists are fine).  Returns moments with
    ``idx``, ``ts0``, ``ts1``, ``utterance_ids`` and ``keyframe_ids`` filled in
    and ``title`` / ``summary`` / ``tags`` empty, or ``[]`` when there is nothing
    at all.  See the module docstring for the rules and guarantees.
    """
    gap_s, min_s, max_s = _limits(cfg)
    items = _timeline(utterances, keyframes)
    if not items:
        return []
    atoms = _atoms(items)
    n = len(atoms)

    # cover[i]: the latest end of anything in atoms[0..i]
    cover: list[float] = []
    latest = -math.inf
    for atom in atoms:
        latest = max(latest, atom.end)
        cover.append(latest)

    hole_s = coverage_hole_seconds(cfg, keyframes)
    holes = {c for c in range(1, n) if atoms[c].start - cover[c - 1] >= hole_s}
    cuts = holes | _pause_cuts(atoms, cover, gap_s)

    # spans between the mandatory boundaries, each cut further if it is too long
    pieces: list[_Piece] = []
    bounds = [0, *sorted(cuts), n]
    gains: list[float] | None = None
    for lo, hi in zip(bounds, bounds[1:], strict=False):
        inner: list[int] = []
        if hi - lo > 1 and _duration(atoms, lo, hi) > max_s:
            if gains is None:
                gains = _cut_gains(atoms, cover, gap_s)
            inner = _split_long(atoms, lo, hi, gains, min_s, max_s)
        edges = [lo, *inner, hi]
        for a, b in zip(edges, edges[1:], strict=False):
            pieces.append(_Piece(a, b, max(atom.end for atom in atoms[a:b])))

    pieces = _merge_short(pieces, atoms, cover, holes, min_s, max_s)

    moments: list[Moment] = []
    for idx, piece in enumerate(pieces):
        ts0 = atoms[piece.lo].start
        ts1 = piece.end if piece.hi >= n else min(piece.end, atoms[piece.hi].start)
        moments.append(
            Moment(
                session_id=session.id,
                idx=idx,
                ts0=ts0,
                ts1=max(ts0, ts1),
                utterance_ids=[i for atom in atoms[piece.lo : piece.hi] for i in atom.utterance_ids],
                keyframe_ids=[i for atom in atoms[piece.lo : piece.hi] for i in atom.keyframe_ids],
            )
        )
    log.debug(
        "session %s: %d utterances + %d keyframes -> %d moments (gap %.0fs, min %.0fs, max %.0fs, hole %.0fs)",
        session.id, len(utterances), len(keyframes), len(moments), gap_s, min_s, max_s, hole_s,
    )  # fmt: skip
    return moments


# -- settings ------------------------------------------------------------------


def _finite(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _limits(cfg: NotesSettings) -> tuple[float, float, float]:
    """(gap, min, max) seconds with nonsensical settings replaced by harmless ones."""
    gap_s = float(cfg.moment_gap_seconds) if _finite(cfg.moment_gap_seconds) else _DEFAULT_GAP_SECONDS
    if gap_s <= 0:
        gap_s = _DEFAULT_GAP_SECONDS
    max_s = float(cfg.moment_max_seconds) if _finite(cfg.moment_max_seconds) else math.inf
    if max_s <= 0:
        max_s = math.inf
    min_s = float(cfg.moment_min_seconds) if _finite(cfg.moment_min_seconds) else 0.0
    min_s = min(max(0.0, min_s), max_s)
    return gap_s, min_s, max_s


# -- timeline ------------------------------------------------------------------


def _timeline(utterances: list[Utterance], keyframes: list[Keyframe]) -> list[_Item]:
    """Utterances and keyframes as one list sorted by start time."""
    keyed: list[tuple[float, int, float, int, int, _Item]] = []
    dropped = 0
    for order, u in enumerate(utterances):
        if not _finite(u.ts0):
            dropped += 1
            continue
        start = float(u.ts0)
        end = float(u.ts1) if _finite(u.ts1) and u.ts1 >= start else start
        item = _Item(start, end, True, u.id, u.clip_id)
        keyed.append((start, 0, end, u.id if u.id is not None else -1, order, item))
    for order, k in enumerate(keyframes):
        if not _finite(k.ts):
            dropped += 1
            continue
        ts = float(k.ts)
        novelty = float(k.novelty) if _finite(k.novelty) else 0.0
        item = _Item(ts, ts, False, k.id, k.clip_id, scene=k.reason == "scene", novelty=novelty)
        keyed.append((ts, 1, ts, k.id if k.id is not None else -1, order, item))
    if dropped:
        log.warning("ignored %d utterances/keyframes without a usable timestamp", dropped)
    keyed.sort(key=lambda entry: entry[:5])
    return [entry[5] for entry in keyed]


def _atoms(items: list[_Item]) -> list[_Atom]:
    """Group the timeline into units a boundary may never split.

    A new atom starts at an item only if that item starts strictly later than
    the previous one and nothing before it is still running (give or take
    OVERLAP_TOLERANCE).
    """
    atoms: list[_Atom] = []
    running_end = -math.inf  # latest end of anything seen so far
    previous_start = -math.inf
    for item in items:
        if not atoms or (item.start > previous_start and item.start >= running_end - OVERLAP_TOLERANCE):
            atoms.append(_Atom(item.start, item.end))
        atom = atoms[-1]
        atom.end = max(atom.end, item.end)
        if item.speech:
            atom.speech = True
            atom.visual = 0.0  # a change of scene while someone is talking is not a place to cut
            if item.ref is not None:
                atom.utterance_ids.append(item.ref)
        else:
            if not atom.speech:
                atom.visual = max(atom.visual, _visual_strength(item))
            if item.ref is not None:
                atom.keyframe_ids.append(item.ref)
        running_end = max(running_end, item.end)
        previous_start = item.start
    return atoms


def _visual_strength(item: _Item) -> float:
    strength = _GAIN_SCENE if item.scene else 0.0
    if item.novelty >= HIGH_NOVELTY:
        strength = max(strength, _GAIN_NOVEL * min(1.0, item.novelty))
    return strength


def _duration(atoms: list[_Atom], lo: int, hi: int) -> float:
    """Length of the moment that atoms[lo:hi] would make."""
    end = max(atom.end for atom in atoms[lo:hi])
    if hi < len(atoms):
        end = min(end, atoms[hi].start)
    return max(0.0, end - atoms[lo].start)


# -- mandatory boundaries --------------------------------------------------------


def _pause_cuts(atoms: list[_Atom], cover: list[float], gap_s: float) -> set[int]:
    """Boundaries caused by pauses in speech (a cut ``c`` means: a moment starts at atoms[c])."""
    n = len(atoms)
    speech = [i for i, atom in enumerate(atoms) if atom.speech]
    if not speech:
        return set()
    cuts: set[int] = set()
    attach = gap_s / 2.0

    def tail_end(lo: int, hi: int, speech_end: float) -> int:
        """First silent atom in lo..hi that no longer belongs to the speech before it."""
        i = lo
        while i < hi and atoms[i].start - speech_end <= attach and atoms[i].visual <= 0.0:
            i += 1
        return i

    def head_start(lo: int, hi: int) -> int:
        """First silent atom in lo..hi that already belongs to the speech starting at atoms[hi]."""
        i = hi
        while i > lo and atoms[hi].start - atoms[i - 1].start <= attach:
            i -= 1
            if atoms[i].visual > 0.0:  # the scene changed here: nothing earlier belongs to it
                break
        return i

    first = speech[0]
    if first > 0 and atoms[first].start - atoms[0].start >= gap_s:  # silent lead-in
        head = head_start(0, first)
        if head > 0:
            cuts.add(head)
    for p, q in zip(speech, speech[1:], strict=False):
        if atoms[q].start - cover[p] < gap_s:
            continue
        tail = tail_end(p + 1, q, cover[p])
        head = head_start(tail, q)
        cuts.add(tail)  # tail == q when no keyframe was left over: one boundary right before the speech
        if head > tail:
            cuts.add(head)  # the silent stretch in between is a span of its own
    last = speech[-1]
    if last < n - 1 and atoms[n - 1].start - cover[last] >= gap_s:  # silent tail
        tail = tail_end(last + 1, n, cover[last])
        if tail < n:
            cuts.add(tail)
    return cuts


# -- too long: split ---------------------------------------------------------------


def _cut_gains(atoms: list[_Atom], cover: list[float], gap_s: float) -> list[float]:
    """How good a place each atom is to start a new moment at (index 0 is unused)."""
    n = len(atoms)
    next_speech_start: list[float | None] = [None] * n
    upcoming: float | None = None
    for i in range(n - 1, -1, -1):
        if atoms[i].speech:
            upcoming = atoms[i].start
        next_speech_start[i] = upcoming
    gains = [0.0] * n
    speech_end: float | None = None  # end of the last speech before atom c
    for c in range(1, n):
        if atoms[c - 1].speech:
            speech_end = cover[c - 1]
        empty = max(0.0, atoms[c].start - cover[c - 1])
        resumes = next_speech_start[c]
        pause = (resumes if resumes is not None else atoms[c].start) - (
            speech_end if speech_end is not None else cover[c - 1]
        )
        pause = max(pause, empty)
        gains[c] = (
            _GAIN_PAUSE * min(1.0, pause / gap_s) + _GAIN_EMPTY * min(1.0, empty / gap_s) + atoms[c].visual
        )
    return gains


def _split_long(
    atoms: list[_Atom], lo: int, hi: int, gains: list[float], min_s: float, max_s: float
) -> list[int]:
    """Where to cut atoms[lo:hi] so that no piece exceeds ``max_s`` (if that is possible at all).

    Optimal partition by dynamic programming over the atoms; the inner loop only
    looks back as far as one maximum-length piece reaches, so the cost is
    O(atoms x atoms-per-piece) even for a day-long span.
    """
    n = len(atoms)
    m = hi - lo
    best = [math.inf] * (m + 1)
    back = [0] * (m + 1)
    best[0] = 0.0
    for i in range(1, m + 1):
        stop = atoms[lo + i].start if lo + i < n else math.inf  # a piece ends where the next one starts
        end = -math.inf
        for j in range(i - 1, -1, -1):
            first = atoms[lo + j]
            end = max(end, first.end)
            duration = max(0.0, min(end, stop) - first.start)
            if duration > max_s and j < i - 1:
                break  # longer pieces only get worse; a single over-long atom is still allowed
            cost = best[j] + _COST_PIECE + _COST_EVEN * (duration / max_s) ** 2
            if duration > max_s:
                cost += _COST_OVER * (1.0 + (duration - max_s) / max_s)
            if duration < min_s:
                cost += _COST_SHORT * (1.0 - duration / min_s)
            if j > 0:
                cost -= gains[lo + j]
            if cost < best[i] - 1e-9:
                best[i] = cost
                back[i] = j
    cuts: list[int] = []
    i = m
    while i > 0:
        j = back[i]
        if j > 0:
            cuts.append(lo + j)
        i = j
    cuts.reverse()
    return cuts


# -- too short: merge --------------------------------------------------------------


def _merge_short(
    pieces: list[_Piece], atoms: list[_Atom], cover: list[float], holes: set[int], min_s: float, max_s: float
) -> list[_Piece]:
    """Merge moments shorter than ``min_s`` into the neighbour that is closer in time.

    Never across a coverage hole, never beyond ``max_s``; a join that does not
    cross a strong visual change is preferred over one that does.
    """
    if min_s <= 0 or len(pieces) < 2:
        return pieces
    n = len(atoms)

    def length(first: _Piece, last: _Piece) -> float:
        end = max(first.end, last.end)
        if last.hi < n:
            end = min(end, atoms[last.hi].start)
        return max(0.0, end - atoms[first.lo].start)

    def distance(right: _Piece) -> float:
        """Stretch with nothing at all just before ``right``."""
        return max(0.0, atoms[right.lo].start - cover[right.lo - 1])

    changed = True
    while changed:
        changed = False
        i = 0
        while i < len(pieces):
            piece = pieces[i]
            if length(piece, piece) >= min_s:
                i += 1
                continue
            # (joins across a strong visual change, distance, neighbour length, index of the left part)
            options: list[tuple[bool, float, float, int]] = []
            if i > 0 and piece.lo not in holes:
                left = pieces[i - 1]
                if length(left, piece) <= max_s:
                    options.append((atoms[piece.lo].visual > 0.0, distance(piece), length(left, left), i - 1))
            if i + 1 < len(pieces):
                right = pieces[i + 1]
                if right.lo not in holes and length(piece, right) <= max_s:
                    options.append((atoms[right.lo].visual > 0.0, distance(right), length(right, right), i))
            if not options:
                i += 1
                continue
            k = min(options)[3]
            a, b = pieces[k], pieces[k + 1]
            pieces[k : k + 2] = [_Piece(a.lo, b.hi, max(a.end, b.end))]
            changed = True
            i = k  # look at the merged moment again: it may still be too short
    return pieces
