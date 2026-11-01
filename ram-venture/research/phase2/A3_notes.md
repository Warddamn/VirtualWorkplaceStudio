# A3 research notes — capacitor-less Si DRAM, SRAM-at-scale, exotic materials

Agent A3 · 2026-11-01 · Outputs: `phase2/A3.json` (14 cards), `phase2/A3_device_params.json` (20 device rows), `sources/A3.jsonl` (39 entries), `assumptions/A3.md`.

---

## 0. Research constraint (read before trusting any company fact here)

- **No web search was possible.** The shared WebSearch budget (200 calls per turn, all agents) was exhausted before A3 started. Every A3 search was refused.
- **Web fetches were also blocked.** WebFetch to `en.wikipedia.org` failed DNS. A test fetch of `www.gsitechnology.com` returned proxy 403. The proxy status shows 403s for trendforce.com, investors.micron.com and sec.gov. Per the tool guidance, A3 stopped trying further hosts.
- **What was reachable.** Only public GitHub repositories (anonymous git clone) and the PyPI JSON API. From these A3 opened:
  - OpenRAM (README, latest commit 2026-10-27, v1.2.50);
  - the SkyWater sky130 SRAM bitcell library (LEF);
  - the OpenRAM sky130 macro set (LEFs);
  - the ChipFoundry Caravel template (README, 2026-04-23);
  - the basicmi/AI-Chip list (2023 snapshot, with URLs and excerpts for Cerebras, Groq, d-Matrix, Graphcore, Untether and Areanna).
- **Consequences for every output:**
  - Facts from those primary repos are **[VERIFIED]**.
  - URLs seen inside them (papers, news) are "seen, not opened" **[REPORTED]**.
  - URLs reused from A1/A2 logs carry a **CROSS-REFERENCE** tag.
  - Everything else comes from training data that ends around mid-2026 and is tagged **[UNVERIFIED-training]**. That covers Z-RAM/T-RAM history, IBM/Intel eDRAM, SRAM cell sizes, and the status of GSI, Nantero, Groq, Cerebras, d-Matrix, RAAAM, Thinfilm and Efabless.
  - Where a card's only mechanism citation is from training data, its evidence list has an entry with `"url": ""` and a NOURL flag for the Phase-3 verify pass. A3 did not invent URLs.
- **Verify first in Phase 3 (highest-leverage unknowns):**
  - GSI Technology: alive, latest revenue, Gemini-II status (A3-08).
  - Nantero: alive, any 2024–26 licensee (A3-11).
  - RAAAM GCRAM: funding, foundry partners (A3-03).
  - ChipFoundry: marketplace terms, MPW price (A3-04).
  - SkyWater Fab 25 node offering and a 90nm FD-SOI public PDK (A3-07).
  - The Groq–NVIDIA deal terms (A3-10).

---

## 1. Headline numbers (computed; `A3_device_params.json`; scratch calc reproduced by the formula in its `conventions`)

**Reference points.**
- Incumbent DRAM **cost** ≈ $2.7/GB (A1 REF row: 0.436 Gb/mm², $5.5k wafer, 88% yield).
- DDR5 **price**: ≈ $14–25/GB contract, ≈ $27/GB spot (Aug–Sep 2026).
- Glut (A-05): ≈ $10–12/GB. Severe glut: ≈ $3/GB. All price figures from phase1/market.md.

| Row | Device | Gb/mm² | $/GB (silicon + test/pkg) | vs DRAM density |
|---|---|---|---|---|
| A3-01 | Floating-body 1T (8F², 45nm PD-SOI) | 0.031 | ~$24 | 14× worse |
| A3-02 | Thyristor TCCT (10F², 32nm SOI) | 0.049 | ~$18 | 9× worse |
| A3-02b | Kilopass VLT *claim* (4F², 20nm) | 0.31 | ~$2.8 | UNSUPPORTED claim |
| A3-03 | Si 2T gain cell, 28nm (embedded) | 0.010 | ~$47 area-equiv. (6T: ~$80) | 44× worse |
| A3-05 | IBM 14HP deep-trench eDRAM | 0.026 | ~$50 (~$20 at a $2.5k depreciated wafer) | 17× worse |
| A3-06 | 6T SRAM 65 / 40 / 28 / 16 / N5 / N2 | 0.0013 → 0.038 | ~$268 / 144 / 102 / 99 / 79 / 120 | 11–330× worse |
| A3-07 | 16Mb SRAM on 200mm 65nm (Fab 25) | 0.0013 | ~$1,200/GB, ~$2.4 COGS per part | n/a (priced per part) |
| A3-09 | 28nm memory-only wafer | 27 GB/wafer | ~$111 silicon, ~$1,000 packaged | — |
| A3-10 | Groq-v1-like SRAM die (230 MB/725 mm²) | 0.0025 | ~$375 chip-level | HBM3E ≈ $12/GB |
| A3-11 | Hypothetical NRAM 1T1R 28nm | 0.026 | ~$31 | 17× worse |
| A3-13 | Printed polymer memory label | — | ~$4×10⁷ | — |

**Primary-verified anchors.**
- SkyWater S130 6T bitcell is **1.200 × 1.580 µm = 1.896 µm²** (PDK LEF, `google/skywater-pdk-libs-sky130_fd_bd_sram`).
- The OpenRAM 2 KB dual-port sky130 macro is **683.1 × 416.54 µm = 0.2845 mm² → 57.6 kbit/mm²**. That is ~6× below the bitcell limit at 0.70 array efficiency, because small macros are dominated by periphery (`VLSIDA/sky130_sram_macros`).

### Three findings that matter downstream

1. **SRAM has a cost floor of ~$80–120/GB at every node from 28nm to N2.**
   - SRAM bitcell scaling stalled after ~N5: N3E/N2 cells barely shrink while wafer prices rise, so $/bit is flat-to-up.
   - Trailing nodes are *worse*, not better, per SRAM bit: 40nm ≈ $144/GB, 65nm ≈ $268/GB.
   - So "SRAM instead of DRAM" can never win on $/GB. Even against shortage-spot DDR5 ($27) it is 3–4× off, and in the glut it is 8–10× off.
   - SRAM wins only on latency and energy, which is why the evidence for SRAM-heavy inference (Groq, Cerebras, d-Matrix, Graphcore) is all T3+ compute companies, not memory companies.
2. **Depreciated fabs do not rescue capacitor-less or embedded DRAM.**
   - Every capacitor-less or eDRAM cell is 9–44× less dense than 1b DRAM.
   - Cutting the wafer cost from $7.5k to a $2.5k cash cost moves 14HP-class eDRAM from ~$50 to ~$20/GB. That is still above glut DDR5 ($10–12) and ~7× incumbent cost.
   - Wafer cost is a second-order term; **density is first-order**.
   - Only the never-demonstrated Kilopass VLT 4F² claim reaches DRAM-cost parity. That is exactly why it was tempting, and exactly why it was marketing.
3. **The surviving opportunities in this branch are about on-chip memory supply and supply security, not $/GB.**
   - A3-04 is an open-PDK SRAM macro service.
   - A3-03 is Si gain-cell IP that replaces SRAM area.
   - A3-07 is a U.S.-fabbed long-lifecycle SRAM second source.
   - All three are indifferent to the DRAM glut because they are priced per macro, per mm² or per part.

---

## 2. Post-mortems (all [UNVERIFIED-training] unless noted)

### Z-RAM (Innovative Silicon, Lausanne)
- **History.**
  - Floating-body 1T cell on SOI, spun out of EPFL (~2002).
  - Licensed to AMD in 2006 (SOI caches) and Hynix in 2007 (a "Gen-2" bipolar-mode cell for commodity DRAM).
  - Neither licensee shipped, and ISi closed in 2010. Its patent portfolio reportedly went to Micron, so Micron is the likely holder of any surviving Z-RAM claims; early filings expire 2022–2028.
- **Why it died.**
  - The stored charge is the majority-carrier excess in a tiny floating body, a few hundred electrons at 45nm.
  - Sense margin, retention and read/write disturb degrade with variability and scaling.
  - Writes use impact ionization or parasitic-BJT action at elevated drain voltage, which wears the device.
  - Going to ultra-thin FD-SOI (<10 nm Si) makes the body even smaller.
  - It also needed SOI wafers, a cost adder vs bulk DRAM.
- **Same story elsewhere.** Toshiba's FBC (ISSCC 2003–2008, 128Mb-class) took the same path.
- **2020s revivals.** These moved to 3D or oxide channels: NEO 3D X-DRAM (PoC Apr-2026, retention >1 s at 85 °C, fabbed at TSRI, CROSS-REF A1) and Unisantis DFM. NEO belongs to A1-05.

### T-RAM / thyristor RAM
- **History.**
  - T-RAM Semiconductor (Milpitas) commercialized the thin capacitively-coupled thyristor (TCCT), from Stanford NDR-cell work (Nemati & Plummer, ~1998).
  - Licensed to AMD (2006) and co-developed with GlobalFoundries for 32/22nm SOI (2009).
  - The company was defunct by about 2010–11.
- **Kilopass VLT (2016)** promised a 4F² cross-point vertical thyristor DRAM with no capacitor and no refresh at roughly 45% lower cost. Synopsys acquired Kilopass in early 2018 and VLT disappeared.
- **Why it died.**
  - The bistable latch needs ON-state holding current: a 1 Gb array at 1–100 pA/cell idles at ~1–110 mA (computed).
  - The bistable window and retention degrade sharply at 85–125 °C.
  - The voltage margins are hard to hold across billions of cells.
  - Three well-funded attempts failed. Early IP has expired, so IP is not the barrier; physics and integration are.

### 1T1C eDRAM (IBM, Intel)
- **IBM.**
  - Deep-trench eDRAM shipped in volume: POWER7 (45nm SOI, 32 MB L3), POWER8 (22nm), POWER9 and z15 (GF 14HP, cell 0.0174 µm² per IEDM 2014).
  - IBM then moved POWER10 and z16 to Samsung 7nm with SRAM only.
  - GF sold East Fishkill (ex-IBM Fab 10) to onsemi, completed end-2022.
- **Intel.** Crystalwell 128 MB eDRAM (22nm, MIM-cap COB, 0.029 µm² cell, ~77 mm² die, 2013) was used through ~2017–18, then dropped.
- **Why it died.**
  - Extra masks (deep trench or MIM) on a logic flow cost more than they save once SRAM is good enough.
  - The advanced logic nodes it would need (FinFET/GAA) make trench and capacitor integration very hard.
  - Chiplets and 3D-stacked SRAM (AMD V-Cache) offered a cheaper path to big caches.
- **Lesson for A3-05:** reviving it on a depreciated fab is a T3 process restart for a product that loses to DRAM on $/GB.

### MoSys 1T-SRAM (precedent for the IP-licensing lens, A3-03)
- DRAM-cell "SRAM-compatible" IP licensed to NEC, Renesas and others. It was used in Nintendo GameCube/Wii.
- Royalties were real but modest and declined. MoSys later pivoted and merged into Peraso (2021).
- Takeaway: embedded-memory IP royalties at trailing nodes support a small company, not a large one.

### Nantero NRAM (CNT)
- Woburn, MA; founded 2001.
- The CNT fabric switches resistance via van-der-Waals contacts and is spin-coated at room temperature.
- Licensed to Fujitsu Semiconductor and Mie Fujitsu in 2016 for a 55nm embedded/standalone product targeted ~2018–19. It is not known to have shipped; Fujitsu exited fabs and the Mie fab became UMC's USJC.
- Status in 2024–2026 is unknown to A3. No primary URL obtainable.
- Kill reason: 20+ years without a volume product. Even a working 1T1R is transistor-limited (~$31/GB hypothetical). The rad-hard niche is held by qualified Toggle MRAM and F-RAM.

### Thinfilm Electronics (printed ferroelectric-polymer memory)
- Oslo; P(VDF-TrFE) printed memory, Xerox PARC/Opticom lineage.
- Shipped 20-bit printed memory labels. Bought Kovio's NFC assets and San Jose fab (2014), then pivoted to solid-state microbatteries and renamed itself Ensurge Micropower (2021). Reported insolvency ~2024 [UNVERIFIED-training].
- Kill reason: ~$4×10⁷/GB, ms latency, 10³–10⁵ endurance, high-voltage programming.

### 2D-material memory (MoS₂/WSe₂)
- Lab results:
  - Fudan quasi-non-volatile 2D memory (Nature Nanotech 2018);
  - Fudan "PoX" ~400 ps 2D flash (Nature 2025);
  - Penn State and Fudan 2D logic circuits (Nature 2025);
  - many MoS₂ 2T0C gain-cell papers with long retention.
- No array-scale (>1 Mb) memory, and no wafer-scale BEOL-temperature growth with defect control.
- Labeled UNSUPPORTED at venture scale. IGZO (A1) delivers the low-leakage benefit at 300mm today.

---

## 3. SRAM-at-scale details

- **Cell sizes used** [UNVERIFIED-training except S130]: 130nm (SkyWater) 1.896 µm² [VERIFIED]; 65nm 0.525; 40nm 0.242; 28nm 0.127; 16nm 0.074; N5 0.021 µm². N2 macro density is 38.1 Mb/mm² (TSMC IEDM 2024).
- **Reticle limit at 28nm:** a single ~858 mm² die holds only ~4.7 Gb (≈590 MB) of SRAM. 1 Gb needs ~181 mm². Standalone SRAM above ~1 Gb/die is impractical at trailing nodes.
- **Standalone SRAM vendors** [UNVERIFIED-training]:
  - Infineon (ex-Cypress, historically made at Fab 25 Austin, now SkyWater under supply agreement — CROSS-REF);
  - Renesas;
  - ISSI (owned by China's Ingenic since 2020, which matters for U.S. defense second-sourcing);
  - GSI Technology (Sunnyvale; TSMC-fabbed high-speed SRAM plus the Gemini APU; ~$20M/yr revenue, loss-making, funded by equity raises; Gemini-II on 16nm);
  - Alliance Memory (Kirkland WA, legacy SRAM/DRAM brand);
  - rad-hard: Honeywell (Plymouth MN), BAE (Manassas VA), Frontgrade.
- **Wafer-scale and SRAM-heavy inference evidence:**
  - Cerebras WSE-2 on TSMC 7nm with "100% yield" via redundancy, and WSE-1 on 16nm (AnandTech headline and excerpt seen). WSE-3: 44 GB SRAM, N5, 46,225 mm² [UNVERIFIED-training], which averages 7.8 Mb/mm² including compute and implies ~$386/GB of wafer cost at $17k/wafer.
  - Groq first-gen LPU: Llama-2 70B at 240 tok/s/user (EE Times excerpt seen); ~230 MB SRAM on ~725 mm² GF 14nm [UNVERIFIED-training]; NVIDIA non-exclusive license plus executive hires Dec 2025, reported ~$20B [UNVERIFIED-training].
  - d-Matrix: digital in-memory (SRAM) compute plus chiplets (Forbes 2022); $110M raise with Microsoft (Reuters 2023).
  - Graphcore wafer-on-wafer IPU (EE Times); Untether AI $125M (VentureBeat 2021); Areanna compute-in-SRAM (EE Times).
- **Verdict.** SRAM-instead-of-DRAM is real for **latency-bound decode**, but it costs ~30× HBM per GB of capacity. A 70B 8-bit model needs ~300+ Groq-v1-class dies.

---

## 4. Three meanings of "cheaper" (rule 5), per card

| Card | (a) material | (b) process | (c) capital | Tag |
|---|---|---|---|---|
| A3-01 FBC | — | no capacitor, +1–2 masks | depreciated SOI | b+c |
| A3-02 Thyristor | — | no capacitor | expired IP | b |
| A3-03 Si gain cell | — | **zero extra masks** in logic | MPW access | b |
| A3-04 OpenRAM service | — | — | **open PDK, MPW, open-source IP instead of owned** | c |
| A3-05 DT eDRAM revival | — | — | **depreciated fab** | c |
| A3-06 Bulk SRAM | — | — | cheap trailing-node wafers | c |
| A3-07 SRAM second source | — | — | **depreciated 200mm fab (Fab 25)** | c |
| A3-08 GSI APU VAR | — | — | buys an existing part | none |
| A3-09 Wafer SRAM | — | — | cheap 28nm wafer | c |
| A3-10 SRAM inference | — | — | U.S. foundry access | c |
| A3-11 NRAM | **CNT** | **room-T spin-coat** | — | a+b |
| A3-12 2D | **MoS₂/WSe₂** | — | — | a |
| A3-13 Printed polymer | **P(VDF-TrFE)** | **printing** | — | a+b |
| A3-14 Cryo gain cell | — | zero-mask logic | — | b |

---

## 5. Card-by-card evidence summary

- **A3-01 Floating-body 1T-DRAM.**
  - URLs: NEO 3D X-DRAM PoC and Kurnal density (CROSS-REF).
  - Z-RAM/FBC primary citations need URLs (NOURL).
  - TRL 4. Kill: physics plus a 14× density gap.
- **A3-02 Thyristor RAM.**
  - URL: Kurnal density only. T-RAM/Kilopass history is NOURL.
  - TRL 4. Kill: holding current, temperature, three failed attempts.
- **A3-03 Si gain-cell IP.**
  - URLs: imec 2T0C concept; DATE-2026 hybrid IGZO/Si; SkyWater–Weebit S130 qualification (third-party memory IP precedent); GF CBRAM acquisition (foundries pay for memory IP); Georgia Tech gain-cell work (all CROSS-REF); OpenRAM (opened).
  - Intel 65nm 2T gain cell (ISSCC 2008) and RAAAM are NOURL.
  - TRL 6. **Promising #2.**
- **A3-04 OpenRAM macro service.**
  - All six URLs opened or seen in primary repos: OpenRAM, PyPI, sky130 bitcell LEF, sky130 macros, ChipFoundry README, OpenRAM IEDM 2020.
  - TRL 6. **Promising #1 (founder fit).**
- **A3-05 DT eDRAM revival.**
  - URLs: Kurnal and XenoSpectrum (CROSS-REF). IBM/Intel eDRAM is NOURL.
  - Kill: density beats depreciation.
- **A3-06 Bulk SRAM as DRAM.**
  - URLs: sky130 LEF (opened), Kurnal, XenoSpectrum.
  - Kill: computed $79–268/GB.
- **A3-07 U.S. SRAM second source.**
  - URLs: SkyWater/Infineon Fab 25 (three sources), Cypress MN sale, Frontgrade, Sandia (all CROSS-REF); sky130 LEF.
  - **Promising #3 (survives glut, U.S.-fab moat), but T2 and not founder-doable.**
- **A3-08 GSI APU VAR.**
  - URLs: d-Matrix and Areanna (category evidence, seen). GSI facts are NOURL.
  - Founder-fit wildcard, but vendor-survival risk.
- **A3-09 Wafer-scale memory.**
  - URLs: Cerebras WSE-2, Andromeda and CS-1 (seen).
  - Kill: edge-I/O bandwidth, ~$1,000/GB.
- **A3-10 SRAM inference chip.**
  - URLs: Groq (×2), d-Matrix (×2), Graphcore, Untether (seen).
  - Possible, but T3 and crowded; not for us.
- **A3-11 Nantero NRAM.**
  - URLs: Weebit/SkyWater BEOL-IP precedent and Frontgrade channel (CROSS-REF). Nantero itself is NOURL.
  - Kill.
- **A3-12 2D materials.**
  - URL: NY CREATES Albany (venue only). The literature is NOURL.
  - **UNSUPPORTED**, TRL 2. Kill.
- **A3-13 Printed organic memory.**
  - No URL obtainable. **UNSUPPORTED** for any RAM role. Kill recorded.
- **A3-14 Cryo gain-cell eDRAM.**
  - URLs: imec (concept), OpenRAM. Cryo literature is NOURL.
  - TRL 3. Physics favorable, market tiny.

### Business-model lenses applied (rule E)
- **Fabless → foundry:** A3-01/02/05/06/07/09/10/11. Only A3-07 is economic, and only per part.
- **IP licensing:** A3-03 (best fit), A3-14, A3-04 (support on open IP).
- **Module/appliance:** A3-06 (fails), A3-08 (VAR), A3-09 (fails).
- **Recert/brokerage:** not applicable in this branch. EOL SRAM continuation is Rochester Electronics' business (Newburyport MA); see "not carded".
- **SaaS:** A3-04, A3-08 software layer.
- **Data product:** the SRAM/eDRAM cost-floor table is a candidate input to A1-14 (MemTech Atlas); not carded separately.
- **Defense-first:** A3-07, A3-04, A3-11.
- **University/lab patent license:**
  - A3-03 (Bar-Ilan/EPFL/Georgia Tech gain cells);
  - A3-01/02 (expired Z-RAM/thyristor filings — free to practice, worthless anyway);
  - A3-12 (2D, premature).

---

## 6. Ideas considered but NOT carded (one line each)

- **IGZO/LTPS memory on glass panels.** Covered by A1-03. LTPS-Si on glass (Sharp memory-in-pixel SRAM) has ~100 µm pixel-scale cells, ~10⁵× worse than DRAM.
- **Optane/3D XPoint revival.** Covered by A2-10/A2-11; not duplicated.
- **Molecular/DNA storage.** Excluded as non-RAM: write and read latencies are minutes to hours, and synthesis cost is $/MB-class. It is archival storage, not memory.
- **Optical/photonic RAM** (photonic-crystal nanocavity bits, NTT-style). UNSUPPORTED: kilobit-scale lab demos at best, µm-scale cells, and continuous optical power to hold state. Killed without a card.
- **Superconducting memory** (SFQ RAM, JMRAM / IARPA C3 lineage). Kb–Mb-scale demos, far less dense than cryo-CMOS, and needs 4 K. Kept only as the losing alternative inside A3-14.
- **Magnetic racetrack / domain-wall memory** (IBM/Parkin, 2008). TRL ~3 after 15+ years; IBM did not commercialize. Kill.
- **Expired-patent capacitor-less IP aggregator.** IP isn't the barrier (see A3-01/02); the A2-08 card covers the patent-licensor pattern.
- **EOL SRAM die-bank and re-packaging (Rochester-style).** Branch C territory (recert/brokerage). Rochester Electronics dominates authorized EOL continuation.
- **3D-stacked SRAM cache chiplet on a U.S. fab** (AMD V-Cache style). T3, needs hybrid bonding; covered in spirit by A2-13 (SOT-MRAM LLC chiplet) and A3-10.
- **SRAM price/availability tracker.** Branch D; overlaps A2-15 and A1-14.
- **Glass-substrate (panel-level packaging) memory modules.** A packaging idea, not a cell. Belongs to branch C.

---

## 7. Final ranking within A3

1. **A3-04 OpenRAM macro service.**
   - Only T0, founder-doable, glut-proof card; recurring revenue (SaaS plus support).
   - Ceiling is small. It can grow by adding A3-03 gain-cell macros and more U.S. PDKs.
2. **A3-03 Si gain-cell eDRAM IP.**
   - Silicon-proven, zero extra masks, high-margin IP, glut-proof.
   - Needs a circuit cofounder; RAAAM competes.
3. **A3-07 U.S.-fabbed long-lifecycle SRAM.**
   - Survives the glut; U.S.-fab plus 20-year-availability moat at a willing foundry (Fab 25).
   - T2, a hardware team, and an incumbent at the same fab.

**Wildcard:** A3-08, the GSI APU appliance, is software-led but rests on vendor survival.

**Kills:** A3-01, 02, 05, 06, 09, 11, 12, 13. **Not for us:** A3-10, A3-14.
