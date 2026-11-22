from __future__ import annotations

import tomllib

from videonotes.config import default_config_text, load_settings, parse_set_overrides


def test_defaults_and_layout(tmp_path):
    s, warnings = load_settings(tmp_path / "h")
    assert warnings == []
    assert s.db_path == tmp_path / "h" / "library.db"
    assert s.vault_dir == tmp_path / "h" / "notes"
    s.ensure_dirs()
    inside = s.frames_dir / "x" / "1.jpg"
    assert s.rel(inside) == "frames/x/1.jpg"
    assert s.abs("frames/x/1.jpg") == inside
    assert s.abs(s.rel("/somewhere/else.mp4")).as_posix() == "/somewhere/else.mp4"


def test_config_file_and_overrides(tmp_path):
    home = tmp_path / "h"
    home.mkdir()
    (home / "config.toml").write_text(
        '[asr]\nbackend = "sherpa-onnx"\nvad = false\n[frames]\nanalysis_fps = 1\n[import]\ncopy_media = "none"\n'
        '[bogus]\nx = 1\n[llm]\nnope = 2\ncontext_tokens = "abc"\n'
    )
    s, warnings = load_settings(home, parse_set_overrides(["vision.backend=none", "ocr.languages=en-US, de-DE"]))
    assert s.asr.backend == "sherpa-onnx" and s.asr.vad is False
    assert s.frames.analysis_fps == 1.0 and isinstance(s.frames.analysis_fps, float)
    assert s.imports.copy_media == "none"
    assert s.vision.backend == "none" and s.ocr.languages == ["en-US", "de-DE"]
    assert s.llm.context_tokens == 8192
    assert len(warnings) == 3


def test_default_config_text_is_valid_toml_and_complete(tmp_path):
    data = tomllib.loads(default_config_text())
    assert data["capture"]["segment_seconds"] == 60
    home = tmp_path / "h"
    home.mkdir()
    (home / "config.toml").write_text(default_config_text())
    s, warnings = load_settings(home)
    assert warnings == []
