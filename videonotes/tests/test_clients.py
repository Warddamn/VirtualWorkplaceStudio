from __future__ import annotations

import base64
import json
from types import SimpleNamespace

import pytest

from fake_ollama import FakeOllama
from videonotes.backends import BackendError, BackendUnavailable
from videonotes.backends.anthropic_client import ClaudeClient, _strict_schema
from videonotes.backends.ollama_client import OllamaClient


def test_ollama_chat_images_schema(tmp_path):
    img = tmp_path / "a.jpg"
    img.write_bytes(b"\xff\xd8fake")
    schema = {"type": "object", "properties": {"x": {"type": "string"}}}
    with FakeOllama(reply='{"x": "y"}') as srv:
        c = OllamaClient(srv.url)
        assert c.is_running() and c.has_model("qwen3:4b") and not c.has_model("nope")
        assert c.first_available(["nope", "qwen2.5vl:3b"]) == "qwen2.5vl:3b"
        out = c.chat("qwen3:4b", system="sys", prompt="hi", images=[img], schema=schema, num_ctx=4096, max_tokens=50, keep_alive="30s")
        assert json.loads(out) == {"x": "y"}
        call = srv.calls[-1]
        assert call["stream"] is False and call["format"] == schema and call["keep_alive"] == "30s"
        assert call["options"] == {"num_ctx": 4096, "num_predict": 50, "temperature": 0.2}
        assert call["messages"][0] == {"role": "system", "content": "sys"}
        assert base64.b64decode(call["messages"][1]["images"][0]) == b"\xff\xd8fake"
        with pytest.raises(BackendUnavailable, match="pull"):
            c.chat("missing-model", prompt="hi")
        c.unload("qwen3:4b")
        assert srv.calls[-1]["keep_alive"] == 0


def test_ollama_not_running():
    c = OllamaClient("http://127.0.0.1:9", timeout=1)
    assert c.is_running() is False
    with pytest.raises(BackendUnavailable, match="not running"):
        c.list_models()


class _FakeMessages:
    def __init__(self, response):
        self.response, self.calls = response, []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return self.response


def _fake_client(response):
    stable, beta = _FakeMessages(response), _FakeMessages(response)
    return SimpleNamespace(messages=stable, beta=SimpleNamespace(messages=beta)), stable, beta


def _resp(text="hello", stop="end_turn"):
    return SimpleNamespace(stop_reason=stop, stop_details=SimpleNamespace(category="cyber"),
                           content=[SimpleNamespace(type="thinking", thinking=""), SimpleNamespace(type="text", text=text)])


def test_claude_request_shape(tmp_path):
    img = tmp_path / "a.jpg"
    img.write_bytes(b"\xff\xd8fake")
    client, stable, beta = _fake_client(_resp('{"title": "x"}'))
    c = ClaudeClient(client=client)
    schema = {"type": "object", "properties": {"title": {"type": "string"}, "items": {"type": "array", "items": {"type": "object", "properties": {"t": {"type": "string"}}}}}}
    out = c.complete(system="sys", prompt="describe", images=[img], schema=schema, effort="low")
    assert out == '{"title": "x"}' and not stable.calls
    call = beta.calls[0]
    assert call["model"] == "claude-opus-5-5" and call["fallbacks"] == "default" and call["betas"] == ["server-side-fallback-2026-07-01"]
    assert "thinking" not in call and "temperature" not in call
    assert call["messages"][0]["content"][0]["type"] == "image" and call["messages"][0]["content"][-1] == {"type": "text", "text": "describe"}
    fmt = call["output_config"]["format"]
    assert call["output_config"]["effort"] == "low" and fmt["type"] == "json_schema"
    assert fmt["schema"]["additionalProperties"] is False and fmt["schema"]["required"] == ["title", "items"]
    assert fmt["schema"]["properties"]["items"]["items"]["additionalProperties"] is False
    assert "additionalProperties" not in schema  # caller's schema untouched


def test_claude_other_model_uses_stable_endpoint_and_refusal():
    client, stable, beta = _fake_client(_resp("hi"))
    assert ClaudeClient("claude-haiku-5-5", client=client).complete(system="", prompt="p") == "hi"
    assert stable.calls and not beta.calls and "system" not in stable.calls[0] and "output_config" not in stable.calls[0]
    client, _, _ = _fake_client(_resp("", stop="refusal"))
    with pytest.raises(BackendError, match="declined"):
        ClaudeClient(client=client).complete(system="", prompt="p")


def test_strict_schema_idempotent():
    s = {"type": "object", "properties": {"a": {"type": "string"}}}
    assert _strict_schema(_strict_schema(s)) == _strict_schema(s)
