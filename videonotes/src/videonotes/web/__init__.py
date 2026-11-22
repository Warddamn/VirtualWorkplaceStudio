"""The local web UI served by ``vnote web``.

``videonotes.web.server`` is a small standard-library HTTP server (no web
framework) that exposes the library read-only as JSON, serves keyframes and
clip media, and hosts the single-page app in ``videonotes/web/static``.
"""

from __future__ import annotations

from .server import WebServerError, make_server, serve

__all__ = ["WebServerError", "make_server", "serve"]
