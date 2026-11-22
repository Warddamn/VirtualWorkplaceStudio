from __future__ import annotations

import json
import logging
import os
import re
import sqlite3
import time
from pathlib import Path
from urllib.parse import unquote

import pytest

from videonotes import timeutil as tu
from videonotes.config import Settings
from videonotes.models import ActionItem, Clip, DayDigest, Keyframe, Moment, Session, SessionNote, Utterance
from videonotes.notes import render as R
from videonotes.notes.moments import segment_moments
from videonotes.notes.render import NoteRenderError, render_day_note, render_session_note
from videonotes.store import Store

T0 = 1_795_357_920.0  # 2026-11-22 14:32:00 UTC; every expectation below is computed in local time
DAY = tu.local_date(T0)
SID = "20261122-143200-ab12"

JPEG = b"\xff\xd8\xff\xe0fake-jpeg-"


# ---------------------------------------------------------------------------
# Building a library through the real Store
# ---------------------------------------------------------------------------


class Lib:
    """One session in a real library: clip, keyframe files on disk, utterances, moments."""

    def __init__(self, settings: Settings, store: Store, sid: str = SID, start: float = T0, **session: object):
        self.settings, self.store, self.sid, self.start = settings, store, sid, start
        fields = {"kind": "import", "source": "Osmo Action 4 (SD card)", "ended_ts": start + 600, **session}
        store.create_session(Session(id=sid, started_ts=start, **fields))  # type: ignore[arg-type]
        self.clip = store.add_clip(
            Clip(session_id=sid, path=f"media/{sid}.mp4", fingerprint=f"fp-{sid}", start_ts=start, duration=600)
        )
        self.frames_dir = settings.frames_dir / sid
        self.frames_dir.mkdir(parents=True, exist_ok=True)
        self._frames: list[Keyframe] = []
        self._said: list[Utterance] = []

    def frame(self, t: float, *, ocr: str | None = None, caption: str | None = None, reason: str = "interval",
              novelty: float = 0.1, sharpness: float = 1.0, on_disk: bool = True, suffix: str = ".jpg") -> Lib:  # fmt: skip
        path = self.frames_dir / f"frame_{len(self._frames):04d}{suffix}"
        if on_disk:
            path.write_bytes(JPEG + str(t).encode())
        self._frames.append(
            Keyframe(clip_id=self.clip.id, session_id=self.sid, t=t, ts=self.start + t, path=self.settings.rel(path),
                     reason=reason, novelty=novelty, sharpness=sharpness, ocr_text=ocr, caption=caption)  # fmt: skip
        )
        return self

    def say(self, t0: float, t1: float, text: str, speaker: str | None = None) -> Lib:
        self._said.append(
            Utterance(clip_id=self.clip.id, session_id=self.sid, t0=t0, t1=t1, ts0=self.start + t0,
                      ts1=self.start + t1, text=text, speaker=speaker)  # fmt: skip
        )
        return self

    def commit(self, *, segment: bool = True) -> Lib:
        self.keyframes = self.store.replace_keyframes(self.clip.id, self._frames)
        self.utterances = self.store.replace_utterances(self.clip.id, self._said)
        self.moments: list[Moment] = []
        if segment:
            session = self.store.get_session(self.sid)
            self.moments = self.store.replace_moments(
                self.sid, segment_moments(session, self.utterances, self.keyframes, self.settings.notes)
            )
        return self

    def summarise(self, note: SessionNote, moment_titles: list[str] | None = None) -> Lib:
        self.store.update_session(self.sid, note=note, title=note.title)
        for m, title in zip(self.moments, moment_titles or [], strict=False):
            self.store.update_moment(m.id, title=title, summary=f"Summary of {title}.", tags=[])
        return self

    def render(self) -> Path:
        return render_session_note(self.settings, self.store, self.sid)


@pytest.fixture()
def cfg(settings: Settings) -> Settings:
    """Settings with explicit segmentation limits, so the tests do not depend on the defaults."""
    settings.notes.moment_gap_seconds = 45.0
    settings.notes.moment_min_seconds = 20.0
    settings.notes.moment_max_seconds = 600.0
    return settings


NOTE = SessionNote(
    title="Planning meeting",
    summary="We went through the launch plan for Q3.\n\nThe Falcon beta ships on June 14.",
    key_points=["Falcon beta ships on June 14", "Sensors are the open risk"],
    action_items=[
        ActionItem(text="Email the quarterly budget to Sarah", owner="me", due="Friday", ts=T0 + 8),
        ActionItem(text="Call the vendor about sensors"),
    ],
    decisions=["Ship the beta on June 14"],
    open_questions=["Who owns the sensor contract?"],
    people=["Sarah", "Bob"],
    places=["Room 4B"],
    captured_text=["Launch plan Q3", "Room 4B\nDesign Review 3 PM", "launch plan q3"],
    tags=["planning", "Q3 launch"],
    llm_backend="ollama:qwen3:4b",
)


def demo_lib(settings: Settings, store: Store, **kw: object) -> Lib:
    """Two moments: a whiteboard conversation, a long pause, a remark at a door sign."""
    lib = Lib(settings, store, **kw)  # type: ignore[arg-type]
    lib.frame(1, reason="first", novelty=1.0)
    lib.frame(30, ocr="Launch plan Q3\nShip Falcon beta by June 14", caption="A whiteboard with a launch plan.")
    lib.frame(50, ocr="Launch plan Q3\nShip Falcon beta by June 14.")
    lib.frame(300, ocr="Room 4B\nDesign Review 3 PM", caption="A door sign.", reason="scene", novelty=0.9)
    lib.say(2, 6, "Okay, quick note to self.")
    lib.say(6.5, 11, "Remember to email the quarterly budget to Sarah before Friday.")
    lib.say(28, 33, "This is the whiteboard from the planning meeting.", speaker="Me")
    lib.say(40, 46, "We decided to ship the Falcon beta on June fourteenth.", speaker="Bob")
    lib.say(301, 306, "The design review is in room 4B at 3 PM.")
    return lib.commit()


# ---------------------------------------------------------------------------
# Reading notes back
# ---------------------------------------------------------------------------


def front_matter(text: str) -> dict[str, object]:
    """The front matter, read without a YAML library (every value is written JSON-compatibly or bare)."""
    assert text.startswith("---\n")
    block = text[4 : text.index("\n---\n", 4)]
    out: dict[str, object] = {}
    for line in block.split("\n"):
        key, _, value = line.partition(": ")
        try:
            out[key] = json.loads(value)
        except ValueError:
            out[key] = value
    return out


def body_of(text: str) -> str:
    return text[text.index("\n---\n", 4) + 5 :]


def scan(text: str) -> tuple[list[str], list[str]]:
    """Split a note's body the way a Markdown parser does: (Markdown lines, HTML blocks).

    Fenced code is dropped; an HTML block runs from a line starting with
    ``<details>`` or ``<!--`` to the next blank line.
    """
    lines: list[str] = []
    html: list[str] = []
    fence: str | None = None
    block: list[str] | None = None
    for line in body_of(text).split("\n"):
        if fence is not None:
            if re.fullmatch(rf"{fence}`*", line):
                fence = None
            continue
        if block is not None:
            if line.strip():
                block.append(line)
            else:
                html.append("\n".join(block))
                block = None
            continue
        opening = re.match(r"(`{3,})", line)
        if opening:
            fence = opening.group(1)
        elif line.startswith(("<details>", "<!--")):
            block = [line]
        else:
            lines.append(line)
    assert fence is None, "an unclosed code fence swallowed the rest of the note"
    assert block is None, "an HTML block runs to the end of the note"
    return lines, html


def markdown_lines(text: str) -> list[str]:
    """Lines a Markdown parser treats as Markdown: outside fenced code and outside HTML blocks."""
    return scan(text)[0]


def headings(text: str) -> list[str]:
    return [line for line in markdown_lines(text) if re.match(r"#{1,6}(\s|$)", line)]


LINK = re.compile(r"(!?)\[((?:[^\]\\]|\\.)*)\]\(([^)\s]+)\)")


def links(text: str) -> list[tuple[bool, str, str]]:
    """(is_image, text, destination) of every Markdown link / image outside code and HTML."""
    found = []
    for line in markdown_lines(text):
        for bang, label, dest in LINK.findall(line):
            found.append((bang == "!", label, dest))
    return found


def resolve(note: Path, destination: str) -> Path:
    return (note.parent / unquote(destination)).resolve()


def vault_files(settings: Settings) -> list[str]:
    root = settings.vault_dir
    return sorted(str(p.relative_to(root)) for p in root.rglob("*") if p.is_file())


def clock(ts: float, fmt: str = "%H:%M") -> str:
    return tu.fmt_clock(ts, fmt)


# ---------------------------------------------------------------------------
# Session notes: structure
# ---------------------------------------------------------------------------


def test_session_note_has_every_section_in_order(cfg: Settings, store: Store):
    lib = demo_lib(cfg, store).summarise(NOTE, ["Whiteboard walkthrough", "Door sign"])
    path = lib.render()

    assert path == cfg.vault_dir / "sessions" / f"{tu.local_dt(T0):%Y-%m-%d %H%M} Planning meeting.md"
    assert store.get_session(SID).note_path == cfg.rel(path) == f"notes/sessions/{path.name}"
    text = path.read_text(encoding="utf-8")

    fm = front_matter(text)
    assert list(fm) == ["title", "date", "start", "end", "duration", "session_id", "kind", "source", "tags", "summarizer"]
    assert fm["title"] == "Planning meeting" and fm["session_id"] == SID and fm["kind"] == "import"
    assert fm["date"] == DAY and fm["start"] == f"{tu.local_dt(T0):%Y-%m-%dT%H:%M:%S}"
    assert fm["end"] == f"{tu.local_dt(T0 + 600):%Y-%m-%dT%H:%M:%S}" and fm["duration"] == "10 min"
    assert fm["source"] == "Osmo Action 4 (SD card)" and fm["summarizer"] == "ollama:qwen3:4b"
    assert fm["tags"] == ["planning", "Q3-launch"]  # no spaces: Obsidian would not accept them

    range1 = f"{clock(T0 + 1)}–{clock(T0 + 50)}" if clock(T0 + 1) != clock(T0 + 50) else clock(T0 + 1)
    assert headings(text) == [
        "# Planning meeting",
        "## Summary",
        "## Key points",
        "## Action items",
        "## Decisions",
        "## Open questions",
        "## People and places",
        "## Captured text",
        "## Timeline",
        f"### {range1}  Whiteboard walkthrough",
        f"### {clock(T0 + 300)}–{clock(T0 + 306)}  Door sign" if clock(T0 + 300) != clock(T0 + 306)
        else f"### {clock(T0 + 300)}  Door sign",
    ]  # fmt: skip
    lines = body_of(text).split("\n")
    # the context line: date, time range, duration, source
    context = lines[lines.index("# Planning meeting") + 2]
    assert context == (
        f"*{tu.local_dt(T0):%A %Y-%m-%d} · {clock(T0)}–{clock(T0 + 600)} · 10 min · Osmo Action 4 (SD card)*"
    )
    assert "We went through the launch plan for Q3.\n\nThe Falcon beta ships on June 14." in text
    assert "- Falcon beta ships on June 14\n- Sensors are the open risk" in text
    assert f"- [ ] Email the quarterly budget to Sarah (owner: me; due: Friday; {clock(T0 + 8)})" in lines
    assert "- [ ] Call the vendor about sensors" in lines  # nothing appended when owner / due / time are unknown
    assert "**People:** Sarah, Bob  \n**Places:** Room 4B" in text
    assert "Not summarised" not in text


def test_captured_text_is_verbatim_and_deduplicated(cfg: Settings, store: Store):
    text = demo_lib(cfg, store).summarise(NOTE).render().read_text(encoding="utf-8")
    section = text[text.index("## Captured text") : text.index("## Timeline")]
    assert section.count("Launch plan Q3") == 1 and "launch plan q3" not in section  # same text, different case
    assert "- Launch plan Q3" in section
    assert "```text\nRoom 4B\nDesign Review 3 PM\n```" in section


def test_empty_sections_are_omitted(cfg: Settings, store: Store):
    lib = demo_lib(cfg, store).summarise(SessionNote(title="Short one", summary="Just a summary.", llm_backend="extractive"))
    text = lib.render().read_text(encoding="utf-8")
    level2 = [h for h in headings(text) if h.startswith("## ")]
    assert level2 == ["## Summary", "## Timeline"]
    assert front_matter(text)["tags"] == [] and front_matter(text)["summarizer"] == "extractive"


def test_timeline_entry_has_summary_images_screen_text_and_collapsed_transcript(cfg: Settings, store: Store):
    lib = demo_lib(cfg, store).summarise(NOTE, ["Whiteboard walkthrough", "Door sign"])
    text = lib.render().read_text(encoding="utf-8")
    first = text[text.index("### ") : text.index("### ", text.index("### ") + 4)]
    order = [
        first.index("Summary of Whiteboard walkthrough."),
        first.index("!["),
        first.index("**On screen**"),
        first.index("<details>"),
    ]
    assert order == sorted(order)
    # on-screen text: the two readings of the same whiteboard collapse into one
    assert first.count("Ship Falcon beta by June 14") == 1
    assert "```text\nLaunch plan Q3\nShip Falcon beta by June 14\n```" in first
    # transcript: one HTML block, collapsed (no "open"), clock times with seconds, speakers when known
    block = first[first.index("<details>") : first.index("</details>") + len("</details>")]
    assert "\n\n" not in block and "<details open" not in block
    assert block.startswith("<details>\n<summary>Transcript · 3 lines</summary>\n<p>\n")
    assert f"<b>{clock(T0 + 2, '%H:%M:%S')}</b> Okay, quick note to self. Remember to email" in block
    assert f"<b>{clock(T0 + 28, '%H:%M:%S')} Me:</b> This is the whiteboard from the planning meeting.<br>" in block
    assert f"<b>{clock(T0 + 40, '%H:%M:%S')} Bob:</b> We decided to ship" in block
    assert text.count("<details>") == text.count("</details>") == 2


def test_transcript_can_be_switched_off(cfg: Settings, store: Store):
    cfg.notes.include_transcript = False
    text = demo_lib(cfg, store).summarise(NOTE).render().read_text(encoding="utf-8")
    assert "<details>" not in text and "quick note to self" not in text


def test_time_format_setting_is_used(cfg: Settings, store: Store):
    cfg.notes.time_format = "%I.%M %p"
    text = demo_lib(cfg, store).summarise(NOTE).render().read_text(encoding="utf-8")
    assert f"{clock(T0, '%I.%M %p')}–{clock(T0 + 600, '%I.%M %p')}" in text
    assert f"<b>{clock(T0 + 2, '%I.%M:%S %p')}</b>" in text
    # a format strftime cannot use falls back to HH:MM instead of failing
    assert R._clock_formatter("%")(T0) in (clock(T0), "%")
    assert R._clock_formatter("")(T0) == clock(T0)


def test_background_moments_are_kept_to_one_line(cfg: Settings, store: Store):
    lib = demo_lib(cfg, store).summarise(NOTE, ["Whiteboard walkthrough", "Door sign"])
    store.update_moment(lib.moments[1].id, title="Door sign", summary="Walked past a door. Nothing else happened.",
                        tags=["hallway"], kind="transit", salience="background")  # fmt: skip
    text = lib.render().read_text(encoding="utf-8")
    entry = text[text.index("  Door sign") :]
    assert "*transit · hallway*" in entry and "*Walked past a door.*" in entry
    assert "Nothing else happened" not in entry
    assert "![" not in entry and "**On screen**" not in entry  # no images, no screen text ...
    assert "<details>" in entry  # ... but what was said is still there, collapsed
    assert text.count("### ") == 2


# ---------------------------------------------------------------------------
# Images
# ---------------------------------------------------------------------------


def test_links_resolve_and_keyframes_are_copied_not_moved(cfg: Settings, store: Store):
    lib = demo_lib(cfg, store).summarise(NOTE, ["Whiteboard walkthrough", "Door sign"])
    path = lib.render()
    text = path.read_text(encoding="utf-8")
    images = [(label, dest) for is_image, label, dest in links(text) if is_image]
    assert len(images) == 3  # two of the three frames of the first moment, the only frame of the second
    second_reading = next(k for k in lib.keyframes if k.t == 50)  # the same whiteboard text again: not worth a slot
    assert all(f"kf_{second_reading.id:06d}" not in dest for _, dest in images)
    assets = cfg.vault_dir / "assets" / SID
    for _, dest in images:
        assert dest.startswith(f"../assets/{SID}/kf_") and "\\" not in dest
        copy = resolve(path, dest)
        assert copy.is_file() and copy.parent == assets.resolve()
    by_id = {f"kf_{k.id:06d}.jpg": k for k in lib.keyframes}
    assert set(by_id) >= {p.name for p in assets.iterdir()}
    for copy in assets.iterdir():
        source = cfg.abs(by_id[copy.name].path)
        assert source.is_file() and source.read_bytes() == copy.read_bytes()  # copied, the original stays
    # captions are the alt text and a visible caption line with the clock time
    assert "![A whiteboard with a launch plan.](" in text
    assert f"*{clock(T0 + 30, '%H:%M:%S')} — A whiteboard with a launch plan.*" in text
    assert f"![Frame at {clock(T0 + 1, '%H:%M:%S')}](" in text  # no caption: the alt text says when it was taken
    assert f"\n*{clock(T0 + 1, '%H:%M:%S')}*\n" in text


def test_image_choice_prefers_informative_frames_spread_in_time(cfg: Settings):
    def kf(i: int, ts: float, **kw: object) -> Keyframe:
        return Keyframe(clip_id=1, session_id=SID, t=ts, ts=T0 + ts, path=f"f{i}.jpg", id=i, **kw)  # type: ignore[arg-type]

    frames = [
        kf(1, 0), kf(2, 10, ocr_text="slide one"), kf(3, 20, caption="a slide", ocr_text="slide one"),
        kf(4, 60), kf(5, 70, novelty=0.9), kf(6, 100, sharpness=9.0),
    ]  # fmt: skip
    # the captioned slide first; the other reading of the same slide adds nothing, so the second pick is the
    # frame farthest away in time
    assert [k.id for k in R._pick_images(frames, 2)] == [3, 6]
    assert [k.id for k in R._pick_images(frames, 3)] == [3, 4, 6]  # then the middle of the widest gap
    # about equally far from what is already chosen: the more novel frame wins
    close_call = [kf(1, 0, caption="start"), kf(2, 49), kf(3, 51, novelty=0.9), kf(4, 100, caption="end")]
    assert [k.id for k in R._pick_images(close_call, 3)] == [1, 3, 4]
    assert [k.id for k in R._pick_images(frames, 1)] == [3]
    assert [k.id for k in R._pick_images(frames, 10)] == [1, 2, 3, 4, 5, 6]
    assert R._pick_images(frames, 0) == [] and R._pick_images([], 3) == []
    # frames that tell something new always come before spreading out
    bunched = [kf(1, 0), kf(2, 1, ocr_text="x"), kf(3, 2, caption="y"), kf(4, 100)]
    assert [k.id for k in R._pick_images(bunched, 2)] == [2, 3]
    assert [k.id for k in R._pick_images(bunched, 3)] == [2, 3, 4]
    # nothing to tell them apart: first, last, middle
    plain = [kf(i, i * 10.0) for i in range(11)]
    assert [k.id for k in R._pick_images(plain, 3)] == [0, 5, 10]
    same_instant = [kf(1, 5), kf(2, 5, caption="c"), kf(3, 5)]
    assert [k.id for k in R._pick_images(same_instant, 2)] == [1, 2]


def test_unreferenced_assets_are_removed_but_foreign_files_survive(cfg: Settings, store: Store):
    lib = demo_lib(cfg, store).summarise(NOTE)
    path = lib.render()
    assets = cfg.vault_dir / "assets" / SID
    before = {p.name for p in assets.iterdir()}
    assert len(before) == 3
    (assets / "my own sketch.png").write_bytes(b"user file")
    (assets / "kf_999999.jpg").write_bytes(b"stale copy from an earlier render")
    (assets / ".vnote-0123abcd.tmp").write_bytes(b"left over from a crash")

    cfg.notes.max_images_per_moment = 1
    text = lib.render().read_text(encoding="utf-8")
    after = {p.name for p in assets.iterdir()}
    assert "my own sketch.png" in after and "kf_999999.jpg" not in after and ".vnote-0123abcd.tmp" not in after
    kept = after - {"my own sketch.png"}
    assert len(kept) == 2 and kept < before
    assert {resolve(path, dest).name for is_image, _, dest in links(text) if is_image} == kept

    # embedding switched off: no image links, the copies are gone, the user's file is not
    cfg.notes.embed_images = False
    text = lib.render().read_text(encoding="utf-8")
    assert not [1 for is_image, _, _ in links(text) if is_image]
    assert {p.name for p in assets.iterdir()} == {"my own sketch.png"}
    (assets / "my own sketch.png").unlink()
    lib.render()
    assert not assets.exists()  # nothing left: the empty folder goes too
    assert all(cfg.abs(k.path).is_file() for k in lib.keyframes)  # the library's own frames were never touched


def test_missing_source_image_is_skipped_and_logged(cfg: Settings, store: Store, caplog: pytest.LogCaptureFixture):
    lib = Lib(cfg, store)
    lib.frame(1, caption="gone", on_disk=False).frame(5, caption="here").frame(9, caption="not an image", suffix=".txt")
    lib.say(2, 8, "Hello there.").commit()
    with caplog.at_level(logging.DEBUG, logger="videonotes.render"):
        path = lib.render()
    text = path.read_text(encoding="utf-8")
    images = [(label, dest) for is_image, label, dest in links(text) if is_image]
    assert [label for label, _ in images] == ["here"]
    assert resolve(path, images[0][1]).is_file()
    assert any("2 keyframe image(s) are missing" in r.getMessage() for r in caplog.records)
    assert not [r for r in caplog.records if r.levelno >= logging.WARNING]


def test_copy_failure_drops_the_image_but_not_the_note(cfg: Settings, store: Store, monkeypatch: pytest.MonkeyPatch,
                                                       caplog: pytest.LogCaptureFixture):  # fmt: skip
    lib = demo_lib(cfg, store)

    def no_space(src: object, dst: object, **kw: object) -> None:
        raise OSError(28, "No space left on device")

    monkeypatch.setattr(R.shutil, "copyfile", no_space)
    with caplog.at_level(logging.WARNING, logger="videonotes.render"):
        path = lib.render()
    text = path.read_text(encoding="utf-8")
    assert "![" not in text and "## Timeline" in text
    assert any("copying" in r.getMessage() for r in caplog.records)
    assert not (cfg.vault_dir / "assets" / SID).exists()


# ---------------------------------------------------------------------------
# File names, renames, collisions, atomicity
# ---------------------------------------------------------------------------


def test_retitled_session_replaces_its_previous_file(cfg: Settings, store: Store):
    lib = demo_lib(cfg, store)
    first = lib.render()
    assert first.name.endswith(" Untitled session.md")
    lib.summarise(NOTE)
    second = lib.render()
    assert second.name.endswith(" Planning meeting.md") and second.is_file() and not first.exists()
    assert store.get_session(SID).note_path == cfg.rel(second)
    renamed = SessionNote(**{**NOTE.to_dict(), "action_items": [], "title": "Budget: Q3 / launch?"})
    store.update_session(SID, note=renamed, title=renamed.title)
    third = lib.render()
    assert third.name.endswith(" Budget Q3 launch.md") and not second.exists()
    assert [p.name for p in (cfg.vault_dir / "sessions").iterdir()] == [third.name]
    assert front_matter(third.read_text(encoding="utf-8"))["title"] == "Budget: Q3 / launch?"


def test_previous_file_outside_the_vault_or_edited_beyond_recognition_is_left_alone(
    cfg: Settings, store: Store, tmp_path: Path
):
    lib = demo_lib(cfg, store)
    old = lib.render()
    old.write_text("my own notes now\n", encoding="utf-8")  # no longer one of our notes
    lib.summarise(NOTE)
    new = lib.render()
    assert new != old and old.read_text(encoding="utf-8") == "my own notes now\n"
    # a remembered path outside the vault is never deleted either
    elsewhere = tmp_path / "elsewhere.md"
    elsewhere.write_text(new.read_text(encoding="utf-8"), encoding="utf-8")
    store.update_session(SID, note_path=str(elsewhere))
    assert lib.render() == new and elsewhere.is_file()


def test_sessions_with_the_same_name_do_not_overwrite_each_other(cfg: Settings, store: Store):
    a = demo_lib(cfg, store).summarise(NOTE)
    b = demo_lib(cfg, store, sid="20261122-143200-cd34").summarise(NOTE)
    c = demo_lib(cfg, store, sid="20261122-143230-ef56", start=T0 + 30).summarise(NOTE)  # same minute
    pa, pb, pc = a.render(), b.render(), c.render()
    assert len({pa, pb, pc}) == 3
    assert [p.name for p in (pa, pb, pc)] == [
        f"{DAY} {clock(T0, '%H%M')} Planning meeting.md",
        f"{DAY} {clock(T0, '%H%M')} Planning meeting (2).md",
        f"{DAY} {clock(T0, '%H%M')} Planning meeting (3).md",
    ]
    for lib, path in ((a, pa), (b, pb), (c, pc)):
        assert front_matter(path.read_text(encoding="utf-8"))["session_id"] == lib.sid
    # rendering again in any order keeps every session on its own file
    assert (c.render(), a.render(), b.render()) == (pc, pa, pb)
    assert len(list((cfg.vault_dir / "sessions").iterdir())) == 3
    # each session embeds its own copies
    for lib, path in ((a, pa), (b, pb)):
        dests = [dest for is_image, _, dest in links(path.read_text(encoding="utf-8")) if is_image]
        assert dests and all(f"/assets/{lib.sid}/" in dest and resolve(path, dest).is_file() for dest in dests)


def test_a_file_of_the_users_with_the_same_name_is_not_overwritten(cfg: Settings, store: Store):
    lib = demo_lib(cfg, store).summarise(NOTE)
    theirs = cfg.vault_dir / "sessions" / f"{DAY} {clock(T0, '%H%M')} Planning meeting.md"
    theirs.parent.mkdir(parents=True, exist_ok=True)
    theirs.write_text("# My own page\n", encoding="utf-8")
    path = lib.render()
    assert path.name.endswith("Planning meeting (2).md")
    assert theirs.read_text(encoding="utf-8") == "# My own page\n"


def test_stale_note_path_never_clobbers_another_sessions_note(cfg: Settings, store: Store):
    a = demo_lib(cfg, store).summarise(NOTE)
    pa = a.render()
    pa.unlink()  # the user deleted A's note by hand; the library still remembers the path
    b = demo_lib(cfg, store, sid="20261122-143200-cd34").summarise(NOTE)
    pb = b.render()
    assert pb == pa  # the name was free
    pa2 = a.render()
    assert pa2 != pb and pa2.name.endswith("(2).md")
    assert front_matter(pb.read_text(encoding="utf-8"))["session_id"] == b.sid
    assert front_matter(pa2.read_text(encoding="utf-8"))["session_id"] == a.sid


def test_note_owner_reads_front_matter_however_it_is_quoted(tmp_path: Path):
    f = tmp_path / "n.md"
    for raw, expected in [
        ('---\ntitle: "x"\nsession_id: "20261122-143200-ab12"\n---\n', SID),
        ("---\nsession_id: 20261122-143200-ab12\n---\n", SID),  # rewritten by an editor without quotes
        ("---\nsession_id: '20261122-143200-ab12'  \n---\n", SID),
        ('---\nsession_id: "a\\"b"\n---\n', 'a"b'),
        ("---\ntitle: x\n---\nsession_id: \"body, not front matter\"\n", None),
        ("# no front matter\nsession_id: \"nope\"\n", None),
        ("", None),
    ]:
        f.write_text(raw, encoding="utf-8")
        assert R._note_owner(f) == expected, raw
    assert R._note_owner(tmp_path / "missing.md") is None and R._note_owner(tmp_path) is None


def test_rendering_twice_is_idempotent(cfg: Settings, store: Store):
    lib = demo_lib(cfg, store).summarise(NOTE, ["Whiteboard walkthrough", "Door sign"])
    path = lib.render()
    day = render_day_note(cfg, store, DAY)
    snapshot = {name: (cfg.vault_dir / name).read_bytes() for name in vault_files(cfg)}
    stamps = {name: (cfg.vault_dir / name).stat().st_mtime_ns for name in snapshot}
    note_path = store.get_session(SID).note_path
    time.sleep(0.02)
    assert lib.render() == path and render_day_note(cfg, store, DAY) == day
    assert {name: (cfg.vault_dir / name).read_bytes() for name in vault_files(cfg)} == snapshot
    # nothing was rewritten at all: unchanged files keep their modification time (kind to sync tools)
    assert {name: (cfg.vault_dir / name).stat().st_mtime_ns for name in snapshot} == stamps
    assert store.get_session(SID).note_path == note_path
    assert not [name for name in snapshot if ".tmp" in name or name.startswith(".")]


def test_ticked_action_items_stay_ticked(cfg: Settings, store: Store):
    lib = demo_lib(cfg, store).summarise(NOTE)
    path = lib.render()
    text = path.read_text(encoding="utf-8")
    done = "- [x] Call the vendor about sensors"
    path.write_text(text.replace("- [ ] Call the vendor about sensors", done), encoding="utf-8")
    again = lib.render().read_text(encoding="utf-8")
    assert done in again and "- [ ] Email the quarterly budget to Sarah" in again
    # ... across a rename too
    renamed = SessionNote(**{**NOTE.to_dict(), "action_items": NOTE.action_items, "title": "Renamed"})
    store.update_session(SID, note=renamed, title="Renamed")
    moved = lib.render()
    assert moved != path and done in moved.read_text(encoding="utf-8")
    # an item whose text changed is a new item
    reworded = SessionNote(**{**NOTE.to_dict(), "action_items": [ActionItem("Call the vendor"), ActionItem("Other")]})
    store.update_session(SID, note=reworded)
    assert "[x]" not in lib.render().read_text(encoding="utf-8")


def test_failed_write_leaves_the_old_note_and_no_debris(cfg: Settings, store: Store, monkeypatch: pytest.MonkeyPatch):
    lib = demo_lib(cfg, store)
    path = lib.render()
    original = path.read_bytes()
    lib.summarise(SessionNote(title="Untitled session", summary="Now with a summary."))

    def fail(src: object, dst: object) -> None:
        if str(dst).endswith(".md"):
            raise OSError(28, "No space left on device")
        return real_replace(src, dst)

    real_replace = os.replace
    monkeypatch.setattr(R.os, "replace", fail)
    with pytest.raises(NoteRenderError) as err:
        lib.render()
    message = str(err.value)
    assert str(cfg.vault_dir) in message and "No space left on device" in message and "config.toml" in message
    assert path.read_bytes() == original
    assert not [p for p in path.parent.iterdir() if p.name != path.name]
    monkeypatch.undo()
    assert "Now with a summary." in lib.render().read_text(encoding="utf-8")


def test_unwritable_vault_gives_an_actionable_error(cfg: Settings, store: Store, tmp_path: Path):
    blocker = tmp_path / "not-a-folder"
    blocker.write_text("x", encoding="utf-8")
    cfg.notes.vault = str(blocker)
    lib = demo_lib(cfg, store)
    with pytest.raises(NoteRenderError, match="Could not write notes into"):
        lib.render()
    with pytest.raises(NoteRenderError, match="point `vault`"):
        render_day_note(cfg, store, DAY)


def test_unknown_session_and_bad_start_time(cfg: Settings, store: Store):
    with pytest.raises(NoteRenderError, match="vnote sessions"):
        render_session_note(cfg, store, "nope")
    store.create_session(Session(id="broken", kind="file", started_ts=float("inf")))
    with pytest.raises(NoteRenderError, match="no usable start time"):
        render_session_note(cfg, store, "broken")


def test_vault_outside_home(cfg: Settings, store: Store, tmp_path: Path):
    cfg.notes.vault = str(tmp_path / "My Obsidian Vault")
    lib = demo_lib(cfg, store).summarise(NOTE)
    path = lib.render()
    assert path.parent == tmp_path / "My Obsidian Vault" / "sessions"
    assert store.get_session(SID).note_path == str(path)  # absolute: it is not inside home
    text = path.read_text(encoding="utf-8")
    assert all(resolve(path, dest).is_file() for is_image, _, dest in links(text) if is_image)
    day = render_day_note(cfg, store, DAY)
    (dest,) = [dest for is_image, _, dest in links(day.read_text(encoding="utf-8")) if not is_image]
    assert resolve(day, dest) == path.resolve()
    lib.summarise(SessionNote(title="Other title"))
    assert lib.render() != path and not path.exists()


# ---------------------------------------------------------------------------
# Unsummarised sessions
# ---------------------------------------------------------------------------


def test_unsummarised_session_still_gets_a_useful_note(cfg: Settings, store: Store):
    lib = demo_lib(cfg, store)
    path = lib.render()
    text = path.read_text(encoding="utf-8")
    fm = front_matter(text)
    assert fm["summarizer"] == "none" and fm["title"] == "Untitled session"
    assert "> **Not summarised yet.**" in text and "`vnote process`" in text
    assert [h for h in headings(text) if h.startswith("## ")] == ["## Captured text", "## Timeline"]
    assert len([h for h in headings(text) if h.startswith("### ")]) == 2
    assert "Room 4B" in text and "quick note to self" in text and text.count("![") == 3
    assert all(resolve(path, dest).is_file() for is_image, _, dest in links(text) if is_image)
    # the session title given at import time is used when there is no note
    store.update_session(SID, title="Tuesday walk")
    assert lib.render().name.endswith(" Tuesday walk.md")


def test_unsegmented_session_is_segmented_for_display_only(cfg: Settings, store: Store):
    lib = Lib(cfg, store)
    lib.frame(1, caption="A desk.").say(2, 8, "First thought.").say(200, 206, "Second thought, much later.")
    lib.commit(segment=False)
    text = lib.render().read_text(encoding="utf-8")
    assert len([h for h in headings(text) if h.startswith("### ")]) == 2
    assert "First thought." in text and "Second thought, much later." in text
    assert store.list_moments(SID) == []  # rendering never writes moments


def test_stale_moment_ids_fall_back_to_time(cfg: Settings, store: Store):
    lib = demo_lib(cfg, store)
    # the clip is transcribed again: utterance ids change, the stored moments still list the old ones
    store.replace_utterances(lib.clip.id, lib._said + [
        Utterance(clip_id=lib.clip.id, session_id=SID, t0=310, t1=312, ts0=T0 + 310, ts1=T0 + 312, text="A late addition.")
    ])  # fmt: skip
    text = lib.render().read_text(encoding="utf-8")
    second = text[text.rindex("### ") :]
    assert "A late addition." in second and "The design review is in room 4B" in second
    assert "quick note to self" in text and "quick note to self" not in second


def test_session_without_any_material(cfg: Settings, store: Store):
    store.create_session(Session(id=SID, kind="live", started_ts=T0))
    path = render_session_note(cfg, store, SID)
    text = path.read_text(encoding="utf-8")
    assert "Not summarised yet" in text and "Nothing has been recognised" in text
    assert headings(text) == ["# Untitled session"]
    assert front_matter(text)["duration"] == "0 s" and front_matter(text)["source"] == ""
    assert f"· {clock(T0)} · 0 s · live*" in text  # no source: the kind of session stands in


# ---------------------------------------------------------------------------
# Hostile text
# ---------------------------------------------------------------------------

HOSTILE = [
    "# heading attempt",
    "</details>",
    "</p></details>\n\n# escaped?",
    "<script>alert(1)</script>",
    "```\ncode fence",
    "~~~python\ntilde fence",
    "````",
    "| a | b |\n|---|---|\n| 1 | 2 |",
    "[click](javascript:alert(1))",
    "![img](http://evil.example/x.png)",
    "[[Some Note]] and ![[embed.png]]",
    "---",
    "===",
    "- [x] not a task",
    "1. numbered",
    "> quote",
    "    indented code",
    "%%hidden%% $x^2$ #tag ==mark== text ^blockid",
    "*** not a rule ***",
    "___",
    "<!-- comment -->",
    "trailing backslash\\",
    "&lt;already&gt; &amp;",
    "\u202eright-to-left override\u202c",
    "nul\x00 and \x1b[31m escape",
    "title: injected\n---\nyaml: break",
    "a\u2028b",
]


def hostile_lib(settings: Settings, store: Store) -> Lib:
    settings.notes.moment_min_seconds = 0.0
    settings.notes.max_images_per_moment = 1
    lib = Lib(settings, store, source="src <script>alert(1)</script>", ended_ts=T0 + 100 * len(HOSTILE))
    for i, text in enumerate(HOSTILE):
        lib.frame(i * 100.0, ocr=text, caption=text)
        lib.say(i * 100.0 + 1, i * 100.0 + 5, text, speaker=text if i % 3 == 0 else None)
    lib.commit()
    assert len(lib.moments) == len(HOSTILE)
    return lib


def assert_inert(text: str) -> None:
    """Nothing from the recording may act as Markdown / HTML structure."""
    lines, html_blocks = scan(text)  # also checks that every code fence and HTML block is closed
    for line in lines:
        if line.startswith("> **Not summarised yet.**"):
            continue  # our own banner, the only quote and the only inline code in a note
        assert "<" not in line, line  # no raw HTML anywhere in the Markdown part
        assert not re.match(r"\s*([-*_])(\s*\1){2,}\s*$", line), f"thematic break: {line!r}"
        assert not re.match(r"\s*(=+|-+)\s*$", line), f"setext underline: {line!r}"
        assert not re.match(r"\s*>", line), f"quote: {line!r}"
        assert not re.search(r"(?<!\\)\|", line), f"table pipe: {line!r}"
        assert not re.search(r"(?<!\\)\[\[", line) and "%%" not in line and "==" not in line, line
        assert not re.search(r"(?<!\\)[`$^~]", line), line
        assert not re.search(r"(?<!\\)#\S", re.sub(r"^#{1,6} ", "", line)), f"tag: {line!r}"
        assert not re.match(r"( {4,}|\t)", line), f"indented code: {line!r}"
        for is_image, _label, dest in ((bang == "!", label, dest) for bang, label, dest in LINK.findall(line)):
            assert dest.startswith("../assets/") if is_image else dest.startswith("../sessions/"), line
    assert html_blocks[-1].startswith("<!-- Written by videonotes.") and html_blocks[-1].endswith("-->")
    for block in html_blocks[:-1]:
        # a transcript: one HTML block (no blank line inside, by construction of scan) made of our tags only
        assert block.startswith("<details>\n<summary>Transcript · ") and block.endswith("</p>\n</details>")
        assert block.count("<details>") == block.count("</details>") == block.count("<summary>") == 1
        inner = re.sub(r"</?(details|summary|p|b)>|<br>", "", block)
        assert "<" not in inner and ">" not in inner, inner
        assert not re.search(r"[`*_\[\]#|$\\~^%=]", inner.replace("&#", "")), inner
    assert "\x00" not in text and "\x1b" not in text and "\u202e" not in text and "\u2028" not in text


def test_hostile_transcripts_and_screen_text_cannot_break_an_unsummarised_note(cfg: Settings, store: Store):
    lib = hostile_lib(cfg, store)
    path = lib.render()
    text = path.read_text(encoding="utf-8")
    assert_inert(text)
    assert headings(text)[:3] == ["# Untitled session", "## Captured text", "## Timeline"]
    moment_headings = headings(text)[3:]
    assert len(moment_headings) == len(HOSTILE)
    assert all(re.fullmatch(r"### \d\d:\d\d(–\d\d:\d\d)?", h) for h in moment_headings)
    # the words themselves are all still there, as text
    assert "&#35; heading attempt" in text and "&lt;/details&gt;" in text
    assert "````text\n```\ncode fence\n````" in text  # a fence longer than the one inside
    assert front_matter(text)["source"] == "src <script>alert(1)</script>"
    images = [dest for is_image, _, dest in links(text) if is_image]
    assert len(images) == len(HOSTILE) and all(resolve(path, dest).is_file() for dest in images)


def test_hostile_summaries_titles_and_tags_cannot_break_a_note(cfg: Settings, store: Store):
    lib = hostile_lib(cfg, store)
    for moment, text in zip(lib.moments, HOSTILE, strict=True):
        store.update_moment(moment.id, title=text, summary=text, tags=[text], kind=text)
    title = "# Plan </details> <script>x</script> ../../etc/passwd\n---\nevil: yes"
    note = SessionNote(
        title=title, summary="\n\n".join(HOSTILE), key_points=list(HOSTILE), decisions=list(HOSTILE),
        open_questions=list(HOSTILE), action_items=[ActionItem(t, t, t, T0 + 5) for t in HOSTILE],
        people=list(HOSTILE), places=list(HOSTILE), captured_text=list(HOSTILE), tags=list(HOSTILE),
        llm_backend="<b>model</b>\n---",
    )  # fmt: skip
    store.update_session(SID, note=note, title=title)
    path = lib.render()
    text = path.read_text(encoding="utf-8")
    assert_inert(text)

    # the file name cannot leave the sessions folder or carry punctuation
    assert path.parent == cfg.vault_dir / "sessions"
    assert path.name == f"{DAY} {clock(T0, '%H%M')} Plan details script x script etc passwd --- evil yes.md"
    # front matter: one key per line, values survive intact, nothing was injected
    fm = front_matter(text)
    assert list(fm) == ["title", "date", "start", "end", "duration", "session_id", "kind", "source", "tags", "summarizer"]
    assert fm["title"] == " ".join(title.split()) and fm["summarizer"] == "<b>model</b> ---"
    assert all(re.fullmatch(r"[\w/-]+", tag) for tag in fm["tags"])  # type: ignore[union-attr]
    # exactly the headings we wrote, in order
    hs = headings(text)
    assert hs[0].startswith("# \\# Plan &lt;/details&gt;")
    assert [h for h in hs if h.startswith("## ")] == [
        "## Summary", "## Key points", "## Action items", "## Decisions", "## Open questions",
        "## People and places", "## Captured text", "## Timeline",
    ]  # fmt: skip
    assert len([h for h in hs if h.startswith("### ")]) == len(HOSTILE)
    # hostile "- [x]" text did not become a ticked task; every real task is unticked
    tasks = [line for line in markdown_lines(text) if line.startswith("- [")]
    assert len(tasks) == len(HOSTILE) and all(line.startswith("- [ ] ") for line in tasks)

    day_store_digest = DayDigest(date=DAY, headline=HOSTILE[0], summary="\n".join(HOSTILE), highlights=list(HOSTILE),
                                 action_items=[ActionItem(t, t, t) for t in HOSTILE], session_ids=[SID])  # fmt: skip
    store.save_day(day_store_digest)
    day = render_day_note(cfg, store, DAY)
    day_text = day.read_text(encoding="utf-8")
    assert_inert(day_text)
    assert headings(day_text)[1:] == ["## Summary", "## Highlights", "## Action items", "## Sessions"]
    (link,) = [dest for is_image, _, dest in links(day_text) if not is_image]
    assert resolve(day, link) == path.resolve()


def test_front_matter_is_valid_yaml_even_for_hostile_values(cfg: Settings, store: Store):
    yaml = pytest.importorskip("yaml")
    lib = hostile_lib(cfg, store)
    title = "\"quoted\" 'single' : colon # hash \\ backslash {curly} [square] & * ! | > % @ ` \ttab é 日本 😀"
    note = SessionNote(title=title, tags=["- dash", "yes", "null", "2026", "a: b", "😀"], llm_backend="x: y # z")
    store.update_session(SID, note=note, title=title, source="/Volumes/DJI: 'SD' \"card\"\\DCIM")
    text = lib.render().read_text(encoding="utf-8")
    data = yaml.safe_load(text[4 : text.index("\n---\n", 4)])
    assert data["title"] == " ".join(title.split())
    assert data["source"] == "/Volumes/DJI: 'SD' \"card\"\\DCIM" and data["summarizer"] == "x: y # z"
    assert data["tags"] == ["dash", "yes", "null", "2026", "a-b"] and all(isinstance(t, str) for t in data["tags"])
    assert data["session_id"] == SID and str(data["date"]) == DAY
    assert data["start"].strftime("%H:%M:%S") == clock(T0, "%H:%M:%S")
    day = render_day_note(cfg, store, DAY)
    day_data = yaml.safe_load(day.read_text(encoding="utf-8").split("\n---\n")[0][4:])
    assert day_data == {"title": DAY, "date": tu.local_dt(T0).date(), "sessions": 1}


def test_escaping_helpers():
    md = R._md
    assert md("plain words, nothing special.") == "plain words, nothing special."
    assert md("# heading") == "\\# heading" and md("  \t# heading") == "\\# heading"
    assert md("- item") == "\\- item" and md("+ item") == "\\+ item" and md("12. item") == "12\\. item"
    assert md("3) item") == "3\\) item" and md("2026 was a year") == "2026 was a year"
    assert md("a | b") == "a \\| b" and md("`code`") == "\\`code\\`"
    assert md("<b>x</b> & y > z") == "&lt;b&gt;x&lt;/b&gt; &amp; y &gt; z"
    assert md("[text](url) ![[embed]]") == "\\[text\\](url) !\\[\\[embed\\]\\]"
    assert md("snake_case *star*") == "snake\\_case \\*star\\*"
    assert md("line one\nline two\r\n\r\nthree") == "line one line two three"
    assert md("") == "" and md(" \n ") == "" and md(None) == "None"
    # prose from the summariser keeps inline emphasis but still cannot start a block
    assert md("this is **important** and _fine_", emphasis=True) == "this is **important** and _fine_"
    assert md("* item", emphasis=True) == "\\* item" and md("***", emphasis=True) == "\\*\\*\\*"
    assert md("**bold** start", emphasis=True) == "**bold** start"
    assert md("~~~python", emphasis=True) == "\\~\\~\\~python"

    html = R._html
    assert html("a <b> & \"c\"") == "a &lt;b&gt; &amp; &quot;c&quot;"
    assert html("# x `y` [[z]] $1 a_b *c* 50% a=b ~t~ \\ ^q |") == (
        "&#35; x &#96;y&#96; &#91;&#91;z&#93;&#93; &#36;1 a&#95;b &#42;c&#42; 50&#37; a&#61;b &#126;t&#126; &#92; &#94;q &#124;"
    )
    assert html("one\n\ntwo") == "one two"

    assert R._fenced("plain") == "```text\nplain\n```"
    assert R._fenced("a ``` b") == "````text\na ``` b\n````"
    assert R._fenced("`````").startswith("``````text\n")

    assert R._tags(["planning", "Q3 launch", "#falcon", "work/meetings", "///", "___", "Planning", "a | b"]) == [
        "planning", "Q3-launch", "falcon", "work/meetings", "a-b",
    ]  # fmt: skip
    assert R._relative_link(Path("/v/sessions/2026-11-22 1432 Café (2).md"), Path("/v/days")) == (
        "../sessions/2026-11-22%201432%20Café%20%282%29.md"
    )
    assert R._safe_component(SID) == SID and R._safe_component("../x y") == ".._x_y" and R._safe_component("..") == "session"


def test_prose_keeps_paragraphs_and_simple_lists():
    out = R._prose("First paragraph\nstill first.\n\n# Not a heading\n- one\n* two\n3. three\nAfter the list.")
    assert out == "First paragraph\nstill first.\n\n\\# Not a heading\n\n- one\n- two\n- three\n\nAfter the list."
    assert R._prose("  \n\n ") == ""


def test_dedupe_texts_ignores_case_punctuation_and_subsets():
    texts = ["Launch plan Q3\nShip Falcon beta", "launch plan q3.", "LAUNCH PLAN Q3\nship falcon beta!", "", None,
             "Launch plan Q3\nNew line here", "  \n  ", "***"]  # fmt: skip
    assert R._dedupe_texts(texts) == ["Launch plan Q3\nShip Falcon beta", "Launch plan Q3\nNew line here", "***"]


def test_screen_text_and_captured_text_are_bounded(cfg: Settings, store: Store):
    lib = Lib(cfg, store)
    for i in range(12):
        lib.frame(i * 2.0, ocr="\n".join(f"frame {i} line {j} " + "x" * 40 for j in range(30)))
    lib.say(1, 20, "Reading a very dense screen.").commit()
    text = lib.render().read_text(encoding="utf-8")
    screen = text[text.index("**On screen**") : text.index("<details>")]
    assert len(screen) < 2600 and "more lines)" in screen
    captured = text[text.index("## Captured text") : text.index("## Timeline")]
    assert len(captured) < 9500 and "more (search the library to find them)" in captured
    assert_inert(text)


# ---------------------------------------------------------------------------
# Day notes
# ---------------------------------------------------------------------------


def day_note_path_in_db(settings: Settings, date: str) -> str | None:
    with sqlite3.connect(settings.db_path) as db:
        row = db.execute("SELECT note_path FROM days WHERE date=?", (date,)).fetchone()
    return row[0] if row else None


def test_day_note_with_digest_and_sessions(cfg: Settings, store: Store):
    a = demo_lib(cfg, store).summarise(NOTE)
    b = demo_lib(cfg, store, sid="20261122-160000-cd34", start=T0 + 5280, source="").summarise(
        SessionNote(title="Walk home", summary="Walked home through the park. Saw a heron! Then rain.")
    )
    c = demo_lib(cfg, store, sid="20261122-170000-ef56", start=T0 + 8880)  # recorded, not summarised, not rendered
    pa, pb = a.render(), b.render()
    digest = DayDigest(
        date=DAY, headline="Planning, then a walk", summary="A planning day.\n\nEnded with a walk.",
        highlights=["Falcon date set", "Saw a heron"],
        action_items=[ActionItem("Email the budget", "me", "Friday", T0 + 8), ActionItem("Buy milk", ts=T0 - 86400 * 3)],
        session_ids=[a.sid, b.sid], llm_backend="ollama:qwen3:4b",
    )  # fmt: skip
    store.save_day(digest)
    path = render_day_note(cfg, store, DAY)
    assert path == cfg.vault_dir / "days" / f"{DAY}.md"
    assert day_note_path_in_db(cfg, DAY) == f"notes/days/{DAY}.md"
    assert store.get_day(DAY) == digest  # saving the path did not disturb the digest

    text = path.read_text(encoding="utf-8")
    assert front_matter(text) == {"title": DAY, "date": DAY, "sessions": 3, "summarizer": "ollama:qwen3:4b"}
    assert headings(text) == [
        f"# {tu.local_dt(T0):%A} {tu.local_dt(T0).day} {tu.local_dt(T0):%B %Y}",
        "## Summary", "## Highlights", "## Action items", "## Sessions",
    ]  # fmt: skip
    assert "**Planning, then a walk**" in text and "A planning day.\n\nEnded with a walk." in text
    assert "- Falcon date set\n- Saw a heron" in text
    assert f"- [ ] Email the budget (owner: me; due: Friday; {clock(T0 + 8)})" in text
    assert "- [ ] Buy milk\n" in text  # its timestamp is from another day: no clock time shown
    assert "*3 sessions · 30 min recorded*" in text

    lines = [line for line in text.split("\n") if line.startswith("- **")]
    assert len(lines) == 3  # in chronological order
    assert lines[0] == (
        f"- **{clock(T0)}–{clock(T0 + 600)}** · [Planning meeting](../sessions/{pa.name.replace(' ', '%20')})"
        " — We went through the launch plan for Q3."
    )
    assert lines[1].startswith(f"- **{clock(T0 + 5280)}–{clock(T0 + 5880)}** · [Walk home](../sessions/")
    assert lines[1].endswith(" — Walked home through the park.")
    assert lines[2] == f"- **{clock(T0 + 8880)}–{clock(T0 + 9480)}** · Untitled session — *not summarised yet*"
    found = [(label, resolve(path, dest)) for is_image, label, dest in links(text) if not is_image]
    assert found == [("Planning meeting", pa.resolve()), ("Walk home", pb.resolve())]
    assert all(target.is_file() for _, target in found)

    # once the third session has a note, it is linked too
    pc = c.render()
    text = render_day_note(cfg, store, DAY).read_text(encoding="utf-8")
    assert f"[Untitled session](../sessions/{pc.name.replace(' ', '%20')}) — *not summarised yet*" in text


def test_day_note_without_digest_lists_sessions_only(cfg: Settings, store: Store):
    lib = demo_lib(cfg, store).summarise(NOTE)
    lib.render()
    path = render_day_note(cfg, store, DAY)
    text = path.read_text(encoding="utf-8")
    assert front_matter(text) == {"title": DAY, "date": DAY, "sessions": 1}
    assert [h for h in headings(text) if h.startswith("## ")] == ["## Sessions"]
    assert "*1 session · 10 min recorded*" in text and "[Planning meeting](" in text
    assert day_note_path_in_db(cfg, DAY) is None and store.get_day(DAY) is None  # no digest: nothing to save


def test_day_note_only_lists_sessions_that_started_that_day(cfg: Settings, store: Store):
    lo, hi = tu.day_bounds(DAY)
    for sid, start, title in (("s-before", lo - 30, "Late last night"), ("s-first", lo, "Midnight"),
                              ("s-last", hi - 30, "Just before midnight"), ("s-after", hi, "Tomorrow")):  # fmt: skip
        store.create_session(Session(id=sid, kind="file", started_ts=start, ended_ts=start + 120, title=title))
    text = render_day_note(cfg, store, DAY).read_text(encoding="utf-8")
    assert "Midnight" in text and "Just before midnight" in text
    assert "Late last night" not in text and "Tomorrow" not in text
    assert text.index("· Midnight") < text.index("· Just before midnight")
    # a session running past midnight says so
    assert f"**{clock(hi - 30)}–{clock(hi + 90)} (+1 d)**" in text


def test_day_without_sessions_says_so(cfg: Settings, store: Store):
    path = render_day_note(cfg, store, "2031-01-05")
    text = path.read_text(encoding="utf-8")
    assert path == cfg.vault_dir / "days" / "2031-01-05.md"
    assert front_matter(text) == {"title": "2031-01-05", "date": "2031-01-05", "sessions": 0}
    assert headings(text) == ["# Sunday 5 January 2031", "## Sessions"]
    assert "*No sessions were recorded on this day.*" in text
    assert render_day_note(cfg, store, " 2031-01-05 ") == path


def test_day_note_keeps_ticks_and_rejects_bad_dates(cfg: Settings, store: Store):
    store.save_day(DayDigest(date=DAY, action_items=[ActionItem("Water the plants"), ActionItem("Call mum")]))
    path = render_day_note(cfg, store, DAY)
    path.write_text(path.read_text(encoding="utf-8").replace("- [ ] Call mum", "- [X] Call mum"), encoding="utf-8")
    text = render_day_note(cfg, store, DAY).read_text(encoding="utf-8")
    assert "- [x] Call mum" in text and "- [ ] Water the plants" in text
    for bad in ("yesterday", "2026-13-40", "", "22/11/2026"):
        with pytest.raises(NoteRenderError, match="YYYY-MM-DD"):
            render_day_note(cfg, store, bad)


# ---------------------------------------------------------------------------
# Size
# ---------------------------------------------------------------------------


def test_three_hour_session_renders_quickly_and_stays_compact(cfg: Settings, store: Store):
    lib = Lib(cfg, store, ended_ts=T0 + 3 * 3600)
    for i in range(360):  # a frame every 30 s; all share one small file on disk
        lib.frame(i * 30.0, ocr=f"Slide {i // 20}\nAgenda item {i // 20}", caption=f"Slide number {i // 20}.")
    t = 0.0
    n = 0
    while t < 3 * 3600:
        lib.say(t, t + 3.0, f"Sentence number {n} of a very long meeting.")
        t += 3.6
        n += 1
    lib.commit()
    assert n == 3000 and 18 <= len(lib.moments) <= 24
    began = time.perf_counter()
    path = lib.render()
    elapsed = time.perf_counter() - began
    text = path.read_text(encoding="utf-8")
    assert elapsed < 15, f"rendering took {elapsed:.1f}s"
    assert text.count("Sentence number") == 3000  # nothing dropped from the transcript
    assert len(text) < 400_000
    assert text.count("![") == 2 * len(lib.moments)
    assert len(list((cfg.vault_dir / "assets" / SID).iterdir())) == 2 * len(lib.moments)
    assert_inert(text)
