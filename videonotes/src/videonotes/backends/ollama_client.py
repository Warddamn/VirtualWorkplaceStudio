"""Minimal client for a local Ollama server (stdlib only).

Used by both the captioning backend (vision models) and the summarisation
backend (text models), so it lives in one place.  Only the documented native
REST API is used: ``/api/version``, ``/api/tags``, ``/api/chat``,
``/api/pull``.
"""

from __future__ import annotations

import base64
import json
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from .base import BackendError, BackendUnavailable

DEFAULT_URL = "http://127.0.0.1:11434"

NOT_RUNNING_HINT = (
    "Ollama is not running at {url}. Install it from https://ollama.com (or `brew install ollama`), "
    "start it (open the Ollama app, or run `ollama serve`), then try again."
)


class OllamaClient:
    def __init__(self, url: str = DEFAULT_URL, *, timeout: float = 600.0):
        self.url = url.rstrip("/")
        self.timeout = timeout

    # -- transport ----------------------------------------------------------

    def _request(self, method: str, path: str, body: dict[str, Any] | None = None, *, timeout: float | None = None) -> Any:
        data = json.dumps(body).encode("utf-8") if body is not None else None
        req = urllib.request.Request(
            self.url + path, data=data, method=method, headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout or self.timeout) as resp:
                raw = resp.read()
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace")[:500]
            try:
                detail = json.loads(detail).get("error", detail)
            except (json.JSONDecodeError, AttributeError):
                pass
            if exc.code == 404 and "model" in str(detail).lower():
                raise BackendUnavailable(f"Ollama: {detail}. Pull it first:  ollama pull <model>") from exc
            raise BackendError(f"Ollama returned HTTP {exc.code}: {detail}") from exc
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as exc:
            raise BackendUnavailable(NOT_RUNNING_HINT.format(url=self.url) + f" ({exc})") from exc
        if not raw:
            return {}
        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            raise BackendError(f"Ollama returned a non-JSON response: {raw[:200]!r}") from exc

    # -- discovery ----------------------------------------------------------

    def is_running(self) -> bool:
        try:
            self._request("GET", "/api/version", timeout=2.0)
            return True
        except (BackendUnavailable, BackendError):
            return False

    def list_models(self) -> list[str]:
        """Names (tags) of locally available models, e.g. ``["qwen3:4b", ...]``."""
        data = self._request("GET", "/api/tags", timeout=10.0)
        return [m.get("name", "") for m in data.get("models", []) if m.get("name")]

    def has_model(self, model: str) -> bool:
        names = self.list_models()
        wanted = model if ":" in model else model + ":latest"
        return model in names or wanted in names

    def first_available(self, candidates: list[str]) -> str | None:
        """First candidate that is already pulled, or None."""
        names = set(self.list_models())
        for cand in candidates:
            if cand in names or (":" not in cand and cand + ":latest" in names):
                return cand
        return None

    # -- inference ----------------------------------------------------------

    def chat(
        self,
        model: str,
        *,
        system: str = "",
        prompt: str,
        images: list[Path] | None = None,
        schema: dict[str, Any] | None = None,
        num_ctx: int | None = None,
        max_tokens: int | None = None,
        temperature: float | None = 0.2,
        keep_alive: str | int | None = None,
        think: bool | None = False,
    ) -> str:
        """One non-streaming chat turn. Returns the assistant text.

        ``schema`` (a JSON Schema) switches on Ollama's structured outputs.
        ``think=False`` asks reasoning-capable models to answer directly;
        if the server rejects the field for a model, the call is retried
        without it.
        """
        message: dict[str, Any] = {"role": "user", "content": prompt}
        if images:
            message["images"] = [base64.b64encode(Path(p).read_bytes()).decode("ascii") for p in images]
        messages: list[dict[str, Any]] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append(message)
        options: dict[str, Any] = {}
        if num_ctx:
            options["num_ctx"] = int(num_ctx)
        if max_tokens:
            options["num_predict"] = int(max_tokens)
        if temperature is not None:
            options["temperature"] = float(temperature)
        body: dict[str, Any] = {"model": model, "messages": messages, "stream": False}
        if options:
            body["options"] = options
        if schema is not None:
            body["format"] = schema
        if keep_alive is not None:
            body["keep_alive"] = keep_alive
        if think is not None:
            body["think"] = think
        try:
            data = self._request("POST", "/api/chat", body)
        except BackendError as exc:
            if think is None or "think" not in str(exc).lower():
                raise
            body.pop("think", None)
            data = self._request("POST", "/api/chat", body)
        content = (data.get("message") or {}).get("content")
        if not isinstance(content, str):
            raise BackendError(f"Ollama returned no message content for model {model}")
        return content

    def unload(self, model: str) -> None:
        """Ask the server to drop a model from memory now (best effort)."""
        try:
            self._request("POST", "/api/chat", {"model": model, "messages": [], "keep_alive": 0}, timeout=30.0)
        except (BackendUnavailable, BackendError):
            pass
