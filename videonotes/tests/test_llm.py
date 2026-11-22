from __future__ import annotations

import importlib.util
import json
import sys
import types
from types import SimpleNamespace

import pytest

from fake_ollama import FakeOllama
from videonotes.backends import llm as llm_mod
from videonotes.backends.anthropic_client import DEFAULT_MODEL, ClaudeClient
from videonotes.backends.base import LLM, BackendError, BackendUnavailable
from videonotes.backends.jsonutil import schema_prompt
from videonotes.backends.llm import (
    MLX_DEFAULT_MODEL,
    OLLAMA_MODEL_PREFERENCE,
    ClaudeLLM,
    MlxLM,
    OllamaLLM,
    input_budget,
    llm_status,
    make_llm,
)

SCHEMA = {
    "type": "object",
    "properties": {"title": {"type": "string"}, "tags": {"type": "array", "items": {"type": "string"}}},
    "required": ["title", "tags"],
}
DEAD_URL = "http://127.0.0.1:9"  # the discard port: nothing answers there


@pytest.fixture()
def no_mac(monkeypatch):
    """This machine is not an Apple Silicon Mac and has no mlx-lm, whatever is really installed."""
    monkeypatch.setattr(llm_mod, "is_apple_silicon", lambda: False)
    monkeypatch.setattr(llm_mod, "_mlx_installed", lambda: False)


@pytest.fixture()
def mac_with_mlx(monkeypatch):
    monkeypatch.setattr(llm_mod, "is_apple_silicon", lambda: True)
    monkeypatch.setattr(llm_mod, "_mlx_installed", lambda: True)


def _status(settings):
    return {s.name: s for s in llm_status(settings)}


# -- budgets -------------------------------------------------------------------------------


@pytest.mark.parametrize("window", [1024, 2048, 4096, 8192, 16384, 32768])
def test_input_budget_leaves_room_for_the_answer(window):
    budget = input_budget(window)
    reserve = llm_mod._output_reserve(window)
    assert 0 < budget < window
    assert budget + reserve <= window  # a full prompt plus a full answer still fit the window
    assert budget >= window // 4  # ... without starving the prompt
    assert input_budget(window, overhead=1024) <= budget


def test_input_budget_survives_silly_windows():
    assert input_budget(0) > 0 and input_budget(-5) > 0


# -- factory rules ---------------------------------------------------------------------------


@pytest.mark.parametrize("backend", ["extractive", "none", "EXTRACTIVE", " off "])
def test_extractive_means_no_llm(settings, backend):
    settings.llm.backend = backend
    assert make_llm(settings) is None


def test_unknown_backend_names_the_valid_ones(settings):
    settings.llm.backend = "chatgpt"
    with pytest.raises(BackendUnavailable, match="auto, ollama, mlx-lm, anthropic, extractive"):
        make_llm(settings)


def test_explicit_ollama_not_running_says_how_to_start_it(settings):
    settings.llm.backend, settings.llm.ollama_url = "ollama", DEAD_URL
    with pytest.raises(BackendUnavailable, match="not running.*ollama serve"):
        make_llm(settings)


def test_ollama_auto_model_takes_the_best_pulled_one_not_the_first_listed(settings):
    assert OLLAMA_MODEL_PREFERENCE.index("qwen3:4b") < OLLAMA_MODEL_PREFERENCE.index("llama3.2:3b")
    with FakeOllama(models=["nomic-embed-text:latest", "llama3.2:3b", "qwen3:4b", "qwen2.5vl:3b"]) as srv:
        settings.llm.backend, settings.llm.ollama_url = "ollama", srv.url
        llm = make_llm(settings)
        assert isinstance(llm, OllamaLLM) and isinstance(llm, LLM)
        assert llm.name == "ollama:qwen3:4b"
        assert not [c for c in srv.calls if c["path"] == "/api/chat"]  # choosing a model loads nothing


def test_ollama_auto_model_accepts_an_untagged_preference_as_latest(settings):
    with FakeOllama(models=["phi4-mini:latest"]) as srv:
        settings.llm.backend, settings.llm.ollama_url = "ollama", srv.url
        assert make_llm(settings).name == "ollama:phi4-mini"


def test_ollama_auto_model_accepts_a_variant_tag_of_a_preferred_size(settings):
    with FakeOllama(models=["llama3.2-vision:11b", "gemma3:4b-it-qat", "qwen3:32b"]) as srv:
        settings.llm.backend, settings.llm.ollama_url = "ollama", srv.url
        assert make_llm(settings).name == "ollama:gemma3:4b-it-qat"
    with FakeOllama(models=["llama3.2-vision:11b", "qwen3:32b", "gemma4:e4b"]) as srv:  # all too big for 16 GB
        settings.llm.ollama_url = srv.url
        with pytest.raises(BackendUnavailable, match="ollama pull"):
            make_llm(settings)


def test_explicit_ollama_without_a_suitable_model_says_what_to_pull(settings):
    with FakeOllama(models=["nomic-embed-text:latest"]) as srv:
        settings.llm.backend, settings.llm.ollama_url = "ollama", srv.url
        with pytest.raises(BackendUnavailable) as err:
            make_llm(settings)
    assert "ollama pull qwen3:4b" in str(err.value) and "nomic-embed-text" in str(err.value)


def test_explicit_ollama_model_must_be_pulled(settings):
    with FakeOllama(models=["qwen3:4b", "mistral:latest"]) as srv:
        settings.llm.backend, settings.llm.ollama_url = "ollama", srv.url
        settings.llm.model = "gemma3:12b"
        with pytest.raises(BackendUnavailable, match="ollama pull gemma3:12b"):
            make_llm(settings)
        settings.llm.model = "mistral"  # pulled as mistral:latest
        assert make_llm(settings).name == "ollama:mistral"


def test_auto_prefers_a_running_ollama(settings, mac_with_mlx):
    with FakeOllama() as srv:
        settings.llm.ollama_url = srv.url
        assert isinstance(make_llm(settings), OllamaLLM)
        status = _status(settings)
    assert status["ollama"].selected and status["ollama"].available and status["ollama"].detail == "qwen3:4b"
    assert not status["mlx-lm"].selected and not status["anthropic"].selected and not status["extractive"].selected


def test_auto_falls_back_to_mlx_on_apple_silicon(settings, mac_with_mlx):
    settings.llm.ollama_url = DEAD_URL
    llm = make_llm(settings)
    assert isinstance(llm, MlxLM) and isinstance(llm, LLM)
    assert llm.name == f"mlx-lm:{MLX_DEFAULT_MODEL}"
    assert llm._model is None  # nothing is loaded (or downloaded) until the first call
    status = _status(settings)
    assert status["mlx-lm"].selected and MLX_DEFAULT_MODEL in status["mlx-lm"].detail
    assert not status["ollama"].available and "ollama serve" in status["ollama"].detail


def test_auto_uses_mlx_when_ollama_has_nothing_suitable(settings, mac_with_mlx):
    with FakeOllama(models=["nomic-embed-text:latest"]) as srv:
        settings.llm.ollama_url = srv.url
        assert isinstance(make_llm(settings), MlxLM)


def test_auto_does_not_hand_an_ollama_tag_to_mlx(settings, mac_with_mlx):
    settings.llm.ollama_url, settings.llm.model = DEAD_URL, "qwen3:4b"
    assert make_llm(settings) is None
    settings.llm.model = "mlx-community/Some-Model-4bit"
    assert make_llm(settings).name == "mlx-lm:mlx-community/Some-Model-4bit"


def test_auto_without_anything_is_extractive_and_never_the_cloud(settings, no_mac, monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test-not-a-real-key")
    monkeypatch.setattr(llm_mod, "ClaudeClient", lambda *a, **k: pytest.fail("auto must never build a cloud client"))
    settings.llm.ollama_url = DEAD_URL
    assert make_llm(settings) is None
    status = _status(settings)
    assert [s.name for s in llm_status(settings)] == ["ollama", "mlx-lm", "anthropic", "extractive"]
    assert status["extractive"].selected and status["extractive"].available
    assert not status["anthropic"].selected and not status["ollama"].selected and not status["mlx-lm"].selected
    assert "Apple Silicon" in status["mlx-lm"].detail


def test_auto_ignores_mlx_off_apple_silicon(settings, monkeypatch):
    monkeypatch.setattr(llm_mod, "is_apple_silicon", lambda: False)
    monkeypatch.setattr(llm_mod, "_mlx_installed", lambda: True)
    settings.llm.ollama_url = DEAD_URL
    assert make_llm(settings) is None
    settings.llm.backend = "mlx-lm"  # asked for by name it is still allowed (mlx has a CPU build)
    assert isinstance(make_llm(settings), MlxLM)
    assert _status(settings)["mlx-lm"].selected


def test_explicit_mlx_missing_says_what_to_install(settings, monkeypatch):
    settings.llm.backend = "mlx-lm"
    monkeypatch.setattr(llm_mod, "_mlx_installed", lambda: False)
    monkeypatch.setattr(llm_mod, "is_apple_silicon", lambda: True)
    with pytest.raises(BackendUnavailable, match="pip install mlx-lm"):
        make_llm(settings)
    assert "pip install mlx-lm" in _status(settings)["mlx-lm"].detail and not _status(settings)["mlx-lm"].selected
    monkeypatch.setattr(llm_mod, "is_apple_silicon", lambda: False)
    with pytest.raises(BackendUnavailable, match="Apple Silicon.*Ollama"):
        make_llm(settings)


def test_explicit_anthropic_builds_the_cloud_backend(settings, monkeypatch):
    built = []

    class StubClient:
        def __init__(self, model):
            built.append(model)
            self.model = model

    monkeypatch.setattr(llm_mod, "ClaudeClient", StubClient)
    settings.llm.backend = "anthropic"
    llm = make_llm(settings)
    assert isinstance(llm, ClaudeLLM) and isinstance(llm, LLM)
    assert built == [DEFAULT_MODEL] and llm.name == f"anthropic:{DEFAULT_MODEL}"
    assert llm.context_tokens == 150_000
    settings.llm.model = "claude-haiku-5-5"
    assert make_llm(settings).name == "anthropic:claude-haiku-5-5"
    assert built[-1] == "claude-haiku-5-5"
    monkeypatch.setattr(llm_mod, "module_available", lambda name: True)
    settings.llm.ollama_url = DEAD_URL
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    status = _status(settings)["anthropic"]
    assert status.selected and status.available and "ANTHROPIC_API_KEY is not set" in status.detail
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test-not-a-real-key")
    assert "ANTHROPIC_API_KEY" not in _status(settings)["anthropic"].detail


def test_explicit_anthropic_without_the_sdk_says_what_to_install(settings, monkeypatch):
    def missing(model):
        raise BackendUnavailable("The Claude backend needs the Anthropic SDK:  pip install anthropic")

    monkeypatch.setattr(llm_mod, "ClaudeClient", missing)
    monkeypatch.setattr(llm_mod, "module_available", lambda name: name != "anthropic")
    settings.llm.backend = "anthropic"
    with pytest.raises(BackendUnavailable, match="pip install"):
        make_llm(settings)
    status = _status(settings)["anthropic"]
    assert not status.available and not status.selected and "pip install anthropic" in status.detail


def test_status_of_a_failing_explicit_choice_selects_nothing(settings, no_mac):
    settings.llm.backend, settings.llm.ollama_url = "ollama", DEAD_URL
    statuses = llm_status(settings)
    assert not any(s.selected for s in statuses)  # doctor then says: nothing usable yet
    assert all(s.detail for s in statuses)


def test_status_with_ollama_running_but_empty(settings, no_mac):
    with FakeOllama(models=[]) as srv:
        settings.llm.ollama_url = srv.url
        status = _status(settings)
    assert not status["ollama"].available and "ollama pull qwen3:4b" in status["ollama"].detail
    assert status["extractive"].selected


# -- Ollama --------------------------------------------------------------------------------


def _ollama(settings, srv, **cfg) -> OllamaLLM:
    settings.llm.backend, settings.llm.ollama_url = "ollama", srv.url
    for key, value in cfg.items():
        setattr(settings.llm, key, value)
    llm = make_llm(settings)
    assert isinstance(llm, OllamaLLM)
    return llm


def _chats(srv):
    return [c for c in srv.calls if c["path"] == "/api/chat" and c.get("messages")]


def test_ollama_json_request_shape(settings):
    with FakeOllama(reply='{"title": "Budget", "tags": ["q3"], "made_up": 1}') as srv:
        llm = _ollama(settings, srv, context_tokens=8192, keep_alive="45s")
        out = llm.json(system="sys", prompt="evidence", schema=SCHEMA, max_tokens=5000)
        call = _chats(srv)[-1]
    assert out == {"title": "Budget", "tags": ["q3"]}  # extra keys dropped
    assert call["model"] == "qwen3:4b" and call["stream"] is False
    assert call["format"] == SCHEMA  # Ollama's schema-constrained output
    assert call["keep_alive"] == "45s" and call["think"] is False
    assert call["messages"] == [{"role": "system", "content": "sys"}, {"role": "user", "content": "evidence"}]
    options = call["options"]
    assert options["num_ctx"] == 8192 and options["temperature"] == 0.0
    # the caller's input budget plus the capped answer fit the window
    assert options["num_predict"] <= 2048
    assert llm.context_tokens + options["num_predict"] <= options["num_ctx"]
    assert llm.context_tokens < 8192


def test_ollama_context_follows_settings(settings):
    with FakeOllama(reply='{"title": "x", "tags": []}') as srv:
        llm = _ollama(settings, srv, context_tokens=4096)
        llm.json(system="", prompt="p", schema=SCHEMA)
        options = _chats(srv)[-1]["options"]
    assert options["num_ctx"] == 4096
    assert llm.context_tokens == input_budget(4096)
    assert llm.context_tokens + options["num_predict"] <= 4096


def test_ollama_fills_missing_keys_and_fixes_types(settings):
    with FakeOllama(reply='```json\n{"tags": "solo"}\n```') as srv:
        llm = _ollama(settings, srv)
        assert llm.json(system="s", prompt="p", schema=SCHEMA) == {"title": "", "tags": ["solo"]}
        assert len(_chats(srv)) == 1  # fenced JSON needs no second request


def test_ollama_json_with_impossible_numbers_does_not_crash(settings):
    schema = {"type": "object", "properties": {"id": {"type": "integer"}}}
    with FakeOllama(reply='{"id": Infinity}') as srv:  # Python's JSON parser accepts this
        llm = _ollama(settings, srv)
        # Non-finite numbers become 0. Moment ids are 1-based, so summarize discards an id of 0
        # instead of attaching the answer to the wrong moment.
        assert llm.json(system="s", prompt="p", schema=schema) == {"id": 0}


def test_ollama_retries_once_with_a_firmer_instruction(settings):
    replies = iter(["Sure! Here is a summary of the evidence you gave me.", '{"title": "Second try", "tags": []}'])
    with FakeOllama(reply=lambda body: next(replies)) as srv:
        llm = _ollama(settings, srv)
        assert llm.json(system="s", prompt="the evidence", schema=SCHEMA) == {"title": "Second try", "tags": []}
        first, second = _chats(srv)
    assert first["messages"][-1]["content"] == "the evidence"
    retry = second["messages"][-1]["content"]
    assert retry.startswith("the evidence") and "not a JSON object" in retry and schema_prompt(SCHEMA) in retry
    assert second["format"] == SCHEMA and second["options"]["num_ctx"] == first["options"]["num_ctx"]
    assert "think" not in second  # leave reasoning at the model's default the second time


def test_ollama_gives_up_after_one_retry(settings):
    with FakeOllama(reply="I cannot help with that.") as srv:
        llm = _ollama(settings, srv)
        with pytest.raises(BackendError, match="did not return JSON"):
            llm.json(system="s", prompt="p", schema=SCHEMA)
        assert len(_chats(srv)) == 2


def test_ollama_text_strips_reasoning_and_sends_no_schema(settings):
    with FakeOllama(reply="<think>the user wants a short answer</think>\nRow G, level two.") as srv:
        llm = _ollama(settings, srv)
        assert llm.text(system="s", prompt="where did I park?") == "Row G, level two."
        call = _chats(srv)[-1]
    assert "format" not in call and call["options"]["num_ctx"] == settings.llm.context_tokens


def test_ollama_close_unloads_only_what_it_loaded(settings):
    with FakeOllama(reply='{"title": "x", "tags": []}') as srv:
        llm = _ollama(settings, srv)
        llm.close()
        assert not [c for c in srv.calls if c["path"] == "/api/chat"]  # never used: nothing to unload
        llm.json(system="s", prompt="p", schema=SCHEMA)
        llm.close()
        unload = srv.calls[-1]
        assert unload["model"] == "qwen3:4b" and unload["keep_alive"] == 0 and unload["messages"] == []
        llm.close()  # idempotent
        assert srv.calls[-1] is unload


def test_ollama_server_gone_is_reported_as_unavailable(settings):
    with FakeOllama(reply='{"title": "x", "tags": []}') as srv:
        llm = _ollama(settings, srv)
        llm.json(system="s", prompt="p", schema=SCHEMA)
    with pytest.raises(BackendUnavailable, match="not running"):
        llm.json(system="s", prompt="p", schema=SCHEMA)
    llm.close()  # must not raise although the server is gone


# -- Claude ---------------------------------------------------------------------------------


class _Messages:
    def __init__(self, text):
        self.text, self.calls = text, []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return SimpleNamespace(stop_reason="end_turn", content=[SimpleNamespace(type="text", text=self.text)])


def _claude(text, model="claude-haiku-5-5"):
    messages = _Messages(text)
    client = SimpleNamespace(messages=messages, beta=SimpleNamespace(messages=messages))
    return ClaudeLLM(ClaudeClient(model, client=client)), messages


def test_claude_json_uses_structured_outputs():
    llm, messages = _claude('{"title": "Launch plan", "tags": ["q3"], "extra": true}')
    assert isinstance(llm, LLM) and llm.name == "anthropic:claude-haiku-5-5" and llm.context_tokens == 150_000
    out = llm.json(system="rules", prompt="evidence", schema=SCHEMA, max_tokens=500)
    assert out == {"title": "Launch plan", "tags": ["q3"]}
    call = messages.calls[0]
    assert call["model"] == "claude-haiku-5-5" and call["system"] == "rules"
    assert call["messages"][0]["content"][-1] == {"type": "text", "text": "evidence"}
    fmt = call["output_config"]["format"]
    assert fmt["type"] == "json_schema" and fmt["schema"]["properties"] == SCHEMA["properties"]
    assert fmt["schema"]["additionalProperties"] is False
    assert call["max_tokens"] >= 4096  # a small cap would only truncate the note
    llm.close()


def test_claude_text_and_non_json():
    llm, messages = _claude("  Row G, level two.  ")
    assert llm.text(system="s", prompt="p") == "Row G, level two."
    assert "output_config" not in messages.calls[0]
    with pytest.raises(BackendError, match="did not return JSON"):
        llm.json(system="s", prompt="p", schema=SCHEMA)


# -- mlx-lm (fake modules pin the call sequence verified against mlx-lm 0.32) -----------------


class _FakeTokenizer:
    """Mimics mlx_lm.tokenizer_utils.TokenizerWrapper as far as the adapter touches it."""

    def __init__(self, log, *, has_chat_template=True, reject_system=False, reject_thinking_kwarg=False):
        self.log = log
        self.has_chat_template = has_chat_template
        self.reject_system = reject_system
        self.reject_thinking_kwarg = reject_thinking_kwarg

    def apply_chat_template(self, messages, **kwargs):
        self.log.append(("apply_chat_template", messages, kwargs))
        if self.reject_thinking_kwarg and "enable_thinking" in kwargs:
            raise TypeError("apply_chat_template() got an unexpected keyword argument 'enable_thinking'")
        if self.reject_system and any(m["role"] == "system" for m in messages):
            raise ValueError("System role not supported")  # what a Jinja raise_exception turns into
        return [1, 2, 3, len(messages)]


@pytest.fixture()
def fake_mlx(monkeypatch):
    """Install fake ``mlx_lm`` / ``mlx`` modules; returns a namespace to script and inspect them."""
    log: list = []
    state = SimpleNamespace(
        log=log, replies=['{"title": "From MLX", "tags": ["a"]}'], tokenizer=_FakeTokenizer(log), load_error=None,
        model=object(),
    )  # fmt: skip

    def load(path_or_hf_repo, **kwargs):
        log.append(("load", path_or_hf_repo, kwargs))
        if state.load_error is not None:
            raise state.load_error
        return state.model, state.tokenizer

    def generate(model, tokenizer, prompt, verbose=False, **kwargs):
        log.append(("generate", model, tokenizer, prompt, verbose, kwargs))
        return state.replies.pop(0) if len(state.replies) > 1 else state.replies[0]

    def make_sampler(temp=0.0, **kwargs):
        log.append(("make_sampler", temp, kwargs))
        return ("sampler", temp)

    mlx_lm = types.ModuleType("mlx_lm")
    mlx_lm.load, mlx_lm.generate = load, generate
    sample_utils = types.ModuleType("mlx_lm.sample_utils")
    sample_utils.make_sampler = make_sampler
    mlx_lm.sample_utils = sample_utils
    mlx = types.ModuleType("mlx")
    core = types.ModuleType("mlx.core")
    core.clear_cache = lambda: log.append(("clear_cache",))
    mlx.core = core
    for name, module in (("mlx_lm", mlx_lm), ("mlx_lm.sample_utils", sample_utils), ("mlx", mlx), ("mlx.core", core)):
        monkeypatch.setitem(sys.modules, name, module)
    state.core = core
    state.mlx = mlx
    return state


def _calls(state, name):
    return [entry for entry in state.log if entry[0] == name]


def test_mlx_call_sequence(fake_mlx):
    llm = MlxLM("mlx-community/Qwen3-4B-Instruct-2507-4bit", context_tokens=8192)
    assert isinstance(llm, LLM) and not fake_mlx.log  # constructing loads nothing
    assert llm.context_tokens < input_budget(8192)  # the schema travels in the prompt: keep room for it

    out = llm.json(system="the rules", prompt="the evidence", schema=SCHEMA, max_tokens=700)
    assert out == {"title": "From MLX", "tags": ["a"]}
    assert [entry[0] for entry in fake_mlx.log] == ["load", "apply_chat_template", "make_sampler", "generate"]

    # model, tokenizer = mlx_lm.load(repo)
    assert _calls(fake_mlx, "load") == [("load", "mlx-community/Qwen3-4B-Instruct-2507-4bit", {})]
    # prompt = tokenizer.apply_chat_template(messages, add_generation_prompt=True, enable_thinking=False)
    _, messages, kwargs = _calls(fake_mlx, "apply_chat_template")[0]
    assert kwargs == {"add_generation_prompt": True, "enable_thinking": False}
    assert [m["role"] for m in messages] == ["system", "user"] and messages[0]["content"] == "the rules"
    assert messages[1]["content"] == "the evidence\n\n" + schema_prompt(SCHEMA)
    # text = generate(model, tokenizer, prompt=prompt, max_tokens=n, sampler=make_sampler(temp=0.0), verbose=False)
    assert _calls(fake_mlx, "make_sampler") == [("make_sampler", 0.0, {})]
    _, model, tokenizer, prompt, verbose, gen_kwargs = _calls(fake_mlx, "generate")[0]
    assert model is fake_mlx.model and tokenizer is fake_mlx.tokenizer
    assert prompt == [1, 2, 3, 2] and verbose is False
    assert gen_kwargs == {"max_tokens": 700, "sampler": ("sampler", 0.0)}

    llm.text(system="s", prompt="p")
    assert len(_calls(fake_mlx, "load")) == 1  # the model stays loaded between calls


def test_mlx_answer_is_capped_to_what_the_window_leaves(fake_mlx):
    llm = MlxLM(context_tokens=4096)
    llm.json(system="s", prompt="p", schema=SCHEMA, max_tokens=100_000)
    cap = _calls(fake_mlx, "generate")[0][5]["max_tokens"]
    assert cap <= 1024 and llm.context_tokens + cap <= 4096


def test_mlx_strips_reasoning_and_retries_once(fake_mlx):
    fake_mlx.replies = ["<think>let me think {not json", '<think>ok</think>{"title": "Retry", "tags": []}']
    llm = MlxLM()
    assert llm.json(system="s", prompt="evidence", schema=SCHEMA) == {"title": "Retry", "tags": []}
    first, second = (entry[1][-1]["content"] for entry in _calls(fake_mlx, "apply_chat_template"))
    assert "not a JSON object" not in first and "not a JSON object" in second and second.startswith("evidence")
    fake_mlx.replies = ["still no json"]
    with pytest.raises(BackendError, match="did not return JSON"):
        llm.json(system="s", prompt="evidence", schema=SCHEMA)
    assert llm.text(system="s", prompt="p") == "still no json"


def test_mlx_template_without_system_role(fake_mlx):
    fake_mlx.tokenizer.reject_system = True
    MlxLM().json(system="the rules", prompt="the evidence", schema=SCHEMA)
    attempts = _calls(fake_mlx, "apply_chat_template")
    final_messages, final_kwargs = attempts[-1][1], attempts[-1][2]
    assert [m["role"] for m in final_messages] == ["user"]
    assert final_messages[0]["content"].startswith("the rules\n\nthe evidence")
    assert final_kwargs == {"add_generation_prompt": True, "enable_thinking": False}  # thinking stays off


def test_mlx_tokenizer_that_rejects_the_thinking_switch(fake_mlx):
    fake_mlx.tokenizer.reject_thinking_kwarg = True
    MlxLM().json(system="the rules", prompt="the evidence", schema=SCHEMA)
    last = _calls(fake_mlx, "apply_chat_template")[-1]
    assert [m["role"] for m in last[1]] == ["system", "user"] and last[2] == {"add_generation_prompt": True}


def test_mlx_model_without_chat_template_gets_plain_text(fake_mlx):
    fake_mlx.tokenizer.has_chat_template = False
    MlxLM().text(system="the rules", prompt="the question")
    assert not _calls(fake_mlx, "apply_chat_template")
    assert _calls(fake_mlx, "generate")[0][3] == "the rules\n\nthe question"


def test_mlx_close_frees_model_and_cache(fake_mlx):
    llm = MlxLM()
    llm.close()
    assert not fake_mlx.log  # nothing was loaded: nothing to free, mlx is not even imported
    llm.text(system="s", prompt="p")
    llm.close()
    assert llm._model is None and llm._tokenizer is None
    assert fake_mlx.log[-1] == ("clear_cache",)
    llm.text(system="s", prompt="p")  # usable again: reloads
    assert len(_calls(fake_mlx, "load")) == 2


def test_mlx_close_with_older_mlx_cache_api(fake_mlx):
    del fake_mlx.core.clear_cache
    fake_mlx.core.metal = SimpleNamespace(clear_cache=lambda: fake_mlx.log.append(("metal.clear_cache",)))
    llm = MlxLM()
    llm.text(system="s", prompt="p")
    llm.close()
    assert fake_mlx.log[-1] == ("metal.clear_cache",)


def test_mlx_load_failure_is_actionable_and_not_retried(fake_mlx):
    fake_mlx.load_error = OSError("Repository Not Found for url: https://huggingface.co/api/models/nope/nope")
    llm = MlxLM("nope/nope")
    for _ in range(2):
        with pytest.raises(BackendUnavailable) as err:
            llm.json(system="s", prompt="p", schema=SCHEMA)
        assert "nope/nope" in str(err.value) and "llm.model" in str(err.value) and "Ollama" in str(err.value)
    assert len(_calls(fake_mlx, "load")) == 1  # a download that failed is not attempted for every moment
    llm.close()


def test_mlx_not_importable(monkeypatch):
    monkeypatch.setitem(sys.modules, "mlx_lm", None)  # makes `import mlx_lm` raise ImportError
    monkeypatch.setattr(llm_mod, "is_apple_silicon", lambda: True)
    with pytest.raises(BackendUnavailable, match="pip install mlx-lm"):
        MlxLM().text(system="s", prompt="p")


def test_mlx_generation_error_is_a_backend_error(fake_mlx):
    def boom(*args, **kwargs):
        raise RuntimeError("[metal] out of memory")

    sys.modules["mlx_lm"].generate = boom
    with pytest.raises(BackendError, match="out of memory"):
        MlxLM().text(system="s", prompt="p")


def test_mlx_cache_probe(tmp_path, monkeypatch):
    monkeypatch.setenv("HF_HUB_CACHE", str(tmp_path / "hub"))
    assert llm_mod._mlx_cached("org/model") is False
    (tmp_path / "hub" / "models--org--model" / "snapshots" / "abc123").mkdir(parents=True)
    assert llm_mod._mlx_cached("org/model") is True
    local = tmp_path / "my-model"
    local.mkdir()
    assert llm_mod._mlx_cached(str(local)) is True


@pytest.mark.slow
@pytest.mark.skipif(
    not all(importlib.util.find_spec(m) for m in ("mlx_lm", "mlx", "tokenizers", "transformers")),
    reason="mlx-lm is not installed here (it needs Apple Silicon, or mlx[cpu] on Linux)",
)
def test_mlx_adapter_against_the_real_library(tmp_path):
    """Runs the adapter through the real mlx-lm with a tiny random-weight model (text is gibberish)."""
    import mlx.core as mx
    from mlx.utils import tree_flatten
    from mlx_lm.models.llama import Model, ModelArgs
    from tokenizers import Tokenizer, decoders, models, pre_tokenizers, trainers
    from transformers import PreTrainedTokenizerFast

    out = tmp_path / "tiny"
    out.mkdir()
    tok = Tokenizer(models.BPE(unk_token="<unk>"))
    tok.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=False)
    tok.decoder = decoders.ByteLevel()
    trainer = trainers.BpeTrainer(
        vocab_size=300, special_tokens=["<unk>", "<s>", "</s>"], initial_alphabet=pre_tokenizers.ByteLevel.alphabet()
    )
    tok.train_from_iterator(["meeting notes action items budget review launch plan friday"] * 50, trainer)
    fast = PreTrainedTokenizerFast(tokenizer_object=tok, bos_token="<s>", eos_token="</s>", unk_token="<unk>", pad_token="</s>")
    fast.chat_template = (
        "{% for m in messages %}{{ '<|' + m['role'] + '|>' + m['content'] }}{% endfor %}"
        "{% if add_generation_prompt %}<|assistant|>{% endif %}"
    )
    fast.save_pretrained(out)
    cfg = {
        "model_type": "llama", "hidden_size": 64, "num_hidden_layers": 2, "intermediate_size": 128,
        "num_attention_heads": 4, "num_key_value_heads": 2, "rms_norm_eps": 1e-5, "vocab_size": len(fast),
        "max_position_embeddings": 512, "tie_word_embeddings": True, "bos_token_id": fast.bos_token_id,
        "eos_token_id": fast.eos_token_id,
    }  # fmt: skip
    (out / "config.json").write_text(json.dumps(cfg))
    model = Model(ModelArgs.from_dict(cfg))
    mx.eval(model.parameters())
    mx.save_safetensors(str(out / "model.safetensors"), dict(tree_flatten(model.parameters())))
    del model

    llm = MlxLM(str(out), context_tokens=2048)
    text = llm.text(system="You write notes.", prompt="budget review", max_tokens=16)
    assert isinstance(text, str)
    with pytest.raises(BackendError, match="did not return JSON"):  # random weights cannot produce JSON
        llm.json(system="You write notes.", prompt="budget review", schema=SCHEMA, max_tokens=16)
    llm.close()
    assert llm._model is None
