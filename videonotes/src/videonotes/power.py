"""Battery state on a Mac laptop, so heavy work can wait for the charger.

Where the power goes while videonotes runs, roughly (estimates, not measurements; `vnote live`
measures the real drain on your Mac and prints it at the end of a session):

* capturing and hardware-encoding video (VideoToolbox) and picking keyframes: light;
* speech-to-text (Parakeet on the GPU) and reading text (Apple Vision on the Neural Engine):
  short bursts, tens of times faster than real time, so light on average;
* describing frames with a vision model and writing summaries with a language model: seconds
  of full GPU load per frame or per call.  This is what empties a battery.

So the default policy (``power.on_battery = "light"``) keeps capture, speech and text reading
going on battery and leaves frame descriptions and the written summary until the Mac is on
its charger (``vnote process`` then finishes them).
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from dataclasses import dataclass

#: Values of ``power.on_battery``.
POLICIES = ("light", "full")

DEFER_REASON = (
    "left for later because this Mac is running on battery "
    "(plug it in and run `vnote process`, or set power.on_battery = \"full\")"
)


@dataclass(frozen=True)
class PowerState:
    on_battery: bool
    percent: int | None = None  # None when the machine has no battery (desktop Mac)
    minutes_left: int | None = None  # macOS's own estimate; None while it is still estimating

    def describe(self) -> str:
        if self.percent is None:
            return "on mains power" if not self.on_battery else "on battery"
        where = "on battery" if self.on_battery else "plugged in"
        text = f"{where}, {self.percent}%"
        if self.on_battery and self.minutes_left is not None:
            hours, minutes = divmod(self.minutes_left, 60)
            text += f" (about {hours}:{minutes:02d} left)"
        return text


_SOURCE = re.compile(r"Now drawing from '([^']+)'")
_BATTERY = re.compile(r"InternalBattery[^%\n]*?(\d{1,3})%;\s*([^;\n]+);\s*(?:(\d+):(\d{2}) remaining|\(no estimate\))?")


def parse_pmset(text: str) -> PowerState | None:
    """Parse the output of ``pmset -g batt``. Returns None if it is not recognisable."""
    source = _SOURCE.search(text or "")
    if not source:
        return None
    on_battery = source.group(1).strip().lower() == "battery power"
    battery = _BATTERY.search(text)
    if not battery:
        return PowerState(on_battery=on_battery)
    percent = max(0, min(100, int(battery.group(1))))
    minutes = None
    if battery.group(3) is not None and on_battery:
        minutes = int(battery.group(3)) * 60 + int(battery.group(4))
        if minutes == 0:
            minutes = None  # pmset says 0:00 while it has no estimate yet
    return PowerState(on_battery=on_battery, percent=percent, minutes_left=minutes)


def power_state() -> PowerState | None:
    """The Mac's current power source and charge, or None when unknown (or not a Mac)."""
    if sys.platform != "darwin":
        return None
    tool = shutil.which("pmset") or "/usr/bin/pmset"
    try:
        out = subprocess.run([tool, "-g", "batt"], capture_output=True, text=True, timeout=5).stdout
    except (OSError, subprocess.SubprocessError):
        return None
    return parse_pmset(out)


def should_defer_heavy_work(policy: str, state: PowerState | None) -> bool:
    """True when frame descriptions and LLM summaries should wait for the charger."""
    return policy != "full" and state is not None and state.on_battery


def drain_report(start: PowerState | None, end: PowerState | None, seconds: float) -> str | None:
    """One line on the battery used during a run, or None when it cannot be measured honestly."""
    if start is None or end is None or start.percent is None or end.percent is None:
        return None
    if not (start.on_battery and end.on_battery):
        return "The Mac was plugged in for part of the session, so the battery use was not measured."
    used = start.percent - end.percent
    minutes = seconds / 60.0
    if minutes < 10 or used < 1:
        return f"Battery: {start.percent}% → {end.percent}% over {minutes:.0f} min (too short to estimate a rate)."
    per_hour = used / (minutes / 60.0)
    return (
        f"Battery: {start.percent}% → {end.percent}% over {minutes:.0f} min, about {per_hour:.0f}% per hour "
        f"(roughly {100 / per_hour:.1f} h from a full charge at this rate)."
    )
