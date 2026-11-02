#!/usr/bin/env python3
"""
ai-memory-diet.py -- first-principles model for the AI MEMORY DIET concept dossier (stage 3).

Owner: dos-ai-memory-diet (dram-moonshot). Written 2026-11-02. Pure standard library.
Run from the dram-moonshot directory:  python3 models/ai-memory-diet.py
Writes: research/stage3/ai-memory-diet_model_output.md  (and prints the same markdown).

What it computes (per GPU, then per GB300-NVL72-class rack, then per 10,000 racks):
  1. KV bytes per token and per session (70B-class GQA, FP8 KV), with an optional retrofit
     latent that cuts capacity by k_cap and per-step KV reads by k_bw.
  2. Active decode sessions per GPU, bounded by HBM capacity and by HBM bandwidth per decode step.
  3. Little's-law session accounting with a heavy-tailed (log-normal) human inter-turn gap fitted
     to a production chat trace: active vs idle sessions, returns per second, the hit fraction
     an LRU host-DRAM KV tier can catch, and flash read/write load.
  4. Client-signal prefetch: a Monte Carlo over turns with a mixture of client lead times
     (typed / pasted / one-click / voice / no-signal) against an M/M/1 flash restore queue.
     Outputs coverage, p99 added TTFT and HBM hold overhead. Uncovered turns fall back to
     parallel load+recompute (Cake-style), which scales the residual restore by f_fb.
  5. DRAM GB per served conversation (HBM + host), DDR5-wafer-equivalent GB per user, host DRAM
     freed per rack, $ value at cost and at 2026 market prices, fab kWh and water avoided,
     NAND DWPD and drive count.
  6. Sensitivity tables on the key unknown (share of turns with too little client lead), context
     length, KV format, prefetch delay policy, host-DRAM-lite size and DRAM price.
  7. A GO/NO-GO line with the threshold the decisive experiment must hit.

Every input carries a source URL (logged in research/sources/dos-ai-memory-diet.jsonl) or
"ESTIMATE: basis" (logged in research/assumptions/dos-ai-memory-diet.md).
"""

import math
import os
import random

# --------------------------------------------------------------------------------------------
# INPUTS  (value, unit, source)
# --------------------------------------------------------------------------------------------
INPUTS = {
    # ---- Rack: GB300 NVL72 ----
    "gpus_per_rack": (72, "GPU", "https://www.nvidia.com/en-in/data-center/gb300-nvl72/ (via search snippet)"),
    "hbm_per_gpu_gb": (288.0, "GB", "20.7 TB HBM3e / 72 GPUs: https://www.supermicro.com/zh_tw/products/rack/srs-gb300-nvl72 (via search snippet)"),
    "host_per_gpu_gb": (240.0, "GB", "~480 GB LPDDR5X per Grace, 1 Grace : 2 GPUs: https://catalog.redhat.com/en/hardware/system/detail/307917 (via search snippet)"),
    "hbm_bw_tbs": (8.0, "TB/s per GPU", "576 TB/s / 72 GPUs: https://www.nvidia.com/en-in/data-center/gb300-nvl72/ (via search snippet)"),
    "c2c_gbs": (450.0, "GB/s", "ESTIMATE: half of Grace-Blackwell NVLink-C2C ~900 GB/s per superchip shared by 2 GPUs [training knowledge]"),
    "host_os_gb": (64.0, "GB per GPU", "ESTIMATE: OS + CUDA/NIXL/GDS bounce buffers + serving process; Stage 2 decisive experiment caps host at 32-64 GB/GPU (stage2_results I-10877)"),
    "host_lite_gb": (64.0, "GB per GPU", "ESTIMATE: host-DRAM-lite target = host_os_gb, no host KV tier"),
    "host_lite_critic_gb": (120.0, "GB per GPU", "ESTIMATE: critic-corrected 2x cut (async checkpoint staging ~16 B/param; stage2 I-10877 innovation critique)"),
    "hbm_util": (0.90, "-", "ESTIMATE: vLLM default gpu_memory_utilization 0.9 [training knowledge]"),
    # ---- Model: 70B-class GQA (Llama-3.1-70B shape) ----
    "layers": (80, "-", "ESTIMATE: Llama-3.1-70B config (80 layers, 8 KV heads, head_dim 128) [training knowledge]"),
    "kv_heads": (8, "-", "ESTIMATE: Llama-3.1-70B config [training knowledge]"),
    "head_dim": (128, "-", "ESTIMATE: Llama-3.1-70B config [training knowledge]"),
    "kv_bytes": (1.0, "B/elem", "ESTIMATE: FP8 KV cache, standard in vLLM/TRT-LLM serving [training knowledge]"),
    "weights_gb": (70.0, "GB", "ESTIMATE: 70B params x 1 B (FP8), one replica per 288 GB GPU"),
    "target_tps_user": (30.0, "tok/s per user", "ESTIMATE: interactive decode speed floor"),
    "t_gen_s": (10.0, "s", "ESTIMATE: ~500 output tokens at ~50 tok/s plus prefill (concept card: 5-10 s)"),
    "tok_new_per_turn": (1000.0, "tokens", "ESTIMATE: ~500 new prompt tokens (incl. pastes) + ~500 response tokens"),
    "ctx_median": (8000.0, "tokens", "ESTIMATE: multi-turn chat context incl. system prompt + history; sensitivity 4k-128k"),
    "ctx_sigma": (1.0, "ln-units", "ESTIMATE: log-normal spread -> p95 ~41k, p99 ~82k tokens, capped at 128k"),
    "ctx_cap": (131072.0, "tokens", "ESTIMATE: 128k context window"),
    # ---- Human inter-turn gap ----
    "gap_median_s": (110.0, "s", "https://arxiv.org/pdf/2605.18825 Qwen-Bailian trace (via search snippet)"),
    "gap_p80_s": (372.0, "s", "https://arxiv.org/pdf/2605.18825 (via search snippet); P99 ~2,207 s used as a fit check"),
    "gap_p99_s_check": (2207.0, "s", "https://arxiv.org/pdf/2605.18825 (via search snippet)"),
    "ttl_s": (600.0, "s", "ESTIMATE: sessions idle >10 min are treated as recompute-or-cold in both baseline and diet"),
    "retain_ssd_s": (3600.0, "s", "ESTIMATE: flash keeps a session's KV for 1 h after its last turn"),
    # ---- Flash ----
    "ssd_read_gbs": (14.0, "GB/s per drive", "ESTIMATE: PCIe Gen5 x4 enterprise NVMe ~14 GB/s sequential read (Gen5 x4 raw ~15.75 GB/s) [training knowledge]"),
    "ssd_per_gpu": (3.0, "Gen5-drive-equivalents", "ESTIMATE: sized by section 4 (bandwidth at rho<=0.6 and 3 DWPD); local E1.S bays (~8 per 4-GPU tray [training knowledge]) plus pod flash shelves over the ~100 GB/s per-GPU NIC (ICMS-style, https://nvidianews.nvidia.com/news/nvidia-bluefield-4-powers-new-class-of-ai-native-storage-infrastructure-for-the-next-frontier-of-ai)"),
    "ssd_cap_gb": (15360.0, "GB", "ESTIMATE: common enterprise TLC capacity point (15.36 TB)"),
    "dwpd_read_int": (1.0, "DWPD", "ESTIMATE: read-intensive enterprise TLC class"),
    "dwpd_mixed": (3.0, "DWPD", "ESTIMATE: mixed-use enterprise TLC class"),
    "rho_max": (0.60, "-", "ESTIMATE: max flash utilisation for a bounded p99 queue"),
    "spill_frac": (1.0, "-", "ESTIMATE: every turn's new KV chunks are appended to flash (append-only, LMCache-style chunks)"),
    "ssd_usd_gb": (0.20, "$/GB", "ESTIMATE: ~$0.08/GB early-2026 enterprise TLC x 2.3-2.8 (https://itldc.com/es/blog/server-ram-ssd-market-update-2026, via search snippet)"),
    # ---- Client-signal prefetch (the decisive experiment measures these) ----
    # (fraction of human chat turns, median lead s, log-normal sigma, typed-delay applies)
    "seg_typed": ((0.60, 8.0, 0.8, True), "-", "ESTIMATE: typed follow-ups of ~5-20 words at ~40 wpm plus focus; measured in Phase 1"),
    "seg_paste": ((0.20, 2.0, 0.6, False), "-", "ESTIMATE: focus -> paste/attach -> send"),
    "seg_click": ((0.10, 0.4, 0.5, False), "-", "ESTIMATE: regenerate / suggested-reply chip; lead = hover-to-click"),
    "seg_voice": ((0.05, 4.0, 0.6, True), "-", "ESTIMATE: speech start to end-of-utterance"),
    "seg_none": ((0.05, 0.0, 0.0, False), "-", "ESTIMATE: no client signal (API-from-UI, background, signal lost)"),
    "p_fp": (0.5, "prefetches per turn", "ESTIMATE: focus/keystroke events that do not end in a send"),
    "fp_hold_s": (2.0, "s", "ESTIMATE: HBM timeout for a false-positive prefetch"),
    "policy": (("jit", 3.0), "-", "ESTIMATE: policy knob; typed/voice turns start restore when a client-side send predictor (typing pause, cursor to send, end-of-speech) estimates remaining lead = m x expected restore time; paste/click turns start at the event"),
    "sigma_pred": (0.7, "ln-units", "ESTIMATE: multiplicative error of the client send predictor"),
    "f_fb": (0.5, "-", "ESTIMATE: Cake-style parallel load+recompute halves the uncovered residual (https://arxiv.org/html/2410.03065v2, via search snippet)"),
    "ttft_budget_s": (0.30, "s", "ESTIMATE: p99 added TTFT allowed (~15% of a 2 s interactive TTFT SLO)"),
    # ---- Latent KV ----
    "k_cap_latent": (3.0, "x", "ESTIMATE: planning case; MHA2MLA 92.19% on MHA Llama2-7B (~3.2x beyond GQA-8) https://arxiv.org/abs/2502.14837v1 ; xKV 8x on GQA Llama-3.1-8B https://arxiv.org/abs/2503.18893 ; X-EcoMLA 6.4x https://arxiv.org/html/2503.11132v1 (all via search snippet)"),
    "k_bw_latent": (3.0, "x", "ESTIMATE: assumes per-step KV reads fall like capacity (per-layer-group latent); a single all-layer latent re-read by every layer falls less"),
    # ---- Economics and resources ----
    "dram_cost_usd_gb": (1.48, "$/GB", "ram-venture models/dram_cost_stack.py (1-beta DDR5 cost)"),
    "dram_price_usd_gb": (20.0, "$/GB", "ESTIMATE: 2026 server DRAM/LPDDR contract; retail DDR5 RDIMM medians ~$31.75-35.70/GB (https://capitalandcompute.net/memory-prices/server/ , via search snippet)"),
    "hbm_wafer_mult": (3.0, "x DDR5 wafer/bit", "https://www.tomshardware.com/tech-industry/semiconductors/micron-says-the-silicon-gap-between-hbm-and-ddr5-is-widening-with-every-generation"),
    "kwh_per_gb": (0.42, "kWh/GB", "dram-moonshot research/models/A2_resource_intensity.py (A2 ESTIMATE)"),
    "water_l_per_gb": (2.6, "L/GB", "dram-moonshot A2 ESTIMATE"),
    "world_dram_eb": (68.0, "EB/yr DDR5-eq", "ESTIMATE: A2 fleet 22.2M wafers/yr x 3,068 GB/wafer (upper bound)"),
    "dram_w_per_gb": (0.15, "W/GB", "A2 [UNVERIFIED-PK] server DRAM power"),
    "racks_unit": (10000, "racks", "ESTIMATE: scaling unit only, not a shipment forecast"),
    # ---- Monte Carlo ----
    "mc_n": (40000, "turns", "model setting"),
    "seed": (20261102, "-", "model setting"),
}

Z80 = 0.8416212335729143
Z99 = 2.3263478740408408


def v(k):
    return INPUTS[k][0]


def phi(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


# --------------------------------------------------------------------------------------------
# Inter-turn gap: log-normal fitted to median and P80
# --------------------------------------------------------------------------------------------
GAP_MU = math.log(v("gap_median_s"))
GAP_SIG = math.log(v("gap_p80_s") / v("gap_median_s")) / Z80
GAP_MEAN = math.exp(GAP_MU + GAP_SIG ** 2 / 2)


def gap_p_lt(t):
    if t <= 0:
        return 0.0
    return phi((math.log(t) - GAP_MU) / GAP_SIG)


def gap_e_min(t):
    """E[min(G, t)] for log-normal G."""
    if t <= 0:
        return 0.0
    lt = math.log(t)
    return GAP_MEAN * phi((lt - GAP_MU - GAP_SIG ** 2) / GAP_SIG) + t * (1 - phi((lt - GAP_MU) / GAP_SIG))


# --------------------------------------------------------------------------------------------
# KV geometry
# --------------------------------------------------------------------------------------------
def kv_bytes_per_token(k=1.0):
    return 2 * v("layers") * v("kv_heads") * v("head_dim") * v("kv_bytes") / k


def ctx_samples(median, sigma, n, seed):
    rng = random.Random(seed + 7)
    cap = v("ctx_cap")
    if sigma <= 0:
        return [min(median, cap)] * n
    return [min(cap, rng.lognormvariate(math.log(median), sigma)) for _ in range(n)]


SEGS = ["seg_typed", "seg_paste", "seg_click", "seg_voice", "seg_none"]


def seg_table(nolead_share=None):
    """Return list of (frac, median, sigma, delay_applies). If nolead_share is given, the
    click+none share is set to it and typed absorbs the difference."""
    t = [list(v(s)) for s in SEGS]
    if nolead_share is not None:
        base_nolead = t[2][0] + t[4][0]
        scale = nolead_share / base_nolead
        t[2][0] *= scale
        t[4][0] *= scale
        t[0][0] = 1.0 - (t[1][0] + t[2][0] + t[3][0] + t[4][0])
    return [tuple(x) for x in t]


# --------------------------------------------------------------------------------------------
# Core per-GPU serving model
# --------------------------------------------------------------------------------------------
def serve(mode="diet", ctx_median=None, ctx_sigma=None, k_cap=1.0, k_bw=1.0, host_gb=None,
          n_ssd=None, policy=None, nolead_share=None, p_fp=None, mc_n=None, prefetch=True,
          sched="edf"):
    """mode: 'baseline' = HBM + LRU host-DRAM KV tier + flash, no client prefetch.
             'diet'     = HBM + flash direct (GDS), no host KV tier, client-signal prefetch."""
    ctx_median = v("ctx_median") if ctx_median is None else ctx_median
    ctx_sigma = v("ctx_sigma") if ctx_sigma is None else ctx_sigma
    host_gb = (v("host_per_gpu_gb") if mode == "baseline" else v("host_lite_gb")) if host_gb is None else host_gb
    n_ssd = v("ssd_per_gpu") if n_ssd is None else n_ssd
    policy = v("policy") if policy is None else policy
    p_fp = (v("p_fp") if (mode == "diet" and prefetch) else 0.0) if p_fp is None else p_fp
    mc_n = v("mc_n") if mc_n is None else mc_n
    seed = v("seed")

    ctxs = ctx_samples(ctx_median, ctx_sigma, mc_n, seed)
    ctx_mean = sum(ctxs) / len(ctxs)
    kvt_cap = kv_bytes_per_token(k_cap)
    kvt_bw = kv_bytes_per_token(k_bw)
    kv_gb = ctx_mean * kvt_cap / 1e9            # mean session KV stored (GB)
    kv_read_gb = ctx_mean * kvt_bw / 1e9        # mean KV read per decode step per session

    t_gen = v("t_gen_s")
    hbm_kv_budget = v("hbm_per_gpu_gb") * v("hbm_util") - v("weights_gb")
    step_gb = v("hbm_bw_tbs") * 1e3 / v("target_tps_user")
    n_bw = (step_gb - v("weights_gb")) / kv_read_gb
    p_ret = gap_p_lt(v("ttl_s"))
    host_kv_gb = max(0.0, host_gb - v("host_os_gb"))
    ssd_bw = v("ssd_read_gbs") * n_ssd
    segs = seg_table(nolead_share)
    cum = []
    acc = 0.0
    for s in segs:
        acc += s[0]
        cum.append(acc)

    hold = 0.0
    urgent_frac = 0.3
    res = {}
    for it in range(6):
        n_cap = hbm_kv_budget / (kv_gb * (1 + hold / t_gen))
        n_a = min(n_cap, n_bw)
        lam = n_a / t_gen                                  # turns started per s per GPU
        if mode == "baseline":
            t_dram = host_kv_gb / (lam * kv_gb) if lam > 0 else 0.0
            p_host = min(gap_p_lt(t_dram), p_ret)
        else:
            t_dram = 0.0
            p_host = 0.0
        demand = lam * (p_ret - p_host) * kv_gb * (1 + p_fp)   # GB/s flash reads
        rho = demand / ssd_bw
        sat = rho >= 0.98
        rho_c = min(rho, 0.98)
        rng = random.Random(seed)
        extras = []
        holds = 0.0
        covered = 0
        n_flash = 0
        urgent_bytes = 0.0
        flash_bytes = 0.0
        use_lead = (mode == "diet" and prefetch)
        # Deadline-aware flash scheduler (diet): restores with no usable lead run at high
        # priority; restores with client lead queue at low priority (preemptive-priority M/M/1).
        rho_h = min(rho_c, rho_c * urgent_frac) if (use_lead and sched == "edf") else rho_c
        for i in range(mc_n):
            kv_i = ctxs[i] * kvt_cap / 1e9
            s_i = kv_i / ssd_bw
            # which tier serves this returning turn
            if mode == "baseline" and rng.random() < (p_host / p_ret if p_ret > 0 else 0):
                extras.append(kv_i / v("c2c_gbs"))
                continue
            n_flash += 1
            flash_bytes += kv_i
            lead, delay_applies = 0.0, False
            if use_lead:
                u = rng.random()
                k = 0
                while k < len(cum) - 1 and u > cum[k]:
                    k += 1
                frac, med, sig, delay_applies = segs[k]
                lead = 0.0 if med <= 0 else rng.lognormvariate(math.log(med), sig)
            t_low = s_i / ((1 - rho_h) * (1 - rho_c))          # mean low-priority response
            urgent = (not use_lead) or sched == "fifo" or lead < t_low
            if urgent:
                urgent_bytes += kv_i
                w = rng.expovariate((1 - rho_h) / s_i) if rng.random() < rho_h else 0.0
                r = s_i + w
                eff = lead
            else:
                wl_mean = t_low - s_i
                w = rng.expovariate(rho_c / wl_mean) if (wl_mean > 0 and rng.random() < rho_c) else 0.0
                r = s_i + w
                if policy[0] == "imm" or not delay_applies:
                    eff = lead
                elif policy[0] == "delay":
                    eff = max(0.0, lead - policy[1])
                else:  # jit: start when predicted remaining lead = m x expected restore time
                    target = policy[1] * t_low * rng.lognormvariate(0.0, v("sigma_pred"))
                    eff = min(lead, target)
            if eff >= r:
                covered += 1
                holds += eff - r
                extras.append(0.0)
            else:
                extras.append(v("f_fb") * (r - eff))
        urgent_frac = (urgent_bytes / flash_bytes) if flash_bytes else 1.0
        extras.sort()
        p99 = extras[int(0.99 * (len(extras) - 1))]
        p90 = extras[int(0.90 * (len(extras) - 1))]
        mean_hold = holds / mc_n + (p_fp * v("fp_hold_s") if use_lead else 0.0)
        hold = mean_hold
        users = n_a * (t_gen + gap_e_min(v("ttl_s"))) / t_gen
        res = dict(mode=mode, ctx_mean=ctx_mean, kv_gb=kv_gb, n_a=n_a, n_cap=n_cap, n_bw=n_bw,
                   lam=lam, t_dram=t_dram, p_host_of_returns=(p_host / p_ret if p_ret else 0.0),
                   demand=demand, rho=rho, sat=sat, p99_extra=(float("inf") if sat else p99),
                   p90_extra=(float("inf") if sat else p90), prefetch=use_lead,
                   coverage=(covered / n_flash if n_flash else 1.0), hold=mean_hold, users=users,
                   host_gb=host_gb, s_mean=kv_gb / ssd_bw, urgent_frac=urgent_frac)
        if mode == "baseline":
            break
    # NAND writes and capacity
    writes_gb_day = res["lam"] * v("tok_new_per_turn") * kvt_cap / 1e9 * v("spill_frac") * 86400
    stored_gb = res["lam"] * gap_e_min(v("retain_ssd_s")) * kv_gb
    res["writes_gb_day"] = writes_gb_day
    res["dwpd"] = writes_gb_day / (v("ssd_cap_gb") * n_ssd)
    res["stored_gb"] = stored_gb
    res["dram_gb_gpu"] = v("hbm_per_gpu_gb") + host_gb
    res["dram_per_user"] = res["dram_gb_gpu"] / res["users"]
    res["wafer_eq_per_user"] = (v("hbm_per_gpu_gb") * v("hbm_wafer_mult") + host_gb) / res["users"]
    return res


def drives_needed(r, dwpd):
    """Drives per GPU to satisfy bandwidth (rho_max), endurance (dwpd) and capacity."""
    n_bw = r["demand"] / (v("ssd_read_gbs") * v("rho_max"))
    n_end = r["writes_gb_day"] / (v("ssd_cap_gb") * dwpd)
    n_capy = r["stored_gb"] / v("ssd_cap_gb")
    return max(1, math.ceil(max(n_bw, n_end, n_capy) - 1e-9)), n_bw, n_end, n_capy


def lead_required(r):
    """Lead time needed so that the p99 restore leaves <= budget after fallback."""
    # p99 restore time at this rho (M/M/1, mean session): S + S*ln(100*rho)/(1-rho)
    s = r["s_mean"]
    rho = min(r["rho"], 0.98) * (r["urgent_frac"] if r["mode"] == "diet" else 1.0)
    w99 = s * math.log(100 * rho) / (1 - rho) if rho > 0.01 else 0.0
    r99 = s + max(0.0, w99)
    return max(0.0, r99 - v("ttft_budget_s") / v("f_fb")), r99


def frac_lead_at_least(x, nolead_share=None, n=100000):
    """Share of turns whose raw client lead (signal to send) is >= x seconds."""
    segs = seg_table(nolead_share)
    rng = random.Random(v("seed") + 3)
    ok = 0
    for _ in range(n):
        u = rng.random()
        acc = 0.0
        for frac, med, sig, d in segs:
            acc += frac
            if u <= acc:
                break
        lead = 0.0 if med <= 0 else rng.lognormvariate(math.log(med), sig)
        eff = lead
        if eff >= x:
            ok += 1
    return ok / n


# --------------------------------------------------------------------------------------------
# Report
# --------------------------------------------------------------------------------------------
def f(x, nd=2):
    if x == float("inf"):
        return "SAT"
    return f"{x:,.{nd}f}"


def main():
    out = []
    P = out.append
    P("# AI MEMORY DIET: model output")
    P("")
    P("Generated by `models/ai-memory-diet.py` (pure stdlib, deterministic seed). Agent: dos-ai-memory-diet, 2026-11-02.")
    P("All numbers are [ESTIMATE] model outputs unless an input row cites a source. Inputs are listed at the end.")
    P("")

    # ---- 1. geometry
    kvt = kv_bytes_per_token()
    P("## 1. KV geometry and the human gap")
    P(f"- KV per token, 70B GQA FP8: 2 x {v('layers')} x {v('kv_heads')} x {v('head_dim')} x {v('kv_bytes'):.0f} B = **{kvt/1024:.0f} KiB/token**; latent {v('k_cap_latent'):.0f}x -> {kvt/v('k_cap_latent')/1024:.1f} KiB/token.")
    for c in (4000, 16000, 32000, 128000):
        P(f"  - {c//1000}k-token session: {c*kvt/1e9:.2f} GB FP8, {c*kvt/v('k_cap_latent')/1e9:.2f} GB latent; one-drive restore {c*kvt/1e9/v('ssd_read_gbs'):.2f} s / {c*kvt/v('k_cap_latent')/1e9/v('ssd_read_gbs'):.2f} s.")
    p99_fit = math.exp(GAP_MU + Z99 * GAP_SIG)
    P(f"- Inter-turn gap log-normal: median {v('gap_median_s'):.0f} s, sigma {GAP_SIG:.3f}, mean {GAP_MEAN:.0f} s; fitted P99 {p99_fit:,.0f} s vs reported {v('gap_p99_s_check'):,.0f} s (fit is ~{p99_fit/v('gap_p99_s_check'):.2f}x heavy in the far tail, conservative for flash capacity).")
    P(f"- Returns within TTL {v('ttl_s'):.0f} s: {gap_p_lt(v('ttl_s'))*100:.1f}%; E[min(gap, TTL)] = {gap_e_min(v('ttl_s')):.0f} s, so idle-but-returning KV is **{gap_e_min(v('ttl_s'))/v('t_gen_s'):.1f}x** the active KV for T_gen = {v('t_gen_s'):.0f} s (concept card assumed a 30 s median and ~3-5x).")
    P("")

    # ---- 2. base case scenarios
    A = serve("baseline")
    B = serve("diet")
    B0 = serve("diet", prefetch=False)
    C = serve("baseline", k_cap=v("k_cap_latent"), k_bw=v("k_bw_latent"))
    D = serve("diet", k_cap=v("k_cap_latent"), k_bw=v("k_bw_latent"))
    D0 = serve("diet", k_cap=v("k_cap_latent"), k_bw=v("k_bw_latent"), prefetch=False)
    P("## 2. Base case per GPU (context log-normal, median 8k, mean "
      f"{A['ctx_mean']/1000:.1f}k tokens)")
    P("")
    P("| Scenario | KV/session GB | active/GPU | conversations/GPU | host-tier share of returns | flash rho | coverage | p99 added TTFT s | HBM hold s/turn | DRAM GB/GPU | DRAM GB per conversation | DDR5-wafer-eq GB per conversation |")
    P("|---|---|---|---|---|---|---|---|---|---|---|---|")
    names = {"A": "A. Today: HBM + 240 GB host KV tier + flash, FP8 GQA",
             "B0": "B0. Host-lite 64 GB + flash-direct, NO client signal, FP8",
             "B": "B. Diet: host 64 GB, flash-direct + client prefetch, FP8",
             "C": "C. Today + latent 3x",
             "D0": "D0. Host-lite + latent 3x, NO client signal",
             "D": "D. Diet + latent 3x"}
    for key, r in (("A", A), ("B0", B0), ("B", B), ("C", C), ("D0", D0), ("D", D)):
        cov = "n/a" if not r["prefetch"] else f"{r['coverage']*100:.1f}%"
        P(f"| {names[key]} | {r['kv_gb']:.2f} | {r['n_a']:.0f} | {r['users']:,.0f} | {r['p_host_of_returns']*100:.1f}% | {f(r['rho'])} | {cov} | {f(r['p99_extra'])} | {r['hold']:.2f} | {r['dram_gb_gpu']:.0f} | {r['dram_per_user']:.3f} | {r['wafer_eq_per_user']:.3f} |")
    P("")
    P(f"- **DRAM GB per served conversation vs today (A): B0 {A['dram_per_user']/B0['dram_per_user']:.2f}x, B {A['dram_per_user']/B['dram_per_user']:.2f}x, C {A['dram_per_user']/C['dram_per_user']:.2f}x, D0 {A['dram_per_user']/D0['dram_per_user']:.2f}x, D {A['dram_per_user']/D['dram_per_user']:.2f}x fewer.** The diet's share beyond the latent: C/D0 = {C['dram_per_user']/D0['dram_per_user']:.2f}x, C/D = {C['dram_per_user']/D['dram_per_user']:.2f}x.")
    P(f"- DDR5-wafer-equivalent per conversation (HBM x{v('hbm_wafer_mult'):.0f}) vs A: B0 {A['wafer_eq_per_user']/B0['wafer_eq_per_user']:.2f}x, B {A['wafer_eq_per_user']/B['wafer_eq_per_user']:.2f}x, D0 {A['wafer_eq_per_user']/D0['wafer_eq_per_user']:.2f}x, D {A['wafer_eq_per_user']/D['wafer_eq_per_user']:.2f}x. In wafer terms the client-signal prefetch's HBM hold cancels most of the host-DRAM saving unless the hold is driven well below ~1 s/turn.")
    verdict0 = "meets" if B0["p99_extra"] <= v("ttft_budget_s") else "lands just over"
    P(f"- Host-lite WITHOUT client signals (B0) {verdict0} the p99 budget ({f(B0['p99_extra'])} s vs {v('ttft_budget_s')} s) at this context mix and {v('ssd_per_gpu'):.0f} drive-eq/GPU; about one more drive-eq/GPU closes it (section 6b). The client signal cuts p99 to {f(B['p99_extra'])} s at the cost of {B['hold']:.2f} s/turn of HBM hold. So the signal is a flash-bandwidth and long-context lever, not the thing that makes host-DRAM-lite possible at short contexts.")
    P(f"- Host-DRAM tier in today's design holds sessions for only ~{A['t_dram']:.0f} s (LRU), so it serves **{A['p_host_of_returns']*100:.1f}%** of returning turns; flash already serves the rest. With the latent it holds ~{C['t_dram']:.0f} s and serves {C['p_host_of_returns']*100:.1f}%.")
    P(f"- Baseline p99 added TTFT with no client prefetch (flash returns on demand, same fallback): {f(A['p99_extra'])} s (FP8), {f(C['p99_extra'])} s (latent). The diet's client prefetch improves on this: {f(B['p99_extra'])} s / {f(D['p99_extra'])} s.")
    P(f"- The diet's HBM hold (prefetched KV waiting for the send) costs {B['hold']/v('t_gen_s')*100:.0f}% extra HBM KV per active session (FP8), which is why B serves {B['n_a']:.0f} vs {A['n_a']:.0f} active sessions/GPU when HBM capacity binds.")
    P("")

    # ---- 3. rack / fleet
    g = v("gpus_per_rack")
    rack_dram = g * (v("hbm_per_gpu_gb") + v("host_per_gpu_gb")) / 1e3
    P("## 3. Rack and fleet (GB300 NVL72 class)")
    P("")
    P(f"- Rack DRAM today: {g} x ({v('hbm_per_gpu_gb'):.0f} HBM + {v('host_per_gpu_gb'):.0f} host) = **{rack_dram:.1f} TB** (NVIDIA lists 37 TB fast memory).")
    P("")
    P("| host-lite GB/GPU | host DRAM freed per rack TB | % of rack DRAM | $ at cost $1.48/GB | $ at $20/GB | $ at $35.70/GB retail | fab kWh avoided | water L avoided |")
    P("|---|---|---|---|---|---|---|---|")
    for h in (32, 64, 120, 160):
        fr = g * (v("host_per_gpu_gb") - h)
        P(f"| {h} | {fr/1e3:.1f} | {fr/1e3/rack_dram*100:.1f}% | ${fr*v('dram_cost_usd_gb'):,.0f} | ${fr*20:,.0f} | ${fr*35.70:,.0f} | {fr*v('kwh_per_gb'):,.0f} | {fr*v('water_l_per_gb'):,.0f} |")
    fr64 = g * (v("host_per_gpu_gb") - v("host_lite_gb"))
    fr120 = g * (v("host_per_gpu_gb") - v("host_lite_critic_gb"))
    units = v("racks_unit")
    P("")
    P(f"- Per {units:,} racks: {fr120*units/1e9:.3f}-{fr64*units/1e9:.3f} EB of host DRAM not bought = {fr120*units/1e9/v('world_dram_eb')*100:.2f}-{fr64*units/1e9/v('world_dram_eb')*100:.2f}% of ~{v('world_dram_eb'):.0f} EB/yr DDR5-equivalent output; ${fr120*units*v('dram_price_usd_gb')/1e9:.1f}-{fr64*units*v('dram_price_usd_gb')/1e9:.1f}B at ${v('dram_price_usd_gb'):.0f}/GB; {fr120*units*v('kwh_per_gb')/1e6:.0f}-{fr64*units*v('kwh_per_gb')/1e6:.0f} GWh fab electricity; use-phase ~{fr120*v('dram_w_per_gb')/1e3:.1f}-{fr64*v('dram_w_per_gb')/1e3:.1f} kW per rack at {v('dram_w_per_gb')} W/GB [UNVERIFIED].")
    # HBM effect of the latent on users -> GPUs per user
    P(f"- HBM bits per conversation (latent's main effect): A {v('hbm_per_gpu_gb')/A['users']:.3f} GB -> D {v('hbm_per_gpu_gb')/D['users']:.3f} GB ({A['users'] and (v('hbm_per_gpu_gb')/A['users'])/(v('hbm_per_gpu_gb')/D['users']):.2f}x fewer HBM GB per conversation, each HBM GB ~{v('hbm_wafer_mult'):.0f}x DDR5 wafer).")
    P("")

    # ---- 4. flash budget
    P("## 4. Flash bandwidth, endurance and capacity per GPU")
    P("")
    P("| Scenario | read demand GB/s | writes TB/day | DWPD on base drives | stored TB (1 h retention) | drives needed @1 DWPD | drives needed @3 DWPD | SSD $/rack @3 DWPD |")
    P("|---|---|---|---|---|---|---|---|")
    bill = {}
    for key, r in (("A", A), ("B0", B0), ("B", B), ("C", C), ("D0", D0), ("D", D)):
        n1 = drives_needed(r, v("dwpd_read_int"))[0]
        n3 = drives_needed(r, v("dwpd_mixed"))[0]
        add = n3 * v("ssd_cap_gb") * v("ssd_usd_gb") * g
        hbm_usd = v("hbm_per_gpu_gb") * v("dram_price_usd_gb") * v("hbm_wafer_mult")
        host_usd = r["host_gb"] * v("dram_price_usd_gb")
        flash_usd = n3 * v("ssd_cap_gb") * v("ssd_usd_gb")
        bill[key] = (hbm_usd + host_usd + flash_usd) / r["users"] * 1000
        P(f"| {names[key]} | {r['demand']:.1f} | {r['writes_gb_day']/1e3:.1f} | {r['dwpd']:.2f} | {r['stored_gb']/1e3:.1f} | {n1} | {n3} | ${add:,.0f} |")
    P("")
    P(f"- Memory + flash bill per 1,000 concurrent conversations [ESTIMATE: DRAM ${v('dram_price_usd_gb'):.0f}/GB, HBM priced at {v('hbm_wafer_mult'):.0f}x DRAM (wafer-proportional), flash ${v('ssd_usd_gb')}/GB at the 3-DWPD drive count]: " + ", ".join(f"{k} ${bill[k]:,.0f}" for k in bill) + f". Host-lite alone (B0) saves {(1-bill['B0']/bill['A'])*100:.0f}% vs A; latent + host-lite (D0) saves {(1-bill['D0']/bill['A'])*100:.0f}%.")
    law = (v("hbm_per_gpu_gb") * v("hbm_util") - v("weights_gb")) / v("t_gen_s") * gap_p_lt(v("ttl_s"))
    P("")
    P(f"- **Flash-supply law [ESTIMATE]:** when HBM capacity binds, flash must re-supply the GPU's whole HBM KV pool once per generation time: read demand ~= HBM KV budget / (T_gen + hold) x P(return) x (1 + p_fp) = {law:.1f} GB/s per GPU before hold and false positives, independent of KV compression. The latent cuts flash load per conversation ({B['demand']/B['users']*1e3:.1f} -> {D['demand']/D['users']*1e3:.1f} MB/s per conversation), not per GPU. Writes follow the same law. So the critics' 'latent fixes flash wear' holds per user, not per drive.")
    nB3 = drives_needed(B, v("dwpd_mixed"))
    nD3 = drives_needed(D, v("dwpd_mixed"))
    P("")
    P(f"- FP8 diet needs {nB3[0]} drives/GPU at 3 DWPD (bandwidth {nB3[1]:.2f}, endurance {nB3[2]:.2f}, capacity {nB3[3]:.2f} drive-equivalents); latent needs {nD3[0]}. Writes per 8-GPU node: {B['writes_gb_day']*8/1e3:,.0f} TB/day FP8 vs {D['writes_gb_day']*8/1e3:,.0f} TB/day latent (critic's figure: ~280 TB/day).")
    P(f"- Rack DRAM $ saved at ${v('dram_price_usd_gb'):.0f}/GB (64 GB host-lite): ${fr64*v('dram_price_usd_gb'):,.0f} vs flash for the KV tier ${nB3[0]*v('ssd_cap_gb')*v('ssd_usd_gb')*g:,.0f} (FP8) / ${nD3[0]*v('ssd_cap_gb')*v('ssd_usd_gb')*g:,.0f} (latent) at ${v('ssd_usd_gb')}/GB. Today's design (A) needs {drives_needed(A, v('dwpd_mixed'))[0]} drive-eq/GPU too, because flash already serves ~{(1-A['p_host_of_returns'])*100:.0f}% of returns and absorbs the same writes, so the diet's incremental flash is ~0 against a 2026 LMCache/ICMS-style design and large only against a no-flash design. At cost (${v('dram_cost_usd_gb')}/GB) the DRAM saved is only ${fr64*v('dram_cost_usd_gb'):,.0f}: the economics are a shortage-price story; the bit savings are not.")
    P("")

    # ---- 5. Sensitivity: context length x KV format (fixed contexts)
    pol = v("policy")
    P(f"## 5. Sensitivity A: fixed context length x KV format ({v('ssd_per_gpu'):.0f} drive-eq/GPU; diet = client prefetch, {pol[0]} m={pol[1]:g}, deadline-aware flash queue)")
    P("")
    P("| context | KV format | KV GB | mean restore s | flash rho | coverage | urgent share of flash bytes | p90 added TTFT s | p99 added TTFT s | p99, host-lite no signal s | p99, today (A) s | diet GO (p99 <= budget)? |")
    P("|---|---|---|---|---|---|---|---|---|---|---|---|")
    sec5 = {}
    for c in (4000, 16000, 32000, 64000, 128000):
        for lab, kc in (("FP8 GQA", 1.0), ("latent 3x", v("k_cap_latent"))):
            r = serve("diet", ctx_median=c, ctx_sigma=0.0, k_cap=kc, k_bw=kc, mc_n=20000)
            r0 = serve("diet", ctx_median=c, ctx_sigma=0.0, k_cap=kc, k_bw=kc, mc_n=20000, prefetch=False)
            rb = serve("baseline", ctx_median=c, ctx_sigma=0.0, k_cap=kc, k_bw=kc, mc_n=20000)
            go = "GO" if (r["p99_extra"] <= v("ttft_budget_s")) else "NO-GO"
            sec5[(c, lab)] = (r, r0, rb)
            P(f"| {c//1000}k | {lab} | {r['kv_gb']:.2f} | {r['s_mean']:.3f} | {f(r['rho'])} | {r['coverage']*100:.1f}% | {r['urgent_frac']*100:.0f}% | {f(r['p90_extra'])} | {f(r['p99_extra'])} | {f(r0['p99_extra'])} | {f(rb['p99_extra'])} | {go} |")
    P("")
    P(f"Reading: p99 added TTFT scales with the restore time of the context. With FP8 KV the diet passes the {v('ttft_budget_s')} s budget up to {max([c for (c, l) in sec5 if l=='FP8 GQA' and sec5[(c,l)][0]['p99_extra'] <= v('ttft_budget_s')] or [0])//1000}k tokens; with the 3x latent up to {max([c for (c, l) in sec5 if l!='FP8 GQA' and sec5[(c,l)][0]['p99_extra'] <= v('ttft_budget_s')] or [0])//1000}k. At every length the client signal cuts p99 by ~{sum(sec5[k][1]['p99_extra']/max(1e-9, sec5[k][0]['p99_extra']) for k in sec5)/len(sec5):.1f}x versus host-lite without signals, because it turns most restores into deadline-tolerant background traffic.")
    P("")

    # ---- 6. Key unknown: share of turns with ~no client lead
    P("## 6. Sensitivity B (KEY UNKNOWN): share of turns with no useful client lead (one-click + no-signal)")
    P("")
    P("| no-lead share | base mix FP8, 3 drive-eq: p99 s | base mix FP8, 2.5 drive-eq: p99 s | base mix FP8, 2 drive-eq: p99 s | 64k FP8: coverage | 64k FP8: p99 s | 128k latent: p99 s | 128k latent, 6 drive-eq: p99 s |")
    P("|---|---|---|---|---|---|---|---|")
    sec6 = []
    for nl in (0.0, 0.02, 0.05, 0.10, 0.15, 0.25, 0.40, 0.60):
        a3 = serve("diet", nolead_share=nl, mc_n=20000)
        a2 = serve("diet", nolead_share=nl, n_ssd=2.5, mc_n=20000)
        a15 = serve("diet", nolead_share=nl, n_ssd=2.0, mc_n=20000)
        b = serve("diet", ctx_median=64000, ctx_sigma=0.0, nolead_share=nl, mc_n=20000)
        c = serve("diet", ctx_median=128000, ctx_sigma=0.0, nolead_share=nl, k_cap=3, k_bw=3, mc_n=20000)
        d = serve("diet", ctx_median=128000, ctx_sigma=0.0, nolead_share=nl, k_cap=3, k_bw=3, n_ssd=6, mc_n=20000)
        sec6.append((nl, a3, a2, a15))
        P(f"| {nl*100:.0f}% | {f(a3['p99_extra'])} | {f(a2['p99_extra'])} | {f(a15['p99_extra'])} | {b['coverage']*100:.1f}% | {f(b['p99_extra'])} | {f(c['p99_extra'])} | {f(d['p99_extra'])} |")
    b2 = [nl for (nl, a3, a2, a15) in sec6 if a2["p99_extra"] <= v("ttft_budget_s")]
    b15 = [nl for (nl, a3, a2, a15) in sec6 if a15["p99_extra"] <= v("ttft_budget_s")]
    nl_max2 = max(b2) if b2 else None
    nl_max15 = max(b15) if b15 else None
    P("")
    def share_txt(x):
        return ("up to a %.0f%% no-lead share" % (x * 100)) if x is not None else "at no share tested"
    P(f"Reading: with a deadline-aware flash queue, the no-lead share matters most when flash is lean. At 3 drive-eq/GPU the base mix passes at every share tested. At 2.5 drive-eq/GPU it passes {share_txt(nl_max2)}; at 2 drive-eq it passes {share_txt(nl_max15)}. Long contexts fail on restore time regardless of the share. The concept card's '>=80% coverage' threshold is therefore the wrong form. The real thresholds are flash utilisation, the p99 context's restore time, and (for lean flash) the no-lead share.")
    P("")

    # ---- 6b. Client signal as a substitute for flash bandwidth
    def min_drives(prefetch, **kw):
        lo, hi = 0.5, 24.0
        if serve("diet", n_ssd=hi, prefetch=prefetch, mc_n=8000, **kw)["p99_extra"] > v("ttft_budget_s"):
            return float("inf")
        for _ in range(9):
            mid = (lo + hi) / 2
            if serve("diet", n_ssd=mid, prefetch=prefetch, mc_n=8000, **kw)["p99_extra"] <= v("ttft_budget_s"):
                hi = mid
            else:
                lo = mid
        return hi
    P("## 6b. Flash drive-equivalents per GPU needed for p99 added TTFT <= budget (host-lite, 64 GB/GPU)")
    P("")
    P("| workload | with client prefetch | without client signal | drives saved by the signal |")
    P("|---|---|---|---|")
    sec6b = {}
    for lab, kw in (("base mix FP8", {}), ("base mix latent 3x", {"k_cap": 3.0, "k_bw": 3.0}),
                    ("32k FP8", {"ctx_median": 32000, "ctx_sigma": 0.0}),
                    ("64k FP8", {"ctx_median": 64000, "ctx_sigma": 0.0}),
                    ("128k latent 3x", {"ctx_median": 128000, "ctx_sigma": 0.0, "k_cap": 3.0, "k_bw": 3.0}),
                    ("128k FP8", {"ctx_median": 128000, "ctx_sigma": 0.0})):
        w1 = min_drives(True, **kw)
        w0 = min_drives(False, **kw)
        sec6b[lab] = (w1, w0)
        P(f"| {lab} | {f(w1, 1)} | {f(w0, 1)} | {f(w0 - w1, 1) if w1 != float('inf') and w0 != float('inf') else 'n/a'} |")
    P("")
    P("Reading: the client signal's measurable value is flash bandwidth it saves (and the long contexts it rescues), not host DRAM. Flash bandwidth is cheap, so the signal is an efficiency feature; host-DRAM-lite stands without it at short contexts.")
    P("")

    # ---- 7. Prefetch delay policy (HBM hold vs coverage)
    P("## 7. Sensitivity C: prefetch timing policy and false positives (base context mix, FP8)")
    P("")
    P("| policy | false-positive prefetches/turn | coverage | p99 added TTFT s | HBM hold s/turn | extra HBM KV % | active/GPU | DRAM GB per conversation | wafer-eq GB per conversation |")
    P("|---|---|---|---|---|---|---|---|---|")
    pol_lab = {"imm": "restore at first keystroke/focus", "delay": "fixed delay {} s", "jit": "send-predictor, margin m={}"}
    r0 = serve("diet", prefetch=False, mc_n=20000)
    P(f"| no client signal (host-lite only) | 0 | n/a | {f(r0['p99_extra'])} | 0.00 | 0% | {r0['n_a']:.0f} | {r0['dram_per_user']:.3f} | {r0['wafer_eq_per_user']:.3f} |")
    for pol, pfp in ((("imm", 0.0), 0.5), (("delay", 2.0), 0.5), (("delay", 4.0), 0.5), (("jit", 2.0), 0.5),
                     (("jit", 3.0), 0.0), (("jit", 3.0), 0.5), (("jit", 3.0), 1.0), (("jit", 5.0), 0.5)):
        r = serve("diet", policy=pol, p_fp=pfp, mc_n=20000)
        lab = pol_lab[pol[0]].format(f"{pol[1]:g}")
        P(f"| {lab} | {pfp:g} | {r['coverage']*100:.1f}% | {f(r['p99_extra'])} | {r['hold']:.2f} | {r['hold']/v('t_gen_s')*100:.0f}% | {r['n_a']:.0f} | {r['dram_per_user']:.3f} | {r['wafer_eq_per_user']:.3f} |")
    P("")
    P(f"Reading: restoring at the first keystroke maximises coverage but parks KV in HBM for the whole composition time, which eats the HBM the diet was meant to save. A client send predictor (typing pause, cursor on send, end of speech) with few false positives is required: today's wafer-equivalent per conversation is {A['wafer_eq_per_user']:.3f} GB, and only policies with hold <~1 s/turn beat it.")
    P("")

    # ---- 8. Host-tier value vs host size (baseline)
    P("## 8. Sensitivity D: what a bigger host-DRAM KV tier buys (baseline, no client prefetch)")
    P("")
    P("| host GB/GPU | FP8: LRU hold s | FP8: share of returns from host | FP8 p99 added TTFT s | latent: share from host | latent p99 s | DRAM GB per conversation (FP8) |")
    P("|---|---|---|---|---|---|---|")
    for h in (64, 240, 750, 2000):
        r = serve("baseline", host_gb=h, mc_n=20000)
        rl = serve("baseline", host_gb=h, k_cap=3, k_bw=3, mc_n=20000)
        P(f"| {h} | {r['t_dram']:.0f} | {r['p_host_of_returns']*100:.1f}% | {f(r['p99_extra'])} | {rl['p_host_of_returns']*100:.1f}% | {f(rl['p99_extra'])} | {r['dram_per_user']:.3f} |")
    P("")
    P("Reading: because human gaps are heavy-tailed (median ~110 s), even 2 TB of host DRAM per GPU catches only a minority of returns; flash serves the rest either way. A host-DRAM KV tier is a poor use of DRAM bits for human chat.")
    P("")

    # ---- 9. DRAM price
    P("## 9. Sensitivity E: $ value of host DRAM freed per rack and per 10,000 racks (64 GB host-lite)")
    P("")
    P("| DRAM $/GB | per rack | per 10,000 racks |")
    P("|---|---|---|")
    for pr in (1.48, 5.0, 10.0, 20.0, 35.70):
        P(f"| {pr:.2f} | ${fr64*pr:,.0f} | ${fr64*pr*units/1e9:,.2f}B |")
    P("")

    # ---- 10. GO / NO-GO
    def ctx_max_mc(kc, prefetch=True):
        lo, hi = 2000.0, v("ctx_cap")
        if serve("diet", ctx_median=hi, ctx_sigma=0.0, k_cap=kc, k_bw=kc, prefetch=prefetch, mc_n=8000)["p99_extra"] <= v("ttft_budget_s"):
            return hi
        for _ in range(9):
            mid = math.sqrt(lo * hi)
            if serve("diet", ctx_median=mid, ctx_sigma=0.0, k_cap=kc, k_bw=kc, prefetch=prefetch, mc_n=8000)["p99_extra"] <= v("ttft_budget_s"):
                lo = mid
            else:
                hi = mid
        return lo
    cmB = ctx_max_mc(1.0)
    cmD = ctx_max_mc(v("k_cap_latent"))
    cmB0 = ctx_max_mc(1.0, prefetch=False)
    cmD0 = ctx_max_mc(v("k_cap_latent"), prefetch=False)
    capk = v("ctx_cap") / 1000
    def kfmt(x):
        return f">={capk:.0f}k" if x >= v("ctx_cap") else f"~{x/1000:.0f}k"
    P("## 10. GO / NO-GO")
    P("")
    P(f"- Base-case diet (FP8, host 64 GB/GPU, {v('ssd_per_gpu'):.0f} drive-eq/GPU): p99 added TTFT {f(B['p99_extra'])} s vs budget {v('ttft_budget_s')} s; coverage {B['coverage']*100:.1f}%; flash rho {B['rho']:.2f}; {B['dwpd']:.2f} DWPD.")
    P(f"- Longest fixed context that passes p99 <= {v('ttft_budget_s')} s: with client prefetch {kfmt(cmB)} tokens FP8, {kfmt(cmD)} latent; without client signal {kfmt(cmB0)} FP8, {kfmt(cmD0)} latent.")
    P("")
    P(f"**GO/NO-GO:** GO if, replaying consented real chat traces on one 8-GPU node with host memory capped at <=64 GB/GPU and no host-DRAM KV tier, three things hold. (1) p99 added TTFT is <={v('ttft_budget_s')} s versus a 240 GB/GPU host-DRAM-tier baseline at equal tokens/s and <={v('ssd_per_gpu'):.0f} Gen5 drive-equivalents per GPU. For the base context mix the model predicts {f(B0['p99_extra'])} s without client signals and {f(B['p99_extra'])} s with them. A workload whose sessions all sit at one length passes up to {kfmt(cmB)} tokens at FP8. (2) Flash stays <=3 DWPD. The model gives {B['dwpd']:.2f} DWPD at {v('ssd_per_gpu'):.0f} x 15.36 TB. (3) For the client signal to earn its place, the send predictor must hold prefetched KV in HBM for <=1.0 s per turn, and, if flash is trimmed to 2.5 drive-eq/GPU, the share of turns with no usable client lead (one-click plus no-signal) must stay <= {('%.0f%%' % (nl_max2*100)) if nl_max2 is not None else 'n/a'}. The latent gate is >=3x over FP8 GQA at <=1 point RULER-average loss at 32k; it makes contexts up to {kfmt(cmD)} pass. NO-GO for the full concept if p99 fails at the measured context distribution even with the latent and 3 drive-eq/GPU, because a DRAM KV tier would then have to return. The host-lite saving of ~{fr120/1e3:.1f}-{fr64/1e3:.1f} TB per rack survives any client-signal result for workloads whose p99 context stays under the FP8 limit.")
    P("")

    # ---- inputs
    P("## Inputs")
    P("")
    P("| key | value | unit | source |")
    P("|---|---|---|---|")
    for k, (val, unit, src) in INPUTS.items():
        P(f"| {k} | {val} | {unit} | {src} |")
    P("")

    text = "\n".join(out)
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(root, "research", "stage3", "ai-memory-diet_model_output.md")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fh:
        fh.write(text + "\n")
    print(text)
    print(f"\n[wrote {path}]")


if __name__ == "__main__":
    main()
