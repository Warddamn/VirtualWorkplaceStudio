# DIODE-TOWER: research notes

*Agent `dos-diode-tower`, 2026-11-02. Concept rank 6 (EV 45) in `FINAL_CONCEPTS.md`. Model: `models/diode-tower.py` (pure stdlib; `python3 models/diode-tower.py` exits 0). Model output: `research/stage3/diode-tower_model_output.md`. Sources: `research/sources/dos-diode-tower.jsonl` (6 web searches, snippets only; WebFetch was not used). Assumptions: `research/assumptions/dos-diode-tower.md`. This is a physics judgement, not a business one.*

## 0. Verdict in one paragraph

DIODE-TOWER is alive on physics, and it is harder than the concept card says. The cell side holds up. A 0.27 fF ring capacitor on a 1.0 fF pillar gives 106 mV at 32 tiers, which is z = 5.8 against a 7 mV CDS residual. Density is 1.9x 1-beta at 32 tiers and 3.9x at 64. Cost is ~0.55x and ~0.35x 1-beta $/bit, if tier yield reaches ≥0.998.

The diode is the whole bet, and the model makes it stricter in three ways:
1. **Thin-shell lowering.** A thin, fully depleted IGZO shell puts ~0.9 MV/cm on the anode. Image force plus thermionic-field emission then lower the reverse barrier by ~0.18-0.25 eV at 15 nm, and ~0.35-0.45 eV at 10 nm.
2. **Inhomogeneity tail.** Barrier inhomogeneity (patch σ 0.05 eV) adds ~0.14 eV for the 1e-4 tail tier.
3. **Lower bar for parity.** In the other direction, DRAM-parity retention (64 ms) needs a much lower bar than the concept's 1 s target.

Net result: a tier reaches DRAM parity if the anode shows a **thick-film (low-field) barrier of ≥1.07-1.12 eV with σ ≤ 0.05 eV**. The 1 s refresh-saving target needs 1.17-1.22 eV. The best IGZO Schottky barrier found is ~0.92 eV (thick film, secondary citation). AgOx on single-crystal ZnO reaches 1.00-1.20 eV. So the decisive coupon run is still the right first experiment, and its odds are lower than the card's P = 3 implies. I would score P at 2 (10-25%) for the linear-capacitor version as specified. A geometry escape lowers the bar to ~0.96-0.97 eV, at 3x rather than 3.9x density at 64 tiers: an 80-100 nm hole, a 30-40 nm shell and a wrapped capacitor.

## 1. How the cell has to be operated (refined by the model)

- **Topology.** Each tier has a TiN plate | ZrO2 (5.5 nm) | recessed metal-oxide node ring. The node ring is the Schottky anode.
  - The hole holds an undoped IGZO shell, which is the cathode semiconductor, on an ohmic metal core: the shared pillar.
  - On top sit an IGZO access transistor (pillar to write bitline) and an IGZO gain FET (gate = pillar) with a read select. That is 2-3 transistors per 16-64 bits.
- **Read tier k.** Precharge and float the pillar, sample the gain FET (CDS sample 1), then pulse plate k. Node k rises and dumps its charge through its forward-biased diode. Sample again (CDS sample 2). Signal = Cs·Vdata/(Cs + Cpillar).
- **Write-back = clamp-write in the same plate pulse.** Drive the pillar to the data level while plate k is high. The node discharges to V_pillar + V_f. Drop plate k; the stored level is V_pillar,write + V_f − ΔV_PL. Read and write use the same diode, so diode-to-diode V_f offsets largely cancel.
- **Plate-swing rule (new).** ΔV_PL ≥ Vdata + V_f(cold) + 0.2 V guard.
  - This puts every stored level below the lowest pillar level, so no unselected tier is ever forward-biased.
  - Without the rule, a 0.5 V forward bias on a victim tier loses 100 mV in ~350 (0.9 eV) to ~2e5 (1.1 eV) pillar accesses. That is far fewer than the ~2e7 accesses possible per second.
  - Cost: a ~1.8-1.9 V plate driver. ZrO2 never sees more than ~0.7 V, because the floating node follows the plate.
- **Page = plate segment.** A plate pulse disturbs every pillar on that plate, so every pillar on a plate segment must be read and written back together, or held at an inhibit level (as in the Sogang 1T-nC thesis's VDD/3 inhibit, sources log). The model assumes a slit every 4 rows, which costs 12% of area.
- **Reverse-bias hold.** With stored levels below the pillar, thermionic reverse current moves both states upward almost equally, so the drift is common-mode. A reference tier per pillar (in the model) or a self-referenced read (read, write a known value, read again, as in 1T1C FeRAM) can tolerate up to ~0.45 V of common-mode drift. The tier-to-tier spread in leakage is not cancelled, and that spread sets the spec.

## 2. Prior art and who is pursuing it (with dates)

| Item | Who | Date | Relevance | Source |
|---|---|---|---|---|
| 1TnC FeRAM bit-cell: n stacked FE capacitors on one storage node, each on its own plate line | Kepler Computing (US 11423967, 11527277, 11521667, 12041785, 12096638, 11978762; app 17/339,850 filed 2021-06-04) | 2021-2025 | The closest architecture. Plate-line selection by FE coercivity. US 12096638 claims a generic "N memory element" cell, so its claims must be read for linear capacitors | [Justia 11423967](https://patents.justia.com/patent/11423967); [USPTO 11527277](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11527277); [USPTO 12096638](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12096638) (via search snippets) |
| "Multi-element ferroelectric gain memory bit-cell having stacked and folded non-planar capacitors" | US 11910618 (assignee presumed Kepler [UNVERIFIED]) | unknown | A gain transistor reads a stacked-capacitor shared node, which overlaps DIODE-TOWER's in-pillar gain-FET read. Only the title was seen; read the claims | [USPTO 11910618](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11910618) |
| EP4016625 3D FeRAM plate lines | Intel (per stage-2 critics) | unknown | 1T-nC plate-line prior art | [EPO](https://data.epo.org/publication-server/rest/v1.2/patents/EP4016625NWA1/document.html) [CROSS-REF] |
| 2T-64C FeRAM cell, "hundreds of layer stacking" | Notre Dame / Penn State / IBM / Fraunhofer / NUS | IEDM 2025 | Shows a 64-capacitor shared-node stack can be built | [IBM](https://research.ibm.com/publications/towards-scalable-3d-integration-of-2t-nc-feram-with-hundreds-of-layer-stacking) [CROSS-REF] |
| 1T-nC victim-capacitor disturb, VDD/3 inhibit on 7 nm HZO | Sogang University thesis | 2026 | The shared-node disturb problem that the plate-swing rule addresses for diodes | [Sogang](https://dcollection.sogang.ac.kr/dcollection/srch/srchDetail/000000082483) [CROSS-REF] |
| 32 Gb NVDRAM; CXMT monolithic 3D FeRAM; Georgia Tech two-tier 1T1C | Micron (IEDM 2023), CXMT and GT (IEDM 2025) | 2023-2025 | The FE persistent variant competes here | A3_research_frontier.md |
| 3T micro sense amp on ~32-cell local bitlines | IBM (Barth, ISSCC 2007 / JSSC 2008) | 2007-08 | Local gain-read prior art. 2007-era filings expire around 2027 [ESTIMATE] | [IBM](https://researcher.ibm.com/publications/a-500-mhz-random-cycle-15-ns-latency-soi-embedded-dram-macro-featuring-a-three-transistor-micro-sense-amplifier) [CROSS-REF] |
| Oxide-semiconductor NAND-string gain cells | US 8421071, US 8750023 (Japanese OS patents per critics) | 2010s | Prior art for series-read gain strings | [Google Patents](https://patents.google.com/patent/US8421071) [CROSS-REF] |
| Oxidized-metal ("Schottky-like") contacts to ZnO: Ag, Cu, Ir, Pt oxides in reactive O2 | US 8508015 (inventors and assignee not seen) | unknown | Process prior art for AgOx/PtOx/IrOx anodes. It may bear on how we make the anode | [USPTO 8508015](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8508015) |
| Cross-point diode-selected memories | US 8134194 family; US 5281837 cross-point DRAM (vertical 1T1C) | 1990s-2010s | Diodes are used as sneak-path selectors, but for resistive elements, not capacitors | [USPTO 8134194](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8134194); [Google 5281837](https://patents.google.com/patent/US5281837) |
| **Negative result** | — | 2026-11 | Two targeted searches here, plus both stage-2 critics, found no diode-steered linear-capacitor 1T-nC or 1D1C DRAM. This is not an FTO opinion | sources log entry "none" |

Process neighbours that make the flow credible:
- Micron/Intel floating-gate 3D-NAND recess rings (critics, prior knowledge).
- The IMECAS 4-tier single-step IGZO 2T0C (VLSI 2026, [IT Home](https://www.ithome.com/0/966/543.htm)).
- Kioxia OCTRAM vertical IGZO access devices with Ioff <1 aA ([BusinessWire 2024-12](https://www.businesswire.com/news/home/20241209099702/en/Kioxia-Develops-OCTRAM-Oxide-Semiconductor-Channel-Transistor-DRAM-Technology)).
- imec's 40 nm IGZO 2T0C: >1e12 cycles and <10 ns write at 95 °C ([imec 2025](https://imec-publications.be/entities/publication/948b2190-065d-48d2-a9b9-4f4ecd22c234)).

## 3. Best demonstrated numbers per component

| Component | Need (model) | Best found | Gap | Source / tag |
|---|---|---|---|---|
| Oxide Schottky barrier on IGZO (thick film, low field) | ≥1.07-1.12 eV (64 ms), ≥1.17-1.22 eV (1 s), σ ≤ 0.05 eV, 15 nm shell | 0.92 eV, n = 1.36 (Pt, O2 during deposition, secondary citation); 0.82 eV, n = 1.35, 1e8 rectification (SiO2-passivated); 0.64 → 0.75 eV with O2 and anneal | **0.15-0.3 eV short** | [KIT](https://publikationen.bibliothek.kit.edu/1000121423/82897741); PKU poster; [IEEE Access 2020](https://doaj.org/article/155d5567667543779c9bef95b9e29878) [REPORTED, snippets] |
| Oxide Schottky on ZnO (best of any oxide) | as above | AgOx 1.00-1.20 eV (single crystal); IrOx 0.89 eV Zn-polar vs 0.67 eV O-polar; PtOx on ALD ZnO 0.79 eV effective, n = 1.31, 1.17e7, 550 MHz | Close for AgOx, but on a crystal | [AVS 2008](https://www2.avs.org/symposium2008/Papers/Paper_EM-TuM3.html); [Wright State 2017](https://corescholar.libraries.wright.edu/physics/1493); [Liverpool](https://livrepository.liverpool.ac.uk/3015044/) [REPORTED] |
| Ideality | ≤1.3 (forward V_f budget) | 1.22 (Ti-Pt/IGZO/Cu, 1e8); 1.31-1.36 typical; 1.7 (AgOx/IGZO, 1e9) | OK | KIT secondary citations [REPORTED] |
| Barrier thermal stability | survives ≤400 °C BEOL | Higher Ga content stabilises the Pt/a-IGZO barrier; Ti contacts break down from annealing-induced V_O | Open, but this points to Ga-rich shells | [Sci Rep 2019](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6536494/) [REPORTED] |
| Oxide-Schottky forward cycling | Δφ ≤ 30 meV after 1e12 pulses at ~515 A/cm² | **None found.** Unpassivated IGZO Schottky diodes are unstable in air. a-Si analogy: reverse current rises under medium-bias stress | **Unmeasured** | PKU poster; [MRS 1997](https://www.cambridge.org/core/journals/mrs-online-proceedings-library-archive/article/abs/time-dependence-of-the-reverse-current-in-amorphous-silicon-schottky-diodes/D877540B37303FF67609B6CBC620774A) |
| Linear capacitor per tier | 0.27 fF (back wall) / 0.73 fF (wrapped) | ZrO2 EOT ~0.55 nm in production DRAM | Geometry only | A1_scaling_limits.md |
| Access / gain IGZO devices | Ioff ≪ 27 aA; ns read | Ioff <1 aA (OCTRAM); 1e12 cycles, <10 ns (imec) | OK | [CROSS-REF] |
| Post-CDS residual of an oxide gain FET | ≤7 mV for ≥32 tiers at z ≥ 3.72 (≤10 mV gives 40 tiers) | Not demonstrated for IGZO | Shared unknown with PIXEL-STACK / MARGIN STACK | model §2 |
| Shared-node stack height | 32-64 tiers | 2T-64C fabricated (FE) | Process exists in FE form | [CROSS-REF] |
| Single-step multi-tier oxide stack | ≥4 tiers for the demo | IMECAS 4 tiers, one stacking step | OK for the demo | [CROSS-REF] |

## 4. Model headline numbers (from `diode-tower_model_output.md`)

**Cell geometry**
- 60 nm hole, 15 nm IGZO shell, 15 nm recess, 25 nm plate and 25 nm ILD: Cs 0.27 fF (843 e⁻ at 0.5 V).
- Ring diode 2,639 nm². Each unselected tier loads the pillar by only 0.018 fF, so the pillar is 0.72 / 1.00 / 1.57 fF at 16 / 32 / 64 tiers. That is lighter than the 1.5 fF the concept assumed.
- Pitch 121 nm; footprint 0.0165 µm² including slits, which is 1.5x the concept's 0.011 µm².

**Signal**
- Fresh / end-of-retention signal: 137 / 109 mV at 16 tiers, 106 / 85 mV at 32, 73 / 59 mV at 64.
- z = 7.4 / 5.8 / 4.1 at a 7 mV CDS residual.
- Correction: the concept compared signal/σ with 3.72. The right test is signal/(2σ) ≥ 3.72.

**Density and cost**
- Density parity at 18 tiers; 1.94x at 32 tiers; 2.9x at 48; 3.94x at 64; 3x at 50 tiers. The concept's "2x at 16 tiers" needs a footprint that leaves no room for the recess.
- Cost (base wafer $3,000 + $25/tier, tier yield 0.998): 1.02x 1-beta at 16 tiers, 0.55x ($0.81/GB) at 32, 0.35x ($0.52/GB) at 64.

**Energy**
- 28 fJ/bit per access vs ~46 fJ DDR5-class. Refresh is 4.1 mW/GB at 64 ms vs 6.1 for DDR5-class, and 0.26 mW/GB at 1 s.

**Leakage budget per tier (85 °C, 100 mV droop)**
- 844 aA (32 ms), 422 aA (64 ms), 27 aA (1 s).
- Homogeneous effective barriers needed: 0.80, 0.82 and 0.90 eV.

**Inhomogeneity tail**
- 1e-4 tail multiplier: 6x at σ = 0.03 eV, ~94x at σ = 0.05, ~900x at σ = 0.07, ~3e5x at σ = 0.10.
- The tail penalty is 0.06 / 0.14 / 0.21 / 0.39 eV.

**Thin-shell lowering** (zero-field barrier 1.2 eV, 0.7 V reverse hold)

| Shell | Field | Total lowering (ε_IF 4 / 12) |
|---|---|---|
| 8 nm | 1.9 MV/cm | 0.63 / 0.52 eV |
| 10 nm | 1.5 MV/cm | 0.45 / 0.35 eV |
| 15 nm | 0.9 MV/cm | 0.25 / 0.18 eV |
| 20 nm | 0.55 MV/cm | 0.17 / 0.11 eV |

**Demonstrated contacts mapped into a 15 nm shell** (σ 0.05 tail)
- Best Pt-IGZO (0.92 eV) gives a 0.2-0.8 ms tail retention: fails.
- AgOx/ZnO (1.10 eV) gives 35-140 ms: marginal pass for 64 ms.
- A 1.30 eV contact gives 10-44 s.

**Write**
- At t_w = 10 ns the settling end current is ~1 nA, so V_f ≈ 1.10 V at 0 °C for a 1.12 eV contact. The plate swing is ~1.8 V.
- The average forward current density is ~515 A/cm², far above where IGZO rectifiers are usually characterised.

**Endurance**
- 843 e⁻ per pulse = 5.1e-6 C/cm².
- Refresh-only life (64 ms) = 9.9e9 pulses. Hot row = 1.4e14 pulses.
- A 1e12-pulse test covers refresh-only life ~100x.

## 5. U.S. facilities for the demo

| Facility | Use for DIODE-TOWER | Cost / access info | Tag |
|---|---|---|---|
| Purdue Birck Nanotechnology Center | First choice for the coupon run and the 4-tier stack: oxide ALD (IGZO/In2O3), BEOL ≤400 °C. Purdue ran 3 stacked In2O3 tiers on 200 mm (2026-09) | Industry tool-hour rates ~$75-250 [ESTIMATE] | [Purdue ECE 2026-09](https://engineering.purdue.edu/ECE/News/2026/purdue-researchers-build-3d-chip-platform-for-faster-more-efficient-ai-computing) [CROSS-REF] |
| Georgia Tech IEN | Second fab option; GT built two-tier 1T1C 3D FeRAM (IEDM 2025) | NNCI site, external rates [ESTIMATE $75-250/hr] | A3 [REPORTED] |
| Notre Dame NDnano | 1T-nC / 2T-64C know-how; FE persistent variant | Collaboration | [CROSS-REF] |
| Penn State (MRI/Nanofab) | 2T-64C co-authors; ALD; oxide characterisation | NNCI-class rates [ESTIMATE] | [CROSS-REF] |
| Stanford SNF, Cornell CNF, MIT.nano, Penn Singh Center, ASU, UT Austin | Backup fabs: e-beam for the ring-sized diodes (2,600 nm²), ALD, sputtered RuOx/PtOx/AgOx | $75-250/tool-hour industrial [ESTIMATE]; NNCI user access | ram-venture landscape row 16 [ESTIMATE] |
| Argonne CNM (DOE NSRC) | ALD process development; XPS/UPS work functions; TEM of the anode/IGZO interface (the 2-3 nm interlayer seen in IrOx/ZnO) | Free for non-proprietary work via proposal; proprietary work at full cost [CROSS-REF, ram-venture landscape] | [UNVERIFIED details] |
| Sandia MESA / CINT | MESA runs HZO FeRAM in a trusted 200 mm flow (FE persistent variant partner); CINT is an open user facility | MESA by CRADA/SPP; CINT by proposal | [Sandia 2026-05-13](https://www.sandia.gov/research/news/evolving-semiconductor-technology-for-national-security-applications/) [CROSS-REF] |
| ORNL CNMS, LBNL Molecular Foundry | Interface microscopy and spectroscopy; Foundry thin-film synthesis | Proposal-based NSRC access | [UNVERIFIED-M] |
| NIST CNST | NanoFab (fee-based, open to industry); band-offset metrology (internal photoemission) as a cross-check on barrier height | Fee-based [UNVERIFIED] | training knowledge |
| ChipFoundry sky130 (SkyWater, U.S.) | Optional CDS readout chip or Si sense FETs for post-processing | ~$15k per 100 chips; shuttles slip if <50% full | [eeNews](https://www.eenewseurope.com/en/tiny-tapeout-sees-industrial-boost-as-it-recovers-from-efabless-closure/) [CROSS-REF] |
| wafer.space GF180MCU | Cheapest readout silicon: ~$7-7.5k for up to 1,000 dies; fab is GF Singapore, not U.S. | as stated | [Crowd Supply](https://www.crowdsupply.com/wafer-space/gf180mcu-run-2) [CROSS-REF] |
| MOSIS 2.0 (USC ISI) | 12-350 nm access across >35 shuttles; GF partner | Quote-based | [ISI](https://www.isi.edu/news/80945/mosis-2-0-revives-a-legacy-rehan-kapadia-outlines-a-bold-future-for-rapid-microelectronics-prototyping/) [CROSS-REF] |
| Shared MARGIN STACK 28/22 nm MPW chip (portfolio) | Reads the 4-tier stack with CDS (planned ~$275k at portfolio level) | Shared cost | FINAL_CONCEPTS.md |
| In-house test bench | Probe station with -40 to 150 °C chuck, Keithley 4200A-SCS + PMU, AWG for 1e12 pulses, low-noise CDS board | ~$90k (mix of used and new) [ESTIMATE] | — |

## 6. Collaborators and recruits (named groups)

- **Notre Dame (Kai Ni) and the Penn State / IBM / Fraunhofer / NUS 2T-64C team.** They know how to build a shared-node stack. They are a natural partner for the FE persistent variant and for disturb methodology [REPORTED, A3].
- **Georgia Tech** (two-tier 1T1C 3D FeRAM, IEDM 2025). Group attribution to S. Yu / A. Khan is [UNVERIFIED: training knowledge].
- **Purdue** (stacked In2O3 tiers, 2026). Attribution to P. Ye's ALD oxide-transistor group is [UNVERIFIED]. This is the most likely host for coupon fabrication.
- **Oxide-Schottky physics:**
  - Wright State (D. Look et al., IrOx/ZnO defect-controlled barriers, APL 2017).
  - ASU (Nemanich group, ZnO interfaces).
  - The inventors behind US 8508015 and the AVS 2008 AgOx work (names not seen; [UNVERIFIED]).
  - Abroad, for data and advice: Liverpool/Durham (PE-ALD ZnO/PtOx rectifier), Empa and KIT/Offenburg (sputtered Pt/IGZO diodes; Offenburg author pages surfaced for S. Bolat, X. Feng, F. Rasheed), Peking University (passivated IGZO SBDs, Zhang Dawei).
- **Circuit side.** Ex-IBM eDRAM micro-sense-amp designers (Barth lineage) and image-sensor CDS designers for the gain-FET readout.
- **Process side.** Ex-Micron Boise floating-gate 3D-NAND recess engineers.
- **Recruit profile for the device co-founder.** An oxide-semiconductor contact and reliability physicist with Schottky I-V-T, IPE and ALD experience, plus aA-level floating-node retention metrology (the imec/IMECAS 2T0C measurement style).

## 7. Decisive experiment

### Stage A: go/no-go coupon run (months 0-7)

**A0 (M0-1). Design.**
- Fix the shell thickness and anode list with this model plus open TCAD (DEVSIM, or a university Sentaurus licence).
- Lay out 4 structure types per die (A2).
- File the architecture provisionals before any non-proprietary user-facility work starts.

**A1 (M1-4). Fabricate at Purdue Birck (alternate: GT IEN).**
- Matrix: 5 anodes (RuOx, IrOx, PtOx, AgOx, MoOx) × 3 IGZO shells (10, 15, 20 nm ALD) × 2 compositions (standard and Ga-rich IGZO), plus an amorphous Ga2O3 split. That is 30+ variants on ~12 wafers (100-150 mm).
- Cathode: ohmic Mo or ITO. Anneals at 300, 350 and 400 °C.
- Anodes go **below** the IGZO, matching the tier, where the node is deposited first.

**A2. Four structures per die:**
1. Large-area vertical thin-film diodes (20-200 µm) for I-V-T from -40 to 150 °C, C-V, and the Werner–Güttler plot (apparent barrier vs 1/T, giving mean φ and σ).
2. Parallel arrays of 1e4-1e6 ring-sized diodes (~2,600 nm², e-beam). Average small-area leakage reaches pA at 85-125 °C. This measures the field and size effects directly.
3. ≥1,000 diode-isolated floating nodes: a ring-sized diode, a 1-2 fF MIM capacitor and an IGZO TFT source-follower readout. Retention-time distributions at 85-125 °C resolve ~1e-19 A per node. This is the direct test of the 99.99th-percentile spec.
4. Pulsed-forward stress arrays: 1e10-1e12 pulses at ~500 A/cm², 10-50 MHz, with I-V-T interleaved every decade.

**A3 (M3-7). Measure.**
- In-house bench plus Argonne CNM for XPS/UPS and TEM.
- Optional IPE cross-check (NIST CNST or a university lab).

**A4 (M7). Gate (model §11).**
- **GO** if any anode/shell combination after ≤400 °C passes all three:
  - G1: 99.99th-percentile ring leakage ≤422 aA at 85 °C and 0.7 V reverse. Equivalently, mean tier effective barrier ≥0.96 eV at σ 0.05, or a low-field barrier of 1.07-1.12 eV.
  - G3: ≥0.8 nA forward at ≤1.2 V and 0 °C, n ≤ 1.3.
  - G4: Δφ_eff ≤30 meV after 1e12 pulses.
  - G2 (≤27 aA) is the stretch that adds the refresh-energy win.
- **NO-GO** if no combination passes G1 (including the thick-shell split, which tests the §7b escape geometry), or if Δφ exceeds 60 meV within 1e10 pulses.

### Stage B: 4-tier stack, a raise milestone (months 7-20)

**B1 (M7-14). Iteration 1.**
- A 4-tier stack in 100-200 nm holes: TiN plate / SiO2 ILD × 4, hole, selective TiN recess, ZrO2 ALD, anode ALD, etch-back to isolate rings, IGZO shell ALD, metal core.
- Plus a wrapped-capacitor split (TiN/SiN/TiN tiers).
- On top: an IGZO access TFT and a discrete IGZO gain FET.

**B2 (M12-18). Iteration 2.** Fix what iteration 1 shows, and add 8-tier coupons if 4 tiers work.

**B3 (M14-20). Measurements:**
- clamp-write levels;
- read charge per tier, with CDS from a discrete board or the shared MARGIN STACK chip;
- signal vs added pillar load (emulating 32-64 tiers);
- per-tier retention distribution at 85 °C;
- unselected-tier disturb after 1e9 pillar accesses, with and without the plate-swing rule;
- neighbour-plate coupling;
- 1e12-cycle endurance in the stack.

**Pass for the raise:** a 4-tier tower with ≥80 mV-equivalent signal at 32-tier loading, 1e-4-tail retention ≥64 ms at 85 °C, no disturb failures in 1e9 accesses, and 1e12 cycles.

### Stage C: data package and raise (months 18-24)

Reliability summary, PCT conversions and the $10-50M raise.

### Pivot if Stage A says NO-GO (M7)

The remaining ~$650-700k moves to one of two paths:
- the FE persistent variant on the same tower, with the Notre Dame and Sandia MESA partnership;
- the portfolio's AND-STACK / PIXEL-STACK cells, which share the oxide coupon vocabulary.

### Budget (≤$1M, 24 months)

| Line | $k | Notes |
|---|---|---|
| A0 design and TCAD | 10 | open TCAD; university licence via collaborator |
| A1 coupon fabrication | 100 | ~450 tool-h × $150 + 60 h e-beam × $250 + targets/precursors $15k [ESTIMATE] |
| A3 characterisation | 25 | outside IPE/TEM; Argonne CNM user time free if non-proprietary |
| Test bench (reused in B and C) | 90 | 4200A-SCS + PMU, hot/cold chuck, AWG, low-noise CDS board [ESTIMATE] |
| **Stage A subtotal (decisive)** | **225** | ~$135k excluding the reusable bench, in line with the concept's $80-120k plus Ga-rich and thick-shell splits |
| B1 + B2 4-tier stacks (2 iterations) | 255 | ~1,400 tool-h × $150 + masks $25k + materials $20k [ESTIMATE] |
| Readout silicon and boards | 30 | discrete CDS board; optional wafer.space GF180 slot (~$7.5k) or ChipFoundry sky130 (~$15k) |
| FIB/TEM cross-sections | 25 | recess and ring uniformity |
| C reliability and disturb campaign | 25 | bench time, consumables |
| IP: 3 provisionals, 1 PCT, Kepler-family FTO read | 45 | [ESTIMATE] |
| Founders (2 × $75k/yr lean, 24 months) | 300 | [ESTIMATE] |
| Travel and user-facility visits | 15 | |
| Contingency (~8%) | 60 | |
| **Total** | **980** | under $1M |

### Timeline

| Months | 0-1 | 1-4 | 3-7 | 7 | 7-14 | 12-18 | 14-20 | 18-24 |
|---|---|---|---|---|---|---|---|---|
| Activity | Design, provisionals | Coupon fab | Coupon test | **GO/NO-GO** | Stack iteration 1 | Stack iteration 2 | Disturb, retention, endurance | Data package, PCT, raise |

## 8. IP landscape

**Patents to watch**
- **Kepler Computing 1TnC family.** US 11423967, 11527277, 11521667, 12041785, 12096638, 11910618 [assignee of the last presumed], and 11978762.
  - Read 12096638 first: its title says "N memory element", which may not be limited to FE.
  - Then read 11910618, the gain bit-cell with stacked capacitors.
  - The diode steering and the linear dielectric are our delta. The gain read of a shared stacked node may sit inside their claims.
- **Intel EP4016625** (1T-nC plate lines).
- **Japanese oxide-semiconductor gain-string patents** (US 8421071, US 8750023).
- **Micron/Intel floating-gate 3D-NAND recess patents.** The tier process.
- **US 8508015** (oxidized-metal Schottky-like contacts). Check expiry and assignee before using AgOx/PtOx/IrOx anodes commercially.
- **IBM micro-sense-amp patents (2007 era).** Likely expiring around 2027-28 [ESTIMATE].
- **Cross-point diode-selector families** (US 8134194 lineage).

**What to file (provisionals before Stage A data is public)**
1. The diode-steered linear-capacitor 1T-nC cell: a per-tier rectifier between each floating node and the shared pillar, a plate-pulse dump read, and a clamp write-back inside the same plate pulse.
2. The plate-swing biasing rule (ΔV_PL ≥ Vdata + V_f + guard; stored levels below the pillar minimum) as the anti-disturb method, plus the page-equals-plate-segment / inhibit scheme.
3. The coaxial outer-anode geometry with a fully depleted shell sized to an anode-field limit, and a Ga-rich or low-electron-affinity shell to raise the barrier.
4. A reference tier per pillar and a self-referenced read for common-mode leakage drift. Optionally, retention-profiled tier repair.
5. The wrapped-plate (TiN/SiN/TiN) recess capacitor for diode-steered stacks.
6. Optional: the floating-node aA-leakage test structure, or publish it to build credibility.

## 9. Open gaps

1. **Barrier at the operating field.** Every literature number is thick-film and low-field. The thin-shell lowering (image force with ε ≈ 4 vs 12; TFE estimated to ±50%) is the largest modelling uncertainty, and only coupon type (1) and (2) data close it.
2. **Patch σ and patch size at ~2,600 nm².** The tail penalty grows from 0.10 to 0.16 eV as patches grow from 5 to 20 nm. Diode-to-diode statistics (coupon type 3) are the only direct measurement.
3. **Anode stability at ≤400 °C.** PtOx and AgOx may decompose at BEOL temperatures [UNVERIFIED: training knowledge]. IrOx/RuOx are more stable, but Ru supply is a concern: A2 says fleet-wide Ru electrodes would need 26-176% of world supply. The anode is a thin ring, so its Ru tonnage is far lower; still, MoOx and IrOx belong in the matrix.
4. **Forward-pulse stability at ~500 A/cm².** No oxide-Schottky cycling data exists. Oxygen-vacancy migration at the interface is the obvious drift mechanism.
5. **RTN and VRT in small oxide Schottky contacts.** These would add a non-Gaussian, time-varying tail. No data was found.
6. **Post-CDS residual of an in-hole IGZO gain FET** (≤7 mV for 32+ tiers; ≤10 mV caps the tower at ~40 tiers). Shared with PIXEL-STACK / MARGIN STACK.
7. **Process.** Uniform lateral recess along a 1.6-3.2 µm hole (Lam flags recess variation as hard, A1 §6). Ring isolation by etch-back. A 60 nm hole at AR 27-53 through TiN/SiO2. Tier yield ≥0.998 after repair. Staircase or tier-decoder area.
8. **Plate segmentation vs page size and energy.** Slits every 4 rows cost 12% of area. Inhibit biasing avoids slits but multiplies pillar-charging energy by the rows per segment.
9. **Temperature dependence of the clamp level.** V_f moves ~0.1 V from 0 to 85 °C, which needs a temperature-compensated plate swing.
10. **[SPECULATIVE] alternatives if Schottky contacts fail G1.**
    - p-oxide / n-oxide heterojunction diodes (e.g., NiO on IGZO). Their reverse current is generation-limited, with no image-force term, but interface traps are untested.
    - Wider-gap or lower-electron-affinity shells (amorphous Ga2O3) that raise every anode's barrier.
    - Both fit in the Stage A matrix for <$10k.
