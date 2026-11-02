#!/usr/bin/env python3
"""
raw-ber-contract.py -- first-principles model of the RAW-BER CONTRACT concept (Stage 3 dossier, rank 4).

Owner: dos-raw-ber-contract (dram-moonshot). Written 2026-11-02. Pure standard library.
Run from /home/user/VirtualWorkplaceStudio/dram-moonshot:   python3 models/raw-ber-contract.py
Writes research/stage3/raw-ber-contract_model_output.md and prints the same text. Exits 0.

What it computes (sections):
  0. The uncorrectable-error (UE) target per 64 B codeword read, derived from a module UE budget.
  1. Code budgets for iid raw errors: line BCH, the 128 check bits a commodity DDR5 ECC RDIMM already
     carries, DDR5 on-die SEC in front of a controller code, and 4 KB page codes (vs the Shannon bound).
  2. Margin: what raw BER buys in sense-signal sigma, mV and storage-capacitor fF.
  3. Erasure flags (the key unknown): flagged share and false-flag rate of margin errors, the
     refresh-latching argument for retention errors, and decoder failure for hard / erase-all / GMD /
     Chase decoding, as a function of the confident (unflaggable) error share.
  4. Correlated bursts: how much multi-bit clustering a t=12 line code survives.
  5. Relaxed refresh on commodity DRAM: retention-tail models, VRT accumulation, scrub, refresh power,
     tRFC loss, and the largest refresh interval the 128-bit side band allows.
  6. The single error budget: margin and refresh relaxation are alternative spends, not additive.
  7. Row hammer under relaxed refresh (RFM substitution), typed pages (page-code RMW, decode energy).
  8. Value: energy $, bandwidth, density cost of check bits, vs $1.48/GB and 0.447 Gb/mm2.
  9. GO / NO-GO thresholds for the decisive experiment.

Every input carries a source URL or "ESTIMATE: basis". Sources: research/sources/dos-raw-ber-contract.jsonl.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import dram_cell_physics as dcp  # noqa: E402  (reuse A1 bitline/refresh physics)

ROOT = os.path.dirname(HERE)
OUT_MD = os.path.join(ROOT, "research", "stage3", "raw-ber-contract_model_output.md")

# --------------------------------------------------------------------------------------------
# INPUTS: (value, source or "ESTIMATE: basis")
# --------------------------------------------------------------------------------------------
INPUTS = {
    # --- reliability target ---
    "module_GB": (64.0, "ESTIMATE: canonical 64 GB DDR5 RDIMM used throughout dram-moonshot A1 (40 x 16Gb dies)"),
    "avg_bw_GBps": (10.0, "ESTIMATE: ~25% of a DDR5-4800 channel peak (38.4 GB/s) averaged over a server day"),
    "ue_budget_per_module_yr": (1e-3, "ESTIMATE: field DIMM UE rates are ~0.2-1%/yr and dominated by hard faults "
                                      "[UNVERIFIED: training knowledge, Schroeder 2009 / Sridharan field studies]; the "
                                      "random-raw-BER share must stay <=0.1%/yr per module"),
    # --- codes ---
    "line_data_bits": (512, "64 B cache line"),
    "bch_m_line": (10, "binary BCH over GF(2^10): n <= 1023 covers 512 + up to 51 x 10 check bits"),
    "page_data_bits": (32768, "4 KB OS page"),
    "bch_m_page": (16, "binary BCH over GF(2^16) for 4 KB codewords"),
    "rdimm_sideband_bits": (128, "ESTIMATE/derivation: DDR5 RDIMM subchannel = 32 data + 8 ECC bits, BL16 -> "
                                 "512 data + 128 check bits per 64 B line [UNVERIFIED: JESD79-5 organisation, training knowledge]"),
    "ondie_n": (136, "DDR5 on-die SEC (136,128); A1 model ecc_factor 1.0625 [REPORTED, JESD79-5 per prior work]"),
    "ondie_miscorrect": (0.53, "ESTIMATE: shortened Hamming(136,128): a 2-bit error yields a syndrome matching one of "
                               "136 of 255 nonzero columns ~0.53 of the time -> a 3rd bit flipped (cf. BEER/HARP, "
                               "https://arxiv.org/pdf/2204.10387)"),
    "chip_slice_bits": (64, "ESTIMATE: x4 DDR5 chip delivers 4 x BL16 = 64 bits per line; 10 chips per line"),
    "chips_per_line": (10, "8 data + 2 ECC x4 chips per DDR5 RDIMM subchannel (same basis as rdimm_sideband_bits)"),
    # --- margin ---
    "dv_baseline_mV": (50.0, "A1 model dv_min_mV (models/dram_cell_physics.py) = SA offset + coupling + guard"),
    "sigma_baseline": (7.0, "FINAL_CONCEPTS.json raw-ber-contract: today's budget sits at ~7 sigma (1.7e10 cells, "
                            "on-die SEC as backup)"),
    # --- flags ---
    "flag_window_sigma": (0.5, "ESTIMATE: reduced-tRCD second sample mis-resolves bits within ~0.5 sigma (~3.6 mV) of "
                               "threshold; Solar-DRAM shows reduced-tRCD failures mark weak cells "
                               "(https://people.cs.rutgers.edu/~mp2099/files/kim_iccd18_solar_paper.pdf)"),
    "chase_max_flags": (8, "ESTIMATE: Chase-II over <=8 flagged positions = <=256 trial BCH decodes, slow path only"),
    "burst_size": (3, "ESTIMATE: on-die-SEC miscorrection turns 2 raw errors into 3 in one chip word"),
    # --- retention / refresh ---
    "ret_anchor_ber_64ms": (3.6e-9, "B4 card02 calibration (research/phaseB/B4-architecture.json): RAIDR-era '~1,000 "
                                    "cells per 32 GB below 256 ms' with a 4x temperature derate to 85 C "
                                    "(https://www.pdl.cmu.edu/ftp/NVM/raidr-isca12.pdf)"),
    "ret_anchor_ber_32ms": (1.1e-10, "ESTIMATE: RAIDR-era '~30 cells per 32 GB below 128 ms', same 4x derate; with the "
                                     "64 ms anchor this fixes a lognormal tail (sigma_ln ~1.24)"),
    "ret_pow_k": (3.0, "B4 card02 power-law tail exponent (BER ~ t^3), optimistic case"),
    "data_pattern_factor": (0.5, "ESTIMATE: random data charges ~half the cells; only charged cells leak"),
    "vrt_growth_per_day": (1.0, "ESTIMATE: VRT cells latch new errors at ~1x the static BER per day of no scrub "
                                "(REAPER: retention changes dynamically, https://people.cs.rutgers.edu/~mp2099/files/"
                                "patel_isca2017_reach_paper.pdf; B4 used x3 accumulation). Swept 0.1-10."),
    "scrub_interval_h": (1.0, "ESTIMATE: design choice, swept"),
    "e_scrub_pJ_bit": (3.0, "ESTIMATE: sequential open-page read inside the CXL device: IO ~2 pJ + array share + syndrome"),
    "e_refresh_fJ_bit": (None, "A1 model refresh_energy_per_bit_fJ() (models/dram_cell_physics.py), ~46 fJ"),
    "trefi_ns": (3900.0, "DDR5 tREFI <85 C (https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/7134/"
                         "SQR-RD5N16G5K6HZZG.pdf via A1)"),
    "trfc_ns": ({"16Gb": 295.0, "32Gb": 410.0, "64Gb": 1600.0},
                "A1 model: 16Gb datasheet; 32Gb [UNVERIFIED]; 64Gb extrapolated (https://arxiv.org/pdf/1712.08304)"),
    "rdimm_idle_W": (3.0, "A1 model [UNVERIFIED: training knowledge, 2-4 W class]"),
    "rdimm_active_W": (12.0, "A1 model [UNVERIFIED: training knowledge, 8-15 W class]"),
    # --- hammer ---
    "tRC_ns": (46.0, "ESTIMATE: DDR5 tRC ~46-48 ns [UNVERIFIED: training knowledge]"),
    "hc_first": (1000.0, "A1 section 9: HCfirst ~0.5-1K by 2026 [extrapolated]"),
    "raaimt": (40.0, "ESTIMATE: DDR5 RFM rolling-ACT threshold of order 32-80 per bank [UNVERIFIED]"),
    "tRFM_ns": (150.0, "ESTIMATE: same-bank RFM ~ half an all-bank tRFC"),
    "act_rate_typ_per_bank": (1e6, "ESTIMATE: ~1 ACT/us per bank for a busy server bank (row-buffer hits included)"),
    # --- page codes / typed pages ---
    "e_page_decode_pJ_bit": (1.0, "ESTIMATE: Stage-2 critic of I-07888 (~1 pJ/bit soft LDPC)"),
    "e_line_decode_pJ_bit": (0.05, "ESTIMATE: syndrome-only fast path for line BCH in 28 nm"),
    # --- value ---
    "ddr5_cost_per_GB": (1.48, "ram-venture models/dram_cost_stack.py (1-beta $3.8k wafer), via A1"),
    "density_1b_Gb_mm2": (0.447, "A1: Micron D1b 16Gb 35.83 mm2 teardown via ram-venture cost_stack"),
    "elec_usd_kWh": (0.10, "ESTIMATE: U.S. industrial/data-centre electricity"),
    "pue": (1.3, "ESTIMATE: hyperscale PUE"),
    "years": (5.0, "ESTIMATE: server life"),
}


def V(k):
    return INPUTS[k][0]


LINES = []


def out(s=""):
    print(s)
    LINES.append(s)


def hr(t):
    out("")
    out("## " + t)
    out("")


# --------------------------------------------------------------------------------------------
# Math helpers
# --------------------------------------------------------------------------------------------
def Q(x):
    return 0.5 * math.erfc(x / math.sqrt(2.0))


def Qinv(p):
    lo, hi = -10.0, 38.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if Q(mid) > p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def pois_pmf(lam, kmax):
    if lam <= 0:
        return [1.0] + [0.0] * kmax
    return [math.exp(-lam + k * math.log(lam) - math.lgamma(k + 1)) for k in range(kmax + 1)]


def pois_sf(a, lam):
    """P(X > a) for X ~ Poisson(lam); exact summation of the upper tail."""
    if a < 0:
        return 1.0
    if lam <= 0:
        return 0.0
    a = int(a)
    start = a + 1
    span = int(12 * math.sqrt(lam) + 80)
    s = 0.0
    for k in range(start, start + span):
        s += math.exp(-lam + k * math.log(lam) - math.lgamma(k + 1))
    if lam > start:  # tail sum misses the bulk when a is below the mean
        lo = sum(math.exp(-lam + k * math.log(lam) - math.lgamma(k + 1)) for k in range(0, start))
        return max(0.0, 1.0 - lo)
    return s


def conv(a, b, kmax):
    c = [0.0] * (kmax + 1)
    for i, x in enumerate(a):
        if x == 0.0:
            continue
        for j, y in enumerate(b):
            if i + j > kmax:
                break
            c[i + j] += x * y
    return c


def compound_burst_pmf(lam_events, b, kmax):
    """Number of errors from Poisson(lam_events) bursts of exactly b bits."""
    ev = pois_pmf(lam_events, kmax // max(b, 1) + 1)
    p = [0.0] * (kmax + 1)
    for n, w in enumerate(ev):
        if n * b <= kmax:
            p[n * b] += w
    return p


def H2(p):
    return -p * math.log2(p) - (1 - p) * math.log2(1 - p)


# --------------------------------------------------------------------------------------------
# 0. UE target
# --------------------------------------------------------------------------------------------
def section_target():
    hr("0. Uncorrectable-error target per 64 B codeword read")
    reads_per_s = V("avg_bw_GBps") * 1e9 / 64
    reads_per_yr = reads_per_s * 3.156e7
    tgt = V("ue_budget_per_module_yr") / reads_per_yr
    out(f"Reads: {V('avg_bw_GBps'):.0f} GB/s / 64 B = {reads_per_s:.3g} lines/s = {reads_per_yr:.3g} lines/yr per module")
    out(f"Module UE budget {V('ue_budget_per_module_yr'):.0e}/yr -> target codeword failure <= {tgt:.2g} per read")
    p_concept = 2e-17
    out(f"Concept's t=8 figure (~2e-17 per read) would give {p_concept*reads_per_yr:.2g} UE per module-year "
        f"({p_concept*reads_per_yr*100:.0f}%/yr): too loose by ~{p_concept/tgt:.0f}x. Corrected target used below.")
    return tgt


# --------------------------------------------------------------------------------------------
# 1. Code budgets for iid errors
# --------------------------------------------------------------------------------------------
def min_t_hard(p, kbits, m, tgt, tmax=2000):
    for t in range(0, tmax + 1):
        n = kbits + m * t
        if pois_sf(t, n * p) <= tgt:
            return t
    return None


def max_p_hard(t, kbits, m, tgt):
    lo, hi = -9.0, -1.0
    for _ in range(60):
        mid = (lo + hi) / 2
        n = kbits + m * t
        if pois_sf(t, n * 10 ** mid) <= tgt:
            lo = mid
        else:
            hi = mid
    return 10 ** lo


def ondie_slice_pmf(p, kmax=40):
    """Errors delivered in one x4 chip's 64-bit slice after DDR5 on-die SEC(136,128)."""
    n = int(V("ondie_n"))
    mis = V("ondie_miscorrect")
    frac = V("chip_slice_bits") / n
    raw = pois_pmf(n * p, 30)
    res = [0.0] * (kmax + 1)
    for j, w in enumerate(raw):
        if w < 1e-300:
            continue
        if j <= 1:
            res[0] += w
            continue
        # j raw + miscorrected bit with prob mis; each erroneous bit lands in our slice w.p. frac
        for tot, wt in ((j, 1 - mis), (j + 1, mis)):
            for k in range(0, min(tot, kmax) + 1):
                res[k] += w * wt * math.comb(tot, k) * frac ** k * (1 - frac) ** (tot - k)
    return res


def line_pmf_ondie(p, kmax=40):
    s = ondie_slice_pmf(p, kmax)
    tot = [1.0] + [0.0] * kmax
    for _ in range(int(V("chips_per_line"))):
        tot = conv(tot, s, kmax)
    return tot


def max_p_ondie(t, tgt):
    lo, hi = -7.0, -1.5
    for _ in range(50):
        mid = (lo + hi) / 2
        pm = line_pmf_ondie(10 ** mid)
        fail = sum(pm[t + 1:])
        if fail <= tgt:
            lo = mid
        else:
            hi = mid
    return 10 ** lo


def section_codes(tgt):
    hr("1. Code budgets for iid raw errors")
    k, m = V("line_data_bits"), V("bch_m_line")
    out("Line code: binary BCH over 512 data bits (m=10). Minimum t meeting the target, and parity:")
    out("")
    out("| raw BER | t | check bits | parity % | P(fail) at t |")
    out("|---|---|---|---|---|")
    res = {}
    for p in (1e-6, 1e-5, 3e-5, 1e-4, 3e-4, 1e-3):
        t = min_t_hard(p, k, m, tgt)
        n = k + m * t
        res[p] = t
        out(f"| {p:.0e} | {t} | {m*t} | {m*t/k*100:.1f} | {pois_sf(t, n*p):.1e} |")
    t8 = pois_sf(8, (k + 80) * 1e-4)
    out("")
    out(f"Check: t=8 at 1e-4 fails {t8:.1e} per read (concept: ~2e-17, matches). Corrected target needs "
        f"t={res[1e-4]} ({m*res[1e-4]} bits, {m*res[1e-4]/k*100:.1f}%).")
    sb = int(V("rdimm_sideband_bits"))
    t_sb = sb // m
    p_sb = max_p_hard(t_sb, k, m, tgt)
    out("")
    out(f"Commodity DDR5 ECC RDIMM side band: {sb} check bits per line -> binary BCH t={t_sb} "
        f"(gives up chipkill). Max iid raw BER at target: {p_sb:.2e}.")
    p_od = max_p_ondie(t_sb, tgt)
    out(f"Same t={t_sb} controller code behind DDR5 on-die SEC(136,128) with miscorrection: max internal raw BER "
        f"{p_od:.2e} (on-die SEC removes singles but turns doubles into 2-3 bit bursts per chip).")
    # page code
    kp, mp = V("page_data_bits"), V("bch_m_page")
    out("")
    out("4 KB page code (binary BCH, m=16) vs the binary-symmetric-channel (Shannon) parity floor:")
    out("")
    out("| raw BER | t | parity % (BCH) | Shannon floor % | ")
    out("|---|---|---|---|")
    for p in (1e-4, 1e-3, 1e-2):
        t = min_t_hard(p, kp, mp, tgt)
        cap = 1 - H2(p)
        out(f"| {p:.0e} | {t} | {mp*t/kp*100:.2f} | {(1/cap-1)*100:.2f} |")
    out("")
    out("Reading: at 1e-4 the 4 KB code needs only ~1-2% parity, but the line code already fits in the 25% side band "
        "a commodity ECC RDIMM carries, so relaxed refresh on today's DRAM needs no page code at all for iid errors.")
    return p_sb, p_od, res


# --------------------------------------------------------------------------------------------
# 2. Margin
# --------------------------------------------------------------------------------------------
def c1b_fF():
    I = dcp.INPUTS
    d_cx = I["user_gbit"] / I["die_cxmt_g4_mm2"]
    d_1b = I["user_gbit"] / I["die_1b_mm2"]
    cell_1b = I["cell_cxmt_g4_um2"] * d_cx / d_1b
    p = dcp.hex_pitch_nm(cell_1b)
    return dcp.cap_pillar_fF(p - I["cap_gap_nm"], I["cap_height_nm"], I["eot_nm"])


def margin_setup():
    I = dcp.INPUTS
    c1 = c1b_fF()
    cbl = dcp.c_bitline_fF(I["cells_per_bl"])
    vpre = I["v_array"] / 2
    v1min = vpre + V("dv_baseline_mV") / 1e3 * (c1 + cbl) / c1
    f = (I["v_array"] - v1min) / I["v_array"]
    vs_f = (1 - f) * I["v_array"] - vpre
    return c1, cbl, vs_f, f


def cs_for_dv(dv_mV):
    c1, cbl, vs_f, _ = margin_setup()
    return dcp.cs_min_fF(cbl, dv_mV, vs_f)


def section_margin(tgt):
    hr("2. Margin: what a raw-BER budget buys at the sense amp")
    sig = V("dv_baseline_mV") / V("sigma_baseline")
    c1, cbl, vs_f, f = margin_setup()
    out(f"Baseline: {V('dv_baseline_mV'):.0f} mV = {V('sigma_baseline'):.0f} sigma -> sigma_eff = {sig:.2f} mV; "
        f"1b Cs (A1 geometry) = {c1:.2f} fF on Cbl = {cbl:.1f} fF; same droop allowance ({f*100:.0f}% of VARY) kept.")
    out("")
    out("| raw BER (all margin errors) | z (sigma) | dV needed mV | Cs needed fF | Cs / 1b | pillar height nm |")
    out("|---|---|---|---|---|---|")
    rows = {}
    for p in (1e-12, 1e-9, 1e-6, 1e-5, 1e-4, 3e-4, 1e-3):
        z = Qinv(p)
        dv = z * sig
        cs = cs_for_dv(dv)
        h = dcp.INPUTS["cap_height_nm"] * cs / c1
        rows[p] = (z, dv, cs)
        out(f"| {p:.0e} | {z:.2f} | {dv:.1f} | {cs:.2f} | {cs/c1:.2f} | {h:.0f} |")
    z4 = rows[1e-4][0]
    out("")
    out(f"7 -> {z4:.2f} sigma at 1e-4: dV falls {V('sigma_baseline')/z4:.2f}x (concept: 1.88x). "
        f"1e-4 -> 1e-3 buys only {rows[1e-4][2]/rows[1e-3][2]:.2f}x more Cs (Gaussian tails).")
    return sig, rows


# --------------------------------------------------------------------------------------------
# 3. Erasure flags and decoders
# --------------------------------------------------------------------------------------------
KMAX = 45


def flag_rates(p, conf_frac, delta):
    """Per-bit rates: flagged errors, unflagged soft errors, false flags (correct but flagged)."""
    p_soft = (1 - conf_frac) * p
    if p_soft <= 0:
        return 0.0, 0.0, 0.0
    s = Qinv(p_soft)
    p_ef = Q(s) - Q(s + delta)
    p_eu = Q(s + delta)
    p_ff = Q(s - delta) - Q(s)
    return p_ef, p_eu, p_ff


def fail_probs(p, t, conf_frac, delta, burst_frac=0.0, b=3, kbits=512, m=10, fmax=8):
    n = kbits + m * t
    p_ef, p_eu, p_ff = flag_rates(p, conf_frac, delta)
    p_conf = conf_frac * p
    lam_ef = n * p_ef
    lam_ec_iid = n * (p_eu + (1 - burst_frac) * p_conf)
    lam_b = n * burst_frac * p_conf / b
    lam_ff = n * p_ff
    pec = conv(pois_pmf(lam_ec_iid, KMAX), compound_burst_pmf(lam_b, b, KMAX), KMAX)
    pef = pois_pmf(lam_ef, KMAX)
    sf_cache = {}

    def sf(a):
        if a not in sf_cache:
            sf_cache[a] = pois_sf(a, lam_ff)
        return sf_cache[a]

    hard = era = gmd = chase = 0.0
    for ec in range(KMAX + 1):
        wc = pec[ec]
        if wc < 1e-280:
            continue
        for ef in range(KMAX + 1 - ec):
            w = wc * pef[ef]
            if w < 1e-280:
                continue
            A = 2 * t - 2 * ec - ef
            se = sf(A)
            era += w * se
            if ec + ef > t:
                hard += w
                gmd += w * se
                if ec > t:
                    chase += w * se
                else:
                    chase += w * sf(max(A, fmax - ef))
    return hard, era, gmd, chase


def min_t_strategy(p, conf_frac, delta, tgt, strat, burst_frac=0.0, b=3):
    idx = {"hard": 0, "erase-all": 1, "GMD": 2, "Chase": 3}[strat]
    for t in range(1, 50):
        if fail_probs(p, t, conf_frac, delta, burst_frac, b)[idx] <= tgt:
            return t
    return None


def max_p_strategy(t, conf_frac, delta, tgt, strat, burst_frac=0.0, b=3):
    idx = {"hard": 0, "erase-all": 1, "GMD": 2, "Chase": 3}[strat]
    lo, hi = -8.0, -1.5
    for _ in range(34):
        mid = (lo + hi) / 2
        if fail_probs(10 ** mid, t, conf_frac, delta, burst_frac, b)[idx] <= tgt:
            lo = mid
        else:
            hi = mid
    return 10 ** lo


def section_flags(tgt, sig):
    hr("3. Erasure flags: the key unknown, modelled")
    out("Physics of the flag. A second, earlier sample (reduced tRCD, or a delayed-latch SA) mis-resolves bits whose "
        "|dV| is inside a window delta. Two consequences the concept text misses:")
    out("")
    out("(a) False flags. Errors live in a density tail that rises toward the mean, so more correct bits sit just "
        "above threshold than wrong bits just below. Margin errors (Gaussian, signal at z sigma):")
    out("")
    out("| delta (sigma) | delta mV | flagged share of errors | false flags per error | flags per 592-b codeword at 1e-4 |")
    out("|---|---|---|---|---|")
    for d in (0.25, 0.5, 1.0, 1.5):
        p_ef, p_eu, p_ff = flag_rates(1e-4, 0.0, d)
        out(f"| {d:.2f} | {d*sig:.1f} | {p_ef/1e-4*100:.0f}% | {p_ff/1e-4:.1f} | {592*(p_ef+p_ff):.2f} |")
    out("")
    out("False flags outnumber caught errors 1.6-130x. An erased bit costs 1 unit of distance against 2 for an "
        "unflagged error, so in the deep tail (target 2e-19) erasures still win while the flag window is narrow "
        "(delta ~0.25-0.5 sigma, <0.4 flags per codeword); at delta >=1.5 sigma the false flags eat the gain. The "
        "best use is soft information: hard-decode first, then erase or Chase-flip the few flagged positions "
        "(<=8 here: <=256 trial decodes on a slow path that <1e-10 of reads take).")
    out("")
    out("(b) Refresh latching. A retention error that occurs before the next refresh is sensed as the wrong value and "
        "restored to a full, confident rail. For long-resident data, retention and VRT errors are therefore almost all "
        "confident (unflaggable). Only bits read within their first refresh period after a write can be caught near "
        "threshold, with flagged share 1-(1+r)^-k (r = window / full bitline swing ~0.05-0.2, k = tail slope ~3-5): "
        f"{(1-1.05**-3)*100:.0f}-{(1-1.2**-5)*100:.0f}%. Flags are a margin-error tool (new cells), not a refresh tool.")
    out("")
    d = V("flag_window_sigma")
    out(f"Decoder comparison at raw BER 1e-4, delta = {d} sigma, 512 data bits, BCH m=10, target {tgt:.1e}: minimum t "
        "(check bits = 10 t) versus the confident (unflaggable) share of errors. THIS IS THE SENSITIVITY TABLE ON THE "
        "KEY UNKNOWN.")
    out("")
    out("| confident share | hard t | erase-all t | GMD t | Chase t | Chase check bits | max raw BER at t=8 (Chase) | dV at that BER (mV) | Cs fF |")
    out("|---|---|---|---|---|---|---|---|---|")
    table = {}
    for c in (0.0, 0.1, 0.25, 0.5, 0.75, 1.0):
        th = min_t_strategy(1e-4, c, d, tgt, "hard")
        te = min_t_strategy(1e-4, c, d, tgt, "erase-all")
        tg = min_t_strategy(1e-4, c, d, tgt, "GMD")
        tc = min_t_strategy(1e-4, c, d, tgt, "Chase")
        pmax = max_p_strategy(8, c, d, tgt, "Chase")
        # margin set by the soft (Gaussian) share of errors
        # (confident errors consume budget but bank no margin; c=1 leaves today's 7-sigma design)
        p_soft = max((1 - c) * pmax, 1e-12)
        dv = Qinv(p_soft) * sig
        cs = cs_for_dv(dv)
        table[c] = (th, te, tg, tc, pmax, dv, cs)
        out(f"| {c:.2f} | {th} | {te} | {tg} | {tc} | {10*tc} | {pmax:.2e} | {dv:.1f} | {cs:.2f} |")
    out("")
    th0 = table[0.0]
    p_hard8 = max_p_strategy(8, 0.0, d, tgt, "hard")
    dv_hard8 = Qinv(p_hard8) * sig
    out(f"Reading: with every error flaggable, Chase cuts check bits {table[1.0][0]*10} -> {th0[3]*10} "
        f"({table[1.0][0]/th0[3]:.2f}x) and lets a t=8 code run at {th0[4]:.1e} raw BER instead of {p_hard8:.1e} "
        f"(hard): dV {dv_hard8:.1f} -> {th0[5]:.1f} mV, i.e. flags add ~{(dv_hard8/th0[5]-1)*100:.0f}% on top of the "
        f"code's 1.88x. With half the errors confident the saving shrinks to {table[1.0][0]*10} -> "
        f"{table[0.5][3]*10} bits; with all confident, flags are worth nothing and no margin is banked (the "
        "confident errors consume the budget). The concept's 'd=5 code, 3.9%' for 4 erasures ignores false flags "
        "and the realistic target.")
    # delta optimisation
    out("")
    out("Flag-window optimisation (all errors soft, raw BER 1e-4): Chase t vs delta")
    out("")
    out("| delta (sigma) | Chase t | max raw BER at t=8 |")
    out("|---|---|---|")
    for dd in (0.25, 0.5, 1.0, 1.5):
        out(f"| {dd:.2f} | {min_t_strategy(1e-4, 0.0, dd, tgt, 'Chase')} | "
            f"{max_p_strategy(8, 0.0, dd, tgt, 'Chase'):.2e} |")
    return table


# --------------------------------------------------------------------------------------------
# 4. Bursts
# --------------------------------------------------------------------------------------------
def max_p_rs(tgt, t_sym=8, n_sym=80, burst_frac=0.0, b=3, erased=0):
    """RS over GF(2^8) bytes in the same 128-bit side band (RS(80,64)): corrects t_sym symbol errors, or
    e errors + f erasures with 2e+f <= 2 t_sym. Bursts assumed confined to one byte (optimistic)."""
    e_max = (2 * t_sym - erased) // 2
    nbits = (n_sym - erased) * 8
    lo, hi = -9.0, -1.5
    for _ in range(60):
        mid = (lo + hi) / 2
        p = 10 ** mid
        lam = nbits * p * (1 - burst_frac) + nbits * p * burst_frac / b
        if pois_sf(e_max, lam) <= tgt:
            lo = mid
        else:
            hi = mid
    return 10 ** lo


def section_bursts(tgt):
    hr("4. Correlated bursts: how much clustering a line code survives")
    out("All errors confident (relaxed-refresh regime); a share of error bits arrives as bursts of b bits inside "
        "one 64 B codeword (b=3: on-die-SEC miscorrection or a 3-bit cluster; b=8: sub-wordline/MAT segment). "
        "Binary BCH t=12 vs RS(80,64) over bytes in the same 128-bit side band (RS: bursts assumed inside one byte; "
        "RS also corrects one fully dead x4 chip = 8 byte erasures, i.e. keeps chipkill).")
    out("")
    out("| burst share of error bits | b | max raw BER, BCH t=12 | max raw BER, RS t=8 | RS with one chip erased |")
    out("|---|---|---|---|---|")
    res = {}
    for b in (3, 8):
        for bf in (0.0, 0.001, 0.01, 0.03, 0.1, 0.5):
            pm = max_p_strategy(12, 1.0, 0.5, tgt, "hard", bf, b)
            pr = max_p_rs(tgt, burst_frac=bf, b=b)
            pe = max_p_rs(tgt, burst_frac=bf, b=b, erased=8)
            res[(b, bf)] = (pm, pr, pe)
            lo_flag = "<=" if pm <= 1.01e-8 else ""
            out(f"| {bf:.3f} | {b} | {lo_flag}{pm:.2e} | {pr:.2e} | {pe:.2e} |")
    out("")
    out("Reading: under a 2e-19 target a binary line code is fragile to clustering: 1% of error bits in 3-bit "
        "clusters already cuts BCH-12 headroom several-fold, and any 8-bit clusters kill it. A byte-symbol RS code "
        "in the same side band is ~6x weaker on iid bits but indifferent to byte-confined bursts and keeps chipkill. "
        "The contract must therefore specify error geometry (cluster-size spectrum per codeword), not only raw BER, "
        "and the controller should pick BCH or RS per device grade. Cluster spectrum is a first-order measurement. "
        "With a chip already marked dead, RS headroom falls to ~1e-6, so the controller must drop that rank back "
        "to <=256 ms refresh until the DIMM is replaced (graceful degradation rule for the contract).")
    return res


# --------------------------------------------------------------------------------------------
# 5. Relaxed refresh on commodity DRAM
# --------------------------------------------------------------------------------------------
def lognormal_params():
    z1, z2 = Qinv(V("ret_anchor_ber_32ms")), Qinv(V("ret_anchor_ber_64ms"))
    # F = Q(-(ln t - mu)/s)  ->  -(ln t - mu)/s = z
    s_ln = (math.log(0.064) - math.log(0.032)) / (z1 - z2)
    mu = math.log(0.064) + z2 * s_ln
    return mu, s_ln


def ber_ret(P, model, temp_scale=1.0):
    """Static retention BER (random data) at refresh interval P s, 85 C; temp_scale>1 = cooler (longer)."""
    Pe = P / temp_scale
    if model == "pow3":
        f = V("ret_anchor_ber_64ms") * (Pe / 0.064) ** V("ret_pow_k")
    elif model == "pow5":
        f = V("ret_anchor_ber_64ms") * (Pe / 0.064) ** 5
    else:
        mu, s = lognormal_params()
        f = Q(-(math.log(Pe) - mu) / s)
    return min(f, 0.5) * V("data_pattern_factor")


def p_max_interval(model, pmax_code, temp_scale=1.0, vrt=None, scrub_h=None):
    vrt = V("vrt_growth_per_day") if vrt is None else vrt
    scrub_h = V("scrub_interval_h") if scrub_h is None else scrub_h
    mult = 1 + vrt * scrub_h / 24.0
    lo, hi = math.log(0.064), math.log(120.0)
    if ber_ret(0.064, model, temp_scale) * mult > pmax_code:
        return 0.064
    for _ in range(80):
        mid = (lo + hi) / 2
        if ber_ret(math.exp(mid), model, temp_scale) * mult <= pmax_code:
            lo = mid
        else:
            hi = mid
    return math.exp(lo)


def refresh_numbers(P):
    e = dcp.refresh_energy_per_bit_fJ()[0] * 1e-15
    cells = dcp.INPUTS["rdimm_dies"] * dcp.INPUTS["user_gbit"] * 1e9 * dcp.INPUTS["ecc_factor"]
    p_ref = cells * e / P
    p_scrub = cells * V("e_scrub_pJ_bit") * 1e-12 / (V("scrub_interval_h") * 3600)
    return p_ref, p_scrub, cells


def section_refresh(p_sb, p_rs):
    hr("5. Relaxed refresh on commodity DRAM (retention-limited regime)")
    mu, s = lognormal_params()
    out(f"Retention tail at 85 C, random data. pow3 = B4 calibration BER ~ t^3; lognormal = fit through the 32/64 ms "
        f"anchors (sigma_ln = {s:.2f}, median {math.exp(mu):.0f} s, local slope ~5 at 64 ms falling with t); "
        "pow5 = RAIDR local slope held (pessimistic bound).")
    out("")
    out("| refresh interval | BER pow3 | BER lognormal | BER pow5 | refresh W / 64 GB | tRFC loss 16Gb | 32Gb | 64Gb |")
    out("|---|---|---|---|---|---|---|---|")
    trfc = V("trfc_ns")
    for P in (0.064, 0.128, 0.256, 0.512, 1.0, 2.0):
        p_ref, _, _ = refresh_numbers(P)
        trefi = V("trefi_ns") * P / 0.064
        out(f"| {P*1e3:.0f} ms | {ber_ret(P,'pow3'):.1e} | {ber_ret(P,'logn'):.1e} | {ber_ret(P,'pow5'):.1e} | "
            f"{p_ref:.3f} | {trfc['16Gb']/trefi*100:.2f}% | {trfc['32Gb']/trefi*100:.2f}% | "
            f"{trfc['64Gb']/trefi*100:.2f}% |")
    out("(64 ms row: formula extrapolation; real parts have those cells repaired at test. 64Gb tRFC uses DDR5's "
        "3.9 us tREFI; A1 quotes ~20% on a 7.8 us basis.)")
    out("")
    out(f"Largest refresh interval whose static BER x (1 + VRT growth x scrub interval) fits the 128-bit side band: "
        f"BCH t=12 for iid errors (max {p_sb:.2e}) or RS(80,64) when errors cluster (max {p_rs:.2e}); scrub every "
        f"{V('scrub_interval_h'):.0f} h, VRT growth {V('vrt_growth_per_day')}/day:")
    out("")
    out("| retention model | code | 85 C | 65 C (x4 retention) | 45 C (x16) |")
    out("|---|---|---|---|---|")
    pm = {}
    for mdl, name in (("pow3", "pow3 (B4)"), ("logn", "lognormal fit"), ("pow5", "pow5 bound")):
        for code, plim in (("BCH-12 iid", p_sb), ("RS-8 clustered", p_rs)):
            r = [p_max_interval(mdl, plim, ts) for ts in (1.0, 4.0, 16.0)]
            pm[(mdl, code)] = r
            out(f"| {name} | {code} | {r[0]*1e3:.0f} ms | {r[1]*1e3:.0f} ms | {r[2]*1e3:.0f} ms |")
    out("")
    out("VRT sensitivity (lognormal model, 85 C): largest interval vs VRT growth and scrub interval")
    out("")
    out("| VRT growth /day | scrub 10 min | scrub 1 h | scrub 24 h |")
    out("|---|---|---|---|")
    for g in (0.1, 1.0, 10.0, 100.0):
        r = [p_max_interval("logn", p_sb, 1.0, g, sh) for sh in (1 / 6, 1.0, 24.0)]
        out(f"| {g:g} | {r[0]*1e3:.0f} ms | {r[1]*1e3:.0f} ms | {r[2]*1e3:.0f} ms |")
    out("")
    base_ref, _, cells = refresh_numbers(0.064)
    out("Power per 64 GB RDIMM at the chosen interval (refresh + scrub; scrub reads every bit once per interval):")
    out("")
    out("| interval | refresh W | scrub W | total W | cut vs 64 ms | idle-power saving (3 W idle) | tRFC loss 16Gb |")
    out("|---|---|---|---|---|---|---|")
    for P in (0.256, 0.5, 1.0, 2.0):
        p_ref, p_scr, _ = refresh_numbers(P)
        tot = p_ref + p_scr
        trefi = V("trefi_ns") * P / 0.064
        out(f"| {P*1e3:.0f} ms | {p_ref:.3f} | {p_scr*1e3:.2f} m | {tot:.3f} | {base_ref/tot:.1f}x | "
            f"{(base_ref-tot)/V('rdimm_idle_W')*100:.0f}% | {trfc['16Gb']/trefi*100:.2f}% |")
    out("")
    lc = pm[("logn", "BCH-12 iid")][0]
    lr = pm[("logn", "RS-8 clustered")][0]
    p5 = pm[("pow5", "RS-8 clustered")][0]
    out(f"Caveats: (1) DRAM self-refresh runs on the die's own timer, so idle savings need the controller to keep ranks "
        "in power-down and issue REF itself (small DLL/clock background cost, not modelled). (2) At 85 C the central "
        f"(lognormal) model allows {lc*1e3:.0f} ms with iid errors and {lr*1e3:.0f} ms if clustering forces RS; the "
        f"pessimistic bound with RS is {p5*1e3:.0f} ms. Most servers run DIMMs at 45-65 C, where a temperature-tracking "
        "controller (DDR5 RDIMM thermal sensor) stretches 4-16x further. (3) The 64 Gb tRFC crisis is where the "
        "time win is largest. (4) Retention-reject bins sit left of these curves by construction: the experiment "
        "must measure them, not assume them.")
    return pm, base_ref


# --------------------------------------------------------------------------------------------
# 6. One error budget
# --------------------------------------------------------------------------------------------
def section_budget(p_sb, sig):
    hr("6. One error budget, two ways to spend it")
    out("A code gives one raw-BER allowance. Margin errors (smaller Cs or lower VARY) and retention errors (longer "
        "refresh) draw on the same allowance. Split of the t=12 side-band allowance on a hypothetical new cell with "
        "today's retention tail (lognormal, 85 C, 1 h scrub):")
    out("")
    out("| share to margin | margin BER | dV mV | Cs fF | refresh interval | refresh cut |")
    out("|---|---|---|---|---|---|")
    base_ref, _, _ = refresh_numbers(0.064)
    for a in (0.0, 0.25, 0.5, 0.75, 0.99):
        pm_ = max(a * p_sb, 1e-12)
        dv = Qinv(pm_) * sig
        cs = cs_for_dv(dv)
        P = p_max_interval("logn", (1 - a) * p_sb)
        p_ref, p_scr, _ = refresh_numbers(P)
        out(f"| {a:.2f} | {pm_:.1e} | {dv:.1f} | {cs:.2f} | {P*1e3:.0f} ms | {base_ref/(p_ref+p_scr):.1f}x |")
    out("")
    out("Reading: the concept's '1.88x margin' and '10-15x refresh' are alternative spends. Splitting the budget "
        "costs little on either axis because both curves are steep (Gaussian margin tail, ~t^3-5 retention tail): "
        "half the budget still gives ~90% of the dV cut and most of the interval.")


# --------------------------------------------------------------------------------------------
# 7. Hammer and typed pages
# --------------------------------------------------------------------------------------------
def section_hammer_pages():
    hr("7. Row hammer under relaxed refresh; typed pages")
    trc = V("tRC_ns") * 1e-9
    for P in (0.064, 1.0):
        out(f"Max activations of one row per refresh window {P*1e3:.0f} ms: {P/trc:.2e} "
            f"({P/trc/V('hc_first'):.0f}x HCfirst {V('hc_first'):.0f}) -> counter-based mitigation is mandatory in "
            "both cases; the relaxed case only removes REF-hosted TRR slots.")
    rfm_worst = (1 / trc) / V("raaimt") * V("tRFM_ns") * 1e-9
    rfm_typ = V("act_rate_typ_per_bank") / V("raaimt") * V("tRFM_ns") * 1e-9
    out(f"Controller RFM substitution (RAAIMT {V('raaimt'):.0f}, tRFMsb {V('tRFM_ns'):.0f} ns): bank time lost "
        f"{rfm_worst*100:.1f}% under back-to-back ACT (attack), {rfm_typ*100:.2f}% at {V('act_rate_typ_per_bank'):.0e} "
        "ACT/s/bank (typical), vs the 7.6% tRFC loss removed. PRAC parts count per row and alert regardless of REF "
        "rate, so relaxed refresh is hammer-safe on PRAC DDR5 at the cost of more alerts [ESTIMATE].")
    out("")
    out("Page codes for cold / compressed pages: 64 B writes into a 4 KB codeword without coalescing cost a 4 KB read "
        "+ 4 KB write (128 line transfers).")
    out("")
    out("| SRAM coalescing hit rate | traffic per 64 B write (lines) |")
    out("|---|---|")
    for h in (0.0, 0.9, 0.99, 0.999):
        out(f"| {h:.3f} | {1 + (1-h)*128:.1f} |")
    e_bit = dcp.refresh_energy_per_bit_fJ()[0] * 1e-15
    saved = e_bit * (1 / 0.064 - 1 / 1.0) * 1e12
    out("")
    out(f"Refresh energy saved by 64 ms -> 1 s: {saved:.2f} pJ per bit per second. Break-even read rate: page decode "
        f"({V('e_page_decode_pJ_bit')} pJ/bit) {saved/V('e_page_decode_pJ_bit'):.2f} reads/s; line syndrome "
        f"({V('e_line_decode_pJ_bit')} pJ/bit) {saved/V('e_line_decode_pJ_bit'):.0f} reads/s. Page codes only for pages "
        "touched less than ~once a second; hot data stays on line BCH. Typed pages: 'regenerable' (KV/prefix cache) "
        "runs CRC-only and repairs by recompute; 'lossy-bounded' runs fixed-rate.")


# --------------------------------------------------------------------------------------------
# 8. Value
# --------------------------------------------------------------------------------------------
def section_value(base_ref, P_choice, res_t):
    hr("8. Value: energy, bandwidth, density, cost")
    p_ref, p_scr, _ = refresh_numbers(P_choice)
    saved_W = base_ref - p_ref - p_scr
    kwh = saved_W * V("years") * 8766 / 1000 * V("pue")
    usd = kwh * V("elec_usd_kWh")
    gb = V("module_GB")
    out(f"At {P_choice*1e3:.0f} ms: saves {saved_W:.2f} W per {gb:.0f} GB RDIMM -> {kwh:.0f} kWh over "
        f"{V('years'):.0f} yr at PUE {V('pue')} = ${usd:.2f} (${usd/gb:.3f}/GB, {usd/gb/V('ddr5_cost_per_GB')*100:.1f}% "
        f"of ${V('ddr5_cost_per_GB')}/GB).")
    fleet_W = saved_W / gb * 1e9  # per EB
    out(f"Fleet scale: {fleet_W/1e6:.1f} MW saved per exabyte of server DRAM (before PUE).")
    trfc = V("trfc_ns")
    for d in ("16Gb", "32Gb", "64Gb"):
        b0 = trfc[d] / V("trefi_ns")
        b1 = trfc[d] / (V("trefi_ns") * P_choice / 0.064)
        out(f"  {d}: refresh-blocked time {b0*100:.1f}% -> {b1*100:.2f}% (bandwidth/latency recovered ~{(b0-b1)*100:.1f} pts)")
    t4 = res_t[1e-4]
    par = V("bch_m_line") * t4 / V("line_data_bits")
    dens = V("density_1b_Gb_mm2") * dcp.INPUTS["ecc_factor"] / (1 + par)
    out("")
    out(f"New-die check-bit cost: t={t4} line BCH = {par*100:.1f}% vs on-die 6.25% -> same 1b cell gives "
        f"{dens:.3f} Gb/mm2 ({dens/V('density_1b_Gb_mm2'):.2f}x of {V('density_1b_Gb_mm2')}). The contract pays for "
        "itself only through the cells it enables (shorter pillar, 3D tiers), never on today's planar cell.")
    out("Commodity path: the 25% ECC side band already exists on RDIMMs, so the contract adds zero bits there; the "
        "choice is BCH-12 (6x more random-bit headroom, no chipkill) or RS-8 (keeps chipkill, section 4).")
    return usd / gb


# --------------------------------------------------------------------------------------------
# 9. GO / NO-GO
# --------------------------------------------------------------------------------------------
def bf_threshold(tgt, p, b=3):
    """Largest share of error bits in b-bit clusters that BCH t=12 tolerates at raw BER p."""
    if max_p_strategy(12, 1.0, 0.5, tgt, "hard", 0.0, b) < p:
        return 0.0
    lo, hi = -6.0, 0.0
    for _ in range(30):
        mid = (lo + hi) / 2
        if max_p_strategy(12, 1.0, 0.5, tgt, "hard", 10 ** mid, b) >= p:
            lo = mid
        else:
            hi = mid
    return 10 ** lo


def section_go(tgt, p_sb, p_rs, flag_table, pm):
    hr("9. GO / NO-GO for the decisive experiment")
    th = flag_table[1.0][0]
    tc50 = flag_table[0.5][3]
    bf3 = bf_threshold(tgt, 1e-4, 3)
    out("Measured on 50-100 DDR4 modules (no on-die ECC: raw physics) + retention-reject DIMMs, DRAM Bender, "
        "45/65/85 C, 0.25-2 s refresh, truncated-tRAS half-charge restore, reduced-tRCD double reads as the flag proxy, "
        ">=4 weeks of VRT soak, hammer with controller RFM:")
    out("")
    out(f"GO-A (refresh, commodity): measured BER at 0.5 s / 85 C (equivalently ~2 s / 65 C), including VRT growth over "
        f"a 1 h scrub, <= {p_sb:.1e} with <= {bf3*100:.2g}% of error bits in >=3-bit clusters per codeword (BCH-12), or "
        f"<= {p_rs:.1e} with clusters confined to bytes/chips (RS-8, chipkill kept). Either gives a >=7.7x refresh-"
        "energy cut and refresh-blocked time 7.6% -> <1% on 16Gb dies.")
    out(f"GO-B (margin, new cells): at emulated half-charge raw BER 1e-4, >=50% of errors flagged at a <=0.5-sigma "
        f"window (<=6 false flags per error), so Chase needs t<={tc50} ({tc50*10} bits) where hard decoding needs "
        f"t={th} ({th*10} bits); per-codeword error counts within 2x of Poisson out to 6 errors per 512 b.")
    out("NO-GO: largest safe interval <256 ms at 65 C even with RS-8 (RAIDR-class profiling already gets ~4x without "
        "ECC), or >10% of error events spanning more than one byte (not modelled here: such clusters need chip-level symbols and "
        "would pull the interval back toward RAIDR-class gains), or <25% of half-charge errors "
        "flaggable (flags then save <=10 check bits and the SA flag latch is not worth 3-7% die area). Revival "
        "condition for a NO-GO-A: oxide/IGZO cells, whose retention tail sits 1e3-1e4x to the right, re-run the "
        "same test.")
    out("")
    out(f"GO/NO-GO LINE: GO if the measured error stream fits the 128-bit side band (BCH-12 <= {p_sb:.1e} iid, or "
        f"RS-8 <= {p_rs:.1e} clustered) at the {tgt:.0e}/read target with refresh >= 0.5 s at 85 C, AND >=50% of "
        "half-charge errors are flaggable; NO-GO if the largest safe interval is <256 ms at 65 C.")
    return bf3


def write_md():
    hdr = ["# RAW-BER CONTRACT: model output",
           "",
           "Generated by `models/raw-ber-contract.py` (pure stdlib, `python3 models/raw-ber-contract.py` from "
           "dram-moonshot/). Inputs and their sources are listed at the end. [ESTIMATE] tags mark model assumptions.",
           ""]
    inp = ["", "## Inputs", "", "| key | value | source / basis |", "|---|---|---|"]
    for k, (v, s) in INPUTS.items():
        if v is None:
            v = f"{dcp.refresh_energy_per_bit_fJ()[0]:.1f}"
        inp.append(f"| {k} | {v} | {s} |")
    os.makedirs(os.path.dirname(OUT_MD), exist_ok=True)
    with open(OUT_MD, "w") as f:
        f.write("\n".join(hdr + LINES + inp) + "\n")


def main():
    out("# RAW-BER CONTRACT model (dos-raw-ber-contract)")
    tgt = section_target()
    p_sb, p_od, res_t = section_codes(tgt)
    sig, _ = section_margin(tgt)
    flag_table = section_flags(tgt, sig)
    burst_res = section_bursts(tgt)
    p_rs = burst_res[(3, 0.0)][1]
    pm, base_ref = section_refresh(p_sb, p_rs)
    section_budget(p_sb, sig)
    section_hammer_pages()
    usd_gb = section_value(base_ref, 1.0, res_t)
    bf3 = section_go(tgt, p_sb, p_rs, flag_table, pm)
    hr("Headline")
    out(f"- Target {tgt:.1e} per 64 B read; the concept's t=8 is ~100x short; t={res_t[1e-4]} (17.6%) needed at 1e-4 "
        "with hard decisions.")
    out(f"- A commodity DDR5 ECC RDIMM's existing 128-bit side band takes iid raw BER up to {p_sb:.1e} (BCH-12) or "
        f"{p_rs:.1e} with byte-confined clusters and chipkill (RS-8); behind DDR5 on-die SEC, internal BER up to "
        f"{p_od:.1e}. BCH-12 tolerates only ~{bf3*100:.2g}% of error bits in 3-bit clusters at 1e-4.")
    L = pm
    out(f"- Refresh interval at 85 C, iid / clustered: pow3 {L[('pow3','BCH-12 iid')][0]:.2f} / "
        f"{L[('pow3','RS-8 clustered')][0]:.2f} s; lognormal {L[('logn','BCH-12 iid')][0]:.2f} / "
        f"{L[('logn','RS-8 clustered')][0]:.2f} s; pow5 {L[('pow5','BCH-12 iid')][0]:.2f} / "
        f"{L[('pow5','RS-8 clustered')][0]:.2f} s. At 1 s: refresh 0.49 -> 0.03 W per 64 GB (15x), "
        f"${usd_gb:.3f}/GB of energy over 5 yr; tRFC loss 7.6% -> 0.5% (16Gb).")
    out(f"- Margin: 1e-4 buys 7 -> 3.72 sigma (50 -> 26.6 mV, Cs 5.4 -> 2.7 fF). Flags add only ~"
        f"{(Qinv(max_p_strategy(8, 0.0, V('flag_window_sigma'), tgt, 'hard'))/Qinv(flag_table[0.0][4])-1)*100:.0f}% "
        f"more (Chase t={flag_table[0.0][3]} vs hard t={flag_table[1.0][0]}) and nothing for refresh-latched errors.")
    write_md()
    print(f"\n[wrote {OUT_MD}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
