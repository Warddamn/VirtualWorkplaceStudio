"""Write the Markdown vault: one note per session, one per day.

Layout (``<vault>`` is ``Settings.vault_dir``, by default ``<home>/notes``)::

    <vault>/days/2026-11-22.md
    <vault>/sessions/2026-11-22 1432 Planning meeting.md
    <vault>/assets/<session_id>/kf_000123.jpg      copies of the embedded keyframes

The notes are plain Markdown with YAML front matter, standard relative links
and image embeds, so they read the same in Obsidian, in VS Code, on GitHub or
in any other Markdown viewer.  The only HTML used is a collapsed
``<details>`` block per moment holding the transcript, and a closing comment
saying the file is generated.

Rules this module keeps
-----------------------
* **Generated files.**  A note is rewritten from the library every time it is
  rendered; edits made to it by hand are lost, with one exception: action items
  that were ticked (``- [x]``, or any other mark in the box) stay marked as long
  as their text is unchanged.
* **One file per session.**  Re-rendering replaces the session's previous file
  even when the title, and with it the file name, changed.  A file that belongs
  to another session (or to the user) is never overwritten: the note gets a
  ``(2)``, ``(3)`` … suffix instead.
* **Nothing half-written.**  Files are written to a temporary name and moved
  into place; unchanged files are not touched at all.
* **Untrusted text stays text.**  Transcripts, on-screen text, captions and
  whatever a language model wrote are escaped so they cannot start headings,
  open HTML, close the transcript block, form links or leak into the front matter.
* All times shown are local time (:mod:`videonotes.timeutil`).
"""

from __future__ import annotations

import bisect
import contextlib
import dataclasses
import errno
import hashlib
import json
import logging
import math
import os
import re
import secrets
import shutil
from collections.abc import Callable, Iterable, Sequence
from datetime import date as _date
from datetime import datetime
from pathlib import Path
from typing import Any

from ..config import NotesSettings, Settings, is_macos
from ..models import ActionItem, Keyframe, Moment, Session, SessionNote, Utterance
from ..store import Store
from ..timeutil import day_bounds, fmt_duration, local_dt, slugify
from .moments import segment_moments

log = logging.getLogger("videonotes.render")

__all__ = ["NoteRenderError", "render_day_note", "render_session_note"]


class NoteRenderError(RuntimeError):
    """A note could not be written. The message says what is wrong and what to do about it."""


_UNTITLED = "Untitled session"
_IMAGE_SUFFIXES = (".jpg", ".jpeg", ".png", ".webp", ".gif")
_ASSET_NAME = re.compile(r"kf_[0-9a-f]+\.[a-z0-9]{1,5}")
_TEMP_NAME = re.compile(r"\.vnote-[0-9a-f]+\.tmp")

# Bounds that keep a note readable (and its size sane) whatever the recording contained.
_MAX_TITLE_CHARS = 160
_MAX_SLUG_BYTES = 180  # title part of a file name; with date, time and " (2).md" it stays below the 255-byte limit
_MAX_TAGS = 24
_MAX_TAG_CHARS = 48
_MAX_ALT_CHARS = 200
_MAX_SCREEN_LINES_PER_MOMENT = 40
_MAX_SCREEN_CHARS_PER_MOMENT = 2000
_MAX_CAPTURED_ENTRIES = 60
_MAX_CAPTURED_CHARS = 8000
_MAX_UTTERANCE_CHARS = 2000
_TRANSCRIPT_JOIN_GAP_S = 1.5  # utterances closer together than this share one transcript line …
_TRANSCRIPT_LINE_CHARS = 320  # … up to about this many characters

_TASKS_HEADING = "## Action items"  # also how _ticked_tasks finds the list again when a note is rendered anew
_FOOTER = (
    "<!-- Written by videonotes. This file is regenerated from the library whenever the {what} is processed "
    "again: edits made here are overwritten (ticked action items are kept). -->"
)


# =============================================================================
# Public API
# =============================================================================


def render_session_note(settings: Settings, store: Store, session_id: str) -> Path:
    """Write ``<vault>/sessions/<date> <time> <title>.md`` (+ copies of embedded keyframes
    under ``<vault>/assets/<session_id>/``). Returns the Markdown path. Re-rendering a session
    replaces its previous file even if the title changed.

    A session that has not been summarised yet still gets a note built from its
    moments, transcript, on-screen text and keyframes, marked as unsummarised.
    The path is recorded in ``session.note_path`` (relative to home).

    Raises :class:`NoteRenderError` when the session does not exist or the vault
    cannot be written to.
    """
    session = store.get_session(session_id)
    if session is None:
        raise NoteRenderError(
            f"There is no session {session_id!r} in this library. Run `vnote sessions` to see the ones that exist."
        )
    started = _local(session.started_ts)
    if started is None:
        raise NoteRenderError(
            f"Session {session_id} has no usable start time ({session.started_ts!r}), so its note cannot be named. "
            "Delete it with `vnote delete` and import the recording again."
        )
    cfg = settings.notes
    utterances = store.list_utterances(session_id=session_id)
    keyframes = store.list_keyframes(session_id=session_id)
    moments = sorted(store.list_moments(session_id), key=lambda m: (m.ts0, m.idx))
    if not moments and (utterances or keyframes):
        # not segmented yet (or segmentation was cleared): work out moments for display only
        moments = segment_moments(session, utterances, keyframes, cfg)
    note = session.note

    vault = _vault(settings)
    notes_dir = vault / "sessions"
    assets_dir = vault / "assets" / _safe_component(session_id)
    title = _session_title(session)
    start, end = _session_span(session, store, utterances, keyframes, moments)
    clock = _clock_formatter(cfg.time_format)
    clock_s = _clock_formatter(_with_seconds(cfg.time_format))

    previous = settings.abs(session.note_path) if session.note_path else None
    try:
        notes_dir.mkdir(parents=True, exist_ok=True)
        stem = f"{started:%Y-%m-%d %H%M} {_fit_bytes(slugify(title), _MAX_SLUG_BYTES)}"
        target = _free_path(notes_dir, stem, session_id, previous)
        ticked = {**(_ticked_tasks(previous) if previous is not None else {}), **_ticked_tasks(target)}

        embedder = _Embedder(settings, assets_dir, enabled=bool(cfg.embed_images))
        blocks: list[str] = [
            _front_matter(
                [
                    ("title", title),
                    ("date", started.date()),
                    ("start", started),
                    ("end", _local(end) or started),
                    ("duration", fmt_duration(end - start)),
                    ("session_id", session.id),
                    ("kind", session.kind),
                    ("source", session.source),
                    ("tags", _tags(note.tags if note else [t for m in moments for t in m.tags])),
                    ("summarizer", (note.llm_backend or "unknown") if note else "none"),
                ]
            ),
            f"# {_md(title)}",
            _context_line(started, _time_range(start, end, clock), end - start, session.source or session.kind),
        ]
        if note is None:
            blocks.append(
                "> **Not summarised yet.** This note was put together straight from the recording — what was "
                "said, the text that was in view and a few frames — without a written summary. "
                "Run `vnote process` to add one."
            )
        else:
            blocks += _note_sections(note, ticked, start, end, clock)
        captured = note.captured_text if note is not None else [k.ocr_text or "" for k in keyframes]
        captured_block = _verbatim_block(_dedupe_texts(captured))
        if captured_block:
            blocks += ["## Captured text", captured_block]
        if moments:
            blocks.append("## Timeline")
            members = _assign(moments, utterances, keyframes)
            for moment, (said, seen) in zip(moments, members, strict=True):
                blocks += _moment_blocks(moment, said, seen, cfg, embedder, clock, clock_s)
        elif note is None:
            blocks.append(
                "*Nothing has been recognised in this recording so far: no speech, no text in view, no frames.*"
            )
        blocks.append(_FOOTER.format(what="session"))

        _write_atomic(target, "\n\n".join(blocks) + "\n")
    except OSError as exc:
        raise _cannot_write(settings, vault, exc) from exc

    stored = settings.rel(target)
    if stored != session.note_path:
        store.update_session(session_id, note_path=stored)
    if previous is not None:
        _remove_previous(previous, target, session_id, vault)
    embedder.prune()
    if embedder.missing:
        log.info(
            "session %s: %d keyframe image(s) are missing or unreadable and were left out of the note",
            session_id, embedder.missing,
        )  # fmt: skip
    log.info("wrote %s", target)
    return target


def render_day_note(settings: Settings, store: Store, date: str) -> Path:
    """Write ``<vault>/days/<date>.md`` for one local calendar day (``YYYY-MM-DD``) and return its path.

    Shows the stored :class:`~videonotes.models.DayDigest` when there is one
    (headline, summary, highlights, merged action items) and always lists the
    sessions that started on that day, each linked to its note.  A day without
    sessions yields a note that says so.  A digest written from sessions that
    have all been deleted since is left out; one that lost only some of them is
    shown with a line saying so.  When a digest exists, the note's path is
    stored with it (``store.save_day``).

    Raises :class:`NoteRenderError` for a malformed date or an unwritable vault.
    """
    try:
        day = _date.fromisoformat(str(date).strip())
    except ValueError:
        raise NoteRenderError(
            f"{date!r} is not a calendar day. Write it as YYYY-MM-DD, for example 2026-11-22."
        ) from None
    iso = day.isoformat()
    cfg = settings.notes
    clock = _clock_formatter(cfg.time_format)
    try:
        lo, hi = day_bounds(day)
    except (ValueError, OverflowError, OSError):
        raise NoteRenderError(
            f"{iso} is outside the range of dates this computer can work with. Write the day as YYYY-MM-DD, "
            "for example 2026-11-22."
        ) from None
    sessions = sorted(store.list_sessions(since_ts=lo, until_ts=hi), key=lambda s: (s.started_ts, s.id))
    stored = store.get_day(iso)

    vault = _vault(settings)
    days_dir = vault / "days"
    target = days_dir / f"{iso}.md"
    ticked = _ticked_tasks(target)

    # A digest describes the sessions it was written from. Sessions can be deleted afterwards: a digest whose
    # sessions are all gone is not shown, one that lost some of them is shown with a note saying so.
    digest = stored
    gone = 0
    if stored is not None and stored.session_ids:
        present = {s.id for s in sessions}
        gone = sum(1 for sid in stored.session_ids if sid not in present)
        if gone == len(stored.session_ids):
            digest = None

    front: list[tuple[str, object]] = [("title", iso), ("date", day), ("sessions", len(sessions))]
    if digest is not None:
        front.append(("summarizer", digest.llm_backend or "unknown"))
    # weekday and month names follow the process locale, so they are escaped like any other text
    blocks: list[str] = [_front_matter(front), "# " + _md(f"{day:%A} {day.day} {day:%B %Y}")]
    if digest is not None:
        headline = _md(digest.headline)
        if headline:  # judged after cleaning: a headline of control characters only must not leave "****" behind
            blocks.append(f"**{headline}**")
        if gone:
            blocks.append(
                f"*This digest was written when the day still had {gone} more session{'s' if gone != 1 else ''}, "
                f"deleted since. Run `vnote day {iso}` to write it again.*"
            )
        summary = _prose(digest.summary)
        if summary:
            blocks += ["## Summary", summary]
        highlights = _bullets(digest.highlights)
        if highlights:
            blocks += ["## Highlights", highlights]
        tasks = _task_lines(digest.action_items, ticked, lo, hi, clock)
        if tasks:
            blocks += [_TASKS_HEADING, tasks]
    blocks.append("## Sessions")
    if sessions:
        recorded = sum(_recorded_seconds(store, x) for x in sessions)
        count = "1 session" if len(sessions) == 1 else f"{len(sessions)} sessions"
        blocks.append(f"*{count} · {fmt_duration(recorded)} recorded*")
        blocks.append("\n".join(_session_line(settings, store, s, days_dir, clock) for s in sessions))
    else:
        blocks.append("*No sessions were recorded on this day.*")
    blocks.append(_FOOTER.format(what="day"))

    try:
        days_dir.mkdir(parents=True, exist_ok=True)
        _write_atomic(target, "\n\n".join(blocks) + "\n")
    except OSError as exc:
        raise _cannot_write(settings, vault, exc) from exc
    if stored is not None:
        if stored.date != iso:
            stored = dataclasses.replace(stored, date=iso)
        store.save_day(stored, settings.rel(target))
    log.info("wrote %s", target)
    return target


# =============================================================================
# Text hygiene and escaping
# =============================================================================

# Characters that must never reach a note, as code-point ranges: C0/C1 controls (tab and newline excepted),
# bidirectional embeddings / overrides / isolates, the byte-order mark, non-characters and lone surrogates.
_UNPRINTABLE_RANGES = (
    (0x00, 0x08), (0x0B, 0x0C), (0x0E, 0x1F), (0x7F, 0x9F), (0x202A, 0x202E), (0x2066, 0x2069),
    (0xFEFF, 0xFEFF), (0xFFFE, 0xFFFF), (0xD800, 0xDFFF),
)  # fmt: skip
_UNPRINTABLE = re.compile(
    "[" + "".join(f"{re.escape(chr(a))}-{re.escape(chr(b))}" for a, b in _UNPRINTABLE_RANGES) + "]"
)
# Everything Unicode treats as a line break: CR LF, CR, VT, FF, NEL, LINE SEPARATOR, PARAGRAPH SEPARATOR.
_NEWLINES = re.compile("\r\n|[" + "".join(chr(c) for c in (0x0D, 0x0B, 0x0C, 0x85, 0x2028, 0x2029)) + "]")


def _clean(text: object) -> str:
    """Text without control / direction-override characters, with ``\\n`` as the only line break."""
    return _UNPRINTABLE.sub("", _NEWLINES.sub("\n", str(text)))


def _one_line(text: object) -> str:
    return " ".join(_clean(text).split())


def _shorten(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    cut = text[: limit - 1]
    space = cut.rfind(" ")
    if space > limit * 0.6:
        cut = cut[:space]
    return cut.rstrip(" ,;:-") + "…"


_MD_ALWAYS = re.compile(r"([\\`\[\]|$#^~])")
_MD_EMPHASIS = re.compile(r"([*_])")
_MD_RUNS = re.compile(r"={2,}|%{2,}")  # Obsidian ==highlight== and %%comment%%
_MD_LEADING_NUMBER = re.compile(r"^(\d{1,9})([.)])(?=\s|$)")
_MD_LEADING_MARK = re.compile(r"^([-+=:>])")
# "&" only needs attention where it would be read as a character reference: &name; &#123; &#x1F;
_MD_REFERENCE = re.compile(r"&(?=#?[0-9A-Za-z]{1,32};)")
_MD_LEADING_RUN = re.compile(r"^([*_]+)(?=\s|$)")


def _md(text: object, *, emphasis: bool = False) -> str:
    """One line of untrusted text, inert wherever it is placed in Markdown.

    Every ``<`` becomes ``&lt;``, so no HTML tag, comment or autolink can form;
    characters that form links, code, tables, tags, maths, comments or block ids
    (Markdown and Obsidian) are backslash-escaped; and whatever would start a
    block at the beginning of a line (heading, list, quote, rule, table, code)
    is defused.  With ``emphasis=True`` the inline emphasis characters ``*`` and
    ``_`` are left alone (used for prose written by the summariser, where
    ``**bold**`` is welcome and cannot break structure).

    No more is escaped than that: ``R&D`` and ``a -> b`` stay as they are (an
    ``&`` is touched only where it would be read as a character reference, a
    ``>`` only at the very start).  The notes are also read as plain text,
    searched by what was literally said, and shown by editors that do not decode
    entities while editing.
    """
    s = _one_line(text)
    s = _MD_REFERENCE.sub("&amp;", s).replace("<", "&lt;")
    s = _MD_ALWAYS.sub(r"\\\1", s)
    s = _MD_RUNS.sub(lambda m: "".join("\\" + ch for ch in m.group(0)), s)
    if emphasis:
        s = _MD_LEADING_RUN.sub(lambda m: "".join("\\" + ch for ch in m.group(1)), s)
    else:
        s = _MD_EMPHASIS.sub(r"\\\1", s)
    s = _MD_LEADING_NUMBER.sub(r"\1\\\2", s)
    return _MD_LEADING_MARK.sub(r"\\\1", s)


_HTML_ENTITIES = {
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "`": "&#96;", "*": "&#42;", "_": "&#95;",
    "[": "&#91;", "]": "&#93;", "#": "&#35;", "|": "&#124;", "$": "&#36;", "\\": "&#92;", "~": "&#126;",
    "^": "&#94;", "%": "&#37;", "=": "&#61;",
}  # fmt: skip
_HTML_SPECIAL = re.compile("[" + re.escape("".join(_HTML_ENTITIES)) + "]")


def _html(text: object) -> str:
    """One line of untrusted text for use inside an HTML block.

    Besides the HTML metacharacters, every character that Markdown or Obsidian
    could still interpret (should a viewer parse Markdown inside HTML) becomes
    a numeric entity.
    """
    return _HTML_SPECIAL.sub(lambda m: _HTML_ENTITIES[m.group(0)], _one_line(text))


def _fenced(text: str) -> str:
    """Verbatim text in a fenced code block whose fence is longer than any backtick run inside."""
    longest = max((len(run) for run in re.findall(r"`+", text)), default=0)
    fence = "`" * max(3, longest + 1)
    return f"{fence}text\n{text}\n{fence}"


def _yaml_scalar(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%dT%H:%M:%S")
    if isinstance(value, _date):
        return value.isoformat()
    # a JSON string is a valid YAML double-quoted scalar; _one_line removed everything YAML forbids
    return json.dumps(_one_line(value), ensure_ascii=False)


def _front_matter(fields: list[tuple[str, object]]) -> str:
    """YAML front matter: one ``key: value`` per line, lists in block style, every string double-quoted."""
    lines = ["---"]
    for key, value in fields:
        if isinstance(value, (list, tuple)):
            lines.append(f"{key}:" if value else f"{key}: []")
            lines += [f"  - {_yaml_scalar(item)}" for item in value]
        else:
            lines.append(f"{key}: {_yaml_scalar(value)}")
    lines.append("---")
    return "\n".join(lines)


def _tags(raw: Iterable[object]) -> list[str]:
    """Tags in the form Obsidian accepts: letters, digits, ``_``, ``-`` and ``/``, with at least one letter;
    no spaces, no ``#``. Compared without regard to case, like Obsidian does."""
    out: list[str] = []
    seen: set[str] = set()
    for item in raw:
        tag = re.sub(r"[^\w/]+", "-", _one_line(item).lstrip("#"), flags=re.UNICODE)
        tag = re.sub(r"-*/[-/]*", "/", tag)[:_MAX_TAG_CHARS].strip("-/")
        if any(ch.isalpha() for ch in tag) and tag.casefold() not in seen:
            seen.add(tag.casefold())
            out.append(tag)
            if len(out) >= _MAX_TAGS:
                break
    return out


# =============================================================================
# Time
# =============================================================================


def _local(ts: object) -> datetime | None:
    """Local datetime of an epoch timestamp, or None when it is not a usable timestamp."""
    if isinstance(ts, (bool, str, bytes)) or ts is None:
        return None
    try:
        return local_dt(float(ts)) if math.isfinite(ts) else None  # type: ignore[arg-type]
    except (TypeError, OverflowError, OSError, ValueError):
        return None


def _clock_formatter(fmt: str) -> Callable[[float], str]:
    """``ts -> clock text`` using the user's ``notes.time_format`` (falling back to HH:MM if it is unusable)."""

    def clock(ts: float) -> str:
        moment = _local(ts)
        if moment is None:
            return "??:??"
        try:
            text = _one_line(moment.strftime(fmt))
        except ValueError:
            text = ""
        return text or moment.strftime("%H:%M")

    return clock


def _with_seconds(fmt: str) -> str:
    """The same clock format, showing seconds too (for transcript lines and frames)."""
    if any(code in fmt for code in ("%S", "%T", "%X", "%c")):
        return fmt
    return fmt.replace("%M", "%M:%S", 1) if "%M" in fmt else fmt


def _time_range(start: float, end: float, clock: Callable[[float], str]) -> str:
    a, b = clock(start), clock(end)
    if a == b:
        return a
    d0, d1 = _local(start), _local(end)
    days = (d1.date() - d0.date()).days if d0 is not None and d1 is not None else 0
    return f"{a}–{b}" + (f" (+{days} d)" if days > 0 else "")


def _session_span(
    session: Session, store: Store, utterances: list[Utterance], keyframes: list[Keyframe], moments: list[Moment]
) -> tuple[float, float]:
    """(start, end) of a session; the end is taken from the clips / material when the session is still open."""
    start = float(session.started_ts)
    end = session.ended_ts
    if end is None or _local(end) is None:
        bounds = store.session_bounds(session.id)
        candidates = [bounds[1]] if bounds else []
        candidates += [u.ts1 for u in utterances] + [k.ts for k in keyframes] + [m.ts1 for m in moments]
        end = max((c for c in candidates if _local(c) is not None), default=start)
    return start, max(start, float(end))


def _context_line(started: datetime, time_range: str, seconds: float, source: str) -> str:
    parts = [_md(f"{started:%A} {started:%Y-%m-%d}"), _md(time_range), fmt_duration(seconds)]
    if _one_line(source):
        parts.append(_md(source))
    return "*" + " · ".join(parts) + "*"


# =============================================================================
# Session note pieces
# =============================================================================


def _session_title(session: Session) -> str:
    for candidate in (session.note.title if session.note else "", session.title):
        text = _one_line(candidate)
        if text:
            return _shorten(text, _MAX_TITLE_CHARS)
    return _UNTITLED


def _note_sections(
    note: SessionNote, ticked: dict[str, str], start: float, end: float, clock: Callable[[float], str]
) -> list[str]:
    blocks: list[str] = []
    summary = _prose(note.summary)
    if summary:
        blocks += ["## Summary", summary]
    points = _bullets(note.key_points)
    if points:
        blocks += ["## Key points", points]
    tasks = _task_lines(note.action_items, ticked, start - 60.0, end + 60.0, clock)
    if tasks:
        blocks += [_TASKS_HEADING, tasks]
    for heading, items in (("Decisions", note.decisions), ("Open questions", note.open_questions)):
        listing = _bullets(items)
        if listing:
            blocks += [f"## {heading}", listing]
    who = _inline_list(note.people)
    where = _inline_list(note.places)
    if who or where:
        lines = ([f"- **People:** {who}"] if who else []) + ([f"- **Places:** {where}"] if where else [])
        blocks += ["## People and places", "\n".join(lines)]
    return blocks


# "- item", "* item", "+ item", bullet characters (U+2022, U+2023, U+25E6) and "1." / "1)" at the start of a line
_BULLET = re.compile(r"^\s*(?:[-*+" + "".join(chr(c) for c in (0x2022, 0x2023, 0x25E6)) + r"]|\d{1,3}[.)])\s+(?=\S)")


def _prose(text: str) -> str:
    """Free text from the summariser as paragraphs (and simple bullet lists), each line defused."""
    blocks: list[str] = []
    kind = ""
    for raw in [*_clean(text).split("\n"), ""]:
        line = raw.strip()
        if not line:
            kind = ""
            continue
        bullet = _BULLET.match(raw)
        if bullet:
            item = "- " + _md(raw[bullet.end() :], emphasis=True)
            if kind == "list":
                blocks[-1] += "\n" + item
            else:
                blocks.append(item)
            kind = "list"
        else:
            piece = _md(line, emphasis=True)
            if kind == "text":
                blocks[-1] += "\n" + piece
            else:
                blocks.append(piece)
            kind = "text"
    return "\n\n".join(blocks)


def _bullets(items: Iterable[object]) -> str:
    lines = [f"- {_md(item, emphasis=True)}" for item in items if _one_line(item)]
    return "\n".join(lines)


def _inline_list(items: Iterable[object]) -> str:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        text = _one_line(item)
        if text and text.casefold() not in seen:
            seen.add(text.casefold())
            out.append(_md(text))
    return ", ".join(out)


def _task_lines(
    items: Iterable[ActionItem], ticked: dict[str, str], lo: float, hi: float, clock: Callable[[float], str]
) -> str:
    """Action items as task checkboxes; owner / due / clock time only when known.

    ``ticked`` maps the text of tasks the user marked in the previous version of the note to their mark.
    """
    lines: list[str] = []
    for item in items:
        text = _md(item.text, emphasis=True)
        if not text:
            continue
        extras: list[str] = []
        if _one_line(item.owner):
            extras.append(f"owner: {_md(item.owner)}")
        if _one_line(item.due):
            extras.append(f"due: {_md(item.due)}")
        ts: Any = item.ts  # whatever the summariser put there: only a timestamp inside the range is shown
        if _local(ts) is not None and lo <= ts <= hi:
            extras.append(_md(clock(ts)))
        body = text + (f" ({'; '.join(extras)})" if extras else "")
        lines.append(f"- [{ticked.get(body, ' ')}] {body}")
    return "\n".join(lines)


_TICKED = re.compile(r"^- \[([^\s\[\]\\])\] (.*\S)\s*$")
_FENCE_OPEN = re.compile(r"`{3,}")  # how _fenced opens a code block: at the start of a line, never indented


def _ticked_tasks(path: Path) -> dict[str, str]:
    """Task lines marked in an existing note, as ``{text: mark}``, so that re-rendering keeps them marked.

    The mark is usually ``x``; Obsidian treats any character in the box as done, and some people use ``-`` or ``/``.

    Only the note's own action-item list is read: the ``## Action items`` section, up to the next heading.
    Code blocks are skipped, because they hold text quoted from the recording: a to-do list that was on screen
    is shown verbatim, and a ticked box seen there (or a line that reads like our heading) must never tick the
    user's own item.
    """
    ticked: dict[str, str] = {}
    try:
        with path.open(encoding="utf-8", errors="replace") as fh:
            fence = ""  # the backticks that opened the code block we are in
            inside = False
            for line in fh:
                line = line.rstrip()
                if fence:
                    if line.startswith(fence) and not line.strip("`"):
                        fence = ""
                    continue
                opening = _FENCE_OPEN.match(line)
                if opening:
                    fence = opening.group(0)
                elif not inside:
                    inside = line == _TASKS_HEADING
                elif line.startswith("#"):
                    break
                else:
                    match = _TICKED.match(line)
                    if match:
                        ticked[match.group(2)] = match.group(1)
    except (OSError, ValueError):
        return {}
    return ticked


def _text_key(line: str) -> str:
    key = "".join(ch for ch in line.casefold() if ch.isalnum())
    return key or line.strip()


def _dedupe_texts(texts: Iterable[object]) -> list[str]:
    """Verbatim text blocks without repeats.

    The same whiteboard is read from many frames, each time with slightly
    different punctuation or case: a block is dropped when every one of its
    lines (compared by letters and digits only) has been seen before.
    """
    seen: set[str] = set()
    out: list[str] = []
    for text in texts:
        lines = [" ".join(line.split()) for line in _clean(text or "").split("\n")]
        lines = [line for line in lines if line]
        keys = {_text_key(line) for line in lines}
        if not keys or keys <= seen:
            continue
        seen |= keys
        out.append("\n".join(lines))
    return out


def _verbatim_block(
    texts: list[str], *, max_entries: int = _MAX_CAPTURED_ENTRIES, max_chars: int = _MAX_CAPTURED_CHARS
) -> str:
    """De-duplicated verbatim texts: single lines as a list, multi-line texts as fenced blocks."""
    blocks: list[str] = []
    in_list = False
    used = 0
    shown = 0
    for text in texts:
        if shown >= max_entries or used + len(text) > max_chars and shown > 0:
            break
        if len(text) > max_chars:
            text = text[:max_chars].rstrip() + " …"
        shown += 1
        used += len(text)
        if "\n" in text:
            blocks.append(_fenced(text))
            in_list = False
        elif in_list:
            blocks[-1] += f"\n- {_md(text)}"
        else:
            blocks.append(f"- {_md(text)}")
            in_list = True
    if shown < len(texts):
        blocks.append(f"*… and {len(texts) - shown} more (search the library to find them).*")
    return "\n\n".join(blocks)


def _assign(
    moments: list[Moment], utterances: list[Utterance], keyframes: list[Keyframe]
) -> list[tuple[list[Utterance], list[Keyframe]]]:
    """What belongs to each moment: by the ids it lists, anything left over by its start time."""
    starts = [m.ts0 for m in moments]

    def split(items: Sequence[Any], id_lists: list[list[int]], when: Callable[[Any], float]) -> list[list[Any]]:
        by_id = {item.id: item for item in items if item.id is not None}
        claimed: set[int] = set()
        groups: list[list[Any]] = []
        for ids in id_lists:
            group: list[Any] = []
            for i in ids:
                if i in by_id and i not in claimed:
                    claimed.add(i)
                    group.append(by_id[i])
            groups.append(group)
        for item in items:
            if item.id is None or item.id not in claimed:
                groups[max(0, bisect.bisect_right(starts, when(item)) - 1)].append(item)
        for group in groups:
            group.sort(key=lambda item: (when(item), item.id if item.id is not None else 0))
        return groups

    said = split(utterances, [m.utterance_ids for m in moments], lambda u: u.ts0)
    seen = split(keyframes, [m.keyframe_ids for m in moments], lambda k: k.ts)
    return list(zip(said, seen, strict=True))


def _moment_blocks(
    moment: Moment,
    said: list[Utterance],
    seen: list[Keyframe],
    cfg: NotesSettings,
    embedder: _Embedder,
    clock: Callable[[float], str],
    clock_s: Callable[[float], str],
) -> list[str]:
    """One timeline entry: heading, summary, images, on-screen text, collapsed transcript."""
    heading = f"### {_md(_time_range(moment.ts0, moment.ts1, clock))}"
    title = _shorten(_one_line(moment.title or ""), _MAX_TITLE_CHARS)
    if title:
        heading += f"  {_md(title)}"
    blocks = [heading]

    salience = getattr(moment, "salience", "normal")
    kind = str(getattr(moment, "kind", "") or "").replace("_", " ")
    labels = ["\u2605 highlight"] if salience == "highlight" else []
    labels += [_md(kind)] if kind != "other" else []
    labels += [_md(tag) for tag in _tags(moment.tags or [])]
    labels = [label for label in labels if label]
    if labels:
        blocks.append("*" + " · ".join(labels) + "*")
    background = salience == "background"
    # background moments (idle stretches, transit …) are kept to one line
    summary = str(moment.summary or "")
    summary = _md(_first_sentence(summary), emphasis=True) if background else _prose(summary)
    if summary:
        blocks.append(f"*{summary}*" if background else summary)

    if not background:
        limit = max(0, int(cfg.max_images_per_moment))
        for frame in _pick_images([k for k in seen if embedder.available(k)] if limit else [], limit):
            link = embedder.embed(frame)
            if link is None:
                continue
            caption = _one_line(frame.caption or "")
            alt = _shorten(caption, _MAX_ALT_CHARS) if caption else f"Frame at {clock_s(frame.ts)}"
            blocks.append(f"![{_md(alt)}]({link})")
            blocks.append(f"*{_md(clock_s(frame.ts))}" + (f" — {_md(caption)}*" if caption else "*"))
        on_screen = _screen_text(seen)
        if on_screen:
            blocks += ["**On screen**", _fenced(on_screen)]

    if cfg.include_transcript:
        transcript = _transcript(said, clock_s)
        if transcript:
            blocks.append(transcript)
    return blocks


# whitespace after ". ! ?" or their CJK counterparts (U+3002, U+FF01, U+FF1F)
_SENTENCE_END = re.compile("(?<=[.!?" + "".join(chr(c) for c in (0x3002, 0xFF01, 0xFF1F)) + r"])\s")


def _first_sentence(text: str, limit: int = 220) -> str:
    line = _one_line(text)
    match = _SENTENCE_END.search(line)
    if match and match.start() >= 12:
        line = line[: match.start()]
    return _shorten(line, limit)


def _screen_text(frames: list[Keyframe]) -> str:
    """Everything read on screen during a moment, de-duplicated and bounded."""
    lines: list[str] = []
    for text in _dedupe_texts(k.ocr_text or "" for k in frames):
        if lines:
            lines.append("")
        lines += text.split("\n")
    kept: list[str] = []
    used = 0
    for line in lines:
        if len(kept) >= _MAX_SCREEN_LINES_PER_MOMENT or used + len(line) > _MAX_SCREEN_CHARS_PER_MOMENT:
            break
        kept.append(line)
        used += len(line)
    while kept and not kept[-1]:
        kept.pop()
    if not kept and lines:  # one enormous first line
        kept = [lines[0][:_MAX_SCREEN_CHARS_PER_MOMENT].rstrip()]
    dropped = sum(1 for line in lines[len(kept) :] if line)
    if dropped and kept:
        kept.append(f"… ({dropped} more line{'s' if dropped != 1 else ''})")
    return "\n".join(kept)


def _number(value: object) -> float:
    try:
        return float(value) if math.isfinite(value) else 0.0  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return 0.0


def _pick_images(frames: list[Keyframe], limit: int) -> list[Keyframe]:
    """Up to ``limit`` frames worth embedding, in time order.

    Chosen one at a time.  What counts, in this order: the frame tells something
    the frames chosen so far do not (text read on it that has not been shown
    yet, a caption); it is far in time from the ones already chosen, so the
    picks spread over the moment; it marks a new scene; novelty; sharpness.
    """
    if limit <= 0 or not frames:
        return []
    frames = sorted(frames, key=lambda k: (k.ts, k.id if k.id is not None else 0))
    if len(frames) <= limit:
        return frames
    span = max(frames[-1].ts - frames[0].ts, 1e-9)
    texts = [{_text_key(line) for line in _clean(k.ocr_text or "").split("\n") if line.strip()} for k in frames]
    captions = [_text_key(_one_line(k.caption or "")) for k in frames]
    chosen: list[int] = []
    shown: set[str] = set()
    while len(chosen) < limit:
        best: tuple[tuple[int, int, int, float, float], int] | None = None
        for i, frame in enumerate(frames):
            if i in chosen:
                continue
            informative = int(bool(texts[i] - shown)) + int(bool(captions[i]) and captions[i] not in shown)
            apart = min((abs(frame.ts - frames[j].ts) for j in chosen), default=0.0)
            rank = (
                informative,
                int(10 * apart / span),  # in tenths of the moment, so near-ties fall through to quality
                int(frame.reason in ("scene", "first")),
                _number(frame.novelty),
                _number(frame.sharpness),
            )
            if best is None or rank > best[0]:  # ties keep the earlier frame
                best = (rank, i)
        assert best is not None  # len(frames) > limit, so something is always left
        chosen.append(best[1])
        shown |= texts[best[1]]
        if captions[best[1]]:
            shown.add(captions[best[1]])
    return [frames[i] for i in sorted(chosen)]


def _transcript(said: list[Utterance], clock_s: Callable[[float], str]) -> str:
    """The transcript as one HTML block: ``<details>`` collapsed by default, a clock time per line.

    It is deliberately a single HTML block without blank lines: Markdown is not
    interpreted inside, so nothing that was said can break out of it.
    """
    lines: list[tuple[float, str, str]] = []  # (start, speaker, text)
    last_end = -math.inf
    for u in said:
        text = _shorten(_one_line(u.text), _MAX_UTTERANCE_CHARS)
        if not text:
            continue
        speaker = _one_line(u.speaker or "")
        if (
            lines
            and lines[-1][1] == speaker
            and u.ts0 - last_end <= _TRANSCRIPT_JOIN_GAP_S
            and len(lines[-1][2]) + len(text) < _TRANSCRIPT_LINE_CHARS
        ):
            lines[-1] = (lines[-1][0], speaker, f"{lines[-1][2]} {text}")
        else:
            lines.append((u.ts0, speaker, text))
        last_end = max(last_end, u.ts1, u.ts0)
    if not lines:
        return ""
    count = f"{len(lines)} line{'s' if len(lines) != 1 else ''}"
    out = ["<details>", f"<summary>Transcript · {count}</summary>", "<p>"]
    for ts, speaker, text in lines:
        label = _html(clock_s(ts)) + (f" {_html(speaker)}:" if speaker else "")
        out.append(f"<b>{label}</b> {_html(text)}<br>")
    out += ["</p>", "</details>"]
    return "\n".join(out)


# =============================================================================
# Day note pieces
# =============================================================================


def _recorded_seconds(store: Store, session: Session) -> float:
    """Footage in a session: the clips' own durations (breaks between clips do not count)."""
    clips = store.list_clips(session.id)
    if clips:
        return sum(max(0.0, _number(clip.duration)) for clip in clips)
    start, end = _session_span(session, store, [], [], [])
    return end - start


def _session_line(
    settings: Settings, store: Store, session: Session, days_dir: Path, clock: Callable[[float], str]
) -> str:
    """One entry of the day's session list: time range, title (linked when its note exists), one-line summary."""
    start, end = _session_span(session, store, [], [], [])
    title = _md(_session_title(session))
    path = settings.abs(session.note_path) if session.note_path else None
    if path is not None and path.is_file():
        title = f"[{title}]({_relative_link(path, days_dir)})"
    if session.note is None:
        tail = " — *not summarised yet*"
    else:
        summary = _first_sentence(session.note.summary)
        tail = f" — {_md(summary, emphasis=True)}" if summary else ""
    return f"- **{_md(_time_range(start, end, clock))}** · {title}{tail}"


# =============================================================================
# Files
# =============================================================================


def _vault(settings: Settings) -> Path:
    """The vault folder as an absolute path.

    ``notes.vault`` may have been written as a relative path; it then means "relative to where vnote was
    started".  Pinning it down here keeps ``note_path`` in the library pointing at the real file.
    """
    return Path(os.path.abspath(settings.vault_dir))


def _fit_bytes(text: str, limit: int) -> str:
    """``text`` cut to at most ``limit`` UTF-8 bytes without splitting a character (file names are limited in
    bytes, and one character of some scripts takes four)."""
    data = text.encode("utf-8", errors="replace")
    if len(data) <= limit:
        return text
    return data[:limit].decode("utf-8", errors="ignore").rstrip() or "Untitled"


def _cannot_write(settings: Settings, vault: Path, exc: OSError) -> NoteRenderError:
    message = (
        f"Could not write notes into {vault}: {exc.strerror or exc}. Check that the folder exists, is writable and "
        f"the disk is not full — or point `vault` in the [notes] section of {settings.config_path} at another folder."
    )
    if exc.errno in (errno.EPERM, errno.EACCES) and is_macos():
        # macOS answers "Operation not permitted" for Documents, Desktop, iCloud Drive … until the terminal is allowed
        message += (
            " On a Mac this is usually a privacy setting: allow the app you run vnote from (Terminal, iTerm …) under "
            "System Settings › Privacy & Security › Files and Folders, then run the command again."
        )
    return NoteRenderError(message)


def _safe_component(name: str) -> str:
    """A session id as a directory name (ids made by videonotes are returned unchanged)."""
    safe = re.sub(r"[^A-Za-z0-9._-]", "_", name)
    return safe if safe.strip(".") else "session"


_URL_SAFE = frozenset("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~")


def _url_component(part: str) -> str:
    """Percent-encode what Markdown link destinations cannot carry; non-ASCII letters stay readable."""
    out: list[str] = []
    for ch in part:
        if ch in _URL_SAFE or ord(ch) > 0x7F and not ch.isspace():
            out.append(ch)
        else:
            out.append("".join(f"%{byte:02X}" for byte in ch.encode("utf-8")))
    return "".join(out)


def _relative_link(target: Path, from_dir: Path) -> str:
    relative = os.path.relpath(target, from_dir)
    return "/".join(part if part == ".." else _url_component(part) for part in Path(relative).parts)


_FM_SESSION_ID = re.compile(r"^session_id:[ \t]*(.*?)[ \t]*$", re.MULTILINE)


def _note_owner(path: Path) -> str | None:
    """The session id recorded in a note's front matter, or None if the file is not one of our notes."""
    try:
        with path.open(encoding="utf-8", errors="replace") as fh:
            head = fh.read(65536).lstrip("\ufeff")  # some editors and sync tools put a byte-order mark in front
    except (OSError, ValueError):
        return None
    if not head.startswith("---"):
        return None
    end = head.find("\n---", 3)
    match = _FM_SESSION_ID.search(head[: end if end != -1 else len(head)])
    if not match:
        return None
    raw = match.group(1)
    if raw.startswith('"'):
        try:
            return str(json.loads(raw))
        except ValueError:
            return raw.strip('"')
    if len(raw) >= 2 and raw.startswith("'") and raw.endswith("'"):
        return raw[1:-1].replace("''", "'")
    return raw or None


def _same_file(a: Path, b: Path) -> bool:
    """True when both paths name the same file (also on case-insensitive volumes)."""
    try:
        return os.path.samefile(a, b)
    except OSError:
        return os.path.abspath(a) == os.path.abspath(b)


def _free_path(directory: Path, stem: str, session_id: str, previous: Path | None) -> Path:
    """Where this session's note goes: ``<stem>.md``, or ``<stem> (2).md`` … if that file is somebody else's."""
    for n in range(1, 10_000):
        candidate = directory / (f"{stem}.md" if n == 1 else f"{stem} ({n}).md")
        if not os.path.lexists(candidate):
            return candidate
        if not candidate.is_file():
            continue
        owner = _note_owner(candidate)
        if owner == session_id:
            return candidate
        # the file the library remembers for this session, with its front matter edited away by hand
        if owner is None and previous is not None and os.path.lexists(previous) and _same_file(candidate, previous):
            return candidate
    raise NoteRenderError(
        f"There are already thousands of notes named {stem!r} in {directory}. "
        "Move or delete some of them and try again."
    )


def _remove_previous(previous: Path, target: Path, session_id: str, vault: Path) -> None:
    """Delete the note a session had before it was renamed (only if it really is that session's note)."""
    try:
        if not previous.is_file() or _same_file(previous, target):
            return
        inside = os.path.commonpath([os.path.abspath(previous), os.path.abspath(vault)]) == os.path.abspath(vault)
        if not inside or _note_owner(previous) != session_id:
            log.info("left %s alone: it is not this session's generated note any more", previous)
            return
        previous.unlink()
        log.info("removed the previous note %s", previous)
    except (OSError, ValueError) as exc:
        log.warning("could not remove the previous note %s: %s", previous, exc)


def _write_atomic(path: Path, text: str) -> bool:
    """Write ``text`` to ``path`` via a temporary file. Returns False when the file already had this content."""
    data = text.encode("utf-8", errors="replace")
    try:
        if path.read_bytes() == data:
            return False
    except OSError:
        pass
    temp = path.with_name(f".vnote-{secrets.token_hex(6)}.tmp")
    try:
        with open(temp, "xb") as fh:
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(temp, path)
    except BaseException:
        with contextlib.suppress(OSError):
            temp.unlink()
        raise
    return True


class _Embedder:
    """Copies the keyframes a note embeds into the vault and forgets the ones it no longer needs."""

    def __init__(self, settings: Settings, assets_dir: Path, *, enabled: bool):
        self._settings = settings
        self._dir = assets_dir
        self._enabled = enabled
        self._used: set[str] = set()
        self.missing = 0

    def _source(self, frame: Keyframe) -> Path:
        return self._settings.abs(frame.path)

    def _name(self, frame: Keyframe) -> str:
        """File name of a frame's copy in the vault."""
        suffix = Path(frame.path).suffix.lower()
        if frame.id is not None:
            return f"kf_{frame.id:06d}{suffix}"
        return f"kf_{hashlib.sha1(frame.path.encode('utf-8', 'replace')).hexdigest()[:12]}{suffix}"

    def available(self, frame: Keyframe) -> bool:
        """Can this frame be embedded (embedding on, an image, and the file — or an earlier copy of it — exists)?"""
        if not self._enabled:
            return False
        ok = Path(frame.path).suffix.lower() in _IMAGE_SUFFIXES and (
            self._source(frame).is_file() or (self._dir / self._name(frame)).is_file()
        )
        if not ok:
            self.missing += 1
            log.debug("keyframe %s not embedded: %s is not an existing image file", frame.id, frame.path)
        return ok

    def embed(self, frame: Keyframe) -> str | None:
        """Copy the frame next to the notes; return the link to use from ``<vault>/sessions/``.

        When the library's own image has gone (the frames folder was deleted to save space, or lives on a disk
        that is not attached) but an earlier render left its copy in the vault, that copy stays in the note:
        it is the only one left, and dropping the link would have it pruned.
        """
        name = self._name(frame)
        source, copy = self._source(frame), self._dir / name
        try:
            if source.is_file() or not copy.is_file():
                self._dir.mkdir(parents=True, exist_ok=True)
                _copy_if_changed(source, copy)
            else:
                log.debug("keyframe %s: %s is gone; keeping the copy already in the vault", frame.id, frame.path)
        except OSError as exc:
            self.missing += 1
            log.warning("keyframe %s not embedded: copying %s failed (%s)", frame.id, frame.path, exc)
            return None
        self._used.add(name)
        return f"../assets/{_url_component(self._dir.name)}/{_url_component(name)}"

    def prune(self) -> None:
        """Remove this session's copied frames that the note no longer shows (never anything else)."""
        try:
            entries = list(self._dir.iterdir())
        except OSError:
            return
        for entry in entries:
            stale_copy = _ASSET_NAME.fullmatch(entry.name) and entry.name not in self._used
            if (stale_copy or _TEMP_NAME.fullmatch(entry.name)) and entry.is_file() and not entry.is_symlink():
                with contextlib.suppress(OSError):
                    entry.unlink()
        with contextlib.suppress(OSError):
            self._dir.rmdir()  # only succeeds when nothing is left


def _copy_if_changed(source: Path, destination: Path) -> None:
    """Copy (never move) ``source`` unless an identical-looking copy is already there."""
    src = source.stat()
    try:
        dst = destination.stat()
        if dst.st_size == src.st_size and abs(dst.st_mtime - src.st_mtime) < 2.0:
            return
    except OSError:
        pass
    temp = destination.with_name(f".vnote-{secrets.token_hex(6)}.tmp")
    try:
        shutil.copyfile(source, temp)
        with contextlib.suppress(OSError):
            os.utime(temp, ns=(src.st_atime_ns, src.st_mtime_ns))  # lets the next render see it is up to date
        os.replace(temp, destination)
    except BaseException:
        with contextlib.suppress(OSError):
            temp.unlink()
        raise
