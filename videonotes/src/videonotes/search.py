"""Search and ask-your-day over the library.

Retrieval is deliberately simple and transparent: a time filter parsed from
the question, SQLite full-text search over speech, on-screen text, captions
and notes, then widening each hit with what was said around it and the
summary of the moment it belongs to.  The answer step only ever sees that
evidence, and the evidence is returned with the answer so it can be shown.
"""

from __future__ import annotations

import re
from datetime import date, datetime, timedelta

from .config import Settings
from .models import Answer, Evidence, SearchHit
from .store import Store
from .timeutil import day_bounds

_WEEKDAYS = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")
_DATE_RE = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")

#: Rough character budget of evidence handed to the answer step.
EVIDENCE_CHAR_BUDGET = 9000


def search(
    store: Store,
    query: str,
    *,
    limit: int = 20,
    kinds: list[str] | None = None,
    session_id: str | None = None,
    day: str | None = None,
    since_ts: float | None = None,
    until_ts: float | None = None,
) -> list[SearchHit]:
    """Full-text search. ``day`` (YYYY-MM-DD, local) is shorthand for a since/until pair."""
    if day:
        since_ts, until_ts = day_bounds(day)
    return store.search(
        query, limit=limit, kinds=kinds, session_id=session_id, since_ts=since_ts, until_ts=until_ts
    )


def parse_time_scope(question: str, now: datetime | None = None) -> tuple[float | None, float | None]:
    """Find a time restriction in a question ("yesterday", "this morning", "on Tuesday", a date).

    Returns ``(since_ts, until_ts)`` in epoch seconds, or ``(None, None)``.
    Weekday names mean the most recent such day, today included.
    """
    now = now or datetime.now()
    text = question.lower()
    today = now.date()

    def span(d: date, h0: int = 0, h1: int = 24) -> tuple[float, float]:
        start, end = day_bounds(d)
        return start + h0 * 3600, (start + h1 * 3600) if h1 < 24 else end

    if m := _DATE_RE.search(text):
        try:
            return span(date(int(m[1]), int(m[2]), int(m[3])))
        except ValueError:
            pass
    part = None
    if "morning" in text:
        part = (4, 12)
    elif "afternoon" in text:
        part = (12, 18)
    elif "evening" in text or "tonight" in text:
        part = (17, 24)
    if "last night" in text:
        start, _ = day_bounds(today - timedelta(days=1))
        return start + 17 * 3600, day_bounds(today)[0] + 4 * 3600
    if "day before yesterday" in text:
        return span(today - timedelta(days=2), *(part or (0, 24)))
    if "yesterday" in text:
        return span(today - timedelta(days=1), *(part or (0, 24)))
    if re.search(r"\b(today|tonight|this (morning|afternoon|evening))\b", text):
        return span(today, *(part or (0, 24)))
    if re.search(r"\b(this|past) week\b", text):
        return day_bounds(today - timedelta(days=6))[0], day_bounds(today)[1]
    if "last week" in text:
        monday = today - timedelta(days=today.weekday() + 7)
        return day_bounds(monday)[0], day_bounds(monday + timedelta(days=6))[1]
    for i, name in enumerate(_WEEKDAYS):
        if re.search(rf"\b(on |last |this )?{name}\b", text):
            back = (today.weekday() - i) % 7
            return span(today - timedelta(days=back), *(part or (0, 24)))
    return None, None


def gather_evidence(store: Store, question: str, *, limit: int = 30, now: datetime | None = None) -> list[Evidence]:
    """Retrieve the evidence relevant to a question, oldest first."""
    since_ts, until_ts = parse_time_scope(question, now)
    hits = store.search(question, limit=limit, since_ts=since_ts, until_ts=until_ts)

    evidence: dict[tuple[str, str], Evidence] = {}
    budget = EVIDENCE_CHAR_BUDGET

    def add(kind: str, ref_id: str, session_id: str, ts: float | None, text: str) -> None:
        nonlocal budget
        text = text.strip()
        key = (kind, ref_id)
        if not text or key in evidence or budget <= 0:
            return
        text = text[:1500]
        evidence[key] = Evidence(kind=kind, session_id=session_id, ts=ts, text=text, ref_id=ref_id)
        budget -= len(text)

    moment_cache: dict[str, list] = {}

    def moment_for(session_id: str, ts: float | None):
        if ts is None:
            return None
        moments = moment_cache.setdefault(session_id, store.list_moments(session_id))
        for m in moments:
            if m.ts0 - 1 <= ts <= m.ts1 + 1:
                return m
        return None

    for hit in hits:
        if hit.kind == "utterance" and hit.ts is not None:
            # speech makes sense in context: take the lines said just before and after as one block
            around = store.list_utterances(session_id=hit.session_id, ts0=hit.ts - 25, ts1=hit.ts + 40)
            text = " ".join(u.text for u in around) or hit.text
            ts = around[0].ts0 if around else hit.ts
            add("utterance", str(around[0].id) if around else hit.ref_id, hit.session_id, ts, text)
        else:
            add(hit.kind, hit.ref_id, hit.session_id, hit.ts, hit.text)
        moment = moment_for(hit.session_id, hit.ts) if hit.kind in ("utterance", "ocr", "caption") else None
        if moment and (moment.title or moment.summary):
            add("moment", str(moment.id), hit.session_id, moment.ts0, f"{moment.title}: {moment.summary}".strip(": "))

    if since_ts is not None and len(evidence) < 6:
        # A question like "what did I do yesterday?" has no useful keywords: fall back to
        # the notes of everything recorded in that time range.
        for session in sorted(store.list_sessions(since_ts=since_ts, until_ts=until_ts), key=lambda s: s.started_ts):
            if session.note:
                note = session.note
                parts = [note.title, note.summary, *note.key_points, *(a.text for a in note.action_items)]
                add("session", session.id, session.id, session.started_ts, "\n".join(p for p in parts if p))
            for m in store.list_moments(session.id):
                if m.title or m.summary:
                    add("moment", str(m.id), session.id, m.ts0, f"{m.title}: {m.summary}".strip(": "))

    return sorted(evidence.values(), key=lambda e: (e.ts is None, e.ts or 0.0))


def ask(settings: Settings, store: Store, question: str, *, llm: object | None = None, now: datetime | None = None) -> Answer:
    """Answer a question from the library, returning the evidence used.

    ``llm`` may be passed in (it is then left open); otherwise one is created
    from the settings for this call and closed afterwards.  Without any LLM the
    answer is the best-matching excerpts.
    """
    from .notes.summarize import answer_question

    evidence = gather_evidence(store, question, now=now)
    own = False
    if llm is None:
        from .backends.base import BackendUnavailable
        from .backends.llm import make_llm

        try:
            llm = make_llm(settings)
            own = llm is not None
        except BackendUnavailable:
            llm = None
    try:
        return answer_question(llm, question, evidence)  # type: ignore[arg-type]
    finally:
        if own and llm is not None:
            llm.close()  # type: ignore[attr-defined]
