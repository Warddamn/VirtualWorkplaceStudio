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

Red-team revision 2026-11-02 (owner response to research/redteam/rt_*.json, 16 objections; sources
research/sources/resp-diode-tower.jsonl): see the RED-TEAM REVISIONS block below the INPUTS and section 12.
The base cell is now the wrapped-capacitor tier on Mo replacement plates, read by a stacked 2T top
(access + gain FET, read-select removed, one merged bitline), with an RTN-inclusive readout budget.
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
    "rows_per_plate": (8, "rows", "RED-TEAM (RT-CIRC-03): was 4. 8 rows halves slit overhead and plate-driver count; replacement slits every ~1 um"),
    # ---- red-team: wrapped tier on Mo replacement plates (RT-CIRC-01, RT-CIRC-03, RT-CIRC-04, RT-PROC-04)
    "cell_wrap": (True, "-", "RED-TEAM (RT-CIRC-01): was back-wall only. Node sits in a poly recess between two Mo plate layers (plate wraps top, bottom, back)"),
    "wrap_plate_nm": (10.0, "nm", "ESTIMATE: each of the two Mo plate layers per wrapped tier (replacement metal, NAND-style)"),
    "wrap_node_layer_nm": (25.0, "nm", "ESTIMATE: sacrificial/back-wall n+ poly layer that is recessed to hold the node (node height = 25 - 2 x ZrO2)"),
    "ild_wrap_nm": (20.0, "nm", "ESTIMATE: inter-tier SiO2 between plate k top layer and plate k+1 bottom layer"),
    "wrap_pullback_nm": (5.0, "nm", "ESTIMATE: Mo plate edge pulled back from the hole face and back-filled with SiO2 (limits plate-to-pillar coupling)"),
    "rho_plate_uohm_cm": (25.0, "uOhm.cm", "ESTIMATE: 10 nm ALD/CVD Mo (thin-film size effect; bulk 5.3); TiN 25 nm ~100-150 for comparison"),
    "seg_len_um": (300.0, "um", "RED-TEAM (RT-CIRC-03): plate segment length, driven from its centre (RC of a 150 um end-driven line)"),
    "stair_step_um": (0.35, "um/tier", "ESTIMATE: staircase step per tier at each segment (3D-NAND-like); binary-chop multi-depth contacts would cut it ~5x"),
    "eps_igzo": (12.0, "-", "ESTIMATE: a-IGZO static permittivity ~10-16 (training knowledge)"),
    "m_eff_igzo": (0.34, "m0", "ESTIMATE: a-IGZO electron effective mass ~0.3-0.35 m0 (training knowledge)"),
    "c_gain_fF": (0.25, "fF", "ESTIMATE: vertical IGZO gain-FET gate, 60 nm dia x 50 nm, 6 nm HfO2"),
    "c_access_fF": (0.10, "fF", "ESTIMATE: access-transistor source junction/overlap"),
    "c_top_fF": (0.10, "fF", "ESTIMATE: pillar top wiring"),
    "c_fringe_tier_fF": (0.005, "fF", "ESTIMATE: pillar core to plate fringe through ILD per tier"),
    # ---- electrical
    "v_data": (0.5, "V", "FINAL_CONCEPTS step_change: 0.5 V data swing"),
    "m_rev": (0.3, "V", "RED-TEAM (RT-CIRC-04): was 0.2. Guard covers 100 mV droop of '1' nodes plus plate-to-neighbour coupling"),
    "t_write_ns": (10.0, "ns", "FINAL_CONCEPTS: <=10-20 ns write"),
    "ideality": (1.3, "-", "PtOx/ZnO n=1.31 (https://livrepository.liverpool.ac.uk/3015044/); IGZO SBD n=1.35 (PKU poster, sources log)"),
    # ---- red-team readout budget (replaces sigma_cds_mV = 7 mV rms) (RT-CIRC-01, RT-CIRC-02)
    "sigma_rand_mV": (2.5, "mV rms", "models/pixel-stack.py: random post-CDS readout sigma 2.49 mV for a 0.01 um2 oxide SF (thermal + 1/f after CDS)"),
    "rtn_tail_mV": (20.0, "mV", "RT-CIRC-pixel-stack-02: 1e-4 RTN tail 9-18 x q/(Cox W L) = 13-25 mV for a ~0.01 um2 oxide FET; midpoint"),
    "coupling_mV": (1.2, "mV", "models/pixel-stack.py: neighbour coupling after decision feedback"),
    "gain_L_nm": (50.0, "nm", "ESTIMATE: in-hole gain-FET channel length (sets c_gain_fF and the RTN tail; lever in section 12)"),
    "temp_slew_K_s": (10.0, "K/s", "ESTIMATE [UNVERIFIED]: LPDDR MR4-polling examples assume ~10 C/s die temperature gradient"),
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
    "base_wafer_usd": (3450.0, "$", "RED-TEAM (RT-PROC-03, RT-PROC-04): was 3000 (A1 base 3D). +~7 masks for the stacked 2T top and bitline, slit/replacement steps, ~$450"),
    "usd_per_tier": (38.0, "$/tier", "RED-TEAM (RT-PROC-04, RT-IND-03): was 25. 4 films/tier (SiO2, SiN, poly, SiN) + share of Mo replacement and poly recess"),
    "tier_yield": (0.995, "-", "RED-TEAM (RT-IND-03): was 0.998 (A1 requirement, undemonstrated). 0.998 and 0.99 shown as sensitivity"),
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

# --------------------------------------------------------------------------------------------
# RED-TEAM REVISIONS (2026-11-02, owner response to research/redteam/rt_{DEV,PROC,CIRC,IND}.json)
#   input: old -> new  [objection id]  why
# --------------------------------------------------------------------------------------------
RT_REVISIONS = [
    ("sigma_cds_mV", "7 mV rms -> removed; sigma_rand_mV 2.5 rms + rtn_tail_mV 20 + coupling_mV 1.2 (deterministic) + dVf(slew)",
     "RT-CIRC-01, RT-CIRC-02", "RTN tail is a deterministic add (PIXEL-STACK model + RT-CIRC-pixel-stack-02); same units as PIXEL-STACK's residual"),
    ("cell_wrap", "False (back-wall Cs 0.27 fF) -> True (wrapped Cs ~0.59 fF, Mo plates, 5 nm pull-back, 65 nm tier)",
     "RT-CIRC-01, RT-CIRC-03, RT-CIRC-04", "restores 64-tier signal under the RTN budget; Mo plates cut plate RC ~10x; own plate shields neighbours"),
    ("rows_per_plate", "4 -> 8", "RT-CIRC-03", "halves slit overhead and plate drivers per mm2"),
    ("seg_len_um / stair_step_um", "unpriced -> 300 um centre-driven segment, 0.35 um/tier staircase priced in density",
     "RT-CIRC-03", "plate RC <= 10 ns and staircase area now in the footprint"),
    ("m_rev", "0.2 V -> 0.3 V", "RT-CIRC-04", "guard covers droop + plate-to-neighbour coupling"),
    ("base_wafer_usd", "$3,000 -> $3,450", "RT-PROC-03, RT-PROC-04", "stacked 2T top + single merged bitline masks, replacement-metal steps"),
    ("usd_per_tier", "$25 -> $38", "RT-PROC-04, RT-IND-03", "wrapped tri-layer tier + replacement + poly recess"),
    ("tier_yield", "0.998 -> 0.995", "RT-IND-03", "0.998 is a requirement, not a demonstration; 0.998/0.99 kept as sensitivity"),
    ("contact list", "AgOx 1.10 eV counted as the reachable class -> AgOx/PtOx/Pt/Ag/Pd = planar diagnostics only",
     "RT-DEV-01, RT-PROC-01", "Ag2O decomposes 300-400 C; no volatile etch products; fab contaminants"),
    ("leakage model", "thermionic only -> + Poole-Frenkel/TAT sensitivity (extra lowering = image-force term)",
     "RT-DEV-02", "gate decisions move to measured ring leakage, not thick-film barrier"),
]


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
def geometry(hole_d=None, shell=None, plate=None, wrap=None):
    """Cell geometry. wrap=None takes INPUTS cell_wrap (red-team base = wrapped tier on Mo plates)."""
    wrap = V("cell_wrap") if wrap is None else wrap
    hole_d = hole_d or V("hole_d_nm")
    shell = shell or V("igzo_shell_nm")
    plate = plate or V("plate_nm")
    rh = hole_d / 2
    rc = rh - shell
    rb = rh + V("node_radial_nm")
    t = V("zro2_nm")
    eps_d = EPS0 * V("k_zro2")
    if wrap:
        # tier = SiO2 ILD / Mo / n+ poly (recessed for the node; back-wall electrode) / Mo
        hn = V("wrap_node_layer_nm") - 2 * t
        tier_pitch = V("ild_wrap_nm") + 2 * V("wrap_plate_nm") + V("wrap_node_layer_nm")
    else:
        hn = plate - 2 * t                 # node height (ZrO2 lines top and bottom of the recess)
        tier_pitch = plate + V("ild_nm")
    # storage cap: back wall coax (node outer radius rb -> plate/poly at rb + t)
    cs = 2 * math.pi * eps_d * hn * 1e-9 / math.log((rb + t) / rb)
    if wrap:
        # two annuli under/over the Mo layers, which stop wrap_pullback_nm short of the hole face
        r_in = rh + V("wrap_pullback_nm")
        cs += 2 * eps_d * math.pi * ((rb * 1e-9) ** 2 - (r_in * 1e-9) ** 2) / (t * 1e-9)
        # plate-edge-to-pillar coupling: SiO2 pull-back coax in series with the depleted shell coax, two Mo layers
        hp = V("wrap_plate_nm") * 1e-9
        c_sh = 2 * math.pi * EPS0 * V("eps_igzo") * hp / math.log(rh / rc)
        if V("wrap_pullback_nm") > 0:
            c_ox = 2 * math.pi * EPS0 * 3.9 * hp / math.log(r_in / rh)
            c_e1 = 1 / (1 / c_ox + 1 / c_sh)
        else:
            c_e1 = c_sh
        c_edge = 2 * c_e1
    else:
        c_edge = V("c_fringe_tier_fF") * 1e-15
    aj_um2 = 2 * math.pi * rh * hn * 1e-6   # ring diode on the hole face
    cj = 2 * math.pi * EPS0 * V("eps_igzo") * hn * 1e-9 / math.log(rh / rc)
    c_unsel = 1 / (1 / cj + 1 / cs) + c_edge
    pitch = hole_d + 2 * (V("node_radial_nm") + t) + V("plate_web_nm")
    a_sq = (pitch * 1e-3) ** 2
    slit = 1 + V("slit_nm") / (V("rows_per_plate") * pitch)
    # plate-to-adjacent-plate capacitance per pillar cell (both neighbours), through the inter-tier ILD
    r_open = (rh + V("wrap_pullback_nm")) if wrap else (rb + t)
    ild = V("ild_wrap_nm") if wrap else V("ild_nm")
    c_pp = 2 * EPS0 * 3.9 * max(0.0, a_sq * 1e-12 - math.pi * (r_open * 1e-9) ** 2) / (ild * 1e-9)
    return dict(rh=rh, rc=rc, rb=rb, hn=hn, cs=cs, aj=aj_um2, cj=cj, c_unsel=c_unsel, c_edge=c_edge, pitch=pitch,
                c_pp=c_pp, r_open=r_open,
                a_fp=a_sq * slit, a_sq=a_sq, slit=slit, shell=shell, hole_d=hole_d, plate=plate, wrap=wrap,
                tier_pitch=tier_pitch)


def stair_factor(n):
    """Staircase area per plate segment (one staircase per centre-driven segment), as a footprint multiplier."""
    return 1 + n * V("stair_step_um") / V("seg_len_um")


def c_gain_at(L_nm=None):
    L_nm = V("gain_L_nm") if L_nm is None else L_nm
    return V("c_gain_fF") * L_nm / 50.0


def c_pillar(g, n, c_gain_fF=None):
    cg = c_gain_at() if c_gain_fF is None else c_gain_fF
    return ((n - 1) * g["c_unsel"] + (cg + V("c_access_fF") + V("c_top_fF")) * 1e-15)


def section_geometry():
    out("## 1. Geometry -> capacitances and footprint")
    g = geometry()
    gb = geometry(wrap=False)
    out(f"Base cell ({'wrapped tier on Mo plates, red-team revision' if g['wrap'] else 'back-wall ring'}): hole "
        f"{g['hole_d']:.0f} nm, IGZO shell {g['shell']:.0f} nm (metal core radius {g['rc']:.0f} nm), node ring "
        f"{V('node_radial_nm'):.0f} nm radial x {g['hn']:.1f} nm tall, ZrO2 {V('zro2_nm')} nm k={V('k_zro2'):.0f}, "
        f"tier pitch {g['tier_pitch']:.0f} nm (back-wall tier {gb['tier_pitch']:.0f} nm).")
    out("")
    out("| Quantity | Value | Note |")
    out("|---|---|---|")
    out(f"| Storage cap Cs, back-wall ring (pre-red-team base) | {gb['cs']*1e15:.3f} fF | concept assumed 0.27 fF |")
    out(f"| Storage cap Cs, wrapped (Mo top+bottom, n+ poly back wall, {V('wrap_pullback_nm'):.0f} nm pull-back) | "
        f"{geometry(wrap=True)['cs']*1e15:.3f} fF | red-team base; 4 films per tier |")
    out(f"| Plate-edge-to-pillar coupling per tier | {g['c_edge']*1e15:.4f} fF | back-wall fringe {gb['c_edge']*1e15:.4f} fF |")
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
_TEMPCO = {}


def vf_tempco_V_per_K(phi_lf=1.10):
    """|dV_f/dT| of the clamp-write forward voltage at I_end (section 7 physics), 0 -> 85 C."""
    if phi_lf in _TEMPCO:
        return _TEMPCO[phi_lf]
    n = V("ideality")
    t_w = V("t_write_ns") * 1e-9
    cs = geometry()["cs"]
    vf = []
    for tc in (0.0, 85.0):
        kt = kT_eV(tc)
        vf.append(n * kt * math.log(cs * n * kt / t_w / thermionic_A(phi_lf, geometry()["aj"], tc)))
    _TEMPCO[phi_lf] = (vf[0] - vf[1]) / 85.0
    return _TEMPCO[phi_lf]


def dvf_signal_V(g, n, t_ref=0.064, slew=None):
    """CIRC-02: every refresh re-writes the level at the current temperature, so write/read temperatures differ
    by at most slew x t_ref; the offset reaches the pillar as Cs x dVf / (Cs + Cp)."""
    slew = V("temp_slew_K_s") if slew is None else slew
    dvf = slew * t_ref * vf_tempco_V_per_K()
    return dvf * g["cs"] / (g["cs"] + c_pillar(g, n))


def signal_noise(g, n, rtn_mV=None, droop_mV=None, tc=None, sigma_rand_mV=None, c_gain_fF=None, t_ref=0.064):
    """Red-team readout budget: margin = signal_end/2 - (RTN tail + coupling + dVf) must exceed z_req x sigma_random,
    sigma_random = sqrt(SF random^2 + kT/C + diode soft-reset). allowed_res = the PIXEL-STACK-style residual
    (3.72 sigma_SF + RTN + coupling) this tier count can tolerate."""
    rtn_mV = V("rtn_tail_mV") if rtn_mV is None else rtn_mV
    sigma_rand_mV = V("sigma_rand_mV") if sigma_rand_mV is None else sigma_rand_mV
    droop_mV = V("droop_mV") if droop_mV is None else droop_mV
    tc = V("temp_c") if tc is None else tc
    cs, cp = g["cs"], c_pillar(g, n, c_gain_fF)
    ctot = cs + cp
    dv_fresh = cs * V("v_data") / ctot
    dv_end = cs * (V("v_data") - droop_mV / 1e3) / ctot
    kt = KB * (tc + 273.15)
    s_ktc = math.sqrt(kt / ctot)
    s_diode = math.sqrt(2 * kt / (2 * cs)) * cs / ctot      # soft-reset noise of node, write + read
    sigma = math.sqrt((sigma_rand_mV / 1e3) ** 2 + s_ktc ** 2 + s_diode ** 2)
    dvf = dvf_signal_V(g, n, t_ref)
    det = rtn_mV / 1e3 + V("coupling_mV") / 1e3 + dvf
    margin = dv_end / 2 - det
    z = margin / sigma
    zreq = qinv(V("ber_target"))
    allowed_res = dv_end / 2 - zreq * math.sqrt(s_ktc ** 2 + s_diode ** 2) - dvf
    return dict(cp=cp, dv_fresh=dv_fresh, dv_end=dv_end, s_ktc=s_ktc, s_diode=s_diode, sigma=sigma, z=z,
                det=det, dvf=dvf, margin=margin, allowed_res=allowed_res, ber=qfunc(z) if margin > 0 else 0.5)


def max_tiers(g, **kw):
    zreq = qinv(V("ber_target"))
    nmax = 0
    for n in range(2, 513):
        if signal_noise(g, n, **kw)["z"] >= zreq:
            nmax = n
    return nmax


def section_signal(g):
    out("## 2. Signal, noise and raw BER vs tier count")
    out(f"Signal = Cs x Vdata / (Cs + Cpillar). RED-TEAM budget (RT-CIRC-01/02): margin = end-of-retention signal/2 - "
        f"(1e-4 RTN tail {V('rtn_tail_mV'):.0f} mV + coupling {V('coupling_mV')} mV + write/read dVf); "
        f"z = margin / sigma_random, sigma_random = sqrt(SF {V('sigma_rand_mV')} mV^2 + kT/C + diode soft-reset). "
        f"Raw-BER target {V('ber_target'):.0e} needs z >= {qinv(V('ber_target')):.2f}. 'Allowed residual' is the "
        "PIXEL-STACK-style residual (3.72 sigma_SF + RTN + coupling) the tier count tolerates.")
    out("")
    for lab, gg in (("wrapped (base)", g if g["wrap"] else geometry(wrap=True)), ("back-wall (pre-red-team)", geometry(wrap=False))):
        out(f"**{lab}, Cs {gg['cs']*1e15:.2f} fF**")
        out("")
        out("| Tiers | Cpillar fF | Fresh signal mV | After 100 mV droop mV | kT/C mV | sigma_random mV | deterministic mV | z | raw BER | allowed residual mV |")
        out("|---|---|---|---|---|---|---|---|---|---|")
        for n in (8, 16, 24, 32, 48, 64, 96, 128):
            r = signal_noise(gg, n)
            out(f"| {n} | {r['cp']*1e15:.2f} | {r['dv_fresh']*1e3:.1f} | {r['dv_end']*1e3:.1f} | {r['s_ktc']*1e3:.2f} | "
                f"{r['sigma']*1e3:.2f} | {r['det']*1e3:.1f} | {r['z']:.2f} | {r['ber']:.1e} | {r['allowed_res']*1e3:.1f} |")
        out("")
    out("Correction to the concept's arithmetic: the concept compared signal/sigma (7-15) with BCH t=8's 3.72 sigma, "
        "but 3.72 is the half-margin (signal/2) requirement. Signal/(2 sigma) is the right comparison, which halves "
        "the quoted margin. The pre-red-team model used a 7 mV rms 'CDS residual', equivalent to a PIXEL-STACK-style "
        "residual of ~3.72 x 7 = 26 mV; the RTN-corrected oxide-SF residual is 24-35 mV.")
    out("")
    out("1e-4 RTN tail tolerance (max tiers with z >= 3.72 at end of retention):")
    out("")
    out("| RTN tail mV | max tiers (back-wall Cs) | max tiers (wrapped Cs) |")
    out("|---|---|---|")
    gw = geometry(wrap=True)
    gb = geometry(wrap=False)
    for s in (5, 13, 20, 25, 35, 45):
        out(f"| {s} | {max_tiers(gb, rtn_mV=s)} | {max_tiers(gw, rtn_mV=s)} |")
    out("")


# --------------------------------------------------------------------------------------------
# 3. Density
# --------------------------------------------------------------------------------------------
def bits_per_pillar(n):
    spares = math.ceil(n / 32) * V("spare_per_32")
    return n - V("ref_tiers") - spares


def density(g, n):
    """User Gb/mm2; footprint includes the slit (rows_per_plate) and, after the red team, the per-segment staircase."""
    return 1e6 / (g["a_fp"] * stair_factor(n)) * bits_per_pillar(n) * V("array_eff") / V("ecc_rawber") / 1e9


def section_density(g):
    out("## 3. Density vs tier count")
    out(f"User Gb/mm2 = (1e6 / (footprint um2 x staircase factor)) x (tiers - reference - spares) x array efficiency "
        f"{V('array_eff')} / ECC {V('ecc_rawber'):.3f}. Staircase factor = 1 + tiers x {V('stair_step_um')} um / "
        f"{V('seg_len_um'):.0f} um segment (RT-CIRC-03). Baseline 1-beta DDR5 = {V('d_1b_gb_mm2')} Gb/mm2.")
    out("")
    out("| Tiers | bits/pillar | Stack height um | Hole AR | Gb/mm2 (60 nm hole) | x 1-beta | Gb/mm2 (concept 0.011 um2) | x 1-beta |")
    out("|---|---|---|---|---|---|---|---|")
    tier_pitch = g["tier_pitch"]
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
    out(f"Demonstrated barriers mapped into a {g['shell']:.0f} nm shell tier (85 C, {V('v_data')+V('m_rev'):.1f} V hold, sigma {s} eV tail):")
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
        "sigma <= 0.05 eV on the as-integrated (bottom-anode, etch-back) interface, from a process-integrable anode "
        "(RuO2, MoOx, WOx; AgOx is excluded after the red team), or a lower-electron-affinity shell (Ga-rich IGZO, "
        "Ga2O3) that raises every anode's barrier. If the leakage is Poole-Frenkel/TAT-limited the bar is higher (section 12g).")
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
    out(f"| Low-field barrier eV | T C | V_f at I_end | I_end nA | V_f at {cs*V('v_data')/t_w*1e9:.1f} nA avg | Plate swing needed V |")
    out("|---|---|---|---|---|---|")
    swing_max = 0
    phi_need = lowfield_needed(req_g1, g["shell"], V("temp_c"))
    for phi in sorted({1.0, 1.1, 1.2, 1.3, round(phi_need, 2)}):
        for tc in (0, 25, 85):
            kt = kT_eV(tc)
            i_end = cs * n * kt / t_w
            i_s = thermionic_A(phi, g["aj"], tc)
            vf_end = n * kt * math.log(i_end / i_s)
            vf_avg = n * kt * math.log(cs * V("v_data") / t_w / i_s)
            swing = V("v_data") + vf_end + V("m_rev")
            if abs(phi - round(phi_need, 2)) < 1e-9:
                swing_max = max(swing_max, swing)
            out(f"| {phi:.2f} | {tc} | {vf_end:.2f} V | {i_end*1e9:.2f} | {vf_avg:.2f} V | {swing:.2f} |")
    out("")
    j = cs * V("v_data") / t_w / (g["aj"] * 1e-8)
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
        "AgOx on ZnO (1.0-1.2 eV; not process-integrable, RT-DEV-01/RT-PROC-01), but still above the best IGZO report "
        "(~0.92 eV). The wrapped capacitor (Mo/poly/Mo tier, now the base cell) gives ~2.2x Cs and ~1.6x signal at the "
        "same footprint; its retention-bar gain alone is small (~0.02 eV) because the leakage budget scales only as Cs.")
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
    c_pp = g["c_pp"]
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


def rel_cost(g, n, base=None, per_tier=None, ty=None):
    base = V("base_wafer_usd") if base is None else base
    per_tier = V("usd_per_tier") if per_tier is None else per_tier
    ty = V("tier_yield") if ty is None else ty
    ref = V("wafer_1b_usd") / V("d_1b_gb_mm2")
    return (base + per_tier * n) / (density(g, n) * ty ** n) / ref


def section_cost(g):
    out("## 9. Cost per bit vs 1-beta DDR5 ($1.48/GB)")
    out(f"Relative $/bit = [(base wafer ${V('base_wafer_usd'):,.0f} + ${V('usd_per_tier'):.0f}/tier x tiers) / "
        f"(density x tier yield^tiers)] / ($3,800 / 0.447). Same wafer area and edge loss as 1-beta; tier yield after "
        "repair. Red-team inputs (RT-PROC-03/04, RT-IND-03); the pre-red-team case ($3,000 + $25/tier, back-wall cell, "
        "yield 0.998, no staircase) is the last column.")
    out("")
    out(f"| Tiers | Wafer $ | Gb/mm2 | $/bit, yield {V('tier_yield')} | $/GB | yield 0.998 | yield 0.99 | pre-red-team |")
    out("|---|---|---|---|---|---|---|---|")
    res = {}
    gb = geometry(wrap=False)
    for n in (16, 24, 32, 48, 64, 96, 128):
        w = V("base_wafer_usd") + V("usd_per_tier") * n
        c0 = rel_cost(g, n)
        c998 = rel_cost(g, n, ty=0.998)
        c99 = rel_cost(g, n, ty=0.99)
        # pre-red-team: back-wall, 4 rows/slit, no staircase
        slit4 = 1 + V("slit_nm") / (4 * gb["pitch"])
        d_old = 1e6 / (gb["a_sq"] * slit4) * bits_per_pillar(n) * V("array_eff") / V("ecc_rawber") / 1e9
        c_old = (3000.0 + 25.0 * n) / (d_old * 0.998 ** n) / (V("wafer_1b_usd") / V("d_1b_gb_mm2"))
        res[n] = c0
        HEAD[f"cost{n}"] = c0
        HEAD[f"cost{n}_998"] = c998
        HEAD[f"cost{n}_99"] = c99
        out(f"| {n} | {w:,.0f} | {density(g, n):.3f} | {c0:.2f}x | ${c0*V('cost_1b_usd_gb'):.2f} | {c998:.2f}x | "
            f"{c99:.2f}x | {c_old:.2f}x |")
    out("")
    out("Tier yield and $/tier are the cost unknowns once the diode passes; the diode itself adds no per-tier "
        "lithography. A 64-tier tower reaches ~"
        f"{res[64]:.2f}x 1-beta $/bit in the red-team base case (was 0.35x).")
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
    out(f"| Gate | Threshold (measured on thin-shell coupons at design thickness, 85 C, {V('v_data')+V('m_rev'):.1f} V reverse hold) |")
    out("|---|---|")
    out(f"| G1 DRAM-parity retention (64 ms) | 99.99th-percentile ring-diode leakage <= {i64*1e18:.0f} aA; equivalently "
        f"mean tier effective barrier >= {r64:.2f} eV at sigma {s} (low-field barrier >= "
        f"{lowfield_needed(r64, g['shell'], tc, 12):.2f}-{lowfield_needed(r64, g['shell'], tc, 4):.2f} eV) |")
    out(f"| G2 refresh-saving retention (1 s) | 99.99th-percentile leakage <= {i1*1e18:.0f} aA; mean effective barrier >= "
        f"{r1:.2f} eV (low-field >= {lowfield_needed(r1, g['shell'], tc, 12):.2f}-{lowfield_needed(r1, g['shell'], tc, 4):.2f} eV) |")
    j = g["cs"] * V("v_data") / (V("t_write_ns") * 1e-9) / (g["aj"] * 1e-8)
    i_end0 = g["cs"] * V("ideality") * kT_eV(0) / (V("t_write_ns") * 1e-9)
    HEAD["i_end0"] = i_end0
    out(f"| G3 write | >= {i_end0*1e9:.1f} nA forward per ring-sized diode at <= {vf_g3 + 0.1:.1f} V and 0 C, ideality <= 1.3 "
        f"(plate swing <= ~{V('v_data') + vf_g3 + 0.1 + V('m_rev'):.1f} V) |")
    out(f"| G4 endurance | effective-barrier drop <= 30 meV (leakage <= 2.6x) after 1e12 forward pulses at ~{j:.0f} A/cm2, 85 C |")
    sn32, sn64 = signal_noise(g, 32), signal_noise(g, 64)
    HEAD["res32"], HEAD["res64"] = sn32["allowed_res"], sn64["allowed_res"]
    out(f"| G5 readout (RT-CIRC-01) | post-CDS readout residual (3.72 sigma random + 1e-4 RTN tail + coupling, 85 C, ~15 ns "
        f"CDS gap, >= 65k in-hole-sized gain FETs) <= {sn64['allowed_res']*1e3:.0f} mV for 64 tiers "
        f"({density(g, 64):.2f} Gb/mm2, {density(g, 64)/V('d_1b_gb_mm2'):.1f}x) or <= {sn32['allowed_res']*1e3:.0f} mV "
        f"for 32 tiers ({density(g, 32):.2f} Gb/mm2, {density(g, 32)/V('d_1b_gb_mm2'):.1f}x) |")
    out("")
    HEAD.update(i64=i64, i1=i1, r64=r64, r1=r1,
                lf64=(lowfield_needed(r64, g["shell"], tc, 12), lowfield_needed(r64, g["shell"], tc, 4)),
                lf1=(lowfield_needed(r1, g["shell"], tc, 12), lowfield_needed(r1, g["shell"], tc, 4)), j=j, vf_g3=vf_g3)
    out(f"**GO/NO-GO (revised after red team):** GO to the 4-tier stack if any one process-integrable anode (RuO2 from a "
        f"Ru node ring, MoOx, WOx; AgOx/PtOx/Pt/Pd are planar diagnostics only) on a >={g['shell']:.0f} nm IGZO, Ga-rich or "
        f"Ga2O3 shell, formed bottom-anode with the real etch-back chemistry and after <=400 C, passes G1 + G3 + G4 measured "
        f"as ring leakage on thin-shell vertical structures (not thick-film barrier), with G2 as the stretch that "
        f"adds the refresh-energy win. NO-GO (park the linear-capacitor tower; the FE variant is not a fallback) if the best "
        f"anode's 1e-4-tail leakage exceeds {i64*1e18:.0f} aA per ring at 85 C (mean effective barrier < "
        f"{r64:.2f} eV at sigma {s}), or if the barrier drifts > 60 meV within 1e10 pulses. Revival condition: a "
        "contact that clears the 80-nm-hole / wrapped-capacitor bar of section 7b (~0.97-0.98 eV low-field at "
        "sigma <= 0.05 eV, ~2.9x 1-beta at 64 tiers), or a lower-electron-affinity shell (Ga-rich IGZO, Ga2O3) or "
        "p-oxide/n-oxide heterojunction that does.")
    out("")
    out(f"Density context: parity at {n_par} tiers and 3x at {n_3x} tiers in this geometry; the step change is "
        "a 32-64-tier claim, not a 16-tier one.")
    out("")


# --------------------------------------------------------------------------------------------
# 12. Red-team variants (owner response, 2026-11-02)
# --------------------------------------------------------------------------------------------
def tier_eff_pf(phi_lf, shell_nm, tc, eps_if, rh_nm=None):
    """Poole-Frenkel/TAT-limited activation energy: PF lowering sqrt(qE/(pi eps)) = 2x the image-force term."""
    v_rev = V("v_data") + V("m_rev")
    l_lf = lowering_at_field(V("e_lowfield_V_per_nm") * 1e9, tc, eps_if)
    phi0 = phi_lf + l_lf
    _, d_if, d_tfe = lowering(phi0, v_rev, shell_nm, tc, eps_if=eps_if, rh_nm=rh_nm)
    return phi0 - 2 * d_if - d_tfe


def lowfield_needed_pf(req, shell_nm, tc, eps_if):
    lo, hi = 0.3, 3.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if tier_eff_pf(mid, shell_nm, tc, eps_if) < req:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def section_redteam(g, req, n_patch):
    out("## 12. Red-team variants (owner response, 2026-11-02)")
    out("")
    out("### 12a. RED-TEAM REVISIONS (inputs changed)")
    out("")
    out("| Input | old -> new | Objection | Why |")
    out("|---|---|---|---|")
    for k, chg, oid, why in RT_REVISIONS:
        out(f"| {k} | {chg} | {oid} | {why} |")
    out("")
    tc = V("temp_c")
    gb = geometry(wrap=False)

    # ---- 12b plate RC, drivers, staircase (RT-CIRC-03)
    out("### 12b. Plate RC, drivers and staircase (RT-CIRC-03)")
    out("")
    out("Distributed-RC (Elmore 0.5 r c L^2) of one plate segment. Mesh sheet resistance = R_sq x (1+f)/(1-f) for "
        "insulating circular openings of area fraction f (Maxwell-Garnett). Load per node during the dump = "
        "Cs x Cp/(Cs+Cp) + plate-to-plate. 'Centre-driven' halves the effective length.")
    out("")
    out("| Plate | R_sq ohm/sq | Opening radius nm | Mesh R ohm/sq | Load per node fF | Rows | Segment um | Drive | RC ns | Drivers per mm2 (32 tiers) | um2 per driver | Staircase overhead 32 / 64 tiers |")
    out("|---|---|---|---|---|---|---|---|---|---|---|---|")
    cases = (("TiN 25 nm back-wall (pre-red-team)", gb, 150.0, 25.0, 1, 4, 50.0, "end"),
             ("TiN 25 nm back-wall (pre-red-team)", gb, 150.0, 25.0, 1, 4, 200.0, "end"),
             ("Mo 25 nm back-wall", gb, V("rho_plate_uohm_cm"), 25.0, 1, 8, 300.0, "centre"),
             ("Mo 2 x 10 nm wrapped (base)", geometry(wrap=True), V("rho_plate_uohm_cm"), V("wrap_plate_nm"), 2,
              V("rows_per_plate"), V("seg_len_um"), "centre"))
    for lab, gg, rho, t_nm, nlay, rows, L, drive in cases:
        rsq = rho * 1e-8 / (t_nm * 1e-9) / nlay
        f = math.pi * gg["r_open"] ** 2 / gg["pitch"] ** 2
        rmesh = rsq * (1 + f) / (1 - f)
        cp32 = c_pillar(gg, 32)
        c_node = gg["cs"] * cp32 / (gg["cs"] + cp32) + gg["c_pp"]
        w_um = rows * gg["pitch"] / 1e3
        r_um = rmesh / w_um
        c_um = rows * (1e3 / gg["pitch"]) * c_node
        l_eff = L / 2 if drive == "centre" else L
        tau = 0.5 * r_um * c_um * l_eff ** 2
        seg_area = L * (w_um + V("slit_nm") / 1e3)
        drv = 32 / seg_area * 1e6
        st32 = 32 * V("stair_step_um") / L
        st64 = 64 * V("stair_step_um") / L
        out(f"| {lab} | {rsq:.1f} | {gg['r_open']:.1f} | {rmesh:.0f} | {c_node*1e15:.3f} | {rows} | {L:.0f} | {drive} | "
            f"{tau*1e9:.1f} | {drv/1e6:.2f}M | {1e6/drv:.2f} | {st32:.0%} / {st64:.0%} |")
    out("")
    out("Reading: the critic's TiN numbers reproduce (50 um segments for <=10 ns need ~1.2M drivers/mm2 at 0.85 um2 "
        "each). Mo replacement plates (10x lower R_sq) plus the wrapped tier (Mo layers are perforated only by the "
        "60 nm hole) allow 300 um centre-driven segments at <=10 ns: ~0.1M drivers/mm2, ~10 um2 each, room for a ~2 V "
        "thick-oxide driver or a NAND-style pass gate fed by global plate drivers. The staircase is now priced in "
        "density (one per segment).")
    out("")

    # ---- 12c gain-FET L lever (RT-CIRC-01)
    out("### 12c. Readout budget and the gain-FET length lever (RT-CIRC-01)")
    out("")
    out("RTN tail scales ~1/(W L) and SF random noise ~1/sqrt(W L); the gate capacitance scales ~L. Wrapped base cell:")
    out("")
    out("| Gain-FET L nm | c_gain fF | RTN tail mV | sigma_SF mV | max tiers (z >= 3.72) | allowed residual @64 mV | x 1-beta @ max tiers |")
    out("|---|---|---|---|---|---|---|")
    for L in (50.0, 100.0, 150.0):
        cg = c_gain_at(L)
        rt = V("rtn_tail_mV") * 50.0 / L
        sr = V("sigma_rand_mV") * math.sqrt(50.0 / L)
        nm = max_tiers(g, rtn_mV=rt, sigma_rand_mV=sr, c_gain_fF=cg)
        r64 = signal_noise(g, 64, rtn_mV=rt, sigma_rand_mV=sr, c_gain_fF=cg)
        out(f"| {L:.0f} | {cg:.2f} | {rt:.1f} | {sr:.2f} | {nm} | {r64['allowed_res']*1e3:.1f} | "
            f"{density(g, min(nm, 512))/V('d_1b_gb_mm2'):.1f} |")
    out("")
    out("Reading: in PIXEL-STACK units the back-wall cell tolerated ~26 mV of residual at 32 tiers but fails at 64 "
        "tiers once a 13-25 mV RTN tail is added; the wrapped cell holds 64 tiers with a 20-25 mV tail, and a "
        "longer in-hole gain FET pushes the ceiling further. RTN-outlier pillars can also be screened and spared at "
        "test (1% spare pillars caps an exponential RTN tail at ~4.6x instead of ~9.2x its mean).")
    out("")

    # ---- 12d cross-temperature V_f (RT-CIRC-02)
    out("### 12d. Write/read temperature mismatch (RT-CIRC-02)")
    out("")
    tco = vf_tempco_V_per_K()
    out(f"Clamp-write V_f temperature coefficient (1.10 eV contact, I_end): {tco*1e3:.2f} mV/K. Every refresh is a "
        "dump read plus a clamp write-back, so a stored level is re-written at the current temperature at least once "
        "per refresh interval; write-to-read temperature difference <= slew x interval.")
    out("")
    out("| Case | dT K | dV_f mV | Pillar offset 32 tiers mV | Pillar offset 64 tiers mV | Share of half-margin @64 |")
    out("|---|---|---|---|---|---|")
    for lab, dT in (("Critic: write 85 C, read 25 C (never refreshed)", 60.0),
                    ("64 ms refresh, 10 K/s slew", 10.0 * 0.064), ("64 ms refresh, 100 K/s slew", 100.0 * 0.064),
                    ("1 s refresh (G2 mode), 10 K/s slew", 10.0)):
        dvf = dT * tco
        o32 = dvf * g["cs"] / (g["cs"] + c_pillar(g, 32))
        o64 = dvf * g["cs"] / (g["cs"] + c_pillar(g, 64))
        hm = signal_noise(g, 64)["dv_end"] / 2
        out(f"| {lab} | {dT:.2f} | {dvf*1e3:.1f} | {o32*1e3:.2f} | {o64*1e3:.2f} | {o64/hm:.1%} |")
    out("")

    # ---- 12e neighbour coupling (RT-CIRC-04)
    out("### 12e. Plate-to-adjacent-node coupling (RT-CIRC-04)")
    out("")
    t = V("zro2_nm")
    a_ann = math.pi * ((gb["rb"] * 1e-9) ** 2 - (gb["rh"] * 1e-9) ** 2)
    c_nn = EPS0 * a_ann / ((V("ild_nm") / 3.9 + 2 * t / V("k_zro2")) * 1e-9)
    follow = gb["cs"] / (gb["cs"] + gb["cj"])
    c_node_tot = gb["cs"] + gb["cj"]
    swing = V("v_data") + 1.10 + V("m_rev")
    out("| Cell | Coupling to plate k+1 / node k+1 fF | Node total fF | Coupled step on node k mV (swing "
        f"{swing:.1f} V) | Guard {V('m_rev'):.1f} V left after 100 mV droop mV |")
    out("|---|---|---|---|---|")
    for lab, cc in (("back-wall, node-node only (parallel plate)", c_nn * follow),
                    ("back-wall, + plate fringe 0.003-0.01 fF", c_nn * follow + 0.01e-15)):
        dv = swing * cc / (c_node_tot + cc)
        out(f"| {lab} | {cc*1e15:.4f} | {c_node_tot*1e15:.3f} | {dv*1e3:.0f} | {(V('m_rev') - 0.1 - dv)*1e3:.0f} |")
    gw = geometry(wrap=True)
    cc_w = 0.0005e-15
    dvw = swing * cc_w / (gw["cs"] + gw["cj"])
    out(f"| wrapped: own Mo layers shield node k+1 [ESTIMATE <= 0.0005 fF] | {cc_w*1e15:.4f} | {(gw['cs']+gw['cj'])*1e15:.3f} | "
        f"{dvw*1e3:.0f} | {(V('m_rev') - 0.1 - dvw)*1e3:.0f} |")
    out("")

    # ---- 12f contacts and integrability (RT-DEV-01, RT-PROC-01, RT-DEV-03)
    out("### 12f. Contacts, integrability and tail retention in the base cell (RT-DEV-01/02/03, RT-PROC-01)")
    out("")
    sbase = V("sigma_patch_eV")
    rng = random.Random(1212)
    out(f"Tier phi_eff from the thick-film barrier (eps 4 / 12), tail at the stated sigma, 85 C, hold {V('v_data')+V('m_rev'):.1f} V. "
        "'PF' = Poole-Frenkel/TAT-limited case (activation = barrier - 2 x image force - TFE).")
    out("")
    out("| Contact | Low-field eV | sigma eV | Process-integrable? | Tail retention, thermionic (eps 4 / 12) | Tail retention, PF (eps 4 / 12) |")
    out("|---|---|---|---|---|---|")
    contacts = (("Pt-IGZO, O2 in deposition (KIT secondary)", V("phi_best_igzo_eV"), sbase, "no: Pt not dry-etchable, fab contaminant"),
                ("AgOx/ZnO single crystal (AVS 2008)", V("phi_agox_zno_eV"), sbase, "no: Ag2O decomposes 300-400 C; Ag diffuses"),
                ("Pd on a-HIZO (JBNU), mean, Werner-Guttler", 1.40, 0.14, "no (Pd), but shows high means on amorphous oxides"),
                ("RuO2 / IrO2 on GaN (POSTECH), analogue only", 1.45, sbase, "Ru yes (RuO4 etch); IGZO value unknown"),
                ("Hypothetical integrable RuO2/IGZO, bottom anode", 1.20, sbase, "target of the coupon matrix"))
    tf_cache = {}
    for lab, phi, sg, integ in contacts:
        if sg not in tf_cache:
            tf_cache[sg] = tail_factor(sg, n_patch, tc, V("ber_target"), 40000, rng)[0]
        tf = tf_cache[sg]
        cells = []
        for fn in (tier_eff_from_lowfield, tier_eff_pf):
            ts = []
            for eps in (4, 12):
                pe = fn(phi, g["shell"], tc, eps_if=eps) if fn is tier_eff_from_lowfield else fn(phi, g["shell"], tc, eps)
                i = thermionic_A(pe, g["aj"], tc) * tf
                ts.append(fmt_t(g["cs"] * V("droop_mV") / 1e3 / i))
            cells.append(" / ".join(ts))
        out(f"| {lab} | {phi:.2f} | {sg:.2f} | {integ} | {cells[0]} | {cells[1]} |")
    out("")

    # ---- 12g bar under thermionic vs PF, and the bottom-anode penalty (RT-DEV-02, RT-DEV-03)
    out("### 12g. G1 bar: thermionic vs Poole-Frenkel, and the bottom-anode penalty (RT-DEV-02, RT-DEV-03)")
    out("")
    r64 = req[sbase][0]
    lf_th = (lowfield_needed(r64, g["shell"], tc, 12), lowfield_needed(r64, g["shell"], tc, 4))
    lf_pf = (lowfield_needed_pf(r64, g["shell"], tc, 12), lowfield_needed_pf(r64, g["shell"], tc, 4))
    HEAD["lf64_pf"] = lf_pf
    out("| Leakage mechanism | Thick-film barrier needed for G1, eps 12 - eps 4 | Top-contact-equivalent if the bottom anode loses 0.1-0.3 eV |")
    out("|---|---|---|")
    out(f"| Thermionic + image force + TFE (model) | {lf_th[0]:.2f}-{lf_th[1]:.2f} eV | {lf_th[0]+0.1:.2f}-{lf_th[1]+0.3:.2f} eV |")
    out(f"| Poole-Frenkel / trap-assisted (2x image-force lowering) | {lf_pf[0]:.2f}-{lf_pf[1]:.2f} eV | {lf_pf[0]+0.1:.2f}-{lf_pf[1]+0.3:.2f} eV |")
    out("")
    out("No process-integrable anode has an IGZO datum. Against the best IGZO datum of any kind (Pt, 0.92 eV, not "
        f"integrable) the gap is {lf_th[0]-0.92:.2f}-{lf_pf[1]-0.92:.2f} eV before any bottom-anode loss "
        f"({lf_th[0]-0.92+0.1:.2f}-{lf_pf[1]-0.92+0.3:.2f} eV with it). Every 0.031 eV is a factor e in leakage at 85 C.")
    out("")

    # ---- 12h flipped core-anode variant (RT-DEV-03 mitigation evaluated)
    out("### 12h. Flipped polarity (anode = pillar core, deposited last onto IGZO) - evaluated and rejected")
    out("")
    out("A core anode is a top contact (as in the literature) and needs no anode etch-back, but it sits at the inner "
        "radius of the coaxial shell, where the charge-free field is highest.")
    out("")
    out("| Hole / shell nm | Outer-anode field MV/cm | Lowering eps 4 / 12 eV | Inner-anode field MV/cm | Lowering eps 4 / 12 eV | Penalty eV |")
    out("|---|---|---|---|---|---|")
    vr = V("v_data") + V("m_rev")
    for hole, shell in ((60, 15), (80, 15), (100, 20)):
        rh, rc = hole / 2, hole / 2 - shell
        eo = (1.2 - 0.1 + vr) / (rh * 1e-9 * math.log(rh / rc))
        ei = (1.2 - 0.1 + vr) / (rc * 1e-9 * math.log(rh / rc))
        lo4, lo12 = lowering_at_field(eo, tc, 4), lowering_at_field(eo, tc, 12)
        li4, li12 = lowering_at_field(ei, tc, 4), lowering_at_field(ei, tc, 12)
        out(f"| {hole} / {shell} | {eo/1e8:.2f} | {lo4:.2f} / {lo12:.2f} | {ei/1e8:.2f} | {li4:.2f} / {li12:.2f} | "
            f"{li12-lo12:.2f}-{li4-lo4:.2f} |")
    out("")
    out("Reading: the flip costs ~0.2-0.3 eV of extra lowering, as much as or more than the 0.1-0.3 eV bottom-anode "
        "loss it avoids. It stays a planar diagnostic (top-anode controls), not the design.")
    out("")

    # ---- 12i tail squaring (I-12627) vs profiled tier repair
    out("### 12i. Squaring the leakage tail: series diodes (I-12627) vs profiled tier repair")
    out("")
    t4 = tail_factor(sbase, n_patch, tc, 1e-4, 40000, rng)[0]
    t2 = tail_factor(sbase, n_patch, tc, 2e-2, 40000, rng)[0]
    t1 = tail_factor(sbase, n_patch, tc, 1e-2, 40000, rng)[0]
    kt = kT_eV(tc)
    pitch2 = g["pitch"] + 2 * (10 + 3)
    out("| Option | Effective quantile | Tail multiplier | Barrier credit eV | Cost |")
    out("|---|---|---|---|---|")
    out(f"| Base (one diode, no profiling) | 1e-4 | {t4:.0f} | 0 | - |")
    out(f"| Two series diodes per tier (I-12627 logic; min of two independent leakages) | 1e-2 | {t1:.0f} | "
        f"{kt*math.log(t4/t1):.3f} | second shell + anode liner: pitch {g['pitch']:.0f} -> {pitch2:.0f} nm "
        f"(footprint x{(pitch2/g['pitch'])**2:.2f}); V_f doubles (+~1.1 V plate swing); defects in one hole are likely correlated |")
    out(f"| Profiled tier repair: map out the worst 2% of tiers at test (2 spares per 32) | 2e-2 | {t2:.0f} | "
        f"{kt*math.log(t4/t2):.3f} | -3% bits per pillar; needs leakage stable in time (no VRT) - a 1,000 h re-test |")
    out("")

    # ---- 12j I-12302 plate-strip sensing comparison
    out("### 12j. Plate-strip sensing (I-12302) vs the tower's pillar")
    out("")
    s32 = signal_noise(g, 32)
    out(f"I-12302 clamps the bitline and senses a ~3.7 fF plate strip (~135 mV vs ~14 mV on a long bitline). The tower "
        f"already senses a short local node: the pillar is {c_pillar(g, 32)*1e15:.2f} fF at 32 tiers and gives "
        f"{s32['dv_fresh']*1e3:.0f} mV. Its plates are page-wide (thousands of nodes), so plate sensing would raise, not "
        "cut, the sense capacitance. I-12302 is already embodied; it does not fix the gain-FET noise.")
    out("")

    # ---- 12k Stoney bow (RT-PROC-04)
    out("### 12k. Stack stress (RT-PROC-04)")
    out("")
    out("Stoney: bow = 3 sigma t_f r^2 / (E' t_s^2), 300 mm wafer (r 150 mm), 775 um Si, E' 180.5 GPa.")
    out("")
    out("| Stack | Metal um | 1.0 GPa | 0.5 GPa | 0.3 GPa | 0.15 GPa |")
    out("|---|---|---|---|---|---|")
    for lab, tm in (("64 x 25 nm TiN (pre-red-team)", 64 * 25e-9), ("32 x 2 x 10 nm Mo", 32 * 20e-9),
                    ("64 x 2 x 10 nm Mo", 64 * 20e-9)):
        cells = []
        for sgm in (1.0e9, 0.5e9, 0.3e9, 0.15e9):
            bow = 3 * sgm * tm * 0.15 ** 2 / (180.5e9 * (775e-6) ** 2)
            cells.append(f"{bow*1e6:.0f} um")
        out(f"| {lab} | {tm*1e6:.2f} | " + " | ".join(cells) + " |")
    out("")
    out(f"Hole aspect ratio with the {g['tier_pitch']:.0f} nm wrapped tier: {32*g['tier_pitch']/g['hole_d']:.0f} at 32 tiers, "
        f"{64*g['tier_pitch']/g['hole_d']:.0f} at 64 (two 32-tier decks, NAND-style). The <=150 um bow target needs "
        "<=~0.15-0.2 GPa net film stress or a backside compensation film.")
    out("")

    # ---- 12l cost vs incumbent curve (RT-IND-03)
    out("### 12l. Cost vs the incumbent curve (RT-IND-03)")
    out("")
    out("| Tiers | x 1-beta density | $/bit vs 1-beta today (yield 0.99 / 0.995 / 0.998) | vs 2032 incumbent at -8%/yr (0.61x) | at -12%/yr (0.46x) |")
    out("|---|---|---|---|---|")
    for n in (32, 64, 96, 128):
        c = [rel_cost(g, n, ty=y) for y in (0.99, 0.995, 0.998)]
        out(f"| {n} | {density(g, n)/V('d_1b_gb_mm2'):.1f} | {c[0]:.2f} / {c[1]:.2f} / {c[2]:.2f} | "
            f"{c[1]/0.92**6:.2f} | {c[1]/0.88**6:.2f} |")
    out("")
    out(f"Per-tier cost ${V('usd_per_tier'):.0f} vs AND-STACK $30 and PIXEL-STACK $25 + $250 per 16-tier deck "
        "(their models): the tower's tier is not <= 50% of theirs. Its distinct portfolio value is the two-terminal "
        "per-tier device (no per-tier transistor), not the cost per tier.")
    out("")

    # ---- 12m top-of-pillar devices (RT-PROC-03)
    out("### 12m. Top of pillar (RT-PROC-03)")
    out("")
    out(f"Read-select device removed (gain-FET source = read word line, as in 2T0C); write and read bitlines merged; "
        f"access and gain FETs stacked in-line as vertical channel-all-around IGZO devices in the pillar's own "
        f"footprint (IMECAS vertical CAA 2T0C beyond 4F2, IEDM 2021). Bitline pitch = pillar pitch = {g['pitch']:.0f} nm "
        f"(single ArFi exposure, >= ~80 nm). Transistors per user bit: 2/{bits_per_pillar(32)} = "
        f"{2/bits_per_pillar(32):.3f} at 32 tiers, 2/{bits_per_pillar(64)} = {2/bits_per_pillar(64):.3f} at 64. "
        f"Added masks priced as +$450 in base_wafer_usd.")
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
    h.append("- **Revision:** red-team base (2026-11-02): wrapped-capacitor tier on Mo replacement plates, stacked 2T "
             "top (access + gain FET, one merged bitline), RTN-inclusive readout budget, tier yield 0.995, "
             "$3,450 base wafer + $38/tier, staircase priced. Section 12 has the objection-by-objection numbers.")
    h.append(f"- **Cell:** Cs {g['cs']*1e15:.2f} fF ({g['cs']*V('v_data')/Q:.0f} e- at 0.5 V), ring diode "
             f"{g['aj']*1e6:.0f} nm2, pillar {c_pillar(g, 32)*1e15:.2f} fF at 32 tiers; footprint {g['a_fp']:.4f} um2 "
             f"before staircase ({g['pitch']:.0f} nm pitch, 60 nm hole, {g['tier_pitch']:.0f} nm tier).")
    h.append(f"- **Signal:** {s32['dv_fresh']*1e3:.0f} mV fresh / {s32['dv_end']*1e3:.0f} mV end-of-retention at 32 "
             f"tiers (z = {s32['z']:.1f} with a {V('rtn_tail_mV'):.0f} mV RTN tail); {s64['dv_fresh']*1e3:.0f} mV at 64 "
             f"tiers (z = {s64['z']:.1f}). Allowed PIXEL-STACK-style readout residual {s32['allowed_res']*1e3:.0f} / "
             f"{s64['allowed_res']*1e3:.0f} mV at 32 / 64 tiers.")
    h.append(f"- **Density:** parity with 1-beta at {n_par} tiers; {density(g, 32):.2f} Gb/mm2 "
             f"({density(g, 32)/V('d_1b_gb_mm2'):.1f}x) at 32 tiers; {density(g, 64):.2f} Gb/mm2 "
             f"({density(g, 64)/V('d_1b_gb_mm2'):.1f}x) at 64; 3x at {n_3x} tiers.")
    h.append(f"- **Cost:** {HEAD['cost32']:.2f}x 1-beta $/bit (${HEAD['cost32']*V('cost_1b_usd_gb'):.2f}/GB) at 32 tiers, "
             f"{HEAD['cost64']:.2f}x (${HEAD['cost64']*V('cost_1b_usd_gb'):.2f}/GB) at 64, at tier yield {V('tier_yield')} "
             f"({HEAD['cost64_998']:.2f}x at 0.998, {HEAD['cost64_99']:.2f}x at 0.99).")
    h.append(f"- **Energy:** {HEAD['e_bit']:.0f} fJ/bit per access vs ~{HEAD['e_dram']:.0f} fJ DDR5-class; refresh win only "
             "if 1 s retention is reached.")
    h.append(f"- **Key unknown, quantified:** the 1e-4-tail tier must leak <= {HEAD['i64']*1e18:.0f} aA (64 ms, DRAM "
             f"parity) or <= {HEAD['i1']*1e18:.0f} aA (1 s) at 85 C. With patch sigma 0.05 eV that needs a mean tier "
             f"effective barrier >= {HEAD['r64']:.2f} / {HEAD['r1']:.2f} eV, i.e. a thick-film (low-field) barrier "
             f">= {HEAD['lf64'][0]:.2f}-{HEAD['lf64'][1]:.2f} eV (64 ms) or {HEAD['lf1'][0]:.2f}-{HEAD['lf1'][1]:.2f} eV "
             "(1 s) in a 15 nm coaxial IGZO shell if leakage is thermionic; "
             f"{HEAD['lf64_pf'][0]:.2f}-{HEAD['lf64_pf'][1]:.2f} eV (64 ms) if Poole-Frenkel/TAT-limited (RT-DEV-02). "
             "Best demonstrated on IGZO: ~0.92 eV (thick film, Pt, not process-integrable); no integrable anode "
             "(RuO2, MoOx, WOx) has an IGZO datum; the AgOx class (1.0-1.2 eV on ZnO) does not survive the flow (RT-DEV-01, RT-PROC-01).")
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
    section_redteam(g, req, n_patch)
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
