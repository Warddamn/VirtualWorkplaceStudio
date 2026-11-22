"""High-level control of a DJI Osmo Action 4 / Osmo Action 5 Pro over Bluetooth LE.

:class:`OsmoCamera` hides two unrelated protocols that the camera speaks on the same
Bluetooth characteristics:

* the official **R SDK** remote-control protocol (:mod:`videonotes.dji.rsdk`) --
  :meth:`~OsmoCamera.pair`, :meth:`~OsmoCamera.start_recording`,
  :meth:`~OsmoCamera.stop_recording`, :meth:`~OsmoCamera.status`;
* the reverse-engineered **livestream** protocol (:mod:`videonotes.dji.duml`) --
  :meth:`~OsmoCamera.start_livestream`, :meth:`~OsmoCamera.stop_livestream`.

Nothing in this package could be tried on a camera when it was written.  Every byte
is traceable to the two research reports (``rsdk_ble.md``, ``livestream_ble.md``) and,
through them, to DJI's demo code and to frames captured from real cameras; and every
frame sent or received is logged as hex at DEBUG level on the logger
``videonotes.dji`` (run ``vnote -vv ...``) so that a first session on hardware can be
compared with those sources.  The one exception: the Wi-Fi password is masked in the
log.

Where the two reports disagree, each protocol follows its own report:

* *Write type.*  R SDK frames are written **with** response and never split
  (``rsdk_ble.md`` §3.2-3.3: the camera ignores a command that arrives in pieces).
  Livestream frames are written **without** response and cut to the link's MTU
  (``livestream_ble.md`` §2.2, §9: that is what DJI Mimo does).
* *One connection, one protocol.*  Neither report could establish whether the two
  protocols may be mixed on one connection (``rsdk_ble.md`` §12,
  ``livestream_ble.md`` §7).  This class never mixes them: when a call needs the
  other protocol it drops the Bluetooth link and reconnects first, so every session
  looks like the ones the reference implementations were tested with.
* *Pairing.*  Each protocol has its own app-level pairing, confirmed once on the
  camera's screen: ``pair()`` does the R SDK handshake (``rsdk_ble.md`` §5);
  ``start_livestream()`` does the livestream pairing (``livestream_ble.md`` §5.1).
* *Model.*  Both reports identify the model from the advertisement; the R SDK
  handshake additionally reports it (``rsdk_ble.md`` §5.4), which wins when the two
  ever differ.
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import logging
import os
import secrets
import threading
from collections.abc import Callable, Coroutine
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, TypeVar

from . import duml, rsdk
from .transport import (
    ATT_HEADER,
    CHAR_FFF3,
    CHAR_NOTIFY,
    CHAR_WRITE,
    LINK_LOST_HELP,
    BleakTransport,
    BluetoothUnavailable,
    CameraDisconnected,
    CameraError,
    CameraNotFound,
    FakeTransport,
    FoundCamera,
    Transport,
    scan,
    write_chunked,
)

__all__ = [
    "BluetoothUnavailable",
    "CameraDisconnected",
    "CameraError",
    "CameraNotFound",
    "CameraStatus",
    "CameraTimeout",
    "CommandRejected",
    "FakeTransport",
    "FoundCamera",
    "Identity",
    "LivestreamFailed",
    "OsmoCamera",
    "PairingRejected",
    "PairingTimeout",
    "SyncCamera",
    "Timeouts",
    "WifiJoinFailed",
    "run_sync",
    "scan",
]

logger = logging.getLogger("videonotes.dji")

T = TypeVar("T")


# -- errors ----------------------------------------------------------------------------


class CameraTimeout(CameraError):
    """The camera did not answer a step in time."""


class PairingRejected(CameraError):
    """The pairing request was declined on the camera."""


class PairingTimeout(CameraTimeout):
    """The camera is (still) waiting for the user to confirm pairing on its screen."""


class CommandRejected(CameraError):
    """The camera answered a command with an error code."""


class WifiJoinFailed(CameraError):
    """The camera could not join the Wi-Fi network."""


class LivestreamFailed(CameraError):
    """The camera refused to start, or reported that it failed to start, the livestream."""


# -- tunables --------------------------------------------------------------------------


@dataclass
class Timeouts:
    """Per-step waiting times in seconds.

    They are engineering choices informed by the reference implementations (DJI's
    demo: 5 s per command, 30 s for the user; moblin: 60 s to start, 10 s to stop;
    osmosis: 8 s per step, 60 s for pairing; dji-vcam: an Osmo Action 5 Pro needs
    about 2 s to enter Live Streaming mode and 10-14 s to join Wi-Fi).  They are not
    protocol constants.
    """

    # R SDK
    command: float = 5.0  # response to a command
    pair_answer: float = 6.0  # the camera may stay completely silent this long after the pairing request
    pair: float = 30.0  # the user's time to confirm on the camera
    pair_prompt_after: float = 2.0  # a known camera that has not let us in by now is probably asking the user
    status: float = 4.0  # first status push after subscribing (pushes come at 2 Hz)
    record_confirm: float = 3.0  # a status push that reflects a record command
    # livestream
    step: float = 8.0  # one attempt of a request/reply step
    pair_reply: float = 2.5  # reply to the pairing request (normally within 250 ms)
    pair_approval: float = 60.0  # the user's time to confirm on the camera
    pair_resend: float = 8.0  # ask again this often while waiting, so the link does not idle
    cleanup_stop: float = 3.0  # the clean-up "stop" before starting; no answer is fine
    wifi: float = 20.0  # one attempt at joining Wi-Fi
    confirm_resend: float = 4.0  # reply to a start confirm written right behind the start frame
    start_confirm: float = 10.0  # reply to the start confirm
    refusal_grace: float = 3.0  # after a refused start confirm, wait this long for a better answer
    live_first: float = 3.0  # first livestream-state push after starting (they come about once a second)
    live_confirm: float = 20.0  # the state push that says "streaming" (or "failed")
    stop: float = 10.0
    abort_stop: float = 2.0  # "stop" sent while cleaning up after an error or Ctrl-C
    # link
    reconnect_pause: float = 1.0  # between dropping the link and looking for the camera again
    frame_gap: float = 0.1  # minimum spacing of livestream frames (back-to-back writes get dropped)
    chunk_gap: float = 0.03  # spacing of the pieces of one frame


# -- identity ----------------------------------------------------------------------------


def default_identity_path() -> Path:
    """``<videonotes home>/camera_identity.json``."""
    from ..config import default_home  # noqa: PLC0415 - keep import of this module light

    return default_home() / "camera_identity.json"


@dataclass
class Identity:
    """What this Mac presents to the camera when pairing.

    The camera remembers an approved controller, so the same values must be sent on
    every connection (``rsdk_ble.md`` §5.3, ``livestream_ble.md`` §5.1); they are
    generated once and kept in a small JSON file.
    """

    rsdk_device_id: int
    rsdk_mac: bytes  # 6-byte pseudo address; the camera accepts one unrelated to the real adapter
    rsdk_code: int  # verification code shown on the camera at first pairing (1000..9999)
    duml_identifier: str  # 32 characters; the camera stores its approval per identifier
    duml_pin: str  # 4 digits, shown on the camera when it asks for confirmation
    paired: list[str] = field(default_factory=list)  # cameras that accepted the R SDK handshake
    path: Path | None = None

    @classmethod
    def generate(cls, path: Path | None = None) -> Identity:
        mac = bytearray(secrets.token_bytes(6))
        mac[0] = (mac[0] & 0xFC) | 0x02  # locally administered, unicast
        return cls(
            rsdk_device_id=secrets.randbelow(0xFFFF0000) + 0x10000,
            rsdk_mac=bytes(mac),
            rsdk_code=1000 + secrets.randbelow(9000),
            duml_identifier=secrets.token_hex(16),
            duml_pin=f"{secrets.randbelow(10000):04d}",
            path=path,
        )

    @classmethod
    def load(cls, path: Path) -> Identity:
        """Read the identity file, creating it (or replacing an unreadable one) when needed."""
        try:
            data = json.loads(Path(path).read_text(encoding="utf-8"))
            identity = cls(
                rsdk_device_id=int(data["rsdk_device_id"]) & 0xFFFFFFFF,
                rsdk_mac=bytes.fromhex(str(data["rsdk_mac"])),
                rsdk_code=int(data["rsdk_code"]),
                duml_identifier=str(data["duml_identifier"]),
                duml_pin=str(data["duml_pin"]),
                paired=[str(a) for a in data.get("paired", [])],
                path=Path(path),
            )
            if len(identity.rsdk_mac) != 6 or not 0 <= identity.rsdk_code <= 0xFFFF:
                raise ValueError("bad rsdk values")
            if (
                not 1 <= len(identity.duml_identifier.encode()) <= 255
                or not 1 <= len(identity.duml_pin.encode()) <= 255
            ):
                raise ValueError("bad livestream values")
            return identity
        except FileNotFoundError:
            pass
        except (OSError, ValueError, KeyError, TypeError) as exc:
            logger.warning("Camera pairing file %s is unreadable (%s); the camera will ask to pair again.", path, exc)
        identity = cls.generate(Path(path))
        identity.save()
        return identity

    def save(self) -> None:
        """Write the file (best effort: a read-only home only costs a repeated pairing prompt)."""
        if self.path is None:
            return
        data = {
            "rsdk_device_id": self.rsdk_device_id,
            "rsdk_mac": self.rsdk_mac.hex(),
            "rsdk_code": self.rsdk_code,
            "duml_identifier": self.duml_identifier,
            "duml_pin": self.duml_pin,
            "paired": self.paired,
        }
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            tmp = self.path.with_name(self.path.name + ".tmp")
            tmp.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
            os.replace(tmp, self.path)
        except OSError as exc:
            logger.warning("Could not save the camera pairing file %s: %s", self.path, exc)


# -- status ------------------------------------------------------------------------------


@dataclass
class CameraStatus:
    """What the camera reports about itself.  ``None`` means "not reported".

    During a remote-control session this comes from the 2 Hz status push
    (``rsdk_ble.md`` §6.6; an Osmo Action 4 on older firmware does not report its
    battery).  During a livestream session only the battery level and the stream
    state are available.
    """

    model: str | None = None
    mode: str | None = None  # "Video", "Photo", "Live Streaming", ...
    state: str | None = None  # "idle", "recording", "pre-recording", "screen off", "playback"
    recording: bool | None = None
    recording_seconds: int | None = None
    battery_percent: int | None = None
    card_free_mb: int | None = None
    recording_time_left_s: int | None = None
    photos_left: int | None = None
    resolution: str | None = None
    fps: int | None = None
    stabilization: str | None = None
    temperature: str | None = None  # "normal", "warm (can still record)", "too hot to record", ...
    sleeping: bool | None = None
    livestreaming: bool | None = None
    raw: dict[str, int | None] = field(default_factory=dict)  # every field of the status push, DJI's names


# -- helpers -----------------------------------------------------------------------------


class _Link(Enum):
    NONE = "no session"
    RSDK = "remote control"
    DUML = "livestream"


_IDLE, _STARTING, _STREAMING = "idle", "starting", "streaming"

_PAIR_SILENT_ATTEMPTS = 3  # unanswered pairing requests before giving up on a characteristic

_NOT_ANSWERING_HELP = (
    "Make sure it is switched on and awake, close DJI Mimo on your phone (the camera accepts only one Bluetooth "
    "connection at a time) and try again. If it keeps happening: on the camera swipe down → Settings → Wireless "
    "Connection → reset the connection, and update the camera's firmware with DJI Mimo."
)


def _short(characteristic: str) -> str:
    return characteristic[4:8].upper()


def _model_from_settings() -> str | None:
    """``dji.model`` from config.toml, when it names a model."""
    try:
        from ..config import load_settings  # noqa: PLC0415

        return duml.normalize_model(load_settings()[0].dji.model)
    except Exception:  # a broken config must never break camera control
        return None


class _DropRecords(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return False


@contextlib.contextmanager
def _quiet_bleak(active: bool) -> Any:
    """While the Wi-Fi password is on its way, keep bleak from echoing the written bytes into the DEBUG log."""
    if not active:
        yield
        return
    target = logging.getLogger("bleak.backends.corebluetooth.client")
    blocker = _DropRecords()
    target.addFilter(blocker)
    try:
        yield
    finally:
        target.removeFilter(blocker)


def _is_secret(frame: duml.Frame) -> bool:
    return frame.command == duml.CMD_SETUP_WIFI and not frame.is_response


def _log_hex(frame: duml.Frame, raw: bytes) -> str:
    """Hex dump for the DEBUG log, with the Wi-Fi password masked."""
    text = [f"{b:02x}" for b in raw]
    if _is_secret(frame) and frame.payload:
        start = 11 + 1 + frame.payload[0] + 1  # header, SSID length byte, SSID, password length byte
        for i in range(start, len(raw) - 2):
            text[i] = "**"
        text[-2:] = ["**", "**"]  # the checksum would let a short password be recovered
    return " ".join(text)


# -- camera ------------------------------------------------------------------------------


class OsmoCamera:
    """Asynchronous control of one camera.

    Args:
        address: what :func:`scan` reported (a CoreBluetooth UUID on macOS).
        model: ``"action4"``, ``"action5pro"`` or ``"auto"``.  With ``"auto"`` the
            model is taken from the camera's advertisement, else from ``dji.model``
            in config.toml; if it stays unknown, the livestream uses a sequence that
            both models are expected to accept.
        transport: the Bluetooth link; a :class:`BleakTransport` by default.
        identity: pairing identity, or the path of its file; by default
            ``camera_identity.json`` in the videonotes home.
        timeouts: per-step waiting times.
        keepalive: send the livestream session's keep-alive frames.

    All methods must be awaited on the same event loop.  ``on_prompt``, when set, is
    called with a sentence whenever the user has to do something on the camera (the
    same text is logged as a warning).
    """

    def __init__(
        self,
        address: str,
        *,
        model: str = "auto",
        transport: Transport | None = None,
        identity: Identity | Path | str | None = None,
        timeouts: Timeouts | None = None,
        keepalive: bool = True,
    ) -> None:
        self.address = address
        self.on_prompt: Callable[[str], None] | None = None
        self._configured_model = duml.normalize_model(model)
        self._model_key = self._configured_model
        self._transport = transport
        self._identity_source = identity
        self._identity_obj: Identity | None = identity if isinstance(identity, Identity) else None
        self._timeouts = timeouts or Timeouts()
        self._keepalive_enabled = keepalive

        self._lock = asyncio.Lock()  # one operation at a time
        self._write_lock = asyncio.Lock()  # one frame on the wire at a time
        self._teardown_lock = asyncio.Lock()
        self._wake = asyncio.Event()  # set whenever something arrived or the link changed
        self._tasks: set[asyncio.Task[Any]] = set()
        self._keepalive_task: asyncio.Task[None] | None = None
        self._subscribed = False
        self._seq = 0
        self._last_duml_write = 0.0
        self._reset_session()

    # -- small accessors ----------------------------------------------------------------

    @property
    def model(self) -> str | None:
        """Resolved model key (``"action4"``, ``"action5pro"`` ...), or ``None`` while unknown."""
        return self._model_key

    @property
    def is_connected(self) -> bool:
        return self._transport is not None and self._transport.is_connected

    @property
    def is_livestreaming(self) -> bool:
        return self._stream_state == _STREAMING

    @property
    def battery_percent(self) -> int | None:
        """Last battery level the camera reported in this session."""
        if self._status is not None and self._status.camera_bat_percentage is not None:
            return self._status.camera_bat_percentage
        return self._battery

    def _profile(self) -> duml.ModelProfile:
        return duml.profile_for(self._model_key)

    def _identity(self) -> Identity:
        if self._identity_obj is None:
            source = self._identity_source
            self._identity_obj = Identity.load(Path(source) if source else default_identity_path())
        return self._identity_obj

    def _prompt(self, text: str) -> None:
        logger.warning("%s", text)
        if self.on_prompt is not None:
            try:
                self.on_prompt(text)
            except Exception:  # a broken callback must not break the session
                logger.debug("on_prompt callback failed", exc_info=True)

    def _reset_session(self) -> None:
        """Forget everything that belongs to one Bluetooth connection."""
        self._link = _Link.NONE
        self._subscribed = False
        self._stream_state = _IDLE
        self._duml_char = CHAR_WRITE
        self._rsdk_rx: dict[str, rsdk.Reassembler] = {}
        self._duml_rx: dict[str, duml.Reassembler] = {}
        self._rsdk_waiting: dict[tuple[int, int, int], rsdk.Frame | None] = {}
        self._duml_waiting: dict[tuple[bytes, int, int], duml.Frame | None] = {}
        self._handshake: rsdk.ConnectHandshake | None = None
        self._handshake_reply: rsdk.Frame | None = None
        self._status: rsdk.StatusPush | None = None
        self._status_count = 0
        self._status_time = 0.0
        self._mode_text: rsdk.NewStatusPush | None = None
        self._pair_decision: duml.PairingDecision | None = None
        self._battery: int | None = None
        self._live: duml.LiveStatus | None = None
        self._live_count = 0
        self._rx_rsdk_frames = 0
        self._rx_duml_frames = 0

    # -- connection ---------------------------------------------------------------------

    async def connect(self) -> None:
        """Find the camera and open the Bluetooth connection.

        Raises :class:`CameraNotFound` when the camera is not advertising (off, asleep,
        wireless disabled, or connected to another device), :class:`BluetoothUnavailable`
        when macOS does not let the terminal use Bluetooth, and ``BackendUnavailable``
        when the ``bleak`` package is missing.
        """
        async with self._lock:
            if self._transport is None:
                self._transport = BleakTransport(self.address)
            if self._transport.is_connected and self._subscribed:
                return
            await self._open_link()

    async def _open_link(self) -> None:
        transport = self._transport
        assert transport is not None
        self._reset_session()
        transport.set_disconnect_handler(self._on_link_closed)
        try:
            await transport.connect()
            await transport.subscribe(CHAR_NOTIFY, lambda data: self._on_notification(CHAR_NOTIFY, data))
        except BaseException:
            with contextlib.suppress(Exception):
                await transport.disconnect()
            raise
        self._subscribed = True
        self._resolve_model()
        logger.info(
            "Connected to the camera %s (model: %s, ATT MTU %d)",
            self.address,
            self._model_key or "unknown",
            transport.mtu,
        )

    def _resolve_model(self) -> None:
        advertisement = getattr(self._transport, "advertisement", None)
        advertised = duml.normalize_model(getattr(advertisement, "model", None))
        if self._configured_model:
            self._model_key = self._configured_model
            if advertised and advertised != self._configured_model:
                logger.warning(
                    "The camera advertises itself as %s but %s is configured; using the configured model. "
                    "Set dji.model = \"auto\" in config.toml to follow the camera.",
                    duml.MODELS[advertised].name, duml.MODELS[self._configured_model].name,
                )  # fmt: skip
        elif advertised:
            self._model_key = advertised
        elif self._model_key is None:
            self._model_key = _model_from_settings()

    def _on_link_closed(self) -> None:
        """The transport reports that the connection is gone (expected or not)."""
        self._link = _Link.NONE
        self._subscribed = False
        self._stream_state = _IDLE
        self._stop_keepalive()
        self._wake.set()

    async def disconnect(self) -> None:
        """Close the connection.  Safe in any state; never raises.

        If a livestream is starting or running, the camera is told to stop first, so
        that it leaves Live Streaming mode and its Wi-Fi goes back to normal.
        """
        try:
            await self._teardown(stop_stream=True)
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            logger.debug("Ignoring error while disconnecting: %r", exc)

    async def _teardown(self, *, stop_stream: bool) -> None:
        async with self._teardown_lock:
            transport = self._transport
            if transport is None:
                return
            try:
                if stop_stream and transport.is_connected and self._link is _Link.DUML and self._stream_state != _IDLE:
                    with contextlib.suppress(Exception):
                        await self._stop_stream(self._timeouts.abort_stop)
            finally:
                self._stop_keepalive()
                with contextlib.suppress(Exception):
                    await asyncio.wait_for(transport.disconnect(), 10.0)
                for task in list(self._tasks):
                    task.cancel()
                self._reset_session()
                self._wake.set()

    async def _reconnect(self, why: str) -> None:
        logger.info("Reconnecting to the camera (%s)", why)
        await self._teardown(stop_stream=False)
        await asyncio.sleep(self._timeouts.reconnect_pause)
        await self._open_link()

    async def _abort(self) -> None:
        """An operation was cancelled (Ctrl-C): stop a livestream and drop the link, even if cancelled again."""
        cleanup = asyncio.ensure_future(self._teardown(stop_stream=True))
        try:
            await asyncio.shield(cleanup)
        except asyncio.CancelledError:
            pass  # the clean-up keeps running in the background
        except Exception as exc:
            logger.debug("Ignoring error during clean-up: %r", exc)

    def _require_link(self) -> Transport:
        transport = self._transport
        if transport is None or not transport.is_connected:
            raise CameraDisconnected(f"The Bluetooth connection to the camera is not open. {LINK_LOST_HELP}")
        return transport

    # -- receiving ----------------------------------------------------------------------

    def _on_notification(self, characteristic: str, data: bytes) -> None:
        logger.debug("RX %s: %s", _short(characteristic), data.hex(" "))
        rsdk_rx = self._rsdk_rx.setdefault(characteristic, rsdk.Reassembler())
        duml_rx = self._duml_rx.setdefault(characteristic, duml.Reassembler())
        for rsdk_frame in rsdk_rx.feed(data):
            try:
                self._on_rsdk_frame(rsdk_frame)
            except Exception:  # one odd frame must not break notification handling
                logger.debug("Dropped R SDK frame %02X %02X", rsdk_frame.cmd_set, rsdk_frame.cmd_id, exc_info=True)
        for duml_frame in duml_rx.feed(data):
            try:
                self._on_duml_frame(duml_frame)
            except Exception:
                logger.debug("Dropped DUML frame %02X %02X", duml_frame.cmd_set, duml_frame.cmd_id, exc_info=True)
        self._wake.set()

    def _on_rsdk_frame(self, frame: rsdk.Frame) -> None:
        self._rx_rsdk_frames += 1
        kind = "response" if frame.is_response else "command"
        logger.debug(
            "RX rsdk %s %02X %02X seq=0x%04X payload=%s",
            kind, frame.cmd_set, frame.cmd_id, frame.seq, frame.payload.hex(" "),
        )  # fmt: skip
        command = frame.command
        if command == rsdk.CMD_STATUS_PUSH and not frame.is_response:
            self._status = rsdk.StatusPush.unpack(frame.payload)
            self._status_count += 1
            self._status_time = asyncio.get_running_loop().time()
        elif command == rsdk.CMD_NEW_STATUS_PUSH and not frame.is_response:
            self._mode_text = rsdk.NewStatusPush.unpack(frame.payload)
        elif command == rsdk.CMD_CONNECT and self._handshake is not None and not self._handshake.done:
            reply = self._handshake.on_frame(frame)
            if reply is not None:
                self._handshake_reply = reply
        elif frame.is_response:
            # match on response bit + command + SEQ: the camera's own SEQ counter overlaps ours (rsdk_ble.md §3.4)
            key = (frame.cmd_set, frame.cmd_id, frame.seq)
            if key in self._rsdk_waiting and self._rsdk_waiting[key] is None:
                self._rsdk_waiting[key] = frame
        # anything else (the undocumented 1D 05 response, unknown pushes) is ignored

    def _on_duml_frame(self, frame: duml.Frame) -> None:
        self._rx_duml_frames += 1
        logger.debug(
            "RX duml %02X->%02X id=%s flags=%02X %02X %02X payload=%s",
            frame.sender, frame.receiver, frame.msg_id.hex(), frame.flags, frame.cmd_set, frame.cmd_id,
            frame.payload.hex(" "),
        )  # fmt: skip
        command = frame.command
        if frame.wants_ack:  # a request from the camera
            if command == duml.CMD_PAIR_APPROVED:
                self._pair_decision = duml.parse_pairing_decision(frame.payload)
            # DJI Mimo answers every request; in a remote-control session DJI says to ignore these frames
            if self._link is _Link.DUML:
                self._spawn(self._send_duml(duml.ack(frame)))
            return
        if command == duml.CMD_BATTERY_PUSH:
            level = duml.parse_battery_percent(frame.payload)
            if level is not None:
                self._battery = level
        elif command == duml.CMD_LIVE_STATUS:
            live = duml.parse_live_status(frame.payload)
            if live is not None:
                self._live = live
                self._live_count += 1
        elif frame.is_response:
            # match on the echoed id and the command: several steps share command 02/8E (livestream_ble.md §9)
            key = (frame.msg_id, frame.cmd_set, frame.cmd_id)
            if key in self._duml_waiting and self._duml_waiting[key] is None:
                self._duml_waiting[key] = frame

    def _spawn(self, coro: Coroutine[Any, Any, Any]) -> None:
        task = asyncio.ensure_future(coro)
        self._tasks.add(task)

        def done(finished: asyncio.Task[Any]) -> None:
            self._tasks.discard(finished)
            if not finished.cancelled() and finished.exception() is not None:
                logger.debug("Background write failed: %r", finished.exception())

        task.add_done_callback(done)

    async def _wait_until(self, predicate: Callable[[], bool], timeout: float) -> bool:
        """Wait until ``predicate()`` holds; ``False`` on timeout.  Raises when the link is gone."""
        loop = asyncio.get_running_loop()
        deadline = loop.time() + max(0.0, timeout)
        while True:
            if predicate():
                return True
            if self._transport is None or not self._transport.is_connected:
                raise CameraDisconnected(f"The Bluetooth connection to the camera was lost. {LINK_LOST_HELP}")
            remaining = deadline - loop.time()
            if remaining <= 0:
                return False
            self._wake.clear()
            with contextlib.suppress(TimeoutError):
                await asyncio.wait_for(self._wake.wait(), remaining)

    # -- sending --------------------------------------------------------------------------

    def _next_seq(self) -> int:
        self._seq = (self._seq % 0xFFFF) + 1  # DJI's demo starts at 1 and counts up
        return self._seq

    async def _send_rsdk(self, frame: rsdk.Frame) -> None:
        transport = self._require_link()
        raw = frame.encode()
        limit = transport.mtu - ATT_HEADER
        if len(raw) > limit:
            # rsdk_ble.md §3.3: the camera ignores a command that arrives in several writes
            raise CameraError(
                f"The Bluetooth link only carries {limit} bytes per write, but the camera needs this {len(raw)}-byte "
                "command in one piece. Run the command again; if it keeps happening, switch Bluetooth off and on "
                "on the Mac."
            )
        properties = transport.properties(CHAR_WRITE)
        with_response = "write" in properties or not properties
        logger.debug("TX rsdk %02X %02X seq=0x%04X: %s", frame.cmd_set, frame.cmd_id, frame.seq, raw.hex(" "))
        async with self._write_lock:
            await transport.write(CHAR_WRITE, raw, with_response)

    async def _rsdk_request(
        self,
        command: tuple[int, int],
        payload: bytes,
        *,
        cmd_type: int = rsdk.CmdType.CMD_RESPONSE_OR_NOT,
        timeout: float | None = None,
        until: Callable[[], bool] | None = None,
    ) -> rsdk.Frame | None:
        """Send a command and wait for its response; ``None`` when none came in time.

        ``until`` ends the wait early when it becomes true (used where a status push
        is as good a confirmation as the optional response).
        """
        seq = self._next_seq()
        key = (command[0], command[1], seq)
        self._rsdk_waiting[key] = None
        try:
            await self._send_rsdk(rsdk.build(command, payload, seq, cmd_type))
            wait = self._timeouts.command if timeout is None else timeout
            await self._wait_until(
                lambda: self._rsdk_waiting.get(key) is not None or (until is not None and until()), wait
            )
            return self._rsdk_waiting.get(key)
        finally:
            self._rsdk_waiting.pop(key, None)

    async def _send_duml(self, frame: duml.Frame) -> None:
        transport = self._require_link()
        raw = frame.encode()
        characteristic = self._duml_char
        properties = transport.properties(characteristic)
        # livestream_ble.md §2.2-2.3: write without response when the characteristic allows it
        with_response = bool(properties) and "write-without-response" not in properties
        loop = asyncio.get_running_loop()
        async with self._write_lock:
            pause = self._timeouts.frame_gap - (loop.time() - self._last_duml_write)
            if pause > 0:
                await asyncio.sleep(pause)
            logger.debug(
                "TX duml %s %02X->%02X id=%s flags=%02X %02X %02X: %s",
                _short(characteristic), frame.sender, frame.receiver, frame.msg_id.hex(), frame.flags, frame.cmd_set,
                frame.cmd_id, _log_hex(frame, raw),
            )  # fmt: skip
            try:
                with _quiet_bleak(_is_secret(frame)):
                    await write_chunked(
                        transport, characteristic, raw, response=with_response, gap=self._timeouts.chunk_gap
                    )
            finally:
                self._last_duml_write = loop.time()

    async def _duml_request(
        self, frame: duml.Frame, *, timeout: float, attempts: int = 1, then: duml.Frame | None = None
    ) -> duml.Frame | None:
        """Send a request (and ``then`` right behind it) and wait for the reply; ``None`` when none came."""
        key = (frame.msg_id, frame.cmd_set, frame.cmd_id)
        self._duml_waiting[key] = None
        try:
            for _ in range(max(1, attempts)):
                await self._send_duml(frame)
                if then is not None:
                    await self._send_duml(then)
                if await self._wait_until(lambda: self._duml_waiting.get(key) is not None, timeout):
                    break
            return self._duml_waiting.get(key)
        finally:
            self._duml_waiting.pop(key, None)

    # -- R SDK: pairing -------------------------------------------------------------------

    async def pair(self) -> None:
        """Pair for remote control (official R SDK handshake, ``rsdk_ble.md`` §5).

        The first time, the camera shows a pop-up with a verification code (the same
        code is logged here); the user must accept it on the camera within about 30 s.
        Later connections from this Mac are accepted silently.

        Raises :class:`PairingTimeout` when the camera is still waiting for the user,
        :class:`PairingRejected` when the request was declined, and
        :class:`CameraTimeout` when the camera does not answer at all.
        """
        async with self._lock:
            await self._enter_rsdk()

    async def _enter_rsdk(self) -> None:
        """Make sure the current link carries an authorised remote-control session."""
        self._require_link()
        if self._link is _Link.RSDK:
            return
        if self._link is _Link.DUML:
            if self._stream_state != _IDLE:
                raise CameraError(
                    "The camera is busy with the livestream. Stop the livestream before using recording control."
                )
            await self._reconnect("remote control uses the camera's other Bluetooth protocol")
        await self._rsdk_handshake()

    async def _rsdk_handshake(self) -> None:
        identity = self._identity()
        timeouts = self._timeouts
        loop = asyncio.get_running_loop()
        first = self.address not in identity.paired
        code = identity.rsdk_code
        handshake = rsdk.ConnectHandshake(identity.rsdk_device_id, identity.rsdk_mac, code, first_pairing=first)
        self._handshake, self._handshake_reply = handshake, None
        duml_before = self._rx_duml_frames
        prompted = False
        if first:
            prompted = True
            self._prompt(f"Confirm the connection on the camera's screen. It should show the code {code:04d}.")
        request = handshake.start(self._next_seq())
        try:
            await self._send_rsdk(request)
            started = loop.time()
            resent = False
            while not handshake.done:
                now = loop.time()
                elapsed = now - started
                if handshake.state is rsdk.HandshakeState.REQUEST_SENT:
                    if elapsed >= timeouts.pair_answer:
                        break
                    if not resent and elapsed >= timeouts.pair_answer / 2:
                        resent = True  # the camera may not have been ready right after connecting
                        await self._send_rsdk(request)
                    wait = min(timeouts.pair_answer / 2, timeouts.pair_answer - elapsed)
                else:
                    if elapsed >= timeouts.pair:
                        break
                    if not prompted and elapsed >= timeouts.pair_prompt_after:
                        prompted = True  # known controller, but the camera forgot it and is asking again
                        self._prompt(
                            f"Confirm the connection on the camera's screen. It should show the code {code:04d}."
                        )
                    wait = timeouts.pair - elapsed
                    if not prompted:
                        wait = min(wait, max(timeouts.pair_prompt_after - elapsed, 0.01))
                state = handshake.state
                await self._wait_until(
                    lambda state=state: handshake.done or handshake.state is not state, max(wait, 0.01)
                )
            if handshake.state is rsdk.HandshakeState.CONNECTED and self._handshake_reply is not None:
                await self._send_rsdk(self._handshake_reply)  # step 4, echoing the camera's SEQ
        finally:
            self._handshake = None
        state = handshake.state
        if state is rsdk.HandshakeState.CONNECTED:
            self._link = _Link.RSDK
            self._adopt_device_id(handshake.camera_device_id)
            if self.address not in identity.paired:
                identity.paired.append(self.address)
                identity.save()
            logger.info("Paired with the camera for remote control")
            await self._subscribe_status()
            return
        if state is rsdk.HandshakeState.REJECTED:
            # the docs: disconnect at once and do not repeat the request
            await self._teardown(stop_stream=False)
            raise PairingRejected(
                "The connection was declined on the camera. Run the command again and accept the request on the "
                "camera's screen."
            )
        if state is rsdk.HandshakeState.FAILED:
            raise PairingRejected(
                f"The camera refused the pairing request ({rsdk.describe_return_code(handshake.ret_code or 0)}). "
                "On the camera swipe down → Settings → Wireless Connection → reset the connection, then try again."
            )
        if state is rsdk.HandshakeState.AWAITING_USER:
            raise PairingTimeout(
                f"The camera is waiting for you to confirm the connection on its screen (code {code:04d}). "
                f"Run the command again and tap the confirmation on the camera within {timeouts.pair:.0f} seconds."
            )
        detail = ""
        if self._rx_duml_frames > duml_before and self._rx_rsdk_frames == 0:
            # rsdk_ble.md §3.3: only 0x55 frames means the request was not accepted
            detail = " (it only sent data of its other protocol, which means it did not accept the request)"
        raise CameraTimeout(f"The camera did not answer the pairing request{detail}. {_NOT_ANSWERING_HELP}")

    def _adopt_device_id(self, device_id: int | None) -> None:
        reported = rsdk.model_from_device_id(device_id) if device_id is not None else None
        if reported is None:
            return
        if self._configured_model and self._configured_model != reported:
            logger.warning(
                "The camera identifies itself as %s but %s is configured; using the configured model.",
                duml.MODELS[reported].name, duml.MODELS[self._configured_model].name,
            )  # fmt: skip
            return
        self._model_key = reported

    async def _subscribe_status(self) -> None:
        """Ask for the 2 Hz status push (``1D 05``; the first ``1D 02`` push is the confirmation)."""
        frame = rsdk.build(
            rsdk.CMD_STATUS_SUBSCRIBE, rsdk.status_subscribe_payload(), self._next_seq(), rsdk.CmdType.CMD_NO_RESPONSE
        )
        await self._send_rsdk(frame)

    # -- R SDK: recording and status --------------------------------------------------------

    async def start_recording(self) -> None:
        """Start recording to the camera's card (``1D 03``, ``rsdk_ble.md`` §6.2).

        Pairs first if this connection is not paired yet.  In Photo mode the same
        command takes a photo.  Raises :class:`CommandRejected` with the camera's
        reason when it refuses (no card, card full, too hot ...).
        """
        async with self._lock:
            await self._enter_rsdk()
            await self._record(True)

    async def stop_recording(self) -> None:
        """Stop recording (``1D 03``)."""
        async with self._lock:
            await self._enter_rsdk()
            await self._record(False)

    async def _record(self, start: bool) -> None:
        what = "start recording" if start else "stop recording"
        loop = asyncio.get_running_loop()
        count = self._status_count
        pushes_flowing = self._status is not None and loop.time() - self._status_time < 1.5

        def reflected() -> bool:
            return self._status is not None and self._status_count > count and self._status.is_recording is start

        reply = await self._rsdk_request(rsdk.CMD_RECORD, rsdk.record_payload(start), until=reflected)
        if reply is None:
            # the response is optional in the protocol; a status push that shows the new state is as good
            if not await self._wait_until(reflected, self._timeouts.record_confirm):
                raise CameraTimeout(f"The camera did not answer the request to {what}. {_NOT_ANSWERING_HELP}")
            return
        code = rsdk.parse_return_code(reply.payload)
        if code:
            raise CommandRejected(self._record_refusal(start, code))
        if pushes_flowing and not await self._wait_until(reflected, min(2.0, self._timeouts.record_confirm)):
            status = self._status
            logger.warning(
                "The camera accepted the request to %s but reports it is %s in %s mode.",
                what, status.state_name if status else "?", status.mode_name if status else "?",
            )  # fmt: skip

    def _record_refusal(self, start: bool, code: int) -> str:
        what = "start recording" if start else "stop recording"
        text = f"The camera refused to {what} ({rsdk.describe_return_code(code)})."
        status = self._status
        if not start:
            return text + " It may not have been recording."
        hints = []
        if status is not None:
            if status.temp_over is not None and status.temp_over >= 2:
                hints.append("it reports that it is too hot to record; let it cool down")
            if status.remain_capacity == 0 or status.remain_time == 0:
                hints.append("its memory card is full or missing")
            if status.camera_mode == rsdk.MODE_WEBCAM:
                hints.append("it is in USB webcam mode")
            if status.is_recording:
                hints.append("it is already recording")
        if not hints:
            hints.append("check that a memory card with free space is inserted and that the camera is in Video mode")
        return text + " Possible reason: " + "; ".join(hints) + "."

    async def status(self) -> CameraStatus:
        """What the camera currently reports (mode, recording, battery, card).

        In a remote-control session this is the latest 2 Hz status push (pairing
        first if needed).  While a livestream is starting or running, only the battery
        level and the stream state are known, and no request is sent to the camera.
        """
        async with self._lock:
            self._require_link()
            if not (self._link is _Link.DUML and self._stream_state != _IDLE):
                await self._enter_rsdk()
                await self._fresh_status()
            return self._build_status()

    async def _fresh_status(self) -> rsdk.StatusPush:
        loop = asyncio.get_running_loop()
        if self._status is not None and loop.time() - self._status_time <= 1.5:
            return self._status
        count = self._status_count
        if not await self._wait_until(lambda: self._status_count > count, self._timeouts.status):
            await self._subscribe_status()  # the subscription may have been lost
            if not await self._wait_until(lambda: self._status_count > count, self._timeouts.status):
                raise CameraTimeout(
                    "The camera is connected but is not reporting its status. Wake it (tap the screen) and try again; "
                    "a sleeping camera stops reporting."
                )
        assert self._status is not None
        return self._status

    def _build_status(self) -> CameraStatus:
        model_name = duml.MODELS[self._model_key].name if self._model_key in duml.MODELS else None
        push = self._status
        if self._link is _Link.DUML or push is None:
            live = self._stream_state == _STREAMING or bool(self._live and self._live.streaming)
            in_session = self._link is _Link.DUML
            return CameraStatus(
                model=model_name,
                mode="Live Streaming" if in_session and self._stream_state != _IDLE else None,
                battery_percent=self._battery,
                livestreaming=live if in_session else None,
            )
        mode = push.mode_name
        if push.camera_mode not in rsdk.CAMERA_MODES and self._mode_text is not None and self._mode_text.mode_name:
            mode = self._mode_text.mode_name.title()
        return CameraStatus(
            model=model_name,
            mode=mode,
            state=push.state_name,
            recording=push.is_recording,
            recording_seconds=push.record_time if push.is_recording else None,
            battery_percent=push.camera_bat_percentage,
            card_free_mb=push.remain_capacity,
            recording_time_left_s=push.remain_time,
            photos_left=push.remain_photo_num if push.is_photo_mode else None,
            resolution=push.resolution_name,
            fps=push.fps,
            stabilization=push.stabilization_name,
            temperature=push.temperature_name,
            sleeping=push.is_sleeping,
            livestreaming=push.camera_mode == rsdk.MODE_LIVESTREAM if push.camera_mode is not None else None,
            raw=push.as_dict(),
        )

    async def version(self) -> rsdk.VersionInfo:
        """Version query (``00 00``): proves the camera answers remote-control commands.

        The strings do **not** identify the model or its firmware (``rsdk_ble.md`` §6.8).
        The 114-byte answer only fits links with an ATT MTU of at least 117.
        """
        async with self._lock:
            await self._enter_rsdk()
            reply = await self._rsdk_request(rsdk.CMD_VERSION, b"", cmd_type=rsdk.CmdType.CMD_WAIT_RESULT)
            if reply is None:
                raise CameraTimeout(f"The camera did not answer the version query. {_NOT_ANSWERING_HELP}")
            return rsdk.VersionInfo.unpack(reply.payload)

    # -- livestream -------------------------------------------------------------------------

    async def start_livestream(
        self,
        *,
        ssid: str,
        password: str,
        rtmp_url: str,
        resolution: str,
        bitrate_kbps: int,
        fps: int,
        stabilization: str = "off",
    ) -> None:
        """Make the camera join a Wi-Fi network and push an RTMP stream to ``rtmp_url``.

        Sequence (``livestream_ble.md`` §5; every step waits for the camera's reply):
        open session → pair (first time: confirm on the camera's screen) → stop (clean-up
        of an earlier stream) → prepare (Live Streaming mode) → join Wi-Fi →
        image stabilisation (Osmo Action 4 / 5 Pro) → start streaming → start confirm.

        Returns once the camera accepted the start command and, on bodies that report
        it, says that the stream is live.  A camera that never reports the stream's
        state is taken at its word after the start command; the RTMP server seeing the
        stream remains the final proof.

        Per-model choices, all from ``livestream_ble.md`` §5.0/§6: the stabilisation
        byte is ``0x08`` on an Osmo Action 4 and ``0x1A`` on an Osmo Action 5 Pro; the
        start confirm is written after the start reply on an Osmo Action 4 and right
        behind the start frame on an Osmo Action 5 Pro (and repeated once if the camera
        does not acknowledge it).  If an Osmo Action 5 Pro does not accept the start
        payload of that report, the layout DJI Mimo was captured sending to that model
        is tried (see :func:`videonotes.dji.duml.start_payload_mimo_json`).

        Raises ``ValueError`` for parameters the camera cannot use (checked before
        anything is sent), :class:`PairingTimeout` / :class:`PairingRejected`,
        :class:`WifiJoinFailed`, :class:`LivestreamFailed`, :class:`CameraTimeout` and
        :class:`CameraDisconnected`.  On any failure the camera is told to leave Live
        Streaming mode; on cancellation (Ctrl-C) it is also disconnected.
        """
        duml.validate_wifi(ssid, password)
        resolution = duml.validate_stream(
            self._profile(), rtmp_url=rtmp_url, resolution=resolution, fps=fps, bitrate_kbps=bitrate_kbps,
            stabilization=stabilization,
        )  # fmt: skip
        if bitrate_kbps > duml.RECOMMENDED_MAX_BITRATE_KBPS:
            logger.warning("Bitrates above %d kbit/s are reported to be unstable.", duml.RECOMMENDED_MAX_BITRATE_KBPS)
        if not password:
            logger.warning("No Wi-Fi password given: joining an open network is untested with these cameras.")
        async with self._lock:
            try:
                await self._start_livestream(ssid, password, rtmp_url, resolution, bitrate_kbps, fps, stabilization)
            except asyncio.CancelledError:
                logger.info("Interrupted: stopping the livestream and disconnecting")
                await self._abort()
                raise
            except CameraError:
                # leave Live Streaming mode so the camera is usable again; keep the link for the caller
                if self.is_connected and self._link is _Link.DUML and self._stream_state != _IDLE:
                    with contextlib.suppress(CameraError):
                        await self._stop_stream(self._timeouts.abort_stop)
                self._stream_state = _IDLE
                raise

    async def _start_livestream(
        self, ssid: str, password: str, rtmp_url: str, resolution: str, bitrate_kbps: int, fps: int, stabilization: str
    ) -> None:
        timeouts = self._timeouts
        await self._enter_duml()
        await self._duml_pair()
        # the model may only be known now (a remote-control handshake reports it); re-check the parameters
        profile = self._profile()
        duml.validate_stream(
            profile, rtmp_url=rtmp_url, resolution=resolution, fps=fps, bitrate_kbps=bitrate_kbps,
            stabilization=stabilization,
        )  # fmt: skip
        logger.info("Livestream sequence for %s", profile.name)

        # clean-up: a stream left over from an earlier session makes the camera refuse new settings
        self._stream_state = _STARTING
        await self._duml_request(duml.stop_streaming(), timeout=timeouts.cleanup_stop)

        reply = await self._duml_request(duml.prepare_livestream(), timeout=timeouts.step, attempts=3)
        if reply is None:
            raise CameraTimeout(
                f"The camera did not answer the request to enter Live Streaming mode. {_NOT_ANSWERING_HELP}"
            )
        code = duml.parse_result(reply.payload)
        if code:
            raise LivestreamFailed(
                f"The camera refused to enter Live Streaming mode ({duml.describe_result(code)}). Stop any recording, "
                "leave playback or the settings menu on the camera, and try again."
            )

        logger.info("Asking the camera to join Wi-Fi network %r", ssid)
        reply = await self._duml_request(duml.setup_wifi(ssid, password), timeout=timeouts.wifi, attempts=2)
        if reply is None:
            raise CameraTimeout(
                f"The camera did not say whether it joined the Wi-Fi network {ssid!r}. Keep the camera near the "
                "router and try again."
            )
        result = duml.parse_wifi_result(reply.payload)
        if not result.joined:
            answer = result.code.hex(" ") or "nothing"
            raise WifiJoinFailed(
                f"The camera could not join the Wi-Fi network {ssid!r} (it answered {answer}). "
                "Check the password and the exact network name (capital letters matter), and keep the camera within "
                "range. The network must be an ordinary 2.4 GHz or 5 GHz network with one password (WPA2): networks "
                "that ask for a user name or a web login cannot be joined, and 5 GHz networks on radar (DFS) channels "
                "52-144 are probably invisible to the camera. The camera uses the band selected in its own Wi-Fi "
                "settings."
            )

        configure = duml.configure_stabilization(profile, stabilization)
        if configure is not None:
            reply = await self._duml_request(configure, timeout=timeouts.step, attempts=2)
            code = duml.parse_result(reply.payload) if reply is not None else None
            if reply is None or code:
                # whether this step is needed at all is not established (livestream_ble.md §5.5): carry on
                logger.warning(
                    "The camera did not accept the image-stabilisation setting (%s); continuing.",
                    "no answer" if reply is None else duml.describe_result(code),
                )

        await self._start_stream(profile, rtmp_url, resolution, fps, bitrate_kbps)
        self._stream_state = _STREAMING
        logger.info("The camera is streaming to %s", rtmp_url)

    async def _enter_duml(self) -> None:
        """Make sure the current link carries a livestream session (and nothing else)."""
        self._require_link()
        if self._link is _Link.DUML:
            return
        if self._link is _Link.RSDK:
            await self._reconnect("the livestream uses the camera's other Bluetooth protocol")
        transport = self._require_link()
        # Some bodies answer livestream requests on FFF5 (livestream_ble.md §2.2): listen there too when it can
        # notify.  Only for this protocol: a remote-control session subscribes to FFF4 alone, as DJI's demo does.
        if transport.properties(CHAR_WRITE) & {"notify", "indicate"}:
            try:
                await transport.subscribe(CHAR_WRITE, lambda data: self._on_notification(CHAR_WRITE, data))
            except CameraDisconnected:
                raise
            except CameraError as exc:
                logger.debug("Could not enable notifications on FFF5 (not fatal): %s", exc)
        self._link = _Link.DUML
        self._duml_char = CHAR_WRITE
        self._pair_decision = None
        # DJI Mimo opens the session before pairing and keeps it alive (livestream_ble.md §5.10)
        await self._send_duml(duml.session_open())
        self._start_keepalive()

    def _start_keepalive(self) -> None:
        self._stop_keepalive()
        if self._keepalive_enabled:
            self._keepalive_task = asyncio.ensure_future(self._keepalive_loop())

    def _stop_keepalive(self) -> None:
        task, self._keepalive_task = self._keepalive_task, None
        if task is not None and not task.done():
            task.cancel()

    async def _keepalive_loop(self) -> None:
        """Keep the session alive: the camera is reported to drop an idle link, and falls back to its own
        access point when the link goes (``livestream_ble.md`` §5.10; dji-vcam protocol notes §3.13)."""
        profile = self._profile()
        frame = duml.session_keepalive(profile.keepalive_payload)
        try:
            while True:
                await asyncio.sleep(profile.keepalive_interval)
                if self._link is not _Link.DUML or not self.is_connected:
                    return
                await self._send_duml(frame)
        except CameraError as exc:
            logger.debug("Keep-alive stopped: %s", exc)

    def _fff3_usable(self) -> bool:
        assert self._transport is not None
        return bool(self._transport.properties(CHAR_FFF3) & {"write", "write-without-response"})

    async def _duml_pair(self) -> None:
        """Livestream pairing: SetPairingPIN, then wait for the user if the camera asks (§5.1)."""
        identity = self._identity()
        timeouts = self._timeouts
        loop = asyncio.get_running_loop()
        request = duml.pair_request(identity.duml_pin, identity.duml_identifier)
        deadline = loop.time() + timeouts.pair_approval
        self._pair_decision = None
        answered = prompted = False
        silent = 0

        def check_decision() -> bool:
            decision = self._pair_decision
            if decision is duml.PairingDecision.APPROVED:
                return True
            if decision in (duml.PairingDecision.DENIED, duml.PairingDecision.TIMED_OUT):
                raise PairingRejected(
                    "The pairing request was not confirmed on the camera "
                    f"({decision.value}). Run the command again and accept the request on the camera's screen."
                )
            return False

        while True:
            remaining = deadline - loop.time()
            if remaining <= 0:
                raise PairingTimeout(
                    "The camera is waiting for you to confirm the pairing request on its screen "
                    f"(code {identity.duml_pin}). Run the command again and tap the confirmation on the camera."
                )
            reply = await self._duml_request(request, timeout=min(timeouts.pair_reply, remaining))
            if check_decision():
                break
            if reply is not None:
                answered = True
                if duml.parse_pairing_status(reply.payload) is duml.PairingStatus.ALREADY_PAIRED:
                    break
                if not prompted:
                    prompted = True
                    self._prompt(
                        f"Confirm the pairing request on the camera's screen (it shows the code {identity.duml_pin})."
                    )
                # keep asking so the link does not idle while the user reaches for the camera
                wait = min(timeouts.pair_resend, max(0.0, deadline - loop.time()))
                await self._wait_until(lambda: self._pair_decision is not None, wait)
                if check_decision():
                    break
                continue
            if answered:
                continue  # the camera has answered before: it is waiting for the user
            silent += 1
            if silent >= _PAIR_SILENT_ATTEMPTS:
                if self._duml_char == CHAR_WRITE and self._fff3_usable():
                    # livestream_ble.md §2.3: some clients write to FFF3; try it before giving up
                    logger.info("No answer to the pairing request on FFF5; trying characteristic FFF3")
                    self._duml_char = CHAR_FFF3
                    silent = 0
                    continue
                raise CameraTimeout(f"The camera did not answer the livestream pairing request. {_NOT_ANSWERING_HELP}")
        logger.info("Paired with the camera for livestreaming")

    async def _start_stream(
        self, profile: duml.ModelProfile, rtmp_url: str, resolution: str, fps: int, bitrate_kbps: int
    ) -> None:
        timeouts = self._timeouts
        confirm = duml.start_confirm()
        confirm_key = (confirm.msg_id, confirm.cmd_set, confirm.cmd_id)
        behind = profile.confirm is duml.Confirm.BEHIND_START
        self._duml_waiting[confirm_key] = None  # catch the confirm's reply whenever it arrives
        self._live = None  # only states reported after the start count
        try:
            accepted = False
            answers: list[str] = []
            for label, payload in duml.start_payload_candidates(profile, rtmp_url, resolution, fps, bitrate_kbps):
                reply = await self._duml_request(
                    duml.start_streaming(payload), timeout=timeouts.step, attempts=2, then=confirm if behind else None
                )
                if reply is None:
                    answers.append(f"{label}: no answer")
                    logger.info("The camera did not answer the start command (%s layout)", label)
                    continue
                code = duml.parse_result(reply.payload)
                if not code:  # 00, or an empty reply
                    accepted = True
                    logger.info("The camera accepted the stream settings (%s layout)", label)
                    break
                answers.append(f"{label}: {duml.describe_result(code)}")
                logger.info("The camera refused the start command (%s layout): %s", label, duml.describe_result(code))
            if not accepted:
                raise LivestreamFailed(
                    "The camera refused to start streaming (" + "; ".join(answers) + "). Switch the camera off and on "
                    "again and retry; if it keeps refusing, update its firmware with DJI Mimo."
                )
            if profile.confirm is not duml.Confirm.NONE:
                await self._confirm_start(confirm, confirm_key, already_sent=behind, required=behind)
            await self._await_stream_state()
        finally:
            self._duml_waiting.pop(confirm_key, None)

    async def _confirm_start(
        self, confirm: duml.Frame, key: tuple[bytes, int, int], *, already_sent: bool, required: bool
    ) -> None:
        """Write the start confirm (again, if the one behind the start frame went unanswered) and read the answer.

        ``required``: the model does not stream without it, so an explicit refusal is an error.  On the other
        models the stream is known to start from the start frame alone (moblin), so a refusal is only logged.
        """
        timeouts = self._timeouts
        loop = asyncio.get_running_loop()

        def settled() -> bool:
            return self._duml_waiting.get(key) is not None or bool(self._live and self._live.streaming)

        if already_sent:
            await self._wait_until(settled, timeouts.confirm_resend)
        if not settled():
            await self._send_duml(confirm)
        deadline = loop.time() + timeouts.start_confirm
        refused: int | None = None
        while True:
            await self._wait_until(settled, max(0.0, deadline - loop.time()))
            if self._live is not None and self._live.streaming:
                return
            reply = self._duml_waiting.get(key)
            if reply is None:
                break
            code = duml.parse_result(reply.payload)
            if not code:
                return
            # refused -- but a duplicate confirm can be refused while the first one is being carried out
            refused = code
            self._duml_waiting[key] = None
            deadline = min(deadline, loop.time() + timeouts.refusal_grace)
        if refused is not None and required:
            raise LivestreamFailed(
                f"The camera refused to start streaming ({duml.describe_result(refused)}). Switch the camera off "
                "and on again and retry."
            )
        logger.warning(
            "The camera did not acknowledge the start command (%s); it may be streaming anyway.",
            "no answer" if refused is None else duml.describe_result(refused),
        )

    async def _await_stream_state(self) -> None:
        """Follow the camera's livestream-state pushes until it says "streaming" or "failed" (§5.8).

        Bodies that never send the push are taken at their word after ``live_first``
        seconds; a body that keeps reporting "ready" is given ``live_confirm`` seconds.
        """
        timeouts = self._timeouts
        loop = asyncio.get_running_loop()
        started = loop.time()
        # a body that sent no state push during "prepare" and the Wi-Fi join will hardly start now
        first = timeouts.live_first if self._live_count else min(timeouts.live_first, 1.0)
        while True:
            live = self._live
            if live is not None and live.streaming:
                return
            if live is not None and live.failed:
                raise LivestreamFailed(
                    "The camera joined the Wi-Fi network but reports that the livestream failed: it could not reach "
                    "the RTMP address. Make sure this Mac is on the same network as the camera, allow incoming "
                    "connections if macOS asks (System Settings → Network → Firewall), and try again."
                )
            limit = timeouts.live_confirm if live is not None else first
            remaining = started + limit - loop.time()
            if remaining <= 0:
                break
            count = self._live_count
            await self._wait_until(lambda count=count: self._live_count != count, remaining)
        if self._live is None:
            logger.info("The camera accepted the start command (this model does not report the stream's state)")
        else:
            logger.warning(
                "The camera accepted the start command but still reports %r; waiting for video will tell.",
                self._live.name,
            )

    async def stop_livestream(self) -> None:
        """Stop the livestream.  Safe in any state; never raises for a camera that is gone or not streaming."""
        async with self._lock:
            try:
                await self._stop_stream(self._timeouts.stop)
            except asyncio.CancelledError:
                await self._abort()
                raise

    async def _stop_stream(self, wait: float) -> None:
        transport = self._transport
        if transport is None or not transport.is_connected or self._link is not _Link.DUML:
            self._stream_state = _IDLE
            return
        try:
            reply = await self._duml_request(duml.stop_streaming(), timeout=wait)
            if reply is None:
                logger.warning("The camera did not confirm that it stopped streaming.")
            else:
                logger.info("The camera stopped streaming")
        except CameraError as exc:
            logger.warning("Could not tell the camera to stop streaming: %s", exc)
        finally:
            self._stream_state = _IDLE


# -- synchronous helpers -----------------------------------------------------------------


def run_sync(coro: Coroutine[Any, Any, T], *, timeout: float | None = None, cleanup_grace: float = 15.0) -> T:
    """Run one coroutine to completion on a private event loop and return its result.

    Meant for a *whole* Bluetooth session written as one coroutine (for example
    ``scan()``, or connect → pair → record → disconnect): bleak needs all calls of a
    session on the same loop, so do not call this once per camera method -- use
    :class:`SyncCamera` for that.

    Ctrl-C cancels the coroutine, then waits up to ``cleanup_grace`` seconds for its
    clean-up (:class:`OsmoCamera` stops a livestream and disconnects when cancelled)
    before ``KeyboardInterrupt`` is raised again.
    """
    loop = asyncio.new_event_loop()
    try:
        task = loop.create_task(coro if timeout is None else asyncio.wait_for(coro, timeout))
        try:
            return loop.run_until_complete(task)
        except KeyboardInterrupt:
            task.cancel()
            with contextlib.suppress(BaseException):
                loop.run_until_complete(asyncio.wait({task}, timeout=cleanup_grace))
            raise
    finally:
        try:
            pending = [t for t in asyncio.all_tasks(loop) if not t.done()]
            for t in pending:
                t.cancel()
            if pending:
                loop.run_until_complete(asyncio.wait(pending, timeout=5.0))
            loop.run_until_complete(loop.shutdown_asyncgens())
        except BaseException:  # never mask the real outcome with a shutdown problem
            logger.debug("Error while closing the event loop", exc_info=True)
        finally:
            loop.close()


class SyncCamera:
    """Blocking facade over :class:`OsmoCamera` for command-line code.

    One private event loop runs on a background thread for the lifetime of the
    object, so the connection (and the livestream keep-alive) stays alive while the
    calling thread does other work.  ``Ctrl-C`` during a call cancels the operation;
    the camera object then stops a livestream and disconnects on its own.

    Usage::

        with SyncCamera(address) as camera:
            camera.pair()
            camera.start_recording()
    """

    def __init__(self, address: str, *, model: str = "auto", **kwargs: Any) -> None:
        self.camera = OsmoCamera(address, model=model, **kwargs)
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._loop.run_forever, name="videonotes-dji", daemon=True)
        self._thread.start()

    def _call(self, coro: Coroutine[Any, Any, T], timeout: float | None = None) -> T:
        if self._loop.is_closed():
            coro.close()
            raise CameraDisconnected("This camera session was closed.")
        future = asyncio.run_coroutine_threadsafe(coro, self._loop)
        try:
            return future.result(timeout)
        except BaseException:
            future.cancel()  # Ctrl-C or timeout: the coroutine cleans up on the loop thread
            raise

    def connect(self) -> None:
        self._call(self.camera.connect())

    def pair(self) -> None:
        self._call(self.camera.pair())

    def start_recording(self) -> None:
        self._call(self.camera.start_recording())

    def stop_recording(self) -> None:
        self._call(self.camera.stop_recording())

    def status(self) -> CameraStatus:
        return self._call(self.camera.status())

    def start_livestream(self, **kwargs: Any) -> None:
        self._call(self.camera.start_livestream(**kwargs))

    def stop_livestream(self) -> None:
        self._call(self.camera.stop_livestream())

    def close(self) -> None:
        """Stop a livestream if one is running, disconnect and stop the background loop.  Never raises."""
        if self._loop.is_closed():
            return
        try:
            self._call(self.camera.disconnect(), timeout=20.0)
        except Exception:  # already gone, or Bluetooth was switched off: nothing more to do
            pass
        finally:
            self._loop.call_soon_threadsafe(self._loop.stop)
            self._thread.join(timeout=5.0)
            if not self._loop.is_running():
                self._loop.close()

    def __enter__(self) -> SyncCamera:
        self.connect()
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()
