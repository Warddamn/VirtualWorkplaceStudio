#!/usr/bin/env python3
"""
B4_architecture_estimates.py -- first-principles arithmetic behind the phase-B lens
"ARCHITECTURE: DO DRAM'S JOB WITH LESS DRAM" (dram-moonshot, agent B4-architecture).
Written 2026-11-01. Pure standard library; `python3` exits 0.

Feeds research/phaseB/B4-architecture.json and B4-architecture_notes.md. Tags:
  [A1]        reused from models/dram_cell_physics.py (imported) or A1_scaling_limits.md
  [A3]        reused from A3_research_frontier.md
  [REPORTED]  a number from a search snippet logged in research/sources/B4-architecture.jsonl
  [ESTIMATE]  my assumption, logged in research/assumptions/B4-architecture.md
  [UNVERIFIED] training knowledge with no URL found this session

One section per idea card (B4-01 ... B4-21). Each prints the numbers quoted in the card.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "models")))
import dram_cell_physics as A1  # noqa: E402  (helpers only; main() is guarded)

# ------------------------------------------------------------------------------------------
# Shared anchors [A1]
# ------------------------------------------------------------------------------------------
I = A1.INPUTS
VARY = I["v_array"]                      # 1.05 V
V_HALF = VARY / 2                        # precharge, 0.525 V
DROOP = 0.15 * VARY                      # 155 mV droop budget for a stored "1" [A1]
V_SIG_END = V_HALF - DROOP               # 0.37 V cell-minus-precharge at end of retention
CBL_512 = A1.c_bitline_fF(512)           # 34.7 fF
CBL_64 = A1.c_bitline_fF(64)             # 7.84 fF
DV_HARD_mV = I["dv_min_mV"]              # 50 mV hard-decision budget [A1]
E_REF_fJ = 46.0                          # energy per bit-refresh [A1]
D_1B = 16.0 / I["die_1b_mm2"]            # 0.447 Gb/mm2 die-level [A1]
COST_GB = 1.48                           # $/GB DDR5 1-beta [ram-venture cost stack]
RDIMM_REF_W = 0.49                       # refresh W per 64GB RDIMM at 64 ms [A1]
CAP_H_NM = I["cap_height_nm"]            # 1,300 nm


def hr(t):
    print("\n" + "=" * 100 + "\n" + t + "\n" + "=" * 100)


def phi_tail(z):
    """One-sided Gaussian tail Q(z)."""
    return 0.5 * math.erfc(z / math.sqrt(2))


def z_for_tail(p):
    lo, hi = 0.0, 40.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if phi_tail(mid) > p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def poisson_tail(lam, t):
    """P(X > t) for X ~ Poisson(lam), computed stably."""
    term = math.exp(-lam)
    cdf = term
    for k in range(1, t + 1):
        term *= lam / k
        cdf += term
    # direct sum of the tail avoids 1-cdf cancellation for tiny tails
    tail = 0.0
    term = math.exp(-lam)
    for k in range(1, t + 60):
        term *= lam / k
        if k > t:
            tail += term
    return tail


def bch_t_needed(n_data, ber, target, m):
    """Smallest t such that P(>t errors in an n_data + m*t codeword) <= target."""
    for t in range(0, 200):
        n = n_data + m * t
        if poisson_tail(n * ber, t) <= target:
            return t, m * t
    return None, None


def cs_min_fF(cbl, dv_mV, v_sig=V_SIG_END):
    return A1.cs_min_fF(cbl, dv_mV, v_sig)


# Sense-amp offset model [ESTIMATE]: A1's 50 mV hard budget is read as z = 7.03 (1e-12 per bit)
SIGMA_EFF_mV = DV_HARD_mV / z_for_tail(1e-12)

# Retention-tail model [ESTIMATE, calibrated to RAIDR's "~1,000 cells in 32 GB below 256 ms"
# (UNVERIFIED training knowledge) and a cubic power-law tail; cross-checked against
# Flikker-era recollections of ~1e-7 at 1 s and ~1e-3 at 20 s (UNVERIFIED)].
BER_256MS = 1000 / (32 * 8 * 2 ** 30)    # ~3.6e-9
TAIL_EXP = 3.0
T_DERATE_85C = 0.25                      # assume calibration at ~65 C; 85 C shortens times 4x [ESTIMATE]


def retention_ber(t_s, cs_scale=1.0, temp_scale=T_DERATE_85C):
    """Fraction of cells failing at refresh interval t (85 C default). cs_scale: Cs/Cs_1b."""
    t0 = 0.256 * cs_scale * temp_scale
    return BER_256MS * (t_s / t0) ** TAIL_EXP


# ------------------------------------------------------------------------------------------
def card01():
    hr("B4-01  ECC-paid capacitor: let the code, not the capacitor, carry the last 6 sigma")
    print(f"sigma_eff (SA offset + coupling) = {SIGMA_EFF_mV:.2f} mV  (50 mV = 7.03 sigma) [ESTIMATE]")
    rows = []
    for ber in (1e-12, 1e-6, 1e-4, 1e-3):
        dv = SIGMA_EFF_mV * z_for_tail(ber)
        cs512 = cs_min_fF(CBL_512, dv)
        cs64 = cs_min_fF(CBL_64, dv)
        h = CAP_H_NM * cs512 / cs_min_fF(CBL_512, DV_HARD_mV)
        rows.append((ber, dv, cs512, cs64, h))
        print(f"raw BER {ber:7.0e}: dV_min {dv:5.1f} mV | Cs_min 512-cell BL {cs512:4.2f} fF "
              f"(pillar ~{h:5.0f} nm, AR {h/21.1:4.1f}) | 64-cell BL {cs64:4.2f} fF")
    # retention check for the shrunken capacitor at 64 ms, 85 C
    cs_ratio = rows[2][2] / cs_min_fF(CBL_512, DV_HARD_mV)
    rb = retention_ber(0.064, cs_scale=cs_ratio)
    print(f"Retention BER at 64 ms, 85 C with Cs x{cs_ratio:.2f}: {rb:.1e} (fits inside a 1e-4 budget)")
    # ECC cost at 64 B granularity
    for ber in (1e-4, 1e-3):
        t, par = bch_t_needed(512, ber, 1e-15, 10)
        print(f"BCH over 512 data bits, raw BER {ber:.0e}, codeword fail <=1e-15: t = {t}, "
              f"parity {par} b = {par/512*100:.1f}% (DDR5 on-die ECC is 6.25%)")
    t, par = bch_t_needed(8192, 1e-4, 1e-15, 14)
    print(f"Page-level BCH (1 KB page) at 1e-4: t = {t}, parity {par} b = {par/8192*100:.1f}%")


def card02():
    hr("B4-02  Scrub-as-refresh: long refresh interval, row-level ECC, accumulate-then-scrub")
    for t in (0.064, 0.256, 0.5, 1.0, 2.0, 4.0):
        print(f"refresh {t*1e3:6.0f} ms at 85 C: raw retention BER ~{retention_ber(t):.1e} "
              f"| refresh energy x{0.064/t:.3f} | 64GB RDIMM refresh {RDIMM_REF_W*0.064/t*1e3:6.1f} mW")
    ber = retention_ber(1.0) * 3   # x3 for VRT accumulation between scrubs [ESTIMATE]
    t, par = bch_t_needed(8192, ber, 1e-15, 14)
    print(f"1 s refresh, BER x3 for VRT = {ber:.1e}: page BCH t = {t}, parity {par/8192*100:.2f}%")
    # syndrome energy if decoded every refresh vs every 60 s
    xor_per_bit = 14 * t / 2
    e_xor_fJ = 2.0   # DRAM-periphery XOR toggle [ESTIMATE]
    e_dec = xor_per_bit * e_xor_fJ
    base = E_REF_fJ / 0.064
    every = (E_REF_fJ + e_dec) / 1.0
    lazy = E_REF_fJ / 1.0 + e_dec / 60.0
    print(f"syndrome energy ~{e_dec:.0f} fJ/bit per decode")
    print(f"refresh power per bit: baseline {base:.0f} fJ/s | decode every refresh {every:.0f} fJ/s "
          f"(x{base/every:.1f}) | scrub every 60 s {lazy:.0f} fJ/s (x{base/lazy:.1f})")
    for name, trfc, trefi in (("16Gb", 295, 3900), ("64Gb", 1600, 7800)):
        print(f"{name}: refresh busy time {trfc/trefi*100:.1f}% -> {trfc/trefi*100*0.064:.2f}% at 1 s")
    # asymmetric errors: only charged cells can fail
    for frac in (0.5, 0.3):
        print(f"fraction of cells charged after charge-minimising encoding {frac:.0%}: at-risk cells x{frac/0.5:.1f}; "
              f"interval stretch at equal BER x{(0.5/frac)**(1/TAIL_EXP):.2f}")


def card03():
    hr("B4-03  Lifetime-leased refresh: streamed and dead data are never refreshed")
    for hbm_gb, bw_tbs in ((141, 4.8), (192, 8.0), (288, 16.0)):
        sweep_ms = hbm_gb / (bw_tbs * 1000) * 1e3
        print(f"HBM {hbm_gb} GB at {bw_tbs} TB/s: a full sweep takes {sweep_ms:5.1f} ms "
              f"({'< 32 ms: every row is restored by use' if sweep_ms < 32 else '> 32 ms'})")
    stack_bits = 36 * 8e9
    p_ref = stack_bits * E_REF_fJ * 1e-15 / 0.032
    print(f"36 GB HBM stack refresh at 32 ms (hot): {p_ref:.2f} W per stack, {8*p_ref:.1f} W per 8 stacks")
    for busy in (0.05, 0.10, 0.15):
        print(f"refresh busy {busy:.0%} recovered -> decode throughput x{1/(1-busy):.3f} (bandwidth-bound)")
    for idle in (0.3, 0.5):
        print(f"server with {idle:.0%} of DRAM free/dead: refresh energy x{1-idle:.1f} from leases alone")


def card04():
    hr("B4-04  Significance-split memory: protect sign+exponent, relax the mantissa")
    exp_bits = 2.9    # DFloat11: exponent entropy ~2.6 b; Huffman ~2.9 b incl. table [REPORTED + ESTIMATE]
    for fmt, s, e_ent, m in (("BF16", 1, exp_bits, 7), ("FP8 E4M3", 1, 2.0, 3), ("FP4 E2M1", 1, 1.5, 1)):
        total = s + (8 if fmt == "BF16" else 4 if fmt == "FP8 E4M3" else 2) + m
        base = total * 1.125            # server: 12.5% ECC
        prot = (s + e_ent) * 1.125
        new = prot + m
        ref_share = (prot + m * 0.064 / 1.0) / base
        print(f"{fmt}: baseline {base:.1f} cells/value -> {new:.1f} (protected {prot:.1f} + approx {m}) "
              f"= x{base/new:.2f} capacity; refresh energy per value x{ref_share:.2f}")
    v_lo = 0.75
    print(f"mantissa planes at VARY {v_lo} V: array CV^2 x{(v_lo/VARY)**2:.2f}")
    q_hi, q_lo = z_for_tail(1e-15), z_for_tail(1e-6)
    print(f"low-swing mantissa lanes: BER 1e-15 needs Q={q_hi:.2f}, 1e-6 needs Q={q_lo:.2f}: "
          f"swing x{q_lo/q_hi:.2f}, driver energy x{(q_lo/q_hi)**2:.2f} (voltage-mode)")


def card05():
    hr("B4-05  Approximate 4-level DRAM for low-order planes and 2-bit KV")
    cs = A1.cap_pillar_fF(21.1, 1300.0, 0.55)
    for n, cbl in ((512, CBL_512), (128, A1.c_bitline_fF(128))):
        att = cs / (cs + cbl)
        slc = V_HALF * att * 1e3
        mlc_half = (VARY / 3) / 2 * att * 1e3
        z = mlc_half / SIGMA_EFF_mV
        print(f"{n}-cell BL: SLC fresh signal {slc:.0f} mV | MLC half level-gap {mlc_half:.1f} mV "
              f"= {z:.2f} sigma -> level error {2*phi_tail(z):.1e} per read")
    print("4-level DRAM for exact data needed ~3x the capacitor (Murotani, ISSCC 1997, via patent)")
    print("KV at 2-bit (KIVI): SLC 2 cells/element -> MLC 1 cell/element (x2); vs BF16 SLC 16 cells (x16)")
    prot = (1 + 2.9) * 1.125
    print(f"BF16 with B4-04 split + MLC mantissa: {prot:.1f} + 3.5 = {prot+3.5:.1f} cells vs 18 -> x{18/(prot+3.5):.2f}")


def card06():
    hr("B4-06  Graceful-forgetting KV memory [SPECULATIVE]")
    # monotone droop: a 4-level magnitude loses one level when droop > VARY/3
    for sigma_ln in (0.6, 1.0):
        # median cell keeps a level ~ (VARY/3)/droop_rate; spread of decay times across cells
        p10 = math.exp(-1.2816 * sigma_ln)
        p90 = math.exp(1.2816 * sigma_ln)
        print(f"leakage spread sigma_ln={sigma_ln}: 10-90% decay-time ratio {p90/p10:.1f}x "
              f"(forgetting is randomised across elements, not per token)")
    kv_tok = 8 * 128 * 80 * 2 * 2   # 70B-class GQA, BF16 bytes per token
    print(f"KV per token (70B GQA, BF16) = {kv_tok/1e3:.0f} KB; at 128k context = {kv_tok*131072/1e9:.0f} GB")
    e_ref_tok = kv_tok * 8 * E_REF_fJ * 1e-15 / 0.064
    print(f"refresh power per stored token {e_ref_tok*1e6:.2f} uW; recompute (2 x 70e9 FLOP x 1 pJ) "
          f"= {2*70e9*1e-12:.2f} J -> refresh beats recompute until {2*70e9*1e-12/e_ref_tok:,.0f} s")


def card07():
    hr("B4-07  Tensor-aware codec at the memory controller (lossless exponent + optional lossy KV)")
    bits = 1 + 2.9 + 7
    print(f"BF16 -> {bits:.1f} b/value lossless: capacity and bandwidth x{16/bits:.2f} (DFloat11 reports ~70% size)")
    e_save = (16 - bits) * 3.5
    print(f"interface energy saved {e_save:.1f} pJ/value at 3.5 pJ/bit vs decode ~0.2-0.5 pJ/value [ESTIMATE]")
    print("lossy KV at 2 bit (KIVI): 2.6x peak memory incl. weights, up to 4x batch [REPORTED]")
    print("decoder placement: base die gives capacity only; GPU-side decode also saves the ~2.5 pJ/bit interposer path")


def card08():
    hr("B4-08  Compression-funded ECC buys slow refresh for compressible lines")
    t, par = bch_t_needed(512 - 80, 1e-4, 1e-15, 10)
    print(f"64 B line, BCH t={t} needs {par} parity bits = {par/8:.0f} B -> line must compress to <= {64 - par/8 - 1:.0f} B")
    print(f"BF16 tensor line: 32 values x {1+2.9+7:.1f} b = {32*(1+2.9+7)/8:.0f} B (+ Huffman table amortised)")
    for t_ref in (0.5, 1.0, 2.0):
        b = retention_ber(t_ref)
        print(f"refresh {t_ref:.1f} s at 85 C: raw BER {b:.1e} {'<=' if b <= 1e-4 else '>'} 1e-4 -> "
              f"refresh energy x{0.064/t_ref:.3f} on fully compressible rows")


def card09():
    hr("B4-09  Top-k KV from MSB-plane sketches scored in memory")
    kv_tok = 8 * 128 * 80 * 2 * 2
    L = 131072
    full = kv_tok * L
    sketch_frac = 4 / 16 * 0.5     # 4 MSB planes of K only
    k = 2048
    sparse = full * (sketch_frac + k / L)
    print(f"dense attention reads {full/1e9:.1f} GB per step per sequence at 128k")
    print(f"sketch (4 of 16 planes of K) + top-{k} full K,V: {sparse/1e9:.2f} GB -> x{full/sparse:.1f} less traffic")
    print(f"HBM holds sketches only: {sketch_frac:.1%} of KV -> x{1/sketch_frac:.0f} less HBM for KV")
    score_bytes = 2 * 8 * L      # one FP16 score per KV head per token
    sk_bytes = full * sketch_frac
    print(f"in-memory scoring returns {score_bytes/1e6:.1f} MB of scores instead of {sk_bytes/1e9:.2f} GB of sketch "
          f"(x{sk_bytes/score_bytes:.0f})")


def card10():
    hr("B4-10  Row-RAID: in-bank XOR parity rows built with triple-row activation")
    for g in (16, 32, 64):
        print(f"group of {g} rows + 1 parity: capacity overhead {1/g*100:.1f}%")
    aap_per_xor, t_aap_ns = 6, 50
    g = 32
    print(f"building parity for {g} rows: {(g-1)*aap_per_xor} row-cycles x {t_aap_ns} ns = "
          f"{(g-1)*aap_per_xor*t_aap_ns/1e3:.1f} us per group (once per weight load) [ESTIMATE]")
    print("hammer victims are rows +/-1, +/-2: interleave so adjacent rows sit in different groups")
    print("PRAC overhead today <13%, future up to 94% [REPORTED]; Row-RAID cost 3% capacity + scrub")


def card11():
    hr("B4-11  Erasure-coded (or spared) memory stacks")
    def p_ok(n, f, y):
        return sum(math.comb(n, k) * (1 - y) ** k * y ** (n - k) for k in range(f + 1))
    for y in (0.98, 0.95, 0.90):
        for data, par in ((12, 1), (16, 2)):
            plain = y ** data
            coded = p_ok(data + par, par, y)
            wafer_plain = 1 / plain
            wafer_coded = (data + par) / data / coded
            print(f"per-die-in-stack yield {y:.2f}: {data}-high plain {plain:.3f} | {data}+{par} tolerant "
                  f"{coded:.3f} | dies per good-stack-bit x{wafer_plain/wafer_coded:.2f} better")


def card12():
    hr("B4-12  Weight-streaming DRAM die (few banks, no refresh, big mats)")
    eff_ddr5 = 0.508
    eff_hbm = eff_ddr5 / 1.40
    for eff_s in (0.45, 0.50, 0.55):
        print(f"streaming die array eff {eff_s:.2f} vs HBM ~{eff_hbm:.2f}: area/bit x{eff_hbm/eff_s:.2f} of HBM")
    print("HBM ~3x DDR5 wafer/bit [REPORTED]: if area tax halves and stack yield +10%, ~1.8-2.2x DDR5")


def card13():
    hr("B4-13  Thermal arbitrage: keep bits away from the GPU's heat")
    for t_hot, t_cool in ((85, 45), (85, 35), (95, 35)):
        rule = 2 ** ((t_hot - t_cool) / 10)
        out = []
        for ea in (0.25, 0.55):
            k = 8.617e-5
            out.append(math.exp(ea / k * (1 / (t_cool + 273.15) - 1 / (t_hot + 273.15))))
        print(f"{t_hot} C -> {t_cool} C: rule-of-thumb x{rule:.0f}; Arrhenius Ea 0.25 eV x{out[0]:.1f}, "
              f"0.55 eV x{out[1]:.1f}")
    i_tail = 13e-15 / 16
    for cs in (4.0, 3.8):
        droop = i_tail * 0.064 / (cs * 1e-15) * 1e3
        print(f"tail leak /16 at cool: Cs {cs} fF droops {droop:.1f} mV in 64 ms -> Cs floor set by sensing "
              f"(no-droop min {cs_min_fF(CBL_512, DV_HARD_mV, V_HALF):.1f} fF)")


def card14():
    hr("B4-14  Photonic periphery wafer bonded under the DRAM cell array")
    for gbps_per_lambda, lambdas in ((32, 16), (64, 8)):
        print(f"{lambdas} wavelengths x {gbps_per_lambda} Gb/s = {lambdas*gbps_per_lambda/8:.0f} GB/s per waveguide")
    die_bw = 128   # GB/s per 16-32 Gb die (HBM-class per die share) [ESTIMATE]
    print(f"a die needing {die_bw} GB/s uses {die_bw/64:.0f} waveguides at 64 GB/s each")
    print("energy: mod+drv+rx ~1 pJ/b + laser ~1 pJ/b + ring tuning 0.1-1 pJ/b = 2-3 pJ/b (vs HBM 3.4-3.5, Celestial 2.4-6.2)")


def card15():
    hr("B4-15  GRS-linked LPDDR 'HBM-lite' on organic substrate")
    lp_core, lp_io_short, grs, buf = 1.5, 0.5, (0.54, 1.17), 0.2
    lo = lp_core + lp_io_short + grs[0] + buf
    hi = lp_core + lp_io_short + grs[1] + buf
    print(f"energy/bit: LPDDR core {lp_core} + short LPDDR I/O {lp_io_short} + GRS {grs} + buffer {buf} "
          f"= {lo:.1f}-{hi:.1f} pJ/b vs HBM3E 3.44 [REPORTED]")
    print("wafer/bit: LPDDR ~1x DDR5 vs HBM ~3x -> ~3x fewer wafers per bit (stack packaging aside)")
    lanes_per_mm, gbps = 50, 25
    print(f"shoreline: {lanes_per_mm} lanes/mm x {gbps} Gb/s = {lanes_per_mm*gbps/8:.0f} GB/s per mm per layer [ESTIMATE]")


def card16():
    hr("B4-16  HBF weight tier with read-disturb-aware management")
    for model_gb, stack_tbs in ((400, 1.6), (100, 1.6), (50, 1.6)):
        tok_s = stack_tbs * 1000 / model_gb
        reads_day = tok_s * 86400
        for limit in (1e5, 1e6):
            reclaims_yr = reads_day / limit * 365
            print(f"{model_gb} GB weights on one 1.6 TB/s stack: {tok_s:.0f} steps/s, {reads_day:.1e} reads/page/day; "
                  f"disturb limit {limit:.0e} -> {reclaims_yr:,.0f} reclaim P/E per year")
    print("TLC ~3k P/E, pSLC ~30-100k P/E [UNVERIFIED]; HBF 8-16x HBM capacity at similar cost [REPORTED]")


def card17():
    hr("B4-17  Procedural (seeded) weights regenerated in the memory path")
    for bits_eq in (3.0, 4.0):
        print(f"{bits_eq} b/weight stored vs BF16: x{16/bits_eq:.1f} fewer bits; vs FP4: x{4/bits_eq:.2f}")
    macs, e_mac = 4, 0.08
    print(f"regeneration ~{macs} low-precision MAC/weight x {e_mac} pJ = {macs*e_mac:.2f} pJ vs fetching 16 b at 3.5 pJ/b = 56 pJ")


def card18():
    hr("B4-18  Nested-precision bit-plane memory + self-speculative decoding")
    for draft_frac, k, a in ((0.5, 4, 0.8), (0.5, 4, 0.9), (0.25, 6, 0.85)):
        e_tok = (1 - a ** (k + 1)) / (1 - a)
        reads = (k * draft_frac + 1) / e_tok
        print(f"draft reads {draft_frac:.2f} of weights, k={k}, accept {a}: {e_tok:.2f} tokens/verify, "
              f"weight reads per token {reads:.2f} -> x{1/reads:.2f} effective bandwidth")


def card19():
    hr("B4-19  BitNet-native charge-sharing popcount PIM in commodity 1T1C")
    w = 70e9 * 1.58
    e_hbm = w * 3.5e-12
    for e_in in (0.1e-12, 0.3e-12):
        print(f"70B ternary GEMV per token: HBM path {e_hbm:.2f} J vs in-bank {w*e_in:.3f} J -> x{e_hbm/(w*e_in):.0f}")
    for n, sig in ((8, 0.05), (16, 0.05), (32, 0.05)):
        s = math.sqrt(n) * sig
        print(f"charge-sharing popcount over {n} cells, Cs sigma {sig:.0%}: sigma_sum {s:.2f} LSB -> "
              f"count error {2*phi_tail(0.5/s):.1e}")


def card20():
    hr("B4-20  Compact-then-sleep: compress, compact, partial-array self-refresh")
    for comp in (2.0, 3.0):
        for long_ref in (1.0, 16.0):
            print(f"compress x{comp:.0f} then PASR, self-refresh interval x{long_ref:.0f}: idle refresh power "
                  f"x{1/(comp*long_ref):.3f} -> 64GB RDIMM {RDIMM_REF_W/(comp*long_ref)*1e3:.0f} mW")
    e_compact = 64e9 * 8 * 10e-12      # move+compress 64 GB at ~10 pJ/bit [ESTIMATE]
    saved_w = RDIMM_REF_W * (1 - 1 / 3)
    print(f"compaction of a full 64 GB at ~10 pJ/bit = {e_compact:.1f} J; at {saved_w:.2f} W saved "
          f"(x3 compaction) break-even after {e_compact/saved_w:.0f} s of idle")


def card21():
    hr("B4-21  Broadcast weight bus: one weight copy feeds N lock-step replicas")
    for model_gb, steps in ((140, 30), (810, 20)):
        print(f"{model_gb} GB model at {steps} steps/s: broadcast stream {model_gb*steps/1000:.1f} TB/s, "
              f"same for 1 or N receivers")
    for n in (8, 16, 32):
        split_db = 10 * math.log10(n)
        print(f"1:{n} optical split loss {split_db:.1f} dB (+~3 dB excess) -> laser +{split_db+3:.0f} dB over point-to-point")
    for hbm_tot, w in ((640, 140), (1128, 810)):
        print(f"node HBM {hbm_tot} GB holding {w} GB weights: {w/hbm_tot:.0%} of HBM freed for KV")


def main():
    for f in (card01, card02, card03, card04, card05, card06, card07, card08, card09, card10,
              card11, card12, card13, card14, card15, card16, card17, card18, card19, card20, card21):
        f()
    print("\nOK")


if __name__ == "__main__":
    main()
