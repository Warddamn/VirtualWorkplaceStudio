"""From recognised evidence (speech, on-screen text, captions) to notes.

Four jobs, each with a language model *or* without one:

* :func:`summarize_moments` - title, summary, tags, kind and salience of every moment;
* :func:`summarize_session` - the structured note of a whole session;
* :func:`summarize_day` - the digest of one calendar day;
* :func:`answer_question` - an answer built strictly from retrieved evidence.

How trust is kept
-----------------
* **The extractive result is always computed first.**  It only quotes: titles come from an
  on-screen heading or the first substantive sentence, action items from cue phrases
  ("remember to", "I'll", "Action:") with a due time only when one was said or shown,
  decisions from "we decided" / "agreed" / "going with", captured text straight from OCR.
  People and places are never guessed.  It is what you get without a model, and the safety
  net when a model call fails or returns something unusable - a failed call never fails a session.
* **Model output is checked before it is used.**  List caps are enforced; an action item,
  decision, question or key point must share most of its content words with the evidence;
  a name must have been said or shown; a due time or an owner that does not occur in the
  evidence is blanked; anything that traces back to a *media* moment (a TV or a video
  playing) is dropped.  Verbatim on-screen text is never taken from the model at all, and an
  explicit reminder ("remember to ...", "Action: ...") is kept even if the model overlooks it.
* **Prompts stay inside the model's budget.**  ``llm.context_tokens`` is the input budget;
  tokens are estimated as characters / 3.5.  Moments are batched, long sessions are split
  into parts and merged (map-reduce), and evidence is trimmed from the middle, never by
  cutting off the tail.
"""

from __future__ import annotations

import bisect
import logging
import math
import re
from collections import Counter
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from datetime import datetime
from difflib import SequenceMatcher
from typing import Any

from ..backends.base import LLM, BackendUnavailable
from ..backends.jsonutil import coerce_to_schema
from ..models import (
    MOMENT_KINDS,
    MOMENT_SALIENCE,
    ActionItem,
    Answer,
    DayDigest,
    Evidence,
    Keyframe,
    Moment,
    Session,
    SessionNote,
    Utterance,
)
from ..timeutil import fmt_duration, local_dt
from . import prompts

log = logging.getLogger("videonotes.summarize")

__all__ = [
    "CHARS_PER_TOKEN",
    "EXTRACTIVE",
    "QUIET_TITLE",
    "answer_question",
    "moment_context",
    "summarize_day",
    "summarize_moments",
    "summarize_session",
]

#: ``llm_backend`` of everything written without a language model.
EXTRACTIVE = "extractive"
#: Token estimate used for budgeting prompts (Latin-script text).
CHARS_PER_TOKEN = 3.5
#: Title of a moment in which nothing was said, shown or described.
QUIET_TITLE = "Quiet stretch"
MEDIA_TITLE = "TV or video playing"
QUIET_SESSION_TITLE = "Quiet recording"
QUIET_SESSION_SUMMARY = "No speech, readable text or scene descriptions were recognised in this recording."

#: A prompt with less room for evidence than this is not worth sending.
MIN_EVIDENCE_CHARS = 500
#: Moments per call for a local model (its answer must fit a small window) ...
MAX_MOMENTS_PER_CALL = 8
#: ... and for a backend with a large context window (fewer round trips).
MAX_MOMENTS_PER_LARGE_CALL = 24
_LARGE_CONTEXT_CHARS = 100_000
MOMENT_CONTEXT_CHARS = 6000
#: A session is never split into more LLM calls than this (evidence is condensed instead).
MAX_SESSION_PARTS = 12
#: After this many failed calls in a row the model is left alone for the rest of the job.
MAX_FAILURES_IN_A_ROW = 2

_BACKGROUND_SECONDS = 120.0
_BACKGROUND_WORDS = 100
_MAX_CAPTURED_ENTRIES = 60
_MAX_CAPTURED_ENTRY_CHARS = 1200


# =============================================================================
# Text helpers
# =============================================================================

_CONTROL = re.compile("[\x00-\x1f\x7f-\x9f\u200b-\u200f\u202a-\u202e\u2066-\u2069\ufeff]")
_RULER = re.compile(r"([=\-_#*~`<>])\1{2,}")
_WORD = re.compile(r"[^\W_]+(?:['’][^\W_]+)*")
_NOT_ALNUM = re.compile(r"[\W_]+")
_SENTENCE_SPLIT = re.compile(r"(?<=[.!?…])[\"'”’)\]]*\s+(?=[^\sa-z])")
#: "Dr." and dotted abbreviations ("p.m.", "U.S.", "e.g.") do not end a sentence; a lone letter does ("row G.").
_ABBREVIATION = re.compile(r"(?:\b(?:mr|mrs|ms|dr|prof|vs|etc|approx)\.|\b(?:[A-Za-z]\.){2,})$", re.I)
_TERMINAL = ".!?…"

_STOP = frozenset(
    """a about above after again all also am an and any are aren't as at be because been before being below
    between both but by can can't cannot could couldn't did didn't do does doesn't doing don't down during each
    few for from further had hadn't has hasn't have haven't having he her here hers herself him himself his how
    i i'd i'll i'm i've if in into is isn't it it's its itself just let's me more most my myself no nor not of
    off on once only or other our ours ourselves out over own same she should shouldn't so some such than that
    that's the their theirs them themselves then there there's these they they're this those through to too
    under until up very was wasn't we we'd we'll we're we've were weren't what what's when where which while
    who whom why will with won't would wouldn't you you'd you'll you're you've your yours yourself yourselves
    got get gets going gonna one will shall may might must
    """.split()
)
_FILLER = frozenset(
    """ok okay yeah yes yep nope right well alright um uh hmm oh hey hi hello thanks thank please like really
    actually basically know mean guess kind sort thing things stuff quick note self gonna wanna lot bit maybe
    """.split()
)
_LEADING_FILLER = re.compile(
    r"^(?:(?:ok(?:ay)?|so|well|alright|all right|right|yeah|yes|um+|uh+|and|but|now|hey|oh|anyway|listen)\b[\s,.!-]*)+", re.I
)

_NUMBER_WORDS = {
    "zero": "0", "one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7",
    "eight": "8", "nine": "9", "ten": "10", "eleven": "11", "twelve": "12", "thirteen": "13", "fourteen": "14",
    "fifteen": "15", "sixteen": "16", "seventeen": "17", "eighteen": "18", "nineteen": "19", "twenty": "20",
    "thirty": "30", "forty": "40", "fifty": "50", "first": "1", "second": "2", "third": "3", "fourth": "4",
    "fifth": "5", "sixth": "6", "seventh": "7", "eighth": "8", "ninth": "9", "tenth": "10", "eleventh": "11",
    "twelfth": "12", "thirteenth": "13", "fourteenth": "14", "fifteenth": "15", "sixteenth": "16",
    "seventeenth": "17", "eighteenth": "18", "nineteenth": "19", "twentieth": "20", "thirtieth": "30",
}  # fmt: skip


def _finite(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _one_line(text: object) -> str:
    """Text on one line, without control or direction-override characters."""
    return " ".join(_CONTROL.sub(" ", str(text if text is not None else "")).split())


def _clip(text: str, limit: int) -> str:
    """At most ``limit`` characters, cut at a word boundary and marked with an ellipsis."""
    if len(text) <= limit:
        return text
    if limit <= 1:
        return text[: max(0, limit)]
    cut = text[: limit - 1]
    space = cut.rfind(" ")
    if space > limit * 0.6:
        cut = cut[:space]
    return cut.rstrip(" ,;:-") + "…"


def _squeeze(text: str, limit: int) -> str:
    """At most ``limit`` characters, keeping the start and the end and dropping the middle."""
    if len(text) <= limit:
        return text
    marker = " […] "
    if limit <= len(marker) + 8:
        return text[: max(0, limit)]
    head = (limit - len(marker)) * 2 // 3
    tail = limit - len(marker) - head
    return text[:head].rstrip() + marker + text[len(text) - tail :].lstrip()


def _evidence_text(text: object, limit: int) -> str:
    """Captured text made safe to place in a prompt: one line, no rulers that could imitate
    the evidence delimiters, bounded length."""
    return _clip(_RULER.sub(r"\1", _one_line(text)), limit)


def _tokens(text: str) -> list[str]:
    return [w.lower().replace("’", "'") for w in _WORD.findall(text)]


def _stem(word: str) -> str:
    """A very light stemmer, enough to match "sensors" with "sensor" and "parked" with "park"."""
    w = word.lower()
    for suffix in ("'s", "’s"):
        if w.endswith(suffix):
            w = w[: -len(suffix)]
    if len(w) > 4 and w.endswith("ies"):
        return w[:-3] + "y"
    if len(w) > 5 and w.endswith("ing"):
        return w[:-3]
    if len(w) > 4 and w.endswith("ed"):
        return w[:-2]
    if len(w) > 3 and w.endswith("s") and not w.endswith("ss"):
        return w[:-1]
    return w


def _content(text: str) -> list[str]:
    """Stems of the words that carry meaning (no stop words, no one- or two-letter words)."""
    out = []
    for tok in _tokens(text):
        if tok in _STOP:
            continue
        if len(tok) >= 3 or any(ch.isdigit() for ch in tok):
            out.append(_stem(tok))
    return out


def _norm_key(text: str) -> str:
    """Letters and digits only, case-folded: equal for two readings that differ in case, spacing or punctuation."""
    return _NOT_ALNUM.sub("", text.casefold())


def _sentences(text: str) -> list[str]:
    """Split text into sentences (text without punctuation stays one sentence)."""
    text = _one_line(text)
    if not text:
        return []
    merged: list[str] = []
    for part in _SENTENCE_SPLIT.split(text):
        if merged and _ABBREVIATION.search(merged[-1]):
            merged[-1] += " " + part
        else:
            merged.append(part)
    return [m.strip() for m in merged if m.strip()]


def _substance(sentence: str) -> int:
    """How many meaningful words a sentence has once fillers are ignored."""
    return sum(1 for tok in _tokens(sentence) if tok not in _STOP and tok not in _FILLER and len(tok) >= 3)


def _capitalise(text: str) -> str:
    return text[:1].upper() + text[1:] if text else text


def _first_sentences(text: str, count: int) -> str:
    return " ".join(_sentences(text)[:count])


def _similar(a: frozenset[str], b: frozenset[str]) -> bool:
    """Two short statements say the same thing (one may be a little more specific)."""
    if not a or not b:
        return False
    shared = len(a & b)
    small = min(len(a), len(b))
    if shared == small and small >= 2:
        return True
    return shared / len(a | b) >= 0.75


def _statement_key(text: str) -> frozenset[str]:
    return frozenset(_content(text)) or frozenset({_norm_key(text)})


def _dedupe(items: Iterable[str], limit: int) -> list[str]:
    """Case-insensitive, wording-tolerant de-duplication keeping the first (or the more specific) entry."""
    out: list[str] = []
    keys: list[frozenset[str]] = []
    seen: set[str] = set()
    for raw in items:
        text = _one_line(raw)
        norm = _norm_key(text)
        if not norm or norm in seen:
            continue
        seen.add(norm)
        key = _statement_key(text)
        for i, other in enumerate(keys):
            if key == other or _similar(key, other):
                if len(key) > len(other):  # the later wording says more: keep that one
                    out[i], keys[i] = text, key
                break
        else:
            out.append(text)
            keys.append(key)
    return out[:limit]


def _merge_actions(items: Iterable[ActionItem], limit: int, ranks: Sequence[int] | None = None) -> list[ActionItem]:
    """De-duplicate action items; a twin contributes its due / owner / time when the kept one lacks them.

    The result keeps the order given.  When more than ``limit`` remain, the first ones are
    kept - or, with ``ranks`` (one number per item, higher = more worth keeping), the best
    ranked ones.
    """
    out: list[ActionItem] = []
    keys: list[frozenset[str]] = []
    worth: list[int] = []
    for n, item in enumerate(items):
        text = _one_line(item.text)
        if not _norm_key(text):
            continue
        key = _statement_key(text)
        ts = item.ts if _finite(item.ts) else None
        rank = ranks[n] if ranks is not None and n < len(ranks) else 0
        for i, other in enumerate(keys):
            if key == other or _similar(key, other):
                kept = out[i]
                if len(key) > len(other):
                    kept.text, keys[i] = text, key
                kept.due = kept.due or _one_line(item.due)
                kept.owner = kept.owner or _one_line(item.owner)
                if kept.ts is None:
                    kept.ts = ts
                worth[i] = max(worth[i], rank)
                break
        else:
            out.append(ActionItem(text=text, owner=_one_line(item.owner), due=_one_line(item.due), ts=ts))
            keys.append(key)
            worth.append(rank)
    if len(out) > limit:
        best = sorted(sorted(range(len(out)), key=lambda i: (-worth[i], i))[: max(0, limit)])
        out = [out[i] for i in best]
    return out


def _chars_per_token(sample: str) -> float:
    """Characters per token to budget with: 3.5 for Latin scripts, far fewer for others."""
    letters = [ch for ch in sample[:4000] if ch.isalpha()]
    if not letters:
        return CHARS_PER_TOKEN
    wide = sum(1 for ch in letters if ord(ch) >= 0x2E80)
    other = sum(1 for ch in letters if 0x250 <= ord(ch) < 0x2E80)
    if wide / len(letters) > 0.2:
        return 1.0
    if other / len(letters) > 0.2:
        return 1.5
    return CHARS_PER_TOKEN


def _budget_chars(llm: Any, sample: str) -> int:
    """Characters one whole prompt (system + user text) may have for this model."""
    try:
        tokens = int(getattr(llm, "context_tokens", 0) or 0)
    except (TypeError, ValueError):
        tokens = 0
    return int(tokens * _chars_per_token(sample)) if tokens > 0 else 0


def _coerced(raw: object, schema: dict[str, Any]) -> dict[str, Any]:
    """``raw`` forced into the shape of ``schema``; the empty shape when it cannot be (a model
    may emit ``NaN`` or ``Infinity`` where a number belongs, which no integer can hold)."""
    try:
        return coerce_to_schema(raw if isinstance(raw, dict) else {}, schema)
    except (ValueError, OverflowError, TypeError, RecursionError):
        return coerce_to_schema({}, schema)


def _llm_name(llm: Any) -> str:
    return _one_line(getattr(llm, "name", "")) or "llm"


def _local(ts: object) -> datetime | None:
    """Local time of a timestamp, or None when it is not a usable point in time."""
    if not _finite(ts):
        return None
    try:
        return local_dt(float(ts))  # type: ignore[arg-type]
    except (OverflowError, OSError, ValueError):
        return None


def _clock(ts: object, fmt: str = "%H:%M") -> str:
    when = _local(ts)
    return when.strftime(fmt) if when is not None else "--:--"


def _span(ts0: object, ts1: object) -> str:
    a = _clock(ts0)
    b = _clock(ts1) if _local(ts1) is not None else a
    return a if a == b else f"{a}–{b}"


# =============================================================================
# Evidence: what belongs to a moment
# =============================================================================


@dataclass(slots=True)
class _Sentence:
    text: str
    ts: float | None
    source: str = "said"  # "said" | "shown"


@dataclass(slots=True)
class _TextBlock:
    """New on-screen text first seen in one keyframe."""

    ts: float
    lines: list[str]


@dataclass(slots=True)
class _Cue:
    text: str
    ts: float | None
    due: str = ""
    source: str = "said"
    #: an explicit reminder ("remember to ...", "remind me ...", a labelled to-do on a surface)
    explicit: bool = False
    #: a suggestion rather than a commitment ("we should maybe ...", "let's ...")
    tentative: bool = False

    @property
    def rank(self) -> int:
        """How much an action item is worth keeping when there are too many."""
        if self.explicit:
            return 3
        if self.due:
            return 2
        return 0 if self.tentative else 1


class _TextDeduper:
    """Keeps only on-screen lines not seen before; the same sign read twice with a character
    or two different, or only partly, is still the same sign."""

    def __init__(self) -> None:
        self._keys: set[str] = set()
        self._recent: list[tuple[str, str]] = []  # (letters and digits of a kept line, its digits)

    def new_lines(self, lines: Iterable[str]) -> list[str]:
        out: list[str] = []
        for line in lines:
            key = _norm_key(line)
            if len(key) < 2 or key in self._keys:
                continue
            self._keys.add(key)
            digits = "".join(ch for ch in key if ch.isdigit())
            if self._near(key, digits):
                continue
            self._recent.append((key, digits))
            if len(self._recent) > 40:
                del self._recent[0]
            out.append(line)
        return out

    def _near(self, key: str, digits: str) -> bool:
        if len(key) < 4:
            return False
        matcher: SequenceMatcher[str] | None = None
        slack = max(2, len(key) // 5)
        for other, other_digits in reversed(self._recent):
            if key in other:
                return True  # a partial read of a line already kept
            # "Slide 3" and "Slide 4", or two prices, are different texts, not a misread
            if len(key) < 8 or other_digits != digits or abs(len(other) - len(key)) > slack:
                continue
            if matcher is None:
                matcher = SequenceMatcher(None, autojunk=False)
                matcher.set_seq2(key)
            matcher.set_seq1(other)
            if matcher.real_quick_ratio() >= 0.88 and matcher.quick_ratio() >= 0.88 and matcher.ratio() >= 0.88:
                return True
        return False


def _ocr_lines(keyframe: Keyframe) -> list[str]:
    if not keyframe.ocr_text:
        return []
    lines = [_one_line(line) for line in str(keyframe.ocr_text).splitlines()]
    return [_clip(line, 300) for line in lines if len(_norm_key(line)) >= 2]


def _speech_sentences(utterances: Sequence[Utterance]) -> list[_Sentence]:
    """Sentences with the time they started at. A sentence that speech-to-text cut across two
    utterances is put back together (only for transcripts that are punctuated at all)."""
    punctuated = any(ch in u.text for u in utterances for ch in ".?!")
    out: list[_Sentence] = []
    buf = ""
    starts: list[tuple[int, float]] = []
    last_end: float | None = None

    def flush() -> None:
        nonlocal buf, starts
        pos = 0
        offsets = [o for o, _ in starts]
        for sent in _sentences(buf):
            at = buf.find(sent, pos)
            at = pos if at < 0 else at
            pos = at + len(sent)
            ts = starts[max(0, bisect.bisect_right(offsets, at) - 1)][1]
            if sent.isupper() and len(sent) > 3:  # some recognisers shout
                sent = sent[0] + sent[1:].lower()
            out.append(_Sentence(sent, ts))
        buf, starts = "", []

    for u in utterances:
        text = _one_line(u.text)
        if not text:
            continue
        if buf:
            gap = u.ts0 - last_end if last_end is not None else math.inf
            if not punctuated or buf[-1] in _TERMINAL or gap > 3.0 or len(buf) > 400:
                flush()
        if buf:
            buf += " "
        starts.append((len(buf), u.ts0))
        buf += text
        last_end = u.ts1 if _finite(u.ts1) and u.ts1 >= u.ts0 else u.ts0
    if buf:
        flush()
    return out


@dataclass
class _Facts:
    """Everything recognised inside one moment, prepared once."""

    moment: Moment
    utterances: list[Utterance]
    keyframes: list[Keyframe]
    sentences: list[_Sentence] = field(default_factory=list)
    blocks: list[_TextBlock] = field(default_factory=list)
    captions: list[tuple[float, str]] = field(default_factory=list)
    words: int = 0
    actions: list[_Cue] = field(default_factory=list)
    decisions: list[_Cue] = field(default_factory=list)
    questions: list[_Cue] = field(default_factory=list)

    @property
    def duration(self) -> float:
        d = self.moment.ts1 - self.moment.ts0
        return d if _finite(d) and d > 0 else 0.0

    @property
    def text_lines(self) -> list[str]:
        return [line for block in self.blocks for line in block.lines]

    @property
    def empty(self) -> bool:
        return not (self.sentences or self.blocks or self.captions)

    @property
    def speech(self) -> str:
        return " ".join(s.text for s in self.sentences)

    @property
    def caption_text(self) -> str:
        return " ".join(c for _, c in self.captions)

    @property
    def substantial_text(self) -> bool:
        lines = self.text_lines
        return len(lines) >= 3 or sum(len(_norm_key(line)) for line in lines) >= 40

    @property
    def self_note(self) -> bool:
        return bool(_SELF_NOTE.search(self.speech))


def _build_facts(moment: Moment, utterances: list[Utterance], keyframes: list[Keyframe]) -> _Facts:
    facts = _Facts(moment, utterances, keyframes)
    facts.sentences = _speech_sentences(utterances)
    facts.words = sum(len(_tokens(s.text)) for s in facts.sentences)
    deduper = _TextDeduper()
    last_caption = ""
    for kf in keyframes:
        fresh = deduper.new_lines(_ocr_lines(kf))
        if fresh:
            facts.blocks.append(_TextBlock(kf.ts, fresh))
        caption = _one_line(kf.caption or "")
        if caption and _norm_key(caption) != last_caption:
            facts.captions.append((kf.ts, caption))
            last_caption = _norm_key(caption)
    return facts


class _Index:
    """Finds the utterances and keyframes of a moment: by the ids it lists, else by time."""

    def __init__(self, utterances: Iterable[Utterance], keyframes: Iterable[Keyframe]):
        self._u = sorted((u for u in utterances if _finite(u.ts0)), key=lambda u: u.ts0)
        self._k = sorted((k for k in keyframes if _finite(k.ts)), key=lambda k: k.ts)
        self._ut = [u.ts0 for u in self._u]
        self._kt = [k.ts for k in self._k]
        self._u_by_id = {u.id: u for u in self._u if u.id is not None}
        self._k_by_id = {k.id: k for k in self._k if k.id is not None}

    @property
    def bounds(self) -> tuple[float, float] | None:
        times = self._ut[:1] + self._ut[-1:] + self._kt[:1] + self._kt[-1:]
        times += [u.ts1 for u in self._u[-50:] if _finite(u.ts1)]
        return (min(times), max(times)) if times else None

    def members(self, moment: Moment, until: float | None = None) -> tuple[list[Utterance], list[Keyframe]]:
        us = [self._u_by_id[i] for i in moment.utterance_ids or [] if i in self._u_by_id]
        ks = [self._k_by_id[i] for i in moment.keyframe_ids or [] if i in self._k_by_id]
        if us or ks:
            return sorted(us, key=lambda u: u.ts0), sorted(ks, key=lambda k: k.ts)
        if not _finite(moment.ts0):
            return [], []
        lo = moment.ts0
        if until is not None and _finite(until) and until > lo:
            u_hi, k_hi = bisect.bisect_left(self._ut, until), bisect.bisect_left(self._kt, until)
        else:
            hi = moment.ts1 if _finite(moment.ts1) and moment.ts1 >= lo else lo
            u_hi, k_hi = bisect.bisect_right(self._ut, hi), bisect.bisect_right(self._kt, hi)
        return (
            self._u[bisect.bisect_left(self._ut, lo) : u_hi],
            self._k[bisect.bisect_left(self._kt, lo) : k_hi],
        )

    def facts(self, moments: Sequence[Moment]) -> list[_Facts]:
        """Facts for every moment, in the order given. A moment without ids owns ``[ts0, next ts0)``."""
        order = sorted(range(len(moments)), key=lambda i: (moments[i].ts0 if _finite(moments[i].ts0) else math.inf, i))
        out: list[_Facts | None] = [None] * len(moments)
        for pos, i in enumerate(order):
            until = moments[order[pos + 1]].ts0 if pos + 1 < len(order) else None
            us, ks = self.members(moments[i], until)
            facts = _build_facts(moments[i], us, ks)
            _find_cues(facts)
            out[i] = facts
        return [f for f in out if f is not None]


# =============================================================================
# Evidence as prompt text
# =============================================================================

_LABELS = {"said": prompts.SAID, "text": prompts.TEXT, "seen": prompts.SEEN}


@dataclass(slots=True)
class _Line:
    ts: float
    kind: str  # "said" | "text" | "seen"
    text: str

    def render(self) -> str:
        return f"[{_clock(self.ts, '%H:%M:%S')}] {_LABELS[self.kind]}: {self.text}"


def _context_lines(facts: _Facts) -> list[_Line]:
    lines: list[tuple[float, int, _Line]] = []
    current: _Line | None = None
    last_end = -math.inf
    for u in facts.utterances:
        text = _evidence_text(u.text, 600)
        if not text:
            continue
        # consecutive short utterances share a line: less overhead, same information
        if current is not None and u.ts0 - last_end <= 2.0 and len(current.text) + len(text) <= 300:
            current.text += " " + text
        else:
            current = _Line(u.ts0, "said", text)
            lines.append((u.ts0, 0, current))
        last_end = u.ts1 if _finite(u.ts1) and u.ts1 >= u.ts0 else u.ts0
    for block in facts.blocks:
        text = " | ".join(_evidence_text(line, 300) for line in block.lines)
        lines.append((block.ts, 1, _Line(block.ts, "text", text)))
    for ts, caption in facts.captions:
        lines.append((ts, 2, _Line(ts, "seen", _evidence_text(caption, 300))))
    lines.sort(key=lambda entry: entry[:2])
    return [entry[2] for entry in lines]


def _take_from_ends(costs: list[int], room: int) -> tuple[int, int]:
    """How many items to keep from the start and from the end so that their costs fit ``room``."""
    head, tail = 0, 0
    n = len(costs)
    from_head = True
    while head + tail < n:
        i = head if from_head else n - 1 - tail
        if costs[i] > room:
            other = n - 1 - tail if from_head else head
            if head + tail < n - 1 and costs[other] <= room:  # the other side still has a line that fits
                from_head = not from_head
                continue
            break
        room -= costs[i]
        if from_head:
            head += 1
        else:
            tail += 1
        from_head = not from_head
    return head, tail


def _fit_lines(lines: list[_Line], max_chars: int) -> str:
    """Render evidence lines within ``max_chars``.

    When there is too much: every distinct on-screen text stays (shortened line by line if it
    has to be), and speech / captions are kept from the start and from the end, with a note
    where the middle was left out.
    """
    max_chars = max(0, int(max_chars))
    rendered = [line.render() for line in lines]
    if sum(len(r) + 1 for r in rendered) - 1 <= max_chars:
        return "\n".join(rendered)
    if max_chars < 120:
        return _squeeze("\n".join(rendered), max_chars)

    text_idx = [i for i, line in enumerate(lines) if line.kind == "text"]
    other_idx = [i for i, line in enumerate(lines) if line.kind != "text"]
    keep: dict[int, str] = {}
    notes: dict[int, str] = {}  # index before which a "left out" note goes
    note_room = 48

    # on-screen text gets at least 60 % of the room, and whatever speech and captions do not need
    other_total = sum(len(rendered[i]) + 1 for i in other_idx)
    text_room = max(int(max_chars * 0.6), max_chars - other_total - 2 * note_room) if other_idx else max_chars - note_room
    if text_idx:
        if sum(len(rendered[i]) + 1 for i in text_idx) > text_room:
            per = max(48, text_room // len(text_idx) - 1)
            shortened = {i: _clip(rendered[i], per) for i in text_idx}
        else:
            shortened = {i: rendered[i] for i in text_idx}
        costs = [len(shortened[i]) + 1 for i in text_idx]
        head, tail = _take_from_ends(costs, text_room)
        kept = text_idx[:head] + text_idx[len(text_idx) - tail :]
        for i in kept:
            keep[i] = shortened[i]
        dropped = len(text_idx) - len(kept)
        if dropped:
            notes[text_idx[head]] = f"[… {dropped} more lines of on-screen text left out …]"

    used = sum(len(v) + 1 for v in keep.values()) + sum(len(v) + 1 for v in notes.values())
    room = max_chars - used - note_room
    if other_idx:
        costs = [len(rendered[i]) + 1 for i in other_idx]
        head, tail = _take_from_ends(costs, room)
        if head + tail == 0 and room >= 80:  # not even one line fits whole: keep the start of the first
            keep[other_idx[0]] = _clip(rendered[other_idx[0]], room - 1)
            head = 1
        else:
            for i in other_idx[:head] + other_idx[len(other_idx) - tail :]:
                keep[i] = rendered[i]
        dropped = len(other_idx) - head - tail
        if dropped:
            first = other_idx[head]
            notes[first] = (notes[first] + "\n" if first in notes else "") + f"[… {dropped} lines left out here …]"

    out: list[str] = []
    for i in range(len(lines)):
        if i in notes:
            out.append(notes[i])
        if i in keep:
            out.append(keep[i])
    return _squeeze("\n".join(out), max_chars)


def moment_context(
    moment: Moment, utterances: list[Utterance], keyframes: list[Keyframe], *, max_chars: int = MOMENT_CONTEXT_CHARS
) -> str:
    """The fused evidence for one moment: timestamped speech, on-screen text, captions.

    One line per piece of evidence in time order, each starting with the local clock time::

        [14:32:05] SAID: Remember to email the quarterly budget to Sarah before Friday.
        [14:32:21] TEXT IN VIEW: Launch plan Q3 | Ship Falcon beta by June 14
        [14:32:21] SEEN: A whiteboard with handwritten notes.

    ``utterances`` / ``keyframes`` may be the whole session: the moment's own are picked by
    the ids it lists, or by its time range when it lists none.  On-screen text that repeats
    from keyframe to keyframe appears once.  The result never exceeds ``max_chars``; when the
    evidence is longer, the start, the end and every distinct on-screen text are kept and the
    middle of the speech is left out (and marked).
    """
    us, ks = _Index(utterances, keyframes).members(moment)
    return _fit_lines(_context_lines(_build_facts(moment, us, ks)), max_chars)


# =============================================================================
# Cue phrases: action items, decisions, questions (extractive)
# =============================================================================

_SELF_NOTE = re.compile(
    r"\b(?:note to (?:my)?self|memo to (?:my)?self|remind me|reminder to (?:my)?self|remember to|don['’]?t forget)\b", re.I
)
_EXPLICIT_REMINDER = re.compile(
    r"\b(?:remind\s+me|remember\s+to|don['’]?t\s+(?:let\s+me\s+)?forget|(?:note|memo|reminder)\s+to\s+(?:my)?self)\b", re.I
)
_TENTATIVE = re.compile(
    r"\b(?:let['’]?s|(?:we|i)\s+should|maybe|perhaps|might|could|some\s?day|some\s?time|at\s+some\s+point|if\s+we)\b", re.I
)
_NEGATED = re.compile(r"(?:\bnot|n['’]t|\bnever|\bno need|\bwithout|\bhardly)\s+(?:\w+\s+){0,2}$", re.I)

_ACTION_CUE = re.compile(
    r"""(?ix)
    (?P<pre>
        \b(?:please\s+)?remind\s+me\s+(?:to|about)\s+
      | \b(?:i|we)\s+(?:really\s+|still\s+|also\s+|just\s+)?(?:need|have|ought|got)\s+to\s+
      | \b(?:i|we)(?:['’]ve|\s+have)\s+got\s+to\s+
      | \b(?:i|we)\s+(?:gotta|must|should|shall)\s+
      | \b(?:i|we)(?:['’]ll|\s+will)\s+(?:need\s+to\s+|have\s+to\s+)?
      | \b(?:i['’]m|i\s+am|we['’]re|we\s+are)\s+(?:going\s+to|gonna)\s+
      | \b(?:remember|need|needs|have|has)\s+to\s+
      | \bdon['’]?t\s+(?:let\s+me\s+)?forget\s+to\s+
      | \bmake\s+sure\s+(?:to\s+|that\s+)?
      | (?:\blet['’]s|^lets|(?<=[.,;!]\s)lets)\s+(?:not\s+forget\s+to\s+)?
      | \b(?:to[-\s]?do|action(?:\s+item)?s?|next\s+steps?|reminder)(?:\s*[:–—]\s*|\s+-\s+)
    )
    | (?P<keep>\bfollow(?:ing)?[-\s]up\s+(?:with|on|about)\b|\bdon['’]?t\s+forget\s+(?!to\b))
    """
)
#: On a surface only explicit labels count ("Action:", "TODO:", a checkbox); "Let's go places" on a
#: billboard is not a task.
_SHOWN_ACTION_CUE = re.compile(
    r"""(?ix)^\s*[-*•·]*\s*
    (?: (?:to[-\s]?do|action(?:\s+item)?s?|next\s+steps?|reminder)(?:\s*[:–—]\s*|\s+-\s+)
      | (?:remember\s+to|don['’]?t\s+forget(?:\s+to)?)\s+
      | (?:\[\s?\]|☐|□|▢)\s*
    )(?P<task>\S.*)$"""
)
_SHOWN_DECISION_CUE = re.compile(r"(?i)^\s*[-*•·]*\s*(?:final\s+)?decisions?\s*[:\-–—]\s*(?P<text>\S.*)$")
_DECISION_CUE = re.compile(
    r"""(?ix)
      \b(?:we|i|they|everyone|everybody|team)(?:['’]ve|\s+have|\s+all|\s+both)?\s+(?:decided|agreed|settled)\b
    | \bdecided\s+(?:to|that|on|against)\b
    | \bagreed\s+(?:to|that|on|upon)\b
    | \b(?:we['’]re|we\s+are|i['’]m|i\s+am|they['’]re)\s+going\s+with\b
    | \b(?:let['’]?s|we['’]ll|we\s+will|i['’]ll|i\s+will)\s+go\s+with\b
    | (?:^|[,.;:]\s*|\b(?:so|okay|ok|then|alright)\s+)going\s+with\b
    | \b(?:final\s+)?decision\s+(?:is|was)\b
    | \bdecision\s*[:\-–—]
    | \bsettled\s+on\b
    """
)

_MONTH = (
    r"(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|june?|july?|aug(?:ust)?|sep(?:t(?:ember)?)?|"
    r"oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)"
)
_ORDINAL = (
    r"(?:\d{1,2}(?:st|nd|rd|th)?|(?:twenty|thirty)[-\s](?:first|second|third|fourth|fifth|sixth|seventh|eighth|ninth)|"
    r"first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|eleventh|twelfth|thirteenth|fourteenth|"
    r"fifteenth|sixteenth|seventeenth|eighteenth|nineteenth|twentieth|thirtieth)"
)
_WEEKDAY = r"(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)"
_DAYPART = r"(?:\s+(?:morning|afternoon|evening|night))?"
_CLOCK = (
    r"(?:\d{1,2}:\d{2}(?:\s*(?:a\.?\s?m\.?|p\.?\s?m\.?))?|\d{1,2}\s*(?:a\.?\s?m\.?|p\.?\s?m\.?|o['’]clock)|"
    r"(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)(?:\s+(?:thirty|fifteen|forty[-\s]five))?"
    r"\s*(?:a\.?\s?m\.?|p\.?\s?m\.?|o['’]clock))"
)
_WHEN = (
    rf"(?:(?:the\s+)?end\s+of\s+(?:the\s+)?(?:day|week|month|year|quarter)|eod|eow|"
    rf"tomorrow{_DAYPART}|tonight|today|noon|midnight|lunch(?:time)?|dinner|breakfast|"
    rf"(?:next\s+|this\s+)?{_WEEKDAY}{_DAYPART}|(?:next|this)\s+(?:week|month|weekend)|the\s+weekend|"
    rf"{_MONTH}\.?\s+(?:the\s+)?{_ORDINAL}|(?:the\s+)?{_ORDINAL}\s+of\s+{_MONTH}|"
    rf"(?:jan(?:uary)?|feb(?:ruary)?|march|april|june|july|august|september|october|november|december)|"
    rf"\d{{1,2}}/\d{{1,2}}(?:/\d{{2,4}})?|{_CLOCK})"
)
#: "by Friday", "before Monday", "due June 14" - the deadline is group "due", kept as said.
_DUE = re.compile(rf"(?i)\b(?:by|before|until|no\s+later\s+than|due(?:\s+(?:on|by))?)\s+(?P<due>{_WHEN})(?![\w-])")
#: A bare day at the very end of a task: "... tomorrow", "... on Monday", "... next week".
_DUE_TRAILING = re.compile(
    rf"(?i)(?:\s+|^)(?:on\s+)?(?P<due>tomorrow{_DAYPART}|tonight|today|(?:this|next)\s+(?:week|month|weekend)|"
    rf"(?:next\s+|this\s+)?{_WEEKDAY}{_DAYPART})\s*$"
)
_CLAUSE_END = re.compile(r"\s*(?:[;—]|,\s+(?:because|so|but|and\s+then|which|or\s+else|if)\b|\s+(?:because|so\s+that)\b).*$", re.I)
_NEVER_TASKS = frozenset("say admit know think guess wonder assume suppose mention imagine".split())
_WEAK_STARTS = frozenset("go do be get have see leave run stop wait try come take look".split())
_NOT_TASKS = re.compile(r"^(?:be\s+(?:honest|fair|fine|ok(?:ay)?|sure|clear|able|back|right|there)|tell\s+you|see\s+(?:what|how|if)\b)", re.I)
_TRIVIAL_QUESTIONS = re.compile(
    r"^(?:(?:you\s+)?know(?:\s+what(?:\s+i\s+mean)?)?|right|really|ok(?:ay)?|what|huh|sorry|pardon|how\s+are\s+you(?:\s+doing)?|"
    r"how(?:['’]s|\s+is)\s+it\s+going|what(?:['’]s|\s+is)\s+up|you\s+see|is\s+that\s+(?:right|ok(?:ay)?)|"
    r"can\s+you\s+hear\s+me|does\s+that\s+make\s+sense)\W*$",
    re.I,
)


def _split_due(task: str) -> tuple[str, str]:
    """Take a stated deadline out of a task. Returns ``(task, due)``; due keeps the words as said."""
    task = task.rstrip(" .,;:!")
    match = _DUE.search(task) or _DUE_TRAILING.search(task)
    if not match:
        return task, ""
    due = _one_line(match.group("due")).strip(" .,;:")
    rest = _one_line(task[: match.start()] + " " + task[match.end() :])
    return rest.strip(" ,;:-"), due


def _tidy_task(task: str) -> str:
    task = _one_line(task).strip(" .,;:!-–—")
    cut = _CLAUSE_END.sub("", task)
    if len(cut.split()) >= 3:
        task = cut
    task = re.sub(r"^(?:to|that|and)\s+", "", task, flags=re.I).strip(" .,;:!-–—")
    words = task.split()
    if len(words) > prompts.ACTION_MAX_WORDS:
        task = " ".join(words[: prompts.ACTION_MAX_WORDS]).rstrip(" ,;:-") + "…"
    return _capitalise(task)


def _acceptable_task(task: str) -> bool:
    words = _tokens(task)
    if len(words) < 2 or not _content(task):
        return False
    if words[0] in _NEVER_TASKS or _NOT_TASKS.match(task):
        return False
    return not (words[0] in _WEAK_STARTS and len(words) < 3)


def _spoken_action(sentence: str) -> tuple[str, str] | None:
    """``(task, due)`` if the sentence states something to do."""
    sentence = sentence.strip()
    if sentence.endswith("?"):
        return None
    match = _ACTION_CUE.search(sentence)
    if not match or _NEGATED.search(sentence[max(0, match.start() - 28) : match.start()]):
        return None
    task = sentence[match.end() :] if match.group("pre") else sentence[match.start() :]
    for _ in range(2):  # "I need to remember to ..." carries two cues
        inner = _ACTION_CUE.match(task)
        if not inner or not inner.group("pre"):
            break
        task = task[inner.end() :]
    task, due = _split_due(task)
    task = _tidy_task(task)
    return (task, due) if _acceptable_task(task) else None


def _shown_action(line: str) -> tuple[str, str] | None:
    match = _SHOWN_ACTION_CUE.match(line)
    if not match:
        return None
    task, due = _split_due(match.group("task"))
    task = _tidy_task(task)
    return (task, due) if _acceptable_task(task) else None


def _spoken_decision(sentence: str) -> str | None:
    sentence = sentence.strip()
    if sentence.endswith("?") or len(_tokens(sentence)) < 4:
        return None
    match = _DECISION_CUE.search(sentence)
    if not match or _NEGATED.search(sentence[max(0, match.start() - 28) : match.start()]):
        return None
    return _capitalise(_clip(_LEADING_FILLER.sub("", sentence) or sentence, 240))


def _spoken_question(sentence: str) -> str | None:
    sentence = sentence.strip()
    if not sentence.endswith("?"):
        return None
    core = _LEADING_FILLER.sub("", sentence) or sentence
    if len(_tokens(core)) < 4 or _TRIVIAL_QUESTIONS.match(core.rstrip("?").strip()):
        return None
    return _capitalise(_clip(core, 240))


def _find_cues(facts: _Facts) -> None:
    """Fill ``facts.actions`` / ``decisions`` / ``questions`` from what was said and shown."""
    for sent in facts.sentences:
        action = _spoken_action(sent.text)
        if action:
            explicit = bool(_EXPLICIT_REMINDER.search(sent.text))
            tentative = not explicit and bool(_TENTATIVE.search(sent.text))
            facts.actions.append(_Cue(action[0], sent.ts, action[1], explicit=explicit, tentative=tentative))
        decision = _spoken_decision(sent.text)
        if decision:
            facts.decisions.append(_Cue(decision, sent.ts))
        question = _spoken_question(sent.text)
        if question:
            facts.questions.append(_Cue(question, sent.ts))
    for block in facts.blocks:
        for line in block.lines:
            action = _shown_action(line)
            if action:
                facts.actions.append(_Cue(action[0], block.ts, action[1], "shown", explicit=True))
            shown = _SHOWN_DECISION_CUE.match(line)
            if shown and len(_tokens(shown.group("text"))) >= 2:
                facts.decisions.append(_Cue(_capitalise(_clip(_one_line(shown.group("text")), 240)), block.ts, "", "shown"))


# =============================================================================
# Moments without a model: kind, salience, title, summary, tags
# =============================================================================

_VIDEO_CALL = re.compile(r"\b(?:video\s+(?:call|conference|meeting|chat)|zoom|teams\s+(?:call|meeting)|google\s+meet|facetime|webinar)\b", re.I)
_MEDIA_SEEN = re.compile(
    r"""(?ix)\b(?:tv|television|movie|film|netflix|youtube|tiktok|cartoon|sitcom|documentary|video\s+game|
        news\s+(?:broadcast|programme|program|channel|anchor)|broadcast|music\s+video|
        (?:watch(?:es|ing)?|play(?:s|ing)?|show(?:s|ing)?|stream(?:s|ing)?)\s+(?:a\s+|an\s+|the\s+|some\s+)?
            (?:video|movie|film|show|series|episode|news|clip|stream)|
        video\s+(?:is\s+)?(?:playing|player|playback)|
        (?:tv|television)\s+(?:show|screen|set|series)
    )\b"""
)
_KIND_SEEN: dict[str, re.Pattern[str]] = {
    "transit": re.compile(
        r"\b(?:walk(?:s|ing)?|street|sidewalk|pavement|road|highway|driv(?:es|ing)|car\s+interior|dashboard|"
        r"steering\s+wheel|windshield|bus|train|tram|subway|metro|platform|station|airport|bicycle|bike|cycling|"
        r"hallway|corridor|stair(?:s|case|well)?|escalator|elevator|lift|crosswalk|crossing|path|trail)\b",
        re.I,
    ),
    "errand": re.compile(
        r"\b(?:store|shop|shopping|supermarket|grocery|groceries|checkout|cashier|cash\s+register|pharmacy|bank|"
        r"post\s+office|aisle|shelves|receipt|restaurant|caf[eé]|coffee\s+shop|counter|market|mall|parking|"
        r"garage|gas\s+station|petrol|atm|queue)\b",
        re.I,
    ),
    "meeting": re.compile(
        r"\b(?:meeting|conference\s+(?:room|table)|whiteboard|flip\s?chart|presentation|projector|projected|slide(?:s|show)?|"
        r"video\s+(?:call|conference)|zoom|lecture|classroom|audience)\b",
        re.I,
    ),
    "solo_work": re.compile(
        r"\b(?:laptop|computer|monitor|keyboard|desk|workstation|code|coding|spreadsheet|document|typing|editor|"
        r"terminal|notebook|workbench|soldering|tools?)\b",
        re.I,
    ),
}
_MEETING_SAID = re.compile(r"\b(?:meeting|agenda|stand-?up|minutes|action\s+items|sync|retro(?:spective)?|kick-?off)\b", re.I)
_DIALOGUE_SAID = re.compile(r"\b(?:you|your|you['’]re|you['’]ve|you['’]ll)\b", re.I)


@dataclass(slots=True)
class _MomentNote:
    title: str
    summary: str
    tags: list[str]
    kind: str
    salience: str


def _media_seen(facts: _Facts) -> bool:
    """A TV or a screen playing video is what the captions of this moment describe."""
    captions = [c for _, c in facts.captions]
    if not captions:
        return False
    hits = sum(1 for c in captions if _MEDIA_SEEN.search(c) and not _VIDEO_CALL.search(c))
    return hits >= 1 and hits * 2 >= len(captions)


def _rule_kind(facts: _Facts) -> str:
    if facts.empty:
        return "idle"
    if _media_seen(facts) and not facts.self_note:
        return "media"
    speech = facts.speech
    scores: Counter[str] = Counter()
    for _, caption in facts.captions:
        for kind, pattern in _KIND_SEEN.items():
            if pattern.search(caption):
                scores[kind] += 1
    if facts.words >= 30:
        if _MEETING_SAID.search(speech):
            scores["meeting"] += 2
        if "?" in speech or len(_DIALOGUE_SAID.findall(speech)) >= 2:
            scores["conversation"] += 2
        scores["transit"] = 0  # talking while walking is about the talk
    elif _MEETING_SAID.search(speech):
        scores["meeting"] += 1
    if facts.self_note:
        scores["solo_work"] += 1
    best = max(scores.values(), default=0)
    if best <= 0:
        return "other"
    for kind in ("meeting", "conversation", "errand", "solo_work", "transit"):
        if scores[kind] == best:
            return kind
    return "other"


def _rule_salience(facts: _Facts, kind: str) -> str:
    """The prior-art thresholds: short, quiet and text-free is background; a commitment, a
    decision or a captured board / document is a highlight."""
    if facts.empty or kind in ("idle", "media"):
        return "background"
    if facts.actions or facts.decisions or facts.substantial_text:
        return "highlight"
    if facts.duration < _BACKGROUND_SECONDS and facts.words < _BACKGROUND_WORDS and not facts.blocks:
        return "background"
    return "normal"


def _is_heading(line: str) -> bool:
    words = _tokens(line)
    alpha = [w for w in words if len(w) >= 3 and w.isalpha()]
    return 2 <= len(words) <= 8 and len(alpha) >= 2 and len(line) <= 64 and "http" not in line.lower()


def _block_heading(block: _TextBlock) -> str | None:
    for line in block.lines[:3]:
        if _is_heading(line) and not _SHOWN_ACTION_CUE.match(line):
            return line
    return None


def _heading(facts: _Facts) -> str | None:
    """The most salient on-screen heading.

    When something substantive was said, only text the speech is about counts (the heading of
    the block sharing most words with it): a fire-exit sign passed during a conversation is not
    its title.  When nothing was said, it is the heading of the block with the most text.
    """
    blocks = [b for b in facts.blocks if _block_heading(b)]
    if not blocks:
        return None
    if _first_substantive(facts) is None:
        return _block_heading(max(blocks, key=lambda b: (len(b.lines), sum(len(line) for line in b.lines))))
    said = set(_content(facts.speech))
    for word in list(said):
        if word in _NUMBER_WORDS:
            said.add(_NUMBER_WORDS[word])
    shared, best = max(((len(said & set(_content(" ".join(b.lines)))), -i), b) for i, b in enumerate(blocks))
    return _block_heading(best) if shared[0] >= 2 else None


def _as_title(text: str) -> str:
    text = _LEADING_FILLER.sub("", _one_line(text)) or _one_line(text)
    text = text.strip(" \"'“”‘’`*#.,;:!?-–—")
    words = text.split()
    if len(words) > prompts.TITLE_MAX_WORDS:
        text = " ".join(words[: prompts.TITLE_MAX_WORDS]).rstrip(" ,;:-–—") + "…"
    return _capitalise(_clip(text, 90))


def _first_substantive(facts: _Facts) -> str | None:
    for sent in facts.sentences:
        if _substance(sent.text) >= 2:
            return sent.text
    return None


def _extractive_title(facts: _Facts, kind: str) -> str:
    if facts.empty:
        return QUIET_TITLE
    if kind == "media":
        return MEDIA_TITLE
    candidates = [
        _heading(facts),
        facts.actions[0].text if facts.actions else None,
        facts.decisions[0].text if facts.decisions else None,
        _first_substantive(facts),
        facts.sentences[0].text if facts.sentences else None,
        facts.text_lines[0] if facts.blocks else None,
        _first_sentences(facts.captions[0][1], 1) if facts.captions else None,
    ]
    for candidate in candidates:
        title = _as_title(candidate) if candidate else ""
        if title:
            return title
    return QUIET_TITLE


def _extractive_summary(facts: _Facts, kind: str) -> str:
    """One to three sentences, all quoted: what was said first, the commitment or decision if
    there was one, and what was in view."""
    if facts.empty:
        return ""
    parts: list[str] = []
    seen: set[str] = set()

    def add(text: str | None) -> None:
        if not text or len(parts) >= prompts.MOMENT_SUMMARY_MAX_SENTENCES:
            return
        text = _clip(_one_line(text), 220)
        key = _norm_key(text)
        if key and key not in seen:
            seen.add(key)
            parts.append(text if text[-1] in _TERMINAL + "”\"" else text + ".")

    substantive = [s.text for s in facts.sentences if _substance(s.text) >= 2]
    if kind != "media":
        add(substantive[0] if substantive else None)
        cue_times = {c.ts for c in (*facts.actions, *facts.decisions) if c.source == "said"}
        for sent in facts.sentences:
            if sent.ts in cue_times and (_spoken_action(sent.text) or _spoken_decision(sent.text)):
                add(sent.text)
                break
    lines = facts.text_lines
    if lines:
        add("Text in view: “" + _clip("; ".join(lines), 170) + "”")
    if kind != "media":
        for text in substantive[1:]:
            add(text)
    if not parts or kind == "media":
        for _, caption in facts.captions[:1]:
            add(_first_sentences(caption, 1))
    if not parts and facts.sentences:
        add(facts.sentences[0].text)
    return " ".join(parts)


_TAG_STOP = frozenset(
    """remember forget need needs have make sure decided agreed going action todo task reminder follow
    said says tell told think want wants look looks today tomorrow tonight week month text view also
    """.split()
) | frozenset(_NUMBER_WORDS)


def _keywords(texts: Iterable[str], limit: int) -> list[str]:
    counts: Counter[str] = Counter()
    order: dict[str, int] = {}
    for text in texts:
        for tok in _tokens(text):
            if len(tok) < 4 or tok in _STOP or tok in _FILLER or tok in _TAG_STOP or not tok.isalpha():
                continue
            counts[tok] += 1
            order.setdefault(tok, len(order))
    ranked = sorted(counts, key=lambda t: (-counts[t], order[t]))
    return ranked[:limit]


def _extractive_moment(facts: _Facts) -> _MomentNote:
    kind = _rule_kind(facts)
    tags = [] if facts.empty else _keywords([s.text for s in facts.sentences] + facts.text_lines, prompts.MOMENT_MAX_TAGS)
    return _MomentNote(
        title=_extractive_title(facts, kind),
        summary=_extractive_summary(facts, kind),
        tags=tags,
        kind=kind,
        salience=_rule_salience(facts, kind),
    )


def _limit_highlights(facts_list: list[_Facts], notes: list[_MomentNote]) -> None:
    """Highlights are meant to be few: of the moments that are highlights only for the text in
    view, keep the ones with the most text (a commitment or decision always stays one)."""
    text_only = [
        i
        for i, (facts, note) in enumerate(zip(facts_list, notes, strict=True))
        if note.salience == "highlight" and not (facts.actions or facts.decisions)
    ]
    allowed = max(3, len(notes) // 5)
    if len(text_only) <= allowed:
        return
    text_only.sort(key=lambda i: -sum(len(line) for line in facts_list[i].text_lines))
    for i in text_only[allowed:]:
        notes[i].salience = "normal"


# =============================================================================
# Cleaning what a model wrote
# =============================================================================

_PLACEHOLDERS = frozenset(
    {"", "unknown", "n/a", "na", "none", "null", "nil", "untitled", "title", "summary", "tbd", "...", "…", "-", "nothing", "no title"}
)
_NARRATION_PREFIX = re.compile(
    r"^(?:(?:a|the|this|brief|short)\s+)*(?:conversation|discussion|talk|chat|moment|video|recording|clip|summary|notes?|"
    r"overview|recap)\s+(?:about|on|of|regarding|covering|concerning|around)\s+",
    re.I,
)
_GENERIC_PEOPLE = re.compile(
    r"^(?:speaker\s*\w*|someone|somebody|unknown|unnamed|me|i|myself|wearer|the\s+wearer|user|the\s+user|narrator|"
    r"(?:a|an|the|another|other|some)\s+.*|man|woman|person|people|guy|girl|boy|colleague|friend|others?|n/?a|none)$",
    re.I,
)
_ME = frozenset({"me", "i", "myself", "wearer", "the wearer", "user", "the user", "self", "mine"})


def _is_placeholder(text: str) -> bool:
    return text.strip(" .\"'").lower() in _PLACEHOLDERS


def _clean_title(raw: object) -> str:
    text = _one_line(raw).strip(" \"'“”‘’`*#")
    text = _NARRATION_PREFIX.sub("", text)
    return "" if _is_placeholder(text) else _as_title(text)


def _clean_prose(raw: object, max_sentences: int, max_chars: int) -> str:
    text = _one_line(raw).strip(" `*#")
    if _is_placeholder(text):
        return ""
    return _clip(" ".join(_sentences(text)[:max_sentences]), max_chars)


def _clean_tags(raw: object, limit: int) -> list[str]:
    out: list[str] = []
    for item in raw if isinstance(raw, list) else []:
        tag = re.sub(r"[^\w\- ]+", " ", _one_line(item).lower(), flags=re.UNICODE)
        tag = " ".join(tag.replace("_", " ").split()[:3])[:32].strip(" -")
        if tag and not _is_placeholder(tag) and tag not in out:
            out.append(tag)
        if len(out) >= limit:
            break
    return out


def _clean_lines(raw: object, limit: int, max_words: int) -> list[str]:
    """Short one-line statements from a model-written list (bounded work even for a huge list)."""
    out: list[str] = []
    for item in (raw if isinstance(raw, list) else [])[:60]:
        text = _one_line(item).lstrip("-*• ").strip()
        if _is_placeholder(text):
            continue
        words = text.split()
        if len(words) > max_words:
            text = " ".join(words[:max_words]).rstrip(" ,;:-") + "…"
        out.append(_clip(text, 320))
    return _dedupe(out, limit)


class _Grounding:
    """Answers "was this actually said or shown?" for things a model wrote."""

    def __init__(self, said_shown: Iterable[str], seen: Iterable[str] = ()):
        self.said = self._vocab(said_shown)
        self.all = self.said | self._vocab(seen)

    @staticmethod
    def _vocab(texts: Iterable[str]) -> set[str]:
        vocab: set[str] = set()
        for text in texts:
            for tok in _tokens(text):
                vocab.add(tok)
                vocab.add(_stem(tok))
                digits = _NUMBER_WORDS.get(tok)
                if digits:
                    vocab.add(digits)
        if {"p", "m"} <= vocab:
            vocab.add("pm")
        if {"a", "m"} <= vocab:
            vocab.add("am")
        return vocab

    def _hits(self, words: list[str], vocab: set[str]) -> int:
        return sum(1 for w in words if w in vocab or _stem(w) in vocab)

    def supports(self, text: str, *, ratio: float = 0.6, captions: bool = False) -> bool:
        """Most content words of ``text`` occur in the evidence."""
        vocab = self.all if captions else self.said
        words = [t for t in _tokens(text) if t not in _STOP and (len(t) >= 3 or any(c.isdigit() for c in t))]
        alpha = [w for w in words if not w.isdigit()]
        if not alpha:
            return bool(words) and self._hits(words, vocab) == len(words)
        return self._hits(alpha, vocab) / len(alpha) >= ratio

    def stated(self, text: str, *, captions: bool = False) -> bool:
        """Every word of ``text`` (a name, a deadline, a place) occurs in the evidence."""
        vocab = self.all if captions else self.said
        words = [re.sub(r"(?<=\d)(?:st|nd|rd|th)$", "", t) for t in _tokens(text) if t not in ("the", "of", "on", "at", "by", "a")]
        return bool(words) and self._hits(words, vocab) == len(words)


class _Locator:
    """Matches a statement back to the sentence it most likely came from."""

    def __init__(self, facts_list: Sequence[_Facts], media: Sequence[bool]):
        self._entries: list[tuple[frozenset[str], float | None, bool]] = []
        self._by_stem: dict[str, list[int]] = {}
        for facts, is_media in zip(facts_list, media, strict=True):
            texts = [(s.text, s.ts) for s in facts.sentences]
            texts += [(line, block.ts) for block in facts.blocks for line in block.lines]
            for text, ts in texts:
                stems = frozenset(_content(text))
                if not stems:
                    continue
                for stem in stems:
                    self._by_stem.setdefault(stem, []).append(len(self._entries))
                self._entries.append((stems, ts, is_media))

    def find(self, text: str) -> tuple[float | None, bool]:
        """``(time, came from a media moment)`` of the closest sentence, ``(None, False)`` if none is close."""
        stems = frozenset(_content(text))
        if not stems:
            return None, False
        counts: Counter[int] = Counter()
        for stem in stems:
            for i in self._by_stem.get(stem, ()):
                counts[i] += 1
        best: tuple[float, int] | None = None
        for i, shared in counts.items():
            if shared < min(2, len(stems)) or shared / len(stems) < 0.5:
                continue
            score = shared / len(stems) + shared / len(self._entries[i][0] | stems)
            if best is None or score > best[0] + 1e-9 or (abs(score - best[0]) <= 1e-9 and i < best[1]):
                best = (score, i)
        if best is None:
            return None, False
        _, ts, is_media = self._entries[best[1]]
        return ts, is_media


# =============================================================================
# summarize_moments
# =============================================================================


def _session_context(session: Session, ts0: float | None, ts1: float | None) -> str:
    start = ts0 if _local(ts0) is not None else session.started_ts
    when = _local(start)
    if when is None:
        return "One recording from my body-worn camera."
    day = f"{when:%A %d %B %Y}"
    if _local(ts1) is not None and ts1 > start:  # type: ignore[operator]
        return f"One recording from my body-worn camera, {day}, {_span(start, ts1)} ({fmt_duration(ts1 - start)})."  # type: ignore[operator]
    return f"One recording from my body-worn camera, {day}, starting {_clock(start)}."


def _facts_bounds(facts_list: Sequence[_Facts]) -> tuple[float | None, float | None]:
    starts = [f.moment.ts0 for f in facts_list if _finite(f.moment.ts0)]
    ends = [f.moment.ts1 for f in facts_list if _finite(f.moment.ts1)]
    return (min(starts) if starts else None, max(ends) if ends else None)


def _sample(facts_list: Sequence[_Facts]) -> str:
    out: list[str] = []
    size = 0
    for facts in facts_list:
        for text in (facts.speech, " ".join(facts.text_lines)):
            if text:
                out.append(text[:1000])
                size += len(out[-1])
        if size >= 4000:
            break
    return " ".join(out)


def _apply_llm_moment(facts: _Facts, base: _MomentNote, item: dict[str, Any]) -> _MomentNote:
    """One moment as the model described it, with the checks that keep it honest."""
    title = _clean_title(item.get("title"))
    summary = _clean_prose(item.get("summary"), prompts.MOMENT_SUMMARY_MAX_SENTENCES, 480)
    if not title and not summary:
        return base
    kind = item.get("kind") if item.get("kind") in MOMENT_KINDS else base.kind
    if kind == "other" and base.kind != "other":
        kind = base.kind  # "other" is also what an invalid value is coerced to: the rule knows more
    if base.kind == "media":
        kind = "media"  # a TV in view and no note-to-self: never treat its sound as the wearer's life
    elif kind == "media" and (facts.self_note or not facts.captions):
        kind = base.kind  # the wearer dictated a note, or nothing was seen that could show a screen
    salience = item.get("salience") if item.get("salience") in MOMENT_SALIENCE else base.salience
    if kind == "media":
        salience = "background" if salience != "normal" else "normal"
    elif salience == "background" and base.salience == "highlight":
        salience = "normal"  # a commitment, a decision or a captured board is never collapsed
    elif salience == "highlight" and base.salience == "background" and facts.words < 20:
        salience = "normal"  # next to nothing was said or shown: not something to find again
    return _MomentNote(
        title=title or base.title,
        summary=summary or base.summary,
        tags=_clean_tags(item.get("tags"), prompts.MOMENT_MAX_TAGS) or base.tags,
        kind=kind,
        salience=salience,
    )


def _moment_block(number: int, facts: _Facts, max_chars: int) -> str:
    header = f"--- MOMENT {number} | {_span(facts.moment.ts0, facts.moment.ts1)} | {fmt_duration(facts.duration)} ---"
    return header + "\n" + _fit_lines(_context_lines(facts), max(0, max_chars - len(header) - 1))


def _llm_moments(llm: LLM, session: Session, facts_list: list[_Facts], notes: list[_MomentNote]) -> None:
    """Replace the extractive notes of the moments the model handled well; leave the rest."""
    pending = [i for i, facts in enumerate(facts_list) if not facts.empty]
    if not pending:
        return
    name = _llm_name(llm)
    context = _session_context(session, *_facts_bounds(facts_list))
    budget = _budget_chars(llm, _sample(facts_list))
    room = budget - len(prompts.SYSTEM) - len(prompts.moments_prompt(context, "")) - 8
    if room < MIN_EVIDENCE_CHARS:
        log.warning(
            "%s: its context budget (%s tokens) is too small for the summary prompt; writing extractive "
            "moment summaries instead. Raise llm.context_tokens in config.toml.",
            name, getattr(llm, "context_tokens", "?"),
        )  # fmt: skip
        return

    batches: list[list[int]] = [[]]
    blocks: dict[int, str] = {}
    used = 0
    per_moment = min(MOMENT_CONTEXT_CHARS, room)
    per_call = MAX_MOMENTS_PER_LARGE_CALL if budget >= _LARGE_CONTEXT_CHARS else MAX_MOMENTS_PER_CALL
    for i in pending:
        number = len(batches[-1]) + 1
        block = _moment_block(number, facts_list[i], per_moment)
        if batches[-1] and (used + len(block) + 1 > room or len(batches[-1]) >= per_call):
            batches.append([])
            used = 0
            block = _moment_block(1, facts_list[i], per_moment)
        batches[-1].append(i)
        blocks[i] = block
        used += len(block) + 1

    done = 0
    failures = 0
    for batch in batches:
        prompt = prompts.moments_prompt(context, "\n".join(blocks[i] for i in batch))
        try:
            raw = llm.json(
                system=prompts.SYSTEM, prompt=prompt, schema=prompts.MOMENTS_SCHEMA,
                max_tokens=256 + 192 * len(batch),
            )  # fmt: skip
        except BackendUnavailable as exc:
            log.warning("%s is no longer available (%s); the remaining moments get extractive summaries", name, exc)
            break
        except Exception as exc:  # a failed batch must never fail the session
            failures += 1
            log.warning("%s failed on a batch of %d moments (%s); using extractive summaries for them", name, len(batch), exc)
            if failures >= MAX_FAILURES_IN_A_ROW:
                log.warning("%s failed %d times in a row; not asking it again for this session", name, failures)
                break
            continue
        data = _coerced(raw, prompts.MOMENTS_SCHEMA)
        answered: set[int] = set()
        for item in data["moments"][: 4 * len(batch)]:
            number = item.get("id")
            if not isinstance(number, int) or not 1 <= number <= len(batch) or number in answered:
                continue  # an id that was never asked for is not evidence of anything
            i = batch[number - 1]
            updated = _apply_llm_moment(facts_list[i], notes[i], item)
            if updated is not notes[i]:
                notes[i] = updated
                answered.add(number)
        done += len(answered)
        if answered:
            failures = 0
        else:
            failures += 1
            log.warning("%s returned nothing usable for a batch of %d moments; keeping extractive summaries", name, len(batch))
            if failures >= MAX_FAILURES_IN_A_ROW:
                break
    log.info("%s summarised %d of %d moments (%d calls planned)", name, done, len(pending), len(batches))


def summarize_moments(
    llm: LLM | None, session: Session, moments: list[Moment], utterances: list[Utterance], keyframes: list[Keyframe]
) -> list[Moment]:
    """Fill title / summary / tags / kind / salience of each moment (LLM, or extractive when llm is None).

    The moments are updated in place and returned in the order given.

    * ``title`` has at most 8 words and names the subject matter; ``summary`` has 1-3 sentences;
      ``tags`` at most 5 lowercase words; ``kind`` is one of :data:`~videonotes.models.MOMENT_KINDS`
      and ``salience`` one of :data:`~videonotes.models.MOMENT_SALIENCE`.
    * A moment in which nothing was said, shown or described is titled "Quiet stretch"
      (kind ``idle``, salience ``background``) without asking the model.
    * A moment whose captions show a TV or a video playing (and in which the wearer did not
      dictate a note) is ``media``: it is collapsed and yields no action items later.
    * With a model, several moments go into one call, sized to ``llm.context_tokens``.  A call
      that fails, or an answer that is malformed or skips a moment, leaves the extractive
      result in place for those moments; after two failures in a row (or when the backend
      reports it is gone) the model is not asked again.
    """
    if not moments:
        return moments
    facts_list = _Index(utterances, keyframes).facts(moments)
    notes = [_extractive_moment(facts) for facts in facts_list]
    _limit_highlights(facts_list, notes)
    if llm is not None:
        try:
            _llm_moments(llm, session, facts_list, notes)
        except Exception:  # whatever a backend does, the extractive result stands
            log.exception("summarising moments with %s failed; keeping extractive summaries", _llm_name(llm))
    for moment, note in zip(moments, notes, strict=True):
        moment.title = note.title
        moment.summary = note.summary
        moment.tags = list(note.tags)
        moment.kind = note.kind
        moment.salience = note.salience
    return moments


# =============================================================================
# summarize_session
# =============================================================================

_SALIENCE_RANK = {"highlight": 0, "normal": 1, "background": 2}
_INFORMATIVE = re.compile(
    rf"(?i)\d|\b(?:{'|'.join(_NUMBER_WORDS)}|{_WEEKDAY}|{_MONTH}|tomorrow|tonight|percent|dollars?|euros?|pounds?|"
    r"o['’]clock|a\.?m\.?|p\.?m\.?)\b"
)


@dataclass
class _Extract:
    """The extractive note of a session plus the timed cues it was built from."""

    note: SessionNote
    actions: list[_Cue]
    decisions: list[_Cue]
    questions: list[_Cue]


def _session_facts(session: Session, moments: list[Moment], index: _Index) -> tuple[list[_Facts], list[_MomentNote]]:
    """Facts and (already written, else extractive) notes of every moment, in time order."""
    ordered = sorted(moments, key=lambda m: (m.ts0 if _finite(m.ts0) else math.inf, m.idx))
    if not ordered:
        bounds = index.bounds
        if bounds is None:
            return [], []
        ordered = [Moment(session_id=session.id, idx=0, ts0=bounds[0], ts1=bounds[1])]
    facts_list = index.facts(ordered)
    notes: list[_MomentNote] = []
    for facts in facts_list:
        m = facts.moment
        if _one_line(m.title) and m.kind in MOMENT_KINDS:
            salience = m.salience if m.salience in MOMENT_SALIENCE else "normal"
            notes.append(_MomentNote(_one_line(m.title), _one_line(m.summary), list(m.tags or []), m.kind, salience))
        else:
            notes.append(_extractive_moment(facts))
    return facts_list, notes


def _captured_text(facts_list: Sequence[_Facts]) -> list[str]:
    """Distinct on-screen text of the session, one entry per newly seen block of lines."""
    deduper = _TextDeduper()
    out: list[str] = []
    for facts in facts_list:
        for block in facts.blocks:
            fresh = deduper.new_lines(block.lines)
            if fresh and len(out) < _MAX_CAPTURED_ENTRIES:
                out.append(_clip("\n".join(fresh), _MAX_CAPTURED_ENTRY_CHARS))
    return out


def _informative_score(sentence: str) -> int:
    words = sentence.split()
    if _substance(sentence) < 3 or not 5 <= len(words) <= 40 or sentence.rstrip().endswith("?"):
        return 0
    score = 1
    if _INFORMATIVE.search(sentence):
        score += 2
    score += min(2, sum(1 for w in words[1:] if w[:1].isupper() and w.lower() not in _STOP and w != "I"))
    return score


def _extractive_session(facts_list: list[_Facts], notes: list[_MomentNote]) -> _Extract:
    live = [(f, n) for f, n in zip(facts_list, notes, strict=True) if n.kind != "media"]
    actions = [c for f, _ in live for c in f.actions]
    decisions = [c for f, _ in live for c in f.decisions]
    questions = [c for f, _ in live for c in f.questions]

    ranked = sorted(
        (i for i, f in enumerate(facts_list) if not f.empty),
        key=lambda i: (_SALIENCE_RANK.get(notes[i].salience, 1), notes[i].kind == "media", i),
    )
    main = [i for i in ranked if notes[i].salience != "background"] or ranked

    note = SessionNote(llm_backend=EXTRACTIVE)
    if not ranked:
        note.title = QUIET_SESSION_TITLE
        note.summary = QUIET_SESSION_SUMMARY
        return _Extract(note, [], [], [])

    note.title = notes[main[0]].title
    summary_parts = _dedupe(
        (_first_sentences(notes[i].summary, 1) or notes[i].title for i in sorted(main[:3])), 3
    )
    note.summary = " ".join(p if p[-1] in _TERMINAL + "”\"" else p + "." for p in summary_parts if p)

    note.action_items = _merge_actions(
        (ActionItem(text=c.text, due=c.due, ts=c.ts) for c in actions),
        prompts.SESSION_MAX_ACTION_ITEMS,
        [c.rank for c in actions],
    )
    note.decisions = _dedupe((c.text for c in decisions), prompts.SESSION_MAX_DECISIONS)
    note.open_questions = _dedupe((c.text for c in questions), prompts.SESSION_MAX_QUESTIONS)
    note.captured_text = _captured_text(facts_list)

    used = {_norm_key(s) for s in _sentences(note.summary)} | {_norm_key(d) for d in note.decisions}
    cue_times = {c.ts for c in actions if c.source == "said"}
    candidates: list[tuple[int, int, str]] = []
    order = 0
    for i in sorted(main):
        for sent in facts_list[i].sentences:
            order += 1
            if sent.ts in cue_times and _spoken_action(sent.text):
                continue  # already an action item
            score = _informative_score(sent.text)
            if score >= 2 and _norm_key(sent.text) not in used:
                candidates.append((score, order, sent.text))
    best = sorted(sorted(candidates, key=lambda c: (-c[0], c[1]))[: 2 * prompts.SESSION_MAX_KEY_POINTS], key=lambda c: c[1])
    note.key_points = _dedupe((_clip(text, 240) for _, _, text in best), prompts.SESSION_MAX_KEY_POINTS)

    tag_counts: Counter[str] = Counter()
    for i in main:
        for tag in notes[i].tags:
            tag_counts[tag] += 1
    note.tags = [t for t, _ in tag_counts.most_common(prompts.SESSION_MAX_TAGS)]
    return _Extract(note, actions, decisions, questions)


def _moment_chunk(facts: _Facts, note: _MomentNote, cap: int) -> str:
    """One moment for the session prompt: what was written about it plus its high-value raw lines."""
    flags = f"[{note.kind}]" + (f" [{note.salience}]" if note.salience != "normal" else "")
    head = f"--- {_span(facts.moment.ts0, facts.moment.ts1)} {flags} {_evidence_text(note.title, 90)}"
    if note.salience == "background" or note.kind == "media" or cap < 200:
        return _clip(head, max(40, cap))
    lines = [head]
    if note.summary:
        lines.append("summary: " + _evidence_text(note.summary, 420))
    stamp = "%H:%M:%S"
    keyed: list[tuple[float, str]] = []
    cue_texts = {(c.ts, c.source) for c in (*facts.actions, *facts.decisions, *facts.questions)}
    for sent in facts.sentences:
        if (sent.ts, "said") in cue_texts and (
            _ACTION_CUE.search(sent.text) or _DECISION_CUE.search(sent.text) or sent.text.rstrip().endswith("?")
        ):
            keyed.append((sent.ts or 0.0, f"[{_clock(sent.ts, stamp)}] {prompts.SAID}: {_evidence_text(sent.text, 260)}"))
    for block in facts.blocks:
        text = " | ".join(_evidence_text(line, 160) for line in block.lines)
        keyed.append((block.ts, f"[{_clock(block.ts, stamp)}] {prompts.TEXT}: {text}"))
    keyed.sort(key=lambda entry: entry[0])
    body = "\n".join([*lines, *(text for _, text in keyed)])
    if len(body) <= cap:
        return body
    # too much raw evidence for this moment: keep the header and summary, squeeze the raw lines
    fixed = "\n".join(lines)
    raw_lines = [text for _, text in keyed]
    room = cap - len(fixed) - 1
    if room < 80:
        return _squeeze(fixed, cap)
    per = max(60, room // max(1, len(raw_lines)) - 1)
    costs = [min(len(text), per) + 1 for text in raw_lines]
    head_n, tail_n = _take_from_ends(costs, room - 40)
    kept = [_clip(t, per) for t in raw_lines[:head_n]]
    if head_n + tail_n < len(raw_lines):
        kept.append(f"[… {len(raw_lines) - head_n - tail_n} lines left out …]")
    kept += [_clip(t, per) for t in raw_lines[len(raw_lines) - tail_n :]] if tail_n else []
    return _squeeze("\n".join([fixed, *kept]), cap)


def _session_parts(facts_list: list[_Facts], notes: list[_MomentNote], room: int) -> list[list[int]]:
    """Group the moments into as few prompts as fit ``room`` characters each (at most MAX_SESSION_PARTS)."""
    cap = min(1800, room)
    while True:
        sizes = [len(_moment_chunk(f, n, cap)) + 1 for f, n in zip(facts_list, notes, strict=True)]
        parts: list[list[int]] = [[]]
        used = 0
        for i, size in enumerate(sizes):
            if parts[-1] and used + size > room:
                parts.append([])
                used = 0
            parts[-1].append(i)
            used += size
        if len(parts) <= MAX_SESSION_PARTS or cap <= 120:
            return parts
        cap = max(120, int(cap * MAX_SESSION_PARTS / len(parts) * 0.9))


def _part_text(facts_list: list[_Facts], notes: list[_MomentNote], part: list[int], room: int) -> str:
    cap = min(1800, room)
    while True:
        text = "\n".join(_moment_chunk(facts_list[i], notes[i], cap) for i in part)
        if len(text) <= room or cap <= 60:
            return _squeeze(text, room)
        cap = max(60, int(cap * room / len(text) * 0.9))


def _validated_note(
    raw: object, grounding: _Grounding, locator: _Locator, *, merge_only: bool = False
) -> SessionNote | None:
    """A model-written session note reduced to what the evidence supports. None if nothing is left."""
    schema = prompts.SESSION_MERGE_SCHEMA if merge_only else prompts.SESSION_SCHEMA
    data = _coerced(raw, schema)
    note = SessionNote(
        title=_clean_title(data["title"]),
        summary=_clean_prose(data["summary"], prompts.SESSION_SUMMARY_MAX_SENTENCES, 900),
        tags=_clean_tags(data["tags"], prompts.SESSION_MAX_TAGS),
    )
    points = _clean_lines(data["key_points"], 3 * prompts.SESSION_MAX_KEY_POINTS, prompts.POINT_MAX_WORDS + 10)
    note.key_points = [p for p in points if grounding.supports(p, ratio=0.5, captions=True)][: prompts.SESSION_MAX_KEY_POINTS]
    if merge_only:
        return note if (note.title or note.summary or note.key_points) else None

    actions: list[ActionItem] = []
    for item in data["action_items"][:40]:
        text = _one_line(item.get("text")).lstrip("-*• ").strip(" .")
        if _is_placeholder(text) or len(text.split()) < 2:
            continue
        words = text.split()
        if len(words) > prompts.ACTION_MAX_WORDS + 5:
            text = " ".join(words[: prompts.ACTION_MAX_WORDS + 5]).rstrip(" ,;:-") + "…"
        if not grounding.supports(text):
            continue  # not something that was said or shown
        ts, from_media = locator.find(text)
        if from_media:
            continue  # it came out of a TV, not out of the wearer's life
        owner = _one_line(item.get("owner"))
        if owner.lower() in _ME:
            owner = "me"
        elif not owner or _is_placeholder(owner) or len(owner.split()) > 4 or not grounding.stated(owner):
            owner = ""
        due = _one_line(item.get("due")).strip(" .")
        if not due or _is_placeholder(due) or len(due.split()) > 6 or not grounding.stated(due):
            due = ""  # a deadline nobody said or showed
        actions.append(ActionItem(text=_capitalise(_clip(text, 200)), owner=owner, due=due, ts=ts))
    note.action_items = _merge_actions(actions, prompts.SESSION_MAX_ACTION_ITEMS)

    def grounded(raw_items: object, limit: int) -> list[str]:
        kept = []
        for text in _clean_lines(raw_items, 3 * limit, prompts.POINT_MAX_WORDS + 10):
            if grounding.supports(text) and not locator.find(text)[1]:
                kept.append(text)
        return kept[:limit]

    note.decisions = grounded(data["decisions"], prompts.SESSION_MAX_DECISIONS)
    note.open_questions = grounded(data["open_questions"], prompts.SESSION_MAX_QUESTIONS)
    note.people = [
        p
        for p in _clean_lines(data["people"], 3 * prompts.SESSION_MAX_PEOPLE, 4)
        if not _GENERIC_PEOPLE.match(p) and any(len(t) >= 3 and t.isalpha() for t in _tokens(p)) and grounding.stated(p)
    ][: prompts.SESSION_MAX_PEOPLE]
    note.places = [
        p for p in _clean_lines(data["places"], 3 * prompts.SESSION_MAX_PLACES, 6) if grounding.stated(p, captions=True)
    ][: prompts.SESSION_MAX_PLACES]

    if not (note.title or note.summary or note.key_points or note.action_items or note.decisions):
        return None
    return note


def _fill_from(note: SessionNote, base: SessionNote) -> SessionNote:
    """What only the extractive pass provides (verbatim text), and what the model left empty."""
    note.title = note.title or base.title
    note.summary = note.summary or base.summary
    note.tags = note.tags or list(base.tags)
    note.captured_text = list(base.captured_text)
    return note


def _llm_session(
    llm: LLM, session: Session, facts_list: list[_Facts], notes: list[_MomentNote], extract: _Extract
) -> SessionNote | None:
    name = _llm_name(llm)
    context = _session_context(session, *_facts_bounds(facts_list))
    budget = _budget_chars(llm, _sample(facts_list))
    room = budget - len(prompts.SYSTEM) - len(prompts.session_prompt(context, "", part=99, parts=99)) - 8
    if room < MIN_EVIDENCE_CHARS:
        log.warning(
            "%s: its context budget (%s tokens) is too small for the session prompt; writing an extractive note "
            "instead. Raise llm.context_tokens in config.toml.",
            name, getattr(llm, "context_tokens", "?"),
        )  # fmt: skip
        return None

    media = [n.kind == "media" for n in notes]
    grounding = _Grounding(
        (text for f in facts_list for text in (*(s.text for s in f.sentences), *f.text_lines)),
        (c for f in facts_list for _, c in f.captions),
    )
    locator = _Locator(facts_list, media)
    # An explicit reminder ("remember to ...", "Action: ...") is quoted evidence: it is kept even if
    # the model overlooks it. Weaker cues ("we should ...") are left to the model's judgement.
    reminders = [ActionItem(text=c.text, due=c.due, ts=c.ts) for c in extract.actions if c.explicit]
    parts = _session_parts(facts_list, notes, room)

    if len(parts) == 1:
        prompt = prompts.session_prompt(context, _part_text(facts_list, notes, parts[0], room))
        raw = llm.json(system=prompts.SYSTEM, prompt=prompt, schema=prompts.SESSION_SCHEMA, max_tokens=1800)
        note = _validated_note(raw, grounding, locator)
        if note is None:
            log.warning("%s returned nothing usable for the session note; writing an extractive note", name)
            return None
        note.action_items = _merge_actions(
            [*note.action_items, *reminders],
            prompts.SESSION_MAX_ACTION_ITEMS,
            [2] * len(note.action_items) + [3] * len(reminders),
        )
        note.llm_backend = name
        return _fill_from(note, extract.note)

    # map: one note per part
    partials: list[tuple[list[int], SessionNote]] = []
    failed: list[list[int]] = []
    failures = 0
    for number, part in enumerate(parts, 1):
        if failures >= MAX_FAILURES_IN_A_ROW:
            failed.append(part)
            continue
        prompt = prompts.session_prompt(
            context, _part_text(facts_list, notes, part, room), part=number, parts=len(parts)
        )
        try:
            raw = llm.json(system=prompts.SYSTEM, prompt=prompt, schema=prompts.SESSION_SCHEMA, max_tokens=1500)
        except BackendUnavailable as exc:
            log.warning("%s is no longer available (%s); the rest of the session note is extractive", name, exc)
            failures = MAX_FAILURES_IN_A_ROW
            failed.append(part)
            continue
        except Exception as exc:
            log.warning("%s failed on part %d of %d of the session (%s)", name, number, len(parts), exc)
            failures += 1
            failed.append(part)
            continue
        partial = _validated_note(raw, grounding, locator)
        if partial is None:
            failures += 1
            failed.append(part)
        else:
            failures = 0
            partials.append((part, partial))
    if not partials:
        return None

    # reduce: lists are merged here; title, summary and key points by one more (small) call
    note = SessionNote()
    extra_actions: list[ActionItem] = []
    extra_ranks: list[int] = []
    extra_decisions: list[str] = []
    extra_questions: list[str] = []
    if failed:
        spans = [(facts_list[p[0]].moment.ts0, facts_list[p[-1]].moment.ts1) for p in failed]

        def uncovered(cue: _Cue) -> bool:
            return cue.ts is not None and any(lo - 1e-6 <= cue.ts <= hi + 1e-6 for lo, hi in spans)

        extra_actions = [ActionItem(text=c.text, due=c.due, ts=c.ts) for c in extract.actions if uncovered(c)]
        extra_ranks = [c.rank for c in extract.actions if uncovered(c)]
        extra_decisions = [c.text for c in extract.decisions if uncovered(c)]
        extra_questions = [c.text for c in extract.questions if uncovered(c)]
    ordered = sorted(partials, key=lambda entry: entry[0][0])
    from_model = [a for _, p in ordered for a in p.action_items]
    ranked = sorted(
        zip(
            from_model + extra_actions + reminders,
            [2] * len(from_model) + extra_ranks + [3] * len(reminders),
            strict=True,
        ),
        key=lambda pair: (pair[0].ts is None, pair[0].ts or 0.0),
    )  # in time order; what cannot be placed in time goes last
    note.action_items = _merge_actions(
        [item for item, _ in ranked], prompts.SESSION_MAX_ACTION_ITEMS, [rank for _, rank in ranked]
    )
    note.decisions = _dedupe([d for _, p in ordered for d in p.decisions] + extra_decisions, prompts.SESSION_MAX_DECISIONS)
    note.open_questions = _dedupe(
        [q for _, p in ordered for q in p.open_questions] + extra_questions, prompts.SESSION_MAX_QUESTIONS
    )
    note.people = _dedupe((x for _, p in ordered for x in p.people), prompts.SESSION_MAX_PEOPLE)
    note.places = _dedupe((x for _, p in ordered for x in p.places), prompts.SESSION_MAX_PLACES)
    tag_counts = Counter(t for _, p in ordered for t in p.tags)
    note.tags = [t for t, _ in tag_counts.most_common(prompts.SESSION_MAX_TAGS)]

    merged: SessionNote | None = None
    merge_context = context + " The notes below were written part by part."
    merge_room = budget - len(prompts.SYSTEM) - len(prompts.session_merge_prompt(merge_context, "")) - 8
    if failures < MAX_FAILURES_IN_A_ROW and merge_room >= MIN_EVIDENCE_CHARS:
        per = max(160, merge_room // len(ordered) - 1)
        blocks = []
        for part, partial in ordered:
            span = _span(facts_list[part[0]].moment.ts0, facts_list[part[-1]].moment.ts1)
            text = f"--- PART {span}\ntitle: {partial.title}\nsummary: {partial.summary}"
            text += "".join(f"\n- {point}" for point in partial.key_points)
            blocks.append(_squeeze(text, per))
        try:
            raw = llm.json(
                system=prompts.SYSTEM,
                prompt=prompts.session_merge_prompt(merge_context, _squeeze("\n".join(blocks), merge_room)),
                schema=prompts.SESSION_MERGE_SCHEMA,
                max_tokens=900,
            )
            merged = _validated_note(raw, grounding, locator, merge_only=True)
        except Exception as exc:
            log.warning("%s failed to merge the parts of the session note (%s); joining them instead", name, exc)
    if merged is not None:
        note.title, note.summary, note.key_points = merged.title, merged.summary, merged.key_points
        note.tags = merged.tags or note.tags
    if not note.title:
        note.title = next((p.title for _, p in ordered if p.title), "")
    if not note.summary:
        firsts = _dedupe((_first_sentences(p.summary, 1) for _, p in ordered), prompts.SESSION_SUMMARY_MAX_SENTENCES)
        note.summary = " ".join(firsts)
    if not note.key_points:
        note.key_points = _dedupe((k for _, p in ordered for k in p.key_points), prompts.SESSION_MAX_KEY_POINTS)
    note.llm_backend = f"{name}+{EXTRACTIVE}" if failed else name
    return _fill_from(note, extract.note)


def summarize_session(
    llm: LLM | None, session: Session, moments: list[Moment], utterances: list[Utterance], keyframes: list[Keyframe]
) -> SessionNote:
    """Write the structured note of a whole session.

    Built from the moment summaries (as filled in by :func:`summarize_moments`) plus the
    high-value raw evidence: lines that look like commitments, decisions or questions, and
    every distinct on-screen text.  A session too long for one context window is split
    into parts that are summarised separately and then merged.

    What the model writes is checked against the evidence (see the module docstring);
    ``captured_text`` is always the verbatim OCR text.  ``ActionItem.ts`` points at the
    utterance or frame the item was matched to, when one is close enough.

    Without a model - or when the model fails or returns nothing usable - the note is
    extractive: quoted sentences, cue-phrase action items ("remember to ...", "Action: ...")
    with a due time only if one was stated ("by Friday" -> "Friday"), decisions, questions,
    captured text; people and places stay empty.  ``llm_backend`` names who wrote the note:
    the model, ``"extractive"``, or ``"<model>+extractive"`` when only some parts of a long
    session came from the model.
    """
    facts_list, notes = _session_facts(session, moments, _Index(utterances, keyframes))
    extract = _extractive_session(facts_list, notes)
    if llm is None or all(f.empty for f in facts_list):
        return extract.note
    try:
        note = _llm_session(llm, session, facts_list, notes, extract)
    except BackendUnavailable as exc:
        log.warning("%s is not available (%s); writing an extractive session note", _llm_name(llm), exc)
        note = None
    except Exception as exc:  # never fail a session over its summary
        log.warning("%s failed on the session note (%s: %s); writing an extractive note", _llm_name(llm), type(exc).__name__, exc)
        note = None
    return note if note is not None else extract.note


# =============================================================================
# summarize_day
# =============================================================================


def _note_block(session: Session, note: SessionNote, number: int, cap: int) -> str:
    start = session.started_ts
    when = _span(start, session.ended_ts)
    lines = [f"--- RECORDING {number} | {when} | {_evidence_text(note.title or session.title, 100)}"]
    if note.summary:
        lines.append("summary: " + _evidence_text(note.summary, 600))
    for label, items in (
        ("key point", note.key_points),
        ("decision", note.decisions),
        ("open question", note.open_questions),
        ("to do", [a.text + (f" (due: {a.due})" if a.due else "") for a in note.action_items]),
    ):
        lines += [f"{label}: {_evidence_text(item, 240)}" for item in items]
    return _squeeze("\n".join(lines), cap)


def _extractive_day(date: str, sessions: list[Session]) -> DayDigest:
    digest = DayDigest(date=date, session_ids=[s.id for s in sessions], llm_backend=EXTRACTIVE)
    noted = [(s, s.note) for s in sessions if s.note is not None]
    digest.action_items = _merge_actions(
        (a for _, note in noted for a in note.action_items), prompts.DAY_MAX_ACTION_ITEMS
    )
    titles = _dedupe((note.title or s.title for s, note in noted), 50)
    titles = [t for t in titles if t != QUIET_SESSION_TITLE] or titles
    if titles:
        headline = "; ".join(titles[:2]) + (f" (+{len(titles) - 2} more)" if len(titles) > 2 else "")
        words = headline.split()
        if len(words) > prompts.DAY_HEADLINE_MAX_WORDS + 4:
            headline = titles[0] + (f" (+{len(titles) - 1} more)" if len(titles) > 1 else "")
        digest.headline = _clip(headline, 120)
    digest.summary = " ".join(
        _dedupe((_first_sentences(note.summary, 1) for _, note in noted), prompts.DAY_SUMMARY_MAX_SENTENCES)
    )

    multi = len(noted) > 1

    def stamped(session: Session, text: str) -> str:
        return f"{_clock(session.started_ts)} — {text}" if multi and _local(session.started_ts) is not None else text

    candidates: list[str] = []
    for kind in ("decisions", "key_points"):
        for s, note in noted:
            candidates += [stamped(s, _clip(item, 200)) for item in getattr(note, kind)[:3]]
    if len(_dedupe(candidates, 5)) < 3:
        for s, note in noted:
            for sent in _sentences(note.summary)[1:3]:
                candidates.append(stamped(s, _clip(sent, 200)))
    digest.highlights = _dedupe(candidates, 5)
    return digest


def _llm_day(llm: LLM, date: str, noted: list[tuple[Session, SessionNote]], digest: DayDigest) -> None:
    """Let the model write headline, summary and highlights into ``digest`` (left as it is if it cannot)."""
    name = _llm_name(llm)
    try:
        day = datetime.strptime(date, "%Y-%m-%d").strftime("%A %d %B %Y")
    except (TypeError, ValueError):
        day = _one_line(date)
    context = f"Notes of the {len(noted)} recording(s) I made on {day}."
    budget = _budget_chars(llm, " ".join(f"{note.title} {note.summary}" for _, note in noted))
    room = budget - len(prompts.SYSTEM) - len(prompts.day_prompt(context, "")) - 8
    if room < MIN_EVIDENCE_CHARS:
        log.warning("%s: context budget too small for the day digest; writing it without the model", name)
        return
    per = max(120, room // len(noted) - 1)
    blocks = [_note_block(s, note, n, min(per, 2400)) for n, (s, note) in enumerate(noted, 1)]
    raw = llm.json(
        system=prompts.SYSTEM,
        prompt=prompts.day_prompt(context, _squeeze("\n".join(blocks), room)),
        schema=prompts.DAY_SCHEMA,
        max_tokens=900,
    )
    data = _coerced(raw, prompts.DAY_SCHEMA)
    grounding = _Grounding(
        text
        for _, note in noted
        for text in (
            note.title, note.summary, *note.key_points, *note.decisions, *note.open_questions,
            *(f"{a.text} {a.due} {a.owner}" for a in note.action_items), *note.people, *note.places, *note.captured_text,
        )
    )  # fmt: skip
    headline = _clean_prose(data["headline"], 1, 140).rstrip(".")
    words = headline.split()
    if len(words) > prompts.DAY_HEADLINE_MAX_WORDS + 2:
        headline = " ".join(words[: prompts.DAY_HEADLINE_MAX_WORDS + 2]).rstrip(" ,;:-") + "…"
    summary = _clean_prose(data["summary"], prompts.DAY_SUMMARY_MAX_SENTENCES + 1, 700)
    highlights = [
        h
        for h in _clean_lines(data["highlights"], 3 * prompts.DAY_MAX_HIGHLIGHTS, prompts.DAY_HIGHLIGHT_MAX_WORDS + 8)
        if grounding.supports(h, ratio=0.5)
    ][: prompts.DAY_MAX_HIGHLIGHTS]
    if not (headline or summary or highlights):
        log.warning("%s returned nothing usable for the day digest; writing it without the model", name)
        return
    digest.headline = headline or digest.headline
    digest.summary = summary or digest.summary
    digest.highlights = highlights or digest.highlights
    digest.llm_backend = name


def summarize_day(llm: LLM | None, date: str, sessions: list[Session]) -> DayDigest:
    """Roll the notes of one local calendar day up into a :class:`~videonotes.models.DayDigest`.

    ``sessions`` are the day's sessions (those without a note are listed but contribute
    nothing).  Action items are merged from the session notes and de-duplicated in code -
    the model never adds one.  The model writes the headline (at most about 10 words), a
    2-3 sentence summary and 3-7 short highlights from what the session notes say; without
    a model the headline is made of the session titles and the highlights are the notes'
    decisions and key points.  Lists are capped so the digest stays quick to read.
    """
    ordered = sorted(sessions or [], key=lambda s: s.started_ts if _finite(s.started_ts) else math.inf)
    digest = _extractive_day(date, ordered)
    noted = [(s, s.note) for s in ordered if s.note is not None]
    if llm is None or not noted:
        return digest
    try:
        _llm_day(llm, date, noted, digest)
    except Exception as exc:  # the digest never fails over its model
        log.warning(
            "%s failed on the day digest (%s: %s); writing it without the model", _llm_name(llm), type(exc).__name__, exc
        )
        return _extractive_day(date, ordered)
    return digest


# =============================================================================
# answer_question
# =============================================================================

_EVIDENCE_LABELS = {
    "utterance": "said",
    "ocr": "text in view",
    "caption": "seen",
    "moment": "note on a moment",
    "session": "note on a recording",
}
_QUESTION_STOP = _STOP | frozenset(
    "did does do was were is are what when where who whom whose which how why tell show find say said anything something".split()
)


def _when(ts: float | None) -> str:
    when = _local(ts)
    return f"{when:%a %d %b %Y, %H:%M}" if when is not None else "time unknown"


def _question_words(question: str) -> set[str]:
    return {_stem(t) for t in _tokens(question) if t not in _QUESTION_STOP and (len(t) >= 3 or t.isdigit())}


#: With equal overlap, what was actually said or shown goes before notes written about it.
_KIND_ORDER = {"utterance": 0, "ocr": 0, "caption": 1, "moment": 2, "session": 3}


def _rank_evidence(question: str, items: Sequence[Evidence]) -> list[tuple[int, int]]:
    """``(score, index)`` per item, best first; the score counts the question's words found in it."""
    wanted = _question_words(question)
    scored = []
    for i, item in enumerate(items):
        have = {_stem(t) for t in _tokens(_one_line(item.text))}
        scored.append((len(wanted & have), i))
    return sorted(scored, key=lambda entry: (-entry[0], _KIND_ORDER.get(items[entry[1]].kind, 1), entry[1]))


def _excerpt(question: str, text: object, limit: int = 260) -> str:
    """The sentence of ``text`` that matches the question best (with the sentence after it if short).

    Lines are kept apart: a note is stored as title, summary and list entries on separate
    lines, and running those together would not read as a quote.
    """
    sentences: list[tuple[int, str]] = []
    for number, line in enumerate(str(text if text is not None else "").splitlines()):
        sentences += [(number, sentence) for sentence in _sentences(line)]
    if not sentences:
        return ""
    wanted = _question_words(question)
    best = max(range(len(sentences)), key=lambda i: (len(wanted & {_stem(t) for t in _tokens(sentences[i][1])}), -i))
    line, out = sentences[best]
    if len(out) < limit // 2 and best + 1 < len(sentences) and sentences[best + 1][0] == line:
        out += " " + sentences[best + 1][1]
    return _clip(out, limit)


def _extractive_answer(question: str, items: Sequence[Evidence]) -> Answer:
    ranked = _rank_evidence(question, items)
    order = [i for score, i in ranked if score > 0]
    if not order:  # e.g. "what did I do yesterday?": nothing to match on, show what there is
        order = sorted(i for _, i in ranked)
    chosen: dict[int, str] = {}
    seen: set[str] = set()
    for i in order:
        excerpt = _excerpt(question, items[i].text)
        key = _norm_key(excerpt)
        if not key or key in seen:
            continue  # the same words again (a sign read in two frames, a note quoting the speech)
        seen.add(key)
        chosen[i] = excerpt
        if len(chosen) >= 5:
            break
    shown = sorted(chosen, key=lambda i: _time_key(items[i], i))
    lines = [prompts.EXCERPTS_HEADER]
    for i in shown:
        item = items[i]
        label = _EVIDENCE_LABELS.get(item.kind, _one_line(item.kind) or "evidence")
        lines.append(f"- {_when(item.ts)} ({label}): “{chosen[i]}”")
    return Answer(text="\n".join(lines), sources=[items[i] for i in shown], llm_backend=EXTRACTIVE)


def _time_key(item: Evidence, index: int) -> tuple[bool, float, int]:
    return (False, float(item.ts), index) if _local(item.ts) is not None else (True, 0.0, index)  # type: ignore[arg-type]


def _llm_answer(llm: LLM, question: str, items: Sequence[Evidence]) -> Answer | None:
    """The model's answer, or None when it has nothing usable (the caller then shows excerpts)."""
    name = _llm_name(llm)
    today = f"{datetime.now():%A %d %B %Y}"
    budget = _budget_chars(llm, " ".join(_one_line(e.text)[:400] for e in items[:10]))
    room = budget - len(prompts.SYSTEM) - len(prompts.answer_prompt(question, "", today=today)) - 8
    if room < MIN_EVIDENCE_CHARS:
        log.warning("%s: context budget too small to answer from evidence; returning excerpts", name)
        return None

    # pick the best-matching evidence first, then show it to the model in time order
    per = max(240, min(1500, room // min(len(items), 12)))
    shown: list[int] = []
    used = 0
    for _, i in _rank_evidence(question, items):
        cost = min(len(_one_line(items[i].text)), per) + 60
        if shown and used + cost > room:
            break
        shown.append(i)
        used += cost
    shown.sort(key=lambda i: _time_key(items[i], i))
    lines = []
    for number, i in enumerate(shown, 1):
        item = items[i]
        label = _EVIDENCE_LABELS.get(item.kind, _one_line(item.kind) or "evidence")
        lines.append(f"[{number}] {_when(item.ts)} ({label}): {_evidence_text(item.text, per)}")
    prompt = prompts.answer_prompt(question, _squeeze("\n".join(lines), room), today=today)
    raw = llm.json(system=prompts.SYSTEM, prompt=prompt, schema=prompts.ANSWER_SCHEMA, max_tokens=700)
    data = _coerced(raw, prompts.ANSWER_SCHEMA)

    cited: list[int] = []
    for number in data["evidence_used"][:50]:
        if isinstance(number, int) and 1 <= number <= len(shown) and shown[number - 1] not in cited:
            cited.append(shown[number - 1])
    sources = [items[i] for i in cited] + [items[i] for i in shown if i not in cited]
    if data["answerable"] == "no":
        return Answer(text=prompts.NOT_IN_EVIDENCE, sources=sources, llm_backend=name)
    text = _clip(" ".join(_sentences(_one_line(data["answer"]))[: prompts.ANSWER_MAX_SENTENCES + 2]), 1500)
    if _is_placeholder(text):
        log.warning("%s returned an empty answer; returning the closest excerpts instead", name)
        return None
    return Answer(text=text, sources=sources, llm_backend=name)


def answer_question(llm: LLM | None, question: str, evidence: list[Evidence]) -> Answer:
    """Answer a question strictly from retrieved evidence.

    With a model the answer is one to four sentences that cite the dates and clock times of
    the evidence they rest on; when the evidence does not contain the answer, the answer
    says exactly that.  ``sources`` are the evidence items the model was shown, the ones it
    cited first.

    Without a model (or when it fails) the answer is the best-matching excerpts, quoted and
    labelled as excerpts, with ``llm_backend == "extractive"``.  With no evidence at all the
    answer says that nothing was found, and no model is called.
    """
    question = _evidence_text(question, 600)
    items = [e for e in evidence or [] if e is not None and _one_line(getattr(e, "text", ""))]
    if not items:
        return Answer(text=prompts.NO_EVIDENCE, sources=[], llm_backend=EXTRACTIVE)
    if llm is None or not question:
        return _extractive_answer(question, items)
    try:
        answer = _llm_answer(llm, question, items)
    except Exception as exc:  # asking must always give something back
        log.warning(
            "%s failed to answer (%s: %s); returning the closest excerpts instead", _llm_name(llm), type(exc).__name__, exc
        )
        answer = None
    return answer if answer is not None else _extractive_answer(question, items)
