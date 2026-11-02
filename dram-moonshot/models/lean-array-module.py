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
  I. RED-TEAM VARIANTS (added 2026-11-02 after the four-persona red team, research/redteam/rt_*.json):
     rotational-accommodation penalty and D2 diagnostic (RT-DEV-01), radial H2 profile and edge-He guard
     zone (RT-PROC-01), oxide-channel chamber exclusion (RT-DEV-02 / RT-CIRC-01), cryogenic chucks
     (RT-PROC-04), requalification cost and insurance value (RT-PROC-05 / RT-IND-04), AAO geometry closure,
     80 nm retarget and missing-pore budget (RT-DEV-03 / RT-CIRC-02 / RT-PROC-03), A1 droop convention
     (RT-CIRC-03), fluorocarbon inventory (RT-PROC-02 / RT-CIRC-04), gallium stockpile (RT-DEV-05).
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

# --------------------------------------------------------------------------------------------
# RED-TEAM REVISIONS (2026-11-02; objections in research/redteam/rt_*.json, responses in
# research/redteam/responses_lean-array-module.json). Format: old -> new (objection id).
#  - alpha_H2 prior: "Baule 0.27 clears the GO line" -> 0.27 is the TRANSLATIONAL prior; with H2 rotational
#    accommodation r = 0.1-0.3 of translational the EFFECTIVE prior is 0.19-0.21 (RT-DEV-lean-array-module-01).
#    Planning value alpha_H2_central stays 0.20, now justified as the effective value; P4 -> P3.
#  - retrofit cost: $50k/chamber hardware only (2.4-day payback) -> hardware + per-family requalification
#    $1.5M x 50 families (payback ~4.7 days brownfield; ~2.6 days greenfield) (RT-PROC-05).
#  - AAO: 35.2 nm pitch with an unstated three-layer fill -> fill closure checked (core ~5.6 nm, AR ~450),
#    1-beta-pitch leg killed; module retargeted to 80 nm pitch for F~40 nm oxide 1T1C tiers
#    (RT-CIRC-02, RT-DEV-03). Missing-pore kill line 1e-4 -> 1e-6 (RT-PROC-03).
#  - retention convention: fixed 0.15 V droop -> A1's 50 mV end-of-retention signal (RT-CIRC-03).
#  - new inputs below for the radial H2 profile, oxide-exposed step share, cryo gas properties, fluorocarbon
#    inventory, gallium mass and D2 diagnostic gas.
# --------------------------------------------------------------------------------------------
RT = {
    "rot_ratio_H2": ((0.05, 0.1, 0.2, 0.3, 0.5, 1.0),
                     "https://ornl.gov/publication/measurement-and-modeling-hydrogen-molecule-ro-vibrational-accommodation-e-204 "
                     "(H2/D2 rotational accommodation on graphite ~0.05-0.2; ratio to translational assumed 0.1-0.4; RT-DEV-01)"),
    "prior_sigma_ln": (math.log(1.5), "ESTIMATE: lognormal spread (factor 1.5, 1 sigma) on the effective a_H2 prior across films"),
    "gas_D2": ((4.028, 1.400, 0.141, 1.26e-5, 7225.0),
               "ESTIMATE: CRC-class 300 K D2 properties (prior knowledge; cp = 3.5R/M); diagnostic gas for the rig"),
    "rot_ratio_D2": ((0.3, 0.6), "ESTIMATE: D2 rotational quanta are half H2's (J=0->2 ~22 meV < kT), so r is higher than H2's"),
    "chamber_p_mTorr": ((30.0, 80.0), "ESTIMATE: HAR oxide etch chamber pressure 20-80 mTorr (RT-PROC-01 edge analysis)"),
    "flow_sccm_case": ((500.0, 1500.0), "ESTIMATE: total process flow for the two cases"),
    "gap_height_cm": (3.0, "ESTIMATE: wafer-to-showerhead/upper-electrode gap, 2-4 cm class for ICP/CCP HAR etch"),
    "D_H2_Ar_1atm_cm2s": (0.83, "ESTIMATE: H2-Ar binary diffusion coefficient at 300 K, 1 atm (textbook ~0.8 cm2/s)"),
    "outer_zone_r_mm": (130.0, "ESTIMATE: inner/outer backside-zone boundary of a dual-zone ESC (edge-He guard zone, RT-PROC-01)"),
    "har_step_frac": (0.30, "ESTIMATE: share of chucked steps that are HAR/critical fluorocarbon etches needing the edge guard"),
    "oxide_exposed_step_frac": ((0.10, 0.15, 0.25), "ESTIMATE: share of chucked steps in an oxide-cell line that see an exposed or "
                                "near-surface oxide channel (RT-DEV-02 / RT-CIRC-01); 0 for today's Si-access DRAM"),
    # cryo chuck (RT-PROC-04): gas properties at ~220 K
    "T_cryo_K": (220.0, "ESTIMATE: backside gas temperature between a -70 C chuck and a ~-40 C wafer"),
    "gas_He_cryo": ((4.0026, 1.667, 0.124, 1.61e-5, 5193.0), "ESTIMATE: He at 220 K (k, mu scaled T^0.68-0.7 from 300 K)"),
    "gas_H2_cryo": ((2.016, 1.43, 0.139, 7.26e-6, 13740.0),
                    "ESTIMATE: normal-H2 at 220 K: Cp ~27.7 J/mol/K (rotational modes partly frozen), gamma ~1.43"),
    # requalification and insurance (RT-PROC-05 / RT-IND-04)
    "chamber_families": ((30, 50, 80), "ESTIMATE: distinct chamber-type x recipe families to requalify in a DRAM fab"),
    "requal_per_family": ((0.5e6, 1.5e6, 3.0e6), "ESTIMATE: 100-300 qual wafers at $3.8k + metrology + reliability lots + PCN engineering"),
    "greenfield_requal_frac": (0.10, "ESTIMATE: incremental qualification cost when H2 is qualified during a new fab's ramp"),
    "cutoff_prob_per_yr": ((0.005, 0.01, 0.03), "ESTIMATE [SPECULATIVE]: annual probability that a fab's helium cut exceeds "
                           "(1 - backside share) beyond storage, i.e. backside cooling becomes the binding use"),
    "cutoff_days": (30.0, "ESTIMATE: stoppage days avoided per binding event"),
    # AAO (RT-DEV-03 / RT-CIRC-02 / RT-PROC-03 / RT-CIRC-03)
    "tin_outer_nm_1b": (3.0, "B2-01 / model liner basis (2 x 3 nm TiN)"),
    "zro2_k": (40.0, "ESTIMATE: tetragonal ZrO2 k ~40 (A1 EOT 0.55 nm basis)"),
    "tin_resistivity_ohm_m": (3.0e-6, "ESTIMATE: few-nm ALD TiN ~300 uOhm cm"),
    "today_cap_AR": (62.0, "RT-DEV-03 (today's AR-62 pillar)"),
    "aao_pitch_oxide_nm": ((80.0, 86.0), "F=40 nm 4F2 cell: 80 nm square pitch; 86 nm = hexagonal pitch of a 6,400 nm2 cell"),
    "tin_nm_oxide": (5.0, "ESTIMATE: thicker 5 nm TiN electrodes affordable at 80 nm pitch"),
    "cbl_oxide_fF": (34.7, "same 512-cell bitline as the 1-beta case (conservative for oxide cells)"),
    "igzo_tail_A": (1e-18, "research/phaseA/A1_scaling_limits.md (IGZO access device at Ioff = 1 aA)"),
    "dv_min_mV": (50.0, "models/dram_cell_physics.py dv_min_mV (A1 end-of-retention signal budget)"),
    "die_bits": (16 * 2 ** 30, "16 Gb die"),
    "ecc_word_bits": (136, "DDR5 on-die SEC: 128 data + 8 check bits"),
    # fluorocarbon inventory (RT-PROC-02 / RT-CIRC-04): scc of C4F6/C4F8/CF4/CHF3 per wafer [ESTIMATE]
    "fc_cap_mold_scc": (1200.0, "ESTIMATE: AR-60 mold etch ~12 min x 80 sccm FC + 3 support-lattice opens x 2 min x 40 sccm"),
    "fc_other_scc": (2000.0, "ESTIMATE: ~25 other oxide/nitride etches x 2 min x 40 sccm FC (contacts, spacers, vias, hard masks); NF3 cleans excluded"),
    "fc_margin_add_scc": (340.0, "ESTIMATE: MARGIN STACK VCT pillar + buried-bitline etch (2 x 3 min x 50 sccm) + 120 nm stub (1 min x 40 sccm)"),
    "fc_3d_add_scc": (4000.0, "ESTIMATE: 3D oxide cell (AND-STACK class) AR-60 hole through ~320 sublayers ~30 min x 100 sccm + slits ~1,000 scc"),
    "cryo_hf_fc_cut": (0.8, "https://semiengineering.com/cryogenic-etch-a-key-enabler-of-3d-nand/ (HF/PF3 cryo 'greatly reduces' CF partial pressure; 80 % cut assumed)"),
    # gallium (RT-DEV-05)
    "igzo_nm": (10.0, "ESTIMATE: IGZO channel film thickness"),
    "igzo_area_factor": (3.0, "ESTIMATE: film area / wafer area for vertical-channel sidewalls"),
    "igzo_tiers": (5, "model section G (>=5 F40 tiers)"),
    "igzo_util": (0.3, "ESTIMATE: PVD target / ALD precursor utilisation"),
    "ga_mass_frac": (69.72 / 313.9, "InGaZnO4 stoichiometry (Ga 69.72 of 313.9 g/mol)"),
    "igzo_density": (6.4, "ESTIMATE: IGZO density g/cm3"),
    "ga_price_per_kg": (700.0, "ESTIMATE: ex-China gallium price 2025-26, $300-1,000/kg"),
}


def rv(key):
    return RT[key][0]


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
def gas(name, props=None):
    M, g, k, mu, cp = v("gas_" + name) if props is None else props
    return {"name": name, "M": M, "gamma": g, "k": k, "mu": mu, "cp": cp,
            "m": M * 1e-3 / 6.02214076e23, "Pr": mu * cp / k}


def mean_free_path_m(gs, p_torr, T=T_GAS):
    """Chapman-Enskog hard-sphere mean free path from viscosity: lambda = (mu/p) sqrt(pi k T / 2m)."""
    return gs["mu"] / (p_torr * TORR) * math.sqrt(math.pi * KB * T / (2.0 * gs["m"]))


def jump_distance_m(gs, alpha, p_torr, T=T_GAS):
    """Smoluchowski temperature-jump distance for one surface."""
    lam = mean_free_path_m(gs, p_torr, T)
    return (2.0 - alpha) / alpha * (2.0 * gs["gamma"] / (gs["gamma"] + 1.0)) * lam / gs["Pr"]


def h_gas(gs, p_torr, gap_um, a_wafer, a_chuck, T=T_GAS):
    d = gap_um * 1e-6
    return gs["k"] / (d + jump_distance_m(gs, a_wafer, p_torr, T) + jump_distance_m(gs, a_chuck, p_torr, T))


def h_total(gs, p_torr, gap_um, a_wafer, a_chuck, T=T_GAS):
    return h_gas(gs, p_torr, gap_um, a_wafer, a_chuck, T) + v("h_contact")


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
    f_lo, f_hi = (4 + 2 * 0.1) / 6, (4 + 2 * 0.3) / 6
    P(f"RED-TEAM (RT-DEV-01): Baule is a translational prior. With H2 rotational accommodation 0.1-0.3x translational, the effective "
      f"coefficient (the one h_gas() fits, with (gamma+1)/(gamma-1) = 6) is {a_est:.2f} x (4+2r)/6 = **{a_est*f_lo:.2f}-{a_est*f_hi:.2f}**, "
      "so the planning value 0.20 is the effective prior, not a pessimistic one (section I1).")
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
      f"{v('chambers_per_fab')} chambers x ${v('retrofit_per_chamber')/1e3:.0f}k = ${retro/1e6:.0f}M of hardware pays back after {retro/day_rev:.1f} days of avoided full stoppage [ESTIMATE].")
    fam, rq = RT["chamber_families"][0][1], RT["requal_per_family"][0][1]
    retro_rt = retro + fam * rq
    P(f"RED-TEAM (RT-PROC-05): adding requalification ({fam} chamber families x ${rq/1e6:.1f}M) gives ${retro_rt/1e6:.0f}M and "
      f"**{retro_rt/day_rev:.1f} days** (brownfield; old 2.4 days was hardware only). Range and greenfield case in section I5.")
    absorb = 1 - share
    P(f"**Honest consequence:** if backside cooling is only ~{100*share:.0f} % of a DRAM fab's helium, a fab under a partial cut keeps backside "
      f"cooling and sheds other uses first (leak check -> H2/N2 tracer, PECVD diluent -> Ar). H2 backside matters only in a near-total "
      f"cutoff (>~{100*absorb:.0f} % loss), or as the last step to a fully He-free line. It is a tail-risk hedge and a He-free enabler, "
      "not a volume or cost lever. The backside share is unverified and is the second number this dossier must pin down.")
    return {"L_per_wafer": L_per_wafer, "share": share, "usd_wafer": usd_wafer, "usd_gb": usd_gb, "payback_days": retro / day_rev,
            "payback_days_rt": retro_rt / day_rev, "hers_L": hers_L_per_wafer, "day_rev": day_rev, "retro_hw": retro}


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


# --------------------------------------------------------------------------------------------
# I. RED-TEAM VARIANTS (2026-11-02)
# --------------------------------------------------------------------------------------------
def phi(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def p_for_parity_T(gs, target_h, a_w, a_c, gap_um, T, pmax=400.0):
    return bisect(lambda p: h_total(gs, p, gap_um, a_w, a_c, T) - target_h, 0.1, pmax)


def alpha_for_parity_T(gs, target_h, p_torr, gap_um, T):
    return bisect(lambda a: h_total(gs, p_torr, gap_um, a, a, T) - target_h, 0.005, 1.0)


def section_I(He, H2, B, D, E):
    hr("I. RED-TEAM VARIANTS (objection ids from research/redteam/rt_*.json)")
    d = v("gap_um")
    pHe = v("p_He_Torr")
    target = B["target"]
    out = {}

    # I1 rotational accommodation (RT-DEV-01)
    P("### I1. Rotational accommodation of H2 (RT-DEV-lean-array-module-01)")
    P("")
    P("Free-molecular energy flux per molecule: translation carries 2kT (factor 4 in (gamma+1)/(gamma-1) units), H2 rotation kT "
      "(factor 2). With rotational accommodation r x translational: effective a = a_trans x (4+2r)/6. Baule gives a_trans ~ "
      f"{B['a_baule']:.2f}.")
    P("")
    P("| r = a_rot/a_trans | (4+2r)/6 | H2/He FM ratio per unit a_trans | effective a_H2 prior | parity pressure (Torr) | verdict |")
    P("|---|---|---|---|---|---|")
    fm_ratio = h_fm_corruccini(H2, 10, 1, 1) / h_fm_corruccini(He, 10, 1, 1)
    for r in rv("rot_ratio_H2"):
        f = (4 + 2 * r) / 6
        a_eff = B["a_baule"] * f
        pp = p_for_parity(H2, target, a_eff, a_eff, d)
        verdict = "GO (drop-in)" if a_eff >= B["a_drop"] else ("GO (raise p)" if a_eff >= B["a_go"] else
                                                                 ("CONDITIONAL" if a_eff >= B["a_max"] else "NO-GO"))
        P(f"| {r:.2f} | {f:.2f} | {fm_ratio*f:.2f}x | {a_eff:.3f} | {pp:.1f} | {verdict} |")
    med_old = B["a_baule"]
    med_new = B["a_baule"] * (4 + 2 * 0.2) / 6
    sg = rv("prior_sigma_ln")
    pgo_old = 1 - phi(math.log(B["a_go"] / med_old) / sg)
    pgo_new = 1 - phi(math.log(B["a_go"] / med_new) / sg)
    pno_new = phi(math.log(B["a_max"] / med_new) / sg)
    P("")
    P(f"Lognormal prior (1-sigma factor 1.5): P(a >= GO {B['a_go']:.3f}) = **{100*pgo_old:.0f} %** with the old median {med_old:.2f} -> "
      f"**{100*pgo_new:.0f} %** with the effective median {med_new:.3f}; P(NO-GO, a < {B['a_max']:.3f}) = {100*pno_new:.0f} %. "
      f"GO needs the WORST of four films (SiO2, SiN, poly, CFx) to pass: with 1-2 effectively independent draws, "
      f"P = {100*pgo_new**2:.0f}-{100*pgo_new:.0f} % (old median: {100*pgo_old**2:.0f}-{100*pgo_old:.0f} %). Adsorbate films "
      "(H on W 0.54 -> 0.14) add a fat lower tail this lognormal does not hold, so carry P3 (~35-55 %), not P4 (50-75 %).")
    out["pgo_old"], out["pgo_new"], out["a_eff_med"] = pgo_old, pgo_new, med_new
    D2 = gas("D2", rv("gas_D2"))
    P("")
    P("D2 as a rig diagnostic and CONDITIONAL-chamber fallback: same mass as He (same Baule a_trans ~0.45), rotational quanta half H2's.")
    P("")
    P("| gas | a_eff | h at 15 Torr (W/m2K) | vs He | parity pressure (Torr) |")
    P("|---|---|---|---|---|")
    for r in rv("rot_ratio_D2"):
        a = v("alpha_He") * (4 + 2 * r) / 6
        h = h_total(D2, pHe, d, a, a)
        pp = p_for_parity(D2, target, a, a, d)
        P(f"| D2 (r={r:.1f}) | {a:.3f} | {h:.0f} | {h/target:.2f}x | {pp:.1f} |")
    P("Reading: H2 vs D2 on the same coupon separates the mass (translational) term from the rotational term; if D2 passes where H2 "
      "fails, the shortfall is rotational and a blend or D2 (recaptured; [SPECULATIVE] cost) is the fallback. D is also a donor in oxide "
      "channels, so I3 applies to D2 too.")

    # I2 radial H2 profile and edge-He guard (RT-PROC-01)
    P("")
    P("### I2. Where the leaked H2 sits on the wafer (RT-PROC-lean-array-module-01)")
    P("")
    P("1-D radial advection-diffusion above the wafer: process gas injected uniformly, flowing outward (v grows with r); the seal leak "
      "enters at r = R. Upstream of the source the steady profile is c(r)/c(R) = exp(-k (R^2 - r^2)/2), k = Q_vol/(2 pi R^2 h D). "
      "Downstream of the source c equals the fully mixed value, so **the wafer edge sees the section-D H/F figure and the interior sees less**.")
    P("")
    P("| chamber p (mTorr) | flow (sccm) | D_H2 (cm2/s) | v at edge (cm/s) | Peclet (1 cm) | c(centre)/c(edge) | edge H/F (molecular-viscous) |")
    P("|---|---|---|---|---|---|---|")
    R = 15.0
    hgt = rv("gap_height_cm")
    for pm, fl in zip(rv("chamber_p_mTorr"), rv("flow_sccm_case")):
        p_atm = pm / 1000.0 / 760.0
        Dh = rv("D_H2_Ar_1atm_cm2s") / p_atm
        Q = fl / p_atm * (T_GAS / 273.15) / 60.0
        vR = Q / (2 * math.pi * R * hgt)
        k = Q / (2 * math.pi * R * R * hgt * Dh)
        cc = math.exp(-k * R * R / 2)
        scale = 500.0 / fl
        P(f"| {pm:.0f} | {fl:.0f} | {Dh:,.0f} | {vR:.0f} | {vR/Dh:.2f} | {cc:.2f} | {100*D['HF']*scale:.2f}-{100*2*D['leak_visc']/v('F_atom_feed_sccm')*scale:.2f} % |")
    ro = rv("outer_zone_r_mm") / 150.0
    a_out = 1 - ro ** 2
    dump, leak = v("He_dump_sccm"), v("He_seal_leak_sccm")
    retained = (a_out * dump + leak) / (dump + leak)
    out["guard_retained"] = retained
    P("")
    P(f"Edge-He guard zone: run He (or Ar) in the outer zone (r > {rv('outer_zone_r_mm'):.0f} mm, {100*a_out:.0f} % of the area) and H2 inside. "
      f"The outer seal then leaks He, so H2 into the plasma falls to ~0 (only the inner-zone seal leaks H2, into the He zone). Helium kept: "
      f"({100*a_out:.0f} % x {dump:.1f} + {leak:.1f}) / {dump+leak:.0f} sccm = **{100*retained:.0f} %**; H2 still replaces **{100*(1-retained):.0f} %** "
      "of backside He in that chamber. Per-zone composition is already one of the dossier's claimable actuators.")

    # I3 oxide-channel exclusion (RT-DEV-02 / RT-CIRC-01)
    P("")
    P("### I3. Hydrogen and oxide channels (RT-DEV-02, RT-CIRC-01)")
    P("")
    lk_H = 2 * D["leak_visc"]
    P(f"Leak H atoms at the viscous bound: {lk_H:.1f} sccm-equivalent. Against the H already in a recipe [ESTIMATE flows]:")
    P("")
    P("| step | recipe H atoms (sccm-eq.) | leak share | rule |")
    P("|---|---|---|---|")
    for name, hflow in (("PECVD SiN (100 SiH4 + 400 NH3)", 100 * 4 + 400 * 3), ("PECVD TEOS oxide (~107 sccm TEOS x 20 H)", 107 * 20),
                        ("HAR FC etch with 10 sccm CH2F2", 20), ("O2-plasma ALD / PVD (Ar) on an exposed oxide channel", 0)):
        share = "dominant" if hflow == 0 else f"{100*lk_H/(hflow+lk_H):.1f} %"
        rule = "H2 allowed" if hflow >= 100 * lk_H else ("H2 allowed, monitor" if hflow > 0 else "EXCLUDE (keep He/Ar)")
        P(f"| {name} | {hflow} | {share} | {rule} |")
    P("")
    P("Share of backside He that H2 can replace (steps excluded keep He or Ar; edge guard only in HAR etch chambers):")
    P("")
    P("| line | oxide-exposed step share | H2 share, no guard | H2 share, guard in HAR chambers |")
    P("|---|---|---|---|")
    har = rv("har_step_frac")
    rows = [("Si-access DRAM (today)", 0.0)] + [("oxide-cell line", f) for f in rv("oxide_exposed_step_frac")]
    for name, f in rows:
        P(f"| {name} | {100*f:.0f} % | {100*(1-f):.0f} % | {100*(1-f)*(1-har*retained):.0f} % |")
    out["ox_share_mid"] = (1 - rv("oxide_exposed_step_frac")[1])

    # I4 cryogenic chucks (RT-PROC-04)
    P("")
    P("### I4. Cryogenic chucks (-70 C) (RT-PROC-lean-array-module-04)")
    P("")
    Tc = rv("T_cryo_K")
    Hec, H2c = gas("He", rv("gas_He_cryo")), gas("H2", rv("gas_H2_cryo"))
    tgt_c = h_total(Hec, pHe, d, v("alpha_He"), v("alpha_He"), Tc)
    a_drop_c = alpha_for_parity_T(H2c, tgt_c, pHe, d, Tc)
    a_go_c = alpha_for_parity_T(H2c, tgt_c, pHe * v("p_go_factor"), d, Tc)
    a_max_c = alpha_for_parity_T(H2c, tgt_c, v("p_max_Torr"), d, Tc)
    fmr_c = ((H2c["gamma"] + 1) / (H2c["gamma"] - 1) / math.sqrt(H2c["M"])) / ((Hec["gamma"] + 1) / (Hec["gamma"] - 1) / math.sqrt(Hec["M"]))
    P(f"Gas at {Tc:.0f} K: normal-H2 gamma {H2c['gamma']:.2f} (rotation partly frozen), FM ratio per unit a = {fmr_c:.2f}x (300 K: {fm_ratio:.2f}x). "
      f"He at 15 Torr, a = 0.45: h = {tgt_c:.0f} W/m2K (300 K: {target:.0f}).")
    P(f"Break-even a_H2 at {Tc:.0f} K: drop-in **{a_drop_c:.3f}**, 1.5x pressure **{a_go_c:.3f}**, clamp limit **{a_max_c:.3f}** "
      f"(300 K: {B['a_drop']:.3f} / {B['a_go']:.3f} / {B['a_max']:.3f}). The GO line moves by {a_go_c-B['a_go']:+.3f}: the gas physics barely "
      "changes; the risk is the surface (condensed by-products, adsorbed H) at -70 C, which only a cryo rig measurement settles.")
    out["a_go_cryo"] = a_go_c

    # I5 requalification and insurance (RT-PROC-05 / RT-IND-04)
    P("")
    P("### I5. Requalification cost and insurance value (RT-PROC-05, RT-IND-04)")
    P("")
    hw = E["retro_hw"]
    dr = E["day_rev"]
    P("| case | families | $/family | total ($M) | payback (days of full stoppage) |")
    P("|---|---|---|---|---|")
    for lab, fam, rq in zip(("low", "mid", "high"), rv("chamber_families"), rv("requal_per_family")):
        tot = hw + fam * rq
        P(f"| brownfield {lab} | {fam} | {rq/1e6:.1f}M | {tot/1e6:.0f} | {tot/dr:.1f} |")
    mid_req = rv("chamber_families")[1] * rv("requal_per_family")[1]
    gf = hw + rv("greenfield_requal_frac") * mid_req
    bf = hw + mid_req
    P(f"| greenfield (qualify during ramp) | - | - | {gf/1e6:.0f} | {gf/dr:.1f} |")
    P("")
    P("Backside cooling is the binding helium use only when a fab's cut exceeds (1 - backside share) after storage: "
      + ", ".join(f"{100*(1-sh):.0f} % for a {100*sh:.0f} % share" for sh in (0.01, E["share"], 0.11)) + ".")
    P("")
    P("| P(binding cutoff)/yr [SPECULATIVE] | expected value ($M/yr) | years to recover brownfield mid | greenfield |")
    P("|---|---|---|---|")
    for pr in rv("cutoff_prob_per_yr"):
        ev = pr * rv("cutoff_days") * dr
        P(f"| {100*pr:.1f} % | {ev/1e6:.1f} | {bf/ev:.0f} | {gf/ev:.1f} |")
    P("Reading: dual qualification is option value for tail risk, best bought on greenfield lines (Micron Idaho/New York, new Korean "
      "fabs), not a brownfield retrofit with a days-scale payback. Qualification takes months, so it must exist before the crisis.")
    out["payback_bf"], out["payback_gf"] = bf / dr, gf / dr

    # I6 AAO closure, retarget, missing-pore budget (RT-DEV-03 / RT-CIRC-02 / RT-PROC-03)
    P("")
    P("### I6. AAO: geometry closure at the 1-beta pitch, retarget to 80 nm, missing-pore budget (RT-DEV-03, RT-CIRC-02, RT-PROC-03)")
    P("")
    hexp = math.sqrt(2 * v("cell_1b_nm2") / math.sqrt(3))
    pore = v("pore_frac") * hexp
    tz = v("eot_nm") * rv("zro2_k") / 3.9
    t_o = rv("tin_outer_nm_1b")
    core = pore - 2 * t_o - 2 * tz
    mid_chk = pore - 2 * t_o - tz
    P(f"1-beta pitch {hexp:.1f} nm: pore {pore:.1f} nm; ZrO2 at EOT {v('eot_nm')} nm and k {rv('zro2_k'):.0f} is {tz:.2f} nm; outer TiN {t_o:.0f} nm. "
      f"Mid-plane {mid_chk:.1f} nm (model used {pore - v('liner_nm'):.1f}); **inner-electrode core {core:.1f} nm**.")
    P("")
    P("| depth (um) | mold AR | ALD dose vs AR-62 (AR^2) | core AR | core TiN rod R (kOhm) | distributed RC (ns) |")
    P("|---|---|---|---|---|---|")
    for h in (2.5, 3.0):
        ar = h * 1000 / pore
        rr = rv("tin_resistivity_ohm_m") * h * 1e-6 / (math.pi * (core * 0.5e-9) ** 2)
        cs = cap_cyl_fF(pore - v("liner_nm"), h, v("eot_nm"))
        P(f"| {h:.1f} | {ar:.0f} | {(ar/rv('today_cap_AR'))**2:.1f}x | {h*1000/core:.0f} | {rr/1e3:.0f} | {rr*cs*1e-15/2*1e9:.2f} |")
    P("Reading: RC is not the blocker; a conformal three-layer fill leaving a ~5.6 nm core at AR ~450, with 3 nm outer TiN, is. "
      "The 1-beta-pitch leg is killed (revival: TEM-verified fill >=2 um at <=36 nm pitch, >=5 fF/pore, <=1e-7 A/cm2).")
    P("")
    P("Retarget: F = 40 nm oxide 1T1C tiers (4F2 = 6,400 nm2), pitch 80 nm square (imprint/DUV-pretextured) or 86 nm hexagonal; "
      f"pore {v('pore_frac')} x pitch; {rv('tin_nm_oxide'):.0f} nm TiN electrodes; same EOT.")
    P("")
    P("| pitch (nm) | pore (nm) | mid-plane (nm) | Cs per um (fF) | depth for 5.4 fF (um) | cup AR at that depth | inner hole after top TiN (nm) |")
    P("|---|---|---|---|---|---|---|")
    tn = rv("tin_nm_oxide")
    aao80 = {}
    for pitch in rv("aao_pitch_oxide_nm"):
        pr_ = v("pore_frac") * pitch
        midp = pr_ - 2 * tn - tz
        cpu = cap_cyl_fF(midp, 1.0, v("eot_nm"))
        hneed = v("cs_1b_fF") / cpu
        inner = pr_ - 2 * tn - 2 * tz - 2 * tn
        P(f"| {pitch:.0f} | {pr_:.1f} | {midp:.1f} | {cpu:.2f} | {hneed:.2f} | {hneed*1000/pr_:.0f} | {inner:.1f} |")
        aao80[pitch] = (cpu, hneed, hneed * 1000 / pr_)
    out["aao80"] = aao80
    v_an = 80.0 / v("nm_per_V")
    P(f"Barrier at 80 nm pitch: ~{v_an:.0f} V anodization -> ~{1.1*v_an:.0f} nm barrier (1.0-1.2 nm/V). Wet-only opening would widen the "
      f"pore by ~{2*1.1*v_an:.0f} nm (> pitch), so it needs current-limited voltage ramp-down to ~3-5 nm first, then a short H3PO4 dip "
      "(~8-10 nm widening) [UNVERIFIED-PK]; no fluorocarbon or chlorine plasma. At 35 nm pitch the same trick works, but the fill does not.")
    P("")
    N = rv("die_bits")
    wb = rv("ecc_word_bits")
    words = N / 128
    P("Missing/branched-pore budget on a 16 Gb die with on-die SEC (136-bit words), random defects:")
    P("")
    P("| defect fraction | dead cells/die | words with >=2 dead (need repair) | verdict |")
    P("|---|---|---|---|")
    for pdef in (1e-4, 1e-5, 1e-6, 1e-7):
        dead = pdef * N
        w2 = wb * (wb - 1) / 2 * pdef ** 2 * words
        verdict = ("fails (eats SEC and repair)" if pdef >= 1e-4 else ("marginal" if pdef >= 1e-5 else "OK"))
        P(f"| {pdef:.0e} | {dead:,.0f} | {w2:,.0f} | {verdict} |")
    P(f"Kill line 1e-4 -> **1e-6** (RT-PROC-03). Showing <=1e-6 at 95 % needs >=3e6 pores with zero defects: "
      f"{3e6*(0.080**2):,.0f} um2 = {3e6*(0.080**2)/1e6:.3f} mm2 at 80 nm pitch (automated SEM count).")

    # I7 A1 droop convention (RT-CIRC-03)
    P("")
    P("### I7. Signal and retention on A1's convention (RT-CIRC-lean-array-module-03)")
    P("")
    cbl = v("c_bl_fF")
    vpre = v("v_array") / 2
    P(f"A1: end-of-retention signal {rv('dv_min_mV'):.0f} mV on Cbl {cbl:.1f} fF; allowed droop = VARY - Vpre - dV_min (Cs+Cbl)/Cs.")
    P("")
    P("| capacitor | Cs (fF) | fresh signal (mV) | allowed droop (mV) | retention @13 fA Si tail (ms) | retention / 2x VRT guard vs 64 ms | retention @1 aA oxide tail |")
    P("|---|---|---|---|---|---|---|")
    cases = [("1-beta pillar", v("cs_1b_fF")), ("AAO 35.2 nm, 2.5 um (killed)", cap_cyl_fF(pore - v("liner_nm"), 2.5, v("eot_nm"))),
             ("AAO 35.2 nm, 3.0 um (killed)", cap_cyl_fF(pore - v("liner_nm"), 3.0, v("eot_nm"))),
             ("AAO 80 nm, 1.0 um (oxide access)", aao80[80.0][0] * 1.0)]
    for name, cs in cases:
        fresh = vpre * cs / (cs + cbl) * 1000
        droop = v("v_array") - vpre - rv("dv_min_mV") / 1e3 * (cs + cbl) / cs
        ret_si = cs * 1e-15 * droop / (v("si_tail_fA") * 1e-15) * 1000
        ret_ox = cs * 1e-15 * droop / rv("igzo_tail_A")
        P(f"| {name} | {cs:.2f} | {fresh:.0f} | {droop*1000:.0f} | {ret_si:.0f} | {ret_si/2/64:.2f}x | {ret_ox:,.0f} s |")
    P("Reading: on A1's convention the Si-access AAO cup gives 1.25-1.9x the 1-beta retention before any VRT guard, i.e. no refresh "
      "relief once a 2x guard is held; any refresh relief comes from the oxide access device, not the AAO cup.")

    # I8 fluorocarbon inventory (RT-PROC-02 / RT-CIRC-04)
    P("")
    P("### I8. Fluorocarbon etch-gas inventory per wafer [ESTIMATE] (RT-PROC-02, RT-CIRC-04)")
    P("")
    cap, oth = rv("fc_cap_mold_scc"), rv("fc_other_scc")
    base = cap + oth
    rows = [("1-beta DDR5 (baseline)", base),
            ("MARGIN STACK-class planar oxide 4F2 + 120 nm stub (LEAN)", oth + rv("fc_margin_add_scc")),
            ("F40 oxide 1T1C + AAO cup at 80 nm (LEAN)", oth + rv("fc_margin_add_scc") - 40.0),
            ("3D oxide cell (AND-STACK class), no capacitor mold", oth + rv("fc_3d_add_scc")),
            ("3D oxide cell + cryo HF/PF3 deep etch (industry lever, not LEAN's)", oth + rv("fc_3d_add_scc") * (1 - rv("cryo_hf_fc_cut")))]
    P("| flow | FC scc/wafer | vs 1-beta |")
    P("|---|---|---|")
    fc = {}
    for name, val in rows:
        P(f"| {name} | {val:,.0f} | {100*(val/base-1):+.0f} % |")
        fc[name] = val / base - 1
    P(f"Reading: the capacitor mold is ~{100*cap/base:.0f} % of a 1-beta wafer's fluorocarbon etch gas; LEAN deletes it only where the "
      "cell has no other deep etch. PFAS-class etch is cut ~25-30 %, not removed; 3D cells add deep FC etches unless cryo HF/PF3 is adopted.")
    out["fc"] = fc
    out["fc_cap_share"] = cap / base

    # I9 gallium (RT-DEV-05)
    P("")
    P("### I9. Gallium in an oxide-cell fab (RT-DEV-lean-array-module-05)")
    P("")
    vol = rv("igzo_nm") * 1e-7 * v("wafer_area_m2") * 1e4 * rv("igzo_area_factor")
    ga_g = vol * rv("igzo_density") * rv("ga_mass_frac") / rv("igzo_util")
    ga_yr = ga_g * rv("igzo_tiers") * v("line_wafers_per_yr") / 1000.0
    P(f"Ga per tier-wafer: {rv('igzo_nm'):.0f} nm x {v('wafer_area_m2')*1e4:.0f} cm2 x {rv('igzo_area_factor'):.0f} x {rv('igzo_density')} g/cm3 x "
      f"{rv('ga_mass_frac'):.3f} / {rv('igzo_util')} = {ga_g*1000:.0f} mg; x {rv('igzo_tiers')} tiers x {v('line_wafers_per_yr')/1e6:.1f}M wafers = "
      f"**{ga_yr:.0f} kg/yr** per 100k-wpm fab. A 10-year stockpile costs ~${10*ga_yr*rv('ga_price_per_kg')/1e6:.1f}M "
      f"(${rv('ga_price_per_kg'):.0f}/kg), {10*ga_yr*rv('ga_price_per_kg')/E['day_rev']*24:.1f} hours of fab revenue. Gallium exposure is a "
      "stockpile item, not a reason to accept ZTO's leakage risk.")
    out["ga_kg_yr"] = ga_yr
    return out


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
    I = section_I(He, H2, B, D, E)

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
      f"({E['usd_gb']*1e6:.0f} u$/GB vs $1.48/GB). Retrofit pays back after ~{E['payback_days_rt']:.1f} days of avoided stoppage "
      f"(brownfield incl. requalification; {I['payback_gf']:.1f} days greenfield; old hardware-only {E['payback_days']:.1f}). Hedge, not cost lever.")
    P(f"- AAO at the 1-beta pitch, 2.5-3 um: {Fz[(round(math.sqrt(2*v('cell_1b_nm2')/math.sqrt(3)),1),2.5)]:.1f}-"
      f"{Fz[(round(math.sqrt(2*v('cell_1b_nm2')/math.sqrt(3)),1),3.0)]:.1f} fF vs 5.4 fF only with an unshown ~5.6 nm-core, AR ~450 fill: "
      f"leg KILLED (RT-CIRC-02). Retarget: 80 nm pitch gives {I['aao80'][80.0][0]:.1f} fF/um, 5.4 fF at {I['aao80'][80.0][1]:.2f} um (cup AR {I['aao80'][80.0][2]:.0f}).")
    P(f"- RED-TEAM: effective a_H2 prior {I['a_eff_med']:.2f} (was 0.27 translational); P(GO) {100*I['pgo_old']:.0f} % -> {100*I['pgo_new']:.0f} % "
      f"before the adsorbate tail; carry P3. Cryo GO line {I['a_go_cryo']:.3f}. Edge-He guard keeps {100*I['guard_retained']:.0f} % He in HAR chambers.")
    P(f"- RED-TEAM: H2 can replace 100 % of backside He in a Si-access line, ~{100*I['ox_share_mid']:.0f} % in an oxide-cell line (oxide-exposed "
      f"steps keep He/Ar). Capacitor mold = ~{100*I['fc_cap_share']:.0f} % of FC etch gas: LEAN cuts PFAS-class etch ~25-30 % in planar oxide "
      f"cells, not to zero. Ga ~{I['ga_kg_yr']:.0f} kg/yr per fab: stockpile, not ZTO.")
    P(f"- EUV-free IL: ~10 nm overlay only (F~40 nm oxide cells, {G:.3f} Gb/mm2 per tier -> >=5 tiers for 1-beta parity).")

    hr("GO / NO-GO")
    P(f"**GO** if the Step-1 rig measures an effective H2 accommodation **a_H2 >= {B['a_go']:.2f}** (symmetric equivalent; wafer-side SiN/SiO2/poly "
      f"films against an Al2O3/AlN chuck counterface, 20-60 C, including fluorocarbon-polymer-contaminated backsides). H2 then matches He wafer "
      f"cooling at <= {p_go:.1f} Torr. **NO-GO** if a_H2 < {B['a_max']:.2f}: parity would need > {v('p_max_Torr'):.0f} Torr, past the clamp limit "
      f"(fallbacks: He recapture, H2/He blend, or a chuck coating that raises a_H2). Step 2 (300 mm chamber) must then show wafer temperature "
      f"within +/-{v('dT_window_K'):.0f} K of He across the wafer, HAR oxide etch-rate drift <= 2 % and mask-selectivity drift <= 5 % at 2x the predicted "
      f"{D['leak']:.1f} sccm leak, and foreline H2 <= 10 % LFL in single fault.")
    P("")
    P(f"**RED-TEAM ADDITIONS (revised after red team).** The GO must hold on plasma-pretreated coupons (Ar, O2, C4F8-polymer, H2 plasma; "
      f"RT-DEV-04) and at -70 to 0 C (cryo GO line {I['a_go_cryo']:.3f}; RT-PROC-04); H2 vs D2 separates the rotational term (RT-DEV-01). "
      "Step 1b thermocouple-wafer a_H2 must agree with the rig within +/-0.03. Step 2 adds edge-zone metrics at r = 140-148 mm on AR >=40 "
      "wafers at 2x leak: hole tilt <=0.1 deg, bottom CD within 1 nm, bow in spec (RT-PROC-01), with the edge-He guard zone as the fallback. "
      "IGZO/ZTO TFT monitor wafers through every H2-cooled chamber type at 2x leak: delta Vt <=5 mV, no Ioff tail shift at 85 C "
      "(RT-DEV-02, RT-CIRC-01); a failing chamber class keeps He/Ar.")

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
