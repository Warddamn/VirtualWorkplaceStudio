"""Byte-exact tests of the DJI R SDK codec (videonotes.dji.rsdk).

Every vector says where it comes from.  "report" is the research report rsdk_ble.md;
"ref script" is rsdk_ble_ref.py and the *_verify.py scripts next to it.  The primary
sources behind them are DJI's demo repository (dji-sdk/Osmo-GPS-Controller-Demo, commit
92fe23e5) and frames from a real Osmo Action 4 / Osmo Action 5 Pro quoted in its issue #5.
"""

from __future__ import annotations

import random
import struct
import zlib

import pytest

from videonotes.dji import rsdk
from videonotes.dji.rsdk import CmdType, Frame, FrameError


def hx(text: str) -> bytes:
    return bytes.fromhex(text.replace("\n", " "))


# -- CRC known answers ---------------------------------------------------------------------


def test_crc_check_values():
    # report §4.1 / §4.2 ("Check value for ASCII 123456789"), printed by the ref script as well
    assert rsdk.crc16(b"123456789") == 0x2752
    assert rsdk.crc32(b"123456789") == 0xE4D9DC14
    assert rsdk.CRC16_INIT == 0x3AA3 and rsdk.CRC32_INIT == 0x00003AA3


def test_crc_tables_match_dji_tables():
    # report §4.1: custom_crc16.c first row and last entry; §4.2: custom_crc32.c first row and last entry
    assert list(rsdk._CRC16_TABLE[:8]) == [0x0000, 0xC0C1, 0xC181, 0x0140, 0xC301, 0x03C0, 0x0280, 0xC241]
    assert rsdk._CRC16_TABLE[-1] == 0x4040
    assert list(rsdk._CRC32_TABLE[:8]) == [
        0x00000000, 0x77073096, 0xEE0E612C, 0x990951BA, 0x076DC419, 0x706AF48F, 0xE963A535, 0x9E6495A3,
    ]  # fmt: skip
    assert rsdk._CRC32_TABLE[-1] == 0x2D02EF8D
    assert len(rsdk._CRC16_TABLE) == len(rsdk._CRC32_TABLE) == 256


def test_crc32_is_not_zlib():
    # report §4.2: same polynomial as zlib, different init and final XOR
    data = b"123456789"
    assert rsdk.crc32(data) != zlib.crc32(data)
    assert rsdk.crc32(data, 0xFFFFFFFF) ^ 0xFFFFFFFF == zlib.crc32(data)


def test_header_crc_of_truncated_demo_frames():
    # ref script V_HDR_1D06 / V_HDR_1D02: test/frame_check/frame_check.c:44,48 (README: "CRC-16 valid: 0x2C95")
    for header, crc in (
        (hx("aa 40 00 00 00 00 00 00 29 43 95 2c"), 0x2C95),
        (hx("AA 38 00 01 00 00 00 00 71 D5 3C 40"), 0x403C),
    ):
        assert rsdk.crc16(header[:10]) == crc == struct.unpack_from("<H", header, 10)[0]


# -- worked examples, report §8 (EX1..EX11) ----------------------------------------------------

MAC = bytes.fromhex("383456789ABC")  # placeholder MAC of DJI's demo

EXAMPLES = {
    # EX1: mode switch -> Hyperlapse; identical to docs/protocol_data_segment.md:165
    "EX1": (
        Frame(0x1D, 0x04, rsdk.mode_switch_payload(0x0A), CmdType.CMD_RESPONSE_OR_NOT, 5),
        "AA 1B 00 01 00 00 00 00 05 00 57 EE 1D 04 00 00 33 FF 0A 01 47 39 36 F4 FA E1 D0",
    ),
    # EX2: connection request, first pairing (verify_mode 1, code 1234)
    "EX2": (
        Frame(0x00, 0x19, rsdk.ConnectRequest(0x12345678, MAC, 1, 1234).pack(), CmdType.CMD_WAIT_RESULT, 1),
        "AA 33 00 02 00 00 00 00 01 00 98 2F 00 19 78 56 34 12 06 38 34 56 78 9A BC 00 00 00"
        " 00 00 00 00 00 00 00 00 00 00 00 00 01 D2 04 00 00 00 00 13 04 4F BD",
    ),
    # EX3: connection response to the camera's request; identical to the TX line in docs/images/debug_info.png
    "EX3": (
        Frame(0x00, 0x19, rsdk.ConnectResponse(0x12345678, 0, 0).pack(), CmdType.ACK_NO_RESPONSE, 0x08AF),
        "AA 1B 00 20 00 00 00 00 AF 08 19 8A 00 19 78 56 34 12 00 00 00 00 00 B8 24 CB 17",
    ),
    # EX4: version query; identical to the second TX line in docs/images/debug_info.png
    "EX4": (
        Frame(0x00, 0x00, b"", CmdType.CMD_WAIT_RESULT, 2),
        "AA 12 00 02 00 00 00 00 02 00 0C 8E 00 00 20 F6 F2 F3",
    ),
    # EX5: status subscription (push_mode 3, push_freq 20)
    "EX5": (
        Frame(0x1D, 0x05, rsdk.status_subscribe_payload(3, 20), CmdType.CMD_NO_RESPONSE, 3),
        "AA 18 00 00 00 00 00 00 03 00 50 7E 1D 05 03 14 00 00 00 00 5F 99 15 FA",
    ),
    # EX6 / EX7: start / stop recording
    "EX6": (
        Frame(0x1D, 0x03, rsdk.record_payload(True), CmdType.CMD_RESPONSE_OR_NOT, 4),
        "AA 1B 00 01 00 00 00 00 04 00 56 7E 1D 03 00 00 FF 33 00 00 00 00 00 6E B6 FF 11",
    ),
    "EX7": (
        Frame(0x1D, 0x03, rsdk.record_payload(False), CmdType.CMD_RESPONSE_OR_NOT, 5),
        "AA 1B 00 01 00 00 00 00 05 00 57 EE 1D 03 00 00 FF 33 01 00 00 00 00 AF 1F 2D 24",
    ),
    # EX8 / EX9: key report, record key / QS key short press
    "EX8": (
        Frame(0x00, 0x11, rsdk.key_report_payload(rsdk.KEY_RECORD), CmdType.CMD_RESPONSE_OR_NOT, 6),
        "AA 16 00 01 00 00 00 00 06 00 0F 8E 00 11 01 01 00 00 8A D9 AA 12",
    ),
    "EX9": (
        Frame(0x00, 0x11, rsdk.key_report_payload(rsdk.KEY_QS), CmdType.CMD_RESPONSE_OR_NOT, 7),
        "AA 16 00 01 00 00 00 00 07 00 0E 1E 00 11 02 01 00 00 F8 6B BF CC",
    ),
    # EX10: sleep
    "EX10": (
        Frame(0x00, 0x1A, rsdk.power_mode_payload(rsdk.POWER_SLEEP), CmdType.CMD_RESPONSE_OR_NOT, 8),
        "AA 13 00 01 00 00 00 00 08 00 34 BE 00 1A 03 71 1E 22 3D",
    ),
    # EX11: mode switch -> Video
    "EX11": (
        Frame(0x1D, 0x04, rsdk.mode_switch_payload(rsdk.MODE_VIDEO), CmdType.CMD_RESPONSE_OR_NOT, 9),
        "AA 1B 00 01 00 00 00 00 09 00 52 EE 1D 04 00 00 33 FF 01 01 47 39 36 12 D1 EB FF",
    ),
}


@pytest.mark.parametrize("name", sorted(EXAMPLES))
def test_worked_examples_encode_and_decode(name):
    frame, text = EXAMPLES[name]
    raw = hx(text)
    assert frame.encode() == raw
    assert len(raw) == rsdk.FRAME_OVERHEAD + len(frame.payload)  # report §4: frame = 18 + payload
    decoded = Frame.decode(raw)
    assert decoded == Frame(frame.cmd_set, frame.cmd_id, frame.payload, int(frame.cmd_type), frame.seq)
    assert decoded.encode() == raw


def test_example_field_breakdown():
    # report §8, tables under EX1 and EX2
    raw = hx(EXAMPLES["EX1"][1])
    assert raw[1:3] == hx("1B 00") and raw[8:10] == hx("05 00") and raw[10:12] == hx("57 EE")
    assert raw[14:18] == hx("00 00 33 FF") and raw[18] == 0x0A and raw[19:23] == hx("01 47 39 36")
    assert struct.unpack("<I", raw[-4:])[0] == 0xD0E1FAF4 == rsdk.crc32(raw[:-4])
    request = rsdk.ConnectRequest.unpack(Frame.decode(hx(EXAMPLES["EX2"][1])).payload)
    assert request == rsdk.ConnectRequest(0x12345678, MAC, 1, 1234)
    assert (request.fw_version, request.conidx, request.reserved) == (0, 0, bytes(4))


# -- vectors from DJI's repository ---------------------------------------------------------------

# test/connect_cmd_frame_builder/connect_cmd_frame.txt, lines 1-10 (report §9 row 2; line 1 is V_CONNECT_1
# in the ref script).  All: device_id 0x12345678, placeholder MAC, verify_mode 0, SEQ 1.
CONNECT_FRAMES = """
AA330002000000000100982F00197856341206383456789ABC00000000000000000000000000000000FE1F00000000796C667C
AA330002000000000100982F00197856341206383456789ABC00000000000000000000000000000000191A0000000033C8C7BF
AA330002000000000100982F00197856341206383456789ABC000000000000000000000000000000008F1200000000AC768844
AA330002000000000100982F00197856341206383456789ABC00000000000000000000000000000000050B00000000E1B45396
AA330002000000000100982F00197856341206383456789ABC000000000000000000000000000000004F0E000000009B1270F0
AA330002000000000100982F00197856341206383456789ABC00000000000000000000000000000000B71F00000000DD373154
AA330002000000000100982F00197856341206383456789ABC00000000000000000000000000000000501000000000368B20DD
AA330002000000000100982F00197856341206383456789ABC00000000000000000000000000000000B82100000000EF8376BB
AA330002000000000100982F00197856341206383456789ABC00000000000000000000000000000000100C00000000D9FB6877
AA330002000000000100982F00197856341206383456789ABC00000000000000000000000000000000E10200000000048F9616
""".split()
CONNECT_CODES = [8190, 6681, 4751, 2821, 3663, 8119, 4176, 8632, 3088, 737]  # report §9 row 2


@pytest.mark.parametrize(("line", "code"), list(zip(CONNECT_FRAMES, CONNECT_CODES, strict=True)))
def test_dji_connection_request_frames(line, code):
    raw = bytes.fromhex(line)
    frame = Frame.decode(raw)
    assert (frame.command, frame.cmd_type, frame.seq) == (rsdk.CMD_CONNECT, CmdType.CMD_WAIT_RESULT, 1)
    request = rsdk.ConnectRequest.unpack(frame.payload)
    assert request == rsdk.ConnectRequest(0x12345678, MAC, rsdk.VERIFY_NONE, code)
    assert Frame(0x00, 0x19, request.pack(), CmdType.CMD_WAIT_RESULT, 1).encode() == raw


def test_handshake_start_reproduces_dji_frame():
    # the state machine's step-1 frame for an already-paired controller == connect_cmd_frame.txt line 1
    handshake = rsdk.ConnectHandshake(0x12345678, MAC, 8190, first_pairing=False)
    assert handshake.start(1).encode() == bytes.fromhex(CONNECT_FRAMES[0])
    # ... and for a first pairing == EX2
    assert rsdk.ConnectHandshake(0x12345678, MAC, 1234, first_pairing=True).start(1).encode() == hx(EXAMPLES["EX2"][1])


# test/test_gps.c:31-97, 13 packets of 66 bytes (report §9 row 3; the first is V_GPS_1 in the ref script)
GPS_FRAMES = """
aa420000000000000300d2dd00174f0035018aa50200bcb2e943a34f750db96d0000de5824418d9ac54100000000e8030000e80300000a0000000e00000063b5d131
aa420000000000000500d17d00174f0035018ba50200cfb2e943914f750da56d00007fb417414767b64100000000e8030000e80300000a0000000e000000fd488f12
aa420000000000000600d18d00174f0035018ca50200d5b2e943a04f750d866d00001e3370401867104100000000e8030000e80300000a0000000e000000c42426ba
aa420000000000000700d01d00174f0035018da50200e2b2e9438f4f750d7e6d00001e33f0401867904100000000e8030000e80300000a0000000e000000df24cc0d
aa420000000000000800d5ed00174f0035018ea50200e0b2e943a04f750d716d00001e33f0401867904100000000e8030000e80300000a0000000d000000d4862c50
aa420000000000000a00d48d00174f00350190a50200ebb2e943a44f750d376d00007fb417414767b64100000000e8030000e80300000a0000000d000000858d2e99
aa420000000000000b00d51d00174f00350191a50200feb2e9438f4f750d446d00000eabaa4030344d4100000000e8030000e80300000a0000000e000000b11d3aeb
aa420000000000000c00d72d00174f00350192a50200ddb2e943984f750d606d0000d9d90bc01b8807c200000000e8030000e80300000a0000000e000000a9427058
aa420000000000000e00d64d00174f003501bca5020073b2e9439e4f750d716d000014419040b1da48c200000000e8030000e80300000a0000000e0000009f32b985
aa420000000000001000dfed00174f003501bea50200e6b1e943734f750d9b6d0000bb3213400ef4ccc100000000e8030000e80300000a0000000e00000062969bb4
aa420000000000001200de8d00174f003501c0a5020037b1e9436d4f750dc06d000050451b4032816ec200000000e8030000e80300000a0000000d0000008ae8f354
aa420000000000001400dd2d00174f003501c2a50200efafe943714f750d336e0000f40ea740a42ce4c200000000e8030000e80300000a0000000e000000031e036c
aa420000000000001700dddd00174f003501c5a5020014ade943794f750da86e0000203f75c1c21d6bc300000000e8030000e80300000a0000000d00000076a5129e
""".split()


@pytest.mark.parametrize("line", GPS_FRAMES)
def test_dji_gps_frames_round_trip(line):
    raw = bytes.fromhex(line)
    frame = Frame.decode(raw)
    assert frame.command == rsdk.CMD_GPS_PUSH and frame.cmd_type == CmdType.CMD_NO_RESPONSE and len(frame.payload) == 48
    gps = rsdk.GpsPush.unpack(frame.payload)
    assert Frame(0x00, 0x17, gps.pack(), CmdType.CMD_NO_RESPONSE, frame.seq).encode() == raw


def test_first_gps_frame_values():
    # report §6.11: "date 20250703, time field 173450, lon 113.9389116, lat 22.5791907, height 28089 mm, 14 satellites"
    gps = rsdk.GpsPush.unpack(Frame.decode(bytes.fromhex(GPS_FRAMES[0])).payload)
    assert (gps.year_month_day, gps.hour_minute_second, gps.height_mm, gps.satellites) == (20250703, 173450, 28089, 14)
    assert gps.longitude_e7 == 1139389116 and gps.latitude_e7 == 225791907
    assert gps.speed_north_cm_s == pytest.approx(10.27, abs=0.01) and gps.speed_east_cm_s == pytest.approx(
        24.70, abs=0.01
    )
    assert (gps.vertical_accuracy_mm, gps.horizontal_accuracy_mm, gps.speed_accuracy_cm_s) == (1000, 1000, 10)
    with pytest.raises(ValueError, match="48"):
        rsdk.GpsPush.unpack(bytes(47))


def test_snapshot_key_report_frame():
    # ref script V_KEY_SNAPSHOT: logic/key_logic.c:216 (key 3, mode 1, value 0, SEQ 0x1200)
    raw = bytes.fromhex("AA1600010000000000128C23001103010000263B43CC")
    frame = Frame(0x00, 0x11, rsdk.key_report_payload(rsdk.KEY_SNAPSHOT, 1, 0), CmdType.CMD_RESPONSE_OR_NOT, 0x1200)
    assert frame.encode() == raw and Frame.decode(raw).seq == 0x1200


def test_pre_2025_09_documentation_example():
    # report §9 V7: the mode-switch example before commit 946defe (device_id 0x33FF0000, SEQ written big-endian)
    raw = hx("AA 1B 00 01 00 00 00 00 00 03 14 BF 1D 04 00 00 FF 33 0A 01 47 39 36 92 A1 09 55")
    frame = Frame.decode(raw)
    assert frame.seq == 0x0300 and frame.payload == rsdk.mode_switch_payload(0x0A, device_id=0x33FF0000)


# -- frames transcribed from DJI's log screenshot (docs/images/debug_info.png) ---------------------

# ref script V_IMG_RX_1D06 / rsdk_ble_screenshot_verify.py rx1
RX_1D06 = hx(
    "AA 40 00 00 00 00 00 00 1A D3 81 B0 1D 06 01 0A 53 55 50 45 52 4E 49 47 48 54"
    + " 00" * 11 + " 02 07 31 30 38 30 50 33 30" + " 00" * 14 + " 4B 83 56 DF"
)  # fmt: skip
# ref script V_IMG_RX_VERSION / rsdk_ble_screenshot_verify.py rx2
RX_VERSION = hx(
    "AA 72 00 20 00 00 00 00 02 00 A6 8E 00 00 00 00 44 4A 49 2D 41 43 54 49 4F 4E 34 00 00 00 00 00"
    " 53 44 4B 2D 76 31 2E 31 20 44 45 42 55 47 20 41 43 32 30 33 2D 30 33 2E 30 34 2E 38 30 2E 31 35"
    + " 00" * 46 + " E3 D4 12 07"
)  # fmt: skip


def test_screenshot_new_status_push():
    frame = Frame.decode(RX_1D06)
    assert len(RX_1D06) == 64 and frame.command == rsdk.CMD_NEW_STATUS_PUSH
    assert (frame.cmd_type, frame.seq) == (0x00, 0xD31A)  # report §6.7
    push = rsdk.NewStatusPush.unpack(frame.payload)
    assert push == rsdk.NewStatusPush("SUPERNIGHT", "1080P30", 0x01, 0x02)
    with pytest.raises(ValueError, match="46"):
        rsdk.NewStatusPush.unpack(frame.payload[:45])


def test_new_status_push_clamps_declared_lengths():
    payload = bytearray(Frame.decode(RX_1D06).payload)
    payload[1], payload[24] = 200, 255  # nonsense lengths must not run into the next field
    push = rsdk.NewStatusPush.unpack(bytes(payload))
    assert push.mode_name == "SUPERNIGHT" and push.mode_param == "1080P30"


def test_screenshot_version_response():
    frame = Frame.decode(RX_VERSION)
    assert len(RX_VERSION) == 114 and (frame.command, frame.cmd_type, frame.seq) == (rsdk.CMD_VERSION, 0x20, 2)
    info = rsdk.VersionInfo.unpack(frame.payload)
    assert info == rsdk.VersionInfo(0, "DJI-ACTION4", "SDK-v1.1 DEBUG AC203-03.04.80.15")
    with pytest.raises(ValueError):
        rsdk.VersionInfo.unpack(b"\x00")


def test_partial_status_body_from_frame_check():
    # ref script V_1D02_PARTIAL (test/frame_check/frame_check.c:48): first 31 payload bytes of a status push
    body = hx("3C 01 0E 03 00 00 00 00 00 00 00 00 00 00 00 74 25 01 00 00 00 00 00 BA 16 00 00 00 00 00 00")
    status = rsdk.StatusPush.unpack(body)
    # report §6.6 notes: mode 0x3C, status 1, resolution 14 (undocumented), fps_idx 3, 75124 MB, 5818 s
    assert (status.camera_mode, status.camera_status, status.video_resolution, status.fps_idx) == (0x3C, 1, 14, 3)
    assert (status.remain_capacity, status.remain_time) == (75124, 5818)
    assert status.mode_name == "Selfie" and status.resolution_name == "resolution code 14"
    assert status.camera_bat_percentage is None and status.payload_length == 31


# -- frames captured from real cameras (upstream issue #5; rsdk_ble_issue5_verify.py, report §5.1.1, §6.5, §6.6) --

CAPTURED = {
    "OA5Pro step 2": "aa 1b 00 20 00 00 00 00 00 01 a4 7c 00 19 44 ff 00 00 00 00 00 00 00 42 d8 ed 0f",
    "OA4 step 2": "aa 1b 00 20 00 00 00 00 00 01 a4 7c 00 19 33 ff 00 00 00 00 00 00 00 5e 76 2f 9b",
    "OA5Pro step 3": "aa 33 00 02 00 00 00 00 01 00 98 2f 00 19 44 ff" + " 00" * 16
    + " 00 00 00 00 00 00 00 00 02 00 00 00 00 00 00 e1 ea 9c 15",
    "OA4 step 3": "aa 33 00 02 00 00 00 00 73 00 bc 8f 00 19 33 ff" + " 00" * 16
    + " 00 00 00 00 00 00 00 00 02 00 00 00 00 00 00 0d 64 a7 26",
    "1D05 response": "aa 17 00 20 00 00 00 00 00 03 70 bd 1d 05 00 00 00 00 00 66 46 32 67",
    "OA4 status": "aa 31 00 01 00 00 00 00 56 3b cd ac 1d 02 01 01 10 03 01 00 00 00 00 00 00 00 00 00 00 d4 db 01"
    " 00 00 00 00 00 ea 27 00 00 00 00 00 00 b6 67 66 4b",
    "OA5Pro status": "aa 38 00 01 00 a1 49 00 b4 7e 85 2a 1d 02 05 01 04 01 00 00 00 00 01 00 00 00 00 00 00 59 db 01"
    " 00 ab 8f 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 5c e9 7b eb 94",
    "OA5Pro version": "aa 72 00 20 00 00 00 00 00 02 26 2f 00 00 00 00 44 4a 49 2d 41 43 54 49 4f 4e 34 00 00 00 00 00"
    " 53 44 4b 2d 76 31 2e 31 20 44 45 42 55 47 20 41 43 32 30 33 2d 30 33 2e 30 34 2e 38 30 2e 31 35"
    + " 00" * 46 + " 7d 60 0a 8d",
    "controller GPS": "AA 42 00 00 00 00 00 00 D8 1B C8 26 00 17 1E 01 35 01 58 B3 01 00 14 06 27 5B FC EC 99 EF 7F 4F"
    " 00 00 E8 B5 67 C1 0D A7 BD C1 00 00 40 40 E8 03 00 00 E8 03 00 00 0A 00 00 00 13 00 00 00 2A EF 4A 0D",
}  # fmt: skip


@pytest.mark.parametrize("name", sorted(CAPTURED))
def test_captured_frames_decode_and_reencode(name):
    raw = hx(CAPTURED[name])
    frame = Frame.decode(raw)  # both CRCs valid
    assert frame.encode() == raw  # including the non-zero RES bytes of the Action 5 Pro push


def test_captured_handshake_frames():
    for model, device_id in (("OA5Pro", 0xFF44), ("OA4", 0xFF33)):
        step2 = Frame.decode(hx(CAPTURED[f"{model} step 2"]))
        assert step2.is_response and step2.cmd_type == 0x20 and step2.seq == 0x0100  # SEQ bytes 00 01 echoed
        response = rsdk.ConnectResponse.unpack(step2.payload)
        assert (response.device_id, response.ret_code, response.camera_number) == (device_id, 0, 0)
        assert step2.payload[:4] == struct.pack("<I", device_id)  # wire bytes 44 FF 00 00 / 33 FF 00 00
        step3 = Frame.decode(hx(CAPTURED[f"{model} step 3"]))
        assert not step3.is_response and step3.cmd_type == 0x02 and len(step3.payload) == 33
        request = rsdk.ConnectRequest.unpack(step3.payload)
        assert request == rsdk.ConnectRequest(device_id, b"", rsdk.VERIFY_RESULT, 0)  # mac_addr_len 0, allowed
    assert Frame.decode(hx(CAPTURED["OA5Pro step 3"])).seq == 0x0001
    assert Frame.decode(hx(CAPTURED["OA4 step 3"])).seq == 0x0073
    assert rsdk.model_from_device_id(0xFF33) == "action4" and rsdk.model_from_device_id(0xFF44) == "action5pro"
    assert rsdk.model_from_device_id(0xFF55) == "action6" and rsdk.model_from_device_id(0xFF66) == "osmo360"
    assert rsdk.model_from_device_id(0x12345678) is None


def test_captured_status_subscription_response():
    frame = Frame.decode(hx(CAPTURED["1D05 response"]))
    assert len(hx(CAPTURED["1D05 response"])) == 23
    assert frame.command == rsdk.CMD_STATUS_SUBSCRIBE and frame.is_response and frame.payload == bytes(5)
    assert rsdk.parse_return_code(frame.payload) == 0


def test_captured_action4_status_push_is_31_bytes():
    frame = Frame.decode(hx(CAPTURED["OA4 status"]))
    assert len(hx(CAPTURED["OA4 status"])) == 49 and frame.cmd_type == 0x01 and len(frame.payload) == 31
    status = rsdk.StatusPush.unpack(frame.payload)
    # report §6.6: Video, idle, 4K 16:9 (16), 30 fps (3), EIS RS (1), 121812 MB, 10218 s, power 0, temp 0
    assert (status.camera_mode, status.camera_status, status.video_resolution, status.fps_idx, status.eis_mode) == (
        1,
        1,
        16,
        3,
        1,
    )
    assert (status.remain_capacity, status.remain_time, status.power_mode, status.temp_over) == (121812, 10218, 0, 0)
    # ... and the payload ends after temp_over
    assert status.photo_countdown_ms is None and status.loop_record_sends is None
    assert status.camera_bat_percentage is None
    assert status.mode_name == "Video" and status.state_name == "idle" and status.is_recording is False
    assert status.resolution_name == "4K 16:9" and status.fps == 30 and status.stabilization_name == "RockSteady"
    assert status.temperature_name == "normal" and status.is_sleeping is False
    assert status.camera_mode_next_flag == 0  # not equal to camera_mode, contrary to the docs (§6.6)


def test_captured_action5pro_status_push_is_38_bytes():
    frame = Frame.decode(hx(CAPTURED["OA5Pro status"]))
    assert len(hx(CAPTURED["OA5Pro status"])) == 56 and frame.res == hx("A1 49 00") and len(frame.payload) == 38
    status = rsdk.StatusPush.unpack(frame.payload)
    # report §6.6: Photo (5), idle, photo size L (4), fps_idx 1, ratio 16:9, 121689 MB, 36779 photos, battery 92 %
    assert (status.camera_mode, status.camera_status, status.video_resolution, status.fps_idx) == (5, 1, 4, 1)
    assert (status.photo_ratio, status.remain_capacity, status.remain_photo_num) == (1, 121689, 36779)
    assert (status.power_mode, status.temp_over, status.camera_bat_percentage) == (0, 0, 92)
    assert status.mode_name == "Photo" and status.resolution_name == "L" and status.fps is None
    assert status.is_photo_mode and status.payload_length == 38
    assert set(status.as_dict()) == {name for name, _ in rsdk._STATUS_FIELDS} and len(status.as_dict()) == 21


def test_captured_version_response_does_not_identify_the_model():
    # report §6.8: an Action 5 Pro answers "DJI-ACTION4"
    info = rsdk.VersionInfo.unpack(Frame.decode(hx(CAPTURED["OA5Pro version"])).payload)
    assert info == rsdk.VersionInfo(0, "DJI-ACTION4", "SDK-v1.1 DEBUG AC203-03.04.80.15")


def test_captured_controller_gps_frame():
    gps = rsdk.GpsPush.unpack(Frame.decode(hx(CAPTURED["controller GPS"])).payload)
    assert gps.year_month_day == 20250910 and gps.satellites == 19


# -- status push: decode by length ---------------------------------------------------------------


def test_status_push_documented_layout_is_38_bytes():
    assert rsdk.STATUS_PUSH_FULL_LEN == 38 == struct.calcsize("<BBBBBHBBHHHIIIBBBBIHB")  # report §6.6


@pytest.mark.parametrize("length", range(0, 45))
def test_status_push_never_raises_and_reports_missing_fields(length):
    full = struct.pack(
        "<BBBBBHBBHHHIIIBBBBIHB", 1, 3, 10, 6, 2, 754, 0, 1, 9, 5, 60, 1000, 20, 3000, 2, 3, 1, 2, 500, 300, 77
    )
    payload = (full + b"\xee" * 10)[:length]
    status = rsdk.StatusPush.unpack(payload)
    offset = 0
    for name, code in rsdk._STATUS_FIELDS:
        size = struct.calcsize("<" + code)
        expected = struct.unpack_from("<" + code, full, offset)[0] if offset + size <= length else None
        assert getattr(status, name) == expected, name
        offset += size
    assert status.payload_length == length
    if length >= 38:  # extra trailing bytes are ignored
        assert status.camera_bat_percentage == 77 and status.is_recording is True and status.is_sleeping is True
        assert status.record_time == 754 and status.fps == 60 and status.resolution_name == "1080p"
        assert status.stabilization_name == "HorizonSteady" and status.temperature_name == "too hot to record"


def test_status_push_empty_and_unknown_values():
    empty = rsdk.StatusPush.unpack(b"")
    assert empty.is_recording is None and empty.is_sleeping is None and empty.mode_name is None
    assert empty.state_name is None and empty.resolution_name is None and empty.fps is None
    assert empty.stabilization_name is None and empty.temperature_name is None
    odd = rsdk.StatusPush.unpack(bytes([0x7E, 9, 200, 99, 9]) + bytes(26))
    assert odd.mode_name == "mode 0x7E" and odd.state_name == "state 9" and odd.fps is None
    assert odd.stabilization_name == "mode 9" and odd.is_recording is False
    pre = rsdk.StatusPush.unpack(bytes([1, 5]))
    assert pre.is_recording is True and pre.state_name == "pre-recording"


# -- frame validation ----------------------------------------------------------------------------


def test_corrupted_frames_are_rejected():
    good = hx(EXAMPLES["EX1"][1])
    bad = bytearray(good)
    bad[18] ^= 1  # ref script: "corrupted payload byte is rejected with CRC-32 mismatch"
    with pytest.raises(FrameError, match="CRC-32"):
        Frame.decode(bytes(bad))
    bad = bytearray(good)
    bad[8] ^= 1  # ref script: "corrupted header byte is rejected with CRC-16 mismatch"
    with pytest.raises(FrameError, match="CRC-16"):
        Frame.decode(bytes(bad))
    with pytest.raises(FrameError, match="length"):
        Frame.decode(good + b"\x00")
    with pytest.raises(FrameError, match="length"):
        Frame.decode(good[:-1])
    with pytest.raises(FrameError, match="short"):
        Frame.decode(good[:10])
    with pytest.raises(FrameError, match="start byte"):
        Frame.decode(b"\x55" + good[1:])


def test_frame_without_data_segment_is_rejected():
    # report §4: a 16-byte frame has an empty DATA segment and the demo drops it
    head = struct.pack("<BHBB3sH", 0xAA, 16, 0, 0, bytes(3), 7)
    head += struct.pack("<H", rsdk.crc16(head))
    raw = head + struct.pack("<I", rsdk.crc32(head))
    with pytest.raises(FrameError, match="DATA"):
        Frame.decode(raw)


def test_encode_validates_fields():
    assert len(Frame(1, 2, bytes(rsdk.MAX_PAYLOAD_LEN)).encode()) == 1023
    with pytest.raises(FrameError, match="1023"):
        Frame(1, 2, bytes(rsdk.MAX_PAYLOAD_LEN + 1)).encode()
    with pytest.raises(FrameError, match="seq"):
        Frame(1, 2, seq=0x10000).encode()
    with pytest.raises(FrameError, match="cmd_id"):
        Frame(1, 256).encode()
    with pytest.raises(FrameError, match="res"):
        Frame(1, 2, res=b"\x00").encode()
    frame = Frame(0x1D, 0x03, b"\x01", CmdType.ACK_NO_RESPONSE, 0xFFFF, version=1)
    decoded = Frame.decode(frame.encode())
    assert decoded.version == 1 and decoded.seq == 0xFFFF and decoded.is_response and decoded.response_type == 0
    assert Frame(1, 2, cmd_type=CmdType.CMD_WAIT_RESULT).response_type == 2
    assert rsdk.build(rsdk.CMD_RECORD, b"\x00", 0x1FFFF).seq == 0xFFFF


def test_payload_builders_validate():
    with pytest.raises(ValueError):
        rsdk.power_mode_payload(1)
    assert rsdk.power_mode_payload(rsdk.POWER_NORMAL) == b"\x00"
    with pytest.raises(ValueError):
        rsdk.mode_switch_payload(256)
    with pytest.raises(ValueError):
        rsdk.mode_switch_payload(1, reserved=b"\x00")
    with pytest.raises(ValueError):
        rsdk.ConnectRequest(1, bytes(17)).pack()
    with pytest.raises(ValueError):
        rsdk.ConnectRequest.unpack(bytes(32))
    with pytest.raises(ValueError):
        rsdk.ConnectResponse.unpack(bytes(4))
    # the demo's struct for some responses is shorter than the documented 9 bytes: tolerate a missing tail
    assert rsdk.ConnectResponse.unpack(struct.pack("<IB", 0xFF33, 2)) == rsdk.ConnectResponse(0xFF33, 2, 0)
    assert rsdk.restart_payload(0x12345678) == hx("78 56 34 12 00 00 00 00")  # report §6.12 layout
    assert rsdk.record_payload(True)[:4] == hx("00 00 FF 33") and rsdk.mode_switch_payload(1)[:4] == hx("00 00 33 FF")
    assert rsdk.parse_return_code(b"") is None and rsdk.parse_return_code(b"\x02\x00\x00\x00\x00") == 2
    assert rsdk.describe_return_code(0) == "ok" and "0x7B" in rsdk.describe_return_code(0x7B)
    assert "carry out" in rsdk.describe_return_code(2)


# -- advertising helpers -------------------------------------------------------------------------


def test_wake_advertisement_vectors():
    # ref script: docs/images/oa4_wakeup_adv.png and oa5pro_wakeup_adv.png
    assert rsdk.wake_advertisement(bytes.fromhex("60601F6011E7")) == bytes.fromhex("0AFF574B50E711601F6060")
    assert rsdk.wake_advertisement(bytes.fromhex("60601FC75096")) == bytes.fromhex("0AFF574B509650C71F6060")
    with pytest.raises(ValueError):
        rsdk.wake_advertisement(b"\x01\x02")


def test_rsdk_camera_marker():
    # ref script is_supported_camera_mfr: the two scan screenshots (company 08AA, data after the company id)
    assert rsdk.is_rsdk_camera(0x08AA, bytes.fromhex("1400FA60601F6011E7"))
    assert rsdk.is_rsdk_camera(0x08AA, bytes.fromhex("1500FA60601FC7509600"))
    assert not rsdk.is_rsdk_camera(0x004C, bytes.fromhex("1400FA60601F6011E7"))
    assert not rsdk.is_rsdk_camera(0x08AA, bytes.fromhex("1400"))
    assert not rsdk.is_rsdk_camera(0x08AA, bytes.fromhex("19000060601F6011E703"))  # Osmo Nano: 00 instead of FA


# -- reassembler ---------------------------------------------------------------------------------

MODE_SWITCH = hx(EXAMPLES["EX1"][1])


def test_reassembler_reference_case():
    # ref script: "3 frames recovered from 20-byte fragments with 0x55 noise"
    stream = b"\x55\x01\x02" + RX_VERSION + b"\x55\xaa\x00" + RX_1D06 + MODE_SWITCH
    reassembler = rsdk.Reassembler()
    got = []
    for i in range(0, len(stream), 20):
        got += reassembler.feed(stream[i : i + 20])
    assert [f.command for f in got] == [(0, 0), (0x1D, 6), (0x1D, 4)]
    assert reassembler.pending == 0 and reassembler.discarded == 6


def test_reassembler_whole_split_and_coalesced():
    frames = [hx(CAPTURED["OA4 status"]), hx(CAPTURED["1D05 response"]), hx(CAPTURED["OA5Pro status"])]
    assert [f.encode() for f in rsdk.Reassembler().feed(frames[0])] == [frames[0]]
    assert [f.encode() for f in rsdk.Reassembler().feed(b"".join(frames))] == frames
    reassembler = rsdk.Reassembler()
    out = []
    for byte in b"".join(frames):
        out += reassembler.feed(bytes([byte]))
    assert [f.encode() for f in out] == frames


def test_reassembler_truncated_frame_does_not_block_the_next():
    reassembler = rsdk.Reassembler()
    assert reassembler.feed(RX_VERSION[:60]) == []  # a 114-byte frame loses its tail ...
    assert reassembler.pending == 60
    assert [f.encode() for f in reassembler.feed(MODE_SWITCH)] == [MODE_SWITCH]  # ... the next frame still comes out
    assert reassembler.pending == 0 and reassembler.discarded == 60


def test_reassembler_skips_frames_of_the_other_protocol():
    duml_frame = bytes.fromhex("550e04660702040040074601" + "1073")  # livestream_ble.md §5.1 (contains no 0xAA)
    reassembler = rsdk.Reassembler()
    assert reassembler.feed(duml_frame) == [] and reassembler.pending == 0
    assert len(reassembler.feed(duml_frame + MODE_SWITCH + duml_frame)) == 1


def test_reassembler_buffer_is_bounded():
    with pytest.raises(ValueError):
        rsdk.Reassembler(max_buffer=100)
    reassembler = rsdk.Reassembler(max_buffer=1023)
    # a valid header that announces 1023 bytes, followed by an endless stream that never completes it
    head = struct.pack("<BHBB3sH", 0xAA, 1023, 1, 0, bytes(3), 9)
    head += struct.pack("<H", rsdk.crc16(head))
    assert reassembler.feed(head) == []
    for _ in range(200):
        assert reassembler.feed(b"\xaa" + head[1:] + b"\x00" * 50) == []
        assert reassembler.pending <= 1023
    assert [f.encode() for f in reassembler.feed(MODE_SWITCH)] == [MODE_SWITCH]
    reassembler.feed(RX_VERSION[:30])
    reassembler.reset()
    assert reassembler.pending == 0


def _random_frame(rng: random.Random) -> bytes:
    payload = rng.randbytes(rng.choice([0, 1, 5, 9, 31, 38, 46, 96, 300]))
    cmd_type = rng.choice([0x00, 0x01, 0x02, 0x20])
    return Frame(
        rng.randrange(256), rng.randrange(256), payload, cmd_type, rng.randrange(65536), res=rng.randbytes(3)
    ).encode()


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
    rng = random.Random(seed)
    stream = bytearray()
    expected: list[bytes] = []
    for _ in range(rng.randrange(1, 25)):
        kind = rng.random()
        frame = _random_frame(rng)
        if kind < 0.60:
            stream += frame
            expected.append(frame)
        elif kind < 0.75:  # garbage, biased towards start bytes
            stream += bytes(rng.choice([0xAA, 0x55, rng.randrange(256)]) for _ in range(rng.randrange(1, 60)))
        elif kind < 0.90:  # a frame that lost its tail
            stream += frame[: rng.randrange(1, len(frame))]
        else:  # a frame with one flipped bit
            broken = bytearray(frame)
            broken[rng.randrange(len(broken))] ^= 1 << rng.randrange(8)
            stream += broken
    final = _random_frame(rng)  # an intact frame at the very end must not need any further input
    stream += final
    expected.append(final)
    reassembler = rsdk.Reassembler()
    got: list[bytes] = []
    for piece in _packetise(rng, bytes(stream)):
        got += [f.encode() for f in reassembler.feed(piece)]
        assert reassembler.pending <= 4096
    assert got == expected
    assert reassembler.pending == 0


# -- handshake state machine ---------------------------------------------------------------------


@pytest.mark.parametrize("model", ["OA5Pro", "OA4"])
@pytest.mark.parametrize("skip_step2", [False, True])
def test_handshake_with_captured_frames(model, skip_step2):
    # rsdk_ble_fsm_verify.py (report §9 V5): the captured frames, with and without step 2
    handshake = rsdk.ConnectHandshake(0x12345678, MAC, 1234, first_pairing=False)
    request = handshake.start(0x0100)  # the capture echoes SEQ bytes 00 01
    assert request.seq == 0x0100 and handshake.state is rsdk.HandshakeState.REQUEST_SENT and not handshake.done
    if not skip_step2:
        assert handshake.on_frame(Frame.decode(hx(CAPTURED[f"{model} step 2"]))) is None
        assert handshake.state is rsdk.HandshakeState.AWAITING_USER and handshake.ret_code == 0
    step3 = Frame.decode(hx(CAPTURED[f"{model} step 3"]))
    reply = handshake.on_frame(step3)
    assert handshake.state is rsdk.HandshakeState.CONNECTED and handshake.done
    assert handshake.camera_device_id == (0xFF44 if model == "OA5Pro" else 0xFF33)
    assert reply is not None and reply.cmd_type == 0x20 and reply.seq == step3.seq and reply.command == (0, 0x19)
    assert reply.payload == bytes.fromhex("78563412 00 00000000")
    assert Frame.decode(reply.encode()) == reply
    assert handshake.on_frame(step3) is None  # finished: further frames are ignored


def test_handshake_synthetic_transcript_of_the_ref_script():
    # report appendix A: frames 2 and 3 are fabricated there but well-formed; the reply equals EX3
    handshake = rsdk.ConnectHandshake(0x12345678, MAC, 1234, first_pairing=True)
    assert handshake.start(1).encode() == hx(EXAMPLES["EX2"][1])
    step2 = hx("AA 1B 00 20 00 00 00 00 01 00 64 2C 00 19 33 FF 00 00 00 00 00 00 00 70 A2 47 9E")
    assert Frame(0, 0x19, rsdk.ConnectResponse(0xFF33).pack(), CmdType.ACK_NO_RESPONSE, 1).encode() == step2
    assert handshake.on_frame(Frame.decode(step2)) is None
    step3 = hx(
        "AA 33 00 02 00 00 00 00 AF 08 E5 89 00 19 33 FF 00 00 06 60 60 1F 60 11 E7 00 00 00 00 00 00 00 00 00 00 00"
        " 00 00 00 00 02 00 00 00 00 00 00 A2 5D D6 0A"
    )
    camera_request = rsdk.ConnectRequest(0xFF33, bytes.fromhex("60601F6011E7"), 2, 0)
    assert Frame(0, 0x19, camera_request.pack(), CmdType.CMD_WAIT_RESULT, 0x08AF).encode() == step3
    reply = handshake.on_frame(Frame.decode(step3))
    assert reply is not None and reply.encode() == hx(EXAMPLES["EX3"][1])
    assert handshake.camera_device_id == 0xFF33


def test_handshake_rejected_by_the_user():
    # ref script: "camera request with verify_data=1 -> REJECTED, nothing sent"
    handshake = rsdk.ConnectHandshake(0x12345678, MAC, 1234, first_pairing=False)
    handshake.start(2)
    rejection = Frame(0, 0x19, rsdk.ConnectRequest(0xFF44, b"", 2, 1).pack(), CmdType.CMD_WAIT_RESULT, 0x0100)
    assert handshake.on_frame(rejection) is None
    assert handshake.state is rsdk.HandshakeState.REJECTED and handshake.reject_code == 1 and handshake.done
    assert handshake.camera_device_id == 0xFF44


def test_handshake_error_code_in_step2():
    handshake = rsdk.ConnectHandshake(1, MAC, 1, first_pairing=False)
    handshake.start(9)
    refusal = Frame(0, 0x19, rsdk.ConnectResponse(0xFF33, 2).pack(), CmdType.ACK_NO_RESPONSE, 9)
    assert handshake.on_frame(refusal) is None
    assert handshake.state is rsdk.HandshakeState.FAILED and handshake.ret_code == 2 and handshake.done


def test_handshake_ignores_what_is_not_part_of_it():
    handshake = rsdk.ConnectHandshake(1, MAC, 1, first_pairing=False)
    step3 = Frame.decode(hx(CAPTURED["OA4 step 3"]))
    assert handshake.on_frame(step3) is None and handshake.state is rsdk.HandshakeState.IDLE  # not started yet
    handshake.start(0x0005)
    # a response with someone else's SEQ, a status push, a 00 19 command that is not a verification result
    assert handshake.on_frame(Frame.decode(hx(CAPTURED["OA4 step 2"]))) is None  # SEQ 0x0100, not ours
    assert handshake.on_frame(Frame.decode(hx(CAPTURED["OA4 status"]))) is None
    other = Frame(0, 0x19, rsdk.ConnectRequest(0xFF33, b"", 0, 0).pack(), CmdType.CMD_WAIT_RESULT, 3)
    assert handshake.on_frame(other) is None
    assert handshake.on_frame(Frame(0, 0x19, b"\x01\x02", CmdType.CMD_WAIT_RESULT, 3)) is None  # malformed
    assert handshake.on_frame(Frame(0, 0x19, b"\x01", CmdType.ACK_NO_RESPONSE, 5)) is None  # malformed response
    assert handshake.state is rsdk.HandshakeState.REQUEST_SENT
    assert handshake.on_frame(step3) is not None and handshake.state is rsdk.HandshakeState.CONNECTED


def test_handshake_verify_mode_and_camera_number():
    first = rsdk.ConnectRequest.unpack(rsdk.ConnectHandshake(7, MAC, 42, first_pairing=True).start(1).payload)
    again = rsdk.ConnectRequest.unpack(rsdk.ConnectHandshake(7, MAC, 42, first_pairing=False).start(1).payload)
    assert (first.verify_mode, again.verify_mode) == (rsdk.VERIFY_REQUIRED, rsdk.VERIFY_NONE)
    assert first.verify_data == again.verify_data == 42 and first.fw_version == 0  # fw_version must stay 0 (§5.3)
    handshake = rsdk.ConnectHandshake(7, MAC, 42, first_pairing=False, camera_number=3)
    handshake.start(1)
    reply = handshake.on_frame(Frame.decode(hx(CAPTURED["OA4 step 3"])))
    assert reply is not None and rsdk.ConnectResponse.unpack(reply.payload) == rsdk.ConnectResponse(7, 0, 3)
