# PIXEL-STACK: research notes (Stage 3 dossier)

Agent `dos-pixel-stack`, 2026-11-02. Model: `models/pixel-stack.py` (output: `research/stage3/pixel-stack_model_output.md`). Sources: `research/sources/dos-pixel-stack.jsonl`. Assumptions: `research/assumptions/dos-pixel-stack.md`. WebSearch budget used: 6 of 6. Search-snippet facts are tagged "(via search snippet)".

## 0. The concept and the verdict

**What it is.** A 3D 1T1C DRAM built from groups of 16 oxide-channel cell tiers. On top of each group sits an all-oxide "amp tier" that reads every vertical bitline (BL) the way a CMOS image sensor reads a pixel:
- The 16-cell vertical BL, plus a small shared node, acts as the floating diffusion.
- A reset transistor (RST) precharges it.
- An oxide source follower (SF) drives a column line through a select transistor (SEL).
- A correlated-double-sampling (CDS) column subtracts the reset sample from the signal sample.

CDS cancels the static SF offset (oxide-TFT Vt sigma of 30-100 mV) and the BL reset kTC. That removes the need for I-11545's bonded Smart-Cut c-Si layer per group. Because each BL is only 16 cells long (~3 fF), the in-tier capacitor needs only ~0.3-0.5 fF.

**Verdict.** The physics holds. The model reproduces the concept's density claim, and its central bet is narrower than the chief's framing suggested:
- **It works.** The modelled read chain closes at Cs 0.45 fF with ~15 mV to spare.
- **What could break it.** The read-noise risk is RTN/1/f in a *scaled* (≤0.01 µm²) oxide SF and coupling between neighbouring bitlines. Both can be measured on a planar test array.
- **The weakest link the model exposed is retention, not reading.** A 0.45 fF node needs ≤34 aA of tail leakage. That is met only if the oxide Vt sigma is ≤~30 mV *and* the hydrogen-induced Vt shift is ≤~10 mV after the full ≤400 °C stack.

| Headline (model, 85 °C) | Value |
|---|---|
| Lateral capacitor for 0.45 fF (EOT 0.50 nm, 69 fF/µm²) | **52 nm** (A1 base case ~500-600 nm) |
| Per-tier footprint | **0.0110 µm²** (70 × 157 nm); A1 base 0.030, optimistic 0.012 |
| Per-tier density (eff 0.55, ECC 592/512) | 0.043 Gb/mm² |
| 1-beta density break-even | **10.4 tiers** (A1 base 26) |
| 64 cell tiers (4 groups) | **2.76 Gb/mm² = 6.2× 1-beta** before tier yield |
| Wafer cost, 64 tiers, two amp sub-layers per group | ~$8,000; stack yield 0.86; **0.40× 1-beta $/bit ≈ $0.58/GB** vs $1.48/GB (Smart-Cut variant: 0.67×, $0.99/GB) |
| End-of-retention signal | 50 mV (~1,200 e- on a 3.8 fF node; 42 µV/e-) |
| Modelled post-CDS readout residual | **14.7 mV** (3.72σ random 9.3 mV + RTN tail 4.2 mV + coupling 1.2 mV after decision feedback). It is 21.5 mV without decision feedback |
| Allowed readout residual at 0.45 fF | 29.5 mV (18 mV at 0.30 fF; 40 mV at 0.60 fF) |
| Minimum Cs with the modelled readout | 0.20 fF (20 nm capacitor) |
| Tail leakage / spec / retention | 31 aA / 34 aA / **1.08 s** (34× DDR5's 32 ms hot interval) |
| tRC (share 2) / energy per accessed bit / refresh power | 55 ns / 89 fJ (DDR5 ~46 fJ per refreshed bit) / **17× lower** than DDR5 |

**GO/NO-GO (the decisive experiment)** is a planar IGZO pixel-amp array at 85 °C, on 3-3.5 fF floating nodes read by oxide SFs of gate area ≤0.01 µm². The measured quantity is the post-CDS readout residual: 3.72σ random noise + 1e-4 RTN tail + worst-pattern neighbour coupling.

| Residual | Verdict | What it means |
|---|---|---|
| ≤15 mV | **GO** | Cs could fall to 0.26 fF, so the 0.45 fF / 52 nm plan keeps ~15 mV for 3D-only effects |
| 15-30 mV | CONDITIONAL GO | 0.45 fF still closes, with no spare |
| >30 mV | **NO-GO as pitched** | The 30-60 nm capacitor claim fails |
| 30-65 mV | Degraded fallback | Cs 0.45-1.0 fF, ≤125 nm capacitor, 64 tiers ~4-6× 1-beta |
| >65 mV | Oxide amp tier dead | Revival is I-11545's Smart-Cut c-Si layer |

Retention gate, on the same run: tail node leakage ≤34 aA after a 400 °C / H₂ sequence, with access-TFT ΔVt <20 mV. It is NO-GO above ~100 aA.

## 1. Closest prior art and who is pursuing it

### 1a. 3D DRAM programs (the cell this concept reads)
| Who | What | Date | Relevance |
|---|---|---|---|
| Samsung | VS-DRAM: 16 tiers, GAA lateral transistors, horizontal capacitor, BL shield, chip-level R/W. Cs grows ~linearly with capacitor length; peri-on-cell bonded ([SemiEngineering](https://semiengineering.com/baby-steps-towards-3d-dram/); VLSI 2026 via A3 §2.3) | VLSI 2026; product ~2030 | The incumbent route. Its capacitor scales with lateral length, which is exactly what PIXEL-STACK shortens 10× |
| Samsung | 10a 4F² IGZO-channel VCT working die, periphery wafer-bonded. 3D from 10d ([TrendForce 2026-04-24](https://www.trendforce.com/news/2026/04/24/news-samsung-reportedly-produces-sub-10nm-10a-dram-working-die-using-4f-square-and-vct-targets-2028-production/)) | 2026; MP 2028 | Shows the incumbents accept IGZO access devices |
| SK hynix | 5-tier stacked 3D DRAM at 56.1% test yield; says 32-192 layers are needed ([Guru3D](https://www.guru3d.com/story/sk-hynix-achieves-yield-in-fivelayer-3d-dram-development)) | VLSI 2024 | Yield compounding; break-even tier count |
| Kioxia (+Nanya) | 3D OCTRAM: SiN→IGZO replacement makes horizontal transistors in 8 tiers at once. Ion >30 µA, Ioff <1 aA, no retention data ([Kioxia 2025-12-12](https://www.kioxia.com/en-jp/about/news/2025/20251212-1.html)) | IEDM 2025 | Closest cell-tier process. Kioxia is the most likely licensee/partner for an oxide amp tier |
| CXMT | BEOL IGZO 3D DRAM select device: 60.9 µA/µm, Vt 0.28 V, SS 80 mV/dec (A3 §1, IEDM 2025 paper 29-3) | IEDM 2025 | Drive and SS used in the model |
| IMECAS + Beijing Super String | 4-tier dual-gate IGZO 2T0C, 3 b/cell, 400 s ([IT Home](https://www.ithome.com/0/966/543.htm)) | VLSI 2026 | Capacitorless competitor route |
| imec/Ghent | 120 Si/SiGe bilayers, still defective (A1 §6) | 2025-26 | The Si-channel route PIXEL-STACK avoids (no Ge) |
| NEO Semiconductor | 3D X-DRAM single-cell PoC (A3 §2.4) | 2026 | Company-reported |

### 1b. Segmented / hierarchical bitlines in 3D DRAM (patents to watch)
All of the following are titles or snippets from one search. Claims were not read, and assignees were not confirmed unless stated.
- **US 12,207,458** "Methods and apparatus for hierarchical bitline for three-dimensional DRAM": local and global BLs; vertical-WL access devices switch the local BL onto the global BL; SAs in FinFET CMOS; aim is lower BL capacitance ([USPTO](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12207458), via search snippet). **Closest structural prior art for bounding the BL.** It still senses with a CMOS SA, with no in-stack gain and no CDS.
- **US 12,603,114** "Memory device": per-layer global BLs, vertical BLs reached through BL-select transistors, shared SAs ([USPTO](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12603114), via search snippet).
- **EP 4567797 / 4567798 / 4567799**: BL-select and precharge transistors from local to global BLs; vertical-BL sub-blocks feeding global BLs; vertical-WL 3D DRAM ([EPO 797](https://data.epo.org/publication-server/rest/v1.2/patents/EP4567797NWA1/document.html), [798](https://data.epo.org/publication-server/rest/v1.2/patents/EP4567798NWA1/document.html), [799](https://data.epo.org/publication-server/rest/v1.2/patents/EP4567799NWA1/document.html), via search snippet). The local-to-global select and precharge transistors resemble our SEL/RST, but without a follower or double sampling.
- **US 12,010,831** "3D DRAM with multiple memory tiers and vertically extending digit lines" ([Google Patents](https://patents.google.com/patent/US12010831)). Metadata only. "Digit line" is Micron vocabulary, so it is probably Micron [inference, UNVERIFIED].
- **US 11,600,309** "3D memory with 3D sense amplifier" (vertical-transistor SAs, BL muxes) ([Justia](https://patents.justia.com/patent/11600309)); **US 11,443,780** "Vertical access line multiplexor" ([USPTO](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11443780)).

### 1c. Local gain and offset cancellation in DRAM
- IBM SOI eDRAM micro sense amplifier: 3T per ~32-cell local BL (Barth, ISSCC 2007 / JSSC 2008; via Stage 2 search snippets). This is the original "local gain per short BL", done in c-Si.
- Samsung and SK hynix offset-cancellation SAs (OCSA) ship in DDR4/5 (Stage 2, training knowledge). Offset cancellation is not new in DRAM. What is new here is doing it with oxide devices in the stack.

### 1d. SEL DOSRAM: oxide cells stacked on sense amps
- SEL patents describe DOSRAM (an IGZO 1T1C) with the SA unit and the cell array stacked: a 1 Kb local array over 128 SAs. Stacking cuts operating energy ≥70%, and the arrays themselves can be stacked ([US 10,622,059](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10622059), [US 11,094,373](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11094373), [US 9,368,501](https://patents.google.com/patent/US9368501); via search snippet).
- The SAs are Si CMOS. SEL is the strongest holder of IP on oxide-cell-over-SA, and a patent family to clear.

### 1e. Oxide-TFT pixel amplifiers with CDS: the image-sensor half of the idea
- **De Roose et al., IISW 2015.** Large-area APS imagers with self-aligned a-IGZO TFTs. They compare source-follower and common-source pixel amps and note that CDS partly compensates the extra TFT noise ([paper](https://imagesensors.org/Past%20Workshops/2015%20Workshop/2015%20Papers/5-15_%20De%20Roose%20et%20al.pdf), via search snippet). **This proves that an oxide SF plus CDS works as a readout chain**, at display-scale (µm) geometry.
- **US 11,477,398**: an oxide-TFT active pixel with RST, SEL and SF feeding a CDS readout, with TFT Vt stored on a capacitor ([USPTO](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11477398)).
- **US 10,187,597**: an APS that compensates SF-TFT process variation ([Google Patents](https://patents.google.com/patent/US10187597)).
- **US 12,615,863**: an image sensor with a nitrogen-doped metal-oxide active pattern **on a hydrogen-blocking layer** ([USPTO](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12615863)). This is directly relevant to an H-barrier claim in the amp tier, so read its claims before filing.

### 1f. The delta, and the novelty status
None of the sources seen combine all four elements:
- (i) a vertical BL bounded every N tiers;
- (ii) read as a floating diffusion by an in-stack oxide SF/RST/SEL tier;
- (iii) with CDS;
- (iv) with a margin budgeted to ECC at 1e-4.

The search was six queries. It was not a freedom-to-operate (FTO) search. The hierarchical-BL patents (1b) and the oxide-APS patents (1e) are the two families an examiner would combine against us. Filings should claim the specific combinations listed in §6.

## 2. Best demonstrated numbers per component

| Component | Best number found | Source | Model input / gap |
|---|---|---|---|
| Oxide access-TFT leakage | Ioff <1 aA, Ion >30 µA, 8 horizontal tiers | [Kioxia 3D OCTRAM, IEDM 2025](https://www.kioxia.com/en-jp/about/news/2025/20251212-1.html) | Median 1 aA at 85 °C (temperature not stated in the source) |
| Oxide select drive / SS | 60.9 µA/µm; SS 80 mV/dec; Vt 0.28 V | CXMT IEDM 2025 (A3 §1) | SS 80 mV/dec; SF Id 2 µA at W = 0.1 µm |
| Oxide retention | 2T0C >200 s at 95 °C (Lg 40 nm); IGO >30,000 s; 3D 4-tier 2T0C 400 s | [imec EDL 2025](https://imec-publications.be/entities/publication/948b2190-065d-48d2-a9b9-4f4ecd22c234); SJTU AFM 2026; IMECAS VLSI 2026 (A3 §2.1) | We need 1 s at the 1e-4 tail on 0.45 fF |
| Oxide endurance | >1e12 cycles at 95 °C (measurement-limited) | imec EDL 2025 | Worst case 5.8e15 accesses in 10 years at tRC 55 ns: a 4-decade gap to show |
| Oxide PBTI / H | Standard and In-poor IGZO drift in opposite directions; H+O anneal cuts H-doping ~30× | [imec IEDM 2025](https://imec-publications.be/handle/20.500.12860/59908) | dVt <20 mV target after the stack |
| Oxide thermal stability | ALD In₂O₃ FETs survive 600 °C; vertical all-oxide TFTs >160 µA/µm | [Purdue EDL 2024](https://engineering.purdue.edu/~yep/Papers/EDL_2024_In2O3%20600C_Lin.pdf), [Purdue VLSI 2024](https://engineering.purdue.edu/~yep/Papers/VLSI2024%20T4-1_Zehao%20Lin.pdf) | Ga-free channel option; vertical amp-tier transistors |
| Oxide 1/f | Hooge α ≈1.5e-3 (long-channel a-IGZO); ≈6e-3 (Al₂O₃/SiNx); Al₂O₃-only gates 100-1000× noisier (normalized) | [Fung JAP 2010](https://web.eecs.umich.edu/omelab/downloads/Fung%20JAP%202010.pdf); Cho EDL 2009 ([record](https://scholarworks.bwise.kr/cau/handle/2019.sw.cau/50716)), via search snippet | **Scaled ALD IGZO is dominated by near-interface traps** (Lee & Niu, IEEE TED 2025, via search snippet). There are almost no data below ~1 µm². **This is the key gap** |
| Oxide pixel + CDS | a-IGZO APS imager, SF vs CS, CDS compensation | [De Roose IISW 2015](https://imagesensors.org/Past%20Workshops/2015%20Workshop/2015%20Papers/5-15_%20De%20Roose%20et%20al.pdf) | Display-scale only |
| 3D DRAM tiers | 16 tiers with chip-level R/W (Samsung); 5 tiers at 56.1% (SK hynix) | A1 §6 | Per-tier yield ≥0.998 after repair is needed for 64 tiers |
| Capacitor dielectric | ZrO₂-based EOT ~0.55 nm in 1-beta | A1 §2 | Model uses 0.50 nm and J 1e-7 A/cm² at 0.5 V |
| Si CIS pixel (for scale) | ~1-2 e- rms read noise on ~1-2 fF floating diffusions [training knowledge, UNVERIFIED] | — | We need only ~2.5 mV rms ≈ 60 e- on 3.8 fF: **30-60× worse than a phone-camera pixel is acceptable** |

## 3. What the model says, and the surprises

1. **Reading is not the binding constraint at the design point.** CDS cuts the random read noise to 2.5 mV rms. The terms are SF 1/f 1.34 mV, uncancelled BL kTC on the shared BL 1.20 mV, column offset 1.11 mV, SF thermal 0.90 mV, kickback variation 0.87 mV and cell kTC 0.43 mV. Against a 50 mV signal, that gives Cs_min ≈ 0.20 fF.
   - The 1/f term needs care. CDS-filtered 1/f grows only logarithmically: F = 2[ln(2π·fc·Δt) + γ] ≈ 5.7, and the numerical integral matches.
   - Two things can break the read instead. A scaled SF (50×50 nm) or a noisy gate stack (α ≥3e-2 at 100×100 nm) fails at 0.45 fF; see the sensitivity table. **The SF must keep ≥~0.01 µm² of gate area and a SiNx-capped, low-trap gate stack.**
2. **Coupling between neighbouring bitlines is the largest single deterministic term without a fix.** It is 8 mV (2 × 0.08 × signal). Decision feedback cuts it to 1.2 mV: shift each node's threshold by the neighbours' decided bits, as NAND does for BL-BL interference.
   - Without decision feedback the residual is 21.5 mV. That still passes at 0.45 fF, but it fails once Cc/C_BL reaches 0.2.
   - Even/odd shielding does **not** work for 1T1C. Every cell on an activated WL is destroyed and must be sensed.
3. **Retention, not reading, is the tight constraint.** The tail leakage is 31 aA against a 34 aA spec.
   - At σVt = 30 mV, a 20 mV hydrogen-induced Vt shift drops the tail retention to 0.67 s. At σVt = 50 mV it is 0.15 s.
   - Raising capacitor leakage to 1e-6 A/cm² gives 0.38 s.
   - Retention between 0.06 and 1 s is still a large refresh win, but it misses the concept's ≥1 s claim.
4. **Area in the amp tier forces either CIS-style sharing or two sub-layers.** One vertical BL gets 0.022 µm² of amp-tier area. SF + RST + SEL need 0.047 µm².
   - Share 2 (two BLs per SF through transfer gates) needs two sub-layers and gives tRC 55 ns.
   - Share 4 still needs two sub-layers, and tRC rises to 106 ns.
   - A **pillar-gated SF**, where the BL pillar itself gates an oxide channel shell in the amp tier, would remove the SF footprint. It is a filing candidate (§6).
5. **Energy per access is about 2× DDR5 per bit, while refresh power is about 17× lower.** The SF bias current dominates: 2 µA × 1.2 V × 16 ns ≈ 38 fJ core. A pulsed column bias and lower Id trade speed for energy.
6. **Group size.** With the modelled readout, 32-tier groups give a lower $/bit (0.28×) than 16-tier groups (0.31×), because there are fewer amp tiers. The 16-tier group is the robust choice; 32 tiers is the upside if the measured residual comes in ≤10 mV.
7. **Cost.** At $300 per amp sub-layer, 64 tiers cost 0.40× 1-beta per bit. A Smart-Cut layer at ~$2,000 per group gives 0.67×, which is ~1.7× worse per bit. With a $15-60 cell tier and $150-600 amp sub-layers, the range is 0.30-0.62×. Confidence in the $/tier inputs is low.

## 4. The decisive experiment (step by step)

**Principle.** The planar array measures every quantity in the GO line. The 3D stack is a raise milestone. Build the readout as a 4,096-node "imager without photodiodes", which means a 64 × 64 array of pixel-amp nodes per die. Read ≥16 dies (65,536 nodes) so the 1e-4 tail is observed directly, with ~6 events per corner, rather than extrapolated.

### Stage A: design and noise modelling (months 0-3)
1. Calibrate the noise model in `models/pixel-stack.py` to literature IGZO PSDs. Build SPICE decks in ngspice/Xyce: SF, RST, SEL, TG and the CDS column, with the 15 ns sample gap.
2. Lay out three coupon designs. Each has:
   - an SF area ladder of 50×50, 100×100, 150×200, 300×300 and 1000×1000 nm (e-beam for the small ones);
   - a matched node-capacitance ladder of 2, 3 and 4 fF ZrO₂ MIM to emulate the BL;
   - Cs emulation of 0.2, 0.3, 0.45, 0.6 and 1.0 fF;
   - aggressor neighbour lines with Cc/C_BL of 0, 0.05, 0.1 and 0.2;
   - dummy WLs for kickback cancellation;
   - a depletion-mode SF split (In-rich) and an enhancement-mode access-TFT split (In-poor, or Ga-free In₂O₃/ITZO).

### Stage B: planar pixel-amp coupons (months 2-10). Seed go/no-go at month 9
3. Fabricate 2-3 lots on 100-150 mm Si/SiO₂ at Purdue Birck or Georgia Tech IEN:
   - bottom TiN/W gate;
   - ALD HfO₂/Al₂O₃ gate dielectric with a SiNx cap (the Cho 2009 result says the cap matters 100-1000× for noise);
   - ALD IGZO or In₂O₃, 8-10 nm;
   - ALD ZrO₂/TiN MIM;
   - two-level metal.
4. Read the arrays with a board-level readout (FPGA + 16-bit ADC + low-noise buffer) and an on-coupon oxide column buffer. The off-chip column is slow (µs), so:
   - (a) measure each SF's input-referred PSD from 1 Hz to 10 MHz and its RTN traces at 25, 55 and 85 °C;
   - (b) run CDS at the achievable gap and compute the 15 ns-gap residual from the measured PSD. The model's F factor depends only logarithmically on the gap, so this extrapolation is short;
   - (c) once the MARGIN STACK MPW chip exists, read the coupon through its CDS column, die-to-die wire bonded.
5. Measure the residual distribution over 65k nodes, under checkerboard, all-0, all-1 and walking-1 aggressor patterns. Apply decision feedback in software.
6. Measure retention with the pixel amp as the meter. Floating-node decay over 1-10⁴ s at 85 °C resolves ~1e-20 A on 3 fF (1 mV in 1,000 s ≈ 3e-21 A), so no electrometer is needed.
7. Run the hydrogen / 400 °C sequence. Splits: as-built; 400 °C N₂; 400 °C forming gas; H-rich PECVD SiN; each of these with and without an ALD Al₂O₃ barrier. Remeasure ΔVt, Ioff tail, noise and residual. Add SIMS H depth profiles on witness wafers.
8. Make lateral-capacitor coupons: 2-4 tier SiO₂/SiN stacks with a 30-60 nm lateral recess filled with TiN/ZrO₂/TiN, using ALD at Argonne CNM under a non-proprietary user proposal. Measure C density (target ≥60 fF/µm² equivalent) and J at 0.5 V, 25-85 °C, before and after 400 °C.
9. **Seed go/no-go (month 9):** apply the GO line in §0.

### Stage C: 4-tier stack plus one amp tier (months 9-21). Raise milestone
10. Build a 4-tier oxide 1T1C stack: SiN→IGZO replacement channel in the Kioxia style, or a deposited lateral channel, with a vertical BL pillar and 30-60 nm lateral capacitors. Put one two-sub-layer amp tier on top. Partners: Purdue Birck / GT IEN, with Argonne CNM for ALD.
11. Measure, on ≥1e4 cells:
    - signal ≥50 mV at Cs ≤0.5 fF;
    - residual ≤15 mV;
    - retention ≥1 s at 85 °C at the 1e-4 tail;
    - ΔVt of the bottom tiers after the amp tier's thermal and H budget.
12. Optionally post-process the amp tier as BEOL on a sky130 die (ChipFoundry), to get realistic CDS timing on-chip.

### Stage D: package (months 21-24)
13. Assemble a data room for a $10-50M raise, with a partner pitch to Kioxia/Nanya, Samsung, SK hynix and Micron. File the claims in §6.

### Budget (≤$1M, ≤24 months)
| Line | $k | Basis |
|---|---|---|
| Modelling, SPICE/TCAD (open tools; academic TCAD through a partner) | 15 | ESTIMATE |
| Planar coupons: 3 lots × ~400 h × ~$120/h door+tool, e-beam, ALD precursors, targets | 150 | Notre Dame $124/h external, Penn $70/h industry door, UW e-beam $495/h industrial ([ND](https://nanofabrication.nd.edu/facility-access/fees/), [Penn](https://nano.upenn.edu/?p=7074), [UW](https://www.wnf.washington.edu/docs/WNF-Rates.pdf)); SNF/Birck/IEN rates not found |
| Readout: FPGA/ADC boards plus a sky130 (ChipFoundry) or GF180 (wafer.space, ~$7k per 1,000 ICs) CDS-column die; packaging | 30 | [wafer.space interview](https://www.electronics-lab.com/e-lab-interview-wafer-space-founder-aims-to-make-custom-silicon-accessible-again/) (via snippet); ESTIMATE |
| Test set: used SMU/parameter analyser, low-noise preamp, spectrum analyser, hot chuck, probe cards | 80 | ESTIMATE (used-equipment market) |
| H/400 °C splits, SIMS H profiles, anneal-furnace time | 25 | ESTIMATE (~$1-2k per SIMS profile, training knowledge) |
| Lateral-capacitor coupons (Argonne CNM proposal, no user fee if non-proprietary [UNVERIFIED]; travel, materials) | 20 | ESTIMATE |
| 4-tier stack + amp tier: 3 lots, ~1,800 h facility, e-beam, ALD | 330 | ESTIMATE at $120-150/h |
| Sponsored research: one student or postdoc at the partner lab, ~12 months | 120 | ESTIMATE |
| IP: 2 provisionals → 1 PCT + 1 US non-provisional, plus a freedom-to-operate (FTO) search | 45 | ESTIMATE |
| Lean founder stipends (balance carried by the program-level seed) | 150 | ESTIMATE |
| Contingency (~4%) | 35 | |
| **Total** | **1,000** | Experiments 770 (seed go/no-go spend by month 9: ~$300k) |

If PIXEL-STACK runs inside the shared program seed (FINAL_CONCEPTS: one 28/22 nm MARGIN STACK MPW of ~$275k reads every coupon), its incremental cost is the concept card's ~$150k (Stage B) plus ~$500k (Stage C).

### Timeline
| Months | 0-3 | 2-6 | 5-9 | 9 | 6-12 | 9-18 | 18-21 | 21-24 |
|---|---|---|---|---|---|---|---|---|
| Work | Design, model calibration | Coupon lot 1, noise PSD | Lot 2, 65k-node residual, retention, H splits | **Seed GO/NO-GO** | Lateral-cap coupons (CNM) | 4-tier + amp-tier lots | Integrated measurements | Data room, filings, raise |

## 5. U.S. facilities, rates and partners

| Facility | Role | Cost / rate information |
|---|---|---|
| **Purdue Birck** | ALD In₂O₃/IGZO; vertical all-oxide TFTs (P. Ye group) | Rates not found; plan $110-150/h |
| **Georgia Tech IEN** | Oxide BEOL transistors; 3T0C gain cell (IEDM 2025); In₂O₃ BTI under 400 °C forming gas (S. Yu, A. Khan, S. Datta) ([GT](https://shimeng.ece.gatech.edu/?p=916)) | Rates not found |
| Stanford SNF | ALD, e-beam, M3D know-how | Rates not found |
| Cornell CNF; MIT.nano | E-beam, ALD; backup line | Not searched |
| Penn Singh (Quattrone) | Backup fab | $35/h academic, **$70/h industry** door; academic cap $6k per semester ([Penn](https://nano.upenn.edu/?p=7074)) |
| Notre Dame NDNF | Backup fab, staff processing | **$124/h external** cleanroom; $125/h staff; SEM $190/h, 2026 ([ND](https://nanofabrication.nd.edu/facility-access/fees/)) |
| Benchmarks | — | TAMU $150/h industry ([AggieFab](https://aggiefab.tamu.edu/fees)); KU staff $143/h external-market ([KU](https://nanofab.ku.edu/rates-fees)); UW e-beam $495/h industrial ([WNF](https://www.wnf.washington.edu/docs/WNF-Rates.pdf)). Industry rates are typically 2-3× academic |
| **Argonne CNM** | ALD of lateral capacitors and channels | User proposal. DOE NSRCs typically charge no fee for non-proprietary work [UNVERIFIED] |
| Sandia CINT / MESA; ORNL CNMS; LBNL Molecular Foundry | Characterisation (TEM of 30-60 nm recesses, H analysis) | Proposal-based [UNVERIFIED] |
| NIST CNST NanoFab | Fee-based fab; backup | Rates not searched |
| ChipFoundry (sky130, SkyWater MN, U.S. fab) | CDS column chip; BEOL host die | A shuttle runs only if ≥50% of slots fill ([Tiny Tapeout](https://tinytapeout.com/news/chipfoundry-sponsor/)) |
| wafer.space (GF180) | Cheap CDS/comparator die | ~$7k per 1,000 ICs; fabbed at GF Singapore, not U.S. ([Crowd Supply](https://www.crowdsupply.com/wafer-space/gf180mcu-run-3)) |
| MOSIS 2.0 (USC ISI) | 12-350 nm shuttles, >35 MPWs ([ISI](https://www.isi.edu/news/80945/mosis-2-0-revives-a-legacy-rehan-kapadia-outlines-a-bold-future-for-rapid-microelectronics-prototyping/)) | Via the program |
| NY CREATES Albany | 300 mm 16-tier stacks after the raise | Concept card; not searched |

**Collaborators and recruits.**
- Purdue (Peide Ye): ALD In₂O₃, 600 °C-stable and vertical all-oxide TFTs. Best fit for the amp tier and the Ga-free channel.
- Georgia Tech (Shimeng Yu, Asif Khan, Suman Datta): oxide BEOL gain cells and BTI under 400 °C forming gas. Best fit for 3D integration and reliability.
- Lee & Niu (IEEE TED 2025, LFN in scaled ALD IGZO; affiliation not confirmed): the noise-measurement methodology for scaled devices.
- Image-sensor readout advisor: Eric Fossum (Dartmouth; CMOS APS, QIS jots) [training knowledge, UNVERIFIED availability]. Plus a recruited CIS-readout engineer from Sony, OmniVision or onsemi.
- Oxide-APS authors: De Roose et al. (IISW 2015; the group is KU Leuven/imec per training knowledge [UNVERIFIED]).
- **Device/circuit co-founder profile:** oxide-TFT circuits plus CIS CDS readout experience, ideally ex-3D-DRAM (Samsung, SK hynix, Micron, Kioxia).

## 6. IP landscape

**Patents to watch:**
- 3D DRAM hierarchical BLs: US 12,207,458; US 12,603,114; EP 4567797/798/799; US 12,010,831; US 11,600,309; US 11,443,780.
- SEL DOSRAM stacking: US 10,622,059; US 11,094,373; US 9,368,501.
- Oxide APS with CDS: US 11,477,398; US 10,187,597; US 12,615,863 (H-blocking layer under the oxide pixel).
- Monolithic 3D Inc. ion-cut patents and CEA-Leti CoolCube (Stage 2, training knowledge).
- Samsung and SK hynix OCSA patents.

**What to file** (provisionals by month 3, before any publication):
1. **The system claim.** A 3D memory with vertical BLs bounded every N cell tiers by an in-stack oxide-semiconductor tier holding a reset device, a source follower whose gate is the vertical-BL node, and a select device. A correlated-double-sampling read subtracts the reset and signal samples. Dependent claims cover N = 8-32, Cs ≤1 fF, and restore through the reset device.
2. **Decision-feedback coupling compensation** in CDS-read DRAM: each node's decision threshold is shifted by its neighbours' first-pass decisions or soft values, with the coupling coefficients calibrated at test.
3. **The pillar-gated source follower.** The vertical-BL pillar continues into the amp tier and gates an oxide channel shell wrapped around it, so the SF uses no extra footprint.
4. **Pixel-style sharing for vertical BLs.** Per-BL transfer gates onto one shared floating node and SF. The restore path runs through the reset/write line. The read is sequenced so the shared BLs' reset kTC sits inside the margin.
5. **Dual-composition oxide stack.** A depletion-mode (In-rich) SF and an enhancement-mode (In-poor or Ga-free) access TFT, with an Al₂O₃/SiNx H-barrier between the amp tier and the cell group below.
6. **Test method.** The in-stack SF as a zeptoamp node-leakage monitor, used for per-node retention binning and refresh-rate assignment.
7. **Co-design rule.** Group size N and Cs chosen against a raw-BER-1e-4 ECC margin. Claim it narrowly; it is likely obvious on its own.

## 7. Open gaps
- **1/f and RTN of scaled ALD oxide SFs at 85 °C.** The literature is at µm scale. This is the decisive unknown, and Stage B measures it.
- **Oxide Vt sigma at Lg ≈40-100 nm.** It sets both the retention tail and the SF operating-point spread. The model assumes 30 mV. Retention fails 1 s at 50 mV.
- **Hydrogen and thermal accumulation.** Group 1 sees the full thermal and H budget of groups 2-4 and their amp tiers. Stage C must measure bottom-group ΔVt after the top amp tier is built.
- **Capacitor leakage at EOT ≈0.5 nm, crystallised at ≤400 °C.** At 1e-6 A/cm² the dielectric alone breaks 1 s retention.
- **Vertical-BL capacitance per tier.** The model assumes 0.15 fF, which needs a 3D field-solver extraction. Each +0.05 fF per tier lowers the signal by ~10%.
- **WL-WL disturb and row hammer in oxide 1T1C.** There are no data (A1 #9). Add a hammer test to Stage C.
- **Endurance.** The demonstrated 1e12 cycles (measurement-limited) sits 4 decades below the worst-case 10-year access count.
- **Speed and energy.** tRC is 55 ns at share 2, and access energy is ~2× DDR5 per bit. Both are acceptable for DRAM-class but worse than DDR5. A pulsed bias and lower Id need verifying.
- **Amp-tier area.** Two sub-layers are needed unless the pillar-gated SF works. Each sub-layer costs ~$300 per wafer (ESTIMATE).
- **Gallium.** Ga is ~98% Chinese and the export-ban suspension ends 2026-11-27 (A2). Qualify an In₂O₃ or ITZO channel in the Stage B splits.
- **Patents.** A professional FTO search on families 1b, 1d and 1e is required before the raise.
- **Cost inputs.** $/tier, $/amp sub-layer and repaired tier yield are low-confidence ESTIMATEs inherited from A1.
