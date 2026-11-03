# e2_gain_cell.py -- E2 "A gain cell without a capacitor": three discrete 2T0C cells side by side.
# REFERENCE CODE - UNTESTED ON HARDWARE. MicroPython, Raspberry Pi Pico (RP2040) or Pico 2 (RP2350).
# Needs t1_common.py on the Pico. Wiring: home-lab/E2_gain_cell_no_capacitor.md, "Circuit".
#
# Each cell: WRITE switch (WBL -> storage node SN) + READ transistor (2N7000) whose gate IS the SN.
# Read = source follower: drain on READ_EN, source -> 47 kOhm -> GND; the source goes to an ADC pin.
#
# Pin map:
#   GP15 PWM -> 10 kOhm -> WBL node with 1 uF film to GND (a filtered DAC; tau = 10 ms)
#   (optional, 'fast' runs on millisecond cells only: WBL from a plain GPIO, WBL_GPIO = 14, through 100 Ohm,
#    with the 10 kOhm / 1 uF filter removed. It can only give 0 or 3.3 V.)
#   GP10 -> opto LED (cell A write switch, e.g. 2N7000)   LED ON = switch OFF (hold)
#   GP11 -> opto LED (cell B write switch, e.g. ALD1106)  LED ON = switch OFF (hold)
#   GP12 -> opto LED (cell C write switch, JFET)           LED ON = switch OFF (hold)
#   GP13 -> reed-relay driver transistor (cell C alternative): HIGH = relay closed (write)
#   GP9  -> READ_EN: drains of the three read transistors (3.3 V = reading)
#   GP26/27/28 (ADC0/1/2) <- follower outputs of cells A/B/C
#   GP22 <- DS18B20
#   GP18 -> optional warm-box heater MOSFET gate (E1 guide section 6.5 circuit). Held LOW unless
#           HEATER_SETPOINT_C is set AND MODE is "retention" or "mlc".
#
# Modes:
#   "transfer"  calibration: all switches on, sweep WBL 0..3.3 V, log Vout per cell (maps Vout <-> Vsn)
#   "retention" write V_WRITE into all cells at once, hold, log Vout of each cell every LOG_S seconds.
#               Each write also logs 'kick_before' (switch on), 'kick_after' (2 ms after switch-off, WBL still
#               at the write level: the WWL gate kick) and 'kick_park' (after WBL parks: adds the step coupled
#               through the switch's drain-source capacitance). analyze_t1.py kick prints both steps.
#   "readmany"  write, hold, toggle READ_EN N_READS times while reading; non-destructive read test
#   "fast"      samples into preallocated integer arrays: a few ms with the switches ON ('kick_before'),
#               KICK_MS after switch-off with WBL held ('kick_after'), then WBL is parked with no settling
#               delay and the decay is sampled for FAST_S, fastest first ('retention' rows, t = 0 at the park).
#               Leaky switches lose 100 mV in milliseconds; a 1 s log interval would miss the whole decay.
#   "mlc"       2 bits/cell on cell MLC_CELL: write-verify 4 levels, hold, log (error rates offline)
# Output: CSV over USB serial. No mode asks questions: mpremote run e2_gain_cell.py > e2_ret_room.csv
# Use a new file name for every run; also set LOGFILE for runs longer than 10 min.
# With a heater: to stop, unplug the 12 V adapter first, then press Thonny's Stop.

import time
import array
from machine import Pin, PWM, ADC
from t1_common import (adc_volts, CsvLog, Thermo, Heater, Clock, low_ripple_supply, hold_s, preheat,
                       start_watchdog, ADC_FULL_SCALE_V)

MODE = "retention"
LABEL = "A=2N7000;B=ALD1106;C=JFET;hold=0V"   # free text written into every row (no commas); edit per run
PIN_PWM_WBL = 15
WBL_GPIO = None              # e.g. 14: drive WBL from a plain GPIO (0 / 3.3 V only) for 'fast' runs; None = PWM DAC
OPTO_PINS = {"A": 10, "B": 11, "C": 12}
RELAY_PIN = 13
CELL_C_IS_RELAY = False      # True if cell C uses the reed relay instead of the JFET
PIN_READ_EN = 9
ADC_PINS = {"A": 26, "B": 27, "C": 28}
HEATER_PIN = 18              # E1 section 6.5 heater circuit; GP18 is free in E2
HEATER_SETPOINT_C = None     # e.g. 45.0 for the warm run; None = heater unused
PREHEAT_HOLD_S = 1800        # hold the set point this long before the first write
PREHEAT_TIMEOUT_S = 7200     # give up (heater off, error) if the set point is not reached in this time
PWM_FREQ = 100000            # ripple after 10 kOhm/1 uF ~ 3.3/(4 f RC) = 0.8 mV
WBL_SETTLE_MS = 80           # 8 tau of the 10 ms filter
WRITE_MS = 50                # switch-on time (reed relays need ~1 ms to close; generous)
V_WRITE = 3.3                # storage-node target for "retention" (needs WWL boost to +9 V for MOSFETs)
PARK_V = 0.0                 # WBL voltage during hold (0 V keeps a 2N7000's body diode reverse-biased)
LOG_S = 1.0
DURATION_S = 1800
FAST_S = 2.0                 # "fast" mode: decay capture length after the park (s)
FAST_AVG = 4                 # ADC samples averaged per point in "fast" mode
FAST_MAX = 2000              # points kept in RAM (about 10 bytes each)
FAST_PRE_MS = 5              # "fast": sampling time with the switches ON
KICK_MS = 3                  # "fast": sampling time after switch-off with WBL still at V_WRITE
N_READS = 10000
MLC_CELL = "C"
MLC_TARGETS = (0.15, 0.45, 0.75, 1.05)   # follower-output targets (V) for levels 00/01/10/11 (bench_calcs E2.9)
MLC_TOL = 0.010
MLC_TRIALS = 5
MLC_HOLD_S = 300
N_AVG = 64
LOGFILE = None

HDR = ["exp", "mode", "t_s", "temp_c", "label", "cell", "v_out"]
NAMES = ("A", "B", "C")


class Cells:
    def __init__(self):
        if WBL_GPIO is None:
            self.pwm = PWM(Pin(PIN_PWM_WBL))
            self.pwm.freq(PWM_FREQ)
            self.wbl_pin = None
        else:
            self.pwm = None
            self.wbl_pin = Pin(WBL_GPIO, Pin.OUT, value=0)
        self.opto = {k: Pin(p, Pin.OUT, value=1) for k, p in OPTO_PINS.items()}   # start in HOLD
        self.relay = Pin(RELAY_PIN, Pin.OUT, value=0)                             # start open
        self.read_en = Pin(PIN_READ_EN, Pin.OUT, value=1)
        self.adc = {k: ADC(p) for k, p in ADC_PINS.items()}
        self.set_wbl(PARK_V)

    def set_wbl_now(self, v):
        """Change WBL without waiting. The PWM DAC then settles with its 10 ms time constant."""
        v = max(0.0, min(3.3, v))
        if self.pwm is not None:
            self.pwm.duty_u16(int(v / 3.3 * 65535))
        else:
            self.wbl_pin.value(1 if v >= 1.65 else 0)

    def set_wbl(self, v):
        self.set_wbl_now(v)
        time.sleep_ms(WBL_SETTLE_MS if self.pwm is not None else 1)

    def switch(self, cell, on):
        if cell == "C" and CELL_C_IS_RELAY:
            self.relay.value(1 if on else 0)
        else:
            self.opto[cell].value(0 if on else 1)      # LED off -> WWL pulled to V_ON -> switch conducts

    def write(self, cells, v):
        """Write v, then measure the two turn-off steps per cell. Returns (before, after, park) dicts of Vout:
        before = switch on; after = 2 ms after switch-off with WBL still at v (gate kick only, almost no
        voltage across the switch); park = after WBL has parked (adds the drain-source coupling step)."""
        self.set_wbl(v)
        for c in cells:
            self.switch(c, True)
        time.sleep_ms(WRITE_MS)
        before = {c: self.vout(c, 16) for c in cells}
        for c in cells:
            self.switch(c, False)
        time.sleep_ms(2)
        after = {c: self.vout(c, 16) for c in cells}
        time.sleep_ms(3)
        self.set_wbl(PARK_V)
        park = {c: self.vout(c, 16) for c in cells}
        return before, after, park

    def vout(self, cell, n=N_AVG):
        return adc_volts(self.adc[cell], n)


def log_kicks(log, kicks, temp):
    for mode, d in zip(("kick_before", "kick_after", "kick_park"), kicks):
        for c in sorted(d):
            log.row(["E2", mode, 0, temp, LABEL, c, d[c]])


def mode_transfer(cells, clk):
    log = CsvLog(["exp", "mode", "label", "v_wbl", "cell", "v_out"], LOGFILE)
    for c in NAMES:
        cells.switch(c, True)
    v = 0.0
    while v <= 3.3001:
        cells.set_wbl(v)
        time.sleep_ms(20)
        for c in NAMES:
            log.row(["E2", "transfer", LABEL, v, c, cells.vout(c)])
        v += 0.05
    for c in NAMES:
        cells.switch(c, False)
    cells.set_wbl(PARK_V)


def mode_retention(cells, clk, thermo, heater=None):
    log = CsvLog(HDR, LOGFILE)
    log.note("retention: write %.2f V to A,B,C together, then hold with WBL parked at %.2f V" % (V_WRITE, PARK_V))
    kicks = cells.write(NAMES, V_WRITE)
    t0 = clk.s()
    log_kicks(log, kicks, thermo.read_c())
    n = 0
    while clk.s() - t0 < DURATION_S:
        temp = thermo.read_c() if n % 30 == 0 else ""
        t = clk.s() - t0
        for c in NAMES:
            log.row(["E2", "retention", t, temp, LABEL, c, cells.vout(c)])
        n += 1
        hold_s(LOG_S, heater)


def mode_fast(cells, clk, thermo):
    """Raw ADC codes into preallocated arrays (floats would fill the heap), then print.
    Run gc.mem_free() at the REPL the first time if you raise FAST_MAX."""
    log = CsvLog(HDR, LOGFILE)
    temp = thermo.read_c()
    adcs = [cells.adc[c] for c in NAMES]
    ts = array.array("i", bytearray(4 * FAST_MAX))        # microseconds since t0 (bytearray = raw zero bytes)
    raw = array.array("H", bytearray(2 * 3 * FAST_MAX))   # mean ADC code per cell
    avg = FAST_AVG

    def sample(k, t):
        ts[k] = t
        for j in range(3):
            a = adcs[j]
            s = 0
            for _ in range(avg):
                s += a.read_u16()
            raw[3 * k + j] = s // avg

    cells.set_wbl(V_WRITE)
    for c in NAMES:
        cells.switch(c, True)
    time.sleep_ms(WRITE_MS)
    k = 0
    t0 = time.ticks_us()
    while k < FAST_MAX:                                    # 1) switches ON: the written level
        t = time.ticks_diff(time.ticks_us(), t0)
        if t >= FAST_PRE_MS * 1000:
            break
        sample(k, t)
        k += 1
    i_off = k
    for c in NAMES:
        cells.switch(c, False)
    t_off = time.ticks_diff(time.ticks_us(), t0)
    while k < FAST_MAX:                                    # 2) switches OFF, WBL still at V_WRITE: gate kick
        t = time.ticks_diff(time.ticks_us(), t0)
        if t >= t_off + KICK_MS * 1000:
            break
        sample(k, t)
        k += 1
    i_park = k
    cells.set_wbl_now(PARK_V)                              # 3) park WBL now, no settling delay
    t_park = time.ticks_diff(time.ticks_us(), t0)
    t_next = t_park
    while k < FAST_MAX:
        t = time.ticks_diff(time.ticks_us(), t0)
        if t - t_park > FAST_S * 1e6:
            break
        if t < t_next:
            continue
        sample(k, t)
        k += 1
        t_next = t + ((t - t_park) >> 8)                   # next point ~0.4% later: fastest first, then log-spaced
    log.note("fast: %d points; switches off at t = %.6f s, WBL parked at t = 0 (PWM DAC tau 10 ms)"
             % (k, (t_off - t_park) / 1e6))
    scale = ADC_FULL_SCALE_V / 65535
    for i in range(k):
        mode = "kick_before" if i < i_off else ("kick_after" if i < i_park else "retention")
        t_rel = (ts[i] - t_park) / 1e6
        for j in range(3):
            log.row(["E2", mode, t_rel, temp, LABEL + ";fast", NAMES[j], raw[3 * i + j] * scale])


def mode_readmany(cells, clk):
    log = CsvLog(["exp", "mode", "label", "read_n", "cell", "v_out"], LOGFILE)
    cells.write(NAMES, V_WRITE)
    for n in range(N_READS + 1):
        cells.read_en.value(1)
        time.sleep_us(200)
        if n % 500 == 0:
            for c in NAMES:
                log.row(["E2", "readmany", LABEL, n, c, cells.vout(c, 16)])
        cells.read_en.value(0)
        time.sleep_us(200)
    cells.read_en.value(1)


def write_verify(cells, cell, target):
    """NAND-style write-verify: adjust WBL until the follower output sits within MLC_TOL of target."""
    v = target + 2.1                      # first guess: Vsn ~ Vout + Vth (2N7000 typ 2.1 V)
    vo = 0.0
    for _ in range(12):
        cells.write((cell,), v)
        time.sleep_ms(20)
        vo = cells.vout(cell)
        err = target - vo
        if abs(err) <= MLC_TOL:
            break
        v += 0.9 * err                    # follower gain ~1
    return v, vo


def mode_mlc(cells, clk, heater=None):
    log = CsvLog(["exp", "mode", "label", "t_s", "trial", "level", "target_v", "v_out"], LOGFILE)
    for trial in range(MLC_TRIALS):
        for level, target in enumerate(MLC_TARGETS):
            write_verify(cells, MLC_CELL, target)
            t0 = clk.s()
            while clk.s() - t0 < MLC_HOLD_S:
                log.row(["E2", "mlc", LABEL, clk.s() - t0, trial, level, target, cells.vout(MLC_CELL)])
                hold_s(LOG_S, heater)


HEATER_MODES = ("retention", "mlc")


def main():
    low_ripple_supply()
    Pin(HEATER_PIN, Pin.OUT, value=0)            # heater off unless a heater mode takes control below
    cells = Cells()
    thermo = Thermo(22)
    heater = None
    clk = Clock()
    print("# E2 gain cells, MODE=%s, LABEL=%s. REFERENCE CODE - UNTESTED ON HARDWARE" % (MODE, LABEL))
    try:
        if HEATER_SETPOINT_C:
            if MODE in HEATER_MODES:
                heater = Heater(HEATER_PIN, thermo, HEATER_SETPOINT_C)
                start_watchdog()
                print("# heater on GP18, set point %.1f C; preheat, then hold %d s" % (heater.setpoint, PREHEAT_HOLD_S))
                preheat(heater, PREHEAT_HOLD_S, PREHEAT_TIMEOUT_S)
                clk = Clock()
            else:
                print("# HEATER_SETPOINT_C ignored: the heater runs only in modes %s" % (HEATER_MODES,))
        if MODE == "transfer":
            mode_transfer(cells, clk)
        elif MODE == "retention":
            mode_retention(cells, clk, thermo, heater)
        elif MODE == "fast":
            mode_fast(cells, clk, thermo)
        elif MODE == "readmany":
            mode_readmany(cells, clk)
        elif MODE == "mlc":
            mode_mlc(cells, clk, heater)
        else:
            print("# unknown MODE")
    finally:
        if heater:
            heater.off()
        for c in NAMES:
            cells.switch(c, False)
        cells.set_wbl(0.0)


if __name__ == "__main__":
    main()
