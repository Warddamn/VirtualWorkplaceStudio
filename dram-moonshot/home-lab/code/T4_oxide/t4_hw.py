# t4_hw.py -- hardware layer for the T4 "mini-SMU" (source-measure unit) on a Raspberry Pi Pico 2.
#
# REFERENCE CODE -- UNTESTED ON HARDWARE. It is syntax-checked and its logic runs on a PC in
# simulation mode (python3 pico_smu.py --sim). Check every pin, gain and limit against YOUR wiring
# before you power anything. Track T4, dram-moonshot home lab (E7 / E8).
#
# Runs on MicroPython (Pico / Pico 2) and, for simulation, on CPython 3 (no numpy needed).
#
# Wiring summary (E7 section 7 has the component-value table and the build order):
#   GP0  PWM -> 15k/1uF -> 15k/1uF (2-pole, ~10 Hz) -> LM358 x9.2 (Rf 82k, Rg 10k; V+ = 30 V)
#        -> [GATE MONITOR TAP here, at the LM358 output] -> 100 kohm -> GATE / WWL0  (node 0..27 V)
#   GP2  PWM -> same filter -> LM358 x6.1 (Rf 51k, Rg 10k) -> 10 kohm -> DRAIN / WBL0
#        [DRAIN MONITOR TAP at the DRAIN node, after the 10 kohm]       (node 0..20 V)
#   GP6  PWM -> same as GP0 (second LM358 half)                            -> WWL1 (array only)
#   GP8  PWM -> 2-pole RC -> follower x1.5                                  -> WBL1 (array only)
#   GP4/GP5 I2C0 SDA/SCL -> 2-channel BSS138 I2C level shifter -> ADS1115 (addr 0x48).
#       The ADS1115 is powered from +5 V (VBUS), never 3.3 V: the TIA output swings 0..5 V.
#       1 kohm in series with each ADS input. AIN0 = TIA0 output (source / RBL0),
#       AIN1 = TIA1 output (RBL1), AIN2 = spare / SN buffer, AIN3 = VREF 2.5 V (LM4040-2.5).
#       Currents are read differentially against VREF.
#   TIA0: LMC6482AIN (A grade, Vos <= 0.75 mV) on +5 V, + input at VREF, - input = SOURCE (E7)
#         or RBL0 (E8); 100 Mohm + 10 pF always in feedback; relay K1 adds 1 Mohm; K2 adds 10 kohm.
#   GP10 / GP11 / GP14 -> ULN2003A inputs 1-3. ULN2003A outputs -> relay coil (-) pins; coil (+)
#         pins -> +5 V; ULN2003A COM (pin 9) -> +5 V (its diodes clamp coil kickback).
#         NEVER drive a reed-relay coil straight from a GPIO pin (3.3 V < 3.75 V must-operate).
#         K1 (GP10) = 1 Mohm range, K2 (GP11) = 10 kohm range, K3 (GP14) = E8 control-cell switch.
#   GP12 / GP13: row-select N-MOSFETs (read-transistor sources of row 0 / row 1 to ground).
#         Use BSS138 (on a SOT-23 adapter) or a 2N7000 you measured with Vth <= 1.8 V.
#   GP15: heater: GP15 -> 220 ohm -> gate of a MOSFET with RDS(on) specified at VGS = 2.5 V;
#         100 kohm gate-to-source (heater OFF whenever the Pico is not driving the pin);
#         10 ohm 25 W resistor on 12 V, in series with a 80 C bimetal thermostat and a ~91 C fuse.
#   GP26 ADC0: GATE monitor (LM358 output, 1 Mohm / 100 kohm divider, /11, 100 nF at the pin)
#   GP27 ADC1: DRAIN monitor (DRAIN node, /11, 100 nF at the pin)
#   GP28 ADC2: NTC thermistor (10 k fixed to 3.3 V, 10 k NTC to ground, 100 nF at the pin)

import math
import sys

try:
    import machine
    import time
    SIM = False
except ImportError:          # CPython: simulation mode
    machine = None
    import time
    SIM = True

CFG = {
    "vref": 2.5,              # TIA virtual node (LM4040-2.5); measured value goes here
    "pwm_freq": 2000,
    "vio": 3.3,               # Pico PWM high level
    "gate_gain": 9.2, "gate_offset": 0.0,      # calibrate_dacs() writes dac_cal.json; Rig loads it
    "drain_gain": 6.1, "drain_offset": 0.0,
    "wwl1_gain": 9.2, "wwl1_offset": 0.0,
    "wbl1_gain": 1.5, "wbl1_offset": 0.0,
    "dac_cal_file": "dac_cal.json",
    "gate_max": 27.0,         # HARD LIMIT. LM358 high output is 27 V min / 28 V typ on a 30 V supply
                              # [DATASHEET], so 27 V is the highest gate node you can count on.
    "drain_max": 20.0,
    "wbl_max": 5.0,           # E8: bit lines never above 5 V
    "mon_div": 11.0,
    "r_hi": 1e8, "r_mid": 1e6, "r_lo": 1e4,
    "tia1_rf": 1e6 * 1e8 / (1e6 + 1e8),
    "relay_settle_ms": 80,
    "vos": [0.0, 0.0],        # TIA0 / TIA1 output offset, volts. zero_offset() measures it.
    "ads_vdd": 5.0,           # ADS1115 supply. Keep 5 V. If you run it at 3.3 V, set 3.3 here.
    "ads_fs": 2.048,
    "ntc_beta": 3950.0, "ntc_r0": 10000.0, "ntc_rfix": 10000.0,
    "t_max_c": 70.0,          # software heater cut-off (the bimetal thermostat is the real guard)
    "t_min_c": 5.0,           # below this the NTC is open or unplugged: heater off
    "heater_duty_max": 0.3,   # ~4.3 W of the 14.4 W heater; 65 C needs ~1-2 W
    "wdt_ms": 8000,           # watchdog for heated runs (0 = off). The Pico reboots ~8 s after
                              # a heated run ends; wait 10 s before the next mpremote command.
}

_SIM_T_MS = [0]
_WDT = [None]


def enable_watchdog(ms=None):
    """Hardware watchdog for heated runs: if the program hangs, the Pico resets, GP15 floats and
    the 100 kohm pull-down turns the heater off. It cannot be stopped once started."""
    ms = CFG["wdt_ms"] if ms is None else ms
    if SIM or not ms or _WDT[0] is not None:
        return
    _WDT[0] = machine.WDT(timeout=int(ms))


def feed_watchdog():
    if _WDT[0] is not None:
        _WDT[0].feed()


def sleep_ms(ms):
    if SIM:
        _SIM_T_MS[0] += int(ms)
        return
    ms = int(ms)
    while ms > 0:                 # sleep in <= 1 s slices so an active watchdog is always fed
        step = 1000 if ms > 1000 else ms
        time.sleep_ms(step)
        feed_watchdog()
        ms -= step


def ticks_ms():
    if SIM:
        return _SIM_T_MS[0]
    return time.ticks_ms()


def elapsed_s(t0_ms):
    if SIM:
        return (_SIM_T_MS[0] - t0_ms) / 1000.0
    return time.ticks_diff(time.ticks_ms(), t0_ms) / 1000.0


# ------------------------------------------------------------------------------------------
# Logging: print every line; on the Pico, optionally also append it to a file in flash, so an
# overnight run survives a sleeping laptop or a dropped USB link (recover: mpremote cp :name .)
# ------------------------------------------------------------------------------------------
_LOG = [None]


def set_log(name):
    close_log()
    if SIM or not name:
        return
    try:
        _LOG[0] = open(name, "a")
    except OSError:
        _LOG[0] = None


def emit(line):
    print(line)
    f = _LOG[0]
    if f is not None:
        f.write(line + "\n")
        f.flush()


def close_log():
    if _LOG[0] is not None:
        try:
            _LOG[0].close()
        except OSError:
            pass
    _LOG[0] = None


# ------------------------------------------------------------------------------------------
# ADS1115 driver (register map per TI ADS1115 datasheet; verify against your copy)
# ------------------------------------------------------------------------------------------
class ADS1115:
    PGA = {6.144: 0, 4.096: 1, 2.048: 2, 1.024: 3, 0.512: 4, 0.256: 5}
    MUX = {"0-1": 0, "0-3": 1, "1-3": 2, "2-3": 3, "0": 4, "1": 5, "2": 6, "3": 7}

    def __init__(self, i2c, addr=0x48):
        self.i2c = i2c
        self.addr = addr

    def read(self, mux="0-3", fs=2.048, dr=3):
        """One single-shot conversion. dr: 0..7 = 8,16,32,64,128,250,475,860 samples/s."""
        cfg = 0x8000 | (self.MUX[mux] << 12) | (self.PGA[fs] << 9) | 0x0100 | (dr << 5) | 0x0003
        self.i2c.writeto_mem(self.addr, 0x01, bytes([cfg >> 8, cfg & 0xFF]))
        for _ in range(200):
            sleep_ms(2)
            b = self.i2c.readfrom_mem(self.addr, 0x01, 2)
            if b[0] & 0x80:
                break
        b = self.i2c.readfrom_mem(self.addr, 0x00, 2)
        raw = (b[0] << 8) | b[1]
        if raw & 0x8000:
            raw -= 65536
        return raw * fs / 32768.0


class PwmDac:
    """PWM + 2-pole RC filter + op-amp gain stage. v = gain * vio * duty + offset."""

    def __init__(self, pin, gain, offset, vmax):
        self.gain, self.offset, self.vmax = gain, offset, vmax
        self.v = 0.0
        self.pwm = None
        if not SIM:
            self.pwm = machine.PWM(machine.Pin(pin))
            self.pwm.freq(CFG["pwm_freq"])
            self.pwm.duty_u16(0)

    def set(self, v):
        v = max(0.0, min(float(v), self.vmax))
        self.v = v
        duty = (v - self.offset) / (self.gain * CFG["vio"])
        duty = max(0.0, min(duty, 1.0))
        if self.pwm is not None:
            self.pwm.duty_u16(int(duty * 65535))
        return v


def load_dac_cal():
    """Load dac_cal.json (written by calibrate_dacs) into CFG. Returns True if found."""
    try:
        import json
        with open(CFG["dac_cal_file"]) as f:
            cal = json.load(f)
    except (OSError, ValueError, ImportError):
        return False
    for k in ("gate_gain", "gate_offset", "drain_gain", "drain_offset"):
        if k in cal:
            CFG[k] = float(cal[k])
    return True


def _overload(v_raw, k):
    """True if the TIA output is clipped (ADS full scale) or, with a 3.3 V ADS, above its rail."""
    if abs(v_raw) > 0.93 * CFG["ads_fs"]:
        return True
    if CFG["ads_vdd"] < 4.5 and v_raw > CFG["ads_vdd"] - CFG["vref"] - 0.1:
        return True
    return False


# ------------------------------------------------------------------------------------------
# Real rig
# ------------------------------------------------------------------------------------------
class Rig:
    def __init__(self):
        P = machine.Pin
        self.dac_cal_loaded = load_dac_cal()
        self.i2c = machine.I2C(0, sda=P(4), scl=P(5), freq=400000)
        self.adc = ADS1115(self.i2c)
        self.gate = PwmDac(0, CFG["gate_gain"], CFG["gate_offset"], CFG["gate_max"])
        self.drain = PwmDac(2, CFG["drain_gain"], CFG["drain_offset"], CFG["drain_max"])
        self.wwl1 = PwmDac(6, CFG["wwl1_gain"], CFG["wwl1_offset"], CFG["gate_max"])
        self.wbl1 = PwmDac(8, CFG["wbl1_gain"], CFG["wbl1_offset"], CFG["wbl_max"])
        self.rly_mid = P(10, P.OUT, value=0)       # via ULN2003A
        self.rly_lo = P(11, P.OUT, value=0)        # via ULN2003A
        self.rsel = [P(12, P.OUT, value=0), P(13, P.OUT, value=0)]
        self.ctrl_relay = P(14, P.OUT, value=0)    # via ULN2003A
        self.heat = machine.PWM(P(15))
        self.heat.freq(100)
        self.heat.duty_u16(0)
        self.mon_g = machine.ADC(26)
        self.mon_d = machine.ADC(27)
        self.ntc = machine.ADC(28)
        self.range = "hi"
        self.set_range("hi")

    # --- sources
    def set_gate(self, v):
        return self.gate.set(v)

    def set_drain(self, v):
        return self.drain.set(v)

    def set_wwl(self, row, v):
        return (self.gate if row == 0 else self.wwl1).set(v)

    def set_wbl(self, col, v):
        v = min(v, CFG["wbl_max"])
        return (self.drain if col == 0 else self.wbl1).set(v)

    def monitor(self):
        k = 3.3 / 65535 * CFG["mon_div"]
        return self.mon_g.read_u16() * k, self.mon_d.read_u16() * k

    # --- current measurement
    def set_range(self, name):
        self.rly_mid.value(1 if name == "mid" else 0)
        self.rly_lo.value(1 if name == "lo" else 0)
        self.range = name
        sleep_ms(CFG["relay_settle_ms"])

    def rf(self, ch=0):
        if ch == 1:
            return CFG["tia1_rf"]
        if self.range == "hi":
            return CFG["r_hi"]
        r_add = CFG["r_mid"] if self.range == "mid" else CFG["r_lo"]
        return 1.0 / (1.0 / CFG["r_hi"] + 1.0 / r_add)

    def _diff(self, ch, n_avg):
        mux = "0-3" if ch == 0 else "1-3"
        s = 0.0
        for _ in range(n_avg):
            v = self.adc.read(mux, CFG["ads_fs"])
            if abs(v) < 0.25:
                v = self.adc.read(mux, 0.256)      # 8x finer steps for small signals
            s += v
        return s / n_avg

    def zero_offset(self, n=32, set_sources=True, chans=(0,), settle_ms=2000):
        """Measure each TIA's output offset with NO current flowing and store it in CFG['vos'].
        It is mostly the op-amp offset voltage (0.11 mV typ, 0.75 mV max for an LMC6482AI) and
        reads as Vos/100 Mohm = 1-7.5 pA if not removed. It does not depend on the range.
        set_sources=True (E7): gate node 0 V (Vgs = -2.5 V, channel off) and drain at VREF
        (Vds = 0), so neither the channel nor the gate oxide can carry current.
        E8: set_sources=False; the row selects are opened instead."""
        if set_sources:
            self.set_gate(0.0)
            self.set_drain(CFG["vref"])
        self.row_select(-1)
        self.set_range("hi")
        sleep_ms(settle_ms)
        vos = list(CFG["vos"])
        for ch in chans:
            vos[ch] = self._diff(ch, n)
        CFG["vos"] = vos
        return vos

    def read_current(self, ch=0, n_avg=4, autorange=True):
        """Signed current INTO the TIA node (A), offset-corrected. E7: drain->source current is
        positive. E8: read current flows OUT of the node, so it reads negative; callers use abs().
        Returns (current, range); the range gets a '!' if the lowest range is still clipped."""
        order = ["lo", "mid", "hi"]
        v_raw = 0.0
        clipped = False
        for _ in range(4):
            v_raw = self._diff(ch, n_avg)
            clipped = _overload(v_raw, 0)
            if ch == 1 or not autorange:
                break
            k = order.index(self.range)
            if clipped and k > 0:
                self.set_range(order[k - 1])
                continue
            if abs(v_raw) < 0.015 and k < 2:
                self.set_range(order[k + 1])
                continue
            break
        v = v_raw - CFG["vos"][ch]
        rng = self.range if ch == 0 else "tia1"
        if clipped:
            rng += "!"
        return -v / self.rf(ch), rng

    # --- E8 helpers
    def row_select(self, row):
        for r in (0, 1):
            self.rsel[r].value(1 if r == row else 0)

    def control_switch(self, on):
        self.ctrl_relay.value(1 if on else 0)

    def temp_c(self):
        v = self.ntc.read_u16() * 3.3 / 65535
        v = min(max(v, 0.01), 3.29)
        r = CFG["ntc_rfix"] * v / (3.3 - v)
        inv = 1.0 / 298.15 + math.log(r / CFG["ntc_r0"]) / CFG["ntc_beta"]
        return 1.0 / inv - 273.15

    def heater(self, duty):
        t = self.temp_c()
        if t > CFG["t_max_c"] or t < CFG["t_min_c"]:   # too hot, or NTC open/unplugged (reads ~-66 C)
            duty = 0.0
        duty = max(0.0, min(duty, CFG["heater_duty_max"]))
        self.heat.duty_u16(int(duty * 65535))
        feed_watchdog()
        return duty

    def all_safe(self):
        for d in (self.gate, self.drain, self.wwl1, self.wbl1):
            d.set(0.0)
        self.heat.duty_u16(0)
        self.row_select(-1)
        self.control_switch(False)
        self.set_range("hi")


# ------------------------------------------------------------------------------------------
# Simulated rig (CPython). Same interface; models one TFT (E7) or a 2x2 gain-cell array (E8).
# ------------------------------------------------------------------------------------------
KB_EV = 8.617333262e-5


def _softplus(x):
    if x > 40:
        return x
    return math.log(1.0 + math.exp(x))


def sim_tft_current(vgs, vds, mu=0.4, vth=7.0, ss=0.9, w_um=1000.0, l_um=10.0, tox_nm=300.0,
                    floor=1.5e-12):
    cox = 3.9 * 8.8541878128e-12 / (tox_nm * 1e-9) / 1e4
    k = 0.5 * mu * cox * w_um / l_um
    m = 2.0 * ss / math.log(10)
    sign = 1.0
    if vds < 0:
        vds, sign = -vds, -1.0
    g1 = m * _softplus((vgs - vth) / m)
    g2 = m * _softplus((vgs - vth - vds) / m)
    # setup floor: a surface/cable leakage path between drain and source, so zero at Vds = 0
    return sign * (k * (g1 * g1 - g2 * g2) + floor * min(1.0, vds / 1.0))


class SimCell:
    """Storage node with an oxide, silicon or ideal (reed relay) write switch.
    LEAK values are ASSUMPTIONS for rehearsal, not predictions. The oxide value (1 pA, Ea 0.35 eV)
    is deliberately placed ABOVE the relay floor (0.1 pA) so the analysis has something to find.
    A real home TFT at WWL = 0 V is predicted to leak ~1e-15 A, i.e. BELOW a ~1 pA rig floor
    (E7 section 1.4): on hardware you will most likely measure the floor (E8 section 1.4)."""
    LEAK = {"oxide": (1.0e-12, 0.35), "si": (1.0e-11, 0.80), "relay": (1.0e-13, 0.10)}

    def __init__(self, switch="oxide", c_sn=10.23e-9, c_ov=173e-12):
        self.switch, self.c = switch, c_sn
        self.c_ov = {"oxide": c_ov, "si": 30e-12, "relay": 1e-12}[switch]   # gate-to-SN coupling
        self.vth = {"oxide": 7.0, "si": 2.0, "relay": 0.0}[switch]
        self.ss = {"oxide": 1.0, "si": 0.09, "relay": 1.0}[switch]       # V/decade
        self.i_vth = {"oxide": 6.3e-8, "si": 1e-6, "relay": 0.0}[switch]  # channel current at Vth
        self.v = 0.0

    def leak_conductance(self, temp_c):
        i25, ea = self.LEAK[self.switch]
        i = i25 * math.exp(-ea / KB_EV * (1 / (temp_c + 273.15) - 1 / 298.15))
        return i / 1.0                            # A per volt of (V_SN - V_WBL): ohmic-like model

    def evolve(self, dt, wwl, wbl, temp_c, forced_on=False):
        if dt <= 0:
            return
        on = forced_on if self.switch == "relay" else (wwl > self.v + self.vth + 0.5)
        if on:                                    # switch on: R_on ~ 200 kohm
            tau = 2e5 * self.c
        else:
            g = self.leak_conductance(temp_c)
            if self.i_vth > 0:                    # subthreshold channel current set by hold bias
                vs = min(self.v, wbl)
                ich = self.i_vth * 10 ** ((wwl - vs - self.vth) / self.ss)
                if self.switch == "oxide":        # same activation as the assumed leak path
                    ich *= math.exp(-0.35 / KB_EV * (1 / (temp_c + 273.15) - 1 / 298.15))
                g += ich / max(abs(self.v - wbl), 0.05)
            tau = self.c / g
        self.v = wbl + (self.v - wbl) * math.exp(-dt / tau)

    def kick(self, wwl_old, wwl_new):
        if self.switch == "relay":
            return
        if wwl_new < wwl_old:
            top = min(wwl_old, self.v + self.vth)
            if top > wwl_new:
                self.v -= (top - wwl_new) * self.c_ov / self.c
        elif wwl_new > wwl_old:                   # rising edge below threshold couples upward
            top = min(wwl_new, self.v + self.vth)
            if top > wwl_old:
                self.v += (top - wwl_old) * self.c_ov / self.c


def sim_read_fet(v_sn):
    """2N7000-like read transistor near threshold (100 mV/decade, 1 nA at 1.0 V, 2 mA cap)."""
    i = 1e-9 * 10 ** ((v_sn - 1.0) / 0.1)
    return i * 2e-3 / (i + 2e-3)


class SimRig:
    VOS_TRUE = (0.45e-3, -0.30e-3)   # simulated TIA offsets (V): 4.5 pA / -3 pA on 100 Mohm

    def __init__(self, mode="tft", switch="oxide", seed=1):
        import random
        self.rnd = random.Random(seed)
        self.mode = mode
        self.vg = self.vd = 0.0
        self.wwl = [0.0, 0.0]
        self.wbl = [0.0, 0.0]
        self.range = "hi"
        self.sel = -1
        self.ctrl = False
        self.t_amb = 24.0
        self.temp = 24.0
        self.duty = 0.0
        self.cells = {(r, c): SimCell(switch) for r in (0, 1) for c in (0, 1)}
        self.last_ms = ticks_ms()
        CFG["vos"] = [0.0, 0.0]               # a fresh rig has an unknown (unmeasured) offset

    def _update(self):
        now = ticks_ms()
        dt = (now - self.last_ms) / 1000.0
        self.last_ms = now
        if dt <= 0:
            return
        t_target = self.t_amb + 250.0 * self.duty         # 14.4 W x ~17 K/W at full duty
        self.temp = t_target + (self.temp - t_target) * math.exp(-dt / 600.0)
        for (r, c), cell in self.cells.items():
            cell.evolve(dt, self.wwl[r], self.wbl[c], self.temp, forced_on=self.ctrl)

    def set_gate(self, v):
        return self.set_wwl(0, v)

    def set_drain(self, v):
        return self.set_wbl(0, v) if self.mode == "cell" else self._set_vd(v)

    def _set_vd(self, v):
        self.vd = max(0.0, min(v, CFG["drain_max"]))
        return self.vd

    def set_wwl(self, row, v):
        self._update()
        v = max(0.0, min(v, CFG["gate_max"]))
        old = self.wwl[row]
        self.wwl[row] = v
        if row == 0:
            self.vg = v
        for c in (0, 1):
            self.cells[(row, c)].kick(old, v)
        return v

    def set_wbl(self, col, v):
        self._update()
        v = max(0.0, min(v, CFG["wbl_max"] if self.mode == "cell" else CFG["drain_max"]))
        self.wbl[col] = v
        if col == 0:
            self.vd = v
        return v

    def monitor(self):
        return self.vg, self.vd

    def set_range(self, name):
        self.range = name
        sleep_ms(CFG["relay_settle_ms"])

    def rf(self, ch=0):
        return {"hi": CFG["r_hi"], "mid": 1e6, "lo": 1e4}[self.range] if ch == 0 else CFG["tia1_rf"]

    def sim_connect(self, what):
        """Simulation only: 'open' = nothing on the TIA input (floor test); 'gleak' = source and
        drain tied to the TIA, so only gate current flows; 'tft' = normal device."""
        self.mode = what

    def _true_current(self, ch):
        if self.mode == "open":
            return 0.0
        if self.mode == "gleak":                     # ~2e14 ohm oxide path, gate -> S+D
            return 5e-15 * (self.vg - CFG["vref"])
        if self.mode == "tft":
            return sim_tft_current(self.vg - CFG["vref"], self.vd - CFG["vref"])
        if self.sel in (0, 1):
            return -sim_read_fet(self.cells[(self.sel, ch)].v)
        return 0.0

    def zero_offset(self, n=32, set_sources=True, chans=(0,), settle_ms=2000):
        if set_sources:
            self.set_gate(0.0)
            self.set_drain(CFG["vref"])
        self.row_select(-1)
        self.range = "hi"
        sleep_ms(settle_ms)
        vos = list(CFG["vos"])
        for ch in chans:
            s = 0.0
            for _ in range(n):
                s += self.VOS_TRUE[ch] - self._true_current(ch) * CFG["r_hi"] + 5e-6 * self.rnd.gauss(0, 1)
            vos[ch] = s / n
        CFG["vos"] = vos
        return vos

    def read_current(self, ch=0, n_avg=4, autorange=True):
        sleep_ms(20 * n_avg)
        self._update()
        i = self._true_current(ch)
        i = i * (1 + 0.003 * self.rnd.gauss(0, 1)) + 5e-14 * self.rnd.gauss(0, 1)
        if ch == 0:
            a = abs(i)
            self.range = "lo" if a > 1.9e-6 else ("mid" if a > 1.5e-8 else "hi")
        rf = self.rf(ch)
        v = -i * rf + self.VOS_TRUE[ch]                 # TIA output relative to VREF
        fs = CFG["ads_fs"]
        clipped = abs(v) > 0.93 * fs
        v = max(-fs, min(v, fs))                        # ADS1115 full scale: the TIA saturates
        rng = self.range if ch == 0 else "tia1"
        if clipped:
            rng += "!"
        return -(v - CFG["vos"][ch]) / rf, rng

    def row_select(self, row):
        self._update()
        self.sel = row

    def control_switch(self, on):
        self._update()
        self.ctrl = bool(on)

    def temp_c(self):
        self._update()
        return self.temp + 0.05 * self.rnd.gauss(0, 1)

    def heater(self, duty):
        self._update()
        if self.temp > CFG["t_max_c"] or self.temp < CFG["t_min_c"]:
            duty = 0.0
        self.duty = max(0.0, min(duty, CFG["heater_duty_max"]))
        return self.duty

    def all_safe(self):
        self.set_wwl(0, 0.0)
        self.set_wwl(1, 0.0)
        self.set_wbl(0, 0.0)
        self.set_wbl(1, 0.0)
        self.duty = 0.0
        self.sel = -1


def make_rig(sim=None, **kw):
    if sim is None:
        sim = SIM
    return SimRig(**kw) if sim else Rig()


def zero_offset(rig, n=32, set_sources=True, chans=(0,)):
    """Module-level wrapper: measure and store the TIA offset(s). Returns CFG['vos']."""
    return rig.zero_offset(n=n, set_sources=set_sources, chans=chans)


def calibrate_dacs(rig=None, points=(0.2, 0.8)):
    """Fit gain/offset of the gate and drain DACs from the ADC monitors (real rig only).
    Run it with NO device connected:
        mpremote exec "import t4_hw as h; h.calibrate_dacs()"
    It writes dac_cal.json to the Pico's flash; every later Rig() loads it automatically.
    Then check 0, 10 and 20 V at the gate node with your multimeter."""
    if SIM:
        print("# calibrate_dacs: nothing to calibrate in simulation")
        return None
    if rig is None:
        rig = make_rig(False)
    res = {}
    for name, dac, idx in (("gate", rig.gate, 0), ("drain", rig.drain, 1)):
        xs, ys = [], []
        for frac in points:
            dac.pwm.duty_u16(int(frac * 65535))
            sleep_ms(500)
            xs.append(frac * CFG["vio"])
            ys.append(rig.monitor()[idx])
        gain = (ys[1] - ys[0]) / (xs[1] - xs[0])
        off = ys[0] - gain * xs[0]
        dac.gain, dac.offset = gain, off
        res[name + "_gain"], res[name + "_offset"] = gain, off
        dac.set(0.0)
    CFG.update(res)
    try:
        import json
        with open(CFG["dac_cal_file"], "w") as f:
            json.dump(res, f)
        print("# dac calibration written to", CFG["dac_cal_file"], res)
    except OSError:
        print("# dac calibration (NOT saved; copy into CFG by hand):", res)
    return res


def is_micropython():
    return sys.implementation.name == "micropython"
