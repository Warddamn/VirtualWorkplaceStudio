"""State-machine tests of videonotes.dji.camera / videonotes.dji.transport against a scripted camera.

``SimCamera`` plays the camera's side of both protocols on a ``FakeTransport``.  Its
frames are the ones captured from real cameras where captures exist (the R SDK
handshake and status pushes of an Osmo Action 4 / Osmo Action 5 Pro from upstream
issue #5, the DUML replies of the DJI Mimo btsnoop) and otherwise follow the layouts
of the research reports rsdk_ble.md and livestream_ble.md.
"""

from __future__ import annotations

import asyncio
import dataclasses
import inspect
import json
import logging
import struct
import sys
import threading
import time
from types import SimpleNamespace

import pytest

from videonotes.backends.base import BackendUnavailable
from videonotes.dji import camera as cam
from videonotes.dji import duml, rsdk, transport
from videonotes.dji.camera import (
    CameraDisconnected,
    CameraError,
    CameraNotFound,
    CameraStatus,
    CameraTimeout,
    CommandRejected,
    Identity,
    LivestreamFailed,
    OsmoCamera,
    PairingRejected,
    PairingTimeout,
    SyncCamera,
    Timeouts,
    WifiJoinFailed,
    run_sync,
)
from videonotes.dji.transport import (
    CHAR_FFF3,
    CHAR_NOTIFY,
    CHAR_WRITE,
    SERVICE_UUID,
    BleakTransport,
    BluetoothUnavailable,
    FakeTransport,
    FoundCamera,
)


def hx(text: str) -> bytes:
    return bytes.fromhex(text.replace("\n", " "))


# frames captured from real cameras (rsdk_ble.md §5.1.1, §6.5, §6.6; rsdk_ble_issue5_verify.py)
OA4_STEP2 = hx("aa 1b 00 20 00 00 00 00 00 01 a4 7c 00 19 33 ff 00 00 00 00 00 00 00 5e 76 2f 9b")
OA4_STEP3 = hx(
    "aa 33 00 02 00 00 00 00 73 00 bc 8f 00 19 33 ff"
    + " 00" * 16
    + " 00 00 00 00 00 00 00 00 02 00 00 00 00 00 00 0d 64 a7 26"
)
OA5_STEP2 = hx("aa 1b 00 20 00 00 00 00 00 01 a4 7c 00 19 44 ff 00 00 00 00 00 00 00 42 d8 ed 0f")
OA5_STEP3 = hx(
    "aa 33 00 02 00 00 00 00 01 00 98 2f 00 19 44 ff"
    + " 00" * 16
    + " 00 00 00 00 00 00 00 00 02 00 00 00 00 00 00 e1 ea 9c 15"
)
SUBSCRIBE_RESPONSE = hx("aa 17 00 20 00 00 00 00 00 03 70 bd 1d 05 00 00 00 00 00 66 46 32 67")
OA4_STATUS = hx(
    "aa 31 00 01 00 00 00 00 56 3b cd ac 1d 02 01 01 10 03 01 00 00 00 00 00 00 00 00 00 00 d4 db 01"
    " 00 00 00 00 00 ea 27 00 00 00 00 00 00 b6 67 66 4b"
)
OA5_STATUS = hx(
    "aa 38 00 01 00 a1 49 00 b4 7e 85 2a 1d 02 05 01 04 01 00 00 00 00 01 00 00 00 00 00 00 59 db 01"
    " 00 ab 8f 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 5c e9 7b eb 94"
)
# frames captured from DJI Mimo <-> camera (livestream_ble.md §5.1, §5.8)
PAIR_APPROVED_REQUEST = hx("55 0e 04 66 07 02 04 00 40 07 46 01 10 73")
PAIR_APPROVED_ACK = hx("55 0e 04 66 02 07 04 00 c0 07 46 00 35 28")
BATTERY_PUSH_88 = hx("552f046305024d01000d020086100000ce010000000000000000000036010058000000000000200400000001018df2")

DEVICE_IDS = {"action4": 0xFF33, "action5pro": 0xFF44}

SSID, PASSWORD, URL = "HomeNet", "correct horse", "rtmp://192.168.1.10:1935/live/cam"
STREAM = dict(ssid=SSID, password=PASSWORD, rtmp_url=URL, resolution="1080p", bitrate_kbps=4000, fps=30)


def fast_timeouts(**overrides) -> Timeouts:
    values = dict(
        command=0.3, pair_answer=0.3, pair=0.6, status=0.25, record_confirm=0.25,
        step=0.25, pair_reply=0.12, pair_approval=1.0, pair_resend=0.15, cleanup_stop=0.1, wifi=0.3,
        confirm_resend=0.12, start_confirm=0.3, refusal_grace=0.1, live_first=0.15, live_confirm=0.5,
        stop=0.25, abort_stop=0.15, reconnect_pause=0.0, frame_gap=0.0, chunk_gap=0.0,
    )  # fmt: skip
    values.update(overrides)
    return Timeouts(**values)


def new_identity(**overrides) -> Identity:
    values = dict(
        rsdk_device_id=0x12345678, rsdk_mac=bytes.fromhex("383456789ABC"), rsdk_code=1234,
        duml_identifier="0123456789abcdef0123456789abcdef", duml_pin="4321",
    )  # fmt: skip
    values.update(overrides)
    return Identity(**values)


class SimCamera:
    """The camera's side of the conversation, attached to a FakeTransport."""

    def __init__(self, link: FakeTransport, *, model: str = "action4", **options) -> None:
        self.link = link
        self.model = model
        link.on_write = self.on_write
        self.rsdk_rx = rsdk.Reassembler()
        self.duml_rx = duml.Reassembler()
        self.rsdk_log: list[rsdk.Frame] = []  # what the controller sent, decoded
        self.duml_log: list[tuple[str, duml.Frame]] = []  # (characteristic, frame)
        self.sizes: int | None = None  # packetisation of our notifications
        self.reply_char = CHAR_NOTIFY
        self.immediate = False  # deliver notifications inside write() instead of on the next loop turn
        # R SDK behaviour
        self.pair_mode = "accept"  # accept | no_step2 | ack_only | silent | reject | error | duml_only
        self.captured_handshake = False  # answer with the frames captured from real cameras (SEQ 0x0100)
        self.record_code: int | None = 0  # None = do not answer record commands
        self.recording = False
        self.push_status = True  # send a status push after the subscription and after record commands
        self.status_changes: dict[str, int] = {}  # payload bytes to override in every push: {"b30": 2}
        self.subscriptions = 0
        self.rsdk_paired = False
        # DUML behaviour
        self.duml_pair = "paired"  # paired | approve | deny | never | silent | fff3
        self.approve_after = 0.03
        self.answer_stop = True
        self.prepare_code: int | None = 0
        self.wifi_reply: bytes | None = b"\x00\x00"
        self.wifi_delay = 0.0
        self.eis_code: int | None = 0
        self.start_codes: dict[str, int | None] = {}  # layout -> reply code; default 0
        self.confirm_code: int | None = 0
        self.ignore_confirms = 0  # swallow this many start confirms (as if written too early)
        self.live_states: list[bytes] = []  # EE/03 payloads pushed after the start confirm was accepted
        self.live_before_start: bytes | None = None  # EE/03 payload pushed after "prepare"
        self.streaming = False
        self.in_live_mode = False
        self.wifi: tuple[str, str] | None = None
        for key, value in options.items():
            assert hasattr(self, key), key
            setattr(self, key, value)

    # -- plumbing ---------------------------------------------------------------------------

    def notify(self, raw: bytes, *, delay: float = 0.0, characteristic: str | None = None) -> None:
        target = characteristic or self.reply_char
        if self.immediate and not delay:
            self.link.feed(raw, target, sizes=self.sizes)
        else:
            self.link.feed_later(raw, target, delay=delay, sizes=self.sizes)

    def on_write(self, link: FakeTransport, characteristic: str, data: bytes, response: bool) -> None:
        for frame in self.rsdk_rx.feed(data):
            self.rsdk_log.append(frame)
            self.handle_rsdk(frame)
        for dframe in self.duml_rx.feed(data):
            self.duml_log.append((characteristic, dframe))
            self.handle_duml(characteristic, dframe)

    def duml_frames(self, *, keepalive: bool = False) -> list[duml.Frame]:
        return [f for _, f in self.duml_log if keepalive or f.command != duml.CMD_SESSION]

    def duml_commands(self) -> list[str]:
        return [describe(f) for f in self.duml_frames()]

    # -- R SDK ------------------------------------------------------------------------------

    def status_frame(self, **changes) -> bytes:
        base = OA4_STATUS if self.model == "action4" else OA5_STATUS
        payload = bytearray(rsdk.Frame.decode(base).payload)
        payload[1] = 3 if self.recording else 1
        for offset, value in {**self.status_changes, **changes}.items():
            payload[int(offset.lstrip("b"))] = value
        return rsdk.Frame(0x1D, 0x02, bytes(payload), 0x01, 0x3B56).encode()

    def handle_rsdk(self, frame: rsdk.Frame) -> None:
        device_id = DEVICE_IDS[self.model]
        if frame.command == rsdk.CMD_CONNECT and not frame.is_response:
            mode = self.pair_mode
            if mode == "silent":
                return
            if mode == "duml_only":  # an Action 5 Pro that did not accept the request only chatters in DUML
                self.notify(BATTERY_PUSH_88)
                return
            if self.captured_handshake:
                assert frame.seq == 0x0100, "the captured frames echo SEQ bytes 00 01"
                self.notify(OA4_STEP2 if self.model == "action4" else OA5_STEP2)
                self.notify(OA4_STEP3 if self.model == "action4" else OA5_STEP3)
                return
            if mode != "no_step2":
                code = 2 if mode == "error" else 0
                step2 = rsdk.Frame(0x00, 0x19, rsdk.ConnectResponse(device_id, code).pack(), 0x20, frame.seq)
                self.notify(step2.encode())
            if mode in ("accept", "no_step2", "reject"):
                verdict = 1 if mode == "reject" else 0
                step3 = rsdk.Frame(0x00, 0x19, rsdk.ConnectRequest(device_id, b"", 2, verdict).pack(), 0x02, 0x0073)
                self.notify(step3.encode())
        elif frame.command == rsdk.CMD_CONNECT:  # step 4
            self.rsdk_paired = True
        elif frame.command == rsdk.CMD_STATUS_SUBSCRIBE:
            self.subscriptions += 1
            self.notify(rsdk.Frame(0x1D, 0x05, bytes(5), 0x20, frame.seq).encode())  # undocumented but real (§6.5)
            if self.push_status:
                self.notify(self.status_frame())
        elif frame.command == rsdk.CMD_RECORD:
            start = frame.payload[4] == 0
            if self.record_code == 0 or self.record_code is None:
                self.recording = start
            if self.push_status:
                # a push that reuses the controller's SEQ must not be mistaken for the response (§3.4)
                push = rsdk.Frame.decode(self.status_frame())
                self.notify(rsdk.Frame(0x1D, 0x02, push.payload, 0x01, frame.seq).encode())
            if self.record_code is not None:
                reply = rsdk.Frame(0x1D, 0x03, bytes([self.record_code, 0, 0, 0, 0]), 0x20, frame.seq)
                self.notify(reply.encode())
        elif frame.command == rsdk.CMD_VERSION:
            payload = struct.pack("<H16s", 0, b"DJI-ACTION4") + b"SDK-v1.1 DEBUG AC203-03.04.80.15" + bytes(46)
            self.notify(rsdk.Frame(0x00, 0x00, payload, 0x20, frame.seq).encode())

    # -- DUML -------------------------------------------------------------------------------

    def reply(self, request: duml.Frame, payload: bytes, flags: int = 0xC0, *, delay: float = 0.0) -> None:
        self.notify(duml.ack(request, payload, flags).encode(), delay=delay)

    def push_live(self, payload: bytes, *, delay: float = 0.0) -> None:
        self.notify(duml.Frame(duml.VIDEO, duml.APP, b"\x00\x00", 0x80, 0xEE, 0x03, payload).encode(), delay=delay)

    def handle_duml(self, characteristic: str, frame: duml.Frame) -> None:
        if frame.is_response:
            return
        command = frame.command
        if command == duml.CMD_PAIR:
            mode = self.duml_pair
            if mode == "silent" or (mode == "fff3" and characteristic != CHAR_FFF3):
                return
            if mode in ("paired", "fff3"):
                self.reply(frame, b"\x00\x01")
                return
            self.reply(frame, b"\x00\x02")
            if mode in ("approve", "deny") and self.approve_after is not None:
                verdict = b"\x01" if mode == "approve" else b"\x00"
                request = duml.Frame(duml.WIFI, duml.APP, b"\x04\x00", 0x40, 0x07, 0x46, verdict)
                assert mode == "deny" or request.encode() == PAIR_APPROVED_REQUEST
                self.notify(request.encode(), delay=self.approve_after)
                self.approve_after = None  # once
        elif command == duml.CMD_PREPARE:
            if self.prepare_code is not None:
                self.in_live_mode = self.prepare_code == 0
                self.reply(frame, bytes([self.prepare_code]))
                if self.live_before_start is not None:
                    self.push_live(self.live_before_start)
        elif command == duml.CMD_SETUP_WIFI:
            ssid_len = frame.payload[0]
            ssid = frame.payload[1 : 1 + ssid_len].decode()
            password = frame.payload[2 + ssid_len :].decode()
            self.wifi = (ssid, password)
            if self.wifi_reply is not None:
                self.reply(frame, self.wifi_reply, delay=self.wifi_delay)
        elif command == duml.CMD_START_STREAMING:
            layout = (
                "json"
                if frame.payload[0] == 1
                else ("legacy" if frame.payload[1] == len(frame.payload) - 3 else "legacy-fixed")
            )
            code = self.start_codes.get(layout, 0)
            if code is not None:
                self.reply(frame, bytes([code]))
        elif command == duml.CMD_PARAMETER and frame.receiver == duml.CAMERA:  # stabilisation
            if self.eis_code is not None:
                self.reply(frame, bytes([self.eis_code]), 0x80)
        elif command == duml.CMD_PARAMETER and frame.payload == duml.PAYLOAD_STOP:
            self.streaming = self.in_live_mode = False
            if self.answer_stop:
                self.reply(frame, b"\x00", 0x80)
        elif command == duml.CMD_PARAMETER and frame.payload == duml.PAYLOAD_START_CONFIRM:
            if self.ignore_confirms > 0:
                self.ignore_confirms -= 1
                return
            if self.confirm_code is not None:
                self.reply(frame, bytes([self.confirm_code]), 0x80)
                if self.confirm_code == 0:
                    self.streaming = True
                    for index, state in enumerate(self.live_states):
                        self.push_live(state, delay=0.02 * (index + 1))
                    self.live_states = []


def describe(frame: duml.Frame) -> str:
    names = {
        duml.CMD_SESSION: "session", duml.CMD_PAIR: "pair", duml.CMD_PAIR_APPROVED: "ack-approval",
        duml.CMD_PREPARE: "prepare", duml.CMD_SETUP_WIFI: "wifi", duml.CMD_START_STREAMING: "start",
    }  # fmt: skip
    if frame.command == duml.CMD_PARAMETER:
        if frame.receiver == duml.CAMERA:
            return "eis"
        return {duml.PAYLOAD_STOP: "stop", duml.PAYLOAD_START_CONFIRM: "confirm"}.get(frame.payload, "parameter")
    return names.get(frame.command, f"{frame.cmd_set:02x}/{frame.cmd_id:02x}")


def make(
    model: str = "action4", *, configured: str | None = None, mtu: int = 185, timeouts: Timeouts | None = None,
    keepalive: bool = False, identity: Identity | None = None, advertise: bool = True, **sim_options,
):  # fmt: skip
    """A FakeTransport, the simulated camera behind it, and an OsmoCamera on top."""
    advert = None
    if advertise:
        advert = FoundCamera("FAKE-0000-CAMERA", "Osmo", -50, model, duml.MODELS[model].name)
    link = FakeTransport(mtu=mtu, advertisement=advert)
    sim = SimCamera(link, model=model, **sim_options)
    camera = OsmoCamera(
        link.address, model=configured or "auto", transport=link, identity=identity or new_identity(),
        timeouts=timeouts or fast_timeouts(), keepalive=keepalive,
    )  # fmt: skip
    return camera, sim, link


async def connected(*args, **kwargs):
    camera, sim, link = make(*args, **kwargs)
    await camera.connect()
    return camera, sim, link


# =============================================================================================
# advertisement parsing and scanning
# =============================================================================================

# manufacturer data as bleak reports it: {company id: bytes after the company id}
# DJI's scan screenshots (rsdk_ble.md §2.2, livestream_ble.md §2.1)
OA4_ADVERT = {0x08AA: bytes.fromhex("1400FA60601F6011E7")}
OA5_ADVERT = {0x08AA: bytes.fromhex("1500FA60601FC7509600")}


def test_parse_advertisement_of_dji_screenshots():
    oa4 = transport.parse_advertisement("UUID-1", "OA4", -47, OA4_ADVERT)
    assert oa4 == FoundCamera("UUID-1", "OA4", -47, "action4", "Osmo Action 4", "60:60:1F:60:11:E7", True)
    oa5 = transport.parse_advertisement("UUID-2", "OA5Pro", -60, OA5_ADVERT)
    assert (oa5.model, oa5.model_name, oa5.mac, oa5.remote_control) == (
        "action5pro",
        "Osmo Action 5 Pro",
        "60:60:1F:C7:50:96",
        True,
    )
    # the MAC is the one the wake-up advertisement of the same camera carries, reversed (rsdk_ble.md §2.2)
    assert rsdk.wake_advertisement(bytes.fromhex(oa4.mac.replace(":", ""))) == bytes.fromhex("0AFF574B50E711601F6060")


def test_parse_advertisement_other_devices():
    parse = transport.parse_advertisement
    # Xtra rebadge (company 0xF7AA): recognised, but not by DJI's remote-control filter
    xtra = parse("U", None, None, {0xF7AA: bytes.fromhex("1500FA112233445566")})
    assert (xtra.model, xtra.name, xtra.rssi, xtra.remote_control) == ("action5pro", "", None, False)
    # Osmo Action 6 fixture of moblin; Osmo Nano without the FA marker (osmosis protocol map)
    assert parse("U", "x", -1, {0x08AA: bytes.fromhex("1800FA0C9AE6A0975600")}).model == "action6"
    nano = parse("U", "OsmoNano-C2D8", -1, {0x08AA: bytes.fromhex("19000060601F6011E703")})
    assert (nano.model, nano.remote_control, nano.mac) == ("nano", False, None)
    # a DJI device with an unknown model id is still listed, without a model
    unknown = parse("U", "Something", -70, {0x08AA: bytes.fromhex("7700FA000000000000")})
    assert unknown is not None and unknown.model is None and unknown.model_name is None and unknown.remote_control
    # short data: model only
    assert parse("U", "n", -1, {0x08AA: bytes.fromhex("1400")}) == FoundCamera("U", "n", -1, "action4", "Osmo Action 4")
    # not DJI: other company, no manufacturer data, a name that merely looks right
    assert parse("U", "OsmoAction4-0BA9", -40, {}) is None
    assert parse("U", "AirPods", -40, {0x004C: bytes.fromhex("1400FA60601F6011E7")}) is None
    assert parse("U", "x", -40, {0x08AA: b"\x14"}) is None
    # several entries: the DJI one is found
    assert parse("U", "x", -40, {0x004C: b"\x01\x02", 0x08AA: OA4_ADVERT[0x08AA]}).model == "action4"


def test_scan_service_filter_only_where_macos_needs_it():
    assert transport.scan_service_filter("12.0") == [SERVICE_UUID]
    assert transport.scan_service_filter("12.2.1") == [SERVICE_UUID]
    for version in ("12.3", "11.7.10", "13.6", "15.1", "26.0", "27.2", "", "unknown"):
        assert transport.scan_service_filter(version) is None
    assert transport.scan_service_filter() in (None, [SERVICE_UUID])  # whatever this machine is


def test_bluetooth_unavailable_messages(monkeypatch):
    assert transport.terminal_app_name({"TERM_PROGRAM": "Apple_Terminal"}) == "Terminal"
    assert transport.terminal_app_name({"TERM_PROGRAM": "iTerm.app"}) == "iTerm"
    assert transport.terminal_app_name({}) == "your terminal app"
    monkeypatch.setenv("TERM_PROGRAM", "Apple_Terminal")
    denied = transport.bluetooth_unavailable("DENIED_BY_USER")
    assert isinstance(denied, BluetoothUnavailable) and isinstance(denied, CameraError)
    assert "System Settings → Privacy & Security → Bluetooth" in str(denied) and "Terminal" in str(denied)
    assert "switched off" in str(transport.bluetooth_unavailable("POWERED_OFF"))
    assert "no usable Bluetooth" in str(transport.bluetooth_unavailable("NO_BLUETOOTH"))
    assert "restricted" in str(transport.bluetooth_unavailable("denied_by_system"))
    assert "Allow" in str(transport.bluetooth_unavailable("PERMISSION_TIMEOUT"))
    assert "try again" in str(transport.bluetooth_unavailable("UNKNOWN", "detail")) and "detail" in str(
        transport.bluetooth_unavailable("UNKNOWN", "detail")
    )


class FakeScanner:
    """Stands in for bleak.BleakScanner: replays (device, advertisement) pairs once started."""

    adverts: list[tuple[str, str | None, dict[int, bytes], int, str | None]] = []
    start_error: Exception | None = None
    instances: list[FakeScanner] = []

    def __init__(self, detection_callback=None, service_uuids=None, **kwargs):
        assert not kwargs, kwargs
        self.callback = detection_callback
        self.service_uuids = service_uuids
        self.started = self.stopped = False
        FakeScanner.instances.append(self)

    async def start(self):
        if FakeScanner.start_error is not None:
            raise FakeScanner.start_error
        self.started = True
        loop = asyncio.get_running_loop()
        for address, device_name, manufacturer_data, rssi, local_name in FakeScanner.adverts:
            device = SimpleNamespace(address=address, name=device_name, details=None)
            advert = SimpleNamespace(local_name=local_name, manufacturer_data=manufacturer_data, rssi=rssi)
            loop.call_soon(self.callback, device, advert)

    async def stop(self):
        self.stopped = True


@pytest.fixture()
def fake_scanner():
    FakeScanner.adverts, FakeScanner.start_error, FakeScanner.instances = [], None, []
    yield FakeScanner
    FakeScanner.adverts, FakeScanner.start_error, FakeScanner.instances = [], None, []


async def test_scan_recognises_cameras(fake_scanner):
    fake_scanner.adverts = [
        ("UUID-PHONE", "iPhone", {0x004C: b"\x10\x05\x01"}, -30, None),
        ("UUID-OA4", None, OA4_ADVERT, -71, None),  # advertisement first ...
        ("UUID-OA4", "OsmoAction4-EF63", {}, -65, "OsmoAction4-EF63"),  # ... scan response with the name later
        ("UUID-OA5", "Osmo5Seagrass1", OA5_ADVERT, -48, "Osmo5Seagrass1"),
        ("UUID-NAMEONLY", "OsmoAction4-FAKE", {}, -20, "OsmoAction4-FAKE"),  # the name alone proves nothing
    ]
    found = await cam.scan(timeout=0.05, scanner_factory=fake_scanner)
    assert [(c.address, c.name, c.rssi, c.model) for c in found] == [
        ("UUID-OA5", "Osmo5Seagrass1", -48, "action5pro"),
        ("UUID-OA4", "OsmoAction4-EF63", -65, "action4"),
    ]
    assert found[1].mac == "60:60:1F:60:11:E7" and all(isinstance(c, FoundCamera) for c in found)
    scanner = fake_scanner.instances[-1]
    assert scanner.started and scanner.stopped
    assert scanner.service_uuids == transport.scan_service_filter()
    # name filter: case-insensitive substring of the name
    assert [c.address for c in await cam.scan(0.02, "seagrass", scanner_factory=fake_scanner)] == ["UUID-OA5"]
    assert await cam.scan(0.02, "gopro", scanner_factory=fake_scanner) == []
    fake_scanner.adverts = []
    assert await cam.scan(0.01, scanner_factory=fake_scanner) == []


async def test_scan_reports_bluetooth_problems(fake_scanner, monkeypatch):
    from bleak.exc import BleakBluetoothNotAvailableError, BleakBluetoothNotAvailableReason, BleakError

    fake_scanner.start_error = BleakBluetoothNotAvailableError(
        "denied", BleakBluetoothNotAvailableReason.DENIED_BY_USER
    )
    with pytest.raises(BluetoothUnavailable, match="Privacy & Security → Bluetooth"):
        await cam.scan(0.01, scanner_factory=fake_scanner)
    fake_scanner.start_error = BleakBluetoothNotAvailableError("off", BleakBluetoothNotAvailableReason.POWERED_OFF)
    with pytest.raises(BluetoothUnavailable, match="switched off"):
        await cam.scan(0.01, scanner_factory=fake_scanner)
    fake_scanner.start_error = BleakError("something else")
    with pytest.raises(CameraError, match="something else"):
        await cam.scan(0.01, scanner_factory=fake_scanner)


async def test_scan_waits_for_the_permission_dialog(caplog):
    class SlowScanner(FakeScanner):
        async def start(self):
            await asyncio.sleep(3600)  # the user never answers the macOS dialog

    caplog.set_level(logging.WARNING, logger="videonotes.dji")
    started = time.monotonic()
    with pytest.raises(BluetoothUnavailable, match="did not grant Bluetooth access"):
        await transport._start_scanner(SlowScanner(lambda d, a: None), permission_timeout=0.05, notice_after=0.05)
    assert time.monotonic() - started < 3
    assert "choose Allow" in caplog.text


async def test_missing_bleak_gives_install_hint(monkeypatch):
    monkeypatch.setitem(sys.modules, "bleak", None)  # makes `import bleak` raise ImportError
    with pytest.raises(BackendUnavailable, match=r"pip install 'videonotes\[ble\]'"):
        await cam.scan(0.01)
    camera = OsmoCamera("UUID-OA4")
    with pytest.raises(BackendUnavailable, match="bleak"):
        await camera.connect()
    await camera.disconnect()  # still safe


def test_importing_the_package_does_not_import_bleak():
    import subprocess

    code = (
        "import sys; import videonotes.dji.camera, videonotes.dji.transport; "
        "sys.exit(1 if 'bleak' in sys.modules else 0)"
    )
    assert subprocess.run([sys.executable, "-c", code], check=False).returncode == 0


# =============================================================================================
# BleakTransport against a fake bleak (and its calls against the installed bleak's signatures)
# =============================================================================================


class FakeBleakChar:
    def __init__(self, uuid, properties, client):
        self.uuid, self.properties, self._client = uuid, list(properties), client

    @property
    def max_write_without_response_size(self) -> int:
        return self._client._next_size()


class FakeBleakClient:
    instances: list[FakeBleakClient] = []
    connect_error: Exception | None = None
    chars = {
        CHAR_NOTIFY: ("read", "write", "notify", "indicate"),
        CHAR_WRITE: ("read", "write-without-response", "write", "notify", "indicate"),
    }
    sizes = [20, 20, 182]  # the write size grows shortly after connecting (bleak docs)

    def __init__(self, device, disconnected_callback=None, services=None, *, timeout=30):
        self.device, self.disconnected_callback, self.requested_services, self.timeout = (
            device,
            disconnected_callback,
            services,
            timeout,
        )
        self.is_connected = False
        self.writes: list[tuple[str, bytes, bool]] = []
        self.notify_callbacks: dict[str, object] = {}
        self._sizes = list(FakeBleakClient.sizes)
        self._chars = {uuid: FakeBleakChar(uuid, props, self) for uuid, props in FakeBleakClient.chars.items()}
        self.services = SimpleNamespace(get_characteristic=self._chars.get)
        FakeBleakClient.instances.append(self)

    def _next_size(self):
        return self._sizes.pop(0) if len(self._sizes) > 1 else self._sizes[0]

    async def connect(self):
        if FakeBleakClient.connect_error is not None:
            raise FakeBleakClient.connect_error
        self.is_connected = True

    async def disconnect(self):
        if self.is_connected:
            self.is_connected = False
            if self.disconnected_callback:
                self.disconnected_callback(self)

    async def start_notify(self, char, callback):
        assert isinstance(char, FakeBleakChar)
        self.notify_callbacks[char.uuid] = callback

    async def write_gatt_char(self, char, data, response=None):
        assert isinstance(char, FakeBleakChar) and isinstance(response, bool)
        if not self.is_connected:
            from bleak.exc import BleakError

            raise BleakError("disconnected")
        self.writes.append((char.uuid, bytes(data), response))


@pytest.fixture()
def fake_bleak(fake_scanner):
    FakeBleakClient.instances, FakeBleakClient.connect_error = [], None
    FakeBleakClient.sizes = [20, 20, 182]
    fake_scanner.adverts = [("UUID-OA4", "OsmoAction4-EF63", OA4_ADVERT, -55, "OsmoAction4-EF63")]
    yield SimpleNamespace(client=FakeBleakClient, scanner=fake_scanner)
    FakeBleakClient.instances, FakeBleakClient.connect_error = [], None


def bleak_transport(fake, address="uuid-oa4", **kwargs) -> BleakTransport:
    return BleakTransport(address, client_factory=fake.client, scanner_factory=fake.scanner, **kwargs)


async def test_bleak_transport_connects_and_talks(fake_bleak):
    link = bleak_transport(fake_bleak, scan_timeout=1.0)
    lost = []
    link.set_disconnect_handler(lambda: lost.append(True))
    assert not link.is_connected and link.mtu == 23 and link.properties(CHAR_WRITE) == frozenset()
    await link.connect()
    client = fake_bleak.client.instances[-1]
    assert link.is_connected and client.device.address == "UUID-OA4"  # matched case-insensitively, found by scanning
    assert client.requested_services == [SERVICE_UUID] and client.timeout == 20.0
    assert link.advertisement.model == "action4" and link.advertisement.name == "OsmoAction4-EF63"
    assert link.mtu == 185  # 182 + 3, after waiting for the size to grow from 20
    assert "write-without-response" in link.properties(CHAR_WRITE) and link.properties(CHAR_FFF3) == frozenset()
    received = []
    await link.subscribe(CHAR_NOTIFY, received.append)
    await link.subscribe(CHAR_NOTIFY, received.append)  # second call is a no-op, not a bleak ValueError
    client.notify_callbacks[CHAR_NOTIFY](None, bytearray(b"\xaa\x01"))
    assert received == [b"\xaa\x01"] and isinstance(received[0], bytes)
    await link.write(CHAR_WRITE, b"\x01\x02", True)
    await link.write(CHAR_WRITE, b"\x03", False)
    assert client.writes == [(CHAR_WRITE, b"\x01\x02", True), (CHAR_WRITE, b"\x03", False)]
    with pytest.raises(CameraError, match="FFF3"):
        await link.write(CHAR_FFF3, b"\x00", False)
    await link.connect()  # already connected: nothing happens
    assert len(fake_bleak.client.instances) == 1
    await link.disconnect()
    assert not link.is_connected and lost == [True]
    await link.disconnect()  # idempotent
    with pytest.raises(CameraDisconnected):
        await link.write(CHAR_WRITE, b"\x00", True)
    with pytest.raises(CameraDisconnected):
        await link.subscribe(CHAR_NOTIFY, received.append)


async def test_bleak_transport_camera_not_found(fake_bleak):
    link = bleak_transport(fake_bleak, address="UUID-SOMEONE-ELSE", scan_timeout=0.05)
    with pytest.raises(CameraNotFound, match="Switch it on and wake it") as info:
        await link.connect()
    assert "DJI Mimo" in str(info.value) and "Wireless Connection" in str(info.value)
    assert not link.is_connected and fake_bleak.client.instances == []
    assert fake_bleak.scanner.instances[-1].stopped


async def test_bleak_transport_connect_failures(fake_bleak):
    from bleak.exc import BleakError

    fake_bleak.client.connect_error = TimeoutError()
    with pytest.raises(CameraDisconnected, match="did not accept the Bluetooth connection"):
        await bleak_transport(fake_bleak, scan_timeout=0.5).connect()
    fake_bleak.client.connect_error = BleakError("failed to connect")
    with pytest.raises(CameraError, match="failed to connect"):
        await bleak_transport(fake_bleak, scan_timeout=0.5).connect()
    # a device without the DJI characteristics
    fake_bleak.client.connect_error = None
    original = dict(fake_bleak.client.chars)
    try:
        fake_bleak.client.chars = {CHAR_NOTIFY: ("notify",)}
        link = bleak_transport(fake_bleak, scan_timeout=0.5)
        with pytest.raises(CameraError, match="does not offer the DJI camera service"):
            await link.connect()
        assert not link.is_connected
    finally:
        fake_bleak.client.chars = original


async def test_bleak_transport_write_errors_are_translated(fake_bleak):
    link = bleak_transport(fake_bleak, scan_timeout=0.5)
    await link.connect()
    client = fake_bleak.client.instances[-1]

    async def lost(char, data, response=None):
        from bleak.exc import BleakError

        raise BleakError("disconnected")

    client.write_gatt_char = lost
    with pytest.raises(CameraDisconnected, match="was lost"):
        await link.write(CHAR_WRITE, b"\x00", True)

    async def hangs(char, data, response=None):
        await asyncio.sleep(3600)

    client.write_gatt_char = hangs
    link._gatt_timeout = 0.05  # a write-with-response that the camera never acknowledges must not hang forever
    with pytest.raises(CameraDisconnected, match="did not respond"):
        await link.write(CHAR_WRITE, b"\x00", True)


def test_calls_match_the_installed_bleak_api():
    """The keyword arguments BleakTransport passes exist in the installed bleak (3.x)."""
    import bleak
    from bleak.backends.characteristic import BleakGATTCharacteristic
    from bleak.backends.scanner import AdvertisementData
    from bleak.exc import BleakBluetoothNotAvailableError, BleakBluetoothNotAvailableReason, BleakDeviceNotFoundError

    client = inspect.signature(bleak.BleakClient.__init__).parameters
    assert {"address_or_ble_device", "disconnected_callback", "services", "timeout"} <= set(client)
    assert client["timeout"].kind is inspect.Parameter.KEYWORD_ONLY
    assert list(inspect.signature(bleak.BleakClient.write_gatt_char).parameters)[1:] == [
        "char_specifier",
        "data",
        "response",
    ]
    assert list(inspect.signature(bleak.BleakClient.start_notify).parameters)[1:3] == ["char_specifier", "callback"]
    for name in ("connect", "disconnect", "is_connected", "services", "mtu_size"):
        assert hasattr(bleak.BleakClient, name)
    scanner = inspect.signature(bleak.BleakScanner.__init__).parameters
    assert {"detection_callback", "service_uuids"} <= set(scanner)
    assert inspect.iscoroutinefunction(bleak.BleakScanner.start) and inspect.iscoroutinefunction(
        bleak.BleakScanner.stop
    )
    assert {"local_name", "manufacturer_data", "rssi"} <= set(AdvertisementData._fields)
    assert isinstance(BleakGATTCharacteristic.max_write_without_response_size, property)
    assert isinstance(BleakGATTCharacteristic.properties, property)
    assert {"DENIED_BY_USER", "POWERED_OFF", "NO_BLUETOOTH", "DENIED_BY_SYSTEM"} <= set(
        BleakBluetoothNotAvailableReason.__members__
    )
    error = BleakBluetoothNotAvailableError("x", BleakBluetoothNotAvailableReason.DENIED_BY_USER)
    assert error.reason.name == "DENIED_BY_USER"
    assert isinstance(transport._translate_bleak_error(error, "testing"), BluetoothUnavailable)
    assert isinstance(
        transport._translate_bleak_error(BleakDeviceNotFoundError("id", "gone"), "testing"), CameraNotFound
    )


# =============================================================================================
# FakeTransport itself
# =============================================================================================


async def test_fake_transport_packetisation_and_limits():
    link = FakeTransport(mtu=23)
    got: list[bytes] = []
    await link.connect()
    await link.subscribe(CHAR_NOTIFY, got.append)
    data = bytes(range(50))
    link.feed(data)
    link.feed(data, sizes=20)
    link.feed(data, sizes=[1, 2, 100])
    link.feed(data, sizes=[5, 5])
    assert got == [
        data,
        data[:20],
        data[20:40],
        data[40:],
        data[:1],
        data[1:3],
        data[3:],
        data[:5],
        data[5:10],
        data[10:],
    ]
    link.feed(data, CHAR_WRITE)  # nobody subscribed there: dropped, as on a real link
    assert len(got) == 10
    await link.write(CHAR_WRITE, bytes(20), False)
    with pytest.raises(CameraError, match="exceeds"):
        await link.write(CHAR_WRITE, bytes(21), False)
    with pytest.raises(CameraError, match="characteristic"):
        await link.write("0000ffff-0000-1000-8000-00805f9b34fb", b"\x00", False)
    assert transport.split_for_write(bytes(45), 20) == [bytes(20), bytes(20), bytes(5)]
    assert transport.split_for_write(b"", 20) == [b""]
    assert await transport.write_chunked(link, CHAR_WRITE, bytes(45), response=False, gap=0) == 3
    assert link.written(CHAR_WRITE) == bytes(65) and [len(w.data) for w in link.writes] == [20, 20, 20, 5]
    lost = []
    link.set_disconnect_handler(lambda: lost.append(1))
    link.drop()
    assert not link.is_connected and lost == [1]
    link.feed(data)
    assert len(got) == 10
    with pytest.raises(CameraDisconnected):
        await link.write(CHAR_WRITE, b"\x00", False)
    link.connect_error = CameraNotFound("nope")
    with pytest.raises(CameraNotFound):
        await link.connect()
    await link.connect()
    assert link.is_connected and link.connect_count == 2 and link.subscriptions == frozenset()
    assert isinstance(link, transport.Transport)


# =============================================================================================
# R SDK: pairing
# =============================================================================================


@pytest.mark.parametrize(("model", "device_id"), [("action4", 0xFF33), ("action5pro", 0xFF44)])
async def test_pair_with_frames_captured_from_real_cameras(model, device_id, tmp_path):
    identity = Identity.load(tmp_path / "identity.json")
    identity.rsdk_device_id, identity.rsdk_mac, identity.rsdk_code = 0x12345678, bytes.fromhex("383456789ABC"), 1234
    camera, sim, link = await connected(model, identity=identity, advertise=False, captured_handshake=True)
    prompts: list[str] = []
    camera.on_prompt = prompts.append
    camera._seq = 0x00FF  # so that the request carries SEQ 0x0100, which the captured frames echo
    assert camera.model is None
    await camera.pair()
    assert link.subscriptions == {CHAR_NOTIFY}  # a remote-control session listens on FFF4 only, like DJI's demo
    step1, step4, subscribe = sim.rsdk_log
    # step 1: first pairing -> verify_mode 1, our persistent identity, fw_version 0, response required
    assert step1.command == rsdk.CMD_CONNECT and step1.cmd_type == 0x02 and step1.seq == 0x0100
    assert rsdk.ConnectRequest.unpack(step1.payload) == rsdk.ConnectRequest(
        0x12345678, bytes.fromhex("383456789ABC"), 1, 1234
    )
    # step 4: response frame that echoes the camera's SEQ (0x0073 Action 4, 0x0001 Action 5 Pro)
    camera_seq = 0x0073 if model == "action4" else 0x0001
    assert step4 == rsdk.Frame(0x00, 0x19, bytes.fromhex("78563412 00 00000000"), 0x20, camera_seq)
    # then the status subscription exactly as DJI's demo sends it (rsdk_ble.md EX5, with our SEQ)
    assert subscribe == rsdk.Frame(0x1D, 0x05, bytes.fromhex("031400000000"), 0x00, 0x0101)
    # every R SDK frame went out in one write, with response, to FFF5 (rsdk_ble.md §3.2-3.3)
    assert [(w.characteristic, w.response, len(w.data)) for w in link.writes] == [
        (CHAR_WRITE, True, 51),
        (CHAR_WRITE, True, 27),
        (CHAR_WRITE, True, 24),
    ]
    assert camera.model == model and sim.rsdk_paired  # from the device_id in the handshake
    assert prompts == ["Confirm the connection on the camera's screen. It should show the code 1234."]
    # the pairing is remembered: next time verify_mode 0 and no prompt
    saved = json.loads((tmp_path / "identity.json").read_text())
    assert saved["paired"] == [link.address] and saved["rsdk_code"] == 1234
    await camera.disconnect()
    again = OsmoCamera(link.address, transport=link, identity=tmp_path / "identity.json", timeouts=fast_timeouts())
    again.on_prompt = prompts.append
    sim.captured_handshake = False
    await again.connect()
    await again.pair()
    request = rsdk.ConnectRequest.unpack(sim.rsdk_log[3].payload)
    assert (request.verify_mode, request.verify_data, request.device_id) == (0, 1234, 0x12345678)
    assert len(prompts) == 1
    await again.pair()  # already paired on this link: nothing is sent
    assert len(sim.rsdk_log) == 6
    await again.disconnect()


@pytest.mark.parametrize("sizes", [1, 7, 20, [3, 9, 40]])
@pytest.mark.parametrize("immediate", [False, True])
async def test_pair_with_notifications_split_across_packets(sizes, immediate):
    camera, sim, link = await connected("action5pro", sizes=sizes, immediate=immediate)
    await camera.pair()
    assert sim.rsdk_paired and [f.command for f in sim.rsdk_log] == [(0, 0x19), (0, 0x19), (0x1D, 0x05)]
    status = await camera.status()
    assert status.battery_percent == 92
    await camera.disconnect()


async def test_pair_with_other_protocol_noise_between_the_frames():
    # an Osmo Action 5 Pro interleaves 0x55 frames (rsdk_ble.md §3.4); rsdk_ble_sketch_verify.py uses this noise
    camera, sim, link = await connected("action5pro", pair_mode="silent")
    task = asyncio.ensure_future(camera.pair())
    await asyncio.sleep(0.02)
    request = sim.rsdk_log[0]
    step2 = rsdk.Frame(0x00, 0x19, rsdk.ConnectResponse(0xFF44, 0).pack(), 0x20, request.seq).encode()
    device_info = duml.Frame(0x48, duml.APP, b"\x22\x03", 0x40, 0x00, 0x81, b"hg212" + bytes(20)).encode()
    stream = step2 + bytes.fromhex("55aa0102030405") + BATTERY_PUSH_88 + device_info + OA5_STEP3
    link.feed(stream, sizes=[10, 30, 3, 50, 9])
    await task
    assert sim.rsdk_paired and camera.model == "action5pro"
    assert sim.duml_log == []  # the camera's DUML request is not answered in a remote-control session
    assert camera._battery == 88  # ... but its battery push is understood (the R SDK status takes precedence)
    await camera.disconnect()


async def test_pair_without_step2_response():
    # rsdk_ble.md §5.1.1: the camera's command with verify_mode 2 completes the handshake even without step 2
    camera, sim, _ = await connected(pair_mode="no_step2")
    await camera.pair()
    assert sim.rsdk_paired and camera.model == "action4"
    await camera.disconnect()


async def test_pair_camera_silent():
    camera, sim, link = await connected(pair_mode="silent")
    started = time.monotonic()
    with pytest.raises(CameraTimeout, match="did not answer the pairing request") as info:
        await camera.pair()
    assert not isinstance(info.value, PairingTimeout)
    assert "DJI Mimo" in str(info.value) and "firmware" in str(info.value)
    assert 0.25 < time.monotonic() - started < 3
    assert len(sim.rsdk_log) == 2 and sim.rsdk_log[0] == sim.rsdk_log[1]  # the request was repeated once, unchanged
    assert camera.is_connected  # the caller decides what to do next
    await camera.disconnect()


async def test_pair_camera_answers_only_in_the_other_protocol():
    # rsdk_ble.md §3.3: "if the camera only ever sends 0x55 frames ... your request was not accepted"
    camera, sim, _ = await connected("action5pro", pair_mode="duml_only")
    with pytest.raises(CameraTimeout, match="other protocol"):
        await camera.pair()
    assert sim.duml_log == []  # and nothing is written in the other protocol during a remote-control session
    await camera.disconnect()


async def test_pair_waiting_for_the_user():
    identity = new_identity(paired=["FAKE-0000-CAMERA"])  # a known controller ...
    camera, sim, _ = await connected(pair_mode="ack_only", identity=identity, timeouts=fast_timeouts(pair=0.4))
    with pytest.raises(PairingTimeout, match=r"waiting for you to confirm the connection on its screen \(code 1234\)"):
        await camera.pair()
    assert rsdk.ConnectRequest.unpack(sim.rsdk_log[0].payload).verify_mode == 0
    assert len(sim.rsdk_log) == 1  # step 2 arrived, so the request was not repeated
    await camera.disconnect()


async def test_pair_prompts_when_a_known_camera_asks_again():
    identity = new_identity(paired=["FAKE-0000-CAMERA"])  # ... whose pairing the camera has forgotten
    timeouts = fast_timeouts(pair=0.5, pair_prompt_after=0.1)
    camera, sim, _ = await connected(pair_mode="ack_only", identity=identity, timeouts=timeouts)
    prompts: list[str] = []
    camera.on_prompt = prompts.append
    with pytest.raises(PairingTimeout):
        await camera.pair()
    assert prompts == ["Confirm the connection on the camera's screen. It should show the code 1234."]
    await camera.disconnect()


async def test_pair_rejected_on_the_camera():
    camera, sim, link = await connected(pair_mode="reject")
    with pytest.raises(PairingRejected, match="declined on the camera"):
        await camera.pair()
    # the docs: disconnect at once, do not answer, do not repeat
    assert not camera.is_connected and link.disconnect_count == 1
    assert [f.command for f in sim.rsdk_log] == [(0, 0x19)] and camera._identity().paired == []
    await camera.disconnect()


async def test_pair_refused_with_error_code():
    camera, sim, _ = await connected(pair_mode="error")
    with pytest.raises(PairingRejected, match="could not carry out the command") as info:
        await camera.pair()
    assert "reset the connection" in str(info.value)
    await camera.disconnect()


async def test_pair_link_lost_mid_handshake():
    camera, sim, link = await connected(pair_mode="ack_only", timeouts=fast_timeouts(pair=5.0))
    asyncio.get_running_loop().call_later(0.05, link.drop)
    with pytest.raises(CameraDisconnected, match="was lost"):
        await camera.pair()
    assert not camera.is_connected
    with pytest.raises(CameraDisconnected, match="not open"):
        await camera.pair()
    await camera.disconnect()


async def test_rsdk_frames_are_never_split():
    # rsdk_ble.md §3.3: a command that arrives in pieces is ignored by the camera, so we refuse to send it
    camera, sim, link = await connected(mtu=23)
    with pytest.raises(CameraError, match=r"only carries 20 bytes per write.*51-byte"):
        await camera.pair()
    assert link.writes == []
    await camera.disconnect()


async def test_not_connected_errors_and_safe_teardown():
    camera, sim, link = make()
    for call in (camera.pair, camera.start_recording, camera.stop_recording, camera.status, camera.version):
        with pytest.raises(CameraDisconnected, match="not open"):
            await call()
    with pytest.raises(CameraDisconnected):
        await camera.start_livestream(**STREAM)
    await camera.stop_livestream()  # safe in any state
    await camera.disconnect()
    await camera.disconnect()
    assert link.writes == [] and not camera.is_connected and not camera.is_livestreaming
    # connect errors propagate with their message and leave nothing half-open
    link.connect_error = CameraNotFound("The camera was not found over Bluetooth.")
    with pytest.raises(CameraNotFound):
        await camera.connect()
    assert not camera.is_connected
    await camera.connect()
    await camera.connect()  # idempotent
    assert link.connect_count == 1
    await camera.disconnect()


# =============================================================================================
# R SDK: recording and status
# =============================================================================================


async def test_start_and_stop_recording():
    camera, sim, link = await connected()
    await camera.pair()
    await camera.start_recording()
    start = sim.rsdk_log[-1]
    # rsdk_ble.md EX6: 1D 03, device_id constant of the demo, record_ctrl 0, response optional
    assert (
        start.command == (0x1D, 0x03)
        and start.cmd_type == 0x01
        and start.payload == bytes.fromhex("0000FF33 00 00000000")
    )
    assert sim.recording and (await camera.status()).recording is True
    await camera.stop_recording()
    stop = sim.rsdk_log[-1]
    assert stop.payload == bytes.fromhex("0000FF33 01 00000000") and stop.seq == start.seq + 1  # EX7
    assert not sim.recording and (await camera.status()).recording is False
    assert all(w.response and w.characteristic == CHAR_WRITE for w in link.writes)
    await camera.disconnect()


async def test_recording_pairs_first_when_needed():
    camera, sim, _ = await connected()
    await camera.start_recording()  # no explicit pair()
    assert [f.command for f in sim.rsdk_log] == [(0, 0x19), (0, 0x19), (0x1D, 0x05), (0x1D, 0x03)]
    await camera.disconnect()


async def test_recording_refused_by_the_camera():
    camera, sim, _ = await connected(record_code=2)
    await camera.pair()
    with pytest.raises(CommandRejected, match="refused to start recording") as info:
        await camera.start_recording()
    assert "could not carry out the command" in str(info.value) and "memory card" in str(info.value)
    with pytest.raises(CommandRejected, match="refused to stop recording"):
        await camera.stop_recording()
    await camera.disconnect()


async def test_recording_refusal_explains_from_the_status():
    hot_and_full = {"b30": 2, "b15": 0, "b16": 0, "b17": 0, "b18": 0}  # temp_over 2, remain_capacity 0
    camera, sim, link = await connected(record_code=2, status_changes=hot_and_full)
    await camera.pair()
    with pytest.raises(CommandRejected) as info:
        await camera.start_recording()
    assert "too hot to record" in str(info.value) and "memory card is full or missing" in str(info.value)
    await camera.disconnect()


async def test_recording_without_response_is_confirmed_by_status_push():
    # the response is optional (CmdType 0x01); a status push that shows the new state is accepted instead
    camera, sim, _ = await connected(record_code=None)
    await camera.pair()
    await camera.start_recording()
    assert sim.recording
    await camera.disconnect()


async def test_recording_no_response_and_no_status():
    camera, sim, _ = await connected(record_code=None, push_status=False)
    await camera.pair()
    with pytest.raises(CameraTimeout, match="did not answer the request to start recording"):
        await camera.start_recording()
    await camera.disconnect()


async def test_recording_link_lost_while_waiting():
    camera, sim, link = await connected(record_code=None, push_status=False, timeouts=fast_timeouts(command=5.0))
    await camera.pair()
    asyncio.get_running_loop().call_later(0.05, link.drop)
    with pytest.raises(CameraDisconnected):
        await camera.start_recording()
    await camera.disconnect()


async def test_status_of_an_action4_without_battery_field():
    camera, sim, _ = await connected("action4")
    status = await camera.status()  # pairs, subscribes, takes the first push (the captured 31-byte one)
    assert isinstance(status, CameraStatus)
    assert (status.model, status.mode, status.state, status.recording) == ("Osmo Action 4", "Video", "idle", False)
    assert (status.resolution, status.fps, status.stabilization) == ("4K 16:9", 30, "RockSteady")
    assert (status.card_free_mb, status.recording_time_left_s, status.temperature) == (121812, 10218, "normal")
    assert status.battery_percent is None and status.sleeping is False and status.livestreaming is False
    assert status.recording_seconds is None and status.photos_left is None
    assert status.raw["camera_mode"] == 1 and status.raw["camera_bat_percentage"] is None and len(status.raw) == 21
    assert camera.battery_percent is None
    await camera.disconnect()


async def test_status_of_an_action5pro():
    camera, sim, _ = await connected("action5pro")
    status = await camera.status()
    assert (status.model, status.mode, status.battery_percent) == ("Osmo Action 5 Pro", "Photo", 92)
    assert (status.resolution, status.fps, status.photos_left, status.card_free_mb) == ("L", None, 36779, 121689)
    assert camera.battery_percent == 92
    # a second call within the push interval reuses the fresh push; nothing else is written
    writes = len(sim.rsdk_log)
    await camera.status()
    assert len(sim.rsdk_log) == writes and sim.subscriptions == 1
    await camera.disconnect()


async def test_status_while_recording_and_livestream_mode():
    camera, sim, link = await connected("action5pro")
    await camera.pair()
    await asyncio.sleep(0)
    link.feed(sim.status_frame(b0=1, b1=3, b5=0x2C, b6=0x01), sizes=5)  # Video, recording, 300 s
    status = await camera.status()
    assert (status.mode, status.state, status.recording, status.recording_seconds) == ("Video", "recording", True, 300)
    link.feed(sim.status_frame(b0=0x1A))
    assert (await camera.status()).livestreaming is True
    await camera.disconnect()


async def test_status_camera_not_reporting():
    camera, sim, _ = await connected(push_status=False)
    with pytest.raises(CameraTimeout, match="not reporting its status"):
        await camera.status()
    assert sim.subscriptions == 2  # the subscription was repeated once before giving up
    await camera.disconnect()


async def test_version_query():
    camera, sim, _ = await connected()
    info = await camera.version()
    assert sim.rsdk_log[-1] == rsdk.Frame(0x00, 0x00, b"", 0x02, sim.rsdk_log[-1].seq)  # EX4 layout
    assert info.product_id == "DJI-ACTION4" and info.ack_result == 0
    await camera.disconnect()


async def test_sequence_numbers_wrap_like_the_demo():
    camera, _, _ = make()
    camera._seq = 0xFFFE
    assert [camera._next_seq() for _ in range(3)] == [0xFFFF, 1, 2]


# =============================================================================================
# livestream: the whole sequence
# =============================================================================================


def start_payload(sim: SimCamera) -> bytes:
    return next(f.payload for f in sim.duml_frames() if f.command == duml.CMD_START_STREAMING)


async def test_livestream_sequence_action4():
    camera, sim, link = await connected("action4")
    await camera.start_livestream(**STREAM)
    assert camera.is_livestreaming and sim.streaming and sim.wifi == (SSID, PASSWORD)
    # livestream_ble.md §5.0: session, pair, stop (clean-up), prepare, Wi-Fi, stabilisation, start, confirm
    frames = [f for _, f in sim.duml_log]
    assert [describe(f) for f in frames] == ["session", "pair", "stop", "prepare", "wifi", "eis", "start", "confirm"]
    expected = [
        duml.session_open(),
        duml.pair_request("4321", "0123456789abcdef0123456789abcdef"),
        duml.stop_streaming(),
        duml.prepare_livestream(),
        duml.setup_wifi(SSID, PASSWORD),
        duml.configure_stabilization(duml.MODELS["action4"], "off"),
        duml.start_streaming(duml.start_payload_legacy(URL, "1080p", 30, 4000)),
        duml.start_confirm(),
    ]
    assert frames == expected
    # byte-exact where the report gives complete frames (§5.2, §5.3, §5.7, §5.10)
    raw = link.written(CHAR_WRITE)
    assert raw.startswith(bytes.fromhex("550f04a202f01bcb40002b04009ab9"))
    for known in (
        "551304030208c8ea40028e01011a0001029219",
        "550e04660208128c4002e11a11df",
        "551304030208b4bb40028e01011a0001013238",
    ):
        assert bytes.fromhex(known) in raw
    assert frames[5].payload == bytes.fromhex("010108000100")  # Osmo Action 4: device byte 0x08
    # every livestream frame goes to FFF5 without response (livestream_ble.md §2.2), nothing in R SDK framing
    assert all(w.characteristic == CHAR_WRITE and not w.response for w in link.writes)
    assert sim.rsdk_log == [] and link.connect_count == 1
    assert link.subscriptions == {CHAR_NOTIFY, CHAR_WRITE}  # replies may come on either (livestream_ble.md §2.2)
    status = await camera.status()  # in a livestream session no request is sent for this
    assert (status.livestreaming, status.mode, status.model) == (True, "Live Streaming", "Osmo Action 4")
    assert len(sim.duml_log) == 8
    await camera.stop_livestream()
    assert not camera.is_livestreaming and not sim.streaming
    assert sim.duml_log[-1][1] == duml.stop_streaming()
    await camera.disconnect()
    assert describe(sim.duml_log[-1][1]) == "stop" and len(sim.duml_log) == 9  # no second stop on disconnect


async def test_livestream_sequence_action5pro():
    camera, sim, link = await connected(
        "action5pro",
        live_before_start=bytes.fromhex("0309"),
        live_states=[bytes.fromhex("0209"), bytes.fromhex("020805007017")],
    )
    await camera.start_livestream(**STREAM, stabilization="rocksteady")
    assert camera.is_livestreaming
    frames = sim.duml_frames()
    # livestream_ble.md §5.0/§5.7: on an Osmo Action 5 Pro the confirm is written right behind the start frame
    assert [describe(f) for f in frames] == ["pair", "stop", "prepare", "wifi", "eis", "start", "confirm"]
    assert frames[4].payload == bytes.fromhex("01011a000101")  # device byte 0x1A, RockSteady
    assert frames[5].payload == duml.start_payload_legacy(URL, "1080p", 30, 4000)
    await camera.disconnect()
    assert describe(sim.duml_log[-1][1]) == "stop" and not sim.streaming  # disconnect() stops a running stream first


async def test_livestream_confirm_behind_start_is_repeated_if_the_camera_missed_it():
    # dji-vcam: an Osmo Action 5 Pro "missed a start sent at once"; the confirm is written again after a pause
    camera, sim, _ = await connected("action5pro", ignore_confirms=1)
    await camera.start_livestream(**STREAM)
    assert [describe(f) for f in sim.duml_frames()][-3:] == ["start", "confirm", "confirm"]
    assert camera.is_livestreaming and sim.streaming
    await camera.disconnect()


async def test_livestream_unknown_model_uses_the_common_sequence():
    camera, sim, _ = await connected("action4", advertise=False)
    assert camera.model is None
    await camera.start_livestream(**STREAM)
    # no stabilisation step, legacy payload, confirm after the reply
    assert sim.duml_commands() == ["pair", "stop", "prepare", "wifi", "start", "confirm"]
    await camera.disconnect()


@pytest.mark.parametrize("mtu", [23, 30, 64])
async def test_livestream_frames_are_cut_to_the_mtu(mtu):
    # livestream_ble.md §9: write-without-response does not chunk; frames longer than the MTU must be cut
    camera, sim, link = await connected("action4", mtu=mtu, sizes=20)
    await camera.start_livestream(**STREAM)
    assert camera.is_livestreaming
    longest = max(len(w.data) for w in link.writes)
    assert longest == min(mtu - 3, 60)  # the longest frame here (start streaming) is 60 bytes
    assert sim.duml_commands() == ["pair", "stop", "prepare", "wifi", "eis", "start", "confirm"]  # reassembled intact
    await camera.disconnect()


@pytest.mark.parametrize("sizes", [1, 5, [2, 2, 2, 100]])
@pytest.mark.parametrize("immediate", [False, True])
async def test_livestream_with_split_notifications_and_replies_on_fff5(sizes, immediate):
    # livestream_ble.md §2.2: some bodies answer on FFF5; replies may arrive in any packetisation
    camera, sim, link = await connected("action5pro", sizes=sizes, immediate=immediate, reply_char=CHAR_WRITE)
    await camera.start_livestream(**STREAM)
    assert camera.is_livestreaming
    await camera.stop_livestream()
    await camera.disconnect()


async def test_livestream_first_pairing_needs_confirmation_on_the_camera():
    camera, sim, link = await connected("action4", duml_pair="approve")
    prompts: list[str] = []
    camera.on_prompt = prompts.append
    await camera.start_livestream(**STREAM)
    assert prompts == ["Confirm the pairing request on the camera's screen (it shows the code 4321)."]
    # the camera's 40 07 46 request is answered exactly as DJI Mimo does (livestream_ble.md §5.1)
    assert PAIR_APPROVED_ACK in link.written(CHAR_WRITE)
    commands = sim.duml_commands()
    assert (
        commands[0] == "pair"
        and "ack-approval" in commands
        and commands[-6:] == ["stop", "prepare", "wifi", "eis", "start", "confirm"]
    )
    await camera.disconnect()


async def test_livestream_pairing_keeps_asking_while_the_user_is_away():
    camera, sim, _ = await connected(duml_pair="approve", approve_after=0.4, timeouts=fast_timeouts(pair_resend=0.1))
    await camera.start_livestream(**STREAM)
    assert sim.duml_commands().count("pair") >= 3  # the request is repeated so that the link does not idle
    await camera.disconnect()


async def test_livestream_pairing_never_confirmed():
    camera, sim, _ = await connected(duml_pair="never", timeouts=fast_timeouts(pair_approval=0.5))
    with pytest.raises(PairingTimeout, match=r"confirm the pairing request on its screen \(code 4321\)"):
        await camera.start_livestream(**STREAM)
    assert set(sim.duml_commands()) == {"pair"} and not camera.is_livestreaming
    assert camera.is_connected
    await camera.disconnect()
    assert set(sim.duml_commands()) == {"pair"}  # the camera never entered Live Streaming mode: no stop needed


async def test_livestream_pairing_declined():
    camera, sim, _ = await connected(duml_pair="deny")
    with pytest.raises(PairingRejected, match="not confirmed on the camera"):
        await camera.start_livestream(**STREAM)
    await camera.disconnect()


async def test_livestream_pairing_unanswered_tries_fff3_then_gives_up():
    camera, sim, link = await connected(duml_pair="silent")
    with pytest.raises(CameraTimeout, match="did not answer the livestream pairing request") as info:
        await camera.start_livestream(**STREAM)
    assert "DJI Mimo" in str(info.value)
    pairs = [(c, f) for c, f in sim.duml_log if f.command == duml.CMD_PAIR]
    assert [c for c, _ in pairs] == [CHAR_WRITE] * 3 + [CHAR_FFF3] * 3  # livestream_ble.md §2.3 fallback
    # FFF3 has no write-without-response property here, so it is written with response
    assert {w.response for w in link.writes if w.characteristic == CHAR_FFF3} == {True}
    await camera.disconnect()


async def test_livestream_on_a_body_that_only_listens_on_fff3():
    camera, sim, link = await connected(duml_pair="fff3")
    await camera.start_livestream(**STREAM)
    assert camera.is_livestreaming
    assert {c for c, f in sim.duml_log if f.command != duml.CMD_SESSION and f.command != duml.CMD_PAIR} == {CHAR_FFF3}
    await camera.disconnect()


async def test_livestream_when_fff5_cannot_notify():
    chars = dict(transport.DEFAULT_FAKE_CHARACTERISTICS)
    chars[CHAR_WRITE] = frozenset({"write-without-response", "write"})
    link = FakeTransport(characteristics=chars)
    SimCamera(link)
    camera = OsmoCamera(
        link.address, transport=link, identity=new_identity(), timeouts=fast_timeouts(), keepalive=False
    )
    await camera.connect()
    await camera.start_livestream(**STREAM)
    assert link.subscriptions == {CHAR_NOTIFY} and camera.is_livestreaming
    await camera.disconnect()


async def test_livestream_without_fff3_does_not_try_it():
    link = FakeTransport(
        characteristics={k: v for k, v in transport.DEFAULT_FAKE_CHARACTERISTICS.items() if k != CHAR_FFF3}
    )
    sim = SimCamera(link, duml_pair="silent")
    camera = OsmoCamera(
        link.address, transport=link, identity=new_identity(), timeouts=fast_timeouts(), keepalive=False
    )
    await camera.connect()
    with pytest.raises(CameraTimeout):
        await camera.start_livestream(**STREAM)
    assert len([1 for _, f in sim.duml_log if f.command == duml.CMD_PAIR]) == 3
    await camera.disconnect()


# =============================================================================================
# livestream: unhappy paths
# =============================================================================================


@pytest.mark.parametrize("reply", [b"\x01\xff", b"\x01\x00", b"\x00\x01", b"\x01"])
async def test_livestream_wifi_join_failure(reply):
    camera, sim, _ = await connected(wifi_reply=reply)
    with pytest.raises(WifiJoinFailed, match="could not join the Wi-Fi network 'HomeNet'") as info:
        await camera.start_livestream(**STREAM)
    text = str(info.value)
    assert reply.hex(" ") in text and "password" in text and "2.4 GHz or 5 GHz" in text and "WPA2" in text
    # the camera is told to leave Live Streaming mode again; the link stays up for the caller
    assert sim.duml_commands() == ["pair", "stop", "prepare", "wifi", "stop"]
    assert camera.is_connected and not camera.is_livestreaming and not sim.in_live_mode
    await camera.disconnect()
    assert sim.duml_commands().count("stop") == 2


async def test_livestream_wifi_reply_with_three_zero_bytes_is_success():
    camera, sim, _ = await connected(wifi_reply=bytes(3))  # captured from DJI Mimo (livestream_ble.md §5.4)
    await camera.start_livestream(**STREAM)
    assert camera.is_livestreaming
    await camera.disconnect()


async def test_livestream_wifi_slow_join_is_awaited():
    # an Osmo Action 5 Pro needs 10-14 s to join; scaled down here
    camera, sim, _ = await connected(wifi_delay=0.2, timeouts=fast_timeouts(wifi=0.5))
    await camera.start_livestream(**STREAM)
    assert sim.duml_commands().count("wifi") == 1
    await camera.disconnect()


async def test_livestream_wifi_no_answer():
    camera, sim, _ = await connected(wifi_reply=None)
    with pytest.raises(CameraTimeout, match="did not say whether it joined"):
        await camera.start_livestream(**STREAM)
    assert sim.duml_commands().count("wifi") == 2 and sim.duml_commands()[-1] == "stop"
    await camera.disconnect()


async def test_livestream_prepare_refused_or_unanswered():
    camera, sim, _ = await connected(prepare_code=0xE4)
    with pytest.raises(LivestreamFailed, match=r"refused to enter Live Streaming mode \(code 0xE4\)"):
        await camera.start_livestream(**STREAM)
    await camera.disconnect()
    camera, sim, _ = await connected(prepare_code=None)
    with pytest.raises(CameraTimeout, match="did not answer the request to enter Live Streaming mode"):
        await camera.start_livestream(**STREAM)
    assert sim.duml_commands().count("prepare") == 3
    await camera.disconnect()


async def test_livestream_cleanup_stop_and_stabilisation_may_go_unanswered():
    # livestream_ble.md §5.2 ("no reply is acceptable") and §5.5 (step of uncertain necessity)
    camera, sim, _ = await connected(answer_stop=False, eis_code=None)
    await camera.start_livestream(**STREAM)
    assert camera.is_livestreaming and sim.duml_commands().count("eis") == 2
    await camera.stop_livestream()  # unanswered stop: logged, not raised
    assert not camera.is_livestreaming
    await camera.disconnect()


async def test_livestream_start_refused():
    camera, sim, _ = await connected("action4", start_codes={"legacy": 0xD6, "legacy-fixed": 0xD6})
    with pytest.raises(LivestreamFailed, match="refused to start streaming") as info:
        await camera.start_livestream(**STREAM)
    assert "legacy: busy" in str(info.value) and "legacy-0x2e: busy" in str(info.value)
    assert sim.duml_commands()[-3:] == ["start", "start", "stop"] and not camera.is_livestreaming
    await camera.disconnect()


async def test_livestream_start_unanswered():
    camera, sim, _ = await connected("action4", start_codes={"legacy": None, "legacy-fixed": None})
    with pytest.raises(LivestreamFailed, match="legacy: no answer"):
        await camera.start_livestream(**STREAM)
    assert sim.duml_commands().count("start") == 4  # two layouts, two attempts each
    await camera.disconnect()


async def test_livestream_action5pro_falls_back_to_mimos_layout():
    camera, sim, _ = await connected("action5pro", start_codes={"legacy": 0xD6})
    await camera.start_livestream(**STREAM)
    starts = [f.payload for f in sim.duml_frames() if f.command == duml.CMD_START_STREAMING]
    assert starts == [
        duml.start_payload_legacy(URL, "1080p", 30, 4000),
        duml.start_payload_mimo_json(URL, "1080p", 4000),
    ]
    assert camera.is_livestreaming
    await camera.disconnect()


async def test_livestream_action4_falls_back_to_the_hard_coded_length():
    camera, sim, _ = await connected("action4", start_codes={"legacy": 0x01})
    await camera.start_livestream(**STREAM)
    starts = [f.payload for f in sim.duml_frames() if f.command == duml.CMD_START_STREAMING]
    assert starts[-1] == duml.start_payload_legacy(URL, "1080p", 30, 4000, length_override=0x2E) and len(starts) == 2
    await camera.disconnect()


async def test_livestream_camera_reports_failure_after_start():
    # dji-vcam: "02 79 failed (the camera then shows 'live stream failed')" -- e.g. the RTMP address is unreachable
    camera, sim, _ = await connected(
        "action5pro",
        live_before_start=bytes.fromhex("0309"),
        live_states=[bytes.fromhex("0209"), bytes.fromhex("0279")],
    )
    with pytest.raises(LivestreamFailed, match="reports that the livestream failed") as info:
        await camera.start_livestream(**STREAM)
    assert "same network" in str(info.value) and "Firewall" in str(info.value)
    assert sim.duml_commands()[-1] == "stop" and not camera.is_livestreaming
    await camera.disconnect()


async def test_livestream_camera_that_keeps_reporting_ready_is_taken_at_its_word(caplog):
    caplog.set_level(logging.WARNING, logger="videonotes.dji")
    camera, sim, _ = await connected(
        "action5pro", live_before_start=bytes.fromhex("0309"), live_states=[bytes.fromhex("0209")]
    )
    await camera.start_livestream(**STREAM)
    assert camera.is_livestreaming and "still reports 'ready, not streaming'" in caplog.text
    await camera.disconnect()


async def test_livestream_start_confirm_refused():
    # required on an Osmo Action 5 Pro: an explicit refusal is an error ...
    camera, sim, _ = await connected("action5pro", confirm_code=0xD6)
    with pytest.raises(LivestreamFailed, match=r"refused to start streaming \(busy\)"):
        await camera.start_livestream(**STREAM)
    await camera.disconnect()
    # ... on an Osmo Action 4 the stream is known to start from the start frame alone (moblin): only logged
    camera, sim, _ = await connected("action4", confirm_code=0xD6)
    await camera.start_livestream(**STREAM)
    assert camera.is_livestreaming
    await camera.disconnect()


async def test_livestream_start_confirm_unanswered_is_not_fatal():
    camera, sim, _ = await connected("action5pro", confirm_code=None)
    await camera.start_livestream(**STREAM)
    assert camera.is_livestreaming and sim.duml_commands().count("confirm") == 2
    await camera.disconnect()


@pytest.mark.parametrize("after", ["pair", "prepare", "wifi", "start"])
async def test_livestream_link_lost_mid_sequence(after):
    camera, sim, link = await connected(
        "action4", timeouts=fast_timeouts(step=5.0, wifi=5.0, pair_reply=5.0, start_confirm=5.0)
    )
    original = sim.handle_duml

    def handle(characteristic, frame):
        if describe(frame) == after:
            asyncio.get_running_loop().call_later(0.03, link.drop)  # the camera goes away instead of answering
            return
        original(characteristic, frame)

    sim.handle_duml = handle
    with pytest.raises(CameraDisconnected, match="was lost"):
        await camera.start_livestream(**STREAM)
    assert not camera.is_connected and not camera.is_livestreaming
    await camera.stop_livestream()
    await camera.disconnect()


async def test_livestream_validation_happens_before_anything_is_sent():
    camera, sim, link = await connected("action4")
    bad = [
        ({"resolution": "4k"}, "480p, 720p or 1080p"),
        ({"fps": 60}, "25 or 30"),
        ({"bitrate_kbps": 50}, "1000 to 20000"),
        ({"rtmp_url": "rtmp://192.168.1.10/cam"}, "application and a stream name"),
        ({"rtmp_url": "http://192.168.1.10/live/cam"}, "rtmp://"),
        ({"ssid": ""}, "name is empty"),
        ({"ssid": "x" * 33}, "at most 32"),
        ({"password": "short"}, "8 to 63"),
        ({"stabilization": "extreme"}, "stabilisation"),
    ]
    for change, message in bad:
        with pytest.raises(ValueError, match=message):
            await camera.start_livestream(**{**STREAM, **change})
    assert link.writes == [] and not camera.is_livestreaming
    await camera.start_livestream(**{**STREAM, "resolution": "1280x720", "fps": 25, "bitrate_kbps": 2000})
    payload = start_payload(sim)
    assert payload[3] == 0x04 and payload[4:6] == struct.pack("<H", 2000) and payload[8] == 0x02
    await camera.disconnect()
    nano = OsmoCamera("X", model="nano", transport=FakeTransport())
    with pytest.raises(ValueError, match="cannot livestream"):
        await nano.start_livestream(**STREAM)


async def test_livestream_open_network_and_high_bitrate_are_allowed_with_a_warning(caplog):
    caplog.set_level(logging.WARNING, logger="videonotes.dji")
    camera, sim, _ = await connected("action4")
    await camera.start_livestream(**{**STREAM, "password": "", "bitrate_kbps": 12000})
    assert sim.wifi == (SSID, "") and "open network is untested" in caplog.text and "unstable" in caplog.text
    await camera.disconnect()


# =============================================================================================
# livestream: stop, disconnect, cancellation, keep-alive, logging
# =============================================================================================


async def test_stop_livestream_is_safe_in_any_state():
    camera, sim, link = await connected("action4")
    await camera.stop_livestream()  # connected, nothing started: nothing is sent
    assert link.writes == []
    await camera.pair()
    await camera.stop_livestream()  # in a remote-control session: nothing is sent either
    assert sim.duml_log == []
    await camera.disconnect()
    await camera.stop_livestream()
    await camera.disconnect()


async def test_stop_livestream_when_the_camera_is_gone():
    camera, sim, link = await connected("action4")
    await camera.start_livestream(**STREAM)
    link.drop()
    await camera.stop_livestream()
    await camera.disconnect()
    assert not camera.is_livestreaming


async def test_cancelling_start_livestream_stops_and_disconnects():
    # Ctrl-C in the CLI cancels the coroutine: the camera must not be left in Live Streaming mode
    camera, sim, link = await connected("action4", wifi_reply=None, timeouts=fast_timeouts(wifi=30.0))
    task = asyncio.ensure_future(camera.start_livestream(**STREAM))
    for _ in range(200):
        await asyncio.sleep(0.005)
        if "wifi" in sim.duml_commands():
            break
    assert sim.in_live_mode
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    assert sim.duml_commands()[-1] == "stop" and not sim.in_live_mode
    assert not camera.is_connected and link.disconnect_count == 1 and not camera.is_livestreaming
    await camera.disconnect()  # what the CLI does next; a no-op now


async def test_cancelling_twice_still_cleans_up():
    camera, sim, link = await connected(
        "action4", wifi_reply=None, answer_stop=False, timeouts=fast_timeouts(wifi=30.0, abort_stop=0.2)
    )
    task = asyncio.ensure_future(camera.start_livestream(**STREAM))
    while "wifi" not in sim.duml_commands():
        await asyncio.sleep(0.005)
    task.cancel()
    await asyncio.sleep(0.02)
    task.cancel()  # an impatient second Ctrl-C
    with pytest.raises(asyncio.CancelledError):
        await task
    for _ in range(100):
        if not link.is_connected:
            break
        await asyncio.sleep(0.01)
    assert not link.is_connected and sim.duml_commands()[-1] == "stop"


async def test_keepalive_frames_per_model():
    # Osmo Action 5 Pro: "04 00" every 2.5 s (DJI Mimo, per dji-vcam); Osmo Action 4: "01 01" every second (osmosis)
    for model, payload, expected in (
        ("action5pro", b"\x04\x00", duml.session_open()),
        ("action4", b"\x01\x01", duml.session_keepalive()),
    ):
        camera, sim, link = make(model, keepalive=True)
        profile = duml.MODELS[model]
        assert profile.keepalive_payload == payload
        fast = dataclasses.replace(profile, keepalive_interval=0.03)  # same frames, shorter period
        camera._profile = lambda fast=fast: fast  # type: ignore[method-assign]
        await camera.connect()
        await camera.start_livestream(**STREAM)
        await asyncio.sleep(0.15)
        session = [f for _, f in sim.duml_log if f.command == duml.CMD_SESSION]
        assert session[0] == duml.session_open() and len(session) >= 3
        assert all(f == expected for f in session[1:])
        await camera.disconnect()
        count = len(sim.duml_log)
        await asyncio.sleep(0.1)
        assert len(sim.duml_log) == count  # the keep-alive stops with the connection


async def test_camera_requests_are_acknowledged_in_a_livestream_session():
    camera, sim, link = await connected("action5pro")
    await camera.start_livestream(**STREAM)
    # a device-info request as captured from a Pocket 3 (48 -> 02, 40 00 81) and the battery push
    request = duml.Frame(0x48, duml.APP, b"\x22\x03", 0x40, 0x00, 0x81, b"hg212" + bytes(20))
    link.feed(request.encode() + BATTERY_PUSH_88, sizes=11)
    await asyncio.sleep(0.02)
    assert sim.duml_log[-1][1] == duml.Frame(duml.APP, 0x48, b"\x22\x03", 0xC0, 0x00, 0x81, b"\x00")
    assert camera.battery_percent == 88 and (await camera.status()).battery_percent == 88
    await camera.disconnect()


async def test_debug_log_has_every_frame_but_not_the_wifi_password(caplog):
    caplog.set_level(logging.DEBUG, logger="videonotes.dji")
    camera, sim, link = await connected("action4")
    await camera.start_livestream(**STREAM)
    await camera.disconnect()
    text = caplog.text
    assert "TX duml FFF5 02->08" in text and duml.prepare_livestream().encode().hex(" ") in text
    assert "RX FFF4: 55 0e 04 66 08 02 12 8c c0 02 e1 00" in text
    assert PASSWORD not in text and PASSWORD.encode().hex(" ") not in text and PASSWORD.encode().hex() not in text
    wifi_line = next(line for line in text.splitlines() if "02->07" in line and "07 47" in line)
    assert SSID.encode().hex(" ") in wifi_line and "** **" in wifi_line
    assert link.written(CHAR_WRITE).count(PASSWORD.encode()) == 1  # ... while the camera did get it


async def test_debug_log_of_rsdk_frames(caplog):
    caplog.set_level(logging.DEBUG, logger="videonotes.dji")
    camera, sim, _ = await connected("action4")
    await camera.pair()
    await camera.status()
    await camera.disconnect()
    assert "TX rsdk 00 19" in caplog.text and sim.rsdk_log[0].encode().hex(" ") in caplog.text
    assert "RX rsdk response 00 19" in caplog.text and "RX rsdk command 1D 02" in caplog.text


# =============================================================================================
# one connection, one protocol
# =============================================================================================


async def test_switching_protocols_reconnects():
    camera, sim, link = await connected("action4")
    await camera.pair()  # what the CLI does before every command
    assert link.connect_count == 1
    writes_before = len(link.writes)
    await camera.start_livestream(**STREAM)
    # the remote-control link was dropped; the livestream ran on a fresh connection, free of R SDK frames
    assert link.connect_count == 2 and link.disconnect_count == 1
    assert all(w.data[0] == 0x55 for w in link.writes[writes_before:])
    assert len(sim.rsdk_log) == 3 and camera.is_livestreaming
    # recording control is refused while the stream runs ...
    with pytest.raises(CameraError, match="Stop the livestream"):
        await camera.start_recording()
    assert camera.is_livestreaming and link.connect_count == 2
    # ... and after stopping it, a remote-control call reconnects once more and pairs silently
    await camera.stop_livestream()
    await camera.start_recording()
    assert link.connect_count == 3 and sim.recording
    assert rsdk.ConnectRequest.unpack(sim.rsdk_log[3].payload).verify_mode == 0
    await camera.disconnect()


async def test_status_after_a_livestream_goes_back_to_remote_control():
    camera, sim, link = await connected("action5pro")
    await camera.start_livestream(**STREAM)
    assert (await camera.status()).mode == "Live Streaming" and sim.rsdk_log == []  # no request while streaming
    await camera.stop_livestream()
    status = await camera.status()  # the stream is over: reconnect, pair, read the real status
    assert link.connect_count == 2 and status.mode == "Photo" and status.battery_percent == 92
    assert status.livestreaming is False
    await camera.disconnect()


async def test_reconnect_failure_is_reported():
    camera, sim, link = await connected("action4")
    await camera.pair()
    link.connect_error = CameraNotFound("The camera was not found over Bluetooth.")
    with pytest.raises(CameraNotFound):
        await camera.start_livestream(**STREAM)
    assert not camera.is_connected
    await camera.disconnect()


# =============================================================================================
# model resolution
# =============================================================================================


async def test_model_resolution(monkeypatch, tmp_path, caplog):
    # 1. "auto": from the advertisement
    camera, _, _ = await connected("action5pro")
    assert camera.model == "action5pro"
    # 2. explicit model wins over the advertisement, with a warning
    caplog.set_level(logging.WARNING, logger="videonotes.dji")
    camera, sim, _ = await connected("action5pro", configured="action4")
    assert camera.model == "action4" and "advertises itself as Osmo Action 5 Pro" in caplog.text
    await camera.pair()  # ... and over the handshake's device_id
    assert camera.model == "action4"
    # 3. "auto" without advertisement: dji.model from config.toml
    home = tmp_path / "home"
    home.mkdir()
    (home / "config.toml").write_text('[dji]\nmodel = "action5pro"\n', encoding="utf-8")
    monkeypatch.setenv("VIDEONOTES_HOME", str(home))
    camera, _, _ = await connected("action4", advertise=False)
    assert camera.model == "action5pro"
    # 4. nothing known: unknown until the R SDK handshake reports the device_id
    (home / "config.toml").write_text("", encoding="utf-8")
    camera, _, _ = await connected("action5pro", advertise=False)
    assert camera.model is None
    await camera.pair()
    assert camera.model == "action5pro"
    # names are accepted as loosely as config.toml users write them
    assert OsmoCamera("X", model="Osmo Action 5 Pro").model == "action5pro"
    assert OsmoCamera("X", model="auto").model is None and OsmoCamera("X", model="nonsense").model is None


# =============================================================================================
# identity
# =============================================================================================


def test_identity_is_generated_once_and_persisted(tmp_path, caplog):
    path = tmp_path / "sub" / "camera_identity.json"
    first = Identity.load(path)
    assert path.is_file() and first.path == path and first.paired == []
    assert len(first.rsdk_mac) == 6 and first.rsdk_mac[0] & 0x03 == 0x02  # locally administered, unicast
    assert 1000 <= first.rsdk_code <= 9999 and first.rsdk_device_id not in (0, 0xFF33, 0xFF44)
    assert len(first.duml_identifier) == 32 and len(first.duml_pin) == 4 and first.duml_pin.isdigit()
    first.paired.append("UUID-OA4")
    first.save()
    second = Identity.load(path)
    assert second == first  # the same identity on every run, as the camera expects
    assert Identity.generate().duml_identifier != first.duml_identifier
    # an unreadable file is replaced (the camera will simply ask to pair again)
    caplog.set_level(logging.WARNING, logger="videonotes.dji")
    path.write_text("{not json", encoding="utf-8")
    third = Identity.load(path)
    assert third.duml_identifier != first.duml_identifier and "unreadable" in caplog.text
    assert Identity.load(path) == third
    path.write_text(
        json.dumps({"rsdk_device_id": 1, "rsdk_mac": "00", "rsdk_code": 1, "duml_identifier": "x", "duml_pin": "1"})
    )
    assert len(Identity.load(path).rsdk_mac) == 6
    # an unwritable location only costs a repeated pairing prompt
    blocked = tmp_path / "file"
    blocked.write_text("x")
    Identity.generate(blocked / "nested" / "identity.json").save()
    Identity.generate().save()  # no path: nothing to do


async def test_default_identity_lives_in_the_videonotes_home(monkeypatch, tmp_path):
    monkeypatch.setenv("VIDEONOTES_HOME", str(tmp_path / "vn"))
    assert cam.default_identity_path() == tmp_path / "vn" / "camera_identity.json"
    link = FakeTransport()
    SimCamera(link)
    camera = OsmoCamera(link.address, transport=link, timeouts=fast_timeouts())
    await camera.connect()
    await camera.pair()
    await camera.disconnect()
    assert json.loads((tmp_path / "vn" / "camera_identity.json").read_text())["paired"] == [link.address]


# =============================================================================================
# synchronous helpers
# =============================================================================================


def test_run_sync_runs_a_whole_session():
    async def session() -> CameraStatus:
        camera, sim, _ = await connected("action5pro")
        try:
            await camera.pair()
            await camera.start_recording()
            return await camera.status()
        finally:
            await camera.disconnect()

    status = run_sync(session())
    assert status.recording is True and status.model == "Osmo Action 5 Pro"
    with pytest.raises(TimeoutError):
        run_sync(asyncio.sleep(5), timeout=0.05)
    with pytest.raises(CameraDisconnected):
        run_sync(OsmoCamera("X", transport=FakeTransport()).pair())


def test_run_sync_ctrl_c_lets_the_camera_clean_up():
    state: dict[str, object] = {}

    def interrupt() -> None:
        raise KeyboardInterrupt

    async def session() -> None:
        camera, sim, link = await connected("action4", wifi_reply=None, timeouts=fast_timeouts(wifi=30.0))
        state.update(sim=sim, link=link)
        asyncio.get_running_loop().call_later(0.1, interrupt)  # the user presses Ctrl-C during the Wi-Fi join
        await camera.start_livestream(**STREAM)

    with pytest.raises(KeyboardInterrupt):
        run_sync(session())
    sim, link = state["sim"], state["link"]
    assert sim.duml_commands()[-1] == "stop" and not sim.in_live_mode and not link.is_connected


def test_sync_camera_facade():
    link = FakeTransport(advertisement=FoundCamera("FAKE-0000-CAMERA", "Osmo", -50, "action4"))
    sim = SimCamera(link)
    main_thread = threading.get_ident()
    seen_threads: set[int] = set()
    original = sim.on_write

    def on_write(*args):
        seen_threads.add(threading.get_ident())
        return original(*args)

    link.on_write = on_write
    with SyncCamera(
        link.address, transport=link, identity=new_identity(), timeouts=fast_timeouts(), keepalive=False
    ) as camera:
        camera.pair()
        camera.start_recording()
        assert camera.status().recording is True
        camera.stop_recording()
        camera.start_livestream(**STREAM)
        assert camera.camera.is_livestreaming
        camera.stop_livestream()
        with pytest.raises(ValueError, match="25 or 30"):
            camera.start_livestream(**{**STREAM, "fps": 12})
    assert not link.is_connected and seen_threads and main_thread not in seen_threads
    camera.close()  # idempotent
    with pytest.raises(CameraDisconnected, match="closed"):
        camera.pair()


def test_sync_camera_close_stops_a_running_stream():
    link = FakeTransport(advertisement=FoundCamera("FAKE-0000-CAMERA", "Osmo", -50, "action5pro"))
    sim = SimCamera(link, model="action5pro")
    camera = SyncCamera(
        link.address, transport=link, identity=new_identity(), timeouts=fast_timeouts(), keepalive=False
    )
    camera.connect()
    camera.start_livestream(**STREAM)
    assert sim.streaming
    camera.close()
    assert not sim.streaming and not link.is_connected
