#!/usr/bin/env python3
"""
diode-tower.py -- first-principles model for the DIODE-TOWER concept (dram-moonshot stage 3, rank 6).

Owner: dos-diode-tower. Written 2026-11-02. Pure standard library. Run from dram-moonshot/:
    python3 models/diode-tower.py
It prints a markdown report and writes it to research/stage3/diode-tower_model_output.md.

Cell (per pillar, bottom to top):
    n tiers of [TiN plate | ZrO2 | recessed metal-oxide node ring (Schottky anode) ] around one hole;
    in the hole: a thin IGZO shell (Schottky cathode semiconductor) on a metal core = the shared pillar;
    on top: one IGZO access transistor (pillar <-> write bitline) and one IGZO gain FET whose gate is the pillar,
    read through a select device with correlated double sampling (CDS).
Read tier k: float the pillar, pulse plate k by dV_PL; node k is pushed above the pillar and dumps its charge
through its forward-biased diode; the pillar swing (gain FET, CDS) is the signal. Write-back = clamp-write:
drive the pillar to the data level while plate k is still high, then drop plate k.

What this model computes (each section prints a table):
  1. Geometry -> storage capacitance Cs, diode area and capacitance, pillar capacitance, pitch and footprint.
  2. Signal, noise, sigma margin and raw BER vs tier count.
  3. Density (user Gb/mm2) vs tier count, vs 1-beta DDR5 0.447 Gb/mm2.
  4. Diode physics: thermionic leakage, image-force and thermionic-field lowering in a thin coaxial shell.
  5. Barrier inhomogeneity (Gaussian patches, Monte Carlo) -> 1e-4 tail leakage per tier.
  6. Sensitivity table on the key unknown (mean effective barrier x patch sigma) -> tail retention.
  7. Write: forward voltage, plate swing, write disturb rule.
  8. Energy per access and refresh power vs DDR5.
  9. Cost per bit vs $1.48/GB DDR5.
 10. Endurance budget (forward pulses and charge fluence per diode).
 11. GO / NO-GO thresholds for the decisive coupon experiment.

Every INPUTS value carries a source URL or "ESTIMATE: basis". Sources: research/sources/dos-diode-tower.jsonl.
"""

import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_MD = os.path.normpath(os.path.join(HERE, "..", "research", "stage3", "diode-tower_model_output.md"))

# physical constants (SI)
Q = 1.602176634e-19
KB = 1.380649e-23
KB_EV = 8.617333262e-5
EPS0 = 8.8541878128e-12
HBAR = 1.054571817e-34
M0 = 9.1093837015e-31

# --------------------------------------------------------------------------------------------
# INPUTS: name -> (value, unit, source)
# --------------------------------------------------------------------------------------------
INPUTS = {
    # ---- baselines
    "d_1b_gb_mm2": (0.447, "Gb/mm2", "A1_scaling_limits.md: Micron D1b 16Gb 35.83 mm2 (TechInsights via ram-venture cost_stack)"),
    "wafer_1b_usd": (3800.0, "$", "A1_scaling_limits.md / ram-venture models/dram_cost_stack.py: 1-beta wafer $3.8k"),
    "cost_1b_usd_gb": (1.48, "$/GB", "A1_scaling_limits.md / ram-venture dram_cost_stack.py: $1.48/GB"),
    "e_dram_bit_fJ": (46.0, "fJ/bit", "models/dram_cell_physics.py refresh_energy_per_bit_fJ() (re-imported below if available)"),
    # ---- geometry
    "hole_d_nm": (60.0, "nm", "ESTIMATE: FINAL_CONCEPTS planning case '~60 nm holes' (critic-corrected)"),
    "igzo_shell_nm": (15.0, "nm", "ESTIMATE: concept did not specify; 15 nm keeps the anode field ~0.8 MV/cm in a 60 nm hole (section 4)"),
    "e_lowfield_V_per_nm": (0.02, "V/nm", "ESTIMATE: ~0.2 MV/cm interface field of the thick, lightly doped films behind literature barrier values"),
    "node_radial_nm": (15.0, "nm", "ESTIMATE: lateral recess depth for the node ring, FG-3D-NAND-style recess"),
    "zro2_nm": (5.5, "nm", "A1_scaling_limits.md: ZrO2 stack 6-7 nm physical, EOT ~0.55 nm"),
    "k_zro2": (40.0, "-", "A1_scaling_limits.md: ZrO2/HfO2 k ~35-45"),
    "plate_nm": (25.0, "nm", "ESTIMATE: TiN plate tier thickness (sets node height = plate - 2 x ZrO2)"),
    "ild_nm": (25.0, "nm", "ESTIMATE: inter-tier SiO2"),
    "plate_web_nm": (20.0, "nm", "ESTIMATE: minimum continuous plate metal between neighbouring recesses"),
    "slit_nm": (60.0, "nm", "ESTIMATE: plate-segment slit width (3D-NAND-like block slit)"),
    "rows_per_plate": (4, "rows", "ESTIMATE: pillar rows sharing one plate segment (a page = all pillars on a segment)"),
    "eps_igzo": (12.0, "-", "ESTIMATE: a-IGZO static permittivity ~10-16 (training knowledge)"),
    "m_eff_igzo": (0.34, "m0", "ESTIMATE: a-IGZO electron effective mass ~0.3-0.35 m0 (training knowledge)"),
    "c_gain_fF": (0.25, "fF", "ESTIMATE: vertical IGZO gain-FET gate, 60 nm dia x 50 nm, 6 nm HfO2"),
    "c_access_fF": (0.10, "fF", "ESTIMATE: access-transistor source junction/overlap"),
    "c_top_fF": (0.10, "fF", "ESTIMATE: pillar top wiring"),
    "c_fringe_tier_fF": (0.005, "fF", "ESTIMATE: pillar core to plate fringe through ILD per tier"),
    # ---- electrical
    "v_data": (0.5, "V", "FINAL_CONCEPTS step_change: 0.5 V data swing"),
    "m_rev": (0.2, "V", "ESTIMATE: reverse-bias guard so no unselected node ever forward-biases"),
    "t_write_ns": (10.0, "ns", "FINAL_CONCEPTS: <=10-20 ns write"),
    "ideality": (1.3, "-", "PtOx/ZnO n=1.31 (https://livrepository.liverpool.ac.uk/3015044/); IGZO SBD n=1.35 (PKU poster, sources log)"),
    "sigma_cds_mV": (7.0, "mV", "ESTIMATE: midpoint of concept's 5-10 mV post-CDS residual (PIXEL-STACK/MARGIN-STACK key unknown)"),
    "droop_mV": (100.0, "mV", "FINAL_CONCEPTS: 100 mV node droop budget"),
    "ber_target": (1e-4, "-", "RAW-BER CONTRACT: BCH t=8 per 512 b at raw BER 1e-4 (stage2 I-11559)"),
    "ecc_rawber": ((512 + 80) / 512, "-", "stage2 I-11559: 80 check bits per 512 data bits"),
    "array_eff": (0.55, "-", "FINAL_CONCEPTS/A1: 0.5-0.6 for CMOS-under-array 3D"),
    "ref_tiers": (1, "tiers", "ESTIMATE: one reference tier per pillar for threshold tracking"),
    "spare_per_32": (1, "tiers", "ESTIMATE: one spare tier per 32 for repair"),
    "temp_c": (85.0, "C", "JEDEC normal range top; DRAM retention spec point"),
    # ---- barrier statistics (the key unknown)
    "phi_best_igzo_eV": (0.92, "eV", "Pt-IGZO with O2 during deposition, n=1.36 (secondary, https://publikationen.bibliothek.kit.edu/1000121423/82897741)"),
    "phi_igzo_passivated_eV": (0.82, "eV", "SiO2-passivated a-IGZO SBD (PKU poster, sources log)"),
    "phi_agox_zno_eV": (1.10, "eV", "AgOx/ZnO 1.00-1.20 eV (https://www2.avs.org/symposium2008/Papers/Paper_EM-TuM3.html)"),
    "sigma_patch_eV": (0.05, "eV", "ESTIMATE: patch-barrier sigma after pinch-off; Gaussian-inhomogeneity literature spans ~0.03-0.15 eV"),
    "eps_if": (4.0, "-", "ESTIMATE: optical permittivity n^2 ~4 for image force (fast electrons); 12 (static) is the optimistic bound"),
    # ---- cost / energy
    "base_wafer_usd": (3000.0, "$", "A1 section 6 base 3D scenario (CMOS-under-array + top layers)"),
    "usd_per_tier": (25.0, "$/tier", "ESTIMATE: between A1 optimistic $20 and base $30 (2 depositions/tier, no per-tier litho)"),
    "tier_yield": (0.998, "-", "A1 section 6: >=0.998 per tier after repair needed"),
    "c_rbl_fF": (15.0, "fF", "ESTIMATE: read bitline, 128 pillars x 0.08 fF + 5 fF"),
    "c_wbl_fF": (15.0, "fF", "ESTIMATE: write bitline, same loading"),
    "dv_rbl": (0.15, "V", "ESTIMATE: read-bitline swing for the CDS comparator"),
    "vdd": (1.1, "V", "ESTIMATE: periphery supply"),
    "c_wl_fF": (0.15, "fF", "dram_cell_physics.py c_wl_per_cell_fF"),
    "v_wl": (2.5, "V", "ESTIMATE: IGZO access WL high"),
    "pump_eff": (0.45, "-", "dram_cell_physics.py pump_eff"),
    "periph_overhead": (2.0, "-", "dram_cell_physics.py periph_overhead"),
    # ---- endurance
    "hot_row_cycles_10y": (7e13, "cycles", "C0 triage: ~7e13 for a hot row at 1% duty in 10 years"),
}


def V(name):
    return INPUTS[name][0]


LINES = []


def out(s=""):
    print(s)
    LINES.append(s)


def kT_eV(tc):
    return KB_EV * (tc + 273.15)


def richardson(m_eff):
    """A* in A/cm^2/K^2 = 120.17 x m*/m0."""
    return 4 * math.pi * Q * m_eff * M0 * KB ** 2 / (2 * math.pi * HBAR) ** 3 * 1e-4


A_STAR = richardson(V("m_eff_igzo"))


def thermionic_A(phi_eV, area_um2, tc):
    t = tc + 273.15
    return area_um2 * 1e-8 * A_STAR * t * t * math.exp(-phi_eV / kT_eV(tc))


def phi_for_current(i_A, area_um2, tc):
    t = tc + 273.15
    return kT_eV(tc) * math.log(area_um2 * 1e-8 * A_STAR * t * t / i_A)


def fmt_t(s):
    if s < 1e-6:
        return f"{s*1e9:.0f} ns"
    if s < 1e-3:
        return f"{s*1e6:.0f} us"
    if s < 1:
        return f"{s*1e3:.0f} ms"
    if s < 1e3:
        return f"{s:.1f} s"
    return f"{s:.1e} s"


def qfunc(z):
    return 0.5 * math.erfc(z / math.sqrt(2))


def qinv(p):
    lo, hi = 0.0, 12.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if qfunc(mid) > p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


# --------------------------------------------------------------------------------------------
# 1. Geometry
# --------------------------------------------------------------------------------------------
def geometry(hole_d=None, shell=None, plate=None, wrap=False):
    hole_d = hole_d or V("hole_d_nm")
    shell = shell or V("igzo_shell_nm")
    plate = plate or V("plate_nm")
    rh = hole_d / 2
    rc = rh - shell
    rb = rh + V("node_radial_nm")
    t = V("zro2_nm")
    hn = plate - 2 * t                     # node height (ZrO2 lines top and bottom of the recess)
    eps_d = EPS0 * V("k_zro2")
    # storage cap: back wall coax (node outer radius rb -> plate at rb + t)
    cs = 2 * math.pi * eps_d * hn * 1e-9 / math.log((rb + t) / rb)
    if wrap:  # plate wraps node top and bottom (TiN/SiN/TiN tier, SiN recessed) -> add two annuli
        cs += 2 * eps_d * math.pi * ((rb * 1e-9) ** 2 - (rh * 1e-9) ** 2) / (t * 1e-9)
    aj_um2 = 2 * math.pi * rh * hn * 1e-6   # ring diode on the hole face
    cj = 2 * math.pi * EPS0 * V("eps_igzo") * hn * 1e-9 / math.log(rh / rc)
    c_unsel = 1 / (1 / cj + 1 / cs) + V("c_fringe_tier_fF") * 1e-15
    pitch = hole_d + 2 * (V("node_radial_nm") + t) + V("plate_web_nm")
    a_sq = (pitch * 1e-3) ** 2
    slit = 1 + V("slit_nm") / (V("rows_per_plate") * pitch)
    return dict(rh=rh, rc=rc, rb=rb, hn=hn, cs=cs, aj=aj_um2, cj=cj, c_unsel=c_unsel, pitch=pitch,
                a_fp=a_sq * slit, a_sq=a_sq, slit=slit, shell=shell, hole_d=hole_d, plate=plate)


def c_pillar(g, n):
    return ((n - 1) * g["c_unsel"] + (V("c_gain_fF") + V("c_access_fF") + V("c_top_fF")) * 1e-15)


def section_geometry():
    out("## 1. Geometry -> capacitances and footprint")
    g = geometry()
    gw = geometry(wrap=True)
    out(f"Hole {g['hole_d']:.0f} nm, IGZO shell {g['shell']:.0f} nm (metal core radius {g['rc']:.0f} nm), node ring "
        f"{V('node_radial_nm'):.0f} nm radial x {g['hn']:.1f} nm tall, ZrO2 {V('zro2_nm')} nm k={V('k_zro2'):.0f}, "
        f"tier pitch {V('plate_nm') + V('ild_nm'):.0f} nm.")
    out("")
    out("| Quantity | Value | Note |")
    out("|---|---|---|")
    out(f"| Storage cap Cs (back-wall ring) | {g['cs']*1e15:.3f} fF | concept assumed 0.27 fF |")
    out(f"| Cs with plate wrapping node top+bottom | {gw['cs']*1e15:.3f} fF | TiN/SiN/TiN tier option, +1 deposition per tier |")
    out(f"| Stored charge for 0.5 V | {g['cs']*V('v_data')/Q:.0f} e- | DRAM 1-beta ~17,700 e- (C0) |")
    out(f"| Diode ring area Aj | {g['aj']*1e6:.0f} nm2 ({g['aj']:.4f} um2) | concept range 0.002-0.0057 um2 |")
    out(f"| Diode (depleted shell) capacitance | {g['cj']*1e15:.3f} fF | coaxial, fully depleted IGZO |")
    out(f"| Unselected-tier load on pillar | {g['c_unsel']*1e15:.3f} fF/tier | Cj in series with Cs, + fringe |")
    for n in (16, 32, 64):
        out(f"| Pillar capacitance, {n} tiers | {c_pillar(g, n)*1e15:.2f} fF | concept assumed ~1.5 fF |")
    out(f"| Hole pitch | {g['pitch']:.0f} nm | hole + 2 x (recess + ZrO2) + plate web |")
    out(f"| Footprint per pillar (square, incl. slit every {V('rows_per_plate')} rows) | {g['a_fp']:.4f} um2 | "
        f"concept assumed 0.010-0.012 um2; slit factor {g['slit']:.3f} |")
    out("")
    out("Insight: the fully depleted shell makes each unselected tier load the pillar by only ~"
        f"{g['c_unsel']*1e15:.3f} fF, so the pillar is lighter than the concept assumed at 16-32 tiers; but the recess "
        "ring needed for a ~0.25 fF capacitor pushes the pitch to ~"
        f"{g['pitch']:.0f} nm, so the footprint is ~{g['a_fp']/0.011:.1f}x the concept's.")
    out("")
    return g


# --------------------------------------------------------------------------------------------
# 2. Signal, noise and raw BER
# --------------------------------------------------------------------------------------------
def signal_noise(g, n, sigma_cds_mV=None, droop_mV=None, tc=None):
    sigma_cds_mV = V("sigma_cds_mV") if sigma_cds_mV is None else sigma_cds_mV
    droop_mV = V("droop_mV") if droop_mV is None else droop_mV
    tc = V("temp_c") if tc is None else tc
    cs, cp = g["cs"], c_pillar(g, n)
    ctot = cs + cp
    dv_fresh = cs * V("v_data") / ctot
    dv_end = cs * (V("v_data") - droop_mV / 1e3) / ctot
    kt = KB * (tc + 273.15)
    s_ktc = math.sqrt(kt / ctot)
    s_diode = math.sqrt(2 * kt / (2 * cs)) * cs / ctot      # soft-reset noise of node, write + read
    sigma = math.sqrt((sigma_cds_mV / 1e3) ** 2 + s_ktc ** 2 + s_diode ** 2)
    z = dv_end / (2 * sigma)
    return dict(cp=cp, dv_fresh=dv_fresh, dv_end=dv_end, s_ktc=s_ktc, s_diode=s_diode, sigma=sigma, z=z,
                ber=qfunc(z))


def section_signal(g):
    out("## 2. Signal, noise and raw BER vs tier count")
    out(f"Signal = Cs x Vdata / (Cs + Cpillar). Decision margin z = (end-of-retention signal / 2) / sigma_total, "
        f"sigma_total = sqrt(CDS residual^2 + kT/C + diode soft-reset noise). Raw-BER target {V('ber_target'):.0e} "
        f"needs z >= {qinv(V('ber_target')):.2f}.")
    out("")
    out("| Tiers | Cpillar fF | Fresh signal mV | After 100 mV droop mV | kT/C mV | sigma_total mV | z | raw BER |")
    out("|---|---|---|---|---|---|---|---|")
    for n in (8, 16, 24, 32, 48, 64, 96, 128):
        r = signal_noise(g, n)
        out(f"| {n} | {r['cp']*1e15:.2f} | {r['dv_fresh']*1e3:.1f} | {r['dv_end']*1e3:.1f} | {r['s_ktc']*1e3:.2f} | "
            f"{r['sigma']*1e3:.2f} | {r['z']:.2f} | {r['ber']:.1e} |")
    out("")
    out("Correction to the concept's arithmetic: the concept compared signal/sigma (7-15) with BCH t=8's 3.72 sigma, "
        "but 3.72 is the half-margin (signal/2) requirement. Signal/(2 sigma) is the right comparison, which halves "
        "the quoted margin.")
    out("")
    out("CDS residual tolerance (max tiers with z >= 3.72 at end of retention):")
    out("")
    out("| CDS residual mV | max tiers (back-wall Cs) | max tiers (wrapped Cs) |")
    out("|---|---|---|")
    gw = geometry(wrap=True)
    zreq = qinv(V("ber_target"))
    for s in (3, 5, 7, 10, 15):
        res = []
        for gg in (g, gw):
            nmax = 0
            for n in range(2, 513):
                if signal_noise(gg, n, sigma_cds_mV=s)["z"] >= zreq:
                    nmax = n
            res.append(nmax)
        out(f"| {s} | {res[0]} | {res[1]} |")
    out("")


# --------------------------------------------------------------------------------------------
# 3. Density
# --------------------------------------------------------------------------------------------
def bits_per_pillar(n):
    spares = math.ceil(n / 32) * V("spare_per_32")
    return n - V("ref_tiers") - spares


def density(g, n):
    return 1e6 / g["a_fp"] * bits_per_pillar(n) * V("array_eff") / V("ecc_rawber") / 1e9


def section_density(g):
    out("## 3. Density vs tier count")
    out(f"User Gb/mm2 = (1e6 / footprint um2) x (tiers - reference - spares) x array efficiency {V('array_eff')} / "
        f"ECC {V('ecc_rawber'):.3f}. Baseline 1-beta DDR5 = {V('d_1b_gb_mm2')} Gb/mm2.")
    out("")
    out("| Tiers | bits/pillar | Stack height um | Hole AR | Gb/mm2 (60 nm hole) | x 1-beta | Gb/mm2 (concept 0.011 um2) | x 1-beta |")
    out("|---|---|---|---|---|---|---|---|")
    tier_pitch = V("plate_nm") + V("ild_nm")
    for n in (8, 16, 24, 32, 48, 64, 96, 128):
        d = density(g, n)
        d_c = 1e6 / 0.011 * bits_per_pillar(n) * V("array_eff") / V("ecc_rawber") / 1e9
        h = n * tier_pitch / 1e3
        out(f"| {n} | {bits_per_pillar(n)} | {h:.2f} | {h*1e3/g['hole_d']:.0f} | {d:.3f} | {d/V('d_1b_gb_mm2'):.2f} | "
            f"{d_c:.3f} | {d_c/V('d_1b_gb_mm2'):.2f} |")
    n_par = next(n for n in range(2, 400) if density(g, n) >= V("d_1b_gb_mm2"))
    n_3x = next(n for n in range(2, 400) if density(g, n) >= 3 * V("d_1b_gb_mm2"))
    out("")
    out(f"Density parity with 1-beta at {n_par} tiers; 3x at {n_3x} tiers (this geometry). The concept's "
        "'2x at 16 tiers' needs the 0.011 um2 footprint, which leaves no room for the recess ring at 60 nm holes.")
    out("")
    return n_par, n_3x


# --------------------------------------------------------------------------------------------
# 4. Diode physics: thermionic leakage and barrier lowering in a thin coaxial shell
# --------------------------------------------------------------------------------------------
def field_at_anode(v_total, rh_nm, rc_nm):
    """Charge-free coaxial field at the outer (anode) radius, V/m."""
    return v_total / (rh_nm * 1e-9 * math.log(rh_nm / rc_nm))


def lowering(phi0, v_rev, shell_nm, tc, eps_if=None, xi=0.1, rh_nm=None):
    """Image-force + thermionic-field-emission lowering (eV) at the anode of a fully depleted shell."""
    eps_if = V("eps_if") if eps_if is None else eps_if
    rh = rh_nm or V("hole_d_nm") / 2
    rc = rh - shell_nm
    e = field_at_anode(phi0 - xi + v_rev, rh, rc)
    d_if = math.sqrt(Q * e / (4 * math.pi * EPS0 * eps_if))
    c = 4 * math.sqrt(2 * V("m_eff_igzo") * M0) * math.sqrt(Q) / (3 * HBAR * e)   # eV^-1.5
    de = (1 / (1.5 * c * kT_eV(tc))) ** 2
    d_tfe = min(de / 3, 0.5 * phi0)
    return e, d_if, d_tfe


def lowering_at_field(e, tc, eps_if=None):
    eps_if = V("eps_if") if eps_if is None else eps_if
    d_if = math.sqrt(Q * e / (4 * math.pi * EPS0 * eps_if))
    c = 4 * math.sqrt(2 * V("m_eff_igzo") * M0) * math.sqrt(Q) / (3 * HBAR * e)
    de = (1 / (1.5 * c * kT_eV(tc))) ** 2
    return d_if + de / 3


def tier_eff_from_lowfield(phi_lf, shell_nm, tc, v_rev=None, eps_if=None, rh_nm=None):
    """Effective barrier a tier sees, given the barrier a thick-film (low-field) diode would report."""
    v_rev = V("v_data") + V("m_rev") if v_rev is None else v_rev
    e_lf = V("e_lowfield_V_per_nm") * 1e9
    l_lf = lowering_at_field(e_lf, tc, eps_if)
    phi0 = phi_lf + l_lf                      # zero-field barrier
    e, d_if, d_tfe = lowering(phi0, v_rev, shell_nm, tc, eps_if=eps_if, rh_nm=rh_nm)
    return phi0 - d_if - d_tfe


def lowfield_needed(phi_eff_req, shell_nm, tc, eps_if=None, rh_nm=None):
    lo, hi = 0.3, 3.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if tier_eff_from_lowfield(mid, shell_nm, tc, eps_if=eps_if, rh_nm=rh_nm) < phi_eff_req:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def i_budget(g, t_ref, droop_mV=None):
    droop_mV = V("droop_mV") if droop_mV is None else droop_mV
    return g["cs"] * droop_mV / 1e3 / t_ref


def section_diode(g):
    out("## 4. Diode physics: leakage budget and thin-shell barrier lowering")
    tc = V("temp_c")
    out(f"Thermionic reverse current I = Aj x A* x T^2 x exp(-phi_eff/kT), A* = {A_STAR:.1f} A/cm2K2 "
        f"(m* = {V('m_eff_igzo')} m0), Aj = {g['aj']:.4f} um2, T = {tc:.0f} C. Budget I <= Cs x droop / t_refresh.")
    out("")
    out("| Refresh interval | Leakage budget per tier | Required homogeneous phi_eff (85 C) | Required at 95 C |")
    out("|---|---|---|---|")
    for t_ref, lab in ((0.032, "32 ms (JEDEC >85 C)"), (0.064, "64 ms (JEDEC)"), (0.256, "256 ms"),
                       (1.0, "1 s (concept target)"), (10.0, "10 s")):
        ib = i_budget(g, t_ref)
        out(f"| {lab} | {ib*1e18:.0f} aA | {phi_for_current(ib, g['aj'], tc):.3f} eV | "
            f"{phi_for_current(ib, g['aj'], 95):.3f} eV |")
    out("")
    out("Leakage per tier for a homogeneous effective barrier (85 C):")
    out("")
    out("| phi_eff eV | I per tier aA | Retention (100 mV) |")
    out("|---|---|---|")
    for phi in (0.80, 0.85, 0.90, 0.92, 0.95, 1.00, 1.05, 1.10):
        i = thermionic_A(phi, g["aj"], tc)
        out(f"| {phi:.2f} | {i*1e18:.2f} | {fmt_t(g['cs']*0.1/i)} |")
    out("")
    out("Thin-shell lowering. A thin IGZO shell between the node (anode) and an ohmic core is fully depleted, so the "
        "field at the anode is ~(Vbi + Vrev)/shell, not the ~0.2 MV/cm of a thick lightly doped film. Image-force "
        "lowering sqrt(qE/(4 pi eps)) and thermionic-field emission through the thin barrier top (WKB, triangular "
        "barrier, optimum energy dE* = (1.5 c kT)^-2, lowering dE*/3) both scale with that field. Zero-field "
        "barrier 1.20 eV, worst hold reverse bias = Vdata + guard = "
        f"{V('v_data') + V('m_rev'):.1f} V, 85 C:")
    out("")
    out("| Shell nm | Field MV/cm | Image force (eps 4) eV | Image force (eps 12) eV | TFE eV | Total (eps 4) eV | Total (eps 12) eV |")
    out("|---|---|---|---|---|---|---|")
    vr = V("v_data") + V("m_rev")
    for sh in (5, 8, 10, 15, 20):
        e, dif4, dtfe = lowering(1.20, vr, sh, tc, eps_if=4)
        _, dif12, _ = lowering(1.20, vr, sh, tc, eps_if=12)
        out(f"| {sh} | {e/1e8:.2f} | {dif4:.3f} | {dif12:.3f} | {dtfe:.3f} | {dif4+dtfe:.3f} | {dif12+dtfe:.3f} |")
    out("")
    e, dif, dtfe = lowering(1.20, vr, g["shell"], tc)
    l_lf = lowering_at_field(V("e_lowfield_V_per_nm") * 1e9, tc)
    out(f"At the design shell ({g['shell']:.0f} nm) the hold-state barrier is ~{dif+dtfe:.2f} eV below the zero-field "
        "barrier (eps 4; ~"
        f"{lowering(1.20, vr, g['shell'], tc, eps_if=12)[1] + dtfe:.2f} eV with eps 12), against ~{l_lf:.2f} eV in a "
        "thick-film diode at ~0.2 MV/cm. Image force uses the optical permittivity (~4) because an electron crosses "
        "the ~1 nm to the barrier maximum in ~10 fs, faster than the lattice polarises; eps 12 is the optimistic bound. "
        "The TFE term uses a triangular-barrier WKB estimate and is uncertain to ~+/-50%. The literature's "
        "barriers (0.75-0.92 eV on IGZO, up to 1.0-1.2 eV for AgOx on ZnO) come from thick-film diodes at low field, "
        "so they overstate what a tier will see. Coupons must be thin-shell vertical diodes at the design thickness.")
    out("")
    return dif + dtfe


# --------------------------------------------------------------------------------------------
# 5. Barrier inhomogeneity Monte Carlo
# --------------------------------------------------------------------------------------------
def tail_factor(sigma_eV, n_patch, tc, q_tail, n_diodes, rng):
    """Quantile (1 - q_tail) of S = mean_i exp(-d_i/kT), d_i ~ N(0, sigma). S = 1 for a homogeneous barrier."""
    if sigma_eV <= 0:
        return 1.0, 1.0
    kt = kT_eV(tc)
    vals = []
    for _ in range(n_diodes):
        s = 0.0
        for _ in range(n_patch):
            s += math.exp(-rng.gauss(0.0, sigma_eV) / kt)
        vals.append(s / n_patch)
    vals.sort()
    idx = min(len(vals) - 1, int(math.floor((1 - q_tail) * len(vals))))
    mean = sum(vals) / len(vals)
    return vals[idx], mean


def section_inhomogeneity(g):
    out("## 5. Barrier inhomogeneity: the per-tier leakage tail")
    tc = V("temp_c")
    patch_nm = g["shell"]          # pinch-off length ~ shell thickness -> patch ~ shell x shell
    n_patch = max(1, round(g["aj"] * 1e6 / (patch_nm * patch_nm)))
    q_tail = V("ber_target")
    rng = random.Random(20261102)
    n_diodes = 40000
    out(f"Each ring diode is modelled as {n_patch} parallel patches ({patch_nm:.0f} x {patch_nm:.0f} nm, the pinch-off "
        "scale of a depleted shell), each with a Gaussian barrier around the mean (Werner-Guttler/Tung picture). "
        f"Monte Carlo of {n_diodes:,} diodes per sigma (seed fixed) gives the {1-q_tail:.4%} leakage quantile, the "
        "tier that the raw-BER-1e-4 contract must still read correctly.")
    out("")
    out("| Patch sigma eV | Mean leakage multiplier | 1e-4 tail multiplier | Tail barrier penalty eV | "
        "Mean phi_eff needed, 64 ms | Mean phi_eff needed, 1 s |")
    out("|---|---|---|---|---|---|")
    req = {}
    for sig in (0.0, 0.03, 0.05, 0.07, 0.10):
        tf, mean = tail_factor(sig, n_patch, tc, q_tail, n_diodes, rng)
        pen = kT_eV(tc) * math.log(tf)
        r64 = phi_for_current(i_budget(g, 0.064), g["aj"], tc) + pen
        r1 = phi_for_current(i_budget(g, 1.0), g["aj"], tc) + pen
        req[sig] = (r64, r1, tf)
        out(f"| {sig:.2f} | {mean:.2f} | {tf:.1f} | {pen:.3f} | {r64:.3f} eV | {r1:.3f} eV |")
    out("")
    out("Patch-size sensitivity at sigma 0.05 eV (fewer, larger patches -> heavier diode-to-diode tail):")
    out("")
    out("| Patch nm | Patches per ring | 1e-4 tail multiplier | Tail penalty eV |")
    out("|---|---|---|---|")
    for pn in (5.0, 10.0, 15.0, 20.0):
        npch = max(1, round(g["aj"] * 1e6 / (pn * pn)))
        tf2, _ = tail_factor(0.05, npch, tc, q_tail, 40000, rng)
        out(f"| {pn:.0f} | {npch} | {tf2:.1f} | {kT_eV(tc)*math.log(tf2):.3f} |")
    out("")
    out("Monte Carlo noise at the 1e-4 quantile is ~+/-30% in the multiplier (~+/-0.01 eV in penalty).")
    out("")
    out("Reading: with sigma = 0.05 eV the 1e-4 tier leaks ~"
        f"{req[0.05][2]:.0f}x the homogeneous value, so the mean effective barrier must sit ~"
        f"{kT_eV(tc)*math.log(req[0.05][2]):.2f} eV above the homogeneous requirement. With sigma = 0.10 eV the penalty "
        f"is ~{kT_eV(tc)*math.log(req[0.10][2]):.2f} eV and no demonstrated oxide-Schottky barrier is close.")
    out("")
    return req, n_patch


def section_requirements(g, req):
    out("## 5b. What a thick-film (literature-style) barrier must be for a tier to pass")
    tc = V("temp_c")
    s = V("sigma_patch_eV")
    r64, r1, _ = req[s]
    out(f"Low-field barrier = what a thick-film diode at ~0.2 MV/cm reports (the literature numbers). Required "
        f"tier effective barrier at sigma {s} eV: {r64:.3f} eV (G1, 64 ms) and {r1:.3f} eV (G2, 1 s).")
    out("")
    out("| Shell nm | Anode field MV/cm | Low-field barrier for G1 (eps 4) | G1 (eps 12) | G2 (eps 4) | G2 (eps 12) |")
    out("|---|---|---|---|---|---|")
    for sh in (8, 10, 15, 20, 25):
        if V("hole_d_nm") / 2 - sh < 4:
            continue
        e = field_at_anode(1.1 + V("v_data") + V("m_rev"), V("hole_d_nm") / 2, V("hole_d_nm") / 2 - sh)
        out(f"| {sh} | {e/1e8:.2f} | {lowfield_needed(r64, sh, tc, 4):.2f} eV | {lowfield_needed(r64, sh, tc, 12):.2f} eV | "
            f"{lowfield_needed(r1, sh, tc, 4):.2f} eV | {lowfield_needed(r1, sh, tc, 12):.2f} eV |")
    out("")
    out(f"Demonstrated barriers mapped into a {g['shell']:.0f} nm shell tier (85 C, 0.7 V hold, sigma {s} eV tail):")
    out("")
    out("| Contact (thick-film report) | Low-field eV | Tier phi_eff (eps 4) | Tail retention | Tier phi_eff (eps 12) | Tail retention |")
    out("|---|---|---|---|---|---|")
    for lab, phi in (("Passivated a-IGZO SBD (PKU)", V("phi_igzo_passivated_eV")),
                     ("Best Pt-IGZO, O2 in deposition (KIT secondary)", V("phi_best_igzo_eV")),
                     ("AgOx/ZnO, single crystal (AVS 2008)", V("phi_agox_zno_eV")),
                     ("Hypothetical 1.30 eV contact", 1.30)):
        cells = []
        for eps in (4, 12):
            pe = tier_eff_from_lowfield(phi, g["shell"], tc, eps_if=eps)
            i = thermionic_A(pe, g["aj"], tc) * req[s][2]
            t = g["cs"] * V("droop_mV") / 1e3 / i
            cells += [f"{pe:.2f} eV", fmt_t(t)]
        out(f"| {lab} | {phi:.2f} | " + " | ".join(cells) + " |")
    out("")
    out("Bottom line: no demonstrated oxide Schottky contact clears DRAM parity inside a thin coaxial shell. The bar "
        "for the coupon run is a low-field barrier of ~"
        f"{lowfield_needed(r64, g['shell'], tc, 12):.2f}-{lowfield_needed(r64, g['shell'], tc, 4):.2f} eV with patch "
        "sigma <= 0.05 eV, i.e. AgOx/ZnO-class barriers (1.0-1.2 eV) transferred to IGZO and then improved by ~0.1-0.2 "
        "eV, or a lower-electron-affinity shell (Ga-rich IGZO, Ga2O3) that raises every anode's barrier.")
    out("")


# --------------------------------------------------------------------------------------------
# 6. Sensitivity table on the key unknown
# --------------------------------------------------------------------------------------------
def section_sensitivity(g, req, n_patch):
    out("## 6. Sensitivity: 1e-4-tail retention at 85 C vs mean effective barrier and patch sigma")
    out("Effective barrier = barrier at the hold field (after image-force and TFE lowering). Cells marked "
        "`P` reach DRAM parity (>= 64 ms); `R` reach the concept's 1 s refresh-saving target.")
    out("")
    sigs = sorted(req.keys())
    out("| mean phi_eff eV | " + " | ".join(f"sigma {s:.2f}" for s in sigs) + " |")
    out("|---|" + "---|" * len(sigs))
    for phi in (0.80, 0.85, 0.90, 0.95, 1.00, 1.05, 1.10, 1.15):
        cells = []
        for s in sigs:
            i = thermionic_A(phi, g["aj"], V("temp_c")) * req[s][2]
            t = g["cs"] * V("droop_mV") / 1e3 / i
            tag = " R" if t >= 1 else (" P" if t >= 0.064 else "")
            cells.append(fmt_t(t) + tag)
        out(f"| {phi:.2f} | " + " | ".join(cells) + " |")
    out("")
    out("Section 5b maps the demonstrated (thick-film) barriers onto this table.")
    out("")


# --------------------------------------------------------------------------------------------
# 7. Write: forward voltage, plate swing, disturb rule
# --------------------------------------------------------------------------------------------
def section_write(g, req_g1):
    out("## 7. Write path: forward voltage, plate swing and the disturb rule")
    n = V("ideality")
    cs = g["cs"]
    t_w = V("t_write_ns") * 1e-9
    out("Clamp-write: the node discharges through its diode into the driven pillar; after t_w the current has decayed "
        "to I_end = Cs n kT/(q t_w) (logarithmic settling), so the clamp level is V_f(I_end). The concept's 14 nA is "
        "the average for a full 0.5 V swing in 10 ns.")
    out("")
    out("Forward bias flattens the shell, so the forward barrier is ~the low-field barrier, not the lowered reverse "
        "one: a contact good enough for retention is also one that needs a large forward voltage.")
    out("")
    out("| Low-field barrier eV | T C | V_f at I_end | I_end nA | V_f at 13.6 nA avg | Plate swing needed V |")
    out("|---|---|---|---|---|---|")
    swing_max = 0
    phi_need = lowfield_needed(req_g1, g["shell"], V("temp_c"))
    for phi in sorted({1.0, 1.1, 1.2, 1.3, round(phi_need, 2)}):
        for tc in (0, 25, 85):
            kt = kT_eV(tc)
            i_end = cs * n * kt / t_w
            i_s = thermionic_A(phi, g["aj"], tc)
            vf_end = n * kt * math.log(i_end / i_s)
            vf_avg = n * kt * math.log(13.6e-9 / i_s)
            swing = V("v_data") + vf_end + V("m_rev")
            if abs(phi - round(phi_need, 2)) < 1e-9:
                swing_max = max(swing_max, swing)
            out(f"| {phi:.2f} | {tc} | {vf_end:.2f} V | {i_end*1e9:.2f} | {vf_avg:.2f} V | {swing:.2f} |")
    out("")
    j = 13.6e-9 / (g["aj"] * 1e-8)
    out(f"Average forward current density during write: {j:.0f} A/cm2 on a {g['aj']*1e6:.0f} nm2 ring - well above "
        "the ~1-100 A/cm2 at which thick-film IGZO rectifiers are usually characterised, so forward-pulse endurance "
        "must be tested at this density, not inferred.")
    out("")
    out("Design rule (new in this model): plate swing >= Vdata + V_f + guard puts every stored level below the lowest "
        "pillar level, so no unselected node is ever forward-biased. Stored levels = V_pillar,write + V_f - plate swing. "
        "Without the rule (stored levels = pillar levels) the pillar-hammer disturb is:")
    out("")
    tc = V("temp_c")
    kt = kT_eV(tc)
    out("| Barrier eV | Forward bias on victim | Charge lost per 10 ns event | Events to 100 mV droop |")
    out("|---|---|---|---|")
    for phi in (0.9, 1.0, 1.1):
        i_s = thermionic_A(phi, g["aj"], tc)
        for vf in (V("v_data"), -V("m_rev")):  # phi here = effective barrier (forward-biased victim)
            i = i_s * (math.exp(vf / (n * kt)) - 1) if vf > 0 else 0.0
            dq = abs(i) * 10e-9
            ev = (cs * 0.1 / dq) if dq > 0 else float("inf")
            out(f"| {phi:.1f} | {vf:+.1f} V | {dq/Q:.2e} e- | {ev:.2e} |")
    out("")
    out("A pillar can be accessed ~2e7 times per second, so the naive biasing fails in well under one refresh "
        "interval; with the rule the victim stays reverse-biased (zero events). Cost: the plate swing rises to "
        f"~{swing_max:.1f} V at 0 C for the G1-passing contact ({phi_need:.2f} eV low-field), paid in plate CV^2 energy "
        "(section 8) and a ~2 V plate driver under the array. ZrO2 itself never "
        "sees more than ~Vdata + guard, because the floating node follows the plate.")
    out("")
    kt0 = kT_eV(0)
    vf_g3 = n * kt0 * math.log(cs * n * kt0 / t_w / thermionic_A(phi_need, g["aj"], 0))
    return swing_max, vf_g3


# --------------------------------------------------------------------------------------------
# 7b. Escape routes: bigger holes / thicker shells / wrapped capacitor
# --------------------------------------------------------------------------------------------
def section_escape(rng):
    out("## 7b. Escape routes: thicker shell in a bigger hole, or a wrapped capacitor")
    out("Each row sets the shell as stated (metal core radius = hole/2 - shell) and recomputes Cs, ring area, pitch, the sigma-0.05 "
        "tail (Monte Carlo, patch = shell) and the low-field barrier a contact needs for G1 (64 ms) at 85 C.")
    out("")
    out("| Hole nm | Shell nm | Wrapped Cs | Cs fF | Footprint um2 | Gb/mm2 @64 tiers | x 1-beta | Signal @64 tiers mV | Low-field barrier for G1 (eps 4 / 12) |")
    out("|---|---|---|---|---|---|---|---|---|")
    tc = V("temp_c")
    rows = []
    for hole, shell, wrap in ((60, 15, False), (60, 20, False), (60, 15, True), (80, 25, False), (80, 30, True),
                              (100, 35, False), (100, 40, True)):
        g = geometry(hole_d=hole, shell=shell, wrap=wrap)
        npch = max(1, round(g["aj"] * 1e6 / (shell * shell)))
        tf, _ = tail_factor(0.05, npch, tc, V("ber_target"), 20000, rng)
        ib = i_budget(g, 0.064)
        req = phi_for_current(ib, g["aj"], tc) + kT_eV(tc) * math.log(tf)
        lf4 = lowfield_needed(req, shell, tc, 4, rh_nm=hole / 2)
        lf12 = lowfield_needed(req, shell, tc, 12, rh_nm=hole / 2)
        d64 = density(g, 64)
        sig = signal_noise(g, 64)["dv_fresh"]
        rows.append((hole, shell, wrap, lf12, d64))
        out(f"| {hole} | {shell} | {'yes' if wrap else 'no'} | {g['cs']*1e15:.2f} | {g['a_fp']:.4f} | {d64:.2f} | "
            f"{d64/V('d_1b_gb_mm2'):.1f} | {sig*1e3:.0f} | {lf4:.2f} / {lf12:.2f} eV |")
    out("")
    base = rows[0]
    best = min(rows, key=lambda r: r[3])
    out(f"The geometry levers lower the G1 bar from {base[3]:.2f} eV (60 nm hole, {base[1]} nm shell) to {best[3]:.2f} eV "
        f"({best[0]} nm hole, {best[1]} nm shell, {'wrapped' if best[2] else 'back-wall'} Cs) at a density cost "
        f"({base[4]:.2f} -> {best[4]:.2f} Gb/mm2 at 64 tiers). That brings the bar into the range already shown for "
        "AgOx on ZnO (1.0-1.2 eV), but still above the best IGZO report (~0.92 eV). The wrapped capacitor "
        "(TiN/SiN/TiN tier) is the cheapest lever: ~2.7x Cs and ~2x signal at the same footprint.")
    out("")
    return rows


# --------------------------------------------------------------------------------------------
# 8. Energy
# --------------------------------------------------------------------------------------------
def section_energy(g, swing, n=32):
    out(f"## 8. Energy per access and refresh ({n} tiers)")
    e_dram = V("e_dram_bit_fJ")
    try:
        sys.path.insert(0, HERE)
        import dram_cell_physics as dcp  # noqa: E402
        e_dram = dcp.refresh_energy_per_bit_fJ()[0]
        src = "dram_cell_physics.refresh_energy_per_bit_fJ()"
    except Exception:  # pragma: no cover
        src = "INPUTS fallback"
    cs = g["cs"]
    cp = c_pillar(g, n)
    c_pp = 2 * EPS0 * 3.9 * max(0.0, g["a_sq"] * 1e-12 - math.pi * ((g["rb"] + V("zro2_nm")) * 1e-9) ** 2) / (V("ild_nm") * 1e-9)
    e_plate = (cs + c_pp) * swing ** 2
    e_pillar = (cs + cp) * V("v_data") ** 2
    e_rbl = V("c_rbl_fF") * 1e-15 * V("dv_rbl") * V("vdd")
    e_wbl = V("c_wbl_fF") * 1e-15 * V("v_data") * V("vdd")
    e_wl = V("c_wl_fF") * 1e-15 * V("v_wl") ** 2 / V("pump_eff")
    core = e_plate + e_pillar + e_rbl + e_wbl + e_wl
    tot = core * V("periph_overhead")
    out("| Component (per bit, read + clamp write-back) | fJ |")
    out("|---|---|")
    for name, e in (("Plate pulse (Cs + plate-plate) x swing^2", e_plate), ("Pillar precharge/write-back", e_pillar),
                    ("Read bitline (CDS)", e_rbl), ("Write bitline", e_wbl), ("Access WL (pumped)", e_wl)):
        out(f"| {name} | {e*1e15:.2f} |")
    out(f"| Core sum | {core*1e15:.1f} |")
    out(f"| x periphery overhead {V('periph_overhead')} | **{tot*1e15:.1f}** |")
    HEAD["e_bit"] = tot * 1e15
    HEAD["e_dram"] = e_dram
    out(f"| DDR5-class reference ({src}) | {e_dram:.1f} |")
    out("")
    bits_gb = 8e9 * V("ecc_rawber")
    out("| Refresh interval | DIODE-TOWER refresh mW/GB | DDR5-class mW/GB |")
    out("|---|---|---|")
    for t in (0.032, 0.064, 1.0):
        out(f"| {fmt_t(t)} | {bits_gb*tot/t*1e3:.2f} | {8e9*1.0625*e_dram*1e-15/t*1e3:.2f} |")
    out("")
    out("No energy step-change per access: bitline wiring dominates as in DRAM. The energy win exists only if "
        "the barrier reaches the 1 s target (16x fewer refreshes).")
    out("")
    return tot


# --------------------------------------------------------------------------------------------
# 9. Cost per bit
# --------------------------------------------------------------------------------------------
HEAD = {}


def section_cost(g):
    out("## 9. Cost per bit vs 1-beta DDR5 ($1.48/GB)")
    ref = V("wafer_1b_usd") / V("d_1b_gb_mm2")
    out(f"Relative $/bit = [(base wafer + $/tier x tiers) / (density x tier yield^tiers)] / ($3,800 / 0.447). "
        "Same wafer area and edge loss as 1-beta; tier yield after repair.")
    out("")
    out("| Tiers | Wafer $ | Gb/mm2 | Tier yield factor | $/bit vs 1-beta | $/GB | ($20/tier, $2.8k base) | ($45/tier, $3.4k base) |")
    out("|---|---|---|---|---|---|---|---|")
    res = {}
    for n in (16, 24, 32, 48, 64, 96, 128):
        d = density(g, n)
        y = V("tier_yield") ** n
        rows = []
        for base, ct in ((V("base_wafer_usd"), V("usd_per_tier")), (2800.0, 20.0), (3400.0, 45.0)):
            w = base + ct * n
            rows.append((w, w / (d * y) / ref))
        res[n] = rows[0][1]
        HEAD[f"cost{n}"] = rows[0][1]
        out(f"| {n} | {rows[0][0]:,.0f} | {d:.3f} | {y:.3f} | {rows[0][1]:.2f}x | ${rows[0][1]*V('cost_1b_usd_gb'):.2f} | "
            f"{rows[1][1]:.2f}x | {rows[2][1]:.2f}x |")
    out("")
    out("Tier yield and $/tier are the cost unknowns once the diode passes; the diode itself adds no per-tier "
        "lithography. A 64-tier tower reaches ~"
        f"{res[64]:.2f}x 1-beta $/bit in the base case.")
    out("")
    return res


# --------------------------------------------------------------------------------------------
# 10. Endurance budget
# --------------------------------------------------------------------------------------------
def section_endurance(g):
    out("## 10. Endurance budget per diode")
    q_pulse = g["cs"] * V("v_data")
    fl = q_pulse / (g["aj"] * 1e-8)
    yr10 = 10 * 365.25 * 86400
    out("Every access to a tier = 1 forward dump (read) + 1 forward clamp (write-back) = 2 forward pulses.")
    out("")
    out("| Use case (10 years) | Forward pulses | Charge fluence C/cm2 | vs 1e12-pulse test |")
    out("|---|---|---|---|")
    for lab, nacc in (("Refresh only, 64 ms", yr10 / 0.064), ("Refresh only, 1 s", yr10 / 1.0),
                      ("Hot row, 1% duty (C0)", V("hot_row_cycles_10y"))):
        p = 2 * nacc
        out(f"| {lab} | {p:.1e} | {p*fl:.1e} | {p/1e12:.2g}x |")
    out("")
    out(f"Per pulse: {q_pulse/Q:.0f} e- through {g['aj']*1e6:.0f} nm2 = {fl:.1e} C/cm2. Charge crosses a "
        "semiconductor barrier (thermionic), not an insulator, so the C0 insulator charge-fluence rule (1e2-1e5 "
        "cycles) does not apply; Si Schottky and p-n rectifiers carry >1e8 C/cm2 in service [ESTIMATE: "
        "100 A/cm2 for 10 years = 3e10 C/cm2]. Oxide-Schottky barrier "
        "drift under this fluence has not been measured. A 1e12-pulse test covers refresh-only life ~100x and a hot row "
        "to within ~2 decades (hammer remapping or extrapolation covers the rest).")
    out("")
    out("Drift budget: a barrier drop of d_phi multiplies leakage by exp(d_phi/kT): 30 meV -> "
        f"{math.exp(0.03/kT_eV(V('temp_c'))):.1f}x, 60 meV -> {math.exp(0.06/kT_eV(V('temp_c'))):.1f}x at 85 C.")
    out("")


# --------------------------------------------------------------------------------------------
# 11. GO / NO-GO
# --------------------------------------------------------------------------------------------
def section_go(g, req, n_par, n_3x, vf_g3):
    out("## 11. GO / NO-GO")
    tc = V("temp_c")
    s = V("sigma_patch_eV")
    r64, r1, tf = req[s]
    i64 = i_budget(g, 0.064)
    i1 = i_budget(g, 1.0)
    out(f"Default sigma {s} eV, shell {g['shell']:.0f} nm, Cs {g['cs']*1e15:.2f} fF, ring {g['aj']*1e6:.0f} nm2, 85 C.")
    out("")
    out("| Gate | Threshold (measured on thin-shell coupons at design thickness, 85 C, 0.7 V reverse hold) |")
    out("|---|---|")
    out(f"| G1 DRAM-parity retention (64 ms) | 99.99th-percentile ring-diode leakage <= {i64*1e18:.0f} aA; equivalently "
        f"mean tier effective barrier >= {r64:.2f} eV at sigma {s} (low-field barrier >= "
        f"{lowfield_needed(r64, g['shell'], tc, 12):.2f}-{lowfield_needed(r64, g['shell'], tc, 4):.2f} eV) |")
    out(f"| G2 refresh-saving retention (1 s) | 99.99th-percentile leakage <= {i1*1e18:.0f} aA; mean effective barrier >= "
        f"{r1:.2f} eV (low-field >= {lowfield_needed(r1, g['shell'], tc, 12):.2f}-{lowfield_needed(r1, g['shell'], tc, 4):.2f} eV) |")
    j = 13.6e-9 / (g["aj"] * 1e-8)
    out(f"| G3 write | >= 0.8 nA forward per ring-sized diode at <= {vf_g3 + 0.1:.1f} V and 0 C, ideality <= 1.3 "
        f"(plate swing <= ~{V('v_data') + vf_g3 + 0.1 + V('m_rev'):.1f} V) |")
    out(f"| G4 endurance | effective-barrier drop <= 30 meV (leakage <= 2.6x) after 1e12 forward pulses at ~{j:.0f} A/cm2, 85 C |")
    out(f"| G5 signal (stage b) | post-CDS residual <= 7 mV for >= 32 tiers (density {density(g, 32):.2f} Gb/mm2, "
        f"{density(g, 32)/V('d_1b_gb_mm2'):.1f}x 1-beta) |")
    out("")
    HEAD.update(i64=i64, i1=i1, r64=r64, r1=r1,
                lf64=(lowfield_needed(r64, g["shell"], tc, 12), lowfield_needed(r64, g["shell"], tc, 4)),
                lf1=(lowfield_needed(r1, g["shell"], tc, 12), lowfield_needed(r1, g["shell"], tc, 4)), j=j, vf_g3=vf_g3)
    out(f"**GO/NO-GO:** GO to the 4-tier stack if any one anode (RuOx, PtOx, PdO, MoOx, AgOx) on a >={g['shell']:.0f} nm IGZO shell after "
        f"<=400 C passes G1 + G3 + G4 (DRAM-class tower, 1.9-4x density at 32-64 tiers), with G2 as the stretch that "
        f"adds the refresh-energy win. NO-GO (park the linear-capacitor tower, keep the FE persistent variant) if the best "
        f"anode's 1e-4-tail leakage exceeds {i64*1e18:.0f} aA per ring at 85 C (mean effective barrier < "
        f"{r64:.2f} eV at sigma {s}), or if the barrier drifts > 60 meV within 1e10 pulses. Revival condition: a "
        "contact that clears the 80-nm-hole / wrapped-capacitor bar of section 7b (~0.96-0.97 eV low-field at "
        "sigma <= 0.05 eV, 3x 1-beta at 64 tiers), or a lower-electron-affinity shell (Ga-rich IGZO, Ga2O3) or "
        "p-oxide/n-oxide heterojunction that does.")
    out("")
    out(f"Density context: parity at {n_par} tiers and 3x at {n_3x} tiers in this geometry; the step change is "
        "a 32-64-tier claim, not a 16-tier one.")
    out("")


def section_inputs():
    out("## Inputs")
    out("| Name | Value | Unit | Source |")
    out("|---|---|---|---|")
    for k, (v, u, s) in INPUTS.items():
        vs = f"{v:.4g}" if isinstance(v, float) else str(v)
        out(f"| {k} | {vs} | {u} | {s} |")
    out("")


def headline(g, n_par, n_3x):
    h = []
    s32, s64 = signal_noise(g, 32), signal_noise(g, 64)
    h.append("## Headline")
    h.append("")
    h.append(f"- **Cell:** Cs {g['cs']*1e15:.2f} fF ({g['cs']*V('v_data')/Q:.0f} e- at 0.5 V), ring diode "
             f"{g['aj']*1e6:.0f} nm2, pillar {c_pillar(g, 32)*1e15:.2f} fF at 32 tiers; footprint {g['a_fp']:.4f} um2 "
             f"({g['pitch']:.0f} nm pitch, 60 nm hole).")
    h.append(f"- **Signal:** {s32['dv_fresh']*1e3:.0f} mV fresh / {s32['dv_end']*1e3:.0f} mV end-of-retention at 32 "
             f"tiers (z = {s32['z']:.1f} at 7 mV CDS residual); {s64['dv_fresh']*1e3:.0f} mV at 64 tiers (z = {s64['z']:.1f}).")
    h.append(f"- **Density:** parity with 1-beta at {n_par} tiers; {density(g, 32):.2f} Gb/mm2 "
             f"({density(g, 32)/V('d_1b_gb_mm2'):.1f}x) at 32 tiers; {density(g, 64):.2f} Gb/mm2 "
             f"({density(g, 64)/V('d_1b_gb_mm2'):.1f}x) at 64; 3x at {n_3x} tiers.")
    h.append(f"- **Cost:** {HEAD['cost32']:.2f}x 1-beta $/bit (${HEAD['cost32']*V('cost_1b_usd_gb'):.2f}/GB) at 32 tiers, "
             f"{HEAD['cost64']:.2f}x (${HEAD['cost64']*V('cost_1b_usd_gb'):.2f}/GB) at 64, if tier yield >= 0.998.")
    h.append(f"- **Energy:** {HEAD['e_bit']:.0f} fJ/bit per access vs ~{HEAD['e_dram']:.0f} fJ DDR5-class; refresh win only "
             "if 1 s retention is reached.")
    h.append(f"- **Key unknown, quantified:** the 1e-4-tail tier must leak <= {HEAD['i64']*1e18:.0f} aA (64 ms, DRAM "
             f"parity) or <= {HEAD['i1']*1e18:.0f} aA (1 s) at 85 C. With patch sigma 0.05 eV that needs a mean tier "
             f"effective barrier >= {HEAD['r64']:.2f} / {HEAD['r1']:.2f} eV, i.e. a thick-film (low-field) barrier "
             f">= {HEAD['lf64'][0]:.2f}-{HEAD['lf64'][1]:.2f} eV (64 ms) or {HEAD['lf1'][0]:.2f}-{HEAD['lf1'][1]:.2f} eV "
             "(1 s) in a 15 nm coaxial IGZO shell. Best demonstrated on IGZO: ~0.92 eV (thick film).")
    tc = V("temp_c")
    l15 = lowering(1.2, V("v_data") + V("m_rev"), g["shell"], tc, eps_if=12)
    l15b = lowering(1.2, V("v_data") + V("m_rev"), g["shell"], tc, eps_if=4)
    h.append("- **New physics flags vs the concept:** (1) a thin depleted shell lowers the reverse barrier by "
             f"~{l15[1]+l15[2]:.2f}-{l15b[1]+l15b[2]:.2f} eV at {g['shell']:.0f} nm (image force + thermionic-field "
             f"emission; ~0.35-0.45 eV at 10 nm), so the concept's 1.05-1.1 eV zero-bias bar for 1 s becomes "
             f"{HEAD['lf1'][0]:.2f}-{HEAD['lf1'][1]:.2f} eV; (2) barrier inhomogeneity adds ~0.14 eV for the 1e-4 tail; (3) the concept's "
             "sigma margin was double-counted (signal/sigma vs signal/2sigma); (4) a plate-swing rule "
             "(swing >= Vdata + Vf + guard) is needed or unselected tiers are hammered within ~1e4 accesses.")
    h.append("")
    return h


def main():
    out("# DIODE-TOWER model output")
    out("")
    out("*Generated by `models/diode-tower.py` (pure stdlib, python3). Agent dos-diode-tower, 2026-11-02. "
        "All numbers are first-principles estimates unless an input cites a source.*")
    out("")
    insert_at = len(LINES)
    g = section_geometry()
    section_signal(g)
    n_par, n_3x = section_density(g)
    section_diode(g)
    req, n_patch = section_inhomogeneity(g)
    section_requirements(g, req)
    section_sensitivity(g, req, n_patch)
    swing, vf_g3 = section_write(g, req[V("sigma_patch_eV")][0])
    section_escape(random.Random(7))
    section_energy(g, swing)
    section_cost(g)
    section_endurance(g)
    section_go(g, req, n_par, n_3x, vf_g3)
    section_inputs()
    h = headline(g, n_par, n_3x)
    LINES[insert_at:insert_at] = h
    print("\n".join(h))
    try:
        os.makedirs(os.path.dirname(OUT_MD), exist_ok=True)
        with open(OUT_MD, "w") as f:
            f.write("\n".join(LINES) + "\n")
        print(f"\n[written to {OUT_MD}]")
    except OSError as exc:  # pragma: no cover
        print(f"[could not write {OUT_MD}: {exc}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
