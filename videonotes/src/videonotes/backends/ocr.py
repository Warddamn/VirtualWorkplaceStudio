"""Reading text off keyframes (OCR).

Two interchangeable engines behind :class:`videonotes.backends.base.OcrEngine`:

* ``apple-vision`` - Apple's Vision framework through pyobjc (``VNRecognizeTextRequest``,
  accurate level, language correction on).  Part of macOS, fully on-device, fast.
* ``rapidocr`` - PP-OCR models run with ONNX Runtime.  Works everywhere (it is what the
  test-suite runs for real) and its models ship inside the ``rapidocr`` wheel, so nothing is
  downloaded: if the package ever asks for a download, that is reported as a broken install.

``ocr.backend = "auto"`` picks Apple Vision on a Mac when the pyobjc bindings are installed,
otherwise RapidOCR when it is installed, otherwise nothing (the pipeline then records the OCR
stage as skipped).

Engines return every line they found, in reading order, with a confidence and a normalised
top-left ``(x, y, w, h)`` box.  :func:`clean_ocr_text` turns that into the text that is stored
and searched: confident, de-duplicated lines with the noise removed.
"""

from __future__ import annotations

import gc
import importlib.util
import logging
import struct
from collections.abc import Callable, Iterator, Sequence
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from ..config import Settings, is_apple_silicon, is_macos
from .base import BackendError, BackendUnavailable, OcrEngine, OcrLine, OcrResult
from .status import BackendStatus, module_available

log = logging.getLogger("videonotes.ocr")

#: Values accepted for ``ocr.backend`` in config.toml.
OCR_BACKENDS = ("auto", "apple-vision", "rapidocr", "none")

APPLE_VISION_INSTALL_HINT = (
    "Apple Vision OCR needs the pyobjc bindings for the Vision framework. Install them with:  "
    "pip install pyobjc-framework-Vision"
)
APPLE_VISION_NOT_MAC_HINT = (
    'Apple Vision OCR only exists on macOS. Set  ocr.backend = "rapidocr"  (or "auto") in config.toml.'
)
RAPIDOCR_REINSTALL_HINT = (
    "Reinstall it so the model files that ship inside the package are restored:  "
    "pip install --force-reinstall rapidocr"
)


# ---------------------------------------------------------------------------
# Geometry and reading order (pure functions)
# ---------------------------------------------------------------------------


def _clamp01(value: float) -> float:
    return min(1.0, max(0.0, float(value)))


def _box_from_edges(x0: float, y0: float, x1: float, y1: float) -> tuple[float, float, float, float]:
    """Normalised ``(x, y, w, h)`` from edges, clipped to the image."""
    left, top = _clamp01(min(x0, x1)), _clamp01(min(y0, y1))
    right, bottom = _clamp01(max(x0, x1)), _clamp01(max(y0, y1))
    return (left, top, right - left, bottom - top)


def vision_box_to_top_left(x: float, y: float, w: float, h: float) -> tuple[float, float, float, float]:
    """Convert a Vision ``boundingBox`` to the contract's box.

    Vision reports rectangles normalised to the image with the origin at the image's
    **lower-left** corner (``VNDetectedObjectObservation.boundingBox``); the contract wants
    ``(x, y, w, h)`` with the origin at the **top-left**.  Only the vertical axis flips:
    the top edge is ``1 - (y + h)``.
    """
    return _box_from_edges(x, 1.0 - (y + h), x + w, 1.0 - y)


def sort_reading_order(lines: Sequence[OcrLine], *, tolerance: float = 0.5) -> list[OcrLine]:
    """Order lines top-to-bottom, then left-to-right, keeping one visual row together.

    Sorting by the top edge alone scrambles text that sits side by side (two columns of a
    table, a label next to its value) as soon as the boxes differ by a pixel.  Instead, lines
    are grouped into rows: a line joins the current row when its vertical centre is within
    ``tolerance`` x the smaller of the two line heights of the row's centre.  Rows are emitted
    top to bottom and each row left to right.

    Lines without a box cannot be placed; if any line lacks one the input order is kept.
    """
    items = list(lines)
    if len(items) < 2 or any(line.box is None for line in items):
        return items

    def centre(line: OcrLine) -> float:
        assert line.box is not None
        return line.box[1] + line.box[3] / 2.0

    rows: list[list[OcrLine]] = []
    row_centre = 0.0
    row_height = 0.0
    for line in sorted(items, key=lambda ln: (centre(ln), ln.box[0])):  # type: ignore[index]
        assert line.box is not None
        height = line.box[3]
        cy = centre(line)
        if rows and abs(cy - row_centre) <= tolerance * min(height, row_height):
            row = rows[-1]
            row.append(line)
            row_centre += (cy - row_centre) / len(row)
            row_height += (height - row_height) / len(row)
        else:
            rows.append([line])
            row_centre, row_height = cy, height
    ordered: list[OcrLine] = []
    for row in rows:
        ordered.extend(sorted(row, key=lambda ln: (ln.box[0], ln.box[1])))  # type: ignore[index]
    return ordered


# ---------------------------------------------------------------------------
# Cleaning OCR output for storage / search
# ---------------------------------------------------------------------------

#: A line needs at least this many letters/digits, and this share of its visible characters
#: must be letters/digits, to count as text rather than as a texture misread ("|||", "~ - .").
_MIN_ALNUM = 2
_MIN_ALNUM_SHARE = 0.4


def _is_noise(text: str) -> bool:
    visible = [ch for ch in text if not ch.isspace()]
    alnum = sum(1 for ch in visible if ch.isalnum())
    if alnum < _MIN_ALNUM:  # empty, a single stray character, or punctuation only
        return True
    return alnum / len(visible) < _MIN_ALNUM_SHARE


def clean_ocr_text(result: OcrResult, *, min_confidence: float, min_chars: int) -> str:
    """The text worth keeping from one OCR result, one line per row, ``""`` if there is none.

    * lines below ``min_confidence`` are dropped;
    * so is noise: single stray characters and strings that are mostly punctuation;
    * whitespace inside a line is collapsed to single spaces;
    * a line that repeats an earlier one exactly is dropped (reading order is kept);
    * if what is left has fewer than ``min_chars`` non-space characters in total, the frame
      is treated as having no text.
    """
    kept: list[str] = []
    seen: set[str] = set()
    for line in result.lines:
        try:
            confident = float(line.confidence) >= min_confidence
        except (TypeError, ValueError):
            confident = False
        if not confident:  # also drops NaN confidences
            continue
        text = " ".join(str(line.text or "").split())
        if _is_noise(text) or text in seen:
            continue
        seen.add(text)
        kept.append(text)
    if sum(len(text.replace(" ", "")) for text in kept) < max(0, int(min_chars)):
        return ""
    return "\n".join(kept)


# ---------------------------------------------------------------------------
# EXIF orientation (pure Python: the core package must not need pillow)
# ---------------------------------------------------------------------------


def _tiff_orientation(tiff: bytes) -> int:
    if len(tiff) < 8:
        return 1
    endian = {b"II": "<", b"MM": ">"}.get(tiff[:2])
    if endian is None or struct.unpack(endian + "H", tiff[2:4])[0] != 42:
        return 1
    offset = struct.unpack(endian + "I", tiff[4:8])[0]
    if offset + 2 > len(tiff):
        return 1
    (count,) = struct.unpack(endian + "H", tiff[offset : offset + 2])
    for index in range(min(count, 512)):
        entry = tiff[offset + 2 + 12 * index : offset + 14 + 12 * index]
        if len(entry) < 12:
            break
        tag, kind = struct.unpack(endian + "HH", entry[:4])
        if tag == 0x0112:  # Orientation; a SHORT (3) or occasionally a LONG (4), stored in the value field
            (value,) = struct.unpack(endian + ("I" if kind == 4 else "H"), entry[8 : 8 + (4 if kind == 4 else 2)])
            return int(value) if 1 <= value <= 8 else 1
    return 1


def exif_orientation(path: str | Path) -> int:
    """EXIF orientation (1-8) of a JPEG file; 1 ("upright") when absent, unreadable or not a JPEG.

    Keyframes written by ffmpeg are already upright and carry no orientation tag, so this is 1
    for everything the pipeline produces; it matters for photos a user adds by hand.
    """
    try:
        with open(path, "rb") as fh:
            if fh.read(2) != b"\xff\xd8":
                return 1
            for _ in range(64):  # header segments only; never walks the image data
                head = fh.read(4)
                if len(head) < 4 or head[0] != 0xFF:
                    return 1
                marker, size = head[1], struct.unpack(">H", head[2:4])[0]
                if marker in (0xDA, 0xD9) or size < 2:  # start of scan / end of image
                    return 1
                if marker == 0xE1:  # APP1: EXIF (or XMP, which is skipped)
                    payload = fh.read(size - 2)
                    if payload[:6] == b"Exif\x00\x00":
                        return _tiff_orientation(payload[6:])
                else:
                    fh.seek(size - 2, 1)
    except (OSError, struct.error):
        return 1
    return 1


# ---------------------------------------------------------------------------
# Apple Vision
# ---------------------------------------------------------------------------


def match_languages(wanted: Sequence[str], supported: Sequence[str] | None) -> list[str]:
    """Map configured language codes onto the identifiers Vision actually supports.

    ``"en"`` or ``"en_us"`` become ``"en-US"``; codes Vision does not know are dropped with a
    warning, because an unsupported identifier makes every request fail.  With ``supported``
    unknown (very old macOS) the configured codes are passed through unchanged.
    """
    cleaned: list[str] = []
    for code in wanted:
        code = str(code).strip().replace("_", "-")
        if code and code not in cleaned:
            cleaned.append(code)
    if supported is None:
        return cleaned
    known = [str(s) for s in supported]
    chosen: list[str] = []
    for code in cleaned:
        match = next((s for s in known if s.casefold() == code.casefold()), None)
        if match is None:
            primary = code.casefold().split("-")[0]
            match = next((s for s in known if s.casefold().split("-")[0] == primary), None)
        if match is None:
            log.warning("Apple Vision cannot read language %r; ignoring it (supported: %s)", code, ", ".join(known))
        elif match not in chosen:
            chosen.append(match)
    if cleaned and not chosen:
        log.warning("none of the configured OCR languages is supported; using Apple Vision's default language")
    return chosen


class AppleVisionOcr:
    """OCR with Apple's Vision framework (``VNRecognizeTextRequest``) through pyobjc.

    Every selector used here was checked against Apple's ``Vision.framework`` headers and the
    pyobjc bindings; the OS boundary is kept to :meth:`_recognise` so the rest is testable
    without a Mac.  One autorelease pool is opened per image, and nothing Objective-C leaves
    it: text, confidence and boxes are copied into plain Python values first, so memory stays
    flat over thousands of frames.
    """

    name = "apple-vision"

    def __init__(self, languages: Sequence[str] = ("en-US",)) -> None:
        try:
            import objc  # type: ignore[import-not-found]
            import Vision  # type: ignore[import-not-found]
            from Foundation import NSURL  # type: ignore[import-not-found]
        except ImportError as exc:
            raise BackendUnavailable(f"{APPLE_VISION_INSTALL_HINT}  ({exc})") from exc
        for needed in ("VNRecognizeTextRequest", "VNImageRequestHandler"):
            if getattr(Vision, needed, None) is None:
                raise BackendUnavailable(
                    f"This macOS does not provide Vision.{needed} (text recognition needs macOS 10.15 or newer). "
                    'Set  ocr.backend = "rapidocr"  in config.toml instead.'
                )
        self._objc: Any = objc
        self._vision: Any = Vision
        self._nsurl: Any = NSURL
        #: VNRequestTextRecognitionLevelAccurate (0); "fast" is 1
        self._level = int(getattr(Vision, "VNRequestTextRecognitionLevelAccurate", 0))
        self._languages = match_languages(languages, self._supported_languages())
        self._closed = False

    def _new_request(self) -> Any:
        request = self._vision.VNRecognizeTextRequest.alloc().init()
        request.setRecognitionLevel_(self._level)
        request.setUsesLanguageCorrection_(True)
        return request

    def _supported_languages(self) -> list[str] | None:
        """Language identifiers the accurate recogniser supports, or None if they cannot be listed."""
        try:
            with self._objc.autorelease_pool():
                request = self._new_request()
                lister = getattr(request, "supportedRecognitionLanguagesAndReturnError_", None)  # macOS 12+
                if lister is None:
                    return None
                answer = lister(None)
                found = answer[0] if isinstance(answer, tuple) else answer
                names = [str(code) for code in (found or [])]
        except Exception as exc:  # listing languages must never stop OCR from working
            log.debug("could not list Apple Vision languages: %s", exc)
            return None
        return names or None

    def read(self, image_path: Path) -> OcrResult:
        """Recognise the text in one image file (anything ImageIO can open: JPEG, PNG, HEIC ...)."""
        if self._closed:
            raise BackendError("the Apple Vision OCR engine has been closed")
        path = Path(image_path)
        if not path.is_file():
            raise BackendError(f"OCR: image file not found: {path}")
        orientation = exif_orientation(path)
        try:
            with self._objc.autorelease_pool():
                lines = self._recognise(path, orientation)
        except (BackendError, BackendUnavailable):
            raise
        except Exception as exc:  # Objective-C exceptions surface as objc.error
            raise BackendError(f"Apple Vision could not read {path.name}: {exc}") from exc
        return OcrResult(lines=sort_reading_order(lines))

    def _recognise(self, path: Path, orientation: int) -> list[OcrLine]:
        """The Vision calls for one image. Must run inside an autorelease pool."""
        vision = self._vision
        request = self._new_request()
        if self._languages:
            request.setRecognitionLanguages_(self._languages)
        url = self._nsurl.fileURLWithPath_(str(path.absolute()))
        if orientation == 1:
            # Vision reads the file through ImageIO. ffmpeg-written keyframes are upright.
            handler = vision.VNImageRequestHandler.alloc().initWithURL_options_(url, {})
        else:
            # An explicit EXIF orientation "supersedes every other orientation information",
            # and results are then relative to the upright image.
            handler = vision.VNImageRequestHandler.alloc().initWithURL_orientation_options_(url, orientation, {})
        outcome = handler.performRequests_error_([request], None)
        # pyobjc returns (BOOL, NSError) for the out-parameter; tolerate a bare BOOL as well.
        ok, error = outcome if isinstance(outcome, tuple) else (outcome, None)
        if not ok:
            raise BackendError(f"Apple Vision could not read {path.name}: {_describe_nserror(error)}")
        lines: list[OcrLine] = []
        for observation in request.results() or []:
            candidates = observation.topCandidates_(1)
            if candidates is None or len(candidates) == 0:
                continue
            best = candidates[0]
            text = str(best.string() or "")
            if not text.strip():
                continue
            rect = observation.boundingBox()  # normalised, origin at the lower-left corner
            box = vision_box_to_top_left(
                float(rect.origin.x), float(rect.origin.y), float(rect.size.width), float(rect.size.height)
            )
            lines.append(OcrLine(text=text, confidence=float(best.confidence()), box=box))
        return lines

    def close(self) -> None:
        """Nothing heavy is held between images; this only marks the engine unusable."""
        self._closed = True


def _describe_nserror(error: Any) -> str:
    if error is None:
        return "the image could not be decoded (damaged or not an image file?)"
    try:
        return str(error.localizedDescription())
    except Exception:
        return str(error)


# ---------------------------------------------------------------------------
# RapidOCR (ONNX Runtime)
# ---------------------------------------------------------------------------


class _DownloadBlocked(RuntimeError):
    """Raised in place of an HTTP request RapidOCR was about to make."""


@contextmanager
def _no_model_downloads() -> Iterator[list[str]]:
    """Make RapidOCR's model downloader refuse to touch the network while the block runs.

    RapidOCR fetches a model file whenever the one it expects is missing or fails its
    checksum.  videonotes is local-first and is often used offline, where that turns into a
    minute-long hang followed by an obscure error on every frame, so the request is replaced
    by an exception and the URL is recorded in the yielded list.  Files that are present and
    valid never reach this code path.
    """
    blocked: list[str] = []
    downloader: Any = None
    original: Any = None
    try:
        from rapidocr.utils import download_file as _download_file  # type: ignore[import-not-found]

        downloader = getattr(_download_file, "DownloadFile", None)
        original = vars(downloader).get("_make_http_request") if downloader is not None else None
    except Exception as exc:  # a future rapidocr without this hook: nothing to guard
        log.debug("rapidocr download guard not installed: %s", exc)
    if downloader is None or original is None:
        yield blocked
        return

    def refuse(_cls: Any, url: Any, *_args: Any, **_kwargs: Any) -> Any:
        blocked.append(str(url))
        raise _DownloadBlocked(str(url))

    downloader._make_http_request = classmethod(refuse)
    try:
        yield blocked
    finally:
        downloader._make_http_request = original


def _download_message(urls: Sequence[str]) -> str:
    names = ", ".join(sorted({url.rsplit("/", 1)[-1] for url in urls})) or "a model file"
    return (
        f"RapidOCR wanted to download {names}, which normally ships inside the rapidocr package; "
        f"videonotes never downloads OCR models on its own. {RAPIDOCR_REINSTALL_HINT}"
    )


def _rapidocr_install_hint() -> str:
    if is_macos() and not is_apple_silicon():
        # onnxruntime stopped publishing Intel-Mac wheels after 1.23.2
        return "RapidOCR is not installed. Install it with:  pip install rapidocr 'onnxruntime<=1.23.2'"
    return "RapidOCR is not installed. Install it with:  pip install rapidocr onnxruntime"


def _rapidocr_problem() -> str | None:
    """Why RapidOCR cannot be used, as an instruction; None when it looks usable (no import)."""
    if not module_available("rapidocr"):
        return _rapidocr_install_hint()
    if not module_available("onnxruntime"):
        pin = "'onnxruntime<=1.23.2'" if is_macos() and not is_apple_silicon() else "onnxruntime"
        return f"RapidOCR is installed but its inference engine is not. Install it with:  pip install {pin}"
    try:
        spec = importlib.util.find_spec("rapidocr")
        locations = list(spec.submodule_search_locations or []) if spec is not None else []
    except (ImportError, ValueError, AttributeError):
        locations = []
    if locations and not any(Path(locations[0], "models").glob("*.onnx")):
        return f"RapidOCR is installed but its bundled model files are missing. {RAPIDOCR_REINSTALL_HINT}"
    return None


class RapidOcrEngine:
    """OCR with RapidOCR (PP-OCR detection + recognition models on ONNX Runtime, CPU).

    The models are loaded once, when the engine is created, so a broken install shows up as
    :class:`BackendUnavailable` up front instead of as an error on every frame.  RapidOCR's own
    confidence floor (0.5) applies before ``ocr.min_confidence`` does.  The bundled model reads
    Latin-script languages and Chinese; ``ocr.languages`` is not used by this engine.
    """

    name = "rapidocr"

    def __init__(self) -> None:
        problem = _rapidocr_problem()
        if problem:
            raise BackendUnavailable(problem)
        try:
            from rapidocr import RapidOCR  # type: ignore[import-not-found]
        except Exception as exc:  # ImportError, or a native library that will not load
            raise BackendUnavailable(
                f"RapidOCR could not be imported ({type(exc).__name__}: {exc}). "
                "Reinstall it:  pip install --force-reinstall rapidocr onnxruntime"
            ) from exc
        with _no_model_downloads() as blocked:
            try:
                engine = self._construct(RapidOCR)
                self._preload(engine)
            except Exception as exc:
                if blocked or isinstance(exc, _DownloadBlocked):
                    raise BackendUnavailable(_download_message(blocked)) from exc
                raise BackendUnavailable(
                    f"RapidOCR could not start ({type(exc).__name__}: {exc}). "
                    "Reinstall it:  pip install --force-reinstall rapidocr onnxruntime"
                ) from exc
        _quiet_rapidocr_logging()
        self._engine: Any = engine

    @staticmethod
    def _construct(factory: Callable[..., Any]) -> Any:
        _quiet_rapidocr_logging()
        try:
            return factory(params={"Global.log_level": "error"})
        except (TypeError, ValueError):  # a release without that config key
            return factory()

    @staticmethod
    def _preload(engine: Any) -> None:
        """Load the models now, so a broken install is reported once instead of on every frame.

        RapidOCR loads each model lazily on first use.  Its loaders are private, so if a release
        drops them, a blank image is pushed through the public call instead: that still creates
        the ONNX session of the detector, which is where a broken install fails.
        """
        loaders = [getattr(engine, hook, None) for hook in ("_load_det_model", "_load_cls_model", "_load_rec_model")]
        if any(callable(loader) for loader in loaders):
            for loader in loaders:
                if callable(loader):
                    loader()
            return
        import numpy as np

        engine(np.full((64, 64, 3), 255, dtype=np.uint8))

    def read(self, image_path: Path) -> OcrResult:
        """Recognise the text in one image file."""
        if self._engine is None:
            raise BackendError("the RapidOCR engine has been closed")
        path = Path(image_path)
        if not path.is_file():
            raise BackendError(f"OCR: image file not found: {path}")
        with _no_model_downloads() as blocked:
            try:
                raw = self._engine(path)
            except Exception as exc:
                if blocked or isinstance(exc, _DownloadBlocked):
                    raise BackendUnavailable(_download_message(blocked)) from exc
                unreadable = isinstance(exc, OSError) or type(exc).__name__ == "LoadImageError"
                hint = "; the file may be damaged or not an image" if unreadable else ""
                raise BackendError(f"OCR failed on {path.name} ({type(exc).__name__}: {exc}){hint}") from exc
        if blocked:
            raise BackendUnavailable(_download_message(blocked))
        return rapidocr_result(raw)

    def close(self) -> None:
        """Drop the ONNX sessions (a few hundred MB)."""
        self._engine = None
        gc.collect()


def _quiet_rapidocr_logging() -> None:
    """RapidOCR logs every model path at INFO and "no text found" at WARNING to stderr."""
    logging.getLogger("RapidOCR").setLevel(logging.ERROR)


def rapidocr_result(raw: Any) -> OcrResult:
    """Convert a ``RapidOCROutput`` (``txts``, ``scores``, pixel quads in ``boxes``) to an OcrResult."""
    texts = getattr(raw, "txts", None)
    if texts is None or len(texts) == 0:
        return OcrResult()
    scores = getattr(raw, "scores", None)
    quads = getattr(raw, "boxes", None)
    shape = getattr(getattr(raw, "img", None), "shape", None)
    rects: list[tuple[float, float, float, float] | None] = []
    for index in range(len(texts)):
        rect = None
        if quads is not None and index < len(quads):
            try:
                xs = [float(point[0]) for point in quads[index]]
                ys = [float(point[1]) for point in quads[index]]
                rect = (min(xs), min(ys), max(xs), max(ys))
            except (TypeError, ValueError, IndexError):
                rect = None
        rects.append(rect)
    exact = shape is not None and len(shape) >= 2 and shape[0] > 0 and shape[1] > 0
    if exact:
        height, width = float(shape[0]), float(shape[1])
    else:  # image size unknown: scale by the text extent, good enough to order the lines
        width = max((r[2] for r in rects if r), default=0.0) or 1.0
        height = max((r[3] for r in rects if r), default=0.0) or 1.0
    lines: list[OcrLine] = []
    for index, text in enumerate(texts):
        text = str(text or "")
        if not text.strip():
            continue
        try:
            confidence = float(scores[index]) if scores is not None and index < len(scores) else 1.0
        except (TypeError, ValueError):
            confidence = 0.0
        rect = rects[index]
        box = _box_from_edges(rect[0] / width, rect[1] / height, rect[2] / width, rect[3] / height) if rect else None
        lines.append(OcrLine(text=text, confidence=confidence, box=box))
    ordered = sort_reading_order(lines)
    if not exact:
        for line in ordered:
            line.box = None  # do not hand out boxes that are not really normalised to the image
    return OcrResult(lines=ordered)


# ---------------------------------------------------------------------------
# Factory and status
# ---------------------------------------------------------------------------


def _apple_vision_problem() -> str | None:
    """Why Apple Vision OCR cannot be used, as an instruction; None when it looks usable."""
    if not is_macos():
        return APPLE_VISION_NOT_MAC_HINT
    if not (module_available("Vision") and module_available("objc")):
        return APPLE_VISION_INSTALL_HINT
    return None


def _backend_name(settings: Settings) -> str:
    return str(settings.ocr.backend or "auto").strip().lower().replace("_", "-") or "auto"


def _auto_order() -> tuple[str, ...]:
    return ("apple-vision", "rapidocr") if is_macos() else ("rapidocr",)


_PROBLEMS: dict[str, Callable[[], str | None]] = {
    "apple-vision": lambda: _apple_vision_problem(),
    "rapidocr": lambda: _rapidocr_problem(),
}


def _build(name: str, settings: Settings) -> OcrEngine:
    if name == "apple-vision":
        return AppleVisionOcr(settings.ocr.languages)
    return RapidOcrEngine()


def make_ocr(settings: Settings) -> OcrEngine | None:
    """The OCR engine the settings ask for.

    ``None`` when ``ocr.backend`` is ``"none"`` or when ``"auto"`` finds nothing usable
    (macOS: Apple Vision, then RapidOCR; elsewhere: RapidOCR).  Raises
    :class:`BackendUnavailable` - with the command that fixes it - when an explicitly chosen
    backend cannot run or the setting is not a known backend.
    """
    backend = _backend_name(settings)
    if backend == "none":
        return None
    if backend == "auto":
        for name in _auto_order():
            problem = _PROBLEMS[name]()
            if problem:
                log.debug("ocr auto: %s not usable: %s", name, problem)
                continue
            try:
                return _build(name, settings)
            except BackendUnavailable as exc:
                log.warning("ocr auto: %s could not start, trying the next option: %s", name, exc)
        return None
    if backend not in _PROBLEMS:
        raise BackendUnavailable(
            f'Unknown OCR backend "{settings.ocr.backend}" in config.toml. '
            f"Set ocr.backend to one of: {', '.join(OCR_BACKENDS)}."
        )
    problem = _PROBLEMS[backend]()
    if problem:
        raise BackendUnavailable(problem)
    return _build(backend, settings)


def ocr_status(settings: Settings) -> list[BackendStatus]:
    """Availability of each OCR backend for ``vnote doctor`` (cheap: imports and loads nothing)."""
    backend = _backend_name(settings)
    problems = {name: check() for name, check in _PROBLEMS.items()}
    if backend == "auto":
        selected = next((name for name in _auto_order() if problems[name] is None), None)
    else:
        selected = backend if backend in problems and problems[backend] is None else None
    languages = ", ".join(str(code) for code in settings.ocr.languages) or "system default"
    details = {
        "apple-vision": f"Apple Vision framework on this Mac (accurate mode; languages: {languages})",
        "rapidocr": "PP-OCR models bundled with the rapidocr package (ONNX Runtime on the CPU, works offline)",
    }
    return [
        BackendStatus(
            name=name,
            available=problems[name] is None,
            detail=problems[name] or details[name],
            selected=selected == name,
        )
        for name in ("apple-vision", "rapidocr")
    ]
