"""Live capture: ffmpeg command builders and the recorder that supervises ffmpeg.

Two ways in, one mechanism.  ``webcam_command`` (camera in USB webcam mode, through
macOS's avfoundation) and ``rtmp_listen_command`` (camera pushing RTMP over Wi-Fi) both
make ffmpeg cut the stream into fixed-length files; :class:`SegmentRecorder` runs that
ffmpeg and hands out each file once it is complete.

Design decisions (why the flags are what they are)
---------------------------------------------------

**Container: MPEG-TS, written through** ``-f stream_segment`` **with**
``-segment_format_options flush_packets=1``.  A recording must survive an abrupt end:
cable pulled, lid closed, crash, power loss.  Measured here with ``kill -9`` 6.5 s into
a segment: plain MP4 is lost entirely (no ``moov`` atom), fragmented MP4 with one-second
fragments keeps 6.0 s (whole fragments only), MPEG-TS with every packet flushed keeps
6.9 s, i.e. everything that reached the muxer, and its real duration is still read from
the timestamps.  ``flush_packets`` only reaches the inner muxer through
``-segment_format_options``.  ``stream_segment`` (rather than ``segment``) does not ask
encoders for a global header, so VideoToolbox repeats SPS/PPS at every key frame and
each ``.ts`` file decodes on its own.  The price: ``.ts`` files may not open in
QuickTime Player (VLC and IINA play them); the pipeline reads them through ffmpeg.

**File names carry the wall clock:** ``seg_YYYYMMDD-HHMMSS_<epoch>.ts``, expanded by
ffmpeg (``-strftime 1``) when it opens the file.  The local-time part is for people; the
epoch part (``%s``) is what :func:`segment_start_from_name` reads, so a segment's start
time can be recovered from its name alone after a restart, in any time zone and across
daylight-saving changes.  Every segment gets its own clock reading: nothing is derived
from "first start + N x segment length", so a clock correction between segments cannot
shift later ones.  While a recording is live the start time is refined to sub-second
precision as *time of last write - probed duration* (see :func:`estimate_start_ts`),
falling back to the name whenever the two disagree (system sleep, clock step, a stalled
stream).  ``strftime`` has one-second resolution, hence two rules: segments are never
shorter than two seconds, and a restarted RTMP listener never starts within the second
in which the previous file was opened.

**Webcam (avfoundation):** ``-framerate`` and ``-video_size`` are always given (the
default 29.97 fps is rejected by devices that only offer 30.000, and without a size
ffmpeg picks the *last* format); ``-pixel_format nv12`` is what the hardware encoder
wants and ffmpeg falls back by itself to the first format the device supports.  Video
and audio come from *one* avfoundation input so they share a capture clock;
``-fps_mode cfr`` and ``aresample=async=1000:first_pts=0`` keep them locked over hours.
Key frames are forced exactly on segment boundaries (``-force_key_frames
expr:gte(t,n_forced*N)``) so segments are exactly N seconds, with a two-second GOP in
between so later analysis can decode key frames only.  If the device rejects the
requested size or rate, :func:`fallback_command` picks the closest mode from the list
ffmpeg prints and the recorder starts again once, scaling down to the configured size.

**RTMP (Wi-Fi):** ffmpeg itself is the server (``-listen 1``).  The stream is *copied*,
not re-encoded: no generation loss (text stays legible), almost no CPU (the Mac is busy
transcribing), and the bitrate was already chosen on the camera.  The price is that
files can only be cut at the camera's key frames.  ``-rw_timeout`` makes ffmpeg give up
on a camera that walked out of Wi-Fi range (without it ffmpeg hangs forever).  ffmpeg
accepts exactly one connection and exits when it ends, so the recorder starts the
listener again and a camera that reconnects continues in the same session.  Segments are
cut on the wall clock (``-segment_atclocktime 1``): after connecting, ffmpeg writes the
seconds it buffered while probing in one burst, and stream-time cutting would then open
two files within the same second, the second overwriting the first (observed here: 4 s
of a 7 s stream lost with 2 s segments).  Clock-time cutting cannot do that.

Nothing in this module needs macOS to be *tested*: the builders are pure, and the
recorder takes any argv (the tests feed it ffmpeg's ``lavfi`` test sources and a real
local RTMP publisher).
"""

from __future__ import annotations

import atexit
import contextlib
import logging
import os
import re
import subprocess
import threading
import time
import weakref
from collections import deque
from dataclasses import dataclass
from datetime import datetime
from fractions import Fraction
from pathlib import Path

from ..config import Settings
from ..media import ffmpeg as ff
from . import CaptureError
from .devices import CaptureDevice, choose_mode, fps_arg, parse_supported_modes
from .network import rtmp_path

log = logging.getLogger("videonotes.capture.live")

#: ffmpeg ``strftime`` pattern of a segment file name (see the module docstring).
SEGMENT_NAME_PATTERN = "seg_%Y%m%d-%H%M%S_%s.ts"
SEGMENT_PREFIX = "seg_"
SEGMENT_SUFFIX = ".ts"
#: Shortest segment length the builders will ask for (strftime names have 1 s resolution).
MIN_SEGMENT_SECONDS = 2
#: Key-frame interval inside a segment, so analysis can decode key frames only.
GOP_SECONDS = 2.0
#: ffmpeg gives up on a silent RTMP connection after about twice this long.
RTMP_RW_TIMEOUT_S = 15
#: How far "last write - duration" may lie before / after the time in the file name and
#: still be believed (before: buffered data written in a burst; after: jitter).
START_EARLY_TOLERANCE_S = 10.0
START_LATE_TOLERANCE_S = 2.0

_MEDIA_SUFFIXES = (".ts", ".mp4", ".mkv", ".mov", ".m4v", ".flv", ".webm", ".avi")


@dataclass
class Segment:
    """One finished recording file: where it is, when it started (epoch s), how long it is."""

    path: Path
    start_ts: float
    duration: float


# ---------------------------------------------------------------------------------
# Command builders (pure: they only read settings and ask ffmpeg which encoders exist)
# ---------------------------------------------------------------------------------


def segment_pattern(out_dir: str | Path) -> str:
    """Output "URL" for the segment muxer: ``<out_dir>/seg_%Y%m%d-%H%M%S_%s.ts``.

    ffmpeg passes the *whole* path through ``strftime``, so a ``%`` in the folder name is
    doubled to keep it literal.
    """
    return str(Path(out_dir)).replace("%", "%%") + "/" + SEGMENT_NAME_PATTERN


def _segment_seconds(settings: Settings) -> int:
    try:
        seconds = int(settings.capture.segment_seconds)
    except (TypeError, ValueError) as exc:
        raise CaptureError(f"capture.segment_seconds must be a whole number of seconds, got "
                           f"{settings.capture.segment_seconds!r}") from exc  # fmt: skip
    if seconds < MIN_SEGMENT_SECONDS:
        log.warning("capture.segment_seconds=%s is too short; using %s", seconds, MIN_SEGMENT_SECONDS)
        return MIN_SEGMENT_SECONDS
    return seconds


def _parse_size(text: str) -> tuple[int, int]:
    match = re.fullmatch(r"\s*(\d{2,5})\s*[xX×]\s*(\d{2,5})\s*", str(text))
    if not match:
        raise CaptureError(f"capture.video_size must look like 1280x720, got {text!r}")
    return int(match[1]), int(match[2])


def _bitrate_bps(text: str, key: str) -> int:
    match = re.fullmatch(r"\s*(\d+(?:\.\d+)?)\s*([kKmM]?)\s*", str(text))
    if not match or float(match[1]) <= 0:
        raise CaptureError(f"capture.{key} must look like 1500k or 2M, got {text!r}")
    scale = {"": 1, "k": 1000, "m": 1_000_000}[match[2].lower()]
    return int(float(match[1]) * scale)


def _kbit(bps: float) -> str:
    return f"{max(1, round(bps / 1000))}k"


def _scale_filter(width: int, height: int) -> str:
    """Fit inside ``width x height`` keeping the aspect ratio; never scale up; even sizes."""
    return f"scale=w='min(iw,{width})':h='min(ih,{height})':force_original_aspect_ratio=decrease:force_divisible_by=2"


def _video_encoder_args(bitrate: str) -> list[str]:
    """Hardware H.264 when this ffmpeg has it (every Mac build does), else libx264."""
    bps = _bitrate_bps(bitrate, "video_bitrate")
    target, peak = _kbit(bps), _kbit(bps * 1.6)
    if ff.has_encoder("h264_videotoolbox"):
        # -realtime: capture hint; -allow_sw: use Apple's software encoder rather than fail.
        return ["-c:v", "h264_videotoolbox", "-profile:v", "high", "-pix_fmt", "nv12",
                "-b:v", target, "-maxrate", peak, "-realtime", "1", "-allow_sw", "1"]  # fmt: skip
    if ff.has_encoder("libx264"):
        # zerolatency: no look-ahead, so a frame is written when it is captured and the
        # segment files' timing reflects the wall clock.
        return ["-c:v", "libx264", "-preset", "veryfast", "-tune", "zerolatency", "-pix_fmt", "yuv420p",
                "-b:v", target, "-maxrate", peak, "-bufsize", _kbit(bps * 2)]  # fmt: skip
    raise CaptureError(
        "This ffmpeg has no H.264 encoder (neither h264_videotoolbox nor libx264). "
        "Install the Homebrew build:  brew install ffmpeg"
    )


def _segment_args(seconds: int, out_dir: str | Path, *, clock_aligned: bool) -> list[str]:
    args = ["-f", "stream_segment", "-segment_time", str(seconds)]
    if clock_aligned:
        args += ["-segment_atclocktime", "1"]
    return args + [
        "-segment_format", "mpegts",
        "-segment_format_options", "flush_packets=1",
        "-reset_timestamps", "1",
        "-strftime", "1",
        segment_pattern(out_dir),
    ]  # fmt: skip


def _base(loglevel: str = "error") -> list[str]:
    # base_cmd() carries -nostdin; -stdin after it switches the keyboard interface back on
    # so the recorder can ask ffmpeg to finish cleanly by writing "q" to its stdin.
    return ff.base_cmd(loglevel=loglevel) + ["-stdin"]


def webcam_command(settings: Settings, video: CaptureDevice, audio: CaptureDevice | None, out_dir: Path) -> list[str]:
    """ffmpeg argv that records the camera (USB webcam mode) into fixed-length segments.

    ``video`` and ``audio`` come from :func:`videonotes.capture.devices.pick_device`
    immediately before launch (indices change when devices are plugged in).  ``audio`` is
    the camera's own USB microphone, any other input device, the pseudo device for the
    Mac's default input, or ``None`` for a video-only recording.
    """
    cap = settings.capture
    if video.kind != "video" or video.index < 0:
        raise CaptureError(f"{video.name!r} is not a video capture device")
    width, height = _parse_size(cap.video_size)
    try:
        fps = float(cap.framerate)
    except (TypeError, ValueError):
        fps = 0.0
    if not 1.0 <= fps <= 240.0:
        raise CaptureError(f"capture.framerate must be between 1 and 240, got {cap.framerate!r}")
    seconds = _segment_seconds(settings)

    if audio is None:
        audio_part = "none"
        log.info("recording %r without audio", video.name)
    elif audio.kind != "audio":
        raise CaptureError(f"{audio.name!r} is not an audio capture device")
    elif audio.index < 0:
        audio_part = "default"
        log.info("recording %r with the Mac's default input device as microphone", video.name)
    else:
        audio_part = str(audio.index)
        log.info("recording %r with microphone %r", video.name, audio.name)

    rate = fps_arg(fps)
    cmd = _base()
    cmd += [
        "-f", "avfoundation",
        "-framerate", rate,
        "-video_size", f"{width}x{height}",
        "-pixel_format", "nv12",
        "-i", f"{video.index}:{audio_part}",
        "-map", "0:v:0",
    ]  # fmt: skip
    cmd += ["-map", "0:a:0"] if audio is not None else ["-an"]
    cmd += ["-vf", _scale_filter(width, height), "-fps_mode", "cfr", "-r", rate]
    cmd += _video_encoder_args(cap.video_bitrate)
    cmd += ["-g", str(max(1, round(fps * GOP_SECONDS))), "-force_key_frames", f"expr:gte(t,n_forced*{seconds})"]
    if audio is not None:
        _bitrate_bps(cap.audio_bitrate, "audio_bitrate")
        cmd += ["-af", "aresample=async=1000:first_pts=0",
                "-c:a", "aac", "-b:a", str(cap.audio_bitrate).strip(), "-ac", "1", "-ar", "48000"]  # fmt: skip
    return cmd + _segment_args(seconds, out_dir, clock_aligned=False)


def rtmp_listen_command(settings: Settings, out_dir: Path) -> list[str]:
    """ffmpeg argv that waits for the camera's RTMP push and records it into segments.

    Listens on every interface at ``capture.rtmp_port``; the camera is told to push to
    :func:`videonotes.capture.network.rtmp_url`.  ffmpeg waits for the first connection
    for as long as it takes, serves exactly one, and exits when that one ends or goes
    silent; :class:`SegmentRecorder` then listens again.
    """
    cap = settings.capture
    try:
        port = int(cap.rtmp_port)
    except (TypeError, ValueError):
        port = 0
    if not 1 <= port <= 65535:
        raise CaptureError(f"capture.rtmp_port must be between 1 and 65535, got {cap.rtmp_port!r}")
    seconds = _segment_seconds(settings)
    cmd = _base()
    cmd += [
        "-listen", "1",
        "-rw_timeout", str(RTMP_RW_TIMEOUT_S * 1_000_000),
        "-i", f"rtmp://0.0.0.0:{port}/{rtmp_path(settings)}",
        "-map", "0:v:0",
        "-map", "0:a:0?",
        "-c", "copy",
    ]  # fmt: skip
    return cmd + _segment_args(seconds, out_dir, clock_aligned=True)


def is_listener_command(command: list[str]) -> bool:
    """True if ``command`` makes ffmpeg wait for an incoming connection (``-listen 1``)."""
    for flag in ("-listen", "-rtmp_listen"):
        if flag in command:
            index = command.index(flag)
            if index + 1 < len(command) and command[index + 1] not in ("0", "false"):
                return True
    return False


def _as_fps(text: str) -> float | None:
    try:
        return float(Fraction(text))
    except (ValueError, ZeroDivisionError):
        return None


def fallback_command(command: list[str], stderr_text: str) -> list[str] | None:
    """A corrected avfoundation command after "Selected video size/framerate ... not supported".

    ``stderr_text`` is what the failed ffmpeg printed; it contains the device's
    ``Supported modes:`` list.  Returns ``command`` with ``-video_size`` / ``-framerate``
    replaced by the closest supported mode (the output is still scaled to the configured
    size), or ``None`` when this is not that failure or nothing better can be offered.
    """
    if "avfoundation" not in command or "Supported modes" not in stderr_text:
        return None
    try:
        i_size, i_rate, i_input = command.index("-video_size"), command.index("-framerate"), command.index("-i")
        width, height = _parse_size(command[i_size + 1])
    except (ValueError, IndexError, CaptureError):
        return None
    fps = _as_fps(command[i_rate + 1])
    if fps is None or not (i_size < i_input and i_rate < i_input):
        return None
    mode = choose_mode(parse_supported_modes(stderr_text), width, height, fps)
    if mode is None:
        return None
    new = list(command)
    new[i_size + 1] = f"{mode.width}x{mode.height}"
    new[i_rate + 1] = fps_arg(mode.max_fps)
    if new == command:
        return None
    if mode.max_fps < fps - 0.01:  # a slower camera: do not pad the output with duplicate frames
        for flag, value in (("-r", fps_arg(mode.max_fps)), ("-g", str(max(1, round(mode.max_fps * GOP_SECONDS))))):
            if flag in new[i_input:]:
                new[new.index(flag, i_input) + 1] = value
    return new


# ---------------------------------------------------------------------------------
# Wall-clock start of a segment
# ---------------------------------------------------------------------------------

_NAME_EPOCH = re.compile(r"_(\d{9,11})(?:\.[A-Za-z0-9]+)?$")
_NAME_LOCAL = re.compile(r"(\d{8})-(\d{6})")


def segment_start_from_name(name: str) -> float | None:
    """Epoch seconds ffmpeg opened a ``seg_YYYYMMDD-HHMMSS_<epoch>.ts`` file at, from its name.

    Prefers the epoch field; falls back to the local-time field (interpreted in the
    current time zone) for names written by a C library without ``%s``.  ``None`` for any
    other name.
    """
    base = os.path.basename(name)
    match = _NAME_EPOCH.search(base)
    if match:
        return float(match[1])
    match = _NAME_LOCAL.search(base)
    if match:
        try:
            return datetime.strptime(match[1] + match[2], "%Y%m%d%H%M%S").timestamp()
        except (ValueError, OverflowError, OSError):
            return None
    return None


def estimate_start_ts(name_ts: float | None, mtime: float, duration: float) -> float:
    """Wall-clock time of a segment's first frame.

    ``mtime - duration`` (when the last packet was written, minus how much media the file
    holds) is accurate to a fraction of a second for a live source, and unlike the file
    name it is not late by the seconds ffmpeg spent probing a fresh RTMP connection.  It
    is wrong when wall time passed without media (system sleep, a stalled camera, the
    trailer of a dead connection written late) or when the clock was stepped, so it is
    only used while it stays close to the whole-second time in the file name; otherwise
    the name wins.  Without a time in the name there is nothing to check against.
    """
    by_content = mtime - max(0.0, duration)
    if name_ts is None:
        return by_content
    if name_ts - START_EARLY_TOLERANCE_S <= by_content <= name_ts + 1.0 + START_LATE_TOLERANCE_S:
        return by_content
    return name_ts


def _read_segment(path: Path, *, min_seconds: float, fallback_seconds: float) -> Segment | None:
    """Probe one finished file. ``None`` when it holds no usable media."""
    try:
        stat = path.stat()
    except OSError:
        return None
    if stat.st_size <= 0:
        return None
    info = ff.probe(path, timeout=30.0)  # FFmpegError propagates: the caller decides what an unreadable file means
    if not (info.has_video or info.has_audio):
        return None
    name_ts = segment_start_from_name(path.name)
    duration = info.duration
    if duration <= 0 and name_ts is not None and stat.st_mtime > name_ts:
        # A container without usable timestamps: bound the length by the wall clock instead.
        duration = min(float(fallback_seconds), stat.st_mtime - name_ts)
    if duration < min_seconds:
        return None
    return Segment(path=path, start_ts=estimate_start_ts(name_ts, stat.st_mtime, duration), duration=duration)


def recover_segments(out_dir: str | Path, *, min_seconds: float = 0.5) -> list[Segment]:
    """Segments found in a recording folder, oldest first (e.g. after a crash or restart).

    Start times come from the file names (and are refined from the files' modification
    times when those are still intact).  Nothing is modified or deleted; unreadable and
    tiny files are skipped.
    """
    folder = Path(out_dir)
    found: list[Segment] = []
    try:
        names = sorted(n for n in os.listdir(folder) if n.startswith(SEGMENT_PREFIX) and n.endswith(_MEDIA_SUFFIXES))
    except OSError:
        return found
    for name in names:
        try:
            segment = _read_segment(folder / name, min_seconds=min_seconds, fallback_seconds=3600.0)
        except ff.FFmpegError as exc:
            log.warning("skipping unreadable segment %s: %s", name, exc)
            continue
        if segment is not None:
            found.append(segment)
    found.sort(key=lambda s: (s.start_ts, s.path.name))
    return found


# ---------------------------------------------------------------------------------
# Turning ffmpeg's stderr into something a person can act on
# ---------------------------------------------------------------------------------

_EXPLANATIONS: tuple[tuple[re.Pattern[str], str], ...] = (
    (
        re.compile(r"Address already in use"),
        "The network port is already in use: another `vnote wireless` (or another streaming server) is running "
        "on this Mac. Stop it, or choose a different port with --set capture.rtmp_port=1936.",
    ),
    (
        re.compile(r"Selected (?:video size|framerate) .*is not supported by the device"),
        "The camera does not offer the requested picture size or frame rate. Choose one of the modes listed "
        "below, e.g. --set capture.video_size=1920x1080 --set capture.framerate=30.",
    ),
    (
        re.compile(r"Failed to create AV capture input device"),
        "macOS did not let ffmpeg open the camera or microphone. Another app may be using it, or access is "
        "switched off: System Settings → Privacy & Security → Camera and Microphone → enable your terminal app, "
        "then quit the terminal completely and open it again.",
    ),
    (
        re.compile(r"(?:Video|Audio) device not found|Invalid (?:audio )?device index|No AV capture device found"),
        "The camera or microphone is not where it was in the device list (unplugged, or the camera left Webcam "
        "mode?). Check with `vnote devices` and start again.",
    ),
    (
        re.compile(r"Unknown input format: '?avfoundation"),
        "This ffmpeg cannot capture from cameras. Install the Homebrew build:  brew install ffmpeg",
    ),
    (
        re.compile(
            r"Unrecognized option|Option not found|Unknown encoder|Protocol not found|"
            r"Requested output format .* is not (?:a suitable|known)|"
            r"Unable to (?:find a suitable|choose an) output format"
        ),
        "This ffmpeg is too old or was built without something videonotes needs. Update it:  brew upgrade ffmpeg",
    ),
    (
        re.compile(r"No space left on device"),
        "The disk is full. Free up some space and start again.",
    ),
)

_PIXFMT_NOTE = re.compile(
    r"Selected pixel format \(.*\) is not supported by the input device|Supported pixel formats:|"
    r"Overriding selected pixel format"
)
_LOG_PREFIX = re.compile(r"^\[[^\]\n]*@\s*0x[0-9a-fA-F]+\]\s?")


def explain_ffmpeg_error(stderr_text: str) -> str:
    """What to do about a known ffmpeg failure, or "" when the text is not recognised."""
    for pattern, advice in _EXPLANATIONS:
        if pattern.search(stderr_text):
            return advice
    return ""


def _meaningful(lines: list[str]) -> list[str]:
    """Drop avfoundation's harmless "pixel format not supported, overriding" chatter."""
    kept: list[str] = []
    in_formats = False
    for line in lines:
        bare = _LOG_PREFIX.sub("", line).strip()
        if _PIXFMT_NOTE.search(bare):
            in_formats = "Supported pixel formats" in bare
            continue
        if in_formats and re.fullmatch(r"[a-z0-9_]+", bare):
            continue
        in_formats = False
        kept.append(line)
    return kept


# ---------------------------------------------------------------------------------
# The recorder
# ---------------------------------------------------------------------------------

_NEW, _RUNNING, _FINISHED = "new", "running", "finished"

_live_recorders: weakref.WeakSet[SegmentRecorder] = weakref.WeakSet()


def _stop_recorders_at_exit() -> None:
    for recorder in list(_live_recorders):
        with contextlib.suppress(Exception):
            recorder._emergency_stop()


atexit.register(_stop_recorders_at_exit)


class SegmentRecorder:
    """Runs one ffmpeg process that writes fixed-length segments and reports each
    segment once it is complete (i.e. once ffmpeg has moved on to the next file).

    ``command`` is any ffmpeg argv whose output files land in ``out_dir`` (normally from
    :func:`webcam_command` or :func:`rtmp_listen_command`).  Typical use::

        recorder = SegmentRecorder(command, out_dir, segment_seconds=60)
        recorder.start()
        while recorder.running:
            for segment in recorder.poll():
                ...                      # a finished file with start_ts and duration
            time.sleep(1)
        leftovers = recorder.stop()      # always call: finishes ffmpeg, returns the rest
        why = recorder.last_error()      # "" unless something went wrong

    What it takes care of:

    * **Completion.** A background thread watches ``out_dir``; a file is complete when
      ffmpeg has opened a later one or has exited.  Files are reported in the order
      ffmpeg created them (not by name, so a clock change cannot reorder them), each
      exactly once, with a probed duration.  Empty and sub-half-second files (a
      segment ffmpeg had only just opened when it stopped) are deleted, not returned.
    * **Stopping.** ``stop()`` writes ``q`` to ffmpeg's stdin, then sends SIGTERM, then
      SIGKILL, each after a timeout, and always reaps the process.  Recorders still
      running when Python exits are stopped too.
    * **Dying at start.** If ffmpeg exits (device busy, permission denied, bad flags),
      ``running`` becomes False and ``last_error()`` explains, with advice for the
      failures that have a known fix.  A camera that rejects the requested picture
      size or frame rate is retried once with the closest mode it offers.
    * **Hanging.** avfoundation waits forever for a first frame (unanswered permission
      dialog) and keeps running when the camera is unplugged.  If no data arrives for
      ``startup_timeout`` seconds after launch, or the current file stops growing for
      ``stall_timeout`` seconds, ffmpeg is stopped and ``last_error()`` says why.
      (``None`` picks defaults that suit the command; ``0`` disables a check.)
    * **RTMP reconnects.** A listener (``-listen 1``) serves one connection and exits;
      it is started again, so ``running`` stays True between connections and a camera
      that reconnects continues in the same recording.  The time waiting for the first
      connection is unlimited.
    """

    #: Seconds to wait for ffmpeg after "q", after SIGTERM and after SIGKILL.
    QUIT_WAIT_S = 3.0
    TERM_WAIT_S = 5.0
    KILL_WAIT_S = 5.0
    #: Default watchdog limits (seconds).
    STARTUP_TIMEOUT_S = 45.0
    STALL_TIMEOUT_S = 20.0
    LISTENER_STALL_TIMEOUT_S = 90.0
    #: How often the background thread looks at the folder and the process.
    MONITOR_INTERVAL_S = 0.2
    #: Pause before listening again after a connection that delivered video.  Kept short: the
    #: port is closed in between, and a camera that retries at once should not be turned away.
    RELISTEN_DELAY_S = 0.1
    #: First pause after a connection that delivered nothing (doubles each time, up to 8x).
    RELISTEN_BACKOFF_S = 1.0
    #: A listener that fails this quickly before any camera ever connected could not start at all.
    LISTENER_STARTUP_FAIL_S = 2.0
    #: Give up listening after this many connections in a row that delivered nothing.
    MAX_UNPRODUCTIVE_RUNS = 5
    #: Files with less media than this are discarded.
    MIN_SEGMENT_S = 0.5
    #: ...unless they are this big: a large file ffprobe cannot make sense of is kept for inspection.
    KEEP_UNREADABLE_BYTES = 1024 * 1024

    def __init__(
        self,
        command: list[str],
        out_dir: Path,
        *,
        segment_seconds: int,
        startup_timeout: float | None = None,
        stall_timeout: float | None = None,
    ) -> None:
        if not command:
            raise ValueError("SegmentRecorder needs a command to run")
        self.command = [str(part) for part in command]
        self.out_dir = Path(out_dir)
        self.segment_seconds = max(1, int(segment_seconds))
        self._listener = is_listener_command(self.command)
        if startup_timeout is None:
            startup_timeout = 0.0 if self._listener else self.STARTUP_TIMEOUT_S
        if stall_timeout is None:
            stall_timeout = self.LISTENER_STALL_TIMEOUT_S if self._listener else self.STALL_TIMEOUT_S
        self._startup_timeout = max(0.0, float(startup_timeout))
        self._stall_timeout = max(0.0, float(stall_timeout))
        self._prefix, self._suffixes = _name_filter(self.command, self.out_dir)

        self._lock = threading.RLock()  # state below
        self._harvest_lock = threading.Lock()  # one poll()/stop() harvest at a time
        self._err_lock = threading.Lock()  # stderr lines
        self._state = _NEW
        self._proc: subprocess.Popen[bytes] | None = None
        self._reader: threading.Thread | None = None
        self._monitor: threading.Thread | None = None
        self._stopping = False
        self._quiet_exit = False  # stopped on request: whatever ffmpeg printed while dying is not an error
        self._generation = 0  # bumped by every start(); lets an old watcher thread notice it is obsolete
        self._abort_reason = ""
        self._failure = ""
        self._returncode: int | None = None
        self._tail: deque[str] = deque(maxlen=40)  # last stderr lines of the current run
        self._run_lines: list[str] = []  # all stderr lines of the current run (bounded)
        self._preexisting: set[str] = set()
        self._known: set[str] = set()
        self._order: list[str] = []  # segment file names in the order ffmpeg created them
        self._reported: set[str] = set()
        self._pending: list[Segment] = []  # inspected, not handed out yet (see _harvest)
        self._run_first = 0  # index into _order of the current run's first file
        self._launched_at = 0.0
        self._last_progress = 0.0
        self._progress_mark: tuple[int, int] = (0, -1)
        self._relaunch_at: float | None = None
        self._fallback_used = False
        self._ever_produced = False
        self._unproductive_runs = 0

    # -- public API -----------------------------------------------------------------

    def start(self) -> None:
        """Launch ffmpeg. Returns at once; a failure shows up as ``running == False``.

        Does nothing while a recording is running.  After the recording has ended (by
        itself or through :meth:`stop`) it starts a new one in the same folder.  Raises
        :class:`~videonotes.media.ffmpeg.FFmpegError` only when the program cannot be
        executed at all.
        """
        with self._lock:
            if self._state == _RUNNING:
                return
            try:
                self.out_dir.mkdir(parents=True, exist_ok=True)
            except OSError as exc:
                raise CaptureError(f"Cannot create the recording folder {self.out_dir}: {exc}") from exc
            if self._state == _NEW:
                self._preexisting = set(self._list_names())
            self._stopping = False
            self._quiet_exit = False
            self._failure = ""
            self._abort_reason = ""
            self._returncode = None
            self._relaunch_at = None
            self._unproductive_runs = 0
            self._launch()
            self._state = _RUNNING
            self._generation += 1
            _live_recorders.add(self)
            self._monitor = threading.Thread(
                target=self._monitor_loop, args=(self._generation,), name="vnote-recorder", daemon=True
            )
            self._monitor.start()

    def poll(self) -> list[Segment]:
        """Newly completed segments, oldest first. Never blocks for long; safe to call any time."""
        return self._harvest()

    def stop(self) -> list[Segment]:
        """Finish the recording cleanly and return the segments not yet reported.

        Asks ffmpeg to quit (``q``), escalates to SIGTERM and SIGKILL after timeouts,
        reaps the process and stops the background thread.  Safe to call more than
        once, from ``finally`` blocks, and on a recorder that never started.
        """
        with self._lock:
            if self._state == _NEW:
                return []
            if self._state == _RUNNING:
                self._tick()  # notice an ffmpeg that has already died by itself: that is not a quiet exit
            self._stopping = True
            self._quiet_exit = self._state == _RUNNING
            self._relaunch_at = None
            proc = self._proc
            wrote_media = len(self._order) > self._run_first
        if proc is not None and proc.poll() is None:
            self._shut_down(proc, graceful=True, in_main_loop=wrote_media)
        with self._lock:
            self._tick()
            if self._state == _RUNNING:  # nothing was running (between two listener runs)
                self._finish("")
            monitor = self._monitor
        if monitor is not None and monitor is not threading.current_thread():
            monitor.join(timeout=5.0)
        return self._harvest()

    @property
    def running(self) -> bool:
        """True while the recording is in progress (including while a listener waits)."""
        with self._lock:
            self._tick()
            return self._state == _RUNNING

    @property
    def returncode(self) -> int | None:
        """Exit status of the last ffmpeg process that ended, if any."""
        with self._lock:
            return self._returncode

    @property
    def pid(self) -> int | None:
        """Process id of the running ffmpeg, if any."""
        with self._lock:
            return self._proc.pid if self._proc is not None else None

    def last_error(self) -> str:
        """Why the recording stopped or is in trouble: advice first, then ffmpeg's last lines.

        Empty when nothing went wrong.
        """
        with self._err_lock:
            lines = _meaningful(list(self._tail))
        with self._lock:
            failure = self._failure
            if self._quiet_exit and not failure:
                return ""
        parts: list[str] = []
        if failure:
            parts.append(failure)
        advice = explain_ffmpeg_error("\n".join(lines))
        if advice and advice not in parts:
            parts.append(advice)
        if lines:
            parts.append("\n".join(lines[-10:]))
        return "\n".join(parts)

    def __enter__(self) -> SegmentRecorder:
        self.start()
        return self

    def __exit__(self, *exc: object) -> None:
        self.stop()

    def __del__(self) -> None:
        with contextlib.suppress(Exception):
            self._emergency_stop()

    # -- process handling -------------------------------------------------------------

    def _launch(self) -> None:
        """Start ffmpeg (lock held)."""
        with self._err_lock:
            self._tail.clear()
            self._run_lines = []
        try:
            proc = subprocess.Popen(
                self.command, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE
            )
        except OSError as exc:
            raise ff.FFmpegError(f"Could not run {self.command[0]}: {exc}\n{ff.INSTALL_HINT}") from exc
        self._proc = proc
        self._abort_reason = ""
        self._run_first = len(self._order)
        self._launched_at = self._last_progress = time.monotonic()
        self._progress_mark = (len(self._order), -1)
        self._reader = threading.Thread(target=self._drain, args=(proc,), name="vnote-recorder-stderr", daemon=True)
        self._reader.start()
        log.debug("started ffmpeg pid %s: %s", proc.pid, " ".join(self.command))

    def _drain(self, proc: subprocess.Popen[bytes]) -> None:
        """Reader thread: keep ffmpeg's stderr flowing and remember its last lines."""
        stream = proc.stderr
        if stream is None:
            return
        pending = b""
        try:
            while True:
                chunk = stream.read1(4096)  # type: ignore[union-attr]
                if not chunk:
                    break
                *lines, pending = re.split(rb"[\r\n]", pending + chunk)
                if len(pending) > 8192:  # a "line" that never ends
                    lines.append(pending)
                    pending = b""
                self._remember(lines)
        except (OSError, ValueError):
            pass
        finally:
            self._remember([pending])

    def _remember(self, raw_lines: list[bytes]) -> None:
        texts = [t for t in (raw.decode("utf-8", "replace").strip() for raw in raw_lines) if t]
        if not texts:
            return
        with self._err_lock:
            self._tail.extend(texts)
            if len(self._run_lines) < 400:
                self._run_lines.extend(texts)
        for text in texts:
            log.debug("ffmpeg: %s", text)

    @staticmethod
    def _wait(proc: subprocess.Popen[bytes], seconds: float) -> bool:
        try:
            proc.wait(timeout=max(0.0, seconds))
            return True
        except subprocess.TimeoutExpired:
            return False

    def _shut_down(self, proc: subprocess.Popen[bytes], *, graceful: bool, in_main_loop: bool = True) -> None:
        """Make ``proc`` exit: "q" (when graceful), then SIGTERM, then SIGKILL. No lock held."""
        try:
            if graceful:
                with contextlib.suppress(OSError, ValueError):
                    if proc.stdin is not None and not proc.stdin.closed:
                        proc.stdin.write(b"q")
                        proc.stdin.flush()
                # ffmpeg only reads its keyboard once it is transcoding; before that (still
                # opening the device, or waiting for a connection) only a signal is noticed.
                if self._wait(proc, self.QUIT_WAIT_S if in_main_loop else 0.3):
                    return
            with contextlib.suppress(OSError):
                proc.terminate()  # ffmpeg finishes the current file on SIGTERM as well
            if self._wait(proc, self.TERM_WAIT_S):
                return
            log.warning("ffmpeg (pid %s) did not react to a polite request; killing it", proc.pid)
            with contextlib.suppress(OSError):
                proc.kill()
            self._wait(proc, self.KILL_WAIT_S)
        except BaseException:  # e.g. a second Ctrl-C while waiting: never leave ffmpeg behind
            with contextlib.suppress(OSError):
                proc.kill()
            self._wait(proc, self.KILL_WAIT_S)
            raise

    def _emergency_stop(self) -> None:
        """Last-resort cleanup (interpreter exit, garbage collection): no locks, no waiting around."""
        proc = self.__dict__.get("_proc")
        if proc is None or proc.poll() is not None:
            return
        with contextlib.suppress(OSError):
            proc.terminate()
        if not self._wait(proc, 2.0):
            with contextlib.suppress(OSError):
                proc.kill()
            self._wait(proc, 2.0)

    def _reap(self, proc: subprocess.Popen[bytes]) -> int:
        """Collect an exited process: exit status, remaining stderr, pipes (lock held)."""
        returncode = proc.wait()
        reader = self._reader
        if reader is not None and reader is not threading.current_thread():
            reader.join(timeout=3.0)
        for stream in (proc.stdin, proc.stderr):
            with contextlib.suppress(OSError, ValueError):
                if stream is not None:
                    stream.close()
        return returncode

    # -- supervision (all with the lock held) -----------------------------------------

    def _monitor_loop(self, generation: int) -> None:
        while True:
            time.sleep(self.MONITOR_INTERVAL_S)
            try:
                with self._lock:
                    if generation != self._generation:
                        return
                    self._tick()
                    if self._state != _RUNNING:
                        return
            except Exception:  # never let the watcher die silently
                log.exception("recorder supervision failed")

    def _tick(self) -> None:
        """Look at the folder and the process once and act on what changed."""
        if self._state != _RUNNING:
            return
        self._scan()
        proc = self._proc
        if proc is None:
            if self._relaunch_at is not None and time.monotonic() >= self._relaunch_at:
                self._relaunch_at = None
                try:
                    self._launch()
                except ff.FFmpegError as exc:
                    self._finish(str(exc))
            return
        returncode = proc.poll()
        if returncode is not None:
            self._handle_exit(proc)
            return
        self._watchdog(proc)

    def _watchdog(self, proc: subprocess.Popen[bytes]) -> None:
        now = time.monotonic()
        wrote_media = len(self._order) > self._run_first
        if not wrote_media:
            if self._startup_timeout and now - self._launched_at > self._startup_timeout:
                self._abort_reason = "startup"
        elif self._stall_timeout and now - self._last_progress > self._stall_timeout:
            self._abort_reason = "stall"
        if self._abort_reason:
            log.warning("no data from ffmpeg (%s watchdog); stopping it", self._abort_reason)
            self._shut_down(proc, graceful=False)
            self._handle_exit(proc)

    def _handle_exit(self, proc: subprocess.Popen[bytes]) -> None:
        """ffmpeg is gone: decide between done, failed, try again and listen again."""
        returncode = self._reap(proc)
        self._returncode = returncode
        self._proc = None
        self._scan()
        wrote_media = len(self._order) > self._run_first
        run_seconds = time.monotonic() - self._launched_at
        with self._err_lock:
            run_text = "\n".join(self._run_lines)
        log.debug("ffmpeg exited with status %s after %.1f s", returncode, run_seconds)

        if self._stopping:
            self._finish("")
            return

        if self._abort_reason:
            reason, self._abort_reason = self._abort_reason, ""
            if self._listener and reason == "stall":
                log.warning("the camera's stream went silent; listening for it again")
                self._schedule_relaunch(self._relisten_delay())
                return
            self._finish(self._watchdog_message(reason))
            return

        # Ctrl-C in the terminal reaches ffmpeg too: it then finishes its file and exits with 255
        # (or reports "Immediate exit requested" if it was still opening its input).  That is a
        # stop, not a failure to explain or recover from.  (255 with error output is a real
        # failure: ffmpeg also uses that status for "Operation not permitted".)
        if returncode < 0:
            self._finish(f"ffmpeg was killed (signal {-returncode}).")
            return
        if "Immediate exit requested" in run_text or (returncode == 255 and not _meaningful(run_text.splitlines())):
            self._quiet_exit = True
            self._finish("")
            return

        if returncode != 0 and not wrote_media and not self._fallback_used:
            replacement = fallback_command(self.command, run_text)
            if replacement is not None:
                self._fallback_used = True
                log.warning(
                    "the camera does not offer the requested capture mode; using %s at %s fps instead "
                    "(the recording is still scaled to the configured size)",
                    replacement[replacement.index("-video_size") + 1],
                    replacement[replacement.index("-framerate") + 1],
                )
                self.command = replacement
                self._schedule_relaunch(0.0)
                return

        if self._listener:
            if wrote_media:
                self._ever_produced = True
                self._unproductive_runs = 0
            else:
                self._unproductive_runs += 1
            could_not_start = not self._ever_produced and returncode != 0 and run_seconds < self.LISTENER_STARTUP_FAIL_S
            if not could_not_start and self._unproductive_runs <= self.MAX_UNPRODUCTIVE_RUNS:
                if wrote_media:
                    log.info("the camera's stream ended; listening for it again")
                backoff = self.RELISTEN_BACKOFF_S * min(8, 2 ** (self._unproductive_runs - 1))
                self._schedule_relaunch(self._relisten_delay() if wrote_media else backoff)
                return

        self._finish("" if returncode == 0 else f"ffmpeg stopped with exit status {returncode}.")

    def _relisten_delay(self) -> float:
        """How long to wait before listening again: as short as the one-second file names allow."""
        delay = self.RELISTEN_DELAY_S
        if self._order:
            opened = segment_start_from_name(self._order[-1])
            if opened is not None:  # the next file must be opened in a later second, or it would replace this one
                delay = max(delay, min(2.0, opened + 1.0 - time.time()))
        return delay

    def _schedule_relaunch(self, delay: float) -> None:
        self._relaunch_at = time.monotonic() + max(0.0, delay)

    def _finish(self, failure: str) -> None:
        self._state = _FINISHED
        self._relaunch_at = None
        if failure:
            self._failure = failure
        _live_recorders.discard(self)

    def _watchdog_message(self, reason: str) -> str:
        camera = "avfoundation" in self.command
        if reason == "startup":
            text = f"No video arrived within {self._startup_timeout:.0f} seconds, so the recording was stopped."
            if camera:
                text += (
                    " If macOS showed a dialog asking for access to the camera or microphone, allow it (System "
                    "Settings → Privacy & Security → Camera / Microphone → your terminal app) and run the "
                    "command "
                    "again. Also check that the camera still shows “Webcam” on its screen; if the microphone is "
                    "the problem, try --audio none."
                )
            return text
        text = (
            f"The video stopped arriving ({self._stall_timeout:.0f} seconds without data), "
            "so the recording was stopped."
        )
        if camera:
            text += (
                " Was the camera unplugged or switched off, or did it overheat? Everything recorded up to that "
                "point is kept."
            )
        return text

    # -- files --------------------------------------------------------------------------

    def _is_segment_name(self, name: str) -> bool:
        return not name.startswith(".") and name.startswith(self._prefix) and name.lower().endswith(self._suffixes)

    def _list_names(self) -> list[str]:
        try:
            return [name for name in os.listdir(self.out_dir) if self._is_segment_name(name)]
        except OSError:
            return []

    def _scan(self) -> None:
        """Notice new files (in creation order) and whether the newest one is growing."""
        fresh: list[tuple[int, str]] = []
        try:
            with os.scandir(self.out_dir) as entries:
                for entry in entries:
                    name = entry.name
                    if name in self._known or name in self._preexisting or not self._is_segment_name(name):
                        continue
                    try:
                        if entry.is_file():
                            fresh.append((entry.stat().st_mtime_ns, name))
                    except OSError:
                        continue
        except OSError:
            return
        for _mtime, name in sorted(fresh):  # several new files at once: the one still growing is the newest
            self._known.add(name)
            self._order.append(name)
        size = -1
        if self._order:
            with contextlib.suppress(OSError):
                size = os.stat(self.out_dir / self._order[-1]).st_size
        mark = (len(self._order), size)
        if mark != self._progress_mark:
            self._progress_mark = mark
            self._last_progress = time.monotonic()

    def _harvest(self) -> list[Segment]:
        with self._harvest_lock:
            with self._lock:
                self._tick()
                names = self._order
                if self._proc is not None and len(names) > self._run_first:
                    names = names[:-1]  # the file ffmpeg is writing right now
                ready = [name for name in names if name not in self._reported]
            for name in ready:
                # Probing takes a moment.  If Ctrl-C lands in it, the file stays unreported and
                # what was already inspected stays in _pending: the next call hands it all out.
                segment = self._finalize(self.out_dir / name)
                with self._lock:
                    self._reported.add(name)
                    if segment is not None:
                        self._pending.append(segment)
            with self._lock:
                segments, self._pending = self._pending, []
            return segments

    def _finalize(self, path: Path) -> Segment | None:
        """Turn a finished file into a Segment, or discard it."""
        try:
            segment = _read_segment(path, min_seconds=self.MIN_SEGMENT_S, fallback_seconds=self.segment_seconds)
        except ff.FFmpegError as exc:
            try:
                size = path.stat().st_size
            except OSError:
                return None
            if size >= self.KEEP_UNREADABLE_BYTES:
                log.warning("could not read the recorded segment %s (kept on disk, not analysed): %s", path.name, exc)
                return None
            segment = None
        except Exception:
            log.exception("could not inspect the recorded segment %s", path.name)
            return None
        if segment is None:
            with contextlib.suppress(OSError):
                if path.stat().st_size >= self.KEEP_UNREADABLE_BYTES:
                    log.warning(
                        "the recorded segment %s holds no readable media (kept on disk, not analysed)", path.name
                    )
                    return None
                log.debug("discarding empty or tiny segment %s", path.name)
                path.unlink()
        return segment


def _name_filter(command: list[str], out_dir: Path) -> tuple[str, tuple[str, ...]]:
    """Which file names in ``out_dir`` are segments of ``command``: (prefix, allowed suffixes).

    Taken from the output pattern (the last argument) when it points into ``out_dir``;
    otherwise any media file counts.
    """
    pattern = command[-1].replace("%%", "\0")
    folder, _, base = pattern.rpartition("/")
    literal_dir = folder.replace("\0", "%")
    try:
        inside = bool(folder) and os.path.abspath(literal_dir) == os.path.abspath(out_dir)
    except (OSError, ValueError):
        inside = False
    suffix = os.path.splitext(base)[1].replace("\0", "%").lower()
    if not inside or "%" in suffix or not suffix:
        return "", _MEDIA_SUFFIXES
    prefix = base.split("%", 1)[0].replace("\0", "%")
    return prefix, (suffix,)
