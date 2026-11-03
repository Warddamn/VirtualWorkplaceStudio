# e4_pico_leakage_bench.py -- MicroPython for Raspberry Pi Pico / Pico 2 (RP2040 / RP2350)
#
# REFERENCE CODE - UNTESTED ON HARDWARE. Syntax-checked only (python3 -m py_compile).
# Check every pin against your own wiring before you power anything.
#
# Home-lab experiment E4, "The DRAM cell is an electrometer" (dram-moonshot track T2).
# It runs a charge-decay leakage measurement on one device under test (DUT):
#   SOAK   : DUT gate ON (write word line, WWL), DUT source at V_write (write bit line, WBL).
#            The storage node (DUT drain + film capacitor + electrometer buffer input) sits at
#            V_write long enough for dielectric absorption to settle.
#            BLANK mode (no DUT): the node is written through the 10 GOhm resistor instead
#            (analog switch on "A" = write/calibration source), then the switch goes to "B".
#   OFF    : gate OFF, then WBL -> 0 V. The DUT now holds the node like a DRAM write transistor.
#   RECORD : log node voltage once per second. Leakage I = -C dV/dt (see leakage_tail.py).
#            The run STOPS by itself if the node leaves V_MIN..V_MAX or droops more than
#            DROOP_MAX_V: past that point the trace measures the buffer's rail, not the device.
# Optional SERIES runs one inserted device at several block temperatures in one unattended run.
# It also runs a block heater (time-proportional, PI control) with firmware cut-outs, a
# time-constant calibration (TAU_CAL) and a heater-only hold (HEAT_ONLY, used by E5).
#
# Output: CSV lines on the USB serial port, in the format leakage_tail.py reads:
#   device,temperature,time,voltage,cap_pf,temp_meas_C
# Log it on the PC with a NEW file name each run (see "Protect your data" in the E4 guide):
#   mpremote run e4_pico_leakage_bench.py | tee 2026-11-03_Q001_25C_r1.csv
#
# Wiring (default pins; change below):
#   GP4/GP5  I2C0 SDA/SCL -> ADS1115 (addr 0x48), ADS1115 VDD from the Pico 3V3(OUT), NOT 5 V.
#            AIN0 = electrometer buffer OUTPUT through 10 kOhm (node copy).
#            AIN2 = write/calibration source voltage "SRC".
#   GP22     1-Wire -> DS18B20 (4.7 kOhm pull-up to 3.3 V). Fit it even at room temperature.
#   GP15     heater MOSFET gate (logic-level N-MOSFET, 100 kOhm gate pull-down to GND).
#   GP16     WWL driver: NPN level shifter to a 9 V battery -> DUT gate. ACTIVE LOW by default:
#            GP16 low = NPN off = gate pulled up to 9 V = DUT ON.  (set WWL_ACTIVE_LOW below)
#   GP17     WBL: GPIO -> 22 kOhm -> DUT source; 10 kOhm from DUT source to GND (~1.03 V when high).
#   GP18     SRC level: 3.3 V -47k- SRC -10k- GND, and GP18 -47k- SRC.
#            GP18 low -> SRC ~0.49 V; GP18 high -> SRC ~0.99 V (check both with a meter).
#   GP19     select of one 74HCT4053 section (100 kOhm pull-down to GND). The section's common
#            pin goes to the far end of the 10 GOhm resistor, whose near end stays soldered to
#            the node for good.  GP19 low = "B" = buffer output (bootstrap: ~Vos across R).
#                                GP19 high = "A" = SRC (write the node / calibrate).

import time
import array
from machine import Pin, I2C, Timer

try:
    from machine import WDT
except ImportError:  # some ports
    WDT = None
import onewire
import ds18x20

# ------------------------------- user settings ------------------------------------------------
MODE = "DUT"             # "DUT", "BLANK" (no device fitted), "TAU_CAL", or "HEAT_ONLY"
DEVICE_ID = "Q001"       # label written into the CSV; BLANK mode writes "BLANK"
SETPOINT_C = 25.0        # block temperature; the code refuses anything above MAX_SETPOINT_C
SERIES = None            # e.g. ((25, 1800), (45, 900), (65, 300), (85, 120)): (setpoint C, RECORD_S)
                         # pairs measured in order on the SAME inserted device (needs the heater)
HEATER_ENABLED = False   # False = room-temperature run with no heater (SETPOINT_C is then a label)
CAP_PF = 10000.0         # your MEASURED node capacitance in pF: multimeter for >= 2.2 nF,
                         # TAU_CAL for smaller. 10 nF is the default for 2N7000s; 470 pF for blanks.
SOAK_S = 600             # seconds the node is held at V_write before switch-off
RECORD_S = 600           # seconds of decay to record (use leakage_tail.py --plan to choose)
SAMPLE_PERIOD_S = 1.0
TEMP_STABLE_K = 0.2      # start only when within +/- this of setpoint ...
TEMP_STABLE_S = 120      # ... for this long
WWL_ACTIVE_LOW = True
CAL_R_OHM = 10e9         # write/calibration resistor (Ohmite HVC1206Z1008KET is 10 GOhm +/-10%)
CAL_SETTLE_S = 120       # TAU_CAL: time at the low SRC level first; >= 10 x tau
CAL_WINDOW_S = 100       # TAU_CAL: capture after the step; >= 10 x tau (tau = CAL_R_OHM x C)
HOLD_HEAT_S = 3600       # HEAT_ONLY: keep holding the setpoint this long once it is stable (E5)

# Valid node window (must match V_LO / V_HI / DROOP_MAX in leakage_tail.py)
V_MIN = 0.45             # below this the single-supply buffer output is near its rail
V_MAX = 2.04             # ADS1115 +/-2.048 V full scale
DROOP_MAX_V = 0.5        # stop once the node has fallen this far

# ------------------------------- safety limits ------------------------------------------------
MAX_SETPOINT_C = 85.0    # E5 warm box: set 60 (the BBD's limit)
HARD_CUTOFF_C = 90.0     # heater latched off above this block reading
MAX_DUTY = 1.0           # heater = two 10 Ohm resistors in SERIES on 12 V = 7.2 W at full duty.
                         # If you ever wire them in parallel (28.8 W), set MAX_DUTY = 0.3.
HEATER_PERIOD_MS = 2000  # time-proportional window: few switching edges near the fA node
RUNAWAY_S = 180          # fault if the duty stays high this long while the block barely warms

# ------------------------------- hardware -----------------------------------------------------
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=100_000)
heater = Pin(15, Pin.OUT, value=0)
wwl = Pin(16, Pin.OUT, value=1 if WWL_ACTIVE_LOW else 0)   # start with DUT OFF
wbl = Pin(17, Pin.OUT, value=0)
calsrc = Pin(18, Pin.OUT, value=0)
wsel = Pin(19, Pin.OUT, value=0)                            # "B": bootstrap
try:
    led = Pin("LED", Pin.OUT)
except (TypeError, ValueError):
    led = Pin(25, Pin.OUT)
ow = ds18x20.DS18X20(onewire.OneWire(Pin(22)))


def dut_gate(on):
    if WWL_ACTIVE_LOW:
        wwl.value(0 if on else 1)
    else:
        wwl.value(1 if on else 0)


class ADS1115:
    FS = (6.144, 4.096, 2.048, 1.024, 0.512, 0.256)
    MUX_AIN0, MUX_AIN1, MUX_AIN2, MUX_AIN3 = 4, 5, 6, 7

    def __init__(self, bus, addr=0x48):
        self.bus, self.addr = bus, addr

    def read(self, mux=4, pga=2, dr=0):
        """Single-shot conversion. pga=2 is +/-2.048 V (62.5 uV LSB). dr=0 is 8 samples/s."""
        cfg = 0x8000 | (mux << 12) | (pga << 9) | 0x0100 | (dr << 5) | 0x0003
        self.bus.writeto_mem(self.addr, 0x01, bytes([cfg >> 8, cfg & 0xFF]))
        t0 = time.ticks_ms()
        while True:
            b = self.bus.readfrom_mem(self.addr, 0x01, 2)
            if b[0] & 0x80:
                break
            if time.ticks_diff(time.ticks_ms(), t0) > 400:
                raise OSError("ADS1115 conversion timeout")
            time.sleep_ms(5)
        b = self.bus.readfrom_mem(self.addr, 0x00, 2)
        raw = (b[0] << 8) | b[1]
        if raw & 0x8000:
            raw -= 65536
        return raw * self.FS[pga] / 32768.0

    def mean(self, n=4, **kw):
        s = 0.0
        for _ in range(n):
            s += self.read(**kw)
        return s / n


adc = ADS1115(i2c)


def read_node(n=4):
    return adc.mean(n, mux=ADS1115.MUX_AIN0, pga=2)


# ------------------------------- temperature --------------------------------------------------
def start_conv(roms):
    """Start a DS18B20 conversion. Returns False (never raises) if no sensor answers:
    the driver's convert_temp() calls ow.reset(True), which raises OneWireError then."""
    if not roms:
        return False
    try:
        ow.convert_temp()
        return True
    except Exception:
        return False


def read_block_temp(roms, started=True):
    if not roms or not started:
        return None
    try:
        return ow.read_temp(roms[0])
    except Exception:
        return None


# ------------------------------- heater control -----------------------------------------------
_state = {"duty": 0.0, "fault": "", "t_block": None, "integ": 0.0, "rw_ms": None, "rw_T": 0.0}
_phase_ms = [0]


def _heater_tick(_t):
    # 100 Hz tick: heater ON for duty x HEATER_PERIOD_MS of every window.
    _phase_ms[0] = (_phase_ms[0] + 10) % HEATER_PERIOD_MS
    on = (not _state["fault"]) and (_phase_ms[0] < _state["duty"] * HEATER_PERIOD_MS)
    heater.value(1 if on else 0)


def heater_fault(msg):
    _state["fault"] = msg
    _state["duty"] = 0.0
    heater.value(0)
    print("# HEATER FAULT:", msg)


def heater_update(t_block, setpoint, dt_s, kp=0.08, ki=0.0015):
    """PI controller -> duty 0..MAX_DUTY. Gains are a starting point: tune on YOUR block.
    These checks use the SAME sensor as the controller: they are not independent cut-outs."""
    if not HEATER_ENABLED:
        _state["duty"] = 0.0
        return
    if t_block is None:
        heater_fault("no temperature reading")
        return
    if t_block > HARD_CUTOFF_C:
        heater_fault("block above %.1f C" % HARD_CUTOFF_C)
        return
    err = setpoint - t_block
    _state["integ"] += err * dt_s
    _state["integ"] = max(-200.0, min(200.0, _state["integ"]))   # anti-windup
    d = kp * err + ki * _state["integ"]
    _state["duty"] = max(0.0, min(MAX_DUTY, d))
    # Runaway check: high duty for RUNAWAY_S while the block warms < 2 K means the sensor has
    # slipped out of the block (the heater would run on unchecked) or the heater is too weak.
    if _state["duty"] >= 0.5 and err > 3.0:
        now = time.ticks_ms()
        if _state["rw_ms"] is None:
            _state["rw_ms"], _state["rw_T"] = now, t_block
        elif time.ticks_diff(now, _state["rw_ms"]) > RUNAWAY_S * 1000:
            if t_block - _state["rw_T"] < 2.0:
                heater_fault("%d s at high duty, block rose < 2 K: sensor off the block, or heater "
                             "too weak for this setpoint" % RUNAWAY_S)
                return
            _state["rw_ms"], _state["rw_T"] = now, t_block
    else:
        _state["rw_ms"] = None


def thermal_step(roms, setpoint, wdt, last_ms):
    """One ~0.8 s step: convert, read, update the heater, feed the watchdog. Returns (t, now_ms)."""
    started = start_conv(roms)
    time.sleep_ms(800)
    t = read_block_temp(roms, started)
    now = time.ticks_ms()
    heater_update(t, setpoint, time.ticks_diff(now, last_ms) / 1000)
    if wdt:
        wdt.feed()
    return t, now


# ------------------------------- main sequences -----------------------------------------------
def csv_header():
    print("device,temperature,time,voltage,cap_pf,temp_meas_C")


def wait_stable(roms, wdt, setpoint):
    if not HEATER_ENABLED:
        return True
    print("# waiting for block to reach %.1f C (+/-%.2f K for %d s)" % (setpoint, TEMP_STABLE_K, TEMP_STABLE_S))
    stable_since = None
    last = time.ticks_ms()
    while True:
        t, last = thermal_step(roms, setpoint, wdt, last)
        if _state["fault"]:
            return False
        if t is not None and abs(t - setpoint) <= TEMP_STABLE_K:
            stable_since = stable_since or last
            if time.ticks_diff(last, stable_since) >= TEMP_STABLE_S * 1000:
                return True
        else:
            stable_since = None
        print("# T_block=%s duty=%.2f" % (t, _state["duty"]))


def hold_heat(roms, wdt, setpoint, seconds):
    """Keep the block at the setpoint for `seconds` (HEAT_ONLY, e.g. E5's warm BBD runs)."""
    print("# holding %.1f C for %d s" % (setpoint, seconds))
    t_end = time.ticks_add(time.ticks_ms(), int(seconds * 1000))
    last = time.ticks_ms()
    while time.ticks_diff(t_end, time.ticks_ms()) > 0:
        t, last = thermal_step(roms, setpoint, wdt, last)
        if _state["fault"]:
            return False
        print("# T_block=%s duty=%.2f" % (t, _state["duty"]))
    return True


def soak(roms, wdt, setpoint, seconds):
    t_end = time.ticks_add(time.ticks_ms(), int(seconds * 1000))
    last = time.ticks_ms()
    while time.ticks_diff(t_end, time.ticks_ms()) > 0:
        _, last = thermal_step(roms, setpoint, wdt, last)
        if _state["fault"]:
            return False
    return True


def run_one(roms, wdt, setpoint, record_s):
    """One full write-soak-release-record sequence at one block temperature."""
    label = "BLANK" if MODE == "BLANK" else DEVICE_ID
    if not wait_stable(roms, wdt, setpoint):
        return False
    soak_s = SOAK_S
    if MODE == "BLANK":
        # No device can write the node, so write it through the 10 GOhm resistor: switch on "A".
        tau = CAL_R_OHM * CAP_PF * 1e-12
        soak_s = max(SOAK_S, int(6 * tau) + 1)
        calsrc.value(1)                     # SRC ~0.99 V
        wsel.value(1)                       # "A"
        print("# BLANK: writing the node to SRC through %.0f GOhm (tau = %.0f s); soak %d s"
              % (CAL_R_OHM / 1e9, tau, soak_s))
    else:
        wsel.value(0)                       # "B": the resistor is bootstrapped, carries ~Vos/R only
        wbl.value(1)
        dut_gate(True)
        print("# SOAK %d s: gate ON, WBL high" % soak_s)
    if not soak(roms, wdt, setpoint, soak_s):
        return False
    print("# node at end of soak: %.6f V" % read_node())
    if MODE == "BLANK":
        wsel.value(0)                       # "B": far end now follows the node (bootstrap)
        calsrc.value(0)
    else:
        dut_gate(False)                     # write word line off first (kickback step appears here)
        time.sleep_ms(500)
        wbl.value(0)                        # then the bit line goes to 0 V: drain junction reverse biased
    time.sleep_ms(500)
    v0 = read_node()
    if not (V_MIN <= v0 <= V_MAX):
        print("# INVALID: node at %.3f V, outside %.2f-%.2f V. A railed buffer or a clipped ADC looks like a"
              " perfect floor. Re-write the node (BLANK: check the 4053 and SRC) and run again." % (v0, V_MIN, V_MAX))
        return False
    t0 = time.ticks_ms()
    csv_header()
    led.value(1)
    next_ms = 0
    stopped = False
    while True:
        el = time.ticks_diff(time.ticks_ms(), t0)
        if el >= record_s * 1000:
            break
        if el < next_ms:
            time.sleep_ms(10)
            continue
        next_ms += int(SAMPLE_PERIOD_S * 1000)
        started = start_conv(roms)
        v = read_node()                     # ~0.5 s at 8 SPS
        time.sleep_ms(300)
        t = read_block_temp(roms, started)
        heater_update(t, setpoint, SAMPLE_PERIOD_S)
        if wdt:
            wdt.feed()
        if _state["fault"]:
            print("# aborted: heater fault")
            stopped = True
            break
        print("%s,%.1f,%.2f,%.7f,%.1f,%s" % (label, setpoint, el / 1000, v, CAP_PF,
                                             ("%.3f" % t) if t is not None else ""))
        if v < V_MIN or v > V_MAX or v < v0 - DROOP_MAX_V:
            print("# node drained or left %.2f-%.2f V (now %.3f V, started %.3f V): stopping. The device leaked"
                  " MORE than this node can hold; re-run with a ~10x larger CAP_PF." % (V_MIN, V_MAX, v, v0))
            stopped = True
            break
    led.value(0)
    print("# done. Analyse with: python3 leakage_tail.py --csv <file> --skip-s %d" % (60 if record_s >= 120 else 10))
    return not (stopped and _state["fault"])


def run_dut(roms, wdt):
    series = SERIES if SERIES else ((SETPOINT_C, RECORD_S),)
    for setpoint, record_s in series:
        if not run_one(roms, wdt, setpoint, record_s):
            if _state["fault"]:
                return
    dut_gate(False)
    wbl.value(0)


def run_tau_cal(wdt):
    """Step the far end of the known resistor; the node relaxes with tau = R * C_node.

    Use >= 10 tau of data per step (CAL_SETTLE_S and CAL_WINDOW_S). C_node = tau / R.
    The DUT's own drain capacitance is NOT included unless a DUT is inserted (gate off, WBL 0 V).
    Prints every sample; keeps a decimated copy in fixed arrays for the quick 63 % estimate.
    """
    wsel.value(1)                           # "A": resistor far end on SRC
    calsrc.value(0)                         # SRC ~0.49 V: node stays inside the buffer's range
    dut_gate(False)
    wbl.value(0)
    print("# TAU_CAL: settling %d s at the low SRC level (~0.49 V)" % CAL_SETTLE_S)
    for _ in range(CAL_SETTLE_S):
        time.sleep(1)
        if wdt:
            wdt.feed()
    v_lo = read_node(8)
    cap = 3000
    ts = array.array("f", range(cap))
    vs = array.array("f", range(cap))
    every = max(1, int(CAL_WINDOW_S * 35 // cap) + 1)    # ~35 samples/s at 128 SPS, two channels
    n = 0
    k = 0
    calsrc.value(1)                         # step to ~0.99 V
    t0 = time.ticks_ms()
    print("time_s,v_node,v_source")
    while time.ticks_diff(time.ticks_ms(), t0) < CAL_WINDOW_S * 1000:
        v = adc.read(mux=ADS1115.MUX_AIN0, pga=2, dr=4)   # 128 SPS
        vsrc = adc.read(mux=ADS1115.MUX_AIN2, pga=2, dr=4)
        el = time.ticks_diff(time.ticks_ms(), t0) / 1000
        print("%.3f,%.6f,%.6f" % (el, v, vsrc))
        if k % every == 0 and n < cap:
            ts[n] = el
            vs[n] = v
            n += 1
        k += 1
        if wdt:
            wdt.feed()
    calsrc.value(0)
    wsel.value(0)                           # back to "B" (bootstrap)
    if n < 20:
        print("# too few samples for an estimate")
        return
    m = max(1, n // 20)                     # last 5 % of the kept samples
    v_inf = sum(vs[n - m:n]) / m
    target = v_lo + 0.632 * (v_inf - v_lo)
    tau = None
    for i in range(n):
        if (vs[i] - target) * (v_inf - v_lo) >= 0:
            tau = ts[i]
            break
    print("# v_lo = %.4f V, v_inf = %.4f V" % (v_lo, v_inf))
    if tau:
        print("# tau ~ %.2f s  ->  C_node ~ %.0f pF (R = %.3g Ohm, +/- the resistor tolerance)"
              % (tau, tau / CAL_R_OHM * 1e12, CAL_R_OHM))
        if CAL_WINDOW_S < 10 * tau:
            print("# WARNING: CAL_WINDOW_S < 10 tau: v_inf is not settled. Set CAL_WINDOW_S >= %d" % int(10 * tau + 1))
    print("# check it properly: plot ln(v_inf - v) against t; the slope is -1/tau")


def main():
    series = SERIES if SERIES else ((SETPOINT_C, RECORD_S),)
    for sp, _ in series:
        if sp > MAX_SETPOINT_C:
            raise ValueError("setpoint above %.0f C is not allowed in this build" % MAX_SETPOINT_C)
    if SERIES and not HEATER_ENABLED:
        raise ValueError("SERIES needs HEATER_ENABLED = True")
    try:
        roms = ow.scan()
    except Exception:
        roms = []
    if not roms:
        print("# no DS18B20 found: temperature will NOT be logged (fit one: the guide needs it)")
        if HEATER_ENABLED:
            _state["fault"] = "no sensor"
            if MODE != "TAU_CAL":
                raise RuntimeError("heater enabled but no temperature sensor: refusing to run")
    tim = Timer(freq=100, mode=Timer.PERIODIC, callback=_heater_tick)
    wdt = WDT(timeout=8000) if WDT else None   # a hang resets the Pico -> heater pin defaults low
    try:
        if MODE in ("DUT", "BLANK"):
            run_dut(roms, wdt)
        elif MODE == "TAU_CAL":
            run_tau_cal(wdt)
        elif MODE == "HEAT_ONLY":
            if wait_stable(roms, wdt, SETPOINT_C):
                hold_heat(roms, wdt, SETPOINT_C, HOLD_HEAT_S)
        else:
            raise ValueError("unknown MODE")
    finally:
        tim.deinit()
        heater.value(0)
        dut_gate(False)
        wbl.value(0)
        calsrc.value(0)
        wsel.value(0)
        print("# heater off, DUT off, switch on B")
        if wdt:
            # The watchdog cannot be stopped on RP2040/RP2350. The script ends here and the board
            # resets itself ~8 s later; that is normal and leaves every output pin low (safe).
            print("# watchdog will reset the board in ~8 s (normal)")


main()
