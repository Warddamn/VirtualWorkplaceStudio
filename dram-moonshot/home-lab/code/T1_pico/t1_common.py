# t1_common.py -- shared helpers for the T1 bench-electronics experiments (E1, E2, E3).
# REFERENCE CODE - UNTESTED ON HARDWARE. MicroPython for Raspberry Pi Pico (RP2040) / Pico 2 (RP2350).
# Copy this file to the Pico together with the experiment script you run.
#
# Contents: ADC averaging in volts, GPIO tri-state helpers, CSV logging (USB serial + optional file
# on the Pico's flash), DS18B20 temperature, an optional low-voltage heater thermostat with a hard
# 55 C cut-off, a preheat-and-hold routine, an optional hardware watchdog, and timing helpers.

import time
from machine import Pin, ADC

ADC_FULL_SCALE_V = 3.3     # Pico ADC reference = the filtered 3V3 rail. Measure yours and edit.


_wdt = None                # hardware watchdog, started only when a heater is in use


def start_watchdog(timeout_ms=8000):
    """Start the hardware watchdog. Once started it cannot be stopped: if the script hangs for longer than
    timeout_ms, the Pico resets, its pins float, and the heater MOSFET's 100 kOhm gate pull-down turns the
    heater off. Side effect: the board also resets itself ~8 s after the script ends. That is expected."""
    global _wdt
    try:
        from machine import WDT
        _wdt = WDT(timeout=timeout_ms)
    except Exception:
        _wdt = None


def feed():
    if _wdt:
        _wdt.feed()


def low_ripple_supply():
    """Pico / Pico 2 (non-W): GPIO23 high puts the on-board regulator in PWM mode, which lowers ADC noise.
    On Pico W / Pico 2 W, GPIO23 powers the radio chip, so this function leaves it alone there."""
    try:
        import os
        machine_name = os.uname().machine     # e.g. "Raspberry Pi Pico W with RP2040"
    except Exception:
        machine_name = ""
    if " W" in machine_name:
        return
    try:
        Pin(23, Pin.OUT, value=1)
    except Exception:
        pass


def adc_volts(adc, n=64):
    """Average n readings. read_u16() returns 0..65535 scaled from the 12-bit converter."""
    total = 0
    for _ in range(n):
        total += adc.read_u16()
    return total / n * ADC_FULL_SCALE_V / 65535


def tristate(pin):
    """High impedance: input, no pull-up, no pull-down. (Pico 2 A2 stepping: see erratum E9 in the guide.)"""
    pin.init(Pin.IN, None)


def drive(pin, value):
    pin.init(Pin.OUT, value=value)


def fmt(x, digits=5):
    if isinstance(x, float):
        return ("{:." + str(digits) + "g}").format(x)
    return str(x).replace(",", ";")      # a comma inside a field would shift every CSV column


class Clock:
    """Elapsed seconds since start, wrap-safe for ~6 days (ticks_ms wraps every ~12 days on rp2)."""

    def __init__(self):
        self.t0 = time.ticks_ms()

    def s(self):
        return time.ticks_diff(time.ticks_ms(), self.t0) / 1000.0


class CsvLog:
    """Prints CSV to USB serial (capture with: mpremote run script.py > log.csv) and optionally appends
    to a file on the Pico's flash for unattended runs. Comment lines start with '#'."""

    def __init__(self, header, filename=None):
        self.f = None
        if filename:
            try:
                self.f = open(filename, "a")
            except OSError:
                self.f = None
        self.row(header)

    def _write(self, s):
        if self.f:
            try:
                self.f.write(s + "\n")
                self.f.flush()
            except OSError:
                self.f = None
                print("# LOGFILE write failed (flash full?); continuing on USB only")

    def row(self, fields):
        feed()
        s = ",".join(fmt(x) for x in fields)
        print(s)
        self._write(s)

    def note(self, text):
        feed()
        print("# " + text)
        self._write("# " + text)

    def close(self):
        if self.f:
            self.f.close()
            self.f = None


class Thermo:
    """DS18B20 on one GPIO with a 4.7 kOhm pull-up to 3V3. Returns NaN if no sensor is found."""

    def __init__(self, pin_no=22):
        self.ds = None
        self.roms = []
        try:
            import onewire
            import ds18x20
            self.ds = ds18x20.DS18X20(onewire.OneWire(Pin(pin_no)))
            self.roms = self.ds.scan()
        except Exception:
            self.ds = None
            self.roms = []

    def read_c(self):
        if not self.roms:
            return float("nan")
        try:
            self.ds.convert_temp()
            time.sleep_ms(750)          # 12-bit conversion time
            return self.ds.read_temp(self.roms[0])
        except Exception:
            return float("nan")


class Heater:
    """Optional bang-bang thermostat for a <=12 V resistor heater switched by a logic-level MOSFET.
    Hardware: E1 guide section 6.5 (two 10 Ohm resistors in SERIES, 72 C thermal fuse, gate via 220 Ohm,
    100 kOhm gate pull-down so the heater is off whenever the Pico is unplugged or resetting).
    Fails safe: heater OFF if the sensor is missing, reads NaN, or exceeds HARD_MAX_C.
    The thermal fuse in series with the heater is the hardware backstop. Never power the heater
    unless a script is running this thermostat."""

    HARD_MAX_C = 55.0

    def __init__(self, pin_no, thermo, setpoint_c, band_c=0.5):
        self.pin = Pin(pin_no, Pin.OUT, value=0)
        self.thermo = thermo
        self.setpoint = min(setpoint_c, self.HARD_MAX_C - 3.0)
        self.band = band_c

    def step(self):
        """One thermostat step. Takes ~0.75 s (sensor conversion). Also feeds the watchdog."""
        feed()
        t = self.thermo.read_c()
        if t != t or t >= self.HARD_MAX_C:      # NaN check: NaN != NaN
            self.pin.value(0)
            return t
        if t < self.setpoint - self.band:
            self.pin.value(1)
        elif t > self.setpoint + self.band:
            self.pin.value(0)
        return t

    def off(self):
        self.pin.value(0)


def hold_s(seconds, heater=None):
    """Wait `seconds`. With a heater, keep stepping the thermostat, but never start a ~0.75 s sensor
    conversion in the last 0.9 s, so short waits stay accurate to ~20 ms."""
    end = time.ticks_add(time.ticks_ms(), int(seconds * 1000))
    while True:
        left = time.ticks_diff(end, time.ticks_ms())
        if left <= 0:
            return
        if heater and left > 900:
            heater.step()
        else:
            feed()
            time.sleep_ms(min(left, 20))


def preheat(heater, hold_for_s=1800, timeout_s=7200, tol_c=1.0):
    """Bring the box to heater.setpoint, then keep it within tol_c for hold_for_s before any measurement.
    Raises RuntimeError if there is no sensor, if the set point is not reached within timeout_s (dead heater,
    open fuse, sensor off the board), or if it cannot be held. The caller's 'finally' turns the heater off."""
    if not heater.thermo.roms:
        heater.off()
        raise RuntimeError("no DS18B20 found: the heater stays off")
    t_start = time.ticks_ms()
    t_in = None
    reached = False
    n = 0
    while True:
        t = heater.step()
        now = time.ticks_ms()
        elapsed = time.ticks_diff(now, t_start)
        if n % 30 == 0:
            print("# preheat %.2f C (set point %.1f C, %d s)" % (t, heater.setpoint, elapsed // 1000))
        n += 1
        if t == t and abs(t - heater.setpoint) <= tol_c:
            reached = True
            if t_in is None:
                t_in = now
            elif time.ticks_diff(now, t_in) >= hold_for_s * 1000:
                print("# preheat done: %.1f C held for %d s" % (heater.setpoint, hold_for_s))
                return
        else:
            t_in = None
        if (not reached and elapsed > timeout_s * 1000) or elapsed > (timeout_s + 2 * hold_for_s) * 1000:
            heater.off()
            raise RuntimeError("set point not reached or not held: check the heater, the fuse and the sensor")


def log_schedule(t_min_s, t_max_s, per_decade=4):
    """Log-spaced wait times, e.g. 1, 1.8, 3.2, 5.6, 10, ... seconds."""
    out = []
    k = 0
    while True:
        t = t_min_s * 10 ** (k / per_decade)
        if t > t_max_s * 1.0001:
            break
        out.append(round(t, 3))
        k += 1
    return out
