"""Time and identifier helpers. All stored times are epoch seconds (UTC); all
times shown to the user are local time."""

from __future__ import annotations

import re
import secrets
import time
from datetime import date, datetime, timedelta


def now_ts() -> float:
    return time.time()


def local_dt(ts: float) -> datetime:
    """Epoch seconds -> timezone-aware local datetime."""
    return datetime.fromtimestamp(ts).astimezone()


def new_session_id(started_ts: float) -> str:
    """Sortable, human-readable id: ``YYYYMMDD-HHMMSS-xxxx`` (local time + random suffix)."""
    return f"{local_dt(started_ts):%Y%m%d-%H%M%S}-{secrets.token_hex(2)}"


def local_date(ts: float) -> str:
    """Local calendar day of a timestamp as ``YYYY-MM-DD``."""
    return f"{local_dt(ts):%Y-%m-%d}"


def day_bounds(day: str | date) -> tuple[float, float]:
    """Epoch range ``[start, end)`` of a local calendar day (DST-safe)."""
    d = date.fromisoformat(day) if isinstance(day, str) else day
    start = datetime(d.year, d.month, d.day).astimezone()
    nxt = d + timedelta(days=1)
    end = datetime(nxt.year, nxt.month, nxt.day).astimezone()
    return start.timestamp(), end.timestamp()


def parse_day(text: str | None) -> str:
    """Accept 'today', 'yesterday' or YYYY-MM-DD; return YYYY-MM-DD."""
    today = datetime.now().date()
    if not text or text == "today":
        return today.isoformat()
    if text == "yesterday":
        return (today - timedelta(days=1)).isoformat()
    return date.fromisoformat(text).isoformat()


def fmt_clock(ts: float, fmt: str = "%H:%M") -> str:
    return local_dt(ts).strftime(fmt)


def fmt_offset(seconds: float) -> str:
    """Media offset as ``M:SS`` or ``H:MM:SS``."""
    s = max(0, int(round(seconds)))
    h, rem = divmod(s, 3600)
    m, sec = divmod(rem, 60)
    return f"{h}:{m:02d}:{sec:02d}" if h else f"{m}:{sec:02d}"


def fmt_duration(seconds: float) -> str:
    """Human duration: ``45 s``, ``12 min``, ``1 h 05 min``."""
    s = max(0, int(round(seconds)))
    if s < 90:
        return f"{s} s"
    m = int(round(s / 60))
    if m < 60:
        return f"{m} min"
    h, m = divmod(m, 60)
    return f"{h} h {m:02d} min"


_UNSAFE = re.compile(r"[^\w\- ]+", re.UNICODE)


def slugify(text: str, max_len: int = 60) -> str:
    """Filesystem-safe fragment for note file names (keeps spaces, drops punctuation)."""
    cleaned = _UNSAFE.sub(" ", text).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned[:max_len].rstrip() or "Untitled"
