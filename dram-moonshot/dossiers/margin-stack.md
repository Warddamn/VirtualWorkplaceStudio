# MARGIN STACK: segment-gain, double-sampled, ECC-budgeted sensing that cuts the cell capacitor ~10x on oxide-access DRAM

NEW DRAM Stage 3 dossier. Author: agent `dosw-margin-stack`, 2026-11-02. Slug `margin-stack`.

Inputs: `models/margin-stack.py` (re-run 2026-11-02, exit 0, output identical to `research/stage3/margin-stack_model_output.md`), `research/stage3/margin-stack_notes.md`, `research/assumptions/dos-margin-stack.md`, and the source logs in §10.

Tags: [REPORTED] logged source, usually a snippet; [ESTIMATE] model or hand arithmetic; [SPECULATIVE] unmeasured physics; [training knowledge] no logged URL.

Program month M0 = 2027-01-01.

---

## 0. Header

| Field | Value |
|---|---|
| Name | MARGIN STACK |
| Thesis | Today's ~17,800-electron bit exists to beat bitline capacitance and amplifier offset, not noise. A 3-transistor gain stage per 32 cells, correlated double sampling (CDS) and a raw-BER-1e-4 row code shrink an oxide-access 4F2 cell's capacitor from 5.4 to ~0.5 fF. That is a 120 nm stub instead of a 1.3 µm, aspect-ratio-62 pillar. |
| Rank / EV | 1 of 10; EV 75 = S3 x P5 x D5 |
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

**Verdicts**
- **PHYSICALLY POSSIBLE? Yes.** No new physics. The thermal floor at raw BER 1e-4 is 0.024 fF, 20x below the 0.5 fF planning cell. Mismatch, coupling, wordline kick and the oxide leakage tail set the size, and all of them are engineering terms. The cut is legal only with oxide access: a silicon 13 fA tail empties 0.54 fF in ~3 ms.
- **STEP CHANGE IF IT WORKS? Yes, on capacitor-module capital and PFAS, plus 3D readiness.** The capacitor is ~10.8x smaller: 5.42 → 0.5 fF, 1,300 → 120 nm tall, AR 62 → 5.7. Array energy per access falls ~2.3x [ESTIMATE]. The stretch is 17-40x [SPECULATIVE]. **It is no step on $/bit** (-3% to +4%) **or density** (-8% against plain 4F2).
- **PROVABLE WITH $1M IN 24 MONTHS? Partly, strongly.** One 22FDX MPW, IGZO coupons and a DRAM Bender study settle the circuit question by M16-17: post-CDS residual, coupling and error clustering. The decisive experiment costs $520k (the model's $675k "experiments alone" line adds spin 2 and IP); with two founders the plan is $955k. No oxide VCT array is built. The oxide terms come from coupons and are combined with the silicon results by projection.

---

## 1. How it works

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

### 2.6 Energy, area, cost, 3D

- **Energy per sensed bit:** 20.1 fJ at 1-beta. MARGIN STACK: 0.99 local + 3.00 global restore + 2.40 two samples + 2.0 comparator = **8.8 fJ** [ESTIMATE; 6 fF global line].
- **Refresh, 16Gb die:** 12.2 mW (1-beta, 64 ms) vs **0.43 mW** (0.5 fF, 100 aA, droop-optimised, 2x guard, 917 ms). Oxide access supplies most of this.
- **Area (correcting the concept's "~9%, flat"):** 4 extra 4F2 sites per 32 cells, so **+12.5% array and +8.8% die**. That gives 0.701 Gb/mm²: 1.57x 1-beta, but -8% against plain 4F2 VCT (0.762).
- **Cost:** if the capacitor module is 10/15/20% of wafer cost [unsourced], $/bit is **+3.6 / +0.4 / -2.8%**, or $1.44-1.53/GB against $1.48. This includes one strap mask (1.2%).
- **3D:** a tier's lateral capacitor shrinks from 450 to **63 nm**. Per-tier density rises 2.8x, and break-even with 1-beta falls from ~26 to **~10 tiers**.

### 2.7 Against 1-beta DDR5

| Metric | 1-beta DDR5 | MARGIN STACK, oxide 4F2 |
|---|---|---|
| Capacitor | 5.42 fF, 1,302 nm, AR 62 | 0.5 fF, 120 nm, AR 5.7 |
| Stored electrons | 17,762 | 1,561 |
| Margin required | 7σ | 3.72σ + BCH t=8 |
| Density | 0.447 Gb/mm² | 0.701 (plain 4F2 0.762) |
| Energy per sensed bit | 20.1 fJ | 8.8 fJ [ESTIMATE] |
| Refresh power, 16Gb | 12.2 mW | 0.43 mW (100 aA tail) |
| $/GB | $1.48 | $1.44-1.53 |
| Added masks | — | +1 DUV; no EUV |

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
| NAND soft-bit sensing (US 11,907,545); XED [training knowledge] | 2016-24 | Not in DRAM silicon |
| Image-sensor source follower + CDS [training knowledge] | decades | Not memory |

**The genuine delta.** Every part is known; no snippet showed them combined into one margin budget on an oxide access device built to shrink the capacitor. Claimable:
1. A same-step oxide gain FET per segment, CDS through that FET, and Cs ≤ 0.5 Cseg with stub height ≤ ~10x diameter.
2. Kick compensation for short segments.
3. Biasing a high-Vt same-step gain FET.
4. Pair-aware codeword orientation.
5. A ≤ 100 nm lateral stub sized to a 16-tier segment.

No oxide VCT program has published a capacitor cut. If DOSRAM already runs ~1 fF cells on short stacked bitlines, the novelty narrows to items 1-3.

---

## 4. Show-stoppers and how persistence could get around them

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

## 9. Kill criteria

Physics-only. Each has a date and a revival condition.

1. **K1, 2027-07-01 (pairs).** Three vendors at emulated 1e-4 show ≥ 10% same-codeword pairs after remapping. This kills the ECC lever (allowed 1.7e-5). The concept survives if CDS meets the no-ECC numbers (~0.25 fF). *Revival:* < 1% pairs on oxide cells.
2. **K2, 2028-01-31 (tail).** The extrapolated IGZO 1e-10 tail at 85 °C is > 1,172 aA on two splits. That kills any cut beyond ~5.4x (Cs > 1 fF at 64 ms). *Revival:* an anneal or channel (imec H+O, In-lean) reaching ≤ 586 aA.
3. **K3, 2028-01-31 (hard tail).** The tail is > 6,352 aA, which fails 64 ms even at 5.42 fF. That kills the oxide-access premise. *Revival:* another access device below 586 aA.
4. **K4, 2028-06-30 (residual).** The projected oxide σ_res is > 34 mV with measured α. That kills the lever beyond ~5x. *Revival:* α ≤ 0.05 with shields and 64-cell segments.
5. **K5, 2028-06-30 (CDS).** CDS removes < 75% of the gain-FET offset. That kills CDS; the fallback is row H (0.60 fF, 4-pillar FETs, +9% array). *Revival:* spin 2 finds and fixes the drift source.
6. **K6, 2028-06-30 (coupling).** α with shields is > 0.20 *and* σ_res is > 14.5 mV. The planning cell rises above 0.5 fF, toward 1 fF. *Revival:* interleaving or a differential reference cuts α below 0.10.
7. **K7, 2028-06-30 (add-ons).** The neutraliser is unstable below Cn/Cbl 0.5, or the charge-transfer residual is > 3 mV. Those levers are dropped; the concept stands.
8. **K8, 2028-12-31 (reproduction).** Spin 2 misses spin 1's σ_res by > 30%: no raise rests on it until a third data set agrees.

---

## 10. Sources

All URLs are logged in `research/sources/*.jsonl`: mostly `dos-margin-stack.jsonl`, plus A1, A2, A3, B3, `dos-raw-ber-contract`, `dos-pixel-stack`, `dos-lean-array-module`, `dos-charge-river` and `dos-hot-side-memory`.

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
