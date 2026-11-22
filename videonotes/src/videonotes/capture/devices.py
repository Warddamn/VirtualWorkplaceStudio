"""Capture devices as ffmpeg's ``avfoundation`` input sees them (macOS).

Everything that touches the operating system is in :func:`list_devices`; the rest are
pure functions over text and lists so they can be tested anywhere.

Facts this module relies on were read in ``libavdevice/avfoundation.m`` (FFmpeg n6.1 to
n9.1; the file is identical between n8.0 and n9.0):

* ``ffmpeg -f avfoundation -list_devices true -i ""`` prints the list on stderr at log
  level *info* and then always fails ("Input/output error"), so the exit status says
  nothing.
* Two sections, ``AVFoundation video devices:`` and ``AVFoundation audio devices:``
  (hard-coded English), each followed by ``[<index>] <localised device name>``.  From
  FFmpeg 9.1 an entry also carries ``  [uid:...]`` and, for USB devices, `` [serial:...]``.
* Screens are listed among the video devices as ``Capture screen N``.
* Indices are positions in the enumeration *at that moment*; they change when a device is
  plugged in or removed.  Resolve a name to an index immediately before every launch.
* ffmpeg's own selection by name is a case-sensitive *prefix* match that breaks on names
  containing ``:`` or starting with a digit, which is why :func:`pick_device` does the
  matching here and callers pass the index.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass

from ..config import DJI_DEVICE_HINTS, is_macos
from ..media import ffmpeg as ff

log = logging.getLogger("videonotes.capture.devices")

#: ``CaptureDevice.index`` of the pseudo device that stands for "whatever input the Mac
#: currently uses" (ffmpeg's ``default`` audio device, chosen in System Settings → Sound).
DEFAULT_AUDIO_INDEX = -1
DEFAULT_AUDIO_NAME = "this Mac's default input (System Settings → Sound → Input)"

#: Name DJI's own instructions give for the camera in webcam mode when it does not
#: identify itself; tried by ``auto`` after :data:`~videonotes.config.DJI_DEVICE_HINTS`.
GENERIC_CAMERA_HINTS = ("uvc camera",)

LIST_TIMEOUT_S = 20.0


@dataclass
class CaptureDevice:
    """One avfoundation capture device. ``kind`` is ``"video"`` or ``"audio"``."""

    index: int
    name: str
    kind: str

    @property
    def is_default(self) -> bool:
        """True for the pseudo device meaning "the Mac's default audio input"."""
        return self.kind == "audio" and self.index == DEFAULT_AUDIO_INDEX


# av_log prefix: "[AVFoundation indev @ 0x12f605e60] ", "[avfoundation @ 0x7f8] ", "[in#0 @ 0x6000] ".
# It can never swallow an entry such as "[0] Name": it needs "@ 0x…" inside the first bracket pair.
_LOG_PREFIX = re.compile(r"^\[[^\]\n]*@\s*0x[0-9a-fA-F]+\]\s?")
_LEVEL_PREFIX = re.compile(r"^\[(?:quiet|panic|fatal|error|warning|info|verbose|debug|trace)\]\s?")
_SECTION = re.compile(r"AVFoundation (video|audio) devices:", re.IGNORECASE)
_ENTRY = re.compile(r"^\[(\d+)\]\s(.*)$")
_ID_SUFFIX = re.compile(r"\s+\[uid:[^\]]*\](?:\s+\[serial:[^\]]*\])?\s*$")
_SCREEN = re.compile(r"^Capture screen \d+$")


def _strip_log_prefix(line: str) -> str:
    line = _LOG_PREFIX.sub("", line.rstrip("\r\n"), count=1)
    return _LEVEL_PREFIX.sub("", line, count=1)


def parse_avfoundation_devices(stderr_text: str) -> list[CaptureDevice]:
    """Parse the stderr of ``ffmpeg -f avfoundation -list_devices true -i ""``.

    Accepts both listing formats (with and without the ``[uid:…] [serial:…]`` suffix),
    with or without ffmpeg's ``[… @ 0x…]`` log prefix, and device names in any language
    or containing brackets and colons.  ``Capture screen N`` pseudo devices are left out:
    a screen is never the camera.  Indices are returned exactly as ffmpeg printed them.
    """
    devices: list[CaptureDevice] = []
    seen: set[tuple[str, int]] = set()
    kind: str | None = None
    for raw in stderr_text.splitlines():
        line = _strip_log_prefix(raw)
        section = _SECTION.search(line)
        if section:
            kind = section.group(1).lower()
            continue
        if kind is None:
            continue
        entry = _ENTRY.match(line)
        if not entry:
            continue
        index = int(entry.group(1))
        name = _ID_SUFFIX.sub("", entry.group(2)).strip()
        if not name or (kind, index) in seen:
            continue
        if kind == "video" and _SCREEN.match(name):
            continue
        seen.add((kind, index))
        devices.append(CaptureDevice(index=index, name=name, kind=kind))
    return devices


def list_devices() -> list[CaptureDevice]:
    """Cameras and microphones ffmpeg can capture from.

    macOS only: returns ``[]`` on any other system, and when this ffmpeg was built
    without the avfoundation input (a warning says how to get one that has it).
    Raises :class:`~videonotes.media.ffmpeg.FFmpegError` (with install instructions) when
    there is no ffmpeg at all.
    """
    if not is_macos():
        return []
    ff.ffmpeg_bin()  # raises FFmpegError with the install hint when ffmpeg is missing
    if not ff.has_input_format("avfoundation"):
        log.warning(
            "this ffmpeg (%s) cannot capture from cameras: it has no avfoundation input. "
            "Install the Homebrew build:  brew install ffmpeg",
            ff.ffmpeg_bin(),
        )
        return []
    try:
        # The listing is logged at level "info"; the command "fails" by design, so no check.
        proc = ff.run(
            ["-f", "avfoundation", "-list_devices", "true", "-i", ""],
            check=False,
            loglevel="info",
            timeout=LIST_TIMEOUT_S,
        )
    except ff.FFmpegError as exc:
        log.warning("could not list capture devices: %s", exc)
        return []
    devices = parse_avfoundation_devices(proc.stderr)
    log.debug("capture devices: %s", devices)
    return devices


def is_dji_device(name: str) -> bool:
    """True if a device name looks like a DJI camera (see ``config.DJI_DEVICE_HINTS``)."""
    lowered = name.casefold()
    return any(hint in lowered for hint in DJI_DEVICE_HINTS)


def _first(pool: list[CaptureDevice], hints: tuple[str, ...]) -> CaptureDevice | None:
    for device in pool:
        lowered = device.name.casefold()
        if any(hint in lowered for hint in hints):
            return device
    return None


def default_audio_device() -> CaptureDevice:
    """The pseudo device for "the Mac's default input" (``index == DEFAULT_AUDIO_INDEX``)."""
    return CaptureDevice(index=DEFAULT_AUDIO_INDEX, name=DEFAULT_AUDIO_NAME, kind="audio")


def pick_device(devices: list[CaptureDevice], kind: str, wanted: str) -> CaptureDevice | None:
    """Resolve a ``capture.video_device`` / ``capture.audio_device`` setting to a device.

    ``wanted`` is matched case-insensitively:

    * ``"auto"`` (or empty) — the first device whose name contains one of
      ``config.DJI_DEVICE_HINTS`` (then, for video, the generic ``UVC Camera`` name DJI
      documents).  For audio that is the camera's own USB microphone; when the camera
      exposes none (an Osmo Action 5 Pro does so only from firmware 01.01.05.20) the Mac's
      default input is used instead and a warning says so.
    * audio only: ``"default"`` — the Mac's default input; ``"none"`` — no audio.
    * a number — the device with that avfoundation index.
    * anything else — a device whose name equals it, else the first whose name contains it.

    Returns ``None`` when nothing matches (for audio: record video only).  The Mac's
    default input is returned as a pseudo device with ``index == DEFAULT_AUDIO_INDEX``;
    :func:`videonotes.capture.live.webcam_command` understands it.
    """
    if kind not in ("video", "audio"):
        raise ValueError(f"kind must be 'video' or 'audio', got {kind!r}")
    pool = [d for d in devices if d.kind == kind and d.index >= 0]
    want = (wanted or "auto").strip()
    key = want.casefold()

    if kind == "audio":
        if key == "none":
            log.info("audio: none requested, recording video only")
            return None
        if key == "default":
            if not pool:
                log.warning("audio: this Mac has no audio input device; recording video only")
                return None
            log.info("audio: using the Mac's default input device")
            return default_audio_device()

    if key == "auto":
        found = _first(pool, DJI_DEVICE_HINTS)
        if kind == "video":
            if found is None:
                found = _first(pool, GENERIC_CAMERA_HINTS)
                if found is not None:
                    log.info("video: no device is named like a DJI camera; using %r", found.name)
            return found
        if found is not None:
            log.info("audio: using the camera's own USB microphone %r", found.name)
            return found
        if not pool:
            log.warning("audio: no microphone found; recording video only")
            return None
        log.warning(
            "audio: the camera exposes no USB microphone, so the Mac's default input is used. It only hears "
            "what is near the Mac. (An Osmo Action 5 Pro sends its microphone over USB from firmware "
            "01.01.05.20 on; update the camera to get its own audio.)"
        )
        return default_audio_device()

    if key.isdigit():
        index = int(key)
        for device in pool:
            if device.index == index:
                return device
        return None

    for device in pool:
        if device.name.casefold() == key:
            return device
    for device in pool:
        if key in device.name.casefold():
            return device
    return None


# -- capture modes ---------------------------------------------------------------
#
# avfoundation only opens a device when -video_size equals one of the device's formats
# and -framerate is within 0.01 fps of that format's maximum rate.  Otherwise it logs
#     Selected video size (1280x720) is not supported by the device.     (or "framerate")
#     Supported modes:
#       1920x1080@[30.000030 30.000030]fps
# and fails.  These helpers turn that list into a mode that will be accepted.


@dataclass(frozen=True)
class CaptureMode:
    """One ``WxH@[min max]fps`` line of avfoundation's "Supported modes" list."""

    width: int
    height: int
    min_fps: float
    max_fps: float


_MODE = re.compile(r"(\d{2,5})x(\d{2,5})@\[\s*([\d.]+)\s+([\d.]+)\s*\]fps")


def parse_supported_modes(stderr_text: str) -> list[CaptureMode]:
    """Modes listed after ``Supported modes:`` in ffmpeg's stderr (duplicates removed)."""
    modes: list[CaptureMode] = []
    for raw in stderr_text.splitlines():
        match = _MODE.search(_strip_log_prefix(raw))
        if not match:
            continue
        try:
            mode = CaptureMode(int(match[1]), int(match[2]), float(match[3]), float(match[4]))
        except ValueError:
            continue
        if mode.width > 0 and mode.height > 0 and mode.max_fps > 0 and mode not in modes:
            modes.append(mode)
    return modes


def choose_mode(modes: list[CaptureMode], width: int, height: int, fps: float) -> CaptureMode | None:
    """The supported mode closest to what was asked for.

    Preference order: the requested frame rate (else the nearest higher one, else the
    nearest lower one), then the requested size (else the smallest larger size with the
    same aspect ratio, else the nearest by pixel count).  A larger capture is scaled down
    afterwards; a smaller one is never scaled up.
    """
    if not modes:
        return None
    want_pixels = width * height
    want_aspect = width / height if height else 0.0

    def score(mode: CaptureMode) -> tuple[float, ...]:
        fps_diff = mode.max_fps - fps
        if abs(fps_diff) < 0.5:
            fps_rank, fps_dist = 0, abs(fps_diff)
        elif fps_diff > 0:
            fps_rank, fps_dist = 1, fps_diff
        else:
            fps_rank, fps_dist = 2, -fps_diff
        pixels = mode.width * mode.height
        same_aspect = abs(mode.width / mode.height - want_aspect) < 0.02
        if mode.width == width and mode.height == height:
            size_rank = 0
        elif pixels >= want_pixels and same_aspect:
            size_rank = 1
        elif pixels >= want_pixels:
            size_rank = 2
        else:
            size_rank = 3
        # Rates within half a frame of the request are equally good; otherwise nearer is better.
        return (fps_rank, 0.0 if fps_rank == 0 else round(fps_dist, 1), size_rank, abs(pixels - want_pixels), fps_dist)

    return min(modes, key=score)


def fps_arg(fps: float) -> str:
    """Render a frame rate for ``-framerate`` so it lands within avfoundation's 0.01 fps tolerance."""
    for num, den in ((30000, 1001), (60000, 1001), (24000, 1001), (15000, 1001), (120000, 1001)):
        if abs(fps - num / den) < 0.005:
            return f"{num}/{den}"
    if abs(fps - round(fps)) < 0.005:
        return str(int(round(fps)))
    return f"{fps:.3f}".rstrip("0").rstrip(".")
