"""DJI "R SDK" remote-control protocol: frames, payloads and the pairing handshake.

This is DJI's *official* Bluetooth LE protocol for remote controllers (start/stop
recording, mode switch, 2 Hz status push, sleep).  It is documented in
https://github.com/dji-sdk/Osmo-GPS-Controller-Demo and supported by the Osmo
Action 4, Osmo Action 5 Pro, Osmo Action 6 and Osmo 360.

Everything in this module is pure: bytes in, bytes or dataclasses out.  No I/O.

Provenance.  Layouts, constants and CRC parameters follow the research report
``rsdk_ble.md`` (sections cited as "§n" below), which was checked byte for byte
against DJI's demo sources and against frames captured from a real Osmo
Action 4 and Osmo Action 5 Pro.  Nothing here has been run against a camera.

Frame (§4), little-endian throughout::

    0      SOF 0xAA
    1..2   u16: bits 15..10 version (0), bits 9..0 total frame length
    3      CmdType: bits 4..0 response wanted (0 no, 1 optional, 2 required), bit 5 = response frame
    4      ENC (0 = not encrypted)
    5..7   RES (zeros when we send; opaque when the camera sends)
    8..9   SEQ u16, chosen by the sender of a command and echoed in its response
    10..11 CRC-16 over bytes 0..9
    12     CmdSet
    13     CmdID
    14..   payload
    last 4 CRC-32 over everything before it

Total frame length is ``18 + len(payload)``.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass, fields
from enum import Enum, IntEnum

# -- CRCs (§4.1, §4.2) -----------------------------------------------------------
# Ordinary reflected table CRCs; only the seed is unusual.
#   CRC-16: poly 0x8005 (reflected 0xA001), init 0x3AA3, no final XOR
#   CRC-32: poly 0x04C11DB7 (reflected 0xEDB88320), init 0x00003AA3, no final XOR
# zlib.crc32 cannot be used: it differs in init and final XOR.

CRC16_INIT = 0x3AA3
CRC32_INIT = 0x00003AA3


def _reflected_table(poly: int) -> tuple[int, ...]:
    table = []
    for i in range(256):
        c = i
        for _ in range(8):
            c = (c >> 1) ^ poly if c & 1 else c >> 1
        table.append(c)
    return tuple(table)


_CRC16_TABLE = _reflected_table(0xA001)
_CRC32_TABLE = _reflected_table(0xEDB88320)


def crc16(data: bytes, crc: int = CRC16_INIT) -> int:
    """Header checksum (bytes 0..9 of a frame)."""
    for b in data:
        crc = (_CRC16_TABLE[(crc ^ b) & 0xFF] ^ (crc >> 8)) & 0xFFFF
    return crc


def crc32(data: bytes, crc: int = CRC32_INIT) -> int:
    """Frame checksum (everything before the last four bytes)."""
    for b in data:
        crc = (_CRC32_TABLE[(crc ^ b) & 0xFF] ^ (crc >> 8)) & 0xFFFFFFFF
    return crc


# -- frame ---------------------------------------------------------------------------

SOF = 0xAA
HEADER_LEN = 12  # SOF .. CRC-16
MIN_FRAME_LEN = 16  # header + CRC-32 with an empty DATA segment (not a usable frame)
FRAME_OVERHEAD = 18  # header + CmdSet + CmdID + CRC-32
MAX_FRAME_LEN = 0x3FF  # 10-bit length field
MAX_PAYLOAD_LEN = MAX_FRAME_LEN - FRAME_OVERHEAD


class CmdType(IntEnum):
    """Values of the CmdType byte used by DJI's demo (§4)."""

    CMD_NO_RESPONSE = 0x00  # command, no response wanted
    CMD_RESPONSE_OR_NOT = 0x01  # command, response wanted but optional
    CMD_WAIT_RESULT = 0x02  # command, response required
    ACK_NO_RESPONSE = 0x20  # response frame
    ACK_RESPONSE_OR_NOT = 0x21
    ACK_WAIT_RESULT = 0x22


RESPONSE_FLAG = 0x20

# (CmdSet, CmdID) pairs documented by DJI (§6.1)
CMD_VERSION = (0x00, 0x00)
CMD_KEY_REPORT = (0x00, 0x11)
CMD_RESTART = (0x00, 0x16)
CMD_GPS_PUSH = (0x00, 0x17)
CMD_CONNECT = (0x00, 0x19)
CMD_POWER_MODE = (0x00, 0x1A)
CMD_STATUS_PUSH = (0x1D, 0x02)
CMD_RECORD = (0x1D, 0x03)
CMD_MODE_SWITCH = (0x1D, 0x04)
CMD_STATUS_SUBSCRIBE = (0x1D, 0x05)
CMD_NEW_STATUS_PUSH = (0x1D, 0x06)


class FrameError(ValueError):
    """A byte string is not a valid R SDK frame."""


@dataclass(frozen=True)
class Frame:
    """One R SDK frame."""

    cmd_set: int
    cmd_id: int
    payload: bytes = b""
    cmd_type: int = CmdType.CMD_RESPONSE_OR_NOT
    seq: int = 0
    version: int = 0
    enc: int = 0
    res: bytes = b"\x00\x00\x00"

    @property
    def command(self) -> tuple[int, int]:
        """``(CmdSet, CmdID)``."""
        return (self.cmd_set, self.cmd_id)

    @property
    def is_response(self) -> bool:
        return bool(self.cmd_type & RESPONSE_FLAG)

    @property
    def response_type(self) -> int:
        """0 = no response wanted, 1 = optional, 2..31 = required."""
        return self.cmd_type & 0x1F

    def encode(self) -> bytes:
        """Serialise the frame, computing both checksums."""
        payload = bytes(self.payload)
        for name, value, limit in (
            ("cmd_set", self.cmd_set, 0xFF),
            ("cmd_id", self.cmd_id, 0xFF),
            ("cmd_type", self.cmd_type, 0xFF),
            ("enc", self.enc, 0xFF),
            ("seq", self.seq, 0xFFFF),
            ("version", self.version, 0x3F),
        ):
            if not 0 <= int(value) <= limit:
                raise FrameError(f"{name}={value!r} does not fit its field (0..{limit})")
        if len(self.res) != 3:
            raise FrameError("res must be exactly 3 bytes")
        total = FRAME_OVERHEAD + len(payload)
        if total > MAX_FRAME_LEN:
            raise FrameError(f"frame would be {total} bytes; the length field allows at most {MAX_FRAME_LEN}")
        head = struct.pack(
            "<BHBB3sH", SOF, (int(self.version) << 10) | total, int(self.cmd_type), int(self.enc), bytes(self.res),
            int(self.seq),
        )  # fmt: skip
        head += struct.pack("<H", crc16(head))
        body = head + bytes([int(self.cmd_set), int(self.cmd_id)]) + payload
        return body + struct.pack("<I", crc32(body))

    @classmethod
    def decode(cls, raw: bytes) -> Frame:
        """Parse exactly one frame; raises :class:`FrameError` on any inconsistency."""
        raw = bytes(raw)
        if len(raw) < MIN_FRAME_LEN:
            raise FrameError(f"too short for a frame: {len(raw)} bytes")
        if raw[0] != SOF:
            raise FrameError(f"bad start byte 0x{raw[0]:02X} (expected 0xAA)")
        ver_len = raw[1] | (raw[2] << 8)
        length = ver_len & MAX_FRAME_LEN
        if length != len(raw):
            raise FrameError(f"length field says {length} bytes but {len(raw)} were given")
        if struct.unpack_from("<H", raw, 10)[0] != crc16(raw[:10]):
            raise FrameError("CRC-16 mismatch in the header")
        if struct.unpack_from("<I", raw, length - 4)[0] != crc32(raw[:-4]):
            raise FrameError("CRC-32 mismatch")
        data = raw[HEADER_LEN:-4]
        if len(data) < 2:
            raise FrameError("empty DATA segment (no CmdSet/CmdID)")
        return cls(
            cmd_set=data[0],
            cmd_id=data[1],
            payload=data[2:],
            cmd_type=raw[3],
            seq=raw[8] | (raw[9] << 8),
            version=ver_len >> 10,
            enc=raw[4],
            res=raw[5:8],
        )


class Reassembler:
    """Recover frames from a stream of GATT notification values.

    DJI's demo assumes one notification is one whole frame.  This accepts that and
    everything else that can happen on a real link: frames split over several
    notifications, several frames in one notification, and bytes that are not R SDK
    at all (an Osmo Action 5 Pro interleaves ``0x55`` frames of its other protocol
    on the same characteristic, §3.4).

    A frame is emitted as soon as all of its bytes have arrived and both checksums
    match, whatever precedes it: a complete valid frame later in the buffer proves
    that anything before it is garbage or a truncated frame, so a false start can
    never hold back real frames.  Memory is bounded by ``max_buffer``.
    """

    def __init__(self, max_buffer: int = 4096) -> None:
        if max_buffer < MAX_FRAME_LEN:
            raise ValueError(f"max_buffer must be at least {MAX_FRAME_LEN}")
        self._buf = bytearray()
        self._max = max_buffer
        #: bytes thrown away so far because they were not part of a valid frame
        self.discarded = 0

    @property
    def pending(self) -> int:
        """Bytes currently held back as a possibly incomplete frame."""
        return len(self._buf)

    def reset(self) -> None:
        """Forget buffered bytes (call after a reconnect)."""
        self._buf.clear()

    def feed(self, chunk: bytes) -> list[Frame]:
        """Add one notification value; return the frames it completed, in order."""
        buf = self._buf
        buf += bytes(chunk)
        frames: list[Frame] = []
        n = len(buf)
        pos = 0
        consumed = 0  # bytes that belonged to emitted frames
        keep_from = -1  # start of the earliest candidate that may still complete
        while pos < n:
            i = buf.find(SOF, pos)
            if i < 0:
                break
            if n - i < HEADER_LEN:
                if keep_from < 0:
                    keep_from = i  # cannot judge the header yet
                pos = i + 1
                continue
            length = (buf[i + 1] | (buf[i + 2] << 8)) & MAX_FRAME_LEN
            header_ok = length >= FRAME_OVERHEAD and struct.unpack_from("<H", buf, i + 10)[0] == crc16(
                bytes(buf[i : i + 10])
            )
            if not header_ok:
                pos = i + 1
                continue
            if n - i < length:
                if keep_from < 0:
                    keep_from = i  # plausible frame, still arriving
                pos = i + 1
                continue
            try:
                frames.append(Frame.decode(bytes(buf[i : i + length])))
            except FrameError:
                pos = i + 1
                continue
            pos = i + length
            consumed += length
            keep_from = -1  # whatever came before a complete frame is dead
        start = keep_from if keep_from >= 0 else n
        kept = n - start
        if kept > self._max:
            start = n - self._max
            kept = self._max
        self.discarded += start - consumed
        del buf[:start]
        return frames


# -- return codes (§6.0) -------------------------------------------------------------

RETURN_CODES = {
    0x00: "ok",
    0x01: "the camera could not parse the command",
    0x02: "the camera could not carry out the command",
    0xFF: "undefined error",
}


def describe_return_code(code: int) -> str:
    """Human-readable meaning of a common R SDK return code."""
    return RETURN_CODES.get(code, f"unknown error code 0x{code:02X}")


def parse_return_code(payload: bytes) -> int | None:
    """First byte of a record / mode-switch / key / power response; ``None`` if the payload is empty.

    The documentation gives some of these responses four extra reserved bytes and the
    demo's structs do not (§13 item 2); only byte 0 carries meaning either way.
    """
    return payload[0] if payload else None


# -- connection / pairing handshake, (0x00, 0x19) (§5) ---------------------------------

_CONNECT_REQUEST = struct.Struct("<IB16sIBBH4s")  # 33 bytes
_CONNECT_RESPONSE = struct.Struct("<IB4s")  # 9 bytes

VERIFY_NONE = 0  # camera decides from its saved pairings whether to ask the user
VERIFY_REQUIRED = 1  # camera shows the verification pop-up
VERIFY_RESULT = 2  # used by the camera only: verify_data 0 = allowed, 1 = rejected

#: ``device_id`` the camera reports about itself (wire bytes ``33 FF 00 00`` etc., §5.4)
CAMERA_DEVICE_IDS = {0xFF33: "action4", 0xFF44: "action5pro", 0xFF55: "action6", 0xFF66: "osmo360"}


def model_from_device_id(device_id: int) -> str | None:
    """Model key for the ``device_id`` a camera sends in the handshake, if known."""
    return CAMERA_DEVICE_IDS.get(device_id)


@dataclass(frozen=True)
class ConnectRequest:
    """Payload of a ``00 19`` *command* frame (33 bytes).

    Sent by the controller to start the handshake, and by the camera (with
    ``verify_mode == 2``) to report the user's decision.
    """

    device_id: int
    mac: bytes = b""
    verify_mode: int = VERIFY_NONE
    verify_data: int = 0
    fw_version: int = 0  # must stay 0, otherwise the camera offers to "update" the remote (§5.3)
    conidx: int = 0
    reserved: bytes = b"\x00\x00\x00\x00"

    def pack(self) -> bytes:
        if len(self.mac) > 16:
            raise ValueError("mac may be at most 16 bytes")
        if len(self.reserved) != 4:
            raise ValueError("reserved must be 4 bytes")
        return _CONNECT_REQUEST.pack(
            self.device_id & 0xFFFFFFFF, len(self.mac), bytes(self.mac), self.fw_version & 0xFFFFFFFF, self.conidx,
            self.verify_mode, self.verify_data & 0xFFFF, bytes(self.reserved),
        )  # fmt: skip

    @classmethod
    def unpack(cls, payload: bytes) -> ConnectRequest:
        if len(payload) < _CONNECT_REQUEST.size:
            raise ValueError(f"connection request payload is {len(payload)} bytes, expected {_CONNECT_REQUEST.size}")
        device_id, mac_len, mac, fw, conidx, vmode, vdata, reserved = _CONNECT_REQUEST.unpack_from(payload)
        return cls(
            device_id=device_id, mac=mac[: min(mac_len, 16)], verify_mode=vmode, verify_data=vdata, fw_version=fw,
            conidx=conidx, reserved=reserved,
        )  # fmt: skip


@dataclass(frozen=True)
class ConnectResponse:
    """Payload of a ``00 19`` *response* frame (9 bytes)."""

    device_id: int
    ret_code: int = 0
    camera_number: int = 0  # "reserved" in the struct; the controller returns the camera number here

    def pack(self) -> bytes:
        return _CONNECT_RESPONSE.pack(
            self.device_id & 0xFFFFFFFF, self.ret_code, struct.pack("<I", self.camera_number & 0xFFFFFFFF)
        )

    @classmethod
    def unpack(cls, payload: bytes) -> ConnectResponse:
        if len(payload) < 5:
            raise ValueError(f"connection response payload is {len(payload)} bytes, expected 9")
        device_id, ret_code = struct.unpack_from("<IB", payload)
        tail = bytes(payload[5:9]).ljust(4, b"\x00")
        return cls(device_id=device_id, ret_code=ret_code, camera_number=struct.unpack("<I", tail)[0])


class HandshakeState(Enum):
    IDLE = "idle"
    REQUEST_SENT = "request sent"  # step 1 written, nothing heard yet
    AWAITING_USER = "waiting for the camera"  # step 2 received with ret_code 0
    CONNECTED = "connected"  # step 3 allowed; the step-4 reply was produced
    REJECTED = "rejected"  # the user (or the camera) refused
    FAILED = "failed"  # the camera answered step 1 with an error


class ConnectHandshake:
    """Sans-IO state machine for the four-frame pairing handshake (§5.1).

    ::

        controller                                   camera
        1. 00 19 command  (CmdType 0x02, SEQ s)  ->
                                                 <-  2. 00 19 response (SEQ s): device_id, ret_code
                 ... first pairing: the user accepts the pop-up on the camera ...
                                                 <-  3. 00 19 command (camera's SEQ c), verify_mode 2
        4. 00 19 response (CmdType 0x20, SEQ c)  ->       only if verify_data == 0

    Rule from §5.1.1 (it replaces a fragile fallback in DJI's demo): a ``00 19``
    *response* with our SEQ is step 2; the first ``00 19`` *command* with
    ``verify_mode == 2`` is step 3 whether or not step 2 was seen.

    Feed every received frame to :meth:`on_frame`; write whatever it returns.
    """

    def __init__(
        self, device_id: int, mac: bytes, verify_code: int, *, first_pairing: bool, camera_number: int = 0
    ) -> None:
        self.device_id = device_id
        self.mac = bytes(mac)
        self.verify_code = verify_code
        self.verify_mode = VERIFY_REQUIRED if first_pairing else VERIFY_NONE
        self.camera_number = camera_number
        self.state = HandshakeState.IDLE
        #: ``device_id`` the camera reported (0xFF33 = Osmo Action 4, 0xFF44 = Osmo Action 5 Pro)
        self.camera_device_id: int | None = None
        #: return code of the camera's step-2 response, when one was received
        self.ret_code: int | None = None
        #: value the camera sent in step 3 when it refused (1 = rejected by the user)
        self.reject_code: int | None = None
        self._seq = 0

    @property
    def done(self) -> bool:
        return self.state in (HandshakeState.CONNECTED, HandshakeState.REJECTED, HandshakeState.FAILED)

    def start(self, seq: int) -> Frame:
        """Step 1: the frame to write (CmdType 0x02, response required)."""
        self._seq = seq & 0xFFFF
        self.state = HandshakeState.REQUEST_SENT
        request = ConnectRequest(self.device_id, self.mac, self.verify_mode, self.verify_code)
        return Frame(*CMD_CONNECT, request.pack(), CmdType.CMD_WAIT_RESULT, self._seq)

    def on_frame(self, frame: Frame) -> Frame | None:
        """Process a received frame; returns the step-4 reply when the camera allowed the connection."""
        if frame.command != CMD_CONNECT or self.state not in (
            HandshakeState.REQUEST_SENT,
            HandshakeState.AWAITING_USER,
        ):
            return None
        if frame.is_response:  # step 2
            if frame.seq != self._seq or self.state is not HandshakeState.REQUEST_SENT:
                return None
            try:
                response = ConnectResponse.unpack(frame.payload)
            except ValueError:
                return None
            self.ret_code = response.ret_code
            self.camera_device_id = response.device_id  # the camera's model id is already in this response
            self.state = HandshakeState.AWAITING_USER if response.ret_code == 0 else HandshakeState.FAILED
            return None
        try:  # step 3
            request = ConnectRequest.unpack(frame.payload)
        except ValueError:
            return None
        if request.verify_mode != VERIFY_RESULT:
            return None  # not the verification result; keep waiting
        self.camera_device_id = request.device_id
        if request.verify_data != 0:
            self.reject_code = request.verify_data
            self.state = HandshakeState.REJECTED
            return None
        self.state = HandshakeState.CONNECTED
        reply = ConnectResponse(self.device_id, 0, self.camera_number)
        return Frame(*CMD_CONNECT, reply.pack(), CmdType.ACK_NO_RESPONSE, frame.seq)


# -- controller -> camera payloads (§6) ------------------------------------------------

#: constants DJI's demo puts in the ``device_id`` field of these two commands (§5.4);
#: the camera very probably ignores the field, the demo's values keep us on the tested path
RECORD_DEVICE_ID = 0x33FF0000
MODE_SWITCH_DEVICE_ID = 0xFF330000
MODE_SWITCH_RESERVED = b"\x01\x47\x39\x36"  # what the demo and the documented example send

RECORD_START = 0
RECORD_STOP = 1

POWER_NORMAL = 0
POWER_SLEEP = 3

KEY_RECORD = 0x01  # shutter: capture / record
KEY_QS = 0x02  # quick-switch button
KEY_SNAPSHOT = 0x03  # capture from sleep (needs the wake-up advertisement first)

KEY_EVENT_SHORT = 0x00
KEY_EVENT_LONG = 0x01
KEY_EVENT_DOUBLE = 0x02

PUSH_OFF = 0
PUSH_SINGLE = 1
PUSH_PERIODIC = 2
PUSH_PERIODIC_AND_ON_CHANGE = 3
PUSH_FREQ_2HZ = 20  # the only value the camera accepts (unit 0.1 Hz)


def record_payload(start: bool, device_id: int = RECORD_DEVICE_ID) -> bytes:
    """``1D 03`` recording control, 9 bytes: ``record_ctrl`` 0 = start, 1 = stop (§6.2)."""
    return struct.pack("<IB4s", device_id, RECORD_START if start else RECORD_STOP, b"\x00" * 4)


def mode_switch_payload(
    mode: int, device_id: int = MODE_SWITCH_DEVICE_ID, reserved: bytes = MODE_SWITCH_RESERVED
) -> bytes:
    """``1D 04`` mode switch, 9 bytes; ``mode`` is a camera mode value such as ``0x01`` (Video) (§6.4)."""
    if not 0 <= mode <= 0xFF:
        raise ValueError(f"mode {mode!r} is not a byte")
    if len(reserved) != 4:
        raise ValueError("reserved must be 4 bytes")
    return struct.pack("<IB4s", device_id, mode, bytes(reserved))


def status_subscribe_payload(push_mode: int = PUSH_PERIODIC_AND_ON_CHANGE, push_freq: int = PUSH_FREQ_2HZ) -> bytes:
    """``1D 05`` camera status subscription, 6 bytes (§6.5)."""
    return struct.pack("<BB4s", push_mode, push_freq, b"\x00" * 4)


def key_report_payload(key_code: int, mode: int = 1, key_value: int = KEY_EVENT_SHORT) -> bytes:
    """``00 11`` key report, 4 bytes; the defaults report a short press event (§6.3)."""
    return struct.pack("<BBH", key_code, mode, key_value)


def power_mode_payload(power_mode: int) -> bytes:
    """``00 1A`` camera power mode, 1 byte: 0 = normal, 3 = sleep (§6.9).

    A sleeping camera can only be woken by an advertisement a Mac cannot send
    (see :func:`wake_advertisement`), so videonotes never sends the sleep command.
    """
    if power_mode not in (POWER_NORMAL, POWER_SLEEP):
        raise ValueError("power_mode must be 0 (normal) or 3 (sleep)")
    return struct.pack("<B", power_mode)


def restart_payload(device_id: int) -> bytes:
    """``00 16`` device restart, 8 bytes (§6.12).  Documented by DJI but not implemented in its demo."""
    return struct.pack("<I4s", device_id & 0xFFFFFFFF, b"\x00" * 4)


_GPS = struct.Struct("<iiiiifffIIII")  # 48 bytes


@dataclass(frozen=True)
class GpsPush:
    """Payload of a ``00 17`` GPS data push (§6.11).  Not used by videonotes; kept for completeness."""

    year_month_day: int  # year*10000 + month*100 + day
    hour_minute_second: int  # (hour+8)*10000 + minute*100 + second, hour in UTC
    longitude_e7: int
    latitude_e7: int
    height_mm: int
    speed_north_cm_s: float
    speed_east_cm_s: float
    speed_down_cm_s: float
    vertical_accuracy_mm: int
    horizontal_accuracy_mm: int
    speed_accuracy_cm_s: int
    satellites: int

    def pack(self) -> bytes:
        return _GPS.pack(*(getattr(self, f.name) for f in fields(self)))

    @classmethod
    def unpack(cls, payload: bytes) -> GpsPush:
        if len(payload) < _GPS.size:
            raise ValueError(f"GPS payload is {len(payload)} bytes, expected {_GPS.size}")
        return cls(*_GPS.unpack_from(payload))


def build(command: tuple[int, int], payload: bytes, seq: int, cmd_type: int = CmdType.CMD_RESPONSE_OR_NOT) -> Frame:
    """A command frame for ``(CmdSet, CmdID)``."""
    return Frame(command[0], command[1], bytes(payload), int(cmd_type), seq & 0xFFFF)


# -- camera -> controller payloads -----------------------------------------------------

CAMERA_MODES = {
    0x00: "Slow Motion",
    0x01: "Video",
    0x02: "Timelapse",
    0x05: "Photo",
    0x0A: "Hyperlapse",
    0x1A: "Live Streaming",
    0x23: "Webcam (UVC)",
    0x28: "SuperNight",
    0x34: "Subject Tracking",
    # Osmo 360 only
    0x38: "Panoramic Video",
    0x3A: "Hyperlapse (360)",
    0x3C: "Selfie",
    0x3F: "Panoramic Photo",
    0x41: "Boost Video",
    0x43: "Vortex",
    0x44: "360 SuperNight",
    0x4A: "Single Lens SuperNight",
}
MODE_VIDEO = 0x01
MODE_PHOTO = 0x05
MODE_LIVESTREAM = 0x1A
MODE_WEBCAM = 0x23

CAMERA_STATES = {
    0x00: "screen off",
    0x01: "idle",  # "live view, including screen on without recording"
    0x02: "playback",
    0x03: "recording",  # "photo or recording in progress"
    0x05: "pre-recording",
}
STATE_RECORDING = 0x03
STATE_PRE_RECORDING = 0x05

VIDEO_RESOLUTIONS = {
    10: "1080p",
    16: "4K 16:9",
    45: "2.7K 16:9",
    66: "1080p 9:16",
    67: "2.7K 9:16",
    95: "2.7K 4:3",
    103: "4K 4:3",
    109: "4K 9:16",
}
PHOTO_SIZES = {4: "L", 3: "M", 2: "12 MP"}
FPS_BY_INDEX = {1: 24, 2: 25, 3: 30, 4: 48, 5: 50, 6: 60, 7: 120, 8: 240, 10: 100, 19: 200}
EIS_MODES = {0: "off", 1: "RockSteady", 2: "HorizonSteady", 3: "RockSteady+", 4: "HorizonBalancing"}
TEMPERATURE_STATES = {
    0: "normal",
    1: "warm (can still record)",
    2: "too hot to record",
    3: "overheating, shutting down",
}

# name, struct code -- 38 bytes when complete: "<BBBBBHBBHHHIIIBBBBIHB" (§6.6)
_STATUS_FIELDS: tuple[tuple[str, str], ...] = (
    ("camera_mode", "B"),
    ("camera_status", "B"),
    ("video_resolution", "B"),
    ("fps_idx", "B"),
    ("eis_mode", "B"),
    ("record_time", "H"),
    ("fov_type", "B"),
    ("photo_ratio", "B"),
    ("real_time_countdown", "H"),
    ("timelapse_interval", "H"),
    ("timelapse_duration", "H"),
    ("remain_capacity", "I"),
    ("remain_photo_num", "I"),
    ("remain_time", "I"),
    ("user_mode", "B"),
    ("power_mode", "B"),
    ("camera_mode_next_flag", "B"),
    ("temp_over", "B"),
    ("photo_countdown_ms", "I"),
    ("loop_record_sends", "H"),
    ("camera_bat_percentage", "B"),
)
STATUS_PUSH_FULL_LEN = sum(struct.calcsize("<" + code) for _, code in _STATUS_FIELDS)  # 38


@dataclass(frozen=True)
class StatusPush:
    """Payload of a ``1D 02`` camera status push (§6.6).

    The documented struct is 38 bytes, but a real Osmo Action 4 was captured sending
    only the first 31 (no photo countdown, loop-recording time or battery).  Fields
    are therefore decoded by length: one that does not fit completely in the payload
    is ``None``.  Unknown enum values are kept as integers.
    """

    camera_mode: int | None = None  # see CAMERA_MODES
    camera_status: int | None = None  # see CAMERA_STATES
    video_resolution: int | None = None  # see VIDEO_RESOLUTIONS (photo modes: PHOTO_SIZES)
    fps_idx: int | None = None  # see FPS_BY_INDEX (photo modes: burst count)
    eis_mode: int | None = None  # see EIS_MODES
    record_time: int | None = None  # seconds recorded so far, including pre-recording
    fov_type: int | None = None  # reserved
    photo_ratio: int | None = None  # 0 = 4:3, 1 = 16:9
    real_time_countdown: int | None = None  # seconds
    timelapse_interval: int | None = None  # 0.1 s (timelapse) or rate (hyperlapse, 0 = auto)
    timelapse_duration: int | None = None  # seconds
    remain_capacity: int | None = None  # free space on the card, MB
    remain_photo_num: int | None = None
    remain_time: int | None = None  # remaining recording time, seconds
    user_mode: int | None = None  # 0 general, 1..5 custom mode
    power_mode: int | None = None  # 0 normal, 3 sleep
    camera_mode_next_flag: int | None = None  # unreliable in real pushes; do not use (§6.6)
    temp_over: int | None = None  # see TEMPERATURE_STATES
    photo_countdown_ms: int | None = None
    loop_record_sends: int | None = None  # loop recording length in seconds, 0 = off, 65535 = max
    camera_bat_percentage: int | None = None  # 0..100
    payload_length: int = 0  # how many payload bytes the camera sent (31 or 38 seen)

    @classmethod
    def unpack(cls, payload: bytes) -> StatusPush:
        """Decode a payload of any length; never raises."""
        values: dict[str, int | None] = {}
        offset = 0
        for name, code in _STATUS_FIELDS:
            size = struct.calcsize("<" + code)
            if offset + size <= len(payload):
                values[name] = struct.unpack_from("<" + code, payload, offset)[0]
            else:
                values[name] = None
            offset += size
        return cls(payload_length=len(payload), **values)

    def as_dict(self) -> dict[str, int | None]:
        """The 21 documented fields by their DJI names."""
        return {name: getattr(self, name) for name, _ in _STATUS_FIELDS}

    @property
    def is_recording(self) -> bool | None:
        """Recording or pre-recording, as DJI's demo decides it (``camera_status`` 3 or 5)."""
        if self.camera_status is None:
            return None
        return self.camera_status in (STATE_RECORDING, STATE_PRE_RECORDING)

    @property
    def is_sleeping(self) -> bool | None:
        return None if self.power_mode is None else self.power_mode == POWER_SLEEP

    @property
    def is_photo_mode(self) -> bool:
        return self.camera_mode in (MODE_PHOTO, 0x3F)

    @property
    def mode_name(self) -> str | None:
        if self.camera_mode is None:
            return None
        return CAMERA_MODES.get(self.camera_mode, f"mode 0x{self.camera_mode:02X}")

    @property
    def state_name(self) -> str | None:
        if self.camera_status is None:
            return None
        return CAMERA_STATES.get(self.camera_status, f"state {self.camera_status}")

    @property
    def resolution_name(self) -> str | None:
        if self.video_resolution is None:
            return None
        if self.is_photo_mode:
            return PHOTO_SIZES.get(self.video_resolution, f"photo size {self.video_resolution}")
        return VIDEO_RESOLUTIONS.get(self.video_resolution, f"resolution code {self.video_resolution}")

    @property
    def fps(self) -> int | None:
        """Frames per second, or ``None`` when unknown or not meaningful (photo modes)."""
        if self.fps_idx is None or self.is_photo_mode:
            return None
        return FPS_BY_INDEX.get(self.fps_idx)

    @property
    def stabilization_name(self) -> str | None:
        if self.eis_mode is None:
            return None
        return EIS_MODES.get(self.eis_mode, f"mode {self.eis_mode}")

    @property
    def temperature_name(self) -> str | None:
        if self.temp_over is None:
            return None
        return TEMPERATURE_STATES.get(self.temp_over, f"state {self.temp_over}")


@dataclass(frozen=True)
class NewStatusPush:
    """Payload of a ``1D 06`` "new camera status push": mode name and parameters as text (§6.7)."""

    mode_name: str
    mode_param: str
    type_mode_name: int = 0x01
    type_mode_param: int = 0x02

    @classmethod
    def unpack(cls, payload: bytes) -> NewStatusPush:
        if len(payload) < 46:
            raise ValueError(f"1D 06 payload is {len(payload)} bytes, expected 46")
        name_len = min(payload[1], 21)
        param_len = min(payload[24], 21)
        return cls(
            mode_name=_text(payload[2 : 2 + name_len]),
            mode_param=_text(payload[25 : 25 + param_len]),
            type_mode_name=payload[0],
            type_mode_param=payload[23],
        )


@dataclass(frozen=True)
class VersionInfo:
    """Payload of the ``00 00`` version response (§6.8).

    Proves that the camera answers R SDK commands and nothing more: an Osmo Action
    5 Pro was captured answering ``DJI-ACTION4``, so the strings identify neither
    the model nor its firmware.
    """

    ack_result: int
    product_id: str
    sdk_version: str

    @classmethod
    def unpack(cls, payload: bytes) -> VersionInfo:
        if len(payload) < 2:
            raise ValueError(f"version response payload is {len(payload)} bytes, expected at least 2")
        (ack,) = struct.unpack_from("<H", payload)
        return cls(ack, _text(payload[2:18]), _text(payload[18:]))


def _text(raw: bytes) -> str:
    return bytes(raw).split(b"\x00", 1)[0].decode("ascii", "replace").strip()


# -- advertising helpers (§2) ----------------------------------------------------------

DJI_COMPANY_ID = 0x08AA
RSDK_MARKER = 0xFA


def is_rsdk_camera(company_id: int, data: bytes) -> bool:
    """DJI's own test for a compatible camera, in bleak terms (§2.1).

    The demo checks raw manufacturer-data bytes 0, 1 and 4 for ``AA 08 .. .. FA``;
    bleak strips the two company-id bytes, so the marker is at index 2 of ``data``.
    """
    return company_id == DJI_COMPANY_ID and len(data) >= 3 and data[2] == RSDK_MARKER


def wake_advertisement(camera_mac: bytes) -> bytes:
    """Raw advertising payload that wakes a sleeping camera: ``0A FF 'W' 'K' 'P'`` + MAC reversed (§2.6).

    For reference and tests only.  CoreBluetooth cannot broadcast arbitrary
    manufacturer data, so a Mac cannot send this with its built-in radio, and
    field reports say the camera ignores it from anything but the remote that
    was connected before.
    """
    if len(camera_mac) != 6:
        raise ValueError("camera_mac must be 6 bytes")
    return bytes([10, 0xFF]) + b"WKP" + bytes(reversed(camera_mac))
