from __future__ import annotations

from datetime import datetime

from videonotes.models import Clip, Keyframe, Moment, Session, SessionNote, Utterance
from videonotes.search import gather_evidence, parse_time_scope, search
from videonotes.timeutil import day_bounds

NOW = datetime(2026, 11, 22, 15, 0, 0)  # a Sunday


def test_parse_time_scope():
    today0, today1 = day_bounds("2026-11-22")
    y0, y1 = day_bounds("2026-11-21")
    assert parse_time_scope("where did I park today?", NOW) == (today0, today1)
    assert parse_time_scope("What happened yesterday", NOW) == (y0, y1)
    assert parse_time_scope("what did we decide this morning", NOW) == (today0 + 4 * 3600, today0 + 12 * 3600)
    assert parse_time_scope("yesterday afternoon", NOW) == (y0 + 12 * 3600, y0 + 18 * 3600)
    assert parse_time_scope("notes from 2026-11-03", NOW) == day_bounds("2026-11-03")
    assert parse_time_scope("what did Sarah say on Friday?", NOW) == day_bounds("2026-11-20")
    assert parse_time_scope("on sunday", NOW) == (today0, today1)  # most recent, today included
    assert parse_time_scope("last night", NOW) == (y0 + 17 * 3600, today0 + 4 * 3600)
    assert parse_time_scope("this week", NOW)[0] == day_bounds("2026-11-16")[0]
    assert parse_time_scope("where are my keys", NOW) == (None, None)
    assert parse_time_scope("2026-13-45 nonsense", NOW) == (None, None)


def _library(store):
    t0 = day_bounds("2026-11-22")[0] + 10 * 3600  # 10:00 today
    s = store.create_session(Session(id="20261122-100000-aaaa", kind="file", started_ts=t0))
    c = store.add_clip(Clip(session_id=s.id, path="a.mp4", fingerprint="a", start_ts=t0, duration=600))
    lines = [
        (10, "Okay let's start the planning meeting."),
        (20, "We decided to ship the Falcon beta on June fourteenth."),
        (30, "I need to call the vendor about the sensors."),
        (300, "I parked the car on level two, row G."),
    ]
    us = store.replace_utterances(c.id, [
        Utterance(clip_id=c.id, session_id=s.id, t0=t, t1=t + 5, ts0=t0 + t, ts1=t0 + t + 5, text=x) for t, x in lines
    ])
    kfs = store.replace_keyframes(c.id, [Keyframe(clip_id=c.id, session_id=s.id, t=25, ts=t0 + 25, path="k.jpg")])
    store.set_keyframe_ocr(kfs[0].id, "Launch plan Q3\nShip Falcon beta by June 14", "x")
    store.replace_moments(s.id, [
        Moment(session_id=s.id, idx=0, ts0=t0 + 10, ts1=t0 + 35, title="Planning meeting", summary="Falcon beta date agreed.",
               utterance_ids=[u.id for u in us[:3]]),
        Moment(session_id=s.id, idx=1, ts0=t0 + 300, ts1=t0 + 305, title="Parking", summary="Parked on level two."),
    ])
    store.update_session(s.id, note=SessionNote(title="Planning and parking", summary="Planned Falcon; parked the car."))
    # an older session that must be excluded by time filters
    old0 = day_bounds("2026-11-10")[0] + 9 * 3600
    o = store.create_session(Session(id="20261110-090000-bbbb", kind="file", started_ts=old0))
    oc = store.add_clip(Clip(session_id=o.id, path="b.mp4", fingerprint="b", start_ts=old0, duration=60))
    store.replace_utterances(oc.id, [Utterance(clip_id=oc.id, session_id=o.id, t0=1, t1=3, ts0=old0 + 1, ts1=old0 + 3,
                                               text="I parked the car on the street near the bakery.")])
    return s, o


def test_search_day_filter(store):
    s, o = _library(store)
    assert {h.session_id for h in search(store, "parked car")} == {s.id, o.id}
    assert {h.session_id for h in search(store, "parked car", day="2026-11-22")} == {s.id}
    assert search(store, "parked", session_id=o.id)[0].session_id == o.id


def test_gather_evidence_expands_context_and_scopes_time(store):
    s, o = _library(store)
    ev = gather_evidence(store, "when is the falcon beta shipping?", now=NOW)
    kinds = {e.kind for e in ev}
    assert {"utterance", "ocr", "moment"} <= kinds
    speech = next(e for e in ev if e.kind == "utterance")
    assert "planning meeting" in speech.text and "vendor" in speech.text  # neighbours pulled in
    assert [e.ts for e in ev] == sorted(e.ts for e in ev)
    assert len({(e.kind, e.ref_id) for e in ev}) == len(ev)

    ev = gather_evidence(store, "where did I park today?", now=NOW)
    assert all(e.session_id == s.id for e in ev) and any("level two" in e.text for e in ev)

    # no keywords, only a time scope: falls back to that period's notes
    ev = gather_evidence(store, "what did I do today?", now=NOW)
    assert any(e.kind == "session" and "Planned Falcon" in e.text for e in ev)
    assert gather_evidence(store, "zebra xylophone", now=NOW) == []
