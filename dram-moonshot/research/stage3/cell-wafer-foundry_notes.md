# CELL-WAFER FOUNDRY: research notes

**Dossier:** `cell-wafer-foundry` (Stage 3, rank 9, EV 36) · **Agent:** `dos-cell-wafer-foundry` · **Date:** 2026-11-02
**Model:** `models/cell-wafer-foundry.py` (pure stdlib, exits 0) → `research/stage3/cell-wafer-foundry_model_output.md`
**Sources:** `research/sources/dos-cell-wafer-foundry.jsonl` (28 entries). Six web searches used out of a quota of six; WebFetch not attempted. Every web fact below came from a search snippet. **Assumptions:** `research/assumptions/dos-cell-wafer-foundry.md`.

Tags: [REPORTED] = search snippet or secondary source; [ESTIMATE] = this model; [UNVERIFIED-training] = from training knowledge, not confirmed in this run (verify before outreach or citation).

---

## 0. Bottom line

1. **The bond physics is not the hard part, at least not in the way the concept framed it.** In the model, random bond-link opens are repairable: with 1% spare bitline groups, die yield stays above 0.9 up to about 6e-3 opens per link. The bond's own capacitance (~0.4 fF) is about 2% of the bitline load. Three things actually bind:
   - **(a) Bridges.** A bridge onto an unswitched global supply kills the die. At the assumed ratios, opens must stay below ~5e-7 per link unless the spec puts domain-switched supplies next to signal pads.
   - **(b) Overlay on bowed multi-tier wafers.** A 5 µm film at 100–500 MPa bows the wafer ~300–1,600 µm. The 1.5 µm pitch overlay budget is 0.375 µm.
   - **(c) Particle voids.** In wafer-to-wafer (W2W) bonding, a 0.5 µm particle unbonds a ~2–3 mm radius.

   The decisive experiment is designed around these three.
2. **1–2 µm bonding is matched to a 22/28 nm periphery, and finer pitch buys nothing.** A 28 nm sense amp of ~2.5 µm² needs about 100–200 vertical bitlines' worth of array above it. So the mux ratio is set by sense-amp (SA) area, not by bond pitch, at any pitch ≤1.5 µm.
3. **If a portfolio cell reaches the tiers, the numbers are strong.** Base case: 1T1C, 64 tiers, F ~40 nm, 1.5 µm bonds.
   - 2.0 Gb/mm² (4.5× 1β) at array efficiency 0.86.
   - Cbl 19.9 fF, needing Cs 1.16 fF with MARGIN STACK's 26 mV threshold.
   - **$0.54/GB, 0.36× DDR5's $1.48/GB.**
   - Zero EUV, against $825–1,155 per wafer at 1c.
   - ~8× less new memory-fab capex per GB/month.
   - Gain-cell variant: 2.6 Gb/mm², $0.41/GB.
   - Cost break-even with 1β comes at only 12–16 tiers.

   All of this is conditional on the cell reaching that tier count. That risk belongs to the cell, not to the bond.
4. **The honest weak point is the null hypothesis, not physics.** Oxide cells are BEOL-compatible, so they could be built directly on the periphery wafer as monolithic CMOS-under-array (CuA), with no bond at all.
   - The bonded split costs ~$800 more per wafer pair.
   - To pay that back, the cell line must process each tier ≥$12.5 cheaper than a logic foundry's BEOL at 64 tiers (42% of a $30 tier), or ≥$6 cheaper at 128 tiers.
   - Otherwise the split must win on tool specialisation, cycle time, thermal or hydrogen freedom, or known-good-die (KGD) selection via die-to-wafer (D2W) bonding.
5. **GO/NO-GO** (from the model). The test vehicle is an 8-tier (~5 µm stressed film) oxide coupon bonded W2W at ≤1.5 µm. GO requires all of:
   - opens ≤1e-5 per link (95% UCL, ≥1e7 links), with no new opens after 500 thermal cycles;
   - bridges ≤1e-7 per adjacent pair;
   - overlay ≤0.30 µm on 100% of dies after backside stress compensation (bow ≤~200 µm);
   - ≥95% void-free dies;
   - after a ≤250 °C anneal, ΔVt ≤20 mV and an 85 °C retention change ≤2×.

   **Cost:** ~$650k of experiments inside a ≤$1M, 24-month standalone plan (§7).

---

## 1. What the model changed in the concept

| Concept claim | Model finding | Consequence for the spec / dossier |
|---|---|---|
| "One bond per bitline group" at 1–2 µm | True, but the group size M ≈ 140–210 is set by **28 nm SA area** (M_SA) at ≤1.5 µm. Bond pitch sets M only at ≥2 µm | Do not chase sub-µm bonding. A 16/12 nm periphery would be needed to use finer pitch |
| Bond parasitics matter (experiment step c) | Pad+via ≈ 0.43 fF = 2–3% of Cbl; Cu resistance < 0.1 Ω | Descope step (c) to an on-chip emulator |
| Mux on the array wafer works for any cell | **Destructive-read 1T1C** can only mux bitlines the active WL does not cross. The group therefore spans M rows (a ~47 µm global line, 7 fF). Non-destructive gain cells cluster freely (Cbl 15.5 vs 19.9 fF) | The spec should favour non-destructive cells (AND-STACK, PIXEL-STACK, 2T0C) or require WL segmentation for 1T1C |
| Bond count = bitline groups | **Word-line bonds** are first-order: 64 tiers × rows. Without on-cell-wafer predecode they outnumber signal bonds. With 1:8 oxide-TFT predecode they are ~20% of bonds | The spec defines a TFT predecode/group-select layer on the cell wafer |
| Needs ≤~1e-5 link failure | Opens are repairable to ~6e-3 with 1% spares. **Bridges** onto global supplies are die-fatal and need opens ≲5e-7 unless supplies next to signal pads are domain-switched | Spec rule: signal pads neighbour only signal or domain-switched supply pads. The test vehicle must have combs as well as daisy chains |
| "A floor that forces >2 µm pitch kills it" (A3) | 1T1C degrades past ~2.5 µm (Cs > 2 fF). Gain cells last to ~3 µm, where WL bonds exhaust the sites | The kill pitch is ~2.5–3 µm, not 2 µm |
| Array efficiency 0.51 → 0.7–0.85 | 0.81–0.91 from 16 to 128 tiers (1T1C), with an 8% staircase and 8% edge/TFT overhead | Supports the concept's claim |
| Periphery moves to "cheap" logic | The 28 nm wafer ($2,800) is **36–64% of pair cost** at 16–128 tiers | A reduced-metal 28 nm periphery flow (~$1.9k) is worth as much as ~30 tiers of cell process |
| Reusable glass carrier (N-36) | Saves ≤$115 per pair (2%) | A resource and prime-wafer win, not a cost win |

---

## 2. Prior art and who is pursuing it

| Who | What | Date | Source | Relation |
|---|---|---|---|---|
| Samsung | 10a 4F² VCT working die, IGZO channel, periphery on a separate wafer W2W hybrid-bonded (PUC), 2028 target | 2026-04-24 | [TrendForce](https://www.trendforce.com/news/2026/04/24/news-samsung-reportedly-produces-sub-10nm-10a-dram-working-die-using-4f-square-and-vct-targets-2028-production/) [REPORTED] | In-house cell/periphery split. Closest incumbent prior art |
| Samsung | VS-DRAM, 16 tiers, GAA lateral 1T1C, peri-on-cell bonding (VLSI 2026 T5.1) | 2026-06 | A3 §2.9 cross-ref [REPORTED] | In-house, 3D |
| SK hynix | 4F² VG with die thinning "in wafer-bonded structures" (VLSI 2026 T8.5); 5-tier 3D DRAM at 56.1% yield (VLSI 2024) | 2024–26 | A1/A3 cross-ref [REPORTED] | In-house |
| YMTC | Xtacking: CMOS wafer bonded to array wafer. Interconnect pitch "10 µm and below"; Xtacking 4.0 at 12.66 Gb/mm² | 2025–26 | [Yole](https://www.yolegroup.com/product/report/nand-comparison-2026/), [TechInsights](https://www.techinsights.com/blog/ymtc-xtacking40-breaking-new-ground-3d-nand-technology) [REPORTED] | NAND, in-house; production bond pitch reference |
| Kioxia/WD | CBA (CMOS bonded array), BiCS8 218L; first IDMs after YMTC to hybrid-bond NAND in volume | 2024–26 | Yole [REPORTED] | NAND, in-house |
| UniIC / XMC | SeDRAM: DRAM wafer Cu-Cu stacked on a logic wafer of another node, 0.88 pJ/bit; two SoCs in production (company claim) | n.d. | [XMC](https://xmcwh.com/en/site/details/300?details=1) (stage-2 log) [REPORTED] | **Closest cross-node precedent** (DRAM wafer + logic wafer from different nodes), but a whole-die interface, not bitline-level |
| imec | W2W at 1.08 µm pitch, daisy chains of 70,866 links; "high yield" for 5–1 µm across 300 mm | n.d. | [imec](https://www.imec-int.com/en/articles/wafer-wafer-hybrid-bonding-pushing-boundaries-400nm-interconnect-pitch) [REPORTED] | Bond-process benchmark |
| imec | W2W at 300 nm pitch, high electrical yield on large daisy chains (ECTC 2025) | 2025 | [imec pubs](https://www.imec-publications.be/entities/publication/6228fcc8-685e-4e72-83ba-3cb478415500) [REPORTED] | Benchmark |
| imec + EV Group | W2W at 200 nm pitch; overlay < 40 nm on 100% of dies over 300 mm (ECTC 2026), on flat logic test wafers | 2026-05-28 | [EVG PR](https://www.evgroup.com/fileadmin/media/company/news/2026/2026_05_28_IMEC/Press_Release_IMEC_EVG_2026_05_28_EN.pdf) [REPORTED] | Best overlay, but on flat wafers |
| imec | D2W at 2 µm: Kelvin e-yield > 85%, daisy-chain e-yield > 70% | n.d. | [Electronic Specifier](https://www.electronicspecifier.com/?p=32321) [REPORTED] | D2W/KGD route benchmark |
| TSMC / Intel | SoIC pitch 9 → 6 µm; Foveros Direct shipping in Clearwater Forest (1H26) | 2026 | [Tom's Hardware](https://www.tomshardware.com/tech-industry/semiconductors/hybrid-bonding-roadmap-examined) [REPORTED] | Production logic hybrid-bonding pitch |
| Patents | US 10,340,261: a memory chip holding only cell arrays, hybrid-bonded to a logic chip holding SAs and word drivers, with a pitch-conversion layer | granted (date not checked) | [Google Patents](https://patents.google.com/patent/US10340261) [REPORTED, stage-2 log] | **Blocking-risk prior art for the generic split** |
| Patents | US 11,430,766 (DRAM array and periphery on separate wafers, hybrid-bonded); US 11,114,453 (memory array face-to-face with periphery, separate processes); US 11,094,653 (W2W overlay tolerance) | granted | USPTO via A3 / stage-2 logs [REPORTED] | Prior art |
| Adeia (ex-Xperi/Ziptronix) | DBI hybrid-bonding portfolio (>14,250 assets). Licensees: Micron (2022), Kioxia/WD (2023), AMD (Mar 2026, after litigation) | 2022–26 | [Business Wire](https://www.businesswire.com/news/home/20220222006259/en/Xperi-and-Micron-Enter-Into-License-Agreement-for-Hybrid-Bonding), [MarketBeat](https://www.marketbeat.com/instant-alerts/adeia-q2-earnings-call-highlights-2026-08-03/) [REPORTED] | Freedom-to-operate gate for any hybrid-bonded product |
| Lithography | MIT SBIL Nanoruler; Eulitha displacement Talbot; Canon NIL trialled by SK hynix and Kioxia | various | B2-12 / I-07130 cross-refs | Optional patterning of periodic layers (N-31) |
| Open-interface analogues | UCIe (die-level); OpenRAM; OpenGCRAM (Stanford 2025); LiteDRAM | 2022–25 | stage-2 critiques | None defines a bitline-level memory interface |

**What is genuinely new here:**
1. An **open, cross-line, bitline-group electrical and mechanical bond spec**. No published spec was found in A3 or Stage 2, or in this run's searches.
2. The spec content this model derives:
   - SA-area-matched pitch;
   - non-destructive-cell preference, or WL segmentation;
   - a TFT word-line predecode layer;
   - a domain-switched supply adjacency rule;
   - a bow and anneal budget;
   - bond-link BIST and remap.
3. **Hybrid bonding of warped multi-tier oxide memory stacks.** Two searches found no published bow-aware hybrid-bond yield data for such stacks. The 3D NAND warpage literature is the nearest.

---

## 3. Best demonstrated numbers per component

| Component | Best number | Source | Need (model) |
|---|---|---|---|
| W2W pitch (research) | 200 nm, "highly yielding" | imec/EVG 2026-05-28 [REPORTED] | 1.0–2.0 µm |
| W2W overlay | < 40 nm on 100% of dies (flat wafers) | imec/EVG 2026 [REPORTED] | ≤ 0.30–0.375 µm on bowed multi-tier wafers |
| Daisy chain at ~1 µm | 70,866-link chains, low R, at 1.08 µm | imec [REPORTED] | ≥1e7 links/wafer measured; opens ≤1e-5 |
| D2W at 2 µm | Kelvin > 85%, daisy > 70% | imec [REPORTED] | — (shows D2W is less mature than W2W) |
| Production bond pitch | TSMC SoIC 6 µm; YMTC Xtacking ≤10 µm | Tom's HW; Yole [REPORTED] | 1.5 µm (≈4× finer than production logic) |
| Bonded-wafer warpage | a few µm to > 100 µm, ~10 µm after run-out compensation | YAP+ arXiv 2511.05506 [REPORTED] | — |
| 3D NAND wafer bow | +300 to −550 µm; warpage causes voids and weak bonds | SPIE 11326; Nova 2025 [REPORTED] | ≤ ~200 µm after compensation |
| Low-temperature bonding | Cu/SiCN bonding at 180 °C with O₂ plasma | Seoul Tech 2024 [REPORTED] | ≤ 250 °C anneal |
| Room-temperature SAB | Ar-beam activated Cu-Cu with no anneal | B3-20 cross-ref (Suga) [REPORTED] | Fallback for drift-sensitive cells |
| IGZO thermal sensitivity | Recovery anneal > ~300 °C rearranges bonding; S/D metal diffusion shifts Vth | KIEEME 2016 [REPORTED] | ΔVt ≤ 20 mV post-bond |
| Multi-tier oxide FETs on 200 mm | 3 tiers of ALD In₂O₃ FETs, > 100k devices on 52 dies | Purdue 2026-09-16 [REPORTED] | 4–8-tier coupons |
| Oxide cell | OCTRAM 275 Mb, Ion > 15 µA, Ioff < 1 aA; IMECAS 4-layer 2T0C, 3 b/cell, 400 s; imec 2T0C > 200 s at 95 °C, > 1e12 cycles | A3 cross-refs [REPORTED] | A portfolio cell at ≥16–64 tiers |
| 28 nm periphery wafer | ~$2,800 ($1.9–3.45k) | ram-venture v4-cost, Silicon Analysts [REPORTED] | — |

---

## 4. Model headline numbers (`models/cell-wafer-foundry.py`)

| Quantity | 1T1C, 64 tiers, 1.5 µm | Gain cell, 64 tiers, 1.5 µm | 1β DDR5 |
|---|---|---|---|
| Cell footprint per tier | 0.0258 µm² (80 × 323 nm; lateral cap 123 nm) | 0.0200 µm² | 0.00107 µm² (6F²) |
| Mux ratio M (limiter) | 146 (SA area) | 205 (SA area) | n/a |
| Cbl | 19.9 fF | 15.5 fF | 35 fF |
| Required Cs / read time | 1.16 fF at 26 mV (2.1 fF at 50 mV) | 0.78 ns to 100 mV at 2 µA | 5.4 fF |
| Die (32 Gb) / array efficiency | 15.9 mm² / 0.86 | 12.3 mm² / 0.86 | — / 0.51 |
| Density | **2.01 Gb/mm² (4.5×)** | **2.60 Gb/mm² (5.8×)** | 0.447 |
| Bitline energy per sensed bit | 11.0 fJ | 8.6 fJ | 19.3 fJ |
| Bonds per die | 3.6e6 signal + 0.85e6 WL | — | — |
| $/GB (W2W; $30/tier, $2.8k periphery) | **$0.54 (0.36×)** | **$0.41 (0.28×)** | $1.48 |
| $/GB at $45/tier · at $1.9k periphery | $0.63 · $0.46 | $0.48 · $0.35 | — |
| Cost break-even tiers | 16 | 12 | — |
| New memory-fab capex | ~$8 per GB/month | — | ~$61 per GB/month |
| EUV layers | 0 | 0 | 5–7 at 1c |

**Sensitivity on the key unknown** (model §7, 1T1C, 64 tiers, 1.5 µm):

| Opens per link | Supplies next to signal pads: die-yield factor / $/GB | With the spec rule (domain-switched supplies): die-yield factor / $/GB |
|---|---|---|
| 1e-6 | 0.89 / $0.60 | 1.00 / $0.54 |
| 1e-5 | 0.33 / $1.65 | 1.00 / $0.54 |
| 1e-4 | ~0 / > $100 | 1.00 / $0.54 |

With the spec rule, the cliff is at spare exhaustion (~6e-3). Particle density on the pre-bond surface matters too:
- 0.05 /cm² → W2W void yield 0.97;
- 0.5 /cm² → 0.73 (D2W 0.94);
- 2 /cm² → 0.24 (D2W 0.73).

**Bow:**
- Stoney's formula gives 311 µm of bow for 5 µm × 100 MPa and 1,557 µm for 500 MPa.
- Flattening run-out is Δ = bow × thickness / radius. That is 1.6 µm at 311 µm of bow.
- After 90% scaling compensation, 0.16 µm remains, which fits the 0.375 µm budget. At 25% residual, the tolerable bow drops to ~290 µm.

**Thermal dose:**
- 250 °C for 2 h ≈ 0.09–0.36 years at 85 °C (Ea 0.58–0.72 eV).
- 350 °C for 16 h ≈ 5–37 years.

---

## 5. U.S. facilities that could build the demo

| Facility | Relevant capability | Role in the demo | Cost / rate info | Status |
|---|---|---|---|---|
| **SkyWater Center for NeoVation** (Osceola County / Kissimmee, FL; county-owned, SkyWater-operated) | SUSS XBC300 Gen2: 200/300 mm, W2W plus collective and sequential D2W hybrid bonding | **Primary bonding partner**: pre-bond CMP/clean, bond-layer damascene, W2W and D2W, anneal splits | No public rate found; budget $280k [ESTIMATE] | Tool [REPORTED: SUSS]; service terms unverified |
| **NY CREATES, Albany NanoTech** (300 mm) | 300 mm R&D line; 2025 memory JDA with Fraunhofer IPMS | Alternative bonding/CMP partner; possible 300 mm coupon fab | Not found | JDA [REPORTED]; bonding capability [UNVERIFIED-training] |
| Applied Materials META Center (Albany) | Materials/process co-development | Bonding-surface and CMP process partner | Not found | [UNVERIFIED-training] |
| Adeia DBI lab (Research Triangle Park, NC) | Licensor of DBI/ZiBond hybrid bonding | Licence plus technical consult | Licence terms unknown | Licensing [REPORTED]; lab access [UNVERIFIED] |
| MIT Lincoln Laboratory Microelectronics Lab (200 mm) | 3D wafer-scale integration heritage | Government lab; collaboration route only | n/a | [UNVERIFIED-training] |
| Texas Institute for Electronics (UT Austin) | DARPA NGMM 3D heterogeneous-integration prototyping | Later-stage prototyping partner | n/a | [UNVERIFIED-training] |
| **Purdue Birck Nanotechnology Center** | 3 tiers of ALD In₂O₃ FETs on 200 mm, > 100k devices | **Coupon fab**: 4- and 8-tier oxide/metal stacks with test FETs and cells, 200 mm | Sponsored research plus user fees; budget $170k [ESTIMATE] | Capability [REPORTED, Purdue 2026-09-16] |
| Stanford SNF; Cornell CNF; MIT.nano; Penn Singh; Georgia Tech IEN; ASU; UT Austin | 100–200 mm academic fabs, ALD, metrology | Device-level IGZO/In₂O₃ learning, metrology, small-sample anneal/Vt studies. Not for 300 mm-grade bonding surfaces (particles, per model §5) | Academic rates are typically ~$50–150/h, with industrial users charged more [UNVERIFIED-training] | — |
| Sandia MESA / CINT | 200 mm trusted fab; HfO₂ FeRAM integrated into MESA CMOS (2026) | Possible 200 mm coupon or periphery-emulator partner; CINT user proposals | Proposal-based | MESA FeRAM [REPORTED, stage-2 log]; bonding [UNVERIFIED] |
| Argonne CNM, ORNL CNMS, LBNL Molecular Foundry, NIST CNST | Characterisation (TEM, XPS, ToF-SIMS for H profiles), some fab | Failure analysis of failed links; hydrogen redistribution after anneal | Generally no fee for non-proprietary user proposals; cost-recovery for proprietary work [UNVERIFIED-training] | — |
| MPW: ChipFoundry sky130; wafer.space GF180; MOSIS 2.0 | Shuttles: ChipFoundry $15k per 100 chips; wafer.space Run 2 full slot up to 1,000 dies; MOSIS 2.0 has > 35 shuttles at 12–350 nm and a GF partnership | Sense-amp and bond-emulator chips for step G (shared MARGIN STACK MPW). Not needed for the decisive bond test | As listed | [REPORTED, ram-venture logs] |
| Test / failure analysis | Semi-auto probe station (bought used), SMU and switch matrix; FIB/TEM at a university MCL or NIST | In-house daisy-chain, comb and Kelvin testing | Used probe station ~$30–60k [UNVERIFIED-training] | — |

**Key facility risk (model §5):** a W2W void from one particle spans millimetres. University-fab surfaces must therefore pass through the bonding partner's CMP and post-CMP clean. A D2W split hedges the particle risk and tests the KGD route.

---

## 6. Collaborators and recruits

All group attributions are [UNVERIFIED-training] unless noted. Verify before outreach.

- **Purdue:** Peide Ye (ALD In₂O₃ transistors, BEOL 3D stacking). The 2026-09-16 Purdue 3-tier In₂O₃ result is logged [REPORTED], but the snippet did not name the PI. Best fit for the coupon fab.
- **Georgia Tech:** Shimeng Yu (oxide-semiconductor 3D DRAM, monolithic 3D benchmarking); Muhannad Bakir (fine-pitch 3D heterogeneous integration); Suman Datta (oxide/ferroelectric devices).
- **UCLA CHIPS:** Subramanian S. Iyer (fine-pitch Cu-Cu, Si-IF, chiplet interface standardisation). A natural ally for an open bond spec.
- **Stanford:** H.-S. Philip Wong and Subhasish Mitra (monolithic 3D, SkyWater 3DSoC heritage); Krishna Saraswat.
- **RPI:** James J.-Q. Lu (wafer bonding and 3D integration). **NC State:** Paul Franzon (3D IC design, early DBI collaborations).
- **MIT:** Mark Schattenburg, Space Nanotechnology Lab (SBIL/Nanoruler), for the optional interference-lithography (N-31/I-07130) path.
- **Recruit profile (the device/circuit co-founder):** an integration engineer who has run hybrid-bond test vehicles in production or advanced R&D. Candidate backgrounds: imec 3D program, Sony stacked CIS, YMTC/Kioxia CBA, Intel Foveros Direct, Micron HBM. Must own daisy-chain, comb and overlay-vernier design plus bow management. A DRAM periphery circuit designer is the second hire, after the raise.

---

## 7. Decisive experiment: design, budget and timeline

**Objective.** Measure the four things the model says bind, on the stack the concept actually needs:
- bond-link opens and bridges;
- overlay on bowed multi-tier wafers;
- particle voids;
- the anneal-induced oxide Vt shift.

The stack is warped 4- and 8-tier oxide/metal coupons with real oxide FETs and cells in the tiers, at 1.0, 1.5 and 2.0 µm pitch.

**Step by step**
1. **Spec v0.1 (M0–3).** Covers:
   - bond grid (1.5 µm baseline; 1.0 and 2.0 µm alternates), pad = 0.5 × pitch, SiCN/SiO₂ dielectric, Cu recess window;
   - signal classes: bitline group, WL predecode, group select, domain-switched supply;
   - electrical envelope: Cbl window 10–30 fF; Cs ≥ 1 fF (1T1C) or I_read ≥ 1 µA (gain cell); VPP ≤ 3.0 V; negative hold bias;
   - bond-link BIST and remap protocol;
   - bow ≤ 200 µm; post-bond thermal budget ≤ 250 °C for 2 h;
   - test pads and alignment marks.
2. **Test-vehicle design (M1–4).** One reticle at three pitches, containing:
   - daisy chains of 1e3, 1e4 and 1e5 links (resolving 1e-7 to 1e-3);
   - Kelvin 4-wire links;
   - pad-to-pad combs next to signal and "supply" pads (≥ 3e7 adjacent pairs, ~34 mm² at 1.5 µm);
   - electrical overlay verniers at die centre, mid-radius and edge;
   - coupon tiers carrying In₂O₃/IGZO FET arrays and 1–4 kb 2T0C/1T1C mini-arrays, plus stress monitors.
3. **Coupon lot 1 (M3–8), Purdue, 200 mm.**
   - 4-tier oxide/metal stack (~2.5 µm of films) with test FETs in tiers 1 and 4.
   - Backside SiN stress-compensation split at 0%, 50% and 100%; wafer-shape maps.
   - Pre-bond Vt, Ioff and 85 °C retention baseline.
4. **Periphery-emulator wafers (M4–8), bonding partner.** Cu-damascene daisy-chain bottom halves on 200 mm Si in SiCN (2–3 masks). A real 28 nm periphery wafer is not needed: the model shows bond parasitics are irrelevant to the sense margin.
5. **Bond layer on the coupons (M6–9), partner.** ILD, Cu pads, CMP to the recess spec, post-CMP clean, particle inspection.
6. **Bond lot 1 (M8–10).**
   - W2W, 6 pairs, anneal splits at 200, 250 and 300 °C for 2 h.
   - A D2W split (diced coupon dies onto an emulator wafer).
   - IR alignment metrology; CSAM void maps.
7. **Thinning and pad reveal (M10–11).**
8. **Test (M11–14).**
   - ≥ 1e7 links and ≥ 3e7 comb pairs per wafer.
   - Kelvin resistance distribution.
   - Overlay map against the bow map.
   - Post-bond FET Vt and cell retention.
   - 500 thermal cycles (−40/125 °C) on half the dies.
   - FIB/TEM on failures.
   - Under the 95% UCL test, 1e7 links pass with ≤ 83 opens (model §8).
9. **GATE 1 (M14).** Apply the GO/NO-GO thresholds to the 4-tier results and choose the 8-tier recipe (compensation, anneal).
10. **Coupon and bond lot 2 (M14–20).**
    - 8-tier stack (~5 µm stressed films), best compensation and anneal, best pitch plus 1.0 µm.
    - Repeat steps 6–8.
    - Add 2T0C/1T1C mini-arrays routed through the bonds to emulator pads, sensed with an external SA board.
11. **Sense-margin emulation (M16–22).** On the shared MARGIN STACK 22/28 nm MPW, an SA with a programmable Cbl and bond-parasitic emulator (0–2 fF). Confirms model §4.
12. **Spec v1.0 and data room (M20–24).** Publish the measured envelope (bow, overlay, opens, bridges, anneal ΔVt), file the PCT, raise.

**Budget (standalone; lean founder pay included)**

| Item | $ |
|---|---|
| A. Spec v0.1/v1.0, model, test-vehicle layout (KLayout and open tools), open-spec licence template | 25,000 |
| B. Masks: coupon contact/stepper layers (Purdue) plus 3 i-line/KrF bond-layer reticles (partner) | 45,000 |
| C. Coupon fabrication, Purdue Birck: sponsored research (one student/postdoc for ~12 months) plus user fees, 2 lots at 200 mm | 170,000 |
| D. Bonding partner (SkyWater NeoVation or NY CREATES): CMP/clean, bond layers on both wafers, 2 W2W lots of 6 pairs with anneal splits, 1 D2W lot, IR overlay, CSAM, thinning and pad reveal | 280,000 |
| E. Electrical test: used semi-auto probe station, probe cards, SMU and switch matrix; thermal-cycling chamber time | 55,000 |
| F. Failure analysis: ~15 FIB/TEM lamellae, SEM cross-sections, ToF-SIMS hydrogen profiles | 25,000 |
| G. Sense-margin emulation: share of the MARGIN STACK MPW plus emulator board; D2W microbump of mini-arrays | 50,000 |
| H. IP: 3 provisionals plus 1 PCT | 30,000 |
| I. Spec and standards: OCP/JEDEC engagement, travel, patent-pledge drafting | 20,000 |
| **Experiments subtotal** | **700,000** |
| J. Founder pay (2 × $50k/yr × 2 yr, lean) | 200,000 |
| K. Contingency (~13% of experiments) | 90,000 |
| **Total** | **990,000** |

Within the portfolio plan (FINAL_CONCEPTS: ~$735k of seed experiments across all concepts), only items A, H and I (~$75k) are seed-funded. Items B–G become a raise milestone, partner-funded, or grant co-funded. NSF SBIR Phase I goes up to $305k (aggregator snippet logged in ram-venture). CHIPS-funded consortium programs are another route.

**Timeline (24 months)**

| Months | Work | Gate |
|---|---|---|
| 0–3 | Spec v0.1, model, partner agreements, provisionals 1–2 | Partner quote ≤ $300k |
| 1–4 | Test-vehicle layout and masks | — |
| 3–8 | Coupon lot 1 (4-tier) plus stress-compensation split; emulator wafers | Bow ≤ 200 µm after compensation |
| 8–11 | Bond lot 1 (W2W and D2W), thin and reveal | Void-free dies ≥ 95% (CSAM) |
| 11–14 | Electrical test, thermal cycling, failure analysis | **GATE 1 (M14):** opens ≤ 1e-5, bridges ≤ 1e-7, overlay ≤ 0.30 µm, ΔVt ≤ 20 mV |
| 14–20 | Coupon and bond lot 2 (8-tier, ~5 µm films) | **GATE 2 (M20):** GO/NO-GO on the 8-tier stack |
| 16–22 | Sense-margin emulation on the shared MPW | Bond-parasitic sensitivity < 5% of margin |
| 20–24 | Spec v1.0, PCT, data room, raise | — |

---

## 8. IP landscape

**Patents to watch**
- **US 10,340,261.** A cell-array-only memory chip bonded to a logic chip with SAs and word drivers, plus pitch conversion. The broad split is likely covered or anticipated. Read the claims before filing anything generic. Assignee and dates were not checked in this run.
- **US 11,430,766; US 11,114,453; US 11,094,653.** Separate-wafer DRAM array and periphery bonding; W2W overlay-tolerance structures.
- **Adeia DBI/ZiBond.** Foundational hybrid-bonding patents, actively licensed (Micron 2022, Kioxia/WD 2023) and enforced (AMD suit, then licence, Mar 2026). Any commercial hybrid-bonded product needs either a licensed bonding supplier or a direct licence. R&D at a partner is lower risk, but get counsel to confirm.
- **Samsung VCT/PUC, SK hynix VG, YMTC Xtacking (incl. bonded-DRAM families), Kioxia CBA.** Large in-house portfolios on array/periphery bonding. Monitor for claims on bitline-level bond grids and segment repair.
- **MIT SBIL; Eulitha DTL; Canon NIL.** Only relevant if the optional interference/imprint patterning path (N-31) is pursued.

**What to file (implementation claims, narrower than the generic split)**
1. **Bond-grid co-design.** A mux ratio set by periphery SA area. Cross-row grouping of vertical bitlines for destructive-read cells, and free clustering for non-destructive cells.
2. **Domain-switched supply adjacency.** No unswitched global supply pad neighbours a signal pad, so a bridge becomes a repairable domain loss. Combined with a bond-link BIST and remap protocol.
3. **On-cell-wafer oxide-TFT word-line predecode and group select**, sized to the bond-site budget.
4. **Stress-compensated multi-tier oxide cell wafers for hybrid bonding.** A backside film recipe co-specified with a bow target and a ≤ 250 °C post-bond thermal budget, and a pre-bond drift-characterisation method that predicts post-bond Vt shift (Arrhenius dose accounting).
5. **The periodic cell array as a large-area moiré overlay target** for W2W bond alignment and metrology (ties to N-31/I-07130).
6. **Strategy.** Publish the spec under an open licence with a royalty-free or FRAND patent pledge for spec-compliant implementations (the UCIe/OCP model). Keep implementation patents (items 1–5) for licensing.

---

## 9. Open gaps

1. **No published data on hybrid bonding of warped multi-tier oxide memory stacks.** Two searches found only 3D NAND bow and overlay papers and flat-wafer imec results. This is exactly what the experiment measures.
2. **No published per-link failure rate for W2W at 1–2 µm**, only "high yield" daisy chains. The opens/bridges split and the bridge ratio (0.1) are estimates.
3. **Residual non-linear run-out (f_res)** after scaling compensation on 300–800 µm-bowed wafers is unknown. The model's 10% is a guess: 25% halves the tolerable bow.
4. **Facility access and pricing.** NY CREATES, the META Center, TIE and MIT LL bonding access were not verified. No bonding-service quote exists. The SkyWater NeoVation SUSS tool is the only sourced U.S. 200/300 mm hybrid bonder found.
5. **28 nm SA area (2.5 µm²) and 3 V WL drivers in 22/28 nm thick-oxide devices** are estimates. A layout study (~1 week) would firm up M. A 1–5 µm² SA range moves density by 3.9–5.0×.
6. **Tier cost ($30/tier) and 0.998 repaired tier yield** come from A1 (low confidence). They dominate $/GB more than anything bond-related.
7. **The monolithic CuA null hypothesis.** A fab-cost model is needed comparing a NAND-class dep/etch line with logic-foundry BEOL per tier. Without a ≥ 20–40% per-tier advantage, or a thermal/H₂ or KGD reason, a foundry will prefer to build the oxide stack on its own periphery wafer, and the merchant split loses.
8. **No direct measurement of IGZO/In₂O₃ Vt shift from a hybrid-bond anneal** (search found none). The 85 °C equivalent dose is inferred from Ea 0.58–0.72 eV (B3-20).
9. **Adeia licence terms** for a startup or for an open-spec ecosystem are unknown.
10. **Incentives.** Whether any incumbent or foundry would source merchant cell wafers is a business question. The mission says not to kill on it, but it shapes the scale path.

**Kill / revival.** The concept dies only if bowed multi-tier oxide wafers cannot reach ≤ 0.5 µm overlay or ≤ 1e-6 bridges at ≤ 2.5–3 µm pitch after compensation. Revival: D2W/KGD bonding of smaller dies (die-level bow scales with die size squared), room-temperature SAB, or a thinner tier stack per bonded layer.
