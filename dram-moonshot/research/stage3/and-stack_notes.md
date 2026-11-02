# AND-STACK: research notes (agent dos-and-stack, 2026-11-02)

The model is `models/and-stack.py`; its output is in `research/stage3/and-stack_model_output.md`. Sources are logged in `research/sources/dos-and-stack.jsonl` and assumptions in `research/assumptions/dos-and-stack.md`. This session had a quota of 6 web searches. Facts marked "(via search snippet)" come from search-result summaries only. Facts marked [UNVERIFIED-PK] come from training knowledge and were not confirmed this session.

## 0. Bottom line

- **The physics holds, and the AND topology makes the key unknown easier than the card says.**
  - Every cell drives its own bitline pillar. So what decides cutoff is how far the 63 unselected rings must be pulled down. That is **1.09 V**, set by the top stored level plus about 5.4 decades of subthreshold. It does not depend on the coupling ratio (CR).
  - CR only sets the plate swing needed: 1.09 V / CR_min.
  - With a ≤2.5 V swing and σ_CR = 0.03, the GO bar is **CR ≥ 0.53**, not ≥0.6. The 0.6 figure was inherited from the series-string pass-boost of I-10664.
- **CR is a design choice, not a hope.**
  - A ring coupled only through its back face, like Micron's FG-NAND recess, gives CR ≈ 0.54 at an IPD EOT of 2.5 nm.
  - A "sandwich" select plate that wraps the ring on three faces gives CR ≈ 0.70, with C_SN ≈ 0.25 fF.
- **Two new risks replace CR as the real killers:**
  1. **Leakage through the ring's extra dielectrics at 85 °C.** For 2 b at 1 s, the 1e-4 tail cell must stay ≤21 aA. For 64 s it must stay ≤0.33 aA.
  2. **Topology closure.** The card's "same film" wording does not close electrically, because the ring would short into the read channel. I propose a closure: write with the BL and SL pillars at the same data voltage (§1). It needs TCAD, then silicon.
- **The prize, at 1% per-tier killer defects with tier-orthogonal erasure:**

| Case | Density | Component cost | Bits per $ vs 1-beta |
|---|---|---|---|
| 64 tiers × 2 b | 3.63 Gb/mm² (8.1× 1-beta) | $0.39/GB | 3.8× (5.0× at wafer level) |
| 32 tiers × 2 b | 1.82 Gb/mm² (4.1×) | $0.56/GB | 2.7× |

  - The sensitivity range for 64 × 2 b is 1.8–4.4×, across $15–80 per tier and 0.2–10% per-tier defect rates.
  - The card's "3–12×" is optimistic at the top end. 12× needs 3 b/cell, and 3 b does not close in a 1 V window (§5 of the model).

## 1. The concept as modelled (with my additions)

**Array**
- Holes sit on a 150 nm hex pitch, are 90 nm in diameter and carry a 15% slit overhead, so each hole takes 0.0224 µm².
- Each tier is two layers about 40 nm thick: a write plate (W/Mo) and a select level.
- At the select level, a recessed TiN ring about 18 nm tall and 10 nm thick is the storage node. The IPD that couples it to the select plate is about 6 nm, Al₂O₃-rich, EOT 2.5 nm.
- The hole is lined with read-gate dielectric (EOT 3 nm) and a 5 nm ALD IGZO or In₂O₃ film.
- The core holds two metal pillars, BL and SL, about 22 nm each, as in Macronix 3D AND.
- Each cell's read FET is two film arcs in parallel: W = 2 × 18 nm, L ≈ 93 nm, W/L 0.39. At Vds 0.1 V and an overdrive of about 1 V it gives ~0.9 µA.

**My additions, needed to close the design**

1. **Write mode with BL = SL = V_data.**
   - A film that touches both pillars and the ring can charge the ring through the write-plate channel with no path from BL to SL.
   - During a read, SL is grounded and only the selected select plate rises.
   - The alternative is per-level film segmentation: an outer write film in the write-level recess and an inner read film at the select level. That costs two more selective recesses.
2. **"Sandwich" select plate.**
   - The select level is built as W / conductive sacrificial layer (e.g. TiN) / W.
   - Recessing only the sacrificial layer from the hole leaves a cavity whose top and bottom faces are select metal.
   - Line the cavity with IPD, fill it with ring metal, and the select plate wraps the ring on three faces.
   - This raises CR from 0.54 to 0.70 and shields the ring from adjacent write plates, so neighbour-ring coupling is about 8 mV per volt.
3. **Hole-top pillar-select gate per select group** (2 hole rows).
   - It cuts unselected blocks off the local BL, so C_BL ≈ 8.9 fF.
   - It forces the top-BL pitch to 75 nm, which is SADP, not single-exposure ArF. The array is still EUV-free.
4. **Single-plate-level, current-mode MLC read**, with write-verify done at the same read bias.
   - Per-cell CR, read-FET Vt and kickback spread are calibrated out, so only the cutoff margin sees CR_min.
5. **Hold and read bias.**
   - Write-plate hold is −1.5 V. The lowest ring potential during reads is −1.09 V, so the write FET stays more than 0.9 V below threshold.
   - IGZO has no GIDL or band-to-band path, which is why oxide suits this cell [ESTIMATE: wide-gap n-type physics].

**Page semantics**
- Raising a write plate opens every hole on that plate strip, about 40 holes per µm of strip.
- Writes are therefore page writes with read-modify-write from an SRAM page buffer, as in DRAM row restore.
- Reads are non-destructive, so there is no overfetch restore.

## 2. Closest prior art and who is pursuing it

| Item | Who | Date | Status | Relation to AND-STACK |
|---|---|---|---|---|
| 3D AND flash: two S/D pillars inside a channel pillar, channel wrapping both; metal/silicide pillars ([US12245428](https://patents.google.com/patent/US12245428), [US12156402](https://patents.google.com/patent/US12156402), [US12200935](https://patents.google.com/patent/US12200935)) | Macronix | granted 2024–25 (dates not in snippet) | Patents (via search snippet) | **The pillar architecture AND-STACK borrows.** Freedom-to-operate check needed |
| 3D NOR with vertical S/D lines and top BL-select transistors ([US10910393](https://patents.google.com/patent/US10910393)) | Macronix | granted 2021 [UNVERIFIED date] | Patent (via search snippet) | Random-access vertical S/D precedent |
| 3D 2T0C bit cell with gate-around and channel-all-around IGZO FETs ([imec article](https://www.imec-int.com/en/articles/disrupting-dram-roadmap-capacitor-less-igzo-dram-technology)) | Macronix | not given | Secondhand (via search snippet) | **Macronix has both halves (3D AND and 3D 2T0C).** Most likely to file the combination: watch first, or partner |
| Vertical CAA IGZO FET for low-latency, high-density 2T0C 3D DRAM ([ECI ULSIC vs TFT 8](https://dc.engconfintl.org/ulsic_vs_tft_8/33)) | not seen | ~2022–24 | Invited talk (title only) | Vertical 2T0C device lineage |
| 4-tier dual-gate IGZO 2T0C formed in one stacking step, 3 b/cell, 400 s ([IT Home](https://www.ithome.com/0/966/543.htm)) | IMECAS + Beijing Super String | VLSI 2026 | Silicon | **Closest silicon competitor.** Single-step stacking, but series/per-tier, not AND |
| 3D DRAM from vertical dual-gate IGZO TFTs, 4F² cell via a self-aligned single-step (SASS) process ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12686015)) | (Nature Commun., Dec 2025, per snippet) | 2025-12 | Peer-reviewed (attribution to this URL probable, not certain) | Dense vertical 2T0C |
| Vertically stacked 2T0C1R with dual-gated IGZO, IEDM 2024 ([NUS](https://shine.nus.edu.sg/2025/02/18/1t1r-and-2toc1r-igzo-mos%e2%82%82-all-beol-3d-memory-cells/)) | NUS | 2024-12 | Silicon | Stacked gain cell |
| 2T0C in vertically aligned plugs "inspired by 3D NAND"; >1e3 s, >1e11 cycles (2021); >200 s at 95 °C, >1e12 cycles (EDL 2025) | imec | 2020–25 | Silicon | Endurance and retention anchors; NAND-plug concept |
| IGO 2T0C with HfO₂ passivation: >30,000 s, 4 b/cell, 10 ns write | SJTU | AFM 2026 | Silicon | Retention headroom (interfaces) |
| 3D X-DRAM: IGZO 1T1C/3T0C (TCAD, 2025); Si single-cell PoC >1 s at 85 °C, >1e14 cycles (2026) | NEO Semiconductor | 2025-05 / 2026-04 | TCAD + one-cell PoC | Competitor narrative ("3D-NAND process DRAM"); licensing talks |
| OCTRAM 4F² (275 Mb); 3D OCTRAM, SiN→IGZO replacement in 8 layers, Ion >30 µA, Ioff <1 aA | Kioxia (+ Nanya) | IEDM 2024 / 2025 | Silicon (transistors) | Shows deposited-oxide channels in all tiers at once |
| Vertical 3D single-word-line gain cell with shared read/write bit line ([US11631453B2](https://patents.google.com/patent/US11631453)) | Micron per one snippet | granted 2023 [UNVERIFIED date] | Patent (claims not read) | **Shared R/W BL resembles our BL = SL write.** Read its claims |
| NAND-style series oxide gain cells (US8421071, US8750023, US12082391) | SEL / Japanese OS camp | 2013–24 | Patents | Series strings: the topology AND-STACK avoids |
| Vertical Si gain cell, read gate = storage node ([US6246083](https://patents.google.com/patent/US6246083)); side- and top-gated read transistor ([EP1938378B1](https://patents.google.com/patent/EP1938378B1/cg-RX-API-DMAC7.html)) | Micron; other | 1998 filing (likely expired); 2000s | Patents | Prior art against over-broad claims; multi-face storage-node gating |
| IGZO 3D CCD buffer memory in vertical holes (IMW 2026) | imec | 2024–26 | Silicon (3 WL) | A rival "IGZO in NAND holes" memory, block-addressable |
| Floating-gate 3D NAND with recessed poly FG and IPD | Micron/Intel (IMFT) | 2015+ | Production (since moved to replacement gate) [UNVERIFIED-PK] | Per-tier recess and IPD know-how at 64+ tiers |

**Novelty read.**
- I found no single public reference that combines all four of:
  1. a gain cell at every tier-hole crossing;
  2. two vertical S/D pillars in each hole (AND wiring);
  3. a per-tier floating ring coupled to a dedicated select plate;
  4. a per-tier write plate.
- This rests on 3 targeted searches (snippets only), so it is not a freedom-to-operate opinion.
- Macronix is the obvious party to have filed this, and Micron's US11631453 needs a claim read.

## 3. Best demonstrated numbers for each component

| Component | Best shown | Source | What AND-STACK needs (model) |
|---|---|---|---|
| Oxide 2T0C retention at temperature | >200 s at 95 °C, Lg 40 nm | imec EDL 2025 | ≥1 s at 85 °C for 2 b, tail cell ≤21 aA; ≥64 s (≤0.33 aA) for refresh-free-class energy |
| Retention at room temperature, multilevel | >30,000 s, 4 b | SJTU AFM 2026 | — |
| 3D multi-tier gain cell | 4 tiers, single step, 3 b, 400 s | IMECAS VLSI 2026 | 32–64 tiers AND-wired |
| Endurance | >1e12 cycles | imec EDL 2025 | 1.3e9 pulses (1 s refresh, 10 yr, ×4 verify); hot row needs 2.8e14 |
| Write speed | <10 ns | imec 2021/2025 | ~20 ns pulse; 2 b ≈ 100 ns with verify |
| Oxide FET drive (vertical ALD In₂O₃) | Imax >160 µA/µm, on/off >1e5 | Purdue VLSI 2024 | ~0.9 µA per cell at Vds 0.1 V (25 µA/µm of W) |
| Oxide FET in all tiers at once | 8 layers, Ion >30 µA, Ioff <1 aA | Kioxia IEDM 2025 | 64 tiers; ring leakage ≤21 aA at 85 °C |
| ALD In₂O₃ thermal budget | survives 600 °C | Purdue EDL 2024 | Array wafer is bonded to periphery after array processing, so 400–600 °C anneals are allowed |
| Monolithic oxide layers at wafer scale | 3 layers, >100,000 devices, 52 dies, 200 mm | Purdue 2026-09 | — |
| Hydrogen and PBTI control | H+O anneal cuts H-doping under PBTI ~30×; 1.2 V overdrive for 5 yr at 95 °C target | imec IEDM 2025 | Drift ≤86 mV per refresh interval for raw BER 1e-4 at 2 b |
| Hybrid bond pitch | 300 nm W2W | imec ECTC 2025 (via A3) | ~1–2 µm per local-BL group |
| 3D AND pillar structure | Patents only for flash | Macronix | DRAM-class in-hole pillars |

## 4. Model headline numbers (`models/and-stack.py`)

**Density**
- 0.0284 Gb/mm² per bit-tier, after array efficiency 0.7 and 10% parity.
- 1-beta parity at 15.7 bit-tiers.
- 32 × 2 b = 1.82 Gb/mm² (4.1×); 64 × 2 b = 3.63 Gb/mm² (8.1×).
- The 64-tier stack is 5.4 µm tall at a 60:1 hole aspect ratio.
- Staircase 4.7% of area; plate web 24 nm; select-plate RC 3.1 ns per 200 µm.

**Storage node**
- C_SN 0.246 fF, CR 0.70 (sandwich plate); C_SN 0.159 fF, CR 0.54 (back face only).
- Kickback 130 mV, deterministic and pre-compensated.
- Neighbour coupling 8 mV; kTC 4.5 mV.
- A 2 b level step is 333 mV, or 512 electrons.

**Select margin**
- Each unselected cell must stay ≤142 fA.
- That requires a ring shift of 1.09 V, so dV_unsel = 1.79 V at CR 0.70, or 2.66 V at CR 0.50.
- **GO: CR ≥ 0.53.**

**Read**
- C_BL 8.9 fF; 2 b current step 298 nA; resolves in 1.5 ns.
- Array read about 15 ns; read energy about 1.5 fJ per cell.

**Write**
- About 23 fJ per pulse, ×4 for 2 b write-verify. A 2 b write takes ~100 ns, so page-parallel writes and an SRAM buffer are needed.

**Raw BER**

| Bits/cell | Window | Raw BER at 60 mV drift + 30 mV coupling | Drift tolerated at BER 1e-4 |
|---|---|---|---|
| 2 | 1 V | 1e-8 | 86 mV |
| 3 | 1 V | does not close | — |
| 3 | 1.5 V, coupling ≤10 mV | — | 48 mV |

**Retention and refresh**
- Leakage budget for 2 b: 21 aA at 1 s, 0.33 aA at 64 s.
- IPD current density limit: ≤1.2e-7 A/cm² at 1 s, or ≤1.8e-9 A/cm² at 64 s.
- Refresh power vs DDR5 at 32 ms: 31× lower at 1 s, ~2,000× lower at 64 s.

**Endurance**
- Refresh-only wear sits 780× inside imec's 1e12.
- Hot rows fall ~280× short, so the controller must remap them, or ≥1e14 must be shown.

**Yield** (64 tiers, 1% per-tier killer defects per die)
- No erasure code: 0.47.
- Tier-orthogonal RS with 2 spares: 0.84 if 10% of defects are not confined to one tier, 0.74 if 30% are not.

**Cost**
- 64 × 2 b: $0.25/GB wafer level, $0.39/GB component (3.8×).
- Component break-even at 19 tiers for 1 b, or 9 tiers for 2 b.

## 5. U.S. facilities that could build the demo

| Facility | Role for AND-STACK | Cost/rate info found |
|---|---|---|
| **Purdue Birck Nanotechnology Center** | ALD In₂O₃ (P. Ye group: vertical all-oxide TFTs, 3-layer monolithic 3D on 200 mm), e-beam. Primary site for Phase 1 and the Phase 2 films | Rates not found this session [UNVERIFIED]; budget at $75–250 per tool-hour (p1-fabs). SK hynix broke ground on its West Lafayette plant 2026-08-27 (logged), a partner channel |
| **Georgia Tech IEN** | Oxide BEOL transistors, 3D FeRAM (GT two-tier 1T-1C, IEDM 2025, logged), device–circuit co-design | Not found [UNVERIFIED] |
| **Notre Dame NDNF** | General cleanroom; oxide-FET heritage [UNVERIFIED-PK] | **$124/h external cleanroom access, FY2025-26**, plus supplies and surcharges ([NDNF](https://nanofabrication.nd.edu/facility-access/fees/), via snippet) |
| **Northwestern NUFAB** | ALD calibration of IPD and channel splits | **ALD $37/h (GEMStar), $77/h (Savannah), academic 2024-25; ×2 for companies** ([NUFAB](https://www.nuance.northwestern.edu/documents/rates/2025-rates/2025-nufab.pdf), via snippet) |
| **UNM CHTM** (near Sandia/CINT) | Backup cleanroom; staff-assisted runs | **$250/h assisted, $88/h unassisted, 2026** ([UNM](https://unmnanofab.unm.edu/user-rates/2026-04-24.pdf), via snippet) |
| Vanderbilt VINSE; UF NRF | Benchmarks | $65/h industry cleanroom (Vanderbilt); Fiji ALD $143.70 per 24 h run plus precursor (UF) (via snippets) |
| Stanford SNF, Cornell CNF, MIT.nano, Penn Singh, ASU, UT Austin (Texas Institute for Electronics) | Alternatives. SNF and MIT.nano have ALD and e-beam; CNF runs a 2026 PFAS-in-etch project (logged) | Not found [UNVERIFIED]; NNCI sites publish hourly industry rates |
| **Argonne CNM; Sandia/LANL CINT; ORNL CNMS; LBNL Molecular Foundry** | ALD process science, in-situ film metrology, TEM | DOE user facilities: no charge for non-proprietary proposals; proprietary work at cost recovery [UNVERIFIED-PK]. Use them for the publishable H-lean-mold and ALD studies |
| **NIST CNST NanoFab** (Gaithersburg) | E-beam lithography for 150–300 nm holes and the split-pillar cut | Fee-based, open to industry [UNVERIFIED-PK]; rate not found |
| **Sandia MESA** | 300 mm-class rad-hard fab; access hard for a startup | [UNVERIFIED-PK] |
| **NY CREATES Albany** | 300 mm hole etch and ALD for a post-raise 16–32 tier lot; JDA model (Fraunhofer IPMS memory JDA, 2025-05, logged) | JDA pricing not public |
| MPW for a readout or sense chip | **ChipFoundry sky130: $15k per 100 chips** (logged); **wafer.space GF180: $7k per 1,000 ICs, fabbed in Singapore** (logged); MOSIS 2.0 (USC ISI, GF partner) | As listed |
| Test and failure analysis | In-house bench (used Keysight B1500A + WGFMU, hot-chuck probe station); FIB/TEM at university characterization centers or commercial labs | Bench ≈ $85k used [ESTIMATE]; FIB/TEM ≈ $2–3k per cross-section [ESTIMATE] |

## 6. Collaborators and recruits

- **Peide Ye (Purdue ECE).** ALD In₂O₃ FETs: 8 nm channel length, 0.84 nm EOT (Nature Electronics 2022); vertical all-oxide TFTs (VLSI 2024); 600 °C survival (EDL 2024); 3-layer monolithic platform (2026). All logged. **Best first collaborator.** The channel film, conformal ALD and a vertical-device heritage are exactly Phase 1/2 needs.
- **Georgia Tech.**
  - The IEDM 2025 two-tier 3D FeRAM team (logged).
  - Shimeng Yu (memory device/circuit co-design, IGZO 2T0C benchmarking) [UNVERIFIED-PK].
  - Suman Datta (oxide-semiconductor BEOL FETs) [UNVERIFIED-PK].
  - Good for the 64-cell parallel AND SPICE and TCAD, and as a second fab.
- **Stanford.** H.-S. Philip Wong (BEOL oxide memory, monolithic 3D, N3XT) [UNVERIFIED-PK]. The Stanford/TSMC gate-dielectric work for oxide FETs is in the VLSI 2025 tip sheet (logged).
- **Recruit profile (the device/process co-founder):** a floating-gate 3D NAND process-integration engineer with hands-on recess/IPD/FG-poly experience. Look at ex-Micron Boise R&D, which developed FG 3D NAND before replacement gate, and ex-Intel/Solidigm NAND R&D in Folsom [UNVERIFIED-PK]. FG recess and IPD wrap are the exact skills for the ring module.
- **Second recruit or advisor:** an oxide-TFT reliability person (PBTI and hydrogen) from imec, Purdue or display-industry IGZO teams [UNVERIFIED-PK].
- **Partners and licensors to watch:**
  - Macronix (3D AND plus 3D 2T0C);
  - SK hynix (Purdue proximity; Solidigm NAND toolsets);
  - Kioxia/SanDisk (idle NAND decks, OCTRAM);
  - NEO Semiconductor, a competitor that is shopping licences.

## 7. Decisive experiment

### Step by step

**Phase 0, months 0–3: design closure (~$30k)**
1. Use a 3D electrostatic solver (open-source FEM, or a collaborator's academic TCAD) to compute CR, C_SN, neighbour coupling and kickback. Cover wrap 0 / 0.5 / 1, IPD EOT 2–5 nm and recess depth ±3 nm. Target CR ≥ 0.6 nominal so that a measured ≥0.53 is safe.
2. Run SPICE of one 64-tier hole with an oxide-TFT compact model: 63 unselected cells holding the top level, plus BL = SL write mode. Confirm 142 fA per unselected cell, the 1.09 V ring shift, and that no write path shorts the ring.
3. Decide the topology: single film with BL = SL writes, or per-level segmented films. Draw the Phase 1 masks.
4. Run a freedom-to-operate search and file Provisional #1 before any talk or poster (§8).

**Phase 1, months 2–11: planar 64-cell AND emulation (~$150k fab + $25k analysis), at Birck (or IEN), with ALD splits at NUFAB or Argonne CNM.**

5. **Planar "hole".** Build 64 cells in parallel on one shared BL line and one shared SL line, each cell with its own write-plate and select-plate electrodes. Each cell has:
   - a bottom select electrode;
   - an ALD IPD;
   - a floating TiN island ring, e-beam patterned to the vertical ring's area (~0.012 µm²) and also at 10× area;
   - an optional top select cap, to emulate wrap;
   - the read-gate dielectric;
   - the IGZO / In₂O₃ / Ga-free IZO or ZTO film;
   - a write-TFT segment gated by its write electrode.

   This measures the 63-unselected cutoff directly instead of extrapolating it.
6. **Splits:** wrap (0 / 1) × IPD EOT (2.5 / 3.5 nm) × channel (IGZO / In₂O₃ / ZTO) × mold (H-lean LPCVD vs PECVD cap, triage N-56). That is 2 runs of about 5 wafers each.
7. **Measurements at 25 / 85 / 110 °C:**
   - (a) CR = ΔVt_read / ΔV_select across ≥50 cells.
   - (b) Per-cell off current versus V_unsel with the top level stored, summed over 63.
   - (c) 2 b write-verify and level maps.
   - (d) Retention, using the read FET as an electrometer on the ring, out to 1e4 s; extract the 1e-4 tail.
   - (e) Neighbour-write disturb after 1e9 writes (≈20 s of BL/SL swing).
   - (f) Kickback and its spread.
   - (g) Endurance to 1e12 (about 28 h at 10 MHz).
   - (h) SIMS hydrogen in H-lean vs PECVD molds.
8. **GO/NO-GO #1 at month 11:**
   - **GO** needs all of:
     - CR ≥ 0.53 with σ ≤ 0.03;
     - each unselected cell ≤142 fA at 85 °C (on/off ≥1e5 against 63);
     - disturb ≤30 mV extra after 1e9 neighbour writes;
     - 4 levels in ≤1 V held ≥1 s at 85 °C, with the 1e-4 tail drifting ≤86 mV (≤21 aA).
   - **NO-GO** on any of:
     - CR < 0.40;
     - tail leakage > 100 aA at 85 °C;
     - disturb > 1 LSB.
   - Revival paths: 1 b/cell with 2× the tiers, or the per-tier coaxial fallback.

**Phase 2, months 10–22: 4-tier vertical AND stack (~$330k fab + $50k FA)**

9. **Stack:** 4 × (write plate + sandwich select W/TiN/W) + hole-top select + caps. That is about 14 layers, ~0.8 µm thick.
   - Holes 200–300 nm in diameter, by e-beam at Birck or CNST; the card asks for 150–200 nm, which is a stretch at university scale.
   - Etch the stack with ICP oxide/metal etch.
10. **Ring module:**
    - selective TiN recess (wet, selective to W) [UNVERIFIED-PK chemistry];
    - ALD IPD, then ALD TiN ring;
    - etch-back to segment the rings per tier;
    - read-gate dielectric, then the ALD channel film (Purdue).
11. **Split-pillar core:** insulating fill, an e-beam-defined cut, then TiN/W fill for the BL and SL pillars (the Macronix-style structure).
12. **Measurements:**
    - per-tier write and read;
    - unselected-tier cutoff (4 tiers, cross-checked against the Phase 1 64-cell result);
    - tier-to-tier spread of CR, Vt and leakage;
    - 2 b retention at 85 °C;
    - disturb after 1e9 neighbour writes;
    - endurance to 1e12;
    - FIB/TEM of the recess, ring and web uniformity;
    - a defect-localization map, to estimate the non-confined defect share for the yield model.
13. **GO/NO-GO #2 at month 22–23:** Phase 1 criteria met on every one of the 4 tiers, with tier-to-tier σ_CR ≤ 0.03 and leakage tails within 2× of planar. Then raise $10–50M for a 16–32 tier 300 mm lot at NY CREATES or with a NAND partner.
14. **Optional:** read the stacks through the portfolio's shared MARGIN STACK MPW sense/ADC chip. It is funded outside this budget.

### Budget (AND-STACK as a standalone seed; under $1M)

| Line | $k | Basis |
|---|---|---|
| Two founders, lean pay (2 × ~$48k/yr × 2 yr) | 190 | Thiel-style lean [ESTIMATE] |
| IP: freedom-to-operate search, 3 provisionals, 1 PCT at month 12 | 50 | [ESTIMATE] |
| Phase 0 electrostatics, TCAD and SPICE (collaborator time, contractor) | 30 | [ESTIMATE] |
| Test bench: used B1500A + WGFMU, hot-chuck probe station, AWG, probe cards | 85 | [ESTIMATE] |
| Phase 1 fab: ~650 tool-h × $150 + ~150 staff-h × $150 + e-beam + materials | 150 | Rates in §5; p1-fabs $75–250 per tool-hour |
| Phase 1 analysis: SIMS (H), XPS, TEM | 25 | [ESTIMATE] |
| Phase 2 fab: ~1,400 tool-h × $175 + ~300 staff-h × $150 + CNST e-beam + materials | 330 | [ESTIMATE] |
| Phase 2 FIB/TEM and failure analysis (~20 cross-sections) | 50 | ~$2.5k each [ESTIMATE] |
| Travel, insurance, legal, company | 40 | [ESTIMATE] |
| Contingency | 35 | ~4% |
| **Total** | **985** | |

Portfolio note: FINAL_CONCEPTS allocates only ~$150k of the shared seed to AND-STACK. In that case Phases 0–1 (~$230k with the bench and IP shares) are the seed deliverable, and Phase 2 becomes the raise milestone or partner-funded work (Purdue/SK hynix, or a NAND maker's idle deck).

### Timeline (under 24 months)

| Months | Work |
|---|---|
| 0–3 | TCAD and SPICE closure; freedom-to-operate search; Provisional #1; bench set-up; nanofab onboarding |
| 2–6 | Phase 1 run 1 (wrap × IPD × channel) |
| 5–9 | Phase 1 run 2 (H-lean vs PECVD mold; 64-cell AND structures; disturb structures) |
| 6–11 | Measurements; **GO/NO-GO #1 at month 11**; Provisionals #2–3 |
| 12 | PCT filing |
| 10–16 | Phase 2 short loops: hole etch, sandwich recess, ring segmentation, split pillars |
| 16–20 | Two full 4-tier lots |
| 19–23 | Measurements; **GO/NO-GO #2 and demo at month 22–23**; data room for the raise |

## 8. IP landscape

**Patents to watch, and to read in full before filing**
- Macronix 3D AND flash: US12245428, US12156402, US12200935. Also its 3D NOR with vertical S/D (US10910393) and any Macronix 3D 2T0C filings. The highest freedom-to-operate risk is the split-pillar-in-hole structure.
- US11631453B2 (vertical 3D single-word-line gain cell with shared R/W bit line; Micron per one snippet), because the shared R/W BL resembles BL = SL writes.
- SEL / Japanese OS NAND gain-cell families (US8421071, US8750023, US12082391), plus SEL NOSRAM/DOSRAM.
- Micron/Intel floating-gate 3D NAND recessed-FG and IPD patents (ring recess, IPD wrap).
- NEO Semiconductor 3D X-DRAM (IGZO 1T1C/3T0C on a NAND-like process).
- Kioxia OCTRAM and 3D OCTRAM (SiN→IGZO replacement).
- imec 2T0C vertical-plug patents; IMECAS / Beijing Super String dual-gate single-step 2T0C; Samsung and SK hynix 3D DRAM.
- Useful prior art against over-broad claims (ours and theirs): US6246083 (likely expired) and EP1938378B1.

**What to file (provisionals, in priority order)**
1. **Dual-plate AND gain-cell array and its operation:**
   - per-tier write plate plus select plate;
   - a floating storage ring coupled to the select plate, gating a channel between BL and SL pillars in a single hole;
   - reads with all other select plates at cutoff;
   - **writes with BL = SL = data**;
   - the hole-top pillar select.
2. **Sandwich select plate:** recessing a conductive interlayer between two plate metals so the select plate wraps the ring (CR ≥ 0.65), including the shielding of adjacent write plates.
3. **Single-bias current-mode MLC read with write-verify at read bias.** It cancels per-cell CR, Vt and kickback, and adjusts the cutoff-bias schedule from measured CR_min.
4. **Tier-orthogonal erasure codewords with exported erasure flags** for 3D gain-cell DRAM. Coordinate with the RAW-BER CONTRACT dossier to avoid duplication.
5. **H-lean batch-furnace mold** for oxide-channel 3D memory (N-56). Coordinate with the portfolio.

## 9. Open gaps

1. **Topology closure is unverified.** BL = SL writes, and the alternative of segmented films, are my own analysis. No TCAD or silicon exists yet. This is the first Phase 0 deliverable.
2. **Ring dielectric leakage at 85 °C at aA–zA levels.** The IPD adds about 1.25e-10 cm² of dielectric to every storage node. No data exists for oxide gain cells with a floating metal ring plus IPD.
3. **CR spread across tiers.** σ = 0.03 is assumed. Lam notes that recess depth varies along the stack (A1). Measure it in Phase 2.
4. **Geometry is tight:**
   - a 24 nm plate web at 150/90 nm;
   - two 22 nm pillars in a 68 nm core;
   - ALD conformality into recesses at 60:1, where Purdue's ALD In₂O₃ has only been shown on planar and short vertical devices.
5. **Write latency.** A 2 b write-verify takes ~100 ns. That is DRAM-class only with page-parallel writes and controller buffering.
6. **Hot-row endurance.** A pathological hot row needs about 2.8e14 pulses against 1e12 shown, so the controller must remap.
7. **Cost inputs are unanchored:**
   - $/tier ($15–45) has no published 3D-NAND per-layer cost behind it;
   - the $1k array base and the $2.5k periphery wafer are estimates;
   - the non-confined defect share (10%) is a guess and drives yield.
8. **3 b/cell does not close in a 1 V window.** The card's top case (12×) needs a 1.5 V window, ≤10 mV coupling and ≤~48 mV drift.
9. **Prior art rests on snippets.** No patent claim was read. The Nature Commun. Dec-2025 SASS paper's URL mapping is uncertain. Macronix's own 3D 2T0C paper was not found.
10. **Facility rates are missing for most named sites.** Rates were found for Notre Dame, Northwestern, UNM, Vanderbilt and UF only. Birck, IEN, SNF, CNF, MIT.nano, CNST and the DOE user-facility terms are unverified this session.
