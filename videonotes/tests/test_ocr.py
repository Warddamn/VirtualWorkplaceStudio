from __future__ import annotations

import importlib.machinery
import importlib.util
import struct
import sys
import types
from pathlib import Path
from types import SimpleNamespace

import pytest

from videonotes.backends import BackendError, BackendUnavailable, OcrEngine, OcrLine, OcrResult
from videonotes.backends import ocr as ocr_mod
from videonotes.backends.ocr import (
    AppleVisionOcr,
    clean_ocr_text,
    exif_orientation,
    make_ocr,
    match_languages,
    ocr_status,
    rapidocr_result,
    sort_reading_order,
    vision_box_to_top_left,
)
from videonotes.config import Settings
from videonotes.media import ffmpeg as ff

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

_FONTS = (
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/Library/Fonts/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/dejavu/DejaVuSans.ttf",
)


def _esc(path: Path) -> str:
    """Escape a path for use inside an ffmpeg filter argument (same rule as videonotes.demo)."""
    return str(path).replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'").replace(",", "\\,")


def render_text_image(
    path: Path,
    placed: list[tuple[str, int, int]],
    *,
    size: str = "960x540",
    background: str = "0xF4F4F0",
    color: str = "black",
    font_size: int = 44,
) -> Path:
    """Draw each ``(text, x, y)`` with ffmpeg drawtext, the way the demo clip draws its scenes."""
    font = next((f for f in _FONTS if Path(f).is_file()), None)
    filters = []
    for index, (text, x, y) in enumerate(placed):
        textfile = path.with_name(f"{path.stem}_{index}.txt")
        textfile.write_text(text, encoding="utf-8")
        spec = f"drawtext=textfile={_esc(textfile)}:fontsize={font_size}:fontcolor={color}:x={x}:y={y}"
        if font:
            spec += f":fontfile={_esc(Path(font))}"
        filters.append(spec)
    args = ["-f", "lavfi", "-i", f"color=c={background}:s={size}"]
    if filters:
        args += ["-vf", ",".join(filters)]
    ff.run(args + ["-frames:v", "1", "-update", "1", "-q:v", "2", str(path)], timeout=120)
    return path


def _norm(text: str) -> str:
    return " ".join(text.split()).casefold()


def line(text: str, x: float, y: float, w: float = 0.2, h: float = 0.05, confidence: float = 0.9) -> OcrLine:
    return OcrLine(text=text, confidence=confidence, box=(x, y, w, h))


def _settings(tmp_path: Path, backend: str = "auto") -> Settings:
    settings = Settings(home=tmp_path / "home")
    settings.ocr.backend = backend
    return settings


# ---------------------------------------------------------------------------
# reading order and box geometry
# ---------------------------------------------------------------------------


def test_vision_box_flips_only_the_vertical_axis():
    # Vision: origin bottom-left. A box whose bottom edge is at 0.7 and is 0.1 tall has its top at 0.2.
    assert vision_box_to_top_left(0.1, 0.7, 0.5, 0.1) == pytest.approx((0.1, 0.2, 0.5, 0.1))
    assert vision_box_to_top_left(0.0, 0.0, 1.0, 1.0) == pytest.approx((0.0, 0.0, 1.0, 1.0))
    # bottom strip of the image -> y close to 1 in top-left coordinates
    assert vision_box_to_top_left(0.25, 0.0, 0.5, 0.05) == pytest.approx((0.25, 0.95, 0.5, 0.05))


def test_vision_box_is_clipped_to_the_image():
    x, y, w, h = vision_box_to_top_left(-0.1, 0.9, 1.3, 0.2)
    assert (x, y) == pytest.approx((0.0, 0.0)) and w == pytest.approx(1.0) and h == pytest.approx(0.1)


def test_reading_order_top_to_bottom_then_left_to_right():
    lines = [line("third", 0.1, 0.5), line("second", 0.6, 0.1), line("first", 0.1, 0.1)]
    assert [ln.text for ln in sort_reading_order(lines)] == ["first", "second", "third"]


def test_reading_order_keeps_a_visual_row_together_despite_jitter():
    # Right-hand column sits a few pixels higher/lower than the left one: a plain sort on the
    # top edge would give Name, Room, 4B, Alice, Bob, 7C.
    lines = [
        line("Name", 0.10, 0.200),
        line("Room", 0.60, 0.210),
        line("4B", 0.60, 0.395),
        line("Alice", 0.10, 0.405),
        line("Bob", 0.10, 0.600),
        line("7C", 0.60, 0.612),
    ]
    assert [ln.text for ln in sort_reading_order(lines)] == ["Name", "Room", "Alice", "4B", "Bob", "7C"]


def test_reading_order_does_not_merge_adjacent_rows():
    # line spacing of 1.2x the height: centres are far more than half a height apart
    lines = [line("b", 0.5, 0.26, h=0.05), line("a", 0.1, 0.20, h=0.05), line("c", 0.1, 0.32, h=0.05)]
    assert [ln.text for ln in sort_reading_order(lines)] == ["a", "b", "c"]


def test_reading_order_small_text_next_to_a_headline_is_its_own_row():
    headline = line("HEADLINE", 0.1, 0.10, w=0.5, h=0.20)
    caption = line("small print", 0.7, 0.26, w=0.2, h=0.03)  # inside the headline's band, but near its bottom
    assert [ln.text for ln in sort_reading_order([caption, headline])] == ["HEADLINE", "small print"]


def test_reading_order_without_boxes_keeps_engine_order():
    lines = [OcrLine("z"), OcrLine("a"), line("m", 0.1, 0.1)]
    assert [ln.text for ln in sort_reading_order(lines)] == ["z", "a", "m"]
    assert sort_reading_order([]) == []


# ---------------------------------------------------------------------------
# clean_ocr_text
# ---------------------------------------------------------------------------


def test_clean_drops_low_confidence_and_keeps_order():
    lines = [OcrLine("Launch plan Q3", 0.95), OcrLine("smudge text", 0.2), OcrLine("Ship Falcon beta", 0.36)]
    result = OcrResult(lines)
    assert clean_ocr_text(result, min_confidence=0.35, min_chars=3) == "Launch plan Q3\nShip Falcon beta"
    assert clean_ocr_text(result, min_confidence=0.5, min_chars=3) == "Launch plan Q3"
    assert clean_ocr_text(result, min_confidence=0.0, min_chars=3).count("\n") == 2


def test_clean_drops_noise_lines():
    noise = ["|", "A", "7", "---", "~ . ~", "(!)", ":-)", "#1", "", "   ", "| | |"]
    result = OcrResult([OcrLine(text, 0.99) for text in noise] + [OcrLine("Room 4B", 0.99)])
    assert clean_ocr_text(result, min_confidence=0.3, min_chars=3) == "Room 4B"


@pytest.mark.parametrize("text", ["$5.00", "3 PM", "A&B", "50%", "\u51fa\u53e3", "Q3", "-> Exit"])
def test_clean_keeps_short_but_real_text(text):
    assert clean_ocr_text(OcrResult([OcrLine(text, 0.9)]), min_confidence=0.3, min_chars=1) == text


def test_clean_normalises_whitespace_and_deduplicates():
    result = OcrResult(
        [
            OcrLine("  Design \t Review\u00a03 PM ", 0.9),
            OcrLine("EXIT", 0.9),
            OcrLine("Design Review 3 PM", 0.8),  # identical after whitespace normalisation
            OcrLine("EXIT", 0.9),
            OcrLine("Exit", 0.9),  # different text: kept
        ]
    )
    assert clean_ocr_text(result, min_confidence=0.3, min_chars=3) == "Design Review 3 PM\nEXIT\nExit"


def test_clean_returns_empty_when_too_little_text():
    assert clean_ocr_text(OcrResult([OcrLine("4B", 0.9)]), min_confidence=0.3, min_chars=3) == ""
    assert clean_ocr_text(OcrResult([OcrLine("4B", 0.9)]), min_confidence=0.3, min_chars=2) == "4B"
    # spaces do not count towards the minimum
    assert clean_ocr_text(OcrResult([OcrLine("a  b", 0.9)]), min_confidence=0.3, min_chars=3) == ""
    assert clean_ocr_text(OcrResult(), min_confidence=0.3, min_chars=0) == ""
    two = OcrResult([OcrLine("ab", 0.9), OcrLine("cd", 0.9)])
    assert clean_ocr_text(two, min_confidence=0.3, min_chars=4) == "ab\ncd"
    assert clean_ocr_text(two, min_confidence=0.3, min_chars=5) == ""


def test_clean_survives_odd_confidences():
    odd = [
        OcrLine("not a number", float("nan")),
        OcrLine("fine text", 1.0),
        OcrLine("none conf", None),  # type: ignore[arg-type]
    ]
    result = OcrResult(odd)
    assert clean_ocr_text(result, min_confidence=0.35, min_chars=3) == "fine text"


# ---------------------------------------------------------------------------
# EXIF orientation
# ---------------------------------------------------------------------------


def _jpeg_with_orientation(value: int, *, endian: str = "<", kind: int = 3, extra_app1: bool = False) -> bytes:
    mark = b"II" if endian == "<" else b"MM"
    field = struct.pack(endian + "HH", value, 0) if kind == 3 else struct.pack(endian + "I", value)
    ifd = struct.pack(endian + "H", 2)
    ifd += struct.pack(endian + "HHI", 0x010F, 2, 1) + b"x\x00\x00\x00"  # Make (some other tag first)
    ifd += struct.pack(endian + "HHI", 0x0112, kind, 1) + field
    ifd += struct.pack(endian + "I", 0)
    tiff = mark + struct.pack(endian + "H", 42) + struct.pack(endian + "I", 8) + ifd
    exif = b"Exif\x00\x00" + tiff
    out = b"\xff\xd8" + b"\xff\xe0" + struct.pack(">H", 16) + b"JFIF\x00" + b"\x00" * 9
    if extra_app1:
        xmp = b"http://ns.adobe.com/xap/1.0/\x00<x/>"
        out += b"\xff\xe1" + struct.pack(">H", len(xmp) + 2) + xmp
    out += b"\xff\xe1" + struct.pack(">H", len(exif) + 2) + exif
    return out + b"\xff\xda\x00\x02" + b"\x00" * 16 + b"\xff\xd9"


@pytest.mark.parametrize("endian", ["<", ">"])
@pytest.mark.parametrize("value", [1, 3, 6, 8])
def test_exif_orientation_reads_both_byte_orders(tmp_path, endian, value):
    path = tmp_path / "o.jpg"
    path.write_bytes(_jpeg_with_orientation(value, endian=endian))
    assert exif_orientation(path) == value


def test_exif_orientation_edge_cases(tmp_path):
    path = tmp_path / "o.jpg"
    path.write_bytes(_jpeg_with_orientation(6, kind=4, extra_app1=True))  # LONG value, XMP segment before EXIF
    assert exif_orientation(path) == 6
    path.write_bytes(_jpeg_with_orientation(42))  # out of range
    assert exif_orientation(path) == 1
    path.write_bytes(b"\xff\xd8\xff\xe1\x00")  # truncated header
    assert exif_orientation(path) == 1
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 32)  # not a JPEG
    assert exif_orientation(path) == 1
    path.write_bytes(b"")
    assert exif_orientation(path) == 1
    assert exif_orientation(tmp_path / "missing.jpg") == 1


def test_exif_orientation_matches_a_real_encoder(tmp_path):
    image_mod = pytest.importorskip("PIL.Image")
    plain, rotated = tmp_path / "plain.jpg", tmp_path / "rotated.jpg"
    img = image_mod.new("RGB", (32, 16), "white")
    img.save(plain)
    exif = image_mod.Exif()
    exif[0x0112] = 6
    img.save(rotated, exif=exif)
    assert exif_orientation(plain) == 1
    assert exif_orientation(rotated) == 6


def test_exif_orientation_of_an_ffmpeg_keyframe_is_upright(tmp_path):
    if not ff.have_ffmpeg():
        pytest.skip("ffmpeg not installed")
    path = tmp_path / "kf.jpg"
    ff.run(["-f", "lavfi", "-i", "color=c=gray:s=64x48", "-frames:v", "1", "-update", "1", str(path)], timeout=60)
    assert exif_orientation(path) == 1


# ---------------------------------------------------------------------------
# Apple Vision through fake pyobjc modules
# ---------------------------------------------------------------------------


class _Obs:
    """A fake VNRecognizedTextObservation with a bottom-left-origin bounding box."""

    def __init__(self, events, text, confidence, x, y, w, h, *, candidates=1):
        self._events, self._text, self._confidence, self._n = events, text, confidence, candidates
        self._rect = SimpleNamespace(origin=SimpleNamespace(x=x, y=y), size=SimpleNamespace(width=w, height=h))

    def topCandidates_(self, count):
        self._events.append(("topCandidates", count))
        candidate = SimpleNamespace(string=lambda: self._text, confidence=lambda: self._confidence)
        return [candidate] * self._n

    def boundingBox(self):
        return self._rect


def _module(name: str) -> types.ModuleType:
    module = types.ModuleType(name)
    module.__spec__ = importlib.machinery.ModuleSpec(name, None)
    return module


@pytest.fixture()
def fake_pyobjc(monkeypatch):
    """Install fake ``objc`` / ``Vision`` / ``Foundation`` modules; returns the knobs and the call log."""
    state = SimpleNamespace(
        events=[],
        observations=[],
        supported=["en-US", "fr-FR", "de-DE", "zh-Hans"],
        outcome=(True, None),
        raise_in_perform=None,
        has_language_listing=True,
    )
    events = state.events

    class autorelease_pool:
        def __enter__(self):
            events.append("pool:enter")

        def __exit__(self, *exc):
            events.append("pool:exit")
            return False

    class Request:
        @classmethod
        def alloc(cls):
            return cls()

        def init(self):
            events.append("request:init")
            return self

        def setRecognitionLevel_(self, level):
            events.append(("level", level))

        def setUsesLanguageCorrection_(self, flag):
            events.append(("correction", flag))

        def setRecognitionLanguages_(self, languages):
            events.append(("languages", list(languages)))

        def results(self):
            events.append("results")
            return state.observations

        def __getattr__(self, name):
            if name == "supportedRecognitionLanguagesAndReturnError_" and state.has_language_listing:

                def lister(error):
                    events.append(("supported", error))
                    return (list(state.supported), None)

                return lister
            raise AttributeError(name)

    class Handler:
        @classmethod
        def alloc(cls):
            return cls()

        def initWithURL_options_(self, url, options):
            events.append(("handler", url.path, options))
            return self

        def initWithURL_orientation_options_(self, url, orientation, options):
            events.append(("handler+orientation", url.path, orientation, options))
            return self

        def performRequests_error_(self, requests, error):
            events.append(("perform", [type(r).__name__ for r in requests], error))
            if state.raise_in_perform:
                raise state.raise_in_perform
            return state.outcome

    class NSURL:
        @classmethod
        def fileURLWithPath_(cls, path):
            events.append(("url", path))
            return SimpleNamespace(path=path)

    objc, vision, foundation = _module("objc"), _module("Vision"), _module("Foundation")
    objc.autorelease_pool = autorelease_pool
    vision.VNRecognizeTextRequest = Request
    vision.VNImageRequestHandler = Handler
    vision.VNRequestTextRecognitionLevelAccurate = 0
    vision.VNRequestTextRecognitionLevelFast = 1
    foundation.NSURL = NSURL
    for module in (objc, vision, foundation):
        monkeypatch.setitem(sys.modules, module.__name__, module)
    return state


def test_apple_vision_call_sequence_and_box_conversion(fake_pyobjc, tmp_path):
    image = tmp_path / "frame.jpg"
    image.write_bytes(b"\xff\xd8\xff\xd9")
    engine = AppleVisionOcr(["en-US"])
    assert isinstance(engine, OcrEngine) and engine.name == "apple-vision"
    # construction asked Vision (inside a pool) which languages the accurate recogniser supports
    assert fake_pyobjc.events == [
        "pool:enter", "request:init", ("level", 0), ("correction", True), ("supported", None), "pool:exit",
    ]  # fmt: skip

    events = fake_pyobjc.events
    events.clear()
    # Vision hands results back bottom-up here; y is measured from the BOTTOM of the image.
    fake_pyobjc.observations = [
        _Obs(events, "Design Review 3 PM", 0.5, 0.10, 0.60, 0.50, 0.10),
        _Obs(events, "Room 4B", 1.0, 0.10, 0.75, 0.30, 0.10),
    ]
    result = engine.read(image)

    assert events == [
        "pool:enter",
        "request:init",
        ("level", 0),  # VNRequestTextRecognitionLevelAccurate
        ("correction", True),
        ("languages", ["en-US"]),
        ("url", str(image)),
        ("handler", str(image), {}),
        ("perform", ["Request"], None),
        "results",
        ("topCandidates", 1),
        ("topCandidates", 1),
        "pool:exit",
    ]
    assert [ln.text for ln in result.lines] == ["Room 4B", "Design Review 3 PM"]  # reading order: top first
    assert result.lines[0].box == pytest.approx((0.10, 0.15, 0.30, 0.10))  # 1 - (0.75 + 0.10)
    assert result.lines[1].box == pytest.approx((0.10, 0.30, 0.50, 0.10))  # 1 - (0.60 + 0.10)
    assert [ln.confidence for ln in result.lines] == [1.0, 0.5]
    # nothing Objective-C escapes the pool: plain Python values only
    assert all(type(ln.text) is str and type(ln.confidence) is float for ln in result.lines)
    assert result.text == "Room 4B\nDesign Review 3 PM"


def test_apple_vision_empty_and_candidate_less_observations(fake_pyobjc, tmp_path):
    image = tmp_path / "frame.jpg"
    image.write_bytes(b"x")
    engine = AppleVisionOcr(["en-US"])
    fake_pyobjc.observations = None  # request.results() is nil when nothing was recognised
    assert engine.read(image).lines == []
    events = fake_pyobjc.events
    fake_pyobjc.observations = [
        _Obs(events, "ghost", 0.9, 0.1, 0.5, 0.2, 0.1, candidates=0),
        _Obs(events, "   ", 0.9, 0.1, 0.3, 0.2, 0.1),
        _Obs(events, "kept", 0.3, 0.1, 0.1, 0.2, 0.1),
    ]
    assert [ln.text for ln in engine.read(image).lines] == ["kept"]


def test_apple_vision_failure_paths(fake_pyobjc, tmp_path):
    image = tmp_path / "frame.jpg"
    image.write_bytes(b"x")
    engine = AppleVisionOcr(["en-US"])
    with pytest.raises(BackendError, match="not found"):
        engine.read(tmp_path / "missing.jpg")

    fake_pyobjc.outcome = (False, SimpleNamespace(localizedDescription=lambda: "The file is damaged"))
    with pytest.raises(BackendError, match="The file is damaged"):
        engine.read(image)
    assert fake_pyobjc.events[-1] == "pool:exit"  # the pool is drained on the error path too

    fake_pyobjc.outcome = (False, None)
    with pytest.raises(BackendError, match="could not be decoded"):
        engine.read(image)

    fake_pyobjc.outcome = (True, None)
    fake_pyobjc.raise_in_perform = RuntimeError("NSInvalidArgumentException")
    with pytest.raises(BackendError, match="NSInvalidArgumentException"):
        engine.read(image)

    fake_pyobjc.raise_in_perform = None
    fake_pyobjc.outcome = True  # some bridges return a bare BOOL
    assert engine.read(image).lines == []

    engine.close()
    with pytest.raises(BackendError, match="closed"):
        engine.read(image)


def test_apple_vision_uses_explicit_orientation_for_rotated_stills(fake_pyobjc, tmp_path):
    image = tmp_path / "rotated.jpg"
    image.write_bytes(_jpeg_with_orientation(6))
    engine = AppleVisionOcr(["en-US"])
    fake_pyobjc.events.clear()
    engine.read(image)
    handlers = [e for e in fake_pyobjc.events if isinstance(e, tuple) and e[0].startswith("handler")]
    assert handlers == [("handler+orientation", str(image), 6, {})]


def test_apple_vision_language_resolution(fake_pyobjc, tmp_path, caplog):
    image = tmp_path / "frame.jpg"
    image.write_bytes(b"x")
    engine = AppleVisionOcr(["en", "klingon", "DE_de", "en-US"])
    fake_pyobjc.events.clear()
    engine.read(image)
    assert ("languages", ["en-US", "de-DE"]) in fake_pyobjc.events
    assert "klingon" in caplog.text

    # nothing supported: do not send a language list at all (Vision's default applies)
    engine = AppleVisionOcr(["klingon"])
    fake_pyobjc.events.clear()
    engine.read(image)
    assert not [e for e in fake_pyobjc.events if isinstance(e, tuple) and e[0] == "languages"]

    # macOS without the listing call: configured codes are passed through as written
    fake_pyobjc.has_language_listing = False
    engine = AppleVisionOcr(["fr-FR"])
    fake_pyobjc.events.clear()
    engine.read(image)
    assert ("languages", ["fr-FR"]) in fake_pyobjc.events


def test_match_languages_pure():
    supported = ["en-US", "fr-FR", "zh-Hans", "zh-Hant"]
    assert match_languages(["EN-us", "zh", "fr_FR", "en-US"], supported) == ["en-US", "zh-Hans", "fr-FR"]
    assert match_languages([" ", "en-GB"], supported) == ["en-US"]
    assert match_languages(["xx"], supported) == []
    assert match_languages(["en-US", "xx"], None) == ["en-US", "xx"]


def test_apple_vision_without_pyobjc_says_what_to_install(monkeypatch):
    for name in ("objc", "Vision", "Foundation"):
        monkeypatch.setitem(sys.modules, name, None)  # makes `import name` raise ImportError
    with pytest.raises(BackendUnavailable, match="pip install pyobjc-framework-Vision"):
        AppleVisionOcr(["en-US"])


def test_apple_vision_on_a_macos_without_text_recognition(fake_pyobjc):
    del sys.modules["Vision"].VNRecognizeTextRequest
    with pytest.raises(BackendUnavailable, match="rapidocr"):
        AppleVisionOcr(["en-US"])


# ---------------------------------------------------------------------------
# RapidOCR result conversion (no model needed)
# ---------------------------------------------------------------------------


def _quad(x0, y0, x1, y1):
    return [[x0, y0], [x1, y0], [x1, y1], [x0, y1]]


def test_rapidocr_result_conversion_normalises_and_orders():
    raw = SimpleNamespace(
        txts=("second line", "first line", "  "),
        scores=(0.91, 0.99, 0.5),
        boxes=[_quad(20, 60, 180, 80), _quad(20, 10, 120, 30), _quad(0, 90, 5, 95)],
        img=SimpleNamespace(shape=(100, 200, 3)),
    )
    result = rapidocr_result(raw)
    assert [ln.text for ln in result.lines] == ["first line", "second line"]
    assert result.lines[0].box == pytest.approx((0.10, 0.10, 0.50, 0.20))
    assert result.lines[1].box == pytest.approx((0.10, 0.60, 0.80, 0.20))
    assert [ln.confidence for ln in result.lines] == [0.99, 0.91]


def test_rapidocr_result_empty_and_degenerate_shapes():
    assert rapidocr_result(SimpleNamespace(txts=None, scores=None, boxes=None, img=None)).lines == []
    assert rapidocr_result(SimpleNamespace(txts=(), scores=(), boxes=None)).lines == []
    assert rapidocr_result(object()).lines == []
    # no image size: order still follows the boxes, but no (wrongly scaled) boxes are handed out
    quads = [_quad(0, 50, 10, 60), _quad(0, 5, 10, 15)]
    raw = SimpleNamespace(txts=("b", "a"), scores=(0.9, 0.8), boxes=quads, img=None)
    result = rapidocr_result(raw)
    assert [(ln.text, ln.box) for ln in result.lines] == [("a", None), ("b", None)]
    # no boxes at all: engine order, default confidence handling
    raw = SimpleNamespace(txts=("x y", "z w"), scores=None, boxes=None, img=None)
    converted = [(ln.text, ln.confidence, ln.box) for ln in rapidocr_result(raw).lines]
    assert converted == [("x y", 1.0, None), ("z w", 1.0, None)]


# ---------------------------------------------------------------------------
# factory and status rules (engines stubbed: no model is loaded)
# ---------------------------------------------------------------------------


class _StubEngine:
    def __init__(self, *args, **kwargs):
        self.args = args

    def read(self, image_path):
        return OcrResult()

    def close(self):
        pass


@pytest.fixture()
def stub_engines(monkeypatch):
    """Replace both engine classes and the availability probes so factory rules can be tested anywhere."""
    state = SimpleNamespace(macos=False, modules={"rapidocr", "onnxruntime"})

    class StubVision(_StubEngine):
        name = "apple-vision"

    class StubRapid(_StubEngine):
        name = "rapidocr"

    monkeypatch.setattr(ocr_mod, "AppleVisionOcr", StubVision)
    monkeypatch.setattr(ocr_mod, "RapidOcrEngine", StubRapid)
    monkeypatch.setattr(ocr_mod, "is_macos", lambda: state.macos)
    monkeypatch.setattr(ocr_mod, "is_apple_silicon", lambda: state.macos)
    monkeypatch.setattr(ocr_mod, "module_available", lambda name: name in state.modules)
    return state


def test_factory_none_and_unknown(tmp_path, stub_engines):
    assert make_ocr(_settings(tmp_path, "none")) is None
    assert make_ocr(_settings(tmp_path, " None ")) is None
    with pytest.raises(BackendUnavailable, match="auto, apple-vision, rapidocr, none"):
        make_ocr(_settings(tmp_path, "tesseract"))


def test_factory_auto_off_macos_prefers_rapidocr_then_none(tmp_path, stub_engines):
    stub_engines.modules = {"rapidocr", "onnxruntime", "Vision", "objc"}  # pyobjc present but not a Mac
    assert make_ocr(_settings(tmp_path, "auto")).name == "rapidocr"
    stub_engines.modules = set()
    assert make_ocr(_settings(tmp_path, "auto")) is None


def test_factory_auto_on_macos(tmp_path, stub_engines):
    stub_engines.macos = True
    stub_engines.modules = {"Vision", "objc", "rapidocr", "onnxruntime"}
    engine = make_ocr(_settings(tmp_path, "auto"))
    assert engine.name == "apple-vision" and engine.args == (["en-US"],)  # languages from settings
    stub_engines.modules = {"rapidocr", "onnxruntime"}  # no pyobjc Vision bindings
    assert make_ocr(_settings(tmp_path, "auto")).name == "rapidocr"
    stub_engines.modules = set()
    assert make_ocr(_settings(tmp_path, "auto")) is None


def test_factory_auto_falls_through_when_an_engine_cannot_start(tmp_path, stub_engines, monkeypatch, caplog):
    stub_engines.macos = True
    stub_engines.modules = {"Vision", "objc", "rapidocr", "onnxruntime"}

    def broken(*args, **kwargs):
        raise BackendUnavailable("Vision exploded")

    monkeypatch.setattr(ocr_mod, "AppleVisionOcr", broken)
    assert make_ocr(_settings(tmp_path, "auto")).name == "rapidocr"
    assert "Vision exploded" in caplog.text
    monkeypatch.setattr(ocr_mod, "RapidOcrEngine", broken)
    assert make_ocr(_settings(tmp_path, "auto")) is None


def test_factory_explicit_backend_is_used_or_raises(tmp_path, stub_engines):
    with pytest.raises(BackendUnavailable, match="only exists on macOS"):
        make_ocr(_settings(tmp_path, "apple-vision"))
    stub_engines.macos = True
    stub_engines.modules = {"rapidocr", "onnxruntime"}
    with pytest.raises(BackendUnavailable, match="pip install pyobjc-framework-Vision"):
        make_ocr(_settings(tmp_path, "apple_vision"))  # underscore spelling is accepted
    stub_engines.modules = {"Vision", "objc"}
    assert make_ocr(_settings(tmp_path, "Apple-Vision")).name == "apple-vision"
    with pytest.raises(BackendUnavailable):
        make_ocr(_settings(tmp_path, "rapidocr"))
    stub_engines.modules = {"rapidocr", "onnxruntime"}
    assert make_ocr(_settings(tmp_path, "rapidocr")).name == "rapidocr"


def test_rapidocr_install_hints(monkeypatch):
    present: set[str] = set()
    monkeypatch.setattr(ocr_mod, "module_available", lambda name: name in present)
    monkeypatch.setattr(ocr_mod, "is_macos", lambda: False)
    assert "pip install rapidocr onnxruntime" in ocr_mod._rapidocr_problem()
    present.add("rapidocr")
    assert "pip install onnxruntime" in ocr_mod._rapidocr_problem()
    # Intel Macs: the last onnxruntime with wheels for them is 1.23.2
    monkeypatch.setattr(ocr_mod, "is_macos", lambda: True)
    monkeypatch.setattr(ocr_mod, "is_apple_silicon", lambda: False)
    assert "onnxruntime<=1.23.2" in ocr_mod._rapidocr_problem()
    present.clear()
    assert "onnxruntime<=1.23.2" in ocr_mod._rapidocr_problem()


def test_status_rules(tmp_path, stub_engines):
    def status(backend):
        return {s.name: s for s in ocr_status(_settings(tmp_path, backend))}

    st = status("auto")
    assert list(st) == ["apple-vision", "rapidocr"]
    assert not st["apple-vision"].available and "macOS" in st["apple-vision"].detail and not st["apple-vision"].selected
    assert st["rapidocr"].available and st["rapidocr"].selected and "offline" in st["rapidocr"].detail

    stub_engines.macos = True
    stub_engines.modules = {"Vision", "objc", "rapidocr", "onnxruntime"}
    st = status("auto")
    assert st["apple-vision"].selected and "en-US" in st["apple-vision"].detail and not st["rapidocr"].selected
    st = status("rapidocr")
    assert st["rapidocr"].selected and st["apple-vision"].available and not st["apple-vision"].selected

    stub_engines.modules = {"rapidocr", "onnxruntime"}
    st = status("apple-vision")  # explicitly chosen but not installed: nothing is selected, the fix is shown
    assert not any(s.selected for s in st.values())
    assert "pip install pyobjc-framework-Vision" in st["apple-vision"].detail
    assert not any(s.selected for s in status("none").values())
    assert not any(s.selected for s in status("bogus").values())


def test_status_on_this_machine_is_cheap_and_consistent(tmp_path):
    statuses = ocr_status(_settings(tmp_path))
    assert [s.name for s in statuses] == ["apple-vision", "rapidocr"]
    assert all(s.detail for s in statuses)
    assert sum(s.selected for s in statuses) <= 1
    if sys.platform != "darwin":
        assert not statuses[0].available


# ---------------------------------------------------------------------------
# RapidOCR for real (bundled ONNX models, no network)
# ---------------------------------------------------------------------------


def _rapidocr_ready() -> bool:
    return all(importlib.util.find_spec(name) is not None for name in ("rapidocr", "onnxruntime"))


needs_rapidocr = pytest.mark.skipif(not _rapidocr_ready(), reason="rapidocr + onnxruntime not installed")


@pytest.fixture(scope="module")
def rapid_engine(tmp_path_factory):
    if not _rapidocr_ready():
        pytest.skip("rapidocr + onnxruntime not installed")
    settings = Settings(home=tmp_path_factory.mktemp("ocr-home"))
    settings.ocr.backend = "rapidocr"
    engine = make_ocr(settings)
    assert engine is not None and engine.name == "rapidocr" and isinstance(engine, OcrEngine)
    yield engine
    engine.close()


@pytest.fixture(scope="module")
def text_images(tmp_path_factory):
    if not (ff.have_ffmpeg() and ff.has_filter("drawtext")):
        pytest.skip("ffmpeg with the drawtext filter is needed to render test images")
    out = tmp_path_factory.mktemp("ocr-images")
    whiteboard = render_text_image(
        out / "whiteboard.jpg",
        [("Launch plan Q3", 80, 80), ("Ship Falcon beta by June 14", 80, 160), ("Action: call vendor", 80, 240)],
    )
    # white on dark, two columns whose rows do not line up exactly (the right column is drawn a few
    # pixels lower in row 1 and higher in row 2), as on a real door sign or timetable
    sign = render_text_image(
        out / "sign.jpg",
        [("Name", 80, 100), ("Room", 520, 106), ("Alice", 80, 226), ("4B North", 520, 220), ("Bob", 80, 340),
         ("7C South", 520, 346)],  # fmt: skip
        background="0x1E3A5F",
        color="white",
    )
    blank = render_text_image(out / "blank.jpg", [])
    return SimpleNamespace(whiteboard=whiteboard, sign=sign, blank=blank, dir=out)


@pytest.mark.slow
def test_rapidocr_reads_multiline_text_in_order(rapid_engine, text_images):
    result = rapid_engine.read(text_images.whiteboard)
    assert [_norm(ln.text) for ln in result.lines] == [
        "launch plan q3", "ship falcon beta by june 14", "action: call vendor",
    ]  # fmt: skip
    assert all(ln.confidence > 0.6 for ln in result.lines)
    boxes = [ln.box for ln in result.lines]
    assert all(b is not None and all(0.0 <= v <= 1.0 for v in b) for b in boxes)
    # top-left origin, normalised: the first line was drawn at x=80/960, y=80/540
    assert boxes[0][0] == pytest.approx(80 / 960, abs=0.03) and boxes[0][1] == pytest.approx(80 / 540, abs=0.05)
    assert boxes[0][1] < boxes[1][1] < boxes[2][1]
    assert boxes[1][2] > boxes[0][2]  # the longer line has the wider box
    text = clean_ocr_text(result, min_confidence=0.35, min_chars=3)
    assert _norm(text.splitlines()[0]) == "launch plan q3" and len(text.splitlines()) == 3


@pytest.mark.slow
def test_rapidocr_white_on_dark_two_columns_in_reading_order(rapid_engine, text_images):
    result = rapid_engine.read(text_images.sign)
    assert [_norm(ln.text) for ln in result.lines] == ["name", "room", "alice", "4b north", "bob", "7c south"]
    left, right = result.lines[0].box, result.lines[1].box
    assert left[0] < 0.2 < 0.5 < right[0]  # two columns really are side by side


@pytest.mark.slow
def test_rapidocr_blank_image_gives_empty_result(rapid_engine, text_images, capfd):
    result = rapid_engine.read(text_images.blank)
    assert result.lines == [] and result.text == ""
    assert clean_ocr_text(result, min_confidence=0.35, min_chars=3) == ""
    captured = capfd.readouterr()
    assert "RapidOCR" not in captured.err and "RapidOCR" not in captured.out  # its INFO/WARNING chatter is silenced


@needs_rapidocr
def test_rapidocr_missing_and_corrupt_files_raise_backend_error(rapid_engine, tmp_path):
    with pytest.raises(BackendError, match="not found"):
        rapid_engine.read(tmp_path / "missing.jpg")
    with pytest.raises(BackendError, match="not found"):
        rapid_engine.read(tmp_path)  # a directory is not an image
    corrupt = tmp_path / "corrupt.jpg"
    corrupt.write_bytes(b"\xff\xd8\xff\xe0 this is not a jpeg")
    with pytest.raises(BackendError, match="corrupt.jpg"):
        rapid_engine.read(corrupt)
    empty = tmp_path / "empty.jpg"
    empty.write_bytes(b"")
    with pytest.raises(BackendError, match="empty.jpg"):
        rapid_engine.read(empty)
    text_file = tmp_path / "notes.txt"
    text_file.write_text("hello")
    with pytest.raises(BackendError):
        rapid_engine.read(text_file)


@needs_rapidocr
def test_rapidocr_never_downloads_models(monkeypatch):
    """A missing/invalid bundled model must become BackendUnavailable with instructions, not a download."""
    from rapidocr.utils.download_file import DownloadFile

    original = vars(DownloadFile)["_make_http_request"]
    monkeypatch.setattr(DownloadFile, "_should_skip_download", classmethod(lambda cls, *a, **k: False))
    with pytest.raises(BackendUnavailable) as err:
        ocr_mod.RapidOcrEngine()
    message = str(err.value)
    assert "pip install --force-reinstall rapidocr" in message and ".onnx" in message
    assert "never downloads" in message
    assert vars(DownloadFile)["_make_http_request"] is original  # the guard is removed again


@needs_rapidocr
def test_rapidocr_download_attempt_at_read_time_is_reported(rapid_engine, tmp_path, monkeypatch):
    """Even if a download were attempted while reading a frame, it is refused and explained."""
    from rapidocr.utils.download_file import DownloadFile

    image = tmp_path / "x.jpg"
    image.write_bytes(b"\xff\xd8")

    def sneaky(path):
        DownloadFile._make_http_request("https://example.invalid/models/extra_model.onnx", None)

    monkeypatch.setattr(rapid_engine, "_engine", sneaky)
    with pytest.raises(BackendUnavailable, match="extra_model.onnx"):
        rapid_engine.read(image)


@needs_rapidocr
def test_rapidocr_closed_engine(tmp_path):
    engine = ocr_mod.RapidOcrEngine.__new__(ocr_mod.RapidOcrEngine)
    engine._engine = object()
    engine.close()
    engine.close()  # idempotent
    with pytest.raises(BackendError, match="closed"):
        engine.read(tmp_path / "x.jpg")
