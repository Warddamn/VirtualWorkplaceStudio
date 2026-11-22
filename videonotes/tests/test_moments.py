from __future__ import annotations

import math
import random
import time
from itertools import pairwise

import pytest

from videonotes.config import NotesSettings
from videonotes.models import Keyframe, Moment, Session, Utterance
from videonotes.notes.moments import (
    HIGH_NOVELTY,
    OVERLAP_TOLERANCE,
    coverage_hole_seconds,
    segment_moments,
)

T0 = 1_795_357_920.0  # an arbitrary wall-clock start
SID = "20261122-143200-ab12"
SESSION = Session(id=SID, kind="import", started_ts=T0)


def cfg(gap: float = 45.0, lo: float = 20.0, hi: float = 600.0) -> NotesSettings:
    return NotesSettings(moment_gap_seconds=gap, moment_min_seconds=lo, moment_max_seconds=hi)


class Timeline:
    """Builds utterances / keyframes with unique ids, times given in seconds from T0."""

    def __init__(self) -> None:
        self.utterances: list[Utterance] = []
        self.keyframes: list[Keyframe] = []
        self._next_id = 1

    def _id(self) -> int:
        self._next_id += 1
        return self._next_id - 1

    def say(self, t0: float, t1: float, text: str = "words", clip: int = 1) -> Utterance:
        u = Utterance(clip_id=clip, session_id=SID, t0=t0, t1=t1, ts0=T0 + t0, ts1=T0 + t1, text=text, id=self._id())
        self.utterances.append(u)
        return u

    def frame(self, t: float, reason: str = "interval", novelty: float = 0.1, clip: int = 1) -> Keyframe:
        k = Keyframe(clip_id=clip, session_id=SID, t=t, ts=T0 + t, path=f"frames/{t}.jpg", reason=reason,
                     novelty=novelty, id=self._id())  # fmt: skip
        self.keyframes.append(k)
        return k

    def talk(self, start: float, end: float, *, length: float = 4.0, pause: float = 0.5, clip: int = 1) -> None:
        """Back-to-back utterances filling [start, end]."""
        t = start
        while t + length <= end + 1e-9:
            self.say(t, t + length, clip=clip)
            t += length + pause

    def segment(self, settings: NotesSettings) -> list[Moment]:
        return segment_moments(SESSION, self.utterances, self.keyframes, settings)


def rel(moments: list[Moment]) -> list[tuple[float, float]]:
    """Moment bounds in seconds from T0, rounded."""
    return [(round(m.ts0 - T0, 3), round(m.ts1 - T0, 3)) for m in moments]


# ---------------------------------------------------------------------------
# The invariants, re-derived here independently of the implementation
# ---------------------------------------------------------------------------


def check_invariants(
    moments: list[Moment], utterances: list[Utterance], keyframes: list[Keyframe], settings: NotesSettings
) -> None:
    gap_s = settings.moment_gap_seconds
    min_s = settings.moment_min_seconds
    max_s = settings.moment_max_seconds
    hole_s = coverage_hole_seconds(settings, keyframes)
    eps = 1e-6

    if not utterances and not keyframes:
        assert moments == []
        return
    assert moments, "material but no moments"

    # numbering and emptiness of what the summariser fills in
    assert [m.idx for m in moments] == list(range(len(moments)))
    for m in moments:
        assert m.session_id == SID and m.title == "" and m.summary == "" and m.tags == []
        assert math.isfinite(m.ts0) and math.isfinite(m.ts1) and m.ts0 <= m.ts1

    # ordered and non-overlapping
    for a, b in pairwise(moments):
        assert a.ts0 < b.ts0
        assert a.ts1 <= b.ts0

    # every utterance / keyframe in exactly one moment
    assert sorted(i for m in moments for i in m.utterance_ids) == sorted(u.id for u in utterances)
    assert sorted(i for m in moments for i in m.keyframe_ids) == sorted(k.id for k in keyframes)

    by_u = {u.id: u for u in utterances}
    by_k = {k.id: k for k in keyframes}
    owner: dict[tuple[str, int], int] = {}
    for n, m in enumerate(moments):
        nxt = moments[n + 1].ts0 if n + 1 < len(moments) else math.inf
        spans = [(by_u[i].ts0, max(by_u[i].ts0, by_u[i].ts1)) for i in m.utterance_ids]
        spans += [(by_k[i].ts, by_k[i].ts) for i in m.keyframe_ids]
        assert spans, "empty moment"
        for start, _ in spans:  # assigned by start time
            assert m.ts0 <= start < nxt
        latest = max(end for _, end in spans)
        assert m.ts0 == min(start for start, _ in spans)  # tight at the front
        assert m.ts1 == min(latest, nxt)  # tight at the back (cut short only by the next moment)
        assert latest - m.ts1 <= OVERLAP_TOLERANCE + eps  # nothing runs on past a boundary: no mid-utterance cut
        # ids are listed in time order
        assert [by_u[i].ts0 for i in m.utterance_ids] == sorted(by_u[i].ts0 for i in m.utterance_ids)
        assert [by_k[i].ts for i in m.keyframe_ids] == sorted(by_k[i].ts for i in m.keyframe_ids)
        for i in m.utterance_ids:
            owner[("u", i)] = n
        for i in m.keyframe_ids:
            owner[("k", i)] = n

    # one sorted timeline with the running end of everything seen so far
    items = [(u.ts0, max(u.ts0, u.ts1), ("u", u.id)) for u in utterances]
    items += [(k.ts, k.ts, ("k", k.id)) for k in keyframes]
    items.sort(key=lambda it: (it[0], it[2][0] == "k", it[1]))
    running = -math.inf
    speech_end = -math.inf
    cuttable: dict[int, bool] = {}  # moment -> is there any place inside where it could be cut
    for (s0, e0, key0), (s1, _e1, key1) in pairwise(items):
        running = max(running, e0)
        if key0[0] == "u":
            speech_end = max(speech_end, e0)
        same = owner[key0] == owner[key1]
        # a coverage hole is always a boundary
        if s1 - running >= hole_s:
            assert not same, "a coverage hole inside a moment"
        # a long pause in speech is a boundary (it can only be merged away to honour the minimum length)
        if key1[0] == "u" and math.isfinite(speech_end) and s1 - speech_end >= gap_s and min_s <= 0:
            previous_speaker = max(
                (it for it in items if it[2][0] == "u" and it[0] < s1), key=lambda it: it[1], default=None
            )
            if previous_speaker is not None:
                assert owner[previous_speaker[2]] != owner[key1], "a long pause inside a moment"
        if same and s1 > s0 and s1 >= running - OVERLAP_TOLERANCE:
            cuttable[owner[key0]] = True

    for n, m in enumerate(moments):
        length = m.ts1 - m.ts0
        # the maximum is honoured wherever a cut is possible at all
        if length > max_s + eps:
            assert not cuttable.get(n, False), f"moment {n} is {length:.0f}s long but could have been cut"
        # the minimum is honoured unless merging would cross a hole or break the maximum
        if length < min_s - eps:
            for other in (n - 1, n + 1):
                if not 0 <= other < len(moments):
                    continue
                a, b = sorted((n, other))
                first_of_b = min(
                    [by_u[i].ts0 for i in moments[b].utterance_ids] + [by_k[i].ts for i in moments[b].keyframe_ids]
                )
                before = (
                    max(max(by_u[i].ts0, by_u[i].ts1) for mm in moments[: a + 1] for i in mm.utterance_ids)
                    if any(mm.utterance_ids for mm in moments[: a + 1])
                    else -math.inf
                )
                before = max([before] + [by_k[i].ts for mm in moments[: a + 1] for i in mm.keyframe_ids])
                hole = first_of_b - before >= hole_s
                merged = max(moments[a].ts1, moments[b].ts1) - moments[a].ts0
                assert hole or merged > max_s - OVERLAP_TOLERANCE - eps, (
                    f"moment {n} ({length:.1f}s) should have been merged with moment {other}"
                )


def random_timeline(rng: random.Random) -> Timeline:
    tl = Timeline()
    t = 0.0
    for clip in range(1, rng.randint(1, 4) + 1):
        t += rng.choice([0.0, 0.0, 3.0, 50.0, 130.0, 400.0, 4000.0])  # recording off between clips
        clip_len = rng.choice([8.0, 40.0, 200.0, 900.0, 2500.0])
        clip_start, clip_end = t, t + clip_len
        mode = rng.choice(["speech", "speech", "mixed", "silent", "empty"])
        if mode in ("speech", "mixed"):
            u = clip_start + rng.uniform(0, 20)
            while u < clip_end:
                length = rng.choice([0.0, 0.4, 2.0, 5.0, 12.0, 40.0])
                tl.say(u, min(u + length, clip_end + 5), clip=clip)
                u += length + rng.choice([-0.6, -0.2, -0.05, 0.0, 0.3, 1.0, 2.5, 8.0, 30.0, 70.0, 150.0, 500.0])
                if u < clip_start:
                    u = clip_start
        if mode in ("mixed", "silent"):
            step = rng.choice([15.0, 60.0, 60.0, 200.0])
            k = clip_start
            while k < clip_end:
                roll = rng.random()
                if roll < 0.1:
                    reason, novelty = "scene", 0.8
                elif roll < 0.3:
                    reason, novelty = "novel", rng.uniform(0.2, 0.9)
                else:
                    reason, novelty = "interval", rng.uniform(0.0, 0.2)
                tl.frame(k, reason, novelty, clip=clip)
                if rng.random() < 0.05:
                    tl.frame(k, "novel", 0.3, clip=clip)  # two frames at the very same instant
                k += step * rng.uniform(0.3, 1.0)
        t = clip_end
    return tl


@pytest.mark.parametrize("seed", range(400))
def test_random_timelines_keep_every_invariant(seed: int):
    rng = random.Random(seed)
    tl = random_timeline(rng)
    settings = cfg(
        gap=rng.choice([5.0, 20.0, 45.0, 120.0]),
        lo=rng.choice([0.0, 0.0, 5.0, 20.0, 30.0, 90.0]),
        hi=rng.choice([30.0, 120.0, 600.0, 900.0, 1e9]),
    )
    moments = tl.segment(settings)
    check_invariants(moments, tl.utterances, tl.keyframes, settings)

    # deterministic, and independent of the order the caller happened to pass things in
    again = tl.segment(settings)
    assert again == moments
    shuffled_u, shuffled_k = tl.utterances[:], tl.keyframes[:]
    rng.shuffle(shuffled_u)
    rng.shuffle(shuffled_k)
    assert segment_moments(SESSION, shuffled_u, shuffled_k, settings) == moments


@pytest.mark.parametrize("seed", range(150))
def test_invariants_hold_when_the_splitter_thins_its_candidates(seed: int, monkeypatch: pytest.MonkeyPatch):
    # very dense spans are split using only the best cut candidate per time slice; force that path everywhere
    from videonotes.notes import moments as module

    monkeypatch.setattr(module, "_DENSE_ATOMS", 0)
    monkeypatch.setattr(module, "_SLICES", 6)
    rng = random.Random(10_000 + seed)
    tl = random_timeline(rng)
    settings = cfg(gap=rng.choice([20.0, 45.0, 120.0]), lo=rng.choice([0.0, 20.0]), hi=rng.choice([30.0, 120.0, 600.0]))
    check_invariants(tl.segment(settings), tl.utterances, tl.keyframes, settings)


def test_dense_span_with_a_large_maximum_is_thinned_and_still_split_well():
    tl = Timeline()
    t = 0.0
    while t < 3.5 * 3600:  # three and a half hours, an utterance every second
        tl.say(t, t + 0.8)
        t += 1.0
    breather = 6000.0  # one 20 s pause, not where an even cut would fall (that would be 6300)
    tl.utterances = [u for u in tl.utterances if not breather <= u.t0 < breather + 20]
    settings = cfg(gap=120, lo=30, hi=3600)
    began = time.perf_counter()
    moments = tl.segment(settings)
    elapsed = time.perf_counter() - began
    check_invariants(moments, tl.utterances, tl.keyframes, settings)
    assert len(moments) == 4 and max(m.ts1 - m.ts0 for m in moments) <= 3600  # as few moments as possible ...
    assert moments[2].ts0 == T0 + breather + 20  # ... and the pause is where the middle cut went
    assert min(m.ts1 - m.ts0 for m in moments) > 2400
    assert elapsed < 10, f"segmenting took {elapsed:.1f}s"


def test_the_checker_itself_catches_a_bad_segmentation():
    tl = Timeline()
    a = tl.say(0, 10)
    b = tl.say(200, 210)  # a coverage hole in between
    bad = [Moment(session_id=SID, idx=0, ts0=a.ts0, ts1=b.ts1, utterance_ids=[a.id, b.id])]
    with pytest.raises(AssertionError):
        check_invariants(bad, tl.utterances, tl.keyframes, cfg())
    mid = tl.say(300, 320)
    cut_inside = [
        Moment(session_id=SID, idx=0, ts0=a.ts0, ts1=a.ts1, utterance_ids=[a.id]),
        Moment(session_id=SID, idx=1, ts0=b.ts0, ts1=b.ts1, utterance_ids=[b.id]),
        Moment(session_id=SID, idx=2, ts0=mid.ts0, ts1=mid.ts0 + 5, utterance_ids=[mid.id]),
    ]
    with pytest.raises(AssertionError):
        check_invariants(cut_inside, tl.utterances, tl.keyframes, cfg(lo=0))


# ---------------------------------------------------------------------------
# Scenarios
# ---------------------------------------------------------------------------


def test_nothing_at_all_gives_no_moments():
    assert segment_moments(SESSION, [], [], cfg()) == []


def test_single_utterance_is_one_moment_even_if_short():
    tl = Timeline()
    u = tl.say(12.0, 14.5, "Buy milk.")
    moments = tl.segment(cfg())
    assert len(moments) == 1
    m = moments[0]
    assert (m.idx, m.ts0, m.ts1, m.utterance_ids, m.keyframe_ids) == (0, u.ts0, u.ts1, [u.id], [])
    assert (m.title, m.summary, m.tags, m.session_id) == ("", "", [], SID)


def test_single_keyframe_is_one_moment():
    tl = Timeline()
    k = tl.frame(3.0, "first", 1.0)
    moments = tl.segment(cfg())
    assert rel(moments) == [(3.0, 3.0)] and moments[0].keyframe_ids == [k.id]


def test_three_hour_silent_walk_is_cut_into_even_stretches():
    tl = Timeline()
    for i in range(181):  # one interval keyframe a minute, nothing else
        tl.frame(i * 60.0)
    settings = cfg(hi=600)
    moments = tl.segment(settings)
    check_invariants(moments, tl.utterances, tl.keyframes, settings)
    lengths = [m.ts1 - m.ts0 for m in moments]
    assert max(lengths) <= 600
    # as few moments as the maximum allows (11 frames span 600 s), all of similar length
    assert len(moments) == math.ceil(181 / 11)
    assert min(lengths) >= 480
    assert sum(len(m.keyframe_ids) for m in moments) == 181 and not any(m.utterance_ids for m in moments)


def test_forty_minutes_of_rapid_conversation_is_cut_evenly_between_utterances():
    rng = random.Random(7)
    tl = Timeline()
    t = 0.0
    while t < 2400:
        length = rng.uniform(0.8, 4.0)
        tl.say(t, t + length)
        t += length + rng.choice([-0.3, -0.1, 0.0, 0.1, 0.2, 0.5])  # speakers cutting in on each other
    for i in range(40):
        tl.frame(i * 60.0 + 7)
    settings = cfg(hi=600)
    moments = tl.segment(settings)
    check_invariants(moments, tl.utterances, tl.keyframes, settings)
    lengths = [m.ts1 - m.ts0 for m in moments]
    assert len(moments) in (4, 5)
    assert max(lengths) <= 600 and min(lengths) >= 400
    boundaries = [m.ts0 for m in moments[1:]]
    for b in boundaries:  # each boundary is the start of an utterance or keyframe, never inside one
        assert any(u.ts0 == b for u in tl.utterances) or any(k.ts == b for k in tl.keyframes)
        assert not any(u.ts0 < b and u.ts1 > b + OVERLAP_TOLERANCE for u in tl.utterances)


def test_two_clips_an_hour_apart_are_never_merged():
    tl = Timeline()
    tl.frame(0, "first", 1.0, clip=1)
    tl.talk(1, 121, clip=1)
    tl.frame(60, clip=1)
    tl.frame(3600 + 122, "first", 1.0, clip=2)
    last = tl.say(3600 + 123, 3600 + 126, "One more thing.", clip=2)  # far shorter than the minimum
    moments = tl.segment(cfg(lo=20))
    assert len(moments) == 2
    assert moments[0].ts1 - T0 < 125 and moments[1].ts0 - T0 == 3722
    assert moments[1].utterance_ids == [last.id] and len(moments[1].keyframe_ids) == 1
    check_invariants(moments, tl.utterances, tl.keyframes, cfg(lo=20))


def test_clips_minutes_apart_split_even_without_speech():
    tl = Timeline()
    for t in (0, 20, 40, 60):
        tl.frame(t, clip=1)
    for t in (300, 320, 340, 360):
        tl.frame(t, clip=2)
    assert rel(tl.segment(cfg())) == [(0, 60), (300, 360)]


def test_tiny_negative_overlaps_from_speech_to_text_do_not_matter():
    tl = Timeline()
    tl.say(0.0, 5.2)
    tl.say(5.0, 9.95)  # starts 0.2 s before the previous one ends
    tl.say(9.9, 14.0)
    tl.say(13.98, 30.0)
    moments = tl.segment(cfg())
    assert rel(moments) == [(0.0, 30.0)]
    assert moments[0].utterance_ids == [u.id for u in tl.utterances]
    # under pressure from the maximum the moment is cut between two of them, and stays non-overlapping
    tight = cfg(lo=0, hi=16)
    moments = tl.segment(tight)
    check_invariants(moments, tl.utterances, tl.keyframes, tight)
    assert len(moments) == 2
    assert moments[0].ts1 == moments[1].ts0 == T0 + 13.98  # 14.0 shortened to where the next moment starts


def test_overlap_beyond_the_tolerance_is_never_cut():
    tl = Timeline()
    tl.say(0, 100)
    tl.say(60, 160)  # 40 s of two people talking at once
    tl.say(120, 220)
    moments = tl.segment(cfg(lo=0, hi=90))
    assert rel(moments) == [(0, 220)]


def test_pause_shorter_than_the_gap_keeps_one_moment_longer_pause_splits():
    tl = Timeline()
    tl.talk(0, 60)
    tl.talk(100, 160)  # 40 s after the last word (which ends at 58.5)
    assert len(tl.segment(cfg(gap=45))) == 1
    assert len(tl.segment(cfg(gap=41))) == 2
    assert [len(m.utterance_ids) for m in tl.segment(cfg(gap=30))] == [13, 13]


def test_keyframes_in_a_pause_stay_with_the_speech_they_are_close_to():
    tl = Timeline()
    tl.talk(0, 60)  # ends at 58.5
    near_first = tl.frame(65)
    near_second = tl.frame(118)
    tl.talk(120, 180)
    moments = tl.segment(cfg(gap=45))
    assert len(moments) == 2
    assert near_first.id in moments[0].keyframe_ids and near_second.id in moments[1].keyframe_ids
    assert moments[0].ts1 == near_first.ts and moments[1].ts0 == near_second.ts


def test_a_long_silent_stretch_between_two_conversations_is_its_own_moment():
    tl = Timeline()
    tl.talk(0, 120)
    for t in range(130, 720, 30):
        tl.frame(float(t))
    tl.talk(720, 840)
    settings = cfg(gap=45, lo=20, hi=600)
    moments = tl.segment(settings)
    check_invariants(moments, tl.utterances, tl.keyframes, settings)
    assert len(moments) == 3
    talk1, walk, talk2 = moments
    assert talk1.utterance_ids and talk2.utterance_ids and not walk.utterance_ids
    assert len(walk.keyframe_ids) >= 15
    # the frames right after / right before the talking stay with it
    assert talk1.keyframe_ids and talk2.keyframe_ids


def test_scene_change_in_a_pause_starts_the_next_moment():
    tl = Timeline()
    tl.talk(0, 60)  # ends 58.5
    still_there = tl.frame(62)
    moved = tl.frame(70, "scene", 0.9)
    after = tl.frame(75)
    tl.talk(110, 170)
    moments = tl.segment(cfg(gap=45))
    assert len(moments) == 2
    assert moments[0].keyframe_ids == [still_there.id]
    assert moments[1].keyframe_ids == [moved.id, after.id] and moments[1].ts0 == moved.ts


def test_first_frame_of_each_live_segment_is_not_a_scene_change():
    # live capture: one clip a minute, each starting with a "first" frame that is maximally novel by definition
    def record(reason_at_60: str) -> list[Moment]:
        tl = Timeline()
        tl.talk(0, 55, clip=1)  # ends 53.5
        tl.frame(60, reason_at_60, 1.0, clip=2)
        tl.frame(75, "interval", 0.1, clip=2)
        tl.frame(120, "first", 1.0, clip=3)
        tl.talk(125, 180, clip=3)
        return tl.segment(cfg(gap=45, lo=20))

    plain = record("first")
    assert [len(m.keyframe_ids) for m in plain] == [2, 1]  # the frames just after the talk stay with it
    moved = record("scene")
    assert [len(m.keyframe_ids) for m in moved] == [0, 3]  # a real change of scene starts the next moment


def test_long_talk_is_split_at_its_longest_pause():
    tl = Timeline()
    tl.talk(0, 350)  # ... a breather of ~30 s (shorter than the gap) ...
    tl.talk(380, 900)
    settings = cfg(gap=45, hi=600)
    moments = tl.segment(settings)
    check_invariants(moments, tl.utterances, tl.keyframes, settings)
    assert len(moments) == 2
    assert moments[1].ts0 == T0 + 380


def test_long_talk_is_split_at_a_strong_visual_change_between_utterances():
    tl = Timeline()
    t = 0.0
    while t < 1000:
        tl.say(t, t + 4.0)
        t += 7.0  # 3 s between utterances all the way through
    for i in range(16):
        tl.frame(i * 61.0 + 5.5)  # ordinary interval frames, also between utterances
    change = tl.frame(7.0 * 60 + 5.0, "scene", 0.9)  # walked into another room at ~7:05
    settings = cfg(gap=45, hi=600)
    moments = tl.segment(settings)
    check_invariants(moments, tl.utterances, tl.keyframes, settings)
    assert len(moments) == 2
    assert moments[1].ts0 == change.ts and moments[1].keyframe_ids[0] == change.id
    # high novelty counts the same way as an explicit scene change
    change.reason, change.novelty = "novel", HIGH_NOVELTY + 0.2
    assert tl.segment(settings)[1].ts0 == change.ts
    # ... an ordinary frame does not attract the cut: it lands near the middle instead
    change.reason, change.novelty = "interval", 0.1
    even = tl.segment(settings)
    assert len(even) == 2 and abs((even[1].ts0 - T0) - 499) < 40 and even[1].ts0 != change.ts


def test_scene_change_while_someone_is_talking_is_not_a_cut_point():
    tl = Timeline()
    tl.say(0, 400)
    tl.frame(200, "scene", 1.0)  # in the middle of the sentence
    tl.say(400.5, 800)
    moments = tl.segment(cfg(lo=0, hi=600))
    assert rel(moments) == [(0, 400), (400.5, 800)]
    assert len(moments[0].keyframe_ids) == 1


def test_one_endless_utterance_is_left_whole_even_beyond_the_maximum():
    tl = Timeline()
    u = tl.say(0, 1500)
    frames = [tl.frame(t) for t in (100.0, 700.0, 1300.0)]
    moments = tl.segment(cfg(hi=600))
    assert rel(moments) == [(0, 1500)]
    assert moments[0].utterance_ids == [u.id] and moments[0].keyframe_ids == [k.id for k in frames]


def test_short_moment_merges_into_the_closer_neighbour():
    tl = Timeline()
    tl.talk(0, 100)  # ends 98.5
    aside = tl.say(150, 155)  # 51.5 s after the first talk, 95 s before the next
    tl.talk(250, 350)
    moments = tl.segment(cfg(gap=45, lo=20))
    assert len(moments) == 2
    assert aside.id in moments[0].utterance_ids
    # the other way round
    tl2 = Timeline()
    tl2.talk(0, 100)
    aside2 = tl2.say(195, 200)
    tl2.talk(250, 350)
    moments2 = tl2.segment(cfg(gap=45, lo=20))
    assert len(moments2) == 2 and aside2.id in moments2[1].utterance_ids
    # with no minimum the aside is a moment of its own
    assert len(tl.segment(cfg(gap=45, lo=0))) == 3


def test_short_moment_is_not_merged_when_that_would_break_the_maximum():
    tl = Timeline()
    tl.talk(0, 580)
    tl.say(640, 643)
    settings = cfg(gap=45, lo=20, hi=600)
    moments = tl.segment(settings)
    assert len(moments) == 2 and moments[1].ts1 - moments[1].ts0 == 3
    check_invariants(moments, tl.utterances, tl.keyframes, settings)


def test_voice_notes_far_apart_stay_separate_but_close_ones_group():
    far = Timeline()
    for i in range(5):
        far.say(i * 300.0, i * 300.0 + 3)  # five minutes apart: nothing in between at all
    assert len(far.segment(cfg(gap=45, lo=20))) == 5
    close = Timeline()
    for i in range(6):
        close.say(i * 60.0, i * 60.0 + 3)  # a minute apart
    grouped = close.segment(cfg(gap=45, lo=20))
    assert 1 < len(grouped) < 6
    assert all(m.ts1 - m.ts0 >= 20 for m in grouped)


def test_sparse_keyframes_inside_one_clip_are_not_mistaken_for_recording_breaks():
    tl = Timeline()
    for i in range(7):  # frames.max_gap_s raised to five minutes; one continuous half-hour clip
        tl.frame(i * 300.0, clip=1)
    settings = cfg(gap=45, lo=20, hi=900)
    assert coverage_hole_seconds(settings, tl.keyframes) == 450
    moments = tl.segment(settings)
    check_invariants(moments, tl.utterances, tl.keyframes, settings)
    assert len(moments) < 7 and max(m.ts1 - m.ts0 for m in moments) <= 900
    # the default sampling (a frame a minute) leaves the threshold at two minutes / the configured gap
    dense = [Keyframe(clip_id=1, session_id=SID, t=i * 60.0, ts=T0 + i * 60.0, path="x.jpg") for i in range(5)]
    assert coverage_hole_seconds(cfg(gap=45), dense) == 120
    assert coverage_hole_seconds(cfg(gap=300), dense) == 300
    assert coverage_hole_seconds(cfg(gap=45), []) == 120


def test_frames_of_two_clips_at_the_same_instant_do_not_make_the_result_depend_on_input_order():
    # Two clips whose frames carry identical timestamps (clips overlapping in time, e.g. after a camera clock
    # reset). The hole threshold is measured inside each clip, so it cannot flip with the order of the input.
    tl = Timeline()
    for i in range(5):
        tl.frame(i * 300.0, clip=1)
        tl.frame(i * 300.0, clip=2)
    tl.say(310, 314, clip=1)
    settings = cfg(gap=45, lo=20, hi=900)
    assert coverage_hole_seconds(settings, tl.keyframes) == 450  # five minutes between frames inside either clip
    expected = tl.segment(settings)
    check_invariants(expected, tl.utterances, tl.keyframes, settings)
    # the remark with the frames around it, then the silent rest: no boundary for "the recording was off"
    assert rel(expected) == [(0, 314), (600, 1200)]
    rng = random.Random(0)
    for _ in range(25):
        shuffled = tl.keyframes[:]
        rng.shuffle(shuffled)
        assert coverage_hole_seconds(settings, shuffled) == 450
        assert segment_moments(SESSION, tl.utterances, shuffled, settings) == expected
    assert coverage_hole_seconds(settings, list(reversed(tl.keyframes))) == 450


def test_input_order_missing_ids_and_bad_timestamps_are_tolerated():
    tl = Timeline()
    a = tl.say(0, 5)
    b = tl.say(6, 11)
    k = tl.frame(3)
    backwards = tl.say(20, 12)  # end before start: treated as an instant
    nameless = Utterance(clip_id=1, session_id=SID, t0=13, t1=14, ts0=T0 + 13, ts1=T0 + 14, text="no id yet")
    broken = Utterance(clip_id=1, session_id=SID, t0=0, t1=0, ts0=float("nan"), ts1=T0, text="?", id=999)
    lost = Keyframe(clip_id=1, session_id=SID, t=0, ts=float("inf"), path="x.jpg", id=998)
    moments = segment_moments(SESSION, [backwards, nameless, b, broken, a], [lost, k], cfg())
    assert len(moments) == 1
    assert moments[0].utterance_ids == [a.id, b.id, backwards.id]  # time order; the id-less one cannot be listed
    assert moments[0].keyframe_ids == [k.id]
    assert rel(moments) == [(0, 20)]


def test_nonsense_settings_do_not_break_segmentation():
    tl = Timeline()
    tl.talk(0, 300)
    tl.talk(500, 800)
    for settings in (
        cfg(gap=0, lo=-5, hi=0),
        cfg(gap=-1, lo=50, hi=10),  # minimum above maximum
        cfg(gap=float("nan"), lo=float("nan"), hi=float("inf")),
        cfg(gap=1e-9, lo=0, hi=1e-9),
    ):
        moments = tl.segment(settings)
        assert moments
        assert sorted(i for m in moments for i in m.utterance_ids) == [u.id for u in tl.utterances]
        for a, b in pairwise(moments):
            assert a.ts1 <= b.ts0


def test_a_whole_day_of_dense_material_is_fast():
    rng = random.Random(3)
    tl = Timeline()
    t = 0.0
    while t < 6 * 3600:  # six hours of near-continuous talking
        length = rng.uniform(1.0, 5.0)
        tl.say(t, t + length)
        t += length + rng.uniform(0.0, 1.5)
    for i in range(6 * 60 * 4):
        tl.frame(i * 15.0)
    settings = cfg(gap=120, lo=30, hi=900)
    began = time.perf_counter()
    moments = tl.segment(settings)
    elapsed = time.perf_counter() - began
    assert len(tl.utterances) > 5000
    assert 24 <= len(moments) <= 40
    assert max(m.ts1 - m.ts0 for m in moments) <= 900
    assert elapsed < 20, f"segmenting took {elapsed:.1f}s"
