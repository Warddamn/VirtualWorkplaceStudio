"""The local web UI server: JSON API, keyframe and media files, and its security rules.

A real server (``make_server`` on port 0) runs in a thread against a library built
with the real ``Store``: a tiny real MP4 and real JPEG keyframes made by ffmpeg.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import signal
import socket
import subprocess
import sys
import textwrap
import threading
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from email.message import Message
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from urllib.parse import quote

import pytest

import videonotes
from videonotes.backends.base import BackendError, BackendUnavailable
from videonotes.config import Settings
from videonotes.media import ffmpeg as ff
from videonotes.models import (
    ActionItem,
    Answer,
    Clip,
    DayDigest,
    Evidence,
    Keyframe,
    Moment,
    Session,
    SessionNote,
    Utterance,
)
from videonotes.store import Store
from videonotes.timeutil import day_bounds
from videonotes.web import server as web
from videonotes.web.server import WebServerError, make_server, serve

DAY = "2026-11-22"
OLD_DAY = "2026-11-10"
SID = "20261122-100000-aaaa"
OLD_SID = "20261110-090000-bbbb"
SECRET = b"TOP-SECRET-CONTENT-THAT-MUST-NEVER-BE-SERVED"
STATIC = Path(web.__file__).parent / "static"

_OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))  # never through a proxy


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------


@dataclass
class Reply:
    status: int
    headers: Message
    body: bytes

    def json(self) -> Any:
        assert self.headers.get_content_type() == "application/json", self.body[:200]
        return json.loads(self.body)

    @property
    def error_code(self) -> str:
        return self.json()["error"]["code"]


def fetch(
    base: str, path: str, *, method: str = "GET", headers: dict[str, str] | None = None, data: bytes | None = None
) -> Reply:
    request = urllib.request.Request(base + path, data=data, method=method, headers=headers or {})
    try:
        with _OPENER.open(request, timeout=15) as response:
            return Reply(response.status, response.headers, response.read())
    except urllib.error.HTTPError as exc:
        with exc:
            return Reply(exc.code, exc.headers, exc.read())


def post_ask(base: str, payload: Any, **headers: str) -> Reply:
    data = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
    return fetch(base, "/api/ask", method="POST", data=data, headers={"Content-Type": "application/json", **headers})


def raw_request(port: int, request: bytes, *, timeout: float = 5.0) -> bytes:
    """Send bytes exactly as given (for requests urllib would never produce) and return the whole reply."""
    with socket.create_connection(("127.0.0.1", port), timeout=timeout) as sock:
        sock.sendall(request)
        chunks = []
        while True:
            try:
                chunk = sock.recv(65536)
            except TimeoutError:
                break
            if not chunk:
                break
            chunks.append(chunk)
    return b"".join(chunks)


def start(settings: Settings):
    server = make_server(settings, port=0)
    thread = threading.Thread(target=server.serve_forever, kwargs={"poll_interval": 0.05}, daemon=True)
    thread.start()
    return server, thread


def stop(server, thread) -> None:
    server.shutdown()
    server.server_close()
    thread.join(5)


# --------------------------------------------------------------------------
# a populated library
# --------------------------------------------------------------------------


@pytest.fixture(scope="module")
def media(tmp_path_factory) -> SimpleNamespace:
    """A tiny real MP4 and three real JPEGs, made once with ffmpeg."""
    if not ff.have_ffmpeg():
        pytest.skip("ffmpeg not installed")
    out = tmp_path_factory.mktemp("web-media")
    mp4 = out / "clip.mp4"
    ff.run(
        [
            "-f", "lavfi", "-i", "testsrc=s=160x90:r=10", "-f", "lavfi", "-i", "sine=f=440:r=16000", "-t", "2",
            "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-c:a", "aac",
            "-movflags", "+faststart", str(mp4),
        ],
        timeout=120,
    )  # fmt: skip
    jpegs = []
    for i, source in enumerate(("testsrc=s=320x180", "testsrc2=s=320x180", "color=c=0x1E3A5F:s=320x180")):
        jpg = out / f"kf_{i}.jpg"
        ff.run(["-f", "lavfi", "-i", source, "-frames:v", "1", "-q:v", "5", str(jpg)], timeout=60)
        jpegs.append(jpg)
    assert ff.probe(mp4).has_video and 1.5 < ff.probe(mp4).duration < 3
    assert all(j.read_bytes()[:2] == b"\xff\xd8" for j in jpegs)
    return SimpleNamespace(mp4=mp4, jpegs=jpegs)


def build_library(home: Path, media: SimpleNamespace) -> SimpleNamespace:
    settings = Settings(home=home)
    settings.ensure_dirs()
    outside = home.parent / (home.name + "-outside")
    outside.mkdir()
    (outside / "secret.jpg").write_bytes(SECRET)
    (outside / "secret.mp4").write_bytes(SECRET)
    (outside / "elsewhere.mp4").write_bytes(media.mp4.read_bytes())
    (home / "config.toml").write_bytes(SECRET)

    with Store(settings.db_path) as store:
        t0 = day_bounds(DAY)[0] + 10 * 3600  # 10:00 local
        store.create_session(
            Session(id=SID, kind="import", started_ts=t0, ended_ts=t0 + 600, source="/Volumes/OSMO/DCIM/DJI_001")
        )
        media_dir = settings.media_dir / SID
        media_dir.mkdir(parents=True)
        (media_dir / "clip.mp4").write_bytes(media.mp4.read_bytes())
        clip = store.add_clip(
            Clip(session_id=SID, path=f"media/{SID}/clip.mp4", fingerprint="fp-a", start_ts=t0, duration=600.0,
                 width=160, height=90, fps=10.0)
        )  # fmt: skip
        # a second, larger "clip" (random bytes) to exercise chunked streaming
        big = os.urandom(700_000)
        (media_dir / "big.mp4").write_bytes(big)
        big_clip = store.add_clip(
            Clip(session_id=SID, path=f"media/{SID}/big.mp4", fingerprint="fp-big", start_ts=t0 + 600, duration=60.0)
        )
        # a clip whose row points at a symlink that leaves the media folder
        os.symlink(outside / "secret.mp4", media_dir / "link.mp4")
        link_clip = store.add_clip(
            Clip(session_id=SID, path=f"media/{SID}/link.mp4", fingerprint="fp-link", start_ts=t0 + 700, duration=5.0)
        )

        frames_dir = settings.frames_dir / SID / f"clip{clip.id:06d}"
        frames_dir.mkdir(parents=True)
        rels = []
        for i, jpg in enumerate(media.jpegs):
            (frames_dir / f"kf_{i:04d}.jpg").write_bytes(jpg.read_bytes())
            rels.append(f"frames/{SID}/clip{clip.id:06d}/kf_{i:04d}.jpg")
        (frames_dir / "orphan.jpg").write_bytes(media.jpegs[0].read_bytes())  # on disk, not in the library
        os.symlink(outside / "secret.jpg", frames_dir / "leak.jpg")  # in the library, but leaves the folder
        board = "Launch plan Q3\nShip Falcon beta by June 14"
        kfs = store.replace_keyframes(clip.id, [
            Keyframe(clip_id=clip.id, session_id=SID, t=20, ts=t0 + 20, path=rels[0], ocr_text=board, ocr_backend="t",
                     caption="A whiteboard with a launch plan.", caption_backend="t"),
            Keyframe(clip_id=clip.id, session_id=SID, t=26, ts=t0 + 26, path=rels[1], ocr_text=board, ocr_backend="t"),
            Keyframe(clip_id=clip.id, session_id=SID, t=310, ts=t0 + 310, path=rels[2],
                     ocr_text="LEVEL 2 <script>alert(1)</script>", ocr_backend="t"),
            Keyframe(clip_id=clip.id, session_id=SID, t=320, ts=t0 + 320, path=f"frames/{SID}/clip{clip.id:06d}/leak.jpg"),
            Keyframe(clip_id=clip.id, session_id=SID, t=330, ts=t0 + 330, path=str(outside / "secret.jpg")),
        ])  # fmt: skip
        lines = [
            (10, "Okay let's start the planning meeting."),
            (20, "We decided to ship the Falcon beta on June fourteenth."),
            (30, "I need to call the vendor about the sensors."),
            (305, "I parked the car on level two, row G."),
        ]
        uts = store.replace_utterances(clip.id, [
            Utterance(clip_id=clip.id, session_id=SID, t0=t, t1=t + 5, ts0=t0 + t, ts1=t0 + t + 5, text=x)
            for t, x in lines
        ])  # fmt: skip
        moments = store.replace_moments(SID, [
            Moment(session_id=SID, idx=0, ts0=t0 + 10, ts1=t0 + 60, title="Planning meeting",
                   summary="Falcon beta date agreed.", tags=["falcon"], kind="meeting", salience="highlight",
                   keyframe_ids=[kfs[0].id, kfs[1].id], utterance_ids=[u.id for u in uts[:3]]),
            Moment(session_id=SID, idx=1, ts0=t0 + 60, ts1=t0 + 300, title="Quiet stretch", kind="idle",
                   salience="background"),
            Moment(session_id=SID, idx=2, ts0=t0 + 300, ts1=t0 + 340, title="Parking", summary="Parked on level two.",
                   kind="errand"),  # no ids: members are found by time
        ])  # fmt: skip
        note = SessionNote(
            title="Planning and parking", summary="Planned the Falcon beta. Then parked the car.",
            key_points=["Beta ships June 14"], decisions=["Ship on June 14"], open_questions=["Sensors in time?"],
            action_items=[ActionItem(text="Call the vendor", owner="me", due="Friday", ts=t0 + 30),
                          ActionItem(text="Made-up time", ts=42.0)],
            people=["Sarah"], places=["Car park"], captured_text=["Launch plan Q3"], tags=["planning"],
            llm_backend="extractive",
        )  # fmt: skip
        store.update_session(SID, note=note, title=note.title, status="ready", note_path="notes/sessions/x.md")
        store.save_day(DayDigest(
            date=DAY, headline="Falcon date fixed", summary="A planning day.", highlights=["Beta ships June 14"],
            action_items=[ActionItem(text="Call the vendor")], session_ids=[SID], llm_backend="extractive",
        ))  # fmt: skip

        old0 = day_bounds(OLD_DAY)[0] + 9 * 3600
        store.create_session(Session(id=OLD_SID, kind="live", started_ts=old0, status="processing", title=""))
        old_clip = store.add_clip(
            Clip(session_id=OLD_SID, path=str(outside / "elsewhere.mp4"), fingerprint="fp-b", start_ts=old0, duration=60.0)
        )
        store.replace_utterances(old_clip.id, [
            Utterance(clip_id=old_clip.id, session_id=OLD_SID, t0=1, t1=3, ts0=old0 + 1, ts1=old0 + 3,
                      text="I parked the car on the street near the bakery."),
        ])  # fmt: skip

    return SimpleNamespace(
        settings=settings, home=home, outside=outside, t0=t0, clip=clip.id, big_clip=big_clip.id, big=big,
        link_clip=link_clip.id, old_clip=old_clip.id, kf=[k.id for k in kfs], ut=[u.id for u in uts],
        moments=[m.id for m in moments], frame_rel=[r.removeprefix("frames/") for r in rels],
        frames_dir=frames_dir, mp4=media.mp4.read_bytes(), jpegs=[j.read_bytes() for j in media.jpegs],
    )  # fmt: skip


@pytest.fixture(scope="module")
def lib(tmp_path_factory, media) -> SimpleNamespace:
    return build_library(tmp_path_factory.mktemp("web-lib") / "home", media)


@pytest.fixture(scope="module")
def srv(lib):
    server, thread = start(lib.settings)
    yield SimpleNamespace(base=server.url.rstrip("/"), port=server.server_port, server=server)
    stop(server, thread)


@pytest.fixture()
def empty_srv(tmp_path):
    settings = Settings(home=tmp_path / "fresh")  # nothing created yet, like `vnote web` before `vnote init`
    server, thread = start(settings)
    yield SimpleNamespace(base=server.url.rstrip("/"), port=server.server_port, server=server, settings=settings)
    stop(server, thread)


# --------------------------------------------------------------------------
# static files and headers
# --------------------------------------------------------------------------


def test_index_is_served_with_security_headers(srv):
    for path in ("/", "/index.html"):
        r = fetch(srv.base, path)
        assert r.status == 200 and r.headers.get_content_type() == "text/html"
        assert b'<script src="/static/app.js" defer></script>' in r.body
    csp = r.headers["Content-Security-Policy"]
    assert "default-src 'none'" in csp and "script-src 'self'" in csp and "frame-ancestors 'none'" in csp
    assert "unsafe-inline" not in csp and "unsafe-eval" not in csp and "*" not in csp and "data:" not in csp
    assert r.headers["X-Content-Type-Options"] == "nosniff"
    assert r.headers["Cross-Origin-Resource-Policy"] == "same-origin"
    assert r.headers["Referrer-Policy"] == "no-referrer"
    assert r.headers["Server"] == "videonotes"  # no Python / library version advertised
    assert "Access-Control-Allow-Origin" not in r.headers


@pytest.mark.parametrize(
    ("name", "content_type"), [("app.js", "text/javascript"), ("style.css", "text/css"), ("index.html", "text/html")]
)
def test_static_files(srv, name, content_type):
    r = fetch(srv.base, f"/static/{name}")
    assert r.status == 200 and r.headers.get_content_type() == content_type
    assert r.body == (STATIC / name).read_bytes()
    assert r.headers["X-Content-Type-Options"] == "nosniff" and "Content-Security-Policy" in r.headers
    again = fetch(srv.base, f"/static/{name}", headers={"If-None-Match": r.headers["ETag"]})
    assert again.status == 304 and again.body == b""


@pytest.mark.parametrize(
    "path",
    ["/static", "/static/", "/static/nope.js", "/static/../server.py", "/static/%2e%2e/server.py", "/static/a/app.js",
     "/static/app.js/", "/server.py", "/nothing/here"],
)  # fmt: skip
def test_no_directory_listing_or_other_static_files(srv, path):
    r = fetch(srv.base, path)
    assert r.status in (400, 404)
    assert r.json()["error"]["message"]
    assert b"def make_server" not in r.body


def test_favicon(srv):
    r = fetch(srv.base, "/favicon.svg")
    assert r.status == 200 and r.headers.get_content_type() == "image/svg+xml" and r.body.startswith(b"<svg")


def test_page_sources_need_no_network_and_no_inline_code():
    html = (STATIC / "index.html").read_text(encoding="utf-8")
    js = (STATIC / "app.js").read_text(encoding="utf-8")
    css = (STATIC / "style.css").read_text(encoding="utf-8")
    for text in (html, js, css):
        assert not re.search(r"https?://|(?<![:\w/])//[\w.-]+\.\w+/", text), "no external resources of any kind"
    assert "@import" not in css and "url(" not in css
    # the CSP forbids inline script and style, so the page must not rely on either
    assert re.findall(r"<script\b[^>]*>", html) == ['<script src="/static/app.js" defer>']
    assert re.findall(r"<script\b[^>]*>(.*?)</script>", html, flags=re.S) == [""]  # nothing inline
    assert "<style" not in html and not re.search(r"\sstyle\s*=", html) and not re.search(r"\son\w+\s*=", html)
    # library text is only ever inserted as text
    code = re.sub(r"/\*.*?\*/", "", js, flags=re.S)
    for forbidden in ("innerHTML", "outerHTML", "insertAdjacentHTML", "document.write", "eval(", "new Function"):
        assert forbidden not in code
    assert all(img.count("alt=") == 1 for img in re.findall(r"<img\b[^>]*>", html))


# --------------------------------------------------------------------------
# JSON API
# --------------------------------------------------------------------------


def test_overview(srv, lib):
    r = fetch(srv.base, "/api/overview")
    assert r.status == 200 and r.headers["Cache-Control"] == "no-store"
    data = r.json()
    assert [d["date"] for d in data["days"]] == [DAY, OLD_DAY]  # newest first
    today = data["days"][0]
    assert today["sessions"] == 1 and today["label"] == "Sunday 22 November 2026" and today["short"] == "Sun 22 Nov"
    assert today["has_digest"] and today["headline"] == "Falcon date fixed" and today["month"] == "November 2026"
    assert data["days"][1]["has_digest"] is False
    assert data["library"]["sessions"] == 2 and data["library"]["keyframes"] == 5
    assert data["library"]["media_duration"] == "12 min"
    assert data["latest_session_id"] == SID
    assert str(lib.home) not in r.body.decode() and str(lib.outside) not in r.body.decode()


def test_sessions_for_a_day(srv, lib):
    data = fetch(srv.base, f"/api/sessions?day={DAY}").json()
    assert data["day"]["date"] == DAY
    (s,) = data["sessions"]
    assert s["id"] == SID and s["title"] == "Planning and parking" and s["kind"] == "import" and s["status"] == "ready"
    assert s["start"]["ts"] == lib.t0 and s["start"]["clock"] == "10:00" and s["end"]["clock"] == "10:10"
    assert s["start"]["text"] == "Sun 22 Nov 2026, 10:00" and s["start"]["day"] == DAY
    assert s["duration_s"] == 600 and s["duration"] == "10 min"
    assert s["summary"] == "Planned the Falcon beta. Then parked the car." and s["has_note"]
    assert s["source"] == "DJI_001"  # a path outside the library is reduced to its name
    thumb = fetch(srv.base, s["thumbnail"]["url"])  # first keyframe of the highlight moment
    assert thumb.status == 200 and thumb.body == lib.jpegs[0]
    assert s["thumbnail"]["alt"] == "A whiteboard with a launch plan."


def test_sessions_other_days_and_latest(srv):
    (old,) = fetch(srv.base, f"/api/sessions?day={OLD_DAY}").json()["sessions"]
    assert old["id"] == OLD_SID and old["untitled"] and old["title"] == "Untitled session"
    assert old["status"] == "processing" and old["summary"] == "" and old["thumbnail"] is None
    assert old["end"]["ts"] == old["start"]["ts"] + 60  # no end recorded: taken from its clips
    assert fetch(srv.base, "/api/sessions?day=2026-01-01").json()["sessions"] == []
    latest = fetch(srv.base, "/api/sessions").json()
    assert latest["day"] is None and [s["id"] for s in latest["sessions"]] == [SID, OLD_SID]
    assert [s["id"] for s in fetch(srv.base, "/api/sessions?limit=1").json()["sessions"]] == [SID]


def test_session_detail(srv, lib):
    r = fetch(srv.base, f"/api/session/{SID}")
    assert r.status == 200
    data = r.json()
    assert data["session"]["id"] == SID and data["session"]["note_path"] == "notes/sessions/x.md"
    note = data["note"]
    assert note["title"] == "Planning and parking" and note["key_points"] == ["Beta ships June 14"]
    assert note["decisions"] == ["Ship on June 14"] and note["open_questions"] == ["Sensors in time?"]
    assert note["people"] == ["Sarah"] and note["places"] == ["Car park"] and note["captured_text"] == ["Launch plan Q3"]
    assert note["tags"] == ["planning"] and note["llm_backend"] == "extractive"
    first, bogus = note["action_items"]
    assert first["text"] == "Call the vendor" and first["owner"] == "me" and first["due"] == "Friday"
    assert first["time"]["clock"] == "10:00" and first["time"]["ts"] == lib.t0 + 30
    assert bogus["time"] is None  # a time outside the recording is not shown as a clock time

    meeting, quiet, parking = data["moments"]
    assert (meeting["title"], meeting["kind"], meeting["salience"]) == ("Planning meeting", "meeting", "highlight")
    assert meeting["id"] == lib.moments[0] and meeting["tags"] == ["falcon"] and meeting["duration"] == "50 s"
    assert meeting["start"]["precise"] == "10:00:10" and meeting["end"]["precise"] == "10:01:00"
    assert [k["id"] for k in meeting["keyframes"]] == lib.kf[:2]
    kf = meeting["keyframes"][0]
    assert kf["caption"] == "A whiteboard with a launch plan." and kf["ocr_text"].startswith("Launch plan Q3")
    assert kf["time"]["ts"] == lib.t0 + 20 and kf["clip_id"] == lib.clip and kf["t"] == 20
    assert fetch(srv.base, kf["url"]).body == lib.jpegs[0]
    assert [line["text"] for line in meeting["transcript"]][1] == "We decided to ship the Falcon beta on June fourteenth."
    assert meeting["transcript"][0]["time"]["precise"] == "10:00:10" and meeting["transcript"][0]["t"] == 10
    assert meeting["play"] == {"clip_id": lib.clip, "t": 10.0}

    assert quiet["salience"] == "background" and quiet["keyframes"] == [] and quiet["transcript"] == []
    assert quiet["play"] == {"clip_id": lib.clip, "t": 60.0}

    # no ids stored for this moment: keyframes and speech are assigned by time
    assert parking["salience"] == "normal" and parking["kind"] == "errand"
    assert [k["id"] for k in parking["keyframes"]] == lib.kf[2:5]
    assert [line["id"] for line in parking["transcript"]] == [lib.ut[3]]
    # text from the library is passed through verbatim as JSON data; the page inserts it as text
    assert parking["keyframes"][0]["ocr_text"] == "LEVEL 2 <script>alert(1)</script>"
    assert b"<script>" not in r.body or r.headers.get_content_type() == "application/json"
    assert r.headers["X-Content-Type-Options"] == "nosniff"
    # keyframes whose file is not safely inside the frames folder get no URL
    assert parking["keyframes"][1]["url"] is None  # a symlink that leads out of the library
    assert parking["keyframes"][2]["url"] is None  # absolute path outside the library
    assert data["unassigned"] == {"keyframes": [], "transcript": []}

    clips = {c["id"]: c for c in data["clips"]}
    assert clips[lib.clip]["url"] == f"/media/{lib.clip}" and clips[lib.clip]["content_type"] == "video/mp4"
    assert clips[lib.clip]["duration"] == "10 min" and clips[lib.clip]["start"]["clock"] == "10:00"
    assert clips[lib.link_clip]["url"] is None  # symlink out of the media folder
    assert data["playable"] is True
    text = r.body.decode()
    assert str(lib.home) not in text and str(lib.outside) not in text and "/Volumes" not in text


def test_session_without_moments_or_media(srv, lib):
    data = fetch(srv.base, f"/api/session/{OLD_SID}").json()
    assert data["note"] is None and data["moments"] == [] and data["playable"] is False
    assert [line["text"] for line in data["unassigned"]["transcript"]] == [
        "I parked the car on the street near the bakery."
    ]
    (clip,) = data["clips"]
    assert clip["url"] is None  # analysed in place, outside the library: nothing to play


@pytest.mark.parametrize("ref", ["nope", "20261122-100000", "latest", "..", "%00", "x" * 300, SID + "%20"])
def test_unknown_session_is_404_json(srv, ref):
    r = fetch(srv.base, f"/api/session/{ref}")
    assert r.status in (400, 404)
    assert r.json()["error"]["code"] in ("unknown_session", "bad_path")


def test_day(srv):
    data = fetch(srv.base, f"/api/day/{DAY}").json()
    assert data["day"]["label"] == "Sunday 22 November 2026"
    digest = data["digest"]
    assert digest["headline"] == "Falcon date fixed" and digest["highlights"] == ["Beta ships June 14"]
    assert digest["action_items"][0]["text"] == "Call the vendor" and digest["session_ids"] == [SID]
    assert [s["id"] for s in data["sessions"]] == [SID]
    older = fetch(srv.base, f"/api/day/{OLD_DAY}").json()
    assert older["digest"] is None and [s["id"] for s in older["sessions"]] == [OLD_SID]
    nothing = fetch(srv.base, "/api/day/2026-01-01").json()
    assert nothing["digest"] is None and nothing["sessions"] == []


@pytest.mark.parametrize("bad", ["2026-13-45", "2026-02-30", "today", "20261122", "2026-11-22x", "0000-01-01", "%20", "x"])
def test_bad_dates_are_400(srv, bad):
    for path in (f"/api/day/{bad}", f"/api/sessions?day={bad}", f"/api/search?q=car&day={bad}"):
        r = fetch(srv.base, path)
        assert r.status == 400 and r.error_code == "bad_day", path


def test_search(srv, lib):
    data = fetch(srv.base, "/api/search?q=falcon+beta").json()
    assert data["query"] == "falcon beta" and data["count"] == len(data["hits"]) > 0 and data["truncated"] is False
    kinds = {h["kind"] for h in data["hits"]}
    assert {"utterance", "ocr", "moment", "session"} <= kinds
    for hit in data["hits"]:
        assert hit["session_id"] == SID and hit["session_title"] == "Planning and parking"
        assert "".join(p["text"] for p in hit["parts"]).replace("[", "").replace("]", "") == re.sub(
            r"\s+", " ", hit["snippet"].replace("[", "").replace("]", "")
        )
        assert any(p["match"] for p in hit["parts"])
        assert hit["time"]["day"] == DAY
    said = next(h for h in data["hits"] if h["kind"] == "utterance")
    assert said["utterance_id"] == lib.ut[1] and said["moment_id"] == lib.moments[0]
    assert said["moment_title"] == "Planning meeting" and said["time"]["precise"] == "10:00:20"
    assert [p["text"] for p in said["parts"] if p["match"]] == ["Falcon", "beta"]
    assert said["thumbnail"]["keyframe_id"] == lib.kf[0]  # nearest keyframe in time
    seen = next(h for h in data["hits"] if h["kind"] == "ocr")
    assert seen["keyframe_id"] == lib.kf[0] and seen["moment_id"] == lib.moments[0]
    assert fetch(srv.base, seen["thumbnail"]["url"]).body == lib.jpegs[0]
    moment = next(h for h in data["hits"] if h["kind"] == "moment")
    assert moment["moment_id"] == lib.moments[0] and moment["thumbnail"]["keyframe_id"] == lib.kf[0]


def test_search_folds_repeated_on_screen_text(srv, lib):
    hits = fetch(srv.base, "/api/search?q=launch+plan&kind=ocr").json()["hits"]
    # two keyframes of the same moment show the same whiteboard: one result, counted
    assert [(h["keyframe_id"], h["similar"]) for h in hits] == [(lib.kf[0], 1)]


def test_search_filters(srv):
    both = fetch(srv.base, "/api/search?q=parked+car").json()
    assert {h["session_id"] for h in both["hits"]} == {SID, OLD_SID}
    only = fetch(srv.base, f"/api/search?q=parked+car&day={OLD_DAY}").json()
    assert {h["session_id"] for h in only["hits"]} == {OLD_SID} and only["day"]["date"] == OLD_DAY
    assert only["hits"][0]["thumbnail"] is None and only["hits"][0]["moment_id"] is None
    speech = fetch(srv.base, "/api/search?q=falcon&kind=utterance").json()
    assert speech["kinds"] == ["utterance"] and {h["kind"] for h in speech["hits"]} == {"utterance"}
    two = fetch(srv.base, "/api/search?q=falcon&kind=ocr,caption&kind=moment").json()
    assert two["kinds"] == ["ocr", "caption", "moment"] and {h["kind"] for h in two["hits"]} <= {"ocr", "caption", "moment"}
    assert len(fetch(srv.base, "/api/search?q=falcon&limit=1").json()["hits"]) == 1
    assert fetch(srv.base, "/api/search?q=falcon&limit=1").json()["truncated"] is True
    assert fetch(srv.base, "/api/search?q=zebra").json()["hits"] == []


@pytest.mark.parametrize(
    "query",
    ["", "q=", "q=%20%20", "q=%ZZ%", "q=%22AND+%28+NEAR+%2A+OR", "q=%E2%82", "q=%00", "q=a&q=b", "q=%27%27%27", "junk",
     "q=caf%C3%A9&unknown=1", "=&=&", "q=" + "é" * 0 + "%F0%9F%9A%97"],
)  # fmt: skip
def test_search_survives_odd_queries(srv, query):
    r = fetch(srv.base, "/api/search?" + query)
    assert r.status == 200 and isinstance(r.json()["hits"], list)


@pytest.mark.parametrize(
    ("query", "code"),
    [
        ("q=car&kind=bogus", "bad_kind"),
        ("q=car&kind=ocr,nope", "bad_kind"),
        ("q=car&limit=abc", "bad_limit"),
        ("q=car&limit=0", "bad_limit"),
        ("q=car&limit=-5", "bad_limit"),
        ("q=car&limit=100000", "bad_limit"),
        ("q=" + "a" * 600, "bad_query"),
        ("&".join(f"a{i}=1" for i in range(60)), "bad_query"),
    ],
)
def test_malformed_query_strings_are_400(srv, query, code):
    r = fetch(srv.base, "/api/search?" + query)
    assert r.status == 400 and r.error_code == code
    assert fetch(srv.base, "/api/sessions?limit=abc").status == 400


def test_unknown_api_route(srv):
    for path in ("/api", "/api/", "/api/nope", "/api/session", "/api/session/a/b", "/api/day", "/api/overview/x"):
        r = fetch(srv.base, path)
        assert r.status in (400, 404) and r.json()["error"]["code"] in ("not_found", "bad_path"), path


# --------------------------------------------------------------------------
# POST /api/ask
# --------------------------------------------------------------------------


def test_ask(srv, lib, monkeypatch):
    calls = []

    def fake_ask(settings, store, question, **kwargs):
        calls.append((settings, store, question))
        return Answer(
            text="  On level two, row G.  ",
            llm_backend="fake:model",
            sources=[
                Evidence(kind="utterance", session_id=SID, ts=lib.t0 + 305, text="I parked the car\non level two.",
                         ref_id=str(lib.ut[3])),
                Evidence(kind="ocr", session_id=SID, ts=lib.t0 + 310, text="LEVEL 2", ref_id=str(lib.kf[2])),
                Evidence(kind="ocr", session_id=SID, ts=lib.t0 + 320, text="level  2\n", ref_id=str(lib.kf[3])),
                Evidence(kind="session", session_id=SID, ts=lib.t0, text="x" * 5000, ref_id=SID),
                Evidence(kind="utterance", session_id="deleted-session", ts=1.0, text="gone", ref_id="1"),
            ],
        )  # fmt: skip

    monkeypatch.setattr("videonotes.search.ask", fake_ask)
    r = post_ask(srv.base, {"question": "  where did I\n park?  "}, Origin=srv.base)
    assert r.status == 200
    data = r.json()
    assert calls == [(lib.settings, srv.server.store, "where did I park?")]
    assert data["answer"] == "On level two, row G." and data["llm_backend"] == "fake:model"
    assert data["extractive"] is False and data["question"] == "where did I park?"
    said, seen, note = data["sources"]  # the source from a deleted session is dropped
    assert said["kind"] == "utterance" and said["text"] == "I parked the car\non level two."
    assert said["session_title"] == "Planning and parking" and said["moment_id"] == lib.moments[2]
    assert said["utterance_id"] == lib.ut[3] and said["time"]["precise"] == "10:05:05"
    assert seen["keyframe_id"] == lib.kf[2] and fetch(srv.base, seen["thumbnail"]["url"]).body == lib.jpegs[2]
    assert seen["similar"] == 1 and said["similar"] == 0  # the same text read off a second frame is folded in
    assert len(note["text"]) <= 701 and note["text"].endswith("…")


def test_ask_extractive_answer_and_utf8(srv, monkeypatch):
    monkeypatch.setattr("videonotes.search.ask", lambda *a, **k: Answer(text="", llm_backend="extractive"))
    r = post_ask(srv.base, json.dumps({"question": "Où est la clé ? 🚗"}).encode("utf-8"))
    data = r.json()
    assert r.status == 200 and data["extractive"] is True and data["answer"] == "" and data["sources"] == []
    assert data["question"] == "Où est la clé ? 🚗"


def test_ask_backend_failures_are_json_errors_without_paths(srv, monkeypatch):
    def unavailable(*a, **k):
        raise BackendUnavailable("Ollama is not running. Start it with: ollama serve (models in /Users/me/.ollama/models)")

    monkeypatch.setattr("videonotes.search.ask", unavailable)
    r = post_ask(srv.base, {"question": "anything"})
    assert r.status == 503 and r.error_code == "backend_unavailable"
    message = r.json()["error"]["message"]
    assert "ollama serve" in message and "vnote doctor" in message and "/Users" not in message

    def failed(*a, **k):
        raise BackendError("model crashed reading /Users/me/VideoNotes/cache/prompt.txt")

    monkeypatch.setattr("videonotes.search.ask", failed)
    r = post_ask(srv.base, {"question": "anything"})
    assert r.status == 502 and r.error_code == "backend_error"
    assert "model crashed" in r.json()["error"]["message"] and "/Users" not in r.body.decode()

    def exploded(*a, **k):
        raise RuntimeError("boom in /Users/me/secret/place.py line 3")

    monkeypatch.setattr("videonotes.search.ask", exploded)
    r = post_ask(srv.base, {"question": "anything"})
    assert r.status == 500 and r.error_code == "internal_error"
    assert "boom" not in r.body.decode() and "/Users" not in r.body.decode() and "Traceback" not in r.body.decode()
    # ... and the server is still fine afterwards
    monkeypatch.setattr("videonotes.search.ask", lambda *a, **k: Answer(text="ok", llm_backend="x"))
    assert post_ask(srv.base, {"question": "anything"}).json()["answer"] == "ok"


@pytest.mark.parametrize(
    ("body", "status", "code"),
    [
        (b"not json", 400, "bad_json"),
        (b"\xff\xfe", 400, "bad_json"),
        (b"[" * 20000, 400, "bad_json"),
        (b"{}", 400, "bad_question"),
        (b"[]", 400, "bad_question"),
        (b'"where"', 400, "bad_question"),
        (b'{"question": 5}', 400, "bad_question"),
        (b'{"question": "   "}', 400, "bad_question"),
        (json.dumps({"question": "x" * 2001}).encode(), 400, "bad_question"),
        (b"", 400, "bad_json"),
        (b'{"question": "' + b"x" * 70_000 + b'"}', 413, "too_large"),
    ],
)
def test_ask_rejects_bad_bodies(srv, monkeypatch, body, status, code):
    monkeypatch.setattr("videonotes.search.ask", lambda *a, **k: pytest.fail("ask() must not run"))
    r = post_ask(srv.base, body)
    assert (r.status, r.error_code) == (status, code)


def test_ask_requires_json_post_from_this_origin(srv, monkeypatch):
    monkeypatch.setattr("videonotes.search.ask", lambda *a, **k: pytest.fail("ask() must not run"))
    body = json.dumps({"question": "where?"}).encode()
    for content_type in ("text/plain", "application/x-www-form-urlencoded", "multipart/form-data", "application/jsonx"):
        r = fetch(srv.base, "/api/ask", method="POST", data=body, headers={"Content-Type": content_type})
        assert r.status == 415 and r.error_code == "unsupported_media_type"
    for origin in ("http://evil.example", f"http://evil.example:{srv.port}", "null", f"https://127.0.0.1:{srv.port}",
                   f"http://127.0.0.1:{srv.port + 1}", "http://localhost"):  # fmt: skip
        r = post_ask(srv.base, body, Origin=origin)
        assert r.status == 403 and r.error_code == "forbidden_origin", origin
    r = post_ask(srv.base, body, **{"Sec-Fetch-Site": "cross-site"})
    assert r.status == 403 and r.error_code == "cross_site"
    r = fetch(srv.base, "/api/ask")
    assert r.status == 405 and r.headers["Allow"] == "POST"
    # a request without Content-Length is refused rather than read until the socket closes
    reply = raw_request(
        srv.port,
        f"POST /api/ask HTTP/1.1\r\nHost: 127.0.0.1:{srv.port}\r\nContent-Type: application/json\r\n\r\n".encode() + body,
    )
    assert reply.startswith(b"HTTP/1.1 411") and b"Connection: close" in reply


def test_ask_accepts_this_servers_origins(srv, monkeypatch):
    monkeypatch.setattr("videonotes.search.ask", lambda *a, **k: Answer(text="ok", llm_backend="x"))
    for origin in (f"http://127.0.0.1:{srv.port}", f"http://localhost:{srv.port}", f"HTTP://LOCALHOST:{srv.port}"):
        assert post_ask(srv.base, {"question": "q"}, Origin=origin, **{"Sec-Fetch-Site": "same-origin"}).status == 200
    r = post_ask(srv.base, json.dumps({"question": "q"}).encode(), **{"Content-Type": "application/json; charset=utf-8"})
    assert r.status == 200


def test_slow_ask_does_not_block_other_requests(srv, monkeypatch):
    started, release = threading.Event(), threading.Event()

    def slow_ask(*a, **k):
        started.set()
        assert release.wait(20)
        return Answer(text="finally", llm_backend="slow")

    monkeypatch.setattr("videonotes.search.ask", slow_ask)
    result: dict[str, Reply] = {}
    worker = threading.Thread(target=lambda: result.update(first=post_ask(srv.base, {"question": "slow one"})))
    worker.start()
    try:
        assert started.wait(10)
        t0 = time.monotonic()
        assert fetch(srv.base, "/api/overview").status == 200
        assert fetch(srv.base, f"/api/session/{SID}").status == 200
        assert time.monotonic() - t0 < 5
        busy = post_ask(srv.base, {"question": "second"})  # one question at a time
        assert busy.status == 429 and busy.error_code == "busy" and busy.headers["Retry-After"] == "5"
    finally:
        release.set()
        worker.join(20)
    assert result["first"].status == 200 and result["first"].json()["answer"] == "finally"
    release.set()
    assert post_ask(srv.base, {"question": "third"}).status == 200  # the lock was released


# --------------------------------------------------------------------------
# /frames
# --------------------------------------------------------------------------


def test_frames_are_served_with_type_and_cache_headers(srv, lib):
    url = f"/frames/{lib.frame_rel[1]}"
    for path in (f"{url}?k={lib.kf[1]}", url, f"{url}?k=999999", f"{url}?k=abc", f"{url}?k={lib.kf[0]}"):
        r = fetch(srv.base, path)  # with or without the keyframe id the API adds
        assert r.status == 200 and r.body == lib.jpegs[1], path
    assert r.headers.get_content_type() == "image/jpeg" and r.headers["Content-Length"] == str(len(lib.jpegs[1]))
    assert r.headers["Cache-Control"] == "private, max-age=86400" and r.headers["Last-Modified"]
    assert r.headers["X-Content-Type-Options"] == "nosniff" and "Accept-Ranges" not in r.headers
    cached = fetch(srv.base, url, headers={"If-None-Match": r.headers["ETag"]})
    assert cached.status == 304 and cached.body == b"" and cached.headers["ETag"] == r.headers["ETag"]
    head = fetch(srv.base, url, method="HEAD")
    assert head.status == 200 and head.body == b"" and head.headers["Content-Length"] == str(len(lib.jpegs[1]))
    ranged = fetch(srv.base, url, headers={"Range": "bytes=0-9"})
    assert ranged.status == 200 and ranged.body == lib.jpegs[1]  # ranges are a media-only feature


def test_frames_refuse_everything_outside_the_library(srv, lib):
    sid_dir = lib.frame_rel[0].rsplit("/", 1)[0]  # <session>/clip000001
    attempts = [
        f"/frames/{sid_dir}/orphan.jpg",  # exists in the folder, unknown to the library
        f"/frames/{sid_dir}/leak.jpg",  # known to the library, but a symlink out of the folder
        f"/frames/{sid_dir}/leak.jpg?k={lib.kf[3]}",
        f"/frames/{sid_dir}/secret.jpg?k={lib.kf[4]}",  # keyframe row with an absolute path elsewhere
        f"/frames/{quote(str(lib.outside / 'secret.jpg'), safe='')}?k={lib.kf[4]}",
        f"/frames/{str(lib.outside / 'secret.jpg').lstrip('/')}?k={lib.kf[4]}",
        "/frames/../config.toml",
        "/frames/%2e%2e/config.toml",
        "/frames/%2E%2E/library.db",
        "/frames/..%2fconfig.toml",
        "/frames/%252e%252e/config.toml",
        f"/frames/{SID}/../../config.toml",
        f"/frames/{SID}/%2e%2e/%2e%2e/config.toml",
        f"/frames/{SID}/..%5c..%5cconfig.toml",
        f"/frames/{sid_dir}/kf_0000.jpg/../../../../config.toml",
        f"/frames/{sid_dir}/kf_0000.jpg%00.txt",
        f"/frames/{sid_dir}/",
        f"/frames/{sid_dir}",
        f"/frames/{SID}",
        "/frames/",
        "/frames",
        "/frames//etc/passwd",
        "/frames/%2Fetc%2Fpasswd",
        "/frames/etc/passwd",
        f"/frames/{sid_dir}/kf_0000.JPG.exe",
        f"/frames/{sid_dir}/../clip000001/kf_0000.jpg",
        f"/frames/./{sid_dir}/kf_0000.jpg",
    ]
    for path in attempts:
        r = fetch(srv.base, path)
        assert r.status in (400, 404), path
        assert SECRET not in r.body and b"SQLite format" not in r.body and b"root:" not in r.body, path
        assert r.headers.get_content_type() == "application/json", path
    # the same through a raw socket, so no client-side URL clean-up can interfere
    reply = raw_request(srv.port, f"GET /frames/../config.toml HTTP/1.1\r\nHost: 127.0.0.1:{srv.port}\r\n\r\n".encode())
    assert reply.startswith(b"HTTP/1.1 400") and SECRET not in reply and b"Connection: close" in reply


def test_frame_that_disappeared_is_a_404(tmp_path, media):
    lib = build_library(tmp_path / "home", media)
    server, thread = start(lib.settings)
    try:
        base = server.url.rstrip("/")
        url = fetch(base, f"/api/session/{SID}").json()["moments"][0]["keyframes"][0]["url"]
        assert fetch(base, url).status == 200
        (lib.frames_dir / "kf_0000.jpg").unlink()  # e.g. the session's frames were deleted meanwhile
        gone = fetch(base, url)
        assert gone.status == 404 and gone.error_code == "not_found"
        assert fetch(base, f"/api/session/{SID}").json()["moments"][0]["keyframes"][0]["url"] is None
    finally:
        stop(server, thread)


# --------------------------------------------------------------------------
# /media with Range
# --------------------------------------------------------------------------


def test_media_full_and_head(srv, lib):
    r = fetch(srv.base, f"/media/{lib.clip}")
    assert r.status == 200 and r.body == lib.mp4
    assert r.headers.get_content_type() == "video/mp4" and r.headers["Accept-Ranges"] == "bytes"
    assert r.headers["Content-Length"] == str(len(lib.mp4)) and r.headers["ETag"]
    assert r.headers["X-Content-Type-Options"] == "nosniff" and r.headers["Cache-Control"].startswith("private")
    head = fetch(srv.base, f"/media/{lib.clip}", method="HEAD")
    assert head.status == 200 and head.body == b"" and head.headers["Content-Length"] == str(len(lib.mp4))
    assert head.headers["Accept-Ranges"] == "bytes"
    not_modified = fetch(srv.base, f"/media/{lib.clip}", headers={"If-None-Match": r.headers["ETag"]})
    assert not_modified.status == 304


def test_media_ranges(srv, lib):
    size = len(lib.mp4)
    url = f"/media/{lib.clip}"

    def ranged(spec: str, **extra: str) -> Reply:
        return fetch(srv.base, url, headers={"Range": spec, **extra})

    first = ranged("bytes=0-99")
    assert first.status == 206 and first.body == lib.mp4[:100]
    assert first.headers["Content-Range"] == f"bytes 0-99/{size}" and first.headers["Content-Length"] == "100"
    assert first.headers["Accept-Ranges"] == "bytes" and first.headers.get_content_type() == "video/mp4"

    middle = ranged("bytes=1000-1999")
    assert middle.status == 206 and middle.body == lib.mp4[1000:2000]
    assert middle.headers["Content-Range"] == f"bytes 1000-1999/{size}"

    one = ranged("bytes=5-5")
    assert one.status == 206 and one.body == lib.mp4[5:6]

    suffix = ranged("bytes=-500")
    assert suffix.status == 206 and suffix.body == lib.mp4[-500:]
    assert suffix.headers["Content-Range"] == f"bytes {size - 500}-{size - 1}/{size}"

    whole_suffix = ranged(f"bytes=-{size * 3}")  # longer than the file: all of it
    assert whole_suffix.status == 206 and whole_suffix.body == lib.mp4

    open_ended = ranged(f"bytes={size - 10}-")
    assert open_ended.status == 206 and open_ended.body == lib.mp4[-10:]

    browser = ranged("bytes=0-")  # what a <video> element sends first
    assert browser.status == 206 and browser.body == lib.mp4
    assert browser.headers["Content-Range"] == f"bytes 0-{size - 1}/{size}"

    clamped = ranged(f"bytes=100-{size + 5000}")
    assert clamped.status == 206 and clamped.body == lib.mp4[100:]
    assert clamped.headers["Content-Range"] == f"bytes 100-{size - 1}/{size}"

    head = fetch(srv.base, url, method="HEAD", headers={"Range": "bytes=0-99"})
    assert head.status == 206 and head.body == b"" and head.headers["Content-Length"] == "100"

    for spec in (f"bytes={size}-", f"bytes={size + 10}-{size + 20}", "bytes=-0", "bytes=99999999999999999-"):
        r = ranged(spec)
        assert r.status == 416 and r.error_code == "range_not_satisfiable", spec
        assert r.headers["Content-Range"] == f"bytes */{size}"

    # ranges that are malformed, in other units, or several at once are ignored: the whole file is sent
    for spec in ("bytes=abc", "bytes=5-2", "items=0-5", "bytes=0-1,5-9", "bytes=-", "bytes", "0-99", "bytes=1-2-3"):
        r = ranged(spec)
        assert r.status == 200 and r.body == lib.mp4 and "Content-Range" not in r.headers, spec

    # If-Range: only honour the range when the file is still the one the client has part of
    etag = first.headers["ETag"]
    assert ranged("bytes=0-9", **{"If-Range": etag}).status == 206
    stale = ranged("bytes=0-9", **{"If-Range": '"something-else"'})
    assert stale.status == 200 and stale.body == lib.mp4


def test_media_streams_large_files_in_chunks(srv, lib):
    assert len(lib.big) > web._CHUNK_BYTES * 2
    full = fetch(srv.base, f"/media/{lib.big_clip}")
    assert full.status == 200 and hashlib.sha256(full.body).digest() == hashlib.sha256(lib.big).digest()
    edge = web._CHUNK_BYTES
    part = fetch(srv.base, f"/media/{lib.big_clip}", headers={"Range": f"bytes={edge - 7}-{edge * 2 + 11}"})
    assert part.status == 206 and part.body == lib.big[edge - 7 : edge * 2 + 12]


def test_media_on_a_disk_that_fails_mid_stream(srv, lib, monkeypatch, caplog):
    import http.client

    real_fdopen = os.fdopen

    class Unplugged:
        """A file whose disk disappears after the first chunk was read."""

        def __init__(self, handle):
            self._handle, self._reads = handle, 0

        def __getattr__(self, name):
            return getattr(self._handle, name)

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            self._handle.close()

        def read(self, n=-1):
            self._reads += 1
            if self._reads > 1:
                raise OSError(5, "Input/output error")
            return self._handle.read(n)

    monkeypatch.setattr(web.os, "fdopen", lambda fd, mode="r", *a, **k: Unplugged(real_fdopen(fd, mode, *a, **k)))
    conn = http.client.HTTPConnection("127.0.0.1", srv.port, timeout=10)
    try:
        conn.request("GET", f"/media/{lib.big_clip}")
        response = conn.getresponse()
        assert response.status == 200  # the headers were already on their way
        with caplog.at_level("WARNING", logger="videonotes.web"), pytest.raises(http.client.IncompleteRead) as info:
            response.read()
        assert len(info.value.partial) == web._CHUNK_BYTES  # the connection was cut, not padded or left hanging
    finally:
        conn.close()
    monkeypatch.undo()
    assert any("disk unplugged" in rec.getMessage() for rec in caplog.records)
    assert "Traceback" not in caplog.text
    assert fetch(srv.base, f"/media/{lib.big_clip}").body == lib.big  # the server carries on


def test_media_refuses_unknown_and_outside_files(srv, lib):
    cases = {
        "/media/999999": "unknown_clip",
        "/media/abc": "unknown_clip",
        "/media/-1": "unknown_clip",
        "/media/1e3": "unknown_clip",
        "/media/" + "9" * 40: "unknown_clip",
        f"/media/{lib.clip}.mp4": "unknown_clip",
        f"/media/{lib.old_clip}": "media_unavailable",  # the file exists, but outside the library
        f"/media/{lib.link_clip}": "media_unavailable",  # symlink out of the media folder
    }
    for path, code in cases.items():
        r = fetch(srv.base, path)
        assert r.status == 404 and r.error_code == code, path
        assert SECRET not in r.body
    for path in (
        "/media", "/media/", f"/media/{lib.clip}/", f"/media/{lib.clip}/x", "/media/../library.db",
        "/media/%2e%2e/library.db", f"/media/{lib.clip}/../../library.db", "/media/..%2f..%2fconfig.toml",
        f"/media/{SID}/clip.mp4", f"/media/{quote(str(lib.outside / 'secret.mp4'), safe='')}",
    ):  # fmt: skip
        r = fetch(srv.base, path)
        assert r.status in (400, 404), path
        assert SECRET not in r.body and b"SQLite format" not in r.body and b"ftyp" not in r.body, path


# --------------------------------------------------------------------------
# Host / cross-site / method rules
# --------------------------------------------------------------------------


def test_requests_for_other_hosts_are_refused(srv, lib):
    paths = ["/", "/api/overview", f"/api/session/{SID}", f"/frames/{lib.frame_rel[0]}", f"/media/{lib.clip}",
             "/static/app.js"]  # fmt: skip
    bad_hosts = [
        "evil.example", f"evil.example:{srv.port}", f"127.0.0.1.evil.example:{srv.port}", f"localhost.evil.example:{srv.port}",
        "127.0.0.1", f"127.0.0.1:{srv.port + 1}", "localhost:80", f"192.168.1.20:{srv.port}", f"0.0.0.0:{srv.port}",
        f"127.0.0.1:{srv.port}@evil.example", f"evil.example@127.0.0.1:{srv.port}", f"[::2]:{srv.port}", "",
        f"127.0.0.1:{srv.port}, evil.example",
    ]  # fmt: skip
    for host in bad_hosts:
        for path in paths:
            r = fetch(srv.base, path, headers={"Host": host})
            assert r.status == 403 and r.error_code == "forbidden_host", (host, path)
            assert lib.mp4[:64] not in r.body and b"Planning" not in r.body
    r = post_ask(srv.base, {"question": "q"}, Host="evil.example")
    assert r.status == 403 and r.error_code == "forbidden_host"
    for host in (f"127.0.0.1:{srv.port}", f"localhost:{srv.port}", f"LOCALHOST:{srv.port}", f"localhost.:{srv.port}",
                 f"[::1]:{srv.port}"):  # fmt: skip
        assert fetch(srv.base, "/api/overview", headers={"Host": host}).status == 200, host


def test_requests_without_or_with_two_host_headers_are_refused(srv):
    no_host = raw_request(srv.port, b"GET /api/overview HTTP/1.0\r\n\r\n")
    assert no_host.startswith(b"HTTP/1.1 403") and b"forbidden_host" in no_host
    two = raw_request(
        srv.port, f"GET /api/overview HTTP/1.1\r\nHost: 127.0.0.1:{srv.port}\r\nHost: evil.example\r\n\r\n".encode()
    )
    assert two.startswith(b"HTTP/1.1 403") and b"Connection: close" in two
    ancient = raw_request(srv.port, b"GET /api/overview\r\n")  # HTTP/0.9: no headers at all
    assert b"forbidden_host" in ancient and b"sessions" not in ancient


def test_cross_site_requests_are_refused(srv, lib):
    def with_site(path: str, site: str, mode: str = "cors", dest: str = "empty") -> Reply:
        return fetch(srv.base, path, headers={"Sec-Fetch-Site": site, "Sec-Fetch-Mode": mode, "Sec-Fetch-Dest": dest})

    for site in ("cross-site", "same-site"):
        assert with_site("/api/overview", site).error_code == "cross_site"
        assert with_site(f"/api/session/{SID}", site, "navigate", "document").status == 403  # data is never a page
        assert with_site(f"/frames/{lib.frame_rel[0]}", site, "no-cors", "image").status == 403
        assert with_site(f"/media/{lib.clip}", site, "no-cors", "video").status == 403
        assert with_site("/static/app.js", site, "no-cors", "script").status == 403
        assert with_site("/", site, "no-cors", "iframe").status == 403
        assert with_site("/", site, "navigate", "iframe").status == 403
        assert with_site("/", site, "navigate", "document").status == 200  # following a link to the app is fine
    for site in ("same-origin", "none"):
        assert with_site("/api/overview", site).status == 200
        assert with_site(f"/frames/{lib.frame_rel[0]}", site, "no-cors", "image").status == 200


@pytest.mark.parametrize("method", ["POST", "PUT", "PATCH", "DELETE", "OPTIONS"])
def test_library_is_read_only_over_http(srv, lib, method):
    before = lib.settings.db_path.read_bytes()
    for path in ("/api/overview", f"/api/session/{SID}", f"/media/{lib.clip}", f"/frames/{lib.frame_rel[0]}", "/"):
        r = fetch(srv.base, path, method=method, data=b"{}" if method != "OPTIONS" else None,
                  headers={"Content-Type": "application/json"})  # fmt: skip
        assert r.status == 405 and r.error_code == "method_not_allowed", path
        assert r.headers["Allow"] == "GET, HEAD" and "Access-Control-Allow-Origin" not in r.headers
    if method != "POST":
        assert fetch(srv.base, "/api/ask", method=method).headers["Allow"] == "POST"
    assert fetch(srv.base, f"/api/session/{SID}").status == 200
    assert lib.settings.db_path.read_bytes() == before


def test_unknown_methods_and_garbage_get_json_errors(srv):
    reply = raw_request(srv.port, f"BREW /api/overview HTTP/1.1\r\nHost: 127.0.0.1:{srv.port}\r\n\r\n".encode())
    assert reply.startswith(b"HTTP/1.1 501") and b'"error"' in reply and b"BREW" not in reply
    reply = raw_request(srv.port, b"GET /<script>alert(1)</script> HTTP/9.9\r\n\r\n")
    assert reply.split(b"\r\n")[0].split()[1] in (b"400", b"505") and b"<script>" not in reply
    reply = raw_request(srv.port, b"\x00\x01\x02 nonsense\r\n\r\n")
    assert b"<script>" not in reply and b"Traceback" not in reply
    long_line = raw_request(srv.port, b"GET /" + b"a" * 70000 + b" HTTP/1.1\r\n\r\n")
    assert long_line.startswith(b"HTTP/1.1 414")
    assert fetch(srv.base, "/api/overview").status == 200  # still serving


def test_internal_errors_do_not_leak_details(srv, monkeypatch, caplog):
    def boom(self):
        raise RuntimeError("exploded while reading /Users/me/VideoNotes/library.db")

    monkeypatch.setattr(web.Library, "overview", boom)
    with caplog.at_level("ERROR", logger="videonotes.web"):
        r = fetch(srv.base, "/api/overview")
    assert r.status == 500 and r.error_code == "internal_error"
    assert "exploded" not in r.body.decode() and "/Users" not in r.body.decode()
    assert any("exploded" in (rec.exc_text or "") or rec.exc_info for rec in caplog.records)  # but it is logged

    import sqlite3

    def locked(self):
        raise sqlite3.OperationalError("database is locked: /Users/me/VideoNotes/library.db")

    monkeypatch.setattr(web.Library, "overview", locked)
    r = fetch(srv.base, "/api/overview")
    assert r.status == 503 and r.error_code == "library_unavailable" and "/Users" not in r.body.decode()


def test_keep_alive_connection_serves_several_requests(srv, lib):
    import http.client

    conn = http.client.HTTPConnection("127.0.0.1", srv.port, timeout=10)
    try:
        for path in ("/api/overview", f"/frames/{lib.frame_rel[0]}", "/api/nope", f"/media/{lib.clip}", "/"):
            conn.request("GET", path)
            response = conn.getresponse()
            body = response.read()
            assert response.version == 11 and len(body) == int(response.headers["Content-Length"])
        conn.request("HEAD", f"/media/{lib.clip}")
        assert conn.getresponse().read() == b""
        conn.request("GET", f"/media/{lib.clip}", headers={"Range": "bytes=0-9"})
        assert conn.getresponse().read() == lib.mp4[:10]
        # a refused POST leaves an unread body behind: the server must close rather than misread it
        conn.request("POST", "/api/ask", body=b'{"question":"x"}', headers={"Content-Type": "text/plain"})
        response = conn.getresponse()
        assert response.status == 415 and response.headers["Connection"] == "close"
        response.read()
    finally:
        conn.close()


def test_stalled_connections_are_dropped(lib, monkeypatch):
    monkeypatch.setattr(web._Handler, "timeout", 0.4)
    server, thread = start(lib.settings)
    try:
        with socket.create_connection(("127.0.0.1", server.server_port), timeout=5) as sock:
            sock.sendall(b"GET /api/overview HTTP/1.1\r\nHost: 127.0.0.1")  # ... and never finish the request
            t0 = time.monotonic()
            assert sock.recv(1024) == b""  # the server hangs up instead of holding a thread forever
            assert time.monotonic() - t0 < 4
    finally:
        stop(server, thread)


# --------------------------------------------------------------------------
# empty library, start-up and shutdown
# --------------------------------------------------------------------------


def test_empty_library(empty_srv):
    data = fetch(empty_srv.base, "/api/overview").json()
    assert data["days"] == [] and data["latest_session_id"] is None and data["library"]["sessions"] == 0
    assert fetch(empty_srv.base, "/api/sessions").json()["sessions"] == []
    assert fetch(empty_srv.base, "/api/search?q=anything").json()["hits"] == []
    assert fetch(empty_srv.base, "/api/day/2026-11-22").json()["sessions"] == []
    assert fetch(empty_srv.base, "/api/session/latest").status == 404
    assert fetch(empty_srv.base, "/").status == 200
    assert fetch(empty_srv.base, "/frames/a/b.jpg").status == 404 and fetch(empty_srv.base, "/media/1").status == 404
    # the page's empty state tells the user what to run
    js = (STATIC / "app.js").read_text(encoding="utf-8")
    assert "No sessions yet" in js and "vnote demo" in js and "vnote import" in js


def test_new_sessions_show_up_without_restart(empty_srv):
    with Store(empty_srv.settings.db_path) as other:  # e.g. `vnote import` running in another Terminal window
        t0 = day_bounds(DAY)[0] + 3600
        other.create_session(Session(id="20261122-010000-cccc", kind="file", started_ts=t0, title="Fresh"))
    data = fetch(empty_srv.base, "/api/overview").json()
    assert [d["date"] for d in data["days"]] == [DAY] and data["latest_session_id"] == "20261122-010000-cccc"
    detail = fetch(empty_srv.base, "/api/session/20261122-010000-cccc").json()
    assert detail["session"]["title"] == "Fresh" and detail["session"]["end"] is None and detail["clips"] == []


def test_make_server_only_listens_on_loopback(tmp_path):
    settings = Settings(home=tmp_path / "home")
    for host in ("0.0.0.0", "::", "192.168.1.10", "example.com", ""):
        with pytest.raises(WebServerError, match="only served to this computer"):
            make_server(settings, host=host, port=0)
    assert not settings.db_path.exists()  # nothing was opened for a refused start
    for port in (-1, 70000, True, "8765"):
        with pytest.raises(WebServerError, match="not a usable port"):
            make_server(settings, port=port)  # type: ignore[arg-type]
    server = make_server(settings, host="localhost", port=0)
    try:
        assert server.server_address[0] == "127.0.0.1" and server.server_port > 0
        assert server.url == f"http://127.0.0.1:{server.server_port}/"
    finally:
        server.server_close()
    assert server.store is None and server.library is None


def test_port_in_use_says_what_to_do(srv, lib):
    with pytest.raises(WebServerError, match="already in use") as info:
        make_server(lib.settings, port=srv.port)
    assert f"--port {srv.port + 1}" in info.value.hint

    lines: list[tuple[str, str]] = []
    out = SimpleNamespace(
        ok=lambda t: lines.append(("ok", t)), info=lambda t: lines.append(("info", t)),
        warn=lambda t: lines.append(("warn", t)), error=lambda t: lines.append(("error", t)),
        line=lambda t="": lines.append(("line", t)),
    )  # fmt: skip
    with pytest.raises(SystemExit) as exit_info:
        serve(lib.settings, port=srv.port, open_browser=False, out=out)
    assert exit_info.value.code == 1
    assert lines[0][0] == "error" and f"Port {srv.port} is already in use" in lines[0][1]
    assert lines[1] == ("line", f"  Use a different one:  vnote web --port {srv.port + 1}")
    with pytest.raises(WebServerError):  # without an `out` to print to, the caller gets the exception
        serve(lib.settings, port=srv.port, open_browser=False)


def test_unreadable_library_is_reported(tmp_path):
    home = tmp_path / "home"
    home.mkdir()
    (home / "library.db").write_bytes(b"this is not a database" * 100)
    with pytest.raises(WebServerError, match="could not be opened") as info:
        make_server(Settings(home=home), port=0)
    assert "vnote doctor" in info.value.hint


def test_serve_prints_the_address_opens_the_browser_and_stops_on_ctrl_c(tmp_path, monkeypatch):
    settings = Settings(home=tmp_path / "home")
    seen: dict[str, Any] = {}
    opened = threading.Event()

    def fake_serve_forever(self, poll_interval=0.5):
        seen["url"] = self.url
        seen["server"] = self
        assert opened.wait(5)
        raise KeyboardInterrupt  # the user presses Ctrl-C

    def fake_open(url):
        seen["opened"] = url
        opened.set()
        return True

    monkeypatch.setattr(web.VideoNotesServer, "serve_forever", fake_serve_forever)
    monkeypatch.setattr("webbrowser.open", fake_open)
    lines: list[str] = []
    out = SimpleNamespace(ok=lines.append, info=lines.append, warn=lines.append, error=lines.append, line=lines.append)
    assert serve(settings, port=0, open_browser=True, out=out) is None  # returns normally: no traceback, exit code 0
    assert seen["url"].startswith("http://127.0.0.1:") and seen["opened"] == seen["url"]
    assert any(seen["url"] in line for line in lines) and any("Ctrl-C" in line for line in lines)
    assert "stopped" in lines[-1]
    assert seen["server"].store is None  # library closed
    with socket.socket() as probe:  # and the port is free again
        probe.bind(("127.0.0.1", seen["server"].server_port))


def test_serve_warns_when_no_browser_can_be_opened(tmp_path, monkeypatch):
    warned = threading.Event()
    lines: list[str] = []

    def warn(text):
        lines.append(text)
        warned.set()

    def fake_serve_forever(self, poll_interval=0.5):
        assert warned.wait(5)
        raise KeyboardInterrupt

    monkeypatch.setattr(web.VideoNotesServer, "serve_forever", fake_serve_forever)
    monkeypatch.setattr("webbrowser.open", lambda url: False)
    out = SimpleNamespace(ok=lambda t: None, info=lambda t: None, warn=warn, error=lambda t: None, line=lambda t="": None)
    serve(Settings(home=tmp_path / "home"), port=0, open_browser=True, out=out)
    assert "Could not open a browser" in lines[0] and "http://127.0.0.1:" in lines[0]


def test_real_process_serves_and_exits_cleanly_on_sigint(tmp_path):
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
    code = textwrap.dedent(
        """
        import signal, sys
        from pathlib import Path
        from videonotes.cli.common import Out
        from videonotes.config import Settings
        from videonotes.web.server import serve

        signal.signal(signal.SIGINT, signal.default_int_handler)  # also when the test runner ignores SIGINT
        serve(Settings(home=Path(sys.argv[1])), port=int(sys.argv[2]), open_browser=False, out=Out())
        print("returned cleanly", flush=True)
        """
    )
    env = {**os.environ, "PYTHONPATH": str(Path(videonotes.__file__).parents[1]), "NO_COLOR": "1"}
    proc = subprocess.Popen(
        [sys.executable, "-c", code, str(tmp_path / "home"), str(port)],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env,
    )  # fmt: skip
    try:
        base = f"http://127.0.0.1:{port}"
        deadline = time.monotonic() + 20
        while True:
            try:
                assert fetch(base, "/api/overview").status == 200
                break
            except (urllib.error.URLError, ConnectionError):
                assert proc.poll() is None, proc.stderr.read()
                assert time.monotonic() < deadline, "server did not come up"
                time.sleep(0.1)
        proc.send_signal(signal.SIGINT)
        out, err = proc.communicate(timeout=20)
    finally:
        if proc.poll() is None:
            proc.kill()
            proc.communicate()
    assert proc.returncode == 0, err
    assert f"http://127.0.0.1:{port}/" in out and "Web UI stopped." in out and "returned cleanly" in out
    assert "Traceback" not in err


# --------------------------------------------------------------------------
# pure helpers
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("127.0.0.1:8765", ("127.0.0.1", 8765)),
        ("LocalHost:8765", ("localhost", 8765)),
        ("localhost", ("localhost", None)),
        ("[::1]:8765", ("[::1]", 8765)),
        ("[::1]", ("[::1]", None)),
        ("", None),
        ("host:port", None),
        ("host:", None),
        ("host:99999", None),
        ("host:123456", None),
        ("host:８７６５", None),
        ("[::1", None),
        ("[::1]x", None),
        ("a b", None),
        ("a/b", None),
        ("user@host", None),
        ("a,b", None),
    ],
)
def test_parse_host(value, expected):
    assert web.parse_host(value) == expected


def test_host_and_origin_rules():
    assert web.host_allowed("127.0.0.1:8765", 8765) and web.host_allowed("localhost:8765", 8765)
    assert web.host_allowed("[::1]:8765", 8765) and web.host_allowed("localhost", 80)
    assert not web.host_allowed("localhost", 8765) and not web.host_allowed("127.0.0.1:8766", 8765)
    assert not web.host_allowed(None, 8765) and not web.host_allowed("127.0.0.2:8765", 8765)
    assert not web.host_allowed("localhost.evil.example:8765", 8765) and not web.host_allowed("[::1].:8765", 8765)
    assert web.origin_allowed("http://127.0.0.1:8765", 8765) and web.origin_allowed("http://localhost:8765", 8765)
    assert not web.origin_allowed("https://127.0.0.1:8765", 8765) and not web.origin_allowed("null", 8765)
    assert not web.origin_allowed("http://127.0.0.1:8765/", 8765) and not web.origin_allowed("http://evil:8765", 8765)
    assert not web.origin_allowed(None, 8765) and not web.origin_allowed("file://", 8765)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("/", []),
        ("/api/overview", ["api", "overview"]),
        ("/frames/s/clip000001/kf%200.jpg", ["frames", "s", "clip000001", "kf 0.jpg"]),
        ("/a/%C3%A9", ["a", "é"]),
        ("/a/%252e%252e/b", ["a", "%2e%2e", "b"]),  # decoded once only: a harmless literal name
        ("", None),
        ("api", None),
        ("http://127.0.0.1/api", None),
        ("/a//b", None),
        ("/a/", None),
        ("/a/./b", None),
        ("/a/../b", None),
        ("/a/%2e%2e/b", None),
        ("/a/%2E/b", None),
        ("/a/b%2fc", None),
        ("/a/b%5cc", None),
        ("/a/b\\c", None),
        ("/a/%00", None),
        ("/a/%0a", None),
        ("/a/%7f", None),
        ("/a/%ff", None),
    ],
)
def test_split_path(raw, expected):
    assert web.split_path(raw) == expected


@pytest.mark.parametrize(
    ("header", "size", "expected"),
    [
        (None, 100, None),
        ("", 100, None),
        ("bytes=0-9", 100, (0, 9)),
        ("bytes=0-", 100, (0, 99)),
        ("bytes=90-200", 100, (90, 99)),
        ("bytes=-10", 100, (90, 99)),
        ("bytes=-500", 100, (0, 99)),
        (" bytes = 5 - 6 ", 100, (5, 6)),
        ("bytes=99-99", 100, (99, 99)),
        ("bytes=9-5", 100, None),
        ("bytes=0-1,3-4", 100, None),
        ("bytes=a-b", 100, None),
        ("bytes=-", 100, None),
        ("lines=0-5", 100, None),
        ("bytes=0-9", 0, "unsatisfiable"),
        ("bytes=-5", 0, "unsatisfiable"),
        ("bytes=-0", 100, "unsatisfiable"),
        ("bytes=100-", 100, "unsatisfiable"),
        ("bytes=100-150", 100, "unsatisfiable"),
    ],
)
def test_parse_range(header, size, expected):
    if expected == "unsatisfiable":
        with pytest.raises(web.RangeNotSatisfiable):
            web.parse_range(header, size)
    else:
        assert web.parse_range(header, size) == expected


def test_split_snippet_only_highlights_real_matches():
    words = web.query_words("Decided budgets café it's")
    assert words == ["decided", "budgets", "cafe", "it's"] or words == ["decided", "budgets", "cafe", "it", "s"]
    parts = web.split_snippet("we [deciding] on the [budget]\nfor array[0] and [x] at the [Café] … [inaudible]", words)
    assert [p["text"] for p in parts if p["match"]] == ["deciding", "budget", "Café"]
    # brackets that were in the recorded text itself stay exactly as they were
    assert "".join(p["text"] for p in parts if not p["match"]) == "we  on the  for array[0] and [x] at the  … [inaudible]"
    assert web.split_snippet("", words) == [] and web.split_snippet("plain", []) == [{"text": "plain", "match": False}]
    assert web.split_snippet("[[note]]", ["notes"]) == [
        {"text": "[", "match": False}, {"text": "note", "match": True}, {"text": "]", "match": False},
    ]  # fmt: skip
    hostile = web.split_snippet("<img src=x onerror=alert(1)> [falcon]", ["falcon"])
    assert hostile[0] == {"text": "<img src=x onerror=alert(1)> ", "match": False}  # data, never markup


def test_text_helpers():
    assert web.one_line("  a\n b  ") == "a b" and web.one_line(None) == ""
    long = "First sentence here. " + "word " * 80
    assert web.one_line(long, 50) == "First sentence here."  # ends at a sentence when that keeps enough
    assert web.one_line("Ok. " + "word " * 80, 60).startswith("Ok. word")  # ... but not a uselessly short one
    assert web.one_line("word " * 80, 30).endswith("…") and len(web.one_line("word " * 80, 30)) <= 31
    assert web.one_line("x" * 500, 40) == "x" * 40 + "…"
    assert web.excerpt("a  b\n\n\n\nc", 100) == "a b\n\nc" and web.excerpt("y" * 900).endswith("…")
    scrubbed = web.public_error_text(
        RuntimeError("cannot read /Users/me/VideoNotes/models/x.gguf or ~/Library/thing;\nsee http://127.0.0.1:11434/api")
    )
    assert "/Users" not in scrubbed and "Library" not in scrubbed and "http://127.0.0.1:11434/api" in scrubbed
    assert web.public_error_text(RuntimeError("pip install 'videonotes[mlx]'")) == "pip install 'videonotes[mlx]'"
    assert web._public_source("/Volumes/SD/DCIM") == "DCIM" and web._public_source("~/Movies/a.mp4") == "a.mp4"
    assert web._public_source("Osmo Action 4 (USB webcam)") == "Osmo Action 4 (USB webcam)"
    assert web._public_source("C:\\Users\\me\\clip.mp4") == "clip.mp4"
    assert web.json_bytes({"a": float("nan"), "b": [float("inf"), 1.5], "c": "é\ud83d"}) == (
        b'{"a":null,"b":[null,1.5],"c":"\\u00e9\\ud83d"}'
    )
    assert web.etag_matches('W/"abc", "def"', '"def"') and web.etag_matches("*", '"x"')
    assert not web.etag_matches('"abc"', '"def"') and not web.etag_matches(None, '"def"')


def test_day_labels():
    from datetime import date

    labels = web.Library.day_labels("2026-11-22", today=date(2026, 11, 22))
    assert labels == {
        "date": "2026-11-22", "label": "Sunday 22 November 2026", "short": "Sun 22 Nov", "month": "November 2026",
        "relative": "Today",
    }  # fmt: skip
    assert web.Library.day_labels("2026-11-21", today=date(2026, 11, 22))["relative"] == "Yesterday"
    assert web.Library.day_labels("2026-11-01", today=date(2026, 11, 22))["relative"] == ""
    assert web.Library.day_labels("2026-11-05", today=date(2026, 11, 22))["label"] == "Thursday 5 November 2026"
