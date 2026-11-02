# MARGIN STACK: segment-gain, double-sampled, ECC-budgeted sensing that cuts the cell capacitor ~10x on oxide-access DRAM

NEW DRAM Stage 3 dossier. Author: agent `dosw-margin-stack`, 2026-11-02. Slug `margin-stack`.

Inputs: `models/margin-stack.py` (re-run 2026-11-02, exit 0, output identical to `research/stage3/margin-stack_model_output.md`), `research/stage3/margin-stack_notes.md`, `research/assumptions/dos-margin-stack.md`, and the source logs in §10.

Tags: [REPORTED] logged source, usually a snippet; [ESTIMATE] model or hand arithmetic; [SPECULATIVE] unmeasured physics; [training knowledge] no logged URL.

Program month M0 = 2027-01-01.

**Red team (2026-11-02).** Four reviewers raised 19 objections; all are answered in §11 and in `research/redteam/responses_margin-stack.json`. The model now carries a RED-TEAM REVISIONS block (sections R1-R12 of `research/stage3/margin-stack_model_output.md`). Sections 0, 2, 5 and 9 are updated where marked "(revised after red team)". **FINAL STATUS: DOWNGRADED.**

---

## 0. Header

| Field | Value |
|---|---|
| Name | MARGIN STACK |
| Thesis | Today's ~17,800-electron bit exists to beat bitline capacitance and amplifier offset, not noise. A 3-transistor gain stage per 32 cells, correlated double sampling (CDS) and a raw-BER-1e-4 row code shrink an oxide-access 4F2 cell's capacitor from 5.4 to ~0.5 fF. That is a 120 nm stub instead of a 1.3 µm, aspect-ratio-62 pillar. **(Revised after red team.)** The design is now a 2-pillar gain FET per 64 cells with one comparator per 4 columns, read by signal-first double sampling, plus an ECC-budgeted retention quantile. 0.5 fF stays the planning cell, with 1.0 fF as the fallback. The win is the capacitor module's resource intensity and 3D readiness, at a +9% to +25% $/bit penalty. |
| Rank / EV | 1 of 10; EV 75 = S3 x P5 x D5. **(Revised after red team)**: owner suggests S2 x P4 x D3 = **24**, with S for the narrowed step, P because the pessimistic case misses 0.5 fF, and D because the VCT terms stay projected |
| Category | sensing/periphery |
| Lineage | Device-lens STUB (physics) merged with system-lens Margin Stack (framing, global-line levers, shared MPW) |

**Constituent ideas** (id: idea; technique; Stage 2 or triage verdict; role)
- I-00257: same-step VCT gain FET; SCAMPER-Substitute; ADVANCE 62.6; the gain stage.
- I-11559: ECC-paid capacitor; Phase B lens; ADVANCE 67.1; 7σ → 3.72σ.
- I-11148: erasure-flagging SAs; Scarcity and constraint as engine; ADVANCE 67.1; flag, demoted to telemetry.
- I-05218: CDS sense amps; First principles; HOLD 61.2; CDS, now load-bearing.
- I-11588: negative-capacitance bitline; Phase B lens; ADVANCE 65.9; neutraliser add-on.
- I-04613: soft-decoded shallow pillars; Assumption inversion; HOLD 60.0; soft information (1.2x).
- I-07812: "local post offices", an SA per 32 cells; Perspective shift / personas; HOLD 60.6; segment framing.
- I-11545: sense layers every 16 tiers; Phase B lens; ADVANCE 65.6; 3D-tier segment.
- I-05154: partial-charge "sip" read; First principles; HOLD 59.4; self-referencing needs local gain.
- N-04: charge-transfer pre-sense; Phase B cell-physics lens; ALIVE; add-on.
- N-40: hierarchical 64-cell bitlines; Phase B 3D/process lens; ALIVE; gain must sit in the array.
- N-27: in-tier oxide SAs; Phase B materials lens; ALIVE; oxide-built amp.

**Verdicts (revised after red team; see §11)**
- **PHYSICALLY POSSIBLE? Yes.** No new physics. The new design pairs a 2-pillar gain FET with 64-cell segments and 4:1-muxed signal-first double sampling, and treats RTN as a heavy tail, not a Gaussian. Its sensing-limited cell is **0.13 / 0.29 / 0.74 fF** (optimistic / central / pessimistic). 0.5 fF closes in the central case (P(err) 8e-7 against a 9e-5 target) but **not** in the pessimistic one; the 1.0 fF fallback closes in all three. Retention needs the aged 1-in-2e5 IGZO leakage quantile at ≤ 586 aA, and the model's own inputs give ~100-260 aA. The 1e-10 tail derived from those inputs is 1.5-5.5 fA, so a 1e-10 requirement would fail.
- **STEP CHANGE IF IT WORKS? Narrowed: capacitor-module resource intensity and 3D readiness.** The capacitor is 10.8x shorter (5.42 → 0.5 fF, AR 62 → 5.7; 5.4x at the 1.0 fF fallback). That means ~10x less HAR capacitor etch (PFAS, He-cooled hours), ~100x less ZrO₂/TiN ALD exposure and no Ru/k>50 push. A 3D lateral capacitor of 63-127 nm (vs ~450 nm) breaks even at ~10-13 tiers instead of ~26, if a 3D host adopts it. **It is a penalty, not a step, on $/bit (+9% to +25%, central +17% vs plain oxide 4F2) and density (-11%).** Array energy improves only 1.3x and latency not at all (~14 ns read chain). Refresh gains (2-12x) are conditional and belong mostly to oxide access.
- **PROVABLE WITH $1M IN 24 MONTHS? Partly.** The decisive experiment costs $563k, inside a $999k plan, with GO/NO-GO at M17. It measures the circuit residual (22FDX emulator with ratio-matched coupling), error pairs (DRAM Bender), IGZO gain-FET RTN at a 1-3 ns gap (a BEOL-IGZO-on-SKY130 carrier) and the 2e-5 leakage quantile directly on ≥ 1e6 cells after a 1,000 h stress. VCT coupling, the VCT sidewall tail and the added mask count remain projections (field solver, process emulation).

<details><summary>Pre-red-team verdicts (superseded, kept for traceability)</summary>

- **PHYSICALLY POSSIBLE? Yes.** No new physics. The thermal floor at raw BER 1e-4 is 0.024 fF, 20x below the 0.5 fF planning cell. Mismatch, coupling, wordline kick and the oxide leakage tail set the size, and all of them are engineering terms. The cut is legal only with oxide access: a silicon 13 fA tail empties 0.54 fF in ~3 ms.
- **STEP CHANGE IF IT WORKS? Yes, on capacitor-module capital and PFAS, plus 3D readiness.** The capacitor is ~10.8x smaller: 5.42 → 0.5 fF, 1,300 → 120 nm tall, AR 62 → 5.7. Array energy per access falls ~2.3x [ESTIMATE]. The stretch is 17-40x [SPECULATIVE]. **It is no step on $/bit** (-3% to +4%) **or density** (-8% against plain 4F2).
- **PROVABLE WITH $1M IN 24 MONTHS? Partly, strongly.** One 22FDX MPW, IGZO coupons and a DRAM Bender study settle the circuit question by M16-17: post-CDS residual, coupling and error clustering. The decisive experiment costs $520k (the model's $675k "experiments alone" line adds spin 2 and IP); with two founders the plan is $955k. No oxide VCT array is built. The oxide terms come from coupons and are combined with the silicon results by projection.


</details>

---

## 1. How it works

*Pre-red-team description. The revised sense chain is in §2.10 and §11.1: 64-cell segments, a 2-pillar gain FET, a 4:1-muxed signal-first DS comparator and a ~14 ns read chain.*

A DRAM bit is a bucket of charge behind a switch. To read it, the switch opens and the charge spills onto a bitline shared by 512 cells. The bitline holds ~35 fF, about 6.4 times the 5.4 fF cell, so the bit shows up as only ~50 mV. A latch must tell that from its own random imbalance (offset) and from neighbour noise, correctly, on ~17 billion cells. That is why the capacitor is a pillar 1.3 µm tall and 21 nm wide. Etching, coating and propping up those pillars is one of the hardest, most chemical-hungry steps in a fab.

MARGIN STACK stacks three tricks:

1. **Short wires with local gain.** Cut the bitline into 32-cell segments of ~1.5 fF. Each segment drives the gate of its own "gain FET". A 0.5 fF cell gives 6 mV on a 35 fF line, but 107 mV on a 1.5 fF segment.
2. **Correlated double sampling.** The gain FET has a ~47 mV random offset. Read it twice, just before and just after the cell opens, and subtract the two readings. The offset cancels. Image sensors read a few hundred electrons this way [training knowledge].
3. **Let a code catch the stragglers.** Design for one bad bit in 10,000 and correct it with a row code (BCH, 80 check bits per 512 data bits). The array then needs 3.72 standard deviations of margin, not 7.

```
 TODAY (1-beta DDR5)                    MARGIN STACK (oxide-access 4F2)

 [5.4 fF] x512, 1.3 um pillars           [0.5 fF] x32, 0.12 um stubs
   |   |   |  ...  |                       |   |  ...  |
 ==+===+===+=======+==> latch SA         ==+===+=======+== segment ~1.5 fF
   bitline 35 fF, signal ~50 mV                        |
   must clear 7 sigma                     [gain FET] (+ reset, write FETs)
                                                       |
                                   ====================+==== global line ~6 fF
                                                       |
                          CDS: sample 1 (before WL) minus sample 2 (after WL)
                                                       |
                                 comparator -> bit (+ slow-decision flag)
                                                       |
                                 row BCH t=8: 512 + 80 bits; needs 3.72 sigma
```

A read takes ~3.6 ns [ESTIMATE]: charge sharing 60 ps, two samples of 0.7 ns, compare 0.5 ns, write-back 1.6 ns. That fits a DDR5 activate (~14 ns). IBM's 2007 silicon local amp did 1.5 ns [REPORTED].

**Why oxide.** A 10x smaller bucket empties 10x faster. Silicon access transistors leak ~13 fA in their worst cells. Kioxia/Nanya's IGZO transistors report under 1 aA [REPORTED]. Only that switch lets 0.5 fF hold a bit for seconds.

---

## 2. The physics and the numbers

### 2.1 Anchors (1-beta, A1 conventions)

- **Capacitance per height.** ε0 x 3.9 / EOT 0.55 nm = 62.8 fF/µm². On a 21.1 nm pillar that is π x 21.1 nm x 0.0628 aF/nm² = **4.16 aF/nm**. So 5.42 fF needs 1,302 nm (AR 62), and 0.5 fF needs **120 nm (AR 5.7)**.
- **Bitline signal.** Cbl = 512 x 0.06 + 4 = 34.7 fF. Signal = (0.525 - 0.155) V x 5.42/40.1 = **50.0 mV**, reproducing A1. That is 7σ x 7.14 mV.
- **Charge.** 5.42 fF x 0.525 V / q = **17,762 e-**. At 0.5 fF x 0.5 V it is **1,561 e-**.
- **ECC.** Q⁻¹(1e-4) = 3.719σ against 7σ: **1.88x**.
- **Thermal floor.** kT/C on a 1.48 fF node at 85 °C is 1.83 mV rms. The floor is Cs ≥ 0.024 fF, even with no kTC cancellation.

### 2.2 The signal equation and what each lever buys

On a segment, S = 0.425 V x Cs/(Cs + Cseg). The array works when S(1 - 2α) - D ≥ 3.72 x √(σ² + (0.05 S)²). Here α is neighbour coupling per side, D the deterministic kick residual, σ the random residual, and 5% the stub spread.

| Case | Cs (fF) | Cut | Height / AR |
|---|---|---|---|
| A. 1-beta, 512-cell line, no ECC | 5.42 | 1.0x | 1,302 nm / 62 |
| B. Oxide 4F2, same latch SA | 4.63 | 1.2x | 1,112 / 53 |
| C. + raw-BER 1e-4 ECC | 2.31 | 2.3x | 556 / 26 |
| D. + neutraliser, Cn/Cbl 0.5 | 1.26 | 4.3x | 303 / 14 |
| E. Charge-transfer pre-sense (3 mV residual) + ECC | 0.91 | 5.9x | 219 / 10 |
| F. Concept base case as written | 0.54 | 10.1x | 129 / 6.1 |
| G. Gain + ECC, no CDS, 1 pillar (σVt 47 mV) | 1.77 | 3.1x | 425 / 20 |
| H. Same, 4 pillars (σVt 24 mV) | 0.60 | 9.0x | 145 / 6.9 |
| **I. Gain + CDS + ECC, optimistic / central / pessimistic** | **0.09 / 0.14 / 0.32** | 59 / 40 / 17x | 22 / 33 / 77 nm |
| **J. (revised after red team) 2-pillar gain FET, 64-cell segment, muxed signal-first DS, RTN heavy tail, optimistic / central / pessimistic** | **0.13 / 0.29 / 0.74** | 41 / 19 / 7.3x | 32 / 69 / 178 nm |

**Critics' corrections carried.** Row F assumed a 1.0 fF segment, 40 mV, and no coupling or kick. Use instead a 1.48 fF segment (32 x 0.04 + 0.2 fF), a Pelgrom σVt of 47 mV (AVT 2.5 mV·µm on a 15 x 60 nm pillar; ESTIMATE, no IGZO AVT found), α = 0.1 and the kick. Then gain plus ECC **without CDS needs 1.77 fF: 3.1x, not 10x**. **CDS is load-bearing, not the stretch.** Also:
- the neutraliser gives 1.26 fF, not 0.96;
- charge-transfer pre-sense needs a ≤ 1.6 mV residual for 0.5 fF, since each mV on 35 fF costs 35 aC;
- Stage 2 capped neutralisation at ~2x and soft decoding at 1.2x.

### 2.3 Post-CDS residual (central, 85 °C, at Cs = 0.25 fF)

| Term | mV rms |
|---|---|
| Gain-FET Vt mismatch (47 mV) | cancelled by CDS |
| Comparator 3 mV / (gain 3 x 0.53 gm at a -4σ FET) | 1.89 |
| Sampling kTC, 2 x 10 fF, / gain | 0.33 |
| Oxide 1/f + RTN between samples **[SPECULATIVE]** | 4.0 |
| Wordline kick, random part | 2.4 |
| **σ_res = √(4.0² + 1.89² + 0.33² + 2.4²)** | **5.0** |

**(Revised after red team.)** This budget understated three things: the gain FET's drive, the comparator's pitch and the RTN statistics (DEV-02/03, CIRC-01/04/06). The revised central case, at 0.5 fF on a 64-cell, 2.81 fF segment, is: comparator 4.28 mV (G = 0.90), sampling kTC 1.56, segment-reset kTC 1.22 (no longer cancelled), reset injection 1.0, 1/f 2.0, kick 1.25. That gives a **Gaussian σ of 5.37 mV, plus an RTN heavy tail** (η = 4.1 mV, w = 0.025, 1e-4 quantile 22.6 mV). See §2.10.

**Two new terms.**
- **Wordline kick-back.**
  - Charge: half the access FET's channel charge (0.5 x 49 aF x 2 V) plus overlap (10 aF x 3 V) = 79 aC.
  - On a 1.73 fF node that is a **46 mV mean kick**. On a 35 fF line it would be 2.3 mV, which is where Stage 2's "~2 mV" holds.
  - A stored '0' turns on harder, adding a 7.1 mV asymmetry.
  - After 90% dummy-edge cancellation, D = 8.1 mV deterministic plus 2.4 mV random remain.
- **The bias conflict.** A same-step gain FET inherits the high Vt that buys < 1 aA, so it is off at a 0.5 V precharge. It needs a pulsed negative read-source line or a back gate to reach ~0.4 V overdrive.

**Hand check, row I central** (Cs = 0.14 fF): S = 425 x 0.14/1.62 = 36.7 mV; after 20% coupling, 29.4 mV; after D (8.6 mV at this node size), 20.7 mV. Needed: 3.72 x √(5.0² + 1.8²) = 20.0 mV. ✓

### 2.4 ECC, flags, clustering

- **BCH t=8** over 592 bits at raw BER 1e-4 fails 2.3e-17 per read, about one uncorrectable read per 0.9 server-years at 100 GB/s.
- **Flags buy ~4%, not "half the parity".** The best Gaussian window catches 83% of errors but flags 3.9x as many correct bits. Allowed raw BER rises only to 1.4e-4 (80% flaggable) or 1.7e-4 (100%), and the code gets no shorter. RAW-BER CONTRACT adds that refresh latches retention errors to confident values. The concept's "≥ 80% flagged" criterion is therefore secondary.
- **Same-codeword pairs are the threat.** At 1% pairs, allowed raw BER falls to 6.3e-5. At 10% it falls to 1.7e-5 (0.90x margin). A bad segment amp hits 32 codewords once each. Pairs come from row causes: weak wordlines, hammer, adjacent VRT cells.

### 2.5 Retention sets the planning cell

Retention t = Cs x droop / (I_leak + I_dielectric). At a 75 mV droop and 85 °C:

| Cs | 10 aA tail | 100 aA | 1,000 aA | Max tail, 64 ms | Max tail, 1 s |
|---|---|---|---|---|---|
| 0.25 fF | 1.8 s | 187 ms | 19 ms | 293 aA | 19 aA |
| **0.5 fF** | 3.5 s | 372 ms | 37 ms | **586 aA** (37.5 aC / 64 ms) | 38 aA |
| 1.0 fF | 6.5 s | 738 ms | 75 ms | 1,172 aA | 75 aA |

- **Correction carried.** The concept's "0.8-81 s at 1-100 aA; ~6 ms at 13 fA" used a 150 mV droop against its own 75 mV convention. At 75 mV, 0.54 fF on a silicon 13 fA tail lasts **3.1 ms**.
- With CDS working, 0.5 fF can droop 370 mV: 1.8 s at 100 aA. The dielectric (1e-8 A/cm²) caps any cell at ~47 s.
- OCTRAM's "< 1 aA" is likely a median; the 1-in-1e10 tail is unpublished.
- **The 0.5 fF planning cell is set by that tail, not by sensing.**
- **(Revised after red team.)** Derived from the inputs (σVt 50 mV, SS 85-100 mV/dec), the 1e-10 tail is 1.5-5.5 fA, which fails 586 aA. The requirement is now an **ECC-budgeted quantile**: 1e-5 of the raw-BER budget goes to retention-weak cells, so the allowed leaky-cell fraction is 2e-5. That quantile is 113-261 aA fresh and 101 aA aged with a -0.1 V negative-WL reserve, and ≥ 1e6 cells observe it directly (§2.10).

### 2.6 Energy, area, cost, 3D

- **Energy per sensed bit:** 20.1 fJ at 1-beta. MARGIN STACK: 0.99 local + 3.00 global restore + 2.40 two samples + 2.0 comparator = **8.8 fJ** [ESTIMATE; 6 fF global line].
- **Refresh, 16Gb die:** 12.2 mW (1-beta, 64 ms) vs **0.43 mW** (0.5 fF, 100 aA, droop-optimised, 2x guard, 917 ms). Oxide access supplies most of this.
- **Area (correcting the concept's "~9%, flat"):** 4 extra 4F2 sites per 32 cells, so **+12.5% array and +8.8% die**. That gives 0.701 Gb/mm²: 1.57x 1-beta, but -8% against plain 4F2 VCT (0.762).
- **Cost:** if the capacitor module is 10/15/20% of wafer cost [unsourced], $/bit is **+3.6 / +0.4 / -2.8%**, or $1.44-1.53/GB against $1.48. This includes one strap mask (1.2%).
- **(Revised after red team.)** The design actually adds 2-4 EUV-class layers (8.7-17.4% of the wafer), BCH parity (+6.2% die) and 64-cell segments (+5.5% die). Density is then **0.677 Gb/mm² (-11% vs plain 4F2)** and **$/bit is +9% to +25% (central +17%)**. A red-team search found no sourced module share (§2.10).
- **3D:** a tier's lateral capacitor shrinks from 450 to **63 nm**. Per-tier density rises 2.8x, and break-even with 1-beta falls from ~26 to **~10 tiers**.

### 2.7 Against 1-beta DDR5 (revised after red team)

| Metric | 1-beta DDR5 | MARGIN STACK, oxide 4F2 (pre-red-team) | **Revised after red team** |
|---|---|---|---|
| Capacitor | 5.42 fF, 1,302 nm, AR 62 | 0.5 fF, 120 nm, AR 5.7 | 0.5 fF planning (1.0 fF fallback: 240 nm, AR 11.4) |
| Stored electrons | 17,762 | 1,561 | 1,561 (3,121 at 1 fF) |
| Margin required | 7σ | 3.72σ + BCH t=8 | P(err) ≤ 9e-5 per bit (Gaussian + RTN tail) + 1e-5 retention share, BCH t=8 |
| Sense architecture | latch SA per 512-cell BL | 3T per 32 cells, CDS comparator per column | 2-pillar gain + reset + write-back per 64 cells; 4:1-muxed signal-first DS |
| Density | 0.447 Gb/mm² | 0.701 (plain 4F2 0.762) | **0.677** (-11% vs plain 4F2) |
| Energy per sensed bit | 20.1 fJ | 8.8 fJ [ESTIMATE] | **15.2 fJ** (1.3x) |
| Read chain | ~14 ns tRCD | 3.6 ns | **~11.4 ns decisions + 3.1 ns restore** |
| Refresh power, 16Gb | 12.2 mW | 0.43 mW (100 aA tail) | 1.0-6.5 mW, conditional (2-12x) |
| $/GB | $1.48 | $1.44-1.53 | **+9% to +25% vs plain 4F2** |
| Added masks | — | +1 DUV; no EUV | **+2-4 EUV-class layers** |

### 2.8 Sensitivity

Required Cs (fF) by random residual and coupling (32-cell segment, kick included):

| σ_res | α 0.05 | α 0.10 | α 0.20 |
|---|---|---|---|
| 8 mV | 0.17 | 0.19 | 0.28 |
| 13 | 0.26 | 0.30 | 0.44 |
| 20 | 0.41 | 0.49 | 0.74 |
| 40 | 1.04 | 1.29 | 2.51 |

- **Thresholds.** Cs ≤ 0.5 fF needs σ_res ≤ 23.5 / 20.5 / 14.5 mV at α 0.05 / 0.10 / 0.20; Cs ≤ 0.25 fF needs ≤ 12.3 / 10.6 / 7.1 mV; above 34 mV (α 0.10), Cs ≥ 1 fF.
- **Segment length.** 64 cells cost 4.4% of the die and need 0.20 fF. 16 cells cost 17.5% for 0.11 fF. 32-64 is the sweet spot.
- **Kick limits only the stretch.** At 0.5 fF with *zero* cancellation, D ≈ 43 mV and the central case still closes: 86 - 43 = 43 mV, against 27 mV needed [ESTIMATE, hand].
- **Without ECC** (k = 7), central CDS needs ~0.25 fF and pessimistic ~0.77 fF [ESTIMATE, model functions at k = 7, not printed by the model]. If CDS works, ECC is insurance, not the lever.

### 2.9 GO / NO-GO (pre-set)

**GO** if all three hold:
1. The post-CDS residual is ≤ **20 mV** at 85 °C, worst-case neighbour data, coupling folded in. That means raw BER ≤ 1e-4 at 0.5 fF (≤ 1.4e-4 if ≥ 80% of errors are flaggable). ≤ 11 mV unlocks 0.25 fF.
2. **< 1%** of errors are same-codeword pairs.
3. The IGZO 1-in-1e10 tail at 85 °C is ≤ **586 aA** (≤ 59 aA for a 10x refresh cut).

**NO-GO** if the residual is > **34 mV** (Cs ≥ 1 fF, which a no-CDS 4-pillar FET already gives) or pairs are > **10%**.

**(Revised after red team) GO / NO-GO.**
- **GO** needs both of the following:
  - a projected raw BER ≤ 9e-5 at Cs 0.5 fF, 85 °C and worst-case data. It is built from the measured 22FDX BER and Gaussian residual (≤ 12 mV) at the field-solver VCT α, which must be ≤ 0.25 (with a sensitivity case reported at 1.5x α); the measured IGZO gain-FET RTN (1e-4 between-sample jump quantile ≤ 44 mV); and pairs < 1%;
  - an aged (post-1,000 h stress) 2e-5 IGZO leakage quantile ≤ 586 aA, or ≤ 1,881 aA (conditional) if the residual supports 241 mV of droop.
- **NO-GO** if any of these holds: the projected BER exceeds 1e-4 at 1.0 fF; pairs exceed 10%; or the leakage quantile exceeds the 1.0 fF limit (1,172 aA at 75 mV droop; 5,529 aA at 354 mV).

### 2.10 Red-team revisions to the numbers (revised after red team)

All numbers come from model sections R1-R12.

| Item | Pre-red-team | Revised | Objection |
|---|---|---|---|
| Segment / gain FET | 32 cells, 1 pillar, G = 3 (5 µA at 0.4 V) | 64 cells (Cseg 2.81 fF), 2 pillars, Vov 0.6 V, gm 9 µS, I 2.7 µA, **G 0.90** (0.48-1.87) | DEV-02, CIRC-06 |
| Global line / comparator | 6 fF, one CDS comparator per column (needs ~1.15 µm² of 0.443) | 12 fF, 1,024-cell column (0.885 µm²); **one comparator per 4 columns**, signal-first DS; ~0.55 µm² per column | CIRC-01 |
| RTN | 4 mV Gaussian | exponential tail: q/(CoxWL) 3.28 mV per pillar x 2.5; 10% active, 25% toggle. **1-pillar 1e-4 quantile 40-65 mV; 2-pillar 22.6-36 mV** | DEV-03, CIRC-04 |
| Sensing-limited Cs | 0.09 / 0.14 / 0.32 fF | **0.13 / 0.29 / 0.74 fF**; 0.5 fF closes centrally, not pessimistically | DEV-02/03, CIRC-01/04 |
| Coupling tolerance at 0.5 fF | σ_res ≤ 20.5 mV at α 0.1 | α ≤ 0.25 (central noise), 0.02 (pessimistic) | PROC-02, CIRC-03 |
| Leakage requirement | 1e-10 tail ≤ 586 aA (not derived) | Derived 1e-10 tail 1.5-5.5 fA fresh. **ECC-budgeted 2e-5 quantile**: 191 aA fresh, 1,304 aA aged, 101 aA aged with -0.1 V NWL (SS 90). The averaged DUE stays at 2.3e-17 | DEV-01, PROC-03, DEV-05 |
| Refresh | 917 ms, 28x | 591 ms (central tail) to 94 ms (high tail): 11.8x-1.9x, conditional, mostly from oxide access | DEV-01 |
| Timing | 3.6 ns | decisions 11.4 ns (13.4 ns with WL rise vs 14 ns tRCD), restore 3.1 ns | DEV-02, CIRC-01 |
| ECC | latency not costed | BCH slow path on 5.75% of reads at 1e-4 (+~15 ns), 0.06% at 1e-6. On-die code for wide-IO parts; DDR5 x4 RDIMMs use the side band, losing chipkill | CIRC-05 |
| Area / density | +8.8% die, 0.701 | segments +5.5%, parity +6.2%, decoders +0.5%: x1.125, **0.677 Gb/mm²** | CIRC-02 |
| Added layers / $/bit | 1 DUV (1.2%), -3% to +4% | 2/3/4 EUV-class (8.7/13.0/17.4%): **+9% to +25%, central +17%** | PROC-01, PROC-04, IND-01 |
| 3D | 450 → 63 nm, ~10 tiers | 0.30 / 0.79 fF sensing-limited in a 3 fF tier segment (central / pessimistic); at 0.5-1.0 fF: 63-127 nm, 2.2-2.8x per tier, ~10-13 tiers | — |
| Energy | 8.8 fJ (2.3x) | 15.2 fJ (1.3x) | CIRC-01 consequence |

**Top-up ideas.**
- **I-12302 (plate-strip sensing)**: it gives 85 mV at 0.5 fF on a 2 fF strip, against 64 mV on the 64-cell segment. That is the same signal class, so its value is in integration: no buried-BL cut, and a separate BEOL gain FET with its own Vt. It is carried as a process-emulation alternative for PROC-01.
- **I-12627 (series write gates)**: if the two gates' tails were independent, each would need only q = 4.5e-3, i.e. 0.8 decade plus a ~10x stack effect. In a same-step VCT, though, a second gate also lengthens the gain FET, and film variation along one pillar is shared. It is therefore a coupon split that measures tail correlation, not the central design.

---

## 3. What is new versus prior art

| Prior art | Date | Gap left |
|---|---|---|
| IBM (Barth et al.): 3T micro-SA per ~32-cell local bitline, 1.5 ns | ISSCC 2007 / JSSC 2008 | Si eDRAM; no CDS; no capacitor co-design |
| Hierarchical / local-bitline sensing; selective bitline activation (Udipi, ISCA 2010); FGDRAM (MICRO 2017) [Stage 2 critics, training knowledge] | 2010-17 | Segmentation for energy, not to shrink Cs |
| Gain-cell eDRAM: Si 2T/3T GC-eDRAM (BGU), UT Austin IGZO eDRAM, imec/Kioxia IGZO 2T0C [Stage 2 critics] | 2010s-20s | Removes the capacitor but needs 2-3 FETs per cell and a different read; not a 1T1C capacitor cut |
| SEL DOSRAM: oxide 1T1C over Si SAs (US 12,230,314; 11,694,594; 11,488,528) | 2010s-20s | No Cs or CDS seen; main FTO risk |
| Hi-ECC (Wilkerson et al.): strong BCH cuts eDRAM refresh ~93%; ECC(552,512) gain-cell refresh study (arXiv 2607.16042, named by a Stage 2 critic, not re-checked) | ISCA 2010; 2026 | ECC spent on refresh; no logged source spends it on capacitor size (Stage 2: "none found") |
| Offset-cancellation SAs (US 11,763,878) | shipping | Global bitline only |
| Charge-transfer SAs (US 8,320,208); NC SA (US 8,872,938); SRAM NC bitlines; Blalock clamped-bitline SA; electrophysiology headstage capacitance neutralisation | 2000s-10s | No DRAM neutraliser found |
| Kioxia + Nanya OCTRAM, 275 Mb vertical IGZO, Ioff < 1 aA | Dec 2024 | Keeps the HAR capacitor |
| Kioxia 3D OCTRAM, 8 IGZO layers | Dec 2025 | No retention data |
| Samsung 16Gb 4F2 VCT (ISSCC 2026); 10a IGZO VCT die | Feb / Apr 2026 | No capacitor cut published |
| Samsung 16-tier VS-DRAM: back gate, bitline shield, horizontal capacitor | 2024-26 | Long capacitor per tier |
| Sequential / M3D sense tiers: CEA-Leti CoolCube, M3D DRAM periphery tier (arXiv 2008.11367), Monolithic 3D ion-cut patents [Stage 2 critics] | 2010s-20s | Si sense tiers; capacitor not sized to the segment |
| SK hynix vertical-gate 4F2 with bitline shielding | VLSI 2026 | No local gain |
| ETH SAFARI SoftMC, DRAM Bender, PaCRAM (388 DDR4 chips) | 2018-25 | Our test method |
| NAND soft-bit sensing (US 11,907,545); XED on-die error flags; static weak-cell erasure maps (US 8,898,544); Razor delayed sampling (MICRO 2003); Solar-DRAM weak-cell profiles; chipkill marking [Stage 2 critics, training knowledge] | 2003-24 | Static or timing flags; no per-read DRAM sense-amp erasure flag |
| Image-sensor source follower + CDS [training knowledge] | decades | Not memory |

**The genuine delta.** Every part is known; no snippet showed them combined into one margin budget on an oxide access device built to shrink the capacitor. Claimable:
1. A same-step oxide gain FET per segment, CDS through that FET, and Cs ≤ 0.5 Cseg with stub height ≤ ~10x diameter.
2. Kick compensation for short segments.
3. Biasing a high-Vt same-step gain FET.
4. Pair-aware codeword orientation.
5. A ≤ 100 nm lateral stub sized to a 16-tier segment.

No logged snippet shows an oxide VCT program publishing a capacitor cut. If DOSRAM already runs ~1 fF cells on short stacked bitlines, the novelty narrows to items 1-3.

**(Revised after red team, IND-02.)** A red-team search found SEL DOSRAM patents (US 12,051,726 / US 12,230,314). They describe local arrays of ~8 word lines over local SAs and state that a shorter bit line "allows the storage capacitance of the memory cell to be reduced". "Short bitline → smaller Cs" is therefore SEL prior art, and IBM + OCSA + Hi-ECC is an obviousness combination against a broad claim 1. The claimable remainder is narrow: the in-array same-step oxide gain FET with double sampling through it (including muxed signal-first DS), kick compensation, high-Vt biasing, and the 3D sense-tier stub. The ECC-budgeted retention quantile is Hi-ECC prior art and is not claimed. A patentability/FTO opinion comes before the first filing.

---

## 4. Show-stoppers and how persistence could get around them

*Pre-red-team table. Rows 1, 2, 5 and 7 are superseded by §2.10 and §11: coupling via extraction plus ratio-matched silicon; RTN as a heavy tail; the ECC-budgeted 2e-5 leakage quantile; 2-4 added EUV-class layers.*

| # | Show-stopper | Number | Workaround |
|---|---|---|---|
| 1 | Data-dependent coupling, which CDS cannot cancel | 0.5 fF needs σ_res ≤ 20.5 mV at α 0.1, ≤ 14.5 at α 0.2 | Shields (SK hynix, VS-DRAM); alternate-segment activation; differential reference; 64-cell segments |
| 2 | Oxide 1/f + RTN [SPECULATIVE] | 4 mV central; 10 mV alone gives ~0.25 fF [ESTIMATE, model functions]; the full pessimistic case (also α 0.15, 5.4 mV comparator) gives 0.32 fF | Shorter sample gap; 4-pillar gain FET; H-lean anneal (imec, ~30x less H-doping); multi-sample averaging |
| 3 | Wordline kick on 1.7 fF | 46 mV mean; D 8.1 mV after cancellation | Dummy edge; reference sample; lower overdrive. Threatens only ≤ 0.25 fF |
| 4 | Gain-FET bias and spread | Off at 0.5 V; -4σ FET keeps 53% gm | Pulsed read source; back gate; one Vt-adjust mask |
| 5 | Unknown IGZO leakage tail | ≤ 586 aA at 0.5 fF; 13 fA gives 3 ms | Retreat to 1 fF (≤ 1,172 aA, still 5.4x); droop optimisation; negative WL hold; repair tail cells |
| 6 | Clustered errors | 1% pairs → 6.3e-5; 10% → 1.7e-5 | Interleave codewords across mats; RFM/PRAC; BCH-12 in the RDIMM side band (iid to 3.3e-4) |
| 7 | Area and a mask | +8.8% die; strap 1.2% of wafer cost | 64-cell segments (4.4%); self-aligned strap |
| 8 | Soft errors at ~1,500 e-; row hammer in IGZO VCT | Both unmeasured; no Si junction should help soft errors [SPECULATIVE] | ECC; RFM/PRAC; neutron and hammer tests on the partner array |
| 9 | Emulation gap: 22FDX Si is not oxide | Si leaks; 1/f differs | Read right after write; add coupon oxide 1/f; real array after the raise |

---

## 5. The decisive experiment

### 5.1 Revised decisive experiment (revised after red team)

**Question.** Three parts:
- At Cs 0.5 fF, 85 °C and worst-case data, is the projected raw BER ≤ 9e-5? It is built from measured silicon circuit statistics, measured oxide gain-FET RTN at ns and an extracted VCT coupling.
- Are errors iid (< 1% same-codeword pairs)?
- Is the aged 2e-5 IGZO leakage quantile ≤ 586 aA?

The reviewers showed three measurements were missing: oxide-native ns double sampling, RTN at the right timescale, and a directly observed leakage quantile. All three are now in the plan.

1. **M0-5: simulation, extraction, process emulation.**
   - SPICE Monte Carlo of the 64-cell / 2-pillar / 4:1-mux DS chain.
   - A 3D field solver for α on published 4F2 VCT geometry (Samsung ISSCC 2026, SK hynix VLSI 2026), with dimensions swept ±30%.
   - Process emulation (SEMulator3D-class, academic or partner) of the same-step 3T and the I-12302 plate-strip integrations.
   - *Gate:* ≤ 3 added critical layers (target ≤ 2) and α ≤ 0.25.
2. **M0-6: DRAM Bender pair study**, unchanged. *Exit:* pairs < 1%.
3. **M2-7: 22FDX MPW, 5 mm²** (the neutraliser and charge-transfer add-on block is dropped).
   - 64-cell segments with emulated 1/2/4-pillar gain stages, a pulsed read source and switchable kick compensation.
   - The full column cell: 4:1-muxed signal-first DS comparator, 4T restore latch and flag, in a ≤ 0.885 µm²-per-column layout (CIRC-01 gate).
   - Ratio-matched programmable coupling: MOM caps between neighbour segments and from a WL-emulation line, set to the extracted Cbl-bl/Cseg and Cwl-bl/Cseg within 20%, with α stepped 0.05-0.30.
   - BIST charge-injection margin sweep; unselected-cell disturb test for the plate-strip mode.
   - BCH t=8 decoder synthesis estimate (contractor).
4. **M2-13: BEOL-IGZO-on-CMOS carrier** (new; DEV-04, PROC-03, CIRC-03).
   - A SKY130 readout die (ChipFoundry shuttle, tape-out M4, second run M9) with on-chip fF sample-and-holds under top-metal landing sites.
   - IGZO FETs post-processed on the dies at ≤ 350 °C (Purdue Birck, Georgia Tech IEN or Stanford SNF):
     - ≥ 1e4 gain FETs at gate areas matched to 1 and 2 pillars (2,827 and 5,655 nm²). Measure Id-Vg and gm at 0.3-0.8 V overdrive, and the between-sample jump distribution at a 1-3 ns gap, 25-110 °C;
     - ≥ 1e6 hybrid 2T leakage cells (IGZO write FET on a Si read-FET gate; ≥ 2.5e5 per die over ≥ 4 dies), read over 10³-10⁵ s with a negative-WL-hold sweep from 0 to -0.5 V.
5. **M3-12: IGZO coupons**:
   - planar, plasma-etched-sidewall and dual-series-gate (I-12627: tail-correlation test) splits;
   - ~0.5 fF ALD ZrO₂/HfO₂ MIM;
   - 1/f spectra.
6. **M12-15: 1,000 h, 105 °C hold-bias stress** on coupons and carriers; tail re-measured (≤ 2x growth passes).
7. **M11-16: test.** 22FDX margin maps (20 chips, 5 mm²) crossed with α settings and mux/DS options; carrier RTN and leakage populations.
8. **M17: GO/NO-GO**, per the revised §2.9. The report carries a measured-vs-projected column.

| Budget item (revised after red team) | $ | When |
|---|---|---|
| DRAM Bender study (shared with RAW-BER CONTRACT) | 80,000 | M0-6 |
| SPICE MC + 3D field-solver α + process emulation | 55,000 | M0-5 |
| 22FDX MPW, 5 mm² x $17,997 + 20% U.S. route | 108,000 | M7 |
| EDA/PDK | 25,000 | M2-7 |
| Layout/verification contractor (22FDX + SKY130 carrier) | 55,000 | M2-7 |
| Packages, PCBs, probe cards | 30,000 | M9-12 |
| Bench: used SMUs, thermal forcer, FPGA, low-noise ns sampler | 50,000 | M6-11 |
| IGZO coupons (planar, sidewall, dual-gate splits) | 60,000 | M3-12 |
| BEOL-IGZO-on-SKY130 carrier: 2 runs ($30k) + die-level post-processing | 90,000 | M4-13 |
| 1,000 h 105 °C hold-bias stress | 10,000 | M12-15 |
| **Total** | **563,000** | |

What it still cannot measure: VCT-geometry α (it uses a field solver plus ratio-matched structures), the VCT etched-pillar leakage tail (planar and sidewall coupons are proxies), and the real added mask count (process emulation). Those are the first milestones of the raise, via partner VCT or OCTRAM silicon.

### 5.2 Pre-red-team version (superseded, kept for traceability)

**Question.** On silicon emulating an oxide 4F2 segment, is the post-CDS residual ≤ ~20 mV under worst-case data at 85 °C? Are errors iid (< 1% pairs)? Is the IGZO tail ≤ 586 aA?

1. **M0-4: simulation.** SPICE Monte Carlo on the 22FDX PDK with a VCT/IGZO model fitted to OCTRAM Ion/Ioff; partner TCAD for the kick charge split and α, with and without shields. *Exit:* σ_res ≤ 10 mV, α ≤ 0.1.
2. **M0-6: DRAM Bender study** (shared with RAW-BER CONTRACT). Emulate reduced charge on three vendors' DDR4/5 parts (truncated restore as in PaCRAM, reduced VPP, stretched refresh). Map raw BER 1e-5 to 1e-3 at 45-95 °C; log errors per 512-bit codeword and a reduced-tRCD flag proxy. *Exit:* pairs < 1%.
3. **M2-7: MPW design**, GF 22FDX, ~6 mm².
   - Array: 64k segments x 32 cells (2.1M); MOM stubs 0.125-1.0 fF; Cseg 0.8 or 1.5 fF; minimum and 4-finger gain FETs; pulsed read source; switchable kick compensation.
   - Global CDS with an auto-zeroed comparator, delayed-compare flag and trim DAC; aggressor patterns with shields on/off.
   - 64 emulated 35 fF lines with charge-transfer pre-sense and a neutraliser (Cn/Cbl 0.3-0.8).
   - BIST margin sweep by charge-injection DAC; AVT and MOM-spread monitors.
4. **M7-11: build.** Tape-out in August 2027, ~12-week fab, then packaging.
5. **M3-12: IGZO coupons** on the shared oxide run: minimum-size planar IGZO FETs, ~0.5 fF ALD ZrO₂/HfO₂ MIM, and 2T droop arrays (≥ 1,000 cells) read over 10³-10⁵ s at 25-110 °C, with a lognormal fit to the 1e-10 tail. Also IGZO 1/f/RTN spectra and a discrete CDS on IGZO gain FETs.
6. **M11-16: test.** Margin maps on 20 chips (42M cells, direct tail to 5.5σ). Raw BER vs Cs at 25/85/110 °C, crossed with patterns and with CDS, kick compensation and shields on/off. Extract σ_res, D and α; record pairs, flags and neutraliser stability (~210 errors per chip per full read).
7. **M16-17: GO/NO-GO.** Silicon σ_res plus coupon oxide 1/f gives the projected oxide σ_res, scored against §2.9.

**Facilities.** MPW: GF 22FDX via MOSIS 2.0 (USC ISI, GF partner since 2026-07) or CMC. Coupons: Purdue Birck, Stanford SNF or Georgia Tech IEN. An early ChipFoundry SKY130 pass ($15k per 100 chips) de-risks the BIST.

| Budget item | $ | When |
|---|---|---|
| DRAM Bender study (FPGA boards, parts, thermal, 0.5 FTE x 6 months) | 80,000 | M0-6 |
| SPICE Monte Carlo + partner TCAD | 30,000 | M0-4 |
| 22FDX MPW, 6 mm² x $17,997 (CMC 2026) + 20% U.S. route | 130,000 | M7 |
| EDA/PDK | 25,000 | M2-7 |
| Layout/verification contractor | 45,000 | M3-7 |
| Packages, PCBs, probe cards | 30,000 | M9-11 |
| Bench: SMUs, thermal forcer, FPGA, low-noise sampler | 60,000 | M6-11 |
| IGZO coupons: ~400 cleanroom h, staff, materials, readout | 120,000 | M3-12 |
| **Total** | **520,000** | |

In the portfolio, Bender and coupons are shared, so MARGIN STACK's increment is ~$260-320k [ESTIMATE: $520k less the $80k Bender study and part or all of the $120k coupons].

**Pass/fail, fixed now.** GO: σ_res ≤ 20 mV, pairs < 1%, tail ≤ 586 aA. NO-GO: σ_res > 34 mV or pairs > 10%. Add-ons: the neutraliser passes if stable at Cn/Cbl ≥ 0.5; charge-transfer pre-sense passes at ≤ 1.6 mV.

---

## 6. The $1M, 24-month plan

| Quarter | Work | Gate |
|---|---|---|
| Q1 2027 | Hire co-founder; Bender rigs; SPICE/TCAD; provisional #1 | G1: simulated σ_res ≤ 10 mV, α ≤ 0.1 (else 64-cell segments) |
| Q2 2027 | Bender maps; coupons; layout | G2: pairs < 1% (1-10%: add interleave, BCH-12; > 10%: K1) |
| Q3 2027 | Tape-out M7; bench | G3: leakage arrays work |
| Q4 2027 | Silicon ~M10; leakage data; provisional #2 | G4: tail ≤ 586 aA (K2) |
| Q1 2028 | Margin maps, splits; PCT | G5: CDS cuts offset ≥ 4x |
| Q2 2028 | **GO/NO-GO M16-17**; spin-2 design | G6: §2.9 |
| Q3 2028 | Spin-2 tape-out; partner reviews | Silicon booked |
| Q4 2028 | Spin-2 data; paper; raise | Partner LOI or JDA |

**Budget.** Decisive experiment $520k; spin 2 (after GO only) $110k; IP (2 provisionals, PCT, FTO search) $45k; two founders at $5k/month $240k; overhead $40k; reserve $45k. **Total $1.0M.**

**(Revised after red team.)** Decisive experiment $563k (§5.1); spin 2 (after GO only, 4 mm²) $86k; IP including a patentability/FTO opinion on the SEL DOSRAM and OCSA families $55k; capacitor-module cost-split study $15k; founders $240k; overhead $40k. **Total $999k.** The listed reserve is ~$1k; the real reserve is the ~$140-200k freed by portfolio sharing of Bender and coupons [ESTIMATE]. Gates G1-G6 follow the revised §2.9 and §9. Before the raise, ask a memory maker whether it would pay for capacitor-module deletion (IND-01).

Honest risk: $60k a year will not hire a seasoned DRAM designer. Fixes: equity, portfolio cost-sharing (~$200-260k freed [ESTIMATE]), NSF SBIR/DARPA/NSTC grants [training knowledge].

**Team**
- *Founder 1, architect/test/ECC:* from ETH SAFARI alumni or U.S. memory-systems groups.
- *Founder 2, recruited circuit expert:* an ex-Micron Boise DRAM sense-amp designer, or a **CMOS image-sensor readout designer** (onsemi, OmniVision [training knowledge]), whose CDS and source-follower Monte Carlo skills map onto the key unknown.
- *Contractors:* analog layout; TCAD via a university.
- *Advisors* [names are training knowledge]:
  - circuits: IBM micro-SA authors (Barth et al.), BGU/Bar-Ilan (A. Teman), EPFL (A. Burg), UT Austin IGZO eDRAM authors;
  - oxide devices: Georgia Tech (S. Yu, S. Datta), Purdue (P. Ye, K. Roy), Stanford (H.-S. P. Wong);
  - errors and codes: ETH SAFARI (O. Mutlu), UCLA (L. Dolecek).

**IP.**
- *First, at M2:* the segmented oxide 1T1C read method (same-step gain FET, CDS through it, Cs ≤ 0.5 Cseg), then kick compensation and high-Vt biasing.
- *M10:* pair-aware ECC orientation and the 3D lateral stub (with PIXEL-STACK). The neutraliser only if it proves stable.
- *M14:* PCT.
- *FTO risks:* SEL's oxide-memory estate (search before filing); Samsung/SK hynix offset-cancellation families; US 8,320,208 and US 8,872,938; NAND soft-bit patents, for the flag.
- IBM's ~2006-08 micro-SA filings are likely expiring [training knowledge; verify]. We do not claim the OCTRAM or VCT cell.

---

## 7. After the demo

**Who licenses or partners.**
- **Samsung:** 4F2 VCT die; its VS-DRAM already uses the back gate and shield we need.
- **SK hynix:** shielded vertical-gate 4F2, plus a 5-layer 3D DRAM at 56.1% yield (2024).
- **Kioxia/Nanya:** OCTRAM and 3D OCTRAM are the closest platform. Nanya, a DRAM maker needing differentiation, may be the natural first licensee [SPECULATIVE].
- **Micron:** reportedly skipping 4F2 (weak source); a 3D-tier licensee with U.S. fabs.
- **Foundries** (GlobalFoundries, TSMC, Intel): BEOL oxide eDRAM on logic, alongside HOT-SIDE MEMORY.
- **Display makers** (SEL, Sharp, LG Display): oxide-TFT know-how and FTO cross-licences, not DRAM fabs. CXMT is excluded by U.S. policy.

**What $10-50M buys.**
- *$10-15M:* a real oxide VCT array with same-step gain FETs and 0.25/0.5/1 fF stubs, through a joint development or 300 mm prototyping at Albany NanoTech (NSTC). Full reliability work: hammer, VRT, neutron soft errors, 1,000 h at 85-125 °C.
- *$25-50M:* a 1 Gb-class vehicle with a licensee, a 3D-tier version with PIXEL-STACK, and a margin-IP compiler, with ~25-40 staff.

**Standards.** With RAW-BER CONTRACT, a JEDEC "ECC-native" raw-BER grade and flag export through on-die ECC. The sense chain becomes CELL-WAFER FOUNDRY's reference periphery.

---

## 8. Resources and America

**Removed.** The AR-60 fluorocarbon etch (PFAS, under ECHA restriction review in 2026); helium-cooled etch hours (Qatar's 2026 shutdown); the SiN support lattice; ~100x of ZrO₂/TiN ALD exposure (∝ AR²) [ESTIMATE], easing Zr/Hf demand as hafnium rose from ~$5,000 to ~$13,115/kg by April 2026 [REPORTED]; and the push to k > 50 with Ru electrodes, which fleet-wide would need 26-176% of world ruthenium (A2).

**Added.** Indium and gallium in nm-thick IGZO films; the tonnage is tiny. Gallium faces Chinese export controls [training knowledge]. Ga-free channels (N-26) hedge it.

**EUV.** None added: one DUV strap mask. The host 4F2 EUV count is unchanged.

**Energy and water.** Not modelled; a 10x shorter capacitor cuts HAR-etch and ALD tool-hours. Scale: Micron's Clay complex, ~16 billion kWh/yr and up to 48 million gallons/day [REPORTED].

**U.S. build.** 22FDX is, to my knowledge, made in GF Dresden [training knowledge; verify], so the concept's "GF Malta 22FDX" needs checking. U.S.-fabbed options are SKY130 in Minnesota (SkyWater, an IonQ subsidiary since 2026-07) and GF 12LP at Malta [training knowledge]. Coupons and test run at Purdue, Georgia Tech and Stanford. Licensee volume: Micron Boise (second Idaho fab output late 2028 [REPORTED]) and Clay, NY.

---

## 9. Kill criteria (revised after red team)

Physics-only. Each has a date and a revival condition. The pre-red-team list is kept below the revised one.

**Revised list**
1. **K1, 2027-07-01 (pairs). Unchanged.** Three vendors at emulated 1e-4 show ≥ 10% same-codeword pairs after remapping. *Revival:* < 1% pairs on oxide cells.
2. **K2, 2028-04-30 (tail; revised after red team).** The aged (1,000 h, 105 °C) 2e-5 IGZO leakage quantile at 85 °C exceeds the 1.0 fF limit on both planar and etched-sidewall splits. The limit is 1,172 aA at 75 mV droop, or 5,529 aA if the measured residual supports 354 mV. That kills any cut beyond 5.4x. *Revival:* a negative-WL hold of ≥ -0.3 V, an anneal (imec H+O) or an In-lean channel that brings it to ≤ 586 aA.
3. **K3, 2028-04-30 (hard tail; revised after red team).** The aged 2e-5 quantile exceeds 6,352 aA, which fails 64 ms even at 5.42 fF. That kills the oxide-access premise. *Revival:* another access device below 586 aA at that quantile.
4. **K4, 2028-06-30 (residual; revised after red team).** The projected raw BER at **1.0 fF** exceeds 1e-4, using the measured Gaussian residual, the measured RTN and the extracted α. That kills the lever beyond 5.4x. *Revival:* α ≤ 0.1 with shields, or 4-pillar gain stages.
5. **K5, 2028-06-30 (double sampling).** DS through the same FET removes < 75% of the gain-FET offset. The planning cell then moves to ≥ 1 fF. *Revival:* spin 2 finds and fixes the drift source.
6. **K6, 2028-06-30 (coupling; revised after red team).** Extracted VCT α (field solver, calibrated against the ratio-matched MPW structures) above 0.25 moves the planning cell to 1.0 fF; above 0.34 it kills any cut beyond 5.4x. *Revival:* shields or a differential reference that cut α below 0.15.
7. **K7 (add-ons): retired after red team.** The neutraliser and charge-transfer blocks are dropped from the MPW and deferred.
8. **K8, 2028-12-31 (reproduction). Unchanged.** Spin 2 misses spin 1's residual by > 30%.
9. **K9, 2028-04-30 (RTN; new after red team).** The measured 1e-4 between-sample jump quantile of 2-pillar-area IGZO gain FETs (1-3 ns gap, 85 °C) exceeds 44 mV, which moves the planning cell to 1.0 fF. Above 82 mV it kills any cut beyond 5.4x. *Revival:* 4-pillar gain FETs, an H-lean anneal, or sort-time RTN screening with segment repair.

**Engineering gates (not physics kills; the founder framing keeps the concept alive through them)**
- **G-PROC, 2027-06-30:** process emulation shows ≤ 3 added critical layers for either the same-step or the plate-strip integration. With more, the $/bit penalty exceeds ~+25%.
- **G-CIRC, 2027-08-01:** the column cell, including 1/4 comparator, lays out in ≤ 0.885 µm². If not, move to 2,048-cell columns at G ~0.45.

<details><summary>Pre-red-team kill criteria (superseded, kept for traceability)</summary>


Physics-only. Each has a date and a revival condition.

1. **K1, 2027-07-01 (pairs).** Three vendors at emulated 1e-4 show ≥ 10% same-codeword pairs after remapping. This kills the ECC lever (allowed 1.7e-5). The concept survives if CDS meets the no-ECC numbers (~0.25 fF). *Revival:* < 1% pairs on oxide cells.
2. **K2, 2028-01-31 (tail).** The extrapolated IGZO 1e-10 tail at 85 °C is > 1,172 aA on two splits. That kills any cut beyond ~5.4x (Cs > 1 fF at 64 ms). *Revival:* an anneal or channel (imec H+O, In-lean) reaching ≤ 586 aA.
3. **K3, 2028-01-31 (hard tail).** The tail is > 6,352 aA, which fails 64 ms even at 5.42 fF. That kills the oxide-access premise. *Revival:* another access device below 586 aA.
4. **K4, 2028-06-30 (residual).** The projected oxide σ_res is > 34 mV with measured α. That kills the lever beyond ~5x. *Revival:* α ≤ 0.05 with shields and 64-cell segments.
5. **K5, 2028-06-30 (CDS).** CDS removes < 75% of the gain-FET offset. That kills CDS; the fallback is row H (0.60 fF, 4-pillar FETs, +9% array). *Revival:* spin 2 finds and fixes the drift source.
6. **K6, 2028-06-30 (coupling).** α with shields is > 0.20 *and* σ_res is > 14.5 mV. The planning cell rises above 0.5 fF, toward 1 fF. *Revival:* interleaving or a differential reference cuts α below 0.10.
7. **K7, 2028-06-30 (add-ons).** The neutraliser is unstable below Cn/Cbl 0.5, or the charge-transfer residual is > 3 mV. Those levers are dropped; the concept stands.
8. **K8, 2028-12-31 (reproduction).** Spin 2 misses spin 1's σ_res by > 30%: no raise rests on it until a third data set agrees.


</details>

---

## 10. Sources

All URLs are logged in `research/sources/*.jsonl`: mostly `dos-margin-stack.jsonl`, plus A1, A2, A3, B3, `dos-raw-ber-contract`, `dos-pixel-stack`, `dos-lean-array-module`, `dos-charge-river` and `dos-hot-side-memory`. Red-team response sources are in `resp-margin-stack.jsonl` (three WebSearches): SEL DOSRAM short-bitline patents, RTN amplitude-tail statistics, and a failed search for a sourced capacitor-module cost share.

**Red-team response sources**
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12051726
- https://arxiv.org/pdf/2001.03236
- https://researchonline.ljmu.ac.uk/id/eprint/14645/1/On%20the%20accuracy%20in%20modelling%20the%20statistical%20distribution%20of%20Random%20Telegraph%20Noise%20Amplitude.pdf
- https://www.iue.tuwien.ac.at/pdf/ib_2016/CP_2016_Rzepa_3.pdf
- https://www.patsnap.com/resources/blog/articles/reducing-etch-loading-effects-in-har-dram-capacitors/

**Circuits and ECC**
- https://researcher.ibm.com/publications/a-500-mhz-random-cycle-15-ns-latency-soi-embedded-dram-macro-featuring-a-three-transistor-micro-sense-amplifier
- https://courses.grainger.illinois.edu/CS534/fa2021/reading_list/9a.pdf
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11763878
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12106797
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8320208
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8872938
- https://www.academia.edu/11650472/Statistical_SRAM_Read_Access_Yield_Improvement_Using_Negative_Capacitance_Circuits
- https://global.ieice.org/en_transactions/Author/a_name=Travis%20N.%20BLALOCK
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11907545
- https://arxiv.org/pdf/2204.10387

**Oxide memory**
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12230314
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11694594
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11488528
- https://www.businesswire.com/news/home/20241209099702/en/Kioxia-Develops-OCTRAM-Oxide-Semiconductor-Channel-Transistor-DRAM-Technology
- https://blocksandfiles.com/2024/10/22/kioxia-developing-new-dram-scm-and-nand-tech/
- https://www.kioxia.com/en-jp/about/news/2025/20251212-1.html
- https://imec-publications.be/handle/20.500.12860/59908
- https://imec-publications.be/entities/publication/948b2190-065d-48d2-a9b9-4f4ecd22c234
- https://hg.gatech.edu/node/675050
- https://sites.utexas.edu/CRL/files/2021/05/IGZO_eDRAM_CIM_ISCAS_2021.pdf
- https://cris.bgu.ac.il/en/publications/a-16-kb-65-nm-gc-edram-macro-with-internal-bias-voltage-generatio/

**4F2 and 3D DRAM**
- https://semiwiki.com/forum/threads/isscc-2026-samsung-electronics-demonstrated-a-16gb-dram.24808/latest
- https://www.trendforce.com/news/2026/04/24/news-samsung-reportedly-produces-sub-10nm-10a-dram-working-die-using-4f-square-and-vct-targets-2028-production/
- https://www.sammyfans.com/2026/10/22/samsung-sk-hynix-micron-cxmt-4f2-dram-technology/amp/
- https://www.vlsisymposium.org/wp-content/uploads/2026/04/2026-VLSI-Technical-Tipsheet-REVISED-FINAL-NO-IMAGES-4.24.26.docx
- https://hao.cnyes.com/post/269690
- https://cloudnews.tech/samsung-and-sk-hynix-seek-another-solution-to-the-physical-limit-of-dram/
- https://www.guru3d.com/story/sk-hynix-achieves-yield-in-fivelayer-3d-dram-development
- https://www.techinsights.com/ja/node/37840
- https://patents.google.com/patent/US12193208

**Error characterisation and mismatch**
- https://arxiv.org/pdf/1805.03195
- https://arxiv.org/pdf/2206.09999
- https://www.arxiv.org/pdf/2502.11745
- https://arxiv.org/pdf/2211.05838
- https://people.cs.rutgers.edu/~mp2099/files/patel_isca2017_reach_paper.pdf
- https://research.ibm.com/publications/transistor-mismatch-properties-in-deep-submicrometer-cmos-technologies

**Fabrication routes and facilities**
- https://www.cmc.ca/globalfoundries-22fdx-fdsoi-22-nm-process/
- https://products.cmc.ca/Fabrication/DMT_Fab
- https://www.isi.edu/news/80945/mosis-2-0-revives-a-legacy-rehan-kapadia-outlines-a-bold-future-for-rapid-microelectronics-prototyping/
- https://allaboutcircuits.com/news/mosis-partners-with-globalfoundries-extending-40-year-prototyping-legacy
- https://www.eenewseurope.com/en/tiny-tapeout-sees-industrial-boost-as-it-recovers-from-efabless-closure/
- https://snfguide.stanford.edu/sites/default/files/sections/diplayfiles/fy20ratesheets-labuse.pdf
- https://mailman.ecn.purdue.edu/archives/list/bnc-all@ecn.purdue.edu/message/QV6GR6XQBKTW7PU5OCDG7VQOPHRKJ2JN/attachment/6/BRKFY24RatesvsCurrent.pdf
- https://senic.gatech.edu/about/rates
- https://www.ny.gov/roadmap-national-semiconductor-technology-center-new-york
- https://ionq.com/news/ionq-completes-acquisition-of-skywater-technology

**Resources and U.S. manufacturing**
- https://www.kitco.com/news/off-the-wire/2026-03-16/ruthenium-prices-hit-record-high-ai-boom-squeezes-supply
- https://news.metal.com/newscontent/103938701-from-stability-to-surge-the-overseas-hafnium-market-caught-between-ai-demand-and-supply-controls
- https://www.sgs.com/news/2026/04/safeguards-05026-echa-consults-over-seacs-draft-opinion-on-pfas-restrictions-under-reach
- https://www.caixinglobal.com/2026-03-16/qatar-helium-shutdown-adds-new-risk-to-chip-supply-chain-102423361.html
- https://www.sec.gov/Archives/edgar/data/0000723125/000072312526000015/mu-20260528.htm
- https://nyruralwater.org/node/3506
- https://www.wskg.org/news/2023-08-06/micron-estimates-needing-up-to-48-million-gallons-of-water-a-day-aiming-to-achieve-100-water-conservation

---

## 11. Red-team outcome

Four reviewers (DEV device physicist, PROC process veteran, CIRC sense-amp designer, IND industry strategist) raised 19 objections. Each is answered in full, with numbers, in `research/redteam/responses_margin-stack.json`. Model sections R1-R12 carry the arithmetic.

**Dispositions:** ACCEPTED-DOWNGRADE 11, ACCEPTED-MITIGATED 8, REFUTED 0, ACCEPTED-KILL 0. No objection was refuted. The reviewers' arithmetic reproduced in every quantitative case. The one partial correction: BCH parity scales the array (70% of the die), giving x1.062, not x1.088 on the whole die.

| id | severity | disposition | action |
|---|---|---|---|
| RT-DEV-margin-stack-01 | MAJOR | ACCEPTED-DOWNGRADE | Derive the tail in the model; replace 1e-10 with an ECC-budgeted aged 2e-5 quantile measured directly on ≥1e6 cells; negative-WL sweep; withdraw the 28x refresh claim |
| RT-DEV-margin-stack-02 | MAJOR | ACCEPTED-MITIGATED | 2-pillar gain FET, Vov 0.6 V, 1.2 ns samples (G 0.9); carrier measures matched-area IGZO gm |
| RT-DEV-margin-stack-03 | MAJOR | ACCEPTED-DOWNGRADE | RTN as an exponential heavy tail; GO = projected BER with measured ns-RTN; stretch withdrawn; K9 |
| RT-DEV-margin-stack-04 | MAJOR | ACCEPTED-MITIGATED | BEOL-IGZO-on-SKY130 carrier: oxide FET drives an on-chip fF node sampled at 1-3 ns (+$90k) |
| RT-DEV-margin-stack-05 | MINOR | ACCEPTED-MITIGATED | -0.1 V NWL drift reserve; 1,000 h 105 °C hold-bias stress; GO on post-stress data |
| RT-PROC-margin-stack-01 | MAJOR | ACCEPTED-DOWNGRADE | 2-4 EUV-class layers (central 13%); $/bit penalty +9-25%; process-emulate same-step and plate-strip (I-12302); gate ≤3 layers |
| RT-PROC-margin-stack-02 | MAJOR | ACCEPTED-MITIGATED | Field-solver α on published VCT geometry + ratio-matched programmable coupling on the MPW; K6 at α 0.25/0.34 |
| RT-PROC-margin-stack-03 | MAJOR | ACCEPTED-DOWNGRADE | 2e-5 quantile observed directly on ≥1e6 planar + etched-sidewall cells; VCT tail deferred to partner data |
| RT-PROC-margin-stack-04 | MINOR | ACCEPTED-DOWNGRADE | Search found no sourced module share; drop $/bit from the claim; $15k cost-split study |
| RT-CIRC-margin-stack-01 | MAJOR | ACCEPTED-MITIGATED | 1,024-cell columns, 4:1-muxed signal-first DS comparator (~0.55 of 0.885 µm²); layout gate at M7 |
| RT-CIRC-margin-stack-02 | MAJOR | ACCEPTED-DOWNGRADE | Parity in model (+6.2% die): density 0.677; RDIMM side-band variant for servers |
| RT-CIRC-margin-stack-03 | MAJOR | ACCEPTED-DOWNGRADE | Ratio-matched coupling + oxide-native DS population; D 5 → 3; measured-vs-projected GO report |
| RT-CIRC-margin-stack-04 | MAJOR | ACCEPTED-DOWNGRADE | 2 pillars + heavy-tail statistic (22.6 mV central); GO as BER tail; stretch withdrawn |
| RT-CIRC-margin-stack-05 | MAJOR | ACCEPTED-MITIGATED | Slow path 5.75% at 1e-4 (+15 ns), 0.06% at 1e-6; wide-IO on-die / x4 side band; decoder synthesis |
| RT-CIRC-margin-stack-06 | MINOR | ACCEPTED-MITIGATED | Same fix as DEV-02; read chain ~14 ns, not 3.6 ns |
| RT-IND-margin-stack-01 | MAJOR | ACCEPTED-DOWNGRADE | Re-scope the claim to capacitor-module resources + 3D enabler; ask a maker before the raise; EV 75 → 24 |
| RT-IND-margin-stack-02 | MAJOR | ACCEPTED-DOWNGRADE | SEL short-BL → small-Cs prior art found; narrow claims; FTO/patentability opinion before filing |
| RT-IND-margin-stack-03 | MAJOR | ACCEPTED-DOWNGRADE | Oxide device terms measured on the carrier; MTA outreach; file before disclosure; investor discount accepted |
| RT-IND-margin-stack-04 | MINOR | ACCEPTED-MITIGATED | Not a physics kill; named-host path (4F2, OCTRAM, 3D tier, BEOL eDRAM); portfolio reader instrument meanwhile |

### 11.1 Redesigns adopted

1. **Sense chain** (DEV-02, CIRC-01/06):
   - a 2-pillar same-step gain FET per **64-cell** segment (Cseg 2.81 fF; 5 sites per 64 cells), driven at Vov 0.6 V by a deeper pulsed read source;
   - 16 segments per **1,024-cell global line** (12 fF);
   - **one auto-zeroed comparator per 4 columns**, read by **signal-first double sampling** (signal, reset, reset sample, compare), with a 4T restore latch per column.
   - The gain-FET Vt still cancels. Segment-reset kTC and injection are budgeted. Decisions take 11.4 ns and restore 3.1 ns.
2. **RTN as a heavy tail** (DEV-03, CIRC-04). Error probability is P = Q(m/σ) + w·e^(-m/η+σ²/2η²)·Φ(m/σ-σ/η), replacing a Gaussian RSS. The GO is a projected BER, not σ_res.
3. **ECC-budgeted retention** (DEV-01, PROC-03). 1e-5 of the 1e-4 raw-BER budget goes to retention-weak cells, so the IGZO tail requirement moves from 1e-10 (6.36σ) to a 2e-5 leaky-cell fraction (4.11σ), observed directly on ≥ 1e6 cells. Averaged DUE is unchanged (2.3e-17). Static weak cells are repaired at sort; patrol scrub bounds VRT. A **negative-WL hold reserve** of -0.1 V absorbs drift (DEV-05).
4. **Oxide-native measurement** (DEV-04, CIRC-03, IND-03). A **BEOL-IGZO-on-SKY130 carrier**: IGZO gain FETs drive on-chip fF nodes sampled at 1-3 ns, plus ≥ 1e6 hybrid 2T leakage cells, with planar, etched-sidewall and dual-series-gate (I-12627) coupon splits and a 1,000 h stress.
5. **Coupling by extraction plus ratio-matched silicon** (PROC-02, CIRC-03). A 3D field solver gives α on published VCT geometry; programmable MOM coupling on the MPW reproduces the extracted ratios within 20%.
6. **Integration honesty** (PROC-01). The model carries 2/3/4 added EUV-class layers. The I-12302 plate-strip variant (clamped BL, sensed plate strip, separate BEOL gain FET) is process-emulated as an alternative.
7. **ECC delivery** (CIRC-02/05). The on-die t=8 code (+6.2% die, +0.5% decoders) suits wide-IO parts (HBM, LPDDR x16). x4 DDR5 RDIMMs carry BCH-12 in the side band and give up chipkill.
8. **Dropped:** the neutraliser and charge-transfer add-ons (K7 retired) and the 17-40x stretch.

### 11.2 Revised step-change claim

**Capacitor-module resource intensity and 3D readiness, not cost.**
- **Planning cell 0.5 fF:** 10.8x shorter than 5.42 fF (AR 62 → 5.7), with a 1.0 fF fallback (5.4x, AR 11.4). That gives ~10x less HAR capacitor etch (fluorocarbon/PFAS, He-cooled hours), ~100x less ZrO₂/TiN ALD exposure and no Ru/k>50 push. The fab-level share of these inputs is unsourced.
- **3D (conditional on a 3D host):** a 63-127 nm lateral capacitor instead of ~450 nm, 2.2-2.8x per-tier density, and break-even at ~10-13 tiers instead of ~26.
- **Penalties:**
  - $/bit +9% to +25% (central +17%) vs plain oxide 4F2;
  - density -11% (0.677 Gb/mm²);
  - array energy only 1.3x better;
  - latency parity (~14 ns);
  - refresh 2-12x only conditionally, and mostly owed to oxide access.
- **Withdrawn:** the 17-40x stretch, the 28x refresh claim, the 3.6 ns read chain, "$/bit flat" and "no EUV added".

### 11.3 Revised decisive experiment

See §5.1: $563k inside a $999k plan, GO/NO-GO at M17 (< $1M, ≤ 24 months).
- **Added measurements, as the reviewers asked:**
  - IGZO gain-FET **RTN jump distribution at a 1-3 ns gap** on ≥ 1e4 matched-area FETs, on an on-chip fF node;
  - IGZO gm at 0.3-0.8 V overdrive;
  - the **aged 2e-5 leakage quantile directly on ≥ 1e6 cells** (planar and etched-sidewall), after 1,000 h at 105 °C, with a negative-WL sweep;
  - ratio-matched coupling at the field-solver α;
  - process emulation of the added layers;
  - layout of the muxed column cell;
  - BCH decoder synthesis.
- **GO:** projected BER ≤ 9e-5 at 0.5 fF, which requires:
  - Gaussian residual ≤ 12 mV;
  - RTN 1e-4 quantile ≤ 44 mV;
  - α ≤ 0.25;
  - pairs < 1%;
  - aged 2e-5 leakage ≤ 586 aA (conditional ≤ 1,881 aA).
- **NO-GO:** BER > 1e-4 at 1.0 fF, pairs > 10%, or leakage above the 1.0 fF limit.

### 11.4 Revised verdicts

- **PHYSICALLY POSSIBLE? Yes.** No new physics. Sensing-limited Cs is 0.13/0.29/0.74 fF; 0.5 fF closes in the central case (P(err) 8e-7 vs a 9e-5 target) but not the pessimistic one, and the 1.0 fF fallback closes in all cases. Retention needs the aged 2e-5 IGZO leakage quantile <= 586 aA (model estimate ~100-260 aA); the 1e-10 tail derived from the inputs is 1.5-5.5 fA fresh.
- **STEP CHANGE IF IT WORKS? Narrowed.** Axis: capacitor-module resource intensity plus 3D readiness. The capacitor goes 5.42 -> 0.5 fF: 10.8x shorter, AR 62 -> 5.7 (5.4x at the 1.0 fF fallback), i.e. ~10x less HAR capacitor etch, ~100x less ZrO2/TiN ALD exposure, and no Ru/k>50 push. A 3D-tier lateral capacitor shrinks to 63-127 nm from ~450 nm (per-tier density 2.2-2.8x, break-even ~10-13 tiers vs ~26), conditional on a 3D host. It is NOT a step on $/bit (+9% to +25% penalty, central +17%), density (-11% vs plain 4F2), latency or array energy (1.3x). Refresh gains of 2-12x are conditional and belong mostly to oxide access.
- **PROVABLE WITH $1M? Partly.** A $563k decisive experiment ($999k plan, 17 months) measures four things: the circuit residual and muxed double sampling on a 22FDX emulator with ratio-matched coupling, error pairs (DRAM Bender), IGZO gain-FET RTN at a 1-3 ns gap on an oxide-on-CMOS carrier, and the 2e-5 leakage quantile directly on >=1e6 planar and etched-sidewall IGZO cells after a 1,000 h stress. VCT coupling alpha, the VCT sidewall tail and the added mask count stay projections (field solver, process emulation) until partner silicon.

### 11.5 FINAL STATUS: **DOWNGRADED**

The physics stands: with a 2-pillar gain FET, 64-cell segments and 4:1-muxed signal-first double sampling, the sensing-limited cell is 0.13/0.29/0.74 fF (optimistic/central/pessimistic), so the 0.5 fF planning cell closes in the central case, and the 1.0 fF fallback closes in all three. But the promise shrinks. (1) RTN heavy tails and a weaker gain FET kill the 17-40x stretch. (2) A leakage tail derived from the model's own inputs kills the 28x refresh claim; the retention requirement becomes an ECC-budgeted 2e-5 quantile. (3) 2-4 added EUV-class layers plus BCH parity turn $/bit into a +9% to +25% penalty and density into -11% vs plain 4F2. (4) The $1M experiment still cannot measure VCT coupling, the VCT sidewall leakage tail or the real mask count. (5) SEL prior art narrows novelty. The concept stays alive. It remains the portfolio's cheapest physics test and its reader chip, but it is no longer a rank-1 step change on the mission's cost or density axes.
