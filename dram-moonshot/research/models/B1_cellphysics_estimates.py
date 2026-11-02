#!/usr/bin/env python3
"""
B1_cellphysics_estimates.py -- first-principles arithmetic behind the phase-B "NEW CELL PHYSICS" idea cards
(dram-moonshot, lens B1). Owner: B1-cellphysics. Written 2026-11-01. Pure standard library; python3 exits 0.

Feeds research/phaseB/B1-cellphysics.json and B1-cellphysics_notes.md. Tags:
  [A1]       reused from models/dram_cell_physics.py (imported, not copied) or A1_scaling_limits.md
  [A3]       reused from research/models/A3_frontier_estimates.py / A3_research_frontier.md
  [REPORTED] number from a search snippet logged in research/sources/B1-cellphysics.jsonl
  [ESTIMATE] my assumption, logged in research/assumptions/B1-cellphysics.md

One section per idea card (B1-01 ... B1-20). Each prints the numbers quoted in the card's
"first_principles_estimate" field.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "models")))
import dram_cell_physics as A1  # noqa: E402  (sibling model: helpers only, main() is guarded)

EPS0 = 8.854e-12
Q_E = 1.602e-19
KB = 1.380649e-23
H_PLANCK = 6.626e-34
HBAR = 1.0546e-34
M_E = 9.109e-31
T_HOT = 358.0  # 85 C

# ------------------------------------------------------------------------------------------------
# Shared anchors [A1]
# ------------------------------------------------------------------------------------------------
CELL_1B_UM2 = 0.00107
D_1B = 16.0 / A1.INPUTS["die_1b_mm2"]            # 0.447 Gb/mm2 die-level
EFF_1B = 0.508                                    # A1/A3 array efficiency
PILLAR_D_NM = 21.1                                # 1b pillar diameter [A1]
CS_1B = A1.cap_pillar_fF(PILLAR_D_NM, 1300.0, 0.55)
VARY = A1.INPUTS["v_array"]
CBL_512 = A1.c_bitline_fF(512)
Q_SIG_1B_fC = CS_1B * VARY / 2                    # signal charge vs mid-rail reference
REFRESH_FJ_PER_BIT = A1.refresh_energy_per_bit_fJ()[0]
CELLS_16GB = 16e9 * A1.INPUTS["ecc_factor"]


def hr(t):
    print("\n" + "=" * 100)
    print(t)
    print("=" * 100)


def pillar_height_for_charge_nm(q_fC, sigma_uC_cm2, d_nm=PILLAR_D_NM):
    """Height of a single-sided pillar (outer wall) that holds q_fC at areal signal charge sigma."""
    sigma = sigma_uC_cm2 * 1e-2  # C/m2
    wall_per_nm = math.pi * d_nm * 1e-9 * 1e-9  # m2 per nm of height
    return q_fC * 1e-15 / (sigma * wall_per_nm)


def density_gb_mm2(cell_um2, eff=EFF_1B, bits=1, tiers=1):
    return A1.gbit_per_mm2(cell_um2, eff, tiers, bits)


def anchors():
    hr("0. ANCHORS (A1 model)")
    print(f"1b die density {D_1B:.3f} Gb/mm2; 1b pillar Cs {CS_1B:.2f} fF (d {PILLAR_D_NM} nm, h 1300 nm, EOT 0.55 nm)")
    print(f"Cbl(512 cells) {CBL_512:.1f} fF; signal charge Cs*VARY/2 = {Q_SIG_1B_fC:.2f} fC "
          f"= {Q_SIG_1B_fC*1e-15/Q_E:,.0f} e-")
    sig_lin = 3.9 * EPS0 / 0.55e-9 * (VARY / 2) * 1e2  # uC/cm2 of signal charge on the wall
    print(f"areal signal charge of today's wall (EOT 0.55 nm, swing VARY/2): {sig_lin:.2f} uC/cm2")
    print(f"refresh energy per bit-refresh {REFRESH_FJ_PER_BIT:.0f} fJ")
    return sig_lin


# ------------------------------------------------------------------------------------------------
# B1-01 Antiferroelectric ZrO2 stub ("AFE charge reservoir")
# ------------------------------------------------------------------------------------------------
def b1_01(sig_lin):
    hr("B1-01 ANTIFERROELECTRIC ZrO2 STUB: field-induced polarization as signal charge")
    # Linear part of an AFE film (k~35-40 below switching) over the read swing
    k_afe, t_afe = 38.0, 6.0      # [ESTIMATE] ZrO2 AFE film, nm
    v1, vpre = 1.3, 0.35          # [ESTIMATE] write-1 level above forward switching; low precharge below backward switching
    sig_linpart = k_afe * EPS0 / (t_afe * 1e-9) * (v1 - vpre) * 1e2
    for p_ind, f_use in ((15, 0.5), (20, 0.6), (25, 0.7)):  # uC/cm2 induced polarization [ESTIMATE range]
        sig = p_ind * f_use + sig_linpart / 2  # half of linear swing is differential signal vs reference
        h = pillar_height_for_charge_nm(Q_SIG_1B_fC, sig)
        print(f"P_ind {p_ind} uC/cm2, usable {f_use:.0%}: signal {sig:5.1f} uC/cm2 = {sig/sig_lin:4.1f}x today's wall "
              f"-> pillar for 1b-equal signal charge {h:5.0f} nm (vs 1300 nm, AR {h/PILLAR_D_NM:4.1f} vs 62)")
    # Plateau effect: leakage drains polarization at ~constant voltage before the node droops
    lin_droop_budget = 0.155 * CS_1B  # fC, A1's allowed droop * Cs
    for p_ind in (15, 20):
        q_res = p_ind * 0.5 * 1e-2 * math.pi * PILLAR_D_NM * 1e-9 * 300e-9 * 1e15  # 300 nm stub, fC
        print(f"300 nm AFE stub, P_ind {p_ind}: reservoir {q_res:.1f} fC vs linear droop budget {lin_droop_budget:.2f} fC "
              f"-> retention stretch up to ~{(q_res+lin_droop_budget)/lin_droop_budget:.0f}x if the backward branch is sharp")
    # Endurance need
    ten_yr = 10 * 3.156e7
    print(f"refresh-only cycles in 10 yr at 64 ms: {ten_yr/0.064:.1e}; at 1 s refresh: {ten_yr:.1e}")
    print(f"hot row at 1 activate/us for 5 yr: {5*3.156e7*1e6:.1e} cycles -> AFE must reach 1e12-1e15 "
          "(only '1' writes/reads of '1' cycle the transition)")


# ------------------------------------------------------------------------------------------------
# B1-02 Negative-capacitance stub
# ------------------------------------------------------------------------------------------------
def b1_02():
    hr("B1-02 NEGATIVE-CAPACITANCE (FE/DE) STUB: enhancement vs stability margin")
    for r in (0.3, 0.5, 0.6, 0.7, 0.8):
        print(f"r = C_DE/|C_FE| = {r:.1f}: C_total/C_DE = {1/(1-r):4.2f}x")
    # Curie-Weiss drift: |C_FE| ~ 1/(T0 - T); r ~ (T0 - T). Design so r <= 0.85 at the coldest corner.
    t0_c = 450.0  # [ESTIMATE] effective Curie-Weiss temperature for HZO-class films
    r_cold = 0.85
    for tc in (-10, 25, 85, 125):
        r = r_cold * (t0_c - tc) / (t0_c - (-10))
        print(f"T {tc:4d} C: r {r:4.2f} -> enhancement {1/(1-r):4.2f}x")
    print("=> robust window ~2-4x at hot corners if r_cold is held at 0.85 (multi-domain hysteresis is the risk)")
    for enh in (2.0, 3.0):
        print(f"enhancement {enh:.0f}x -> pillar {1300/enh:.0f} nm for the same Cs")


# ------------------------------------------------------------------------------------------------
# B1-03 IGZO gated-diode ("CCD-well") storage on a 3D tier strip
# ------------------------------------------------------------------------------------------------
def b1_03():
    hr("B1-03 IGZO GATED-DIODE STORAGE: plate-driven complete charge transfer")
    eot_mos = 1.1   # [ESTIMATE] HfO2/ZrO2 gate EOT ~0.8 nm + accumulation-layer centroid ~0.3 nm
    v_pl_swing, vt = 2.5, 0.5   # [ESTIMATE] row-shared plate line swing and flat-band/threshold offset
    vary_low = 0.45
    gain = (v_pl_swing - vt) / VARY
    print(f"signal-charge gain vs linear cap at equal C (plate {v_pl_swing} V swing, VARY {VARY} V): {gain:.1f}x "
          "(IBM gated diode reported ~3.1-4)")
    per_area_vs_dram = (0.55 / eot_mos) * gain
    print(f"net signal per um2 of wall vs today's EOT-0.55 linear wall: {per_area_vs_dram:.1f}x")
    # 3D tier version: GAA strip 40 nm wide x 10 nm IGZO, plate length L
    perim_nm = 2 * (40 + 10)
    for lp in (100, 150, 200):
        c_gd = 3.9 * EPS0 * perim_nm * lp * 1e-18 / (eot_mos * 1e-9) * 1e15
        q1 = c_gd * (v_pl_swing - vt)       # fC, full well
        cbl = A1.c_bitline_fF(64)
        dv = q1 / 2 / cbl * 1e3             # vs mid reference, complete transfer
        print(f"plate length {lp} nm: C_gd {c_gd:.2f} fF, full well {q1:.2f} fC ({q1*1e-15/Q_E:,.0f} e-), "
              f"signal on 64-cell local BL ({cbl:.1f} fF) {dv:4.0f} mV")
    # Tier footprint and break-even tiers (A1 base economics, simplified to density break-even)
    for name, fp in (("A1 base lateral 1T1C 50x600 nm", 0.050 * 0.600), ("gated-diode strip 70x230 nm", 0.070 * 0.230),
                     ("gated-diode strip 60x180 nm", 0.060 * 0.180)):
        dt = A1.gbit_per_mm2(fp, 0.55)
        print(f"{name:34s}: {dt:.4f} Gb/mm2/tier -> density break-even with 1b at {D_1B/dt:4.1f} tiers")
    e_bl_low = A1.c_bitline_fF(64) * 1e-15 * vary_low ** 2 * 1e15
    e_pl = 0.6e-15 * v_pl_swing ** 2 * 1e15
    print(f"energy/bit: local BL at {vary_low} V {e_bl_low:.1f} fJ + plate {e_pl:.1f} fJ vs today's BL "
          f"{CBL_512*VARY**2:.0f} fJ (CV^2)")


# ------------------------------------------------------------------------------------------------
# B1-04 Charge-transfer pre-sensing on a long bitline (Cs shrink without shortening the bitline)
# ------------------------------------------------------------------------------------------------
def b1_04():
    hr("B1-04 CHARGE-TRANSFER PRE-SENSE: sub-fF cell on a 512-cell bitline")
    cbl = CBL_512
    c_sn = 1.5     # [ESTIMATE] sense node incl. transfer-gate parasitics, fF
    i_bias = 100e-9  # [ESTIMATE] transfer gate at its own threshold (self-biased precharge)
    n_ss = 1.3
    gm = i_bias / (n_ss * KB * T_HOT / Q_E)
    tau = cbl * 1e-15 / gm
    print(f"subthreshold transfer gm {gm*1e6:.2f} uS -> tau = Cbl/gm = {tau*1e9:.1f} ns")
    for t_ns in (20, 30, 45):
        eta = 1 - math.exp(-t_ns * 1e-9 / tau)
        print(f"  after {t_ns} ns: transfer efficiency {eta:.3f}")
    eta = 1 - math.exp(-30e-9 / tau)
    print(f"\n{'Cs fF':>6s} {'conventional dV mV':>19s} {'CT dV on SN mV':>15s} {'pillar nm':>10s} {'electrons':>10s}")
    for cs in (5.4, 2.0, 1.0, 0.5, 0.3):
        conv = A1.sense_signal_mV(cs, cbl, VARY, VARY / 2)
        ct = cs * (VARY / 2) * eta / c_sn * 1e3
        h = 1300 * cs / CS_1B
        print(f"{cs:6.1f} {conv:19.1f} {ct:15.0f} {h:10.0f} {cs*1e-15*VARY/2/Q_E:10,.0f}")
    print("conventional needs >=50 mV after droop; CT target >=100 mV on SN leaves room for transfer-gate mismatch")
    for cs in (0.5, 0.3):
        t_ret = cs * 1e-15 * 0.15 / 1e-18
        print(f"Cs {cs} fF with IGZO Ioff 1 aA, 150 mV droop: retention {t_ret:.0f} s")
    print(f"kT/C on SN: {math.sqrt(KB*T_HOT/(c_sn*1e-15))*1e3:.1f} mV rms")


# ------------------------------------------------------------------------------------------------
# B1-05 Multi-level 1T1C on an oxide channel
# ------------------------------------------------------------------------------------------------
def b1_05():
    hr("B1-05 2-BIT/CELL 1T1C ON AN IGZO ACCESS DEVICE")
    for n in (512, 128, 64):
        cbl = A1.c_bitline_fF(n)
        s1 = A1.sense_signal_mV(CS_1B, cbl, VARY, VARY / 2)
        s2 = (VARY / 6) * CS_1B / (CS_1B + cbl) * 1e3
        print(f"{n:4d} cells/BL (Cbl {cbl:5.1f} fF): 1-bit signal {s1:5.0f} mV; 2-bit level-edge signal {s2:4.0f} mV")
    droop_rate = 1e-18 / (CS_1B * 1e-15) * 1e3  # mV/s at 1 aA
    print(f"IGZO 1 aA leakage: droop {droop_rate:.2f} mV/s -> 15 mV level budget lasts {15/droop_rate:.0f} s")
    for eff in (EFF_1B, 0.45, 0.70):
        print(f"2 b/cell at 1b cell, array eff {eff:.2f}: {density_gb_mm2(CELL_1B_UM2, eff, 2):.2f} Gb/mm2 "
              f"({density_gb_mm2(CELL_1B_UM2, eff, 2)/D_1B:.2f}x 1b)")


# ------------------------------------------------------------------------------------------------
# B1-06 Vertical oxide semi-floating-gate 1T1D gain cell
# ------------------------------------------------------------------------------------------------
def b1_06():
    hr("B1-06 VERTICAL OXIDE SEMI-FLOATING-GATE (1T + Schottky/MIS diode) GAIN CELL")
    a_star = 41.0  # A/cm2K2, Richardson constant for m* ~0.34 [ESTIMATE]
    area_cm2 = (20e-7) ** 2
    c_fg, dv = 0.3e-15, 0.2
    for phi in (0.8, 0.9, 1.0, 1.1):
        for tk in (358.0, 398.0):
            j = a_star * tk ** 2 * math.exp(-phi * Q_E / (KB * tk))
            i = j * area_cm2
            t = c_fg * dv / i
            print(f"barrier {phi:.1f} eV at {tk-273:.0f} C: reverse J {j:.1e} A/cm2, I {i:.1e} A -> retention {t:.1e} s")
    for f_nm in (20, 40):
        for kf2 in (4, 10):
            cell = kf2 * (f_nm * 1e-3) ** 2
            d = density_gb_mm2(cell)
            print(f"{kf2:2d}F2 at F={f_nm} nm: {d:.3f} Gb/mm2/tier -> b x N for 1b parity {D_1B/d:4.1f}")


# ------------------------------------------------------------------------------------------------
# B1-07 Tunnel-diode (NDR) latch cell
# ------------------------------------------------------------------------------------------------
def b1_07():
    hr("B1-07 1T + 2 NDR-DIODE LATCH (refresh-free static cell)")
    p_refresh_die = CELLS_16GB * REFRESH_FJ_PER_BIT * 1e-15 / 0.064
    print(f"16Gb die refresh power at 64 ms: {p_refresh_die*1e3:.1f} mW")
    v = 0.5
    area_cm2 = (25e-7) ** 2
    for label, p_die in (("match refresh power", p_refresh_die), ("4x refresh power (= ~1/3 of idle RDIMM share)", 4 * p_refresh_die)):
        i_cell = p_die / CELLS_16GB / v
        print(f"{label}: valley current <= {i_cell*1e12:.2f} pA/cell -> J_valley <= {i_cell/area_cm2:.2f} A/cm2 "
              f"(25 nm diode); at PVCR 5 J_peak {5*i_cell/area_cm2:.1f} A/cm2")
    for label, p_cell in (("TI RTD/HFET gain cell (EDL 1998, ~50 nW/cell)", 50e-9), ("InP RTD 'nA operation' (~0.5 nW)", 0.5e-9)):
        print(f"{label}: 16Gb die standby {p_cell*CELLS_16GB:,.0f} W -> {p_cell/(p_refresh_die/CELLS_16GB):,.0f}x too high")
    print(f"refresh removed: tRFC/tREFI availability loss 7.6% (16Gb) -> 0; refresh energy {REFRESH_FJ_PER_BIT:.0f} fJ/bit -> 0")


# ------------------------------------------------------------------------------------------------
# B1-08 Vertical oxide CCD string memory
# ------------------------------------------------------------------------------------------------
def b1_08():
    hr("B1-08 VERTICAL OXIDE CCD STRING (3D-NAND-like stack, no per-bit transistor)")
    hole_pitch_nm = 150.0
    a_hole = (math.sqrt(3) / 2) * hole_pitch_nm ** 2 * 1e-6  # um2 per hole (hex)
    for planes, gpb in ((128, 2), (256, 2), (256, 3)):
        bits = planes / gpb
        d = 1e6 / a_hole * bits * 0.60 / A1.INPUTS["ecc_factor"] / 1e9
        print(f"{planes} planes, {gpb} gates/bit: {bits:.0f} bits/hole, {d:.2f} Gb/mm2 (eff 0.60) = {d/D_1B:.1f}x 1b")
    c_gate = 3.9 * EPS0 * math.pi * 60e-9 * 30e-9 / 6e-9
    e_toggle = c_gate * 2.0 ** 2
    print(f"gate-hole capacitance {c_gate*1e18:.0f} aF, toggle energy at 2 V {e_toggle*1e15:.2f} fJ")
    for gates in (64, 128, 256):
        bits = gates // 2
        e_step = gates * 2 * e_toggle
        e_bit = e_step * bits / bits  # each bit exits after 'bits' steps on average for a full readout of the string
        print(f"{gates:3d}-gate string ({bits} bits): one shift step {e_step*1e15:5.1f} fJ; full readout "
              f"{e_step*bits*1e12:5.2f} pJ = {e_step*1e15:5.1f} fJ/bit; worst latency at 1 ns/step {bits} ns")
    for cte in (0.999, 0.9999, 0.99999):
        for transfers in (128, 512):
            print(f"CTE {cte}: after {transfers} transfers {cte**transfers*100:5.1f}% of packet remains")
    n_t = 1e11 * 1  # cm-2 eV-1 interface traps [ESTIMATE]
    area = math.pi * 60e-7 * 30e-7
    print(f"interface traps under one gate at Dit 1e11-1e12 /cm2eV: {n_t*area:.1f}-{10*n_t*area:.0f} per eV "
          "-> needs fat-zero background charge to keep traps filled")


# ------------------------------------------------------------------------------------------------
# B1-09 Vacuum/air nanogap floating node (trap-free Fowler-Nordheim barrier)
# ------------------------------------------------------------------------------------------------
def fn_j(field_v_m, phi_ev):
    a, b = 1.54e-6, 6.83e9
    return a * field_v_m ** 2 / phi_ev * math.exp(-b * phi_ev ** 1.5 / field_v_m)  # A/m2


def simmons_low_v(s_angstrom, phi_ev, v):
    return 3.16e10 * math.sqrt(phi_ev) / s_angstrom * v * math.exp(-1.025 * s_angstrom * math.sqrt(phi_ev))  # A/cm2


def b1_09():
    hr("B1-09 NANOGAP (VACUUM/AIR) TUNNEL BARRIER FLOATING NODE")
    area_m2 = 100e-18  # 10 x 10 nm emission area
    c_node = 0.2e-15
    for phi in (2.7, 3.5, 4.5):
        for gap_nm, v_w, beta in ((3.0, 6.0, 2.0), (3.0, 8.0, 2.0), (4.0, 8.0, 3.0)):
            f = v_w / (gap_nm * 1e-9) * beta
            i = fn_j(f, phi) * area_m2
            t_w = c_node * 1.0 / i if i > 0 else float("inf")
            print(f"phi {phi} eV, gap {gap_nm} nm, {v_w} V, beta {beta}: I_write {i:.1e} A -> 1 V on 0.2 fF in {t_w:.1e} s")
    for phi in (2.7, 4.5):
        for gap_nm in (2.0, 2.5, 3.0):
            j = simmons_low_v(gap_nm * 10, phi, 1.0)
            i = j * area_m2 * 1e4
            t = c_node * 0.2 / i if i > 0 else float("inf")
            print(f"hold: phi {phi} eV, gap {gap_nm} nm, 1 V across gap: J {j:.1e} A/cm2 -> I {i:.1e} A -> retention {t:.1e} s")
    p = EPS0 * (2.5e9) ** 2 / 2
    print(f"electrostatic pressure at 2.5 V/nm: {p/1e6:.0f} MPa (anchored node; no free-standing beam)")


# ------------------------------------------------------------------------------------------------
# B1-10 Direct-tunnel charge-trap "volatile 3D AND"
# ------------------------------------------------------------------------------------------------
def b1_10():
    hr("B1-10 DIRECT-TUNNEL CHARGE-TRAP 3D AND (DRAM made with 3D-NAND tools)")
    for tiers, fp in ((64, 0.030), (128, 0.030), (128, 0.045), (256, 0.045)):
        d = A1.gbit_per_mm2(fp, 0.60, tiers)
        print(f"{tiers:3d} tiers, per-tier cell {fp:.3f} um2: {d:.2f} Gb/mm2 = {d/D_1B:.1f}x 1b")
    for t_ret in (1.0, 10.0, 100.0):
        print(f"worst-case retention {t_ret:5.0f} s: refresh energy/time x{t_ret/0.064:,.0f} lower than 64 ms")
    print("endurance need with 10 s refresh over 10 yr: refresh-only "
          f"{10*3.156e7/10:.1e} cycles; writes dominate -> 1e10-1e12 target with write-back caching")


# ------------------------------------------------------------------------------------------------
# B1-11 Capacitive non-destructive-read ferroelectric gain cell
# ------------------------------------------------------------------------------------------------
def b1_11():
    hr("B1-11 CAPACITIVE NDRO FERROELECTRIC GAIN CELL (1T-nC_FE, small n)")
    c_cap, c_gate, v_read = 1.0, 0.5, 0.3   # fF, fF, V [ESTIMATE]
    for dcc in (0.2, 0.5, 1.0):  # (C_high - C_low)/C_low
        for n in (1, 2, 4, 8, 64):
            c_node = n * c_cap + c_gate
            dv = v_read * dcc * c_cap / c_node * 1e3
            print(f"dC/C {dcc:3.1f}, n {n:2d} caps/node: node signal {dv:5.1f} mV")
    print("IEDM 2023 imec: zero-bias capacitive window ~8.7 (units per snippet ambiguous), read endurance >1e11, "
          "write endurance ~1e7 [REPORTED]")
    for label, period_s in (("one rewrite per minute", 60.0), ("one rewrite per hour", 3600.0), ("one per day", 86400.0)):
        w = 10 * 3.156e7 / period_s
        print(f"read-mostly tier, {label:22s}: {w:.1e} writes in 10 yr -> margin vs 1e7 write endurance {1e7/w:6.1f}x")


# ------------------------------------------------------------------------------------------------
# B1-12 Sliding ferroelectric semiconductor channel
# ------------------------------------------------------------------------------------------------
def b1_12():
    hr("B1-12 SLIDING-FERROELECTRIC (3R-MoS2 / bilayer hBN) GAIN CHANNEL")
    p_eff = 0.68  # uC/cm2: ~2.25 pC/m dipole density / 0.33 nm [ESTIMATE from typical hBN value]
    for eot in (0.8, 1.0, 1.5):
        c = 3.9 * EPS0 / (eot * 1e-9) * 1e2  # uF/cm2
        print(f"EOT {eot} nm: C_gate {c:.2f} uF/cm2 -> Vt shift per state {p_eff/c:.2f} V, window ~{2*p_eff/c:.2f} V")
    print(f"polarization charge {p_eff} uC/cm2 = {p_eff*1e-6/Q_E:.1e} e/cm2 (comparable to FET channel charge)")
    print("endurance evidence: 3R-MoS2 no fatigue after 1e6 cycles (ms pulses); bilayer-BN FeFET >1e11 cycles, ns [REPORTED]")


# ------------------------------------------------------------------------------------------------
# B1-13 LNOI conductive-domain-wall memory
# ------------------------------------------------------------------------------------------------
def b1_13():
    hr("B1-13 LITHIUM-NIOBATE-ON-INSULATOR DOMAIN-WALL MEMORY")
    ec_v_um = 21.0  # congruent LN coercive field ~21 kV/mm [ESTIMATE, textbook]
    for gap in (20, 50, 100):
        print(f"in-plane electrode gap {gap} nm: switching ~{ec_v_um*gap/1e3:.2f} V")
    for f_nm, layers in ((40, 1), (40, 4), (20, 1)):
        d = density_gb_mm2(4 * (f_nm * 1e-3) ** 2, 0.60, 1, layers)
        print(f"4F2 crosspoint at F={f_nm} nm x {layers} bonded layers: {d:.2f} Gb/mm2 = {d/D_1B:.2f}x 1b")


# ------------------------------------------------------------------------------------------------
# B1-14 VCMA crosspoint, relaxed retention
# ------------------------------------------------------------------------------------------------
def b1_14():
    hr("B1-14 VCMA CROSSPOINT MRAM WITH RELAXED (REFRESHED) RETENTION")
    n = CELLS_16GB
    for t, label in ((1.0, "1 s refresh"), (60.0, "1 min"), (10 * 3.156e7, "10 yr non-volatile")):
        delta = math.log(n * t / 1e-9)
        print(f"{label:20s}: Delta >= {delta:5.1f} kT (mean, before sigma margin)")
    print(f"relaxing 10 yr -> 1 s cuts required Delta by {(1-math.log(n*1/1e-9)/math.log(n*3.156e8/1e-9))*100:.0f}% "
          "(write voltage/energy and free-layer volume scale ~Delta)")
    for f_nm, decks in ((20, 1), (20, 4), (30, 4)):
        d = density_gb_mm2(4 * (f_nm * 1e-3) ** 2, 0.55, 1, decks)
        print(f"4F2 x {decks} decks at F={f_nm} nm: {d:.2f} Gb/mm2 = {d/D_1B:.2f}x 1b")
    print(f"write energy 6-20 fJ [A3 REPORTED] vs refresh {REFRESH_FJ_PER_BIT:.0f} fJ per bit-refresh; no refresh at all if Delta>=64")


# ------------------------------------------------------------------------------------------------
# B1-15 Shared-rail SOT on logic
# ------------------------------------------------------------------------------------------------
def b1_15():
    hr("B1-15 4-MTJ SHARED-RAIL SOT TIER ON LOGIC")
    f = 0.020
    for mtj, area_f2 in ((1, 30), (4, 60), (8, 100)):
        per_bit = area_f2 * f ** 2 / mtj
        d = density_gb_mm2(per_bit, 0.55)
        print(f"{mtj} MTJ/rail, {area_f2}F2 per rail group: {per_bit*1e6:.0f} nm2/bit -> {d:.3f} Gb/mm2 "
              f"({d/0.04:.1f}x N2 SRAM macro ~0.04 Gb/mm2 [A1]; {d/D_1B:.2f}x 1b)")


# ------------------------------------------------------------------------------------------------
# B1-16 Protonic gain cell
# ------------------------------------------------------------------------------------------------
def b1_16(sig_lin):
    hr("B1-16 PROTONIC (H+ in WO3, PSG electrolyte) GAIN CELL")
    for t_psg in (2, 5, 10):
        print(f"PSG {t_psg} nm at ~1 V/nm (MIT Science 2022 regime): write {t_psg:.0f} V")
    # Pseudocapacitor charge density (why the 'nano-supercap stub' looked attractive, and why it fails on read speed)
    rho, mw, dx = 7.16, 231.8, 0.1
    q_vol = rho / mw * dx * 96485  # C/cm3
    q_area = q_vol * 2e-7 * 1e6    # uC/cm2 in 2 nm
    print(f"WO3 dx=0.1 H/W in 2 nm film: {q_area:.0f} uC/cm2 vs today's wall signal {sig_lin:.1f} uC/cm2 -> "
          f"{q_area/sig_lin:.0f}x, but extraction needs ~1 V/nm (same field as writing) -> no fast low-field read")
    print("hence the card is a 3-terminal gain cell (read WO3 conductance), not a capacitor")


# ------------------------------------------------------------------------------------------------
# B1-17 Redox-molecule capacitor
# ------------------------------------------------------------------------------------------------
def b1_17(sig_lin):
    hr("B1-17 REDOX-MOLECULE MONOLAYER CAPACITOR (porphyrin class)")
    for footprint_nm2 in (1.0, 2.0):
        n = 1e14 / footprint_nm2  # per cm2
        q = n * Q_E * 1e6
        print(f"molecule footprint {footprint_nm2} nm2: {n:.1e}/cm2 -> {q:.1f} uC/cm2 per redox state "
              f"({q/sig_lin:.1f}x today's wall signal)")
        for states in (2, 3):
            h = pillar_height_for_charge_nm(Q_SIG_1B_fC, q)
            print(f"   {states} oxidation states -> {math.log2(states+1):.1f} bit/cell with discrete plateaus; "
                  f"pillar for 1b-equal per-state charge {h:.0f} nm")


# ------------------------------------------------------------------------------------------------
# B1-18 NEMS relay access switch
# ------------------------------------------------------------------------------------------------
def b1_18():
    hr("B1-18 NEMS RELAY ACCESS SWITCH (zero GIDL)")
    area_cm2 = math.pi * PILLAR_D_NM * 1e-7 * 1300e-7
    for jg in (1e-8, 1e-7):
        i = jg * area_cm2
        t = CS_1B * 1e-15 * 0.155 / i
        print(f"capacitor dielectric J {jg:.0e} A/cm2 at hold bias: I {i:.1e} A -> retention {t:.0f} s")
    # switching time of a cantilever ~ 1/(2 f0); f0 for a 200 nm x 20 nm x 10 nm Si3N4/TiN beam
    e_mod, rho = 250e9, 3200.0
    for l_nm, t_nm in ((200, 10), (100, 8)):
        l, t = l_nm * 1e-9, t_nm * 1e-9
        f0 = 0.162 * t / l ** 2 * math.sqrt(e_mod / rho)
        print(f"cantilever {l_nm} nm x {t_nm} nm: f0 {f0/1e9:.2f} GHz -> mechanical switch ~{1/(2*f0)*1e9:.2f} ns + pull-in delay")
    print(f"contact charge per access: {CS_1B*0.5:.1f} fC (cold-ish switching, uA-level) vs mA in RF MEMS")
    print(f"wordline swing ~1 V (pull-in) vs 2.9 V: WL energy x{(1/2.9)**2*0.45/0.95:.2f} (no pump)")


# ------------------------------------------------------------------------------------------------
# B1-19 NbO2 Mott threshold-switch local sense element
# ------------------------------------------------------------------------------------------------
def b1_19():
    hr("B1-19 NbO2 MOTT THRESHOLD SWITCH AS A BEOL LOCAL SENSE ELEMENT")
    cv, t_imt, t_amb = 3.0, 1080.0, 358.0  # J/cm3K, K, K [ESTIMATE]
    for d_nm in (10, 20):
        vol = (d_nm * 1e-7) ** 3
        e = cv * vol * (t_imt - t_amb)
        print(f"{d_nm} nm cube heated to the IMT: {e*1e15:.1f} fJ (x~3-10 with losses)")
    for sigma_pct in (1, 2, 5):
        print(f"threshold sigma {sigma_pct}% of 1.0 V = {sigma_pct*10} mV vs 64-cell BL 1-bit signal "
              f"{A1.sense_signal_mV(CS_1B, A1.c_bitline_fF(64), VARY, VARY/2):.0f} mV")


# ------------------------------------------------------------------------------------------------
# B1-20 2D-barrier quasi-volatile memory
# ------------------------------------------------------------------------------------------------
def b1_20():
    hr("B1-20 2D-BARRIER QUASI-VOLATILE CELL (seconds-minutes retention, low-field writes)")
    for t in (10.0, 100.0):
        print(f"retention {t:.0f} s: refresh x{t/0.064:.0f} lower")
    print("Fudan PoX: 400 ps, 5 V, 5.5e6 cycles, 10 yr [REPORTED]; Fudan 2D SFG: 10 s, 15 ns [A3 REPORTED]")
    print(f"endurance gap to 1e12: {1e12/5.5e6:.1e}x; to 1e15: {1e15/5.5e6:.1e}x")
    d4 = density_gb_mm2(4 * 0.020 ** 2)
    print(f"1T 4F2 at F=20 nm: {d4:.2f} Gb/mm2/tier ({d4/D_1B:.2f}x 1b)")


def main():
    sig_lin = anchors()
    b1_01(sig_lin)
    b1_02()
    b1_03()
    b1_04()
    b1_05()
    b1_06()
    b1_07()
    b1_08()
    b1_09()
    b1_10()
    b1_11()
    b1_12()
    b1_13()
    b1_14()
    b1_15()
    b1_16(sig_lin)
    b1_17(sig_lin)
    b1_18()
    b1_19()
    b1_20()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
