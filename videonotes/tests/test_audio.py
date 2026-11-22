from __future__ import annotations

import numpy as np
import pytest

from videonotes.media import audio
from videonotes.media import ffmpeg as ff

RATE = audio.SAMPLE_RATE


def _tone_burst(seconds: float, freq: float = 800.0, amp: float = 0.2) -> np.ndarray:
    """A crude speech stand-in: an amplitude-modulated tone in the speech band."""
    t = np.arange(int(seconds * RATE)) / RATE
    return (amp * np.sin(2 * np.pi * freq * t) * (0.6 + 0.4 * np.sin(2 * np.pi * 4 * t))).astype(np.float32)


def _silence(seconds: float) -> np.ndarray:
    return np.zeros(int(seconds * RATE), dtype=np.float32)


def test_wav_roundtrip(tmp_path):
    x = _tone_burst(1.0)
    audio.write_wav(tmp_path / "a.wav", x)
    y = audio.read_wav(tmp_path / "a.wav")
    assert y.shape == x.shape and np.abs(x - y).max() < 1e-3
    assert audio.wav_duration(tmp_path / "a.wav") == pytest.approx(1.0)


def test_vad_basic_spans():
    x = np.concatenate([_silence(2), _tone_burst(3), _silence(4), _tone_burst(2), _silence(1)])
    spans = audio.detect_speech(x)
    assert len(spans) == 2
    assert spans[0].t0 == pytest.approx(1.75, abs=0.15) and spans[0].t1 == pytest.approx(5.25, abs=0.15)
    assert spans[1].t0 == pytest.approx(8.75, abs=0.15) and spans[1].t1 == pytest.approx(11.25, abs=0.15)
    assert audio.speech_ratio(spans, 12.0) == pytest.approx(6.0 / 12.0, abs=0.05)


def test_vad_silence_noise_and_wind():
    rng = np.random.default_rng(0)
    assert audio.detect_speech(_silence(5)) == []
    assert audio.detect_speech(np.zeros(10, dtype=np.float32)) == []
    # steady background hiss with no speech: nothing stands out from the floor
    hiss = (0.01 * rng.standard_normal(RATE * 6)).astype(np.float32)
    assert audio.speech_ratio(audio.detect_speech(hiss), 6.0) < 0.1
    # loud low-frequency rumble (wind / handling) must not count as speech
    t = np.arange(RATE * 6) / RATE
    wind = (0.5 * np.sin(2 * np.pi * 40 * t) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.7 * t))).astype(np.float32)
    assert audio.detect_speech(wind) == []
    # speech-band burst on top of hiss + wind is still found
    mix = hiss + wind
    mix[RATE * 2 : RATE * 4] += _tone_burst(2.0)
    spans = audio.detect_speech(mix)
    assert len(spans) == 1 and spans[0].t0 < 2.1 and spans[0].t1 > 3.9


def test_vad_merges_short_gaps_and_keeps_all_speech_clip():
    x = np.concatenate([_tone_burst(1), _silence(0.3), _tone_burst(1)])
    assert len(audio.detect_speech(x)) == 1
    spans = audio.detect_speech(_tone_burst(5))
    assert audio.speech_ratio(spans, 5.0) > 0.9


def test_chunk_spans():
    S = audio.SpeechSpan
    chunks = audio.chunk_spans([S(0, 10), S(10.5, 20), S(40, 45), S(50, 120)], max_chunk_s=28)
    assert all(c.duration <= 28.0 + 1e-6 for c in chunks)
    assert chunks[0].t0 == 0 and chunks[0].t1 == 20  # packed together
    assert chunks[1].t0 == 40 and chunks[1].t1 == 45
    assert chunks[2].t0 == 50 and chunks[-1].t1 == pytest.approx(120)
    assert audio.chunk_spans([]) == []


@pytest.mark.skipif(not ff.have_ffmpeg(), reason="ffmpeg not installed")
def test_extract_audio_from_demo(demo_video, tmp_path):
    wav = tmp_path / "demo.wav"
    dur = audio.extract_audio(demo_video.path, wav)
    assert dur == pytest.approx(demo_video.duration, abs=0.5)
    x = audio.read_wav(wav)
    assert x.dtype == np.float32 and abs(len(x) / RATE - dur) < 0.01
    part = audio.extract_audio(demo_video.path, tmp_path / "part.wav", start=18, duration=10)
    assert part == pytest.approx(10.0, abs=0.2)
    if not demo_video.has_speech:
        pytest.skip("no speech synthesiser available for the demo clip")
    spans = audio.detect_speech(x)
    walking = next(s for s in demo_video.scenes if s.name == "walking")
    for scene in demo_video.scenes:
        covered = sum(max(0.0, min(s.t1, scene.t0 + scene.duration) - max(s.t0, scene.t0)) for s in spans)
        if scene.speech:
            assert covered > 1.5, f"speech in scene {scene.name} was missed"
    covered = sum(max(0.0, min(s.t1, walking.t0 + walking.duration) - max(s.t0, walking.t0)) for s in spans)
    assert covered < 1.0
    assert audio.speech_ratio(spans, dur) < 0.6


@pytest.mark.skipif(not ff.have_ffmpeg(), reason="ffmpeg not installed")
def test_extract_audio_without_audio_stream(tmp_path):
    silent = tmp_path / "silent.mp4"
    ff.run(["-f", "lavfi", "-i", "testsrc2=size=160x120:rate=5:duration=1", "-an", "-c:v", "libx264", "-preset", "ultrafast", str(silent)])
    with pytest.raises(audio.NoAudioError):
        audio.extract_audio(silent, tmp_path / "x.wav")
