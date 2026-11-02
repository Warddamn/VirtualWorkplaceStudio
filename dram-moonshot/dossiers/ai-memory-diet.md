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

**(revised after red team)** EV 15 (S1 x P3 x D5). FINAL STATUS: **DOWNGRADED** (section 11). Revised thesis: delete the host-DRAM KV tier for *human-chat* traffic only, keep a right-sized host tier for agent/API traffic (gap-aware tiering), and claim ~1.4x fewer DRAM GB per human-chat conversation (1.17x in wafer terms), not 4.5x. The single all-layer latent is killed; the latent and the client signal are now optional, prior-art or moot legs.

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

**Verdicts (revised after red team; the v1 verdicts above are kept for the record)**

- **PHYSICALLY POSSIBLE? Yes, for host-lite; no for the single all-layer latent.**
  - With program/erase interference, WAF 1.1 (FDP) and NAND-side accounting, 70B GQA human chat needs 3.5 Gen5 drive-eq/GPU fresh and 5.0 at end of life with one drive throttled (2.3-3.3 with the client signal). MLA-class models need <=2 local drives.
  - A latent shared by all 80 layers reads 26.7x more KV per decode step than GQA FP8 (~3 sessions/GPU): killed.
- **STEP CHANGE IF IT WORKS? No. Axis: DRAM bits per served AI chat user, 1.40x (1.17x wafer-eq).**
  - Full KV path (host + SSD controller DRAM + shelf heads), p99-sized flash, 64 GB host floor. 1.24x / 1.11x at a 120 GB floor; 1.50x / 1.19x for MLA models with local drives only.
  - Agent/API traffic needs host DRAM: fleet gain ~1.17x at 50% agent capacity. S = 1.
- **PROVABLE WITH $1M? Yes for the technical claim (~$205k external, mixed human + agent traces, FDP and pre-cycled drives, one MLA model, by M12); no for adoption.**

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

> **(revised after red team)** The model now carries a RED-TEAM REVISIONS block. Changes that move numbers in this section:
> - NAND program/erase die-time is in the flash queue and WAF is 1.1 (FDP). At 3 drive-eq/GPU, p99 added TTFT is A 0.35 s, B0 0.38 s (was 0.33 s), B 0.13 s. B0 needs **3.5 drive-eq/GPU** for p99 <= 0.30 s (was 3.2), and 5.0 at end of life with one drive throttled. NAND-side DWPD on 3 x 15.36 TB is 2.98 (B0) and 2.56 (B).
> - Active sessions are also capped by GPU FLOPs (~143 per GPU for 70B dense at 30 tok/s plus prompt prefill). A and B0 are unchanged (HBM still binds at 89). The latent scenarios become compute-bound: C 1.62x, D0 and D 2.43x DRAM GB per conversation (1.93x wafer-eq), down from 3.00x and 4.50x (3.57x).
> - The single all-layer latent is dropped (26.7x more decode reads); the latent rows assume a per-layer latent.
> - Full KV-path DRAM (SSD controller DRAM plus shelf heads) and p99-sized flash cut B0's gain to **1.40x DRAM / 1.17x wafer-eq**.
> - Agent/API traffic is modeled (model section 11.6). The host tier catches 84-90% of agent returns, so it is kept for agents and deleted only for human chat.
>
> Revised scenario table (base mix, 3 drive-eq/GPU):
>
> | Scenario | Conv./GPU | p99 added TTFT | DRAM GB/conv. | Wafer-eq GB/conv. | Gain: DRAM / wafer |
> |---|---|---|---|---|---|
> | A | 1,820 | 0.35 s | 0.290 | 0.607 | 1.00x / 1.00x |
> | B0 | 1,820 | 0.38 s (0.30 s at 3.5 drive-eq) | 0.193 | 0.510 | 1.50x / 1.19x; full path 1.40x / 1.17x |
> | B | 1,553 | 0.13 s | 0.227 | 0.597 | 1.28x / 1.02x |
> | C (latent, compute-bound) | 2,945 | 0.07 s | 0.179 | 0.375 | 1.62x / 1.62x |
> | D0 | 2,945 | 0.08 s | 0.120 | 0.315 | 2.43x / 1.93x |
> | D | 2,945 | 0.02 s | 0.120 | 0.315 | 2.43x / 1.93x |
>
> Correction to 2.4's "the diet adds ~0 flash against 2026 practice": that holds against a flash-tier baseline (A). Against a DGX-class rack with 3.84 TB/GPU and no KV flash, 3 drive-eq/GPU add ~25 NAND wafers per rack while freeing ~4.1 DRAM wafer-equivalents. Per served conversation, total wafer starts still fall ~2.5x, because the flash tier lets a GPU serve 1,820 conversations instead of ~378. That credit belongs to the flash tier, which is prior art. The diet's own increment is ~1.04x in total DRAM + NAND wafer starts.
>
> Correction to 2.5: the client signal saves 1.2 drive-eq/GPU at the base mix (2.3 vs 3.5) and ~1.7 at end of life. It saves no DRAM, and it is moot for MLA models.

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

**(revised after red team, RT-IND-01, RT-CIRC-02)**
- Delta 1 is demoted from "strongest IP" to an optional efficiency feature. Operators who own both client and server can ship it in weeks. The FTO search (LiveMind, CachedAttention, speculation rules) now comes first, at M0-M1, and the feature is filed only if it clears; otherwise it is published defensively as an open API hint.
- Delta 2 (the all-layer latent) is killed.
- Delta 3 becomes "gap-aware tiering": delete the host tier for human chat, keep it for agents. It is the measured result that remains, and it is publishable but weak IP.

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
| 7 | Agent and API traffic (modeled after red team, model 11.6) | No typing; second-scale tool waits. Today's host tier catches 84-90% of agent returns. Host-lite with agents on flash needs 5.8-7.3 drive-eq/GPU for agent p99 | **Adopted:** gap-aware tiering keeps a host tier for agents (103/143/187/240 GB/GPU at 25/50/75/100% agent share). Also: server-side tool-latency deadlines (not yet modeled); InferCept "preserve"; KV+sandbox hibernation (I-07651) |
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

### 5R. Revised decisive experiment (revised after red team)

**Question.** Serve a measured mix of human-chat and agent/API traffic on one 8-GPU node, at equal tokens/s, against a 240 GB/GPU LRU host-tier baseline. Use gap-aware tiering: human-chat KV bypasses the host and goes HBM to flash; the host keeps 64 GB/GPU plus the measured agent working set. Does it hold p99 added TTFT ≤0.30 s on both turn types, at ≤3.5 Gen5 drive-eq/GPU (2 local plus a shelf), on drives as they will be at end of life? Does it cut full-KV-path DRAM per human-chat conversation by ≥1.4x? And does the same hold on an MLA-class model with ≤2 local drives?

**Steps**
1. **Setup and traces, M0-M3.**
   - Stand up vLLM+LMCache over GPUDirect Storage with a gap-aware placement policy.
   - Get traces under NDA from a production partner (LMArena or an inference provider), plus public chat traces (Mooncake, BurstGPT, Qwen-Bailian).
   - Generate agent trajectories with real tool latencies by running coding and browsing agents on rented GPUs.
   - Measure the host floor with DAMON, and bill the full KV path: host RSS, SSD controller DRAM and shelf heads.
   - **Gate G0.**
2. **Replay, M3-M10.** Run A, B0, B and B_gap at measured agent shares, on 70B GQA FP8 and on one MLA-class model (DeepSeek-V3 or Kimi K2 FP8 on 8x H200/B200). Record p50/p99 TTFT per turn type under the full read-plus-write mix. **Gate G2.**
3. **Wear and thermal rig, M4-M10.**
   - FDP-capable drives, with placement by expiry class.
   - NAND-side writes and WAF from the vendor or OCP log page.
   - 4 used drives pre-cycled to ≥80% of rated wear.
   - A 24 h soak at 35 °C inlet with drive temperatures logged.
   - One week on a GB200/GB300 tray: Grace LPDDR5X power per GB and E1.S thermals. TACC Vista GH200 serves as a free cross-check.
4. **Optional legs, M6-M12.**
   - A reduced lead-time study with 100-150 users. It matters only for GQA long contexts; G1 is unchanged.
   - A decode-tokens/s-at-batch plus RULER check of prior-art per-layer latent retrofits (TransMLA, MHA2MLA) on 8B and 70B. This is an adopt-or-drop decision, not IP.

**Budget (decisive core, external)**

| Line | $ [ESTIMATE] |
|---|---|
| Traces: partner data handling plus agent-trajectory generation | 20,000 |
| Reduced lead-time study, optional | 15,000 |
| Replay compute (~4,000 node-hours at ~$25; GQA, MLA, hybrid; human plus agent mixes) | 100,000 |
| Wear and thermal rig: 12 Gen5 drives (≥4 FDP), 4 pre-cycled used drives, thermal and power instrumentation | 45,000 |
| GB200/GB300 tray week | 10,000 |
| Per-layer latent check (decode tokens/s at batch plus RULER) | 15,000 |
| **External total** (was $206k; the FTO search moves to M0-M1 inside section 6's IP line) | **205,000** |

**Pre-set pass/fail**

| Gate | Date | PASS | FAIL |
|---|---|---|---|
| G0 | M3 | Host floor ≤64-120 GB/GPU, with the full-path DRAM bill in hand | Floor >160 GB/GPU: host-lite saving <15% |
| G1 (optional) | M6 | Hold ≤1.0 s/turn at ≤0.5 false positives/turn | Drop the signal |
| G2 | M10 | p99 ≤0.30 s for human **and** agent turns at ≤3.5 drive-eq/GPU (fresh) and ≤5 (pre-cycled, 35 °C soak). NAND-side WAF ≤1.25 and ≤3 NAND DWPD. Full-path DRAM ≥1.4x per human-chat conversation | p99 fails at ≤5 drive-eq end of life, or full-path ratio <1.25x: FP8 host-lite fails |
| G2b | M12 | MLA-class model: p99 ≤0.30 s with ≤2 local drives/GPU, ratio ≥1.4x | MLA run needs a DRAM KV tier |
| G3' | M12 | A prior-art per-layer latent gives decode tokens/s at batch ≥ GQA FP8 at ≤1 point RULER loss | Drop the latent leg (no effect on host-lite) |

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
| Micron, Samsung, SK hynix (DRAM) | Mixed: in a shortage, freed host bits move to HBM and servers; they also sell SSDs and SOCAMM. **(revised after red team, RT-PROC-03)** Freed LPDDR5X bits relieve conventional server and LPDDR demand, not HBM, whose 2026-28 output is gated by TSV, stacking and test capacity. The HBM-relief claim is withdrawn |
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
- **Energy in use (revised after red team, RT-DEV-03).** Host memory here is LPDDR5X at ~0.04 W/GB, so the freed 12.7 TB saves ~0.4-0.6 kW per rack, not 1.9 kW. The 216 drives draw 3.2-5.4 kW. Net: ~0.5 kW saved against a flash-tier baseline; +1.5-3.2 kW against a DGX-class rack with one drive per GPU, which serves ~4.8x fewer conversations per GPU. The original v1 line follows. Freed host DRAM saves ~1.9 kW per rack at 0.15 W/GB [UNVERIFIED]. The 216 drive-eq draw ~3.2 kW at ~15 W each [ESTIMATE, not in the model]. Net: ~1.3 kW more than a no-flash design (3.2 - 1.9 kW); ~1.9 kW saved against the 2026 baseline, which carries the same flash.
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

**Kill criteria (revised after red team).** Rows 1-7 stand except where amended here.

| # | Kill (deadline) | Measurable condition | Revival condition |
|---|---|---|---|
| 4R | FP8 host-lite (2027-10-31), amends row 4 | p99 added TTFT >0.30 s for human **or** agent turns at ≤3.5 drive-eq/GPU fresh, or ≤5 pre-cycled at 35 °C inlet. Or >3 **NAND-side** DWPD, or WAF >1.25 with FDP | MLA-class models (≤2 local drives), Gen6 drives, program-suspend firmware |
| 5R | Latent arm, amends row 5 | **Killed now (RT-CIRC-02):** the single all-layer latent reads 26.7x GQA's KV per decode step | A serving regime where decode is not HBM-bandwidth-bound. Per-layer latents stay as prior-art adoption only |
| 7R | Full-path ratio (2027-10-31), amends row 7 | Host RSS + SSD controller DRAM + shelf heads give <1.25x fewer DRAM GB per human-chat conversation | Large-IU or ZNS drives, plus the host floor brought to ≤64 GB/GPU by GPU-to-NVMe checkpoints |
| 8 | Agent placement (2027-10-31) | Gap-aware tiering cannot hold agent p99 ≤0.30 s without a host tier ≥240 GB/GPU on mixed nodes | Segregated pools: host-lite for human chat, full host tier for agents |
| 9 | Hybrid-model endurance (2028-02-29), flash tier generally | Recurrent-state rewrite drives >3 NAND DWPD at ≤3.5 drive-eq even with FP8 state and selective spill | High-endurance flash for the state, or state recompute from a cached prefix |

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

**Red-team response sources** (`research/sources/resp-ai-memory-diet.jsonl`)
- https://arxiv.org/abs/2503.11665
- https://developer.nvidia.com/blog/introducing-nvidia-bluefield-4-powered-inference-context-memory-storage-platform-for-the-next-frontier-of-ai/
- https://the-decoder.com/ai-is-becoming-ais-biggest-customer-as-agentic-token-usage-jumps-14x-on-openrouter/
- https://www.cudocompute.com/products/nvidia-gb300/ (logged by rt-CIRC)

---

## 11. Red-team outcome

Four reviewers attacked this dossier on 2026-11-02: DEV (device physics), PROC (process), CIRC (circuits) and IND (industry). Their 16 objections are in `research/redteam/rt_*.json`; the owner's responses are in `research/redteam/responses_ai-memory-diet.json`.
- The model was re-run with a RED-TEAM REVISIONS block (`models/ai-memory-diet.py`; exit 0). New results are in section 11 of `research/stage3/ai-memory-diet_model_output.md`, cited below as "model 11.x".
- Three WebSearches were used.
- Neither top-up idea flagged by the critics applies. I-12302 (plate-strip sensing) and I-12627 (series write transistors) are DRAM-cell fixes, and this concept has no cell.

**Dispositions:** 0 REFUTED, 8 ACCEPTED-MITIGATED, 7 ACCEPTED-DOWNGRADE, 1 ACCEPTED-KILL (the single all-layer latent leg).

### 11.1 Objections

| Id | Severity | Disposition | One-line action |
|---|---|---|---|
| RT-CIRC-ai-memory-diet-01 | MAJOR | ACCEPTED-DOWNGRADE | Gap-aware tiering: host tier kept for agents, deleted for chat; gain scales with chat share |
| RT-CIRC-ai-memory-diet-02 | MAJOR | ACCEPTED-KILL | All-layer latent killed (26.7x decode reads); per-layer = prior art |
| RT-CIRC-ai-memory-diet-03 | MAJOR | ACCEPTED-MITIGATED | Full-path DRAM bill: 1.40x (1.47x large-IU); meets >=1.4x |
| RT-CIRC-ai-memory-diet-04 | MINOR | ACCEPTED-MITIGATED | P/E die-time in queue: B0 needs 3.5 drive-eq; measured in G2 |
| RT-DEV-ai-memory-diet-01 | MAJOR | ACCEPTED-MITIGATED | FDP placement by expiry class, WAF 1.1; GO reads NAND-side writes |
| RT-DEV-ai-memory-diet-02 | MINOR | ACCEPTED-MITIGATED | Pre-cycled-drive arm; EOL needs 4.2 drive-eq (5.0 with throttling) |
| RT-DEV-ai-memory-diet-03 | MINOR | ACCEPTED-DOWNGRADE | Energy claim cut from 1.9 kW to ~0.5 kW per rack |
| RT-DEV-ai-memory-diet-04 | MINOR | ACCEPTED-MITIGATED | 24 h 35 °C soak; throttle margin priced at 4.2-5.0 drive-eq |
| RT-IND-ai-memory-diet-01 | MAJOR | ACCEPTED-DOWNGRADE | Signal demoted to optional; FTO first; defensive publication |
| RT-IND-ai-memory-diet-02 | MAJOR | ACCEPTED-DOWNGRADE | S 2 -> 1: 1.40x DRAM / 1.17x wafer-eq; latent no longer counted |
| RT-IND-ai-memory-diet-03 | MAJOR | ACCEPTED-DOWNGRADE | Adoption not provable; add host-size sweep on mixed traces |
| RT-IND-ai-memory-diet-04 | MAJOR | ACCEPTED-MITIGATED | Host-lite holds at 1.50x on MLA/hybrid; latent and signal moot; plan re-baselined |
| RT-IND-ai-memory-diet-05 | MINOR | ACCEPTED-MITIGATED | Production + agent traces lead; GB200/GB300 tray week added |
| RT-PROC-ai-memory-diet-01 | MAJOR | ACCEPTED-DOWNGRADE | Resource claim withdrawn: ~1.04x total wafer starts vs A |
| RT-PROC-ai-memory-diet-02 | MAJOR | ACCEPTED-DOWNGRADE | S 2 -> 1, EV 30 -> 15 |
| RT-PROC-ai-memory-diet-03 | MINOR | ACCEPTED-MITIGATED | HBM-relief claim withdrawn; restated as conventional-DRAM relief |

### 11.2 Redesigns adopted

1. **Gap-aware tiering replaces "delete the host rung"** (RT-CIRC-01, RT-IND-03).
   - Human-chat KV goes HBM to flash and bypasses the host.
   - Agent/API sessions, whose tool waits are seconds long and are known on the server, keep a host tier sized to their working set: 103/143/187/240 GB/GPU at 25/50/75/100% agent share.
   - Where pools can be segregated, chat pools ship host-lite and agent pools keep today's host memory.
2. **Latent leg** (RT-CIRC-02, RT-IND-04).
   - The single all-layer latent is killed.
   - Per-layer latents are prior art (MHA2MLA, TransMLA). They are compute-bound at 1.62x active sessions, and moot on MLA-native models.
   - The latent becomes a $15k adopt-or-drop check. It is no longer research or IP.
3. **Flash provisioning** (RT-DEV-01, -02, -04, RT-CIRC-03, -04).
   - FDP drives with placement by expiry class: WAF ~1.1, NAND-side accounting.
   - Large-indirection-unit or ZNS drives, which cut SSD controller DRAM 16x.
   - The flash queue now counts program/erase die-time.
   - Flash is sized for p99: 3.5 drive-eq/GPU fresh, 5.0 at end of life with one drive throttled. That is 2 local drives plus shelf for GQA, and ≤2 local for MLA-class models.
   - The rig adds pre-cycled drives and a 35 °C soak.
4. **Client signal demoted to optional** (RT-IND-01).
   - It saves flash (1.2 drive-eq at the base mix), not DRAM, and is moot for MLA models.
   - FTO comes first; the fallback is defensive publication and an open API hint field.
5. **Metrics and baselines** (RT-PROC-01, RT-CIRC-03).
   - Three baselines: DGX-class no-flash, A (2026 flash tier) and B0.
   - DRAM is counted across the full KV path: host, SSD controllers and shelf heads.
   - Total DRAM + NAND wafer starts are reported per 1,000 conversations.
6. **Claims withdrawn** (RT-DEV-03, RT-PROC-01, RT-PROC-03).
   - Energy: 1.9 kW becomes ~0.5 kW per rack.
   - "Saves fab resources": the diet is ~1.04x, close to neutral.
   - "Freed host bits relieve HBM": it relieves conventional DRAM/LPDDR only.
   - The headline 4.5x / 3.6x is withdrawn.

### 11.3 Revised numbers [ESTIMATE, model section 11]

| Quantity | Dossier v1 | Revised |
|---|---|---|
| B0 p99 added TTFT at 3 drive-eq/GPU | 0.33 s | 0.38 s (program/erase die-time, WAF 1.1) |
| B0 drive-eq/GPU for p99 ≤0.30 s: fresh / EOL + throttled | 3.2 / n.a. | 3.5 / 5.0 (with signal: 2.3 / 3.3) |
| NAND DWPD, B0 on 3 x 15.36 TB | 2.72 (host writes, WAF 1) | 2.98 at WAF 1.1; 5.41 at WAF 2.0 |
| B0 vs A, DRAM GB/conv (wafer-eq) | 1.50x (1.19x) | 1.40x (1.17x) full path, p99-sized; 1.47x large-IU; 1.24x at 120 GB floor |
| D0 vs A (latent + host-lite) | 4.50x (3.57x) | 2.43x (1.93x), compute-bound; latent not credited to the diet |
| All-layer latent, active sessions/GPU | assumed 266 | ~3 (26.7x decode reads): killed |
| Agent share 25/50/75/100%: host GB/GPU, gain | not modeled | 103/143/187/240 GB; 1.35x/1.22x/1.11x/1.00x |
| Fleet gain at 50% agent capacity (full path) | n.a. | 1.17x |
| MLA-class model: B0 gain, drive-eq, p99 at 2 drives | n.a. | 1.50x, ~0.6 drive-eq, 0.05 s |
| Hybrid model: host writes | n.a. | 402 TB/day per GPU (state rewrite), ~9.6 drive-eq at 3 DWPD, same for A |
| Energy saved per rack vs flash baseline | 1.9 kW | 0.4-0.6 kW |
| Total wafer starts per 1,000 conv.: DGX no-flash / A / B0 | n.a. | 1.037 / 0.427 / 0.411 |

### 11.4 Revised step-change claim

On the axis of DRAM bits per served AI chat user, the diet's own lever is **~1.4x fewer DRAM GB per human-chat conversation, or 1.17x in DDR5-wafer terms**. That counts host, SSD controller DRAM and shelf heads, with flash sized for p99.
- It is 1.47x with large-IU drives, 1.50x on MLA-class models with local drives only, and 1.24x if the host floor is 120 GB.
- It scales with the human-chat share of serving capacity: ~1.17x fleet-wide at 50% agent/API capacity.
- It is not a step change: **S = 1** on FINAL_CONCEPTS' scale (EV 30 → 15).
- The latent and client signal no longer count toward it.

### 11.5 Revised decisive experiment

See section 5R.
- **Traces.** Measured human-chat plus agent/API traces (a production partner, public traces and generated agent trajectories) replayed on one 8-GPU node with gap-aware tiering.
- **GO conditions:**
  - p99 ≤0.30 s for **both** turn types at ≤3.5 drive-eq/GPU fresh, and ≤5 on pre-cycled drives during a 24 h 35 °C soak;
  - NAND-side WAF ≤1.25 and ≤3 NAND DWPD on FDP drives;
  - full-KV-path DRAM ≥1.4x lower per human-chat conversation;
  - G2b: the same on one MLA-class model with ≤2 local drives.
- **Measurements the reviewers showed were missing:**
  - agent/API mix and tool-latency distribution;
  - NAND-side writes;
  - read-plus-write interference;
  - end-of-life and thermal p99;
  - SSD and shelf DRAM;
  - LPDDR5X W/GB on a GB200/GB300 tray;
  - a host-size sweep (240/750/1,500 GB) to test whether bigger host tiers sit idle in serving;
  - decode tokens/s at batch for any latent.
- **Cost and schedule:** ~$205k external; G0 M3, G2 M10, G2b and G3' M12. This stays inside the $882k, 24-month plan; the IP line now funds the FTO search first.

### 11.6 Revised verdicts

- **PHYSICALLY POSSIBLE?** Yes for host-lite with gap-aware tiering. It involves no device physics and fits 3.5-5.0 Gen5 drive-eq/GPU (≤2 local for MLA models). No for the single all-layer latent.
- **STEP CHANGE IF IT WORKS?** No.
  - DRAM bits per served chat user fall 1.40x (1.17x wafer-eq) on human-chat pools.
  - The fleet figure is ~1.17x at 50% agent capacity. S = 1.
- **PROVABLE WITH $1M?** Partly.
  - Yes for the technical claim: ~$205k, by M12, no fab.
  - No for "bits not bought", which needs NVIDIA or a hyperscaler to ship host-lite pool SKUs.

### 11.7 FINAL STATUS: DOWNGRADED

The concept is not killed: nothing in physics blocks host-lite for human chat. It survives full-path DRAM accounting, write amplification, interference, end-of-life and throttling margins, and re-runs on MLA and hybrid models. But the reviewers were right on the size of the prize, for four reasons:
- Agent/API traffic, a large and fast-growing share, genuinely uses host DRAM.
- The all-layer latent that carried the 4.5x is physically ruled out, and the per-layer version is prior art.
- The client signal saves flash, not DRAM.
- On total wafer starts the diet is close to neutral.

What remains is a measured ~1.2-1.45x DRAM-per-user lever for human-chat pools, plus a cheap, publishable host-tier study. It stays in the portfolio as a low-cost demand hedge, not as a step-change bet.

**Revival condition for STANDS:** deleting host DRAM alone can never reach S = 2. Even at zero host DRAM the wafer-eq gain caps at (288 x 3 + 240)/(288 x 3) = 1.28x. A step change needs a lever on HBM per conversation, and the red-team runs point to one [SPECULATIVE]:
- On compute-bound MLA-class nodes, ~136 GB/GPU of HBM holds no active KV (model 11.7).
- Chat-pool GPUs with ~2/3 of today's HBM, plus host-lite, would give ~1.7x in wafer terms: (192 x 3 + 64) vs (288 x 3 + 240).
- That would need such a GPU SKU, and a measured p99 with idle KV on flash.

This is the persistence path. It should be scored as a new concept, not credited to this one.
