"""Byte-exact tests of the DJI livestream ("DUML over BLE") codec (videonotes.dji.duml).

Every vector says where it comes from.  "report" is the research report livestream_ble.md;
"ref script" is livestream_ble_ref.py (62 vectors) and livestream_ble_verify.py next to it.
Behind them are the unit tests and captures of moblin, node-osmo, djictl, libdji, osmosis,
dji-remote, osmo-live, DJILib and xaionaro/reverse-engineering-dji (DJI Mimo <-> Pocket 3
btsnoop).  The three "[dji-vcam]" items are checked against that project's own unit test.
"""

from __future__ import annotations

import json
import random
import re
import struct

import pytest

from videonotes.dji import duml
from videonotes.dji.duml import Confirm, Frame, FrameError


def H(text: str) -> bytes:
    return bytes.fromhex(re.sub(r"[\s_]", "", text))


def frame(sender, receiver, msg_id, flags, cmd_set, cmd_id, payload=b"") -> bytes:
    return Frame(sender, receiver, bytes(msg_id), flags, cmd_set, cmd_id, bytes(payload)).encode()


def moblin(target: int, id_: int, type_: int, payload: bytes) -> bytes:
    """A frame written with moblin's (target u16 LE, id u16 LE, type u24 LE) triple (report §3)."""
    return frame(
        target & 0xFF, target >> 8, struct.pack("<H", id_), type_ & 0xFF, (type_ >> 8) & 0xFF, type_ >> 16, payload
    )


def fields(f: Frame):
    """(target, id LE, id BE, type) as the two code families name them (report §3)."""
    return (
        f.sender | (f.receiver << 8),
        f.msg_id[0] | (f.msg_id[1] << 8),
        (f.msg_id[0] << 8) | f.msg_id[1],
        f.flags | (f.cmd_set << 8) | (f.cmd_id << 16),
    )


IDENT_HEX = "3238346165356238643736623333373561303461363431376164373162656133"  # the 32 ASCII characters
OA4 = duml.MODELS["action4"]
OA5 = duml.MODELS["action5pro"]


# -- CRC ---------------------------------------------------------------------------------------


def _reflect(value: int, width: int) -> int:
    return int(f"{value:0{width}b}"[::-1], 2)


def _rocksoft(data: bytes, width: int, poly: int, init: int) -> int:
    """Bit-by-bit MSB-first CRC with refin = refout = true, xorout 0 (the catalogue form in report §4)."""
    top, mask, crc = 1 << (width - 1), (1 << width) - 1, init
    for b in data:
        crc ^= _reflect(b, 8) << (width - 8)
        for _ in range(8):
            crc = ((crc << 1) ^ poly) & mask if crc & top else (crc << 1) & mask
    return _reflect(crc, width)


def test_crc_parameters_and_tables():
    # report §4: reflected init 0x77 / 0x3692, reflected poly 0x8C / 0x8408; first and last table rows
    assert _reflect(0xEE, 8) == 0x77 and _reflect(0x31, 8) == 0x8C
    assert _reflect(0x496C, 16) == 0x3692 and _reflect(0x1021, 16) == 0x8408
    assert list(duml._CRC8_TABLE[:8]) == [0x00, 0x5E, 0xBC, 0xE2, 0x61, 0x3F, 0xDD, 0x83]
    assert list(duml._CRC8_TABLE[-8:]) == [0xB6, 0xE8, 0x0A, 0x54, 0xD7, 0x89, 0x6B, 0x35]
    assert list(duml._CRC16_TABLE[:8]) == [0x0000, 0x1189, 0x2312, 0x329B, 0x4624, 0x57AD, 0x6536, 0x74BF]
    assert list(duml._CRC16_TABLE[-8:]) == [0x7BC7, 0x6A4E, 0x58D5, 0x495C, 0x3DE3, 0x2C6A, 0x1EF1, 0x0F78]


def test_crc_known_answers():
    # libdji tests/tst_crc.cpp:6-18
    assert duml.crc8(b"123456789") == 0xFB and duml.crc16(b"123456789") == 0x7109
    # djictl pkg/duml/pcap_integration_test.go:11-29
    assert duml.crc8(H("551b04")) == 0x75 and duml.crc8(H("551204")) == 0xC7
    # dji-remote DjiCrcTest.kt:143-149 / osmosis DjiCrcTest.kt:118-121
    assert duml.crc8(H("553304")) == 0xC2
    # report §4 "Known-answer values"
    assert duml.crc8(H("550E04")) == 0x66 and duml.crc8(H("551304")) == 0x03 and duml.crc8(H("550D04")) == 0x33
    # dji-remote DjiCrcTest.kt:151-169: pairing frame body with PIN "mbln" -> 0x5ACE
    assert duml.crc16(H("553304c2 0207 9280 400745 20" + IDENT_HEX + "04 6d626c6e")) == 0x5ACE


def test_crc_three_formulations_agree():
    # ref script "crc.three-forms-agree" and the dji-remote / osmosis cross-verify inputs
    samples = [b"", b"\x00", b"\xff", bytes(range(256)), b"123456789", H("551b04"), H("553304"), H("550d04"),
               H("550b04"), H("0102030405"), H("55330404 0207 9280 400745 20" + IDENT_HEX + "04 6d626c6e"),
               H("550d0469 0208 2c8c 400878")]  # fmt: skip
    for sample in samples:
        assert duml.crc8(sample) == _rocksoft(sample, 8, 0x31, 0xEE)
        assert duml.crc16(sample) == _rocksoft(sample, 16, 0x1021, 0x496C)


# -- pairing -----------------------------------------------------------------------------------

PAIR_MBLN = H("553304c2 0207 9280 400745 20" + IDENT_HEX + "04 6d626c6e ce5a")


def test_pairing_frame_with_moblin_pin():
    # dji-remote DjiMessageVerificationTest.kt:8-41 (report §5.1): full 51-byte frame, PIN "mbln"
    assert duml.pair_request("mbln").encode() == PAIR_MBLN and len(PAIR_MBLN) == 51
    assert (
        moblin(0x0702, 0x8092, 0x450740, duml.pack_string(duml.SHARED_IDENTIFIER) + duml.pack_string("mbln"))
        == PAIR_MBLN
    )
    decoded = Frame.decode(PAIR_MBLN)
    assert fields(decoded)[0::3] == (0x0702, 0x450740) and fields(decoded)[1] == 0x8092
    assert decoded.command == duml.CMD_PAIR and decoded.wants_ack and not decoded.is_response
    # moblin DjiDeviceMessage.swift:3-19: the payload bytes
    assert decoded.payload == H("20" + IDENT_HEX + "04 6d626c6e")


def test_pairing_frame_variants():
    # dji-remote DjiMessageVerificationTest.kt:43-55: empty PIN -> 47 bytes
    assert len(duml.pair_request("").encode()) == 47
    # DJILib.swift:212: PIN "8670", id a8 94, CRC b1 88
    assert duml.pair_request("8670", msg_id=H("a894")).encode() == H(
        "553304C2 0207 A894 400745 20" + IDENT_HEX + "04 38363730 B188"
    )
    # osmosis MEDIA_PROTOCOL.md:995: token "osmo", id 00 a0, CRC 8c 02
    expected = H(
        "553304c2020700a0400745203238346165356238643736623333373561303461363431376164373162656133046f736d6f8c02"
    )
    assert duml.pair_request("osmo", msg_id=H("00a0")).encode() == expected
    # osmosis DjiCrcTest.kt:123-140: 51 bytes, header 55 33 04, decode round trip
    raw = duml.pair_request("osmo").encode()
    assert len(raw) == 51 and raw[:3] == H("553304")
    decoded = Frame.decode(raw)
    assert fields(decoded) == (0x0702, 0x8092, 0x9280, 0x450740) and decoded.payload.endswith(b"\x04osmo")
    # djictl interface_app_to_wifi_ground_station_pair.go: identifier "001749319286102", PIN "5160"
    own = duml.pair_request("5160", "001749319286102")
    assert own.payload == H("0f 303031373439333139323836313032 04 35313630")


def test_pairing_replies():
    # reverse-engineering-dji message_types.md:1196-1233 (report §5.1)
    need = H("55 0F 04 A2 07 02 72 AA C0 07 45 00 02 00 69")
    done = H("55 0F 04 A2 07 02 FC AB C0 07 45 00 01 8C 5F")
    assert frame(0x07, 0x02, H("72aa"), 0xC0, 0x07, 0x45, H("0002")) == need
    assert frame(0x07, 0x02, H("fcab"), 0xC0, 0x07, 0x45, H("0001")) == done
    assert duml.parse_pairing_status(Frame.decode(need).payload) is duml.PairingStatus.APPROVAL_REQUIRED
    assert duml.parse_pairing_status(Frame.decode(done).payload) is duml.PairingStatus.ALREADY_PAIRED
    assert duml.parse_pairing_status(b"") is duml.PairingStatus.UNKNOWN
    assert duml.parse_pairing_status(b"\x00\x07") is duml.PairingStatus.UNKNOWN
    assert Frame.decode(need).is_response and not Frame.decode(need).wants_ack


def test_pairing_approval_request_and_ack():
    # message_types.md:1157-1193; djictl message.go:134; libdji tst_message.cpp:9-46 (report §5.1)
    approved = H("55 0E 04 66 07 02 04 00 40 07 46 01 10 73")
    request = Frame.decode(approved)
    assert (
        request.command == duml.CMD_PAIR_APPROVED and request.wants_ack and (request.sender, request.receiver) == (7, 2)
    )
    assert duml.parse_pairing_decision(request.payload) is duml.PairingDecision.APPROVED
    assert duml.ack(request).encode() == H("55 0E 04 66 02 07 04 00 C0 07 46 00 35 28")  # what DJI Mimo answers
    # DJILib.swift:612-627 (unconfirmed readings of the other values)
    assert duml.parse_pairing_decision(b"\x00") is duml.PairingDecision.DENIED
    assert duml.parse_pairing_decision(b"\x02") is duml.PairingDecision.TIMED_OUT
    assert duml.parse_pairing_decision(b"") is duml.PairingDecision.UNKNOWN
    assert duml.parse_pairing_decision(b"\x09") is duml.PairingDecision.UNKNOWN
    # djictl-style ack: flags 0x80
    assert duml.ack(request, flags=duml.FLAG_RESPONSE).flags == 0x80


def test_pairing_stage_two_frame_of_djictl():
    # message_types.md:1052-1069; djictl ...pair.go:132-139 (not sent by us; framing check only)
    raw = frame(duml.APP, 0x88, H("74aa"), 0x40, 0x00, 0x32, H("3131000000"))
    assert raw[1] == 0x12 and raw[3] == 0xC7 and raw[-2:] == struct.pack("<H", 0x6A42)


# -- session open / keep-alive ---------------------------------------------------------------------


def test_session_frames():
    # report §5.10 (osmosis MEDIA_PROTOCOL.md:982-986)
    assert duml.session_open().encode() == H("55 0F 04 A2 02 F0 1B CB 40 00 2B 04 00 9A B9")
    assert duml.session_keepalive().encode() == H("55 0F 04 A2 02 F0 1B CB 40 00 2B 01 01 AB D6")
    # the Osmo Action 5 Pro profile repeats the "open" payload every 2.5 s [dji-vcam protocol-notes §3.13]
    assert duml.session_keepalive(OA5.keepalive_payload).encode() == duml.session_open().encode()
    assert (OA5.keepalive_payload, OA5.keepalive_interval) == (b"\x04\x00", 2.5)
    assert (OA4.keepalive_payload, OA4.keepalive_interval) == (b"\x01\x01", 1.0)


def test_osmosis_doc_frames():
    # osmosis MEDIA_PROTOCOL.md:1025,1030,1038: GetWifiSsid / GetWifiPassword / GetWifiMac (framing check only)
    assert frame(0x02, 0x07, H("00a0"), 0x40, 0x07, 0x07) == H("550d0433020700a04007077472")
    assert frame(0x02, 0x07, H("00a0"), 0x40, 0x07, 0x0E) == H("550d0433020700a040070eb5ef")
    assert frame(0x02, 0x07, H("00a0"), 0x40, 0x07, 0x0C) == H("550d0433020700a040070ca7cc")


# -- stop / prepare / stabilisation / start confirm -------------------------------------------------


def test_stop_frames():
    # report §5.2: complete frame with moblin's id; djictl message.go:135 with id b5 bb
    assert duml.stop_streaming().encode() == H("55 13 04 03 02 08 C8 EA 40 02 8E 01 01 1A 00 01 02 92 19")
    assert duml.stop_streaming(H("b5bb")).encode() == H("55130403 0208 b5bb 40028e 01011a000102 385f")
    # osmo-live pkg/osmo/client_test.go:192-236
    raw = duml.stop_streaming().encode()
    assert raw[10] == 0x8E and raw[4:8] == H("0208c8ea")


def test_prepare_frames():
    # DJILib.swift:258-260 (report §5.3)
    assert duml.prepare_livestream().encode() == H("55 0E 04 66 02 08 12 8C 40 02 E1 1A 11 DF")
    # captured reply, message_types.md:1268-1285
    reply = H("55 0E 04 66 08 02 FE AB C0 02 E1 00 8A 61")
    assert frame(0x08, 0x02, H("feab"), 0xC0, 0x02, 0xE1, H("00")) == reply
    assert duml.parse_result(Frame.decode(reply).payload) == 0
    # Mimo's optional "stage 2" (message_types.md:955-1014): framing check only, we do not send it
    assert frame(duml.APP, duml.VIDEO, H("ffab"), 0x40, 0x02, 0x8E, H("00011c00")) == H(
        "551104920208ffab40028e00011c003bc8"
    )
    # osmosis OsmoCommandsRtmpTest.kt:85-96: djictl's ids
    stage1 = duml.prepare_livestream(H("feab"))
    assert fields(stage1)[0] == 0x0802 and fields(stage1)[2] == 0xFEAB and stage1.payload == H("1a")


def test_start_confirm_frames():
    # djictl message.go:136 (id b4 bb, our default); DJILib.swift:248-252 (id 6a c0)
    assert duml.start_confirm().encode() == H("55 13 04 03 02 08 B4 BB 40 02 8E 01 01 1A 00 01 01 32 38")
    assert duml.start_confirm(H("6ac0")).encode() == H("55130403 0208 6AC0 40028E 01011A000101 686D")
    # report §8.3: moblin sends it with the stop id
    assert duml.start_confirm(duml.ID_STOP).encode() == H("551304030208c8ea40028e01011a000101092b")
    # osmosis OsmoCommandsRtmpTest.kt:98-106: start and stop differ only in the last payload byte
    start, stop = duml.start_confirm(), duml.stop_streaming()
    assert start.payload == H("01011a000101") and stop.payload == H("01011a000102")
    assert start.command == stop.command == (0x02, 0x8E) and (start.sender, start.receiver) == (2, 8)
    assert start.msg_id != stop.msg_id  # so that the two replies can be told apart (report §9 notes)


def test_stabilisation_frames():
    # report §5.5: Osmo Action 4 with RockSteady
    assert duml.configure_stabilization(OA4, "rocksteady").encode() == H(
        "55 13 04 03 02 01 2D 8C 40 02 8E 01 01 08 00 01 01 2B FD"
    )
    # osmosis OsmoCommandsRtmpTest.kt:108-117; moblin DjiDeviceMessage.swift:144-176
    assert duml.configure_stabilization(OA4, "rocksteady+").payload == H("010108000103")
    assert duml.configure_stabilization(OA5, "off").payload == H("01011a000100")
    configure = duml.configure_stabilization(OA4, "rocksteady+")
    assert fields(configure) == (0x0102, 0x8C2D, 0x2D8C, 0x8E0240)
    # dji-vcam protocol-notes appendix "Moblin RTMP push (A5P)": cfg, stabilisation off
    assert duml.configure_stabilization(OA5, "off").encode() == H("5513040302012d8c40028e01011a0001007516")
    assert duml.STABILIZATION == {
        "off": 0,
        "rocksteady": 1,
        "horizonsteady": 2,
        "rocksteady+": 3,
        "horizonbalancing": 4,
    }
    # models without the step (report §6)
    for key in ("action2", "action3", "pocket3", "pocket4", "pocket4pro"):
        assert duml.configure_stabilization(duml.MODELS[key], "rocksteady") is None
    assert duml.configure_stabilization(duml.UNKNOWN_MODEL, "off") is None
    with pytest.raises(ValueError, match="stabilisation"):
        duml.configure_stabilization(OA4, "turbo")


# -- setup Wi-Fi ----------------------------------------------------------------------------------


def test_setup_wifi_frames():
    # osmosis MEDIA_PROTOCOL.md:1020 (report §5.4): SSID "OsmoNano-C2D8", 12 x "x", id 00 a0
    expected = H("5528040d020700a04007470d4f736d6f4e616e6f2d433244380c78787878787878787878787827e1")
    assert duml.setup_wifi("OsmoNano-C2D8", "x" * 12, H("00a0")).encode() == expected
    # osmo-live pkg/osmo/client_test.go:178-190: ("foo", "bar")
    foo = duml.setup_wifi("foo", "bar", validate=False)
    assert foo.payload == H("03 666f6f 03 626172")
    assert fields(foo) == (0x0702, 0x8C19, 0x198C, 0x470740)
    # dji-remote DjiPayloadsTest.kt:16-23: ("ssid", "pass")
    assert duml.setup_wifi("ssid", "pass", validate=False).payload == H("04 73736964 04 70617373")
    # report §8.3 demo sequence: MyWifi / MyPassword
    assert duml.setup_wifi("MyWifi", "MyPassword").encode() == H(
        "551f044e0207198c400747064d79576966690a4d7950617373776f726408c2"
    )
    # dji-vcam protocol-notes appendix: "MyRouter" / "secret123"
    assert duml.setup_wifi("MyRouter", "secret123").encode() == H(
        "5520047b0207198c400747084d79526f75746572097365637265743132335048"
    )
    # UTF-8, length counted in bytes
    assert duml.setup_wifi("Café", "pässwörd").payload == b"\x05Caf\xc3\xa9\x0ap\xc3\xa4ssw\xc3\xb6rd"


def test_wifi_results():
    # report §5.4: "00 00" joined; a captured reply carries three zero bytes (message_types.md:1325-1342)
    captured = H("55 10 04 56 07 02 19 8C C0 07 47 00 00 00 F3 B8")
    assert frame(0x07, 0x02, H("198c"), 0xC0, 0x07, 0x47, H("000000")) == captured
    assert duml.parse_wifi_result(Frame.decode(captured).payload) == duml.WifiResult(True, bytes(3))
    assert duml.parse_wifi_result(H("0000")).joined
    # DJILib.swift:629-639: first byte 01 = connection failed; dji-vcam saw "01 ff" outside Live Streaming mode
    assert duml.parse_wifi_result(H("01ff")) == duml.WifiResult(False, H("01ff"))
    assert not duml.parse_wifi_result(H("0100")).joined
    assert not duml.parse_wifi_result(H("0001")).joined
    assert not duml.parse_wifi_result(H("00")).joined and not duml.parse_wifi_result(b"").joined


# -- start streaming: legacy payload -----------------------------------------------------------------

MIMO_URL = "rtmp://192.168.0.131:1946/test/stream0/"
# DJI Mimo's own frame, quoted in djictl interface_app_to_video_transmission_start_live_stream.go:89-91
MIMO_FRAME = H(
    "554204b0 0208 b3bb 400878 0032000a 7017 0200 03 000000 2700"
    "72746d703a2f2f3139322e3136382e302e3133313a313934362f746573742f73747265616d302f 995c"
)


def test_start_payload_moblin_fixture():
    # moblin DjiDeviceSuite.swift:60-71 ("Osmo Action 4 RTMP config test from DJI Mimo capture")
    expected = H(
        "0031000a7017020003000000260072746d703a2f2f3131302e3134342e392e3234303a313933352f7075626c6973682f6c697665"
    )
    assert duml.start_payload_legacy("rtmp://110.144.9.240:1935/publish/live", "1080p", 30, 6000) == expected
    assert expected[:14] == H("00 31 00 0A 70 17 02 00 03 00 00 00 26 00")  # report §5.6


def test_start_frame_as_dji_mimo_sends_it():
    # the builder reproduces Mimo's frame byte for byte, including the computed length and the CRC16
    payload = duml.start_payload_legacy(MIMO_URL, "1080p", 30, 6000)
    assert duml.start_streaming(payload, H("b3bb")).encode() == MIMO_FRAME
    decoded = Frame.decode(MIMO_FRAME)
    assert struct.unpack("<H", decoded.payload[1:3])[0] == len(decoded.payload) - 3 == 11 + len(MIMO_URL)
    assert decoded.command == duml.CMD_START_STREAMING and fields(decoded)[0] == 0x0802


def test_start_payload_hard_coded_length_variants():
    # osmosis OsmoCommandsRtmpTest.kt:33-47: 0x2A instead of the computed length
    raw = duml.start_streaming(
        duml.start_payload_legacy(MIMO_URL, "1080p", 30, 6000, length_override=0x2A), H("b3bb")
    ).encode()
    decoded = Frame.decode(raw)
    assert raw[1] == 0x42 and fields(decoded) == (0x0802, 0xBBB3, 0xB3BB, 0x780840)
    assert decoded.payload == H("002a000a7017020003000000 2700") + MIMO_URL.encode()
    # osmosis OsmoCommandsRtmpTest.kt:49-53: 0x2E
    assert duml.start_payload_legacy(MIMO_URL, "1080p", 30, 6000, length_override=0x2E)[1] == 0x2E
    # osmosis OsmoCommandsRtmpTest.kt:64-71: 720p / 4000 kbit/s / 25 fps
    payload = duml.start_payload_legacy("rtmp://h/l", "720p", 25, 4000, length_override=0x2A)
    assert payload[4:6] == H("a00f") and payload[3] == 0x04 and payload[6] == 0x02 and payload[8] == 0x02
    # dji-remote DjiPayloadsTest.kt:25-32 (node-osmo style 0x2E)
    payload = duml.start_payload_legacy("rtmp://example/stream", "1080p", 30, 4000, length_override=0x2E)
    assert payload == H("002e000a a00f 0200 03 000000 1500") + b"rtmp://example/stream"
    assert Frame.decode(moblin(0x0802, 0x8C2C, 0x780840, payload)).payload == payload
    # osmo-live pkg/commands/wifi.go:35-63
    assert (
        duml.start_payload_legacy("rtmp://a/b", "1080p", 30, 6000, length_override=0x2E)
        == H("002e000a 7017 0200 03 000000 0a00") + b"rtmp://a/b"
    )
    # dji-vcam protocol-notes appendix "Moblin RTMP push (A5P)": start with the old 0x2A byte
    old = duml.start_streaming(
        duml.start_payload_legacy("rtmp://192.168.1.10/live/oa5", "1080p", 30, 6000, length_override=0x2A)
    )
    assert old.encode() == H(
        "553704f902082c8c400878002a000a70170200030000001c0072746d703a2f2f3139322e3136382e312e31302f6c6976652f6f6135e192"
    )


def test_start_payload_url_limits_and_positions():
    # osmosis OsmoCommandsRtmpTest.kt:73-83: 228-byte URL -> 242-byte payload, 255-byte frame
    payload = duml.start_payload_legacy("x" * 228, "1080p", 30, 6000)
    assert len(payload) == 242 and payload[12:14] == H("e400")
    assert len(duml.start_streaming(payload).encode()) == 255 == duml.SAFE_FRAME_LEN
    with pytest.raises(ValueError, match="shorter RTMP address"):
        duml.start_streaming(duml.start_payload_legacy("x" * 229, "1080p", 30, 6000))
    # DJILib Tests/DJILibTests/DJILibTests.swift:34-49: URL length at absolute frame offset 23
    raw = duml.start_streaming(
        duml.start_payload_legacy("rtmp://192.168.1.123/publish/live/a/test", "1080p", 30, 3000)
    ).encode()
    assert raw[23] == 0x28
    # DJILib.swift:305-307,351-356: Mimo template "27 00 0A 70 17 02 00 03 00 00 00 1C 00" = 11 + 0x1C (report §5.6)
    payload = duml.start_payload_legacy("rtmp://192.168.1.10/live/oa5", "1080p", 30, 6000)
    assert payload[1:14] == H("27 00 0A 70 17 02 00 03 00 00 00 1C 00")


def test_start_payload_encodings():
    # report §5.6 / §6: resolution, fps and bitrate codes
    assert duml.RESOLUTIONS == {"480p": 0x47, "720p": 0x04, "1080p": 0x0A}
    assert duml.FRAME_RATES == {25: 0x02, 30: 0x03}
    for name, code in duml.RESOLUTIONS.items():
        for fps, fps_code in duml.FRAME_RATES.items():
            for kbps in (1000, 2000, 4000, 6000, 10000, 20000):
                payload = duml.start_payload_legacy("rtmp://h/a/b", name, fps, kbps)
                assert payload[0] == 0 and payload[3] == code and struct.unpack("<H", payload[4:6])[0] == kbps
                assert payload[6:8] == H("0200") and payload[8] == fps_code and payload[9:12] == bytes(3)
                assert payload[14:] == b"rtmp://h/a/b" and payload[12:14] == H("0c00")
    assert duml.start_payload_legacy("rtmp://h/a/b", "1080p", 24, 6000)[8] == 0  # moblin sends 00 for other rates
    with pytest.raises(ValueError, match="resolution"):
        duml.start_payload_legacy("rtmp://h/a/b", "4k", 30, 6000)
    with pytest.raises(ValueError, match="16-bit"):
        duml.start_payload_legacy("rtmp://h/a/b", "1080p", 30, 70000)


def test_report_demo_sequence():
    # report §8.3: example sequence for an Osmo Action 4, 1080p30, 6000 kbit/s, RockSteady
    assert duml.pair_request("mbln").encode() == H(
        "553304c202079280400745203238346165356238643736623333373561303461363431376164373162656133046d626c6ece5a"
    )
    assert duml.stop_streaming().encode() == H("551304030208c8ea40028e01011a0001029219")
    assert duml.prepare_livestream().encode() == H("550e04660208128c4002e11a11df")
    assert duml.configure_stabilization(OA4, "rocksteady").encode() == H("5513040302012d8c40028e0101080001012bfd")
    start = duml.start_streaming(duml.start_payload_legacy("rtmp://192.168.1.10:1935/live/dji", "1080p", 30, 6000))
    assert start.encode() == H(
        "553c04da02082c8c400878002c000a7017020003000000210072746d703a2f2f3139322e3136382e312e31303a313933352f6c6976652f646a6969c1"
    )


# -- start streaming: JSON payloads -------------------------------------------------------------------


def test_start_payload_json_pocket4():
    # moblin DjiDeviceSuite.swift:6-31: 161 bytes, body length 158, bytes 3..13, JSON content
    url = "rtmp://192.168.1.59/live/1"
    payload = duml.start_payload_json(url, "1080p", 30, 5000, middle=b"\x02\x01", codec="HEVC", enhanced_rtmp=True)
    assert len(payload) == 161 and payload[0] == 1 and struct.unpack("<H", payload[1:3])[0] == 158
    assert payload[3:14] == H("0a88130201030000009300") and len(payload[14:]) == 147
    assert json.loads(payload[14:]) == {
        "EnhancedRTMP": True, "codec": "HEVC", "orientation": "landscape", "rtmpAddress": url, "supportStopLive": False,
        "watermark": 0,
    }  # fmt: skip
    assert rb"rtmp:\/\/192.168.1.59\/live\/1" in payload  # the lengths only match with escaped slashes


def test_start_payload_json_action6():
    # moblin DjiDeviceSuite.swift:33-58: 169 bytes, body length 166, bytes 3..13
    url = "rtmp://192.168.1.59/live/123456789"
    payload = duml.start_payload_json(url, "720p", 30, 7000, middle=b"\xfe\x00", codec="AVC", enhanced_rtmp=False)
    assert len(payload) == 169 and struct.unpack("<H", payload[1:3])[0] == 166
    assert payload[3:14] == H("04581bfe00030000009b00") and len(payload[14:]) == 155
    assert json.loads(payload[14:])["rtmpAddress"] == url and json.loads(payload[14:])["codec"] == "AVC"
    with pytest.raises(ValueError):
        duml.start_payload_json(url, "720p", 30, 7000, middle=b"\xfe")


def test_start_payload_mimo_json_for_action5pro():
    # [dji-vcam] app/tests/live_stream_test.cpp "StartFollowsMimosLayout" (hardware-tested on an Osmo Action 5 Pro)
    payload = duml.start_payload_mimo_json("rtmp://192.168.1.20:1935/live/cam", "1080p", 6000)
    head = bytes([0x01, 0x8A, 0x00, 0x0A, 0x70, 0x17, 0xFE, 0x01, 0x00, 0x00, 0x00, 0x00, 0x7F, 0x00])
    text = (
        rb'{"rtmpAddress":"rtmp:\/\/192.168.1.20:1935\/live\/cam","watermark":0,"codec":"",'
        rb'"EnhancedRTMP":false,"supportStopLive":false}'
    )
    assert payload == head + text
    assert json.loads(text)["rtmpAddress"] == "rtmp://192.168.1.20:1935/live/cam"
    small = duml.start_payload_mimo_json("rtmp://h/x/y", "720p", 4000)
    assert small[3] == 0x04 and small[4:6] == H("a00f")
    # same test file, "TheSettingsJsonFitsTheCamerasBuffer": 127 bytes is the most the camera takes
    assert len(duml.mimo_json_text("rtmp://172.16.100.20:1935/live/vcam")) == 127 == duml.MIMO_JSON_MAX_BYTES
    assert len(duml.mimo_json_text("rtmp://172.16.100.20:1935/live/vcam1")) == 128
    duml.start_payload_mimo_json("rtmp://172.16.100.20:1935/live/vcam", "1080p", 6000)
    with pytest.raises(ValueError, match="too long"):
        duml.start_payload_mimo_json("rtmp://172.16.100.20:1935/live/vcam1", "1080p", 6000)


def test_start_payload_candidates_per_model():
    url = "rtmp://192.168.1.10:1935/live/cam"
    legacy = duml.start_payload_legacy(url, "1080p", 30, 4000)
    # Osmo Action 4: computed length first (what Mimo sends to an OA4), then the byte older clients hard-coded
    labels = [(label, payload) for label, payload in duml.start_payload_candidates(OA4, url, "1080p", 30, 4000)]
    assert labels == [
        ("legacy", legacy),
        ("legacy-0x2e", duml.start_payload_legacy(url, "1080p", 30, 4000, length_override=0x2E)),
    ]
    # Osmo Action 5 Pro: the report's legacy layout first, then Mimo's own layout for that model, then 0x2A
    labels = duml.start_payload_candidates(OA5, url, "1080p", 30, 4000)
    assert [label for label, _ in labels] == ["legacy", "mimo-json", "legacy-0x2a"]
    assert labels[0][1] == legacy and labels[1][1] == duml.start_payload_mimo_json(url, "1080p", 4000)
    # a URL too long for Mimo's 127-byte buffer simply drops that fallback
    long_url = "rtmp://192.168.100.100:1935/live/a-rather-long-stream-key"
    assert [label for label, _ in duml.start_payload_candidates(OA5, long_url, "1080p", 30, 4000)] == [
        "legacy",
        "legacy-0x2a",
    ]
    # a URL whose computed length happens to equal the hard-coded byte is not sent twice
    url_2e = "rtmp://" + "h" * 24 + "/a/b"  # 11 + 35 = 0x2E
    assert len(url_2e) == 35
    assert [label for label, _ in duml.start_payload_candidates(OA4, url_2e, "1080p", 30, 4000)] == ["legacy"]
    # JSON models and models without fallbacks
    assert [label for label, _ in duml.start_payload_candidates(duml.MODELS["action6"], url, "1080p", 30, 4000)] == [
        "json"
    ]
    assert duml.start_payload_candidates(duml.MODELS["action6"], url, "1080p", 30, 4000)[0][1][6:8] == H("fe00")
    assert duml.start_payload_candidates(duml.MODELS["pocket4"], url, "1080p", 30, 4000)[0][1][6:8] == H("0201")
    assert duml.start_payload_candidates(duml.UNKNOWN_MODEL, url, "1080p", 30, 4000) == [("legacy", legacy)]
    assert duml.start_payload_candidates(duml.MODELS["pocket3"], url, "1080p", 30, 4000) == [("legacy", legacy)]


# -- framing -------------------------------------------------------------------------------------


def test_frame_lengths():
    # osmo-live pkg/protocol/packet_test.go
    raw = frame(0x02, 0x08, struct.pack("<H", 0x1234), 0x40, 0x02, 0x01, H("deadbeef"))
    assert len(raw) == 17 and raw[0] == 0x55 and raw[1] == 17
    assert len(frame(0, 0, b"\0\0", 0, 0, 0)) == 13
    assert len(frame(0, 0, b"\0\0", 0, 0, 0, bytes(242))) == 255
    # djictl pkg/duml/features_test.go:27-42: 38-byte payload -> 51-byte frame
    assert len(frame(0x02, 0x06, b"\0\0", 0x00, 0x06, 0x24, bytes(38))) == 51
    # libdji tests/tst_message.cpp:9-46
    raw = frame(0x02, 0x07, H("0400"), 0xC0, 0x07, 0x46, H("00"))
    assert list(raw[:3]) == [0x55, 14, 0x04] and raw[4:12] == H("0207 0400 c00746 00")


def test_ten_bit_length():
    # djictl pkg/duml/pcap_integration_test.go:51-68: 300-byte payload -> 313-byte frame
    payload = bytes(i & 0xFF for i in range(300))
    raw = frame(1, 2, b"\x00\x03", 0x40, 0x01, 0x1E, payload)
    assert len(raw) == 313 and raw[1] == 313 & 0xFF and raw[2] == 0x04 | (313 >> 8)
    assert Frame.decode(raw).payload == payload and duml.frame_length(raw) == 313
    assert len(frame(1, 2, b"\0\0", 0, 0, 0, bytes(1010))) == 1023
    with pytest.raises(FrameError, match="1023"):
        frame(1, 2, b"\0\0", 0, 0, 0, bytes(1011))


def test_round_trip_and_header_corruption():
    # dji-remote DjiMessageTest.kt
    raw = moblin(0x0702, 0x1234, 0x112233, H("010203"))
    decoded = Frame.decode(raw)
    assert fields(decoded) == (0x0702, 0x1234, 0x3412, 0x112233) and decoded.payload == H("010203")
    bad = bytearray(moblin(1, 2, 3, b"\x01"))
    bad[2] = 0x05
    with pytest.raises(FrameError):
        Frame.decode(bytes(bad))


def test_decode_errors():
    good = duml.stop_streaming().encode()
    for mutate, message in (
        (lambda b: b[:12], "short"),
        (lambda b: b"\xaa" + b[1:], "start byte"),
        (lambda b: b[:3] + bytes([b[3] ^ 1]) + b[4:], "CRC8"),
        (lambda b: b[:-1] + bytes([b[-1] ^ 1]), "CRC16"),
        (lambda b: b[:12] + bytes([b[12] ^ 0x80]) + b[13:], "CRC16"),
        (lambda b: b + b"\x00", "unexpected"),
        (lambda b: b[:-1], "incomplete"),
    ):
        with pytest.raises(FrameError, match=message):
            Frame.decode(mutate(good))
    version2 = bytearray(good)
    version2[2] = 0x08
    version2[3] = duml.crc8(bytes(version2[:3]))
    with pytest.raises(FrameError, match="version"):
        Frame.decode(bytes(version2))
    with pytest.raises(FrameError, match="msg_id"):
        Frame(2, 8, b"\x01", 0x40, 2, 0x8E).encode()
    with pytest.raises(FrameError, match="receiver"):
        Frame(2, 256, b"\x01\x02", 0x40, 2, 0x8E).encode()


def test_trailing_bytes():
    # djictl pkg/duml/pcap_integration_test.go:31-49: the frame parses, also with 4 bytes of padding behind it
    raw = H("55110492021bfd944007450000000031d7")
    decoded = Frame.decode(raw)
    assert (decoded.sender, decoded.receiver, decoded.msg_id, decoded.flags, decoded.command, decoded.payload) == (
        0x02, 0x1B, H("fd94"), 0x40, (0x07, 0x45), H("00000000"),
    )  # fmt: skip
    assert Frame.decode(raw + b"\x01\x02\x03\x04", allow_trailing=True) == decoded


def test_djictl_pcap_samples():
    # djictl pkg/duml/pcap_integration_test.go:70-90 and the annotated frames in message.go:132-134
    for sample in (
        "551204c70402f6010004270000080000299d",
        "550d04330207ea94400707242b",
        "551f044e0702ea94c0070700104f736d6f506f636b6574332d36303934ccc8",
        "553e044b0402f001000405010700000b008000e0ff00014987fc276afd00001bfd010013aed43b68ce6c3d00917f3ff91bc5b900000000010000000099b5",
        "551204C70402AEB50004270000080000B684",
        "550e046602070400c00746003528",
    ):
        raw = H(sample)
        assert Frame.decode(raw).encode() == raw
    reply = Frame.decode(H("551f044e0702ea94c0070700104f736d6f506f636b6574332d36303934ccc8"))
    assert reply.payload == b"\x00\x10" + b"OsmoPocket3-6094"


def test_pack_string_and_url():
    # libdji tests/tst_message.cpp:70-88
    assert duml.pack_string("Hello") == b"\x05Hello"
    packed = duml.pack_url("http://example.com")
    assert len(packed) == 20 and packed[0] == 18 and packed[1] == 0 and packed[2:] == b"http://example.com"
    assert duml.pack_string("x" * 255)[0] == 255
    with pytest.raises(ValueError, match="255"):
        duml.pack_string("x" * 256)
    assert duml.pack_url("u" * 300)[:2] == struct.pack("<H", 300)  # full u16, not moblin's truncated byte


# Captured frames ("Value:" lines) of xaionaro/reverse-engineering-dji mimo/ble/message_types.md
# (DJI Mimo <-> Osmo Pocket 3), copied from MD_VALUES in the ref script: (line, type, hex)
MD_VALUES = [
    (
        112,
        "0x000280",
        "554904930102411000028001048000010000000000000000000000000000000000000000000000000000000246000001000000000000000000000000000000000000000001000017fc",
    ),
    (
        132,
        "0x000280",
        "554904930102421000028001048000010000000000000000000000000000000000000000000000000000000246000001000000000000000000000000000000000000000001000099fa",
    ),
    (
        152,
        "0x000280",
        "55490493010246100002800104800001000000000000000000000000000000000000000000000000000000024600000100000000000000000000000000000000000000000100007e0b",
    ),
    (
        172,
        "0x000280",
        "55490493010247100002800104800001000000000000000000000000000000000000000000000000000000024600000100000000000000000000000000000000000000000100000bf1",
    ),
    (
        192,
        "0x000280",
        "5549049301027910000280010480000100000000000000000000000000000000000000000000000000000002460000010000000000000000000000000000000000000000010000287f",
    ),
    (224, "0x0002dc", "5523042e010240100002dc0012010000020000000000000000000000000000000019e7"),
    (244, "0x0002dc", "5523042e010245100002dc0012010000020000000000000000000000000000000060f4"),
    (
        308,
        "0x000405",
        "553e044b04021913000405e3060000ffff80000000000179320500a92a0000cefcf4ffac1f983cef9550bff430143ff221d63c00000000010000000014a9",
    ),
    (
        328,
        "0x000405",
        "553e044b04022d13000405e3060000ffff800000000001dd320500a92a0000cefcf4ff182e983c209650bfae30143f2a1dd63c0000000001000000007e92",
    ),
    (
        350,
        "0x000405",
        "553e044b04025413000405e3060000ffff800000000001a5330500a92a0000cefcf4ff3820983cf39550bfe930143f632cd63c00000000010000000096eb",
    ),
    (
        370,
        "0x000405",
        "553e044b04026613000405e3060000ffff80000000000109340500a92a0000cefcf4ff1826983c189650bfbd30143f0d1ad63c000000000100000000321b",
    ),
    (
        390,
        "0x000405",
        "553e044b0402b916000405e3060000feff8000000000010d440500a92a0000cefcf3ffb621983c6c9550bfad31143ffb22d63c0000000001000000000d12",
    ),
    (
        410,
        "0x000405",
        "553e044b04022227000405e3060000feff800000000001bd930500a92a0000cefcf3ff1422983c6d9550bfab31143fcb21d63c00000000010000000006a0",
    ),
    (
        430,
        "0x000405",
        "553e044b0402d02f000405e3060000feff800000000001edbd0500a92a0000cefcf4ff9b25983c619550bfbd31143f1020d63c00000000010000000031be",
    ),
    (464, "0x000d02", "552f046305024d01000d020086100000ce010000000000000000000036010058000000000000200400000001018df2"),
    (511, "0x000427", "551204c704020d1300042700000800006d69"),
    (531, "0x000427", "551204c70402211300042700000800006d1c"),
    (551, "0x000427", "551204c70402331300042700000800007196"),
    (571, "0x000427", "551204c704025a130004270000080000b12e"),
    (
        616,
        "0x400081",
        "554d04a84802220340008168673231320000000000000000000000000000000000000000000000000000000208000000000000020800000000000000000000000000000000000000000000dc0e",
    ),
    (648, "0x000438", "551204c70402671300043800006464002678"),
    (668, "0x000438", "551204c704029f1600043800006464007dee"),
    (698, "0x00041c", "550e046604026b1300041c48e5e2"),
    (718, "0x00041c", "550e04660402a31600041c489ae2"),
    (750, "0x0000f1", "551504a9040273130000f100000000000000002057"),
    (
        797,
        "0x000099",
        "554804572802302000009902060000964800000000002e000f0063616d5f6c617073655f706172616d00000000000015000000000000000000000000000000000000000000002a20",
    ),
    (
        817,
        "0x000099",
        "553b04b42802312000009902060000974800000000002100070063616d5f666f76000000000000100000300000001b000001000000c4540000f4d6",
    ),
    (
        837,
        "0x000099",
        "553b04b42802332000009902060000994800000000002100150063616d5f736d6172745f67696d62616c5f6d6f64650000000000000200010035e4",
    ),
    (971, "0x40028e", "551104920208ffab40028e00011c003bc8"),
    (1004, "0x80028e", "551c041b0802ffab80028e0000011c0009000900000000000020e729"),
    (1116, "0x4007ab", "550d0433021bb0bb4007ab6633"),
]

# Field-by-field samples of the same file, copied from MD_SAMPLES in the ref script:
# (line, subsystem, msg id, type, payload, crc16, length, crc8); payload None = truncated in the notes
MD_SAMPLES = [
    (
        113,
        "0102",
        "4110",
        "000280",
        "010480000100000000000000000000000000000000000000000000000000000002460000010000000000000000000000000000000000000000010000",
        64535,
        73,
        147,
    ),
    (
        133,
        "0102",
        "4210",
        "000280",
        "010480000100000000000000000000000000000000000000000000000000000002460000010000000000000000000000000000000000000000010000",
        64153,
        73,
        147,
    ),
    (
        153,
        "0102",
        "4610",
        "000280",
        "010480000100000000000000000000000000000000000000000000000000000002460000010000000000000000000000000000000000000000010000",
        2942,
        73,
        147,
    ),
    (
        173,
        "0102",
        "4710",
        "000280",
        "010480000100000000000000000000000000000000000000000000000000000002460000010000000000000000000000000000000000000000010000",
        61707,
        73,
        147,
    ),
    (
        193,
        "0102",
        "7910",
        "000280",
        "010480000100000000000000000000000000000000000000000000000000000002460000010000000000000000000000000000000000000000010000",
        32552,
        73,
        147,
    ),
    (225, "0102", "4010", "0002dc", "00120100000200000000000000000000000000000000", 59161, 35, 46),
    (245, "0102", "4510", "0002dc", "00120100000200000000000000000000000000000000", 62560, 35, 46),
    (
        288,
        "0402",
        "4c12",
        "000405",
        "e3060000ffff800000000001912e0500a92a0000cefcf4ffee27983c069650bfd330143fee1ed63c000000000100000000",
        53611,
        62,
        75,
    ),
    (
        309,
        "0402",
        "1913",
        "000405",
        "e3060000ffff80000000000179320500a92a0000cefcf4ffac1f983cef9550bff430143ff221d63c000000000100000000",
        43284,
        62,
        75,
    ),
    (
        329,
        "0402",
        "2d13",
        "000405",
        "e3060000ffff800000000001dd320500a92a0000cefcf4ff182e983c209650bfae30143f2a1dd63c000000000100000000",
        37502,
        62,
        75,
    ),
    (
        351,
        "0402",
        "5413",
        "000405",
        "e3060000ffff800000000001a5330500a92a0000cefcf4ff3820983cf39550bfe930143f632cd63c000000000100000000",
        60310,
        62,
        75,
    ),
    (
        371,
        "0402",
        "6613",
        "000405",
        "e3060000ffff80000000000109340500a92a0000cefcf4ff1826983c189650bfbd30143f0d1ad63c000000000100000000",
        6962,
        62,
        75,
    ),
    (
        391,
        "0402",
        "b916",
        "000405",
        "e3060000feff8000000000010d440500a92a0000cefcf3ffb621983c6c9550bfad31143ffb22d63c000000000100000000",
        4621,
        62,
        75,
    ),
    (
        411,
        "0402",
        "2227",
        "000405",
        "e3060000feff800000000001bd930500a92a0000cefcf3ff1422983c6d9550bfab31143fcb21d63c000000000100000000",
        40966,
        62,
        75,
    ),
    (
        431,
        "0402",
        "d02f",
        "000405",
        "e3060000feff800000000001edbd0500a92a0000cefcf4ff9b25983c619550bfbd31143f1020d63c000000000100000000",
        48689,
        62,
        75,
    ),
    (
        465,
        "0502",
        "4d01",
        "000d02",
        "0086100000ce01000000000000000000003601005800000000000020040000000101",
        62093,
        47,
        99,
    ),
    (
        482,
        "0502",
        "3e39",
        "000d02",
        "0015110000000000000000000000000000cc01006400000000000020040000000001",
        1742,
        47,
        99,
    ),
    (512, "0402", "0d13", "000427", "0000080000", 26989, 18, 199),
    (532, "0402", "2113", "000427", "0000080000", 7277, 18, 199),
    (552, "0402", "3313", "000427", "0000080000", 38513, 18, 199),
    (572, "0402", "5a13", "000427", "0000080000", 11953, 18, 199),
    (
        617,
        "4802",
        "2203",
        "400081",
        "68673231320000000000000000000000000000000000000000000000000000000208000000000000020800000000000000000000000000000000000000000000",
        3804,
        77,
        168,
    ),
    (649, "0402", "6713", "000438", "0000646400", 30758, 18, 199),
    (669, "0402", "9f16", "000438", "0000646400", 61053, 18, 199),
    (699, "0402", "6b13", "00041c", "48", 58085, 14, 102),
    (719, "0402", "a316", "00041c", "48", 58010, 14, 102),
    (751, "0402", "7313", "0000f1", "0000000000000000", 22304, 21, 169),
    (
        798,
        "2802",
        "3020",
        "000099",
        "02060000964800000000002e000f0063616d5f6c617073655f706172616d0000000000001500000000000000000000000000000000000000000000",
        8234,
        72,
        87,
    ),
    (
        818,
        "2802",
        "3120",
        "000099",
        "02060000974800000000002100070063616d5f666f76000000000000100000300000001b000001000000c4540000",
        55028,
        59,
        180,
    ),
    (
        838,
        "2802",
        "3320",
        "000099",
        "02060000994800000000002100150063616d5f736d6172745f67696d62616c5f6d6f646500000000000002000100",
        58421,
        59,
        180,
    ),
    (871, "0802", "0000", "80ee03", "031900000000000020", 63394, 22, 252),
    (888, "0802", "0000", "80ee03", "031900000000000020", 63394, 22, 252),
    (914, "0702", "96bb", "c007ab", "00", 16442, 14, 102),
    (944, "0702", "0600", "4007ac", None, 64832, 244, 24),
    (972, "0208", "ffab", "40028e", "00011c00", 51259, 17, 146),
    (1005, "0802", "ffab", "80028e", "0000011c0009000900000000000020", 10727, 28, 27),
    (1031, "0802", "a2bb", "c0028e", "d6", 61817, 14, 102),
    (1060, "0288", "74aa", "400032", "3131000000", 27202, 18, 199),
    (1088, "0207", "76aa", "400707", "20", 4316, 14, 102),
    (1117, "021b", "b0bb", "4007ab", "", 13158, 13, 51),
    (1146, "021b", "0000", "c007ac", "01110200b5d0000000752b", 49792, 24, 32),
    (1165, "0207", "0400", "c00746", "00", 10293, 14, 102),
    (1184, "0702", "0400", "400746", "01", 29456, 14, 102),
    (1208, "0702", "72aa", "c00745", "0002", 26880, 15, 162),
    (1222, "0702", "fcab", "c00745", "0001", 24460, 15, 162),
    (1246, "2802", "5520", "400088", "1900", 51500, 15, 162),
    (1257, "2802", "c720", "400088", "1900", 52547, 15, 162),
    (1276, "0802", "feab", "c002e1", "00", 24970, 14, 102),
    (1295, "021b", "00ac", "4007ab", "", 63842, 13, 51),
    (1312, "0702", "00ac", "c007ab", "00", 39758, 14, 102),
    (1333, "0702", "198c", "c00747", "000000", 47347, 16, 86),
]


def test_all_captured_frames_decode_and_reencode():
    assert len(MD_VALUES) == 31
    for line, kind, text in MD_VALUES:
        raw = bytes.fromhex(text)
        decoded = Frame.decode(raw)
        assert decoded.encode() == raw, line
        assert f"0x{decoded.flags:02x}{decoded.cmd_set:02x}{decoded.cmd_id:02x}" == kind, line


def test_decoded_samples_rebuild_to_listed_length_and_checksums():
    checked = 0
    for line, subsystem, msg_id, kind, payload, crc, length, header_crc in MD_SAMPLES:
        if payload is None:
            continue
        sender, receiver = bytes.fromhex(subsystem)
        flags, cmd_set, cmd_id = bytes.fromhex(kind)
        raw = frame(sender, receiver, bytes.fromhex(msg_id), flags, cmd_set, cmd_id, bytes.fromhex(payload))
        assert (raw[1], raw[3], struct.unpack("<H", raw[-2:])[0]) == (length, header_crc, crc), line
        checked += 1
    assert checked == 50 and len(MD_SAMPLES) == 51


# -- camera -> app parsing ---------------------------------------------------------------------------


def test_battery_pushes():
    # message_types.md:442-491; moblin DjiDeviceMessage.swift:178-187; osmo-live client_test.go:72-127 (report §5.8)
    first = Frame.decode(
        H("552f046305024d01000d020086100000ce010000000000000000000036010058000000000000200400000001018df2")
    )
    assert (first.sender, first.receiver, first.flags, first.command) == (0x05, 0x02, 0x00, duml.CMD_BATTERY_PUSH)
    assert len(first.payload) == 34 and duml.parse_battery_percent(first.payload) == 0x58 == 88
    second = frame(
        0x05,
        0x02,
        H("3e39"),
        0x00,
        0x0D,
        0x02,
        H("0015110000000000000000000000000000cc01006400000000000020040000000001"),
    )
    assert second[-2:] == struct.pack("<H", 0x06CE) and second[31] == 100  # osmo-live reads absolute offset 31
    assert duml.parse_battery_percent(Frame.decode(second).payload) == 100
    assert struct.unpack("<H", first.payload[17:19])[0] == 310  # DJILib: temperature x10 at frame[28:30]
    # short frames carry it at offset 12 (djictl); nonsense values and short payloads give None
    assert duml.parse_battery_percent(bytes(12) + b"\x2a") == 42
    assert duml.parse_battery_percent(bytes(12)) is None and duml.parse_battery_percent(b"") is None
    assert duml.parse_battery_percent(bytes(20) + b"\xff") is None


def test_live_status_push():
    # captured on a Pocket 3 (message_types.md:850-897, MD_SAMPLES lines 871/888): 80 EE 03, payload 03 19 ...
    raw = frame(0x08, 0x02, H("0000"), 0x80, 0xEE, 0x03, H("031900000000000020"))
    assert (raw[1], raw[3], struct.unpack("<H", raw[-2:])[0]) == (22, 252, 63394)
    status = duml.parse_live_status(Frame.decode(raw).payload)
    assert status == duml.LiveStatus(0x03, 0x19) and not status.streaming and not status.failed
    assert status.name == "state 0x19"
    # DJILib.swift:660-675 (0x08 live, 0x09 ready) and dji-vcam protocol-notes §3.13 (Osmo Action 5 Pro):
    # "03 09" ready, "02 09" joined, "02 08 <n> ... 70 17" streaming, "02 79" failed
    assert duml.parse_live_status(H("0309")).name == "ready, not streaming"
    assert not duml.parse_live_status(H("0209")).streaming
    live = duml.parse_live_status(H("0208 05 00 7017"))
    assert live.streaming and live.name == "streaming" and (live.phase, live.state) == (2, duml.LIVE_STREAMING)
    failed = duml.parse_live_status(H("0279"))
    assert failed.failed and not failed.streaming and failed.name == "failed"
    assert duml.parse_live_status(b"\x02") is None and duml.parse_live_status(b"") is None


def test_result_codes():
    assert duml.parse_result(b"") is None and duml.parse_result(b"\x00\x01") == 0 and duml.parse_result(b"\xd6") == 0xD6
    assert duml.describe_result(0) == "ok" and duml.describe_result(0xD6) == "busy"  # [dji-vcam]
    assert duml.describe_result(0xE4) == "code 0xE4" and duml.describe_result(None) == "an empty reply"


# -- models ----------------------------------------------------------------------------------------


def identify(text: str):
    """Identify from manufacturer data that includes the two company-id bytes (the layout of the fixtures)."""
    raw = H(text)
    if len(raw) < 2:
        return None
    profile = duml.identify_model(int.from_bytes(raw[:2], "little"), raw[2:])
    if profile is None:
        return None
    return "unknown" if profile is duml.UNKNOWN_MODEL else profile.name


def test_model_identification_fixtures():
    # DJILib Tests/DJILibTests/DJILibTests.swift:9-32
    assert identify("FF") is None and identify("FFFFFFFFFFFFFFFFFFFF") is None
    assert identify("AA08FFFFFFFFFFFFFFFF") == "unknown"
    assert identify("AA081200") == "Osmo Action 3" and identify("AA081400") == "Osmo Action 4"
    assert identify("AA081500") == "Osmo Action 5 Pro" and identify("AA082000") == "Osmo Pocket 3"
    assert identify("AAF71400") == "Osmo Action 4" and identify("AAF71500") == "Osmo Action 5 Pro"  # Xtra rebadges
    assert identify("AAF72000") == "Osmo Pocket 3"
    # moblin DjiDeviceSuite.swift:73-94
    assert identify("AA081800FA0C9AE6A0975600") == "Osmo Action 6"
    assert identify("AA08000000CF000476EA8B20DA000010") == "Osmo Pocket 4 Pro"
    assert identify("AA08000000C10004FD9CD320DA000040") == "Osmo Pocket 4 Pro"
    # DJI's own scan screenshots (Osmo-GPS-Controller-Demo docs/images/*_bluetooth_scan_example.png)
    assert identify("AA08 1400FA60601F6011E7") == "Osmo Action 4"
    assert identify("AA08 1500FA60601FC7509600") == "Osmo Action 5 Pro"
    # the rest of the table in report §2.1
    assert identify("AA081000") == "Osmo Action 2" and identify("AA081700") == "Osmo 360"
    assert identify("AA081900") == "Osmo Nano" and identify("AA082100") == "Osmo Pocket 4"
    assert identify("AA080000") == "unknown" and identify("AA08") is None and identify("AA0814") is None
    assert identify("4C001400") is None  # another company


def test_model_table():
    # report §6: per-model gating
    table = {
        "action2": (None, "legacy", Confirm.NONE),
        "action3": (None, "legacy", Confirm.NONE),
        "action4": (0x08, "legacy", Confirm.AFTER_REPLY),
        "action5pro": (0x1A, "legacy", Confirm.BEHIND_START),
        "osmo360": (0x1A, "legacy", Confirm.BEHIND_START),
        "action6": (0x08, "json", Confirm.BEHIND_START),
        "pocket3": (None, "legacy", Confirm.AFTER_REPLY),
        "pocket4": (None, "json", Confirm.BEHIND_START),
        "pocket4pro": (None, "json", Confirm.BEHIND_START),
    }
    for key, (eis, fmt, confirm) in table.items():
        profile = duml.MODELS[key]
        assert (profile.eis_device_byte, profile.start_format, profile.confirm) == (eis, fmt, confirm), key
        assert profile.livestream and profile.key == key
    assert not duml.MODELS["nano"].livestream
    assert duml.MODELS["action6"].json_middle == H("fe00") and duml.MODELS["pocket4"].json_middle == H("0201")
    assert set(duml.MODELS) == set(table) | {"nano"}
    unknown = duml.UNKNOWN_MODEL
    assert (unknown.eis_device_byte, unknown.start_format, unknown.confirm) == (None, "legacy", Confirm.AFTER_REPLY)
    # the keys videonotes' config uses, and what the R SDK handshake reports, resolve to the same profiles
    from videonotes.dji import rsdk

    assert {duml.MODELS[key].name for key in rsdk.CAMERA_DEVICE_IDS.values()} == {
        "Osmo Action 4", "Osmo Action 5 Pro", "Osmo Action 6", "Osmo 360",
    }  # fmt: skip


def test_normalize_model():
    for text, key in (
        ("action4", "action4"), ("Action4", "action4"), ("Osmo Action 4", "action4"), ("DJI Osmo Action 4", "action4"),
        ("oa4", "action4"), ("action5pro", "action5pro"), ("Osmo Action 5 Pro", "action5pro"), ("OA5Pro", "action5pro"),
        ("action5", "action5pro"), ("osmo360", "osmo360"), ("360", "osmo360"), ("Osmo Pocket 3", "pocket3"),
        ("pocket4pro", "pocket4pro"), ("nano", "nano"),
    ):  # fmt: skip
        assert duml.normalize_model(text) == key, text
    for text in ("auto", "", None, "gopro", "osmo", "action7"):
        assert duml.normalize_model(text) is None
    assert duml.profile_for("auto") is duml.UNKNOWN_MODEL and duml.profile_for("oa4") is OA4


# -- validation --------------------------------------------------------------------------------------

GOOD = dict(rtmp_url="rtmp://192.168.1.10:1935/live/cam", resolution="1080p", fps=30, bitrate_kbps=4000)


def test_validate_stream_accepts_supported_values():
    for profile in (OA4, OA5, duml.UNKNOWN_MODEL, duml.MODELS["pocket3"]):
        for resolution in ("480p", "720p", "1080p", "1080", "720P", " 1080p ", "1920x1080", "854x480"):
            for fps in (25, 30):
                for kbps in (duml.MIN_BITRATE_KBPS, 4000, 6000, 10000, duml.MAX_BITRATE_KBPS):
                    name = duml.validate_stream(
                        profile, rtmp_url=GOOD["rtmp_url"], resolution=resolution, fps=fps, bitrate_kbps=kbps
                    )
                    assert name in duml.RESOLUTIONS
    assert duml.validate_stream(OA4, **GOOD) == "1080p"
    assert duml.validate_stream(OA4, **{**GOOD, "resolution": "1280x720"}) == "720p"
    assert duml.validate_stream(OA4, **GOOD, stabilization="rocksteady+") == "1080p"


@pytest.mark.parametrize(
    ("change", "message"),
    [
        ({"resolution": "4k"}, "480p, 720p or 1080p"),
        ({"resolution": "2.7k"}, "resolution"),
        ({"resolution": ""}, "resolution"),
        ({"fps": 60}, "25 or 30"),
        ({"fps": 24}, "25 or 30"),
        ({"fps": True}, "25 or 30"),
        ({"fps": "30"}, "25 or 30"),
        ({"bitrate_kbps": 999}, "1000 to 20000"),
        ({"bitrate_kbps": 20001}, "1000 to 20000"),
        ({"bitrate_kbps": 0}, "1000 to 20000"),
        ({"bitrate_kbps": -4000}, "1000 to 20000"),
        ({"bitrate_kbps": 4000.5}, "whole number"),
        ({"bitrate_kbps": "4000"}, "whole number"),
        ({"bitrate_kbps": True}, "whole number"),
        ({"stabilization": "max"}, "stabilisation"),
        ({"rtmp_url": ""}, "empty"),
        ({"rtmp_url": "http://192.168.1.10/live/cam"}, "rtmp://"),
        ({"rtmp_url": "rtmps://192.168.1.10/live/cam"}, "rtmp://"),
        ({"rtmp_url": "rtmp:///live/cam"}, "no host"),
        ({"rtmp_url": "rtmp://:1935/live/cam"}, "no host"),
        ({"rtmp_url": "rtmp://192.168.1.10:1935"}, "application and a stream name"),
        ({"rtmp_url": "rtmp://192.168.1.10:1935/"}, "application and a stream name"),
        ({"rtmp_url": "rtmp://192.168.1.10:1935/cam"}, "application and a stream name"),
        ({"rtmp_url": "rtmp://192.168.1.10:1935/live/"}, "application and a stream name"),
        ({"rtmp_url": "rtmp://192.168.1.10/live/my cam"}, "spaces or characters"),
        ({"rtmp_url": "rtmp://192.168.1.10/live/caméra"}, "spaces or characters"),
        ({"rtmp_url": "rtmp://192.168.1.10/live/cam\n"}, "spaces or characters"),
        ({"rtmp_url": "rtmp://h/live/" + "k" * 215}, "at most 228"),
        ({"rtmp_url": None}, "empty"),
    ],
)
def test_validate_stream_rejects(change, message):
    params = {**GOOD, **change}
    with pytest.raises(ValueError, match=message):
        duml.validate_stream(OA4, **params)


def test_validate_stream_limits_are_exact():
    longest = "rtmp://h/live/" + "k" * 214
    assert len(longest) == duml.MAX_URL_BYTES == 228
    duml.validate_rtmp_url(longest)
    assert len(duml.start_streaming(duml.start_payload_legacy(longest, "1080p", 30, 4000)).encode()) == 255
    duml.validate_rtmp_url("RTMP://Host.local:1935/app/key?token=a%20b")
    with pytest.raises(ValueError, match="cannot livestream"):
        duml.validate_stream(duml.MODELS["nano"], **GOOD)


def test_validate_wifi():
    duml.validate_wifi("Home", "password")  # 8 characters
    duml.validate_wifi("x" * 32, "p" * 63)
    duml.validate_wifi("Café ☕", "correct horse battery staple")
    duml.validate_wifi("Home", "ab" * 32)  # a 64-digit hexadecimal key
    duml.validate_wifi("Open network", "")  # nothing known against it
    for ssid, password, message in (
        ("", "password", "name is empty"),
        ("x" * 33, "password", "at most 32"),
        ("é" * 17, "password", "34 bytes"),
        ("Home", "short", "8 to 63"),
        ("Home", "p" * 64, "8 to 63"),
        ("Home", "ü" * 32, "8 to 63"),  # 64 bytes in UTF-8
        ("Ho\x00me", "password", "NUL"),
        ("Home", "pass\x00word", "NUL"),
        (None, "password", "text"),
        ("Home", 12345678, "text"),
    ):
        with pytest.raises(ValueError, match=message):
            duml.validate_wifi(ssid, password)
    with pytest.raises(ValueError, match="8 to 63"):
        duml.setup_wifi("Home", "short")
    assert duml.normalize_resolution("480") == "480p"
    with pytest.raises(ValueError, match="dji.stream_resolution"):
        duml.normalize_resolution("8k")


# -- reassembler -----------------------------------------------------------------------------------


def test_reassembler_cases_of_osmosis():
    # osmosis DumlReassemblerTest.kt: whole frame, split frame, two frames in one notification, garbage, noise
    one = duml.start_confirm().encode()
    assert [f.encode() for f in duml.Reassembler().feed(one)] == [one]
    reassembler = duml.Reassembler()
    cut = len(one) // 2
    assert reassembler.feed(one[:cut]) == []
    assert [f.encode() for f in reassembler.feed(one[cut:])] == [one]
    out = duml.Reassembler().feed(duml.prepare_livestream().encode() + duml.stop_streaming().encode())
    assert len(out) == 2 and out[0].cmd_id == 0xE1 and out[1].payload == H("01011a000102")
    assert [f.encode() for f in duml.Reassembler().feed(b"\x00\x11\x22" + one)] == [one]
    reassembler = duml.Reassembler()
    for _ in range(10):
        assert reassembler.feed(bytes([0x11]) * 100) == []
    assert len(reassembler.feed(one)) == 1 and reassembler.pending == 0 and reassembler.discarded == 1000


def test_reassembler_long_frame_in_20_byte_chunks():
    # ref script: a >255-byte frame split into 20-byte ATT chunks (10-bit length)
    big = frame(0x07, 0x02, H("0600"), 0x40, 0x07, 0xAC, bytes(range(256)) + bytes(44))
    reassembler = duml.Reassembler()
    got = []
    for i in range(0, len(big), 20):
        got += reassembler.feed(big[i : i + 20])
    assert [f.encode() for f in got] == [big]


def test_reassembler_skips_rsdk_frames_and_noise():
    # the same characteristic carries R SDK frames (start byte 0xAA); livestream_ble_sketch "rsdk_noise" scenario
    one = duml.prepare_livestream().encode()
    reassembler = duml.Reassembler()
    assert [f.encode() for f in reassembler.feed(b"\xaa\x1b\x00\x55\x10\x04\x00\x01" + one)] == [one]
    rsdk_status = H(
        "aa 31 00 01 00 00 00 00 56 3b cd ac 1d 02 01 01 10 03 01 00 00 00 00 00 00 00 00 00 00 d4 db 01"
        " 00 00 00 00 00 ea 27 00 00 00 00 00 00 b6 67 66 4b"
    )
    assert reassembler.feed(rsdk_status) == [] and reassembler.pending == 0


def test_reassembler_truncated_frame_does_not_block_the_next():
    reassembler = duml.Reassembler()
    big = frame(0x01, 0x02, H("4110"), 0x00, 0x02, 0x80, bytes(60))
    assert reassembler.feed(big[:40]) == [] and reassembler.pending == 40
    one = duml.stop_streaming().encode()
    assert [f.encode() for f in reassembler.feed(one)] == [one]
    assert reassembler.pending == 0 and reassembler.discarded == 40


def test_reassembler_buffer_is_bounded():
    with pytest.raises(ValueError):
        duml.Reassembler(max_buffer=10)
    reassembler = duml.Reassembler(max_buffer=1023)
    head = bytes([0x55, 0xFF, 0x07])  # announces 1023 bytes
    head += bytes([duml.crc8(head)])
    for _ in range(300):
        assert reassembler.feed(head + bytes(40)) == []
        assert reassembler.pending <= 1023
    one = duml.stop_streaming().encode()
    assert [f.encode() for f in reassembler.feed(one)] == [one]
    reassembler.feed(one[:5])
    reassembler.reset()
    assert reassembler.pending == 0


def _random_frame(rng: random.Random) -> bytes:
    payload = rng.randbytes(rng.choice([0, 1, 2, 6, 14, 34, 60, 242, 500]))
    return frame(rng.randrange(256), rng.randrange(256), rng.randbytes(2), rng.choice([0x00, 0x40, 0x80, 0xC0]),
                 rng.randrange(256), rng.randrange(256), payload)  # fmt: skip


def _packetise(rng: random.Random, stream: bytes) -> list[bytes]:
    pieces, i = [], 0
    while i < len(stream):
        size = rng.choice([1, 2, 3, 7, 20, 20, 20, 23, 61, 182, 244, 512])
        pieces.append(stream[i : i + size])
        i += size
    return pieces


@pytest.mark.parametrize("seed", range(40))
def test_reassembler_fuzz(seed):
    """Random frames, random garbage between them, truncated frames, random packetisation: every intact
    frame comes out, in order, as soon as its last byte has arrived, and nothing else does."""
    rng = random.Random(1000 + seed)
    stream = bytearray()
    expected: list[bytes] = []
    for _ in range(rng.randrange(1, 25)):
        kind = rng.random()
        one = _random_frame(rng)
        if kind < 0.60:
            stream += one
            expected.append(one)
        elif kind < 0.75:  # garbage, biased towards start bytes and plausible headers
            stream += bytes(rng.choice([0x55, 0xAA, 0x04, rng.randrange(256)]) for _ in range(rng.randrange(1, 60)))
        elif kind < 0.90:  # a frame that lost its tail
            stream += one[: rng.randrange(1, len(one))]
        else:  # a frame with one flipped bit
            broken = bytearray(one)
            broken[rng.randrange(len(broken))] ^= 1 << rng.randrange(8)
            stream += broken
    final = _random_frame(rng)  # an intact frame at the very end must not need any further input
    stream += final
    expected.append(final)
    reassembler = duml.Reassembler()
    got: list[bytes] = []
    for piece in _packetise(rng, bytes(stream)):
        got += [f.encode() for f in reassembler.feed(piece)]
        assert reassembler.pending <= 4096
    assert got == expected
    assert reassembler.pending == 0
