# AI MEMORY DIET: delete DRAM's jobs in the AI racks that cause the shortage

NEW DRAM Stage 3 dossier. Author: agent `dosw-ai-memory-diet`, 2026-11-02.

Inputs: `models/ai-memory-diet.py` (re-run today, exit 0, output matches `research/stage3/ai-memory-diet_model_output.md`); `research/stage3/ai-memory-diet_notes.md`; `research/assumptions/dos-ai-memory-diet.md`; the card in `research/stage3/FINAL_CONCEPTS.json`; Stage 2 critiques in `research/ideas10k/stage2/stage2_results.jsonl`.

Tags:
- [REPORTED]: from a logged source, usually seen only as a search snippet.
- [ESTIMATE]: model arithmetic.
- [UNVERIFIED-PK]: prior knowledge, no URL.
- [SPECULATIVE]: not yet shown by anyone.

The dossier writer ran no WebSearch. Web facts come from the research phase's 6 searches (snippets only; see notes). No patent search has been run for this concept.

---

## 0. Header

**Name:** AI MEMORY DIET.

**Thesis:** Human chat leaves a GPU's KV cache idle ~95% of the time, so stop parking it in host DRAM. Stream it between HBM and flash on client deadlines, shrink it ~3x with a trained latent, and ship AI nodes with a fraction of today's host DRAM.

**Rank:** 10 of 10, EV 30 (S2 x P3 x D5).

**Category:** system/architecture; the portfolio's demand hedge. No new cell.

**Lineage:** the system-lens "AI Memory Diet", taken whole. It has no device-lens counterpart. The chief demoted PIM top-k to an option.

| Id | Idea | Creativity technique | Stage 2 verdict | Role |
|---|---|---|---|---|
| I-10877 | Host-DRAM-lite AI servers | Wishful thinking / ideal final result | ADVANCE 63.2 | Core: host DRAM cut to 64-120 GB/GPU |
| I-08555 | Typing-indicator KV prefetch | Scale and time shifting | ADVANCE 72.1 | Core: client-deadline flash restore |
| I-07651 | Mycologist's spores: hibernate idle agents | Perspective shift / personas | HOLD 65.6 | Core, agent variant |
| I-04878 | One latent per token for every layer | Assumption inversion | ADVANCE 60.6 | Core: shared cross-layer latent |
| I-11326 | Cross-finetune KV sharing | Scarcity and constraint as engine | HOLD 64.1 (innovation DROP) | Demoted to a platform rule |
| I-09070 | In-DRAM KV top-k | Failure mining | ADVANCE 64.7 | Option |
| I-00766 | Retired GPUs as KV servers | SCAMPER-Combine | ADVANCE 64.1 | Option |
| I-04908 | Lease idle host DRAM as far memory | Assumption inversion | HOLD 63.5 | Bridge for soldered boards |
| I-10963 | Recompute-as-correction for KV | Wishful thinking / ideal final result | HOLD 63.5 | Fallback for misses |
| I-07637 | KV as an implicit neural field | Perspective shift / personas | HOLD 68.8 | Research option beyond 3x |

**Verdicts**

- **PHYSICALLY POSSIBLE? Yes.**
  - No device physics is involved. The limits are flash bandwidth (16.6-21 GB/s per GPU), NAND writes (107-126 TB/day per GPU) and the p99 restore time of long contexts.
  - All three fit in 3 Gen5 drive-equivalents per GPU, up to ~38k tokens at FP8 or ~113k with a 3x latent [ESTIMATE].
- **STEP CHANGE IF IT WORKS? Partly. Axis: DRAM bits per served AI chat user.**
  - Host-lite frees 22% (critic) to 33% (model) of rack DRAM. That is 1.50x fewer DRAM GB per conversation, or 1.19x in wafer terms.
  - With a 3x latent the factor is 4.5x (3.6x in wafer terms), but most of the latent is prior art.
- **PROVABLE WITH $1M IN 24 MONTHS? Yes for the technical claim; no for "bits not bought".**
  - ~$206k of external spend settles all three gates by month 14 on rented GPUs, with no fab.
  - Whether OEMs ship depopulated boards is a partner decision.

---

## 1. How it works

A chatbot keeps "working notes" on the conversation, called its KV cache: ~160 kB per token for a 70B-class model, so ~2 GB for a 13k-token chat. The notes must sit in the GPU's own memory (HBM) while the model writes its ~10 s reply. Then you read, think and type, for a median of ~110 s between turns [REPORTED, arXiv 2605.18825].

During that gap, today's servers move the notes down a ladder: HBM, then host DRAM, then flash. Each AI rack carries ~17 TB of host DRAM against ~21 TB of HBM. But with so many people chatting, a 240 GB/GPU host tier keeps any one conversation for only ~9 s. Only ~5% of returning turns find their notes there; flash already serves the other ~95%.

The diet makes four changes:
1. **Delete the host rung.** Notes go HBM-to-flash and back over GPUDirect Storage. Host DRAM shrinks to the operating system and runtime: 64 GB/GPU, or 120 GB/GPU in the critic's case.
2. **Give flash a deadline.** The chat app sends a content-free "about to send" hint, from a typing pause, the cursor reaching Send, or the end of speech. A two-class flash queue restores urgent sessions first and streams the rest in the background.
3. **Shrink the notes ~3x** with a distilled shared latent that each layer expands back into keys and values.
4. **Publish the node spec**, so servers can ship with less host DRAM.

```
TODAY (per GPU)                              THE DIET (per GPU)
+-----------+  evict   +--------------+      +-----------+                    +-----------------+
| HBM 288GB | -------> | host DRAM    |      | HBM 288GB | <== GPUDirect ==>  | flash: 3 Gen5   |
| weights + | <------- | 240 GB tier, |      | weights + |  deadline queue    | drive-eq/GPU    |
| live KV   |  ~5% of  | holds ~9 s   |      | live KV   |  (urgent first)    | (3 x 15.36 TB)  |
+-----------+  returns +--------------+      +-----------+                    +-----------------+
      ^                      | evict               ^
      +-- ~95% of returns -- [flash]               +-- "about to send" hint (timing only)
                                              host DRAM: 64 GB/GPU, OS + runtime, no KV tier
```

---

## 2. The physics and the numbers

All numbers are [ESTIMATE] outputs of `models/ai-memory-diet.py` unless tagged otherwise.

### 2.1 KV geometry and the human gap

- **KV per token.** For a 70B GQA model with FP8 KV it is 2 x 80 layers x 8 heads x 128 x 1 B = **160 KiB**. A 3x latent cuts it to 53.3 KiB.
  - 32k tokens = 5.24 GB, or 1.75 GB latent. 128k tokens = 20.97 GB, or 6.99 GB latent.
  - One Gen5 drive (~14 GB/s [UNVERIFIED-PK]) restores 32k in 0.37 s and 128k in 1.50 s, or 0.12 s and 0.50 s latent.
- **The human gap.** The model fits a log-normal to the reported median of 110 s and P80 of 372 s [REPORTED].
  - The fit has a mean of 314 s. Its P99 is 3,192 s, against 2,207 s reported, which is conservative.
  - With a 600 s warm TTL, 87.9% of turns return, and E[min(gap, TTL)] = 195 s.
  - Idle-but-returning KV is therefore 195/10 = **19.5x** the active KV. The card assumed ~3-5x, from a 30 s median.

### 2.2 Per-GPU scenarios

These runs use the base context mix, a log-normal with median 8k and mean 13.0k tokens.
- **Active sessions.** The HBM KV budget is 288 x 0.9 - 70 GB of weights = 189 GB. At 2.13 GB per session, that holds 89 active sessions.
- **Conversations.** 89 x (10 + 195)/10 = 1,820 per GPU.

| Scenario | Host GB/GPU | Conv./GPU | p99 added TTFT | DRAM GB/conv. | Wafer-eq GB/conv. (HBM x3) | Gain: DRAM / wafer |
|---|---|---|---|---|---|---|
| A. Today: host tier + flash, FP8 | 240 | 1,820 | 0.30 s | 528/1,820 = 0.290 | 1,104/1,820 = 0.607 | 1.00x / 1.00x |
| B0. Host-lite, no signal | 64 | 1,820 | 0.33 s | 0.193 | 0.510 | 1.50x / 1.19x |
| B. Host-lite + client prefetch | 64 | 1,557 | 0.11 s | 0.226 | 0.596 | 1.28x / 1.02x |
| C. Today + 3x latent | 240 | 5,459 | 0.10 s | 0.097 | 0.202 | 3.00x / 3.00x |
| D0. Host-lite + latent, no signal | 64 | 5,459 | 0.11 s | 0.064 | 0.170 | 4.50x / 3.57x |
| D. Full diet | 64 | 4,713 | 0.03 s | 0.075 | 0.197 | 3.89x / 3.08x |

Three corrections to the card:
1. **Host-lite needs no client signal at short contexts.** B0 misses the budget by 0.03 s; 3.2 drive-eq/GPU closes it.
2. **The signal costs HBM.** Prefetched KV waits ~1.7 s per turn (+17% HBM KV), so B beats A by only 1.02x in wafer terms. It pays only if hold stays under ~1 s.
3. **The latent supplies 3x of D0's 4.5x.** The diet's own share is 1.50x.

### 2.3 Rack and fleet (GB300 NVL72 class)

A rack holds 72 x (288 GB HBM + 240 GB LPDDR5X) = **38.0 TB** of DRAM [REPORTED; NVIDIA lists 37 TB].

| Host-lite GB/GPU | Freed per rack | % of rack DRAM | $ at $1.48/GB | $ at $20/GB | Fab kWh | Water |
|---|---|---|---|---|---|---|
| 64 (model) | 72 x 176 GB = 12.7 TB | 33.3% | $18,755 | $253,440 | 5,322 | 32,947 L |
| 120 (critic) | 8.6 TB | 22.7% | $12,787 | $172,800 | 3,629 | 22,464 L |
| 160 | 5.8 TB | 15.2% | $8,525 | $115,200 | 2,419 | 14,976 L |

- **Fleet.** 10,000 racks (a scaling unit, not a forecast) avoid 0.086-0.127 EB. That is 0.13-0.19% of ~68 EB/yr of world DDR5-equivalent output.
- **HBM per conversation** falls 2.59x, from 0.158 GB in A to 0.061 GB in D. Each HBM GB costs ~3x the DDR5 wafer area [REPORTED, Micron].
- **Honest scale.** At the $1.48/GB production cost, the freed DRAM is worth ~$19k per rack. The dollar case depends on shortage prices; the bit savings do not.

### 2.4 Flash: the supply law and the critics' numbers

When HBM capacity binds, flash must refill the whole HBM KV pool once per generation time.

- **Reads.** 189 GB / 10 s x 0.879 returning = **16.6 GB/s per GPU**. With HBM hold and false positives it is 21 GB/s.
  - This does not depend on bytes per token.
  - The latent cuts flash load per conversation 3x (13.7 to 4.6 MB/s), not per drive.
- **Writes.** ~8.9k new tokens/s x 160 KiB = 1.45 GB/s = **125.6 TB/day per GPU** (107 TB/day with prefetch). With prefetch that is **~860 TB/day per 8-GPU node** (~1,000 without).
- **Drives.** The binding constraint is bandwidth: 21.3/(14 x 0.6) = 2.54 drive-equivalents. Endurance needs 107.4/(15.36 x 3) = 2.33, and capacity 0.31. So each GPU needs **3 x 15.36 TB drives rated at 3 DWPD**, used at 2.33 DWPD.

**Critic corrections carried:**
- NAND writes are ~860 TB/day per node, **3x** the Stage 2 figure of ~280.
- Flash bandwidth is ~17 GB/s **per GPU**, not per node: 133-170 GB/s per node.
- Today's 2026 design (A: an LMCache-disk or ICMS-style tier) needs the same 3 drive-eq/GPU. **The diet adds ~0 flash against 2026 practice.**

**Memory plus flash bill per 1,000 concurrent conversations** (DRAM $20/GB, HBM 3x, flash $0.20/GB): A $17,200; B0 $15,265 (-11%); D0 $5,088 (-70%).

### 2.5 Sensitivity

**Fixed context length**, p99 added TTFT at 3 drive-eq/GPU (with signal / without):

| Context | FP8 | Latent 3x | Verdict, FP8 / latent |
|---|---|---|---|
| 16k | 0.13 / 0.22 s | 0.04 / 0.07 s | GO / GO |
| 32k | 0.27 / 0.44 s | 0.08 / 0.15 s | GO / GO |
| 64k | 0.57 / 0.88 s | 0.18 / 0.29 s | NO-GO / GO |
| 128k | 1.21 / 1.76 s | 0.37 / 0.59 s | NO-GO / NO-GO |

The longest single length that passes is ~38k tokens with the signal and ~21k without. With the latent it is ~113k and ~63k.

**No-lead share, the card's "key unknown".** Base-mix p99 by drive count:

| Drive-eq/GPU | p99 at 0% no-lead | p99 at 60% no-lead | Passes up to |
|---|---|---|---|
| 3 | 0.10 s | 0.17 s | every share tested |
| 2.5 | 0.16 s | 0.28 s | 60% |
| 2 | 0.37 s | 0.63 s | none |

**The card's "≥80% coverage" threshold is the wrong form.** p99 is set by flash utilisation and by the restore time of the p99 context. Lead coverage matters only when flash is lean.

**Drive-eq/GPU needed for p99 ≤ 0.30 s**, with signal / without: base FP8 2.2 / 3.2; 64k FP8 3.9 / 6.1; 128k FP8 5.5 / 10.1. The signal is worth 1.1-4.7 drive-eq of flash per GPU, plus the long contexts it rescues. It saves no host DRAM.

**Prefetch policy.** Restoring at the first keystroke holds KV 8.22 s per turn (+82% HBM KV), giving 0.936 wafer-eq GB per conversation, worse than today's 0.607. A send predictor (m=3, 0-0.5 false positives) holds 0.66-1.70 s (+7-17%), giving 0.548-0.601.

**Bigger host tier (baseline).** 750 GB/GPU serves 25.2% of returns; 2 TB/GPU serves only 54.6%, at 1.267 DRAM GB per conversation.

**Price.** Freed DRAM per rack: $18.8k at $1.48/GB; $452k at $35.70/GB retail.

### 2.6 Against 1-beta DDR5

The diet leaves the DRAM chip unchanged. What changes is how many 1-beta bits one served user consumes.

| Metric | 1-beta rack today (A) | Host-lite (B0) | Host-lite + latent (D0) |
|---|---|---|---|
| DRAM $/GB | $1.48 | $1.48 | $1.48 |
| DRAM GB per conversation | 0.290 | 0.193 | 0.064 |
| Wafer-eq GB per conversation | 0.607 | 0.510 | 0.170 |
| Wafer-eq $ per conversation at $1.48/GB | $0.90 | $0.75 | $0.25 |
| Per-bit cell gain needed to match | 1.0x | 1.19x | 3.57x |

### 2.7 GO / NO-GO

The test replays consented chat traces on one 8-GPU node. Host memory is capped at ≤64 GB/GPU, with no host KV tier.

**GO if all three hold:**
1. p99 added TTFT ≤0.30 s against a 240 GB/GPU host-tier baseline, at equal tokens/s and ≤3 drive-eq/GPU. The model predicts 0.33 s without the signal and 0.11 s with it.
2. Flash wear ≤3 DWPD. The model predicts 2.33.
3. For the signal to stay in the design: HBM hold ≤1.0 s per turn. If flash is trimmed to 2.5 drive-eq/GPU, the no-lead share must also stay ≤60%.

**Latent gate:** ≥3x over FP8 GQA at ≤1 point loss in RULER average at 32k.

**NO-GO for the full concept:** p99 fails at the measured context mix even with the latent and 3 drive-eq/GPU, which would force a DRAM KV tier back.

---

## 3. What is new versus prior art

| Component | Prior art (date) | Gap left |
|---|---|---|
| GPU-direct data paths (host-lite) | NVIDIA GPUDirect Storage, nvCOMP/DALI GPU decode, DeepSpeed ZeRO-Infinity/FastPersist NVMe paths (named by Stage 2 critics) [UNVERIFIED-PK] | The mechanisms exist. Critics found no published host-DRAM-minimal node spec or fleet host-DRAM study |
| Flash KV tier | NVIDIA ICMS on BlueField-4 (CES, Jan 2026), with Dell, HPE, Pure, VAST and WEKA [REPORTED] | **KV-to-flash is mainstream.** The diet cannot claim it |
| Tiered KV | Dynamo KVBM (2025) [UNVERIFIED-PK]; NIXL [REPORTED]; LMCache [UNVERIFIED-PK]; Mooncake, FAST'25 [UNVERIFIED-PK]; TensorMesh: SSD gives ~4x TTFT vs ~1.4x RAM-only (vendor) [REPORTED] | All keep a host-DRAM tier. None uses client deadlines |
| Disk prefetch | CachedAttention, USENIX ATC'24 (arXiv 2403.19708) [REPORTED] | Scheduler hints give <1 s of lead |
| Reuse prediction | Alibaba "KVCache Cache in the Wild" (Jun 2025); gap-aware eviction, arXiv 2605.18825 (May 2026) [REPORTED] | Server-side only |
| Typing as a signal | LiveMind, TUM (Jun 2024) [REPORTED]; web prefetch-on-hover [UNVERIFIED-PK]. WEKA (2026) calls KV prefetch "almost impossible" [REPORTED] | Text-level, not KV placement. **Closest prior art** |
| Agents, fallback | InferCept, ICML'24 [UNVERIFIED-PK]; TVCache, ICML'26; agent host-tier sizing (Sep 2026); Cake load+recompute (Oct 2024) [REPORTED] | Agents may need a host tier |
| Latent KV | DeepSeek-V2 MLA (May 2024) [UNVERIFIED-PK]; MHA2MLA (Feb 2025): -92.19% KV at -0.5% LongBench, ~3.2x beyond GQA-8; TransMLA: -68.75% training-free; X-EcoMLA: 6.4x; xKV: 8x at 87.8% RULER [REPORTED] | All per-layer or layer-group. Training-free cross-layer retrofits exist: xKV, and MiniCache (2024, named by the Stage 2 critic) [UNVERIFIED-PK], stalling near 2-7x. **A retrofit single latent shared by all layers has not been shown.** YOCO, LCKV and CLA (2024) were pretrained [UNVERIFIED-PK] |
| Cross-finetune | DroidSpeak, NSDI'26 [REPORTED]; Activated LoRA, IBM 2025 [UNVERIFIED-PK] | Freezing adds little |
| Sparse / PIM | Quest, ShadowKV [UNVERIFIED-PK]; Samsung LPDDR5X-PIM (Hot Chips 2026); H2EAL; StarC; Lamina [REPORTED] | Software top-k already gives 8-16x |

The 2026 field is crowded: SwiftCache, CacheWise, TraceLab and a KV-offload bottleneck study [REPORTED, titles only] must be read before filing.

**The genuine delta**, from most to least defensible:
1. **Client-deadline restore scheduling.**
   - Client events set deadlines in a two-class NVMe queue, and a send predictor caps HBM hold at ≤1 s.
   - It saves 1.1-4.7 drive-eq of flash per GPU and lifts the FP8 context limit from ~21k to ~38k tokens.
   - It is the strongest IP.
2. **A single shared cross-layer latent added by retrofit.** This is open research, and it may fail.
3. **The quantified case for deleting the host tier.** The tier serves ~5% of returns at 240 GB/GPU and ~55% even at 2 TB. This is publishable, but weak IP.
4. **A host-DRAM-minimal node spec.** It is worth something only if adopted, so publish it.

---

## 4. Show-stoppers and how persistence could get around them

| # | Show-stopper | Number | Workaround |
|---|---|---|---|
| 1 | Long-context tail | 64k FP8 p99 0.57 s; 128k 1.21 s vs a 0.30 s budget. The base mix's p99 context (~82k) is a guess | Latent (64k at 0.18 s); 6 drive-eq (128k latent at 0.08 s); layer-pipelined restore; Cake load+recompute; small DRAM lane for the top few % of sessions; Gen6 NVMe (~28 GB/s [ESTIMATE]) |
| 2 | Retrofit latent stalls | Training-free methods stall at 2-7x. An all-layer latent re-read per layer cuts bandwidth only ~8x unless held on-chip (critic) | Layer-group latents; add FP4 or 2-bit KIVI; MLA-pretrained models. Without the latent the gain is still 1.5x |
| 3 | NAND wear | 107-126 TB/day per GPU; ~860 TB/day per node | Spill gated on return probability (12% never return); chunk dedup; NVMe FDP/ZNS; pod shelves. The 2026 baseline needs the same flash |
| 4 | Flash slots | 24 drive-eq per node, 216 per rack. Local bays give ~2 per GPU [UNVERIFIED-PK] | ICMS-style pod shelves: 21 GB/s is ~1/5 of a ~100 GB/s GPU NIC; Gen6; HBF |
| 5 | Soldered or busy host DRAM | Grace solders 480 GB. Vera has ~1.5 TB/CPU and checkpoints need ~16 B/param (critic). Realistic cut 2x: 8.6 TB/rack, 22.7% | OEM SKU with fewer modules; GPU-to-NVMe checkpoints; lease idle installed DRAM (I-04908) |
| 6 | Signal eats HBM | First-keystroke prefetch: 8.2 s hold; 0.936 wafer-eq GB per conversation | Send predictor at m=3: 0.66-1.70 s. Or drop the signal (B0) |
| 7 | Agent and API traffic (not modeled) | No typing; second-scale tool waits; agents may need a host tier [REPORTED] | Tool-call start is known on the server; per-tool latency gives the lead; InferCept "preserve"; small agent tier; KV+sandbox hibernation (I-07651) |
| 8 | Write-read interference | ~1.2 GB/s of writes per GPU, not in the M/M/1 model | Split read and write drives; NVMe WRR arbitration; measure it in the rig |
| 9 | Signal privacy | Typing timing is personal data | Timing only; on-device predictor emits one bit; IRB; opt-in |
| 10 | Economics at cost (not physics) | $18.8k per rack at $1.48/GB | Out of scope; bits are saved at any price |

---

## 5. The decisive experiment

**Question.** Can an 8-GPU node serving real human chat drop its host KV tier (host ≤64 GB/GPU) and hold p99 added TTFT ≤0.30 s on ≤3 drive-eq/GPU? And does a retrofit shared latent reach ≥3x?

**Steps**
1. **Setup, M0-M2.** Fork Open WebUI with a "signal SDK" that logs focus, keystroke, pause, paste, hover-on-send, speech and send timestamps, never content. Get IRB approval. Stand up vLLM+LMCache on GPUDirect Storage. Reproduce A and B0 on WildChat, Mooncake and BurstGPT traces [UNVERIFIED-PK]. Measure the host floor with DAMON.
2. **Lead-time study, M2-M6.** 300-500 consenting users for 6 weeks. Measure lead per event type, the no-lead share, and the gap and context distributions. Train a send predictor and plot hold versus miss. **Gate G1.**
3. **Replay testbed, M4-M10.** One 8-GPU H200/B200 node with 16-24 Gen5 drives, or 8 local plus an NVMe-oF shelf. Build the two-class preemptive restore queue. Replay A, B0 and B at equal tokens/s; record p50/p90/p99 TTFT, host RSS, flash utilisation, interference and SMART writes. Run the wear rig alongside. **Gate G2.**
4. **Shared latent, M6-M14.** Distil Llama-3.1-8B into one cross-layer latent with decoupled RoPE dimensions (2-5B tokens). Ablate 3x, 6x and 12x against xKV, MHA2MLA and TransMLA on RULER and LongBench at 32-128k. Confirm at 3x on 70B. **Gate G3.**

**Facilities.** No nanofab or MPW is needed.
- A rented 8-GPU node with root access: Lambda, CoreWeave, Together or AWS p5, at ~$3/GPU-h [ESTIMATE].
- TACC Vista (GH200), via NSF ACCESS or the NAIRR Pilot, for a Grace-class check.
- NERSC Perlmutter or ALCF Polaris via DOE ALCC, for large replays [UNVERIFIED-PK].
- An in-house JBOF wear rig.
- An IRB at UChicago, Berkeley or UCSD.

**Budget (decisive core)**

| Line | $ [ESTIMATE] |
|---|---|
| Lead-time study (400 x $50 incentives, hosted model, IRB and privacy review) | 45,000 |
| Replay compute (~3,000 node-hours at ~$25) | 75,000 |
| Wear rig (12 x 15.36 TB Gen5 at ~$3k; the ~$5-10k JBOF chassis comes from section 6 contingency) | 36,000 |
| Latent distillation and evals (~11,000 GPU-h). X-EcoMLA took ~70 MI300-h for 1B [REPORTED] | 50,000 |
| **External total** (founder time in section 6; the card said $280k) | **206,000** |

**Pre-set pass/fail**

| Gate | Date | PASS | FAIL |
|---|---|---|---|
| G1 | M6 | Hold ≤1.0 s/turn at ≤0.5 false positives/turn | Drop the signal; continue with B0 |
| G2 | M10 | p99 added TTFT ≤0.30 s vs the 240 GB/GPU baseline, at equal tokens/s, ≤3 drive-eq/GPU and ≤3 DWPD | p99 >0.30 s at the measured mix: FP8 host-lite fails |
| G3 | M14 | ≥3x at ≤1 point RULER-average loss at 32k | <2x: the latent arm fails. 2-3x: partial; re-run the model's context limits at the measured factor |

---

## 6. The $1M, 24-month plan

The start is January 2027 (M0).

| Quarter | Milestones | Gate |
|---|---|---|
| Q1 2027 | SDK, IRB, testbed; A and B0 reproduced; host floor measured; FTO search; provisional 1 | G0: floor ≤120 GB/GPU |
| Q2 2027 | Lead-time study; send predictor | G1 |
| Q3 2027 | Measured-trace replay; deadline queue; wear rig; latent starts; provisional 2 | |
| Q4 2027 | Hit-rate paper to MLSys/OSDI/ATC; latent ablations | G2 |
| Q1 2028 | 70B confirm; provisional 3 before the preprint | G3 |
| Q2 2028 | Two-node integrated demo; one GB300 week; OEM talks | |
| Q3 2028 | 4-week opt-in beta; open-source plugins; OCP spec draft; PCT filings | M20 demo |
| Q4 2028 | Raise $10-50M | |

**Budget ($882k)**

| Line | $ |
|---|---|
| Two founders, 22 months at $9k/month each, loaded | 396,000 |
| ML-systems contractor or PhD intern, part-time | 60,000 |
| Decisive core (section 5) | 206,000 |
| Integrated demo (16 GPUs x 6 weeks) | 60,000 |
| IP: 3 provisionals, FTO search and opinion | 45,000 |
| Travel, tooling, storage | 35,000 |
| Contingency | 80,000 |
| **Total** | **882,000** |

The ~$118k left is reserve, or a PIM top-k look (UPMEM, Ramulator2).

**Team.** The mission's "device or circuit expert" seat becomes an ML-systems seat. Affiliations are [UNVERIFIED-PK].
- **Founder 1, serving systems:** a vLLM or LMCache committer, from UChicago (Junchen Jiang: LMCache, DroidSpeak), Berkeley Sky Lab (Ion Stoica: vLLM), UCSD (Hao Zhang; Yiying Zhang) or CMU (Zhihao Jia, Beidi Chen).
- **Founder 2, ML research, owns the latent:** from Cornell (Mohamed Abdelfattah: xKV), PKU (Muhan Zhang: TransMLA), the Fudan MHA2MLA authors, AMD's X-EcoMLA team or the MIT Han Lab.
- **Part-time:** an HCI/privacy researcher; an SSD advisor from Solidigm, Micron, Kioxia or Samsung; an OCP advisor from a hyperscaler.
- **Programs:** NSF ACCESS, NAIRR, DOE ALCC, NSF SBIR. LMArena is a possible trace partner.

**IP strategy.**
- **File first (M2):** client-deadline KV restore. Client events set deadlines in a two-class flash scheduler, and a send-predictor gate bounds HBM hold.
- **Then:**
  - return-probability-gated, wear-aware spill with cross-turn chunk dedup;
  - the shared-latent retrofit recipe, with absorbed per-layer up-projections and decoupled RoPE dimensions.
- **Publish defensively:** the node spec and the hit-rate analysis.
- **Open-source** the plugins under Apache-2.0 [UNVERIFIED-PK], and license the patents to vendors.
- **FTO risks.** No search has been run, so it comes first (~$15-20k). Assignees to check: NVIDIA (KVBM, ICMS), Huawei, Alibaba, Moonshot (Mooncake), WEKA, VAST, Pure, Microsoft, Google, Samsung (PIM/CXL KV), IBM (aLoRA) and DeepSeek (MLA).
- **Prior art that narrows the claims:** speculation rules, LiveMind and CachedAttention.

---

## 7. After the demo

There is no fab on this path.

| Partner | Interest |
|---|---|
| NVIDIA (Dynamo/ICMS) | Likeliest partner or acquirer; the queue slots into Dynamo/NIXL |
| WEKA, VAST, Pure, DDN | A deadline API fixes their "prefetch is impossible" problem |
| Solidigm, Kioxia, Micron, Samsung, SK hynix (flash) | 3 x 15.36 TB of 3-DWPD flash per GPU; may fund the wear study. Sandisk/SK hynix High Bandwidth Flash (OCP spec Aug 2026 [REPORTED]) could host an in-package KV tier |
| Micron, Samsung, SK hynix (DRAM) | Mixed: in a shortage, freed host bits move to HBM and servers; they also sell SSDs and SOCAMM |
| Foundries | Only for optional PIM top-k, e.g. Samsung LPDDR5X-PIM, mass production end-2026/early-2027 [REPORTED] |
| Display makers | No role |
| OEMs/ODMs: Supermicro, Dell, HPE, Lenovo, Foxconn, Quanta, Wiwynn | The depopulated host-lite SKU |
| Inference providers (Together, Fireworks, Baseten, CoreWeave, Lambda) and hyperscalers via OCP | Deployment |

**What $10-50M buys**
- 15-30 engineers and a production stack covering chat, agent and API traffic.
- A 2-4 rack GB300/Vera Rubin pilot that measures DRAM per served user in production.
- Open latent-retrofitted models from 8B to 400B.
- An OEM host-lite board.
- An evaluation of the PIM and retired-GPU options.

**Standards:** OCP (host-DRAM-lite node spec); NVMe (deadline classes, FDP profiles for KV); JEDEC (SOCAMM depopulation); SNIA (KV storage); a "prefetch hint" field in the OpenAI-compatible API [SPECULATIVE].

---

## 8. Resources and America

- **Scarce inputs.** The diet moves capacity from DRAM to NAND.
  - Per DRAM GB avoided: ~0.42 kWh of fab electricity and ~2.6 L of water [ESTIMATE, A2]. Per rack at 64 GB host-lite: 5,322 kWh and 32,947 L.
  - HBM avoided saves ~3x the wafer area per bit. HBM dies are 35-45% larger, with 20-30% lower TSV yield [REPORTED].
  - NAND is not free either: enterprise SSDs cost ~2.3-2.8x more in 2026 [REPORTED]. But the 2026 baseline buys the same flash.
- **EUV.** Bits not bought include the EUV layers of 1c DRAM and HBM. 3D NAND uses no EUV [UNVERIFIED-PK], and neither does the diet.
- **Energy in use.** Freed host DRAM saves ~1.9 kW per rack at 0.15 W/GB [UNVERIFIED]. The 216 drive-eq draw ~3.2 kW at ~15 W each [ESTIMATE, not in the model]. Net: ~1.3 kW more than a no-flash design (3.2 - 1.9 kW); ~1.9 kW saved against the 2026 baseline, which carries the same flash.
- **Fab water and power.** Micron's Clay, NY complex projects ~16 billion kWh/yr and up to 48 million gallons/day [REPORTED]. Lower demand per AI user defers build-out like this.
- **U.S. manufacturability.**
  - No fab is needed. The diet runs on any U.S. GPU cluster, including NERSC, ORNL and TACC.
  - Caveat: the moved bits land in NAND made mostly in Japan, Korea, Singapore and China [UNVERIFIED-PK].
  - So the diet cuts the imported DRAM and HBM bits needed per AI user while U.S. DRAM capacity is built. It does not onshore what remains.

---

## 9. Kill criteria

These are physics and measurement kills, each with a revival condition. M0 is January 2027.

| # | Kill (deadline) | Measurable condition | Revival condition |
|---|---|---|---|
| 1 | Host-lite floor (2027-03-31) | DAMON working set >160 GB/GPU under serving plus GDS checkpoints, so the saving is <15% of rack DRAM | GPU-to-NVMe checkpoint streaming brings the floor to ≤120 GB/GPU |
| 2 | Deletion argument (2027-06-30) | A 240 GB/GPU LRU host tier serves >30% of measured returns (model: 5%) | Broader consumer traffic shows long gaps again |
| 3 | Client signal only (2027-06-30) | No predictor reaches ≤1.0 s hold at ≤0.5 false positives/turn. B0 continues | On-device intent models predict send within ≤0.5 s |
| 4 | FP8 host-lite (2027-10-31) | p99 added TTFT >0.30 s at the measured mix with 3 drive-eq/GPU, or >3 DWPD by SMART | Latent passes G3, or Gen6 drives (~28 GB/s) |
| 5 | Latent arm (2028-02-29) | <2x at ≤1 point RULER-average loss at 32k | Layer-group latents or MLA-pretrained models reach ≥3x |
| 6 | **Full concept** (2028-02-29) | Measured p99 context >~40k tokens at FP8 **and** latent <2x, so a DRAM KV tier returns | A ≥3x latent, or Gen6 NVMe doubling the FP8 limit |
| 7 | Integrated demo (2028-08-31) | 4-week beta misses p99 ≤0.30 s, or DRAM per conversation is <1.5x below A at equal tokens/s | Fix the measured cause and re-run within one quarter |

---

## 10. Sources

All URLs are logged in `research/sources/*.jsonl`; most were seen as search snippets.

**Rack memory and flash KV tiers**
- https://www.supermicro.com/zh_tw/products/rack/srs-gb300-nvl72
- https://www.nvidia.com/en-in/data-center/gb300-nvl72/
- https://catalog.redhat.com/en/hardware/system/detail/307917
- https://nvidianews.nvidia.com/news/nvidia-bluefield-4-powers-new-class-of-ai-native-storage-infrastructure-for-the-next-frontier-of-ai
- https://www.solidigm.com/products/technology/icmsp-ai-inference-is-flash-storage-problem.html
- https://nand-research.com/research-note-improving-inference-nvidias-inference-context-memory-storage-platform/
- https://nand-research.com/?p=5081
- https://www.weka.io/article/why-prefill-has-become-the-bottleneck-in-inference-and-how-augmented-memory-grid-helps
- https://www.gmicloud.ai/blog/gmi-cloud-achieves-4x-llm-performance-boost-with-tensormesh

**Human gaps, reuse, prefetch, agents**
- https://arxiv.org/pdf/2605.18825
- https://arxiv.org/html/2506.02634v4
- https://arxiv.org/abs/2403.19708
- https://arxiv.org/html/2406.14319v2
- https://arxiv.org/html/2410.03065v2
- https://chatpaper.com/paper/351013
- https://icml.cc/media/icml-2026/Slides/61148.pdf
- https://arxiv.org/pdf/2606.30560
- https://arxiv.org/pdf/2606.16135
- https://arxiv.org/pdf/2606.16824
- https://arxiv.org/pdf/2601.19910

**KV compression, sharing, offload, PIM**
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

**HBM, flash roadmap, prices, resources**
- https://www.tomshardware.com/tech-industry/semiconductors/micron-says-the-silicon-gap-between-hbm-and-ddr5-is-widening-with-every-generation
- https://www.trendforce.com/presscenter/news/20240318-12081.html
- https://www.sandisk.com/company/newsroom/press-releases/2026/2026-02-25-sandisk-and-sk-hynix-begin-global-standardization-of-next-generation-memory-solution-high-bandwidth-flash-hbf
- https://dev.to/breachprotocol/high-bandwidth-flash-became-a-spec-today-not-a-product-you-can-buy-48p1
- https://capitalandcompute.net/memory-prices/server/
- https://www.trendforce.com/presscenter/news/20260202-12911.html
- https://itldc.com/es/blog/server-ram-ssd-market-update-2026
- https://nyruralwater.org/node/3506
- https://www.wskg.org/news/2023-08-06/micron-estimates-needing-up-to-48-million-gallons-of-water-a-day-aiming-to-achieve-100-water-conservation
