# e4_pico_leakage_bench.py -- MicroPython for Raspberry Pi Pico / Pico 2 (RP2040 / RP2350)
#
# REFERENCE CODE - UNTESTED ON HARDWARE. Syntax-checked only (python3 -m py_compile).
# Check every pin against your own wiring before you power anything.
#
# Home-lab experiment E4, "The DRAM cell is an electrometer" (dram-moonshot track T2).
# It runs one charge-decay leakage measurement on one device under test (DUT):
#   SOAK   : DUT gate ON (write word line, WWL), DUT source at V_write (write bit line, WBL).
#            The storage node (DUT drain + film capacitor + electrometer buffer input) sits at
#            V_write long enough for dielectric absorption to settle.
#   OFF    : gate OFF, then WBL -> 0 V. The DUT now holds the node like a DRAM write transistor.
#   RECORD : log node voltage once per second. Leakage I = -C dV/dt (see leakage_tail.py).
# It also runs a block heater (time-proportional, PI control) with hard safety cut-outs, and
# a time-constant calibration (TAU_CAL) that measures C_node through a known 10 GOhm resistor.
#
# Output: CSV lines on the USB serial port, in the format leakage_tail.py reads:
#   device,temperature,time,voltage,cap_pf,temp_meas_C
# Log it on the PC with:   mpremote run e4_pico_leakage_bench.py > Q001_25C.csv
#
# Wiring (default pins; change below):
#   GP4/GP5  I2C0 SDA/SCL -> ADS1115 (addr 0x48). AIN0 = electrometer buffer OUTPUT (node copy).
#                            AIN2 = calibration source voltage (TAU_CAL only).
#   GP22     1-Wire -> DS18B20 in the heater block (4.7 kOhm pull-up to 3.3 V).
#   GP15     heater MOSFET gate (logic-level N-MOSFET, 100 kOhm gate pull-down to GND).
#   GP16     WWL driver: NPN level shifter to a 9 V battery -> DUT gate. ACTIVE LOW by default:
#            GP16 low = NPN off = gate pulled up to 9 V = DUT ON.  (set WWL_ACTIVE_LOW below)
#   GP17     WBL: GPIO -> 22 kOhm -> DUT source; 10 kOhm from DUT source to GND (~1.03 V when high).
#   GP18     TAU_CAL source step: GPIO -> divider -> far end of the 10 GOhm calibration resistor.

import time
from machine import Pin, I2C, Timer

try:
    from machine import WDT
except ImportError:  # some ports
    WDT = None
import onewire
import ds18x20

# ------------------------------- user settings ------------------------------------------------
MODE = "DUT"             # "DUT", "BLANK" (no device fitted), "TAU_CAL", or "HEAT_ONLY"
DEVICE_ID = "Q001"       # label written into the CSV; use "BLANK" for the floor run
SETPOINT_C = 25.0        # block temperature; the code refuses anything above MAX_SETPOINT_C
HEATER_ENABLED = True    # False = room-temperature run with no heater (SETPOINT_C is then a label)
CAP_PF = 470.0           # your node capacitance (measure it with TAU_CAL)
SOAK_S = 600             # seconds the node is held at V_write before switch-off
RECORD_S = 1800          # seconds of decay to record (use 300-600 s at 65-85 C)
SAMPLE_PERIOD_S = 1.0
TEMP_STABLE_K = 0.2      # start only when within +/- this of setpoint ...
TEMP_STABLE_S = 120      # ... for this long
WWL_ACTIVE_LOW = True
CAL_R_OHM = 10e9         # TAU_CAL resistor (Ohmite HVC1206Z1008KET is 10 GOhm +/-10%)

# ------------------------------- safety limits ------------------------------------------------
MAX_SETPOINT_C = 85.0
HARD_CUTOFF_C = 90.0     # heater latched off above this block reading
MAX_DUTY = 0.8           # never run the heater at 100 %
HEATER_PERIOD_MS = 2000  # time-proportional window: few switching edges near the fA node

# ------------------------------- hardware -----------------------------------------------------
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=100_000)
heater = Pin(15, Pin.OUT, value=0)
wwl = Pin(16, Pin.OUT, value=1 if WWL_ACTIVE_LOW else 0)   # start with DUT OFF
wbl = Pin(17, Pin.OUT, value=0)
calsrc = Pin(18, Pin.OUT, value=0)
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

# ------------------------------- heater control -----------------------------------------------
_state = {"duty": 0.0, "fault": "", "t_block": None, "integ": 0.0}
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
    """PI controller -> duty 0..MAX_DUTY. Gains are a starting point: tune on YOUR block."""
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


def read_block_temp(roms):
    try:
        return ow.read_temp(roms[0])
    except Exception:
        return None


# ------------------------------- main sequences -----------------------------------------------
def csv_header():
    print("device,temperature,time,voltage,cap_pf,temp_meas_C")


def wait_stable(roms, wdt):
    if not HEATER_ENABLED:
        return True
    print("# waiting for block to reach %.1f C (+/-%.2f K for %d s)" % (SETPOINT_C, TEMP_STABLE_K, TEMP_STABLE_S))
    stable_since = None
    last = time.ticks_ms()
    while True:
        ow.convert_temp()
        time.sleep_ms(800)
        t = read_block_temp(roms)
        now = time.ticks_ms()
        heater_update(t, SETPOINT_C, time.ticks_diff(now, last) / 1000)
        last = now
        if wdt:
            wdt.feed()
        if _state["fault"]:
            return False
        if t is not None and abs(t - SETPOINT_C) <= TEMP_STABLE_K:
            stable_since = stable_since or now
            if time.ticks_diff(now, stable_since) >= TEMP_STABLE_S * 1000:
                return True
        else:
            stable_since = None
        print("# T_block=%s duty=%.2f" % (t, _state["duty"]))


def run_dut(roms, wdt):
    label = "BLANK" if MODE == "BLANK" else DEVICE_ID
    if not wait_stable(roms, wdt):
        return
    print("# SOAK %d s: gate ON, WBL high" % SOAK_S)
    wbl.value(1)
    dut_gate(True)
    t_end = time.ticks_add(time.ticks_ms(), SOAK_S * 1000)
    last = time.ticks_ms()
    while time.ticks_diff(t_end, time.ticks_ms()) > 0:
        ow.convert_temp()
        time.sleep_ms(800)
        t = read_block_temp(roms)
        now = time.ticks_ms()
        heater_update(t, SETPOINT_C, time.ticks_diff(now, last) / 1000)
        last = now
        if wdt:
            wdt.feed()
        if _state["fault"]:
            return
    v_soak = adc.mean(4, mux=ADS1115.MUX_AIN0, pga=2)
    print("# node at end of soak: %.6f V" % v_soak)
    dut_gate(False)          # write word line off first (kickback step appears here)
    time.sleep_ms(500)
    wbl.value(0)             # then the bit line goes to 0 V: drain-body junction now reverse biased
    t0 = time.ticks_ms()
    csv_header()
    led.value(1)
    next_ms = 0
    while True:
        el = time.ticks_diff(time.ticks_ms(), t0)
        if el >= RECORD_S * 1000:
            break
        if el < next_ms:
            time.sleep_ms(10)
            continue
        next_ms += int(SAMPLE_PERIOD_S * 1000)
        ow.convert_temp()
        v = adc.mean(4, mux=ADS1115.MUX_AIN0, pga=2)   # ~0.5 s at 8 SPS
        time.sleep_ms(300)
        t = read_block_temp(roms)
        heater_update(t, SETPOINT_C, SAMPLE_PERIOD_S)
        if wdt:
            wdt.feed()
        if _state["fault"]:
            print("# aborted: heater fault")
            break
        print("%s,%.1f,%.2f,%.7f,%.1f,%s" % (label, SETPOINT_C, el / 1000, v, CAP_PF,
                                             ("%.3f" % t) if t is not None else ""))
    led.value(0)
    print("# done. Analyse with: python3 leakage_tail.py --csv <file> --skip-s 60")


def run_tau_cal(wdt):
    """Step the far end of a known resistor; the node relaxes with tau = R * C_node.

    Node and calibration resistor only (no DUT). C_node = tau / R. Prints raw samples and a
    quick log-linear tau estimate. Use ~100 s of data per step for C_node = 100-1000 pF.
    """
    calsrc.value(0)
    print("# TAU_CAL: settling 120 s with source low")
    for _ in range(120):
        time.sleep(1)
        if wdt:
            wdt.feed()
    v_inf_lo = adc.mean(8, mux=ADS1115.MUX_AIN0, pga=2)
    calsrc.value(1)
    t0 = time.ticks_ms()
    print("time_s,v_node,v_source")
    ts, vs = [], []
    while time.ticks_diff(time.ticks_ms(), t0) < 100_000:
        v = adc.read(mux=ADS1115.MUX_AIN0, pga=2, dr=4)   # 128 SPS
        vsrc = adc.read(mux=ADS1115.MUX_AIN2, pga=2, dr=4)
        el = time.ticks_diff(time.ticks_ms(), t0) / 1000
        ts.append(el)
        vs.append(v)
        print("%.3f,%.6f,%.6f" % (el, v, vsrc))
        if wdt:
            wdt.feed()
    v_inf = sum(vs[-50:]) / 50
    # tau from the time to reach 63.2 % of the step
    target = v_inf_lo + 0.632 * (v_inf - v_inf_lo)
    tau = None
    for t, v in zip(ts, vs):
        if (v - target) * (v_inf - v_inf_lo) >= 0:
            tau = t
            break
    if tau:
        print("# tau ~ %.2f s  ->  C_node ~ %.0f pF (R = %.3g Ohm, +/- the resistor tolerance)"
              % (tau, tau / CAL_R_OHM * 1e12, CAL_R_OHM))
    calsrc.value(0)


def main():
    if SETPOINT_C > MAX_SETPOINT_C:
        raise ValueError("setpoint above %.0f C is not allowed in this build" % MAX_SETPOINT_C)
    roms = ow.scan()
    if not roms:
        print("# no DS18B20 found: heater disabled")
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
            wait_stable(roms, wdt)
    finally:
        tim.deinit()
        heater.value(0)
        dut_gate(False)
        wbl.value(0)
        print("# heater off, DUT off")
        if wdt:
            # The watchdog cannot be stopped on RP2040/RP2350. The script ends here and the board
            # resets itself ~8 s later; that is normal and leaves every output pin low (safe).
            print("# watchdog will reset the board in ~8 s (normal)")


main()
