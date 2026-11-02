# PIXEL-STACK: technical dossier

*Agent `dosw-pixel-stack`, 2026-11-02.*
- Model: `models/pixel-stack.py`, re-run 2026-11-02 (exit 0); output in `research/stage3/pixel-stack_model_output.md`.
- Notes: `research/stage3/pixel-stack_notes.md`. Assumptions: `research/assumptions/dos-pixel-stack.md`.
- Sources: `research/sources/dos-pixel-stack.jsonl`, plus cross-references in the other logs.

Numbers are model outputs unless sourced. [ESTIMATE] = modelled judgement; [SPECULATIVE] = plausible, unshown physics.

---

## 0. Header

**Name.** PIXEL-STACK: image-sensor-style group-sensed 3D 1T1C DRAM, with an all-oxide source-follower and CDS "amp tier" every 16 cell tiers.

**Thesis.** Read each 16-cell vertical bitline the way a camera reads a pixel. An oxide source follower plus correlated double sampling (CDS) cancels the transistor offsets that used to require a bonded silicon layer. That lets the 3D capacitor shrink from ~600 nm to ~52 nm, with the whole stack oxide and ≤400 °C.

**Rank / category.** Rank 5 of 10 (EV 4 × 3 × 4 = 48); cell/array.

**Constituent ideas and technique lineage.**

| Id | Contribution | Technique |
|---|---|---|
| I-11545 / N-48 | Sense layer every 16 tiers bounds the bitline to ~3 fF, so 0.3-0.6 fF fits a 30-60 nm capacitor | Phase B lens (B3); triage ALIVE |
| I-00257 | Local gain transistor per 16-cell segment | SCAMPER-Substitute |
| I-05218 | CDS sense amps cancel offset and reset kTC | First principles |
| I-02936 | All-oxide n-only periphery (TRIZ #33 Homogeneity) | TRIZ |
| I-11559 | ECC-paid margin: raw BER 1e-4 = 3.72σ | Phase B lens (B4) |
| I-00729 | Tier-orthogonal codewords | SCAMPER-Combine |
| I-07812 | "Local post offices": a sense amp every ~32 cells | Perspective shift / personas |
| I-01381 | A few hundred electrons suffice on a quiet read path | SCAMPER-Magnify/Minify |
| N-40 | Hierarchical 64-cell bitlines, sense amps bonded under the array | Phase B lens (B3); triage ALIVE |

Merge: device-lens PIXEL-STACK plus system-lens Margin Stack segmentation; the chief staged a planar test before the 3D build.

**Verdicts.**
- **PHYSICALLY POSSIBLE? Yes.** No physics is violated.
  - The modelled read closes with ~2× margin: 14.7 mV residual against 29.5 mV allowed at Cs 0.45 fF.
  - Retention closes only narrowly: 31 aA tail against a 34 aA spec. At oxide σVt 30 mV that leaves almost no room for hydrogen shift (≤~3 mV; 10 mV gives 0.85 s); σVt 20-25 mV tolerates ~20-40 mV.
- **STEP CHANGE IF IT WORKS? Yes, on density.**
  - 64 tiers give 2.76 Gb/mm², **6.2× 1-beta** before tier yield. That is ~2.5× the incumbent-style 3D base case.
  - Secondary gains: ~2.5× bits/$ (low confidence) and ~17× lower refresh power.
- **PROVABLE WITH $1M IN 24 MONTHS? Partly.**
  - A ~$300k planar array settles the decisive unknowns by month 9: the scaled oxide source-follower residual, and leakage after 400 °C/H₂.
  - A 4-tier stack fits in $1M only with partner labs.
  - 64-tier yield cannot be shown at this budget.

---

## 1. How it works (for a smart non-engineer)

A DRAM bit is a tiny bucket of charge (a capacitor) behind a tap (a transistor). To read it, you open the tap onto a long shared wire, the bitline, and detect the small voltage nudge. Today's bitlines are long (~35 fF), so each bucket must be large (~5 fF). That forces the 60:1 capacitor towers known as the "capacitor wall".

3D DRAM stacks cells in tiers like 3D NAND, capacitors lying sideways. The vertical bitline grows with every tier, so the base case needs a ~600 nm sideways capacitor and ~26 tiers to match 1-beta (A1 §6).

A phone camera solves the same problem. A pixel holds a few thousand electrons, and a tiny amplifier sits right at the pixel (a "source follower"). The readout takes a "reset" sample and a "signal" sample and subtracts them. This correlated double sampling erases the amplifier's offset and the reset noise.

PIXEL-STACK copies this:
- Every 16 tiers there is a thin **amp tier**, and the 16-cell bitline is the "pixel".
- The short bitline (~3 fF) makes 0.45 fF enough, which fits a 52 nm capacitor.
- The amp transistors are the same oxide semiconductor (IGZO or In₂O₃) as the cells, made at ≤400 °C.
- Oxide transistors have large offsets (30-100 mV), but CDS cancels any static offset.

```
     column line --> CDS comparator in logic periphery ("reset" sample, "signal" sample, subtract)
        ^
  +-----|---------------------------------------------------+
  | AMP TIER (oxide, 2 sub-layers)                           |
  |   SEL ---- SF (its gate IS the floating node) ---- RST   |
  |                 |                                        |
  |         TG -----+----- TG        (2 bitlines share 1 SF) |
  +---------|---------------|--------------------------------+
  tier 16  [C]=T==|      [C]=T==|     T = oxide access transistor
    ...           |             |     C = 52 nm sideways capacitor, 0.45 fF
  tier 1   [C]=T==|      [C]=T==|     | = vertical bitline, 16 cells, 3.0 fF
  +---------------------------------------------------------+
  |  next 16-tier group + amp tier ... (x4 = 64 tiers)       |
  |  base wafer: decoders, CDS columns, I/O                  |
  +---------------------------------------------------------+
```

A read runs in five steps:
1. RST precharges the bitline, and the column samples it.
2. A wordline opens one tier, and the cell shares its charge with the bitline.
3. The column samples again.
4. The difference between the samples is the bit.
5. The bit is written back, because the read is destructive.

---

## 2. The physics and the numbers

### 2.1 Design point (85 °C, Cs 0.45 fF, 16-tier groups)

| Quantity | Arithmetic | Value |
|---|---|---|
| Capacitor | (0.45 fF ÷ 69.1 fF/µm² at EOT 0.50 nm − 750 nm² end cap) ÷ 110 nm perimeter | **52 nm** (A1 base ~600) |
| Cell footprint per tier | 70 nm × (20 BL + 70 TFT + 52 cap + 15 plate) | **0.0110 µm²** (A1 base 0.030) |
| Bitline / shared node | 16 × 0.15 + 0.6 fF; 0.25 + 2 × 0.05 fF | 3.00 fF / 0.35 fF |
| End-of-retention signal | (0.5 − 0.075 V) × 0.45 ÷ (0.45 + 3.0 + 0.35) | **50.3 mV** (concept 55) |
| Conversion gain | q ÷ 3.80 fF | 42 µV/e⁻; signal ≈ 1,194 e⁻ |
| Per-tier density | 0.55 efficiency ÷ (0.0110 µm² × 592/512 ECC) | 0.0432 Gb/mm² |
| 1-beta break-even | 0.447 ÷ 0.0432 | **10.4 tiers** (A1 base 26) |
| 64 tiers | 64 × 0.0432 | **2.76 Gb/mm² = 6.2×** |

### 2.2 Read noise after CDS

The source follower (SF) is 100 × 100 nm, EOT 3 nm, 2 µA, gm 10 µS, driving a 15 fF column with a 15 ns CDS gap. CDS-filtered 1/f noise grows only logarithmically with the gap: F = 2[ln(2π·fc·Δt) + γ] ≈ 5.7, which the numerical integral confirms.

| Term (input-referred) | mV |
|---|---|
| SF 1/f (Hooge α 1.5e-3) | 1.34 rms |
| Uncancelled reset kTC on the second (shared) bitline | 1.20 rms |
| Column offset after auto-zero | 1.11 rms |
| SF thermal; WL kickback variation; cell kTC | 0.90; 0.87; 0.43 rms |
| **Random σ** | **2.49**, × 3.72 = **9.3** |
| RTN 1e-4 tail (3 × q/Cox·W·L) | 4.2 |
| Neighbour coupling: raw 8.05; after decision feedback | 1.2 |
| **Readout residual** | **14.7** (21.5 without decision feedback) |

At raw BER 1e-4, including the Cs, Cbl and gain spread and an 8 mV guard band, the allowed residual is **29.5 mV** at 0.45 fF (18.0 at 0.30 fF; 40.2 at 0.60 fF). The modelled residual sets a minimum Cs of 0.20 fF.

PIXEL-STACK needs ~60 e⁻ rms on 3.8 fF, 30-60× worse than a camera pixel (~1-2 e⁻ [UNVERIFIED]).

### 2.3 Retention: the tight constraint

| Term | Arithmetic | Value |
|---|---|---|
| Access-TFT tail Ioff | 1 aA × 10^(3.72 × 30/80) | 24.8 aA |
| Capacitor leakage | 1e-7 A/cm² × 0.0065 µm² | 6.5 aA |
| Tail leakage vs spec | spec = 0.45 fF × 75 mV ÷ 1 s | **31.3 vs 33.8 aA** |
| Tail retention | 0.45 fF × 75 mV ÷ 31.3 aA | **1.08 s** (DDR5 hot: 32 ms) |

**Correction carried.** The concept's 68 aA spec assumed 150 mV of droop, which contradicts its own 0.85 signal factor (that factor implies 75 mV). The consistent spec is **34 aA**.

### 2.4 Comparison with 1-beta DDR5

| Metric | 1-beta DDR5 | PIXEL-STACK, 64 tiers |
|---|---|---|
| Density | 0.447 Gb/mm² (TechInsights via A1) | 2.76 Gb/mm² (6.2×), before tier yield |
| Capacitor / bitline | ~5.4 fF pillar, AR ~60 / ~35 fF | 0.45 fF, 52 nm lateral / 3.0 fF |
| Wafer cost / yield / $/GB | $3,800 / priced in / $1.48 | ~$8,000 / 0.862 / **$0.58 (0.40×)** [ESTIMATE, low confidence] |
| 85 °C tail refresh | 32 ms | 1.08 s; refresh power 17× lower; bank busy 1.24% vs 7.6% |
| tRC | ~46 ns | 55 ns (two bitlines share one SF) |
| Energy per accessed bit | ~46 fJ | **89 fJ (~2× worse)**; SF bias 2 µA × 1.2 V × 16 ns ≈ 38 fJ core |
| EUV / maximum process temperature | DUV/EUV multipatterning / >1,000 °C | none / ≤400 °C |
| Endurance | effectively unlimited | 1e12 shown (measurement-limited) vs 5.8e15 worst case over 10 years |

### 2.5 Sensitivity

**SF noise vs gate area.** The table gives the residual in mV; ≤29.5 passes at 0.45 fF.

| α_H \ W×L (nm) | 50×50 | 100×100 | 150×200 | 300×300 |
|---|---|---|---|---|
| 1e-3 | 29.2 | 14.2 | 10.8 | 9.6 |
| 1e-2 | 44.8 ✗ | 20.5 | 13.4 | 10.6 |
| 1e-1 | 99.7 ✗ | 46.8 ✗ | 27.4 | 17.3 |

Measured α values:
- 1.5e-3 for long-channel a-IGZO ([Fung, JAP 2010](https://web.eecs.umich.edu/omelab/downloads/Fung%20JAP%202010.pdf)).
- ~6e-3 with an Al₂O₃/SiNx gate; Al₂O₃-only gates are 100-1000× noisier ([Cho, EDL 2009](https://scholarworks.bwise.kr/cau/handle/2019.sw.cau/50716)).

**The SF must keep ≥~0.01 µm² of gate area and a SiNx-capped gate.**

**Coupling.** With decision feedback the residual stays ≤16.5 mV up to Cc/C_BL 0.2; without it, 0.2 fails (33.6 mV). Even/odd shielding does not work for 1T1C, because every cell on an opened wordline must be sensed.

**Retention** at Cs 0.45 fF:

| σVt / H ΔVt / J | Retention |
|---|---|
| 20 mV / 0 / 1e-7 | 2.25 s |
| 30 / 20 / 1e-7 | 0.67 s |
| 30 / 0 / 1e-6 | 0.38 s |
| 50 / 0 / 1e-7 | 0.15 s |
| 50 / 50 / 1e-7 | 0.04 s (fail) |

**Measured residual → capacitor → density:**

| Residual (mV) | Cs min (fF) | Cap (nm) | 64-tier Gb/mm² | $/bit vs 1b |
|---|---|---|---|---|
| 10 | 0.20 | 20 | 3.48 (7.8×) | 0.31× |
| 30 | 0.46 | 53 | 2.75 (6.1×) | 0.40× |
| 50 | 0.75 | 92 | 2.21 (5.0×) | 0.49× |
| 70 | 1.08 | 136 | 1.81 (4.0×) | 0.60× |

**Cost.** Over $15-60 per cell tier and $150-600 per amp sub-layer, $/bit runs 0.30-0.62× of 1-beta. One ~$2,000 Smart-Cut layer per group gives 0.67× ($13,600 wafer); at $2,000 per amp sub-layer (two per group) it is 1.03-1.18×. 32-tier groups reach 0.28× at the modelled readout (14.7 mV).

### 2.6 GO/NO-GO threshold

The measured quantity is the post-CDS residual on a planar IGZO pixel-amp array at 85 °C: 3.72σ random noise + 1e-4 RTN tail + worst-pattern coupling. It is measured on 3-3.5 fF nodes read by SFs of ≤0.01 µm².

| Residual | Verdict |
|---|---|
| **≤15 mV** | **GO.** Cs could reach 0.26 fF, leaving ~15 mV for 3D-only effects |
| 15-30 mV | CONDITIONAL GO: 0.45 fF closes with no spare |
| **>30 mV** | **NO-GO as pitched.** At 30-65 mV a fallback remains: Cs ≤1 fF, ~4-6× 1-beta |
| >65 mV | Oxide amp tier dead. Revival is I-11545's Smart-Cut layer, at ~1.7× the $/bit |

Retention gate on the same run: tail leakage ≤34 aA after a 400 °C/H₂ sequence, with ΔVt <20 mV. NO-GO above 101 aA (≈0.33 s).

---

## 3. What is new versus prior art

| Prior art (date) | Has | Lacks |
|---|---|---|
| Samsung 16-tier VS-DRAM, peri-on-cell bonded ([VLSI 2026 tipsheet](https://www.vlsisymposium.org/wp-content/uploads/2026/04/2026-VLSI-Technical-Tipsheet-REVISED-FINAL-NO-IMAGES-4.24.26.docx); [Cnyes](https://hao.cnyes.com/post/269690)) (2026) | Chip-level read/write; Cs grows with capacitor length | The bitline spans the stack, so the capacitor stays long |
| SK hynix 5-tier, 56.1% yield ([Guru3D](https://www.guru3d.com/story/sk-hynix-achieves-yield-in-fivelayer-3d-dram-development)) (VLSI 2024) | Says 32-192 layers are needed | ~0.89 raw yield per tier |
| Kioxia 3D OCTRAM: 8 IGZO tiers at once, Ioff <1 aA ([Kioxia](https://www.kioxia.com/en-jp/about/news/2025/20251212-1.html)) (IEDM 2025) | The closest cell-tier process | No retention data; no in-stack gain |
| Samsung 10a IGZO 4F² VCT ([TrendForce](https://www.trendforce.com/news/2026/04/24/news-samsung-reportedly-produces-sub-10nm-10a-dram-working-die-using-4f-square-and-vct-targets-2028-production/)) (2026) | Incumbents accept IGZO | Planar |
| IBM 3T micro sense amp per ~32 cells ([Barth](https://researcher.ibm.com/publications/a-500-mhz-random-cycle-15-ns-latency-soi-embedded-dram-macro-featuring-a-three-transistor-micro-sense-amplifier)) (ISSCC 2007) | Local gain per short bitline | Built in c-Si; no CDS |
| CEA-Leti 400-500 °C sequential CMOS ([EEJournal](https://www.eejournal.com/industry_news/cea-leti-scientists-demonstrate-cmos-device-fabrication-at-500c-paving-the-way-to-high-performance-3d-monolithic-cmos-integration/); [Electronics World](https://www.electronicsworld.co.uk/3d-sequential-integration-closer-to-commercialisation-thanks-to-cea-leti/874/)) (2020; IEDM 2025) | c-Si layers at low temperature (the I-11545 route) | Needs Smart-Cut donors and implanted H |
| US 12,207,458, hierarchical 3D bitline ([USPTO](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12207458)) | Local/global bitlines with access switches | CMOS sense amp; no in-stack gain, no CDS |
| EP 4567797/798/799 ([797](https://data.epo.org/publication-server/rest/v1.2/patents/EP4567797NWA1/document.html), [798](https://data.epo.org/publication-server/rest/v1.2/patents/EP4567798NWA1/document.html), [799](https://data.epo.org/publication-server/rest/v1.2/patents/EP4567799NWA1/document.html)); US 12,603,114 ([USPTO](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12603114)) | Bitline-select and precharge transistors (≈ SEL/RST) | No follower, no double sampling |
| SEL DOSRAM, IGZO 1T1C over sense amps ([US 10,622,059](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10622059), [US 11,094,373](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11094373), [US 9,368,501](https://patents.google.com/patent/US9368501)) | Oxide cells stacked on sense amps | Si CMOS sense amps |
| De Roose et al., a-IGZO APS imagers ([IISW 2015](https://imagesensors.org/Past%20Workshops/2015%20Workshop/2015%20Papers/5-15_%20De%20Roose%20et%20al.pdf)) (2015) | **Proof that an oxide SF + CDS works** | Display-scale (µm) devices |
| Oxide APS with CDS ([US 11,477,398](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11477398)); SF compensation ([US 10,187,597](https://patents.google.com/patent/US10187597)); oxide pixel on an H-blocking layer ([US 12,615,863](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12615863)) | RST/SEL/SF + CDS in oxide; H barrier | Imagers, not memory |
| Samsung/SK hynix offset-cancelling sense amps [training knowledge] | Offset cancellation in DRAM | c-Si; long bitlines |
| Named by Stage 2 critics: Hitachi charge-transfer pre-sensing; Hi-ECC (ISCA 2010), DDR5 on-die ECC, NAND LDPC soft sensing; Chipkill and NAND RAIN; PragmatIC Flex-RV NMOS-only IGZO (Nature 2024), 1970s NMOS DRAM; M3D DRAM periphery tier (arXiv 2008.11367); skipper CCD, Hitachi PLEDM, Fossum QIS [training knowledge / snippet] | Pre-sense gain; ECC-paid margin; cross-die codes; n-only oxide logic; monolithic periphery tiers; few-electron reads | None reads a bounded 3D bitline through an in-stack oxide SF with CDS |

**The genuine delta.** No source seen combines all four of these:
- a vertical bitline bounded every N tiers;
- read as a floating diffusion by an in-stack oxide RST/SF/SEL tier;
- with CDS;
- with margin budgeted to a raw-BER-1e-4 code.

The new claim is that CDS makes oxide-TFT offset irrelevant, so the bitline-bounding sense layer no longer needs c-Si. That removes Smart-Cut layers, implanted hydrogen and >400 °C steps.

**Honest caveats.**
- The search was six queries, not freedom-to-operate (FTO).
- An examiner could combine the hierarchical-bitline and oxide-APS families against the broad system claim, so the defensible claims are the specific implementations in §6.
- Against A1's *optimistic* 3D case (40 × 300 nm, 6.7× at 64 tiers) there is no density gain. The real delta is reaching that density at a realistic 70 nm pitch with a 52 nm recess. Against A1's base case it is 2.5× density and ~1.5× $/bit before yield.

---

## 4. Show-stoppers and how persistence could get around them

1. **Scaled oxide SF 1/f and RTN.** At 50 × 50 nm the residual is 29-100 mV. Data below ~1 µm² are nearly absent, and scaled ALD IGZO is dominated by interface traps (Lee & Niu, TED 2025, via snippet; [arXiv 2503.12718](https://arxiv.org/pdf/2503.12718)). *Workarounds:*
   - keep the SF gate ≥0.01 µm², with a SiNx cap;
   - use an In₂O₃/IGZO buried bilayer channel;
   - accept Cs 0.6 fF, which allows 40 mV;
   - a [SPECULATIVE] **pillar-gated SF**: the bitline pillar gates an oxide shell in the amp tier, giving large gate area at zero footprint.
2. **Data-dependent coupling.** Raw, it is 8 mV at Cc/C_BL 0.08 and 20 mV at 0.2, and CDS cannot cancel it. *Workarounds:* decision feedback (NAND-style, leaving 15% [ESTIMATE]), plus Samsung's BL shield. The fallback is a two-pass soft read through the RAW-BER controller.
3. **Retention tail.** At σVt 30 mV, 1 s needs an H-induced ΔVt ≤~3 mV (20 mV gives 0.67 s); σVt 20-25 mV tolerates ~20-40 mV; at σVt 50 mV retention is 0.15 s. *Workarounds:*
   - negative wordline hold;
   - In-poor or Ga-free access channel;
   - Cs 0.6 fF;
   - per-node refresh binning, with the in-stack SF as a zeptoamp leakage meter.
   Even 0.15 s is ~5× DDR5. **Missing 1 s costs the refresh claim, not the density claim.**
4. **Hydrogen/thermal accumulation.** Group 1 absorbs every later group's budget. Standard and In-poor IGZO drift in opposite directions, and an H+O anneal cuts H doping ~30× ([imec IEDM 2025](https://imec-publications.be/handle/20.500.12860/59908)). *Workarounds:*
   - Al₂O₃/SiNx barriers per group;
   - H-lean ALD molds;
   - Vt pre-compensation of the bottom groups;
   - an In₂O₃ channel, which survives 600 °C ([Purdue EDL 2024](https://engineering.purdue.edu/~yep/Papers/EDL_2024_In2O3%20600C_Lin.pdf)).
5. **Amp-tier area.** Each bitline needs 0.034 µm² but has 0.022 µm² available, so each group needs **two amp sub-layers** (~4 masks each), not the concept's "3-5 masks". *Workarounds:* sharing one SF among 4 bitlines (tRC 106 ns) or 8 (one sub-layer, but 210 ns), or the pillar-gated SF.
6. **Capacitor dielectric at EOT 0.50 nm and ≤400 °C.** At J 1e-6 A/cm², retention is 0.38 s. *Workarounds:* relax EOT to ~0.7 nm, which gives a ~75 nm capacitor [ESTIMATE]; laser anneal; ZrO₂/HZO morphotropic-phase-boundary stacks (k ~56-62, B2 log).
7. **Tier yield.** 64 tiers need ≥0.998 per tier after repair, against the ~0.89 raw implied by SK hynix. Every 3D DRAM shares this. *Workarounds:* each 16-tier group is a natural repair and fuse boundary; spare tiers; tier-orthogonal codes. **Critic correction:** WL-WL shorts are not confined to one tier, and a vertical-bitline array cannot read 32 tiers in one activation, so codes must interleave across activations.
8. **Endurance.** 1e12 cycles at 95 °C has been shown ([imec EDL 2025](https://imec-publications.be/entities/publication/948b2190-065d-48d2-a9b9-4f4ecd22c234)), against a pathological worst case of 5.8e15. CDS tolerates ~150 mV of SF drift. *Workarounds:* test to 1e14 accelerated; refresh-management (RFM) activation limits bound the worst case.
9. **Bitline capacitance per tier (0.15 fF assumed).** Each extra 0.05 fF costs ~10% of the signal. *Workaround:* field-solver extraction in Q1, then measure on the 4-tier stack.

---

## 5. The decisive experiment

**Principle.** A planar "imager without photodiodes": 64 × 64 nodes per die on ≥16 dies (65,536 nodes) observes the 1e-4 tail directly (~6 events per corner).

**Steps.**
1. **M0-3: design.** Calibrate the noise model and build ngspice/Xyce decks. Coupon contents:
   - SF area ladder from 50 × 50 to 1000 × 1000 nm;
   - 2/3/4 fF ZrO₂ MIM bitline emulators, with Cs emulated from 0.2 to 1.0 fF;
   - aggressor lines at Cc/C_BL 0-0.2, plus dummy wordlines;
   - an In-rich depletion SF split, and In-poor or Ga-free In₂O₃/ITZO access splits.
2. **M2-10: 2-3 planar lots** at Purdue Birck or Georgia Tech IEN: TiN/W gate, ALD HfO₂/Al₂O₃ + SiNx, 8-10 nm ALD IGZO/In₂O₃, ZrO₂/TiN MIM, two metal levels.
3. **Noise.** Measure PSD (1 Hz-10 MHz) and RTN at 25/55/85 °C with an FPGA, a 16-bit ADC and a low-noise front end. Compute the 15 ns CDS residual from the measured PSD (F depends only logarithmically on the gap). Then read through the MARGIN STACK MPW column.
4. **Residual.** Run 65k nodes under checkerboard, all-0, all-1 and walking-1 aggressors, with decision feedback in software.
5. **Retention.** Use the pixel amp as the meter: 1 mV in 1,000 s on 3 fF ≈ 3e-21 A, so no electrometer is needed.
6. **H/400 °C splits.** As-built, N₂, forming gas and H-rich PECVD SiN, each ± an ALD Al₂O₃ barrier. Re-measure ΔVt, Ioff tail, noise and residual, with SIMS H profiles.
7. **M6-12: lateral-capacitor coupons.** 2-4-tier stacks with 30-60 nm recesses filled with TiN/ZrO₂/TiN by ALD at Argonne CNM. Measure C and J at 25-85 °C, before and after 400 °C.
8. **M9: seed GO/NO-GO** per §2.6.
9. **M9-21: raise milestone.** A 4-tier oxide 1T1C (Kioxia-style replacement or deposited channel) with a vertical bitline, 30-60 nm capacitors and one amp tier, plus hammer and WL-WL disturb tests.

**Facilities.**
- Purdue Birck: P. Ye group, ALD In₂O₃ and vertical all-oxide TFTs ([VLSI 2024](https://engineering.purdue.edu/~yep/Papers/VLSI2024%20T4-1_Zehao%20Lin.pdf)).
- Georgia Tech IEN: S. Yu, A. Khan and S. Datta, oxide BEOL gain cells ([GT](https://shimeng.ece.gatech.edu/?p=916)).
- Argonne CNM, by proposal.
- Backup fabs: Notre Dame ([$124/h external](https://nanofabrication.nd.edu/facility-access/fees/)) and Penn ([$70/h industry](https://nano.upenn.edu/?p=7074)).
- Rates for Birck, IEN and SNF were not found. The plan uses $110-150/h (cf. [TAMU $150/h](https://aggiefab.tamu.edu/fees), [KU](https://nanofab.ku.edu/rates-fees), [UW e-beam $495/h](https://www.wnf.washington.edu/docs/WNF-Rates.pdf)).
- CDS column chip: the shared 22FDX MPW. Backups are ChipFoundry sky130 at SkyWater ([note](https://tinytapeout.com/news/chipfoundry-sponsor/)), wafer.space GF180 ([~$7k per 1,000 ICs](https://www.crowdsupply.com/wafer-space/gf180mcu-run-3)) or MOSIS 2.0 ([ISI](https://www.isi.edu/news/80945/mosis-2-0-revives-a-legacy-rehan-kapadia-outlines-a-bold-future-for-rapid-microelectronics-prototyping/)).

**Budget (standalone, ≤$1M).**

| Line | $k |
|---|---|
| Modelling, SPICE/TCAD | 15 |
| Planar coupons: 3 lots × ~400 h × ~$120/h, e-beam, precursors | 150 |
| Readout boards, CDS column die, packaging | 30 |
| Test set (used SMU, low-noise preamp, analyser, hot chuck, probe cards) | 80 |
| H/400 °C splits, SIMS, anneals | 25 |
| Lateral-capacitor coupons (CNM; no-fee status [UNVERIFIED]) | 20 |
| 4-tier stack + amp tier: 3 lots, ~1,800 h | 330 |
| Sponsored student/postdoc, ~12 months | 120 |
| IP: 2 provisionals → PCT + US, FTO search | 45 |
| Lean founder stipends | 150 |
| Contingency (~4%) | 35 |
| **Total** (≈$300k spent by M9) | **1,000** |

Lines are ESTIMATEs at cited rates. $150k cannot pay two founders for two years; standalone assumes subsidised founders. Inside the portfolio seed, where the shared ~$275k MPW reads every coupon, PIXEL-STACK's incremental cost is ~$150k (planar) + ~$500k (4-tier).

**Timeline.**

| Months | 0-3 | 2-6 | 5-9 | **9** | 6-12 | 9-18 | 18-21 | 21-24 |
|---|---|---|---|---|---|---|---|---|
| Work | Design, provisionals | Lot 1 noise | Lot 2: residual, retention, H | **GO/NO-GO** | Capacitor coupons | 4-tier lots | Integrated test | Data room, raise |

**Pass/fail numbers, set in advance.**
- **M9.** Residual ≤15 mV is GO; 15-30 mV is conditional; >30 mV is NO-GO. Leakage must be ≤34 aA after 400 °C/H₂ with ΔVt <20 mV; >101 aA is NO-GO.
- **M12.** The capacitor must reach ≥60 fF/µm² with J ≤1e-7 A/cm² at 0.5 V after 400 °C; it fails at ≥1e-6.
- **M21.**
  - Signal ≥50 mV at Cs ≤0.5 fF (the concept said 55; corrected in §2.1).
  - Residual ≤15 mV.
  - Retention ≥1 s at 85 °C at the 1e-4 tail over ≥1e4 cells.
  - Bottom-tier ΔVt <20 mV after the amp tier is built.

---

## 6. The $1M, 24-month plan

**Quarterly gates** (M0 = funding close, assumed 2027-01-04).

| Quarter | Milestone | Gate |
|---|---|---|
| Q1 | Noise model, coupon tape-out, field-solver C_BL, 2 provisionals | G0: C_BL ≤0.20 fF/tier |
| Q2 | Lot 1: SF PSD/RTN vs area, 25-85 °C | G1: α_H ≤1e-2 at ≤0.01 µm² |
| Q3 | Lot 2: 65k residual, retention, H splits, MPW read | **G2: seed GO/NO-GO** |
| Q4 | Capacitor coupons; 4-tier masks; pillar-gated SF structure | G3: ≥60 fF/µm², J ≤1e-7 |
| Q5 | 4-tier lot 1 (cells only) | G4: signal ≥45 mV at ≤0.5 fF |
| Q6 | 4-tier lot 2 with amp tier | G5: amp tier works on the stack |
| Q7 | Retention, hammer, H accumulation on ≥1e4 cells | **G6: raise milestone** |
| Q8 | PCT/US filings, FTO, data room | Raise |

**Allocation.** Experiments $770k: ~$300k planar by M9 (modelling, coupons, readout, test set, H splits), $330k 4-tier, $20k capacitor coupons, $120k sponsored researcher. Founders $150k. IP $45k. Contingency $35k. Total $1,000k.

**Team.**
- **Founder A, device/process.** Recruit from Purdue (Ye), Georgia Tech (Datta, Khan, Yu), Stanford, or the Kioxia, Samsung, SK hynix or Micron 3D DRAM programs.
- **Founder B, circuits (CIS CDS readout plus DRAM sensing).** Recruit from Sony Semiconductor, OmniVision, onsemi, Gigajot or Micron sense-amp design.
- **Advisors.** Eric Fossum, Dartmouth: QIS read noise 0.21 e⁻ ([Laser Focus World](https://www.laserfocusworld.com/test-measurement/research/article/16555293/advances-in-detectors-the-quanta-image-sensor-qis-making-every-photon-count)); availability UNVERIFIED. The De Roose oxide-APS group (KU Leuven/imec, UNVERIFIED). A scaled-oxide noise specialist (Lee & Niu).

**IP: file provisionals by M3, before any publication.**
1. System claim: vertical bitlines bounded every N tiers by an in-stack oxide RST/SF/SEL tier, with the SF gate on the bitline node and a CDS read. Dependents: N = 8-32; Cs ≤1 fF.
2. The pillar-gated SF [SPECULATIVE].
3. Decision-feedback coupling compensation in CDS-read DRAM.
4. Pixel-style bitline sharing with restore through RST/TG.
5. A dual-composition oxide stack with an Al₂O₃/SiNx H barrier between groups.
6. The in-stack SF as a leakage monitor for per-node refresh binning.

**FTO risks:**
- hierarchical 3D bitlines: US 12,207,458; US 12,603,114; EP 4567797-799; US 12,010,831, probably Micron [inference]; [US 11,600,309](https://patents.justia.com/patent/11600309); [US 11,443,780](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11443780);
- SEL DOSRAM;
- oxide-APS CDS patents, including US 12,615,863 (H barrier);
- offset-cancelling sense amp (OCSA) patents;
- Monolithic 3D Inc. ion-cut patents [training knowledge].

A professional FTO search precedes the raise.

---

## 7. After the demo: scale path

**Partners and licensees.**
- **Kioxia + Nanya:** the likeliest first partner. OCTRAM already makes 8 IGZO tiers at once, and PIXEL-STACK adds the bitline-bounding sense layer.
- **Samsung:** VS-DRAM and IGZO VCT, with 3D from "10d" (~2030). PIXEL-STACK offers a shorter capacitor and one fewer bonded layer.
- **SK hynix:** says 32-192 layers are needed; PIXEL-STACK pulls break-even to ~10 tiers.
- **Micron:** the U.S. home. Its vertical-digit-line patents probably make a cross-license necessary.
- **Foundries:** GlobalFoundries and SkyWater for CDS and periphery wafers, or CELL-WAFER FOUNDRY's fab-lite route.
- **Display makers:** Sharp/SEL, LG Display and Samsung Display bring oxide-TFT reliability and hydrogen know-how. SEL is also an IP counterparty.

**What a raise buys.**
- **$10M:** a 300 mm 16-tier group plus amp tier at NY CREATES Albany ([NSTC NY](https://www.ny.gov/roadmap-national-semiconductor-technology-center-new-york); [JDA model](https://nachrichten.idw-online.de/2025/05/16/ny-creates-and-fraunhofer-ipms-announce-joint-development-agreement-to-advance-memory-devices-at-300mm-wafer-scale)), a ~1 Mb test chip, 1,000 h at 85-105 °C, and endurance to 1e14.
- **$25-50M:** 32 tiers, tier-yield learning with group repair, a 1-4 Gb demonstrator behind a RAW-BER CONTRACT CXL controller, and a joint development agreement (JDA).

**Standards.** CXL attach under an "ECC-native" raw-BER grade (RAW-BER CONTRACT, then JEDEC); DDR/HBM compatibility later via logic base dies.

---

## 8. Resources and America

- **EUV: none.** Density comes from tiers, and each amp sub-layer is ~4 DUV masks. An EUV scanner draws up to ~10 GWh/yr ([TechInsights](https://www.techinsights.com/blog/euv-lithography-power-hungry-path-innovation)).
- **Gallium.** In/Ga is <0.4% by A2's inventory. But Ga is ~98% Chinese [UNVERIFIED], and the U.S. ban suspension expires **2026-11-27** ([Fastmarkets](https://fastmarkets.com/insights/china-suspends-export-prohibition-on-superhard-materials-us)). Qualify Ga-free In₂O₃/ITZO in the Stage B splits.
- **Hafnium/zirconium** (gate dielectric and capacitor). Overseas Hf was up ~140% to ~$13k/kg by 2026-04 ([SMM](https://news.metal.com/newscontent/103938701-from-stability-to-surge-the-overseas-hafnium-market-caught-between-ai-demand-and-supply-controls)). Film masses are tiny, so this is a security risk, not a cost driver.
- **Tungsten** (wordlines). China has ~80% of supply ([Oregon Group](https://theoregongroup.com/commodities/tungsten/why-tungsten-prices-are-rising-so-fast-inside-the-supply-crunch/)). Mo or Ru wordlines are the hedge.
- **Germanium: none.** There is no Si/SiGe superlattice, unlike imec's 120-bilayer route ([technews](https://technews.tw/2025/08/25/3d-dram-120-layers/)).
- **PFAS.** One ~24:1 bitline hole per group, against AR ~60 pillars. Fluorocarbon etch remains, but it is shallower.
- **Energy and water** [ESTIMATE, scaled by the 0.40× $/bit ratio]. ~0.17 kWh/GB and ~1 L/GB, against 1-beta's 0.42 kWh/GB and 2.6 L/GB (A2). An ALD-heavy stack could raise kWh per wafer faster than cost, and this has not been measured.
- **U.S. manufacturability.**
  - Stage B-C runs entirely at U.S. facilities.
  - The CDS column can be made at SkyWater in Minnesota. The shared 22FDX MPW is fabricated in Dresden, and wafer.space is in Singapore.
  - Scale-up goes to Albany.
  - A ≤400 °C, EUV-free oxide stack suits BEOL-class U.S. lines and Micron's U.S. fabs [inference].

---

## 9. Kill criteria (M0 = 2027-01-04; physics only, each with a revival condition)

1. **2027-09-30.** Best-split residual >**30 mV** at 85 °C (≤0.01 µm² SFs, 65k nodes): kill the 0.45 fF/52 nm claim and fall back to ≤1 fF. Above **65 mV**: kill the oxide amp tier. *Revival:* α_H ≤1e-2 at ≤0.01 µm², or a working pillar-gated SF.
2. **2027-09-30.** Tail leakage >**101 aA** after 400 °C/H₂, or H ΔVt ≥**50 mV** with the best barrier: kill ≥0.3 s retention at 0.45 fF. *Revival:* a Ga-free or In-poor channel with σVt ≤30 mV and ΔVt ≤20 mV.
3. **2027-09-30.** Coupling after decision feedback >**15 mV**: kill 16-tier groups at 0.45 fF. *Revival:* a shield or air gap giving Cc/C_BL ≤0.1.
4. **2027-12-31.** No 30-60 nm capacitor reaches ≥**40 fF/µm²** with J ≤1e-6 after 400 °C: kill the short capacitor. *Revival:* a ≤400 °C high-k at EOT ≤0.7 nm with J ≤1e-7.
5. **2028-06-30.** 4-tier signal <**35 mV** at Cs ≤0.5 fF: move to 8-tier groups (3.74 Gb/mm², 0.51× $/bit). *Revival:* C_BL ≤0.15 fF per tier.
6. **2028-09-30.** Bottom-tier ΔVt >**50 mV** after an amp tier is built, or tail retention <**0.06 s**: kill multi-group stacking as built. *Revival:* barriers holding ≤20 mV through two group budgets.
7. **2028-12-31.** SF Vt drift >**150 mV** (the CDS headroom) after 1e12 reads at 85 °C: kill the oxide amp tier for DRAM endurance. *Revival:* a drift-tracking auto-zero, or a lower-PBTI composition.

---

## 10. Sources

All of these URLs are logged in `research/sources/*.jsonl`, mostly in `dos-pixel-stack.jsonl`. Log items marked "via search snippet" were not opened in full.

- Fung, a-IGZO 1/f, JAP 2010: https://web.eecs.umich.edu/omelab/downloads/Fung%20JAP%202010.pdf
- Cho, IGZO noise vs gate stack, EDL 2009: https://scholarworks.bwise.kr/cau/handle/2019.sw.cau/50716
- Deep states in ALD IGZO: https://arxiv.org/pdf/2503.12718
- De Roose, IGZO APS, IISW 2015: https://imagesensors.org/Past%20Workshops/2015%20Workshop/2015%20Papers/5-15_%20De%20Roose%20et%20al.pdf
- US 11,477,398: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11477398
- US 12,615,863: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12615863
- US 10,187,597: https://patents.google.com/patent/US10187597
- US 12,207,458: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12207458
- US 12,603,114: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12603114
- EP 4567797: https://data.epo.org/publication-server/rest/v1.2/patents/EP4567797NWA1/document.html
- EP 4567798: https://data.epo.org/publication-server/rest/v1.2/patents/EP4567798NWA1/document.html
- EP 4567799: https://data.epo.org/publication-server/rest/v1.2/patents/EP4567799NWA1/document.html
- US 11,600,309: https://patents.justia.com/patent/11600309
- US 12,010,831: https://patents.google.com/patent/US12010831
- US 11,443,780: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11443780
- SEL US 10,622,059: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10622059
- SEL US 11,094,373: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11094373
- US 9,368,501: https://patents.google.com/patent/US9368501
- IBM 3T micro sense amp: https://researcher.ibm.com/publications/a-500-mhz-random-cycle-15-ns-latency-soi-embedded-dram-macro-featuring-a-three-transistor-micro-sense-amplifier
- Kioxia 3D OCTRAM: https://www.kioxia.com/en-jp/about/news/2025/20251212-1.html
- VLSI 2026 tipsheet: https://www.vlsisymposium.org/wp-content/uploads/2026/04/2026-VLSI-Technical-Tipsheet-REVISED-FINAL-NO-IMAGES-4.24.26.docx
- Samsung VS-DRAM Cs vs length: https://hao.cnyes.com/post/269690
- SemiEngineering 3D DRAM: https://semiengineering.com/baby-steps-towards-3d-dram/
- Samsung 10a IGZO VCT: https://www.trendforce.com/news/2026/04/24/news-samsung-reportedly-produces-sub-10nm-10a-dram-working-die-using-4f-square-and-vct-targets-2028-production/
- SK hynix 5-tier yield: https://www.guru3d.com/story/sk-hynix-achieves-yield-in-fivelayer-3d-dram-development
- IMECAS 4-tier 2T0C: https://www.ithome.com/0/966/543.htm
- imec 2T0C, EDL 2025: https://imec-publications.be/entities/publication/948b2190-065d-48d2-a9b9-4f4ecd22c234
- imec PBTI/H, IEDM 2025: https://imec-publications.be/handle/20.500.12860/59908
- Purdue In₂O₃ 600 °C: https://engineering.purdue.edu/~yep/Papers/EDL_2024_In2O3%20600C_Lin.pdf
- Purdue vertical oxide TFTs: https://engineering.purdue.edu/~yep/Papers/VLSI2024%20T4-1_Zehao%20Lin.pdf
- CEA-Leti 500 °C: https://www.eejournal.com/industry_news/cea-leti-scientists-demonstrate-cmos-device-fabrication-at-500c-paving-the-way-to-high-performance-3d-monolithic-cmos-integration/
- CEA-Leti 400 °C, IEDM 2025: https://www.electronicsworld.co.uk/3d-sequential-integration-closer-to-commercialisation-thanks-to-cea-leti/874/
- imec 120 bilayers: https://technews.tw/2025/08/25/3d-dram-120-layers/
- Georgia Tech Yu group: https://shimeng.ece.gatech.edu/?p=916
- Fossum QIS: https://www.laserfocusworld.com/test-measurement/research/article/16555293/advances-in-detectors-the-quanta-image-sensor-qis-making-every-photon-count
- Fab rates: https://nanofabrication.nd.edu/facility-access/fees/ ; https://nano.upenn.edu/?p=7074 ; https://aggiefab.tamu.edu/fees ; https://nanofab.ku.edu/rates-fees ; https://www.wnf.washington.edu/docs/WNF-Rates.pdf
- MPW routes: https://www.crowdsupply.com/wafer-space/gf180mcu-run-3 ; https://tinytapeout.com/news/chipfoundry-sponsor/ ; https://www.isi.edu/news/80945/mosis-2-0-revives-a-legacy-rehan-kapadia-outlines-a-bold-future-for-rapid-microelectronics-prototyping/
- Albany: https://www.ny.gov/roadmap-national-semiconductor-technology-center-new-york ; https://nachrichten.idw-online.de/2025/05/16/ny-creates-and-fraunhofer-ipms-announce-joint-development-agreement-to-advance-memory-devices-at-300mm-wafer-scale
- Resources: https://fastmarkets.com/insights/china-suspends-export-prohibition-on-superhard-materials-us ; https://news.metal.com/newscontent/103938701-from-stability-to-surge-the-overseas-hafnium-market-caught-between-ai-demand-and-supply-controls ; https://theoregongroup.com/commodities/tungsten/why-tungsten-prices-are-rising-so-fast-inside-the-supply-crunch/ ; https://www.techinsights.com/blog/euv-lithography-power-hungry-path-innovation

Internal sources:
- `phaseA/A1_scaling_limits.md`: 1-beta 0.447 Gb/mm², 3D scenarios, tier yield.
- `phaseA/A2_materials_resources.md`: In/Ga inventory, energy, water.
- `ideas10k/stage2/stage2_results.jsonl`: critic corrections for I-11545, I-02936, I-05218 and I-00729.
- `research/stage3/FINAL_CONCEPTS.md`.
