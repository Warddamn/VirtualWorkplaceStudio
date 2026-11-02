# AI MEMORY DIET: delete DRAM's jobs in the AI racks that cause the shortage

NEW DRAM Stage 3 dossier. Author: agent `dosw-ai-memory-diet`, 2026-11-02.

Inputs:
- Model `models/ai-memory-diet.py`, re-run today with exit 0. Its output matches `research/stage3/ai-memory-diet_model_output.md`.
- Notes `research/stage3/ai-memory-diet_notes.md`; assumptions `research/assumptions/dos-ai-memory-diet.md`.
- Concept card in `research/stage3/FINAL_CONCEPTS.json`; Stage 2 critiques in `research/ideas10k/stage2/stage2_results.jsonl`.

Tags:
- [REPORTED]: from a logged source, usually seen only as a search snippet.
- [ESTIMATE]: model arithmetic.
- [UNVERIFIED-PK]: prior knowledge, no URL.
- [SPECULATIVE]: not yet shown by anyone.

No WebSearch was used for this dossier. No patent search has been run for this concept.

---

## 0. Header

**Name:** AI MEMORY DIET.

**Thesis:** Human chat leaves a GPU's KV cache idle ~95% of the time, so stop parking it in host DRAM. Stream it straight between HBM and flash on client deadlines, shrink it ~3x with a trained latent, and ship AI nodes with a small fraction of today's host DRAM.

**Rank:** 10 of 10, EV 30 (S2 x P3 x D5).

**Category:** system/architecture. This is the portfolio's demand hedge. It makes no new cell.

**Lineage:** system-lens concept "AI Memory Diet", taken whole. It has no device-lens counterpart. The chief scientist demoted in-PIM top-k to an option, because software top-k already takes most of that gain.

| Id | Idea | Creativity technique | Stage 2 verdict (consensus) | Role in the diet |
|---|---|---|---|---|
| I-10877 | Host-DRAM-lite AI servers (GPU-direct shard decode, checkpoint streaming) | Wishful thinking / ideal final result | ADVANCE (63.2) | Core 1: host DRAM cut to 64-120 GB/GPU |
| I-08555 | Typing-indicator KV prefetch for hibernated chat | Scale and time shifting | ADVANCE (72.1) | Core 2: client-deadline restore from flash |
| I-07651 | Mycologist's spores: hibernate idle agents | Perspective shift / personas | HOLD (65.6) | Core 2 for agents (KV plus sandbox) |
| I-04878 | One latent per token regenerates every layer's K/V | Assumption inversion | ADVANCE (60.6) | Core 3: shared cross-layer latent |
| I-11326 | Cross-finetune KV sharing below the first modified layer | Scarcity and constraint as engine | HOLD (64.1; innovation DROP) | Core 4, demoted to a platform rule |
| I-09070 | In-DRAM KV top-k ("Automata Processor fixed") | Failure mining | ADVANCE (64.7) | Option: PIM top-k for long context |
| I-00766 | Retired GPUs as attention/KV servers | SCAMPER-Combine | ADVANCE (64.1) | Option: long-context KV tier |
| I-04908 | Export idle host DRAM of GPU servers as far memory | Assumption inversion | HOLD (63.5) | Bridge for installed, soldered boards |
| I-10963 | Recompute-as-correction for KV caches | Wishful thinking / ideal final result | HOLD (63.5) | Fallback: recompute repairs misses |
| I-07637 | KV cache as a per-sequence implicit neural field ("2050 engineer") | Perspective shift / personas | HOLD (68.8) | Research option beyond 3x |

**Verdicts**

- **PHYSICALLY POSSIBLE? Yes.**
  - Nothing here touches device physics. The limits are flash bandwidth (16.6-21 GB/s per GPU), NAND wear (107-126 TB/day per GPU), and the restore time of long contexts at p99.
  - All three fit inside 3 Gen5 drive-equivalents per GPU for contexts up to ~38k tokens at FP8, or ~113k with a 3x latent [ESTIMATE].
- **STEP CHANGE IF IT WORKS? Partly. Axis: DRAM bits demanded per served AI chat user, which is the A2 binding constraint.**
  - Host-lite alone frees 22% (critic-corrected) to 33% (model) of rack DRAM. That is 1.50x fewer DRAM GB per conversation, or 1.19x in DDR5-wafer terms.
  - With a 3x latent the gain is 4.5x (3.6x wafer). But most of the latent's 3x is prior art (MLA-class compression).
- **PROVABLE WITH $1M IN 24 MONTHS? Yes for the technical claim; no for "bits not bought".**
  - ~$206k of external spend settles all three gates by month 14 on rented GPUs. No fab is needed.
  - Whether OEMs ship boards with less host DRAM fitted is a partner decision, outside the seed.

---

## 1. How it works

A chatbot answering you keeps "working notes" on the whole conversation. These are its KV cache. For a 70B-class model they take ~160 kB per token, so a 13k-token chat needs ~2 GB of notes. The notes must sit in the GPU's own memory, HBM, while the model is writing a reply. That takes ~10 seconds.

Then you read, think and type, and that takes much longer. A production chat trace shows a median gap of ~110 s between turns, with a P80 of ~372 s [REPORTED, arXiv 2605.18825]. During that gap, today's servers move your notes down a ladder: from HBM to the host computer's DRAM, then to flash (SSDs). Each AI rack carries ~17 TB of host DRAM, against ~21 TB of HBM.

The model finds that the host-DRAM rung barely works for human chat. So many people are chatting that a 240 GB/GPU host tier holds any one conversation for only ~9 s before evicting it. People take ~110 s. Only ~5% of returning turns find their notes still in host DRAM. Flash already serves the other ~95%.

The diet does four things:

1. **Delete the host-DRAM rung.** Notes go directly from HBM to flash and back over GPUDirect Storage. Host DRAM shrinks to what the operating system and runtime need: 64 GB/GPU in the model, 120 GB/GPU in the critic's case.
2. **Give flash a deadline.** The chat app sends a content-free hint: "this user is about to hit send". The hint comes from a typing pause, the cursor moving to Send, or the end of speech. The server then pulls the notes back from flash just in time. A two-class flash queue serves urgent restores first and streams the rest in the background.
3. **Shrink the notes ~3x.** A short distillation teaches the model to store one compact "latent" per token, which each layer expands back to keys and values. The KV cache gets smaller at every tier.
4. **Publish the node spec**, so that GPU servers can ship with far less host DRAM fitted.

```
TODAY (per GPU)                              THE DIET (per GPU)

 reply ~10 s      think ~110 s (median)       reply ~10 s      think ~110 s
 +-----------+    evict    +-------------+    +-----------+                     +------------------+
 | HBM 288GB |  -------->  | host DRAM   |    | HBM 288GB | <== GPUDirect ===>  | flash, 3 Gen5    |
 | weights + |  <--------  | 240 GB KV   |    | weights + |   deadline queue    | drive-eq/GPU     |
 | live KV   |  ~5% of     | tier (holds |    | live KV   |   (urgent first)    | 3 x 15.36 TB     |
 +-----------+  returns    | ~9 s)       |    +-----------+                     +------------------+
       ^                   +-------------+          ^
       |                         | evict            |  "about to send" hint (timing only, no text)
       +--- ~95% of returns -- [ flash ]      [ chat app send predictor ]
                                              host DRAM: 64 GB/GPU for OS + runtime, no KV tier
```

---

## 2. The physics and the numbers

All numbers are [ESTIMATE] outputs of `models/ai-memory-diet.py` unless tagged otherwise.

### 2.1 KV geometry and the human gap

- KV per token for a 70B GQA model with FP8 KV is 2 x 80 layers x 8 KV heads x 128 x 1 B = **160 KiB/token**. A 3x latent gives 53.3 KiB.
- Session sizes and one-drive restore times at ~14 GB/s per Gen5 drive [UNVERIFIED-PK]:

| Context | FP8 KV | Latent KV | One-drive restore, FP8 / latent |
|---|---|---|---|
| 4k | 0.66 GB | 0.22 GB | 0.05 / 0.02 s |
| 32k | 5.24 GB | 1.75 GB | 0.37 / 0.12 s |
| 128k | 20.97 GB | 6.99 GB | 1.50 / 0.50 s |

- The inter-turn gap is fitted as a log-normal with median 110 s and P80 372 s [REPORTED]. Its mean is 314 s. The fitted P99 is 3,192 s against 2,207 s reported, which is conservative for flash capacity.
- With a 600 s warm TTL, 87.9% of turns return in time, and E[min(gap, TTL)] = 195 s. Idle-but-returning KV is therefore 195/10 = **19.5x** the active KV for a 10 s generation. The card assumed a 30 s median and ~3-5x.

### 2.2 Per-GPU scenarios (base context mix: log-normal, median 8k, mean 13.0k tokens)

The HBM KV budget is 288 x 0.9 - 70 GB of weights = 189 GB. Divided by 2.13 GB per session, that gives 89 active sessions. Conversations per GPU = 89 x (10 + 195)/10 = 1,820.

| Scenario | Host GB/GPU | Conversations/GPU | p99 added TTFT | DRAM GB / conversation | Wafer-eq GB / conversation (HBM x3) | vs today, DRAM / wafer |
|---|---|---|---|---|---|---|
| A. Today: HBM + 240 GB host tier + flash, FP8 | 240 | 1,820 | 0.30 s | 0.290 = 528/1,820 | 0.607 = (864+240)/1,820 | 1.00x / 1.00x |
| B0. Host-lite, no client signal, FP8 | 64 | 1,820 | 0.33 s | 0.193 | 0.510 | 1.50x / 1.19x |
| B. Host-lite + client prefetch, FP8 | 64 | 1,557 | 0.11 s | 0.226 | 0.596 | 1.28x / 1.02x |
| C. Today + 3x latent | 240 | 5,459 | 0.10 s | 0.097 | 0.202 | 3.00x / 3.00x |
| D0. Host-lite + 3x latent, no signal | 64 | 5,459 | 0.11 s | 0.064 | 0.170 | 4.50x / 3.57x |
| D. Full diet | 64 | 4,713 | 0.03 s | 0.075 | 0.197 | 3.89x / 3.08x |

Three results change the card's story:
1. **Host-lite does not need the client signal at short contexts.** B0 misses the 0.30 s budget by only 0.03 s at 3 drive-equivalents per GPU. A fourth drive closes the gap: 3.2 drive-eq/GPU is enough (section 2.5).
2. **The client signal costs HBM.** Prefetched KV waits in HBM for ~1.7 s per turn, which adds 17% HBM KV per active session. In wafer terms, B is only 1.02x better than A. The signal pays only if HBM hold stays under ~1 s per turn.
3. **The latent provides most of the gain:** 3x of D0's 4.5x. The diet's own share beyond the latent is C/D0 = 1.50x.

### 2.3 Rack and fleet (GB300 NVL72 class)

Rack DRAM today is 72 x (288 GB HBM + 240 GB LPDDR5X) = **38.0 TB** [REPORTED: ~21 TB HBM3e and ~17 TB LPDDR5X; NVIDIA lists 37 TB].

| Host-lite GB/GPU | Host DRAM freed per rack | % of rack DRAM | $ at $1.48/GB cost | $ at $20/GB | Fab kWh avoided | Water avoided |
|---|---|---|---|---|---|---|
| 64 (model) | 72 x 176 = 12.7 TB | 33.3% | $18,755 | $253,440 | 5,322 | 32,947 L |
| 120 (critic) | 72 x 120 = 8.6 TB | 22.7% | $12,787 | $172,800 | 3,629 | 22,464 L |
| 160 | 5.8 TB | 15.2% | $8,525 | $115,200 | 2,419 | 14,976 L |

- Per 10,000 racks, that is 0.086-0.127 EB not bought. This is 0.13-0.19% of ~68 EB/yr of DDR5-equivalent world output. The 10,000 racks are a scaling unit, not a forecast.
- HBM per conversation falls 2.59x, from 0.158 GB in A to 0.061 GB in D. Each HBM GB costs ~3x the DDR5 wafer area [REPORTED, Micron].
- **Honest scale.** At the $1.48/GB production cost, the freed host DRAM is worth only ~$19k per rack. The dollar case is a shortage-price story. The bit savings stand at any price.

### 2.4 Flash: the flash-supply law and the critics' numbers

When HBM capacity binds, flash must refill the whole HBM KV pool once per generation time:

- Read demand ≈ HBM KV budget / T_gen x P(return) = 189 GB / 10 s x 0.879 = **16.6 GB/s per GPU**. It rises to 21 GB/s with HBM hold and false positives.
- This holds **whatever the bytes per token**. The latent triples conversations per GPU, so flash load per conversation falls 3x (13.7 to 4.6 MB/s), but load per drive does not.
- Writes: ~8.9k new tokens/s per GPU x 160 KiB = 1.45 GB/s, or **125.6 TB/day per GPU** (107 TB/day with prefetch hold). That is **~860 TB/day per 8-GPU node**.
- Drives needed per GPU, in drive-equivalents: bandwidth 21.3/(14 x 0.6) = 2.54; endurance 107.4/(15.36 x 3 DWPD) = 2.33; capacity 0.31. Result: **3 x 15.36 TB, 3-DWPD drives per GPU, running at 2.33 DWPD**.

**Critic corrections carried:**
- Stage 2 put NAND wear at ~280 TB/day per node. The model's ~860 TB/day is **3x higher**, at B300-class throughput.
- The card said the latent cuts flash to ~17 GB/s per node. The model gives ~17 GB/s **per GPU**: 133-170 GB/s per node, or 24 drive-equivalents.
- Today's 2026 design (A: an LMCache-disk or ICMS-style flash tier) needs the same 3 drive-eq/GPU, because flash already serves ~95% of returns. **The diet's flash increment is ~0 against 2026 practice.** It is large only against a no-flash design.

Memory-plus-flash bill per 1,000 concurrent conversations (DRAM $20/GB, HBM at 3x, flash $0.20/GB): A $17,200; B0 $15,265 (-11%); D0 $5,088 (-70%).

### 2.5 Sensitivity

**Fixed context length** (3 drive-eq/GPU, deadline-aware queue, client prefetch):

| Context | p99 FP8, with signal / without | p99 latent, with / without | GO? FP8 / latent |
|---|---|---|---|
| 16k | 0.13 / 0.22 s | 0.04 / 0.07 s | GO / GO |
| 32k | 0.27 / 0.44 s | 0.08 / 0.15 s | GO / GO |
| 64k | 0.57 / 0.88 s | 0.18 / 0.29 s | NO-GO / GO |
| 128k | 1.21 / 1.76 s | 0.37 / 0.59 s | NO-GO / NO-GO |

The longest single length that passes is ~38k tokens at FP8 with the signal and ~21k without. With the latent, the limits are ~113k and ~63k.

**Share of turns with no client lead** (the card's "key unknown"). At 3 drive-eq/GPU, base-mix p99 runs from 0.10 s at 0% no-lead to 0.17 s at 60%, so it passes everywhere. At 2.5 drive-eq/GPU it passes up to 60% (0.28 s). At 2 drive-eq/GPU it fails at every share (0.37 s even at 0%). **The card's "≥80% coverage" threshold is the wrong form.** p99 is set by flash utilisation and by the restore time of the p99 context. Lead coverage matters only when flash is lean.

**Drives needed for p99 ≤ 0.30 s**, with signal / without:
- base FP8: 2.2 / 3.2;
- base latent: 1.7 / 2.0;
- 64k FP8: 3.9 / 6.1;
- 128k FP8: 5.5 / 10.1.

So the signal's real value is 1.1-4.7 drive-eq/GPU of flash saved, plus rescued long contexts. It does not save host DRAM.

**Prefetch policy:**

| Policy | HBM hold per turn | Extra HBM KV | Wafer-eq GB per conversation |
|---|---|---|---|
| Restore at first keystroke | 8.22 s | +82% | 0.936 (worse than today's 0.607) |
| Send predictor, m=3, 0 false positives/turn | 0.66 s | +7% | 0.548 |
| Send predictor, m=3, 0.5 false positives/turn | 1.70 s | +17% | 0.601 |

**Bigger host tier (baseline):**

| Host DRAM per GPU | Share of returns served from host | DRAM GB per conversation |
|---|---|---|
| 240 GB | 5.0% | 0.292 |
| 750 GB | 25.2% | 0.575 |
| 2,000 GB | 54.6% | 1.267 |

Heavy-tailed human gaps make a host-DRAM KV tier a poor use of bits.

**DRAM price:** the host DRAM freed is worth $18.8k per rack at $1.48/GB, $253k at $20/GB and $452k at $35.70/GB retail.

### 2.6 Against 1-beta DDR5

The diet does not change the DRAM chip. It changes how many 1-beta bits one served user consumes.

| Metric | 1-beta rack today (A) | Host-lite (B0) | Host-lite + latent (D0) |
|---|---|---|---|
| $/GB of the DRAM itself | $1.48 | $1.48 | $1.48 |
| DRAM GB per conversation | 0.290 | 0.193 | 0.064 |
| Wafer-eq GB per conversation | 0.607 | 0.510 | 0.170 |
| Wafer-eq at $1.48/GB, $ per conversation | $0.90 | $0.75 | $0.25 |
| Per-bit cost gain a new cell would need to match | 1.0x | 1.19x | 3.57x |
| Flash drive-eq per GPU | 3 | 3 | 3 |
| New cell, EUV or fab | n/a | none | none |

### 2.7 GO / NO-GO

The test replays consented chat traces on one 8-GPU node. Host memory is capped at ≤64 GB/GPU and there is no host-DRAM KV tier.

**GO if all three hold:**
1. p99 added TTFT ≤0.30 s against a 240 GB/GPU host-tier baseline, at equal tokens/s and ≤3 drive-eq/GPU. The model predicts 0.33 s without the signal and 0.11 s with it.
2. Flash stays at ≤3 DWPD. The model predicts 2.33.
3. For the signal to stay in the design, HBM hold must be ≤1.0 s per turn. If flash is trimmed to 2.5 drive-eq, the no-lead share must also be ≤60%.

**Latent gate:** ≥3x over FP8 GQA at ≤1 point loss in RULER average at 32k.

**NO-GO for the full concept:** p99 fails at the measured context distribution even with the latent and 3 drive-eq/GPU. A DRAM KV tier would then have to return.

---

## 3. What is new versus prior art

| Component | Prior art (date) | Who | What it leaves open |
|---|---|---|---|
| Flash KV tier | NVIDIA Inference Context Memory Storage Platform (ICMS) on BlueField-4, CES, Jan 2026 [REPORTED] | NVIDIA with Dell, HPE, Pure, VAST, WEKA | Pod-level "G3.5" flash KV tier. **KV-to-flash is mainstream; the diet cannot claim it.** |
| Tiered KV manager | Dynamo KVBM: HBM / host / SSD / remote, 2025 [UNVERIFIED-PK]; NIXL [REPORTED] | NVIDIA | Keeps the host-DRAM G2 tier; no client deadlines |
| Vendor-neutral KV cache | LMCache, 2024-25 [UNVERIFIED-PK]; TensorMesh: SSD prefix cache ~4x TTFT gain vs ~1.4x RAM-only (vendor) [REPORTED] | UChicago / TensorMesh | The RAM-only result agrees with the model: host RAM evicts too fast |
| Disaggregated KV pool | Mooncake, FAST'25 [UNVERIFIED-PK] | Moonshot AI / Tsinghua | DRAM+SSD pool |
| Disk prefetch | CachedAttention/AttentionStore, USENIX ATC'24 (arXiv 2403.19708, Mar 2024) [REPORTED] | Huawei and co-authors [UNVERIFIED-PK] | Scheduler-lookahead prefetch with <1 s of lead |
| Reuse prediction | "KVCache Cache in the Wild" (arXiv 2506.02634, Jun 2025) [REPORTED] | Alibaba Cloud [UNVERIFIED-PK] | Server-side history; no client signals |
| Gap-aware eviction | arXiv 2605.18825 (May 2026) [REPORTED] | academic | Log-normal gaps; 99.28% same-session reuse |
| Typing as a signal | LiveMind (arXiv 2406.14319, Jun 2024) [REPORTED] | TUM | Inference on partial input; text level, not KV placement. **Closest prior art to the signal** |
| Input-event prefetch | Prefetch-on-hover, browser speculation rules [UNVERIFIED-PK] | Web ecosystem | Weakens any broad "prefetch on user input" claim |
| Skeptic | WEKA: KV prefetch "almost impossible" (2026) [REPORTED] | WEKA | Client deadlines answer exactly this objection |
| Load-or-recompute | Cake (arXiv 2410.03065, Oct 2024) [REPORTED] | academic | Fallback for uncovered turns |
| Tool-wait KV | InferCept, ICML'24 [UNVERIFIED-PK]; TVCache, ICML'26 [REPORTED]; agent host-tier sizing paper (Sep 2026) [REPORTED] | UCSD; others | Agent prefixes survive tool waits only if the host tier holds the agent pool |
| Latent KV | MLA in DeepSeek-V2 (May 2024) [UNVERIFIED-PK]; MHA2MLA, Feb 2025: -92.19% KV on MHA Llama2-7B at -0.5% LongBench, ~3.2x beyond GQA-8 [REPORTED + ESTIMATE]; TransMLA, Feb 2025: -68.75% training-free; X-EcoMLA, Mar 2025: 6.4x; xKV, Mar 2025: 8x at 87.8% RULER on Llama-3.1-8B [REPORTED] | DeepSeek; Fudan; PKU; AMD; Cornell [UNVERIFIED-PK] | All per-layer or layer-group. **One latent shared by all layers, added by retrofit, is open.** YOCO, LCKV and CLA (2024) shared KV only by pretraining [UNVERIFIED-PK] |
| Cross-finetune KV | DroidSpeak, NSDI'26 [REPORTED]; Activated LoRA, IBM 2025 [UNVERIFIED-PK] | Microsoft/UChicago; IBM | Exact sharing by freezing layers adds little |
| Sparse/PIM KV | Quest, ShadowKV (2024) [UNVERIFIED-PK]; Samsung LPDDR5X-PIM, Hot Chips 2026 [REPORTED]; H2EAL; IBM StarC [REPORTED] | MIT, CMU, Samsung, IBM | Software top-k already takes 8-16x |
| Attention offload | Lamina (arXiv 2405.01814, 2024) [REPORTED] | Tsinghua | Retired-GPU option |
| Crowded 2026 field | SwiftCache, CacheWise, TraceLab, KV-offload bottlenecks (arXiv 2601-2606) [REPORTED, titles only] | academic | Must be read before filing |

**The genuine delta.** Four items, in falling order of defensibility:
1. **Client-deadline restore scheduling.** Client input events set restore deadlines in a two-class, deadline-aware NVMe queue. A send predictor bounds HBM hold time to ≤1 s per turn. Its value is 1.1-4.7 drive-eq/GPU of flash saved and the FP8 context limit raised from ~21k to ~38k tokens. This is the strongest IP.
2. **A retrofit with one cross-layer shared latent**, going beyond per-layer MLA retrofits. This is open research, and it may fail (show-stopper 2).
3. **The quantified case for deleting the host KV tier.** It serves ~5% of returns at 240 GB/GPU, and only ~55% even at 2 TB/GPU. This is a publishable result, not strong IP.
4. **A host-DRAM-minimal node spec**, co-designed so the KV job cannot migrate back into host DRAM. Its value comes from adoption, so publish it openly.

Hibernating KV to flash is **not** new: ICMS, LMCache and Mooncake already do it. Exact cross-finetune sharing is not new either.

---

## 4. Show-stoppers and how persistence could get around them

| # | Show-stopper | Number | Workaround path |
|---|---|---|---|
| 1 | Long-context tail sets p99 | At 3 drive-eq: 64k FP8 p99 0.57 s and 128k FP8 1.21 s, vs a 0.30 s budget. The base mix's p99 context is ~82k [ESTIMATE; real distribution unknown] | 3x latent (64k passes at 0.18 s); 6 drive-eq for 128k latent (0.08 s); layer-wise pipelined restore (decode layer 1 while later layers stream); Cake load+recompute; a small DRAM "long-context lane" for the top few % of sessions only; Gen6 NVMe at ~28 GB/s per drive [ESTIMATE] roughly doubles the limits |
| 2 | Retrofit latent stalls | Training-free methods stall at ~2-7x. xKV is 8x at 87.8% RULER. An all-layer latent re-read by every layer cuts bandwidth only ~8x unless it stays on-chip (critic) | Per-layer-group latents (xKV-style) instead of one; stack with FP8-to-FP4 or KIVI-class 2-bit quantization; new models pretrained with MLA (DeepSeek-style) carry it natively. The diet still yields 1.5x without the latent |
| 3 | NAND writes and wear | 107-126 TB/day per GPU, ~860 TB/day per node (3x the critic's 280). Needs 3 x 15.36 TB 3-DWPD drives per GPU | Gate spills on return probability (12% of sessions never return within the TTL); dedup chunks across turns; NVMe Flexible Data Placement/ZNS to cut write amplification; pod flash shelves. The same flash is already needed in the 2026 baseline |
| 4 | Physical flash slots | 24 drive-eq per 8-GPU node, 216 per NVL72 rack. Local E1.S bays give ~2 per GPU [UNVERIFIED-PK] | The rest comes from ICMS-style pod shelves over the ~100 GB/s per-GPU NIC; 21 GB/s is ~1/5 of it. Gen6 or higher-bandwidth drives; HBF later (section 7) |
| 5 | Host DRAM is soldered or gaining jobs | Grace solders 480 GB of LPDDR5X. Vera ships ~1.5 TB/CPU (critic). Async checkpoints need ~16 B/param, so the realistic cut is 2x: 120 GB/GPU, 8.6 TB/rack, 22.7% | An OEM SKU with fewer or smaller SOCAMM-style modules; checkpoints streamed GPU-to-NVMe; for the installed base, lease the idle host DRAM as far memory (I-04908) so CPU-server purchases fall |
| 6 | Client signal eats HBM | First-keystroke prefetch: 8.2 s/turn hold, +82% HBM KV, 0.936 wafer-eq GB per conversation (worse than today) | Send predictor at m=3 with ≤0.5 false positives per turn: 0.66-1.70 s hold. Or drop the signal (B0) and keep it for long-context sessions only |
| 7 | Agent and API traffic | No typing signal; tool waits of seconds; a Sep 2026 paper says agent prefixes need a host tier that holds the whole agent pool [REPORTED]. Not modeled | The server knows when a tool call starts, and per-tool latency histories give the lead; keep KV in HBM for short waits (InferCept "preserve"); a small agent-only host tier; co-hibernate KV and sandbox (I-07651) |
| 8 | Write-read interference on shared drives | ~1.2 GB/s of writes per GPU ignored by the M/M/1 model; NVMe priority support varies by drive | Separate write and read drives; NVMe weighted-round-robin arbitration; measure it in the wear rig |
| 9 | Privacy of client signals | Typing timing is personal data | Log timing only, never content; the predictor runs on-device and emits one "prefetch now" bit; IRB review; opt-in |
| 10 | Weak economics at cost (not physics) | $18.8k of DRAM per rack at $1.48/GB | Out of scope under the mission. Bits and resources are saved at any price |

---

## 5. The decisive experiment

**Question.** Can an 8-GPU node serving real human chat drop its host-DRAM KV tier (host ≤64 GB/GPU) and hold p99 added TTFT ≤0.30 s on ≤3 Gen5 drive-eq/GPU? And does a retrofit shared latent reach ≥3x?

**Step by step**
1. **Setup (M0-M2).**
   - Fork Open WebUI and add a client "signal SDK". It emits timestamped focus, keystroke, pause, paste, hover-on-send, chip-hover, speech start/end and send events, and no content.
   - Get IRB approval through a university partner.
   - Stand up vLLM+LMCache with a GPUDirect Storage backend.
   - Reproduce scenarios A and B0 on public traces (WildChat timestamps, Mooncake trace, BurstGPT) [UNVERIFIED-PK].
   - Measure host working sets with DAMON under serving plus GDS checkpointing, to fix the real host floor.
2. **Lead-time study (M2-M6).**
   - 300-500 consenting users, 6 weeks, against a hosted open model.
   - Measure: lead per event type; the no-lead share; the gap and context-length distributions.
   - Train a send predictor and plot its hold-versus-miss curve and false-positive rate.
   - **Gate G1 (M6).**
3. **Replay testbed (M4-M10).**
   - One 8-GPU H200/B200 node with 16-24 Gen5 drives, or 8 local drives plus an NVMe-oF shelf.
   - Build the two-class restore queue: urgent restores at NVMe high priority; restores with lead are chunked and preemptible.
   - Replay the study traces, scaled up, at equal tokens/s for A, B0 and B.
   - Record p50/p90/p99 TTFT, host RSS, flash utilisation, read/write interference and SMART NAND writes.
   - Run the 12-drive wear rig in parallel at the measured write rate.
   - **Gate G2 (M10).**
4. **Shared latent (M6-M14).**
   - Distil Llama-3.1-8B into one shared cross-layer latent with decoupled RoPE dimensions, using 2-5B tokens.
   - Ablate at 3x, 6x and 12x against xKV, MHA2MLA and TransMLA on RULER and LongBench at 32-128k.
   - Do one 70B confirm run at 3x.
   - **Gate G3 (M14).**

**Facilities**
- Rented 8-GPU node with root access for cgroups, GDS and NVMe queues: Lambda, CoreWeave, Together or AWS p5 at ~$3/GPU-h [ESTIMATE].
- TACC Vista (GH200) via NSF ACCESS or the NAIRR Pilot, for a Grace-class host-lite check [UNVERIFIED-PK].
- NERSC Perlmutter or ALCF Polaris via DOE ALCC, for large replays. Local NVMe and GDS support must be checked [UNVERIFIED-PK].
- An own JBOF wear rig.
- IRB at UChicago, Berkeley or UCSD.
- No nanofab, MPW or national-lab cleanroom is needed.

**Budget (decisive core)**

| Line | $ | Basis [ESTIMATE] |
|---|---|---|
| Lead-time study: 400 x $50 incentives, hosted-model GPUs, IRB and privacy review | 45,000 | |
| Replay compute: ~3,000 node-hours | 75,000 | ~$25 per node-hour |
| Flash wear rig: 12 x 15.36 TB Gen5 plus JBOF | 36,000 | ~$3k per drive at 2026 prices |
| Latent distillation and evals: ~11,000 GPU-h plus storage | 50,000 | X-EcoMLA used ~70 MI300-hours for 1B [REPORTED]; an 8B run is ~200-500 H100-h |
| **External total** | **206,000** | Founder time is in section 6. The card's figure was $280k |

**Pre-set pass/fail numbers**

| Gate | Date | PASS | FAIL |
|---|---|---|---|
| G1 | M6 | One predictor reaches HBM hold ≤1.0 s/turn at ≤0.5 false positives/turn | No predictor does: drop the signal and continue with B0 |
| G2 | M10 | p99 added TTFT ≤0.30 s vs a 240 GB/GPU baseline at equal tokens/s, ≤3 drive-eq/GPU, ≤3 DWPD (SMART) | p99 >0.30 s at the measured context mix with 3 drive-eq: the FP8 host-lite claim fails |
| G3 | M14 | ≥3x vs FP8 GQA at ≤1 point loss in RULER average at 32k | <2x at that loss: the latent arm fails |

---

## 6. The $1M, 24-month plan

The plan starts in January 2027 (M0).

| Quarter | Milestones | Gate |
|---|---|---|
| Q1 2027 | SDK, IRB, testbed up; A and B0 reproduced on public traces; DAMON host floor measured; FTO search; provisional 1 filed | G0: host floor ≤120 GB/GPU |
| Q2 2027 | Lead-time study live; send predictor trained | G1 (M6) |
| Q3 2027 | Measured-trace replay; deadline queue; wear rig; latent runs start; provisional 2 filed | |
| Q4 2027 | Host-tier hit-rate paper submitted (MLSys/OSDI/ATC); latent ablations | G2 (M10) |
| Q1 2028 | 70B confirm run; provisional 3 filed before the preprint | G3 (M14) |
| Q2 2028 | Two-node integrated demo; one GB300 validation week; OEM talks on a depopulated SKU | |
| Q3 2028 | 4-week opt-in live beta; open-source LMCache/vLLM plugins; OCP spec draft; provisionals converted to PCT | M20 demo |
| Q4 2028 | Raise $10-50M on the measured numbers | |

**Budget allocation ($882k)**

| Line | $ |
|---|---|
| Two founders, 22 months loaded ($9k/month each) | 396,000 |
| ML-systems contractor or PhD intern, 12 months part-time | 60,000 |
| Lead-time study | 45,000 |
| Replay compute | 75,000 |
| Wear rig | 36,000 |
| Latent distillation and evals | 50,000 |
| Integrated live demo (16 GPUs x 6 weeks) | 60,000 |
| IP: 3 provisionals plus FTO search and opinion | 45,000 |
| Travel (OCP Summit, MLSys/OSDI), tooling, storage | 35,000 |
| Contingency (~10%) | 80,000 |
| **Total** | **882,000** |

The ~$118k left under $1M is reserve, or the optional PIM top-k look on UPMEM or Ramulator2.

**Team**

The mission's "device or circuit expert" seat becomes an ML-systems seat. All affiliations below are [UNVERIFIED-PK].
- **Founder 1, serving systems.** A vLLM or LMCache committer. Recruit from the UChicago group of Junchen Jiang (LMCache, CacheGen, DroidSpeak), the Berkeley Sky Computing Lab of Ion Stoica (vLLM, LMArena), UCSD (Hao Zhang; Yiying Zhang for InferCept), or CMU (Zhihao Jia, Beidi Chen).
- **Founder 2, ML research, owns the latent.** Recruit from Cornell (Mohamed Abdelfattah: xKV, Palu), the PKU TransMLA group (Muhan Zhang), the Fudan MHA2MLA authors, AMD's X-EcoMLA team, or the MIT Han Lab (Quest, DuoAttention).
- **Part-time.**
  - An HCI/privacy researcher for the study.
  - A storage advisor from the SSD side of Solidigm, Micron, Kioxia or Samsung.
  - An OCP hardware advisor from a hyperscaler server team.
- **Programs.**
  - NSF ACCESS, the NAIRR Pilot and DOE ALCC for free cycles.
  - NSF SBIR Phase I as non-dilutive top-up.
  - LMArena as a possible large-scale trace partner.

**IP strategy**

- **First filing (M2): client-deadline KV restore.** Client input events set deadlines in a two-class flash scheduler. Urgent restores preempt. A send-predictor gate bounds HBM hold.
- **Second filing:** wear-aware append-only KV spill, gated by predicted return probability, with chunk dedup across turns.
- **Third filing:** a retrofit recipe for one shared cross-layer latent, with per-layer absorbed up-projections and decoupled RoPE dimensions.
- **Publish defensively:** the host-DRAM-lite node spec (OCP) and the hit-rate analysis.
- **Licensing:** open-source the plugins under the projects' Apache-2.0 licence [UNVERIFIED-PK]. License the patents to hardware and storage vendors.
- **FTO risks** (no patent search has been run, so the first ~$15-20k goes to one):
  - NVIDIA: Dynamo KVBM, ICMS, BlueField-4 KV placement;
  - Huawei and Alibaba: CachedAttention, reuse prediction;
  - Moonshot AI: Mooncake;
  - WEKA, VAST, Pure: KV storage;
  - Microsoft and Google: schedulers;
  - Samsung: PIM and CXL KV;
  - IBM: aLoRA;
  - DeepSeek: MLA.
- **Prior art that narrows claims:** speculation rules and prefetch-on-hover, LiveMind, CachedAttention.

---

## 7. After the demo

**Who partners or licenses.** There is no fab in this path.

| Partner | Their interest |
|---|---|
| NVIDIA (Dynamo/ICMS team) | Most likely partner or acquirer. The client-deadline queue slots into Dynamo and NIXL |
| Storage vendors: WEKA, VAST, Pure, DDN | A deadline API turns their "prefetch is impossible" stance into a feature |
| Flash makers: Solidigm, Kioxia, Micron, Samsung, SK hynix | They sell 3 x 15.36 TB of 3-DWPD flash per GPU, and may fund the wear study. The Sandisk/SK hynix High Bandwidth Flash (HBF) effort (OCP spec Aug 2026, samples 2H26 [REPORTED]) is a natural home: an in-package flash KV tier |
| DRAM makers: Micron, Samsung, SK hynix | Mixed interest. In a supply-limited market, freed host bits move to HBM and servers rather than going unsold. Micron and SK hynix also sell SSDs and SOCAMM modules |
| Foundries | Matter only for the optional PIM top-k, e.g. Samsung's LPDDR5X-PIM, mass production end-2026/early-2027 [REPORTED] |
| Display makers | Have no role |
| OEMs/ODMs: Supermicro, Dell, HPE, Lenovo, Foxconn, Quanta, Wiwynn | Build the depopulated host-lite SKU |
| Inference providers: Together, Fireworks, Baseten, CoreWeave, Lambda; hyperscalers via OCP | Deploy it |

**What $10-50M buys**
- 15-30 engineers and a production-grade stack covering chat, agents and API traffic.
- A 2-4 rack GB300/Vera Rubin pilot with an inference provider, measuring DRAM per served user in production.
- An open family of latent-retrofitted models (8B to 400B).
- An OEM co-designed host-lite board.
- Agent-workload extensions (I-07651).
- The PIM top-k and retired-GPU options evaluated on real long-context traffic.

**Standards**
- OCP: a host-DRAM-lite node spec.
- NVMe: deadline/priority classes and FDP profiles for KV.
- JEDEC: SOCAMM depopulation options.
- A "prefetch hint" field in the OpenAI-compatible chat API [SPECULATIVE].
- SNIA, for the KV-storage semantics.

---

## 8. Resources and America

- **Scarce inputs.** The diet moves capacity from DRAM to NAND. Per conversation it deletes 0.097-0.226 GB of DRAM (B0 to D0). Per GB avoided, that saves ~0.42 kWh of fab electricity and ~2.6 L of water [ESTIMATE, A2]: 5,322 kWh and 32,947 L per rack at 64 GB host-lite.
  - Each HBM GB avoided saves ~3x the DDR5 wafer area. HBM dies are 35-45% larger, and TSV packaging yields are 20-30% lower [REPORTED].
  - NAND is not free either: enterprise SSD prices are up ~2.3-2.8x in 2026 [REPORTED]. But the 2026 baseline already buys the same flash.
- **EUV.** Memory not bought includes the EUV layers of 1c DRAM and HBM. 3D NAND needs no EUV [UNVERIFIED-PK]. The diet itself needs none.
- **Energy in use.** Freed host DRAM saves ~1.9 kW per rack at 0.15 W/GB [UNVERIFIED]. The 216 drive-eq per rack draw ~3 kW at ~15 W average each [ESTIMATE, not in the model]. This is a wash against a no-flash design, and a ~1.9 kW saving against the 2026 baseline, which carries the flash already.
- **Water and power at fabs.** Micron's Clay, NY complex is projected at ~16 billion kWh/yr and up to 48 million gallons/day [REPORTED]. Every EB not needed defers that build-out.
- **U.S. manufacturability.**
  - The diet needs no fab and runs on any U.S. GPU cluster. National-lab clusters (NERSC, ORNL, TACC) can host the studies.
  - Honest caveat: the bits it moves go to NAND made mostly in Japan, Korea, Singapore and China [UNVERIFIED-PK]. So it cuts total memory exposure rather than onshoring the bits that remain.
  - Its strategic value for America is that fewer imported DRAM and HBM bits are needed per AI user while U.S. DRAM capacity is still being built.

---

## 9. Kill criteria

These are physics and measurement kills. Each names its revival condition. M0 is January 2027.

| # | Kill (deadline) | Measurable condition | Revival condition |
|---|---|---|---|
| 1 | Host-lite floor (2027-03-31, M3) | DAMON working set under serving plus GDS checkpointing is >160 GB/GPU, so the saving is <15% of rack DRAM | Checkpoint staging moved to GPU-to-NVMe streaming; floor re-measured ≤120 GB/GPU |
| 2 | Host-tier deletion argument (2027-06-30, M6) | In measured traces, a 240 GB/GPU LRU host tier serves >30% of returning turns (model: 5%) | Gap distribution shifts long again in broader traffic, e.g. consumer rather than power users |
| 3 | Client signal (2027-06-30, M6) | No send predictor reaches HBM hold ≤1.0 s/turn at ≤0.5 false positives/turn. Kills the signal only; B0 continues | On-device speech or intent models predict send with ≤0.5 s error |
| 4 | FP8 host-lite (2027-10-31, M10) | p99 added TTFT >0.30 s at the measured context mix with 3 drive-eq/GPU, or flash >3 DWPD by SMART | The latent passes G3, or Gen6 drives (~28 GB/s) are on the testbed |
| 5 | Latent arm (2028-02-29, M14) | <2x vs FP8 GQA at ≤1 point loss in RULER average at 32k | Per-layer-group latents or pretrained MLA models reach ≥3x |
| 6 | **Full concept** (2028-02-29, M14) | Measured p99 context >~40k tokens at FP8 **and** the latent <2x, so a DRAM KV tier must return | ≥3x shared latent, or Gen6 NVMe roughly doubling the FP8 limit |
| 7 | Integrated demo (2028-08-31, M20) | 4-week live beta misses p99 added TTFT ≤0.30 s, or DRAM per conversation is <1.5x lower than A at equal tokens/s | Fix the measured cause (interference, slots) and re-run within one quarter |

---

## 10. Sources

All URLs below are logged in `research/sources/*.jsonl`, mainly `dos-ai-memory-diet.jsonl`. Most were seen only as search snippets.

**Rack memory and flash KV tiers**
- https://www.supermicro.com/zh_tw/products/rack/srs-gb300-nvl72
- https://www.nvidia.com/en-in/data-center/gb300-nvl72/
- https://catalog.redhat.com/en/hardware/system/detail/307917
- https://pubs.lenovo.com/gb300-nvl72/server_features
- https://nvidianews.nvidia.com/news/nvidia-bluefield-4-powers-new-class-of-ai-native-storage-infrastructure-for-the-next-frontier-of-ai
- https://www.barchart.com/story/news/36894738/nvidia-bluefield-4-powers-new-class-of-ai-native-storage-infrastructure-for-the-next-frontier-of-ai
- https://www.nasdaq.com/press-release/nvidia-bluefield-4-powers-new-class-ai-native-storage-infrastructure-next-frontier-ai
- https://www.solidigm.com/products/technology/icmsp-ai-inference-is-flash-storage-problem.html
- https://nand-research.com/research-note-improving-inference-nvidias-inference-context-memory-storage-platform/
- https://nand-research.com/?p=5081
- https://www.weka.io/article/why-prefill-has-become-the-bottleneck-in-inference-and-how-augmented-memory-grid-helps
- https://www.gmicloud.ai/blog/gmi-cloud-achieves-4x-llm-performance-boost-with-tensormesh
- https://pypi.org/project/thaw-vllm/0.3.2/

**Human gaps, KV reuse, prefetch and agents**
- https://arxiv.org/pdf/2605.18825
- https://arxiv.org/html/2506.02634v4
- https://arxiv.org/abs/2403.19708
- https://arxiv.org/html/2406.14319v2
- https://github.com/ChuangtaoChen-TUM/LiveMind
- https://arxiv.org/html/2410.03065v2
- https://chatpaper.com/paper/351013
- https://icml.cc/media/icml-2026/Slides/61148.pdf
- https://arxiv.org/pdf/2606.30560
- https://arxiv.org/pdf/2606.16135
- https://arxiv.org/pdf/2606.16824
- https://arxiv.org/pdf/2601.19910

**KV compression, sharing and offload**
- https://arxiv.org/abs/2502.14837v1
- https://arxiv.org/html/2502.07864v5
- https://arxiv.org/html/2503.11132v1
- https://arxiv.org/abs/2503.18893
- https://proceedings.mlr.press/v235/liu24bz.html
- https://www.usenix.org/conference/nsdi26/presentation/liu-yuhan
- https://arxiv.org/html/2405.01814v1
- https://www.tomshardware.com/pc-components/dram/hot-chips-2026-samsung-makes-lpddr5x-smart-with-logic-unit-in-memory-lpddr5x-pim-is-3-01x-faster-than-lpddr5x-in-ai-inference-with-8x-the-bandwidth
- https://www.trendforce.com/news/?p=63155
- https://arxiv.org/pdf/2508.16653
- https://research.ibm.com/publications/starc-selective-token-access-with-remapping-and-clustering-for-efficient-llm-decoding-on-pim-systems

**HBM, flash roadmap, prices and resources**
- https://www.tomshardware.com/tech-industry/semiconductors/micron-says-the-silicon-gap-between-hbm-and-ddr5-is-widening-with-every-generation
- https://www.trendforce.com/presscenter/news/20240318-12081.html
- https://www.sandisk.com/company/newsroom/press-releases/2026/2026-02-25-sandisk-and-sk-hynix-begin-global-standardization-of-next-generation-memory-solution-high-bandwidth-flash-hbf
- https://dev.to/breachprotocol/high-bandwidth-flash-became-a-spec-today-not-a-product-you-can-buy-48p1
- https://capitalandcompute.net/memory-prices/server/
- https://datacenterdisk.com/reports/server-ram-market-report-2026
- https://www.trendforce.com/presscenter/news/20260202-12911.html
- https://itldc.com/es/blog/server-ram-ssd-market-update-2026
- https://nyruralwater.org/node/3506
- https://www.wskg.org/news/2023-08-06/micron-estimates-needing-up-to-48-million-gallons-of-water-a-day-aiming-to-achieve-100-water-conservation
