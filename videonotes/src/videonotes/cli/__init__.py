"""``vnote`` — the videonotes command line.

Commands are grouped in modules, each exposing ``register(subparsers)``:

* :mod:`.library`  notes and library (demo, add, process, sessions, show, day, search, ask, delete, config)
* :mod:`.capture`  getting footage in (devices, live, wireless, import)
* :mod:`.camera`   Bluetooth control of the camera (scan, pair, record, status)
* :mod:`.system`   setup and diagnosis (init, doctor, web)
"""

from __future__ import annotations

import argparse
import importlib
import sys

from .. import __version__
from .common import EXIT_USAGE, run_command

_MODULES = ("system", "capture", "camera", "library")

_EPILOG = """\
typical use:
  vnote init                 set up ~/VideoNotes and check this Mac
  vnote demo                 try the whole pipeline on a generated sample clip
  vnote import               pull new recordings off the camera / SD card and write notes
  vnote live                 take notes live from the camera in USB webcam mode
  vnote wireless             take notes live over Wi-Fi (camera set up over Bluetooth)
  vnote day                  today's digest      vnote ask "where did I park?"
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="vnote",
        description="Video note-taking for a worn action camera: local speech-to-text, keyframes, OCR and summaries.",
        epilog=_EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--version", action="version", version=f"videonotes {__version__}")
    parser.add_argument("--home", metavar="DIR", help="library folder (default ~/VideoNotes, or $VIDEONOTES_HOME)")
    parser.add_argument(
        "--set", action="append", metavar="SECTION.KEY=VALUE", default=[],
        help="override a config.toml setting for this run (repeatable), e.g. --set vision.backend=none",
    )  # fmt: skip
    parser.add_argument("-v", "--verbose", action="count", default=0, help="more detail (-vv for debug logs)")
    sub = parser.add_subparsers(dest="command", metavar="COMMAND")
    for name in _MODULES:
        module = importlib.import_module(f"{__name__}.{name}")
        module.register(sub)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    func = getattr(args, "func", None)
    if func is None:
        parser.print_help()
        return EXIT_USAGE
    return run_command(func, args)


if __name__ == "__main__":
    sys.exit(main())
