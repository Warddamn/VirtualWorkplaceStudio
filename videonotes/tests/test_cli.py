from __future__ import annotations

import pytest

from videonotes.cli import main
from videonotes.config import Settings
from videonotes.models import ActionItem, Clip, Keyframe, Moment, Session, SessionNote, Utterance
from videonotes.store import Store


@pytest.fixture()
def home(tmp_path, monkeypatch):
    monkeypatch.setenv("NO_COLOR", "1")
    monkeypatch.delenv("VIDEONOTES_HOME", raising=False)
    return tmp_path / "lib"


def _populate(home) -> str:
    settings = Settings(home=home)
    settings.ensure_dirs()
    with Store(settings.db_path) as store:
        t0 = 1_795_357_920.0
        s = store.create_session(Session(id="20261122-143200-ab12", kind="file", started_ts=t0, ended_ts=t0 + 600))
        c = store.add_clip(Clip(session_id=s.id, path="media/x/a.mp4", fingerprint="fp", start_ts=t0, duration=600))
        us = store.replace_utterances(c.id, [
            Utterance(clip_id=c.id, session_id=s.id, t0=5, t1=9, ts0=t0 + 5, ts1=t0 + 9,
                      text="Remember to email the quarterly budget to Sarah before Friday."),
        ])
        kfs = store.replace_keyframes(c.id, [Keyframe(clip_id=c.id, session_id=s.id, t=30, ts=t0 + 30, path="frames/x/k.jpg")])
        store.set_keyframe_ocr(kfs[0].id, "Launch plan Q3\nShip Falcon beta by June 14", "test")
        store.replace_moments(s.id, [
            Moment(session_id=s.id, idx=0, ts0=t0, ts1=t0 + 60, title="Budget reminder", summary="A note to self about the budget.",
                   salience="highlight", utterance_ids=[us[0].id]),
            Moment(session_id=s.id, idx=1, ts0=t0 + 60, ts1=t0 + 600, title="Quiet stretch", salience="background"),
        ])
        note = SessionNote(title="Budget and launch plan", summary="Planned the Falcon beta.", key_points=["Beta ships June 14"],
                           action_items=[ActionItem(text="Email the budget to Sarah", owner="me", due="Friday", ts=t0 + 5)],
                           captured_text=["Launch plan Q3"], llm_backend="extractive")
        store.update_session(s.id, note=note, title=note.title, status="ready")
        # files that `delete` must remove
        for d in (settings.media_dir / s.id, settings.frames_dir / s.id, settings.vault_dir / "assets" / s.id):
            d.mkdir(parents=True)
            (d / "f.bin").write_bytes(b"x")
        note_file = settings.vault_dir / "sessions" / "note.md"
        note_file.parent.mkdir(parents=True)
        note_file.write_text("# note")
        store.update_session(s.id, note_path=settings.rel(note_file))
    return "20261122-143200-ab12"


def test_help_and_empty_library(home, capsys):
    assert main([]) == 2
    assert "typical use" in capsys.readouterr().out
    assert main(["--home", str(home), "sessions"]) == 0
    assert "No sessions yet" in capsys.readouterr().out
    assert main(["--home", str(home), "show"]) == 1
    assert "library is empty" in capsys.readouterr().err
    assert main(["--home", str(home), "search", "anything"]) == 0


def test_sessions_show_search(home, capsys):
    sid = _populate(home)
    assert main(["--home", str(home), "sessions"]) == 0
    out = capsys.readouterr().out
    assert sid in out and "Budget and launch plan" in out and "10 min" in out
    assert main(["--home", str(home), "show", "2026", "--transcript"]) == 0
    out = capsys.readouterr().out
    for expected in ("Budget and launch plan", "Planned the Falcon beta.", "Email the budget to Sarah (me, due Friday)",
                     "Beta ships June 14", "★ Budget reminder", "1 quiet stretch", "quarterly budget", "Launch plan Q3"):
        assert expected in out, expected
    assert "Quiet stretch\n" not in out  # background moment is collapsed
    assert main(["--home", str(home), "show", "nope"]) == 1
    assert "No session matches" in capsys.readouterr().err
    assert main(["--home", str(home), "search", "falcon", "beta"]) == 0
    out = capsys.readouterr().out
    assert "seen (text)" in out and "[Falcon]" in out
    assert main(["--home", str(home), "search", "falcon", "--kind", "utterance"]) == 0
    assert "No matches" in capsys.readouterr().out
    assert main(["--home", str(home), "search", "x", "--day", "not-a-date"]) == 1


def test_delete_removes_everything(home, capsys, monkeypatch):
    sid = _populate(home)
    settings = Settings(home=home)
    assert main(["--home", str(home), "delete", sid]) == 1  # no tty, no --yes
    assert "Refusing" in capsys.readouterr().err
    assert main(["--home", str(home), "delete", sid, "--yes"]) == 0
    assert not (settings.media_dir / sid).exists() and not (settings.frames_dir / sid).exists()
    assert not (settings.vault_dir / "assets" / sid).exists() and not (settings.vault_dir / "sessions" / "note.md").exists()
    with Store(settings.db_path) as store:
        assert store.list_sessions() == [] and store.search("falcon") == []


def test_config_commands(home, capsys):
    assert main(["--home", str(home), "config", "--init"]) == 0
    assert (home / "config.toml").is_file()
    assert main(["--home", str(home), "config", "--init"]) == 1
    capsys.readouterr()
    assert main(["--home", str(home), "--set", "asr.backend=none", "config"]) == 0
    out = capsys.readouterr().out
    assert "[asr]" in out and "backend = 'none'" in out and "[import]" in out
    assert main(["--home", str(home), "--set", "nonsense", "config"]) == 2
    assert main(["--home", str(home), "config", "--path"]) == 0
    assert capsys.readouterr().out.strip().endswith("config.toml")


def test_unexpected_errors_are_plain_messages(home, capsys, monkeypatch):
    import videonotes.cli.library as lib

    def boom(ctx, args):
        raise RuntimeError("kaboom")

    monkeypatch.setattr(lib, "cmd_sessions", boom)
    # the parser captured the original function at registration; patch via set_defaults path instead
    from videonotes.cli import build_parser, run_command

    args = build_parser().parse_args(["--home", str(home), "sessions"])
    args.func = boom
    assert run_command(boom, args) == 1
    err = capsys.readouterr().err
    assert "Unexpected error: RuntimeError: kaboom" in err and "Traceback" not in err
    args.verbose = 1
    with pytest.raises(RuntimeError):
        run_command(boom, args)
