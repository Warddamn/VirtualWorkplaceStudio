# t4_hw.py -- hardware layer for the T4 "mini-SMU" (source-measure unit) on a Raspberry Pi Pico 2.
#
# REFERENCE CODE -- UNTESTED ON HARDWARE. It is syntax-checked and its logic runs on a PC in
# simulation mode (python3 pico_smu.py --sim). Check every pin, gain and limit against YOUR wiring
# before you power anything. Track T4, dram-moonshot home lab (E7 / E8).
#
# Runs on MicroPython (Pico / Pico 2) and, for simulation, on CPython 3 (no numpy needed).
#
# Wiring summary (see E7 section "Build the T4 mini-SMU" for the full schematic in words):
#   GP0  PWM -> 2-pole RC (10 Hz) -> LM358 x9.2 (30 V supply) -> 100 kohm -> GATE / WWL0
#   GP2  PWM -> 2-pole RC (10 Hz) -> LM358 x6.1               -> 1 kohm   -> DRAIN / WBL0
#   GP6  PWM -> same as GP0 (second LM358 half)                            -> WWL1 (array only)
#   GP8  PWM -> 2-pole RC -> follower x1.5                                  -> WBL1 (array only)
#   GP4/GP5 I2C0 SDA/SCL -> ADS1115 (addr 0x48)
#       ADS AIN0 = TIA0 output (source / RBL0), AIN1 = TIA1 output (RBL1), AIN2 = spare / SN buffer,
#       AIN3 = VREF 2.5 V (LM4040-2.5). Currents are read differentially against VREF.
#   TIA0: LMC6482, + input at VREF, - input = SOURCE (E7) or RBL0 (E8); 100 Mohm + 10 pF always in
#         feedback; reed relay on GP10 adds 1 Mohm in parallel; reed relay on GP11 adds 10 kohm.
#   GP12 / GP13: row-select N-MOSFETs (read-transistor sources of row 0 / row 1 to ground)
#   GP14: reed relay used as an "ideal switch" for the control cell (E8)
#   GP15: heater PWM -> logic-level MOSFET -> 10 ohm 25 W resistor on 12 V (thermal fuse in series)
#   GP26 ADC0: GATE monitor (1 Mohm / 100 kohm divider, /11)   GP27 ADC1: DRAIN monitor (/11)
#   GP28 ADC2: NTC thermistor (10 k fixed to 3.3 V, 10 k NTC to ground)

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
    "gate_gain": 9.2, "gate_offset": 0.0,      # calibrate with calibrate_dacs()
    "drain_gain": 6.1, "drain_offset": 0.0,
    "wwl1_gain": 9.2, "wwl1_offset": 0.0,
    "wbl1_gain": 1.5, "wbl1_offset": 0.0,
    "gate_max": 28.0,         # HARD LIMITS (the 30 V rule). Never raise above 30.
    "drain_max": 20.0,
    "wbl_max": 5.0,           # E8: bit lines never above 5 V
    "mon_div": 11.0,
    "r_hi": 1e8, "r_mid": 1e6, "r_lo": 1e4,
    "tia1_rf": 1e6 * 1e8 / (1e6 + 1e8),
    "relay_settle_ms": 80,
    "ntc_beta": 3950.0, "ntc_r0": 10000.0, "ntc_rfix": 10000.0,
    "t_max_c": 70.0,          # software heater cut-off (hardware thermal fuse is the real guard)
}

_SIM_T_MS = [0]


def sleep_ms(ms):
    if SIM:
        _SIM_T_MS[0] += int(ms)
    else:
        time.sleep_ms(int(ms))


def ticks_ms():
    if SIM:
        return _SIM_T_MS[0]
    return time.ticks_ms()


def elapsed_s(t0_ms):
    if SIM:
        return (_SIM_T_MS[0] - t0_ms) / 1000.0
    return time.ticks_diff(time.ticks_ms(), t0_ms) / 1000.0


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


# ------------------------------------------------------------------------------------------
# Real rig
# ------------------------------------------------------------------------------------------
class Rig:
    def __init__(self):
        P = machine.Pin
        self.i2c = machine.I2C(0, sda=P(4), scl=P(5), freq=400000)
        self.adc = ADS1115(self.i2c)
        self.gate = PwmDac(0, CFG["gate_gain"], CFG["gate_offset"], CFG["gate_max"])
        self.drain = PwmDac(2, CFG["drain_gain"], CFG["drain_offset"], CFG["drain_max"])
        self.wwl1 = PwmDac(6, CFG["wwl1_gain"], CFG["wwl1_offset"], CFG["gate_max"])
        self.wbl1 = PwmDac(8, CFG["wbl1_gain"], CFG["wbl1_offset"], CFG["wbl_max"])
        self.rly_mid = P(10, P.OUT, value=0)
        self.rly_lo = P(11, P.OUT, value=0)
        self.rsel = [P(12, P.OUT, value=0), P(13, P.OUT, value=0)]
        self.ctrl_relay = P(14, P.OUT, value=0)
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
            v = self.adc.read(mux, 2.048)
            if abs(v) < 0.25:
                v = self.adc.read(mux, 0.256)      # 8x finer steps for small signals
            s += v
        return s / n_avg

    def read_current(self, ch=0, n_avg=4, autorange=True):
        """Signed current INTO the TIA node (A). E7: drain->source current is positive.
        E8: read current flows OUT of the node, so it reads negative; callers use abs()."""
        order = ["lo", "mid", "hi"]
        for _ in range(4):
            v = self._diff(ch, n_avg)
            if ch == 1 or not autorange:
                break
            k = order.index(self.range)
            if abs(v) > 1.9 and k > 0:
                self.set_range(order[k - 1])
                continue
            if abs(v) < 0.015 and k < 2:
                self.set_range(order[k + 1])
                continue
            break
        return -v / self.rf(ch), self.range

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
        if self.temp_c() > CFG["t_max_c"]:
            duty = 0.0
        self.heat.duty_u16(int(max(0.0, min(duty, 1.0)) * 65535))

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
    return sign * (k * (g1 * g1 - g2 * g2) + floor)


class SimCell:
    """Storage node with an oxide, silicon or ideal (reed relay) write switch."""
    LEAK = {"oxide": (1.0e-12, 0.35), "si": (1.0e-11, 0.80), "relay": (1.0e-13, 0.10)}

    def __init__(self, switch="oxide", c_sn=10.18e-9, c_ov=115e-12):
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


def sim_read_fet(v_sn):
    """2N7000-like read transistor near threshold (100 mV/decade, 1 nA at 1.0 V, 2 mA cap)."""
    i = 1e-9 * 10 ** ((v_sn - 1.0) / 0.1)
    return i * 2e-3 / (i + 2e-3)


class SimRig:
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

    def _update(self):
        now = ticks_ms()
        dt = (now - self.last_ms) / 1000.0
        self.last_ms = now
        if dt <= 0:
            return
        t_target = self.t_amb + 60.0 * self.duty          # ~60 K full-scale rise
        self.temp = t_target + (self.temp - t_target) * math.exp(-dt / 60.0)
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

    def read_current(self, ch=0, n_avg=4, autorange=True):
        sleep_ms(20 * n_avg)
        self._update()
        if self.mode == "tft":
            i = sim_tft_current(self.vg - CFG["vref"], self.vd - CFG["vref"])
        else:
            i = 0.0
            if self.sel in (0, 1):
                i = -sim_read_fet(self.cells[(self.sel, ch)].v)
        i = i * (1 + 0.003 * self.rnd.gauss(0, 1)) + 5e-14 * self.rnd.gauss(0, 1)
        a = abs(i)
        self.range = "lo" if a > 1.9e-6 else ("mid" if a > 1.5e-8 else "hi")
        return i, self.range

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
        if self.temp > CFG["t_max_c"]:
            duty = 0.0
        self.duty = max(0.0, min(duty, 1.0))

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


def calibrate_dacs(rig, points=(0.2, 0.8)):
    """Fit gain/offset of the gate and drain DACs from the ADC monitors (real rig only)."""
    if SIM:
        return
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
        res[name] = (gain, off)
        dac.set(0.0)
    print("# dac calibration (gain, offset):", res)
    return res


def is_micropython():
    return sys.implementation.name == "micropython"
