# RAW-BER CONTRACT: an SSD-style CXL controller, erasure-flag interface and typed pages that let weak bits ship

NEW DRAM Stage 3 dossier. Author: agent `dosw-raw-ber-contract`, 2026-11-02. Concept slug `raw-ber-contract`.

Inputs:
- Model `models/raw-ber-contract.py`, re-run 2026-11-02 (exit 0; matches `research/stage3/raw-ber-contract_model_output.md`). Re-run again after the red team with a "RED-TEAM REVISIONS" block and a new section 10 (exit 0).
- Red team: `research/redteam/rt_{DEV,PROC,CIRC,IND}.json` (19 objections on this dossier); responses in `research/redteam/responses_raw-ber-contract.json`; sources `research/sources/resp-raw-ber-contract.jsonl` (8 entries). Outcome in §11.
- Notes `research/stage3/raw-ber-contract_notes.md`; assumptions `research/assumptions/dos-raw-ber-contract.md`.
- Sources `research/sources/dos-raw-ber-contract.jsonl` (43 entries) plus A1, A2 and other dossier logs.

Tags: [REPORTED] a logged source, usually a search snippet; [ESTIMATE] model arithmetic; [UNVERIFIED-PK] prior knowledge with no logged URL; [SPECULATIVE] not yet shown by anyone.

---

## 0. Header

| Field | Value |
|---|---|
| Name | RAW-BER CONTRACT |
| One-line thesis | Do for DRAM what controllers did for NAND: publish a raw-error-rate contract (raw BER ≤1e-4 with a stated error geometry), and build a mature-node CXL controller that meets it, so weak bits, long refresh and new cells can ship. |
| Rank / EV | 4 of 10. EV 60 = S3 x P4 x D5 (ranks 2-4 sit within scoring noise) |
| Category | system/architecture |
| Lineage | Device-lens RAW-BER CONTRACT (contract framing, analog counter, flag sense stack) + system-lens ECC-Native Memory (typed pages, refresh arithmetic, experiment) + the JEDEC "ECC-native" grade from the cut Memory Bits Compact |
| Status (revised after red team) | **DOWNGRADED** (§11.7). Flag leg killed; commodity headline ~9x (DDR5, chipkill kept) instead of 15x; provable "partly" |

**Constituent ideas and their creativity-technique lineage**

| Id | Idea | Technique (facet) | Stage 2 | Role here |
|---|---|---|---|---|
| I-01312 | SSD-controller playbook: 28 nm CXL controller with page LDPC | SCAMPER-Adapt (ECC/error tolerance) | ADVANCE 67.1 | Core controller |
| I-11148 | Erasure-flagging sense amps | Scarcity and constraint as engine (sensing) | ADVANCE 67.1 | Flag interface |
| I-11559 | ECC-paid capacitor (Phase-B import of N-62) | Phase-B lens | ADVANCE 67.1 | Margin arithmetic |
| I-04613 | Shallow 1 fF pillars rescued by soft sensing + LDPC | Assumption inversion (bit storage) | HOLD 60.0 | Soft-information limit |
| I-00729 | Vertical codewords across 3D tiers | SCAMPER-Combine (manufacturing) | HOLD 60.6 | Tier-orthogonal codes |
| I-05623 | Smoke-detector analog hammer counters | Random stimulus / forced connection (sensing) | ADVANCE 63.5 | Hammer guard (reset-on-REF) |
| I-10963 | Recompute-as-correction for KV caches | Wishful thinking / ideal final result (ECC) | HOLD 63.5 | "Regenerable" page type |
| I-10420 | Compress pages, fill freed space with ECC | Manufacturing analogies (need less DRAM) | HOLD 60.6 | Page code for compressed pages |
| I-07888 | Deep-space LDPC pages, refresh at the 1% quantile | Extreme users and edge cases (leakage/refresh) | HOLD 56.5 | Relaxed refresh |
| I-09037 | LLNL zfp as a page attribute | Failure mining (need less DRAM) | ADVANCE 67.1 | "Lossy-bounded" page type |
| N-62 | ECC-paid capacitor (B4-01) | Phase-B lens "Architecture: do DRAM's job with less DRAM" | Triage ALIVE, TWIST | Margin |
| N-63 | Scrub-as-refresh (B4-02) | Same lens | Triage ALIVE, TWIST | Refresh |

**Verdicts (revised after red team; the pre-red-team verdicts are kept in §11.6)**

- **PHYSICALLY POSSIBLE? Yes** for relaxed refresh behind a code: standard coding theory on measured retention tails, no new physics. **No** for the delayed-strobe sense-amp flag as specified. Its 3.6 mV window is only τ·ln2 ≈ 14-35 ps of latch time, against 50-150 ps of strobe skew (RT-CIRC-01). That leg is killed.
- **STEP CHANGE IF IT WORKS? Yes on refresh energy and refresh-busy time, but smaller than first claimed.** Keeping chipkill (RS-8) gives:
  - **~9x on DDR5 RDIMMs at 85 C.** The range is 6-20x by tail model, 18x without the DDR5 retention derate, ~35x at 65 C and 2.9x in degraded mode.
  - **~13x on retired DDR4 behind CXL** (7.8x pessimistic).

  The original 15x gave up chipkill. At module level, refresh falls 0.98 → 0.11 W per 64 GB (DDR5's real 32 ms window), worth ~$3.9 per module over 5 years at 20% self-refresh residency. 64Gb refresh-busy time falls 18% → 2%, not 41% → 2.6%. Margin for new cells stays 1.88x (50 → 26.6 mV, Cs halved), with no flag bonus.
- **PROVABLE WITH $1M IN 24 MONTHS? Partly.**
  - **Yes:** DDR4 raw physics; DDR5 post-on-die-ECC statistics (JEDEC ECS counts, open DDR5 RDIMM testers); a failure-mode census; a per-module servo test; 1,000 h soaks. Phase 1 (decisive) costs ~$124k; the plan is $946k all-in.
  - **No:**
    - raw ECC-off 1b/1c maps, which need a vendor test mode;
    - 2e-19 per read directly, which is bounded by census plus model instead;
    - the sort flow for new dies, which stays a paper study.

---

## 1. How it works

**The problem.** A DRAM bit is a tiny leaking bucket of charge. Every one of ~17 billion buckets on a die must read correctly on its own, with only a small on-die code as backup. So every bucket is refreshed every 64 ms, because a few in a billion leak fast, and each must hold enough charge to sit ~7 noise widths (σ) above the sense amplifier's error. That rule drives the tall capacitor, the refresh energy, and the "refresh busy" time when memory cannot answer.

**How flash solved it.** NAND cells are terrible: one bit in a thousand can be wrong. Flash got cheap anyway because a controller with a strong error-correcting code sits between cells and computer, and cell makers design to an error rate the controller can absorb. DRAM never made that move.

**The contract.** RAW-BER CONTRACT is that move for DRAM. It has two halves:
1. **A published spec.** The memory may deliver up to 1 wrong bit in 10,000 (raw BER 1e-4), if its errors arrive in a stated pattern: mostly isolated bits, confined to bytes or chips, with a stated rate at which new weak cells appear (VRT growth).
2. **A controller that keeps the promise.** A CXL memory-expander chip on cheap 28/22 nm logic stores check bits, decodes every read, scrubs in the background, schedules refresh by temperature and guards against row hammer. It accepts a per-bit "unsure" flag from sense amplifiers that resolved slowly, and lets software mark pages exact, regenerable or lossy-OK.

The same box works today on commodity DDR5 (refresh 64 ms → ~0.5-1.5 s) and on retention-reject chips. Later, every new cell in this portfolio is designed to the contract rather than to 64 ms / 7σ.

```
   HOST CPU / GPU                   ordinary loads and stores, ~100-200 ns
        |  CXL link (PCIe wires)
   +----v-------------------------------------------------------------+
   | RAW-BER CONTROLLER  (28/22 nm, no EUV)                           |
   |  page-type table:  EXACT  |  REGENERABLE (CRC)  |  LOSSY (fixed)  |
   |  line code: BCH-12 or RS-8 inside the 128 check bits per line    |
   |  page code (cold pages) + SRAM write buffer (>=99% coalescing)   |
   |  refresh scheduler 0.25-2 s by temperature | scrub every 1 h     |
   |  hammer guard (RFM / PRAC)  |  flag-aware Chase decoder          |
   +----+--------------------------------------------^----------------+
        | DDR commands, relaxed REF                  | data + "unsure" flags
   +----v--------------------------------------------+----------------+
   | DRAM: today commodity / reject DDR4-DDR5; later new cells built   |
   |       to raw BER <=1e-4 (MARGIN STACK, PIXEL-STACK, AND-STACK...) |
   +-------------------------------------------------------------------+
```

**One analogy.** Today we pump every bike tyre in the city every minute because one in a billion has a fast leak. The contract pumps every tyre every 15 minutes, and a roving mechanic, the code plus the scrubber, fixes the few that went flat before anyone rides them.

---

## 2. The physics and the numbers

All figures come from `models/raw-ber-contract.py` unless tagged otherwise.

**(revised after red team)** Model section 10 changes six things:
1. **Chipkill is now the default.** The headline code is RS-8, which keeps chipkill, not BCH-12 (RT-CIRC-03).
2. **DDR5's real refresh window is 32 ms.** That is tREFI 3.9 µs × 8,192 REF. The original paired DDR5's tREFI with a 64 ms window, so its relaxed-interval tRFC loss was 2x too high and its DDR5 refresh-power baseline 2x too low.
3. **DDR5 retention is derated 0.5x versus the DDR3/DDR4-era anchors** (RT-DEV-02, RT-PROC-01).
4. **On DDR5 the controller code sits behind on-die SEC, which *hurts* RS-8.** SEC turns doublets into 3-symbol events, so the limit falls from 5.4e-5 to 1.5e-5.
5. **64Gb tRFC is 700 ns, not 1,600** (RT-PROC-04).
6. **The flag leg is killed** (§2.3).

The subsections below keep the original arithmetic, with notes where it changed.

### 2.1 The reliability target (critic correction: ~100x tighter)

A 64 GB module at 10 GB/s average serves 10e9 / 64 = 1.56e8 line reads/s, or 4.93e15 per year. A budget of ≤1e-3 uncorrectable errors (UE) per module-year from random raw errors therefore needs **≤2e-19 failures per 64 B read** [ESTIMATE; field UE rates of ~0.2-1%/yr are UNVERIFIED-PK]. The concept's t=8 BCH fails 2.3e-17 per read at raw BER 1e-4, i.e. ~0.1 UE per module-year: **too loose by ~100x.** The corrected code is **t=9: 90 check bits per 512 data bits (17.6%)**, which fails 1.6e-19.

| Raw BER | Line BCH t | Check bits | Parity | 4 KB page BCH parity | Shannon floor |
|---|---|---|---|---|---|
| 1e-5 | 6 | 60 | 11.7% | - | - |
| 1e-4 | 9 | 90 | 17.6% | 1.46% | 0.15% |
| 3e-4 | 12 | 120 | 23.4% | - | - |
| 1e-3 | 17 | 170 | 33.2% | 4.83% | 1.15% |

### 2.2 What the budget buys at the sense amplifier

Today's 50 mV budget = 7σ, so σ_eff = 7.14 mV. At 1e-4 per bit the threshold sits at z = 3.72σ: **26.6 mV, 1.88x less signal.** On the A1 bitline (34.7 fF), the storage capacitor falls from **5.42 to 2.68 fF**, and the pillar from ~1,307 to 644 nm. Gaussian tails flatten fast: going on to 1e-3 buys only 1.22x more (22.1 mV, 2.20 fF). That is why page-scale codes at 1% BER (I-07888, I-10420) add little margin.

### 2.3 Erasure flags (critic correction: worth ~8%, not "3.9% parity")

A second, earlier sample (reduced tRCD today; a delayed-latch sense amp in new silicon) flags bits whose |dV| fell inside a window δ. Two effects the concept missed:
- **False flags.** More correct bits sit just above threshold than wrong bits below it. At δ = 0.5σ (3.6 mV), 88% of margin errors are caught, with 5.4 false flags each; at δ = 1.5σ, 131 each.
- **Refresh latching.** A cell that leaks past threshold before its next refresh is sensed wrong and *restored to a full, confident rail*. For long-resident data, retention and VRT errors are therefore unflaggable; only first-period reads after a write can be flagged (14-60% of those). **Flags are a margin tool for new cells, not a refresh tool.**

Sensitivity on the key unknown (raw BER 1e-4, δ = 0.5σ, target 2e-19):

| Confident share of errors | Hard t | Chase t | Check bits (Chase) | Max raw BER at t=8 | dV at that BER |
|---|---|---|---|---|---|
| 0 | 9 | 7 | 70 | 1.73e-4 | 25.6 mV |
| 0.25 | 9 | 8 | 80 | 1.52e-4 | 26.3 mV |
| 0.50 | 9 | 8 | 80 | 1.06e-4 | 27.7 mV |
| 1.00 | 9 | 9 | 90 | 5.9e-5 | no margin banked |

At best, flags save 20 check bits (90 → 70) or add ~8% to the code's 1.88x. The concept's "d=5 code, 3.9%" ignored false flags and the real target.

**(revised after red team) Leg killed** (RT-CIRC-01, RT-CIRC-02, RT-IND-02; model §10.5):
- **The circuit cannot resolve its window.** A delayed-strobe flag sees 50-150 ps of strobe skew. That equals 6 mV to >1 V of amplitude noise against a 3.6 mV window. Only a locally referenced strobe with ≤15 ps skew and τ ≥ 50 ps reaches the critic's 1.5 mV line.
- **Even ideal flags lose density.** They net −2.2% to −0.2% of die once transport (≥11 bits per line; 0.40 flags per line) and the second SA latch (+2-4% die) are paid.
- **They barely help inside a fixed 128-bit side band.** There, flags buy at most +9% raw-BER headroom over plain BCH-12, and −7% with 1.5 mV comparator noise.
- **The reduced-tRCD proxy measures the wrong population** (RT-DEV-01).

### 2.4 Error geometry (new finding: as important as flaggability)

Binary BCH counts bits, so clusters defeat it. Inside the 128 check bits per line a DDR5 ECC RDIMM already carries:

| Share of error bits in clusters | Cluster size | Max raw BER, BCH-12 | Max raw BER, RS(80,64) | RS with one chip dead |
|---|---|---|---|---|
| 0 | - | 3.3e-4 | 5.4e-5 | 8.3e-7 |
| 1% | 3 bits | 5.2e-5 | 5.5e-5 | 8.3e-7 |
| 10% | 3 bits | 8.5e-6 | 5.8e-5 | 8.9e-7 |
| 0.1% | 8 bits | ≤1e-8 | 5.5e-5 | 8.3e-7 |

BCH-12 tolerates only **~0.4% of error bits in 3-bit clusters** at 1e-4, and essentially no 8-bit clusters. Byte-symbol Reed-Solomon is 6x weaker on isolated bits but ignores byte-confined clusters and keeps chipkill. DDR5 on-die SEC miscorrects a 2-bit error into a 3-bit burst ~53% of the time [ESTIMATE]; behind it, BCH-12 holds to an internal raw BER of 1.7e-4. **The contract must specify a per-codeword cluster-size spectrum, not just a BER.**

### 2.5 Relaxed refresh on commodity DRAM

**Power.** A 64 GB RDIMM holds 40 dies × 16 Gb × 1.0625 (on-die ECC) = 6.8e11 cells. At 45.9 fJ per cell refresh (A1), one pass costs 31 mJ, or 31 mJ / 0.064 s = **0.488 W** at 64 ms and **0.031 W** at 1 s. An hourly scrub adds 6.8e11 × 3 pJ / 3,600 s = 0.57 mW.

**Refresh-blocked time.** tRFC/tREFI = 295 / 3,900 ns = 7.56% for 16Gb. At 1 s, tREFI stretches 15.6x and the loss falls to 0.48%. For 64Gb (tRFC ~1.6 µs, extrapolated), it is 41% → 2.6%.

**Safe interval** (static BER × VRT accumulation fits the side-band code; VRT growth 1x/day, 1 h scrub):

| Retention model (85 C) | BCH-12, iid errors | RS-8, clustered | At 65 C (x4) | At 45 C (x16) |
|---|---|---|---|---|
| pow3 (B4, optimistic) | 3.6 s | 2.0 s | 7.9-14 s | 31-58 s |
| lognormal (central) | **1.5 s** | **0.84 s** | 3.3-6.1 s | 13-24 s |
| pow5 (pessimistic) | 0.72 s | **0.50 s** | 2.0-2.9 s | 8-11 s |

| Interval | Refresh + scrub | Cut vs 64 ms | Idle-power saving (3 W idle) | tRFC loss, 16Gb |
|---|---|---|---|---|
| 0.5 s | 0.063 W | 7.7x | 14% | 0.97% |
| 1 s | 0.032 W | 15.3x | 15% | 0.48% |
| 2 s | 0.016 W | 30x | 16% | 0.24% |

**VRT sensitivity.** At 100x/day growth with a 24 h scrub, the interval falls to 375 ms; a 10-minute scrub (3.4 mW) holds 1.3 s.

**(revised after red team) DDR5 RDIMMs versus retired DDR4.** The tables above use DDR3/DDR4-era tails with no on-die ECC, so they describe retired DDR4. With chipkill kept (model §10.1):

| Part / code (chipkill kept) | 85 C central | 85 C pessimistic | 65 C central | Degraded (one chip dead), 85 C |
|---|---|---|---|---|
| Retired DDR4 / RS-8 | 837 ms (13.1x of 64 ms) | 500 ms (7.8x) | 3.3 s | 258 ms (4.0x) |
| DDR5 / RS-8 behind on-die SEC, retention ×0.5 | 285 ms (8.9x of 32 ms) | 194 ms (6.1x) | 1.14 s (35x) | 92 ms (2.9x); 366 ms at 65 C |
| DDR5, no retention derate | 569 ms (17.8x) | - | 2.3 s | - |
| DDR5 / BCH-12 behind SEC (no chipkill, for comparison) | 603 ms (18.9x) | - | 2.4 s | not correctable |

- **Power and value.** DDR5 refresh at its 32 ms window is 0.98 W per 64 GB [A1 per-cell energy; ESTIMATE]. At the central interval it falls to 0.11 W, saving 0.87 W. A hybrid self-refresh policy keeps 0.69 W at 20% self-refresh residency, worth $3.94 per module over 5 years (RT-CIRC-04).
- **Refresh-blocked time at 1 s** is 0.24% for 16Gb, not 0.48%.
- **64Gb at tRFC 700 ns** goes from 17.9% blocked to 2.0% at the DDR5 central interval. Same-bank refresh already hides perhaps half to two thirds of the 17.9% (RT-IND-03).
- **Latency.** The decoder slow path is small. On raw DDR4, 1.2% of lines hold an error, almost all single-symbol, so a ~4 ns lookup fixes them; only 0.007% need Berlekamp-Massey. Behind DDR5's on-die SEC, ~0% of lines need any fix. The CXL hop (70-150 ns) makes the commodity product a capacity tier (RT-CIRC-05).
- **A new correlated-fault term.** Relaxed refresh turns benign chip faults into UE risk through coincidence with random errors. On DDR4 that requires marking a chip on its first chip-confined correction: 1.1e-4 UE per module-year with first-read marking, against 1.1e-3 after 10 reads (RT-DEV-04; model §10.6).

**Positive finding.** The commodity path needs **no new storage and no page code**: the RDIMM's 25% side band, re-coded as BCH-12 or RS-8, carries it.

### 2.6 One budget, two ways to spend it (critic correction)

Margin errors and retention errors draw on the same allowance. On a new cell with today's retention tail (lognormal, 85 C), spending the whole BCH-12 allowance on margin leaves 371 ms of refresh. Spending it all on refresh gives 1.5 s at 50 mV. **A 50/50 split gives 25.6 mV *and* 1.2 s (18x)**, because both tails are steep. Portfolio cells that bank the 1.88x (MARGIN STACK, PIXEL-STACK, DIODE-TOWER, AND-STACK MLC) must not also bank the full refresh cut, unless the retention tail moves right (oxide channels: 1e3-1e4x [REPORTED in portfolio logs]).

### 2.7 Against 1-beta DDR5

**(revised after red team)** The "today" and "same die" columns are corrected to DDR5's 32 ms window and to chipkill-kept RS-8 behind on-die SEC. Original values are in brackets.

| Metric | 1-beta DDR5 RDIMM today | Contract on the same die | New 1-beta-class die built to contract |
|---|---|---|---|
| Refresh interval | 32 ms [was 64 ms] | 0.19-0.64 s at 85 C, central 0.29 s; 1.1 s at 65 C; 92 ms in degraded mode [was 0.5-1.5 s, no chipkill] | 0.37-1.5 s, depending on the margin split |
| Refresh power / 64 GB | 0.98 W [was 0.49 W] | 0.11 W central [was 0.03-0.06 W] | similar |
| Refresh-blocked time | 7.6% (16Gb) | 0.85% central [was 0.5-1%] | <1% |
| Required signal / Cs | 50 mV / 5.4 fF | unchanged | 26.6 mV / 2.7 fF |
| Check-bit overhead | 6.25% on-die + 25% module side band | the same 25%, re-coded | 17.6% (t=9) |
| Density | 0.447 Gb/mm² | unchanged | **0.404 Gb/mm² (0.90x) on the same planar cell** |
| Cost | $1.48/GB | +$0 bits; energy saving worth $0.062/GB over 5 yr at 20% self-refresh residency [was $0.041/GB] | pays off only via cells it enables |

Energy value: 0.456 W × 43,830 h × 1.3 PUE = 26 kWh = **$2.60 per 64 GB over 5 years** at $0.10/kWh (2.7% of module cost), or 7.1 MW per exabyte. The large value is **strategic**: it defuses the 64Gb tRFC crisis and lets new cells qualify against a controller instead of 7σ.

**(revised after red team)** On DDR5's 32 ms basis the value is $3.94 per module (~4% of module cost) with 20% self-refresh residency. The "64Gb tRFC crisis" shrinks: 18% blocked at a 700 ns tRFC, not 41%, and same-bank refresh hides part of it. That leaves ~6-16 points recovered, not ~38 (RT-PROC-04, RT-IND-03). The strategic value now rests mainly on letting new cells qualify against a controller, which the $1M plan cannot prove.

### 2.8 Hammer and page codes

- **Hammer.** A 1 s window allows 2.17e7 activations of one row (21,739x HCfirst 1,000), so counters are mandatory at any refresh rate. Relaxed refresh only removes the REF slots that host in-DRAM TRR. Controller RFM substitution costs ~0.4% of bank time typically and ~8% under attack, against the 7.6% tRFC removed [ESTIMATE]. PRAC parts count rows regardless of REF rate.
- **Page codes.** Uncoalesced, a 64 B write into a 4 KB codeword costs 129 line transfers; ≥99% SRAM coalescing brings it to 2.3. A page decode (~1 pJ/bit [ESTIMATE]) beats refresh only for pages read <~0.7 times/s, so page codes serve cold or compressed pages only.

### 2.9 GO/NO-GO threshold (pre-set)

**(revised after red team: superseded by the revised gate in §5 and §11.4; the flag condition is removed.)** **GO** if the measured error stream (including VRT over a 1 h scrub) fits the side band at 2e-19 per read with refresh ≥0.5 s at 85 C: BCH-12 ≤3.3e-4 with ≤0.4% of error bits in ≥3-bit clusters, or RS-8 ≤5.4e-5 with byte-confined clusters. **And** ≥50% of half-charge errors must be flaggable at a ≤0.5σ window. **NO-GO** if the safe interval is <256 ms at 65 C even with RS-8 (RAIDR-class profiling gets ~4x without ECC), or >10% of error events span more than one byte, or <25% of margin errors are flaggable.

---

## 3. What is new versus prior art

**Known, with dates:**
- **ECC buys refresh: Micron, 2000s.** US 7,447,974 (2008) through US 9,064,600 (2015): the controller slows refresh because the errors are correctable [REPORTED]. **The core idea is old**; early members are likely expired [UNVERIFIED].
- **Error-rate-driven and per-page refresh.** Elpida US 7,493,531 (2009); Qimonda US 7,975,170 (2011).
- **Hi-ECC** (Intel, ISCA 2010): multi-bit BCH cut eDRAM refresh power ~93% at ~2% storage [REPORTED]. Ancestor of the page code.
- **RAIDR** (CMU, ISCA 2012): 74.6% fewer refreshes without ECC [REPORTED]; the NO-GO baseline.
- **LOT-ECC** (Utah, ISCA 2012): tiered chipkill on commodity DRAM.
- **ArchShield** (Georgia Tech, ISCA 2013): tolerates BER 1e-4 at 4% capacity [REPORTED]; the closest system precedent.
- **REAPER** (ISCA 2017) retention profiling; **Solar-DRAM** (ICCD 2018): reduced-tRCD failures mark stable weak cells (the flag proxy).
- **DRAM Bender** (ETH/CMU, IEEE TCAD 2022-23): open FPGA tester; DDR3/DDR4 and HBM2, no DDR5 found [REPORTED].
- **Read disturb.** PRAC study (SAFARI 2024: <13% overhead now, up to 94% later); CnC-PRAC (2025, ~1% energy); PaCRAM (HPCA 2025, partial restore on 388 DDR4 chips); DejaVu (ISCA 2026, restoration level shifts ACmin) [REPORTED].
- **CXL reuse.** X-PPR (IEEE CAL 2025) repairs recycled DDR4 in a CXL device; Meta Vistara and Marvell Structera X/XA (2025-26) put retired DDR4 behind CXL. None is known to relax refresh.
- **Neighbouring patents.** US 12,488,827 (2025, CXL hammer refresher); US 8,898,544 (weak-cell maps as erasures); Micron analog accumulators US 10,943,636 (2021), US 11,568,918 (2023), US 10,964,378.
- **Flash soft bits.** SanDisk/WD US 11,907,545 (2024): a longer-discharge second sense yields a soft bit. The nearest analogue of the DRAM flag.
- **Typed pages.** SHIELD (arXiv 2026): KV mantissa tolerates 1e-4 [REPORTED]; LLNL zfp fixed-rate arrays. Kelle (arXiv 2025) pairs relaxed eDRAM refresh with KV eviction and recomputation [REPORTED]. Flikker (ASPLOS 2011) relaxes refresh for non-critical data and EDEN (MICRO 2019) runs DNNs on approximate DRAM [UNVERIFIED-PK]. Reliability-typed data is therefore not new.
- **Compression-funded ECC and lossy memory.** Frugal ECC (SC15) [REPORTED]; COP (ISCA 2015) and CREAM (HPCA 2017) [UNVERIFIED-PK]; AVR/MemSZ lossy memory compression (Chalmers) [REPORTED].
- **More ECC-for-refresh.** SECRET leaky-cell ECC, -87% refresh power [REPORTED, snippet]; ECC(552,512) on gain-cell eDRAM, ~21x longer refresh (arXiv 2607.16042, preprint) [REPORTED].
- **Flag-adjacent precedents (named by Stage 2 critics of I-11148).** Razor (MICRO 2003) flags late-settling logic with a delayed shadow latch: the circuit ancestor of the delayed-sample flag. XED (ISCA 2016) exports on-die ECC detections to the controller as chip-level erasure hints. FLY-DRAM; IBM chipkill chip marking [all UNVERIFIED-PK].
- **Tier-orthogonal codes.** NAND RAIN across planes/dies and chipkill symbol codes; the Stage 2 innovation critic dropped I-00729 on this basis [UNVERIFIED-PK].
- **[UNVERIFIED-PK]:** Morphable ECC and AVATAR (DSN 2015); BEER/HARP (MICRO 2020-21); Microsoft GreenSKU; HBM3 ECC severity reporting.

**The genuine delta** (not found in this session's limited searches; an FTO search is still required):
1. **A per-read sense-amp reliability flag exported across the interface**, decoded by a bounded Chase/GMD decoder. Nearest DRAM precedents: XED (chip-level detections after on-die decode, not per-bit analog confidence), static weak-cell erasure maps (US 8,898,544) and offline reduced-tRCD profiling (Solar-DRAM). A per-read, per-bit DRAM sense flag was not found, but Razor's delayed-sample latch and NAND soft-bit sensing make obviousness and design-around the main risks.
2. **An open raw-BER device grade** defined by BER, cluster-size spectrum per codeword and VRT growth rate at a stated interval and temperature. The controller picks binary or symbol codes from the grade.
3. **Latching-aware relaxed refresh.** Scrub sized to VRT growth, temperature-tracked intervals, RFM substitution for REF-hosted TRR, and graceful degradation when a chip dies. The novelty is the combination; each piece has precedent.
4. **Typed pages as device code classes:** exact (BCH/RS), regenerable (CRC plus recompute), lossy-bounded (fixed-rate). Reliability-typed data has precedent (Flikker, EDEN, Kelle); the delta is only the code-class interface inside a CXL expander.

**Not new:** "ECC lets refresh slow down", retention profiling, reliability-typed data, compression-funded ECC, and CXL boxes for weak or old DRAM. Do not claim them.

---

## 4. Show-stoppers and how persistence could get around them

| # | Show-stopper | Number | Workaround path |
|---|---|---|---|
| 1 | Clustered errors (sub-wordline/MAT faults, SEC miscorrection) | BCH-12 survives only ~0.4% of error bits in 3-bit clusters | RS-8 (keeps chipkill): 0.84 s central, 0.50 s pessimistic at 85 C; chip-symbol codes for multi-byte clusters; 4-16x more at 45-65 C |
| 2 | Refresh latching makes retention errors confident | Flags catch 14-60% of first-period errors, ~0 for resident data | Flags for margin only; hard-decision codes plus scrub for refresh |
| 3 | Unknown VRT growth | 100x/day, 24 h scrub → 375 ms | 10-min scrub holds 1.3 s for 3.4 mW; measure g |
| 4 | Hammer at relaxed refresh; partial restore weakens victims (PaCRAM, DejaVu) | 2.17e7 ACT per 1 s window; TRR slots lost | Controller RFM (0.4% typical, 8% attack) or PRAC; measure weakened-victim HCfirst |
| 5 | Self-refresh timer is on the die | Idle savings vanish in self-refresh | Controller issues REF in power-down (background cost unmodelled); programmable self-refresh in the JEDEC grade |
| 6 | DDR5 on-die ECC hides raw errors | 53% 2 → 3-bit miscorrection; internal limit 1.7e-4 | Raw physics on DDR4; post-SEC statistics on DDR5; vendor test mode under NDA |
| 7 | Check bits cost area on new dies | t=9: 17.6% vs 6.25% → 0.90x density | Pays only via the cells it enables; 1.46% page codes for cold data |
| 8 | Page-code RMW and decode energy | 129 transfers per write uncoalesced; break-even 0.7 reads/s | ≥99% coalescing; cold/compressed pages only |
| 9 | 2e-19 cannot be shown directly | 1,000 h soak = 5.6e14 reads per board | Extrapolate from Phase 1 maps; accelerate with heat and longer intervals; fleet telemetry after the raise |
| 10 | Typed-page traps | Regenerable at 1e-6: ~3e5 recomputes/s on a 40 GB KV cache (critic). Lossy: zfp block re-quantization and drift over 1e4 steps | Light ECC under the CRC; zfp only for whole-array HPC regions after a drift test |
| 11 | Tier-orthogonal codes assume tier-confined faults | WL-WL shorts span 32 tiers; 0.99^32 = 72% rescued only if shorts are isolated | Defer to 3D-cell coupons (AND-STACK, PIXEL-STACK) |
| 12 | Analog hammer counter | Designed 64 ms leak ~8 fA, drifts ~100x over 25-95 C; ~10% mismatch; Micron owns the core | Reset-on-REF no-leak variant; FTO opinion; PRAC/RFM fallback |

None is a physics wall. Items 1-4 are the measurement that decides the concept.

---

## 5. The decisive experiment

### 5.R Revised decisive experiment (revised after red team)

**Question (revised).** With chipkill kept (RS-8), does each part's error stream fit the 128-bit side band at 2e-19 per read with refresh ≥6x its own JEDEC window at 85 C, and ≥24x at 65 C? The windows are 64 ms for DDR4 and 32 ms for DDR5. The stream must include:
- VRT accumulated over the scrub period;
- the post-on-die-ECC event structure of 1a/1b DDR5;
- the chip-fault coincidence term.

Does a per-module servo hold the grade it predicts? The flag question is dropped: that leg is killed (§2.3).

**What changed and why.**
- **DDR5 is measured, not inferred from DDR4** (RT-DEV-02, RT-PROC-01, RT-IND-04).
- **A failure-mode census replaces the "Poisson to 6 errors" check** (RT-DEV-04).
- **VRT coincidence and dwell time (RTN at the right timescale) are added** (RT-DEV-03).
- **The population spans ≥30 lots per vendor, and the gate tests a servo** rather than a population floor (RT-PROC-02).
- **A 1 h grade is checked against a 1,000 h hold**, a sort-flow proxy (RT-PROC-03).
- **Phase 2 measures latency at injected 1e-4 and idle power**, self-refresh versus power-down (RT-CIRC-04, RT-CIRC-05).

**Facility.** As before, plus two open Antmicro DDR5 RDIMM testers. These are Apache-2.0 boards on an AMD Artix UltraScale+ FPGA; Google funded them and Google/ETH used them for the DDR5 "Phoenix" study [REPORTED, `resp-raw-ber-contract.jsonl`].

**Phase 1 steps (M0-6), revised.**
1. **DDR4 population (retired-DDR4 / CXL landing zone).**
   - Quick screen: 150 modules spanning ≥30 lots (date codes) per vendor, 85 C, two intervals.
   - Deep maps: 60 modules covering 1x/1y/1z/1a date codes, to fit a node trend.
   - 20 retention-reject modules.
2. **Retention map.** 0.128-4 s × {45, 65, 85} C × 4 patterns; fit pow3, lognormal or pow5.
3. **DDR5 leg.** At least 24 1a/1b DDR5 RDIMMs from 2-3 vendors, on the open testers.
   - Measure per-die singleton counts through JEDEC ECS codeword-count mode. Its 256/Gb threshold masks only BER below ~2.4e-7 on a 16Gb die, below the regime of interest [REPORTED: ECS counts codewords with errors; thresholds 256/1,024/4,096 per Gb].
   - Add post-SEC 2-3-bit event maps; their geometry is visible because SEC events are chip-confined.
   - Invert to raw BER with BEER-style recovery of the on-die H-matrix.
   - Compute the RS-8-behind-SEC safe interval directly from the post-SEC stream, which is what the controller decodes.
4. **VRT.**
   - Hourly whole-module re-maps for 1,000 h (6 weeks) on 20 modules at 65/85 C: growth rate g, and VRT arrivals per codeword per scrub period (overdispersion against Poisson).
   - A dwell-time (RTN) spectrum from row subsets re-mapped every 20 s-20 min at 85 C.
5. **Failure-mode census.** Classify every multi-bit event by chip, DQ, beat, row, column and MAT. Measure each mechanism's event rate at 1 s against 32/64 ms. Fold in the chip-fault coincidence term (model §10.6). Test first-read chip marking in the controller RTL.
6. **Servo and sort proxy.** Grade each module from ≤1 h of test (interval, cluster spectrum). Check that the grade holds over the 1,000 h soak, for ≥95% of modules.
7. **Hammer × relaxed refresh** with controller RFM in place of TRR (unchanged).
8. **Flag-proxy validation, as revival data only.** Compare truncated-tRAS cells (known |dV|) with reduced-tRCD flags: overlap, and column/subarray correlation against random. Also test a biased-precharge amplitude proxy [UNVERIFIED-PK method].
9. **GO/NO-GO #1 at M6** (table below).

**Phases 2-3 (M4-18), revised.**
- **CXL soak.** The Agilex CXL Type-3 controller runs on retired DDR4. Controller RTL also runs on the open DDR5 tester. Both get 1,000 h soaks at the servoed interval.
- **Latency.** Measure p50/p99 load-to-use at injected raw BER 1e-4, plus an ASIC projection for a host-IMC decoder.
- **Idle power.** Measure RDIMM + PHY power in self-refresh versus power-down with controller REF.
- **sky130.** One slot carries the reset-on-REF counters and one amplitude-domain flag test structure (revival data). The second slot is dropped.

**Budget (revised; standalone, under $1M).** Inside the portfolio seed only Phase 1 (~$124k) is funded.

| # | Item | Cost | Change |
|---|---|---|---|
| 1 | 4 DRAM Bender stations | $56k | - |
| 1a | 2 open DDR5 RDIMM testers (fab, assembly, FPGA) | $20k | new [ESTIMATE] |
| 2 | 150 DDR4 (≥30 lots/vendor) + 20 reject + 24 DDR5 RDIMM | $24k | +$6k |
| 3 | Thermal (6 rigs) | $14k | +$2k |
| 4 | 50 TB analysis server | $10k | - |
| | **Phase 1 (decisive)** | **$124k** | +$28k |
| 5-9 | Agilex kits, CXL IP, hosts, RTL contractor, soak ops (DDR4 CXL + DDR5 tester) | $262k | - |
| 10 | 1 sky130 slot (counters + amplitude-flag structure) | $30k | -$20k |
| 11 | Collaborator subawards | $60k | - |
| 12 | IP: 2 provisionals + 1 PCT (grade/test method; servoed latching-aware refresh with first-read chip marking) | $35k | -$10k |
| 13-14 | Founders; rent, insurance, travel | $360k | - |
| 15 | Contingency (~8.6%) | $75k | +$5k |
| | **Total** | **$946k** | was $943k |

**Pre-set pass/fail numbers (revised).**

| Measurement | PASS | FAIL |
|---|---|---|
| RS-8 safe interval incl. VRT (1 h scrub), 2e-19 | ≥6x window at 85 C (DDR5 ≥0.19 s; DDR4 ≥0.38 s) and ≥24x at 65 C | <4x window at 65 C (DDR5 <128 ms; DDR4 <256 ms) |
| Multi-byte (multi-chip) error events | ≤10% of events; no mechanism >2x its 32/64 ms rate | >10% of events, or a new multi-chip mechanism |
| VRT | g ≤700x/day (10-min scrub holds the interval); per-codeword pairs within 2x of Poisson | 10-min scrub cannot hold 6x window at 85 C (85 C claim killed; 45-65 C kept) |
| Servo / sort proxy | 1 h grade holds ≥1,000 h for ≥95% of modules | <90% |
| DDR5 inference | ECS counts resolve singletons at the operating BER; post-SEC model within 2x | ECS masked and no vendor test mode → DDR5 claim stays unproven |
| 1,000 h soaks (DDR4 CXL, DDR5 tester) | 0 UE; corrected errors within 2x of model | any UE |
| Latency (Phase 2) | p99 adder from decoding ≤5 ns at injected 1e-4 | BM path on >1% of lines |

### 5.O Original decisive experiment (pre-red-team; superseded where §5.R differs)

**Question.** At raw BER 1e-4, are DRAM errors isolated, byte-confined and slow-growing enough for the 128-bit side band at 2e-19 per read with refresh ≥0.5 s at 85 C? And are ≥50% of margin errors flaggable?

**Facility.** A bench lab, not a cleanroom. Four DRAM Bender stations (open source, CMU-SAFARI) on Xilinx/BittWare DDR4 boards, with heater-pad PID and VPP control. A subaward to a lab that already runs DRAM Bender: CMU (SAFARI lineage), Rutgers (Minesh Patel) or Georgia Tech (Moinuddin Qureshi). DDR5 comes through a collaborator or the Phase 2 FPGA PHY.

**Steps (Phase 1, months 0-6).**
1. **Population.** 60 DDR4 modules (3 vendors × 2-3 date codes, x4 and x8) plus 20 retention-reject or recycled modules. DDR4 has no on-die ECC, so it shows raw physics.
2. **Retention map.** 0.128-4 s × {45, 65, 85} C × four data patterns, REF suppressed. Fit pow3, lognormal or pow5.
3. **Latching test.** At 1 s, read after N periods, then at reduced tRCD (flag proxy). Compare first-period and steady-state flagged share.
4. **VRT soak.** Re-map 20 modules hourly for ≥4 weeks at 65/85 C to get growth rate g.
5. **Cluster spectrum.** Map every failing bit into 64 B codeword geometry (chip, DQ, beat); score with BCH-12, RS-8 and Chase decoders.
6. **Margin emulation.** Truncated-tRAS partial restore (PaCRAM's open method) plus reduced VPP, BER 1e-5 to 1e-3; double-read at nominal and stepped tRCD for flagged share and false-flag ratio.
7. **Hammer × relaxed refresh.** Double- and many-sided hammer at 64 ms vs 1 s, with controller-directed neighbour refresh in place of TRR.
8. **DDR5 cross-check** of post-on-die-ECC patterns against the 1.7e-4 prediction.
9. **GO/NO-GO #1 at month 6** (§2.9).

**Then:** Phase 2 (months 5-16) builds an Agilex 7 CXL Type-3 controller with every block in the §1 diagram, and runs a 1,000 h soak at 1 s on two boards under Redis, SPEC CPU and vLLM+LMCache traces. Phase 3 (months 8-18) puts a delayed-sample flag latch and 1k reset-on-REF counters on a sky130 shuttle.

**Budget (standalone, under $1M).** Inside the portfolio seed only Phase 1 (~$80-96k) is funded; Phases 2-3 are raise or grant milestones.

| # | Item | Cost | Basis |
|---|---|---|---|
| 1 | 4 DRAM Bender stations | $56k | ESTIMATE $14k each |
| 2 | 60 DDR4 + 20 reject + 20 DDR5 RDIMM | $18k | ESTIMATE |
| 3 | Thermal chamber, thermometry | $12k | ESTIMATE |
| 4 | 50 TB analysis server | $10k | ESTIMATE |
| | **Phase 1 (decisive)** | **$96k** | |
| 5 | 2 × Agilex 7 I-Series kits | $22k | ~€9k each [REPORTED, Jan 2025] |
| 6 | CXL Type-3 IP (negotiated) or partner IP | $100k | List ~€192k [REPORTED] |
| 7 | 2 CXL host servers | $35k | ESTIMATE |
| 8 | RTL/verification contractor | $90k | ESTIMATE |
| 9 | Soak operations | $15k | ESTIMATE |
| 10 | 2 sky130 slots + package/test | $50k | $15k per 100 chips [REPORTED] |
| 11 | Collaborator subawards | $60k | ESTIMATE |
| 12 | IP: 3 provisionals + 1 PCT | $45k | ESTIMATE |
| 13 | Two founders, lean, 2 yr | $300k | ESTIMATE |
| 14 | Rent, insurance, JEDEC/OCP travel | $60k | ESTIMATE |
| 15 | Contingency (~8%) | $70k | |
| | **Total** | **$943k** | |

**Timeline.** Rigs and population by month 2; campaigns months 2-6; **GO/NO-GO month 6**; RTL months 4-12; sky130 tape-out month 8 (chips ~month 16); soak months 12-16; spec v0.9 month 18.

**Pre-set pass/fail numbers.**

| Measurement | PASS | FAIL |
|---|---|---|
| Safe interval at 85 C, side band, 2e-19 | ≥0.5 s | <256 ms at 65 C |
| Error bits in ≥3-bit clusters (BCH path) | ≤0.4% | >10% of events multi-byte (both paths) |
| Flaggable margin errors at ≤0.5σ | ≥50% | <25% |
| Per-codeword overdispersion | within 2x of Poisson to 6 errors | >2x |
| 1,000 h soak at 1 s | 0 UE; corrected errors within 2x of model | any UE |

---

## 6. The $1M, 24-month plan

**(revised after red team)** The changes are in §5.R and §11.2:
- The budget is now $946k, with Phase 1 at $124k. The DDR5 leg is added, and one sky130 slot is dropped.
- The IP order changes: grade/test method and servoed refresh first, with flag filings optional and defensive.
- The flag latch milestones (Q7, kill #7) are moot.

The quarter table below is the original.

Assume M0 = 2027-01-01.

| Quarter | Milestones | Gate |
|---|---|---|
| Q1 (M0-3) | 4 rigs up; 100 modules in hand; subaward signed; provisional #1 (SA flag) filed before any talk | Rigs reproduce published REAPER/PaCRAM behaviour |
| Q2 (M3-6) | Retention, latching, cluster, margin and hammer campaigns; VRT soak running; provisionals #2-3; CXL IP path locked | **GO/NO-GO #1 (M6)** |
| Q3 (M6-9) | Controller RTL; page-type HDM regions; sky130 tape-out (M8) | VRT growth measured (kill #4) |
| Q4 (M9-12) | Bring-up on Agilex; error-injection tests reproduce the model's decoder curves | Gate 2: decoder failure curves within 2x of the model |
| Q5 (M12-15) | 1,000 h soak at 1 s (staggered boards), commodity and reject RDIMMs | Mid-soak: 0 UE |
| Q6 (M15-18) | Soak complete; DDR5 cross-check; contract spec v0.9; PCT filed | **Gate 3 (M16):** soak pass |
| Q7 (M18-21) | sky130 flag latch and counters measured (δ vs offset σ; trip spread 25-110 C); OCP/CXL submission; JEDEC grade proposal draft | Flag latch passes kill #7 |
| Q8 (M21-24) | Raise package: error atlas, soak, spec, IP, partner letters | Raise |

**Budget allocation.** Experiments and hardware $408k (43%), people incl. subawards $360k (38%), IP $45k (5%), rent/insurance/travel $60k (6%), contingency $70k (7%).

**Team.**
- **Founder A, systems/ECC.** A flash-controller ECC architect (BCH/LDPC RTL, Chase decoders) from SSD controller teams: Phison, Silicon Motion, Marvell, Microchip, SanDisk/WD, Kioxia, Samsung [UNVERIFIED-PK as hiring sources]. The concept *is* the NAND playbook, and such people exist in volume.
- **Founder B, device/circuit.** A DRAM sense-amp/periphery designer, e.g. ex-Micron Boise. Owns half-charge emulation, the flag latch and the JEDEC grade.
- **Student/postdoc (subaward).** Someone who has already run DRAM Bender: SAFARI (Onur Mutlu, ETH/CMU), Rutgers (Minesh Patel) or Georgia Tech (Moinuddin Qureshi).
- **Advisors.** Coding: Lara Dolecek (UCLA) [UNVERIFIED]. CXL testbeds: Nam Sung Kim (UIUC) [UNVERIFIED]. Resilience: Mattan Erez (UT Austin) [UNVERIFIED]. LOT-ECC: Rajeev Balasubramonian (Utah). zfp: Peter Lindstrom (LLNL) [UNVERIFIED]. DDR5 hammer: Kaveh Razavi (ETH) [UNVERIFIED].
- **Non-dilutive add-ons.** NSF SBIR/STTR, DoD Microelectronics Commons hubs, DOE efficiency programs [UNVERIFIED-PK fit].

**IP strategy.**
- **File first (by M3):** the DRAM sense-amp reliability flag. That covers a delayed second sample or slow-resolution detector, a burst-level flag transfer (side band or repurposed ECC beats), and a bounded Chase/GMD decoder that consumes it. It is the strongest novelty.
- **By M6:**
  - (2) the raw-BER grade and test method: BER plus cluster spectrum plus VRT growth, with code type and interval selected from the grade;
  - (3) latching-aware relaxed refresh: VRT-sized scrub, RFM substitution, graceful degradation.
- **By M18:** PCT, plus (4) typed pages in a CXL device. File (5) tier-orthogonal mapping later as a continuation (weak: NAND RAIN and chipkill precede it).
- **FTO risks:**
  - SanDisk/WD soft-bit family (US 11,907,545; 11,971,829): NAND-specific per snippets; check claims.
  - US 8,898,544 (map-based erasures): design around with per-read timing flags.
  - Micron analog accumulators (US 10,943,636; 11,568,918; 10,964,378); Micron relaxed-refresh family (confirm expiry).
  - US 10,691,532 (ECC scrub); US 12,488,827 (CXL hammer refresher); US 11,347,650 (lossy controller); US 8,458,568 (compression funds ECC); JEDEC PRAC/RFM essential patents (FRAND).

---

## 7. After the demo

**Who licenses or partners.**
- **CXL controller vendors** (Marvell Structera, Microchip, Astera Labs [UNVERIFIED-PK]). Fastest route: license the decoder, scheduler and grade-aware firmware into chips that already host retired DDR4.
- **Hyperscalers** (Meta, already running Vistara; Google, Microsoft [UNVERIFIED-PK]). Pilot customers and fleet error telemetry to validate 2e-19.
- **Micron, Samsung, SK hynix.** A sellable relaxed-spec bin (retention rejects become product) and a way to qualify short-capacitor and oxide cells. Micron also holds the hammer-counter patents and is the only U.S. DRAM maker.
- **Kioxia** (with Nanya on oxide-channel DRAM, per FINAL_CONCEPTS) has flash-controller culture: a natural early adopter [SPECULATIVE fit].
- **Foundries.** GlobalFoundries (22FDX, Malta NY) or SkyWater for the controller ASIC; TSMC 28 nm as second source.
- **Display makers** (IGZO TFT lines: LG Display, Samsung Display, Sharp, BOE [UNVERIFIED-PK]). Not controller customers, but possible builders of oxide cell wafers qualified to the contract instead of 64 ms (links to CELL-WAFER FOUNDRY) [SPECULATIVE].

**What $10-50M buys.**
- *$10-15M:* a 22/28 nm CXL Type-3 controller ASIC (mask set plus a ~25-person team for ~2 years [ESTIMATE]), CXL compliance, and two module-maker design-ins.
- *$15-30M:* a 10k-module field pilot at one or two hyperscalers. Fleet-scale reads (~5e19 per year at 10k modules [ESTIMATE]) finally test the 2e-19 target directly.
- *$30-50M:* a co-designed new-cell demo with MARGIN STACK silicon behind the controller, with real SA flags in place of the timing proxy, plus standards staffing.

**Standards.**
- An OCP contribution (Composable Memory Systems) and CXL Consortium RAS work for the interface and the typed-page classes.
- A JEDEC JC-42 "ECC-native" device grade: raw BER, cluster spectrum, VRT growth, and a programmable self-refresh interval [UNVERIFIED-PK committee fit].
- Adoption is the scale path, not a kill criterion.

---

## 8. Resources and America

- **Scarce inputs.** The commodity path needs **zero wafer starts**: it re-codes existing RDIMMs and turns reject bins into product. The controller is mature 28/22 nm logic: **no EUV, no HAR capacitor etch, no capacitor Hf/Zr stack**. Correction to the concept text: 22FDX/28 nm HKMG still uses a negligible hafnium-oxide gate film.
- **EUV.** None for the controller. For new cells, halving Cs drops pillars from ~1,300 to ~644 nm, easing the helium- and PFAS-heavy HAR etch, but not removing EUV from cell patterning.
- **Energy.** Use-phase energy is ~6.6 kWh per server GB over 5 years, ~16x its fab electricity (A2 [ESTIMATE]). At 1 s refresh the contract saves 26 kWh per 64 GB module over 5 years, 7.1 MW per exabyte: real, but small next to I/O and background power.
- **Water.** No incremental fab water.
- **U.S. manufacturability.** Every piece is U.S.-buildable now:
  - DRAM Bender and FPGA work at any university lab (CMU, Georgia Tech, Rutgers);
  - test structures on SkyWater sky130 (Minnesota) via ChipFoundry;
  - the controller at GlobalFoundries Malta via MOSIS 2.0 or direct 22FDX MPW (~$18k/mm², 4 mm² minimum [REPORTED]);
  - soak partners at NERSC or TACC.

  It also gives Micron's U.S. output and second-life DRAM a higher-value outlet.

---

## 9. Kill criteria

M0 = 2027-01-01. Each criterion is physics or measurement; standards adoption is not one. **(revised after red team:** #1, #3 and #7 rewritten, #9-#10 added; the originals are kept struck through where replaced.)

1. **By 2027-06-30 (M6): kill the commodity relaxed-refresh product** if the RS-8 (chipkill) safe interval is <4x the part's own JEDEC window at 65 C, including VRT over a 1 h scrub. That is <256 ms for DDR4 and <128 ms for DDR5. *Revival (revised after red team, RT-DEV-05):* an oxide or gain-cell array whose measured retention CDF reaches ≤1e-6 at 85 C, sits ≥10x right of Si at the same Cs, and has PBTI/hydrogen drift and RTN-like Ioff switching characterised as extra error terms. Or stacked write devices (I-12627) with a measured tail-correlation share ρ ≤0.1: model §10.10 gives 0.84 → 1.8 s at ρ = 0.1, and 5.6 s only at ρ = 0. ~~Revival: re-run on IGZO cells "1e3-1e4x to the right"~~: that was a typical-Ioff ratio, not a tail.
2. **By M6: kill binary BCH** if >0.4% of error bits arrive in ≥3-bit clusters per codeword; **kill both line codes** if >10% of error events span more than one byte. *Revival:* chip-symbol codes in a wider side band (DDR6/LPDDR6 organisations [UNVERIFIED-PK]).
3. **KILLED by the red team (RT-CIRC-01, RT-CIRC-02): the per-read sense-amp flag leg.** A delayed strobe sees 50-150 ps skew against a 14-35 ps window. Even ideal flags net −2.2% to −0.2% of die after transport and the second SA latch. ~~By M6: kill the SA flag latch if <25% flaggable~~. *Revival:* silicon with a flag-window σ ≤1.5 mV across ≥1k SAs at 85 C without per-SA trim (amplitude-domain, or a locally referenced strobe with ≤15 ps skew), **and** a positive measured ledger. That ledger means check bits saved exceed transport bits plus SA area, e.g. on new cells where margin errors dominate and the parity saving is ≥25% (RT-IND-02). CDS-derived flags on MARGIN STACK silicon remain a candidate.
4. **By 2027-09-30 (M9): kill the 85 C claim** (keep 45-65 C temperature-tracking) if measured VRT growth is so fast that a 10-minute scrub cannot hold ≥0.5 s at 85 C. In the model (lognormal tail) that needs growth above ~700x static BER per day with RS-8 or ~5,000x with BCH-12; at 100x/day a 10-minute scrub still holds 0.72 s (RS-8) to 1.3 s (BCH-12) [ESTIMATE].
5. **By 2027-12-31 (M12): kill relaxed refresh on non-PRAC parts** if weakened victims at 1 s show HCfirst <50% of the 64 ms value *and* controller RFM at ≤8% bank time cannot hold zero flips under many-sided patterns.
6. **By 2028-04-30 (M16): stop and diagnose before any raise** if the 1,000 h soak shows any UE or corrected errors >2x the Phase 1 model.
7. ~~By M19: kill the flag latch if the sky130 latch needs a window >1σ~~ **(revised after red team: moot; the leg is already killed, see #3).** The single sky130 slot's amplitude-flag structure only measures the revival condition.
8. **By M6 (re-scope, not kill):** with no CXL IP path at ≤$100k, soak through PCIe-BAR emulation instead.
9. **(new, revised after red team) By M6: kill the DDR5 commodity claim, keeping retired DDR4 behind CXL,** if either:
   - the DDR5 RS-8-behind-on-die-SEC safe interval, inferred from ECS singleton counts plus post-SEC event maps, is <4x the 32 ms window (128 ms) at 65 C; or
   - ECS masking prevents resolving singletons at the operating BER and no vendor test mode is obtained. In that case the claim is "unproven", not "killed".

   *Revival:* vendor ECC-off maps under NDA (RT-DEV-02, RT-PROC-01, RT-IND-04).
10. **(new, revised after red team) By M12: kill relaxed refresh beyond 4x on raw DDR4** if the controller cannot mark a chip on its first chip-confined multi-symbol correction in the soak. Marking after 10 reads uses the whole 1e-3 UE budget (model §10.6; RT-DEV-04).

---

## 10. Sources

All URLs below are logged in `research/sources/*.jsonl` (mostly `dos-raw-ber-contract.jsonl`; others in A1, A2, Stage 2 critic and dossier logs).

**Characterization tools and retention**
- https://arxiv.org/pdf/2211.05838
- https://www.research-collection.ethz.ch/handle/20.500.11850/642507
- https://files.futurememorystorage.com/proceedings/2024/20240808_TEST-301-1_LUO.pdf
- https://arxiv.org/html/2506.10441v2
- https://arxiv.org/pdf/1805.03195
- https://people.cs.rutgers.edu/~mp2099/files/patel_isca2017_reach_paper.pdf
- https://people.cs.rutgers.edu/~mp2099/files/patel_isca2017_reach_full_talk.pdf
- https://arxiv.org/pdf/2204.10387
- https://arxiv.org/html/2306.16024v1
- https://www.pdl.cmu.edu/ftp/NVM/raidr-isca12.pdf
- https://people.cs.rutgers.edu/~mp2099/files/kim_iccd18_solar_paper.pdf
- https://people.cs.rutgers.edu/~mp2099/files/wang_micro18_reducing_poster.pdf

**ECC architecture and typed pages**
- https://courses.grainger.illinois.edu/CS534/fa2021/reading_list/9a.pdf
- https://memlab.ece.gatech.edu/papers/ISCA_2013_1.pdf
- https://users.cs.utah.edu/~rajeev/pubs/isca12.pdf
- https://arxiv.org/pdf/2604.07396
- https://sc22.supercomputing.org/presentation/index-870.htm
- https://arxiv.org/pdf/2510.16040
- https://arxiv.org/pdf/2607.16042
- https://www.sc15.supercomputing.org/schedule/event_detail-evid=pap528.html
- https://research.chalmers.se/en/publication/512096

**Row hammer**
- https://www.arxiv.org/pdf/2502.11745
- https://arxiv.org/pdf/2406.19094v1
- https://www.arxiv.org/pdf/2506.11970
- https://cispa.de/de/research/publications/213276-dejavu-why-you-should-write-to-your-dram-rows-twice-carefully

**CXL landing zone and platforms**
- https://ieeexplore.ieee.org/document/10935665
- https://www.storagenewsletter.com/2026/07/02/meta-uses-cxl-for-memory-expansion-to-replace-ddr4/
- https://www.techspot.com/news/112977-meta-using-old-ddr4-memory-ddr5-only-ai.html
- https://www.marvell.com/blogs/structera-xa-cxl-compression-every-gigabyte-counts.html
- https://www.altera.com/products/devkit/po-3247/agilex-7-fpga-i-series-development-kit-2x-r-tile-and-1x-f-tile-rev-b
- https://os.itec.kit.edu/4012.php
- https://www.intel.com/content/www/us/en/docs/programmable/683288/current/i-series-fpga.html

**DRAM timing and scaling**
- https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/7134/SQR-RD5N16G5K6HZZG.pdf
- https://arxiv.org/pdf/1712.08304

**Patents**
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7447974
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9064600
- https://patents.google.com/patent/US7493531
- https://patents.google.com/patent/US7975170
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8898544
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10691532
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12488827
- https://patents.justia.com/patent/10943636
- https://patents.google.com/patent/US11568918
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11907545
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11971829
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11347650

**Fabrication access**
- https://tinytapeout.com/news/chipfoundry-sponsor/
- https://www.eenewseurope.com/en/tiny-tapeout-sees-industrial-boost-as-it-recovers-from-efabless-closure/
- https://www.isi.edu/news/80945/mosis-2-0-revives-a-legacy-rehan-kapadia-outlines-a-bold-future-for-rapid-microelectronics-prototyping/
- https://allaboutcircuits.com/news/mosis-partners-with-globalfoundries-extending-40-year-prototyping-legacy
- https://www.cmc.ca/globalfoundries-22fdx-fdsoi-22-nm-process/

**Red-team response (logged in `research/sources/resp-raw-ber-contract.jsonl`)**
- https://lkml.iu.edu/2411.2/07040.html
- https://kernel.org/doc/Documentation/ABI/testing/sysfs-edac-ecs
- https://patents.google.com/patent/US12430203
- https://en.wikipedia.org/wiki/DDR5_SDRAM
- https://faculty-web.msoe.edu/johnsontimoj/ELE4142/files4142/DDR5_Spec.pdf
- https://github.com/antmicro/ddr5-tester
- https://blog.google/security/supporting-rowhammer-research-to/
- https://chipsalliance.org/news/versatile-rowhammer-testing-platform/

No-URL items: field DIMM UE rates (Schroeder 2009 and Sridharan field studies); Razor, FLY-DRAM, Flikker, EDEN, COP, CREAM, NAND RAIN and chipkill chip marking (named by Stage 2 critics); XED, Morphable ECC, AVATAR, BEER/HARP, GreenSKU and HBM3 ECC reporting; US 8,458,568 and US 10,964,378 (cited in Stage 2 and notes without a logged URL); A2's use-phase energy estimate (internal); named researchers' affiliations marked [UNVERIFIED].

---

## 11. Red-team outcome

Four reviewers attacked this dossier on 2026-11-02 (`research/redteam/rt_*.json`): DEV, the device physicist; PROC, the DRAM/3D-NAND process veteran; CIRC, the sense-amp designer; and IND, the industry strategist. They raised **19 objections**: DEV 5, PROC 4, CIRC 5, IND 5.

**Dispositions: 0 REFUTED, 10 ACCEPTED-MITIGATED, 7 ACCEPTED-DOWNGRADE, 2 ACCEPTED-KILL.** Both kills hit the same leg, the per-read sense-amp flag.

Full responses with numbers are in `research/redteam/responses_raw-ber-contract.json`. The model variants are in `models/raw-ber-contract.py` section 10 and the RED-TEAM REVISIONS block. Sources are in `research/sources/resp-raw-ber-contract.jsonl`. Every objection is answered; none is deleted.

### 11.1 Disposition table

| Id | Severity | Disposition | One-line action |
|---|---|---|---|
| RT-DEV-raw-ber-contract-01 | MAJOR | ACCEPTED-MITIGATED | GO-B (>=50% flaggable) deleted from the M6 gate. |
| RT-DEV-raw-ber-contract-02 | MAJOR | ACCEPTED-DOWNGRADE | Commodity DDR5 headline cut from 15x (DDR4-derived, no chipkill) to ~9x central (6-20x) at 85 C. |
| RT-DEV-raw-ber-contract-03 | MINOR | ACCEPTED-MITIGATED | Phase 1 step 4: VRT coincidence counts and a dwell-time (RTN) spectrum. |
| RT-DEV-raw-ber-contract-04 | MINOR | ACCEPTED-MITIGATED | Failure-mode census replaces the overdispersion-to-6 pass line. |
| RT-DEV-raw-ber-contract-05 | MINOR | ACCEPTED-MITIGATED | Kill #1 revival rewritten as a measurable condition (CDF to 1e-6 at 85 C plus drift and RTN terms). |
| RT-PROC-raw-ber-contract-01 | MAJOR | ACCEPTED-MITIGATED | DDR5 leg (ECS + post-SEC maps + H-matrix inversion) and a DDR4 node-trend axis added. |
| RT-PROC-raw-ber-contract-02 | MAJOR | ACCEPTED-MITIGATED | Per-module servoed interval added to the controller; population widened to >=30 lots/vendor; servo pass line (1 h grade holds 1,000 h for >=95%) in the M6 gate. |
| RT-PROC-raw-ber-contract-03 | MAJOR | ACCEPTED-MITIGATED | Sort-flow test-time estimate added (model 10.9). |
| RT-PROC-raw-ber-contract-04 | MINOR | ACCEPTED-DOWNGRADE | trfc_ns[64Gb] 1600 -> 700 ns in the RED-TEAM REVISIONS block. |
| RT-CIRC-raw-ber-contract-01 | MAJOR | ACCEPTED-KILL | Kill the per-read SA flag leg (named leg: delayed-sample flag latch). |
| RT-CIRC-raw-ber-contract-02 | MAJOR | ACCEPTED-KILL | Same leg as RT-CIRC-01: the flag interface is removed from the contract and the headline. |
| RT-CIRC-raw-ber-contract-03 | MAJOR | ACCEPTED-DOWNGRADE | Server headline restated as ~9x (DDR5) / ~13x (retired DDR4) at 85 C with chipkill, plus a degraded-mode fallback of 2.9-4x. |
| RT-CIRC-raw-ber-contract-04 | MAJOR | ACCEPTED-MITIGATED | Hybrid self-refresh policy in the controller. |
| RT-CIRC-raw-ber-contract-05 | MAJOR | ACCEPTED-MITIGATED | Single-symbol fast path specified in the controller. |
| RT-IND-raw-ber-contract-01 | MAJOR | ACCEPTED-DOWNGRADE | Commodity value restated at ~$3.9 per module over 5 yr. |
| RT-IND-raw-ber-contract-02 | MAJOR | ACCEPTED-DOWNGRADE | IP strategy reordered: grade/test method and servoed refresh first, flag filing optional and defensive. |
| RT-IND-raw-ber-contract-03 | MAJOR | ACCEPTED-DOWNGRADE | Strategic 64Gb claim restated as ~6-16 points recovered. |
| RT-IND-raw-ber-contract-04 | MAJOR | ACCEPTED-MITIGATED | Demo redefined around DDR5 + retired-DDR4 system soaks. |
| RT-IND-raw-ber-contract-05 | MINOR | ACCEPTED-DOWNGRADE | Section 7's '$10-15M ASIC' is demoted to contingent. |

### 11.2 Redesigns adopted

1. **Chipkill by default** (RT-CIRC-03). The headline code is RS(80,64) over bytes, not BCH-12. When a chip is marked dead, its rank drops to a degraded interval until service: 258 ms on retired DDR4 and 92 ms on DDR5 at 85 C, or 366 ms at 65 C. BCH-12 is kept only for tiers that waive chipkill.
2. **DDR5 is measured, on the right basis** (RT-DEV-02, RT-PROC-01, RT-IND-04).
   - **The 32 ms window.** The model now uses DDR5's real 32 ms JEDEC window. The original paired DDR5's 3.9 µs tREFI with 64 ms.
   - **Derate and SEC.** DDR5 retention is derated 0.5x, and the controller code sits behind on-die SEC. A new model finding: SEC hurts RS-8, because doublets become 3-symbol events, so the limit falls from 5.4e-5 to 1.5e-5.
   - **The DDR5 leg.** Phase 1 adds ≥24 1a/1b RDIMMs on open Antmicro DDR5 testers. It reads ECS singleton counts, maps post-SEC events and inverts them to raw BER.
3. **A per-module servo replaces a fleet-wide interval** (RT-PROC-02, RT-PROC-03).
   - **Servo.** The controller servos each rank's interval on its own corrected-error telemetry, at a 3x BER guard. That gives a ~6x fleet-mean cut, against 1-3x for a fixed worst-lot interval.
   - **Grade test.** The demo proves that a 1 h grade holds for 1,000 h.
   - **Sort flow.** A sort flow for new dies is sketched at ~40 s per batch (~0.08 s per die).
4. **First-read chip marking and a failure-mode census** (RT-DEV-04). Relaxed refresh turns benign chip faults into UE risk through coincidence with random errors. Marking a chip on its first chip-confined correction keeps raw DDR4 at 1.1e-4 UE per module-year; marking after 10 reads costs 1.1e-3. A census of multi-bit events by mechanism replaces the "Poisson to 6 errors" check.
5. **VRT coincidence and dwell time** (RT-DEV-03). Same-codeword VRT pairs are counted, and a dwell-time (RTN) spectrum is taken with 20 s-20 min re-maps. RS-8 is insensitive to pairs; BCH-12 loses 3.3x at a 10% pair share.
6. **A hybrid self-refresh policy** (RT-CIRC-04). Idle ranks use the die's own self-refresh, so the policy never loses power. A programmable self-refresh interval is added to the JEDEC grade ask, and Phase 2 measures the background power.
7. **A single-symbol decoder fast path, with the host memory controller as the DRAM-class path** (RT-CIRC-05). Only 0.007% of lines need Berlekamp-Massey at the servoed DDR4 BER, and ~0% behind DDR5 SEC. The CXL product is labelled a capacity tier.
8. **The flag leg is killed** (RT-CIRC-01, RT-CIRC-02, RT-IND-02, RT-DEV-01). The controller keeps a generic erasure input (chip marks, XED-style hints) at no cost. The flag-proxy validation runs as revival data only.
9. **Strategy changes** (RT-IND-01, RT-IND-03, RT-IND-05).
   - **IP.** Lead with the grade and test method, plus servoed latching-aware refresh with first-read chip marking. Flag filings become optional and defensive.
   - **Commercial vehicle.** License firmware into incumbent CXL controllers. The ASIC is built only if a new-cell partner needs it. Venture-scale value is contingent on new-cell partners.
10. **Top-up ideas.**
    - **I-12627 (two series write transistors).** Recorded as an oxide/gain-cell tail route. It only works if shared-defect share ρ ≤0.1: the RS-8 interval goes 0.84 → 1.8 s at ρ = 0.1, and to 5.6 s only at ρ = 0.
    - **I-12302 (plate-strip sensing).** Recorded as the new-cell margin route: Cs 0.30 → 0.15 fF with the contract, against 5.42 → 2.68 fF on the bitline. It is ~18x larger than the flag's +8%, but has planar Micron prior art, so it is not this dossier's IP.

**Model inputs changed (RED-TEAM REVISIONS block):**
- `trfc_ns[64Gb]`: 1600 → 700 ns (RT-PROC-04, RT-IND-03).
- `trefw_ddr5_s`: implicit 0.064 → 0.032 s (RT-DEV-02, RT-PROC-01).
- `ret_time_scale_ddr5`: 1.0 → 0.5 (RT-DEV-02).
- Headline code: BCH-12 → RS-8 (RT-CIRC-03).
- New `RT_INPUTS` for self-refresh, latency, fault rate, lot spread, servo guard, sort, stacked-write correlation, plate strip, flag noise and transport.

The model exits 0, and the output is overwritten in `research/stage3/raw-ber-contract_model_output.md`.

### 11.3 Revised step-change claim

**The step change is in refresh energy and refresh-busy time on commodity DRAM, with chipkill kept.**

| Product | 85 C central | Range | 65 C | Degraded mode |
|---|---|---|---|---|
| DDR5 RDIMMs (vs the 32 ms spec) | ~9x | 6.1x pessimistic to 20x optimistic; 17.8x without the DDR5 retention derate | ~35x | 2.9x |
| Retired DDR4 behind CXL (vs 64 ms) | ~13x | 7.8x pessimistic | - | 4x |

That compares with 15x (7.7-30x) claimed without chipkill.
- **Module level.** DDR5 refresh falls 0.98 → 0.11 W per 64 GB, 23-29% of a 3 W idle module. That is worth ~$3.9 per module over 5 years ($0.062/GB, ~4% of module cost) at 20% self-refresh residency.
- **64Gb.** Refresh-busy time falls 18% → 2% on an all-bank basis, ~6-16 points after same-bank refresh. The original claim was 41% → 2.6%.
- **New cells.** Margin stays 1.88x (50 → 26.6 mV, Cs 5.4 → 2.7 fF) with **no flag bonus**. The concept's largest value, new cells qualified against the grade, stays conditional and outside the $1M proof.

### 11.4 Revised decisive experiment (full version in §5.R)

**Phase 1 (M0-6, ~$124k, decisive).**
- **Retired-DDR4 raw physics:** 150 modules screened over ≥30 lots per vendor, plus a node trend.
- **DDR5 leg:** ≥24 1a/1b RDIMMs on open Antmicro testers. ECS singleton counts plus post-SEC maps, inverted to raw BER.
- **Newly added measurements:**
  - VRT per-codeword coincidence and a **dwell-time (RTN) spectrum at the right timescale** (20 s-20 min re-maps at 85 C);
  - a **failure-mode census** with the chip-fault coincidence term;
  - **1 h grade vs 1,000 h hold** (servo and sort proxy);
  - hammer with controller RFM;
  - flag-proxy validation, as revival data only.

**GO at M6** requires three things:
- the RS-8 safe interval, including VRT, is ≥6x the part's window at 85 C (DDR5 ≥0.19 s, DDR4 ≥0.38 s) and ≥24x at 65 C;
- multi-chip events are ≤10%, with no new mechanism at >2x its 32/64 ms rate;
- the servo grade holds for ≥95% of modules.

**NO-GO** if the interval is <4x the window at 65 C.

**Phases 2-3 (M4-18).**
- DDR4 CXL and DDR5-tester soaks of 1,000 h: 0 UE, corrected errors within 2x of model.
- p50/p99 latency at injected 1e-4.
- Self-refresh vs power-down power.
- One sky130 slot.

**Total $946k over 24 months** (was $943k).

### 11.5 Revised verdicts

- **PHYSICALLY POSSIBLE? Yes** for relaxed refresh behind a side-band code. **No** for the delayed-strobe sense-amp flag as specified (killed).
- **STEP CHANGE IF IT WORKS? Yes, smaller:** refresh energy and busy time ~9x (DDR5) to ~13x (retired DDR4) at 85 C with chipkill. The range and module value are in §11.3. New-cell margin stays 1.88x with no flag bonus.
- **PROVABLE WITH $1M? Partly.**
  - **Yes:** DDR4 physics; DDR5 post-SEC statistics; census; servo test; soaks. Phase 1 is ~$124k and decides at M6.
  - **No:**
    - raw 1b/1c maps (vendor test mode);
    - 2e-19 per read directly (bounded by census plus model);
    - the new-die sort flow (paper only).

### 11.6 Pre-red-team verdicts (kept for the record)

- **PHYSICALLY POSSIBLE? Yes.** Standard coding theory on measured retention tails; the commodity half needs no new physics. The one unknown, the error statistics at 1e-4 (cluster geometry, VRT growth, flaggable share), is a measurement, not a law.
- **STEP CHANGE IF IT WORKS? Yes on refresh energy: ~15x (range 7.7-30x) on today's DRAM.** Refresh-blocked time falls 7.6% → 0.5% at 16Gb and 41% → 2.6% at 64Gb. On margin, 1.88x for new cells (50 → 26.6 mV, Cs halved). But margin and refresh share one error budget, flags add only ~8%, and at module level idle power falls just 14-16% ($0.041/GB).
- **PROVABLE WITH $1M IN 24 MONTHS? Yes** for the binary error-physics GO/NO-GO (~$96k, month 6) and an FPGA CXL soak (~$943k all-in). **Partly** for flags (timing proxy plus a sky130 latch, not new-cell silicon). **No** for proving 2e-19 per read directly; it is extrapolated.

### 11.7 FINAL STATUS: DOWNGRADED

**Reason.** All 19 objections are valid in whole or part, and no physics wall appeared for relaxed refresh behind a side-band code. Four things changed:
- **The flag leg is killed.** A delayed strobe sees skew, not signal, and even ideal flags are net negative on die area.
- **The commodity headline falls from 15x to ~9x** at 85 C on DDR5. Three corrections drive this: chipkill kept, DDR5's real 32 ms window, and its post-on-die-SEC error structure. Retired DDR4 behind CXL stays ~13x.
- **The strategic 64Gb and value claims shrink.** Recovery falls from ~38 to ~6-16 points, and the value is ~$3.9 per module.
- **Provability falls from "yes" to "partly".**

The concept's promise (weak bits ship behind a controller) stands, as a smaller, better-specified claim.
