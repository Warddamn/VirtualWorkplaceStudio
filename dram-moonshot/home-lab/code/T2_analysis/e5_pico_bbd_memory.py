# e5_pico_bbd_memory.py -- MicroPython for Raspberry Pi Pico / Pico 2 (RP2040 / RP2350)
#
# REFERENCE CODE - UNTESTED ON HARDWARE. Syntax-checked only (python3 -m py_compile).
# Check every pin against your own wiring and the BBD datasheet before you power anything.
#
# Home-lab experiment E5, "A charge river in a chip" (dram-moonshot track T2).
# A bucket-brigade device (BBD, e.g. Coolaudio V3207 = 1024 stages) becomes a circulating
# delay-line memory. The Pico's PIO block makes the two-phase BBD clock and, in "regen" mode,
# copies each bit read at the output (through a comparator) straight back into the input:
# exactly what a mercury delay-line memory of 1949 did, and what a DRAM sense amplifier does.
#
# MODES (set MODE below, then, with a NEW file name every run:
#        mpremote run e5_pico_bbd_memory.py | tee 2026-11-03_cte_1024_10k_r1.csv )
#   "delay"     : write a pseudo-random sequence, find the loop length L (clock periods) by correlation.
#   "cte"       : one pulse every 32 samples, ADC-sampled once per clock -> CSV for ccd_cte.py --samples.
#                 Valid only up to F_REF_HZ ~10-20 kHz (hard-IRQ latency); use a scope above that.
#   "retention" : for each hold in HOLDS_S: write a pattern, STOP the clock, restart, count flipped
#                 bits and which positions (buckets) flipped. The rotation is fixed ONCE from a
#                 0.01 s reference hold. A BBD bucket is a DRAM-like capacitor.
#   "retention_analog": same holds, but logs the ANALOG level of every bucket (hold_s,index,value)
#                 -> ccd_cte.py --retention separates common-mode drift from the weak-bucket tail.
#   "loop"      : write a pattern, regenerate it at F_RUN_HZ for STORE_S seconds, read it back,
#                 count errors -> bit-error rate per bit per lap.
#   "analog"    : no regeneration: flip an analog switch (CD4066) so the BBD output, through an
#                 op-amp gain stage, feeds its own input; ADC-log how the pattern blurs lap by lap.
#   "clock"     : just run the clock (for supply-current / energy-per-bit measurements).
#
# PIO timing: 32 state-machine cycles per BBD clock period. Phase A (CLK1 high) = 16 cycles,
# phase B (CLK2 high) = 16 cycles. The comparator is sampled at the middle of phase A and the
# next input bit is presented right after, so the BBD input is stable for the rest of the period.
#
# Default pins:
#   GP2, GP3  CLK1, CLK2 -> 74AHCT125 buffers powered from the BBD supply (5 V) -> BBD clock pins
#   GP4       DATA -> 100 kOhm -> BBD input node (biased by a divider, see E5 write-up)
#   GP5       COMP <- LM393 output (open collector, 10 kOhm pull-up to 3.3 V)
#   GP6       ANALOG-LOOP switch control -> spare 74AHCT125 buffer (5 V logic) -> CD4066 control
#             (a CD4066B on 5 V needs >= 3.5 V for "high"; 3.3 V straight from the Pico is not enough)
#             0 = input from DATA, 1 = input from feedback amp
#   GP26      ADC0 <- BBD output through a 15 kOhm / 22 kOhm divider (5 V -> 2.97 V)

import time
import array
import rp2
from machine import Pin, ADC

# ------------------------------- user settings ------------------------------------------------
MODE = "delay"
N_STAGES = 1024          # V3207 = 1024; two in series = 2048; V3205SD = 4096
F_REF_HZ = 10_000        # clock for writing / reading (datasheet range 10-200 kHz for V3207)
F_RUN_HZ = 10_000        # clock while regenerating in "loop" mode (sweep this: 10k ... 500k)
REGEN_LATE = False       # True: decide at cycle 14 of 16 in phase A (more comparator settling time;
                         # use above ~150 kHz with an LM393, whose response is ~0.3-1.3 us)
HOLDS_S = (0.03, 0.1, 0.3, 1, 3, 10, 30, 100)   # "retention" modes: clock-stop times (s)
REF_HOLD_S = 0.01        # reference hold: fixes the rotation / the 0-s analog levels
STORE_S = 60             # "loop": how long data circulates with regeneration
CTE_SAMPLES = 32 * 80    # "cte": ADC samples to capture (80 pulses)
INVERT = False           # True if your comparator output is inverted relative to the input
LOOP_LEN = None          # set to the value "delay" mode prints, e.g. 513; None = measure first
ANALOG_LAPS = 12

PIN_CLK1, PIN_DATA, PIN_COMP, PIN_SW, PIN_ADC = 2, 4, 5, 6, 26
SM_ID = 0

# ------------------------------- PIO programs -------------------------------------------------
# All programs start in phase A, and a stalled or stopped program also rests in phase A, so the
# init state of the side-set pins is phase A too: (CLK1 high, CLK2 low). Switching programs then
# never inserts a spurious clock cycle (which would add or drop one bit in the loop).
LO, HI = rp2.PIO.OUT_LOW, rp2.PIO.OUT_HIGH


@rp2.asm_pio(sideset_init=(HI, LO), out_init=LO,
             out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=32,
             in_shiftdir=rp2.PIO.SHIFT_LEFT, autopush=True, push_thresh=32)
def bbd_write():
    wrap_target()
    nop()                .side(0b01) [7]   # phase A: CLK1=1, CLK2=0 (8 cycles)
    in_(pins, 1)         .side(0b01)       # sample comparator, middle of phase A
    out(pins, 1)         .side(0b01) [6]   # present next data bit (phase A total 16)
    nop()                .side(0b10) [7]   # phase B: CLK1=0, CLK2=1
    nop()                .side(0b10) [7]   # phase B total 16 -> period 32 cycles
    wrap()


@rp2.asm_pio(sideset_init=(HI, LO), out_init=LO)
def bbd_regen():
    wrap_target()
    nop()                .side(0b01) [7]
    mov(pins, pins)      .side(0b01) [7]   # comparator -> data: regenerate the bit (phase A 16)
    nop()                .side(0b10) [7]
    nop()                .side(0b10) [7]
    wrap()


@rp2.asm_pio(sideset_init=(HI, LO), out_init=LO)
def bbd_regen_inv():
    wrap_target()
    nop()                .side(0b01) [7]
    mov(pins, invert(pins)) .side(0b01) [7]
    nop()                .side(0b10) [7]
    nop()                .side(0b10) [7]
    wrap()


@rp2.asm_pio(sideset_init=(HI, LO), out_init=LO)
def bbd_regen_late():
    wrap_target()
    nop()                .side(0b01) [7]
    nop()                .side(0b01) [5]
    mov(pins, pins)      .side(0b01) [1]   # decide at cycle 14 of 16: more comparator settling time
    nop()                .side(0b10) [7]
    nop()                .side(0b10) [7]
    wrap()


@rp2.asm_pio(sideset_init=(HI, LO), out_init=LO)
def bbd_regen_late_inv():
    wrap_target()
    nop()                .side(0b01) [7]
    nop()                .side(0b01) [5]
    mov(pins, invert(pins)) .side(0b01) [1]
    nop()                .side(0b10) [7]
    nop()                .side(0b10) [7]
    wrap()


def regen_program():
    if REGEN_LATE:
        return bbd_regen_late_inv if INVERT else bbd_regen_late
    return bbd_regen_inv if INVERT else bbd_regen


@rp2.asm_pio(sideset_init=(HI, LO), out_init=LO,
             out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=32)
def bbd_sample():
    wrap_target()
    nop()                .side(0b01) [7]
    irq(rel(0))          .side(0b01)       # tell the CPU: sample the ADC now
    out(pins, 1)         .side(0b01) [6]
    nop()                .side(0b10) [7]
    nop()                .side(0b10) [7]
    wrap()


def start(prog, f_clk, active=True):
    sm = rp2.StateMachine(SM_ID, prog, freq=int(32 * f_clk),
                          sideset_base=Pin(PIN_CLK1), out_base=Pin(PIN_DATA), in_base=Pin(PIN_COMP))
    if active:
        sm.active(1)
    return sm


def stop(sm):
    sm.active(0)


# ------------------------------- bit helpers --------------------------------------------------
def lfsr_bits(n, seed=0xACE1):
    """16-bit Galois LFSR pseudo-random bits."""
    out = bytearray(n)
    s = seed
    for i in range(n):
        lsb = s & 1
        s >>= 1
        if lsb:
            s ^= 0xB400
        out[i] = lsb
    return out


def pack(bits):
    words = []
    for i in range(0, len(bits) - len(bits) % 32, 32):
        w = 0
        for b in bits[i:i + 32]:
            w = (w << 1) | b
        words.append(w)
    return words


def unpack(words):
    out = bytearray(32 * len(words))
    k = 0
    for w in words:
        for j in range(31, -1, -1):
            out[k] = (w >> j) & 1
            k += 1
    return out


def stream(sm, tx_words):
    """Write mode: push tx words, collect the same number of rx words (comparator samples)."""
    rx = []
    pre = min(4, len(tx_words))
    for w in tx_words[:pre]:
        sm.put(w)
    for w in tx_words[pre:]:
        rx.append(sm.get())
        sm.put(w)
    while len(rx) < len(tx_words):
        rx.append(sm.get())
    return rx


def best_lag(tx, rx, lo, hi):
    best = (-1, None)
    n = len(rx)
    for d in range(lo, hi):
        agree = 0
        cnt = 0
        for t in range(d, n):
            agree += 1 if rx[t] == (tx[t - d] ^ (1 if INVERT else 0)) else 0
            cnt += 1
        if cnt and agree * 1000 // cnt > best[0]:
            best = (agree * 1000 // cnt, d)
    return best[1], best[0] / 1000


# ------------------------------- modes --------------------------------------------------------
def mode_delay():
    bits = lfsr_bits(32 * 96)
    sm = start(bbd_write, F_REF_HZ)
    rx = unpack(stream(sm, pack(bits)))
    stop(sm)
    half = N_STAGES // 2
    d, agree = best_lag(bits, rx, half - 40, half + 40)
    print("# loop length L = %s clock periods (agreement %.3f; expect ~N/2 = %d)" % (d, agree, half))
    print("# set LOOP_LEN = %s for 'retention' and 'loop' modes" % d)
    return d


def periodic_pattern(L, reps):
    """reps laps of an L-bit pattern, extended (not zero-padded) to a whole number of 32-bit
    words, so the last L bits written - the ones left in the line - are a rotation of it."""
    base = lfsr_bits(L, seed=0x1D0F)
    n = ((L * reps + 31) // 32) * 32
    out = bytearray(n)
    for i in range(n):
        out[i] = base[i % L]
    return base, out


def count_errors_rotation(ref, got):
    """Min errors over all rotations of ref (the loop content is a rotated copy)."""
    L = len(ref)
    best = (L + 1, 0)
    for r in range(L):
        e = 0
        for i in range(L):
            if got[i] != ref[(i + r) % L]:
                e += 1
                if e >= best[0]:
                    break
        if e < best[0]:
            best = (e, r)
    return best


def mode_retention(L):
    base, wr = periodic_pattern(L, 4)
    sm = start(bbd_write, F_REF_HZ)
    stream(sm, pack(wr))
    stop(sm)                       # clock frozen mid-period: every bucket holds its charge
    time.sleep(HOLD_S)
    sm.active(1)                   # resume where it stopped
    filler = bytes(32 * ((2 * L) // 32 + 2))
    rx = unpack(stream(sm, pack(filler)))
    stop(sm)
    got = rx[:L]
    e, rot = count_errors_rotation(base, got)
    pos = [i for i in range(L) if got[i] != base[(i + rot) % L]]
    ones_to_zero = sum(1 for i in pos if base[(i + rot) % L] == 1)
    print("hold_s,errors,bits,ones_to_zero,zeros_to_one,positions")
    print("%.3f,%d,%d,%d,%d,%s" % (HOLD_S, e, L, ones_to_zero, e - ones_to_zero,
                                   ";".join(str(p) for p in pos)))


def mode_loop(L):
    base, wr = periodic_pattern(L, 4)
    sm = start(bbd_write, F_REF_HZ)
    stream(sm, pack(wr))
    stop(sm)
    sm = start(bbd_regen_inv if INVERT else bbd_regen, F_RUN_HZ)
    t0 = time.ticks_ms()
    time.sleep(STORE_S)
    stop(sm)
    stored_s = time.ticks_diff(time.ticks_ms(), t0) / 1000
    sm = start(bbd_write, F_REF_HZ)
    rx = unpack(stream(sm, pack(bytes(32 * ((2 * L) // 32 + 2)))))
    stop(sm)
    e, rot = count_errors_rotation(base, rx[:L])
    laps = stored_s * F_RUN_HZ / L
    ber = e / (L * laps) if laps > 0 else 0
    print("f_run_hz,stored_s,laps,bits,errors,ber_per_bit_per_lap")
    print("%d,%.2f,%.0f,%d,%d,%.3e" % (F_RUN_HZ, stored_s, laps, L, e, ber))
    if e == 0:
        print("# zero errors: BER < %.1e per bit-lap (95%% upper limit = 3 / bit-laps)" % (3 / (L * laps)))


BUF_N = max(CTE_SAMPLES, ANALOG_LAPS * (N_STAGES // 2 + 8))
_buf = array.array("H", [0] * BUF_N)
_n = 0
_n_max = CTE_SAMPLES
_adc = ADC(PIN_ADC)
ADC_TO_V = 3.3 / 65535   # multiply by your divider ratio for real volts (ratios do not need it)


def _on_sample(sm):
    # hard IRQ: no allocation. _n < 0 means "still discarding line-fill samples".
    global _n
    if _n < 0:
        _n += 1
    elif _n < _n_max:
        _buf[_n] = _adc.read_u16()
        _n += 1


def capture_samples(word, n_skip, n_keep, switch_after=None, sw=None):
    """Run bbd_sample at F_REF_HZ feeding `word` repeatedly; ADC-sample once per clock."""
    global _n, _n_max
    _n_max = min(n_keep, BUF_N)
    _n = -n_skip                   # negative = still discarding the line-fill samples
    sm = start(bbd_sample, F_REF_HZ)
    sm.irq(_on_sample, hard=True)
    sent = 0
    while _n < _n_max:
        if switch_after is not None and sw is not None and sent * 32 >= switch_after:
            sw.value(1)
            word = 0               # input now comes from the feedback amplifier
        sm.put(word)
        sent += 1
    stop(sm)
    sm.irq(None)
    return _buf


def mode_cte():
    # discard the first N/2 + 64 samples while the line fills, then log one value per clock
    buf = capture_samples(0x80000000, N_STAGES // 2 + 64, CTE_SAMPLES)
    print("run,n_stages,f_clk_hz,index,value")
    for i in range(_n_max):
        print("N%d_%dHz,%d,%d,%d,%.6f" % (N_STAGES, F_REF_HZ, N_STAGES, F_REF_HZ, i, buf[i] * ADC_TO_V))
    print("# analyse: python3 ccd_cte.py --samples out.csv --fold-period 32 --skip 0")


def mode_analog(L):
    sw = Pin(PIN_SW, Pin.OUT, value=0)
    # one lap of a slow square pattern written from DATA, then the switch closes the analog loop
    buf = capture_samples(0xFFFF0000, 0, ANALOG_LAPS * L, switch_after=L, sw=sw)
    sw.value(0)
    print("lap,index_in_lap,value")
    for i in range(_n_max):
        print("%d,%d,%.6f" % (i // L, i % L, buf[i] * ADC_TO_V))


def mode_clock():
    sm = start(bbd_regen, F_RUN_HZ)
    print("# clock running at %d Hz for 60 s: read the supply currents now" % F_RUN_HZ)
    time.sleep(60)
    stop(sm)
    print("# clock stopped for 60 s: read the supply currents again")
    time.sleep(60)


def main():
    L = LOOP_LEN
    if MODE == "delay":
        mode_delay()
        return
    if MODE in ("retention", "loop", "analog") and L is None:
        L = mode_delay()
        if L is None:
            raise RuntimeError("could not find the loop length: check wiring and comparator threshold")
    if MODE == "retention":
        mode_retention(L)
    elif MODE == "loop":
        mode_loop(L)
    elif MODE == "cte":
        mode_cte()
    elif MODE == "analog":
        mode_analog(L)
    elif MODE == "clock":
        mode_clock()
    else:
        raise ValueError("unknown MODE")


main()
