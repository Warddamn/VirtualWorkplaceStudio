"""Card / folder / file import, against fake cards built with the exact DJI layout and names.

The media files are tiny but real (made with ffmpeg), so probing, stream-copy merging and
the library database all run for real.  A ".LRF" here is what DJI says it is: an MP4 with
another extension.
"""

from __future__ import annotations

import errno
import logging
import os
import shutil
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

from videonotes.capture import CaptureError, importer
from videonotes.capture.importer import CardClip, clip_fingerprint, group_into_sessions, parse_dji_name, scan_card
from videonotes.media import ffmpeg as ff
from videonotes.store import Store

pytestmark = pytest.mark.skipif(not ff.have_ffmpeg(), reason="ffmpeg not installed")

CLIP_SECONDS = 2.0


# ---------------------------------------------------------------------------------
# Fixtures: stock media and fake cards
# ---------------------------------------------------------------------------------


@pytest.fixture(scope="module")
def media(tmp_path_factory) -> dict[str, Path]:
    """Small real media files, rendered once: main (video+audio), proxies, a photo, a WAV."""
    folder = tmp_path_factory.mktemp("stock")
    video = ["-c:v", "libx264", "-preset", "ultrafast"] if ff.has_encoder("libx264") else ["-c:v", "mpeg4"]
    video += ["-pix_fmt", "yuv420p", "-g", "10"]
    tone = ["-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000"]

    def picture(size: str) -> list[str]:
        return ["-f", "lavfi", "-i", f"testsrc2=size={size}:rate=10"]

    out = {name: folder / name for name in ("main.mp4", "proxy.mp4", "silent_proxy.mp4", "photo.jpg", "backup.wav")}
    length = ["-t", str(CLIP_SECONDS)]
    stamp = ["-metadata", "creation_time=2026-11-22T18:15:00Z"]  # what a Mimo-synced camera in UTC-8 writes at 10:15
    sound = ["-c:a", "aac", "-b:a", "64k"]
    main = [*picture("320x240"), *tone, *length, *video, *sound, *stamp, "-f", "mp4", str(out["main.mp4"])]
    ff.run(main, timeout=120)
    ff.run([*picture("160x120"), *tone, *length, *video, *sound, "-f", "mp4", str(out["proxy.mp4"])], timeout=120)
    ff.run([*picture("160x120"), *length, *video, "-an", "-f", "mp4", str(out["silent_proxy.mp4"])], timeout=120)
    ff.run([*picture("640x480"), "-frames:v", "1", "-update", "1", str(out["photo.jpg"])], timeout=120)
    ff.run([*tone, "-t", "1", "-c:a", "pcm_s16le", str(out["backup.wav"])], timeout=120)
    return out


D = "DCIM/DJI_001"
# name -> stock file.  Times are camera-local wall clock on 2026-11-22.
CARD_FILES = {
    # a recording the camera split in two: the second file starts when the first ends
    f"{D}/DJI_20261122101500_0001_D.MP4": "main.mp4",
    f"{D}/DJI_20261122101500_0001_D.LRF": "proxy.mp4",
    f"{D}/DJI_20261122101502_0002_D.MP4": "main.mp4",
    f"{D}/DJI_20261122101502_0002_D.LRF": "proxy.mp4",
    # later: a clip whose proxy has no sound, with an audio backup and a photo taken right after
    f"{D}/DJI_20261122120000_0003_D.MP4": "main.mp4",
    f"{D}/DJI_20261122120000_0003_D.LRF": "silent_proxy.mp4",
    f"{D}/DJI_20261122120000_0003_D.WAV": "backup.wav",
    f"{D}/DJI_20261122120003_0004_D.JPG": "photo.jpg",
    f"{D}/DJI_20261122120003_0004_D.DNG": "photo.jpg",
    # loop-recording chapters (3-digit sub-index), no proxies
    f"{D}/DJI_20261122130000_0005_D_026.MP4": "main.mp4",
    f"{D}/DJI_20261122130002_0005_D_027.MP4": "main.mp4",
    # custom folder + file-name suffix (a camera setting)
    "DCIM/DJI_001_OA5/DJI_20260724070214_0002_D_DOA5.MP4": "main.mp4",
    "DCIM/DJI_001_OA5/DJI_20260724070214_0002_D_DOA5.LRF": "proxy.mp4",
    # thumbnails: same base names, never to be imported
    "MISC/THM/DJI_001/DJI_20261122101500_0001_D.THM": "photo.jpg",
    "MISC/THM/DJI_001/DJI_20261122101500_0001_D.SCR": "photo.jpg",
    # junk the scanner must ignore
    f"{D}/._DJI_20261122101500_0001_D.MP4": "photo.jpg",  # macOS AppleDouble litter
    f"{D}/.hidden.MP4": "main.mp4",
    f"{D}/readme.txt": "backup.wav",
}
EMPTY_FILES = (
    f"{D}/DJI_20261122140000_0006_D.MP4",  # zero-length main (card pulled while recording)...
    f"{D}/DJI_20261122140000_0006_D.LRF",  # ...and its zero-length proxy
)


def build_card(root: Path, media: dict[str, Path]) -> Path:
    for name, stock in CARD_FILES.items():
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(media[stock], target)
    for name in EMPTY_FILES:
        (root / name).write_bytes(b"")
    return root


@pytest.fixture()
def card(tmp_path: Path, media) -> Path:
    return build_card(tmp_path / "volumes" / "Untitled", media)


@pytest.fixture()
def tz(monkeypatch):
    """Switch the process time zone; always restored."""

    def use(name: str) -> None:
        monkeypatch.setenv("TZ", name)
        time.tzset()

    yield use
    monkeypatch.undo()
    time.tzset()


def local_ts(text: str, zone: str) -> float:
    return datetime.strptime(text, "%Y-%m-%d %H:%M:%S").replace(tzinfo=ZoneInfo(zone)).timestamp()


def snapshot(root: Path) -> dict[str, tuple[int, int]]:
    """Every file under root with its size and modification time: to prove nothing was touched."""
    return {
        str(p.relative_to(root)): (p.stat().st_size, p.stat().st_mtime_ns)
        for p in sorted(root.rglob("*"))
        if p.is_file()
    }


def library_files(settings) -> list[str]:
    return sorted(str(p.relative_to(settings.media_dir)) for p in settings.media_dir.rglob("*") if p.is_file())


# ---------------------------------------------------------------------------------
# Names and times
# ---------------------------------------------------------------------------------


def test_parse_dji_name_variants():
    plain = parse_dji_name("DJI_20260812131032_0006_D.MP4")
    assert (plain.prefix, plain.index, plain.sub_index, plain.suffix) == ("DJI", 6, None, None)
    assert plain.start_local == datetime(2026, 8, 12, 13, 10, 32)
    burst = parse_dji_name("DJI_20260811205751_0286_D_003.JPG")
    assert (burst.index, burst.sub_index, burst.suffix) == (286, 3, None)
    custom = parse_dji_name("DJI_20260724070214_0002_D_DOA5.LRF")
    assert (custom.index, custom.sub_index, custom.suffix) == (2, None, "DOA5")
    both = parse_dji_name("CAM_20260822234724_0075_D_027_A01.XRF")  # Xtra-branded body, chapter + suffix
    assert (both.prefix, both.index, both.sub_index, both.suffix) == ("CAM", 75, 27, "A01")
    assert parse_dji_name("dji_20260812131032_0006_d.mp4").index == 6  # a copy tool lower-cased it


@pytest.mark.parametrize(
    "name",
    ["holiday.mp4", "DJI_0001.MP4", "DJI_20261350101500_0001_D.MP4", "DJI_19700101000000_0001_D.MP4",
     "DJI_2026112210150_0001_D.MP4", "DJI_20261122101500_001_D.MP4", "GX010001.MP4", "DJI_20261122101500_0001_D"],
)  # fmt: skip
def test_parse_dji_name_rejects(name):
    assert parse_dji_name(name) is None


def test_file_name_time_is_camera_local_time_in_the_macs_zone(card, tz):
    name = "DJI_20261122101500_0001_D.MP4"
    for zone in ("America/Los_Angeles", "Europe/Berlin", "Asia/Tokyo", "UTC"):
        tz(zone)
        clip = next(c for c in scan_card(card) if c.original.name == name)
        assert clip.start_ts == local_ts("2026-11-22 10:15:00", zone), zone
        assert clip.time_source == "name"
    # The container says 18:15 UTC (see the fixture); the name wins anyway, whatever the zone.
    tz("Asia/Tokyo")
    assert clip.start_ts != datetime(2026, 11, 22, 18, 15, tzinfo=UTC).timestamp()
    # Summer time is honoured per date, not taken from "now".
    tz("Europe/Berlin")
    summer = next(c for c in scan_card(card) if c.original.name == "DJI_20260724070214_0002_D_DOA5.MP4")
    assert summer.start_ts == datetime(2026, 7, 24, 5, 2, 14, tzinfo=UTC).timestamp()  # CEST = UTC+2


def test_resolve_creation_time_detects_local_time_labelled_utc(tz):
    tz("Europe/Berlin")  # UTC+1 in November
    truth = datetime(2026, 11, 22, 9, 15, tzinfo=UTC).timestamp()  # recording really began 10:15 local
    labelled_correctly = truth
    labelled_local = datetime(2026, 11, 22, 10, 15, tzinfo=UTC).timestamp()  # "10:15Z": local clock labelled UTC
    mtime = truth + 600 + 3  # the camera closed the file when the 10-minute recording stopped
    assert importer.resolve_creation_time(labelled_correctly, 600, mtime) == truth
    assert importer.resolve_creation_time(labelled_local, 600, mtime) == truth
    # the file's times were lost (downloaded, copied): nothing to compare with, the label is believed
    assert importer.resolve_creation_time(labelled_local, 600, truth + 5_000_000) == labelled_local
    tz("UTC")
    assert importer.resolve_creation_time(labelled_local, 600, mtime) == labelled_local


# ---------------------------------------------------------------------------------
# Finding and scanning cards
# ---------------------------------------------------------------------------------


def test_find_camera_volumes(tmp_path, media, monkeypatch):
    volumes = tmp_path / "volumes"
    dji = build_card(volumes / "Untitled", media)
    xtra = volumes / "NO NAME"
    (xtra / "DCIM" / "CAM_001").mkdir(parents=True)  # Xtra-branded body, freshly formatted: folder only
    odd = volumes / "Backup"
    (odd / "DCIM" / "Camera roll").mkdir(parents=True)  # unusual folder, but DJI-named files inside
    shutil.copyfile(media["main.mp4"], odd / "DCIM" / "Camera roll" / "DJI_20261122101500_0001_D.MP4")
    (volumes / "iPhone" / "DCIM" / "100APPLE").mkdir(parents=True)  # some other camera
    (volumes / "Empty").mkdir()
    (volumes / ".Spotlight").mkdir()
    (volumes / "a file").write_text("x")
    (volumes / "Macintosh HD").symlink_to("/")  # how the boot volume appears under /Volumes
    (volumes / "Alias").symlink_to(dji)  # symlinks are never followed
    second = build_card(tmp_path / "direct-card", media)  # a root that is itself a card

    monkeypatch.setenv(importer.ENV_VOLUME_ROOTS, os.pathsep.join([str(volumes), str(second), str(tmp_path / "gone")]))
    assert importer.find_camera_volumes() == [odd, xtra, dji, second]
    monkeypatch.setenv(importer.ENV_VOLUME_ROOTS, "")
    if sys.platform != "darwin":
        assert importer.find_camera_volumes() == []
    assert importer._is_system_volume(Path("/"))


def test_find_camera_volumes_explains_blocked_volumes(tmp_path, media, monkeypatch, caplog):
    volumes = tmp_path / "volumes"
    good = build_card(volumes / "Card", media)
    (volumes / "Locked" / "DCIM").mkdir(parents=True)
    real = importer._looks_like_camera_card

    def guarded(volume: Path) -> bool:
        if volume.name == "Locked":
            raise PermissionError(errno.EPERM, "Operation not permitted")  # macOS "Removable Volumes" refusal
        return real(volume)

    monkeypatch.setattr(importer, "_looks_like_camera_card", guarded)
    monkeypatch.setenv(importer.ENV_VOLUME_ROOTS, str(volumes))
    with caplog.at_level(logging.WARNING, logger="videonotes.capture.importer"):
        assert importer.find_camera_volumes() == [good]  # the readable card is still found...
    assert "Removable Volumes" in caplog.text  # ...and the user is told about the other
    shutil.rmtree(good)
    with pytest.raises(CaptureError, match="Removable Volumes") as failure:  # nothing found: the likely reason
        importer.find_camera_volumes()
    assert str(volumes / "Locked") in str(failure.value) and "plug it in" in str(failure.value)

    def not_ours(volume: Path) -> bool:
        raise PermissionError(errno.EACCES, "Permission denied")  # somebody else's disk, not a privacy refusal

    monkeypatch.setattr(importer, "_looks_like_camera_card", not_ours)
    assert importer.find_camera_volumes() == []


MOUNT_OUTPUT = """\
/dev/disk3s1s1 on / (apfs, sealed, local, read-only, journaled)
devfs on /dev (devfs, local, nobrowse)
/dev/disk3s5 on /System/Volumes/Data (apfs, local, journaled, nobrowse, protect, root data)
map auto_home on /System/Volumes/Data/home (autofs, automounted, nobrowse)
/dev/disk4s1 on /Volumes/Untitled (exfat, local, nodev, nosuid, noowners)
/dev/disk5s1 on /Volumes/My (old) Card (msdos, local, nodev, nosuid, noowners)
//me@nas._smb._tcp.local/media on /Volumes/media (smbfs, nodev, nosuid, mounted by me)
nas:/export/video on /Volumes/video on nas (nfs)
"""


def test_parse_mount_table():
    table = importer.parse_mount_table(MOUNT_OUTPUT)
    assert table["/"] == "apfs" and table["/Volumes/Untitled"] == "exfat"
    assert table["/Volumes/My (old) Card"] == "msdos"  # brackets and spaces in a volume name
    assert table["/Volumes/media"] == "smbfs" and table["/Volumes/video on nas"] == "nfs"
    assert importer.parse_mount_table("") == {} and importer.parse_mount_table("nonsense\n(x)") == {}


def test_find_camera_volumes_never_looks_into_network_shares(tmp_path, media, monkeypatch):
    volumes = tmp_path / "volumes"
    card = build_card(volumes / "Untitled", media)
    share = build_card(volumes / "media", media)  # even if it looked like a card
    monkeypatch.setenv(importer.ENV_VOLUME_ROOTS, str(volumes))
    assert importer.find_camera_volumes() == [card, share]
    inspected: list[str] = []
    real = importer._looks_like_camera_card
    monkeypatch.setattr(importer, "_network_mount_points", lambda: {str(share)})
    monkeypatch.setattr(importer, "_looks_like_camera_card", lambda v: (inspected.append(v.name), real(v))[1])
    assert importer.find_camera_volumes() == [card]
    assert inspected == ["Untitled"]  # an unreachable server cannot stall the search
    monkeypatch.undo()
    assert importer._network_mount_points() == set() or sys.platform == "darwin"


def test_scan_card_pairs_proxies_and_ignores_junk(card, tz):
    tz("America/Los_Angeles")
    clips = scan_card(card)
    assert [(c.original.name, c.proxy.name if c.proxy else None, c.index) for c in clips] == [
        ("DJI_20260724070214_0002_D_DOA5.MP4", "DJI_20260724070214_0002_D_DOA5.LRF", 2),
        ("DJI_20261122101500_0001_D.MP4", "DJI_20261122101500_0001_D.LRF", 1),
        ("DJI_20261122101502_0002_D.MP4", "DJI_20261122101502_0002_D.LRF", 2),
        ("DJI_20261122120000_0003_D.MP4", "DJI_20261122120000_0003_D.LRF", 3),
        ("DJI_20261122120003_0004_D.JPG", None, 4),
        ("DJI_20261122130000_0005_D_026.MP4", None, 5),
        ("DJI_20261122130002_0005_D_027.MP4", None, 5),
    ]
    by_name = {c.original.name: c for c in clips}
    first = by_name["DJI_20261122101500_0001_D.MP4"]
    assert first.original.parent == card / "DCIM" / "DJI_001" and first.proxy.parent == first.original.parent
    assert first.size == first.original.stat().st_size and first.analysed == first.proxy
    assert first.duration is None  # nothing was probed: the names said it all
    photo = by_name["DJI_20261122120003_0004_D.JPG"]
    assert photo.is_photo and photo.duration == 0.0 and photo.analysed == photo.original
    assert photo.start_ts == local_ts("2026-11-22 12:00:03", "America/Los_Angeles")
    assert [c.start_ts for c in clips] == sorted(c.start_ts for c in clips)
    # the same answers when pointed at DCIM or at the folder itself
    assert [c.original for c in scan_card(card / "DCIM")] == [c.original for c in clips]
    assert len(scan_card(card / "DCIM" / "DJI_001")) == 6


def test_scan_card_orphan_proxy_and_xtra_names(tmp_path, media):
    folder = tmp_path / "card" / "DCIM" / "CAM_001"
    folder.mkdir(parents=True)
    shutil.copyfile(media["main.mp4"], folder / "CAM_20260822234724_0075_D.MP4")
    shutil.copyfile(media["proxy.mp4"], folder / "CAM_20260822234724_0075_D.XRF")
    shutil.copyfile(media["proxy.mp4"], folder / "CAM_20260822235000_0076_D.XRF")  # its main file was deleted
    (folder / "CAM_20260822235500_0077_D.MP4").write_bytes(b"")  # empty main...
    shutil.copyfile(media["proxy.mp4"], folder / "CAM_20260822235500_0077_D.XRF")  # ...with a good proxy
    clips = scan_card(tmp_path / "card")
    assert [(c.original.name, c.proxy.name if c.proxy else None) for c in clips] == [
        ("CAM_20260822234724_0075_D.MP4", "CAM_20260822234724_0075_D.XRF"),
        ("CAM_20260822235000_0076_D.XRF", None),  # the proxy still shows the recording
        ("CAM_20260822235500_0077_D.XRF", None),
    ]


def test_scan_plain_folder_of_videos(tmp_path, media, tz):
    tz("Europe/Berlin")
    folder = tmp_path / "Meeting recordings"
    (folder / "sub" / "deeper").mkdir(parents=True)
    shutil.copyfile(media["main.mp4"], folder / "kickoff.mp4")  # has creation_time 18:15 UTC
    ff.run(
        ["-i", str(media["proxy.mp4"]), "-c", "copy", str(folder / "sub" / "walk.mkv")], timeout=120
    )  # no creation_time
    shutil.copyfile(media["proxy.mp4"], folder / "sub" / "deeper" / "CLIP.MOV")
    shutil.copyfile(media["photo.jpg"], folder / "whiteboard.jpg")  # not named by the camera: not imported
    shutil.copyfile(media["photo.jpg"], folder / "DJI_20261122181700_0009_D.JPG")  # the camera's own photo: yes
    (folder / "broken.mp4").write_bytes(b"this is not a video" * 50)
    (folder / "empty.mp4").write_bytes(b"")
    (folder / "notes.txt").write_text("agenda")
    shutil.copyfile(media["main.mp4"], folder / ".trashed.mp4")
    mtime = datetime(2026, 11, 20, 9, 0, 30, tzinfo=UTC).timestamp()
    os.utime(folder / "sub" / "walk.mkv", (mtime, mtime))

    clips = {c.original.name: c for c in scan_card(folder)}
    assert sorted(clips) == ["CLIP.MOV", "DJI_20261122181700_0009_D.JPG", "kickoff.mp4", "walk.mkv"]
    kickoff = clips["kickoff.mp4"]
    assert kickoff.time_source == "creation_time"
    assert kickoff.start_ts == datetime(2026, 11, 22, 18, 15, tzinfo=UTC).timestamp()
    assert kickoff.duration == pytest.approx(CLIP_SECONDS, abs=0.2) and kickoff.index is None and kickoff.proxy is None
    walk = clips["walk.mkv"]  # no creation_time: when the file was finished, minus its length
    assert walk.time_source == "mtime" and walk.start_ts == pytest.approx(mtime - CLIP_SECONDS, abs=0.2)
    assert clips["DJI_20261122181700_0009_D.JPG"].time_source == "name"


def test_scan_card_errors_are_actionable(tmp_path, card, monkeypatch):
    with pytest.raises(CaptureError, match="still connected"):
        scan_card(tmp_path / "not there")
    (tmp_path / "file.txt").write_text("x")
    with pytest.raises(CaptureError, match="not a folder"):
        scan_card(tmp_path / "file.txt")
    (tmp_path / "nothing here" / "sub").mkdir(parents=True)
    (tmp_path / "nothing here" / "sub" / "notes.txt").write_text("x")
    assert scan_card(tmp_path / "nothing here") == []  # a folder without any media is simply empty
    assert len(scan_card(tmp_path / "volumes")) == 7  # the folder above a card: found a few levels down

    def refuse(path: Path) -> bool:
        raise PermissionError(errno.EPERM, "Operation not permitted")

    monkeypatch.setattr(importer, "_is_dir", refuse)
    with pytest.raises(CaptureError, match="Removable Volumes"):
        scan_card(card)

    def denied(path: Path) -> bool:
        raise PermissionError(errno.EACCES, "Permission denied")

    monkeypatch.setattr(importer, "_is_dir", denied)
    with pytest.raises(CaptureError, match="no permission to open it"):
        scan_card(card)


# ---------------------------------------------------------------------------------
# Sessions and fingerprints
# ---------------------------------------------------------------------------------


def _clip(start: float, duration: float | None, name: str = "x.mp4") -> CardClip:
    return CardClip(original=Path("/nowhere") / name, proxy=None, start_ts=start, size=1, index=None, duration=duration)


def test_group_into_sessions_uses_end_to_start_gaps():
    hour = 3600.0
    clips = [
        _clip(0, hour, "a"),
        _clip(hour + 1, hour, "b"),
        _clip(2 * hour + 2, 600, "c"),  # one recording in three parts
        _clip(2 * hour + 602 + 299, 10, "d"),  # 299 s after it ended: same session
        _clip(2 * hour + 911 + 300, 10, "e"),  # exactly the gap: a new session
        _clip(2 * hour + 911 + 305, 0, "photo.jpg"),  # a photo joins the session it falls into
    ]
    groups = group_into_sessions(list(reversed(clips)), 300)  # input order does not matter
    assert [[c.original.name for c in g] for g in groups] == [["a", "b", "c", "d"], ["e", "photo.jpg"]]
    assert group_into_sessions([], 300) == []
    # overlapping clips (two storage volumes, a clock that was set back) stay together
    assert len(group_into_sessions([_clip(100, 500), _clip(50, 10), _clip(590, 5)], 60)) == 1


def test_group_into_sessions_probes_lazily_and_proxies_first(card, monkeypatch):
    probed: list[str] = []
    real = ff.probe

    def spy(path, **kwargs):
        probed.append(Path(path).name)
        return real(path, **kwargs)

    monkeypatch.setattr(ff, "probe", spy)
    clips = [c for c in scan_card(card) if c.original.name.startswith("DJI_20261122")]
    assert probed == []  # scanning a camera card opens no media file at all: the names say when
    # A clip that starts within the gap of the previous start joins without measuring anything. A clip
    # far away needs the length of what came before (it could have run for hours): the small proxy is
    # measured, never the multi-gigabyte main file, never a photo, never the last session.
    groups = group_into_sessions(clips, 300)
    assert [len(g) for g in groups] == [2, 2, 2]
    assert probed == [
        "DJI_20261122101500_0001_D.LRF", "DJI_20261122101502_0002_D.LRF", "DJI_20261122120000_0003_D.LRF",
    ]  # fmt: skip
    assert clips[0].duration == pytest.approx(CLIP_SECONDS, abs=0.2)  # remembered on the clip

    # With a 1-second gap the lengths decide everything: the split recording (0 s between its parts)
    # stays together, the photo taken a second after its clip ended does not.
    groups = group_into_sessions(clips, 1.0)
    assert [[c.index for c in g] for g in groups] == [[1, 2], [3], [4], [5, 5]]
    assert probed[3:] == ["DJI_20261122130000_0005_D_026.MP4"]  # no proxy: the main file it is; nothing twice
    group_into_sessions(clips, 1.0)
    assert len(probed) == 4


def test_fingerprint_survives_remount_and_copy(tmp_path, card, media):
    original = card / D / "DJI_20261122101500_0001_D.MP4"
    fp = clip_fingerprint(original)
    assert fp == clip_fingerprint(original) and len(fp) == 40
    elsewhere = tmp_path / "another mount" / "DCIM" / "DJI_001"
    elsewhere.mkdir(parents=True)
    copy = Path(shutil.copy(original, elsewhere / original.name))  # new path, new mtime, same recording
    assert clip_fingerprint(copy) == fp
    # same content under another name is another recording (the continuation file here is a byte-identical copy)
    assert clip_fingerprint(card / D / "DJI_20261122101502_0002_D.MP4") != fp
    assert clip_fingerprint(card / D / "DJI_20261122101500_0001_D.LRF") != fp
    with open(copy, "ab") as handle:
        handle.write(b"\0")
    assert clip_fingerprint(copy) != fp
    with pytest.raises(CaptureError, match="still connected"):
        clip_fingerprint(tmp_path / "pulled out.mp4")


def test_fingerprint_reads_only_the_ends_of_a_big_file(tmp_path, monkeypatch):
    """A 16 GB original must fingerprint in milliseconds: only the first and last megabyte are read."""
    big = tmp_path / "DJI_20261122101500_0001_D.MP4"
    megabyte = 1024 * 1024
    big.write_bytes(b"".join(bytes([n]) * megabyte for n in range(8)))
    read: list[int] = []
    real_open = open

    class Counting:
        def __init__(self, handle):
            self._handle = handle

        def read(self, size=-1):
            data = self._handle.read(size)
            read.append(len(data))
            return data

        def __getattr__(self, name):
            return getattr(self._handle, name)

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            self._handle.close()

    monkeypatch.setattr(importer, "open", lambda path, mode="r": Counting(real_open(path, mode)), raising=False)
    fp = clip_fingerprint(big)
    assert sum(read) == 2 * megabyte  # of 8

    def poke(offset: int) -> str:
        with real_open(big, "r+b") as handle:
            handle.seek(offset)
            handle.write(b"\xff")
        return clip_fingerprint(big)

    assert poke(8 * megabyte - 1) != fp  # the last megabyte counts
    assert poke(10) != fp  # so does the first
    assert poke(4 * megabyte) == poke(4 * megabyte + 1)  # the middle is not read (size and both ends identify the file)

    # small files are hashed in full, without reading anything twice
    read.clear()
    small = tmp_path / "tiny.mp4"
    small.write_bytes(b"abc" * 1000)
    one = clip_fingerprint(small)
    assert sum(read) == 3000
    small.write_bytes(b"abd" * 1000)
    assert clip_fingerprint(small) != one
    middle = tmp_path / "middle.mp4"
    middle.write_bytes(b"x" * (megabyte + megabyte // 2))  # between one and two megabytes: no overlap, no gap
    read.clear()
    clip_fingerprint(middle)
    assert sum(read) == megabyte + megabyte // 2


# ---------------------------------------------------------------------------------
# Importing
# ---------------------------------------------------------------------------------


def test_import_default_mode_copies_proxies_and_never_touches_the_card(settings, store, card, tz, caplog):
    tz("America/Los_Angeles")
    before = snapshot(card)
    clips = scan_card(card)
    with caplog.at_level(logging.WARNING, logger="videonotes.capture.importer"):
        sessions = importer.import_clips(settings, store, clips, source=str(card))
    assert snapshot(card) == before  # read-only: same files, same sizes, same times
    assert caplog.text == ""

    assert [s.kind for s in sessions] == ["import"] * 4 and all(s.source == str(card) for s in sessions)
    assert all(s.status == "open" and store.get_session(s.id) is not None for s in sessions)
    listed = [[Path(c.original_path or c.path).name for c in store.list_clips(s.id)] for s in sessions]
    assert listed == [
        ["DJI_20260724070214_0002_D_DOA5.MP4"],
        ["DJI_20261122101500_0001_D.MP4", "DJI_20261122101502_0002_D.MP4"],  # the split recording: one session
        ["DJI_20261122120000_0003_D.MP4", "DJI_20261122120003_0004_D.JPG"],  # the photo joined its session
        ["DJI_20261122130000_0005_D_026.MP4", "DJI_20261122130002_0005_D_027.MP4"],  # loop chapters
    ]

    morning = sessions[1]
    assert morning.id.startswith("20261122-101500-")  # id from the local start time
    assert morning.started_ts == local_ts("2026-11-22 10:15:00", "America/Los_Angeles")
    assert morning.ended_ts == pytest.approx(morning.started_ts + 2 + CLIP_SECONDS, abs=0.2)
    first, second = store.list_clips(morning.id)
    # analysed file: the proxy, copied into the library under a playable name
    assert first.path == f"media/{morning.id}/DJI_20261122101500_0001_D_proxy.mp4"
    assert settings.abs(first.path).read_bytes() == (card / D / "DJI_20261122101500_0001_D.LRF").read_bytes()
    # full-quality original: still on the card (stills are cut from it while it is connected)
    assert first.original_path == str(card / D / "DJI_20261122101500_0001_D.MP4")
    assert first.fingerprint == clip_fingerprint(card / D / "DJI_20261122101500_0001_D.MP4")
    assert first.start_ts == morning.started_ts and second.start_ts == first.start_ts + 2
    assert first.duration == pytest.approx(CLIP_SECONDS, abs=0.2)
    assert (first.width, first.height) == (160, 120) and first.fps == pytest.approx(10.0)
    assert first.has_audio and first.has_video and first.stages == {}

    # no proxy: the original itself is copied and is what gets analysed
    chapter = store.list_clips(sessions[3].id)[0]
    assert chapter.path == f"media/{sessions[3].id}/DJI_20261122130000_0005_D_026.MP4" and chapter.original_path is None
    assert (chapter.width, chapter.height) == (320, 240)

    # the photo: a clip of length zero at its file-name time, read at full resolution
    photo = store.list_clips(sessions[2].id)[1]
    assert photo.path == f"media/{sessions[2].id}/DJI_20261122120003_0004_D.JPG" and photo.original_path is None
    assert photo.duration == 0.0 and photo.fps is None and photo.has_video and not photo.has_audio
    assert (photo.width, photo.height) == (640, 480)
    assert photo.start_ts == local_ts("2026-11-22 12:00:03", "America/Los_Angeles")
    assert sessions[2].ended_ts == pytest.approx(photo.start_ts, abs=0.2)

    assert not [name for name in library_files(settings) if name.endswith(".part")]
    assert len(library_files(settings)) == 7


def test_silent_proxy_gets_the_originals_audio(settings, store, card):
    clips = [c for c in scan_card(card) if c.index == 3]
    silent, main = clips[0].proxy, clips[0].original
    assert not ff.probe(silent).has_audio and ff.probe(main).has_audio
    (session,) = importer.import_clips(settings, store, clips, source="card")
    (clip,) = store.list_clips(session.id)
    merged = settings.abs(clip.path)
    assert merged.name == "DJI_20261122120000_0003_D_proxy.mp4" and clip.has_audio
    info = ff.probe(merged)
    # one self-contained file: the proxy's picture and the original's sound, both copied bit for bit
    assert info.has_video and info.has_audio
    assert (info.width, info.height) == (160, 120) and info.video_codec == ff.probe(silent).video_codec
    assert info.audio_codec == "aac" and info.duration == pytest.approx(CLIP_SECONDS, abs=0.2)
    assert _packets(merged, "v") == _packets(silent, "v") and _packets(merged, "a") == _packets(main, "a")
    assert clip.original_path == str(main)  # stills still come from the full-quality file
    assert not list(merged.parent.glob("*.part"))


def _packets(path: Path, kind: str) -> list[str]:
    """Size of every packet of the first video/audio stream: equal lists mean a bit-exact stream copy."""
    probe = ff.ffprobe_bin()
    if probe is None:
        pytest.skip("ffprobe not installed")
    out = subprocess.run(
        [probe, "-v", "error", "-select_streams", f"{kind}:0",
         "-show_entries", "packet=size", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, timeout=60, check=True,
    )  # fmt: skip
    return out.stdout.split()


def test_merge_reads_only_the_audio_of_the_big_file(tmp_path, media):
    """A 16 GB original must not be read in full just to fetch its sound."""
    if not sys.platform.startswith("linux"):
        pytest.skip("reads are counted through /proc")
    main = tmp_path / "DJI_20261122101500_0001_D.MP4"
    # A stand-in for a high-bitrate original: uncompressed frames (0.6 MB each) with AAC in between.
    ff.run(
        ["-f", "lavfi", "-i", "testsrc2=size=640x480:rate=10",
         "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000",
         "-t", "4", "-c:v", "rawvideo", "-pix_fmt", "uyvy422", "-c:a", "aac", "-b:a", "128k",
         "-timecode", "10:15:00:00", "-f", "mov", str(main)],
        timeout=120,
    )  # fmt: skip
    size = main.stat().st_size
    assert size > 20 * 1024 * 1024
    merged = tmp_path / "merged.mp4"
    proc = subprocess.Popen(
        ff.base_cmd() + importer.merge_args(media["silent_proxy.mp4"], main, merged),
        stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
    )  # fmt: skip
    try:
        os.waitid(os.P_PID, proc.pid, os.WEXITED | os.WNOWAIT)  # finished, but not collected yet
        counters = dict(line.split(": ") for line in Path(f"/proc/{proc.pid}/io").read_text().splitlines())
    finally:
        _, errors = proc.communicate(timeout=60)
    assert proc.returncode == 0, errors.decode(errors="replace")
    info = ff.probe(merged)
    assert info.has_video and info.has_audio and (info.width, info.height) == (160, 120)  # data tracks left out
    assert int(counters["rchar"]) < size / 4, f"read {counters['rchar']} bytes of a {size}-byte original"


def test_reimport_is_idempotent(settings, store, card):
    clips = scan_card(card)
    first = importer.import_clips(settings, store, clips, source="card")
    stats, files = store.stats(), library_files(settings)
    assert stats["sessions"] == len(first) == 4 and stats["clips"] == 7

    report = importer.import_with_report(settings, store, scan_card(card), source="card")
    assert report.sessions == [] and report.imported == [] and report.failed == []
    assert len(report.skipped) == 7  # every recording recognised, none copied or recorded again
    assert importer.import_clips(settings, store, scan_card(card), source="card") == []
    assert store.stats() == stats and library_files(settings) == files

    # a new recording next to known ones: only that one comes in, as a session of its own
    shutil.copyfile(card / D / "DJI_20261122101500_0001_D.MP4", card / D / "DJI_20261122150000_0007_D.MP4")
    (session,) = importer.import_clips(settings, store, scan_card(card), source="card")
    assert [Path(c.path).name for c in store.list_clips(session.id)] == ["DJI_20261122150000_0007_D.MP4"]
    assert store.stats()["clips"] == 8


def test_copy_mode_original(settings, store, card):
    settings.imports.copy_media = "original"
    before = snapshot(card)
    clips = [c for c in scan_card(card) if c.index == 1]
    (session,) = importer.import_clips(settings, store, clips, source="card")
    (clip,) = store.list_clips(session.id)
    # both files are in the library: the proxy to analyse, the original for stills and sound
    assert clip.path == f"media/{session.id}/DJI_20261122101500_0001_D_proxy.mp4"
    assert clip.original_path == f"media/{session.id}/DJI_20261122101500_0001_D.MP4"
    assert settings.abs(clip.original_path).stat().st_size == clips[0].size
    assert settings.abs(clip.original_path).stat().st_mtime == pytest.approx(clips[0].original.stat().st_mtime, abs=1)
    assert (clip.width, clip.height) == (160, 120)
    assert snapshot(card) == before


def test_copy_mode_none_leaves_everything_in_place(settings, store, card):
    settings.imports.copy_media = "none"
    before = snapshot(card)
    clips = [c for c in scan_card(card) if c.index in (3, 4)]
    (session,) = importer.import_clips(settings, store, clips, source="card")
    video, photo = store.list_clips(session.id)
    assert video.path == str(card / D / "DJI_20261122120000_0003_D.LRF")  # analysed where it is
    assert video.original_path == str(card / D / "DJI_20261122120000_0003_D.MP4")
    assert video.has_audio  # the silent proxy is left alone; the pipeline takes the sound from the original
    assert not ff.probe(settings.abs(video.path)).has_audio
    assert photo.path == str(card / D / "DJI_20261122120003_0004_D.JPG") and photo.original_path is None
    assert library_files(settings) == [] and not (settings.media_dir / session.id).exists()
    assert snapshot(card) == before
    assert importer.import_clips(settings, store, scan_card(card)[3:5], source="card") == []  # still idempotent


def test_prefer_proxy_off_ignores_proxies(settings, store, card):
    settings.imports.prefer_proxy = False
    clips = [c for c in scan_card(card) if c.index == 1]
    (session,) = importer.import_clips(settings, store, clips, source="card")
    (clip,) = store.list_clips(session.id)
    assert clip.path == f"media/{session.id}/DJI_20261122101500_0001_D.MP4" and clip.original_path is None
    assert (clip.width, clip.height) == (320, 240)
    assert library_files(settings) == [f"{session.id}/DJI_20261122101500_0001_D.MP4"]


def test_unknown_copy_mode_is_refused(settings, store, card):
    settings.imports.copy_media = "everything"
    with pytest.raises(CaptureError, match="proxy, original, none"):
        importer.import_clips(settings, store, scan_card(card), source="card")
    assert store.stats()["sessions"] == 0


def test_not_enough_disk_space_stops_before_anything_is_copied(settings, store, card, monkeypatch):
    usage = shutil.disk_usage(settings.home)
    monkeypatch.setattr(importer.shutil, "disk_usage", lambda path: usage._replace(free=100 * 1024 * 1024))
    with pytest.raises(CaptureError) as failure:
        importer.import_clips(settings, store, scan_card(card), source="card")
    message = str(failure.value)
    assert "Not enough free disk space" in message and "0.1 GB are free" in message
    assert "import.copy_media=none" in message  # the way out
    assert store.stats()["sessions"] == 0 and library_files(settings) == []
    assert not [p for p in settings.media_dir.iterdir()]
    # analysing in place needs no space at all
    settings.imports.copy_media = "none"
    assert len(importer.import_clips(settings, store, scan_card(card), source="card")) == 4


def test_card_pulled_out_mid_import_then_resumed(settings, store, card, media, monkeypatch, caplog):
    clips = [c for c in scan_card(card) if c.original.name.startswith("DJI_20261122")]
    real_copy = importer._copy_file
    copies: list[str] = []

    def copy_then_vanish(src: Path, dst: Path) -> None:
        if len(copies) == 3:  # the first session (2 files) is done, the second is half-way
            shutil.rmtree(card)  # the USB connection drops
        real_copy(src, dst)
        copies.append(src.name)

    monkeypatch.setattr(importer, "_copy_file", copy_then_vanish)
    monkeypatch.setattr(importer, "_merge_proxy_audio", lambda proxy, main, dst: False)  # keep the copies countable
    with caplog.at_level(logging.WARNING, logger="videonotes.capture.importer"):
        sessions = importer.import_clips(settings, store, clips, source="card")
    # What was complete is kept and returned; the rest is reported, not half-recorded.
    assert len(sessions) == 1 and len(store.list_clips(sessions[0].id)) == 2
    assert "disappeared during the import" in caplog.text and "run the import again" in caplog.text
    assert store.stats()["sessions"] == 1 and store.stats()["clips"] == 2
    assert not [name for name in library_files(settings) if name.endswith(".part")]
    leftover = sorted(p.name for p in settings.media_dir.iterdir() if store.get_session(p.name) is None)
    assert len(leftover) == 1 and leftover[0].startswith("20261122-120000-")  # the interrupted session's folder
    assert library_files(settings)[2:] == [f"{leftover[0]}/DJI_20261122120000_0003_D_proxy.mp4"]

    # The card is plugged in again: the same command finishes the job, in the same folder,
    # without copying the file that already made it.
    build_card(card, media)
    copies.clear()
    monkeypatch.setattr(importer, "_copy_file", lambda src, dst: (real_copy(src, dst), copies.append(src.name))[0])
    rescanned = [c for c in scan_card(card) if c.original.name.startswith("DJI_20261122")]
    resumed = importer.import_clips(settings, store, rescanned, source="card")
    assert [s.id for s in resumed] == [leftover[0], resumed[1].id] and len(resumed) == 2
    assert store.stats()["sessions"] == 3 and store.stats()["clips"] == 6
    kept = settings.media_dir / leftover[0] / "DJI_20261122120000_0003_D_proxy.mp4"
    assert kept.stat().st_size == (card / D / "DJI_20261122120000_0003_D.LRF").stat().st_size
    assert importer.import_clips(settings, store, rescanned, source="card") == []


def test_nothing_imported_because_the_card_is_gone(settings, store, card):
    clips = scan_card(card)
    shutil.rmtree(card)
    with pytest.raises(CaptureError) as failure:
        importer.import_clips(settings, store, clips, source="card")
    assert "could not be imported" in str(failure.value) and "still connected" in str(failure.value)
    assert store.stats()["sessions"] == 0 and library_files(settings) == []


def test_one_unreadable_recording_does_not_block_the_others(settings, store, card, caplog):
    clips = [c for c in scan_card(card) if c.original.name.startswith("DJI_202611221015")]
    first, second = clips
    first.proxy.write_bytes(b"\x00" * 4096)  # a damaged proxy: the original is used instead
    second.proxy.write_bytes(b"\x00" * 4096)  # proxy and original both damaged: this one is lost...
    second.original.write_bytes(b"\x00" * 8192)
    with caplog.at_level(logging.WARNING, logger="videonotes.capture.importer"):
        report = importer.import_with_report(settings, store, clips, source="card")
    assert [c.original.name for c in report.imported] == ["DJI_20261122101500_0001_D.MP4"]  # ...but not the first
    assert [c.original.name for c, _ in report.failed] == ["DJI_20261122101502_0002_D.MP4"]
    assert "damaged or not a media file" in report.failed[0][1]
    assert not report.source_lost and len(report.sessions) == 1
    assert "ignoring the unreadable proxy DJI_20261122101500_0001_D.LRF" in caplog.text
    assert "1 recording(s) could not be imported" in caplog.text and "DJI_20261122101502_0002_D.MP4" in caplog.text
    (clip,) = store.list_clips(report.sessions[0].id)
    assert Path(clip.path).name == "DJI_20261122101500_0001_D.MP4" and clip.original_path is None
    assert (clip.width, clip.height) == (320, 240)
    # import_clips itself only raises when nothing at all could be imported
    with pytest.raises(CaptureError, match="could not be imported"):
        importer.import_clips(settings, store, [second], source="card")


def test_copy_is_atomic_and_verified(tmp_path, media, monkeypatch):
    src, dst = media["main.mp4"], tmp_path / "lib" / "clip.mp4"
    dst.parent.mkdir()

    def disk_error(fd: int) -> None:
        raise OSError(errno.EIO, "Input/output error")

    monkeypatch.setattr(importer.os, "fsync", disk_error)
    with pytest.raises(OSError):
        importer._copy_file(src, dst)
    assert list(dst.parent.iterdir()) == []  # neither a half file nor a temporary one

    monkeypatch.setattr(importer.os, "fsync", lambda fd: os.ftruncate(fd, 10))  # the copy came out short
    with pytest.raises(OSError, match="only 10 of"):
        importer._copy_file(src, dst)
    assert list(dst.parent.iterdir()) == []

    monkeypatch.undo()
    importer._copy_file(src, dst)
    assert dst.read_bytes() == src.read_bytes() and [p.name for p in dst.parent.iterdir()] == ["clip.mp4"]
    stamp = dst.stat().st_mtime_ns
    importer._copy_file(src, dst)  # already there in full: not copied again
    assert dst.stat().st_mtime_ns == stamp
    dst.write_bytes(b"stale")  # a different size is not "already there"
    importer._copy_file(src, dst)
    assert dst.read_bytes() == src.read_bytes()


def test_same_file_name_from_two_folders_does_not_collide(settings, store, tmp_path, media):
    for sub, stock in (("a", "silent_proxy.mp4"), ("b", "proxy.mp4")):  # neither carries a creation_time
        (tmp_path / "trip" / sub).mkdir(parents=True)
        shutil.copyfile(media[stock], tmp_path / "trip" / sub / "clip.mp4")
    stamp = datetime(2026, 11, 20, 9, 0, tzinfo=UTC).timestamp()
    os.utime(tmp_path / "trip" / "a" / "clip.mp4", (stamp, stamp))
    os.utime(tmp_path / "trip" / "b" / "clip.mp4", (stamp + 5, stamp + 5))
    clips = scan_card(tmp_path / "trip")
    assert len(clips) == 2
    (session,) = importer.import_clips(settings, store, clips, source="trip")
    assert sorted(library_files(settings)) == [f"{session.id}/clip-2.mp4", f"{session.id}/clip.mp4"]
    sizes = sorted(settings.abs(c.path).stat().st_size for c in store.list_clips(session.id))
    assert sizes == sorted([media["silent_proxy.mp4"].stat().st_size, media["proxy.mp4"].stat().st_size])


# ---------------------------------------------------------------------------------
# import_file
# ---------------------------------------------------------------------------------


def test_import_file_uses_creation_time_then_mtime(settings, store, tmp_path, media, tz):
    tz("Europe/Berlin")
    talk = Path(shutil.copy(media["main.mp4"], tmp_path / "talk.mp4"))
    session = importer.import_file(settings, store, talk)
    assert session.kind == "file" and session.source == str(talk) and session.id.startswith("20261122-191500-")
    assert session.started_ts == datetime(2026, 11, 22, 18, 15, tzinfo=UTC).timestamp()  # the container's creation_time
    assert session.ended_ts == pytest.approx(session.started_ts + CLIP_SECONDS, abs=0.2)
    (clip,) = store.list_clips(session.id)
    assert clip.path == f"media/{session.id}/talk.mp4" and clip.original_path is None
    assert clip.fingerprint == clip_fingerprint(talk) and clip.has_audio and clip.has_video
    assert importer.import_file(settings, store, talk).id == session.id  # again: the same session, no duplicate
    assert store.stats()["sessions"] == 1

    plain = Path(shutil.copy(media["proxy.mp4"], tmp_path / "no-metadata.mp4"))  # no creation_time inside
    mtime = datetime(2026, 11, 21, 8, 0, 10, tzinfo=UTC).timestamp()
    os.utime(plain, (mtime, mtime))
    assert importer.import_file(settings, store, plain).started_ts == pytest.approx(mtime - CLIP_SECONDS, abs=0.2)


def test_import_file_with_explicit_start_and_in_place(settings, store, tmp_path, media):
    settings.imports.copy_media = "none"
    talk = Path(shutil.copy(media["main.mp4"], tmp_path / "talk.mp4"))
    session = importer.import_file(settings, store, talk, start_ts=1_700_000_000.0)
    assert session.started_ts == 1_700_000_000.0
    (clip,) = store.list_clips(session.id)
    assert clip.path == str(talk) and clip.start_ts == 1_700_000_000.0
    assert library_files(settings) == []


def test_import_file_camera_original_uses_name_time_and_proxy(settings, store, card, tz):
    tz("Asia/Tokyo")
    main = card / D / "DJI_20261122101500_0001_D.MP4"
    session = importer.import_file(settings, store, main)
    assert session.started_ts == local_ts("2026-11-22 10:15:00", "Asia/Tokyo")  # the name, not creation_time
    (clip,) = store.list_clips(session.id)
    assert clip.path == f"media/{session.id}/DJI_20261122101500_0001_D_proxy.mp4" and clip.original_path == str(main)
    # the proxy file on its own is just a small video
    lone = importer.import_file(settings, store, card / D / "DJI_20261122101502_0002_D.LRF")
    (clip,) = store.list_clips(lone.id)
    assert clip.original_path is None and clip.path.endswith("DJI_20261122101502_0002_D.LRF")


def test_import_file_accepts_sound_and_pictures(settings, store, tmp_path, media):
    memo = Path(shutil.copy(media["backup.wav"], tmp_path / "memo.wav"))
    (clip,) = store.list_clips(importer.import_file(settings, store, memo).id)
    assert clip.has_audio and not clip.has_video and clip.duration == pytest.approx(1.0, abs=0.1)
    board = Path(shutil.copy(media["photo.jpg"], tmp_path / "whiteboard.jpg"))
    (clip,) = store.list_clips(importer.import_file(settings, store, board).id)
    assert clip.has_video and not clip.has_audio and clip.duration == 0.0 and clip.fps is None


def test_import_file_refuses_what_it_cannot_read(settings, store, tmp_path):
    with pytest.raises(CaptureError, match="No such file"):
        importer.import_file(settings, store, tmp_path / "missing.mp4")
    with pytest.raises(CaptureError, match="No such file"):
        importer.import_file(settings, store, tmp_path)  # a folder
    (tmp_path / "empty.mp4").write_bytes(b"")
    with pytest.raises(CaptureError, match="empty"):
        importer.import_file(settings, store, tmp_path / "empty.mp4")
    (tmp_path / "letter.txt").write_text("Dear diary, " * 200)
    with pytest.raises(CaptureError, match="not a video, audio or picture"):
        importer.import_file(settings, store, tmp_path / "letter.txt")
    assert store.stats()["sessions"] == 0 and library_files(settings) == []


def test_two_stores_do_not_import_the_same_recording_twice(settings, card):
    """Fingerprints are unique in the library, so a second process cannot duplicate a clip."""
    clips = [c for c in scan_card(card) if c.index == 1]
    with Store(settings.db_path) as one, Store(settings.db_path) as two:
        assert len(importer.import_clips(settings, one, clips, source="card")) == 1
        assert importer.import_clips(settings, two, clips, source="card") == []
        assert two.stats()["clips"] == 1
