# MARGIN STACK: segment-gain, double-sampled, ECC-budgeted sensing that cuts the cell capacitor ~10x on oxide-access DRAM

NEW DRAM Stage 3 dossier. Author: agent `dosw-margin-stack`, 2026-11-02. Concept slug `margin-stack`.

Inputs:
- Model `models/margin-stack.py`, re-run 2026-11-02 (exit 0; output identical to `research/stage3/margin-stack_model_output.md`).
- Research notes `research/stage3/margin-stack_notes.md`. Assumptions `research/assumptions/dos-margin-stack.md`.
- Sources `research/sources/dos-margin-stack.jsonl`, plus the A1, A2, A3, B3 and other dossier logs.

Tags: [REPORTED] = logged source, usually a search snippet. [ESTIMATE] = model or hand arithmetic. [SPECULATIVE] = physics nobody has measured. [training knowledge] = prior knowledge with no logged URL.

Program months: M0 = 2027-01-01.

---

## 0. Header

| Field | Value |
|---|---|
| Name | MARGIN STACK |
| One-line thesis | Today's ~17,800-electron bit exists to beat bitline capacitance and amplifier offset, not noise. Put a 3-transistor gain stage on every 32 cells, cancel its offset with correlated double sampling (CDS), budget the array for raw BER 1e-4 behind row ECC, and the capacitor of an oxide-access 4F2 cell shrinks from 5.4 fF to ~0.5 fF: a 120 nm stub instead of a 1.3 µm, aspect-ratio-62 pillar. |
| Rank / EV | 1 of 10. EV 75 = S3 x P5 x D5 |
| Category | sensing/periphery |
| Lineage | Device-lens STUB (primary physics: same-step local gain, CDS, raw-BER ECC, the oxide retention argument) merged with system-lens Margin Stack (framing; global-line levers; shared-MPW plan) |

**Constituent ideas and their creativity-technique lineage**

| Id | Idea | Technique (facet) | Stage 2 / triage verdict | Role now |
|---|---|---|---|---|
| I-00257 | Local gain FETs from the same VCT step | SCAMPER-Substitute (lithography and capital) | ADVANCE 62.6 | The in-array gain stage |
| I-11559 | ECC-paid capacitor | Phase B lens | ADVANCE 67.1 | Raw-BER 1e-4 budget: 7σ to 3.72σ |
| I-11148 | Erasure-flagging sense amps | Scarcity and constraint as engine (sensing) | ADVANCE 67.1 | Delayed-sample flag, demoted to telemetry |
| I-05218 | CDS sense amps read 0.2 fF cells | First principles (array/3D) | HOLD 61.2 | CDS, now load-bearing |
| I-11588 | Negative-capacitance bitline neutraliser | Phase B lens | ADVANCE 65.9 | Global-line add-on |
| I-04613 | Shallow pillars rescued by soft decoding | Assumption inversion (storage element) | HOLD 60.0 | Soft information, capped at 1.2x |
| I-07812 | "Local post offices": a sense amp every 32 cells | Perspective shift / personas (industry) | HOLD 60.6 | Segment framing |
| I-11545 | Sense layers every 16 oxide tiers | Phase B lens | ADVANCE 65.6 | 3D-tier segment argument |
| I-05154 | Partial-charge "sip" read | First principles (sensing) | HOLD 59.4 | Critic: self-referencing needs local gain |
| N-04 | Charge-transfer pre-sense (B1-04) | Phase B cell-physics lens, TWIST | ALIVE | Global-line add-on |
| N-40 | Hierarchical 64-cell bitlines, bonded SAs (B3-01) | Phase B 3D/process lens, NEW | ALIVE | Why the gain must sit in the array |
| N-27 | In-tier complementary-oxide sense amps (B2-08) | Phase B materials lens, NEW | ALIVE | Oxide-built amp in the array |

**Verdicts**

- **PHYSICALLY POSSIBLE? Yes.** No new physics is needed. The thermal-noise floor for a 32-cell segment at raw BER 1e-4 is 0.024 fF (~63 electrons), 20x below the 0.5 fF planning cell. What sets the size is mismatch, coupling, wordline kick and the oxide leakage tail, which are all engineering terms. The cut is legal only with oxide access: a silicon 13 fA tail drains 0.54 fF in ~3 ms.
- **STEP CHANGE IF IT WORKS? Yes, on capacitor-module capital, PFAS and 3D readiness: a ~10.8x smaller capacitor** (5.42 to 0.5 fF; height 1,300 to 120 nm; aspect ratio 62 to 5.7). Array energy per access falls ~2.3x [ESTIMATE]. The stretch is 17-40x [SPECULATIVE]. **It is not a step on $/bit** (-3% to +4%) **or density** (-8% against plain 4F2).
- **PROVABLE WITH $1M IN 24 MONTHS? Partly, and strongly.** One 22FDX MPW, IGZO coupons and a DRAM Bender study answer the circuit question (post-CDS residual, coupling, error clustering) by M16-17. The experiments cost $520k; the plan with two founders costs $955k. They do not build an oxide VCT array. The oxide-only terms (1/f noise, leakage tail) come from coupons, and the two are combined by projection.

---

## 1. How it works

A DRAM bit is a small bucket of charge behind a switch. To read it, the switch opens and the bucket's charge spills onto a long wire, the bitline, shared by 512 cells. The bitline holds ~35 fF, about seven times the cell's 5.4 fF, so the voltage it sees is only ~50 mV. A latch at the end must tell that 50 mV from the latch's own random imbalance (offset) and from noise coupled in by neighbouring wires, and it must get it right on all ~17 billion cells of a chip. That is why today's capacitor is a 1.3 µm-tall, 21 nm-wide pillar, 62 times taller than it is wide. Etching, coating and propping up those pillars is one of the hardest and most chemical-hungry steps in the fab.

MARGIN STACK attacks the reason the bucket must be big, using three stacked tricks.

1. **Short wires, local gain.** Cut the bitline into 32-cell segments (~1.5 fF each). Each segment drives the gate of its own small transistor, the "gain FET". A small bucket on a short wire gives a large voltage. On the 35 fF line a 0.5 fF cell would give 6 mV; on the 1.5 fF segment it gives 107 mV.
2. **Correlated double sampling.** The gain FET has its own random offset, ~47 mV. So read twice through the same transistor: once just before the cell opens, once just after. Subtract the two. The offset is in both readings and cancels. CMOS image sensors read a few hundred electrons with a few electrons of noise this way [training knowledge].
3. **Let the code catch the last few.** Design for one wrong bit in 10,000 (raw BER 1e-4) and fix them with a row code (BCH, 80 check bits per 512 data bits). The array then needs 3.72 standard deviations of margin instead of 7.

```
 TODAY (1-beta DDR5)                    MARGIN STACK (oxide-access 4F2)

 [5.4 fF] x512, each a 1.3 um pillar     [0.5 fF] x32, each a 0.12 um stub
   |   |   |   ...   |                     |   |  ...  |
 ==+===+===+=========+==> latch SA       ==+===+=======+== local node ~1.5 fF
   bitline 35 fF   signal ~50 mV                       |
   must clear 7 sigma of offset+noise             [gain FET] (+ reset, write FETs)
                                                       |
                                     ==================+===== global line ~6 fF
                                                       |
                            CDS: sample 1 (before WL) - sample 2 (after WL)
                                                       |
                                comparator --> bit (+ "slow decision" flag)
                                                       |
                                 row ECC: 512 data + 80 check bits, BCH t=8
                                 margin needed 3.72 sigma, not 7
```

A read takes about 3.6 ns: share charge (60 ps), two samples (0.7 ns each), compare (0.5 ns), write back (1.6 ns) [ESTIMATE]. That fits inside a DDR5 row-activate budget (~14 ns). IBM's 2007 silicon version of the local gain stage reported 1.5 ns latency [REPORTED].

Why oxide? A bucket 10x smaller leaks empty 10x faster. Silicon access transistors leak ~13 fA in their worst cells. Oxide-semiconductor (IGZO) transistors from Kioxia/Nanya report under 1 aA, more than 10,000 times less [REPORTED]. Only with that switch can a 0.5 fF bucket hold its bit for seconds.

---

## 2. The physics and the numbers

All numbers are from `models/margin-stack.py` unless tagged otherwise.

### 2.1 Baseline anchors (1-beta, A1 conventions)

- Pillar capacitance: ε0 x 3.9 / EOT 0.55 nm = 62.8 fF/µm² (0.0628 aF/nm²). Per nm of height: π x 21.1 nm x 0.0628 aF/nm² = **4.16 aF/nm**. 5.42 fF needs 1,302 nm (AR 62); 0.5 fF needs **120 nm (AR 5.7)**.
- Bitline: 512 x 0.06 fF + 4 fF = 34.7 fF. Signal = (1.05/2 - 0.155) V x 5.42/(5.42 + 34.7) = 0.370 x 0.135 = **50.0 mV**, reproducing A1. The 50 mV budget = 7σ x 7.14 mV.
- Stored charge: 5.42 fF x 0.525 V / q = **17,762 e-**; at 0.5 fF x 0.5 V, **1,561 e-**.
- ECC: Q⁻¹(1e-4) = 3.719σ, against 7σ: a 1.88x margin gain.
- Thermal floor: kT/C on a 1.48 fF node at 85 °C is 1.83 mV rms. Even with no kTC cancellation, Cs ≥ 0.024 fF. Every case below sits 5-100x above it.

### 2.2 The signal equation and what each lever buys

On a segment, signal S = 0.425 V x Cs/(Cs + Cseg). The usable half swing is 0.5 V x (1 - 0.15 droop). The array works when S(1 - 2α) - D ≥ 3.72 x √(σ² + (0.05 S)²). Here α is data-dependent neighbour coupling per side, D the deterministic kick residual, σ the random residual, and 5% the stub spread.

| Case | Cs needed (fF) | Cut vs 5.42 | Stub height / AR |
|---|---|---|---|
| A. 1-beta, 512-cell bitline, no ECC | 5.42 | 1.0x | 1,302 nm / 62 |
| B. Oxide 4F2, same latch SA | 4.63 | 1.2x | 1,112 / 53 |
| C. + raw-BER 1e-4 ECC | 2.31 | 2.3x | 556 / 26 |
| D. + neutraliser, Cn/Cbl 0.5 | 1.26 | 4.3x | 303 / 14 |
| E. Charge-transfer pre-sense, 3 mV residual, + ECC | 0.91 | 5.9x | 219 / 10 |
| F. Concept base case as written (1.0 fF segment, 40 mV, no coupling or kick) | 0.54 | 10.1x | 129 / 6.1 |
| G. Local gain + ECC, no CDS, 1-pillar gain FET (σVt 47 mV) | 1.77 | 3.1x | 425 / 20 |
| H. Same, 4-pillar gain FET (σVt 24 mV) | 0.60 | 9.0x | 145 / 6.9 |
| **I. Local gain + CDS + ECC: optimistic / central / pessimistic** | **0.09 / 0.14 / 0.32** | 59x / 40x / 17x | 22 / 33 / 77 nm |

**Critics' corrections carried here.** The concept's 0.54 fF base case (row F) assumed a 1.0 fF segment, a 40 mV gain-FET spread and no coupling or kick. With a realistic 1.48 fF segment (32 x 0.04 fF + 0.2 fF), a Pelgrom σVt of 47 mV (AVT 2.5 mV·µm on a 15 nm x 60 nm pillar, an ESTIMATE because no IGZO AVT was found), 10% coupling and the wordline kick, local gain plus ECC **without CDS needs 1.77 fF: a 3.1x cut, not 10x**. CDS is therefore load-bearing, not the stretch. Other corrected numbers:
- The neutraliser gives 1.26 fF, not 0.96.
- Charge-transfer pre-sense reaches 0.5 fF only if its bitline-referred residual is ≤1.6 mV, because every mV on a 35 fF line costs 35 aC of charge.
- Stage 2 critics capped the neutraliser at ~2x (I-11588) and soft decoding at 1.2x (I-04613).

### 2.3 The post-CDS residual (central case, 85 °C, evaluated at Cs = 0.25 fF)

| Term | mV rms | Status |
|---|---|---|
| Gain-FET Vt mismatch, 47 mV | 0 | Cancelled by CDS (same FET in both samples) |
| Comparator 3 mV offset / (gain 3 x 0.53 gm at a -4σ FET) | 1.89 | Gain spread is not cancelled |
| Sampling kTC on 2 x 10 fF / gain | 0.33 | |
| Oxide 1/f + RTN between samples | 4.0 | **[SPECULATIVE]**; a single trap is ~6 mV at this size |
| Wordline kick, random part | 2.4 | |
| **RSS σ_res** | **5.0** | √(4.0² + 1.89² + 0.33² + 2.4²) |

Two terms are new in this dossier.

**(1) Wordline kick-back.** The access FET's gate holds 49 aF. Half its channel charge (0.5 x 49 aF x 2 V) plus overlap charge (10 aF x 3 V) is 79 aC. On a 1.73 fF node that is a **46 mV mean kick**, against 2.3 mV on a 35 fF bitline. Stage 2 assumed ~2 mV; that holds only on a long line. A stored '0' turns the FET on harder, which adds a 7.1 mV data asymmetry. After 90% dummy-edge cancellation, D = 8.1 mV deterministic plus 2.4 mV random remain.

**(2) The bias conflict.** A gain FET made in the access-FET step inherits the high Vt that gives <1 aA leakage. At a 0.5 V precharge it is off. It needs a pulsed negative read-source line or a back gate to reach ~0.4 V overdrive.

Hand check of row I central at Cs = 0.14 fF: S = 425 x 0.14/1.62 = 36.7 mV. Less 20% coupling, that is 29.4 mV. Less D (8.6 mV at this node size), 20.7 mV remain. The requirement is 3.72 x √(5.0² + 1.8²) = 20.0 mV. ✓

### 2.4 ECC, erasure flags and clustering

- BCH t=8 over 592 bits at raw BER 1e-4: P(>8 errors) = **2.3e-17 per read**, about one uncorrectable read per ~0.9 server-years at 100 GB/s.
- **Erasure flags buy ~4%, not "half the parity."** The best Gaussian flag window catches 83% of errors but also flags 3.9x as many correct bits. Allowed raw BER rises only from 1.0e-4 to 1.4e-4 (80% flaggable) or 1.7e-4 (100%), and the code gets no shorter. RAW-BER CONTRACT adds a second reason: retention errors on long-resident data are latched to confident rails by refresh. The concept's "≥80% flagged" go criterion is therefore secondary.
- **Same-codeword pairs are the real threat.** At 1% pairs the allowed raw BER falls to 6.3e-5. At 10% it falls to 1.7e-5, a 0.90x margin. Codewords run along a row, so a bad segment amp touches 32 different codewords once each. Pairs come from row-level causes: weak wordlines, hammer, adjacent variable-retention (VRT) cells.

### 2.5 Retention sets the planning point, not sensing

Retention is t = Cs x droop / (I_leak + I_diel). The dielectric at 1e-8 A/cm² adds ~0.8 aA at 0.5 fF and caps any size at ~47 s.

| Cs | 10 aA tail | 100 aA tail | 1,000 aA tail | Max tail for 64 ms | Max tail for 1 s |
|---|---|---|---|---|---|
| 0.25 fF | 1.8 s | 187 ms | 19 ms | 293 aA | 19 aA |
| **0.5 fF** | 3.5 s | 372 ms | 37 ms | **586 aA** | 38 aA |
| 1.0 fF | 6.5 s | 738 ms | 75 ms | 1,172 aA | 75 aA |

(At a 75 mV droop: 0.5 fF x 75 mV = 37.5 aC; 37.5 aC / 64 ms = 586 aA.)

**Correction carried:** the concept's "0.8-81 s at 1-100 aA, ~6 ms at 13 fA" used a 150 mV droop against its own 75 mV signal convention. At 75 mV, 0.54 fF on a 13 fA silicon tail lasts **3.1 ms**. Once CDS works, a 0.5 fF cell can tolerate a 370 mV droop at the central residual, which gives 1.8 s at a 100 aA tail. OCTRAM's "<1 aA" is likely a median; nobody has published the 1-in-1e10 tail. **The planning cell is 0.5 fF, set by that tail.**

### 2.6 Energy, area, cost, 3D

- **Energy per sensed bit:** 1-beta Cbl x VARY²/2/η = 20.1 fJ. MARGIN STACK: local node 0.99 + global restore 3.00 + two CDS samples 2.40 + comparator 2.0 = **8.8 fJ** [ESTIMATE; global line 6 fF assumed].
- **Refresh power, 16Gb die:** 12.2 mW (1-beta, 64 ms) vs **0.43 mW** (0.5 fF, 100 aA tail, droop-optimised, 2x guard, 917 ms interval) or 0.046 mW at a 10 aA tail. Most of that gain comes from oxide access itself.
- **Area:** a 3T amp plus a strap site is 4 extra 4F2 sites per 32 cells, so **+12.5% array and +8.8% die**. Density is 0.701 Gb/mm², which is 1.57x 1-beta but -8% against plain 4F2 VCT (0.762). The concept's "~9%, density about flat" is corrected.
- **Cost:** capacitor module 10/15/20% of wafer cost [unsourced], with 65% of it scaling with height. Saving 5.9/8.8/11.8%, plus 1.2% for one strap mask, plus 8.7% area: **$/bit +3.6% / +0.4% / -2.8%**, or $1.44-1.53/GB against $1.48.
- **3D:** a lateral capacitor in a tier falls from 450 nm to **63 nm** at 0.5 fF. Per-tier density rises 2.8x, and 3D breaks even with 1-beta at **~10 tiers instead of ~26**.

### 2.7 Against 1-beta DDR5

| Metric | 1-beta DDR5 (6F2) | MARGIN STACK on oxide 4F2 |
|---|---|---|
| Cell capacitor | 5.42 fF | 0.5 fF planning (0.14 sensing-limited) |
| Capacitor height / AR | 1,302 nm / 62 | 120 nm / 5.7 |
| Stored electrons | 17,762 | 1,561 |
| Sense margin required | 7σ, no ECC | 3.72σ behind BCH t=8 |
| Density | 0.447 Gb/mm² | 0.701 Gb/mm² (plain 4F2: 0.762) |
| Array energy per sensed bit | 20.1 fJ | 8.8 fJ [ESTIMATE] |
| Refresh power, 16Gb | 12.2 mW | 0.43 mW at a 100 aA tail |
| Sense + restore | — | ~3.6 ns |
| $/GB | $1.48 | $1.44-1.53 |
| Added masks | — | +1 DUV critical (strap); no EUV |

### 2.8 Sensitivity

Required Cs (fF) against the random residual σ_res and coupling α (32-cell segment, kick included):

| σ_res (mV) | α 0.05 | α 0.10 | α 0.20 |
|---|---|---|---|
| 4 | 0.10 | 0.12 | 0.16 |
| 8 | 0.17 | 0.19 | 0.28 |
| 13 | 0.26 | 0.30 | 0.44 |
| 20 | 0.41 | 0.49 | 0.74 |
| 30 | 0.68 | 0.82 | 1.37 |
| 40 | 1.04 | 1.29 | 2.51 |

- **Thresholds.** Cs ≤ 0.5 fF needs σ_res ≤ 23.5 / 20.5 / 14.5 mV at α 0.05 / 0.10 / 0.20. Cs ≤ 0.25 fF needs ≤ 12.3 / 10.6 / 7.1 mV. Above 34 mV (α 0.10), Cs stays ≥ 1 fF.
- **Segment length.** 64 cells cost 6.2% of the array (4.4% die) and need 0.20 fF. 16 cells cost 25% (17.5% die) for 0.11 fF. 32-64 cells is the sweet spot.
- **Kick** limits the stretch, not the planning point. At 0.5 fF with *no* cancellation, D ≈ 43 mV and the central case still closes: 86 - 43 = 43 mV against 27 mV needed [ESTIMATE, hand calculation].
- **Without ECC** (k = 7), the central CDS case needs ~0.26 fF and the pessimistic case ~0.8 fF [ESTIMATE, hand calculation outside the model]. If CDS works, ECC is margin insurance, not the lever that carries the cut.
- **Cost share** decides the sign of $/bit (above).

### 2.9 GO / NO-GO (pre-set, from the model)

**GO** requires all three:
1. Post-CDS input-referred residual ≤ **20 mV** at 85 °C under worst-case neighbour data on 32-cell segments, coupling folded in. That is raw BER ≤ 1e-4 at Cs = 0.5 fF for iid errors (≤ 1.4e-4 if ≥ 80% are flaggable). ≤ 11 mV unlocks 0.25 fF.
2. **< 1%** of errors are same-codeword pairs.
3. The IGZO 1-in-1e10 leakage tail at 85 °C is ≤ **586 aA** at 0.5 fF (≤ 59 aA for a 10x refresh cut).

**NO-GO** if the residual is > **34 mV** (Cs ≥ 1 fF: a ~5x cut, which a 4-pillar gain FET without CDS already gives), or if pairs exceed **~10%** of errors.

---

## 3. What is new versus prior art

| Prior art | Date | What it shows | Gap left |
|---|---|---|---|
| IBM, Barth et al., SOI eDRAM with a 3T micro sense amp on ~32-cell local bitlines | ISSCC 2007 / JSSC 2008 | Local gain per short segment, 1.5 ns latency | Silicon eDRAM; no CDS; capacitor not co-designed |
| Semiconductor Energy Laboratory DOSRAM patents (US 12,230,314; 11,694,594; 11,488,528) | 2010s-2020s | Oxide 1T1C cells stacked over silicon sense amps | No Cs or CDS found in snippets; main freedom-to-operate risk |
| Hi-ECC, Wilkerson et al. | ISCA 2010 | Strong BCH cuts eDRAM refresh ~93% at ~2% storage | ECC used for refresh, never to shrink the capacitor |
| Offset-cancellation SAs (e.g. US 11,763,878) | Shipping | Margin = ΔV_BL - (V_OS + coupling) | Global bitline only |
| Charge-transfer SAs (US 8,320,208 family) | 2010s | Pre-sense gain for small Cs | Needs ≤1.6 mV residual for 0.5 fF |
| NC sense amp US 8,872,938; SRAM NC bitlines (TVLSI); Blalock clamped-bitline SA | Various | Active bitline-load cancellation | No DRAM neutraliser found |
| Kioxia + Nanya OCTRAM, 275 Mb, 4F2 vertical IGZO | Dec 2024 | Ion > 15 µA, Ioff < 1 aA | Keeps the HAR capacitor |
| Kioxia 3D OCTRAM, 8 horizontal IGZO layers | Dec 2025 | Ion > 30 µA, Ioff < 1 aA | No retention published |
| Samsung 16Gb 4F2 VCT (ISSCC 2026); 10a IGZO VCT working die, W2W-bonded periphery | Feb / Apr 2026 | Oxide 4F2 is real | No capacitor cut published |
| Samsung 16-tier VS-DRAM, horizontal capacitor, shared back gate, bitline shield | 2024-2026 | Cs rises ~linearly with capacitor length | Long capacitor in each tier |
| SK hynix vertical-gate 4F2 with bitline shielding | VLSI 2026 | Shielding attacks α | No local gain |
| ETH SAFARI: SoftMC (2018), DRAM Bender (2022), reduced-VPP study (2022), PaCRAM (2025) | 2018-2025 | Real-chip error characterisation and partial charge restore on 388 DDR4 chips | The method for our Bender study |
| NAND soft-bit sensing (US 11,907,545); XED flag export (ISCA 2016) [training knowledge for XED] | 2016-2024 | Second sense as a soft bit | Not in DRAM silicon |
| CMOS image sensors: source follower + CDS | Decades [training knowledge] | Few-e- noise on few-hundred-e- packets | Not memory |

**The genuine delta.** Every part is known. Nothing published (in any snippet seen) combines them into one co-designed margin budget on an oxide access device, built to shrink the capacitor. The claimable pieces are:
1. A same-step oxide gain FET per segment, read by CDS through that same FET, with the capacitor sized below the segment capacitance (Cs ≤ 0.5 Cseg, height ≤ ~10x diameter).
2. Wordline kick compensation for short segments: a dummy edge between samples plus per-mat trim of the data asymmetry.
3. Biasing a high-Vt same-step gain FET with a pulsed read-source line or back gate.
4. Pair-aware row-codeword orientation and flag-driven scrub.
5. A ≤100 nm lateral stub sized to a 16-tier local-gain segment.

No oxide VCT program has published a capacitor cut. If SEL's DOSRAM already runs ~1 fF cells on short stacked bitlines, the novelty narrows to items 1-3.

---

## 4. Show-stoppers and how persistence could get around them

| # | Show-stopper | Number | Workaround path |
|---|---|---|---|
| 1 | Data-dependent coupling, which CDS cannot cancel (the chief's top risk) | α 0.10 holds 0.5 fF only if σ_res ≤ 20.5 mV; at α 0.20, ≤ 14.5 mV | Bitline shields (SK hynix VLSI 2026, Samsung VS-DRAM); activate alternate segments; differential reference segment; coupling-aware threshold trim; 64-cell segments |
| 2 | Oxide 1/f + RTN between the two samples [SPECULATIVE] | 4 mV central; 10 mV pessimistic gives 0.32 fF; > ~20 mV loses 0.5 fF | Shorten the sample gap; 4-pillar gain FET (4x area, ~2x less RTN); hydrogen-lean anneal (imec, 30x less H-doping under PBTI); average multiple samples |
| 3 | Wordline kick on a 1.7 fF node | 46 mV mean, 7.1 mV asymmetry; D 8.1 mV after 90% cancellation | Dummy wordline edge; reference sample after a dummy edge; lower WL overdrive; 64-cell segments. Only threatens ≤ 0.25 fF |
| 4 | Gain-FET bias conflict and gain spread | Off at 0.5 V precharge; a -4σ FET keeps 53% of gm | Pulsed negative read-source line; back gate (VS-DRAM already uses one); a Vt-adjust step at one mask |
| 5 | IGZO leakage tail unknown at 1-in-1e10 | Needs ≤ 586 aA at 0.5 fF; a 13 fA tail gives 3 ms | Retreat to 1 fF (≤ 1,172 aA, still 5.4x); droop optimisation (370 mV usable gives 1.8 s at 100 aA); negative wordline hold; screen and repair tail cells |
| 6 | Clustered errors (pairs) defeat t=8 | 1% pairs gives 6.3e-5 allowed; 10% gives 1.7e-5 | Interleave codewords across mats; RFM/PRAC hammer control; BCH-12 in the DDR5 RDIMM side band (RAW-BER CONTRACT: iid to 3.3e-4); weak-row repair |
| 7 | Area and one critical mask | +12.5% array, +8.8% die; strap mask 1.2% of wafer cost | 64-cell segments (4.4% die) at 0.20 fF; self-aligned strap |
| 8 | Soft errors on a ~1,500-e- cell | Unmeasured; an oxide node with no Si junction should collect less charge [SPECULATIVE] | Row ECC absorbs singles; neutron/alpha test after the raise |
| 9 | Row hammer in IGZO VCT | Unknown (A1) | Measure on the partner array; RFM/PRAC |
| 10 | Emulation gap: 22FDX silicon is not oxide | Si access leaks too much to hold charge; Si 1/f differs | Read right after write on the MPW; measure oxide 1/f and RTN on coupons and add them in the projection; real VCT array after the raise |

---

## 5. The decisive experiment

**Question.** On silicon that emulates an oxide 4F2 segment, is the post-CDS residual ≤ ~20 mV under worst-case data at 85 °C? Are errors iid singles (< 1% same-codeword pairs)? Is the IGZO leakage tail ≤ 586 aA?

**Step by step**
1. **M0-4, simulation.** SPICE Monte Carlo on the 22FDX PDK, with a VCT/IGZO compact model fitted to OCTRAM Ion/Ioff. TCAD through a partner for the channel-charge split (kick) and α on VCT geometry, with and without shields. *Exit:* simulated σ_res ≤ 10 mV and α ≤ 0.1 with shields.
2. **M0-6, DRAM Bender study** (shared with RAW-BER CONTRACT). Emulate reduced charge on DDR4/DDR5 parts from three vendors with truncated restore (the PaCRAM method), reduced VPP and stretched refresh. Map raw BER from 1e-5 to 1e-3 at 45-95 °C. Log errors per 512-bit row codeword (pair fraction) and a reduced-tRCD flag proxy. *Exit:* pairs < 1%.
3. **M2-7, MPW design** (GF 22FDX, ~6 mm²):
   - (A) 64k segments x 32 cells (2.1M cells). Four Cs quadrants of custom MOM stubs (0.125 / 0.25 / 0.5 / 1.0 fF). Dummy loads give Cseg 0.8 or 1.5 fF. Minimum-size gain FET (σVt 40-50 mV) plus a 4-finger variant. Pulsed read-source line. Switchable kick compensation.
   - (B) Global CDS: sampling pair, auto-zeroed comparator, delayed second compare as the flag, trim DAC.
   - (C) Aggressor patterns (all-0, all-1, checkerboard, stripes); shields and interleaved activation on/off.
   - (D) 64 emulated 35 fF global lines with charge-transfer pre-sense and a neutraliser (Cn/Cbl 0.3-0.8) with a stability monitor.
   - (E) BIST: per-cell margin sweep by a calibrated charge-injection DAC; row/column error counters; SPI to an FPGA.
   - (F) Matched-FET (AVT) arrays and MOM spread monitors.
4. **M7-11.** Tape-out M7 (August 2027), ~12-week fab, packaging, boards.
5. **M3-12, IGZO coupons** on the shared oxide run. Planar IGZO FETs at minimum size, ALD ZrO₂/HfO₂ MIM at ~0.5 fF, and 2T read structures (≥ 1,000 cells) that measure aA leakage by droop over 10³-10⁵ s at 25-110 °C. A lognormal fit extrapolates the 1e-10 tail. Measure IGZO 1/f/RTN spectra, and run a discrete CDS on IGZO gain FETs.
6. **M11-16, test.** Per-cell margin maps on 20 chips (42M cells, direct tail to 5.5σ). Run raw BER vs Cs at 25/85/110 °C, crossed with data patterns and with CDS, kick compensation and shields each on and off. Extract σ_res, D and α; record codeword multiplicity, flag statistics and a neutraliser stability map. At raw BER 1e-4 each full read gives ~210 errors per chip, so 1,000 reads give ~210k errors.
7. **M16-17, GO/NO-GO.** Add the coupons' oxide 1/f term to the silicon σ_res to project the oxide VCT σ_res, and test it against §2.9.

**Facilities.** GF 22FDX via MOSIS 2.0 (USC ISI, GF partner since 2026-07) or CMC. Coupons at Purdue Birck, Stanford SNF or Georgia Tech IEN. Our own test bench. A ChipFoundry SKY130 shuttle ($15k per 100 chips) can de-risk the BIST and CDS logic early.

**Budget (decisive experiment, through GO/NO-GO)**

| Item | $ | When |
|---|---|---|
| DRAM Bender study: 2 FPGA boards, DDR4/5 parts, thermal rigs, 0.5 FTE x 6 months | 80,000 | M0-6 |
| SPICE Monte Carlo + partner TCAD | 30,000 | M0-4 |
| 22FDX MPW, ~6 mm² x $17,997/mm² (CMC 2026 list) + 20% U.S.-route premium | 130,000 | M7 |
| EDA/PDK access | 25,000 | M2-7 |
| Layout/verification contractor | 45,000 | M3-7 |
| Packages, PCBs, sockets, probe cards | 30,000 | M9-11 |
| Test bench: SMUs, used thermal forcer, FPGA, low-noise sampler | 60,000 | M6-11 |
| IGZO FET + MIM coupons: ~400 cleanroom h, staff assist, materials, 2T readout | 120,000 | M3-12 |
| **Total** | **520,000** | |

In the portfolio plan the Bender study and coupon run are shared, so MARGIN STACK's incremental cost is ~$260-320k (MPW chain plus bench).

**Pre-set pass/fail.** These are the §2.9 numbers, fixed now: GO at σ_res ≤ 20 mV, pairs < 1%, tail ≤ 586 aA. NO-GO at σ_res > 34 mV or pairs > 10%. Two lever tests are scored too: the neutraliser passes if stable at Cn/Cbl ≥ 0.5, and charge-transfer pre-sense passes if its residual is ≤ 1.6 mV.

---

## 6. The $1M, 24-month plan

**Quarterly milestones and gates**

| Quarter | Work | Gate (pass to continue) |
|---|---|---|
| Q1 2027 (M0-3) | Hire the device/circuit co-founder; Bender rigs up; SPICE/TCAD; provisional #1 (M2) | G1: simulated σ_res ≤ 10 mV and α ≤ 0.1 with shields, otherwise switch to 64-cell segments before layout |
| Q2 (M3-6) | Bender error maps; coupon run starts; MPW layout | G2: pairs < 1% (proceed); 1-10% (add interleave and BCH-12 to the plan); > 10% (kill review K1) |
| Q3 (M6-9) | Tape-out M7; bench built; coupons fabricated | G3: ≥ 1,000-cell 2T leakage arrays working |
| Q4 (M9-12) | Silicon back ~M10; first light; leakage data; provisional #2 (M10) | G4: extrapolated tail ≤ 586 aA at 85 °C (K3) |
| Q1 2028 (M12-15) | Margin maps on 20 chips; CDS / kick / shield splits; PCT (M14) | G5: CDS cuts the gain-FET offset ≥ 4x |
| Q2 (M15-18) | **GO/NO-GO at M16-17**; spin-2 design | G6: §2.9 |
| Q3 (M18-21) | Spin 2 tape-out (16- and 64-cell, better kick compensation); partner technical reviews | Spin-2 silicon booked |
| Q4 (M21-24) | Spin-2 results; VLSI/ISSCC submission; data room; raise | Partner array LOI or JDA |

**Budget allocation**

| Line | $ |
|---|---|
| Decisive experiment (§5) | 520,000 |
| Second MPW spin (only after GO) | 110,000 |
| IP: 2 provisionals, 1 PCT, FTO search | 45,000 |
| Two founders at $5k/month x 24 | 240,000 |
| Overhead: insurance, travel, accounting, legal | 40,000 |
| Reserve | 45,000 |
| **Total** | **1,000,000** |

Honest risk: $60k a year will not hire an experienced DRAM designer. The fixes are equity, portfolio-shared costs (which free ~$250k), and non-dilutive programs (NSF SBIR/STTR, DARPA, NSTC) [training knowledge].

**Team.**
- *Founder 1 (architect / test / ECC).* Runs Bender, BIST and the code. Recruit from ETH SAFARI alumni or U.S. memory-systems groups.
- *Founder 2 (recruited circuit expert).* A DRAM sense-amp designer (ex-Micron Boise) or a **CMOS image-sensor readout designer**, whose CDS, column-ADC and source-follower Monte Carlo skills map one-to-one onto the key unknown. Pools: U.S. image-sensor design teams [training knowledge].
- *Contractors.* Analog layout and verification; TCAD through a university partner.
- *Advisors and partners* [names are training knowledge, institutions logged]:
  - IBM eDRAM micro-sense-amp authors (Barth et al.).
  - ETH SAFARI (O. Mutlu), for the Bender method.
  - Georgia Tech (S. Yu, S. Datta) and Purdue (P. Ye; K. Roy), for oxide FETs and coupons.
  - Stanford (H.-S. P. Wong), for oxide 3D memory.
  - BGU/Bar-Ilan gain-cell eDRAM (A. Teman) and EPFL (A. Burg), for retention statistics.
  - UT Austin IGZO eDRAM authors.
  - UCLA (L. Dolecek), for codes under clustering.

**IP strategy.**
- *File first (M2).* The segmented oxide 1T1C read method: same-step gain FET, CDS through it, Cs ≤ 0.5 Cseg, stub height ≤ 10x diameter. Then kick compensation and high-Vt gain-FET biasing.
- *M10.* Pair-aware ECC orientation with flag scrub, and the 3D lateral stub (coordinated with PIXEL-STACK). The neutraliser only if the MPW shows it stable at ≥ 0.5.
- *M14.* PCT.
- *Freedom-to-operate risks:*
  - The SEL oxide-memory estate (DOSRAM): broad OS-transistor claims; search before filing.
  - Samsung/SK hynix offset-cancellation families.
  - Charge-transfer (US 8,320,208) and NC sense-amp (US 8,872,938) patents.
  - NAND soft-bit patents (US 11,907,545) for the flag.
  - IBM's micro-SA family (~2006-08 filings) is likely expiring [training knowledge; verify].
  - We do not claim the OCTRAM or VCT cell.

---

## 7. After the demo

**Who licenses or partners.**
- **Samsung.** It has the 4F2 VCT working die, 16-tier VS-DRAM, and already uses a back gate and bitline shield, both of which MARGIN STACK needs.
- **SK hynix.** Its vertical-gate 4F2 with shielding attacks α directly, and it has a 5-layer 3D DRAM at 56.1% yield (2024).
- **Kioxia/Nanya.** OCTRAM and 3D OCTRAM are the closest platform. Nanya is a DRAM maker that needs differentiation, which may make it the natural first licensee [SPECULATIVE].
- **Micron** is reportedly skipping 4F2 (weak source). It is a 3D-tier licensee with U.S. fabs.
- **Foundries.** GlobalFoundries, TSMC and Intel could license the block for BEOL oxide eDRAM on logic, alongside HOT-SIDE MEMORY.
- **Display makers.** SEL, Sharp and LG Display bring oxide-TFT process know-how and FTO cross-licences, not DRAM fabs.
- CXMT is excluded by U.S. policy.

**What $10-50M buys.**
- **$10-15M.** A real oxide VCT test array: through a joint development deal, or 300 mm prototyping at Albany NanoTech (NSTC). It would have true same-step gain FETs and 0.25/0.5/1 fF stubs. Full reliability: hammer, VRT, neutron soft errors, 1,000 h at 85-125 °C.
- **$25-50M.** A 1 Gb-class test vehicle with a licensee, a 3D-tier version with PIXEL-STACK, and a margin-IP compiler, with ~25-40 staff.

**Standards.** Work with RAW-BER CONTRACT on a JEDEC "ECC-native" raw-BER grade and on exporting flags through on-die ECC. The sense chain becomes the reference periphery in the CELL-WAFER FOUNDRY bond spec.

---

## 8. Resources and America

**Scarce inputs removed.**
- The AR-60 fluorocarbon capacitor etch (PFAS; ECHA's restriction consultation moved in 2026).
- Helium-cooled etch-chamber hours (Qatar's 2026 helium shutdown).
- The SiN support lattice.
- ~100x of ZrO₂/TiN ALD exposure (∝ AR²) [ESTIMATE]. That eases zirconium/hafnium demand: overseas hafnium went from ~$5,000 to ~$13,115/kg by April 2026 [REPORTED].
- The push to k > 50 dielectrics with Ru electrodes, which fleet-wide would need 26-176% of world ruthenium (A2).

**Scarce inputs added.** Indium and gallium in IGZO, in nanometre films, so tonnage is tiny. Gallium faces Chinese export controls [training knowledge]. Ga-free channels (LEAN ARRAY N-26) are the hedge.

**EUV.** MARGIN STACK adds none. It adds one DUV critical mask (the strap). The host 4F2 process's EUV count is unchanged.

**Energy and water.** Not modelled. Directionally, a 10x shorter capacitor cuts HAR-etch and ALD tool-hours. For scale, Micron's Clay complex is projected at 16 billion kWh/yr and up to 48 million gallons of water per day [REPORTED].

**U.S. manufacturability.**
- The demo needs no U.S. silicon to be valid, but the plan prefers U.S. routes. 22FDX is, to my knowledge, made in GF Dresden [training knowledge; verify], so "GF Malta 22FDX" in the concept text needs checking.
- Fully U.S. options: SKY130 (Minnesota; SkyWater has been an IonQ subsidiary since 2026-07) and GF 12LP at Malta [training knowledge].
- Coupons: Purdue, Georgia Tech, Stanford, and DOE nanoscience centers [training knowledge].
- Licensee volume: Micron's Boise fabs (second Idaho fab output late 2028 [REPORTED]) and Clay, NY.

---

## 9. Kill criteria

Physics-only, as MISSION.md requires. Each has a date and a revival condition.

1. **K1, 2027-07-01 (M6). Pairs.** In all three vendors' parts at emulated raw BER 1e-4, ≥ 10% of errors are same-codeword pairs after pair-aware remapping. This kills the ECC lever: allowed BER 1.7e-5. The concept continues if CDS later meets the no-ECC numbers (~0.26 fF central). *Revival:* oxide coupons or the partner array show < 1% pairs.
2. **K2, 2028-01-31 (M12). Leakage tail.** The extrapolated IGZO 1-in-1e10 tail at 85 °C is > 1,172 aA on two process splits, so even 1 fF misses 64 ms. This kills any cut beyond ~4.6x (Cs > 1.17 fF). *Revival:* an anneal or channel (imec H+O, In-lean oxide) that brings the tail ≤ 586 aA.
3. **K3, 2028-01-31 (M12). Hard tail.** The tail is > 6,352 aA, which fails 64 ms even at 5.42 fF. That kills the oxide-access premise for this concept. *Revival:* a different access device below 586 aA.
4. **K4, 2028-06-30 (M18). Residual.** The projected oxide VCT σ_res is > 34 mV at 85 °C with measured α, so Cs ≥ 1 fF. This kills MARGIN STACK as a capacitor lever beyond ~5x, which a 4-pillar no-CDS design already gives. *Revival:* shielded geometry with α ≤ 0.05 and 64-cell segments.
5. **K5, 2028-06-30 (M18). CDS.** CDS removes < 75% of the measured gain-FET offset. That kills CDS. The fallback is row H: 0.60 fF with 4-pillar gain FETs at +9% array area. *Revival:* a sample-to-sample drift source identified and fixed in spin 2.
6. **K6, 2028-06-30 (M18). Coupling.** The measured α under worst-case data with shields on is > 0.20, so 0.5 fF needs σ_res ≤ 14.5 mV. If σ_res also exceeds 14.5 mV, the planning cell moves to 1 fF. *Revival:* interleaved activation or a differential reference cuts α below 0.10.
7. **K7, 2028-06-30 (M18). Add-on levers.** The neutraliser is unstable below Cn/Cbl 0.5, or the charge-transfer residual is > 3 mV. Those levers are dropped; the concept stands.
8. **K8, 2028-12-31 (M24). Reproduction.** Spin 2 does not reproduce spin 1's σ_res within 30%. The result is then not trusted for a raise until a third data set exists.

---

## 10. Sources

Every URL below is logged in `research/sources/*.jsonl`, mostly in `dos-margin-stack.jsonl`; the A1, A2, A3, B3, `dos-raw-ber-contract`, `dos-pixel-stack`, `dos-lean-array-module`, `dos-charge-river` and `dos-hot-side-memory` logs cover the rest.

**Circuit and ECC prior art**
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
- https://personalpages.hs-kempten.de/~vollratj/Publications/2002_DELTA_SignalMargin.html

**Oxide memory and SEL**
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12230314
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11694594
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11488528
- https://www.businesswire.com/news/home/20241209099702/en/Kioxia-Develops-OCTRAM-Oxide-Semiconductor-Channel-Transistor-DRAM-Technology
- https://blocksandfiles.com/2024/10/22/kioxia-developing-new-dram-scm-and-nand-tech/
- https://www.kioxia.com/en-jp/about/news/2025/20251212-1.html
- https://imec-publications.be/handle/20.500.12860/59908
- https://imec-publications.be/entities/publication/948b2190-065d-48d2-a9b9-4f4ecd22c234
- https://www.ithome.com/0/966/543.htm
- https://hg.gatech.edu/node/675050
- https://sites.utexas.edu/CRL/files/2021/05/IGZO_eDRAM_CIM_ISCAS_2021.pdf
- https://cris.bgu.ac.il/en/publications/a-16-kb-65-nm-gc-edram-macro-with-internal-bias-voltage-generatio/

**4F2 and 3D DRAM industry**
- https://semiwiki.com/forum/threads/isscc-2026-samsung-electronics-demonstrated-a-16gb-dram.24808/latest
- https://www.trendforce.com/news/2026/04/24/news-samsung-reportedly-produces-sub-10nm-10a-dram-working-die-using-4f-square-and-vct-targets-2028-production/
- https://www.sammyfans.com/2026/10/22/samsung-sk-hynix-micron-cxmt-4f2-dram-technology/amp/
- https://www.vlsisymposium.org/wp-content/uploads/2026/04/2026-VLSI-Technical-Tipsheet-REVISED-FINAL-NO-IMAGES-4.24.26.docx
- https://hao.cnyes.com/post/269690
- https://cloudnews.tech/samsung-and-sk-hynix-seek-another-solution-to-the-physical-limit-of-dram/
- https://www.guru3d.com/story/sk-hynix-achieves-yield-in-fivelayer-3d-dram-development
- https://www.techinsights.com/ja/node/37840
- https://patents.google.com/patent/US12193208

**Error characterisation**
- https://arxiv.org/pdf/1805.03195
- https://arxiv.org/pdf/2206.09999
- https://www.arxiv.org/pdf/2502.11745
- https://arxiv.org/pdf/2211.05838
- https://people.cs.rutgers.edu/~mp2099/files/patel_isca2017_reach_paper.pdf
- https://people.cs.rutgers.edu/~mp2099/files/kim_iccd18_solar_paper.pdf

**Mismatch**
- https://research.ibm.com/publications/transistor-mismatch-properties-in-deep-submicrometer-cmos-technologies
- https://technav.ieee.org/topic/transistor-mismatch/

**Fabrication routes and facilities**
- https://www.cmc.ca/globalfoundries-22fdx-fdsoi-22-nm-process/
- https://products.cmc.ca/Fabrication/DMT_Fab
- https://www.isi.edu/news/80945/mosis-2-0-revives-a-legacy-rehan-kapadia-outlines-a-bold-future-for-rapid-microelectronics-prototyping/
- https://allaboutcircuits.com/news/mosis-partners-with-globalfoundries-extending-40-year-prototyping-legacy
- https://europractice-ic.com/schedules-prices-2026/
- https://www.eenewseurope.com/en/tiny-tapeout-sees-industrial-boost-as-it-recovers-from-efabless-closure/
- https://www.crowdsupply.com/wafer-space/gf180mcu-run-2
- https://snfguide.stanford.edu/sites/default/files/sections/diplayfiles/fy20ratesheets-labuse.pdf
- https://nanolabs.stanford.edu/snfrates
- https://mailman.ecn.purdue.edu/archives/list/bnc-all@ecn.purdue.edu/message/QV6GR6XQBKTW7PU5OCDG7VQOPHRKJ2JN/attachment/6/BRKFY24RatesvsCurrent.pdf
- https://senic.gatech.edu/about/rates
- https://as.cornell.edu/index%2Ephp/news/nanotech-facility-gets-5-year-75m-renewal-nsf
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
