#!/usr/bin/env python3
"""
dram_cell_physics.py -- first-principles estimates for the NEW DRAM bottleneck map (phase A1).

Owner: A1-scaling (dram-moonshot). Written 2026-11-01. Pure standard library; run with `python3`.

What it computes:
  1. Cell area -> bits/mm^2 (6F2, 4F2, 3D tiers), calibrated to teardown die densities.
  2. Storage-capacitor capacitance from geometry (pillar/cylinder, height, EOT) and the k or
     height needed to hold a target capacitance.
  3. Charge-sharing sense signal vs bitline capacitance; minimum Cs for a given sense budget.
  4. Retention: maximum tail-cell leakage for a refresh interval; Ion/Ioff "decade budget".
  5. Refresh energy, refresh power per die/module, tRFC/tREFI time overhead.
  6. Activation overfetch energy (destructive read + page size).
  7. 3D DRAM tier economics (break-even tier count) and compound tier yield.
  8. HBM area/yield tax, interface power at accelerator bandwidths, row-hammer trend, EUV $/wafer.

Every input is tagged in INPUTS with its basis. [ESTIMATE] values are logged in
research/assumptions/A1-scaling.md; cited values are in research/sources/A1-scaling.jsonl and
research/phaseA/A1_scaling_limits.md.
"""

import math

EPS0 = 8.854e-12   # F/m
KB = 1.380649e-23  # J/K
Q_E = 1.602e-19    # C

# --------------------------------------------------------------------------------------------
# INPUTS
# --------------------------------------------------------------------------------------------
INPUTS = {
    # Teardown anchors (ram-venture cost_stack.md section 3.1, TechInsights via snippets)
    "die_1b_mm2": 35.83,          # Micron D1b 16Gb DDR5 [REPORTED-P]
    "die_cxmt_g4_mm2": 66.99,     # CXMT G4 16Gb DDR5 [REPORTED]
    "cell_cxmt_g4_um2": 0.0020,   # CXMT G4 cell area [REPORTED]
    "die_1c_mm2": 29.1,           # 1-gamma 16Gb, derived from Micron ">30% bits/wafer" [ESTIMATE]
    "user_gbit": 16.0,
    "ecc_factor": 1.0625,         # DDR5 on-die ECC 8 check bits per 128 [REPORTED, JESD79-5 per prior work]
    # Capacitor geometry [ESTIMATE: derived from cell pitch; see A1 md section 2]
    "cap_gap_nm": 14.0,           # pillar-to-pillar gap = 2 x ~5.5 nm dielectric + ~3 nm top TiN
    "cap_height_nm": 1300.0,      # storage-node height (AR ~60 at 1b)
    "eot_nm": 0.55,               # ZrO2-based stack, 6-7 nm physical (TechInsights/Choe) -> EOT ~0.5-0.6
    # Array electrical [ESTIMATE]
    "v_array": 1.05,              # bitline restore voltage (VARY), V
    "v_wl": 2.9,                  # boosted wordline high, V
    "cells_per_bl": 512,
    "c_bl_per_cell_fF": 0.06,     # BL capacitance contributed per attached cell (coupling-dominated)
    "c_bl_fixed_fF": 4.0,         # sense-amp + junction + mux
    "c_wl_per_cell_fF": 0.15,
    "pump_eff": 0.45,             # VPP charge-pump efficiency
    "reg_eff": 0.95,              # VARY regulator efficiency
    "periph_overhead": 2.0,       # multiplier for decode/control/timing energy around the array
    "dv_min_mV": 50.0,            # SA offset (after compensation) + coupling noise + guard
    # Timing [REPORTED]
    "t_ref_s": 0.064,             # JEDEC 64 ms (32 ms above 85 C)
    "trefi_ns": 3900.0,           # DDR5 tREFI <85 C (SQR/SK hynix-based datasheet via snippet)
    "trfc_16Gb_ns": 295.0,        # DDR5 16Gb tRFC1 (datasheet via snippet)
    "trfc_32Gb_ns": 410.0,        # [UNVERIFIED: training knowledge; not confirmed by search]
    "trfc_64Gb_ns": 1600.0,       # extrapolation in arXiv 1712.08304 (via snippet) -- DDR4-style tREFI basis
    # Module [ESTIMATE / prior work]
    "rdimm_dies": 40,             # 64GB RDIMM = 40 x 16Gb (ram-venture section 4.2)
    "rdimm_active_W": 12.0,       # [UNVERIFIED: training knowledge, 8-15 W class]
    "rdimm_idle_W": 3.0,          # [UNVERIFIED: training knowledge, 2-4 W class]
}

TEMP_K_HOT = 358.0     # 85 C
RET_HALVING_C = 10.0   # retention halves per ~10 C [ESTIMATE: Arrhenius-like GIDL/junction tail, rule of thumb]


def hr(title):
    print("\n" + "=" * 96)
    print(title)
    print("=" * 96)


# --------------------------------------------------------------------------------------------
# 1. Cell area -> density
# --------------------------------------------------------------------------------------------
def gbit_per_mm2(cell_um2, array_eff, tiers=1, bits_per_cell=1, ecc=INPUTS["ecc_factor"]):
    """User Gb/mm^2 (ECC bits removed)."""
    raw_bits_per_mm2 = 1e6 / cell_um2
    return raw_bits_per_mm2 * array_eff * tiers * bits_per_cell / ecc / 1e9


def array_efficiency(die_mm2, cell_um2, user_gbit=INPUTS["user_gbit"], ecc=INPUTS["ecc_factor"]):
    return user_gbit * ecc * 1e9 * cell_um2 * 1e-6 / die_mm2


def section_density():
    hr("1. CELL AREA -> DENSITY")
    I = INPUTS
    eff = array_efficiency(I["die_cxmt_g4_mm2"], I["cell_cxmt_g4_um2"])
    d_cx = I["user_gbit"] / I["die_cxmt_g4_mm2"]
    d_1b = I["user_gbit"] / I["die_1b_mm2"]
    d_1c = I["user_gbit"] / I["die_1c_mm2"]
    cell_1b = I["cell_cxmt_g4_um2"] * d_cx / d_1b
    cell_1c = I["cell_cxmt_g4_um2"] * d_cx / d_1c
    f_1b = math.sqrt(cell_1b / 6) * 1e3
    f_1c = math.sqrt(cell_1c / 6) * 1e3
    print(f"CXMT G4 array efficiency (cell 0.0020 um2, 66.99 mm2): {eff:.3f}")
    print(f"1b: die density {d_1b:.3f} Gb/mm2 -> implied cell {cell_1b*1e6:.0f} nm2 (6F2 at F={f_1b:.1f} nm)")
    print(f"1c: die density {d_1c:.3f} Gb/mm2 -> implied cell {cell_1c*1e6:.0f} nm2 (6F2 at F={f_1c:.1f} nm)")
    rows = [
        ("6F2 1b (calibrated)", cell_1b, eff, 1),
        ("6F2 1c (calibrated)", cell_1c, eff, 1),
        ("4F2 VCT at 1c F, same array eff", 4 * (f_1c * 1e-3) ** 2, eff, 1),
        ("4F2 VCT at 1c F, periphery-under-cell eff 0.70", 4 * (f_1c * 1e-3) ** 2, 0.70, 1),
        ("4F2 VCT at F=14.7 nm (= 6F2 area at 12 nm)", 4 * 0.0147 ** 2, 0.70, 1),
        ("OCTRAM demo 54x63 nm (Kioxia/Nanya)", 0.054 * 0.063, eff, 1),
        ("3D lateral 1T1C tier 50x600 nm, x32 tiers", 0.050 * 0.600, 0.55, 32),
        ("3D lateral tier 40x300 nm, x64 tiers", 0.040 * 0.300, 0.55, 64),
        ("IGZO 2T0C 30F2 at F=28 nm, 4 tiers", 30 * 0.028 ** 2, 0.45, 4),
    ]
    print(f"\n{'Cell option':52s} {'cell um2':>10s} {'eff':>5s} {'tiers':>5s} {'Gb/mm2':>8s} {'x 1b':>6s}")
    for name, a, e, t in rows:
        g = gbit_per_mm2(a, e, t)
        print(f"{name:52s} {a:10.5f} {e:5.2f} {t:5d} {g:8.3f} {g/d_1b:6.2f}")
    print("\n4F2 vs 6F2 pitch equivalence: same cell area at F4 = F6 * sqrt(6/4) = "
          f"{math.sqrt(6/4):.3f} x F6 (e.g. 12.0 nm 6F2 == {12.0*math.sqrt(1.5):.1f} nm 4F2)")
    return cell_1b, cell_1c, eff, d_1b


# --------------------------------------------------------------------------------------------
# 2. Capacitor
# --------------------------------------------------------------------------------------------
def hex_pitch_nm(cell_um2):
    """Honeycomb capacitor lattice: area per site = (sqrt(3)/2) p^2."""
    return math.sqrt(cell_um2 * 1e6 / (math.sqrt(3) / 2))


def cap_pillar_fF(d_nm, h_nm, eot_nm, double_sided=False):
    """Pillar: outer wall only. Cylinder (double_sided): outer + inner wall (inner diameter ~ d - 2*wall)."""
    area = math.pi * d_nm * h_nm
    if double_sided:
        area += math.pi * max(d_nm - 2 * 6.0, 0) * h_nm
    return 3.9 * EPS0 * area * 1e-18 / (eot_nm * 1e-9) * 1e15


def section_capacitor(cell_1b, cell_1c):
    hr("2. STORAGE CAPACITOR")
    I = INPUTS
    out = {}
    for node, cell in (("1a-class (cell 0.0015 um2)", 0.0015), ("1b", cell_1b), ("1c", cell_1c),
                       ("4F2 at F=14.7 nm", 4 * 0.0147 ** 2), ("next (cell 0.0006 um2)", 0.0006)):
        p = hex_pitch_nm(cell)
        d = p - I["cap_gap_nm"]
        c = cap_pillar_fF(d, I["cap_height_nm"], I["eot_nm"])
        ar = I["cap_height_nm"] / d
        h7 = 7.0 / c * I["cap_height_nm"]
        eot7 = I["eot_nm"] * c / 7.0
        print(f"{node:28s} pitch {p:5.1f} nm  pillar d {d:5.1f} nm  AR {ar:5.1f}  C {c:5.2f} fF | "
              f"for 7 fF: h {h7:6.0f} nm (AR {h7/d:5.0f}) or EOT {eot7:.2f} nm (k {6.5*3.9/eot7:4.0f} @6.5nm)")
        out[node] = (d, c)
    # Charge and electrons
    c1b = out["1b"][1]
    q = c1b * 1e-15 * I["v_array"] / 2
    print(f"\n1b stored signal charge (C x VARY/2): {q*1e15:.2f} fC = {q/Q_E:,.0f} electrons")
    # kT/C noise on bitline vs margin
    cbl = INPUTS["cells_per_bl"] * INPUTS["c_bl_per_cell_fF"] + INPUTS["c_bl_fixed_fF"]
    ktc = math.sqrt(KB * TEMP_K_HOT / (cbl * 1e-15)) * 1e3
    print(f"kT/C noise on a {cbl:.1f} fF bitline at 85 C: {ktc:.2f} mV rms (vs ~50 mV sense budget) -> "
          "noise floor is NOT thermodynamic; it is device mismatch and coupling")
    # Short capacitor for 3D tiers
    for h in (300, 500):
        for eot in (0.55, 0.30):
            c = cap_pillar_fF(20.0, h, eot)
            print(f"short pillar d=20 nm h={h} nm EOT={eot} nm -> {c:4.2f} fF")
    return out


# --------------------------------------------------------------------------------------------
# 3. Sense margin
# --------------------------------------------------------------------------------------------
def c_bitline_fF(n_cells):
    return n_cells * INPUTS["c_bl_per_cell_fF"] + INPUTS["c_bl_fixed_fF"]


def sense_signal_mV(cs, cbl, v_cell, v_pre):
    return (v_cell - v_pre) * cs / (cs + cbl) * 1e3


def cs_min_fF(cbl, dv_min_mV, v_sig):
    dv = dv_min_mV / 1e3
    return cbl * dv / (v_sig - dv)


def section_sense(c1b):
    hr("3. SENSE MARGIN vs BITLINE CAPACITANCE")
    I = INPUTS
    vpre = I["v_array"] / 2
    print(f"VARY {I['v_array']} V, precharge {vpre:.3f} V, required end-of-retention signal {I['dv_min_mV']} mV")
    cbl = c_bitline_fF(I["cells_per_bl"])
    v1min = vpre + I["dv_min_mV"] / 1e3 * (c1b + cbl) / c1b
    droop = I["v_array"] - v1min
    f = droop / I["v_array"]
    print(f"At 512 cells/BL and Cs={c1b:.2f} fF: a stored '1' may droop to {v1min:.3f} V "
          f"(allowed droop {droop*1e3:.0f} mV, {f*100:.0f}% of VARY)")
    print(f"\n{'cells/BL':>8s} {'Cbl fF':>7s} {'Cbl/Cs':>7s} {'fresh dV mV':>12s} "
          f"{'Cs_min fF (droop ' + format(f*100, '.0f') + '%)':>22s} {'Cs_min fF (droop 0)':>20s}")
    vs_f = (1 - f) * I["v_array"] - vpre
    for n in (1024, 512, 256, 128, 64, 32):
        cb = c_bitline_fF(n)
        fresh = sense_signal_mV(c1b, cb, I["v_array"], vpre)
        print(f"{n:8d} {cb:7.1f} {cb/c1b:7.2f} {fresh:12.1f} {cs_min_fF(cb, I['dv_min_mV'], vs_f):22.2f} "
              f"{cs_min_fF(cb, I['dv_min_mV'], vpre):20.2f}")
    # Array-voltage floor: VARY needed for the same margin and the same fractional droop allowance
    print()
    for cs in (c1b, c1b / 2, 1.0):
        vneed = I["dv_min_mV"] / 1e3 * (cs + cbl) / cs / (0.5 - f)
        print(f"Cs {cs:4.2f} fF at Cbl {cbl:.0f} fF needs VARY >= {vneed:4.2f} V for the same margin and droop allowance")
    for n in (128, 64):
        cb = c_bitline_fF(n)
        vneed = I["dv_min_mV"] / 1e3 * (c1b + cb) / c1b / (0.5 - f)
        print(f"Cs {c1b:4.2f} fF at {n} cells/BL (Cbl {cb:.1f} fF) needs only VARY >= {vneed:4.2f} V "
              f"-> array CV^2 energy x{(vneed/I['v_array'])**2:.2f} on top of the smaller Cbl")
    return droop


# --------------------------------------------------------------------------------------------
# 4. Retention, leakage, decade budget
# --------------------------------------------------------------------------------------------
def section_retention(c1b, droop):
    hr("4. RETENTION, LEAKAGE AND THE Ion/Ioff DECADE BUDGET")
    I = INPUTS
    q_allow = c1b * 1e-15 * droop
    for t, label in ((0.064, "64 ms (<85 C)"), (0.032, "32 ms (85-95 C)"), (1.0, "1 s"), (10.0, "10 s"),
                     (3600.0, "1 h")):
        print(f"max tail-cell leakage for {label:16s}: {q_allow/t*1e15:10.4f} fA")
    n_cells = I["user_gbit"] * I["ecc_factor"] * 1e9
    z = 6.4
    print(f"A 16Gb die has {n_cells:.2e} cells; the weakest cell sits near the {z}-sigma tail of the "
          "retention distribution [ESTIMATE: 1-in-1.7e10 ~ 6.4 sigma one-sided]")
    # decade budget
    for ion_uA, ioff_fA, ss in ((20, 17, 95), (20, 1, 95), (20, 1e-3, 95), (5, 1e-3, 95), (20, 17, 72)):
        dec = math.log10(ion_uA * 1e-6 / (ioff_fA * 1e-15))
        print(f"Ion {ion_uA:>3} uA / Ioff {ioff_fA:>7} fA = {dec:5.2f} decades x {ss} mV/dec = "
              f"{dec*ss/1e3:4.2f} V gate swing (ideal SS at 85 C = {60*TEMP_K_HOT/300:.1f} mV/dec)")
    # temperature
    for tc in (85, 95, 105, 125):
        f = 2 ** ((tc - 85) / RET_HALVING_C)
        print(f"at {tc:3d} C retention shrinks ~{f:4.1f}x vs 85 C -> refresh every {64/f:5.1f} ms for Si cells")
    # oxide-semiconductor contrast (Kioxia OCTRAM Ioff < 1 aA per prior card A1-04)
    t_igzo = q_allow / 1e-18
    print(f"IGZO access device at Ioff = 1 aA: retention ~{t_igzo:,.0f} s (~{t_igzo/3600:.1f} h) for the same Cs and droop "
          "[ESTIMATE; ignores Vt shift and SN junction leakage]")


# --------------------------------------------------------------------------------------------
# 5. Refresh energy and time
# --------------------------------------------------------------------------------------------
def refresh_energy_per_bit_fJ(n_cells_per_bl=None):
    I = INPUTS
    n = n_cells_per_bl or I["cells_per_bl"]
    cbl = c_bitline_fF(n) * 1e-15
    e_bl = cbl * I["v_array"] ** 2 / 2 / I["reg_eff"]
    e_wl = I["c_wl_per_cell_fF"] * 1e-15 * I["v_wl"] ** 2 / I["pump_eff"]
    return (e_bl + e_wl) * I["periph_overhead"] * 1e15, e_bl * 1e15, e_wl * 1e15


def section_refresh():
    hr("5. REFRESH ENERGY, POWER AND TIME")
    I = INPUTS
    e, e_bl, e_wl = refresh_energy_per_bit_fJ()
    print(f"energy per refreshed bit: BL {e_bl:.1f} fJ + WL {e_wl:.1f} fJ, x{I['periph_overhead']} periphery = {e:.0f} fJ")
    bits = I["user_gbit"] * I["ecc_factor"] * 1e9
    for t in (0.064, 0.032):
        p_die = bits * e * 1e-15 / t
        p_mod = p_die * I["rdimm_dies"]
        print(f"refresh at {t*1e3:.0f} ms: {p_die*1e3:5.1f} mW per 16Gb die, {p_mod:4.2f} W per 64GB RDIMM "
              f"({p_mod/I['rdimm_active_W']*100:4.1f}% of ~{I['rdimm_active_W']:.0f} W active, "
              f"{p_mod/I['rdimm_idle_W']*100:4.0f}% of ~{I['rdimm_idle_W']:.0f} W idle)")
    for name, trfc in (("16Gb", I["trfc_16Gb_ns"]), ("32Gb", I["trfc_32Gb_ns"])):
        print(f"DDR5 {name}: tRFC {trfc:.0f} ns / tREFI {I['trefi_ns']:.0f} ns = {trfc/I['trefi_ns']*100:4.1f}% "
              f"of time unavailable (all-bank); {2*trfc/I['trefi_ns']*100:4.1f}% above 85 C")
    print(f"64Gb (extrapolated tRFC {I['trfc_64Gb_ns']:.0f} ns, source context tREFI 7.8 us): "
          f"{I['trfc_64Gb_ns']/7800*100:4.1f}% of time; DDR5's 3.9 us tREFI would double that unless per-bank/"
          "same-bank refresh hides it")
    # world-scale refresh power, illustrative
    print("Retention x16 (1 s worst-case) cuts refresh energy and time 16x; x160 (10 s) makes refresh <1% of idle power")
    return e


# --------------------------------------------------------------------------------------------
# 6. Activation overfetch
# --------------------------------------------------------------------------------------------
def section_activation(e_bit_fJ):
    hr("6. DESTRUCTIVE READ + PAGE OVERFETCH (core access energy)")
    # A row activation restores every cell in the page; the controller wants 64 B (+ECC)
    e_restore = e_bit_fJ  # same physics as refresh per bit
    cases = [
        ("DDR5 RDIMM subchannel: 10 x4 dies x 1 KB page, 1 line/ACT", 10 * 8192, 640, 1),
        ("DDR5 same, 4 lines/ACT (open-page hits)", 10 * 8192, 640, 4),
        ("HBM pseudo-channel 1 KB page, 32 B/access, 8 access/ACT", 8192, 256, 8),
        ("HBM streaming, 32 accesses/ACT", 8192, 256, 32),
        ("Hypothetical 64 B sub-page activation, 1 line/ACT", 640, 640, 1),
    ]
    for name, page_bits, line_bits, hits in cases:
        e_per_bit = page_bits * e_restore / (line_bits * hits) / 1e3
        print(f"{name:62s} overfetch {page_bits/(line_bits*hits):6.1f}x -> {e_per_bit:5.2f} pJ/useful bit")
    print("cross-check: RPU paper (arXiv 2602.18568) models HBM row activation at ~0.18 pJ/bit for streaming")


# --------------------------------------------------------------------------------------------
# 7. 3D DRAM tier economics
# --------------------------------------------------------------------------------------------
def section_3d(d_1b):
    hr("7. 3D DRAM TIER ECONOMICS")
    wafer_2d = 3800.0          # ram-venture canonical 1b wafer
    cost_per_gb_area_2d = wafer_2d / d_1b
    scenarios = {
        # name: (tier footprint um2, array eff, base wafer $, $ per tier)
        "optimistic (40x300 nm cell, $20/tier)": (0.040 * 0.300, 0.60, 2800.0, 20.0),
        "base (50x600 nm cell, $30/tier)": (0.050 * 0.600, 0.55, 3000.0, 30.0),
        "pessimistic (60x1000 nm cell, $45/tier)": (0.060 * 1.000, 0.50, 3400.0, 45.0),
    }
    for name, (fp, eff, base, ct) in scenarios.items():
        dt = gbit_per_mm2(fp, eff)
        n_dens = d_1b / dt
        denom = cost_per_gb_area_2d * dt - ct
        n_cost = base / denom if denom > 0 else float("inf")
        print(f"{name:42s} {dt:6.4f} Gb/mm2/tier | density break-even {n_dens:5.1f} tiers | "
              f"cost break-even {n_cost:5.1f} tiers")
        for n in (32, 64, 128):
            dens = dt * n
            cost_rel = ((base + ct * n) / dens) / cost_per_gb_area_2d
            print(f"      {n:4d} tiers: {dens:5.2f} Gb/mm2 ({dens/d_1b:4.1f}x 1b), $/bit {cost_rel:4.2f}x 1b "
                  "(before tier yield)")
    # compound yield
    y5 = 0.561
    yt = y5 ** (1 / 5)
    print(f"\nSK hynix 5-tier test wafer 56.1% -> implied per-tier yield {yt:.3f} if tiers were independent and unrepaired")
    for yt_ in (yt, 0.99, 0.998, 0.9995):
        print(f"  per-tier yield {yt_:.4f}: 32 tiers {yt_**32*100:7.3f}%  64 tiers {yt_**64*100:7.3f}%  "
              f"128 tiers {yt_**128*100:7.3f}%")
    print("=> 3D DRAM needs NAND-like defect tolerance (row/column repair per tier, ECC) so that a defect kills a "
          "block, not a die; per-tier killer-defect probability must be <~0.1-0.2%.")


# --------------------------------------------------------------------------------------------
# 8. HBM, interface power, row hammer, EUV
# --------------------------------------------------------------------------------------------
def section_system():
    hr("8. HBM TAX, INTERFACE POWER, ROW HAMMER, EUV")
    # HBM tax
    for die_pen in (1.35, 1.45):
        for ylow in (0.20, 0.30):
            print(f"HBM die +{(die_pen-1)*100:.0f}% area, yield -{ylow*100:.0f}% -> "
                  f"{die_pen/(1-ylow):4.2f}x wafer per good bit (vs Micron's ~3x for HBM3E, Hot Chips 2026)")
    # Interface power
    print()
    for name, bw_TBps, pj in (("H200-class 4.8 TB/s @3.5 pJ/b", 4.8, 3.5), ("B200-class 8 TB/s @3.5 pJ/b", 8.0, 3.5),
                              ("HBM4 8 stacks x 2 TB/s @3.5 pJ/b", 16.0, 3.5),
                              ("same 16 TB/s @1.3 pJ/b (3D, no interposer)", 16.0, 1.3),
                              ("same 16 TB/s @0.4 pJ/b (I/O-only floor quoted)", 16.0, 0.4),
                              ("DDR5 host 0.5 TB/s @15 pJ/b", 0.5, 15.0)):
        p = bw_TBps * 1e12 * 8 * pj * 1e-12
        print(f"{name:46s} -> {p:6.0f} W")
    print("HBM at full bandwidth on a ~1,000 W accelerator: ~22%; at 700 W H200: ~19% [ESTIMATE]")
    # HBM stack power from first principles
    for gbps in (8.0, 10.0):
        bw = 2048 * gbps / 8  # GB/s
        p = bw * 1e9 * 8 * 3.5e-12
        print(f"HBM4 stack 2048 b x {gbps} Gb/s = {bw/1000:.2f} TB/s -> {p:4.0f} W at 3.5 pJ/b")
    # Row hammer trend
    print()
    pts = {2014: 139e3, 2020: 4.8e3, 2022: 3.2e3}
    r = (pts[2022] / pts[2014]) ** (1 / 8)
    r2 = (3.2e3 / 69.2e3) ** (1 / 10)
    for yr in (2024, 2026, 2028):
        print(f"HCfirst extrapolation {yr}: {pts[2022]*r**(yr-2022):6.0f} (2014-22 fit, {r:.2f}/yr) .. "
              f"{pts[2022]*r2**(yr-2022):6.0f} (2012-22 fit, {r2:.2f}/yr)  [ESTIMATE, not measured]")
    # EUV
    print()
    for layers in (1, 5, 7, 10):
        lo, base, hi = 115 * layers, 165 * layers, 270 * layers
        print(f"EUV {layers:2d} layers: ${lo:,}-{hi:,} per wafer (base ${base:,}) = {base/4308*100:4.1f}% of a $4,308 "
              "1c wafer before netting DUV steps removed")


def main():
    cell_1b, cell_1c, eff, d_1b = section_density()
    caps = section_capacitor(cell_1b, cell_1c)
    c1b = caps["1b"][1]
    droop = section_sense(c1b)
    section_retention(c1b, droop)
    e = section_refresh()
    section_activation(e)
    section_3d(d_1b)
    section_system()
    hr("DONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
