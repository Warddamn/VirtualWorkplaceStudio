from __future__ import annotations

import sqlite3

import pytest

from videonotes.models import ActionItem, Clip, DayDigest, Keyframe, Moment, Session, SessionNote, Utterance
from videonotes.store import Store, fts_query


def _session(store: Store, sid: str = "20261122-143200-ab12", ts: float = 1_800_000_000.0) -> Session:
    return store.create_session(Session(id=sid, kind="file", started_ts=ts, source="test"))


def _clip(store: Store, sid: str, fp: str = "fp1", start: float = 1_800_000_000.0) -> Clip:
    return store.add_clip(Clip(session_id=sid, path="media/a.mp4", fingerprint=fp, start_ts=start, duration=60))


def test_session_roundtrip_and_find(store: Store):
    s = _session(store)
    assert store.get_session(s.id).kind == "file"
    assert store.find_session("20261122").id == s.id
    assert store.find_session("latest").id == s.id
    _session(store, "20261122-150000-cd34", 1_800_000_100.0)
    assert store.find_session("20261122") is None  # ambiguous prefix
    assert store.find_session("latest").id == "20261122-150000-cd34"
    assert [x.id for x in store.list_sessions()] == ["20261122-150000-cd34", s.id]


def test_clip_fingerprint_unique_and_stages(store: Store):
    s = _session(store)
    c = _clip(store, s.id)
    with pytest.raises(sqlite3.IntegrityError):
        _clip(store, s.id)
    assert store.clip_by_fingerprint("fp1").id == c.id
    store.set_clip_stage(c.id, "extract", "done", keyframes=3)
    got = store.get_clip(c.id)
    assert got.stage_done("extract") and not got.stage_done("ocr")
    assert got.stages["extract"]["keyframes"] == 3
    store.clear_clip_stage(c.id, "extract")
    assert not store.get_clip(c.id).stage_done("extract")
    assert store.session_bounds(s.id) == (1_800_000_000.0, 1_800_000_060.0)


def test_keyframes_utterances_search(store: Store):
    s = _session(store)
    c = _clip(store, s.id)
    kfs = store.replace_keyframes(
        c.id,
        [
            Keyframe(clip_id=c.id, session_id=s.id, t=1.0, ts=c.start_ts + 1, path="frames/1.jpg"),
            Keyframe(clip_id=c.id, session_id=s.id, t=30.0, ts=c.start_ts + 30, path="frames/2.jpg"),
        ],
    )
    assert all(k.id for k in kfs)
    store.set_keyframe_ocr(kfs[0].id, "Launch plan Q3: ship Falcon beta", "rapidocr")
    store.set_keyframe_caption(kfs[1].id, "A person writing on a whiteboard in an office", "mock")
    store.replace_utterances(
        c.id,
        [
            Utterance(clip_id=c.id, session_id=s.id, t0=2, t1=6, ts0=c.start_ts + 2, ts1=c.start_ts + 6,
                      text="Remember to email the quarterly budget to Sarah before Friday."),
        ],
    )
    assert store.search("falcon")[0].kind == "ocr"
    assert store.search("whiteboards")[0].kind == "caption"  # porter stemming
    hit = store.search("what did I need to email Sarah?")[0]
    assert hit.kind == "utterance" and "[" in hit.snippet
    assert store.search("falcon", kinds=["utterance"]) == []
    assert store.search("???") == []
    # re-running a stage replaces rows and their index entries
    store.replace_utterances(c.id, [])
    assert store.search("budget") == []
    store.replace_keyframes(c.id, [])
    assert store.search("falcon") == []
    assert store.list_keyframes(session_id=s.id) == []


def test_keyframe_time_filters(store: Store):
    s = _session(store)
    c = _clip(store, s.id)
    store.replace_keyframes(
        c.id, [Keyframe(clip_id=c.id, session_id=s.id, t=float(t), ts=c.start_ts + t, path=f"f{t}.jpg") for t in (1, 20, 40)]
    )
    got = store.list_keyframes(session_id=s.id, ts0=c.start_ts + 10, ts1=c.start_ts + 40)
    assert [k.t for k in got] == [20.0]


def test_notes_moments_days(store: Store):
    s = _session(store)
    note = SessionNote(
        title="Budget sync", summary="Talked about the budget.", key_points=["Budget due Friday"],
        action_items=[ActionItem(text="Email budget to Sarah", owner="me", due="Friday")],
    )
    store.update_session(s.id, note=note, title=note.title, status="ready")
    got = store.get_session(s.id)
    assert got.note.action_items[0].due == "Friday" and got.status == "ready"
    assert store.search("sarah")[0].kind == "session"
    ms = store.replace_moments(s.id, [Moment(session_id=s.id, idx=0, ts0=1, ts1=2, title="Desk", summary="Typing", tags=["work"], keyframe_ids=[1], utterance_ids=[2])])
    store.update_moment(ms[0].id, title="At the desk", summary="Typing an email", tags=["work"])
    m = store.list_moments(s.id)[0]
    assert m.title == "At the desk" and m.keyframe_ids == [1] and m.utterance_ids == [2]
    assert store.search("typing")[0].kind == "moment"
    store.save_day(DayDigest(date="2026-11-22", headline="A day", session_ids=[s.id]), "notes/days/2026-11-22.md")
    assert store.get_day("2026-11-22").session_ids == [s.id]
    assert store.get_day("2026-11-23") is None
    store.delete_session(s.id)
    assert store.search("sarah") == [] and store.stats()["sessions"] == 0


def test_session_note_from_untrusted_dict():
    note = SessionNote.from_dict({"title": " T ", "action_items": ["call Bob", {"text": ""}, {"text": "x", "owner": None}],
                                  "key_points": ["a", "", None], "people": None})
    assert note.title == "T" and [a.text for a in note.action_items] == ["call Bob", "x"]
    assert note.key_points == ["a", "None"] or note.key_points == ["a"]


def test_fts_query_is_safe():
    assert fts_query('he said "hello" AND (NOT) x*') .count('"') % 2 == 0
    assert fts_query("") == ""
    assert "keys" in fts_query("where did I leave my keys")


def test_moment_kind_salience_and_search_scale(store: Store):
    s = _session(store)
    ms = store.replace_moments(s.id, [Moment(session_id=s.id, idx=0, ts0=1, ts1=2, kind="transit", salience="background")])
    assert store.list_moments(s.id)[0].salience == "background"
    store.update_moment(ms[0].id, title="Walk", summary="Walking", tags=[])
    assert store.list_moments(s.id)[0].kind == "transit"  # None leaves kind/salience alone
    store.update_moment(ms[0].id, title="Walk", summary="Walking", tags=[], kind="errand", salience="highlight")
    m = store.list_moments(s.id)[0]
    assert (m.kind, m.salience) == ("errand", "highlight")

    # replacing rows must stay cheap and leave no stale index entries behind
    c = _clip(store, s.id)
    for round_no in range(3):
        us = [Utterance(clip_id=c.id, session_id=s.id, t0=i, t1=i + 1, ts0=c.start_ts + i, ts1=c.start_ts + i + 1,
                        text=f"round{round_no} marker word{i}") for i in range(300)]
        store.replace_utterances(c.id, us)
    assert store.search("round0") == [] and store.search("round1") == []
    assert len(store.search("round2", limit=500)) == 300
    assert store.search("word7", since_ts=c.start_ts + 7, until_ts=c.start_ts + 8)[0].text.endswith("word7")
    assert store.search("word7", since_ts=c.start_ts + 100) == []
    n_docs = store._one("SELECT COUNT(*) AS n FROM search")["n"]
    assert n_docs == 300 + 1  # utterances + the moment
