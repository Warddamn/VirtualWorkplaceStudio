# HOT-SIDE MEMORY: refresh-free oxide gain-cell tiers in the backside-power carrier wafer, plus at most 4 tiers in the logic BEOL

*Dossier for `hot-side-memory`. Agent `dosw-hot-side-memory`, 2026-11-02.*

*Inputs: `FINAL_CONCEPTS.json/.md`, `hot-side-memory_notes.md`, the model output, `models/hot-side-memory.py` (re-run 2026-11-02, exit 0, identical output) and `MISSION.md`. Tags: [ESTIMATE] is a rule-of-thumb number; [SPECULATIVE] is untested; [training knowledge] was not re-verified.*

## 0. Header

**Thesis (revised after red team).** Backside power puts a bonded carrier wafer on every backside-power logic die. That means TSMC A16 and Intel 18A/14A; the first accelerators are due ~2028, with Nvidia Feynman on A16 as reported. Rubin-class parts are still front-side power. Suppose that carrier is a 28 nm-class CMOS wafer with 8-16 tiers of oxide gain cells, joined *after* backside processing (carrier-last). Oxide gain cells are the one DRAM-class cell that holds data for seconds at junction temperature. Then the accelerator gets 39-78 GB per GPU at 1 b/cell (157 GB if 2 b works), ~3 mm from its compute, at about a tenth of HBM's delivered energy per bit. *Was:* "every leading-edge logic die", "tens of GB a micrometre away", "holds data for minutes", "refresh-free".

**Rank:** 2 of 10. EV 64 = S4 x P4 x D4. Ranks 2-4 are within scoring noise.

**Category:** integration/manufacturing.

**Merge:** the device-lens cell, energy and BEOL-test work combined with the system lens's carrier-first split, cap of 4 BEOL tiers and fail-soft binning.

| ID | Idea | Creativity technique |
|---|---|---|
| I-11538 = N-41 | Carrier-is-memory: the BSPDN carrier becomes a memory wafer (B3-02) | Phase B lens: B3 3D/process |
| I-11532 = N-35 | Main memory inside the logic die's own metal stack (B2-16) | Phase B lens: B2 materials |
| I-00156 | Wafer-scale DRAM bonded under a wafer-scale accelerator | SCAMPER-Substitute |
| I-02936 | All-IGZO memory with n-only periphery | TRIZ #33, Homogeneity |
| I-00729 | Tier-orthogonal codewords break 3D yield compounding | SCAMPER-Combine |
| I-11559 | ECC-paid margin: design to raw BER 1e-4 (B4-01) | Phase B lens: B4 architecture |
| I-11192 | GPU-owned sense amps under a bonded array | Scarcity and constraint as engine |
| I-11544 | Vt-coded in-stack tier decoder (B3-08) | Phase B lens: B3 3D/process |
| N-57 (I-11554) | Oxide tiers on a finished die, with hydrogen sequencing (B3-18) | Phase B lens: B3 3D/process |

**Verdicts (revised after red team; the originals are quoted in s11)**

- **PHYSICALLY POSSIBLE? Yes at 1 b/cell; 2 b/cell conditional.**
  - Every part is shown separately: oxide 2T0C (>200 s at 95 C, >1e12 cycles), W2W bonds at 0.2-1 um, BSPDN carriers in production, and inorganic IR-release temporary carriers for the carrier-last flow (vendor claim).
  - The 1e-4 leakage tail makes the cell refresh-light, not refresh-free: 1 b refreshes every ~3.6 s at 105 C and ~1.4 s at 125 C, still ~225x rarer than Si.
  - 2 b depends on read-FET RTN, cross-temperature reads and tail leakage, none of which is measured yet. These are open reliability numbers, not laws of physics.
- **STEP CHANGE IF IT WORKS? Yes, ~10x on energy per bit moved (was ~12x); ~90 W per GPU at the planning case (was ~190 W).**
  - 0.37 vs 3.95 pJ/bit delivered with SM-local placement (5.5x if placement is random, 15x at 1 mm).
  - Traffic share tracks capacity: 48 W (8 x 1 b), **92 W (16 x 1 b, planning)**, 169 W (16 x 2 b).
  - Not a cost step: $4.6-12/GB incremental (was $1.36-3.55), 3-8x DDR5 cost, below HBM4 price.
- **PROVABLE WITH $1M IN 24 MONTHS? Partly.**
  - The cell question, now including RTN, cross-temperature reads, the measured 1e-4 tail and a real bond, is answered for ~$240k by month 11.
  - The 22FDX logic-shift leg and carrier proxies (in-plane distortion, CSAM voids, VPD-ICPMS) fit in $1.00M.
  - Production backside overlay, killer-defect density, foundry materials acceptance and a named BSPDN partner need the raise.

**Final status after red team: DOWNGRADED** (section 11).

## 1. How it works

**Today: memory sits beside the processor.** An AI accelerator keeps its working data in HBM, stacks of DRAM beside the processor on a silicon interposer. Each bit crosses a high-speed port (PHY), millimetres of interposer and a stack of vertical vias, at ~3.5 picojoules. At up to 22 TB/s per GPU, that is hundreds of watts.

**Why it can't go on top.** The processor runs near 100 C, and ordinary DRAM stores each bit as charge on a tiny capacitor that leaks away within milliseconds when it is that hot. At 105 C silicon DRAM must be refreshed about every 16 ms.

**Two recent changes make it possible.**
1. **Backside power.** Intel 18A and TSMC A16 build the processor, then flip the wafer and glue its wiring side to a second "carrier" wafer. They grind off the original silicon and put the power wiring on the exposed back. Today the carrier is blank silicon, just a pallet that holds things up, and it sits between the processor and the heat sink.
2. **Oxide gain cells.** This cell uses two thin-film transistors made of indium-gallium-zinc oxide (IGZO), the material in phone displays.
   A bit is charge on the read transistor's gate. The write transistor, when off, leaks only zeptoamps (1e-21 A), so the charge survives minutes even at 95 C. Reading senses current through the read transistor, like reading a gauge instead of opening the tap, so the bit is not destroyed.

**The idea: turn the pallet into a warehouse.**
The carrier becomes a cheap 28-65 nm CMOS wafer holding sense amplifiers under 8-16 oxide-cell tiers built below 400 C, bonded face-to-face to the processor so data moves about a micrometre. Up to 4 more tiers can sit in the processor's wiring. A defective memory spot is remapped; the chip ships with slightly less near memory instead of being scrapped.

```
              HEAT SINK
 ==========================================
  carrier silicon (heat spreader)
  carrier CMOS: sense amps, decoders     <- 28-65 nm, trailing-node fab
  8-16 oxide gain-cell tiers             <- built at <=400 C, ~0.2 um each
 ---- hybrid bond, ~1.5 um pitch, ~44k data bonds per die ----
  0-4 optional oxide tiers in logic BEOL
  logic front-side wiring (signals)
  logic transistors (GPU)                <- ~105 C junction
  backside power network
 ==========================================
        package bumps

 HBM:      GPU -> PHY -> interposer (mm) -> base die -> TSVs -> DRAM  ~3.5 pJ/b
 Hot-side: GPU -> bond (~1 um) -> carrier sense amp -> oxide cell     ~0.1-0.3 pJ/b
```

It is a **near tier, not an HBM replacement**, holding the hottest data: a tensor-parallel weight slice, hot KV and activations.

## 2. The physics and the numbers (revised after red team)

All values below come from `models/hot-side-memory.py`, re-run after the red team (its RED-TEAM REVISIONS block and section 11). Pre-red-team values are kept as *was*.

**Density.**
- **Cell:** vertical 2T0C at 10F2, F = 40 nm (ArF-immersion single exposure, no EUV). That is 0.016 um2, or 62.5 M cells/mm2 per tier. The tier is now 0.24 um thick (was 0.20) to fit the series write gate (RT-DEV-01).
- **Carrier tiers:** CMOS sits under the array. Tier efficiency is 0.45 (was 0.50), because the periphery is now hierarchical (RT-CIRC-01). Overhead is RS(36,32) tier erasure (12.5%) plus a row BCH t=23 (2.1%), 14.9% in all (was 12.5%; RT-CIRC-04). Per tier-bit: 62.5e6 x 0.45 / 1.149 = **0.0245 Gb/mm2** (was 0.0278).
- **Carrier floorplan (new; RT-CIRC-01).**
  - Rows of 8,192 cells; a 64-cell local RBL behind an oxide segment switch; a 4,096-cell global RBL (126 fF); one via per tier to a Si 16:1 tier mux and a shared 2-b SA in the carrier.
  - That allows 9.1 um2 per WL driver and 146 um2 per SA, 50% of the carrier area in **28 nm-class** CMOS. A 65 nm carrier fits only ~4-5 tiers.
  - The original 64 x 256 subarrays needed 0.13 um2 per SA and 0.26 um2 per driver, ~24x the area available.
- **BEOL tiers:** all-oxide periphery at efficiency 0.3 gives 0.0163 Gb/mm2.

| Configuration | Gb/mm2 | vs 1-beta (0.447) | GB/die | GB/GPU (vs 288 GB HBM4) |
|---|---|---|---|---|
| Carrier 8 x 1 b | 0.196 | 0.44x | 20 | 39 (14%) |
| Carrier 16 x 1 b (**planning**) | 0.392 | 0.88x | 39 | 78 (27%) |
| Carrier 16 x 2 b (upside) | 0.783 | 1.75x | 78 | 157 (54%) |
| + 4 BEOL x 2 b | +0.131 | +0.29x | +13 | +26 |

*Was:* 22-89 GB/die, and 0.889 Gb/mm2 (1.99x) at 16 x 2 b. The planning case moved to 1 b because RTN, cross-temperature reads and the 1e-4 leakage tail are unmeasured (RT-DEV-01/02, RT-CIRC-02).

**Retention and refresh.**
- **Typical cell:** from imec's >200 s at 95 C, Arrhenius at Ea = 0.8 eV gives 200 x e^-0.667 = **103 s at 105 C**, vs 16 ms for silicon (6,417x), and 30 s vs 4 ms at 125 C. Implied leakage is 0.15 fF x 100 mV / 200 s = **75 zA**. Over Ea = 0.5-1.1 eV the extrapolation spans 80-132 s (105 C) and 15-61 s (125 C). No 125 C oxide 2T0C data is published.
- **The 1e-4 tail sets refresh (revised; RT-DEV-01).**
  - A write-FET sigma_Vt of 50 mV at SS 95 mV/dec makes the tail cell leak 10^(3.72 x 50/95) = **91x** the typical one (was an assumed 3x). 30 mV gives 15x; 100 mV gives 8,217x.
  - Adopted: a series or double-length write gate (top-up I-12627; no footprint in a vertical cell) brings this to 17-36x for independent to rho = 0.5 tails. A -0.7 V hold buys ~127x if leakage is subthreshold-limited. Planning value: **25x**.
  - Tail leakage: 3.7 aA at 105 C and 12.5 aA at 125 C, against ceilings of 7.5 aA (2 b, 1 s) and 22.5 aA (1 b, 1 s).
  - Refresh at the tail: **1 b every 3.6 s (105 C) / 1.4 s (125 C)**, ~225x rarer than Si at 105 C; **2 b every 0.64 s / 0.25 s**. Unmitigated 91x gives 0.24 s (2 b, 105 C) and 0.49 s (1 b, 125 C).
  - This is **refresh-light, not refresh-free**.

**Multi-level margin: the key unknown in numbers (revised).**
- **Budget:** half of the raw BER 1e-4 is reserved for read-FET RTN, which references and write-verify cannot cancel (RT-DEV-02), leaving 5e-5 for the Gaussian terms.
- **Gaussian terms:**
  - write placement 10 mV: verify-truncated kT/C (5.9-6.1 mV per shot) plus verify noise gives 9.9 mV (RT-DEV-04);
  - sense residual 10 mV (was 8): global RBL, segment switch and tier mux;
  - cross-temperature residual 10 mV (new): in-row per-level references plus a rewrite when |T - T_write| > 10 K, i.e. 5% x 17 mV/K x 10 K = 8.5 mV (RT-CIRC-02).
- **2 b/cell:** Q = 3.82 on a 100 mV half-spacing gives total sigma 26.2 mV, so sqrt(26.2^2 - 3 x 10^2) = **20 mV allowed drift sigma** over a 1 s hold (was 24). **1 b:** **75 mV** (was 80). **3 b:** out.
- **RTN (new):** single-trap dVt = q/(Cox A) at EOT 4 nm.
  - Planar 40 nm read FET (0.0016 um2, eta 11.6 mV): P(err) ~3e-3, so 2 b fails.
  - Vertical channel-all-around, >=0.01 um2 (eta 1.2-1.9 mV): <=1e-5 even with 3x percolation.
  - Spec: 1e-4 RTN quantile <=30 mV for 2 b, <=100 mV for 1 b. No IGZO RTN amplitude data was found (logged).

| Drift sigma, 1 s, 105 C | Raw Gaussian BER at 2 b | Max bits/cell | GB/die (16 tiers) |
|---|---|---|---|
| 10 mV | 2.1e-7 | 2 | 78 |
| 20 mV | 5.9e-5 | 1 (boundary) | 39 |
| 25 mV | 3.8e-4 | 1 | 39 |
| 50 mV | 2.2e-2 | 1 | 39 |
| 80 mV | 8.3e-2 | 0 | NO-GO |

**Window sensitivity:** 400 mV gives 2 / 48 mV (2 b / 1 b), so 2 b needs a measured window >=600 mV. 800 mV gives 30 / 101 mV.

**Energy per bit (revised; RT-CIRC-01, -05).**

Read path: cell and local RBL (8.1 fF) plus global RBL (126 fF) at 0.3 V swing, three SA comparisons and the read wordline; local data line 8.1 fJ; bond and via 2.8 fJ. All of it is doubled for unmodeled periphery, plus 50 fJ for the controller and SRAM.

| Path | pJ/bit | was |
|---|---|---|
| Near-tier read, at port | **0.121** | 0.087 |
| Near-tier 2-b write-verify (global WBL, 3 loops, ~60 ns), at port | 0.543 | 0.134 |
| 20%-write mix, at port | **0.206** | 0.097 |
| Near tier delivered, 3 mm mean (80% SM-local) | **0.374** | 0.153 at 1 mm |
| Near tier delivered, random placement (9 mm) | 0.71 | - |
| HBM at the PHY | 3.5 | 3.5 |
| HBM plus 8 mm NoC at 56 fJ/mm | **3.95** | 3.95 |

The delivered ratio is **~11x** with SM-local placement, 15x at 1 mm and 5.5x at 9 mm (was ~12x). SM-local placement is natural for decode: each GEMV weight tile and each FlashDecoding KV split is read by one SM.

**Watts saved per GPU (revised; RT-IND-01, RT-CIRC-03).**
- Decode reads every resident byte each step, so traffic share tracks resident-byte share. Share = mean of additive C/(C + 288) and HBM-shrink C/288, capped at 0.5.
- At 22 TB/s x 8 x 0.60 x (3.95 - 0.37) pJ:

| Config | GB/GPU | Share (additive / planning / shrink) | W saved |
|---|---|---|---|
| 8 x 1 b | 39 | 12 / 13 / 14% | 45 / **48** / 51 |
| 16 x 1 b (planning) | 78 | 21 / 24 / 27% | 81 / **92** / 103 |
| 16 x 2 b | 157 | 35 / 45 / 50% | 133 / **169** / 189 |

- **Planning figure: ~90 W per GPU** (was ~190 W, which needed the 16 x 2 b case).
- 5-year value at ~$16.4/W ($12/W of datacenter capacity plus $4.4/W of power at PUE 1.25): ~$1,500 per GPU (was ~$3,100).
- The 22 TB/s two-die GPU stands in for a 2028-30 backside-power accelerator (RT-IND-02). At Blackwell's 8 TB/s and 50% share the saving is ~69 W. The card's full-traffic bound is 563 W.

**Other quantities.**
- **Refresh power (78 GB):** at 105 C, 1.80 W for Si vs ~0.2 W for oxide at 2 b (0.64 s at 200 fJ/bit; was 9.7 mW); at 125 C, 7.2 W vs ~0.5 W. Hot silicon really loses availability and its retention tail.
- **Bandwidth:** 5.5 TB/s per die uses 0.13% of one tier's 64 x 8,192 subarrays and 44,000 bonds (0.10 mm2 at 1.5 um), at 11 mW/mm2.
- **Endurance:** ~2.2e9 writes/cell in 5 years vs >=1e12 measured. A row hammered every 20 ns reaches 1e12 in 5.6 h, so throttle.
- **Latency:** ~50-80 ns reads, including ~20-40 ns of row-BCH decode (was ~30-40 ns), vs ~100+ ns for HBM [ESTIMATE]. 2-b writes take ~60 ns and are posted through logic-side SRAM.

**Thermal (revised; RT-IND-05).**
- The 16-tier stack is now 3.84 um (k = 1.4 W/mK). With no vias, dT = qt/k gives +2.7 K at 1 W/mm2 and **+27 K at 10 W/mm2**.
- Power-map-sized Cu via fill fixes it: **10% over the ~15% hotspot area gives 0.93 K at 10 W/mm2**, and 3% elsewhere gives 0.29 K at 1 W/mm2, for ~1.5% capacity.
- The memory runs ~5 K below Tj: ~100 C on average, ~114 C over BSPDN hotspots (attribution uncertain), which run 1 b. This is a 1-D upper bound with no lateral spreading.

**Yield and cost (revised; RT-PROC-02, -03, -04).**
- **Logic scrap:**
  - Shorts at 0.1% per item over 4 BEOL tiers, the bond and the carrier: 0.6%.
  - Bond voids at 0.001 particles/cm2 incremental, with an 11 cm2 kill area per particle (2.5 mm void radius): 1.1%.
  - Carrier-last temporary bonds: 1%.
  - Total **2.7%** (~$21 per $800 die); carrier-only 2.3%.
  - At a merchant-grade 0.05/cm2, voids alone would scrap 43%. The pre-bond carrier inspect/re-clean/reject step is mandatory.
- **Incremental cost** [ESTIMATE]:
  - Per wafer: $2,800 for 28 nm-class CMOS, 16 x $550 tiers (>=5-6 patterned levels each, ~88 masks), $500 bond and test, $400 for carrier-last, less the $150 blank carrier: $12,350/wafer.
  - Spread over only the **38 good** logic dies (W2W has no known-good-die screen): **$9.22/GB at 16 x 1 b**, $4.61/GB at 16 x 2 b, $11.87/GB at 8 x 1 b.
  - *Was:* $1.36-3.55/GB over 64 gross sites.
  - Per GPU that is ~$420-650 against ~$790-1,500 of 5-year value. HBM-shrink placement also removes ~2 HBM4 stacks (~$1,150).

| Metric | 1-beta DDR5 | HOT-SIDE carrier (revised) |
|---|---|---|
| Density | 0.447 Gb/mm2 | 0.20-0.78 Gb/mm2 (planning 0.39), under a die that exists anyway |
| Refresh at 105 C, 1e-4 tail | 16 ms | 1 b ~3.6 s; 2 b ~0.64 s (typical cell ~103 s) |
| Read | Destructive, page restore | Non-destructive |
| Energy per bit delivered | HBM 3.95 (3.5 at the PHY); host DDR5 ~10-20 [UNVERIFIED] | 0.37 at 3 mm (0.21 at the port) |
| Cost | ~$1.48/GB component cost | $4.6-12/GB incremental; HBM4 price ~$16/GB |
| EUV / masks | Vendor-dependent | None / ~88 ArFi levels for 16 tiers |

**GO/NO-GO (revised).** Arrays of >=64 kb after <=400 C tiers, a *real* 350-400 C bond, thinning, and 400 C backside metal plus forming gas.
- **GO 1 b (planning):** drift sigma <=75 mV (1 s, 105 C), 1e-4 RTN quantile <=100 mV, 1e-4-tail retention >=1 s at 125 C (<=22.5 aA), bonded top-tier dVt <=10 mV.
- **GO 2 b (upside):** drift sigma <=20 mV in a >=600 mV window, cross-temperature residual <=10 mV (dT +/-30 K), RTN quantile <=30 mV, tail <=7.5 aA at 105 C (2-b refresh >=0.2 s at 125 C).
- **Logic:** RO shift <=1% and Vt shift <=10 mV.
- **NO-GO:** in every split, drift above 75 mV, RTN quantile above 100 mV, or tail retention below 1 s at 105 C.

## 3. What is new versus prior art

| Prior art | Date | Relation |
|---|---|---|
| imec/Arm BSPDN flow: device wafer bonded to a carrier, thinned, powered from the back (eeNews Power) | 2021 | The slot this concept fills |
| Chip Scale Review Nov/Dec 2022, p.49: BSPDN carrier replaced by an active memory wafer | 2022 | **Bars any broad "memory as carrier" claim** |
| imec memory-logic face-to-face plus BSPDN carrier (Tech Design Forums); imec CMOS 2.0 functional tiers (imec; arXiv 2510.04535) | 2023-25 | Closest architecture; assumes Si memory; expect imec IP |
| UniIC SeDRAM: W2W DRAM-on-logic, 0.88 pJ/bit, in production (XMC; MDPI) | IEDM 2020 | Bonded DRAM-on-logic, with Si DRAM |
| Samsung 10a VCT: IGZO channel plus W2W-bonded periphery (TrendForce) | 2026-04 | The incumbent adopts both ingredients |
| TSMC BEOL memory over logic (VLSI 2025); CXMT BEOL IGZO 3D DRAM (IEDM 2025) | 2025 | BEOL host precedents |
| imec 2T0C: >400 s (IEDM 2020); >200 s at 95 C, >1e12 cycles (EDL 2025); H+O anneal (IEDM 2025) | 2020-25 | The cell |
| IMECAS 4-tier 3 b/cell (VLSI 2026); SJTU IGO >30,000 s (AFM 2026); Kioxia/Nanya OCTRAM; SEL DOSRAM | 2019-26 | Multi-tier MLC; oxide-DRAM incumbents |
| U. Michigan Ga-free ZTO 2T0C (>1,500 s); Purdue 3 stacked In2O3 layers on 200 mm | -, 2026-09 | Ga-free and U.S. stacking |
| Stanford/MIT N3XT, DARPA 3DSoC; Graphcore Bow carrier; AP Memory VHM WoW DRAM [training knowledge] | 2016-23 | Monolithic memory-on-logic; a carrier with a function; WoW DRAM |
| imec BEOL IGZO 2T0C eDRAM; NUS all-BEOL IGZO/MoS2 2T0C 3D cells (NUS) | 2020-25 | BEOL-compatible oxide gain cells (named by the Stage 2 critic of I-11532) |
| Micron RAIN parity across NAND planes/dies; Chipkill symbol codes; 3D NAND bad-block management [training knowledge] | - | Erasure coding and capacity binning are established (named by the Stage 2 critic of I-00729) |
| RAAAM Si gain-cell RAM (TSMC N2, GF FDX) | 2026 | Cache only: Si gain cells hold for microseconds to milliseconds when hot |
| Taalas hard-wired weights (AMD acquiring) | 2026 | Competes for static weights only |
| US 12,666,958; US 2025/0167193; US 11,676,954; US 11,430,766; US 11,114,453; US 10,340,261 | - | FTO watch list (claims not read) |

**The genuine delta.** These are combinations, not new physics.
1. **An oxide gain-cell carrier on trailing-node CMOS** in the BSPDN slot. Earlier carrier-memory ideas assumed Si DRAM, which the stage-2 critics flagged as the killer doubt (refresh at 95-105 C).
2. **A carrier/BEOL tier split** (at most 4 BEOL tiers) that caps yield coupling. This is how the chief settled inventor disagreement #7.
3. **Fail-soft capacity binning**: logic-side remap plus tier-orthogonal erasure codes. The codes and binning themselves are established (RAIN, Chipkill, NAND bad-block management); the delta is applying them so a memory defect in a logic-bonded tier costs capacity, not a logic die.
4. **Thermal-map-aware bits per cell** (new in this dossier): 2 b over cool regions and 1 b over hotspots, set by the power map and on-die sensors, with per-level reference cells. Closest analogues: NAND SLC/MLC mode switching and DRAM temperature-compensated refresh [training knowledge].
5. **Thermal-via fill in the tier stack sized to the logic power map**, plus a hydrogen barrier that survives backside processing.

**Search gap:** this search (mostly snippets) found no published 125 C oxide 2T0C retention or MLC drift, and no BEOL-on-logic oxide gain cell with logic-shift data; BEOL-compatible 2T0C cells (imec, NUS) exist.

## 4. Show-stoppers and how persistence could get around them

*Thresholds revised after red team: 2 b <=20 mV and 1 b <=75 mV; added risks are RTN, cross-temperature reads, the 1e-4 leakage tail, bond-interface water, backside overlay, voids and contamination. See s2, s5 and s11; the table below is the pre-red-team list.*

| # | Show-stopper | Number | Workaround path |
|---|---|---|---|
| 1 | **Hot 2-b drift** from PBTI and hydrogen after the bond and backside steps | Must be <=24 mV (1 s, 105 C). A 20 mV budget is ~3 ppm of the H in one PECVD SiN tier (triage). | (a) 1 b (<=80 mV) keeps the energy win. (b) **Refresh faster:** drift ~t^0.2, so 100 ms refresh tolerates 24/0.63 = **38 mV** at 2 b for 89 GB x 8e9 x 60 fJ / 0.1 s = 0.43 W, below Si's 2 W [ESTIMATE]. (c) In-poor IGZO, H+O anneal, Al2O3 barrier. (d) IGO+HfO2, ZTO, In2O3. (e) Charge-trap write FET, 0 V hold. (f) Thermal-map bits per cell. |
| 2 | **Data-dependent PBTI** (references cannot cancel it) | No published distribution | Per-level references; data scrambling plus periodic rewrite [SPECULATIVE]; read-retry |
| 3 | **Window after kickback** | <400 mV forces 2 b to <=13 mV | Dual-gate cells (IMECAS shows 8 levels), or 1 b |
| 4 | **Thermal tax on logic** | +22.9 K at 10 W/mm2 with no vias | 3% Cu via fill (2.4 K); bitline pillars as partial fill [ESTIMATE]; AlN interlayers; bin hotspot area out |
| 5 | **Logic-killing shorts** in the bond and BEOL tiers | 0.1% per tier per 8 cm2 die means <=**1.25e-4/cm2** killer density. At 1%: 5.85% scrap. | Carrier-only build (2% scrap even at 1%). **Carrier-side isolation switches** per bitline group disconnect a shorted tier [SPECULATIVE]. Critic: WL-WL shorts load shared bitlines, so failures are not always tier-confined. |
| 6 | **Logic Vt/RO shift** from H and 400 C anneals (BEOL tiers) | Must be RO <=1%, Vt <=10 mV | Carrier-first: the logic sees only the bond anneal it already gets |
| 7 | **Carrier bow vs backside-litho overlay** | Unknown; BSPDN already needs distortion corrections | Stress-balanced back films; scanner high-order correction; mapped in carrier emulation; foundry sign-off |
| 8 | **Hot-row endurance** | 1e12 cycles in 5.6 h at one write per 20 ns | Per-row throttle; SRAM hot buffer |
| 9 | **All-oxide periphery** (BEOL only) | 3-5x Si area; 30-100 mV Vt sigma | CDS sensing; Si periphery in the carrier |
| 10 | **Gallium supply** | ~98% Chinese [UNVERIFIED-PK]; ban suspension ends 2026-11-27 | Qualify ZTO, In2O3, ITZO in Gate A |

None breaks physics. Gate A measures #1-3; the carrier and BEOL legs, #4-7.

## 5. The decisive experiment (revised after red team)

**Question.** After a BSPDN-like heat and hydrogen sequence *and a real bond*, does a <=400 C vertical oxide 2T0C array meet four tests?
- Drift sigma <=75 mV for 1 b (<=20 mV for 2 b) over 1 s at 105 C.
- 1e-4 RTN quantile <=100 mV (<=30 mV for 2 b).
- 1e-4-tail retention >=1 s at 125 C.
- For 2 b, a cross-temperature residual <=10 mV.

Two further questions:
- Does the logic underneath stay within 1% RO and 10 mV Vt?
- Does a processed carrier stay within the overlay, void and contamination budgets?

*Added by the red team:*
- RTN at the right timescale (DEV-02)
- cross-temperature reads (CIRC-02)
- the measured leakage tail (DEV-01)
- bond-interface water (DEV-03)
- in-plane distortion in place of bow (PROC-01)
- bond voids (PROC-04)
- contamination (PROC-05)
- the traffic and placement study (IND-01, CIRC-03, CIRC-05)

**Step 1. Design and model (M0-3).**
- Feed measured inputs into the model and SPICE the MLC window and kickback.
- **Carrier floorplan (new):** SA and WL-driver counts per mm2 for the hierarchical RBL, with an extracted 16-tier via (CIRC-01).
- **Trace and placement study (revised):** bytes-moved share vs resident-byte share on production dense and MoE decode traces, plus the SM-local placement fraction. The placement test passes if >=80% of reads are within 1-2 mm.
- **Claims read** for US 12,666,958 and US 2025/0167193 (IND-03).
- Design one chip: 4 mm2 **GF 22FDX** via CMC Microsystems, made in **Dresden**. It carries ring oscillators, Vt monitors, SRAM, and a 2-b sense/ADC with fast verify loops behind ~2 um landing pads.
- *The sky130 chip is dropped to fund the red-team measurements; a U.S.-only readout moves to the raise.*

**Step 2. Coupon reliability study, Gate A+ (M2-11).**
- **Arrays:** vertical channel-all-around 2T0C arrays with read-gate area >=0.01 um2 (the RTN design rule), built at **Purdue Birck** or **Georgia Tech IEN**. Each split gets >=25 arrays of 4 kb, i.e. >=1e5 cells.
- **Splits:** IGZO, In-poor IGZO, IGO and ZTO channels; H-lean vs PECVD encapsulation, with and without ALD Al2O3; **single vs series write gate** (I-12627); **-0.5 vs -0.7 V hold**.
- **Emulation:** the post-bond heat sequence: 350 C/2 h, then 400 C/30 min forming gas, then PECVD SiN, then a 400 C backside-metal anneal.
- **Real-bond split (new; DEV-03):** D2O-hydrated, plasma-activated Si cap chips with 0.5-1 um of bond oxide are fusion-bonded over the arrays, leaving the pads open, and annealed at 350-400 C. SIMS H/D is done at a DOE nanoscience center (CINT, CNM, CNMS, Molecular Foundry or CFN).
- **Measurements on >=1e5 cells per split:**
  - drift sigma at 1/10/100 s at 85/105/125 C;
  - usable window;
  - PBTI vs stored level;
  - **write-at-T1/read-at-T2 maps (dT +/-30 K) with in-row references** (new);
  - **RTN from >=100 reads ~1 s apart, plus fast reads at 1 us-1 ms spacing** (new);
  - **write-FET Vt and SS distributions, and the directly measured 1e-4 retention quantile at 105/125 C** (new);
  - **top-tier dVt after the real bond** (new).

**Step 3. BEOL-on-logic, Gate B (M4-18).**
- Tape out in M4-5; dies return around M9-10. Measure baselines.
- Post-process **2** tiers of the best Gate-A split (was 2-4). Re-measure, then bake 1,000 h at 105 C.
- Include short-monitor combs and a deliberately shorted tier behind an isolation switch.
- **New:** placement sigma <=10 mV within <=3 verify loops in <=60 ns at 105 C, using the on-chip sense (DEV-04).

**Step 4. Carrier emulation and foundry-risk proxies, Gate C (M12-22).**
- Fusion-bond an SOI "dummy logic" wafer onto a 200 mm tier coupon. Grind to the BOX, then run 400 C backside nano-via/metal plus forming gas. Map drift and the retention tail.
- **Distortion in place of bow (new; PROC-01):** film-stress maps of patterned vs blanket tiers, FEM, and wafer-geometry in-plane distortion (IPD) vs a blank-carrier reference.
- **Voids (new; PROC-04):** CSAM and Surfscan on 20 fusion-bonded 200 mm pairs with tier-emulating topography.
- **Contamination (new; PROC-05):** VPD-ICPMS/TXRF on encapsulated, bevel-cleaned coupons after the backside sequence.
- **Heater test** at 1 and 10 W/mm2, with 3% and 10% via fill.
- **Where:** a university bonder (MIT.nano, CNF, SNF) or MIT Lincoln Laboratory, with geometry metrology at NY CREATES. The carrier-last IR-release flow is requested as a vendor demo (EVG).
- Production overlay, Cu hybrid-bond pad yield and killer density are raise milestones.

**Timeline (revised):**
- M0-3: design and trace study.
- M2-11: coupons (**Gate A+, 2027-11-30**).
- M4-18: BEOL-on-logic (**Gate B, 2028-06-30**).
- M12-22: carrier emulation and proxies (**Gate C, 2028-10-31**).
- M22-24: data room.

**Experiment budget (revised; salaries and IP in s6)**

| Line | $k | was | Basis |
|---|---|---|---|
| Coupon run: sponsored research + fees (6 splits incl. series gate and hold bias, 2 lots) | 130 | 120 | [ESTIMATE] |
| Gate A real-bond split (cap chips, D2O, anneal, SIMS) | 25 | - | [ESTIMATE] |
| Bench: analyzer + pulse units, dual-zone thermal probe station, FPGA fast-read RTN capture | 85 | 80 | [ESTIMATE] |
| EDA/PDK via startup programs | 20 | 30 | [ESTIMATE] |
| 22FDX MPW, 4 mm2 x $17,997 | 72 | 72 | CMC list (snippet) |
| sky130 MPW | 0 | 15 | dropped (U.S.-only readout moves to the raise) |
| BEOL post-processing on logic dies (2 tiers) | 100 | 130 | [ESTIMATE] |
| Packaging, probe cards, bake boards | 35 | 40 | [ESTIMATE] |
| Carrier emulation incl. film stress, FEM, wafer-geometry IPD | 130 | 110 | [ESTIMATE] |
| CSAM + Surfscan void study, 20 bonded 200 mm pairs | 45 | - | [ESTIMATE] |
| VPD-ICPMS/TXRF contamination (commercial lab) | 15 | - | [ESTIMATE] |
| Thermal metrology | 20 | 25 | [ESTIMATE] |
| **Total** | **677** | 622 | Gate A+ alone: **~$240k, month 11** |

**Pre-set pass/fail numbers (revised)**

| Gate | Pass | Fail |
|---|---|---|
| A+ (M11) | **1 b (planning):** some split has drift sigma <=75 mV, RTN 1e-4 quantile <=100 mV, tail leakage <=22.5 aA at 125 C and bonded top-tier dVt <=10 mV. **2 b (upside):** drift <=20 mV in a >=600 mV window, cross-temperature residual <=10 mV, RTN quantile <=30 mV, tail <=7.5 aA at 105 C. | All splits >75 mV, or RTN quantile >100 mV, or tail >22.5 aA at 105 C, or bonded dVt >10 mV with no barrier fix. 20-75 mV, or any 2-b line missed, means 1 b. |
| B (M18) | RO <=1%, Vt <=10 mV, drift within Gate A after 1,000 h, no killer shorts in >=20 dies, isolation recovers 100% of shorted structures; 2 b also needs placement <=10 mV in <=60 ns | RO >1% that process changes cannot recover |
| C (M22) | Drift within Gate A after carrier emulation; heater adds <=1 K at 10 W/mm2 with 10% fill (model 0.93 K); FEM + IPD predict <=2 nm intrafield residual after correction; void loss consistent with <=0.001/cm2 after re-clean; In/Ga/Zn <=1e10 at/cm2 | Drift sigma up >50%; >2.5 K with 10% fill; In/Ga/Zn >1e10 at/cm2 or >2 nm predicted residual (bond-first dies; carrier-last only) |

*Honesty note (revised):*
- 20 dies cannot verify a 0.1% kill rate.
- University fabs run far above 1.25e-4/cm2 for killers and 0.001/cm2 for particles.
- Wafer-geometry IPD predicts overlay; it does not measure it.
- Gates B and C show that the mechanisms are extrinsic, isolatable and correctable. The rates and the overlay residual are foundry measurements.

## 6. The $1M, 24-month plan

The plan assumes M0 = January 2027.

| Quarter | Milestones | Gate |
|---|---|---|
| Q1 2027 | Team; Purdue/GT agreements; bench; chip design; 2 provisionals; FTO search; trace study | Bench reproduces published retention |
| Q2 2027 | 22FDX tape-out (the sky130 chip was dropped in section 5; the judges later moved Gate B onto a sky130 carrier, see `research/stage3/decision.json`); coupon lot 1 with emulation; first 85/105 C maps; file provisionals 3-4 | Window measured |
| Q3 2027 | Coupon lot 2; >=1e5-cell distributions at 85/105/125 C; dies return | - |
| Q4 2027 | **Gate A+ (2027-11-30; revised after red team: adds real-bond split, RTN, cross-T, tail)**; logic baselines; BEOL post-processing starts | **A** |
| Q1 2028 | Tiers on logic; 1,000 h bake; carrier bonds; PCT filing | - |
| Q2 2028 | **Gate B (2028-06-30)**; carrier backside steps; heater test | **B** |
| Q3 2028 | Carrier maps; energy extrapolation; model update | - |
| Q4 2028 | **Gate C (2028-10-31)**; data room; partner JDA talks; raise | **C** |

**Budget allocation:**

| Line | $k (revised after red team) | was |
|---|---|---|
| Two founder salaries, 24 months at $5k/month each | 240 | 240 |
| Experiments (s5) | 677 | 622 |
| IP (incl. claim reading in M0-3) | 40 | 40 |
| Contingency (~4.3%) | 43 | 80 |
| **Total** | **1,000** | 982 |

Inside the portfolio seed, only Gate A runs, on the shared coupon run (~$150k; ~$175k with the real-bond split). Gates B and C then become raise milestones. *Revised after red team:* the standalone $1.00M plan keeps Gate B on real 22FDX dies and adds the foundry-risk proxies (RT-IND-04).

**Team**
- **Founder A, systems/circuits** (MLC sensing, controller, remap): NVIDIA Research, Google TPU, Tenstorrent, Cerebras, d-Matrix alumni; Stanford (Mitra) or Georgia Tech (Yu) graduates [training knowledge].
- **Founder B, recruited device expert** (oxide-FET PBTI/hydrogen reliability): imec 2T0C alumni (G. S. Kar's team); Purdue (Ye), Georgia Tech (Datta/Khan/Yu), Stanford (Wong/Saraswat) groups; Intel Components Research, Micron [training knowledge].
- **Partners:** Purdue/Ye, Georgia Tech/Datta-Khan, U. Michigan (ZTO), Stanford/Wong-Mitra; MIT LL and NY CREATES (bonding); a BSPDN thermal group (arXiv 2508.02284 authors); DARPA 3DSoC alumni, Texas Institute for Electronics, NSF SBIR [training knowledge].

**IP strategy**
- **File first:**
  1. Thermal-map-aware bits per cell with per-level references. It is cheap to reduce to practice from the Gate A data.
  2. The heat-tolerant carrier: oxide tiers over carrier CMOS, power-map-sized via fill and a backside-proof hydrogen barrier, plus bond/thin/backside method claims.
- **Then:**
  3. Fail-soft binning with isolation switches.
  4. Hot-row throttling.
  5. KV and weight locality placement, patented or published defensively.
- **Revised after red team (RT-IND-03):** read the claims of US 12,666,958 and US 2025/0167193 in M0-3, before filing. Re-order the provisionals:
  1. bond-interface hydrogen control (D2O-labelled qualification method plus barrier and SiCN bond stack);
  2. cross-temperature MLC (in-row references, write-temperature tags, delta-T rewrite);
  3. carrier-last oxide-memory flow with its contamination package;
  4. RTN screen and remap;
  5. Si tier-mux carrier floorplan.

  The exit is a JDA or acquisition built on data and know-how, not royalties.
- **FTO risks:** Chip Scale Review 2022 and imec CMOS 2.0 bar broad claims; read US 12,666,958 and US 2025/0167193 first; families from SEL, Samsung, Kioxia/Nanya, TSMC, Intel, imec; Adeia hybrid-bonding patents (license via the foundry). Professional FTO opinion before the raise.

## 7. After the demo: scale path

**Partners and licensees**
- **Logic foundries own the slot.**
  - **Intel Foundry** (18A PowerVia, Arizona and Oregon) is the natural first partner: the only U.S. BSPDN line [training knowledge], and it needs differentiators.
  - **TSMC** (A16 Super Power Rail) and **Samsung Foundry** follow.
  - The product is a "memory carrier option" in the foundry's 3D kit.
  - *Revised after red team (RT-IND-02):*
    - **Timing:** the backside-power slot opens with A16/18A/14A accelerators from ~2028. Nvidia Feynman on A16 is reported, not confirmed by TSMC.
    - **Front-side-power hosts:** an SoIC/V-Cache-style face-to-back bond with TSVs is the fallback. It pays for a full extra wafer, so the free-slot advantage is lost.
    - **Raise gate:** a named BSPDN accelerator or foundry contact willing to evaluate a third-party carrier.
  - **Carrier-last flow (RT-PROC-01/05):** the memory wafer joins after backside processing, on bond and packaging tools, using inorganic IR-release temporary carriers (EVG IR LayerRelease class).
- **Accelerator makers** (NVIDIA, AMD, hyperscaler ASIC teams) set capacity and floorplan.
- **Memory makers** could supply carriers or license cell and binning IP: **Samsung** (IGZO plus W2W periphery already), **Kioxia** (OCTRAM with Nanya; CBA bonding in NAND), **Micron** (hybrid-bond licence 2022, U.S. fabs), **SK hynix** (HBM leader; this tier complements HBM).
- **Display makers** (Sharp/SEL, LG Display, BOE, Samsung Display): deepest IGZO reliability base; SEL may need a cross-licence. **Carrier fabs:** CELL-WAFER FOUNDRY (concept 9). **Tools:** Applied, Lam, EVG, Besi.

**What $10-50M buys**

| Raise | What it pays for |
|---|---|
| $10-15M | 300 mm transfer at NY CREATES or imec; 8 tiers; Mb-class arrays; Cu/SiCN bond at 1-1.5 um; short density at fab cleanliness; 1,000 h HTOL at 125 C |
| $25-35M | Joint development with a BSPDN foundry; carriers on real backside-power test logic; foundry overlay sign-off; Gb-class macro plus remap RTL |
| $50M | 16 tiers at 2 b; memory compiler; qualification package; early-adopter tape-out |

**Standards.** The interface is on-die, so no JEDEC device standard is needed. Publish a carrier-wafer spec (bond map, power, test access, bin record) via a foundry kit or imec CMOS 2.0; UCIe's 3D profile is the nearest interconnect standard [training knowledge]; the raw-BER interface follows RAW-BER CONTRACT's JEDEC grade.

## 8. Resources and America

**Scarce inputs.**
- In and Ga quantities are negligible: under 0.4% of world supply even at 40 tiers (A2).
- Gallium concentration is the risk: ~98% Chinese [UNVERIFIED-PK], and China's suspension of its export ban expires **2026-11-27**. Ga-free ZTO, In2O3 and ITZO are in Gate A.

**EUV.** None is added. The tiers use ArFi single exposure and the carrier is 28-65 nm CMOS.

**HBM tax avoided.** HBM3E needs ~3x DDR5's wafer area per bit (Micron, Hot Chips 2026). The near tier needs no TSVs, interposer or base die.

**Energy and water [ESTIMATE].**
- **Fab:** if a carrier plus 16 tiers costs about as much as one DRAM wafer (~1,300 kWh, ~8 m3 gross water; A2), that is ~0.25 kWh and ~1.6 L per GB. DDR5 is 0.42 kWh and 2.6 L per GB; HBM is ~1.0-1.3 kWh/GB.
- **Use phase:** making a 178 GB near tier takes ~45 kWh; running it saves ~10,559 kWh per GPU over 5 years. This is the portfolio's largest resource lever.

**U.S. manufacturability.** BSPDN logic: Intel 18A now, TSMC Arizona A16 later; 300 mm carrier CMOS: GF Malta, Samsung Austin, TI [training knowledge]. Demo: SkyWater Bloomington/sky130. Hybrid bonding: SkyWater Florida's SUSS XBC300 Gen2, MIT LL, NY CREATES/META Center. Deposition tools are U.S. (Applied, Lam); bonders mostly European. Weak link: 22FDX is made in Dresden, so a U.S.-only demo uses sky130 or partner GF Malta/Intel wafers.

## 9. Kill criteria (revised after red team)

All are physics-based. Dates assume M0 = January 2027. Gate A moves to M11 so it can include the real-bond split.

1. **2027-11-30 (M11).** **KILL the capacity claim** if every Gate-A split, *including the real-bond split*, exceeds 75 mV drift sigma at a 1 s hold (105 C; 48 mV at a 400 mV window) *and* still exceeds 75 mV when re-measured at a 100 ms hold (~119 mV at 1 s). *Revival:* an H-barrier plus In-poor/ZTO split at <=25 mV. *Was:* 80 mV, 2027-10-31, unbonded coupons.
2. **2027-11-30.** **KILL** if every split has 1e-4-tail retention <1 s at 105 C (measured tail leakage >22.5 aA at 0.15 fF). This includes the series-write-gate and -0.7 V-hold splits. *Revival:* a channel or passivation with write-FET sigma_Vt <=30 mV, or a measured tail <=22.5 aA.
3. **2027-11-30 (new; RT-DEV-02).** **KILL the capacity claim** if the 1e-4 RTN quantile exceeds 100 mV in every vertical split. *Revival:* a larger read gate or a lower-trap gate stack.
4. **2027-11-30.** **Drop 2 b permanently** if, in every split, any one of these holds:
   - usable window <600 mV;
   - cross-temperature residual >10 mV after in-row references (dT +/-30 K);
   - RTN quantile >30 mV;
   - 105 C tail leakage >7.5 aA.

   The concept continues at 1 b, which is already the planning case. *Was:* window <300 mV only.
5. **2028-06-30 (M18).** **Kill the BEOL tiers** (carrier-only from then on) if RO shift is >1% or Vt shift is >10 mV and process changes cannot recover it.
6. **2028-06-30.** **Downgrade the energy claim** below 4x (S from 4 to 3) if measured bitline and sense energy extrapolates to >0.9 pJ/bit at the port. The revised model gives 0.21 pJ/bit.
7. **2028-10-31 (M22).**
   - **KILL the carrier host** if drift degrades >50% after carrier emulation and fails criterion 1's 1-b line.
   - **KILL bond-first** (carrier-last only from then on) if FEM plus IPD predicts >2 nm of uncorrectable intrafield distortion, or if In/Ga/Zn exceed 1e10 at/cm2 after encapsulation and bevel clean (new; RT-PROC-01/05). *Revival for bond-first:* stress-neutral tiers measured within 1-2 nm of a blank carrier at a BSPDN partner.
8. **2028-10-31.** **Cut capacity by the excluded fraction** if the heater test adds >2.5 K at 10 W/mm2 even with 10% via fill *and* hotspot exclusion would take >30% of the area. *Revival:* AlN interlayers. *Was:* >5 K with 3% fill.
9. **2028-12-31 (M24).** **Downgrade the W/GPU claim** below 50 W if traces show the near tier's traffic share falls below its resident-byte share *and* SM-local placement serves <80% of reads within 2 mm. This is not a kill: the per-bit energy and capacity value remain. *Was:* <20% share, <77 W.

## 10. Sources

All logged in `research/sources/*.jsonl`; mostly via search snippet; patent claims not read.

**Cell and oxide memory**
- https://imec-publications.be/entities/publication/948b2190-065d-48d2-a9b9-4f4ecd22c234
- https://imec-publications.be/handle/20.500.12860/59908
- https://www.eenewseurope.com/news/imec-shows-capacitor-free-dram
- https://arxiv.org/abs/2412.07362v3
- https://sigroup.sjtu.edu.cn/files/AdvFunctMater_UltrathinOxide_DRAM_2026.pdf
- https://www.ithome.com/0/966/543.htm
- https://deepblue.lib.umich.edu/items/e6ac2d99-46aa-444a-bc41-2851e63c965c
- https://shine.nus.edu.sg/2025/02/18/1t1r-and-2toc1r-igzo-mos%e2%82%82-all-beol-3d-memory-cells/
- https://engineering.purdue.edu/ECE/News/2026/purdue-researchers-build-3d-chip-platform-for-faster-more-efficient-ai-computing
- https://www.jos.ac.cn/article/doi/10.1088/1674-4926/25050019
- https://in4.iue.tuwien.ac.at/pdfs/sispad2023/SISPAD2023_1-2.pdf
- https://www.businesswire.com/news/home/20241209099702/en/Kioxia-Develops-OCTRAM-Oxide-Semiconductor-Channel-Transistor-DRAM-Technology
- https://dc.engconfintl.org/ulsic_tft_vii/34
- https://vlsisymposium.org/wp-content/uploads/EN09_Technical-Tip-Sheet-VLSI-2025_EN_fin.pdf
- https://pc.watch.impress.co.jp/docs/column/semicon/2061772.html
- https://www.trendforce.com/news/2026/04/24/news-samsung-reportedly-produces-sub-10nm-10a-dram-working-die-using-4f-square-and-vct-targets-2028-production/
- https://anysilicon.com/news/raaam-selects-avnet-asic-as-its-vca-partner-for-tsmcs-2nm-gcram-development-and-qualification/

**Backside power, bonding and thermal**
- https://www.imec-int.com/en/articles/how-power-chips-backside
- https://www.eenewspower.com/en/imec-arm-demonstrate-backside-power-delivery/
- https://chipscalereview.com/wp-content/uploads/flipbook/30/files/basic-html/page49.html
- https://www.techdesignforums.com/?p=11005
- https://www.imec-int.com/en/articles/path-high-density-front-and-backside-wafer-connectivity
- https://arxiv.org/html/2510.04535v2
- https://www.imec-int.com/en/press/imec-and-ev-group-demonstrate-wafer-wafer-hybrid-bonding-200nm-interconnect-pitch-and-record
- https://semiengineering.com/backside-power-delivery-gears-up-for-2nm-devices
- https://arxiv.org/pdf/2508.02284v1
- https://in4.iue.tuwien.ac.at/pdfs/sispad2025/SISPAD2025_059.pdf
- https://xmcwh.com/en/site/details/300?details=1
- https://mdpi.com/2151526
- https://www.suss.com/de/news/technical-publications/suss-microtec-xbc300-gen2-neovation-microelectronics
- https://www.businesswire.com/news/home/20220222006259/en/Xperi-and-Micron-Enter-Into-License-Agreement-for-Hybrid-Bonding

**System, energy, market, supply**
- https://www.guru3d.com/story/nvidia-details-rubin-gpu-architecture-with-hbm4-nvlink-6-and-336-billion-transistors/
- https://arxiv.org/pdf/2602.18568
- https://eu.36kr.com/en/p/4002393085071497
- https://capitalandcompute.net/memory-prices/hbm/
- https://www.tomshardware.com/tech-industry/semiconductors/micron-says-the-silicon-gap-between-hbm-and-ddr5-is-widening-with-every-generation
- https://www.nextplatform.com/2026/02/19/taalas-etches-ai-models-onto-transistors-to-rocket-boost-inference/
- https://fastmarkets.com/insights/china-suspends-export-prohibition-on-superhard-materials-us
- https://www.cmc.ca/globalfoundries-22fdx-fdsoi-22-nm/
- https://www.iis.fraunhofer.DE/content/dam/iis/en/doc/il/ics/GF%20HR%20CMYK.pdf
- https://www.eenewseurope.com/en/tiny-tapeout-sees-industrial-boost-as-it-recovers-from-efabless-closure/

**Red-team response (revised after red team; `research/sources/resp-hot-side-memory.jsonl`)**
- https://www.evgroup.com/technologies/nanocleave/
- https://www.EVGroup.com/company/news/detail/ev-group-brings-revolutionary-layer-transfer-technology-to-high-volume-manufacturing-with-evgr850-nanocleavetm-system
- https://www.evgroup.com/company/news/detail/ev-group-highlights-revolutionary-temporary-wafer-bonding-and-debonding-solution-for-hbm-and-3d-dram-at-semicon-korea
- https://www.heise.de/en/news/Nvidia-to-become-TSMC-s-first-customer-for-A16-technology-10652601.html
- https://tomshardware.com/tech-industry/semiconductors/nvidia-dethrones-apple-to-debut-tsmc-a16
- https://heise.de/-9856195
- https://www.nist.gov/node/613726
- https://briefs.techconnect.org/papers/1-f-noise-and-rtsrandom-telegraph-signal-errors-in-comparators-and-sense-amplifiers/
- https://arxiv.org/abs/2001.03236v1
- Red-team sources used: Chen et al. IEEE TED 2009 (rt-CIRC), Chip Scale Review 2024 / SPIE 12496 (rt-PROC)

**Patents**
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12666958
- https://eureka.patsnap.com/triz-case/backside-package-hbm-routing
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11676954
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11430766
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11114453
- https://patents.google.com/patent/US10340261

## 11. Red-team outcome

*Owner response, 2026-11-02, to `research/redteam/rt_{DEV,PROC,CIRC,IND}.json` (19 objections). Full responses are in `research/redteam/responses_hot-side-memory.json`. The model was re-run with a RED-TEAM REVISIONS block (exit 0); output is in `research/stage3/hot-side-memory_model_output.md`, section 11. Sources are logged in `research/sources/resp-hot-side-memory.jsonl` (3 searches). Objections are answered, not deleted.*

| ID | Severity | Disposition | Action |
|---|---|---|---|
| RT-PROC-hot-side-memory-01 | FATAL | ACCEPTED-MITIGATED | Carrier-last flow (inorganic IR-release temporary carriers) becomes the baseline, so the memory wafer never sees backside litho; bond-first is kept only if the distortion residual is <=1-2 nm; Gate C measures in-plane distortion, not bow |
| RT-PROC-hot-side-memory-02 | MAJOR | ACCEPTED-DOWNGRADE | $/GB spread over 38 good logic dies, not 64 sites (x1.68); with PROC-03 etc., $1.36-3.55 becomes $4.6-12/GB |
| RT-PROC-hot-side-memory-03 | MAJOR | ACCEPTED-DOWNGRADE | Tier $300 to $550 (>=5-6 levels, ~88 masks for 16 tiers); revival: <=3 levels per tier via self-aligned multi-tier patterning |
| RT-PROC-hot-side-memory-04 | MAJOR | ACCEPTED-MITIGATED | Void term added (0.001/cm2 incremental gives 1.1%; total scrap 2.7%); pre-bond carrier inspect/re-clean/reject; CSAM on 20 pairs in seed |
| RT-PROC-hot-side-memory-05 | MAJOR | ACCEPTED-MITIGATED | Carrier-last keeps oxide tiers off backside tools; encapsulation, 2-3 mm edge exclusion, bevel clean; VPD-ICPMS <=1e10 at/cm2 in seed |
| RT-DEV-hot-side-memory-01 | MAJOR | ACCEPTED-DOWNGRADE | Tail multiplier 3x to 25x (91x unmitigated); series write gate (I-12627) plus a -0.7 V hold option; refresh-free becomes refresh-light (~225x fewer refreshes than Si for 1 b, not 6,400x) |
| RT-DEV-hot-side-memory-02 | MAJOR | ACCEPTED-MITIGATED | RTN reserve of half the raw-BER budget; vertical read gate >=0.01 um2 as a design rule; repeated-read RTN maps in Gate A; flagged cells remapped |
| RT-DEV-hot-side-memory-03 | MAJOR | ACCEPTED-MITIGATED | Real D2O-labelled 350-400 C bond split moved into Gate A (+$25k, M11); Al2O3/SiCN barrier splits |
| RT-DEV-hot-side-memory-04 | MINOR | ACCEPTED-MITIGATED | Placement 10 mV defended (verify-truncated, 9.9 mV); 2-b write quoted as ~60 ns, posted; timing measured in Gate B |
| RT-CIRC-hot-side-memory-01 | MAJOR | ACCEPTED-MITIGATED | Hierarchical floorplan (8k-cell rows, 64-cell local and 4k-cell global RBL, Si tier mux) fits 50% of a 28 nm carrier; efficiency 0.45; read 0.12, mix 0.21 pJ/b at the port |
| RT-CIRC-hot-side-memory-02 | MAJOR | ACCEPTED-DOWNGRADE | In-row references, write-temperature tags and a 10 K rewrite rule (10 mV residual); planning default moves to 1 b; cross-temperature maps in Gate A |
| RT-CIRC-hot-side-memory-03 | MAJOR | ACCEPTED-DOWNGRADE | Traffic share indexed to capacity: ~190 W becomes ~90 W planning (48-169 W) |
| RT-CIRC-hot-side-memory-04 | MINOR | ACCEPTED-MITIGATED | Inner row BCH t=23 (2.1%) under the tier RS; overhead 14.9%; +20-40 ns decode |
| RT-CIRC-hot-side-memory-05 | MINOR | ACCEPTED-MITIGATED | SM-local placement (3 mm mean) gives 0.37 pJ/b delivered, ~11x; random placement gives 5.5x; placement study in M0-3 |
| RT-IND-hot-side-memory-01 | MAJOR | ACCEPTED-DOWNGRADE | Same as CIRC-03; 5-year value ~$3,100 becomes ~$1,500 per GPU, still ~2x the near-tier cost |
| RT-IND-hot-side-memory-02 | MAJOR | ACCEPTED-MITIGATED | Premise re-dated to A16/18A/14A (~2028; Nvidia Feynman on A16 as reported); front-side-power SoIC fallback; named BSPDN contact as a raise gate |
| RT-IND-hot-side-memory-03 | MAJOR | ACCEPTED-MITIGATED | IP refocused on bond-H qualification, cross-temperature MLC, carrier-last contamination package, RTN remap and Si tier-mux floorplan; claims read in M0-3; JDA/data exit, not royalties |
| RT-IND-hot-side-memory-04 | MAJOR | ACCEPTED-MITIGATED | Partly refuted (Gate B on 22FDX is already in the $1M plan); IPD, CSAM and VPD proxies added; plan rebalanced to $1.00M |
| RT-IND-hot-side-memory-05 | MINOR | ACCEPTED-MITIGATED | 10% via fill over hotspots gives 0.93 K at 10 W/mm2 (~1.5% capacity); hotspots run 1 b; Gate C line <=1 K |

**Count:** 0 REFUTED, 13 ACCEPTED-MITIGATED, 6 ACCEPTED-DOWNGRADE, 0 ACCEPTED-KILL. Two of the mitigated items (IND-04, PROC-04) are partly refuted in their text.

**Redesigns adopted**
1. **Carrier-last flow** (PROC-01, PROC-05), replacing the **bond-first** order that today's BSPDN uses (carrier bonded before thinning and backside litho). This is distinct from the system lens's "carrier-first" tier split in s0 and s4, which is kept:
   - The logic wafer does thinning and backside processing on an inorganic IR-release temporary Si carrier (EVG IR LayerRelease class, front-end and fusion-bond compatible per the vendor).
   - It is then flipped to a second temporary carrier, and the memory wafer is hybrid-bonded to the front last.
   - Removes carrier-induced backside-overlay distortion and keeps In/Ga/Zn off the backside tools.
   - Costs $400/wafer and 1% logic scrap.
2. **Hierarchical carrier floorplan** (CIRC-01):
   - 8,192-cell rows; a 64-cell local RBL behind an oxide segment switch; a 4,096-cell global RBL; a Si 16:1 tier mux and shared 2-b SA in a **28 nm-class** carrier ($2,800).
   - Fits in 50% of the carrier at 16 tiers.
3. **Series or double-length write gate** (DEV-01, top-up I-12627):
   - Vertical, no footprint; tier 0.24 um.
   - Squares independent tails (17-36x at 50 mV vs 91x), with -0.7 V hold as a second knob.
4. **Margin budget with three new terms:**
   - RTN reserve (50% of the BER budget) with a >=0.01 um2 vertical read gate (DEV-02);
   - cross-temperature residual of 10 mV from in-row references, write-temperature tags and a 10 K rewrite rule (CIRC-02);
   - sense residual raised to 10 mV.
   - Result: 2 b <=20 mV, 1 b <=75 mV.
5. **Planning case 16 tiers x 1 b** (78 GB/GPU); 2 b is an upside gated on Gate A+.
6. **Concatenated ECC:** row BCH t=23 inside the tier-orthogonal RS(36,32), 14.9% in all (CIRC-04).
7. **SM-local placement** of GEMV tiles and KV splits (CIRC-05). **Capacity-indexed traffic share** in all watt claims (IND-01, CIRC-03).
8. **Power-map via fill** of 10% over hotspots and 3% elsewhere (IND-05). **Pre-bond carrier inspect/re-clean/reject** (PROC-04). **Encapsulation, edge exclusion and bevel clean** (PROC-05).
9. **Real bond inside Gate A**, D2O-labelled for SIMS (DEV-03).

*Top-up ideas:*
- **I-12627 (two series write transistors) is ADOPTED** (item 3). The p^2 tail holds only for independent defects, so Gate A tests single vs series gates and measures the tail directly.
- **I-12302 (plate-strip sensing) is NOT adopted.** Its ~135 vs ~14 mV gain comes from avoiding charge sharing on a long bitline in 1T1C cells. A 2T0C cell already senses through its own read FET, which is the "local gain FET per strip" that I-12302's critics said it would need. The one transferable element, sensing on a short local segment, is already in the 64-cell local RBL. The planar Micron prior art (US 5,991,216; US 8,009,460) is noted.

**Revised step-change claim.**
- **Energy per bit moved: ~10x lower than HBM** (0.37 vs 3.95 pJ/bit delivered with SM-local placement; 5.5x with random placement, 15x at 1 mm).
- **~90 W saved per GPU** at the 16 x 1 b planning case on a 2028-30 backside-power accelerator at ~22 TB/s: 48 W at 8 x 1 b, ~170 W if 2 b works.
- *Was:* ~12x and ~190 W. The per-bit factor fell ~15%, the system watts ~50%.
- Refresh-light (~225x fewer refreshes than Si at 105 C for 1 b), not refresh-free.
- **Not a cost step:** $4.6-12/GB incremental, 3-8x DDR5 cost, at or below HBM4 price. It is a premium near tier.

**Revised decisive experiment.** Gate A+ by M11 (2027-11-30), ~$240k:
- **Arrays and splits:** vertical channel-all-around IGZO, In-poor IGZO, IGO and ZTO 2T0C coupons; single vs series write gate; -0.5 vs -0.7 V hold.
- **Process:** each split after the post-bond heat/H sequence *and* a real D2O-labelled 350-400 C fusion bond.
- **Measurements on >=1e5 cells per split:**
  - drift sigma at 1/10/100 s at 85/105/125 C;
  - write-at-T1/read-at-T2 maps (dT +/-30 K) with in-row references;
  - **RTN at the right timescales:** >=100 reads ~1 s apart, plus fast reads at 1 us-1 ms;
  - write-FET Vt/SS and the directly measured 1e-4 retention quantile;
  - SIMS H/D and top-tier dVt after the bond.
- **Pass 1 b:** drift <=75 mV, RTN quantile <=100 mV, tail <=22.5 aA at 125 C, bonded dVt <=10 mV.
- **Pass 2 b:** drift <=20 mV in a >=600 mV window, cross-temperature residual <=10 mV, RTN quantile <=30 mV, tail <=7.5 aA at 105 C.
- **Then Gate B (M18):** 22FDX RO/Vt shift under 2 tiers, 1,000 h bake, placement <=10 mV in <=60 ns.
- **Then Gate C (M22):** carrier emulation with in-plane distortion (stress maps, FEM, IPD) instead of bow; CSAM on 20 bonded pairs; VPD-ICPMS; heater <=1 K at 10 W/mm2 with 10% fill.
- **Total:** $1.00M (experiments $677k), 24 months.

**Revised verdicts**
- **PHYSICALLY POSSIBLE? Yes at 1 b/cell; 2 b conditional.** No law is violated. The 1e-4 leakage tail makes the cell refresh-light (1 b: ~3.6 s at 105 C, ~1.4 s at 125 C). 2 b waits on unmeasured RTN, cross-temperature and tail numbers. Overlay and contamination are engineering risks that carrier-last sidesteps. *Was:* "Yes; the open item is a 2-bit drift number."
- **STEP CHANGE IF IT WORKS? Yes, energy per bit moved ~10x (5.5-15x), ~90 W per GPU at the planning case.** *Was:* ~12x, ~190 W. Not cost per bit.
- **PROVABLE WITH $1M IN 24 MONTHS? Partly.** Cell reliability is settled for ~$240k by M11, and the logic-shift and carrier proxies fit in $1.00M. Production backside overlay, killer-defect density, foundry materials acceptance and a named BSPDN partner need the raise. *Was:* "Partly" (unchanged), with more proxies now inside the seed.

**FINAL STATUS: DOWNGRADED.**
- **What survives:** the energy-per-bit step (~10x vs HBM). No objection kills the physics, and the FATAL one (backside overlay) has a design-around in the carrier-last flow.
- **What was cut:**
  - The system claim halved (~190 to ~90 W/GPU), because traffic share tracks capacity and the planning case drops to 1 b/cell until RTN, cross-temperature and tail data exist.
  - The refresh claim fell from "free" to "light".
  - Cost rose ~3x, to $4.6-12/GB.
- **What only a BSPDN foundry can prove:** carrier-last itself, plus the overlay, void-rate and contamination numbers.
