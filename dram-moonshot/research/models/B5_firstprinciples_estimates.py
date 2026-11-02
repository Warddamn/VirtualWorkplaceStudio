#!/usr/bin/env python3
"""
B5_firstprinciples_estimates.py -- arithmetic behind phase-B lens 5,
"FIRST PRINCIPLES & WILD CARDS" (dram-moonshot, agent B5-firstprinciples).
Written 2026-11-01. Pure standard library; `python3` exits 0.

Feeds research/phaseB/B5-firstprinciples.json and B5-firstprinciples_notes.md.
Tags used in comments:
  [A1]          reused from models/dram_cell_physics.py (imported) or A1_scaling_limits.md
  [A3]          reused from A3_research_frontier.md / A3_frontier_estimates.py
  [REPORTED]    number from a search snippet logged in research/sources/B5-firstprinciples.jsonl
  [ESTIMATE]    my assumption, logged in research/assumptions/B5-firstprinciples.md
  [UNVERIFIED]  training knowledge; no URL seen this session

Section B5-00 is the thermodynamic floor ledger. Sections B5-01..B5-18 map 1:1 to idea cards.
Every number quoted in a card's first_principles_estimate is printed here.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "models")))
import dram_cell_physics as A1  # noqa: E402  (helpers only; main() is guarded)

# ------------------------------------------------------------------------------------------
# Physical constants
# ------------------------------------------------------------------------------------------
KB = 1.380649e-23        # J/K
Q = 1.602176634e-19      # C
EPS0 = 8.8541878128e-12  # F/m
HBAR = 1.054571817e-34   # J s
PHI0 = 2.067833848e-15   # Wb (flux quantum)
T_RT = 300.0
T_HOT = 358.0            # 85 C


def kT(T=T_RT):
    return KB * T


def kT_eV(T=T_RT):
    return KB * T / Q


def hr(title):
    print("\n" + "=" * 100)
    print(title)
    print("=" * 100)


# ------------------------------------------------------------------------------------------
# Shared anchors [A1]
# ------------------------------------------------------------------------------------------
CELL_1B_NM2 = 1070.0          # 6F2 at F = 13.4 nm (A1 section 1)
F_1B_NM = 13.4
ARRAY_EFF = 0.51              # A1 section 1
DENS_1B = 0.447               # Gb/mm2, Micron D1b teardown (A1)
N_BITS_DIE = 16e9 * A1.INPUTS["ecc_factor"]   # 1.7e10 physical bits per 16Gb die
E_REF_FJ, E_REF_BL_FJ, E_REF_WL_FJ = A1.refresh_energy_per_bit_fJ()   # ~45.8 fJ total
CS_1B_FF = 5.4
CBL_512_FF = A1.c_bitline_fF(512)   # ~34.7 fF


def density_gb_mm2(nm2_per_bit, eff=ARRAY_EFF):
    """User Gb/mm2 for a given physical area per bit (ECC removed, like A1.gbit_per_mm2)."""
    return A1.gbit_per_mm2(nm2_per_bit * 1e-6, eff)


# ==========================================================================================
# B5-00  Thermodynamic floor ledger: what does it cost, at minimum, to hold a bit for ~1 s?
# ==========================================================================================
def barrier_kT(t_hold_s, tau0_s, n_bits=1.0, p_fail=1.0):
    """Barrier (in kT) so that n_bits cells see <= p_fail expected flips in t_hold.
    Arrhenius/Neel-Brown: rate = (1/tau0) exp(-E/kT)."""
    return math.log(n_bits * t_hold_s / (tau0_s * p_fail))


def section_floor():
    hr("B5-00  THERMODYNAMIC FLOOR LEDGER (minimum barrier, energy and charge to hold a bit ~1 s)")
    print("Barrier needed, E_b/kT = ln(N * t / (tau0 * p_fail))   [ESTIMATE: Neel-Brown/Arrhenius]")
    print(f"{'case':58s} {'tau0=1ns':>10s} {'tau0=0.1ps':>11s} {'eV @300K':>9s} {'eV @358K':>9s}")
    cases = [
        ("single bit, 1 s, p=1", 1.0, 1.0, 1.0),
        ("16Gb die (1.7e10 bits), 1 s, <=1 flip", 1.0, N_BITS_DIE, 1.0),
        ("16Gb die, 1 s, raw BER 1e-6 (ECC cleans)", 1.0, 1.0, 1e-6),
        ("16Gb die, 10 yr (3.15e8 s), <=1 flip (non-volatile)", 3.15e8, N_BITS_DIE, 1.0),
    ]
    for name, t, n, p in cases:
        b_mag = barrier_kT(t, 1e-9, n, p)
        b_atom = barrier_kT(t, 1e-13, n, p)
        print(f"{name:58s} {b_mag:10.1f} {b_atom:11.1f} {b_atom*kT_eV(T_RT):9.2f} {b_atom*kT_eV(T_HOT):9.2f}")
    landauer = kT(T_RT) * math.log(2)
    print(f"\nLandauer kT ln2 at 300 K = {landauer:.2e} J ({landauer/Q*1e3:.1f} meV)")
    print(f"A1 refresh energy per bit-refresh = {E_REF_FJ:.1f} fJ (BL {E_REF_BL_FJ:.1f}, WL {E_REF_WL_FJ:.1f}, x2 periphery)")
    print(f"  ratio to Landauer = {E_REF_FJ*1e-15/landauer:.1e}")
    p64 = E_REF_FJ * 1e-15 / 0.064
    p1 = E_REF_FJ * 1e-15 / 1.0
    print(f"Holding power per bit: 64 ms refresh = {p64*1e12:.2f} pW; 1 s = {p1*1e15:.1f} fW; "
          f"16Gb die @64 ms = {p64*N_BITS_DIE*1e3:.1f} mW")
    # stored energy of today's bit vs barrier needed
    e_stored = 0.5 * CS_1B_FF * 1e-15 * A1.INPUTS["v_array"] ** 2
    print(f"Energy stored on a 1b cell (0.5 C V^2) = {e_stored:.2e} J = {e_stored/kT():.1e} kT "
          f"(barrier needed ~50 kT): DRAM holds charge kinetically (leakage), not thermodynamically.")
    # electrons per bit
    ne_1b = CS_1B_FF * 1e-15 * A1.INPUTS["v_array"] / 2 / Q
    print(f"Signal electrons today ~{ne_1b:,.0f}; a 0.22 e- rms sensor (QIS jot, REPORTED) resolves "
          f"levels ~3 e- apart at 6 sigma -> charge floor is set by leakage and sensor bandwidth, not noise.")
    # wire-limited area floor
    for f in (13.4, 20.0, 40.0):
        print(f"Wire floor: 4F2 at F={f:4.1f} nm = {4*f*f:6.0f} nm2/bit per layer "
              f"({4*f*f/CELL_1B_NM2:.2f}x 1b cell); below that only shift-addressing, MLC or tiers help")


# ==========================================================================================
# B5-01  Click-RAM: snap-through 2D nanoribbon as a mechanical floating gate
# ==========================================================================================
def buckled_ribbon(E2D, rho2D, t_nm, L_nm, w_nm, target_kT, g0_nm, T=T_RT):
    """Clamped-clamped ribbon, first-mode shape w(x) = (q/2)(1 - cos 2pi x/L).
    Energy U(q) = EI pi^4 q^2/L^3 + (EA/2L)(pi^2 q^2/(4L) - delta)^2
    => barrier dU = (EA/2L)(delta - delta_cr)^2 = EA pi^4 q^4 / (32 L^3)  [derived; ESTIMATE]
    E2D = E*t (N/m); rho2D = areal mass (kg/m2)."""
    L, w, t = L_nm * 1e-9, w_nm * 1e-9, t_nm * 1e-9
    EA = E2D * w
    dU = target_kT * kT(T)
    q = (dU * 32 * L ** 3 / (EA * math.pi ** 4)) ** 0.25
    delta_cr = 4 * math.pi ** 2 * (t ** 2 / 12) / L          # Euler shortening, I/A = t^2/12
    delta_excess = math.pi ** 2 * q ** 2 / (4 * L)
    strain = (delta_cr + delta_excess) / L
    k_eff = 8 * dU / q ** 2                                  # curvature of quartic well at minimum
    m_eff = 0.375 * rho2D * L * w                            # (3/8) of ribbon mass for this mode
    f0 = math.sqrt(k_eff / m_eff) / (2 * math.pi)
    F_snap = 1.54 * dU / q                                   # max slope of quartic double well
    A_eff = 0.5 * L * w                                      # electrode overlap weighted by mode shape
    g_up = (g0_nm * 1e-9) + q
    V_snap = math.sqrt(F_snap * 2 * g_up ** 2 / (EPS0 * A_eff))
    C_el = EPS0 * A_eff / g_up
    E_write = C_el * V_snap ** 2
    g_dn = (g0_nm * 1e-9) - q
    neg_k = EPS0 * A_eff * V_snap ** 2 / g_dn ** 3           # electrostatic negative stiffness at down state
    return dict(q_nm=q * 1e9, strain_pct=strain * 100, k=k_eff, f0_GHz=f0 / 1e9, F_snap_nN=F_snap * 1e9,
                V_snap=V_snap, E_write_aJ=E_write * 1e18, neg_k=neg_k, g_up_nm=g_up * 1e9, g_dn_nm=g_dn * 1e9)


def section_click():
    hr("B5-01  CLICK-RAM: snap-through 2D nanoribbon mechanical floating gate")
    mats = {
        "graphene (E2D 340 N/m, 0.76 mg/m2)": (340.0, 7.6e-7, 0.335),     # [UNVERIFIED] textbook values
        "MoS2 1L (E2D ~180 N/m, 3.1 mg/m2)": (180.0, 3.1e-6, 0.65),       # [UNVERIFIED]
        "ALD Al2O3 2 nm (E~170 GPa)": (340.0, 6.4e-6, 2.0),               # [ESTIMATE]
    }
    for (L, w, g0, tgt) in [(100, 20, 6.0, 80), (50, 10, 3.5, 80), (50, 10, 3.5, 45)]:
        for name, (E2D, rho, t) in mats.items():
            r = buckled_ribbon(E2D, rho, t, L, w, tgt, g0)
            print(f"L={L:3d} w={w:2d} nm, dU={tgt:3d} kT, {name:36s}: q=+/-{r['q_nm']:.2f} nm, "
                  f"strain {r['strain_pct']:.3f}%, f0={r['f0_GHz']:.1f} GHz, V_snap={r['V_snap']:.2f} V, "
                  f"E_write={r['E_write_aJ']:.1f} aJ, k={r['k']:.2f} N/m vs neg-k {r['neg_k']:.2f}")
    # read contrast: ribbon = suspended gate over an oxide channel; gaps (g0+q) vs (g0-q) + 1 nm EOT
    g_up, g_dn, eot = 6 + 1.33, 6 - 1.33, 1.0      # nm, graphene L=100 case rounded
    c_ratio = (g_up + eot) / (g_dn + eot)
    v_read = 0.8
    dv_eff = v_read * (1 - 1 / c_ratio)
    print(f"Read: gate-coupling ratio down/up = {c_ratio:.2f}; at V_read {v_read} V the effective gate drive "
          f"differs by {dv_eff:.2f} V -> ~10^{dv_eff/0.075:.1f} current ratio at 75 mV/dec; read force "
          f"= {(v_read/1.9)**2:.2f} of write force (no snap)")
    for (cell_nm2, label) in [(140 * 40, "L=100 beam, 40 nm pitch"), (90 * 40, "L=50, w=20/40 pitch"),
                              (90 * 25, "L=50, w=10/25 pitch")]:
        for tiers in (1, 2):
            print(f"  cell {label:26s}: {cell_nm2:5d} nm2, {tiers} BEOL tier(s) -> {cell_nm2/tiers/CELL_1B_NM2:.2f}x 1b area/bit")
    # fatigue reference: a 5 MHz MEMS oscillator for 10 years
    print(f"Fatigue reference: a 5 MHz MEMS resonator over 10 yr = {5e6*3.15e8:.1e} cycles [ESTIMATE]")


# ==========================================================================================
# B5-02  Capacitor-hole racetrack: electroplated Bloch-point domain-wall wires in the HAR mold
# ==========================================================================================
def section_racetrack():
    hr("B5-02  CAPACITOR-HOLE RACETRACK (vertical electroplated CoNi/NiFe wires, DW shift register)")
    d_nm = 20.0
    bit_len_nm = 3 * d_nm               # [ESTIMATE] domain + wall + dipolar guard ~3 diameters
    for H in (1300.0, 3000.0):
        raw_slots = H / bit_len_nm
        data_bits = math.floor(raw_slots / 2)   # half the track is shift buffer
        dens = DENS_1B * data_bits
        print(f"Hole height {H:5.0f} nm (AR {H/d_nm:.0f}): {raw_slots:.1f} slots -> {data_bits} data bits per hole "
              f"-> {data_bits}x bits per 1b-cell footprint (~{dens:.1f} Gb/mm2 at 1b array efficiency)")
    A = math.pi * (d_nm * 1e-9 / 2) ** 2
    rho = 2e-7                           # ohm m, CoNi/NiFe nanowire [ESTIMATE]
    for J in (1e11, 3e11, 1e12):
        I = J * A
        for H in (1300e-9,):
            R = rho * H / A
            P = I ** 2 * R
            v = 100.0 if J <= 1e11 else (200.0 if J <= 3e11 else 300.0)   # m/s [ESTIMATE from 300 m/s sim, REPORTED]
            t_bit = bit_len_nm * 1e-9 / v
            n = 10
            t_avg = (n / 2) * t_bit
            e_op = P * t_avg
            print(f"J={J:.0e} A/m2: I={I*1e6:6.1f} uA, R={R:6.0f} ohm, P={P*1e6:6.2f} uW, v~{v:.0f} m/s, "
                  f"{t_bit*1e9:.2f} ns/bit, avg access (5 shifts) {t_avg*1e9:.1f} ns, E/shift-op {e_op*1e15:.1f} fJ")
    print(f"Cu electromigration design rule ~1e10 A/m2 DC [UNVERIFIED]; racetrack needs 10-100x that, in short bipolar pulses")
    # material per wafer
    holes_per_mm2 = 1e12 / CELL_1B_NM2 * ARRAY_EFF
    usable_mm2 = 60334.0                 # ram-venture device model usable area per 300 mm wafer
    vol = math.pi * (10e-9) ** 2 * 1.3e-6 * holes_per_mm2 * usable_mm2
    grams = vol * 1e6 * 8.9
    print(f"Holes/wafer {holes_per_mm2*usable_mm2:.2e}; magnetic metal {grams:.2f} g/wafer; fleet 22.2M wafers -> "
          f"{grams*22.2e6/1e6:.1f} t/yr (Co+Ni; world Co mine supply ~2e5 t [UNVERIFIED])")
    # TMR read
    ra = 5.0                             # ohm um2 [ESTIMATE]
    r_mtj = ra / (math.pi * (0.01) ** 2)
    print(f"Top MTJ read head d=20 nm, RA {ra} ohm.um2 -> R = {r_mtj/1e3:.1f} kohm; 10 uA read -> "
          f"{10e-6*r_mtj*0.5:.2f} V swing at 100% TMR")


# ==========================================================================================
# B5-03  Deep-level charge bit: QD-Flash ensemble -> atom-placed single-defect bit
# ==========================================================================================
def section_deeplevel():
    hr("B5-03  DEEP-LEVEL CHARGE BIT (thermal-emission-limited storage, capture write)")
    sigma, vth, Nv = 1e-15, 1e7, 1e19   # cm2, cm/s, cm-3 [ESTIMATE]
    pref = 1 / (sigma * vth * Nv)       # s
    print(f"Emission prefactor 1/(sigma v N) = {pref:.0e} s")
    for label, t, extra in [("1 s, single bit", 1.0, 0.0), ("1 s, raw BER 1e-6", 1.0, math.log(1e6)),
                            ("1 s, <=1 flip in 1.7e10", 1.0, math.log(N_BITS_DIE)),
                            ("1 day, raw BER 1e-6", 86400.0, math.log(1e6))]:
        x = math.log(t / pref) + extra
        print(f"  {label:26s}: E_loc >= {x:.1f} kT = {x*kT_eV(T_RT):.2f} eV (300 K), {x*kT_eV(T_HOT):.2f} eV (358 K)")
    t_rec = 4 * 86400.0
    e_imp = math.log(t_rec / pref) * kT_eV()
    print(f"QD-Flash record 4 days at RT (REPORTED) implies E_loc ~{e_imp:.2f} eV with this prefactor")
    # capture write time
    n = 1e18
    tau_cap = 1 / (sigma * vth * n)
    print(f"Capture write: tau = 1/(sigma v n) at n=1e18 cm-3 = {tau_cap*1e9:.2f} ns (QD-Flash measured 6 ns write, REPORTED)")
    # single-electron threshold shift
    cox = 3.45e-2   # F/m2 at EOT 1 nm
    for a_nm in (10, 15, 20):
        dvt = Q / (cox * (a_nm * 1e-9) ** 2)
        print(f"  one electron under a {a_nm} nm x {a_nm} nm gate (EOT 1 nm): dVt = {dvt*1e3:.0f} mV")
    for f_nm, bits in [(10, 1), (10, 2), (14, 2)]:
        area = 4 * f_nm ** 2
        print(f"  4F2 at F={f_nm} nm with {bits} b/cell: {area/bits:.0f} nm2/bit -> {CELL_1B_NM2/(area/bits):.1f}x 1b density")
    print(f"Gate write energy C V^2 at 10 nm, EOT 1 nm, 1 V: {cox*(10e-9)**2*1.0*1e18:.1f} aJ")
    # Poole-Frenkel lowering is not enough on its own
    eps = 11 * EPS0
    E = 1e8
    dE = math.sqrt(Q * E / (math.pi * eps))
    print(f"Poole-Frenkel lowering at 1 MV/cm (eps_r 11) = {dE:.2f} eV -> emission x{math.exp(dE/kT_eV()):.0f}: "
          f"erase needs band-to-trap tunnelling at high field, not barrier lowering alone")


# ==========================================================================================
# B5-04  Jot-RAM: image-sensor pinned well + correlated-double-sampling read for few-electron MLC
# ==========================================================================================
def section_jot():
    hr("B5-04  JOT-RAM (pinned storage well + transfer gate + shared floating diffusion, CDS read)")
    cg = 423e-6       # V/e-  [REPORTED Ma et al. 2015]
    rn = 0.22         # e- rms [REPORTED]
    idark_rt = 0.1    # e-/s at room temperature [REPORTED]
    c_fd = Q / cg
    print(f"Floating diffusion C = q/CG = {c_fd*1e18:.0f} aF; 20 e- level spacing = {20*cg*1e3:.1f} mV at the FD")
    spacing, budget = 20, 10
    for T_c in (25, 45, 65, 85):
        mult = 2 ** ((T_c - 25) / 7.0)      # dark current doubles ~7 C [ESTIMATE]
        med = idark_rt * mult
        tail = med * 100                    # [ESTIMATE] 6-sigma tail = 100x median (hot pixels)
        print(f"  {T_c:2d} C: dark {med:7.2f} e-/s median, {tail:8.0f} e-/s tail -> retention for a {budget} e- budget: "
              f"median {budget/med:8.1f} s, tail {budget/tail*1e3:9.1f} ms")
    # noise at memory bandwidth
    for bw_ratio in (50, 500):
        print(f"  read noise if bandwidth is {bw_ratio}x the QIS readout bandwidth: {rn*math.sqrt(bw_ratio):.1f} e- rms "
              f"-> {spacing/(rn*math.sqrt(bw_ratio)):.0f} sigma per 20 e- level")
    # full well
    fw_density = 6000.0   # e-/um2 junction area [UNVERIFIED: CIS pinned photodiode class]
    levels = 16
    need = levels * spacing
    print(f"16 levels x 20 e- = {need} e- full well; planar pinned well needs {need/fw_density:.3f} um2 "
          f"({need/fw_density*1e6/CELL_1B_NM2:.0f}x a 1b cell) -> must be vertical")
    d, h = 40e-3, 0.6     # um
    side = math.pi * d * h
    print(f"Vertical pinned well d=40 nm, h=600 nm: sidewall {side:.3f} um2 -> ~{side*fw_density:.0f} e- full well")
    for cell_nm2 in (4000, 5000):
        per_bit = (cell_nm2 + 2000 / 8) / 4
        print(f"  cell {cell_nm2} nm2 + 1/8 shared readout (2000 nm2), 4 b/cell -> {per_bit:.0f} nm2/bit "
              f"({per_bit/CELL_1B_NM2:.2f}x 1b area/bit)")
    print(f"Read energy: column 30 fF x 0.15 V swing x 1 V supply ~ {30e-15*0.15*1.0*1e15:.1f} fJ per 4-bit read [ESTIMATE]")


# ==========================================================================================
# B5-05  Crystalline crested-barrier selector 1S1C crosspoint (transistor-less, deck-stacked)
# ==========================================================================================
def section_crested():
    hr("B5-05  CRESTED-BARRIER 1S1C CROSSPOINT: the charge-fluence rule")
    # stub capacitor: k=40 physical 5 nm on a 14 nm pillar, 300 nm tall (single-sided)
    k, t, d, h = 40.0, 5e-9, 14e-9, 300e-9
    cs = EPS0 * k * math.pi * d * h / t
    print(f"Stub capacitor 14 nm x 300 nm, k=40 / 5 nm: Cs = {cs*1e15:.2f} fF")
    cbl64 = A1.c_bitline_fF(64)
    sig = A1.sense_signal_mV(cs * 1e15, cbl64, A1.INPUTS['v_array'], A1.INPUTS['v_array'] / 2)
    print(f"64-cell bitline Cbl = {cbl64:.2f} fF -> signal {sig:.0f} mV (need >= 50 mV)")
    for F in (20.0,):
        area_cm2 = (F * 1e-7) ** 2
        q_write = cs * 1.0
        fluence = q_write / area_cm2
        print(f"Charge fluence per write through an F={F:.0f} nm selector: {q_write*1e15:.2f} fC / {area_cm2:.1e} cm2 "
              f"= {fluence:.1e} C/cm2")
        for qbd, label in [(1, "amorphous high-k"), (10, "thin SiO2"), (100, "best SiO2"),
                           (3e13, "epitaxial RTD-class barrier (1e5 A/cm2 x 10 yr)")]:
            print(f"    Q_BD {qbd:8.0e} C/cm2 ({label:44s}) -> {qbd/fluence:.1e} writes")
        print(f"    DRAM-class target 1e15 writes needs Q_BD >= {1e15*fluence:.1e} C/cm2")
    for decks, F in [(1, 20.0), (2, 20.0), (4, 20.0), (4, 26.0)]:
        per_bit = 4 * F * F / decks
        print(f"  {decks} deck(s) of 4F2 at F={F:.0f} nm -> {per_bit:.0f} nm2/bit = {CELL_1B_NM2/per_bit:.2f}x 1b cell density")


# ==========================================================================================
# B5-06  Seconds-ULTRARAM: resonant-tunnelling floating gate retuned from 1000 yr to ~1 day
# ==========================================================================================
def section_ultraram():
    hr("B5-06  SECONDS-ULTRARAM (triple-barrier resonant-tunnelling floating gate, retention traded for speed)")
    cox = 3.45e-2   # F/m2 coupling (EOT ~1 nm) [ESTIMATE]
    for dv, tw in [(0.5, 10e-9), (0.5, 1e-9), (0.3, 10e-9)]:
        J = cox * dv / tw
        print(f"  dV_FG={dv} V in {tw*1e9:.0f} ns needs J = {J:.1e} A/m2 = {J/1e4:.0f} A/cm2 "
              f"(resonant-tunnel diodes carry 1e4-1e5 A/cm2 [UNVERIFIED])")
    for a_nm in (20,):
        e = cox * (a_nm * 1e-9) ** 2 * 2.5 ** 2
        print(f"  C V^2 of a {a_nm} nm cell at 2.5 V = {e:.1e} J (Lancaster predicts ~1e-17 J, REPORTED)")
    print(f"  endurance: >1e7 degradation-free cycles reported; target 1e15 needs crystalline barriers (see B5-05 rule)")
    print(f"  retention ratio 1000 yr -> 1 day = {1000*365:.0e}x = ln -> {math.log(1000*365):.1f} kT less barrier "
          f"({math.log(1000*365)*kT_eV():.2f} eV)")


# ==========================================================================================
# B5-07  Self-timed 2-terminal NEMS-selector crosspoint
# ==========================================================================================
def section_nems_selector():
    hr("B5-07  SELF-TIMED NEMS-SELECTOR 1S1C CROSSPOINT")
    k, g, A, gc = 1.0, 5e-9, 2e-15, 1e-9   # N/m, m, m2, contact gap (dielectric coat) [ESTIMATE]
    v_pi = math.sqrt(8 * k * g ** 3 / (27 * EPS0 * A))
    v_r = math.sqrt(k * g * 2 * gc ** 2 / (EPS0 * A))
    print(f"k={k} N/m, gap {g*1e9:.0f} nm, area {A*1e15:.0f}e-15 m2: pull-in V_pi = {v_pi:.2f} V, release V_r = {v_r:.2f} V "
          f"(no adhesion); window {v_pi-v_r:.2f} V")
    v_bl = 2.2
    print(f"Write '1' with BL={v_bl} V: relay closes, cap charges until V_BL - V_cap < V_r -> V_cap = {v_bl-v_r:.2f} V "
          f"(self-limited); write '0' with BL=-0.3 V -> V_cap = {-0.3+v_r:.2f} V")
    for gvar in (0.05, 0.10):
        print(f"  gap variation {gvar*100:.0f}% -> V_pi variation {((1+gvar)**1.5-1)*100:.0f}%")
    cs = 1.0e-15
    for leak_aA in (8.6, 86.0):
        print(f"  hold: relay open, leakage only via cap dielectric {leak_aA} aA (B1-18 numbers) -> "
              f"{cs*0.5/(leak_aA*1e-18):.0f} s for a 0.5 V budget on 1 fF")
    m = 3e-21   # kg [ESTIMATE] effective mass of a 100x20 nm 2D beam incl. electrode
    f0 = math.sqrt(k / m) / (2 * math.pi)
    print(f"  mechanical f0 ~ {f0/1e9:.1f} GHz -> closure in ~{1/(4*f0)*1e9:.2f}-{1/f0*1e9:.1f} ns")


# ==========================================================================================
# B5-08  Adiabatic refresh with resonant (piezo-MEMS) charge recovery
# ==========================================================================================
def section_adiabatic():
    hr("B5-08  ADIABATIC REFRESH: stepwise / resonant charge recovery on bitlines and wordlines")
    core = E_REF_BL_FJ + E_REF_WL_FJ
    print(f"A1 refresh energy {E_REF_FJ:.1f} fJ = 2 x (BL {E_REF_BL_FJ:.1f} + WL {E_REF_WL_FJ:.1f})")
    base_ref = core * 1.3     # refresh needs no column/I-O path: periphery multiplier 1.3 [ESTIMATE]
    print(f"Refresh-only baseline with 1.3x periphery = {base_ref:.1f} fJ/bit")
    for label, frac in [("N=4 stepwise tanks", 1 / 4), ("N=8 stepwise", 1 / 8),
                        ("resonant, 50% recovered (Vaire first chip, REPORTED)", 0.5),
                        ("resonant, 90% recovered (MEMS-resonator target)", 0.1)]:
        new = core * frac + core * 0.3
        print(f"  {label:52s}: {new:5.1f} fJ/bit -> {base_ref/new:.1f}x lower refresh energy")
    c_bank = 8192 * CBL_512_FF * 1e-15
    for f in (50e6, 200e6):
        L = 1 / ((2 * math.pi * f) ** 2 * c_bank)
        print(f"  one bank row: 8192 bitlines x {CBL_512_FF:.1f} fF = {c_bank*1e12:.0f} pF; resonance at {f/1e6:.0f} MHz "
              f"needs L = {L*1e9:.1f} nH (on-chip spiral Q~10 vs piezo-MEMS Q~1e3 [UNVERIFIED])")
    die_mw = E_REF_FJ * 1e-15 / 0.064 * N_BITS_DIE * 1e3
    print(f"  16Gb die refresh power today {die_mw:.1f} mW; at 3x lower -> {die_mw/3:.1f} mW")


# ==========================================================================================
# B5-09  Negative-capacitance (active neutralization) bitline
# ==========================================================================================
def section_negcap():
    hr("B5-09  NEGATIVE-CAPACITANCE BITLINE (capacitance neutralization imported from electrophysiology)")
    v = A1.INPUTS["v_array"]
    q = CS_1B_FF * 1e-15 * v / 2
    for frac in (0.0, 0.5, 0.7, 0.8):
        cbl_eff = CBL_512_FF * (1 - frac)
        sig = q / ((CS_1B_FF + cbl_eff) * 1e-15) * 1e3
        cs_needed = A1.cs_min_fF(cbl_eff, 50.0, v / 2)
        noise_gain = 1 / (1 - frac)
        print(f"  Cn/Cbl={frac:.1f}: Cbl_eff {cbl_eff:5.1f} fF, signal with 5.4 fF cell {sig:5.0f} mV, "
              f"Cs needed for 50 mV {cs_needed:.2f} fF (height ~{1300*cs_needed/CS_1B_FF:.0f} nm), amp-noise gain {noise_gain:.1f}x")
    for vos_mV, cf in [(10, 24.3), (3, 24.3)]:
        err = vos_mV * 1e-3 * cf * 1e-15
        print(f"  amplifier offset {vos_mV} mV on Cf {cf} fF injects {err*1e15:.2f} fC vs a 1.7 fF cell's "
              f"{1.7e-15*v/2*1e15:.2f} fC signal charge")


# ==========================================================================================
# B5-10  Myelinated saltatory bitline (vacuum sheath + 2T regenerative nodes)
# ==========================================================================================
def section_myelin():
    hr("B5-10  MYELINATED BITLINE: vacuum sheath + non-latching 2T gain nodes every N cells")
    split = {"lateral BL-BL and BL-contact": 0.55, "BL-WL crossover": 0.25, "junction + SA fixed": 0.20}
    print("Cbl split [ESTIMATE]: " + ", ".join(f"{k} {v:.0%}" for k, v in split.items()))
    for k_old in (4.0, 2.5):   # effective lateral k today (spacer partly air already: Samsung 1y air spacer)
        f = split["lateral BL-BL and BL-contact"] * (1 / k_old) + (1 - split["lateral BL-BL and BL-contact"])
        print(f"  full vacuum sheath, effective lateral k {k_old} -> 1: Cbl x{f:.2f}")
    for n in (512, 128, 64, 32):
        cbl = A1.c_bitline_fF(n)
        cs = A1.cs_min_fF(cbl, 50.0, A1.INPUTS["v_array"] / 2)
        print(f"  segment {n:3d} cells: Cbl {cbl:5.1f} fF -> Cs for 50 mV {cs:.2f} fF (~{1300*cs/CS_1B_FF:4.0f} nm tall)")
    # axon analogy: node spacing ~100x fibre diameter (textbook) [UNVERIFIED]
    print("  axon analogy: internode ~100 x fibre diameter [UNVERIFIED]; DRAM analogue: one 2T node per 32-64 cells")


# ==========================================================================================
# B5-11  DNA-brick nanotrench patterning (EUV-free 10 nm-pitch arrays)
# ==========================================================================================
def section_dna():
    hr("B5-11  DNA-BRICK NANOTRENCH TEMPLATES FOR THE CELL LATTICE")
    pitch = 10.4    # nm [REPORTED]
    yld = 0.95      # [REPORTED] assembly yield
    feats = N_BITS_DIE
    print(f"Pitch {pitch} nm reported (CNT arrays); 1b capacitor pitch is ~35 nm (A1) -> {35/pitch:.1f}x finer")
    print(f"Features per 16Gb die {feats:.1e}; at {yld:.0%} yield -> {feats*(1-yld):.1e} defects/die")
    for need in (1e-4, 1e-6):
        print(f"  needed defect rate {need:.0e}/feature (repair + on-die ECC) -> {(1-yld)/need:.0e}x improvement")
    thick_cm = 20e-7
    area_cm2 = math.pi * 15 ** 2
    mass_mg = area_cm2 * thick_cm * 1.7 * 1e3
    for usd_per_g in (200.0, 1e4):
        print(f"  DNA per wafer (20 nm layer, 1.7 g/cm3) = {mass_mg:.1f} mg -> ${mass_mg/1e3*usd_per_g:.2f}/wafer "
              f"at ${usd_per_g:.0f}/g [UNVERIFIED: bioreactor scaffold ~$200/g; synthetic oligos far higher]")
    for euv_layers, usd in [(5, 165.0), (7, 165.0)]:
        print(f"  replaces up to {euv_layers} EUV exposures at ~${usd:.0f} each (A1: $825-1,155/wafer) -> "
              f"${euv_layers*usd:.0f}/wafer of litho cost at risk")


# ==========================================================================================
# B5-12  Voltage-clocked skyrmion 'magnetic CCD'
# ==========================================================================================
def section_skyrmion():
    hr("B5-12  VOLTAGE-CLOCKED SKYRMION SHIFT REGISTER (bubble-memory revival, no lateral current)")
    for xi in (100e-15, 1000e-15):     # J/(V m) VCMA coefficient [ESTIMATE: 30-100 typical, 1000 aspirational]
        E = 1.0 / 1.5e-9
        dKs = xi * E
        r = 10e-9
        dE = dKs * math.pi * r ** 2
        print(f"  VCMA xi={xi*1e15:.0f} fJ/(V m), 1 V on 1.5 nm MgO: dK_s={dKs:.1e} J/m2 -> energy step for a "
              f"20 nm skyrmion {dE:.1e} J = {dE/kT():.0f} kT (need >> pinning, ~tens of kT)")
    for F in (13.4, 20.0):
        per_bit = 2 * F * 4 * F     # track pitch 2F x bit length 4F (2-phase, 2 gates/bit)
        print(f"  2-phase track at F={F} nm: {per_bit:.0f} nm2/bit/layer = {per_bit/CELL_1B_NM2:.2f}x 1b cell area")
    cg = EPS0 * 10 * (20e-9 * 40e-9) / 1.5e-9
    print(f"  gate C = {cg*1e18:.0f} aF -> {cg*1e18:.0f} aJ per gate toggle at 1 V; 64-bit track, avg 32 steps at 1 ns "
          f"-> {32:.0f} ns latency, ~{64*32*2*cg*1e15:.0f} fJ per random access")


# ==========================================================================================
# B5-13  Altermagnetic tunnel-junction RAM [SPECULATIVE]
# ==========================================================================================
def section_altermagnet():
    hr("B5-13  ALTERMAGNETIC TUNNEL-JUNCTION RAM")
    # stray-field-limited MRAM pitch vs stray-field-free
    for d in (20.0,):
        mram_pitch = 2.5 * d       # [ESTIMATE] dipolar interaction keeps ferromagnetic MTJs >= ~2.5 d apart
        am_pitch = 1.5 * d
        print(f"  MTJ d={d:.0f} nm: ferromagnet crosspoint pitch ~{mram_pitch:.0f} nm -> {mram_pitch**2:.0f} nm2/bit; "
              f"altermagnet ~{am_pitch:.0f} nm -> {am_pitch**2:.0f} nm2/bit ({mram_pitch**2/am_pitch**2:.1f}x denser; "
              f"{CELL_1B_NM2/am_pitch**2:.2f}x 1b cell density per deck)")
    print("  read: need TMR >= ~100% for ns sensing; experiments so far report spin-direction-dependent TMR in RuO2 "
          "(magnitude small, altermagnetism of RuO2 debated) [REPORTED]")
    print("  resource: Ru is A2-flagged (176% of world supply if used as fleet electrodes); prefer CrSb/MnTe if they work")


# ==========================================================================================
# B5-14  77 K oxide MLC gain-cell stage for cryogenic compute
# ==========================================================================================
def section_cryo77():
    hr("B5-14  77 K OXIDE MLC GAIN-CELL STAGE")
    pen_lo, pen_hi = 9.7, 19.3   # W wall per W removed at 77 K [A3 model section 6]
    v300, v77 = A1.INPUTS["v_array"], 0.4
    wl300, wl77 = A1.INPUTS["v_wl"], 1.0
    core300 = 5.9   # pJ per useful bit, random DDR5 activation [A1]
    scale = ((v77 / v300) ** 2 + (wl77 / wl300) ** 2) / 2
    core77 = core300 * scale
    print(f"Array-energy scale at 77 K (VARY {v300}->{v77} V, WL {wl300}->{wl77} V): x{scale:.2f} -> "
          f"{core77:.2f} pJ/useful bit cold")
    print(f"  wall-plug with cooling: {core77*pen_lo:.1f}-{core77*pen_hi:.1f} pJ/bit vs {core300} pJ/bit warm core: "
          f"wins only if the compute is already cold (no 300 K link)")
    print(f"  retention: IGZO 2T0C 8,000 s at 77 K [A3] -> refresh interval 64 ms -> 8,000 s = {8000/0.064:.0e}x fewer refreshes")
    for b in (2, 3, 4):
        print(f"  {b} b/cell oxide gain cell at 2.5x the 1T1C area -> {b/2.5:.1f}x 1b density per tier")
    snm = 2.6e6 / 100 / 1e9   # Gb/mm2 [REPORTED 2.6 Mb/cm2]
    print(f"  vs best 4 K superconducting memory array {snm:.1e} Gb/mm2 -> 1b-class density is {DENS_1B/snm:,.0f}x higher")


# ==========================================================================================
# B5-15  Superconducting kinetic-inductance memory, frequency-multiplexed readout
# ==========================================================================================
def section_snm():
    hr("B5-15  SUPERCONDUCTING NANOWIRE (KINETIC-INDUCTANCE) MEMORY")
    snm = 2.6e6 / 100 / 1e9
    print(f"Reported array density 2.6 Mb/cm2 = {snm:.1e} Gb/mm2 = 1/{DENS_1B/snm:,.0f} of DDR5 1b [REPORTED]")
    print(f"2018 cell 3 x 7 um = 21 um2, ~10 fJ per operation, BER < 1e-7 [REPORTED]")
    Rsq, Tc = 500.0, 10.0          # NbN-class film [ESTIMATE]
    delta = 1.764 * KB * Tc
    Lk = HBAR * Rsq / (math.pi * delta)
    print(f"Kinetic inductance L_k = hbar R_sq/(pi Delta) = {Lk*1e12:.0f} pH/sq (R_sq {Rsq} ohm, Tc {Tc} K)")
    for I_uA in (10.0, 30.0):
        L_need = PHI0 / (I_uA * 1e-6)
        sq = L_need / Lk
        print(f"  store one flux quantum at {I_uA:.0f} uA: L = {L_need*1e12:.0f} pH = {sq:.1f} squares "
              f"({sq*50:.0f} nm of 50 nm wire); energy I*Phi0 = {I_uA*1e-6*PHI0:.1e} J")
    for cell_um2 in (0.5, 0.1):
        d = 1e6 / cell_um2 * 0.5 / 1e9
        print(f"  scaled cell {cell_um2} um2 (loop + 2 hTrons), 0.5 eff -> {d:.4f} Gb/mm2 = 1/{DENS_1B/d:.0f} of DDR5")
    print(f"  4 K cooling penalty ~300-1000 W/W [ESTIMATE] -> 1e-17 J cold costs 3e-15 to 1e-14 J at the wall")


# ==========================================================================================
# B5-16  1T-TaS2 charge-density-wave cryomemory
# ==========================================================================================
def section_cdw():
    hr("B5-16  1T-TaS2 CHARGE-CONFIGURATION (CDW) CRYOMEMORY")
    e_density = 9.4e-15    # J/um2 [REPORTED]
    for side_nm in (50, 100):
        a = (side_nm * 1e-3) ** 2
        print(f"  {side_nm} x {side_nm} nm device: {e_density*a*1e18:.0f} aJ per switch, ~2 ps pulse [REPORTED scaling]")
    print("  intrinsic switching-time floor ~0.5 ps [REPORTED]; mechanism (thermal vs non-thermal) disputed [REPORTED]")
    for F in (20.0, 40.0):
        print(f"  crosspoint 4F2 at F={F:.0f} nm -> {4*F*F:.0f} nm2/bit = {CELL_1B_NM2/(4*F*F):.2f}x 1b density per deck")


# ==========================================================================================
# B5-17  Quantum-dot charge RAM at 4 K on spin-qubit process lines
# ==========================================================================================
def section_qdram():
    hr("B5-17  QUANTUM-DOT CHARGE RAM AT 4 K")
    r = 15e-9
    eps = 11.7 * EPS0
    C = 4 * math.pi * eps * r * 2      # self + gate/environment, x2 [ESTIMATE]
    Ec = Q ** 2 / (2 * C)
    print(f"Dot r=15 nm: C_sigma ~{C*1e18:.0f} aF, E_c = {Ec/Q*1e3:.1f} meV = {Ec/(KB*4.2):.0f} kT at 4.2 K "
          f"({Ec/(KB*77):.1f} kT at 77 K -> 4 K only)")
    print("  Coulomb blockade is NOT required: a bit = ~20 electrons vs 0, held by a pinched barrier; "
          f"a 50 meV barrier is {0.050*Q/(KB*4.2):.0f} kT at 4.2 K (thermal escape impossible) but "
          f"{0.050*Q/(KB*77):.1f} kT at 77 K")
    for cell_nm, eff in [(100, 0.5), (70, 0.5)]:
        d = 1e12 / cell_nm ** 2 * eff / 1e9
        print(f"  cell {cell_nm} x {cell_nm} nm, eff {eff}: {d:.3f} Gb/mm2 = {d/DENS_1B:.2f}x DDR5 1b, "
              f"{d/(2.6e6/100/1e9):,.0f}x the best superconducting array")
    cg = 10e-18
    for v in (0.05, 0.2):
        e = cg * v ** 2
        print(f"  gate write {cg*1e18:.0f} aF x ({v} V)^2 = {e*1e21:.1f} zJ; at ~500 W/W -> {e*500*1e18:.2f} aJ wall-plug")
    i_sense, t = 1e-9, 50e-9
    n = i_sense * t / Q
    print(f"  shared SET sensor at {i_sense*1e9:.0f} nA for {t*1e9:.0f} ns integrates {n:.0f} electrons "
          f"(shot-noise SNR ~{math.sqrt(n):.0f})")


# ==========================================================================================
# B5-18  TSV-free inductive (ThruChip-style) memory stacks
# ==========================================================================================
def section_inductive():
    hr("B5-18  TSV-FREE INDUCTIVE STACKING")
    bw = 2048 * 8e9
    link = 8.5e9            # b/s per link [REPORTED HC2022 7 nm poster]
    n_links = bw / link
    print(f"HBM4-class 2048 x 8 Gb/s = {bw/1e12:.1f} Tb/s -> {n_links:.0f} inductive links at 8.5 Gb/s")
    for die_um, stack in [(30.0, 16), (10.0, 16), (10.0, 4)]:
        reach = die_um * (stack - 1)
        D = max(reach, 3 * die_um)          # coil diameter ~ coupling distance [ESTIMATE rule of thumb]
        area = n_links * (1.2 * D) ** 2 / 1e6
        print(f"  dies {die_um:.0f} um thick, {stack}-high, direct reach {reach:.0f} um -> coil ~{D:.0f} um -> "
              f"{area:.0f} mm2 of coil area per die")
    hop = 0.9
    print(f"  relay alternative: {hop} pJ/b per chip hop [REPORTED] -> 16-high top die {15*hop:.1f} pJ/b vs HBM ~3-4 pJ/b total [A1]")
    print(f"  4-high memory-on-logic: {3*hop:.1f} pJ/b worst hop; reported -26% die area vs TSV (7 nm SRAM stack)")


# ==========================================================================================
# B5-R  Arithmetic behind the REJECTED ideas (see B5-firstprinciples_notes.md)
# ==========================================================================================
def section_rejected():
    hr("B5-R  REJECTED IDEAS: the numbers that killed them (each has a revival condition in the notes)")
    # R1 acoustic delay line
    v, rate = 5000.0, 10e9           # m/s (AlN-class), bits/s
    bit_len = v / rate
    width = 1e-6
    d = 1 / (bit_len * width) / 1e6 / 1e9   # Gb/mm2
    print(f"R1 acoustic delay line @10 Gb/s: bit length {bit_len*1e6:.2f} um, 1 um-wide line -> {d*1e3:.1f} Mb/mm2 "
          f"= 1/{DENS_1B/d:.0f} of DDR5; 1 mm line = {1e-3/bit_len:.0f} bits, {1e-3/v*1e9:.0f} ns loop")
    # R2 optical bistable nanocavity
    lam, n = 1550e-9, 3.48
    cell = (lam / (2 * n)) ** 2
    print(f"R2 optical cavity at the diffraction limit: {(cell)*1e12:.3f} um2 -> {1e-6/cell/1e6:.0f} Mb/mm2 "
          f"(1/{DENS_1B/(1e-6/cell/1e9):.0f} of DDR5 before any waveguides); holding 30 nW/bit -> {30e-9*1e9:.0f} W per Gb")
    # R3 frequency-multiplexed NEMS resonator bits
    E, f, Qm = 1e-17, 1e9, 1e4
    p = E * 2 * math.pi * f / Qm
    print(f"R3 resonator bit (E 1e-17 J, 1 GHz, Q 1e4): {p*1e12:.1f} pW/bit vs DRAM refresh 0.72 pW/bit @64 ms; "
          f"Q 1e6 needed to reach {p*1e12/100:.2f} pW")
    # R4 thermally gated write (single Arrhenius barrier)
    tau0 = 1e-13
    for t_hold in (1.0, 1e6):
        Eb = kT_eV(T_RT) * math.log(t_hold / tau0)            # minimum barrier for the hold time at 300 K
        T2 = Eb * Q / (KB * math.log(1e-9 / tau0))            # temperature giving a 1 ns hop over that barrier
        print(f"R4 heat-as-gate: hold {t_hold:.0e} s at 300 K needs Eb >= {Eb:.2f} eV; a 1 ns write over it needs "
              f"T_write = {T2:.0f} K (single Arrhenius barrier, tau0 0.1 ps)")
    # R5 quantum-paraelectric SrTiO3 cryo capacitor
    for k, t in ((20000, 20e-9), (2000, 100e-9)):
        c = EPS0 * k * (40e-9) ** 2 / t
        print(f"R5 planar STO k={k}, t={t*1e9:.0f} nm, 40x40 nm: {c*1e15:.2f} fF (field at 1 V = {1/t/1e5:.0f} kV/cm; "
              f"STO k collapses at tens of kV/cm)")
    # R6 via-threaded nanoring 'core memory'
    for I in (100e-6, 1e-3):
        H = I / (2 * math.pi * 25e-9)
        print(f"R6 nanoring core: {I*1e6:.0f} uA through a via, r=25 nm -> H = {H:.0f} A/m = {H*4*math.pi*1e-3:.0f} Oe")
    phi = 4 * math.pi * 1e-7 * 1e6 * (5e-9 * 20e-9)
    print(f"   induction read: flux {phi:.1e} Wb switched in 1 ns -> {phi/1e-9*1e6:.2f} uV")
    # R7 nanofluidic ion bit without a binding barrier
    D = 5e-8 * 0.02585
    print(f"R7 aqueous ion over 10 nm: drift at 1 V/10 nm {5e-8*1e8:.0f} m/s ({10e-9/(5e-8*1e8)*1e9:.0f} ns) but "
          f"diffusive loss in {(10e-9)**2/D*1e9:.0f} ns without a binding barrier")
    # R8 'ballistic' or superconducting bitlines
    print("R8 bitline capacitance per length (~0.15-0.2 fF/um) is geometric: conductor material cannot lower it")


def main():
    print("B5_firstprinciples_estimates.py -- dram-moonshot phase B, lens 5 (first principles & wild cards)")
    print(f"Anchors [A1]: 1b cell {CELL_1B_NM2:.0f} nm2, array eff {ARRAY_EFF}, {DENS_1B} Gb/mm2, "
          f"Cs {CS_1B_FF} fF, Cbl(512) {CBL_512_FF:.1f} fF, refresh {E_REF_FJ:.1f} fJ/bit")
    section_floor()
    section_click()
    section_racetrack()
    section_deeplevel()
    section_jot()
    section_crested()
    section_ultraram()
    section_nems_selector()
    section_adiabatic()
    section_negcap()
    section_myelin()
    section_dna()
    section_skyrmion()
    section_altermagnet()
    section_cryo77()
    section_snm()
    section_cdw()
    section_qdram()
    section_inductive()
    section_rejected()
    return 0


if __name__ == "__main__":
    sys.exit(main())
