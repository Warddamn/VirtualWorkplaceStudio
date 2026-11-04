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
  10. Red-team revisions (10.1-10.10) and the DDR4 line-geometry correction of 2026-11-04 (10.11): a DDR4 x4
      RDIMM carries 64 check bits per 64 B line, not the 128 of a DDR5 RDIMM sub-channel.

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
    # RED-TEAM REVISION: 64Gb 1600 -> 700 ns (RT-PROC-raw-ber-contract-04, RT-IND-raw-ber-contract-03); 1600 kept
    # only as the upper sensitivity in section 10.
    "trfc_ns": ({"16Gb": 295.0, "32Gb": 410.0, "64Gb": 700.0},
                "A1 model: 16Gb datasheet; 32Gb [UNVERIFIED]; 64Gb was 1600 ns extrapolated (https://arxiv.org/pdf/"
                "1712.08304); revised to 700 ns ESTIMATE (critic range 600-800 ns: JEDEC held tRFC1 at 410 ns from 24Gb "
                "to 32Gb; resp-raw-ber-contract search did not confirm any 64Gb value)"),
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


# --------------------------------------------------------------------------------------------
# RED-TEAM REVISIONS (2026-11-02, owner response to research/redteam/rt_{DEV,PROC,CIRC,IND}.json;
# responses in research/redteam/responses_raw-ber-contract.json). old -> new (objection id):
#   trfc_ns["64Gb"]        1600 -> 700 ns central; 600-800 and 1600 as sensitivity      (RT-PROC-04, RT-IND-03)
#   trefw_ddr5_s           implicit 0.064 -> 0.032 s. DDR5 tREFI 3.9 us x 8192 REF = 32 ms; the original
#                          model paired DDR5's 3.9 us tREFI with a 64 ms window, so relaxed-interval tRFC
#                          loss was 2x too high and the DDR5 refresh-power baseline 2x too low. Found while
#                          answering RT-DEV-02 / RT-PROC-01 (DDR4 data vs the DDR5 product).
#   ret_time_scale_ddr5    implicit 1.0 -> 0.5 (DDR5 retention tail ~2x left of the DDR3/DDR4 anchors;
#                          the halved JEDEC window is the evidence; 1.0 kept as sensitivity)  (RT-DEV-02, RT-PROC-01)
#   headline code          BCH-12 (no chipkill) -> RS(80,64) byte code with chipkill; on DDR5, RS-8 sits
#                          behind on-die SEC; degraded mode (one chip marked dead) gets its own interval  (RT-CIRC-03)
#   flag leg               removed from the headline and from the GO/NO-GO; ledger added in section 10.5
#                          (RT-CIRC-01, RT-CIRC-02, RT-IND-02, RT-DEV-01)
#   NEW inputs below:      self-refresh residency and power-down background (RT-CIRC-04); decoder latency
#                          (RT-CIRC-05); multi-bit chip-fault rate and marking delay (RT-DEV-04); VRT pair
#                          share (RT-DEV-03); lot-to-lot retention spread and online servo guard (RT-PROC-02);
#                          sort-flow test time (RT-PROC-03); stacked-write tail correlation (RT-DEV-05,
#                          idea I-12627); plate-strip sense node (idea I-12302); flag-comparator noise and
#                          strobe skew (RT-CIRC-01); flag transport (RT-CIRC-02)
# --------------------------------------------------------------------------------------------
RT_INPUTS = {
    "trefw_ddr5_s": (0.032, "DDR5 refresh window 32 ms up to 85 C (https://en.wikipedia.org/wiki/DDR5_SDRAM, "
                            "via search snippet) = tREFI 3.9 us x 8192; DDR4 64 ms"),
    "ret_time_scale_ddr5": (0.5, "ESTIMATE: DDR5 1a/1b retention times = 0.5x the DDR3/DDR4-era anchors (JEDEC halved "
                                 "the window to 32 ms; 1b Cs ~5.4 fF); swept 0.5-1.0. RT-DEV-02 / RT-PROC-01"),
    "trfc64_range_ns": ((600.0, 700.0, 800.0, 1600.0), "RT-PROC-04 critic range 600-800 ns; old 1600 ns extrapolation"),
    "refsb_factor": ((0.33, 0.5), "ESTIMATE: same-bank refresh (tRFCsb) keeps other banks serving; rank-level "
                                  "throughput loss ~1/3-1/2 of all-bank REF [UNVERIFIED: training knowledge]. RT-IND-03"),
    "sr_residency": ((0.0, 0.1, 0.2, 0.5), "ESTIMATE: share of server time a rank spends in self-refresh (deep idle); "
                                           "swept. RT-CIRC-04"),
    "pd_background_W": ((0.3, 1.0), "RT-CIRC-04 critic estimate: clock, CA bus, RCD and PHY kept awake per RDIMM in "
                                    "power-down with controller REF [ESTIMATE, training knowledge]"),
    "lat_fast_ns": (2.0, "ESTIMATE: syndrome-zero check, 28 nm, pipelined"),
    "lat_single_ns": (4.0, "ESTIMATE: single-symbol correction by syndrome lookup / closed form, 28 nm"),
    "lat_bm_ns": (25.0, "RT-CIRC-05 critic: Berlekamp-Massey + Chien ~15-30 ns at 28 nm"),
    "cxl_adder_ns": ((70.0, 150.0), "RT-CIRC-05 critic: CXL Type-3 load-to-use adder over local DDR5 [training knowledge]"),
    "multibit_fault_fit_per_die": (30.0, "ESTIMATE: row/column/bank (multi-bit) DRAM faults ~half of ~25-70 FIT per "
                                         "device in field studies [UNVERIFIED-PK: Sridharan & Liberty SC12, Sridharan "
                                         "et al. ASPLOS 2015]. RT-DEV-04"),
    "census_module_hours": (1.8e5, "ESTIMATE: Phase 1 + Phase 2 exposure: ~80 modules x ~2,000 h campaigns + 20 x "
                                   "1,000 h soak. RT-DEV-04"),
    "lot_sigma_ln": ((0.35, 0.7), "ESTIMATE: lot-to-lot spread of retention-time scale (1 sigma, ln units); swept. "
                                  "RT-PROC-02"),
    "servo_ber_guard": (3.0, "ESTIMATE: the controller servos each rank's interval so measured corrected BER stays "
                             "<= 1/3 of the code's limit (NAND-style adaptive trim). RT-PROC-02"),
    "sort_pauses_s": ((0.5, 1.0, 2.0), "ESTIMATE: sort retention pauses for a contract grade. RT-PROC-03"),
    "sort_patterns": (4, "ESTIMATE: data patterns per pause"),
    "sort_temps": (2, "ESTIMATE: hot + room insertions"),
    "sort_pass_s": (0.25, "ESTIMATE: one full-die write + read pass in test mode"),
    "sort_sites": (512, "ESTIMATE: dies tested in parallel per memory test head [UNVERIFIED-PK]"),
    "stack_corr": ((0.0, 0.01, 0.1, 0.3), "ESTIMATE: share of leakage-tail defects shared by both series write "
                                          "devices (idea I-12627 needs independence). RT-DEV-05"),
    "plate_node_fF": (2.7, "idea I-12302: ~2 fF plate strip + parasitics; 1 fF cell into ~3.7 fF total gives ~135 mV "
                           "(research/ideas10k/stage2/stage2_results.jsonl)"),
    "plate_swing_V": (0.5, "derived from I-12302's 135 mV for 1 fF into 3.7 fF"),
    "tau_latch_ps": ((20.0, 50.0), "RT-CIRC-01 critic: latch regeneration time constant"),
    "strobe_skew_ps": ((15.0, 50.0, 150.0), "RT-CIRC-01 critic: SAN/SAP enable skew + droop along a 1k-SA strip"),
    "flag_cmp_noise_mV": ((0.0, 1.5, 3.6, 7.1), "ESTIMATE: flag comparator offset/noise (1.5 mV = critic's pass line)"),
    "flag_pos_bits": (10, "log2(640) rounded up: bits to name one flagged position in a 640-bit line. RT-CIRC-02"),
    "flag_sa_area_die": ((0.02, 0.04), "RT-CIRC-02 critic: second latch + comparator per SA = +20-40% SA strip = "
                                       "+2-4% die [ESTIMATE]"),
}


# --------------------------------------------------------------------------------------------
# DDR4 LINE-GEOMETRY CORRECTION (2026-11-04). The red-team-era DDR4 rows (sections 10.1, 10.4, 10.6) gave retired
# DDR4 the DDR5 RDIMM line: 640 bits = 512 data + 128 check bits, RS(80,64) with an x4 chip = 8 bytes. A DDR4 x4
# ECC RDIMM moves 72 bits x burst 8 per 64 B line = 512 data + 64 check bits (12.5%), 18 x4 chips x 32 bits. Section
# 10.11 models three DDR4 layouts: (a) one 72-bit channel, RS(72,64) over bytes; (b) two channels in lockstep,
# RS(144,128) over bytes on a 128 B access; (c) a CXL layout that stores 64 more check bits per line in DRAM data
# space (RS(80,64), -11.1% capacity). The old DDR4 rows equal layout (c) exactly and are kept, relabelled.
# DDR5 rows are unchanged: 2 x 40-bit sub-channels (32 data + 8 ECC) x burst 16 = 512 + 128 per 64 B line.
# --------------------------------------------------------------------------------------------
GEO_INPUTS = {
    "ddr4_bus_bits": (72, "DDR4 ECC DIMM bus = 64 data + 8 ECC bits [REPORTED: US 11,437,114, "
                          "https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11437114, via search snippet]; "
                          "fixed burst 8 [DATASHEET: Micron DDR4 RDIMM, https://dtsheet.com/model/4467123, via search "
                          "snippet] -> 512 data + 64 check bits per 64 B line"),
    "ddr4_x4_chips": (18, "16 data + 2 ECC x4 chips per 72-bit rank [REPORTED: https://arxiv.org/pdf/1908.01806, via "
                          "search snippet]; each chip gives 4 DQ x 8 beats = 32 bits = 4 byte symbols per line"),
    "ddr4_ssc_codewords": (4, "host-style x4 SSC: one 8-bit symbol per chip over 2 beats, 16 data + 2 check symbols per "
                              "codeword, 4 codewords per 8-beat request (AMD 2013) [REPORTED: https://arxiv.org/pdf/"
                              "1908.01806, via search snippet]. Intel SDDC on x4 DDR4 runs in independent-channel mode "
                              "[REPORTED: Lenovo/Dell server manuals via search snippet]"),
    "ddr4_lockstep_bits": (1152, "two 72-bit channels in lockstep: 36 x4 chips, 144-bit word = 128 data + 16 check bits "
                                 "per beat [REPORTED: US 9,772,900, https://image-ppubs.uspto.gov/dirsearch-public/print/"
                                 "downloadPdf/9772900; arXiv 1908.01806]; burst 8 -> 1024 data + 128 check per 128 B access. "
                                 "Lockstep halves rank/bank parallelism and doubles prefetch energy at burst 8 [REPORTED: "
                                 "same patent, via search snippet]"),
    "ddr4_extra_check_bits": (64, "ESTIMATE/design: layout (c) stores 64 more check bits per 512 data bits in DRAM data "
                                  "space (one parity line per 8 data lines) -> 128 check bits, RS(80,64) as on DDR5; worst "
                                  "line: a dead chip holds 4 data + 4 parity bytes (8 erasures)"),
    "ddr4_dies_note": ((36, 72), "ESTIMATE: a 64 GB DDR4 x4 RDIMM holds 36 (16Gb) to 72 (8Gb) dies; section 10.11 keeps "
                                 "the model's 40-die fault count (scale the chip-fault UE by 0.9-1.8x)"),
}


def G(k):
    return GEO_INPUTS[k][0]


def R(k):
    return RT_INPUTS[k][0]


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
        "a commodity DDR5 ECC RDIMM carries, so relaxed refresh on today's DRAM needs no page code at all for iid errors. "
        "[Correction 2026-11-04: a DDR4 ECC RDIMM carries 12.5% (64 check bits per 64 B line); see section 10.11.]")
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


FLAG_NOISE = [0.0]  # RED-TEAM (RT-CIRC-01): flag-comparator noise in sigma_eff units; 0 = ideal flag (original model)


def flag_rates(p, conf_frac, delta):
    """Per-bit rates: flagged errors, unflagged soft errors, false flags (correct but flagged)."""
    p_soft = (1 - conf_frac) * p
    if p_soft <= 0:
        return 0.0, 0.0, 0.0
    s = Qinv(p_soft)
    sf_ = FLAG_NOISE[0]
    if sf_ <= 0:
        p_ef = Q(s) - Q(s + delta)
        p_eu = Q(s + delta)
        p_ff = Q(s - delta) - Q(s)
        return p_ef, p_eu, p_ff
    # Noisy flag: bit signal x ~ N(s, 1) relative to the main threshold (x<0 = error); the flag comparator sees
    # x + n, n ~ N(0, sf_), and flags if |x + n| < delta.
    L = delta + 8 * sf_ + 1.0
    N = 4000
    dx = 2 * L / N
    p_ef = p_ff = 0.0
    for i in range(N):
        x = -L + (i + 0.5) * dx
        dens = math.exp(-0.5 * (x - s) ** 2) / math.sqrt(2 * math.pi)
        pf = Q((-delta - x) / sf_) - Q((delta - x) / sf_)
        if x < 0:
            p_ef += dens * pf * dx
        else:
            p_ff += dens * pf * dx
    p_ef = min(p_ef, p_soft)
    return p_ef, p_soft - p_ef, p_ff


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
    lo, hi = math.log(0.016), math.log(120.0)  # RED-TEAM: floor 64 -> 16 ms so DDR5/degraded cases can resolve
    if ber_ret(0.016, model, temp_scale) * mult > pmax_code:
        return 0.016
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
    for P in (0.032, 0.064, 0.128, 0.256, 0.512, 1.0, 2.0):
        p_ref, _, _ = refresh_numbers(P)
        trefi = V("trefi_ns") * P / R("trefw_ddr5_s")  # RED-TEAM fix: DDR5 tREFI 3.9 us belongs to a 32 ms window
        out(f"| {P*1e3:.0f} ms | {ber_ret(P,'pow3'):.1e} | {ber_ret(P,'logn'):.1e} | {ber_ret(P,'pow5'):.1e} | "
            f"{p_ref:.3f} | {trfc['16Gb']/trefi*100:.2f}% | {trfc['32Gb']/trefi*100:.2f}% | "
            f"{trfc['64Gb']/trefi*100:.2f}% |")
    out("(32/64 ms rows: formula extrapolation; real parts have those cells repaired at test. tRFC loss uses DDR5's "
        "3.9 us tREFI at its 32 ms window and scales tREFI with the interval [RED-TEAM fix: the original scaled from "
        "64 ms, doubling the relaxed-interval loss]. 64Gb tRFC revised 1600 -> 700 ns [RT-PROC-04]. BER columns use "
        "the DDR3/DDR4-era anchors; DDR5 is ~2x left, see section 10.)")
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
    out("[Correction 2026-11-04: 128 check bits per 64 B line is the DDR5 RDIMM organisation. With these DDR3/DDR4-era "
        "tails the table describes retired DDR4 only in the capacity-trading layout (c) of section 10.11; a DDR4 RDIMM "
        "line carries 64 check bits.]")
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
    out("| interval | refresh W | scrub W | total W | cut vs 64 ms (DDR4) | cut vs 32 ms (DDR5 spec) | idle-power saving vs 64 ms (3 W idle) | tRFC loss 16Gb |")
    out("|---|---|---|---|---|---|---|---|")
    base32 = refresh_numbers(R("trefw_ddr5_s"))[0]
    for P in (0.256, 0.5, 1.0, 2.0):
        p_ref, p_scr, _ = refresh_numbers(P)
        tot = p_ref + p_scr
        trefi = V("trefi_ns") * P / R("trefw_ddr5_s")
        out(f"| {P*1e3:.0f} ms | {p_ref:.3f} | {p_scr*1e3:.2f} m | {tot:.3f} | {base_ref/tot:.1f}x | {base32/tot:.1f}x | "
            f"{(base_ref-tot)/V('rdimm_idle_W')*100:.0f}% | {trfc['16Gb']/trefi*100:.2f}% |")
    out("")
    lc = pm[("logn", "BCH-12 iid")][0]
    lr = pm[("logn", "RS-8 clustered")][0]
    p5 = pm[("pow5", "RS-8 clustered")][0]
    out(f"Caveats: (1) DRAM self-refresh runs on the die's own timer, so idle savings need the controller to keep ranks "
        "in power-down and issue REF itself (background cost 0.3-1 W per RDIMM per RT-CIRC-04; hybrid policy in section 10.3). (2) At 85 C the central "
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
        b1 = trfc[d] / (V("trefi_ns") * P_choice / R("trefw_ddr5_s"))  # RED-TEAM fix (32 ms window)
        out(f"  {d}: refresh-blocked time {b0*100:.1f}% -> {b1*100:.2f}% (bandwidth/latency recovered ~{(b0-b1)*100:.1f} pts)")
    t4 = res_t[1e-4]
    par = V("bch_m_line") * t4 / V("line_data_bits")
    dens = V("density_1b_Gb_mm2") * dcp.INPUTS["ecc_factor"] / (1 + par)
    out("")
    out(f"New-die check-bit cost: t={t4} line BCH = {par*100:.1f}% vs on-die 6.25% -> same 1b cell gives "
        f"{dens:.3f} Gb/mm2 ({dens/V('density_1b_Gb_mm2'):.2f}x of {V('density_1b_Gb_mm2')}). The contract pays for "
        "itself only through the cells it enables (shorter pillar, 3D tiers), never on today's planar cell.")
    out("Commodity path: the 25% ECC side band already exists on DDR5 RDIMMs, so the contract adds zero bits there; the "
        "choice is BCH-12 (6x more random-bit headroom, no chipkill) or RS-8 (keeps chipkill, section 4). [Correction "
        "2026-11-04: DDR4 RDIMMs carry 12.5%, not 25%; section 10.11.]")
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
        "energy cut and refresh-blocked time 7.6% -> <1% on 16Gb dies. [Correction 2026-11-04: a DDR4 module has a "
        "64-bit, not 128-bit, side band per 64 B line; these limits apply to DDR4 only in layout (c) of section 10.11.]")
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


# --------------------------------------------------------------------------------------------
# 10. RED-TEAM REVISIONS: variants run for the 19 objections (see the RED-TEAM REVISIONS block at the top)
# --------------------------------------------------------------------------------------------
def max_p_rs_ondie(tgt, erased=False):
    """RS(80,64) over bytes behind DDR5 on-die SEC(136,128). Each x4 chip's 64-bit slice = 8 byte symbols; post-SEC
    bit errors in a slice count as min(k, 8) symbols (upper bound: every bit in its own byte). Healthy: fail if
    > 8 symbol errors over 10 chips. One chip marked dead (erased): 9 chips, fail if > 4 symbol errors."""
    chips = int(V("chips_per_line")) - (1 if erased else 0)
    cap = 4 if erased else 8
    lo, hi = -7.0, -2.0
    for _ in range(45):
        mid = (lo + hi) / 2
        sym = slice_symbol_pmf(10 ** mid)
        tot = [1.0] + [0.0] * 40
        for _ in range(chips):
            tot = conv(tot, sym, 40)
        if sum(tot[cap + 1:]) <= tgt:
            lo = mid
        else:
            hi = mid
    return 10 ** lo


def slice_symbol_pmf(p):
    sl = ondie_slice_pmf(p, 40)
    sym = [0.0] * 9
    for k, w in enumerate(sl):
        sym[min(k, 8)] += w
    return sym


def line_symbol_pmf_ondie(p, chips):
    sym = slice_symbol_pmf(p)
    tot = [1.0] + [0.0] * 40
    for _ in range(chips):
        tot = conv(tot, sym, 40)
    return tot


def local_slope(P, model, ts):
    return (math.log(ber_ret(P * 1.01, model, ts)) - math.log(ber_ret(P, model, ts))) / math.log(1.01)


def max_p_chase_F(t, F, tgt, delta=None):
    """All-soft margin errors (best case for flags); Chase/erasure over at most F transported flag positions."""
    delta = V("flag_window_sigma") if delta is None else delta
    lo, hi = -8.0, -1.5
    for _ in range(34):
        mid = (lo + hi) / 2
        f = fail_probs(10 ** mid, t, 0.0, delta, fmax=F)
        if min(f[2], f[3]) <= tgt:
            lo = mid
        else:
            hi = mid
    return 10 ** lo


def section_redteam(tgt, p_sb, p_od, p_rs, p_rs_er, sig):
    RES = {}
    hr("10. RED-TEAM REVISIONS: variants run for the 19 objections")
    out("Owner response, 2026-11-02. Objections in research/redteam/rt_*.json; responses in research/redteam/"
        "responses_raw-ber-contract.json. Inputs added here are in the RT_INPUTS table at the end.")

    # ---------------- 10.1 DDR5 basis, chipkill kept ----------------
    hr("10.1 DDR5 basis with chipkill kept (RT-CIRC-03, RT-DEV-02, RT-PROC-01)")
    p_rs_od = max_p_rs_ondie(tgt)
    p_rs_od_er = max_p_rs_ondie(tgt, erased=True)
    RES.update(p_rs_od=p_rs_od, p_rs_od_er=p_rs_od_er)
    out("Code limits at the 2e-19/read target (max internal raw BER, iid errors; DDR5 rows include on-die "
        "SEC(136,128) with 53% doublet miscorrection in front of the controller code):")
    out("")
    out("| part | controller code | chipkill | max raw BER |")
    out("|---|---|---|---|")
    out(f"| DDR4 (no on-die ECC), 640-bit layout (c) | BCH-12 | no | {p_sb:.2e} |")
    out(f"| DDR4, 640-bit layout (c) | RS(80,64) bytes | yes | {p_rs:.2e} |")
    out(f"| DDR4, 640-bit layout (c) | RS(80,64), one chip marked dead | degraded | {p_rs_er:.2e} |")
    out(f"| DDR5 behind on-die SEC | BCH-12 | no | {p_od:.2e} |")
    out(f"| DDR5 behind on-die SEC | RS(80,64) bytes | yes | {p_rs_od:.2e} |")
    out(f"| DDR5 behind on-die SEC | RS(80,64), one chip marked dead | degraded | {p_rs_od_er:.2e} |")
    out("")
    out("[Correction 2026-11-04: the DDR4 rows give retired DDR4 a 640-bit line with 128 check bits, the DDR5 RDIMM "
        "organisation. A DDR4 x4 RDIMM carries 64 check bits per 64 B line, so these rows hold only for layout (c), "
        "which spends 11.1% of capacity on extra check bits. Realistic DDR4 layouts: section 10.11.]")
    out("")
    out("On-die SEC HURTS the chipkill code (a red-team-run finding): it strips singletons but turns doublets into "
        "2-3-bit chip-confined events that each consume 2-3 RS symbols, so three such events on one read exceed "
        "t=8 (failure ~p^6 instead of ~p^9 for iid singles). RS-8 behind SEC tolerates ~3.6x less internal BER than "
        "RS-8 on the same 640-bit line without SEC. The symbol count is an upper bound (each post-SEC bit in its own byte; for 3 bits in "
        "8 bytes that holds 66% of the time anyway).")
    out("")
    sc = R("ret_time_scale_ddr5")
    w5, w4 = R("trefw_ddr5_s"), 0.064
    out(f"Safe refresh interval (1 h scrub, VRT 1x/day). DDR5 retention = DDR3/DDR4-era anchors x {sc} in time "
        f"[RT-DEV-02 derate; 1.0 = no derate]. 'cut' = interval / the part's own JEDEC window (DDR4 64 ms, DDR5 32 ms).")
    out("")
    out("| part / code | retention model | ret. scale | 85 C | cut at 85 C | 65 C | 45 C |")
    out("|---|---|---|---|---|---|---|")
    cases = [
        ("DDR4 (c) / RS-8 chipkill", p_rs, "logn", 1.0, w4),
        ("DDR4 (c) / RS-8 chipkill", p_rs, "pow5", 1.0, w4),
        ("DDR4 (c) / RS-8 degraded (chip dead)", p_rs_er, "logn", 1.0, w4),
        ("DDR5 / RS-8 behind SEC", p_rs_od, "pow3", sc, w5),
        ("DDR5 / RS-8 behind SEC", p_rs_od, "logn", sc, w5),
        ("DDR5 / RS-8 behind SEC", p_rs_od, "pow5", sc, w5),
        ("DDR5 / RS-8 behind SEC", p_rs_od, "logn", 1.0, w5),
        ("DDR5 / RS-8 degraded (chip dead)", p_rs_od_er, "logn", sc, w5),
        ("DDR5 / RS-8 degraded (chip dead)", p_rs_od_er, "pow5", sc, w5),
        ("DDR5 / BCH-12 behind SEC (no chipkill)", p_od, "logn", sc, w5),
    ]
    iv = {}
    for name, plim, mdl, scale, win in cases:
        r = [p_max_interval(mdl, plim, ts * scale) for ts in (1.0, 4.0, 16.0)]
        iv[(name, mdl, scale)] = r
        out(f"| {name} | {mdl} | {scale:g} | {r[0]*1e3:.0f} ms | {r[0]/win:.1f}x | {r[1]*1e3:.0f} ms | {r[2]*1e3:.0f} ms |")
    I_c = iv[("DDR5 / RS-8 behind SEC", "logn", sc)][0]
    I_p = iv[("DDR5 / RS-8 behind SEC", "pow5", sc)][0]
    I_o = iv[("DDR5 / RS-8 behind SEC", "pow3", sc)][0]
    I_d = iv[("DDR5 / RS-8 degraded (chip dead)", "logn", sc)][0]
    I_c65 = iv[("DDR5 / RS-8 behind SEC", "logn", sc)][1]
    I_d65 = iv[("DDR5 / RS-8 degraded (chip dead)", "logn", sc)][1]
    I_4c = iv[("DDR4 (c) / RS-8 chipkill", "logn", 1.0)][0]
    RES.update(I_c=I_c, I_p=I_p, I_o=I_o, I_d=I_d, I_c65=I_c65, I_d65=I_d65, I_4c=I_4c)
    base32 = refresh_numbers(w5)[0]
    pr, ps, _ = refresh_numbers(I_c)
    sav = base32 - pr - ps
    RES.update(base32=base32, sav=sav, cut_c=base32 / (pr + ps))
    pr_p, ps_p, _ = refresh_numbers(I_p)
    RES["cut_p"] = base32 / (pr_p + ps_p)
    pr_d, ps_d, _ = refresh_numbers(I_d)
    RES["cut_d"] = base32 / (pr_d + ps_d)
    pr65, ps65, _ = refresh_numbers(min(I_c65, 4.0))
    RES["cut_65"] = base32 / (pr65 + ps65)
    out("")
    out(f"Revised commodity headline (DDR5 RDIMM, chipkill kept, 85 C): central {I_c*1e3:.0f} ms = "
        f"{RES['cut_c']:.1f}x refresh energy vs the 32 ms spec; pessimistic (pow5) {I_p*1e3:.0f} ms = "
        f"{RES['cut_p']:.1f}x; optimistic (pow3) {I_o*1e3:.0f} ms; degraded mode {I_d*1e3:.0f} ms = "
        f"{RES['cut_d']:.1f}x until the DIMM is serviced. At 65 C: {I_c65*1e3:.0f} ms ({RES['cut_65']:.0f}x, "
        f"capped at 4 s), degraded {I_d65*1e3:.0f} ms.")
    out(f"DDR5 refresh baseline at its real 32 ms window: {base32:.3f} W per 64 GB (A1 per-cell energy; the "
        f"original model's 0.488 W was a 64 ms figure). Saving at the central interval: {sav:.3f} W.")

    # ---------------- 10.2 tRFC ----------------
    hr("10.2 64Gb refresh-blocked time (RT-PROC-04, RT-IND-03)")
    out("| 64Gb tRFC | blocked, all-bank REF at 3.9 us | same-bank REF equivalent (x0.33-0.5) | at central interval | at pessimistic interval |")
    out("|---|---|---|---|---|")
    for tr in R("trfc64_range_ns"):
        b0 = tr / V("trefi_ns")
        bc = tr / (V("trefi_ns") * I_c / w5)
        bp = tr / (V("trefi_ns") * I_p / w5)
        f1, f2 = R("refsb_factor")
        out(f"| {tr:.0f} ns{' (old)' if tr == 1600 else ''} | {b0*100:.1f}% | {b0*f1*100:.1f}-{b0*f2*100:.1f}% | "
            f"{bc*100:.2f}% | {bp*100:.2f}% |")
    b0 = 700 / V("trefi_ns")
    RES.update(b64=b0, b64c=700 / (V("trefi_ns") * I_c / w5))
    out("")
    out(f"Reading: at 700 ns the 64Gb blocked time is {b0*100:.0f}% (not 41%); same-bank refresh hides perhaps half to "
        f"two thirds of it. Relaxed refresh still divides whatever remains by ~{I_c/w5:.0f}x, so the recovered "
        f"bandwidth is ~{(b0*0.33)*100:.0f}-{b0*100:.0f} points, not ~38.")

    # ---------------- 10.3 self-refresh ----------------
    hr("10.3 Self-refresh and the idle saving (RT-CIRC-04)")
    out(f"Refresh saving while the controller issues REF: {sav:.3f} W per 64 GB at the central interval. Policy A keeps "
        "ranks in power-down with controller REF even when idle (pays the background cost); policy B lets idle "
        "ranks enter the die's own self-refresh (no saving there, no loss).")
    out("")
    out("| self-refresh residency | policy A, background 0.3 W | policy A, background 1.0 W | policy B (hybrid) | 5-yr value, policy B |")
    out("|---|---|---|---|---|")
    for f in R("sr_residency"):
        a1 = sav - f * R("pd_background_W")[0]
        a2 = sav - f * R("pd_background_W")[1]
        b = sav * (1 - f)
        usd = b * V("years") * 8766 / 1000 * V("pue") * V("elec_usd_kWh")
        out(f"| {f:.1f} | {a1:+.3f} W | {a2:+.3f} W | {b:+.3f} W | ${usd:.2f} |")
    usd02 = sav * 0.8 * V("years") * 8766 / 1000 * V("pue") * V("elec_usd_kWh")
    RES["usd02"] = usd02
    out("")
    out(f"Reading: always-on controller REF goes negative once self-refresh residency exceeds "
        f"{sav/R('pd_background_W')[1]*100:.0f}% (1 W background) or {min(sav/R('pd_background_W')[0],1)*100:.0f}% "
        f"(0.3 W). The hybrid policy never loses; at 20% residency it keeps ${usd02:.2f} per module over 5 years "
        f"(${usd02/V('module_GB'):.3f}/GB). A programmable self-refresh interval (an LPDDR-style temperature-"
        "compensated rate, [UNVERIFIED-PK]) would recover the rest; it is a JEDEC ask, not a controller feature.")

    # ---------------- 10.4 latency ----------------
    hr("10.4 Decoder slow path and latency (RT-CIRC-05)")
    out(f"Fast path {R('lat_fast_ns'):.0f} ns (syndrome zero), single-symbol fix {R('lat_single_ns'):.0f} ns, "
        f"multi-symbol Berlekamp-Massey + Chien {R('lat_bm_ns'):.0f} ns. The operating BER is the code limit / "
        f"{R('servo_ber_guard'):.0f} (servo guard, 10.8) or the limit itself (worst case).")
    out("")
    out("| case | operating raw BER | lines with any error | lines needing BM | mean added ns | p99 path |")
    out("|---|---|---|---|---|---|")
    for name, p_op, ondie in (("DDR4 (c), RS-8 at limit", p_rs, False),
                              ("DDR4 (c), RS-8 servoed", p_rs / R("servo_ber_guard"), False),
                              ("DDR4 (c), BCH-12 at 1e-4 (critic case)", 1e-4, False),
                              ("DDR5 behind SEC, RS-8 at limit", p_rs_od, True),
                              ("DDR5 behind SEC, RS-8 servoed", p_rs_od / R("servo_ber_guard"), True)):
        if ondie:
            pm = line_symbol_pmf_ondie(p_op, int(V("chips_per_line")))
            p1 = 1 - pm[0]
            p2 = 1 - pm[0] - pm[1]
        else:
            lam = 640 * p_op
            p1 = 1 - math.exp(-lam)
            p2 = 1 - math.exp(-lam) * (1 + lam)
        mean = R("lat_fast_ns") + (p1 - p2) * R("lat_single_ns") + p2 * R("lat_bm_ns")
        path = "BM" if p2 > 0.01 else ("single fix" if p1 > 0.01 else "fast")
        out(f"| {name} | {p_op:.1e} | {p1*100:.3f}% | {p2*100:.4f}% | {mean:.2f} | {path} |")
    out("")
    out(f"Reading: the critic's 5.6% slow path is real for a raw 640-bit line at 1e-4, but almost all of it is single-symbol "
        "errors that a lookup fixes in a few ns; BM is needed on <0.2% of lines. Behind DDR5's on-die SEC the "
        f"controller rarely sees an error at all. The CXL hop itself adds {R('cxl_adder_ns')[0]:.0f}-"
        f"{R('cxl_adder_ns')[1]:.0f} ns: the commodity product is a capacity tier, and DRAM-class latency needs the "
        "decoder in the host memory controller (where chipkill decoders already sit) or on-die. [Correction 2026-11-04: "
        "DDR4 rows are layout (c); DDR4 layouts (a) and (b) are in section 10.11.]")

    # ---------------- 10.5 flag ledger ----------------
    hr("10.5 Flag ledger (RT-CIRC-01, RT-CIRC-02, RT-IND-02, RT-DEV-01)")
    dmv = V("flag_window_sigma") * sig
    out(f"(a) Time-domain (delayed-strobe) flag: window delta = {dmv:.1f} mV. Resolution time t = tau ln(V/dV), so a "
        "timing error s shifts the effective threshold by exp(s/tau); equivalent amplitude noise ~ delta (exp(s/tau) - 1).")
    out("")
    out("| tau ps | window tau ln2 ps | skew 15 ps | skew 50 ps | skew 150 ps |")
    out("|---|---|---|---|---|")
    for tau in R("tau_latch_ps"):
        cells = []
        for sk in R("strobe_skew_ps"):
            eq = dmv * (math.exp(sk / tau) - 1)
            cells.append(f"{eq:.1f} mV" if eq < 1000 else ">1 V")
        out(f"| {tau:.0f} | {tau*math.log(2):.0f} | " + " | ".join(cells) + " |")
    out("")
    out("(b) Amplitude-domain flag (offset-cancelled dual-reference comparator) with comparator noise sigma_f; all "
        "errors soft (best case for flags), raw BER 1e-4, delta = 0.5 sigma:")
    out("")
    out("| sigma_f mV | flagged share of errors | false flags per error | Chase t | max raw BER at t=8 |")
    out("|---|---|---|---|---|")
    for nmv in R("flag_cmp_noise_mV"):
        FLAG_NOISE[0] = nmv / sig
        pe, pu, pf = flag_rates(1e-4, 0.0, V("flag_window_sigma"))
        tc = min_t_strategy(1e-4, 0.0, V("flag_window_sigma"), tgt, "Chase")
        pm8 = max_p_strategy(8, 0.0, V("flag_window_sigma"), tgt, "Chase")
        out(f"| {nmv:.1f} | {pe/1e-4*100:.0f}% | {pf/1e-4:.1f} | {tc} | {pm8:.2e} |")
    FLAG_NOISE[0] = 0.0
    pe, pu, pf = flag_rates(1e-4, 0.0, V("flag_window_sigma"))
    lam_f = 640 * (pe + pf)
    out("")
    out(f"(c) Transport: {lam_f:.2f} flags per 640-bit line at 1e-4 (ideal flag). Naming F positions costs "
        f"{R('flag_pos_bits')} F + 2 bits; overflow P(flags > F): F=1 {1-math.exp(-lam_f)*(1+lam_f):.3f}, "
        f"F=2 {1-math.exp(-lam_f)*(1+lam_f+lam_f**2/2):.4f}, F=3 {1-math.exp(-lam_f)*(1+lam_f+lam_f**2/2+lam_f**3/6):.5f}.")
    out("")
    out("(d) Inside a fixed 128-bit side band (ideal flags, all errors soft):")
    out("")
    out("| allocation | bits used | max raw BER |")
    out("|---|---|---|")
    out(f"| BCH t=12, no flags | 120 | {p_sb:.2e} |")
    for t, F in ((11, 0), (10, 2), (9, 3), (8, 4)):
        bits = 10 * t + (R("flag_pos_bits") * F + 2 if F else 0)
        if F == 0:
            pm_ = max_p_hard(t, 512, 10, tgt)
        else:
            pm_ = max_p_chase_F(t, F, tgt)
        out(f"| BCH t={t} + {F} flag positions | {bits} | {pm_:.2e} |")
    FLAG_NOISE[0] = 1.5 / sig
    pm_n = max_p_chase_F(10, 2, tgt)
    FLAG_NOISE[0] = 0.0
    out(f"| BCH t=10 + 2 flag positions, comparator noise 1.5 mV | 122 | {pm_n:.2e} |")
    RES["sb_flag_ideal"] = max_p_chase_F(10, 2, tgt)
    RES["sb_flag_noisy"] = pm_n
    th = min_t_strategy(1e-4, 1.0, V("flag_window_sigma"), tgt, "hard")
    tcb = min_t_strategy(1e-4, 0.0, V("flag_window_sigma"), tgt, "Chase")
    saved = (th - tcb) * 10 / 512
    tr1 = (R("flag_pos_bits") + 1) / 512
    a1, a2 = R("flag_sa_area_die")
    RES.update(flag_net_lo=saved - tr1 - a2, flag_net_hi=saved - tr1 - a1, flag_saved=saved)
    out("")
    out(f"(e) New-die ledger at raw BER 1e-4, ideal flags: check bits saved {th*10}-{tcb*10} = {(th-tcb)*10} per 512 "
        f"({saved*100:.1f}% of die bits); transport >= 1 position + overflow bit = {tr1*100:.1f}% (or one extra beat "
        f"in 16 = 6.25% bandwidth); second SA latch +{a1*100:.0f}-{a2*100:.0f}% die. Net: "
        f"{(saved-tr1-a2)*100:+.1f}% to {(saved-tr1-a1)*100:+.1f}% of die. Within a fixed side band, ideal flags on "
        f"all-soft errors buy at most {(RES['sb_flag_ideal']/p_sb-1)*100:+.0f}% raw-BER headroom over plain BCH-12 "
        f"({(RES['sb_flag_noisy']/p_sb-1)*100:+.0f}% with 1.5 mV comparator noise), before any confident "
        "(refresh-latched) errors, which erase the gain.")

    # ---------------- 10.6 correlated-fault coincidence ----------------
    hr("10.6 Correlated faults and the 2e-19 target (RT-DEV-04)")
    nf = dcp.INPUTS["rdimm_dies"] * R("multibit_fault_fit_per_die") * 1e-9 * 8766
    out(f"Multi-bit (row/column/bank) faults: {R('multibit_fault_fit_per_die'):.0f} FIT/die x "
        f"{dcp.INPUTS['rdimm_dies']} dies = {nf:.4f} per module-year. RS-8 corrects one fully corrupted chip slice "
        "(8 symbols) but then has no spare: a UE needs one more symbol error in the other 9 chips on the same read. "
        "After the first chip-confined correction the controller marks the chip (erasure mode, degraded refresh). "
        "UE per module-year = faults x reads-before-marking x q.")
    out("")
    out("| case | operating raw BER | q = P(other-chip symbol error) | mark after 1 read | after 10 | after 100 |")
    out("|---|---|---|---|---|---|")
    p64 = ber_ret(0.064, "logn")
    rows = (("64 ms today (DDR4 anchors)", p64, False),
            ("DDR4 (c) RS-8 at limit", p_rs, False), ("DDR4 (c) RS-8 servoed", p_rs / R("servo_ber_guard"), False),
            ("DDR5 behind SEC, RS-8 at limit", p_rs_od, True),
            ("DDR5 behind SEC, RS-8 servoed", p_rs_od / R("servo_ber_guard"), True))
    for name, p_op, ondie in rows:
        if ondie:
            q = 1 - line_symbol_pmf_ondie(p_op, int(V("chips_per_line")) - 1)[0]
        else:
            q = 1 - math.exp(-576 * p_op)
        ue = [nf * n * q for n in (1, 10, 100)]
        RES[("q", name)] = q
        out(f"| {name} | {p_op:.1e} | {q:.2e} | {ue[0]:.1e} | {ue[1]:.1e} | {ue[2]:.1e} |")
    ev = 3.0 / R("census_module_hours") * 8766
    RES["census_bound"] = ev
    out("")
    out("Reading: relaxed refresh turns benign chip faults into UE risk through coincidence with random errors "
        "(q rises ~1e4x vs 64 ms on raw DDR4). On DDR4 the controller must mark a chip on its first chip-confined "
        "multi-symbol correction; marking after 10 reads already uses the whole 1e-3 budget. Behind DDR5 on-die SEC, "
        "q stays small. [Correction 2026-11-04: the DDR4 rows are layout (c), 640-bit line. On a real DDR4 line "
        "(section 10.11) q is much smaller on one channel, because its lower code limit sets a lower operating BER, "
        "and negligible in lockstep, where a dead chip leaves 4 spare symbols.]")
    out(f"Census power: {R('census_module_hours'):.1e} module-hours with zero events of a mechanism bound its rate "
        f"at <= {ev:.2f} per module-year (95%). With immediate marking, that bounds its UE share at <= "
        f"{ev*RES[('q','DDR4 (c) RS-8 servoed')]:.1e} (DDR4 (c) servoed) and <= {ev*RES[('q','DDR5 behind SEC, RS-8 servoed')]:.1e} "
        "(DDR5) per module-year, against the 1e-3 budget. Each mechanism's rate is measured as events, not "
        "inferred from 1e15 codeword reads; multi-chip common-mode events (VPP droop, thermal slew faster than the "
        "scheduler) remain the residual that only fleet telemetry bounds.")

    # ---------------- 10.7 VRT pairs ----------------
    hr("10.7 VRT coincidence inside a codeword (RT-DEV-03)")
    out("Share of VRT/retention error bits arriving as same-codeword pairs (b=2) vs the BCH-12 limit (RS-8: a pair "
        "in one byte is one symbol, across chips two, so RS sees pairs as at most iid):")
    out("")
    out("| pair share | BCH-12 max raw BER |")
    out("|---|---|")
    for bf in (0.0, 0.01, 0.1, 0.3):
        out(f"| {bf:.2f} | {max_p_strategy(12, 1.0, 0.5, tgt, 'hard', bf, 2):.2e} |")
    out("")
    out("VRT state dwell times at 85 C run minutes to hours (RT-DEV-03), so the soak must re-map a subset of rows "
        "every ~20 s-20 min (<= 1/3 of the shortest dwell) as well as whole modules hourly, and must count VRT "
        "arrivals per codeword per scrub period (overdispersion vs Poisson) to feed this table.")

    # ---------------- 10.8 lot-to-lot ----------------
    hr("10.8 Lot-to-lot spread and per-module adaptive intervals (RT-PROC-02)")
    k = local_slope(I_c, "logn", sc)
    servo = R("servo_ber_guard") ** (-1.0 / k)
    out(f"Lot retention scale L ~ lognormal(0, sigma). Local tail slope at {I_c*1e3:.0f} ms (DDR5 central): BER ~ "
        f"t^{k:.1f}, so a {R('servo_ber_guard'):.0f}x BER guard costs {servo:.2f}x in interval.")
    out("")
    out("| lot sigma (ln) | fixed fleet interval (covers 1-in-1000 lot) | cut | adaptive per module (servoed), fleet-mean cut |")
    out("|---|---|---|---|")
    for sl in R("lot_sigma_ln"):
        fixed = I_c * math.exp(-3.09 * sl)
        ad = (I_c / w5) * servo * math.exp(-sl ** 2 / 2)
        RES[("lot", sl)] = (fixed, ad)
        out(f"| {sl:.2f} | {fixed*1e3:.0f} ms | {fixed/w5:.1f}x | {ad:.1f}x |")
    n100 = math.log(0.05) / math.log(0.99)
    out("")
    out(f"Reading: a fixed worst-lot interval throws away most of the gain; an adaptive controller that servos each "
        f"rank on its own corrected-error telemetry keeps most of it. Proving a 1-in-100 worst lot directly needs "
        f"~{n100:.0f} lots, so the demo proves the servo (per-module grade predicted in 1 h, held for 1,000 h), "
        "not a population floor; a vendor 1 s retention screen remains an optional bin, not a requirement.")

    # ---------------- 10.9 sort flow ----------------
    hr("10.9 Sort-flow test time for a die built to contract (RT-PROC-03)")
    pause = sum(R("sort_pauses_s")) * R("sort_patterns") * R("sort_temps")
    passes = len(R("sort_pauses_s")) * R("sort_patterns") * R("sort_temps") * 2 * R("sort_pass_s")
    out(f"Pauses {R('sort_pauses_s')} s x {R('sort_patterns')} patterns x {R('sort_temps')} temperatures = {pause:.0f} s "
        f"of pause plus {passes:.0f} s of write/read passes = {pause+passes:.0f} s per batch, i.e. "
        f"{(pause+passes)/R('sort_sites'):.2f} s per die at {R('sort_sites')} sites [ESTIMATE]. The same maps give each "
        "die's cluster spectrum (repair clusters, leave singletons). VRT growth cannot be screened at sort: it "
        "becomes a lot statistic from sampled 24-48 h soaks plus the field controller's servo and chip marking.")

    # ---------------- 10.10 new-cell routes ----------------
    hr("10.10 New-cell routes: oxide revival, stacked write (I-12627), plate-strip sensing (I-12302) (RT-DEV-05)")
    out("Stacked write devices square the leakage-tail fraction only for independent defects: p_eff = p (rho + "
        "(1 - rho) p), rho = shared-defect share. Applies to gain/oxide cells whose hold leakage is the write path, "
        "not to Si 1T1C storage-node junction/GIDL leakage. DDR4-anchor tail, RS-8 limit of a 640-bit line (128 check bits), "
        "85 C:")
    out("")
    out("| rho | p_eff at 1 s | safe interval |")
    out("|---|---|---|")
    for rho in R("stack_corr"):
        b1 = ber_ret(1.0, "logn")
        pe_ = b1 * (rho + (1 - rho) * b1)
        lo, hi = math.log(0.064), math.log(1e4)
        for _ in range(80):
            mid = (lo + hi) / 2
            bb = ber_ret(math.exp(mid), "logn")
            if bb * (rho + (1 - rho) * bb) <= p_rs:
                lo = mid
            else:
                hi = mid
        out(f"| {rho:.2f} | {pe_:.1e} | {math.exp(lo):.1f} s |")
    out("")
    cn, sw = R("plate_node_fF"), R("plate_swing_V")
    c50 = cn * 0.050 / (sw - 0.050)
    c27 = cn * 0.0266 / (sw - 0.0266)
    RES.update(c50=c50, c27=c27)
    out(f"Plate-strip sense node ({cn} fF, {sw} V swing): Cs for 50 mV = {c50:.2f} fF; for the contract's 26.6 mV = "
        f"{c27:.2f} fF (bitline sensing: 5.42 -> 2.68 fF). If I-12302 works in 3D it is a ~{c1b_fF()/c50:.0f}x margin lever (vs the contract's 1.88x) "
        "and dwarfs flags (+8%); the contract still halves the remaining Cs. Smaller Cs "
        "shortens retention at fixed leakage (section 6), so these cells need the oxide/stacked-write tail as well.")
    out("")
    out("Oxide revival (RT-DEV-05): no published IGZO array retention CDF reaches 1e-6 at 85 C; the '1e3-1e4x' "
        "figure was a typical-Ioff ratio, not a tail. The revival condition is restated as a measurement.")
    return RES


# --------------------------------------------------------------------------------------------
# 10.11 DDR4 LINE-GEOMETRY CORRECTION (2026-11-04): see the GEO_INPUTS block at the top
# --------------------------------------------------------------------------------------------
def max_p_ssc(tgt, erased=False):
    """Host-style x4 SSC on one DDR4 channel: 4 codewords of 18 byte symbols (16 data + 2 check), one symbol per chip
    (4 DQ x 2 beats). Healthy: a codeword fails at >= 2 symbol errors. One chip marked dead (1 erasure per codeword):
    no correction is left, so any further symbol error fails. Every bit error counts as its own symbol (upper bound);
    union bound over the 4 codewords."""
    ncw = int(G("ddr4_ssc_codewords"))
    nbits = (18 - (1 if erased else 0)) * 8
    a = 0 if erased else 1
    lo, hi = -26.0, -1.5
    for _ in range(90):
        mid = (lo + hi) / 2
        if ncw * pois_sf(a, nbits * 10 ** mid) <= tgt:
            lo = mid
        else:
            hi = mid
    return 10 ** lo


def section_ddr4_geometry(tgt, p_sb, p_rs, p_rs_er, RES):
    hr("10.11 DDR4 line geometry (correction 2026-11-04)")
    w4 = 0.064
    chips = int(G("ddr4_x4_chips"))
    line4 = G("ddr4_bus_bits") * 8
    lock = int(G("ddr4_lockstep_bits"))
    cap_c = G("ddr4_extra_check_bits") / (512 + G("ddr4_extra_check_bits"))
    out("Correction. Sections 10.1, 10.4 and 10.6 gave retired DDR4 the DDR5 RDIMM line: 640 bits = 512 data + 128 "
        f"check bits, RS(80,64), an x4 chip = 8 bytes. A DDR4 x4 ECC RDIMM moves {G('ddr4_bus_bits')} bits x burst 8 = "
        f"512 data + {line4 - 512} check bits per 64 B line ({(line4 - 512) / 512 * 100:.1f}%), {chips} x4 chips x 4 "
        "bytes [REPORTED; GEO_INPUTS]. Three DDR4 layouts follow. Each keeps the 2e-19 target per codeword decode (one "
        "decode per 64 B request) and the DDR3/DDR4-era tails, VRT 1x/day and 1 h scrub of section 10.1:")
    out("")
    out(f"- (a) One 72-bit channel, {line4}-bit line: RS(72,64) over bytes, t=4. A dead chip is 4 byte errors = t, so "
        "chipkill is kept but no random-error margin is left until the chip is marked, and double-chip detection is "
        "not guaranteed. Reference row: the host-style x4 SSC code (4 x RS(18,16), one symbol per chip) on the same bits.")
    out(f"- (b) Two channels in lockstep, {lock}-bit access (1024 data + 128 check): RS(144,128) over bytes, t=8; a dead "
        "chip uses 4 of 8. No capacity cost, but every 64 B request fetches 128 B (half the rank/bank parallelism, ~2x "
        "prefetch energy [REPORTED; GEO_INPUTS]).")
    out(f"- (c) CXL capacity trade: {G('ddr4_extra_check_bits')} more check bits per 512 data bits kept in DRAM data "
        f"space (one parity line per 8 data lines) -> RS(80,64) as on DDR5. Usable capacity 512/576 = "
        f"{(1 - cap_c) * 100:.1f}% ({-cap_c * 100:.1f}%), plus up to 1/8 of a line of extra reads per access when the "
        "parity line is not cached [ESTIMATE]. Layout (c) equals the old DDR4 rows exactly.")
    out("")
    pa, pa_er = max_p_rs(tgt, t_sym=4, n_sym=72), max_p_rs(tgt, t_sym=4, n_sym=72, erased=4)
    pb, pb_er = max_p_rs(tgt, t_sym=8, n_sym=144), max_p_rs(tgt, t_sym=8, n_sym=144, erased=4)
    ps, ps_er = max_p_ssc(tgt), max_p_ssc(tgt, erased=True)
    pa_bch, pb_bch = max_p_hard(6, 512, 10, tgt), max_p_hard(11, 1024, 11, tgt)
    RES.update(g_pa=pa, g_pa_er=pa_er, g_pb=pb, g_pb_er=pb_er, g_ps=ps, g_ps_er=ps_er, g_pa_bch=pa_bch, g_pb_bch=pb_bch)
    out("Code limits (max iid raw BER at the target; no on-die ECC):")
    out("")
    out("| layout | data + check bits | capacity cost | code | chipkill | max raw BER | one chip marked dead |")
    out("|---|---|---|---|---|---|---|")
    out(f"| (a) one channel | 512 + 64 | 0 | host SSC, 4 x RS(18,16) | yes (single symbol) | {ps:.1e} | {ps_er:.1e} |")
    out(f"| (a) one channel | 512 + 64 | 0 | RS(72,64) bytes, t=4 | yes, no spare | {pa:.2e} | {pa_er:.2e} |")
    out(f"| (a) one channel | 512 + 64 | 0 | BCH t=6 (m=10, 60 bits) | no | {pa_bch:.2e} | - |")
    out(f"| (b) lockstep | 1024 + 128 | 0 (128 B access) | RS(144,128) bytes, t=8 | yes, 4 spare | {pb:.2e} | {pb_er:.2e} |")
    out(f"| (b) lockstep | 1024 + 128 | 0 (128 B access) | BCH t=11 (m=11, 121 bits) | no | {pb_bch:.2e} | - |")
    out(f"| (c) capacity trade | 512 + 128 | {cap_c * 100:.1f}% | RS(80,64) bytes, t=8 (old DDR4 row) | yes | {p_rs:.2e} | "
        f"{p_rs_er:.2e} |")
    out(f"| (c) capacity trade | 512 + 128 | {cap_c * 100:.1f}% | BCH-12 (old DDR4 row) | no | {p_sb:.2e} | - |")
    out("")
    mult = 1 + V("vrt_growth_per_day") * V("scrub_interval_h") / 24.0
    b64 = ber_ret(w4, "logn") * mult

    def fiv(i):
        return "<=16 ms" if i <= 0.0161 else (f"{i * 1e3:.0f} ms" if i < 1.0 else f"{i:.2f} s")

    out(f"Safe refresh interval, retired DDR4 (DDR3/DDR4-era anchors, no derate). The lognormal tail at 64 ms already "
        f"carries {b64:.1e} (VRT included), so a code whose limit sits below that gives no relaxation [model tail; real "
        "parts repair those cells at test].")
    out("")
    out("| layout / code | retention model | 85 C | x of 64 ms | 65 C | 45 C |")
    out("|---|---|---|---|---|---|")
    rows = [("(a) host SSC 4 x RS(18,16)", ps, ("logn",)),
            ("(a) RS(72,64)", pa, ("logn", "pow5", "pow3")),
            ("(a) RS(72,64), one chip dead", pa_er, ("logn", "pow5")),
            ("(a) BCH t=6 (no chipkill)", pa_bch, ("logn",)),
            ("(b) lockstep RS(144,128)", pb, ("logn", "pow5", "pow3")),
            ("(b) lockstep RS(144,128), one chip dead", pb_er, ("logn", "pow5")),
            ("(b) lockstep BCH t=11 (no chipkill)", pb_bch, ("logn",)),
            ("(c) RS(80,64), -11.1% capacity", p_rs, ("logn", "pow5", "pow3")),
            ("(c) RS(80,64), one chip dead", p_rs_er, ("logn", "pow5")),
            ("(c) BCH-12 (no chipkill)", p_sb, ("logn",))]
    iv = {}
    for name, plim, mdls in rows:
        for mdl in mdls:
            if plim < b64:
                r = [0.0, 0.0, 0.0]
                iv[(name, mdl)] = r
                out(f"| {name} | {mdl} | none (limit < 64 ms tail BER) | 1.0x at best | - | - |")
                continue
            r = [p_max_interval(mdl, plim, ts) for ts in (1.0, 4.0, 16.0)]
            iv[(name, mdl)] = r
            out(f"| {name} | {mdl} | {fiv(r[0])} | {r[0] / w4:.1f}x | {fiv(r[1])} | {fiv(r[2])} |")
    for key, name in (("a", "(a) RS(72,64)"), ("b", "(b) lockstep RS(144,128)"), ("c", "(c) RS(80,64), -11.1% capacity")):
        RES[f"g_I{key}"] = iv[(name, "logn")][0]
        RES[f"g_I{key}_p"] = iv[(name, "pow5")][0]
        RES[f"g_I{key}_o"] = iv[(name, "pow3")][0]
        RES[f"g_I{key}65"] = iv[(name, "logn")][1]
    for key, name in (("a", "(a) RS(72,64), one chip dead"), ("b", "(b) lockstep RS(144,128), one chip dead"),
                      ("c", "(c) RS(80,64), one chip dead")):
        RES[f"g_I{key}_d"] = iv[(name, "logn")][0]
        RES[f"g_I{key}_d65"] = iv[(name, "logn")][1]
    out("")
    out("Decoder load (as section 10.4; each bit error its own symbol):")
    out("")
    out("| case | operating raw BER | lines with any error | lines needing BM | mean added ns |")
    out("|---|---|---|---|---|")
    for name, p_op, nb in (("(a) RS(72,64) at limit", pa, line4), ("(a) RS(72,64) servoed", pa / R("servo_ber_guard"), line4),
                           ("(b) RS(144,128) at limit", pb, lock), ("(b) RS(144,128) servoed", pb / R("servo_ber_guard"), lock),
                           ("(c) RS(80,64) servoed (old DDR4 row)", p_rs / R("servo_ber_guard"), 640)):
        lam = nb * p_op
        p1 = 1 - math.exp(-lam)
        p2 = 1 - math.exp(-lam) * (1 + lam)
        mean = R("lat_fast_ns") + (p1 - p2) * R("lat_single_ns") + p2 * R("lat_bm_ns")
        out(f"| {name} | {p_op:.1e} | {p1 * 100:.3f}% | {p2 * 100:.5f}% | {mean:.2f} |")
    out("")
    nf = dcp.INPUTS["rdimm_dies"] * R("multibit_fault_fit_per_die") * 1e-9 * 8766
    ev = RES["census_bound"]
    out(f"Chip-fault coincidence (as section 10.6; {nf:.4f} multi-bit faults per module-year, 40-die basis kept; a 64 GB "
        "DDR4 x4 RDIMM has 36-72 dies, so scale by 0.9-1.8x [ESTIMATE]). q = P(a dead, not yet marked chip plus "
        "random symbol errors elsewhere exceed the code on one read):")
    out("")
    out("| case | operating raw BER | q | mark after 1 read | after 10 | after 100 | census-bound UE share |")
    out("|---|---|---|---|---|---|---|")
    other_a = (chips - 1) * 32
    other_b = (2 * chips - 1) * 32
    for name, p_op, kind in (("(a) RS(72,64) at limit", pa, "a"), ("(a) RS(72,64) servoed", pa / R("servo_ber_guard"), "a"),
                             ("(b) RS(144,128) at limit", pb, "b"), ("(b) RS(144,128) servoed", pb / R("servo_ber_guard"), "b"),
                             ("(c) RS(80,64) servoed (old DDR4 row)", p_rs / R("servo_ber_guard"), "c")):
        if kind == "a":
            q = 1 - math.exp(-other_a * p_op)  # t=4 used up by the dead chip's 4 bytes
        elif kind == "b":
            q = pois_sf(4, other_b * p_op)  # 4 of t=8 left after the dead chip
        else:
            q = 1 - math.exp(-576 * p_op)  # worst line: the dead chip holds 4 data + 4 parity bytes
        RES[("gq", name)] = q
        ue = [nf * n * q for n in (1, 10, 100)]
        out(f"| {name} | {p_op:.1e} | {q:.2e} | {ue[0]:.1e} | {ue[1]:.1e} | {ue[2]:.1e} | {ev * q:.1e} |")
    out("")
    ia, ib, ic = RES["g_Ia"], RES["g_Ib"], RES["g_Ic"]
    out(f"Reading: at 85 C (lognormal, central) one 72-bit channel gives {fiv(ia)} = {ia / w4:.1f}x of 64 ms with chipkill "
        f"(pessimistic {RES['g_Ia_p'] / w4:.1f}x) and no relaxation once a chip is dead ({fiv(RES['g_Ia_d'])}); the host "
        f"SSC code gives none. Lockstep gives {fiv(ib)} = {ib / w4:.1f}x (pessimistic {RES['g_Ib_p'] / w4:.1f}x) and "
        f"{fiv(RES['g_Ib_d'])} = {RES['g_Ib_d'] / w4:.1f}x with a chip dead, at the cost of 128 B accesses. The old "
        f"~{ic / w4:.0f}x ({fiv(ic)}) needs layout (c) and costs {cap_c * 100:.1f}% of capacity. The DDR5 rows are "
        "unchanged: a DDR5 RDIMM sub-channel really carries 128 check bits per 64 B line. At 65 C: (a) "
        f"{fiv(RES['g_Ia65'])}, (b) {fiv(RES['g_Ib65'])}, (c) {fiv(RES['g_Ic65'])}.")
    vrt_txt = []
    for key, plim in (("a", pa), ("b", pb), ("c", p_rs)):
        if p_max_interval("logn", plim, 1.0, 0.0, 1 / 6) < 0.5:
            vrt_txt.append(f"({key}) cannot hold 0.5 s at any growth rate")
            continue
        lo, hi = 0.0, 1e5
        for _ in range(60):
            mid = (lo + hi) / 2
            if p_max_interval("logn", plim, 1.0, mid, 1 / 6) >= 0.5:
                lo = mid
            else:
                hi = mid
        vrt_txt.append(f"({key}) holds it up to ~{lo:.0f}x/day ({fiv(p_max_interval('logn', plim, 1.0, 100.0, 1 / 6))} "
                       "at 100x/day)")
    out("Kill #4 basis (10-minute scrub, 85 C, lognormal: the VRT growth at which 0.5 s can no longer be held): "
        + "; ".join(vrt_txt) + ".")
    kill = [k for k in "abc" if RES[f"g_I{k}65"] < 4 * w4]
    go = [k for k in "abc" if RES[f"g_I{k}"] >= 6 * w4 and RES[f"g_I{k}65"] >= 24 * w4]
    out(f"Against the dossier's DDR4 gate (model tail, central): kill #1 (<4x = 256 ms at 65 C) triggered in "
        f"{', '.join('(' + k + ')' for k in kill) if kill else 'no layout'}; GO (>=6x = 0.38 s at 85 C and >=24x at 65 C) "
        f"met in {', '.join('(' + k + ')' for k in go) if go else 'no layout'}. With 8 check bytes, 4 byte errors is the "
        "most any byte code can correct (Singleton bound). A binary code that corrects BCH-6-class random bits and also "
        "a whole x4 chip in 64 check bits is not known to us; the Hamming bound does not forbid one (~2^46 + ~2^36 "
        "patterns < 2^64 syndromes), so it stays an open coding question, as RT-CIRC-03 recorded for the 128-bit case.")
    return RES


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
    inp += ["", "## RT_INPUTS (red-team revisions)", "", "| key | value | source / basis |", "|---|---|---|"]
    for k, (v, s) in RT_INPUTS.items():
        inp.append(f"| {k} | {v} | {s} |")
    inp += ["", "## GEO_INPUTS (DDR4 line-geometry correction, 2026-11-04)", "", "| key | value | source / basis |",
            "|---|---|---|"]
    for k, (v, s) in GEO_INPUTS.items():
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
    RT = section_redteam(tgt, p_sb, p_od, p_rs, burst_res[(3, 0.0)][2], sig)
    section_ddr4_geometry(tgt, p_sb, p_rs, burst_res[(3, 0.0)][2], RT)
    hr("Headline (revised after red team)")
    out(f"- Commodity DDR5 RDIMM, chipkill kept (RS-8 behind on-die SEC, max internal BER {RT['p_rs_od']:.1e}), DDR5 "
        f"retention derated 0.5x: safe interval at 85 C {RT['I_c']*1e3:.0f} ms central / {RT['I_p']*1e3:.0f} ms "
        f"pessimistic = {RT['cut_c']:.1f}x / {RT['cut_p']:.1f}x refresh energy vs the 32 ms spec; degraded mode "
        f"(chip dead) {RT['I_d']*1e3:.0f} ms = {RT['cut_d']:.1f}x; at 65 C {RT['I_c65']*1e3:.0f} ms.")
    out(f"- Retired DDR4 behind CXL, chipkill kept (corrected 2026-11-04, section 10.11; vs 64 ms, 85 C central / "
        f"pessimistic): two channels in lockstep {RT['g_Ib']*1e3:.0f} ms = {RT['g_Ib']/0.064:.1f}x / "
        f"{RT['g_Ib_p']/0.064:.1f}x, {RT['g_Ib_d']/0.064:.1f}x with a chip dead; one channel {RT['g_Ia']*1e3:.0f} ms = "
        f"{RT['g_Ia']/0.064:.1f}x / {RT['g_Ia_p']/0.064:.1f}x, {RT['g_Ia_d']/0.064:.1f}x with a chip dead. The earlier "
        f"{RT['g_Ic']/0.064:.1f}x / {RT['g_Ic_p']/0.064:.1f}x ({RT['g_Ic_d']/0.064:.1f}x degraded) used DDR5's 128-bit "
        "side band and needs a layout that spends 11.1% of DDR4 capacity on check bits.")
    out(f"- Refresh power {RT['base32']:.2f} W -> {RT['base32']-RT['sav']:.3f} W per 64 GB; with 20% self-refresh "
        f"residency (hybrid policy) ${RT['usd02']:.2f} per module over 5 yr. 64Gb (tRFC 700 ns) blocked time "
        f"{RT['b64']*100:.0f}% -> {RT['b64c']*100:.1f}% (all-bank basis).")
    out(f"- Flag leg: net {RT['flag_net_lo']*100:+.1f}% to {RT['flag_net_hi']*100:+.1f}% of die even with ideal flags; "
        "a delayed-strobe flag sees skew, not signal. Removed from the headline and the GO/NO-GO.")
    out(f"- Margin for new cells unchanged at 1.88x (50 -> 26.6 mV, Cs 5.4 -> 2.7 fF) without flags; plate-strip "
        f"sensing (I-12302) would need only {RT['c50']:.2f} -> {RT['c27']:.2f} fF.")
    hr("Headline (original dossier basis, superseded by the revised headline above)")
    out(f"- Target {tgt:.1e} per 64 B read; the concept's t=8 is ~100x short; t={res_t[1e-4]} (17.6%) needed at 1e-4 "
        "with hard decisions.")
    out(f"- A commodity DDR5 ECC RDIMM's existing 128-bit side band takes iid raw BER up to {p_sb:.1e} (BCH-12) or "
        f"{p_rs:.1e} with byte-confined clusters and chipkill (RS-8); behind DDR5 on-die SEC, internal BER up to "
        f"{p_od:.1e}. BCH-12 tolerates only ~{bf3*100:.2g}% of error bits in 3-bit clusters at 1e-4.")
    L = pm
    out(f"- Refresh interval at 85 C, iid / clustered: pow3 {L[('pow3','BCH-12 iid')][0]:.2f} / "
        f"{L[('pow3','RS-8 clustered')][0]:.2f} s; lognormal {L[('logn','BCH-12 iid')][0]:.2f} / "
        f"{L[('logn','RS-8 clustered')][0]:.2f} s; pow5 {L[('pow5','BCH-12 iid')][0]:.2f} / "
        f"{L[('pow5','RS-8 clustered')][0]:.2f} s. At 1 s: refresh 0.49 -> 0.03 W per 64 GB (15x vs 64 ms), "
        f"${usd_gb:.3f}/GB of energy over 5 yr; tRFC loss 7.6% -> 0.24% (16Gb, 32 ms-window fix).")
    out(f"- Margin: 1e-4 buys 7 -> 3.72 sigma (50 -> 26.6 mV, Cs 5.4 -> 2.7 fF). Flags add only ~"
        f"{(Qinv(max_p_strategy(8, 0.0, V('flag_window_sigma'), tgt, 'hard'))/Qinv(flag_table[0.0][4])-1)*100:.0f}% "
        f"more (Chase t={flag_table[0.0][3]} vs hard t={flag_table[1.0][0]}) and nothing for refresh-latched errors.")
    write_md()
    print(f"\n[wrote {OUT_MD}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
