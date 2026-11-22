"""Swappable perception and language backends. See :mod:`videonotes.backends.base`."""

from .base import (
    LLM,
    BackendError,
    BackendUnavailable,
    Captioner,
    OcrEngine,
    OcrLine,
    OcrResult,
    Transcriber,
    TranscriptSegment,
)

__all__ = [
    "LLM",
    "BackendError",
    "BackendUnavailable",
    "Captioner",
    "OcrEngine",
    "OcrLine",
    "OcrResult",
    "Transcriber",
    "TranscriptSegment",
]
