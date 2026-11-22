"""Speech-to-text: the shared transcription flow, the four engine adapters, and the factory.

Only sherpa-onnx can run for real here (see the tests marked ``slow``).  The
MLX and CTranslate2 engines are exercised through stand-in modules whose
function signatures were copied from the released wheels (mlx-whisper 0.4.3,
parakeet-mlx 0.7.0, faster-whisper 1.2.1), so a misspelt or unsupported keyword
argument in an adapter fails the test exactly as it would fail on the Mac.
"""

from __future__ import annotations

import dataclasses
import inspect
import io
import math
import os
import sys
import tarfile
import threading
import types
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

import numpy as np
import pytest

from videonotes.backends import asr, modelfetch
from videonotes.backends.asr import EngineResult, Piece, SpeechTranscriber
from videonotes.backends.base import BackendError, BackendUnavailable, Transcriber, TranscriptSegment
from videonotes.media import audio as au
from videonotes.media.audio import SpeechSpan

RATE = 16000
TINY_EN = Path(__file__).resolve().parents[1] / ".test-models" / "sherpa-onnx-whisper-tiny.en"


# -- helpers ---------------------------------------------------------------------------------------


def synth(total_s: float, bursts: list[tuple[float, float, float]], amp: float = 0.3) -> np.ndarray:
    """Digital silence with tone bursts ``(t0, t1, hz)``; the energy VAD takes the bursts for speech."""
    samples = np.zeros(int(total_s * RATE), dtype=np.float32)
    for t0, t1, hz in bursts:
        i0, i1 = int(t0 * RATE), int(t1 * RATE)
        t = np.arange(i1 - i0) / RATE
        samples[i0:i1] = amp * np.sin(2 * np.pi * hz * t)
    return samples


def write(path: Path, samples: np.ndarray) -> Path:
    au.write_wav(path, samples)
    return path


def dominant_hz(samples: np.ndarray) -> int:
    spectrum = np.abs(np.fft.rfft(samples))
    return int(round(np.argmax(spectrum) * RATE / samples.size))


class FakeEngine:
    """An engine that answers from a script and remembers what it was asked."""

    def __init__(self, reply: Any = None, *, max_chunk_s: float = 28.0, detects: str | None = None):
        self.max_chunk_s = max_chunk_s
        self.reply = reply or (lambda samples, language, n: [Piece(0.0, samples.size / RATE, f"chunk {n}")])
        self.detects = detects
        self.calls: list[dict[str, Any]] = []
        self.closed = 0

    def transcribe(self, samples: np.ndarray, language: str | None) -> EngineResult:
        assert samples.dtype == np.float32 and samples.ndim == 1
        self.calls.append({"seconds": samples.size / RATE, "language": language, "hz": dominant_hz(samples)})
        pieces = self.reply(samples, language, len(self.calls) - 1)
        return EngineResult(list(pieces), language=self.detects if language is None else None)

    def close(self) -> None:
        self.closed += 1


class Loader:
    """Spy for the lazy model load."""

    def __init__(self, engine: Any = None, error: Exception | None = None):
        self.engine = engine if engine is not None else FakeEngine()
        self.error = error
        self.count = 0

    def __call__(self) -> Any:
        self.count += 1
        if self.error:
            raise self.error
        return self.engine


def transcriber(loader: Loader, **kwargs: Any) -> SpeechTranscriber:
    return SpeechTranscriber("fake", "model-x", loader, **kwargs)


def fixed_spans(monkeypatch, spans: list[tuple[float, float]]) -> list[int]:
    """Make the VAD return exactly these spans; returns a list that counts the calls."""
    calls: list[int] = []

    def fake(samples: np.ndarray, rate: int = RATE, **_: Any) -> list[SpeechSpan]:
        calls.append(samples.size)
        return [SpeechSpan(a, b) for a, b in spans]

    monkeypatch.setattr(au, "detect_speech", fake)
    return calls


# ==================================================================================================
# The shared flow
# ==================================================================================================


def test_transcriber_satisfies_the_protocol_and_is_lazy():
    loader = Loader()
    t = transcriber(loader)
    assert isinstance(t, Transcriber)
    assert t.name == "fake:model-x"
    assert loader.count == 0 and not t.loaded
    t.close()  # closing something that never loaded is fine
    assert loader.count == 0


def test_silence_returns_nothing_and_never_loads_the_model(tmp_path):
    loader = Loader()
    t = transcriber(loader)
    assert t.transcribe(write(tmp_path / "silence.wav", np.zeros(20 * RATE, dtype=np.float32))) == []
    hiss = (np.random.default_rng(1).standard_normal(20 * RATE) * 0.02).astype(np.float32)
    assert t.transcribe(write(tmp_path / "hiss.wav", hiss)) == []  # steady noise is not speech either
    hum = synth(20, [(0, 20, 440)])
    assert t.transcribe(write(tmp_path / "hum.wav", hum)) == []
    assert loader.count == 0


@pytest.mark.parametrize("seconds", [0.0, 0.05])
def test_empty_and_tiny_files_return_nothing(tmp_path, seconds):
    loader = Loader()
    for vad in (True, False):
        t = transcriber(loader, vad=vad)
        assert t.transcribe(write(tmp_path / "tiny.wav", np.full(int(seconds * RATE), 0.2, dtype=np.float32))) == []
    assert loader.count == 0


def test_unreadable_input_is_a_clear_backend_error(tmp_path):
    t = transcriber(Loader())
    with pytest.raises(BackendError, match="not found"):
        t.transcribe(tmp_path / "missing.wav")
    garbage = tmp_path / "garbage.wav"
    garbage.write_bytes(os.urandom(2000))
    with pytest.raises(BackendError, match="not a readable WAV"):
        t.transcribe(garbage)
    (tmp_path / "empty.wav").write_bytes(b"")
    with pytest.raises(BackendError, match="not a readable WAV"):
        t.transcribe(tmp_path / "empty.wav")
    au.write_wav(tmp_path / "8k.wav", synth(2, [(0.5, 1.5, 440)]), rate=8000)
    with pytest.raises(BackendError, match="16 kHz"):
        t.transcribe(tmp_path / "8k.wav")


def test_truncated_wav_is_transcribed_as_far_as_it_goes(tmp_path):
    """A recording cut off mid-write (header promises more audio than the file holds)."""
    path = write(tmp_path / "cut.wav", synth(20, [(2, 4, 440), (15, 17, 880)]))
    data = path.read_bytes()
    path.write_bytes(data[: 44 + 10 * RATE * 2])  # keep only the first 10 s of samples
    engine = FakeEngine()
    segments = transcriber(Loader(engine)).transcribe(path)
    assert [c["hz"] for c in engine.calls] == [440]
    assert len(segments) == 1 and 1.5 < segments[0].t0 < 2.1


def test_chunks_are_cut_from_the_right_place_and_timestamps_shift_back_to_file_time(tmp_path):
    # three "utterances", each a different pitch so the engine can tell which audio it was given
    path = write(tmp_path / "talk.wav", synth(90, [(5, 8, 400), (40, 44, 800), (70, 72, 1600)]))
    engine = FakeEngine(lambda samples, language, n: [Piece(0.5, 1.5, f"utterance {n}")])
    segments = transcriber(Loader(engine), language="en").transcribe(path)  # known language: chunks go in time order

    assert [c["hz"] for c in engine.calls] == [400, 800, 1600]
    assert [s.text for s in segments] == ["utterance 0", "utterance 1", "utterance 2"]
    for segment, (burst_start, _, _) in zip(segments, [(5, 8, 0), (40, 44, 0), (70, 72, 0)], strict=True):
        # chunk starts 0.25 s (VAD padding) before the burst; the piece starts 0.5 s into the chunk
        assert segment.t0 == pytest.approx(burst_start - 0.25 + 0.5, abs=0.1)
        assert segment.t1 - segment.t0 == pytest.approx(1.0, abs=1e-6)
    assert all(isinstance(s, TranscriptSegment) and type(s.t0) is float and type(s.t1) is float for s in segments)
    assert all(c["seconds"] < 5.0 for c in engine.calls)  # only the speech was decoded, not 90 s


def test_timestamps_are_clamped_to_the_chunk(tmp_path, monkeypatch):
    path = write(tmp_path / "a.wav", synth(30, [(10, 14, 440)]))
    fixed_spans(monkeypatch, [(10.0, 14.0)])
    engine = FakeEngine(
        lambda samples, language, n: [
            Piece(-3.0, 1.0, "starts before the chunk"),
            Piece(2.0, 99.0, "ends after the chunk"),  # Whisper rounds segment ends up past the audio
            Piece(math.nan, math.nan, "no usable times"),
            Piece(3.5, 3.0, "ends before it starts"),
        ]
    )
    by_text = {s.text: s for s in transcriber(Loader(engine)).transcribe(path)}
    assert (by_text["starts before the chunk"].t0, by_text["starts before the chunk"].t1) == (10.0, 11.0)
    assert (by_text["ends after the chunk"].t0, by_text["ends after the chunk"].t1) == (12.0, 14.0)
    assert (by_text["no usable times"].t0, by_text["no usable times"].t1) == (10.0, 14.0)
    assert by_text["ends before it starts"].t0 == by_text["ends before it starts"].t1 == 13.5
    assert all(s.t0 <= s.t1 for s in by_text.values())


def test_text_outside_detected_speech_is_dropped(tmp_path, monkeypatch):
    """Long-form engines get speech islands that include short pauses; text invented in a pause goes."""
    path = write(tmp_path / "a.wav", synth(60, [(10, 12, 440), (13.8, 16, 440)]))
    fixed_spans(monkeypatch, [(10.0, 12.0), (13.8, 16.0)])  # 1.8 s apart: one chunk
    engine = FakeEngine(
        lambda samples, language, n: [
            Piece(0.2, 1.8, "real one"),
            Piece(2.7, 3.1, "invented in the pause"),  # file time 12.7-13.1, more than 0.5 s from any speech
            Piece(2.1, 2.4, "just after the first span"),  # 12.1-12.4: within tolerance, kept
            Piece(4.0, 5.5, "real two"),
        ],
        max_chunk_s=600.0,
    )
    segments = transcriber(Loader(engine)).transcribe(path)
    assert len(engine.calls) == 1 and engine.calls[0]["seconds"] == pytest.approx(6.0)
    assert [s.text for s in segments] == ["real one", "just after the first span", "real two"]
    assert segments[-1].t0 == pytest.approx(14.0)


def test_place_pieces_evidence_fields():
    spans = [SpeechSpan(10.0, 12.0)]
    chunk = SpeechSpan(10.0, 14.0)
    samples = np.concatenate([np.full(2 * RATE, 0.25, dtype=np.float32), np.zeros(2 * RATE, dtype=np.float32)])
    loud, half, quiet = asr.place_pieces(
        [Piece(0.0, 2.0, "loud"), Piece(1.0, 3.0, "half"), Piece(2.2, 2.4, "quiet")], chunk, samples, spans
    )
    assert loud.speech_fraction == pytest.approx(1.0) and loud.level_db == pytest.approx(-12.04, abs=0.1)
    assert half.speech_fraction == pytest.approx(0.5)
    assert quiet.speech_fraction == 0.0 and quiet.level_db < -100
    assert asr.place_pieces([Piece(3.0, 3.5, "far")], chunk, samples, spans) == []
    # without VAD there are no spans: nothing is dropped and the fraction is unknown
    (free,) = asr.place_pieces([Piece(3.0, 3.5, "far")], chunk, samples, None)
    assert free.speech_fraction is None and (free.t0, free.t1) == (13.0, 13.5)


def test_place_pieces_instant_and_unknown_end():
    spans = [SpeechSpan(10.0, 12.0)]
    chunk = SpeechSpan(10.0, 14.0)
    samples = np.full(4 * RATE, 0.1, dtype=np.float32)
    inside, near = asr.place_pieces([Piece(1.0, 1.0, "inside"), Piece(2.3, 2.3, "near")], chunk, samples, spans)
    assert (inside.t0, inside.t1, inside.speech_fraction) == (11.0, 11.0, 1.0)
    assert near.speech_fraction == 0.0  # within tolerance of the speech, so kept, but not inside it
    (open_ended,) = asr.place_pieces([Piece(0.5, math.nan, "no end time")], chunk, samples, spans)
    assert (open_ended.t0, open_ended.t1) == (10.5, 14.0)  # runs to the end of the chunk


def test_vad_off_transcribes_everything_in_engine_sized_chunks(tmp_path, monkeypatch):
    calls = fixed_spans(monkeypatch, [])  # would say "no speech" if it were asked
    path = write(tmp_path / "a.wav", synth(70, [(5, 8, 440), (60, 62, 440)]))
    engine = FakeEngine(max_chunk_s=28.0)
    segments = transcriber(Loader(engine), vad=False).transcribe(path)
    assert calls == []
    assert len(engine.calls) == 3 and sum(c["seconds"] for c in engine.calls) == pytest.approx(70.0, abs=0.01)
    assert all(c["seconds"] <= 28.0 + asr.CUT_SEARCH_S for c in engine.calls)
    assert [s.t0 for s in segments] == sorted(s.t0 for s in segments) and segments[0].t0 == 0.0
    assert segments[-1].t1 == pytest.approx(70.0, abs=0.01)


def test_long_speech_is_cut_at_a_quiet_instant_not_mid_word():
    samples = synth(60, [(0, 60, 440)])
    for dip in (19.3, 41.1):  # 100 ms pauses near where equal cuts (20 s, 40 s) would land
        samples[int(dip * RATE) : int((dip + 0.1) * RATE)] = 0.0

    def read(t0: float, t1: float) -> np.ndarray:
        return samples[int(t0 * RATE) : int(t1 * RATE)]

    blind = asr.plan_chunks([SpeechSpan(0.0, 60.0)], 28.0)
    assert [round(c.t1, 2) for c in blind] == [20.0, 40.0, 60.0]
    chunks = asr.plan_chunks([SpeechSpan(0.0, 60.0)], 28.0, read)
    assert chunks[0].t1 == pytest.approx(19.35, abs=0.03) and chunks[1].t1 == pytest.approx(41.15, abs=0.03)
    assert all(a.t1 == b.t0 for a, b in zip(chunks, chunks[1:], strict=False))  # nothing lost, nothing doubled
    assert all(c.t1 - c.t0 <= 28.0 + asr.CUT_SEARCH_S for c in chunks)
    # chunks separated by a real pause are left alone
    apart = asr.plan_chunks([SpeechSpan(0.0, 5.0), SpeechSpan(20.0, 25.0)], 28.0, read)
    assert [(c.t0, c.t1) for c in apart] == [(0.0, 5.0), (20.0, 25.0)]


def test_quietest_offset():
    samples = np.full(RATE, 0.5, dtype=np.float32)
    samples[int(0.70 * RATE) : int(0.78 * RATE)] = 0.0
    assert asr.quietest_offset(samples) == pytest.approx(0.74, abs=0.03)
    assert asr.quietest_offset(np.full(RATE, 0.5, dtype=np.float32)) == pytest.approx(0.5, abs=0.03)  # tie: middle
    assert asr.quietest_offset(np.zeros(10, dtype=np.float32)) == pytest.approx(10 / RATE / 2)


def test_long_files_are_scanned_in_blocks_with_bounded_reads(tmp_path, monkeypatch):
    """Stands in for an hour-long recording: the same code path, with the block size turned down."""
    monkeypatch.setattr(asr, "_VAD_WHOLE_FILE_S", 20.0)
    monkeypatch.setattr(asr, "_VAD_BLOCK_S", 10.0)
    # one utterance straddles the 10 s block boundary, one sits in the last block
    path = write(tmp_path / "long.wav", synth(44, [(3, 4, 440), (9, 11.5, 660), (33, 35, 880)]))
    reads: list[float] = []
    real_read = asr.WavReader.read

    def spy(self: asr.WavReader, t0: float, t1: float) -> np.ndarray:
        reads.append(t1 - t0)
        return real_read(self, t0, t1)

    monkeypatch.setattr(asr.WavReader, "read", spy)
    with asr.WavReader(path) as wav:
        spans = asr.find_speech(wav)
    assert len(spans) == 3  # the utterance across the block boundary is one span, not two
    for span, (t0, t1) in zip(spans, [(2.75, 4.25), (8.75, 11.75), (32.75, 35.25)], strict=True):
        assert span.t0 == pytest.approx(t0, abs=0.1) and span.t1 == pytest.approx(t1, abs=0.1)
    # ten-second blocks; a tail shorter than half a block is folded into the last one
    assert reads == pytest.approx([10.0, 10.0, 10.0, 14.0])


def test_block_scan_matches_whole_file_scan_on_real_speech(demo_video, tmp_path, monkeypatch):
    if not demo_video.has_speech:
        pytest.skip("no speech synthesiser available for the demo clip")
    wav_path = tmp_path / "demo.wav"
    au.extract_audio(demo_video.path, wav_path)
    with asr.WavReader(wav_path) as wav:
        whole = asr.find_speech(wav)
        monkeypatch.setattr(asr, "_VAD_WHOLE_FILE_S", 30.0)
        monkeypatch.setattr(asr, "_VAD_BLOCK_S", 30.0)
        blocks = asr.find_speech(wav)
    assert len(blocks) == len(whole) >= 4
    for a, b in zip(whole, blocks, strict=True):
        assert a.t0 == pytest.approx(b.t0, abs=0.3) and a.t1 == pytest.approx(b.t1, abs=0.3)


def test_stereo_wav_is_mixed_down(tmp_path):
    import wave

    mono = synth(10, [(3, 5, 440)])
    stereo = np.stack([mono, np.zeros_like(mono)], axis=1)
    with wave.open(str(tmp_path / "stereo.wav"), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes((stereo * 32767).astype("<i2").tobytes())
    engine = FakeEngine()
    segments = transcriber(Loader(engine)).transcribe(tmp_path / "stereo.wav")
    assert len(segments) == 1 and engine.calls[0]["hz"] == 440
    assert engine.calls[0]["seconds"] == pytest.approx(2.5, abs=0.15)


# -- language ----------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("value", "expected"),
    [(None, None), ("", None), ("auto", None), (" AUTO ", None), ("en", "en"), ("EN", "en"), ("en-US", "en"),
     ("pt_BR", "pt"), ("zh-Hans", "zh"), ("<|de|>", "de")],
)  # fmt: skip
def test_normalise_language(value, expected):
    assert asr.normalise_language(value) == expected


def test_language_from_settings_and_per_call_override(tmp_path, monkeypatch):
    path = write(tmp_path / "a.wav", synth(20, [(5, 8, 440)]))
    fixed_spans(monkeypatch, [(5.0, 8.0)])
    for configured, per_call, expected in [
        ("auto", None, None),
        ("en", None, "en"),
        ("en-GB", None, "en"),
        ("en", "de", "de"),
        ("auto", "fr", "fr"),
        ("de", "auto", "de"),  # "auto" per call means "no opinion": the configured language stands
    ]:
        engine = FakeEngine()
        transcriber(Loader(engine), language=configured).transcribe(path, language=per_call)
        assert [c["language"] for c in engine.calls] == [expected], (configured, per_call)


def test_detected_language_of_the_longest_chunk_is_kept_for_the_file(tmp_path, monkeypatch):
    path = write(tmp_path / "a.wav", synth(120, [(5, 6, 300), (30, 45, 600), (80, 82, 1200), (100, 101, 2400)]))
    fixed_spans(monkeypatch, [(5.0, 6.0), (30.0, 45.0), (80.0, 82.0), (100.0, 101.0)])
    engine = FakeEngine(detects="DE")
    segments = transcriber(Loader(engine)).transcribe(path)
    # the 15 s chunk goes first without a language; what it detects is used for the short ones
    assert [(c["hz"], c["language"]) for c in engine.calls] == [(600, None), (300, "de"), (1200, "de"), (2400, "de")]
    assert [s.t0 for s in segments] == [5.0, 30.0, 80.0, 100.0]  # output is in time order regardless

    monolingual = FakeEngine(detects=None)  # an engine that reports nothing keeps getting None
    transcriber(Loader(monolingual)).transcribe(path)
    assert [c["language"] for c in monolingual.calls] == [None] * 4

    pinned = FakeEngine(detects="de")
    transcriber(Loader(pinned), language="en").transcribe(path)
    assert [(c["hz"], c["language"]) for c in pinned.calls] == [(300, "en"), (600, "en"), (1200, "en"), (2400, "en")]


# -- failures and lifecycle ----------------------------------------------------------------------------


def test_engine_failure_becomes_backend_error_naming_the_file(tmp_path):
    def explode(samples: np.ndarray, language: str | None, n: int) -> list[Piece]:
        raise ValueError("Unsupported language: xx")

    path = write(tmp_path / "meeting.wav", synth(20, [(5, 8, 440)]))
    with pytest.raises(BackendError, match=r"fake:model-x failed on meeting\.wav.*Unsupported language: xx"):
        transcriber(Loader(FakeEngine(explode))).transcribe(path)


def test_keyboard_interrupt_is_not_swallowed(tmp_path):
    def interrupt(samples: np.ndarray, language: str | None, n: int) -> list[Piece]:
        raise KeyboardInterrupt

    path = write(tmp_path / "a.wav", synth(20, [(5, 8, 440)]))
    t = transcriber(Loader(FakeEngine(interrupt)))
    with pytest.raises(KeyboardInterrupt):
        t.transcribe(path)
    t.close()


def test_failed_model_load_is_reported_once_and_not_retried_per_clip(tmp_path):
    path = write(tmp_path / "a.wav", synth(20, [(5, 8, 440)]))
    loader = Loader(error=BackendUnavailable("could not download; do X"))
    t = transcriber(loader)
    for _ in range(3):
        with pytest.raises(BackendUnavailable, match="do X"):
            t.transcribe(path)
    assert loader.count == 1  # e.g. offline: the download is not attempted again for every clip

    loader = Loader(error=MemoryError("out of memory"))
    t = transcriber(loader)
    with pytest.raises(BackendUnavailable, match="could not be loaded.*MemoryError"):
        t.transcribe(path)
    # close() forgets the failure, so a later run can try again
    t.close()
    loader.error = None
    assert len(t.transcribe(path)) == 1 and loader.count == 2


def test_close_releases_the_engine_and_it_reloads_on_demand(tmp_path):
    path = write(tmp_path / "a.wav", synth(20, [(5, 8, 440)]))
    engine = FakeEngine()
    loader = Loader(engine)
    t = transcriber(loader)
    t.transcribe(path)
    t.transcribe(path)
    assert loader.count == 1 and t.loaded
    t.close()
    t.close()
    assert engine.closed == 1 and not t.loaded
    t.transcribe(path)
    assert loader.count == 2

    class BadClose(FakeEngine):
        def close(self) -> None:
            raise RuntimeError("metal said no")

    t = transcriber(Loader(BadClose()))
    t.transcribe(path)
    t.close()  # must not raise: the pipeline closes backends on its way out
    assert not t.loaded


# ==================================================================================================
# Text clean-up
# ==================================================================================================


def texts(pieces: list[Piece]) -> list[str]:
    return [s.text for s in asr.postprocess(pieces)]


def test_whitespace_and_empty_segments():
    assert texts(
        [Piece(0, 1, "  Hello \n  there\tworld  "), Piece(1, 2, "   "), Piece(2, 3, ""), Piece(3, 4, " ... ")]
    ) == ["Hello there world"]


def test_output_is_sorted_and_well_formed():
    segments = asr.postprocess([Piece(5.0, 4.0, "second"), Piece(np.float64(1.23456), np.float32(2.0), "first")])
    assert [(s.t0, s.t1, s.text) for s in segments] == [(1.235, 2.0, "first"), (5.0, 5.0, "second")]
    assert all(type(s.t0) is float and type(s.t1) is float and s.speaker is None for s in segments)


@pytest.mark.parametrize(
    "tag",
    ["[ Silence ]", "(wind howling)", "[BLANK_AUDIO]", "[MUSIC]", "(music)", "*laughs*", "♪♪", "[Music] [Clap]"],
)
def test_non_speech_tags_are_dropped(tag):
    assert texts([Piece(0, 2, tag)]) == []
    assert texts([Piece(0, 2, f"Wait {tag} what was that?")]) == [f"Wait {tag} what was that?"]


@pytest.mark.parametrize(
    "text",
    [
        "Thanks for watching!",
        "Thank you for watching.",
        "thank you so much for watching",
        "Thanks for watching, and I'll see you in the next video.",
        "Subtitles by the Amara.org community",
        "Subtitles made by DimaTorzok",
        "Captions by someone",
        "Sous-titres réalisés par la communauté d'Amara.org",
    ],
)
def test_caption_credit_hallucinations_are_dropped_even_over_real_sound(text):
    loud = Piece(0, 2, text, speech_fraction=1.0, level_db=-20.0)
    assert texts([loud]) == []


def test_phantom_filter_only_touches_short_segments():
    long_real = (
        "Thanks for watching the kids yesterday, it really helped me get through the budget review "
        "and the planning meeting on time."
    )
    assert texts([Piece(0, 8, long_real, speech_fraction=1.0, level_db=-20.0)]) == [long_real]
    assert texts([Piece(0, 2, "I said thanks for watching the dog.", speech_fraction=1.0, level_db=-20.0)]) == [
        "I said thanks for watching the dog."
    ]


@pytest.mark.parametrize("text", ["you", "You.", "Thank you.", "Thank you very much.", "Thanks.", "Bye.", "Bye-bye."])
def test_everyday_phrases_are_dropped_only_over_near_silence(text):
    spoken = Piece(10.0, 11.2, text, speech_fraction=1.0, level_db=-22.0, no_speech_prob=0.05)
    assert texts([spoken]) == [text]  # somebody really said it: keep
    for weak in (
        dataclasses.replace(spoken, level_db=-63.0),  # the audio under it is next to silent
        dataclasses.replace(spoken, speech_fraction=0.2),  # mostly outside detected speech
        dataclasses.replace(spoken, no_speech_prob=0.8),  # Whisper itself doubts there was speech
        dataclasses.replace(spoken, t1=18.0),  # two words "lasting" eight seconds
    ):
        assert texts([weak]) == []
    # the near-silence rule is about lone stock phrases, not about speech in general
    assert texts([Piece(10.0, 18.0, "Thank you for the flowers, they are lovely.", level_db=-63.0)]) == [
        "Thank you for the flowers, they are lovely."
    ]
    assert texts([Piece(10.0, 11.0, "You know what?", level_db=-63.0)]) == ["You know what?"]


def test_whisper_no_speech_verdict_is_respected():
    doubtful = Piece(0, 3, "And that's how it works.", no_speech_prob=0.9, avg_logprob=-1.4)
    assert texts([doubtful]) == []
    assert texts([dataclasses.replace(doubtful, avg_logprob=-0.3)]) == ["And that's how it works."]
    assert texts([dataclasses.replace(doubtful, no_speech_prob=0.2)]) == ["And that's how it works."]


def test_exact_consecutive_repeats_collapse():
    looped = [Piece(float(i), i + 1.0, "I'm not sure." if i % 2 == 0 else " i'm not sure ") for i in range(6)]
    result = asr.postprocess(looped)
    assert [(s.t0, s.text) for s in result] == [(0.0, "I'm not sure.")]
    # the same words again much later are a second remark, not a loop
    apart = asr.postprocess([Piece(0, 1, "Okay."), Piece(60, 61, "Okay."), Piece(61.5, 62, "Okay.")])
    assert [s.t0 for s in apart] == [0.0, 60.0]
    # a repeat with something else in between is kept
    assert texts([Piece(0, 1, "Yes."), Piece(1, 2, "No."), Piece(2, 3, "Yes.")]) == ["Yes.", "No.", "Yes."]


def test_repetition_loops_inside_one_segment():
    assert asr.collapse_repeated_sentences("I see. I see. I see. Right.") == "I see. Right."
    assert asr.collapse_repeated_sentences("No repeats here. None at all.") == "No repeats here. None at all."
    assert texts([Piece(0, 20, "We should go. " + "I don't know. " * 12)]) == ["We should go. I don't know."]
    # a loop without sentence breaks is caught by Whisper's own measure (text that compresses too well)
    assert asr.compression_ratio("word " * 60) > 2.4
    assert texts([Piece(0, 28, "and the and the " * 30)]) == []
    assert texts([Piece(0, 5, "fine", compression_ratio=3.1)]) == []  # the engine's own verdict counts too
    normal = "Remember to email the quarterly budget to Sarah before Friday, and call the vendor about the sensors."
    assert asr.compression_ratio(normal) < 1.5 and texts([Piece(0, 5, normal)]) == [normal]


def test_pieces_from_tokens_groups_sentences():
    tokens = [" Hello", ",", " wor", "ld", ".", " How", " are", " you", "?", " Fine"]
    starts = [0.0, 0.3, 0.4, 0.6, 0.8, 1.2, 1.4, 1.6, 1.8, 6.0]
    durations = [0.2, 0.1, 0.2, 0.2, 0.1, 0.2, 0.2, 0.2, 0.1, 0.4]
    pieces = asr.pieces_from_tokens(tokens, starts, durations, 7.0)
    assert [(p.text, p.t0, round(p.t1, 2)) for p in pieces] == [
        ("Hello, world.", 0.0, 0.9),
        ("How are you?", 1.2, 1.9),
        ("Fine", 6.0, 6.4),
    ]
    # no punctuation: a long pause ends the piece; without durations the next token's start is the end
    pieces = asr.pieces_from_tokens(["▁so", "▁then", "▁later"], [0.0, 0.5, 4.0], None, 5.0)
    assert [(p.text, p.t0, p.t1) for p in pieces] == [("so then", 0.0, 1.0), ("later", 4.0, 4.3)]
    pieces = asr.pieces_from_tokens(["▁so", "▁then", "▁later"], [0.0, 0.5, 4.0], [0.3, 0.3, 0.3], 5.0)
    assert [(p.text, p.t0, p.t1) for p in pieces] == [("so then", 0.0, 0.8), ("later", 4.0, 4.3)]
    # a decimal point or an abbreviation inside a word does not end the sentence
    pieces = asr.pieces_from_tokens(
        [" It", " costs", " 3", ".", "5", " dollars", "."], [0, 0.2, 0.4, 0.5, 0.6, 0.7, 0.9], None, 2.0
    )
    assert [p.text for p in pieces] == ["It costs 3.5 dollars."]
    # endless unpunctuated speech is still cut into pieces of bounded length, at word boundaries
    many = asr.pieces_from_tokens([" word"] * 100, [i * 0.5 for i in range(100)], [0.4] * 100, 50.0, max_s=10.0)
    assert len(many) >= 4 and all(p.t1 - p.t0 <= 10.5 for p in many)
    assert " ".join(p.text for p in many).split() == ["word"] * 100
    assert asr.pieces_from_tokens([], [], [], 3.0) == []
    assert asr.pieces_from_tokens([" a"], [9.0], [5.0], 9.5)[0].t1 == 9.5  # never past the end of the audio


# ==================================================================================================
# Engine adapters, against stand-ins with the real signatures
# ==================================================================================================

SAMPLES = (np.sin(np.arange(3 * RATE) / 20.0) * 0.1).astype(np.float32)


class Spy:
    def __init__(self, result: Any = None):
        self.calls: list[tuple[tuple, dict]] = []
        self.result = result

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        self.calls.append((args, kwargs))
        return self.result


@pytest.fixture()
def fake_mlx(monkeypatch):
    """``mlx.core`` with the two things the adapters touch."""
    core = types.ModuleType("mlx.core")
    core.float16 = "mx.float16"
    core.clear_cache = Spy()
    core.array = lambda data: ("mx.array", data)
    package = types.ModuleType("mlx")
    package.core = core
    monkeypatch.setitem(sys.modules, "mlx", package)
    monkeypatch.setitem(sys.modules, "mlx.core", core)
    return core


# decode options accepted by mlx_whisper.decoding.DecodingOptions (mlx-whisper 0.4.3)
MLX_DECODE_OPTIONS = {
    "task", "language", "temperature", "sample_len", "best_of", "beam_size", "patience", "length_penalty",
    "prompt", "prefix", "suppress_tokens", "suppress_blank", "without_timestamps", "max_initial_timestamp", "fp16",
}  # fmt: skip


@pytest.fixture()
def fake_mlx_whisper(monkeypatch, fake_mlx):
    state = types.SimpleNamespace(calls=[], loads=[], result=None, load_error=None)

    class ModelHolder:  # mlx_whisper/transcribe.py: class-level cache of the loaded model
        model = None
        model_path = None

        @classmethod
        def get_model(cls, model_path: str, dtype: Any) -> Any:
            if state.load_error:
                raise state.load_error
            state.loads.append((model_path, dtype))
            cls.model, cls.model_path = object(), model_path
            return cls.model

    def transcribe(  # signature of mlx_whisper.transcribe.transcribe in the 0.4.3 wheel
        audio,
        *,
        path_or_hf_repo="mlx-community/whisper-tiny",
        verbose=None,
        temperature=(0.0, 0.2, 0.4, 0.6, 0.8, 1.0),
        compression_ratio_threshold=2.4,
        logprob_threshold=-1.0,
        no_speech_threshold=0.6,
        condition_on_previous_text=True,
        initial_prompt=None,
        word_timestamps=False,
        prepend_punctuations="\"'“¿([{-",
        append_punctuations="\"'.。,，!！?？:：”)]}、",
        clip_timestamps="0",
        hallucination_silence_threshold=None,
        **decode_options,
    ):
        assert set(decode_options) <= MLX_DECODE_OPTIONS, f"not a DecodingOptions field: {set(decode_options)}"
        ModelHolder.get_model(path_or_hf_repo, "mx.float16")
        state.calls.append(
            {
                "audio": audio,
                "path_or_hf_repo": path_or_hf_repo,
                "verbose": verbose,
                "condition_on_previous_text": condition_on_previous_text,
                "word_timestamps": word_timestamps,
                "hallucination_silence_threshold": hallucination_silence_threshold,
                "clip_timestamps": clip_timestamps,
                "temperature": temperature,
                "no_speech_threshold": no_speech_threshold,
                "decode_options": decode_options,
            }
        )
        return state.result

    package = types.ModuleType("mlx_whisper")
    submodule = types.ModuleType("mlx_whisper.transcribe")
    submodule.ModelHolder = ModelHolder
    submodule.transcribe = transcribe
    package.transcribe = transcribe  # as in the real package, the function shadows the submodule
    monkeypatch.setitem(sys.modules, "mlx_whisper", package)
    monkeypatch.setitem(sys.modules, "mlx_whisper.transcribe", submodule)
    state.holder = ModelHolder
    return state


def test_mlx_whisper_adapter_calls_and_mapping(fake_mlx, fake_mlx_whisper):
    model = "mlx-community/whisper-large-v3-turbo"
    engine = asr.MlxWhisperEngine(model)
    assert engine.max_chunk_s == 600.0
    assert fake_mlx_whisper.loads == [(model, "mx.float16")]  # loaded up front, in the dtype transcribe() uses

    fake_mlx_whisper.result = {
        "text": " Hello there. General remark.",
        "language": "en",
        "segments": [
            {"id": 0, "seek": 0, "start": 0.52, "end": 1.9, "text": " Hello there.", "tokens": [1], "temperature": 0.0,
             "avg_logprob": -0.21, "compression_ratio": 1.1, "no_speech_prob": 0.02, "words": []},
            {"id": 1, "seek": 0, "start": 2.0, "end": 2.9, "text": " General remark.", "tokens": [2], "temperature": 0,
             "avg_logprob": float("nan"), "compression_ratio": 0.9, "no_speech_prob": 0.01, "words": []},
            {"id": 2, "seek": 0, "start": 2.9, "end": 2.9, "text": "", "tokens": [], "temperature": 0.0,
             "avg_logprob": -0.5, "compression_ratio": 1.0, "no_speech_prob": 0.4, "words": []},
        ],
    }  # fmt: skip
    result = engine.transcribe(SAMPLES, None)

    (call,) = fake_mlx_whisper.calls
    assert call["audio"] is SAMPLES  # in-memory float32 audio: no ffmpeg lookup inside the library
    assert call["path_or_hf_repo"] == model  # never the library default (whisper-tiny in 0.4.3)
    assert call["verbose"] is None
    assert call["condition_on_previous_text"] is False
    assert call["word_timestamps"] is True and call["hallucination_silence_threshold"] == 2.0
    assert call["decode_options"] == {"language": None}
    assert call["clip_timestamps"] == "0"  # not used: 0.4.3 does not skip the gaps between clips
    assert call["temperature"] == (0.0, 0.2, 0.4, 0.6, 0.8, 1.0) and call["no_speech_threshold"] == 0.6
    assert result.language == "en"
    assert [(p.t0, p.t1, p.text) for p in result.pieces] == [
        (0.52, 1.9, " Hello there."),
        (2.0, 2.9, " General remark."),
        (2.9, 2.9, ""),
    ]
    assert (result.pieces[0].no_speech_prob, result.pieces[0].avg_logprob, result.pieces[0].compression_ratio) == (
        0.02,
        -0.21,
        1.1,
    )
    assert result.pieces[1].avg_logprob is None  # NaN means "unknown", not "terrible"

    told = engine.transcribe(SAMPLES, "de")
    assert fake_mlx_whisper.calls[-1]["decode_options"] == {"language": "de"}
    assert told.language is None  # nothing was detected; the caller already knows
    assert fake_mlx_whisper.loads == [(model, "mx.float16")] * 3

    engine.close()
    assert fake_mlx_whisper.holder.model is None and fake_mlx_whisper.holder.model_path is None
    assert len(fake_mlx.clear_cache.calls) == 1


def test_mlx_cache_clear_falls_back_to_the_old_location(fake_mlx, fake_mlx_whisper):
    old = Spy()
    del fake_mlx.clear_cache
    fake_mlx.metal = types.SimpleNamespace(clear_cache=old)
    asr.MlxWhisperEngine("m").close()
    assert len(old.calls) == 1


def test_mlx_whisper_load_failure_explains_the_download(fake_mlx, fake_mlx_whisper):
    fake_mlx_whisper.load_error = OSError("We couldn't connect to 'https://huggingface.co'")
    with pytest.raises(BackendUnavailable) as err:
        asr.MlxWhisperEngine("mlx-community/whisper-large-v3-turbo")
    message = str(err.value)
    assert "mlx-community/whisper-large-v3-turbo" in message and "Hugging Face" in message
    assert "internet connection" in message and "asr.model" in message


def test_broken_install_is_not_reported_as_missing(monkeypatch, fake_mlx):
    """The package is there but one of its own dependencies is not: say so, with the reinstall command."""
    import builtins

    real_import = builtins.__import__

    def failing_import(name: str, *args: Any, **kwargs: Any) -> Any:
        if name == "mlx_whisper":
            raise ImportError("cannot import name 'jit' from 'numba'")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", failing_import)
    with pytest.raises(BackendUnavailable) as err:
        asr.MlxWhisperEngine("m")
    assert "installed but could not be started" in str(err.value) and "numba" in str(err.value)
    assert "pip install --upgrade mlx-whisper" in str(err.value)

    def missing_import(name: str, *args: Any, **kwargs: Any) -> Any:
        if name == "mlx_whisper":
            raise ModuleNotFoundError("No module named 'mlx_whisper'", name="mlx_whisper")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", missing_import)
    with pytest.raises(BackendUnavailable, match="is not installed. Install it with:  pip install mlx-whisper"):
        asr.MlxWhisperEngine("m")


def test_mlx_whisper_through_the_whole_flow(tmp_path, monkeypatch, settings, fake_mlx, fake_mlx_whisper):
    monkeypatch.setattr(asr, "module_available", lambda module: True)
    settings.asr.backend = "mlx-whisper"
    settings.asr.language = "en"
    fixed_spans(monkeypatch, [(5.0, 8.0)])
    fake_mlx_whisper.result = {
        "language": "en",
        "segments": [
            {"start": 0.4, "end": 2.6, "text": " Remember the  budget.", "no_speech_prob": 0.01, "avg_logprob": -0.2,
             "compression_ratio": 1.0},
            {"start": 2.6, "end": 3.0, "text": " Thanks for watching!", "no_speech_prob": 0.3, "avg_logprob": -0.6,
             "compression_ratio": 0.8},
        ],
    }  # fmt: skip
    t = asr.make_transcriber(settings)
    assert t.name == "mlx-whisper:mlx-community/whisper-large-v3-turbo"
    assert fake_mlx_whisper.loads == []  # nothing loads in the factory
    segments = t.transcribe(write(tmp_path / "a.wav", synth(20, [(5, 8, 440)])))
    assert [(s.t0, s.t1, s.text) for s in segments] == [(5.4, 7.6, "Remember the budget.")]
    call = fake_mlx_whisper.calls[0]
    assert call["decode_options"] == {"language": "en"}
    assert (
        isinstance(call["audio"], np.ndarray) and call["audio"].dtype == np.float32 and call["audio"].size == 3 * RATE
    )
    t.close()
    assert fake_mlx_whisper.holder.model is None


@pytest.fixture()
def fake_parakeet(monkeypatch, fake_mlx):
    state = types.SimpleNamespace(loads=[], mels=[], generates=[], sentences=[], load_error=None)

    @dataclasses.dataclass
    class SentenceConfig:  # parakeet_mlx/alignment.py, 0.7.0
        max_words: int | None = None
        silence_gap: float | None = None
        max_duration: float | None = None

    @dataclasses.dataclass
    class DecodingConfig:  # parakeet_mlx/parakeet.py, 0.7.0
        decoding: Any = "Greedy()"
        sentence: SentenceConfig = dataclasses.field(default_factory=SentenceConfig)

    class Model:
        preprocessor_config = "PreprocessArgs(sample_rate=16000, …)"

        def generate(self, mel, *, decoding_config=None):  # BaseParakeet.generate
            state.generates.append((mel, decoding_config))
            return [types.SimpleNamespace(text="ignored", sentences=list(state.sentences))]

    def from_pretrained(hf_id_or_path, *, dtype="mx.bfloat16", cache_dir=None):  # parakeet_mlx/utils.py
        if state.load_error:
            raise state.load_error
        state.loads.append((hf_id_or_path, dtype, cache_dir))
        return Model()

    def get_logmel(x, args):  # parakeet_mlx/audio.py
        state.mels.append((x, args))
        return ("mel", x)

    package = types.ModuleType("parakeet_mlx")
    package.from_pretrained = from_pretrained
    package.DecodingConfig = DecodingConfig
    package.SentenceConfig = SentenceConfig
    audio_module = types.ModuleType("parakeet_mlx.audio")
    audio_module.get_logmel = get_logmel
    package.audio = audio_module
    monkeypatch.setitem(sys.modules, "parakeet_mlx", package)
    monkeypatch.setitem(sys.modules, "parakeet_mlx.audio", audio_module)
    return state


def test_parakeet_mlx_adapter_calls_and_mapping(fake_mlx, fake_parakeet):
    engine = asr.ParakeetMlxEngine("mlx-community/parakeet-tdt-0.6b-v3")
    assert engine.max_chunk_s == 120.0
    assert fake_parakeet.loads == [("mlx-community/parakeet-tdt-0.6b-v3", "mx.bfloat16", None)]  # library defaults

    sentence = types.SimpleNamespace  # AlignedSentence: text, tokens, start, end, duration, confidence
    fake_parakeet.sentences = [
        sentence(text=" Ship the Falcon beta.", start=0.48, end=2.24, duration=1.76, confidence=0.97, tokens=[]),
        sentence(text=" Call the vendor.", start=3.2, end=4.4, duration=1.2, confidence=0.9, tokens=[]),
    ]
    result = engine.transcribe(SAMPLES, "en")  # the model detects languages itself; "en" is not passed anywhere

    ((mx_audio, preprocess_args),) = fake_parakeet.mels
    assert mx_audio[0] == "mx.array" and mx_audio[1].dtype == np.float32 and np.array_equal(mx_audio[1], SAMPLES)
    assert preprocess_args == "PreprocessArgs(sample_rate=16000, …)"  # model.preprocessor_config
    ((mel, config),) = fake_parakeet.generates
    assert mel == ("mel", mx_audio)
    assert (config.sentence.silence_gap, config.sentence.max_duration, config.sentence.max_words) == (2.0, 30.0, None)
    assert config.decoding == "Greedy()"  # greedy decoding, the library default
    assert [(p.t0, p.t1, p.text) for p in result.pieces] == [
        (0.48, 2.24, " Ship the Falcon beta."),
        (3.2, 4.4, " Call the vendor."),
    ]
    assert result.language is None

    engine.close()
    assert len(fake_mlx.clear_cache.calls) == 1


def test_parakeet_mlx_load_failure(fake_mlx, fake_parakeet):
    fake_parakeet.load_error = FileNotFoundError("config.json")
    with pytest.raises(BackendUnavailable, match="Hugging Face"):
        asr.ParakeetMlxEngine("mlx-community/typo")


@pytest.fixture()
def fake_faster_whisper(monkeypatch):
    state = types.SimpleNamespace(
        inits=[],
        calls=[],
        vad_calls=[],
        segments=[],
        speech=[{"start": 0, "end": 16000}],
        language="en",
        probability=0.93,
        consumed=False,
        load_error=None,
    )

    @dataclasses.dataclass
    class VadOptions:  # faster_whisper/vad.py, 1.2.1
        threshold: float = 0.5
        neg_threshold: float | None = None
        min_speech_duration_ms: int = 0
        max_speech_duration_s: float = float("inf")
        min_silence_duration_ms: int = 2000
        speech_pad_ms: int = 400

    def get_speech_timestamps(audio, vad_options=None, sampling_rate=16000, **kwargs):
        state.vad_calls.append((audio, vad_options, sampling_rate))
        return list(state.speech)

    class WhisperModel:
        def __init__(self, model_size_or_path, device="auto", device_index=0, compute_type="default", cpu_threads=0,
                     num_workers=1, download_root=None, local_files_only=False, files=None, revision=None,
                     use_auth_token=None, **model_kwargs):  # fmt: skip
            assert not model_kwargs
            if state.load_error:
                raise state.load_error
            state.inits.append({"model": model_size_or_path, "device": device, "compute_type": compute_type,
                                "cpu_threads": cpu_threads, "download_root": download_root})  # fmt: skip

        def transcribe(self, audio, language=None, task="transcribe", log_progress=False, beam_size=5, best_of=5,
                       patience=1, length_penalty=1, repetition_penalty=1, no_repeat_ngram_size=0,
                       temperature=(0.0, 0.2, 0.4, 0.6, 0.8, 1.0), compression_ratio_threshold=2.4,
                       log_prob_threshold=-1.0, no_speech_threshold=0.6, condition_on_previous_text=True,
                       prompt_reset_on_temperature=0.5, initial_prompt=None, prefix=None, suppress_blank=True,
                       suppress_tokens=(-1,), without_timestamps=False, max_initial_timestamp=1.0,
                       word_timestamps=False, prepend_punctuations="", append_punctuations="", multilingual=False,
                       vad_filter=False, vad_parameters=None, max_new_tokens=None, chunk_length=None,
                       clip_timestamps="0", hallucination_silence_threshold=None, hotwords=None,
                       language_detection_threshold=0.5, language_detection_segments=1):  # fmt: skip
            if isinstance(vad_parameters, dict):
                VadOptions(**vad_parameters)  # as the library does: unknown keys are a TypeError
            state.calls.append({"audio": audio, "language": language, "task": task, "beam_size": beam_size,
                                "condition_on_previous_text": condition_on_previous_text,
                                "word_timestamps": word_timestamps, "vad_filter": vad_filter,
                                "vad_parameters": vad_parameters, "clip_timestamps": clip_timestamps,
                                "hallucination_silence_threshold": hallucination_silence_threshold})  # fmt: skip

            def generate():  # decoding happens lazily, while the caller iterates
                yield from state.segments
                state.consumed = True

            return generate(), types.SimpleNamespace(language=state.language, language_probability=state.probability)

    package = types.ModuleType("faster_whisper")
    package.WhisperModel = WhisperModel
    vad_module = types.ModuleType("faster_whisper.vad")
    vad_module.VadOptions = VadOptions
    vad_module.get_speech_timestamps = get_speech_timestamps
    package.vad = vad_module
    monkeypatch.setitem(sys.modules, "faster_whisper", package)
    monkeypatch.setitem(sys.modules, "faster_whisper.vad", vad_module)
    return state


def fw_segment(start: float, end: float, text: str, **extra: Any) -> Any:
    fields = {"id": 1, "seek": 0, "tokens": [], "avg_logprob": -0.3, "compression_ratio": 1.2, "no_speech_prob": 0.05,
              "words": None, "temperature": 0.0}  # fmt: skip
    return types.SimpleNamespace(start=start, end=end, text=text, **{**fields, **extra})


def test_faster_whisper_adapter_calls_and_mapping(fake_faster_whisper):
    engine = asr.FasterWhisperEngine("small", vad=True)
    assert engine.max_chunk_s == 600.0
    assert fake_faster_whisper.inits == [
        {"model": "small", "device": "cpu", "compute_type": "int8", "cpu_threads": 0, "download_root": None}
    ]
    fake_faster_whisper.segments = [
        fw_segment(0.3, 2.1, " The design review is at three."),
        fw_segment(2.4, 3.0, " Room four B.", no_speech_prob=0.61, avg_logprob=-1.2, compression_ratio=0.7),
    ]
    result = engine.transcribe(SAMPLES, None)

    ((vad_audio, vad_options, rate),) = fake_faster_whisper.vad_calls
    assert vad_audio is SAMPLES and rate == 16000 and vad_options.min_silence_duration_ms == 500
    (call,) = fake_faster_whisper.calls
    assert call == {
        "audio": SAMPLES,
        "language": None,
        "task": "transcribe",
        "beam_size": 5,
        "condition_on_previous_text": False,
        "word_timestamps": True,
        "vad_filter": True,
        "vad_parameters": {"min_silence_duration_ms": 500},
        "clip_timestamps": "0",
        "hallucination_silence_threshold": 2.0,
    }
    assert fake_faster_whisper.consumed  # the generator was drained inside the engine
    assert result.language == "en"
    assert [(p.t0, p.t1, p.text) for p in result.pieces] == [
        (0.3, 2.1, " The design review is at three."),
        (2.4, 3.0, " Room four B."),
    ]
    assert (result.pieces[1].no_speech_prob, result.pieces[1].avg_logprob, result.pieces[1].compression_ratio) == (
        0.61,
        -1.2,
        0.7,
    )

    assert engine.transcribe(SAMPLES, "fr").language is None
    assert fake_faster_whisper.calls[-1]["language"] == "fr"
    fake_faster_whisper.probability = 0.31  # a guess, not a detection: do not pin the rest of the file to it
    assert engine.transcribe(SAMPLES, None).language is None
    engine.close()


def test_faster_whisper_skips_chunks_in_which_silero_hears_nothing(fake_faster_whisper):
    engine = asr.FasterWhisperEngine("small", vad=True)
    fake_faster_whisper.speech = []
    result = engine.transcribe(SAMPLES, None)
    assert result.pieces == [] and result.language is None  # and no language "detected" from noise
    assert fake_faster_whisper.calls == []


def test_faster_whisper_without_vad(fake_faster_whisper):
    engine = asr.FasterWhisperEngine("small", vad=False)
    fake_faster_whisper.speech = []
    fake_faster_whisper.segments = [fw_segment(0.0, 1.0, " hi")]
    assert [p.text for p in engine.transcribe(SAMPLES, "en").pieces] == [" hi"]
    assert fake_faster_whisper.vad_calls == []
    assert fake_faster_whisper.calls[0]["vad_filter"] is False


def test_faster_whisper_vad_precheck_failure_does_not_lose_speech(fake_faster_whisper, monkeypatch):
    def broken(*args: Any, **kwargs: Any) -> Any:
        raise RuntimeError("onnxruntime session failed")

    monkeypatch.setattr(sys.modules["faster_whisper.vad"], "get_speech_timestamps", broken)
    engine = asr.FasterWhisperEngine("small", vad=True)
    fake_faster_whisper.segments = [fw_segment(0.0, 1.0, " still here")]
    assert [p.text for p in engine.transcribe(SAMPLES, None).pieces] == [" still here"]


def test_faster_whisper_load_failure(fake_faster_whisper):
    fake_faster_whisper.load_error = RuntimeError("LocalEntryNotFoundError: cannot find the requested files")
    with pytest.raises(BackendUnavailable, match=r'faster-whisper could not load the speech model "small"'):
        asr.FasterWhisperEngine("small")


# -- sherpa-onnx: arguments are bound against the installed package's real signatures -----------------


def make_model_dir(root: Path, names: list[str]) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    for name in names:
        (root / name).write_bytes(b"onnx")
    return root


WHISPER_FILES = ["small-encoder.onnx", "small-encoder.int8.onnx", "small-decoder.onnx", "small-decoder.int8.onnx",
                 "small-tokens.txt"]  # fmt: skip
PARAKEET_FILES = ["encoder.int8.onnx", "decoder.int8.onnx", "joiner.int8.onnx", "tokens.txt"]


def test_sherpa_layout_recognises_model_folders(tmp_path):
    whisper = asr.sherpa_layout(make_model_dir(tmp_path / "w", WHISPER_FILES + ["README.md"]))
    assert whisper.family == "whisper" and whisper.multilingual
    assert (whisper.encoder.name, whisper.decoder.name, whisper.tokens.name) == (
        "small-encoder.int8.onnx",  # the quantised files win when both are present
        "small-decoder.int8.onnx",
        "small-tokens.txt",
    )
    english = asr.sherpa_layout(
        make_model_dir(tmp_path / "e", ["tiny.en-encoder.onnx", "tiny.en-decoder.onnx", "tiny.en-tokens.txt"])
    )
    assert english.family == "whisper" and not english.multilingual and english.encoder.name == "tiny.en-encoder.onnx"
    parakeet = asr.sherpa_layout(make_model_dir(tmp_path / "p", PARAKEET_FILES))
    assert parakeet.family == "transducer" and parakeet.joiner.name == "joiner.int8.onnx"

    assert asr.sherpa_layout(tmp_path / "missing") is None
    assert asr.sherpa_layout(make_model_dir(tmp_path / "half", ["encoder.int8.onnx", "tokens.txt"])) is None
    assert asr.sherpa_layout(make_model_dir(tmp_path / "nodec", ["small-encoder.onnx", "small-tokens.txt"])) is None
    truncated = make_model_dir(tmp_path / "trunc", PARAKEET_FILES)
    (truncated / "decoder.int8.onnx").write_bytes(b"")
    assert asr.sherpa_layout(truncated) is None  # a zero-byte file is not a model
    assert asr.sherpa_layout(make_model_dir(tmp_path / "other", ["model.onnx", "tokens.txt"])) is None
    icefall = ["encoder-epoch-99-avg-1.onnx", "decoder-epoch-99-avg-1.onnx", "joiner-epoch-99-avg-1.onnx", "tokens.txt"]
    assert asr.sherpa_layout(make_model_dir(tmp_path / "icefall", icefall)) is None  # not a NeMo transducer
    plain = asr.sherpa_layout(
        make_model_dir(tmp_path / "fp32", ["encoder.onnx", "decoder.onnx", "joiner.onnx", "tokens.txt"])
    )
    assert plain.family == "transducer" and plain.encoder.name == "encoder.onnx"


class FakeStream:
    def __init__(self, result: Any):
        self.result = result
        self.options: dict[str, str] = {}
        self.audio: tuple[int, np.ndarray] | None = None

    def set_option(self, key: str, value: str) -> None:
        self.options[key] = value

    def accept_waveform(self, sample_rate: int, waveform: np.ndarray) -> None:
        self.audio = (sample_rate, waveform)


class FakeRecognizer:
    def __init__(self, result: Any):
        self.result = result
        self.streams: list[FakeStream] = []
        self.decoded: list[FakeStream] = []

    def create_stream(self) -> FakeStream:
        self.streams.append(FakeStream(self.result))
        return self.streams[-1]

    def decode_stream(self, stream: FakeStream) -> None:
        self.decoded.append(stream)


@pytest.fixture()
def sherpa_factories(monkeypatch):
    """Replace the two factory methods; every call must bind to the *installed* package's signature."""
    sherpa_onnx = pytest.importorskip("sherpa_onnx")
    state = types.SimpleNamespace(calls=[], recognizer=None)

    def patch(method: str) -> None:
        signature = inspect.signature(getattr(sherpa_onnx.OfflineRecognizer, method))

        def factory(*args: Any, **kwargs: Any) -> Any:
            bound = signature.bind(*args, **kwargs)  # TypeError here = the adapter uses an argument that is not there
            state.calls.append((method, dict(bound.arguments)))
            return state.recognizer

        factory.__signature__ = signature  # the adapter looks at the signature to see what this version offers
        monkeypatch.setattr(sherpa_onnx.OfflineRecognizer, method, staticmethod(factory))

    patch("from_whisper")
    patch("from_transducer")
    return state


def sherpa_result(**fields: Any) -> Any:
    base = {"text": "", "tokens": [], "timestamps": [], "durations": [], "lang": "", "segment_timestamps": [],
            "segment_durations": [], "segment_texts": []}  # fmt: skip
    return types.SimpleNamespace(**{**base, **fields})


def test_sherpa_whisper_adapter(tmp_path, sherpa_factories):
    folder = make_model_dir(tmp_path / "sherpa-onnx-whisper-small", WHISPER_FILES)
    sherpa_factories.recognizer = FakeRecognizer(
        sherpa_result(
            text=" Bonjour. Ça va ?",
            lang="fr",
            segment_timestamps=[0.0, 1.5],
            segment_durations=[1.4, 2.0],
            segment_texts=[" Bonjour.", " Ça va ?"],
        )
    )
    engine = asr.SherpaOnnxEngine(folder, asr.sherpa_layout(folder), threads=3)
    assert engine.max_chunk_s == 28.0  # Whisper's window is 30 s
    ((method, args),) = sherpa_factories.calls
    assert method == "from_whisper"
    assert args == {
        "encoder": str(folder / "small-encoder.int8.onnx"),
        "decoder": str(folder / "small-decoder.int8.onnx"),
        "tokens": str(folder / "small-tokens.txt"),
        "language": "",  # multilingual model: detect, unless a stream says otherwise
        "task": "transcribe",
        "num_threads": 3,
        "enable_segment_timestamps": True,
    }

    result = engine.transcribe(SAMPLES, None)
    stream = sherpa_factories.recognizer.decoded[0]
    assert stream.options == {} and stream.audio[0] == 16000 and np.array_equal(stream.audio[1], SAMPLES)
    assert result.language == "fr"
    assert [(p.t0, p.t1, p.text) for p in result.pieces] == [(0.0, 1.4, " Bonjour."), (1.5, 3.5, " Ça va ?")]

    told = engine.transcribe(SAMPLES, "fr")
    assert sherpa_factories.recognizer.decoded[1].options == {"language": "fr"}
    assert told.language is None
    engine.close()


def test_sherpa_english_only_whisper_ignores_the_language(tmp_path, sherpa_factories):
    folder = make_model_dir(
        tmp_path / "en", ["tiny.en-encoder.int8.onnx", "tiny.en-decoder.int8.onnx", "tiny.en-tokens.txt"]
    )
    sherpa_factories.recognizer = FakeRecognizer(sherpa_result(text=" No segment info here."))
    engine = asr.SherpaOnnxEngine(folder, asr.sherpa_layout(folder))
    assert sherpa_factories.calls[0][1]["language"] == "en"
    assert 1 <= sherpa_factories.calls[0][1]["num_threads"] <= 4
    result = engine.transcribe(SAMPLES, "de")
    assert sherpa_factories.recognizer.decoded[0].options == {}  # an English-only model is not told "de"
    # without segment timestamps the whole chunk is one piece
    assert [(p.t0, p.t1, p.text) for p in result.pieces] == [(0.0, 3.0, " No segment info here.")]


def test_sherpa_whisper_adapter_with_an_older_sherpa_onnx(tmp_path, monkeypatch):
    """Releases before segment timestamps / per-stream options: degrade to one piece per chunk."""
    sherpa_onnx = pytest.importorskip("sherpa_onnx")
    calls: list[dict[str, Any]] = []

    class OldStream:  # no set_option
        result = sherpa_result(text=" Hallo zusammen.", lang="")
        del result.segment_texts, result.segment_timestamps, result.segment_durations

        def accept_waveform(self, sample_rate: int, waveform: np.ndarray) -> None:
            pass

    class OldRecognizer:
        def create_stream(self) -> OldStream:
            return OldStream()

        def decode_stream(self, stream: OldStream) -> None:
            pass

    def from_whisper(encoder, decoder, tokens, language="en", task="transcribe", num_threads=1,
                     decoding_method="greedy_search", debug=False, provider="cpu", tail_paddings=-1):  # fmt: skip
        calls.append({"language": language, "num_threads": num_threads})
        return OldRecognizer()

    monkeypatch.setattr(sherpa_onnx.OfflineRecognizer, "from_whisper", staticmethod(from_whisper))
    folder = make_model_dir(tmp_path / "w", WHISPER_FILES)
    engine = asr.SherpaOnnxEngine(folder, asr.sherpa_layout(folder), threads=2)
    assert calls == [{"language": "", "num_threads": 2}]
    result = engine.transcribe(SAMPLES, "de")
    assert [(p.t0, p.t1, p.text) for p in result.pieces] == [(0.0, 3.0, " Hallo zusammen.")]


def test_sherpa_parakeet_adapter(tmp_path, sherpa_factories):
    folder = make_model_dir(tmp_path / "sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8", PARAKEET_FILES)
    sherpa_factories.recognizer = FakeRecognizer(
        sherpa_result(
            text="Ship it. Call them",
            tokens=[" Ship", " it", ".", " Call", " them"],
            timestamps=[0.4, 0.72, 0.88, 1.6, 1.92],
            durations=[0.24, 0.16, 0.08, 0.32, 0.4],
        )
    )
    engine = asr.SherpaOnnxEngine(folder, asr.sherpa_layout(folder), threads=2)
    assert engine.max_chunk_s == 30.0  # memory grows with chunk length; 30 s keeps it under about 1.4 GB
    ((method, args),) = sherpa_factories.calls
    assert method == "from_transducer"
    assert args == {
        "encoder": str(folder / "encoder.int8.onnx"),
        "decoder": str(folder / "decoder.int8.onnx"),
        "joiner": str(folder / "joiner.int8.onnx"),
        "tokens": str(folder / "tokens.txt"),
        "num_threads": 2,
        "decoding_method": "greedy_search",
        "model_type": "nemo_transducer",  # NeMo export, not an icefall transducer
    }
    result = engine.transcribe(SAMPLES, "en")
    assert sherpa_factories.recognizer.decoded[0].options == {}
    assert [(p.text, p.t0, round(p.t1, 2)) for p in result.pieces] == [
        ("Ship it.", 0.4, 0.96),
        ("Call them", 1.6, 2.32),
    ]
    assert result.language is None
    silent = FakeRecognizer(sherpa_result())
    engine._recognizer = silent
    assert engine.transcribe(SAMPLES, None).pieces == []


def test_sherpa_load_failure_says_how_to_recover(tmp_path, monkeypatch):
    sherpa_onnx = pytest.importorskip("sherpa_onnx")

    def broken(*args: Any, **kwargs: Any) -> Any:
        raise RuntimeError("Load model from encoder.int8.onnx failed: Protobuf parsing failed")

    monkeypatch.setattr(sherpa_onnx.OfflineRecognizer, "from_transducer", staticmethod(broken))
    folder = make_model_dir(tmp_path / "broken-model", PARAKEET_FILES)
    with pytest.raises(BackendUnavailable) as err:
        asr.SherpaOnnxEngine(folder, asr.sherpa_layout(folder))
    assert str(folder) in str(err.value) and "delete that folder" in str(err.value)


# -- sherpa-onnx model resolution and download ----------------------------------------------------------


def test_installed_sherpa_model_is_used_without_any_download(settings, monkeypatch):
    def no_network(*args: Any, **kwargs: Any) -> Any:
        raise AssertionError("must not download")

    monkeypatch.setattr(modelfetch, "fetch_archive", no_network)
    # unpacked by hand, so there is no completion marker: complete files are enough
    make_model_dir(settings.models_dir / "sherpa-onnx-whisper-small", WHISPER_FILES)
    folder, layout = asr.ensure_sherpa_model(settings, "sherpa-onnx-whisper-small")
    assert folder == settings.models_dir / "sherpa-onnx-whisper-small" and layout.family == "whisper"


def test_explicit_model_path_is_used_as_is_and_never_downloaded(settings, tmp_path, monkeypatch):
    monkeypatch.setattr(modelfetch, "fetch_archive", lambda *a, **k: pytest.fail("must not download"))
    elsewhere = make_model_dir(tmp_path / "my models" / "parakeet", PARAKEET_FILES)
    folder, layout = asr.ensure_sherpa_model(settings, str(elsewhere))
    assert folder == elsewhere and layout.family == "transducer"
    with pytest.raises(BackendUnavailable, match="not a sherpa-onnx model folder") as err:
        asr.ensure_sherpa_model(settings, str(tmp_path / "nothing-here"))
    assert 'asr.model = "auto"' in str(err.value)
    with pytest.raises(BackendUnavailable, match="not a sherpa-onnx model name"):
        asr.ensure_sherpa_model(settings, "bad name; rm -rf")


@pytest.fixture()
def model_server(monkeypatch):
    """A local stand-in for the sherpa-onnx GitHub release."""
    files: dict[str, bytes] = {}
    hits: list[str] = []

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args: Any) -> None:
            pass

        def do_GET(self) -> None:
            hits.append(self.path)
            data = files.get(self.path)
            if data is None:
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, kwargs={"poll_interval": 0.01}, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_address[1]}"
    monkeypatch.setattr(asr, "SHERPA_MODEL_URL", base + "/asr-models/{name}.tar.bz2")
    monkeypatch.setenv("no_proxy", "127.0.0.1,localhost")
    monkeypatch.setattr(modelfetch.time, "sleep", lambda seconds: None)
    yield types.SimpleNamespace(files=files, hits=hits, base=base)
    server.shutdown()
    server.server_close()


def model_archive(name: str, file_names: list[str]) -> bytes:
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:bz2") as tar:
        for file_name in file_names:
            info = tarfile.TarInfo(f"{name}/{file_name}")
            info.size = 4
            tar.addfile(info, io.BytesIO(b"onnx"))
    return buf.getvalue()


def test_missing_sherpa_model_is_downloaded_into_the_models_folder(settings, model_server):
    name = "sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8"
    model_server.files[f"/asr-models/{name}.tar.bz2"] = model_archive(name, PARAKEET_FILES)
    folder, layout = asr.ensure_sherpa_model(settings, name)
    assert folder == settings.models_dir / name and layout.family == "transducer"
    assert modelfetch.is_fetched(asr.SHERPA_MODEL_URL.format(name=name), settings.models_dir, expected_member=name)
    asr.ensure_sherpa_model(settings, name)
    assert model_server.hits == [f"/asr-models/{name}.tar.bz2"]  # the second call found it on disk


def test_failed_download_tells_the_user_what_to_do(settings, model_server, tmp_path, monkeypatch):
    monkeypatch.setattr(asr, "module_available", lambda module: module == "sherpa_onnx")
    settings.asr.backend = "sherpa-onnx"
    settings.asr.model = "sherpa-onnx-whisper-typo"
    t = asr.make_transcriber(settings)  # creating it costs nothing and contacts nobody
    assert model_server.hits == []
    path = write(tmp_path / "a.wav", synth(20, [(5, 8, 440)]))
    with pytest.raises(BackendUnavailable) as err:
        t.transcribe(path)
    message = str(err.value)
    url = f"{model_server.base}/asr-models/sherpa-onnx-whisper-typo.tar.bz2"
    assert "sherpa-onnx-whisper-typo" in message and "could not be downloaded" in message
    assert url in message and "404" in message
    assert "by hand" in message and str(settings.models_dir) in message
    assert 'asr.model = "auto"' in message and asr.SHERPA_MODEL_LIST in message
    with pytest.raises(BackendUnavailable):
        t.transcribe(path)
    assert len(model_server.hits) == 1  # the pipeline's next clip does not hammer the server again
    # silence never needs the model, so it is fine even while the model is missing
    assert t.transcribe(write(tmp_path / "s.wav", np.zeros(5 * RATE, dtype=np.float32))) == []


def test_downloaded_archive_of_an_unsupported_kind(settings, model_server):
    name = "sherpa-onnx-some-ctc-model"
    model_server.files[f"/asr-models/{name}.tar.bz2"] = model_archive(name, ["model.onnx", "tokens.txt"])
    with pytest.raises(BackendUnavailable, match="not a kind of model videonotes can run"):
        asr.ensure_sherpa_model(settings, name)


def test_default_sherpa_model_url_is_the_release_asset():
    assert asr.SHERPA_MODEL_URL.format(name=asr.DEFAULT_MODELS["sherpa-onnx"]) == (
        "https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/"
        "sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8.tar.bz2"
    )


# ==================================================================================================
# Factory and status
# ==================================================================================================

ALL_MODULES = {"mlx.core", "mlx_whisper", "parakeet_mlx", "faster_whisper", "sherpa_onnx"}


def machine(monkeypatch, *, apple_silicon: bool, macos: bool = True, modules: set[str] = frozenset()) -> None:
    monkeypatch.setattr(asr, "is_apple_silicon", lambda: apple_silicon)
    monkeypatch.setattr(asr, "is_macos", lambda: macos or apple_silicon)
    monkeypatch.setattr(asr, "module_available", lambda module: module in modules)


def test_backend_none_returns_none(settings, monkeypatch):
    machine(monkeypatch, apple_silicon=True, modules=ALL_MODULES)
    settings.asr.backend = "none"
    assert asr.make_transcriber(settings) is None
    assert not any(s.selected for s in asr.asr_status(settings))


@pytest.mark.parametrize(
    ("backend", "package"),
    [("mlx-whisper", "mlx-whisper"), ("parakeet-mlx", "parakeet-mlx"), ("faster-whisper", "faster-whisper"),
     ("sherpa-onnx", "sherpa-onnx")],
)  # fmt: skip
def test_explicit_backend_that_is_not_installed_raises_with_the_install_command(
    settings, monkeypatch, backend, package
):
    machine(monkeypatch, apple_silicon=True, modules=ALL_MODULES - set(asr._SPECS[backend].modules[-1:]))
    settings.asr.backend = backend
    with pytest.raises(BackendUnavailable) as err:
        asr.make_transcriber(settings)
    assert f"pip install {package}" in str(err.value) and backend in str(err.value)
    statuses = asr.asr_status(settings)
    assert not any(s.selected for s in statuses)  # nothing is in use, even though other backends are installed
    (mine,) = [s for s in statuses if s.name == backend]
    assert not mine.available and f"pip install {package}" in mine.detail


def test_explicit_mlx_backend_on_an_intel_mac(settings, monkeypatch):
    machine(monkeypatch, apple_silicon=False, macos=True, modules=ALL_MODULES)
    settings.asr.backend = "mlx-whisper"
    with pytest.raises(BackendUnavailable, match="Apple Silicon") as err:
        asr.make_transcriber(settings)
    assert "faster-whisper" in str(err.value)


def test_unknown_backend_name(settings, monkeypatch):
    machine(monkeypatch, apple_silicon=True, modules=ALL_MODULES)
    settings.asr.backend = "whisper"
    with pytest.raises(BackendUnavailable, match="auto, mlx-whisper, parakeet-mlx, faster-whisper, sherpa-onnx, none"):
        asr.make_transcriber(settings)
    assert not any(s.selected for s in asr.asr_status(settings))


def test_auto_preference_order_on_apple_silicon(settings, monkeypatch):
    expected = ["mlx-whisper", "parakeet-mlx", "faster-whisper", "sherpa-onnx"]
    modules = set(ALL_MODULES)
    for backend, removed in zip(
        expected, ["mlx_whisper", "parakeet_mlx", "faster_whisper", "sherpa_onnx"], strict=True
    ):
        machine(monkeypatch, apple_silicon=True, modules=modules)
        t = asr.make_transcriber(settings)
        assert t.name == f"{backend}:{asr.DEFAULT_MODELS[backend]}"
        statuses = asr.asr_status(settings)
        assert [s.name for s in statuses if s.selected] == [backend]
        assert [s.name for s in statuses] == expected
        modules.discard(removed)
    machine(monkeypatch, apple_silicon=True, modules=modules)
    assert asr.make_transcriber(settings) is None  # nothing installed: the pipeline skips the stage
    assert not any(s.selected or s.available for s in asr.asr_status(settings))


def test_auto_preference_order_elsewhere(settings, monkeypatch):
    # MLX packages being importable (they exist for Linux) does not make "auto" choose them off Apple Silicon
    for macos in (True, False):
        machine(monkeypatch, apple_silicon=False, macos=macos, modules=ALL_MODULES)
        assert asr.make_transcriber(settings).name == "faster-whisper:small"
        machine(monkeypatch, apple_silicon=False, macos=macos, modules=ALL_MODULES - {"faster_whisper"})
        assert asr.make_transcriber(settings).name == f"sherpa-onnx:{asr.DEFAULT_MODELS['sherpa-onnx']}"
        statuses = asr.asr_status(settings)
        assert [s.name for s in statuses if s.selected] == ["sherpa-onnx"]
        assert sorted(s.name for s in statuses) == sorted(asr.BACKENDS)
        machine(monkeypatch, apple_silicon=False, macos=macos, modules={"mlx.core", "mlx_whisper", "parakeet_mlx"})
        assert asr.make_transcriber(settings) is None
    # on an Intel Mac the MLX backends are reported as impossible rather than "install me"
    machine(monkeypatch, apple_silicon=False, macos=True, modules=set())
    by_name = {s.name: s for s in asr.asr_status(settings)}
    assert "Apple Silicon" in by_name["mlx-whisper"].detail and "pip install" not in by_name["mlx-whisper"].detail
    assert "pip install faster-whisper" in by_name["faster-whisper"].detail


def test_mlx_backends_need_mlx_itself(settings, monkeypatch):
    machine(monkeypatch, apple_silicon=True, modules={"mlx_whisper", "parakeet_mlx", "sherpa_onnx"})  # no mlx.core
    assert asr.make_transcriber(settings).name.startswith("sherpa-onnx:")


def test_model_setting_passes_through(settings, monkeypatch, tmp_path):
    machine(monkeypatch, apple_silicon=True, modules=ALL_MODULES)
    settings.asr.backend = "faster-whisper"
    settings.asr.model = "distil-large-v3.5"
    assert asr.make_transcriber(settings).name == "faster-whisper:distil-large-v3.5"
    settings.asr.model = " AUTO "
    assert asr.make_transcriber(settings).name == "faster-whisper:small"
    settings.asr.backend = "mlx-whisper"
    settings.asr.model = "mlx-community/whisper-small-mlx"
    assert asr.make_transcriber(settings).name == "mlx-whisper:mlx-community/whisper-small-mlx"
    local = tmp_path / "models" / "my-whisper"
    settings.asr.model = str(local)
    t = asr.make_transcriber(settings)
    assert t.name == "mlx-whisper:my-whisper" and t.model == str(local)  # short name for display, full path for use
    monkeypatch.setenv("HOME", str(tmp_path))
    settings.asr.model = "~/models/my-whisper"  # the libraries would take "~" literally
    assert asr.make_transcriber(settings).model == str(local)


def test_explicit_backend_is_the_selected_one(settings, monkeypatch):
    machine(monkeypatch, apple_silicon=True, modules=ALL_MODULES)
    for backend in asr.BACKENDS:
        settings.asr.backend = backend.upper()  # forgiving about case
        assert asr.make_transcriber(settings).backend == backend
        statuses = asr.asr_status(settings)
        assert [s.name for s in statuses if s.selected] == [backend]
        assert all(s.available for s in statuses)


def test_factory_and_status_do_not_import_or_load_anything(settings, monkeypatch):
    machine(monkeypatch, apple_silicon=True, modules=ALL_MODULES)
    monkeypatch.setattr(asr, "MlxWhisperEngine", lambda *a, **k: pytest.fail("loaded a model"))
    monkeypatch.setattr(modelfetch, "fetch_archive", lambda *a, **k: pytest.fail("downloaded a model"))
    before = set(sys.modules)
    for backend in ("auto", *asr.BACKENDS):
        settings.asr.backend = backend
        asr.make_transcriber(settings)
        asr.asr_status(settings)
    assert not {
        m
        for m in set(sys.modules) - before
        if m.split(".")[0] in {"mlx", "mlx_whisper", "parakeet_mlx", "faster_whisper", "sherpa_onnx", "onnxruntime"}
    }


def test_settings_reach_the_transcriber(settings, monkeypatch, tmp_path, fake_faster_whisper):
    machine(monkeypatch, apple_silicon=False, modules={"faster_whisper"})
    settings.asr.vad = False
    settings.asr.language = "de"
    path = write(tmp_path / "a.wav", synth(10, [(2, 4, 440)]))
    fake_faster_whisper.segments = [fw_segment(2.0, 4.0, " Guten Tag.")]
    t = asr.make_transcriber(settings)
    assert [(s.t0, s.t1, s.text) for s in t.transcribe(path)] == [(2.0, 4.0, "Guten Tag.")]
    call = fake_faster_whisper.calls[0]
    assert call["language"] == "de" and call["vad_filter"] is False and call["audio"].size == 10 * RATE
    assert fake_faster_whisper.vad_calls == []


def test_status_details(settings, monkeypatch, tmp_path):
    machine(monkeypatch, apple_silicon=True, modules=ALL_MODULES)
    monkeypatch.setenv("HF_HOME", str(tmp_path / "hf"))
    monkeypatch.delenv("HF_HUB_CACHE", raising=False)
    monkeypatch.delenv("HUGGINGFACE_HUB_CACHE", raising=False)
    by_name = {s.name: s for s in asr.asr_status(settings)}
    assert (
        by_name["mlx-whisper"].detail
        == "mlx-community/whisper-large-v3-turbo (downloaded from Hugging Face on first use)"
    )
    assert by_name["faster-whisper"].detail == "small (downloaded from Hugging Face on first use)"
    assert (
        by_name["sherpa-onnx"].detail == "sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8 (487 MB, downloaded on first use)"
    )

    # once the files are there, the detail is just the model
    (tmp_path / "hf" / "hub" / "models--mlx-community--whisper-large-v3-turbo" / "snapshots" / "abc").mkdir(
        parents=True
    )
    (tmp_path / "hf" / "hub" / "models--Systran--faster-whisper-small" / "snapshots" / "abc").mkdir(parents=True)
    make_model_dir(settings.models_dir / asr.DEFAULT_MODELS["sherpa-onnx"], PARAKEET_FILES)
    by_name = {s.name: s for s in asr.asr_status(settings)}
    assert by_name["mlx-whisper"].detail == "mlx-community/whisper-large-v3-turbo"
    assert by_name["faster-whisper"].detail == "small"
    assert by_name["sherpa-onnx"].detail == "sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8"
    assert by_name["parakeet-mlx"].detail.startswith("mlx-community/parakeet-tdt-0.6b-v3")

    settings.asr.backend = "sherpa-onnx"
    settings.asr.model = "sherpa-onnx-whisper-small.en"
    assert {s.name: s for s in asr.asr_status(settings)}["sherpa-onnx"].detail == (
        "sherpa-onnx-whisper-small.en (downloaded on first use)"
    )
    settings.asr.model = str(tmp_path / "not-a-model")
    assert "not a sherpa-onnx model folder" in {s.name: s for s in asr.asr_status(settings)}["sherpa-onnx"].detail


# ==================================================================================================
# The real thing: sherpa-onnx with real models
# ==================================================================================================


@pytest.fixture(scope="module")
def demo_wav(demo_video, tmp_path_factory) -> Path:
    if not demo_video.has_speech:
        pytest.skip("no speech synthesiser available for the demo clip (needs macOS `say` or ffmpeg with flite)")
    wav = tmp_path_factory.mktemp("asr") / "demo.wav"
    au.extract_audio(demo_video.path, wav)
    return wav


def scene_text(segments: list[TranscriptSegment], demo_video: Any, name: str) -> str:
    """Everything said during one scene of the demo clip, lower-cased."""
    scene = next(s for s in demo_video.scenes if s.name == name)
    midpoints = [(s, (s.t0 + s.t1) / 2) for s in segments]
    return " ".join(s.text for s, mid in midpoints if scene.t0 <= mid < scene.t0 + scene.duration).lower()


@pytest.mark.slow
def test_sherpa_onnx_transcribes_the_demo_clip_scene_by_scene(settings, demo_video, demo_wav, monkeypatch, tmp_path):
    pytest.importorskip("sherpa_onnx")
    if not asr.sherpa_layout(TINY_EN):
        pytest.skip(f"test model not found: {TINY_EN}")
    monkeypatch.setattr(modelfetch, "fetch_archive", lambda *a, **k: pytest.fail("must not download"))
    loads: list[Path] = []
    real_engine = asr.SherpaOnnxEngine

    def counting_engine(folder: Path, layout: asr.SherpaLayout, **kwargs: Any) -> Any:
        loads.append(folder)
        return real_engine(folder, layout, **kwargs)

    monkeypatch.setattr(asr, "SherpaOnnxEngine", counting_engine)
    settings.asr.backend = "sherpa-onnx"
    settings.asr.model = str(TINY_EN)
    t = asr.make_transcriber(settings)
    assert t.name == "sherpa-onnx:sherpa-onnx-whisper-tiny.en" and loads == []

    segments = t.transcribe(demo_wav)
    assert loads == [TINY_EN] and t.loaded  # loaded on first use

    # sturdy words land in the scene in which they were spoken (the tiny model mishears names)
    desk = scene_text(segments, demo_video, "desk")
    assert "friday" in desk and ("budget" in desk or "quarter" in desk)
    whiteboard = scene_text(segments, demo_video, "whiteboard")
    assert "falcon" in whiteboard
    assert "falcon" not in desk and "friday" not in whiteboard
    assert any(word in scene_text(segments, demo_video, "door-sign") for word in ("design", "review", "room"))
    assert any(word in scene_text(segments, demo_video, "parking") for word in ("car", "parked", "level"))
    assert scene_text(segments, demo_video, "walking") == ""  # the silent scene yields nothing at all

    assert segments and all(0.0 <= s.t0 <= s.t1 <= demo_video.duration + 0.5 for s in segments)
    assert [s.t0 for s in segments] == sorted(s.t0 for s in segments)
    assert all(s.text == s.text.strip() and "  " not in s.text for s in segments)

    # a second file reuses the loaded model; an English-only model takes a language request in its stride
    short = tmp_path / "desk.wav"
    au.extract_audio(demo_video.path, short, duration=8.0)
    assert t.transcribe(short, language="de")
    assert loads == [TINY_EN]

    t.close()
    assert not t.loaded


@pytest.mark.slow
def test_real_backend_returns_nothing_for_silence_without_loading(settings, tmp_path, monkeypatch):
    pytest.importorskip("sherpa_onnx")
    monkeypatch.setattr(asr, "SherpaOnnxEngine", lambda *a, **k: pytest.fail("the model was loaded for silence"))
    monkeypatch.setattr(asr, "ensure_sherpa_model", lambda *a, **k: pytest.fail("looked for the model for silence"))
    settings.asr.backend = "sherpa-onnx"
    t = asr.make_transcriber(settings)
    assert t.transcribe(write(tmp_path / "silence.wav", np.zeros(30 * RATE, dtype=np.float32))) == []
    rumble = synth(30, [(0, 30, 60)], amp=0.4)  # wind / handling noise below the speech band
    assert t.transcribe(write(tmp_path / "rumble.wav", rumble)) == []


@pytest.mark.slow
def test_sherpa_whisper_does_not_turn_noise_into_words(settings, tmp_path):
    """With the VAD switched off, a noise-only file goes through the real model; nothing may come out."""
    pytest.importorskip("sherpa_onnx")
    if not asr.sherpa_layout(TINY_EN):
        pytest.skip(f"test model not found: {TINY_EN}")
    settings.asr.backend = "sherpa-onnx"
    settings.asr.model = str(TINY_EN)
    settings.asr.vad = False
    t = asr.make_transcriber(settings)
    try:
        assert t.transcribe(write(tmp_path / "silence.wav", np.zeros(8 * RATE, dtype=np.float32))) == []
        noise = (np.random.default_rng(0).standard_normal(6 * RATE) * 0.05).astype(np.float32)
        assert t.transcribe(write(tmp_path / "noise.wav", noise)) == []
    finally:
        t.close()


@pytest.mark.slow
def test_other_sherpa_models_if_present(settings, demo_video, demo_wav):
    """Optional: point VIDEONOTES_TEST_SHERPA_MODELS at model folders (os.pathsep-separated) to try them.

    This is how the Parakeet (transducer) and multilingual Whisper paths were
    checked against real models; the folders are too large to keep with the tests.
    """
    pytest.importorskip("sherpa_onnx")
    folders = [Path(p) for p in os.environ.get("VIDEONOTES_TEST_SHERPA_MODELS", "").split(os.pathsep) if p]
    if not folders:
        pytest.skip("VIDEONOTES_TEST_SHERPA_MODELS is not set")
    for folder in folders:
        settings.asr.backend = "sherpa-onnx"
        settings.asr.model = str(folder)
        t = asr.make_transcriber(settings)
        try:
            segments = t.transcribe(demo_wav)
        finally:
            t.close()
        assert "budget" in scene_text(segments, demo_video, "desk"), folder
        assert "falcon" in scene_text(segments, demo_video, "whiteboard"), folder
        assert scene_text(segments, demo_video, "walking") == "", folder
        assert all(s.t0 <= s.t1 for s in segments)
