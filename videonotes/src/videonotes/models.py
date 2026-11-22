"""Core data model shared by every videonotes component.

Time conventions (IMPORTANT — every component relies on these):

* ``ts``  — absolute wall-clock time, UNIX epoch seconds (float, UTC).
* ``t``   — seconds from the start of one clip (media-relative, float).
* For anything inside a clip:  ``ts = clip.start_ts + t``.

Paths stored in the database are relative to the videonotes home directory
(``Settings.home``) whenever the file lives inside it, so a library can be
moved or synced.  Use ``Settings.rel()`` / ``Settings.abs()`` to convert.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

# --------------------------------------------------------------------------
# Session / clip
# --------------------------------------------------------------------------

SESSION_KINDS = ("import", "live", "wireless", "file")
SESSION_STATUSES = ("open", "processing", "ready", "error")

#: Per-clip pipeline stages, in execution order.
CLIP_STAGES = ("probe", "extract", "transcribe", "ocr", "caption")
#: Per-session stages, run after every clip of the session finished CLIP_STAGES.
SESSION_STAGES = ("segment", "summarize", "render")


@dataclass
class Session:
    """One continuous stretch of capture: a live run, or a group of imported clips."""

    id: str
    kind: str  # one of SESSION_KINDS
    started_ts: float
    source: str = ""  # human description: "Osmo Action 4 (USB webcam)", "/Volumes/…"
    title: str = ""
    ended_ts: float | None = None
    status: str = "open"  # one of SESSION_STATUSES
    note: SessionNote | None = None
    note_path: str | None = None  # Markdown file, relative to home
    created_ts: float = 0.0
    updated_ts: float = 0.0


@dataclass
class Clip:
    """One media file analysed by the pipeline (a live segment or an imported file)."""

    session_id: str
    path: str  # file that is analysed (proxy if available, else original)
    fingerprint: str  # stable identity used to avoid re-importing the same file
    start_ts: float  # wall-clock time of the first frame
    duration: float = 0.0
    original_path: str | None = None  # full-quality original, if `path` is a proxy
    width: int | None = None
    height: int | None = None
    fps: float | None = None
    has_audio: bool = True
    has_video: bool = True
    stages: dict[str, dict[str, Any]] = field(default_factory=dict)
    id: int | None = None
    created_ts: float = 0.0

    @property
    def end_ts(self) -> float:
        return self.start_ts + self.duration

    def stage_done(self, stage: str) -> bool:
        return self.stages.get(stage, {}).get("status") == "done"


# --------------------------------------------------------------------------
# Perception outputs
# --------------------------------------------------------------------------


@dataclass
class Keyframe:
    """A selected still frame plus whatever was read from / said about it."""

    clip_id: int
    session_id: str
    t: float
    ts: float
    path: str  # JPEG, relative to home
    sharpness: float = 0.0
    novelty: float = 0.0
    reason: str = ""  # why it was selected: "first" | "scene" | "novel" | "interval"
    ocr_text: str | None = None  # None = OCR not run yet; "" = ran, nothing found
    ocr_backend: str | None = None
    caption: str | None = None  # None = not captioned (yet, or skipped by budget)
    caption_backend: str | None = None
    id: int | None = None


@dataclass
class Utterance:
    """A stretch of transcribed speech."""

    clip_id: int
    session_id: str
    t0: float
    t1: float
    ts0: float
    ts1: float
    text: str
    speaker: str | None = None
    backend: str | None = None
    id: int | None = None


# --------------------------------------------------------------------------
# Notes
# --------------------------------------------------------------------------


@dataclass
class ActionItem:
    text: str
    owner: str = ""  # "me", a name, or "" if unknown
    due: str = ""  # free text as stated ("Friday"), never invented
    ts: float | None = None  # where in the session it came from, if known

    @staticmethod
    def from_dict(d: dict[str, Any]) -> ActionItem:
        return ActionItem(
            text=str(d.get("text", "")).strip(),
            owner=str(d.get("owner", "") or "").strip(),
            due=str(d.get("due", "") or "").strip(),
            ts=d.get("ts"),
        )


@dataclass
class Moment:
    """A coherent span of a session (a conversation, a task, a place)."""

    session_id: str
    idx: int
    ts0: float
    ts1: float
    title: str = ""
    summary: str = ""
    tags: list[str] = field(default_factory=list)
    keyframe_ids: list[int] = field(default_factory=list)
    utterance_ids: list[int] = field(default_factory=list)
    id: int | None = None


@dataclass
class SessionNote:
    """The structured note produced for a whole session."""

    title: str = ""
    summary: str = ""
    key_points: list[str] = field(default_factory=list)
    action_items: list[ActionItem] = field(default_factory=list)
    decisions: list[str] = field(default_factory=list)
    open_questions: list[str] = field(default_factory=list)
    people: list[str] = field(default_factory=list)
    places: list[str] = field(default_factory=list)
    captured_text: list[str] = field(default_factory=list)  # whiteboards, slides, screens, signs
    tags: list[str] = field(default_factory=list)
    llm_backend: str = ""  # which summariser produced it ("extractive" = no LLM)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(d: dict[str, Any]) -> SessionNote:
        def strs(key: str) -> list[str]:
            return [str(x).strip() for x in (d.get(key) or []) if str(x).strip()]

        items = []
        for a in d.get("action_items") or []:
            if isinstance(a, str):
                a = {"text": a}
            item = ActionItem.from_dict(a)
            if item.text:
                items.append(item)
        return SessionNote(
            title=str(d.get("title", "") or "").strip(),
            summary=str(d.get("summary", "") or "").strip(),
            key_points=strs("key_points"),
            action_items=items,
            decisions=strs("decisions"),
            open_questions=strs("open_questions"),
            people=strs("people"),
            places=strs("places"),
            captured_text=strs("captured_text"),
            tags=strs("tags"),
            llm_backend=str(d.get("llm_backend", "") or ""),
        )


@dataclass
class DayDigest:
    """Roll-up of every session that started on one local calendar day."""

    date: str  # YYYY-MM-DD (local time)
    headline: str = ""
    summary: str = ""
    highlights: list[str] = field(default_factory=list)
    action_items: list[ActionItem] = field(default_factory=list)
    session_ids: list[str] = field(default_factory=list)
    llm_backend: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(d: dict[str, Any]) -> DayDigest:
        items = []
        for a in d.get("action_items") or []:
            if isinstance(a, str):
                a = {"text": a}
            item = ActionItem.from_dict(a)
            if item.text:
                items.append(item)
        return DayDigest(
            date=str(d.get("date", "")),
            headline=str(d.get("headline", "") or "").strip(),
            summary=str(d.get("summary", "") or "").strip(),
            highlights=[str(x).strip() for x in (d.get("highlights") or []) if str(x).strip()],
            action_items=items,
            session_ids=[str(x) for x in (d.get("session_ids") or [])],
            llm_backend=str(d.get("llm_backend", "") or ""),
        )


@dataclass
class SearchHit:
    kind: str  # "utterance" | "ocr" | "caption" | "moment" | "session"
    ref_id: str
    session_id: str
    ts: float | None
    text: str
    snippet: str
    score: float
