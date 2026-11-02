# CELL-WAFER FOUNDRY

*Stage-3 technical dossier · slug `cell-wafer-foundry` · agent `dosw-cell-wafer-foundry` · 2026-11-02*
*Revised after red team 2026-11-02 (owner response `resp-cell-wafer-foundry`): see §11. Sections 0, 2, 5 and 9 carry revised blocks; the pre-red-team text is kept below each for traceability. FINAL STATUS: DOWNGRADED.*
*Inputs: `research/stage3/FINAL_CONCEPTS.json`/`.md`, `research/stage3/cell-wafer-foundry_notes.md`, `models/cell-wafer-foundry.py` (re-run 2026-11-02, exit 0, output identical to `research/stage3/cell-wafer-foundry_model_output.md`), `research/assumptions/dos-cell-wafer-foundry.md`, `MISSION.md`. Tags: [REPORTED] = logged source; [ESTIMATE] = model arithmetic; [SPECULATIVE] = first-principles guess; [UNVERIFIED-training] = from training knowledge, not checked in this project.*

---

## 0. Header

**Name.** CELL-WAFER FOUNDRY: litho-light periodic oxide cell wafers bonded to U.S. foundry periphery under an open bitline-group bond spec.

**One-line thesis.** Split the DRAM die at the bitline-group bond. A purely periodic, multi-tier oxide cell wafer is made with no EUV on NAND-class deposition and etch tools. It is hybrid-bonded at ~1.5 µm pitch to a sense/decode wafer from an existing logic foundry, and the interface is published so either half can come from anyone.

**Rank / category / score.** Rank 9 of 10, integration/manufacturing. EV 36 = S3 × P3 × D4.

**Constituent ideas and creativity-technique lineage**

| Id | Contribution | Technique (cell / lens) |
|---|---|---|
| I-04714 | Open array-to-periphery bond standard for merchant cell wafers (the core) | Assumption inversion (T11, sensing and periphery) |
| I-07130 | Interference lithography plus coarse cuts for purely periodic layers | Reverse brainstorming (T16, manufacturing) |
| I-00729 | Tier-orthogonal codewords against tier-yield compounding | SCAMPER-Combine (T02, manufacturing) |
| I-02936 | All-oxide n-only periphery; here cut back to a TFT predecode layer | TRIZ #33 Homogeneity (T07, array architecture) |
| I-11545 | Sense layers inside the stack (the in-stack alternative the bond replaces) | Phase B lens B3 (B3-09) |
| I-05632 | Open, silicon-proven periphery IP commons | Random stimulus / forced connection (T13) |
| I-00869 | Open-PDK shuttle CMOS plus university BEOL cell post-processing | SCAMPER-Combine (T02, reliability) |
| N-31 | NIL-only periodic cell wafer (triage: KNOWN+TWIST, ALIVE) | Phase B lens B2 (B2-12) |
| N-36 | BEOL-only cell mini-line on reusable glass carriers (triage: NEW, ALIVE) | Phase B lens B2 (B2-17) |

Merge: device-lens CELL-WAFER FOUNDRY (bond pitch, yield, daisy-chain test) plus system-lens Merchant Cell Wafer (open interface, planar mux route); its chokepoint recipe moved to LEAN ARRAY MODULE.

**Verdicts (revised after red team; see §11)**

- **PHYSICALLY POSSIBLE? Yes (unchanged).** No physics is violated. The red team added two device risks that must be measured, not argued: hydrogen from the oxide bond plane reaching top-tier oxide channels and TFTs (the barrier stack must attenuate ~1,400–3,500×; one ALD Al₂O₃ layer has shown ~18×), and an n-only oxide sub-word-line driver that must hold its levels while its Vt drifts.
- **STEP CHANGE IF IT WORKS? Yes, but about half the original factor, and mostly inherited from the cell's tiers.** For 1T1C-64 with D2W: 3.6× less new memory-fab capex per GB/month ($61 → $17.1; was 7.6×), $/GB 0.62× DDR5 ($0.92; was 0.36×), density 3.6× 1β (was 4.5×), and 0 EUV layers (unchanged). The gain-cell variant gives 5.9× capex, 0.38× $/GB and 5.8× density. Only ~1.5× of the capex factor comes from the split itself, and only while existing 28 nm logic capacity absorbs the periphery.
- **PROVABLE WITH $1M IN 24 MONTHS? Partly (unchanged), with a narrower claim.** Run standalone, $795k of experiments plus $200k founder pay ($995k in all) settles bond physics, bond-plane hydrogen, the oxide WL driver and group select, on 4- and 8-tier coupons bonded D2W at a fab-grade partner by M22. It cannot settle a 64-tier cell, the deck-driven cell-wafer cost, or merchant economics. Inside the portfolio seed only ~$60k is funded, so the answer there is **No**, unless a bonding partner contributes in kind.
- **FINAL STATUS: DOWNGRADED.** The concept lives as the bond and integration scale path for whichever portfolio cell passes.

**Original verdicts (pre-red-team, kept for the record)**

- **PHYSICALLY POSSIBLE? Yes.** No physics is violated. W2W hybrid bonding already runs 70,866-link daisy chains at 1.08 µm in research and ships at 6–10 µm in production. The open questions (bow, overlay, bridges, voids and anneal drift on warped oxide stacks) are engineering.
- **STEP CHANGE IF IT WORKS? Yes, conditionally, on capital intensity, EUV and U.S. manufacturability.** Versus 1β DDR5: 0 EUV layers against 5–7, ~7.6× less new memory-fab capex per GB/month ($61 → $8), array efficiency 0.51 → 0.86, and $/GB at 0.36× [ESTIMATE]. All of this assumes a portfolio cell reaches 64 tiers, and most of the factor comes from the tiers rather than the split.
- **PROVABLE WITH $1M IN 24 MONTHS? Partly.** About $700k of experiments settles the bond physics on 4- and 8-tier warped oxide coupons. It cannot settle whether a cell reaches 64 tiers, or whether the merchant split beats monolithic CMOS-under-array.

---

## 1. How it works

A DRAM chip has two parts: a huge grid of storage cells (the shelves) and the circuitry that finds, reads and refreshes them (the forklifts). Today both are built on one wafer in one fab, each with tools chosen for the other, and the circuitry takes about **49% of the die** (array efficiency ~0.51).

CELL-WAFER FOUNDRY separates the two parts:

1. A **cell wafer** carries only shelves, stacked 16–128 floors high like 3D NAND, with oxide-semiconductor transistors (IGZO or In₂O₃) and relaxed 40 nm features: deposition and etch tools, no EUV. Because it holds only repeating patterns, interference lithography or nanoimprint become optional.
2. A **periphery wafer** carries sense amplifiers, word-line drivers, decoders and I/O: ordinary 22/28 nm logic, no EUV.
3. The wafers are pressed face to face (**hybrid bonding**); millions of copper pads fuse, and so does the oxide between them.
4. The trick: in a vertical-bitline stack one pad serves a **group of ~150 bitlines** through switches on the cell wafer, so pads sit 1.5 µm apart, not 0.08 µm.
5. The pad grid, voltages and capacitance window are published as an **open bond spec**, so a cell-wafer maker and a logic foundry can each make half a memory die.

```
 CELL WAFER  (NAND-class dep/etch tools, F ~40 nm, no EUV, <=400 C)
 +----------------------------------------------------------------+
 | tier 64   ==o====o====o====o==   o = oxide memory cell          |
 |   ...       |    |    |    |      == word line (one per tier)   |
 | tier 1    ==o====o====o====o==    |  vertical bitline, 80 nm pitch|
 |            [ group select: ~146 bitlines -> 1 pad ]             |
 |            [ oxide-TFT word-line predecode, 1 pad per 8 WLs ]   |
 |                 [Cu]     [Cu]     [Cu]   pads at 1.5 um pitch    |
 +=================||=======||=======||============================+ <- hybrid bond
 |                 [Cu]     [Cu]     [Cu]   (Cu-Cu + SiCN/oxide)    |
 |      [sense amp ~2.5 um2] [3 V WL driver] [decode] [I/O, pumps] |
 | PERIPHERY WAFER  (22/28 nm logic foundry, no EUV)                |
 +----------------------------------------------------------------+
```

---

## 2. The physics and the numbers

All figures come from `models/cell-wafer-foundry.py`, base case **1T1C, 64 tiers, F ~40 nm, 1.5 µm bonds, 32 Gb die**.

**Revised numbers (revised after red team).** The model now carries a `RED_TEAM_REVISIONS` block and an output §10. `--original` reproduces the numbers below the table. Ten input changes were made:
- ECC parity 6.25% → 15.6%, because the 26 mV threshold is only valid with that parity (CIRC-02).
- Global-line coupling is now modelled: α 0.145 unshielded, 0.035 with shielding on two metal levels (CIRC-02).
- SA area 2.5 → 4.0 µm² (CIRC-03).
- $800 per deck, with decks limited to AR 60, giving 2 decks at 64 tiers (PROC-02).
- +$200 per cell wafer for shield metal, a sub-WL-driver TFT plane and a hydrogen-barrier stack (CIRC-01/02, DEV-01/03).
- Bond cost $400 → $500 for a contamination-qualified line (PROC-03).
- D2W adder $300 → $600, priced by throughput (PROC-01).
- Pre-bond screening of cell dies catches 50% of bad dies, not 100% (owner correction).
- DBI royalty: 1% of pair cost (IND-05).
- The primary bond mode is now D2W (PROC-01).

| Quantity (1T1C-64) | Original | Revised | Gain-64 revised |
|---|---|---|---|
| M / Cbl / Cs | 146 / 19.9 fF / 1.16 fF | 196 / 25.8 fF / 1.62 fF | 328 / 20.5 fF / — |
| Required raw signal | 26 mV | 28.0 mV (α 0.035) | 100 mV current-mode |
| Density | 2.01 Gb/mm² (4.5×) | **1.60 Gb/mm² (3.6×)** | 2.60 (5.8×) |
| Cell wafer / pair | $2,620 / $5,820 | $4,420 / $7,797 | same |
| $/GB | $0.54 W2W (0.36×) | **$0.92 D2W (0.62×)**; $0.91 W2W | $0.56 (0.38×) |
| Cost break-even vs 1β | 16 tiers | 28 tiers | 16 tiers |
| New memory-fab capex | $8.0 per GB/month (7.6×) | **$17.1 (3.6×)** | $10.4 (5.9×) |
| Bitline energy | 11.0 fJ (1.8×) | 14.2 fJ (1.4×) | 11.3 fJ (1.7×) |
| Split premium over monolithic CuA, 64 tiers | $800, ≥$12.5/tier | $977, ≥$15.3/tier (W2W); ≥$21.4/tier (D2W net of KGD) | — |
| EUV layers | 0 | 0 | 0 |

**Cumulative effect on $/GB (W2W):**

| Step | $/GB |
|---|---|
| Original | $0.54 |
| + ECC parity | $0.59 |
| + coupling, shielded | $0.60 (unshielded would be $0.65) |
| + SA 4 µm² | $0.68 |
| + decks | $0.87 |
| + adders, bond cost and royalty | $0.91 |

The deck cost is the largest single correction.

**Bond pitch.** With a 4 µm² SA the group is SA-limited up to 2.0 µm, so the spec moves to **2.0 µm pitch at no density or cost penalty**. That gives a 0.50 µm overlay budget. D2W die-level run-out is 0.038 µm plus 0.10 µm (3σ) placement, a 3.6× margin.

**Capex attribution.** Of the 3.6× capex factor, 3.3× is good GB per wafer, which comes from tier density. A monolithic in-house 3D DRAM would need ~$26.4 per GB/month (2.3× less than DDR5), so the split's own share is ~1.5×. The original text below is the pre-red-team analysis and is kept for traceability.

**Bond grid.** One bond per bitline group. The group size M is set by sense-amp area, not bond pitch. A ~2.5 µm² 28 nm sense amp needs 2.5 ÷ (0.0258 µm² footprint × 0.66) ≈ 146 bitlines of array above it, where 0.66 is the 85% periphery fill less ~19% for 3 V word-line drivers. The bond pitch alone would allow M = 101 at 1.5 µm and 41 at 1.0 µm. **So bonding finer than ~1.5 µm buys nothing until the periphery node shrinks.** Bond pitch becomes the limit only at ≥2 µm.

**Bitline and cell.** Cbl = 0.43 fF (pad+via) + 7.1 fF (a 47 µm global line spanning M rows) + 5.8 fF (off selectors) + 5.1 fF (64 tiers × 0.08 fF) + SA input ≈ **19.9 fF**. With MARGIN STACK's 26 mV threshold and a 474 mV cell swing, Cs = 26 × 19.9 / (474 − 26) = **1.16 fF**, a 123 nm lateral capacitor. At a conventional 50 mV threshold Cs = 2.11 fF.

**Density.** Footprint 80 × 323 nm = 0.0258 µm² per cell per tier. With 8% staircase and 8% edge/TFT overhead, the 32 Gb die is 15.9 mm². Array efficiency is **0.86**, and density is 32 / 15.9 = **2.01 Gb/mm² = 4.5× 1β** (0.447). A non-destructive gain cell can cluster any M bitlines under one pad (Cbl 15.5 fF, read 0.78 ns to 100 mV at 2 µA), giving **2.60 Gb/mm² (5.8×)**.

**Energy.** Bitline energy is ½·Cbl·V² = ½ × 19.9 fF × 1.05² = **11.0 fJ** per sensed bit, against 19.3 fJ for 1β (1.8× lower; 2.3× for gain cells).

**Cost.** Wafer pair = $700 cell base + 64 × $30 per tier + $2,800 periphery + $400 bond/thin = **$5,820**. Yield = 0.998⁶⁴ tiers (0.880) × periphery (0.992) × voids (0.965) = 0.842. That gives 10,804 good GB per pair, so $5,820 / 10,804 = **$0.54/GB, 0.36× DDR5's $1.48** ($3,800 / 2,568 GB). Gain cell: $0.41/GB.

**Capex.** DRAM greenfield costs $158k per wafer-start/month; ÷ 2,568 GB = $61 per GB/month. A cell line scaled by processing dollars (× 0.8 tool intensity) costs $87k per wpm; ÷ 10,804 GB = **$8 per GB/month** [ESTIMATE]. Of that 7.6×, ~4.2× is tier density, which any in-house 3D DRAM would also get.

**EUV.** None on either wafer. Against 5–7 layers × $165 = **$825–1,155 per wafer** at 1c (19–27% of a $4,308 wafer).

**Bonds and yield.** A die carries 3.64e6 signal bonds plus 0.85e6 word-line bonds (4.49e6 in all). At 1e-5 opens per link that is ~45 dead links per die. With 1% spare groups, repaired die yield stays >0.9 up to **~6e-3 per link**. Opens are therefore not the threat. **Bridges** are: if 25% of a signal pad's neighbours are unswitched global supplies, then at a bridge rate of 0.1 × opens, die yield = exp(−0.1 × 1e-5 × 4.49e6 × 0.25) = **0.33**.

| Quantity | CELL-WAFER FOUNDRY 1T1C-64 | Gain-64 | 1β DDR5 |
|---|---|---|---|
| Density | 2.01 Gb/mm² | 2.60 | 0.447 |
| Array efficiency | 0.86 | 0.86 | 0.51 |
| Cbl / Cs | 19.9 fF / 1.16 fF | 15.5 fF / — | 35 fF / 5.4 fF |
| Bitline energy | 11.0 fJ | 8.6 fJ | 19.3 fJ |
| $/GB | $0.54 | $0.41 | $1.48 |
| EUV layers | 0 | 0 | 5–7 at 1c |
| New memory-fab capex | ~$8 per GB/month | — | ~$61 |

**Corrections carried from the critics and the model**

- **Yield:** the concept's 0.97 × 0.95 × 0.99 = 0.91 becomes 0.84 at 64 tiers, dominated by tier yield (0.88), not the bond.
- **Dead segments:** "~220 on 50 mm² at 1e-5" becomes ~45 per 15.9 mm² die. The 1e-5 open bar has >100× headroom and survives only as a proxy for bridge and reliability tails.
- **Bond parasitics** (0.43 fF) are ~2% of Cbl, so the I-04714 critic's ~$900k bonded sense tape-out becomes a ~$50k on-chip emulator.
- **Kill pitch** is ~2.5 µm (1T1C) to ~3 µm (gain), not A3's 2 µm.
- **Word-line bonds** outnumber signal bonds without 1:8 TFT predecode on the cell wafer; with it they are ~19% of all bonds (0.85e6 of 4.49e6).
- **Destructive-read 1T1C** must group bitlines across rows (+7 fF), so the spec favours non-destructive cells or WL segmentation.
- **Periphery** is 36–64% of pair cost; a reduced-metal $1.9k flow is worth ~30 tiers. The **N-36 glass carrier** saves ≤$115/pair (2%): a resource win, not a cost win.
- **"Production-proven" is too strong.** Production bonds at 6 µm (SoIC) and ≤10 µm (Xtacking); 1.5 µm is ~4× finer and research-proven only (imec 1.08 µm).
- **Null hypothesis.** Oxide cells could be built monolithically on the periphery wafer (CuA). The bonded split costs **+$800 per pair**, so the cell line must process each tier ≥$12.5 cheaper than logic BEOL at 64 tiers (42% of $30), ≥$25 at 32, ≥$6.2 at 128. Otherwise only D2W known-good-die selection, tool specialisation, thermal or hydrogen freedom, or cycle time justifies it.

**Sensitivity (1T1C-64 unless noted)**

| Variable | Range | Result |
|---|---|---|
| Tiers | 16 / 32 / 128 | $1.32 (0.89×) / $0.77 / $0.49 per GB. Break-even at 16 tiers (12 for gain) |
| $/tier | $20 / $45 | $0.48 / $0.63 |
| Periphery wafer | $1.9k / $3.45k | $0.46 / ~$0.60 |
| SA area | 1–5 µm² | 1.69–2.16 Gb/mm² (3.8–4.8×) |
| Sense threshold | 50 mV | Cs 2.11 fF; 1.53 Gb/mm² (3.4×) |
| Bond pitch | 2.0 / 2.5 / 3.0 µm | 1.86 / 1.57 / 1.31 Gb/mm²; Cs 1.40 / 2.01 / 2.78 fF |
| Opens, no spec rule | 1e-6 / 1e-5 / 1e-4 | Yield 0.89 / 0.33 / ~0; $0.60 / $1.65 / >$100 |
| Opens, with switched supplies | up to 3e-3 (>0.9 to ~6e-3) | Yield 1.00; $0.54 (spares exhausted at 1e-2) |
| Particles ≥0.5 µm | 0.05 / 0.5 / 2 per cm² | W2W yield 0.97 / 0.70 / 0.24; D2W 0.99 / 0.92 / 0.73 |
| Residual run-out after compensation | 10% / 25% | Tolerable bow 726 / 290 µm (budget 0.375 µm) |

**GO/NO-GO threshold.** The test vehicle is an 8-tier oxide coupon (~5 µm of stressed film) bonded W2W at ≤1.5 µm. **GO** requires all of:

- opens ≤1e-5 per link (95% UCL over ≥1e7 links, i.e. ≤83 failures), with no new opens after 500 cycles of −40/125 °C;
- bridges ≤1e-7 per adjacent pair (zero shorts in ≥3e7 pairs);
- overlay ≤0.30 µm on 100% of dies after backside compensation (bow ≤~200 µm);
- ≥95% void-free dies;
- after a ≤250 °C anneal, ΔVt ≤20 mV and an 85 °C retention change ≤2×.

**NO-GO for 1T1C** is any of: opens ≥1e-4 at 2.0 µm, bridges ≥1e-6, or overlay >0.5 µm after best compensation. Gain cells hold to ~3.0 µm.

---

## 3. What is new versus prior art

| Who / what | Date | Relation |
|---|---|---|
| Samsung 10a 4F² VCT: IGZO channel, periphery wafer W2W-bonded under the cells (PUC), 2028 target ([TrendForce](https://www.trendforce.com/news/2026/04/24/news-samsung-reportedly-produces-sub-10nm-10a-dram-working-die-using-4f-square-and-vct-targets-2028-production/)) | 2026-04-24 | Closest in-house split |
| Samsung 16-tier VS-DRAM with peri-on-cell bonding (T5.1); SK hynix 4F² VG with die thinning for wafer-bonded structures (T8.5) ([VLSI 2026 tipsheet](https://www.vlsisymposium.org/wp-content/uploads/2026/04/2026-VLSI-Technical-Tipsheet-REVISED-FINAL-NO-IMAGES-4.24.26.docx); [Mynavi](https://news.mynavi.jp/techplus/article/vlsi2026-5/)) | 2026-06 | In-house, 3D |
| YMTC Xtacking (bond pitch ≤10 µm; 4.0 at 12.66 Gb/mm²); Kioxia/WD CBA in volume NAND ([Yole](https://www.yolegroup.com/product/report/nand-comparison-2026/); [TechInsights](https://www.techinsights.com/blog/ymtc-xtacking40-breaking-new-ground-3d-nand-technology)) | 2025–26 | NAND, in-house |
| UniIC/XMC SeDRAM: a DRAM wafer Cu-Cu stacked on a logic wafer of another node, 0.88 pJ/bit ([XMC](https://xmcwh.com/en/site/details/300?details=1)) | n.d. | Closest cross-node precedent, but a whole-die interface |
| imec W2W at 1.08 µm, 70,866-link chains ([imec](https://www.imec-int.com/en/articles/wafer-wafer-hybrid-bonding-pushing-boundaries-400nm-interconnect-pitch)); 300 nm pitch ([ECTC 2025](https://www.imec-publications.be/entities/publication/6228fcc8-685e-4e72-83ba-3cb478415500)); imec+EVG 200 nm pitch, overlay <40 nm on flat wafers ([EVG](https://www.evgroup.com/fileadmin/media/company/news/2026/2026_05_28_IMEC/Press_Release_IMEC_EVG_2026_05_28_EN.pdf)); D2W at 2 µm, daisy-chain e-yield >70% ([Electronic Specifier](https://www.electronicspecifier.com/?p=32321)) | 2025–26 | Bond-process benchmarks, all on flat wafers |
| TSMC SoIC 9 → 6 µm; Intel Foveros Direct shipping 1H26 ([Tom's Hardware](https://www.tomshardware.com/tech-industry/semiconductors/hybrid-bonding-roadmap-examined)) | 2026 | Production pitch |
| US 10,340,261: cell-array-only chip bonded to a logic chip with SAs and word drivers, plus pitch conversion ([Google Patents](https://patents.google.com/patent/US10340261)); US 11,430,766; US 11,114,453; US 11,094,653 | granted | **The generic split is anticipated** |
| Adeia/Xperi DBI licences: Micron 2022 ([Business Wire](https://www.businesswire.com/news/home/20220222006259/en/Xperi-and-Micron-Enter-Into-License-Agreement-for-Hybrid-Bonding)); AMD March 2026 after litigation ([MarketBeat](https://www.marketbeat.com/instant-alerts/adeia-q2-earnings-call-highlights-2026-08-03/)) | 2022–26 | Freedom-to-operate gate |
| Canon NIL trialled at SK hynix and Kioxia ([Bits&Chips](https://bits-chips.com/magazine/bc202308/?pagenr=7)); scanning-beam IL ([US 9,195,146](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9195146)) | 2015–23 | Optional periodic patterning (N-31) |
| OpenGCRAM, an open gain-cell compiler ([arXiv 2507.10849](https://arxiv.org/abs/2507.10849)) | 2025 | Open periphery IP, not an interface |

**The genuine delta**

1. An **open, cross-line, bitline-group electrical and mechanical spec**. No open *bitline-level* spec was found in A3, Stage 2 or this run. The nearest open interface is die-level (UCIe, named by the I-04714 Stage 2 critic), and the in-house splits above (VCT/PUC, VG, Xtacking, CBA, SeDRAM) already implement proprietary versions of the same cut.
2. **Spec content the model derived**, patentable as implementation: a pad grid matched to sense-amp area; a non-destructive-cell preference (or WL segmentation for 1T1C); an oxide-TFT WL predecode layer; a **domain-switched supply adjacency rule** that turns a die-fatal bridge into a repairable domain loss; a bow and anneal budget; bond-link BIST and remap.
3. **Hybrid bonding of warped multi-tier oxide memory stacks.** Two searches found no published yield data. The nearest literature is 3D NAND bow (+300 to −550 µm; [SPIE 11326](https://photonicsforenergy.spiedigitallibrary.org/conference-proceedings-of-spie/11326/113260M/How-to-improve-overlay-of-highly-deformed-3D-NAND-wafers/10.1117/12.2552042.full)).

**Not new:** the split itself, cross-node DRAM-on-logic stacking, interference lithography. The delta is the interface and its yield rules, not the bonding.

---

## 4. Show-stoppers and how persistence could get around them

| # | Show-stopper | Number | Workaround path |
|---|---|---|---|
| 1 | **Bow-driven overlay** on multi-tier wafers | 5 µm film × 100–500 MPa gives 311–1,557 µm of bow. The budget is 0.375 µm at 1.5 µm pitch, so bow must be ≤~200 µm (or ≤290 µm if residual run-out is 25%) | Backside SiN compensation (3D NAND practice); litho pre-compensation, reported to halve residual distortion ([Research Square](https://www.researchsquare.com/article/rs-9444875/v1)); stress-balanced tier films; 2.0 µm pitch (0.50 µm budget); D2W of small dies (die bow scales with size²) |
| 2 | **Bridges** onto global supplies | At 25% supply adjacency, yield drops below 0.95 above 5e-7 opens per link, and is 0.33 at 1e-5 | Spec rule: signal pads neighbour only signal or domain-switched supply pads. Add BIST and remap. Comb structures in the test vehicle measure the rate directly |
| 3 | **Particle voids** (W2W) | A 0.5 µm particle unbonds a 2–3 mm radius ([YAP+](https://arxiv.org/pdf/2511.05506) lists voids as a top failure mode). Yield is 0.70 at 0.5/cm² and needs ≤0.05/cm² | Fab-grade CMP and clean at the bonding partner; edge trim; D2W (0.92 at 0.5/cm²) |
| 4 | **Anneal-induced oxide Vt shift** | 250 °C × 2 h equals 0.09–0.36 yr at 85 °C. IGZO's ionic bonding rearranges in anneals above ~300 °C ([KIEEME](https://koreascience.kr/article/CFKO201622355579119.pdf)). The limit is ΔVt ≤20 mV | 180 °C Cu/SiCN bonding with O₂ plasma ([Seoul Tech](https://pure.seoultech.ac.kr/en/publications/characterization-and-optimization-of-sicn-films-for-low-temperatu/)); room-temperature surface-activated bonding ([Kim/Suga 2003](https://www.ece.mcmaster.ca/~mrhowlader/Publications/Cu_Cu%20bonding.pdf)); pre-characterised drift plus trim; Al₂O₃ hydrogen barriers |
| 5 | **Monolithic CuA null hypothesis** (structural, not physics) | The split costs +$800 per pair and needs ≥$12.5/tier advantage at 64 tiers | D2W known-good die; high-aspect-ratio tools logic fabs lack; >400 °C or H-rich cell steps the periphery cannot see; reduced-metal $1.9k periphery |
| 6 | **The cell must pass** | 1T1C break-even at 16 tiers (12 for gain); the 0.36× case needs 64 tiers at 0.998 repaired tier yield | Keep the spec cell-agnostic across four portfolio cells (AND-STACK, PIXEL-STACK, DIODE-TOWER, 2T0C). Even 16 tiers gives cost parity with zero EUV |
| 7 | **Word-line bond demand** and oxide TFT drift | Without predecode, WL bonds exceed signal bonds. The I-02936 critics estimate 50–100 mV of oxide drift | The predecode is digital and offset-tolerant; go to 1:16–1:64 predecode; keep SAs and drivers on Si |
| 8 | **Thin U.S. 22/28 nm capacity** | GF's 22/28 nm prototyping is fabricated in Dresden ([Fraunhofer IIS](https://www.iis.fraunhofer.DE/content/dam/iis/en/doc/il/ics/GF%20HR%20CMYK.pdf)). A $3.45k periphery gives ~$0.60/GB | U.S. 12/14 nm or Intel 16 [UNVERIFIED-training]. A ~$4.5k periphery gives ~$0.70/GB [ESTIMATE], with a smaller SA as a partial offset |
| 9 | **Freedom to operate** | US 10,340,261 and the Adeia DBI portfolio | Narrow implementation claims (§6); a licensed bonding supplier |

Revival if the 8-tier W2W stack fails: D2W/KGD with small dies, room-temperature SAB, or bonding thinner sub-stacks.

---

## 5. The decisive experiment

### 5R. Revised decisive experiment (revised after red team)

**Objective.** Measure the binding failure modes on warped 4- and 8-tier oxide coupons bonded **D2W** (primary) at **2.0 and 1.5 µm**:
- opens and bridges;
- overlay;
- voids;
- post-bond ΔVt.

Also measure the risks the reviewers showed were missing:
- bond-plane hydrogen;
- the oxide sub-word-line driver and group select;
- in-stack adhesion;
- contamination;
- bond-proximity RTN/VRT.

All of it runs at a **fab-grade bonding partner** with particle density logged.

**Changes to the step list (original steps 1–12 below still apply unless replaced)**
1. **Bond mode (PROC-01).** D2W is primary for both lots. W2W runs one 4-pair split in lot 1, and continues to lot 2 only if both-axis shape maps show an anisotropic half-difference of ≤40 µm after compensation. The 1.0 µm pitch is dropped: the SA-area limit makes it worthless.
2. **Fab-grade surfaces (IND-04).** Bond-layer CMP, clean, particle inspection and bonding all happen at the partner. Opens and bridges are counted only on CSAM-void-free fields, so university particles cannot trip K4. The model shows D2W void yield of 0.905 even at 0.5 particles/cm².
3. **Hydrogen gate (DEV-01, PROC-04, DEV-02).**
   - Barrier split: none / O₃-ALD Al₂O₃ / Al₂O₃ + low-H SiN + Al₂O₃.
   - Deuterium-labelled bond surfaces (D₂O rinse or D-plasma activation), so ToF-SIMS separates bond-origin hydrogen from background.
   - ΔVt of top-tier cells **and** of the selector and sub-WL-driver TFTs, measured after the bond, after 3 × 260 °C reflow and after 1,000 h at 125 °C.
   - Anneal split at 150/200/250/300 °C, to test whether one activation energy matches 85 °C aging.
4. **Oxide circuits on the coupons (CIRC-01, DEV-03, CIRC-04).**
   - A bootstrapped 1:8 sub-WL driver with VNWL clamps, driving a ~260 fF WL load. Measure WL high and hold levels, 10–90% edges, and level loss after 1,000 h of PBTI stress at 125 °C.
   - A 196:1 oxide group-select mux. Measure R_on, Vt spread, kickback and charge injection.
   - In lot 2, both are read through the bonds by the MPW SA board.
5. **Sense chain (CIRC-02, CIRC-03).**
   - Field-solver α for the 73 µm global line, shielded and unshielded.
   - A 28 nm SA layout with offset cancellation and write driver at ≤4 µm², Monte Carlo σ ≤7 mV, taped out on the MARGIN STACK MPW share.
6. **Adhesion (DEV-04).**
   - Four-point bend on the tier-stack laminates, requiring Gc ≥5 J/m².
   - Unbonded control chains through the tiers, given the same thinning and cycling.
   - FIB on **every** failed chain, to locate the failing plane.
7. **Contamination (PROC-03).** VPD-ICPMS on bevel, backside and front before the bond line, requiring In/Ga/Zn ≤1e10 at/cm².
8. **Cu reliability (PROC-04).** A nanotwinned-Cu split for low-temperature bonding. Kelvin-resistance stability after **1,000** thermal cycles (was 500).
9. **RTN/VRT at the right timescales.** Top-tier versus bottom-tier cells and select TFTs, pre- and post-bond, on 1e4–1e5 devices:
   - ns–µs sampling for the select/read path;
   - second-scale retention VRT.

   This isolates bond-proximity degradation.
10. **GATE 1 at M14** (4 tiers, D2W). **GATE 2 moves M20 → M22**, because of the 1,000 h bake after the lot 2 bond.

**Revised budget (experiments)**

| Item | Original $ | Revised $ |
|---|---|---|
| A. Spec, model, layout, field-solver α, 28 nm SA layout and Monte Carlo | 25,000 | 30,000 |
| B. Masks: coupon layers incl. TFT driver/mux test structures, bond reticles at 1.5/2.0 µm | 45,000 | 55,000 |
| C. Purdue coupons: 2 lots with H-barrier and adhesion splits | 170,000 | 175,000 |
| D. Fab-grade bonding partner: CMP/clean, particle maps, 2 D2W lots, 1 W2W 4-pair lot (+1 conditional), IR overlay, CSAM, thinning | 280,000 | 275,000 |
| E. Electrical test incl. ns pulse/TFT driver tester, 125 °C 1,000 h bake, reflow, RTN sampling | 55,000 | 65,000 |
| F. Failure analysis and materials: ~25 FIB/TEM, ToF-SIMS with D-labelling, VPD-ICPMS, four-point bend | 25,000 | 60,000 |
| G. Sense-margin emulation (MPW share, board reading coupon selectors and drivers) | 50,000 | 50,000 |
| H. IP | 30,000 | 25,000 |
| I. Standards engagement (deferred after IND-01) | 20,000 | 5,000 |
| **Subtotal** | **700,000** | **740,000** |
| K. Contingency | 90,000 | 55,000 (7.4%, thin) |
| **Experiment total** | **790,000** | **795,000** |
| Founder pay (§6) | 200,000 | 200,000 |
| **Plan total** | **990,000** | **995,000** |

**Revised GO (D2W, 8 tiers, ≤2.0 µm).** All of the original GO items must hold, plus:
- anisotropic warp ≤40 µm, or else W2W is dropped (not a concept kill);
- D-traced hydrogen shows no rise in the top-tier channel above background with the chosen barrier;
- ΔVt ≤20 mV on top-tier cells and on selector/driver TFTs after the bond, 3 × 260 °C reflow and 1,000 h at 125 °C;
- the oxide sub-WL driver delivers VPP with ≤50 mV level loss, ≤10 ns edges and an active ≤−0.5 V clamp after stress;
- tier-stack Gc ≥5 J/m²;
- VPD-ICPMS ≤1e10 at/cm²;
- Kelvin resistance stable after 1,000 cycles.

---

### 5.0 Original decisive experiment (pre-red-team, kept for traceability)

**Objective.** Measure the four binding failure modes (opens and bridges, overlay on bowed wafers, particle voids, anneal ΔVt) on the stack the concept needs: warped 4- and 8-tier oxide/metal coupons with real oxide FETs and mini-arrays, bonded at 1.0, 1.5 and 2.0 µm.

**Facilities**
- **Primary bonding partner:** SkyWater-operated Center for NeoVation (Osceola County, FL), SUSS XBC300 Gen2 for 200/300 mm W2W and D2W hybrid bonding ([SUSS](https://www.suss.com/de/news/technical-publications/suss-microtec-xbc300-gen2-neovation-microelectronics)). Tool [REPORTED]; service terms unverified.
- **Coupon fab:** Purdue Birck: three tiers of ALD In₂O₃ FETs on 200 mm, >100k devices ([Purdue](https://engineering.purdue.edu/ECE/News/2026/purdue-researchers-build-3d-chip-platform-for-faster-more-efficient-ai-computing)).
- **Alternate:** NY CREATES Albany NanoTech, 300 mm, memory JDA with Fraunhofer IPMS ([idw](https://nachrichten.idw-online.de/2025/05/16/ny-creates-and-fraunhofer-ipms-announce-joint-development-agreement-to-advance-memory-devices-at-300mm-wafer-scale)) and NSTC startup access ([NY.gov](https://www.ny.gov/roadmap-national-semiconductor-technology-center-new-york)); bonding capability [UNVERIFIED-training].

**Step by step**
1. **Spec v0.1 (M0–3):** 1.5 µm grid (1.0/2.0 µm alternates), pad = 0.5 × pitch; signal classes; Cbl 10–30 fF, Cs ≥1 fF or I_read ≥1 µA, VPP ≤3.0 V; BIST/remap; bow ≤200 µm; ≤250 °C for 2 h.
2. **Test-vehicle reticle (M1–4):** daisy chains of 1e3/1e4/1e5 links (resolving 1e-7 to 1e-3); Kelvin links; combs beside signal and supply pads (≥3e7 pairs, 34 mm²); overlay verniers at centre, mid-radius and edge; stress monitors.
3. **Coupon lot 1 (M3–8, Purdue, 200 mm):** 4-tier stack (~2.5 µm of film) with In₂O₃/IGZO FETs and 1–4 kb 2T0C/1T1C mini-arrays; backside compensation split at 0/50/100%; shape maps; pre-bond Vt and 85 °C retention.
4. **Periphery-emulator wafers (M4–8):** Cu-damascene daisy-chain halves in SiCN, 2–3 masks. No real 28 nm wafer is needed, since bond parasitics are ~2% of Cbl.
5. **Bond layer on coupons (M6–9):** ILD, Cu, CMP to recess spec, clean, particle inspection.
6. **Bond lot 1 (M8–10):** 6 W2W pairs annealed at 200/250/300 °C, one D2W split, IR alignment metrology, CSAM void maps.
7. **Thin and reveal pads (M10–11).**
8. **Test (M11–14):** ≥1e7 links and ≥3e7 comb pairs per wafer; Kelvin distribution; overlay against bow; post-bond Vt and retention; 500 thermal cycles on half the dies; FIB/TEM and ToF-SIMS hydrogen profiles on failures.
9. **GATE 1 (M14).**
10. **Lot 2 (M14–20).** An 8-tier stack (~5 µm of film) with the best recipe, at the best pitch and at 1.0 µm, plus mini-arrays read through the bonds by an external SA board.
11. **Sense-margin emulation (M16–22).** Uses a share of the MARGIN STACK 22/28 nm MPW, with a programmable Cbl and a 0–2 fF bond emulator.
12. **Spec v1.0, PCT and data room (M20–24).**

**Budget (experiments only; founder pay in §6)**

| Item | $ |
|---|---|
| A. Spec, model, test-vehicle layout (KLayout) | 25,000 |
| B. Masks: coupon layers plus 3 i-line/KrF bond reticles | 45,000 |
| C. Purdue coupons: 2 lots at 200 mm, sponsored student/postdoc plus user fees | 170,000 |
| D. Bonding partner: CMP/clean, bond layers, 2 W2W lots × 6 pairs, 1 D2W lot, IR overlay, CSAM, thinning | 280,000 |
| E. Electrical test: used semi-auto prober, cards, SMU, switch matrix, thermal chamber | 55,000 |
| F. Failure analysis: ~15 FIB/TEM lamellae, ToF-SIMS | 25,000 |
| G. Sense-margin emulation (MPW share, board) | 50,000 |
| H. IP: 3 provisionals plus 1 PCT | 30,000 |
| I. Standards engagement, patent-pledge drafting | 20,000 |
| **Subtotal** | **700,000** |
| K. Contingency (~13%) | 90,000 |
| **Experiment total** | **790,000** |

No quotes obtained; C and D are [ESTIMATE]. Statistics: 1e7 links pass at ≤83 opens (95% UCL ≤1e-5); zero shorts in 3e7 pairs gives ≤1e-7.

**Pre-set pass/fail.** The gates are the §2 GO/NO-GO, plus intermediate gates:
- bow ≤200 µm after compensation (M8);
- ≥95% void-free dies by CSAM (M11);
- bond-parasitic sensitivity <5% of sense margin (M22).

---

## 6. The $1M, 24-month plan

Month 1 = January 2027.

| Quarter | Milestones | Gate |
|---|---|---|
| Q1 (M1–3) | Spec v0.1; partner agreements; provisionals 1–2; test-vehicle layout | Bonding quote ≤$300k, or switch partner |
| Q2 (M4–6) | Masks; coupon lot 1 starts; emulator wafers | Coupon FETs working pre-bond |
| Q3 (M7–9) | Stress-compensation split; bond layers | **Bow ≤200 µm** |
| Q4 (M10–12) | Bond lot 1 (W2W + D2W); thin; first test | **≥95% void-free** |
| Q5 (M13–15) | Full test, cycling, FIB | **GATE 1 (M14, Feb 2028):** opens ≤1e-5, bridges ≤1e-7, overlay ≤0.30 µm, ΔVt ≤20 mV on 4 tiers |
| Q6 (M16–18) | 8-tier coupon lot 2; MPW emulator taped out | — |
| Q7 (M19–21) | Bond lot 2 and test | **GATE 2 (M20, Aug 2028):** GO/NO-GO on 8 tiers |
| Q8 (M22–24) | Emulator results; spec v1.0 published; PCT; raise | Data room complete |

**Budget allocation ($990k).** Experiments $700k (71%), founder pay 2 × $50k/yr × 2 yr = $200k (20%), contingency $90k (9%). *(Revised after red team: $995k. Experiments $740k, contingency $55k, founder pay $200k. GATE 2 moves to M22, and the bond mode is D2W-primary; see §5R and §11.)*

Portfolio caveat: inside the portfolio seed (FINAL_CONCEPTS, ~$735k of experiments across ten concepts), only A, H and I (~$75k) are seed-funded. Items B–G (~$625k) become partner-funded, grant co-funded (SBIR or CHIPS-consortium programmes) or a raise milestone.

**Team**
- **Founder 1, architect.** Owns the spec, the model, partners and standards.
- **Founder 2, recruited hybrid-bond integration engineer** who owns daisy-chain, comb, vernier and bow design. Recruit from the imec 3D programme, Sony stacked CIS, Kioxia CBA, Intel Foveros Direct, TSMC SoIC or Micron HBM.
- **Sponsored Purdue student/postdoc** for the coupon fab.
- **Part-time DRAM periphery designer** (ex-Micron or other DRAM design teams) for the SA emulator; full hire after the raise.
- **Advisors to approach** [UNVERIFIED-training]: Peide Ye (Purdue, ALD In₂O₃); Shimeng Yu and Muhannad Bakir (Georgia Tech); Subramanian Iyer (UCLA CHIPS, interface standards); H.-S. Philip Wong and Subhasish Mitra (Stanford, monolithic 3D); James Lu (RPI, wafer bonding); Paul Franzon (NC State, 3D IC); Mark Schattenburg (MIT, SBIL) for the optional IL path.

**IP strategy.** File narrow implementation claims first.
- **Provisional 1 (M2):** domain-switched supply adjacency plus bond-link BIST and remap: detectable in competitors' products and independent of the generic split.
- **Provisional 2 (M3):** SA-area-matched bond grid; cross-row grouping for destructive cells, free clustering for non-destructive cells; TFT predecode sized to the bond-site budget.
- **Provisional 3 (M12, after coupon data):** a stress-compensated multi-tier oxide cell wafer co-specified with a ≤250 °C budget, plus an Arrhenius pre-bond drift-prediction method.
- **Later:** the periodic array as a moiré W2W overlay target (N-31). **PCT by M24.**
- **The spec itself:** publish under an open licence with a royalty-free or FRAND pledge for compliant implementations (the UCIe/OCP model), and license the implementation patents.

**Freedom-to-operate risks**
- Read the claims of US 10,340,261, 11,430,766, 11,114,453 and 11,094,653 before filing anything generic.
- R&D bonding at a licensed partner is lower risk. Product needs an Adeia DBI licence.
- Monitor Samsung VCT/PUC, SK hynix VG, YMTC and Kioxia CBA filings for bitline-level grid and segment-repair claims.

---

## 7. After the demo: scale path

**Who partners and why**

- **Kioxia** owns both halves in-house: OCTRAM oxide cells (Ion >15 µA, Ioff <1 aA, [Business Wire](https://www.businesswire.com/news/home/20241209099702/en/Kioxia-Develops-OCTRAM-Oxide-Semiconductor-Channel-Transistor-DRAM-Technology); 8-layer 3D OCTRAM, [Kioxia](https://www.kioxia.com/en-jp/about/news/2025/20251212-1.html)) and CBA bonding. It and other NAND makers with idle decks are natural cell-wafer makers.
- **Micron**, the U.S. DRAM maker and an Adeia licensee, is the licence target for the spec and yield rules, and has the most reason of the incumbents to want U.S. logic periphery.
- **Samsung and SK hynix** already split in-house (VCT PUC, VS-DRAM, VG). They would license implementation patents, not buy merchant wafers; their incentive to open the interface is weak, which the mission does not kill on.
- **Foundries** (GlobalFoundries, SkyWater, Intel, TSMC Arizona) sell periphery wafers and could host BEOL cell tiers, so they are both customer and null-hypothesis competitor (monolithic CuA).
- **Display makers:** critics put panel steppers at ~1.2–1.5 µm, so they cannot make F~40 nm cell wafers. They bring oxide-TFT know-how and glass carriers (N-36).

**What $10–50M buys** [ESTIMATE]
- **$10–15M:** spec v1.x through a consortium; 300 mm coupons at NY CREATES; a real 28 nm SA plus WL-driver periphery bonded to a 16-tier portfolio-cell array (a Mb-class functional macro with retention and disturb data); an Adeia licence.
- **$30–50M:** a partner-hosted 32–64-tier Gb-class demonstrator; JEDEC-style reliability qualification; a fab-lite agreement for a depreciated U.S. 200/300 mm line. An owned 300 mm cell line exceeds this round [SPECULATIVE].

**Standards.** OCP published its first spec for a new memory class, High Bandwidth Flash, in August 2026 ([eeNews](https://www.eenewseurope.com/en/sk-hynix-sets-first-hbf-standard-for-ai-memory/)): the fastest template. JEDEC follows for qualification, or a CHIPS/NSTC consortium.

---

## 8. Resources and America

- **EUV.** Zero layers on both wafers. Low-NA EUV is supply-capped at ~65 shipments in 2026 ([MarketBeat](https://www.marketbeat.com/instant-alerts/asml-q2-earnings-call-highlights-2026-07-15/)). DRAM is adding EUV layers at 1c: "five or more" at SK hynix ([TechNews](https://technews.tw/2025/08/12/euv-sk-hynix-1c-dram/)) and 6–7 at Samsung ([TrendForce](https://www.trendforce.com/news/2025/03/11/news-micron-pioneers-1%CE%B3-ddr5-samples-with-reduced-euv-use-but-future-risks-loom/)).
- **Capital and cleanroom.** This is the binding constraint. New cleanroom output is not meaningful until late 2028 ([CIO/Micron](https://cio.com/article/4229625/memory-squeeze-set-to-tighten-through-2028-micron-says.html); [JoongAng](https://www.koreajoongangdaily.com/business/samsung-and-sk-are-expanding-fast-but-why-is-memory-still-in-short-supply/12526698)). The concept puts periphery on *existing* logic capacity: ~93 wafers/month per 1M GB/month, or $5.6–9.3 per GB/month if it had to be built new.
- **Gallium and indium.** IGZO uses <0.4% In and Ga, but gallium is ~98% Chinese. China's Ga/Ge export ban on the U.S. is suspended only until **2026-11-27** ([Fastmarkets](https://fastmarkets.com/insights/china-suspends-export-prohibition-on-superhard-materials-us)). The spec should qualify Ga-free In₂O₃ or ZTO channels.
- **Helium.** Qatar has been offline since March 2026 ([AP/WTOP](https://wtop.com/news/2026/03/iran-war-halts-qatar-helium-output-threatening-global-tech-supply-chains/); [IUMI](https://iumi.com/newsletter-june-2026/qatari-helium-shortages/)). Deep tier etch on the cell line uses backside helium unless the LEAN ARRAY MODULE H₂ recipe is adopted.
- **Energy and water.** A2 puts DRAM at ~1,300 kWh and ~8 m³ per wafer (0.42 kWh, 2.6 L per GB). [SPECULATIVE] If the cell-plus-periphery pair draws ~2× one DRAM wafer while delivering 4.2× the GB (model: 10,804 vs 2,568 GB), that is ~0.24 kWh/GB, ~2.1× below the ~0.51 kWh/GB that 1,300 kWh gives on the model's 2,568 GB 1β wafer (A2's 0.42 implies ~3,100 GB/wafer; ~1.75× on that basis); break-even is ~4.2× per-wafer energy. Siting is the real limit (Micron Clay: up to 48 MGD, [WSKG](https://www.wskg.org/news/2023-08-06/micron-estimates-needing-up-to-48-million-gallons-of-water-a-day-aiming-to-achieve-100-water-conservation)); a small cell line plus distributed logic capacity eases it.
- **U.S. manufacturability.** Bonding: SkyWater Center for NeoVation (sourced), NY CREATES [UNVERIFIED]. Coupons: Purdue (sourced). Periphery: U.S. 12/14 nm or Intel 16 [UNVERIFIED-training]; GF's 22/28 nm is in Dresden. Volume cell line: the gap, since no U.S. NAND-class volume line exists.

---

## 9. Kill criteria

### Revised kill criteria (revised after red team)

Month 1 = January 2027. Each kill names its revival condition.

1. **K1′, M8. Anisotropic warp (PROC-01).** If no compensation split brings the anisotropic half-difference to ≤40 µm (≤97 µm allowed at 2.0 µm pitch with perfect isotropic correction), **W2W is dropped for multi-tier wafers.** This is not a concept kill: D2W is already primary. *Revival:* stress-balanced 0/90° die-orientation layouts, or patterned backside stress films.
2. **K2′, M14. Bond physics.** The 1T1C variant is dead if any of these holds, in D2W at 2.0 µm:
   - opens ≥1e-4 per link;
   - bridges ≥1e-6 per adjacent pair;
   - overlay >0.5 µm.

   All three are counted on CSAM-void-free fields only. Gain cells continue only if ≤3.0 µm passes.
3. **K3′, M14. Hydrogen and thermal (DEV-01/02, PROC-04).** If ΔVt >20 mV, or 85 °C retention falls >2×, on top-tier cells **or** on selector/sub-WL-driver TFTs at every anneal tested, **with the best barrier stack**, after 3 × 260 °C reflow and 1,000 h at 125 °C, then oxide cells are incompatible with dielectric hybrid bonding. *Revival:* Cu-only room-temperature SAB (no Si-OH condensation), a thicker multi-layer barrier with a hydrogen getter, or TFTs moved to the substrate side of the stack.
4. **K3b, M14. Oxide sub-WL driver (CIRC-01, DEV-03).** If no bootstrapped oxide driver holds ≤50 mV level loss, ≤10 ns edges and a ≤−0.5 V clamp after 1,000 h at 125 °C, the **TFT predecode leg is dead.** Without ≥1:8 predecode on the cell wafer, WL bonds exceed the sites at 1.5–2.0 µm. *Revival:* a layer-transferred thin-Si driver plane on the cell wafer (a cost adder to price), or 1:16–1:64 decoding with Si-defined levels.
5. **K4′, M22. 8-tier GO.** If the 8-tier (~5 µm film) stack misses GO by D2W at ≤2.5 µm (1T1C) or ≤3.0 µm (gain), **the concept is dead.** *Revival:* bonding ≤4-tier sub-stacks repeatedly.
6. **K5′, M22. Re-scope trigger, not a kill.** Re-scope the spec if bond parasitics **plus** the oxide group-select effects (kickback, R_on, Vt spread) exceed 5% of sense margin, or if the field-solver α exceeds 0.05 with shielding.
7. **K6, M24. Unchanged.** If no portfolio cell has passed its own go/no-go, hibernate the spec.
8. **Demotion D1′, M24.** The threshold rises from $12.5 to ≥$15.3/tier (W2W) or ≥$21.4/tier (D2W) at 64 tiers. Note: a delamination failure inside the stack (Gc <5 J/m²) is routed to the cell's owner as a cell-stack problem, not counted against the bond.

### Original kill criteria (pre-red-team, kept for traceability)

Physics kills, each with its revival condition. Month 1 = January 2027.

1. **K1, M8 (Aug 2027).** If no compensation split brings a 4-tier coupon to bow ≤300 µm, *and* modelled residual run-out exceeds 25%: kill W2W for full wafers and pivot to D2W. *Revival:* stress-balanced tier films.
2. **K2, M14 (Feb 2028).** Opens ≥1e-4 per link at 2.0 µm, *or* bridges ≥1e-6 per adjacent pair, *or* max overlay >0.5 µm after best compensation: the **1T1C variant is dead**. Gain cells continue only if ≤3.0 µm passes.
3. **K3, M14.** If post-bond ΔVt >20 mV or 85 °C retention falls >2× at every anneal tested (down to the lowest that bonds, 180–200 °C): oxide cells are incompatible with thermal hybrid bonding. *Revival:* room-temperature SAB or a hydrogen-barrier stack.
4. **K4, M20 (Aug 2028).** If the 8-tier (~5 µm film) stack misses GO by both W2W and D2W at ≤2.5 µm (1T1C) or ≤3.0 µm (gain): **the concept is dead.** *Revival:* bonding ≤4-tier sub-stacks repeatedly, or die-level KGD bonding.
5. **K5, M22 (Oct 2028), re-scope trigger, not a kill.** Bond parasitics >5% of sense margin means the model is wrong; re-scope the spec.
6. **K6, M24 (Dec 2028).** If no portfolio cell (AND-STACK, PIXEL-STACK, DIODE-TOWER or 2T0C) has passed its own go/no-go, the concept has no product: hibernate the spec. *Revival:* any oxide cell at ≥16 tiers with ≥99.8% repaired tier yield.

**Demotion (step-change, not physics).**
- **D1, M24.** If a fab-cost model shows a NAND-class line's per-tier advantage over logic BEOL is <$12.5 at 64 tiers, and no thermal, hydrogen or KGD reason holds, the merchant split is not a step change over monolithic CuA. The spec survives as an option inside someone else's 3D DRAM.

---

## 10. Sources

All URLs are logged in `research/sources/*.jsonl` (mainly `dos-cell-wafer-foundry.jsonl`; also A1, A2, A3, B2, B3, `dos-and-stack`, `dos-hot-side-memory`, `dos-lean-array-module`, `s2-*`).

- **Bonding process:** https://www.imec-int.com/en/articles/wafer-wafer-hybrid-bonding-pushing-boundaries-400nm-interconnect-pitch ; https://www.imec-publications.be/entities/publication/6228fcc8-685e-4e72-83ba-3cb478415500 ; https://www.evgroup.com/fileadmin/media/company/news/2026/2026_05_28_IMEC/Press_Release_IMEC_EVG_2026_05_28_EN.pdf ; https://www.electronicspecifier.com/?p=32321 ; https://www.tomshardware.com/tech-industry/semiconductors/hybrid-bonding-roadmap-examined ; https://arxiv.org/pdf/2511.05506 ; https://www.researchsquare.com/article/rs-9444875/v1
- **Bow/warpage:** https://photonicsforenergy.spiedigitallibrary.org/conference-proceedings-of-spie/11326/113260M/How-to-improve-overlay-of-highly-deformed-3D-NAND-wafers/10.1117/12.2552042.full ; https://novami.com/wp-content/uploads/2025/04/challenges-and-responses-of-metrology-technologies-for-the-new-wave-of-3d-nand-devices.pdf
- **Low-temperature bonding and oxide drift:** https://pure.seoultech.ac.kr/en/publications/characterization-and-optimization-of-sicn-films-for-low-temperatu/ ; https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10489970/ ; https://www.ece.mcmaster.ca/~mrhowlader/Publications/Cu_Cu%20bonding.pdf ; https://ieeetv.ieee.org/hbs/feasibility-of-the-surface-activated-bonding-for-hybrid-bonding-and-its-alternatives ; https://koreascience.kr/article/CFKO201622355579119.pdf
- **In-house splits and cells:** https://www.trendforce.com/news/2026/04/24/news-samsung-reportedly-produces-sub-10nm-10a-dram-working-die-using-4f-square-and-vct-targets-2028-production/ ; https://www.vlsisymposium.org/wp-content/uploads/2026/04/2026-VLSI-Technical-Tipsheet-REVISED-FINAL-NO-IMAGES-4.24.26.docx ; https://news.mynavi.jp/techplus/article/vlsi2026-5/ ; https://www.techinsights.com/blog/ymtc-xtacking40-breaking-new-ground-3d-nand-technology ; https://www.yolegroup.com/product/report/nand-comparison-2026/ ; https://xmcwh.com/en/site/details/300?details=1 ; https://www.businesswire.com/news/home/20241209099702/en/Kioxia-Develops-OCTRAM-Oxide-Semiconductor-Channel-Transistor-DRAM-Technology ; https://www.kioxia.com/en-jp/about/news/2025/20251212-1.html ; https://www.guru3d.com/story/sk-hynix-achieves-yield-in-fivelayer-3d-dram-development ; https://engineering.purdue.edu/ECE/News/2026/purdue-researchers-build-3d-chip-platform-for-faster-more-efficient-ai-computing
- **Patents and licences:** https://patents.google.com/patent/US10340261 ; https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11430766 ; https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11114453 ; https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11094653 ; https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9195146 ; https://www.businesswire.com/news/home/20220222006259/en/Xperi-and-Micron-Enter-Into-License-Agreement-for-Hybrid-Bonding ; https://www.marketbeat.com/instant-alerts/adeia-q2-earnings-call-highlights-2026-08-03/
- **Patterning and open IP:** https://bits-chips.com/magazine/bc202308/?pagenr=7 ; https://arxiv.org/abs/2507.10849
- **Facilities, MPW, costs:** https://www.suss.com/de/news/technical-publications/suss-microtec-xbc300-gen2-neovation-microelectronics ; https://nachrichten.idw-online.de/2025/05/16/ny-creates-and-fraunhofer-ipms-announce-joint-development-agreement-to-advance-memory-devices-at-300mm-wafer-scale ; https://www.ny.gov/roadmap-national-semiconductor-technology-center-new-york ; https://www.crowdsupply.com/wafer-space/gf180mcu-run-2 ; https://www.isi.edu/news/80945/mosis-2-0-revives-a-legacy-rehan-kapadia-outlines-a-bold-future-for-rapid-microelectronics-prototyping/ ; https://siliconanalysts.com/data/wafer-pricing ; https://www.iis.fraunhofer.DE/content/dam/iis/en/doc/il/ics/GF%20HR%20CMYK.pdf ; https://github.com/ASU-VDA-Lab/ECO-CHIP
- **Standards:** https://www.eenewseurope.com/en/sk-hynix-sets-first-hbf-standard-for-ai-memory/
- **Resources:** https://www.marketbeat.com/instant-alerts/asml-q2-earnings-call-highlights-2026-07-15/ ; https://technews.tw/2025/08/12/euv-sk-hynix-1c-dram/ ; https://www.trendforce.com/news/2025/03/11/news-micron-pioneers-1%CE%B3-ddr5-samples-with-reduced-euv-use-but-future-risks-loom/ ; https://cio.com/article/4229625/memory-squeeze-set-to-tighten-through-2028-micron-says.html ; https://www.koreajoongangdaily.com/business/samsung-and-sk-are-expanding-fast-but-why-is-memory-still-in-short-supply/12526698 ; https://fastmarkets.com/insights/china-suspends-export-prohibition-on-superhard-materials-us ; https://wtop.com/news/2026/03/iran-war-halts-qatar-helium-output-threatening-global-tech-supply-chains/ ; https://iumi.com/newsletter-june-2026/qatari-helium-shortages/ ; https://www.wskg.org/news/2023-08-06/micron-estimates-needing-up-to-48-million-gallons-of-water-a-day-aiming-to-achieve-100-water-conservation
- **Red-team response sources:** `research/sources/resp-cell-wafer-foundry.jsonl` (Besi D2W 100 nm @3σ; Applied/Besi Kinex; ALD Al₂O₃ hydrogen barrier on IGZO, ~18×; KAIST Al₂O₃/SiNx passivation; hydrogen in oxide TFTs)

---

## 11. Red-team outcome

*Owner response, 2026-11-02, to the 17 objections in `research/redteam/rt_{DEV,PROC,CIRC,IND}.json`. Full responses: `research/redteam/responses_cell-wafer-foundry.json`. Model: `RED_TEAM_REVISIONS` block and output §10 (`research/stage3/cell-wafer-foundry_model_output.md`); `python3 models/cell-wafer-foundry.py --original` reproduces the pre-red-team numbers. WebSearch used: 2 of 3.*

**Dispositions: 0 REFUTED, 12 ACCEPTED-MITIGATED, 5 ACCEPTED-DOWNGRADE, 0 ACCEPTED-KILL.**

| Id | Severity | Disposition | One-line action |
|---|---|---|---|
| RT-CIRC-cell-wafer-foundry-01 | MAJOR | ACCEPTED-MITIGATED | WL predecode redesigned as a bootstrapped n-only sub-WL driver (gate ~5.1 V, Si-defined FX level, VNWL clamp per WL) on a dedicated TFT plane (19% of array area, +$60); new kill K3b |
| RT-CIRC-cell-wafer-foundry-02 | MAJOR | ACCEPTED-DOWNGRADE | Parity 6.25% → 15.6% plus modelled coupling (α 0.145 unshielded → 0.035 with two shielded metal levels, +$120). 1T1C density −10% (4.5× → 4.0× before CIRC-03) |
| RT-CIRC-cell-wafer-foundry-03 | MINOR | ACCEPTED-DOWNGRADE | SA 2.5 → 4.0 µm²: density −12% (to 3.6×). Restore τ 2.6 ns is OK. Spec pitch relaxes to 2.0 µm at no cost |
| RT-CIRC-cell-wafer-foundry-04 | MINOR | ACCEPTED-MITIGATED | Oxide 196:1 group-select mux and sub-WL driver built on both coupon lots and read through the bonds by the MPW board |
| RT-DEV-cell-wafer-foundry-01 | MAJOR | ACCEPTED-MITIGATED | Al₂O₃/low-H SiN/Al₂O₃ barrier (+$20). D-labelled bond-surface ToF-SIMS plus ΔVt on top-tier cells and TFTs after bond, 3 × 260 °C reflow and 1,000 h at 125 °C; K3′ extended |
| RT-DEV-cell-wafer-foundry-02 | MINOR | ACCEPTED-MITIGATED | Arrhenius map withdrawn as the spec basis (now a lower bound); anneal split 150–300 °C measured |
| RT-DEV-cell-wafer-foundry-03 | MINOR | ACCEPTED-MITIGATED | Same redesign as CIRC-01; DEV's 1,000 h/125 °C, ≤10 ns, ≤50 mV test adopted verbatim as K3b |
| RT-DEV-cell-wafer-foundry-04 | MINOR | ACCEPTED-MITIGATED | Four-point bend Gc ≥5 J/m², unbonded control chains, FIB on every failed chain; in-stack failures routed to the cell owner |
| RT-IND-cell-wafer-foundry-01 | MAJOR | ACCEPTED-MITIGATED | IP re-based: defensive open spec; claims on bond-ready oxide stack, oxide SWD plane and D-labelled qualification; adjacency rule admitted avoidable |
| RT-IND-cell-wafer-foundry-02 | MAJOR | ACCEPTED-DOWNGRADE | Split's own capex share ~1.5×, conditional on existing logic capacity. Null-hypothesis bar $12.5 → $15.3/tier (W2W) or $21.4/tier (D2W) |
| RT-IND-cell-wafer-foundry-03 | MAJOR | ACCEPTED-DOWNGRADE | Merchant leg demoted to optional; first adopter in-house (Micron + U.S. logic periphery); U.S.-supply claim goes from step change to enabler |
| RT-IND-cell-wafer-foundry-04 | MAJOR | ACCEPTED-MITIGATED | Fab-grade partner as a Q1 gate; opens/bridges counted on void-free fields only; D2W primary; portfolio-seed provability stated as No |
| RT-IND-cell-wafer-foundry-05 | MINOR | ACCEPTED-MITIGATED | DBI royalty booked at 1% of pair ($77; +~1% $/GB); FTO review of the post-2010 Adeia families |
| RT-PROC-cell-wafer-foundry-01 | MAJOR | ACCEPTED-MITIGATED | D2W primary (die run-out 0.038 µm + 0.10 µm placement against a 0.50 µm budget at 2.0 µm); W2W only if anisotropic warp ≤40 µm |
| RT-PROC-cell-wafer-foundry-02 | MAJOR | ACCEPTED-DOWNGRADE | Decks at AR ≤60 priced ($800/deck, 2 decks at 64 tiers). Cell wafer $2.6k → $4.4k; 1T1C break-even 16 → 28 tiers |
| RT-PROC-cell-wafer-foundry-03 | MAJOR | ACCEPTED-MITIGATED | Encapsulated bond face, bevel and backside; VPD-ICPMS ≤1e10 at/cm² clause in the spec; bond cost $400 → $500 |
| RT-PROC-cell-wafer-foundry-04 | MINOR | ACCEPTED-MITIGATED | Nanotwinned-Cu split; Kelvin stable after 1,000 cycles; 3 × 260 °C reflow added before the ΔVt and SIMS measurements |

**Redesigns adopted**
1. **D2W is the primary bond mode and the spec pitch is 2.0 µm (PROC-01, CIRC-03).**
   - With a 4 µm² SA, the bitline group is SA-area-limited up to 2.0 µm, so density and cost are unchanged.
   - The overlay budget grows to 0.50 µm.
   - D2W error is 0.14 µm (3.6× margin), against a ±2.2 µm residual for W2W on a saddle-warped wafer.
   - D2W is cost-neutral after throughput pricing and partial screening of cell dies: $0.92 vs $0.91/GB.
   - The 1.0 µm pitch is dropped.
2. **Bootstrapped oxide sub-word-line driver plane (CIRC-01, DEV-03).**
   - The pass TFT is overdriven, so the WL level comes from silicon rails and Vt drift shows up only as edge time (~8% per 0.1 V).
   - An active clamp per WL holds unselected WLs at ≤−0.5 V.
   - The drivers take 3.3 mm² (19% of the array), on a dedicated TFT plane.
3. **Shielded two-level global lines (CIRC-02).** α falls from 0.145 to 0.035, and the required signal from 36.6 to 28.0 mV.
4. **Hydrogen-barrier stack plus D-labelled qualification (DEV-01, PROC-04).** It also uses an SiCN bond dielectric.
5. **Contamination clause and encapsulated bond face in the spec (PROC-03).**
6. **Honest cost structure (PROC-02, IND-05, owner correction).**
   - Decks at AR ≤60.
   - Bond line $500 per pair.
   - 1% DBI royalty.
   - Pre-bond screening catches 50% of bad cell dies, because a cell-only wafer cannot be fully tested without sense amps.
7. **The spec now favours the gain-cell (non-destructive) class (CIRC-02/03).** The gain cell keeps 2.60 Gb/mm² and $0.56/GB, and none of the coupling corrections touch it.

**Top-up ideas considered**
- **I-12302 (plate-strip sensing, ~135 mV vs ~14 mV).**
  - In this bond-group architecture, a plate strip needs a local gain FET per 8–64 cells to drive the shared global line. That turns 1T1C into the non-destructive class, which is effectively the gain-cell route (2.60 Gb/mm²).
  - It also meets Micron's planar prior art (US 5,991,216; 8,009,460).
  - Kept as the **1T1C revival path** if measured α or Cs pushes 1T1C below 3×. Not the base case.
- **I-12627 (two series write transistors square the leakage tail).**
  - It applies to the gain-cell variant. Both devices pulse together, so they can share one WL and one predecode output, with no extra WL bonds.
  - Cost: L_gain 250 → 300 nm, giving 2.16 Gb/mm² (4.8×) and $0.68/GB [model variant].
  - The p² gain needs independent defects. Bond-plane hydrogen is a correlated sheet source, so it is **not** counted as a DEV-01 mitigation.
  - Offered to the 2T0C portfolio cell as a retention-tail lever.

**Revised step-change claim.** Assumes a 64-tier portfolio cell; numbers are 1T1C-64 with D2W at 2.0 µm.

| Axis | Revised | Original |
|---|---|---|
| New memory-fab capex | **3.6× less** per GB/month ($17.1 vs $61) | 7.6× |
| EUV layers | **0** (vs 5–7) | 0 |
| $/GB | **0.62× DDR5** ($0.92) | 0.36× |
| Density | 3.6× 1β (1.60 Gb/mm²) | 4.5× |
| Bitline energy | 1.4× lower | 1.8× |

- **Gain-cell variant:** 5.9× capex, 0.38× $/GB, 5.8× density.
- **Attribution:** ~3.3× of the capex factor is tier density, which any in-house 3D DRAM also gets.
- **The bonded split and interface contribute about 1.5× in capex.** That holds only while existing 28 nm logic capacity absorbs the periphery, and only if a NAND-class line beats logic BEOL by ≥$15/tier. On their own, the split and interface are not a step change.
- **Cost break-even** moves to 28 tiers for 1T1C (16 for gain).

**Revised decisive experiment.** Full detail is in §5R.
- **Vehicle:** 4- and 8-tier warped oxide coupons. Each carries mini-arrays, a 196:1 oxide group select and a bootstrapped 1:8 sub-WL driver.
- **Bond:** D2W at 2.0/1.5 µm at a fab-grade partner. W2W runs only if anisotropic warp is ≤40 µm.
- **Original GO items:** opens and bridges (counted on void-free fields), overlay, voids, ΔVt.
- **Measurements the reviewers showed were missing:**
  - D-labelled bond-hydrogen ToF-SIMS with a barrier split;
  - ΔVt on cells **and** TFTs after 3 × 260 °C reflow and 1,000 h at 125 °C;
  - anneal series at 150–300 °C;
  - WL driver level, edge and clamp after stress;
  - oxide-mux R_on, kickback and Vt spread read through the bonds;
  - field-solver α and a ≤4 µm² 28 nm SA Monte Carlo;
  - four-point-bend adhesion and FIB on every failure;
  - VPD-ICPMS;
  - nanotwinned-Cu with 1,000-cycle Kelvin;
  - **RTN/VRT on top- vs bottom-tier devices at ns–µs (select/read path) and second (retention) timescales**, to isolate bond-proximity damage.
- **Cost and timing:** **$795k of experiments** ($740k + $55k contingency; $995k with founder pay), M1–M24, GATE 1 at M14, GATE 2 at M22.

**Revised verdicts**
- **PHYSICALLY POSSIBLE: YES (unchanged).**
  - No physics is violated.
  - New measured risks: bond-plane hydrogen (needs ~1,400–3,500× barrier attenuation; one Al₂O₃ layer has shown ~18×) and an n-only oxide WL driver under Vt drift.
  - Anisotropic warp is solved by D2W.
- **STEP CHANGE IF IT WORKS: YES, but smaller and mostly inherited.**
  - Capital intensity is 3.6× (was 7.6×), with 0 EUV.
  - $/GB is 0.62× (was 0.36×).
  - The gain cell gives 5.9× and 0.38×.
  - The split's own contribution is ~1.5×, conditional.
- **PROVABLE WITH $1M: PARTLY.**
  - Run standalone, $795k settles bond physics, hydrogen, the WL driver, the oxide select, adhesion and contamination on 4/8-tier coupons by M22.
  - It cannot settle a 64-tier cell, deck cost or merchant economics.
  - Inside the portfolio seed (~$60k funded): **NO**, unless a bonding partner contributes in kind.

**FINAL STATUS: DOWNGRADED.**
- **No physics kill.** The bond physics remains cheap to test, and the zero-EUV, U.S.-periphery path stands.
- **The headline factors roughly halve** after the red-team corrections: capex 7.6× → 3.6×, $/GB 0.36× → 0.62×, 1T1C break-even 16 → 28 tiers. The largest single term is deck cost.
- **Most of what remains is tier density** that any in-house 3D DRAM gets; the split itself adds ~1.5×.
- **The merchant/open-interface leg** has no buyer, seller or royalty and is demoted to optional.
- **Two new must-pass device gates** are in place: bond-plane hydrogen and the oxide sub-WL driver.
- **The concept continues as the bond and integration scale path** for whichever portfolio cell (AND-STACK, PIXEL-STACK, DIODE-TOWER, 2T0C) passes.
- **Revival of the full original claim** needs three things: a ≤2-deck 64-tier flow with a ≤$3k cell wafer; a measured NAND-line advantage of ≥$15/tier over logic BEOL; and an LOI pair (cell-wafer maker plus periphery foundry) trading under the spec.
