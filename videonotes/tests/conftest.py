from __future__ import annotations

import sys
from pathlib import Path

import pytest

from videonotes.config import Settings
from videonotes.store import Store

sys.path.insert(0, str(Path(__file__).parent))  # lets tests import helper modules such as fake_ollama


@pytest.fixture()
def settings(tmp_path: Path) -> Settings:
    s = Settings(home=tmp_path / "home")
    s.ensure_dirs()
    return s


@pytest.fixture()
def store(settings: Settings):
    st = Store(settings.db_path)
    yield st
    st.close()



@pytest.fixture(scope="session")
def demo_video(tmp_path_factory):
    """The synthetic sample clip (rendered once per test run). Returns a DemoInfo."""
    from videonotes.demo import make_demo_video
    from videonotes.media import ffmpeg as ff

    if not ff.have_ffmpeg():
        pytest.skip("ffmpeg not installed")
    out = tmp_path_factory.mktemp("demo") / "demo.mp4"
    return make_demo_video(out, size="640x360", fps=15, creation_time="2026-11-22T14:32:00Z")
