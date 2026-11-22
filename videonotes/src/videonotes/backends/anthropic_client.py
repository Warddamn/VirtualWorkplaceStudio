"""Optional cloud backend: the Claude API through the official ``anthropic`` SDK.

videonotes is local-first.  Nothing here runs unless the user explicitly sets
``backend = "anthropic"`` for vision and/or llm in config.toml; ``auto`` never
selects a cloud backend, because frames and transcripts of a person's day are
exactly the kind of data that should not leave the laptop by default.

Credentials are resolved by the SDK itself (``ANTHROPIC_API_KEY``, or a
profile created with ``ant auth login``).
"""

from __future__ import annotations

import base64
import json
from pathlib import Path
from typing import Any

from .base import BackendError, BackendUnavailable

DEFAULT_MODEL = "claude-opus-5-5"

#: Models for which a safety-classifier decline can be retried server-side.
_FALLBACK_MODELS = ("claude-opus-5-5", "claude-opus-5", "claude-sonnet-5-5", "claude-fable-5-2", "claude-fable-5-1")
_FALLBACK_BETA = "server-side-fallback-2026-07-01"

INSTALL_HINT = "The Claude backend needs the Anthropic SDK:  pip install 'videonotes[cloud]'  (or: pip install anthropic)"
AUTH_HINT = (
    "No valid Anthropic credentials. Set the ANTHROPIC_API_KEY environment variable "
    "(or run `ant auth login`), then try again."
)

_MEDIA_TYPES = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp", ".gif": "image/gif"}


def image_block(path: Path) -> dict[str, Any]:
    """An image content block (base64) for a local file."""
    media_type = _MEDIA_TYPES.get(Path(path).suffix.lower())
    if media_type is None:
        raise BackendError(f"unsupported image type for the Claude API: {path}")
    data = base64.standard_b64encode(Path(path).read_bytes()).decode("ascii")
    return {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": data}}


class ClaudeClient:
    """Thin wrapper: one user turn in, text (or a schema-conforming object) out."""

    def __init__(self, model: str = DEFAULT_MODEL, *, client: Any = None):
        self.model = model or DEFAULT_MODEL
        if client is not None:
            self._anthropic = None
            self._client = client
            return
        try:
            import anthropic
        except ImportError as exc:
            raise BackendUnavailable(INSTALL_HINT) from exc
        self._anthropic = anthropic
        self._client = anthropic.Anthropic()

    def complete(
        self,
        *,
        system: str,
        prompt: str,
        images: list[Path] | None = None,
        schema: dict[str, Any] | None = None,
        max_tokens: int = 16000,
        effort: str | None = None,
    ) -> str:
        """Send one request and return the response text.

        With ``schema`` the response is constrained to that JSON Schema
        (structured outputs), so the returned text parses as JSON.
        """
        content: list[dict[str, Any]] = [image_block(p) for p in (images or [])]
        content.append({"type": "text", "text": prompt})
        kwargs: dict[str, Any] = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": content}],
        }
        if system:
            kwargs["system"] = system
        output_config: dict[str, Any] = {}
        if effort:
            output_config["effort"] = effort
        if schema is not None:
            output_config["format"] = {"type": "json_schema", "schema": _strict_schema(schema)}
        if output_config:
            kwargs["output_config"] = output_config

        response = self._send(kwargs)
        if response.stop_reason == "refusal":
            details = getattr(response, "stop_details", None)
            category = getattr(details, "category", None) or "unspecified"
            raise BackendError(f"Claude declined this request (category: {category}).")
        text = "".join(block.text for block in response.content if block.type == "text")
        if not text.strip():
            raise BackendError(f"Claude returned no text (stop_reason={response.stop_reason}).")
        return text

    def _send(self, kwargs: dict[str, Any]) -> Any:
        anthropic = self._anthropic
        use_fallback = self.model in _FALLBACK_MODELS
        try:
            if use_fallback:
                # A classifier decline is re-run server-side on the model Anthropic
                # recommends for that refusal category instead of failing the note.
                return self._client.beta.messages.create(betas=[_FALLBACK_BETA], fallbacks="default", **kwargs)
            return self._client.messages.create(**kwargs)
        except Exception as exc:
            if anthropic is None:
                raise
            if isinstance(exc, (anthropic.AuthenticationError, anthropic.PermissionDeniedError)):
                raise BackendUnavailable(AUTH_HINT) from exc
            if isinstance(exc, anthropic.NotFoundError):
                raise BackendUnavailable(f"Claude model not found: {self.model!r}") from exc
            if isinstance(exc, anthropic.RateLimitError):
                raise BackendError("Claude API rate limit reached; try again in a minute.") from exc
            if isinstance(exc, anthropic.APIStatusError):
                raise BackendError(f"Claude API error {exc.status_code}: {exc.message}") from exc
            if isinstance(exc, anthropic.APIConnectionError):
                raise BackendError("Could not reach the Claude API (network problem).") from exc
            if isinstance(exc, TypeError) and "api_key" in str(exc).lower():
                raise BackendUnavailable(AUTH_HINT) from exc
            raise


def _strict_schema(schema: dict[str, Any]) -> dict[str, Any]:
    """Structured outputs require ``additionalProperties: false`` and every key required."""

    def fix(node: Any) -> Any:
        if isinstance(node, dict):
            node = {k: fix(v) for k, v in node.items()}
            if node.get("type") == "object" and isinstance(node.get("properties"), dict):
                node["additionalProperties"] = False
                node["required"] = list(node["properties"].keys())
            return node
        if isinstance(node, list):
            return [fix(v) for v in node]
        return node

    return fix(json.loads(json.dumps(schema)))
