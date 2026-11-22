"""Bluetooth LE transport for the DJI camera protocols.

The protocol logic in :mod:`videonotes.dji.camera` talks to the camera through the
small :class:`Transport` interface defined here, which has two implementations:

* :class:`BleakTransport` -- the real thing, on top of the optional ``bleak`` package
  (CoreBluetooth on macOS).  ``bleak`` is imported lazily, inside functions.
* :class:`FakeTransport` -- an in-memory stand-in for tests: it records every write
  and lets a test play the camera's notifications in any packetisation.

GATT layout, identical for the official R SDK and the reverse-engineered livestream
protocol (``rsdk_ble.md`` §3, ``livestream_ble.md`` §2.2): service ``FFF0``, camera to
app notifications on ``FFF4`` (some bodies also notify on ``FFF5``), app to camera
writes on ``FFF5``.

macOS specifics that shaped this module (``mac_capture.md`` §4): a camera's "address"
is a UUID that CoreBluetooth assigns per Mac, not its MAC; there is no way to request
an MTU; several bleak calls have no timeout of their own, so every call here is
bounded; and the first Bluetooth call of a process can wait for the user to answer
the macOS permission dialog.
"""

from __future__ import annotations

import asyncio
import contextlib
import inspect
import logging
import os
import platform
from collections.abc import Awaitable, Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable

from ..backends.base import BackendUnavailable
from . import duml, rsdk

logger = logging.getLogger("videonotes.dji.transport")

SERVICE_UUID = "0000fff0-0000-1000-8000-00805f9b34fb"
CHAR_FFF3 = "0000fff3-0000-1000-8000-00805f9b34fb"  # alternative write characteristic some clients use
CHAR_NOTIFY = "0000fff4-0000-1000-8000-00805f9b34fb"  # FFF4: camera -> app
CHAR_WRITE = "0000fff5-0000-1000-8000-00805f9b34fb"  # FFF5: app -> camera

ATT_HEADER = 3  # bytes of the ATT MTU that are not payload
DEFAULT_ATT_MTU = 23  # what a link has before (or without) MTU negotiation

BLEAK_INSTALL_HINT = "Bluetooth control needs the 'bleak' package. Install it:  pip install 'videonotes[ble]'"

NotifyCallback = Callable[[bytes], None]


# -- errors ----------------------------------------------------------------------------


class CameraError(RuntimeError):
    """Something went wrong talking to the camera; the message says what to do next."""


class BluetoothUnavailable(CameraError):
    """Bluetooth cannot be used on this Mac right now (switched off, or not permitted)."""


class CameraNotFound(CameraError):
    """The camera was not seen over Bluetooth."""


class CameraDisconnected(CameraError):
    """The Bluetooth link to the camera is not (or no longer) there."""


# -- advertisements --------------------------------------------------------------------


@dataclass
class FoundCamera:
    """A DJI camera seen in a Bluetooth scan."""

    address: str  # CoreBluetooth UUID on macOS (specific to this Mac), a MAC address elsewhere
    name: str
    rssi: int | None
    model: str | None  # "action4", "action5pro", ... as used in config.toml; None when not recognised
    model_name: str | None = None  # "Osmo Action 4"
    mac: str | None = None  # the camera's own Bluetooth address, when the advertisement carries it
    remote_control: bool = False  # advertises the marker DJI's remote-control (R SDK) demo looks for


def parse_advertisement(
    address: str, name: str | None, rssi: int | None, manufacturer_data: Mapping[int, bytes]
) -> FoundCamera | None:
    """Recognise a DJI camera from advertising data in the form bleak reports it.

    ``manufacturer_data`` maps the Bluetooth company id to the bytes that follow it.
    A DJI camera uses company ``0x08AA`` ("Xtra" rebadges ``0xF7AA``); the first two
    bytes are the model id, little endian (``14 00`` Osmo Action 4, ``15 00`` Osmo
    Action 5 Pro), the third is ``FA`` on cameras that support the official remote
    protocol, and the next six are the camera's MAC address (``rsdk_ble.md`` §2.1-2.2,
    ``livestream_ble.md`` §2.1).  Returns ``None`` for anything else.
    """
    for company_id, raw in manufacturer_data.items():
        data = bytes(raw)
        profile = duml.identify_model(company_id, data)
        if profile is None:
            continue
        known = profile is not duml.UNKNOWN_MODEL
        marker = len(data) >= 3 and data[2] == rsdk.RSDK_MARKER
        mac = ":".join(f"{b:02X}" for b in data[3:9]) if marker and len(data) >= 9 else None
        return FoundCamera(
            address=address,
            name=name or "",
            rssi=rssi,
            model=profile.key if known else None,
            model_name=profile.name if known else None,
            mac=mac,
            remote_control=rsdk.is_rsdk_camera(company_id, data),
        )
    return None


def scan_service_filter(macos_version: str | None = None) -> list[str] | None:
    """Service UUIDs to pass to the scanner, or ``None`` for an unfiltered scan.

    Cameras are recognised by their manufacturer data, so no filter is wanted.  The
    exception is macOS 12.0 - 12.2, where CoreBluetooth delivers no advertisements
    to a plain Python process unless a service filter is given (bleak issue 720);
    the cameras do list ``FFF0`` in their advertisement.
    """
    version = platform.mac_ver()[0] if macos_version is None else macos_version
    parts = [int(p) for p in version.split(".")[:2] if p.isdigit()]
    if len(parts) == 2 and parts[0] == 12 and parts[1] < 3:
        return [SERVICE_UUID]
    return None


def terminal_app_name(environ: Mapping[str, str] | None = None) -> str:
    """Best guess at the app macOS holds responsible for our Bluetooth use (the terminal emulator)."""
    env = os.environ if environ is None else environ
    known = {"Apple_Terminal": "Terminal", "iTerm.app": "iTerm", "vscode": "Visual Studio Code", "WarpTerminal": "Warp"}
    return known.get(env.get("TERM_PROGRAM", ""), "your terminal app")


def bluetooth_unavailable(reason: str, detail: str = "") -> BluetoothUnavailable:
    """Turn bleak's reason for "Bluetooth not available" into an instruction."""
    app = terminal_app_name()
    reason = reason.upper()
    if reason in ("DENIED_BY_USER", "DENIED_BY_UNKNOWN"):
        text = (
            f"macOS is not letting {app} use Bluetooth. Open System Settings → Privacy & Security → Bluetooth, "
            f"switch on {app}, then quit {app} completely and start it again."
        )
    elif reason == "DENIED_BY_SYSTEM":
        text = (
            "Bluetooth is restricted on this Mac (for example by Screen Time or a management profile). "
            "Lift the restriction in System Settings, then try again."
        )
    elif reason == "POWERED_OFF":
        text = "Bluetooth is switched off on this Mac. Turn it on in Control Centre or System Settings → Bluetooth."
    elif reason in ("NO_BLUETOOTH", "NO_BLE_CENTRAL_ROLE"):
        text = "This computer has no usable Bluetooth LE radio, so the camera cannot be controlled from it."
    elif reason == "PERMISSION_TIMEOUT":
        text = (
            f"macOS did not grant Bluetooth access in time. If a dialog asked whether {app} may use Bluetooth, "
            f"choose Allow and run the command again; otherwise enable {app} under "
            "System Settings → Privacy & Security → Bluetooth."
        )
    else:
        text = "Bluetooth is not available right now. Wait a few seconds and try again."
    if detail:
        text += f" ({detail})"
    return BluetoothUnavailable(text)


# -- transport interface -----------------------------------------------------------------


@runtime_checkable
class Transport(Protocol):
    """What the camera logic needs from a Bluetooth link."""

    address: str
    #: what the camera advertised when it was found, if known
    advertisement: FoundCamera | None

    async def connect(self) -> None:
        """Find the camera and open a GATT connection; raises a :class:`CameraError`."""
        ...

    async def disconnect(self) -> None:
        """Close the connection.  Never raises; safe to call when not connected."""
        ...

    async def write(self, characteristic: str, data: bytes, response: bool) -> None:
        """One GATT write of ``data`` (the caller keeps it within :attr:`mtu`)."""
        ...

    async def subscribe(self, characteristic: str, callback: NotifyCallback) -> None:
        """Enable notifications; ``callback`` gets every value, on the event loop."""
        ...

    def properties(self, characteristic: str) -> frozenset[str]:
        """GATT properties of a characteristic (``"write"``, ``"notify"`` ...); empty if it does not exist."""
        ...

    def set_disconnect_handler(self, handler: Callable[[], None] | None) -> None:
        """``handler`` is called (on the event loop) whenever the link goes away."""
        ...

    @property
    def is_connected(self) -> bool: ...

    @property
    def mtu(self) -> int:
        """ATT MTU of the link; one write carries at most ``mtu - 3`` bytes."""
        ...


def split_for_write(data: bytes, max_len: int) -> list[bytes]:
    """Cut ``data`` into pieces of at most ``max_len`` bytes (the last one may be shorter)."""
    if max_len < 1:
        raise ValueError("max_len must be positive")
    data = bytes(data)
    return [data[i : i + max_len] for i in range(0, len(data), max_len)] or [b""]


async def write_chunked(
    transport: Transport, characteristic: str, data: bytes, *, response: bool, gap: float = 0.03
) -> int:
    """Write ``data`` in as many GATT writes as the link's MTU requires; returns the number of writes.

    A write-without-response longer than the MTU allows is silently dropped by
    CoreBluetooth, so long frames must be cut.  The pieces are paced ``gap`` seconds
    apart (dji-remote sends 20-byte pieces every 30 ms to an Osmo Action 4).  Only the
    livestream protocol may be split like this; R SDK frames must go out in one write.
    """
    pieces = split_for_write(data, max(DEFAULT_ATT_MTU - ATT_HEADER, transport.mtu - ATT_HEADER))
    for index, piece in enumerate(pieces):
        if index and gap > 0:
            await asyncio.sleep(gap)
        await transport.write(characteristic, piece, response)
    return len(pieces)


# -- bleak -------------------------------------------------------------------------------


def _import_bleak() -> Any:
    try:
        import bleak  # noqa: PLC0415 - optional dependency, imported lazily
    except ImportError as exc:
        raise BackendUnavailable(BLEAK_INSTALL_HINT) from exc
    return bleak


def _translate_bleak_error(exc: BaseException, doing: str) -> CameraError:
    """Map an exception raised by bleak to one of our errors (``doing`` completes "while ...")."""
    try:
        from bleak import exc as bleak_exc  # noqa: PLC0415
    except ImportError:  # pragma: no cover - bleak raised it, so it is importable
        return CameraError(f"Bluetooth failed while {doing}: {exc}")
    if isinstance(exc, bleak_exc.BleakBluetoothNotAvailableError):
        reason = getattr(exc.reason, "name", "UNKNOWN")
        return bluetooth_unavailable(reason)
    if isinstance(exc, bleak_exc.BleakDeviceNotFoundError):
        return CameraNotFound(CAMERA_NOT_FOUND_HELP)
    if isinstance(exc, TimeoutError):
        return CameraDisconnected(f"The camera did not respond over Bluetooth while {doing}. {LINK_LOST_HELP}")
    text = str(exc).strip() or type(exc).__name__
    if "disconnected" in text.lower() or "not connected" in text.lower():
        return CameraDisconnected(f"The Bluetooth connection to the camera was lost while {doing}. {LINK_LOST_HELP}")
    return CameraError(f"Bluetooth failed while {doing}: {text}")


CAMERA_NOT_FOUND_HELP = (
    "The camera was not found over Bluetooth. Switch it on and wake it (tap the screen or press a button), keep it "
    "within a few metres, and make sure its wireless connection is enabled (swipe down on the camera → Settings → "
    "Wireless Connection). Close DJI Mimo on your phone: the camera accepts only one Bluetooth connection at a time."
)
LINK_LOST_HELP = "Make sure the camera is switched on, awake and close to the Mac, then try again."


async def _start_scanner(scanner: Any, permission_timeout: float = 120.0, notice_after: float = 3.0) -> None:
    """Start a ``BleakScanner``; survive the wait for the macOS Bluetooth permission dialog.

    ``BleakScanner.start()`` waits without a timeout until CoreBluetooth reports its
    state, which only happens once the user has answered the permission dialog.
    """
    task = asyncio.ensure_future(scanner.start())
    try:
        done, _ = await asyncio.wait({task}, timeout=notice_after)
        if not done:
            logger.warning(
                "Waiting for macOS to allow Bluetooth: if a dialog asks whether %s may use Bluetooth, choose Allow.",
                terminal_app_name(),
            )
            done, _ = await asyncio.wait({task}, timeout=permission_timeout)
        if not done:
            raise bluetooth_unavailable("PERMISSION_TIMEOUT")
        task.result()
    except CameraError:
        raise
    except asyncio.CancelledError:
        raise
    except Exception as exc:
        raise _translate_bleak_error(exc, "starting the Bluetooth scan") from exc
    finally:
        if not task.done():
            task.cancel()


async def _stop_scanner(scanner: Any) -> None:
    with contextlib.suppress(Exception):
        await asyncio.wait_for(scanner.stop(), 5.0)


class _Sighting:
    """Everything learned about one device during a scan (advertisement and scan response arrive separately)."""

    def __init__(self, device: Any) -> None:
        self.device = device
        self.name = ""
        self.rssi: int | None = None
        self.manufacturer_data: dict[int, bytes] = {}

    def update(self, device: Any, adv: Any) -> None:
        self.device = device
        self.name = getattr(adv, "local_name", None) or getattr(device, "name", None) or self.name
        rssi = getattr(adv, "rssi", None)
        if isinstance(rssi, int):
            self.rssi = rssi
        for company_id, value in (getattr(adv, "manufacturer_data", None) or {}).items():
            self.manufacturer_data[int(company_id)] = bytes(value)

    def camera(self) -> FoundCamera | None:
        return parse_advertisement(self.device.address, self.name, self.rssi, self.manufacturer_data)


async def scan(timeout: float = 8.0, name_filter: str = "", *, scanner_factory: Any = None) -> list[FoundCamera]:
    """Look for DJI cameras for ``timeout`` seconds; strongest signal first.

    Cameras are recognised from their manufacturer data (see
    :func:`parse_advertisement`), never from their name, which the user can change.
    ``name_filter`` keeps only cameras whose name contains it (case-insensitive).
    ``scanner_factory`` replaces ``bleak.BleakScanner`` in tests.

    Raises :class:`BluetoothUnavailable` when Bluetooth is off or not permitted, and
    ``BackendUnavailable`` when the ``bleak`` package is missing.
    """
    factory = scanner_factory or _import_bleak().BleakScanner
    sightings: dict[str, _Sighting] = {}

    def on_advertisement(device: Any, adv: Any) -> None:
        sightings.setdefault(device.address, _Sighting(device)).update(device, adv)

    kwargs: dict[str, Any] = {}
    service_filter = scan_service_filter()
    if service_filter:
        kwargs["service_uuids"] = service_filter
    scanner = factory(detection_callback=on_advertisement, **kwargs)
    await _start_scanner(scanner)
    try:
        await asyncio.sleep(max(0.0, timeout))
    finally:
        await _stop_scanner(scanner)
    wanted = name_filter.strip().lower()
    found = [camera for camera in (s.camera() for s in sightings.values()) if camera is not None]
    if wanted:
        found = [camera for camera in found if wanted in camera.name.lower()]
    found.sort(key=lambda c: c.rssi if c.rssi is not None else -999, reverse=True)
    return found


class BleakTransport:
    """:class:`Transport` on top of ``bleak`` (CoreBluetooth on macOS).

    Every bleak call was checked against the bleak 3.1 sources: ``BleakScanner(detection_callback=...,
    service_uuids=...)`` with ``start()`` / ``stop()``; ``BleakClient(device, disconnected_callback=...,
    services=[...], timeout=...)`` with ``connect()``, ``disconnect()``, ``is_connected``, ``services``,
    ``start_notify(char, callback)`` and ``write_gatt_char(char, data, response=...)``; and
    ``BleakGATTCharacteristic.properties`` / ``.max_write_without_response_size``.
    """

    def __init__(
        self,
        address: str,
        *,
        scan_timeout: float = 12.0,
        connect_timeout: float = 20.0,
        gatt_timeout: float = 10.0,
        client_factory: Any = None,
        scanner_factory: Any = None,
    ) -> None:
        self.address = address
        self.advertisement: FoundCamera | None = None
        self._scan_timeout = scan_timeout
        self._connect_timeout = connect_timeout
        self._gatt_timeout = gatt_timeout
        self._client_factory = client_factory
        self._scanner_factory = scanner_factory
        self._client: Any = None
        self._chars: dict[str, Any] = {}
        self._subscribed: set[str] = set()
        self._on_disconnect: Callable[[], None] | None = None

    # -- connection -------------------------------------------------------------------

    def set_disconnect_handler(self, handler: Callable[[], None] | None) -> None:
        self._on_disconnect = handler

    async def connect(self) -> None:
        if self.is_connected:
            return
        bleak = None if (self._client_factory and self._scanner_factory) else _import_bleak()
        device = await self._find_device(self._scanner_factory or bleak.BleakScanner)
        client_factory = self._client_factory or bleak.BleakClient
        # services=[FFF0]: only the DJI service is discovered (an Osmo Action 5 Pro also exposes HID and battery)
        client = client_factory(
            device,
            disconnected_callback=self._handle_disconnect,
            services=[SERVICE_UUID],
            timeout=self._connect_timeout,
        )
        try:
            # connect() has a timeout, but on expiry it waits for the cancellation without one
            await asyncio.wait_for(client.connect(), self._connect_timeout + 10.0)
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            with contextlib.suppress(Exception):
                await asyncio.wait_for(client.disconnect(), 5.0)
            error = _translate_bleak_error(exc, "connecting to the camera")
            if isinstance(exc, TimeoutError):
                error = CameraDisconnected(
                    "The camera was seen but did not accept the Bluetooth connection. Wake it, close DJI Mimo on your "
                    "phone (the camera accepts only one Bluetooth connection at a time), and try again."
                )
            raise error from exc
        self._client = client
        self._chars = {}
        self._subscribed = set()
        try:
            services = client.services
            for uuid in (CHAR_NOTIFY, CHAR_WRITE, CHAR_FFF3):
                char = services.get_characteristic(uuid)
                if char is not None:
                    self._chars[uuid] = char
        except Exception as exc:
            await self.disconnect()
            raise _translate_bleak_error(exc, "reading the camera's Bluetooth services") from exc
        if CHAR_NOTIFY not in self._chars or CHAR_WRITE not in self._chars:
            await self.disconnect()
            raise CameraError(
                "This Bluetooth device does not offer the DJI camera service. If it is the camera, switch it off and "
                "on again and retry; otherwise run `vnote camera forget` and `vnote camera scan` to pick the camera."
            )
        await self._wait_for_mtu()

    async def _find_device(self, scanner_factory: Any) -> Any:
        """Scan until the camera with our address shows up (never connect by a bare address string)."""
        wanted = self.address.lower()
        sighting: _Sighting | None = None
        sighted = asyncio.Event()  # the device was seen at all
        complete = asyncio.Event()  # ... and with manufacturer data (it may only come with the scan response)

        def on_advertisement(device: Any, adv: Any) -> None:
            nonlocal sighting
            if str(device.address).lower() != wanted:
                return
            if sighting is None:
                sighting = _Sighting(device)
            sighting.update(device, adv)
            sighted.set()
            if sighting.manufacturer_data:
                complete.set()

        kwargs: dict[str, Any] = {}
        service_filter = scan_service_filter()
        if service_filter:
            kwargs["service_uuids"] = service_filter
        scanner = scanner_factory(detection_callback=on_advertisement, **kwargs)
        await _start_scanner(scanner)
        try:
            with contextlib.suppress(TimeoutError):
                await asyncio.wait_for(sighted.wait(), self._scan_timeout)
                await asyncio.wait_for(complete.wait(), 1.0)
        finally:
            await _stop_scanner(scanner)
        if sighting is None:
            raise CameraNotFound(CAMERA_NOT_FOUND_HELP)
        self.advertisement = sighting.camera()
        return sighting.device

    async def _wait_for_mtu(self, settle: float = 2.0) -> None:
        """Right after connecting the write size can still read 20; give it a moment to grow."""
        loop = asyncio.get_running_loop()
        deadline = loop.time() + settle
        while self.mtu <= DEFAULT_ATT_MTU and loop.time() < deadline and self.is_connected:
            await asyncio.sleep(0.1)
        logger.debug("ATT MTU %d (writes of up to %d bytes)", self.mtu, self.mtu - ATT_HEADER)

    def _handle_disconnect(self, _client: Any = None) -> None:
        logger.debug("Bluetooth link to %s closed", self.address)
        handler = self._on_disconnect
        if handler is not None:
            handler()

    async def disconnect(self) -> None:
        client, self._client = self._client, None
        self._chars = {}
        self._subscribed = set()
        if client is None:
            return
        try:
            # disconnect() waits for CoreBluetooth without a timeout of its own
            await asyncio.wait_for(client.disconnect(), 5.0)
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            logger.debug("Ignoring error while disconnecting: %r", exc)

    @property
    def is_connected(self) -> bool:
        client = self._client
        try:
            return bool(client is not None and client.is_connected)
        except Exception:  # CoreBluetooth objects can be gone during shutdown
            return False

    @property
    def mtu(self) -> int:
        char = self._chars.get(CHAR_WRITE)
        try:
            if char is not None:
                return int(char.max_write_without_response_size) + ATT_HEADER
            if self._client is not None:
                return int(self._client.mtu_size)
        except Exception:
            pass
        return DEFAULT_ATT_MTU

    # -- GATT -------------------------------------------------------------------------

    def properties(self, characteristic: str) -> frozenset[str]:
        char = self._chars.get(characteristic)
        return frozenset(char.properties) if char is not None else frozenset()

    def _char(self, characteristic: str) -> Any:
        if not self.is_connected:
            raise CameraDisconnected(f"Not connected to the camera. {LINK_LOST_HELP}")
        char = self._chars.get(characteristic)
        if char is None:
            raise CameraError(f"The camera has no Bluetooth characteristic {characteristic[4:8].upper()}.")
        return char

    async def write(self, characteristic: str, data: bytes, response: bool) -> None:
        char = self._char(characteristic)
        try:
            # a write with response waits for the camera's acknowledgement without a timeout of its own
            await asyncio.wait_for(
                self._client.write_gatt_char(char, bytes(data), response=response), self._gatt_timeout
            )
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            raise _translate_bleak_error(exc, "sending a command to the camera") from exc

    async def subscribe(self, characteristic: str, callback: NotifyCallback) -> None:
        char = self._char(characteristic)
        if characteristic in self._subscribed:
            return

        def on_value(_sender: Any, data: bytearray) -> None:
            callback(bytes(data))

        try:
            await asyncio.wait_for(self._client.start_notify(char, on_value), self._gatt_timeout)
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            raise _translate_bleak_error(exc, "subscribing to the camera's notifications") from exc
        self._subscribed.add(characteristic)


# -- fake --------------------------------------------------------------------------------

DEFAULT_FAKE_CHARACTERISTICS: Mapping[str, frozenset[str]] = {
    # property sets reported for an Osmo Action 4 (livestream_ble.md §2.2)
    CHAR_FFF3: frozenset({"read", "write", "notify", "indicate"}),
    CHAR_NOTIFY: frozenset({"read", "write", "notify", "indicate"}),
    CHAR_WRITE: frozenset({"read", "write-without-response", "write", "notify", "indicate"}),
}

WriteHook = Callable[["FakeTransport", str, bytes, bool], Awaitable[None] | None]


@dataclass(frozen=True)
class RecordedWrite:
    characteristic: str
    data: bytes
    response: bool


class FakeTransport:
    """In-memory :class:`Transport` for tests.

    * every write is appended to :attr:`writes` (and checked against the MTU, because
      a real link would drop or mangle an oversized write);
    * ``on_write`` -- a function or coroutine function ``(transport, characteristic,
      data, response)`` -- lets a test script the camera's reaction;
    * :meth:`feed` delivers bytes as notifications, cut into any packetisation;
    * :meth:`drop` simulates the link going away.
    """

    def __init__(
        self,
        address: str = "FAKE-0000-CAMERA",
        *,
        mtu: int = 185,
        characteristics: Mapping[str, Iterable[str]] | None = None,
        advertisement: FoundCamera | None = None,
        on_write: WriteHook | None = None,
    ) -> None:
        self.address = address
        self.advertisement = advertisement
        self.on_write = on_write
        self.writes: list[RecordedWrite] = []
        self.connect_count = 0
        self.disconnect_count = 0
        #: raise this from the next ``connect()`` (then forget it)
        self.connect_error: Exception | None = None
        self._mtu = mtu
        chars = DEFAULT_FAKE_CHARACTERISTICS if characteristics is None else characteristics
        self._characteristics = {uuid: frozenset(props) for uuid, props in chars.items()}
        self._callbacks: dict[str, NotifyCallback] = {}
        self._connected = False
        self._on_disconnect: Callable[[], None] | None = None

    # -- Transport --------------------------------------------------------------------

    def set_disconnect_handler(self, handler: Callable[[], None] | None) -> None:
        self._on_disconnect = handler

    async def connect(self) -> None:
        if self.connect_error is not None:
            error, self.connect_error = self.connect_error, None
            raise error
        if not self._connected:
            self._connected = True
            self._callbacks = {}
            self.connect_count += 1

    async def disconnect(self) -> None:
        if self._connected:
            self._connected = False
            self._callbacks = {}
            self.disconnect_count += 1
            if self._on_disconnect is not None:
                self._on_disconnect()

    @property
    def is_connected(self) -> bool:
        return self._connected

    @property
    def mtu(self) -> int:
        return self._mtu

    def properties(self, characteristic: str) -> frozenset[str]:
        return self._characteristics.get(characteristic, frozenset())

    async def write(self, characteristic: str, data: bytes, response: bool) -> None:
        if not self._connected:
            raise CameraDisconnected(f"Not connected to the camera. {LINK_LOST_HELP}")
        if characteristic not in self._characteristics:
            raise CameraError(f"The camera has no Bluetooth characteristic {characteristic[4:8].upper()}.")
        data = bytes(data)
        if len(data) > self._mtu - ATT_HEADER:
            raise CameraError(
                f"write of {len(data)} bytes exceeds what the link carries in one write ({self._mtu - ATT_HEADER})"
            )
        self.writes.append(RecordedWrite(characteristic, data, response))
        if self.on_write is not None:
            result = self.on_write(self, characteristic, data, response)
            if inspect.isawaitable(result):
                await result

    async def subscribe(self, characteristic: str, callback: NotifyCallback) -> None:
        if not self._connected:
            raise CameraDisconnected(f"Not connected to the camera. {LINK_LOST_HELP}")
        if characteristic not in self._characteristics:
            raise CameraError(f"The camera has no Bluetooth characteristic {characteristic[4:8].upper()}.")
        self._callbacks[characteristic] = callback

    # -- test controls ------------------------------------------------------------------

    @property
    def subscriptions(self) -> frozenset[str]:
        """Characteristics that currently have notifications enabled."""
        return frozenset(self._callbacks)

    def written(self, characteristic: str | None = None) -> bytes:
        """All bytes written so far (to one characteristic, or to any), concatenated."""
        return b"".join(w.data for w in self.writes if characteristic in (None, w.characteristic))

    def feed(self, data: bytes, characteristic: str = CHAR_NOTIFY, *, sizes: int | Sequence[int] | None = None) -> None:
        """Deliver ``data`` as notifications now.

        ``sizes`` chooses the packetisation: ``None`` one notification, an int that
        many bytes per notification, a sequence the successive notification sizes
        (whatever remains goes into a final one).  Nothing is delivered when the
        link is down or the characteristic has no subscriber, as on a real link.
        """
        callback = self._callbacks.get(characteristic)
        if not self._connected or callback is None:
            return
        data = bytes(data)
        if sizes is None:
            pieces = [data]
        elif isinstance(sizes, int):
            pieces = split_for_write(data, sizes)
        else:
            pieces, offset = [], 0
            for size in sizes:
                if offset >= len(data):
                    break
                pieces.append(data[offset : offset + size])
                offset += size
            if offset < len(data):
                pieces.append(data[offset:])
        for piece in pieces:
            callback(piece)

    def feed_later(
        self, data: bytes, characteristic: str = CHAR_NOTIFY, *, delay: float = 0.0,
        sizes: int | Sequence[int] | None = None,
    ) -> None:  # fmt: skip
        """Like :meth:`feed`, but from the event loop after ``delay`` seconds (0 = on its next turn)."""
        loop = asyncio.get_running_loop()
        if delay > 0:
            loop.call_later(delay, lambda: self.feed(data, characteristic, sizes=sizes))
        else:
            loop.call_soon(lambda: self.feed(data, characteristic, sizes=sizes))

    def drop(self) -> None:
        """Simulate the camera going away (switched off, out of range)."""
        if self._connected:
            self._connected = False
            self._callbacks = {}
            if self._on_disconnect is not None:
                self._on_disconnect()
