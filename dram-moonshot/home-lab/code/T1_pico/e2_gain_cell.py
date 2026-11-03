# e2_gain_cell.py -- E2 "A gain cell without a capacitor": three discrete 2T0C cells side by side.
# REFERENCE CODE - UNTESTED ON HARDWARE. MicroPython, Raspberry Pi Pico (RP2040) or Pico 2 (RP2350).
# Needs t1_common.py on the Pico. Wiring: home-lab/E2_gain_cell_no_capacitor.md, "Circuit".
#
# Each cell: WRITE switch (WBL -> storage node SN) + READ transistor (2N7000) whose gate IS the SN.
# Read = source follower: drain on READ_EN, source -> 47 kOhm -> GND; the source goes to an ADC pin.
#
# Pin map:
#   GP15 PWM -> 10 kOhm -> WBL node with 1 uF film to GND (a filtered DAC; tau = 10 ms)
#   GP10 -> opto LED (cell A write switch, e.g. 2N7000)   LED ON = switch OFF (hold)
#   GP11 -> opto LED (cell B write switch, e.g. ALD1106)  LED ON = switch OFF (hold)
#   GP12 -> opto LED (cell C write switch, JFET)           LED ON = switch OFF (hold)
#   GP13 -> reed-relay driver transistor (cell C alternative): HIGH = relay closed (write)
#   GP9  -> READ_EN: drains of the three read transistors (3.3 V = reading)
#   GP26/27/28 (ADC0/1/2) <- follower outputs of cells A/B/C
#   GP22 <- DS18B20
#
# Modes:
#   "transfer"  calibration: all switches on, sweep WBL 0..3.3 V, log Vout per cell (maps Vout <-> Vsn)
#   "retention" write V_WRITE into all cells at once, hold, log Vout of each cell every LOG_S seconds
#   "readmany"  write, hold, toggle READ_EN N_READS times while reading; non-destructive read test
#   "fast"      like "retention" but samples as fast as possible for FAST_S seconds (leaky switches lose
#               100 mV in milliseconds: a 1 s log interval would miss the whole decay)
#   "mlc"       2 bits/cell on cell MLC_CELL: write-verify 4 levels, hold, log (error rates offline)
# Output: CSV over USB serial (mpremote run e2_gain_cell.py > e2_retention.csv)

import time
from machine import Pin, PWM, ADC
from t1_common import adc_volts, CsvLog, Thermo, Clock, low_ripple_supply

MODE = "retention"
LABEL = "A=2N7000;B=ALD1106;C=JFET;hold=0V"   # free text written into every row (no commas); edit per run
PIN_PWM_WBL = 15
OPTO_PINS = {"A": 10, "B": 11, "C": 12}
RELAY_PIN = 13
CELL_C_IS_RELAY = False      # True if cell C uses the reed relay instead of the JFET
PIN_READ_EN = 9
ADC_PINS = {"A": 26, "B": 27, "C": 28}
PWM_FREQ = 100000            # ripple after 10 kOhm/1 uF ~ 3.3/(4 f RC) = 0.8 mV
WBL_SETTLE_MS = 80           # 8 tau of the 10 ms filter
WRITE_MS = 50                # switch-on time (reed relays need ~1 ms to close; generous)
V_WRITE = 3.3                # storage-node target for "retention" (needs WWL boost to +9 V for MOSFETs)
PARK_V = 0.0                 # WBL voltage during hold (0 V keeps a 2N7000's body diode reverse-biased)
LOG_S = 1.0
DURATION_S = 1800
FAST_S = 2.0                 # "fast" mode capture length
FAST_AVG = 4                 # ADC samples averaged per point in "fast" mode
FAST_MAX = 3000              # points kept in RAM before printing
N_READS = 10000
MLC_CELL = "C"
MLC_TARGETS = (0.15, 0.45, 0.75, 1.05)   # follower-output targets (V) for levels 00/01/10/11 (bench_calcs E2.9)
MLC_TOL = 0.010
MLC_TRIALS = 5
MLC_HOLD_S = 300
N_AVG = 64
LOGFILE = None


class Cells:
    def __init__(self):
        self.pwm = PWM(Pin(PIN_PWM_WBL))
        self.pwm.freq(PWM_FREQ)
        self.opto = {k: Pin(p, Pin.OUT, value=1) for k, p in OPTO_PINS.items()}   # start in HOLD
        self.relay = Pin(RELAY_PIN, Pin.OUT, value=0)                             # start open
        self.read_en = Pin(PIN_READ_EN, Pin.OUT, value=1)
        self.adc = {k: ADC(p) for k, p in ADC_PINS.items()}
        self.set_wbl(PARK_V)

    def set_wbl(self, v):
        v = max(0.0, min(3.3, v))
        self.pwm.duty_u16(int(v / 3.3 * 65535))
        time.sleep_ms(WBL_SETTLE_MS)

    def switch(self, cell, on):
        if cell == "C" and CELL_C_IS_RELAY:
            self.relay.value(1 if on else 0)
        else:
            self.opto[cell].value(0 if on else 1)      # LED off -> WWL pulled to V_ON -> switch conducts

    def write(self, cells, v):
        self.set_wbl(v)
        for c in cells:
            self.switch(c, True)
        time.sleep_ms(WRITE_MS)
        for c in cells:
            self.switch(c, False)
        time.sleep_ms(5)
        self.set_wbl(PARK_V)

    def vout(self, cell, n=N_AVG):
        return adc_volts(self.adc[cell], n)


def mode_transfer(cells, clk):
    log = CsvLog(["exp", "mode", "label", "v_wbl", "cell", "v_out"], LOGFILE)
    for c in ("A", "B", "C"):
        cells.switch(c, True)
    v = 0.0
    while v <= 3.3001:
        cells.set_wbl(v)
        time.sleep_ms(20)
        for c in ("A", "B", "C"):
            log.row(["E2", "transfer", LABEL, v, c, cells.vout(c)])
        v += 0.05
    for c in ("A", "B", "C"):
        cells.switch(c, False)
    cells.set_wbl(PARK_V)


def mode_retention(cells, clk, thermo):
    log = CsvLog(["exp", "mode", "t_s", "temp_c", "label", "cell", "v_out"], LOGFILE)
    log.note("retention: write %.2f V to A,B,C together, then hold with WBL parked at %.2f V" % (V_WRITE, PARK_V))
    cells.write(("A", "B", "C"), V_WRITE)
    t0 = clk.s()
    n = 0
    while clk.s() - t0 < DURATION_S:
        temp = thermo.read_c() if n % 30 == 0 else ""
        t = clk.s() - t0
        for c in ("A", "B", "C"):
            log.row(["E2", "retention", t, temp, LABEL, c, cells.vout(c)])
        n += 1
        time.sleep_ms(int(LOG_S * 1000))


def mode_fast(cells, clk, thermo):
    """Capture into RAM first (printing is slow), then print. Typical rate: a few hundred points/s."""
    log = CsvLog(["exp", "mode", "t_s", "temp_c", "label", "cell", "v_out"], LOGFILE)
    temp = thermo.read_c()
    buf = []
    cells.write(("A", "B", "C"), V_WRITE)
    t0 = time.ticks_us()
    while len(buf) < FAST_MAX:
        t = time.ticks_diff(time.ticks_us(), t0) / 1e6
        if t > FAST_S:
            break
        buf.append((t, cells.vout("A", FAST_AVG), cells.vout("B", FAST_AVG), cells.vout("C", FAST_AVG)))
    for t, va, vb, vc in buf:
        log.row(["E2", "retention", t, temp, LABEL + ";fast", "A", va])
        log.row(["E2", "retention", t, temp, LABEL + ";fast", "B", vb])
        log.row(["E2", "retention", t, temp, LABEL + ";fast", "C", vc])


def mode_readmany(cells, clk):
    log = CsvLog(["exp", "mode", "label", "read_n", "cell", "v_out"], LOGFILE)
    cells.write(("A", "B", "C"), V_WRITE)
    for n in range(N_READS + 1):
        cells.read_en.value(1)
        time.sleep_us(200)
        if n % 500 == 0:
            for c in ("A", "B", "C"):
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


def mode_mlc(cells, clk):
    log = CsvLog(["exp", "mode", "label", "t_s", "trial", "level", "target_v", "v_out"], LOGFILE)
    for trial in range(MLC_TRIALS):
        for level, target in enumerate(MLC_TARGETS):
            write_verify(cells, MLC_CELL, target)
            t0 = clk.s()
            while clk.s() - t0 < MLC_HOLD_S:
                log.row(["E2", "mlc", LABEL, clk.s() - t0, trial, level, target, cells.vout(MLC_CELL)])
                time.sleep_ms(int(LOG_S * 1000))


def main():
    low_ripple_supply()
    cells = Cells()
    thermo = Thermo(22)
    clk = Clock()
    print("# E2 gain cells, MODE=%s, LABEL=%s. REFERENCE CODE - UNTESTED ON HARDWARE" % (MODE, LABEL))
    try:
        if MODE == "transfer":
            mode_transfer(cells, clk)
        elif MODE == "retention":
            mode_retention(cells, clk, thermo)
        elif MODE == "fast":
            mode_fast(cells, clk, thermo)
        elif MODE == "readmany":
            mode_readmany(cells, clk)
        elif MODE == "mlc":
            mode_mlc(cells, clk)
    finally:
        for c in ("A", "B", "C"):
            cells.switch(c, False)
        cells.set_wbl(0.0)


if __name__ == "__main__":
    main()
