"""Keyframe selection and frame extraction (videonotes.media.keyframes).

Three layers are tested:

* pure pieces (settings clamping, geometry, argv builder, parsers, measures);
* the streaming selector, fed synthetic numpy frames with scripted sharpness;
* the real thing end to end, on the shared demo clip and small purpose-made lavfi clips.
"""

from __future__ import annotations

import math
import subprocess
import sys
import textwrap
import time
from pathlib import Path

import numpy as np
import pytest

from videonotes.config import FrameSettings
from videonotes.demo import DEMO_SCENES
from videonotes.media import ffmpeg as ff
from videonotes.media import keyframes as K
from videonotes.media.keyframes import FrameCandidate, extract_frames, select_keyframes  # noqa: F401

needs_ffmpeg = pytest.mark.skipif(not ff.have_ffmpeg(), reason="ffmpeg not installed")

H, W = 180, 320  # thumbnail size the selector normally sees


# =====================================================================================
# helpers
# =====================================================================================


M = 64  # margin around the thumbnail-sized centre of a canvas, so views can be shifted


def canvas(seed: int, block: int = 12) -> np.ndarray:
    """A random blocky picture, larger than the thumbnail so it can be shifted."""
    rng = np.random.default_rng(seed)
    coarse = rng.integers(30, 226, size=((H + 2 * M) // block + 1, (W + 2 * M) // block + 1)).astype(np.float32)
    return np.kron(coarse, np.ones((block, block), np.float32))[: H + 2 * M, : W + 2 * M]


def view(
    picture: np.ndarray, dx: int = 0, dy: int = 0, *, gain: float = 1.0, offset: float = 0.0, noise: int | None = None
) -> np.ndarray:
    """What the camera sees of ``picture``: shifted, exposure changed, with sensor noise."""
    assert abs(dx) <= M and abs(dy) <= M
    crop = picture[M + dy : M + dy + H, M + dx : M + dx + W] * gain + offset
    if noise is not None:
        crop = crop + np.random.default_rng(noise).normal(0.0, 2.0, crop.shape)
    return np.clip(crop, 0, 255).astype(np.uint8)


def run_selector(
    frames: list[tuple[np.ndarray, float]], cfg: FrameSettings | None = None, *, fps: float = 2.0, budget: bool = True
) -> list[FrameCandidate]:
    """Push ``(thumbnail, sharpness)`` pairs spaced 1/fps apart through the selector."""
    params = K._Params.from_settings(cfg or FrameSettings())
    selector = K._Selector(params)
    for i, (gray, sharp) in enumerate(frames):
        selector.push(i / fps, gray, sharp)
    out = selector.finish()
    if not budget or selector.t_first is None or selector.t_last is None:
        return out
    return K._apply_budget(out, selector.t_last - selector.t_first + params.period, params, start=selector.t_first)


def gaps(cands: list[FrameCandidate]) -> list[float]:
    return [b.t - a.t for a, b in zip(cands, cands[1:], strict=False)]


def lavfi(out: Path, source: str, *args: str, vf: str | None = None, codec: tuple[str, ...] | None = None) -> Path:
    """Render a small clip from an ffmpeg lavfi source."""
    cmd = ["-f", "lavfi", "-i", source]
    if vf:
        cmd += ["-vf", vf]
    cmd += list(codec) if codec is not None else ["-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p"]
    ff.run([*cmd, *args, str(out)], timeout=300)
    return out


def mean_rgb(image: Path, tmp: Path) -> tuple[float, float, float]:
    raw = tmp / (image.stem + ".rgb")
    ff.run(["-i", str(image), "-vf", "scale=16:16:flags=area", "-f", "rawvideo", "-pix_fmt", "rgb24", str(raw)], timeout=120)
    r, g, b = np.fromfile(raw, dtype=np.uint8).reshape(-1, 3).mean(axis=0)
    return float(r), float(g), float(b)


def mean_gray(image: Path, tmp: Path) -> float:
    raw = tmp / (image.stem + ".gray")
    ff.run(["-i", str(image), "-f", "rawvideo", "-pix_fmt", "gray", str(raw)], timeout=120)
    return float(np.fromfile(raw, dtype=np.uint8).mean())


def image_size(image: Path) -> tuple[int, int]:
    info = ff.probe(image)
    assert info.width and info.height
    return info.width, info.height


def scene_at(t: float) -> str:
    start = 0.0
    for scene in DEMO_SCENES:
        if start <= t < start + scene.duration:
            return scene.name
        start += scene.duration
    return DEMO_SCENES[-1].name


# =====================================================================================
# settings, geometry, command, parsers
# =====================================================================================


def test_params_defaults_pass_through():
    p = K._Params.from_settings(FrameSettings())
    assert (p.fps, p.width, p.threshold, p.window_s, p.min_gap_s, p.max_gap_s, p.max_per_minute) == (
        2.0, 320, 0.25, 1.5, 2.0, 60.0, 8.0,
    )  # fmt: skip
    assert p.period == 0.5


def test_params_clamp_zero_negative_and_nonsense():
    cfg = FrameSettings(
        analysis_fps=0, analysis_width=-5, novelty_threshold=-1, sharpness_window_s=-3, min_gap_s=-2, max_gap_s=0,
        max_per_minute=-4,
    )  # fmt: skip
    p = K._Params.from_settings(cfg)
    assert p.fps == 2.0 and p.width == 320  # nonsense -> built-in default
    assert 0 < p.threshold <= 1 and p.window_s == 0 and p.min_gap_s == 0
    assert math.isinf(p.max_gap_s)  # 0 = no keep-alive frames
    assert p.max_per_minute == 0  # 0 = no budget

    cfg = FrameSettings(analysis_fps=float("nan"), analysis_width=10**9, novelty_threshold=7.0, max_gap_s=1.0, min_gap_s=5.0)
    cfg.max_per_minute = "lots"  # type: ignore[assignment]
    p = K._Params.from_settings(cfg)
    assert p.fps == 2.0 and p.width == 1920 and p.threshold == 1.0
    assert p.max_gap_s >= p.min_gap_s + p.period  # a keep-alive can never undercut the minimum gap
    # ... nor come more often than the budget pays for
    assert K._Params.from_settings(FrameSettings(max_gap_s=60, max_per_minute=0.5)).max_gap_s == 120.0
    assert p.max_per_minute == 8.0
    assert K._Params.from_settings(FrameSettings(analysis_fps=1000)).fps == 30.0


@pytest.mark.parametrize(
    ("size", "width", "expected"),
    [
        ((1920, 1080), 320, (320, 180, 640, 360)),
        ((3840, 2160), 320, (320, 180, 960, 540)),  # focus frame capped for 4K
        ((1080, 1920), 320, (320, 568, 360, 640)),  # portrait
        ((1280, 720), 320, (320, 180, 426, 240)),
        ((641, 361), 320, (320, 180, 320, 180)),  # odd-sized source
        ((641, 361), 2000, (640, 360, 640, 360)),  # never wider than the source
        ((200, 100), 320, (200, 100, 200, 100)),
        ((10, 10), 320, (16, 16, 16, 16)),  # floor
        (None, 320, (320, 180, 640, 360)),  # size unknown: assume 16:9
    ],
)
def test_analysis_geometry(size, width, expected):
    g = K.analysis_geometry(size, width)
    assert (g.width, g.height, g.sharp_width, g.sharp_height) == expected
    assert all(v % 2 == 0 for v in expected)
    assert g.sharp_width >= g.width  # the thumbnail is padded to the focus frame's width
    assert g.frame_bytes == g.sharp_width * (g.sharp_height + g.height)


def test_analysis_geometry_extreme_aspect_stays_bounded():
    g = K.analysis_geometry((16, 20000), 320)
    assert g.height <= 8 * g.width and g.sharp_height <= 8 * g.sharp_width and g.frame_bytes < 10**6


def test_display_size_respects_rotation(tmp_path):
    info = ff.MediaInfo(path=tmp_path / "x.mp4", has_video=True, width=1920, height=1080, rotation=90)
    assert K.display_size(info) == (1080, 1920)
    info.rotation = 270
    assert K.display_size(info) == (1080, 1920)
    info.rotation = 180
    assert K.display_size(info) == (1920, 1080)
    info.width = None
    assert K.display_size(info) is None


def test_analysis_command_shape(monkeypatch):
    monkeypatch.setattr(ff, "ffmpeg_bin", lambda: "/opt/homebrew/bin/ffmpeg")
    g = K.analysis_geometry((1920, 1080), 320)
    cmd = K.analysis_command("clips/a b.mp4", g, analysis_fps=2.0, source_fps=30.0, hwaccel="videotoolbox")
    assert cmd[0] == "/opt/homebrew/bin/ffmpeg" and "-nostdin" in cmd and "-nostats" in cmd
    i = cmd.index("-i")
    assert cmd[cmd.index("-hwaccel") + 1] == "videotoolbox" and cmd.index("-hwaccel") < i  # an input option
    assert Path(cmd[i + 1]).is_absolute() and cmd[i + 1].endswith("a b.mp4")
    graph = cmd[cmd.index("-filter_complex") + 1]
    assert "[0:V:0]select=" in graph and "showinfo" in graph and "format=gray" in graph
    assert "gte(t-prev_selected_t,0.483333)" in graph  # every 15th frame of 30 fps, with half a frame of slack
    assert "scale=320:180:flags=area,pad=640:180" in graph and "scale=640:360:flags=neighbor" in graph
    assert cmd[cmd.index("-fps_mode") + 1] == "passthrough"  # or ffmpeg duplicates frames to refill the rate
    assert cmd[-5:] == ["-f", "rawvideo", "-pix_fmt", "gray", "pipe:1"]
    assert "-an" in cmd and "-loglevel" in cmd

    software = K.analysis_command("a.mp4", g, analysis_fps=2.0, source_fps=None)
    assert "-hwaccel" not in software
    # low frame-rate sources: the slack never eats more than a quarter of the sampling period
    slow = K.analysis_command("a.mp4", g, analysis_fps=2.0, source_fps=1.0)
    assert "gte(t-prev_selected_t,0.375000)" in slow[slow.index("-filter_complex") + 1]


def test_parse_showinfo_lines():
    old = "[Parsed_showinfo_1 @ 0x55e1] [info] n:   7 pts: 324324 pts_time:10810.8 duration:    512 fmt:yuv420p"
    assert K.parse_showinfo(old) == (324324, 10810.8)
    new = "[Parsed_showinfo_1 @ 0x1] n:1234 pts:162162000 pts_time:10810.8 duration:   1001 duration_time:0.033367"
    assert K.parse_showinfo(new) == (162162000, 10810.8)
    assert K.parse_showinfo("[Parsed_showinfo_1 @ 0x1] n:   0 pts:  NOPTS pts_time:NOPTS duration: 1") == (None, None)
    assert K.parse_showinfo("[Parsed_showinfo_1 @ 0x1] n:   3 pts:     -5 pts_time:-0.01 ") == (-5, -0.01)
    assert K.parse_showinfo("[Parsed_showinfo_1 @ 0x1] config in time_base: 1/15360, frame_rate: 30/1") is None
    assert K.parse_showinfo("[h264 @ 0x1] [error] error while decoding MB 12 3") is None
    assert K.parse_timebase("[Parsed_showinfo_1 @ 0x1] [info] config in time_base: 1/15360, frame_rate: 30/1") == 1 / 15360
    assert K.parse_timebase("[Parsed_showinfo_1 @ 0x1] config in time_base: 1001/30000, frame_rate: 0/0") == 1001 / 30000
    assert K.parse_timebase("config in time_base: 0/0") is None
    assert K.parse_timebase("something else") is None


def test_frame_filename():
    assert K.frame_filename(0.0) == "kf_000000000.jpg"
    assert K.frame_filename(12.3456) == "kf_000012346.jpg"
    assert K.frame_filename(3723.5, "clip7") == "clip7_003723500.jpg"
    assert K.frame_filename(-4.0) == "kf_000000000.jpg"


# =====================================================================================
# measures
# =====================================================================================


def test_sharpness_ranks_blur_below_sharp():
    sharp = view(canvas(1))
    f = sharp.astype(np.float32)
    blurred = ((f + np.roll(f, 1, 0) + np.roll(f, -1, 0) + np.roll(f, 1, 1) + np.roll(f, -1, 1)) / 5).astype(np.uint8)
    assert K.sharpness(sharp) > 3 * K.sharpness(blurred) > 0
    assert K.sharpness(np.full((H, W), 90, np.uint8)) == 0.0
    assert K.sharpness(np.zeros((2, 2), np.uint8)) == 0.0  # too small to have a Laplacian


def test_is_usable():
    rng = np.random.default_rng(0)
    assert K.is_usable(view(canvas(2)))
    assert not K.is_usable(rng.integers(0, 12, (H, W)).astype(np.uint8))  # lens cap, noisy black
    assert not K.is_usable(rng.integers(244, 256, (H, W)).astype(np.uint8))  # blown out
    assert not K.is_usable(np.full((H, W), 128, np.uint8))  # featureless
    dark_sign = np.full((H, W), 20, np.uint8)
    dark_sign[80:96, 40:140] = 230  # a lit sign at night is still worth keeping
    assert K.is_usable(dark_sign)
    whiteboard = np.full((H, W), 240, np.uint8)
    whiteboard[40:44, 30:200] = 40
    assert K.is_usable(whiteboard)
    assert not K.is_usable(np.zeros((0, 0), np.uint8))


def novelty(a: np.ndarray, b: np.ndarray) -> float:
    cmp = K._Comparer(a.shape)
    return cmp.novelty(K._Frame(0.0, 1.0, a, True), K._Frame(0.5, 1.0, b, True))


def test_novelty_scale():
    a = canvas(3)
    assert novelty(view(a), view(a)) == 0.0
    assert novelty(view(a), view(a, noise=1)) < 0.1
    assert novelty(view(a), view(canvas(4))) > 0.9  # a different place
    # a new object covering a twentieth of the picture is clearly "novel" at the default threshold
    edited = a.copy()
    edited[M + 60 : M + 100, M + 100 : M + 172] = 255 - edited[M + 60 : M + 100, M + 100 : M + 172]
    assert 0.2 < novelty(view(a), view(edited)) < K._SCENE_NOVELTY
    # ... and one tile changing is not
    edited = a.copy()
    edited[M + 64 : M + 80, M + 96 : M + 112] += 60
    assert novelty(view(a), view(edited)) < 0.2


@pytest.mark.parametrize(("dx", "dy"), [(3, 0), (-7, 4), (20, -11), (-45, 9), (0, 30)])
def test_novelty_ignores_camera_shake(dx, dy):
    a = canvas(5)
    unaligned = K._changed_fraction(
        K._tile_means(view(a), 16).astype(np.float64), K._tile_means(view(a, dx, dy), 16).astype(np.float64)
    )
    assert novelty(view(a, noise=1), view(a, dx, dy, noise=2)) < 0.15
    if max(abs(dx), abs(dy)) >= 7:
        assert unaligned > 0.2  # ... which is the alignment's doing: tile for tile these differ a lot


def test_novelty_does_not_align_away_a_real_change():
    assert novelty(view(canvas(6)), view(canvas(7), 5, 5)) > 0.9
    # a shift larger than the tolerated 30 % of the frame is a new view
    assert novelty(view(canvas(6), -30, 0), view(canvas(6), 31, 0)) < 0.15
    wide = np.concatenate([canvas(8), canvas(9)], axis=1)
    assert novelty(wide[M : M + H, 0:W].astype(np.uint8), wide[M : M + H, 200 : 200 + W].astype(np.uint8)) > 0.5


@pytest.mark.parametrize(
    ("gain", "offset"),
    [(1.0, 18.0), (1.0, -25.0), (1.25, 0.0), (0.8, 0.0), (1.4, 0.0)],
)
def test_novelty_ignores_exposure_flicker(gain, offset):
    a = canvas(10) * 0.6 + 30  # keep clear of clipping so the change is a pure exposure change
    assert novelty(view(a, noise=1), view(a, gain=gain, offset=offset, noise=2)) < 0.15


def test_novelty_sees_big_brightness_jumps():
    a = canvas(11) * 0.3 + 20
    assert novelty(view(a), view(a, offset=120.0)) > 0.9  # lights on: not flicker
    assert novelty(view(a), view(a, gain=3.0)) > 0.5


def test_novelty_on_tiny_frames():
    rng = np.random.default_rng(1)
    a = rng.integers(0, 255, (16, 16)).astype(np.uint8)
    b = rng.integers(0, 255, (16, 16)).astype(np.uint8)
    assert novelty(a, a) == 0.0 and novelty(a, b) > 0.5
    one = np.full((2, 2), 7, np.uint8)
    assert novelty(one, one) == 0.0


# =====================================================================================
# selector on synthetic frames
# =====================================================================================


def test_selector_single_frame_gives_exactly_one_first():
    out = run_selector([(view(canvas(1)), 50.0)])
    assert [(c.t, c.reason, c.novelty) for c in out] == [(0.0, "first", 1.0)]
    assert run_selector([]) == []


def test_selector_first_is_the_sharpest_of_the_opening_window():
    a = canvas(1)
    frames = [(view(a, noise=i), s) for i, s in enumerate([10, 40, 90, 60, 500, 500, 500, 500])]
    out = run_selector(frames)
    assert [(c.t, c.reason) for c in out] == [(1.0, "first")]  # 500 comes after the 1.5 s window
    assert out[0].sharpness == 90
    # near-ties go to the earliest frame
    out = run_selector([(view(a, noise=i), s) for i, s in enumerate([100, 104, 103, 101, 100, 100])])
    assert [(c.t, c.reason) for c in out] == [(0.0, "first")]


def test_selector_static_scene_only_gets_keep_alive_frames():
    a = canvas(2)
    frames = [(view(a, noise=i), 100.0 + (i % 5)) for i in range(2 * 60 * 5)]  # five minutes
    out = run_selector(frames)
    assert [c.reason for c in out] == ["first"] + ["interval"] * (len(out) - 1)
    assert 4 <= len(out) - 1 <= 6  # about one a minute, not one every sample
    assert max(gaps(out)) <= 60.0 and min(gaps(out)) >= 40.0
    assert all(c.novelty < 0.2 for c in out[1:])


def test_selector_keep_alive_takes_the_sharpest_of_the_recent_stretch():
    a = canvas(2)
    sharp = [100.0] * 600
    sharp[110] = 200.0  # t = 55 s: inside the 15 s before the 60 s deadline
    sharp[60] = 300.0  # t = 30 s: sharper still, but too far back to hold in memory for
    out = run_selector([(view(a, noise=i), s) for i, s in enumerate(sharp)])
    assert (out[1].t, out[1].reason, out[1].sharpness) == (55.0, "interval", 200.0)


def test_selector_no_keep_alive_when_disabled():
    a = canvas(2)
    frames = [(view(a, noise=i), 100.0) for i in range(600)]
    out = run_selector(frames, FrameSettings(max_gap_s=0))
    assert [c.reason for c in out] == ["first"]


def test_selector_scene_change_takes_sharpest_settled_frame_not_the_transition():
    a, b = canvas(3), canvas(4)
    frames = [(view(a, noise=i), 100.0) for i in range(20)]  # 0 .. 9.5 s
    #            t=10 (transition)  10.5   11.0   11.5   12.0   12.5   13.0 ...
    after = [900.0, 50.0, 60.0, 300.0, 80.0, 70.0, 999.0, 999.0, 999.0, 999.0]
    frames += [(view(b, noise=100 + i), s) for i, s in enumerate(after)]
    out = run_selector(frames)
    assert [(c.t, c.reason) for c in out] == [(0.0, "first"), (11.5, "scene")]
    assert out[1].sharpness == 300.0 and out[1].novelty > 0.9
    # the transition frame (sharpest of all) was not taken, nor the frames past the window


def test_selector_waits_out_a_blurred_stretch_after_a_change():
    a, b = canvas(3), canvas(4)
    frames = [(view(a, noise=i), 400.0) for i in range(10)]
    # the new view arrives sharp for one frame, then smeared for 4 s, then holds sharp
    sharp = [400.0] + [30.0] * 8 + [420.0, 410.0] + [400.0] * 10
    frames += [(view(b, noise=50 + i), s) for i, s in enumerate(sharp)]
    out = run_selector(frames)
    assert [(c.reason, c.sharpness) for c in out] == [("first", 400.0), ("scene", 420.0)]


def test_selector_takes_a_blurred_frame_when_nothing_better_comes():
    a, b = canvas(3), canvas(4)
    frames = [(view(a, noise=i), 400.0) for i in range(10)]
    frames += [(view(b, noise=50), 400.0)] + [(view(b, noise=51 + i), 30.0 + i % 3) for i in range(60)]
    out = run_selector(frames)
    assert [c.reason for c in out[:2]] == ["first", "scene"]
    assert 5.0 < out[1].t <= 5.0 + K._MOTION_GAP_S + 0.5 and out[1].sharpness <= 32.0


def test_selector_gradual_change_is_novel_not_scene():
    a = canvas(5)
    grown = a.copy()
    frames = []
    for i in range(80):  # an object slowly grows into the picture over 20 s, then stays
        width = min(i, 40) * 4
        grown[M + 40 : M + 140, M : M + width] = 250
        frames.append((view(grown, noise=i), 100.0))
    out = run_selector(frames)
    assert out[0].reason == "first"
    assert len(out) >= 2 and all(c.reason == "novel" for c in out[1:])
    assert all(c.novelty >= 0.2 for c in out[1:])


def test_selector_slow_drift_eventually_triggers():
    wide = np.kron(np.random.default_rng(7).integers(30, 226, (20, 200)).astype(np.float32), np.ones((12, 12), np.float32))
    frames = [(wide[:H, x : x + W].astype(np.uint8), 100.0) for x in range(0, 1600, 4)]  # 2 px per second
    out = run_selector(frames, FrameSettings(max_gap_s=0))
    assert len(out) >= 4 and all(c.reason == "novel" for c in out[1:])


def test_selector_shake_and_flicker_do_not_trigger():
    a = canvas(6) * 0.6 + 30
    rng = np.random.default_rng(3)
    frames = []
    for i in range(240):  # two minutes of a hand-held, flickering view of one thing
        dx, dy = int(rng.integers(-9, 10)), int(rng.integers(-6, 7))
        frames.append((view(a, dx, dy, gain=float(rng.uniform(0.85, 1.2)), offset=float(rng.uniform(-12, 12)), noise=i), 100.0))
    out = run_selector(frames)
    assert [c.reason for c in out] == ["first", "interval"]


def test_selector_glancing_back_is_not_new():
    a, b = canvas(8), canvas(9)
    frames = []
    for k in range(8):  # 8 s at the screen, 8 s at the notebook, and back, four times over
        frames += [(view(a if k % 2 == 0 else b, noise=10 * k + i), 100.0) for i in range(16)]
    out = run_selector(frames)
    assert [c.reason for c in out][:2] == ["first", "scene"]
    assert len(out) <= 3  # the two views (plus at most one keep-alive), not eight
    without_memory = [c for c in out if c.reason == "scene"]
    assert len(without_memory) == 1


def test_selector_unusable_frames_are_not_chosen_for_novelty():
    a = canvas(10)
    black = np.random.default_rng(0).integers(0, 10, (H, W)).astype(np.uint8)
    frames = [(view(a, noise=i), 100.0) for i in range(20)]
    frames += [(black, 5000.0)] * 40  # 20 s in a pocket: compression noise makes it look "sharp"
    frames += [(view(a, noise=99 + i), 100.0) for i in range(20)]
    out = run_selector(frames)
    assert [c.reason for c in out] == ["first"]

    # ... but a covered lens still gets its keep-alive frames, the least bad available
    out = run_selector([(black, 5.0)] * 400)
    assert [c.reason for c in out] == ["first", "interval", "interval", "interval"]

    # and the first usable picture after darkness is a new scene
    out = run_selector([(black, 5.0)] * 20 + [(view(a, noise=i), 100.0) for i in range(20)])
    assert [c.reason for c in out] == ["first", "scene"] and out[1].t >= 10.5


def test_selector_relatively_blurred_frames_lose_to_plain_ones():
    a = canvas(11)
    frames = [(view(a, noise=i), 400.0) for i in range(100)]  # 50 s sharp
    frames += [(view(a, noise=200 + i), 40.0) for i in range(40)]  # then the wearer fidgets: all smeared
    out = run_selector(frames)
    assert [c.reason for c in out] == ["first", "interval"]
    assert out[1].sharpness == 400.0  # the keep-alive due at 60 s reached back to the last sharp frame


def test_selector_takes_another_frame_when_the_view_gets_much_sharper():
    a = canvas(12)
    frames = [(view(a, noise=i), 40.0) for i in range(40)]  # out of focus for 20 s ...
    frames += [(view(a, noise=100 + i), s) for i, s in enumerate([400.0, 450.0, 420.0, 400.0] + [400.0] * 20)]
    out = run_selector(frames)
    assert [(c.reason, c.sharpness) for c in out] == [("first", 40.0), ("interval", 450.0)]
    assert out[1].novelty < 0.2


def test_selector_min_gap_and_budget():
    pictures = [canvas(20 + k) for k in range(40)]
    frames = []
    for k, picture in enumerate(pictures):  # a new scene every 3 s for two minutes
        frames += [(view(picture, noise=10 * k + i), 100.0) for i in range(6)]
    cfg = FrameSettings(min_gap_s=2.0, max_per_minute=8.0)
    unlimited = run_selector(frames, cfg, budget=False)
    assert len(unlimited) > 16 and min(gaps(unlimited)) >= 2.0
    out = run_selector(frames, cfg)
    assert len(out) <= 16 and out[0].reason == "first"  # 8 a minute over two minutes
    assert min(gaps(out)) >= 2.0
    wide = run_selector(frames, FrameSettings(min_gap_s=7.0, max_per_minute=0))
    assert min(gaps(wide)) >= 7.0 and len(wide) >= 10
    assert [c.t for c in out] == sorted(c.t for c in out)
    assert {c.reason for c in unlimited} <= set(K.REASONS)


def test_selector_continuous_motion_is_paced():
    wide = np.kron(np.random.default_rng(5).integers(30, 226, (20, 700)).astype(np.float32), np.ones((12, 12), np.float32))
    frames = [(wide[:H, x : x + W].astype(np.uint8), 100.0) for x in range(0, 7200, 30)]  # walking pace: 60 px/s
    out = run_selector(frames, budget=False)
    per_minute = len(out) / (len(frames) / 2 / 60)
    assert 3 <= per_minute <= 9, per_minute  # some coverage of the walk, nowhere near one per sample
    assert {c.reason for c in out[1:]} <= {"novel", "scene"}


@pytest.mark.parametrize(
    "cfg",
    [
        FrameSettings(analysis_fps=0, analysis_width=0, novelty_threshold=0, sharpness_window_s=0, min_gap_s=0, max_gap_s=0,
                      max_per_minute=0),
        FrameSettings(analysis_fps=-1, analysis_width=-1, novelty_threshold=-1, sharpness_window_s=-1, min_gap_s=-1,
                      max_gap_s=-1, max_per_minute=-1),
        FrameSettings(novelty_threshold=0, min_gap_s=0, max_gap_s=0.001, sharpness_window_s=0, max_per_minute=1e9),
        FrameSettings(novelty_threshold=5, min_gap_s=1e6, max_gap_s=1e-9, sharpness_window_s=1e6),
        FrameSettings(max_per_minute=1e-6, max_gap_s=1.0),
    ],
)  # fmt: skip
def test_selector_survives_degenerate_settings(cfg):
    pictures = [canvas(k) for k in range(6)]
    frames = []
    for k in range(30):
        frames += [(view(pictures[k % 6], k % 5, 0, noise=k * 7 + i), 50.0 + i) for i in range(5)]
    started = time.monotonic()
    out = run_selector(frames, cfg)
    assert time.monotonic() - started < 30
    params = K._Params.from_settings(cfg)
    assert out and out[0].reason == "first"
    assert [c.t for c in out] == sorted({c.t for c in out})  # ascending, no repeats
    assert all(c.reason in K.REASONS and 0.0 <= c.novelty <= 1.0 for c in out)
    if len(out) > 1:
        assert min(gaps(out)) >= params.min_gap_s - 1e-6
    if params.max_per_minute > 0:
        assert len(out) <= max(1, math.ceil(params.max_per_minute * (len(frames) / 2) / 60))


def test_selector_ignores_frames_whose_time_goes_backwards():
    a = canvas(1)
    selector = K._Selector(K._Params.from_settings(FrameSettings()))
    for t in [0.0, 0.5, 1.0, 0.2, 1.0, float("nan"), 1.5, 2.0]:
        selector.push(t, view(a), 10.0)
    assert selector.n_frames == 5 and selector.n_out_of_order == 3
    assert [c.reason for c in selector.finish()] == ["first"]


def test_selector_memory_stays_bounded():
    """An hour of footage must not make the selector hold on to an hour of frames."""
    pictures = [canvas(k) for k in range(12)]
    selector = K._Selector(K._Params.from_settings(FrameSettings()))
    for i in range(7200):
        selector.push(i * 0.5, view(pictures[(i // 45) % 12], i % 3, 0), 100.0 + i % 7)
    held = len(selector._pool) + len(selector._refs) + len(selector._sharp_hist)
    assert held < 100
    assert len(selector.finish()) < 500


# =====================================================================================
# budget
# =====================================================================================


def cands(*items: tuple[float, float, str]) -> list[FrameCandidate]:
    return [FrameCandidate(t, 100.0, nov, reason) for t, nov, reason in items]


def budget_params(**kw) -> K._Params:
    return K._Params.from_settings(FrameSettings(**kw))


def test_budget_keeps_first_and_the_most_novel():
    picked = cands((0, 1.0, "first"), (10, 0.9, "scene"), (20, 0.3, "novel"), (30, 0.8, "scene"), (40, 0.25, "novel"),
                   (50, 0.6, "novel"))  # fmt: skip
    out = K._apply_budget(picked, 60.0, budget_params(max_per_minute=3))
    assert [c.t for c in out] == [0, 10, 30]
    out = K._apply_budget(picked, 60.0, budget_params(max_per_minute=1))
    assert [c.reason for c in out] == ["first"]  # "first" survives even when it is the only one allowed
    assert K._apply_budget(picked, 60.0, budget_params(max_per_minute=6)) == picked
    assert K._apply_budget(picked, 60.0, budget_params(max_per_minute=0)) == picked  # no budget
    assert len(K._apply_budget(picked, 61.0, budget_params(max_per_minute=3))) == 4  # a started minute counts


def test_budget_prefers_dropping_frames_that_leave_no_hole():
    # A busy first minute, then a quiet stretch covered only by keep-alive frames.
    picked = cands((0, 1.0, "first"), (10, 0.5, "novel"), (20, 0.6, "novel"), (30, 0.7, "novel"), (40, 0.55, "novel"),
                   (100, 0.05, "interval"), (160, 0.04, "interval"), (220, 0.03, "interval"))  # fmt: skip
    out = K._apply_budget(picked, 240.0, budget_params(max_per_minute=1.5, max_gap_s=60))  # allows 6
    assert len(out) == 6
    assert [c.t for c in out if c.reason == "interval"] == [100, 160, 220]  # the least novel, but they stay
    # 10 s goes (least novel of the busy minute); 40 s stays although 20 s is more novel,
    # because without it nothing would cover the 70 s from 30 s to 100 s
    assert [c.t for c in out][:3] == [0, 30, 40]
    # when the budget cannot afford the coverage, the most novel simply win
    out = K._apply_budget(picked, 240.0, budget_params(max_per_minute=0.5, max_gap_s=60))  # allows 2
    assert [c.t for c in out] == [0, 30]
    out = K._apply_budget(picked, 240.0, budget_params(max_per_minute=0.75, max_gap_s=60))  # allows 3
    assert [c.t for c in out] == [0, 20, 30]


def test_budget_pass_enforces_min_gap():
    picked = cands((0, 1.0, "first"), (0.5, 0.9, "scene"), (3.0, 0.3, "novel"), (3.5, 0.8, "scene"), (9.0, 0.4, "novel"))
    out = K._apply_budget(picked, 10.0, budget_params(min_gap_s=2.0, max_per_minute=0))
    assert [c.t for c in out] == [0, 3.5, 9.0]  # "first" beats its neighbour; otherwise the more novel stays
    assert K._apply_budget([], 10.0, budget_params()) == []


# =====================================================================================
# the ffmpeg boundary, with a stand-in process
# =====================================================================================

FAKE = textwrap.dedent(
    """
    import sys, time
    frame, count, mode = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    err, out = sys.stderr, sys.stdout.buffer
    err.write("Input #0, mov, from 'x.mp4':\\n")
    err.write("[Parsed_showinfo_1 @ 0x1] [info] config in time_base: 1001/30000, frame_rate: 30000/1001\\n")
    for i in range(count):
        if mode != "nostamps":
            # pts_time deliberately useless: only pts x time_base is exact
            err.write(f"[Parsed_showinfo_1 @ 0x1] [info] n:{i:4d} pts:{i * 15:7d} pts_time:9e3 duration: 1\\n")
            err.write("[Parsed_showinfo_1 @ 0x1] [info]   side data - User Data Unregistered: " + "ab" * 3000 + "\\n")
        err.flush()
        out.write(bytes([i % 251]) * frame)
        out.flush()
        if mode == "hang" and i == 1:
            time.sleep(120)
    if mode == "partial":
        out.write(b"x" * (frame // 2))
    if mode == "fail":
        err.write("[h264 @ 0x2] [error] error while decoding MB 3 4\\n")
        err.write("[in#0 @ 0x3] [fatal] Error opening input: Invalid data found when processing input\\n")
        sys.exit(187)
    """
)


def fake_cmd(tmp_path: Path, frame: int, count: int, mode: str = "ok") -> list[str]:
    script = tmp_path / "fake_ffmpeg.py"
    script.write_text(FAKE)
    return [sys.executable, str(script), str(frame), str(count), mode]


def test_stream_pairs_frames_with_exact_timestamps(tmp_path):
    with K._FrameStream(fake_cmd(tmp_path, 4096, 40), 4096, period=0.5) as stream:
        got = [(t, bytes(buf[:1]), len(buf)) for t, buf in stream]
    assert len(got) == 40 and stream.frames == 40 and stream.returncode == 0
    assert [g[1][0] for g in got] == list(range(40)) and {g[2] for g in got} == {4096}
    assert got[7][0] == pytest.approx(7 * 15 * 1001 / 30000, abs=1e-9)  # pts x time base, not the rounded pts_time
    assert stream.guessed_times == 0


def test_stream_estimates_missing_timestamps_and_drops_partial_frame(tmp_path):
    with K._FrameStream(fake_cmd(tmp_path, 1000, 3, "nostamps"), 1000, period=0.5) as stream:
        times = [t for t, _ in stream]
    assert times == [0.0, 0.5, 1.0] and stream.guessed_times == 3
    with K._FrameStream(fake_cmd(tmp_path, 1000, 3, "partial"), 1000, period=0.5) as stream:
        assert len(list(stream)) == 3  # the half-written fourth frame is not delivered


def test_stream_reports_ffmpeg_errors(tmp_path):
    with K._FrameStream(fake_cmd(tmp_path, 1000, 2, "fail"), 1000, period=0.5) as stream:
        assert len(list(stream)) == 2
    assert stream.returncode == 187
    text = stream.error_text()
    assert "Invalid data found" in text and "error while decoding" in text
    assert "[fatal]" not in text and "Input #0" not in text  # just what went wrong, without log decoration


def test_stream_stops_a_hung_process(tmp_path):
    started = time.monotonic()
    with pytest.raises(ff.FFmpegError, match="produced no video for"):
        with K._FrameStream(fake_cmd(tmp_path, 1000, 5, "hang"), 1000, period=0.5, stall_timeout=1.0) as stream:
            for _ in stream:
                pass
    assert time.monotonic() - started < 60
    assert stream.returncode is not None  # terminated and reaped, not left behind


@pytest.mark.parametrize("error", [KeyboardInterrupt, RuntimeError])
def test_stream_reaps_process_when_the_consumer_stops(tmp_path, error):
    procs: list[subprocess.Popen] = []
    real_popen = subprocess.Popen

    def spy(*args, **kwargs):
        procs.append(real_popen(*args, **kwargs))
        return procs[-1]

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(K.subprocess, "Popen", spy)
        with pytest.raises(error):
            with K._FrameStream(fake_cmd(tmp_path, 1000, 10**6), 1000, period=0.5) as stream:
                for i, _ in enumerate(stream):
                    if i == 3:
                        raise error()
    assert len(procs) == 1 and procs[0].returncode is not None
    assert procs[0].stdout.closed and procs[0].stderr.closed


def test_stream_missing_binary_is_a_helpful_error(tmp_path):
    with pytest.raises(ff.FFmpegError, match="brew install ffmpeg"):
        with K._FrameStream([str(tmp_path / "no-such-ffmpeg")], 100, period=0.5):
            pass


# =====================================================================================
# end to end: select_keyframes
# =====================================================================================

RAMP_FPS = 30
RAMP_FRAMES = 105
RAMP_LUMA = "geq=lum='16+2*N':cb=128:cr=128"  # frame N is a flat gray, two (limited-range) luma steps per frame
RAMP_STEP = 2.0 * 255.0 / 219.0  # ... which is this many gray levels once expanded to full range


def ramp_index(image: Path, tmp: Path) -> int:
    """Which frame of a ramp clip an image shows (frame N is a flat gray of level N * RAMP_STEP)."""
    return int(round(mean_gray(image, tmp) / RAMP_STEP))


@pytest.fixture(scope="module")
def clips(tmp_path_factory) -> dict[str, Path]:
    """Small purpose-made clips (rendered once per test module)."""
    if not ff.have_ffmpeg():
        pytest.skip("ffmpeg not installed")
    d = tmp_path_factory.mktemp("kfclips")
    c: dict[str, Path] = {}
    ramp_vf = RAMP_LUMA + ",format=yuv420p"
    lossless = ("-c:v", "libx264", "-preset", "ultrafast", "-qp", "0", "-g", "50", "-pix_fmt", "yuv420p")
    # every frame is a flat gray that encodes its own index: frame N shows at t = N / 30
    c["ramp"] = lavfi(d / "ramp.mp4", "color=c=black:s=320x240:r=30:d=3.5", vf=ramp_vf, codec=lossless)
    # the same with frames dropped irregularly but timestamps kept: variable frame rate
    c["vfr"] = lavfi(
        d / "vfr.mkv", "color=c=black:s=320x240:r=30:d=3.5", "-fps_mode", "vfr",
        vf=RAMP_LUMA + ",select='not(mod(n,2))+gt(mod(n,13),9)',format=yuv420p", codec=lossless,
    )  # fmt: skip
    c["audio"] = lavfi(d / "audio_only.m4a", "sine=f=440:d=2", codec=("-c:a", "aac"))
    c["tiny"] = lavfi(d / "tiny.mp4", "testsrc2=s=320x240:r=30:d=0.3")
    c["testsrc"] = lavfi(d / "testsrc.mp4", "testsrc2=s=640x360:r=30:d=4")
    c["still"] = lavfi(
        d / "still.jpg", "testsrc2=s=640x360:r=1:d=1", "-frames:v", "1", "-update", "1",
        vf="format=yuvj444p,crop=639:359", codec=(),
    )  # fmt: skip
    c["portrait"] = lavfi(
        d / "portrait_odd.mp4", "testsrc2=s=360x640:r=30:d=3", vf="format=yuv444p,crop=357:635",
        codec=("-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv444p"),
    )  # fmt: skip
    c["rotated"] = d / "rotated.mp4"
    ff.run(["-display_rotation", "90", "-i", str(c["testsrc"]), "-c", "copy", str(c["rotated"])], timeout=120)
    # no container, so no duration and no timestamps of its own
    c["raw"] = lavfi(d / "raw.h264", "testsrc2=s=320x240:r=25:d=3", "-f", "h264")
    # a recording cut off part-way (index at the front, so what is there can still be read)
    whole = lavfi(d / "whole.mp4", "testsrc2=s=320x240:r=30:d=8", "-g", "15", "-movflags", "+faststart")
    c["truncated"] = d / "truncated.mp4"
    c["truncated"].write_bytes(whole.read_bytes()[: int(whole.stat().st_size * 0.55)])
    c["garbage"] = d / "garbage.mp4"
    c["garbage"].write_bytes(np.random.default_rng(0).integers(0, 256, 50_000, dtype=np.uint8).tobytes())
    c["empty"] = d / "empty.mp4"
    c["empty"].write_bytes(b"")

    board = (
        "color=c=0xF4F4F0:s=640x360:r=15:d=5,drawgrid=w=40:h=40:t=2:color=black,"
        "drawbox=x=60:y=60:w=200:h=90:color=0x203080:t=fill,drawbox=x=380:y=200:w=160:h=110:color=0xA03020:t=fill"
    )
    # bars for 4 s, then a cut to a "whiteboard" that is smeared for its first 1.3 s and sharp after
    c["blur_then_sharp"] = d / "blur_then_sharp.mp4"
    ff.run(
        ["-f", "lavfi", "-i", "smptehdbars=s=640x360:r=15:d=4", "-f", "lavfi", "-i", board, "-filter_complex",
         "[1:v]gblur=sigma=7:enable='lt(t,1.3)'[b];[0:v][b]concat=n=2:v=1:a=0,format=yuv420p[v]", "-map", "[v]",
         "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18", str(c["blur_then_sharp"])],
        timeout=300,
    )  # fmt: skip
    # one static picture seen by a shaking camera under flickering light, for 20 s
    shake = (
        "crop=640:360:x='32+14*sin(2*PI*1.3*t)+8*sin(2*PI*3.7*t+1)':y='32+9*sin(2*PI*0.9*t+2)+5*sin(2*PI*2.9*t)',"
        "eq=brightness='0.06*sin(2*PI*0.7*t)':contrast='1+0.08*sin(2*PI*0.45*t)':eval=frame,format=yuv420p"
    )
    c["shaky"] = lavfi(
        d / "shaky.mp4", "smptehdbars=s=704x424:r=15:d=20",
        vf="drawgrid=w=64:h=64:t=3:color=black,drawbox=x=100:y=80:w=220:h=120:color=0x2040A0:t=fill," + shake,
    )  # fmt: skip
    return c


def check_selection(kfs: list[FrameCandidate], cfg: FrameSettings, duration: float) -> None:
    """Invariants every selection must satisfy."""
    assert kfs, "a video with frames always yields at least one keyframe"
    assert [k.t for k in kfs] == sorted(k.t for k in kfs)
    assert kfs[0].reason == "first" and sum(k.reason == "first" for k in kfs) == 1
    assert all(k.reason in K.REASONS for k in kfs)
    assert all(0.0 <= k.novelty <= 1.0 and k.sharpness >= 0.0 and math.isfinite(k.sharpness) for k in kfs)
    assert all(-0.001 <= k.t <= duration + 0.001 for k in kfs)
    if len(kfs) > 1:
        assert min(gaps(kfs)) >= cfg.min_gap_s - 1e-6
    if cfg.max_per_minute > 0:
        assert len(kfs) <= max(1, math.ceil(cfg.max_per_minute * duration / 60.0))


@needs_ffmpeg
def test_demo_every_scene_gets_a_keyframe_that_shows_it(demo_video, tmp_path):
    cfg = FrameSettings()
    kfs = select_keyframes(demo_video.path, cfg, duration=demo_video.duration)
    check_selection(kfs, cfg, demo_video.duration)
    assert kfs[0].t < cfg.sharpness_window_s + 0.1  # "first" is near the start

    by_scene = {s.name: [k for k in kfs if s.t0 <= k.t < s.t0 + s.duration] for s in demo_video.scenes}
    assert all(by_scene.values()), {name: len(found) for name, found in by_scene.items()}
    # Unchanging scenes shorter than max_gap_s get one frame each, not one per sample.
    for name in ("whiteboard", "door-sign", "parking"):
        assert len(by_scene[name]) == 1, (name, by_scene[name])
    # A cut is never represented by the frame at the cut itself.
    for scene in demo_video.scenes[1:]:
        assert by_scene[scene.name][0].t >= scene.t0 + 0.4
    assert by_scene["whiteboard"][0].reason == "scene" and by_scene["door-sign"][0].reason == "scene"
    assert by_scene["whiteboard"][0].novelty > 0.5

    paths = extract_frames(demo_video.path, [k.t for k in kfs], tmp_path / "frames", width=640)
    colour = {scene_at(k.t): mean_rgb(p, tmp_path) for k, p in zip(kfs, paths, strict=True)}
    r, g, b = colour["whiteboard"]  # near-white
    assert min(r, g, b) > 195, colour
    r, g, b = colour["door-sign"]  # dark blue
    assert b > r + 30 and b > g + 15 and r < 110, colour
    r, g, b = colour["parking"]  # dark grey
    assert max(r, g, b) < 110 and abs(r - g) < 15 and b < r + 8, colour
    r, g, b = colour["desk"]  # colour bars: neither of the flat scenes
    assert 60 < (r + g + b) / 3 < 195, colour


@needs_ffmpeg
def test_demo_keep_alive_interval(demo_video):
    cfg = FrameSettings(max_gap_s=8.0, max_per_minute=0)  # no budget, so every keep-alive survives
    kfs = select_keyframes(demo_video.path, cfg)
    check_selection(kfs, cfg, demo_video.duration)
    assert max(gaps(kfs)) <= cfg.max_gap_s + 1.0 / cfg.analysis_fps + 0.1
    assert demo_video.duration - kfs[-1].t <= cfg.max_gap_s + 1.0 / cfg.analysis_fps + 0.1
    board = demo_video.scenes[1]
    on_board = [k for k in kfs if board.t0 <= k.t < board.t0 + board.duration]
    assert [k.reason for k in on_board] == ["scene", "interval", "interval"]  # 24 s of one whiteboard
    assert all(k.novelty < cfg.novelty_threshold for k in on_board[1:])


@needs_ffmpeg
def test_demo_budget_and_min_gap(demo_video):
    cfg = FrameSettings(max_per_minute=2.0)
    kfs = select_keyframes(demo_video.path, cfg)
    check_selection(kfs, cfg, demo_video.duration)
    assert len(kfs) == 3  # 2 a minute over 82 s; the default settings find more than that
    assert len(select_keyframes(demo_video.path, FrameSettings())) > 3
    assert all(k.novelty > 0.5 for k in kfs)  # what stayed is "first" and the biggest changes

    cfg = FrameSettings(min_gap_s=25.0, max_gap_s=30.0)
    kfs = select_keyframes(demo_video.path, cfg)
    check_selection(kfs, cfg, demo_video.duration)
    assert len(kfs) >= 3 and min(gaps(kfs)) >= 25.0


@needs_ffmpeg
def test_demo_wrong_duration_hint_changes_nothing(demo_video, caplog):
    cfg = FrameSettings()
    expected = select_keyframes(demo_video.path, cfg)
    assert select_keyframes(demo_video.path, cfg, duration=0.5) == expected
    with caplog.at_level("WARNING", logger="videonotes.keyframes"):
        assert select_keyframes(demo_video.path, cfg, duration=7200.0) == expected
    assert "expected 7200 s of video" in caplog.text


@needs_ffmpeg
def test_sharp_frame_is_chosen_over_blurred_ones(clips):
    cfg = FrameSettings()
    kfs = select_keyframes(clips["blur_then_sharp"], cfg)
    check_selection(kfs, cfg, 9.0)
    assert [k.reason for k in kfs] == ["first", "scene"]
    # the cut is at 4.0 s, the picture is smeared until 5.3 s; the keyframe waits for it to clear
    assert 5.3 <= kfs[1].t <= 4.0 + K._SETTLE_S + cfg.sharpness_window_s + 0.6


@needs_ffmpeg
def test_camera_shake_and_flicker_do_not_trigger_keyframes(clips):
    cfg = FrameSettings()
    kfs = select_keyframes(clips["shaky"], cfg)
    check_selection(kfs, cfg, 20.0)
    assert [k.reason for k in kfs] == ["first"]  # 40 samples of one picture, one keyframe
    kfs = select_keyframes(clips["shaky"], FrameSettings(max_gap_s=8.0))
    assert [k.reason for k in kfs] == ["first", "interval", "interval"]


@needs_ffmpeg
def test_no_video_stream_gives_empty_list(clips):
    assert select_keyframes(clips["audio"], FrameSettings()) == []


@needs_ffmpeg
def test_clip_shorter_than_one_analysis_interval_gives_one_frame(clips):
    kfs = select_keyframes(clips["tiny"], FrameSettings())
    assert [(k.t, k.reason) for k in kfs] == [(0.0, "first")]


@needs_ffmpeg
def test_still_image_gives_one_frame_at_zero(clips, tmp_path):
    kfs = select_keyframes(clips["still"], FrameSettings())
    assert [(k.t, k.reason) for k in kfs] == [(0.0, "first")]
    assert kfs[0].sharpness > 0
    (path,) = extract_frames(clips["still"], [kfs[0].t], tmp_path)
    assert image_size(path) == (639, 359)  # odd-sized, untouched
    # a time past a photo's only frame still gives that frame
    (late,) = extract_frames(clips["still"], [5.0], tmp_path, width=320)
    assert late.name == "kf_000005000.jpg" and image_size(late)[0] == 320
    assert mean_rgb(late, tmp_path) == pytest.approx(mean_rgb(path, tmp_path), abs=6)


@needs_ffmpeg
@pytest.mark.parametrize(("name", "duration", "portrait"), [("portrait", 3.0, True), ("rotated", 4.0, True), ("raw", 3.0, False)])
def test_odd_portrait_rotated_and_durationless_sources(clips, tmp_path, name, duration, portrait):
    info = ff.probe(clips[name])
    if name == "raw":
        assert info.duration == 0.0  # the container knows no duration ...
    if name == "rotated":
        assert info.rotation == 90 and (info.width, info.height) == (640, 360)
    cfg = FrameSettings(max_gap_s=1.0, min_gap_s=0.5, max_per_minute=0)
    kfs = select_keyframes(clips[name], cfg)
    check_selection(kfs, cfg, duration)
    assert len(kfs) >= 3  # ... yet the whole clip was analysed
    assert kfs[-1].t > duration - 1.6
    paths = extract_frames(clips[name], [k.t for k in kfs], tmp_path / name, width=200)
    w, h = image_size(paths[0])
    assert w <= 200 and (h > w) == portrait
    if name == "portrait":
        assert (info.width, info.height) == (357, 635)  # odd in both directions
        geometry = K.analysis_geometry(K.display_size(info), 320)
        assert (geometry.width, geometry.height) == (320, 570) and geometry.sharp_width == 320  # as for (641, 361) above


@needs_ffmpeg
@pytest.mark.parametrize("name", ["ramp", "vfr"])
def test_keyframe_times_are_the_source_timestamps(clips, tmp_path, name):
    """Each frame of these clips encodes its own index, so a selected time can be checked
    against the picture found there - also when the frame rate is variable."""
    cfg = FrameSettings(max_gap_s=1.0, min_gap_s=0.5, max_per_minute=0, sharpness_window_s=0)
    kfs = select_keyframes(clips[name], cfg)
    assert len(kfs) >= 4 and kfs[0].t == 0.0
    paths = extract_frames(clips[name], [k.t for k in kfs], tmp_path / name)
    for k, path in zip(kfs, paths, strict=True):
        index = ramp_index(path, tmp_path)
        assert index / RAMP_FPS == pytest.approx(k.t, abs=0.0015), (k, index)  # mkv rounds to the millisecond
        if name == "vfr":
            assert index % 2 == 0 or index % 13 > 9  # a frame that exists in the file


@needs_ffmpeg
def test_unreadable_files_raise_ffmpeg_error(clips, tmp_path):
    for name in ("garbage", "empty"):
        with pytest.raises(ff.FFmpegError) as err:
            select_keyframes(clips[name], FrameSettings())
        assert str(err.value).strip()
    with pytest.raises(ff.FFmpegError, match="no such media file"):
        select_keyframes(tmp_path / "missing.mp4", FrameSettings())


@needs_ffmpeg
def test_recording_cut_off_part_way_yields_what_is_there(clips):
    cfg = FrameSettings(max_gap_s=1.0, min_gap_s=0.5, max_per_minute=0)
    kfs = select_keyframes(clips["truncated"], cfg, duration=8.0)
    assert kfs and kfs[0].reason == "first"
    assert 2.0 < kfs[-1].t < 6.5  # about half of the 8 s survived, and nothing is invented beyond it


@needs_ffmpeg
def test_decode_failure_surfaces_ffmpeg_text(clips, monkeypatch):
    real = K.analysis_command

    def broken(src, geometry, **kw):
        cmd = real(src, geometry, **kw)
        cmd[cmd.index("-filter_complex") + 1] = "[0:V:0]nosuchfilter[out]"
        return cmd

    monkeypatch.setattr(K, "analysis_command", broken)
    with pytest.raises(ff.FFmpegError) as err:
        select_keyframes(clips["testsrc"], FrameSettings())
    assert "testsrc.mp4" in str(err.value) and "nosuchfilter" in str(err.value)
    assert err.value.returncode not in (None, 0) and "nosuchfilter" in err.value.stderr


def hardware_available(monkeypatch) -> list[str | None]:
    """Pretend to be a Mac with VideoToolbox; returns the list of decoders tried."""
    tried: list[str | None] = []
    real = K.analysis_command

    def spy(src, geometry, **kw):
        tried.append(kw.get("hwaccel"))
        return real(src, geometry, **kw)

    monkeypatch.setattr(K, "is_macos", lambda: True)
    monkeypatch.setattr(ff, "has_hwaccel", lambda name: name == "videotoolbox")
    monkeypatch.setattr(K, "analysis_command", spy)
    return tried


@needs_ffmpeg
def test_software_decode_unless_mac_with_videotoolbox(clips, monkeypatch):
    tried = hardware_available(monkeypatch)
    monkeypatch.setattr(K, "is_macos", lambda: False)
    select_keyframes(clips["testsrc"], FrameSettings())
    assert tried == [None]
    monkeypatch.setattr(K, "is_macos", lambda: True)
    select_keyframes(clips["testsrc"], FrameSettings(), hwaccel=False)
    assert tried == [None, None]
    monkeypatch.setattr(ff, "has_hwaccel", lambda name: False)
    select_keyframes(clips["testsrc"], FrameSettings())
    assert tried == [None, None, None]


@needs_ffmpeg
@pytest.mark.parametrize("failure", ["exit 3", "no frames", "dies after two frames", "hangs"])
def test_hardware_decode_failure_falls_back_to_software(clips, monkeypatch, tmp_path, failure):
    expected = select_keyframes(clips["testsrc"], FrameSettings())
    tried = hardware_available(monkeypatch)
    real = K.analysis_command
    geometry = K.analysis_geometry((640, 360), 320)

    def flaky(src, geom, **kw):
        cmd = real(src, geom, **kw)
        if not kw.get("hwaccel"):
            return cmd
        if failure == "exit 3":
            return [sys.executable, "-c", "import sys; sys.exit(3)"]
        if failure == "no frames":
            return [sys.executable, "-c", "pass"]
        if failure == "hangs":
            monkeypatch.setattr(K, "_STALL_TIMEOUT_S", 1.0)
            return fake_cmd(tmp_path, geometry.frame_bytes, 5, "hang")
        return fake_cmd(tmp_path, geometry.frame_bytes, 2, "fail")

    monkeypatch.setattr(K, "analysis_command", flaky)
    assert select_keyframes(clips["testsrc"], FrameSettings()) == expected
    assert tried == ["videotoolbox", None]


@needs_ffmpeg
def test_real_hwaccel_flag_on_a_build_without_it_still_works(clips, monkeypatch):
    """The actual ``-hwaccel videotoolbox`` command line, on an ffmpeg that lacks VideoToolbox:
    whatever that ffmpeg does with it (refuse or ignore), the result is the software one."""
    expected = select_keyframes(clips["testsrc"], FrameSettings())
    tried = hardware_available(monkeypatch)
    assert select_keyframes(clips["testsrc"], FrameSettings()) == expected
    assert tried[0] == "videotoolbox"


@needs_ffmpeg
def test_ctrl_c_during_analysis_leaves_no_ffmpeg_behind(clips, monkeypatch):
    procs: list[subprocess.Popen] = []
    real_popen = subprocess.Popen

    def spy(*args, **kwargs):
        procs.append(real_popen(*args, **kwargs))
        return procs[-1]

    def interrupt(self, t, gray, sharp, usable=None):
        raise KeyboardInterrupt

    monkeypatch.setattr(K.subprocess, "Popen", spy)
    monkeypatch.setattr(K._Selector, "push", interrupt)
    with pytest.raises(KeyboardInterrupt):
        select_keyframes(clips["testsrc"], FrameSettings())
    analysis = [p for p in procs if "pipe:1" in p.args]
    assert len(analysis) == 1 and all(p.returncode is not None for p in procs)


@needs_ffmpeg
def test_degenerate_settings_on_a_real_clip(clips):
    for cfg in (
        FrameSettings(analysis_fps=0, analysis_width=0, novelty_threshold=0, sharpness_window_s=0, min_gap_s=0,
                      max_gap_s=0, max_per_minute=0),
        FrameSettings(analysis_fps=-3, analysis_width=-3, novelty_threshold=-3, sharpness_window_s=-3, min_gap_s=-3,
                      max_gap_s=-3, max_per_minute=-3),
        FrameSettings(analysis_fps=1e6, analysis_width=7),
    ):  # fmt: skip
        kfs = select_keyframes(clips["testsrc"], cfg)
        assert kfs and kfs[0].reason == "first" and [k.t for k in kfs] == sorted({k.t for k in kfs})


# =====================================================================================
# end to end: extract_frames
# =====================================================================================


@needs_ffmpeg
def test_extract_names_order_and_duplicates(clips, tmp_path):
    out = tmp_path / "nested" / "frames"  # created on demand
    times = [2.0, 0.5, 2.0, 1.0004, 0.0, 1.0]
    paths = extract_frames(clips["ramp"], times, out, prefix="clip3")
    assert [p.name for p in paths] == [
        "clip3_000002000.jpg", "clip3_000000500.jpg", "clip3_000002000.jpg", "clip3_000001000.jpg",
        "clip3_000000000.jpg", "clip3_000001000.jpg",
    ]  # fmt: skip
    assert all(p.parent == out.resolve() and p.is_file() for p in paths)
    assert sorted(p.name for p in out.iterdir()) == sorted({p.name for p in paths})  # no temporary files left
    assert [ramp_index(p, tmp_path) for p in paths] == [60, 15, 60, 30, 0, 30]
    assert extract_frames(clips["ramp"], [], out) == []
    assert extract_frames(tmp_path / "missing.mp4", [], out) == []


@needs_ffmpeg
def test_extract_is_accurate_to_the_frame(clips, tmp_path):
    """Tolerance: the image is the frame on screen at ``t`` give or take half a frame, i.e.
    never more than one source frame away; times that are exact frame timestamps are exact."""
    exact = [n / RAMP_FPS for n in (0, 1, 2, 29, 30, 31, 49, 50, 51, 77, 95, 100, 103, 104)]  # around GOP starts too
    paths = extract_frames(clips["ramp"], exact, tmp_path / "exact")
    assert [ramp_index(p, tmp_path) for p in paths] == [round(t * RAMP_FPS) for t in exact]

    rng = np.random.default_rng(4)
    anywhere = [float(t) for t in rng.uniform(0.0, (RAMP_FRAMES - 1) / RAMP_FPS, 23)]  # more than one batch
    paths = extract_frames(clips["ramp"], anywhere, tmp_path / "anywhere")
    shown = [ramp_index(p, tmp_path) / RAMP_FPS for p in paths]
    assert max(abs(s - t) for s, t in zip(shown, anywhere, strict=True)) <= 0.5 / RAMP_FPS + 1e-3


@needs_ffmpeg
def test_extract_never_upscales(clips, tmp_path):
    (native,) = extract_frames(clips["ramp"], [1.0], tmp_path / "a", width=1280)
    assert image_size(native) == (320, 240)
    (small,) = extract_frames(clips["ramp"], [1.0], tmp_path / "b", width=160)
    assert image_size(small) == (160, 120)
    (unlimited,) = extract_frames(clips["ramp"], [1.0], tmp_path / "c", width=0)
    assert image_size(unlimited) == (320, 240)
    (odd,) = extract_frames(clips["portrait"], [1.0], tmp_path / "d", width=4000, quality=99)
    assert image_size(odd) == (357, 635)
    (tall,) = extract_frames(clips["rotated"], [1.0], tmp_path / "e", width=180)
    assert image_size(tall) == (180, 320)  # rotation applied, aspect kept


@needs_ffmpeg
def test_extract_past_the_end_gives_the_last_frame(clips, tmp_path):
    last = RAMP_FRAMES - 1
    paths = extract_frames(clips["ramp"], [3.0, 3.5, 60.0, 1e6, -5.0], tmp_path)
    assert [p.name for p in paths][2:] == ["kf_000060000.jpg", "kf_1000000000.jpg", "kf_000000000.jpg"]
    assert [ramp_index(p, tmp_path) for p in paths] == [90, last, last, last, 0]
    # also when the container cannot say how long it is
    paths = extract_frames(clips["raw"], [1.0, 500.0], tmp_path / "raw")
    assert all(p.is_file() for p in paths) and paths[0] != paths[1]


@needs_ffmpeg
def test_extract_rejects_bad_requests(clips, tmp_path):
    with pytest.raises(ff.FFmpegError, match="no video"):
        extract_frames(clips["audio"], [0.5], tmp_path)
    with pytest.raises(ff.FFmpegError):
        extract_frames(clips["garbage"], [0.5], tmp_path)
    with pytest.raises(ff.FFmpegError, match="no such media file"):
        extract_frames(tmp_path / "missing.mp4", [0.5], tmp_path)
    for bad in (float("nan"), float("inf")):
        with pytest.raises(ValueError, match="not a valid time"):
            extract_frames(clips["ramp"], [1.0, bad], tmp_path)
    with pytest.raises(ValueError, match="path separator"):
        extract_frames(clips["ramp"], [1.0], tmp_path, prefix="../kf")
    assert list(tmp_path.glob("*.jpg")) == []


@needs_ffmpeg
def test_extract_redoes_a_failed_batch_one_by_one(clips, tmp_path, monkeypatch):
    real_run = ff.run
    calls: list[int] = []

    def flaky(args, **kw):
        inputs = args.count("-i")
        if "-update" in args:  # an extraction (the test's own helpers decode images with ffmpeg too)
            calls.append(inputs)
        if inputs > 1:  # every multi-seek process "crashes" after writing some of its files
            real_run(args, **kw)
            return subprocess.CompletedProcess(args, 1, "", "Conversion failed!")
        return real_run(args, **kw)

    monkeypatch.setattr(ff, "run", flaky)
    times = [n / RAMP_FPS for n in (5, 20, 35, 50, 65, 80, 95, 101)]
    paths = extract_frames(clips["ramp"], times, tmp_path)
    assert [ramp_index(p, tmp_path) for p in paths] == [5, 20, 35, 50, 65, 80, 95, 101]
    assert sorted(calls, reverse=True)[:2] == [6, 2] and calls.count(1) == 8


@needs_ffmpeg
def test_extract_failure_never_returns_stale_or_partial_images(clips, tmp_path, monkeypatch):
    stale = tmp_path / "kf_000001000.jpg"
    stale.write_bytes(b"left over from an earlier run")
    real_run = ff.run

    def failing(args, **kw):
        if any(str(a).endswith("kf_000002000.jpg") or "kf_000002000.jpg." in str(a) for a in args) and args.count("-i") == 1:
            return subprocess.CompletedProcess(args, 1, "", "[mov] Input/output error")
        return real_run(args, **kw)

    monkeypatch.setattr(ff, "run", failing)
    monkeypatch.setattr(K, "_SEEK_BATCH", 1)
    with pytest.raises(ff.FFmpegError) as err:
        extract_frames(clips["ramp"], [1.0, 2.0, 3.0], tmp_path)
    message = str(err.value)
    assert "1 of 3" in message and "2.000 s" in message and "Input/output error" in message
    assert "still connected" in message  # says what to do next
    assert stale.read_bytes() == b"left over from an earlier run"  # untouched, and not passed off as new
    assert sorted(p.name for p in tmp_path.iterdir() if p.suffix == ".jpg") == ["kf_000001000.jpg"]  # no leftovers


@needs_ffmpeg
def test_extract_replaces_existing_files(clips, tmp_path):
    target = tmp_path / "kf_000001000.jpg"
    target.write_bytes(b"old")
    (path,) = extract_frames(clips["ramp"], [1.0], tmp_path)
    assert path == target.resolve() and ramp_index(path, tmp_path) == 30


def test_extract_command_shape():
    shots = [
        K._Shot(0.0, -0.016, Path("/o/.a.part.jpg"), Path("/o/a.jpg")),
        K._Shot(12.5, 12.483333, Path("/o/.b.part.jpg"), Path("/o/b.jpg")),
    ]
    args = K.extract_command("/v/clip.mp4", shots, scale="scale=1280:-2:flags=bicubic", quality=3)
    assert args.count("-i") == 2 and args.count("-ss") == 1  # the first frame needs no seek
    ss = args.index("-ss")
    assert args[ss + 1] == "12.483333" and args[ss + 2 : ss + 6] == ["-threads", "2", "-i", "/v/clip.mp4"]  # seek before -i
    first_out = args.index("-map")
    assert args[first_out : first_out + 7] == ["-map", "0:V:0", "-an", "-sn", "-dn", "-frames:v", "1"]
    assert args[-1] == "/o/.b.part.jpg" and args[-3:-1] == ["-update", "1"]
    assert "1:V:0" in args and args.count("-vf") == 2 and args[args.index("-q:v") + 1] == "3"
    assert "-vf" not in K.extract_command("/v/clip.mp4", shots[:1], scale=None, quality=3)
    assert K._scale_filter((1920, 1080), 1280) == "scale=1280:-2:flags=bicubic"
    assert K._scale_filter((1280, 720), 1280) is None and K._scale_filter((1920, 1080), 0) is None
    assert "min(iw,1280)" in (K._scale_filter(None, 1280) or "")
