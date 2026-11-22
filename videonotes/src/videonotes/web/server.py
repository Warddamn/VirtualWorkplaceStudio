"""The local web UI behind ``vnote web``: browse days, sessions and moments, search, ask.

Standard library only (``http.server``), no web framework and no build step.
The server exposes the library read-only as JSON, serves keyframe JPEGs and
clip media (with HTTP Range, so a ``<video>`` element can seek to a moment)
and hosts the single-page app in ``web/static``.

It serves a person's private footage, so it is deliberately strict:

* it only ever listens on a loopback address;
* a request must be addressed to a loopback name on the server's own port
  (``Host`` check: protection against DNS rebinding), cross-site requests are
  refused (``Sec-Fetch-Site`` / ``Origin``), and ``POST`` needs a JSON body;
* files are only served when the library references them *and* they resolve
  inside the library's ``frames`` / ``media`` directory (symlinks included);
* every response carries ``nosniff``, a self-only Content-Security-Policy and
  ``Cross-Origin-Resource-Policy: same-origin``;
* error responses never contain exception text or file-system paths.

Public API: :func:`make_server` and :func:`serve`.
"""

from __future__ import annotations

import errno
import hashlib
import ipaddress
import json
import logging
import math
import os
import re
import socket
import socketserver
import sqlite3
import stat
import sys
import threading
import time
import unicodedata
from collections.abc import Iterable, Mapping
from datetime import date, datetime
from email.utils import formatdate
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, quote, unquote

from .. import __version__
from .. import search as search_mod
from ..backends.base import BackendError, BackendUnavailable
from ..config import Settings
from ..models import ActionItem, Clip, DayDigest, Keyframe, Moment, Session, SessionNote, Utterance
from ..store import SEARCH_KINDS, Store
from ..timeutil import day_bounds, fmt_duration, local_dt

log = logging.getLogger("videonotes.web")

DEFAULT_PORT = 8765
#: Largest accepted POST body. A question is a sentence, not a document.
MAX_POST_BYTES = 64 * 1024
MAX_QUESTION_CHARS = 2000
MAX_QUERY_CHARS = 500
SEARCH_LIMIT_DEFAULT = 40
SEARCH_LIMIT_MAX = 100
SESSIONS_LIMIT_DEFAULT = 50
SESSIONS_LIMIT_MAX = 500
#: Seconds a connection may sit idle (or a client may stall mid-request) before it is dropped.
REQUEST_TIMEOUT_S = 30.0
_CHUNK_BYTES = 256 * 1024

CONTENT_SECURITY_POLICY = (
    "default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self'; media-src 'self'; "
    "connect-src 'self'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'"
)

_SECURITY_HEADERS = (
    ("X-Content-Type-Options", "nosniff"),
    ("Content-Security-Policy", CONTENT_SECURITY_POLICY),
    ("Referrer-Policy", "no-referrer"),
    ("Cross-Origin-Resource-Policy", "same-origin"),
    ("Cross-Origin-Opener-Policy", "same-origin"),
    ("X-Frame-Options", "DENY"),
)

_STATIC_DIR = Path(__file__).resolve().parent / "static"
#: The only files served from ``web/static`` (no directory listing, no other names).
_STATIC_FILES = {
    "index.html": "text/html; charset=utf-8",
    "app.js": "text/javascript; charset=utf-8",
    "style.css": "text/css; charset=utf-8",
}

_FAVICON_SVG = (
    b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
    b'<rect width="32" height="32" rx="7" fill="#1f6f8b"/>'
    b'<rect x="7" y="9" width="18" height="3" rx="1.5" fill="#fff"/>'
    b'<rect x="7" y="14.5" width="18" height="3" rx="1.5" fill="#fff" opacity=".8"/>'
    b'<rect x="7" y="20" width="11" height="3" rx="1.5" fill="#fff" opacity=".6"/>'
    b"</svg>"
)

_IMAGE_TYPES = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}
_MEDIA_TYPES = {
    ".mp4": "video/mp4",
    ".m4v": "video/mp4",
    ".lrf": "video/mp4",  # DJI low-resolution proxy: an ordinary H.264 MP4 under another name
    ".mov": "video/quicktime",
    ".mkv": "video/x-matroska",
    ".webm": "video/webm",
    ".ts": "video/mp2t",
    ".m4a": "audio/mp4",
    ".aac": "audio/aac",
    ".mp3": "audio/mpeg",
    ".wav": "audio/wav",
    ".flac": "audio/flac",
    ".ogg": "audio/ogg",
    ".opus": "audio/ogg",
}

_LOOPBACK_HOSTS = frozenset({"localhost", "127.0.0.1", "[::1]"})
_DAY_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_ID_RE = re.compile(r"^[0-9]{1,18}$")


class WebServerError(RuntimeError):
    """The web UI could not be started. ``hint`` says what to try instead."""

    def __init__(self, message: str, *, hint: str = ""):
        super().__init__(message)
        self.hint = hint


class HttpError(Exception):
    """An error to report to the client as ``{"error": {"code", "message"}}``."""

    def __init__(self, status: int, code: str, message: str, *, headers: Mapping[str, str] | None = None):
        super().__init__(message)
        self.status = status
        self.code = code
        self.message = message
        self.headers = dict(headers or {})


class RangeNotSatisfiable(Exception):
    """The requested byte range lies outside the file."""


# --------------------------------------------------------------------------
# Pure helpers (unit-tested directly)
# --------------------------------------------------------------------------


def parse_host(value: str) -> tuple[str, int | None] | None:
    """Split a ``Host`` header into ``(lower-case host, port or None)``; None if malformed."""
    value = value.strip().lower()
    if not value or any(ch in value for ch in " \t\r\n/\\@?#,"):
        return None
    if value.startswith("["):
        end = value.find("]")
        if end < 0:
            return None
        host, rest = value[: end + 1], value[end + 1 :]
    else:
        host, sep, port_text = value.partition(":")
        rest = sep + port_text
    if not rest:
        return host, None
    digits = rest[1:]
    if not rest.startswith(":") or not digits.isascii() or not digits.isdigit() or len(digits) > 5:
        return None
    port = int(digits)
    return (host, port) if port <= 65535 else None


def host_allowed(value: str | None, port: int) -> bool:
    """True when a ``Host`` header names this machine's loopback interface and our port."""
    parsed = parse_host(value or "")
    if parsed is None:
        return False
    host, host_port = parsed
    if not host.startswith("["):
        host = host.rstrip(".")
    return host in _LOOPBACK_HOSTS and (host_port if host_port is not None else 80) == port


def origin_allowed(value: str | None, port: int) -> bool:
    """True when an ``Origin`` header is this server itself (``http://<loopback>:<port>``)."""
    value = (value or "").strip().lower()
    if not value.startswith("http://"):
        return False
    return host_allowed(value[len("http://") :], port)


def split_path(raw: str) -> list[str] | None:
    """Decode a request path into its segments, or None when it must be refused.

    Each segment is percent-decoded exactly once.  Empty segments, ``.``, ``..``,
    encoded slashes, backslashes and control characters are refused outright, so
    nothing that reaches a file lookup can step out of its directory.
    """
    if not raw.startswith("/"):
        return None
    if raw == "/":
        return []
    segments: list[str] = []
    for part in raw.split("/")[1:]:
        try:
            segment = unquote(part, errors="strict")
        except UnicodeDecodeError:
            return None
        if segment in ("", ".", "..") or "/" in segment or "\\" in segment:
            return None
        if any(ord(ch) < 32 or ord(ch) == 127 for ch in segment):
            return None
        segments.append(segment)
    return segments


_RANGE_RE = re.compile(r"^bytes=(\d{0,19})-(\d{0,19})$")


def parse_range(header: str | None, size: int) -> tuple[int, int] | None:
    """Parse a single-range ``Range`` header into inclusive ``(start, end)`` byte offsets.

    Returns None when there is no usable range (absent, malformed, or several
    ranges: the whole file is sent then, which HTTP allows).  Raises
    :class:`RangeNotSatisfiable` when the range starts beyond the end of the file.
    """
    if not header:
        return None
    match = _RANGE_RE.match("".join(header.split()))
    if not match:
        return None
    first, last = match.groups()
    if not first and not last:
        return None
    if not first:  # "bytes=-N": the final N bytes
        length = int(last)
        if length == 0 or size == 0:
            raise RangeNotSatisfiable
        return max(0, size - length), size - 1
    start = int(first)
    if start >= size:
        raise RangeNotSatisfiable
    end = min(int(last), size - 1) if last else size - 1
    if end < start:
        return None
    return start, end


def etag_matches(header: str | None, etag: str) -> bool:
    """``If-None-Match`` comparison (weak comparison, ``*`` matches anything)."""
    if not header:
        return False
    for candidate in header.split(","):
        candidate = candidate.strip()
        if candidate == "*" or candidate.removeprefix("W/") == etag:
            return True
    return False


def _fold(text: str) -> str:
    """Lower-case and strip diacritics, the way the search index compares words."""
    decomposed = unicodedata.normalize("NFKD", text.lower())
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch))


def query_words(query: str) -> list[str]:
    """The words of a search query, folded for comparison with snippet tokens."""
    words = [_fold(w.strip("'")) for w in re.findall(r"[\w']+", query, flags=re.UNICODE)]
    return [w for w in words if w]


def _plausible_match(token: str, words: list[str]) -> bool:
    token = _fold(token)
    for word in words:
        shared = 0
        for a, b in zip(token, word, strict=False):
            if a != b:
                break
            shared += 1
        shortest = min(len(token), len(word))
        # the index stems words and matches prefixes, so "decided" finds "deciding": allow a suffix to differ
        if shared >= min(3, shortest) and shared >= shortest - 3:
            return True
    return False


_MARK_RE = re.compile(r"\[(\w+)\]", re.UNICODE)


def split_snippet(snippet: str, words: list[str]) -> list[dict[str, Any]]:
    """Turn a search snippet with ``[match]`` markers into ``[{"text", "match"}]`` parts.

    The store marks matched words with square brackets, which may also occur in
    the indexed text itself (``array[0]``).  A bracketed word only counts as a
    match when it plausibly matches one of the query words; anything else is
    kept verbatim, so the page never drops or re-styles what was really there.
    """
    parts: list[dict[str, Any]] = []

    def add(text: str, match: bool) -> None:
        if not text:
            return
        if parts and parts[-1]["match"] == match:
            parts[-1]["text"] += text
        else:
            parts.append({"text": text, "match": match})

    pos = 0
    for found in _MARK_RE.finditer(snippet):
        if not _plausible_match(found.group(1), words):
            continue
        add(snippet[pos : found.start()], False)
        add(found.group(1), True)
        pos = found.end()
    add(snippet[pos:], False)
    for part in parts:
        part["text"] = re.sub(r"\s+", " ", part["text"])
    return parts


def one_line(text: str | None, limit: int = 200) -> str:
    """Collapse whitespace and shorten to about ``limit`` characters at a sentence or word boundary."""
    flat = " ".join((text or "").split())
    if len(flat) <= limit:
        return flat
    head = flat[:limit]
    stop = max(head.rfind(". "), head.rfind("! "), head.rfind("? "))
    if stop >= limit // 3:
        return head[: stop + 1]
    cut = head.rfind(" ")
    return (head[:cut] if cut >= limit // 2 else head).rstrip(" ,;:") + "…"


def excerpt(text: str | None, limit: int = 700) -> str:
    """Trim long evidence text, keeping line breaks."""
    cleaned = "\n".join(" ".join(row.split()) for row in (text or "").strip().splitlines())
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[:limit].rstrip() + "…"


_PATH_RE = re.compile(r"(?<![\w:/.~-])~?/(?:[^\s/'\"`<>]+/)+[^\s'\"`<>]*")


def public_error_text(exc: BaseException, limit: int = 400) -> str:
    """Text of a backend error that is safe to show in the page: file-system paths are removed."""
    text = " ".join(str(exc).split())
    text = _PATH_RE.sub("a file on this Mac", text)
    return text[:limit].rstrip()


def _number(value: Any) -> float | None:
    """A finite float, or None for anything else (the note JSON is written by an LLM)."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    number = float(value)
    return number if math.isfinite(number) else None


def _public_source(source: str) -> str:
    """Session source for display: a device description as is, a path reduced to its last name."""
    source = " ".join((source or "").split())
    if source.startswith(("/", "~")) or re.match(r"^[A-Za-z]:[\\/]", source):
        return Path(source.replace("\\", "/")).name
    return source[:120]


def _finite(value: Any) -> Any:
    """Copy of a JSON-ready structure with NaN / infinity replaced by None."""
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    if isinstance(value, dict):
        return {key: _finite(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_finite(item) for item in value]
    return value


def json_bytes(payload: Any) -> bytes:
    """Serialise to strict JSON (ASCII-only, so odd characters from OCR can never break the encoding)."""
    try:
        text = json.dumps(payload, allow_nan=False, separators=(",", ":"))
    except ValueError:  # a NaN or infinity slipped into the library (e.g. an unknown duration)
        text = json.dumps(_finite(payload), allow_nan=False, separators=(",", ":"))
    return text.encode("ascii")


def _printable(text: str, limit: int = 200) -> str:
    """Make untrusted text safe for a log line (no control characters, bounded length)."""
    return "".join(ch if ch.isprintable() else "?" for ch in text[:limit])


# --------------------------------------------------------------------------
# The library as JSON
# --------------------------------------------------------------------------


class _Lookup:
    """Per-request memo of sessions and moments, so resolving many hits stays cheap."""

    def __init__(self, store: Store):
        self._store = store
        self._sessions: dict[str, Session | None] = {}
        self._moments: dict[str, list[Moment]] = {}

    def session(self, session_id: str) -> Session | None:
        if session_id not in self._sessions:
            self._sessions[session_id] = self._store.get_session(session_id)
        return self._sessions[session_id]

    def moments(self, session_id: str) -> list[Moment]:
        if session_id not in self._moments:
            self._moments[session_id] = self._store.list_moments(session_id)
        return self._moments[session_id]

    def moment_at(self, session_id: str, ts: float | None, *, keyframe_id: int | None = None) -> Moment | None:
        moments = self.moments(session_id)
        if keyframe_id is not None:
            for m in moments:
                if keyframe_id in m.keyframe_ids:
                    return m
        if ts is None:
            return None
        for m in moments:
            if m.ts0 <= ts < m.ts1:
                return m
        for m in moments:
            if m.ts0 - 1 <= ts <= m.ts1 + 1:
                return m
        return None


class Library:
    """Read-only JSON view of a videonotes library, plus the files the page may fetch."""

    def __init__(self, settings: Settings, store: Store):
        self.settings = settings
        self.store = store
        self._clock_format = settings.notes.time_format or "%H:%M"
        self._roots: dict[Path, tuple[float, Path]] = {}

    # -- formatting -------------------------------------------------------

    def _clock(self, dt: datetime) -> str:
        try:
            return dt.strftime(self._clock_format)
        except ValueError:
            return dt.strftime("%H:%M")

    def when(self, ts: Any) -> dict[str, Any] | None:
        """A time as epoch seconds plus local strings ready for display."""
        number = _number(ts)
        if number is None:
            return None
        try:
            dt = local_dt(number)
        except (OverflowError, OSError, ValueError):
            return None
        clock = self._clock(dt)
        return {
            "ts": number,
            "clock": clock,
            "precise": f"{dt:%H:%M:%S}",
            "day": f"{dt:%Y-%m-%d}",
            "text": f"{dt:%a} {dt.day} {dt:%b %Y}, {clock}",
        }

    @staticmethod
    def day_labels(day: str, today: date | None = None) -> dict[str, Any]:
        d = date.fromisoformat(day)
        today = today or datetime.now().date()
        delta = (today - d).days
        relative = "Today" if delta == 0 else "Yesterday" if delta == 1 else ""
        return {
            "date": day,
            "label": f"{d:%A} {d.day} {d:%B %Y}",
            "short": f"{d:%a} {d.day} {d:%b}",
            "month": f"{d:%B %Y}",
            "relative": relative,
        }

    # -- files ------------------------------------------------------------

    def _lexical_rel(self, stored: str, root: Path) -> str | None:
        """``stored`` (a database path) relative to ``root`` without touching the disk, or None."""
        target = Path(os.path.normpath(self.settings.abs(stored)))
        try:
            rel = target.relative_to(Path(os.path.normpath(root)))
        except ValueError:
            return None
        text = rel.as_posix()
        return text if text not in ("", ".") else None

    def frame_url(self, kf: Keyframe) -> str | None:
        """URL of a keyframe image, or None when its file is not in the library's frames folder."""
        if kf.id is None or not kf.path:
            return None
        rel = self._lexical_rel(kf.path, self.settings.frames_dir)
        if rel is None or Path(rel).suffix.lower() not in _IMAGE_TYPES:
            return None
        real = self._inside(self.settings.frames_dir / rel, self.settings.frames_dir)
        if real is None or not real.is_file():
            return None  # missing, or a link that leads out of the frames folder
        return f"/frames/{quote(rel)}?k={kf.id}"

    def frame_alt(self, kf: Keyframe) -> str:
        clock = (self.when(kf.ts) or {}).get("clock", "")
        if kf.caption and kf.caption.strip():
            return one_line(kf.caption, 160)
        if kf.ocr_text and kf.ocr_text.strip():
            return f"Frame at {clock} showing the text: {one_line(kf.ocr_text, 100)}"
        return f"Frame at {clock}" if clock else "Keyframe"

    def _thumb(self, kf: Keyframe | None) -> dict[str, Any] | None:
        if kf is None:
            return None
        url = self.frame_url(kf)
        return {"url": url, "alt": self.frame_alt(kf), "keyframe_id": kf.id} if url else None

    def _real_root(self, root: Path) -> Path:
        """``root`` with symlinks resolved; remembered for a second (many frames are checked per request)."""
        now = time.monotonic()
        cached = self._roots.get(root)
        if cached is None or now - cached[0] > 1.0:
            cached = (now, root.resolve())
            self._roots[root] = cached
        return cached[1]

    def _inside(self, path: Path, root: Path) -> Path | None:
        """``path`` fully resolved (symlinks followed) if it exists inside ``root``, else None."""
        try:
            real = path.resolve(strict=True)
            real.relative_to(self._real_root(root))
        except (OSError, RuntimeError, ValueError):
            return None
        return real

    def frame_file(self, rel: str, key: str | None) -> tuple[Path, str]:
        """Resolve ``/frames/<rel>`` to ``(real path, content type)`` or raise a 404 :class:`HttpError`.

        The file must be a keyframe the library knows (``key`` is the keyframe id
        the API put in the URL; without it the session folder is searched) and
        must really live inside the frames directory once symlinks are resolved.
        """
        missing = HttpError(404, "not_found", "That image is not in the library.")
        content_type = _IMAGE_TYPES.get(Path(rel).suffix.lower())
        if content_type is None or not self._frame_referenced(rel, key):
            raise missing
        real = self._inside(self.settings.frames_dir / rel, self.settings.frames_dir)
        if real is None:
            raise missing
        return real, content_type

    def _frame_referenced(self, rel: str, key: str | None) -> bool:
        frames_dir = self.settings.frames_dir
        if key is not None and _ID_RE.match(key):
            kf = self.store.get_keyframe(int(key))
            if kf is not None and self._lexical_rel(kf.path, frames_dir) == rel:
                return True
        session_id = rel.split("/", 1)[0]
        if self.store.get_session(session_id) is None:
            return False
        return any(
            self._lexical_rel(kf.path, frames_dir) == rel for kf in self.store.list_keyframes(session_id=session_id)
        )

    def _clip_media(self, clip: Clip) -> Path | None:
        """The clip's playable file if it is still inside the library's media folder."""
        for stored in (clip.path, clip.original_path):
            if not stored:
                continue
            real = self._inside(self.settings.abs(stored), self.settings.media_dir)
            if real is not None and real.is_file():
                return real
        return None

    def media_file(self, clip_ref: str) -> tuple[Path, str]:
        """Resolve ``/media/<clip_id>`` to ``(real path, content type)`` or raise a 404 :class:`HttpError`."""
        if not _ID_RE.match(clip_ref):
            raise HttpError(404, "unknown_clip", "That clip is not in the library.")
        clip = self.store.get_clip(int(clip_ref))
        if clip is None:
            raise HttpError(404, "unknown_clip", "That clip is not in the library.")
        real = self._clip_media(clip)
        if real is None:
            raise HttpError(404, "media_unavailable", "The video for that clip is no longer kept in the library.")
        return real, _MEDIA_TYPES.get(real.suffix.lower(), "application/octet-stream")

    # -- sessions ---------------------------------------------------------

    def _session_thumbnail(self, session_id: str) -> dict[str, Any] | None:
        moments = self.store.list_moments(session_id)
        for salience in ("highlight", "normal", "background"):
            for m in moments:
                if (m.salience or "normal") != salience:
                    continue
                first: dict[str, Any] | None = None
                for kid in m.keyframe_ids[:8]:
                    kf = self.store.get_keyframe(kid) if isinstance(kid, int) else None
                    thumb = self._thumb(kf)
                    if thumb is None or kf is None:
                        continue
                    if kf.ocr_text or kf.caption:
                        return thumb
                    first = first or thumb
                if first:
                    return first
        for kf in self.store.list_keyframes(session_id=session_id):
            thumb = self._thumb(kf)
            if thumb:
                return thumb
        return None

    def session_brief(self, s: Session, *, thumbnail: bool = True) -> dict[str, Any]:
        note = s.note
        title = one_line((note.title if note and note.title else s.title) or "", 200)
        ended = _number(s.ended_ts)
        if ended is None:
            bounds = self.store.session_bounds(s.id)
            ended = bounds[1] if bounds else None
        duration = max(0.0, ended - s.started_ts) if ended is not None else None
        start = self.when(s.started_ts)
        return {
            "id": s.id,
            "title": title or "Untitled session",
            "untitled": not title,
            "kind": s.kind,
            "status": s.status,
            "source": _public_source(s.source),
            "day": start["day"] if start else "",
            "start": start,
            "end": self.when(ended),
            "duration_s": duration,
            "duration": fmt_duration(duration) if duration is not None else "",
            "summary": one_line(note.summary, 220) if note else "",
            "has_note": note is not None,
            "llm_backend": note.llm_backend if note else "",
            "thumbnail": self._session_thumbnail(s.id) if thumbnail else None,
        }

    def overview(self) -> dict[str, Any]:
        stats = self.store.stats()
        sessions = self.store.list_sessions()  # newest first
        counts: dict[str, int] = {}
        for s in sessions:
            start = self.when(s.started_ts)
            if start:
                counts[start["day"]] = counts.get(start["day"], 0) + 1
        today = datetime.now().date()
        days = []
        for day in sorted(counts, reverse=True):
            digest = self._stored_digest(day)
            days.append(
                {
                    **self.day_labels(day, today),
                    "sessions": counts[day],
                    "has_digest": digest is not None,
                    "headline": one_line(digest.headline, 120) if digest else "",
                }
            )
        media_seconds = _number(stats.get("media_seconds")) or 0.0
        return {
            "version": __version__,
            "library": {**stats, "media_seconds": media_seconds, "media_duration": fmt_duration(media_seconds)},
            "days": days,
            "latest_session_id": sessions[0].id if sessions else None,
        }

    def sessions(self, day: str | None, limit: int) -> dict[str, Any]:
        if day is None:
            found = self.store.list_sessions(limit=limit)
            return {"day": None, "sessions": [self.session_brief(s) for s in found]}
        since, until = day_bounds(day)
        found = sorted(self.store.list_sessions(since_ts=since, until_ts=until), key=lambda s: s.started_ts)
        return {"day": self.day_labels(day), "sessions": [self.session_brief(s) for s in found[:limit]]}

    def _action_items(self, items: Iterable[ActionItem], span: tuple[float, float] | None) -> list[dict[str, Any]]:
        out = []
        for item in items:
            ts = _number(item.ts)
            if ts is not None and span is not None and not (span[0] - 60 <= ts <= span[1] + 60):
                ts = None  # an offset or a made-up time, not a moment of this recording
            out.append({"text": item.text, "owner": item.owner, "due": item.due, "time": self.when(ts)})
        return out

    def _note(self, note: SessionNote, span: tuple[float, float] | None) -> dict[str, Any]:
        return {
            "title": note.title,
            "summary": note.summary,
            "key_points": note.key_points,
            "action_items": self._action_items(note.action_items, span),
            "decisions": note.decisions,
            "open_questions": note.open_questions,
            "people": note.people,
            "places": note.places,
            "captured_text": note.captured_text,
            "tags": note.tags,
            "llm_backend": note.llm_backend,
        }

    def _keyframe(self, kf: Keyframe) -> dict[str, Any]:
        return {
            "id": kf.id,
            "url": self.frame_url(kf),
            "alt": self.frame_alt(kf),
            "time": self.when(kf.ts),
            "caption": (kf.caption or "").strip(),
            "ocr_text": (kf.ocr_text or "").strip(),
            "clip_id": kf.clip_id,
            "t": kf.t,
        }

    def _utterance(self, u: Utterance) -> dict[str, Any]:
        return {
            "id": u.id,
            "time": self.when(u.ts0),
            "text": u.text.strip(),
            "speaker": u.speaker or "",
            "clip_id": u.clip_id,
            "t": u.t0,
        }

    @staticmethod
    def _locate(clips: list[Clip], ts0: float, ts1: float) -> tuple[Clip, float] | None:
        """The clip (and offset into it) where a span starts; clips are in start order."""
        for clip in clips:
            if clip.start_ts <= ts0 < clip.start_ts + max(clip.duration, 0.0):
                return clip, ts0 - clip.start_ts
            if ts0 <= clip.start_ts <= ts1:
                return clip, 0.0
        return None

    def session(self, session_id: str) -> dict[str, Any]:
        s = self.store.get_session(session_id)
        if s is None:
            raise HttpError(404, "unknown_session", "That session is not in the library. It may have been deleted.")
        clips = self.store.list_clips(s.id)
        keyframes = self.store.list_keyframes(session_id=s.id)
        utterances = self.store.list_utterances(session_id=s.id)
        moments = self.store.list_moments(s.id)

        playable: set[int] = set()
        clips_json = []
        for clip in clips:
            media = self._clip_media(clip)
            if media is not None and clip.id is not None:
                playable.add(clip.id)
            clips_json.append(
                {
                    "id": clip.id,
                    "start": self.when(clip.start_ts),
                    "duration_s": clip.duration,
                    "duration": fmt_duration(clip.duration),
                    "url": f"/media/{clip.id}" if media is not None else None,
                    "content_type": _MEDIA_TYPES.get(media.suffix.lower(), "") if media is not None else "",
                    "has_video": clip.has_video,
                    "has_audio": clip.has_audio,
                }
            )

        kf_by_id = {kf.id: kf for kf in keyframes}
        ut_by_id = {u.id: u for u in utterances}
        used_kf: set[int | None] = set()
        used_ut: set[int | None] = set()
        moments_json = []
        for m in moments:
            frames = list(dict.fromkeys(i for i in m.keyframe_ids if i in kf_by_id))
            mine_kf = [kf_by_id[i] for i in frames]
            if not mine_kf:  # ids missing or stale: fall back to what lies inside the moment's time span
                mine_kf = [kf for kf in keyframes if kf.id not in used_kf and m.ts0 <= kf.ts <= m.ts1]
            lines = list(dict.fromkeys(i for i in m.utterance_ids if i in ut_by_id))
            mine_ut = [ut_by_id[i] for i in lines]
            if not mine_ut:
                mine_ut = [u for u in utterances if u.id not in used_ut and m.ts0 <= u.ts0 <= m.ts1]
            mine_kf.sort(key=lambda kf: (kf.ts, kf.id or 0))
            mine_ut.sort(key=lambda u: (u.ts0, u.id or 0))
            used_kf.update(kf.id for kf in mine_kf)
            used_ut.update(u.id for u in mine_ut)
            where = self._locate(clips, m.ts0, m.ts1)
            play = None
            if where is not None and where[0].id in playable:
                play = {"clip_id": where[0].id, "t": round(max(0.0, where[1]), 2)}
            moments_json.append(
                {
                    "id": m.id,
                    "idx": m.idx,
                    "title": one_line(m.title, 200),
                    "summary": m.summary.strip(),
                    "tags": [str(t) for t in m.tags if str(t).strip()],
                    "kind": m.kind or "",
                    "salience": m.salience or "normal",
                    "start": self.when(m.ts0),
                    "end": self.when(m.ts1),
                    "duration": fmt_duration(max(0.0, m.ts1 - m.ts0)),
                    "keyframes": [self._keyframe(kf) for kf in mine_kf],
                    "transcript": [self._utterance(u) for u in mine_ut],
                    "play": play,
                }
            )

        brief = self.session_brief(s)
        span = None
        if brief["start"] and brief["end"]:
            span = (brief["start"]["ts"], brief["end"]["ts"])
        note_path = s.note_path if s.note_path and not Path(s.note_path).expanduser().is_absolute() else None
        errors = sorted({stage for clip in clips for stage, info in clip.stages.items() if _is_error(info)})
        return {
            "session": {**brief, "note_path": note_path, "failed_stages": errors},
            "note": self._note(s.note, span) if s.note else None,
            "moments": moments_json,
            "unassigned": {
                "keyframes": [self._keyframe(kf) for kf in keyframes if kf.id not in used_kf],
                "transcript": [self._utterance(u) for u in utterances if u.id not in used_ut],
            },
            "clips": clips_json,
            "playable": bool(playable),
        }

    # -- days -------------------------------------------------------------

    def _stored_digest(self, day: str) -> DayDigest | None:
        """The saved digest of a day; a damaged one is treated as missing rather than breaking the page."""
        try:
            return self.store.get_day(day)
        except (ValueError, TypeError, AttributeError, KeyError):
            log.warning("the stored summary of %s is unreadable; run `vnote day %s` to rebuild it", day, day)
            return None

    def _digest(self, digest: DayDigest, day: str) -> dict[str, Any]:
        return {
            "date": day,
            "headline": digest.headline,
            "summary": digest.summary,
            "highlights": digest.highlights,
            "action_items": self._action_items(digest.action_items, day_bounds(day)),
            "session_ids": digest.session_ids,
            "llm_backend": digest.llm_backend,
        }

    def day(self, day: str) -> dict[str, Any]:
        since, until = day_bounds(day)
        sessions = sorted(self.store.list_sessions(since_ts=since, until_ts=until), key=lambda s: s.started_ts)
        digest = self._stored_digest(day)
        return {
            "day": self.day_labels(day),
            "digest": self._digest(digest, day) if digest else None,
            "sessions": [self.session_brief(s) for s in sessions],
        }

    # -- search and ask -----------------------------------------------------

    def _target(
        self, look: _Lookup, kind: str, ref_id: str, session_id: str, ts: float | None
    ) -> dict[str, Any] | None:
        """Where a search hit or a piece of evidence lives, so the page can jump to it."""
        session = look.session(session_id)
        if session is None:
            return None
        ref = int(ref_id) if _ID_RE.match(ref_id or "") else None
        moment: Moment | None = None
        keyframe: Keyframe | None = None
        utterance_id: int | None = None
        thumb: dict[str, Any] | None = None
        if kind in ("ocr", "caption") and ref is not None:
            keyframe = self.store.get_keyframe(ref)
            moment = look.moment_at(session_id, ts, keyframe_id=ref)
            thumb = self._thumb(keyframe)
        elif kind == "utterance":
            utterance_id = ref
            moment = look.moment_at(session_id, ts)
            if ts is not None:
                near = self.store.list_keyframes(session_id=session_id, ts0=ts - 90, ts1=ts + 90)
                for kf in sorted(near, key=lambda kf: abs(kf.ts - ts)):
                    thumb = self._thumb(kf)
                    if thumb:
                        break
        elif kind == "moment" and ref is not None:
            moment = next((m for m in look.moments(session_id) if m.id == ref), None)
            for kid in (moment.keyframe_ids[:4] if moment else []):
                thumb = self._thumb(self.store.get_keyframe(kid)) if isinstance(kid, int) else None
                if thumb:
                    break
        if thumb is None and kind in ("session", "moment"):
            thumb = self._session_thumbnail(session_id)
        note = session.note
        title = one_line((note.title if note and note.title else session.title) or "", 200)
        return {
            "session_id": session.id,
            "session_title": title or "Untitled session",
            "moment_id": moment.id if moment else None,
            "moment_title": one_line(moment.title, 200) if moment else "",
            "keyframe_id": keyframe.id if keyframe and kind in ("ocr", "caption") else None,
            "utterance_id": utterance_id,
            "thumbnail": thumb,
        }

    def search(self, query: str, *, day: str | None, kinds: list[str], limit: int) -> dict[str, Any]:
        """Search hits in rank order, with repeats of the same on-screen text folded together.

        A sign or whiteboard is usually caught by several keyframes in a row; those
        would otherwise fill the page with identical results.  Frames of one moment
        that carry the same text become one hit with a ``similar`` count.
        """
        fetch = min(limit * 4, 400)
        hits = search_mod.search(self.store, query, limit=fetch, kinds=kinds or None, day=day) if query else []
        look = _Lookup(self.store)
        words = query_words(query)
        out: list[dict[str, Any]] = []
        folded: dict[tuple[Any, ...], dict[str, Any]] = {}
        truncated = len(hits) >= fetch
        for hit in hits:
            key: tuple[Any, ...] | None = None
            if hit.kind in ("ocr", "caption"):
                ref = int(hit.ref_id) if _ID_RE.match(hit.ref_id or "") else None
                moment = look.moment_at(hit.session_id, hit.ts, keyframe_id=ref)
                key = (hit.kind, hit.session_id, moment.id if moment else None, " ".join(hit.text.split()).casefold())
                if key in folded:
                    folded[key]["similar"] += 1
                    continue
            if len(out) >= limit:
                truncated = True
                break
            target = self._target(look, hit.kind, hit.ref_id, hit.session_id, hit.ts)
            if target is None:
                continue  # an index row whose session is gone
            item = {
                "kind": hit.kind,
                "ref_id": hit.ref_id,
                "time": self.when(hit.ts),
                "snippet": hit.snippet,
                "parts": split_snippet(hit.snippet, words),
                "score": round(hit.score, 4),
                "similar": 0,
                **target,
            }
            if key is not None:
                folded[key] = item
            out.append(item)
        return {
            "query": query,
            "day": self.day_labels(day) if day else None,
            "kinds": kinds,
            "count": len(out),
            "truncated": truncated,
            "hits": out,
        }

    def ask(self, question: str) -> dict[str, Any]:
        answer = search_mod.ask(self.settings, self.store, question)
        look = _Lookup(self.store)
        sources: list[dict[str, Any]] = []
        folded: dict[tuple[Any, ...], dict[str, Any]] = {}
        for item in list(answer.sources)[:120]:
            # the same sign or whiteboard read off several frames of one session is one piece of evidence
            key = (item.kind, item.session_id, " ".join(str(item.text).split()).casefold())
            if item.kind in ("ocr", "caption") and key in folded:
                folded[key]["similar"] += 1
                continue
            target = self._target(look, item.kind, item.ref_id, item.session_id, _number(item.ts))
            if target is None:
                continue
            source = {"kind": item.kind, "time": self.when(item.ts), "text": excerpt(item.text), "similar": 0, **target}
            folded.setdefault(key, source)
            sources.append(source)
        backend = str(answer.llm_backend or "")
        return {
            "question": question,
            "answer": str(answer.text or "").strip(),
            "llm_backend": backend,
            "extractive": backend == "extractive",
            "sources": sources,
        }


def _is_error(info: Any) -> bool:
    return isinstance(info, dict) and info.get("status") == "error"


# --------------------------------------------------------------------------
# HTTP
# --------------------------------------------------------------------------


class VideoNotesServer(ThreadingHTTPServer):
    """A loopback-only HTTP server bound to one library. Each request runs in its own thread."""

    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, settings: Settings, address: tuple[str, int], family: socket.AddressFamily):
        self.address_family = family
        self.settings = settings
        self.store: Store | None = None
        self.library: Library | None = None
        #: one question at a time: a local LLM cannot usefully answer two at once on a laptop
        self.ask_lock = threading.Lock()
        self._warn_lock = threading.Lock()
        self._warned: dict[str, float] = {}
        super().__init__(address, _Handler)

    def server_bind(self) -> None:
        # HTTPServer.server_bind() calls socket.getfqdn(), a reverse DNS lookup that can stall
        # for seconds on some Macs. Nothing here needs the machine's fully-qualified name.
        socketserver.TCPServer.server_bind(self)
        host, port = self.server_address[:2]
        self.server_name = str(host)
        self.server_port = int(port)

    def open_library(self) -> None:
        self.store = Store(self.settings.db_path)
        self.library = Library(self.settings, self.store)

    @property
    def url(self) -> str:
        host = f"[{self.server_name}]" if ":" in self.server_name else self.server_name
        return f"http://{host}:{self.server_port}/"

    def server_close(self) -> None:
        super().server_close()
        self.library = None
        store, self.store = self.store, None
        if store is not None:
            try:
                store.close()
            except sqlite3.Error:  # pragma: no cover - closing is best effort
                log.debug("closing the library failed", exc_info=True)

    def warn_limited(self, key: str, message: str, *args: Any) -> None:
        """Log a warning at most once every 30 s per kind, so a hostile page cannot flood the terminal."""
        now = time.monotonic()
        with self._warn_lock:
            quiet = now - self._warned.get(key, -1e9) < 30.0
            if not quiet:
                self._warned[key] = now
        log.log(logging.DEBUG if quiet else logging.WARNING, message, *args)

    def handle_error(self, request: Any, client_address: Any) -> None:
        exc = sys.exc_info()[1]
        if isinstance(exc, (ConnectionError, TimeoutError)):
            log.debug("connection from %s ended early: %s", client_address, exc)
        else:
            log.error("unexpected error serving %s", client_address, exc_info=True)


class _Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    timeout = REQUEST_TIMEOUT_S
    server: VideoNotesServer

    _responded = False
    _body_read = False

    # -- plumbing ---------------------------------------------------------

    def version_string(self) -> str:
        return "videonotes"

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A002 - signature of the base class
        log.debug("%s " + format, self.client_address[0], *(_printable(str(a)) for a in args))

    def send_error(self, code: int, message: str | None = None, explain: str | None = None) -> None:
        """Protocol-level failures detected by the base class: answer in JSON, never echo the request."""
        status = int(code)
        try:
            phrase = HTTPStatus(status).phrase
        except ValueError:
            phrase = "Error"
        self.close_connection = True
        payload = {"error": {"code": "bad_request" if status < 500 else "server_error", "message": f"{phrase}."}}
        self._send_json(status, payload)

    def _send(
        self,
        status: int,
        body: bytes,
        content_type: str | None,
        *,
        cache: str = "no-store",
        headers: Mapping[str, str] | None = None,
        length: int | None = None,
    ) -> None:
        """Send a complete response (or only its head for HEAD and for bodiless statuses)."""
        self.send_response(status)
        bodiless = status in (HTTPStatus.NO_CONTENT, HTTPStatus.NOT_MODIFIED)
        if content_type and not bodiless:
            self.send_header("Content-Type", content_type)
        if not bodiless:
            self.send_header("Content-Length", str(len(body) if length is None else length))
        for name, value in _SECURITY_HEADERS:
            self.send_header(name, value)
        self.send_header("Cache-Control", cache)
        for name, value in (headers or {}).items():
            self.send_header(name, value)
        if self.close_connection:
            self.send_header("Connection", "close")
        self.end_headers()
        self._responded = True
        if body and not bodiless and self.command != "HEAD":
            self.wfile.write(body)

    def _send_json(self, status: int, payload: Any, *, headers: Mapping[str, str] | None = None) -> None:
        self._send(status, json_bytes(payload), "application/json; charset=utf-8", headers=headers)

    def _fail(self, exc: HttpError) -> None:
        if self._responded:  # part of a response is already on the wire: all we can do is hang up
            self.close_connection = True
            return
        if self.command not in ("GET", "HEAD") and not self._body_read:
            self.close_connection = True  # an unread request body would be parsed as the next request
        self._send_json(exc.status, {"error": {"code": exc.code, "message": exc.message}}, headers=exc.headers)

    # -- entry points -----------------------------------------------------

    def do_GET(self) -> None:
        self._handle()

    do_HEAD = do_GET
    do_POST = do_GET
    do_PUT = do_GET
    do_PATCH = do_GET
    do_DELETE = do_GET
    do_OPTIONS = do_GET

    def _handle(self) -> None:
        self._responded = False
        self._body_read = False
        try:
            if self.command in ("GET", "HEAD") and (
                self.headers.get("Content-Length", "0").strip() not in ("", "0")
                or self.headers.get("Transfer-Encoding")
            ):
                self.close_connection = True  # we do not read bodies of GET requests; do not reuse the connection
            try:
                self._guard()
            except HttpError:
                self.close_connection = True  # do not keep talking to a client we just refused
                raise
            raw_path, _, query = self.path.partition("?")
            segments = split_path(raw_path.partition("#")[0])
            if segments is None:
                self.close_connection = True
                raise HttpError(400, "bad_path", "That address is not valid.")
            self._route(segments, query.partition("#")[0])
        except HttpError as exc:
            self._fail(exc)
        except (ConnectionError, TimeoutError) as exc:
            log.debug("client went away during %s: %s", _printable(self.path), exc)
            self.close_connection = True
        except sqlite3.Error:
            log.exception("library error while serving %s", _printable(self.path))
            self._fail(
                HttpError(503, "library_unavailable", "The library could not be read just now. Try again in a moment.")
            )
        except Exception:  # last resort: log everything, tell the client nothing specific
            log.exception("unexpected error while serving %s", _printable(self.path))
            self._fail(
                HttpError(
                    500,
                    "internal_error",
                    "Something went wrong inside videonotes. The details are in the Terminal window running vnote web.",
                )
            )

    # -- request checks ---------------------------------------------------

    def _guard(self) -> None:
        """Refuse requests that were not made by this server's own page (or a local tool)."""
        port = self.server.server_port
        headers = self.headers
        hosts = headers.get_all("Host") or [] if hasattr(headers, "get_all") else []
        if len(hosts) != 1 or not host_allowed(hosts[0], port):
            self.server.warn_limited(
                "host",
                "refused a request addressed to host %r; only localhost is served (this protects against "
                "other websites reaching your notes)",
                _printable(hosts[0]) if hosts else "",
            )
            raise HttpError(
                403, "forbidden_host", "videonotes only answers requests addressed to localhost on its own port."
            )
        site = (headers.get("Sec-Fetch-Site") or "").strip().lower()
        if site and site not in ("same-origin", "none"):
            page = self.path.partition("?")[0] in ("/", "/index.html")
            navigation = (
                self.command in ("GET", "HEAD")
                and (headers.get("Sec-Fetch-Mode") or "").strip().lower() == "navigate"
                and (headers.get("Sec-Fetch-Dest") or "document").strip().lower() == "document"
            )
            if not (page and navigation):  # following a link to the app is fine; reading its data is not
                self.server.warn_limited("site", "refused a cross-site request for %s", _printable(self.path))
                raise HttpError(403, "cross_site", "This request came from another website and was refused.")
        if self.command not in ("GET", "HEAD"):
            origins = headers.get_all("Origin") or []
            if len(origins) > 1 or (origins and not origin_allowed(origins[0], port)):
                self.server.warn_limited("origin", "refused a %s from origin %r", self.command, _printable(origins[0]))
                raise HttpError(403, "forbidden_origin", "This request came from another website and was refused.")

    # -- routing ----------------------------------------------------------

    def _route(self, segments: list[str], query: str) -> None:
        if segments == ["api", "ask"]:
            if self.command != "POST":
                raise HttpError(405, "method_not_allowed", "Questions are sent with POST.", headers={"Allow": "POST"})
            self._api_ask()
            return
        if self.command not in ("GET", "HEAD"):
            raise HttpError(
                405, "method_not_allowed", "This address is read-only.", headers={"Allow": "GET, HEAD"}
            )
        if not segments or segments == ["index.html"]:
            self._static("index.html")
        elif len(segments) == 2 and segments[0] == "static":
            self._static(segments[1])
        elif segments in (["favicon.svg"], ["favicon.ico"]):
            self._send(200, _FAVICON_SVG, "image/svg+xml", cache="private, max-age=86400")
        elif segments[0] == "api":
            self._api_get(segments[1:], query)
        elif segments[0] == "frames" and len(segments) >= 2:
            params = self._params(query)
            real, content_type = self._library().frame_file("/".join(segments[1:]), _first(params, "k"))
            self._send_file(real, content_type, cache="private, max-age=86400", ranges=False)
        elif segments[0] == "media" and len(segments) == 2:
            real, content_type = self._library().media_file(segments[1])
            self._send_file(real, content_type, cache="private, max-age=3600", ranges=True)
        else:
            raise HttpError(404, "not_found", "There is nothing at that address.")

    def _library(self) -> Library:
        library = self.server.library
        if library is None:
            raise HttpError(503, "library_unavailable", "The library is closed. Start `vnote web` again.")
        return library

    def _params(self, query: str) -> dict[str, list[str]]:
        try:
            return parse_qs(query, keep_blank_values=True, max_num_fields=32)
        except ValueError:
            raise HttpError(400, "bad_query", "That address has a malformed query string.") from None

    def _day_param(self, value: str | None) -> str | None:
        if value is None or value == "":
            return None
        try:
            if not _DAY_RE.match(value):
                raise ValueError(value)
            day_bounds(value)
        except (ValueError, OverflowError, OSError):
            raise HttpError(400, "bad_day", "Dates are written like 2026-11-22.") from None
        return value

    @staticmethod
    def _limit_param(value: str | None, default: int, maximum: int) -> int:
        if value is None:
            return default
        if not _ID_RE.match(value) or not 1 <= int(value) <= maximum:
            raise HttpError(400, "bad_limit", f"limit must be a number from 1 to {maximum}.")
        return int(value)

    def _api_get(self, rest: list[str], query: str) -> None:
        library = self._library()
        params = self._params(query)
        if rest == ["overview"]:
            payload = library.overview()
        elif rest == ["sessions"]:
            day = self._day_param(_first(params, "day"))
            limit = self._limit_param(_first(params, "limit"), SESSIONS_LIMIT_DEFAULT, SESSIONS_LIMIT_MAX)
            payload = library.sessions(day, limit)
        elif len(rest) == 2 and rest[0] == "session":
            payload = library.session(rest[1])
        elif len(rest) == 2 and rest[0] == "day":
            day = self._day_param(rest[1])
            if day is None:
                raise HttpError(400, "bad_day", "Dates are written like 2026-11-22.")
            payload = library.day(day)
        elif rest == ["search"]:
            payload = self._search(library, params)
        elif rest == ["ask"]:  # pragma: no cover - handled before routing; kept for clarity
            raise HttpError(405, "method_not_allowed", "Questions are sent with POST.", headers={"Allow": "POST"})
        else:
            raise HttpError(404, "not_found", "There is nothing at that address.")
        self._send_json(200, payload)

    def _search(self, library: Library, params: dict[str, list[str]]) -> dict[str, Any]:
        query = " ".join((_first(params, "q") or "").split())
        if len(query) > MAX_QUERY_CHARS:
            raise HttpError(400, "bad_query", f"That search is too long (at most {MAX_QUERY_CHARS} characters).")
        day = self._day_param(_first(params, "day"))
        kinds: list[str] = []
        for value in params.get("kind", []):
            for kind in value.split(","):
                kind = kind.strip()
                if not kind:
                    continue
                if kind not in SEARCH_KINDS:
                    raise HttpError(400, "bad_kind", "kind must be one of: " + ", ".join(SEARCH_KINDS) + ".")
                if kind not in kinds:
                    kinds.append(kind)
        limit = self._limit_param(_first(params, "limit"), SEARCH_LIMIT_DEFAULT, SEARCH_LIMIT_MAX)
        return library.search(query, day=day, kinds=kinds, limit=limit)

    # -- POST /api/ask ------------------------------------------------------

    def _read_json(self) -> Any:
        headers = self.headers
        if (headers.get("Content-Type") or "").split(";")[0].strip().lower() != "application/json":
            raise HttpError(415, "unsupported_media_type", "Send the question as JSON (Content-Type: application/json).")
        length_text = (headers.get("Content-Length") or "").strip()
        if headers.get("Transfer-Encoding") or not _ID_RE.match(length_text):
            raise HttpError(411, "length_required", "The request needs a Content-Length.")
        length = int(length_text)
        if length > MAX_POST_BYTES:
            raise HttpError(413, "too_large", "That request is too large.")
        raw = self.rfile.read(length) if length else b""
        if len(raw) != length:
            self.close_connection = True
            raise HttpError(400, "incomplete_body", "The request ended before its body was complete.")
        self._body_read = True
        try:
            return json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, ValueError, RecursionError):
            raise HttpError(400, "bad_json", "The request body is not valid JSON.") from None

    def _api_ask(self) -> None:
        library = self._library()
        body = self._read_json()
        question = body.get("question") if isinstance(body, dict) else None
        if not isinstance(question, str) or not question.strip():
            raise HttpError(400, "bad_question", "Type a question first.")
        question = " ".join(question.split())
        if len(question) > MAX_QUESTION_CHARS:
            raise HttpError(400, "bad_question", f"That question is too long (at most {MAX_QUESTION_CHARS} characters).")
        if not self.server.ask_lock.acquire(blocking=False):
            raise HttpError(
                429,
                "busy",
                "Still working on the previous question. Wait for that answer, then ask again.",
                headers={"Retry-After": "5"},
            )
        started = time.monotonic()
        try:
            payload = library.ask(question)
        except BackendUnavailable as exc:
            log.warning("ask: no usable language model: %s", exc)
            detail = public_error_text(exc) or "No language model is available."
            raise HttpError(503, "backend_unavailable", f"{detail} Run `vnote doctor` to see what to set up.") from None
        except BackendError as exc:
            log.warning("ask: the language model failed: %s", exc)
            detail = public_error_text(exc)
            raise HttpError(
                502,
                "backend_error",
                "The language model ran into a problem" + (f": {detail}" if detail else ".") + " Try again; "
                "`vnote doctor` shows whether the model is set up and running.",
            ) from None
        finally:
            self.server.ask_lock.release()
        log.info("answered a question in %.1f s (%s)", time.monotonic() - started, payload.get("llm_backend") or "?")
        self._send_json(200, payload)

    # -- files --------------------------------------------------------------

    def _static(self, name: str) -> None:
        content_type = _STATIC_FILES.get(name)
        if content_type is None:
            raise HttpError(404, "not_found", "There is nothing at that address.")
        try:
            body = (_STATIC_DIR / name).read_bytes()
        except OSError:
            log.error("the web UI file %s is missing from this installation", name)
            raise HttpError(
                500, "broken_install", "A file of the web page is missing. Reinstall videonotes."
            ) from None
        etag = '"' + hashlib.sha256(body).hexdigest()[:24] + '"'
        if etag_matches(self.headers.get("If-None-Match"), etag):
            self._send(304, b"", None, cache="no-cache", headers={"ETag": etag})
            return
        self._send(200, body, content_type, cache="no-cache", headers={"ETag": etag})

    def _send_file(self, real: Path, content_type: str, *, cache: str, ranges: bool) -> None:
        """Stream a file that has already been checked to lie inside the library."""
        gone = HttpError(404, "not_found", "That file is no longer in the library.")
        try:
            fd = os.open(real, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0))
        except OSError:
            raise gone from None
        with os.fdopen(fd, "rb") as handle:
            info = os.fstat(handle.fileno())
            if not stat.S_ISREG(info.st_mode):
                raise gone
            size = info.st_size
            etag = f'"{info.st_mtime_ns:x}-{size:x}"'
            headers = {"ETag": etag, "Last-Modified": formatdate(info.st_mtime, usegmt=True)}
            if ranges:
                headers["Accept-Ranges"] = "bytes"
            if etag_matches(self.headers.get("If-None-Match"), etag):
                self._send(304, b"", None, cache=cache, headers=headers)
                return
            start, end, status = 0, size - 1, 200
            if ranges:
                if_range = self.headers.get("If-Range")
                wanted = self.headers.get("Range") if if_range is None or if_range.strip() == etag else None
                try:
                    span = parse_range(wanted, size)
                except RangeNotSatisfiable:
                    raise HttpError(
                        416,
                        "range_not_satisfiable",
                        "That part of the file does not exist.",
                        headers={"Content-Range": f"bytes */{size}", "Accept-Ranges": "bytes"},
                    ) from None
                if span is not None:
                    start, end = span
                    status = 206
                    headers["Content-Range"] = f"bytes {start}-{end}/{size}"
            remaining = end - start + 1
            self._send(status, b"", content_type, cache=cache, headers=headers, length=remaining)
            if self.command == "HEAD":
                return
            if start:
                handle.seek(start)
            while remaining > 0:
                try:
                    chunk = handle.read(min(_CHUNK_BYTES, remaining))
                except OSError as exc:
                    chunk = b""
                    log.debug("read error while sending a file: %s", exc)
                if not chunk:  # the file shrank or its disk went away: the client must not reuse this stream
                    self.close_connection = True
                    log.warning("A file could not be read to its end while it was being sent. Was its disk unplugged?")
                    return
                self.wfile.write(chunk)
                remaining -= len(chunk)


def _first(params: dict[str, list[str]], name: str) -> str | None:
    values = params.get(name)
    return values[0] if values else None


# --------------------------------------------------------------------------
# Public API
# --------------------------------------------------------------------------


def _loopback_address(host: str) -> tuple[str, socket.AddressFamily]:
    if host == "localhost":
        return "127.0.0.1", socket.AF_INET
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        ip = None
    if ip is None or not ip.is_loopback:
        raise WebServerError(
            f"Refusing to listen on {host!r}: the web UI shows private footage and is only served to this "
            "computer (127.0.0.1)."
        )
    return str(ip), socket.AF_INET6 if ip.version == 6 else socket.AF_INET


def make_server(settings: Settings, *, host: str = "127.0.0.1", port: int = DEFAULT_PORT) -> ThreadingHTTPServer:
    """Create (but do not start) the web UI server for the library in ``settings``.

    ``port=0`` picks a free port (see ``server.server_port`` / ``server.url``).
    Run it with ``serve_forever()``; ``shutdown()`` then ``server_close()`` stop
    it and close its library connection.  Only loopback addresses are accepted.

    Raises :class:`WebServerError` when the port is taken or not allowed, when
    ``host`` is not a loopback address, or when the library cannot be opened.
    """
    address, family = _loopback_address(host)
    if isinstance(port, bool) or not isinstance(port, int) or not 0 <= port <= 65535:
        raise WebServerError(f"{port!r} is not a usable port number.", hint="Pick one from 1024 to 65535.")
    try:
        server = VideoNotesServer(settings, (address, port), family)
    except OSError as exc:
        if exc.errno == errno.EADDRINUSE:
            raise WebServerError(
                f"Port {port} is already in use (is another `vnote web` still running?).",
                hint=f"Use a different one:  vnote web --port {port + 1 if port < 65535 else 8765}",
            ) from None
        if exc.errno in (errno.EACCES, errno.EPERM):
            raise WebServerError(
                f"This account is not allowed to listen on port {port}.",
                hint="Use a port above 1024:  vnote web --port 8765",
            ) from None
        raise WebServerError(f"Could not start the web server on {address}:{port} ({exc.strerror or exc}).") from None
    try:
        server.open_library()
    except (sqlite3.Error, OSError, RuntimeError) as exc:
        server.server_close()
        raise WebServerError(
            f"The library at {settings.home} could not be opened: {exc}",
            hint="Run `vnote doctor` to check the library folder.",
        ) from None
    return server


def serve(settings: Settings, *, port: int = DEFAULT_PORT, open_browser: bool = True, out: Any = None) -> None:
    """Run the web UI until Ctrl-C.

    Prints the address through ``out`` (a ``videonotes.cli.common.Out``; plain
    logging when None) and optionally opens it in the default browser.  If the
    server cannot start, the reason and what to try are printed and the process
    exits with status 1 (without ``out``, :class:`WebServerError` is raised).
    """

    def say(method: str, text: str) -> None:
        if out is not None:
            getattr(out, method)(text)
        else:
            log.log(logging.WARNING if method in ("warn", "error") else logging.INFO, "%s", text.strip())

    try:
        server = make_server(settings, port=port)
    except WebServerError as exc:
        if out is None:
            raise
        out.error(str(exc))
        if exc.hint:
            out.line(f"  {exc.hint}")
        raise SystemExit(1) from None

    url = server.url
    say("ok", f"videonotes is running at {url}")
    say("info", "  Only this computer can open it. Press Ctrl-C here to stop.")
    if open_browser:

        def launch() -> None:
            try:
                import webbrowser

                opened = webbrowser.open(url)
            except Exception:  # a missing or broken browser must never take the server down
                opened = False
            if not opened:
                say("warn", f"Could not open a browser automatically. Open {url} yourself.")

        threading.Thread(target=launch, name="videonotes-open-browser", daemon=True).start()
    try:
        server.serve_forever(poll_interval=0.25)
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    if out is not None:
        out.line("")
    say("info", "Web UI stopped.")
