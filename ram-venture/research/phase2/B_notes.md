# Phase 2 — Branch B notes: architecture and systems ("make existing RAM go 2–10x further")

**Agent:** `B` · **As of:** 2026-11-01 · **Cards:** `research/phase2/B.json` (15 cards, B-01 to B-15) · **Sources:** `research/sources/B.jsonl` (51 entries) · **Assumptions:** `research/assumptions/B.md`

> **Method and limits, stated up front.**
> - **No web search.** The shared WebSearch budget for this turn (200 calls across all agents) was used up before my first query. All six queries I sent came back "not performed".
> - **WebFetch was blocked too.** It could not resolve arxiv.org, asteralabs.com or zeropoint-tech.com because they are not on the network allowlist. I stopped probing other hosts, as the tool instructed.
> - **Primary sources came from GitHub.** Public GitHub repositories could be cloned through the git proxy, so my primary evidence is the documents I opened there:
>   - the mainline Linux CXL maturity map, IAA and zswap docs (HEAD 2026-10-31)
>   - vLLM, NVIDIA Dynamo, LMCache, Mooncake and SGLang docs (HEAD 2026-11-01)
>   - Samsung SMDK and SK hynix HMSDK
>   - KTransformers
>   - the DeepSeek-V3 and Llama-3.1 model configs
>   - the Pond (ASPLOS '23) artifact repo
>   - the PrIM/UPMEM benchmarks
>   - IBM aihwkit
>   - CHIPS Alliance AIB
> - **Prices are cross-referenced.** The DDR4/DDR5/HBM/NAND prices come from Phase-1 agents' logged search snippets and are marked CROSS-REFERENCE.
> - **Vendor status is unverified.** Facts about the status of specific CXL, KV-cache, PIM and compression vendors are from my training knowledge (to about mid-2026). They are tagged **[UNVERIFIED-T]** and carry no URL. Phase 3 should re-verify them when search is available. The list: Astera Leo/Azure, Marvell Structera, Montage, Microchip SMC 2000, Samsung CMM-D/B, Micron CZ120/122, SK hynix CMM, SMART/Penguin, Liqid, GigaIO, XConn, Panmnesia, Unifabrix, Enfabrica→NVIDIA, ZeroPoint, Pliops, VAST, Hammerspace, NVIDIA ICMS/BlueField-4, d-Matrix, Mythic, EnCharge, Sagence, GSI, UPMEM, Eliyan and SanDisk HBF.
> - **Effective research volume:** 6 failed searches, 4 failed fetches, 15 repos cloned, and about 30 primary documents read inside them.

---

## 0. Bottom line for Branch B

1. **The software layer that makes RAM "go further" is free, upstream and moving fast. Hardware for a small company is mostly commodity integration.** Three examples:
   - KV-cache tiering to host DRAM, SSD and CXL ships in vLLM (`OffloadingConnector`), Dynamo KVBM, LMCache, Mooncake Store and SGLang HiCache. LMCache and Mooncake already allocate KV on CXL `/dev/dax`.
   - CXL tiering (weighted interleave, DAMON migration) is in mainline Linux v6.9 and v6.11.
   - Hardware memory compression (Intel IAA under zswap) is already in Xeons.
2. **CXL pooling and sharing (the "CXL 3.x" story) is not ready at the OS level in late 2026.** In mainline Linux (2026-10-31), Dynamic Capacity Devices, multi-host sharing and fabrics/G-FAM are all **[0] "known gap"** ([Linux maturity map](https://github.com/torvalds/linux/blob/master/Documentation/driver-api/cxl/maturity-map.rst)) [VERIFIED]. Single-host Type-3 expansion is "[2] stabilizing". Any pooling appliance is therefore a 2028+ product and a hyperscaler-only buyer. It is killed for us (B-07).
3. **The DDR4-behind-CXL reuse idea flips this cycle.** DDR4 is now as dear as DDR5 or dearer:
   - DDR4 8Gb spot was $21–44 in Aug 2026, about $21–44/GB.
   - DDR4 is price-inverted against DDR5 in some channels (Barclays, Oct 2026).

   At small-vendor card cost (~$2.3/GB), "sell the DDR4 and buy DDR5" beats reuse in the 2023 trough, in 4Q26 and in the 2028–29 glut. Reuse wins only at hyperscaler scale (§2.4). That kills B-01 for a small company.
4. **KV-cache economics favour flash over DRAM for warm KV, and DRAM only for hot KV.**
   - Holding Llama-70B FP8 KV in DDR5 at 4Q26 prices pays only if a prefix is reused at least once every ~1.35 h.
   - On NVMe it pays at once every ~78 h.
   - Either beats recompute by 20–100x on latency for long contexts (§2.3).

   The flash tier is where NVIDIA (KVBM + GDS, BlueField-4), WEKA, VAST and Pliops already compete, so it is crowded (B-03). A DRAM KV node is commodity (B-02).
5. **The most founder-compatible hardware idea uses DRAM in place of HBM, not more DRAM per se.**
   - **What:** an on-prem MoE inference appliance (B-05). It holds about 1 TB of open-model weights in about $20k of DDR5 instead of about $240k of HBM-bearing GPUs.
   - **Software:** KTransformers/SGLang.
   - **Who buys:** regulated buyers who cannot use cloud APIs.
   - **Glut:** it survives, because DRAM gets cheaper.
   - **Catch:** it is an integration and service business with thin hardware margin.

## 1. What I tried and what I read

| # | Action | Result |
|---|---|---|
| 1–6 | WebSearch: Astera Leo/Azure; Marvell Structera X DDR4/compression; CXL 4.0/3.1 switch status; NVIDIA ICMS/BlueField-4 KV; ZeroPoint 2026; Pliops 2026 | **Not performed**: shared per-turn budget exhausted |
| 7–10 | WebFetch: arXiv Pond 2203.00241; arXiv TPP 2206.02878; asteralabs.com Leo page; zeropoint-tech.com | **DNS-blocked** (not in session allowlist). Proxy status also shows 403s for trendforce.com, sec.gov, investors.micron.com, gsitechnology.com |
| 11 | Mined `sources/*.jsonl` from p1-market, p1-micron, p1-fabs, p1-backend, A1, A2 | 24 price/Optane/Everspin/Micron URLs reused as CROSS-REFERENCE (attribution checked by script) |
| 12–26 | `git clone --depth 1 --filter=blob:limit` of 15 public repos | All succeeded. See the table below |
| 27–60 | Read about 30 docs inside the repos (`git show HEAD:<path>`, `git grep`) | Evidence in §3 |

| Repo (HEAD date) | What I took from it |
|---|---|
| torvalds/linux (2026-10-31) | CXL maturity map: DCD [0], multi-host sharing [0], fabrics [0], switch enumeration [2], PMEM GPF [3], Type-2 accelerator memory [0]. IAA doc: hardware DEFLATE (`deflate-iaa`, 4 KiB history window) as the zswap compressor. zswap doc |
| vllm-project/vllm (2026-11-01) | `OffloadingConnector`: CPU is the primary tier, and secondary tiers are staged through the CPU, so host DRAM is mandatory |
| ai-dynamo/dynamo (2026-11-01) | KVBM tiers GPU↔CPU↔Disk↔Remote with GDS/NIXL. LMCache, FlexKV and HiCache are alternative backends. WEKA–NVIDIA KV storage (SC25, 2025-11-20) |
| LMCache/LMCache (2026-11-01) | Device-DAX backend for CXL memory. PyTorch Foundation and Tensormesh (Oct 2025). CoreWeave/Cohere (Nov 2025). MP architecture (Apr 2026). 3FS backend |
| kvcache-ai/Mooncake (2026-11-01) | Kimi handles "75% more requests while adhering to SLOs". Store has CXL-aware allocation. Integrated with vLLM (May 2026) and TensorRT-LLM (Oct 2026). FAST '25 paper |
| kvcache-ai/ktransformers (2026-10-28) | Kimi-K2.5 needs ≥600 GB RAM plus 2x4090. DeepSeek-V4-Flash needs ≥200 GB RAM plus one RTX 5090. GLM-5.x and MiniMax-M3 had day-0 support in 2026 |
| OpenMPDK/SMDK (2024-12-09) | Samsung CMM software v2.2. No commits since Dec 2024, a weak signal that Samsung's open CXL software push has slowed [ESTIMATE] |
| skhynix/hmsdk (2026-03) | HMSDK v4.0 (2025-11-03). Weighted interleave landed in Linux v6.9 and DAMON tiering in v6.11 |
| vtess/Pond (2024-10) | Pond (ASPLOS '23, Microsoft Azure). Emulation scripts only |
| meta-llama/llama-models; deepseek-ai/DeepSeek-V3 | Architecture parameters for the KV math |
| sgl-project/sglang | HiCache: the benefit scales with reusable tokens relative to GPU memory |
| CMU-SAFARI/prim-benchmarks (2026-06) | UPMEM PIM characterization. The repo is still active |
| IBM/aihwkit (2026-10) | Analog in-memory compute toolkit, still "beta" |
| chipsalliance/aib-phy-hardware (2024-09) | Open die-to-die PHY RTL |

## 2. Key numbers (computed, not guessed)

The script below is a verbatim copy of `b_models.py` from my scratchpad. It runs with `python3` and exits 0. Its inputs are logged in `assumptions/B.md`. It lives here because B owns only these files; Phase 3/4 can promote it to `models/branch_b_kv_cxl.py`.

### 2.0 Script
```python
#!/usr/bin/env python3
"""Branch B back-of-envelope models (agent B, 2026-11-01).

Every input is either from a model config read from a primary repo, a price
logged in research/sources/*.jsonl, or an explicit [ESTIMATE] logged in
research/assumptions/B.md. Run: python3 b_models.py
"""

GiB = 1024 ** 3
MB = 1e6

# ---------------------------------------------------------------- 1. KV size per token
# Configs read from github.com/meta-llama/llama-models (models/sku_list.py) and
# github.com/deepseek-ai/DeepSeek-V3 (inference/configs/config_671B.json).
MODELS = {
    # name: (n_layers, n_kv_heads, head_dim, attention type)
    "Llama-3.1-8B": (32, 8, 4096 // 32, "GQA"),
    "Llama-3.1-70B": (80, 8, 8192 // 64, "GQA"),
    "Llama-3.1-405B": (126, 8, 16384 // 128, "GQA"),
}
DSV3 = dict(n_layers=61, kv_lora_rank=512, qk_rope_head_dim=64)  # MLA latent cache


def kv_bytes_per_token_gqa(n_layers, n_kv_heads, head_dim, bytes_per_elem=2):
    return 2 * n_layers * n_kv_heads * head_dim * bytes_per_elem  # K and V


def kv_bytes_per_token_mla(n_layers, kv_lora_rank, qk_rope_head_dim, bytes_per_elem=2):
    return n_layers * (kv_lora_rank + qk_rope_head_dim) * bytes_per_elem


kv = {}
for name, (L, H, D, _) in MODELS.items():
    kv[name] = kv_bytes_per_token_gqa(L, H, D)
kv["DeepSeek-V3 (MLA)"] = kv_bytes_per_token_mla(**DSV3)

print("== 1. KV cache per token (BF16; FP8 halves these) ==")
for name, b in kv.items():
    print(f"{name:22s} {b/1024:8.1f} KiB/token | 32k ctx {b*32768/GiB:6.1f} GiB | "
          f"128k ctx {b*131072/GiB:6.1f} GiB | 1M tokens {b*1e6/1e9:7.1f} GB")

# ---------------------------------------------------------------- 2. $/GB by tier
# HBM3E ~$1.50/Gb = $12/GB and HBM4 2027 ask ~$4.5-4.9/Gb (sources/p1-market.jsonl,
# sammyfans 2026-10-02) -- but HBM is only purchasable inside a GPU.
TIERS = {
    # tier: (low $/GB, high $/GB, note)
    "GPU HBM (bought as H200/B200)": (180.0, 250.0, "[ESTIMATE] GPU price / HBM GB; e.g. ~$30k / 141GB"),
    "HBM3E die-level (contract)": (12.0, 12.0, "$1.50/Gb reported 2026"),
    "DDR5 RDIMM (4Q26)": (20.0, 32.0, "[ESTIMATE] 64GB RDIMM >$900 1Q26 x 2Q-4Q26 hikes; retail ~$32/GB Aug-26"),
    "DDR5 RDIMM (2028-29 glut, -60%)": (8.0, 12.8, "A-05 glut"),
    "Enterprise TLC NVMe (4Q26)": (0.30, 0.60, "[ESTIMATE] NAND contract +55-75%/qtr 1H26"),
}
print("\n== 2. $/GB by tier ==")
for t, (lo, hi, note) in TIERS.items():
    print(f"{t:34s} ${lo:7.2f}-{hi:7.2f}/GB   {note}")

# ---------------------------------------------------------------- 3. Cache-vs-recompute break-even
# Prefill cost for a dense 70B model: ~2*P FLOPs/token.
P = 70e9
flops_per_tok = 2 * P
h100_bf16_dense = 989e12        # NVIDIA H100 SXM dense BF16 peak [UNVERIFIED datasheet figure]
mfu = 0.45                      # [ESTIMATE]
gpu_hour = 2.5                  # [ESTIMATE] $/H100-hour neocloud 2026
prefill_tps = h100_bf16_dense * mfu / flops_per_tok
recompute_cost_per_Mtok = gpu_hour / (prefill_tps * 3600 / 1e6)
kv70 = kv["Llama-3.1-70B"] / 2   # FP8 KV, common in production [ESTIMATE]
GB_per_Mtok = kv70 * 1e6 / 1e9
amort_hours = 3 * 8760          # 3-year straight-line [ESTIMATE]
print("\n== 3. Llama-3.1-70B, FP8 KV: hold-in-tier vs recompute ==")
print(f"prefill throughput ~{prefill_tps:,.0f} tok/s per H100; recompute ${recompute_cost_per_Mtok:.3f} per 1M tokens")
print(f"KV for 1M tokens = {GB_per_Mtok:.0f} GB")
for t in ["GPU HBM (bought as H200/B200)", "DDR5 RDIMM (4Q26)", "DDR5 RDIMM (2028-29 glut, -60%)",
          "Enterprise TLC NVMe (4Q26)"]:
    lo, hi, _ = TIERS[t]
    mid = (lo + hi) / 2
    hold_per_hour = mid * GB_per_Mtok / amort_hours
    breakeven_h = recompute_cost_per_Mtok / hold_per_hour
    print(f"{t:34s} hold ${hold_per_hour:8.4f}/h per 1M tok -> caching pays if reused at least once every {breakeven_h:8.2f} h")

# Latency side: reload 128k-token context vs recompute.
ctx = 131072
bytes_ctx = kv70 * ctx
for name, bw in [("Gen5 x4 NVMe SSD", 12e9), ("CXL x16 Gen5 expander", 50e9), ("400G RDMA", 45e9), ("Host DDR5 via PCIe Gen5 x16", 55e9)]:
    print(f"reload 128k ctx ({bytes_ctx/GiB:.1f} GiB) over {name:26s}: {bytes_ctx/bw:5.2f} s  vs recompute on 1xH100 {ctx/prefill_tps:5.1f} s")

# ---------------------------------------------------------------- 4. DDR4 second-life CXL: sell vs reuse
# Per GB of capacity the owner needs. Reuse wins iff card$/GB + DDR4 resale$/GB < new DDR5$/GB.
print("\n== 4. DDR4 reuse behind CXL vs sell DDR4 + buy DDR5 ($/GB) ==")
card_cost = 1200.0      # [ESTIMATE] CXL AIC w/o DRAM (controller + PCB + firmware) at low volume
card_gb = 512.0          # 8 x 64GB RDIMM
card_per_gb = card_cost / card_gb
scen = {
    "2023 trough": dict(ddr4_resale=1.0, ddr5_new=3.0),     # DDR4 8Gb $1.30 Sep-2023 (sources)
    "4Q26 shortage": dict(ddr4_resale=25.0, ddr5_new=26.0), # DDR4 8Gb spot $21-44 Aug-26; DDR5 est.
    "2028-29 glut": dict(ddr4_resale=12.0, ddr5_new=10.4),  # DDR5 -60%; DDR4 sticky (EOL supply) [ESTIMATE]
}
hyperscaler_card_per_gb = 250.0 / card_gb   # [ESTIMATE] in-house controller board at 100k+ volume
for who, cpg in [("small vendor", card_per_gb), ("hyperscaler", hyperscaler_card_per_gb)]:
    for s, v in scen.items():
        resale = v["ddr4_resale"] if who == "small vendor" else v["ddr4_resale"] * 0.5  # dumping millions halves realised resale [ESTIMATE]
        reuse = cpg + resale
        margin = v["ddr5_new"] - reuse
        print(f"{who:12s} {s:14s} card ${cpg:4.2f}/GB + DDR4 opp. cost ${resale:5.2f} = ${reuse:6.2f}/GB vs new DDR5 "
              f"${v['ddr5_new']:6.2f}/GB -> advantage ${margin:6.2f}/GB ({'REUSE' if margin > 0 else 'SELL DDR4'})")

# ---------------------------------------------------------------- 5. DRAM-heavy MoE appliance roofline
print("\n== 5. On-prem MoE appliance: DRAM instead of HBM ==")
ch, mts = 12, 6400                       # 12-ch DDR5-6400 per EPYC 9005 socket [UNVERIFIED spec]
bw_socket = ch * mts * 1e6 * 8           # bytes/s
active_params = 32e9                     # Kimi-K2-class MoE, ~32B active [UNVERIFIED]
bytes_per_param = 0.5                    # INT4 experts (ktransformers native INT4)
tok_s = bw_socket * 0.6 / (active_params * bytes_per_param)   # 60% achievable BW [ESTIMATE]
print(f"socket BW {bw_socket/1e9:.0f} GB/s -> single-stream decode roofline ~{tok_s:.0f} tok/s (2 sockets ~{2*tok_s:.0f} if NUMA-aware)")
dram_gb = 768
for label, p in [("4Q26", 26.0), ("glut", 10.4)]:
    dram_cost = dram_gb * p
    base = 18000 + 2 * 9000              # [ESTIMATE] 2S EPYC platform + 2 workstation GPUs
    bom = base + dram_cost
    price = bom / (1 - 0.22)             # 22% hardware GM target
    print(f"{label}: DRAM ${dram_cost:,.0f} + platform/GPUs ${base:,.0f} = BOM ${bom:,.0f}; list @22% GM ${price:,.0f}")
hbm_route = 8 * 30000                    # [ESTIMATE] 8 x H200-class to hold ~1TB of weights in HBM
print(f"HBM route to hold ~1TB of INT4/FP8 weights: ~${hbm_route:,.0f} in GPUs alone")
```

### Output (2026-11-01)
```
== 1. KV cache per token (BF16; FP8 halves these) ==
Llama-3.1-8B              128.0 KiB/token | 32k ctx    4.0 GiB | 128k ctx   16.0 GiB | 1M tokens   131.1 GB
Llama-3.1-70B             320.0 KiB/token | 32k ctx   10.0 GiB | 128k ctx   40.0 GiB | 1M tokens   327.7 GB
Llama-3.1-405B            504.0 KiB/token | 32k ctx   15.8 GiB | 128k ctx   63.0 GiB | 1M tokens   516.1 GB
DeepSeek-V3 (MLA)          68.6 KiB/token | 32k ctx    2.1 GiB | 128k ctx    8.6 GiB | 1M tokens    70.3 GB

== 2. $/GB by tier ==
GPU HBM (bought as H200/B200)      $ 180.00- 250.00/GB   [ESTIMATE] GPU price / HBM GB; e.g. ~$30k / 141GB
HBM3E die-level (contract)         $  12.00-  12.00/GB   $1.50/Gb reported 2026
DDR5 RDIMM (4Q26)                  $  20.00-  32.00/GB   [ESTIMATE] 64GB RDIMM >$900 1Q26 x 2Q-4Q26 hikes; retail ~$32/GB Aug-26
DDR5 RDIMM (2028-29 glut, -60%)    $   8.00-  12.80/GB   A-05 glut
Enterprise TLC NVMe (4Q26)         $   0.30-   0.60/GB   [ESTIMATE] NAND contract +55-75%/qtr 1H26

== 3. Llama-3.1-70B, FP8 KV: hold-in-tier vs recompute ==
prefill throughput ~3,179 tok/s per H100; recompute $0.218 per 1M tokens
KV for 1M tokens = 164 GB
GPU HBM (bought as H200/B200)      hold $  1.3404/h per 1M tok -> caching pays if reused at least once every     0.16 h
DDR5 RDIMM (4Q26)                  hold $  0.1621/h per 1M tok -> caching pays if reused at least once every     1.35 h
DDR5 RDIMM (2028-29 glut, -60%)    hold $  0.0648/h per 1M tok -> caching pays if reused at least once every     3.37 h
Enterprise TLC NVMe (4Q26)         hold $  0.0028/h per 1M tok -> caching pays if reused at least once every    77.87 h
reload 128k ctx (20.0 GiB) over Gen5 x4 NVMe SSD          :  1.79 s  vs recompute on 1xH100  41.2 s
reload 128k ctx (20.0 GiB) over CXL x16 Gen5 expander     :  0.43 s  vs recompute on 1xH100  41.2 s
reload 128k ctx (20.0 GiB) over 400G RDMA                 :  0.48 s  vs recompute on 1xH100  41.2 s
reload 128k ctx (20.0 GiB) over Host DDR5 via PCIe Gen5 x16:  0.39 s  vs recompute on 1xH100  41.2 s

== 4. DDR4 reuse behind CXL vs sell DDR4 + buy DDR5 ($/GB) ==
small vendor 2023 trough    card $2.34/GB + DDR4 opp. cost $ 1.00 = $  3.34/GB vs new DDR5 $  3.00/GB -> advantage $ -0.34/GB (SELL DDR4)
small vendor 4Q26 shortage  card $2.34/GB + DDR4 opp. cost $25.00 = $ 27.34/GB vs new DDR5 $ 26.00/GB -> advantage $ -1.34/GB (SELL DDR4)
small vendor 2028-29 glut   card $2.34/GB + DDR4 opp. cost $12.00 = $ 14.34/GB vs new DDR5 $ 10.40/GB -> advantage $ -3.94/GB (SELL DDR4)
hyperscaler  2023 trough    card $0.49/GB + DDR4 opp. cost $ 0.50 = $  0.99/GB vs new DDR5 $  3.00/GB -> advantage $  2.01/GB (REUSE)
hyperscaler  4Q26 shortage  card $0.49/GB + DDR4 opp. cost $12.50 = $ 12.99/GB vs new DDR5 $ 26.00/GB -> advantage $ 13.01/GB (REUSE)
hyperscaler  2028-29 glut   card $0.49/GB + DDR4 opp. cost $ 6.00 = $  6.49/GB vs new DDR5 $ 10.40/GB -> advantage $  3.91/GB (REUSE)

== 5. On-prem MoE appliance: DRAM instead of HBM ==
socket BW 614 GB/s -> single-stream decode roofline ~23 tok/s (2 sockets ~46 if NUMA-aware)
4Q26: DRAM $19,968 + platform/GPUs $36,000 = BOM $55,968; list @22% GM $71,754
glut: DRAM $7,987 + platform/GPUs $36,000 = BOM $43,987; list @22% GM $56,394
HBM route to hold ~1TB of INT4/FP8 weights: ~$240,000 in GPUs alone
```

### 2.1 KV cache per token (model configs [VERIFIED] from the repos; arithmetic [ESTIMATE])
- **Formula.** GQA: `2 × layers × kv_heads × head_dim × bytes`. MLA: `layers × (kv_lora_rank + rope_dim) × bytes`.
- **Llama-3.1-8B:** 128 KiB/token (BF16), so 16 GiB at a 128k context.
- **Llama-3.1-70B:** 320 KiB/token, so 40 GiB at 128k. 1M tokens take 328 GB in BF16 and 164 GB in FP8.
- **Llama-3.1-405B:** 504 KiB/token, so 63 GiB at 128k.
- **DeepSeek-V3 (MLA):** 68.6 KiB/token, so 8.6 GiB at 128k. That is **4.7x smaller than Llama-70B**.

**Implication:** architecture changes (MLA, FP8/FP4 KV, KV compression) shrink KV demand per token faster than hardware vendors like to admit. Any product built on "KV needs more RAM" has a moving target.

### 2.2 $/GB by tier (4Q26)

| Tier | $/GB | Basis |
|---|---|---|
| GPU HBM, bought inside a GPU | ~$180–250 | [ESTIMATE] |
| HBM3E, die level | ~$12 (~$1.50/Gb) | [REPORTED], cross-ref |
| HBM4 2027 asks | ~$36–39 | [REPORTED] |
| DDR5 RDIMM | ~$20–32 | [ESTIMATE]: Counterpoint >$900/64GB in 1Q26 compounded by the 2Q–4Q hikes; ServNet street price ~$32/GB in Aug 2026 |
| DDR5 RDIMM in the glut | ~$8–13 | |
| Enterprise TLC NVMe | ~$0.30–0.60 | [ESTIMATE] |

One irony: at die level, HBM3E (~$12/GB) is now cheaper per GB than DDR5 spot (~$27/GB). Samsung said conventional DRAM was more profitable than HBM in 1Q26 (p1-market). Nobody small can buy HBM dies, though.

### 2.3 Cache-vs-recompute (Llama-3.1-70B, FP8 KV, one H100 at 45% MFU, $2.50/h)
- **Recompute cost and speed:** $0.218 per 1M prefill tokens, at about 3,180 tok/s.
- **Break-even reuse interval.** Holding KV beats recomputing it if the prefix is reused at least once every:

  | Tier | Break-even interval |
  |---|---|
  | HBM-in-GPU | 0.16 h (~10 min) |
  | DDR5, 4Q26 | 1.35 h |
  | DDR5, glut | 3.4 h |
  | NVMe | 78 h |

- **Latency:** reloading a 128k context (20 GiB FP8) takes 1.8 s from one Gen5 SSD and 0.4–0.5 s over CXL, 400G RDMA or host DDR5. Recompute takes about 41 s.

**Takeaway:** hot KV (minutes) belongs in DRAM, and warm KV (hours to days) belongs on flash. DRAM-heavy KV appliances are the wrong product while DRAM is at 4Q26 prices.

### 2.4 DDR4 second life: sell vs reuse

Reuse is cheaper only if `card $/GB + DDR4 resale $/GB < new DDR5 $/GB`.

| Owner | 2023 trough | 4Q26 | 2028–29 glut |
|---|---|---|---|
| Small vendor's customer (card ~$2.34/GB, full DDR4 resale) | −$0.34/GB → **sell** | −$1.34/GB → **sell** | −$3.94/GB → **sell** |
| Hyperscaler (card ~$0.49/GB, realizes ~50% of DDR4 resale) | +$2.01/GB → reuse | +$13.01/GB → reuse | +$3.91/GB → reuse |

The Microsoft/Meta DDR4-reuse logic (2022–23) was built when DDR4 was worth ~$1/GB. The 2025–26 DDR4 end-of-life squeeze made used DDR4 a liquid, high-value asset, which turns it into a **brokerage** opportunity (branch C), not a CXL product opportunity.

The one exception is an operator who cannot get DDR5 allocation at any price (TrendForce, 2026-01: supply goes to strategic OEMs first). That is a supply-security sale, not a cost sale.

### 2.5 On-prem MoE appliance (B-05)
- **Decode speed:** a 12-channel DDR5-6400 socket gives 614 GB/s peak. At 60% efficiency and 16 GB of weights read per token (32B active parameters, INT4), single-stream decode tops out around **23 tok/s per socket**, or about 46 tok/s with NUMA-aware placement across two sockets.
- **Cost:**

  | | DRAM (768 GB) | Total BOM | List price at 22% hardware GM |
  |---|---|---|---|
  | 4Q26 | $20k | ~$56k | ~$72k |
  | Glut | $8k | ~$44k | ~$56k |

  The alternative is holding 1 TB of weights in HBM, which takes about $240k of GPUs.

## 3. Evidence behind each card

| Card | Primary evidence (opened) | Cross-ref / [UNVERIFIED-T] | Verdict |
|---|---|---|---|
| B-01 DDR4 Second-Life CXL | Linux maturity map; Pond repo; HMSDK upstream tiering | DDR4 spot $21–44 (TrendForce, DRAMeXchange); Barclays DDR4>DDR5; DDR4 $1.30 in Sep 2023. Marvell Structera X, Astera Leo, SMART AICs [UNVERIFIED-T] | **Kill for us.** Computed negative in all scenarios at small scale |
| B-02 KV Pool Node | Mooncake README/Store guide (CXL alloc, +75% requests); LMCache DAX; vLLM offloading; Dynamo KVBM; model configs | Counterpoint RDIMM price. NVIDIA ICMS, Penguin, Pliops [UNVERIFIED-T] | Commodity; marginal |
| B-03 Flash KV Accelerator | Dynamo KVBM (GDS disk tier); LMCache (3FS backend); WEKA–NVIDIA SC25 headline | NAND flat Oct 2026; NAND surplus 2H27. Pliops/VAST/Hammerspace [UNVERIFIED-T] | Crowded; NVIDIA absorbing |
| B-04 Compressed CXL Expander | Linux IAA + zswap docs; maturity map | ZeroPoint, Marvell inline LZ4, Meta TMO [UNVERIFIED-T] | Kill: commoditized, glut-fragile |
| B-05 On-prem MoE Box | KTransformers README and tutorials (RAM needs); DeepSeek-V3 config | HBM pricing; RDIMM pricing. DGX Station, Mac Studio [UNVERIFIED-T] | **Most founder-doable in B** |
| B-06 TB-Class CXL Node | HMSDK; SMDK; maturity map | OEM CXL platforms [UNVERIFIED-T] | VAR margins; weak pain point |
| B-07 Rack-Scale Pooling | Linux maturity map (DCD/sharing/fabrics [0]); Pond | Liqid, GigaIO, XConn, Panmnesia, Unifabrix [UNVERIFIED-T] | **Kill:** OS not ready; hyperscaler-only |
| B-08 Persistent CXL Log Card | Maturity map (PMEM GPF [3]) | IBM FCM5 Everspin MRAM; Everspin 1Gb at $102.60 (~$821/GB); Optane $559M impairment. SMART NV-CMM [UNVERIFIED-T] | Niche; not founder |
| B-09 Optane Revival | — | Intel 10-Q; SNIA >$7B losses; Micron 3D XPoint exit; SanDisk 3D Matrix Memory | **Kill** (scale economics, glut) |
| B-10 LPDDR HBM-lite Chiplet | CHIPS Alliance AIB RTL | HBM 22% of wafer starts for 9% of bits; HBM 3x area per bit; HBM4 asks; LPDDR +70–90%. Eliyan, Synopsys, Cadence [UNVERIFIED-T] | Possible; T3; not us |
| B-11 HBF Weight-Store | — | NAND flat/surplus; SanDisk investor day. HBF specifics [UNVERIFIED-T] | Watch only |
| B-12 PIM DIMM Servers | PrIM (UPMEM) repo and IEEE Access link | UPMEM company status, Samsung AiM/HBM-PIM [UNVERIFIED-T] | **Kill:** research-grade demand |
| B-13 Analog CIM Edge Module | IBM aihwkit ("beta") | LPDDR price hikes. EnCharge, Mythic, Sagence [UNVERIFIED-T] | Marginal integrator play |
| B-14 TrustedCXL (U.S. provenance) | Maturity map | Micron Manassas DDR4 ramp; Everspin–Amentum $40M. Microchip SMC 2000 [UNVERIFIED-T] | Marginal; SBIR-led only |
| B-15 Memory-Fabric SuperNIC | Mooncake (standard-RDMA alternative); vLLM; Llama config | Enfabrica → NVIDIA (Sep 2025) [UNVERIFIED-T] | **Kill:** acquired away |

## 4. Post-mortems and negative findings worth carrying forward

1. **Optane (B-09).** Intel took a $559M impairment in Q2-22 and lost more than $7B cumulatively. Micron left 3D XPoint in Mar 2021 citing "insufficient market validation" and pivoted to CXL. The lesson is that **a DRAM substitute needs DRAM-scale volume to win on $/GB, and each glut resets the target.** The 2026 spike does not change that; SanDisk's 3D Matrix Memory is the next test, not ours.
2. **CXL pooling is a 2028+ software story.** The kernel has no DCD extent handling, no DC-backed DAX regions and no multi-host coherent sharing as of 2026-10-31. Pond's own Azure result showed single-digit-percent fleet DRAM savings [UNVERIFIED-T]. The pooling-startup wave (Enfabrica acqui-hired by NVIDIA, Unifabrix status unknown) is consolidating into large vendors [UNVERIFIED-T].
3. **DDR4 reuse flipped sign.** See §2.4. The DDR4 end-of-life squeeze made used DDR4 more valuable to sell than to reuse, except at hyperscaler scale.
4. **Compression is being commoditized from both sides:** CPU IAA plus zswap, upstream, and merchant CXL controllers with inline LZ4 [UNVERIFIED-T]. FP8/INT4 tensors barely compress, so the hottest "need more RAM" data is the least compressible.
5. **KV-cache tiering software is open source and vendor-neutral.** Its developers are well capitalized: Tensormesh behind LMCache, Moonshot behind Mooncake, and NVIDIA's Dynamo. Hardware differentiation in KV tiering lives only in flash-controller silicon (Pliops) or NVIDIA's DPU, and neither is open to a small entrant.
6. **Samsung's SMDK repo has been idle since Dec 2024.** Read alongside HMSDK's upstreaming, the vendor SDKs are being replaced by mainline Linux. A software-only CXL middleware company has little room left, which is a note for branch D.
7. **Architecture shrinks KV demand.** MLA (DeepSeek) is 4.7x smaller per token than GQA Llama-70B, and FP8 KV halves it again. A product sized to today's KV-per-token is exposed to the next model generation.

## 5. Ideas considered but NOT carded (one-line reason each)

- **In-server CXL retrofit kit for HGX GPU servers (host-memory KV tier).** It is a variant of B-02. HGX servers have few spare Gen5 slots, since NICs and DPUs take them, and OEMs own the BOM.
- **CXL-attached STT-MRAM capacity tier.** MRAM is about $821/GB against DDR5 at about $26/GB (32x); the persistence case is covered by B-08.
- **CXL-attached NAND "memory-semantic SSD" (Samsung CMM-H, Kioxia XL-Flash).** Only memory makers can build it, and it is covered by B-03 and B-08.
- **SOCAMM2 / LPDDR5X module assembly in the U.S.** It is module assembly (branch C), and bare LPDDR5X packages are allocated to NVIDIA-tier buyers.
- **CXL Type-3 FPGA dev kits for researchers.** The market is tiny, and Intel/Altera, AMD and BittWare already sell R-tile and CPM5 kits [UNVERIFIED-T].
- **GPU-side CXL memory expansion (Panmnesia CXL-GPU).** NVIDIA uses NVLink-C2C and LPDDR5X (Grace) and does not expose CXL.mem on GPUs. The Linux Type-2 accelerator memory support score is [0].
- **RAM-as-a-service: renting CXL-expanded large-memory bare metal.** It is mostly a hosting/software business (branch D lists it), and DRAM capex at 4Q26 prices is brutal.
- **KV-cache SaaS, tiering daemon, or memory-aware scheduler.** Pure software, so it belongs to branch D.
- **Memory price/allocation data product.** Pure data/software, so it belongs to branch D (Phase 1 already found that Mobius Materials' report is content marketing).
- **Wafer-scale SRAM "RAM" (Cerebras-style).** Device and wafer-scale, so it belongs to branch A. It is also T4.
- **Building DDR5 RDIMMs from recovered dies.** That is the branch C recert/brokerage path. Per §2.4, the profitable form of B-01 is brokerage, not a CXL product.
- **Hardware dedup engine for VM memory.** Hypervisor KSM/TPS already does this in software. Security concerns (side channels) killed cross-VM page sharing in public clouds [UNVERIFIED-T].
- **Selling into Azure/Meta CXL programs as a contract designer.** Those buyers work with Marvell, Astera and Montage directly, so there is no room for a newcomer.

## 6. Ranking within branch B (for Phase 3 input; separate scores, not blended)

| Card | POSSIBLE | PROFITABLE | DOABLE BY FOUNDER | Glut |
|---|---|---|---|---|
| B-05 On-prem MoE Box | yes | marginal (yes with subscription) | **yes** | yes |
| B-02 KV Pool Node | yes | marginal | marginal | partially |
| B-14 TrustedCXL | yes | marginal | marginal (SBIR-led) | yes |
| B-13 Analog CIM Edge | yes | marginal | marginal | yes |
| B-06 TB-Class CXL Node | yes | marginal | marginal | partially |
| B-03 Flash KV Accelerator | yes | marginal | no | yes |
| B-08 Persistent CXL Log | yes | marginal | no | yes |
| B-10 LPDDR HBM-lite Chiplet | yes | marginal | no | partially |
| B-01 DDR4 Second-Life CXL | yes | **no** (computed) | no | no |
| B-04 Compressed CXL | yes | no | no | no |
| B-07 Rack-Scale Pooling | marginal | no | no | no |
| B-11 HBF Module | marginal | no | no | partially |
| B-12 PIM DIMM Servers | yes | no | no | partially |
| B-15 Memory-Fabric SuperNIC | yes | no | no | partially |
| B-09 Optane Revival | yes | no | no | no |

**Cheapest kill experiments (< $10k, < 30 days) for the top three:**
- **B-05:**
  - Rent a 2-socket EPYC box with 768 GB+ from a bare-metal provider for one week (about $300–600).
  - Run KTransformers with Kimi-K2.5 or DeepSeek-V4-Flash.
  - Measure tokens/s at 1, 4 and 8 concurrent users against the 23–46 tok/s roofline.
  - Put the numbers in front of 10 compliance-bound firms (law, healthcare, defense subcontractors) and ask them to commit a $5k deposit.
  - **Kill if** throughput is below 10 tok/s at 4 users, or there are fewer than 2 deposits.
- **B-02:**
  - Replay the public Mooncake FAST '25 traces through LMCache with a CPU tier sized from 128 GB to 2 TB.
  - Measure hit-rate against capacity.
  - **Kill if** the hit-rate curve flattens below about 512 GB per GPU server. In that case a separate node adds nothing over in-server DRAM.
- **B-14:**
  - Email Micron's Manassas defense sales team and two DoD HPCMP centers.
  - Ask whether Manassas DDR4 can be bought for a CXL card, and whether any program would pay a provenance premium.
  - **Kill if** there is no die/module access, or no buyer names a program.
