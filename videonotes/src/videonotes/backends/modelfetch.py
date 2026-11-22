"""Downloading and unpacking model archives (standard library only).

Some backends keep their model files under ``<home>/models`` and fetch them
from a plain HTTPS URL on first use (the sherpa-onnx speech models are GitHub
release assets, for example).  This module does that one job carefully:

* **streaming, resumable download** — the archive goes to
  ``<dest_dir>/.downloads/<name>.part``; an interrupted download (Wi-Fi drop,
  Ctrl-C, laptop lid) continues from where it stopped, using HTTP ``Range``
  with ``If-Range`` so a file that changed on the server is fetched afresh;
* **timeouts** — a connection that delivers nothing for ``timeout`` seconds is
  dropped and retried; there is deliberately no limit on the total time,
  because half a gigabyte over hotel Wi-Fi is slow but fine;
* **safe extraction** of ``.tar.bz2`` / ``.tar.gz`` / ``.tar.xz`` / ``.tar`` /
  ``.zip`` — every member is checked before anything is written: no absolute
  paths, no ``..``, no device files, no writing *through* a symlink, and a
  symlink may only point at or below its own folder (with no way to say "up",
  no chain of links can lead out of the destination);
* **never a half-unpacked model** — the archive is unpacked into a hidden
  staging directory, moved into place with a rename, and only then is the
  completion marker ``<dest_dir>/.<archive name>.complete`` written.
  :func:`is_fetched` (and the fast path of :func:`fetch_archive`) trust
  nothing without that marker;
* **errors a person can act on** — every failure is a :class:`ModelFetchError`
  whose message names the URL, the folder, and the by-hand alternative
  (download the file in a browser and unpack it into the folder).

Proxies are honoured the standard way (``HTTPS_PROXY`` / ``HTTP_PROXY`` /
``NO_PROXY``, and the macOS system proxy settings), because ``urllib`` does
that by default.
"""

from __future__ import annotations

import contextlib
import json
import logging
import os
import posixpath
import shutil
import stat
import tarfile
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from collections.abc import Callable, Iterator
from http.client import HTTPException, HTTPMessage
from pathlib import Path
from typing import IO, Any

log = logging.getLogger("videonotes.modelfetch")

_ARCHIVE_ERRORS: tuple[type[BaseException], ...] = (tarfile.TarError, zipfile.BadZipFile, EOFError)
try:  # both are optional parts of a Python build
    import zlib

    _ARCHIVE_ERRORS += (zlib.error,)
except ImportError:  # pragma: no cover
    pass
try:
    import lzma

    _ARCHIVE_ERRORS += (lzma.LZMAError,)
except ImportError:  # pragma: no cover
    pass

#: ``progress(bytes_done, bytes_total)``; ``bytes_total`` is None when the server does not say.
ProgressFn = Callable[[int, int | None], None]

DEFAULT_TIMEOUT = 30.0  # seconds a connection may stay silent before it is dropped
DEFAULT_RETRIES = 4  # consecutive attempts that made no progress before giving up
#: Refuse to unpack more than this (a corrupt or hostile archive must not fill the disk).
MAX_UNPACKED_BYTES = 16 * 1024**3
_CHUNK = 256 * 1024
_USER_AGENT = "videonotes-modelfetch"
_DOWNLOADS_DIR = ".downloads"
_STAGING_PREFIX = ".unpack-"
_ARCHIVE_SUFFIXES = {
    ".tar.bz2": "tar",
    ".tbz2": "tar",
    ".tbz": "tar",
    ".tar.gz": "tar",
    ".tgz": "tar",
    ".tar.xz": "tar",
    ".txz": "tar",
    ".tar": "tar",
    ".zip": "zip",
}
#: HTTP statuses worth another attempt (the rest of 4xx will not get better by retrying).
_RETRY_STATUSES = frozenset({408, 425, 429, 500, 502, 503, 504})


class ModelFetchError(RuntimeError):
    """A model archive could not be downloaded or unpacked.

    ``str(exc)`` is written for the person at the keyboard: it says what went
    wrong, which URL was involved and how to install the files by hand.
    """

    def __init__(self, message: str, *, url: str = "", dest_dir: Path | None = None):
        super().__init__(message)
        self.url = url
        self.dest_dir = dest_dir


class UnsafeArchiveError(ModelFetchError):
    """The archive contains an entry that would be written outside the destination."""


class _UnpackIOError(ModelFetchError):
    """Unpacking failed because of the local disk (full, read-only, …), not because of the archive."""


class _Restart(Exception):
    """The partial file cannot be continued; start again from byte 0."""


class _LocalIOError(Exception):
    """Writing the download to disk failed (as opposed to reading it from the network)."""


# -- names, markers ---------------------------------------------------------------------


def archive_name(url: str) -> str:
    """File name of the archive a URL points at (``…/model.tar.bz2?x=1`` -> ``model.tar.bz2``)."""
    path = urllib.parse.urlsplit(url).path
    name = posixpath.basename(urllib.parse.unquote(path.rstrip("/")))
    name = name.replace("\\", "_").replace("/", "_").lstrip(".")
    if not name:
        raise ValueError(f"cannot tell the file name from the URL {url!r}")
    return name


def archive_kind(name: str | Path) -> str | None:
    """``"tar"``, ``"zip"`` or None, judged by the file name."""
    lower = str(name).lower()
    for suffix, kind in _ARCHIVE_SUFFIXES.items():
        if lower.endswith(suffix):
            return kind
    return None


def marker_path(url: str, dest_dir: str | Path) -> Path:
    """Where the completion marker for ``url`` unpacked into ``dest_dir`` lives."""
    return Path(dest_dir) / f".{archive_name(url)}.complete"


def _fetched_members(url: str, dest: Path, expected_member: str | None) -> list[str] | None:
    """Top-level names a completed fetch of ``url`` put into ``dest``; None if it is not (or no longer) complete."""
    try:
        data = json.loads(marker_path(url, dest).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict) or data.get("url") != url or not isinstance(data.get("members"), list):
        return None
    members = [m for m in data["members"] if isinstance(m, str)]
    if not members or not all((dest / m).exists() for m in members):
        return None
    if expected_member is not None and not (dest / expected_member).exists():
        return None
    return members


def _result_path(dest: Path, members: list[str], expected_member: str | None) -> Path:
    if expected_member:
        return dest / expected_member
    return dest / members[0] if len(members) == 1 else dest


def is_fetched(url: str, dest_dir: str | Path, *, expected_member: str | None = None) -> bool:
    """True if :func:`fetch_archive` already completed for this URL and its files are still there."""
    return _fetched_members(url, Path(dest_dir).expanduser(), expected_member) is not None


def manual_instructions(url: str, dest_dir: str | Path, *, expected_member: str | None = None) -> str:
    """The by-hand alternative to :func:`fetch_archive`, as text for an error message."""
    dest = Path(dest_dir)
    name = archive_name(url)
    if archive_kind(name) == "zip":
        command = f'unzip ~/Downloads/{name} -d "{dest}"'
    else:
        command = f'tar -xf ~/Downloads/{name} -C "{dest}"'
    lines = [
        "To install it by hand instead, download",
        f"    {url}",
        "in a web browser, then unpack it into the models folder:",
        f'    mkdir -p "{dest}"',
        f"    {command}",
    ]
    if expected_member:
        lines.append(f"Afterwards this should exist:  {dest / expected_member}")
    return "\n".join(lines)


# -- download ---------------------------------------------------------------------------


def _describe_network_error(exc: BaseException, timeout: float) -> str:
    if isinstance(exc, urllib.error.HTTPError):
        return f"the server answered HTTP {exc.code} {exc.reason}"
    reason = exc.reason if isinstance(exc, urllib.error.URLError) else exc
    if isinstance(reason, TimeoutError) or "timed out" in str(reason).lower():
        return f"the connection stalled (no data for {timeout:.0f} s)"
    return f"network problem: {str(reason) or type(reason).__name__}"


def _parse_content_range(value: str | None) -> tuple[int | None, int | None]:
    """``bytes 100-199/1000`` -> (100, 1000); ``bytes */1000`` -> (None, 1000)."""
    if not value or not value.strip().lower().startswith("bytes"):
        return None, None
    span, _, total_text = value.strip()[5:].strip().partition("/")
    start: int | None = None
    if "-" in span:
        with contextlib.suppress(ValueError):
            start = int(span.split("-", 1)[0])
    try:
        return start, int(total_text)
    except ValueError:
        return start, None


def _validator(headers: HTTPMessage) -> str:
    """A strong ETag if there is one, else Last-Modified, else '' (resume is then unconditional)."""
    etag = (headers.get("ETag") or "").strip()
    if etag and not etag.startswith("W/"):
        return etag
    return (headers.get("Last-Modified") or "").strip()


def _require_free_space(folder: Path, needed: int, url: str) -> None:
    try:
        free = shutil.disk_usage(folder).free
    except OSError:
        return
    if free < needed:
        raise ModelFetchError(
            f"Not enough free disk space in {folder} to download and unpack {archive_name(url)}: "
            f"about {needed / 1e9:.1f} GB needed, {free / 1e9:.1f} GB free. Free some space and run the command again.",
            url=url,
            dest_dir=folder,
        )


def _attempt(
    url: str, part: Path, meta: Path, progress: ProgressFn | None, timeout: float
) -> tuple[bool, int, int | None]:
    """One HTTP request appending to ``part``. Returns (finished, bytes on disk, total or None)."""
    offset = part.stat().st_size if part.is_file() else 0
    saved: dict[str, Any] = {}
    if offset:
        try:
            saved = json.loads(meta.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            saved = {}
        if not isinstance(saved, dict) or saved.get("url") != url:
            # a partial file we know nothing about: never glue two different downloads together
            part.unlink(missing_ok=True)
            offset, saved = 0, {}
    headers = {"User-Agent": _USER_AGENT, "Accept-Encoding": "identity"}
    if offset:
        headers["Range"] = f"bytes={offset}-"
        if saved.get("validator"):
            headers["If-Range"] = str(saved["validator"])
    request = urllib.request.Request(url, headers=headers)
    try:
        response = urllib.request.urlopen(request, timeout=timeout)  # scheme was checked by the caller
    except urllib.error.HTTPError as exc:
        if exc.code == 416 and offset:  # "range not satisfiable": the partial file is as long as the real one, or longer
            _, total = _parse_content_range(exc.headers.get("Content-Range") if exc.headers else None)
            with contextlib.suppress(Exception):
                exc.close()
            if total is not None and total == offset:
                return True, offset, total
            raise _Restart from None
        raise
    with response:
        total: int | None
        if getattr(response, "status", 200) == 206:
            start, total = _parse_content_range(response.headers.get("Content-Range"))
            if start != offset:
                raise _Restart
        else:  # 200: the server ignored the range, or the file changed (If-Range) -> from the top
            offset = 0
            length = response.headers.get("Content-Length")
            total = int(length) if length and length.strip().isdigit() else None
        if total is not None:
            # the rest of the download, plus room to unpack it (archive and unpacked copy coexist briefly)
            _require_free_space(part.parent, (total - offset) + int(1.5 * total), url)
        done = offset
        try:
            meta.write_text(
                json.dumps({"url": url, "validator": _validator(response.headers), "total": total}), encoding="utf-8"
            )
            out = open(part, "r+b" if offset else "wb")
        except OSError as exc:
            raise _LocalIOError(exc.strerror or str(exc)) from exc
        with out:
            if offset:
                out.seek(offset)
                out.truncate()
            if progress:
                progress(done, total)
            while True:
                block = response.read(_CHUNK)
                if not block:
                    break
                try:
                    out.write(block)
                except OSError as exc:
                    raise _LocalIOError(exc.strerror or str(exc)) from exc
                done += len(block)
                if progress:
                    progress(done, total)
    return (total is None or done >= total), done, total


def download_file(
    url: str,
    dest: str | Path,
    *,
    progress: ProgressFn | None = None,
    timeout: float = DEFAULT_TIMEOUT,
    retries: int = DEFAULT_RETRIES,
) -> Path:
    """Download ``url`` to the file ``dest``, resuming ``<dest>.part`` if one is there.

    The file appears under its final name only once it is complete (atomic
    rename).  Raises :class:`ModelFetchError` after more than ``retries``
    consecutive attempts that made no progress, or at once for errors that
    retrying will not fix (HTTP 404, disk full).  The partial file is kept so
    that the next call resumes.
    """
    if urllib.parse.urlsplit(url).scheme not in ("http", "https"):
        raise ValueError(f"only http(s) URLs can be downloaded, got {url!r}")
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    part = dest.with_name(dest.name + ".part")
    meta = dest.with_name(dest.name + ".part.json")
    failures = 0
    while True:
        before = part.stat().st_size if part.is_file() else 0
        try:
            finished, done, total = _attempt(url, part, meta, progress, timeout)
        except _Restart:
            part.unlink(missing_ok=True)
            meta.unlink(missing_ok=True)
            failures += 1
            if failures > retries:
                raise ModelFetchError(
                    f"Could not download {url}\n  the server kept refusing to continue the download.",
                    url=url,
                    dest_dir=dest.parent,
                ) from None
            log.info("cannot resume %s; starting the download again", dest.name)
            continue
        except _LocalIOError as exc:
            raise ModelFetchError(
                f"Could not save the download to {part.parent}: {exc}", url=url, dest_dir=dest.parent
            ) from exc
        except urllib.error.HTTPError as exc:
            if exc.code not in _RETRY_STATUSES:
                hint = "  There is no such file at that address." if exc.code in (404, 410) else ""
                raise ModelFetchError(
                    f"Could not download {url}\n  the server answered HTTP {exc.code} {exc.reason}.{hint}",
                    url=url,
                    dest_dir=dest.parent,
                ) from exc
            problem = _describe_network_error(exc, timeout)
        except (OSError, HTTPException) as exc:  # URLError, timeouts, resets, TLS errors, …
            problem = _describe_network_error(exc, timeout)
        else:
            if finished:
                os.replace(part, dest)
                meta.unlink(missing_ok=True)
                return dest
            problem = f"the connection closed early (after {done} of {total} bytes)"
        after = part.stat().st_size if part.is_file() else 0
        failures = 0 if after > before else failures + 1
        if failures > retries:
            kept = f"\n  The {after / 1e6:.0f} MB received so far were kept; running the command again resumes." if after else ""
            raise ModelFetchError(
                f"Could not download {url}\n  {problem}. Check the internet connection and try again.{kept}",
                url=url,
                dest_dir=dest.parent,
            )
        delay = min(20.0, 1.5 ** max(failures, 1))
        log.warning("download of %s interrupted (%s); retrying in %.0f s", dest.name, problem, delay)
        time.sleep(delay)


# -- extraction -------------------------------------------------------------------------


def _safe_relative(name: str) -> str:
    """Normalise an archive member name to a clean relative POSIX path, or raise."""
    raw = name.replace("\\", "/")
    if not raw or "\x00" in raw:
        raise UnsafeArchiveError(f"archive entry with an unusable name: {name!r}")
    if raw.startswith("/") or (len(raw) > 1 and raw[1] == ":"):
        raise UnsafeArchiveError(f"archive entry has an absolute path: {name!r}")
    parts = [p for p in raw.split("/") if p not in ("", ".")]
    if ".." in parts:
        raise UnsafeArchiveError(f"archive entry tries to leave the destination folder: {name!r}")
    return "/".join(parts)


def _check_symlink(member: str, target: str) -> None:
    """Allow only symlinks that point at or below their own folder.

    Checking where a link *resolves* is fragile (a later entry can change what
    an earlier path means).  A link target that is relative and has no ``..``
    cannot go up, so no combination of such links leaves the destination.
    """
    raw = target.replace("\\", "/")
    if not raw or raw.startswith("/") or (len(raw) > 1 and raw[1] == ":") or "\x00" in raw:
        raise UnsafeArchiveError(f"archive entry {member!r} is a link to an absolute path: {target!r}")
    if ".." in raw.split("/"):
        raise UnsafeArchiveError(f"archive entry {member!r} is a link that leaves its folder: {target!r}")


def _prepare_target(root: Path, relative: str) -> Path:
    """Create the parent folders of ``root/relative`` and return the (now free) target path.

    Refuses to go through a symlink — an archive can plant ``a -> somewhere``
    and then ask for ``a/file`` — and removes a link or file already at the target
    so nothing is ever written *through* one.
    """
    target = root
    parts = relative.split("/")
    for part in parts[:-1]:
        target = target / part
        if target.is_symlink():
            raise UnsafeArchiveError(f"archive entry {relative!r} would be written through the link {part!r}")
        if not target.is_dir():
            if target.exists():
                target.unlink()
            target.mkdir()
    target = target / parts[-1]
    if target.is_symlink() or target.is_file():
        target.unlink()
    return target


def _write_member(src: IO[bytes], dst_path: Path, budget: list[int], mode: int) -> None:
    with open(dst_path, "wb") as dst:
        while True:
            block = src.read(_CHUNK)
            if not block:
                break
            budget[0] -= len(block)
            if budget[0] < 0:
                raise ModelFetchError(
                    f"the archive unpacks to more than {MAX_UNPACKED_BYTES / 1e9:.0f} GB; refusing to continue"
                )
            dst.write(block)
    # owner can always read and write; keep the executable bit; never setuid/setgid/sticky or world-writable
    os.chmod(dst_path, 0o755 if mode & 0o100 else 0o644)


def _extract_tar(archive: Path, root: Path, budget: list[int]) -> None:
    with tarfile.open(archive, "r:*") as tar:
        for member in tar:
            relative = _safe_relative(member.name)
            if not relative:
                continue  # the "./" entry
            if member.isdir():
                target = _prepare_target(root, relative)
                target.mkdir(exist_ok=True)
            elif member.isreg():
                target = _prepare_target(root, relative)
                source = tar.extractfile(member)
                if source is None:
                    raise ModelFetchError(f"cannot read {member.name!r} from the archive")
                with source:
                    _write_member(source, target, budget, member.mode)
            elif member.issym():
                _check_symlink(relative, member.linkname)
                os.symlink(member.linkname, _prepare_target(root, relative))
            elif member.islnk():
                # a hard link: copy the file it refers to (which must already have come out of this archive)
                source_path = root / _safe_relative(member.linkname)
                if not source_path.is_file():
                    raise UnsafeArchiveError(
                        f"archive entry {member.name!r} is a hard link to {member.linkname!r}, which is not in the archive"
                    )
                target = _prepare_target(root, relative)
                with open(source_path, "rb") as source:
                    _write_member(source, target, budget, member.mode)
            else:
                raise UnsafeArchiveError(f"archive entry {member.name!r} is a device or other special file")


def _extract_zip(archive: Path, root: Path, budget: list[int]) -> None:
    with zipfile.ZipFile(archive) as zf:
        for info in zf.infolist():
            relative = _safe_relative(info.filename)
            if not relative:
                continue
            mode = info.external_attr >> 16
            if info.is_dir():
                _prepare_target(root, relative).mkdir(exist_ok=True)
            elif stat.S_ISLNK(mode):
                link = zf.read(info).decode("utf-8", "replace")
                _check_symlink(relative, link)
                os.symlink(link, _prepare_target(root, relative))
            else:
                target = _prepare_target(root, relative)
                with zf.open(info) as source:
                    _write_member(source, target, budget, mode)


def extract_archive(archive: str | Path, dest_dir: str | Path, *, kind: str | None = None) -> list[str]:
    """Unpack ``archive`` into the folder ``dest_dir``. Returns the top-level names now in it.

    Every entry is validated before it is written (see the module docstring);
    an :class:`UnsafeArchiveError` aborts the extraction.  ``kind`` ("tar" or
    "zip") is only needed when the file name does not have a known suffix.
    Unpack into a fresh folder: files already at an entry's path are replaced.
    """
    archive, root = Path(archive), Path(dest_dir)
    kind = kind or archive_kind(archive.name)
    if kind not in ("tar", "zip"):
        raise ModelFetchError(f"{archive.name} is not a .tar.bz2 / .tar.gz / .tar.xz / .zip archive")
    damaged = f"{archive.name} is damaged or not a valid archive"
    try:
        root.mkdir(parents=True, exist_ok=True)
        budget = [MAX_UNPACKED_BYTES]
        if kind == "tar":
            _extract_tar(archive, root, budget)
        else:
            _extract_zip(archive, root, budget)
    except _ARCHIVE_ERRORS as exc:
        raise ModelFetchError(f"{damaged} ({exc})") from exc
    except OSError as exc:
        if exc.errno is None:  # bz2/gzip report corrupt data as a bare OSError("Invalid data stream")
            raise ModelFetchError(f"{damaged} ({exc})") from exc
        raise _UnpackIOError(f"Could not unpack {archive.name} into {root}: {exc.strerror or exc}") from exc
    return sorted(p.name for p in root.iterdir())


# -- the whole job ------------------------------------------------------------------------


@contextlib.contextmanager
def _locked(lock_file: Path, what: str) -> Iterator[None]:
    """Hold an advisory lock so two videonotes processes do not fetch the same archive at once.

    The lock belongs to the open file, so it vanishes with the process that
    holds it: a crash can never leave a stale lock behind.
    """
    try:
        import fcntl
    except ImportError:  # not POSIX: go without
        yield
        return
    with open(lock_file, "a+b") as handle:
        announced = False
        while True:
            try:
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except OSError:
                if not announced:
                    log.info("another videonotes process is already fetching %s; waiting for it to finish", what)
                    announced = True
                time.sleep(1.0)
        try:
            yield
        finally:
            with contextlib.suppress(OSError):
                fcntl.flock(handle, fcntl.LOCK_UN)


def _remove(path: Path) -> None:
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    else:
        path.unlink()


def _reserved(name: str) -> bool:
    """Top-level names this module uses itself inside ``dest_dir``."""
    return name == _DOWNLOADS_DIR or name.startswith(_STAGING_PREFIX) or (name.startswith(".") and name.endswith(".complete"))


def fetch_archive(
    url: str,
    dest_dir: str | Path,
    *,
    expected_member: str | None = None,
    progress: ProgressFn | None = None,
    timeout: float = DEFAULT_TIMEOUT,
    retries: int = DEFAULT_RETRIES,
) -> Path:
    """Download the archive at ``url`` and unpack it into ``dest_dir``.

    Returns ``dest_dir/expected_member`` when ``expected_member`` (a file or
    folder the archive must contain, relative to its root) is given; otherwise
    the archive's single top-level entry, or ``dest_dir`` itself when it has
    several.  Calling it again after it succeeded costs nothing: the completion
    marker short-circuits the network.  Entries already in ``dest_dir`` under
    the same names as the archive's top-level entries are replaced.

    ``progress(bytes_done, bytes_total)`` is called while downloading, once per
    block (throttle inside the callback if it does anything slow).

    Raises :class:`ModelFetchError` (a ``RuntimeError``) with instructions when
    anything fails; a partial download is kept and resumed by the next call.
    """
    if urllib.parse.urlsplit(url).scheme not in ("http", "https"):
        raise ValueError(f"only http(s) URLs can be fetched, got {url!r}")
    dest = Path(dest_dir).expanduser()
    name = archive_name(url)
    if expected_member is not None:
        expected_member = _safe_relative(expected_member)
    downloads = dest / _DOWNLOADS_DIR

    def explain(exc: ModelFetchError) -> ModelFetchError:
        if isinstance(exc, UnsafeArchiveError):
            text = (
                f"{name} was NOT unpacked because it looks unsafe: {exc}\n"
                f"It came from {url}\nDo not unpack it by hand either."
            )
        else:
            text = f"{exc}\n{manual_instructions(url, dest, expected_member=expected_member)}"
        kind = UnsafeArchiveError if isinstance(exc, UnsafeArchiveError) else ModelFetchError
        return kind(text, url=url, dest_dir=dest)

    try:
        downloads.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise explain(ModelFetchError(f"Cannot create the models folder {dest}: {exc.strerror or exc}")) from exc

    with _locked(downloads / f"{name}.lock", name):
        members = _fetched_members(url, dest, expected_member)
        if members is not None:
            return _result_path(dest, members, expected_member)

        archive = downloads / name
        staging: Path | None = None
        try:
            if not archive.is_file():
                log.info("downloading %s", url)
                download_file(url, archive, progress=progress, timeout=timeout, retries=retries)
            log.info("unpacking %s", name)
            staging = Path(tempfile.mkdtemp(prefix=_STAGING_PREFIX, dir=dest))
            try:
                members = extract_archive(archive, staging)
                if not members:
                    raise ModelFetchError(f"{name} is empty")
                if any(_reserved(member) for member in members):
                    raise UnsafeArchiveError(f"{name} contains an entry with a reserved name")
                if expected_member and not (staging / expected_member).exists():
                    raise ModelFetchError(
                        f"{name} does not contain {expected_member!r} (it contains: {', '.join(members[:8])})"
                    )
            except ModelFetchError as exc:
                if not isinstance(exc, _UnpackIOError):  # the bytes are bad: never try them again
                    archive.unlink(missing_ok=True)
                raise
            marker_path(url, dest).unlink(missing_ok=True)
            for member in members:
                target = dest / member
                if target.exists() or target.is_symlink():
                    _remove(target)
                os.replace(staging / member, target)
            payload = {"url": url, "members": members, "bytes": archive.stat().st_size, "fetched_at": time.time()}
            tmp_marker = downloads / f"{name}.complete.tmp"
            tmp_marker.write_text(json.dumps(payload), encoding="utf-8")
            os.replace(tmp_marker, marker_path(url, dest))
            archive.unlink(missing_ok=True)
        except ModelFetchError as exc:
            raise explain(exc) from exc
        except OSError as exc:
            raise explain(ModelFetchError(f"Could not install {name} into {dest}: {exc.strerror or exc}")) from exc
        finally:
            if staging is not None:
                shutil.rmtree(staging, ignore_errors=True)
        log.info("installed %s into %s", name, dest)
        return _result_path(dest, members, expected_member)
