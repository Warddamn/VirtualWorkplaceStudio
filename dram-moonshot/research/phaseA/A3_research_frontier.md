# A3: The 2022–2026 research frontier for DRAM and DRAM replacements

**Agent:** `A3-frontier` · **Written:** 2026-11-01 · **Phase:** A (bottleneck map), part 3 of 3

**Companion files**
- Model: `research/models/A3_frontier_estimates.py` (standard library only; `python3` exits 0).
- Sources: `research/sources/A3-frontier.jsonl` (74 entries).
- Assumptions: `research/assumptions/A3-frontier.md`.
- Sibling work: `A1_scaling_limits.md` (physics walls) and `A2_materials_resources.md` (resource intensity). This file gives the frontier evidence; A1 and A2 give the bottlenecks it attacks.

**How this was researched**
- 30 of 30 WebSearch calls, and no WebFetch: IEEE Xplore, arXiv and TrendForce were unreachable.
- Every fact taken from the web comes from a search snippet and is tagged *(via search snippet)* in the jsonl. Most venue papers (IEDM, VLSI, IMW) were seen only through press releases, institutional repository records or trade-press previews, never as full text.
- Numbers therefore carry these tags:
  - `[REPORTED]`: secondary source or snippet.
  - `[CO-REPORTED]`: company claim, no peer review.
  - `[ESTIMATE]`: my arithmetic, done in the model.
  - `[UNVERIFIED]`: could not confirm.
  - `[CROSS-REF]`: reused from a `ram-venture` device card, not re-opened by this agent.
- Framing follows MISSION.md: ideas are judged on physics only, never killed for business reasons, and every kill names a revival condition.

---

## 0. Key findings in twelve lines

1. **Oxide-semiconductor channels have won the incumbents' next-DRAM bet.**
   - Samsung: 4F² VCT working die with an IGZO channel, targeting 2028 [CROSS-REF].
   - Kioxia: 3D OCTRAM, with 8-layer horizontal IGZO transistors at Ion >30 µA and Ioff <1 aA (IEDM 2025) [REPORTED].
   - CXMT: BEOL IGZO 3D DRAM (IEDM 2025, paper 29-3) [REPORTED].
   - IMECAS: 4-tier 2T0C at 3 bits/cell and 400 s (VLSI 2026) [REPORTED].
   - SK hynix: 4F² vertical-gate DRAM (VLSI 2026) [REPORTED].
2. **Best oxide gain-cell numbers today.**
   - Retention >30,000 s, 10 ns write, 4 bits/cell: IGO 2T0C with HfO₂ passivation (Adv. Funct. Mater. 2026, SJTU) [REPORTED].
   - >200 s at 95 °C, >10¹² cycles, <10 ns write at Lg = 40 nm: imec, EDL 2025 [REPORTED].
3. **Retention in oxide gain cells is set by interfaces, not by the channel.**
   - The results imply only ~7–200 zA of *total* storage-node leakage.
   - Passivation alone bought 100×.
   - "Days" of retention (10⁵–10⁶ s, effectively refresh-free) needs ≤0.2–2 zA. That is a materials and interface problem, not a bandgap problem [ESTIMATE, model §1].
4. **Oxide mobility is not a blocker at DRAM-class speed.**
   - A 20–40 nm IGZO read device develops 100 mV on a 64-cell read bitline in ~1–2 ns, or ~8–15 ns for 3-bit sensing [ESTIMATE, model §2].
   - The "IGZO is slow" complaint is an SRAM/eDRAM-speed complaint.
5. **Multi-level × tiers is the density lever nobody has built at array level.**
   - A vertical 2T0C at F = 20 nm needs b×N ≥ 3.7 (bits/cell × tiers) to match 1β density.
   - At F = 40 nm (single-exposure ArF immersion, no EUV, no multipatterning) it needs b×N ≥ 15: 3 bits × 5 tiers [ESTIMATE, model §3].
6. **Ferroelectric memory reached Gb scale and is going 3D.**
   - Micron's 32 Gb dual-layer NVDRAM, with a 1e15-cycle endurance claim (press) [REPORTED].
   - CXMT monolithic 3D FeRAM (IEDM 2025) [REPORTED].
   - Notre Dame / Penn State / IBM / Fraunhofer / NUS 2T-64C cell, "hundreds of layers" (IEDM 2025) [REPORTED].
   - HZO arrays elsewhere show ~10¹¹ cycles [CROSS-REF], against ~10¹⁵ needed for DRAM-class use without wear-levelling [ESTIMATE, model §4].
7. **Capacitor-less silicon is quietly back.**
   - Unisantis/imec DFM on 65 nm SOI: >10 s at 85 °C (IMW 2025) [REPORTED].
   - NEO 3D X-DRAM single-cell PoC: >1 s at 85 °C, >10¹⁴ cycles, <10 ns [CO-REPORTED].
   - Neither has published array data.
8. **3D silicon DRAM is still at 5–16 tiers.**
   - Samsung 16-tier VS-DRAM reads and writes at chip level (VLSI 2026) [REPORTED].
   - SK hynix 5-layer at 56.1% yield (2024) [CROSS-REF].
   - Every 3D and 4F² program now uses **wafer bonding of periphery to cells** (peri-on-cell or periphery-under-cell).
9. **MRAM does not reach DRAM-class density or endurance in one device.**
   - SOT: >10¹⁵ cycles at <100 fJ, but only a 4 kb field-free array (imec, IEDM 2025).
   - VCMA: 6–20 fJ at 0.5–1 ns, but ~10¹⁰ cycles, last shown at the 2020 frontier.
   - STT: cell 0.017 µm², 16× a 1β cell [CROSS-REF].
10. **2D materials reproduce oxide retention without beating it.** MoS₂ 2T0C gives >1,000 s, 20 ns writes and 0.2 fJ; Si-MoS₂ eDRAM gives 6,000 s and 5 ns. The yield story starts with Fudan's 94.34% (Nature 2025) [REPORTED].
11. **PIM DRAM is shipping-class but it is an overlay, not a new cell.**
    - Samsung LPDDR5X-PIM: 8× internal bandwidth (614 vs 76.8 GB/s), 3.01× Llama-3.1-8B throughput, mass production end-2026 or early 2027 [REPORTED].
    - The measured speed-up implies ~76% of runtime is offloadable [ESTIMATE, model §8].
12. **Cryogenic DRAM is killed for data centres on system energy, not on device physics.**
    - At 77 K a refrigerator costs ~10–19 W at the wall per W removed, so a 12 W RDIMM costs 38–64 W at the wall [ESTIMATE, model §6].
    - It lives only where the cooling is already paid for.

**Top three white spaces** (detail in §5):
- **(1)** Multi-level, non-destructive oxide gain-cell DRAM with write-verify.
- **(2)** A deposition-stacked ferroelectric 2T-nC tier: one transistor pair, tens of BEOL capacitors.
- **(3)** "Disaggregated" bonded DRAM: a litho-light oxide cell-stack wafer bonded to a foundry periphery wafer at ~1 µm pitch.

---

## 1. Scorecard: every frontier family on one page

The DRAM-class bar is ~10–100 ns access, ≥10¹⁵ cycles (or architecture that tolerates less), and density competitive with 1β (~0.44–0.47 Gb/mm² die-level).

| Family | Best demonstrated numbers (2022–26) | TRL | Who leads | DRAM-class status |
|---|---|---|---|---|
| **IGZO/IGO/In₂O₃ 2T0C gain cell (planar)** | >30,000 s, 10 ns write, 4 b/cell (SJTU 2026). >200 s at 95 °C, >10¹² cycles, <10 ns write, Lg 40 nm (imec 2025). >10³ s, Lg 14 nm (imec 2021) | 4 | imec, SJTU, IMECAS, Purdue, Georgia Tech | Speed OK, endurance OK, density per tier 4–35× worse than 1β |
| **3D oxide 2T0C** | 4 tiers in one stacking step, 3 b/cell, 400 s (IMECAS + Beijing Super String, VLSI 2026) | 3 | IMECAS, NEO (3T0C TCAD), NUS (IGZO/MoS₂ all-BEOL) | Alive. The best density path (§3, §5-1) |
| **Oxide 1T1C 4F² (VCT/OCTRAM)** | 275 Mb OCTRAM array, WL 54 / BL 63 nm pitch, Ion >15 µA, Ioff <1 aA (Kioxia+Nanya, IEDM 2024) [CROSS-REF]. Samsung 10a 4F² IGZO VCT working die, periphery wafer-bonded, 2028 [CROSS-REF] | 5–6 | Samsung, Kioxia/Nanya, SK hynix (4F² VG), CXMT (4F² DDR5 by end-2026) | Incumbent roadmap. Keeps the HAR capacitor |
| **3D oxide 1T1C / horizontal IGZO** | 8-layer horizontal IGZO transistors via SiN→IGZO replacement, Ion >30 µA, Ioff <1 aA, no retention published (Kioxia, IEDM 2025). BEOL IGZO 3D DRAM select device at 60.9 µA/µm, Vt 0.28 V, SS 80 mV/dec (CXMT, IEDM 2025) | 3 | Kioxia, CXMT | Transistor-level only |
| **3D Si DRAM (VS-DRAM, lateral 1T1C)** | 16 tiers, GAA + horizontal capacitor, chip-level R/W, Cs ∝ capacitor length, peri-on-cell bonded (Samsung, VLSI 2026). 5-layer at 56.1% yield (SK hynix, 2024). 120 Si/SiGe bilayers grown (imec 2025) [CROSS-REF A1] | 4 | Samsung, SK hynix, imec | Alive. Needs 32–192 tiers. Epi defects and horizontal capacitor unsolved |
| **Capacitor-less Si 1T (floating body / DFM / 3D X-DRAM)** | DFM on 65 nm SOI (300 mm): >10 s at 85 °C, BL disturb 10 ms at 2.5 V (IMW 2025). NEO PoC: >1 s at 85 °C, >10¹⁴ cycles, <10 ns, single cell [CO-REPORTED] | 3–4 | Unisantis + imec, NEO + NYCU/TSRI | Revived. No array data |
| **Ferroelectric 1T1C NVDRAM** | 32 Gb dual-layer, 5.7 nm FE cap. 10¹⁵ cycles (press), 10-yr retention (one unverified source) (Micron, IEDM 2023) | 5–6 | Micron (shelved), FMC (DRAM+, no public silicon), SK hynix/Samsung research | Physics proven at Gb scale. Endurance on reads is the issue |
| **3D FeRAM / 2T-nC** | 2T-64C cell fabricated. FN-discharge read removes sequence dependence but costs read endurance (ND/PSU/IBM/Fraunhofer/NUS, IEDM 2025). Two-tier 1T1C (Georgia Tech). Monolithic 3D FeRAM (CXMT, IEDM 2025). 1 Mb HZO 1T1C: 10¹¹ cycles, 1 month at 85 °C [CROSS-REF] | 3 | Notre Dame (K. Ni), Georgia Tech, CXMT, Fraunhofer IPMS | Alive. White space §5-2 |
| **FeFET (hafnia)** | Embedded NVM on 22–28 nm [CROSS-REF]. Memory window closes with trapping: 1.2 → 0.45 V after 10⁴ cycles at ±5 V. Samsung IGZO/HZO FeFET for eNVM (IEDM 2025) | 5 (eNVM) / 2 (DRAM-class) | GF/FMC, Samsung, Fraunhofer | Fails DRAM-class endurance by >10⁸× |
| **SOT-MRAM** | Field-free perpendicular, 4 kb array, <10 ns (imec, IEDM 2025). >10¹⁵ cycles, <100 fJ, ~50 nm CD (imec, IEDM 2023). 210 ps (2018). 2 Kb array claiming 10¹⁸ (Nano Research 2026, contested) | 4 | imec; foundry programs undisclosed | SRAM/LLC-class speed and endurance; density far from DRAM |
| **VCMA-MRAM (MeRAM)** | 20 fJ at 1.1 GHz, >10¹⁰ cycles, TMR 246%, field-free (imec 2020). 6 fJ at 0.5 ns (Spintec) | 3 | imec, Spintec, UCLA lineage | Energy is DRAM-beating. Endurance and write-error rate are not |
| **STT-MRAM** | Samsung eMRAM 0.024 µm² (14 nm) and 0.017 µm² (8 nm) [CROSS-REF] | 9 (embedded) | Samsung, TSMC, Everspin | ~16× 1β cell area |
| **2D (MoS₂/WSe₂) gain cells** | MoS₂ 2T0C: 20 ns, >1,000 s, 0.2 fJ/write (ACS Nano 2025). Hybrid-gate MoS₂ 2T0C, wafer-scale CVD, >100 s, multi-bit (NSR 2025). Si-MoS₂ eDRAM: 6,000 s, 5 ns, 35 µA/µm margin (Nat. Commun. 2024). MoS₂ memory chip on Si at 94.34% yield (Fudan, Nature 2025). 2D semi-floating gate: 10 s, 15 ns (2018) | 2–3 | Fudan (P. Zhou, C. Liu), NUS, PolyU | No retention edge over oxide. Growth and yield are the gate |
| **Hybrid bonding / wafer-on-wafer DRAM** | W2W hybrid bonding at 300 nm pitch (imec, ECTC 2025). Production use in Samsung VCT (PUC) and in SK hynix 4F² VG with die thinning [REPORTED]. HBM hybrid bonding delayed to HBM4E/HBM5 [CROSS-REF A1] | 5–6 (DRAM) | Samsung, SK hynix, imec, YMTC-style patents | The enabling process of the decade |
| **PIM DRAM** | LPDDR5X-PIM: 16 GB, 614 GB/s internal, 2.28× wall-clock and 3.01× throughput on Llama-3.1-8B (Hot Chips 2026). HBM-PIM: 300 MHz FP16 per bank, AMD reports up to 85% data-movement energy saved. GDDR6-AiM: 16 Gbps | 7–8 | Samsung, SK hynix | Shipping-class overlay |
| **Cryogenic DRAM (77 K)** | Commercial DDR3 reaches 4,096 s refresh at 77 K once 6 weak rows are excluded (JSTS 2022). IGZO 2T0C: 8,000 s at 77 K (2025). CryoRAM: 3.8× speed or 9.2% power (simulation). Hammer-like failures appear when refresh is cut (CryoGuard) | 3–4 | SKKU, Rambus/Microsoft (2017), BGU/BIU | Killed for data centres on system energy (§6) |

---

## 2. Family by family

Each entry gives the frontier, the open problems, and what is still untried.

### 2.1 Oxide-semiconductor gain cells (2T0C / 3T0C), planar and 3D

**Frontier**
- **imec lineage.**
  - IEDM 2020: 45 nm Lg on 300 mm, >400 s, extracted Ioff 3×10⁻¹⁹ A/µm ([eeNews 2020](https://www.eenewseurope.com/news/imec-shows-capacitor-free-dram)).
  - IEDM 2021: >10³ s and >10¹¹ cycles, Lg down to 14 nm ([TechXplore 2021](https://techxplore.com/news/2021-12-capacitor-less-igzo-based-dram-cell-excellent.html)).
  - EDL 2025: Lg 40 nm holds >200 s **at 95 °C**, >10¹² cycles, <10 ns write at 95 °C. The gains came from removing sidewall metal residue, a negative hold voltage and gate-oxide optimisation ([imec record](https://imec-publications.be/entities/publication/948b2190-065d-48d2-a9b9-4f4ecd22c234)) [REPORTED].
- **Record retention.** An IGO 2T0C with HfO₂ passivation reaches >30,000 s, 100× its unpassivated control, with a 10 ns write and 4-bit storage ([SJTU, Adv. Funct. Mater. 2026](https://sigroup.sjtu.edu.cn/files/AdvFunctMater_UltrathinOxide_DRAM_2026.pdf)) [REPORTED].
- **3D.** IMECAS with Beijing Super String showed a dual-gate IGZO 2T0C with a vertical wordline: four tiers formed in **one** stacking step, a record 3 bits/cell, 400 s retention. Paper: "Highly stackable 3D DRAM of Dual-gate IGZO 2T0C with Record 3 bits/cell and 400s Data Retention", VLSI 2026 ([IT Home](https://www.ithome.com/0/966/543.htm)) [REPORTED].
- **Heterogeneous cells.**
  - Si-MoS₂ eDRAM (MoS₂ write, Si read): 6,000 s, 5 ns ([Nat. Commun. 2024](https://doaj.org/article/5350e037ffd64032b574966642f36fb4)).
  - Hybrid IGZO-write / Si-read cell proposed because IGZO-only cells are slow at eDRAM speed ([DATE 2026](https://past.date-conference.com/proceedings-archive/2026/DATA/154.pdf)).
  - NUS all-BEOL IGZO/MoS₂ 2T0C1R cells ([NUS 2025](https://shine.nus.edu.sg/2025/02/18/1t1r-and-2toc1r-igzo-mos%e2%82%82-all-beol-3d-memory-cells/)).
- **Reliability.**
  - imec IEDM 2025 targets 1.2 V overdrive for 5 years at 95 °C. Standard and In-poor IGZO drift Vt in opposite directions (electron trapping vs H-doping). An H+O anneal cuts H-doping under PBTI ~30× ([imec IEDM 2025](https://imec-publications.be/handle/20.500.12860/59908)).
  - Forming-gas damage and H-driven PBTI are distinct mechanisms ([arXiv 2412.07362](https://arxiv.org/abs/2412.07362v3)) [REPORTED].
- **Thermal budget.**
  - Purdue's ALD In₂O₃ top-gate FETs survive 600 °C ([EDL 2024](https://engineering.purdue.edu/~yep/Papers/EDL_2024_In2O3%20600C_Lin.pdf)), and its vertical all-oxide TFTs reach >160 µA/µm ([VLSI 2024](https://engineering.purdue.edu/~yep/Papers/VLSI2024%20T4-1_Zehao%20Lin.pdf)).
  - Samsung reportedly showed at IEDM 2025 that a zinc-free IGO survives >550 °C ([blog](https://blog.ai.dmomo.co.kr/news/17048)) [UNVERIFIED].

**TRL:** 4 for planar cells; 3 for 3D.

**Open problems**
1. PBTI/hydrogen drift that is acceptable for *multi-level* storage. A 50 mV drift is fine for 1 bit and fatal for 3 bits.
2. Footprint per tier: planar 2T0C is ~24F²; vertical needs ~8–12F².
3. Contact resistance and Vt variability at Lg <20 nm.
4. Read-write disturb in shared-wordline 3D arrays.
5. Row-hammer and soft-error behaviour: **no data found** (also flagged in A1 §9).

**Untried or under-explored**
- (a) An **array-level** multi-level gain-cell DRAM with write-verify and ECC at DRAM latency. Only single cells or tiny arrays show 3–4 b/cell.
- (b) Pushing retention from 10⁴ to 10⁶ s by interface engineering alone. SJTU's 100× from passivation suggests large headroom.
- (c) Single-etch, NAND-style vertical-channel 2T0C at ≥16 tiers. IMECAS stops at 4; Kioxia shows transistors without cells.
- (d) Hammer and SER characterisation.

### 2.2 Oxide 1T1C: 4F² VCT, OCTRAM, 3D OCTRAM

**Frontier**
- Kioxia+Nanya OCTRAM: a 275 Mb array of vertical IGZO transistors on a HAR capacitor, Ioff <1 aA ([BusinessWire 2024](https://www.businesswire.com/news/home/20241209099702/en/Kioxia-Develops-OCTRAM-Oxide-Semiconductor-Channel-Transistor-DRAM-Technology); [Blocks & Files](https://blocksandfiles.com/2024/10/22/kioxia-developing-new-dram-scm-and-nand-tech/)) [CROSS-REF].
- **3D OCTRAM** (IEDM 2025, paper 29.1): an SiO₂/SiN stack in which the SiN is replaced by InGaZnO, forming **horizontal transistors in all tiers at once**. Ion >30 µA, Ioff <1 aA, 8 layers operating; no retention or refresh measured ([Kioxia 2025-12-12](https://www.kioxia.com/en-jp/about/news/2025/20251212-1.html)) [REPORTED].
- Samsung 10a 4F² VCT with an IGZO channel and a wafer-bonded periphery, targeting 2028 ([TrendForce 2026-04-24](https://www.trendforce.com/news/2026/04/24/news-samsung-reportedly-produces-sub-10nm-10a-dram-working-die-using-4f-square-and-vct-targets-2028-production/)) [CROSS-REF].
- SK hynix 4F² VG (VLSI 2026, T8.5): bit-line shielding, a shared back gate for Vt control, and die thinning for the wafer-bonded structure ([VLSI tipsheet](https://www.vlsisymposium.org/wp-content/uploads/2026/04/2026-VLSI-Technical-Tipsheet-REVISED-FINAL-NO-IMAGES-4.24.26.docx)). SK hynix keeps 6F² as its main platform and phases in 4F² and 3D on economics ([XenoSpectrum](https://xenospectrum.com/en/sk-hynix-dram-scaling-bonding/)) [REPORTED].

**TRL:** 5–6.

**Open problems:** the HAR capacitor remains (A1 §2); the IGZO/storage-node contact; hydrogen from the capacitor module; thermal budget (hence IGO and In-poor variants).

**Untried:** little is open to outsiders here, because this is the incumbents' main line. The one gap is that the 3D OCTRAM *replacement-channel* trick has not been published with a capacitor-less cell. That overlaps §2.1(c) and A1 white space 2.

### 2.3 3D silicon DRAM roadmaps

**Frontier**
- Samsung VS-DRAM: 16 tiers, GAA cell transistors, horizontal capacitors, chip-level read/write; Cs grows ~linearly with horizontal capacitor length; peri-on-cell wafer bonding (VLSI 2026, T5.1; [cnyes](https://hao.cnyes.com/post/269690), [Mynavi](https://news.mynavi.jp/techplus/article/vlsi2026-5/)). Product ~2030 ([Yole 2024](https://www.yolegroup.com/industry-news/samsung-reveals-16-layer-3d-dram-plans-with-vct-dram-as-a-stepping-stone/)) [REPORTED].
- SK hynix: 5-layer at 56.1% yield, with 32–192 layers needed for products [CROSS-REF A1].
- imec: 120 Si/SiGe bilayers on 300 mm, still with edge dislocations [CROSS-REF A1].
- NEO 3D X-DRAM: single-cell PoC (see §2.4).
- Micron: 4F² is "not on the roadmap right now" [REPORTED via SK hynix coverage]. Micron's 3D DRAM status was not found [UNVERIFIED].

**TRL:** 4.

**Open problems:** single-crystal Si in every tier (epi defects); the lateral recess etch; horizontal capacitor area per tier; yield compounding (A1 §6).

**Untried:** a 3D Si stack *without* a capacitor (floating-body or gain cell in epi Si/SiGe), which shares the epi blocker. The more promising alternative is to replace epi Si with a deposited oxide channel (§2.1–2.2).

### 2.4 Capacitor-less silicon 1T revivals

**Frontier**
- Unisantis/imec Dynamic Flash Memory (DFM): a split-gate surrounding-gate transistor on 300 mm SOI at 65 nm. A wide 1/0 margin was validated experimentally for the first time, with **>10 s at 85 °C** and 10 ms BL disturb tolerance at 2.5 V (IMW 2025, via an [IEICE 2026 invited abstract](https://ken.ieice.org/ken/paper/20260409PcUx/eng/)) [REPORTED, single abstract].
- NEO 3D X-DRAM PoC: >1 s at 85 °C, BL/WL disturb >1 s, >10¹⁴ cycles, <10 ns. Single cell, 3D-NAND-style process at NYCU/TSRI; arrays and multi-layer chips are the next step ([StorageNewsletter 2026-05](https://www.storagenewsletter.com/2026/05/13/neo-semiconductor-demonstrates-3d-x-dram-proof-of-concept-secures-strategic-investment-to-advance-ai-memory/)) [CO-REPORTED].
- History (Z-RAM, T-RAM, Kilopass VLT) failed on margin, variability and holding current [CROSS-REF ram-venture A3].

**TRL:** 3–4.

**Physics note:** IGZO cannot host a floating-body cell. It is n-type with no usable hole accumulation, so capacitor-less 1T cells need Si, poly-Si or a p-type channel [ESTIMATE, device physics].

**Open problems:** SRH generation in the depleted body, which is worse in poly-Si; a margin that shrinks with body volume; disturb in dense arrays; temperature.

**Untried:** independent, array-level (≥64 kb) verification of the >1–10 s at 85 °C claims, and a retention-tail distribution. This is a cheap and decisive measurement.

### 2.5 Ferroelectric DRAM: NVDRAM, 3D FeRAM, 2T-nC

**Frontier**
- Micron NVDRAM (IEDM 2023, paper 15.7): 32 Gb, dual-layer, 5.7 nm FE capacitor, near-DRAM performance, presented in a generative-AI focus session ([eeNews](https://www.eenewseurope.com/en/iedm-micron-to-present-dram-like-non-volatile-memory-for-ai/)). **10¹⁵ cycles** per press ([Blocks & Files](https://blocksandfiles.com/2024/01/05/ferroelectric-ram-update-and-micron/), [Hi-Tech Mail](https://hi-tech.mail.ru/news/105402-micron-predstavila-neubivaemuyu-vysokoskorostnuyu/)). "Up to 10 years" retention per one source ([ichip](https://ichip.ru/novosti/micron-razrabotala-energonezavisimyj-chip-pamyati-feram-na-32-gbit-855782)) [UNVERIFIED]. Not productised [CROSS-REF].
- **2T-nC** (IEDM 2025): Notre Dame, Penn State, IBM, Fraunhofer and NUS fabricated a **2T-64C** cell, aiming at "hundreds of layer stacking". An FN-discharge read removes read-sequence dependence but costs read endurance ([IBM listing](https://research.ibm.com/publications/towards-scalable-3d-integration-of-2t-nc-feram-with-hundreds-of-layer-stacking), [Fraunhofer record](https://publica.fraunhofer.de/handle/publica/514071)). Earlier: a vertical 2T-3C on Si CMOS (IEDM 2024) [REPORTED].
- Georgia Tech: two-tier 1T-1C for bit-cost-scalable 3D FeRAM ([Mynavi](https://news.mynavi.jp/techplus/article/iedm2025-4/)). CXMT: monolithic 3D FeRAM (IEDM 2025) ([china.com](https://m.tech.china.com/redian/2025/1008/102025_1744298.html), promotional) [REPORTED].
- 1 Mb HZO 1T1C: 10¹¹ cycles, 1 month at 85 °C (IEDM 2023) [CROSS-REF].
- FMC DRAM+: no public silicon, €100M raised [CROSS-REF] ([TrendForce 2025-04](https://www.trendforce.com/news/2025/04/16/news-novel-memory-drammay-emerge-as-germany-restarts-memory-chip-production/)).

**TRL:** 5–6 for 1T1C at Gb scale (Micron); 3 for 2T-nC.

**Physics (model §4)**
- A 40 nm pillar MFM capacitor 20–40 nm tall switches 2P_r·A ≈ **1.0–2.0 fC (6,300–12,600 e⁻)**, against ~17,800 e⁻ in a DRAM bit. That is enough when it is read into a gain-transistor gate rather than a long bitline [ESTIMATE].
- 5-year endurance needs: 3.4×10¹⁵ cycles for a row hammered at tRC; 1.6×10¹⁴ at one write per µs; 1.6×10¹¹ at one write per ms [ESTIMATE].
- **Every FE read is destructive**, so reads count too.

**Open problems:** wake-up, imprint and fatigue in HZO; read-sequence dependence in 2T-nC; disturb of unselected capacitors on a shared plate; the BEOL thermal budget for crystallising HZO (~400 °C class) [ESTIMATE].

**Untried:** 2T-nC with **oxide-channel** gain transistors as a fully BEOL, deposition-only stack, targeting DRAM-class endurance through low-field partial switching or non-destructive (capacitive) readout. See §5-2.

### 2.6 FeFET-based memory

**Frontier**
- Embedded NVM at 22/28 nm [CROSS-REF].
- Endurance is limited because the memory window closes through charge trapping ([TU Dresden](https://tud.qucosa.de/en/api/qucosa%3A76933/attachment/ATT-0/)). After 10⁴ cycles at ±5 V and 100 ns, N_it doubles and the window falls from 1.2 V to 0.45 V ([IIT Madras 2026](https://ee.iitm.ac.in/events/2026/01/Masud-Rana-phd-viva/)) [REPORTED].
- Samsung IGZO-channel / HZO FeFET for eNVM (IEDM 2025) ([PC Watch](https://pc.watch.impress.co.jp/docs/column/semicon/2061772.html)) [REPORTED].

**TRL:** 5 as eNVM; 2 as DRAM-class.

**Verdict:** not DRAM-class. The gap is ~10⁸–10¹¹× in endurance.

**Revival condition:** oxide-channel FeFETs with no SiO₂ interlayer showing ≥10¹² cycles at a ≥0.5 V window, plus an architecture that absorbs the rest.

### 2.7 MRAM aimed at DRAM-class (STT, SOT, VCMA)

**Frontier**
- **SOT** (imec):
  - >10¹⁵ cycles at <100 fJ, with a ~50 nm CD (IEDM 2023) ([D&R](https://www.design-reuse.com/news/55400/imec-sot-mram.html)).
  - 210 ps on 300 mm (2018).
  - **Field-free perpendicular SOT in a 4 kb array, <10 ns** (IEDM 2025) ([imec record](https://www.imec-publications.be/entities/publication/20690070-6c98-4f55-aaa2-0371175f056f)).
  - A 2 Kb array claims 10¹⁸ cycles, contested ([Nano Research 2026](https://www.sciopen.com/article/10.26599/NR.2026.94908447)) [REPORTED].
- **VCMA:**
  - 1.1 GHz, 20 fJ, >10¹⁰ cycles, TMR 246%, field-free (imec 2020) ([eeNews](https://www.eenewseurope.com/en/imec-claims-two-voltage-mram-breakthroughs)).
  - 6 fJ at 0.5 ns ([Spintec](https://spintec.fr/?p=6408)) [REPORTED].
  - No 2025 IEDM VCMA array was found [UNVERIFIED].
- **STT:** Samsung eMRAM 0.017 µm² at 8 nm [CROSS-REF].

**TRL:** SOT 4; VCMA 3; STT 9 (embedded).

**Physics (model §5)**
- Charging the MTJ costs C·V² ≈ 0.13 fJ at 1 V (50 nm, 1.2 nm MgO), or ~1–5 fJ with the line. The measured 6–20 fJ is consistent.
- Every VCMA write is cheaper than a single DRAM refresh event (~46 fJ/bit, A1) [ESTIMATE].

**Open problems**
- SOT is a 3-terminal cell, larger than STT.
- VCMA: precessional timing control (the pulse must equal half a precession period); write-error rate; MgO breakdown endurance (~10¹⁰); needs a selector for crosspoint.
- STT: 16× the DRAM cell area.

**Untried:** a **selector-based VCMA crosspoint**, transistor-light, stackable at 4F² per layer. No array exists. The bets are a VCMA coefficient high enough for ≤0.5 V writes (better endurance) and write-verify plus ECC to absorb the write-error rate. Listed as white space 6 (§4).

### 2.8 2D-material memory cells (MoS₂, WSe₂)

**Frontier**
- MoS₂ 2T0C: 20 ns write, >1,000 s, ~0.2 fJ/write ([ACS Nano 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11760144)).
- Hybrid-gate MoS₂ 2T0C on wafer-scale CVD MoS₂: >100 s, multi-bit, high linearity ([NSR 2025](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12857206/)).
- Si-MoS₂ eDRAM: 6,000 s, 5 ns.
- Fudan "ATOM2CHIP": an MoS₂ memory chip grown on Si circuitry at 94.34% yield (Nature 2025; array size unknown) ([Berliner Zeitung](https://www.berliner-zeitung.de/article/durchbruch-forscher-integrieren-2d-materialien-erfolgreich-auf-silizium-chips-10004097)).
- A 2D FPGA with ~4,000 MoS₂ FETs uses 2T0C configuration memory ([Compound Semi](https://compoundsemiconductor.net/article/122919/2D_MoS%E2%82%82_FPGA_integrates_4000_FETs)).
- MoS₂/hBN/WSe₂ semi-floating-gate quasi-non-volatile memory: 10 s refresh, ~15 ns write (2018) ([IEEE Spectrum](https://spectrum.ieee.org/quasinonvolatile-memory-looks-to-fill-gap-between-volatile-and-nonvolatile-memory)) [REPORTED].

**TRL:** 2–3.

**Verdict:** physics fine. **No unique advantage over oxide** at DRAM-class: similar retention (10³–6×10³ s vs oxide's 10³–3×10⁴ s) and similar write speed.

**Real differentiators, untried:**
- p-type WSe₂ for **complementary** gain cells. Oxides have no good p-type.
- A 2D read device stacked on an oxide write device, in BEOL, for higher read current. NUS has started.

**Revival to "frontline":** BEOL-temperature (≤400 °C) wafer-scale growth giving Mb arrays at >90% yield, or a function oxide cannot do.

### 2.9 Hybrid bonding and wafer-on-wafer DRAM

**Frontier**
- **Every** 2026 next-generation DRAM demo bonds a periphery wafer to the cell wafer:
  - Samsung VCT, with the periphery underneath [CROSS-REF].
  - Samsung VS-DRAM, peri-on-cell [REPORTED].
  - SK hynix 4F² VG, with die thinning "in wafer-bonded structures" [REPORTED].
- imec reports W2W hybrid bonding at **300 nm pitch**, i.e. 11.1 M bonds/mm² (ECTC 2025) ([imec](https://www.imec-publications.be/entities/publication/6228fcc8-685e-4e72-83ba-3cb478415500/full)).
- Patents describe a DRAM array on one wafer bonded to periphery or processor wafers ([US 11,430,766](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11430766)). Overlay tolerance is the known weakness ([US 11,094,653](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11094653)) [REPORTED].
- HBM hybrid bonding is slipping to HBM4E/HBM5 [CROSS-REF A1].

**TRL:** 5–6 for DRAM (9 for NAND/CIS-style bonding [UNVERIFIED-training]).

**Physics (model §7):** one bond per bitline segment needs:

| BL pitch | Cell pitch | Cells per segment | Bond pitch needed |
|---|---|---|---|
| 40 nm | 40 nm | 128 | ≤0.45 µm |
| 80 nm | 120 nm | 128–256 | ≤1.1–1.6 µm |

Litho-light oxide pitches therefore need only **~1–2 µm** bond pitch, which is mature territory. A vertical-bitline 3D stack needs one bond per vertical BL group, not one per tier [ESTIMATE].

**Untried:** a cell wafer deliberately made on a *different, cheaper, litho-light line* (for example an oxide-cell stack on a 3D-NAND-class or depreciated line) and bonded to a foundry logic periphery. Incumbents bond wafers made in their own DRAM fabs. See §5-3.

### 2.10 Processing-in-memory DRAM

**Frontier**
- Samsung **LPDDR5X-PIM** (Hot Chips 2026; FMS 2026 Best of Show) ([Tom's Hardware](https://www.tomshardware.com/pc-components/dram/hot-chips-2026-samsung-makes-lpddr5x-smart-with-logic-unit-in-memory-lpddr5x-pim-is-3-01x-faster-than-lpddr5x-in-ai-inference-with-8x-the-bandwidth)):
  - 16 GB, with 614 GB/s internal PIM bandwidth vs 76.8 GB/s external (8×).
  - Llama-3.1-8B runs 2.28× faster on wall clock, with 3.01× throughput.
  - Same 561-ball package; mass production end-2026 or early 2027 ([TrendForce](https://www.trendforce.com/news/?p=63155)).
- HBM-PIM (2021): 300 MHz FP16 per bank, >70% energy saving (vendor) ([eeNews](https://www.eenewseurope.com/news/samsung-HBM-PIM-ai-chip)). AMD saw up to 85% data-movement energy saved (ISSCC 2023) ([Samsung](https://news.samsungsemiconductor.com/global/hbm-pim-cutting-edge-memory-technology-to-accelerate-next-generation-ai/)).
- SK hynix GDDR6-AiM at 16 Gbps ([HotHardware](https://amp.hothardware.com/news/sk-hynix-ai-accelerating-pim-memory)) [REPORTED].

**TRL:** 7–8.

**Physics (model §8):** under Amdahl's law, 3.01× from an 8× bandwidth ratio implies p ≈ 0.76 of runtime is offloadable [ESTIMATE].

**Open problem:** DRAM-process logic is slow and area-expensive, and every read is destructive (activate and restore).

**Untried:** PIM *inside a non-destructive gain-cell array*. A gain cell's read current is an analog function of the stored voltage, so in-array multiply-accumulate needs no restore. In a 3D oxide stack bonded to logic this merges with A1 white space 3. Listed as white space 8 (§4).

### 2.11 Cryogenic DRAM

**Frontier**
- At 77 K, commercial DDR3 reaches a 4,096 s refresh interval (up from 8 s) once six weak rows are excluded ([JSTS 2022](https://jsts.org/jsts/ArticleDetail/RD_R/414471)).
- IGZO 2T0C: 8,000 s at 77 K ([Front. Phys. 2025](https://journal.hep.com.cn/fop/EN/1159713851849629948)).
- Gain-cell eDRAM at 77 K: retention +44%, power −27% ([BGU](https://cris.bgu.ac.il/en/publications/gain-cell-embedded-dram-under-cryogenic-operation-a-first-study/)).
- CryoRAM: 3.8× speed, or power down to 9.2% (simulation).
- Cutting refresh makes ordinary accesses behave like row-hammer ([CryoGuard](https://pure.skku.edu/en/publications/cryoguard-a-near-refresh-free-robust-dram-design-for-cryogenic-co/)).
- Rambus/Microsoft "cold DRAM" (2017) ([Rambus](https://www.rambus.com/blogs/the-case-for-cold-dram-in-the-data-center/)) [REPORTED].

**TRL:** 3–4.

**Physics (model §6):**
- Carnot COP at 77 K is 0.345. At 15–30% of Carnot, the plant needs **9.7–19.3 W at the wall per W removed**.
- A 12 W RDIMM that drops to 3.6–6 W cold still costs **38–64 W at the wall**. The refresh share it saves is only ~0.75 W.

**Verdict:** killed for data centres; see §6 for the revival condition.

### 2.12 Other families, for completeness (reused from ram-venture, not re-searched)

PCM/3D XPoint, ReRAM, CBRAM, NRAM, thyristor RAM and 3D NOR are covered in ram-venture phase 2 (A2, A3 cards) [CROSS-REF].
- None of them shows DRAM-class endurance at the cell. Their strength is non-volatility or density in a storage-class tier.
- No 2025–26 frontier result found in this pass changes that.
- 3D NOR (SunRise) still has no public array data [CROSS-REF].

---

## 3. Cross-cutting physics findings (from `research/models/A3_frontier_estimates.py`)

### 3.1 Retention is an interface problem

Let C_SN be the storage-node capacitance (assumed 1 fF) and ΔV the droop a cell can tolerate (200 mV for 1 bit; 62 mV for 3 bits). The leakage ceiling for a retention target t is I ≤ C_SN·ΔV / t.

| Target retention | Max total leakage, 1-bit | Max total leakage, 3-bit |
|---|---|---|
| 10³ s | 2.0×10⁻¹⁹ A | 6.2×10⁻²⁰ A |
| 10⁴ s | 2.0×10⁻²⁰ A | 6.2×10⁻²¹ A |
| 10⁵ s (~1.2 days) | 2.0×10⁻²¹ A | 6.2×10⁻²² A |
| 10⁶ s (~11.6 days) | 2.0×10⁻²² A | 6.2×10⁻²³ A |

- Measured cells (400–30,000 s) therefore already sit at **~7–200 zA total node leakage**. At that level, gate-stack, passivation and trap-emission currents compete with channel leakage.
- That passivation alone moved retention 100× (SJTU) is the evidence.
- **Implication:** a days-retention, practically refresh-free DRAM cell is an interface-chemistry target, testable on single cells in a university fab.

### 3.2 Oxide gain cells are fast enough for DRAM-class

Take the CXMT IGZO select device (60.9 µA/µm) at 50% drive, with W = 20–40 nm (0.6–1.2 µA). It develops a 100 mV signal on a 64-cell read bitline (C ≈ 11 fF) in **0.9–1.9 ns**. With 256 cells (31 fF) it takes 2.5–5 ns. Three-bit sensing, needing ~8× finer resolution, takes ~7.5–40 ns. All of these are inside DRAM's 10–100 ns window [ESTIMATE].

### 3.3 Multi-level × tiers density and bits per wafer-dollar

Basis: same array efficiency (0.508) for every design; each tier adds 12.5% of base wafer cost (the A2 convention); base wafer cost relative to 1β is 0.9 at F = 20 and 0.55 at F = 40 [ESTIMATE].

| Design | Bits/cell × tiers | Gb/mm² (die-level) | × 1β density | × 1β bits/$ |
|---|---|---|---|---|
| 1β 6F² 1T1C (reference) | 1 × 1 | 0.475 | 1.00 | 1.00 |
| Vertical 2T0C, 10F², F = 20 nm | 1 × 1 | 0.127 | 0.27 | 0.30 |
| Vertical 2T0C, 10F², F = 20 nm | 3 × 4 | 1.52 | 3.21 | 2.59 |
| Vertical 2T0C, 10F², F = 20 nm | 3 × 8 | 3.05 | 6.42 | 3.80 |
| Vertical 2T0C, 10F², F = 40 nm (no EUV, no multipatterning) | 3 × 8 | 0.76 | 1.60 | 1.56 |
| Vertical 2T0C, 10F², F = 40 nm | 3 × 16 | 1.52 | 3.21 | 2.03 |
| Planar 2T0C, 24F², F = 40 nm | 3 × 16 | 0.64 | 1.34 | 0.85 |

Break-even bits/cell × tiers for density parity:

| Design | Break-even b×N |
|---|---|
| Vertical 2T0C, F = 20 nm | 3.7 |
| Vertical 2T0C, F = 40 nm | 15.0 |
| Planar 2T0C, F = 40 nm | 35.9 |

**Takeaways**
- Multi-level storage is worth as much as 3× more tiers.
- A vertical-channel cell is mandatory: planar 2T0C never wins.
- An EUV-free, single-exposure F = 40 nm process can beat 1β on bits per dollar at 3 bits × ≥8 tiers.

### 3.4 Ferroelectric 2T-nC

Basis: a two-transistor footprint of 2×8F² plus 50% routing at F = 20 nm [ESTIMATE].

| Capacitors per transistor pair (n) | Density vs 1β |
|---|---|
| 16 | 1.8× |
| 32 | 3.6× |
| 64 | 7.1× |
| 128 | 14× |

- Each extra layer is metal/HZO/metal, deposited at BEOL temperature.
- There is no single-crystal Si and no HAR capacitor etch per bit. A pillar etch through the whole stack is still needed.
- Switched charge is adequate (§2.5). Endurance is the bet.

---

## 4. White-space map

Each white space is a frontier gap that a small team could attack. "Novelty" says who, if anyone, is already near it.

| # | White space | Frontier evidence it builds on | What is untried | Axis won | Main physics risk | Small-team proof (18–24 mo) | Novelty |
|---|---|---|---|---|---|---|---|
| 1 | **MLC non-destructive oxide gain-cell DRAM** (2–3 b/cell, write-verify, ECC) | SJTU 4 b and 30,000 s; IMECAS 3 b and 400 s; imec 10¹² cycles at 95 °C | An array (≥4 kb) storing ≥2 b/cell at DRAM latency, with a level-drift budget under PBTI/H over hours | Density, cost/bit, refresh energy | Vt drift and variability eating level margin (62 mV at 3 b) | BEOL oxide arrays (Purdue/GT-class fab) plus an MPW sense/ADC chip; retention-vs-level maps at 85 °C | Single cells exist; no MLC DRAM array or architecture published. Extends A1 white space 2 |
| 2 | **Deposition-stacked FE 2T-nC tier** with oxide transistors | Micron 32 Gb at 10¹⁵ (press); ND 2T-64C; CXMT 3D FeRAM; GT two-tier | All-BEOL 2T-nC (oxide gain pair plus n MFM caps) aimed at DRAM-class endurance via low-field / partial switching or capacitive non-destructive read | Density (7× at n = 64), zero refresh, capex (deposition not litho) | HZO fatigue and wake-up; destructive read; plate disturb | 2T-8C/16C test structures on a university HZO ALD tool; endurance at DRAM-like duty | Academic 2T-nC exists. The oxide-channel, DRAM-endurance version is open |
| 3 | **Disaggregated bonded DRAM**: litho-light cell-stack wafer plus foundry periphery wafer | Samsung VCT/VS-DRAM and SK hynix VG all bond periphery; imec 300 nm W2W; model §7 says 1–2 µm suffices at litho-light pitches | A cell wafer from a *non-DRAM* line (oxide stack, F ≈ 40 nm, no EUV) bonded to a commodity logic periphery wafer | Capex, U.S. manufacturability, EUV independence | Bond yield and overlay at ~1 µm on warped multi-tier wafers; thermal budget of bonding vs oxide drift | Bond a university-fab oxide 2T0C array coupon to an MPW periphery die (die-to-wafer first) | Incumbents bond in-house wafers. The cross-line, litho-light version is unexplored. Pairs with A1 white space 1 and A2 white space 1 |
| 4 | **Days-retention oxide storage node** (10⁵–10⁶ s) via interface/passivation engineering | SJTU 100× from HfO₂ passivation; imec H+O anneal 30× | A systematic interface study aimed at ≤1 zA total node leakage; system use as power-gatable, refresh-free memory | Energy (refresh plus idle), enables #1 | Trap emission and PBTI set a floor | Single cells; Arrhenius retention at 85–125 °C | Partly explored |
| 5 | **Disturb, row-hammer and SER characterisation of oxide and capacitor-less cells** | No data found (A1 §9); CryoGuard shows hammer-like failures when refresh changes | Hammer and SER on IGZO 2T0C, 1T1C and DFM | Reliability; gates everyone | None (measurement) | Cheap test structures plus a pulse tester | Untouched in public literature [UNVERIFIED] |
| 6 | **Selector-based VCMA crosspoint MRAM** | 6–20 fJ at 0.5–1 ns, 10¹⁰ cycles (2020) | Any VCMA crosspoint array; a VCMA coefficient high enough for ≤0.5 V writes | Energy, non-volatility, density if stacked | WER, timing precision, MgO endurance | Device stacks at a university magnetics lab | Largely abandoned since 2020 |
| 7 | **Independent array test of capacitor-less Si (DFM / 3D X-DRAM)** | DFM >10 s at 85 °C; NEO >1 s at 85 °C, 10¹⁴ | ≥64 kb tail distributions | Cost (no capacitor) | Variability; SRH generation | SOI test chips | Claims exist, verification absent |
| 8 | **Gain-cell-native PIM in a 3D oxide stack** | LPDDR5X-PIM shows 8× internal bandwidth giving 3× on LLM decode | Analog MAC from non-destructive gain-cell read, with no restore | Energy/bit moved | Analog precision vs Vt drift | Small array plus MPW ADC | IGZO eDRAM CIM was simulated (ISCAS 2021) |

---

## 5. The three most promising white spaces

### 5-1. Multi-level, non-destructive oxide gain-cell DRAM

**Why it is a step change**
- Density and cost per bit both multiply, on top of whatever tier count is achieved.
- A 64 ms silicon cell cannot hold 8 levels.
- A cell with 10³–10⁴ s retention and a non-destructive gain read can, which is exactly what the 2025–26 frontier now shows at cell level (3–4 b/cell).
- Three bits × 8 tiers on an EUV-free F = 40 nm process gives **1.6× 1β density at ~1.56× bits per dollar**. The same at F = 20 nm gives 6.4× and 3.8× [ESTIMATE].

**What has to be true**
1. Vt drift ≤~20 mV over the refresh interval at 85 °C. That sets the refresh interval for multi-level storage; even 10 s is 150× DRAM's.
2. Vt σ small enough for 8 levels in a ~1 V window after write-verify.
3. Read in ≤50 ns with time-based or successive-approximation sensing (§3.2 suggests 8–40 ns).
4. Endurance ≥10¹² with level stability; imec shows >10¹² at 1 bit.

**What would kill it:** an irreducible PBTI/H Vt drift of ≥60 mV within seconds at 85 °C.
- *Revival condition:* fall back to 2 b/cell, and to 85 °C-limited markets.

**First experiment:** a 1–4 kb planar IGZO or In₂O₃ 2T0C array (university BEOL), read by an MPW sense chip. Map level-retention distributions vs temperature and cycling.

### 5-2. Deposition-stacked ferroelectric 2T-nC tier

**Why it is a step change**
- Bits are added by **deposition**: each extra bit is a metal/HZO/metal layer. That is the 3D-NAND economic model, applied to a fast, non-volatile, refresh-free cell.
- n = 64 gives ~7× 1β footprint density [ESTIMATE].
- Micron's 32 Gb NVDRAM shows hafnia can reach Gb scale at near-DRAM speed with a claimed 10¹⁵ cycles. Notre Dame's 2T-64C shows the stack builds.

**What has to be true**
1. 10¹⁴–10¹⁵ cycles including reads. Routes: low-field partial switching, an antiferroelectric or imprint-engineered stack, or non-destructive capacitive readout.
2. Plate-line disturb of the other n−1 capacitors ≤10⁻⁶ per access.
3. Read-sequence independence without the FN-discharge endurance penalty seen at IEDM 2025.
4. An all-BEOL ≤400 °C flow, using oxide-channel gain transistors.

**What would kill it:** HZO fatigue staying ≤10¹² under DRAM-like duty.
- *Revival condition:* use it as a persistent tier behind an SRAM/eDRAM write cache, with 1 write per ms per cell, which needs 1.6×10¹¹ cycles.

**First experiment:** 2T-8C and 2T-16C test structures with oxide transistors. Measure endurance and disturb at 10–100 ns pulses.

### 5-3. Disaggregated bonded DRAM: a litho-light cell-stack wafer on a foundry periphery wafer

**Why it is a step change**
- Incumbents have already proven that periphery and cells can be made on separate wafers and bonded (Samsung VCT and VS-DRAM, SK hynix VG).
- The untried step is to make the **cell wafer on a different, cheaper line**: an oxide-channel stack at F ≈ 40 nm, with no EUV and no high-temperature silicon. The periphery wafer comes from any logic foundry.
- That attacks capital intensity, EUV dependence and U.S. manufacturability together, the A2 white-space-1 axes.
- Model §7: one bond per 128–256-cell segment at oxide pitches needs only ~1–2 µm bond pitch, well inside demonstrated hybrid bonding (300 nm at imec).

**What has to be true**
1. Bond yield ≥99.99% per segment at ~1 µm pitch on multi-tier, possibly warped wafers.
2. The bonding thermal cycle (~250–400 °C) does not shift oxide Vt beyond the level budget.
3. A vertical-bitline architecture, so bond count does not scale with tiers.
4. Sense amplifiers fit under each bitline group in the periphery wafer. A1 white space 1 gives the area math.

**What would kill it:** an overlay or yield floor that forces >2 µm pitch.
- *Revival condition:* larger segments (512 cells) with gain-cell local amplification in the cell wafer.

**First experiment:** die-to-wafer bond a university-fab 2T0C coupon to an MPW periphery die. Measure per-bond yield and pre/post-bond retention.

---

## 6. Kills and downgrades from this pass, each with a revival condition

| Idea | Verdict | Reason (physics or show-stopper) | Revival condition |
|---|---|---|---|
| Cryogenic (77 K) DRAM for data-centre main memory | **Kill (system energy)** | 9.7–19.3 W wall per W removed; a 12 W RDIMM costs 38–64 W at the wall; refresh saving ≤0.75 W | Cooling already paid for (quantum or superconducting compute), or cold DRAM power falls below ~1/10 of warm power |
| FeFET as DRAM-class memory | **Kill (endurance)** | Window collapses after ~10⁴–10⁶ cycles; need ~10¹⁵ | Interlayer-free oxide-channel FeFET at ≥10¹² cycles plus an architecture absorbing the rest |
| STT-MRAM as main-memory density | **Kill (area)** | 0.017 µm² vs 0.00107 µm² (16×) | Selector crosspoint at ≤6F² per layer, stacked |
| 2D materials as primary DRAM channel | **Downgrade** (not dead) | No retention or speed edge over oxide; BEOL growth and yield unproven at Mb scale | ≤400 °C wafer-scale growth giving Mb arrays at >90% yield, or p-type complementary gain cells |
| Floating-body Si 1T (ram-venture "marginal") | **Upgrade to alive, TRL 3–4** | DFM >10 s at 85 °C on 65 nm SOI; NEO >1 s, 10¹⁴ | Needs ≥64 kb array tails to stay alive |
| Ferroelectric 1T1C NVDRAM (ram-venture business kill) | **Alive on physics** | 32 Gb functional; business, not physics, shelved it | n/a (alive) |
| PIM DRAM as a "new DRAM" | **Reclassify** | An overlay, not a cell; shipping-class | Merge into gain-cell PIM (white space 8) |

---

## 7. What I could not verify

- Full-text numbers from IEDM 2025, VLSI 2026 and IMW 2025 papers: only press releases, previews and repository abstracts were seen.
  - No retention for Kioxia 3D OCTRAM.
  - No cell size, endurance or retention for Samsung VS-DRAM or SK hynix 4F² VG.
  - No CXMT 3D FeRAM metrics.
  - No 2T-64C layer, endurance or margin numbers.
- Micron NVDRAM retention (10 years appears in one Russian-language source) and the conditions behind its 10¹⁵ cycles.
- Samsung IGO (>550 °C), which comes from a blog.
- FMC DRAM+ silicon status in 2026: none found.
- Micron's 3D DRAM program status.
- Any 2025–26 VCMA array result, or a TSMC or Samsung SOT array.
- Row-hammer or SER data on oxide cells: none found. I logged this as a gap, not as evidence of immunity.
- Fudan ATOM2CHIP array size and cell type.
- Cell footprints of the frontier 3D 2T0C cells. The model uses assumed 10F² (vertical) and 24F² (planar), logged in the assumptions file.

## Sources

Every source is logged in `research/sources/A3-frontier.jsonl` (74 entries; web facts via search snippets; `[CROSS-REF]` entries reused from ram-venture phase 2 cards). Inline links above point to the same URLs.
