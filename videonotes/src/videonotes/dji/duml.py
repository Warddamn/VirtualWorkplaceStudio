"""DJI "DUML" frames over Bluetooth LE: make the camera join Wi-Fi and push an RTMP livestream.

This protocol is *not* documented by DJI.  It is what the DJI Mimo app speaks and was
reverse-engineered by several open-source projects (moblin, node-osmo, djictl, osmosis,
DJILib, dji-remote ...).  It shares the GATT characteristics of the official R SDK
(:mod:`videonotes.dji.rsdk`) but nothing else: different start byte, checksums,
command numbers and pairing.

Everything in this module is pure: bytes in, bytes or dataclasses out.  No I/O.

Provenance.  Unless a comment says otherwise, layouts and constants follow the
research report ``livestream_ble.md`` (cited as "§n"), which was verified byte for
byte against the projects' unit tests and against frames captured from DJI Mimo.
Three things come from one further source, the MIT-licensed project *dji-vcam*
(``docs/protocol-notes.md`` §3.13, hardware-tested on an Osmo Action 5 Pro in
September 2026) and are marked "[dji-vcam]": the alternative start payload DJI Mimo
sends to an Osmo Action 5 Pro, the ``0x79`` "failed" livestream state and the
``0xD6`` "busy" result code.  Nothing here has been run against a camera.

Frame (§3)::

    0      0x55
    1      total frame length, low 8 bits        (13 + len(payload))
    2      (version << 2) | (length >> 8)        version 1 -> reads 0x04 below 256 bytes
    3      CRC8 of bytes 0..2
    4      sender component     (app 0x02)
    5      receiver component   (camera 0x01, Wi-Fi 0x07, video 0x08, session 0xF0)
    6..7   message id: opaque, echoed in the reply
    8      flags: 0x40 request that wants an answer, 0x80 / 0xC0 response, 0x00 push
    9      command set
    10     command id
    11..   payload
    last 2 CRC16 of everything before it, little endian
"""

from __future__ import annotations

import struct
from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum

# -- CRCs (§4) -------------------------------------------------------------------
#   CRC8 : poly 0x31,   init 0xEE,   reflected in/out, no final XOR   (header)
#   CRC16: poly 0x1021, init 0x496C, reflected in/out, no final XOR   (frame)
# Written LSB-first below: poly and init are the bit-reversed catalogue values.

_CRC8_INIT = 0x77  # bit-reverse of 0xEE
_CRC16_INIT = 0x3692  # bit-reverse of 0x496C


def _reflected_table(poly: int) -> tuple[int, ...]:
    table = []
    for i in range(256):
        c = i
        for _ in range(8):
            c = (c >> 1) ^ poly if c & 1 else c >> 1
        table.append(c)
    return tuple(table)


_CRC8_TABLE = _reflected_table(0x8C)  # bit-reverse of 0x31
_CRC16_TABLE = _reflected_table(0x8408)  # bit-reverse of 0x1021


def crc8(data: bytes) -> int:
    """Header checksum over bytes 0..2."""
    crc = _CRC8_INIT
    for b in data:
        crc = _CRC8_TABLE[(crc ^ b) & 0xFF]
    return crc


def crc16(data: bytes) -> int:
    """Frame checksum over everything before the last two bytes."""
    crc = _CRC16_INIT
    for b in data:
        crc = (crc >> 8) ^ _CRC16_TABLE[(crc ^ b) & 0xFF]
    return crc & 0xFFFF


# -- frame -----------------------------------------------------------------------------

MAGIC = 0x55
PROTOCOL_VERSION = 1
HEADER_LEN = 4  # magic, length, version|length, CRC8
FRAME_OVERHEAD = 13  # 11 header bytes + CRC16
MAX_FRAME_LEN = 1023  # 10-bit length field
#: several cameras and all first-generation clients only handle a one-byte length (§7)
SAFE_FRAME_LEN = 255

# component ids (bytes 4 and 5)
CAMERA = 0x01
APP = 0x02
WIFI_AIR = 0x05  # sender of the battery push
WIFI = 0x07  # pairing and Wi-Fi
VIDEO = 0x08  # livestream
SESSION = 0xF0  # session open / keep-alive

FLAG_PUSH = 0x00
FLAG_REQUEST = 0x40
FLAG_RESPONSE = 0x80
FLAG_ACK = 0xC0  # what the camera (and DJI Mimo) put on most replies

# (command set, command id)
CMD_SESSION = (0x00, 0x2B)
CMD_PAIR = (0x07, 0x45)
CMD_PAIR_APPROVED = (0x07, 0x46)
CMD_SETUP_WIFI = (0x07, 0x47)
CMD_PREPARE = (0x02, 0xE1)
CMD_PARAMETER = (0x02, 0x8E)  # stop / start confirm / stabilisation: one command, different payloads
CMD_START_STREAMING = (0x08, 0x78)
CMD_BATTERY_PUSH = (0x0D, 0x02)
CMD_LIVE_STATUS = (0xEE, 0x03)


class FrameError(ValueError):
    """A byte string is not a valid DUML frame."""


@dataclass(frozen=True)
class Frame:
    """One DUML frame."""

    sender: int
    receiver: int
    msg_id: bytes  # the two wire bytes at offsets 6..7
    flags: int
    cmd_set: int
    cmd_id: int
    payload: bytes = b""

    @property
    def command(self) -> tuple[int, int]:
        """``(command set, command id)``."""
        return (self.cmd_set, self.cmd_id)

    @property
    def is_response(self) -> bool:
        return bool(self.flags & FLAG_RESPONSE)

    @property
    def wants_ack(self) -> bool:
        """A request (from the camera) that expects an answer."""
        return bool(self.flags & FLAG_REQUEST) and not self.is_response

    def encode(self) -> bytes:
        """Serialise the frame, computing both checksums."""
        payload = bytes(self.payload)
        if len(self.msg_id) != 2:
            raise FrameError("msg_id must be the 2 raw wire bytes")
        for name, value in (
            ("sender", self.sender),
            ("receiver", self.receiver),
            ("flags", self.flags),
            ("cmd_set", self.cmd_set),
            ("cmd_id", self.cmd_id),
        ):
            if not 0 <= int(value) <= 0xFF:
                raise FrameError(f"{name}={value!r} is not a byte")
        total = FRAME_OVERHEAD + len(payload)
        if total > MAX_FRAME_LEN:
            raise FrameError(f"frame would be {total} bytes; the length field allows at most {MAX_FRAME_LEN}")
        head = bytes([MAGIC, total & 0xFF, (PROTOCOL_VERSION << 2) | (total >> 8)])
        head += bytes([crc8(head)])
        body = (
            head
            + bytes([self.sender, self.receiver])
            + bytes(self.msg_id)
            + bytes([self.flags, self.cmd_set, self.cmd_id])
            + payload
        )
        return body + struct.pack("<H", crc16(body))

    @classmethod
    def decode(cls, raw: bytes, *, allow_trailing: bool = False) -> Frame:
        """Parse one frame; raises :class:`FrameError` on any inconsistency."""
        raw = bytes(raw)
        if len(raw) < FRAME_OVERHEAD:
            raise FrameError(f"too short for a frame: {len(raw)} bytes")
        if raw[0] != MAGIC:
            raise FrameError(f"bad start byte 0x{raw[0]:02X} (expected 0x55)")
        total = frame_length(raw)
        if raw[2] >> 2 != PROTOCOL_VERSION:
            raise FrameError(f"unsupported protocol version {raw[2] >> 2}")
        if crc8(raw[:3]) != raw[3]:
            raise FrameError("CRC8 mismatch in the header")
        if total < FRAME_OVERHEAD:
            raise FrameError(f"length field {total} is shorter than an empty frame")
        if len(raw) < total:
            raise FrameError(f"incomplete frame: have {len(raw)} of {total} bytes")
        if len(raw) > total and not allow_trailing:
            raise FrameError(f"{len(raw) - total} unexpected bytes after the frame")
        raw = raw[:total]
        if crc16(raw[:-2]) != struct.unpack("<H", raw[-2:])[0]:
            raise FrameError("CRC16 mismatch")
        return cls(raw[4], raw[5], raw[6:8], raw[8], raw[9], raw[10], raw[11:-2])


def frame_length(buf: bytes) -> int:
    """Total frame length announced by the first three bytes (10-bit field)."""
    return buf[1] | ((buf[2] & 0x03) << 8)


class Reassembler:
    """Recover frames from a stream of GATT notification values.

    A notification may hold part of a frame, exactly one frame, or several frames,
    and the same characteristic also carries R SDK frames (start byte ``0xAA``),
    which are skipped here.  A frame is emitted as soon as all of its bytes have
    arrived and both checksums match, whatever precedes it: a complete valid frame
    later in the buffer proves that anything before it is garbage or a truncated
    frame, so a false start can never hold back real frames.  Memory is bounded by
    ``max_buffer``.
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
        consumed = 0
        keep_from = -1  # start of the earliest candidate that may still complete
        while pos < n:
            i = buf.find(MAGIC, pos)
            if i < 0:
                break
            if n - i < HEADER_LEN:
                if keep_from < 0:
                    keep_from = i  # cannot judge the header yet
                pos = i + 1
                continue
            length = buf[i + 1] | ((buf[i + 2] & 0x03) << 8)
            header_ok = (
                buf[i + 2] >> 2 == PROTOCOL_VERSION
                and length >= FRAME_OVERHEAD
                and crc8(bytes(buf[i : i + 3])) == buf[i + 3]
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
        if n - start > self._max:
            start = n - self._max
        self.discarded += start - consumed
        del buf[:start]
        return frames


# -- strings (§3) ----------------------------------------------------------------------


def pack_string(value: str) -> bytes:
    """``[len: u8] + utf8`` -- identifier, PIN, SSID, password."""
    data = value.encode("utf-8")
    if len(data) > 255:
        raise ValueError(f"string is {len(data)} bytes; at most 255 fit a one-byte length")
    return bytes([len(data)]) + data


def pack_url(value: str) -> bytes:
    """``[len: u16 LE] + utf8`` -- the RTMP URL."""
    data = value.encode("utf-8")
    if len(data) > 0xFFFF:
        raise ValueError("URL too long")
    return struct.pack("<H", len(data)) + data


# -- models (§2.1, §6) -----------------------------------------------------------------

COMPANY_DJI = 0x08AA
COMPANY_XTRA = 0xF7AA  # "Xtra" rebadged cameras (Xtra Edge = Action 4, Xtra Edge Pro = Action 5 Pro)

RESOLUTIONS = {"480p": 0x47, "720p": 0x04, "1080p": 0x0A}
FRAME_RATES = {25: 0x02, 30: 0x03}
STABILIZATION = {"off": 0, "rocksteady": 1, "horizonsteady": 2, "rocksteady+": 3, "horizonbalancing": 4}

#: Mimo's lowest preset is 1 Mbit/s; moblin offers up to 20 Mbit/s ("High bitrates may be unstable") (§6)
MIN_BITRATE_KBPS = 1000
MAX_BITRATE_KBPS = 20000
#: above this the stream is reported to get unstable (dji-remote README, §6)
RECOMMENDED_MAX_BITRATE_KBPS = 10000
#: longest RTMP URL whose start frame still fits in 255 bytes (§7)
MAX_URL_BYTES = 228
MAX_SSID_BYTES = 32  # IEEE 802.11
#: the JSON text DJI Mimo sends to an Osmo Action 5 Pro lives in a 128-byte buffer [dji-vcam]
MIMO_JSON_MAX_BYTES = 127


class Confirm(Enum):
    """When the "start confirm" message is written relative to the start-streaming frame (§5.0, §5.7)."""

    NONE = "none"  # moblin on Osmo Action 2/3
    AFTER_REPLY = "after reply"  # djictl / osmosis order, measured on an Osmo Action 4 and a Pocket 3
    BEHIND_START = "behind start"  # moblin order, the only one exercised on an Osmo Action 5 Pro


@dataclass(frozen=True)
class ModelProfile:
    """Per-model differences of the livestream sequence (§6)."""

    key: str  # value used in config.toml: "action4", "action5pro", ...
    name: str
    advert_id: int | None  # first manufacturer-data byte after the company id
    livestream: bool = True
    eis_device_byte: int | None = None  # 0x08 / 0x1A; None = the stabilisation step is skipped
    start_format: str = "legacy"  # "legacy" binary payload or "json"
    json_middle: bytes = b""  # two bytes inside the JSON-variant header
    confirm: Confirm = Confirm.NONE
    #: hard-coded length byte older clients sent instead of the computed one; tried if the camera refuses (§5.6)
    legacy_length_fallback: int | None = None
    #: also try the layout DJI Mimo sends to this model [dji-vcam]
    mimo_json_fallback: bool = False
    #: payload and period of the session keep-alive (§5.10; Action 5 Pro values from [dji-vcam])
    keepalive_payload: bytes = b"\x01\x01"
    keepalive_interval: float = 1.0
    tested_by: str = ""


_PROFILES = (
    ModelProfile("action2", "Osmo Action 2", 0x10, tested_by="reported not to work (dji-remote)"),
    ModelProfile("action3", "Osmo Action 3", 0x12, tested_by="moblin"),
    ModelProfile(
        "action4", "Osmo Action 4", 0x14, eis_device_byte=0x08, confirm=Confirm.AFTER_REPLY,
        legacy_length_fallback=0x2E, tested_by="moblin, dji-remote, osmo-live, osmosis (measured Oct 2026)",
    ),
    ModelProfile(
        "action5pro", "Osmo Action 5 Pro", 0x15, eis_device_byte=0x1A, confirm=Confirm.BEHIND_START,
        legacy_length_fallback=0x2A, mimo_json_fallback=True, keepalive_payload=b"\x04\x00", keepalive_interval=2.5,
        tested_by="moblin patch by an owner (2024), dji-remote reports, dji-vcam (Mimo layout, Sept 2026)",
    ),
    ModelProfile("osmo360", "Osmo 360", 0x17, eis_device_byte=0x1A, confirm=Confirm.BEHIND_START),
    ModelProfile(
        "action6", "Osmo Action 6", 0x18, eis_device_byte=0x08, start_format="json", json_middle=b"\xfe\x00",
        confirm=Confirm.BEHIND_START, tested_by="moblin",
    ),
    ModelProfile("nano", "Osmo Nano", 0x19, livestream=False),
    ModelProfile("pocket3", "Osmo Pocket 3", 0x20, confirm=Confirm.AFTER_REPLY, tested_by="moblin, djictl"),
    ModelProfile(
        "pocket4", "Osmo Pocket 4", 0x21, start_format="json", json_middle=b"\x02\x01", confirm=Confirm.BEHIND_START,
        tested_by="moblin",
    ),
    ModelProfile(
        "pocket4pro", "Osmo Pocket 4 Pro", None, start_format="json", json_middle=b"\x02\x01",
        confirm=Confirm.BEHIND_START,
    ),
)  # fmt: skip

MODELS: Mapping[str, ModelProfile] = {p.key: p for p in _PROFILES}
_BY_ADVERT_ID = {p.advert_id: p for p in _PROFILES if p.advert_id is not None}

#: Used when the model could not be determined: the sequence every camera is expected to accept --
#: legacy payload, no stabilisation step, start confirm after the reply (harmless where not needed).
UNKNOWN_MODEL = ModelProfile("unknown", "DJI camera (unknown model)", None, confirm=Confirm.AFTER_REPLY)

_ALIASES = {
    "oa2": "action2", "oa3": "action3", "oa4": "action4", "oa5pro": "action5pro", "oa5p": "action5pro",
    "action5": "action5pro", "oa6": "action6", "360": "osmo360",
}  # fmt: skip


def normalize_model(model: str | None) -> str | None:
    """Map a user-supplied model name to a profile key; ``None`` for "auto", empty or unknown names."""
    if not model:
        return None
    key = "".join(ch for ch in str(model).lower() if ch.isalnum())
    for prefix in ("dji", "osmo"):
        if key.startswith(prefix) and key not in MODELS:
            key = key[len(prefix) :]
    key = _ALIASES.get(key, key)
    return key if key in MODELS else None


def profile_for(model: str | None) -> ModelProfile:
    """The profile for a model key (or name); :data:`UNKNOWN_MODEL` when it is not known."""
    key = normalize_model(model)
    return MODELS[key] if key else UNKNOWN_MODEL


def identify_model(company_id: int, data: bytes) -> ModelProfile | None:
    """Identify a DJI camera from its manufacturer data as bleak reports it (§2.1).

    ``company_id`` is the Bluetooth company identifier and ``data`` the bytes after
    it.  Returns ``None`` when the advertisement is not from a DJI camera, and
    :data:`UNKNOWN_MODEL` for a DJI device whose model id is not in the table.
    """
    data = bytes(data)
    if company_id not in (COMPANY_DJI, COMPANY_XTRA) or len(data) < 2:
        return None
    if data[0:2] == b"\x00\x00":  # newer advertisement layout: 16-bit product type further in
        if len(data) >= 12 and data[10:12] == b"\xda\x00":
            return MODELS["pocket4pro"]
        return UNKNOWN_MODEL
    if data[1] != 0x00:
        return UNKNOWN_MODEL
    return _BY_ADVERT_ID.get(data[0], UNKNOWN_MODEL)


# -- validation ------------------------------------------------------------------------


def normalize_resolution(resolution: str) -> str:
    """``"1080p"`` / ``"1080"`` / ``"1920x1080"`` -> ``"1080p"``; ValueError for anything the cameras cannot stream."""
    text = str(resolution).strip().lower()
    if "x" in text:
        text = text.rsplit("x", 1)[1]
    if text.isdigit():
        text += "p"
    if text not in RESOLUTIONS:
        raise ValueError(
            f"Unsupported livestream resolution {resolution!r}: the camera can stream 480p, 720p or 1080p "
            "(set dji.stream_resolution in config.toml)."
        )
    return text


def validate_wifi(ssid: str, password: str) -> None:
    """Check the Wi-Fi credentials before they are sent; raises ValueError with what to fix."""
    if not isinstance(ssid, str) or not isinstance(password, str):
        raise ValueError("The Wi-Fi name and password must be text.")
    if not ssid:
        raise ValueError("The Wi-Fi network name is empty: give the name of the network the camera should join.")
    if "\x00" in ssid or "\x00" in password:
        raise ValueError("The Wi-Fi name and password must not contain NUL characters.")
    ssid_len = len(ssid.encode("utf-8"))
    if ssid_len > MAX_SSID_BYTES:
        raise ValueError(f"The Wi-Fi network name is {ssid_len} bytes long; network names are at most 32 bytes.")
    pass_len = len(password.encode("utf-8"))
    if pass_len == 0:
        return  # open network: nothing known against it, nothing known for it either (§7)
    is_raw_key = pass_len == 64 and all(c in "0123456789abcdefABCDEF" for c in password)
    if not is_raw_key and not 8 <= pass_len <= 63:
        raise ValueError(
            f"The Wi-Fi password is {pass_len} characters long; WPA2 passwords are 8 to 63 characters. "
            "The camera can only join a network that uses one password (WPA2-Personal), "
            "not one that asks for a user name or a web login."
        )


def validate_rtmp_url(url: str) -> None:
    """Check the RTMP address the camera will push to; raises ValueError with what to fix."""
    if not isinstance(url, str) or not url:
        raise ValueError("The RTMP address is empty.")
    if any(ord(ch) < 0x21 or ord(ch) > 0x7E for ch in url):
        raise ValueError(f"The RTMP address {url!r} contains spaces or characters outside plain ASCII.")
    if not url.lower().startswith("rtmp://"):
        raise ValueError(
            f"The RTMP address {url!r} must start with rtmp:// (rtmps and other schemes are not known to work)."
        )
    host, _, path = url[len("rtmp://") :].partition("/")
    if not host or host.startswith(":"):
        raise ValueError(
            f"The RTMP address {url!r} has no host: it should look like rtmp://192.168.1.10:1935/live/cam."
        )
    if len([part for part in path.split("/") if part]) < 2:
        # [dji-vcam]: an Osmo Action 5 Pro accepted "rtmp://host/name" but never connected to it
        raise ValueError(
            f"The RTMP address {url!r} needs an application and a stream name after the host, "
            "for example rtmp://192.168.1.10:1935/live/cam (see capture.rtmp_path in config.toml)."
        )
    size = len(url.encode("utf-8"))
    if size > MAX_URL_BYTES:
        raise ValueError(f"The RTMP address is {size} bytes long; the camera accepts at most {MAX_URL_BYTES}.")


def validate_stream(
    profile: ModelProfile, *, rtmp_url: str, resolution: str, fps: int, bitrate_kbps: int, stabilization: str = "off"
) -> str:
    """Validate livestream parameters for a model; returns the normalised resolution name.

    Raises ValueError with a message that says what to change.
    """
    if not profile.livestream:
        raise ValueError(f"The {profile.name} cannot livestream over Wi-Fi.")
    validate_rtmp_url(rtmp_url)
    name = normalize_resolution(resolution)
    if isinstance(fps, bool) or fps not in FRAME_RATES:
        raise ValueError(
            f"Unsupported livestream frame rate {fps!r}: the camera streams at 25 or 30 fps (set dji.stream_fps)."
        )
    if isinstance(bitrate_kbps, bool) or not isinstance(bitrate_kbps, int):
        raise ValueError(f"The livestream bitrate must be a whole number of kbit/s, not {bitrate_kbps!r}.")
    if not MIN_BITRATE_KBPS <= bitrate_kbps <= MAX_BITRATE_KBPS:
        raise ValueError(
            f"Unsupported livestream bitrate {bitrate_kbps} kbit/s: use {MIN_BITRATE_KBPS} to {MAX_BITRATE_KBPS} "
            "(4000 to 6000 is what DJI's own app uses; set dji.stream_bitrate_kbps)."
        )
    if stabilization not in STABILIZATION:
        raise ValueError(f"Unknown stabilisation {stabilization!r}: choose one of {', '.join(sorted(STABILIZATION))}.")
    return name


# -- message ids -----------------------------------------------------------------------
# Opaque values; the camera echoes them.  moblin's constants are reused where a byte-exact
# reference frame exists for them (§5), djictl's for the start confirm so that its reply
# can be told apart from the reply to "stop", and osmosis' for the session frames (§5.10).

ID_SESSION = b"\x1b\xcb"
ID_PAIR = b"\x92\x80"
ID_STOP = b"\xc8\xea"
ID_PREPARE = b"\x12\x8c"
ID_SETUP_WIFI = b"\x19\x8c"
ID_START = b"\x2c\x8c"
ID_CONFIGURE = b"\x2d\x8c"
ID_START_CONFIRM = b"\xb4\xbb"

PAYLOAD_SESSION_OPEN = b"\x04\x00"
PAYLOAD_SESSION_KEEPALIVE = b"\x01\x01"
PAYLOAD_PREPARE = b"\x1a"  # camera mode 0x1A = Live Streaming
PAYLOAD_START_CONFIRM = b"\x01\x01\x1a\x00\x01\x01"
PAYLOAD_STOP = b"\x01\x01\x1a\x00\x01\x02"

#: identifier moblin and most other clients send (§5.1); only used when no own identifier is given
SHARED_IDENTIFIER = "284ae5b8d76b3375a04a6417ad71bea3"


# -- app -> camera messages (§5) ---------------------------------------------------------


def session_open(msg_id: bytes = ID_SESSION) -> Frame:
    """Open the session; DJI Mimo writes this before pairing (§5.10)."""
    return Frame(APP, SESSION, msg_id, FLAG_REQUEST, *CMD_SESSION, PAYLOAD_SESSION_OPEN)


def session_keepalive(payload: bytes = PAYLOAD_SESSION_KEEPALIVE, msg_id: bytes = ID_SESSION) -> Frame:
    """Keep the link alive; the camera is reported to drop an idle link after about 6 s (§5.10)."""
    return Frame(APP, SESSION, msg_id, FLAG_REQUEST, *CMD_SESSION, bytes(payload))


def pair_request(pin: str, identifier: str = SHARED_IDENTIFIER, msg_id: bytes = ID_PAIR) -> Frame:
    """SetPairingPIN: ``PackString(identifier) + PackString(pin)`` (§5.1).

    The camera remembers its approval per ``identifier``; ``pin`` is shown on the
    camera's screen when it asks the user to confirm.
    """
    return Frame(APP, WIFI, msg_id, FLAG_REQUEST, *CMD_PAIR, pack_string(identifier) + pack_string(pin))


def ack(request: Frame, payload: bytes = b"\x00", flags: int = FLAG_ACK) -> Frame:
    """Answer a camera request: sender and receiver swapped, same id and command (§5.10)."""
    return Frame(request.receiver, request.sender, request.msg_id, flags, request.cmd_set, request.cmd_id, payload)


def stop_streaming(msg_id: bytes = ID_STOP) -> Frame:
    """Stop the livestream; also sent first as a clean-up of an earlier session (§5.2, §5.9)."""
    return Frame(APP, VIDEO, msg_id, FLAG_REQUEST, *CMD_PARAMETER, PAYLOAD_STOP)


def prepare_livestream(msg_id: bytes = ID_PREPARE) -> Frame:
    """Switch the camera to Live Streaming mode (§5.3)."""
    return Frame(APP, VIDEO, msg_id, FLAG_REQUEST, *CMD_PREPARE, PAYLOAD_PREPARE)


def setup_wifi(ssid: str, password: str, msg_id: bytes = ID_SETUP_WIFI, *, validate: bool = True) -> Frame:
    """Join an existing Wi-Fi network as a station: ``PackString(ssid) + PackString(password)`` (§5.4).

    The payload has no field for security type, band or user name: only networks
    with a plain password (WPA2-Personal) can work.  ``validate=False`` skips
    :func:`validate_wifi` (used to reproduce reference frames with toy credentials).
    """
    if validate:
        validate_wifi(ssid, password)
    return Frame(APP, WIFI, msg_id, FLAG_REQUEST, *CMD_SETUP_WIFI, pack_string(ssid) + pack_string(password))


def configure_stabilization(profile: ModelProfile, mode: str = "off", msg_id: bytes = ID_CONFIGURE) -> Frame | None:
    """Image-stabilisation step ``01 01 XX 00 01 EE`` (§5.5); ``None`` for models that skip it."""
    if profile.eis_device_byte is None:
        return None
    if mode not in STABILIZATION:
        raise ValueError(f"Unknown stabilisation {mode!r}: choose one of {', '.join(sorted(STABILIZATION))}.")
    payload = bytes([0x01, 0x01, profile.eis_device_byte, 0x00, 0x01, STABILIZATION[mode]])
    return Frame(APP, CAMERA, msg_id, FLAG_REQUEST, *CMD_PARAMETER, payload)


def start_confirm(msg_id: bytes = ID_START_CONFIRM) -> Frame:
    """ "Start confirm" ``01 01 1A 00 01 01``: required on an Osmo Action 5 Pro, harmless elsewhere (§5.7)."""
    return Frame(APP, VIDEO, msg_id, FLAG_REQUEST, *CMD_PARAMETER, PAYLOAD_START_CONFIRM)


def _resolution_code(resolution: str) -> int:
    try:
        return RESOLUTIONS[resolution]
    except KeyError:
        raise ValueError(f"unknown resolution {resolution!r}; expected one of {', '.join(RESOLUTIONS)}") from None


def _bitrate(bitrate_kbps: int) -> bytes:
    if not 0 < bitrate_kbps <= 0xFFFF:
        raise ValueError(f"bitrate {bitrate_kbps!r} kbit/s does not fit the 16-bit field")
    return struct.pack("<H", bitrate_kbps)


def start_payload_legacy(
    url: str, resolution: str, fps: int, bitrate_kbps: int, *, length_override: int | None = None
) -> bytes:
    """Legacy binary start-streaming payload (Osmo Action 2/3/4/5 Pro, Osmo 360, Pocket 3) (§5.6)::

        00 | len u16 = 11 + len(url) | resolution | bitrate u16 | 02 00 | fps | 00 00 00 | url len u16 | url

    ``length_override`` reproduces older clients that hard-coded the length byte
    (``0x2E`` / ``0x2A``) instead of computing it.
    """
    body = (
        bytes([_resolution_code(resolution)])
        + _bitrate(bitrate_kbps)
        + b"\x02\x00"
        + bytes([FRAME_RATES.get(fps, 0)])
        + b"\x00\x00\x00"
        + pack_url(url)
    )
    length = len(body) if length_override is None else length_override
    return b"\x00" + struct.pack("<H", length) + body


def _json_escape(text: str) -> str:
    return "".join("\\" + ch if ch in '"\\/' else ch for ch in text)


def start_payload_json(
    url: str, resolution: str, fps: int, bitrate_kbps: int, *, middle: bytes, codec: str = "AVC",
    enhanced_rtmp: bool = False,
) -> bytes:  # fmt: skip
    """JSON start-streaming payload of the Osmo Action 6 (``middle`` FE 00) and Pocket 4 (02 01) (§5.6).

    Slashes are escaped as Swift's encoder does, which is what moblin's verified
    fixtures were produced with; the order of the keys is not known to matter.
    """
    if len(middle) != 2:
        raise ValueError("middle must be 2 bytes")
    text = (
        '{"codec":"' + _json_escape(codec) + '","EnhancedRTMP":' + ("true" if enhanced_rtmp else "false")
        + ',"supportStopLive":false,"watermark":0,"rtmpAddress":"' + _json_escape(url)
        + '","orientation":"landscape"}'
    )  # fmt: skip
    data = text.encode("utf-8")
    body = (
        bytes([_resolution_code(resolution)])
        + _bitrate(bitrate_kbps)
        + bytes(middle)
        + bytes([FRAME_RATES.get(fps, 0)])
        + b"\x00\x00\x00"
        + struct.pack("<H", len(data))
        + data
    )
    return b"\x01" + struct.pack("<H", len(body)) + body


def mimo_json_text(url: str) -> bytes:
    """The settings JSON DJI Mimo sends to an Osmo Action 5 Pro [dji-vcam]."""
    text = '{"rtmpAddress":"' + _json_escape(url) + '","watermark":0,"codec":"","EnhancedRTMP":false,'
    return (text + '"supportStopLive":false}').encode("utf-8")


def start_payload_mimo_json(url: str, resolution: str, bitrate_kbps: int) -> bytes:
    """Start-streaming payload as DJI Mimo sends it to an Osmo Action 5 Pro [dji-vcam]::

        01 8A 00 | resolution | bitrate u16 | FE 01 00 00 00 00 7F 00 | JSON (at most 127 bytes)

    The two length fields are constants (the camera keeps the JSON in a 128-byte
    buffer); it refused longer JSON as "busy".  Not part of ``livestream_ble.md``;
    used only as a fallback when the camera does not accept the legacy payload.
    """
    data = mimo_json_text(url)
    if len(data) > MIMO_JSON_MAX_BYTES:
        raise ValueError(
            f"RTMP address too long for this payload: its settings text is {len(data)} bytes, "
            f"the camera takes at most {MIMO_JSON_MAX_BYTES}"
        )
    head = bytes([0x01, 0x8A, 0x00, _resolution_code(resolution)]) + _bitrate(bitrate_kbps)
    return head + b"\xfe\x01\x00\x00\x00\x00\x7f\x00" + data


def start_payload_candidates(
    profile: ModelProfile, url: str, resolution: str, fps: int, bitrate_kbps: int
) -> list[tuple[str, bytes]]:
    """Start-streaming payloads to try for a model, most trusted first, as ``(label, payload)``.

    The first entry is what ``livestream_ble.md`` §5.6/§6 prescribes for the model.
    The others are fallbacks for a camera that refuses or ignores it: the layout
    DJI Mimo was captured sending to an Osmo Action 5 Pro [dji-vcam], and the
    hard-coded length byte older clients used for years (§5.6).
    """
    if profile.start_format == "json":
        return [("json", start_payload_json(url, resolution, fps, bitrate_kbps, middle=profile.json_middle))]
    candidates = [("legacy", start_payload_legacy(url, resolution, fps, bitrate_kbps))]
    if profile.mimo_json_fallback and len(mimo_json_text(url)) <= MIMO_JSON_MAX_BYTES:
        candidates.append(("mimo-json", start_payload_mimo_json(url, resolution, bitrate_kbps)))
    if profile.legacy_length_fallback is not None:
        payload = start_payload_legacy(
            url, resolution, fps, bitrate_kbps, length_override=profile.legacy_length_fallback
        )
        if payload != candidates[0][1]:
            candidates.append((f"legacy-0x{profile.legacy_length_fallback:02x}", payload))
    return candidates


def start_streaming(payload: bytes, msg_id: bytes = ID_START) -> Frame:
    """Start-streaming ("configure streaming") frame around one of the payloads above (§5.6)."""
    frame = Frame(APP, VIDEO, msg_id, FLAG_REQUEST, *CMD_START_STREAMING, bytes(payload))
    if FRAME_OVERHEAD + len(frame.payload) > SAFE_FRAME_LEN:
        raise ValueError(
            f"The start command would be {FRAME_OVERHEAD + len(frame.payload)} bytes; "
            f"the camera only handles {SAFE_FRAME_LEN}. Use a shorter RTMP address."
        )
    return frame


# -- camera -> app messages ------------------------------------------------------------


class PairingStatus(Enum):
    ALREADY_PAIRED = "already paired"  # payload 00 01
    APPROVAL_REQUIRED = "approval required"  # payload 00 02: the camera shows a prompt
    UNKNOWN = "unknown"


def parse_pairing_status(payload: bytes) -> PairingStatus:
    """Reply to SetPairingPIN, ``C0 07 45`` (§5.1)."""
    if len(payload) >= 2 and payload[1] == 0x01:
        return PairingStatus.ALREADY_PAIRED
    if len(payload) >= 2 and payload[1] == 0x02:
        return PairingStatus.APPROVAL_REQUIRED
    return PairingStatus.UNKNOWN


class PairingDecision(Enum):
    APPROVED = "approved"  # payload 01 (captured)
    DENIED = "denied"  # payload 00 (DJILib; unconfirmed)
    TIMED_OUT = "timed out"  # payload 02 (DJILib; unconfirmed)
    UNKNOWN = "unknown"


def parse_pairing_decision(payload: bytes) -> PairingDecision:
    """The camera's ``40 07 46`` request that follows the user's choice on its screen (§5.1)."""
    code = payload[0] if payload else None
    return {0x01: PairingDecision.APPROVED, 0x00: PairingDecision.DENIED, 0x02: PairingDecision.TIMED_OUT}.get(
        code, PairingDecision.UNKNOWN
    )


#: result codes seen in the first byte of replies; anything else is reported as a number
RESULT_CODES = {0x00: "ok", 0xD6: "busy"}  # 0xD6 [dji-vcam]


def parse_result(payload: bytes) -> int | None:
    """First payload byte of a reply (``00`` = accepted); ``None`` when the reply is empty."""
    return payload[0] if payload else None


def describe_result(code: int | None) -> str:
    if code is None:
        return "an empty reply"
    return RESULT_CODES.get(code, f"code 0x{code:02X}")


@dataclass(frozen=True)
class WifiResult:
    """Reply to setup Wi-Fi, ``C0 07 47`` (§5.4)."""

    joined: bool
    code: bytes  # the raw reply payload; 00 00 (or 00 00 00) = joined, first byte 01 = failed


def parse_wifi_result(payload: bytes) -> WifiResult:
    """``joined`` when the payload starts with ``00 00`` (the test §5.4 recommends)."""
    payload = bytes(payload)
    return WifiResult(len(payload) >= 2 and payload[0] == 0 and payload[1] == 0, payload)


def parse_battery_percent(payload: bytes) -> int | None:
    """Battery level from the ``00 0D 02`` push sent about once a second while streaming (§5.8)."""
    if len(payload) >= 21:
        value = payload[20]
    elif len(payload) >= 13:
        value = payload[12]
    else:
        return None
    return value if value <= 100 else None


LIVE_STREAMING = 0x08  # DJILib, [dji-vcam]
LIVE_READY = 0x09  # DJILib: "ready for Wi-Fi credentials"; [dji-vcam]: ready / joined, not streaming
LIVE_FAILED = 0x79  # [dji-vcam]: "live stream failed"; the camera retries by itself


@dataclass(frozen=True)
class LiveStatus:
    """The ``80 EE 03`` push the video component sends about once a second in Live Streaming mode (§5.8).

    Only the second payload byte is understood, from two independent readings
    (DJILib, and dji-vcam's hardware test on an Osmo Action 5 Pro): ``0x08`` the
    stream is live, ``0x09`` ready but not streaming, ``0x79`` failed.
    """

    phase: int  # payload[0]: 0x03 before the network is joined, 0x02 after [dji-vcam]
    state: int  # payload[1]

    @property
    def streaming(self) -> bool:
        return self.state == LIVE_STREAMING

    @property
    def failed(self) -> bool:
        return self.state == LIVE_FAILED

    @property
    def name(self) -> str:
        return {LIVE_STREAMING: "streaming", LIVE_READY: "ready, not streaming", LIVE_FAILED: "failed"}.get(
            self.state, f"state 0x{self.state:02X}"
        )


def parse_live_status(payload: bytes) -> LiveStatus | None:
    """Decode an ``EE 03`` push; ``None`` when it is too short."""
    if len(payload) < 2:
        return None
    return LiveStatus(payload[0], payload[1])
