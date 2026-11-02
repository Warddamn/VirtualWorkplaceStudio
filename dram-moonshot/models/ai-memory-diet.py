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

RED-TEAM REVISIONS (2026-11-02, owner response to research/redteam/rt_*.json; sources in
research/sources/resp-ai-memory-diet.jsonl). Format: input or mechanism: old -> new [objection id].
  - waf (NAND write amplification): implicit 1.0 -> 1.1 with FDP placement by expiry class; DWPD and
    endurance drive count are now NAND-side; sensitivity 1.0-2.0 in section 11.3   [RT-DEV-01]
  - flash queue: reads only -> reads + NAND program/erase die-time (write_interf 1.0, ssd_write_gbs
    10 GB/s per drive) added to flash utilisation                                  [RT-CIRC-04, RT-DEV-04]
  - bw_derate stress cases: none -> end-of-life read derate 0.85 and 1-of-3 drives throttled to 50%
    (bandwidth x 5/6), section 11.4                                                 [RT-DEV-02, RT-DEV-04]
  - latent geometry: "single latent shared by all layers" (g = 80 layers per latent, so per-step KV
    reads x 80/3 = 26.7x GQA) -> per-layer latent (latent_group_layers 1, k_bw = k_cap / g = 3);
    all-layer case shown in section 11.1 as a kill                                  [RT-CIRC-02]
  - compute bound: none -> active sessions also capped by GPU FLOPs (decode + prompt prefill;
    gpu_fp8_pflops 5.0 x mfu_serve 0.4); spare HBM then acts as an idle-KV tier. This changes the
    latent scenarios C/D/D0 (compute binds before HBM) and is needed for MLA models  [RT-CIRC-02, RT-IND-04]
  - dram_w_per_gb: 0.15 (DDR5 RDIMM class) -> 0.04 (LPDDR5X on Grace); ssd_w 20 W   [RT-DEV-03]
  - full-KV-path DRAM bill: HBM + host only -> + SSD FTL DRAM (1 GB/TB at 4 KiB IU; 1/16 at 64 KiB
    IU) + pod-shelf server/DPU DRAM for drive-eq beyond 2 local bays per GPU         [RT-CIRC-03]
  - traffic mix: human chat only -> + agent/API class (tool-wait gaps median 3 s) with three
    placements (today's LRU, host-lite flash-only, gap-aware right-sized host tier)  [RT-CIRC-01, RT-IND-05]
  - model mix: 70B GQA only -> + MLA (DeepSeek-V3-class) and hybrid linear-attention
    (Qwen3-Next-class, with per-turn recurrent-state rewrite)                       [RT-IND-04]
  - baselines: today's flash-tier design only -> + no-KV-flash DGX-class baseline (3.84 TB/GPU,
    misses recomputed), with DRAM + NAND wafer starts per 1,000 conversations         [RT-PROC-01]
  - step-change scoring: headline now human-chat pool host-lite with full-path DRAM (section 11.9)
                                                                                    [RT-IND-02, RT-PROC-02]
"""

import math
import os
import random
from contextlib import contextmanager

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
    "k_bw_latent": (3.0, "x", "RED-TEAM [RT-CIRC-02]: = k_cap_latent / latent_group_layers; per-layer latent (g=1) keeps per-step KV reads 3x below GQA FP8. A single latent shared by all 80 layers gives k_bw = 3/80 (26.7x MORE reads than GQA) and is killed (section 11.1)"),
    "latent_group_layers": (1, "layers per latent", "RED-TEAM [RT-CIRC-02]: old design = 80 (one latent for all layers) -> 1 (per-layer, MHA2MLA/TransMLA-style prior art)"),
    # ---- Economics and resources ----
    "dram_cost_usd_gb": (1.48, "$/GB", "ram-venture models/dram_cost_stack.py (1-beta DDR5 cost)"),
    "dram_price_usd_gb": (20.0, "$/GB", "ESTIMATE: 2026 server DRAM/LPDDR contract; retail DDR5 RDIMM medians ~$31.75-35.70/GB (https://capitalandcompute.net/memory-prices/server/ , via search snippet)"),
    "hbm_wafer_mult": (3.0, "x DDR5 wafer/bit", "https://www.tomshardware.com/tech-industry/semiconductors/micron-says-the-silicon-gap-between-hbm-and-ddr5-is-widening-with-every-generation"),
    "kwh_per_gb": (0.42, "kWh/GB", "dram-moonshot research/models/A2_resource_intensity.py (A2 ESTIMATE)"),
    "water_l_per_gb": (2.6, "L/GB", "dram-moonshot A2 ESTIMATE"),
    "world_dram_eb": (68.0, "EB/yr DDR5-eq", "ESTIMATE: A2 fleet 22.2M wafers/yr x 3,068 GB/wafer (upper bound)"),
    "dram_w_per_gb": (0.04, "W/GB", "RED-TEAM [RT-DEV-03]: 0.15 (A2 DDR5 RDIMM class) -> 0.04, LPDDR5X background+active power per GB under serving load on Grace, range 0.03-0.05 [UNVERIFIED-PK]"),
    "racks_unit": (10000, "racks", "ESTIMATE: scaling unit only, not a shipment forecast"),
    # ---- RED-TEAM additions (2026-11-02) ----
    "waf": (1.1, "-", "RED-TEAM [RT-DEV-01]: implicit 1.0 -> 1.1; KV chunks appended and expired in bulk, placed by expiry class with NVMe FDP; CacheLib+FDP reaches device WAF ~1 on Meta/Twitter traces (https://arxiv.org/abs/2503.11665, via search snippet). Sensitivity 1.0-2.0"),
    "write_interf": (1.0, "-", "RED-TEAM [RT-CIRC-04]: share of NAND program/erase die-time that blocks reads (1.0 = no program/erase suspend; conservative)"),
    "ssd_write_gbs": (10.0, "GB/s per drive", "RED-TEAM [RT-CIRC-04]: ESTIMATE Gen5 15.36 TB TLC sustained sequential write ~8-10 GB/s [training knowledge]"),
    "eol_read_derate": (0.85, "x", "RED-TEAM [RT-DEV-02]: ESTIMATE read throughput at >=80% rated P/E (read-retry, soft LDPC); measured in the pre-cycled arm"),
    "throttle_derate": (5.0 / 6.0, "x", "RED-TEAM [RT-DEV-04]: ESTIMATE 1 of 3 drives thermally throttled to 50% bandwidth"),
    "ssd_w": (20.0, "W per drive", "RED-TEAM [RT-DEV-03]: ESTIMATE Gen5 drive under mixed read/write load, range 15-25 W"),
    "local_bays_per_gpu": (2.0, "drives", "RED-TEAM [RT-CIRC-03]: 8 E1.S bays per 4-GPU GB300 tray (https://www.cudocompute.com/products/nvidia-gb300/, logged by rt-CIRC)"),
    "ftl_gb_per_tb": (1.0, "GB DRAM per TB", "RED-TEAM [RT-CIRC-03]: page-mapped FTL, 4 B per 4 KiB indirection unit [training knowledge]"),
    "ftl_gb_per_tb_large_iu": (1.0 / 16, "GB DRAM per TB", "RED-TEAM [RT-CIRC-03]: 64 KiB indirection unit (QLC-style large-IU drives) or ZNS; fits KV chunks of ~40 MB (256 tokens x 160 KiB) written sequentially [training knowledge]"),
    "shelf_dram_gb_per_drive": (10.0, "GB per drive", "RED-TEAM [RT-CIRC-03]: ESTIMATE pod flash shelf: ~256 GB of storage-head + DPU DRAM per ~24-26 drives [UNVERIFIED-PK]"),
    "gpu_fp8_pflops": (5.0, "PFLOP/s dense", "RED-TEAM [RT-IND-04, RT-CIRC-02]: ESTIMATE Blackwell-Ultra FP8 dense per GPU [training knowledge]"),
    "mfu_serve": (0.40, "-", "RED-TEAM: ESTIMATE serving MFU for decode+prefill mix; gives ~11-14k tok/s/GPU on 70B dense, in line with MLPerf-class B200 results [training knowledge]"),
    "active_params_b": (70.0, "B params", "RED-TEAM: 70B dense (Llama-3.1-70B); MLA case 37B active (DeepSeek-V3), hybrid 3B active (Qwen3-Next-80B-A3B) [training knowledge]"),
    "q_heads": (64, "-", "RED-TEAM: Llama-3.1-70B query heads; attention FLOPs per context token = layers x 4 x q_heads x head_dim [training knowledge]"),
    "attn_flops_ctx_override": (0.0, "FLOP per ctx token per token", "RED-TEAM [RT-IND-04]: 0 = GQA formula; MLA absorbed attention 61 x 2 x 128 x (576+512) = 17.0 MFLOP"),
    "kv_elems_layer": (0, "elements/token/layer", "RED-TEAM [RT-IND-04]: 0 = GQA 2 x kv_heads x head_dim; MLA latent 512 + 64 RoPE = 576 (DeepSeek-V3) [training knowledge]"),
    "state_gb": (0.0, "GB per session", "RED-TEAM [RT-IND-04]: fixed recurrent state per session (hybrid linear attention ~0.04 GB, rewritten every turn) [ESTIMATE]"),
    "prompt_tok_per_turn": (500.0, "tokens", "RED-TEAM: new prompt tokens prefilled per human turn (the other ~500 of tok_new_per_turn are decoded)"),
    "agent_tgen_s": (4.0, "s", "RED-TEAM [RT-CIRC-01]: ESTIMATE agent step: prefill tool output + emit ~100-300 tokens of reasoning/tool call"),
    "agent_gap_median_s": (3.0, "s", "RED-TEAM [RT-CIRC-01]: ESTIMATE tool-call wait median (reviewer: 1-10 s)"),
    "agent_gap_sigma": (1.2, "ln-units", "RED-TEAM [RT-CIRC-01]: ESTIMATE -> P90 ~14 s, P95 ~22 s, P99 ~49 s"),
    "agent_ctx_median": (24000.0, "tokens", "RED-TEAM [RT-CIRC-01]: ESTIMATE agent/API context (log-normal, mean ~33k)"),
    "agent_ctx_sigma": (0.8, "ln-units", "RED-TEAM [RT-CIRC-01]: ESTIMATE"),
    "agent_prompt_tok": (1000.0, "tokens", "RED-TEAM [RT-CIRC-01]: ESTIMATE tool-output tokens prefilled per agent step"),
    "agent_new_tok": (1300.0, "tokens", "RED-TEAM [RT-CIRC-01]: ESTIMATE new KV tokens per agent step (tool output + generated)"),
    "dgx_flash_tb_per_gpu": (3.84, "TB", "RED-TEAM [RT-PROC-01]: DGX B200 8 x 3.84 TB NVMe per 8 GPUs (reviewer figure) [training knowledge]"),
    "dram_gb_per_wafer": (3068.0, "GB DDR5-eq per wafer", "dram-moonshot A2 ESTIMATE (same basis as world_dram_eb)"),
    "nand_tb_per_wafer": (120.0, "TB per wafer", "RED-TEAM [RT-PROC-01]: reviewer 100-140 TB per 300 mm 2xx-layer TLC wafer"),
    "nand_kwh_per_wafer": (1300.0, "kWh per wafer", "RED-TEAM [RT-PROC-01]: ESTIMATE, taken equal to a DRAM wafer (0.42 kWh/GB x 3,068 GB) [SPECULATIVE parity]"),
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
    elems = v("kv_elems_layer") or 2 * v("kv_heads") * v("head_dim")
    return v("layers") * elems * v("kv_bytes") / k


def attn_flops_per_ctx_token():
    """Attention FLOPs per decoded token per context token (RED-TEAM compute bound)."""
    return v("attn_flops_ctx_override") or v("layers") * 4 * v("q_heads") * v("head_dim")


@contextmanager
def patched(**kw):
    """Temporarily override INPUT values (RED-TEAM model-mix runs)."""
    old = {k: INPUTS[k] for k in kw}
    for k, val in kw.items():
        INPUTS[k] = (val,) + tuple(INPUTS[k][1:])
    try:
        yield
    finally:
        INPUTS.update(old)


def ln_p_lt(t, mu, sig):
    if t <= 0:
        return 0.0
    return phi((math.log(t) - mu) / sig)


def ln_e_min(t, mu, sig):
    """E[min(G, t)] for G ~ log-normal(mu, sig)."""
    if t <= 0:
        return 0.0
    mean = math.exp(mu + sig ** 2 / 2)
    lt = math.log(t)
    return mean * phi((lt - mu - sig ** 2) / sig) + t * (1 - phi((lt - mu) / sig))


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
          sched="edf", waf=None, bw_derate=1.0, write_interf=None, compute=True):
    """mode: 'baseline' = HBM + LRU host-DRAM KV tier + flash, no client prefetch.
             'diet'     = HBM + flash direct (GDS), no host KV tier, client-signal prefetch.
    RED-TEAM additions: waf (NAND writes), bw_derate (EOL / throttling), write_interf (program/erase
    die-time in the flash queue), compute bound on active sessions with spare HBM as idle tier."""
    ctx_median = v("ctx_median") if ctx_median is None else ctx_median
    ctx_sigma = v("ctx_sigma") if ctx_sigma is None else ctx_sigma
    host_gb = (v("host_per_gpu_gb") if mode == "baseline" else v("host_lite_gb")) if host_gb is None else host_gb
    n_ssd = v("ssd_per_gpu") if n_ssd is None else n_ssd
    policy = v("policy") if policy is None else policy
    p_fp = (v("p_fp") if (mode == "diet" and prefetch) else 0.0) if p_fp is None else p_fp
    mc_n = v("mc_n") if mc_n is None else mc_n
    waf = v("waf") if waf is None else waf
    write_interf = v("write_interf") if write_interf is None else write_interf
    seed = v("seed")

    ctxs = ctx_samples(ctx_median, ctx_sigma, mc_n, seed)
    ctx_mean = sum(ctxs) / len(ctxs)
    kvt_cap = kv_bytes_per_token(k_cap)
    kvt_bw = kv_bytes_per_token(k_bw)
    state_gb = v("state_gb")
    kv_gb = ctx_mean * kvt_cap / 1e9 + state_gb            # mean session KV stored (GB)
    kv_read_gb = ctx_mean * kvt_bw / 1e9 + state_gb        # mean KV read per decode step per session

    t_gen = v("t_gen_s")
    hbm_kv_budget = v("hbm_per_gpu_gb") * v("hbm_util") - v("weights_gb")
    step_gb = v("hbm_bw_tbs") * 1e3 / v("target_tps_user")
    n_bw = (step_gb - v("weights_gb")) / kv_read_gb
    # RED-TEAM compute bound: decode at target_tps plus prompt prefill, per active session
    per_tok = 2 * v("active_params_b") * 1e9 + attn_flops_per_ctx_token() * ctx_mean
    eff_flops = v("gpu_fp8_pflops") * 1e15 * v("mfu_serve")
    n_comp = eff_flops / ((v("target_tps_user") + v("prompt_tok_per_turn") / t_gen) * per_tok) if compute else float("inf")
    p_ret = gap_p_lt(v("ttl_s"))
    host_kv_gb = max(0.0, host_gb - v("host_os_gb"))
    ssd_bw = v("ssd_read_gbs") * n_ssd * bw_derate
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
        n_a = min(n_cap, n_bw, n_comp)
        lam = n_a / t_gen                                  # turns started per s per GPU
        # RED-TEAM: HBM left over when bandwidth or compute binds holds idle KV (LRU) first
        spare = max(0.0, hbm_kv_budget - n_a * kv_gb * (1 + hold / t_gen))
        t_hbm = spare / (lam * kv_gb) if lam > 0 else 0.0
        p_hbm = min(gap_p_lt(t_hbm), p_ret) if spare > 1e-9 else 0.0
        if mode == "baseline":
            t_dram = (spare + host_kv_gb) / (lam * kv_gb) if lam > 0 else 0.0
            p_host = max(0.0, min(gap_p_lt(t_dram), p_ret) - p_hbm)
        else:
            t_dram = t_hbm
            p_host = 0.0
        demand = lam * (p_ret - p_host - p_hbm) * kv_gb * (1 + p_fp)   # GB/s flash reads
        w_gbs = lam * (v("tok_new_per_turn") * kvt_cap / 1e9 + state_gb) * v("spill_frac")
        rho_w = write_interf * w_gbs * waf / (v("ssd_write_gbs") * n_ssd * bw_derate)
        rho = demand / ssd_bw + rho_w
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
            if mode == "baseline":
                u_t = rng.random()
                if u_t < (p_hbm / p_ret if p_ret > 0 else 0):
                    extras.append(0.0)
                    continue
                if u_t < ((p_hbm + p_host) / p_ret if p_ret > 0 else 0):
                    extras.append(kv_i / v("c2c_gbs"))
                    continue
            elif p_hbm > 0 and rng.random() < p_hbm / p_ret:
                extras.append(0.0)
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
                   host_gb=host_gb, s_mean=kv_gb / ssd_bw, urgent_frac=urgent_frac,
                   n_comp=n_comp, spare=spare, p_hbm_of_returns=(p_hbm / p_ret if p_ret else 0.0),
                   rho_w=rho_w, w_gbs=w_gbs, n_ssd=n_ssd, waf=waf)
        if mode == "baseline":
            break
    # NAND writes and capacity (RED-TEAM: NAND-side = host writes x WAF)
    writes_gb_day = res["w_gbs"] * 86400
    stored_gb = res["lam"] * gap_e_min(v("retain_ssd_s")) * kv_gb
    res["writes_gb_day"] = writes_gb_day
    res["nand_writes_gb_day"] = writes_gb_day * waf
    res["dwpd_host"] = writes_gb_day / (v("ssd_cap_gb") * n_ssd)
    res["dwpd"] = writes_gb_day * waf / (v("ssd_cap_gb") * n_ssd)
    res["stored_gb"] = stored_gb
    res["dram_gb_gpu"] = v("hbm_per_gpu_gb") + host_gb
    res["dram_per_user"] = res["dram_gb_gpu"] / res["users"]
    res["wafer_eq_per_user"] = (v("hbm_per_gpu_gb") * v("hbm_wafer_mult") + host_gb) / res["users"]
    return res


def drives_needed(r, dwpd):
    """Drives per GPU to satisfy bandwidth (rho_max, reads + program die-time), endurance (dwpd,
    NAND-side writes incl. WAF) and capacity."""
    n_bw = (r["demand"] / v("ssd_read_gbs") + v("write_interf") * r["w_gbs"] * r["waf"] / v("ssd_write_gbs")) / v("rho_max")
    n_end = r["nand_writes_gb_day"] / (v("ssd_cap_gb") * dwpd)
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


# --------------------------------------------------------------------------------------------
# RED-TEAM helpers (2026-11-02)
# --------------------------------------------------------------------------------------------
MLA_PATCH = dict(layers=61, kv_elems_layer=576, weights_gb=84.0, active_params_b=37.0,
                 attn_flops_ctx_override=61 * 2 * 128 * (576 + 512))
# ESTIMATE [training knowledge]: DeepSeek-V3/R1-class MLA, 671B total / 37B active, FP8 weights
# sharded 8 ways (~84 GB per GPU, all read per decode step at large batch).
HYB_PATCH = dict(layers=12, kv_heads=2, head_dim=256, q_heads=16, weights_gb=80.0, active_params_b=3.0,
                 state_gb=0.04)
# ESTIMATE [training knowledge]: Qwen3-Next-80B-A3B-class hybrid: 12 of 48 layers full attention
# (2 KV heads x 256), 36 Gated-DeltaNet layers with ~40 MB bf16 recurrent state per session.


def min_drives_rt(mode="diet", prefetch=False, budget=None, mc_n=8000, **kw):
    """Drive-equivalents per GPU for p99 added TTFT <= budget (bisection)."""
    budget = v("ttft_budget_s") if budget is None else budget
    lo, hi = 0.5, 24.0
    if serve(mode, n_ssd=hi, prefetch=prefetch, mc_n=mc_n, **kw)["p99_extra"] > budget:
        return float("inf")
    for _ in range(9):
        mid = (lo + hi) / 2
        if serve(mode, n_ssd=mid, prefetch=prefetch, mc_n=mc_n, **kw)["p99_extra"] <= budget:
            hi = mid
        else:
            lo = mid
    return hi


def path_dram(host_gb, n_ssd, ftl, shelf=True, hbm_mult=1.0):
    """Full KV-path DRAM per GPU [RT-CIRC-03]: HBM (x hbm_mult) + host + SSD FTL + shelf heads."""
    local = min(n_ssd, v("local_bays_per_gpu"))
    remote = max(0.0, n_ssd - local) if shelf else 0.0
    ftl_gb = n_ssd * v("ssd_cap_gb") / 1e3 * ftl
    shelf_gb = remote * v("shelf_dram_gb_per_drive")
    return v("hbm_per_gpu_gb") * hbm_mult + host_gb + ftl_gb + shelf_gb, ftl_gb, shelf_gb


def lru_T(pool_gb, classes):
    """Exclusive LRU hold time T with sum_c E_c * E[min(g_c, T)] = pool. classes: (E, mu, sig)."""
    if pool_gb <= 0:
        return 0.0
    lo, hi = 0.0, 1e5
    for _ in range(80):
        mid = (lo + hi) / 2
        occ = sum(E * ln_e_min(mid, mu, sg) for E, mu, sg in classes)
        if occ < pool_gb:
            lo = mid
        else:
            hi = mid
    return lo


def agent_mix(s_a, mc_n=20000):
    """[RT-CIRC-01] GPU share s_a serves agent/API traffic, 1 - s_a human chat (base mix, no signal).
    Returns per-GPU results for A_mix (240 GB host, shared exclusive LRU over spare HBM + host),
    B_flash (host-lite 64 GB; agents restored from flash on arrival) and B_gap (gap-aware: humans
    bypass host; host right-sized so agents keep today's A_mix hold time, i.e. the same agent hit rate)."""
    A = serve("baseline", mc_n=mc_n)
    kvt = kv_bytes_per_token()
    h_mu, h_sig = GAP_MU, GAP_SIG
    a_mu, a_sig = math.log(v("agent_gap_median_s")), v("agent_gap_sigma")
    p_ret_h = gap_p_lt(v("ttl_s"))
    # human class, scaled from the share-1 baseline
    hs = 1.0 - s_a
    kv_h = A["kv_gb"]
    lam_h = hs * A["lam"]
    E_h = lam_h * kv_h
    spare_h = hs * A["spare"]
    w_h = lam_h * v("tok_new_per_turn") * kvt / 1e9
    # agent class
    rng = random.Random(v("seed") + 11)
    cap = v("ctx_cap")
    actx = [min(cap, rng.lognormvariate(math.log(v("agent_ctx_median")), v("agent_ctx_sigma"))) for _ in range(mc_n)]
    actx_mean = sum(actx) / len(actx)
    kv_a = actx_mean * kvt / 1e9
    budget = v("hbm_per_gpu_gb") * v("hbm_util") - v("weights_gb")
    step_gb = v("hbm_bw_tbs") * 1e3 / v("target_tps_user")
    per_tok = 2 * v("active_params_b") * 1e9 + attn_flops_per_ctx_token() * actx_mean
    eff = v("gpu_fp8_pflops") * 1e15 * v("mfu_serve")
    n_cap_a = s_a * budget / kv_a
    n_bw_a = s_a * (step_gb - v("weights_gb")) / kv_a
    n_comp_a = s_a * eff / ((v("target_tps_user") + v("agent_prompt_tok") / v("agent_tgen_s")) * per_tok)
    n_ag = min(n_cap_a, n_bw_a, n_comp_a)
    spare_a = max(0.0, s_a * budget - n_ag * kv_a)
    lam_a = n_ag / v("agent_tgen_s")
    E_a = lam_a * kv_a
    w_a = lam_a * v("agent_new_tok") * kvt / 1e9
    host_kv_A = v("host_per_gpu_gb") - v("host_os_gb")
    cls = [(E_h, h_mu, h_sig), (E_a, a_mu, a_sig)]

    def drives_for(demand, w):
        n_bw = (demand / v("ssd_read_gbs") + v("write_interf") * w * v("waf") / v("ssd_write_gbs")) / v("rho_max")
        n_end = w * v("waf") * 86400 / (v("ssd_cap_gb") * v("dwpd_mixed"))
        return max(n_bw, n_end)

    def p99s(hit_h, host_h, hit_a, host_a, demand, w, n_ssd):
        """MC p99 added TTFT per class; hit_* = served from spare HBM, host_* = from host DRAM."""
        bw = v("ssd_read_gbs") * n_ssd
        rho = min(0.98, demand / bw + v("write_interf") * w * v("waf") / (v("ssd_write_gbs") * n_ssd))
        r2 = random.Random(v("seed") + 13)
        hctx = ctx_samples(v("ctx_median"), v("ctx_sigma"), mc_n, v("seed"))
        out = []
        for ctxs, hit, hst, ret in ((hctx, hit_h, host_h, p_ret_h), (actx, hit_a, host_a, 1.0)):
            ex = []
            for c in ctxs:
                kv_i = c * kvt / 1e9
                u = r2.random() * ret
                if u < hit:
                    ex.append(0.0)
                elif u < hit + hst:
                    ex.append(kv_i / v("c2c_gbs"))
                else:
                    s_i = kv_i / bw
                    wq = r2.expovariate((1 - rho) / s_i) if r2.random() < rho else 0.0
                    ex.append(v("f_fb") * (s_i + wq))
            ex.sort()
            out.append(ex[int(0.99 * (len(ex) - 1))])
        return out[0], out[1], rho

    res = {}
    # A_mix: shared exclusive LRU over spare HBM + 176 GB host KV
    T_hbm = lru_T(spare_h + spare_a, cls)
    T_A = lru_T(spare_h + spare_a + host_kv_A, cls)
    hh_hbm, ha_hbm = min(gap_p_lt(T_hbm), p_ret_h), ln_p_lt(T_hbm, a_mu, a_sig)
    hh_A, ha_A = min(gap_p_lt(T_A), p_ret_h), ln_p_lt(T_A, a_mu, a_sig)
    dem_A = lam_h * (p_ret_h - hh_A) * kv_h + lam_a * (1 - ha_A) * kv_a
    nA = max(v("ssd_per_gpu"), drives_for(dem_A, w_h + w_a))
    pA = p99s(hh_hbm, hh_A - hh_hbm, ha_hbm, ha_A - ha_hbm, dem_A, w_h + w_a, nA)
    res["A"] = dict(host=v("host_per_gpu_gb"), T=T_A, hit_h=hh_A, hit_a=ha_A, demand=dem_A, w=w_h + w_a,
                    n_ssd=nA, p99_h=pA[0], p99_a=pA[1], rho=pA[2])
    # B_flash: host-lite, idle pool = spare HBM only, agents from flash on arrival
    dem_B = lam_h * (p_ret_h - hh_hbm) * kv_h + lam_a * (1 - ha_hbm) * kv_a
    nB = max(v("ssd_per_gpu"), drives_for(dem_B, w_h + w_a))
    pB = p99s(hh_hbm, 0.0, ha_hbm, 0.0, dem_B, w_h + w_a, nB)
    lo, hi = nB, 40.0
    if p99s(hh_hbm, 0.0, ha_hbm, 0.0, dem_B, w_h + w_a, hi)[1] > v("ttft_budget_s"):
        n_p99 = float("inf")
    else:
        for _ in range(10):
            mid = (lo + hi) / 2
            if p99s(hh_hbm, 0.0, ha_hbm, 0.0, dem_B, w_h + w_a, mid)[1] <= v("ttft_budget_s"):
                hi = mid
            else:
                lo = mid
        n_p99 = hi
    res["B_flash"] = dict(host=v("host_lite_gb"), hit_h=hh_hbm, hit_a=ha_hbm, demand=dem_B, w=w_h + w_a,
                          n_ssd=nB, p99_h=pB[0], p99_a=pB[1], rho=pB[2], n_p99_agent=n_p99)
    # B_gap: humans bypass host (pool = their spare HBM); agents get spare HBM + right-sized host
    Th = lru_T(spare_h, [cls[0]])
    hh_G = min(gap_p_lt(Th), p_ret_h)
    T_star = T_A
    host_kv_a = max(0.0, E_a * ln_e_min(T_star, a_mu, a_sig) - spare_a) if s_a > 0 else 0.0
    Ta_hbm = lru_T(spare_a, [cls[1]])
    ha_hbm_G = ln_p_lt(Ta_hbm, a_mu, a_sig) if s_a > 0 else 0.0
    ha_G = ln_p_lt(T_star, a_mu, a_sig) if s_a > 0 else 0.0
    ha_G = max(ha_G, ha_hbm_G)
    dem_G = lam_h * (p_ret_h - hh_G) * kv_h + lam_a * (1 - ha_G) * kv_a
    w_G = w_h + w_a                                  # write-through of new chunks, as in A_mix
    nG = max(v("ssd_per_gpu") if s_a < 1 else 1.0, drives_for(dem_G, w_G))
    pG = p99s(hh_G, 0.0, ha_hbm_G, ha_G - ha_hbm_G, dem_G, w_G, nG)
    res["B_gap"] = dict(host=v("host_lite_gb") + host_kv_a, hit_h=hh_G, hit_a=ha_G, demand=dem_G, w=w_G,
                        n_ssd=nG, p99_h=pG[0], p99_a=pG[1], rho=pG[2], T_star=T_star)
    res["meta"] = dict(n_ag=n_ag, n_cap_a=n_cap_a, n_comp_a=n_comp_a, kv_a=kv_a, actx_mean=actx_mean,
                       spare_a=spare_a, E_a=E_a, E_h=E_h, lam_a=lam_a)
    return res


def noflash_baseline(host_gb=None, mc_n=20000):
    """[RT-PROC-01] DGX-class node without a KV flash tier: idle KV in spare HBM + host LRU,
    misses recomputed by prefill. Active sessions are cut until prefill + decode FLOPs fit."""
    host_gb = v("host_per_gpu_gb") if host_gb is None else host_gb
    ctxs = ctx_samples(v("ctx_median"), v("ctx_sigma"), mc_n, v("seed"))
    ctx_mean = sum(ctxs) / len(ctxs)
    kv = ctx_mean * kv_bytes_per_token() / 1e9
    t_gen = v("t_gen_s")
    budget = v("hbm_per_gpu_gb") * v("hbm_util") - v("weights_gb")
    step_gb = v("hbm_bw_tbs") * 1e3 / v("target_tps_user")
    n_max = min(budget / kv, (step_gb - v("weights_gb")) / kv)
    per_tok = 2 * v("active_params_b") * 1e9 + attn_flops_per_ctx_token() * ctx_mean
    eff = v("gpu_fp8_pflops") * 1e15 * v("mfu_serve")
    p_ret = gap_p_lt(v("ttl_s"))
    host_kv = max(0.0, host_gb - v("host_os_gb"))
    rec = (2 * v("active_params_b") * 1e9 + attn_flops_per_ctx_token() * ctx_mean / 2) * ctx_mean

    def comp(n):
        lam = n / t_gen
        spare = max(0.0, budget - n * kv)
        T = (spare + host_kv) / (lam * kv)
        p_hit = min(gap_p_lt(T), p_ret)
        return n * (v("target_tps_user") + v("prompt_tok_per_turn") / t_gen) * per_tok + lam * (p_ret - p_hit) * rec, p_hit, T

    lo, hi = 0.1, n_max
    for _ in range(60):
        mid = (lo + hi) / 2
        if comp(mid)[0] <= eff:
            lo = mid
        else:
            hi = mid
    n = lo
    _, p_hit, T = comp(n)
    users = n * (t_gen + gap_e_min(v("ttl_s"))) / t_gen
    c99 = sorted(ctxs)[int(0.99 * (len(ctxs) - 1))]
    rec99 = (2 * v("active_params_b") * 1e9 + attn_flops_per_ctx_token() * c99 / 2) * c99
    return dict(n_a=n, users=users, p_hit=p_hit, T=T, ttft_mean=rec / eff, ttft_p99=rec99 / eff,
                dram_per_user=(v("hbm_per_gpu_gb") + host_gb) / users)


def wafers_per_k(host_gb, flash_tb, users):
    """DRAM (DDR5-eq, HBM x3) and NAND 300 mm wafer starts per 1,000 conversations."""
    d = (v("hbm_per_gpu_gb") * v("hbm_wafer_mult") + host_gb) / v("dram_gb_per_wafer") * 1000 / users
    n = flash_tb / v("nand_tb_per_wafer") * 1000 / users
    return d, n


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
    P(f"| Scenario | read demand GB/s | host writes TB/day | NAND DWPD on base drives (WAF {v('waf'):g}) | stored TB (1 h retention) | drives needed @1 DWPD | drives needed @3 DWPD | SSD $/rack @3 DWPD |")
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
    P(f"**Revised GO/NO-GO (after red team; numbers in section 11):** GO if, replaying a measured human-chat plus agent/API trace mix on one 8-GPU node at equal tokens/s against a 240 GB/GPU LRU host-tier baseline, with a gap-aware host tier (human-chat KV bypasses host; host = {v('host_lite_gb'):.0f} GB/GPU plus the measured agent working set): (1) p99 added TTFT <= {v('ttft_budget_s')} s for both human and agent turns at <= 3.5 Gen5 drive-eq/GPU (2 local + shelf), measured under the full read-plus-write mix on FDP drives, including a pre-cycled (>= 80% rated wear) arm and a 24 h soak at rack inlet temperature; (2) NAND-side WAF <= 1.25 and NAND-side writes <= 3 DWPD from the vendor log page; (3) full-KV-path DRAM (host RSS + SSD controller DRAM + shelf heads) gives >= 1.4x fewer DRAM GB per human-chat conversation; (4) the same holds on one MLA-class model with <= 2 local drives. NO-GO if host-lite on the human-chat share fails p99 at <= 5 drive-eq/GPU at end of life, or the full-path ratio is < 1.25x. The single all-layer latent is dropped; the latent gate becomes a decode-tokens/s-at-batch check of prior-art per-layer retrofits.")
    P("")

    # ---- 11. RED-TEAM REVISIONS
    P("## 11. RED-TEAM REVISIONS (2026-11-02)")
    P("")
    P("Owner runs answering `research/redteam/rt_*.json`. Sections 1-10 above already include the revised inputs (WAF 1.1, program/erase die-time in the flash queue, compute bound, per-layer latent, LPDDR5X W/GB).")
    P("")
    # 11.1 latent geometry
    P("### 11.1 Latent geometry vs decode reads [RT-CIRC-02]")
    P("")
    P("A latent shared by g layers at 3x capacity compression: each layer reads its group's whole latent, so per-step KV reads = GQA x g / 3 (k_bw = 3 / g).")
    P("")
    P("| layers per latent g | k_bw | KV read per decode step, 32k session GB | n_bw (HBM-bandwidth sessions) | n_comp | active/GPU | conversations/GPU | DRAM GB/conv gain vs A (host-lite) |")
    P("|---|---|---|---|---|---|---|---|")
    lat_rows = {}
    for g_l in (1, 2, 3, 8, 80):
        kb = v("k_cap_latent") / g_l
        r = serve("diet", k_cap=v("k_cap_latent"), k_bw=kb, prefetch=False, mc_n=20000)
        lat_rows[g_l] = r
        P(f"| {g_l} | {kb:.3f} | {32000*kv_bytes_per_token(kb)/1e9:.2f} | {r['n_bw']:.1f} | {r['n_comp']:.0f} | {r['n_a']:.1f} | {r['users']:,.0f} | {A['dram_per_user']/r['dram_per_user']:.2f}x |")
    P("")
    P(f"Reading: the all-layer latent (g = 80) reads {32000*kv_bytes_per_token(v('k_cap_latent')/80)/1e9:.0f} GB per step for one 32k session versus {32000*kv_bytes_per_token()/1e9:.1f} GB for GQA FP8; HBM bandwidth then allows only ~{lat_rows[80]['n_a']:.0f} active sessions per GPU (vs {A['n_a']:.0f}). **The single all-layer latent is killed.** Per-layer (g = 1) keeps reads 3x below GQA, but even then the GPU's FLOPs (decode + prompt prefill, n_comp ~{lat_rows[1]['n_comp']:.0f}) bind before HBM capacity ({lat_rows[1]['n_cap']:.0f}), so a 3x latent buys {lat_rows[1]['n_a']/A['n_a']:.2f}x active sessions, not 3x.")
    P("")
    # 11.2 full KV path DRAM bill
    P("### 11.2 DRAM across the full KV path [RT-CIRC-03]")
    P("")
    nA_p99 = min_drives_rt("baseline")
    nB0_p99 = min_drives_rt("diet", prefetch=False)
    P(f"Drive-eq/GPU for p99 <= {v('ttft_budget_s')} s with write interference (WAF {v('waf'):g}): today A {nA_p99:.1f}, host-lite B0 {nB0_p99:.1f}. Local E1.S bays: {v('local_bays_per_gpu'):.0f} per GPU; the rest comes from pod shelves.")
    P("")
    P("| accounting | A DRAM GB/GPU | B0 DRAM GB/GPU | gain B0 vs A (DRAM GB/conv) | A wafer-eq | B0 wafer-eq | gain (wafer-eq) |")
    P("|---|---|---|---|---|---|---|")
    path_rows = []
    for lab, nA_, nB_, ftl, shelf, hostB in (
            ("HBM + host only (dossier v1), 3 drive-eq", 3, 3, 0.0, False, 64),
            ("+ SSD FTL DRAM (4 KiB IU), 3 drive-eq", 3, 3, v("ftl_gb_per_tb"), False, 64),
            ("+ FTL 4 KiB + shelf DRAM for drive-eq beyond 2 local, 3 drive-eq", 3, 3, v("ftl_gb_per_tb"), True, 64),
            ("FTL 4 KiB + shelf, drive-eq sized for p99 (A %.1f, B0 %.1f)" % (nA_p99, nB0_p99), nA_p99, nB0_p99, v("ftl_gb_per_tb"), True, 64),
            ("large-IU/ZNS drives (64 KiB) + shelf, p99-sized", nA_p99, nB0_p99, v("ftl_gb_per_tb_large_iu"), True, 64),
            ("critic host floor 120 GB, FTL 4 KiB + shelf, p99-sized", nA_p99, nB0_p99, v("ftl_gb_per_tb"), True, 120)):
        a = path_dram(v("host_per_gpu_gb"), nA_, ftl, shelf)[0]
        b = path_dram(hostB, nB_, ftl, shelf)[0]
        aw = path_dram(v("host_per_gpu_gb"), nA_, ftl, shelf, hbm_mult=v("hbm_wafer_mult"))[0]
        bw_ = path_dram(hostB, nB_, ftl, shelf, hbm_mult=v("hbm_wafer_mult"))[0]
        path_rows.append((lab, a / b, aw / bw_))
        P(f"| {lab} | {a:.0f} | {b:.0f} | {a/b:.2f}x | {aw:.0f} | {bw_:.0f} | {aw/bw_:.2f}x |")
    P("")
    P("Reading: SSD controller DRAM and shelf heads cost host-lite ~0.05-0.1x of its gain; large-indirection-unit or ZNS drives (KV chunks are ~40 MB sequential appends) recover most of it. B0 stays >= 1.4x on DRAM GB per conversation at the 64 GB host floor, and ~1.25x at the critic's 120 GB floor.")
    P("")
    # 11.3 WAF
    P("### 11.3 Write amplification and endurance [RT-DEV-01]")
    P("")
    P("| WAF | B NAND DWPD on 3 x 15.36 TB | B0 NAND DWPD | endurance drive-eq @3 DWPD (B0) | B0 p99 s @3 drive-eq | B p99 s @3 drive-eq |")
    P("|---|---|---|---|---|---|")
    for wf in (1.0, 1.1, 1.3, 1.5, 2.0):
        rb = serve("diet", waf=wf, mc_n=20000)
        rb0 = serve("diet", waf=wf, prefetch=False, mc_n=20000)
        P(f"| {wf:g} | {rb['dwpd']:.2f} | {rb0['dwpd']:.2f} | {rb0['nand_writes_gb_day']/(v('ssd_cap_gb')*v('dwpd_mixed')):.2f} | {f(rb0['p99_extra'])} | {f(rb['p99_extra'])} |")
    P("")
    P("Reading: at WAF 1.3-2.0 (no placement control) endurance, not bandwidth, sets the drive count (3.5-5.5 drive-eq). With FDP placement by expiry class (WAF ~1.0-1.1; CacheLib+FDP reached ~1 on production traces) 3 drive-eq hold at <= 3 NAND DWPD. G2 must read NAND-side writes (vendor/OCP log page), not host writes.")
    P("")
    # 11.4 interference / EOL / throttling
    P("### 11.4 Program/erase interference, end-of-life and thermal throttling [RT-CIRC-04, RT-DEV-02, RT-DEV-04]")
    P("")
    P("| case (base mix, FP8, 3 drive-eq) | B0 p99 s | B (signal) p99 s | B0 drive-eq for p99 <= budget | B drive-eq for p99 <= budget |")
    P("|---|---|---|---|---|")
    stress = (("reads only (dossier v1 queue)", dict(write_interf=0.0, waf=1.0)),
              ("+ program/erase die-time, WAF 1.1 (revised base)", dict()),
              ("+ WAF 2.0 (no FDP)", dict(waf=2.0)),
              ("end of life (read x 0.85)", dict(bw_derate=v("eol_read_derate"))),
              ("1 of 3 drives throttled to 50%", dict(bw_derate=v("throttle_derate"))),
              ("EOL + throttled + WAF 1.1", dict(bw_derate=v("eol_read_derate") * v("throttle_derate"))))
    st_rows = {}
    for lab, kw in stress:
        r0 = serve("diet", prefetch=False, mc_n=20000, **kw)
        r1 = serve("diet", mc_n=20000, **kw)
        d0 = min_drives_rt("diet", prefetch=False, **kw)
        d1 = min_drives_rt("diet", prefetch=True, **kw)
        st_rows[lab] = (r0, r1, d0, d1)
        P(f"| {lab} | {f(r0['p99_extra'])} | {f(r1['p99_extra'])} | {f(d0, 1)} | {f(d1, 1)} |")
    P("")
    P(f"Reading: program/erase die-time, wear and throttling cost up to ~{st_rows[stress[-1][0]][2]-st_rows[stress[0][0]][2]:.1f} drive-eq/GPU of margin without the signal and ~{st_rows[stress[-1][0]][3]-st_rows[stress[0][0]][3]:.1f} with it. Host-lite without the signal needs ~{st_rows[stress[1][0]][2]:.1f} drive-eq/GPU fresh, ~{st_rows[stress[3][0]][2]:.1f} at end of life or with one drive throttled, and ~{st_rows[stress[-1][0]][2]:.1f} with both; with the deadline queue {st_rows[stress[1][0]][3]:.1f}-{st_rows[stress[-1][0]][3]:.1f}. The fix is flash (and FDP / program-suspend drives), not DRAM, but the GO line must be tested on pre-cycled drives at rack inlet temperature.")
    P("")
    # 11.5 energy
    P("### 11.5 Energy in use [RT-DEV-03]")
    P("")
    fr_tb = fr64 / 1e3
    P(f"- Freed host LPDDR5X per rack: {fr_tb:.1f} TB x {v('dram_w_per_gb')} W/GB = **{fr64*v('dram_w_per_gb')/1e3:.2f} kW** (range {fr64*0.03/1e3:.2f}-{fr64*0.05/1e3:.2f} kW at 0.03-0.05 W/GB; dossier v1 said 1.9 kW at 0.15 W/GB).")
    P(f"- 3 drive-eq/GPU = {3*g:.0f} drives per rack x {v('ssd_w'):.0f} W = {3*g*v('ssd_w')/1e3:.1f} kW (range {3*g*15/1e3:.1f}-{3*g*25/1e3:.1f} kW).")
    P(f"- Against a 2026 flash-tier baseline with the same drives the diet saves ~{fr64*0.03/1e3:.1f}-{fr64*0.05/1e3:.1f} kW per rack (well under 1% of a ~130 kW rack). Against a DGX-class rack with {g:.0f} local drives it adds ~{(3*g-g)*15/1e3 - fr64*0.05/1e3:.1f}-{(3*g-g)*25/1e3 - fr64*0.03/1e3:.1f} kW per rack, but that rack serves far fewer conversations per GPU (11.8).")
    P("")
    # 11.6 agent mix
    P("### 11.6 Agent and API traffic [RT-CIRC-01, RT-IND-05]")
    P("")
    P(f"Agent class [ESTIMATE]: tool-wait gap log-normal median {v('agent_gap_median_s'):.0f} s (sigma {v('agent_gap_sigma')}), step time {v('agent_tgen_s'):.0f} s, context median {v('agent_ctx_median')/1000:.0f}k (sigma {v('agent_ctx_sigma')}), {v('agent_prompt_tok'):.0f} tool-output tokens prefilled per step, no client signal. s_a = share of GPU capacity serving agent/API traffic. Placements: **A_mix** today's 240 GB host, one exclusive LRU over spare HBM + host; **B_flash** host-lite, agents restored from flash on arrival; **B_gap** gap-aware: human-chat KV bypasses host; host right-sized so agents keep A_mix's hold time (same agent DRAM hit rate as today).")
    P("")
    P("| s_a | agent active/GPU (cap / comp) | A_mix: agent / human returns from DRAM | A_mix flash GB/s, drive-eq | B_flash: flash GB/s, drive-eq | B_flash agent p99 s | B_flash drive-eq for agent p99 <= budget | B_gap host GB/GPU | B_gap agent / human p99 s | DRAM GB/conv gain vs A_mix: B_flash / B_gap |")
    P("|---|---|---|---|---|---|---|---|---|---|")
    ag_rows = {}
    for s_a in (0.0, 0.25, 0.5, 0.75, 1.0):
        m = agent_mix(s_a)
        ag_rows[s_a] = m
        mt, ra, rbf, rg = m["meta"], m["A"], m["B_flash"], m["B_gap"]
        gbf = 528.0 / (v("hbm_per_gpu_gb") + rbf["host"])
        ggp = 528.0 / (v("hbm_per_gpu_gb") + rg["host"])
        na = (lambda x: "n/a") if s_a == 0 else (lambda x: x)
        hit_a_txt = "%.0f%%" % (ra["hit_a"] * 100)
        P(f"| {s_a:.2f} | {mt['n_ag']:.1f} ({mt['n_cap_a']:.0f} / {mt['n_comp_a']:.0f}) | {na(hit_a_txt)} / {ra['hit_h']*100:.1f}% | {ra['demand']:.1f}, {ra['n_ssd']:.1f} | {rbf['demand']:.1f}, {rbf['n_ssd']:.1f} | {na(f(rbf['p99_a']))} | {na(f(rbf['n_p99_agent'], 1))} | {rg['host']:.0f} | {na(f(rg['p99_a']))} / {f(rg['p99_h'])} | {gbf:.2f}x / {ggp:.2f}x |")
    P("")
    g1 = 528.0 / (v("hbm_per_gpu_gb") + ag_rows[1.0]["B_gap"]["host"])
    P(f"Reading: agent tool waits are seconds long, so today's host tier catches most agent returns ({ag_rows[0.5]['A']['hit_a']*100:.0f}% at s_a = 0.5) while catching almost no human-chat returns. Host-lite with agents on flash (restore on arrival, no server-side deadline) keeps the 1.50x DRAM figure but needs ~{ag_rows[0.5]['B_flash']['n_p99_agent']:.1f} drive-eq/GPU at s_a = 0.5 for the agent p99 (70B GQA FP8 contexts of ~{ag_rows[0.5]['meta']['kv_a']:.1f} GB; today's A_mix agent p99 is {f(ag_rows[0.5]['A']['p99_a'])} s): more flash than the 2 local bays plus one shelf drive. The gap-aware design keeps a right-sized host tier for agents and deletes only the human-chat share: {ag_rows[0.25]['B_gap']['host']:.0f} / {ag_rows[0.5]['B_gap']['host']:.0f} / {ag_rows[0.75]['B_gap']['host']:.0f} GB/GPU at s_a = 0.25 / 0.5 / 0.75; an agent-only node keeps ~{ag_rows[1.0]['B_gap']['host']:.0f} GB/GPU ({g1:.2f}x). **So the diet is a human-chat-pool design: the DRAM gain scales with the human-chat share of serving capacity.**")
    P("")
    P("| human-chat share of fleet capacity | fleet DRAM GB/conv gain (human pools B0 1.50x incl. host only; agent pools gap-aware) | with full-path DRAM (11.2, p99-sized) |")
    P("|---|---|---|")
    g_h_path = path_rows[3][1]
    for sh in (1.0, 0.75, 0.5, 0.25):
        gf = 1.0 / (sh / 1.50 + (1 - sh) / g1)
        gfp = 1.0 / (sh / g_h_path + (1 - sh) / g1)
        P(f"| {sh*100:.0f}% | {gf:.2f}x | {gfp:.2f}x |")
    P("")
    # 11.7 MLA / hybrid
    P("### 11.7 MLA and hybrid linear-attention models [RT-IND-04]")
    P("")
    P("| model (base context mix) | KV/token KiB | KV/session GB | n_cap / n_bw / n_comp | active/GPU | conv/GPU | A: returns from spare HBM / host | B0 flash read GB/s | host writes TB/day | B0 drive-eq @3 DWPD (bw, end.) | B0 p99 s @2 local drives | B p99 s @2 | DRAM GB/conv gain B0 vs A |")
    P("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    mm_rows = {}
    for lab, patch in (("70B GQA FP8 (dossier base)", {}), ("MLA, DeepSeek-V3-class FP8", MLA_PATCH), ("hybrid, Qwen3-Next-class (+40 MB state/turn)", HYB_PATCH)):
        with patched(**patch):
            ra = serve("baseline", mc_n=20000)
            rb0 = serve("diet", prefetch=False, mc_n=20000)
            rb0_2 = serve("diet", prefetch=False, n_ssd=2.0, mc_n=20000)
            rb_2 = serve("diet", n_ssd=2.0, mc_n=20000)
            dn = drives_needed(rb0, v("dwpd_mixed"))
            kvt_k = kv_bytes_per_token() / 1024
        mm_rows[lab] = (ra, rb0, rb0_2, rb_2, dn)
        P(f"| {lab} | {kvt_k:.1f} | {ra['kv_gb']:.2f} | {ra['n_cap']:.0f} / {ra['n_bw']:.0f} / {ra['n_comp']:.0f} | {ra['n_a']:.0f} | {ra['users']:,.0f} | {ra['p_hbm_of_returns']*100:.0f}% / {ra['p_host_of_returns']*100:.0f}% | {rb0['demand']:.1f} | {rb0['writes_gb_day']/1e3:.1f} | {dn[1]:.2f}, {dn[2]:.2f} | {f(rb0_2['p99_extra'])} | {f(rb_2['p99_extra'])} | {ra['dram_per_user']/rb0['dram_per_user']:.2f}x |")
    P("")
    mla = mm_rows["MLA, DeepSeek-V3-class FP8"]
    hyb = mm_rows["hybrid, Qwen3-Next-class (+40 MB state/turn)"]
    P(f"Reading: host-lite's DRAM ratio does not depend on bytes per token; it is set by how long the host tier can hold a session versus human gaps. MLA models are compute-bound at ~{mla[0]['n_comp']:.0f} active sessions, so ~{mla[0]['spare']:.0f} GB of HBM per GPU sits idle and itself holds idle KV; host-lite then needs ~{max(mla[4][1], mla[4][2]):.1f} drive-eq/GPU (fits the 2 local bays, no shelf) and restores in tens of ms, so the client signal and the latent become unnecessary. Hybrid models are HBM-bound again (turnover law: {hyb[1]['demand']:.0f} GB/s per GPU), and rewriting the ~40 MB recurrent state every turn makes endurance bind (~{hyb[4][2]:.1f} drive-eq/GPU at 3 DWPD, for today's flash-tier design as much as for host-lite) unless the state is quantized (FP8 halves it), spilled only for sessions predicted to return, or written to higher-endurance flash. That is a measured item, not a DRAM cost.")
    P("")
    # 11.8 no-flash baseline
    P("### 11.8 Against a DGX-class baseline with no KV flash [RT-PROC-01]")
    P("")
    nf = noflash_baseline()
    nf_m = None
    with patched(**MLA_PATCH):
        nf_m = noflash_baseline()
    P(f"No-flash node (240 GB host, {v('dgx_flash_tb_per_gpu')} TB/GPU NVMe not used for KV, misses recomputed): prefill FLOPs cap it at **{nf['n_a']:.0f} active / {nf['users']:,.0f} conversations per GPU** (vs {A['n_a']:.0f} / {A['users']:,.0f} with a flash tier); idle KV hits DRAM {nf['p_hit']*100:.0f}% of the time; a miss adds ~{nf['ttft_mean']:.1f} s mean and ~{nf['ttft_p99']:.0f} s p99 TTFT (full-GPU recompute), far past the {v('ttft_budget_s')} s budget. MLA-class: {nf_m['n_a']:.0f} active / {nf_m['users']:,.0f} conversations per GPU.")
    P("")
    P("| design (70B GQA FP8 unless noted) | host GB/GPU | flash TB/GPU | conv/GPU | DRAM GB/conv | DRAM wafers per 1,000 conv | NAND wafers per 1,000 conv | total wafers per 1,000 conv | fab kWh per 1,000 conv |")
    P("|---|---|---|---|---|---|---|---|---|")
    kwh_dw = v("kwh_per_gb") * v("dram_gb_per_wafer")
    B0_ = B0
    wrows = (("DGX-class, no KV flash (recompute)", v("host_per_gpu_gb"), v("dgx_flash_tb_per_gpu"), nf["users"]),
             ("A: 2026 flash tier, 3 drive-eq (dossier v1)", v("host_per_gpu_gb"), 3 * v("ssd_cap_gb") / 1e3, A["users"]),
             ("A: 2026 flash tier, %.1f drive-eq (p99-sized)" % nA_p99, v("host_per_gpu_gb"), nA_p99 * v("ssd_cap_gb") / 1e3, A["users"]),
             ("B0: host-lite, %.1f drive-eq (p99-sized)" % nB0_p99, v("host_lite_gb"), nB0_p99 * v("ssd_cap_gb") / 1e3, B0_["users"]),
             ("MLA: DGX-class no KV flash", v("host_per_gpu_gb"), v("dgx_flash_tb_per_gpu"), nf_m["users"]),
             ("MLA: B0 host-lite, 2 local drives", v("host_lite_gb"), 2 * v("ssd_cap_gb") / 1e3, mla[1]["users"]))
    wtab = {}
    for lab, h, ftb, us in wrows:
        dwf, nwf = wafers_per_k(h, ftb, us)
        wtab[lab] = (dwf, nwf)
        P(f"| {lab} | {h:.0f} | {ftb:.1f} | {us:,.0f} | {(v('hbm_per_gpu_gb')+h)/us:.3f} | {dwf:.3f} | {nwf:.3f} | {dwf+nwf:.3f} | {dwf*kwh_dw + nwf*v('nand_kwh_per_wafer'):,.0f} |")
    P("")
    add_nand = (3 * v("ssd_cap_gb") / 1e3 - v("dgx_flash_tb_per_gpu")) * g / v("nand_tb_per_wafer")
    save_dram = fr64 / v("dram_gb_per_wafer")
    P(f"Reading: per rack the reviewer is right: 3 drive-eq/GPU instead of DGX-class 3.84 TB/GPU adds ~{add_nand:.0f} NAND wafers per rack, against ~{save_dram:.1f} DRAM wafer-eq of host DRAM freed. Per served conversation it is the other way round: the flash tier (prior art, ICMS/LMCache) is what lets a GPU serve ~{A['users']/nf['users']:.1f}x more conversations, so total wafer starts per 1,000 conversations fall ~{(sum(wtab['DGX-class, no KV flash (recompute)']))/(sum(wtab[list(wtab)[3]])):.1f}x. Credit for that belongs to the flash tier, not to the diet. The diet's own increment over A at equal p99 ({nA_p99:.1f} vs {nB0_p99:.1f} drive-eq) is {sum(wtab[list(wtab)[2]])/sum(wtab[list(wtab)[3]]):.2f}x in total (DRAM + NAND) wafer starts per conversation: on resource intensity it is close to neutral.")
    P("")
    # 11.9 revised headline
    P("### 11.9 Revised step-change claim [RT-IND-02, RT-PROC-02]")
    P("")
    g_wafer_path = path_rows[3][2]
    P(f"- Human-chat pool, 70B GQA FP8, host-lite 64 GB vs today, full KV path, p99-sized flash: **{path_rows[3][1]:.2f}x fewer DRAM GB per conversation, {g_wafer_path:.2f}x in wafer terms** (large-IU drives {path_rows[4][1]:.2f}x / {path_rows[4][2]:.2f}x; critic's 120 GB floor {path_rows[5][1]:.2f}x / {path_rows[5][2]:.2f}x).")
    P(f"- MLA-class models: {mla[0]['dram_per_user']/mla[1]['dram_per_user']:.2f}x on HBM + host with 2 local drives and no shelf; wafer terms {((v('hbm_per_gpu_gb')*3+240)/(v('hbm_per_gpu_gb')*3+64)):.2f}x.")
    P(f"- Fleet with 50% of capacity on agent/API traffic: ~{1.0/(0.5/g_h_path + 0.5/g1):.2f}x DRAM GB per conversation.")
    P(f"- Latent: per-layer only (all-layer killed); compute-bound at {lat_rows[1]['n_a']/A['n_a']:.2f}x active sessions; it is prior art (MHA2MLA, TransMLA) or moot for MLA-native models, so it is not counted as the diet's step.")
    P(f"- **On FINAL_CONCEPTS' scale this is S = 1 (<= 1.3x in wafer terms; 1.25-1.45x in DRAM GB on human-chat pools).** EV 2 x 3 x 5 = 30 -> 1 x 3 x 5 = 15.")
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
