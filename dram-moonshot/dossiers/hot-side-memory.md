# HOT-SIDE MEMORY: refresh-free oxide gain-cell tiers in the backside-power carrier wafer, plus at most 4 tiers in the logic BEOL

*Dossier for `hot-side-memory`. Agent `dosw-hot-side-memory`, 2026-11-02.*

*Inputs: `FINAL_CONCEPTS.json/.md`, `hot-side-memory_notes.md`, the model output, `models/hot-side-memory.py` (re-run 2026-11-02, exit 0, identical output) and `MISSION.md`. Tags: [ESTIMATE] is a rule-of-thumb number; [SPECULATIVE] is untested; [training knowledge] was not re-verified.*

## 0. Header

**Thesis.** Backside power already forces a bonded carrier wafer onto every leading-edge logic die. If that carrier is a trailing-node CMOS wafer carrying 8-16 tiers of oxide gain cells, the one DRAM-class cell that holds data for minutes at junction temperature, the accelerator gets tens of GB a micrometre from its compute at about a tenth of HBM's energy per bit.

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

**Verdicts**

- **PHYSICALLY POSSIBLE? Yes.**
  - Every part is shown separately: oxide 2T0C (>200 s at 95 C, >1e12 cycles), W2W bonds at 0.2-1 um, BSPDN carriers in production. The open item is a reliability number (2-bit drift after the bond/backside sequence), not a law of physics.
- **STEP CHANGE IF IT WORKS? Yes, ~12x on energy per bit moved.**
  - 3.5 to 0.3 pJ/bit planning value (model: 0.10-0.15), saving **~190 W per Rubin-class GPU** (critic-corrected from the card's full-traffic ~205 W). Also ~6,400x fewer refreshes than silicon at 105 C and 22-89 GB per die. Not a cost-per-bit step.
- **PROVABLE WITH $1M IN 24 MONTHS? Partly.**
  - The key unknown is answered for ~$200k by month 10, and the logic-shift and carrier-emulation legs fit in $982k. A Cu-bonded carrier on production BSPDN logic and the 0.1% logic-kill spec need a foundry partner and the raise.

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

## 2. The physics and the numbers

All values below come from `models/hot-side-memory.py`.

**Density.**
- **Cell:** vertical 2T0C at 10F2, F = 40 nm (ArF-immersion single exposure, no EUV). That is 0.016 um2, or 62.5 M cells/mm2 per tier.
- **Carrier tiers:** CMOS sits under the array, so array efficiency is 0.5. RS(36,32) erasure parity costs 12.5%. Per tier-bit: 62.5e6 x 0.5 / 1.125 = **0.0278 Gb/mm2**.
- **BEOL tiers:** all-oxide periphery, which the critic sized at 3-5x Si area, gives efficiency 0.3, or 0.0167 Gb/mm2.
- **Full carrier:** 16 tiers x 2 b x 0.0278 = 0.889 Gb/mm2. Over 800 mm2 that is **89 GB per die**.

| Configuration | Gb/mm2 | vs 1-beta (0.447) | GB/die | GB/GPU (vs 288 GB HBM4) |
|---|---|---|---|---|
| Carrier 8 x 1 b | 0.222 | 0.50x | 22 | 44 (15%) |
| Carrier 8 x 2 b | 0.444 | 0.99x | 44 | 89 (31%) |
| Carrier 16 x 2 b | 0.889 | 1.99x | 89 | 178 (62%) |
| + 4 BEOL x 2 b | +0.133 | +0.30x | +13 | +27 |

*Correction carried:* the card's 30-100 GB per die becomes **22-89 GB**, plus 7-13 GB if BEOL tiers are added.

**Retention.**
From imec's >200 s at 95 C, Arrhenius at Ea = 0.8 eV gives 200 x exp[(0.8/8.617e-5)(1/378.15 - 1/368.15)] = 200 x e^-0.667 = **103 s at 105 C**. Silicon halves every 10 C from 64 ms at 85 C, to 16 ms: **6,417x**. At 125 C: 30 s vs 4 ms. Implied leakage: 0.15 fF x 100 mV / 200 s = **75 zA**. *Caveat:* no 125 C oxide 2T0C data is published; over Ea = 0.5-1.1 eV the extrapolation spans 80-132 s (105 C) and 15-61 s (125 C).

**Multi-level margin: the key unknown in numbers.**
- **2 b/cell:** in a 600 mV window the level half-spacing is 100 mV. A raw BER of 1e-4 needs Q = 3.65, so total sigma can be 27.4 mV.
- Subtract write placement (10 mV) and sense residual (8 mV) in quadrature: sqrt(27.4^2 - 10^2 - 8^2) = **24 mV allowed cell-to-cell drift sigma over a 1 s hold**.
- **1 b/cell:** 80 mV. **3 b/cell:** 0 mV, so 3 bits is out.
- **Refresh interval at 105 C**, with the 3x-leakage tail cell included: 4.4 s at 15 mV drift, 1.8 s at 20 mV.

| Drift sigma, 1 s, 105 C | Raw BER at 2 b | Max bits/cell | GB/die (16 tiers) |
|---|---|---|---|
| 10 mV | 2.8e-10 | 2 | 89 |
| 20 mV | 9.5e-6 | 2 | 89 |
| 25 mV | 1.4e-4 | 1 | 44 |
| 50 mV | 2.0e-2 | 1 | 44 |
| 80 mV | 8.1e-2 | 0 | NO-GO |

**Window sensitivity:** 400 mV gives 13 / 52 mV (2 b / 1 b); 800 mV gives 34 / 107 mV. *Correction carried:* the card's "<=20-30 / <=~50 mV" becomes **<=24 / <=80 mV at 600 mV**, gated on the measured window.

**Energy per bit.**

Cell, sense and read wordline on an 8.1 fF bitline (64 x 0.08 + 3 fF): 5.7 fJ/bit; local data line 8.1 fJ; bond and via 2.8 fJ; all doubled for unmodeled periphery, plus 50 fJ controller/SRAM.

| Path | pJ/bit |
|---|---|
| Near-tier read, at port | **0.087** |
| Near-tier 2-b write-verify, at port | 0.134 |
| 20%-write mix, at port | **0.097** |
| Near tier delivered 1 mm to the SM | **0.153** |
| HBM at the PHY | 3.5 |
| HBM plus 8 mm NoC at 56 fJ/mm | **3.95** |

**Watts saved per GPU.** 22 TB/s x 8 x 0.60 utilization x 0.50 traffic share x (3.95 - 0.30) pJ = **193 W**. For savings the model conservatively uses the card's 0.30 pJ/bit, not its own 0.153.
- **Over 5 years:** 10,559 kWh at PUE 1.25, about $845 of power or $2,313 of datacenter capacity at $12/W.
- **Range:** 77 / 193 / 347 W at 20 / 50 / 90% traffic share. At Blackwell's 8 TB/s and 50% share, only 70 W.
- *Correction carried:* the card's ~205 W assumed 100% of traffic at full bandwidth. The 22 TB/s full-traffic bound is 563 W. **The planning figure is ~190 W.**

**Other quantities.**
- **Refresh power (89 GB, 105 C):** 2.04 W Si vs 9.7 mW oxide; hot silicon really loses availability and its retention tail.
- **Bandwidth:** 5.5 TB/s per die uses 0.11% of one tier's subarrays and 44,000 bonds (0.10 mm2 at 1.5 um); 5 mW/mm2.
- **Endurance:** ~2.0e9 writes/cell in 5 years vs >=1e12 measured; a row hammered every 20 ns hits 1e12 in 5.6 h, so throttle.
- **Latency:** ~30-40 ns vs ~100+ ns for HBM [ESTIMATE].

**Thermal red flag (new in this dossier).** All logic heat crosses the 16-tier stack (3.2 um, k = 1.4 W/mK). dT = qt/k gives +2.3 K at 1 W/mm2 but **+22.9 K at 10 W/mm2 hotspots**; a 3% Cu via fill (k_eff 13.4 W/mK) cuts that to **2.4 K**. The memory runs ~5 K below Tj: ~100 C average, ~114 C over BSPDN hotspots (attribution uncertain). 1-D upper bound, no lateral spreading.

**Yield and cost.**
- **Logic scrap:** 1 - (1 - p)^6 (4 BEOL tiers, bond, carrier-side shorts) = **0.6%** at p = 0.1% (~$5 per $800 die); 5.85% at p = 1%; 16 unrepairable monolithic tiers would scrap 15%.
- **Incremental cost** [ESTIMATE]: $1,800 CMOS + 16 x $300 tiers + $500 bond/test - $150 blank = $6,950/wafer; over 64 sites x 80 GB, **$1.36/GB** (8 x 1 b: $3.55/GB).

| Metric | 1-beta DDR5 | HOT-SIDE carrier |
|---|---|---|
| Density | 0.447 Gb/mm2 | 0.22-0.89 Gb/mm2, under a die that exists anyway |
| Refresh at 85 / 105 C | 64 / 16 ms | ~404 / ~103 s (1 b); 2-b interval 1.8-4.4 s at 105 C |
| Read | Destructive, page restore | Non-destructive |
| Energy per bit moved | ~10-20 pJ host DDR5 [UNVERIFIED]; HBM 3.5 | 0.10-0.15 (0.30 planning) |
| Cost | ~$1.48/GB component cost | $1.36-3.55/GB incremental; HBM4 price ~$16/GB |
| EUV | Vendor-dependent | None |

**GO/NO-GO** (>=64 kb arrays after <=400 C tiers, 350-400 C bond anneal, thinning, 400 C backside metal plus forming gas): **GO 2 b** at drift sigma <=24 mV (1 s, 105 C, window >=600 mV; <=13 mV at 400 mV), 1e-4-tail retention >=1 s at 125 C, ring-oscillator (RO) shift <=1%, Vt shift <=10 mV. **GO 1 b** at 24-80 mV (capacity halves, energy win stays). **NO-GO** above 80 mV or below 1 s tail retention at 105 C.

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
| Stanford/MIT N3XT, DARPA 3DSoC; Graphcore Bow carrier [training knowledge] | 2016-23 | Monolithic memory-on-logic; a carrier with a function |
| RAAAM Si gain-cell RAM (TSMC N2, GF FDX) | 2026 | Cache only: Si gain cells hold for microseconds to milliseconds when hot |
| Taalas hard-wired weights (AMD acquiring) | 2026 | Competes for static weights only |
| US 12,666,958; US 2025/0167193; US 11,676,954; US 11,430,766; US 11,114,453; US 10,340,261 | - | FTO watch list (claims not read) |

**The genuine delta.** These are combinations, not new physics.
1. **An oxide gain-cell carrier on trailing-node CMOS** in the BSPDN slot. Earlier carrier-memory ideas assumed Si DRAM, which the stage-2 critics killed on refresh at 95-105 C.
2. **A carrier/BEOL tier split** (at most 4 BEOL tiers) that caps yield coupling. This is how the chief settled inventor disagreement #7.
3. **Fail-soft capacity binning**: logic-side remap plus tier-orthogonal erasure codes.
4. **Thermal-map-aware bits per cell** (new in this dossier): 2 b over cool regions and 1 b over hotspots, set by the power map and on-die sensors, with per-level reference cells.
5. **Thermal-via fill in the tier stack sized to the logic power map**, plus a hydrogen barrier that survives backside processing.

**Search gap:** no published 125 C oxide 2T0C retention or MLC drift, and no BEOL-on-logic oxide gain cell with logic-shift data.

## 4. Show-stoppers and how persistence could get around them

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

## 5. The decisive experiment

**Question.** After a BSPDN-like heat and hydrogen sequence, does a <=400 C oxide 2T0C array keep drift sigma <=24 mV (2 b) or <=80 mV (1 b) over 1 s at 105 C, with 1e-4-tail retention >=1 s at 125 C, and does the logic underneath stay within 1% RO and 10 mV Vt?

**Step 1. Design and model (M0-3).**
- Feed measured inputs into the model; SPICE the MLC window and kickback; run a traffic-share trace study. Design two chips:
  - 4 mm2 **GF 22FDX** via CMC Microsystems, made in **Dresden** (card's "Malta" corrected): ring oscillators, Vt monitors, SRAM, 2-b sense/ADC behind ~2 um landing pads;
  - **sky130** via ChipFoundry (SkyWater, Bloomington MN): same readout plus heaters.

**Step 2. Coupon drift study, Gate A (M2-10).**
- **Arrays:** 1-4 kb planar and vertical 2T0C arrays, built at **Purdue Birck** (Peide Ye's ALD In2O3 platform) or **Georgia Tech IEN** under sponsored research.
- **Six splits:** IGZO, In-poor IGZO, IGO and ZTO channels; H-lean ALD vs PECVD SiN encapsulation; with and without an ALD Al2O3 barrier.
- **Emulation:** half of each wafer runs the post-bond sequence: 350 C/2 h, then 400 C/30 min forming gas, then PECVD SiN, then a 400 C backside-metal anneal.
- **Measurements:** at 85/105/125 C on >=1e5 cells per split: drift sigma at 1/10/100 s, usable window, PBTI vs stored level.
- **Hydrogen:** SIMS at a DOE nanoscience center (CINT, CNM, CNMS, Molecular Foundry, CFN; free for non-proprietary work [training knowledge]).

**Step 3. BEOL-on-logic, Gate B (M4-18).**
- Tape out M4-5; dies return ~M9-10; measure baselines. Post-process 2-4 tiers (die-level e-beam, best Gate-A split), re-measure, then bake 1,000 h at 105 C. Include short-monitor combs and a deliberately shorted tier behind an isolation switch.

**Step 4. Carrier emulation, Gate C (M12-22).**
- Fusion-bond an SOI "dummy logic" wafer face-to-face onto a 200 mm tier coupon; grind to the buried-oxide stop (<1 um left); run 400 C backside nano-via/metal plus forming gas; probe the tiers through backside pad openings. Map drift, retention tail, bow and distortion before and after. Heater test at 1 and 10 W/mm2, with and without 3% via fill.
- **Where:** a university bonder (MIT.nano, CNF, SNF) or **MIT Lincoln Laboratory** (full version). Cu hybrid-bond pad yield is a raise milestone (NY CREATES or MIT LL).

**Timeline:** M0-3 design; M2-10 coupons (Gate A); M4-18 BEOL-on-logic (Gate B); M12-22 carrier emulation (Gate C); M22-24 data room.

**Experiment budget** (salaries and IP in s6)

| Line | $k | Basis |
|---|---|---|
| Coupon run: sponsored research + fees (6 splits, 2 lots) | 120 | [ESTIMATE] |
| Bench: used analyzer + pulse units, thermal probe station, FPGA | 80 | [ESTIMATE] |
| EDA/PDK via startup programs | 30 | [ESTIMATE] |
| 22FDX MPW, 4 mm2 x $17,997 | 72 | CMC list (snippet) |
| sky130 MPW, 100 chips | 15 | ChipFoundry |
| BEOL post-processing on logic dies | 130 | [ESTIMATE] |
| Packaging, probe cards, bake boards | 40 | [ESTIMATE] |
| Carrier emulation, university (the card's full MIT LL version: $250-400k) | 110 | [ESTIMATE] |
| Thermal metrology | 25 | [ESTIMATE] |
| **Total** | **622** | Gate A alone: **~$200k, month 10** |

**Pre-set pass/fail numbers**

| Gate | Pass | Fail |
|---|---|---|
| A (M10) | Some split: drift sigma <=24 mV in a window >=600 mV (<=13 mV at 400 mV); tail retention >=1 s at 125 C (tail leakage <=7.5 aA) | All splits >80 mV, or tail <1 s at 105 C. 24-80 mV means 1 b. |
| B (M18) | RO <=1%, Vt <=10 mV, drift within Gate A after 1,000 h, no killer shorts in >=20 dies, isolation recovers 100% of shorted structures | RO >1% that process changes cannot recover |
| C (M22) | Drift within Gate A after carrier emulation; heater adds <=5 K at 10 W/mm2 with vias (model: 2.4 K); bow increase <=10% [ASSUMPTION] | Drift sigma up >50%, or >5 K with vias |

*Honesty note:* 20 dies cannot verify a 0.1% kill rate, and university fabs run far above 1.25e-4/cm2. Gate B shows only that shorts are extrinsic and isolatable; the rate itself is a foundry measurement.

## 6. The $1M, 24-month plan

The plan assumes M0 = January 2027.

| Quarter | Milestones | Gate |
|---|---|---|
| Q1 2027 | Team; Purdue/GT agreements; bench; chip design; 2 provisionals; FTO search; trace study | Bench reproduces published retention |
| Q2 2027 | 22FDX + sky130 tape-out; coupon lot 1 with emulation; first 85/105 C maps; file provisionals 3-4 | Window measured |
| Q3 2027 | Coupon lot 2; >=1e5-cell distributions at 85/105/125 C; dies return | - |
| Q4 2027 | **Gate A (2027-10-31)**; logic baselines; BEOL post-processing starts | **A** |
| Q1 2028 | Tiers on logic; 1,000 h bake; carrier bonds; PCT filing | - |
| Q2 2028 | **Gate B (2028-06-30)**; carrier backside steps; heater test | **B** |
| Q3 2028 | Carrier maps; energy extrapolation; model update | - |
| Q4 2028 | **Gate C (2028-10-31)**; data room; partner JDA talks; raise | **C** |

**Budget allocation:**

| Line | $k |
|---|---|
| Two founder salaries, 24 months at $5k/month each | 240 |
| Experiments (s5) | 622 |
| IP | 40 |
| Contingency (~9%) | 80 |
| **Total** | **982** |

Inside the portfolio seed, only Gate A runs, on the shared coupon run (~$150k). Gates B and C then become raise milestones.

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
- **FTO risks:** Chip Scale Review 2022 and imec CMOS 2.0 bar broad claims; read US 12,666,958 and US 2025/0167193 first; families from SEL, Samsung, Kioxia/Nanya, TSMC, Intel, imec; Adeia hybrid-bonding patents (license via the foundry). Professional FTO opinion before the raise.

## 7. After the demo: scale path

**Partners and licensees**
- **Logic foundries own the slot.**
  - **Intel Foundry** (18A PowerVia, Arizona and Oregon) is the natural first partner: the only U.S. BSPDN line [training knowledge], and it needs differentiators.
  - **TSMC** (A16 Super Power Rail) and **Samsung Foundry** follow.
  - The product is a "memory carrier option" in the foundry's 3D kit.
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

## 9. Kill criteria

All are physics-based. Dates assume M0 = January 2027.

1. **2027-10-31 (M10).** **KILL the capacity claim** if every Gate-A split exceeds 80 mV drift sigma at a 1 s hold (105 C, after emulation; 52 mV at a 400 mV window) *and* still exceeds 80 mV when re-measured at a 100 ms hold (~127 mV at 1 s). *Revival:* an H-barrier plus In-poor/ZTO split at <=25 mV.
2. **2027-10-31.** **KILL** if every split has 1e-4-tail retention <1 s at 105 C, i.e. tail leakage >22.5 aA at 0.15 fF. *Revival:* a channel or passivation that keeps the tail <=22.5 aA.
3. **2027-10-31.** **Drop 2 b permanently** if the usable window is <300 mV in every split. The concept continues at 1 b with half the capacity.
4. **2028-06-30 (M18).** **Kill the BEOL tiers** (carrier-only from then on) if RO shift >1% or Vt shift >10 mV and process changes cannot recover it.
5. **2028-06-30.** **Downgrade the energy claim** below 4x (S from 4 to 3) if measured bitline and sense energy extrapolates to >0.9 pJ/bit at the port.
6. **2028-10-31 (M22).** **KILL the carrier host** if drift degrades >50% after carrier emulation and fails criterion 1's 1-b line.
7. **2028-10-31.** **Cut capacity by the excluded fraction** if the heater test adds >5 K at 10 W/mm2 even with vias *and* hotspot exclusion would take >30% of the area. *Revival:* AlN interlayers.
8. **2028-12-31 (M24).** **Downgrade the energy-axis value** if traces show <20% of HBM traffic can be placed on the near tier (<77 W saved). This is not a kill: the capacity value remains.

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

**Patents**
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12666958
- https://eureka.patsnap.com/triz-case/backside-package-hbm-routing
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11676954
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11430766
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11114453
- https://patents.google.com/patent/US10340261
