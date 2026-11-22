"""Text LLM backends for summaries and question answering.

``make_llm(settings)`` returns something that satisfies :class:`videonotes.backends.base.LLM`,
or ``None`` when summaries should be built without a model (the callers in
``videonotes.notes.summarize`` then use their extractive fallbacks).

Backends
--------
``ollama``
    A local Ollama server (default).  JSON comes from Ollama's schema-constrained
    ``format``; the context window is set per request (``num_ctx``) because Ollama's
    default of 4096 tokens silently truncates longer prompts.
``mlx-lm``
    In-process on Apple Silicon.  mlx-lm has no schema-constrained decoding, so the
    schema is described in the prompt and the reply is parsed leniently.
``anthropic``
    The Claude API.  Only when chosen explicitly: ``auto`` never leaves the laptop.
``extractive``
    No model at all.

``auto`` picks, in this order: Ollama if it is running and already has a suitable
model -> mlx-lm if it is installed on an Apple Silicon Mac -> none.

Token budgets
-------------
``LLM.context_tokens`` is the budget of *input* tokens a caller may put into one
prompt (system + user text).  For the local backends it is smaller than the model's
context window (``llm.context_tokens`` in the settings): room is kept for the answer
and for the chat template, so a prompt that respects the budget is never truncated.
"""

from __future__ import annotations

import gc
import logging
import os
import re
from pathlib import Path
from typing import Any

from ..config import Settings, is_apple_silicon
from .anthropic_client import DEFAULT_MODEL as CLAUDE_DEFAULT_MODEL
from .anthropic_client import ClaudeClient
from .base import LLM, BackendError, BackendUnavailable
from .jsonutil import coerce_to_schema, extract_json, schema_prompt
from .ollama_client import NOT_RUNNING_HINT, OllamaClient
from .status import BackendStatus, module_available

log = logging.getLogger("videonotes.llm")

__all__ = [
    "MLX_DEFAULT_MODEL",
    "OLLAMA_MODEL_PREFERENCE",
    "OLLAMA_PULL_SUGGESTION",
    "ClaudeLLM",
    "MlxLM",
    "OllamaLLM",
    "input_budget",
    "llm_status",
    "make_llm",
]

#: Text models that fit a 16 GB Mac with nothing else loaded (about 2-6 GB), best first.
#: ``auto`` uses the first one that is already pulled.  Order: the small instruct models the
#: model research ranked for summaries (Qwen3.5-4B, Qwen3-4B, Gemma 3 4B / Gemma 4 E2B at Q4,
#: Phi-4-mini, Llama 3.2 3B), then smaller siblings, then the 9B quality tier (fits alone, but
#: slower), and last the small vision models a user may already have pulled for captions -
#: they summarise text as well, which beats having no model.  Larger default tags (such as
#: gemma4:e4b at about 10 GB) are deliberately absent: they do not fit next to an 8k context.
OLLAMA_MODEL_PREFERENCE: tuple[str, ...] = (
    "qwen3.5:4b",
    "qwen3:4b",
    "gemma3:4b",
    "gemma4:e2b-it-q4_K_M",
    "phi4-mini",
    "llama3.2:3b",
    "llama3.2",
    "qwen3.5:2b",
    "gemma3n:e4b",
    "qwen3.5:9b",
    "qwen3-vl:4b",
    "qwen2.5vl:3b",
)

#: The model suggested when Ollama runs but has nothing suitable.
OLLAMA_PULL_SUGGESTION = "qwen3:4b"

#: Default MLX model: the small instruct model mlx-lm itself benchmarks (about 3.4 GB peak at 4-bit).
MLX_DEFAULT_MODEL = "mlx-community/Qwen3-4B-Instruct-2507-4bit"

#: Input budget of the cloud backend (well inside the model's context window).
CLAUDE_CONTEXT_TOKENS = 150_000

_BACKENDS = ("auto", "ollama", "mlx-lm", "anthropic", "extractive")
_ALIASES = {"mlx": "mlx-lm", "mlx_lm": "mlx-lm", "claude": "anthropic", "none": "extractive", "off": "extractive", "": "auto"}

_MLX_INSTALL = "pip install mlx-lm"
_THINK_BLOCK = re.compile(r"<think>.*?</think>", re.S | re.I)
_THINK_OPEN = re.compile(r"<think>.*\Z", re.S | re.I)

_RETRY_NOTE = "Your previous reply was not a JSON object. "


# -- budgets ---------------------------------------------------------------------------------


def _output_reserve(window: int) -> int:
    """Tokens of the context window kept free for the model's answer."""
    return max(256, min(2048, window // 4))


def input_budget(window: int, *, overhead: int = 512) -> int:
    """Input tokens a caller may use in a context window of ``window`` tokens.

    ``overhead`` covers the chat template, the JSON instruction a retry appends and the
    slack of estimating tokens from characters.  Never less than a quarter of the window.
    """
    window = max(512, int(window))
    return max(window // 4, window - _output_reserve(window) - min(overhead, window // 8))


def _strip_thinking(text: str) -> str:
    """Drop ``<think>`` blocks (also one that was cut off before it closed)."""
    return _THINK_OPEN.sub("", _THINK_BLOCK.sub("", text or "")).strip()


def _shaped(obj: dict[str, Any], schema: dict[str, Any], name: str) -> dict[str, Any]:
    """``obj`` forced into the shape of ``schema`` (a model can emit ``NaN`` where an integer belongs)."""
    try:
        return coerce_to_schema(obj, schema)
    except (ValueError, OverflowError, TypeError, RecursionError) as exc:
        raise BackendError(f"{name} returned JSON that does not fit the requested shape ({exc})") from exc


def _firmer(prompt: str, schema: dict[str, Any]) -> str:
    return f"{prompt}\n\n{_RETRY_NOTE}{schema_prompt(schema)}"


# -- Ollama --------------------------------------------------------------------------------------


class OllamaLLM:
    """A text model served by a local Ollama server."""

    def __init__(self, client: OllamaClient, model: str, *, num_ctx: int = 8192, keep_alive: str | int | None = "30s"):
        self.client = client
        self.model = model
        self.name = f"ollama:{model}"
        self.num_ctx = max(1024, int(num_ctx))
        self.keep_alive = keep_alive
        self.context_tokens = input_budget(self.num_ctx)
        self._used = False

    def _max_tokens(self, wanted: int) -> int:
        # the answer has to fit into what the input budget leaves free in the window
        return max(64, min(int(wanted), _output_reserve(self.num_ctx)))

    def json(self, *, system: str, prompt: str, schema: dict[str, Any], max_tokens: int = 2048) -> dict[str, Any]:
        """One schema-constrained reply. Retries once, more firmly, if no JSON object came back."""
        self._used = True
        raw = self.client.chat(
            self.model, system=system, prompt=prompt, schema=schema, num_ctx=self.num_ctx,
            max_tokens=self._max_tokens(max_tokens), temperature=0.0, keep_alive=self.keep_alive,
        )  # fmt: skip
        obj = extract_json(raw)
        if obj is None:
            log.info("%s returned no JSON object (%d chars); asking once more", self.name, len(raw))
            # think=None leaves the reasoning switch at the model's default: some reasoning
            # models ignore `format` while thinking is forced off.
            raw = self.client.chat(
                self.model, system=system, prompt=_firmer(prompt, schema), schema=schema, num_ctx=self.num_ctx,
                max_tokens=self._max_tokens(max_tokens), temperature=0.0, keep_alive=self.keep_alive, think=None,
            )  # fmt: skip
            obj = extract_json(raw)
        if obj is None:
            raise BackendError(f"{self.name} did not return JSON (got: {raw[:120]!r})")
        return _shaped(obj, schema, self.name)

    def text(self, *, system: str, prompt: str, max_tokens: int = 1024) -> str:
        self._used = True
        raw = self.client.chat(
            self.model, system=system, prompt=prompt, num_ctx=self.num_ctx,
            max_tokens=self._max_tokens(max_tokens), temperature=0.2, keep_alive=self.keep_alive,
        )  # fmt: skip
        return _strip_thinking(raw)

    def close(self) -> None:
        """Ask the server to drop the model from memory now (the next stage needs the RAM)."""
        if self._used:
            self._used = False
            self.client.unload(self.model)


def _pick_ollama_model(pulled: list[str]) -> str | None:
    """The best already-pulled model of the preference list, or None."""
    names = set(pulled)
    for cand in OLLAMA_MODEL_PREFERENCE:
        if cand in names or (":" not in cand and cand + ":latest" in names):
            return cand
    for cand in OLLAMA_MODEL_PREFERENCE:  # a variant tag of a preferred size, e.g. "gemma3:4b-it-qat"
        if ":" in cand:
            for name in sorted(names):
                if name.startswith(cand + "-"):
                    return name
    return None


def _ollama_probe(settings: Settings) -> tuple[OllamaClient, str | None, str]:
    """``(client, model or None, detail)`` - detail says what to do when model is None."""
    cfg = settings.llm
    client = OllamaClient(cfg.ollama_url)
    if not client.is_running():
        return client, None, NOT_RUNNING_HINT.format(url=client.url)
    try:
        pulled = client.list_models()
    except (BackendUnavailable, BackendError) as exc:
        return client, None, f"Ollama at {client.url} did not list its models ({exc}). Restart Ollama and try again."
    wanted = (cfg.model or "auto").strip()
    if wanted.lower() == "auto":
        best = _pick_ollama_model(pulled)
        if best is not None:
            return client, best, best
        have = f" Pulled now: {', '.join(sorted(pulled)[:8])}." if pulled else ""
        return (
            client,
            None,
            f"Ollama is running but has no suitable text model. Pull one:  ollama pull {OLLAMA_PULL_SUGGESTION}"
            f"  (or set llm.model in config.toml to a model you already have).{have}",
        )
    if wanted in pulled or (":" not in wanted and wanted + ":latest" in pulled):
        return client, wanted, wanted
    return client, None, f'Ollama does not have the model "{wanted}" yet. Pull it:  ollama pull {wanted}'


def _make_ollama(settings: Settings, *, strict: bool) -> OllamaLLM | None:
    client, model, detail = _ollama_probe(settings)
    if model is None:
        if strict:
            raise BackendUnavailable(detail)
        log.debug("ollama not usable for summaries: %s", detail)
        return None
    cfg = settings.llm
    return OllamaLLM(client, model, num_ctx=cfg.context_tokens, keep_alive=cfg.keep_alive or None)


# -- mlx-lm ----------------------------------------------------------------------------------------


def _mlx_model(settings: Settings) -> str:
    wanted = (settings.llm.model or "auto").strip()
    return MLX_DEFAULT_MODEL if wanted.lower() == "auto" else wanted


def _mlx_installed() -> bool:
    return module_available("mlx_lm") and module_available("mlx")


def _mlx_cached(model: str) -> bool:
    """True if ``model`` is a local folder or already sits in the Hugging Face cache.

    Only used to word log messages and the doctor output, so a wrong guess is harmless.
    """
    try:
        if Path(model).expanduser().exists():
            return True
        hub = os.environ.get("HF_HUB_CACHE") or os.environ.get("HUGGINGFACE_HUB_CACHE")
        root = Path(hub) if hub else Path(os.environ.get("HF_HOME") or "~/.cache/huggingface") / "hub"
        snapshots = root.expanduser() / ("models--" + model.strip("/").replace("/", "--")) / "snapshots"
        return snapshots.is_dir() and any(snapshots.iterdir())
    except OSError:
        return False


def _mlx_missing_hint() -> str:
    if is_apple_silicon():
        return f"The mlx-lm backend is not installed. Install it:  {_MLX_INSTALL}"
    return (
        "The mlx-lm backend needs a Mac with Apple Silicon (M1 or later). On this machine use Ollama instead: "
        'set llm.backend = "ollama" (or leave it on "auto").'
    )


class MlxLM:
    """A text model run in-process with mlx-lm (Apple Silicon). Loaded on first use.

    The call sequence is the one in mlx-lm's README, checked against the 0.32 sources::

        model, tokenizer = mlx_lm.load(repo)
        prompt = tokenizer.apply_chat_template(messages, add_generation_prompt=True, enable_thinking=False)
        text = mlx_lm.generate(model, tokenizer, prompt=prompt, max_tokens=n, sampler=make_sampler(temp=t), verbose=False)

    ``enable_thinking=False`` matters: mlx-lm's tokenizer wrapper switches reasoning ON by
    default for models that support it.
    """

    def __init__(self, model: str = MLX_DEFAULT_MODEL, *, context_tokens: int = 8192):
        self.model = model
        self.name = f"mlx-lm:{model}"
        self.window = max(1024, int(context_tokens))
        # no schema-constrained decoding here: the schema travels in the prompt, so leave room for it
        self.context_tokens = input_budget(self.window, overhead=1024)
        self._model: Any = None
        self._tokenizer: Any = None
        self._load_error: str | None = None

    # -- model lifecycle --

    def _ensure_loaded(self) -> None:
        if self._model is not None:
            return
        if self._load_error is not None:
            raise BackendUnavailable(self._load_error)
        try:
            import mlx_lm
        except Exception as exc:  # ImportError, or mlx failing to initialise on unsupported hardware
            self._load_error = f"{_mlx_missing_hint()} ({type(exc).__name__}: {exc})"
            raise BackendUnavailable(self._load_error) from exc
        if _mlx_cached(self.model):
            log.info("loading %s", self.model)
        else:
            log.warning(
                "downloading the summary model %s from Hugging Face (a few GB, first use only); "
                "summaries start when it has arrived",
                self.model,
            )
        try:
            self._model, self._tokenizer = mlx_lm.load(self.model)
        except Exception as exc:
            self._model = self._tokenizer = None
            self._load_error = (
                f'Could not load the MLX model "{self.model}" ({type(exc).__name__}: {exc}). Check the name in '
                "llm.model, and that this Mac is online for the first download (a few GB), or use Ollama instead."
            )
            raise BackendUnavailable(self._load_error) from exc

    def close(self) -> None:
        """Free the model and give the memory MLX cached back to the system."""
        loaded = self._model is not None
        self._model = None
        self._tokenizer = None
        if not loaded:
            return
        gc.collect()
        try:
            import mlx.core as mx

            clear = getattr(mx, "clear_cache", None) or getattr(getattr(mx, "metal", None), "clear_cache", None)
            if clear is not None:
                clear()
        except Exception:  # freeing the cache is best effort
            log.debug("clearing the MLX cache failed", exc_info=True)

    # -- generation --

    def _chat_prompt(self, system: str, prompt: str) -> Any:
        """Token ids (or text) of the chat-formatted prompt, for whatever template the model ships."""
        tokenizer = self._tokenizer
        has_template = getattr(tokenizer, "has_chat_template", None)
        if has_template is None:
            has_template = getattr(tokenizer, "chat_template", None) is not None
        merged = f"{system}\n\n{prompt}" if system else prompt
        if not has_template:
            return merged
        with_system = [{"role": "system", "content": system}, {"role": "user", "content": prompt}]
        attempts: list[tuple[list[dict[str, str]], dict[str, Any]]] = []
        if system:
            attempts.append((with_system, {"enable_thinking": False}))
            attempts.append((with_system, {}))
        # some templates (older Gemma, Mistral) reject a system role: fold it into the user turn
        attempts.append(([{"role": "user", "content": merged}], {"enable_thinking": False}))
        attempts.append(([{"role": "user", "content": merged}], {}))
        last: Exception | None = None
        for messages, extra in attempts:
            try:
                return tokenizer.apply_chat_template(messages, add_generation_prompt=True, **extra)
            except Exception as exc:  # TypeError (unknown kwarg) or a Jinja TemplateError
                last = exc
        raise BackendError(f"{self.name}: the model's chat template could not be applied ({last})")

    def _generate(self, system: str, prompt: str, max_tokens: int, temperature: float) -> str:
        self._ensure_loaded()
        chat_prompt = self._chat_prompt(system, prompt)
        try:
            from mlx_lm import generate
        except Exception as exc:
            raise BackendUnavailable(f"{_mlx_missing_hint()} ({exc})") from exc
        kwargs: dict[str, Any] = {"max_tokens": max(16, int(max_tokens)), "verbose": False}
        try:
            from mlx_lm.sample_utils import make_sampler

            kwargs["sampler"] = make_sampler(temp=float(temperature))
        except Exception:  # very old mlx-lm: the default sampler is greedy, which is what we want anyway
            log.debug("mlx_lm.sample_utils.make_sampler unavailable; using the default sampler")
        try:
            text = generate(self._model, self._tokenizer, prompt=chat_prompt, **kwargs)
        except Exception as exc:
            raise BackendError(f"{self.name} failed while generating ({type(exc).__name__}: {exc})") from exc
        return _strip_thinking(text if isinstance(text, str) else "")

    def json(self, *, system: str, prompt: str, schema: dict[str, Any], max_tokens: int = 2048) -> dict[str, Any]:
        limit = max(64, min(int(max_tokens), _output_reserve(self.window)))
        raw = self._generate(system, f"{prompt}\n\n{schema_prompt(schema)}", limit, 0.0)
        obj = extract_json(raw)
        if obj is None:
            log.info("%s returned no JSON object (%d chars); asking once more", self.name, len(raw))
            raw = self._generate(system, _firmer(prompt, schema), limit, 0.0)
            obj = extract_json(raw)
        if obj is None:
            raise BackendError(f"{self.name} did not return JSON (got: {raw[:120]!r})")
        return _shaped(obj, schema, self.name)

    def text(self, *, system: str, prompt: str, max_tokens: int = 1024) -> str:
        limit = max(64, min(int(max_tokens), _output_reserve(self.window)))
        return self._generate(system, prompt, limit, 0.2)


def _make_mlx(settings: Settings) -> MlxLM:
    if not _mlx_installed():
        raise BackendUnavailable(_mlx_missing_hint())
    return MlxLM(_mlx_model(settings), context_tokens=settings.llm.context_tokens)


# -- Claude (explicit opt-in only) ----------------------------------------------------------


def _claude_model(settings: Settings) -> str:
    wanted = (settings.llm.model or "auto").strip()
    return CLAUDE_DEFAULT_MODEL if wanted.lower() == "auto" else wanted


class ClaudeLLM:
    """The Claude API through :class:`ClaudeClient` (structured outputs for JSON)."""

    context_tokens = CLAUDE_CONTEXT_TOKENS

    def __init__(self, client: ClaudeClient):
        self.client = client
        self.name = f"anthropic:{client.model}"

    def json(self, *, system: str, prompt: str, schema: dict[str, Any], max_tokens: int = 2048) -> dict[str, Any]:
        # Nothing has to be kept small for memory here; a low cap would only cut a long note off.
        raw = self.client.complete(system=system, prompt=prompt, schema=schema, max_tokens=max(4096, int(max_tokens)))
        obj = extract_json(raw)
        if obj is None:
            raise BackendError(f"{self.name} did not return JSON (got: {raw[:120]!r})")
        return _shaped(obj, schema, self.name)

    def text(self, *, system: str, prompt: str, max_tokens: int = 1024) -> str:
        return self.client.complete(system=system, prompt=prompt, max_tokens=max(1024, int(max_tokens))).strip()

    def close(self) -> None:
        """Nothing is held locally."""


# -- factory and status ------------------------------------------------------------------------


def _backend_name(settings: Settings) -> str:
    raw = (settings.llm.backend or "auto").strip().lower()
    return _ALIASES.get(raw, raw)


def make_llm(settings: Settings) -> LLM | None:
    """The text LLM the settings ask for, or ``None`` for extractive summaries.

    * ``extractive`` -> ``None``.
    * ``ollama`` / ``mlx-lm`` / ``anthropic`` -> that backend, or :class:`BackendUnavailable`
      saying exactly what to start, pull or install.
    * ``auto`` -> Ollama when it runs and already has a suitable model, else mlx-lm when it is
      installed on Apple Silicon, else ``None``.  Never a cloud backend.
    """
    backend = _backend_name(settings)
    if backend == "extractive":
        return None
    if backend == "ollama":
        return _make_ollama(settings, strict=True)
    if backend == "mlx-lm":
        return _make_mlx(settings)
    if backend == "anthropic":
        return ClaudeLLM(ClaudeClient(_claude_model(settings)))
    if backend == "auto":
        llm = _make_ollama(settings, strict=False)
        if llm is not None:
            return llm
        if _mlx_auto_ok(settings):
            return MlxLM(_mlx_model(settings), context_tokens=settings.llm.context_tokens)
        return None
    raise BackendUnavailable(
        f'llm.backend = "{settings.llm.backend}" is not a known backend. Use one of: {", ".join(_BACKENDS)}.'
    )


def _mlx_auto_ok(settings: Settings) -> bool:
    """mlx-lm is an ``auto`` candidate only on Apple Silicon, and not for an Ollama-style model name."""
    if not (is_apple_silicon() and _mlx_installed()):
        return False
    wanted = (settings.llm.model or "auto").strip()
    return wanted.lower() == "auto" or "/" in wanted


def llm_status(settings: Settings) -> list[BackendStatus]:
    """What ``vnote doctor`` shows for the summary LLM: every backend, what it needs, which one is in use."""
    backend = _backend_name(settings)

    _, ollama_model, ollama_detail = _ollama_probe(settings)
    ollama_ok = ollama_model is not None

    mlx_installed = _mlx_installed()
    mlx_model = _mlx_model(settings)
    if mlx_installed and is_apple_silicon():
        where = "already downloaded" if _mlx_cached(mlx_model) else "a few GB are downloaded from Hugging Face on first use"
        mlx_detail = f"{mlx_model} (in-process; {where})"
    elif mlx_installed:
        mlx_detail = f'{mlx_model} (not an Apple Silicon Mac: used only when llm.backend = "mlx-lm")'
    else:
        mlx_detail = _mlx_missing_hint()

    claude_installed = module_available("anthropic")
    if claude_installed:
        claude_detail = f'{_claude_model(settings)} (cloud; used only when llm.backend = "anthropic")'
        if backend == "anthropic" and not os.environ.get("ANTHROPIC_API_KEY"):
            claude_detail += "; ANTHROPIC_API_KEY is not set (set it, or run `ant auth login`)"
    else:
        claude_detail = "Cloud backend, never picked automatically. To use it:  pip install anthropic  and set llm.backend = \"anthropic\""

    if backend == "auto":
        selected = "ollama" if ollama_ok else ("mlx-lm" if _mlx_auto_ok(settings) else "extractive")
    elif backend in ("ollama", "mlx-lm", "anthropic"):
        available = {"ollama": ollama_ok, "mlx-lm": mlx_installed, "anthropic": claude_installed}[backend]
        selected = backend if available else ""
    else:
        selected = "extractive" if backend == "extractive" else ""

    statuses = [
        BackendStatus("ollama", ollama_ok, ollama_detail, selected == "ollama"),
        BackendStatus("mlx-lm", mlx_installed, mlx_detail, selected == "mlx-lm"),
        BackendStatus("anthropic", claude_installed, claude_detail, selected == "anthropic"),
        BackendStatus(
            "extractive", True, "built in: notes quote what was said and shown, no language model", selected == "extractive"
        ),
    ]
    return statuses
