#!/usr/bin/env python3
"""
lean-array-module.py -- first-principles model for the LEAN ARRAY MODULE dossier (stage 3, rank 8).

Owner: dos-lean-array-module (dram-moonshot). Written 2026-11-02. Pure standard library.
Run from /home/user/VirtualWorkplaceStudio/dram-moonshot with:  python3 models/lean-array-module.py
Writes: research/stage3/lean-array-module_model_output.md (and prints the same text).

Concept: keep a memory-array line running without its single-source inputs:
  (1) helium backside wafer cooling  -> low-pressure H2 backside gas   [CORE, decisive experiment]
  (2) AR-60 fluorocarbon capacitor etch -> AAO / carbon mold / stub cells [secondary]
  (3) EUV for periodic layers -> interference litho / NIL + coarse DUV cuts [deferred]

What it computes:
  A. Wafer-to-chuck gas-gap conductance h(p, gap, gas, accommodation) with the temperature-jump
     (Smoluchowski) model, checked against the free-molecular (Corruccini) limit. Wafer temperature
     rise under 2-5 kW bias. Gap (bow) sensitivity, which is why He is used instead of N2/Ar.
  B. The key unknown: H2 thermal accommodation alpha. Break-even alpha for (i) drop-in at the He
     pressure, (ii) parity at <=1.5x He pressure, (iii) parity at the clamp-limited pressure.
  C. Arcing (Paschen minimum) for He, H2, N2, Ar.
  D. H2 leak into the etch plasma (H/F atom ratio) and exhaust H2 vs the 4 % LFL.
  E. Helium volume per wafer for backside cooling, its share of DRAM-fleet helium, $ per GB, and
     the outage-insurance value -- the honest scale of the helium lever.
  F. AAO capacitor for Si-access cells: Cs vs pitch/height, sense signal, retention, anodization energy.
  G. EUV-free periodic patterning: overlay budget vs residual distortion; density of F=40 nm cells.
  H. Sensitivity table on alpha_H2 and the GO/NO-GO line.
"""

import math
import os

KB = 1.380649e-23      # J/K
R_GAS = 8.314462       # J/mol/K
EPS0 = 8.854e-12       # F/m
FARADAY = 96485.0      # C/mol
TORR = 133.322         # Pa
V_STP_L = 22.414       # L/mol at 0 C, 1 atm
T_GAS = 300.0          # K, backside gas temperature

# --------------------------------------------------------------------------------------------
# INPUTS  -- every value carries a source URL or "ESTIMATE: basis"
# --------------------------------------------------------------------------------------------
INPUTS = {
    # ---- gas properties at ~300 K (textbook) ----
    # (M g/mol, gamma, k W/m/K, mu Pa s, cp J/kg/K)
    "gas_He": ((4.0026, 1.667, 0.155, 1.99e-5, 5193.0),
               "ESTIMATE: CRC-handbook 300 K values from prior knowledge, not web-verified this session"),
    "gas_H2": ((2.016, 1.405, 0.181, 8.96e-6, 14310.0),
               "ESTIMATE: CRC-handbook 300 K values (k_H2 0.18 vs k_He 0.15 also quoted in Stage-2 I-10762)"),
    "gas_N2": ((28.013, 1.400, 0.0259, 1.79e-5, 1040.0),
               "ESTIMATE: CRC-handbook 300 K values"),
    "gas_Ar": ((39.948, 1.667, 0.0177, 2.27e-5, 520.0),
               "ESTIMATE: CRC-handbook 300 K values"),
    # ---- thermal accommodation coefficients ----
    "alpha_He": (0.45, "https://www.sandia.gov/research/publications/details/an-experimental-assembly-for-precise-measurement-of-thermal-accommodation-c-2010-11-01/ (Trott et al.: ~0.45 He, untreated surfaces incl. Si; via search snippet)"),
    "alpha_N2": (0.85, "https://sandia.gov/research/publications/details/determination-of-thermal-accommodation-coefficients-from-heat-transfer-meas-2010-10-01 (~0.85 N2; via search snippet)"),
    "alpha_Ar": (0.95, "https://sandia.gov/research/publications/details/determination-of-thermal-accommodation-coefficients-from-heat-transfer-meas-2010-10-01 (~0.95 Ar; via search snippet)"),
    "alpha_H2_central": (0.20, "ESTIMATE: KEY UNKNOWN. Baule mass-ratio scaling of measured He 0.45 gives ~0.26 (computed in section B), "
                               "minus poorer rotational accommodation; engineering surfaces 0.2-0.5 per "
                               "https://deepblue.lib.umich.edu/bitstream/handle/2027.42/70040/JCPSA6-58-10-4080-1.pdf;sequence=2 (via snippet)"),
    "surface_mass_amu": (20.0, "ESTIMATE: mean atomic mass of SiO2/SiN/Al2O3 surfaces (O 16, N 14, Al 27, Si 28)"),
    # ---- ESC geometry and operating point ----
    "gap_um": (10.0, "ESTIMATE: wafer-to-ESC gap set by mesa/emboss height and roughness, 5-20 um class"),
    "h_contact": (50.0, "ESTIMATE: solid conduction through mesa contacts (few % area), W/m2/K; same for every gas"),
    "p_He_Torr": (15.0, "ESTIMATE: typical He backside pressure for high-power dielectric etch, 10-20 Torr"),
    "p_max_Torr": (40.0, "ESTIMATE: clamp-limited backside pressure; J-R/Coulombic ESC clamp pressure ~50-100 Torr-equivalent, keep gas <= ~half"),
    "p_go_factor": (1.5, "ESTIMATE: GO allows H2 at <=1.5x the He pressure (keeps clamp margin and leak <=~2x)"),
    "bias_W": (3000.0, "Concept card key_unknown: 2-5 kW bias (FINAL_CONCEPTS.json lean-array-module)"),
    "heat_fraction": (0.80, "ESTIMATE: fraction of bias + ion power deposited in the wafer as heat"),
    "wafer_area_m2": (math.pi * 0.15 ** 2, "300 mm wafer geometry"),
    "dT_window_K": (2.0, "ESTIMATE: HAR fluorocarbon etch tolerance on wafer temperature (polymer deposition / selectivity)"),
    # ---- Paschen constants A (1/cm/Torr), B (V/cm/Torr) ----
    "paschen": ({"He": (3.0, 34.0), "H2": (5.0, 130.0), "N2": (12.0, 342.0), "Ar": (12.0, 180.0)},
                "ESTIMATE: textbook Townsend constants (Lieberman & Lichtenberg / Raizer), prior knowledge, not web-verified"),
    "gamma_se": (0.01, "ESTIMATE: secondary-electron yield, same for all gases so ratios are meaningful"),
    # ---- leaks and exhaust ----
    "He_seal_leak_sccm": (0.5, "https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9753463 (~0.5 sccm passes chuck seal; via search snippet)"),
    "He_dump_sccm": (19.5, "https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9753463 (~19.5 sccm dumped through orifice; via search snippet)"),
    "process_flow_sccm": (500.0, "ESTIMATE: HAR oxide etch C4F6/C4F8/O2/Ar total flow, 300-1000 sccm"),
    "F_atom_feed_sccm": (420.0, "ESTIMATE: 30 sccm C4F6 (6 F) + 30 sccm C4F8 (8 F) fully counted"),
    "pump_purge_slm": (50.0, "ESTIMATE: dry-pump N2 purge + ballast, 20-100 slm class"),
    "LFL_H2": (0.04, "H2 lower flammability limit 4 % in air (concept card; standard value)"),
    "rfo_sccm": (200.0, "ESTIMATE: restricting flow orifice on the H2 backside line (single-fault max flow)"),
    # ---- helium volume and value ----
    "esc_steps_per_wafer": (150, "ESTIMATE: ~100-150 etch + ~50 CVD/PVD chucked steps in a ~600-1000-step DRAM flow"),
    "min_per_step": (2.5, "ESTIMATE: average chucked time per step, min"),
    "dram_wafers_per_yr": (22.2e6, "research/phaseA/A2_materials_resources.md (DRAM fleet ~22.2M wafers/yr)"),
    "world_He_m3": (160e6, "ESTIMATE: world helium production ~160-190 million m3/yr (USGS-order value; not web-verified this session)"),
    "semi_He_share": (0.225, "https://tomshardware.com/tech-industry/semiconductors/the-global-helium-shortage-is-a-direct-threat-to-chipmaking (semis 20-25 %; via search snippet)"),
    "dram_share_of_semi_wafers": (0.17, "ESTIMATE: DRAM ~22M of ~130M 300mm-equivalent wafer starts/yr"),
    "He_price_per_Mcf": (1200.0, "https://tomshardware.com/tech-industry/semiconductors/the-global-helium-shortage-is-a-direct-threat-to-chipmaking ($1,000-1,200/Mcf spot 2026; via search snippet)"),
    "HeRS_t_per_yr": (4.7, "https://kr.linkedin.com/in/haneul-yu-49296072 (Samsung HeRS first line ~4.7 t/yr; via search snippet, weak attribution)"),
    "line_wafers_per_yr": (1.2e6, "ESTIMATE: one large DRAM line ~100k wafers/month"),
    "gb_per_wafer": (3068.0, "research/phaseA/A2_materials_resources.md / ram-venture dram_cost_stack (1-beta 3,068 GB/wafer)"),
    "ddr5_cost_per_gb": (1.48, "ram-venture models/dram_cost_stack.py ($1.48/GB 1-beta DDR5)"),
    "wafer_cost": (3800.0, "ram-venture models/dram_cost_stack.py ($3,800 1-beta wafer)"),
    "revenue_per_wafer": (9500.0, "ESTIMATE: 2026 tight-market DRAM revenue ~2.5x the $3,800 cost per wafer"),
    "fab_wpm": (100000.0, "ESTIMATE: one large DRAM fab, wafers per month"),
    "chambers_per_fab": (1500, "ESTIMATE: etch + CVD + PVD chambers with backside gas in a 100k-wpm DRAM fab"),
    "retrofit_per_chamber": (50000.0, "ESTIMATE: H2 gas stick, RFO, H2 sensor/interlock, exhaust review, requalification per chamber"),
    "H2_price_per_kg": (5.0, "ESTIMATE: on-site PEM electrolysis H2 at ~$4-6/kg"),
    # ---- AAO capacitor (Si-access cell) ----
    "eot_nm": (0.55, "research/phaseA/A1_scaling_limits.md / models/dram_cell_physics.py (ZrO2 stack EOT ~0.55 nm)"),
    "cs_1b_fF": (5.4, "research/phaseA/A1_scaling_limits.md (1-beta pillar ~5.4 fF)"),
    "cell_1b_nm2": (1070.0, "research/phaseA/A1_scaling_limits.md (1-beta 6F2 cell 1,070 nm2)"),
    "pore_frac": (0.65, "ESTIMATE: pore diameter / interpore pitch after widening (porosity ~0.38 hex); B2-01 used 26 nm at 40 nm"),
    "liner_nm": (11.0, "ESTIMATE: 2 x 3 nm TiN + ~5 nm dielectric removed from pore diameter to the mid-plane (B2-01)"),
    "nm_per_V": (2.5, "ESTIMATE: AAO interpore distance ~2.5 nm/V (Masuda/O'Sullivan rule, prior knowledge)"),
    "al_film_um": (2.75, "B2-01 (2.5-3 um Al film)"),
    "anod_V": (15.0, "B2-01 (~15-20 V anodization)"),
    "anod_eff": (0.7, "ESTIMATE: current efficiency of Al -> Al2O3 (rest O2 evolution / dissolution)"),
    "c_bl_fF": (512 * 0.06 + 4.0, "models/dram_cell_physics.py (512 cells x 0.06 fF + 4 fF)"),
    "v_array": (1.05, "models/dram_cell_physics.py (VARY 1.05 V)"),
    "si_tail_fA": (13.0, "research/stage3/FINAL_CONCEPTS.md (Si 13 fA tail-cell leakage)"),
    "dv_loss_V": (0.15, "research/stage3/FINAL_CONCEPTS.md (0.15 V allowed droop)"),
    "fab_kwh_per_wafer": (1300.0, "research/phaseA/A2_materials_resources.md (~1,300 kWh/wafer fab total)"),
    # ---- EUV-free periodic patterning ----
    "density_1b": (0.447, "research/phaseA/A1_scaling_limits.md (Micron 1-beta 0.447 Gb/mm2)"),
    "F_oxide_nm": (40.0, "FINAL_CONCEPTS.json why_bigger_than_parts (oxide cells at F ~40 nm)"),
    "array_eff_oxide": (0.70, "ESTIMATE: periphery-under-cell / bonded-periphery array efficiency (A1 white space 7)"),
    "ol_frac_of_F": (0.25, "ESTIMATE: overlay budget ~F/4 (Stage-2: ~10 nm at F 40 nm; 2.5 nm at 1-beta)"),
    "si_cte_ppm_K": (2.6, "ESTIMATE: Si CTE 2.6 ppm/K (textbook)"),
    "euv_cost_per_wafer": ((825.0, 1155.0), "research/phaseA/A1_scaling_limits.md (5-7 EUV layers at 1c, 19-27 % of $4.3k wafer)"),
}


def v(key):
    return INPUTS[key][0]


OUT = []


def P(s=""):
    OUT.append(s)


def hr(title):
    P("")
    P("## " + title)
    P("")


# --------------------------------------------------------------------------------------------
# A. Gas-gap conductance
# --------------------------------------------------------------------------------------------
def gas(name):
    M, g, k, mu, cp = v("gas_" + name)
    return {"name": name, "M": M, "gamma": g, "k": k, "mu": mu, "cp": cp,
            "m": M * 1e-3 / 6.02214076e23, "Pr": mu * cp / k}


def mean_free_path_m(gs, p_torr, T=T_GAS):
    """Chapman-Enskog hard-sphere mean free path from viscosity: lambda = (mu/p) sqrt(pi k T / 2m)."""
    return gs["mu"] / (p_torr * TORR) * math.sqrt(math.pi * KB * T / (2.0 * gs["m"]))


def jump_distance_m(gs, alpha, p_torr):
    """Smoluchowski temperature-jump distance for one surface."""
    lam = mean_free_path_m(gs, p_torr)
    return (2.0 - alpha) / alpha * (2.0 * gs["gamma"] / (gs["gamma"] + 1.0)) * lam / gs["Pr"]


def h_gas(gs, p_torr, gap_um, a_wafer, a_chuck):
    d = gap_um * 1e-6
    return gs["k"] / (d + jump_distance_m(gs, a_wafer, p_torr) + jump_distance_m(gs, a_chuck, p_torr))


def h_total(gs, p_torr, gap_um, a_wafer, a_chuck):
    return h_gas(gs, p_torr, gap_um, a_wafer, a_chuck) + v("h_contact")


def h_fm_corruccini(gs, p_torr, a1, a2, T=T_GAS):
    """Free-molecular parallel-plate limit (Corruccini 1959)."""
    a_eff = a1 * a2 / (a1 + a2 - a1 * a2)
    return a_eff * (gs["gamma"] + 1) / (gs["gamma"] - 1) * p_torr * TORR * math.sqrt(R_GAS / (8 * math.pi * gs["M"] * 1e-3 * T))


def gap_sensitivity(gs, p_torr, gap_um, a1, a2):
    """d ln h_gas / d ln gap = -d / (d + g1 + g2)."""
    d = gap_um * 1e-6
    gt = jump_distance_m(gs, a1, p_torr) + jump_distance_m(gs, a2, p_torr)
    return -d / (d + gt)


def heat_flux():
    return v("bias_W") * v("heat_fraction") / v("wafer_area_m2")


def bisect(f, lo, hi, n=80):
    flo = f(lo)
    if flo * f(hi) > 0:
        return None
    for _ in range(n):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if flo * fm <= 0:
            hi = mid
        else:
            lo, flo = mid, fm
    return 0.5 * (lo + hi)


def section_A(He, H2, N2, Ar):
    hr("A. Wafer-to-chuck gas conductance: He vs H2 vs N2 vs Ar")
    q = heat_flux()
    d = v("gap_um")
    pHe = v("p_He_Torr")
    aH2 = v("alpha_H2_central")
    P(f"Heat flux into wafer: {v('bias_W')/1e3:.1f} kW bias x {v('heat_fraction'):.2f} / {v('wafer_area_m2'):.4f} m2 = **{q/1e3:.1f} kW/m2** [ESTIMATE].")
    P(f"Gap {d:.0f} um, contact conductance {v('h_contact'):.0f} W/m2K added equally to every gas. Model: h = k/(d + g_wafer + g_chuck), "
      "Smoluchowski jump distance g = (2-a)/a * 2gamma/(gamma+1) * lambda/Pr, lambda from viscosity.")
    P("")
    P("Free-molecular check (Corruccini), per unit accommodation: H2/He conductance ratio = "
      f"**{h_fm_corruccini(H2, 10, 1, 1)/h_fm_corruccini(He, 10, 1, 1):.2f}x** (concept card: 2.1x). Continuum ratio k_H2/k_He = "
      f"**{H2['k']/He['k']:.2f}x**.")
    # check jump model reproduces Corruccini in the FM limit
    fm_jump = He["k"] / (2 * jump_distance_m(He, v("alpha_He"), 10))
    fm_corr = h_fm_corruccini(He, 10, v("alpha_He"), v("alpha_He"))
    P(f"Consistency: He at 10 Torr, gap->0, a=0.45: jump model {fm_jump:.0f} vs Corruccini {fm_corr:.0f} W/m2K "
      f"({100*(fm_jump/fm_corr-1):+.1f} %).")
    P("")
    P(f"| Gas (alpha) | p (Torr) | lambda (um) | g per surface (um) | h (W/m2K) | wafer-chuck dT (K) | d ln h / d ln gap | dT spread, gap {d-5:.0f}-{d+5:.0f} um (K) |")
    P("|---|---|---|---|---|---|---|---|")
    rows = [(He, v("alpha_He"), pHe), (H2, aH2, pHe), (H2, aH2, pHe * v("p_go_factor")), (H2, aH2, v("p_max_Torr")),
            (H2, 0.10, v("p_max_Torr")), (N2, v("alpha_N2"), pHe), (Ar, v("alpha_Ar"), pHe), (He, v("alpha_He"), v("p_max_Torr"))]
    res = {}
    for gs, a, p in rows:
        h = h_total(gs, p, d, a, a)
        dT = q / h
        dTlo = q / h_total(gs, p, d - 5, a, a)
        dThi = q / h_total(gs, p, d + 5, a, a)
        P(f"| {gs['name']} ({a:.2f}) | {p:.1f} | {mean_free_path_m(gs, p)*1e6:.1f} | {jump_distance_m(gs, a, p)*1e6:.1f} | {h:.0f} | {dT:.1f} | "
          f"{gap_sensitivity(gs, p, d, a, a):+.2f} | {dThi - dTlo:.1f} |")
        res[(gs["name"], a, p)] = h
    P("")
    P("Reading: at the He operating point, N2 (a~0.85) gives a similar *average* h, but its conductance is continuum-limited, so it "
      "tracks the local gap: the dT spread for a +/-5 um gap (wafer bow, film stress, chuck wear) is several times He's. "
      "That gap insensitivity, from a long jump distance, is why He is used. H2 is the only other gas with a long jump distance "
      "(light, poorly accommodating) AND a continuum conductivity above He's, so it is the only He-like substitute. N2/Ar remain "
      "fine for low-flux chambers (the ESC patents already list them).")
    return res


# --------------------------------------------------------------------------------------------
# B. Key unknown: H2 accommodation
# --------------------------------------------------------------------------------------------
def baule(mu):
    return 2.4 * mu / (1 + mu) ** 2


def alpha_for_parity(H2, target_h, p_torr, gap_um, chuck_alpha=None):
    """Symmetric (or fixed-chuck) H2 alpha that gives h_total = target at pressure p."""
    def f(a):
        ac = a if chuck_alpha is None else chuck_alpha
        return h_total(H2, p_torr, gap_um, a, ac) - target_h
    return bisect(f, 0.005, 1.0)


def p_for_parity(H2, target_h, a_w, a_c, gap_um, pmax=400.0):
    def f(p):
        return h_total(H2, p, gap_um, a_w, a_c) - target_h
    return bisect(f, 0.1, pmax)


def section_B(He, H2):
    hr("B. The key unknown: H2 thermal accommodation on film-coated backsides")
    ms = v("surface_mass_amu")
    bHe = baule(He["M"] / ms)
    bH2 = baule(H2["M"] / ms)
    a_est = v("alpha_He") * bH2 / bHe
    P(f"First-principles prior (Baule hard-cube mass ratio, surface mass {ms:.0f} amu): a_H2/a_He = {bH2:.3f}/{bHe:.3f} = "
      f"{bH2/bHe:.2f}; applied to the measured He value {v('alpha_He'):.2f} -> **a_H2 ~ {a_est:.2f}** before the rotational-mode "
      f"penalty. Planning value {v('alpha_H2_central'):.2f}; the card's pessimistic case is 0.10. [ESTIMATE]")
    d = v("gap_um")
    pHe = v("p_He_Torr")
    target = h_total(He, pHe, d, v("alpha_He"), v("alpha_He"))
    a_drop = alpha_for_parity(H2, target, pHe, d)
    a_go = alpha_for_parity(H2, target, pHe * v("p_go_factor"), d)
    a_max = alpha_for_parity(H2, target, v("p_max_Torr"), d)
    P("")
    P(f"Target: He at {pHe:.0f} Torr, a=0.45, gap {d:.0f} um -> h = {target:.0f} W/m2K. Break-even symmetric a_H2:")
    P(f"- drop-in at the same {pHe:.0f} Torr: **a_H2 >= {a_drop:.3f}**")
    P(f"- at {v('p_go_factor'):.1f}x He pressure ({pHe*v('p_go_factor'):.1f} Torr, GO line): **a_H2 >= {a_go:.3f}**")
    P(f"- at the clamp-limited {v('p_max_Torr'):.0f} Torr (NO-GO line): **a_H2 >= {a_max:.3f}**")
    P("")
    P("Asymmetric case (wafer film vs chuck ceramic): H2 pressure (Torr) needed for He parity; '>max' means above the clamp limit.")
    P("")
    aw_list = [0.05, 0.10, 0.15, 0.20, 0.30]
    ac_list = [0.10, 0.20, 0.30, 0.45]
    P("| a_wafer \\ a_chuck | " + " | ".join(f"{x:.2f}" for x in ac_list) + " |")
    P("|---|" + "---|" * len(ac_list))
    for aw in aw_list:
        cells = []
        for ac in ac_list:
            p = p_for_parity(H2, target, aw, ac, d)
            cells.append(">max" if (p is None or p > v("p_max_Torr")) else f"{p:.1f}")
        P(f"| {aw:.2f} | " + " | ".join(cells) + " |")
    P("")
    P("Gap sensitivity of the break-even (symmetric a_H2 for drop-in at He pressure, target recomputed for each gap):")
    P("")
    P("| gap (um) | h_He (W/m2K) | a_H2 drop-in | a_H2 at 1.5x p | a_H2 at p_max |")
    P("|---|---|---|---|---|")
    for g in (5.0, 10.0, 20.0, 40.0):
        t = h_total(He, pHe, g, v("alpha_He"), v("alpha_He"))
        r = [alpha_for_parity(H2, t, pp, g) for pp in (pHe, pHe * v("p_go_factor"), v("p_max_Torr"))]
        P(f"| {g:.0f} | {t:.0f} | " + " | ".join("n/a" if x is None else f"{x:.3f}" for x in r) + " |")
    return {"target": target, "a_drop": a_drop, "a_go": a_go, "a_max": a_max, "a_baule": a_est}


# --------------------------------------------------------------------------------------------
# C. Arcing
# --------------------------------------------------------------------------------------------
def section_C():
    hr("C. Backside arcing margin (Paschen minimum)")
    gse = v("gamma_se")
    lnl = math.log(math.log(1 + 1 / gse))
    P("V_min = (B/A) e ln(1+1/gamma_se); pd_min = e ln(1+1/gamma_se)/A. Constants are textbook [ESTIMATE].")
    P("")
    P("| Gas | V_min (V) | pd at min (Torr cm) | ratio to He |")
    P("|---|---|---|---|")
    vm = {}
    for gname, (A, B) in v("paschen").items():
        vmin = B / A * math.e * math.log(1 + 1 / gse)
        pdmin = math.e * math.log(1 + 1 / gse) / A
        vm[gname] = vmin
    for gname in ("He", "H2", "N2", "Ar"):
        A, B = v("paschen")[gname]
        pdmin = math.e * math.log(1 + 1 / gse) / A
        P(f"| {gname} | {vm[gname]:.0f} | {pdmin:.2f} | {vm[gname]/vm['He']:.2f} |")
    P("")
    P(f"H2 roughly doubles the worst-case backside breakdown voltage vs He (Stage-2 critics: ~270 vs ~150 V measured). "
      f"Raising H2 pressure moves pd right of the minimum in mm-scale gas holes, which only raises V_b further. [ESTIMATE; lnln term {lnl:.2f}]")
    return vm


# --------------------------------------------------------------------------------------------
# D. Leak-in and exhaust
# --------------------------------------------------------------------------------------------
def leak_h2_sccm(He, H2, p_h2, viscous=False):
    """Seal leak scaled from 0.5 sccm He at p_He. Molecular: Q ~ p/sqrt(M). Viscous: Q ~ p^2/mu."""
    base = v("He_seal_leak_sccm")
    pr = p_h2 / v("p_He_Torr")
    if viscous:
        return base * pr ** 2 * He["mu"] / H2["mu"]
    return base * pr * math.sqrt(He["M"] / H2["M"])


def dump_h2_sccm(He, H2, p_h2):
    return v("He_dump_sccm") * p_h2 / v("p_He_Torr") * math.sqrt(He["M"] / H2["M"])


def section_D(He, H2, p_h2):
    hr("D. H2 leak into the etch plasma and exhaust flammability")
    lm = leak_h2_sccm(He, H2, p_h2)
    lv = leak_h2_sccm(He, H2, p_h2, viscous=True)
    dump = dump_h2_sccm(He, H2, p_h2)
    hf = 2 * lm / v("F_atom_feed_sccm")
    hf_v = 2 * lv / v("F_atom_feed_sccm")
    frac_flow = lm / v("process_flow_sccm")
    tot_slm = v("pump_purge_slm") + v("process_flow_sccm") / 1000.0
    conc = (lm + dump) / 1000.0 / tot_slm
    conc_fault = v("rfo_sccm") / 1000.0 / tot_slm
    P(f"At H2 backside pressure {p_h2:.1f} Torr (scaled from 0.5 sccm He seal leak at {v('p_He_Torr'):.0f} Torr):")
    P(f"- seal leak into chamber: **{lm:.2f} sccm** (molecular scaling) to {lv:.2f} sccm (viscous scaling); {100*frac_flow:.2f} % of a {v('process_flow_sccm'):.0f} sccm recipe")
    P(f"- H atoms vs F-atom feed: **{100*hf:.1f} %** ({100*hf_v:.1f} % viscous). For scale, deliberate H-additive steps (CH2F2/H2) add several sccm; "
      "this is a recipe perturbation of that order, which is why Step 2 must measure etch rate and selectivity drift.")
    P(f"- foreline H2 with {dump:.1f} sccm dump + leak into {tot_slm:.1f} slm: **{100*conc:.3f} %** = {100*conc/v('LFL_H2'):.1f} % of LFL")
    P(f"- single fault (RFO-limited {v('rfo_sccm'):.0f} sccm): {100*conc_fault:.2f} % = **{100*conc_fault/v('LFL_H2'):.0f} % of LFL** "
      "(below the usual 25 % LFL alarm point; the NFPA 55 / SEMI S2 case rests on the RFO plus purge interlock)")
    return {"leak": lm, "leak_visc": lv, "HF": hf, "lfl_pct": 100 * conc / v("LFL_H2"), "lfl_fault_pct": 100 * conc_fault / v("LFL_H2")}


# --------------------------------------------------------------------------------------------
# E. Helium volume and value
# --------------------------------------------------------------------------------------------
def section_E(He, H2, p_h2):
    hr("E. Honest scale of the helium lever")
    flow = v("He_seal_leak_sccm") + v("He_dump_sccm")
    L_per_wafer = v("esc_steps_per_wafer") * v("min_per_step") * flow / 1000.0
    fleet_m3 = L_per_wafer * v("dram_wafers_per_yr") / 1000.0
    dram_He_m3 = v("world_He_m3") * v("semi_He_share") * v("dram_share_of_semi_wafers")
    share = fleet_m3 / dram_He_m3
    cf = L_per_wafer / 28.3168
    usd_wafer = cf / 1000.0 * v("He_price_per_Mcf")
    usd_gb = usd_wafer / v("gb_per_wafer")
    hers_L_per_wafer = v("HeRS_t_per_yr") * 1e6 / (v("gas_He")[0] / V_STP_L) / v("line_wafers_per_yr")
    h2_scale = (p_h2 / v("p_He_Torr")) * math.sqrt(He["M"] / H2["M"])
    h2_L = L_per_wafer * h2_scale
    h2_g = h2_L / V_STP_L * 2.016
    h2_usd = h2_g / 1000.0 * v("H2_price_per_kg")
    P(f"Backside He per DRAM wafer: {v('esc_steps_per_wafer')} chucked steps x {v('min_per_step')} min x {flow:.0f} sccm = **{L_per_wafer:.1f} L (STP)** [ESTIMATE].")
    P(f"Cross-check: Samsung HeRS first line ~{v('HeRS_t_per_yr')} t/yr over ~{v('line_wafers_per_yr')/1e6:.1f}M wafers/yr = {hers_L_per_wafer:.0f} L/wafer recovered "
      "(HeRS scope not disclosed; same order of magnitude).")
    P(f"Fleet backside He: {fleet_m3/1e3:.0f} thousand m3/yr = {100*fleet_m3/v('world_He_m3'):.2f} % of world He; "
      f"**~{100*share:.0f} % of DRAM's pro-rata helium** ({dram_He_m3/1e6:.1f} M m3/yr) [ESTIMATE]. Range for 3-30 L/wafer: "
      f"{100*share*3/L_per_wafer:.0f}-{100*share*30/L_per_wafer:.0f} %.")
    P(f"Cost: {usd_wafer:.2f} $/wafer at ${v('He_price_per_Mcf'):.0f}/Mcf = {usd_gb*1e6:.0f} u$/GB vs ${v('ddr5_cost_per_gb')}/GB "
      f"({100*usd_wafer/v('wafer_cost'):.3f} % of wafer cost). H2 replacement: {h2_L:.1f} L = {h2_g:.2f} g = ${h2_usd:.3f}/wafer.")
    day_rev = v("fab_wpm") / 30.0 * v("revenue_per_wafer")
    retro = v("chambers_per_fab") * v("retrofit_per_chamber")
    P(f"Outage insurance: a {v('fab_wpm')/1e3:.0f}k-wpm fab books ~${day_rev/1e6:.0f}M revenue/day; an H2 retrofit of "
      f"{v('chambers_per_fab')} chambers x ${v('retrofit_per_chamber')/1e3:.0f}k = ${retro/1e6:.0f}M pays back after **{retro/day_rev:.1f} days** of avoided full stoppage [ESTIMATE].")
    absorb = 1 - share
    P(f"**Honest consequence:** if backside cooling is only ~{100*share:.0f} % of a DRAM fab's helium, a fab under a partial cut keeps backside "
      f"cooling and sheds other uses first (leak check -> H2/N2 tracer, PECVD diluent -> Ar). H2 backside matters only in a near-total "
      f"cutoff (>~{100*absorb:.0f} % loss), or as the last step to a fully He-free line. It is a tail-risk hedge and a He-free enabler, "
      "not a volume or cost lever. The backside share is unverified and is the second number this dossier must pin down.")
    return {"L_per_wafer": L_per_wafer, "share": share, "usd_wafer": usd_wafer, "usd_gb": usd_gb, "payback_days": retro / day_rev,
            "hers_L": hers_L_per_wafer}


# --------------------------------------------------------------------------------------------
# F. AAO capacitor for Si-access cells
# --------------------------------------------------------------------------------------------
def cap_cyl_fF(mid_d_nm, h_um, eot_nm):
    return 3.9 * EPS0 * math.pi * mid_d_nm * 1e-9 * h_um * 1e-6 / (eot_nm * 1e-9) * 1e15


def section_F():
    hr("F. AAO capacitor mold for Si-access cells (no fluorocarbon HAR etch)")
    hexp = math.sqrt(2 * v("cell_1b_nm2") / math.sqrt(3))
    P(f"1-beta cell {v('cell_1b_nm2'):.0f} nm2 -> hexagonal pitch {hexp:.1f} nm -> anodization ~{hexp/v('nm_per_V'):.0f} V "
      f"(sulfuric regime; self-ordering needs imprint pretexturing). Pore = {v('pore_frac'):.2f} x pitch; mid-plane d = pore - {v('liner_nm'):.0f} nm; EOT {v('eot_nm')} nm.")
    P("")
    cbl = v("c_bl_fF")
    P(f"| pitch (nm) | height (um) | Cs (fF) | vs 1-beta 5.4 fF | signal (mV, Cbl {cbl:.1f} fF) | retention at 13 fA tail (ms) |")
    P("|---|---|---|---|---|---|")
    out = {}
    for pitch in (hexp, 40.0):
        for h in (1.3, 2.5, 3.0):
            mid = v("pore_frac") * pitch - v("liner_nm")
            cs = cap_cyl_fF(mid, h, v("eot_nm"))
            sig = v("v_array") / 2 * cs / (cs + cbl) * 1000
            ret = cs * 1e-15 * v("dv_loss_V") / (v("si_tail_fA") * 1e-15) * 1000
            P(f"| {pitch:.1f} | {h:.1f} | {cs:.2f} | {cs/v('cs_1b_fF'):.2f}x | {sig:.0f} | {ret:.0f} |")
            out[(round(pitch, 1), h)] = cs
    base_sig = v("v_array") / 2 * v("cs_1b_fF") / (v("cs_1b_fF") + cbl) * 1000
    P(f"| 1-beta pillar | 1.3 | {v('cs_1b_fF'):.2f} | 1.00x | {base_sig:.0f} | {v('cs_1b_fF')*v('dv_loss_V')/v('si_tail_fA')*1000:.0f} |")
    al_g = v("wafer_area_m2") * v("al_film_um") * 1e-6 * 2.70e6
    q_c = al_g / 26.98 * 3 * FARADAY / v("anod_eff")
    e_wh = q_c * v("anod_V") / 3600.0
    P("")
    P(f"Anodization of a full-wafer {v('al_film_um')} um Al film: {al_g:.2f} g Al, {q_c:.0f} C at {100*v('anod_eff'):.0f} % efficiency, "
      f"**{e_wh:.0f} Wh/wafer** = {100*e_wh/1000/v('fab_kwh_per_wafer'):.4f} % of fab energy. (B2-01 quoted 0.19 g / 8.4 Wh, apparently for "
      "the array area only; either way it is negligible.)")
    P("At the 1-beta pitch the AAO cup gives parity-to-+30 % Cs at 2.5-3 um, not the +37-64 % B2-01 found at 40 nm pitch: the wall "
      "liner eats a larger share of a 23 nm pore. Its value is the deleted fluorocarbon etch and support-lattice masks, not charge.")
    return out


# --------------------------------------------------------------------------------------------
# G. EUV-free periodic patterning
# --------------------------------------------------------------------------------------------
def section_G():
    hr("G. EUV-free periodic layers: overlay and density")
    F = v("F_oxide_nm")
    ol = v("ol_frac_of_F") * F
    P(f"Overlay budget ~F/4: F={F:.0f} nm oxide cell -> {ol:.0f} nm; 1-beta Si DRAM -> ~2.5 nm (Stage-2 I-07130).")
    P("")
    P("| field / exposure | residual distortion 0.05 ppm | 0.1 ppm | 0.3 ppm | 1 ppm | 0.1 K wafer-temperature error |")
    P("|---|---|---|---|---|---|")
    for name, half_mm in (("26x33 mm field, per-field phase lock", 21.0), ("full 300 mm wafer, one grating", 150.0)):
        cells = [f"{ppm*1e-6*half_mm*1e6:.1f} nm" for ppm in (0.05, 0.1, 0.3, 1.0)]
        th = v("si_cte_ppm_K") * 0.1 * 1e-6 * half_mm * 1e6
        P(f"| {name} | " + " | ".join(cells) + f" | {th:.1f} nm |")
    dens = 1e12 / (4 * F * F) * v("array_eff_oxide") / 1e9
    P("")
    P(f"Density of a 4F2 oxide cell at F={F:.0f} nm, array efficiency {v('array_eff_oxide')}: **{dens:.3f} Gb/mm2 per tier** = "
      f"{dens/v('density_1b'):.2f}x 1-beta; parity needs >= {math.ceil(v('density_1b')/dens)} tiers (or bits x tiers).")
    lo, hi = v("euv_cost_per_wafer")
    P(f"EUV removed at 1c: ${lo:.0f}-{hi:.0f}/wafer (19-27 % of wafer cost), before netting the DUV/IL steps that replace it.")
    P("Reading: a single full-wafer grating fails even a 10 nm budget (0.1 K alone moves the edge by tens of nm); IL must be "
      "field-stepped or scanning (SBIL-type) with per-field phase lock, and that only meets ~10 nm, never 2.5 nm. So EUV-free IL "
      "is legal only for the portfolio's F~40 nm oxide cells, which need tiers to reach 1-beta density.")
    return dens


# --------------------------------------------------------------------------------------------
# H. Sensitivity and GO/NO-GO
# --------------------------------------------------------------------------------------------
def section_H(He, H2, B):
    hr("H. Sensitivity on the key unknown (symmetric a_H2) and GO/NO-GO")
    d = v("gap_um")
    pHe = v("p_He_Torr")
    q = heat_flux()
    target = B["target"]
    dT_He = q / target
    P(f"Baseline He: {pHe:.0f} Torr, h {target:.0f} W/m2K, wafer-chuck dT {dT_He:.1f} K at {q/1e3:.1f} kW/m2. Window +/-{v('dT_window_K'):.0f} K.")
    P("")
    P("| a_H2 | h at He pressure | dT shift at He pressure (K) | parity pressure (Torr) | leak at parity (sccm) | H/F atoms | foreline % LFL | verdict |")
    P("|---|---|---|---|---|---|---|---|")
    for a in (0.05, 0.08, 0.10, 0.13, 0.16, 0.20, 0.25, 0.30, 0.45):
        h0 = h_total(H2, pHe, d, a, a)
        shift = q / h0 - dT_He
        pp = p_for_parity(H2, target, a, a, d)
        if pp is None or pp > v("p_max_Torr"):
            P(f"| {a:.2f} | {h0:.0f} | {shift:+.1f} | >{v('p_max_Torr'):.0f} | - | - | - | NO-GO (clamp limit) |")
            continue
        lk = leak_h2_sccm(He, H2, pp)
        dump = dump_h2_sccm(He, H2, pp)
        conc = (lk + dump) / 1000.0 / (v("pump_purge_slm") + v("process_flow_sccm") / 1000.0)
        if pp <= pHe * 1.0001 or abs(shift) <= v("dT_window_K"):
            verdict = "GO (drop-in)"
        elif pp <= pHe * v("p_go_factor"):
            verdict = "GO (raise p)"
        else:
            verdict = "CONDITIONAL"
        P(f"| {a:.2f} | {h0:.0f} | {shift:+.1f} | {max(pp, 0):.1f} | {lk:.2f} | {100*2*lk/v('F_atom_feed_sccm'):.1f} % | "
          f"{100*conc/v('LFL_H2'):.1f} % | {verdict} |")
    P("")
    P("Bias-power sensitivity (a_H2 = planning value): dT for He and H2 at He pressure and at the GO pressure.")
    P("")
    P("| bias (kW) | q (kW/m2) | dT He (K) | dT H2 @ He p (K) | dT H2 @ 1.5x p (K) |")
    P("|---|---|---|---|---|")
    a = v("alpha_H2_central")
    for kw in (2.0, 3.0, 5.0, 10.0):
        qq = kw * 1e3 * v("heat_fraction") / v("wafer_area_m2")
        P(f"| {kw:.0f} | {qq/1e3:.1f} | {qq/target:.1f} | {qq/h_total(H2, pHe, d, a, a):.1f} | "
          f"{qq/h_total(H2, pHe*v('p_go_factor'), d, a, a):.1f} |")


def main():
    He, H2, N2, Ar = gas("He"), gas("H2"), gas("N2"), gas("Ar")
    P("# LEAN ARRAY MODULE -- model output")
    P("")
    P("Generated by `models/lean-array-module.py` (pure stdlib). Every input carries a source URL or an ESTIMATE basis in the INPUTS block. "
      "Axis: supply-chain exposure (helium, PFAS etch gas, EUV), not $/bit.")
    A = section_A(He, H2, N2, Ar)
    B = section_B(He, H2)
    C = section_C()
    p_go = v("p_He_Torr") * v("p_go_factor")
    D = section_D(He, H2, p_go)
    E = section_E(He, H2, p_go)
    Fz = section_F()
    G = section_G()
    section_H(He, H2, B)

    hr("HEADLINE")
    P(f"- H2 per unit accommodation conducts **{h_fm_corruccini(H2, 10, 1, 1)/h_fm_corruccini(He, 10, 1, 1):.2f}x** He (free-molecular) and "
      f"**{H2['k']/He['k']:.2f}x** (continuum); with a_H2 = {v('alpha_H2_central')} vs a_He = 0.45 it reaches He parity at "
      f"{p_for_parity(H2, B['target'], v('alpha_H2_central'), v('alpha_H2_central'), v('gap_um')):.1f} Torr (He: {v('p_He_Torr'):.0f} Torr).")
    P(f"- Break-even a_H2: {B['a_drop']:.2f} (drop-in), {B['a_go']:.2f} (<=1.5x pressure), {B['a_max']:.2f} (clamp limit {v('p_max_Torr'):.0f} Torr). "
      f"Baule prior: {B['a_baule']:.2f}.")
    P(f"- Paschen minimum H2/He = {C['H2']/C['He']:.1f}x (less backside arcing).")
    P(f"- Leak into plasma at the GO pressure: {D['leak']:.2f}-{D['leak_visc']:.2f} sccm; H/F {100*D['HF']:.1f} %; foreline {D['lfl_pct']:.1f} % LFL "
      f"(single fault {D['lfl_fault_pct']:.0f} % LFL).")
    P(f"- Helium lever: ~{E['L_per_wafer']:.1f} L He/wafer, ~{100*E['share']:.0f} % of DRAM's pro-rata helium, ${E['usd_wafer']:.2f}/wafer "
      f"({E['usd_gb']*1e6:.0f} u$/GB vs $1.48/GB). Retrofit pays back after ~{E['payback_days']:.1f} days of avoided stoppage. Hedge, not cost lever.")
    P(f"- AAO at the 1-beta pitch, 2.5-3 um: {Fz[(round(math.sqrt(2*v('cell_1b_nm2')/math.sqrt(3)),1),2.5)]:.1f}-"
      f"{Fz[(round(math.sqrt(2*v('cell_1b_nm2')/math.sqrt(3)),1),3.0)]:.1f} fF vs 5.4 fF; value is the deleted fluorocarbon etch.")
    P(f"- EUV-free IL: ~10 nm overlay only (F~40 nm oxide cells, {G:.3f} Gb/mm2 per tier -> >=5 tiers for 1-beta parity).")

    hr("GO / NO-GO")
    P(f"**GO** if the Step-1 rig measures an effective H2 accommodation **a_H2 >= {B['a_go']:.2f}** (symmetric equivalent; wafer-side SiN/SiO2/poly "
      f"films against an Al2O3/AlN chuck counterface, 20-60 C, including fluorocarbon-polymer-contaminated backsides). H2 then matches He wafer "
      f"cooling at <= {p_go:.1f} Torr. **NO-GO** if a_H2 < {B['a_max']:.2f}: parity would need > {v('p_max_Torr'):.0f} Torr, past the clamp limit "
      f"(fallbacks: He recapture, H2/He blend, or a chuck coating that raises a_H2). Step 2 (300 mm chamber) must then show wafer temperature "
      f"within +/-{v('dT_window_K'):.0f} K of He across the wafer, HAR oxide etch-rate drift <= 2 % and mask-selectivity drift <= 5 % at 2x the predicted "
      f"{D['leak']:.1f} sccm leak, and foreline H2 <= 10 % LFL in single fault.")

    text = "\n".join(OUT) + "\n"
    print(text)
    here = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.normpath(os.path.join(here, "..", "research", "stage3", "lean-array-module_model_output.md"))
    try:
        with open(out_path, "w") as f:
            f.write(text)
    except OSError as e:
        print(f"[warn] could not write {out_path}: {e}")


if __name__ == "__main__":
    main()
