"""A tiny in-process stand-in for the Ollama HTTP API, for tests."""

from __future__ import annotations

import json
import threading
from collections.abc import Callable
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any


class FakeOllama:
    """Start with ``with FakeOllama(reply=...) as srv:`` and point clients at ``srv.url``.

    ``reply`` is either a string returned for every chat, or a callable
    ``(request_body: dict) -> str``.  Every request body is kept in ``calls``.
    """

    def __init__(self, reply: str | Callable[[dict[str, Any]], str] = "ok", models: list[str] | None = None):
        self.reply = reply
        self.models = models if models is not None else ["qwen3:4b", "qwen2.5vl:3b"]
        self.calls: list[dict[str, Any]] = []
        outer = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args: Any) -> None:  # silence
                pass

            def _send(self, code: int, payload: dict[str, Any]) -> None:
                raw = json.dumps(payload).encode()
                self.send_response(code)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(raw)))
                self.end_headers()
                self.wfile.write(raw)

            def do_GET(self) -> None:
                if self.path == "/api/version":
                    self._send(200, {"version": "0.0-fake"})
                elif self.path == "/api/tags":
                    self._send(200, {"models": [{"name": m} for m in outer.models]})
                else:
                    self._send(404, {"error": "not found"})

            def do_POST(self) -> None:
                body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", "0"))) or b"{}")
                outer.calls.append({"path": self.path, **body})
                if self.path != "/api/chat":
                    self._send(404, {"error": "not found"})
                    return
                model = body.get("model", "")
                if model not in outer.models and model + ":latest" not in outer.models:
                    self._send(404, {"error": f'model "{model}" not found, try pulling it first'})
                    return
                if not body.get("messages"):
                    self._send(200, {"done": True})
                    return
                text = outer.reply(body) if callable(outer.reply) else outer.reply
                self._send(200, {"model": model, "message": {"role": "assistant", "content": text}, "done": True})

        self._server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.url = f"http://127.0.0.1:{self._server.server_address[1]}"
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)

    def __enter__(self) -> FakeOllama:
        self._thread.start()
        return self

    def __exit__(self, *exc: object) -> None:
        self._server.shutdown()
        self._server.server_close()
