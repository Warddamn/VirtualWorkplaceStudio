from __future__ import annotations

import json

import pytest

from fake_ollama import FakeOllama
from videonotes.capture.devices import CaptureDevice, pick_device
from videonotes.capture.importer import import_file
from videonotes.pipeline import Pipeline
from videonotes.power import PowerState, drain_report, parse_pmset, should_defer_heavy_work

ON_BATTERY = "Now drawing from 'Battery Power'\n -InternalBattery-0 (id=21823587)\t76%; discharging; 4:31 remaining present: true\n"
PLUGGED = "Now drawing from 'AC Power'\n -InternalBattery-0 (id=21823587)\t100%; charged; 0:00 remaining present: true\n"


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        (ON_BATTERY, PowerState(True, 76, 271)),
        (PLUGGED, PowerState(False, 100, None)),
        ("Now drawing from 'AC Power'\n -InternalBattery-0 (id=1) 91%; charging; (no estimate) present: true\n",
         PowerState(False, 91, None)),
        ("Now drawing from 'Battery Power'\n -InternalBattery-0 (id=1)\t35%; discharging; (no estimate) present: true\n",
         PowerState(True, 35, None)),
        ("Now drawing from 'AC Power'\n", PowerState(False, None, None)),  # desktop Mac: no battery
        ("", None),
        ("something else entirely", None),
    ],
)
def test_parse_pmset(text, expected):
    assert parse_pmset(text) == expected


def test_policy_and_drain_report():
    battery, plugged = PowerState(True, 80), PowerState(False, 80)
    assert should_defer_heavy_work("light", battery) and not should_defer_heavy_work("full", battery)
    assert not should_defer_heavy_work("light", plugged) and not should_defer_heavy_work("light", None)
    assert "about 10% per hour" in drain_report(PowerState(True, 80), PowerState(True, 70), 3600)
    assert "plugged in" in drain_report(PowerState(True, 80), PowerState(False, 85), 3600)
    assert "too short" in drain_report(PowerState(True, 80), PowerState(True, 80), 300)
    assert drain_report(None, PowerState(True, 70), 3600) is None
    assert drain_report(PowerState(False, None), PowerState(False, None), 3600) is None


def _fill(schema):
    kind = schema.get("type")
    if kind == "object":
        return {k: _fill(v) for k, v in (schema.get("properties") or {}).items()}
    if kind == "array":
        return []
    if kind == "string":
        return (schema.get("enum") or ["Falcon launch planning"])[0]
    return 0


def _reply(body):
    if body["messages"][-1].get("images"):
        return "A whiteboard with a launch plan in an office."
    fmt = body.get("format")
    return json.dumps(_fill(fmt)) if isinstance(fmt, dict) else "ok"


def test_heavy_work_waits_for_the_charger_and_finishes_later(settings, store, demo_video):
    settings.asr.backend = "none"
    settings.ocr.backend = "rapidocr"
    settings.vision.backend = "ollama"
    settings.llm.backend = "ollama"
    pytest.importorskip("rapidocr")
    session = import_file(settings, store, demo_video.path, start_ts=1_795_357_920.0)
    with FakeOllama(reply=_reply, models=["qwen3:4b", "qwen3-vl:4b-instruct"]) as srv:
        settings.llm.ollama_url = srv.url
        battery = PowerState(True, 60, 200)
        with Pipeline(settings, store, power=lambda: battery) as p:
            out = p.process_session(session.id)
            assert p.deferred == {"vision", "llm"}
        assert out.status == "deferred" and out.note is not None and out.note.llm_backend == "extractive"
        assert srv.calls == []  # nothing heavy ran on battery
        assert all(k.caption is None for k in store.list_keyframes(session_id=session.id))
        (clip,) = store.list_clips(session.id)
        assert clip.stage_done("ocr") and clip.stages["caption"]["status"] == "skipped"

        with Pipeline(settings, store, power=lambda: PowerState(False, 61)) as p:
            out = p.process_session(session.id)
            assert p.deferred == set()
        assert out.status == "ready" and out.note.llm_backend.startswith("ollama:")
        assert any(k.caption for k in store.list_keyframes(session_id=session.id))

        # policy "full" never defers
        settings.power.on_battery = "full"
        with Pipeline(settings, store, power=lambda: battery) as p:
            p.process_session(session.id, force=["summarize"])
            assert p.deferred == set()


def test_builtin_camera_alias():
    devices = [
        CaptureDevice(0, "OsmoAction4", "video"),
        CaptureDevice(1, "Jan's iPhone Camera", "video"),
        CaptureDevice(2, "MacBook Air Camera", "video"),
        CaptureDevice(3, "Capture screen 0", "video"),
        CaptureDevice(0, "MacBook Air Microphone", "audio"),
    ]
    assert pick_device(devices, "video", "mac").name == "MacBook Air Camera"
    assert pick_device(devices, "video", "builtin").name == "MacBook Air Camera"
    assert pick_device(devices, "video", "auto").name == "OsmoAction4"
    older = [CaptureDevice(0, "FaceTime HD Camera (Built-in)", "video")]
    assert pick_device(older, "video", "mac").name.startswith("FaceTime")
    assert pick_device([CaptureDevice(0, "Jan's iPhone Camera", "video")], "video", "mac") is None


def test_cloud_backends_are_not_deferred_on_battery(settings, store):
    """Claude runs in Anthropic's data centre: waiting for the charger would save nothing."""
    settings.vision.backend = "anthropic"
    settings.llm.backend = "ollama"
    calls = []
    factories = {"vision": lambda: calls.append("vision") or None, "llm": lambda: calls.append("llm") or None}
    with Pipeline(settings, store, power=lambda: PowerState(True, 50), factories=factories) as p:
        assert p._backend("vision") is None and p._backend("llm") is None
        assert p.deferred == {"llm"} and calls == ["vision"]
