# B2 notes: new materials and low-resource fabrication

**Agent:** `B2-materials` · **Written:** 2026-11-01 · **Phase:** B (divergent ideation), lens 2 of 5

**Files**
- Cards: `research/phaseB/B2-materials.json` (20 ideas, validated with python3).
- Model: `research/models/B2_materials_estimates.py` (stdlib; `python3` exits 0). Every number in the cards comes from it or from a cited source.
- Sources: `research/sources/B2-materials.jsonl` (47 entries, all via search snippets).
- Assumptions: `research/assumptions/B2-materials.md`.

**Evidence grade.** I used 15 of my 15 searches and made no fetches. Web facts are snippet-level `[REPORTED]`. My arithmetic is `[ESTIMATE]`. Facts I knew without a URL are `[UNVERIFIED-PK]`. Phase A sources reused without re-opening are `[CROSS-REF]`.

---

## 1. How I aimed the lens

Phase A says geology is not the constraint (A2 §0). The real constraints are:
- capital and cleanroom time per bit;
- use-phase (refresh) energy;
- EUV;
- concentrated chokepoints: Ga, Hf, Ru, Ge, Sc, W, PFAS and helium.

A1 says the master physics wall is the storage capacitor (#1), followed by the lack of a 3D cell (#2), the leakage tail (#3) and litho-bound capital (#4).

So I asked one question per bottleneck: **which material or process change removes the scarce input or the expensive step, without making the physics worse?** That produced four families:

| Family | Cards | Bottleneck attacked |
|---|---|---|
| Capacitor without the 60:1 plasma etch or scarce electrodes | B2-01 AAO mold, B2-02 SnO2-templated rutile, B2-03 Hf-free MPB, B2-04 capacitor-first perovskite, B2-05 proton EDL, B2-06 flat AlBN | A1 #1, A2 Ru/Hf/Sc/PFAS |
| Abundant-element oxide transistors and circuits in BEOL | B2-07 Ga-free ZTO, B2-08 in-tier oxide CMOS sense amps | A2 Ga chokepoint, A1 #10/#7 |
| Bits by deposition and cheap patterning | B2-09 Ge-free NAND-line 3D, B2-10 carbon mold, B2-11 DSA, B2-12 NIL, B2-13 interference litho, B2-14 ASD, B2-15 defect-tolerance, B2-20 self-assembled tiers | A1 #2/#4, A2 EUV/Ge/PFAS |
| Where and on what it is built | B2-16 memory inside the logic BEOL, B2-17 glass-carrier BEOL-only line, B2-18 trailing-node fab reuse, B2-19 panels | A2 capital/cleanroom, wafers/HPQ, A1 #5/#6 |

**One cross-cutting insight drives several cards.** Every 2026 next-generation DRAM program already bonds the periphery wafer to the cell wafer (A3 §2.9). Once that is true, the cell wafer contains **only perfectly periodic arrays**. Periodic-only patterning is exactly what nanoimprint (B2-12), interference lithography (B2-13), DSA (B2-11) and anodic self-ordering (B2-01) do well and what they fail at for logic. B2-15 (designed-in defect tolerance) is the glue that lets those higher-defectivity processes in.

## 2. The three most exciting

1. **B2-16: main memory inside the logic die's own metal stack.**
   - *Claim.* 3 bits × 8–16 tiers of oxide gain cells at F = 40 nm gives 0.76–1.52 Gb/mm², which is **76–152 GB over an 800 mm² die**.
   - *Energy.* Interface energy falls from ~3.5 to ~0.2 pJ/bit, saving **211–422 W per accelerator** at 8–16 TB/s.
   - *Cost.* Added cost is ~$0.87/GB at $500 per tier per wafer, with zero extra wafers and no TSVs.
   - *Anchor.* TSMC already embeds an oxide-selector memory fully in BEOL above advanced logic (VLSI 2025). Imec cells hold data >200 s at 95 °C.
   - *Risk.* Compound yield on expensive logic wafers, plus multi-level drift at 95–110 °C.
2. **B2-01: AAO-Cap.**
   - *Mechanism.* Anodize aluminum into a self-ordered, imprint-registered honeycomb of pores at aspect ratio ~100.
   - *Claim.* At 40 nm pitch this gives **Cs 7.4–8.9 fF from 2.5–3 µm cups** (vs 5.4 fF today) with no fluorocarbon HAR etch and no SiN support lattice.
   - *Cost and resources.* About 8 Wh/wafer of anodization energy and 0.19 g of Al.
   - *Risk.* AAO ordering is reported at 40–500 nm intervals, so it fits 4F² at F = 20 nm but not today's 32–35 nm honeycomb.
3. **B2-18: trailing-node fab reuse.**
   - *Mechanism.* Put CMOS under 16–24 tiers of 3–4-bit oxide gain cells at F = 65 nm.
   - *Claim.* **1.8–2.7× 1-beta density and 1.7–3.5× bits per wafer-dollar** (before yield), depending on tier cost.
   - *Where.* Depreciated U.S. 200/300 mm lines, with no immersion, no EUV and no bonding.
   - *Risk.* Shares the multi-level drift risk.

**Runner-up: B2-13, maskless interference lithography.** Two-beam 193 nm immersion fringes reach a 34.5–36 nm half-pitch. Adding one SADP step gives 4F² at F ≈ 17–18 nm, with no masks and no projection lens. Overlay is the bet.

## 3. Biggest physics doubts

- **Multi-level stability in oxide channels** (B2-09, B2-16, B2-18, B2-19).
  - *Why it matters.* The density claims assume 3 bits/cell, which needs ≤~20 mV Vt drift over the refresh interval at 85–110 °C. PBTI and hydrogen drift are documented (A3 §2.1).
  - *Evidence so far.* Only single cells or tiny arrays show 3–4 bits.
  - *Fallback.* At 1 bit/cell, B2-18 needs ~27–37 tiers at F = 65 nm just to reach parity.
- **Dielectric leakage of every super-k route** (B2-02, B2-03, B2-04).
  - *Key arithmetic.* For a 64 ms Si-BCAT cell, the capacitor dielectric may leak up to ~1e-5 A/cm² at the stored bias. That is looser than folklore, and it rescues rutile TiO2 and SrTiO3 for conventional DRAM.
  - *The catch.* For a 10 s oxide-channel cell the spec is ≤~1e-7 A/cm². That has not been shown for rutile or perovskite at EOT ≤0.4 nm.
- **Endurance of wurtzite ferroelectrics** (B2-06). There is a gap of 1.6e5–3.4e9×, which is the most likely kill in this set.
- **Ion transport at storage-level fields** (B2-05). MIT's nanosecond proton motion was measured at ~1 V/nm, roughly 10× the field a DRAM bit would apply.

## 4. Rejected or folded ideas, with revival conditions

| Idea | Why rejected / folded | Revival condition |
|---|---|---|
| Inkjet/printed DRAM (solution-processed oxide TFT memory) | Printed features are ~1–10 µm, so density is 10⁴–10⁶× below 1-beta. Physics allows it, but no tier count closes the gap | Combine printing with imprint at ≤100 nm and ≥64 tiers. That is B2-19, so it is folded there |
| Roll-to-roll flexible DRAM | Overlay on webs is ~µm, and the thermal budget limits ALD quality | Same as above; only for non-DRAM-class niches |
| Display-fab (Gen 6–8.5) IGZO memory at 2 µm rules (ram-venture A1-03) | Killed in ram-venture on density | Revived as B2-19, with density moved into tiers and imprint patterning |
| Hydrothermal (aqueous, 90 °C) ZnO nanowire vertical channels for 4F² | Defect donors and hydrogen in solution-grown ZnO make Ioff ≤1 aA implausible. Solution growth registered at 40 nm pitch is unshown. No search budget left to find evidence | ZnO NW off-current ≤1e-18 A at 20 nm diameter after O3/Al2O3 passivation. Registration via imprinted seed pits |
| DNA-origami / DNA-crystal lithography templates | Defect rates per site (~1e-2–1e-3 [UNVERIFIED-PK]) are 10⁴× above what memory needs, even with B2-15 | Per-site placement defects ≤1e-5 over cm², plus metallization compatible with ALD |
| Colloidal (nanosphere) lithography for hole arrays | Small domains with grain boundaries; no registration | Guided colloidal assembly with ≤1e-5 vacancies; superseded by DSA (B2-11) |
| SiC DRAM (very long retention in 4H-SiC) | Expensive substrate and >1,500 °C processing, the opposite of low-resource | Cheap SiC-on-insulator at 300 mm. More relevant to harsh-environment niches |
| Ti/TiOx ReRAM "abundant" crosspoint | Endurance far from DRAM-class (covered by ram-venture A2) | ≥1e12-cycle filament-free switching |
| Laser or flash crystallization of rutile/perovskite inside BEOL holes | Absorption is at the top surface, so deep holes heat unevenly | Folded into B2-02/B2-04 as a revival path |
| Anodic (electrochemical) growth of Ta2O5/Nb2O5/TiO2 dielectrics in 3D | Possible, but Nb and Ta are concentrated, and ALD already conformal-coats | Folded into B2-01 as an option on Ti |
| W → Mo, Al-only metallization, water-lean cleans, helium recapture | Real but incremental: under ~1% of cost, not a step change (A2) | Kept as resource angles inside B2-14 and B2-01 |
| Cryogenic or 2D-channel DRAM | Covered and downgraded in A3 | Per A3 §6 |
| Poly-Si 3D gain cell | SRH generation in grain boundaries leaks too much (A3 §2.4) | Laser-recrystallized Si with oxide-like leakage. Unlikely |

## 5. Novelty map (honest)

| Novelty | Cards |
|---|---|
| **KNOWN, with a twist** | B2-02 (Gordon/KIST rutile-on-SnO2), B2-07 (UMich ZTO 2T0C), B2-11 (imec DSA), B2-12 (Canon NIL), B2-15 (NAND-style ECC) |
| **TWIST on known** | B2-01, B2-03, B2-06, B2-09, B2-10, B2-14, B2-16 |
| **NEW combination** | B2-04, B2-08, B2-13, B2-17, B2-18 |
| **[SPECULATIVE]** | B2-05, B2-19, B2-20 |

The most defensible new ideas (patentable, with a provable small demo) are:
- **B2-01:** AAO walls as the permanent support lattice of a registered DRAM capacitor array.
- **B2-13:** a production interference litho for a periphery-free cell wafer.
- **B2-08:** in-tier complementary-oxide sense amplifiers.
- **B2-04:** the capacitor-first perovskite flow.

## 6. What a $1M team could prove first (cheapest decisive experiments)

1. **Multi-level retention maps for ZTO and IGZO 2T0C at 85–110 °C** (~$200k). This de-risks B2-07, B2-09, B2-16 and B2-18 at once.
2. **AAO pore-bottom opening and ordering on TiN pads at 40 nm pitch** (~$120k), the first half of B2-01.
3. **SnO2-templated rutile MIM** (~$100–250k). The pass bar is EOT ≤0.40 nm at ≤1e-7 A/cm² at 0.5 V and 85 °C, which decides B2-02 and feeds B2-01.
4. **Fault-injection emulation plus a BCH decoder** on a 28 nm shuttle (~$100k), to set the defect budget for B2-11/12/13.

## 7. Could not verify

- The smallest AAO interval achieved by imprint pretexturing (the snippet gave "typically 40 nm", and the RSC 2017 minimum was not visible).
- Any 2025–26 NIL-for-DRAM status.
- DSA defect density numbers.
- Sub-100 nm panel-scale imprint.
- A Hf-free MPB k value.
- Rutile-on-SnO2 leakage at EOT 0.34–0.40 nm.
- The production landing-pad lithography layer count.
- Tool prices for NIL and IL.
- Any ZTO vertical or 3D gain-cell result.
