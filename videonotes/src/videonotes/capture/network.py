"""Where the camera should send its livestream: this Mac's LAN address, Wi-Fi name, RTMP URL.

Nothing here talks to another machine.  The only socket operations are a UDP
``connect()`` (which sends no packet; it just asks the kernel which local address it
would use) and a local ``bind()`` to see whether a port is free.

macOS specifics, from Apple's TN3179 and the capture research:

* Listening for the camera's incoming connection needs **no** "Local Network" permission.
* There is no dependable way for a command-line tool to read the Wi-Fi network name on
  macOS 14.4+: ``airport`` is gone, ``networksetup -getairportnetwork`` and
  ``ipconfig getsummary`` are progressively redacted, and CoreWLAN returns nothing
  without Location Services.  :func:`current_wifi_ssid` therefore tries the methods that
  still work somewhere and returns ``None`` (never ``"<redacted>"``) so the caller asks.
"""

from __future__ import annotations

import errno
import logging
import re
import socket
import subprocess

from ..config import Settings, is_macos
from . import CaptureError

log = logging.getLogger("videonotes.capture.network")

_CMD_TIMEOUT_S = 5.0
# TEST-NET-1 (RFC 5737): reserved for documentation, never routed, and not on the local network.
_PROBE_TARGET = ("192.0.2.1", 9)


def _usable(ip: str | None) -> bool:
    """A concrete IPv4 address another device could connect to."""
    if not ip:
        return False
    try:
        packed = socket.inet_aton(ip)
    except OSError:
        return False
    if len(packed) != 4 or ip.count(".") != 3:
        return False
    first = packed[0]
    return first not in (0, 127) and not (224 <= first <= 255)


def _is_link_local(ip: str) -> bool:
    return ip.startswith("169.254.")


def _run(cmd: list[str]) -> str:
    """stdout of a small system tool, or "" when it is missing, fails or hangs."""
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, errors="replace", timeout=_CMD_TIMEOUT_S)
    except (OSError, subprocess.SubprocessError):
        return ""
    return proc.stdout if proc.returncode == 0 else ""


# -- parsers (pure) ----------------------------------------------------------------

_PORT_BLOCK = re.compile(r"Hardware Port:\s*(?P<port>.+?)\s*\n\s*Device:\s*(?P<dev>\S+)", re.IGNORECASE)


def parse_hardware_ports(text: str) -> list[tuple[str, str]]:
    """``(port name, BSD device)`` pairs from ``networksetup -listallhardwareports``."""
    return [(m["port"].strip(), m["dev"].strip()) for m in _PORT_BLOCK.finditer(text)]


def wifi_device_from_ports(text: str) -> str | None:
    """The BSD name of the Wi-Fi interface (never assume ``en0``)."""
    for port, dev in parse_hardware_ports(text):
        if port.casefold() in ("wi-fi", "wifi", "airport", "wlan"):
            return dev
    return None


def _clean_ssid(value: str | None) -> str | None:
    """None for anything that is not a real network name (empty, redacted, null)."""
    if value is None:
        return None
    text = str(value).strip()
    if not text or "redacted" in text.casefold() or text.casefold() in ("(null)", "null", "none", "<unknown>"):
        return None
    return text


_SUMMARY_SSID = re.compile(r"^\s*SSID\s*:\s*(.*)$", re.MULTILINE)
_AIRPORT_NETWORK = re.compile(r"^Current (?:Wi-Fi|AirPort) Network:\s*(.*)$", re.MULTILINE)


def parse_ipconfig_summary(text: str) -> str | None:
    """The ``SSID : name`` line of ``ipconfig getsummary <iface>`` (None when redacted)."""
    match = _SUMMARY_SSID.search(text)  # "BSSID :" does not match: the pattern is anchored on SSID
    return _clean_ssid(match.group(1)) if match else None


def parse_airport_network(text: str) -> str | None:
    """The name from ``networksetup -getairportnetwork <iface>`` (None when not reported)."""
    match = _AIRPORT_NETWORK.search(text)
    return _clean_ssid(match.group(1)) if match else None


# -- addresses -----------------------------------------------------------------------


def _wifi_device() -> str | None:
    return wifi_device_from_ports(_run(["networksetup", "-listallhardwareports"])) if is_macos() else None


def _default_route_ip() -> str | None:
    """Local address of the interface with the default route (UDP connect; sends nothing)."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.settimeout(1.0)
        sock.connect(_PROBE_TARGET)
        ip = sock.getsockname()[0]
    except OSError:
        return None
    finally:
        sock.close()
    return ip if _usable(ip) else None


def _hostname_ips() -> list[str]:
    """Addresses the Mac's own host name resolves to (no network traffic)."""
    try:
        _name, _aliases, addresses = socket.gethostbyname_ex(socket.gethostname())
    except OSError:
        return []
    return [ip for ip in addresses if _usable(ip)]


def lan_ip() -> str | None:
    """The IPv4 address other devices on the Wi-Fi can reach this Mac at, or None.

    Order: the Wi-Fi interface's own address on a Mac (with a VPN or a second network the
    default route is not what the camera can reach), then the address of the default
    route (UDP ``connect`` trick), then whatever the host name resolves to.  Self-assigned
    169.254.x.x addresses are only returned when there is nothing better.
    """
    candidates: list[str] = []
    device = _wifi_device()
    if device:
        ip = _run(["ipconfig", "getifaddr", device]).strip()
        if _usable(ip):
            candidates.append(ip)
    route_ip = _default_route_ip()
    if route_ip:
        candidates.append(route_ip)
    candidates += _hostname_ips()
    for ip in candidates:
        if not _is_link_local(ip):
            return ip
    return candidates[0] if candidates else None


def _corewlan_ssid() -> str | None:
    """SSID via CoreWLAN (optional pyobjc bridge; needs Location Services for the terminal app)."""
    try:
        import CoreWLAN  # type: ignore[import-not-found]

        interface = CoreWLAN.CWWiFiClient.sharedWiFiClient().interface()
        return _clean_ssid(interface.ssid()) if interface is not None else None
    except Exception:  # missing bridge, no Wi-Fi hardware, or the framework refusing: not an error
        return None


def current_wifi_ssid() -> str | None:
    """Name of the Wi-Fi network this Mac is on, or None when macOS will not say.

    Tries CoreWLAN, then ``ipconfig getsummary``, then ``networksetup -getairportnetwork``.
    Recent macOS versions hide the name from command-line tools, so ``None`` is a normal
    answer: ask the user (``vnote wireless --ssid NAME``).
    """
    if not is_macos():
        return None
    ssid = _corewlan_ssid()
    if ssid:
        return ssid
    device = _wifi_device()
    if not device:
        return None
    ssid = parse_ipconfig_summary(_run(["ipconfig", "getsummary", device]))
    if ssid:
        return ssid
    return parse_airport_network(_run(["networksetup", "-getairportnetwork", device]))


# -- RTMP ---------------------------------------------------------------------------


def rtmp_path(settings: Settings) -> str:
    """The configured stream path without leading/trailing slashes (default ``live/cam``)."""
    return settings.capture.rtmp_path.strip().strip("/") or "live/cam"


def rtmp_url(settings: Settings) -> str:
    """The URL the camera must push to, e.g. ``rtmp://192.168.1.20:1935/live/cam``."""
    ip = lan_ip()
    if ip is None:
        raise CaptureError(
            "This Mac has no network address the camera could reach. "
            "Join the Wi-Fi network the camera should use, then try again."
        )
    return f"rtmp://{ip}:{int(settings.capture.rtmp_port)}/{rtmp_path(settings)}"


def port_in_use(port: int) -> bool:
    """True if something is already listening on TCP ``port`` on this machine.

    Uses the same socket options as ffmpeg's listener (``SO_REUSEADDR`` then ``bind``),
    so the answer matches whether ffmpeg will be able to listen: a port that is merely
    cooling down after a previous run counts as free.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("0.0.0.0", int(port)))
    except OSError as exc:
        if exc.errno == errno.EADDRINUSE:
            return True
        log.debug("port %s cannot be checked (%s); leaving the decision to ffmpeg", port, exc)
        return False
    except (OverflowError, ValueError):
        return False
    finally:
        sock.close()
    return False
