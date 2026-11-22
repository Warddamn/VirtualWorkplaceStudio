"""modelfetch: resumable downloads and safe extraction, exercised against a local HTTP server."""

from __future__ import annotations

import io
import json
import os
import socket
import stat
import tarfile
import threading
import time
import urllib.parse
import urllib.request
import zipfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

import pytest

from videonotes.backends import modelfetch
from videonotes.backends.modelfetch import ModelFetchError, UnsafeArchiveError, fetch_archive

MODEL = "sherpa-onnx-test-model"
MODEL_FILES = {
    f"{MODEL}/encoder.int8.onnx": os.urandom(150_000),  # incompressible, so the archive is a real download
    f"{MODEL}/tokens.txt": b"<blk> 0\nhello 1\n",
    f"{MODEL}/test_wavs/readme.txt": b"nested file\n",
}


# -- a small HTTP server with the misbehaviours a real network has --------------------------------


class ArchiveServer:
    """Serves ``files`` with Range / ETag support and scripted faults.

    ``drop_after[path]``  byte counts: the next GETs send only that many body bytes, then hang up
    ``statuses[path]``    HTTP statuses to answer with before behaving normally
    ``ignore_range``      paths that always answer 200 with the whole file
    ``stall``             paths that never answer (until the server shuts down)
    """

    def __init__(self) -> None:
        self.files: dict[str, bytes] = {}
        self.etags: dict[str, str] = {}
        self.requests: list[dict[str, Any]] = []
        self.drop_after: dict[str, list[int]] = {}
        self.statuses: dict[str, list[int]] = {}
        self.ignore_range: set[str] = set()
        self.stall: set[str] = set()
        self.delay = 0.0
        self._released = threading.Event()
        outer = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args: Any) -> None:
                pass

            def do_GET(self) -> None:
                path = urllib.parse.urlsplit(self.path).path  # a proxy request carries the absolute URL
                outer.requests.append(
                    {
                        "path": path,
                        "raw": self.path,
                        "range": self.headers.get("Range"),
                        "if_range": self.headers.get("If-Range"),
                        "agent": self.headers.get("User-Agent"),
                    }
                )
                if path in outer.stall:
                    outer._released.wait(10)
                    return
                if outer.delay:
                    time.sleep(outer.delay)
                if outer.statuses.get(path):
                    self.send_error(outer.statuses[path].pop(0))
                    return
                if path not in outer.files:
                    self.send_error(404)
                    return
                data = outer.files[path]
                etag = outer.etags.get(path, f'"v1-{len(data)}"')
                start = 0
                wanted = self.headers.get("Range")
                if wanted and path not in outer.ignore_range:
                    if_range = self.headers.get("If-Range")
                    if if_range is None or if_range == etag:
                        start = int(wanted.split("=", 1)[1].split("-", 1)[0])
                if start >= len(data) and start > 0:
                    self.send_response(416)
                    self.send_header("Content-Range", f"bytes */{len(data)}")
                    self.send_header("Content-Length", "0")
                    self.end_headers()
                    return
                body = data[start:]
                self.send_response(206 if start else 200)
                self.send_header("Content-Type", "application/octet-stream")
                self.send_header("Content-Length", str(len(body)))
                self.send_header("ETag", etag)
                if start:
                    self.send_header("Content-Range", f"bytes {start}-{len(data) - 1}/{len(data)}")
                self.end_headers()
                if outer.drop_after.get(path):
                    self.wfile.write(body[: outer.drop_after[path].pop(0)])
                    self.wfile.flush()
                    self.connection.shutdown(socket.SHUT_RDWR)  # the "Wi-Fi dropped" moment
                    return
                self.wfile.write(body)

        self._server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self._server.daemon_threads = True
        self.url = f"http://127.0.0.1:{self._server.server_address[1]}"
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()

    def add(self, name: str, data: bytes) -> str:
        self.files[f"/{name}"] = data
        return f"{self.url}/{name}"

    def gets(self, name: str) -> list[dict[str, Any]]:
        return [r for r in self.requests if r["path"] == f"/{name}"]

    def close(self) -> None:
        self._released.set()
        self._server.shutdown()
        self._server.server_close()


@pytest.fixture()
def server():
    srv = ArchiveServer()
    yield srv
    srv.close()


@pytest.fixture(autouse=True)
def no_waiting(monkeypatch):
    """Retries back off for seconds in real life; in tests they only yield the CPU."""
    real_sleep = time.sleep
    monkeypatch.setattr(modelfetch.time, "sleep", lambda seconds: real_sleep(min(seconds, 0.01)))
    # other machines' proxy settings must not leak into requests for 127.0.0.1
    monkeypatch.setenv("no_proxy", "127.0.0.1,localhost")
    monkeypatch.setenv("NO_PROXY", "127.0.0.1,localhost")


# -- archive builders ------------------------------------------------------------------------------


def make_tar(files: dict[str, bytes], mode: str = "w:bz2", extra: list[tarfile.TarInfo] | None = None) -> bytes:
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode=mode) as tar:
        for name, data in files.items():
            info = tarfile.TarInfo(name)
            info.size = len(data)
            info.mode = 0o644
            tar.addfile(info, io.BytesIO(data))
        for info in extra or []:
            tar.addfile(info, io.BytesIO(b"x" * info.size) if info.isreg() else None)
    return buf.getvalue()


def make_zip(files: dict[str, bytes]) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, data in files.items():
            zf.writestr(name, data)
    return buf.getvalue()


def link_info(name: str, target: str, kind: bytes = tarfile.SYMTYPE) -> tarfile.TarInfo:
    info = tarfile.TarInfo(name)
    info.type = kind
    info.linkname = target
    return info


def file_info(name: str, size: int = 4, mode: int = 0o644) -> tarfile.TarInfo:
    info = tarfile.TarInfo(name)
    info.size = size
    info.mode = mode
    return info


def assert_model_installed(folder: Path) -> None:
    for name, data in MODEL_FILES.items():
        assert (folder.parent / name).read_bytes() == data


def leftovers(dest: Path) -> list[str]:
    """Anything in dest besides installed models, the marker files and the downloads folder."""
    return sorted(p.name for p in dest.iterdir() if p.name.startswith(".unpack-"))


# -- the happy path ----------------------------------------------------------------------------------


def test_fetch_tar_bz2_installs_model_and_reports_progress(server, tmp_path):
    archive = make_tar(MODEL_FILES)
    url = server.add(f"{MODEL}.tar.bz2", archive)
    dest = tmp_path / "models"
    seen: list[tuple[int, int | None]] = []

    result = fetch_archive(url, dest, expected_member=MODEL, progress=lambda done, total: seen.append((done, total)))

    assert result == dest / MODEL
    assert_model_installed(result)
    assert seen[0] == (0, len(archive)) and seen[-1] == (len(archive), len(archive))
    assert [d for d, _ in seen] == sorted(d for d, _ in seen)
    assert modelfetch.is_fetched(url, dest, expected_member=MODEL)
    assert modelfetch.marker_path(url, dest).is_file()
    # nothing half-done is left behind: no archive, no partial file, no staging folder
    assert [p.name for p in (dest / ".downloads").iterdir()] == [f"{MODEL}.tar.bz2.lock"]
    assert leftovers(dest) == []
    assert server.gets(f"{MODEL}.tar.bz2")[0]["agent"] == "videonotes-modelfetch"


def test_second_fetch_uses_the_marker_and_no_network(server, tmp_path):
    url = server.add(f"{MODEL}.tar.bz2", make_tar(MODEL_FILES))
    first = fetch_archive(url, tmp_path, expected_member=MODEL)
    count = len(server.requests)
    second = fetch_archive(url, tmp_path, expected_member=MODEL)
    assert first == second
    assert len(server.requests) == count


def test_deleted_model_is_fetched_again(server, tmp_path):
    url = server.add(f"{MODEL}.tar.bz2", make_tar(MODEL_FILES))
    folder = fetch_archive(url, tmp_path, expected_member=MODEL)
    for path in sorted(folder.rglob("*"), reverse=True):
        path.rmdir() if path.is_dir() else path.unlink()
    folder.rmdir()
    assert not modelfetch.is_fetched(url, tmp_path, expected_member=MODEL)  # the marker alone proves nothing
    fetch_archive(url, tmp_path, expected_member=MODEL)
    assert_model_installed(folder)
    assert len(server.gets(f"{MODEL}.tar.bz2")) == 2


@pytest.mark.parametrize(
    ("name", "build"),
    [
        ("m.tar.gz", lambda files: make_tar(files, "w:gz")),
        ("m.tgz", lambda files: make_tar(files, "w:gz")),
        ("m.tar.xz", lambda files: make_tar(files, "w:xz")),
        ("m.tar", lambda files: make_tar(files, "w")),
        ("m.zip", make_zip),
    ],
)
def test_other_archive_formats(server, tmp_path, name, build):
    url = server.add(name, build(MODEL_FILES))
    result = fetch_archive(url, tmp_path)
    assert result == tmp_path / MODEL  # a single top-level folder is the result when no member is named
    assert_model_installed(result)


def test_archive_with_several_top_level_entries_returns_dest(server, tmp_path):
    url = server.add("pair.zip", make_zip({"a.onnx": b"A", "b/tokens.txt": b"B"}))
    assert fetch_archive(url, tmp_path) == tmp_path
    assert (tmp_path / "a.onnx").read_bytes() == b"A" and (tmp_path / "b" / "tokens.txt").read_bytes() == b"B"
    assert fetch_archive(url, tmp_path, expected_member="b/tokens.txt") == tmp_path / "b" / "tokens.txt"


def test_stale_folder_without_marker_is_replaced(server, tmp_path):
    stale = tmp_path / MODEL
    stale.mkdir()
    (stale / "half-written.onnx").write_bytes(b"junk")
    url = server.add(f"{MODEL}.tar.bz2", make_tar(MODEL_FILES))
    assert not modelfetch.is_fetched(url, tmp_path)
    folder = fetch_archive(url, tmp_path, expected_member=MODEL)
    assert not (folder / "half-written.onnx").exists()
    assert_model_installed(folder)


def test_file_modes_are_sanitised(server, tmp_path):
    extra = [file_info(f"{MODEL}/run.sh", mode=0o4777), file_info(f"{MODEL}/data.bin", mode=0o666)]
    url = server.add(f"{MODEL}.tar.gz", make_tar(MODEL_FILES, "w:gz", extra))
    folder = fetch_archive(url, tmp_path, expected_member=MODEL)
    assert stat.S_IMODE((folder / "run.sh").stat().st_mode) == 0o755  # executable kept, setuid and o+w gone
    assert stat.S_IMODE((folder / "data.bin").stat().st_mode) == 0o644


def test_helpers():
    assert modelfetch.archive_name("https://x.test/a/b/model.tar.bz2?token=1#frag") == "model.tar.bz2"
    assert modelfetch.archive_name("https://x.test/a/my%20model.zip") == "my model.zip"
    assert modelfetch.archive_kind("m.TAR.BZ2") == "tar" and modelfetch.archive_kind("m.zip") == "zip"
    assert modelfetch.archive_kind("m.onnx") is None
    with pytest.raises(ValueError):
        modelfetch.archive_name("https://x.test/")
    text = modelfetch.manual_instructions("https://x.test/m.tar.bz2", "/models dir", expected_member="m")
    assert "https://x.test/m.tar.bz2" in text and 'tar -xf ~/Downloads/m.tar.bz2 -C "/models dir"' in text
    assert "unzip" in modelfetch.manual_instructions("https://x.test/m.zip", "/d")


@pytest.mark.parametrize("url", ["file:///etc/passwd", "ftp://x.test/m.tar.gz", "m.tar.gz"])
def test_only_http_urls(tmp_path, url):
    with pytest.raises(ValueError, match="http"):
        fetch_archive(url, tmp_path)
    with pytest.raises(ValueError, match="http"):
        modelfetch.download_file(url, tmp_path / "x")


def test_environment_proxy_is_used(server, tmp_path, monkeypatch):
    """urllib's default opener honours http_proxy: the request for another host arrives at our 'proxy'."""
    server.files["/models/m.zip"] = make_zip(MODEL_FILES)
    monkeypatch.setenv("http_proxy", server.url)
    # urllib reads the proxy environment once, when it builds its shared opener; make it build a new one
    monkeypatch.setattr(urllib.request, "_opener", None)
    result = fetch_archive("http://models.invalid/models/m.zip", tmp_path, expected_member=MODEL)
    assert_model_installed(result)
    assert server.requests[0]["raw"] == "http://models.invalid/models/m.zip"


# -- network trouble -------------------------------------------------------------------------------


def test_404_is_reported_with_url_and_manual_alternative(server, tmp_path):
    url = f"{server.url}/no-such-model.tar.bz2"
    with pytest.raises(ModelFetchError) as err:
        fetch_archive(url, tmp_path / "models", expected_member="no-such-model")
    message = str(err.value)
    assert "404" in message and url in message
    assert "by hand" in message and str(tmp_path / "models") in message and "tar -xf" in message
    assert err.value.url == url and err.value.dest_dir == tmp_path / "models"
    assert len(server.requests) == 1  # a missing file is not retried
    assert not modelfetch.is_fetched(url, tmp_path / "models")


def test_interrupted_download_resumes_with_a_range_request(server, tmp_path):
    archive = make_tar(MODEL_FILES)
    name = f"{MODEL}.tar.bz2"
    url = server.add(name, archive)
    server.drop_after[f"/{name}"] = [40_000]

    folder = fetch_archive(url, tmp_path, expected_member=MODEL)

    assert_model_installed(folder)
    first, second = server.gets(name)
    assert first["range"] is None
    assert second["range"] == "bytes=40000-"
    assert second["if_range"] == f'"v1-{len(archive)}"'  # only continue if it is still the same file


def test_resume_survives_a_failed_run(server, tmp_path):
    archive = make_tar(MODEL_FILES)
    name = f"{MODEL}.tar.bz2"
    url = server.add(name, archive)
    server.drop_after[f"/{name}"] = [30_000, 0]  # 30 kB arrive, then the line is dead

    with pytest.raises(ModelFetchError) as err:
        fetch_archive(url, tmp_path, expected_member=MODEL, retries=0)
    assert "resumes" in str(err.value) and url in str(err.value)
    part = tmp_path / ".downloads" / f"{name}.part"
    assert part.stat().st_size == 30_000
    assert not (tmp_path / MODEL).exists()

    before = len(server.requests)
    folder = fetch_archive(url, tmp_path, expected_member=MODEL)  # "run the command again"
    assert_model_installed(folder)
    assert [r["range"] for r in server.requests[before:]] == ["bytes=30000-"]
    assert not part.exists()


def test_changed_remote_file_is_not_spliced_onto_the_old_part(server, tmp_path):
    name = "m.tar.gz"
    old = make_tar({f"{MODEL}/tokens.txt": os.urandom(60_000)}, "w:gz")
    url = server.add(name, old)
    server.drop_after[f"/{name}"] = [20_000, 0]
    with pytest.raises(ModelFetchError):
        fetch_archive(url, tmp_path, retries=0)

    new = make_tar(MODEL_FILES, "w:gz")
    server.files[f"/{name}"] = new
    server.etags[f"/{name}"] = '"v2"'
    folder = fetch_archive(url, tmp_path, expected_member=MODEL)
    assert_model_installed(folder)  # the new file, whole — not 20 kB of old bytes + the tail of the new one


def test_server_that_ignores_range_restarts_from_zero(server, tmp_path):
    name = f"{MODEL}.tar.bz2"
    url = server.add(name, make_tar(MODEL_FILES))
    server.ignore_range.add(f"/{name}")
    server.drop_after[f"/{name}"] = [50_000]
    assert_model_installed(fetch_archive(url, tmp_path, expected_member=MODEL))


def test_complete_partial_file_is_accepted_on_416(server, tmp_path):
    archive = make_tar(MODEL_FILES)
    name = f"{MODEL}.tar.bz2"
    url = server.add(name, archive)
    downloads = tmp_path / ".downloads"
    downloads.mkdir()
    (downloads / f"{name}.part").write_bytes(archive)  # the whole file arrived, then the process was killed
    (downloads / f"{name}.part.json").write_text(json.dumps({"url": url, "validator": "", "total": len(archive)}))
    assert_model_installed(fetch_archive(url, tmp_path, expected_member=MODEL))
    assert server.gets(name)[0]["range"] == f"bytes={len(archive)}-"


def test_unknown_partial_file_is_discarded(server, tmp_path):
    name = f"{MODEL}.tar.bz2"
    url = server.add(name, make_tar(MODEL_FILES))
    downloads = tmp_path / ".downloads"
    downloads.mkdir()
    (downloads / f"{name}.part").write_bytes(b"left over from who knows what")
    assert_model_installed(fetch_archive(url, tmp_path, expected_member=MODEL))
    assert server.gets(name)[0]["range"] is None


def test_temporary_server_errors_are_retried(server, tmp_path):
    name = f"{MODEL}.tar.bz2"
    url = server.add(name, make_tar(MODEL_FILES))
    server.statuses[f"/{name}"] = [503, 500]
    assert_model_installed(fetch_archive(url, tmp_path, expected_member=MODEL))
    assert len(server.gets(name)) == 3


def test_persistent_server_error_gives_up(server, tmp_path):
    name = f"{MODEL}.tar.bz2"
    url = server.add(name, make_tar(MODEL_FILES))
    server.statuses[f"/{name}"] = [503] * 10
    with pytest.raises(ModelFetchError, match="503"):
        fetch_archive(url, tmp_path, retries=2)
    assert len(server.gets(name)) == 3  # one try + two retries


def test_connection_refused_explains_what_to_do(tmp_path):
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]  # nothing listens here once the socket is closed
    url = f"http://127.0.0.1:{port}/{MODEL}.tar.bz2"
    with pytest.raises(ModelFetchError) as err:
        fetch_archive(url, tmp_path, expected_member=MODEL, retries=1)
    message = str(err.value)
    assert url in message and "internet connection" in message and "by hand" in message
    assert str(tmp_path / MODEL) in message


def test_stalled_connection_times_out(server, tmp_path):
    name = f"{MODEL}.tar.bz2"
    url = server.add(name, make_tar(MODEL_FILES))
    server.stall.add(f"/{name}")
    started = time.monotonic()
    with pytest.raises(ModelFetchError, match="stalled"):
        fetch_archive(url, tmp_path, timeout=0.3, retries=1)
    assert time.monotonic() - started < 5
    assert len(server.gets(name)) == 2


def test_progress_callback_error_aborts_but_keeps_the_partial_file(server, tmp_path):
    name = f"{MODEL}.tar.bz2"
    url = server.add(name, make_tar(MODEL_FILES))

    def cancel(done: int, total: int | None) -> None:
        if done > 0:
            raise KeyboardInterrupt  # what Ctrl-C looks like from inside the download loop

    with pytest.raises(KeyboardInterrupt):
        fetch_archive(url, tmp_path, progress=cancel)
    assert (tmp_path / ".downloads" / f"{name}.part").stat().st_size > 0
    assert not (tmp_path / MODEL).exists() and leftovers(tmp_path) == []
    assert_model_installed(fetch_archive(url, tmp_path, expected_member=MODEL))
    assert server.gets(name)[-1]["range"] is not None


def test_two_fetches_at_once_download_only_once(server, tmp_path):
    name = f"{MODEL}.tar.bz2"
    url = server.add(name, make_tar(MODEL_FILES))
    server.delay = 0.2
    results: list[Any] = []

    def worker() -> None:
        try:
            results.append(fetch_archive(url, tmp_path, expected_member=MODEL))
        except Exception as exc:  # pragma: no cover - shown by the assertion below
            results.append(exc)

    threads = [threading.Thread(target=worker) for _ in range(2)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(30)
    assert results == [tmp_path / MODEL, tmp_path / MODEL]
    assert len(server.gets(name)) == 1


def test_not_enough_disk_space_is_reported_before_downloading(server, tmp_path, monkeypatch):
    name = f"{MODEL}.tar.bz2"
    url = server.add(name, make_tar(MODEL_FILES))
    usage = type("Usage", (), {"free": 1000, "total": 10**12, "used": 10**12 - 1000})
    monkeypatch.setattr(modelfetch.shutil, "disk_usage", lambda path: usage)
    with pytest.raises(ModelFetchError, match="free disk space"):
        fetch_archive(url, tmp_path)
    assert len(server.gets(name)) == 1


# -- hostile and broken archives ---------------------------------------------------------------------


def fetch_expecting_refusal(server, tmp_path, name: str, data: bytes, match: str) -> None:
    """Serve a hostile archive; it must be refused and leave no trace inside or outside dest."""
    url = server.add(name, data)
    dest = tmp_path / "sandbox" / "models"
    with pytest.raises(UnsafeArchiveError, match=match) as err:
        fetch_archive(url, dest)
    assert "NOT unpacked" in str(err.value) and "by hand" in str(err.value)
    assert "tar -xf" not in str(err.value)  # never tell the user to unpack a hostile archive themselves
    survivors = sorted(p.relative_to(tmp_path).as_posix() for p in (tmp_path / "sandbox").rglob("*") if p.is_file())
    assert all(s.startswith("sandbox/models/.downloads/") for s in survivors), survivors
    assert not (dest / ".downloads" / name).exists()  # the hostile bytes are not kept for a retry
    assert not modelfetch.is_fetched(url, dest)
    assert leftovers(dest) == []


def test_parent_traversal_member_is_refused(server, tmp_path):
    data = make_tar({f"{MODEL}/ok.txt": b"fine", "../evil.txt": b"gotcha", f"{MODEL}/../../evil2.txt": b"gotcha"})
    fetch_expecting_refusal(server, tmp_path, "evil.tar.bz2", data, "leave the destination")
    assert not (tmp_path / "sandbox" / "evil.txt").exists() and not (tmp_path / "evil2.txt").exists()


def test_absolute_member_is_refused(server, tmp_path):
    target = tmp_path / "absolute-evil.txt"
    fetch_expecting_refusal(server, tmp_path, "abs.tar.gz", make_tar({str(target): b"gotcha"}, "w:gz"), "absolute")
    assert not target.exists()


def test_symlink_escape_is_refused(server, tmp_path):
    outside = tmp_path / "outside"
    outside.mkdir()
    # a link out of the tree, then a file written "into" it
    extra = [link_info(f"{MODEL}/escape", str(outside)), file_info(f"{MODEL}/escape/pwned.txt")]
    fetch_expecting_refusal(server, tmp_path, "symlink.tar.bz2", make_tar(MODEL_FILES, extra=extra), "absolute")
    assert list(outside.iterdir()) == []


def test_relative_symlink_escape_is_refused(server, tmp_path):
    extra = [link_info(f"{MODEL}/up", "../../.."), file_info(f"{MODEL}/up/pwned.txt")]
    fetch_expecting_refusal(server, tmp_path, "uplink.tar.bz2", make_tar(MODEL_FILES, extra=extra), "leaves its folder")
    assert not (tmp_path / "pwned.txt").exists()


def test_writing_through_an_inner_symlink_is_refused(server, tmp_path):
    # the link itself is harmless (it points down), but nothing may be written through a link
    extra = [link_info(f"{MODEL}/alias", "test_wavs"), file_info(f"{MODEL}/alias/extra.txt")]
    fetch_expecting_refusal(server, tmp_path, "through.tar.bz2", make_tar(MODEL_FILES, extra=extra), "through the link")


def test_hard_link_to_outside_is_refused(server, tmp_path):
    secret = tmp_path / "secret.txt"
    secret.write_text("private")
    extra = [link_info(f"{MODEL}/copy", "../../secret.txt", tarfile.LNKTYPE)]
    fetch_expecting_refusal(server, tmp_path, "hard.tar.bz2", make_tar(MODEL_FILES, extra=extra), "leave the destination")


def test_device_file_is_refused(server, tmp_path):
    fifo = tarfile.TarInfo(f"{MODEL}/pipe")
    fifo.type = tarfile.FIFOTYPE
    fetch_expecting_refusal(server, tmp_path, "fifo.tar.bz2", make_tar(MODEL_FILES, extra=[fifo]), "special file")


def test_zip_traversal_and_symlink_are_refused(server, tmp_path):
    fetch_expecting_refusal(
        server, tmp_path, "evil.zip", make_zip({f"{MODEL}/a": b"1", "../evil.txt": b"2"}), "leave the destination"
    )
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        link = zipfile.ZipInfo(f"{MODEL}/escape")
        link.external_attr = (stat.S_IFLNK | 0o777) << 16
        zf.writestr(link, "/etc")
    fetch_expecting_refusal(server, tmp_path, "link.zip", buf.getvalue(), "absolute")


def test_reserved_top_level_names_are_refused(server, tmp_path):
    fetch_expecting_refusal(server, tmp_path, "sneaky.zip", make_zip({".downloads/x": b"1"}), "reserved name")


def test_harmless_links_inside_the_archive_are_kept(server, tmp_path):
    extra = [
        link_info(f"{MODEL}/tokens-link.txt", "tokens.txt"),
        link_info(f"{MODEL}/hard-copy.txt", f"{MODEL}/tokens.txt", tarfile.LNKTYPE),
    ]
    url = server.add(f"{MODEL}.tar.bz2", make_tar(MODEL_FILES, extra=extra))
    folder = fetch_archive(url, tmp_path, expected_member=MODEL)
    assert (folder / "tokens-link.txt").is_symlink()
    assert (folder / "tokens-link.txt").read_bytes() == MODEL_FILES[f"{MODEL}/tokens.txt"]
    assert not (folder / "hard-copy.txt").is_symlink()
    assert (folder / "hard-copy.txt").read_bytes() == MODEL_FILES[f"{MODEL}/tokens.txt"]


def test_damaged_archive_is_reported_and_downloaded_again_next_time(server, tmp_path):
    name = f"{MODEL}.tar.bz2"
    good = make_tar(MODEL_FILES)
    url = server.add(name, good[: len(good) // 2])  # a truncated upload on the server side
    with pytest.raises(ModelFetchError, match="damaged") as err:
        fetch_archive(url, tmp_path, expected_member=MODEL)
    assert "by hand" in str(err.value)
    assert not (tmp_path / MODEL).exists() and leftovers(tmp_path) == []
    assert not modelfetch.is_fetched(url, tmp_path)

    server.files[f"/{name}"] = good
    assert_model_installed(fetch_archive(url, tmp_path, expected_member=MODEL))
    assert len(server.gets(name)) == 2


def test_not_an_archive(server, tmp_path):
    with pytest.raises(ModelFetchError, match="damaged"):
        fetch_archive(server.add("noise.tar.gz", os.urandom(4000)), tmp_path)
    with pytest.raises(ModelFetchError, match="damaged"):
        fetch_archive(server.add("noise.zip", os.urandom(4000)), tmp_path)
    with pytest.raises(ModelFetchError, match="not a"):
        fetch_archive(server.add("model.onnx", b"onnx"), tmp_path)
    with pytest.raises(ModelFetchError, match="empty"):
        fetch_archive(server.add("empty.tar", make_tar({}, "w")), tmp_path)


def test_missing_expected_member(server, tmp_path):
    url = server.add("other.tar.bz2", make_tar({"other-model/tokens.txt": b"t"}))
    with pytest.raises(ModelFetchError, match="does not contain") as err:
        fetch_archive(url, tmp_path, expected_member=MODEL)
    assert "other-model" in str(err.value)
    assert not (tmp_path / "other-model").exists()  # nothing is installed from an archive that is not what was asked for
    with pytest.raises(UnsafeArchiveError):
        fetch_archive(url, tmp_path, expected_member="../elsewhere")


def test_unpacked_size_limit(server, tmp_path, monkeypatch):
    monkeypatch.setattr(modelfetch, "MAX_UNPACKED_BYTES", 10_000)
    url = server.add("bomb.tar.bz2", make_tar({"bomb/zeros.bin": b"\0" * 5_000_000}))
    with pytest.raises(ModelFetchError, match="refusing"):
        fetch_archive(url, tmp_path)
    assert not (tmp_path / "bomb").exists() and leftovers(tmp_path) == []


def test_crash_while_installing_never_leaves_a_usable_looking_model(server, tmp_path, monkeypatch):
    """Die between unpacking and the final rename: no marker, nothing under the final name."""
    name = f"{MODEL}.tar.bz2"
    url = server.add(name, make_tar(MODEL_FILES))
    real_replace = os.replace

    def failing_replace(src: Any, dst: Any) -> None:
        if Path(dst).name == MODEL:
            raise OSError(28, "No space left on device")
        real_replace(src, dst)

    monkeypatch.setattr(modelfetch.os, "replace", failing_replace)
    with pytest.raises(ModelFetchError, match="No space left"):
        fetch_archive(url, tmp_path, expected_member=MODEL)
    assert not (tmp_path / MODEL).exists()
    assert not modelfetch.is_fetched(url, tmp_path, expected_member=MODEL)
    assert leftovers(tmp_path) == []

    monkeypatch.setattr(modelfetch.os, "replace", real_replace)
    assert_model_installed(fetch_archive(url, tmp_path, expected_member=MODEL))
    assert len(server.gets(name)) == 1  # the intact archive was reused, not downloaded twice


def test_marker_for_another_url_does_not_count(server, tmp_path):
    url = server.add(f"{MODEL}.tar.bz2", make_tar(MODEL_FILES))
    fetch_archive(url, tmp_path, expected_member=MODEL)
    other = f"{server.url}/mirror/{MODEL}.tar.bz2"
    assert not modelfetch.is_fetched(other, tmp_path, expected_member=MODEL)
    modelfetch.marker_path(url, tmp_path).write_text("not json")
    assert not modelfetch.is_fetched(url, tmp_path, expected_member=MODEL)


def test_extract_archive_directly(tmp_path):
    archive = tmp_path / "m.tar.bz2"
    archive.write_bytes(make_tar(MODEL_FILES))
    assert modelfetch.extract_archive(archive, tmp_path / "out") == [MODEL]
    assert_model_installed(tmp_path / "out" / MODEL)
    odd = tmp_path / "download"
    odd.write_bytes(make_zip(MODEL_FILES))
    assert modelfetch.extract_archive(odd, tmp_path / "out2", kind="zip") == [MODEL]
