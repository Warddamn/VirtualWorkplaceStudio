"""Availability reporting shared by every backend family (used by ``vnote doctor``)."""

from __future__ import annotations

import importlib.util
from dataclasses import dataclass


@dataclass
class BackendStatus:
    name: str  # backend id as written in config.toml, e.g. "mlx-whisper"
    available: bool
    detail: str  # resolved model when available; otherwise exactly what to install / start
    selected: bool = False  # True for the backend the current settings resolve to


def module_available(module: str) -> bool:
    """True if ``module`` can be imported, without importing it (cheap, no side effects)."""
    try:
        return importlib.util.find_spec(module) is not None
    except (ImportError, ValueError, AttributeError):
        return False
