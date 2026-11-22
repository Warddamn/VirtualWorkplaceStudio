"""Audio extraction and a small, dependency-free voice activity detector.

The pipeline only ever feeds speech-to-text 16 kHz mono audio, and only the
parts of it that plausibly contain speech.  Skipping silence is the single
biggest saving for all-day footage (most of a day is not talking) and it
also stops Whisper-family models from hallucinating text over silence.

The detector is deliberately simple and conservative: it measures energy in
the speech band (so low-frequency wind and handling rumble on a body-worn
camera count for less), adapts to the clip's own noise floor, and errs on
the side of keeping audio.
"""

from __future__ import annotations

import wave
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from . import ffmpeg as ff

SAMPLE_RATE = 16000


class NoAudioError(ff.FFmpegError):
    """The media file has no audio stream."""


def extract_audio(
    src: str | Path,
    dst_wav: str | Path,
    *,
    start: float | None = None,
    duration: float | None = None,
    timeout: float | None = None,
) -> float:
    """Write ``src``'s audio as 16 kHz mono 16-bit PCM WAV. Returns its duration in seconds.

    Raises :class:`NoAudioError` if ``src`` has no audio stream.
    """
    src, dst = Path(src), Path(dst_wav)
    info = ff.probe(src)
    if not info.has_audio:
        raise NoAudioError(f"{src.name} has no audio track")
    dst.parent.mkdir(parents=True, exist_ok=True)
    args: list[str] = []
    if start:
        args += ["-ss", f"{start:.3f}"]
    args += ["-i", str(src)]
    if duration:
        args += ["-t", f"{duration:.3f}"]
    # First audio stream only; drop video/data; resample with ffmpeg's default (swr) resampler.
    args += ["-map", "0:a:0", "-vn", "-sn", "-dn", "-ac", "1", "-ar", str(SAMPLE_RATE), "-c:a", "pcm_s16le", str(dst)]
    ff.run(args, timeout=timeout)
    return wav_duration(dst)


def wav_duration(path: str | Path) -> float:
    with wave.open(str(path), "rb") as w:
        rate = w.getframerate()
        return w.getnframes() / float(rate) if rate else 0.0


def read_wav(path: str | Path) -> np.ndarray:
    """Read a PCM WAV as float32 mono in [-1, 1]. Expects 16-bit audio (what extract_audio writes)."""
    with wave.open(str(path), "rb") as w:
        if w.getsampwidth() != 2:
            raise ValueError(f"{path}: expected 16-bit PCM WAV, got {8 * w.getsampwidth()}-bit")
        channels = w.getnchannels()
        raw = w.readframes(w.getnframes())
    samples = np.frombuffer(raw, dtype="<i2").astype(np.float32) / 32768.0
    if channels > 1:
        samples = samples.reshape(-1, channels).mean(axis=1)
    return samples


def write_wav(path: str | Path, samples: np.ndarray, rate: int = SAMPLE_RATE) -> None:
    """Write float samples in [-1, 1] as 16-bit mono PCM WAV."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    pcm = (np.clip(np.asarray(samples, dtype=np.float32), -1.0, 1.0) * 32767.0).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(pcm.tobytes())


# -- voice activity detection ------------------------------------------------------


@dataclass
class SpeechSpan:
    t0: float
    t1: float

    @property
    def duration(self) -> float:
        return self.t1 - self.t0


_FRAME_S = 0.032  # analysis window
_HOP_S = 0.016
_BAND_HZ = (250.0, 3800.0)  # where speech energy lives; excludes wind / handling rumble
_MIN_ABS_DB = -55.0  # never call anything quieter than this speech (dBFS, band energy)
_MARGIN_DB = 9.0  # how far above the clip's noise floor a frame must be
_MIN_DYNAMIC_DB = 6.0  # p99 - p10 band energy below this = stationary noise, not speech


def _band_db(samples: np.ndarray, rate: int) -> np.ndarray:
    """Per-frame speech-band energy in dBFS."""
    frame = max(16, int(round(_FRAME_S * rate)))
    hop = max(8, int(round(_HOP_S * rate)))
    if samples.size < frame:
        return np.empty(0, dtype=np.float32)
    count = 1 + (samples.size - frame) // hop
    window = np.hanning(frame).astype(np.float32)
    freqs = np.fft.rfftfreq(frame, 1.0 / rate)
    band = (freqs >= _BAND_HZ[0]) & (freqs <= _BAND_HZ[1])
    norm = float((window**2).sum()) * frame / 2.0  # so a full-scale sine reads about 0 dBFS
    out = np.empty(count, dtype=np.float32)
    # Process in blocks so an hour of audio never needs more than a few MB at once.
    block = 4096
    for b0 in range(0, count, block):
        b1 = min(count, b0 + block)
        idx = (np.arange(b0, b1) * hop)[:, None] + np.arange(frame)[None, :]
        spec = np.fft.rfft(samples[idx] * window, axis=1)
        power = (spec.real**2 + spec.imag**2)[:, band].sum(axis=1) / norm
        out[b0:b1] = 10.0 * np.log10(power + 1e-12)
    return out


def detect_speech(
    samples: np.ndarray,
    rate: int = SAMPLE_RATE,
    *,
    min_speech_s: float = 0.25,
    min_silence_s: float = 0.6,
    pad_s: float = 0.25,
) -> list[SpeechSpan]:
    """Find stretches that plausibly contain speech.

    Conservative by design (keeps borderline audio).  Returns spans in time
    order, non-overlapping, padded by ``pad_s`` and merged when the gap between
    them is shorter than ``min_silence_s``.
    """
    samples = np.asarray(samples, dtype=np.float32)
    db = _band_db(samples, rate)
    if db.size == 0:
        return []
    hop = max(8, int(round(_HOP_S * rate))) / rate
    total = samples.size / rate

    # Noise floor: a low percentile of the clip's own band energy.
    floor = float(np.percentile(db, 10))
    peak = float(np.percentile(db, 99))
    if peak < _MIN_ABS_DB:
        return []
    # Speech is strongly modulated (syllables, pauses).  A signal whose level barely
    # moves is hiss, hum or a steady tone, however loud it is.
    if peak - floor < _MIN_DYNAMIC_DB:
        return []
    # If the clip is wall-to-wall talking the "floor" is itself speech, so never let
    # the threshold climb to within 12 dB of the loudest material.
    threshold = max(_MIN_ABS_DB, min(floor + _MARGIN_DB, peak - 12.0))
    active = db > threshold

    # Smooth single-frame flicker with a short majority filter.
    k = 5
    if active.size >= k:
        active = np.convolve(active.astype(np.float32), np.ones(k, dtype=np.float32) / k, mode="same") >= 0.5

    spans: list[SpeechSpan] = []
    edges = np.flatnonzero(np.diff(np.concatenate(([0], active.view(np.int8), [0]))))
    for start, end in zip(edges[::2], edges[1::2], strict=True):
        t0, t1 = start * hop, end * hop + _FRAME_S
        if t1 - t0 >= min_speech_s:
            spans.append(SpeechSpan(t0, t1))
    if not spans:
        return []

    merged: list[SpeechSpan] = [SpeechSpan(max(0.0, spans[0].t0 - pad_s), min(total, spans[0].t1 + pad_s))]
    for span in spans[1:]:
        t0, t1 = max(0.0, span.t0 - pad_s), min(total, span.t1 + pad_s)
        if t0 - merged[-1].t1 < min_silence_s:
            merged[-1].t1 = max(merged[-1].t1, t1)
        else:
            merged.append(SpeechSpan(t0, t1))
    return merged


def speech_ratio(spans: list[SpeechSpan], duration: float) -> float:
    """Fraction of the clip covered by speech spans (0..1)."""
    if duration <= 0:
        return 0.0
    return min(1.0, sum(s.duration for s in spans) / duration)


def chunk_spans(spans: list[SpeechSpan], *, max_chunk_s: float = 28.0) -> list[SpeechSpan]:
    """Group speech spans into chunks no longer than ``max_chunk_s``.

    Speech-to-text models with a fixed window (Whisper: 30 s) are fed one chunk
    at a time.  Adjacent spans are packed together while they fit; a single span
    longer than the limit is cut into equal parts.
    """
    chunks: list[SpeechSpan] = []
    for span in spans:
        if span.duration > max_chunk_s:
            parts = int(np.ceil(span.duration / max_chunk_s))
            step = span.duration / parts
            pieces = [SpeechSpan(span.t0 + i * step, span.t0 + (i + 1) * step) for i in range(parts)]
        else:
            pieces = [SpeechSpan(span.t0, span.t1)]
        for piece in pieces:
            if chunks and piece.t1 - chunks[-1].t0 <= max_chunk_s and piece.t0 - chunks[-1].t1 < 2.0:
                chunks[-1].t1 = piece.t1
            else:
                chunks.append(piece)
    return chunks
