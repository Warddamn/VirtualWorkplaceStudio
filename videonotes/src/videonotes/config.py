"""Settings and on-disk layout.

Everything videonotes owns lives under one *home* directory (default
``~/VideoNotes``, override with the ``VIDEONOTES_HOME`` environment variable or
``--home``)::

    ~/VideoNotes/
        config.toml        user settings (every key optional)
        library.db         SQLite library (see videonotes.store)
        media/<session>/   analysed media: live segments / imported proxies
        frames/<session>/  keyframe JPEGs
        cache/             scratch (16 kHz WAVs …) — safe to delete
        models/            downloaded model files
        notes/             Markdown notes (an Obsidian-compatible vault)
        logs/

Settings resolve as: built-in defaults  <  config.toml  <  explicit overrides
passed to :func:`load_settings` (CLI flags).
"""

from __future__ import annotations

import dataclasses
import os
import platform
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ENV_HOME = "VIDEONOTES_HOME"
DEFAULT_HOME = "~/VideoNotes"

#: Substrings (case-insensitive) that identify a DJI camera among capture devices.
DJI_DEVICE_HINTS = ("osmo", "dji", "action 4", "action 5", "action4", "action5")


@dataclass
class CaptureSettings:
    """Live capture (USB webcam mode, or RTMP from the camera over Wi-Fi)."""

    video_device: str = "auto"  # "auto" | device-name substring | avfoundation index
    audio_device: str = "auto"  # "auto" | name substring | index | "default" | "none"
    video_size: str = "1280x720"
    framerate: float = 30.0
    segment_seconds: int = 60  # live video is cut into files this long and processed as they close
    video_bitrate: str = "1500k"
    audio_bitrate: str = "64k"
    keep_segments: bool = True  # keep the recorded segments after they were analysed
    rtmp_port: int = 1935
    rtmp_path: str = "live/cam"


@dataclass
class ImportSettings:
    """Importing recordings from the camera's SD card / USB volume."""

    prefer_proxy: bool = True  # analyse DJI's low-res .LRF proxy when one exists
    copy_media: str = "proxy"  # "proxy" | "original" | "none" (analyse in place, keep nothing)
    session_gap_seconds: float = 300.0  # clips closer together than this form one session


@dataclass
class FrameSettings:
    """Sparse keyframe selection."""

    analysis_fps: float = 2.0  # frames per second looked at (tiny grayscale)
    analysis_width: int = 320
    novelty_threshold: float = 0.25  # 0..1, higher = fewer keyframes (0.25 ~ 4 % of the picture changed)
    sharpness_window_s: float = 1.5  # pick the sharpest frame within this window
    min_gap_s: float = 2.0  # never two keyframes closer than this
    max_gap_s: float = 60.0  # always at least one keyframe this often
    max_per_minute: float = 8.0
    jpeg_width: int = 1920  # stored keyframe width (never upscaled); wide enough to read text
    jpeg_quality: int = 3  # ffmpeg -q:v (2 best … 31 worst)


@dataclass
class AsrSettings:
    backend: str = "auto"  # auto | mlx-whisper | parakeet-mlx | faster-whisper | sherpa-onnx | none
    model: str = "auto"
    language: str = "auto"  # "auto" or an ISO code such as "en"
    vad: bool = True  # skip silence before transcription


@dataclass
class OcrSettings:
    backend: str = "auto"  # auto | apple-vision | rapidocr | none
    languages: list[str] = field(default_factory=lambda: ["en-US"])
    min_confidence: float = 0.35
    min_chars: int = 3  # ignore OCR results shorter than this


@dataclass
class VisionSettings:
    """Captioning keyframes with a vision-language model."""

    backend: str = "auto"  # auto | ollama | mlx-vlm | anthropic | none
    model: str = "auto"
    max_per_minute: float = 2.0  # caption budget; the most novel keyframes win
    image_width: int = 768  # frames are downscaled to this before captioning


@dataclass
class LlmSettings:
    """Summarisation / question answering."""

    backend: str = "auto"  # auto | ollama | mlx-lm | anthropic | extractive
    model: str = "auto"
    ollama_url: str = "http://127.0.0.1:11434"
    context_tokens: int = 8192
    keep_alive: str = "30s"  # how long Ollama keeps a model in RAM after a call


@dataclass
class NotesSettings:
    vault: str = ""  # "" = <home>/notes ; point this at an Obsidian vault folder if you like
    embed_images: bool = True
    max_images_per_moment: int = 2
    moment_gap_seconds: float = 120.0  # a pause in speech this long starts a new moment
    moment_min_seconds: float = 30.0
    moment_max_seconds: float = 900.0
    include_transcript: bool = True
    time_format: str = "%H:%M"


@dataclass
class DjiSettings:
    """Bluetooth / Wi-Fi control of the camera."""

    name_filter: str = ""  # only consider BLE devices whose name contains this
    address: str = ""  # remembered CoreBluetooth UUID of the camera (set by `vnote camera pair`)
    model: str = "auto"  # auto | action4 | action5pro
    wifi_ssid: str = ""  # network the camera should join for wireless capture
    stream_resolution: str = "1080p"  # 480p | 720p | 1080p
    stream_bitrate_kbps: int = 4000
    stream_fps: int = 30


@dataclass
class Settings:
    home: Path = field(default_factory=lambda: default_home())
    capture: CaptureSettings = field(default_factory=CaptureSettings)
    imports: ImportSettings = field(default_factory=ImportSettings)
    frames: FrameSettings = field(default_factory=FrameSettings)
    asr: AsrSettings = field(default_factory=AsrSettings)
    ocr: OcrSettings = field(default_factory=OcrSettings)
    vision: VisionSettings = field(default_factory=VisionSettings)
    llm: LlmSettings = field(default_factory=LlmSettings)
    notes: NotesSettings = field(default_factory=NotesSettings)
    dji: DjiSettings = field(default_factory=DjiSettings)

    # -- layout -----------------------------------------------------------

    @property
    def config_path(self) -> Path:
        return self.home / "config.toml"

    @property
    def db_path(self) -> Path:
        return self.home / "library.db"

    @property
    def media_dir(self) -> Path:
        return self.home / "media"

    @property
    def frames_dir(self) -> Path:
        return self.home / "frames"

    @property
    def cache_dir(self) -> Path:
        return self.home / "cache"

    @property
    def models_dir(self) -> Path:
        return self.home / "models"

    @property
    def logs_dir(self) -> Path:
        return self.home / "logs"

    @property
    def vault_dir(self) -> Path:
        return Path(self.notes.vault).expanduser() if self.notes.vault else self.home / "notes"

    def ensure_dirs(self) -> None:
        for d in (self.home, self.media_dir, self.frames_dir, self.cache_dir, self.models_dir,
                  self.logs_dir, self.vault_dir):  # fmt: skip
            d.mkdir(parents=True, exist_ok=True)

    def rel(self, path: str | Path) -> str:
        """Path as stored in the database: relative to home when inside it."""
        p = Path(path).expanduser()
        try:
            return p.resolve().relative_to(self.home.resolve()).as_posix()
        except (ValueError, OSError):
            return str(p)

    def abs(self, stored: str | Path) -> Path:
        """Inverse of :meth:`rel`."""
        p = Path(stored).expanduser()
        return p if p.is_absolute() else self.home / p

    def to_dict(self) -> dict[str, Any]:
        d = dataclasses.asdict(self)
        d["home"] = str(self.home)
        return d


# The TOML section name for each Settings attribute.
_SECTIONS = {
    "capture": "capture",
    "import": "imports",
    "frames": "frames",
    "asr": "asr",
    "ocr": "ocr",
    "vision": "vision",
    "llm": "llm",
    "notes": "notes",
    "dji": "dji",
}


def default_home() -> Path:
    return Path(os.environ.get(ENV_HOME) or DEFAULT_HOME).expanduser()


def _coerce(current: Any, value: Any, where: str) -> Any:
    """Coerce a TOML/CLI value to the type of the default it replaces."""
    if isinstance(current, bool):
        if isinstance(value, bool):
            return value
        if isinstance(value, str) and value.lower() in ("true", "false", "1", "0", "yes", "no"):
            return value.lower() in ("true", "1", "yes")
        raise ValueError(f"{where}: expected true/false, got {value!r}")
    if isinstance(current, int) and not isinstance(current, bool):
        if isinstance(value, bool):
            raise ValueError(f"{where}: expected a number, got {value!r}")
        return int(value)
    if isinstance(current, float):
        if isinstance(value, bool):
            raise ValueError(f"{where}: expected a number, got {value!r}")
        return float(value)
    if isinstance(current, list):
        if isinstance(value, str):
            return [v.strip() for v in value.split(",") if v.strip()]
        return [str(v) for v in value]
    return str(value)


def apply_overrides(settings: Settings, data: dict[str, Any], *, source: str = "config") -> list[str]:
    """Apply ``{"section": {"key": value}}`` onto settings. Returns warnings for unknown keys."""
    warnings: list[str] = []
    for section, values in data.items():
        attr = _SECTIONS.get(section)
        if attr is None:
            warnings.append(f"{source}: unknown section [{section}] ignored")
            continue
        if not isinstance(values, dict):
            warnings.append(f"{source}: [{section}] must be a table; ignored")
            continue
        target = getattr(settings, attr)
        for key, value in values.items():
            if not hasattr(target, key):
                warnings.append(f"{source}: unknown key {section}.{key} ignored")
                continue
            try:
                setattr(target, key, _coerce(getattr(target, key), value, f"{section}.{key}"))
            except (TypeError, ValueError) as exc:
                warnings.append(f"{source}: {exc}; keeping default")
    return warnings


def load_settings(
    home: str | Path | None = None, overrides: dict[str, Any] | None = None
) -> tuple[Settings, list[str]]:
    """Load settings. Returns ``(settings, warnings)``; never raises on a bad config key."""
    settings = Settings(home=Path(home).expanduser() if home else default_home())
    warnings: list[str] = []
    if settings.config_path.is_file():
        try:
            data = tomllib.loads(settings.config_path.read_text(encoding="utf-8"))
        except (tomllib.TOMLDecodeError, OSError) as exc:
            warnings.append(f"{settings.config_path}: could not be read ({exc}); using defaults")
        else:
            warnings += apply_overrides(settings, data, source=str(settings.config_path))
    if overrides:
        warnings += apply_overrides(settings, overrides, source="command line")
    return settings, warnings


def parse_set_overrides(pairs: list[str]) -> dict[str, dict[str, str]]:
    """Parse repeated ``--set section.key=value`` CLI options."""
    out: dict[str, dict[str, str]] = {}
    for pair in pairs:
        if "=" not in pair or "." not in pair.split("=", 1)[0]:
            raise ValueError(f"--set expects section.key=value, got {pair!r}")
        name, value = pair.split("=", 1)
        section, key = name.strip().split(".", 1)
        out.setdefault(section, {})[key] = value.strip()
    return out


# -- platform helpers ----------------------------------------------------------


def is_macos() -> bool:
    return sys.platform == "darwin"


def is_apple_silicon() -> bool:
    return sys.platform == "darwin" and platform.machine() == "arm64"


def default_config_text() -> str:
    """A commented config.toml listing every setting at its default value."""
    s = Settings()
    lines = [
        "# videonotes settings. Every key is optional; delete a line to get the default.",
        "# Run `vnote doctor` to see which backends 'auto' resolves to on this Mac.",
        "",
    ]
    for section, attr in _SECTIONS.items():
        obj = getattr(s, attr)
        doc = (type(obj).__doc__ or "").strip().splitlines()
        if doc and doc[0]:
            lines.append(f"# {doc[0]}")
        lines.append(f"[{section}]")
        for f in dataclasses.fields(obj):
            lines.append(f"{f.name} = {_toml_value(getattr(obj, f.name))}")
        lines.append("")
    return "\n".join(lines)


def _toml_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return repr(value)
    if isinstance(value, list):
        return "[" + ", ".join(_toml_value(v) for v in value) + "]"
    return '"' + str(value).replace("\\", "\\\\").replace('"', '\\"') + '"'
