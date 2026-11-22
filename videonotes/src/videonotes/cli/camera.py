"""Bluetooth control of the camera: scan, pair, record, status.

The camera API (:mod:`videonotes.dji.camera`) is asynchronous because
Bluetooth is; the command line is not.  :class:`CameraHandle` bridges the two
by running one private event loop on a background thread for the lifetime of
a connection, so the connection stays alive while the main thread is busy
(for example recording a livestream).
"""

from __future__ import annotations

import argparse
import asyncio
import dataclasses
import threading
from collections.abc import Coroutine
from typing import Any

from ..backends.status import module_available
from .common import CliError, Context

META_ADDRESS = "dji.address"
META_NAME = "dji.name"
META_MODEL = "dji.model"

BLUETOOTH_HELP = (
    "Switch the camera on and keep it awake and close to the Mac. If macOS asks whether your terminal app may "
    "use Bluetooth, allow it (System Settings → Privacy & Security → Bluetooth)."
)


def register(sub: argparse._SubParsersAction) -> None:
    p = sub.add_parser("camera", help="control the camera over Bluetooth (scan, pair, record, status)")
    actions = p.add_subparsers(dest="action", metavar="ACTION")
    p.set_defaults(func=lambda ctx, args: _usage(p))

    a = actions.add_parser("scan", help="look for DJI cameras nearby")
    a.add_argument("--seconds", type=float, default=8.0)
    a.set_defaults(func=cmd_scan)

    a = actions.add_parser("pair", help="pair with the camera (confirm on the camera's screen) and remember it")
    a.set_defaults(func=cmd_pair)

    a = actions.add_parser("record", help="start or stop recording to the camera's card")
    a.add_argument("state", choices=["start", "stop"])
    a.set_defaults(func=cmd_record)

    a = actions.add_parser("status", help="show what the camera reports (mode, recording, battery, card)")
    a.set_defaults(func=cmd_status)

    a = actions.add_parser("forget", help="forget the remembered camera")
    a.set_defaults(func=cmd_forget)


def _usage(parser: argparse.ArgumentParser) -> int:
    parser.print_help()
    return 2


# -- sync bridge -----------------------------------------------------------------


class BleRunner:
    """One event loop on a background thread; coroutines are submitted from the main thread."""

    def __init__(self) -> None:
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._loop.run_forever, name="videonotes-ble", daemon=True)
        self._thread.start()

    def call(self, coro: Coroutine[Any, Any, Any], timeout: float | None = None) -> Any:
        future = asyncio.run_coroutine_threadsafe(coro, self._loop)
        try:
            return future.result(timeout)
        except BaseException:
            future.cancel()
            raise

    def close(self) -> None:
        if self._loop.is_closed():
            return
        self._loop.call_soon_threadsafe(self._loop.stop)
        self._thread.join(timeout=5)
        if not self._loop.is_running():
            self._loop.close()


class CameraHandle:
    """Synchronous facade over a connected ``OsmoCamera``."""

    def __init__(self, runner: BleRunner, camera: Any, name: str = ""):
        self._runner = runner
        self._camera = camera
        self.name = name

    def pair(self) -> None:
        self._runner.call(self._camera.pair())

    def start_recording(self) -> None:
        self._runner.call(self._camera.start_recording())

    def stop_recording(self) -> None:
        self._runner.call(self._camera.stop_recording())

    def status(self) -> Any:
        return self._runner.call(self._camera.status())

    def start_livestream(self, **kwargs: Any) -> None:
        self._runner.call(self._camera.start_livestream(**kwargs))

    def stop_livestream(self) -> None:
        self._runner.call(self._camera.stop_livestream())

    def close(self) -> None:
        try:
            self._runner.call(self._camera.disconnect(), timeout=15)
        except Exception:  # already gone, or Bluetooth was switched off: nothing more to do
            pass
        finally:
            self._runner.close()

    def __enter__(self) -> CameraHandle:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()


def _require_bleak() -> None:
    if not module_available("bleak"):
        raise CliError(
            "Bluetooth control needs the 'bleak' package.", hint="Install it:  pip install 'videonotes[ble]'"
        )


def _friendly(exc: BaseException) -> CliError:
    """Turn a camera/Bluetooth failure into a plain message."""
    text = str(exc).strip() or type(exc).__name__
    return CliError(text, hint=BLUETOOTH_HELP)


def find_camera(ctx: Context, runner: BleRunner, *, seconds: float = 8.0, use_saved: bool = True) -> tuple[str, str, str]:
    """Return ``(address, name, model)`` of the camera to use: the remembered one, or a scan result."""
    from ..dji.camera import scan

    settings, store = ctx.settings, ctx.store
    saved = settings.dji.address or (store.get_meta(META_ADDRESS) if use_saved else None)
    if saved and use_saved:
        return saved, store.get_meta(META_NAME, "") or "", settings_model(ctx)
    ctx.out.line(f"Looking for the camera over Bluetooth ({seconds:g} s)…")
    try:
        found = runner.call(scan(timeout=seconds, name_filter=settings.dji.name_filter), timeout=seconds + 20)
    except CliError:
        raise
    except Exception as exc:
        raise _friendly(exc) from exc
    if not found:
        raise CliError("No DJI camera found over Bluetooth.", hint=BLUETOOTH_HELP)
    if len(found) > 1:
        found.sort(key=lambda c: c.rssi if c.rssi is not None else -999, reverse=True)
        ctx.out.warn(
            f"{len(found)} cameras found; using the closest one ({found[0].name}). "
            "Set dji.name_filter in config.toml to choose another."
        )
    best = found[0]
    return best.address, best.name, best.model or settings_model(ctx)


def settings_model(ctx: Context) -> str:
    configured = ctx.settings.dji.model
    if configured and configured != "auto":
        return configured
    return ctx.store.get_meta(META_MODEL, "auto") or "auto"


def connect_camera(ctx: Context, *, pair: bool = True) -> CameraHandle:
    """Find, connect to and (by default) pair with the camera. The caller must ``close()`` the handle."""
    from ..dji.camera import OsmoCamera

    _require_bleak()
    runner = BleRunner()
    try:
        address, name, model = find_camera(ctx, runner)
        camera = OsmoCamera(address, model=model)
        try:
            runner.call(camera.connect())
        except Exception:
            # A remembered address can go stale (camera reset, different Mac): scan once and retry.
            if not (ctx.settings.dji.address or ctx.store.get_meta(META_ADDRESS)):
                raise
            ctx.out.info("The remembered camera did not answer; scanning again…")
            address, name, model = find_camera(ctx, runner, use_saved=False)
            camera = OsmoCamera(address, model=model)
            runner.call(camera.connect())
        handle = CameraHandle(runner, camera, name)
        ctx.out.ok(f"Connected to {name or 'the camera'}")
        if pair:
            ctx.out.line("Pairing… if the camera shows a prompt on its screen, confirm it.")
            handle.pair()
        ctx.store.set_meta(META_ADDRESS, address)
        ctx.store.set_meta(META_NAME, name or "")
        if model and model != "auto":
            ctx.store.set_meta(META_MODEL, model)
        return handle
    except CliError:
        runner.close()
        raise
    except KeyboardInterrupt:
        runner.close()
        raise
    except Exception as exc:
        runner.close()
        raise _friendly(exc) from exc


# -- commands --------------------------------------------------------------------


def cmd_scan(ctx: Context, args: argparse.Namespace) -> int:
    from ..dji.camera import scan

    _require_bleak()
    runner = BleRunner()
    try:
        ctx.out.line(f"Scanning for {args.seconds:g} s…")
        try:
            found = runner.call(scan(timeout=args.seconds, name_filter=ctx.settings.dji.name_filter), timeout=args.seconds + 20)
        except Exception as exc:
            raise _friendly(exc) from exc
    finally:
        runner.close()
    if not found:
        raise CliError("No DJI camera found over Bluetooth.", hint=BLUETOOTH_HELP)
    rows = [[c.name or "(no name)", c.model or "?", str(c.rssi) if c.rssi is not None else "?", c.address] for c in found]
    ctx.out.table(rows, header=["NAME", "MODEL", "SIGNAL", "ADDRESS"])
    return 0


def cmd_pair(ctx: Context, args: argparse.Namespace) -> int:
    ctx.store.set_meta(META_ADDRESS, "")  # always look afresh when pairing
    with connect_camera(ctx, pair=True) as camera:
        ctx.out.ok(f"Paired with {camera.name or 'the camera'}. It will be used automatically from now on.")
    return 0


def cmd_record(ctx: Context, args: argparse.Namespace) -> int:
    with connect_camera(ctx) as camera:
        try:
            if args.state == "start":
                camera.start_recording()
                ctx.out.ok("Recording started.")
            else:
                camera.stop_recording()
                ctx.out.ok("Recording stopped.")
        except Exception as exc:
            raise _friendly(exc) from exc
    return 0


def cmd_status(ctx: Context, args: argparse.Namespace) -> int:
    with connect_camera(ctx) as camera:
        try:
            status = camera.status()
        except Exception as exc:
            raise _friendly(exc) from exc
    fields = dataclasses.asdict(status) if dataclasses.is_dataclass(status) else dict(vars(status))
    rows = [[key.replace("_", " "), str(value)] for key, value in fields.items() if value is not None and key != "raw"]
    ctx.out.table(rows)
    return 0


def cmd_forget(ctx: Context, args: argparse.Namespace) -> int:
    for key in (META_ADDRESS, META_NAME, META_MODEL):
        ctx.store.set_meta(key, "")
    ctx.out.ok("Forgot the remembered camera.")
    return 0
