# e1_array_4x4.py -- E1 "A bit on the bench", part B: a 16-bit (4 x 4) discrete DRAM array.
# REFERENCE CODE - UNTESTED ON HARDWARE. MicroPython, Raspberry Pi Pico (RP2040) or Pico 2 (RP2350).
# Needs t1_common.py and hamming16.py on the Pico. Wiring: home-lab/E1_bit_on_the_bench.md, "Circuit B".
#
# Pin map:
#   GP2..GP5   -> CD40109B inputs A..D -> wordlines WL0..WL3 (one ALD1106 package = one row of 4 cells)
#   GP6/GP7    -> 10 kOhm each -> BL0      GP8/GP9   -> BL1
#   GP10/GP11  -> 10 kOhm each -> BL2      GP12/GP13 -> BL3
#   GP14..GP17 <- MCP6544 comparator outputs SA0..SA3 (+in = BLn, -in = shared VREF 1.65 V)
#   GP18       -> optional heater MOSFET gate via 220 Ohm, 100 kOhm gate pull-down (guide section 6.5). Held
#                 LOW unless HEATER_SETPOINT_C is set AND MODE is "retmap" or "ecc".
#   GP22       <- DS18B20
#   GP28 (ADC2)<- VREF monitor
#
# Modes:
#   "pattern"  write checkerboard / inverse / all-1 / all-0, read back, count errors
#   "refresh"  random data, refresh every T_REF_S for RUN_S; compare with a no-refresh copy at the end
#   "retmap"   write all 1s, wait t, read all 16 without restore -> per-cell retention. A coarse pass
#              (4 waits per decade, 1.78x steps) finds where cells fail; a fine pass (5% steps) then
#              resolves each cell's retention well enough to see a 1.1-1.4x ECC gain.
#   "ecc"      store an 11-bit word as a Hamming(16,11) codeword, wait t, read, correct -> raw vs corrected,
#              with the same coarse + fine passes.
# With HEATER_SETPOINT_C set, the script first preheats and holds the set point for PREHEAT_HOLD_S, and it
# starts the hardware watchdog. To stop a heated run: unplug the 12 V adapter first, then press Thonny's
# Stop (Ctrl-C in an mpremote terminal does not stop the Pico).
# Output: CSV over USB serial (mpremote run e1_array_4x4.py > e1_retmap.csv); no mode asks questions.

import time
import random
from machine import Pin, ADC
from t1_common import (tristate, drive, CsvLog, Thermo, Heater, Clock, low_ripple_supply, log_schedule,
                       hold_s, preheat, start_watchdog)
import hamming16

MODE = "retmap"
WL_PINS = (2, 3, 4, 5)
BL_A_PINS = (6, 8, 10, 12)
BL_B_PINS = (7, 9, 11, 13)
SA_PINS = (14, 15, 16, 17)
HEATER_PIN = 18
HEATER_SETPOINT_C = None     # e.g. 45.0 to hold the warm-box temperature; None = heater unused
PREHEAT_HOLD_S = 1800        # hold the set point this long before the first write
PREHEAT_TIMEOUT_S = 7200     # give up (heater off, error) if the set point is not reached in this time
PRECHARGE_MS = 2             # 5 kOhm x (4.7 nF + 1 nF) = 28.5 us tau; 2 ms is ~70 tau
WRITE_MS = 2
SHARE_MS = 1
T_REF_S = 5.0                # refresh interval for "refresh" mode
RUN_S = 3600                 # duration of "refresh" mode
RET_MIN_S, RET_MAX_S = 1.0, 3600.0
FINE_STEP = 1.05             # fine pass: each wait 5% longer than the one before
FINE_STOP_CELLS = 16         # retmap fine pass stops once this many cells fail (2 is enough for the ECC gain)
ECC_DATA = 0x7FF             # 11 data bits; all ones -> the codeword has many stored 1s (the leaky state)
LOGFILE = None


class Array4x4:
    def __init__(self):
        self.wl = [Pin(p, Pin.OUT, value=0) for p in WL_PINS]
        self.a = [Pin(p, Pin.OUT, value=0) for p in BL_A_PINS]
        self.b = [Pin(p, Pin.OUT, value=0) for p in BL_B_PINS]
        self.sa = [Pin(p, Pin.IN, None) for p in SA_PINS]
        self.adc_ref = ADC(28)
        self.park()

    def bl(self, col, level):
        a, b = self.a[col], self.b[col]
        if level == 1:
            drive(a, 1); drive(b, 1)
        elif level == 0:
            drive(a, 0); drive(b, 0)
        elif level == "half":
            drive(a, 1); drive(b, 0)
        else:
            tristate(a); tristate(b)

    def all_bl(self, level):
        for c in range(4):
            self.bl(c, level)

    def park(self):
        self.all_bl("half")

    def write_row(self, r, bits):
        for c in range(4):
            self.bl(c, bits[c])
        time.sleep_ms(PRECHARGE_MS)
        self.wl[r].value(1)
        time.sleep_ms(WRITE_MS)
        self.wl[r].value(0)
        self.park()

    def read_row(self, r, restore=True):
        self.all_bl("half")
        time.sleep_ms(PRECHARGE_MS)
        self.all_bl("float")
        time.sleep_us(50)
        self.wl[r].value(1)
        time.sleep_ms(SHARE_MS)
        bits = [self.sa[c].value() for c in range(4)]
        if restore:
            for c in range(4):
                self.bl(c, bits[c])
            time.sleep_ms(WRITE_MS)
        self.wl[r].value(0)
        self.park()
        return bits

    def write_all(self, bits16):
        for r in range(4):
            self.write_row(r, bits16[4 * r:4 * r + 4])

    def read_all(self, restore=True):
        out = []
        for r in range(4):
            out += self.read_row(r, restore)
        return out

    def refresh(self):
        for r in range(4):
            self.read_row(r, restore=True)


def mode_pattern(arr, clk, thermo, heater=None):
    log = CsvLog(["exp", "mode", "t_s", "temp_c", "pattern", "errors"], LOGFILE)
    checker = [((i // 4) + i) % 2 for i in range(16)]
    pats = (("checker", checker), ("inverse", [1 - x for x in checker]), ("ones", [1] * 16), ("zeros", [0] * 16))
    for name, bits in pats:
        arr.write_all(bits)
        got = arr.read_all(True)
        log.row(["E1B", "pattern", clk.s(), thermo.read_c(), name, sum(1 for i in range(16) if got[i] != bits[i])])


def mode_refresh(arr, clk, thermo, heater=None):
    log = CsvLog(["exp", "mode", "t_s", "temp_c", "t_ref_s", "errors"], LOGFILE)
    data = [random.getrandbits(1) for _ in range(16)]
    arr.write_all(data)
    t0 = clk.s()
    next_check = 60.0
    while clk.s() - t0 < RUN_S:
        hold_s(T_REF_S)
        arr.refresh()
        if clk.s() - t0 >= next_check:
            got = arr.read_all(True)
            log.row(["E1B", "refresh", clk.s(), thermo.read_c(), T_REF_S,
                     sum(1 for i in range(16) if got[i] != data[i])])
            next_check += 60.0
    log.note("now the same data WITHOUT refresh for the same time")
    arr.write_all(data)
    hold_s(RUN_S)
    got = arr.read_all(False)
    log.row(["E1B", "no_refresh", clk.s(), thermo.read_c(), 0, sum(1 for i in range(16) if got[i] != data[i])])


def retmap_once(arr, log, clk, thermo, heater, wait):
    """Write all 1s, wait, read all 16 without restore, log one row per cell. Returns the number of failed cells."""
    arr.write_all([1] * 16)
    hold_s(wait, heater)
    got = arr.read_all(False)
    temp = thermo.read_c()
    for i in range(16):
        log.row(["E1B", "retmap", clk.s(), temp, wait, i // 4, i % 4, 1, got[i]])
    return 16 - sum(got)


def mode_retmap(arr, clk, thermo, heater):
    log = CsvLog(["exp", "mode", "t_s", "temp_c", "wait_s", "row", "col", "stored_bit", "read_bit"], LOGFILE)
    first_fail = None
    all_fail = None
    for wait in log_schedule(RET_MIN_S, RET_MAX_S, 4):
        nfail = retmap_once(arr, log, clk, thermo, heater, wait)
        if nfail and first_fail is None:
            first_fail = wait
        if nfail == 16:
            all_fail = wait
            log.note("coarse pass: all cells lost their 1s at %g s" % wait)
            break
    if first_fail is None:
        log.note("no cell failed up to RET_MAX_S = %g s: raise RET_MAX_S and repeat" % RET_MAX_S)
        return
    # Fine pass: 5% steps from just below the first failure. A 1.78x step cannot resolve a 1.1-1.4x gap.
    w = first_fail / 10 ** 0.25
    w_end = min(RET_MAX_S, all_fail * 1.2) if all_fail else RET_MAX_S
    log.note("fine pass: %.0f%% steps from %.4g s until %d cells fail (or %.4g s)"
             % ((FINE_STEP - 1) * 100, w * FINE_STEP, FINE_STOP_CELLS, w_end))
    while True:
        w = round(w * FINE_STEP, 3)
        if w > w_end:
            break
        if retmap_once(arr, log, clk, thermo, heater, w) >= FINE_STOP_CELLS:
            break


def ecc_once(arr, log, clk, thermo, heater, cw, wait):
    """Store the codeword, wait, read without restore, decode, log. Returns (raw_errors, uncorrectable)."""
    arr.write_all(cw)
    hold_s(wait, heater)
    got = arr.read_all(False)
    data, status, pos = hamming16.decode(got)
    raw = sum(1 for i in range(16) if got[i] != cw[i])
    ok = 1 if data == ECC_DATA else 0
    log.row(["E1B", "ecc", clk.s(), thermo.read_c(), wait, raw, status, pos, ok])
    return raw, (status == hamming16.DETECTED or not ok)


def mode_ecc(arr, clk, thermo, heater):
    log = CsvLog(["exp", "mode", "t_s", "temp_c", "wait_s", "raw_errors", "status", "corrected_pos", "data_ok"],
                 LOGFILE)
    cw = hamming16.encode(ECC_DATA)
    log.note("codeword bits (cell 0..15): " + "".join(str(b) for b in cw))
    first_raw = None
    first_bad = None
    for wait in log_schedule(RET_MIN_S, RET_MAX_S, 4):
        raw, bad = ecc_once(arr, log, clk, thermo, heater, cw, wait)
        if raw and first_raw is None:
            first_raw = wait
        if bad:
            first_bad = wait
            break
    if first_raw is None:
        log.note("no raw error up to RET_MAX_S = %g s: raise RET_MAX_S and repeat" % RET_MAX_S)
        return
    # Fine pass: 5% steps from just below the first raw error until the decoder can no longer fix the word.
    w = first_raw / 10 ** 0.25
    w_end = min(RET_MAX_S, first_bad * 1.2) if first_bad else RET_MAX_S
    log.note("fine pass: %.0f%% steps from %.4g s until the word is uncorrectable (or %.4g s)"
             % ((FINE_STEP - 1) * 100, w * FINE_STEP, w_end))
    while True:
        w = round(w * FINE_STEP, 3)
        if w > w_end:
            break
        raw, bad = ecc_once(arr, log, clk, thermo, heater, cw, w)
        if bad:
            break


HEATER_MODES = ("retmap", "ecc")


def main():
    low_ripple_supply()
    Pin(HEATER_PIN, Pin.OUT, value=0)            # heater off unless a heater mode takes control below
    arr = Array4x4()
    thermo = Thermo(22)
    heater = None
    clk = Clock()
    print("# E1B 4x4 array, MODE=%s. REFERENCE CODE - UNTESTED ON HARDWARE" % MODE)
    try:
        if HEATER_SETPOINT_C:
            if MODE in HEATER_MODES:
                heater = Heater(HEATER_PIN, thermo, HEATER_SETPOINT_C)
                start_watchdog()
                print("# heater on GP18, set point %.1f C; preheat, then hold %d s" % (heater.setpoint, PREHEAT_HOLD_S))
                preheat(heater, PREHEAT_HOLD_S, PREHEAT_TIMEOUT_S)
                clk = Clock()                    # time zero = first write after the preheat
            else:
                print("# HEATER_SETPOINT_C ignored: the heater runs only in modes %s" % (HEATER_MODES,))
        if MODE == "pattern":
            mode_pattern(arr, clk, thermo)
        elif MODE == "refresh":
            mode_refresh(arr, clk, thermo)
        elif MODE == "retmap":
            mode_retmap(arr, clk, thermo, heater)
        elif MODE == "ecc":
            mode_ecc(arr, clk, thermo, heater)
        else:
            print("# unknown MODE")
    finally:
        if heater:
            heater.off()
        for w in arr.wl:
            w.value(0)
        arr.park()


if __name__ == "__main__":
    main()
