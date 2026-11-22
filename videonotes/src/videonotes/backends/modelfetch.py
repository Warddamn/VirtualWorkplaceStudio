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


def _read_marker(url: str, dest_dir: Path) -> dict[str, Any] | None:
    try:
        data = json.loads(marker_path(url, dest_dir).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) and data.get("url") == url else None


def _result_path(dest_dir: Path, members: list[str], expected_member: str | None) -> Path:
    if expected_member:
        return dest_dir / expected_member
    return dest_dir / members[0] if len(members) == 1 else dest_dir


def is_fetched(url: str, dest_dir: str | Path, *, expected_member: str | None = None) -> bool:
    """True if :func:`fetch_archive` already completed for this URL and its files are still there."""
    dest = Path(dest_dir)
    marker = _read_marker(url, dest)
    if marker is None:
        return False
    members = [m for m in marker.get("members", []) if isinstance(m, str)]
    if not members or not all((dest / m).exists() for m in members):
        return False
    return expected_member is None or (dest / expected_member).exists()


def manual_instructions(url: str, dest_dir: str | Path, *, expected_member: str | None = None) -> str:
    """The by-hand alternative to :func:`fetch_archive`, as text for an error message."""
    dest = Path(dest_dir)
    name = archive_name(url)
    if archive_kind(name) == "zip":
        command = f'unzip ~/Downloads/{name} -d "{dest}"'
    else:
        command = f'tar -xf ~/Downloads/{name} -C "{dest}"'
    lines = [
        "To install it by hand instead: download",
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
    reason = exc.reason if isinstance(exc, urllib.error.URLError) and not isinstance(exc, urllib.error.HTTPError) else exc
    if isinstance(reason, TimeoutError) or "timed out" in str(reason).lower():
        return f"the connection stalled (no data for {timeout:.0f} s)"
    if isinstance(exc, urllib.error.HTTPError):
        return f"the server answered HTTP {exc.code} {exc.reason}"
    text = str(reason) or type(reason).__name__
    return f"network problem: {text}"


def _parse_content_range(value: str | None) -> tuple[int | None, int | None]:
    """``bytes 100-199/1000`` -> (100, 1000); ``bytes */1000`` -> (None, 1000)."""
    if not value or not value.strip().lower().startswith("bytes"):
        return None, None
    spec = value.strip()[5:].strip()
    span, _, total = spec.partition("/")
    start: int | None = None
    if "-" in span:
        with contextlib.suppress(ValueError):
            start = int(span.split("-", 1)[0])
    try:
        return start, int(total)
    except ValueError:
        return start, None


def _validator(headers: HTTPMessage) -> str:
    """A strong ETag if there is one, else Last-Modified, else '' (resume is then unconditional)."""
    etag = (headers.get("ETag") or "").strip()
    if etag and not etag.startswith("W/"):
        return etag
    return (headers.get("Last-Modified") or "").strip()


class _Restart(Exception):
    """The partial file cannot be continued; start again from byte 0."""


def _attempt(
    url: str, part: Path, meta: Path, progress: ProgressFn | None, timeout: float
) -> tuple[bool, int, int | None]:
    """One HTTP request. Returns (finished, bytes now on disk, total or None)."""
    offset = part.stat().st_size if part.is_file() else 0
    saved: dict[str, Any] = {}
    if offset:
        try:
            saved = json.loads(meta.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            saved = {}
        if saved.get("url") != url:  # a leftover from something else: do not glue two files together
            part.unlink(missing_ok=True)
            offset, saved = 0, {}
    headers = {"User-Agent": _USER_AGENT, "Accept-Encoding": "identity"}
    if offset:
        headers["Range"] = f"bytes={offset}-"
        if saved.get("validator"):
            headers["If-Range"] = str(saved["validator"])
    request = urllib.request.Request(url, headers=headers)
    try:
        response = urllib.request.urlopen(request, timeout=timeout)  # noqa: S310 - scheme checked by caller
    except urllib.error.HTTPError as exc:
        with exc:
            if exc.code == 416 and offset:
                _, total = _parse_content_range(exc.headers.get("Content-Range"))
                if total is not None and total == offset:
                    return True, offset, total  # everything was already there
                raise _Restart from None
        raise
    with response:
        status = getattr(response, "status", 200)
        total: int | None
        if status == 206:
            start, total = _parse_content_range(response.headers.get("Content-Range"))
            if start != offset:
                raise _Restart
        else:  # 200: the server ignored the range, or the file changed (If-Range) -> from the top
            offset = 0
            length = response.headers.get("Content-Length")
            total = int(length) if length and length.isdigit() else None
        meta.write_text(
            json.dumps({"url": url, "validator": _validator(response.headers), "total": total}), encoding="utf-8"
        )
        if total is not None:
            _require_free_space(part.parent, (total - offset) + 2 * total, url)
        done = offset
        if progress:
            progress(done, total)
        with open(part, "r+b" if offset else "wb") as out:
            if offset:
                out.seek(offset)
                out.truncate()
            while True:
                block = response.read(_CHUNK)
                if not block:
                    break
                out.write(block)
                done += len(block)
                if progress:
                    progress(done, total)
    return (total is None or done >= total), done, total


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


def download_file(
    url: str,
    dest: str | Path,
    *,
    progress: ProgressFn | None = None,
    timeout: float = DEFAULT_TIMEOUT,
    retries: int = DEFAULT_RETRIES,
) -> Path:
    """Download ``url`` to the file ``dest``, resuming ``dest + ".part"`` if one is there.

    The file appears under its final name only once it is complete (atomic
    rename).  Raises :class:`ModelFetchError` after ``retries`` consecutive
    attempts that made no progress, or at once for errors that retrying will
    not fix (HTTP 404, disk full).  The partial file is kept so that the next
    call resumes.
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
        problem: str
        try:
            finished, done, total = _attempt(url, part, meta, progress, timeout)
        except _Restart:
            log.info("cannot resume %s; starting the download again", dest.name)
            part.unlink(missing_ok=True)
            meta.unlink(missing_ok=True)
            failures += 1
            if failures > retries:
                raise ModelFetchError(
                    f"Could not download {url}\n  the server kept rejecting the request.", url=url, dest_dir=dest.parent
                ) from None
            continue
        except urllib.error.HTTPError as exc:
            if exc.code not in _RETRY_STATUSES:
                hint = "  The file does not exist at that address." if exc.code in (404, 410) else ""
                raise ModelFetchError(
                    f"Could not download {url}\n  the server answered HTTP {exc.code} {exc.reason}.{hint}",
                    url=url,
                    dest_dir=dest.parent,
                ) from exc
            problem = _describe_network_error(exc, timeout)
        except (urllib.error.URLError, HTTPException, TimeoutError, ConnectionError) as exc:
            problem = _describe_network_error(exc, timeout)
        except OSError as exc:  # disk full, permission denied, … — not a network problem
            raise ModelFetchError(
                f"Could not save the download to {part}: {exc.strerror or exc}", url=url, dest_dir=dest.parent
            ) from exc
        else:
            if finished:
                os.replace(part, dest)
                meta.unlink(missing_ok=True)
                return dest
            problem = f"the connection closed early ({done} of {total} bytes)"
        after = part.stat().st_size if part.is_file() else 0
        failures = 0 if after > before else failures + 1
        if failures > retries:
            kept = f"\n  The {after / 1e6:.0f} MB received so far were kept; running the command again resumes." if after else ""
            raise ModelFetchError(
                f"Could not download {url}\n  {problem}. Check the internet connection.{kept}",
                url=url,
                dest_dir=dest.parent,
            )
        delay = min(30.0, 1.5 ** max(failures, 1))
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
    if any(p == ".." for p in parts):
        raise UnsafeArchiveError(f"archive entry tries to leave the destination folder: {name!r}")
    return "/".join(parts)


def _check_link(member: str, target: str, *, relative_to_member: bool) -> None:
    """Refuse a symlink / hard link whose target is outside the extraction root."""
    raw = target.replace("\\", "/")
    if not raw or raw.startswith("/") or (len(raw) > 1 and raw[1] == ":"):
        raise UnsafeArchiveError(f"archive entry {member!r} links to an absolute path: {target!r}")
    base = posixpath.dirname(member) if relative_to_member else ""
    resolved = posixpath.normpath(posixpath.join(base, raw))
    if resolved == ".." or resolved.startswith("../") or resolved.startswith("/"):
        raise UnsafeArchiveError(f"archive entry {member!r} links outside the destination folder: {target!r}")


def _prepare_parent(root: Path, relative: str) -> Path:
    """Create the parent folders of ``root/relative`` and return the target path.

    Refuses to go through a symlink (an archive can plant ``a -> elsewhere``
    and then ask for ``a/file``), and replaces whatever was at the target.
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


def _copy_limited(src: IO[bytes], dst_path: Path, budget: list[int], mode: int) -> None:
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
    # owner can always read/write; keep the executable bit; drop setuid/setgid/sticky and group/other write
    os.chmod(dst_path, 0o644 | (0o111 if mode & 0o100 else 0))


def _extract_tar(archive: Path, root: Path, budget: list[int]) -> None:
    with tarfile.open(archive, "r:*") as tar:
        for member in tar:
            relative = _safe_relative(member.name)
            if not relative:
                continue  # the "./" entry
            if member.isdir():
                target = _prepare_parent(root, relative)
                target.mkdir(exist_ok=True)
            elif member.isreg():
                target = _prepare_parent(root, relative)
                source = tar.extractfile(member)
                if source is None:
                    raise ModelFetchError(f"cannot read {member.name!r} from the archive")
                with source:
                    _copy_limited(source, target, budget, member.mode)
            elif member.issym():
                _check_link(relative, member.linkname, relative_to_member=True)
                target = _prepare_parent(root, relative)
                os.symlink(member.linkname, target)
            elif member.islnk():
                _check_link(relative, member.linkname, relative_to_member=False)
                source_path = root / _safe_relative(member.linkname)
                if source_path.is_symlink() or not source_path.is_file():
                    raise UnsafeArchiveError(f"archive entry {member.name!r} is a hard link to something not in the archive")
                target = _prepare_parent(root, relative)
                with open(source_path, "rb") as source:
                    _copy_limited(source, target, budget, member.mode)
            elif member.type in (tarfile.XHDTYPE, tarfile.XGLTYPE, tarfile.GNUTYPE_LONGNAME, tarfile.GNUTYPE_LONGLINK):
                continue  # metadata records, already applied by tarfile
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
                _prepare_parent(root, relative).mkdir(exist_ok=True)
            elif stat.S_ISLNK(mode):
                link = zf.read(info).decode("utf-8", "replace")
                _check_link(relative, link, relative_to_member=True)
                os.symlink(link, _prepare_parent(root, relative))
            else:
                target = _prepare_parent(root, relative)
                with zf.open(info) as source:
                    _copy_limited(source, target, budget, mode)


def extract_archive(archive: str | Path, dest_dir: str | Path, *, kind: str | None = None) -> list[str]:
    """Unpack ``archive`` into the existing folder ``dest_dir``. Returns the top-level names created.

    Every entry is validated before it is written (see the module docstring);
    an :class:`UnsafeArchiveError` aborts the extraction.  ``kind`` ("tar" or
    "zip") is only needed when the file name does not have a known suffix.
    """
    archive, root = Path(archive), Path(dest_dir)
    kind = kind or archive_kind(archive.name)
    if kind not in ("tar", "zip"):
        raise ModelFetchError(f"{archive.name}: not a .tar.bz2 / .tar.gz / .zip archive")
    root.mkdir(parents=True, exist_ok=True)
    budget = [MAX_UNPACKED_BYTES]
    try:
        if kind == "tar":
            _extract_tar(archive, root, budget)
        else:
            _extract_zip(archive, root, budget)
    except (tarfile.TarError, zipfile.BadZipFile, EOFError, ValueError, RuntimeError, NotImplementedError) as exc:
        if isinstance(exc, ModelFetchError):
            raise
        raise ModelFetchError(f"{archive.name} is damaged or not a valid archive ({exc})") from exc
    except OSError as exc:
        if isinstance(exc, (tarfile.TarError, zipfile.BadZipFile)):
            raise ModelFetchError(f"{archive.name} is damaged or not a valid archive ({exc})") from exc
        raise ModelFetchError(f"could not unpack {archive.name} into {root}: {exc.strerror or exc}") from exc
    return sorted(p.name for p in root.iterdir())


# -- the whole job ------------------------------------------------------------------------


@contextlib.contextmanager
def _locked(lock_file: Path, what: str) -> Iterator[None]:
    """Hold an advisory lock so two videonotes processes do not fetch the same archive at once."""
    try:
        import fcntl
    except ImportError:  # not POSIX: go without
        yield
        return
    lock_file.parent.mkdir(parents=True, exist_ok=True)
    with open(lock_file, "a+b") as handle:
        announced = False
        while True:
            try:
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except OSError:
                if not announced:
                    log.info("another videonotes process is already downloading %s; waiting for it", what)
                    announced = True
                time.sleep(1.0)
        try:
            yield
        finally:
            with contextlib.suppress(OSError):
                fcntl.flock(handle, fcntl.LOCK_UN)


def _remove(path: Path) -> None:
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path, ignore_errors=True)
    else:
        with contextlib.suppress(OSError):
            path.unlink()


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
    several.  Calling it again once it succeeded costs nothing: the completion
    marker short-circuits the network.  Existing entries with the same names
    as the archive's top-level entries are replaced.

    ``progress(bytes_done, bytes_total)`` is called while downloading (often:
    throttle in the callback if it does something slow).

    Raises :class:`ModelFetchError` (a ``RuntimeError``) with instructions when
    anything fails; a partial download is kept and resumed by the next call.
    """
    if urllib.parse.urlsplit(url).scheme not in ("http", "https"):
        raise ValueError(f"only http(s) URLs can be fetched, got {url!r}")
    dest = Path(dest_dir).expanduser()
    name = archive_name(url)
    if expected_member is not None:
        expected_member = _safe_relative(expected_member)
    manual = manual_instructions(url, dest, expected_member=expected_member)

    def fail(exc: ModelFetchError) -> ModelFetchError:
        error = type(exc)(f"{exc}\n{manual}", url=url, dest_dir=dest)
        error.__cause__ = exc.__cause__ or exc
        return error

    try:
        dest.mkdir(parents=True, exist_ok=True)
        downloads = dest / _DOWNLOADS_DIR
        downloads.mkdir(exist_ok=True)
    except OSError as exc:
        raise ModelFetchError(
            f"Cannot create the models folder {dest}: {exc.strerror or exc}", url=url, dest_dir=dest
        ) from exc

    with _locked(downloads / f"{name}.lock", name):
        marker = _read_marker(url, dest)
        if marker is not None and is_fetched(url, dest, expected_member=expected_member):
            return _result_path(dest, list(marker["members"]), expected_member)

        archive = downloads / name
        staging: Path | None = None
        try:
            if not archive.is_file():
                log.info("downloading %s", url)
                download_file(url, archive, progress=progress, timeout=timeout, retries=retries)
            staging = Path(tempfile.mkdtemp(prefix=".unpack-", dir=dest))
            log.info("unpacking %s", name)
            try:
                members = extract_archive(archive, staging)
            except ModelFetchError:
                archive.unlink(missing_ok=True)  # damaged or hostile: never retry with the same bytes
                raise
            if not members:
                archive.unlink(missing_ok=True)
                raise ModelFetchError(f"{name} is empty")
            if expected_member and not (staging / expected_member).exists():
                archive.unlink(missing_ok=True)
                raise ModelFetchError(
                    f"{name} does not contain {expected_member!r} (it contains: {', '.join(members[:8])})"
                )
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
            raise fail(exc) from exc.__cause__
        except OSError as exc:
            raise fail(ModelFetchError(f"Could not install {name} into {dest}: {exc.strerror or exc}")) from exc
        finally:
            if staging is not None:
                shutil.rmtree(staging, ignore_errors=True)
        return _result_path(dest, members, expected_member)
