"""Speech-to-text backends (contract section 4.2).

Four engines sit behind the :class:`~videonotes.backends.base.Transcriber`
protocol:

``mlx-whisper``     Whisper large-v3-turbo on Apple Silicon (MLX / Metal).
``parakeet-mlx``    NVIDIA Parakeet TDT 0.6b v3 on Apple Silicon (MLX).
``faster-whisper``  Whisper ``small`` with int8 weights on any CPU (CTranslate2).
``sherpa-onnx``     ONNX Runtime on any CPU; its models are plain downloads from
                    GitHub (no Hugging Face account, cache or library needed).

Everything that is *not* specific to an engine is implemented once, in
:class:`SpeechTranscriber`:

1. **Silence is never transcribed.**  The file is scanned with
   :func:`videonotes.media.audio.detect_speech`; a file without speech returns
   ``[]`` without loading a model.  Skipping silence is the biggest saving on
   all-day footage, and silence is where Whisper-family models invent text.
2. **Speech is fed in chunks, timestamps come back in file time.**  The speech
   spans are packed into chunks no longer than the engine can take in one call
   (:func:`videonotes.media.audio.chunk_spans`): 28 s for Whisper through
   sherpa-onnx (a fixed 30 s window), two minutes for Parakeet, ten minutes for
   the engines that slide their own window over long audio (mlx-whisper,
   faster-whisper).  A cut that falls inside continuous speech is moved to the
   quietest nearby instant so it does not split a word.  Audio is read from the
   WAV chunk by chunk, so an hour-long file needs no more memory than a short one.
3. **Text outside detected speech is dropped**, and what remains is cleaned by
   :func:`postprocess`: whitespace, non-speech tags (``[BLANK_AUDIO]``),
   repetition loops, exact repeats and a short list of well-known Whisper
   phantom phrases ("Thanks for watching").
4. **Models load lazily** on the first file that contains speech and are
   released by ``close()``.

Why chunks even for engines with long-form decoding: ``clip_timestamps`` in
mlx-whisper 0.4.3 does not skip the gaps between clips (the decode loop never
seeks to the start of the next clip), and an engine that is handed a whole file
decodes all of its silence and detects the language from the first 30 seconds,
which on worn-camera footage are often not speech.  Feeding speech islands
avoids both; within an island the engine's own long-form decoding is used
unchanged.
"""

from __future__ import annotations

import contextlib
import dataclasses
import gc
import importlib
import logging
import math
import os
import re
import sys
import wave
import zlib
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path
from types import TracebackType
from typing import Any, Protocol

import numpy as np

from ..config import Settings, is_apple_silicon, is_macos
from ..media import audio as au
from . import modelfetch
from .base import BackendError, BackendUnavailable, Transcriber, TranscriptSegment
from .status import BackendStatus, module_available

log = logging.getLogger("videonotes.asr")

SAMPLE_RATE = au.SAMPLE_RATE

#: Backend ids as written in ``config.toml``, in the order ``vnote doctor`` lists them.
BACKENDS = ("mlx-whisper", "parakeet-mlx", "faster-whisper", "sherpa-onnx")

#: What ``asr.model = "auto"`` means for each backend.
DEFAULT_MODELS = {
    # Whisper large-v3-turbo, fp16: ~1.6 GB of weights, 99+ languages.
    "mlx-whisper": "mlx-community/whisper-large-v3-turbo",
    # Parakeet TDT 0.6b v3: 25 European languages, punctuation, token timestamps.
    "parakeet-mlx": "mlx-community/parakeet-tdt-0.6b-v3",
    # Multilingual Whisper "small"; int8 keeps it near 1.5 GB of RAM on a CPU.
    "faster-whisper": "small",
    # The same Parakeet model, int8 ONNX: see the measurements in SHERPA_DEFAULT_NOTE.
    "sherpa-onnx": "sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8",
}

#: sherpa-onnx publishes its speech models as assets of one GitHub release.
SHERPA_MODEL_URL = "https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/{name}.tar.bz2"
SHERPA_MODEL_LIST = "https://github.com/k2-fsa/sherpa-onnx/releases/tag/asr-models"
_SHERPA_DOWNLOAD_MB = {"sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8": 487}

# -- tuning constants ---------------------------------------------------------------------

#: Longest audio handed to an engine in one call.
WHISPER_WINDOW_CHUNK_S = 28.0  # Whisper's context is 30 s; leaves room for a moved cut
PARAKEET_CHUNK_S = 120.0  # full-attention encoder: memory grows with the square of the length
LONGFORM_CHUNK_S = 600.0  # engines that slide their own 30 s window
#: A cut inside continuous speech may move this far to find a quiet instant.
CUT_SEARCH_S = 1.5
#: Text is kept only if it lies within this distance of detected speech.
SPAN_TOLERANCE_S = 0.5
#: Files longer than this are scanned for speech block by block (bounded memory).
_VAD_WHOLE_FILE_S = 900.0
_VAD_BLOCK_S = 600.0
_MIN_AUDIO_S = 0.1  # nothing shorter can contain a word
#: Whisper's own "this decoding failed" thresholds, reused as filters.
_MAX_COMPRESSION_RATIO = 2.4
_NO_SPEECH_PROB = 0.6
_MIN_AVG_LOGPROB = -1.0
#: A stock phrase counts as "over near-silence" when the audio under it is quieter than this …
_QUIET_DBFS = -50.0
#: … or it stretches over more time than anyone needs to say two words.
_LONE_PHRASE_MAX_S = 3.0
#: An identical line this soon after the previous one is a decoding loop, not a second remark.
_REPEAT_WINDOW_S = 10.0
_PHANTOM_MAX_WORDS = 12


# ==========================================================================================
# Engine interface
# ==========================================================================================


@dataclass
class Piece:
    """One stretch of recognised text.

    Engines return pieces with times relative to the audio they were given;
    :class:`SpeechTranscriber` shifts them to file time and fills in the two
    evidence fields before :func:`postprocess` decides what to keep.
    """

    t0: float
    t1: float
    text: str
    no_speech_prob: float | None = None  # Whisper engines only
    avg_logprob: float | None = None
    compression_ratio: float | None = None
    speech_fraction: float | None = None  # share of [t0, t1] inside detected speech; None when VAD is off
    level_db: float | None = None  # RMS level (dBFS) of the audio under the piece


@dataclass
class EngineResult:
    pieces: list[Piece]
    language: str | None = None  # the language the engine detected, when it was not told one


class Engine(Protocol):
    """A loaded model. ``transcribe`` gets at most ``max_chunk_s`` of 16 kHz mono float32 audio."""

    max_chunk_s: float

    def transcribe(self, samples: np.ndarray, language: str | None) -> EngineResult: ...

    def close(self) -> None: ...


# ==========================================================================================
# Text clean-up (pure functions)
# ==========================================================================================

_SPACE_RE = re.compile(r"\s+")
_KEY_RE = re.compile(r"[^\w']+")
_SENTENCE_RE = re.compile(r"(?<=[.!?。！？])\s+")
#: A whole segment that is only stage directions: "[BLANK_AUDIO]", "(wind howling)", "*music*", "♪♪".
_NON_SPEECH_RE = re.compile(r"^(?:\s*(?:\[[^\]]*\]|\([^)]*\)|\*[^*]+\*|[♪♫]+))+\s*[.!]?\s*$")
#: Caption credits that Whisper learned from subtitle files; nobody says these to a body camera.
_PHANTOM_RE = re.compile(
    r"^(?:(?:thanks|thank you)(?: so much| very much)? for watching\b"
    r"|(?:subtitles?|captions?|transcription|translation) (?:made |provided |created )?by\b)"
)
#: Real phrases that are also Whisper's favourite output for silence; dropped only over near-silence.
_QUIET_PHANTOMS = frozenset({"you", "thank you", "thank you very much", "thank you so much", "thanks", "bye", "bye bye"})


def normalise_language(value: str | None) -> str | None:
    """``"auto"`` / empty -> None (auto-detect); ``"en-US"`` -> ``"en"``."""
    if value is None:
        return None
    code = value.strip().lower().strip("<>|")
    if code in ("", "auto", "none", "detect"):
        return None
    return re.split(r"[-_]", code, maxsplit=1)[0] or None


def clean_text(text: str) -> str:
    """Strip and collapse whitespace."""
    return _SPACE_RE.sub(" ", text or "").strip()


def text_key(text: str) -> str:
    """Lower-case words only, for comparing two pieces of text ("Thank you." == "thank you")."""
    return _KEY_RE.sub(" ", text.lower()).strip()


def is_non_speech_tag(text: str) -> bool:
    """True for segments that are only an annotation such as ``[ Silence ]`` or ``(wind blowing)``."""
    return bool(_NON_SPEECH_RE.match(text))


def is_phantom_phrase(text: str, *, near_silence: bool) -> bool:
    """True for the well-known Whisper silence hallucinations.

    Deliberately short and conservative: caption credits ("Thanks for
    watching", "Subtitles by …") are dropped whenever a *short* segment starts
    with them; everyday phrases ("you", "Thank you.") only when they are the
    whole segment **and** the audio under them was near-silent.
    """
    key = text_key(text)
    words = key.split()
    if not words or len(words) > _PHANTOM_MAX_WORDS:
        return False
    if "amara org" in key or _PHANTOM_RE.match(key):
        return True
    return near_silence and key in _QUIET_PHANTOMS


def compression_ratio(text: str) -> float:
    """Whisper's repetition measure: bytes of text per byte of its zlib compression."""
    raw = text.encode("utf-8")
    return len(raw) / len(zlib.compress(raw)) if raw else 0.0


def collapse_repeated_sentences(text: str) -> str:
    """"I see. I see. I see. Right." -> "I see. Right." (a decoding loop inside one segment)."""
    sentences = _SENTENCE_RE.split(text)
    if len(sentences) < 2:
        return text
    kept: list[str] = []
    last_key = None
    for sentence in sentences:
        key = text_key(sentence)
        if key and key == last_key:
            continue
        kept.append(sentence)
        last_key = key or last_key
    return " ".join(kept)


def _near_silence(piece: Piece) -> bool:
    if piece.level_db is not None and piece.level_db < _QUIET_DBFS:
        return True
    if piece.speech_fraction is not None and piece.speech_fraction < 0.5:
        return True
    if piece.no_speech_prob is not None and piece.no_speech_prob > 0.5:
        return True
    return piece.t1 - piece.t0 > _LONE_PHRASE_MAX_S


def postprocess(pieces: Sequence[Piece]) -> list[TranscriptSegment]:
    """Turn raw pieces (file time) into the final segments, in time order.

    Drops: empty text, punctuation-only text, non-speech tags, segments Whisper
    itself scored as "no speech", repetition loops, known phantom phrases, and
    an exact repeat that follows its twin within a few seconds.
    """
    segments: list[TranscriptSegment] = []
    last_key = ""
    for piece in sorted(pieces, key=lambda p: (p.t0, p.t1)):
        text = clean_text(piece.text)
        if not text or is_non_speech_tag(text):
            continue
        if (
            piece.no_speech_prob is not None
            and piece.avg_logprob is not None
            and piece.no_speech_prob > _NO_SPEECH_PROB
            and piece.avg_logprob < _MIN_AVG_LOGPROB
        ):
            continue
        text = collapse_repeated_sentences(text)
        key = text_key(text)
        if not key:
            continue
        ratio = max(piece.compression_ratio or 0.0, compression_ratio(text))
        if ratio > _MAX_COMPRESSION_RATIO:
            log.debug("dropping a repetition loop (%.1fx compressible): %.60s", ratio, text)
            continue
        if is_phantom_phrase(text, near_silence=_near_silence(piece)):
            log.debug("dropping a known phantom phrase: %s", text)
            continue
        t0 = float(piece.t0)
        t1 = float(max(piece.t1, piece.t0))
        if segments and key == last_key and t0 - segments[-1].t1 <= _REPEAT_WINDOW_S:
            continue
        segments.append(TranscriptSegment(t0=round(t0, 3), t1=round(t1, 3), text=text))
        last_key = key
    return segments


def pieces_from_tokens(
    tokens: Sequence[str],
    starts: Sequence[float],
    durations: Sequence[float] | None,
    total_s: float,
    *,
    pause_s: float = 1.2,
    max_s: float = 30.0,
) -> list[Piece]:
    """Group a transducer's timestamped tokens into sentence-sized pieces.

    A piece ends after sentence punctuation, before a pause of ``pause_s``, or
    when it has grown to ``max_s``.  Word-initial tokens start with a space
    (or SentencePiece's ``▁``).
    """
    count = min(len(tokens), len(starts))
    if count == 0:
        return []
    texts = [str(tokens[i]).replace("▁", " ") for i in range(count)]
    begin = [float(starts[i]) for i in range(count)]
    has_durations = durations is not None and len(durations) >= count
    end: list[float] = []
    for i in range(count):
        if has_durations:
            stop = begin[i] + max(0.0, float(durations[i]))  # type: ignore[index]
        else:
            stop = begin[i + 1] if i + 1 < count else begin[i] + 0.3
        end.append(min(max(stop, begin[i]), total_s) if total_s > 0 else stop)

    pieces: list[Piece] = []
    first = 0
    for i in range(count):
        last = i == count - 1
        next_is_word = last or texts[i + 1].startswith(" ")
        sentence_end = texts[i].rstrip().endswith((".", "!", "?", "。", "！", "？")) and next_is_word
        pause = not last and next_is_word and begin[i + 1] - end[i] >= pause_s
        too_long = next_is_word and end[i] - begin[first] >= max_s
        if last or sentence_end or pause or too_long:
            text = "".join(texts[first : i + 1]).strip()
            if text:
                pieces.append(Piece(t0=begin[first], t1=max(end[i], begin[first]), text=text))
            first = i + 1
    return pieces


# ==========================================================================================
# Audio access and chunk planning
# ==========================================================================================


class WavReader:
    """Random access to a 16 kHz PCM WAV, a slice at a time (so long files stay cheap)."""

    def __init__(self, path: Path):
        self.path = path
        try:
            self._wave = wave.open(str(path), "rb")
        except FileNotFoundError as exc:
            raise BackendError(f"audio file not found: {path}") from exc
        except (wave.Error, EOFError, OSError) as exc:
            raise BackendError(f"{path.name} is not a readable WAV file ({exc})") from exc
        try:
            self.rate = self._wave.getframerate()
            self.channels = self._wave.getnchannels()
            self.frames = self._wave.getnframes()
            width = self._wave.getsampwidth()
            if width != 2 or self.rate != SAMPLE_RATE or self.channels < 1:
                raise BackendError(
                    f"{path.name}: expected 16 kHz 16-bit PCM audio, got {self.rate} Hz {8 * width}-bit "
                    "(videonotes.media.audio.extract_audio writes the right format)"
                )
        except BaseException:
            self._wave.close()
            raise

    @property
    def duration(self) -> float:
        return self.frames / float(self.rate)

    def read(self, t0: float, t1: float) -> np.ndarray:
        """Samples of ``[t0, t1)`` seconds as float32 mono in [-1, 1]."""
        start = min(max(0, int(round(t0 * self.rate))), self.frames)
        stop = min(max(start, int(round(t1 * self.rate))), self.frames)
        if stop <= start:
            return np.zeros(0, dtype=np.float32)
        try:
            self._wave.setpos(start)
            raw = self._wave.readframes(stop - start)
        except (wave.Error, EOFError, OSError) as exc:
            raise BackendError(f"{self.path.name} could not be read ({exc}); the file may be damaged") from exc
        usable = len(raw) - len(raw) % (2 * self.channels)  # a truncated file may end mid-frame
        samples = np.frombuffer(raw[:usable], dtype="<i2").astype(np.float32) / 32768.0
        if self.channels > 1:
            samples = samples.reshape(-1, self.channels).mean(axis=1)
        return samples

    def close(self) -> None:
        self._wave.close()

    def __enter__(self) -> WavReader:
        return self

    def __exit__(self, kind: type[BaseException] | None, exc: BaseException | None, tb: TracebackType | None) -> None:
        self.close()


def find_speech(wav: WavReader) -> list[au.SpeechSpan]:
    """Speech spans of a whole file (file time). Long files are scanned in ten-minute blocks."""
    total = wav.duration
    if total <= _VAD_WHOLE_FILE_S:
        return [au.SpeechSpan(float(s.t0), float(s.t1)) for s in au.detect_speech(wav.read(0.0, total), wav.rate)]
    spans: list[au.SpeechSpan] = []
    t = 0.0
    while t < total:
        stop = t + _VAD_BLOCK_S
        if total - stop < _VAD_BLOCK_S / 2:  # do not leave a short tail with its own noise statistics
            stop = total
        for span in au.detect_speech(wav.read(t, stop), wav.rate):
            t0, t1 = float(span.t0) + t, float(span.t1) + t
            if spans and t0 - spans[-1].t1 < 0.6:  # speech that ran across the block boundary
                spans[-1].t1 = max(spans[-1].t1, t1)
            else:
                spans.append(au.SpeechSpan(t0, t1))
        t = stop
    return spans


def overlap_seconds(t0: float, t1: float, spans: Sequence[au.SpeechSpan]) -> float:
    """How much of ``[t0, t1]`` lies inside the spans."""
    return sum(max(0.0, min(t1, s.t1) - max(t0, s.t0)) for s in spans)


def quietest_offset(samples: np.ndarray, rate: int = SAMPLE_RATE, *, frame_s: float = 0.05) -> float:
    """Offset (s) of the centre of the quietest ``frame_s`` window; ties go to the middle of ``samples``."""
    frame = max(1, int(frame_s * rate))
    if samples.size < 2 * frame:
        return samples.size / (2.0 * rate)
    hop = max(1, frame // 2)
    energy = np.concatenate(([0.0], np.cumsum(samples.astype(np.float64) ** 2)))
    starts = np.arange(0, samples.size - frame + 1, hop)
    power = energy[starts + frame] - energy[starts]
    centres = (starts + frame / 2.0) / rate
    middle = samples.size / (2.0 * rate)
    quiet = power <= power.min() * 1.05 + 1e-12
    best = int(np.flatnonzero(quiet)[np.argmin(np.abs(centres[quiet] - middle))])
    return float(centres[best])


def plan_chunks(
    spans: Sequence[au.SpeechSpan],
    max_chunk_s: float,
    read: Callable[[float, float], np.ndarray] | None = None,
) -> list[au.SpeechSpan]:
    """Pack speech spans into chunks of at most ``max_chunk_s`` (plus ``CUT_SEARCH_S``).

    Uses :func:`videonotes.media.audio.chunk_spans`.  Where that had to cut a
    long stretch of continuous speech, and ``read`` is given, the cut is moved
    to the quietest instant within ``CUT_SEARCH_S`` so it lands between words.
    """
    chunks = [
        au.SpeechSpan(float(c.t0), float(c.t1)) for c in au.chunk_spans(list(spans), max_chunk_s=max_chunk_s)
    ]
    if read is None:
        return chunks
    for left, right in zip(chunks, chunks[1:], strict=False):
        if abs(right.t0 - left.t1) > 1e-3:
            continue  # a real pause separates them already
        cut = left.t1
        lo = max(left.t0 + 1.0, cut - CUT_SEARCH_S)
        hi = min(right.t1 - 1.0, cut + CUT_SEARCH_S)
        if hi - lo < 0.2:
            continue
        window = read(lo, hi)
        if window.size:
            left.t1 = right.t0 = lo + quietest_offset(window)
    return chunks


def _level_db(samples: np.ndarray) -> float | None:
    if samples.size == 0:
        return None
    rms = float(np.sqrt(np.mean(samples.astype(np.float64) ** 2)))
    return 20.0 * math.log10(rms + 1e-10)


def _finite(value: Any, default: float) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def place_pieces(
    pieces: Sequence[Piece],
    chunk: au.SpeechSpan,
    samples: np.ndarray,
    spans: Sequence[au.SpeechSpan] | None,
) -> list[Piece]:
    """Shift a chunk's pieces to file time, attach evidence, and drop text outside detected speech."""
    duration = samples.size / float(SAMPLE_RATE)
    placed: list[Piece] = []
    for piece in pieces:
        r0 = min(max(_finite(piece.t0, 0.0), 0.0), duration)
        r1 = min(max(_finite(piece.t1, duration), r0), duration)
        t0, t1 = chunk.t0 + r0, chunk.t0 + r1
        fraction: float | None = None
        if spans is not None:
            if overlap_seconds(t0 - SPAN_TOLERANCE_S, t1 + SPAN_TOLERANCE_S, spans) <= 0.0:
                log.debug("dropping text outside detected speech at %.1fs: %.60s", t0, piece.text)
                continue
            fraction = overlap_seconds(t0, t1, spans) / (t1 - t0) if t1 - t0 > 1e-6 else 1.0
        level = _level_db(samples[int(r0 * SAMPLE_RATE) : int(r1 * SAMPLE_RATE)])
        placed.append(dataclasses.replace(piece, t0=t0, t1=t1, speech_fraction=fraction, level_db=level))
    return placed


# ==========================================================================================
# The transcriber every backend shares
# ==========================================================================================


class SpeechTranscriber:
    """A :class:`~videonotes.backends.base.Transcriber` built from an engine loader.

    ``load`` is called on the first file that contains speech; it must return an
    :class:`Engine` or raise :class:`BackendUnavailable` saying what to do.
    """

    def __init__(
        self,
        backend: str,
        model: str,
        load: Callable[[], Engine],
        *,
        vad: bool = True,
        language: str | None = None,
    ):
        self.backend = backend
        self.model = model
        self.name = f"{backend}:{_display_model(model)}"
        self._load = load
        self._vad = vad
        self._language = normalise_language(language)
        self._engine: Engine | None = None
        self._load_error: BackendUnavailable | None = None

    # -- model lifecycle --------------------------------------------------------------

    @property
    def loaded(self) -> bool:
        return self._engine is not None

    def _ensure_engine(self) -> Engine:
        if self._engine is not None:
            return self._engine
        if self._load_error is not None:  # do not retry a failed download for every clip of a run
            raise self._load_error
        log.info("loading speech model %s", self.name)
        try:
            self._engine = self._load()
        except BackendUnavailable as exc:
            self._load_error = exc
            raise
        except Exception as exc:
            self._load_error = BackendUnavailable(
                f"{self.name}: the speech model could not be loaded ({type(exc).__name__}: {exc})"
            )
            raise self._load_error from exc
        return self._engine

    def close(self) -> None:
        """Release the model. The transcriber can be used again; it reloads on demand."""
        engine, self._engine = self._engine, None
        self._load_error = None
        if engine is None:
            return
        try:
            engine.close()
        except Exception:  # freeing memory must never fail a run
            log.debug("closing %s failed", self.name, exc_info=True)
        gc.collect()

    # -- transcription ----------------------------------------------------------------

    def transcribe(self, wav_path: Path, *, language: str | None = None) -> list[TranscriptSegment]:
        """Transcribe a 16 kHz mono WAV. Returns segments in time order; ``[]`` when nobody speaks.

        ``language=None`` uses ``asr.language`` from the settings, and auto-detects
        when that is ``"auto"``.  Raises :class:`BackendError` for an unreadable
        file or a failed decode, :class:`BackendUnavailable` when the model
        cannot be loaded.
        """
        wanted = normalise_language(language) or self._language
        with WavReader(Path(wav_path)) as wav:
            if wav.duration < _MIN_AUDIO_S:
                return []
            spans: list[au.SpeechSpan] | None = None
            if self._vad:
                spans = find_speech(wav)
                if not spans:
                    log.debug("%s: no speech detected", wav.path.name)
                    return []
            engine = self._ensure_engine()
            whole = [au.SpeechSpan(0.0, wav.duration)]
            chunks = plan_chunks(spans if spans is not None else whole, engine.max_chunk_s, wav.read)
            pieces = self._run(engine, wav, chunks, spans, wanted)
        return postprocess(pieces)

    def _run(
        self,
        engine: Engine,
        wav: WavReader,
        chunks: list[au.SpeechSpan],
        spans: list[au.SpeechSpan] | None,
        language: str | None,
    ) -> list[Piece]:
        order = list(range(len(chunks)))
        if language is None and len(chunks) > 1:
            # Let the engine identify the language on the longest stretch of speech, then keep it
            # for the rest of the file: one-word chunks are too short to detect a language from.
            longest = max(order, key=lambda i: chunks[i].t1 - chunks[i].t0)
            order.sort(key=lambda i: i != longest)
        results: list[list[Piece]] = [[] for _ in chunks]
        for index in order:
            chunk = chunks[index]
            samples = wav.read(chunk.t0, chunk.t1)
            if samples.size < int(_MIN_AUDIO_S * SAMPLE_RATE):
                continue
            try:
                result = engine.transcribe(samples, language)
            except (BackendError, BackendUnavailable):
                raise
            except Exception as exc:
                raise BackendError(
                    f"{self.name} failed on {wav.path.name} at {chunk.t0:.0f}s ({type(exc).__name__}: {exc})"
                ) from exc
            if language is None and result.language:
                language = normalise_language(result.language)
            results[index] = place_pieces(result.pieces, chunk, samples, spans)
        return [piece for group in results for piece in group]


def _display_model(model: str) -> str:
    """Model id for ``Transcriber.name``: a local folder is shown by its name, not its full path."""
    with contextlib.suppress(OSError):
        path = Path(model).expanduser()
        if path.is_absolute() and path.name:
            return path.name
    return model


# ==========================================================================================
# Engines
# ==========================================================================================


def _threads() -> int:
    return max(1, min(4, os.cpu_count() or 2))


def _clear_mlx_cache() -> None:
    """Return MLX's buffer cache (Metal memory) to the system: ``mlx.core.clear_cache()``."""
    mx = sys.modules.get("mlx.core")
    if mx is None:
        return
    clear = getattr(mx, "clear_cache", None)
    if clear is None:  # MLX older than 0.22 only had the (now deprecated) mx.metal.clear_cache
        clear = getattr(getattr(mx, "metal", None), "clear_cache", None)
    if clear is not None:
        with contextlib.suppress(Exception):
            clear()


def _missing(backend: str) -> BackendUnavailable:
    return BackendUnavailable(_SPECS[backend].install_text())


def _hugging_face_load_error(backend: str, model: str, exc: BaseException) -> BackendUnavailable:
    return BackendUnavailable(
        f'{backend} could not load the speech model "{model}" ({type(exc).__name__}: {exc}).\n'
        "The first use downloads it from Hugging Face, which needs an internet connection once; "
        "check the connection and run the command again.\n"
        f'If the model name is wrong, fix asr.model in config.toml ("auto" uses {DEFAULT_MODELS[backend]}).'
    )


class MlxWhisperEngine:
    """Whisper on Apple Silicon through ``mlx-whisper``.

    Decoding follows the hallucination mitigations in the research notes:
    no conditioning on previous text, word timestamps with
    ``hallucination_silence_threshold``, and Whisper's default failure
    thresholds (whose per-segment scores :func:`postprocess` re-checks).
    """

    max_chunk_s = LONGFORM_CHUNK_S

    def __init__(self, model: str):
        self.model = model
        try:
            import mlx.core as mx
            import mlx_whisper
        except ImportError as exc:
            raise _missing("mlx-whisper") from exc
        self._transcribe = mlx_whisper.transcribe
        # mlx_whisper.transcribe is a function that shadows the submodule of the same name; the
        # module (with the model cache, ModelHolder) has to be fetched from the import system.
        self._holder = importlib.import_module("mlx_whisper.transcribe").ModelHolder
        try:
            # Load now, with the dtype transcribe() uses by default (fp16), so that a failed
            # download surfaces here as "backend unavailable" rather than as a per-clip error.
            self._holder.get_model(model, mx.float16)
        except Exception as exc:
            raise _hugging_face_load_error("mlx-whisper", model, exc) from exc

    def transcribe(self, samples: np.ndarray, language: str | None) -> EngineResult:
        result = self._transcribe(
            samples,
            path_or_hf_repo=self.model,
            verbose=None,
            language=language,
            condition_on_previous_text=False,
            word_timestamps=True,
            hallucination_silence_threshold=2.0,
        )
        pieces = [
            Piece(
                t0=_finite(seg.get("start"), 0.0),
                t1=_finite(seg.get("end"), 0.0),
                text=str(seg.get("text") or ""),
                no_speech_prob=_optional(seg.get("no_speech_prob")),
                avg_logprob=_optional(seg.get("avg_logprob")),
                compression_ratio=_optional(seg.get("compression_ratio")),
            )
            for seg in result.get("segments") or []
        ]
        return EngineResult(pieces, language=result.get("language") if language is None else None)

    def close(self) -> None:
        # mlx-whisper keeps the model in a class-level cache; empty it, then hand the memory back.
        self._holder.model = None
        self._holder.model_path = None
        gc.collect()
        _clear_mlx_cache()


class ParakeetMlxEngine:
    """NVIDIA Parakeet TDT on Apple Silicon through ``parakeet-mlx``.

    Audio is passed in memory (``get_logmel`` + ``model.generate``, the
    library's documented low-level path) so the ``ffmpeg`` lookup that
    ``model.transcribe(path)`` performs is not needed.  The model detects the
    language itself; a requested language is ignored.
    """

    max_chunk_s = PARAKEET_CHUNK_S

    def __init__(self, model: str):
        self.model = model
        try:
            import mlx.core as mx
            from parakeet_mlx import DecodingConfig, SentenceConfig, from_pretrained
            from parakeet_mlx.audio import get_logmel
        except ImportError as exc:
            raise _missing("parakeet-mlx") from exc
        self._mx = mx
        self._get_logmel = get_logmel
        # Sentences end at punctuation; also split at long pauses so timestamps stay meaningful.
        self._config = DecodingConfig(sentence=SentenceConfig(silence_gap=2.0, max_duration=30.0))
        try:
            self._model: Any = from_pretrained(model)
        except Exception as exc:
            raise _hugging_face_load_error("parakeet-mlx", model, exc) from exc

    def transcribe(self, samples: np.ndarray, language: str | None) -> EngineResult:
        audio = self._mx.array(np.ascontiguousarray(samples, dtype=np.float32))
        mel = self._get_logmel(audio, self._model.preprocessor_config)
        result = self._model.generate(mel, decoding_config=self._config)[0]
        pieces = [Piece(t0=float(s.start), t1=float(s.end), text=str(s.text)) for s in result.sentences]
        return EngineResult(pieces)

    def close(self) -> None:
        self._model = None
        gc.collect()
        _clear_mlx_cache()


class FasterWhisperEngine:
    """Whisper on the CPU through ``faster-whisper`` (CTranslate2, int8 weights).

    With ``vad=True`` the library's bundled Silero VAD is applied inside each
    chunk as a second, stricter gate behind videonotes' own energy detector.
    """

    max_chunk_s = LONGFORM_CHUNK_S

    def __init__(self, model: str, *, vad: bool = True):
        self.model = model
        self._vad = vad
        try:
            from faster_whisper import WhisperModel
        except ImportError as exc:
            raise _missing("faster-whisper") from exc
        try:
            self._model: Any = WhisperModel(model, device="cpu", compute_type="int8", cpu_threads=0)
        except Exception as exc:
            raise _hugging_face_load_error("faster-whisper", model, exc) from exc

    def _silero_hears_speech(self, samples: np.ndarray) -> bool:
        try:
            from faster_whisper.vad import VadOptions, get_speech_timestamps

            return bool(get_speech_timestamps(samples, VadOptions(min_silence_duration_ms=500)))
        except Exception:  # the pre-check is an optimisation; never let it lose speech
            log.debug("Silero pre-check failed; transcribing the chunk anyway", exc_info=True)
            return True

    def transcribe(self, samples: np.ndarray, language: str | None) -> EngineResult:
        if self._vad and not self._silero_hears_speech(samples):
            return EngineResult([])
        segments, info = self._model.transcribe(
            samples,
            language=language,
            beam_size=5,
            condition_on_previous_text=False,
            word_timestamps=True,
            hallucination_silence_threshold=2.0,
            vad_filter=self._vad,
            vad_parameters={"min_silence_duration_ms": 500},
        )
        pieces = [  # ``segments`` is a generator: the decoding happens during this loop
            Piece(
                t0=_finite(seg.start, 0.0),
                t1=_finite(seg.end, 0.0),
                text=str(seg.text or ""),
                no_speech_prob=_optional(seg.no_speech_prob),
                avg_logprob=_optional(seg.avg_logprob),
                compression_ratio=_optional(seg.compression_ratio),
            )
            for seg in segments
        ]
        return EngineResult(pieces, language=info.language if language is None else None)

    def close(self) -> None:
        self._model = None
        gc.collect()


def _optional(value: Any) -> float | None:
    if value is None:
        return None
    number = _finite(value, math.nan)
    return None if math.isnan(number) else number


# -- sherpa-onnx ----------------------------------------------------------------------------


@dataclass(frozen=True)
class SherpaLayout:
    """Which model family a sherpa-onnx model folder holds, and its files."""

    family: str  # "whisper" | "transducer"
    encoder: Path
    decoder: Path
    tokens: Path
    joiner: Path | None = None
    multilingual: bool = True


def _pick_onnx(folder: Path, pattern: str) -> Path | None:
    """The file matching ``pattern`` (glob), preferring the int8-quantised variant."""
    found = sorted(p for p in folder.glob(pattern) if p.is_file() and p.stat().st_size > 0)
    if not found:
        return None
    return next((p for p in found if ".int8." in p.name), found[0])


def sherpa_layout(folder: Path) -> SherpaLayout | None:
    """Recognise a sherpa-onnx model folder; None if it is missing, incomplete or of an unknown kind.

    Supported: Whisper exports (``<name>-encoder[.int8].onnx``,
    ``<name>-decoder[.int8].onnx``, ``<name>-tokens.txt``) and NeMo transducers
    such as Parakeet TDT (``encoder``/``decoder``/``joiner[.int8].onnx``,
    ``tokens.txt``).
    """
    if not folder.is_dir():
        return None
    tokens = folder / "tokens.txt"
    if tokens.is_file():
        encoder, decoder, joiner = (_pick_onnx(folder, f"{part}*.onnx") for part in ("encoder", "decoder", "joiner"))
        if encoder and decoder and joiner:
            return SherpaLayout("transducer", encoder, decoder, tokens, joiner=joiner)
    for whisper_tokens in sorted(folder.glob("*-tokens.txt")):
        prefix = whisper_tokens.name[: -len("-tokens.txt")]
        encoder = _pick_onnx(folder, f"{glob_escape(prefix)}-encoder*.onnx")
        decoder = _pick_onnx(folder, f"{glob_escape(prefix)}-decoder*.onnx")
        if encoder and decoder:
            return SherpaLayout("whisper", encoder, decoder, whisper_tokens, multilingual=not prefix.endswith(".en"))
    return None


def glob_escape(text: str) -> str:
    """Escape glob metacharacters in a literal file-name prefix."""
    return re.sub(r"([*?\[\]])", r"[\1]", text)


_MODEL_NAME_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")


def sherpa_model_dir(settings: Settings, model: str) -> tuple[Path, bool]:
    """Where a sherpa model lives: ``(folder, is_downloadable)``.

    A bare name is a folder under ``<home>/models`` that can be downloaded from
    the sherpa-onnx release; anything that looks like a path is used as it is.
    """
    as_path = Path(model).expanduser()
    if as_path.is_absolute() or "/" in model or os.sep in model or model.startswith(("~", ".")):
        return as_path, False
    return settings.models_dir / model, True


class _DownloadLog:
    """Progress callback that logs a line every ten percent."""

    def __init__(self, label: str):
        self.label = label
        self._step = -1

    def __call__(self, done: int, total: int | None) -> None:
        if not total:
            return
        step = int(10 * done / total)
        if step != self._step:
            self._step = step
            log.info("downloading %s: %d%% of %.0f MB", self.label, min(100, 10 * step), total / 1e6)


def ensure_sherpa_model(settings: Settings, model: str) -> tuple[Path, SherpaLayout]:
    """Find the model folder, downloading and unpacking it into ``<home>/models`` if it is missing."""
    folder, downloadable = sherpa_model_dir(settings, model)
    layout = sherpa_layout(folder)
    if layout is not None:
        return folder, layout
    expected = (
        "a Whisper export (<name>-encoder.onnx, <name>-decoder.onnx, <name>-tokens.txt) or a "
        "NeMo transducer such as Parakeet (encoder.onnx, decoder.onnx, joiner.onnx, tokens.txt)"
    )
    if not downloadable:
        raise BackendUnavailable(
            f"asr.model points at {folder}, which is not a sherpa-onnx model folder.\n"
            f"Expected {expected}.\n"
            f'Set asr.model = "auto" in config.toml to use {DEFAULT_MODELS["sherpa-onnx"]} (downloaded automatically).'
        )
    if not _MODEL_NAME_RE.fullmatch(model):
        raise BackendUnavailable(
            f'asr.model = "{model}" is not a sherpa-onnx model name. Use "auto", or a name from {SHERPA_MODEL_LIST}'
        )
    url = SHERPA_MODEL_URL.format(name=model)
    log.info("speech model %s is not installed yet; downloading it to %s", model, settings.models_dir)
    try:
        modelfetch.fetch_archive(url, settings.models_dir, expected_member=model, progress=_DownloadLog(model))
    except modelfetch.ModelFetchError as exc:
        raise BackendUnavailable(
            f'The speech model "{model}" is not installed and could not be downloaded.\n{exc}\n'
            f'(If the name is wrong: asr.model = "auto" uses {DEFAULT_MODELS["sherpa-onnx"]}; '
            f"all names are listed at {SHERPA_MODEL_LIST})"
        ) from exc
    layout = sherpa_layout(folder)
    if layout is None:
        raise BackendUnavailable(
            f'"{model}" was downloaded to {folder} but is not a kind of model videonotes can run.\n'
            f"Supported: {expected}."
        )
    return folder, layout


class SherpaOnnxEngine:
    """ONNX Runtime on the CPU through ``sherpa-onnx``.

    Whisper models have a fixed 30 s window, so they get 28 s chunks; NeMo
    transducers (Parakeet) take longer audio and return per-token timestamps.
    """

    def __init__(self, folder: Path, layout: SherpaLayout, *, threads: int | None = None):
        try:
            import sherpa_onnx
        except ImportError as exc:
            raise _missing("sherpa-onnx") from exc
        self.layout = layout
        threads = threads or _threads()
        try:
            if layout.family == "whisper":
                self.max_chunk_s = WHISPER_WINDOW_CHUNK_S
                self._recognizer: Any = sherpa_onnx.OfflineRecognizer.from_whisper(
                    encoder=str(layout.encoder),
                    decoder=str(layout.decoder),
                    tokens=str(layout.tokens),
                    language="" if layout.multilingual else "en",  # "" = detect; set per stream when known
                    task="transcribe",
                    num_threads=threads,
                    enable_segment_timestamps=True,
                )
            else:
                self.max_chunk_s = PARAKEET_CHUNK_S
                self._recognizer = sherpa_onnx.OfflineRecognizer.from_transducer(
                    encoder=str(layout.encoder),
                    decoder=str(layout.decoder),
                    joiner=str(layout.joiner),
                    tokens=str(layout.tokens),
                    num_threads=threads,
                    decoding_method="greedy_search",
                    model_type="nemo_transducer",
                )
        except Exception as exc:
            raise BackendUnavailable(
                f"sherpa-onnx could not load the model in {folder} ({type(exc).__name__}: {exc}).\n"
                "The files may be damaged: delete that folder and run the command again to download it afresh."
            ) from exc

    def transcribe(self, samples: np.ndarray, language: str | None) -> EngineResult:
        whisper = self.layout.family == "whisper"
        stream = self._recognizer.create_stream()
        if whisper and self.layout.multilingual and language:
            stream.set_option("language", language)
        stream.accept_waveform(SAMPLE_RATE, np.ascontiguousarray(samples, dtype=np.float32))
        self._recognizer.decode_stream(stream)
        result = stream.result
        duration = samples.size / float(SAMPLE_RATE)
        text = str(result.text or "")
        pieces: list[Piece] = []
        if whisper:
            starts = list(getattr(result, "segment_timestamps", None) or [])
            lengths = list(getattr(result, "segment_durations", None) or [])
            texts = list(getattr(result, "segment_texts", None) or [])
            if texts and len(texts) == len(starts) == len(lengths):
                pieces = [
                    Piece(t0=float(s), t1=float(s) + max(0.0, float(d)), text=str(t))
                    for s, d, t in zip(starts, lengths, texts, strict=True)
                ]
            detected = normalise_language(str(getattr(result, "lang", "") or "")) if language is None else None
        else:
            pieces = pieces_from_tokens(
                list(result.tokens), list(result.timestamps), list(getattr(result, "durations", None) or []), duration
            )
            detected = None
        if not pieces and text.strip():
            pieces = [Piece(t0=0.0, t1=duration, text=text)]
        return EngineResult(pieces, language=detected)

    def close(self) -> None:
        self._recognizer = None
        gc.collect()


# ==========================================================================================
# Factory and status
# ==========================================================================================


@dataclass(frozen=True)
class _Spec:
    name: str
    modules: tuple[str, ...]  # all must be importable
    package: str  # what to pip-install
    needs_mlx: bool = False

    def install_text(self) -> str:
        return f'The speech-to-text backend "{self.name}" is not installed. Install it with:  pip install {self.package}'


_SPECS = {
    "mlx-whisper": _Spec("mlx-whisper", ("mlx.core", "mlx_whisper"), "mlx-whisper", needs_mlx=True),
    "parakeet-mlx": _Spec("parakeet-mlx", ("mlx.core", "parakeet_mlx"), "parakeet-mlx", needs_mlx=True),
    "faster-whisper": _Spec("faster-whisper", ("faster_whisper",), "faster-whisper"),
    "sherpa-onnx": _Spec("sherpa-onnx", ("sherpa_onnx",), "sherpa-onnx"),
}

#: Repositories behind faster-whisper's short model names (faster_whisper/utils.py, 1.2.1).
_FASTER_WHISPER_REPOS = {
    "tiny.en": "Systran/faster-whisper-tiny.en",
    "tiny": "Systran/faster-whisper-tiny",
    "base.en": "Systran/faster-whisper-base.en",
    "base": "Systran/faster-whisper-base",
    "small.en": "Systran/faster-whisper-small.en",
    "small": "Systran/faster-whisper-small",
    "medium.en": "Systran/faster-whisper-medium.en",
    "medium": "Systran/faster-whisper-medium",
    "large-v3": "Systran/faster-whisper-large-v3",
    "distil-large-v3.5": "distil-whisper/distil-large-v3.5-ct2",
    "large-v3-turbo": "mobiuslabsgmbh/faster-whisper-large-v3-turbo",
    "turbo": "mobiuslabsgmbh/faster-whisper-large-v3-turbo",
}


def auto_order() -> tuple[str, ...]:
    """The order in which ``asr.backend = "auto"`` tries backends on this machine."""
    if is_apple_silicon():
        return ("mlx-whisper", "parakeet-mlx", "faster-whisper", "sherpa-onnx")
    return ("faster-whisper", "sherpa-onnx")


def backend_problem(name: str) -> str | None:
    """None if the backend's package can be imported here; otherwise what to do about it."""
    spec = _SPECS[name]
    if spec.needs_mlx and is_macos() and not is_apple_silicon():
        return (
            f'"{name}" needs an Apple Silicon Mac (MLX does not run on Intel Macs). '
            'Use asr.backend = "faster-whisper" or "sherpa-onnx" instead.'
        )
    if not all(module_available(module) for module in spec.modules):
        return spec.install_text()
    return None


def resolve_model(settings: Settings, backend: str) -> str:
    """``asr.model`` for a backend: its default when the setting is ``"auto"``."""
    model = (settings.asr.model or "").strip()
    return DEFAULT_MODELS[backend] if model.lower() in ("", "auto") else model


def _engine_loader(settings: Settings, backend: str, model: str) -> Callable[[], Engine]:
    if backend == "mlx-whisper":
        return lambda: MlxWhisperEngine(model)
    if backend == "parakeet-mlx":
        return lambda: ParakeetMlxEngine(model)
    if backend == "faster-whisper":
        return lambda: FasterWhisperEngine(model, vad=settings.asr.vad)

    def load_sherpa() -> Engine:
        if not module_available("sherpa_onnx"):
            raise _missing("sherpa-onnx")
        folder, layout = ensure_sherpa_model(settings, model)
        return SherpaOnnxEngine(folder, layout)

    return load_sherpa


def _selected_backend(settings: Settings) -> str | None:
    """The backend the settings resolve to, or None. Raises BackendUnavailable for a bad explicit choice."""
    wanted = (settings.asr.backend or "auto").strip().lower()
    if wanted == "none":
        return None
    if wanted == "auto":
        return next((name for name in auto_order() if backend_problem(name) is None), None)
    if wanted not in _SPECS:
        raise BackendUnavailable(
            f'Unknown speech-to-text backend asr.backend = "{settings.asr.backend}". '
            f"Choose one of: auto, {', '.join(BACKENDS)}, none."
        )
    problem = backend_problem(wanted)
    if problem:
        raise BackendUnavailable(problem)
    return wanted


def make_transcriber(settings: Settings) -> Transcriber | None:
    """Build the transcriber the settings ask for.

    Returns None when ``asr.backend`` is ``"none"``, or when ``"auto"`` finds
    no installed backend.  Raises :class:`BackendUnavailable` (with the install
    command) when an explicitly chosen backend cannot run here.  No model is
    loaded or downloaded until the first file with speech is transcribed.
    """
    backend = _selected_backend(settings)
    if backend is None:
        return None
    model = resolve_model(settings, backend)
    return SpeechTranscriber(
        backend,
        model,
        _engine_loader(settings, backend, model),
        vad=settings.asr.vad,
        language=settings.asr.language,
    )


def _hf_cached(repo_id: str) -> bool:
    """True if huggingface_hub's cache already holds a snapshot of ``repo_id`` (no import needed)."""
    env = os.environ
    cache = env.get("HF_HUB_CACHE") or env.get("HUGGINGFACE_HUB_CACHE")
    if not cache:
        home = env.get("HF_HOME") or os.path.join(env.get("XDG_CACHE_HOME") or "~/.cache", "huggingface")
        cache = os.path.join(home, "hub")
    snapshots = Path(cache).expanduser() / ("models--" + repo_id.replace("/", "--")) / "snapshots"
    try:
        return snapshots.is_dir() and any(snapshots.iterdir())
    except OSError:
        return False


def _model_detail(settings: Settings, backend: str, model: str) -> str:
    """The resolved model, plus a note when using it will first need a download."""
    if backend == "sherpa-onnx":
        folder, downloadable = sherpa_model_dir(settings, model)
        if sherpa_layout(folder) is not None:
            return model
        if not downloadable:
            return f"{model} (not a sherpa-onnx model folder)"
        size = _SHERPA_DOWNLOAD_MB.get(model)
        return f"{model} ({f'{size} MB, ' if size else ''}downloaded on first use)"
    with contextlib.suppress(OSError):
        if Path(model).expanduser().is_dir():
            return model
    repo = _FASTER_WHISPER_REPOS.get(model, model) if backend == "faster-whisper" else model
    if "/" in repo and not _hf_cached(repo):
        return f"{model} (downloaded from Hugging Face on first use)"
    return model


def asr_status(settings: Settings) -> list[BackendStatus]:
    """One entry per backend for ``vnote doctor``; at most one is marked ``selected``.

    ``detail`` is the resolved model when the backend can be used, otherwise
    the instruction that makes it usable.  Nothing is imported, loaded or
    downloaded.
    """
    try:
        selected = _selected_backend(settings)
    except BackendUnavailable:
        selected = None  # an explicit choice that cannot run: nothing is in use
    order = list(auto_order()) + [name for name in BACKENDS if name not in auto_order()]
    statuses: list[BackendStatus] = []
    for name in order:
        problem = backend_problem(name)
        detail = problem if problem else _model_detail(settings, name, resolve_model(settings, name))
        statuses.append(BackendStatus(name=name, available=problem is None, detail=detail, selected=name == selected))
    return statuses
