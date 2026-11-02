# HOT-SIDE MEMORY: dossier research notes

Agent `dos-hot-side-memory`, 2026-11-02. Concept rank 2 (EV 64) in `FINAL_CONCEPTS.md`. Model: `models/hot-side-memory.py` (output: `research/stage3/hot-side-memory_model_output.md`). Sources: `research/sources/dos-hot-side-memory.jsonl`. Assumptions: `research/assumptions/dos-hot-side-memory.md`. This session had 6 web searches; everything else comes from earlier phases' source logs (marked CROSS-REF) or is tagged [ESTIMATE] / [training knowledge].

## 0. The concept in one paragraph, and what this dossier changed

Backside power delivery (BSPDN: Intel 18A PowerVia, TSMC A16 Super Power Rail) flips the finished logic wafer, bonds its front-side BEOL to a carrier wafer, grinds the original substrate away and builds the power network on the back ([imec](https://www.imec-int.com/en/articles/how-power-chips-backside); [eeNews Power, 2021](https://www.eenewspower.com/en/imec-arm-demonstrate-backside-power-delivery/)). The carrier then faces the heat sink, so anything in it runs near junction temperature. HOT-SIDE MEMORY makes that carrier a trailing-node CMOS wafer carrying 8-16 tiers of oxide-semiconductor 2T0C gain cells, hybrid-bonded face-to-face to the logic. At most 4 more tiers go in the logic BEOL. Oxide gain cells are the one DRAM-class cell that tolerates heat: >200 s retention at 95 C, >1e12 cycles ([imec EDL 2025](https://imec-publications.be/entities/publication/948b2190-065d-48d2-a9b9-4f4ecd22c234), CROSS-REF).

**What the dossier adds or corrects:**
1. **The headline numbers survive first-principles arithmetic.**
   - Near-tier energy is 0.10 pJ/bit at the controller port (0.15 pJ/bit delivered 1 mm to the consuming SM), against ~3.5 pJ/bit for HBM. The card's 0.3 pJ/bit has ~2-3x headroom.
   - At 105 C the oxide cell needs refreshing ~6,400x less often than silicon.
2. **The "~205 W per accelerator" claim needs weighting.** The near tier carries only part of the traffic, and HBM is not used at 100%. With Rubin-class HBM4 (22 TB/s per GPU), 60% utilization and 50% of traffic on the near tier, the saving is **~190 W per GPU**: ~$850 of electricity over 5 years, or ~$2,300 of datacenter power capacity freed. The full-traffic upper bound is ~560 W.
3. **The key unknown now has a number.** At a raw BER of 1e-4 and a 600 mV usable window, the cell-to-cell level drift over a 1 s hold at 105 C must be **<=24 mV for 2 b/cell** (<=13 mV if the window is only 400 mV) and **<=80 mV for 1 b**. 3 b/cell needs an >=800 mV window and <=9.5 mV of drift, so the card was right to stop at 2 b.
4. **New red flag (thermal).** In BSPDN all logic heat crosses the carrier tiers. An unvia'd 16-tier oxide stack (~3.2 um at k ~1.4 W/mK) adds ~2 K at 1 W/mm2 but **~23 K over 10 W/mm2 hotspots**.
   - Fix: ~3% Cu/W thermal-via fill (back to ~2 K), or keep tiers off hotspots and bin that area out.
   - The demo must include a heater test of this.
5. **Correction.** GF 22FDX MPW wafers are made in **Dresden**, not Malta ([Fraunhofer IIS](https://www.iis.fraunhofer.DE/content/dam/iis/en/doc/il/ics/GF%20HR%20CMYK.pdf), via snippet).
   - A U.S.-made logic host means SkyWater S130/sky130 (Bloomington MN) or a partner's GF Malta/Intel wafers.
   - 22FDX is still the better high-k/metal-gate sensitivity host for the logic-shift test.
6. **Cost is not a blocker.**
   - The incremental carrier cost is ~$1.4-3.6/GB, depending on tiers and bits/cell, against a DDR5 component cost of ~$1.48/GB.
   - That is 5-12x below the HBM4 price of ~$16/GB ([Capital and Compute, 2026-07](https://capitalandcompute.net/memory-prices/hbm/), CROSS-REF).

## 1. Model headline (from `models/hot-side-memory.py`)

| Quantity | Value | Basis |
|---|---|---|
| Density per tier-bit | 0.0278 Gb/mm2 (carrier, eff 0.5); 0.0167 (BEOL, eff 0.3) | 10F2 at F = 40 nm, 12.5% erasure parity |
| Footprint density | 0.22 (8x1 b) to 0.89 (16x2 b) Gb/mm2 = 0.5-2.0x 1-beta (0.447) | s1 |
| Capacity per 800 mm2 die | 22 / 44 / 44 / 89 GB (8x1, 8x2, 16x1, 16x2 b); +7-13 GB from 4 BEOL tiers | s1 |
| Per 2-die GPU vs 288 GB HBM4 | 44-178 GB = 15-62% of HBM bits | s1 |
| Retention at 105 / 125 C (1 b) | ~103 s / ~30 s (Ea 0.8 eV; 80-132 s / 15-61 s over 0.5-1.1 eV) vs Si 16 / 4 ms | s2 |
| 2-b refresh interval at 105 C | 4.4 s at 15 mV drift sigma; 1.8 s at 20 mV (tail droop included) | s3 |
| Allowed drift sigma (1 s, 105 C) | 2 b <= 24 mV; 1 b <= 80 mV (600 mV window) | s3-4 |
| Energy, near tier | 0.087 read, 0.134 2-b write-verify, 0.097 mixed pJ/b at port; 0.15 delivered | s5 |
| Energy, HBM | 3.5 pJ/b at PHY; ~3.95 delivered (+8 mm NoC) | s5 |
| Watts saved per GPU | 77 / 193 / 347 W at 20 / 50 / 90% traffic share (22 TB/s, 60% util) | s5 |
| Bandwidth feasibility | 5.5 TB/s per die needs 0.11% of one tier's subarrays active and 44k bonds (0.1 mm2 at 1.5 um) | s6 |
| Endurance | ~2e9 writes per cell in 5 yr vs >=1e12 measured (512x); single hot row must be throttled | s6 |
| Logic scrap | 0.6% at 0.1% kill per tier/bond with 4 BEOL tiers (vs 15% for 16 unrepairable tiers) | s8 |
| Incremental $/GB | $1.36 (16x2 b) to $3.55 (8x1 b) carrier; $2.3-4.7 BEOL | s9 |

## 2. Prior art and who is pursuing it (closest first)

**Architecture: memory in or as the BSPDN carrier / memory-on-logic tier stacking**

| Who | What | Date | Relation |
|---|---|---|---|
| imec (CMOS 2.0) | Stacked functional tiers (logic, memory, ESD, regulators) joined by W2W hybrid bonding with BSPDN. W2W favoured for memory-on-logic, ~400 nm-pitch W2W shown at VLSI 2025 ([imec](https://www.imec-int.com/en/articles/path-high-density-front-and-backside-wafer-connectivity); [arXiv 2510.04535](https://arxiv.org/html/2510.04535v2), via snippet) | 2024-2025 | **Closest architectural prior art.** It frames memory as a bonded tier, not specifically an oxide gain-cell carrier on trailing-node CMOS. Expect imec IP here. |
| imec | Face-to-face memory-on-logic in a BSPDN stack (Stage 2 critique of I-11538, via snippet) | ~2023-25 | Same slot, with Si memory assumed |
| Chip Scale Review | "Memory wafer replaces BSPDN carrier" (Stage 2 critique, via snippet) | 2022 | Published idea, so the bare architectural claim is likely not patentable as a broad claim |
| UniIC (Xi'an) SeDRAM | W2W hybrid-bonded DRAM-on-logic | IEDM 2020 [training knowledge, via Stage 2] | Proves DRAM-on-logic bonding, with Si DRAM |
| Graphcore Bow; AP Memory VHM | Functional (power/capacitor) carrier wafer by WoW; WoW DRAM | 2022- | Carrier with function |
| Samsung 10a 4F2 VCT | IGZO-channel DRAM with periphery wafer-bonded underneath, targeting 2028 ([TrendForce, 2026-04-24](https://www.trendforce.com/news/2026/04/24/news-samsung-reportedly-produces-sub-10nm-10a-dram-working-die-using-4f-square-and-vct-targets-2028-production/), CROSS-REF) | 2026 | Incumbent adopts both oxide channel and W2W bonding |
| Stanford/MIT N3XT; DARPA 3DSoC (MIT, Stanford, SkyWater) | Monolithic memory-on-logic at <400 C (CNFET + RRAM on SkyWater 200 mm) [training knowledge] | 2016-2023 | Monolithic BEOL route; SkyWater has done <=400 C BEOL device integration |
| Patents | See s6 | | |

**Cell: oxide gain cells (2T0C/3T0C) and BEOL oxide memory**

| Who | Best number | Date |
|---|---|---|
| imec (G. S. Kar's team) | 2T0C: >400 s, 45 nm Lg, 300 mm (IEDM 2020); >1e3 s, >1e11 cycles, 14 nm Lg (IEDM 2021); **>200 s at 95 C, >1e12 cycles, <10 ns write at 95 C, 40 nm Lg (EDL 2025)**; H+O anneal cuts H-doping under PBTI ~30x, targeting 1.2 V overdrive for 5 yr at 95 C (IEDM 2025) ([EDL](https://imec-publications.be/entities/publication/948b2190-065d-48d2-a9b9-4f4ecd22c234); [IEDM 2025](https://imec-publications.be/handle/20.500.12860/59908); CROSS-REF) | 2020-2025 |
| imec | In-poor IGZO (In <=17%) more H-resilient; forming-gas damage and H-driven PBTI are distinct mechanisms ([arXiv 2412.07362](https://arxiv.org/abs/2412.07362v3), CROSS-REF) | 2024-12 |
| SJTU | IGO 2T0C with HfO2 passivation: **>30,000 s**, 10 ns write, 4 b/cell ([AFM 2026](https://sigroup.sjtu.edu.cn/files/AdvFunctMater_UltrathinOxide_DRAM_2026.pdf), CROSS-REF) | 2026 |
| IMECAS + Beijing Super String | 4 tiers in one stacking step, dual-gate IGZO 2T0C, **3 b/cell, 400 s** (VLSI 2026) ([IT Home](https://www.ithome.com/0/966/543.htm), CROSS-REF) | 2026-06 |
| CXMT | BEOL IGZO 3D DRAM select device, 60.9 uA/um, SS 80 mV/dec (IEDM 2025) ([PC Watch](https://pc.watch.impress.co.jp/docs/column/semicon/2061772.html), CROSS-REF) | 2025-12 |
| TSMC | Memory array fully in BEOL over advanced logic, oxide-semiconductor selector + low-T capacitor, density above SRAM (VLSI 2025) ([VLSI tip sheet](https://vlsisymposium.org/wp-content/uploads/EN09_Technical-Tip-Sheet-VLSI-2025_EN_fin.pdf), CROSS-REF) | 2025-06 |
| Kioxia + Nanya | OCTRAM 275 Mb, Ioff <1 aA (IEDM 2024); 3D OCTRAM 8-layer horizontal IGZO (IEDM 2025) ([BusinessWire](https://www.businesswire.com/news/home/20241209099702/en/Kioxia-Develops-OCTRAM-Oxide-Semiconductor-Channel-Transistor-DRAM-Technology), CROSS-REF) | 2024-25 |
| SEL | CAAC-IGZO DOSRAM, leakage <=200 zA ([ULSIC-TFT 2019](https://dc.engconfintl.org/ulsic_tft_vii/34), CROSS-REF) | 2019 |
| U. Michigan | First Ga-free ZTO 2T0C, >1,500 s ([Deep Blue](https://deepblue.lib.umich.edu/items/e6ac2d99-46aa-444a-bc41-2851e63c965c), CROSS-REF) | - |
| Purdue (P. Ye) | Three vertically stacked ALD In2O3 transistor layers on 200 mm Si, >100,000 devices over 52 dies ([Purdue, 2026-09-16](https://engineering.purdue.edu/ECE/News/2026/purdue-researchers-build-3d-chip-platform-for-faster-more-efficient-ai-computing), CROSS-REF) | 2026-09 |
| J. Semicond. 2026 | Charge-trap write transistor keeps >1,000 s at 0 V hold, so no negative hold rail ([JoS 47(2)](https://www.jos.ac.cn/article/doi/10.1088/1674-4926/25050019), via snippet) | 2026-02 |
| Sogang (attribution by index) | a-IGZO write + c-Si read hybrid: >4,800 s, 5-bit levels ([ScholarWorks](https://scholarworks.sogang.ac.kr/item/2007b65f-cef1-441a-941f-e046a52b6244), via snippet) | - |
| SISPAD 2023 | Simulation: stacked 2T0C arrays self-heat through inter-tier crosstalk, which shortens retention ([SISPAD 2023](https://in4.iue.tuwien.ac.at/pdfs/sispad2023/SISPAD2023_1-2.pdf), via snippet) | 2023 |
| RAAAM (Si GCRAM) | Si gain-cell RAM on a TSMC N2 test chip (2026-03); GF FDX collaboration ([AnySilicon](https://anysilicon.com/news/raaam-selects-avnet-asic-as-its-vca-partner-for-tsmcs-2nm-gcram-development-and-qualification/); [Silicon Saxony](https://silicon-saxony.de/en/globalfoundries-and-raaam-memory-technologies-development-of-next-generation-gcram-technology-and-a-test-chip-on-the-fdx-platform/), CROSS-REF) | 2026 |

RAAAM is a competitor for on-die cache-class memory. It is not capacity-class: Si gain cells hold only microseconds to milliseconds when hot.

**Search gap (2026-11-02):** a targeted search found **no published retention or multi-level drift data for oxide 2T0C at 125 C**, and no BEOL-on-logic oxide gain-cell demonstration with logic-shift data. That absence is the opening for a small team.

## 3. Best demonstrated numbers per component vs what the concept needs

| Component | Best shown | Needed | Gap |
|---|---|---|---|
| Retention, hot | >200 s at 95 C (imec, 1 b, single cells/small arrays) | >=1 s at 125 C for the 1e-4 tail after the post-bond sequence | Margin ~30x on typical cells; tail and post-sequence unknown |
| Retention, room temp | >30,000 s (SJTU IGO + HfO2 passivation) | - | Large interface headroom |
| Multi-level | 3 b/cell 400 s (IMECAS, 4 tiers); 4 b (SJTU); 5-bit hybrid (Sogang) | 2 b with <=24 mV drift sigma at 105 C | No drift distribution at temperature published |
| Endurance | >1e12 cycles at 95 C (imec) | ~2e9 per cell average over 5 yr | OK; per-row hot-spot throttling |
| Write speed | <10 ns at 95 C (imec) | <=20 ns cycle | OK |
| PBTI / H | H+O anneal 30x less H-doping; 5-yr 95 C target (imec IEDM 2025) | Survive bond anneal + 400 C backside FGA; trackable long-term drift | Key unknown |
| Tiers | 4 in one step (IMECAS); 3 In2O3 layers on 200 mm (Purdue); 8 transistor layers (Kioxia) | 8-16 carrier tiers | Engineering |
| W2W hybrid bond pitch | 300 nm (imec ECTC 2025); 400 nm (imec VLSI 2025) | 1-2 um | Mature |
| HBM interface energy | HBM3E 3.44 pJ/b ([arXiv 2602.18568](https://arxiv.org/pdf/2602.18568)); HBM4 3-4 pJ/b ([36Kr](https://eu.36kr.com/en/p/4002393085071497)) | Beat by >=10x | Model: 0.10-0.15 pJ/b |
| Accelerator HBM | Rubin 288 GB HBM4, 8 stacks, up to 22 TB/s ([Guru3D](https://www.guru3d.com/story/nvidia-details-rubin-gpu-architecture-with-hbm4-nvlink-6-and-336-billion-transistors/)); one report says 19.2 TB/s ([pasqualepillitteri.it](https://pasqualepillitteri.it/news/27545/nvidia-ritira-22-tbs-vera-rubin-hbm4-nvlink-6), unverified) | - | - |
| BSPDN thermal | Hotspots up to ~14 C hotter than front-side power ([arXiv 2508.02284](https://arxiv.org/pdf/2508.02284v1), attribution uncertain); Samsung SISPAD 2025: results depend strongly on boundary conditions ([SISPAD 2025](https://in4.iue.tuwien.ac.at/pdfs/sispad2025/SISPAD2025_059.pdf)); "may exacerbate" ([SemiEngineering](https://semiengineering.com/backside-power-delivery-adds-new-thermal-concerns)) | Memory at <=125 C locally | Test at 105/125 C; thermal vias |

## 4. Physics notes from the model (things a reviewer will ask)

1. **Why the carrier beats the BEOL as the primary host (beyond yield).**
   - The carrier tiers sit behind ~10 um of logic BEOL and a bond layer, which contain SiN/SiCN barrier films, during the post-bond backside PECVD and forming-gas steps.
   - So they probably see less hydrogen than BEOL tiers do [ESTIMATE, untested].
   - The decisive experiment should measure both hosts with the same cell split.
2. **Thermal position.**
   - Memory runs ~5 K below junction on average: ~100 C at a 105 C design Tj, and ~114 C over BSPDN hotspots.
   - The tiers also add thermal resistance in the logic's heat path. That is ~2 K at 1 W/mm2 but ~23 K at 10 W/mm2 hotspots unless ~3% thermal-via fill is used.
   - Vertical-pillar 2T0C arrays already contain vertical metal (bitline and plate pillars), which may supply part of that fill [ESTIMATE].
3. **Drift spec, decomposed.** The 2-b budget is a 100 mV half-spacing divided by Q = 3.65, giving 27 mV total sigma. That is placement (10 mV) + sense (8 mV) + drift (24 mV) in quadrature.
   - **Common-mode drift** (all cells in a row shift together) is removed by per-row reference cells written at the same time.
   - **What counts against the spec** is the cell-to-cell and *data-dependent* part. PBTI on the read transistor depends on the stored level, so "1" cells drift more than "0" cells; that drift is the risk.
   - Long-term (5-yr) drift is tracked by reference recalibration, like NAND read-retry.
4. **The energy win does not depend on bits/cell.** A 1-b fallback halves capacity (to 22-44 GB per die) but keeps ~12x interface energy and the refresh win. The concept has a soft landing.
5. **Refresh is not about watts.**
   - Si refresh for 89 GB at 105 C is ~2 W; oxide is ~10 mW.
   - Si loses availability (tRFC/tREFI) and the retention tail at temperature.
   - The real system wins are no-PHY latency (~30-40 ns vs ~100+ ns) and the interface energy.
6. **Honest value per GPU.**
   - Energy: ~190 W, about $850 of electricity or ~$2,300 of DC power capacity over 5 yr. Material, but smaller than the capacity value.
   - Capacity: 44-178 GB of near-tier bits at ~$1.4-3.6/GB of cost would displace HBM bits priced at ~$12-16/GB, worth ~$700-2,800 per GPU at HBM4 prices.
   - The pitch to accelerator makers is **energy + capacity + latency together**.

## 5. U.S. facilities and services (with any cost/rate information)

**Logic hosts (MPW shuttles)**

| Service | Node / where made | Cost info | Use |
|---|---|---|---|
| CMC Microsystems (GF 22FDX) | 22 nm FD-SOI, made in Dresden | **$24,075/mm2 (1 mm2 minimum, 100 untested dies); $17,997/mm2 (4 mm2 minimum)**; a ~6 mm2 die was $108,342 ([CMC](https://www.cmc.ca/globalfoundries-22fdx-fdsoi-22-nm/), via snippet; rate-to-customer mapping unclear) | High-k/metal-gate logic-shift host (ring oscillators, Vt FETs, SRAM) plus driver/sense pads for oxide arrays |
| ChipFoundry (sky130) | SkyWater 130 nm, Bloomington MN (IonQ-owned since 2026-07-31) | ~$15k per 100 chips ([eeNews Europe](https://www.eenewseurope.com/en/tiny-tapeout-sees-industrial-boost-as-it-recovers-from-efabless-closure/); [IonQ](https://ionq.com/news/ionq-completes-acquisition-of-skywater-technology), CROSS-REF) | Cheap U.S.-made first host for flow learning; MLC sense/ADC test chip |
| Cadence SKY130 MPW | SkyWater 130 nm | $10-12k per design block (CROSS-REF, SkyWater) | Alternative |
| wafer.space (GF180MCU) | 180 nm, made in Singapore | ~$7-7.5k per 1,000-die slot ([Crowd Supply](https://www.crowdsupply.com/wafer-space/gf180mcu-run-2), CROSS-REF) | Cheapest readout chip, not U.S.-made |
| MOSIS 2.0 (USC ISI) | 12-350 nm, >35 shuttles (CROSS-REF) | Quote | Broker |

**Oxide tier deposition (BEOL-temperature ALD/sputter, e-beam lithography)**

| Facility | Fit | Rate info |
|---|---|---|
| Purdue Birck (Peide Ye's ALD In2O3; 200 mm 3-layer platform) | Best fit for vertical/stacked oxide transistors at BEOL temperature | Not verified [UNVERIFIED]; sponsored research is the realistic mode |
| Georgia Tech IEN (Suman Datta, Asif Khan, Shimeng Yu groups) | Oxide-semiconductor BEOL transistors, gain-cell/eDRAM benchmarking, ferroelectrics [training knowledge] | Not verified |
| Stanford SNF (H.-S. P. Wong, S. Mitra, K. Saraswat, E. Pop) | N3XT/BEOL memory-on-logic heritage; oxide and 2D channels [training knowledge] | Not verified; external-user rates apply |
| MIT.nano; Cornell CNF; Penn Singh Center; ASU NanoFab; UT Austin (MRC, Texas Institute for Electronics) | General ALD/e-beam/bonding; TIE is a DARPA 3D heterogeneous-integration prototyping center [training knowledge] | Not verified |
| SkyWater Bloomington (BEOL integration / engineering runs) | Industrial <=400 C BEOL module on a U.S. 200 mm line (3DSoC heritage) [training knowledge] | Quote; a dedicated 130 nm mask set is ~$500-600k ([AnySilicon](https://anysilicon.com/130nm-wafer-mpw-cost/), CROSS-REF) |

**Bonding / thinning / backside emulation**

| Facility | Fit |
|---|---|
| MIT Lincoln Laboratory (200 mm 3D integration, oxide bonding) | Carrier emulation (bond, thin, backside); partner or user [training knowledge] |
| NY CREATES Albany (300 mm; memory-device JDA with Fraunhofer IPMS ([idw, 2025-05-16](https://nachrichten.idw-online.de/2025/05/16/ny-creates-and-fraunhofer-ipms-announce-joint-development-agreement-to-advance-memory-devices-at-300mm-wafer-scale), CROSS-REF)) and Applied Materials META Center | 300 mm hybrid bonding; raise-stage partner |
| Texas Institute for Electronics (UT Austin); SkyWater Florida | 3D heterogeneous-integration prototyping [training knowledge] |
| University EVG-class fusion bonders (MIT.nano, CNF, SNF) [training knowledge] | Cheapest oxide-oxide fusion bond + SOI-stop thinning for the stress/thermal/H emulation |

**Characterization (national-lab user facilities)**
- **Facilities:** Sandia/LANL CINT, Argonne CNM, ORNL CNMS, LBNL Molecular Foundry, Brookhaven CFN.
- **Measurements:** SIMS/ToF-SIMS hydrogen depth profiles through the tier stack, STEM/EELS of oxide interfaces, nano-thermal imaging.
- **Cost:** DOE nanoscience centers give user time free for non-proprietary work through peer-reviewed proposals; proprietary work pays full cost recovery [training knowledge].
- **NIST CNST NanoFab:** fee-based and open to industry.
- **Sandia MESA:** a trusted Si fab; a partner only if a government sponsor appears.

## 6. Potential collaborators and recruits

- **Device expert (founder #2), target profile.** Someone who has taken an oxide 2T0C or IGZO BEOL transistor through PBTI/hydrogen reliability.
  - Pools: imec's 2T0C program alumni (Gouri Sankar Kar's memory team; lead authors on the IEDM 2020-21 2T0C papers) [training knowledge]; PhD graduates of the Datta (Georgia Tech), Ye (Purdue), Wong/Saraswat (Stanford) and Shimeng Yu (Georgia Tech) groups; Intel Components Research or Micron oxide-TFT alumni [training knowledge, unverified].
- **Sponsored-research partners (seed).**
  - Purdue/Ye: ALD In2O3/IGZO, vertical oxide FETs, 200 mm multi-layer platform.
  - Georgia Tech/Datta and Khan: BEOL oxide gain cells and PBTI.
  - Stanford/Wong and Mitra: memory-on-logic system co-design.
  - U. Michigan: the ZTO 2T0C authors, for the Ga-free channel.
- **Thermal.** A BSPDN thermal-modeling group: the arXiv 2508.02284 authors; Samsung's SISPAD 2025 team (industrial). Plus a U.S. thermal-metrology lab (thermoreflectance) [training knowledge].
- **Industry (raise stage).**
  - Intel Foundry: 18A PowerVia (Arizona/Oregon), the only U.S. BSPDN line in production [training knowledge].
  - TSMC Arizona: A16 later.
  - imec: CMOS 2.0 program membership, an IP-licence path.
  - Accelerator makers: NVIDIA, AMD, hyperscaler ASIC teams.
  - Tool makers for bonding and H-lean deposition: Applied Materials (META Center), Lam, EVG.

## 7. Decisive experiment: design, budget, timeline

**Question:** after the full BSPDN-like sequence, does a <=400 C oxide 2T0C array keep the level drift sigma <=24 mV (2 b) or <=80 mV (1 b) over a 1 s hold at 105 C, with a 1e-4-tail retention >=1 s at 125 C? And does building it on logic shift the logic by <=1% ring-oscillator frequency and <=10 mV Vt?

**Step by step**

1. **M0-3, design and modeling.**
   - Extend `models/hot-side-memory.py` with measured inputs as they arrive.
   - SPICE the 2T0C MLC window and kickback.
   - Run a trace-driven estimate of the traffic share (TP weight slice + hot KV) using open inference traces.
   - Design two test chips:
     - a 4 mm2 22FDX die: ring-oscillator banks, Vt-monitor FETs, an SRAM block, and driver/sense/2-b ADC circuits behind top-metal landing pads at ~2 um pitch for 1-4 kb oxide arrays;
     - a sky130 die with the same readout, plus a heater/thermal-sensor array for the hotspot test.
2. **M2-10, coupon drift study (answers the key unknown first).**
   - Build 1-4 kb planar and vertical 2T0C arrays on 150/200 mm Si/SiO2 wafers at Purdue Birck or Georgia Tech IEN under sponsored research.
   - Six-way split: standard IGZO, In-poor IGZO, IGO, ZTO (Ga-free); H-lean ALD encapsulation vs PECVD SiN; with and without an ALD Al2O3 H-barrier.
   - Run each wafer half through the **post-bond emulation**: 350 C/2 h bond anneal, then 400 C/30 min forming gas, then a PECVD SiN "backside passivation", then a 400 C backside-metal anneal.
   - Measure with a bench MLC tester (parameter analyzer with fast pulse units, thermal-chuck probe station, FPGA write-verify controller) at 85/105/125 C:
     - retention tails over >=1e5 cells per split;
     - 1-b and 2-b drift sigma at 1 s, 10 s and 100 s;
     - usable window;
     - PBTI vs stored level.
   - **Gate A (M10):** at least one split meets <=24 mV, so the plan stays at 2 b. If only <=80 mV, go to 1 b. If >80 mV in every split, NO-GO, pending an H-barrier revival.
3. **M4-18, BEOL-on-logic.**
   - Tape out the 22FDX and sky130 dies (M4-5). Dies return at ~M9-10; the wafer.space run took 12 weeks at GF ([Crowd Supply](https://www.crowdsupply.com/wafer-space/gf180mcu-run-1)), and 22FDX MPW turns are ~4-6 months [ESTIMATE].
   - Measure logic baselines (RO, Vt, SRAM Vmin).
   - Post-process 2 oxide tiers (4 if time allows) at <=400 C on dies, using die-level e-beam lithography and the best Gate-A split.
   - Re-measure the logic. Run a 1,000 h, 105 C bake/operate (6 weeks) with periodic 2-b drift maps.
   - **Gate B (M18):** RO shift <=1%, Vt shift <=10 mV, array drift within the Gate-A threshold, and no logic-killing shorts across >=20 dies.
4. **M12-22, carrier emulation.**
   - Oxide-tier coupon wafers (200 mm) are oxide-fusion-bonded face-down onto SOI "dummy logic" wafers. The SOI BOX serves as the etch stop in place of SiGe, which is cheaper.
   - Thin to <1 um, then run backside nano-via/metal at 400 C plus forming gas.
   - Map the retention tail, 2-b drift and overlay/bow before and after.
   - Run the heater test vehicle under the coupon at 1 and 10 W/mm2, with and without thermal-via fill, to verify the ~2 K vs ~23 K prediction.
   - Do this at a university bonder (lean) or at MIT Lincoln Laboratory (full).
   - Fine-pitch hybrid-bond pad yield is a raise milestone at NY CREATES or MIT LL.
5. **M20-24, data room.** Package for the raise:
   - drift/retention distributions vs temperature;
   - logic-shift data;
   - the thermal-via result;
   - an updated model with measured inputs;
   - provisional patents converted to PCT.

**Budget (seed <= $1M, 24 months)**

| Line | $k | Basis |
|---|---|---|
| Founder salaries, 2 x 24 months x $5k/month (lean) | 240 | ESTIMATE |
| Sponsored research + user fees, coupon run (Purdue Birck or GT IEN; 6 splits, 2 lots) | 120 | ESTIMATE |
| Test bench: used parameter analyzer + fast pulse units, thermal-chuck probe station, FPGA MLC controller | 80 | ESTIMATE (used-equipment market) |
| EDA, PDK access, design (startup programs) | 30 | ESTIMATE |
| 22FDX MPW, 4 mm2 x $17,997 | 72 | [CMC](https://www.cmc.ca/globalfoundries-22fdx-fdsoi-22-nm/) list (via snippet) |
| sky130 MPW (ChipFoundry, 100 chips) | 15 | CROSS-REF eeNews |
| BEOL post-processing on logic dies (e-beam, ALD, etch; university fab) | 130 | ESTIMATE |
| Packaging, probe cards, 1,000 h 105 C bake/operate boards | 40 | ESTIMATE |
| Carrier emulation: fusion bond + SOI-stop thin + backside 400 C (university; MIT LL as an upgrade) | 110 | ESTIMATE (card: $250-400k at MIT LL/NY CREATES for the full hybrid version) |
| Thermal metrology (heater vehicle, IR/thermoreflectance) | 25 | ESTIMATE |
| IP: 4 provisionals + 1 PCT | 40 | ESTIMATE |
| Contingency (~9%) | 80 | - |
| **Total** | **982** | **< $1M** |

The decisive answer to the key unknown (Gate A) costs **~$200k** (coupon run + bench) and arrives by **month 10**. If HOT-SIDE runs inside the portfolio seed, only Gate A (on the shared oxide coupon run) is seed-funded. BEOL-on-logic and the carrier then become raise milestones, as `FINAL_CONCEPTS.md` already plans.

**Timeline**

| Months | 0-3 | 3-6 | 6-10 | 10-14 | 14-18 | 18-22 | 22-24 |
|---|---|---|---|---|---|---|---|
| Design/model | X | x | | | | | x |
| Coupon drift study | | X | X (Gate A) | | | | |
| MPW tape-out / fab | | X | X | | | | |
| BEOL-on-logic post-process + 1,000 h | | | | X | X (Gate B) | | |
| Carrier emulation + heater test | | | | X | X | X | |
| Data room / raise | | | | | | X | X |

## 8. IP landscape

**Patents and filings to watch** (all via search snippet; claims not read):
- US 12,666,958, "Flexible wiring architecture for multi-die integration": logic wafer flipped and bonded to a carrier, BSPDN on the logic ([USPTO](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12666958)). **Read the claims first:** does the carrier carry active circuits?
- US 2025/0167193 A1: BSPDN with a memory module coupled to the signal network (secondhand summary, [PatSnap](https://eureka.patsnap.com/triz-case/backside-package-hbm-routing)). Verify against the filing.
- US 11,676,954: bonded memory-on-CMOS, carrier removed, backside source power mesh ([USPTO](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11676954), CROSS-REF).
- US 11,444,068: 3D IC with BSPDN ([USPTO](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11444068)).
- US 12,354,982: memory with backside bond pads under the array ([USPTO OG](https://patentsgazette.uspto.gov/week27/OG/html/1536-2/US12354982-20250708.html)).
- US 11,430,766: DRAM cell array and periphery on separate wafers, hybrid-bonded (CROSS-REF). US 10,340,261 / US 10,600,772: cell chip bonded to a logic chip holding SAs and word drivers. US 11,996,389: logic-on-DRAM-cell bond (Stage 2 critique of I-11192, via snippet).
- SEL CAAC-IGZO DOSRAM family (e.g., US 10,276,578) on oxide-semiconductor memory cells (CROSS-REF).
- Expect dense families from imec (CMOS 2.0, 2T0C), Samsung (VCT + bonded periphery), Kioxia/Nanya (OCTRAM), TSMC (BEOL oxide memory over logic), Intel (PowerVia carrier) and CXMT. Run a professional freedom-to-operate search before the raise.
- The bare idea "memory wafer as the BSPDN carrier" was published in 2022 (Chip Scale Review), so it is prior art against broad architectural claims.

**What to file (provisionals in months 0-6, ~$40k)**
1. **Heat-tolerant carrier memory.**
   - Structure: a BSPDN carrier comprising oxide-semiconductor gain-cell tiers over trailing-node CMOS periphery, face-to-face bonded to logic. It is defined by a thermal-via fill in the tier stack sized to the logic power map, and by H-barrier encapsulation that survives post-bond backside processing.
   - Method claims: the bond, thin, backside sequence with tiers resident in the carrier.
2. **Thermal-map-aware bits-per-cell.**
   - Per-region bits/cell (2 b over cool regions, 1 b over hotspots) set from the logic floorplan's power map and on-die thermal sensors.
   - Per-row reference cells track common-mode drift; regions are rebinned in the field.
   - This is new in the dossier and cheap to reduce to practice in the Gate-A data.
3. **Fail-soft capacity binning.** A logic-side remap table plus tier-orthogonal erasure codes (RS across tiers), so a W2W-bonded memory defect lowers a capacity bin rather than scrapping logic.
4. **Locality-aware placement.** Runtime/compiler mapping of tensor-parallel weight slices and hot KV to the near-tier region above the consuming SM cluster, which is what makes the 0.15 pJ/b delivered number real. Patent it, or publish it defensively.
5. **Write-throttle / hot-row policy for gain-cell endurance**, plus PBTI-aware hold-bias scheduling (using the 0 V-hold charge-trap write transistor as an option).

## 9. Open gaps

1. **No 125 C oxide 2T0C retention or MLC drift data** was found in public sources (search 2026-11-02). The 105/125 C numbers in the model are Arrhenius extrapolations from one 95 C point with an assumed Ea (0.8 eV; 0.5-1.1 swept) and an assumed retention criterion (100 mV).
2. **The usable window after kickback** for a vertical 2T0C at F = 40 nm is unknown. The 2-b drift limit moves from 13 to 34 mV across a 400-800 mV window, so Gate A must measure the window and the drift together.
3. **Data-dependent PBTI** (a stored "1" stresses the read transistor more than a "0") is not separable by reference cells. No published distribution exists.
4. **BSPDN process details are proprietary**: carrier thickness and bonding oxide, the backside thermal budget, H sources (Intel PowerVia, TSMC SPR). The emulation sequence is a guess at the envelope. Carrier bow and overlay changes from adding tiers could disturb backside lithography, which a foundry partner must judge.
5. **The thermal tax** (~23 K at 10 W/mm2 without vias) is from a 1-D estimate. The hotspot size and power maps of real accelerators, and BSPDN's own ~14 C hotspot penalty (attribution uncertain), need 3-D simulation and the heater test.
6. **The traffic share (20-90%) and utilization (60%)** set the watts-saved number. They need a trace study on real inference workloads.
7. **HBM energy** for HBM4 at 2.5-4 pJ/b, and Rubin bandwidth at 22 vs 19.2 TB/s, are not settled. The ratio stays >=8x across that range.
8. **University fab rates, MIT LL and NY CREATES pricing, and DOE user-facility terms** were not verified this session.
9. **Claims of the key patents** (US 12,666,958; US 2025/0167193) were not read.
10. **Ga supply:** IGZO's Ga is ~98% Chinese (A2). The ZTO/IGO/In2O3 splits in Gate A double as the supply-chain hedge, but Ga-free channels have less hot-retention data.
11. **Product question (not physics).** Variable near-tier capacity per die (fail-soft bins) must be acceptable to accelerator SKUs and their software.
