# B4: Architecture — do DRAM's job with less DRAM. Reasoning notes, ranking and rejected ideas

**Agent** `B4-architecture` · **Written** 2026-11-01 · **Phase** B (divergent ideation)

**Files**
- **Cards:** `research/phaseB/B4-architecture.json`: 21 cards, built and validated with python3. Every card has all 14 fields, and every evidence URL is in the source log.
- **Arithmetic:** `research/models/B4_architecture_estimates.py` has one section per card. It imports A1's `models/dram_cell_physics.py` and exits 0.
- **Sources:** `research/sources/B4-architecture.jsonl` has 55 entries. 39 come from my 15 searches; 16 are cross-references to the A1/A3 logs.
- **Assumptions:** `research/assumptions/B4-architecture.md`.

**Evidence grade.** I used all 15 WebSearch calls and no WebFetch, so every web fact comes from a search snippet. Numbers are my own arithmetic from the model. Nothing is killed for business reasons. Every rejection below names its revival condition.

---

## 1. How I aimed the lens

Phase A traces the ten bottlenecks to two root causes (A1 §10):
1. The bit is passive charge behind a leaky switch, read through a long bitline. This gates #1 (capacitor), #3 (refresh), #4 (litho) and #10 (voltage).
2. The bits sit far from compute and are read destructively in big pages. This gates #5 (interface), #6 (HBM tax) and #8 (overfetch).

An architecture lens cannot change the cell. It can change three things, and I sorted ideas by which one they pull:

| Lever | What it trades | Cards |
|---|---|---|
| **Relax the cell's spec: let a code or a policy absorb what the cell used to guarantee** | ECC bits, scrub energy and data knowledge in exchange for capacitor height, refresh rate or bits per cell | B4-01 ECC-paid capacitor, B4-02 scrub-as-refresh, B4-03 leased refresh, B4-04 significance split, B4-05 approximate MLC, B4-06 graceful forgetting, B4-08 compression-funded ECC, B4-10 Row-RAID, B4-11 erasure-coded stacks, B4-13 thermal arbitrage |
| **Need fewer bits** | Compute or algorithm in exchange for stored bits | B4-07 tensor codec, B4-09 top-k sketches, B4-17 procedural weights, B4-18 nested precision, B4-21 broadcast weight bus, B4-20 compact-then-sleep |
| **Move fewer bits, or move them more cheaply** | New interfaces, packaging or in-memory compute in exchange for pJ/bit and HBM wafer tax | B4-12 streaming die, B4-14 photonic periphery wafer, B4-15 GRS HBM-lite, B4-16 HBF weight mode, B4-19 BitNet PIM |

**The key observation behind the first lever.** Today's DRAM is designed so that every one of ~1.7×10¹⁰ cells works with no help:
- **Sensing:** a 50 mV budget, about 7σ of sense-amp offset.
- **Retention:** the 6.4σ tail cell at 85 °C.

Physics is not the reason. The interface promises bit-perfect storage with only on-die SEC as backup. On the A1 model's numbers:
- Moving the design point from 1e-12 to 1e-4 raw BER halves the capacitor.
- Moving retention from 64 ms to 1 s cuts refresh 15×.
- The price is 2–16% check bits.

NAND made this trade around 2010, and DRAM has not.

**The key observation behind the second lever.** AI data is not uniform bits:
- Exponents carry ~2.6 bits of entropy in 8.
- Mantissas tolerate BER 1e-5 and exponents do not tolerate 1e-12 (RangeGuard).
- KV mantissas tolerate 1e-4 (SHIELD).
- Weights are read every token, which by itself refreshes every row.

A memory that knows what it stores can store less, refresh less and protect less.

## 2. My ranking (physics plausibility × size of step × provability on $1M)

| Rank | Card | Step-change claim | Why it ranks here | Main physics doubt |
|---|---|---|---|---|
| 1 | **B4-01** ECC-paid capacitor | Capacitor 1,300 → 640 nm (AR 62 → 30) at 1e-4 raw BER, for +9 points of check bits. 3D/local-bitline tiers need 0.6 fF | Attacks the master bottleneck (#1) through architecture alone. Pure circuit physics, provable with an FPGA BER study plus one MPW | Whether errors at a halved margin stay iid (bitline coupling, VRT, SA drift), and the 3–10 ns decode on errored reads |
| 2 | **B4-04** Significance-split memory (with **B4-05**) | BF16 ×1.58 capacity per DRAM bit and ×3.7 less refresh (×2.28 with approximate MLC) on today's dies | NEW combination. Each half is evidenced (DFloat11, RangeGuard, SHIELD). Needs no new silicon at first | Tolerance at 70B scale and on long reasoning chains. Extra activation per sector (bank-parallel) |
| 3 | **B4-02** Scrub-as-refresh | Refresh energy ×15 lower; refresh busy 20.5% → 1.3% at 64 Gb | Cheapest decisive experiment of the lens (~$150k FPGA rig). It also measures the tail model every other card depends on | VRT bursts and pattern dependence |
| 4 | **B4-11** Erasure-coded stacks | At 95% per-die-in-stack yield: 16-high 44% → 94% (×1.9 dies per good bit) | Aims straight at the hybrid-bonding yield collapse that is delaying HBM4E/HBM5 | A power or serial-TSV short above a failed layer cannot be erasure-coded |
| 5 | **B4-09** Top-k KV via in-memory MSB-plane scoring | ×7 less KV traffic, ×8 less HBM for KV at 128k | NEW combination; PIM DRAM is shipping-class | Sketch selection quality on heads with diffuse attention |
| 6 | **B4-13** Thermal arbitrage | Retention ×3.7–18 (85 → 35 °C) → refresh ÷4–18 or Cs −30% | The measurement is cheap and decisive; it combines with B4-02 and B4-05 | Low activation energy for GIDL/TAT tail cells caps the gain at ~3–5× |
| 7 | **B4-15** GRS LPDDR HBM-lite | ~3× fewer wafers per bit than HBM at 2.7–3.4 pJ/b | Known links on known dies; the HBM tax is the biggest wafer sink | Single-ended crosstalk across hundreds of 25 Gb/s lanes |
| 8 | **B4-14** Photonic periphery wafer | 2–3 pJ/b at metre reach on DDR-density dies | Rides the periphery wafer-bonding transition the incumbents are already making | Ring thermal tuning next to a heat-sensitive array |
| 9 | **B4-21** Broadcast weight bus | 22–72% of replica HBM freed (N copies → 1) | The most original card | Lock-step skew; laser power grows with N |
| 10 | **B4-07** Tensor codec | Lossless ×1.47 capacity and bandwidth for BF16 | Simple, evidenced | Gain shrinks for FP8/FP4 |
| 11 | B4-03 Leased refresh | +5–18% decode throughput, refresh → 0 for streamed data | Easy and real, but a modest step | Restore-truncating controllers void the guarantee |
| 12 | B4-10 Row-RAID | Hammer tolerance at 3% capacity vs PRAC's up to 94% | NEW combination | Triple-row activation is unreliable on commodity chips |
| 13 | B4-16 HBF weight mode | ~3–5× HBM capacity per $ at endurance-safe pSLC | Known product; my contribution is the disturb arithmetic | Read disturb at 1e5–3e6 reads/page/day |
| 14 | B4-19 BitNet charge-sharing PIM | ×12–35 GEMV energy | Clean arithmetic | 8-row activation outside spec; analog accuracy |
| 15 | B4-08 Compression-funded ECC | ×8–16 refresh at zero capacity cost | Elegant, but B4-02 gets most of the same benefit | Mixed rows stay fast |
| 16 | B4-05 Approximate MLC (standalone) | 2× bits per cell for approximate data | Strong alongside B4-04 | Restoring an analog level after a destructive read |
| 17 | B4-20 Compact-then-sleep | Idle refresh ÷32–48 | Known pieces | Coarse PASR granularity |
| 18 | B4-12 Weight-streaming die | ~1.3–1.5× less silicon per bit than HBM | Moderate step; needs a DRAM maker | Area gain may be smaller than estimated |
| 19 | B4-18 Nested precision + self-speculation | ×1.1–1.8 effective bandwidth | Mostly ML; the hardware is just layout | Acceptance rate |
| 20 | B4-06 Graceful forgetting [SPECULATIVE] | KV refresh → 0 outside the leased window | Wild but consistent with physics | Random decay rotates K vectors |
| 21 | B4-17 Procedural weights | 4–5× fewer bits than BF16, but only 1.0–1.33× vs FP4 | Weakest: the step exists only if it beats FP4 | Accuracy vs plain quantisation (ML, not physics) |

**Strongest cross-lens pairings**
- **B4-01 + B1-04.** B1-04 is charge-transfer pre-sense. Combined, a 512-cell bitline could run on ~0.25 fF cells: ECC halves the needed signal, and pre-sense amplifies it.
- **B4-01 + B2-15.** B2-15 tolerates pattern defects with ECC; B4-01 tolerates sense margin with ECC. One shared code could pay for both.
- **B4-02 / B4-05 + B4-13.** Cool memory plus scrubbing makes multi-level DRAM on today's cell plausible.
- **B4-04 + B4-07.** These share one tensor-aware controller.
- **B4-09 + B4-15 / B4-14.** The full-KV tier is the commodity-die tier.

## 3. Rejected or folded ideas (each with its revival condition)

| Idea | Why rejected or folded | Revival condition |
|---|---|---|
| **Refresh-or-recompute**: let KV decay and recompute lost tokens | Killed on energy arithmetic. Refresh costs 1.9 µW per stored token; recompute costs ~0.14 J per token. Refresh wins for any lifetime under ~74,000 s (model card06) | Recompute energy below ~1e-6 J per token-second of retention, or a lost fraction under ~1e-5 (then it is just ECC) |
| **Whole-word approximate memory for AI** (no ECC on any bit) | Killed. Exponent flips are catastrophic even at BER 1e-12 (RangeGuard) | Exponent-free formats (INT4/INT8 with protected scales) behave like mantissas. This survives inside B4-04 |
| **Sub-page / fine-grained activation** as a standalone card | Known: Sectored DRAM gives 20% average DRAM energy, Half-DRAM, PRA. For AI streaming, activation is already amortised to 0.05–0.18 pJ/b | Random-access CPU and graph workloads, where 128× overfetch costs ~5.9 pJ per useful bit (A1 §8). A real but known lever |
| **"Consume-read" (skip restore for dead data)** | Saves only ~Cs/(Cs+Cbl) ≈ 13% of bitline energy, because the sense amp swings the bitline full-rail anyway; ~10 ns of tRAS | Short bitlines (Cs/Cbl near 1) or non-destructive gain cells, where restore dominates |
| **Via-programmed ROM chiplets for frozen weights** | 1T NOR-ROM at F = 28 nm is ~0.13 Gb/mm², below DRAM. Needs a mask re-spin per model. HBF (NAND) dominates on density | Maskless direct-write of one via layer plus monolithic 3D oxide-transistor ROM tiers at ≥8 layers |
| **Hardware dedup (HICAMP-style content-addressed memory) for AI** | Tensor-parallel sharding already stores weights once per group; KV prefix sharing is done in software (paged attention); dedup ratio on AI tensors is ~1 | Multi-tenant VM consolidation (known: KSM), or many fine-tuned variants of one base model. The second case is a delta-encoding problem; it would become a card if fleets serve 100s of LoRA/full fine-tunes |
| **Cryogenic DRAM** | A3 killed it at 77 K on refrigerator energy | B4-13 is the version that survives: ordinary liquid cooling at 30–40 °C, no fridge |
| **Rack-scale pooling (Pond-like) as its own card** | Known; a system and business lever with no physics step | Folded into B4-14 and B4-21 as context |
| **Retention-reject die rescue** as its own card | Magnitude unknown: no public data on what fraction of dies fail retention screening | Folded into B4-03 (access-guaranteed bin) and B4-04 (approximate bin). Becomes a card if a DRAM maker shares retention-yield loss data |
| **Zero-row refresh skipping / data-value-aware refresh** | DRAM data scrambling makes all-zero rows rare. Charge-minimising encoding buys only ×1.19 in interval (card02) | Folded into B4-02 as a garnish |
| **Charge-recycling / adiabatic bitlines** | Precharge to VARY/2 already recycles half the bitline charge; the remaining gain is small | Very long bitlines (≥1,024 cells) with B1-04-style sensing |
| **Low-swing PAM-n DRAM interface** as a card | Incremental: GDDR7 PAM3 already ships | Folded into B4-04: lower swing only on the mantissa lanes |
| **Inductive-coupling (ThruChip) stacking** as its own card | No evidence found this session [UNVERIFIED] | Folded into B4-11 as the revival for the serial-TSV-chain show-stopper |
| **Analog 5-bit KV cells** | At a 512-cell bitline only ~3–4 levels are resolvable (half-gap 23.6 mV = 3.3σ at 4 levels) | Folded into B4-05. Becomes 3–4 bits per cell at 128-cell bitlines (half-gap 55 mV at 4 levels) |

## 4. The biggest physics doubt across the lens

**The shape of DRAM's error tail at 1e-6 to 1e-4.**

Six cards spend the margin between today's 1e-12 design point and a code-protected 1e-4 design point: B4-01, B4-02, B4-04, B4-05, B4-08 and B4-13. Their arithmetic rests on two models:
- a Gaussian sense-offset model, reading A1's 50 mV budget as 7σ;
- a cubic power-law retention tail (BER 1.4e-5 at 1 s, 85 °C) calibrated to RAIDR-era recollections that I could not verify this session.

Two things would weaken all six cards:
- **Heavy tails or bursts:** VRT cells, pattern-dependent bitline coupling, SA offset drift with temperature.
- **A flatter retention tail:** the 1 s interval would then become ~0.3 s, and ×15 refresh would become ×5.

A $60–150k FPGA characterisation of 50–100 modern DDR5/LPDDR5 dies settles it. It should measure retention BER vs interval at 45–95 °C, BER vs reduced tRCD/voltage, VRT rates and burst statistics. It is the first experiment I would fund in Phase E.

**Second doubt.** Many AI-tolerance numbers (RangeGuard 1e-5, SHIELD 1e-4) come from 1–8B models and short tasks. Transfer to 70B+ models and long reasoning chains is unverified.

## 5. What I could not verify
- Primary papers for Smart Refresh, ESKIMO, Hi-ECC, COP, Quest, SeedLM, Matryoshka Quantization, DRISA/DrAcc and ThruChip. All are training knowledge, tagged [UNVERIFIED], with no URLs.
- NAND read-disturb limits and P/E ratings used in B4-16.
- The 1997 4-level DRAM's affiliation and details, known only through a patent citation.
- The Kelle speed-up and energy figures, which come via a mirror abstract.
- Any independent measurement of the Celestial AI pJ/bit claims.
