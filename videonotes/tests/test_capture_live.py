"""Live capture: command builders, segment timing, and SegmentRecorder against real ffmpeg.

The recorder takes any argv, so the "camera" here is ffmpeg's lavfi test source read in
real time, pushed through the *real* output half of ``webcam_command`` (encoder, key
frames, segment muxer, file naming).  The RTMP path is exercised with a real listener
and a second ffmpeg publishing to it over localhost.  Behaviours that need a misbehaving
ffmpeg (hangs, ignored signals, a camera rejecting a mode) use tiny Python stand-ins.
"""

from __future__ import annotations

import logging
import os
import shutil
import signal
import socket
import subprocess
import sys
import time
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path

import pytest

from videonotes.capture import CaptureError, live
from videonotes.capture.devices import CaptureDevice, default_audio_device
from videonotes.capture.live import Segment, SegmentRecorder
from videonotes.config import Settings
from videonotes.media import ffmpeg as ff

needs_ffmpeg = pytest.mark.skipif(not ff.have_ffmpeg(), reason="ffmpeg not installed")

CAMERA = CaptureDevice(1, "OsmoAction4", "video")
CAMERA_MIC = CaptureDevice(2, "OsmoAction4", "audio")


def wait_for(condition: Callable[[], object], timeout: float, what: str) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if condition():
            return
        time.sleep(0.05)
    pytest.fail(f"timed out after {timeout:.0f} s waiting for {what}")


def assert_reaped(pid: int) -> None:
    """The process must be gone *and* collected (no zombie left behind)."""
    with pytest.raises(ChildProcessError):
        os.waitpid(pid, os.WNOHANG)


def value_after(cmd: list[str], flag: str) -> str:
    return cmd[cmd.index(flag) + 1]


@pytest.fixture()
def small(settings: Settings) -> Settings:
    """Settings for quick tests: tiny picture, 2-second segments."""
    settings.capture.segment_seconds = 2
    settings.capture.video_size = "320x240"
    settings.capture.framerate = 10.0
    settings.capture.video_bitrate = "300k"
    return settings


def lavfi_camera(settings: Settings, out_dir: Path, *, audio: bool = True, limit: float | None = None) -> list[str]:
    """webcam_command with the avfoundation input swapped for a real-time lavfi "camera"."""
    cmd = live.webcam_command(settings, CAMERA, CAMERA_MIC if audio else None, out_dir)
    first, last = cmd.index("-f"), cmd.index("-i") + 2
    assert cmd[first + 1] == "avfoundation"
    graph = "testsrc2=size=640x480:rate=10[out0]"
    if audio:
        graph += ";sine=frequency=440:sample_rate=48000[out1]"
    source = ["-re", "-f", "lavfi", "-i", graph]
    if limit is not None:
        source = ["-t", str(limit), *source]
    return cmd[:first] + source + cmd[last:]


# ---------------------------------------------------------------------------------
# Builders
# ---------------------------------------------------------------------------------


@needs_ffmpeg
def test_webcam_command_shape(settings, tmp_path, monkeypatch):
    monkeypatch.setattr(ff, "has_encoder", lambda name: name == "h264_videotoolbox")
    out = tmp_path / "media" / "s1"
    cmd = live.webcam_command(settings, CAMERA, CAMERA_MIC, out)
    base = ff.base_cmd(loglevel="error")
    assert cmd[: len(base)] == base
    assert cmd[len(base)] == "-stdin"  # re-enables "q" on stdin after base_cmd's -nostdin
    # input options must precede -i, and say everything avfoundation would otherwise guess wrongly
    i = cmd.index("-i")
    assert cmd[len(base) + 1 : i] == [
        "-f", "avfoundation", "-framerate", "30", "-video_size", "1280x720", "-pixel_format", "nv12",
    ]  # fmt: skip
    assert cmd[i + 1] == "1:2"  # devices by index, never by name
    rest = cmd[i + 2 :]
    assert rest[:4] == ["-map", "0:v:0", "-map", "0:a:0"]
    assert value_after(rest, "-fps_mode") == "cfr" and value_after(rest, "-r") == "30"
    assert "min(iw,1280)" in value_after(rest, "-vf") and "min(ih,720)" in value_after(rest, "-vf")
    # hardware encoder with the settings' bitrate
    assert value_after(rest, "-c:v") == "h264_videotoolbox"
    assert value_after(rest, "-b:v") == "1500k" and value_after(rest, "-maxrate") == "2400k"
    assert value_after(rest, "-realtime") == "1" and value_after(rest, "-allow_sw") == "1"
    assert value_after(rest, "-pix_fmt") == "nv12"
    # key frames: every 2 s, and exactly on every segment boundary
    assert value_after(rest, "-g") == "60"
    assert value_after(rest, "-force_key_frames") == "expr:gte(t,n_forced*60)"
    # audio: locked to its timestamps, mono speech
    assert value_after(rest, "-af") == "aresample=async=1000:first_pts=0"
    assert value_after(rest, "-c:a") == "aac" and value_after(rest, "-b:a") == "64k"
    assert value_after(rest, "-ac") == "1" and value_after(rest, "-ar") == "48000"
    # crash-safe fixed-length segments named by wall clock
    assert rest[-13:] == [
        "-f", "stream_segment", "-segment_time", "60", "-segment_format", "mpegts",
        "-segment_format_options", "flush_packets=1", "-reset_timestamps", "1", "-strftime", "1",
        f"{out}/seg_%Y%m%d-%H%M%S_%s.ts",
    ]  # fmt: skip
    assert "-segment_atclocktime" not in rest
    assert all(isinstance(part, str) for part in cmd)


@needs_ffmpeg
def test_webcam_command_software_encoder_and_errors(settings, tmp_path, monkeypatch):
    monkeypatch.setattr(ff, "has_encoder", lambda name: name == "libx264")
    cmd = live.webcam_command(settings, CAMERA, CAMERA_MIC, tmp_path)
    assert value_after(cmd, "-c:v") == "libx264" and value_after(cmd, "-preset") == "veryfast"
    assert value_after(cmd, "-tune") == "zerolatency" and value_after(cmd, "-bufsize") == "3000k"
    assert "-realtime" not in cmd

    monkeypatch.setattr(ff, "has_encoder", lambda name: False)
    with pytest.raises(CaptureError, match="brew install ffmpeg"):
        live.webcam_command(settings, CAMERA, CAMERA_MIC, tmp_path)


@needs_ffmpeg
def test_webcam_command_audio_choices(settings, tmp_path, caplog):
    with caplog.at_level(logging.INFO, logger="videonotes.capture.live"):
        silent = live.webcam_command(settings, CAMERA, None, tmp_path)
        default = live.webcam_command(settings, CAMERA, default_audio_device(), tmp_path)
    assert value_after(silent, "-i") == "1:none"
    assert "-an" in silent and "-c:a" not in silent and "-af" not in silent and "0:a:0" not in silent
    assert value_after(default, "-i") == "1:default"
    assert "0:a:0" in default and "-an" not in default
    assert "without audio" in caplog.text and "default input" in caplog.text  # the choice is logged


@needs_ffmpeg
def test_webcam_command_follows_settings(settings, tmp_path):
    settings.capture.framerate = 29.97
    settings.capture.video_size = "1920x1080"
    settings.capture.video_bitrate = "4M"
    settings.capture.audio_bitrate = "96k"
    settings.capture.segment_seconds = 30
    weird = tmp_path / "100% mine"
    cmd = live.webcam_command(
        settings, CaptureDevice(0, "UVC Camera", "video"), CaptureDevice(0, "Mic", "audio"), weird
    )
    assert value_after(cmd, "-framerate") == "30000/1001" and value_after(cmd, "-r") == "30000/1001"
    assert value_after(cmd, "-video_size") == "1920x1080" and value_after(cmd, "-i") == "0:0"
    assert value_after(cmd, "-b:v") == "4000k" and value_after(cmd, "-maxrate") == "6400k"
    assert value_after(cmd, "-b:a") == "96k"
    assert value_after(cmd, "-segment_time") == "30" and value_after(cmd, "-force_key_frames").endswith("n_forced*30)")
    assert value_after(cmd, "-g") == "60"
    # ffmpeg runs the whole output path through strftime: a "%" in a folder name must be doubled
    assert cmd[-1] == f"{tmp_path}/100%% mine/seg_%Y%m%d-%H%M%S_%s.ts"


@needs_ffmpeg
def test_webcam_command_rejects_bad_settings(settings, tmp_path, caplog):
    def build(**changes):
        fresh = Settings(home=settings.home)
        for key, value in changes.items():
            setattr(fresh.capture, key, value)
        return live.webcam_command(fresh, CAMERA, CAMERA_MIC, tmp_path)

    with pytest.raises(CaptureError, match="video_size"):
        build(video_size="720p")
    with pytest.raises(CaptureError, match="framerate"):
        build(framerate=0)
    with pytest.raises(CaptureError, match="video_bitrate"):
        build(video_bitrate="fast")
    with pytest.raises(CaptureError, match="audio_bitrate"):
        build(audio_bitrate="-1")
    with pytest.raises(CaptureError, match="not a video"):
        live.webcam_command(settings, CAMERA_MIC, None, tmp_path)
    with pytest.raises(CaptureError, match="not an audio"):
        live.webcam_command(settings, CAMERA, CAMERA, tmp_path)
    # one-second file names cannot tell two segments apart below two seconds
    with caplog.at_level(logging.WARNING, logger="videonotes.capture.live"):
        assert value_after(build(segment_seconds=1), "-segment_time") == "2"
    assert "too short" in caplog.text


@needs_ffmpeg
def test_rtmp_listen_command_shape(settings, tmp_path):
    settings.capture.rtmp_port = 1936
    settings.capture.rtmp_path = "/live/cam/"
    cmd = live.rtmp_listen_command(settings, tmp_path)
    base = ff.base_cmd(loglevel="error")
    assert cmd[: len(base) + 1] == [*base, "-stdin"]
    i = cmd.index("-i")
    # listen for one connection, wait for it forever, give up on a silent one
    assert cmd[len(base) + 1 : i] == ["-listen", "1", "-rw_timeout", "15000000"]
    assert "-timeout" not in cmd
    assert cmd[i + 1] == "rtmp://0.0.0.0:1936/live/cam"
    # stream copy; audio optional
    assert cmd[i + 2 : i + 8] == ["-map", "0:v:0", "-map", "0:a:0?", "-c", "copy"]
    assert "-c:v" not in cmd and "-force_key_frames" not in cmd
    # wall-clock cutting: a burst after connecting must not open two files in one second
    assert value_after(cmd, "-f") == "stream_segment" and value_after(cmd, "-segment_atclocktime") == "1"
    assert value_after(cmd, "-segment_format") == "mpegts"
    assert value_after(cmd, "-segment_format_options") == "flush_packets=1"
    assert value_after(cmd, "-strftime") == "1" and cmd[-1] == f"{tmp_path}/seg_%Y%m%d-%H%M%S_%s.ts"
    assert live.is_listener_command(cmd)
    assert not live.is_listener_command(live.webcam_command(settings, CAMERA, None, tmp_path))
    assert not live.is_listener_command(["ffmpeg", "-listen", "0", "-i", "x"])

    for bad in (0, 70000, "abc"):
        settings.capture.rtmp_port = bad
        with pytest.raises(CaptureError, match="rtmp_port"):
            live.rtmp_listen_command(settings, tmp_path)


MODE_ERROR = """\
[avfoundation @ 0x14f] Selected video size (1280x720) is not supported by the device.
[avfoundation @ 0x14f] Supported modes:
[avfoundation @ 0x14f]   1920x1080@[30.000030 30.000030]fps
[avfoundation @ 0x14f]   1920x1080@[25.000000 25.000000]fps
[in#0 @ 0x600] Error opening input: Invalid argument
"""


@needs_ffmpeg
def test_fallback_command_picks_a_supported_mode(settings, tmp_path):
    cmd = live.webcam_command(settings, CAMERA, CAMERA_MIC, tmp_path)
    fixed = live.fallback_command(cmd, MODE_ERROR)
    assert fixed is not None and len(fixed) == len(cmd)
    assert value_after(fixed, "-video_size") == "1920x1080" and value_after(fixed, "-framerate") == "30"
    assert value_after(fixed, "-r") == "30"  # output rate unchanged
    assert "min(iw,1280)" in value_after(fixed, "-vf")  # still scaled to the configured size
    changed = [k for k in range(len(cmd)) if cmd[k] != fixed[k]]
    assert changed == [cmd.index("-video_size") + 1]

    # a camera that is slower than asked: capture at its rate, and do not pad the output
    slow = MODE_ERROR.replace("1920x1080@[30.000030 30.000030]fps", "1280x720@[15.000000 15.000000]fps")
    fixed = live.fallback_command(cmd, slow)
    assert value_after(fixed, "-video_size") == "1920x1080" and value_after(fixed, "-framerate") == "25"
    assert value_after(fixed, "-r") == "25" and value_after(fixed, "-g") == "50"


@needs_ffmpeg
def test_fallback_command_knows_when_not_to_apply(settings, tmp_path):
    cmd = live.webcam_command(settings, CAMERA, CAMERA_MIC, tmp_path)
    assert live.fallback_command(cmd, "Failed to create AV capture input device: busy") is None
    assert live.fallback_command(cmd, "Supported modes:\n") is None  # no mode to choose from
    same = MODE_ERROR.replace("1920x1080@[30.000030", "1280x720@[30.000030")
    assert live.fallback_command(cmd, same) is None  # already what was asked for: retrying would loop
    assert live.fallback_command(live.rtmp_listen_command(settings, tmp_path), MODE_ERROR) is None
    assert live.fallback_command(["ffmpeg", "-f", "avfoundation", "-i", "0"], MODE_ERROR) is None


@needs_ffmpeg
def test_recorder_recognises_its_own_files_only(settings, tmp_path):
    odd = tmp_path / "100% mine"
    cmd = live.webcam_command(settings, CAMERA, None, odd)
    assert live._name_filter(cmd, odd) == ("seg_", (".ts",))  # the doubled "%" is understood
    recorder = SegmentRecorder(cmd, odd, segment_seconds=60)
    assert recorder._is_segment_name("seg_20261122-143200_1795357920.ts")
    assert not recorder._is_segment_name(".seg_20261122-143200_1795357920.ts")
    assert not recorder._is_segment_name("seg_20261122-143200_1795357920.ts.part")
    assert not recorder._is_segment_name("notes_20261122.ts")
    # an argv whose output is not a pattern inside out_dir: any media file there counts
    assert live._name_filter(["ffmpeg", "-i", "x", "/elsewhere/out.mkv"], odd) == ("", live._MEDIA_SUFFIXES)
    other = SegmentRecorder(["ffmpeg", "-i", "x", "pipe:1"], odd, segment_seconds=60)
    assert other._is_segment_name("anything.mp4") and not other._is_segment_name("anything.txt")


def test_capture_errors_are_reported_like_other_media_errors():
    # The command line prints FFmpegError messages as plain text; capture problems must look the same.
    assert issubclass(CaptureError, ff.FFmpegError) and issubclass(CaptureError, RuntimeError)
    assert str(CaptureError("Plug the camera in.")) == "Plug the camera in."


def test_listener_restart_never_reuses_a_file_name(tmp_path):
    recorder = SegmentRecorder(["ffmpeg", "-listen", "1", "-i", "rtmp://x", str(tmp_path / "seg_%s.ts")], tmp_path,
                               segment_seconds=60)  # fmt: skip
    assert recorder._relisten_delay() == SegmentRecorder.RELISTEN_DELAY_S  # nothing recorded yet
    now = int(time.time())
    recorder._order.append(f"seg_20200101-000000_{now - 30}.ts")  # the last file was opened long ago
    assert recorder._relisten_delay() == SegmentRecorder.RELISTEN_DELAY_S  # listen again at once
    recorder._order.append(f"seg_20200101-000000_{now}.ts")  # opened within this very second
    assert 0.0 < recorder._relisten_delay() <= 1.0 + SegmentRecorder.RELISTEN_DELAY_S  # wait for the next second
    recorder._order.append(f"seg_20200101-000000_{now + 3600}.ts")  # the clock was set back meanwhile
    assert recorder._relisten_delay() == 2.0  # never wait long because of a strange clock


def test_segment_start_from_name(monkeypatch):
    assert live.segment_start_from_name("seg_20261122-143200_1795357920.ts") == 1795357920.0
    assert live.segment_start_from_name("/x/y/seg_20261122-143200_1795357920.ts") == 1795357920.0
    assert live.segment_start_from_name("seg_000.ts") is None
    assert live.segment_start_from_name("holiday.mp4") is None
    # no epoch field (a C library without %s): the local-time field, in the current time zone
    monkeypatch.setenv("TZ", "America/New_York")
    time.tzset()
    try:
        noon_in_new_york = datetime(2026, 7, 4, 16, 0, tzinfo=UTC).timestamp()  # EDT is UTC-4
        assert live.segment_start_from_name("seg_20260704-120000_s.ts") == noon_in_new_york
        assert live.segment_start_from_name("seg_20269999-120000_s.ts") is None
    finally:
        monkeypatch.undo()
        time.tzset()


def test_estimate_start_ts():
    name = 1_000_000.0
    # live source: last write minus content length is the precise start
    assert live.estimate_start_ts(name, name + 60.4, 60.0) == pytest.approx(name + 0.4)
    # fresh RTMP connection: the file was opened 3 s after the content began
    assert live.estimate_start_ts(name, name + 57.0, 60.0) == pytest.approx(name - 3.0)
    # a stalled stream / system sleep / late trailer: wall time passed without media -> trust the name
    assert live.estimate_start_ts(name, name + 95.0, 60.0) == name
    # clock stepped back while recording, or times lost by copying -> trust the name
    assert live.estimate_start_ts(name, name - 3000.0, 60.0) == name
    assert live.estimate_start_ts(name, name + 86400.0, 60.0) == name
    # nothing in the name to check against
    assert live.estimate_start_ts(None, 500.0, 60.0) == 440.0
    assert live.estimate_start_ts(None, 500.0, -1.0) == 500.0


def test_explain_ffmpeg_error():
    assert "already in use" in live.explain_ffmpeg_error("[in#0 @ 0x1] Error opening input: Address already in use")
    assert "Privacy & Security" in live.explain_ffmpeg_error("Failed to create AV capture input device: Cannot use X")
    assert "vnote devices" in live.explain_ffmpeg_error("[AVFoundation indev @ 0x1] Video device not found")
    assert "brew upgrade ffmpeg" in live.explain_ffmpeg_error("Unrecognized option 'fps_mode'.")
    assert "capture.video_size" in live.explain_ffmpeg_error(MODE_ERROR)
    assert "disk is full" in live.explain_ffmpeg_error("av_interleaved_write_frame(): No space left on device")
    assert live.explain_ffmpeg_error("something nobody has seen before") == ""
    assert live.explain_ffmpeg_error("") == ""


def test_pixel_format_chatter_is_not_an_error():
    lines = [
        "[avfoundation @ 0x1] Selected pixel format (nv12) is not supported by the input device.",
        "[avfoundation @ 0x1] Supported pixel formats:",
        "[avfoundation @ 0x1]   uyvy422",
        "[avfoundation @ 0x1]   yuyv422",
        "[avfoundation @ 0x1] Overriding selected pixel format to use uyvy422 instead.",
        "[in#0 @ 0x2] Error opening input: Input/output error",
    ]
    assert live._meaningful(lines) == ["[in#0 @ 0x2] Error opening input: Input/output error"]
    assert live._meaningful(lines[:5]) == []


# ---------------------------------------------------------------------------------
# SegmentRecorder with real ffmpeg
# ---------------------------------------------------------------------------------


@needs_ffmpeg
def test_recorder_reports_complete_segments(small, tmp_path):
    out = tmp_path / "rec"
    recorder = SegmentRecorder(lavfi_camera(small, out), out, segment_seconds=2)
    assert recorder.running is False and recorder.poll() == [] and recorder.last_error() == ""
    launched = time.time()
    recorder.start()
    assert recorder.running
    pid = recorder.pid
    assert pid is not None

    segments: list[Segment] = []
    first_seen = 0.0
    deadline = time.monotonic() + 40
    while len(segments) < 2 and time.monotonic() < deadline:
        new = recorder.poll()
        if new and not segments:
            first_seen = time.time()
        segments += new
        # While ffmpeg runs, the file it is writing is never handed out.
        on_disk = sorted(p.name for p in out.glob("seg_*.ts"))
        assert len(on_disk) >= len(segments)
        if recorder.running and on_disk:
            assert len(on_disk) > len(segments), "the segment still being written was reported"
        time.sleep(0.1)
    assert len(segments) == 2, recorder.last_error()
    assert recorder.running and recorder.last_error() == ""

    stopping = time.monotonic()
    rest = recorder.stop()
    assert time.monotonic() - stopping < 8, "a clean stop should take well under the escalation timeouts"
    assert recorder.running is False and recorder.returncode == 0  # ffmpeg quit on "q", it was not killed
    assert_reaped(pid)
    assert recorder.stop() == [] and recorder.poll() == []  # idempotent, nothing reported twice
    assert recorder.last_error() == ""

    everything = segments + rest
    assert len(rest) <= 1
    # every file on disk was reported exactly once, in the order it was recorded
    assert [s.path.name for s in everything] == sorted(p.name for p in out.glob("seg_*.ts"))
    assert all(s.path.parent == out and s.path.is_file() for s in everything)
    starts = [s.start_ts for s in everything]
    assert starts == sorted(starts)

    # exact two-second segments (key frames are forced on the boundaries)
    for segment in segments:
        assert segment.duration == pytest.approx(2.0, abs=0.15)
    if rest:
        assert 0.5 <= rest[0].duration < 2.2

    # wall-clock start: the first segment began when ffmpeg was launched...
    assert launched - 1.0 <= segments[0].start_ts <= first_seen - 2.0 + 1.0
    assert abs(segments[0].start_ts - launched) < 1.0 + (first_seen - launched - 2.0)
    # ...each next one where the previous ended...
    for before, after in zip(everything, everything[1:], strict=False):
        assert after.start_ts == pytest.approx(before.start_ts + before.duration, abs=1.0)
    # ...and the name alone gives the same time to within its one-second resolution.
    for segment in everything:
        from_name = live.segment_start_from_name(segment.path.name)
        assert from_name is not None and abs(from_name - segment.start_ts) < 2.0

    # the files are real: H.264 + AAC at the configured size, readable on their own
    info = ff.probe(segments[1].path)
    assert info.has_video and info.has_audio and (info.width, info.height) == (320, 240)
    assert info.video_codec == "h264" and info.audio_codec == "aac"
    ff.run(["-v", "error", "-i", str(segments[1].path), "-f", "null", "-"], timeout=60)

    # after a restart the same segments are recovered from the files alone
    recovered = live.recover_segments(out)
    assert [s.path.name for s in recovered] == [s.path.name for s in everything]
    for again, original in zip(recovered, everything, strict=True):
        assert again.start_ts == pytest.approx(original.start_ts, abs=0.01)
        assert again.duration == pytest.approx(original.duration, abs=0.01)


@needs_ffmpeg
def test_recorder_when_ffmpeg_exits_by_itself(small, tmp_path):
    out = tmp_path / "rec"
    recorder = SegmentRecorder(lavfi_camera(small, out, audio=False, limit=2.6), out, segment_seconds=2)
    recorder.start()
    pid = recorder.pid
    wait_for(lambda: not recorder.running, 40, "ffmpeg to finish its 2.6 s input")
    assert recorder.returncode == 0 and recorder.last_error() == ""
    assert_reaped(pid)
    segments = recorder.poll()  # with ffmpeg gone the last file is complete too
    assert [round(s.duration, 1) for s in segments] == [2.0, 0.6]
    assert not ff.probe(segments[0].path).has_audio  # video-only recording
    assert recorder.poll() == [] and recorder.stop() == []
    assert recorder.running is False


@needs_ffmpeg
def test_recorder_reports_why_ffmpeg_died_at_start(small, tmp_path):
    out = tmp_path / "rec"
    cmd = lavfi_camera(small, out)
    cmd[cmd.index("-i") + 1] = "no_such_source=1"
    recorder = SegmentRecorder(cmd, out, segment_seconds=2)
    recorder.start()
    pid = recorder.pid
    wait_for(lambda: not recorder.running, 20, "the failing ffmpeg to be noticed")
    assert recorder.returncode not in (0, None)
    assert "no_such_source" in recorder.last_error()
    assert recorder.poll() == [] and recorder.stop() == []
    assert "no_such_source" in recorder.last_error()  # stopping afterwards does not hide the reason
    assert_reaped(pid)
    assert list(out.glob("*")) == []


@needs_ffmpeg
def test_segments_survive_a_killed_ffmpeg(small, tmp_path):
    """The reason for MPEG-TS with flush_packets=1: after `kill -9` the open file is still usable."""
    out = tmp_path / "rec"
    recorder = SegmentRecorder(lavfi_camera(small, out), out, segment_seconds=2)
    recorder.start()
    pid = recorder.pid
    wait_for(lambda: len(list(out.glob("seg_*.ts"))) >= 2, 40, "the second segment to be opened")
    time.sleep(0.9)  # some media into the second file
    os.kill(pid, signal.SIGKILL)
    wait_for(lambda: not recorder.running, 20, "the recorder to notice the kill")
    assert recorder.returncode == -signal.SIGKILL and "killed" in recorder.last_error()
    segments = recorder.poll()
    assert len(segments) == 2
    assert segments[0].duration == pytest.approx(2.0, abs=0.15)
    assert 0.5 <= segments[1].duration < 2.2  # the truncated file: readable, with its real length
    info = ff.probe(segments[1].path)
    assert info.has_video and info.has_audio
    assert segments[1].start_ts == pytest.approx(segments[0].start_ts + segments[0].duration, abs=1.0)
    assert recorder.stop() == []
    assert_reaped(pid)


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def _publish(port: int, seconds: float) -> subprocess.Popen[bytes]:
    """A stand-in for the camera: push H.264 + AAC as FLV over RTMP, in real time."""
    cmd = ff.base_cmd() + [
        "-re", "-f", "lavfi", "-i", "testsrc2=size=320x240:rate=25[out0];sine=frequency=440:sample_rate=48000[out1]",
        "-t", str(seconds),
        "-c:v", "libx264", "-preset", "veryfast", "-tune", "zerolatency", "-pix_fmt", "yuv420p", "-g", "25",
        "-b:v", "300k", "-c:a", "aac", "-b:a", "64k",
        "-f", "flv", f"rtmp://127.0.0.1:{port}/live/cam",
    ]  # fmt: skip
    return subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


@needs_ffmpeg
def test_rtmp_listener_records_what_the_camera_pushes(small, tmp_path):
    if not ff.has_encoder("libx264"):
        pytest.skip("this ffmpeg cannot play the camera (no libx264)")
    out = tmp_path / "wireless"
    small.capture.rtmp_port = _free_port()
    recorder = SegmentRecorder(live.rtmp_listen_command(small, out), out, segment_seconds=2)
    recorder.start()
    listener_pid = recorder.pid
    time.sleep(0.7)
    assert recorder.running, recorder.last_error()  # waiting for the camera, for as long as it takes
    assert recorder.poll() == []

    published = 3.0
    camera = _publish(small.capture.rtmp_port, published)
    segments: list[Segment] = []
    try:
        assert camera.wait(timeout=60) == 0, camera.stderr.read().decode(errors="replace")
    finally:
        if camera.poll() is None:
            camera.kill()
            camera.wait()
        camera.stderr.close()
    # The camera hung up: ffmpeg's one-shot server exits and the recorder listens again.
    wait_for(lambda: recorder.pid not in (None, listener_pid), 30, "the listener to be restarted")
    assert recorder.running and recorder.last_error() == ""
    assert_reaped(listener_pid)
    segments += recorder.poll()  # everything of the finished connection is complete now
    stopping = time.monotonic()
    segments += recorder.stop()  # stopping a listener that is only waiting must be quick
    assert time.monotonic() - stopping < 8
    assert recorder.running is False and recorder.last_error() == ""

    assert segments, "nothing was recorded"
    assert [s.path.name for s in segments] == sorted(p.name for p in out.glob("seg_*.ts"))
    # nothing was lost, not even what ffmpeg buffered while probing the fresh connection
    assert sum(s.duration for s in segments) == pytest.approx(published, abs=0.5)
    for segment in segments:
        info = ff.probe(segment.path)
        assert info.has_video and info.has_audio
        assert (info.video_codec, info.audio_codec) == ("h264", "aac")  # copied, not re-encoded
        assert (info.width, info.height) == (320, 240)
        ff.run(["-v", "error", "-i", str(segment.path), "-f", "null", "-"], timeout=60)  # plays through
    for before, after in zip(segments, segments[1:], strict=False):
        assert after.start_ts == pytest.approx(before.start_ts + before.duration, abs=1.0)


@needs_ffmpeg
def test_rtmp_listener_cannot_start_on_a_busy_port(small, tmp_path):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as squatter:
        squatter.bind(("0.0.0.0", 0))
        squatter.listen(1)
        small.capture.rtmp_port = squatter.getsockname()[1]
        recorder = SegmentRecorder(live.rtmp_listen_command(small, tmp_path / "w"), tmp_path / "w", segment_seconds=2)
        recorder.start()
        wait_for(lambda: not recorder.running, 20, "the listener to give up")
    reason = recorder.last_error()
    assert "already in use" in reason and "capture.rtmp_port" in reason  # advice first, then ffmpeg's words
    assert recorder.stop() == []


# ---------------------------------------------------------------------------------
# SegmentRecorder with stand-in processes (misbehaviour that real ffmpeg will not show on demand)
# ---------------------------------------------------------------------------------


@pytest.fixture(scope="module")
def sample_ts(tmp_path_factory) -> Path:
    """A real one-second MPEG-TS file that stand-in "recorders" can copy into place."""
    if not ff.have_ffmpeg():
        pytest.skip("ffmpeg not installed")
    path = tmp_path_factory.mktemp("sample") / "sample.ts"
    ff.run(
        [
            "-f",
            "lavfi",
            "-i",
            "testsrc2=size=160x120:rate=10",
            "-t",
            "1",
            "-c:v",
            "mpeg2video",
            "-f",
            "mpegts",
            str(path),
        ],
        timeout=120,
    )
    return path


def stand_in(script: str, out: Path, *extra: str) -> list[str]:
    """argv of a Python process playing ffmpeg; its last argument is the output pattern."""
    return [sys.executable, "-c", script, *extra, str(out / "seg_%03d.ts")]


def test_recorder_cannot_run_a_missing_program(tmp_path):
    recorder = SegmentRecorder([str(tmp_path / "no-ffmpeg-here"), "-i", "x"], tmp_path / "o", segment_seconds=2)
    with pytest.raises(ff.FFmpegError, match="brew install ffmpeg"):
        recorder.start()
    assert recorder.running is False and recorder.stop() == [] and recorder.poll() == []
    with pytest.raises(ValueError):
        SegmentRecorder([], tmp_path, segment_seconds=2)


WRITE_THEN_HANG = """
import os, shutil, signal, sys, time
signal.signal(signal.SIGTERM, signal.SIG_IGN)       # like an ffmpeg stuck in a blocked read
out = os.path.dirname(sys.argv[-1])
shutil.copy(sys.argv[1], os.path.join(out, "seg_000.ts"))
shutil.copy(sys.argv[1], os.path.join(out, "seg_001.ts"))
time.sleep(600)
"""


def test_stall_watchdog_stops_a_recording_that_went_silent(tmp_path, sample_ts, monkeypatch):
    monkeypatch.setattr(SegmentRecorder, "TERM_WAIT_S", 0.5)
    out = tmp_path / "o"
    recorder = SegmentRecorder(
        stand_in(WRITE_THEN_HANG, out, str(sample_ts)), out, segment_seconds=2, stall_timeout=1.0
    )
    recorder.start()
    pid = recorder.pid
    wait_for(lambda: len(list(out.glob("seg_*.ts"))) == 2, 20, "the stand-in to write its files")
    assert [s.path.name for s in recorder.poll()] == ["seg_000.ts"]  # seg_001 is "still being written"
    wait_for(lambda: not recorder.running, 20, "the stall watchdog")
    assert "stopped arriving" in recorder.last_error()
    assert [s.path.name for s in recorder.poll()] == ["seg_001.ts"]  # what was recorded is kept
    assert recorder.stop() == []
    assert_reaped(pid)  # SIGTERM was ignored, so it was killed, and collected


SLEEP_FOREVER = "import time; time.sleep(600)"


def test_startup_watchdog_stops_an_ffmpeg_that_never_gets_a_frame(tmp_path):
    out = tmp_path / "o"
    cmd = stand_in(SLEEP_FOREVER, out, "-f", "avfoundation")
    recorder = SegmentRecorder(cmd, out, segment_seconds=2, startup_timeout=1.0)
    recorder.start()
    pid = recorder.pid
    wait_for(lambda: not recorder.running, 20, "the start-up watchdog")
    reason = recorder.last_error()
    assert "No video arrived within 1 seconds" in reason
    assert "Privacy & Security" in reason and "--audio none" in reason  # what to do about it
    assert recorder.poll() == [] and recorder.stop() == []
    assert_reaped(pid)


def test_watchdogs_can_be_switched_off_and_stop_escalates(tmp_path, sample_ts, monkeypatch):
    monkeypatch.setattr(SegmentRecorder, "QUIT_WAIT_S", 0.3)
    monkeypatch.setattr(SegmentRecorder, "TERM_WAIT_S", 0.5)
    out = tmp_path / "o"
    cmd = stand_in(WRITE_THEN_HANG, out, str(sample_ts))
    recorder = SegmentRecorder(cmd, out, segment_seconds=2, startup_timeout=0, stall_timeout=0)
    recorder.start()
    pid = recorder.pid
    wait_for(lambda: len(list(out.glob("seg_*.ts"))) == 2, 20, "the stand-in to write its files")
    time.sleep(1.2)
    assert recorder.running  # silent for longer than the other tests' limits, but nobody is watching
    started = time.monotonic()
    rest = recorder.stop()  # ignores "q", ignores SIGTERM: must be killed, within the timeouts
    assert time.monotonic() - started < 5
    assert [s.path.name for s in rest] == ["seg_000.ts", "seg_001.ts"]
    assert recorder.running is False and recorder.returncode == -signal.SIGKILL
    assert recorder.last_error() == ""  # the user asked for the stop: not an error
    assert_reaped(pid)


QUITS_ON_Q = """
import os, shutil, sys
out = os.path.dirname(sys.argv[-1])
shutil.copy(sys.argv[1], os.path.join(out, "seg_000.ts"))
open(os.path.join(out, "seg_001.ts"), "wb").close()                  # just opened, still empty
open(os.path.join(out, "seg_notes.txt"), "w").write("not a segment")
sys.stdout.write("ready"); sys.stdout.flush()
key = sys.stdin.buffer.read(1)
open(os.path.join(out, "asked.txt"), "wb").write(key)
sys.exit(0 if key == b"q" else 3)
"""


def test_stop_asks_politely_and_discards_empty_trailing_file(tmp_path, sample_ts):
    out = tmp_path / "o"
    out.mkdir()
    shutil.copy(sample_ts, out / "seg_900.ts")  # left over from an earlier run: not this recorder's business
    recorder = SegmentRecorder(stand_in(QUITS_ON_Q, out, str(sample_ts)), out, segment_seconds=2)
    recorder.start()
    wait_for(lambda: (out / "seg_001.ts").exists(), 20, "the stand-in to open its second file")
    rest = recorder.stop()
    assert (out / "asked.txt").read_bytes() == b"q"  # stdin "q", not a signal
    assert recorder.returncode == 0
    assert [s.path.name for s in rest] == ["seg_000.ts"]
    assert rest[0].duration == pytest.approx(1.0, abs=0.2)
    assert not (out / "seg_001.ts").exists()  # the empty file was removed, not reported
    assert (out / "seg_900.ts").exists() and (out / "seg_notes.txt").exists()  # nothing else was touched


FAKE_CAMERA = """
import os, shutil, sys, time
args = sys.argv
out = os.path.dirname(args[-1])
if args[args.index("-video_size") + 1] != "1920x1080" or args[args.index("-framerate") + 1] != "30":
    sys.stderr.write("[avfoundation @ 0x1] Selected pixel format (nv12) is not supported by the input device.\\n")
    sys.stderr.write("[avfoundation @ 0x1] Supported pixel formats:\\n[avfoundation @ 0x1]   uyvy422\\n")
    sys.stderr.write("[avfoundation @ 0x1] Overriding selected pixel format to use uyvy422 instead.\\n")
    sys.stderr.write("[avfoundation @ 0x1] Selected video size (1280x720) is not supported by the device.\\n")
    sys.stderr.write("[avfoundation @ 0x1] Supported modes:\\n")
    sys.stderr.write("[avfoundation @ 0x1]   1920x1080@[30.000030 30.000030]fps\\n")
    sys.stderr.write("[in#0 @ 0x2] Error opening input: Invalid argument\\n")
    sys.exit(234)
shutil.copy(args[1], os.path.join(out, "seg_000.ts"))
shutil.copy(args[1], os.path.join(out, "seg_001.ts"))
sys.stdin.buffer.read(1)
"""


def test_recorder_retries_once_with_a_mode_the_camera_offers(tmp_path, sample_ts, caplog):
    out = tmp_path / "o"
    cmd = stand_in(
        FAKE_CAMERA, out, str(sample_ts),
        "-f", "avfoundation", "-framerate", "30", "-video_size", "1280x720", "-pixel_format", "nv12", "-i", "1:none",
    )  # fmt: skip
    recorder = SegmentRecorder(cmd, out, segment_seconds=2)
    with caplog.at_level(logging.WARNING, logger="videonotes.capture.live"):
        recorder.start()
        first_pid = recorder.pid
        wait_for(lambda: len(list(out.glob("seg_*.ts"))) == 2, 20, "the second attempt to record")
    assert recorder.running and recorder.pid != first_pid
    assert "1920x1080" in caplog.text and "does not offer" in caplog.text  # the user is told
    assert value_after(recorder.command, "-video_size") == "1920x1080"
    assert recorder.last_error() == ""  # the first attempt's complaint is history
    assert [s.path.name for s in recorder.stop()] == ["seg_000.ts", "seg_001.ts"]
    assert_reaped(first_pid)


ALWAYS_REJECTS = """
import sys
sys.stderr.write("[avfoundation @ 0x1] Selected framerate (30.000000) is not supported by the device.\\n")
sys.stderr.write("[avfoundation @ 0x1] Supported modes:\\n[avfoundation @ 0x1]   1920x1080@[25.000000 25.000000]fps\\n")
sys.exit(234)
"""


def test_recorder_gives_up_when_the_fallback_mode_fails_too(tmp_path):
    out = tmp_path / "o"
    cmd = stand_in(ALWAYS_REJECTS, out, "-f", "avfoundation", "-framerate", "30", "-video_size", "1280x720", "-i", "1")
    recorder = SegmentRecorder(cmd, out, segment_seconds=2)
    recorder.start()
    wait_for(lambda: not recorder.running, 20, "both attempts to fail")
    assert value_after(recorder.command, "-framerate") == "25"  # it did try the offered mode, once
    reason = recorder.last_error()
    assert "capture.video_size" in reason and "1920x1080@[25" in reason  # advice plus the modes to choose from
    assert recorder.stop() == []


ONE_CONNECTION = """
import os, shutil, sys, time
out = os.path.dirname(sys.argv[-1])
runs = os.path.join(out, "runs.txt")
n = len(open(runs).read()) if os.path.exists(runs) else 0
open(runs, "a").write("x")
if n < 2:                                   # two "connections" that deliver a file each, then silence
    shutil.copy(sys.argv[1], os.path.join(out, "seg_%03d.ts" % n))
    time.sleep(0.3)
    sys.stderr.write("[in#0/flv @ 0x1] Error during demuxing: Input/output error\\n")
    sys.exit(0)
sys.stdin.buffer.read(1)                    # waiting for the next connection
"""


def test_listener_is_started_again_after_each_connection(tmp_path, sample_ts):
    out = tmp_path / "o"
    cmd = stand_in(ONE_CONNECTION, out, str(sample_ts), "-listen", "1")
    recorder = SegmentRecorder(cmd, out, segment_seconds=2)
    recorder.start()
    seen: list[str] = []
    stayed_running = True

    def third_run_waiting() -> bool:
        nonlocal stayed_running
        stayed_running = stayed_running and recorder.running  # True between connections as well
        seen.extend(s.path.name for s in recorder.poll())
        return (out / "runs.txt").exists() and len((out / "runs.txt").read_text()) == 3

    wait_for(third_run_waiting, 30, "the listener to be started a third time")
    assert stayed_running
    time.sleep(0.3)
    seen.extend(s.path.name for s in recorder.poll())
    # Both finished connections were handed out although the listener is running (and has no file yet).
    assert seen == ["seg_000.ts", "seg_001.ts"]
    assert recorder.last_error() == ""  # an ended connection is not an error once we listen again
    assert recorder.stop() == [] and recorder.running is False


LISTENER_FAILS = """
import os, sys
out = os.path.dirname(sys.argv[-1])
open(os.path.join(out, "runs.txt"), "a").write("x")
sys.stderr.write("[rtmp @ 0x1] RTMP protocol version mismatch\\n")
sys.exit(251)
"""


def test_listener_that_cannot_start_is_not_restarted(tmp_path):
    out = tmp_path / "o"
    recorder = SegmentRecorder(stand_in(LISTENER_FAILS, out, "-listen", "1"), out, segment_seconds=2)
    recorder.start()
    wait_for(lambda: not recorder.running, 20, "the failed listener to be noticed")
    time.sleep(0.5)
    assert (out / "runs.txt").read_text() == "x"  # one attempt only
    assert "version mismatch" in recorder.last_error() and "251" in recorder.last_error()


def test_listener_gives_up_after_repeated_empty_connections(tmp_path, monkeypatch):
    monkeypatch.setattr(SegmentRecorder, "RELISTEN_BACKOFF_S", 0.01)
    monkeypatch.setattr(SegmentRecorder, "LISTENER_STARTUP_FAIL_S", 0.0)  # treat even instant exits as connections
    monkeypatch.setattr(SegmentRecorder, "MAX_UNPRODUCTIVE_RUNS", 2)
    out = tmp_path / "o"
    recorder = SegmentRecorder(stand_in(LISTENER_FAILS, out, "-listen", "1"), out, segment_seconds=2)
    recorder.start()
    wait_for(lambda: not recorder.running, 30, "the listener to give up")
    assert (out / "runs.txt").read_text() == "xxx"  # the first try and two more
    assert "version mismatch" in recorder.last_error()


def test_recorder_can_be_started_again_and_used_as_context_manager(tmp_path, sample_ts):
    out = tmp_path / "o"
    with SegmentRecorder(stand_in(QUITS_ON_Q, out, str(sample_ts)), out, segment_seconds=2) as recorder:
        recorder.start()  # a second start while running changes nothing
        first_pid = recorder.pid
        wait_for(lambda: (out / "seg_001.ts").exists(), 20, "the stand-in to open its files")
    assert recorder.running is False
    assert_reaped(first_pid)
    assert recorder.poll() == []  # leaving the block stopped it and consumed what was left
    (out / "seg_000.ts").unlink()
    recorder.start()  # a fresh run in the same folder
    assert recorder.running and recorder.pid != first_pid
    wait_for(lambda: (out / "seg_001.ts").exists(), 20, "the stand-in to open its files again")
    recorder.stop()
    assert recorder.running is False


def test_ctrl_c_while_inspecting_a_segment_loses_nothing(tmp_path, sample_ts, monkeypatch):
    out = tmp_path / "o"
    recorder = SegmentRecorder(stand_in(WRITE_THEN_HANG, out, str(sample_ts)), out, segment_seconds=2, stall_timeout=0)
    monkeypatch.setattr(SegmentRecorder, "QUIT_WAIT_S", 0.2)
    monkeypatch.setattr(SegmentRecorder, "TERM_WAIT_S", 0.3)
    recorder.start()
    wait_for(lambda: len(list(out.glob("seg_*.ts"))) == 2, 20, "the stand-in to write its files")
    real = recorder._finalize
    calls: list[str] = []

    def interrupted_once(path: Path):
        calls.append(path.name)
        if len(calls) == 2:
            raise KeyboardInterrupt  # the user presses Ctrl-C while the second file is being probed
        return real(path)

    monkeypatch.setattr(recorder, "_finalize", interrupted_once)
    with pytest.raises(KeyboardInterrupt):
        recorder.stop()
    # what the command line does next (in its `finally`): stop again and take what is left
    assert [s.path.name for s in recorder.stop()] == ["seg_000.ts", "seg_001.ts"]
    assert calls == ["seg_000.ts", "seg_001.ts", "seg_001.ts"]
    assert recorder.stop() == [] and recorder.running is False


def test_interpreter_exit_hook_stops_running_recorders(tmp_path):
    out = tmp_path / "o"
    recorder = SegmentRecorder(stand_in(SLEEP_FOREVER, out), out, segment_seconds=2, startup_timeout=0)
    recorder.start()
    pid = recorder.pid
    assert recorder in live._live_recorders
    live._stop_recorders_at_exit()  # what atexit runs
    wait_for(lambda: not recorder.running, 10, "the recorder to notice")
    assert_reaped(pid)
    assert recorder not in live._live_recorders
    assert recorder.stop() == []


def test_recover_segments_handles_junk(tmp_path, sample_ts):
    assert live.recover_segments(tmp_path / "missing") == []
    out = tmp_path / "o"
    out.mkdir()
    shutil.copy(sample_ts, out / "seg_20261122-143200_1795357920.ts")
    shutil.copy(sample_ts, out / "seg_20261122-143100_1795357860.ts")
    (out / "seg_20261122-143300_1795357980.ts").write_bytes(b"")  # empty
    (out / "seg_20261122-143400_1795358040.ts").write_bytes(b"garbage" * 100)  # unreadable
    (out / "notes.txt").write_text("hello")
    found = live.recover_segments(out)
    assert [s.path.name for s in found] == ["seg_20261122-143100_1795357860.ts", "seg_20261122-143200_1795357920.ts"]
    # the copies' modification times say nothing about 2026-11-22 14:31: the names decide
    assert [s.start_ts for s in found] == [1795357860.0, 1795357920.0]
    assert all(s.duration == pytest.approx(1.0, abs=0.2) for s in found)
    assert len(list(out.iterdir())) == 5  # recovery never deletes anything
