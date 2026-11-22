"""Importing recordings: the camera's SD card / USB volume, a folder of videos, or one file.

The card is treated as **read-only**: files are opened for reading and nothing on it is
ever written, renamed or deleted.

What a DJI Osmo Action 4 / 5 Pro card looks like (from the USB research; names verified
against media lists captured from a real Action 4)::

    <volume>/DCIM/DJI_001/DJI_20260812131032_0006_D.MP4    main video (4K, up to ~16 GB)
                          DJI_20260812131032_0006_D.LRF    low-res proxy: an MP4 (H.264, 720 lines)
                          DJI_20260812131032_0006_D.WAV    optional audio backup (ignored)
                          DJI_20260811205751_0002_D.JPG    still photo
                          DJI_20260811205751_0002_D.DNG    raw still (ignored)
              MISC/THM/DJI_001/….THM / ….SCR               thumbnails (ignored)

* The name is ``PPP_YYYYMMDDhhmmss_NNNN_D[_NNN][_SUFFIX].EXT``: prefix (``DJI``, or ``CAM``
  on Xtra-branded bodies), start time in **camera local time**, the camera's running file
  number, a designator letter, an optional 3-digit sub-index (burst photo, loop-recording
  chapter) and an optional user-defined suffix.  Folders are ``PPP_NNN[_SUFFIX]``.
* A proxy sits next to its main file with the same base name and the extension ``.LRF``
  (``.XRF`` on Xtra bodies).  Pairing is by base name only.
* Long recordings continue in a new file with its own time stamp; there is no naming link
  between the parts, so parts are joined into one session by time (see
  :func:`group_into_sessions`).

Where a clip's start time comes from, best source first:

1. **The file name.**  It is the camera's local wall clock at the moment recording
   started, it is what the wearer saw on the camera, and it is the same whether or not
   the camera was ever paired with the DJI app.  It carries no zone, so it is interpreted
   in the Mac's current time zone (right unless the footage is imported in a different
   zone from where it was shot).
2. **The container's** ``creation_time``.  Labelled UTC, but only trustworthy as UTC when
   the camera knows its zone: an Osmo Action 4 has no time-zone setting of its own and
   learns the zone only from the DJI Mimo app, so a clock set by hand ends up as *local
   time labelled UTC* (GoPro and others do the same).  :func:`resolve_creation_time` uses
   the file's modification time to tell the two readings apart.
3. **The file's modification time** minus the duration (the camera closes the file when
   recording stops).  Copying without preserving times destroys it, hence last.
"""

from __future__ import annotations

import contextlib
import errno
import hashlib
import logging
import os
import re
import shutil
import sqlite3
import stat as stat_module
import subprocess
import unicodedata
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING

from ..config import Settings, is_macos
from ..media import ffmpeg as ff
from ..models import Clip, Session
from ..timeutil import new_session_id
from . import CaptureError

if TYPE_CHECKING:
    from ..store import Store

log = logging.getLogger("videonotes.capture.importer")

#: Extra folders (``os.pathsep``-separated) whose sub-folders are checked for camera cards,
#: in addition to ``/Volumes`` on macOS.  Used by the tests; also handy on other systems.
ENV_VOLUME_ROOTS = "VIDEONOTES_VOLUME_ROOTS"

VIDEO_SUFFIXES = frozenset(
    {".mp4", ".mov", ".m4v", ".mkv", ".avi", ".webm", ".mts", ".m2ts", ".ts", ".3gp", ".mpg", ".mpeg", ".wmv", ".flv"}
)
PROXY_SUFFIXES = frozenset({".lrf", ".xrf"})
PHOTO_SUFFIXES = frozenset({".jpg", ".jpeg"})
#: Still-picture types :func:`import_file` accepts (a card scan only takes the camera's own JPGs).
IMAGE_SUFFIXES = PHOTO_SUFFIXES | {".png", ".heic", ".heif", ".tif", ".tiff", ".bmp", ".webp"}
COPY_MODES = ("proxy", "original", "none")

#: How deep below the given folder recordings are looked for.
MAX_SCAN_DEPTH = 4
_SKIP_DIRS = frozenset({"misc", "thm", "system volume information", "$recycle.bin", "lost.dir"})
_SYSTEM_VOLUMES = frozenset({"macintosh hd", "macintosh hd - data", "recovery", "preboot", "vm", "update", "data"})

_COPY_CHUNK = 4 * 1024 * 1024
_FINGERPRINT_CHUNK = 1024 * 1024
_SPACE_RESERVE = 256 * 1024 * 1024
#: ``creation_time`` and "mtime - duration" closer than this are taken to describe the same moment.
_SAME_MOMENT_S = 120.0

REMOVABLE_VOLUME_HELP = (
    "macOS did not allow reading it. Allow access under System Settings → Privacy & Security → "
    "Files and Folders → (your terminal app) → Removable Volumes, then run the command again."
)
#: File systems that live on another machine: looking into a dead one can block for minutes.
NETWORK_FILESYSTEMS = frozenset(
    {"smbfs", "afpfs", "nfs", "nfs4", "webdav", "ftp", "autofs", "cifs", "macfuse", "osxfuse"}
)

_DJI_FOLDER = re.compile(r"^[A-Z]{3}_\d{3}(?:_[A-Za-z0-9]+)?$")
_DJI_NAME = re.compile(
    r"^(?P<prefix>[A-Za-z]{3})_(?P<ts>\d{14})_(?P<seq>\d{4})_(?P<des>[A-Za-z])"
    r"(?P<rest>(?:_[A-Za-z0-9]+)*)\.(?P<ext>[A-Za-z0-9]+)$"
)


# ---------------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------------


@dataclass
class CardClip:
    """One recording (or still photo) found on a card or in a folder.

    ``original`` is the main file, ``proxy`` its low-res ``.LRF`` companion if there is
    one, ``start_ts`` the wall-clock start (epoch seconds), ``size`` the main file's size
    in bytes and ``index`` the camera's running file number (``None`` for files not named
    by a DJI camera).
    """

    original: Path
    proxy: Path | None
    start_ts: float
    size: int
    index: int | None
    #: Seconds of media once known (probed lazily; always 0.0 for a still photo).
    duration: float | None = None
    #: Where ``start_ts`` came from: "name", "creation_time", "mtime" or "given".
    time_source: str = ""

    @property
    def is_photo(self) -> bool:
        return self.original.suffix.lower() in IMAGE_SUFFIXES

    @property
    def analysed(self) -> Path:
        """The cheapest file that shows the recording: the proxy when there is one."""
        return self.proxy or self.original

    @property
    def end_ts(self) -> float:
        return self.start_ts + (self.duration or 0.0)


@dataclass
class DjiName:
    """The parts of a DJI file name (see the module docstring)."""

    prefix: str
    start_local: datetime  # naive: the camera's local wall clock
    index: int
    sub_index: int | None
    suffix: str | None

    @property
    def start_ts(self) -> float:
        """Epoch seconds, reading the camera's local time in this machine's current time zone."""
        return self.start_local.timestamp()


@dataclass
class ImportReport:
    """What :func:`import_with_report` did."""

    sessions: list[Session] = field(default_factory=list)
    imported: list[CardClip] = field(default_factory=list)
    #: Already in the library (same fingerprint): left alone.
    skipped: list[CardClip] = field(default_factory=list)
    #: Could not be imported, with the reason.
    failed: list[tuple[CardClip, str]] = field(default_factory=list)
    #: True when the source vanished part-way (card pulled out, USB connection dropped).
    source_lost: bool = False

    def failure_summary(self) -> str:
        if not self.failed:
            return ""
        if self.source_lost:
            head = (
                f"The card or folder disappeared during the import; {len(self.failed)} recording(s) were not "
                "imported. Reconnect it and run the import again: what is already in the library is skipped."
            )
        else:
            head = f"{len(self.failed)} recording(s) could not be imported:"
        details = [f"  {clip.original.name}: {reason}" for clip, reason in self.failed[:5]]
        if len(self.failed) > 5:
            details.append(f"  … and {len(self.failed) - 5} more")
        return "\n".join([head, *details])


def parse_dji_name(name: str) -> DjiName | None:
    """Split a DJI file name into its parts, or ``None`` if it is not one (or its date is impossible)."""
    match = _DJI_NAME.match(name)
    if not match:
        return None
    try:
        start = datetime.strptime(match["ts"], "%Y%m%d%H%M%S")
    except ValueError:
        return None
    if start.year < 2000:
        return None
    sub_index: int | None = None
    extra: list[str] = []
    for token in (t for t in match["rest"].split("_") if t):
        if sub_index is None and re.fullmatch(r"\d{3}", token):
            sub_index = int(token)  # burst photo number or loop-recording chapter
        else:
            extra.append(token)  # the user's custom file-name suffix
    return DjiName(match["prefix"].upper(), start, int(match["seq"]), sub_index, "_".join(extra) or None)


def resolve_creation_time(creation_ts: float, duration: float, mtime: float) -> float:
    """Decide whether a container ``creation_time`` is really UTC.

    ``creation_ts`` is the tag read as labelled (UTC).  Cameras without a time-zone
    setting write their local wall clock there instead.  The file's modification time
    (the camera's "recording stopped" moment) is stored correctly either way, so
    ``mtime - duration`` tells which reading describes this file.  When it supports
    neither (the file was copied without its times), the label is believed.
    """
    try:
        as_local = datetime.fromtimestamp(creation_ts, UTC).replace(tzinfo=None).timestamp()
    except (OverflowError, OSError, ValueError):
        return creation_ts
    if abs(as_local - creation_ts) < 60.0:
        return creation_ts  # this machine is on UTC: both readings are the same moment
    expected = mtime - max(0.0, duration)
    if abs(as_local - expected) <= _SAME_MOMENT_S < abs(creation_ts - expected):
        return as_local
    return creation_ts


# ---------------------------------------------------------------------------------
# Finding cards
# ---------------------------------------------------------------------------------


def _is_dir(path: Path) -> bool:
    """Like ``Path.is_dir`` but a refusal by the system (macOS privacy protection) is raised, not hidden."""
    try:
        return stat_module.S_ISDIR(os.stat(path).st_mode)
    except (FileNotFoundError, NotADirectoryError):
        return False


def _looks_like_camera_card(volume: Path) -> bool:
    """``DCIM`` holding a DJI-style folder (``DJI_001``, ``CAM_001`` …) or DJI-named files."""
    dcim = volume / "DCIM"
    if not _is_dir(dcim):
        return False
    for folder in sorted(dcim.iterdir()):
        if folder.name.startswith(".") or not folder.is_dir():
            continue
        if _DJI_FOLDER.match(folder.name):
            return True
        with os.scandir(folder) as entries:
            for count, entry in enumerate(entries):
                if parse_dji_name(entry.name) is not None:
                    return True
                if count >= 200:
                    break
    return False


def _is_system_volume(volume: Path) -> bool:
    if volume.is_symlink() or volume.name.casefold() in _SYSTEM_VOLUMES:
        return True  # "/Volumes/Macintosh HD" is a symlink to "/"
    try:
        return os.path.samefile(volume, "/")
    except OSError:
        return False


_MOUNT_LINE = re.compile(r"^.+? on (/.*) \(([^,)]+)[,)]")


def parse_mount_table(text: str) -> dict[str, str]:
    """``{mount point: file-system type}`` from the output of ``mount`` (macOS / BSD format)."""
    table: dict[str, str] = {}
    for line in text.splitlines():
        match = _MOUNT_LINE.match(line)
        if match:
            table[match.group(1)] = match.group(2).strip().lower()
    return table


def _network_mount_points() -> set[str]:
    """Mount points of network shares (macOS only; empty when ``mount`` cannot be asked)."""
    if not is_macos():
        return set()
    try:
        proc = subprocess.run(["mount"], capture_output=True, text=True, errors="replace", timeout=5.0)
    except (OSError, subprocess.SubprocessError):
        return set()
    return {point for point, kind in parse_mount_table(proc.stdout).items() if kind in NETWORK_FILESYSTEMS}


def find_camera_volumes() -> list[Path]:
    """Mounted volumes that look like the camera's card (or its built-in storage).

    Looks at ``/Volumes/*`` on macOS plus the sub-folders of every folder listed in
    ``$VIDEONOTES_VOLUME_ROOTS``.  A card is recognised by its content, never by its
    label (cards are often "Untitled").  The system volume is never returned, and
    network shares are not even looked into (an unreachable one would hang the search).
    Raises :class:`~videonotes.capture.CaptureError` when no card was found *and* macOS
    refused access to a volume, because that refusal is then the likely reason.
    """
    roots = [Path("/Volumes")] if is_macos() else []
    extra = [Path(p).expanduser() for p in os.environ.get(ENV_VOLUME_ROOTS, "").split(os.pathsep) if p.strip()]
    remote = _network_mount_points()
    found: list[Path] = []
    blocked: list[Path] = []
    for root in roots + extra:
        candidates: list[Path] = []
        try:
            if root in extra and (root / "DCIM").is_dir():
                candidates.append(root)  # the root itself is a card
            candidates += sorted(p for p in root.iterdir() if not p.name.startswith("."))
        except OSError as exc:
            log.debug("cannot list %s: %s", root, exc)
            continue
        for volume in candidates:
            if str(volume) in remote:
                log.debug("not looking into the network share %s", volume)
                continue
            try:
                if _is_system_volume(volume) or not _is_dir(volume):
                    continue
                if _looks_like_camera_card(volume) and volume not in found:
                    found.append(volume)
            except PermissionError as exc:
                # macOS privacy protection answers EPERM ("Operation not permitted"); an ordinary
                # permission problem (EACCES) on some other disk is nobody's camera card.
                if exc.errno == errno.EPERM:
                    blocked.append(volume)
                else:
                    log.debug("cannot inspect %s: %s", volume, exc)
            except OSError as exc:
                log.debug("cannot inspect %s: %s", volume, exc)
    if blocked:
        names = ", ".join(str(v) for v in blocked)
        if not found:
            raise CaptureError(
                f"No camera card could be read. Is it {names}? {REMOVABLE_VOLUME_HELP} "
                "(If the camera is not connected yet: plug it in with USB-C and choose the file transfer "
                "option on its screen.)"
            )
        log.warning("could not look at %s: %s", names, REMOVABLE_VOLUME_HELP)
    return found


# ---------------------------------------------------------------------------------
# Scanning
# ---------------------------------------------------------------------------------


def _walk(start: Path) -> list[tuple[Path, list[os.DirEntry[str]]]]:
    """``(folder, files)`` for ``start`` and its sub-folders, in a stable order."""
    result: list[tuple[Path, list[os.DirEntry[str]]]] = []
    pending: list[tuple[Path, int]] = [(start, 0)]
    while pending:
        folder, depth = pending.pop(0)
        try:
            with os.scandir(folder) as scan:
                entries = sorted(scan, key=lambda e: e.name)
        except PermissionError:
            if folder == start:
                raise
            log.warning("skipping %s: no permission to read it", folder)
            continue
        except OSError as exc:
            if folder == start:
                raise
            log.warning("skipping %s: %s", folder, exc)
            continue
        files: list[os.DirEntry[str]] = []
        for entry in entries:
            if entry.name.startswith("."):  # "._" AppleDouble litter, .Spotlight-V100, .Trashes …
                continue
            try:
                if entry.is_dir(follow_symlinks=False):
                    if depth < MAX_SCAN_DEPTH and entry.name.casefold() not in _SKIP_DIRS:
                        pending.append((Path(entry.path), depth + 1))
                elif entry.is_file():
                    files.append(entry)
            except OSError:
                continue
        result.append((folder, files))
    return result


def _start_from_media(path: Path, mtime: float) -> tuple[float, str, float] | None:
    """``(start_ts, source, duration)`` of a file without a time in its name; None if unreadable."""
    try:
        info = ff.probe(path)
    except ff.FFmpegError as exc:
        log.warning("skipping %s: not a readable media file (%s)", path.name, str(exc).splitlines()[0])
        return None
    if not _is_footage(info):
        return None
    if info.creation_ts is not None:
        return resolve_creation_time(info.creation_ts, info.duration, mtime), "creation_time", info.duration
    return mtime - info.duration, "mtime", info.duration


def scan_card(root: Path) -> list[CardClip]:
    """Every recording under ``root``, oldest first.

    ``root`` may be a camera volume (only its ``DCIM`` tree is read), a copy of one, or
    any folder of video files (sub-folders up to :data:`MAX_SCAN_DEPTH` deep).  Each main
    video is paired with its ``.LRF`` / ``.XRF`` proxy when one lies next to it; a proxy
    whose main file is missing is returned on its own.  Still photos named by the camera
    are included as clips of duration 0 so their text can be read at full resolution.
    Ignored: hidden and ``._`` files, empty files, raw ``.DNG`` photos, ``.WAV`` audio
    backups, the ``MISC/THM`` thumbnail tree, photos not named by the camera, and
    anything ffmpeg cannot read.
    """
    root = Path(root).expanduser()
    try:
        if not _is_dir(root):
            raise CaptureError(f"{root} is not a folder (is the card still connected?)")
        start = root / "DCIM" if _is_dir(root / "DCIM") else root
        tree = _walk(start)
    except PermissionError as exc:
        if exc.errno == errno.EPERM:  # macOS privacy protection, not ordinary file permissions
            raise CaptureError(f"Cannot read {root}: {REMOVABLE_VOLUME_HELP}") from exc
        raise CaptureError(f"Cannot read {root}: your user account has no permission to open it.") from exc
    except OSError as exc:
        raise CaptureError(f"Cannot read {root}: {exc.strerror or exc}. Is the card still connected?") from exc

    clips: list[CardClip] = []
    for folder, entries in tree:
        mains: list[tuple[str, Path, os.stat_result]] = []
        proxies: dict[str, tuple[Path, os.stat_result]] = {}
        for entry in entries:
            suffix = os.path.splitext(entry.name)[1].lower()
            if suffix not in VIDEO_SUFFIXES and suffix not in PROXY_SUFFIXES and suffix not in PHOTO_SUFFIXES:
                continue
            try:
                stat = entry.stat()
            except OSError:
                continue
            if stat.st_size <= 0:
                continue
            path = folder / entry.name
            stem = os.path.splitext(entry.name)[0].casefold()
            if suffix in PROXY_SUFFIXES:
                proxies.setdefault(stem, (path, stat))
            elif suffix in PHOTO_SUFFIXES:
                if parse_dji_name(entry.name) is not None:  # only the camera's own photos
                    mains.append((stem, path, stat))
            else:
                mains.append((stem, path, stat))
        # .MP4 before other containers, so that it is the one paired with a proxy of the same name
        mains.sort(key=lambda m: (m[0], m[1].suffix.lower() != ".mp4", m[1].name))
        for stem, path, stat in mains:
            proxy = None
            if path.suffix.lower() not in PHOTO_SUFFIXES and stem in proxies:
                proxy = proxies.pop(stem)[0]
            clip = _make_clip(path, proxy, stat)
            if clip is not None:
                clips.append(clip)
        for path, stat in proxies.values():  # proxies whose main file is gone still show the recording
            clip = _make_clip(path, None, stat)
            if clip is not None:
                clips.append(clip)
    clips.sort(key=lambda c: (c.start_ts, c.index if c.index is not None else -1, c.original.name))
    return clips


def _make_clip(path: Path, proxy: Path | None, stat: os.stat_result) -> CardClip | None:
    named = parse_dji_name(path.name)
    is_photo = path.suffix.lower() in IMAGE_SUFFIXES
    if named is not None:
        try:
            start_ts = named.start_ts
        except (OverflowError, OSError, ValueError):
            named = None
    if named is not None:
        return CardClip(
            original=path, proxy=proxy, start_ts=start_ts, size=stat.st_size, index=named.index,
            duration=0.0 if is_photo else None, time_source="name",
        )  # fmt: skip
    resolved = _start_from_media(proxy or path, stat.st_mtime)
    if resolved is None:
        return None
    start_ts, source, duration = resolved
    return CardClip(
        original=path, proxy=proxy, start_ts=start_ts, size=stat.st_size, index=None,
        duration=0.0 if is_photo else duration, time_source=source,
    )  # fmt: skip


# ---------------------------------------------------------------------------------
# Sessions and identity
# ---------------------------------------------------------------------------------


def _ensure_duration(clip: CardClip) -> float:
    """Length of a clip in seconds, probing once (the small proxy first) and remembering it."""
    if clip.duration is not None:
        return clip.duration
    if clip.is_photo:
        clip.duration = 0.0
        return 0.0
    candidates = [clip.proxy, clip.original] if clip.proxy is not None else [clip.original]
    for candidate in candidates:
        try:
            clip.duration = max(0.0, ff.probe(candidate).duration)
            return clip.duration
        except ff.FFmpegError as exc:
            log.debug("cannot read the length of %s: %s", candidate.name, str(exc).splitlines()[0])
    clip.duration = 0.0
    return 0.0


def group_into_sessions(clips: list[CardClip], gap_seconds: float) -> list[list[CardClip]]:
    """Group recordings made close together into sessions (lists of clips, oldest first).

    A clip joins the running session when it starts less than ``gap_seconds`` after that
    session's last clip *ended*; the parts a long recording is split into therefore stay
    together however long each part is, and a photo joins the session it falls into.
    Clip lengths are only probed when the start times alone do not settle it (and the
    small proxy is probed rather than the multi-gigabyte main file); they are remembered
    on the clips.
    """
    ordered = sorted(clips, key=lambda c: (c.start_ts, c.index if c.index is not None else -1, c.original.name))
    sessions: list[list[CardClip]] = []
    session_end = 0.0  # latest known end time in the running session
    exact_end = True  # False while session_end is a lower bound (some lengths not probed yet)
    for clip in ordered:
        if sessions:
            current = sessions[-1]
            joins = clip.start_ts - session_end < gap_seconds
            if not joins and not exact_end:
                session_end = max(c.start_ts + _ensure_duration(c) for c in current)
                exact_end = True
                joins = clip.start_ts - session_end < gap_seconds
            if joins:
                current.append(clip)
            else:
                sessions.append([clip])
                session_end, exact_end = clip.start_ts, True
        else:
            sessions.append([clip])
            session_end, exact_end = clip.start_ts, True
        if clip.duration is not None:
            session_end = max(session_end, clip.start_ts + clip.duration)
        else:
            session_end = max(session_end, clip.start_ts)
            exact_end = False
    return sessions


_fingerprints: dict[tuple[str, int, int], str] = {}


def clip_fingerprint(path: Path) -> str:
    """A stable identity for a media file: its name, its size and a hash of its first and last megabyte.

    The same recording gets the same fingerprint after the card is re-mounted under
    another name or the file is copied elsewhere, and it takes milliseconds on a 16 GB
    file because only two megabytes are read.  Raises
    :class:`~videonotes.capture.CaptureError` when the file cannot be read.
    """
    path = Path(path)
    try:
        stat = path.stat()
        key = (str(path), stat.st_size, stat.st_mtime_ns)
        cached = _fingerprints.get(key)
        if cached is not None:
            return cached
        digest = hashlib.sha256()
        digest.update(unicodedata.normalize("NFC", path.name).encode("utf-8", "surrogateescape"))
        digest.update(b"\0%d\0" % stat.st_size)
        with open(path, "rb") as handle:
            head = handle.read(_FINGERPRINT_CHUNK)
            digest.update(head)
            tail_start = max(len(head), stat.st_size - _FINGERPRINT_CHUNK)
            if tail_start < stat.st_size:
                handle.seek(tail_start)
                digest.update(handle.read(_FINGERPRINT_CHUNK))
    except OSError as exc:
        raise CaptureError(
            f"Cannot read {path}: {exc.strerror or exc}. Is the card or folder still connected?"
        ) from exc
    if len(_fingerprints) > 20000:
        _fingerprints.clear()
    value = digest.hexdigest()[:40]
    _fingerprints[key] = value
    return value


# ---------------------------------------------------------------------------------
# Copying
# ---------------------------------------------------------------------------------


def _copy_file(src: Path, dst: Path) -> None:
    """Copy ``src`` to ``dst`` via a temporary name, verifying the size. ``src`` is only read."""
    size = src.stat().st_size
    with contextlib.suppress(OSError):
        if dst.is_file() and dst.stat().st_size == size:
            return  # finished by an earlier, interrupted import
    tmp = dst.with_name(dst.name + ".part")
    try:
        with open(src, "rb") as fin, open(tmp, "wb") as fout:
            while chunk := fin.read(_COPY_CHUNK):
                fout.write(chunk)
            fout.flush()
            os.fsync(fout.fileno())
        copied = tmp.stat().st_size
        if copied != size:
            raise OSError(errno.EIO, f"only {copied} of {size} bytes arrived")
        with contextlib.suppress(OSError):
            source_stat = src.stat()
            os.utime(tmp, (source_stat.st_atime, source_stat.st_mtime))
        os.replace(tmp, dst)
    except BaseException:
        with contextlib.suppress(OSError):
            tmp.unlink()
        raise


def merge_args(video_src: Path, audio_src: Path, dst: Path) -> list[str]:
    """ffmpeg arguments (for :func:`videonotes.media.ffmpeg.run`) that write ``dst`` as an MP4
    with the first real video stream of ``video_src`` and the first audio stream of
    ``audio_src``, both copied bit for bit.

    ``0:V:0`` skips cover pictures; naming the streams also keeps the camera's data
    tracks (``djmd``, ``dbgi``, ``tmcd``) out, which the MP4 muxer would refuse.  Because
    only the audio stream of ``audio_src`` is mapped, ffmpeg marks its other streams as
    discarded and the MP4 demuxer never reads their samples: it seeks from one audio
    chunk to the next, so a multi-gigabyte main file costs a small fraction of its size
    in reads (measured: 1.9 MB read from a 24.6 MB file whose audio is 64 KB).
    """
    return [
        "-i", str(video_src),
        "-i", str(audio_src),
        "-map", "0:V:0",
        "-map", "1:a:0",
        "-c", "copy",
        "-f", "mp4",
        str(dst),
    ]  # fmt: skip


def _merge_proxy_audio(proxy: Path, main: Path, dst: Path) -> bool:
    """Write ``dst`` = proxy video + main audio. False (and no file) if ffmpeg cannot do it."""
    with contextlib.suppress(OSError):
        if dst.is_file() and dst.stat().st_size > 0:
            return True  # finished by an earlier, interrupted import (written atomically)
    tmp = dst.with_name(dst.name + ".part")
    try:
        timeout = 600.0 + main.stat().st_size / 2_000_000  # generous: bounded by a 2 MB/s card
        ff.run(merge_args(proxy, main, tmp), timeout=timeout)
        merged = ff.probe(tmp)
        if not (merged.has_video and merged.has_audio):
            raise ff.FFmpegError("the merged file lacks a video or an audio stream")
        os.replace(tmp, dst)
        return True
    except ff.FFmpegError as exc:
        log.warning(
            "could not combine %s with the sound of %s (%s); the sound will be read from the original instead",
            proxy.name, main.name, str(exc).splitlines()[0],
        )  # fmt: skip
        return False
    finally:
        with contextlib.suppress(OSError):
            tmp.unlink()


#: ffmpeg "plays" plain text and ANSI art as video; that is not footage.
_TEXT_ART_CODECS = frozenset({"ansi", "bintext", "xbin", "idf"})


def _is_footage(info: ff.MediaInfo) -> bool:
    """True if a probed file holds real video, audio or a picture (not text rendered by ffmpeg)."""
    if info.has_video and info.video_codec in _TEXT_ART_CODECS:
        return info.has_audio
    return info.has_video or info.has_audio


def _is_mp4_family(info: ff.MediaInfo) -> bool:
    name = str((info.raw.get("format") or {}).get("format_name", ""))
    if not name:  # probed without ffprobe: only ffmpeg's banner is available
        banner = re.search(r"Input #0, ([^ ]+), from", str(info.raw.get("banner", "")))
        name = banner.group(1) if banner else ""
    return "mp4" in name or "mov" in name


# ---------------------------------------------------------------------------------
# Importing
# ---------------------------------------------------------------------------------


@dataclass
class _Plan:
    """One session about to be imported."""

    session_id: str
    dest: Path
    items: list[tuple[CardClip, str]]  # (clip, fingerprint)
    names: dict[str, Path] = field(default_factory=dict)  # file name in dest -> the source it belongs to

    def target(self, name: str, source: Path) -> Path:
        """Where ``source`` goes in the session folder; a second file of the same name gets a number."""
        stem, suffix = os.path.splitext(name)
        candidate, number = name, 1
        while self.names.get(candidate.casefold(), source) != source:
            number += 1
            candidate = f"{stem}-{number}{suffix}"
        self.names[candidate.casefold()] = source
        return self.dest / candidate


def _effective_proxy(settings: Settings, clip: CardClip) -> Path | None:
    return clip.proxy if settings.imports.prefer_proxy else None


def _session_id_for(settings: Settings, store: Store, started_ts: float, taken: set[str]) -> str:
    """A new session id, or the id of a media folder an interrupted import left behind.

    Media is copied before the session is recorded in the library, so a crash or a pulled
    card can leave ``media/<id>/`` without a session.  Running the import again finds that
    folder by its time prefix and carries on in it instead of copying everything twice.
    """
    fresh = new_session_id(started_ts)
    prefix = fresh.rsplit("-", 1)[0]
    with contextlib.suppress(OSError):
        for folder in sorted(settings.media_dir.glob(f"{prefix}-*")):
            if folder.is_dir() and folder.name not in taken and store.get_session(folder.name) is None:
                log.info("continuing the interrupted import in %s", folder)
                return folder.name
    return fresh


def _copy_estimate(settings: Settings, clip: CardClip, dest: Path, mode: str) -> int:
    """Bytes the import of ``clip`` will add to the library (0 for what is already there)."""
    if mode == "none":
        return 0
    proxy = _effective_proxy(settings, clip)
    wanted: list[tuple[Path, Path]] = []
    if mode == "original" or proxy is None:
        wanted.append((clip.original, dest / clip.original.name))
    if proxy is not None:
        wanted.append((proxy, dest / _proxy_name(clip)))
    total = 0
    for src, dst in wanted:
        with contextlib.suppress(OSError):
            size = src.stat().st_size
            if dst.is_file() and dst.stat().st_size >= size:
                continue  # already copied by an interrupted import
            total += size
            if src is proxy:
                total += size // 10  # a silent proxy gains the main file's audio track
    return total


def _proxy_name(clip: CardClip) -> str:
    return f"{clip.original.stem}_proxy.mp4"


def _check_free_space(settings: Settings, needed: int) -> None:
    if needed <= 0:
        return
    try:
        free = shutil.disk_usage(settings.media_dir).free
    except OSError as exc:
        raise CaptureError(f"Cannot use the library folder {settings.media_dir}: {exc.strerror or exc}") from exc
    required = needed + max(_SPACE_RESERVE, needed // 50)
    if free < required:
        gib = 1024**3
        raise CaptureError(
            f"Not enough free disk space for this import: it needs about {required / gib:.1f} GB, but only "
            f"{free / gib:.1f} GB are free where the library lives ({settings.home}). Free up some space, or "
            "import without copying anything:  vnote --set import.copy_media=none import  "
            "(keep the card connected until the notes are written)."
        )


def _ingest(settings: Settings, clip: CardClip, fingerprint: str, plan: _Plan, mode: str) -> Clip:
    """Bring one recording into the library folder (per ``mode``) and describe it as a Clip."""
    proxy = _effective_proxy(settings, clip)
    info: ff.MediaInfo | None = None
    if proxy is not None:
        try:
            info = ff.probe(proxy)
            if not info.has_video:
                raise ff.FFmpegError(f"{proxy.name} has no video")
        except ff.FFmpegError as exc:
            # A damaged proxy must not cost the recording: use the original as if there were none.
            log.warning("ignoring the unreadable proxy %s (%s)", proxy.name, str(exc).splitlines()[0].rstrip(":"))
            proxy, info = None, None
    analysed_src = proxy or clip.original
    if info is None:
        info = ff.probe(analysed_src)
    if not _is_footage(info):
        raise ff.FFmpegError(f"{analysed_src.name} has neither video nor audio")
    original_has_audio = False
    if proxy is not None and not info.has_audio:
        with contextlib.suppress(ff.FFmpegError):
            original_has_audio = ff.probe(clip.original).has_audio
    has_audio = info.has_audio or original_has_audio

    path: Path
    original_path: Path | None
    if mode == "none":
        path, original_path = analysed_src, (clip.original if proxy is not None else None)
    else:
        plan.dest.mkdir(parents=True, exist_ok=True)
        if proxy is None:
            path, original_path = plan.target(clip.original.name, clip.original), None
            _copy_file(clip.original, path)
        else:
            path = plan.target(_proxy_name(clip) if _is_mp4_family(info) else proxy.name, proxy)
            if mode == "original":
                original_path = plan.target(clip.original.name, clip.original)
                _copy_file(clip.original, original_path)
                _copy_file(proxy, path)
            else:
                original_path = clip.original  # stays on the card; stills are cut from it while it is connected
                # Never lose the sound: a silent proxy gets the main file's audio track muxed in.
                if not (original_has_audio and _merge_proxy_audio(proxy, clip.original, path)):
                    _copy_file(proxy, path)

    clip.duration = 0.0 if clip.is_photo else max(0.0, info.duration)
    return Clip(
        session_id=plan.session_id,
        path=settings.rel(path),
        fingerprint=fingerprint,
        start_ts=clip.start_ts,
        duration=clip.duration,
        original_path=settings.rel(original_path) if original_path is not None else None,
        width=info.width,
        height=info.height,
        fps=None if clip.is_photo else info.fps,
        has_audio=has_audio,
        has_video=info.has_video,
    )


def _source_is_gone(clip: CardClip) -> bool:
    try:
        return not clip.original.parent.is_dir()
    except OSError:
        return True


def import_with_report(
    settings: Settings, store: Store, clips: list[CardClip], *, source: str, kind: str = "import"
) -> ImportReport:
    """Import ``clips`` and say exactly what happened to each (see :func:`import_clips`).

    Raises :class:`~videonotes.capture.CaptureError` only when the import cannot start
    (unknown ``copy_media`` value, not enough disk space, library folder unusable);
    per-recording problems are returned in the report.
    """
    mode = str(settings.imports.copy_media).strip().lower()
    if mode not in COPY_MODES:
        raise CaptureError(
            f"import.copy_media must be one of {', '.join(COPY_MODES)}; it is {settings.imports.copy_media!r}"
        )
    report = ImportReport()

    fresh: list[tuple[CardClip, str]] = []
    seen: set[str] = set()
    for clip in clips:
        try:
            fingerprint = clip_fingerprint(clip.original)
        except CaptureError as exc:
            report.failed.append((clip, str(exc)))
            continue
        if fingerprint in seen:
            continue  # the same file listed twice
        seen.add(fingerprint)
        if store.clip_by_fingerprint(fingerprint) is not None:
            log.info("already in the library, skipping: %s", clip.original.name)
            report.skipped.append(clip)
        else:
            fresh.append((clip, fingerprint))

    fingerprint_of = {id(clip): fp for clip, fp in fresh}
    plans: list[_Plan] = []
    taken: set[str] = set()
    for group in group_into_sessions([clip for clip, _ in fresh], float(settings.imports.session_gap_seconds)):
        session_id = _session_id_for(settings, store, min(c.start_ts for c in group), taken)
        taken.add(session_id)
        plans.append(_Plan(session_id, settings.media_dir / session_id, [(c, fingerprint_of[id(c)]) for c in group]))

    if mode != "none":
        try:
            settings.media_dir.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise CaptureError(f"Cannot use the library folder {settings.media_dir}: {exc.strerror or exc}") from exc
        _check_free_space(
            settings, sum(_copy_estimate(settings, clip, plan.dest, mode) for plan in plans for clip, _ in plan.items)
        )

    for number, plan in enumerate(plans):
        if report.source_lost:
            report.failed += [(clip, "the card or folder was no longer there") for clip, _ in plan.items]
            continue
        rows: list[tuple[CardClip, Clip]] = []
        for position, (clip, fingerprint) in enumerate(plan.items):
            try:
                log.info("importing %s (%d of %d in session %d of %d)",
                         clip.original.name, position + 1, len(plan.items), number + 1, len(plans))  # fmt: skip
                rows.append((clip, _ingest(settings, clip, fingerprint, plan, mode)))
            except (OSError, ff.FFmpegError) as exc:
                reason = (getattr(exc, "strerror", None) or str(exc)).splitlines()[0].rstrip(":")
                if isinstance(exc, ff.FFmpegError):
                    reason = (
                        f"it is damaged or not a media file ({reason.replace(str(clip.original.parent) + os.sep, '')})"
                    )
                if _source_is_gone(clip):
                    # Keep what was copied: the next run continues in the same folder.
                    report.source_lost = True
                    remaining = plan.items[position:]
                    report.failed += [(c, "the card or folder was no longer there") for c, _ in remaining]
                    report.failed += [
                        (c, "its session was interrupted; it will be imported with the rest") for c, _ in rows
                    ]
                    rows = []
                    break
                log.warning("could not import %s: %s", clip.original.name, reason)
                report.failed.append((clip, reason))
        if not rows:
            with contextlib.suppress(OSError):
                plan.dest.rmdir()  # only succeeds when nothing was copied into it
            continue
        session = Session(
            id=plan.session_id,
            kind=kind,
            started_ts=min(row.start_ts for _, row in rows),
            ended_ts=max(row.end_ts for _, row in rows),
            source=source,
            status="open",
        )
        try:
            with store.tx():
                store.create_session(session)
                for _, row in rows:
                    store.add_clip(row)
        except sqlite3.IntegrityError as exc:
            log.warning("session %s was not recorded: %s", plan.session_id, exc)
            report.failed += [(clip, "it is already in the library (another import running?)") for clip, _ in rows]
            continue
        report.sessions.append(session)
        report.imported += [clip for clip, _ in rows]

    if report.failed:
        log.warning("%s", report.failure_summary())
    return report


def import_clips(
    settings: Settings, store: Store, clips: list[CardClip], *, source: str, kind: str = "import"
) -> list[Session]:
    """Create sessions + clips (copying media per imports.copy_media); skips known fingerprints.

    For every recording whose fingerprint is not in the library yet:

    * ``copy_media = "proxy"`` copies the low-res proxy (the original when there is no
      proxy) into ``<home>/media/<session>/``.  A proxy without sound whose original has
      sound is written as one file with the proxy's picture and the original's audio.
    * ``"original"`` copies the original (and its proxy, which stays the file analysed).
    * ``"none"`` copies nothing and analyses the files where they are.

    ``Clip.path`` is the file to analyse (the proxy when ``imports.prefer_proxy`` and one
    exists), ``Clip.original_path`` the full-quality file.  Copies go through a temporary
    name and are checked for size; the source is only ever read.  Free disk space is
    checked first.  Recordings close together in time become one session.  Running the
    same import again is safe: known recordings are skipped, and one that was interrupted
    carries on where it stopped.

    Returns the new sessions (oldest first).  Recordings that could not be imported are
    logged; if *nothing* could be imported although something failed, raises
    :class:`~videonotes.capture.CaptureError` with the reasons.
    """
    report = import_with_report(settings, store, clips, source=source, kind=kind)
    if report.failed and not report.sessions:
        raise CaptureError(report.failure_summary())
    return report.sessions


def _proxy_sibling(path: Path) -> Path | None:
    for suffix in sorted(PROXY_SUFFIXES):
        for candidate in (path.with_suffix(suffix.upper()), path.with_suffix(suffix)):
            with contextlib.suppress(OSError):
                if candidate != path and candidate.is_file() and candidate.stat().st_size > 0:
                    return candidate
    return None


def import_file(settings: Settings, store: Store, path: Path, *, start_ts: float | None = None) -> Session:
    """Add one media file (video, audio or picture) as a session of its own (kind ``"file"``).

    The start time is ``start_ts`` when given; otherwise the time in a DJI file name, else
    the container's creation time, else the file's modification time (minus its length).
    A camera original with its ``.LRF`` proxy next to it is analysed through the proxy,
    as on import.  Importing the same file again returns the session it already has.
    """
    path = Path(path).expanduser()
    if not path.is_file():
        raise CaptureError(f"No such file: {path}")
    try:
        stat = path.stat()
    except OSError as exc:
        raise CaptureError(f"Cannot read {path}: {exc.strerror or exc}") from exc
    if stat.st_size <= 0:
        raise CaptureError(f"{path.name} is empty (0 bytes); there is nothing to import.")

    fingerprint = clip_fingerprint(path)
    existing = store.clip_by_fingerprint(fingerprint)
    if existing is not None:
        session = store.get_session(existing.session_id)
        if session is not None:
            log.info("%s is already in the library (session %s)", path.name, session.id)
            return session

    suffix = path.suffix.lower()
    proxy = _proxy_sibling(path) if suffix in VIDEO_SUFFIXES else None
    try:
        info = ff.probe(proxy or path)
    except ff.FFmpegError as exc:
        raise CaptureError(f"{path.name} is not a video, audio or picture file that ffmpeg can read.") from exc
    if not _is_footage(info):
        raise CaptureError(f"{path.name} is not a video, audio or picture file (it contains no footage).")
    is_photo = suffix in IMAGE_SUFFIXES
    duration = 0.0 if is_photo else max(0.0, info.duration)
    named = parse_dji_name(path.name)
    if start_ts is not None:
        start, source = float(start_ts), "given"
    elif named is not None:
        start, source = named.start_ts, "name"
    elif info.creation_ts is not None:
        start, source = resolve_creation_time(info.creation_ts, info.duration, stat.st_mtime), "creation_time"
    else:
        start, source = stat.st_mtime - duration, "mtime"
    clip = CardClip(
        original=path, proxy=proxy, start_ts=start, size=stat.st_size,
        index=named.index if named is not None else None, duration=duration, time_source=source,
    )  # fmt: skip
    report = import_with_report(settings, store, [clip], source=str(path), kind="file")
    if report.sessions:
        return report.sessions[0]
    reason = report.failed[0][1] if report.failed else "it is already in the library"
    raise CaptureError(f"Could not add {path.name}: {reason}")
