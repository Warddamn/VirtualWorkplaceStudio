"""Locating and running ffmpeg / ffprobe, and probing media files.

Every component that shells out to ffmpeg goes through this module so there is
one place that knows where the binary is and how failures are reported.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from dataclasses import dataclass, field
from datetime import UTC, datetime
from functools import cache, lru_cache
from pathlib import Path
from typing import Any

ENV_FFMPEG = "VIDEONOTES_FFMPEG"
ENV_FFPROBE = "VIDEONOTES_FFPROBE"

# Homebrew (Apple Silicon, Intel) and MacPorts locations; GUI-launched or
# LaunchAgent processes on macOS often do not have these on PATH.
_EXTRA_DIRS = ("/opt/homebrew/bin", "/usr/local/bin", "/opt/local/bin")

INSTALL_HINT = (
    "ffmpeg was not found. Install it with Homebrew:  brew install ffmpeg\n"
    "(or set VIDEONOTES_FFMPEG to the full path of an ffmpeg binary)."
)


class FFmpegError(RuntimeError):
    """ffmpeg/ffprobe is missing or exited with an error."""

    def __init__(self, message: str, *, returncode: int | None = None, stderr: str = ""):
        super().__init__(message)
        self.returncode = returncode
        self.stderr = stderr


def _find(name: str, env: str) -> str | None:
    explicit = os.environ.get(env)
    if explicit:
        return explicit if Path(explicit).is_file() else None
    found = shutil.which(name)
    if found:
        return found
    for d in _EXTRA_DIRS:
        candidate = Path(d) / name
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return str(candidate)
    return None


@lru_cache(maxsize=1)
def ffmpeg_bin() -> str:
    """Path of the ffmpeg binary. Raises :class:`FFmpegError` with install help if missing."""
    found = _find("ffmpeg", ENV_FFMPEG)
    if found:
        return found
    try:  # optional zero-setup fallback: `pip install imageio-ffmpeg`
        import imageio_ffmpeg  # type: ignore[import-not-found]

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        raise FFmpegError(INSTALL_HINT) from None


@lru_cache(maxsize=1)
def ffprobe_bin() -> str | None:
    """Path of ffprobe, or None (probing then falls back to parsing ``ffmpeg -i``)."""
    found = _find("ffprobe", ENV_FFPROBE)
    if found:
        return found
    try:
        sibling = Path(ffmpeg_bin()).with_name("ffprobe")
    except FFmpegError:
        return None
    return str(sibling) if sibling.is_file() else None


def have_ffmpeg() -> bool:
    try:
        ffmpeg_bin()
        return True
    except FFmpegError:
        return False


def base_cmd(*, loglevel: str = "error") -> list[str]:
    """``ffmpeg`` plus the flags every non-interactive invocation should carry."""
    return [ffmpeg_bin(), "-hide_banner", "-nostdin", "-loglevel", loglevel, "-y"]


def run(
    args: list[str],
    *,
    timeout: float | None = None,
    check: bool = True,
    loglevel: str = "error",
) -> subprocess.CompletedProcess[str]:
    """Run ``ffmpeg <args>`` to completion, capturing output as text.

    ``args`` excludes the binary and the standard flags (see :func:`base_cmd`).
    Raises :class:`FFmpegError` carrying the tail of stderr when ``check`` and
    ffmpeg fails or times out.
    """
    cmd = base_cmd(loglevel=loglevel) + [str(a) for a in args]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, errors="replace", timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        raise FFmpegError(f"ffmpeg timed out after {timeout:.0f}s", stderr=str(exc.stderr or "")) from exc
    if check and proc.returncode != 0:
        tail = "\n".join(proc.stderr.strip().splitlines()[-12:])
        raise FFmpegError(
            f"ffmpeg failed (exit {proc.returncode}):\n{tail}", returncode=proc.returncode, stderr=proc.stderr
        )
    return proc


@lru_cache(maxsize=1)
def version() -> str:
    try:
        out = subprocess.run([ffmpeg_bin(), "-version"], capture_output=True, text=True, timeout=20).stdout
    except (OSError, subprocess.SubprocessError, FFmpegError):
        return ""
    return out.splitlines()[0] if out else ""


@cache
def _listing(flag: str) -> str:
    try:
        return subprocess.run(
            [ffmpeg_bin(), "-hide_banner", flag], capture_output=True, text=True, timeout=30
        ).stdout
    except (OSError, subprocess.SubprocessError, FFmpegError):
        return ""


def has_encoder(name: str) -> bool:
    return bool(re.search(rf"^\s*[VAS][\w.]+\s+{re.escape(name)}\s", _listing("-encoders"), re.M))


def has_filter(name: str) -> bool:
    return bool(re.search(rf"^\s*[T.][S.][C.]?\s+{re.escape(name)}\s", _listing("-filters"), re.M))


def has_hwaccel(name: str) -> bool:
    return name in _listing("-hwaccels").split()


def has_input_format(name: str) -> bool:
    """True if this ffmpeg build has the given demuxer/input device (e.g. 'avfoundation')."""
    return bool(re.search(rf"^\s*D[ E ]?\s+{re.escape(name)}\b", _listing("-devices") + _listing("-formats"), re.M))


# -- probing -------------------------------------------------------------------


@dataclass
class MediaInfo:
    path: Path
    duration: float = 0.0
    has_video: bool = False
    has_audio: bool = False
    width: int | None = None
    height: int | None = None
    fps: float | None = None
    video_codec: str | None = None
    audio_codec: str | None = None
    rotation: int = 0
    #: container/stream ``creation_time`` as epoch seconds (UTC), if present
    creation_ts: float | None = None
    raw: dict[str, Any] = field(default_factory=dict, repr=False)


def _ratio(value: str | None) -> float | None:
    if not value or value in ("0/0", "N/A"):
        return None
    try:
        if "/" in value:
            num, den = value.split("/", 1)
            return float(num) / float(den) if float(den) else None
        return float(value)
    except ValueError:
        return None


def parse_creation_time(value: str | None) -> float | None:
    """Parse an ffprobe ``creation_time`` tag (ISO 8601, usually UTC 'Z') to epoch seconds."""
    if not value:
        return None
    text = value.strip().replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    ts = dt.timestamp()
    return ts if ts > 86400 * 365 else None  # cameras with an unset clock report ~1970/1904


def probe(path: str | Path, *, timeout: float = 60.0) -> MediaInfo:
    """Read duration / streams / creation time of a media file."""
    p = Path(path)
    if not p.is_file():
        raise FFmpegError(f"no such media file: {p}")
    probe_bin = ffprobe_bin()
    if probe_bin is None:
        return _probe_with_ffmpeg(p, timeout=timeout)
    cmd = [probe_bin, "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(p)]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, errors="replace", timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        raise FFmpegError(f"ffprobe timed out on {p}") from exc
    if proc.returncode != 0:
        tail = "\n".join(proc.stderr.strip().splitlines()[-6:])
        raise FFmpegError(f"ffprobe could not read {p}:\n{tail}", returncode=proc.returncode, stderr=proc.stderr)
    try:
        data = json.loads(proc.stdout or "{}")
    except json.JSONDecodeError as exc:
        raise FFmpegError(f"ffprobe returned unreadable output for {p}") from exc

    info = MediaInfo(path=p, raw=data)
    fmt = data.get("format") or {}
    try:
        info.duration = float(fmt.get("duration") or 0.0)
    except ValueError:
        info.duration = 0.0
    creation = (fmt.get("tags") or {}).get("creation_time")
    for stream in data.get("streams") or []:
        kind = stream.get("codec_type")
        tags = stream.get("tags") or {}
        if kind == "video" and not info.has_video:
            if (stream.get("disposition") or {}).get("attached_pic"):
                continue  # cover art, not a video track
            info.has_video = True
            info.width = stream.get("width")
            info.height = stream.get("height")
            info.video_codec = stream.get("codec_name")
            info.fps = _ratio(stream.get("avg_frame_rate")) or _ratio(stream.get("r_frame_rate"))
            creation = creation or tags.get("creation_time")
            rotate = tags.get("rotate")
            for side in stream.get("side_data_list") or []:
                if "rotation" in side:
                    rotate = side["rotation"]
            try:
                info.rotation = int(float(rotate)) % 360 if rotate is not None else 0
            except (TypeError, ValueError):
                info.rotation = 0
            if not info.duration:
                try:
                    info.duration = float(stream.get("duration") or 0.0)
                except ValueError:
                    pass
        elif kind == "audio" and not info.has_audio:
            info.has_audio = True
            info.audio_codec = stream.get("codec_name")
            creation = creation or tags.get("creation_time")
    info.creation_ts = parse_creation_time(creation)
    return info


_DURATION_RE = re.compile(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)")
_VIDEO_RE = re.compile(r"Stream #\S+.*?: Video: (\w+).*?, (\d{2,5})x(\d{2,5})")
_FPS_RE = re.compile(r"(\d+(?:\.\d+)?) fps")
_AUDIO_RE = re.compile(r"Stream #\S+.*?: Audio: (\w+)")
_CREATION_RE = re.compile(r"creation_time\s*:\s*(\S+)")


def _probe_with_ffmpeg(p: Path, *, timeout: float) -> MediaInfo:
    """Fallback when ffprobe is unavailable: parse the banner of ``ffmpeg -i``."""
    try:
        proc = subprocess.run(
            [ffmpeg_bin(), "-hide_banner", "-nostdin", "-i", str(p)],
            capture_output=True, text=True, errors="replace", timeout=timeout,
        )  # fmt: skip
    except subprocess.TimeoutExpired as exc:
        raise FFmpegError(f"ffmpeg timed out probing {p}") from exc
    text = proc.stderr
    info = MediaInfo(path=p, raw={"banner": text})
    if m := _DURATION_RE.search(text):
        info.duration = int(m[1]) * 3600 + int(m[2]) * 60 + float(m[3])
    for line in text.splitlines():
        if not info.has_video and (m := _VIDEO_RE.search(line)) and "attached pic" not in line:
            info.has_video = True
            info.video_codec, info.width, info.height = m[1], int(m[2]), int(m[3])
            if f := _FPS_RE.search(line):
                info.fps = float(f[1])
        elif not info.has_audio and (m := _AUDIO_RE.search(line)):
            info.has_audio = True
            info.audio_codec = m[1]
    if m := _CREATION_RE.search(text):
        info.creation_ts = parse_creation_time(m[1])
    if not (info.has_video or info.has_audio):
        raise FFmpegError(f"could not read {p} as a media file")
    return info
