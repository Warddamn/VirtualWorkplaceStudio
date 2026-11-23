"""Getting footage in: devices, live (USB webcam), wireless (Wi-Fi/RTMP), import (card or folder)."""

from __future__ import annotations

import argparse
import getpass
import os
import shutil
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

from ..config import DJI_DEVICE_HINTS, is_macos
from ..models import Clip, Session
from ..timeutil import fmt_clock, fmt_duration, new_session_id, now_ts
from .common import CliError, Context, keep_awake, progress_printer
from .library import print_note, process_sessions, report_session, report_unavailable

ENV_WIFI_PASSWORD = "VIDEONOTES_WIFI_PASSWORD"

WEBCAM_HELP = (
    "Plug the camera into the Mac with a USB-C data cable, switch it on, and choose the Webcam option "
    "on the camera's screen. Then run `vnote devices` to check it shows up."
)


def register(sub: argparse._SubParsersAction) -> None:
    p = sub.add_parser("devices", help="list cameras and microphones this Mac can capture from")
    p.set_defaults(func=cmd_devices)

    p = sub.add_parser("live", help="take notes live from the camera in USB webcam mode (Ctrl-C to finish)")
    p.add_argument(
        "--device", help="video device name or index (default: the DJI camera; 'mac' = this Mac's own camera)"
    )
    p.add_argument("--audio", help="audio device name or index, 'default' (Mac microphone) or 'none'")
    p.add_argument("--minutes", type=float, default=0, help="stop by itself after this many minutes")
    p.add_argument("--quiet", action="store_true", help="do not print speech and on-screen text as it is recognised")
    p.set_defaults(func=cmd_live)

    p = sub.add_parser(
        "wireless", help="take notes live over Wi-Fi: the camera streams to this Mac (set up over Bluetooth)"
    )
    p.add_argument("--ssid", help="Wi-Fi network the camera should join (default: the one this Mac is on)")
    p.add_argument("--password", help=f"Wi-Fi password (or set ${ENV_WIFI_PASSWORD}; asked for otherwise)")
    p.add_argument(
        "--manual", action="store_true",
        help="do not use Bluetooth: just listen, and start the RTMP livestream yourself from the DJI Mimo app",
    )  # fmt: skip
    p.add_argument("--minutes", type=float, default=0, help="stop by itself after this many minutes")
    p.add_argument("--quiet", action="store_true", help="do not print speech and on-screen text as it is recognised")
    p.set_defaults(func=cmd_wireless)

    p = sub.add_parser("import", help="import new recordings from the camera / SD card (or a folder) and write notes")
    p.add_argument("path", nargs="?", help="card, folder or file to import from (default: look for a mounted camera card)")
    p.add_argument("--dry-run", action="store_true", help="only show what would be imported")
    p.add_argument("--no-process", action="store_true", help="only import; run `vnote process` later")
    p.add_argument("--since", help="only recordings from this day on (YYYY-MM-DD, today, yesterday)")
    p.set_defaults(func=cmd_import)


# -- devices -------------------------------------------------------------------


def cmd_devices(ctx: Context, args: argparse.Namespace) -> int:
    from ..capture.devices import list_devices

    if not is_macos():
        raise CliError("Capturing from a camera needs macOS.", hint="On this system use `vnote add FILE` or `vnote import FOLDER`.")
    devices = list_devices()
    if not devices:
        raise CliError(
            "No capture devices found.",
            hint="If the list is empty even for the built-in camera, allow Camera and Microphone access for your "
            "terminal app in System Settings → Privacy & Security, then try again.",
        )
    out = ctx.out
    for kind, title in (("video", "Video"), ("audio", "Audio")):
        out.heading(title)
        for d in devices:
            if d.kind != kind:
                continue
            is_dji = any(h in d.name.lower() for h in DJI_DEVICE_HINTS)
            out.line(f"  [{d.index}] {d.name}{out.style('   ← camera', 'green') if is_dji else ''}")
    if not any(any(h in d.name.lower() for h in DJI_DEVICE_HINTS) for d in devices if d.kind == "video"):
        out.line("")
        out.warn("The DJI camera is not among the video devices.")
        out.para(WEBCAM_HELP, indent=2)
    return 0


# -- the live loop (shared by `live` and `wireless`) -----------------------------


def _new_live_session(ctx: Context, kind: str, source: str) -> tuple[Session, Path]:
    started = now_ts()
    session = Session(id=new_session_id(started), kind=kind, started_ts=started, source=source, status="open")
    ctx.store.create_session(session)
    out_dir = ctx.settings.media_dir / session.id
    out_dir.mkdir(parents=True, exist_ok=True)
    return session, out_dir


def run_live(
    ctx: Context,
    session: Session,
    recorder: Any,
    *,
    quiet: bool = False,
    max_minutes: float = 0,
    waiting_message: str = "",
    on_stop: Callable[[], None] | None = None,
) -> int:
    """Record until Ctrl-C (or the source ends), processing each finished segment as it arrives."""
    from ..capture.importer import clip_fingerprint
    from ..pipeline import Pipeline

    out = ctx.out
    settings, store = ctx.settings, ctx.store
    keep_awake(out)
    from ..power import drain_report, power_state, should_defer_heavy_work

    power_start = power_state()
    if power_start is not None and power_start.percent is not None:
        out.info(f"Power: {power_start.describe()}.")
        if should_defer_heavy_work(settings.power.on_battery, power_start):
            out.info("  On battery, describing frames and the written summary wait until you plug in.")
    pipeline = Pipeline(settings, store)
    clips = 0
    recorded = 0.0
    started = time.monotonic()

    def handle(segment: Any) -> None:
        nonlocal clips, recorded
        clip = store.add_clip(
            Clip(
                session_id=session.id,
                path=settings.rel(segment.path),
                fingerprint=clip_fingerprint(segment.path),
                start_ts=segment.start_ts,
                duration=segment.duration,
            )
        )
        clips += 1
        recorded += segment.duration
        statuses = pipeline.process_clip_light(clip.id)
        if quiet:
            return
        for u in store.list_utterances(clip_id=clip.id):
            out.line(f"{out.style(fmt_clock(u.ts0, '%H:%M:%S'), 'cyan')}  {u.text}")
        seen: set[str] = set()
        for kf in store.list_keyframes(clip_id=clip.id):
            text = " / ".join((kf.ocr_text or "").split("\n"))[:160]
            if text and text not in seen:
                seen.add(text)
                out.line(f"{out.style(fmt_clock(kf.ts, '%H:%M:%S'), 'cyan')}  {out.style('seen:', 'dim')} {text}")
        failed = [stage for stage, status in statuses.items() if status == "error"]
        if failed:
            out.warn(f"segment {clips}: {', '.join(failed)} failed (will be retried when the session is finished)")

    interrupted = False
    try:
        if not recorder.running:
            recorder.start()
        waited_notice = False
        while True:
            for segment in recorder.poll():
                handle(segment)
            if not recorder.running:
                reason = recorder.last_error().strip()
                out.warn("The recording stopped by itself." + (f"\n  {reason}" if reason else ""))
                break
            elapsed = time.monotonic() - started
            if max_minutes and elapsed >= max_minutes * 60:
                out.line(f"Reached {max_minutes:g} minute(s).")
                break
            if waiting_message and not waited_notice and clips == 0 and elapsed > 20:
                out.info(waiting_message)
                waited_notice = True
            time.sleep(1.0)
    except KeyboardInterrupt:
        interrupted = True
        out.line("")
    finally:
        out.line("Finishing the recording…")
        try:
            for segment in recorder.stop():
                handle(segment)
        finally:
            if on_stop is not None:
                try:
                    on_stop()
                except Exception as exc:  # the footage is safe; do not lose the notes over cleanup
                    out.warn(f"Could not stop the camera cleanly: {exc}")

    if clips == 0:
        pipeline.close()
        store.delete_session(session.id)
        shutil.rmtree(settings.media_dir / session.id, ignore_errors=True)
        reason = recorder.last_error().strip()
        raise CliError("Nothing was recorded." if interrupted else "No video arrived.", hint=reason or WEBCAM_HELP)

    out.line(f"Recorded {fmt_duration(recorded)} in {clips} segment(s). Writing the notes…")
    pipeline.progress = progress_printer(out)
    try:
        result = pipeline.finalize_session(session.id)
    finally:
        pipeline.close()
    report_unavailable(ctx, pipeline)
    drain = drain_report(power_start, power_state(), time.monotonic() - started)
    if drain:
        out.info(drain)
    if not settings.capture.keep_segments:
        shutil.rmtree(settings.media_dir / session.id, ignore_errors=True)
    report_session(ctx, result)
    out.line("")
    print_note(ctx, store.get_session(session.id) or result)
    return 0


# -- live over USB -----------------------------------------------------------------


def cmd_live(ctx: Context, args: argparse.Namespace) -> int:
    from ..capture.devices import list_devices, pick_device
    from ..capture.live import SegmentRecorder, webcam_command

    if not is_macos():
        raise CliError("Live capture needs macOS.", hint="On this system use `vnote add FILE` or `vnote import FOLDER`.")
    settings = ctx.settings
    devices = list_devices()
    video = pick_device(devices, "video", args.device or settings.capture.video_device)
    if video is None:
        names = ", ".join(d.name for d in devices if d.kind == "video") or "none"
        raise CliError(
            f"The camera was not found among the video devices ({names}).",
            hint=WEBCAM_HELP + "\n  To try it with this Mac's own camera instead:  vnote live --device mac",
        )
    wanted_audio = args.audio or settings.capture.audio_device
    is_dji = any(h in video.name.lower() for h in DJI_DEVICE_HINTS)
    if not is_dji and wanted_audio.strip().lower() in ("", "auto"):
        wanted_audio = "default"  # not the DJI camera: its USB microphone is not there to look for
    audio = pick_device(devices, "audio", wanted_audio)
    out = ctx.out
    out.ok(f"Camera: {video.name}")
    if audio is not None:
        out.ok(f"Microphone: {audio.name}")
    else:
        out.warn("No microphone: recording video only, so the notes will have no speech.")
    session, out_dir = _new_live_session(ctx, "live", f"{video.name} (USB webcam)" if is_dji else video.name)
    recorder = SegmentRecorder(
        webcam_command(settings, video, audio, out_dir), out_dir, segment_seconds=settings.capture.segment_seconds
    )
    out.line(
        f"Recording. Notes appear every {settings.capture.segment_seconds} s; press Ctrl-C to finish and write the summary."
    )
    return run_live(ctx, session, recorder, quiet=args.quiet, max_minutes=args.minutes)


# -- live over Wi-Fi ---------------------------------------------------------------


def cmd_wireless(ctx: Context, args: argparse.Namespace) -> int:
    from ..capture.live import SegmentRecorder, rtmp_listen_command
    from ..capture.network import current_wifi_ssid, lan_ip, port_in_use, rtmp_url

    settings = ctx.settings
    out = ctx.out
    port = settings.capture.rtmp_port
    if port_in_use(port):
        raise CliError(
            f"Port {port} is already in use on this Mac.",
            hint="Another `vnote wireless` (or another streaming server) is running. Stop it, or pick a different "
            "port with --set capture.rtmp_port=1936.",
        )
    if lan_ip() is None:
        raise CliError("This Mac is not connected to a network.", hint="Join the Wi-Fi the camera should use, then try again.")
    url = rtmp_url(settings)

    session, out_dir = _new_live_session(ctx, "wireless", "Wi-Fi livestream (RTMP)")
    recorder = SegmentRecorder(
        rtmp_listen_command(settings, out_dir), out_dir, segment_seconds=settings.capture.segment_seconds
    )
    recorder.start()  # listen before the camera is told to connect
    time.sleep(1.0)
    if not recorder.running:
        reason = recorder.last_error().strip()
        ctx.store.delete_session(session.id)
        shutil.rmtree(out_dir, ignore_errors=True)
        raise CliError("Could not start listening for the camera's stream.", hint=reason)
    out.ok(f"Listening for the camera at {url}")

    on_stop: Callable[[], None] | None = None
    if args.manual:
        out.line("")
        out.para(
            "Start the livestream from the DJI Mimo app: connect to the camera, choose Live Streaming → RTMP, "
            "pick this Wi-Fi network and enter the address above as the stream URL. If macOS asks whether to allow "
            "incoming connections, choose Allow."
        )
    else:
        try:
            on_stop = _start_camera_stream(ctx, args, url, current_wifi_ssid)
        except BaseException:
            recorder.stop()
            ctx.store.delete_session(session.id)
            shutil.rmtree(out_dir, ignore_errors=True)
            raise
    out.line("Press Ctrl-C to finish and write the summary.")
    return run_live(
        ctx,
        session,
        recorder,
        quiet=args.quiet,
        max_minutes=args.minutes,
        on_stop=on_stop,
        waiting_message=(
            "Still waiting for video from the camera. If macOS showed a dialog about incoming network connections "
            "or local network access, allow it. The camera and this Mac must be on the same Wi-Fi network."
        ),
    )


def _start_camera_stream(
    ctx: Context, args: argparse.Namespace, url: str, current_wifi_ssid: Callable[[], str | None]
) -> Callable[[], None]:
    """Tell the camera over Bluetooth to join Wi-Fi and stream to ``url``. Returns the stop function."""
    from .camera import connect_camera

    settings = ctx.settings
    out = ctx.out
    ssid = args.ssid or settings.dji.wifi_ssid or current_wifi_ssid()
    if not ssid:
        raise CliError(
            "Which Wi-Fi network should the camera join?",
            hint="Pass it with --ssid \"Network name\" (macOS hides the current network's name from command-line tools).",
        )
    password = args.password or os.environ.get(ENV_WIFI_PASSWORD)
    if password is None:
        password = getpass.getpass(f"Password for Wi-Fi network {ssid!r} (sent to the camera only, not stored): ")
    camera = connect_camera(ctx)
    out.line(f"Asking the camera to join {ssid!r} and start streaming…")
    try:
        camera.start_livestream(
            ssid=ssid,
            password=password,
            rtmp_url=url,
            resolution=settings.dji.stream_resolution,
            bitrate_kbps=settings.dji.stream_bitrate_kbps,
            fps=settings.dji.stream_fps,
        )
    except BaseException:
        camera.close()
        raise
    # The camera gives no "stream connected" signal over Bluetooth: video arriving here is the proof.
    out.ok("The camera accepted the request. Waiting for its video to arrive…")

    def stop() -> None:
        try:
            camera.stop_livestream()
        finally:
            camera.close()

    return stop


# -- import --------------------------------------------------------------------------


def cmd_import(ctx: Context, args: argparse.Namespace) -> int:
    from ..capture import importer
    from ..timeutil import day_bounds, parse_day

    out = ctx.out
    settings, store = ctx.settings, ctx.store
    since_ts = None
    if args.since:
        try:
            since_ts = day_bounds(parse_day(args.since))[0]
        except ValueError as exc:
            raise CliError(f"Not a date: {args.since!r} (use YYYY-MM-DD, today or yesterday)") from exc

    if args.path:
        root = Path(args.path).expanduser()
        if root.is_file():
            session = importer.import_file(settings, store, root)
            out.ok(f"Added {root.name} as session {session.id}")
            if not args.no_process:
                process_sessions(ctx, [session])
            return 0
        if not root.is_dir():
            raise CliError(f"No such file or folder: {root}")
        roots = [root]
    else:
        roots = importer.find_camera_volumes()
        if not roots:
            raise CliError(
                "No camera card is mounted.",
                hint="Plug the camera in with USB-C and choose the file transfer option on its screen (or put the SD "
                "card in a reader). You can also name a folder: `vnote import /path/to/folder`.",
            )

    new_sessions: list[Session] = []
    for root in roots:
        clips = importer.scan_card(root)
        if since_ts is not None:
            clips = [c for c in clips if c.start_ts >= since_ts]
        fresh = [c for c in clips if store.clip_by_fingerprint(importer.clip_fingerprint(c.proxy or c.original)) is None
                 and store.clip_by_fingerprint(importer.clip_fingerprint(c.original)) is None]  # fmt: skip
        out.heading(str(root))
        out.line(f"  {len(clips)} recording(s) found, {len(fresh)} new")
        if not fresh:
            continue
        groups = importer.group_into_sessions(fresh, settings.imports.session_gap_seconds)
        for group in groups:
            size = sum(c.size for c in group) / 1024**3
            first, last = group[0], group[-1]
            out.line(
                f"  • {fmt_clock(first.start_ts, '%a %d %b %H:%M')}–{fmt_clock(last.start_ts)}  "
                f"{len(group)} file(s), {size:.1f} GB on the card"
            )
        if args.dry_run:
            continue
        mode = settings.imports.copy_media
        if mode != "none":
            what = "low-res proxies" if mode == "proxy" else "full-quality originals"
            out.line(f"  Copying {what} into the library…")
        sessions = importer.import_clips(settings, store, fresh, source=str(root))
        out.ok(f"Imported {len(sessions)} session(s) from {root.name or root}")
        new_sessions += sessions

    if args.dry_run or not new_sessions:
        if not args.dry_run and not new_sessions:
            out.ok("Nothing new to import.")
        return 0
    if args.no_process:
        out.line("Run `vnote process` to write the notes.")
        return 0
    out.line("")
    out.info(
        "Keep the camera / card connected until “Extracting audio and keyframes” has finished: "
        "stills are cut from the full-quality files so that text stays readable."
    )
    new_sessions.sort(key=lambda s: s.started_ts)
    done = process_sessions(ctx, new_sessions)
    return 1 if any(s.status == "error" for s in done) else 0
