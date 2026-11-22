"""Shared plumbing for the ``vnote`` command line: context, output, error handling."""

from __future__ import annotations

import argparse
import logging
import os
import shutil
import subprocess
import sys
import textwrap
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from ..config import Settings, load_settings, parse_set_overrides
from ..store import Store

EXIT_OK = 0
EXIT_ERROR = 1
EXIT_USAGE = 2
EXIT_INTERRUPTED = 130


class CliError(Exception):
    """A problem to show to the user as a plain message (no traceback)."""

    def __init__(self, message: str, *, hint: str = "", code: int = EXIT_ERROR):
        super().__init__(message)
        self.hint = hint
        self.code = code


# -- output --------------------------------------------------------------------


def _use_colour(stream: Any) -> bool:
    if os.environ.get("NO_COLOR"):
        return False
    return bool(getattr(stream, "isatty", lambda: False)())


class Out:
    """Tiny terminal writer: colours when attached to a terminal, plain otherwise."""

    _CODES = {"bold": "1", "dim": "2", "red": "31", "green": "32", "yellow": "33", "blue": "34", "cyan": "36"}

    def __init__(self, stream: Any = None, err: Any = None):
        self.stream = stream or sys.stdout
        self.err = err or sys.stderr
        self.colour = _use_colour(self.stream)

    def style(self, text: str, *styles: str) -> str:
        if not self.colour or not styles:
            return text
        codes = ";".join(self._CODES[s] for s in styles if s in self._CODES)
        return f"\033[{codes}m{text}\033[0m" if codes else text

    def line(self, text: str = "") -> None:
        print(text, file=self.stream)

    def heading(self, text: str) -> None:
        print(self.style(text, "bold"), file=self.stream)

    def ok(self, text: str) -> None:
        print(f"{self.style('✓', 'green')} {text}", file=self.stream)

    def warn(self, text: str) -> None:
        print(f"{self.style('!', 'yellow')} {text}", file=self.err)

    def error(self, text: str) -> None:
        print(f"{self.style('✗', 'red')} {text}", file=self.err)

    def info(self, text: str) -> None:
        print(self.style(text, "dim"), file=self.stream)

    def para(self, text: str, indent: int = 0) -> None:
        width = max(40, min(100, shutil.get_terminal_size((100, 24)).columns) - indent)
        for block in text.split("\n"):
            wrapped = textwrap.wrap(block, width=width) or [""]
            for row in wrapped:
                print(" " * indent + row, file=self.stream)

    def table(self, rows: list[list[str]], header: list[str] | None = None) -> None:
        """Left-aligned columns; the last column is not padded."""
        data = ([header] if header else []) + rows
        if not data:
            return
        widths = [max(len(str(r[i])) for r in data) for i in range(len(data[0]))]
        for n, row in enumerate(data):
            cells = [str(c).ljust(widths[i]) for i, c in enumerate(row[:-1])] + [str(row[-1])]
            text = "  ".join(cells)
            print(self.style(text, "bold") if header and n == 0 else text, file=self.stream)


# -- context -------------------------------------------------------------------


@dataclass
class Context:
    """Everything a command needs; the library is opened on first use."""

    settings: Settings
    out: Out = field(default_factory=Out)
    verbose: int = 0
    _store: Store | None = None

    @property
    def store(self) -> Store:
        if self._store is None:
            self.settings.ensure_dirs()
            self._store = Store(self.settings.db_path)
        return self._store

    def close(self) -> None:
        if self._store is not None:
            self._store.close()
            self._store = None

    def require_session(self, ref: str):
        """Resolve 'latest', a full id or a unique id prefix; explain when it does not resolve."""
        session = self.store.find_session(ref)
        if session is None:
            if not self.store.list_sessions(limit=1):
                raise CliError(
                    "The library is empty.", hint="Try `vnote demo`, or add footage with `vnote import` / `vnote add FILE`."
                )
            raise CliError(
                f"No session matches {ref!r} (or more than one does).", hint="Run `vnote sessions` to list them."
            )
        return session


def make_context(args: argparse.Namespace) -> Context:
    out = Out()
    try:
        overrides = parse_set_overrides(getattr(args, "set", None) or [])
    except ValueError as exc:
        raise CliError(str(exc), code=EXIT_USAGE) from exc
    settings, warnings = load_settings(getattr(args, "home", None), overrides)
    for warning in warnings:
        out.warn(warning)
    verbose = int(getattr(args, "verbose", 0) or 0)
    logging.basicConfig(
        level=logging.DEBUG if verbose >= 2 else logging.INFO if verbose == 1 else logging.WARNING,
        format="%(levelname)s %(name)s: %(message)s",
    )
    return Context(settings=settings, out=out, verbose=verbose)


# -- keeping the Mac awake -----------------------------------------------------


def keep_awake(out: Out | None = None) -> None:
    """Stop macOS from idle-sleeping while this process runs (long recordings and imports).

    Uses the system ``caffeinate`` tool bound to our process id, so it ends by
    itself when the command does.  Does nothing on other systems.  Closing the
    laptop lid still sleeps the Mac.
    """
    if sys.platform != "darwin":
        return
    tool = shutil.which("caffeinate")
    if not tool:
        return
    try:
        subprocess.Popen(
            [tool, "-i", "-w", str(os.getpid())],
            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )  # fmt: skip
    except OSError:
        if out is not None:
            out.info("(could not keep the Mac awake; avoid letting it sleep during this run)")


# -- pipeline progress ---------------------------------------------------------

_STAGE_LABELS = {
    "probe": "Reading clips",
    "extract": "Extracting audio and keyframes",
    "transcribe": "Transcribing speech",
    "ocr": "Reading on-screen text",
    "caption": "Describing keyframes",
    "segment": "Splitting into moments",
    "summarize": "Writing the summary",
    "render": "Writing the note",
    "day": "Updating the day note",
}


def progress_printer(out: Out) -> Callable[..., None]:
    """A Pipeline progress callback that prints one line per stage, with clip counts."""
    state = {"stage": None}
    live = out.colour  # only redraw in place on a real terminal

    def on_event(event: str, **info: Any) -> None:
        if event == "stage_start":
            state["stage"] = info["stage"]
            if not live:
                out.line(f"  {_STAGE_LABELS.get(info['stage'], info['stage'])} ({info['total']} clip(s))")
        elif event == "clip_stage":
            label = _STAGE_LABELS.get(info["stage"], info["stage"])
            status = info.get("status", "")
            note = "" if status == "done" else f" [{status}]"
            if live:
                end = "\n" if info["index"] == info["total"] else "\r"
                print(f"\033[2K  {label}  {info['index']}/{info['total']}{note}", end=end, file=out.stream, flush=True)
            elif status != "done":
                out.line(f"    clip {info['clip_id']}: {status}")
        elif event == "session_stage":
            out.line(f"  {_STAGE_LABELS.get(info['stage'], info['stage'])}")

    return on_event


# -- running a command ---------------------------------------------------------


def run_command(func: Callable[[Context, argparse.Namespace], int | None], args: argparse.Namespace) -> int:
    """Run one command, turning known failures into plain messages and exit codes."""
    from ..backends.base import BackendError, BackendUnavailable
    from ..media.ffmpeg import FFmpegError

    out = Out()
    ctx: Context | None = None
    try:
        ctx = make_context(args)
        out = ctx.out
        return int(func(ctx, args) or EXIT_OK)
    except CliError as exc:
        out.error(str(exc))
        if exc.hint:
            out.line(f"  {exc.hint}")
        return exc.code
    except KeyboardInterrupt:
        out.line("")
        out.warn("Interrupted. Work finished so far is saved; run the same command again to continue.")
        return EXIT_INTERRUPTED
    except BackendUnavailable as exc:
        out.error(str(exc))
        out.line("  Run `vnote doctor` to see what is installed and what to set up.")
        return EXIT_ERROR
    except (BackendError, FFmpegError) as exc:
        out.error(str(exc))
        return EXIT_ERROR
    except BrokenPipeError:
        return EXIT_OK  # e.g. `vnote search … | head`
    except Exception as exc:
        if type(exc).__name__ == "NoteRenderError":  # its message already says what to do
            out.error(str(exc))
            return EXIT_ERROR
        if ctx is not None and ctx.verbose:
            raise
        out.error(f"Unexpected error: {type(exc).__name__}: {exc}")
        out.line("  Run the command again with -v to see the details.")
        return EXIT_ERROR
    finally:
        if ctx is not None:
            ctx.close()
