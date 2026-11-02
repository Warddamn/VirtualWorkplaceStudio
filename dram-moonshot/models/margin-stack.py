#!/usr/bin/env python3
"""
margin-stack.py -- first-principles model of MARGIN STACK (dram-moonshot Stage 3, rank 1).

Owner: dos-margin-stack. Written 2026-11-02. Pure standard library. Run from dram-moonshot/:
    python3 models/margin-stack.py
It prints a report and writes research/stage3/margin-stack_model_output.md.

Concept (research/stage3/FINAL_CONCEPTS.json, slug margin-stack): put a 3-transistor local gain stage
on every 16-32-cell bitline segment of an oxide-channel (IGZO) 4F2 DRAM, read it with correlated
double sampling (CDS), size the array for raw BER 1e-4 behind row ECC with erasure flags, and shrink
the storage capacitor from ~5.4 fF (1.3 um, AR~62 pillar) to <=0.5 fF (a ~130 nm stub).

What this model computes, with explicit arithmetic:
  1. Baseline anchors (1-beta capacitor, bitline, electrons, kT/C floor).
  2. A bottom-up post-CDS residual budget for a same-step oxide gain FET, including two terms the
     concept did not budget: wordline kick-back onto a ~1.5 fF local node and the gain-FET bias.
  3. Required Cs for every lever combination (global-line levers, local gain with/without CDS).
  4. Raw-BER / BCH t=8 / erasure-flag statistics: what flags are worth under Gaussian noise and how
     many confident (unflaggable) errors the code can absorb.
  5. Retention from IGZO channel + capacitor-dielectric leakage, with the droop budget optimised.
  6. Energy per access and refresh power; 7. area, $/GB vs $1.48/GB; 8. 3D-tier capacitor length;
  9. sense timing; 10. sensitivity on the key unknown; 11. MPW statistics and budget check;
  12. the GO/NO-GO threshold.

Every input carries a source URL or "ESTIMATE: basis". Numbers marked [SPECULATIVE] are first-principles
estimates with no measurement behind them.
"""

import math
import os

EPS0 = 8.854e-12     # F/m
KB = 1.380649e-23    # J/K
QE = 1.602e-19       # C
T_HOT = 358.0        # K (85 C)

A1 = "dram-moonshot research/phaseA/A1_scaling_limits.md + models/dram_cell_physics.py"
RV = "ram-venture models/dram_cost_stack.py (via A1/A2 md)"

# --------------------------------------------------------------------------------------------
# INPUTS  (value, unit, source)
# --------------------------------------------------------------------------------------------
INPUTS = {
    # ---- 1-beta reference (A1) ----
    "cs_1b_fF": (5.42, "fF", A1 + "; TechInsights/Choe 5-6 fF at 1c https://www.techinsights.com/ja/node/37840"),
    "cap_h_1b_nm": (1300.0, "nm", A1 + "; patents cite 50-100:1 AR https://patents.google.com/patent/US12193208"),
    "pillar_d_1b_nm": (21.1, "nm", A1 + " (honeycomb pitch 35.1 nm - 14 nm gap) [ESTIMATE in A1]"),
    "eot_cap_nm": (0.55, "nm", A1 + " (ZrO2-based, 6-7 nm physical) [ESTIMATE in A1]"),
    "vary_1b_V": (1.05, "V", A1 + " [ESTIMATE in A1]"),
    "droop_1b_mV": (155.0, "mV", A1 + " (allowed '1' droop that reproduces 5.42 fF)"),
    "dv_budget_conv_mV": (50.0, "mV", A1 + "; margin = dVBL-(VOS+coupling) https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11763878"),
    "k_sigma_noecc": (7.0, "sigma", "ESTIMATE: Stage 2 I-11559 convention; 1.7e10 cells x Q(7)=0.02 expected fails/die"),
    "cbl_per_cell_6f2_fF": (0.06, "fF/cell", A1 + "; Cbl = n*c_cell + c_SA https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12106797"),
    "cbl_fixed_fF": (4.0, "fF", A1),
    "cells_per_bl": (512, "cells", A1),
    "density_1b_gb_mm2": (0.447, "Gb/mm2", A1 + " (16Gb/35.83 mm2 Micron D1b teardown)"),
    "cost_ddr5_usd_gb": (1.48, "$/GB", RV + " (1-beta $3.8k wafer, 3,068 GB/wafer)"),
    "wafer_cost_usd": (3800.0, "$/wafer", RV),
    # ---- oxide 4F2 array (MARGIN STACK target) ----
    "vary_ox_V": (1.0, "V", "ESTIMATE: concept convention (0.5 V half swing); IGZO VCT keeps ~1 V array"),
    "droop_frac": (0.15, "of half swing", "ESTIMATE: concept convention 0.5 V x 0.85 = 0.425 V usable"),
    "ber_raw": (1e-4, "per bit", "concept RAW-BER CONTRACT; Hi-ECC strong-BCH precedent https://courses.grainger.illinois.edu/CS534/fa2021/reading_list/9a.pdf"),
    "n_seg": (32, "cells/segment", "concept; IBM 3T micro-SA on ~32-cell local BL https://researcher.ibm.com/publications/a-500-mhz-random-cycle-15-ns-latency-soi-embedded-dram-macro-featuring-a-three-transistor-micro-sense-amplifier"),
    "c_lbl_per_cell_fF": (0.04, "fF/cell", "ESTIMATE: between A1's 0.06 (6F2, WL/contact coupling) and ~0.01 (wire only, 29 nm/cell) for a buried 4F2 BL"),
    "c_seg_fixed_fF": (0.20, "fF", "ESTIMATE: gain-FET gate ~0.05 fF + reset/write FET junctions + BL-to-gate strap"),
    "c_seg_concept_fF": (1.0, "fF", "concept FINAL_CONCEPTS.json step_change (reproduction only)"),
    "sigma_vt_concept_mV": (40.0, "mV", "concept / Stage 2 I-00257 (reproduction only)"),
    "avt_oxide_mVum": (2.5, "mV*um", "ESTIMATE: no IGZO AVT found (search 2026-11-02); Si HKMG ~1-2 mV*um and scaling per https://research.ibm.com/publications/transistor-mismatch-properties-in-deep-submicrometer-cmos-technologies; oxide assumed worse"),
    "vct_channel_d_nm": (15.0, "nm", "ESTIMATE: VCT pillar inside a 4F2 site at F~14.7 nm"),
    "vct_lg_nm": (60.0, "nm", "ESTIMATE: vertical gate length"),
    "eot_gate_nm": (2.0, "nm", "ESTIMATE: IGZO GAA gate stack"),
    "n_gain_pillars": (1, "pillars", "concept: one same-step gain FET per segment"),
    "sites_extra_per_seg": (3, "4F2 sites", "concept: 3T local amp (gain, reset, write-back) per segment"),
    "sites_strap": (1, "4F2 site", "ESTIMATE: buried-BL-to-gain-gate strap/contact (Stage 2 critic: likely one critical mask)"),
    "vov_gain_V": (0.40, "V", "ESTIMATE: needs a pulsed read-source line or back gate (same-step FET has the access FET's high Vt)"),
    "gain_local": (3.0, "V/V", "ESTIMATE: gm*t_int/C_GBL with gm~25 uS, t~0.7 ns, C_GBL 6 fF"),
    "sigma_comp_az_mV": (3.0, "mV", "ESTIMATE: Stage 3 system inventor's post-auto-zero offset (FINAL_CONCEPTS.md ruling 3)"),
    "c_sample_fF": (10.0, "fF", "ESTIMATE: CDS sampling capacitor on the global line"),
    "sigma_1f_rtn_mV": (4.0, "mV", "ESTIMATE [SPECULATIVE]: oxide-FET 1/f+RTN between two samples ~5-10 ns apart; single-trap dVt=q/(Cox*W*L)~6 mV here"),
    "c_ov_access_fF": (0.010, "fF", "ESTIMATE: WL-to-BL overlap of the VCT access FET"),
    "dv_wl_V": (3.0, "V", A1 + " (boosted WL ~2.9 V)"),
    "vov_access_V": (2.0, "V", "ESTIMATE: VWL - Vt - Vnode at turn-on"),
    "chan_charge_to_bl": (0.5, "fraction", "ESTIMATE: channel charge splits ~half to each terminal"),
    "kick_cancel": (0.90, "fraction", "ESTIMATE: dummy-WL / complementary-edge compensation efficiency"),
    "kick_geom_frac": (0.05, "fraction", "ESTIMATE: random part of kick from geometry spread"),
    "sigma_vt_access_mV": (50.0, "mV", "ESTIMATE: access-FET Vt spread"),
    "alpha_couple": (0.10, "per side", "ESTIMATE: Stage 2 I-11588/I-05218 critics assume BL-BL 20-30% of Cbl total (10-15%/side); interleave/shield ~halves"),
    "cs_var_frac": (0.05, "sigma/mean", "ESTIMATE: stub CD/height spread"),
    "sigma_bl_ct_mV": (3.0, "mV", "ESTIMATE: BL-referred residual of a self-referenced charge-transfer pre-sense (N-04)"),
    "neut_ratio": (0.5, "Cn/Cbl", "Stage 2 I-11588 critic cap (worst-pattern stability)"),
    "sigma_neut_amp_mV": (3.0, "mV", "ESTIMATE: neutraliser amp offset after auto-zero (I-11588 innovation critic)"),
    # ---- ECC ----
    "ecc_n": (592, "bits", "concept: 512 data + 80 check (BCH t=8), Stage 2 I-11559"),
    "ecc_t": (8, "errors", "concept"),
    # ---- retention / leakage ----
    "ioff_igzo_median_aA": (1.0, "aA", "Kioxia/Nanya OCTRAM Ioff <1 aA https://www.businesswire.com/news/home/20241209099702/en/Kioxia-Develops-OCTRAM-Oxide-Semiconductor-Channel-Transistor-DRAM-Technology"),
    "j_diel_A_cm2": (1e-8, "A/cm2 at ~0.5 V", "ESTIMATE: A1 target <=1e-7 A/cm2 at 0.8 V; leakage falls steeply at half-VDD bias"),
    "t_ref_ddr5_s": (0.064, "s", A1 + " (JEDEC 64 ms)"),
    "refresh_guard": (2.0, "x", "ESTIMATE: refresh at half the worst-cell retention (VRT/temperature guard)"),
    "cells_16gb": (1.7e10, "cells", A1 + " (16Gb + ECC)"),
    # ---- energy ----
    "c_gbl_fF": (6.0, "fF", "ESTIMATE: 15 um GBL at ~0.25 fF/um + 16 amp drains/junctions"),
    "v_sample_swing_V": (0.2, "V", "ESTIMATE: GBL swing per CDS sample"),
    "e_comp_fJ": (2.0, "fJ", "ESTIMATE: comparator/latch per column per read"),
    "e_wl_per_bit_fJ": (2.8, "fJ", A1 + " (WL energy per refreshed bit)"),
    "periph_factor": (2.0, "x", A1),
    "reg_eff": (0.95, "", A1),
    # ---- area / cost ----
    "array_eff_4f2_puc": (0.70, "", A1 + " (4F2 with periphery under cell)"),
    "density_4f2_gb_mm2": (0.762, "Gb/mm2", A1 + " (4F2 at F=14.7 nm, eff 0.70)"),
    "cap_module_share": (0.15, "of wafer cost", "ESTIMATE: concept says 10-20% [unsourced]; range swept"),
    "cap_height_scaled_frac": (0.65, "of module cost", "ESTIMATE: mold dep, HAR etch, support lattice, ALD dose scale with height/AR"),
    "added_mask_frac": (0.012, "of wafer cost", "ESTIMATE: one critical DUV litho+etch layer for the BL-to-gate strap"),
    # ---- 3D tier ----
    "tier_pitch_nm": (50.0, "nm", A1 + " (3D lateral tier base 50x600 nm)"),
    "lat_fet_len_nm": (150.0, "nm", "ESTIMATE: lateral FET + contacts; A1 base 600 nm = 150 + ~450 nm capacitor"),
    "lat_cap_d_nm": (40.0, "nm", "ESTIMATE: lateral cylinder diameter in a ~60 nm tier"),
    "tier_eff": (0.55, "", A1),
    "c_seg_3d_fF": (3.0, "fF", "Stage 2 I-11545: 16-cell vertical BL ~2-4 fF"),
    # ---- timing ----
    "ion_access_uA": (15.0, "uA", "OCTRAM Ion >15 uA (businesswire link above)"),
    "i_gain_uA": (5.0, "uA", "ESTIMATE: gain FET current at Vov 0.4 V"),
    # ---- MPW / budget ----
    "mpw_usd_mm2": (17997.0, "$/mm2", "CMC 22FDX run 2602DJ, 4 mm2 min (via search snippet) https://products.cmc.ca/Fabrication/DMT_Fab"),
    "mpw_area_mm2": (6.0, "mm2", "ESTIMATE: 2.1M emulated cells ~1 mm2 + 64k amps + 64 global lines + BIST/pads"),
    "mpw_chips_tested": (20, "chips", "ESTIMATE"),
}


def I(k):
    return INPUTS[k][0]


OUT = []


def p(s=""):
    OUT.append(s)
    print(s)


def hr(t):
    p("")
    p("## " + t)
    p("")


# --------------------------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------------------------
def Q(x):
    return 0.5 * math.erfc(x / math.sqrt(2.0))


def Qinv(pv):
    lo, hi = 0.0, 40.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if Q(mid) > pv:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def c_per_nm_fF(d_nm, eot_nm):
    """Pillar/cylinder outer wall: fF per nm of height."""
    return 3.9 * EPS0 * math.pi * d_nm * 1e-9 * 1e-9 / (eot_nm * 1e-9) * 1e15


CPN_1B = c_per_nm_fF(I("pillar_d_1b_nm"), I("eot_cap_nm"))


def stub_h_nm(cs):
    return cs / CPN_1B


def cs_for_signal(dv, cnode, vsig):
    if dv >= vsig:
        return float("inf")
    return cnode * dv / (vsig - dv)


def c_seg(n=None, per=None, fixed=None):
    n = I("n_seg") if n is None else n
    per = I("c_lbl_per_cell_fF") if per is None else per
    fixed = I("c_seg_fixed_fF") if fixed is None else fixed
    return n * per + fixed


VSIG = I("vary_ox_V") / 2 * (1 - I("droop_frac"))   # 0.425 V
K_ECC = Qinv(I("ber_raw"))                          # 3.719


def cg_access_fF():
    cox = 3.9 * EPS0 / (I("eot_gate_nm") * 1e-9)     # F/m2
    area = math.pi * I("vct_channel_d_nm") * 1e-9 * I("vct_lg_nm") * 1e-9
    return cox * area * 1e15


def sigma_vt_gain_mV(npillars=None):
    npillars = I("n_gain_pillars") if npillars is None else npillars
    w_um = math.pi * I("vct_channel_d_nm") * 1e-3
    l_um = I("vct_lg_nm") * 1e-3
    return I("avt_oxide_mVum") / math.sqrt(w_um * l_um * npillars)


def kick_terms(cs, cseg):
    """WL kick-back onto the (cell + local bitline) node. Returns mean, random sigma, det. residual (mV)."""
    cg = cg_access_fF()
    ctot = cs + cseg
    q_mean = I("chan_charge_to_bl") * cg * I("vov_access_V") + I("c_ov_access_fF") * I("dv_wl_V")  # fC
    mean = q_mean / ctot * 1e3
    # data-dependent part: a stored '0' turns the FET on with ~0.5 V more Vgs than a '1' (BL at Vpre)
    asym = I("chan_charge_to_bl") * cg * (I("vary_ox_V") / 2) / ctot * 1e3
    rnd = math.sqrt((I("kick_geom_frac") * mean) ** 2 +
                    (I("chan_charge_to_bl") * cg * I("sigma_vt_access_mV") / ctot) ** 2)
    det = mean * (1 - I("kick_cancel")) + asym / 2
    return mean, rnd, det, asym


def cds_residual(cs, cseg, scale_1f=1.0, sigma_comp=None, gain=None, vov=None, npillars=None):
    sigma_comp = I("sigma_comp_az_mV") if sigma_comp is None else sigma_comp
    gain = I("gain_local") if gain is None else gain
    vov = I("vov_gain_V") if vov is None else vov
    svt = sigma_vt_gain_mV(npillars)
    tail = max(0.05, (vov - 4 * svt / 1e3) / vov)   # square-law gm at a -4 sigma (high-Vt) gain FET
    s_comp = sigma_comp / (gain * tail)
    s_ktc = math.sqrt(2 * KB * T_HOT / (I("c_sample_fF") * 1e-15)) * 1e3 / gain
    s_1f = I("sigma_1f_rtn_mV") * scale_1f
    _, s_kick, det, _ = kick_terms(cs, cseg)
    tot = math.sqrt(s_comp ** 2 + s_ktc ** 2 + s_1f ** 2 + s_kick ** 2)
    return dict(s_comp=s_comp, s_ktc=s_ktc, s_1f=s_1f, s_kick=s_kick, tot=tot, det=det, tail=tail, svt=svt)


def solve_local_cs(sigma_fn, cseg, k=K_ECC, alpha=None, cv=None, det_fn=None, vsig=VSIG):
    """Find Cs so that S(1-2a) - det >= k*sqrt(sigma^2 + (cv*S)^2), S = vsig*Cs/(Cs+cseg).
    sigma_fn(cs) and det_fn(cs) may depend on Cs (kick terms scale with 1/(Cs+Cseg))."""
    alpha = I("alpha_couple") if alpha is None else alpha
    cv = I("cs_var_frac") if cv is None else cv

    def margin(cs):
        s = vsig * cs / (cs + cseg) * 1e3
        sig = sigma_fn(cs)
        det = det_fn(cs) if det_fn else 0.0
        return s * (1 - 2 * alpha) - det - k * math.sqrt(sig ** 2 + (cv * s) ** 2)

    lo, hi = 1e-4, 200.0
    if margin(hi) < 0:
        return float("inf")
    for _ in range(200):
        mid = math.sqrt(lo * hi)
        if margin(mid) >= 0:
            hi = mid
        else:
            lo = mid
    return hi


def retention_s(cs_fF, i_chan_aA, droop_mV, j_diel=None):
    """Worst-cell retention: channel leak + capacitor-dielectric leak in parallel."""
    j_diel = I("j_diel_A_cm2") if j_diel is None else j_diel
    area_cm2 = cs_fF * 1e-15 / (3.9 * EPS0 / (I("eot_cap_nm") * 1e-9)) * 1e4
    i_tot = i_chan_aA * 1e-18 + j_diel * area_cm2
    return cs_fF * 1e-15 * droop_mV * 1e-3 / i_tot


def fmt_t(s):
    if s == float("inf"):
        return "inf"
    if s < 1e-3:
        return f"{s*1e6:.0f} us"
    if s < 1:
        return f"{s*1e3:.0f} ms"
    if s < 600:
        return f"{s:.1f} s"
    return f"{s/3600:.1f} h"


# Poisson tail tools for ECC
def pois_pmf(k, lam):
    if lam <= 0:
        return 1.0 if k == 0 else 0.0
    return math.exp(k * math.log(lam) - lam - math.lgamma(k + 1))


def pois_tail_gt(m, lam):
    """P(X > m), accurate both deep in the tail (~1e-20) and when lam >> m."""
    if m < 0:
        return 1.0
    if lam > m + 1:
        return max(0.0, 1.0 - sum(pois_pmf(k, lam) for k in range(0, m + 1)))
    kmax = m + 60 + int(10 * math.sqrt(lam + 1))
    return sum(pois_pmf(k, lam) for k in range(m + 1, kmax))


def fail_hard(p_bit, n=None, t=None):
    n = I("ecc_n") if n is None else n
    t = I("ecc_t") if t is None else t
    return pois_tail_gt(t, n * p_bit)


def fail_flags(lam_f, lam_e, budget):
    """Errors-and-erasures: fail if F + 2E > budget (budget = d-1 = 2t)."""
    tot = pois_tail_gt(budget // 2, lam_e)          # E >= budget/2 + 1 alone fails
    for e in range(0, budget // 2 + 1):
        tot += pois_pmf(e, lam_e) * pois_tail_gt(budget - 2 * e, lam_f)
    return tot


def flag_probs(s, w, p_x=0.0):
    """Normalised decision x~N(s,1): flagged if |x|<w; confident error if x<-w; p_x extra confident errors."""
    p_flag = (1 - Q(w - s)) - (1 - Q(-w - s))   # Phi(w-s) - Phi(-w-s)
    p_conf = Q(s + w) + p_x
    p_err = Q(s) + p_x
    p_flag_err = Q(s) - Q(s + w)
    return p_flag, p_conf, p_err, p_flag_err


def best_flag(s, p_x=0.0):
    n = I("ecc_n")
    budget = 2 * I("ecc_t")
    best = (fail_hard(Q(s) + p_x), 0.0)
    w = 0.02
    while w <= 2.5:
        pf, pc, _, _ = flag_probs(s, w, p_x)
        f = fail_flags(n * pf, n * pc, budget)
        if f < best[0]:
            best = (f, w)
        w += 0.02
    return best


def fail_mixed(p_total, f_flag, c_pair, w):
    """Errors split three ways: a fraction f_flag are Gaussian-tail (small |dV|, flaggable with window w, which also
    flags correct bits); a fraction c_pair arrive as confident 2-bit clusters in one codeword (shared-cause: row defect,
    hammer, VRT pair); the rest are confident singles. Fail if F + 2E + 4P > 2t."""
    n = I("ecc_n")
    budget = 2 * I("ecc_t")
    p_g = f_flag * p_total
    lam_p = n * c_pair * p_total / 2.0
    p_cs = max(0.0, (1 - f_flag - c_pair)) * p_total
    if p_g > 0:
        s = Qinv(p_g)
        pf, pc, _, _ = flag_probs(s, w, p_cs)
    else:
        pf, pc = 0.0, p_cs
    lam_f, lam_e = n * pf, n * pc
    tot = pois_tail_gt(budget // 4, lam_p)
    for k in range(0, budget // 4 + 1):
        tot += pois_pmf(k, lam_p) * fail_flags(lam_f, lam_e, budget - 4 * k)
    return tot


def max_ber(f_flag, c_pair, target):
    """Largest total raw BER meeting the codeword-failure target, with the flag window optimised."""
    def ok(pt):
        if f_flag <= 0:
            return fail_mixed(pt, 0.0, c_pair, 0.0) <= target
        w = 0.02
        while w <= 2.5:
            if fail_mixed(pt, f_flag, c_pair, w) <= target:
                return True
            w += 0.04
        return False
    lo, hi = math.log(1e-9), math.log(3e-2)
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        if ok(math.exp(mid)):
            lo = mid
        else:
            hi = mid
    return math.exp(lo)


# --------------------------------------------------------------------------------------------
# 0. inputs
# --------------------------------------------------------------------------------------------
def section_inputs():
    p("# MARGIN STACK -- model output")
    p("")
    p("Generated by `models/margin-stack.py` (pure stdlib). Agent `dos-margin-stack`, 2026-11-02.")
    p("Every number below is computed from the INPUTS table; [SPECULATIVE] marks first-principles terms with no measurement.")
    hr("0. INPUTS")
    p("| key | value | unit | source / basis |")
    p("|---|---|---|---|")
    for k, (v, u, s) in INPUTS.items():
        p(f"| {k} | {v:g} | {u} | {s} |")


# --------------------------------------------------------------------------------------------
# 1. baseline anchors
# --------------------------------------------------------------------------------------------
def section_baseline():
    hr("1. Baseline anchors (1-beta, A1 conventions)")
    cbl = I("cells_per_bl") * I("cbl_per_cell_6f2_fF") + I("cbl_fixed_fF")
    vsig_1b = I("vary_1b_V") / 2 - I("droop_1b_mV") / 1e3
    cs_1b = cs_for_signal(I("dv_budget_conv_mV") / 1e3, cbl, vsig_1b)
    e_1b = I("cs_1b_fF") * 1e-15 * I("vary_1b_V") / 2 / QE
    p(f"- Pillar capacitance per nm of height (d={I('pillar_d_1b_nm')} nm, EOT {I('eot_cap_nm')} nm): {CPN_1B*1e3:.2f} aF/nm "
      f"-> {I('cs_1b_fF')} fF needs {stub_h_nm(I('cs_1b_fF')):.0f} nm (AR {stub_h_nm(I('cs_1b_fF'))/I('pillar_d_1b_nm'):.0f}).")
    p(f"- 512-cell bitline: Cbl = {cbl:.1f} fF. With a 50 mV budget, VARY 1.05 V and 155 mV droop: Cs_min = {cs_1b:.2f} fF (reproduces A1's 5.42).")
    p(f"- Stored signal charge at 1-beta (Cs x VARY/2): {e_1b:,.0f} electrons.")
    p(f"- The 50 mV budget = {I('k_sigma_noecc'):.0f} sigma x {I('dv_budget_conv_mV')/I('k_sigma_noecc'):.2f} mV "
      f"(effective SA offset + coupling sigma backed out of the budget).")
    ktc_bl = math.sqrt(KB * T_HOT / (cbl * 1e-15)) * 1e3
    cseg = c_seg()
    ktc_charge_e = math.sqrt(KB * T_HOT * (cseg + 0.5) * 1e-15) / QE
    cs_kt_floor = K_ECC * math.sqrt(KB * T_HOT * cseg * 1e-15) / VSIG * 1e15
    p(f"- kT/C on the 512-cell bitline at 85 C: {ktc_bl:.2f} mV rms. On a {cseg:.2f} fF local node: "
      f"{math.sqrt(KB*T_HOT/(cseg*1e-15))*1e3:.2f} mV rms ({ktc_charge_e:.0f} e- with a 0.5 fF cell).")
    p(f"- Thermodynamic floor even with NO kTC cancellation: Cs >= {K_ECC:.2f} x sqrt(kT*Cseg)/Vsig = {cs_kt_floor:.3f} fF "
      f"(~{cs_kt_floor*1e-15*VSIG/QE:.0f} e-). Every case below sits 5-100x above it: the floor is mismatch, coupling and kick, not physics.")
    p(f"- Oxide-array usable half swing Vsig = {I('vary_ox_V')/2:.2f} V x (1-{I('droop_frac')}) = {VSIG:.3f} V. "
      f"Raw BER {I('ber_raw'):.0e} -> k = Q^-1 = {K_ECC:.3f} sigma (vs {I('k_sigma_noecc'):.0f}): x{I('k_sigma_noecc')/K_ECC:.2f} margin.")
    return cbl


# --------------------------------------------------------------------------------------------
# 2. post-CDS residual budget
# --------------------------------------------------------------------------------------------
def section_residual():
    hr("2. Post-CDS residual budget for a same-step oxide gain FET (input-referred at the local node, 85 C)")
    cseg = c_seg()
    cs_ref = 0.25
    r = cds_residual(cs_ref, cseg)
    mean, rnd, det, asym = kick_terms(cs_ref, cseg)
    cg = cg_access_fF()
    p(f"Local node: {I('n_seg')} cells x {I('c_lbl_per_cell_fF')} fF + {I('c_seg_fixed_fF')} fF = **Cseg {cseg:.2f} fF** "
      f"(concept assumed {I('c_seg_concept_fF')} fF). Evaluated at Cs = {cs_ref} fF.")
    p("")
    p(f"- Gain-FET Vt mismatch (Pelgrom, AVT {I('avt_oxide_mVum')} mV*um, W = pi x {I('vct_channel_d_nm'):.0f} nm, L {I('vct_lg_nm'):.0f} nm, "
      f"{I('n_gain_pillars')} pillar): sigma_Vt = {r['svt']:.0f} mV. **CDS cancels it** (both samples use the same FET).")
    p(f"- Gain spread is NOT cancelled. At Vov {I('vov_gain_V')} V a -4 sigma (high-Vt) gain FET keeps {r['tail']*100:.0f}% of gm, so the "
      f"global comparator's {I('sigma_comp_az_mV')} mV post-auto-zero offset refers to {r['s_comp']:.2f} mV at the input (G={I('gain_local')}).")
    p(f"- Sampling kTC on two {I('c_sample_fF'):.0f} fF caps / G: {r['s_ktc']:.2f} mV. Local-node reset kTC: cancelled by CDS (frozen before sample 1).")
    p(f"- 1/f + RTN between the two samples [SPECULATIVE]: {r['s_1f']:.1f} mV.")
    p(f"- **Wordline kick-back (new term).** Access-FET gate cap {cg*1e3:.0f} aF; channel charge to the node "
      f"{I('chan_charge_to_bl')} x {cg*1e3:.0f} aF x {I('vov_access_V')} V + overlap {I('c_ov_access_fF')*1e3:.0f} aF x {I('dv_wl_V')} V "
      f"= {(I('chan_charge_to_bl')*cg*I('vov_access_V')+I('c_ov_access_fF')*I('dv_wl_V'))*1e3:.0f} aC on {cs_ref+cseg:.2f} fF "
      f"-> **mean kick {mean:.0f} mV** (vs {mean*(cs_ref+cseg)/34.7:.1f} mV on a 35 fF bitline: {34.7/(cs_ref+cseg):.0f}x worse on a short segment). "
      f"Data-dependent asymmetry ('0' turns on harder): {asym:.1f} mV. "
      f"After {I('kick_cancel')*100:.0f}% dummy-edge cancellation and centring: deterministic loss {det:.1f} mV; random part {rnd:.1f} mV.")
    p(f"- **RSS residual sigma_res = {r['tot']:.1f} mV** plus {det:.1f} mV deterministic, plus coupling as a fractional loss "
      f"(signal x (1 - 2 x {I('alpha_couple')}) under worst-case neighbour data).")
    p("")
    p("| scenario | 1/f+RTN mV | comparator mV | gain Vov V | alpha | sigma_res mV | det mV |")
    p("|---|---|---|---|---|---|---|")
    scen = {}
    for name, s1f, sc, vov, a in (("optimistic", 0.5, 1.5, 0.5, 0.05), ("central", 1.0, 3.0, 0.4, 0.10),
                                  ("pessimistic", 2.5, 6.0, 0.3, 0.15)):
        rr = cds_residual(cs_ref, cseg, scale_1f=s1f, sigma_comp=sc, vov=vov)
        scen[name] = (s1f, sc, vov, a)
        p(f"| {name} | {rr['s_1f']:.1f} | {rr['s_comp']:.2f} | {vov} | {a} | {rr['tot']:.1f} | {rr['det']:.1f} |")
    p("")
    p("Bias conflict (design note): a gain FET made in the access-FET step inherits the access FET's high Vt (needed for <1 aA),")
    p("so at a 0.5 V local precharge it is OFF. It needs a pulsed negative read-source line or a back gate to reach Vov ~0.4 V.")
    return scen


# --------------------------------------------------------------------------------------------
# 3. required Cs, all lever combinations
# --------------------------------------------------------------------------------------------
def row(name, cs, note, rows):
    rows.append((name, cs, note))


def section_cases(cbl, scen):
    hr("3. Required storage capacitance for each lever combination")
    rows = []
    s_conv = I("dv_budget_conv_mV") / I("k_sigma_noecc")   # 7.14 mV effective sigma at the SA
    # A. 1-beta reference
    row("A. 1-beta 6F2, 512-cell BL, no ECC (reference)", I("cs_1b_fF"), "A1 teardown-calibrated", rows)
    # B. oxide 512 BL no ECC
    row("B. oxide 4F2, 512-cell BL, 50 mV, Vsig 0.425 V",
        cs_for_signal(0.050, cbl, VSIG), "same SA; smaller droop allowance", rows)
    # C. + ECC
    dv_c = K_ECC * s_conv
    row("C. + raw-BER-1e-4 row ECC (global line only)", cs_for_signal(dv_c / 1e3, cbl, VSIG),
        f"needs {dv_c:.1f} mV", rows)
    # D. + neutraliser
    rn = I("neut_ratio")
    s_d = math.sqrt(s_conv ** 2 + (I("sigma_neut_amp_mV") * rn / (1 - rn)) ** 2)
    dv_d = K_ECC * s_d
    row(f"D. + bitline neutraliser Cn/Cbl={rn}", cs_for_signal(dv_d / 1e3, cbl * (1 - rn), VSIG),
        f"Cbl_eff {cbl*(1-rn):.1f} fF, sigma {s_d:.1f} mV", rows)
    # E. charge-transfer pre-sense: BL-referred residual -> charge error Cbl*sigma
    for sct in (I("sigma_bl_ct_mV"), 1.0):
        q_noise = cbl * sct   # aC (fF*mV)
        cs_e = K_ECC * q_noise / (VSIG * 1e3)
        row(f"E. charge-transfer pre-sense, BL-referred residual {sct:.0f} mV + ECC", cs_e,
            f"charge error Cbl x {sct:.0f} mV = {q_noise:.0f} aC", rows)
    # F. concept reproduction
    cs_f = cs_for_signal(K_ECC * I("sigma_vt_concept_mV") / 1e3, I("c_seg_concept_fF"), VSIG)
    row("F. concept base case reproduced (Cseg 1.0 fF, 40 mV, no coupling/kick)", cs_f,
        "matches FINAL_CONCEPTS 0.54 fF", rows)
    cseg = c_seg()
    det_fn = lambda cs: kick_terms(cs, cseg)[2]
    # G. local gain, no CDS, 1 pillar
    svt1 = sigma_vt_gain_mV(1)
    sig_g = lambda cs: math.sqrt(svt1 ** 2 + kick_terms(cs, cseg)[1] ** 2 + I("sigma_1f_rtn_mV") ** 2)
    row(f"G. local gain + ECC, NO CDS, 1-pillar gain FET (sigma_Vt {svt1:.0f} mV)", solve_local_cs(sig_g, cseg, det_fn=det_fn),
        f"Cseg {cseg:.2f} fF, alpha {I('alpha_couple')}", rows)
    svt4 = sigma_vt_gain_mV(4)
    sig_h = lambda cs: math.sqrt(svt4 ** 2 + kick_terms(cs, cseg)[1] ** 2 + I("sigma_1f_rtn_mV") ** 2)
    row(f"H. local gain + ECC, NO CDS, 4-pillar gain FET (sigma_Vt {svt4:.0f} mV)", solve_local_cs(sig_h, cseg, det_fn=det_fn),
        "+3 sites/segment", rows)
    out = {}
    for name in ("optimistic", "central", "pessimistic"):
        s1f, sc, vov, a = scen[name]
        sig = lambda cs, s1f=s1f, sc=sc, vov=vov: cds_residual(cs, cseg, scale_1f=s1f, sigma_comp=sc, vov=vov)["tot"]
        cs_i = solve_local_cs(sig, cseg, alpha=a, det_fn=det_fn)
        out[name] = cs_i
        row(f"I. local gain + CDS + ECC, {name}", cs_i, f"alpha {a}", rows)
    p("| case | Cs needed fF | cut vs 5.42 fF | stub h nm (d 21 nm) | AR | stored e- (Cs x VARY/2) | note |")
    p("|---|---|---|---|---|---|---|")
    for name, cs, note in rows:
        h = stub_h_nm(cs)
        p(f"| {name} | {cs:.2f} | {I('cs_1b_fF')/cs:.1f}x | {h:,.0f} | {h/I('pillar_d_1b_nm'):.1f} | "
          f"{cs*1e-15*(I('vary_1b_V') if name.startswith('A.') else I('vary_ox_V'))/2/QE:,.0f} | {note} |")
    p("")
    cs_g = [c for nm, c, _ in rows if nm.startswith("G.")][0]
    cs_h = [c for nm, c, _ in rows if nm.startswith("H.")][0]
    p(f"Reading: without CDS a same-step oxide gain FET ({svt1:.0f} mV sigma_Vt) plus kick and coupling needs {cs_g:.1f} fF, a "
      f"{I('cs_1b_fF')/cs_g:.1f}x cut, not 10x; four parallel gain pillars bring it to {cs_h:.2f} fF at +9% array area.")
    p("The concept's 0.54 fF base case (row F) assumed a 1.0 fF segment, 40 mV, and no coupling or kick. CDS is therefore")
    p("load-bearing, not a stretch: with it the sensing-limited Cs is ~0.1-0.4 fF. Charge-transfer pre-sense on an unchanged")
    p("512-cell line (row E) reaches 0.5 fF only if its BL-referred residual is <=~1.6 mV, because a BL-referred error costs Cbl x dV of charge.")
    return out, rows


# --------------------------------------------------------------------------------------------
# 4. ECC and erasure flags
# --------------------------------------------------------------------------------------------
def section_ecc():
    hr("4. Raw BER, BCH t=8 and erasure flags")
    n, t = I("ecc_n"), I("ecc_t")
    target = fail_hard(I("ber_raw"))
    p(f"- BCH t={t} over {n} bits at raw BER {I('ber_raw'):.0e}: P(codeword fail) = P(>{t} errors) = **{target:.2e}** per read. "
      f"This is the concept's contract level and the target used below (at 100 GB/s, 64 B reads: one DUE per "
      f"~{1/(100e9/64*target)/3.15e7:.1f} server-years).")
    for pb in (3e-5, 1e-4, 2e-4, 3e-4, 1e-3):
        p(f"  - raw {pb:.0e}: {fail_hard(pb):.2e}")
    s0 = K_ECC
    f0, w0 = best_flag(s0)
    pf, pc, pe, pfe = flag_probs(s0, w0)
    p(f"- Errors-and-erasures decoding (fail if flagged + 2 x confident > {2*t}), pure Gaussian noise at s = {s0:.2f}: the best flag window "
      f"w = {w0:.2f} sigma gives fail {f0:.1e} (vs {target:.1e} hard). It flags {pfe/pe*100:.0f}% of errors but also "
      f"{(pf-pfe):.1e} correct bits per bit ({(pf-pfe)/pe:.1f}x the error rate): false flags eat the erasure budget, so flags are worth")
    p("  less than 'half the parity'. The table gives the largest raw BER that still meets the target:")
    p("")
    p("| errors flaggable (Gaussian-tail) | errors in same-codeword pairs | max raw BER | sense margin needed (sigma) | vs 3.72 sigma |")
    p("|---|---|---|---|---|")
    res = {}
    for f_flag, c_pair in ((0.0, 0.0), (0.5, 0.0), (0.8, 0.0), (0.9, 0.0), (1.0, 0.0),
                           (0.8, 0.001), (0.8, 0.01), (0.0, 0.001), (0.0, 0.01), (0.0, 0.1)):
        b = max_ber(f_flag, c_pair, target)
        res[(f_flag, c_pair)] = b
        pg = max(f_flag, 1e-12) * b if f_flag > 0 else b
        sg = Qinv(pg) if f_flag > 0 else Qinv(b)
        p(f"| {f_flag*100:.0f}% | {c_pair*100:.1f}% | {b:.1e} | {sg:.2f} | {K_ECC/sg:.2f}x |")
    p("")
    s_flag = Qinv(res[(1.0, 0.0)])
    p(f"- Pure Gaussian with flags: raw BER can rise to {res[(1.0,0.0)]:.1e} (s = {s_flag:.2f}), a {K_ECC/s_flag:.2f}x margin gain on top of ECC's "
      f"{I('k_sigma_noecc')/K_ECC:.2f}x. At 80% flaggable it is {res[(0.8,0.0)]:.1e} ({K_ECC/Qinv(0.8*res[(0.8,0.0)]):.2f}x).")
    p(f"- **Clustering is the real threat.** If just 1% of errors arrive as 2-bit pairs in one codeword, the allowed raw BER falls to "
      f"{res[(0.0,0.01)]:.1e} (hard) / {res[(0.8,0.01)]:.1e} (80% flaggable); at 10% pairs it is {res[(0.0,0.1)]:.1e}. "
      f"The DRAM Bender study must measure the pair fraction, not only the flagged fraction.")
    # parity saving: smallest erasure budget that meets the target at 1e-4 with flags
    p("")
    p("Where flags DO pay: a weaker code. Smallest designed distance (d-1 = flagged + 2 x confident budget) meeting the target at raw BER 1e-4:")
    p("")
    p("| errors flaggable | min d-1 | ~check bits (10 per t-equivalent) | vs 80 for hard t=8 | array area saved |")
    p("|---|---|---|---|---|")
    for f_flag in (0.0, 0.8, 1.0):
        best_b = None
        for b in range(16, 1, -2):
            ok = False
            if f_flag == 0:
                ok = pois_tail_gt(b // 2, n * 1e-4) <= target
            else:
                sg = Qinv(f_flag * 1e-4)
                w = 0.02
                while w <= 2.5 and not ok:
                    pf_, pc_, _, _ = flag_probs(sg, w, (1 - f_flag) * 1e-4)
                    ok = fail_flags(n * pf_, n * pc_, b) <= target
                    w += 0.02
            if ok:
                best_b = b
            else:
                break
        cb = 10 * best_b / 2
        p(f"| {f_flag*100:.0f}% | {best_b} | {cb:.0f} | -{80-cb:.0f} | {(80-cb)/592*100:.1f}% |")
    p("")
    p("Result: a single resolution-time flag window buys ~4% in sense margin and does not even shorten the code at this target, because")
    p("a window wide enough to catch most errors also flags ~4x as many correct bits. Flags are not a capacitor lever. Their value is")
    p("diagnostic (separating small-|dV| errors from confident ones) and weak-cell telemetry for scrubbing; multi-trial Chase/GMD soft")
    p("decoding might reach the ~1.1-1.2x of Stage 2 I-04613. The concept's '>=80% flagged' go criterion is therefore secondary;")
    p("the pair (same-codeword cluster) fraction below is the criterion that matters.")
    p("")
    p("- Codewords run along a row, so each bit passes a different segment amp and comparator: static offsets are iid across a codeword.")
    p("  A bad segment amp touches 32 cells in one column = 32 different rows = 32 different codewords (one bit each). Row-level")
    p("  causes (a weak wordline, hammer on one row, a VRT pair on adjacent cells) are what create same-codeword pairs.")
    return s_flag, res, target


# --------------------------------------------------------------------------------------------
# 5. retention
# --------------------------------------------------------------------------------------------
def section_retention(cs_central):
    hr("5. Retention: IGZO channel leakage + capacitor-dielectric leakage")
    droop = I("vary_ox_V") / 2 * I("droop_frac") * 1e3   # 75 mV
    p(f"Droop allowance at the concept's signal convention: {droop:.0f} mV (15% of the 0.5 V half swing). "
      f"Dielectric leak at {I('j_diel_A_cm2'):.0e} A/cm2 gives a size-independent limit of "
      f"{3.9*EPS0/(I('eot_cap_nm')*1e-9)*1e-4*droop*1e-3/I('j_diel_A_cm2'):.0f} s.")
    p("")
    leaks = (1, 10, 100, 1000, 13000)
    p("| Cs fF | " + " | ".join(f"tail {x:g} aA" for x in leaks) + " | Imax for 64 ms | Imax for 1 s |")
    p("|---" * (len(leaks) + 3) + "|")
    for cs in (0.125, 0.25, 0.5, 1.0, 5.42):
        cells = [fmt_t(retention_s(cs, x, droop)) for x in leaks]
        imax64 = cs * 1e-15 * droop * 1e-3 / I("t_ref_ddr5_s") * 1e18
        imax1 = cs * 1e-15 * droop * 1e-3 / 1.0 * 1e18
        p(f"| {cs} | " + " | ".join(cells) + f" | {imax64:,.0f} aA | {imax1:,.0f} aA |")
    p("")
    p("Note: the concept quotes 0.8-81 s at 1-100 aA and ~6 ms at 13 fA for 0.54 fF; those use a 150 mV droop. At its own 0.425 V")
    p("signal convention (75 mV droop) the numbers halve: 0.54 fF x 75 mV / 13 fA = 3.1 ms. Silicon access stays illegal either way.")
    # optimise droop: at a given Cs, take the largest droop that still meets the sensing requirement
    cseg = c_seg()
    det_fn = lambda cs: kick_terms(cs, cseg)[2]
    sig = lambda cs: cds_residual(cs, cseg)["tot"]
    p("")
    p("Droop optimisation (central CDS residual): for each Cs, the largest droop that still meets the k=3.72 sensing margin.")
    p("")
    p("| Cs fF | max droop mV | retention @10 aA | retention @100 aA | refresh interval @100 aA (guard 2x) |")
    p("|---|---|---|---|---|")
    best = {}
    for cs in (0.15, 0.25, 0.5, 1.0):
        lo, hi = 0.0, 0.49
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            vs = I("vary_ox_V") / 2 - mid
            need = solve_local_cs(sig, cseg, det_fn=det_fn, vsig=vs)
            if need <= cs:
                lo = mid
            else:
                hi = mid
        dmax = lo * 1e3
        r10 = retention_s(cs, 10, dmax)
        r100 = retention_s(cs, 100, dmax)
        best[cs] = (dmax, r10, r100)
        p(f"| {cs} | {dmax:.0f} | {fmt_t(r10)} | {fmt_t(r100)} | {fmt_t(r100/I('refresh_guard'))} |")
    p("")
    p("Once CDS works, the capacitor floor is set by the IGZO leakage TAIL and the refresh target, not by sensing.")
    return droop, best


# --------------------------------------------------------------------------------------------
# 6. energy
# --------------------------------------------------------------------------------------------
def section_energy(cs_plan, cbl, droop_best):
    hr("6. Energy per access and refresh power")
    v = I("vary_ox_V")
    cseg = c_seg()
    e_conv = cbl * I("vary_1b_V") ** 2 / 2 / I("reg_eff")
    e_lbl = (cs_plan + cseg) * v ** 2 / 2
    e_gbl_restore = I("c_gbl_fF") * v ** 2 / 2
    e_samples = 2 * I("c_gbl_fF") * I("v_sample_swing_V") * v
    e_ms = (e_lbl + e_gbl_restore + e_samples + I("e_comp_fJ")) / I("reg_eff")
    p(f"- Conventional 1-beta bitline energy per sensed bit: Cbl x VARY^2/2 / eta = {e_conv:.1f} fJ (A1 convention).")
    p(f"- MARGIN STACK at Cs {cs_plan:.2f} fF: local node {e_lbl:.2f} + GBL restore {e_gbl_restore:.2f} + two CDS samples "
      f"{e_samples:.2f} + comparator {I('e_comp_fJ'):.1f} = **{e_ms:.1f} fJ** ({e_conv/e_ms:.1f}x lower) [ESTIMATE: C_GBL {I('c_gbl_fF')} fF].")
    e_ref_conv = (e_conv + I("e_wl_per_bit_fJ")) * I("periph_factor")
    e_ref_ms = (e_ms + I("e_wl_per_bit_fJ")) * I("periph_factor")
    n = I("cells_16gb")
    p_conv = e_ref_conv * 1e-15 * n / I("t_ref_ddr5_s") * 1e3
    p(f"- Refresh energy per bit incl. WL and x{I('periph_factor'):.0f} periphery: {e_ref_conv:.0f} fJ (1-beta) vs {e_ref_ms:.0f} fJ.")
    p(f"- 16Gb die refresh power: 1-beta at 64 ms = {p_conv:.1f} mW.")
    for cs, (dmax, r10, r100) in sorted(droop_best.items()):
        for lab, r in (("10 aA", r10), ("100 aA", r100)):
            tref = r / I("refresh_guard")
            pw = e_ref_ms * 1e-15 * n / tref * 1e3
            p(f"  - Cs {cs} fF, tail {lab}: refresh every {fmt_t(tref)} -> {pw:.3f} mW ({p_conv/pw:,.0f}x lower)")
    return e_ms, e_conv


# --------------------------------------------------------------------------------------------
# 7. area and cost
# --------------------------------------------------------------------------------------------
def section_cost(cs_plan):
    hr("7. Area, density and cost per bit")
    sites = I("sites_extra_per_seg") + I("sites_strap")
    ovh = sites / I("n_seg")
    dens = I("density_4f2_gb_mm2") / (1 + ovh * 1.0)  # density already includes array eff; overhead is array area
    # careful: only the array part grows
    eff = I("array_eff_4f2_puc")
    die_growth = eff * ovh
    dens = I("density_4f2_gb_mm2") / (1 + die_growth)
    p(f"- Segment overhead: {sites} extra 4F2 sites per {I('n_seg')} cells = {ovh*100:.1f}% of array area; "
      f"die +{die_growth*100:.1f}% at array efficiency {eff}.")
    p(f"- Density: 4F2 VCT (F=14.7 nm, PUC) {I('density_4f2_gb_mm2'):.3f} -> **{dens:.3f} Gb/mm2** "
      f"= {dens/I('density_1b_gb_mm2'):.2f}x 1-beta ({I('density_1b_gb_mm2')} Gb/mm2). MARGIN STACK costs density; it does not add it.")
    r_h = stub_h_nm(cs_plan) / I("cap_h_1b_nm")
    p(f"- Capacitor height {I('cap_h_1b_nm'):.0f} -> {stub_h_nm(cs_plan):.0f} nm (x{r_h:.2f}); AR {I('cap_h_1b_nm')/I('pillar_d_1b_nm'):.0f} -> "
      f"{stub_h_nm(cs_plan)/I('pillar_d_1b_nm'):.1f}. Conformal-ALD exposure scales ~AR^2 [ESTIMATE, Gordon-type model]: "
      f"x{(stub_h_nm(cs_plan)/I('cap_h_1b_nm'))**2:.3f}. No support lattice below AR ~20 [ESTIMATE].")
    p("")
    p("| cap-module share of wafer cost | module saving | net wafer cost | die area | $/bit vs 4F2 baseline | $/GB at $1.48 anchor |")
    p("|---|---|---|---|---|---|")
    res = {}
    for share in (0.10, 0.15, 0.20):
        saving = share * I("cap_height_scaled_frac") * (1 - r_h)
        wafer = 1 - saving + I("added_mask_frac")
        rel = wafer * (1 + die_growth)
        res[share] = rel
        p(f"| {share*100:.0f}% | -{saving*100:.1f}% | {wafer:.3f} | x{1+die_growth:.3f} | {(rel-1)*100:+.1f}% | ${I('cost_ddr5_usd_gb')*rel:.2f} |")
    p("")
    p("Verdict: $/bit is flat (-4% to +4%). The step change is in the capacitor module itself: ~10x less HAR etch depth")
    p("(fluorocarbon/PFAS etch time, He-cooled chuck hours), no support lattice, ~10x less ZrO2/TiN ALD, no k>50 / Ru push,")
    p("and a capacitor short enough to lie in a 3D tier (section 8).")
    return dens, res


# --------------------------------------------------------------------------------------------
# 8. 3D tier
# --------------------------------------------------------------------------------------------
def section_3d(cs_plan):
    hr("8. 3D readiness: lateral capacitor length per tier")
    cpn = c_per_nm_fF(I("lat_cap_d_nm"), I("eot_cap_nm"))
    base_len = 600 - I("lat_fet_len_nm")
    base_cs = base_len * cpn
    p(f"- Lateral cylinder d={I('lat_cap_d_nm'):.0f} nm: {cpn*1e3:.2f} aF/nm. A1's 50x600 nm base cell holds ~{base_cs:.1f} fF in {base_len:.0f} nm.")
    cseg3 = I("c_seg_3d_fF")
    det_fn = lambda cs: kick_terms(cs, cseg3)[2]
    sig = lambda cs: cds_residual(cs, cseg3)["tot"]
    cs3 = solve_local_cs(sig, cseg3, det_fn=det_fn)
    svt1 = sigma_vt_gain_mV(1)
    sig_n = lambda cs: math.sqrt(svt1 ** 2 + kick_terms(cs, cseg3)[1] ** 2 + I("sigma_1f_rtn_mV") ** 2)
    cs3n = solve_local_cs(sig_n, cseg3, det_fn=det_fn)
    p(f"- 16-tier vertical BL segment ~{cseg3} fF: Cs needed {cs3:.2f} fF with CDS, {cs3n:.2f} fF without.")
    p("")
    p("| Cs fF | lateral cap nm | cell nm2 | Gb/mm2 per tier | x A1 base | tiers to match 1-beta (1 amp tier per 16) |")
    p("|---|---|---|---|---|---|")
    base_gb = 1e6 / (I("tier_pitch_nm") * 600 * 1e-6) * I("tier_eff") / 1.0625 / 1e9
    for cs in (base_cs, cs3n, 0.5, cs3):
        L = cs / cpn
        cell = I("tier_pitch_nm") * (I("lat_fet_len_nm") + L)
        gb = 1e6 / (cell * 1e-6) * I("tier_eff") / 1.0625 / 1e9
        tiers = I("density_1b_gb_mm2") / (gb * 16 / 17)
        p(f"| {cs:.2f} | {L:.0f} | {cell:,.0f} | {gb:.4f} | {gb/base_gb:.2f}x | {tiers:.1f} |")
    p("")
    p("The same margin stack that removes the 4F2 HAR pillar cuts the 3D lateral capacitor from ~450 nm to <100 nm, which roughly halves")
    p("the per-tier footprint and the 3D break-even tier count (A1 base ~26 tiers). This is PIXEL-STACK's argument, read by the same chip.")
    return cs3


# --------------------------------------------------------------------------------------------
# 9. timing
# --------------------------------------------------------------------------------------------
def section_timing(cs_plan):
    hr("9. Sense timing")
    cseg = c_seg()
    r_on = (I("vary_ox_V") / 2) / (I("ion_access_uA") * 1e-6)
    tau = r_on * cs_plan * cseg / (cs_plan + cseg) * 1e-15
    gm = 2 * I("i_gain_uA") * 1e-6 / I("vov_gain_V")
    t_int = I("gain_local") * I("c_gbl_fF") * 1e-15 / gm
    t_restore = 3 * (I("c_gbl_fF") + cseg + cs_plan) * 1e-15 * I("vary_ox_V") / (I("ion_access_uA") * 1e-6)
    tot = 5 * tau + 2 * t_int + 0.5e-9 + t_restore
    p(f"- Charge sharing: R_on ~{r_on/1e3:.0f} kOhm x series C -> tau {tau*1e12:.1f} ps (5 tau {5*tau*1e12:.0f} ps).")
    p(f"- Gain stage gm {gm*1e6:.0f} uS: each CDS sample needs {t_int*1e9:.2f} ns for G={I('gain_local')} on {I('c_gbl_fF')} fF.")
    p(f"- Comparator 0.5 ns [ESTIMATE]; write-back 3 tau through the write FET {t_restore*1e9:.2f} ns.")
    p(f"- Total sense+restore ~{tot*1e9:.1f} ns, inside a DDR5 tRCD/tRAS budget (~14/32 ns). IBM's 3T micro-SA eDRAM reported 1.5 ns latency.")
    p("- The delayed second comparison (erasure flag) adds ~0.5-1 ns only on the flag path.")
    return tot


# --------------------------------------------------------------------------------------------
# 10. sensitivity on the key unknown
# --------------------------------------------------------------------------------------------
def section_sensitivity():
    hr("10. Sensitivity on the key unknown: post-CDS residual x data-dependent coupling")
    cseg = c_seg()
    det_fn = lambda cs: kick_terms(cs, cseg)[2]
    alphas = (0.0, 0.05, 0.10, 0.15, 0.20)
    p(f"Required Cs (fF) on a {I('n_seg')}-cell segment (Cseg {cseg:.2f} fF), k = {K_ECC:.2f}, kick det. term included.")
    p("")
    p("| sigma_res mV | " + " | ".join(f"alpha {a}" for a in alphas) + " | stub h nm @alpha 0.1 | cut vs 5.42 @0.1 |")
    p("|---" * (len(alphas) + 3) + "|")
    table = {}
    for sr in (2, 4, 6, 8, 10, 13, 16, 20, 25, 30, 40, 50):
        vals = []
        for a in alphas:
            cs = solve_local_cs(lambda c, sr=sr: sr, cseg, alpha=a, det_fn=det_fn)
            vals.append(cs)
            table[(sr, a)] = cs
        c01 = table[(sr, 0.10)]
        p(f"| {sr} | " + " | ".join(f"{v:.2f}" for v in vals) + f" | {stub_h_nm(c01):.0f} | {I('cs_1b_fF')/c01:.1f}x |")
    # thresholds
    def sig_for(cs_target, a):
        lo, hi = 0.1, 200.0
        for _ in range(80):
            mid = 0.5 * (lo + hi)
            if solve_local_cs(lambda c: mid, cseg, alpha=a, det_fn=det_fn) <= cs_target:
                lo = mid
            else:
                hi = mid
        return lo
    p("")
    thr = {}
    for cs_t in (0.25, 0.5, 1.0):
        vals = [sig_for(cs_t, a) for a in (0.05, 0.10, 0.15, 0.20)]
        thr[cs_t] = vals
        p(f"- Max sigma_res for Cs <= {cs_t} fF: alpha 0.05 -> {vals[0]:.1f} mV, 0.10 -> {vals[1]:.1f}, 0.15 -> {vals[2]:.1f}, 0.20 -> {vals[3]:.1f} mV")
    p("")
    p("Segment length (central CDS residual, alpha 0.1):")
    p("")
    p("| cells/segment | Cseg fF | Cs needed fF | stub h nm | array overhead | die growth | density Gb/mm2 |")
    p("|---|---|---|---|---|---|---|")
    for n in (8, 16, 32, 64, 128):
        cs_n = c_seg(n=n)
        det_n = lambda cs, cs_n=cs_n: kick_terms(cs, cs_n)[2]
        sig = lambda cs, cs_n=cs_n: cds_residual(cs, cs_n)["tot"]
        need = solve_local_cs(sig, cs_n, det_fn=det_n)
        ovh = (I("sites_extra_per_seg") + I("sites_strap")) / n
        dg = I("array_eff_4f2_puc") * ovh
        p(f"| {n} | {cs_n:.2f} | {need:.2f} | {stub_h_nm(need):.0f} | {ovh*100:.1f}% | {dg*100:.1f}% | {I('density_4f2_gb_mm2')/(1+dg):.3f} |")
    p("")
    p("Short segments shrink Cseg but make the kick larger relative to the signal and cost area; 32-64 cells is the sweet spot.")
    return thr


# --------------------------------------------------------------------------------------------
# 11. MPW statistics and budget
# --------------------------------------------------------------------------------------------
BUDGET = [
    ("DRAM Bender error-tail study (shared with RAW-BER CONTRACT): 2 FPGA boards, DDR4/DDR5 parts, thermal rigs, 0.5 FTE x 6 mo", 80000, "M0-6"),
    ("Pre-silicon: SPICE Monte Carlo, TCAD for kick/coupling on VCT geometry (partner licence or startup TCAD seat)", 30000, "M0-4"),
    ("22FDX MPW, ~6 mm2 at $17,997/mm2 (CMC listing) + 20% U.S.-route premium", 130000, "M7 tape-out"),
    ("EDA/PDK access (startup or university-partner programme)", 25000, "M2-7"),
    ("Layout/verification contractor (custom 0.125-1 fF MOM stubs, BIST)", 45000, "M3-7"),
    ("Packages, PCBs, sockets, probe cards", 30000, "M9-11"),
    ("Test bench: SMUs, thermal forcer (used), FPGA controller, low-noise sampling front end", 60000, "M6-11"),
    ("IGZO FET + 0.5 fF MIM coupons on the shared oxide run (cleanroom ~400 h, staff assist, targets, wafers, 2T leakage readout)", 120000, "M3-12"),
    ("Second MPW spin or 22FDX re-spin with fixes (contingent on M14 data)", 110000, "M15-22"),
    ("IP: 2 provisionals, 1 PCT, freedom-to-operate search", 45000, "M2, M10, M14"),
    ("Two founders, lean salaries ($5k/month each x 24 months)", 240000, "M0-24"),
    ("Overhead: insurance, travel to fabs/conferences, accounting, legal", 40000, "M0-24"),
]


def section_mpw(target_fail):
    hr("11. Decisive-experiment statistics and budget check")
    cells = 64 * 1024 * I("n_seg")
    chips = I("mpw_chips_tested")
    p(f"- Test chip: 64k emulated segments x {I('n_seg')} cells = {cells/1e6:.1f}M cells/chip; {chips} chips -> {cells*chips/1e6:.0f}M cells.")
    p(f"- Direct one-sided tail coverage: Q^-1(1/N) = {Qinv(1/(cells*chips)):.2f} sigma (raw BER 1e-4 needs only {K_ECC:.2f}).")
    p(f"- At raw BER 1e-4 one full-array read yields ~{cells*1e-4:.0f} errors/chip; 1,000 reads per condition -> "
      f"{cells*1e-4*1000:,.0f} errors: enough to test iid-ness along {cells//I('ecc_n'):,} row codewords per chip.")
    p(f"- Per-cell margin maps: sweep a calibrated charge injection / Vpre offset in 64 steps per cell to get each cell's flip point;")
    p(f"  fit the distribution and check the tail against Gaussian to 5 sigma (~3e-7) on the {chips}-chip population.")
    p(f"- MPW silicon: {I('mpw_area_mm2')} mm2 x ${I('mpw_usd_mm2'):,.0f}/mm2 = ${I('mpw_area_mm2')*I('mpw_usd_mm2'):,.0f} (CMC 22FDX listing; 100 untested dies).")
    p("")
    p("| item | $ | when |")
    p("|---|---|---|")
    tot = 0
    for name, usd, when in BUDGET:
        tot += usd
        p(f"| {name} | {usd:,} | {when} |")
    p(f"| **Total** | **{tot:,}** | 24 months |")
    p("")
    exp_only = sum(u for n, u, w in BUDGET if "founders" not in n.lower() and "overhead" not in n.lower())
    p(f"Experiments alone: ${exp_only:,}. Within the $1M seed: {'YES' if tot <= 1_000_000 else 'NO'} (headroom ${1_000_000-tot:,}).")
    return tot


# --------------------------------------------------------------------------------------------
# 12. GO / NO-GO
# --------------------------------------------------------------------------------------------
def section_go(thr, s_flag, ber_res, cs_cases, droop):
    hr("12. GO / NO-GO")
    sig05 = thr[0.5][1]
    sig025 = thr[0.25][1]
    sig1 = thr[1.0][1]
    imax64 = 0.5e-15 * droop * 1e-3 / I("t_ref_ddr5_s") * 1e18
    imax_10x = imax64 / 10
    b80 = ber_res[(0.8, 0.0)]
    b_pair = ber_res[(0.8, 0.01)]
    p(f"Headline: central post-CDS residual {cds_residual(0.25, c_seg())['tot']:.1f} mV -> sensing-limited Cs "
      f"{cs_cases['central']:.2f} fF (range {cs_cases['optimistic']:.2f}-{cs_cases['pessimistic']:.2f}); planning Cs 0.5 fF "
      f"(set by the IGZO leakage tail, not by sensing): a {I('cs_1b_fF')/0.5:.1f}x cut, {stub_h_nm(0.5):.0f} nm stub, "
      f"AR {stub_h_nm(0.5)/I('pillar_d_1b_nm'):.1f}, {0.5e-15*0.5/QE:,.0f} stored electrons vs 17,762.")
    p("")
    p(f"**GO/NO-GO:** GO if the 22FDX MPW, at 85 C under worst-case neighbour data on 32-cell segments, shows a post-CDS "
      f"input-referred residual <= {sig05:.0f} mV (coupling folded in), i.e. raw BER <= 1e-4 at Cs = 0.5 fF for iid errors "
      f"(<= {b80:.1e} if >= 80% are flaggable; <= {sig025:.0f} mV unlocks 0.25 fF); AND the DRAM Bender/MPW error maps show "
      f"< 1% of errors as same-codeword pairs (at 1% pairs the allowed BER already falls to {ber_res[(0.0,0.01)]:.0e}); AND the IGZO "
      f"coupons extrapolate a 1-in-1e10 85 C leakage tail <= {imax64:.0f} aA at 0.5 fF (DDR5 64 ms parity; <= {imax_10x:.0f} aA "
      f"for a 10x refresh cut). NO-GO if the residual exceeds {sig1:.0f} mV (Cs stays >= 1 fF, a ~5x cut that a 4-pillar gain FET "
      f"without CDS already gives), or if pairs exceed ~10% of errors (allowed BER {ber_res[(0.0,0.1)]:.0e}, margin lost).")


def main():
    section_inputs()
    cbl = section_baseline()
    scen = section_residual()
    cs_cases, rows = section_cases(cbl, scen)
    s_flag, ber_res, target = section_ecc()
    droop, best = section_retention(cs_cases["central"])
    cs_plan = 0.5
    section_energy(cs_plan, cbl, best)
    section_cost(cs_plan)
    section_3d(cs_plan)
    section_timing(cs_plan)
    thr = section_sensitivity()
    section_mpw(target)
    section_go(thr, s_flag, ber_res, cs_cases, droop)
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.normpath(os.path.join(here, "..", "research", "stage3", "margin-stack_model_output.md"))
    with open(out, "w") as f:
        f.write("\n".join(OUT) + "\n")
    print(f"\n[wrote {out}]")


if __name__ == "__main__":
    main()
