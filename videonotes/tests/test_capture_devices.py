"""Capture devices (avfoundation listing, picking, modes) and the network helpers."""

from __future__ import annotations

import logging
import socket
import subprocess

import pytest

from videonotes.capture import CaptureError, devices, network
from videonotes.capture.devices import (
    DEFAULT_AUDIO_INDEX,
    CaptureDevice,
    CaptureMode,
    choose_mode,
    fps_arg,
    parse_avfoundation_devices,
    parse_supported_modes,
    pick_device,
)
from videonotes.config import Settings
from videonotes.media import ffmpeg as ff

# -- listings -------------------------------------------------------------------
# Built from the format strings in libavdevice/avfoundation.m:
#   FFmpeg <= 9.0:  "[%d] %s"                       FFmpeg >= 9.1:  "[%d] %s  [uid:%s] [serial:%s]"

OLD_LISTING = """\
[AVFoundation indev @ 0x12f605e60] AVFoundation video devices:
[AVFoundation indev @ 0x12f605e60] [0] FaceTime HD Camera
[AVFoundation indev @ 0x12f605e60] [1] OsmoAction4
[AVFoundation indev @ 0x12f605e60] [2] Capture screen 0
[AVFoundation indev @ 0x12f605e60] [3] Capture screen 1
[AVFoundation indev @ 0x12f605e60] AVFoundation audio devices:
[AVFoundation indev @ 0x12f605e60] [0] MacBook Pro Microphone
[AVFoundation indev @ 0x12f605e60] [1] OsmoAction4
[in#0 @ 0x600001f8c000] Error opening input: Input/output error
Error opening input file .
Error opening input files: Input/output error
"""

NEW_LISTING = """\
[AVFoundation indev @ 0x12f605e60] AVFoundation video devices:
[AVFoundation indev @ 0x12f605e60] [0] FaceTime HD Camera  [uid:3F45E80A-0176-46F7-B185-BB9E2C0E82E3]
[AVFoundation indev @ 0x12f605e60] [1] Osmo Action 5 Pro  [uid:0x1100002ca31020] [serial:6SHXK3F0123ABC]
[AVFoundation indev @ 0x12f605e60] [2] Capture screen 0
[AVFoundation indev @ 0x12f605e60] AVFoundation audio devices:
[AVFoundation indev @ 0x12f605e60] [0] MacBook Pro Microphone  [uid:BuiltInMicrophoneDevice]
[AVFoundation indev @ 0x12f605e60] [1] Osmo Action 5 Pro  [uid:AppleUSBAudioEngine:DJI:Osmo Action:6S:2] [serial:6S]
"""

# A German Mac with awkward device names: brackets, colons, digits first, non-ASCII, CRLF line ends.
AWKWARD_LISTING = (
    "[AVFoundation indev @ 0x7fd1] AVFoundation video devices:\r\n"
    "[AVFoundation indev @ 0x7fd1] [0] FaceTime HD-Kamera (integriert)\r\n"
    "[AVFoundation indev @ 0x7fd1] [1] USB Camera [HD] : front\r\n"
    "[AVFoundation indev @ 0x7fd1] [2] 4K Kamera №2\r\n"
    "[AVFoundation indev @ 0x7fd1] [3] [Virtual] OBS Camera\r\n"
    "[AVFoundation indev @ 0x7fd1] [4] Capture screen 0\r\n"
    "[AVFoundation indev @ 0x7fd1] AVFoundation audio devices:\r\n"
    "[AVFoundation indev @ 0x7fd1] [0] MacBook Pro-Mikrofon\r\n"
    "[AVFoundation indev @ 0x7fd1] [1] 外付けマイク: USB [2ch]\r\n"
)


def _triples(found: list[CaptureDevice]) -> list[tuple[str, int, str]]:
    return [(d.kind, d.index, d.name) for d in found]


def test_parse_old_listing_keeps_indices_and_drops_screens():
    found = parse_avfoundation_devices(OLD_LISTING)
    assert _triples(found) == [
        ("video", 0, "FaceTime HD Camera"),
        ("video", 1, "OsmoAction4"),
        ("audio", 0, "MacBook Pro Microphone"),
        ("audio", 1, "OsmoAction4"),
    ]


def test_parse_new_listing_strips_uid_and_serial():
    found = parse_avfoundation_devices(NEW_LISTING)
    assert _triples(found) == [
        ("video", 0, "FaceTime HD Camera"),
        ("video", 1, "Osmo Action 5 Pro"),
        ("audio", 0, "MacBook Pro Microphone"),
        ("audio", 1, "Osmo Action 5 Pro"),
    ]


def test_parse_awkward_names():
    found = parse_avfoundation_devices(AWKWARD_LISTING)
    assert _triples(found) == [
        ("video", 0, "FaceTime HD-Kamera (integriert)"),
        ("video", 1, "USB Camera [HD] : front"),
        ("video", 2, "4K Kamera №2"),
        ("video", 3, "[Virtual] OBS Camera"),
        ("audio", 0, "MacBook Pro-Mikrofon"),
        ("audio", 1, "外付けマイク: USB [2ch]"),
    ]


def test_parse_without_log_prefix_and_with_level_prefix():
    text = (
        "AVFoundation video devices:\n[0] FaceTime HD Camera\n"
        "[AVFoundation indev @ 0x1] [info] AVFoundation audio devices:\n"
        "[AVFoundation indev @ 0x1] [info] [0] Built-in Microphone\n"
    )
    assert _triples(parse_avfoundation_devices(text)) == [
        ("video", 0, "FaceTime HD Camera"),
        ("audio", 0, "Built-in Microphone"),
    ]


@pytest.mark.parametrize(
    "text",
    [
        "",
        "ffmpeg: command not found\n",
        "[0] not inside a section\n",
        "Unknown input format: 'avfoundation'\n",
        "[avf @ 0x1] AVFoundation video devices:\n[avf @ 0x1] AVFoundation audio devices:\n",
    ],
)
def test_parse_nothing_useful(text):
    assert parse_avfoundation_devices(text) == []


def test_parse_ignores_duplicates_and_empty_names():
    text = "AVFoundation video devices:\n[0] Cam\n[0] Cam again\n[1] \n[2]   Spaced  \n"
    assert _triples(parse_avfoundation_devices(text)) == [("video", 0, "Cam"), ("video", 2, "Spaced")]


def test_parse_audio_capture_screen_is_a_real_name():
    # Only *video* entries named "Capture screen N" are pseudo devices.
    text = "AVFoundation video devices:\n[0] Capture screen 0\nAVFoundation audio devices:\n[0] Capture screen 0\n"
    assert _triples(parse_avfoundation_devices(text)) == [("audio", 0, "Capture screen 0")]


# -- list_devices -----------------------------------------------------------------


def test_list_devices_is_empty_off_macos(monkeypatch):
    monkeypatch.setattr(devices, "is_macos", lambda: False)
    monkeypatch.setattr(ff, "run", lambda *a, **k: pytest.fail("ffmpeg must not be run"))
    assert devices.list_devices() == []


def test_list_devices_runs_the_listing_at_info_level(monkeypatch):
    calls = []

    def fake_run(args, **kwargs):
        calls.append((args, kwargs))
        return subprocess.CompletedProcess(args, 251, stdout="", stderr=OLD_LISTING)  # it always "fails"

    monkeypatch.setattr(devices, "is_macos", lambda: True)
    monkeypatch.setattr(ff, "has_input_format", lambda name: name == "avfoundation")
    monkeypatch.setattr(ff, "run", fake_run)
    found = devices.list_devices()
    assert [d.name for d in found if d.kind == "video"] == ["FaceTime HD Camera", "OsmoAction4"]
    args, kwargs = calls[0]
    assert args == ["-f", "avfoundation", "-list_devices", "true", "-i", ""]
    assert kwargs["check"] is False and kwargs["loglevel"] == "info" and kwargs["timeout"] > 0


def test_list_devices_without_avfoundation(monkeypatch, caplog):
    monkeypatch.setattr(devices, "is_macos", lambda: True)
    monkeypatch.setattr(ff, "has_input_format", lambda name: False)
    monkeypatch.setattr(ff, "run", lambda *a, **k: pytest.fail("ffmpeg must not be run"))
    with caplog.at_level(logging.WARNING, logger="videonotes.capture.devices"):
        assert devices.list_devices() == []
    assert "brew install ffmpeg" in caplog.text


def test_list_devices_survives_a_hanging_ffmpeg(monkeypatch, caplog):
    def hang(args, **kwargs):
        raise ff.FFmpegError("ffmpeg timed out after 20s")

    monkeypatch.setattr(devices, "is_macos", lambda: True)
    monkeypatch.setattr(ff, "has_input_format", lambda name: True)
    monkeypatch.setattr(ff, "run", hang)
    with caplog.at_level(logging.WARNING, logger="videonotes.capture.devices"):
        assert devices.list_devices() == []
    assert "timed out" in caplog.text


def test_list_devices_reports_missing_ffmpeg(monkeypatch):
    def missing():
        raise ff.FFmpegError(ff.INSTALL_HINT)

    monkeypatch.setattr(devices, "is_macos", lambda: True)
    monkeypatch.setattr(ff, "ffmpeg_bin", missing)
    with pytest.raises(ff.FFmpegError, match="brew install ffmpeg"):
        devices.list_devices()


# -- pick_device --------------------------------------------------------------------


@pytest.fixture()
def action4() -> list[CaptureDevice]:
    return parse_avfoundation_devices(OLD_LISTING)


def test_pick_auto_finds_the_dji_camera_and_its_microphone(action4, caplog):
    with caplog.at_level(logging.INFO, logger="videonotes.capture.devices"):
        video = pick_device(action4, "video", "auto")
        audio = pick_device(action4, "audio", "auto")
    assert (video.kind, video.index, video.name) == ("video", 1, "OsmoAction4")
    assert (audio.kind, audio.index, audio.name) == ("audio", 1, "OsmoAction4")
    assert not audio.is_default
    assert "camera's own USB microphone" in caplog.text


def test_pick_auto_matches_hints_case_insensitively():
    found = [CaptureDevice(0, "FaceTime HD Camera", "video"), CaptureDevice(3, "DJI OSMO ACTION 5 PRO", "video")]
    assert pick_device(found, "video", "AUTO").index == 3
    assert pick_device(found, "video", "").index == 3


def test_pick_auto_video_falls_back_to_generic_uvc_name_only(caplog):
    generic = [CaptureDevice(0, "FaceTime HD Camera", "video"), CaptureDevice(1, "UVC Camera", "video")]
    assert pick_device(generic, "video", "auto").name == "UVC Camera"
    builtin_only = [CaptureDevice(0, "FaceTime HD Camera", "video"), CaptureDevice(1, "USB Webcam", "video")]
    assert pick_device(builtin_only, "video", "auto") is None


def test_pick_auto_audio_falls_back_to_the_macs_default_input(caplog):
    # An Osmo Action 5 Pro on old firmware: a camera, but no USB microphone.
    found = [
        CaptureDevice(0, "FaceTime HD Camera", "video"),
        CaptureDevice(1, "OsmoAction5pro", "video"),
        CaptureDevice(0, "MacBook Pro Microphone", "audio"),
    ]
    with caplog.at_level(logging.WARNING, logger="videonotes.capture.devices"):
        audio = pick_device(found, "audio", "auto")
    assert audio is not None and audio.is_default and audio.index == DEFAULT_AUDIO_INDEX and audio.kind == "audio"
    assert "default input" in audio.name
    assert "01.01.05.20" in caplog.text and "default input" in caplog.text


def test_pick_audio_without_any_microphone(caplog):
    only_video = [CaptureDevice(1, "OsmoAction4", "video")]
    with caplog.at_level(logging.WARNING, logger="videonotes.capture.devices"):
        assert pick_device(only_video, "audio", "auto") is None
        assert pick_device(only_video, "audio", "default") is None
    assert "video only" in caplog.text


def test_pick_audio_default_and_none(action4):
    forced = pick_device(action4, "audio", "default")
    assert forced.is_default  # even though the camera has a microphone
    assert pick_device(action4, "audio", "Default").is_default
    assert pick_device(action4, "audio", "none") is None
    assert pick_device(action4, "audio", " NONE ") is None


def test_pick_by_index(action4):
    assert pick_device(action4, "video", "0").name == "FaceTime HD Camera"
    assert pick_device(action4, "audio", "1").name == "OsmoAction4"
    assert pick_device(action4, "video", "2") is None  # index 2 is a screen, not a camera
    assert pick_device(action4, "video", "7") is None


def test_pick_by_name_substring_prefers_exact_match():
    found = [
        CaptureDevice(0, "USB Microphone Pro", "audio"),
        CaptureDevice(1, "USB Microphone", "audio"),
        CaptureDevice(2, "MacBook Pro Microphone", "audio"),
    ]
    assert pick_device(found, "audio", "usb microphone").index == 1  # exact (case-insensitive) wins
    assert pick_device(found, "audio", "macbook").index == 2
    assert pick_device(found, "audio", "microphone").index == 0  # first substring match
    assert pick_device(found, "audio", "gopro") is None
    assert pick_device(found, "video", "usb") is None  # wrong kind


def test_pick_video_does_not_treat_default_or_none_specially(action4):
    assert pick_device(action4, "video", "default") is None
    assert pick_device(action4, "video", "none") is None


def test_pick_rejects_unknown_kind(action4):
    with pytest.raises(ValueError):
        pick_device(action4, "screen", "auto")


def test_pick_from_nothing():
    assert pick_device([], "video", "auto") is None
    assert pick_device([], "audio", "auto") is None
    assert pick_device([], "audio", "0") is None


# -- capture modes -----------------------------------------------------------------

MODES_TEXT = """\
[avfoundation @ 0x7f8] Selected video size (1280x720) is not supported by the device.
[avfoundation @ 0x7f8] Supported modes:
[avfoundation @ 0x7f8]   1920x1080@[30.000030 30.000030]fps
[avfoundation @ 0x7f8]   1920x1080@[30.000030 30.000030]fps
[avfoundation @ 0x7f8]   1280x960@[29.970030 29.970030]fps
[avfoundation @ 0x7f8]   640x480@[15.000000 60.000240]fps
[in#0 @ 0x6000] Error opening input: Invalid argument
"""


def test_parse_supported_modes():
    assert parse_supported_modes(MODES_TEXT) == [
        CaptureMode(1920, 1080, 30.00003, 30.00003),
        CaptureMode(1280, 960, 29.97003, 29.97003),
        CaptureMode(640, 480, 15.0, 60.00024),
    ]
    assert parse_supported_modes("nothing here") == []


def test_choose_mode_prefers_frame_rate_then_size():
    modes = parse_supported_modes(MODES_TEXT)
    # 720p is not offered: take the 16:9 mode at the requested rate and scale down later.
    assert choose_mode(modes, 1280, 720, 30) == CaptureMode(1920, 1080, 30.00003, 30.00003)
    assert choose_mode(modes, 640, 480, 60) == CaptureMode(640, 480, 15.0, 60.00024)
    assert choose_mode(modes, 1280, 960, 29.97) == CaptureMode(1280, 960, 29.97003, 29.97003)
    assert choose_mode([], 1280, 720, 30) is None


def test_choose_mode_exact_size_wins_at_the_same_rate():
    modes = [CaptureMode(1920, 1080, 30, 30), CaptureMode(1280, 720, 30, 30), CaptureMode(640, 360, 30, 30)]
    assert choose_mode(modes, 1280, 720, 30) == CaptureMode(1280, 720, 30, 30)
    # A faster mode is better than a slower one when the exact rate is missing.
    modes = [CaptureMode(1280, 720, 15, 15), CaptureMode(1280, 720, 60, 60)]
    assert choose_mode(modes, 1280, 720, 30) == CaptureMode(1280, 720, 60, 60)
    # Never prefer a smaller picture when a larger one with the same shape exists.
    modes = [CaptureMode(640, 360, 30, 30), CaptureMode(1920, 1080, 30, 30), CaptureMode(1600, 1200, 30, 30)]
    assert choose_mode(modes, 1280, 720, 30) == CaptureMode(1920, 1080, 30, 30)


@pytest.mark.parametrize(
    ("fps", "text"),
    [(30.00003, "30"), (29.97003, "30000/1001"), (60.00024, "60"), (59.94006, "60000/1001"), (25.0, "25"),
     (23.976, "24000/1001"), (12.5, "12.5"), (7.512, "7.512")],
)  # fmt: skip
def test_fps_arg_lands_within_avfoundation_tolerance(fps, text):
    assert fps_arg(fps) == text
    num, _, den = text.partition("/")
    assert abs(float(num) / float(den or 1) - fps) < 0.01


# -- network ------------------------------------------------------------------------

HARDWARE_PORTS = """
Hardware Port: Ethernet Adapter (en4)
Device: en4
Ethernet Address: 3a:c1:5c:2b:aa:01

Hardware Port: Wi-Fi
Device: en1
Ethernet Address: f0:18:98:aa:bb:cc

Hardware Port: Thunderbolt Bridge
Device: bridge0
Ethernet Address: 36:8f:d0:11:22:33

VLAN Configurations
===================
"""


def test_parse_hardware_ports_finds_wifi_device():
    assert network.parse_hardware_ports(HARDWARE_PORTS) == [
        ("Ethernet Adapter (en4)", "en4"), ("Wi-Fi", "en1"), ("Thunderbolt Bridge", "bridge0"),
    ]  # fmt: skip
    assert network.wifi_device_from_ports(HARDWARE_PORTS) == "en1"
    assert network.wifi_device_from_ports("Hardware Port: AirPort\nDevice: en0\n") == "en0"
    assert network.wifi_device_from_ports("Hardware Port: Ethernet\nDevice: en0\n") is None
    assert network.wifi_device_from_ports("") is None


def test_parse_ipconfig_summary():
    summary = (
        "<dictionary> {\n  BSSID : aa:bb:cc:dd:ee:ff\n  InterfaceType : WiFi\n"
        "  SSID : Home Network 5G\n  Security : WPA2\n}\n"
    )
    assert network.parse_ipconfig_summary(summary) == "Home Network 5G"
    assert network.parse_ipconfig_summary(summary.replace("Home Network 5G", "<redacted>")) is None
    assert network.parse_ipconfig_summary("  BSSID : aa:bb:cc:dd:ee:ff\n") is None  # BSSID is not the SSID
    assert network.parse_ipconfig_summary("  SSID : \n") is None
    assert network.parse_ipconfig_summary("") is None


def test_parse_airport_network():
    assert network.parse_airport_network("Current Wi-Fi Network: Café Net\n") == "Café Net"
    assert network.parse_airport_network("Current AirPort Network: old-mac\n") == "old-mac"
    assert network.parse_airport_network("You are not associated with an AirPort network.\n") is None
    assert network.parse_airport_network("Current Wi-Fi Network: <redacted>\n") is None


def test_current_wifi_ssid_is_none_off_macos(monkeypatch):
    monkeypatch.setattr(network, "is_macos", lambda: False)
    monkeypatch.setattr(network, "_run", lambda cmd: pytest.fail("no system tools off macOS"))
    assert network.current_wifi_ssid() is None


def _fake_tools(answers: dict[str, str]):
    def run(cmd: list[str]) -> str:
        return answers.get(" ".join(cmd), "")

    return run


def test_current_wifi_ssid_tries_methods_in_order(monkeypatch):
    monkeypatch.setattr(network, "is_macos", lambda: True)
    monkeypatch.setattr(network, "_corewlan_ssid", lambda: None)
    answers = {
        "networksetup -listallhardwareports": HARDWARE_PORTS,
        "ipconfig getsummary en1": "  SSID : <redacted>\n",
        "networksetup -getairportnetwork en1": "Current Wi-Fi Network: Workshop\n",
    }
    monkeypatch.setattr(network, "_run", _fake_tools(answers))
    assert network.current_wifi_ssid() == "Workshop"  # redacted summary skipped, never returned
    answers["ipconfig getsummary en1"] = "  SSID : Attic\n"
    assert network.current_wifi_ssid() == "Attic"
    monkeypatch.setattr(network, "_corewlan_ssid", lambda: "From CoreWLAN")
    assert network.current_wifi_ssid() == "From CoreWLAN"


def test_current_wifi_ssid_none_when_macos_hides_it(monkeypatch):
    monkeypatch.setattr(network, "is_macos", lambda: True)
    monkeypatch.setattr(network, "_corewlan_ssid", lambda: None)
    answers = {
        "networksetup -listallhardwareports": HARDWARE_PORTS,
        "ipconfig getsummary en1": "  SSID : <redacted>\n",
        "networksetup -getairportnetwork en1": "You are not associated with an AirPort network.\n",
    }
    monkeypatch.setattr(network, "_run", _fake_tools(answers))
    assert network.current_wifi_ssid() is None
    monkeypatch.setattr(network, "_run", _fake_tools({}))  # no Wi-Fi hardware at all
    assert network.current_wifi_ssid() is None


def test_corewlan_missing_is_not_an_error():
    assert network._corewlan_ssid() is None  # the bridge is not installed here


def test_lan_ip_here_is_a_plain_ipv4_or_none():
    ip = network.lan_ip()
    assert ip is None or (network._usable(ip) and not ip.startswith("127."))


def test_lan_ip_prefers_wifi_interface_on_a_mac(monkeypatch):
    monkeypatch.setattr(network, "is_macos", lambda: True)
    monkeypatch.setattr(network, "_default_route_ip", lambda: "10.8.0.2")  # a VPN owns the default route
    monkeypatch.setattr(network, "_hostname_ips", lambda: [])
    answers = {"networksetup -listallhardwareports": HARDWARE_PORTS, "ipconfig getifaddr en1": "192.168.1.23\n"}
    monkeypatch.setattr(network, "_run", _fake_tools(answers))
    assert network.lan_ip() == "192.168.1.23"
    answers["ipconfig getifaddr en1"] = ""  # Wi-Fi off: the wired address is the best there is
    assert network.lan_ip() == "10.8.0.2"


def test_lan_ip_fallbacks(monkeypatch):
    monkeypatch.setattr(network, "is_macos", lambda: False)
    monkeypatch.setattr(network, "_default_route_ip", lambda: None)
    monkeypatch.setattr(network, "_hostname_ips", lambda: ["192.168.7.7"])
    assert network.lan_ip() == "192.168.7.7"
    monkeypatch.setattr(network, "_hostname_ips", lambda: [])
    assert network.lan_ip() is None
    # A self-assigned address is only used when nothing better exists.
    monkeypatch.setattr(network, "_default_route_ip", lambda: "169.254.10.20")
    assert network.lan_ip() == "169.254.10.20"
    monkeypatch.setattr(network, "_hostname_ips", lambda: ["192.168.7.7"])
    assert network.lan_ip() == "192.168.7.7"


@pytest.mark.parametrize(
    ("ip", "ok"),
    [("192.168.1.2", True), ("10.0.0.1", True), ("127.0.0.1", False), ("0.0.0.0", False), ("", False),
     (None, False), ("1.2.3", False), ("fe80::1", False), ("224.0.0.1", False), ("not an ip", False)],
)  # fmt: skip
def test_usable_address(ip, ok):
    assert network._usable(ip) is ok


def test_rtmp_url(monkeypatch):
    settings = Settings()
    monkeypatch.setattr(network, "lan_ip", lambda: "192.168.1.23")
    assert network.rtmp_url(settings) == "rtmp://192.168.1.23:1935/live/cam"
    settings.capture.rtmp_port = 1936
    settings.capture.rtmp_path = "/notes/today/"
    assert network.rtmp_url(settings) == "rtmp://192.168.1.23:1936/notes/today"
    settings.capture.rtmp_path = " / "
    assert network.rtmp_url(settings) == "rtmp://192.168.1.23:1936/live/cam"


def test_rtmp_url_without_network(monkeypatch):
    monkeypatch.setattr(network, "lan_ip", lambda: None)
    with pytest.raises(CaptureError, match="Wi-Fi"):
        network.rtmp_url(Settings())


def test_port_in_use():
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind(("0.0.0.0", 0))
        listener.listen(1)
        port = listener.getsockname()[1]
        assert network.port_in_use(port) is True
    finally:
        listener.close()
    assert network.port_in_use(port) is False  # free again as soon as the listener is gone
    assert network.port_in_use(-5) is False
    assert network.port_in_use(70000) is False
