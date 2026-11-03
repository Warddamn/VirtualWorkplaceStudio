# e3_energy.py -- E3 "The price of distance": supply energy per transition vs load capacitance.
# REFERENCE CODE - UNTESTED ON HARDWARE. MicroPython, Raspberry Pi Pico (RP2040) or Pico 2 (RP2350).
# Needs t1_common.py on the Pico. Wiring: home-lab/E3_price_of_distance.md, "Circuit".
#
# Part A/B ("sweep"): GP15 PWM -> 74AHC125 buffer -> 33 Ohm -> load (cable / capacitor).
#   The buffer's GND pin returns through a 100 Ohm LOW-SIDE SHUNT to real ground.
#   ADC0 (GP26) <- shunt voltage through a 10 kOhm / 10 uF RC filter (averages the pulses; tau 0.1 s)
#   ADC1 (GP27) <- buffer VCC through a 100k/100k divider (so V_eff = 2*ADC1 - V_shunt)
#   Average current I = V_shunt / R_SHUNT; C_measured = slope of I vs f, divided by V_eff.
#   If MANUAL_DMM is True the script also asks you to type your multimeter reading (mV across the shunt).
# Part C ("spi"): idle loop, SRAM copy loop, SPI write loop; you read a USB power meter during each phase.
# Output: CSV over USB serial (mpremote run e3_energy.py > e3_sweep.csv)

import time
from machine import Pin, PWM, ADC, SPI
from t1_common import adc_volts, CsvLog, Clock, low_ripple_supply

MODE = "sweep"
PIN_OUT = 15
R_SHUNT = 100.0
FREQS = (100000, 250000, 500000, 1000000, 2000000)
SETTLE_MS = 1500             # > 10 x the 0.1 s RC filter
N_AVG = 4096
MANUAL_DMM = False
PHASE_S = 20                 # Part C phase length
SPI_BAUD = 10000000
LOGFILE = None


def measure(adc_shunt, adc_vcc):
    vs = adc_volts(adc_shunt, N_AVG)
    vcc = 2.0 * adc_volts(adc_vcc, 256)
    return vs, vs / R_SHUNT, vcc - vs


def mode_sweep(clk):
    pwm = PWM(Pin(PIN_OUT))
    adc_shunt, adc_vcc = ADC(26), ADC(27)
    log = CsvLog(["exp", "mode", "label", "c_nom_pF", "f_hz", "v_shunt", "i_a", "v_eff", "dmm_mV"], LOGFILE)
    log.note("Law: I = I_static + C * V * f.  Run the 'open' (nothing attached) load first.")
    while True:
        label = input("Load label (e.g. open, 1m_RG58, 100pF; blank = stop): ").strip()
        if not label:
            break
        c_nom = input("Nominal C in pF (0 if unknown): ").strip() or "0"
        fmax_s = input("Highest frequency in Hz (blank = %d; use 250000 for 1 nF): " % FREQS[-1]).strip()
        fmax = float(fmax_s) if fmax_s else FREQS[-1]
        # static point: output held low (no switching)
        pwm.freq(FREQS[0])
        pwm.duty_u16(0)
        time.sleep_ms(SETTLE_MS)
        vs, i, ve = measure(adc_shunt, adc_vcc)
        dmm = input("DMM mV across shunt (static), blank to skip: ").strip() if MANUAL_DMM else ""
        log.row(["E3", "sweep", label, c_nom, 0, vs, i, ve, dmm])
        for f in FREQS:
            if f > fmax:
                continue                  # the load could not fully charge each half-cycle (see bench_calcs E3)
            pwm.freq(f)
            pwm.duty_u16(32768)
            time.sleep_ms(SETTLE_MS)
            vs, i, ve = measure(adc_shunt, adc_vcc)
            dmm = input("DMM mV at %d Hz, blank to skip: " % f).strip() if MANUAL_DMM else ""
            log.row(["E3", "sweep", label, c_nom, f, vs, i, ve, dmm])
        pwm.duty_u16(0)
    pwm.deinit()


def mode_spi(clk):
    """Qualitative: watch the USB meter's average current during each 20 s phase."""
    log = CsvLog(["exp", "mode", "phase", "t_start_s", "t_end_s", "bytes", "bytes_per_s"], LOGFILE)
    src = bytearray(4096)
    dst = bytearray(4096)
    for i in range(4096):
        src[i] = (i * 37) & 0xFF
    msrc, mdst = memoryview(src), memoryview(dst)
    spi = SPI(0, baudrate=SPI_BAUD, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
    phases = ("idle_busy", "sram_copy", "spi_write")
    for phase in phases:
        log.note("PHASE %s starts now for %d s: note the USB meter average" % (phase, PHASE_S))
        t0 = clk.s()
        n = 0
        end = time.ticks_add(time.ticks_ms(), PHASE_S * 1000)
        while time.ticks_diff(end, time.ticks_ms()) > 0:
            if phase == "sram_copy":
                mdst[:] = msrc
                n += 4096
            elif phase == "spi_write":
                spi.write(src)
                n += 4096
            else:
                n += 0
        t1 = clk.s()
        log.row(["E3", "spi", phase, t0, t1, n, n / (t1 - t0)])
        time.sleep_ms(3000)            # gap so phases are separable in the meter's log
    spi.deinit()


def main():
    low_ripple_supply()
    clk = Clock()
    print("# E3 energy, MODE=%s. REFERENCE CODE - UNTESTED ON HARDWARE" % MODE)
    if MODE == "sweep":
        mode_sweep(clk)
    elif MODE == "spi":
        mode_spi(clk)


if __name__ == "__main__":
    main()
