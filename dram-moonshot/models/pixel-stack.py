#!/usr/bin/env python3
"""
pixel-stack.py -- first-principles model of PIXEL-STACK (dram-moonshot Stage 3, rank 5).

Concept: 3D 1T1C DRAM built as groups of G (=16) oxide-channel cell tiers. Each group is capped by an
all-oxide "amp tier" that reads every vertical bitline the way a CMOS image sensor reads a pixel:
the vertical bitline (+ a shared floating node) is the floating diffusion, an oxide source follower (SF)
drives a column line through a select (SEL) transistor, a reset (RST) transistor precharges it, and a
correlated-double-sampling (CDS) column subtracts reset and signal samples. CDS cancels the SF offset
(oxide-TFT Vt sigma) and the reset kTC, so no Smart-Cut c-Si layer is needed per group, and the short
(16-cell) bitline lets the in-tier capacitor shrink to tens of nm.

Owner: dos-pixel-stack. Written 2026-11-02. Pure standard library. Run from dram-moonshot/:
    python3 models/pixel-stack.py
It prints a markdown report and writes it to research/stage3/pixel-stack_model_output.md.

What it computes (all with explicit arithmetic):
  1. Geometry: per-tier cell footprint vs lateral capacitor length; capacitor C from geometry and EOT.
  2. Bitline: vertical-bitline capacitance vs tiers per group; charge-sharing signal (mV, electrons).
  3. Read chain: SF thermal noise, SF 1/f noise filtered by the CDS transfer function (numerical
     integral of a Hooge-model PSD), RTN tail, uncancelled kTC terms, column offset, WL kickback,
     data-dependent bitline coupling (with/without decision-feedback compensation).
  4. Margin: required signal at raw BER 1e-4 (3.72 sigma, the RAW-BER CONTRACT target), minimum Cs,
     resulting capacitor length, and the allowed "readout residual" -- the decisive experiment's number.
  5. Retention: leakage tail (oxide TFT Ioff with Vt tail and hydrogen shift + capacitor dielectric).
  6. Density (Gb/mm2) and 1-beta break-even tiers; amp-tier area fit vs sharing factor.
  7. Wafer cost and $/GB vs 1-beta DDR5 ($1.48/GB), vs the Smart-Cut (N-48 / I-11545) variant.
  8. Energy per access and refresh; timing (tRC) vs sharing; endurance/drift budget.
  9. Sensitivity tables on the key unknowns and the GO/NO-GO threshold.
"""

import math
import os

KB = 1.380649e-23   # J/K
Q = 1.602176634e-19  # C
EPS0 = 8.8541878128e-12  # F/m

# ------------------------------------------------------------------------------------------------
# INPUTS -- (value, basis). Every value carries a source URL or "ESTIMATE: basis".
# ------------------------------------------------------------------------------------------------
INPUTS = {
    # --- reference DRAM (1-beta DDR5) ---
    "d_1b_gb_mm2": (0.447, "A1_scaling_limits.md sec.1 table: Micron D1b 16Gb DDR5 35.83 mm2 (TechInsights teardown via ram-venture cost_stack sec.3.1) -> 0.447 Gb/mm2"),
    "wafer_1b_usd": (3800.0, "ram-venture models/dram_cost_stack.py canonical 1b wafer (A1_scaling_limits.md line 8)"),
    "cost_1b_usd_per_gb": (1.48, "ram-venture models/dram_cost_stack.py ($1.48/GB DDR5 1b), A1_scaling_limits.md"),
    "ddr5_refresh_s_hot": (0.032, "JEDEC DDR5 32 ms above 85 C (A1 / dram_cell_physics.py INPUTS t_ref)"),
    "ddr5_e_refresh_fJ_bit": (46.0, "models/dram_cell_physics.py sec.5 output: 46 fJ per refreshed bit incl. 2x periphery"),
    # --- operating point ---
    "T_K": (358.15, "85 C worst-case junction temperature (JEDEC normal/extended boundary)"),
    "v_half": (0.5, "ESTIMATE: VARY 1.0 V with VARY/2 precharge, as in dram_cell_physics.py (1.05 V)"),
    "droop_budget_V": (0.075, "ESTIMATE: 15% of the 0.5 V half-swing lost to leakage by end of refresh (concept's 0.85 factor)"),
    "t_ret_target_s": (1.0, "ESTIMATE: concept target >=1 s at 85 C (A1 white space: worst-cell >=1 s at 85 C)"),
    "k_sigma": (3.72, "raw BER 1e-4 one-sided Gaussian (RAW-BER CONTRACT / I-11559 t=8 BCH target)"),
    # --- geometry of a lateral 1T1C cell in a tier ---
    "tiers_per_group": (16, "concept: amp tier every 16 cell tiers (I-11545 / N-48 group size)"),
    "cell_tiers_total": (64, "concept: 64 cell tiers = 4 groups + 4 amp tiers"),
    "y_pitch_nm": (70.0, "ESTIMATE: WL-direction pitch = vertical-BL pitch; 30 nm IGZO ribbon + GAA gate + space (Kioxia 3D OCTRAM / OCTRAM 54-63 nm pitches, A3 sec.2.2)"),
    "bl_half_nm": (20.0, "ESTIMATE: half of a 40 nm vertical BL pillar shared by mirrored cells"),
    "tft_len_nm": (70.0, "ESTIMATE: lateral GAA IGZO access TFT Lg 40-50 nm + S/D extensions (Kioxia 3D OCTRAM horizontal IGZO, IEDM 2025)"),
    "plate_half_nm": (15.0, "ESTIMATE: half of shared plate electrode + isolation"),
    "sn_perimeter_nm": (110.0, "ESTIMATE: storage-node cross-section ~30x25 nm inside a 60 nm tier after dielectric + plate liners"),
    "sn_end_nm2": (750.0, "ESTIMATE: end-cap area of the storage node (30x25 nm)"),
    "eot_nm": (0.50, "ESTIMATE: ZrO2-based stack; 1b uses ~0.55 nm (A1 INPUTS eot_nm); concept assumed 0.45 nm"),
    "array_eff": (0.55, "A1 sec.6 base-case 3D array efficiency (staircase + periphery), models/dram_cell_physics.py section_3d"),
    "ecc_factor": (592.0 / 512.0, "RAW-BER CONTRACT: t=8 BCH, 80 check bits per 512 data bits (I-11559)"),
    # --- bitline electrical ---
    "c_bl_per_tier_fF": (0.15, "ESTIMATE: 2 mirrored cells per tier (drain overlap ~0.03 fF each) + pillar-to-WL/neighbour coupling; 16 tiers -> 2.4 fF (concept: ~3 fF on 16 cells)"),
    "c_bl_fixed_fF": (0.6, "ESTIMATE: RST/TG junctions, SF gate, local via in the amp tier"),
    "c_fd_base_fF": (0.25, "ESTIMATE: shared floating node: SF gate 0.1 + RST junction 0.05 + wire 0.1 fF"),
    "c_fd_per_share_fF": (0.05, "ESTIMATE: each transfer-gate (TG) junction added to the shared node"),
    # --- source follower and read chain ---
    "sf_W_nm": (100.0, "ESTIMATE: amp-tier SF width (design point)"),
    "sf_L_nm": (100.0, "ESTIMATE: amp-tier SF length (design point; longer L lowers 1/f)"),
    "sf_eot_nm": (3.0, "ESTIMATE: ALD HfO2/Al2O3 TFT gate dielectric EOT ~3 nm"),
    "sf_vov_V": (0.4, "ESTIMATE: SF overdrive"),
    "sf_id_A": (2.0e-6, "ESTIMATE: 2 uA = 20 uA/um at W=0.1 um, below CXMT IGZO 60.9 uA/um (A3 sec.1, IEDM 2025)"),
    "sf_gain": (0.90, "ESTIMATE: oxide TFT SF without body effect, finite gds/load"),
    "sf_gain_sigma": (0.02, "ESTIMATE: 2% SF gain sigma (gain is NOT cancelled by CDS)"),
    "gamma_th": (1.0, "ESTIMATE: thermal-noise factor for short-channel TFT (2/3 long-channel)"),
    "alpha_H": (1.5e-3, "https://web.eecs.umich.edu/omelab/downloads/Fung JAP 2010.pdf (a-IGZO TFT Hooge ~1.5e-3, long channel; via search snippet). Cho EDL 2009 reports ~6e-3 (Al2O3/SiNx) and 100-1000x higher normalized noise for Al2O3-only"),
    "c_col_fF": (15.0, "ESTIMATE: local column line shared by 16-32 SELs plus wire"),
    "t_cds_gap_ns": (15.0, "ESTIMATE: time between reset and signal samples (WL rise + charge share + settle)"),
    "col_offset_mV": (1.0, "ESTIMATE: auto-zeroed comparator in the 28/22 nm or sky130 CDS column (MARGIN STACK MPW)"),
    "rtn_mult": (3.0, "ESTIMATE: 1e-4-tail RTN amplitude as a multiple of q/(Cox*W*L) (Si RTN amplitude distributions are exponential with mean ~1-2x q/CoxWL)"),
    "wl_overlap_fF": (0.010, "ESTIMATE: selected access-TFT gate-to-BL overlap"),
    "v_wl_swing": (3.0, "ESTIMATE: WL from -0.7 V hold to +2.3 V (negative hold voltage as in imec 2T0C, A3 sec.2.1)"),
    "kick_var": (0.10, "ESTIMATE: 10% sigma of WL kickback after dummy-WL / reference cancellation"),
    "cc_ratio": (0.08, "ESTIMATE: neighbour-BL coupling per aggressor / C_BL with a BL shield (Samsung VS-DRAM uses a BL shield, A1 sec.6)"),
    "n_aggr": (2, "ESTIMATE: two simultaneously activated neighbours on the same WL"),
    "dfb_residual": (0.15, "ESTIMATE: fraction of coupling left after decision-feedback threshold shift using neighbours' decided bits"),
    "cs_sigma_frac": (0.06, "ESTIMATE: 6% Cs sigma from lateral-recess length variation (Lam: recess varies along stack, A1 sec.6)"),
    "cbl_sigma_frac": (0.03, "ESTIMATE: 3% bitline-capacitance sigma"),
    "guard_mV": (8.0, "ESTIMATE: unmodelled terms (reference error, WL-WL disturb, temperature drift between samples)"),
    # --- retention ---
    "ioff_med_85C_A": (1.0e-18, "https://www.kioxia.com/en-jp/about/news/2025/20251212-1.html (3D OCTRAM horizontal IGZO Ioff <1 aA; temperature not stated -> used as 85 C median, ESTIMATE)"),
    "vt_sigma_mV": (30.0, "ESTIMATE: IGZO TFT Vt sigma 30 mV for ~40 nm devices (stage-2 critiques quote 30-100 mV)"),
    "ss_mV_dec_85C": (80.0, "CXMT BEOL IGZO select device SS 80 mV/dec (A3 sec.1, IEDM 2025 via snippet)"),
    "h_vt_shift_mV": (0.0, "ESTIMATE: hydrogen-induced negative Vt shift after the 400 C stack (decisive-experiment target <20 mV)"),
    "j_cap_A_cm2": (1.0e-7, "ESTIMATE: ZrO2 MIM leakage at 0.5 V; A1 bottleneck #1 target <=1e-7 A/cm2 at 0.8 V"),
    "leak_tail_sigma": (3.72, "ESTIMATE: retention failures share the 1e-4 raw-BER budget"),
    # --- cost ---
    "base_wafer_usd": (3000.0, "A1 sec.6 base-case 3D base wafer (logic periphery), models/dram_cell_physics.py section_3d"),
    "usd_per_cell_tier": (25.0, "ESTIMATE: between A1 optimistic $20 and base $30 per tier; short lateral recess"),
    "usd_per_deck": (250.0, "ESTIMATE: per 16-tier group BL-hole HAR etch, recess, ALD fills, staircase"),
    "usd_per_amp_sublayer": (300.0, "ESTIMATE: 4 DUV masks x ~$60 + ALD oxide/anneal ~$60 (concept: 3-5 oxide masks)"),
    "usd_smartcut_layer": (2000.0, "ESTIMATE: mid of critics' $0.75-4k per Smart-Cut c-Si layer (I-11545 stage-2 critiques)"),
    "tier_yield": (0.998, "A1 sec.6: per-tier killer-defect <=0.2% after repair needed for 64 tiers"),
    "amp_tier_yield": (0.995, "ESTIMATE: amp tier, repaired by spare columns"),
    # --- amp-tier area ---
    "tft_W_min_nm": (50.0, "ESTIMATE: minimum RST/SEL/TG width"),
    "tft_L_min_nm": (40.0, "ESTIMATE: minimum RST/SEL/TG length"),
    "tft_ovh_W_nm": (40.0, "ESTIMATE: isolation added to TFT width"),
    "tft_ovh_L_nm": (80.0, "ESTIMATE: S/D contacts added to TFT length"),
    "share": (2, "ESTIMATE: CIS-style sharing; 2 vertical BLs share one SF/RST/SEL via per-BL transfer gates (see sharing table)"),
    # --- timing / energy ---
    "t_restore_ns": (8.0, "ESTIMATE: BL restore through TG+RST (2 series TFTs, ~500 kOhm x 3.5 fF, 5 tau)"),
    "t_wl_ns": (5.0, "ESTIMATE: WL rise + charge share in a 16-tier group"),
    "c_wl_per_cell_fF": (0.15, "models/dram_cell_physics.py INPUTS c_wl_per_cell_fF"),
    "pump_eff": (0.45, "models/dram_cell_physics.py INPUTS pump_eff"),
    "bits_per_row": (4096, "ESTIMATE: vertical BLs per activated WL"),
    "bank_bits": (1.0e9, "ESTIMATE: 1 Gb per bank"),
    "periph_mult": (2.0, "models/dram_cell_physics.py INPUTS periph_overhead"),
    # --- endurance / drift ---
    "v_amp": (1.2, "ESTIMATE: amp-tier supply; a depletion-mode (In-rich) oxide SF keeps the column output above ground with the BL at VARY/2"),
    "ddr_trc_ns": (46.0, "ESTIMATE: DDR5 tRC ~46 ns class (JEDEC speed bins, training knowledge [UNVERIFIED])"),
    "endurance_demo": (1.0e12, "https://imec-publications.be/entities/publication/948b2190-065d-48d2-a9b9-4f4ecd22c234 (imec IGZO 2T0C >1e12 cycles at 95 C, EDL 2025; A3 sec.2.1)"),
    "sf_headroom_mV": (150.0, "ESTIMATE: SF Vt drift CDS tolerates before column range clips (Vdd 1.8 V amp supply)"),
}


def P(key):
    return INPUTS[key][0]


OUT = []


def emit(s=""):
    OUT.append(s)
    print(s)


# ------------------------------------------------------------------------------------------------
# 1. Geometry
# ------------------------------------------------------------------------------------------------
def cox_F_m2(eot_nm):
    return 3.9 * EPS0 / (eot_nm * 1e-9)


def cap_fF(l_cap_nm, eot_nm=None):
    eot = P("eot_nm") if eot_nm is None else eot_nm
    area_nm2 = P("sn_perimeter_nm") * l_cap_nm + P("sn_end_nm2")
    return cox_F_m2(eot) * area_nm2 * 1e-18 * 1e15


def l_cap_for(cs_fF, eot_nm=None):
    eot = P("eot_nm") if eot_nm is None else eot_nm
    area_nm2 = cs_fF * 1e-15 / cox_F_m2(eot) / 1e-18
    return max((area_nm2 - P("sn_end_nm2")) / P("sn_perimeter_nm"), 0.0)


def x_cell_nm(l_cap_nm):
    return P("bl_half_nm") + P("tft_len_nm") + l_cap_nm + P("plate_half_nm")


def cell_um2(l_cap_nm):
    return P("y_pitch_nm") * x_cell_nm(l_cap_nm) * 1e-6


def gb_per_mm2_tier(cell):
    return 1e6 / cell * P("array_eff") / P("ecc_factor") / 1e9


# ------------------------------------------------------------------------------------------------
# 2. Bitline and signal
# ------------------------------------------------------------------------------------------------
def c_bl_fF(g=None):
    g = P("tiers_per_group") if g is None else g
    return g * P("c_bl_per_tier_fF") + P("c_bl_fixed_fF")


def c_fd_fF(share=None):
    s = P("share") if share is None else share
    return P("c_fd_base_fF") + P("c_fd_per_share_fF") * s if s > 1 else 0.0


def signal_mV(cs, cbl, cfd=None):
    """End-of-retention signal on the floating node (BL + shared FD after transfer)."""
    cfd = c_fd_fF() if cfd is None else cfd
    v = P("v_half") - P("droop_budget_V")
    s_bl = v * cs / (cs + cbl)
    return s_bl * (cbl + cs) / (cbl + cs + cfd) * 1e3


# ------------------------------------------------------------------------------------------------
# 3. Read chain noise
# ------------------------------------------------------------------------------------------------
_CDS_CACHE = {}


def cds_flicker_factor(dt_s, fc_hz):
    """F = integral over f of 4 sin^2(pi f dt) / (1 + (f/fc)^2) df/f  (log-spaced midpoint rule).
    Integrated 1/f noise after CDS = K * F for S_v(f) = K/f."""
    key = (round(dt_s * 1e12), round(fc_hz))
    if key in _CDS_CACHE:
        return _CDS_CACHE[key]
    u0, u1 = math.log(1e-3), math.log(fc_hz * 300.0)
    n = 120000
    du = (u1 - u0) / n
    tot = 0.0
    for i in range(n):
        f = math.exp(u0 + (i + 0.5) * du)
        tot += 4.0 * math.sin(math.pi * f * dt_s) ** 2 / (1.0 + (f / fc_hz) ** 2) * du
    _CDS_CACHE[key] = tot
    return tot


def sf_gm():
    return 2.0 * P("sf_id_A") / P("sf_vov_V")


def fc_hz():
    return sf_gm() / (2 * math.pi * P("c_col_fF") * 1e-15)


def noise_terms(alpha_h=None, w_nm=None, l_nm=None, share=None, cs=None, cbl=None, dfb=True,
                cc_ratio=None):
    """Return dict of input-referred noise terms (mV): random sigmas and deterministic worst cases."""
    a = P("alpha_H") if alpha_h is None else alpha_h
    w = (P("sf_W_nm") if w_nm is None else w_nm) * 1e-9
    l = (P("sf_L_nm") if l_nm is None else l_nm) * 1e-9
    s = P("share") if share is None else share
    cs = 0.45 if cs is None else cs
    cbl = c_bl_fF() if cbl is None else cbl
    ccr = P("cc_ratio") if cc_ratio is None else cc_ratio
    T = P("T_K")
    g = P("sf_gain")
    cox = cox_F_m2(P("sf_eot_nm"))
    out = {}
    # SF thermal: output kT/C_col per sample (gamma), two samples, referred to input
    out["sf_thermal"] = math.sqrt(2 * P("gamma_th") * KB * T / (P("c_col_fF") * 1e-15)) / g * 1e3
    # SF 1/f, Hooge: S_vg = alpha q Vov / (4 Cox W L f) * 1.5 (N_sat = 2/3 Cox W L Vov / q)
    K = a * Q * P("sf_vov_V") / (4 * cox * w * l) * 1.5
    F = cds_flicker_factor(P("t_cds_gap_ns") * 1e-9, fc_hz())
    out["sf_flicker"] = math.sqrt(K * F) * 1e3
    # cell write kTC on Cs, transferred by charge sharing (not cancelled)
    out["cell_kTC"] = math.sqrt(KB * T / (cs * 1e-15)) * cs / (cs + cbl) * 1e3
    # BL reset kTC: cancelled for the BL whose reset is sampled; uncancelled for shared BLs
    out["bl_kTC_uncancelled"] = (math.sqrt(KB * T / ((cbl + cs) * 1e-15)) * 1e3) if s > 1 else 0.0
    out["column_offset"] = P("col_offset_mV") / g
    kick = P("wl_overlap_fF") * P("v_wl_swing") / (cbl + cs) * 1e3
    out["wl_kick_var"] = kick * P("kick_var")
    out["_wl_kick_mean"] = kick
    # RTN tail (non-Gaussian): q/(Cox W L) x multiplier
    out["rtn_tail_det"] = Q / (cox * w * l) * P("rtn_mult") * 1e3
    # data-dependent neighbour coupling (deterministic worst case), with optional decision feedback
    sig = signal_mV(cs, cbl)
    cpl = P("n_aggr") * ccr * sig
    out["_coupling_raw"] = cpl
    out["coupling_det"] = cpl * (P("dfb_residual") if dfb else 1.0)
    return out


def readout_sigma(nt):
    keys = ["sf_thermal", "sf_flicker", "cell_kTC", "bl_kTC_uncancelled", "column_offset", "wl_kick_var"]
    return math.sqrt(sum(nt[k] ** 2 for k in keys))


def readout_residual(nt):
    """The decisive experiment's number: k*sigma_random(readout) + RTN tail + data-dependent coupling."""
    return P("k_sigma") * readout_sigma(nt) + nt["rtn_tail_det"] + nt["coupling_det"]


def margin_mV(cs, cbl=None, nt=None, residual_override=None, cs_sigma=None):
    """Signal minus everything at k sigma. >0 means the 1e-4 raw-BER read passes."""
    cbl = c_bl_fF() if cbl is None else cbl
    sig = signal_mV(cs, cbl)
    csf = P("cs_sigma_frac") if cs_sigma is None else cs_sigma
    frac = math.sqrt(csf ** 2 + P("sf_gain_sigma") ** 2 + (P("cbl_sigma_frac") * cbl / (cs + cbl)) ** 2)
    sig_var = sig * frac  # signal-proportional sigma
    if residual_override is None:
        nt = noise_terms(cs=cs, cbl=cbl) if nt is None else nt
        sr = readout_sigma(nt)
        det = nt["rtn_tail_det"] + nt["coupling_det"]
        tot = P("k_sigma") * math.sqrt(sr ** 2 + sig_var ** 2) + det + P("guard_mV")
    else:
        # residual_override = measured readout residual (already at k sigma, linear-added: conservative)
        tot = residual_override + P("k_sigma") * sig_var + P("guard_mV")
    return sig - tot


def cs_min_fF(cbl=None, residual_override=None, cs_sigma=None):
    lo, hi = 0.02, 20.0
    if margin_mV(hi, cbl, residual_override=residual_override, cs_sigma=cs_sigma) <= 0:
        return float("inf")
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if margin_mV(mid, cbl, residual_override=residual_override, cs_sigma=cs_sigma) > 0:
            hi = mid
        else:
            lo = mid
    return hi


def residual_allowed(cs, cbl=None):
    """Largest readout residual (mV, at k sigma) that still passes at this Cs."""
    lo, hi = 0.0, 200.0
    if margin_mV(cs, cbl, residual_override=0.0) <= 0:
        return 0.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if margin_mV(cs, cbl, residual_override=mid) > 0:
            lo = mid
        else:
            hi = mid
    return lo


# ------------------------------------------------------------------------------------------------
# 5. Retention
# ------------------------------------------------------------------------------------------------
def leak_tail_A(l_cap_nm, h_shift_mV=None, vt_sigma=None, j_cap=None):
    h = P("h_vt_shift_mV") if h_shift_mV is None else h_shift_mV
    vs = P("vt_sigma_mV") if vt_sigma is None else vt_sigma
    j = P("j_cap_A_cm2") if j_cap is None else j_cap
    i_tft = P("ioff_med_85C_A") * 10 ** ((P("leak_tail_sigma") * vs + h) / P("ss_mV_dec_85C"))
    area_cm2 = (P("sn_perimeter_nm") * l_cap_nm + P("sn_end_nm2")) * 1e-14
    i_cap = j * area_cm2
    return i_tft + i_cap, i_tft, i_cap


def retention_s(cs, i_leak):
    return cs * 1e-15 * P("droop_budget_V") / i_leak


# ------------------------------------------------------------------------------------------------
# 6/7. Density, area, cost
# ------------------------------------------------------------------------------------------------
def tft_area_um2(w, l):
    return (w + P("tft_ovh_W_nm")) * (l + P("tft_ovh_L_nm")) * 1e-6


def amp_area_check(l_cap_nm, share=None, w=None, l=None):
    s = P("share") if share is None else share
    w = P("sf_W_nm") if w is None else w
    l = P("sf_L_nm") if l is None else l
    avail = P("y_pitch_nm") * 2 * x_cell_nm(l_cap_nm) * 1e-6  # per vertical BL (mirrored cells)
    a_min = tft_area_um2(P("tft_W_min_nm"), P("tft_L_min_nm"))
    group = tft_area_um2(w, l) + 2 * a_min  # SF + RST + SEL
    need = group / s + (a_min if s > 1 else 0.0)
    return avail, need, math.ceil(need / avail - 1e-9)


def wafer_cost(n_tiers, g, sublayers, smartcut=False):
    groups = math.ceil(n_tiers / g)
    c = P("base_wafer_usd") + n_tiers * P("usd_per_cell_tier") + groups * P("usd_per_deck")
    if smartcut:
        c += groups * P("usd_smartcut_layer")
    else:
        c += groups * sublayers * P("usd_per_amp_sublayer")
    return c, groups


def rel_cost_per_bit(wafer_usd, dens, yld):
    ref = P("wafer_1b_usd") / P("d_1b_gb_mm2")
    return (wafer_usd / dens / yld) / ref


def stack_yield(n_tiers, groups):
    return P("tier_yield") ** n_tiers * P("amp_tier_yield") ** groups


# ------------------------------------------------------------------------------------------------
# 8. Energy and timing
# ------------------------------------------------------------------------------------------------
def t_read_ns(share=None):
    s = P("share") if share is None else share
    tau = P("c_col_fF") * 1e-15 / sf_gm()
    t_settle = math.log(100) * tau * 1e9
    first = t_settle + P("t_wl_ns") + t_settle + 2.0  # reset sample, WL+share, signal sample, reset 2 ns
    per = (2.0 + t_settle) * 2 if s > 1 else 0.0       # FD reset+sample, TG+sample
    t_first_bit = first
    trc = first + P("t_restore_ns") + (s - 1) * (per + P("t_restore_ns"))
    return t_first_bit, trc, t_settle


def energy_access_fJ(cs, cbl, trc_ns):
    v = 2 * P("v_half")
    e_bl = (cbl + cs) * v * P("v_half")              # restore swing from VARY/2 to rail
    e_col = P("c_col_fF") * P("v_amp") * 0.1         # SF column swing ~0.1 V per bit read
    t_on = (2 * t_read_ns(1)[2] + 2.0) * 1e-9          # pulsed column bias: on for two samples per bit
    e_sf = P("sf_id_A") * P("v_amp") * t_on * 1e15
    e_wl = P("c_wl_per_cell_fF") * P("v_wl_swing") ** 2 / P("pump_eff")
    core = e_bl + e_col + e_sf + e_wl
    return core * P("periph_mult"), dict(bl=e_bl, col=e_col, sf=e_sf, wl=e_wl)


# ------------------------------------------------------------------------------------------------
# Report
# ------------------------------------------------------------------------------------------------
def table(headers, rows):
    emit("| " + " | ".join(headers) + " |")
    emit("|" + "|".join("---" for _ in headers) + "|")
    for r in rows:
        emit("| " + " | ".join(str(x) for x in r) + " |")
    emit()


def main():
    emit("# PIXEL-STACK model output")
    emit()
    emit("Generated by `models/pixel-stack.py` (dos-pixel-stack, 2026-11-02). Pure stdlib; all numbers below are "
         "computed from the INPUTS block in the script, where each value carries a source URL or an "
         "`ESTIMATE: basis`. [ESTIMATE] unless a source is named.")
    emit()

    # ---------------- 1-2. design point ----------------
    g = P("tiers_per_group")
    cbl = c_bl_fF()
    cfd = c_fd_fF()
    cs0 = 0.45
    lcap0 = l_cap_for(cs0)
    cell0 = cell_um2(lcap0)
    sig0 = signal_mV(cs0, cbl)
    e_store = cs0 * 1e-15 * P("v_half") / Q
    emit("## 1. Design point (concept: Cs 0.45 fF on a 16-cell vertical bitline)")
    emit()
    table(["Quantity", "Value", "Basis"], [
        ["Capacitor dielectric", f"EOT {P('eot_nm'):.2f} nm -> {cox_F_m2(P('eot_nm'))*1e3:.1f} fF/um2", "eot_nm"],
        ["Lateral capacitor length for 0.45 fF", f"{lcap0:.0f} nm (A1 base case: ~500-600 nm)", "perimeter x length + end cap"],
        ["Per-tier cell footprint", f"{P('y_pitch_nm'):.0f} x {x_cell_nm(lcap0):.0f} nm = {cell0:.4f} um2 (A1 base 0.030, optimistic 0.012)", "y pitch x (BL/2 + TFT + cap + plate/2)"],
        ["Vertical bitline C (16 tiers)", f"{cbl:.2f} fF", "16 x c_bl_per_tier + fixed"],
        ["Shared floating node (share = %d)" % P("share"), f"{cfd:.2f} fF", "SF gate + RST + TG junctions"],
        ["Stored charge at 0.5 V", f"{e_store:,.0f} electrons", "Cs x VARY/2 / q"],
        ["End-of-retention signal", f"{sig0:.1f} mV (concept: 55 mV)", "(0.5 - 0.075) V x Cs/(Cs+Cbl) x Cbl/(Cbl+Cfd)"],
        ["Conversion gain on node", f"{Q/((cbl+cs0+cfd)*1e-15)*1e6:.0f} uV/e-", "q / C_node"],
        ["Signal in node electrons", f"{sig0*1e-3*(cbl+cs0+cfd)*1e-15/Q:,.0f} e-", "signal x C_node / q"],
    ])

    # ---------------- 3. noise budget ----------------
    nt = noise_terms(cs=cs0, cbl=cbl)
    nt_nodfb = noise_terms(cs=cs0, cbl=cbl, dfb=False)
    sr = readout_sigma(nt)
    res = readout_residual(nt)
    res_nodfb = readout_residual(nt_nodfb)
    emit("## 2. Read-chain noise after CDS (input-referred, 85 C)")
    emit()
    emit(f"SF: W/L = {P('sf_W_nm'):.0f}/{P('sf_L_nm'):.0f} nm, EOT {P('sf_eot_nm')} nm, Id {P('sf_id_A')*1e6:.1f} uA, "
         f"gm {sf_gm()*1e6:.1f} uS, column {P('c_col_fF'):.0f} fF -> fc {fc_hz()/1e6:.0f} MHz; CDS gap {P('t_cds_gap_ns'):.0f} ns; "
         f"Hooge alpha {P('alpha_H'):.1e}. CDS 1/f factor F = {cds_flicker_factor(P('t_cds_gap_ns')*1e-9, fc_hz()):.2f} "
         "(integral of 4 sin^2(pi f dt)/(1+(f/fc)^2) df/f).")
    emit()
    rows = []
    for k, lab in [("sf_thermal", "SF thermal (kT/C_col, 2 samples)"), ("sf_flicker", "SF 1/f after CDS (Hooge)"),
                   ("cell_kTC", "Cell write kTC (not cancelled)"), ("bl_kTC_uncancelled", "BL reset kTC, shared BLs (not cancelled)"),
                   ("column_offset", "Column comparator offset after auto-zero"), ("wl_kick_var", "WL kickback variation (mean cancelled)")]:
        rows.append([lab, f"{nt[k]:.2f} mV rms", "random"])
    rows.append(["**Random readout sigma**", f"**{sr:.2f} mV**", f"x {P('k_sigma')} = {P('k_sigma')*sr:.1f} mV"])
    rows.append(["RTN tail at 1e-4 (q/CoxWL x %.0f)" % P("rtn_mult"), f"{nt['rtn_tail_det']:.2f} mV", "deterministic add"])
    rows.append(["Neighbour-BL coupling, raw worst pattern", f"{nt['_coupling_raw']:.2f} mV", f"{P('n_aggr')} x {P('cc_ratio')} x signal"])
    rows.append(["Neighbour-BL coupling after decision feedback", f"{nt['coupling_det']:.2f} mV", f"x {P('dfb_residual')}"])
    rows.append(["WL kickback mean (removed by dummy WL/reference)", f"{nt['_wl_kick_mean']:.2f} mV", "systematic"])
    rows.append(["**Readout residual (k sigma + RTN + coupling), with DFB**", f"**{res:.1f} mV**", "the decisive-experiment number"])
    rows.append(["Readout residual without decision feedback", f"{res_nodfb:.1f} mV", ""])
    table(["Term", "Value", "Note"], rows)

    # ---------------- 4. margin ----------------
    m0 = margin_mV(cs0, cbl)
    csmin = cs_min_fF(cbl)
    lmin = l_cap_for(csmin)
    r_allow = residual_allowed(cs0, cbl)
    r_allow_03 = residual_allowed(0.30, cbl)
    r_allow_06 = residual_allowed(0.60, cbl)
    emit("## 3. Sense margin at raw BER 1e-4 (3.72 sigma)")
    emit()
    table(["Quantity", "Value"], [
        ["Margin at Cs 0.45 fF (modelled readout)", f"{m0:+.1f} mV (signal {sig0:.1f} mV; guard {P('guard_mV'):.0f} mV included)"],
        ["Minimum Cs (modelled readout, DFB on)", f"{csmin:.3f} fF -> capacitor {lmin:.0f} nm"],
        ["Minimum Cs without decision feedback", f"{cs_min_fF_nodfb(cbl):.3f} fF"],
        ["Allowed readout residual at Cs 0.30 fF", f"{r_allow_03:.1f} mV"],
        ["Allowed readout residual at Cs 0.45 fF", f"**{r_allow:.1f} mV**"],
        ["Allowed readout residual at Cs 0.60 fF", f"{r_allow_06:.1f} mV"],
    ])

    # ---------------- 5. retention ----------------
    it, itft, icap = leak_tail_A(lcap0)
    ret0 = retention_s(cs0, it)
    i_spec = cs0 * 1e-15 * P("droop_budget_V") / P("t_ret_target_s")
    emit("## 4. Retention (85 C, 1e-4 tail)")
    emit()
    table(["Quantity", "Value"], [
        ["Oxide access TFT Ioff, median", f"{P('ioff_med_85C_A')*1e18:.1f} aA"],
        ["TFT Ioff at 3.72 sigma Vt tail (sigma %.0f mV, SS %.0f mV/dec)" % (P("vt_sigma_mV"), P("ss_mV_dec_85C")), f"{itft*1e18:.1f} aA"],
        ["Capacitor dielectric leakage (J %.0e A/cm2, area %.4f um2)" % (P("j_cap_A_cm2"), (P('sn_perimeter_nm')*lcap0+P('sn_end_nm2'))*1e-6), f"{icap*1e18:.1f} aA"],
        ["Tail-cell total leakage", f"{it*1e18:.1f} aA"],
        ["Leakage spec for 1 s with 75 mV droop at 0.45 fF", f"**{i_spec*1e18:.1f} aA** (concept quoted 68 aA for 150 mV droop)"],
        ["Tail-cell retention", f"{ret0:.2f} s (DDR5: 0.032 s hot) -> {ret0/P('ddr5_refresh_s_hot'):.0f}x longer refresh interval"],
    ])

    # ---------------- 6. density and break-even ----------------
    dt0 = gb_per_mm2_tier(cell0)
    n_be = P("d_1b_gb_mm2") / dt0
    nt_total = P("cell_tiers_total")
    d64 = dt0 * nt_total
    avail, need, subl = amp_area_check(lcap0)
    emit("## 5. Density, amp-tier area and 1-beta break-even")
    emit()
    table(["Quantity", "Value"], [
        ["Per-tier density (eff %.2f, ECC %.3f)" % (P("array_eff"), P("ecc_factor")), f"{dt0:.4f} Gb/mm2"],
        ["Density break-even vs 1-beta (0.447 Gb/mm2)", f"{n_be:.1f} cell tiers (A1 base 26)"],
        ["64 cell tiers (4 groups)", f"{d64:.2f} Gb/mm2 = {d64/P('d_1b_gb_mm2'):.1f}x 1-beta (before tier yield)"],
        ["Amp-tier area per vertical BL available / needed (share %d)" % P("share"), f"{avail:.4f} / {need:.4f} um2 -> {subl} amp sub-layer(s)"],
        ["Stack height", f"{nt_total*60/1000 + math.ceil(nt_total/g)*subl*0.12:.1f} um (60 nm cell tier, 120 nm amp sub-layer); BL hole AR per group {g*60/40:.0f}:1"],
    ])

    # ---------------- 7. cost ----------------
    wc, groups = wafer_cost(nt_total, g, subl)
    wc_sc, _ = wafer_cost(nt_total, g, subl, smartcut=True)
    y = stack_yield(nt_total, groups)
    rc = rel_cost_per_bit(wc, d64, y)
    rc_sc = rel_cost_per_bit(wc_sc, d64, y)
    emit("## 6. Wafer cost and $/GB vs 1-beta DDR5")
    emit()
    table(["Variant (64 cell tiers)", "Wafer $", "Stack yield", "$/bit vs 1b", "$/GB"], [
        ["PIXEL-STACK (oxide amp tiers)", f"{wc:,.0f}", f"{y:.3f}", f"{rc:.2f}x", f"${rc*P('cost_1b_usd_per_gb'):.2f}"],
        ["Smart-Cut c-Si sense layer per group (I-11545/N-48)", f"{wc_sc:,.0f}", f"{y:.3f}", f"{rc_sc:.2f}x", f"${rc_sc*P('cost_1b_usd_per_gb'):.2f}"],
        ["1-beta DDR5 reference", f"{P('wafer_1b_usd'):,.0f}", "(in $1.48)", "1.00x", f"${P('cost_1b_usd_per_gb'):.2f}"],
    ])
    # cost break-even tiers
    be_rows = []
    for n in (8, 12, 16, 24, 32, 48, 64, 96, 128):
        gg = math.ceil(n / g)
        w_, _ = wafer_cost(n, g, subl)
        yy = stack_yield(n, gg)
        dd = dt0 * n
        be_rows.append([n, f"{dd:.2f}", f"{dd/P('d_1b_gb_mm2'):.2f}x", f"{w_:,.0f}", f"{yy:.3f}", f"{rel_cost_per_bit(w_, dd, yy):.2f}x"])
    table(["Cell tiers", "Gb/mm2", "x 1b density", "Wafer $", "Yield", "$/bit vs 1b"], be_rows)

    # ---------------- 8. energy/timing/endurance ----------------
    tfb, trc, tset = t_read_ns()
    e_acc, parts = energy_access_fJ(cs0, cbl, trc)
    e_ref_ratio = (e_acc / ret0) / (P("ddr5_e_refresh_fJ_bit") / P("ddr5_refresh_s_hot"))
    rows_per_bank = P("bank_bits") / P("bits_per_row")
    ref_busy = rows_per_bank * trc * 1e-9 / ret0
    emit("## 7. Timing, energy, refresh and endurance")
    emit()
    table(["Quantity", "Value"], [
        ["SF settling per sample (1%)", f"{tset:.1f} ns"],
        ["First bit of a share group", f"{tfb:.1f} ns"],
        ["Row cycle tRC (share %d, sequential CDS + restore)" % P("share"), f"{trc:.0f} ns (DDR5 ~{P('ddr_trc_ns'):.0f} ns; mission window 10-100 ns)"],
        ["Energy per accessed bit (x%.0f periphery)" % P("periph_mult"), f"{e_acc:.0f} fJ (BL {parts['bl']:.1f}, column {parts['col']:.1f}, SF bias {parts['sf']:.1f}, WL {parts['wl']:.1f} fJ core) vs DDR5 46 fJ"],
        ["Refresh power per bit vs DDR5 at 32 ms", f"{e_ref_ratio:.3f}x ({1/e_ref_ratio:.0f}x lower)"],
        ["Refresh busy time per bank", f"{ref_busy*100:.2f}% (DDR5 16Gb: 7.6% all-bank at 3.9 us tREFI)"],
        ["Worst-case access count, 10 yr at tRC", f"{10*3.156e7/(trc*1e-9):.1e} (demonstrated oxide 2T0C: {P('endurance_demo'):.0e}, measurement-limited)"],
        ["Amp-tier SF Vt drift tolerated by CDS", f"{P('sf_headroom_mV'):.0f} mV (headroom, not margin: offset cancels each read)"],
    ])

    # ---------------- 9. sensitivity tables ----------------
    emit("## 8. Sensitivity: the key unknown (oxide SF 1/f + RTN + coupling after CDS)")
    emit()
    emit("Readout residual (mV, 3.72 sigma random + RTN tail + coupling after DFB) vs Hooge alpha and SF gate area. "
         f"Pass at Cs 0.45 fF requires <= {r_allow:.1f} mV.")
    emit()
    areas = [(50, 50), (100, 100), (150, 200), (300, 300), (1000, 1000)]
    alphas = [1e-3, 3e-3, 1e-2, 3e-2, 1e-1]
    hdr = ["alpha_H \\ SF W x L (nm)"] + [f"{w}x{l}" for w, l in areas]
    rows = []
    for a in alphas:
        r = [f"{a:.0e}"]
        for w, l in areas:
            ntt = noise_terms(alpha_h=a, w_nm=w, l_nm=l, cs=cs0, cbl=cbl)
            rr = readout_residual(ntt)
            r.append(f"{rr:.1f}{'' if rr <= r_allow else ' X'}")
        rows.append(r)
    table(hdr, rows)
    emit("X = fails at Cs 0.45 fF (needs a larger capacitor). Fung JAP 2010 long-channel a-IGZO: alpha ~1.5e-3; "
         "Cho EDL 2009 Al2O3/SiNx ~6e-3, Al2O3-only 100-1000x noisier (normalized). Scaled ALD IGZO is trap-dominated "
         "(Lee & Niu, TED 2025) -- the measurement must use scaled devices.")
    emit()

    emit("### Measured readout residual -> minimum Cs -> capacitor length -> density (16-tier groups)")
    emit()
    rows = []
    for rmeas in (5, 10, 15, 20, 25, 30, 40, 50, 60, 70):
        cm = cs_min_fF(cbl, residual_override=rmeas)
        if math.isinf(cm) or cm > 5:
            rows.append([rmeas, "no solution", "-", "-", "-", "-", "NO-GO"])
            continue
        lc = l_cap_for(cm)
        ce = cell_um2(lc)
        dt = gb_per_mm2_tier(ce)
        w_, gg = wafer_cost(64, g, subl)
        rcb = rel_cost_per_bit(w_, dt * 64, stack_yield(64, gg))
        verdict = ("GO + stretch" if cm <= 0.30 else "GO" if cm <= 0.45 + 1e-9 else
                   "NO-GO as pitched (1 fF fallback)" if cm <= 1.0 else "NO-GO (oxide amp tier dead)")
        rows.append([rmeas, f"{cm:.2f}", f"{lc:.0f}", f"{ce:.4f}", f"{P('d_1b_gb_mm2')/dt:.1f}",
                     f"{dt*64:.2f} ({dt*64/P('d_1b_gb_mm2'):.1f}x), {rcb:.2f}x $/bit", verdict])
    table(["Readout residual (mV)", "Cs min (fF)", "Cap length (nm)", "Cell um2", "Break-even tiers",
           "64-tier Gb/mm2, $/bit vs 1b", "Verdict"], rows)

    emit("### Group size (tiers per amp tier) at the modelled readout")
    emit()
    rows = []
    for gg in (4, 8, 16, 32, 64):
        cb = c_bl_fF(gg)
        cm = cs_min_fF(cb)
        if math.isinf(cm):
            rows.append([gg, f"{cb:.2f}", "inf", "-", "-", "-", "-"])
            continue
        lc = l_cap_for(cm)
        ce = cell_um2(lc)
        dt = gb_per_mm2_tier(ce)
        av, nd, sl = amp_area_check(lc)
        w_, grp = wafer_cost(64, gg, sl)
        rcb = rel_cost_per_bit(w_, dt * 64, stack_yield(64, grp))
        rows.append([gg, f"{cb:.2f}", f"{cm:.2f}", f"{lc:.0f}", f"{dt*64:.2f}", grp, f"{rcb:.2f}x"])
    table(["Tiers/group", "C_BL (fF)", "Cs min (fF)", "Cap (nm)", "64-tier Gb/mm2", "Amp tiers", "$/bit vs 1b"], rows)

    emit("### Data-dependent coupling (Cc/C_BL per aggressor) with and without decision feedback")
    emit()
    rows = []
    for ccr in (0.02, 0.05, 0.08, 0.12, 0.20):
        r1 = readout_residual(noise_terms(cs=cs0, cbl=cbl, cc_ratio=ccr, dfb=True))
        r0 = readout_residual(noise_terms(cs=cs0, cbl=cbl, cc_ratio=ccr, dfb=False))
        rows.append([ccr, f"{r1:.1f}", "pass" if r1 <= r_allow else "FAIL", f"{r0:.1f}", "pass" if r0 <= r_allow else "FAIL"])
    table(["Cc/C_BL", "Residual with DFB (mV)", "", "Residual raw (mV)", ""], rows)

    emit("### Retention vs Vt tail, hydrogen shift and capacitor leakage (Cs 0.45 fF, 75 mV droop)")
    emit()
    rows = []
    for vs in (20, 30, 50):
        for hs in (0, 20, 50, 100):
            for j in (1e-7, 1e-6):
                tot, a, b = leak_tail_A(lcap0, h_shift_mV=hs, vt_sigma=vs, j_cap=j)
                rt = retention_s(cs0, tot)
                rows.append([vs, hs, f"{j:.0e}", f"{tot*1e18:.1f}", f"{rt:.2f}", "ok" if rt >= 1.0 else ("refresh<1s" if rt >= 0.064 else "FAIL")])
    table(["Vt sigma (mV)", "H dVt (mV)", "J_cap (A/cm2)", "Tail leak (aA)", "Retention (s)", ">=1 s?"], rows)

    emit("### Sharing factor: amp-tier area vs row cycle time")
    emit()
    rows = []
    for s in (1, 2, 4, 8):
        INPUTS["share"] = (s, INPUTS["share"][1])
        av, nd, sl = amp_area_check(lcap0, share=s)
        _, trc_s, _ = t_read_ns(s)
        ntt = noise_terms(cs=cs0, cbl=cbl, share=s)
        rows.append([s, f"{nd:.4f}", f"{av:.4f}", sl, f"{trc_s:.0f}", f"{readout_residual(ntt):.1f}"])
    INPUTS["share"] = (2, INPUTS["share"][1])
    table(["Share", "Amp area need/BL (um2)", "Available/BL (um2)", "Sub-layers", "tRC (ns)", "Residual (mV)"], rows)

    emit("### Cost per amp sub-layer and per cell tier ($/bit vs 1-beta at 64 tiers)")
    emit()
    rows = []
    for ct in (15, 25, 40, 60):
        r = [f"${ct}/tier"]
        for ca in (150, 300, 600, 2000):
            INPUTS["usd_per_cell_tier"] = (ct, "sweep")
            INPUTS["usd_per_amp_sublayer"] = (ca, "sweep")
            w_, gg = wafer_cost(64, g, subl)
            r.append(f"{rel_cost_per_bit(w_, d64, stack_yield(64, gg)):.2f}x")
        rows.append(r)
    INPUTS["usd_per_cell_tier"] = (25.0, "restored")
    INPUTS["usd_per_amp_sublayer"] = (300.0, "restored")
    table(["Cell tier $ \\ amp sub-layer $", "$150", "$300", "$600", "$2,000 (~Smart-Cut)"], rows)

    # ---------------- GO/NO-GO ----------------
    emit("## 9. GO / NO-GO")
    emit()
    emit(f"Headline: Cs 0.45 fF fits a {lcap0:.0f} nm lateral capacitor; per-tier footprint {cell0:.4f} um2; "
         f"{dt0:.4f} Gb/mm2 per tier; 1-beta break-even at {n_be:.1f} tiers; 64 tiers = {d64:.2f} Gb/mm2 "
         f"({d64/P('d_1b_gb_mm2'):.1f}x 1-beta) at {rc:.2f}x 1-beta $/bit (${rc*P('cost_1b_usd_per_gb'):.2f}/GB, "
         f"before learning-curve); signal {sig0:.0f} mV; modelled readout residual {res:.1f} mV "
         f"({res_nodfb:.1f} mV without decision feedback) against {r_allow:.1f} mV allowed; tail retention {ret0:.2f} s at 85 C.")
    emit()
    r_allow_10 = residual_allowed(1.0, cbl)
    cs15 = cs_min_fF(cbl, residual_override=15.0)
    emit(f"**GO/NO-GO line (decisive experiment: planar IGZO pixel-amp array, 85 C).** Measure the post-CDS readout "
         f"residual = 3.72 sigma of the random read noise + 1e-4 RTN tail + worst-pattern neighbour coupling, on 3-3.5 fF "
         f"floating nodes read by an oxide SF with gate area <= 0.01 um2. "
         f"**GO if <= 15 mV** (Cs can fall to {cs15:.2f} fF, so the 0.45 fF / {lcap0:.0f} nm plan keeps "
         f"~{r_allow-15:.0f} mV for 3D-only effects the planar test cannot see). "
         f"CONDITIONAL GO at 15-{r_allow:.0f} mV (0.45 fF still closes, no spare). "
         f"**NO-GO for the concept as pitched above {r_allow:.0f} mV** (the 0.45 fF / 30-60 nm capacitor claim fails). "
         f"Between {r_allow:.0f} and {r_allow_10:.0f} mV a degraded fallback survives (Cs 0.45-1.0 fF, capacitor "
         f"<= {l_cap_for(1.0):.0f} nm, 64 tiers ~4-6x 1-beta). Above {r_allow_10:.0f} mV the oxide amp tier is dead "
         f"(footprint >= {cell_um2(l_cap_for(1.0)):.3f} um2, the edge over the A1 base case collapses). "
         f"Retention gate, same run: tail node leakage <= {i_spec*1e18:.0f} aA (>= 1 s at 75 mV droop) after a 400 C / "
         f"hydrogen sequence with access-TFT dVt < 20 mV; NO-GO if > {3*i_spec*1e18:.0f} aA. Revival path for a "
         "NO-GO: the Smart-Cut c-Si sense layer of I-11545 (N-48), which the cost table prices at ~1.7x the oxide amp tiers.")
    emit()


def cs_min_fF_nodfb(cbl):
    """Minimum Cs when decision feedback is off."""
    saved = INPUTS["dfb_residual"]
    INPUTS["dfb_residual"] = (1.0, saved[1])
    try:
        return cs_min_fF(cbl)
    finally:
        INPUTS["dfb_residual"] = saved


if __name__ == "__main__":
    main()
    here = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(here, "..", "research", "stage3", "pixel-stack_model_output.md")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as fh:
        fh.write("\n".join(OUT) + "\n")
