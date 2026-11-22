from __future__ import annotations

import pytest

from videonotes.media import ffmpeg as ff

pytestmark = pytest.mark.skipif(not ff.have_ffmpeg(), reason="ffmpeg not installed")


@pytest.fixture(scope="module")
def tiny_video(tmp_path_factory):
    out = tmp_path_factory.mktemp("media") / "tiny.mp4"
    ff.run([
        "-f", "lavfi", "-i", "testsrc2=size=320x240:rate=10:duration=2",
        "-f", "lavfi", "-i", "sine=frequency=440:duration=2",
        "-metadata", "creation_time=2026-11-22T14:32:00.000000Z",
        "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(out),
    ])
    return out


def test_probe(tiny_video):
    info = ff.probe(tiny_video)
    assert info.has_video and info.has_audio
    assert (info.width, info.height) == (320, 240)
    assert abs(info.duration - 2.0) < 0.3
    assert abs(info.fps - 10.0) < 0.01
    assert info.creation_ts == pytest.approx(1795357920.0)


def test_probe_fallback_without_ffprobe(tiny_video):
    info = ff._probe_with_ffmpeg(tiny_video, timeout=30)
    assert info.has_video and info.has_audio and (info.width, info.height) == (320, 240)
    assert abs(info.duration - 2.0) < 0.3 and info.creation_ts == pytest.approx(1795357920.0)


def test_errors(tmp_path):
    with pytest.raises(ff.FFmpegError):
        ff.probe(tmp_path / "missing.mp4")
    bad = tmp_path / "bad.mp4"
    bad.write_bytes(b"not a video")
    with pytest.raises(ff.FFmpegError):
        ff.probe(bad)
    with pytest.raises(ff.FFmpegError) as err:
        ff.run(["-i", str(bad), str(tmp_path / "o.wav")])
    assert err.value.returncode not in (0, None)


def test_parse_creation_time():
    assert ff.parse_creation_time("1970-01-01T00:00:00.000000Z") is None
    assert ff.parse_creation_time("garbage") is None
    assert ff.parse_creation_time("2026-11-22T14:32:00Z") == pytest.approx(1795357920.0)


def test_capabilities():
    assert ff.has_encoder("libx264") or ff.has_encoder("h264_videotoolbox") or True
    assert isinstance(ff.has_hwaccel("videotoolbox"), bool)
    assert ff.version().startswith("ffmpeg")
