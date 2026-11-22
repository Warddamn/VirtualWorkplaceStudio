"""Pipeline behaviour that only shows up when the stages run together."""

from __future__ import annotations

import pytest

from videonotes.backends.base import OcrLine, OcrResult
from videonotes.backends.jsonutil import coerce_to_schema
from videonotes.capture.importer import import_file
from videonotes.cli import main
from videonotes.pipeline import Pipeline
from videonotes.timeutil import local_date


class FlakyOcr:
    """Fails on the first ``fail_first`` calls, then reads 'Hello' on every frame."""

    name = "flaky"

    def __init__(self, fail_first: int):
        self.calls = 0
        self.fail_first = fail_first

    def read(self, image_path):
        self.calls += 1
        if self.calls <= self.fail_first:
            raise RuntimeError("model ran out of memory")
        return OcrResult([OcrLine("Hello whiteboard", 0.99)])

    def close(self) -> None:
        pass


class BrokenOcr(FlakyOcr):
    def __init__(self):
        super().__init__(fail_first=10**9)


def _pipeline(settings, store, ocr):
    settings.asr.backend = "none"
    settings.vision.backend = "none"
    settings.llm.backend = "extractive"
    return Pipeline(settings, store, factories={"ocr": lambda: ocr})


@pytest.fixture()
def session(settings, store, demo_video):
    return import_file(settings, store, demo_video.path, start_ts=1_795_357_920.0)


def test_failed_frames_are_retried_on_the_next_run(settings, store, session):
    ocr = FlakyOcr(fail_first=2)
    with _pipeline(settings, store, ocr) as p:
        out = p.process_session(session.id)
    (clip,) = store.list_clips(session.id)
    assert clip.stages["ocr"]["status"] == "error" and "will retry" in clip.stages["ocr"]["message"]
    assert out.status == "error" and out.note is not None  # notes are still written
    kfs = store.list_keyframes(session_id=session.id)
    assert sum(k.ocr_text is None for k in kfs) == 2  # the two failures stay pending
    with _pipeline(settings, store, ocr) as p:
        out = p.process_session(session.id)
    assert store.list_clips(session.id)[0].stage_done("ocr") and out.status == "ready"
    assert all(k.ocr_text == "Hello whiteboard" for k in store.list_keyframes(session_id=session.id))


def test_frames_that_fail_twice_are_given_up(settings, store, session):
    ocr = BrokenOcr()
    for _ in range(2):
        with _pipeline(settings, store, ocr) as p:
            out = p.process_session(session.id)
    assert store.list_clips(session.id)[0].stage_done("ocr") and out.status == "ready"
    assert all(k.ocr_text == "" for k in store.list_keyframes(session_id=session.id))
    calls = ocr.calls
    with _pipeline(settings, store, ocr) as p:
        p.process_session(session.id)
    assert ocr.calls == calls  # nothing left to retry


def test_deleting_the_last_session_of_a_day_drops_its_digest(settings, store, session, monkeypatch, capsys):
    with _pipeline(settings, store, FlakyOcr(0)) as p:
        p.process_session(session.id)
    day = local_date(session.started_ts)
    assert store.get_day(day) is not None
    day_note = settings.vault_dir / "days" / f"{day}.md"
    assert day_note.is_file()
    store.close()
    monkeypatch.setenv("NO_COLOR", "1")
    assert main(["--home", str(settings.home), "delete", session.id, "--yes"]) == 0
    from videonotes.store import Store

    with Store(settings.db_path) as again:
        assert again.get_day(day) is None
    assert not day_note.exists()


def test_non_finite_numbers_from_a_model_become_zero():
    schema = {"type": "object", "properties": {"n": {"type": "integer"}, "x": {"type": "number"}}}
    assert coerce_to_schema({"n": float("inf"), "x": float("nan")}, schema) == {"n": 0, "x": 0.0}
    assert coerce_to_schema({"n": "1e999"}, schema) == {"n": 0, "x": 0.0}


def test_render_errors_are_plain_messages(settings, monkeypatch, capsys):
    from videonotes.cli import library
    from videonotes.notes.render import NoteRenderError

    def boom(ctx, args):
        raise NoteRenderError("The notes folder /x is not writable. Change notes.vault in config.toml.")

    monkeypatch.setattr(library, "cmd_sessions", boom)
    monkeypatch.setenv("NO_COLOR", "1")
    from videonotes.cli import build_parser, run_command

    args = build_parser().parse_args(["--home", str(settings.home), "sessions"])
    assert run_command(boom, args) == 1
    err = capsys.readouterr().err
    assert "not writable" in err and "Unexpected error" not in err


def test_deleting_one_of_two_sessions_rebuilds_the_day_digest(settings, store, demo_video, monkeypatch, tmp_path):
    import shutil

    other = tmp_path / "second-recording.mp4"  # a different file, so it is not taken for a re-import
    shutil.copyfile(demo_video.path, other)
    first = import_file(settings, store, demo_video.path, start_ts=1_795_357_920.0)
    second = import_file(settings, store, other, start_ts=1_795_357_920.0 + 600)
    assert first.id != second.id
    ocr = FlakyOcr(0)
    with _pipeline(settings, store, ocr) as p:
        p.process_session(first.id)
        p.process_session(second.id)
    day = local_date(first.started_ts)
    assert set(store.get_day(day).session_ids) == {first.id, second.id}
    store.close()
    monkeypatch.setenv("NO_COLOR", "1")
    assert main(["--home", str(settings.home), "--set", "llm.backend=extractive", "delete", second.id, "--yes"]) == 0
    from videonotes.store import Store

    with Store(settings.db_path) as again:
        digest = again.get_day(day)
    assert digest is not None and digest.session_ids == [first.id]
    assert second.id not in (settings.vault_dir / "days" / f"{day}.md").read_text()
