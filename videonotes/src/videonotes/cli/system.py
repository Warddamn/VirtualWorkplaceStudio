"""Setup and diagnosis: init, doctor, web."""

from __future__ import annotations

import argparse
import os
import platform
import shutil
import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass, field

from ..backends.status import BackendStatus, module_available
from ..config import default_config_text, is_apple_silicon, is_macos
from .common import Context


def register(sub: argparse._SubParsersAction) -> None:
    p = sub.add_parser("init", help="create the library folder and config, then check this Mac")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("doctor", help="check what is installed and what each feature still needs")
    p.set_defaults(func=cmd_doctor)

    p = sub.add_parser("web", help="browse notes, timeline and search in the browser (local only)")
    p.add_argument("--port", type=int, default=8765)
    p.add_argument("--no-open", action="store_true", help="do not open the browser automatically")
    p.set_defaults(func=cmd_web)


# -- doctor --------------------------------------------------------------------


@dataclass
class Check:
    name: str
    ok: bool
    detail: str = ""
    fix: str = ""  # what to do when not ok
    optional: bool = False  # a missing optional feature is a note, not a problem


@dataclass
class Report:
    sections: list[tuple[str, list[Check]]] = field(default_factory=list)

    def add(self, title: str, checks: list[Check]) -> None:
        self.sections.append((title, checks))

    @property
    def problems(self) -> list[Check]:
        return [c for _, checks in self.sections for c in checks if not c.ok and not c.optional]


def memory_gb() -> float | None:
    try:
        if sys.platform == "darwin":
            out = subprocess.run(["sysctl", "-n", "hw.memsize"], capture_output=True, text=True, timeout=5).stdout
            return int(out.strip()) / 1024**3
        return os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / 1024**3
    except (OSError, ValueError, subprocess.SubprocessError):
        return None


def check_system(ctx: Context) -> list[Check]:
    checks = [
        Check("Python", sys.version_info >= (3, 11), platform.python_version(), fix="videonotes needs Python 3.11 or newer."),
    ]
    if is_macos():
        chip = "Apple Silicon" if is_apple_silicon() else "Intel"
        checks.append(Check("macOS", True, f"{platform.mac_ver()[0]} ({chip})"))
    else:
        checks.append(
            Check(
                "Operating system", True, f"{platform.system()} — capture from the camera and Apple's on-device "
                "text recognition need macOS; processing files works here.", optional=True,
            )  # fmt: skip
        )
    ram = memory_gb()
    if ram is not None:
        checks.append(
            Check("Memory", ram >= 7.5, f"{ram:.0f} GB", fix="Under 8 GB: use small models and set vision.backend = \"none\".", optional=True)
        )
    try:
        ctx.settings.ensure_dirs()
        free = shutil.disk_usage(ctx.settings.home).free / 1024**3
        checks.append(
            Check("Library", free > 5, f"{ctx.settings.home}  ({free:.0f} GB free)", fix="Less than 5 GB free on the library disk.")
        )
    except OSError as exc:
        checks.append(Check("Library", False, str(ctx.settings.home), fix=f"Cannot create the library folder: {exc}"))
    return checks


def check_ffmpeg() -> list[Check]:
    from ..media import ffmpeg as ff

    if not ff.have_ffmpeg():
        return [Check("ffmpeg", False, "not found", fix="Install it:  brew install ffmpeg")]
    checks = [Check("ffmpeg", True, f"{ff.version()}  ({ff.ffmpeg_bin()})")]
    checks.append(
        Check("ffprobe", ff.ffprobe_bin() is not None, ff.ffprobe_bin() or "not found (falling back to ffmpeg)", optional=True)
    )
    if is_macos():
        checks.append(
            Check(
                "Camera capture (avfoundation)", ff.has_input_format("avfoundation"),
                fix="This ffmpeg cannot capture from cameras. Use the Homebrew build:  brew install ffmpeg",
            )  # fmt: skip
        )
        checks.append(
            Check(
                "Hardware video (VideoToolbox)", ff.has_encoder("h264_videotoolbox") and ff.has_hwaccel("videotoolbox"),
                fix="Hardware encode/decode unavailable; software will be used (slower, more battery).", optional=True,
            )  # fmt: skip
        )
    return checks


def _status_checks(title: str, loader: Callable[[], list[BackendStatus]]) -> list[Check]:
    try:
        statuses = loader()
    except Exception as exc:  # doctor must keep going whatever a backend probe does
        return [Check(title, False, f"could not be checked: {type(exc).__name__}: {exc}")]
    checks: list[Check] = []
    any_selected = any(s.selected for s in statuses)
    for s in statuses:
        mark = "  ← in use" if s.selected else ""
        if s.available:
            checks.append(Check(s.name, True, f"{s.detail}{mark}"))
        else:
            checks.append(Check(s.name, False, "", fix=s.detail, optional=True))
    if not any_selected:
        checks.append(Check(f"{title}: nothing usable yet", False, "", fix="Set up one of the options above.", optional=False))
    return checks


def check_backends(ctx: Context) -> list[tuple[str, list[Check]]]:
    settings = ctx.settings

    def asr() -> list[BackendStatus]:
        from ..backends.asr import asr_status

        return asr_status(settings)

    def ocr() -> list[BackendStatus]:
        from ..backends.ocr import ocr_status

        return ocr_status(settings)

    def vision() -> list[BackendStatus]:
        from ..backends.vision import vision_status

        return vision_status(settings)

    def llm() -> list[BackendStatus]:
        from ..backends.llm import llm_status

        return llm_status(settings)

    out = []
    for title, kind, loader in (
        ("Speech-to-text", "asr", asr),
        ("Reading on-screen text (OCR)", "ocr", ocr),
        ("Describing keyframes (vision model)", "vision", vision),
        ("Writing summaries (LLM)", "llm", llm),
    ):
        configured = getattr(settings, kind).backend
        if configured == "none" or (kind == "llm" and configured == "extractive"):
            out.append((title, [Check("turned off in config", True, f"{kind}.backend = \"{configured}\"")]))
            continue
        checks = _status_checks(title, loader)
        if kind in ("vision", "llm"):
            # Notes still work without these (extractive summaries, OCR-only frames).
            for c in checks:
                c.optional = True
        out.append((title, checks))
    return out


def check_camera(ctx: Context) -> list[Check]:
    checks: list[Check] = []
    if is_macos():
        try:
            from ..capture.devices import list_devices, pick_device

            devices = list_devices()
            video = pick_device(devices, "video", ctx.settings.capture.video_device)
            names = ", ".join(d.name for d in devices if d.kind == "video") or "none"
            if video:
                checks.append(Check("Camera in USB webcam mode", True, video.name))
            else:
                checks.append(
                    Check(
                        "Camera in USB webcam mode", False, f"not connected (video devices: {names})", optional=True,
                        fix="Plug the camera in with USB-C and choose Webcam on its screen, then `vnote live`.",
                    )  # fmt: skip
                )
        except Exception as exc:
            checks.append(Check("Camera in USB webcam mode", False, f"could not list devices: {exc}", optional=True))
    try:
        from ..capture.importer import find_camera_volumes

        volumes = find_camera_volumes()
        checks.append(
            Check(
                "Camera storage / SD card", bool(volumes), ", ".join(str(v) for v in volumes) or "not mounted", optional=True,
                fix="Plug the camera in and choose File Transfer (or insert the SD card), then `vnote import`.",
            )  # fmt: skip
        )
    except Exception as exc:
        checks.append(Check("Camera storage / SD card", False, f"could not be checked: {exc}", optional=True))
    checks.append(
        Check(
            "Bluetooth control (bleak)", module_available("bleak"), "installed" if module_available("bleak") else "",
            fix="For `vnote wireless` and `vnote camera …`:  pip install 'videonotes[ble]'", optional=True,
        )  # fmt: skip
    )
    return checks


def build_report(ctx: Context) -> Report:
    report = Report()
    report.add("System", check_system(ctx))
    report.add("ffmpeg", check_ffmpeg())
    for title, checks in check_backends(ctx):
        report.add(title, checks)
    report.add("Camera", check_camera(ctx))
    return report


def print_report(ctx: Context, report: Report) -> None:
    out = ctx.out
    for title, checks in report.sections:
        out.line("")
        out.heading(title)
        for c in checks:
            if c.ok:
                mark = out.style("✓", "green")
            elif c.optional:
                mark = out.style("–", "yellow")
            else:
                mark = out.style("✗", "red")
            out.line(f"  {mark} {c.name}{('  ' + out.style(c.detail, 'dim')) if c.detail else ''}")
            if not c.ok and c.fix:
                for row in c.fix.splitlines():
                    out.line(f"      {row}")
    out.line("")
    if report.problems:
        out.error(f"{len(report.problems)} thing(s) need attention before videonotes can do its job (marked ✗).")
    else:
        out.ok("Ready. Items marked – are optional extras. Try `vnote demo`.")


def cmd_doctor(ctx: Context, args: argparse.Namespace) -> int:
    report = build_report(ctx)
    print_report(ctx, report)
    return 1 if report.problems else 0


def cmd_init(ctx: Context, args: argparse.Namespace) -> int:
    settings = ctx.settings
    settings.ensure_dirs()
    if not settings.config_path.exists():
        settings.config_path.write_text(default_config_text(), encoding="utf-8")
        ctx.out.ok(f"Created {settings.config_path}")
    else:
        ctx.out.info(f"Keeping existing {settings.config_path}")
    _ = ctx.store  # creates library.db
    ctx.out.ok(f"Library at {settings.home}  (notes in {settings.vault_dir})")
    return cmd_doctor(ctx, args)


def cmd_web(ctx: Context, args: argparse.Namespace) -> int:
    from ..web.server import serve

    serve(ctx.settings, port=args.port, open_browser=not args.no_open, out=ctx.out)
    return 0
