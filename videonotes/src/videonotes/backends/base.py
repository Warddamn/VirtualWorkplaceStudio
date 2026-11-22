"""Interfaces every perception / language backend implements.

The pipeline only ever talks to these protocols, so backends are swappable
(Apple-Silicon MLX models, CPU ONNX models, a local Ollama server, or — only
when the user explicitly selects it — a cloud API).

Rules for backend authors
-------------------------
* Heavy imports (mlx, torch, onnxruntime, pyobjc, bleak, anthropic …) happen
  lazily inside the backend, never at module import time, so ``import
  videonotes`` and the CLI stay fast and work without optional dependencies.
* Raise :class:`BackendUnavailable` (with a message telling the user exactly
  what to install or start) when a backend cannot be used on this machine.
* ``close()`` must release model memory.  The pipeline loads one heavy model
  at a time on a 16 GB machine and calls ``close()`` before loading the next.
* Backends are synchronous and are called from a single worker thread.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol, runtime_checkable


class BackendUnavailable(RuntimeError):
    """The requested backend cannot run here (missing package, server, model, OS)."""


class BackendError(RuntimeError):
    """A backend was available but failed on a particular input."""


# -- speech to text ----------------------------------------------------------


@dataclass
class TranscriptSegment:
    t0: float  # seconds from the start of the audio file
    t1: float
    text: str
    speaker: str | None = None


@runtime_checkable
class Transcriber(Protocol):
    name: str  # e.g. "mlx-whisper:large-v3-turbo"

    def transcribe(self, wav_path: Path, *, language: str | None = None) -> list[TranscriptSegment]:
        """Transcribe a 16 kHz mono WAV file. ``language=None`` means auto-detect.

        Must return segments in time order with ``t0 <= t1``; must return ``[]``
        (not hallucinated text) for silence.
        """
        ...

    def close(self) -> None: ...


# -- OCR ---------------------------------------------------------------------


@dataclass
class OcrLine:
    text: str
    confidence: float = 1.0
    #: normalised (x, y, w, h) with the origin at the TOP-LEFT of the image, or None
    box: tuple[float, float, float, float] | None = None


@dataclass
class OcrResult:
    lines: list[OcrLine] = field(default_factory=list)

    @property
    def text(self) -> str:
        """Lines joined in reading order (top-to-bottom, then left-to-right)."""
        return "\n".join(line.text for line in self.lines if line.text.strip())


@runtime_checkable
class OcrEngine(Protocol):
    name: str  # e.g. "apple-vision"

    def read(self, image_path: Path) -> OcrResult:
        """Recognise text in one image. Lines must be returned in reading order."""
        ...

    def close(self) -> None: ...


# -- image captioning --------------------------------------------------------


@runtime_checkable
class Captioner(Protocol):
    name: str  # e.g. "ollama:qwen2.5vl:3b"

    def caption(self, image_path: Path, *, context: str = "") -> str:
        """Describe what the camera wearer is looking at / doing in 1-3 sentences.

        ``context`` is optional grounding text (OCR text found in the frame).
        """
        ...

    def close(self) -> None: ...


# -- text LLM ----------------------------------------------------------------


@runtime_checkable
class LLM(Protocol):
    name: str  # e.g. "ollama:qwen3:4b"
    #: rough budget of *input* tokens the caller may put in one prompt
    context_tokens: int

    def json(self, *, system: str, prompt: str, schema: dict[str, Any], max_tokens: int = 2048) -> dict[str, Any]:
        """Return a JSON object conforming to ``schema`` (a JSON Schema object).

        Implementations use the provider's structured-output feature when there
        is one and otherwise parse leniently (see ``videonotes.backends.jsonutil``).
        Raises :class:`BackendError` if no valid object can be obtained.
        """
        ...

    def text(self, *, system: str, prompt: str, max_tokens: int = 1024) -> str: ...

    def close(self) -> None: ...
