"""Getting a JSON object out of a language model, leniently.

Local models asked for JSON often wrap it in prose or code fences, leave a
trailing comma, or get cut off.  ``extract_json`` recovers the object when it
reasonably can; ``coerce_to_schema`` then forces the result into the shape the
caller asked for so downstream code never has to defend against a missing key
or a string where a list was expected.
"""

from __future__ import annotations

import json
import re
from typing import Any

_FENCE = re.compile(r"```(?:json|JSON)?\s*(.*?)```", re.S)
_THINK = re.compile(r"<think>.*?</think>", re.S | re.I)
_TRAILING_COMMA = re.compile(r",\s*([}\]])")


def _balanced_object(text: str) -> str | None:
    """Return the first top-level ``{...}`` in text, closing it if it was cut off."""
    start = text.find("{")
    if start < 0:
        return None
    stack: list[str] = []
    in_str = False
    escape = False
    for i in range(start, len(text)):
        ch = text[i]
        if in_str:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch in "{[":
            stack.append("}" if ch == "{" else "]")
        elif ch in "}]":
            if stack and stack[-1] == ch:
                stack.pop()
                if not stack:
                    return text[start : i + 1]
    # Truncated output: close what is open so we keep everything that did arrive.
    body = text[start:]
    if in_str:
        body += '"'
    body = re.sub(r"[,:]\s*$", "", body.rstrip())
    return body + "".join(reversed(stack))


def extract_json(text: str) -> dict[str, Any] | None:
    """Best-effort parse of a JSON object from model output. Returns None if hopeless."""
    if not text:
        return None
    text = _THINK.sub("", text).strip()
    candidates = [text]
    candidates += [m.group(1).strip() for m in _FENCE.finditer(text)]
    obj = _balanced_object(text)
    if obj:
        candidates.append(obj)
    for cand in candidates:
        for attempt in (cand, _TRAILING_COMMA.sub(r"\1", cand)):
            try:
                value = json.loads(attempt)
            except (json.JSONDecodeError, ValueError):
                continue
            if isinstance(value, dict):
                return value
    return None


def coerce_to_schema(value: Any, schema: dict[str, Any]) -> Any:
    """Force ``value`` into the shape of a (simple) JSON Schema.

    Supports the subset videonotes uses: object/array/string/number/integer/
    boolean, ``properties``, ``items`` and ``enum``.  Missing keys get an empty
    value of the right type; unknown keys are dropped.
    """
    kind = schema.get("type")
    if kind == "object":
        src = value if isinstance(value, dict) else {}
        return {key: coerce_to_schema(src.get(key), sub) for key, sub in (schema.get("properties") or {}).items()}
    if kind == "array":
        items = schema.get("items") or {}
        if value is None:
            return []
        if not isinstance(value, list):
            value = [value]
        out = [coerce_to_schema(v, items) for v in value if v is not None]
        if items.get("type") == "string":
            out = [v for v in out if v]
        return out
    if kind == "string":
        if value is None:
            text = ""
        elif isinstance(value, str):
            text = value.strip()
        elif isinstance(value, (list, tuple)):
            text = ", ".join(str(v) for v in value)
        elif isinstance(value, dict):
            text = json.dumps(value, ensure_ascii=False)
        else:
            text = str(value)
        enum = schema.get("enum")
        if enum and text not in enum:
            return enum[0]
        return text
    if kind in ("number", "integer"):
        try:
            num = float(value)
        except (TypeError, ValueError):
            num = 0.0
        return int(num) if kind == "integer" else num
    if kind == "boolean":
        if isinstance(value, str):
            return value.strip().lower() in ("true", "yes", "1")
        return bool(value)
    return value


def schema_prompt(schema: dict[str, Any]) -> str:
    """A compact, model-friendly description of the JSON object to return."""
    return (
        "Reply with ONE JSON object and nothing else (no markdown fences, no commentary). "
        "It must match this JSON Schema:\n" + json.dumps(schema, ensure_ascii=False)
    )
