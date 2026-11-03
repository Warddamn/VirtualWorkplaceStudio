# e1_single_cell.py -- E1 "A bit on the bench", part A: one discrete 1T1C DRAM cell.
# REFERENCE CODE - UNTESTED ON HARDWARE. MicroPython, Raspberry Pi Pico (RP2040) or Pico 2 (RP2350).
# Needs t1_common.py on the Pico. Wiring: see home-lab/E1_bit_on_the_bench.md, section "Circuit A".
#
# Pin map (edit below if you wire differently):
#   GP2  -> CD40109B input A; its output drives the access-transistor gate = WORDLINE (WL)
#   GP3  -> 10 kOhm -> BITLINE (BL)     } both high = write 1, both low = write 0,
#   GP4  -> 10 kOhm -> BITLINE (BL)     } one high + one low = precharge to V/2, both inputs = float
#   GP5  <- comparator output (+in = BL, -in = VREF): the SENSE AMP
#   GP26 (ADC0) <- LMC6482 follower of BL
#   GP27 (ADC1) <- LMC6482 follower of the storage node (optional "peek" probe)
#   GP28 (ADC2) <- VREF (1.65 V divider with 1 uF), to calibrate the comparator threshold
#   GP22 <- DS18B20 data (4.7 kOhm pull-up to 3V3)
#
# Modes (set MODE below, or call the functions from the REPL):
#   "share"        charge-sharing: dV vs Cbl/Cs. You swap Cbl by hand; the script asks for its value.
#   "destructive"  read the same '1' four times WITHOUT restore, then restore and read again.
#   "retention"    DRAM-style test: write 1, wait t (log-spaced), read; repeat. Logs dV and the bit.
#   "peek"         write 1, then log the storage-node follower every second (decay curve -> leakage).
# Output: CSV on USB serial. Capture on a PC with:  mpremote run e1_single_cell.py > e1_share.csv

import time
from machine import Pin, ADC
from t1_common import (adc_volts, tristate, drive, CsvLog, Thermo, Clock, low_ripple_supply, log_schedule)

# ---------------- configuration ----------------
MODE = "share"
PIN_WL, PIN_BL_A, PIN_BL_B, PIN_SA = 2, 3, 4, 5
CS_NF = 1.0                  # storage capacitor you fitted (nF)
PARK = "half"                # where the bitline rests between operations: "half" (V/2) or "zero"
PRECHARGE_MS = 5             # >= 7 tau of 5 kOhm x (Cbl + Cs); 5 ms covers Cbl up to ~100 nF
WRITE_MS = 5                 # wordline-on time for a write / restore
SHARE_MS = 1                 # wordline-on time before sensing (charge sharing settles in ~1 us)
N_AVG = 64                   # ADC samples per voltage reading
REPEATS = 10                 # reads per stored value in "share" mode
RET_MIN_S, RET_MAX_S = 1.0, 1800.0   # retention schedule (seconds)
PEEK_S = 3600                # duration of a "peek" decay log (seconds)
LOGFILE = None               # e.g. "e1_log.csv" to also write to the Pico's flash


class Cell:
    def __init__(self):
        self.wl = Pin(PIN_WL, Pin.OUT, value=0)
        self.a = Pin(PIN_BL_A, Pin.OUT, value=0)
        self.b = Pin(PIN_BL_B, Pin.OUT, value=0)
        self.sa = Pin(PIN_SA, Pin.IN, None)
        self.adc_bl = ADC(26)
        self.adc_sn = ADC(27)
        self.adc_ref = ADC(28)
        self.park()

    # --- bitline drivers
    def bl(self, level):
        if level == "hi":
            drive(self.a, 1); drive(self.b, 1)
        elif level == "lo":
            drive(self.a, 0); drive(self.b, 0)
        elif level == "half":
            drive(self.a, 1); drive(self.b, 0)
        else:  # "float"
            tristate(self.a); tristate(self.b)

    def park(self):
        self.bl("half" if PARK == "half" else "lo")

    # --- cell operations
    def write(self, bit):
        self.bl("hi" if bit else "lo")
        time.sleep_ms(PRECHARGE_MS)
        self.wl.value(1)
        time.sleep_ms(WRITE_MS)
        self.wl.value(0)
        time.sleep_ms(1)
        self.park()

    def read(self, restore=True):
        """Precharge to V/2, float, open the wordline, sense, optionally write back. Returns a dict."""
        self.bl("half")
        time.sleep_ms(PRECHARGE_MS)
        self.bl("float")
        time.sleep_us(50)
        v_pre = adc_volts(self.adc_bl, N_AVG)
        self.wl.value(1)
        time.sleep_ms(SHARE_MS)
        sa_bit = self.sa.value()
        v_after = adc_volts(self.adc_bl, N_AVG)
        v_ref = adc_volts(self.adc_ref, 16)
        if restore:
            self.bl("hi" if sa_bit else "lo")          # sense amp drives the bitline to full rail
            time.sleep_ms(WRITE_MS)
        self.wl.value(0)
        time.sleep_ms(1)
        self.park()
        return {"v_pre": v_pre, "v_after": v_after, "dv": v_after - v_pre, "sa_bit": sa_bit,
                "adc_bit": 1 if v_after > v_ref else 0, "v_ref": v_ref}

    def peek(self):
        return adc_volts(self.adc_sn, N_AVG)


HEADER = ["exp", "mode", "t_s", "temp_c", "cs_nF", "cbl_nF", "wait_s", "read_idx", "stored_bit",
          "v_pre", "v_after", "dv", "sa_bit", "adc_bit", "v_ref"]


def row(log, mode, clk, temp, cbl, wait, idx, bit, r):
    log.row(["E1A", mode, clk.s(), temp, CS_NF, cbl, wait, idx, bit, r["v_pre"], r["v_after"], r["dv"],
             r["sa_bit"], r["adc_bit"], r["v_ref"]])


def mode_share(cell, log, clk, thermo):
    log.note("charge sharing: predicted dV = (V - V/2) * Cs / (Cs + Cbl). Swap Cbl when asked.")
    while True:
        s = input("Cbl fitted now in nF (blank = stop): ").strip()
        if not s:
            break
        cbl = float(s)
        temp = thermo.read_c()
        for bit in (1, 0):
            for k in range(REPEATS):
                cell.write(bit)
                r = cell.read(restore=True)
                row(log, "share", clk, temp, cbl, 0, k, bit, r)


def mode_destructive(cell, log, clk, thermo):
    cbl = float(input("Cbl fitted now in nF: ").strip() or "4.7")
    temp = thermo.read_c()
    cell.write(1)
    for k in range(4):
        r = cell.read(restore=False)      # no write-back: the cell keeps the shared voltage
        row(log, "destructive", clk, temp, cbl, 0, k, 1, r)
    cell.write(1)
    r = cell.read(restore=True)
    row(log, "destructive_restored", clk, temp, cbl, 0, 4, 1, r)
    r = cell.read(restore=True)
    row(log, "destructive_restored", clk, temp, cbl, 0, 5, 1, r)


def mode_retention(cell, log, clk, thermo):
    cbl = float(input("Cbl fitted now in nF: ").strip() or "4.7")
    log.note("retention: write 1, park bitline at '%s', wait, read. Schedule %g..%g s" % (PARK, RET_MIN_S, RET_MAX_S))
    for wait in log_schedule(RET_MIN_S, RET_MAX_S, 4):
        for bit in (1, 0):
            cell.write(bit)
            t_end = time.ticks_add(time.ticks_ms(), int(wait * 1000))
            while time.ticks_diff(t_end, time.ticks_ms()) > 0:
                time.sleep_ms(20)
            r = cell.read(restore=False)
            row(log, "retention", clk, thermo.read_c(), cbl, wait, 0, bit, r)


def mode_peek(cell, log, clk, thermo):
    log.note("peek: storage-node follower vs time; leakage I = Cs * dV/dt")
    plog = CsvLog(["exp", "mode", "t_s", "temp_c", "v_sn", "v_ref"], LOGFILE)
    cell.write(1)
    t0 = clk.s()
    n = 0
    while clk.s() - t0 < PEEK_S:
        temp = thermo.read_c() if n % 30 == 0 else ""
        plog.row(["E1A", "peek", clk.s(), temp, cell.peek(), adc_volts(cell.adc_ref, 16)])
        n += 1
        time.sleep_ms(1000)


def main():
    low_ripple_supply()
    cell = Cell()
    thermo = Thermo(22)
    clk = Clock()
    log = CsvLog(HEADER, LOGFILE)
    log.note("E1A single cell, MODE=%s, Cs=%g nF, park=%s. REFERENCE CODE - UNTESTED ON HARDWARE" % (MODE, CS_NF, PARK))
    try:
        if MODE == "share":
            mode_share(cell, log, clk, thermo)
        elif MODE == "destructive":
            mode_destructive(cell, log, clk, thermo)
        elif MODE == "retention":
            mode_retention(cell, log, clk, thermo)
        elif MODE == "peek":
            mode_peek(cell, log, clk, thermo)
        else:
            log.note("unknown MODE")
    finally:
        cell.wl.value(0)
        cell.park()
        log.close()


if __name__ == "__main__":
    main()
