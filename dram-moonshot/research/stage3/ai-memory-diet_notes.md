# AI MEMORY DIET: stage 3 dossier research notes

Agent `dos-ai-memory-diet`, 2026-11-02. Concept rank 10 (EV 30), system/architecture. The model is `models/ai-memory-diet.py` and its output is `research/stage3/ai-memory-diet_model_output.md`. Sources are logged in `research/sources/dos-ai-memory-diet.jsonl` and assumptions in `research/assumptions/dos-ai-memory-diet.md`.

**Evidence grade.** I used all 6 of my WebSearch calls and no WebFetch. Every web fact here comes from a search snippet and is tagged (via search snippet) in the log. Facts from training knowledge carry the tag [training knowledge] and never get a URL. My own arithmetic is tagged [ESTIMATE] and lives in the model. No patent search was possible within the quota.

---

## 1. Bottom line

The concept survives on physics, but the model changes what matters. The client typing signal, which the card names as the key unknown, is not the binding risk. Deleting the host-DRAM KV tier works at short contexts even without the signal. What binds is the tail of the context-length distribution, how good a retrofitted latent can get, how long prefetched KV sits in HBM, and how much the flash is written.

Headline numbers, all [ESTIMATE] from the model unless cited:

| Quantity | Value | Note |
|---|---|---|
| Rack DRAM today (GB300 NVL72) | 38.0 TB = 72 x (288 GB HBM + 240 GB LPDDR5X) | 17 TB LPDDR5X and ~21 TB HBM3e per rack ([Supermicro](https://www.supermicro.com/zh_tw/products/rack/srs-gb300-nvl72); [NVIDIA](https://www.nvidia.com/en-in/data-center/gb300-nvl72/)) [REPORTED] |
| Host DRAM freed by host-DRAM-lite | **12.7 TB per rack (33%)** at 64 GB/GPU; 8.6 TB (22.7%) at the critic's 120 GB/GPU | $253k per rack at $20/GB; $18.8k at the $1.48/GB production cost |
| Share of returning turns a 240 GB/GPU host KV tier serves | **~5%** | An LRU tier holds a session ~9 s, against a ~110 s median human gap ([arXiv 2605.18825](https://arxiv.org/pdf/2605.18825)) |
| Idle-but-returning KV vs active KV | **19.5x** (card assumed ~3-5x) | Gap fit: median 110 s, P80 372 s, TTL 600 s |
| DRAM GB per served conversation, host-lite only (B0) | **1.50x fewer** than today | No client signal; p99 added TTFT 0.33 s at 3 drive-eq/GPU |
| ... with the 3x latent (D0) | **4.50x fewer** (latent alone: 3.00x) | Card claimed 2-3x net |
| ... with client prefetch too (D) | 3.89x fewer | Prefetched KV held in HBM (1.6-1.7 s/turn) costs back part of the gain |
| DDR5-wafer-equivalent per conversation (HBM counted x3) | B0 1.19x, D0 3.57x, B 1.02x | In wafer terms the client signal's HBM hold cancels most of the host-lite saving unless hold is <~1 s/turn |
| Flash read demand per GPU | ~16.6 GB/s before hold and false positives (flash-supply law); 21 GB/s with them | Independent of KV compression when HBM capacity binds |
| Flash writes | ~107-126 TB/day per GPU, i.e. **~860 TB/day per 8-GPU node** (critic: ~280) | B300-class throughput (~7.6k new tokens/s per GPU) |
| Flash needed | **3 Gen5 drive-equivalents (3 x 15.36 TB, 3 DWPD) per GPU**: 2.33 DWPD, rho 0.51 | The 2026 baseline (LMCache disk / ICMS) needs the same, so the increment is ~0 |
| Client-signal value | p99 added TTFT 0.33 s down to 0.11 s at base. It saves 1.1 drive-eq/GPU (base mix) up to 4.7 (128k FP8) and lifts the FP8 single-length context limit from ~21k to ~38k tokens (latent: ~63k to ~113k) | Needs a send predictor; first-keystroke prefetch costs +82% HBM KV |

**GO/NO-GO (from the model).** The decisive test replays consented chat traces on one 8-GPU node with host memory capped at <=64 GB/GPU and no host-DRAM KV tier. It is a GO if three things hold.
1. p99 added TTFT is <=0.30 s against a 240 GB/GPU host-tier baseline, at equal tokens/s and <=3 Gen5 drive-equivalents per GPU. The model predicts 0.33 s without the signal and 0.11 s with it.
2. Flash stays at <=3 DWPD. The model gives 2.33.
3. The send predictor holds prefetched KV in HBM for <=1.0 s per turn.

The latent gate is >=3x compression over FP8 GQA at <=1 point loss in RULER average at 32k. It is a NO-GO if p99 fails at the measured context distribution even with the latent and 3 drive-eq/GPU, because a DRAM KV tier would then have to come back.

### Corrections to the concept card
1. **Think time.** The card assumed a 30 s median. A production chat trace gives ~110 s median, ~372 s P80 and ~2,207 s P99 ([arXiv 2605.18825](https://arxiv.org/pdf/2605.18825), via snippet). Resident-KV duty is therefore ~5%, not 15-25%. The hibernation lever is bigger than claimed. But today's systems already exploit it, because flash (LMCache disk, ICMS) serves ~95% of returns.
2. **The ">=80% coverage" threshold is the wrong form.** p99 is set by flash queueing and by the restore time of long contexts. With a deadline-aware flash queue, the share of turns with no usable lead barely moves p99 at 3 drive-eq/GPU (0.10 s at 0% no-lead, 0.17 s at 60%). At 2.5 drive-eq it passes up to 60%; at 2 drive-eq nothing passes. Lean flash is where lead coverage matters.
3. **The latent does not fix per-drive flash wear or bandwidth.** It fixes them per user. When HBM capacity binds, a GPU's flash traffic is about its HBM KV pool divided by the generation time, whatever the bytes per token (the flash-supply law). The latent triples conversations per GPU, so flash load per conversation falls 3x (13.7 to 4.6 MB/s).
4. **NAND writes are ~3x the critic's figure** at B300-class throughput (~860 TB/day per 8-GPU node). They fit only with ~3 x 15.36 TB mixed-use drives per GPU, or pod flash shelves.
5. **Client prefetch must not start at the first keystroke.** That parks KV in HBM for the whole composition time: 8.2 s/turn, 82% more HBM KV, and a worse DRAM-per-user figure than today. A send predictor (typing pause, cursor on send, end of speech) with <=0.5 false positives per turn brings hold to 0.7-1.7 s.
6. **Latent distillation is cheap.** X-EcoMLA used 3.6B tokens and ~70 MI300 GPU-hours for a 1B model ([arXiv 2503.11132](https://arxiv.org/html/2503.11132v1), via snippet). An 8B retrofit at 2-5B tokens is ~200-500 H100-hours [ESTIMATE]. The full ablation campaign plus a 70B confirm run is ~$50k, not $100k.

---

## 2. Prior art and who is pursuing it

| Component | Closest prior art (date) | Who | What it does / gap left |
|---|---|---|---|
| Flash KV tier | NVIDIA Inference Context Memory Storage Platform with BlueField-4 (CES, 2026-01) ([NVIDIA](https://nvidianews.nvidia.com/news/nvidia-bluefield-4-powers-new-class-of-ai-native-storage-infrastructure-for-the-next-frontier-of-ai)) | NVIDIA, with Dell, HPE, Pure, VAST and WEKA ([Barchart](https://www.barchart.com/story/news/36894738/nvidia-bluefield-4-powers-new-class-of-ai-native-storage-infrastructure-for-the-next-frontier-of-ai)) | Pod-level flash "G3.5" KV tier fronted by DPUs ([Solidigm](https://www.solidigm.com/products/technology/icmsp-ai-inference-is-flash-storage-problem.html)). Treats KV as ephemeral ([NAND Research](https://nand-research.com/research-note-improving-inference-nvidias-inference-context-memory-storage-platform/)). **KV-to-flash is now mainstream; the diet cannot claim it.** |
| Tiered KV manager | Dynamo KVBM (G1 HBM, G2 host, G3 SSD, G4 remote) [training knowledge, 2025]; NIXL ([NAND Research](https://nand-research.com/?p=5081)) | NVIDIA | Keeps the host-DRAM G2 tier. Gap: no host-DRAM-minimal configuration or client deadlines. |
| Vendor-neutral KV cache | LMCache (disk and remote backends) [training knowledge]; TensorMesh ([GMI Cloud](https://www.gmicloud.ai/blog/gmi-cloud-achieves-4x-llm-performance-boost-with-tensormesh), vendor claim: SSD prefix caching ~4x TTFT vs ~1.4x RAM-only) | UChicago (Junchen Jiang) / TensorMesh | The RAM-only result matches the model: host RAM evicts too fast on multi-turn work. |
| Disaggregated KV pool | Mooncake [training knowledge, FAST'25] | Moonshot AI / Tsinghua | DRAM+SSD pool across nodes. |
| Disk prefetch | CachedAttention/AttentionStore, ATC'24 ([arXiv 2403.19708](https://arxiv.org/abs/2403.19708)) | Huawei and academic co-authors [training knowledge] | Scheduler-lookahead prefetch with <1 s of lead. |
| Reuse prediction | KVCache Cache in the Wild ([arXiv 2506.02634](https://arxiv.org/html/2506.02634v4), 2025-06) | Alibaba Cloud [training knowledge] | Reuse time predictable per category. Server-side, no client signals. |
| Gap-aware eviction | Semantic-aware prefix-cache eviction ([arXiv 2605.18825](https://arxiv.org/pdf/2605.18825), 2026-05) | academic [unverified affiliation] | Log-normal per-session gaps; 99.28% same-session reuse. |
| Using typing as a signal | LiveMind ([arXiv 2406.14319](https://arxiv.org/html/2406.14319v2), 2024-06; [code](https://github.com/ChuangtaoChen-TUM/LiveMind)) | TUM (Chuangtao Chen et al.) | Runs inference on partial typed input. Text level, not KV-tier placement. The closest prior art to the client-signal delta. |
| Input-event prefetch (general) | Prefetch-on-hover (instant.page, browser speculation rules) [training knowledge] | Web ecosystem | Weakens any broad claim on "prefetch triggered by user input events". |
| Skeptic view | WEKA: KV prefetch is "almost impossible" because need is unpredictable ([WEKA](https://www.weka.io/article/why-prefill-has-become-the-bottleneck-in-inference-and-how-augmented-memory-grid-helps)) | WEKA | Client signals answer exactly this objection. |
| Load-or-recompute | Cake ([arXiv 2410.03065](https://arxiv.org/html/2410.03065v2)) | academic | Fallback for uncovered turns (f_fb = 0.5 in the model). |
| Tool-wait KV | InferCept, ICML'24 [training knowledge] | UCSD | Agent tool waits. |
| Latent KV retrofit | MHA2MLA ([2502.14837](https://arxiv.org/abs/2502.14837v1)): -92.19% KV on Llama2-7B (MHA), -0.5% LongBench. TransMLA ([2502.07864](https://arxiv.org/html/2502.07864v5)): GQA to MLA, -68.75% training-free. X-EcoMLA ([2503.11132](https://arxiv.org/html/2503.11132v1)): 6.4x with an 8B teacher. xKV ([2503.18893](https://arxiv.org/abs/2503.18893)): 8x on GQA Llama-3.1-8B at 87.8% RULER avg | Fudan [training knowledge]; PKU (Muhan Zhang) [training knowledge]; AMD; Cornell (Abdelfattah) [training knowledge] | **Per-layer** latents. One latent shared across all layers and trained by retrofit is still open (YOCO and LCKV were pretrained). |
| Cross-finetune KV | DroidSpeak, NSDI'26 ([USENIX](https://www.usenix.org/conference/nsdi26/presentation/liu-yuhan)); Activated LoRA (IBM 2025) [training knowledge] | Microsoft/UChicago; IBM | Exact-sharing-by-freezing adds little (Stage 2 innovation lens: DROP). Keep only as a platform rule. |
| Attention offload | Lamina ([2405.01814](https://arxiv.org/html/2405.01814v1)) | Tsinghua [training knowledge] | Optional retired-GPU KV tier. |
| PIM top-k (optional) | Samsung LPDDR5X-PIM, Hot Chips 2026 (A3 log) | Samsung | Demoted to optional by the chief. |
| 2026 KV-serving papers (titles only) | SwiftCache ([2606.16135](https://arxiv.org/pdf/2606.16135)); CacheWise ([2606.16824](https://arxiv.org/pdf/2606.16824)); TraceLab ([2606.30560](https://arxiv.org/pdf/2606.30560)); KV-offload bottlenecks ([2601.19910](https://arxiv.org/pdf/2601.19910)) | academic | Crowded field; read before filing. |

**What remains new.** Four things.
1. Client deadlines turn flash restores into scheduled background traffic, using a two-class deadline-aware NVMe queue and a bound on HBM hold time.
2. The claim that host-DRAM KV tiers are a poor use of bits for human chat, with the arithmetic to back it (~5% hit rate at 240 GB/GPU; ~55% even at 2 TB/GPU).
3. A trained cross-layer shared latent beyond per-layer MLA retrofits.
4. A published host-DRAM-minimal node spec.

Items 2 and 4 are publishable results rather than strong IP.

## 3. Best demonstrated numbers by component

| Component | Best number found | Source |
|---|---|---|
| Rack memory | 20.7-21 TB HBM3e plus 17-17.3 TB LPDDR5X; 576 TB/s HBM and 14 TB/s CPU memory bandwidth per rack | Supermicro, NVIDIA, [Red Hat](https://catalog.redhat.com/en/hardware/system/detail/307917), [Lenovo](https://pubs.lenovo.com/gb300-nvl72/server_features) (snippets) |
| Human inter-turn gap | median ~110 s, P80 ~372 s, P99 ~2,207 s | arXiv 2605.18825 (snippet) |
| KV compression, retrofit | 8x (xKV, RULER 87.8% avg); 12.8x vs MHA (MHA2MLA, -0.5% LongBench) = ~3.2x beyond GQA-8 [ESTIMATE]; 6.4x (X-EcoMLA, LM-Harness) | snippets above |
| KV restore software | thaw-vllm restores a 136 MB cache in ~0.135 s (project claim, s2 log) | [PyPI](https://pypi.org/project/thaw-vllm/0.3.2/) |
| SSD prefix cache vs RAM-only | ~4x vs ~1.4x TTFT gain (vendor) | GMI Cloud |
| Gen5 NVMe | ~14 GB/s read per drive [training knowledge, ESTIMATE] | — |
| Server DRAM price 2026 | retail DDR5 RDIMM medians ~$31.75-35.70/GB; contract reset ~+95% in 1Q26 (snippet attribution unconfirmed) | [Capital & Compute](https://capitalandcompute.net/memory-prices/server/); [DatacenterDisk](https://datacenterdisk.com/reports/server-ram-market-report-2026); [TrendForce](https://www.trendforce.com/presscenter/news/20260202-12911.html) |
| Enterprise SSD price 2026 | a 3.84 TB enterprise NVMe drive costs ~2.3-2.8x its January price | [ITLDC](https://itldc.com/es/blog/server-ram-ssd-market-update-2026) (snippet) |
| HBM wafer tax | ~3x DDR5 wafer per bit | Micron via Tom's Hardware (A1) |

## 4. Facilities

**No fabrication is needed.** The nanofab, national-lab cleanroom and MPW list in the brief (SNF, CNF, MIT.nano, Singh, IEN, ASU, Birck, UT Austin; MESA/CINT, CNM, CNMS, Molecular Foundry, CNST; ChipFoundry sky130, wafer.space GF180, MOSIS) does not apply to the seed plan. The only hardware arm is the optional PIM top-k, which would start on Samsung LPDDR5X-PIM samples or UPMEM DIMMs with Ramulator2 and DRAMPower. A 28 nm top-k synthesis via MOSIS or ChipFoundry would be a post-raise option.

| Need | Facility | Notes |
|---|---|---|
| Grace-class host-lite tests | TACC Vista (NVIDIA GH200 Grace Hopper nodes) via NSF ACCESS or the NAIRR Pilot [training knowledge] | Closest public analogue to Grace LPDDR5X plus HBM. Allocation is free; cycle time is months. |
| Large replays | NERSC Perlmutter (A100), ALCF Polaris (A100), via DOE ALCC or Director's Discretionary [training knowledge] | The concept card names these. Local NVMe and GDS support per node must be checked [UNVERIFIED]. |
| 8-GPU node with local Gen5 NVMe and GDS | Neocloud rental (Lambda, CoreWeave, Together) or AWS p5 (8 local NVMe) [training knowledge] | Assumed $2-4/GPU-h [ESTIMATE, not verified this session]. Needs root access for cgroups, GDS and the NVMe priority queue. |
| GB300 / NVL72 validation | CoreWeave or other GB300 cloud capacity [training knowledge] | One week of time for the integrated demo. |
| Flash wear rig | Own box: 12 x Gen5 15.36 TB drives in a JBOF | ~$36k [ESTIMATE]. SMART media-wear counters under replayed write traces. |
| User study | IRB through a university collaborator (UChicago, Berkeley or UCSD) | Logs event timing only, never content. |
| Front-end | Open WebUI or LibreChat fork with a "signal SDK" [training knowledge] | LMArena (Berkeley origin) is a possible large-scale partner. |
| Public traces | WildChat (per-turn timestamps), Mooncake trace, BurstGPT [training knowledge] | Gap and context distributions for free; no typing lead. |

## 5. Collaborators and recruits

All affiliations below are [training knowledge] unless a URL is given.
- **UChicago, Junchen Jiang** (LMCache, CacheGen, CacheBlend, DroidSpeak). Natural home for the replay testbed; LMCache is the plugin target.
- **UC Berkeley Sky Computing Lab, Ion Stoica** (vLLM, LMArena). Trace partnership and upstreaming.
- **UCSD: Hao Zhang** (DistServe; vLLM co-creator) **and Yiying Zhang** (InferCept). Agent and tool-wait traffic.
- **CMU: Beidi Chen** (ShadowKV) **and Zhihao Jia**. Sparse KV and serving systems.
- **MIT Han Lab, Song Han** (Quest, DuoAttention). Top-k KV.
- **Cornell, Mohamed Abdelfattah** (xKV, Palu). Best fit for the shared-latent arm.
- **PKU, Muhan Zhang** (TransMLA); **Fudan** MHA2MLA authors; **AMD** X-EcoMLA team. Latent retrofit baselines.
- **Tsinghua, Mingxing Zhang / Moonshot AI** (Mooncake).
- **TUM, Grace Li Zhang and Ulf Schlichtmann** (LiveMind). Streaming-input inference.
- **IBM Research** (Activated LoRA).
- **Industry partners or potential acquirers:** NVIDIA Dynamo/ICMS team; WEKA, VAST and Pure (KV storage); flash makers (Solidigm, Micron, Samsung, Kioxia), which gain from more flash per GPU and may fund a wear study.
- **Recruit profile.** The mission's "device or circuit expert" seat becomes an ML-systems engineer: a vLLM or LMCache committer, ideally a PhD from the Jiang, Stoica or Zhang groups. A second, part-time ML researcher owns the latent distillation.

## 6. Decisive experiment

### Step by step
1. **M0-M2: setup.**
   - Fork Open WebUI and add a client "signal SDK" that emits timestamped focus, keystroke, pause, paste, hover-on-send, chip-hover, speech-start/end and send events. It logs no content.
   - Secure IRB approval through a university partner.
   - Stand up vLLM+LMCache with a GPUDirect-Storage backend on a rented 8-GPU node.
   - Reproduce the model's scenarios A (240 GB/GPU host tier) and B0 (host capped at 64 GB/GPU by cgroup, no host KV tier) on public traces.
2. **M2-M6: lead-time study.**
   - Recruit 300-500 consenting users for 6 weeks against a hosted open model.
   - Measure the lead distribution per event type and the no-lead share.
   - Train and evaluate a send predictor and plot its hold-vs-miss curve and false-positive rate.
   - Measure the context-length distribution.
   - Fit the gap distribution and compare it with arXiv 2605.18825.
   - **Gate G1:** at least one predictor reaches hold <=1.0 s/turn with <=0.5 false positives per turn. If no predictor does, drop the client signal and continue with B0.
3. **M4-M10: replay testbed.**
   - Use an 8-GPU H200/B200 node with 16-24 Gen5 drives (2-3 per GPU) or 8 local drives plus an NVMe-oF shelf.
   - Implement the two-class deadline-aware restore queue: urgent restores go at NVMe high priority; restores with lead are chunked and preemptible.
   - Replay the study traces, scaled up, at equal tokens/s for A, B0 and B.
   - Record p50/p90/p99 TTFT, host RSS, flash utilisation, read/write interference and NAND TB/day (SMART).
   - Run the wear rig in parallel at the measured write rate.
   - **Gate G2:** p99 added TTFT <=0.30 s versus A at <=3 drive-eq/GPU, and <=3 DWPD.
4. **M6-M14: shared latent.**
   - Distil Llama-3.1-8B into one shared cross-layer latent with decoupled RoPE dimensions (MLA-style), using 2-5B tokens.
   - Run ablations at 3x, 6x and 12x against xKV, MHA2MLA and TransMLA on RULER and LongBench at 32-128k.
   - Do a 70B confirm run at 3x.
   - **Gate G3:** >=3x at <=1 point loss in RULER average at 32k.
5. **M14-M20: integrated demo.**
   - Run two nodes (16 GPUs) with the latent model, host-lite, the signal SDK and an opt-in live beta for 4 weeks.
   - Publish open-source LMCache/vLLM plugins and an OCP-style host-DRAM-lite node spec with wear projections.
6. **M20-M24:** raise $10-50M on the measured numbers.

### Budget (<= $1M)

| Line | $ | Basis [ESTIMATE] |
|---|---|---|
| Two founders, 22 months loaded | 396,000 | $9k/month each |
| ML-systems contractor or PhD intern (12 months part-time) | 60,000 | |
| Lead-time study (incentives 400 x $50, hosted model GPUs, IRB/privacy review) | 45,000 | |
| Replay testbed compute (~3,000 node-hours at ~$25/h) | 75,000 | $3/GPU-h |
| Flash wear rig (12 x 15.36 TB Gen5 plus JBOF) | 36,000 | ~$3k/drive at 2026 prices |
| Latent distillation and evals (~11,000 GPU-h plus storage) | 50,000 | 8B ablations, 70B confirm, RULER 128k |
| Integrated live demo (16 GPUs x 6 weeks) | 60,000 | |
| IP: 3 provisionals plus FTO search and opinion | 45,000 | |
| Travel (OCP Summit, MLSys/OSDI), tooling, cloud storage | 35,000 | |
| Contingency (~10%) | 80,000 | |
| **Total** | **882,000** | Decisive core (G1+G2+G3) external spend ~$206k |

### Timeline (months)

| Workstream | M0-2 | M2-6 | M6-10 | M10-14 | M14-20 | M20-24 |
|---|---|---|---|---|---|---|
| Setup, SDK, IRB, A/B0 repro | X | | | | | |
| Lead-time study, G1 at M6 | | X | | | | |
| Replay testbed and wear rig, G2 at M10 | | X | X | | | |
| Latent distillation, G3 at M14 | | | X | X | | |
| Integrated demo, spec, plugins | | | | | X | |
| Raise | | | | | | X |

## 7. IP landscape

- **Patents to watch.** No patent search was run (quota). Do FTO before filing. Likely assignees, inferred from who ships these features [training knowledge]:
  - NVIDIA: Dynamo KVBM, ICMS, BlueField-4 KV placement.
  - Huawei and Alibaba: CachedAttention, KV cache in the wild.
  - Moonshot AI: Mooncake.
  - WEKA, VAST, Pure: KV storage.
  - Microsoft and Google: serving schedulers.
  - Samsung: PIM and CXL KV.
  - IBM: aLoRA.
  - DeepSeek: MLA (patent status unknown).
- **Prior art that narrows claims.** Web prefetch-on-hover and speculation rules (input-event-triggered prefetch); LiveMind (typing-time inference); CachedAttention (scheduler-hint prefetch); MLA, MHA2MLA, TransMLA, X-EcoMLA and xKV (latent KV).
- **What to file (provisionals).**
  1. Client-deadline KV restore: a two-class NVMe/flash scheduler where client input events set deadlines, urgent restores preempt, and a send-predictor gate bounds HBM hold time.
  2. Wear-aware append-only KV spill gated by predicted return probability, with chunk-level dedup across turns.
  3. A retrofit recipe for one shared cross-layer latent with per-layer absorbed up-projections and decoupled RoPE dimensions.
- **Publish defensively, do not patent.** The host-DRAM-lite node spec (OCP) and the host-tier hit-rate analysis. Their value comes from adoption.

## 8. Open gaps

1. **No lead-time data exists**, so the segment mix is entirely [ESTIMATE]. This is Phase 1.
2. **Context-length distribution of real chat.** The model's median 8k / sigma 1.0 is a guess, and the FP8 limit (~38k single-length) makes this the swing input.
3. **Write interference.** The model's M/M/1 read queue ignores write interference on the same drives (~1.2 GB/s writes per GPU), and NVMe priority-queue support varies by drive.
4. **Physical flash slots.** Can GB300/Vera Rubin trays hold 3 drive-eq per GPU locally, or must part come from pod shelves over the NIC? [UNVERIFIED]
5. **Board options.** Whether Vera Rubin's host memory (SOCAMM-style modules, ~1.5 TB/CPU per the Stage 2 critique) can be shipped depopulated is what turns host-lite into bits not bought. Soldered Grace LPDDR5X cannot be.
6. **Agent traffic** (short tool gaps, sandbox DRAM) and **training nodes** (checkpoint staging) are not modeled. The critic-corrected 120 GB/GPU case covers part of this.
7. **Prices.** DRAM and SSD prices are snippet-level and unattributed. At cost ($1.48/GB) the host DRAM saved is ~$19k per rack: this is a shortage-era economics story, and the bit savings stand regardless.
8. **Fleet size.** The model reports per 10,000 racks (0.09-0.13 EB, 0.13-0.19% of world DRAM bits) and makes no shipment forecast.
9. **Shared latent quality beyond ~3x** is unknown. The latent supplies most of the DRAM-per-user gain (3x of the 4.5x).

**Kill/revival.** No physics kill. The concept's DRAM-bit value would collapse only if real p99 context lengths are long (>~40k tokens at FP8) and the latent stalls at <=2x. Then a DRAM KV tier returns for long contexts and the gain shrinks to host-lite on short-context fleets. **Revival condition:** a >=3x shared latent, or Gen6 NVMe at ~28 GB/s per drive [ESTIMATE: PCIe 6.0 x4 doubles Gen5], which roughly halves restore time and doubles the FP8 context limit.
