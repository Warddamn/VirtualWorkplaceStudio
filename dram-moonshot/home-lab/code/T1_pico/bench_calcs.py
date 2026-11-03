#!/usr/bin/env python3
"""
bench_calcs.py -- expected numbers for Track T1 (bench electronics) of the DRAM Moonshot home lab.

Owner: T1 track (home-lab). Written 2026-11-03. Runs on a normal computer with Python 3 + numpy
(no scipy, no matplotlib). Usage:

    python3 bench_calcs.py              # print every table used in E1, E2 and E3
    python3 bench_calcs.py --selftest   # check the formulas against independent calculations, exit 0 on pass
    python3 bench_calcs.py --section e1 # only one experiment (e1, e2 or e3)

What it computes (first principles, shown with the arithmetic):
  E1  "A bit on the bench": charge sharing dV = (Vcell - Vpre) * Cs / (Cs + Cbl), repeated destructive reads,
      threshold-voltage loss without a boosted wordline, wordline kickback, write/restore time constants,
      retention t = C * dV_allowed / I_leak, leakage vs temperature (intrinsic-carrier physics and datasheet),
      ADC resolution, 16-cell retention statistics ("tails"), and the ECC refresh-extension Monte Carlo.
  E2  "A gain cell without a capacitor": storage-node capacitance (pure vs trimmed), retention per write switch,
      droop rate vs the published oxide cell, the chip-scale leakage needed, bandgap suppression of thermal
      generation, read-disturb coupling, 2-bit (MLC) margins.
  E3  "The price of distance": E = C*V^2 per charge/discharge cycle, expected shunt readings, settling limits,
      V^2 sweep, series-resistor independence, the chip-scale ladder and the hot-side 0.37 vs 3.95 pJ/bit
      breakdown (replicated from models/hot-side-memory.py), and the SPI-vs-SRAM estimate.

Evidence tags used in comments: [DATASHEET] [REPORTED] [ESTIMATE] [UNVERIFIED] [MODEL] (= study model output).
Every sourced number is listed in SOURCES at the bottom and in the Sources section of each guide.
"""

import argparse
import math
import sys

import numpy as np

KB_EV = 8.617333e-5      # Boltzmann constant, eV/K
Q_E = 1.602177e-19       # C
EPS0 = 8.854e-12         # F/m

# --------------------------------------------------------------------------------------------------------------
# INPUTS. Each entry: value, tag, note. Units in the key name.
# --------------------------------------------------------------------------------------------------------------
INPUTS = {
    # --- supply and Pico
    "V_io": (3.3, "[DATASHEET]", "Pico GPIO / 3V3 rail"),
    "adc_bits": (12, "[DATASHEET]", "RP2040/RP2350 ADC"),
    "adc_enob": (8.7, "[REPORTED]", "pico-sdk commit: RP2040 ADC ENOB 8.7 (measured, per RP2040 datasheet)"),
    # --- E1 parts
    "ald1106_vth_typ_V": (0.7, "[UNVERIFIED]", "ALD1106 typical Vth; a distributor lists 1 V (likely max); measure yours"),
    "ald1106_ioff_typ_A_12V": (10e-12, "[DATASHEET]", "ALD1106 IDS(OFF) 10 pA typ / 400 pA max, VDS=12 V, VGS=0, 25 C"),
    "ald1106_ioff_max_A_12V": (400e-12, "[DATASHEET]", "as above"),
    "ald1106_ioff_typ_A_125C": (1e-9, "[DATASHEET]", "ALD1106 IDS(OFF) 1 nA typ / 4 nA max at 125 C"),
    "ald1106_igss_typ_A": (0.1e-12, "[DATASHEET]", "ALD1106 IGSS 0.1 pA typ / 10 pA max, 25 C"),
    "ald1106_cov_F": (1e-12, "[ESTIMATE]", "gate-source overlap of a small-signal MOSFET array, ~0.5-2 pF"),
    "body_gamma_sqrtV": (0.5, "[ESTIMATE]", "generic body-effect coefficient"),
    "phi2_V": (0.7, "[ESTIMATE]", "2*phi_F"),
    "n2n7000_vth_typ_V": (2.1, "[DATASHEET]", "2N7000 VGS(th) 0.8 / 2.1 / 3.0 V at 1 mA"),
    "n2n7000_ciss_typ_F": (20e-12, "[DATASHEET]", "2N7000 Ciss 20 pF typ / 50 pF max (newer onsemi sheet; older: 60 pF max)"),
    "n2n7000_crss_F": (5e-12, "[ESTIMATE]", "2N7000 reverse transfer capacitance, few pF; not verified"),
    "n2n7000_idss_max_A_48V": (1e-6, "[DATASHEET]", "2N7000 IDSS 1 uA max at VDS=48 V (production limit, not typical)"),
    "n2n7000_K_A_per_V2": (0.1, "[ESTIMATE]", "square-law K from ID(on) 600 mA typ at VGS 4.5 V"),
    "lmc6482_ib_typ_A": (0.02e-12, "[DATASHEET]", "LMC6482 input current 20 fA typ, 4 pA max (25 C)"),
    "lmc6482_ib_max_A": (4e-12, "[DATASHEET]", "as above"),
    "mcp6544_ib_A": (1e-12, "[REPORTED]", "MCP6541/6544 bias current 1 pA (distributor attribute)"),
    "sa_offset_noise_V": (0.020, "[ESTIMATE]", "comparator offset + reference error + noise budget"),
    "c0g_ir_min_ohm_1nF": (1e11, "[DATASHEET]", "KEMET C0G: IR >= 1000 Ohm*F or 100 GOhm, whichever is lower -> 100 GOhm at 1 nF"),
    "bl_stray_F": (30e-12, "[ESTIMATE]", "bitline wiring + comparator + op-amp + 2 GPIO pins"),
    "r_bl_driver_ohm": (5e3, "[ESTIMATE]", "two 10 kOhm resistors from two GPIOs in parallel (Thevenin)"),
    "r_on_ald1106_ohm": (500.0, "[REPORTED]", "distributor lists RDS(on) 500 Ohm at 5 V for ALD1106"),
    # --- E2 parts
    "pn4117a_igss_max_A": (1e-12, "[REPORTED]", "2N4117A/PN4117A IGSS <= 1 pA at VGS=-20 V (A suffix); 10 pA non-A"),
    "pn4117_igss_max_A": (10e-12, "[REPORTED]", "non-A 4117"),
    "reed_ir_min_ohm": (1e12, "[DATASHEET]", "Coto 9000 series insulation resistance 1e12 Ohm min, 1e13 typ"),
    "reed_ir_typ_ohm": (1e13, "[DATASHEET]", "as above"),
    "sn_stray_F": (5e-12, "[ESTIMATE]", "air-wired storage node: switch terminal + wire + follower gate overlap"),
    "c_trim_F": (220e-12, "[ESTIMATE]", "C0G trim capacitor that makes the storage node a known size"),
    "kick_2n7000_F": (5e-12, "[ESTIMATE]", "2N7000 write switch gate-to-storage-node capacitance (~Crss)"),
    "kick_ald1106_F": (1e-12, "[ESTIMATE]", "ALD1106 gate-drain overlap"),
    "kick_jfet_F": (1.5e-12, "[ESTIMATE]", "4117-class JFET gate-drain capacitance"),
    "kick_reed_F": (1e-12, "[ESTIMATE]", "reed relay coil-to-contact capacitance"),
    "follower_gain": (0.98, "[ESTIMATE]", "source-follower small-signal gain with 47 kOhm source resistor"),
    "imec_ret_s_95C": (200.0, "[REPORTED]", "imec 2T0C IGZO >200 s at 95 C (via dossier hot-side-memory)"),
    "chip_csn_F": (0.15e-15, "[ESTIMATE]", "dossier: read-transistor gate as storage node at F=40 nm"),
    "chip_dv_crit_V": (0.100, "[ESTIMATE]", "dossier retention criterion"),
    "eg_si_eV": (1.12, "[ESTIMATE]", "textbook Si bandgap at 300 K"),
    "eg_igzo_eV": (3.15, "[ESTIMATE]", "amorphous IGZO optical gap ~3.0-3.3 eV"),
    # --- E3
    "rg58_pF_per_m": (101.0, "[DATASHEET]", "RG-58C/U nominal 30.8 pF/ft = 101 pF/m (varies 82-106)"),
    "jumper_pF_per_m": (20.0, "[ESTIMATE]", "single hook-up wire a few mm above a ground return"),
    "pcb_pF_per_m": (121.0, "[ESTIMATE]", "50 Ohm FR-4 microstrip: C = t_pd/Z0 = 6.06 ns/m / 50 Ohm"),
    "buffer_rout_ohm": (40.0, "[ESTIMATE]", "74AHC/74HC output resistance at 3.3 V"),
    "r_series_ohm": (33.0, "[ESTIMATE]", "damping resistor at the buffer output"),
    "r_shunt_ohm": (100.0, "[ESTIMATE]", "low-side shunt chosen for this build"),
    "fnb58_res_A": (10e-6, "[REPORTED]", "FNIRSI FNB58 USB tester current resolution 0.00001 A (retailer listings)"),
    "dmm_res_V": (0.1e-3, "[ESTIMATE]", "typical 6000-count DMM on its 600 mV range"),
    "pico_buck_eff": (0.85, "[UNVERIFIED]", "Pico on-board buck-boost efficiency at light load"),
    "c_pin_pad_F": (5e-12, "[ESTIMATE]", "MCU pin + pad + package"),
    "c_spi_device_in_F": (7e-12, "[ESTIMATE]", "typical CMOS input capacitance of an SPI peripheral"),
    "sram_pJ_per_32b": (5.0, "[ESTIMATE]", "on-chip SRAM access in a 40 nm-class MCU, 1-10 pJ per 32-bit word"),
}

# hot-side model inputs after the red team, copied from models/hot-side-memory.py (INPUTS + RED_TEAM_REVISIONS)
HOTSIDE = {
    "cells_per_rbl": 64, "c_bl_per_cell_fF": 0.08, "c_bl_fixed_fF": 3.0, "c_gbl_fF": 126.0,
    "V_array": 0.9, "dV_rbl_V": 0.3, "E_sa_cmp_fJ": 3.0, "cells_per_row": 8192, "c_wl_per_cell_fF": 0.16,
    "V_rwl_swing": 1.2, "V_wwl_swing": 2.2, "pump_eff": 0.45, "E_decode_fJ_bit": 2.0, "L_local_mm": 0.10,
    "c_wire_pF_mm": 0.20, "V_logic": 0.75, "C_bond_via_fF": 10.0, "activity": 0.5, "overhead_factor": 2.0,
    "E_ctrl_fJ_bit": 50.0, "write_verify_iters": 3.0, "write_share": 0.20, "L_deliver_near_mm": 3.0,
    "L_deliver_hbm_mm": 8.0, "E_hbm_pJ": 3.5,
}


def V(key):
    return INPUTS[key][0]


def hr(title):
    print("\n" + "=" * 100)
    print(title)
    print("=" * 100)


def eng(x, unit, digits=3):
    """Engineering notation, e.g. eng(1.2e-12, 'A') -> '1.2 pA'."""
    if x == 0:
        return "0 " + unit
    prefixes = [(1e-21, "z"), (1e-18, "a"), (1e-15, "f"), (1e-12, "p"), (1e-9, "n"), (1e-6, "u"), (1e-3, "m"),
                (1.0, ""), (1e3, "k"), (1e6, "M"), (1e9, "G"), (1e12, "T")]
    ax = abs(x)
    chosen = prefixes[0]
    for scale, p in prefixes:
        if ax >= scale:
            chosen = (scale, p)
    scale, p = chosen
    return "{:.{d}g} {}{}".format(x / scale, p, unit, d=digits)


def table(headers, rows):
    widths = [max(len(str(h)), *(len(str(r[i])) for r in rows)) for i, h in enumerate(headers)]
    line = "  ".join(str(h).rjust(w) for h, w in zip(headers, widths))
    print(line)
    print("  ".join("-" * w for w in widths))
    for r in rows:
        print("  ".join(str(c).rjust(w) for c, w in zip(r, widths)))


# --------------------------------------------------------------------------------------------------------------
# Shared physics
# --------------------------------------------------------------------------------------------------------------
def charge_share_dv(v_cell, v_pre, cs, cbl):
    """Charge conservation: (Cs*Vcell + Cbl*Vpre) = (Cs+Cbl)*Vfinal -> dV = (Vcell-Vpre)*Cs/(Cs+Cbl)."""
    return (v_cell - v_pre) * cs / (cs + cbl)


def repeated_reads(v_cell, v_pre, cs, cbl, n):
    """Destructive read without restore: each read leaves the cell at the shared voltage."""
    out = []
    v = v_cell
    for _ in range(n):
        dv = charge_share_dv(v, v_pre, cs, cbl)
        out.append(dv)
        v = v_pre + dv          # cell now sits at the bitline's shared voltage
    return out


def retention_time(c, dv_allowed, i_leak):
    """t = C * dV / I (constant-current leakage, first order)."""
    return c * dv_allowed / i_leak


def allowed_droop_1t1c(v_write, v_pre, cs, cbl, delta):
    """A stored '1' still reads correctly while (Vsn - Vpre)*Cs/(Cs+Cbl) > delta."""
    v_min = v_pre + delta * (cs + cbl) / cs
    return v_write - v_min, v_min


def vth_body(vth0, vsb, gamma, phi2):
    return vth0 + gamma * (math.sqrt(phi2 + max(vsb, 0.0)) - math.sqrt(phi2))


def sn_max_vt_loss(v_wl, v_bl, vth0, gamma, phi2):
    """Highest storage-node voltage a source-follower-connected NMOS can pass: Vsn = min(Vbl, Vwl - Vth(Vsn))."""
    v = 0.0
    for _ in range(200):
        v_new = min(v_bl, v_wl - vth_body(vth0, v, gamma, phi2))
        if abs(v_new - v) < 1e-9:
            break
        v = 0.5 * (v + v_new)
    return v


def kickback(dv_wl, c_ov, cs):
    return dv_wl * c_ov / (cs + c_ov)


def eg_si(t_k):
    """Varshni fit for Si (textbook constants): Eg(T) = 1.17 - 4.73e-4 T^2/(T+636) eV."""
    return 1.17 - 4.73e-4 * t_k ** 2 / (t_k + 636.0)


def gen_leak_ratio(t_c, tref_c=22.0):
    """Depletion-region generation current ~ ni ~ T^1.5 exp(-Eg/2kT)."""
    t, tr = t_c + 273.15, tref_c + 273.15
    return (t / tr) ** 1.5 * math.exp(-eg_si(t) / (2 * KB_EV * t) + eg_si(tr) / (2 * KB_EV * tr))


def diff_leak_ratio(t_c, tref_c=22.0):
    """Diffusion current ~ ni^2 ~ T^3 exp(-Eg/kT)."""
    t, tr = t_c + 273.15, tref_c + 273.15
    return (t / tr) ** 3 * math.exp(-eg_si(t) / (KB_EV * t) + eg_si(tr) / (KB_EV * tr))


def datasheet_leak_ratio(t_c, tref_c=22.0):
    """ALD1106 typical IDS(OFF): 10 pA at 25 C -> 1 nA at 125 C = 100x per 100 C."""
    per_c = (V("ald1106_ioff_typ_A_125C") / V("ald1106_ioff_typ_A_12V")) ** (1.0 / 100.0)
    return per_c ** (t_c - tref_c)


def doubling_interval(ratio_fn, t1=22.0, t2=45.0):
    r = ratio_fn(t2, t1)
    return (t2 - t1) * math.log(2) / math.log(r)


def norm_cdf(x):
    return 0.5 * math.erfc(-x / math.sqrt(2.0))


def norm_ppf(p):
    """Inverse standard normal CDF by bisection (stdlib only)."""
    lo, hi = -40.0, 40.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if norm_cdf(mid) < p:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def rc_charge_energy_numeric(c, r, v, n=200000, t_mult=15.0):
    """Integrate supply energy and resistor heat while charging C from 0 to V through R (numpy)."""
    tau = r * c
    t = np.linspace(0.0, t_mult * tau, n)
    i = (v / r) * np.exp(-t / tau)
    e_supply = np.trapezoid(v * i, t)
    e_heat = np.trapezoid(i * i * r, t)
    return e_supply, e_heat


# --------------------------------------------------------------------------------------------------------------
# E1
# --------------------------------------------------------------------------------------------------------------
def e1_tables(rng):
    hr("E1  A BIT ON THE BENCH (discrete 1T1C cell and 4x4 array)")
    vio = V("V_io")
    vpre = vio / 2
    stray = V("bl_stray_F")
    print("Law 1 (charge conservation): dV = (Vcell - Vpre) * Cs / (Cs + Cbl).  Vcell = %.2f V, Vpre = %.3f V."
          % (vio, vpre))
    print("Bitline total = plug-in Cbl + ~%s of wiring/comparator/op-amp/GPIO strays [ESTIMATE]." % eng(stray, "F"))
    rows = []
    for cs in (1e-9, 10e-9):
        for cbl_nom in (1e-9, 2.2e-9, 4.7e-9, 10e-9, 22e-9, 47e-9, 100e-9):
            if cbl_nom / cs > 25 or cbl_nom / cs < 0.9:
                continue
            cbl = cbl_nom + stray
            dv1 = charge_share_dv(vio, vpre, cs, cbl)
            dv0 = charge_share_dv(0.0, vpre, cs, cbl)
            lo = charge_share_dv(vio, vpre, cs * 0.95, cbl * 1.05)
            hi = charge_share_dv(vio, vpre, cs * 1.05, cbl * 0.95)
            rows.append((eng(cs, "F"), eng(cbl_nom, "F"), "%.2f" % (cbl / cs), "%+.0f" % (dv1 * 1e3),
                         "%+.0f" % (dv0 * 1e3), "%.0f-%.0f" % (lo * 1e3, hi * 1e3)))
    table(["Cs", "Cbl (plug-in)", "Cbl/Cs", "dV '1' mV", "dV '0' mV", "'1' range, 5% caps"], rows)
    print("Real DRAM: Cbl/Cs ~6.4 (models/dram_cell_physics.py: 34.7 fF bitline vs 5.42 fF cell at 1-beta, fresh "
          "signal ~71 mV at a 1.05 V array). The 4.7 nF and 10 nF rows bracket that ratio.")

    hr("E1.2  Destructive read: read the same cell again WITHOUT restore (Cs = 1 nF, Cbl = 4.7 nF)")
    seq = repeated_reads(vio, vpre, 1e-9, 4.7e-9 + stray, 4)
    for k, dv in enumerate(seq, 1):
        print("  read %d: dV = %+.1f mV" % (k, dv * 1e3))
    print("Each read shrinks the signal by Cs/(Cs+Cbl) = %.3f. Restore (write-back) after every read is mandatory."
          % (1e-9 / (1e-9 + 4.7e-9 + stray)))

    hr("E1.3  Threshold-voltage loss and the boosted wordline (ALD1106, body at 0 V)")
    vth0, g, p2 = V("ald1106_vth_typ_V"), V("body_gamma_sqrtV"), V("phi2_V")
    rows = []
    for vwl in (3.3, 5.0, 9.0):
        sn = sn_max_vt_loss(vwl, vio, vth0, g, p2)
        rows.append(("%.1f V" % vwl, "%.2f V" % sn, "%.2f V" % vth_body(vth0, sn, g, p2)))
    table(["wordline high", "max stored '1'", "Vth at that node"], rows)
    print("2N7000 (body tied to source, Vth typ 2.1 V): wordline 3.3 V passes only ~%.1f V. "
          "Real DRAM boosts its wordline (VPP ~2.9 V for a ~1.05 V array) for the same reason." % (3.3 - 2.1))
    sn33 = sn_max_vt_loss(3.3, vio, vth0, g, p2)
    dv_lost = charge_share_dv(sn33, vpre, 1e-9, 4.7e-9 + stray)
    print("Signal with the unboosted '1' (Cs 1 nF, Cbl 4.7 nF): %+.0f mV instead of %+.0f mV."
          % (dv_lost * 1e3, charge_share_dv(vio, vpre, 1e-9, 4.7e-9 + stray) * 1e3))

    hr("E1.4  Wordline kickback when the gate falls 9 V -> 0 V")
    rows = []
    for name, cov in (("ALD1106 (~1 pF overlap, est.)", V("ald1106_cov_F")),
                      ("2N7000 (~half of Ciss 20 pF)", V("n2n7000_ciss_typ_F") / 2)):
        for cs in (1e-9, 10e-9):
            rows.append((name, eng(cs, "F"), "%.1f mV" % (kickback(9.0, cov, cs) * 1e3)))
    table(["switch", "Cs", "kick"], rows)

    hr("E1.5  Write / precharge / restore time constants")
    rdrv = V("r_bl_driver_ohm")
    for cbl in (4.7e-9, 22e-9, 100e-9):
        tau = rdrv * (cbl + 1e-9)
        print("  precharge/restore through %s into %s + 1 nF: tau = %s, settle to 0.1%% in 7 tau = %s"
              % (eng(rdrv, "Ohm"), eng(cbl, "F"), eng(tau, "s"), eng(7 * tau, "s")))
    tau_on = V("r_on_ald1106_ohm") * (1e-9 * 4.7e-9 / 5.7e-9)
    print("  charge sharing through the access switch (Ron ~500 Ohm): tau = %s -> 1 ms wordline pulse is plenty"
          % eng(tau_on, "s"))

    hr("E1.6  Retention: t = Cs * dV_allowed / I_leak")
    delta = V("sa_offset_noise_V")
    rows = []
    for cs, cbl in ((1e-9, 4.7e-9), (10e-9, 47e-9)):
        droop, vmin = allowed_droop_1t1c(vio, vpre, cs, cbl + stray, delta)
        for i in (1e-12, 10e-12, 33e-12, 100e-12, 1e-9):
            rows.append((eng(cs, "F"), "%.2f V" % vmin, "%.2f V" % droop, eng(i, "A"),
                         eng(retention_time(cs, droop, i), "s")))
    table(["Cs", "lowest readable '1'", "allowed droop", "leakage", "retention"], rows)
    i_ald_3v = V("ald1106_ioff_typ_A_12V") * math.sqrt(3.3 / 12.0)
    i_c0g = 3.3 / V("c0g_ir_min_ohm_1nF")
    print("Leakage budget at 22 C for Cs = 1 nF C0G [ESTIMATE]:")
    print("  ALD1106 off-state, 10 pA typ at 12 V scaled by sqrt(3.3/12) (junction width): ~%s (max %s at 12 V)"
          % (eng(i_ald_3v, "A"), eng(V("ald1106_ioff_max_A_12V"), "A")))
    print("  C0G 1 nF at its WORST-CASE spec (100 GOhm at 3.3 V): <= %s (typical parts are far better)"
          % eng(i_c0g, "A"))
    print("  peek op-amp LMC6482 input: %s typ, %s max" % (eng(V("lmc6482_ib_typ_A"), "A"),
                                                         eng(V("lmc6482_ib_max_A"), "A")))
    droop, _ = allowed_droop_1t1c(vio, vpre, 1e-9, 4.7e-9 + stray, delta)
    print("  => planning retention at 22 C: %s (ALD typ) down to %s (cap at its worst-case spec)"
          % (eng(retention_time(1e-9, droop, i_ald_3v), "s"), eng(retention_time(1e-9, droop, i_c0g), "s")))

    hr("E1.7  Leakage vs temperature (retention scales as 1/leakage)")
    rows = []
    for tc in (4.0, 22.0, 35.0, 45.0, 55.0):
        rows.append(("%.0f C" % tc, "%.2fx" % gen_leak_ratio(tc), "%.2fx" % diff_leak_ratio(tc),
                     "%.2fx" % datasheet_leak_ratio(tc)))
    table(["temperature", "generation (ni)", "diffusion (ni^2)", "ALD1106 datasheet trend"], rows)
    print("Doubling interval near room temperature: generation %.1f C, diffusion %.1f C, datasheet trend %.1f C."
          % (doubling_interval(gen_leak_ratio), doubling_interval(diff_leak_ratio),
             doubling_interval(datasheet_leak_ratio)))
    print("Study models use 'retention halves per ~10 C' for silicon DRAM (models/dram_cell_physics.py).")
    print("If retention barely changes with temperature, leakage is NOT junction physics: suspect surface/humidity "
          "paths or the capacitor's dielectric.")

    hr("E1.8  Pico ADC resolution vs the signal")
    lsb = V("V_io") / 2 ** V("adc_bits")
    eff = V("V_io") / 2 ** V("adc_enob")
    print("12-bit LSB = %.3f mV; ENOB 8.7 -> effective step %.1f mV; averaging 256 samples -> ~%.2f mV (if noise "
          "is random)." % (lsb * 1e3, eff * 1e3, eff * 1e3 / 16))
    print("Smallest planned signal (Cbl/Cs ~22) is ~70 mV: >10 effective steps even for a single sample.")

    hr("E1.9  Sixteen cells: the first taste of tails (lognormal retention, Monte Carlo)")
    z4 = norm_ppf(1e-4)
    print("For lognormal retention ln(t) ~ N(mu, s): the 1e-4 quantile is median * exp(%.3f * s)." % z4)
    rows = []
    for s in (0.3, 0.5, 1.0):
        samples = rng.lognormal(mean=0.0, sigma=s, size=(20000, 16))
        srt = np.sort(samples, axis=1)
        weakest = np.median(srt[:, 0])
        second = np.median(srt[:, 1])
        ratio = np.median(srt[:, 1] / srt[:, 0])
        q4_true = math.exp(z4 * s)
        # estimate s from 16 samples, extrapolate to 1e-4, report 90% spread
        mu_hat = np.mean(np.log(samples), axis=1)
        s_hat = np.std(np.log(samples), axis=1, ddof=1)
        q4_hat = np.exp(mu_hat + z4 * s_hat)
        p5, p95 = np.percentile(q4_hat / q4_true, [5, 95])
        rows.append(("%.1f" % s, "%.2f" % weakest, "%.2f" % second, "%.2fx" % ratio, "%.4f" % q4_true,
                     "%.2f-%.2fx" % (p5, p95)))
    table(["sigma ln", "weakest of 16 (x median)", "2nd weakest", "2nd/1st ratio (median)", "true 1e-4 quantile",
           "16-cell estimate of it (90% band)"], rows)
    print("Reading: 16 cells pin down the median; their extrapolation to the 1e-4 quantile is off by up to ~2-3x "
          "either way EVEN IF the distribution really is lognormal, and real tails often are not (VRT, defects). "
          "The study's kill lines sit at the 1e-4 quantile: that needs >=1e5 cells measured directly.")
    print("ECC link (raw-ber-contract in miniature): one-error-correcting code over the 16 cells lets you refresh at "
          "the 2nd-weakest cell's retention, i.e. the 2nd/1st ratio above, instead of the weakest's.")

    hr("E1.10  Refresh cost on the bench vs on a chip")
    cbl, cs = 4.7e-9, 1e-9
    e_restore = (cbl + cs + stray) * vio * (vio - (vpre + charge_share_dv(vio, vpre, cs, cbl + stray)))
    e_pre = (vio / 20e3) * vio * 5e-3   # static current of the 10k+10k GPIO divider during a 5 ms precharge
    print("Restore one '1' on the bench: E ~ (Cbl+Cs) * V * (V - Vshared) = %s; precharge divider for 5 ms adds %s."
          % (eng(e_restore, "J"), eng(e_pre, "J")))
    print("Chip DRAM refresh is ~46 fJ per bit (models/dram_cell_physics.py) [MODEL]: the bench pays ~1e5-1e6x more "
          "per bit because its capacitors are ~1e5x larger and its voltage ~3x higher.")
    return {"dv_4p7": charge_share_dv(vio, vpre, 1e-9, 4.7e-9 + stray)}


# --------------------------------------------------------------------------------------------------------------
# E2
# --------------------------------------------------------------------------------------------------------------
def e2_tables():
    hr("E2  A GAIN CELL WITHOUT A CAPACITOR (discrete 2T0C)")
    crss = V("n2n7000_crss_F")
    ciss = V("n2n7000_ciss_typ_F")
    cgs = ciss - crss
    a = V("follower_gain")
    stray = V("sn_stray_F")
    c_pure = crss + cgs * (1 - a) + stray
    c_trim = c_pure + V("c_trim_F")
    print("Storage node = read-FET gate + strays. With a source-follower read, the source tracks the gate, so Cgs is "
          "bootstrapped away:")
    print("  C_SN(pure) = Crss + Cgs*(1-A) + strays = %s + %s*(1-%.2f) + %s = %s [ESTIMATE]"
          % (eng(crss, "F"), eng(cgs, "F"), a, eng(stray, "F"), eng(c_pure, "F")))
    print("  C_SN(trimmed, +%s C0G) = %s" % (eng(V("c_trim_F"), "F"), eng(c_trim, "F")))
    print("  (With a common-source read instead, Miller multiplies Crss and C_SN becomes bias-dependent; avoid.)")

    hr("E2.2  Expected leakage of each write switch at ~3 V, 22 C")
    switches = [
        ("2N7000 (ordinary MOSFET)", 10e-12, 10e-9,
         "datasheet only gives 1 uA max at 48 V; real value unknown -> measure [ESTIMATE range]"),
        ("ALD1106 (low-leakage MOSFET)", V("ald1106_ioff_typ_A_12V") * math.sqrt(3.3 / 12),
         V("ald1106_ioff_max_A_12V"), "10 pA typ / 400 pA max at 12 V [DATASHEET], scaled"),
        ("JFET 4117-class (gate off at -9 V)", 0.2e-12, V("pn4117_igss_max_A"),
         "IGSS <= 1 pA (A suffix) / 10 pA (non-A) at -20 V [REPORTED]"),
        ("reed relay (Coto 9000-class)", 3.3 / V("reed_ir_typ_ohm"), 3.3 / V("reed_ir_min_ohm"),
         "IR 1e13 typ / 1e12 min Ohm [DATASHEET] at 3.3 V across the contacts"),
    ]
    rows = []
    for name, lo, hi, note in switches:
        rows.append((name, eng(lo, "A"), eng(hi, "A"), note))
    table(["switch", "low/typ", "high/max", "basis"], rows)

    hr("E2.3  Retention to lose 100 mV (dossier criterion) and 200 mV (SEL patent criterion)")
    rows = []
    for name, lo, hi, _ in switches:
        for cname, c in (("pure", c_pure), ("trimmed", c_trim)):
            rows.append((name, cname, eng(retention_time(c, 0.1, hi), "s"), eng(retention_time(c, 0.1, lo), "s"),
                         eng(retention_time(c, 0.2, lo), "s")))
    table(["switch", "node", "100 mV @ high leak", "100 mV @ low leak", "200 mV @ low leak"], rows)
    print("Floor: the read FET's own gate leakage and board/surface leakage (~0.01-1 pA) cap the best switch. "
          "The reed-relay cell measures that floor.")

    hr("E2.4  Droop rate: your bench cell vs the published oxide cell")
    i_imec = V("chip_csn_F") * V("chip_dv_crit_V") / V("imec_ret_s_95C")
    rate_imec = i_imec / V("chip_csn_F")
    print("Published oxide 2T0C: 0.15 fF x 100 mV / 200 s = %s leakage -> droop %.2f mV/s at 95 C [ESTIMATE from "
          "REPORTED retention]." % (eng(i_imec, "A"), rate_imec * 1e3))
    for name, lo, hi, _ in switches:
        print("  %-36s trimmed node droops %s/s (low) to %s/s (high)"
              % (name, eng(lo / c_trim, "V"), eng(hi / c_trim, "V")))
    print("Same droop rate = same retention. The oxide cell gets it with ~%s less capacitance, so its switch must "
          "leak ~%s less." % ("%.0e x" % (c_trim / V("chip_csn_F")), "%.0e x" % (c_trim / V("chip_csn_F"))))

    hr("E2.5  Scale-up: leakage a 0.15 fF chip node may have, for a given retention (100 mV loss)")
    rows = []
    for t in (0.064, 1.0, 3.6, 100.0, 3600.0):
        i = retention_time(V("chip_csn_F"), V("chip_dv_crit_V"), 1.0) / t  # C*dV/t
        rows.append(("%g s" % t, eng(i, "A")))
    table(["target retention", "max leakage"], rows)
    print("The study's kill line (1e-4 tail >=1 s at 105 C) allows ~22.5 aA for 1 bit (dossier); a silicon "
          "junction of chip size leaks ~fA at 85 C -> 1e3-1e4x too much.")

    hr("E2.6  First principles: why a wide bandgap kills thermal leakage")
    rows = []
    for tc in (25.0, 95.0, 125.0):
        t = tc + 273.15
        ratio = math.exp(-(V("eg_igzo_eV") - V("eg_si_eV")) / (2 * KB_EV * t))
        rows.append(("%.0f C" % tc, "%.1e" % ratio))
    table(["temperature", "generation-current factor exp(-(Eg_ox - Eg_Si)/2kT)"], rows)
    print("Thermal generation in IGZO (Eg ~3.15 eV) is ~1e-17 of silicon's per unit volume. Measured oxide leakage "
          "(zA-aA) is set by defects, contacts and tunnelling, not this intrinsic floor [ESTIMATE].")

    hr("E2.6b  Write-wordline kickback: the switch's own gate capacitance kicks the node when it turns off")
    rows = []
    for name, ck, swing in (("2N7000, WWL +9 -> 0 V", V("kick_2n7000_F"), 9.0),
                            ("2N7000, WWL +9 -> -9 V (negative hold)", V("kick_2n7000_F"), 18.0),
                            ("ALD1106, WWL +9 -> 0 V", V("kick_ald1106_F"), 9.0),
                            ("JFET, gate ~+3 -> -9 V", V("kick_jfet_F"), 12.0),
                            ("reed relay, coil 5 -> 0 V", V("kick_reed_F"), 5.0)):
        rows.append((name, "%.0f mV" % (kickback(swing, ck, c_pure) * 1e3),
                     "%.0f mV" % (kickback(swing, ck, c_trim) * 1e3)))
    table(["write switch", "kick, pure node", "kick, trimmed node"], rows)
    print("A kick of volts on the pure node can push it below 0 V and forward-bias junctions: data lost. That is why "
          "real 2T0C designs budget a 'window after WWL kickback' (dossier: 600 mV) and why the trim capacitor is used "
          "for MOSFET switches here.")

    hr("E2.7  Read disturb by capacitive coupling (read-enable toggles the drain 0 <-> 3.3 V)")
    for cname, c in (("pure", c_pure), ("trimmed", c_trim)):
        print("  %-8s node: transient kick = Crss * 3.3 V / C_SN = %.0f mV (returns when the drain returns; "
              "net charge unchanged)" % (cname, crss * 3.3 / c * 1e3))

    hr("E2.8  Read transfer: source follower Vout = Vsn - Vth - sqrt(I/K)")
    vth = V("n2n7000_vth_typ_V")
    for vsn in (2.3, 2.6, 2.9, 3.2):
        # solve Vout = Vsn - vth - sqrt((Vout/Rs)/K)
        rs, k = 47e3, V("n2n7000_K_A_per_V2")
        vout = max(vsn - vth, 0.0)
        for _ in range(100):
            vout = max(vsn - vth - math.sqrt(max(vout, 0.0) / rs / k), 0.0)
        print("  Vsn %.1f V -> Vout ~%.3f V (2N7000 Vth 2.1 V typ; your part may sit anywhere in 0.8-3.0 V)"
              % (vsn, vout))

    hr("E2.9  Two bits per cell (MLC) on the bench (firmware targets 0.15 / 0.45 / 0.75 / 1.05 V at the follower)")
    halves = ((1, 0.55, "'0' = node below Vth (Vout ~0), '1' = Vout ~1.1 V, threshold 0.55 V"),
              (2, 0.15, "4 levels 0.30 V apart, thresholds midway"))
    for bits, half, note in halves:
        print("  %d bit/cell: %s -> half-spacing %.0f mV; time to lose it at 1 pA on the trimmed node = %s"
              % (bits, note, half * 1e3, eng(retention_time(c_trim, half, 1e-12), "s")))
    sig = 0.002
    for bits, half, _ in halves:
        q = half / sig
        p_err = 2 * (1 - norm_cdf(q))
        print("  read noise 2 mV rms (Pico ADC averaged), %d bit: margin = %.0f sigma -> raw error rate per read %s"
              % (bits, q, ("%.1e" % p_err) if p_err > 1e-15 else "< 1e-15 (negligible)"))
    print("  So MLC on the bench fails by DRIFT (leakage), not noise: retention shrinks ~%.1fx going 1 -> 2 bits."
          % (0.55 / 0.15))
    return {"c_pure": c_pure, "c_trim": c_trim, "rate_imec": rate_imec}


# --------------------------------------------------------------------------------------------------------------
# E3
# --------------------------------------------------------------------------------------------------------------
def hotside_energy():
    h = HOTSIDE
    c_rbl = h["cells_per_rbl"] * h["c_bl_per_cell_fF"] + h["c_bl_fixed_fF"]
    bits = 2
    e_rbl_cell = (c_rbl + h["c_gbl_fF"]) * h["V_array"] * h["dV_rbl_V"]
    e_sa_cell = (2 ** bits - 1) * h["E_sa_cmp_fJ"]
    c_wl = h["cells_per_row"] * h["c_wl_per_cell_fF"]
    e_rwl_cell = c_wl * h["V_rwl_swing"] ** 2 / h["cells_per_row"]
    e_cell_read_bit = (e_rbl_cell + e_sa_cell + e_rwl_cell) / bits
    e_local = h["activity"] * h["L_local_mm"] * h["c_wire_pF_mm"] * 1e3 * h["V_array"] ** 2
    e_bond = h["activity"] * h["C_bond_via_fF"] * h["V_logic"] ** 2
    e_read = (e_cell_read_bit + h["E_decode_fJ_bit"] + e_local + e_bond) * h["overhead_factor"] + h["E_ctrl_fJ_bit"]
    e_wbl = (c_rbl + h["c_gbl_fF"]) * h["V_array"] ** 2
    e_wwl = c_wl * h["V_wwl_swing"] ** 2 / h["pump_eff"] / h["cells_per_row"]
    e_write_cell = h["write_verify_iters"] * (e_wbl + e_wwl + e_rbl_cell + e_sa_cell)
    e_write = (e_write_cell / bits + h["E_decode_fJ_bit"] + e_local + e_bond) * h["overhead_factor"] \
        + h["E_ctrl_fJ_bit"]
    e_mix = (1 - h["write_share"]) * e_read + h["write_share"] * e_write
    e_wire_mm = h["activity"] * h["c_wire_pF_mm"] * 1e3 * h["V_logic"] ** 2
    near = (e_mix + e_wire_mm * h["L_deliver_near_mm"]) / 1e3
    hbm = h["E_hbm_pJ"] + e_wire_mm * h["L_deliver_hbm_mm"] / 1e3
    return dict(c_rbl=c_rbl, e_rbl_cell=e_rbl_cell, e_cell_read_bit=e_cell_read_bit, e_local=e_local,
                e_bond=e_bond, e_read=e_read, e_write=e_write, e_mix=e_mix, e_wire_mm=e_wire_mm,
                near_pJ=near, hbm_pJ=hbm)


def e3_tables():
    hr("E3  THE PRICE OF DISTANCE (energy per bit vs wire capacitance)")
    v = V("V_io")
    print("Law: charging a capacitance C to V draws Q = C*V from the supply, i.e. E = Q*V = C*V^2 per full "
          "charge+discharge cycle. Half heats the pull-up, half the pull-down, whatever their resistance.")
    print("Average supply current of a square wave: I = C * V * f.  At 3.3 V and 1 MHz: %.2f uA per pF."
          % (1e-12 * v * 1e6 * 1e6))
    loads = [
        ("open buffer output (baseline)", 0.0),
        ("10 cm hook-up wire", 0.10 * V("jumper_pF_per_m") * 1e-12),
        ("10 cm PCB trace (50 Ohm)", 0.10 * V("pcb_pF_per_m") * 1e-12),
        ("1 m RG-58", 1.0 * V("rg58_pF_per_m") * 1e-12),
        ("3 m RG-58", 3.0 * V("rg58_pF_per_m") * 1e-12),
        ("100 pF C0G (calibration)", 100e-12),
        ("330 pF C0G (calibration)", 330e-12),
        ("1 nF C0G (calibration)", 1e-9),
    ]
    rshunt = V("r_shunt_ohm")
    r_drive = V("buffer_rout_ohm") + V("r_series_ohm")
    rows = []
    for name, c in loads:
        e_cyc = c * v * v
        tau = r_drive * c
        fmax = 1.0 / (2 * 7 * tau) if c > 0 else float("inf")
        di_1m = c * v * 1e6
        rows.append((name, eng(c, "F") if c else "~0 (pin + buffer Cpd)", eng(e_cyc, "J"), eng(e_cyc / 4, "J"),
                     eng(di_1m, "A"), "%.2f mV" % (di_1m * rshunt * 1e3),
                     ("%.2g MHz" % (fmax / 1e6)) if c else "-"))
    table(["load", "C", "E per cycle C*V^2", "per random bit ~CV^2/4", "extra I at 1 MHz",
           "on %g Ohm shunt" % rshunt, "max f (7 tau settle)"], rows)
    print("Resolution check: DMM 0.1 mV on a 100 Ohm shunt = 1 uA = 0.3 pF at 1 MHz; FNB58 USB meter 10 uA "
          "resolution = 3 pF at 1 MHz (on the 3.3 V side) [REPORTED resolution, not accuracy].")

    hr("E3.2  Frequency sweep: I must rise linearly with f (energy is per transition, not per second)")
    c = V("rg58_pF_per_m") * 1e-12
    rows = []
    for f in (100e3, 250e3, 500e3, 1e6, 2e6):
        rows.append(("%g kHz" % (f / 1e3), eng(c * v * f, "A"), "%.2f mV" % (c * v * f * rshunt * 1e3)))
    table(["f (1 m RG-58)", "extra current", "shunt"], rows)

    hr("E3.3  Supply-voltage sweep: E ~ V^2")
    for vv in (1.8, 2.5, 3.3):
        print("  V = %.1f V: E per cycle on 1 m RG-58 = %s (%.2fx of 3.3 V)" % (vv, eng(c * vv * vv, "J"),
                                                                            (vv / 3.3) ** 2))

    hr("E3.4  Series resistance does not change the energy (numerical check, 100 pF to 3.3 V)")
    for r in (33.0, 330.0, 3300.0):
        es, eh = rc_charge_energy_numeric(100e-12, r, 3.3)
        print("  R = %6.0f Ohm: supply gives %s, resistor burns %s, cap stores %s"
              % (r, eng(es, "J"), eng(eh, "J"), eng(0.5 * 100e-12 * 3.3 ** 2, "J")))

    hr("E3.5  From the bench to the chip: one law, ten orders of magnitude")
    hs = hotside_energy()
    act = HOTSIDE["activity"]
    ladder = [
        ("3 m RG-58 at 3.3 V (bench)", 3 * V("rg58_pF_per_m") * 1e-12, 3.3),
        ("1 m RG-58 at 3.3 V (bench)", V("rg58_pF_per_m") * 1e-12, 3.3),
        ("10 cm PCB trace at 3.3 V", 0.1 * V("pcb_pF_per_m") * 1e-12, 3.3),
        ("MCU pin + pad at 3.3 V", V("c_pin_pad_F"), 3.3),
        ("HBM path, 'equivalent C' at 0.75 V (3.95 pJ)", hs["hbm_pJ"] * 1e-12 / (act * 0.75 ** 2), 0.75),
        ("on-chip wire 8 mm (HBM PHY -> SM) at 0.75 V", 8 * HOTSIDE["c_wire_pF_mm"] * 1e-12, 0.75),
        ("hot-side delivered, 'equivalent C' (0.37 pJ)", hs["near_pJ"] * 1e-12 / (act * 0.75 ** 2), 0.75),
        ("on-chip wire 1 mm at 0.75 V", HOTSIDE["c_wire_pF_mm"] * 1e-12, 0.75),
        ("hybrid bond + via stack at 0.75 V", HOTSIDE["C_bond_via_fF"] * 1e-15, 0.75),
        ("oxide storage node 0.15 fF at 0.6 V", 0.15e-15, 0.6),
    ]
    rows = []
    for name, cc, vv in ladder:
        rows.append((name, eng(cc, "F"), "%.2f V" % vv, eng(act * cc * vv * vv, "J")))
    table(["path", "C", "V", "E per bit = 0.5*C*V^2 (study convention)"], rows)
    print("Convention: the study's model charges activity 0.5 x C x V^2 per bit; strict accounting for random data "
          "gives 0.25 x C x V^2. The ratio between paths is what matters.")

    hr("E3.6  Where 0.37 vs 3.95 pJ/bit comes from (replicating models/hot-side-memory.py after red team)")
    print("Near tier read at the port: bitlines (%.1f fF local + %.0f fF global) x %.1f V x %.1f V swing = %.1f fJ "
          "per cell, + sense + wordline -> %.1f fJ/bit; local wire %.1f fJ; bond+via %.1f fJ; x2 periphery; "
          "+50 fJ controller = %.3f pJ"
          % (hs["c_rbl"], HOTSIDE["c_gbl_fF"], HOTSIDE["V_array"], HOTSIDE["dV_rbl_V"], hs["e_rbl_cell"],
             hs["e_cell_read_bit"], hs["e_local"], hs["e_bond"], hs["e_read"] / 1e3))
    print("2-bit write-verify at the port: %.3f pJ; 20%%-write mix: %.3f pJ" % (hs["e_write"] / 1e3,
                                                                             hs["e_mix"] / 1e3))
    print("Delivery wire: 0.5 x 0.2 pF/mm x 0.75^2 = %.2f fJ/bit/mm" % hs["e_wire_mm"])
    print("  hot-side delivered = %.3f + 3 mm x %.4f = %.3f pJ/bit" % (hs["e_mix"] / 1e3, hs["e_wire_mm"] / 1e3,
                                                                    hs["near_pJ"]))
    print("  HBM delivered      = 3.5 (PHY, REPORTED) + 8 mm x %.4f = %.3f pJ/bit" % (hs["e_wire_mm"] / 1e3,
                                                                                    hs["hbm_pJ"]))
    print("  ratio = %.1fx. The HBM 3.5 pJ is mostly the PHY + interposer + TSV path (SerDes, termination, clocking), "
          "not one wire's C*V^2: E3 tests the law, not that number." % (hs["hbm_pJ"] / hs["near_pJ"]))

    hr("E3.7  SPI to an external chip vs internal SRAM (qualitative)")
    c_sck = V("c_pin_pad_F") + V("c_spi_device_in_F") + 0.10 * V("jumper_pF_per_m") * 1e-12 + 2e-12
    e_bit_spi = (c_sck + 0.25 * c_sck) * v * v      # clock toggles every bit, data ~1/4 of bits rise
    p_spi_8mbps = e_bit_spi * 8e6
    e_bit_sram = V("sram_pJ_per_32b") * 1e-12 / 32
    print("SPI pins: C_SCK ~ C_MOSI ~ %s; E/bit = (C_SCK + 0.25 C_MOSI) V^2 = %s [ESTIMATE]"
          % (eng(c_sck, "F"), eng(e_bit_spi, "J")))
    print("At 8 Mbit/s: %s on 3.3 V = %s, ~%s at the 5 V USB input (85%% converter) -> visible on a 10 uA USB meter"
          % (eng(p_spi_8mbps, "W"), eng(p_spi_8mbps / v, "A"),
             eng(p_spi_8mbps / 5.0 / V("pico_buck_eff"), "A")))
    print("Internal SRAM: ~%s per bit [ESTIMATE] -> ~%.0fx less than the pins. A memory copy at 20 MB/s adds only ~%s "
          "-> at or below the meter's floor." % (eng(e_bit_sram, "J"), e_bit_spi / e_bit_sram,
                                                eng(e_bit_sram * 20e6 * 8 * 2 / 5.0 / V("pico_buck_eff"), "A")))
    return hs


# --------------------------------------------------------------------------------------------------------------
# Self-test
# --------------------------------------------------------------------------------------------------------------
def selftest():
    ok = True

    def check(name, cond):
        nonlocal ok
        print(("PASS  " if cond else "FAIL  ") + name)
        ok = ok and cond

    # charge conservation
    cs, cbl, vc, vp = 1e-9, 4.7e-9, 3.3, 1.65
    dv = charge_share_dv(vc, vp, cs, cbl)
    q_before = cs * vc + cbl * vp
    q_after = (cs + cbl) * (vp + dv)
    check("charge sharing conserves charge", abs(q_before - q_after) < 1e-21)
    check("dV(Cbl=Cs) = (V-Vpre)/2", abs(charge_share_dv(3.3, 1.65, 1e-9, 1e-9) - 0.825) < 1e-12)
    seq = repeated_reads(vc, vp, cs, cbl, 5)
    ratio = cs / (cs + cbl)
    check("repeated reads shrink by Cs/(Cs+Cbl)", all(abs(seq[k + 1] / seq[k] - ratio) < 1e-12 for k in range(4)))
    # Vt loss fixed point
    sn = sn_max_vt_loss(3.3, 3.3, 0.7, 0.0, 0.7)
    check("no body effect: Vsn = Vwl - Vth", abs(sn - 2.6) < 1e-6)
    sn9 = sn_max_vt_loss(9.0, 3.3, 0.7, 0.5, 0.7)
    check("boosted wordline passes the full bitline", abs(sn9 - 3.3) < 1e-9)
    # retention identity
    check("retention t = C dV / I", abs(retention_time(1e-9, 1.5, 1e-11) - 150.0) < 1e-9)
    # temperature model sanity
    d = doubling_interval(gen_leak_ratio)
    check("generation leakage doubles every 8-11 C near room temperature (got %.1f C)" % d, 8.0 < d < 11.0)
    # RC energy: supply gives C V^2, resistor gets half, independent of R
    for r in (33.0, 3300.0):
        es, eh = rc_charge_energy_numeric(100e-12, r, 3.3)
        ev = 100e-12 * 3.3 ** 2
        check("RC charge with R=%g: E_supply = CV^2 (%.4g vs %.4g J)" % (r, es, ev), abs(es / ev - 1) < 2e-3)
        check("RC charge with R=%g: E_R = CV^2/2" % r, abs(eh / (0.5 * ev) - 1) < 2e-3)
    # normal quantile
    check("norm_ppf(1e-4) = -3.719", abs(norm_ppf(1e-4) + 3.7190) < 1e-3)
    check("norm_ppf(0.5) = 0", abs(norm_ppf(0.5)) < 1e-9)
    # replicate the hot-side model numbers quoted in the dossier
    hs = hotside_energy()
    check("hot-side read at port 0.121 pJ (got %.3f)" % (hs["e_read"] / 1e3), abs(hs["e_read"] / 1e3 - 0.121) < 0.002)
    check("hot-side write at port 0.543 pJ (got %.3f)" % (hs["e_write"] / 1e3),
          abs(hs["e_write"] / 1e3 - 0.543) < 0.002)
    check("hot-side 20%%-write mix 0.206 pJ (got %.3f)" % (hs["e_mix"] / 1e3), abs(hs["e_mix"] / 1e3 - 0.206) < 0.002)
    check("hot-side delivered 0.374 pJ (got %.3f)" % hs["near_pJ"], abs(hs["near_pJ"] - 0.374) < 0.002)
    check("HBM delivered 3.95 pJ (got %.3f)" % hs["hbm_pJ"], abs(hs["hbm_pJ"] - 3.95) < 0.005)
    # lognormal order statistics: 2nd/1st ratio grows with sigma
    rng = np.random.default_rng(1)
    r1 = np.median(np.sort(rng.lognormal(0, 0.3, (5000, 16)), axis=1)[:, 1:2] /
                   np.sort(rng.lognormal(0, 0.3, (5000, 16)), axis=1)[:, 0:1])
    r2 = np.median(np.sort(rng.lognormal(0, 1.0, (5000, 16)), axis=1)[:, 1:2] /
                   np.sort(rng.lognormal(0, 1.0, (5000, 16)), axis=1)[:, 0:1])
    check("weak-cell gap grows with spread (%.2f < %.2f)" % (r1, r2), r1 < r2)
    print("SELFTEST " + ("PASSED" if ok else "FAILED"))
    return 0 if ok else 1


SOURCES = [
    ("RP2040 ADC ENOB 8.7", "https://pigweed.googlesource.com/third_party/github/raspberrypi/pico-sdk/+/"
     "d0c7642369b91c934b014134c862000eee1dbca4%5E%21", "[REPORTED]"),
    ("ALD1106 IDS(OFF), IGSS", "https://www.electronicsdatasheets.com/download/120482.pdf?format=pdf", "[DATASHEET]"),
    ("ALD1106 RDS(on) 500 Ohm, Vth 1 V listing", "https://www.lcsc.com/product-detail/C3289693.html", "[REPORTED]"),
    ("2N7000 IDSS, VGS(th), Ciss", "https://www.onsemi.com/download/data-sheet/pdf/2n7000-d.pdf", "[DATASHEET]"),
    ("LMC6482 input current, 3 V spec", "https://www.ti.com/product/LMC6482", "[DATASHEET]"),
    ("MCP6541/MCP6544 bias, supply", "https://futureelectronics.com/fr/p/semiconductors--analog--comparators/"
     "mcp6544-i-p-microchip-1851997", "[REPORTED]"),
    ("4117 JFET IGSS", "https://linearsystems.com/_files/ugd/7e8069_12949627a6794d63a612d89b494fc997.pdf",
     "[REPORTED]"),
    ("Coto 9000 reed relay IR", "https://cototechnology.com/library/cotoclassic-9000-series-reed-relay-datasheet.pdf",
     "[DATASHEET]"),
    ("KEMET C0G insulation resistance", "https://mfgdatasheets.nlight.net/Kemet%20C0G.pdf", "[DATASHEET]"),
    ("RG-58C/U 30.8 pF/ft", "https://www.fairviewmicrowave.com/content/dam/infinite-electronics/product-assets/"
     "fairview-microwave/product-datasheets/RG58CU-FT.pdf", "[DATASHEET]"),
    ("FNIRSI FNB58 resolution", "https://core-electronics.com.au/fnirsi-fnb58-usb-fast-charge-tester.html",
     "[REPORTED]"),
    ("imec 2T0C >200 s at 95 C", "https://imec-publications.be/entities/publication/"
     "948b2190-065d-48d2-a9b9-4f4ecd22c234", "[REPORTED] (via dossiers/hot-side-memory.md)"),
    ("hot-side energy model", "models/hot-side-memory.py (repo)", "[MODEL]"),
]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--selftest", action="store_true", help="run formula checks and exit 0/1")
    ap.add_argument("--section", choices=["e1", "e2", "e3"], help="print only one experiment")
    ap.add_argument("--seed", type=int, default=2026, help="Monte Carlo seed")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    rng = np.random.default_rng(args.seed)
    print("bench_calcs.py -- Track T1 expected numbers (prices/specs as of Nov 2026; see guides for sources)")
    if args.section in (None, "e1"):
        e1_tables(rng)
    if args.section in (None, "e2"):
        e2_tables()
    if args.section in (None, "e3"):
        e3_tables()
    if args.section is None:
        hr("SOURCES (also in each guide)")
        for name, url, tag in SOURCES:
            print("  %-40s %s %s" % (name, tag, url))
        hr("INPUTS")
        for k, (val, tag, note) in INPUTS.items():
            print("  %-26s %-12g %-13s %s" % (k, val, tag, note))
    return 0


if __name__ == "__main__":
    sys.exit(main())
