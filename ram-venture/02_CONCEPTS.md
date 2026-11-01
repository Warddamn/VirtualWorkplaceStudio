# 02 — CONCEPTS

**98 concept cards** generated in Phase 2 by parallel ideation agents (one per branch A–E; branch A split three ways because it is the largest), then deduplicated. Merges are noted on each card. Status after Phase 3 kill pass: **98 alive, 0 killed**. Scores are in `03_SCORING.md`. The machine-readable copy is `concepts.csv`. Device $/GB comparisons are in `models/device_cost_compare.py`.

Legend: TRL = technology readiness level 1–9 · Tier T0 <$50k, T1 $50k–$2M, T2 $2M–$50M, T3 $50M–$1B, T4 >$1B · materials sense: (a) material system, (b) process, (c) capital (mission rule 5).

## Deduplication log

- Reviewed and kept SEPARATE (distinct business model, buyer or technology): C-94 (working id E.10) lab-patent STTR studio vs C-06 (working id A1.06) HZO FeRAM and C-07 (working id A1.07) AlScN (portfolio/option vehicle vs single-device company); C-61 (working id C.04) consignment LTB vault vs C-91 (working id E.07) title-taking die bank vs C-72 (working id C.15) buying co-op (service vs inventory owner vs agency); C-85 (working id E.01) DIMM health subscription vs C-62 (working id C.05) graded recovered RDIMM sales vs C-79 (working id D.08) TB-RAM rental (subscription vs product vs rental); C-93 (working id E.09) compliant-memory federal reseller vs C-64 (working id C.07) provenance verification (reseller margin vs verification software); C-96 (working id E.12) Optane IP-estate licensing vs C-25 (working id A2.10) Optane device revival; C-44 (working id B.01) recovered-DDR4 CXL expander vs C-56 (working id B.14) Manassas-DDR4 trusted CXL expander; C-80 (working id D.09) OEM cost alerts vs C-86 (working id E.02) licensed escalation index vs C-83 (working id D.13) newsletter; C-13 (working id A1.13) emerging-memory qual lab vs C-92 (working id E.08) AS6171 counterfeit lab vs C-18 (working id A2.03) MRAM radiation data; C-97 (working id E.13) CXL tiering practice vs C-75 (working id D.03) KV-cache integration vs C-45 (working id B.02) KV pool appliance; C-12 (working id A1.12) F-RAM NVSRAM-replacement modules vs C-16 (working id A2.01) MRAM PLP reference design; C-55 (working id B.13) CIM module integration vs C-24 (working id A2.09) RRAM CIM chip design.
- Evidence caveat carried into Phase 3: the session's shared WebSearch budget (200/turn) was exhausted during ideation; branches C, D, E and parts of A3/B ran with zero or few searches, citing other agents' logged URLs, GitHub/PyPI, and training knowledge tagged UNVERIFIED. The Phase 3 adversarial audit re-checks evidence under explicit search quotas.
- C-64 (working id C.07) + C-64 (working id D.11) → kept C-64 (working id C.07) (CleanBOM-5949: memory-provenance verification for federal IT sellers): Same product: SPD/JEP106 fleet scan + attestation + lab confirmation for NDAA FY2023 §5949 memory provenance. C-64 (working id C.07) kept (adds the partner-lab and attestation layer); C-64 (working id D.11)'s open-core scanner becomes its acquisition funnel.
- C-25 (working id A2.10) + C-25 (working id B.09) → kept C-25 (working id A2.10) (3D XPoint / PCM Crosspoint Revival for the CXL Memory Tier): Same idea: rebuild a 3D XPoint/PCM crosspoint storage-class memory as a CXL tier. Kept the device-branch card (fuller device physics + cost inputs).
- C-51 (working id B.08) + C-51 (working id A2.12) → kept C-51 (working id B.08) (Persistent CXL Log Card (post-Optane PMem for WAL/journals)): Same product category and buyer: post-Optane persistent write-ahead-log/journal card (MRAM or DRAM+NAND+supercap behind PCIe/CXL). C-51 (working id B.08) kept as the broader formulation; C-51 (working id A2.12)'s MRAM-only variant is one implementation option.
- C-73 (working id D.01) + C-73 (working id D.04) → kept C-73 (working id D.01) (Memory FinOps Audit for Cloud SaaS): C-73 (working id D.04) (Redis->Valkey/Dragonfly cache sizing) is a narrower instance of C-73 (working id D.01) (cloud memory FinOps audit for SaaS); same buyer, same motion. Merged.

## A. Device & materials (43 cards)

### C-01 — OS-eDRAM: IGZO/IWO 2T0C gain-cell memory IP on a U.S. 200mm foundry

*Sub-branch:* Oxide-semiconductor DRAM (embedded gain cell) · *Materials sense:* mixed:a+b+c

**What it is:** A fabless IP company co-develops a low-temperature (<400C) IGZO or W-doped In2O3 2T0C gain-cell BEOL module with SkyWater (S130 in Bloomington MN, or the ex-Infineon Fab 25 in Austin, 130-65nm, 200mm). It then licenses the memory macro and compiler to ASIC designers, giving them on-die memory with ~4-5x the bit density of 130nm SRAM and near-zero standby leakage, stacked over logic.

**Why it could work:** IGZO off-current ~3e-19 A/um gives >400-1,000 s retention (imec IEDM 2020/2021) vs SRAM's constant leakage, so an always-on edge chip can hold weights/activations at near-zero standby power. A planar 2T0C at ~30F2 is ~0.5 um2/bit at 130nm vs ~2.0-2.5 um2 for 6T SRAM [ESTIMATE], and because it sits in BEOL it uses no extra silicon area. Arbitrage: SkyWater bought Fab 25 (~$73M + working capital, ~400k wafer starts/yr) and is converting it to a foundry, so it needs differentiated process options. Embedded-memory IP royalties carry ~85% gross margin.

**Evidence:** TRL 4 · Rule 1: SUPPORTED
  - [imec shows capacitor-free DRAM (IEDM 2020)](https://www.eenewseurope.com/news/imec-shows-capacitor-free-dram) — conference, 2020-12. IGZO 2T0C cell, retention >400 s, extracted Ioff 3e-19 A/um, 45nm gate length, 300mm wafers
  - [Capacitor-less IGZO-based DRAM cell with excellent retention, endurance and gate length scaling (IEDM 2021)](https://techxplore.com/news/2021-12-capacitor-less-igzo-based-dram-cell-excellent.html) — conference, 2021-12. Fully 300mm BEOL-compatible 2T0C: >1e3 s retention, >1e11 endurance, Lg 14nm with >100 s; PBTI lifetime ~1 yr vs 5-yr target
  - [Double-gate W-doped amorphous indium oxide transistors for monolithic 3D capacitorless gain cell eDRAM](https://investigadores.uandes.cl/en/publications/double-gate-w-doped-amorphous-indium-oxide-transistors-for-monoli/) — conference, 2020. IWO 2T gain-cell eDRAM, retention 1 s at 25C and 300 ms at 85C
  - [Georgia Tech 3T IWO BEOL eDRAM (ISCAS 2024)](https://hg.gatech.edu/node/675050) — conference, 2024. Shimeng Yu lab: BEOL W-doped In2O3 3T eDRAM for near/in-memory compute; low leakage improves retention
  - [DATE 2026: hybrid IGZO-Si 2T gain cell](https://past.date-conference.com/proceedings-archive/2026/DATA/154.pdf) — conference, 2026. IGZO-2T eDRAM suffers low operating speed from low mobility; BEOL stacking raises density
  - [US12191135 Two transistor gain cell memory with IGZO](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12191135) — patent, 2025. Granted 2T IGZO gain-cell patent (assignee not verified) -> active patenting; freedom-to-operate risk
  - [SkyWater to acquire Infineon's Austin Fab (Fab 25)](https://www.businesswire.com/news/home/20250226773415/en/SkyWater-to-Acquire-Infineons-Austin-Fab-and-Establish-Strategic-Partnership-to-Expand-U.S.-Foundry-Capacity-for-Foundational-Chips) — company, 2025-02. U.S. 200mm 130-65nm fab converting to foundry; closed 2025-06-30, ~400k wafer starts/yr (LaPedus)
  - [Purdue: 3D chip platform, three layers of ALD indium-oxide transistors on 200mm](https://engineering.purdue.edu/ECE/News/2026/purdue-researchers-build-3d-chip-platform-for-faster-more-efficient-ai-computing) — industry, 2026-09. >100,000 oxide devices on 52 dies of a 200mm wafer incl. ferroelectric FETs; BEOL-compatible; U.S. university IP

**Capital tier:** T2 | **Time to first revenue:** 36-48 months: 12-18 mo module development with foundry, 12 mo test chip + reliability, then first NRE/license from an edge-AI or defense ASIC customer | **Gross margin estimate:** 80-90% (IP royalties/NRE); revenue small early

**US manufacturability:** SkyWater Bloomington MN (S130/S90) or SkyWater Fab 25 Austin TX (130-65nm), both 200mm; needs a new IGZO sputter or In2O3 ALD + O2 anneal module. Development could start at NY CREATES Albany (300mm) or Purdue (200mm oxide BEOL demonstrated Sep 2026).

**Who is already doing this:** imec (2T0C program since IEDM 2020), Kioxia, IMECAS, Macronix (3D 2T0C), Georgia Tech/Shimeng Yu (IWO eDRAM), Notre Dame/Datta (IWO 2T), Purdue/Ye & Li (ALD In2O3 3-layer 200mm), SEL (DOSRAM / OS-LSI; dominant oxide-semiconductor patent estate). Competing embedded memories already at U.S. foundries: Weebit ReRAM (SkyWater S130), MRAM at GlobalFoundries.

**Wins on which axis, for which buyer:** standby power per bit (W/Mb at idle) and on-die memory density vs SRAM at mature nodes — for Always-on edge-AI ASICs (keyword spotting, vision wake-up, sensor fusion) and DoD/onshore sensor ASICs on 130-65nm U.S. nodes that are SRAM-limited

**Survives a 2029 glut?:** yes — Priced against on-die SRAM/MRAM/ReRAM, not DDR5; a DDR5 price collapse does not change an ASIC's on-die memory choice.

**Fatal-flaw candidate:** No U.S. foundry offers an oxide-semiconductor module. Qualifying one costs ~$10-30M and 3+ years [ESTIMATE], and PBTI lifetime was only ~1 year vs a 5-10 year target (imec 2021). ASIC teams rarely design in a single-source, unqualified memory when SkyWater already offers qualified ReRAM. SEL's patent estate is a freedom-to-operate risk.

*Possible?* yes - cells demonstrated on 300mm, oxide BEOL demonstrated on a U.S. 200mm line (Purdue) · *Profitable?* marginal - royalties on low-volume 130nm ASICs are small; the real money needs a 28nm-or-better foundry partner · *Doable by this founder?* no - process-module development and reliability qualification are far beyond <$50k and a day job

*Business-model lenses:* IP licensing; fabless->foundry; university/lab patent license (Georgia Tech/Notre Dame IWO, Purdue In2O3); defense-first

### C-02 — Standalone IGZO 2T0C DRAM die on a depreciated U.S. 200mm line (commodity DRAM substitute)

*Sub-branch:* Oxide-semiconductor DRAM (standalone) · *Materials sense:* mixed:a+c

**What it is:** Build discrete DRAM-substitute chips (DDR4/LPDDR-class interface) from four stacked IGZO 2T0C tiers over CMOS periphery on a depreciated U.S. 200mm 130nm line (SkyWater Fab 25 Austin) and sell them into the 2026 shortage. A capacitor-less, BEOL-stackable cell on cheap wafers is the whole pitch.

**Why it could work:** No capacitor, low-temperature BEOL, and stackable tiers (IMECAS showed 4-layer 3D 2T0C with 400 s retention and 3 bits/cell at VLSI 2026), with depreciated 200mm wafers at ~$1-2.5K [ESTIMATE], while DDR5 sells for ~$27/GB. The scratch model kills it: ~0.0035 Gb/mm2 => ~7.6 GB per 200mm wafer => ~$336/GB including test and packaging, ~12x today's DDR5 price, ~31x the glut price and ~125x DDR5's estimated cost (~$2.7/GB). Even a hypothetical 300mm 28nm-class 4-tier version models at ~$11.8/GB, about the glut price and ~4x DRAM cost, and no U.S. foundry offers that line.

**Evidence:** TRL 3 · Rule 1: SUPPORTED
  - [Capacitor-less IGZO-based DRAM cell with excellent retention, endurance and gate length scaling (IEDM 2021)](https://techxplore.com/news/2021-12-capacitor-less-igzo-based-dram-cell-excellent.html) — conference, 2021-12. Fully 300mm BEOL-compatible 2T0C: >1e3 s retention, >1e11 endurance, Lg 14nm with >100 s; PBTI lifetime ~1 yr vs 5-yr target
  - [IMECAS 4-layer 3D 2T0C IGZO DRAM (VLSI 2026)](https://www.ithome.com/0/966/543.htm) — news, 2026-06. 4-layer 3D 2T0C, single stacking step, 400 s retention, 3 bits/cell
  - [DRAM value-per-area chart (Kurnal Insights)](https://www.kitguru.net/channel/generaltech/joao-silva/new-dram-value%E2%80%91per%E2%80%91area-chart-draws-attention-amid-rising-memory-prices/) — news, 2026-09. 1b DRAM bit density ~0.436 Gb/mm2 (baseline for density comparison)
  - [CXMT DDR5 die analysis](https://semiwiki.com/forum/threads/chinas-cxmts-ddr5-reveals-3-year-technology-gap.23270/latest) — news, 2025. 16Gb DDR5 die 66.99 mm2 => 0.239 Gb/mm2
  - [DATE 2026: hybrid IGZO-Si 2T gain cell](https://past.date-conference.com/proceedings-archive/2026/DATA/154.pdf) — conference, 2026. IGZO-2T eDRAM suffers low operating speed from low mobility; BEOL stacking raises density

**Capital tier:** T3 | **Time to first revenue:** 60+ months (process development, multi-tier yield learning, JEDEC-interface die design, qualification) | **Gross margin estimate:** negative at any plausible price

**US manufacturability:** SkyWater Fab 25 Austin (200mm, 130-65nm) technically could add IGZO tiers; 130nm litho is the binding constraint

**Who is already doing this:** Nobody commercially at mature nodes; imec, IMECAS, Kioxia, SK hynix, and Samsung pursue oxide DRAM at leading-edge pitches

**Wins on which axis, for which buyer:** none for commodity buyers (loses on $/GB, bandwidth, latency); refresh power only — for (would be) industrial and legacy DDR4 buyers in the shortage, who will not pay ~12x DDR5 prices

**Survives a 2029 glut?:** no — Already ~12x DDR5's current price; in a glut where DDR5 falls 60% toward ~$11/GB the gap widens to ~31x.

**Fatal-flaw candidate:** 130nm lithography gives ~120x lower bit density than 1b DRAM (0.0035 vs 0.436 Gb/mm2 with 4 tiers); stacking recovers only linear factors.

*Possible?* yes - physics works (2T0C cells and 4-tier stacks are demonstrated) · *Profitable?* no - $/GB 12x DDR5 price today, ~125x DDR5 cost · *Doable by this founder?* no

*Business-model lenses:* module maker; fabless->foundry (both fail)

### C-03 — IGZO memory printed on idle display-fab glass

*Sub-branch:* Oxide-semiconductor DRAM (display-fab / large-area) · *Materials sense:* mixed:b+c

**What it is:** Use a depreciated Gen 6-8.5 oxide-TFT display backplane line (the CAAC-IGZO process Sharp and SEL commercialized) to pattern 2T0C memory arrays on glass, then cut and bond them to silicon sense/IO chips as cheap bulk memory. Large-area tooling and a 4-6 mask process are the 'cheaper process/capital' bet.

**Why it could work:** Display oxide-TFT lines are heavily depreciated and running underutilized (Omdia 2025). IGZO TFT leakage is tiny (SEL CAAC-IGZO <=200 zA), and a Gen 8.5 sheet is ~5.5 m2. Scratch model: at a ~2 um design rule a 2T0C cell is ~120 um2 => ~4e-6 Gb/mm2 => only ~2.3 GB per sheet => ~$266/GB before bonding, with microsecond access.

**Evidence:** TRL 2 · Rule 1: SUPPORTED
  - [SEL: Embedded DRAM using CAAC-IGZO FET with 1.8V supply](https://dc.engconfintl.org/ulsic_tft_vii/34) — conference, 2019. DOSRAM with CAAC-IGZO: leakage <=200 zA, 7 orders below Si; 1.8V operation
  - [That giant LCD fab touted for Wisconsin ... never mind](https://www.sixteen-nine.net/?p=20827) — news, 2019. Foxconn's Wisconsin Gen 10.5 LCD fab was never built; no U.S. TFT panel fab
  - [State report: Foxconn's project can't possibly be a factory](https://upnorthnewswi.com/2020/10/22/state-report-foxconns-project-cant-possibly-be-a-factory) — news, 2020-10. Wisconsin DOA: Gen 6 building shows no sign of LCD manufacturing
  - [Pragmatic opens UK's first 300mm wafer fab](https://www.semiconductor-today.com/news_items/2024/mar/pragmatic-280324.shtml) — news, 2024-03. IGZO FlexIC fab is in Durham, UK -- the closest thing to a 'memory-adjacent IGZO fab' is not in the U.S.
  - [Display panel industry faces utilization decline amid tariff uncertainty (Omdia)](https://telecomlead.com/electronics/display-panel-industry-faces-utilization-decline-amid-tariff-uncertainty-120613) — news, 2025. Panel fab utilization falling from >80% in 2025 -> idle oxide-TFT capacity exists, but in Asia

**Capital tier:** T3 | **Time to first revenue:** never as RAM; 72+ months for any memory-on-glass product | **Gross margin estimate:** negative

**US manufacturability:** None: the U.S. has no active-matrix TFT panel fab (Foxconn's Wisconsin Gen 10.5/Gen 6 LCD fab was never built); all oxide-TFT capacity is in Asia. Pragmatic's IGZO FlexIC fab is in the UK.

**Who is already doing this:** Display makers (Sharp, LG Display, BOE, JDI) for backplanes; Pragmatic (UK) for flexible IGZO logic and RFID; nobody for RAM

**Wins on which axis, for which buyer:** none for RAM; large-area and flexible form factors only — for none for RAM (possible niche: flexible smart labels, which is Pragmatic's market)

**Survives a 2029 glut?:** no — Already ~10x DDR5's price with µs latency; a glut makes it irrelevant.

**Fatal-flaw candidate:** Micrometer design rules => ~100,000x lower density than DRAM, plus no U.S. line exists.

*Possible?* marginal - TFT memory on glass is feasible but useless as RAM · *Profitable?* no · *Doable by this founder?* no

*Business-model lenses:* module maker; display-fab partnership (none in U.S.)

### C-04 — OCTRAM-class 4F2 IGZO-on-capacitor low-refresh DRAM as a U.S. second source

*Sub-branch:* Oxide-semiconductor DRAM (4F2 1T1C) · *Materials sense:* a-material

**What it is:** License Kioxia and Nanya's OCTRAM (a vertical cylindrical InGaZnO access transistor built on top of a high-aspect-ratio DRAM capacitor, 4F2) and have it produced for U.S. low-power DRAM buyers. The product would be a low-refresh LPDDR-class part for defense and IoT.

**Why it could work:** Ioff <1 aA/cell and Ion >15 uA (2024), >30 uA in Kioxia's 8-layer stack (IEDM 2025); a 275 Mbit array works at 54/63nm pitches. Scratch model at demo pitches on a DRAM-class line: ~0.16 Gb/mm2, ~$8.4/GB (below DDR5's ~$27 price but ~3x DDR5's estimated ~$2.7/GB cost at today's demo pitch).

**Evidence:** TRL 4 · Rule 1: SUPPORTED
  - [Kioxia develops OCTRAM (with Nanya), IEDM 2024](https://www.businesswire.com/news/home/20241209099702/en/Kioxia-Develops-OCTRAM-Oxide-Semiconductor-Channel-Transistor-DRAM-Technology) — company, 2024-12. 4F2 DRAM: vertical InGaZnO transistor on high-aspect-ratio capacitor; Ion >15 uA/cell, Ioff <1 aA/cell
  - [Kioxia developing new DRAM, SCM and NAND tech](https://blocksandfiles.com/2024/10/22/kioxia-developing-new-dram-scm-and-nand-tech/) — news, 2024-10. 275 Mbit OCTRAM array, WL 54nm / BL 63nm pitch, operates in design voltage range
  - [Kioxia core technology for high-density low-power 3D DRAM (IEDM 2025)](https://www.kioxia.com/en-jp/about/news/2025/20251212-1.html) — company, 2025-12. 8-layer horizontally stacked InGaZnO transistors (SiN replaced by IGZO); Ion >30 uA, Ioff <1 aA
  - [Samsung reportedly produces 10a DRAM working die using 4F2 and VCT, targets 2028](https://www.trendforce.com/news/2026/04/24/news-samsung-reportedly-produces-sub-10nm-10a-dram-working-die-using-4f-square-and-vct-targets-2028-production/) — news, 2026-04. Samsung 4F2 VCT working die Mar 2026; channel reportedly shifted to IGZO; mass production transfer 2028

**Capital tier:** T4 | **Time to first revenue:** 84+ months and only inside a DRAM maker | **Gross margin estimate:** n/a for a startup

**US manufacturability:** Requires a DRAM capacitor process => only Micron (Boise ID, Manassas VA) in the U.S.; Nanya (Taiwan) is Kioxia's partner. Violates rule 3 for us.

**Who is already doing this:** Kioxia + Nanya (OCTRAM); Samsung (4F2 VCT with reportedly IGZO channel, 2028 target); SK hynix (4F2 vertical-gate DRAM at VLSI 2026)

**Wins on which axis, for which buyer:** refresh/standby power (W/GB) at DRAM density — for mobile/IoT and AI-server low-power DRAM buyers (via DRAM makers), not a startup's customers

**Survives a 2029 glut?:** partially — A low-power premium may survive for whoever owns the fab; a startup without a fab gets nothing.

**Fatal-flaw candidate:** Needs a DRAM fab and Kioxia/Nanya IP, which is not offered for license; it is a T4 incumbent technology race.

*Possible?* yes - for DRAM makers · *Profitable?* no - not for a startup · *Doable by this founder?* no

*Business-model lenses:* IP licensing (as licensee - not available); fabless->foundry (no DRAM foundry exists in U.S.)

### C-05 — License NEO Semiconductor 3D X-DRAM and build it in the U.S.

*Sub-branch:* 3D DRAM (vertically stacked, IGZO variants) · *Materials sense:* mixed:a+b

**What it is:** Take a license to NEO Semiconductor's (San Jose) 3D X-DRAM (1T1C, or 3T0C with IGZO channels), built with a modified 3D-NAND flow, and stand up or partner on a U.S. 3D-NAND-class line to make it. This is the '3D NAND economics for DRAM' bet.

**Why it could work:** NEO claims ~10x DRAM density (up to 512Gb), <10 ns, >1e14 endurance and >1 s retention at 85C (company-reported PoC, Apr 2026). At the claimed density the scratch model gives ~$1.2/GB, which would be transformative if real. The big IDMs are converging on 3D: Samsung 16-tier VS-DRAM (VLSI 2026), SK hynix 5-layer at 56.1% yield (2024, needs 32-192 layers), Kioxia 8-layer IGZO stack, IMECAS 4-layer 2T0C.

**Evidence:** TRL 3 · Rule 1: SUPPORTED
  - [NEO Semiconductor demonstrates 3D X-DRAM proof-of-concept](https://www.storagenewsletter.com/2026/05/13/neo-semiconductor-demonstrates-3d-x-dram-proof-of-concept-secures-strategic-investment-to-advance-ai-memory/) — company, 2026-04. Company-reported PoC: retention >1 s at 85C, endurance >1e14, <10 ns; test chips by NYCU, fabbed at TSRI Taiwan; next: arrays, multi-layer
  - [NEO adds IGZO to 3D DRAM designs](https://www.eenewseurope.com/en/neo-semiconductor-adds-igzo-to-3d-dram-designs/) — news, 2025-05. 1T1C and 3T0C IGZO variants: TCAD-simulated 10 ns and >450 s retention, not silicon; modified 3D NAND process
  - [SK hynix 5-layer 3D DRAM 56.1% yield (VLSI 2024)](https://trendforce.com/news/?p=10820) — news, 2024-06. 5-layer stacked 3D DRAM yield 56.1%; needs 32-192 layers for products; Samsung ~2030 target
  - [2026 VLSI Technical Tipsheet](https://www.vlsisymposium.org/wp-content/uploads/2026/04/2026-VLSI-Technical-Tipsheet-REVISED-FINAL-NO-IMAGES-4.24.26.docx) — conference, 2026-04. Samsung 16-tier vertically stacked DRAM with GAA cell transistors and horizontal capacitors
  - [Kioxia core technology for high-density low-power 3D DRAM (IEDM 2025)](https://www.kioxia.com/en-jp/about/news/2025/20251212-1.html) — company, 2025-12. 8-layer horizontally stacked InGaZnO transistors (SiN replaced by IGZO); Ion >30 uA, Ioff <1 aA

**Capital tier:** T4 | **Time to first revenue:** 96+ months; NEO's next steps are array-level and multi-layer test chips | **Gross margin estimate:** n/a for us; NEO's own model is licensing

**US manufacturability:** Needs a 3D-NAND-class fab; no volume 3D NAND fab operates in the U.S. [UNVERIFIED - from training knowledge]. NEO's PoC was fabbed at TSRI (Taiwan) with NYCU.

**Who is already doing this:** NEO Semiconductor (licensor), Samsung, SK hynix, Micron, Kioxia, imec, IMECAS

**Wins on which axis, for which buyer:** $/GB via density (if claims hold) — for DRAM makers (NEO's intended licensees), not end customers

**Survives a 2029 glut?:** partially — A true 10x-density cost leader survives any glut, but that leader would be Samsung, SK hynix or Micron, not us.

**Fatal-flaw candidate:** Single-cell, company-reported PoC with no peer-reviewed array data; production needs a $10B-class fab. NEO pitches to memory companies, so the licensee seat is not available to a startup.

*Possible?* marginal - a PoC exists but array/multilayer feasibility is unproven · *Profitable?* no - not for us · *Doable by this founder?* no

*Business-model lenses:* IP licensing (wrong side of the table); fabless->foundry (no foundry)

### C-06 — U.S.-made HZO FeRAM family (1-16 Mb, rad-hard option) via SkyWater + Sandia

*Sub-branch:* Ferroelectric (HfZrO 1T1C FeRAM) · *Materials sense:* mixed:a+c

**What it is:** A fabless company designs a family of hafnium-zirconium-oxide 1T1C FeRAM chips (SPI/QSPI and parallel, 1-16 Mb, plus rad-hard variants). The HZO capacitor module would be built on SkyWater's 130nm line (Bloomington MN or Fab 25 Austin), with rad-hard variants co-developed with or licensed from Sandia, which integrated HZO FeRAM into its trusted MESA fab at 200mm (May 2026). It sells an onshore second source to Infineon's PZT F-RAM.

**Why it could work:** HZO is ALD-deposited and CMOS-friendly (no PZT lead contamination; ~2-3 extra masks, by analogy to TI's 2-mask FRAM on 130nm) and radiation hard (heavy-ion data; Sandia program). Space/defense F-RAM is close to sole-source (Infineon QML-V 2Mb). Wafers: ~$1,400 per 200mm [ESTIMATE]. This is a supply-security play, not a $/GB play: the scratch model is ~$770/GB because these are Mb-class parts.

**Evidence:** TRL 5 · Rule 1: SUPPORTED
  - [A highly reliable 1.8 V 1 Mb Hf0.5Zr0.5O2-based 1T1C FeRAM array with 3-D capacitors (IEDM 2023)](https://fis.tu-dresden.de/portal/en/publications/a-highly-reliable-18-v-1-mb-hf05zr05o2based-1t1c-feram-array-with-3d-capacitors%28e6411421-d8d0-4f39-97d3-03a6d18e3513%29.html) — conference, 2023-12. 1 Mb HZO 1T1C FeRAM: 1e11 endurance, 1-month retention at 85C
  - [Sandia: Facing radiation challenges head on](https://www.sandia.gov/research/news/evolving-semiconductor-technology-for-national-security-applications/) — government, 2026-05. HfO2/HZO rad-hard FeRAM integrated into Sandia's trusted MESA fab; FeRAM at 200mm scale; binary and 32-state FTJs
  - [Heavy-ion irradiation of ferroelectric hafnia NVM](https://publica.fraunhofer.de/handle/publica/456991) — peer-reviewed, unknown. Ferroelectric hafnia NVM devices show excellent radiation hardness
  - [Infineon 5962R1821601VXC rad-hard 2Mb serial F-RAM (QML-V)](https://infineon.com/cms/en/product/memories/radiation-hardened-high-reliability-memories/space-memories/5962r1821601vxc) — company, 2022-04. Incumbent PZT F-RAM: TID >150 krad(Si), SEL immune, 1e13 cycles, >100-yr retention at 85C
  - [Infineon EXCELON F-RAM family](https://infineon.com/cms/en/product/memories/f-ram-ferroelectric-ram/excelon-f-ram) — company, unknown. Shipping F-RAM 1-16 Mb, SPI/QSPI 108 MHz, 1e14 endurance, AEC-Q100
  - [FRAM set to save energy in write-intensive MCU applications](https://newelectronics.co.uk/content/features/fram-set-to-save-energy-in-write-intensive-mcu-applications) — news, 2010. TI embedded FRAM on 130nm adds 2 masks; cell 0.54-0.71 um2; made in-house
  - [Cypress PCN: Fab 25 Austin qualified as alternate wafer fab for 4/16/64Kb F-RAM](https://community.infineon.com/gfawx74859/attachments/gfawx74859/NonVolatileRAM/1143/1/002-18474_00_V.pdf) — company, unknown. F-RAM has history at Austin Fab 25 (now SkyWater); 130nm F-RAM transferred to TI Dallas 300mm

**Capital tier:** T2 | **Time to first revenue:** 36-60 months: Sandia CRADA/license + SkyWater module (18-24 mo), product design and samples (12 mo), first industrial sales; QML-V qualification adds 1-2 years | **Gross margin estimate:** 50-65% (high-rel ASPs); low volume

**US manufacturability:** SkyWater Bloomington MN (S130; DMEA-accredited trusted foundry [UNVERIFIED]) or SkyWater Fab 25 Austin (qualified by Cypress as an alternate fab for small PZT F-RAM parts, so the line has F-RAM history); Sandia MESA (Albuquerque) for rad-hard pilot.

**Who is already doing this:** Infineon (PZT F-RAM incl. rad-hard; 130nm F-RAM transferred to TI Dallas; Fab 25 history), RAMXEED (ex-Fujitsu, Japan), TI (embedded FRAM MCUs), Sandia (HZO R&D), FMC (HfO2, Germany), Sony/Fraunhofer/NaMLab (HZO 1T1C research)

**Wins on which axis, for which buyer:** supply security (U.S.-made, trusted) + non-volatile fast writes + radiation hardness — for Space/defense primes (satellite bus controllers, munitions/flight data recorders) and industrial/automotive event-data recorders wanting an onshore second source

**Survives a 2029 glut?:** yes — Mb-class NVM priced on reliability and supply security; unrelated to DDR5 $/GB.

**Fatal-flaw candidate:** HZO loses to incumbent PZT F-RAM on the specs F-RAM buyers pay for: 1e11 endurance and 1-month retention at 85C (IEDM 2023, 1Mb) vs 1e13-1e14 and >100 years. Infineon's F-RAM is already partly U.S.-fabbed (TI Dallas; Fab 25 history), so 'Made in USA' is not a moat against it. The niche is ~hundreds of $M/yr [ESTIMATE].

*Possible?* yes - 1 Mb HZO arrays exist; Sandia has 200mm FeRAM · *Profitable?* marginal - small, incumbent-dominated niche with a reliability gap to close · *Doable by this founder?* no - T2 chip company with qualification burden

*Business-model lenses:* fabless->foundry; university/lab patent license (Sandia CRADA/license); defense-first

### C-07 — AlScN ferro-diode memory for 500-600C electronics (Penn/AFRL license + STTR)

*Sub-branch:* Ferroelectric (AlScN ferroelectric diode, extreme environment) · *Materials sense:* a-material

**What it is:** License Penn's AlScN ferroelectric-diode NVM (Jariwala/Olsson group, co-developed with AFRL) and build kB-to-Mb memory dies and high-temperature packaged modules for SiC electronics. Target uses are hypersonics, turbine-engine health monitoring, downhole geothermal/oil tools and Venus/space probes, entered through AFRL/DARPA SBIR-STTR contracts.

**Why it could work:** Silicon DRAM and flash fail well below 300C [ESTIMATE]. Ni/Al0.68Sc0.32N/Pt diodes switched at 600C for >60 h at <15 V, which is compatible with SiC logic (Nature Electronics 2024), and scaled devices reach >100 Mbit/mm2 (arXiv 2025). The 2-terminal self-rectifying crossbar is a simple 3-4 mask BEOL. DoD keeps asking for this: AF254-D0806 (500C kB-scale NVM manufacturing scale-up) and DARPA DPA26BZ04-DV017 (-269 to +600C NVM, ~$1.2M Direct-to-Phase II, closed Aug 2026).

**Evidence:** TRL 4 · Rule 1: SUPPORTED
  - [New memory circuit can handle the heat (Nature Electronics 2024 coverage)](https://physicstoday.aip.org/news/new-memory-circuit-can-handle-the-heat) — news, 2024. Ni/Al0.68Sc0.32N(45nm)/Pt ferroelectric diodes on 4-inch Si switch at 600C for >60 h at <15 V (Penn + AFRL)
  - [Turning up the heat on data storage](https://www.engineering.upenn.edu/stories/turning-up-the-heat-on-data-storage/) — industry, 2024-05. Penn (Jariwala, Olsson) + AFRL; Nature Electronics Apr 29 2024
  - [Scalable and Stable Ferroelectric Non-Volatile Memory at > 500 C](https://arxiv.org/pdf/2309.04555) — peer-reviewed, 2023-09. AlScN NVM >500C; AFRL FAST program support
  - [Demonstration of highly scaled AlScN ferroelectric diode memory with storage density > 100 Mbit/mm2](https://arxiv.org/pdf/2504.13283) — peer-reviewed, 2025-04. Scaled AlScN ferro-diode memory >100 Mbit/mm2 (preprint)
  - [DARPA SBIR DPA26BZ04-DV017 Non-Volatile Memory for Extreme Environments](https://www.darpa.mil/research/programs/non-volatile-memory-extreme-environments) — government, 2026-07. Direct-to-Phase II (~$1.2M per BWCO) for -269C to +600C rad-tolerant NVM (NOR flash target); closed 2026-08-19
  - [SBIR topic AF254-D0806 Manufacturing Scale-up of 500C Capable, Kilo-Byte Scale, NVM](https://www.sbir.gov/topics/12036) — government, 2025. USAF topic (closed) citing ferroelectric diode memory stable to 600C; recurring DoD demand signal

**Capital tier:** T1 | **Time to first revenue:** ~36 months to first paid prototype/eval-part sales to primes; STTR Phase I/II money ($0.25-2M) comes earlier but is funding, not revenue (A-04) | **Gross margin estimate:** 55-70% on low-volume, high-ASP qualified parts

**US manufacturability:** Prototype at Penn's Singh Center for Nanotechnology, Philadelphia [external-user access UNVERIFIED]; scale on a U.S. 200mm line with AlN/AlScN sputter capability (MEMS/RF foundries or SkyWater) [UNVERIFIED which has AlScN today]; high-temperature ceramic packaging from U.S. hybrid houses.

**Who is already doing this:** Penn (Jariwala, Olsson), AFRL (Moore), other SBIR performers on the AF/DARPA topics; SiC high-temperature IC efforts (NASA Glenn, others) [UNVERIFIED]

**Wins on which axis, for which buyer:** operating temperature / survival in extreme environments (no incumbent RAM or flash works at 500C+) — for AFRL and hypersonic/engine programs; aero-engine OEMs (health monitoring); downhole tool makers (oilfield services, geothermal); planetary-probe teams

**Survives a 2029 glut?:** yes — Completely decoupled from commodity memory pricing.

**Fatal-flaw candidate:** Tiny, grant-shaped market that easily becomes an SBIR mill (the mission bars grant farming). It also needs a high-temperature periphery (SiC CMOS) that barely exists commercially, and Penn may already have licensed or spun out the IP [UNVERIFIED].

*Possible?* yes - devices work at 600C; arrays early · *Profitable?* marginal - high ASP but very low volume; depends on DoD program pull · *Doable by this founder?* marginal - best founder-entry among device cards via STTR, but not an 18-month revenue path

*Business-model lenses:* university/lab patent license; defense-first; fabless->foundry

### C-08 — Ferroelectric 'Optane-slot' persistent memory (NVDRAM-class HZO 1T1C NVDIMM/CXL)

*Sub-branch:* Ferroelectric (NVDRAM / storage-class memory) · *Materials sense:* a-material

**What it is:** Revive the Optane persistent-memory tier using Micron-style HfZrO 1T1C NVDRAM (32Gb dual-layer stacked, IEDM 2023) on DIMM or CXL modules for in-memory databases and AI checkpointing. This is the tempting 'DRAM is 2-3x, so a persistent tier must pay now' idea.

**Why it could work:** NVDRAM promised near-DRAM speed with non-volatility; at DRAM-like density the scratch model gives ~$4/GB if a DRAM maker built it. High DRAM prices revive interest in cheaper tiers.

**Evidence:** TRL 5 · Rule 1: SUPPORTED
  - [IEDM: Micron to present DRAM-like non-volatile memory for AI](https://www.eenewseurope.com/en/iedm-micron-to-present-dram-like-non-volatile-memory-for-ai/) — news, 2023-11. Micron 32Gb dual-layer stacked ferroelectric 1T1C NVDRAM, 5.7nm FE capacitor (IEDM 2023 paper 15.7)
  - [Micron NVDRAM might never become a product](https://blocksandfiles.com/2024/01/09/micron-nvdram-might-never-become-a-product/) — news, 2024-01. NVDRAM seen as a proving ground; no product
  - [Ferroelectric RAM looking rusty and stuck](https://www.design-reuse.com/news/202501939-ferroelectric-ram-looking-rusty-and-stuck-/) — news, 2025-01. As of 2025 no Micron NVDRAM product commitment
  - [Intel to wind down Optane memory business](https://www.anandtech.com/show/17515) — news, 2022-07. Optane wound down; $559M impairment Q2 2022
  - [Intel pulls the plug on Optane](https://www.techtarget.com/it-infrastructure/news/252523339/Intel-pulls-the-plug-on-Optane) — news, 2022-07. Optane losses incl. $576M in 2020; needed volume to cut cost
  - [Memory chip company FMC keeps working on semiconductor plant near Magdeburg](https://heise.de/-11151026) — news, 2026. FMC has no ferroelectric memory chips on the market yet; pursuing a fab near Magdeburg

**Capital tier:** T4 | **Time to first revenue:** never for a startup; Micron shelved it | **Gross margin estimate:** n/a

**US manufacturability:** Only a DRAM fab (Micron Boise/Manassas) could make it; rule 3 violation

**Who is already doing this:** Micron (shelved NVDRAM), FMC (DRAM+, no chip as of 2026), SK hynix/Samsung research

**Wins on which axis, for which buyer:** non-volatility at near-DRAM latency (persistence) — for in-memory DB and AI-checkpoint operators (hyperscalers)

**Survives a 2029 glut?:** no — A persistent tier must undercut DRAM; at -60% DDR5 plus cheap NAND the value gap closes, which is exactly what killed Optane.

**Fatal-flaw candidate:** Needs a DRAM fab plus a CPU/OS ecosystem. Optane lost ~$576M in 2020 alone and took a $559M impairment, and the one company able to build NVDRAM (Micron) never productized it.

*Possible?* yes - Micron built a 32Gb die · *Profitable?* no - market rejected the tier at Optane's cost; startup has no fab · *Doable by this founder?* no

*Business-model lenses:* module/appliance (dead); IP licensing (none available)

### C-09 — U.S. design-in and module partner for FMC DRAM+ (HfO2 non-volatile DRAM)

*Sub-branch:* Ferroelectric (HfO2 FeCAP DRAM, channel/module) · *Materials sense:* c-capital

**What it is:** Become FMC's U.S. application channel: eval boards, reference designs and small-volume non-volatile memory modules (U.S.-assembled at an East Coast EMS) around FMC's DRAM+ (ferroelectric HfO2 replacing the DRAM capacitor). Customers would be U.S. industrial PLC, medical-device and automotive data-logging OEMs.

**Why it could work:** FMC raised EUR100M (Nov 2025) with two DRAM-maker partners and an Asian logic foundry and wants global presence. U.S. OEMs value instant-on NV working memory that removes supercaps and batteries. A small partner can earn design-in services plus module margin, with capital limited to boards and inventory.

**Evidence:** TRL 4 · Rule 1: SUPPORTED
  - [FMC raises EUR100M to set new standards for memory chips](https://www.hpcwire.com/off-the-wire/fmc-raises-e100m-to-set-new-standards-for-memory-chips/) — company, 2025-11. EUR100M (EUR77M equity + EUR23M public) for DRAM+ and 3D CACHE+; works with two DRAM makers and an Asian logic foundry
  - [FMC + Neumonda DRAM+ (TrendForce)](https://www.trendforce.com/news/?p=37749) — news, 2025-04. DRAM+ replaces DRAM capacitor with ferroelectric HfO2 (non-volatile), Gb-class target; Neumonda provides test platforms
  - [Memory chip company FMC keeps working on semiconductor plant near Magdeburg](https://heise.de/-11151026) — news, 2026. FMC has no ferroelectric memory chips on the market yet; pursuing a fab near Magdeburg

**Capital tier:** T1 | **Time to first revenue:** 30-54 months: entirely gated by FMC sampling DRAM+ (no chips as of 2026) | **Gross margin estimate:** 25-35% (modules + services)

**US manufacturability:** U.S.-assembled only (dies from FMC's Asian DRAM partner) => 'U.S.-assembled', not U.S.-made (A-09)

**Who is already doing this:** FMC (Dresden), Neumonda (Munich, test platforms); global distributors (Arrow/Avnet-type) would take this role at volume

**Wins on which axis, for which buyer:** non-volatility at DRAM-like speed (instant-on, no backup power) — for industrial automation (PLC/CNC), medical devices, automotive event recorders

**Survives a 2029 glut?:** partially — The NV premium persists, but DRAM+ priced against DRAM gets squeezed by a 60% DDR5 drop.

**Fatal-flaw candidate:** Zero control: FMC has no chip, its timeline is uncertain, and once it ships it will use established distributors. A one-person channel partner has no moat.

*Possible?* marginal - depends on FMC delivering silicon · *Profitable?* marginal - thin channel margins · *Doable by this founder?* marginal

*Business-model lenses:* module/appliance; distribution/brokerage

### C-10 — FeFET embedded NVM licensing on GlobalFoundries 22FDX for U.S. MCU/edge SoCs

*Sub-branch:* Ferroelectric (FeFET eNVM) · *Materials sense:* mixed:a+b

**What it is:** Act as licensing/design-services intermediary for HfO2 FeFET embedded NVM (FMC technology) on GlobalFoundries 22FDX, selling it to U.S. MCU and edge-AI SoC makers as an eFlash replacement needing only 1-3 extra masks.

**Why it could work:** FeFET puts the ferroelectric in the HKMG gate stack (sub-5nm films, low write energy), and FMC/GF integrated it on 28nm HKMG years ago. Embedded NVM below 28nm is scarce.

**Evidence:** TRL 5 · Rule 1: SUPPORTED
  - [Ferroelectric memory startup aims at GloFo's 22FDX](https://www.eenewseurope.com/en/ferroelectric-memory-startup-aims-at-glofos-22fdx/) — news, 2016. FMC FeFET integrated on GF 28nm HKMG; licensing model
  - [Ferroelectric memory startup aims to be the Arm of memories](https://www.eenewseurope.com/en/ferroelectric-memory-startup-aims-to-be-the-arm-of-memories/) — news, 2017. FMC plans licensing to foundries/IDMs plus validation/qualification services
  - [CEA-Leti and Fraunhofer IPMS validate wafer exchange for FE memory materials (FAMES)](https://www.ipms.fraunhofer.de/en/press-media/press/2026/FAMES-wafer-exchange.html) — industry, 2026. HfO2 FE stacks to be evaluated embedded in upcoming GF 22nm FDX memory -- not yet qualified

**Capital tier:** T3 | **Time to first revenue:** 60+ months; 22FDX FE memory is still 'upcoming' per FAMES 2026 | **Gross margin estimate:** n/a for us (FMC/GF capture it)

**US manufacturability:** 22FDX runs mainly at GF Dresden, Germany [UNVERIFIED for any U.S. 22FDX FeFET flow]; GF Malta NY would need the module transferred

**Who is already doing this:** FMC, GlobalFoundries, Fraunhofer IPMS, CEA-Leti (FAMES pilot line)

**Wins on which axis, for which buyer:** embedded NVM write energy and scalability vs eFlash (NVM, not RAM) — for MCU/edge SoC designers on 22FDX

**Survives a 2029 glut?:** yes — eNVM is unrelated to DDR5 pricing, which is also why it isn't a 'RAM' answer.

**Fatal-flaw candidate:** We would own nothing: FMC and GF own the IP and the line. It is NVM not RAM, and it is not yet qualified.

*Possible?* yes · *Profitable?* no - not for an intermediary · *Doable by this founder?* no

*Business-model lenses:* IP licensing (as intermediary - no value add); fabless->foundry

### C-11 — SunRise-style 3D NOR 'quasi-volatile' memory as a DRAM substitute

*Sub-branch:* 3D DRAM alternatives (3D NOR charge-trap) · *Materials sense:* b-process

**What it is:** Thin-film 3D NOR charge-trap arrays with minutes-to-days retention, proposed by SunRise Memory (Eli Harari, San Jose) as a cheaper-than-DRAM tier refreshed rarely. A licensee would build it on NAND-class tooling.

**Why it could work:** If 3D NOR offered DRAM-like latency at NAND-like cost per bit, it would sit under DRAM for AI/KV-cache capacity. SunRise has kept patenting into 2024-2026.

**Evidence:** TRL 3 · Rule 1: UNSUPPORTED
  - [SanDisk founder has his next memory chip startup](https://www.eenewseurope.com/en/sandisk-founder-has-his-next-memory-chip-startup) — news, 2018. SunRise Memory (Eli Harari) 3D NOR positioned as DRAM-alternative tier
  - [SunRise Memory profile](https://www.cbinsights.com/company/sunrise-memory) — industry, unknown. Founded 2016, San Jose; Seagate investor; no product news found 2025-26
  - [US12052867B2 3D NOR memory array with very fine pitch](https://patents.google.com/patent/US12052867) — patent, 2024. SunRise still patenting; no silicon density data public

**Capital tier:** T4 | **Time to first revenue:** unknown; no public silicon after ~8 years | **Gross margin estimate:** n/a

**US manufacturability:** Would need a NAND-class fab (none in U.S. [UNVERIFIED])

**Who is already doing this:** SunRise Memory (status unclear 2025-26), Macronix (3D NOR research)

**Wins on which axis, for which buyer:** $/GB below DRAM with refresh-tolerant retention (claimed) — for (claimed) AI/datacenter memory tier

**Survives a 2029 glut?:** no — A sub-DRAM tier is squeezed from both sides when DRAM and NAND both fall.

**Fatal-flaw candidate:** No public silicon or peer-reviewed array data found for the DRAM-substitute claim. Patents do not show it works at scale, so it is UNSUPPORTED under rule 1.

*Possible?* marginal - unproven publicly · *Profitable?* no · *Doable by this founder?* no

*Business-model lenses:* IP licensing (as licensee)

### C-12 — Battery-free NV-cache / NVSRAM-replacement modules from off-the-shelf F-RAM

*Sub-branch:* Ferroelectric (PZT F-RAM, module) · *Materials sense:* c-capital

**What it is:** Design and sell small U.S.-assembled modules and firmware drivers built on shipping Infineon EXCELON 4-16 Mb QSPI F-RAM (or RAMXEED FeRAM). They would be drop-in replacements for battery- or supercap-backed SRAM/NVSRAM write caches in industrial controllers, CNC and data loggers, including legacy-equipment repair.

**Why it could work:** Shipping F-RAM offers 1e14 writes, zero write delay and >100-year retention, with no battery to fail, maintain or ship as hazmat. Legacy machines with battery-backed SRAM cards need maintenance-free replacements [ESTIMATE of demand]. Capital is just PCB design, contract EMS assembly and inventory. Key negative finding: F-RAM at ~$1-4/Mbit [ESTIMATE] is ~$8,000-30,000/GB, ~300-1,000x DDR5, so F-RAM cannot take DRAM sockets during the shortage, only battery-backed-SRAM sockets.

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [Infineon EXCELON F-RAM family](https://infineon.com/cms/en/product/memories/f-ram-ferroelectric-ram/excelon-f-ram) — company, unknown. Shipping F-RAM 1-16 Mb, SPI/QSPI 108 MHz, 1e14 endurance, AEC-Q100
  - [Infineon 5962R1821601VXC rad-hard 2Mb serial F-RAM (QML-V)](https://infineon.com/cms/en/product/memories/radiation-hardened-high-reliability-memories/space-memories/5962r1821601vxc) — company, 2022-04. Incumbent PZT F-RAM: TID >150 krad(Si), SEL immune, 1e13 cycles, >100-yr retention at 85C
  - [FRAM set to save energy in write-intensive MCU applications](https://newelectronics.co.uk/content/features/fram-set-to-save-energy-in-write-intensive-mcu-applications) — news, 2010. TI embedded FRAM on 130nm adds 2 masks; cell 0.54-0.71 um2; made in-house

**Capital tier:** T0 | **Time to first revenue:** 6-12 months (first module SKUs sold online and to MRO buyers) | **Gross margin estimate:** 40-55%

**US manufacturability:** East Coast contract EMS assembly; F-RAM dies from Infineon (TI Dallas / Fab 25 history) or RAMXEED (Japan) via distribution

**Who is already doing this:** Infineon (also sells nvSRAM), Everspin (MRAM drop-ins), Analog Devices/Maxim legacy NVSRAM modules [UNVERIFIED current status], niche industrial-repair vendors

**Wins on which axis, for which buyer:** non-volatility without batteries; lifecycle (maintenance-free) — for industrial MRO for legacy CNC/PLC with battery-backed SRAM; data-logger and metering OEMs

**Survives a 2029 glut?:** yes — Sold against batteries and NVSRAM, not DDR5.

**Fatal-flaw candidate:** Small, fragmented market where each design-in is custom engineering, and chip vendors (Infineon nvSRAM, Everspin MRAM) offer chip-level drop-ins. It is not 'RAM's job' at scale.

*Possible?* yes - parts ship today · *Profitable?* marginal - a niche product line, not a venture · *Doable by this founder?* yes

*Business-model lenses:* module/appliance; e-commerce

### C-13 — U.S. independent emerging-memory test and qualification lab (HZO / IGZO / AlScN)

*Sub-branch:* Ferroelectric + oxide (test/qualification services) · *Materials sense:* c-capital

**What it is:** An East Coast lab near Albany NanoTech or Philadelphia offering wafer-level ferroelectric and oxide-TFT characterization: P-E loops, wake-up/fatigue, retention bakes, PBTI/NBTI lifetime, coordination of radiation tests, and JEDEC-style qualification flows. Customers would be memory startups, university spinouts, SBIR performers and foreign memory firms entering the U.S.; it is a U.S. analogue of Neumonda's role for FMC.

**Why it could work:** Reliability is the gating problem for every A1 device: imec IGZO PBTI ~1 yr vs a 5-yr target, HZO 1-month retention at 85C, NEO's claims company-reported only. FMC itself sold 'validation and qualification services' as part of its model and uses Neumonda's test platforms. Used parametric analyzers, probe stations and ferroelectric testers cost ~$0.3-1M [ESTIMATE].

**Evidence:** TRL 8 · Rule 1: SUPPORTED
  - [Ferroelectric memory startup aims to be the Arm of memories](https://www.eenewseurope.com/en/ferroelectric-memory-startup-aims-to-be-the-arm-of-memories/) — news, 2017. FMC plans licensing to foundries/IDMs plus validation/qualification services
  - [FMC + Neumonda DRAM+ (TrendForce)](https://www.trendforce.com/news/?p=37749) — news, 2025-04. DRAM+ replaces DRAM capacitor with ferroelectric HfO2 (non-volatile), Gb-class target; Neumonda provides test platforms
  - [Capacitor-less IGZO-based DRAM cell with excellent retention, endurance and gate length scaling (IEDM 2021)](https://techxplore.com/news/2021-12-capacitor-less-igzo-based-dram-cell-excellent.html) — conference, 2021-12. Fully 300mm BEOL-compatible 2T0C: >1e3 s retention, >1e11 endurance, Lg 14nm with >100 s; PBTI lifetime ~1 yr vs 5-yr target
  - [A highly reliable 1.8 V 1 Mb Hf0.5Zr0.5O2-based 1T1C FeRAM array with 3-D capacitors (IEDM 2023)](https://fis.tu-dresden.de/portal/en/publications/a-highly-reliable-18-v-1-mb-hf05zr05o2based-1t1c-feram-array-with-3d-capacitors%28e6411421-d8d0-4f39-97d3-03a6d18e3513%29.html) — conference, 2023-12. 1 Mb HZO 1T1C FeRAM: 1e11 endurance, 1-month retention at 85C
  - [NY CREATES and Fraunhofer IPMS JDA on memory devices at 300mm](https://nachrichten.idw-online.de/2025/05/16/ny-creates-and-fraunhofer-ipms-announce-joint-development-agreement-to-advance-memory-devices-at-300mm-wafer-scale) — industry, 2025-05. Albany 300mm HfO2 ferroelectric memory co-development; East Coast access point

**Capital tier:** T1 | **Time to first revenue:** 12-18 months (first paid characterization projects from university spinouts / SBIR teams) | **Gross margin estimate:** 45-60% (services)

**US manufacturability:** Lab only (no fab); located near NY CREATES Albany (300mm HfO2 memory JDA with Fraunhofer IPMS) or Penn (Philadelphia)

**Who is already doing this:** Neumonda (Germany), Fraunhofer IPMS (Germany), university shared facilities, Sandia (not commercial-turnaround) [ESTIMATE that no U.S. commercial specialist exists - UNVERIFIED]

**Wins on which axis, for which buyer:** time-to-reliability-data and independence (enabling service, not a RAM axis) — for device startups, SBIR/STTR performers, defense primes evaluating new NVM, VCs doing tech diligence

**Survives a 2029 glut?:** partially — Startup funding shrinks in a memory glut, but defense and university demand continues.

**Fatal-flaw candidate:** Small, lumpy demand: customers with money (Samsung, Micron, Infineon) test in-house. Device-physicist labor is the bottleneck and the founder is not one.

*Possible?* yes · *Profitable?* marginal - services margin, small market · *Doable by this founder?* marginal

*Business-model lenses:* services; defense-first; data product (test database)

### C-14 — MemTech Atlas: emerging-memory device-parameter and $/GB cost-model data product

*Sub-branch:* Cross-cutting (oxide/ferroelectric/3D DRAM data product) · *Materials sense:* none

**What it is:** A subscription web app that curates published device parameters (cell area, retention, endurance, layers, mask adders, demonstrated vs simulated) for IGZO/IWO, HZO, FeFET, AlScN, MRAM, ReRAM and 3D DRAM. It pairs them with an open, auditable $/GB cost model and a 'claims vs silicon' tracker, sold to memory investors, corporate strategy teams, defense program offices and procurement.

**Why it could work:** It plays to the founder's software skill. This branch's research shows the data is scattered across press releases, IEDM/VLSI papers and paywalled TechInsights/Yole reports. Claims diverge sharply (NEO: 450 s simulated vs >1 s measured), and simple per-area analyses go viral (Kurnal Insights, Sep 2026). A transparent, cheaper tool for non-Yole budgets gives recurring revenue at ~80%+ margin.

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [DRAM value-per-area chart (Kurnal Insights)](https://www.kitguru.net/channel/generaltech/joao-silva/new-dram-value%E2%80%91per%E2%80%91area-chart-draws-attention-amid-rising-memory-prices/) — news, 2026-09. 1b DRAM bit density ~0.436 Gb/mm2 (baseline for density comparison)
  - [NEO adds IGZO to 3D DRAM designs](https://www.eenewseurope.com/en/neo-semiconductor-adds-igzo-to-3d-dram-designs/) — news, 2025-05. 1T1C and 3T0C IGZO variants: TCAD-simulated 10 ns and >450 s retention, not silicon; modified 3D NAND process
  - [NEO Semiconductor demonstrates 3D X-DRAM proof-of-concept](https://www.storagenewsletter.com/2026/05/13/neo-semiconductor-demonstrates-3d-x-dram-proof-of-concept-secures-strategic-investment-to-advance-ai-memory/) — company, 2026-04. Company-reported PoC: retention >1 s at 85C, endurance >1e14, <10 ns; test chips by NYCU, fabbed at TSRI Taiwan; next: arrays, multi-layer
  - [Capacitor-less IGZO-based DRAM cell with excellent retention, endurance and gate length scaling (IEDM 2021)](https://techxplore.com/news/2021-12-capacitor-less-igzo-based-dram-cell-excellent.html) — conference, 2021-12. Fully 300mm BEOL-compatible 2T0C: >1e3 s retention, >1e11 endurance, Lg 14nm with >100 s; PBTI lifetime ~1 yr vs 5-yr target

**Capital tier:** T0 | **Time to first revenue:** 6-9 months (MVP from this engagement's device_params + cost model; first annual subscriptions) | **Gross margin estimate:** 80-90% (SaaS)

**US manufacturability:** Software; no fab

**Who is already doing this:** TechInsights, Yole/System Plus, Objective Analysis, Coughlin Associates, Kurnal Insights, Mobius Materials (market reports)

**Wins on which axis, for which buyer:** cost and transparency of technology intelligence (RAM-adjacent, not a RAM axis) — for memory-focused VCs/CVCs, DoD/DOE program managers, SBIR applicants, OEM component strategists

**Survives a 2029 glut?:** partially — Technology diligence continues in a glut, but customer budgets shrink.

**Fatal-flaw candidate:** Small TAM, and incumbents with teardown access (TechInsights) own the authoritative data. It risks becoming content or consulting, which the mission treats as a bridge only.

*Possible?* yes · *Profitable?* marginal - real but small recurring revenue · *Doable by this founder?* yes

*Business-model lenses:* SaaS; data product

### C-15 — Onshore In-Ga-Zn oxide sputter-target and ALD-precursor supply for IGZO-channel DRAM

*Sub-branch:* Oxide-semiconductor DRAM (materials supply chain) · *Materials sense:* a-material

**What it is:** Supply DRAM-grade IGZO/ITO/IWO sputter targets and indium/gallium/zinc ALD precursors to DRAM makers moving to oxide channels: Samsung 10a 4F2 VCT with a reportedly IGZO channel targeted for 2028, Kioxia OCTRAM, imec and IMECAS 3D 2T0C. U.S. research lines (Purdue ALD In2O3 on 200mm, NY CREATES) would be early customers, positioned as a non-Chinese indium chain.

**Why it could work:** If oxide channels enter mainstream DRAM, every such wafer needs oxide-semiconductor deposition, and the materials play wins whichever cell architecture wins. Micron's U.S. fabs (Boise, Manassas, NY) and CHIPS-funded supply-chain localization favor onshore materials.

**Evidence:** TRL 6 · Rule 1: SUPPORTED
  - [Samsung reportedly produces 10a DRAM working die using 4F2 and VCT, targets 2028](https://www.trendforce.com/news/2026/04/24/news-samsung-reportedly-produces-sub-10nm-10a-dram-working-die-using-4f-square-and-vct-targets-2028-production/) — news, 2026-04. Samsung 4F2 VCT working die Mar 2026; channel reportedly shifted to IGZO; mass production transfer 2028
  - [Kioxia develops OCTRAM (with Nanya), IEDM 2024](https://www.businesswire.com/news/home/20241209099702/en/Kioxia-Develops-OCTRAM-Oxide-Semiconductor-Channel-Transistor-DRAM-Technology) — company, 2024-12. 4F2 DRAM: vertical InGaZnO transistor on high-aspect-ratio capacitor; Ion >15 uA/cell, Ioff <1 aA/cell
  - [Kioxia core technology for high-density low-power 3D DRAM (IEDM 2025)](https://www.kioxia.com/en-jp/about/news/2025/20251212-1.html) — company, 2025-12. 8-layer horizontally stacked InGaZnO transistors (SiN replaced by IGZO); Ion >30 uA, Ioff <1 aA
  - [Purdue: 3D chip platform, three layers of ALD indium-oxide transistors on 200mm](https://engineering.purdue.edu/ECE/News/2026/purdue-researchers-build-3d-chip-platform-for-faster-more-efficient-ai-computing) — industry, 2026-09. >100,000 oxide devices on 52 dies of a 200mm wafer incl. ferroelectric FETs; BEOL-compatible; U.S. university IP

**Capital tier:** T2 | **Time to first revenue:** 24-48 months (research-line sales first; fab qualification 2-3 years) | **Gross margin estimate:** 35-50% (specialty materials)

**US manufacturability:** Specialty-chemical/target plant on the East Coast; incumbents include Japanese target makers and U.S. firms such as Materion and Indium Corporation (current oxide-target/precursor product lines UNVERIFIED)

**Who is already doing this:** Display-grade IGZO target suppliers (Japan/Korea/China) and ALD precursor majors; DRAM-grade oxide precursors are an emerging category

**Wins on which axis, for which buyer:** supply security of a critical material for next-generation DRAM — for Samsung / SK hynix / Micron fabs and U.S. research lines (Purdue, NY CREATES, Sandia)

**Survives a 2029 glut?:** partially — Volumes track DRAM capex (down in a glut) but follow the technology transition, not DDR5 price.

**Fatal-flaw candidate:** DRAM makers qualify materials over 2-3 years with incumbent Japanese/Korean suppliers, and a startup without chemistry pedigree won't get qualified. Samsung's IGZO choice is only 'reported' and could revert to silicon.

*Possible?* yes · *Profitable?* marginal - real market if IGZO channels win, but incumbents are strong · *Doable by this founder?* no

*Business-model lenses:* materials supplier; defense/supply-security (CHIPS supply-chain programs)

### C-16 — Supercap-Killer PLP Kit (MRAM write-cache reference design)

*Sub-branch:* STT-MRAM design-in: power-loss-protection write cache · *Materials sense:* mixed:a+c

**What it is:** A licensed reference design (schematic/layout, FPGA or RISC-V controller RTL, Linux/Zephyr journaling driver, validation suite) that replaces the DRAM + supercapacitor power-loss-protection block in SSD, computational-storage, RAID/HBA and industrial data-logger boards with Everspin PERSYST 1Gb ST-DDR4 or 64-256Mb xSPI STT-MRAM. Parts come from Everspin (GF 28nm CMOS + Chandler AZ MTJ BEOL; Microchip Gresham OR line from 2H-2027); revenue is design-package fee + per-unit royalty + design-in services.

**Why it could work:** IBM moved its 5th-gen FlashCore Module to Everspin MRAM instead of capacitors (Oct-2026) because supercaps/batteries wear out in a few years and take board space. The PLP block needs only 64-512 MB, so MRAM's ~30x $/bit penalty (~$100/Gb street vs ~$3/Gb DRAM) costs ~$50-400 per board but deletes the capacitor bank, hold-up circuitry and its field failures. DRAM write-cache cost doubled in 2026 while MRAM pricing did not move with the DRAM cycle, narrowing the delta. Everspin is adding U.S. capacity (Microchip 10-yr deal, up to 1,300 wafers/qtr).

**Evidence:** TRL 8 · Rule 1: SUPPORTED
  - [IBM using Everspin MRAM in 5th-gen FlashCore Modules](https://www.blocksandfiles.com/flash/2026/10/05/ibm-using-everspin-mram-in-5th-gen-flashcore-modules/5300966) — news, 2026-10. IBM FCM5 (QLC SSD) uses a few hundred MB of Everspin MRAM as write cache/journal instead of supercapacitors for power-loss protection; production product (via search snippet)
  - [Next-Generation IBM FlashCore Modules Feature Everspin's PERSYST 1Gb STT-MRAM](https://businesswire.com/news/home/20240430370312/en/Next-Generation-IBM-FlashCore-Modules-Feature-Everspins-PERSYST-1-Gigabit-STT-MRAM-Enhancing-Reliability) — company, 2024-04. IBM FCM4 design-in of EMD4E001G 1Gb STT-MRAM (via search snippet)
  - [IBM and Everspin announce 19TB NVMe SSD with MRAM write cache](https://www.anandtech.com/show/13174) — news, 2018-08. IBM chose MRAM over DRAM+supercaps because supercaps/batteries last only a few years (via search snippet)
  - [Phison brings Everspin 1Gb STT-MRAM to next-gen SSD controllers](https://www.3dtested.com/news/phison-ssd-controller-everspin-mram,40022.html) — news, 2018. SSD controller support for MRAM-based PLP without supercaps (via search snippet)
  - [Everspin 8-K: Foundry Services Agreement with Microchip](https://www.sec.gov/Archives/edgar/data/1438423/000162828026024696/mram-20260408xexx991.htm) — company, 2026-04. 10-yr deal: Microchip Fab 4 (Gresham OR) 8-inch MRAM/TMR/STT wafers, ramp to max 1,300 wafers/qtr, first products 2H-2027; Microchip barred from making TMR devices for Everspin competitors (via search snippet)
  - [EMD4E001G16G2-150CAS2R listing](https://www.lcsc.com/product-image/C20342497.html) — industry, 2026. 1Gb STT-MRAM reference price $102.60 @500 (~$821/GB) (via search snippet)

**Capital tier:** T1 | **Time to first revenue:** 12-18 months: first paid design-in (services) to a Tier-2 SSD/computational-storage or industrial logger OEM; royalties only after their product ships (24-36 months) | **Gross margin estimate:** 45-70% (package/royalty high, services ~40%)

**US manufacturability:** MRAM die: Everspin Chandler AZ (MTJ BEOL, co-located at NXP) on GF Singapore 28nm CMOS today; Microchip Fab 4 Gresham OR 200mm from 2H-2027 for lower densities. Board assembly at any U.S. EMS. Not fully U.S.-made at 1Gb density until a U.S. CMOS source exists.

**Who is already doing this:** Everspin application engineering (gives reference designs free), IBM (in-house FCM), Phison (controller support), Broadcom/LSI RAID (Everspin journal MRAM since 2012), Marvell/Microchip SSD controller reference boards

**Wins on which axis, for which buyer:** lifecycle length and non-volatility of the write cache (no supercap aging), board area, PLP reliability — NOT $/GB — for Tier-2 enterprise/industrial and rugged/defense SSD makers, computational-storage startups, RAID/HBA card makers, flight/data-recorder and PLC OEMs with 10-20-year field life

**Survives a 2029 glut?:** partially — The reliability/supercap-elimination case is independent of DRAM price, but a 60% DDR5/DDR4 drop makes the DRAM+supercap alternative ~$20-50 cheaper per board, so marginal designs revert to DRAM.

**Fatal-flaw candidate:** Everspin and the controller vendors already give this engineering away to win sockets, and the number of new PLP designs per year is dozens, not thousands — a kit business likely caps below ~$1M/yr; plus an ITC exclusion order on Everspin STT-MRAM (Avalanche, 337-TA-1487, ~mid-2027) could interrupt 1Gb supply.

*Possible?* yes — the mechanism ships today in IBM FCM5 and LSI RAID journals · *Profitable?* marginal — real but small niche; Everspin captures most of the value · *Doable by this founder?* marginal — T1 and needs an EE partner; no fab, no chip design

*Business-model lenses:* module/appliance (reference design), IP licensing (design package + royalty), design services, defense-first variant (rugged SSDs)

### C-17 — DDR3-EOL Socket Swap to ST-DDR4 MRAM

*Sub-branch:* STT-MRAM as small-density DRAM replacement (industrial long-lifecycle) · *Materials sense:* a-material

**What it is:** Redesign service and drop-in mezzanine that replace end-of-life 1-4Gb DDR3/DDR4 chips on long-lifecycle industrial, medical and rail controllers with Everspin 1Gb ST-DDR4 STT-MRAM (GF 28nm + Chandler BEOL), selling instant-on non-volatility as the bonus. Target boards that need <=256 MB of working memory.

**Why it could work:** DDR3/DDR4 are being exited by Samsung/SK hynix/Micron in 2026 and DDR4 contract rose >50% QoQ in Q3-2026, so long-lifecycle OEMs face forced respins anyway; a respin to MRAM removes battery-backed SRAM/supercaps and gives a part with a 10+-year roadmap from a U.S. vendor. COMPUTED REALITY: MRAM street ~$100/Gb vs DDR3 4Gb spot ~$3.19/Gb = ~32x per bit; manufacturing cost ~$91/GB (MRAM, 28nm) vs ~$2.5-4.5/GB (DRAM). Doubling DRAM prices does not close a 30x gap.

**Evidence:** TRL 7 · Rule 1: SUPPORTED
  - [DDR4 reportedly leads legacy memory rally; DDR3 in tight supply](https://www.trendforce.com/news/2026/01/19/news-ddr4-reportedly-leads-legacy-memory-rally-with-q1-prices-up-to-50-ddr3-in-tight-supply/) — industry, 2026-01. Makers exiting DDR4 in 2026; DDR3 supply tight (via search snippet)
  - [Memory shortages drive DDR4 prices over 50% in Q3 2026; DDR3 also impacted](https://wccftech.com/memory-shortages-drive-ddr4-prices-over-50-in-q3-2026-ddr3-also-impacted-by-higher-costs/) — news, 2026-07. DDR3 4Gb spot ~$3.19/Gb vs DDR5 16Gb ~$2.94/Gb early July 2026 (via search snippet)
  - [EMD4E001G16G2-150CAS2R listing](https://www.lcsc.com/product-image/C20342497.html) — industry, 2026. 1Gb STT-MRAM reference price $102.60 @500 (~$821/GB) (via search snippet)
  - [World's First 1 Gb 28 nm STT-MRAM Product - by Everspin](https://www.techinsights.com/blog/memory/worlds-first-1-gb-28-nm-stt-mram-product-everspin) — industry, 2019. 1Gb die 105.1 mm2, cell 0.0396 um2, 9.75 Mb/mm2 on GF 28nm (via search snippet)

**Capital tier:** T0 | **Time to first revenue:** 6-12 months for a paid redesign study; product revenue only on boards needing <=256 MB | **Gross margin estimate:** 15-35% (services; part resale is distributor-thin)

**US manufacturability:** Everspin Chandler AZ BEOL on GF Singapore CMOS; board work at U.S. EMS

**Who is already doing this:** Everspin FAEs; long-lifecycle memory specialists (e.g., legacy-DRAM die-bank suppliers) solve the same EOL problem more cheaply with last-time-buy stock or LPDDR4 respins

**Wins on which axis, for which buyer:** non-volatility + supply longevity (U.S. vendor roadmap) for boards needing <=256 MB — for industrial PLC, medical-device and rail-signalling OEMs with DDR3 EOL exposure

**Survives a 2029 glut?:** no — In a glut DDR3/DDR4 last-time-buy and broker stock gets cheap and plentiful; the only reason to swap (forced EOL respin at shortage prices) disappears and the 30x bit-cost gap widens to ~100x.

**Fatal-flaw candidate:** 30x $/bit gap, 1Gb max per MRAM die (a 1GB board needs 8 dies), and ST-DDR4 is not pin/protocol compatible with DDR3, so a respin to LPDDR4/DDR4 is cheaper for almost everyone.

*Possible?* yes — parts exist · *Profitable?* no — loses on $/GB by ~30x except in rare <=256 MB sockets · *Doable by this founder?* marginal — consulting-only form is T0 but needs an EE

*Business-model lenses:* design services, recert/brokerage (part resale), module (mezzanine)

### C-18 — NewSpace MRAM Radiation-Data & Upscreen Service

*Sub-branch:* Defense/space-first MRAM (data product + screened parts) · *Materials sense:* mixed:a+c

**What it is:** Buy lot-traceable Everspin Toggle MRAM (MR4A16B, Chandler AZ) and PERSYST HR xSPI STT-MRAM (EM064LX) and run heavy-ion, proton and TID campaigns at U.S. beam facilities (e.g., Texas A&M Cyclotron Institute, LBNL 88-Inch BASE [names from training, UNVERIFIED access terms]), then sell (a) a subscription database of lot-specific radiation and screening results and (b) upscreened, serialized parts to LEO smallsat builders. Software platform (lot genealogy, test data, SEE rate calculators) is the founder's build.

**Why it could work:** NewSpace demand is pulling non-volatile MRAM into orbit: Everspin's 64Mb HR xSPI reached full production on LEO demand and Astro Digital picked it for a GEO bus (Q2-2026). Toggle MRAM shows >1 Mrad(Si) TID (Frontgrade/Cobham). Smallsat builders cannot pay QML-V prices or wait 20-26-week lead times (EM064LX 20 wks, EM128LX 26 wks) and want lot-specific COTS+ data. A report sells for ~$5-25k [ESTIMATE]; screened parts carry 2-4x markup on ~$40-60 parts.

**Evidence:** TRL 8 · Rule 1: SUPPORTED
  - [Case study touts Everspin Toggle MRAM for space](https://www.frontgrade.com/news/new-case-study-touts-everspins-toggle-mram-highly-reliable-memory-technology-space) — company, 2020. Toggle MRAM >1 Mrad(Si) TID, QML-Q/Q+ products via Cobham/Frontgrade (via search snippet)
  - [Everspin Q2-2026 earnings call highlights](https://www.marketbeat.com/instant-alerts/everspin-tech-q2-earnings-call-highlights-2026-08-05/) — news, 2026-08. Q2-2026 rev $18.7M (+42%); Astro Digital picked PERSYST 64Mb STT-MRAM for GEO Raven bus; LEO demand drove 64Mb HR production (via search snippet)
  - [EM064LX Future Electronics listing](https://futureelectronics.com/p/semiconductors--memory--RAM--nvram--mram/em064lxoab320is1t-everspin-technologies-4175573) — industry, 2026. 64Mb xSPI STT-MRAM $39.38 @480, 20-week lead time (via search snippet)
  - [EM128LXQAB313IS2T DigiKey listing](https://punchouttest.digikey.hk/en/products/detail/everspin-technologies-inc/EM128LXQAB313IS2T/24375470) — industry, 2026. Everspin 128Mb xSPI MRAM manufacturer lead time 26 weeks (via search snippet)
  - [Everspin earns $40 million MRAM deal for defense memory services](https://electronics360.globalspec.com/article/23702/everspin-earns-40-million-mram-deal-for-defense-memory-services) — news, 2026-04. $40M/2.5-yr subcontract to provide Toggle MRAM process tech and foundry services for DoW Defense Industrial Base; onshore Toggle capability (via search snippet)

**Capital tier:** T1 | **Time to first revenue:** 9-15 months: first paid test campaign / report for a smallsat bus maker; parts revenue after 2-3 campaigns build credibility | **Gross margin estimate:** 45-65%

**US manufacturability:** Parts: Everspin Chandler AZ Toggle line (onshore Toggle program under $40M DoW subcontract), PERSYST on GF CMOS + Chandler BEOL; testing at U.S. beam lines; screening at a U.S. test house (East Coast lab feasible).

**Who is already doing this:** Frontgrade (ex-Cobham CAES, QML MRAM using Everspin IP), Avalanche Technology (space-grade STT-MRAM, UMC 22nm), Everspin's own HR line, NASA GSFC/NEPP (publishes free radiation reports), independent upscreen/test labs and COTS-space distributors

**Wins on which axis, for which buyer:** radiation tolerance + non-volatility + data/lot traceability (supply security for NewSpace) — for LEO/GEO smallsat bus and payload makers (Astro Digital-type buyers, constellation primes), university cubesat programs, defense small-launch payload integrators

**Survives a 2029 glut?:** yes — Space buyers price on radiation data and heritage, not on DRAM $/GB; a DDR5 glut does not change rad-hard NVM demand.

**Fatal-flaw candidate:** Credibility and competition from free data: NASA NEPP publishes radiation reports for free, Everspin/Frontgrade/Avalanche sell pre-screened space parts with heritage, and a non-engineer founder has no radiation-effects reputation buyers will trust.

*Possible?* yes — standard industry practice · *Profitable?* marginal — small, credibility-gated market · *Doable by this founder?* marginal — T1 with a rad-effects partner; data platform is the founder's lever

*Business-model lenses:* data product (subscription rad database), defense-first niche, recert/upscreen of parts, SaaS (SEE calculators)

### C-19 — New Fabless Discrete STT-MRAM Vendor

*Sub-branch:* Discrete STT-MRAM chips (fabless on foundry eMRAM) · *Materials sense:* c-capital

**What it is:** Start a fabless U.S. company selling 128Mb-4Gb discrete STT-MRAM (CoFeB/MgO pMTJ) built on a foundry MRAM module (Samsung 28FDS/14nm, UMC 22nm or TSMC 16nm), competing with Everspin, Netsol and Avalanche in SPI/xSPI and ST-DDR4 sockets.

**Why it could work:** Foundry eMRAM is now standard (Samsung 14/8nm cells 0.024/0.017 um2; GF AutoPro150; TSMC 16nm), so a fabless entrant needs no MTJ fab. COMPUTED: a 4Gb die at 14/16nm with a 0.024 um2 cell is ~229 mm2 and costs ~$72/GB — still ~3.6x the PEAK DDR5 contract price before margin — so the only markets are NOR/FRAM/nvSRAM replacement and PLP, which Everspin already serves.

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [IEDM 2024 Samsung eMRAM (PC Watch)](https://pc.watch.impress.co.jp/docs/column/semicon/1649812.html) — conference, 2024-12. Samsung eMRAM cell 0.024 um2 (14nm) and 0.017 um2 (8nm), IEDM 2024 paper 11-4 (via search snippet)
  - [Netsol launches standalone STT-MRAM on Samsung 28nm FDSOI](https://mram-info.com/netsol-launches-stand-alone-stt-mram-product-fabricated-samsung-foundrys-28nm-fdsoi-process) — news, 2023-08. Netsol 1-64Mb parallel/serial STT-MRAM via Samsung Foundry (via search snippet)
  - [Avalanche AS301G208 UMC 22nm 512Mb MRAM Process Analysis](https://www.techinsights.com/blog/avalanche-as301g208-umc-22-nm-512mb-mram-process-analysis) — industry, unknown. Avalanche 512Mb STT-MRAM manufactured at UMC 22nm (via search snippet)
  - [Everspin Q3-2026 results (8-K Ex.99.1)](https://www.sec.gov/Archives/edgar/data/0001438423/000162828026067890/mram-20260930xexx991.htm) — company, 2026-10. Q3-2026 revenue $20.6M, MRAM product $16.9M, GM 51.4%, $6.0M litigation cost, cash $43.0M (via search snippet)
  - [USITC institutes Section 337 investigation 337-TA-1487](https://www.usitc.gov/press_room/news_release/2026/er0227_68226.htm) — government, 2026-02. Avalanche seeks exclusion order against Everspin STT-MRAM imports (via search snippet)

**Capital tier:** T2 | **Time to first revenue:** 36-48 months (design, MPW, qualification, AEC/JEDEC reliability, design-in cycles) | **Gross margin estimate:** 40-50% at scale (Everspin runs ~51%)

**US manufacturability:** Poor: foundry MRAM modules are at Samsung (Korea/Austin for logic only), UMC (Taiwan/Singapore), TSMC (Taiwan), GF 22FDX (Dresden). No U.S. 300mm MRAM foundry offering; Everspin-Microchip Gresham line is exclusive.

**Who is already doing this:** Everspin (U.S., ~$80M/yr run-rate), Netsol (Korea, Samsung 28FDS), Avalanche (Fremont CA, UMC 22nm), Renesas/Infineon/Cypress-lineage parts

**Wins on which axis, for which buyer:** non-volatility + endurance vs NOR/EEPROM (not vs DRAM) — for industrial/automotive NOR/FRAM replacement sockets, FPGA configuration, storage PLP

**Survives a 2029 glut?:** partially — Not priced against DRAM, so the glut does not kill it, but it never wins DRAM sockets in either regime.

**Fatal-flaw candidate:** Crowded tiny market (the category leader books ~$17M/qtr of MRAM product) plus a live patent war (Avalanche v. Everspin ITC 337-TA-1487) — a new entrant buys litigation risk for a market already served.

*Possible?* yes — Netsol did it in ~5 years · *Profitable?* no — crowded, sub-scale, litigious · *Doable by this founder?* no — T2 chip company

*Business-model lenses:* fabless->foundry; IP licensing (unlikely); defense-first variant

### C-20 — MRAM Main-Memory DIMM / CXL Module

*Sub-branch:* STT-MRAM as DRAM replacement · *Materials sense:* a-material

**What it is:** A persistent DDR4/DDR5 RDIMM or CXL Type-3 module populated with STT-MRAM dies (Everspin 1Gb ST-DDR4 today, hypothetical 4Gb 16nm dies later) sold as non-volatile main memory for servers during the DRAM shortage.

**Why it could work:** Tempting because DRAM is 2-3x and MRAM is non-volatile with no refresh. COMPUTED KILL: Everspin 1Gb density 9.75 Mb/mm2 vs ~400 Mb/mm2 for 1b DRAM (~42x less silicon-efficient). A 32GB RDIMM needs 256 MRAM dies (~27,000 mm2) vs 16 DRAM dies (~640 mm2). Cost ~$91/GB (28nm) or ~$72/GB (16nm) vs DDR5 ~$20/GB peak and ~$8/GB glut; street MRAM ~$821/GB.

**Evidence:** TRL 4 · Rule 1: SUPPORTED
  - [World's First 1 Gb 28 nm STT-MRAM Product - by Everspin](https://www.techinsights.com/blog/memory/worlds-first-1-gb-28-nm-stt-mram-product-everspin) — industry, 2019. 1Gb die 105.1 mm2, cell 0.0396 um2, 9.75 Mb/mm2 on GF 28nm (via search snippet)
  - [EMD4E001G16G2-150CAS2R listing](https://www.lcsc.com/product-image/C20342497.html) — industry, 2026. 1Gb STT-MRAM reference price $102.60 @500 (~$821/GB) (via search snippet)
  - [DRAM spot price snapshot (citing TrendForce)](https://www.buysellram.com/?p=20058) — news, 2026-08. DDR5 16Gb spot avg $53.92 on 2026-08-31 (~$27/GB) (via search snippet)
  - [IEDM 2024 Samsung eMRAM (PC Watch)](https://pc.watch.impress.co.jp/docs/column/semicon/1649812.html) — conference, 2024-12. Samsung eMRAM cell 0.024 um2 (14nm) and 0.017 um2 (8nm), IEDM 2024 paper 11-4 (via search snippet)

**Capital tier:** T2 | **Time to first revenue:** Never at competitive price; 5+ years for a niche persistent module | **Gross margin estimate:** negative at DRAM-parity pricing (~-355% at $20/GB)

**US manufacturability:** Dies: Everspin Chandler AZ + GF Singapore; module assembly U.S. possible (SMART Modular-type assemblers)

**Who is already doing this:** Nobody at volume; Everspin demonstrated ST-MRAM DIMMs ~2013-2016 [UNVERIFIED: training] and moved to niche PLP

**Wins on which axis, for which buyer:** non-volatility only; loses on $/GB, density, bandwidth and power per GB — for none at scale (in-memory DB persistence is better served by DRAM + NVMe logging)

**Survives a 2029 glut?:** no — At $8/GB DRAM the gap becomes ~10x on cost and ~100x on street price.

**Fatal-flaw candidate:** ~40x density deficit and ~4x-plus cost above peak DRAM price; physics of 50 F2 1T1MTJ cells vs 6 F2 1T1C.

*Possible?* marginal — buildable but absurdly sized · *Profitable?* no — loses on every buyer axis except persistence · *Doable by this founder?* no

*Business-model lenses:* module/appliance

### C-21 — Second U.S. MTJ BEOL Line on a Depreciated 200mm Fab

*Sub-branch:* MRAM manufacturing capacity (cheaper capital) · *Materials sense:* c-capital

**What it is:** Install an MTJ back-end module (multi-target PVD such as Canon Anelva/Applied Endura-class, ion-beam etch, magnetic anneal) in an idle or depreciated U.S. 200mm fab and offer Toggle/STT MRAM foundry services as a second U.S. source to DoD and IoT customers.

**Why it could work:** Depreciated 200mm capacity is cheap capital and DoD wants onshore Toggle MRAM ($40M DoW subcontract to Everspin, Apr-2026). But Everspin already locked the obvious partner: Microchip Fab 4 Gresham OR, 10-year deal, up to 1,300 wafers/qtr, and Microchip is barred from making TMR devices for Everspin competitors. Minimal MTJ module capex ~$20-50M [ESTIMATE] for a market whose leader books ~$65-70M/yr of MRAM product.

**Evidence:** TRL 8 · Rule 1: SUPPORTED
  - [Everspin 8-K: Foundry Services Agreement with Microchip](https://www.sec.gov/Archives/edgar/data/1438423/000162828026024696/mram-20260408xexx991.htm) — company, 2026-04. 10-yr deal: Microchip Fab 4 (Gresham OR) 8-inch MRAM/TMR/STT wafers, ramp to max 1,300 wafers/qtr, first products 2H-2027; Microchip barred from making TMR devices for Everspin competitors (via search snippet)
  - [Everspin earns $40 million MRAM deal for defense memory services](https://electronics360.globalspec.com/article/23702/everspin-earns-40-million-mram-deal-for-defense-memory-services) — news, 2026-04. $40M/2.5-yr subcontract to provide Toggle MRAM process tech and foundry services for DoW Defense Industrial Base; onshore Toggle capability (via search snippet)
  - [Everspin Form 10-K FY2025](https://www.sec.gov/Archives/edgar/data/1438423/000162828026014733/mram-20251231.htm) — company, 2026-03. Everspin buys foundry CMOS wafers and adds MTJ BEOL in Chandler AZ; single foundry GLOBALFOUNDRIES Singapore for higher-density products (via search snippet)
  - [Everspin Q3-2026 results (8-K Ex.99.1)](https://www.sec.gov/Archives/edgar/data/0001438423/000162828026067890/mram-20260930xexx991.htm) — company, 2026-10. Q3-2026 revenue $20.6M, MRAM product $16.9M, GM 51.4%, $6.0M litigation cost, cash $43.0M (via search snippet)

**Capital tier:** T2 | **Time to first revenue:** 36-60 months (tool install, process transfer/licensing, qualification) | **Gross margin estimate:** 20-40% foundry services at low loading

**US manufacturability:** By design U.S. (e.g., an idle 200mm line in the Northeast or Texas) — but needs MTJ process IP that only Everspin/Avalanche/foundries hold

**Who is already doing this:** Everspin (Chandler AZ + Microchip Gresham OR), foundries with eMRAM (GF Dresden, TSMC, Samsung, UMC)

**Wins on which axis, for which buyer:** supply security / trusted U.S. source — for DoD primes and the Defense Industrial Base

**Survives a 2029 glut?:** partially — Defense demand is price-insensitive, but commercial loading collapses and a sub-scale line cannot absorb fixed cost.

**Fatal-flaw candidate:** No process IP and no demand gap: Everspin's onshore expansion with Microchip and DoW money already fills the U.S. trusted-MRAM need.

*Possible?* yes · *Profitable?* no — sub-scale vs Everspin+Microchip · *Doable by this founder?* no

*Business-model lenses:* foundry services; defense-first

### C-22 — TrustNVM: U.S.-Made ReRAM Secure-NVM Chiplet on SkyWater S130

*Sub-branch:* Embedded ReRAM (oxide 1T1R) via licensed IP at a U.S. trusted foundry · *Materials sense:* mixed:a+c

**What it is:** A fabless 1-4 Mb serial NVM / secure-boot key-store and FPGA-configuration chip using Weebit Nano's JEDEC-qualified 1T1R oxide ReRAM module in SkyWater's S130 130nm process (Bloomington MN), sold to DoD primes and rugged-board makers that need domestic, trusted, radiation-tolerant NVM to replace imported SPI NOR/EEPROM (e.g., Renesas serial EEPROM, last-time ship 2026-10-31).

**Why it could work:** The ReRAM module is already qualified (256Kb, 3 lots, 10-yr retention, 125C) and sits in the S130 PDK, so IP risk is low and capital is licensed, not owned. SkyWater is a U.S. foundry used for DoD work [trusted-foundry accreditation: UNVERIFIED in this session]. Oxide ReRAM is reported to be intrinsically radiation tolerant [UNVERIFIED: literature]. Chips price per part ($20-200 in defense), so the ~$3,300/GB bit cost is irrelevant. SBIR/STTR topics for trusted microelectronics can fund the design.

**Evidence:** TRL 7 · Rule 1: SUPPORTED
  - [Weebit Nano's ReRAM IP now fully qualified in SkyWater S130](https://www.weebit-nano.com/news/press-releases/weebit-nanos-reram-ip-now-fully-qualified-in-skywater-technologys-s130-process/) — company, 2023-06. 256Kb 1T1R ReRAM module JEDEC-qualified (3 lots), 10-yr retention at industrial temp, in SkyWater S130 PDK (via search snippet)
  - [Weebit ReRAM IP achieves high-temperature qualification in SkyWater S130](https://www.skywatertechnology.com/weebit-nano-reram-ip-achieves-high-temperature-qualification-in-skywater-s130-process/) — company, 2023-11. Qualified to 125C, ready for production tape-out at SkyWater (via search snippet)
  - [Weebit Nano secures a license agreement with Texas Instruments](https://www.weebit-nano.com/news/press-releases/weebit-nano-secures-a-license-agreement-with-texas-instruments/) — company, 2025-12. TI licenses Weebit embedded ReRAM (tech transfer, design enablement, qualification) (via search snippet)
  - [Renesas EOL plan: serial EEPROM products](https://www.renesas.cn/zh/document/gde/eol-plan-serial-eeprom-products) — company, 2025-11. Renesas serial EEPROM families EOL, last-time shipment 2026-10-31 (via search snippet)
  - [TSMC 2025 Annual Report ch.5](https://investor.tsmc.com/static/annualReports/2025/english/pdf/2025_tsmc_ar_e_ch5.pdf) — company, 2026. TSMC N12e RRAM consumer-qualified; 22RRAM passed 100K-cycle qualification in 2025 (via search snippet)

**Capital tier:** T1 | **Time to first revenue:** 24-36 months: SBIR Phase I/II funds design + MPW; first revenue from engineering samples/qualification lots to a prime | **Gross margin estimate:** 50-65% (defense pricing) after Weebit royalty

**US manufacturability:** SkyWater Technology, Bloomington MN, S130 (200mm, 130nm) with Weebit ReRAM in PDK; U.S. OSAT (e.g., Amkor Arizona when open, or small U.S. packaging houses)

**Who is already doing this:** Weebit (IP), SkyWater (foundry), Everspin Toggle MRAM (incumbent U.S. rad-tolerant NVM with DoW onshore program), Frontgrade, Infineon/Cypress rad-hard NOR/FRAM

**Wins on which axis, for which buyer:** supply security (U.S.-trusted fab) + radiation tolerance + EOL replacement — not $/GB — for DoD primes and subsystem makers needing trusted NVM for FPGA config, secure boot and key storage; rugged industrial/space board makers

**Survives a 2029 glut?:** yes — Defense trusted-NVM demand is not tied to DRAM pricing.

**Fatal-flaw candidate:** Everspin Toggle MRAM already fills the U.S.-made rad-tolerant NVM slot with heritage and a $40M DoW onshore program; a new ReRAM chip must beat that on cost or density with tiny volumes and a Weebit royalty.

*Possible?* yes — qualified IP in a U.S. PDK · *Profitable?* marginal — small defense volumes, incumbent MRAM · *Doable by this founder?* no — needs an IC design co-founder and SBIR money

*Business-model lenses:* fabless->foundry, IP licensing (in-licensed), defense-first, SBIR-funded

### C-23 — University / Expired-Patent CBRAM-ReRAM IP Licensor

*Sub-branch:* ReRAM/CBRAM IP licensing (university tech-transfer path) · *Materials sense:* c-capital

**What it is:** License (or design around expired) early CBRAM/PMC patents (Ag/Cu-GeS conductive-bridge lineage from ASU -> Axon -> Adesto) or oxide ReRAM patents from a university tech-transfer office, package them with a test-chip on an MPW, and license the eNVM module to second-tier foundries/IDMs.

**Why it could work:** CBRAM needs ~1 extra mask on logic (GF statement), and the oldest PMC patents date to the late 1990s so freedom-to-operate may be cheap. But the production-proven CBRAM now belongs to GlobalFoundries (bought from Renesas, 2023); TSMC has in-house RRAM at 28/22/12nm; Weebit, the best-funded independent ReRAM licensor (A$167M cash), took ~10+ years to reach ~A$13.5M FY26 revenue; 4DS was suspended from ASX quotation in Apr-2026.

**Evidence:** TRL 8 · Rule 1: SUPPORTED
  - [GlobalFoundries acquires Renesas' non-volatile resistive RAM (CBRAM) technology](https://gf.com/gf-press-release/globalfoundries-acquires-renesas-non-volatile-resistive-ram-technology-to-proliferate-iot-and-5g-applications/) — company, 2023-02. Adesto->Dialog->Renesas CBRAM now owned by GF; being qualified on 22FDX; ~1 extra mask (via search snippet)
  - [New Adesto memory takes 25 years to consume a battery](https://spectrum.ieee.org/new-adesto-memory-takes-25-years-to-consume-a-battery) — news, 2016. Adesto CBRAM ultra-low-energy products shipped (Moneta/Mavriq) (via search snippet)
  - [Weebit Nano expands licensing agreements; three customer chip designs taped out](https://www.weebit-nano.com/news/press-releases/weebit-nano-expands-licensing-agreements-with-key-customers-three-customer-chip-designs-taped-out-to-date/) — company, 2026-07. 3 customer tape-outs; FY26 revenue guide >=A$13.5M; cash A$167M; licensing slowed by fab undercapacity (via search snippet)
  - [4DS Memory filings index (suspension from quotation 2026-04-29)](https://financialfilings.com/companies/4ds-memory-limited/) — other, 2026-04. 4DS (PCMO interface-switching ReRAM) suspended from ASX quotation Apr-2026 (via search snippet)
  - [TSMC 2025 Annual Report ch.5](https://investor.tsmc.com/static/annualReports/2025/english/pdf/2025_tsmc_ar_e_ch5.pdf) — company, 2026. TSMC N12e RRAM consumer-qualified; 22RRAM passed 100K-cycle qualification in 2025 (via search snippet)

**Capital tier:** T1 | **Time to first revenue:** 4-6 years to first meaningful license revenue (Weebit benchmark) | **Gross margin estimate:** 80-90% on license revenue, but revenue tiny

**US manufacturability:** Test chips at SkyWater MN or via MPW; licensees are foundries anywhere

**Who is already doing this:** Weebit Nano (ReRAM IP, SkyWater/onsemi/DB HiTek/TI), GlobalFoundries (owns CBRAM), TSMC (in-house RRAM), Crossbar (private, status unclear), 4DS (suspended)

**Wins on which axis, for which buyer:** eNVM cost (masks) for MCUs — not RAM — for second-tier foundries and IDMs wanting eNVM at 40-130nm

**Survives a 2029 glut?:** yes — Unrelated to DRAM price; but irrelevant to the DRAM shortage too.

**Fatal-flaw candidate:** Decade-long licensing sales cycles in a field where the strongest independent (Weebit) is still sub-scale and foundries own their own RRAM/CBRAM.

*Possible?* yes · *Profitable?* no — revenue too slow and small · *Doable by this founder?* no

*Business-model lenses:* university/lab patent license, IP licensing

### C-24 — RRAM Analog In-Memory-Compute Edge AI Chip

*Sub-branch:* Memristor compute-in-memory (less RAM per unit of work) · *Materials sense:* a-material

**What it is:** An edge-AI inference SoC storing INT4 weights as multi-level conductances in HfOx/TaOx RRAM crossbars on TSMC 22nm/12nm, doing MACs in the array so the device needs little external DRAM.

**Why it could work:** Analog IMC cuts weight-movement energy and DRAM bandwidth; TetraMem (San Jose) validated 22nm MLX200 silicon (May-2026) and taped out a 12nm MLX300 with 64M INT4 params on-chip, 50-80 TOPS/W target (Oct-2026). HPE's memristor program (The Machine) is the cautionary tale: shelved as not economically viable (2015-16).

**Evidence:** TRL 6 · Rule 1: SUPPORTED
  - [TetraMem 22nm multi-level RRAM analog IMC SoC milestone](https://www.businesswire.com/news/home/20260516556464/en/TetraMem-Announces-22nm-Multi-Level-RRAM-Analog-In-Memory-Computing-SoC-Milestone) — company, 2026-05. MLX200 on TSMC 22nm: tape-out, manufacturing, initial silicon validation; sampling 2H-2026 (via search snippet)
  - [TetraMem tapes out 12nm AI SoC (MLX300)](https://www.sttinfo.fi/tiedote/72447857/tetramem-advances-analog-in-memory-computing-with-tapeout-of-new-12nm-ai-soc?publisherId=58763726) — company, 2026-10. 12nm multi-level RRAM A-IMC SoC, 64M INT4 params on-chip, 50-80 TOPS/W target (via search snippet)
  - [HP puts the future of computing on hold](https://www.technologyreview.com/2015/06/04/167804/hp-puts-the-future-of-computing-on-hold/) — news, 2015-06. HP removed memristor from The Machine; not economically viable for volume production (via search snippet)
  - [TSMC 2025 Annual Report ch.5](https://investor.tsmc.com/static/annualReports/2025/english/pdf/2025_tsmc_ar_e_ch5.pdf) — company, 2026. TSMC N12e RRAM consumer-qualified; 22RRAM passed 100K-cycle qualification in 2025 (via search snippet)

**Capital tier:** T3 | **Time to first revenue:** 4+ years (multiple tape-outs, compiler stack, customer qualification) | **Gross margin estimate:** 40-60% if it ever scales

**US manufacturability:** RRAM modules at TSMC (Taiwan; Arizona fab does not list RRAM) — not U.S.-made

**Who is already doing this:** TetraMem (RRAM A-IMC), plus a crowded field of digital/analog edge-AI chips; IBM Research PCM analog AI (HERMES) [UNVERIFIED: training]

**Wins on which axis, for which buyer:** TOPS/W and DRAM bandwidth avoided for always-on edge inference — for wearable, hearing-aid, industrial-sensor and always-on vision module makers

**Survives a 2029 glut?:** partially — Value is energy, not DRAM $/GB, so it survives a glut — but cheap DRAM weakens the 'less RAM' pitch.

**Fatal-flaw candidate:** Analog drift/accuracy plus a software stack war against digital NPUs; TetraMem is already two tape-outs ahead with TSMC access.

*Possible?* yes — silicon validated by TetraMem · *Profitable?* marginal — crowded edge-AI market · *Doable by this founder?* no

*Business-model lenses:* fabless->foundry, IP licensing (TetraMem offers multi-level RRAM IP)

### C-25 — 3D XPoint / PCM Crosspoint Revival for the CXL Memory Tier

*Sub-branch:* Phase-change crosspoint storage-class memory (Optane post-mortem) · *Materials sense:* a-material · *Merged from:* A2.10, B.09

**What it is:** Rebuild Optane-class memory: Ge-Sb-Te phase-change (or OTS selector-only) cells in a 4-deck 20nm-half-pitch crosspoint, sold as CXL Type-3 persistent/capacity memory at a fraction of DRAM $/GB during the shortage.

**Why it could work:** The math looks great in Nov-2026: XPoint Gen2 was 1.31 Gb/mm2 (~3.3x 1b DRAM density) and at full fab loading the die cost computes to ~$1/GB vs DDR5 at ~$20/GB. But Optane died anyway: Intel lost >$7B, took a $559M inventory write-off (Q2-2022); Micron cited 'insufficient market validation', booked ~$545M underutilization in 4 quarters and sold Lehi to TI for $900M (below book). The killers were volume (Lehi underloaded), an Intel-only DDR-T ecosystem, ~3-4x DRAM latency, and the 2019 DRAM glut erasing Optane's ~$6.6/GB price advantage. SanDisk + imec are now prototyping '3D Matrix Memory' (target ~half DRAM cost/bit, no dates).

**Evidence:** TRL 6 · Rule 1: SUPPORTED
  - [Intel 10-Q Q2-2022](https://www.sec.gov/Archives/edgar/data/50863/000005086322000030/intc-20220702.htm) — company, 2022-07. Optane wind-down; $559M inventory impairment (via search snippet)
  - [Micron sells Lehi 3D XPoint fab to Texas Instruments for $900M](https://www.anandtech.com/show/16800) — news, 2021-06. Lehi sold to TI for $900M cash (+~$600M tools), below book value (via search snippet)
  - [Micron updates data center portfolio strategy (ends 3D XPoint)](https://www.nasdaq.com/press-release/micron-updates-data-center-portfolio-strategy-to-address-growing-opportunity-for) — company, 2021-03. 'insufficient market validation' to keep investing in 3D XPoint; CXL pivot (via search snippet)
  - [Persistent Memories Without Optane: Where Would We Be? (Coughlin & Handy)](https://www.snia.org/sites/default/files/2025-05/SNIA-SDC22-Coughlin-Handy-Persistent-Memories-Without-Optane-Where-Would-We-Be.pdf) — conference, 2022. Intel Optane losses >$7B; emerging memory moving to foundry embedded (via search snippet)
  - [Intel 2nd generation XPoint memory](https://www.techinsights.com/blog/memory/intel-2nd-generation-xpoint-memory) — industry, 2020. 256Gb 4-deck die 195.6 mm2, 1.31 Gb/mm2 (via search snippet)
  - [SanDisk makes first 3D Matrix Memory chips aiming for half the cost per bit of DRAM](https://www.notebookcheck.net/SanDisk-makes-first-3D-Matrix-Memory-chips-aiming-for-half-the-cost-per-bit-of-DRAM.1374351.0.html) — news, 2026-08. SanDisk crosspoint-class prototypes on 300mm, multi-Gb, target ~half DRAM cost/bit, no dates (via search snippet)
  - [Does phase change memory ride again with SanDisk?](https://www.eenewseurope.com/en/does-phase-change-memory-ride-again-with-sandisk) — news, 2025. 3D Matrix Memory resembles 3D XPoint; imec 'Project Neo' since 2024 (via search snippet)
  - [Pricing of Intel's Optane DC Persistent Memory Modules Leaks](https://www.anandtech.com/show/14180) — news, 2019-04. PMem 128GB ~$842-893 ($6.6-7.0/GB), 256GB ~$10.4-11.1/GB (via search snippet)
  - [SanDisk Investor Day 2026](https://quartr.com/events/sandisk-corporation-sndk-investor-day-2026_F6lVAkBS) — company, 2026. CROSS-REF (A2.jsonl snippet). SanDisk memory roadmap beyond NAND (3D Matrix Memory nearing product specs).

**Capital tier:** T4 | **Time to first revenue:** 6+ years for a new entrant (tech hit TRL 9 at Intel/Micron 2017-22, but process IP stays with them; new entrants restart near TRL 4-6) | **Gross margin estimate:** theoretical 75-85% at full loading vs $8/GB glut DRAM; deeply negative during ramp (Intel/Micron history)

**US manufacturability:** Lehi UT (the only U.S. XPoint fab) now runs TI analog/embedded at 65/45nm; a new 300mm fab is T4

**Who is already doing this:** SanDisk (3D Matrix Memory with imec), Samsung/SK hynix/Micron selector-only-memory research (IEDM 2022-2024)

**Wins on which axis, for which buyer:** $/GB and capacity vs DRAM for a CXL capacity tier (in theory) — for hyperscaler CXL memory-tier and in-memory database buyers (who already chose CXL DRAM + NVMe/KV-cache offload instead)

**Survives a 2029 glut?:** no — A fab started now ships ~2030 into the cycle after the 2028-29 glut; Optane already showed a DRAM glut erases the price gap that justifies the latency penalty.

**Fatal-flaw candidate:** T4 capital and 6-year timeline, IP owned by Intel/Micron, and the exact volume/ecosystem trap that cost Intel >$7B; incumbents (SanDisk/imec) are ahead.

*Possible?* yes — it shipped 2017-2022 · *Profitable?* no — for anyone below SanDisk/Samsung scale · *Doable by this founder?* no

*Business-model lenses:* fabless->foundry (impossible: no foundry offers it), IP licensing (Intel/Micron unlikely to license)

### C-26 — Optane PMem Salvage: Cheap Memory-Mode Capacity for Cascade/Ice Lake Fleets

*Sub-branch:* Optane post-mortem arbitrage (recovered XPoint modules) · *Materials sense:* c-capital

**What it is:** Buy decommissioned Intel Optane PMem 100/200 modules (128/256/512 GB, 3D XPoint Gen1 media) from U.S. ITAD/recyclers, health-test them (ipmctl SMART/percentage-used, burn-in), and sell validated kits plus a web sizing tool that configures Memory Mode or App Direct for VMware/KVM, SAP HANA, Redis and HPC nodes on 2nd/3rd-gen Xeon Scalable servers.

**Why it could work:** DDR4 RDIMMs rose >50% QoQ in Q3-2026 and DDR4 is being exited, so owners of still-useful Cascade Lake/Ice Lake fleets cannot cheaply add memory. New PMem cost $6.6-11/GB in 2019 and Intel exited with ~2 years of excess XPoint inventory; recovered modules may trade at ~$0.8-2/GB [UNVERIFIED] vs DDR4 RDIMM ~$25+/GB. Memory Mode uses DRAM as cache in front of 4-8x more PMem capacity. Software (sizing, health certificates, config scripts) is the founder's edge.

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [Pricing of Intel's Optane DC Persistent Memory Modules Leaks](https://www.anandtech.com/show/14180) — news, 2019-04. PMem 128GB ~$842-893 ($6.6-7.0/GB), 256GB ~$10.4-11.1/GB (via search snippet)
  - [Intel kills off Optane memory, writes off $559M inventory](https://www.datacenterdynamics.com/en/news/intel-kills-off-optane-memory-writes-off-559-million-inventory) — news, 2022-07. Optane wind-down; reports of ~2 years of excess XPoint inventory (via search snippet)
  - [Intel 10-Q Q2-2022](https://www.sec.gov/Archives/edgar/data/50863/000005086322000030/intc-20220702.htm) — company, 2022-07. Optane wind-down; $559M inventory impairment (via search snippet)
  - [Memory shortages drive DDR4 prices over 50% in Q3 2026; DDR3 also impacted](https://wccftech.com/memory-shortages-drive-ddr4-prices-over-50-in-q3-2026-ddr3-also-impacted-by-higher-costs/) — news, 2026-07. DDR3 4Gb spot ~$3.19/Gb vs DDR5 16Gb ~$2.94/Gb early July 2026 (via search snippet)
  - [DDR4 reportedly leads legacy memory rally; DDR3 in tight supply](https://www.trendforce.com/news/2026/01/19/news-ddr4-reportedly-leads-legacy-memory-rally-with-q1-prices-up-to-50-ddr3-in-tight-supply/) — industry, 2026-01. Makers exiting DDR4 in 2026; DDR3 supply tight (via search snippet)

**Capital tier:** T0 | **Time to first revenue:** 2-6 months: first kits sold on eBay/own storefront to refurb-server buyers and homelab/SMB | **Gross margin estimate:** 30-50% on kits (test + validation premium over raw eBay lots)

**US manufacturability:** No fabrication; U.S. sourcing from ITAD firms and testing in an East Coast garage/lab (Xeon Cascade Lake test server ~$1-3k)

**Who is already doing this:** eBay/refurb-server sellers already list PMem; ITAD firms; refurbished-server resellers bundle it opportunistically — no one sells a validated, sized, warrantied PMem capacity kit [UNVERIFIED]

**Wins on which axis, for which buyer:** $/GB of usable memory capacity for legacy Intel platforms (plus persistence in App Direct) — for SMBs and MSPs running VMware/KVM on Cascade/Ice Lake, research HPC labs, refurb-server resellers, homelab buyers

**Survives a 2029 glut?:** no — When DDR4 falls ~60% and Cascade/Ice Lake servers retire (~2028-29), the arbitrage and the installed base both shrink.

**Fatal-flaw candidate:** Finite, shrinking installed base and supply (Intel exited 2022; only Intel Xeon 2nd/3rd gen support PMem) — a 2-3-year bridge business, not a venture; Memory Mode latency penalty limits buyers.

*Possible?* yes — the parts and platforms exist · *Profitable?* marginal — real but small and temporary · *Doable by this founder?* yes — the most founder-doable card in A2

*Business-model lenses:* recert/brokerage, SaaS (sizing/health tool), data product (PMem health/price index)

### C-27 — SOT-MRAM Last-Level-Cache Chiplet

*Sub-branch:* SOT-MRAM (moonshot SRAM replacement) · *Materials sense:* a-material

**What it is:** A UCIe-attached cache chiplet using spin-orbit-torque MRAM (beta-W/Ta SOT track under CoFeB/MgO MTJ, 2T1R) to replace SRAM last-level cache in AI accelerators at N5-class nodes.

**Why it could work:** imec reports SOT switching <100 fJ/bit and >1e15 endurance (IEDM-2023) and a 2025 IEEE TED study shows BEOL read selectors shrink bitcells 10-40% toward sub-N3 SRAM area; multi-bit VGSOT claims ~3x SRAM density. COMPUTED: even at 0.03 um2 a 1Gb die is ~80 mm2 at ~$262/GB — an SRAM-replacement play, not a DRAM one.

**Evidence:** TRL 4 · Rule 1: SUPPORTED
  - [Why SOT-MRAM can replace SRAM in future cache memories](https://imec-int.com/en/articles/bringing-sot-mram-technology-closer-last-level-cache-memory-specifications) — industry, 2023. imec SOT-MRAM <100 fJ/bit, >1e15 endurance (IEDM 2023) (via search snippet)
  - [SOT-MRAM bitcell scaling with BEOL read selectors (IEEE TED)](https://imec-publications.be/handle/20.500.12860/59271) — peer-reviewed, 2025. BEOL read selectors cut SOT bitcell area 10-40%, approaching sub-N3 SRAM (via search snippet)
  - [MRAM startup makes progress as rival closes (Antaios)](https://www.eenewseurope.com/en/mram-startup-makes-progress-as-rival-closes/) — news, 2021-09. Antaios SOT-MRAM test chip at tier-1 foundry 28/22nm; eVaderis closed (via search snippet)
  - [Antaios company profile](https://app.dealroom.co/companies/antaios) — other, unknown. Antaios listed as 'closed' (undated, unverified) (via search snippet)

**Capital tier:** T3 | **Time to first revenue:** 7+ years | **Gross margin estimate:** unknown; 50% if achieved

**US manufacturability:** Requires a leading-edge foundry MTJ/SOT module (TSMC/Samsung/Intel); none offered commercially

**Who is already doing this:** imec, TSMC/Samsung/Intel R&D; Antaios (Grenoble SOT startup) listed closed [UNVERIFIED]; eVaderis closed 2017

**Wins on which axis, for which buyer:** cache density and standby power vs SRAM — for AI accelerator and CPU designers

**Survives a 2029 glut?:** partially — Not tied to DRAM price, but irrelevant to the DRAM shortage.

**Fatal-flaw candidate:** TRL 4 plus dependence on a leading-edge foundry module that only the foundries/IDMs control; independent SOT startups have folded.

*Possible?* marginal — lab-proven, not product-proven · *Profitable?* no · *Doable by this founder?* no

*Business-model lenses:* IP licensing, fabless->foundry

### C-28 — eMRAM-Unified-Memory Edge MCU (no external DRAM)

*Sub-branch:* Embedded NVM (eMRAM/RRAM/ePCM) SoC · *Materials sense:* mixed:a+b

**What it is:** A fabless edge-AI MCU on GF 22FDX+ with AutoPro150 eMRAM (alt: TSMC 22RRAM) holding 16-64 MB of weights and working data on-die so the board needs no external DRAM/PSRAM or NOR — a way to dodge the DRAM shortage in edge devices.

**Why it could work:** Foundry eNVM is mature: GF AutoPro150 (Auto Grade 1, 500k cycles, <10ns read, volume 2H-2026 Dresden, PDK self-serve), TSMC 22RRAM (100K cycles), ST/Samsung 18nm ePCM (0.059 um2 cell, smallest). Removing an external LPDDR4 (now ~2x price) saves BOM and standby power.

**Evidence:** TRL 8 · Rule 1: SUPPORTED
  - [GlobalFoundries announces AutoPro150 eMRAM on FDX](https://www.globenewswire.com/news-release/2026/03/09/3251832/0/en/GlobalFoundries-Announces-Availability-of-AutoPro150-eMRAM-Technology-on-Enhanced-FDX-Platform-for-Advanced-Automotive-Applications.html) — company, 2026-03. Auto Grade 1 eMRAM, 500k cycles, <10ns read; volume 2H-2026 at Dresden; PDK via GF Connect (via search snippet)
  - [ST first 18nm FD-SOI + ePCM MCU (STM32V8)](https://news.mynavi.jp/techplus/article/20251120-3693534/) — news, 2025-11. ST ePCM 0.059 um2 vs MRAM 0.129 um2 (16nm) vs RRAM 0.174 um2 (12nm) per ST; co-developed with Samsung Foundry (via search snippet)
  - [TSMC 2025 Annual Report ch.5](https://investor.tsmc.com/static/annualReports/2025/english/pdf/2025_tsmc_ar_e_ch5.pdf) — company, 2026. TSMC N12e RRAM consumer-qualified; 22RRAM passed 100K-cycle qualification in 2025 (via search snippet)
  - [Infineon and TSMC to introduce RRAM for automotive MCUs](https://www.eenewseurope.com/en/infineon-and-tsmc-to-introduce-rram-for-automotive-mcus) — news, 2022. AURIX TC4x on TSMC 28nm RRAM (via search snippet)
  - [IEDM 2024 Samsung eMRAM (PC Watch)](https://pc.watch.impress.co.jp/docs/column/semicon/1649812.html) — conference, 2024-12. Samsung eMRAM cell 0.024 um2 (14nm) and 0.017 um2 (8nm), IEDM 2024 paper 11-4 (via search snippet)

**Capital tier:** T2 | **Time to first revenue:** 4+ years (SoC design, AEC/industrial qual, ecosystem) | **Gross margin estimate:** 40-55%

**US manufacturability:** Weak: GF 22FDX eMRAM is in Dresden (not Malta NY); TSMC RRAM in Taiwan; ST ePCM captive (Crolles/Samsung). No U.S. line offers this eNVM at 22nm.

**Who is already doing this:** ST (STM32V8 ePCM), Infineon (AURIX TC4x RRAM), NXP/Renesas eMRAM MCUs [UNVERIFIED: training], GF automotive eMRAM customers (Bosch engagement)

**Wins on which axis, for which buyer:** BOM and standby power (no external DRAM/NOR), instant-on — for industrial/automotive edge-AI module makers

**Survives a 2029 glut?:** partially — The 'avoid DRAM' pitch weakens when LPDDR4 is cheap; power and instant-on remain.

**Fatal-flaw candidate:** Head-on competition with the top-5 MCU vendors who already own eNVM MCUs, and not manufacturable in the U.S.

*Possible?* yes · *Profitable?* no — for a startup vs ST/Infineon/NXP/Renesas · *Doable by this founder?* no

*Business-model lenses:* fabless->foundry

### C-29 — NVM-EOL Migration Finder (MRAM/FeRAM/ReRAM cross-reference SaaS)

*Sub-branch:* Software tool for the shortage, grounded in emerging-NVM device data · *Materials sense:* none

**What it is:** A web app that ingests lifecycle/PCN/EOL notices and distributor data (e.g., Renesas serial EEPROM EOL with last-time ship 2026-10-31, DDR3/DDR4 EOLs) and recommends pin- and protocol-compatible emerging-NVM replacements (Everspin Toggle/xSPI MRAM, FeRAM, Netsol MRAM, ReRAM-based parts) with BOM cost, lead-time (e.g., 20-26 weeks for Everspin xSPI) and qualification deltas; revenue from seats for component engineers plus referral fees from authorized distributors.

**Why it could work:** 2026 is an EOL wave (DDR3/DDR4 exits, serial EEPROM EOLs) during a shortage, and emerging-NVM parts are under-known by component engineers. The founder can build it with no hardware capital; device knowledge from this branch becomes the data moat (density, endurance, interface compatibility).

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [Renesas EOL plan: serial EEPROM products](https://www.renesas.cn/zh/document/gde/eol-plan-serial-eeprom-products) — company, 2025-11. Renesas serial EEPROM families EOL, last-time shipment 2026-10-31 (via search snippet)
  - [DDR4 reportedly leads legacy memory rally; DDR3 in tight supply](https://www.trendforce.com/news/2026/01/19/news-ddr4-reportedly-leads-legacy-memory-rally-with-q1-prices-up-to-50-ddr3-in-tight-supply/) — industry, 2026-01. Makers exiting DDR4 in 2026; DDR3 supply tight (via search snippet)
  - [EM128LXQAB313IS2T DigiKey listing](https://punchouttest.digikey.hk/en/products/detail/everspin-technologies-inc/EM128LXQAB313IS2T/24375470) — industry, 2026. Everspin 128Mb xSPI MRAM manufacturer lead time 26 weeks (via search snippet)
  - [EM064LX Future Electronics listing](https://futureelectronics.com/p/semiconductors--memory--RAM--nvram--mram/em064lxoab320is1t-everspin-technologies-4175573) — industry, 2026. 64Mb xSPI STT-MRAM $39.38 @480, 20-week lead time (via search snippet)

**Capital tier:** T0 | **Time to first revenue:** 6-9 months: first paid seats from mid-size industrial OEMs; referral revenue later | **Gross margin estimate:** 75-85%

**US manufacturability:** n/a (software); promotes U.S.-made parts (Everspin Chandler) as a filter

**Who is already doing this:** SiliconExpert (Arrow), Z2Data, Octopart/Nexar (Altium, now Renesas-owned [UNVERIFIED]), Accuris/IHS parts databases, Findchips

**Wins on which axis, for which buyer:** time-to-replacement and supply security for component engineers — for component/reliability engineers at industrial, medical and defense OEMs facing NVM/DRAM EOL

**Survives a 2029 glut?:** partially — EOLs continue in a glut, but shortage urgency and willingness to pay fall.

**Fatal-flaw candidate:** Incumbent lifecycle databases already provide cross-references; the emerging-NVM slice may be too narrow to sustain standalone SaaS.

*Possible?* yes · *Profitable?* marginal — crowded by SiliconExpert/Z2Data · *Doable by this founder?* yes

*Business-model lenses:* SaaS, data product, referral/brokerage

### C-30 — Floating-body 1T-DRAM (Z-RAM lineage) on U.S. SOI

*Sub-branch:* Capacitor-less silicon DRAM: floating body · *Materials sense:* mixed:b+c

**What it is:** Recreate a Z-RAM/Toshiba-FBC-style floating-body 1T cell (charge held in the body of an SOI MOSFET and read as a threshold-voltage shift) on a GlobalFoundries SOI flow (45RFSOI-class at a U.S. GF fab [UNVERIFIED-training]; note 22FDX is made in Dresden, not the U.S.). Product: standalone 2-4 Gb DDR3/DDR4-interface dies for legacy-DRAM buyers, or last-level-cache macros.

**Why it could work:** No storage capacitor, so only 1-2 extra masks on a logic SOI flow instead of a DRAM stack-capacitor module. Depreciated SOI capacity exists in the U.S. On paper an 8F2 cell at 45nm gives 0.031 Gb/mm2 and about $24/GB including test (A3_device_params C-30), which is below today's DDR5 spot (~$27/GB). The 2026 capacitor-less revival (NEO 3D X-DRAM PoC) shows the industry still wants capacitor-less DRAM.

**Evidence:** TRL 4 · Rule 1: SUPPORTED
  - [NEO Semiconductor demonstrates 3D X-DRAM proof of concept](https://www.storagenewsletter.com/2026/05/13/neo-semiconductor-demonstrates-3d-x-dram-proof-of-concept-secures-strategic-investment-to-advance-ai-memory/) — news, 2026-04. 2026 capacitor-less DRAM revival: PoC retention >1 s at 85C, >1e14 cycles, <10 ns, fabbed at TSRI (IGZO/3D-NAND-style, not Si floating body) (CROSS-REFERENCE: seen in another agent's search results, not opened by A3)
  - [DRAM value-per-area chart (Kurnal Insights)](https://www.kitguru.net/channel/generaltech/joao-silva/new-dram-value%E2%80%91per%E2%80%91area-chart-draws-attention-amid-rising-memory-prices/) — news, 2026-09. 1b DRAM bit density ~0.436 Gb/mm2, the reference against which A3 densities are compared (CROSS-REFERENCE: seen in another agent's search results, not opened by A3)
  - [Innovative Silicon Z-RAM (AMD 2006, Hynix 2007 licenses; company closed 2010; patents to Micron) and Toshiba FBC ISSCC/IEDM papers 2002-2008]() — conference, 2002-2010. [UNVERIFIED-training] citation from A3 training data (<= mid-2026). No URL could be opened or seen this session: the shared WebSearch budget was exhausted and web hosts returned proxy 403. Verify agent: add a URL or downgrade. Shows floating-body cells worked in 128Mb-class SOI test chips but never reached a qualified product.

**Capital tier:** T3 | **Time to first revenue:** >60 months (needs foundry JDA, array-scale reliability, then qualification) | **Gross margin estimate:** negative in glut; ~10-20% at 2026 spot if it worked

**US manufacturability:** A U.S. GlobalFoundries SOI line (Malta NY / Essex VT; which SOI flows run in the U.S. in 2026 is [UNVERIFIED-training]) under a JDA. GF offers no capacitor-less DRAM today, and A3 knows no U.S. line running one.

**Who is already doing this:** Nobody in Si floating-body production. Micron reportedly holds the ISi Z-RAM patents [UNVERIFIED-training]. NEO Semiconductor (3D X-DRAM, see C-05) and Unisantis (Dynamic Flash Memory) [UNVERIFIED-training] are the capacitor-less revivals. Samsung and SK hynix publish capacitor-less 3D DRAM research.

**Wins on which axis, for which buyer:** Nominal $/GB vs 2026 DDR5 spot plus process simplicity. It wins on no axis once DRAM prices normalize. — for Hypothetical legacy DDR3/DDR4 industrial buyers; SoC teams wanting dense LLC on SOI.

**Survives a 2029 glut?:** no — Computed ~$24/GB against ~$10-12/GB DDR5 in the A-05 glut and ~$2.7/GB incumbent DRAM cost. Density is 14x below 1b DRAM, so even a perfect cell loses.

**Fatal-flaw candidate:** Physics at scale: body charge is a few hundred electrons at 45nm and tens in thin FD-SOI, so sense margin, retention and disturb immunity collapse with variability. AMD and Hynix both licensed Z-RAM and dropped it (2006-2010) [UNVERIFIED-training].

*Possible?* marginal — demonstrated in test chips 15-20 years ago, never qualified; scaling makes it harder · *Profitable?* no — 14x density gap vs 1b DRAM; ~$24/GB vs glut ~$11/GB · *Doable by this founder?* no — T3 device program

*Business-model lenses:* university/lab patent license (expired/expiring 2002-2008 filings); fabless->foundry; IP licensing — all fail on cost

### C-31 — Thyristor RAM revival (T-RAM TCCT / Kilopass VLT)

*Sub-branch:* Capacitor-less silicon DRAM: thyristor · *Materials sense:* b-process

**What it is:** Revive the thin capacitively-coupled thyristor (TCCT) T-RAM cell, or Kilopass's vertical-layered-thyristor (VLT) cross-point cell, as a capacitor-less SRAM/DRAM replacement on a U.S. line (a GF U.S. SOI flow or SkyWater 90nm FD-SOI [UNVERIFIED-training]). Product: cache macros, or a standalone DRAM-replacement die.

**Why it could work:** A PNPN latch stores the bit with built-in gain, so it reads fast (1-2 ns claimed) and needs no capacitor. The VLT marketing claim (4F2, no refresh, 'DRAM cost minus 45%') computes to ~$2.8/GB, DRAM-cost parity (A3-02b). A planar TCCT at 10F2/32nm computes to ~$18/GB. The earliest Stanford NDR-cell patents (~1998) have expired, so IP is no longer the barrier [UNVERIFIED-training].

**Evidence:** TRL 4 · Rule 1: SUPPORTED
  - [DRAM value-per-area chart (Kurnal Insights)](https://www.kitguru.net/channel/generaltech/joao-silva/new-dram-value%E2%80%91per%E2%80%91area-chart-draws-attention-amid-rising-memory-prices/) — news, 2026-09. 1b DRAM bit density ~0.436 Gb/mm2, the reference against which A3 densities are compared (CROSS-REFERENCE: seen in another agent's search results, not opened by A3)
  - [T-RAM Semiconductor TCCT (AMD license 2006, GlobalFoundries 32/22nm SOI partnership 2009; company defunct ~2010-11) and Kilopass VLT announcement (2016; Kilopass acquired by Synopsys 2018)]() — conference, 1998-2018. [UNVERIFIED-training] citation from A3 training data (<= mid-2026). No URL could be opened or seen this session: the shared WebSearch budget was exhausted and web hosts returned proxy 403. Verify agent: add a URL or downgrade. Shows TCCT SRAM test arrays on SOI; VLT never shown in an array.

**Capital tier:** T3 | **Time to first revenue:** >60 months | **Gross margin estimate:** negative

**US manufacturability:** A GF U.S. SOI flow or SkyWater Bloomington MN 90nm FD-SOI [UNVERIFIED-training]. Neither offers a thyristor module.

**Who is already doing this:** Nobody commercially. GF dropped T-RAM. Synopsys owns the Kilopass assets and has not marketed VLT [UNVERIFIED-training]. There is some academic TCAD work on 3D thyristor DRAM.

**Wins on which axis, for which buyer:** Read latency (SRAM-class) and density vs SRAM. It does not win on $/GB vs DRAM except in the never-demonstrated VLT claim. — for SoC cache designers (if it worked); hypothetical DRAM buyers.

**Survives a 2029 glut?:** no — ~$18/GB planar against $10-12/GB glut DDR5. The only version that beats DRAM (VLT 4F2) is UNSUPPORTED marketing.

**Fatal-flaw candidate:** The ON state needs a holding current. At 1-100 pA/cell a 1 Gb array idles at ~1-110 mA, and the bistable window shrinks at 85-125C. Three serious attempts failed to productize: AMD 2006, GlobalFoundries 2009, Kilopass 2016 [UNVERIFIED-training].

*Possible?* marginal — TCCT arrays demonstrated, temperature/standby problems unsolved · *Profitable?* no · *Doable by this founder?* no

*Business-model lenses:* expired-patent practice; IP licensing; fabless->foundry

### C-32 — Si gain-cell eDRAM (GCRAM) IP for U.S. trailing-node SoCs

*Sub-branch:* Capacitor-less silicon DRAM: 2T/3T gain-cell eDRAM in logic · *Materials sense:* b-process

**What it is:** A memory-IP company that builds and licenses a logic-compatible (zero extra masks) 2T/3T silicon gain-cell eDRAM compiler, first for SkyWater S130/S90 FD-SOI and GlobalFoundries 12LP+ (Malta NY). It replaces 6T SRAM in edge-AI activation buffers, image-sensor line buffers and FPGA block RAM. Revenue is a per-node license fee plus royalty, sold through the foundry IP catalog, as SkyWater already does for Weebit ReRAM.

**Why it could work:** SRAM scaling has stalled, and 6T SRAM costs ~$80-120/GB of die area at every node from 28nm to N2 (C-35). A gain cell at ~50% of 6T area computes to ~$47/GB area-equivalent at 28nm, about 40% memory-area savings with lower leakage per bit. Foundries pay for differentiated embedded memory: GF bought Renesas CBRAM, and SkyWater qualified third-party ReRAM. Si read devices are fast; oxide gain cells (C-01) are slow (DATE 2026).

**Evidence:** TRL 6 · Rule 1: SUPPORTED
  - [Disrupting the DRAM roadmap with capacitor-less IGZO DRAM technology](https://www.imec-int.com/en/articles/disrupting-dram-roadmap-capacitor-less-igzo-dram-technology) — industry, 2023. 2T0C gain-cell concept: charge stored on the read-transistor gate capacitance — the same topology as Si gain cells (CROSS-REFERENCE: seen in another agent's search results, not opened by A3)
  - [IGZO-2T eDRAM: hybrid IGZO/Si gain cells (DATE 2026)](https://past.date-conference.com/proceedings-archive/2026/DATA/154.pdf) — conference, 2026. IGZO 2T eDRAM is slow (low mobility); hybrid IGZO/Si gain cells proposed — Si read devices give speed, oxide gives retention (CROSS-REFERENCE: seen in another agent's search results, not opened by A3)
  - [Weebit Nano ReRAM IP achieves high-temperature qualification in SkyWater S130](https://www.skywatertechnology.com/weebit-nano-reram-ip-achieves-high-temperature-qualification-in-skywater-s130-process/) — company, 2023-11. SkyWater's S130 PDK hosts third-party memory IP — precedent for licensing a memory macro into a U.S. 130nm foundry (CROSS-REFERENCE: seen in another agent's search results, not opened by A3)
  - [GlobalFoundries acquires Renesas CBRAM technology](https://gf.com/gf-press-release/globalfoundries-acquires-renesas-non-volatile-resistive-ram-technology-to-proliferate-iot-and-5g-applications/) — company, 2023-02. Foundries pay for differentiated embedded-memory IP (GF bought CBRAM, ~1 extra mask, qualifying on 22FDX) (CROSS-REFERENCE: seen in another agent's search results, not opened by A3)
  - [Georgia Tech (Shimeng Yu) 3T IWO eDRAM for in-memory compute](https://hg.gatech.edu/node/675050) — industry, 2024. U.S. university gain-cell eDRAM work (oxide-channel 3T) for compute-in-memory (CROSS-REFERENCE: seen in another agent's search results, not opened by A3)
  - [OpenRAM open-source SRAM compiler (GitHub README; v1.2.50 commit 2026-10-27)](https://github.com/VLSIDA/OpenRAM) — industry, 2026-10. Opened via git: BSD-3 SRAM compiler, generates GDS/LEF/Liberty/SPICE for sky130 (SkyWater) and gf180mcu; actively maintained (last commit 2026-10-27)
  - [Si gain-cell eDRAM literature: Intel 2T gain cell 65nm (Somasekhar, ISSCC 2008/JSSC 2009); Teman/Giterman/Burg 28nm FD-SOI gain cells; RAAAM Memory Technologies GCRAM]() — conference, 2008-2025. [UNVERIFIED-training] citation from A3 training data (<= mid-2026). No URL could be opened or seen this session: the shared WebSearch budget was exhausted and web hosts returned proxy 403. Verify agent: add a URL or downgrade. Shows silicon-proven gain-cell macros at 65-16nm in academia and one startup.

**Capital tier:** T2 | **Time to first revenue:** 24-36 months (two MPW test chips, characterization, first evaluation license) | **Gross margin estimate:** 80-90% (IP license/royalty)

**US manufacturability:** SkyWater Bloomington MN (S130, 90nm FD-SOI) and Fab 25 Austin TX; GlobalFoundries Fab 8 Malta NY (12LP+). Test chips go via ChipFoundry/SkyWater MPW shuttles.

**Who is already doing this:** RAAAM Memory Technologies (Israel; GCRAM, claims ~2x SRAM density) [UNVERIFIED-training]; academic groups at Bar-Ilan, EPFL and Georgia Tech (oxide 3T); Synopsys/Arm SRAM compilers as incumbents. C-01 covers oxide (IGZO) gain cells; this card is Si-only and zero-mask.

**Wins on which axis, for which buyer:** On-chip memory density (bits/mm2) and standby leakage per bit vs 6T SRAM at equal process cost. — for Edge-AI and sensor SoC teams on U.S. trailing nodes; DoD trusted-foundry ASIC programs; FPGA vendors needing denser block RAM.

**Survives a 2029 glut?:** yes — Embedded memory is priced in die area inside someone else's SoC, so it is decoupled from DRAM contract prices.

**Fatal-flaw candidate:** At 85-125C Si gain-cell retention is ~10-100 us, so refresh erodes the power advantage. Royalties at trailing nodes are small; the MoSys 1T-SRAM precedent saw modest royalties, then decline [UNVERIFIED-training]. RAAAM got there first.

*Possible?* yes — silicon-proven in academia and at one startup · *Profitable?* marginal — high-margin IP but small trailing-node royalty pool and an incumbent startup · *Doable by this founder?* marginal — needs a circuit cofounder and ~$2-3M

*Business-model lenses:* IP licensing; university/lab patent license (Bar-Ilan/EPFL/Georgia Tech); fabless->foundry test chips; defense-first (trusted SkyWater)

### C-33 — OpenRAM macro service for U.S. open-PDK tapeouts (SkyWater S130)

*Sub-branch:* SRAM-at-scale on trailing nodes: on-chip memory supply for U.S.-fab ASICs · *Materials sense:* c-capital

**What it is:** A software-first business that generates, DRC/LVS-verifies, silicon-characterizes and supports SRAM macros (later gain-cell macros) for teams taping out on SkyWater S130 (Bloomington, MN) through ChipFoundry shuttles. It is built on the BSD-licensed OpenRAM compiler and sold as a SaaS subscription (hosted macro generator, characterized Liberty/LEF/GDS libraries, CI regression) plus per-tapeout support, listed on the ChipFoundry Marketplace.

**Why it could work:** OpenRAM is alive (v1.2.50, 2026-10-27), but only 1-4 KB prebuilt sky130 macros exist. They are periphery-dominated: a 2 KB macro takes 0.2845 mm2 (57.6 kbit/mm2), ~6x worse than the 1.896 um2 bitcell allows. Small teams cannot afford commercial memory compilers ($50k-$200k+ per node [UNVERIFIED-training]). ChipFoundry runs an IP marketplace on an active SkyWater shuttle flow. The work is Python, CI and web tooling, which is the founder's skill set.

**Evidence:** TRL 6 · Rule 1: SUPPORTED
  - [OpenRAM open-source SRAM compiler (GitHub README; v1.2.50 commit 2026-10-27)](https://github.com/VLSIDA/OpenRAM) — industry, 2026-10. Opened via git: BSD-3 SRAM compiler, generates GDS/LEF/Liberty/SPICE for sky130 (SkyWater) and gf180mcu; actively maintained (last commit 2026-10-27)
  - [openram on PyPI](https://pypi.org/pypi/openram/json) — industry, 2026-10. Opened: release 1.2.50 on 2026-10-27; first PyPI release 2023-02-08
  - [SkyWater sky130_fd_bd_sram bitcell library (LEF)](https://github.com/google/skywater-pdk-libs-sky130_fd_bd_sram) — industry, 2021-10. Opened via git: SkyWater 130nm single-port 6T SRAM cell is 1.200 x 1.580 um = 1.896 um2 (VERIFIED primary PDK data)
  - [OpenRAM sky130 SRAM macros (LEF sizes)](https://github.com/VLSIDA/sky130_sram_macros) — industry, 2024-07. Opened via git: 2 KB 1rw1r macro = 683.1 x 416.54 um (0.2845 mm2, 57.6 kbit/mm2); only 1-4 KB macros published
  - [ChipFoundry Caravel user project (README)](https://github.com/chipfoundry/caravel_user_project) — industry, 2026-04. Opened via git: active SkyWater 130nm shuttle flow (last commit 2026-04-23); ChipFoundry Marketplace sells 'additional IP blocks, EDA tools, and shuttle services'
  - [Enabling Design Technology Co-Optimization of SRAMs though Open-Source Software (IEDM 2020)](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=9372047) — conference, 2020-12. URL seen in OpenRAM README (not opened): IEDM paper on open-source SRAM DTCO

**Capital tier:** T0 | **Time to first revenue:** 9-15 months (paid support/macro packages to MPW teams; one ~$10-15k shuttle slot for silicon characterization) | **Gross margin estimate:** 70-85% (software/services)

**US manufacturability:** Customer silicon is made at SkyWater Bloomington MN (S130) via ChipFoundry MPW, later SkyWater Fab 25 Austin. The venture itself is software in the U.S.

**Who is already doing this:** VLSIDA/UC Santa Cruz (OpenRAM maintainers, free); ChipFoundry marketplace vendors; commercial compilers from Synopsys and Arm (not offered for open PDKs at small-team prices) [UNVERIFIED-training]; SkyWater's own IP partners.

**Wins on which axis, for which buyer:** Supply security and access: time and cost to get characterized on-chip RAM in a U.S.-fabbed ASIC. Not $/GB. — for University VLSI labs, DoD SBIR/STTR ASIC teams needing U.S.-only fabrication, hardware startups on ChipFoundry/SkyWater shuttles.

**Survives a 2029 glut?:** yes — Demand tracks ASIC tapeout activity and U.S.-fab policy, not DRAM prices.

**Fatal-flaw candidate:** Tiny market (MPW customers number in the hundreds per year) with low willingness to pay for something free (BSD). UCSC, SkyWater or ChipFoundry could bundle equivalent macros at no charge. It is also on-chip memory IP, not 'RAM' in the mission's main sense.

*Possible?* yes — compiler and PDK exist; needs larger, better-characterized macros · *Profitable?* marginal — likely <$1M ARR ceiling unless it expands to gain-cell IP (C-32) or more PDKs · *Doable by this founder?* yes — T0, software-led, starts alongside the day job

*Business-model lenses:* SaaS; IP licensing (support/indemnity on open IP); fabless->foundry (MPW); defense-first (U.S.-only fab flows)

### C-34 — Depreciated-fab revival of IBM-heritage deep-trench eDRAM

*Sub-branch:* 1T1C eDRAM at foundries; depreciated trailing-edge capacity · *Materials sense:* c-capital

**What it is:** Restart IBM-heritage 1T1C deep-trench eDRAM (32SOI/14HP class) on a depreciated U.S. 300mm line: onsemi East Fishkill NY (the former IBM/GF Fab 10) or GF Fab 8 Malta. Sell standalone 'fast DRAM' dies or LLC chiplets to U.S. HPC/ASIC buyers.

**Why it could work:** The 0.0174 um2 14HP cell (IBM, IEDM 2014) is the densest logic-compatible DRAM ever shipped. It was used in POWER8/9 and z15. A fully depreciated line might sell wafers near cash cost (~$2.5k), which computes to ~$20/GB standalone including test (C-34), below today's ~$27/GB DDR5 spot.

**Evidence:** TRL 5 · Rule 1: SUPPORTED
  - [DRAM value-per-area chart (Kurnal Insights)](https://www.kitguru.net/channel/generaltech/joao-silva/new-dram-value%E2%80%91per%E2%80%91area-chart-draws-attention-amid-rising-memory-prices/) — news, 2026-09. 1b DRAM bit density ~0.436 Gb/mm2, the reference against which A3 densities are compared (CROSS-REFERENCE: seen in another agent's search results, not opened by A3)
  - [DRAM vs N2 wafer value comparison](https://xenospectrum.com/dram-n2-wafer-price-comparison/) — news, 2026-09. Kurnal: 1b DRAM sales value per mm2 ~54% above TSMC N2 — logic-process memory cannot match DRAM bits per wafer dollar (CROSS-REFERENCE: seen in another agent's search results, not opened by A3)
  - [IBM 14nm SOI FinFET with 0.0174 um2 eDRAM (IEDM 2014); Intel 22nm eDRAM 0.029 um2 (VLSI 2013, Crystalwell 128MB); IBM POWER10/z16 moved to Samsung 7nm without eDRAM; GF sold East Fishkill to onsemi (2019-2022)]() — conference, 2013-2022. [UNVERIFIED-training] citation from A3 training data (<= mid-2026). No URL could be opened or seen this session: the shared WebSearch budget was exhausted and web hosts returned proxy 403. Verify agent: add a URL or downgrade. Shows deep-trench eDRAM shipped in volume (TRL 9) and then was retired.

**Capital tier:** T3 | **Time to first revenue:** 48-60 months (re-establish DT module, requalify) | **Gross margin estimate:** negative vs glut

**US manufacturability:** onsemi East Fishkill NY (ex-IBM 300mm; now running onsemi products) or GF Fab 8 Malta NY. A3 knows of no current U.S. deep-trench eDRAM capability [UNVERIFIED-training].

**Who is already doing this:** Nobody. IBM exited eDRAM with POWER10/z16. Intel ended Crystalwell-class eDRAM. GF no longer offers 14HP [UNVERIFIED-training].

**Wins on which axis, for which buyer:** Latency (~2 ns macro cycle) vs commodity DRAM. Nothing on $/GB. — for HPC/ASIC teams wanting a fast on-package cache tier (hypothetical).

**Survives a 2029 glut?:** no — ~$20/GB at depreciated cash cost and ~$50/GB at a normal wafer price, against $10-12/GB glut DDR5 and ~$2.7/GB DRAM cost.

**Fatal-flaw candidate:** Depreciation cannot close a 17x density gap: wafer cost is a minor term once density is 0.026 vs 0.436 Gb/mm2. The tool set and know-how are likely gone [UNVERIFIED-training].

*Possible?* marginal — it shipped before, but the process is retired · *Profitable?* no — density gap dominates even at cash-cost wafers · *Doable by this founder?* no

*Business-model lenses:* c-capital arbitrage of a depreciated fab; fabless->foundry — both fail

### C-35 — Trailing-node bulk SRAM as a DRAM substitute (SRAM-DIMM/CXL)

*Sub-branch:* SRAM-at-scale on trailing nodes · *Materials sense:* c-capital

**What it is:** A fabless 'SRAM-DIMM/CXL' product: ~1 Gb standalone 6T SRAM dies on 28nm-class foundry wafers (GF 12/14nm at Malta NY, or UMC/TSMC 28nm) behind a DDR4/CXL controller on a module. It is sold as refresh-free, lower-latency DRAM-replacement capacity during the shortage.

**Why it could work:** Trailing-node logic wafers are cheap (~$3k at 28nm) and DRAM spot is ~$27/GB, so naive math looks close. SRAM is static (no refresh), simple to test, and made by many foundries, so supply is secure.

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [SkyWater sky130_fd_bd_sram bitcell library (LEF)](https://github.com/google/skywater-pdk-libs-sky130_fd_bd_sram) — industry, 2021-10. Opened via git: SkyWater 130nm single-port 6T SRAM cell is 1.200 x 1.580 um = 1.896 um2 (VERIFIED primary PDK data)
  - [DRAM value-per-area chart (Kurnal Insights)](https://www.kitguru.net/channel/generaltech/joao-silva/new-dram-value%E2%80%91per%E2%80%91area-chart-draws-attention-amid-rising-memory-prices/) — news, 2026-09. 1b DRAM bit density ~0.436 Gb/mm2, the reference against which A3 densities are compared (CROSS-REFERENCE: seen in another agent's search results, not opened by A3)
  - [DRAM vs N2 wafer value comparison](https://xenospectrum.com/dram-n2-wafer-price-comparison/) — news, 2026-09. Kurnal: 1b DRAM sales value per mm2 ~54% above TSMC N2 — logic-process memory cannot match DRAM bits per wafer dollar (CROSS-REFERENCE: seen in another agent's search results, not opened by A3)
  - [Published 6T SRAM bitcells: 65nm 0.525 / 40nm 0.242 / 28nm 0.127 / 16nm 0.074 / N5 0.021 um2; TSMC N2 macro 38.1 Mb/mm2 (IEDM 2024)]() — conference, 2006-2024. [UNVERIFIED-training] citation from A3 training data (<= mid-2026). No URL could be opened or seen this session: the shared WebSearch budget was exhausted and web hosts returned proxy 403. Verify agent: add a URL or downgrade.

**Capital tier:** T2 | **Time to first revenue:** ~24 months (28nm mask set + controller/module) | **Gross margin estimate:** deeply negative (~$100/GB COGS vs ~$27/GB price)

**US manufacturability:** GF Fab 8 Malta NY (12/14nm) is the closest U.S. option. 28nm SRAM die is otherwise Taiwan-made.

**Who is already doing this:** Nobody sells SRAM as bulk DRAM capacity. SRAM capacity is sold only as on-die memory (Groq, Cerebras, see C-38/C-39) or small standalone parts (C-36).

**Wins on which axis, for which buyer:** None at a DRAM interface: the latency advantage is lost behind the DDR/CXL controller (~50-100 ns), and it loses on $/GB by 3-40x. — for None identified. A DRAM buyer will not pay 4x spot for refresh-free capacity.

**Survives a 2029 glut?:** no — Computed COGS ~$79-120/GB at N5-N2 and ~$99-144/GB at 16-40nm, against $27/GB spot today, $10-12/GB in the glut and $2.7/GB DRAM cost.

**Fatal-flaw candidate:** SRAM has a ~$80-120/GB silicon+test cost floor at every node from 28nm to N2. SRAM cell scaling has stalled, so trailing nodes are not cheaper per SRAM bit: 40nm is ~$144/GB and 65nm ~$268/GB.

*Possible?* yes — trivially manufacturable · *Profitable?* no — 4x above today's spot, ~10x above glut · *Doable by this founder?* no

*Business-model lenses:* fabless->foundry; module maker — both lose on cost

### C-36 — U.S.-fabbed long-lifecycle SRAM second source (SkyWater Fab 25)

*Sub-branch:* SRAM 'RAM' products on depreciated U.S. 200mm capacity · *Materials sense:* c-capital

**What it is:** A fabless company with a pin-compatible family of 4-64 Mb async and QDR/sync SRAMs (plus a rad-tolerant option on SkyWater 90nm FD-SOI). Wafers come from SkyWater Fab 25 Austin TX (the ex-Cypress 200mm SRAM fab, 130-65nm), with U.S. assembly and test. Parts ship with 15-20-year longevity commitments to defense, avionics, industrial and networking OEMs replacing EOL or non-U.S.-owned sources.

**Why it could work:** Legacy SRAM is priced per part, not per GB. A 16Mb die at 65nm is ~12 mm2, so COGS is ~$2.4 against distributor prices of ~$10-40 [UNVERIFIED-training]. Demand comes from long-lifecycle designs, not the DRAM cycle. Fab 25 made Cypress memory for decades and now runs as a foundry under an Infineon supply agreement. U.S.-fab provenance and longevity matter to DMSMS programs. ISSI is owned by China's Ingenic [UNVERIFIED-training].

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [SkyWater to Acquire Infineon's Austin Fab (Fab 25)](https://www.businesswire.com/news/home/20250226773415/en/SkyWater-to-Acquire-Infineons-Austin-Fab-and-Establish-Strategic-Partnership-to-Expand-U.S.-Foundry-Capacity-for-Foundational-Chips) — company, 2025-02. 200mm 130-65nm ex-Cypress fab becomes a SkyWater foundry with a long-term Infineon supply agreement (CROSS-REFERENCE: seen in another agent's search results, not opened by A3)
  - [SkyWater acquires Infineon's 200mm fab (close and capacity)](https://marklapedus.substack.com/p/skywater-acquires-infineons-200mm) — news, 2025. Closed 2025-06-30; ~400k wafer starts/yr; ~$73M at close; ~1,000 employees; conversion to foundry (CROSS-REFERENCE: seen in another agent's search results, not opened by A3)
  - [Infineon retains U.S. manufacturing via SkyWater supply agreement](https://new-origin.infineon.com/cms/en/about-infineon/press/press-releases/2025/INFXX202502-066.html) — company, 2025-02. Legacy Infineon/Cypress products keep U.S. wafer supply through SkyWater (CROSS-REFERENCE: seen in another agent's search results, not opened by A3)
  - [Cypress Minnesota wafer fab sale](https://us.design-reuse.com/news/41552/cypress-minnesota-wafer-fabrication-facility-sale.html) — news, 2017. Cypress sold its Minnesota fab (now SkyWater Bloomington), consolidating into Fab 25 Austin (CROSS-REFERENCE: seen in another agent's search results, not opened by A3)
  - [Frontgrade case study: Everspin Toggle MRAM for space](https://www.frontgrade.com/news/new-case-study-touts-everspins-toggle-mram-highly-reliable-memory-technology-space) — company, 2020. Qualified hi-rel/space memory reaches primes through channels like Frontgrade — the buyer channel for U.S.-made long-lifecycle memory (CROSS-REFERENCE: seen in another agent's search results, not opened by A3)
  - [Sandia: evolving semiconductor technology for national security](https://www.sandia.gov/research/news/evolving-semiconductor-technology-for-national-security-applications/) — government, 2026-05. DoE/NNSA funds trusted U.S. memory in the MESA rad-hard fab — evidence that U.S. trusted-memory buyers exist (CROSS-REFERENCE: seen in another agent's search results, not opened by A3)
  - [SkyWater sky130_fd_bd_sram bitcell library (LEF)](https://github.com/google/skywater-pdk-libs-sky130_fd_bd_sram) — industry, 2021-10. Opened via git: SkyWater 130nm single-port 6T SRAM cell is 1.200 x 1.580 um = 1.896 um2 (VERIFIED primary PDK data)

**Capital tier:** T2 | **Time to first revenue:** 30-36 months (design, 65-90nm masks, AEC-Q100/QML-style qualification) | **Gross margin estimate:** 45-60%

**US manufacturability:** SkyWater Fab 25 Austin TX (200mm, 130-65nm) and SkyWater Bloomington MN (S130; 90nm FD-SOI for rad-tolerant parts [UNVERIFIED-training]); a U.S. hi-rel OSAT for assembly and test.

**Who is already doing this:** Infineon (ex-Cypress SRAM; U.S. supply now via SkyWater), Renesas, ISSI (Ingenic-owned), GSI Technology (TSMC-fabbed high-speed SRAM), Alliance Memory, Rochester Electronics (EOL continuation, Newburyport MA). Rad-hard: Honeywell (Plymouth MN), BAE Systems (Manassas VA), Frontgrade [UNVERIFIED-training for current product status].

**Wins on which axis, for which buyer:** Supply security and lifecycle length: U.S.-fab, 20-year availability, non-PRC ownership. Not $/GB. — for Defense primes (avionics, radar, EW), DMSMS/obsolescence programs, industrial controls, networking line cards using QDR SRAM.

**Survives a 2029 glut?:** yes — SRAM ASPs are decoupled from DRAM contract prices; long-lifecycle buyers pay for availability through cycles.

**Fatal-flaw candidate:** The incumbent (Infineon, supplied from the same Fab 25 under contract) and Renesas can match or undercut on any socket. The standalone SRAM market is small and shrinking, and qualification takes 2-3 years before revenue.

*Possible?* yes — mature technology at a willing U.S. foundry · *Profitable?* marginal — real margins per part, but a small market with a strong incumbent at the same fab · *Doable by this founder?* no — T2 hardware team required

*Business-model lenses:* fabless->foundry; defense-first; module/component maker

### C-37 — Compute-in-SRAM vector-search appliance on GSI Gemini APU

*Sub-branch:* SRAM-at-scale: compute-in-SRAM as a DRAM-bandwidth substitute · *Materials sense:* none

**What it is:** An on-prem retrieval and vector-search appliance plus software (FAISS/Milvus-compatible API, index build pipeline, monitoring) built on GSI Technology's Gemini APU PCIe cards. The APU does associative processing inside SRAM bit-lines (Gemini-I on TSMC 28nm, Gemini-II on 16nm) [UNVERIFIED-training]. It is sold to air-gapped defense/IC RAG and SIEM buyers as hardware plus an annual software subscription.

**Why it could work:** The APU runs nearest-neighbour search inside SRAM, so a billion-vector index needs far less DRAM bandwidth and capacity per query than on CPUs/GPUs. With DRAM/HBM at 2-3x 2025 prices, DRAM GB per QPS matters. A 2025 Cornell study reported GPU-class retrieval at much lower energy [UNVERIFIED-training]. GSI is small (~$20M revenue) and needs software channel partners, and the integration is mostly software.

**Evidence:** TRL 7 · Rule 1: SUPPORTED
  - [D-Matrix AI chip promises efficient transformer processing](https://www.forbes.com/sites/karlfreund/2022/06/21/d-matrix-ai-chip-promises-efficient-transformer-processing/) — news, 2022-06. URL + excerpt seen in basicmi/AI-Chip README (not opened): digital in-memory (SRAM) compute + chiplets for datacenter inference
  - [Startup Runs AI in Novel SRAM](https://www.eetimes.com/document.asp?doc_id=1334947) — news, 2019. URL + excerpt seen in basicmi/AI-Chip README (not opened): another compute-in-SRAM startup (Areanna AI)
  - [GSI Technology Gemini APU (Sunnyvale CA; FY2025 revenue ~$20M; Cornell/MICRO-2025 energy-efficiency study of APU retrieval)]() — company, 2025. [UNVERIFIED-training] citation from A3 training data (<= mid-2026). No URL could be opened or seen this session: the shared WebSearch budget was exhausted and web hosts returned proxy 403. Verify agent: add a URL or downgrade. Status as of 2026-11-01 not verified.

**Capital tier:** T1 | **Time to first revenue:** 12-18 months (eval cards, one defense/enterprise pilot) | **Gross margin estimate:** 30-50% blended (hardware pass-through + software subscription)

**US manufacturability:** APU silicon is TSMC (Taiwan) and boards are GSI-sourced. Integration and software are in the U.S., so the product is U.S.-assembled, not U.S.-made.

**Who is already doing this:** GSI Technology itself (Leda boards, software); GPU/CPU vector search (NVIDIA cuVS, Milvus/Zilliz, Pinecone, Weaviate); other compute-in-SRAM startups (d-Matrix for LLMs, Areanna historically).

**Wins on which axis, for which buyer:** Watts per query and DRAM GB per QPS for large-scale vector search. — for Air-gapped defense/intelligence RAG deployments; on-prem enterprise search with power or DRAM constraints.

**Survives a 2029 glut?:** partially — The DRAM-savings pitch weakens when DDR5 falls to ~$10/GB, but the energy and air-gap pitches remain.

**Fatal-flaw candidate:** Single-supplier dependency on a small, loss-making vendor whose roadmap or survival is uncertain [UNVERIFIED-training], while GPU/CPU vector search improves every year and DRAM gets cheap in the glut.

*Possible?* yes — the APU ships · *Profitable?* marginal — thin hardware margin, vendor risk · *Doable by this founder?* marginal — software-led but needs a hardware partner that stays alive

*Business-model lenses:* module/appliance maker (VAR); SaaS (software subscription); defense-first

### C-38 — Memory-only wafer-scale SRAM ('Cerebras for RAM')

*Sub-branch:* Wafer-scale SRAM as a RAM product · *Materials sense:* c-capital

**What it is:** A whole 300mm 28nm wafer of redundant, stitched SRAM (~27 GB) packaged with power delivery and cooling as an ultra-low-latency memory appliance, attached to hosts through edge SerDes/CXL links. Wafers would come from a 28nm-class foundry (GF Malta 12/14nm is the U.S. option).

**Why it could work:** Cerebras proved wafer-scale yield through redundancy (WSE-2 '100% yield' on 7nm; WSE-3 holds 44 GB SRAM on 46,225 mm2 [UNVERIFIED-training]). 28nm wafers are cheap, and on-wafer bandwidth is enormous.

**Evidence:** TRL 4 · Rule 1: SUPPORTED
  - [Cerebras Unveils Wafer Scale Engine Two (WSE2): 2.6 Trillion Transistors, 100% Yield](https://www.anandtech.com/show/16626/cerebras-unveils-wafer-scale-engine-two-wse2-26-trillion-transistors-100-yield) — news, 2021-04. URL + excerpt seen in basicmi/AI-Chip README (not opened): wafer-scale engine on TSMC 7nm (WSE1 on 16nm); redundancy gives '100% yield'
  - [Cerebras Unveils Andromeda, a 13.5 Million Core AI Supercomputer](https://www.cerebras.net/press-release/cerebras-unveils-andromeda-a-13.5-million-core-ai-supercomputer-that-delivers-near-perfect-linear-scaling-for-large-language-models) — company, 2022-11. URL seen in basicmi/AI-Chip README (not opened): wafer-scale systems clustered for LLM work
  - [The Cerebras CS-1 computes deep learning AI problems by being bigger](https://techcrunch.com/2019/11/19/the-cerebras-cs-1-computes-deep-learning-ai-problems-by-being-bigger-bigger-and-bigger-than-any-other-chip/) — news, 2019-11. URL + excerpt seen in basicmi/AI-Chip README (not opened): CS-1 launch; first customer Argonne National Laboratory

**Capital tier:** T3 | **Time to first revenue:** ~48 months | **Gross margin estimate:** negative

**US manufacturability:** GF Fab 8 Malta NY for wafers. Wafer-scale packaging capability in the U.S. is unclear [UNVERIFIED-training].

**Who is already doing this:** Cerebras (compute + SRAM on one wafer, TSMC). Nobody sells memory-only wafers.

**Wins on which axis, for which buyer:** None for a host: on-wafer bandwidth cannot leave the wafer through an ~860 mm perimeter. — for None identified. Latency-critical buyers buy Cerebras/Groq compute instead.

**Survives a 2029 glut?:** no — ~$111/GB in silicon alone and ~$1,000/GB packaged (C-38), against $10-27/GB DRAM.

**Fatal-flaw candidate:** Cerebras's economics come from co-locating compute with SRAM. A memory-only wafer exports its bandwidth through edge I/O, so it is DRAM at 40-100x the price with no latency advantage visible to the host.

*Possible?* yes — engineering-feasible · *Profitable?* no · *Doable by this founder?* no

*Business-model lenses:* module/appliance maker — fails

### C-39 — U.S.-fabbed SRAM-only LLM inference accelerator (Groq pattern)

*Sub-branch:* SRAM-instead-of-DRAM for inference · *Materials sense:* c-capital

**What it is:** A fabless startup building a deterministic SRAM-only LLM-decode accelerator (the Groq LPU pattern) on GlobalFoundries 12LP+ at Fab 8 Malta, NY. It would be sold as U.S.-made inference racks or cloud tokens, replacing HBM/DRAM with on-chip SRAM for low-latency decode.

**Why it could work:** Groq ran Llama-2 70B at 240 tokens/s/user on first-gen 14nm silicon (EE Times 2023). Groq v1 was fabbed at GF 14nm, Malta NY [UNVERIFIED-training]. Big money keeps following SRAM-centric inference: NVIDIA's reported ~$20B license-and-hire deal with Groq (Dec 2025) [UNVERIFIED-training], d-Matrix and Cerebras raises. HBM is supply-constrained.

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [Groq Demonstrates Fast LLMs on 4-Year-Old Silicon](https://www.eetimes.com/groq-demos-fast-llms-on-4-year-old-silicon/) — news, 2023-09. URL + excerpt seen in basicmi/AI-Chip README (not opened): first-gen SRAM-only LPU ran Llama-2 70B at 240 tokens/s/user
  - [AI Chip Startup Groq Raises $300 Million](https://www.forbes.com/sites/amyfeldman/2021/04/14/ai-chip-startup-groq-founded-by-ex-googlers-raises-300-million-to-power-autonomous-vehicles-and-data-centers/) — news, 2021-04. URL + excerpt seen in basicmi/AI-Chip README (not opened): Groq raised $300M in 2021 (T3 capital intensity)
  - [D-Matrix AI chip promises efficient transformer processing](https://www.forbes.com/sites/karlfreund/2022/06/21/d-matrix-ai-chip-promises-efficient-transformer-processing/) — news, 2022-06. URL + excerpt seen in basicmi/AI-Chip README (not opened): digital in-memory (SRAM) compute + chiplets for datacenter inference
  - [AI chip startup d-Matrix raises $110 million with backing from Microsoft](https://www.reuters.com/technology/ai-chip-startup-d-matrix-raises-110-mln-with-backing-microsoft-2023-09-06/) — news, 2023-09. URL + excerpt seen in basicmi/AI-Chip README (not opened): $110M raise incl. Microsoft
  - [Graphcore Supercharges IPU with Wafer-on-Wafer](https://www.eetimes.com/graphcore-supercharges-ipu-with-wafer-on-wafer/) — news, 2022-03. URL + excerpt seen in basicmi/AI-Chip README (not opened): SRAM-heavy IPU (no HBM) using 3D wafer-on-wafer
  - [Untether AI nabs $125M for AI acceleration chips](https://venturebeat.com/2021/07/20/untether-ai-nabs-125m-for-ai-acceleration-chips/) — news, 2021-07. URL + excerpt seen in basicmi/AI-Chip README (not opened): at-memory (SRAM) inference startup raised $125M

**Capital tier:** T3 | **Time to first revenue:** 36-48 months | **Gross margin estimate:** 40-60% if it wins

**US manufacturability:** GlobalFoundries Fab 8 Malta NY (12LP+/14nm), the same U.S. fab class Groq v1 used [UNVERIFIED-training]. U.S. OSAT assembly.

**Who is already doing this:** Groq (with NVIDIA license), Cerebras, d-Matrix, SambaNova, Etched, MatX, Positron. Graphcore (now SoftBank) and Untether AI (team absorbed by AMD, 2025) [UNVERIFIED-training] show the attrition.

**Wins on which axis, for which buyer:** Tokens/s/user (decode latency) and energy per bit moved (no off-chip DRAM I/O). — for Latency-sensitive inference (agents, voice, real-time trading) and sovereign/U.S.-made AI clouds.

**Survives a 2029 glut?:** partially — The latency premium persists, but cheap HBM/DDR in a glut erodes the 'no DRAM needed' cost story, and SRAM is ~$350/GB at chip level vs ~$12/GB HBM3E (C-39).

**Fatal-flaw candidate:** Upper-T3 capital (incumbents raised $0.3-1B+ each) against four or more well-funded incumbents, with NVIDIA now holding Groq's technology license. A 70B 8-bit model needs ~300+ SRAM dies.

*Possible?* yes — shipping at incumbents · *Profitable?* marginal — only for the category winner · *Doable by this founder?* no

*Business-model lenses:* fabless->foundry; appliance; cloud service

### C-40 — Nantero NRAM (carbon-nanotube) license and U.S. second source

*Sub-branch:* Exotic: carbon-nanotube memory · *Materials sense:* mixed:a+b

**What it is:** License Nantero's (Woburn, MA) carbon-nanotube NRAM 1T1R BEOL module and run it at SkyWater Bloomington MN (200mm, already hosting third-party BEOL memory). The first product would be rad-hard, high-temperature non-volatile RAM for space and defense; the long-term pitch is DDR-class persistent memory.

**Why it could work:** The CNT fabric is spin-coated at room temperature, which is CMOS-compatible and uses cheap tooling (materials sense a+b). Nantero claims ns switching, high endurance, multi-year retention at high temperature and radiation tolerance [UNVERIFIED-training]. A hypothetical 1T1R at 28nm computes to ~$31/GB (C-40), cheap for rad-hard NVM.

**Evidence:** TRL 5 · Rule 1: SUPPORTED
  - [Weebit Nano ReRAM IP achieves high-temperature qualification in SkyWater S130](https://www.skywatertechnology.com/weebit-nano-reram-ip-achieves-high-temperature-qualification-in-skywater-s130-process/) — company, 2023-11. SkyWater's S130 PDK hosts third-party memory IP — precedent for licensing a memory macro into a U.S. 130nm foundry (CROSS-REFERENCE: seen in another agent's search results, not opened by A3)
  - [Frontgrade case study: Everspin Toggle MRAM for space](https://www.frontgrade.com/news/new-case-study-touts-everspins-toggle-mram-highly-reliable-memory-technology-space) — company, 2020. Qualified hi-rel/space memory reaches primes through channels like Frontgrade — the buyer channel for U.S.-made long-lifecycle memory (CROSS-REFERENCE: seen in another agent's search results, not opened by A3)
  - [Nantero NRAM: Fujitsu Semiconductor + Mie Fujitsu licenses (2016, 55nm target product ~2018-19, not known to have shipped); Nantero IEDM/company disclosures]() — company, 2016-2020. [UNVERIFIED-training] citation from A3 training data (<= mid-2026). No URL could be opened or seen this session: the shared WebSearch budget was exhausted and web hosts returned proxy 403. Verify agent: add a URL or downgrade. Status of Nantero in 2026 unknown.

**Capital tier:** T2 | **Time to first revenue:** ~48 months (module transfer, rad testing, QML-style qualification) | **Gross margin estimate:** 40-60% in a rad-hard niche if it worked

**US manufacturability:** SkyWater Bloomington MN (S130 BEOL) or Fab 25 Austin. The licensor is in Massachusetts (East Coast).

**Who is already doing this:** Nantero (licensor; activity in 2024-2026 unverified). Fujitsu/Mie Fujitsu (licensees; Mie fab now USJC) [UNVERIFIED-training]. Rad-hard NVM incumbents: Everspin Toggle MRAM via Frontgrade, Infineon rad-hard F-RAM.

**Wins on which axis, for which buyer:** Non-volatility plus radiation and temperature tolerance (space/defense). Not $/GB vs DRAM. — for Space primes and rad-hard component distributors (Frontgrade-type channel); downhole/high-temperature industrial.

**Survives a 2029 glut?:** partially — The rad-hard niche is independent of DRAM prices, but the 'DRAM replacement' story dies at $10/GB DDR5.

**Fatal-flaw candidate:** 20+ years and >$100M [UNVERIFIED-training] without a known volume product; the Fujitsu-licensed product apparently never shipped. In rad-hard it must displace qualified Toggle MRAM and F-RAM incumbents.

*Possible?* marginal — demonstrated by licensees, never productized · *Profitable?* no — no evidence of a cost or performance win that incumbents can't match · *Doable by this founder?* no

*Business-model lenses:* university/lab-style patent license (from Nantero); defense-first; fabless->foundry

### C-41 — 2D-material (MoS2/WSe2) gain-cell DRAM or 2D flash

*Sub-branch:* Exotic: 2D semiconductor memory · *Materials sense:* a-material

**What it is:** BEOL 2T0C gain cells or 2D-channel flash built from wafer-scale MoS2/WSe2, under a university license (Penn State 2D Crystal Consortium, MIT, or the Fudan 'PoX' line of work). Pilot fabrication would be at the Penn State 2DCC user facility or NY CREATES Albany 300mm.

**Why it could work:** Atomically thin, wide-gap channels give ultra-low off-current (long retention, like IGZO) with higher mobility than IGZO. Lab papers report sub-ns 2D flash programming (Fudan PoX, ~400 ps, Nature 2025) and 2D logic circuits of a few thousand transistors [UNVERIFIED-training].

**Evidence:** TRL 2 · Rule 1: UNSUPPORTED
  - [NY CREATES + Fraunhofer IPMS JDA on memory devices at 300mm (Albany NY)](https://nachrichten.idw-online.de/2025/05/16/ny-creates-and-fraunhofer-ipms-announce-joint-development-agreement-to-advance-memory-devices-at-300mm-wafer-scale) — news, 2025-05. Venue evidence only: Albany NY 300mm hosts external memory-device JDAs (HfO2 FE), a possible pilot site; does NOT show 2D-memory mechanism (CROSS-REFERENCE: seen in another agent's search results, not opened by A3)
  - [2D-material memory literature: Fudan quasi-non-volatile 2D memory (Nature Nanotech 2018), Fudan PoX 400-ps 2D flash (Nature 2025), Penn State 2D CMOS computer (Nature 2025)]() — peer-reviewed, 2018-2025. [UNVERIFIED-training] citation from A3 training data (<= mid-2026). No URL could be opened or seen this session: the shared WebSearch budget was exhausted and web hosts returned proxy 403. Verify agent: add a URL or downgrade. No array-scale (>1 Mb) 2D memory known to A3.

**Capital tier:** T3 | **Time to first revenue:** >8 years | **Gross margin estimate:** not modelable

**US manufacturability:** No U.S. production line; research only (Penn State 2DCC, NY CREATES Albany).

**Who is already doing this:** Academic groups (Fudan, Penn State, MIT, Stanford); TSMC/imec/Intel 2D-channel logic research [UNVERIFIED-training].

**Wins on which axis, for which buyer:** Retention per area (speculative) — not demonstrated at array scale. — for None until TRL 6+.

**Survives a 2029 glut?:** no — Too far from product to matter. A product landing in the 2030s competes with mature IGZO 2T0C (A1) and cheap DRAM.

**Fatal-flaw candidate:** No defect-controlled, wafer-scale 2D growth at BEOL-compatible temperature, and no array-scale demonstration. Contact resistance and variability are unsolved. IGZO (C-01..04) already delivers the low-leakage benefit on 300mm today.

*Possible?* no (not within the venture horizon) — lab devices only; UNSUPPORTED at array scale · *Profitable?* no · *Doable by this founder?* no

*Business-model lenses:* university/lab patent license — premature

### C-42 — Printed organic ferroelectric memory (Thinfilm post-mortem)

*Sub-branch:* Exotic: organic/polymer and printed memory · *Materials sense:* mixed:a+b

**What it is:** Roll-to-roll printed P(VDF-TrFE) ferroelectric-polymer passive-matrix memory, the Thinfilm Electronics lineage, built on a U.S. printed-electronics pilot line (e.g. NextFlex, San Jose CA) [UNVERIFIED-training]. Product: printed memory labels, pitched here as 'printable RAM'.

**Why it could work:** No lithography and no vacuum: gravure or inkjet printing of a ferroelectric polymer between printed electrodes costs cents per label. Thinfilm did ship 20-bit printed memory labels (~2010s) [UNVERIFIED-training].

**Evidence:** TRL 2 · Rule 1: UNSUPPORTED
  - [Thin Film Electronics ASA printed ferroelectric polymer memory (20-bit labels); pivot to NFC (Kovio fab, 2014), then to microbatteries as Ensurge Micropower (2021); insolvency ~2024]() — company, 2009-2024. [UNVERIFIED-training] citation from A3 training data (<= mid-2026). No URL could be opened or seen this session: the shared WebSearch budget was exhausted and web hosts returned proxy 403. Verify agent: add a URL or downgrade.

**Capital tier:** T2 | **Time to first revenue:** never as RAM | **Gross margin estimate:** n/a

**US manufacturability:** NextFlex pilot lines (San Jose CA) or university printed-electronics labs. The former Thinfilm/Kovio San Jose line is closed [UNVERIFIED-training].

**Who is already doing this:** Nobody for RAM. Thinfilm exited memory.

**Wins on which axis, for which buyer:** Cost per label for a few bits (anti-counterfeit tags) — not any RAM axis. — for None for RAM; brand-protection labels at most.

**Survives a 2029 glut?:** no — About $4e7/GB by label cost (C-42), ~7 orders of magnitude above DRAM, with ms latency and 1e3-1e5 endurance.

**Fatal-flaw candidate:** Density, latency and endurance are each 6-10 orders of magnitude from RAM. The company that pioneered it abandoned memory twice and later failed [UNVERIFIED-training].

*Possible?* no as RAM (UNSUPPORTED for any RAM role; 20-bit labels did ship, no URL retrievable this session) · *Profitable?* no · *Doable by this founder?* no

*Business-model lenses:* none viable

### C-43 — Cryo-CMOS gain-cell eDRAM IP for quantum-computer control

*Sub-branch:* Exotic/cryogenic memory (vs superconducting memory) · *Materials sense:* b-process

**What it is:** A memory-IP and test-chip business offering Si gain-cell eDRAM macros characterized at 4 K and 77 K for cryo-CMOS qubit-controller ASICs, fabbed on GF 12LP+ (Malta NY) or SkyWater 90nm FD-SOI. Revenue is NRE plus licenses from quantum hardware teams and national-lab programs.

**Why it could work:** At cryogenic temperatures subthreshold leakage collapses, so Si gain-cell retention rises from microseconds to seconds or more [UNVERIFIED-training]. That makes refresh nearly free while keeping ~2x SRAM density and very low static power. This matters because the 4 K stage has only ~1 W of cooling budget. Superconducting memories (SFQ/JMRAM) remain far less dense.

**Evidence:** TRL 3 · Rule 1: SUPPORTED
  - [Disrupting the DRAM roadmap with capacitor-less IGZO DRAM technology](https://www.imec-int.com/en/articles/disrupting-dram-roadmap-capacitor-less-igzo-dram-technology) — industry, 2023. 2T0C gain-cell concept: charge stored on the read-transistor gate capacitance — the same topology as Si gain cells (CROSS-REFERENCE: seen in another agent's search results, not opened by A3)
  - [OpenRAM open-source SRAM compiler (GitHub README; v1.2.50 commit 2026-10-27)](https://github.com/VLSIDA/OpenRAM) — industry, 2026-10. Opened via git: BSD-3 SRAM compiler, generates GDS/LEF/Liberty/SPICE for sky130 (SkyWater) and gf180mcu; actively maintained (last commit 2026-10-27)
  - [Cryogenic CMOS eDRAM/gain-cell characterization papers (2020-2024) and Intel Horse Ridge cryo-CMOS controller]() — conference, 2020-2024. [UNVERIFIED-training] citation from A3 training data (<= mid-2026). No URL could be opened or seen this session: the shared WebSearch budget was exhausted and web hosts returned proxy 403. Verify agent: add a URL or downgrade.

**Capital tier:** T1 | **Time to first revenue:** 24-36 months (NRE/research contracts) | **Gross margin estimate:** 60-80% (IP/NRE)

**US manufacturability:** GF Fab 8 Malta NY (12LP+) or SkyWater Bloomington MN (90nm FD-SOI). Cryo test needs a dilution refrigerator, rented from a university or national lab.

**Who is already doing this:** Intel (Horse Ridge), IBM Quantum, Google Quantum AI and imec do in-house cryo-CMOS; SEEQC (Elmsford NY) does superconducting SFQ control; academic cryo gain-cell groups [UNVERIFIED-training].

**Wins on which axis, for which buyer:** Static power at the 4 K stage and memory density for cryo control electronics. — for Quantum computing hardware teams (IBM Quantum NY, Google Quantum AI), DARPA/IARPA quantum programs.

**Survives a 2029 glut?:** yes — Unrelated to DRAM pricing.

**Fatal-flaw candidate:** The market is a few dozen teams, most of which design memory in-house. Quantum roadmaps may keep control at room temperature for years. It needs a cryo test lab and a circuit designer.

*Possible?* yes — physics favorable · *Profitable?* marginal — tiny market · *Doable by this founder?* no

*Business-model lenses:* IP licensing; defense/government NRE; university/lab patent license

## B. Architecture & systems (14 cards)

### C-44 — DDR4 Second-Life CXL Expander

*Sub-branch:* CXL memory expansion / DIMM reuse (Microsoft-Meta style DDR4 recycling) · *Materials sense:* mixed:b+c

**What it is:** A PCIe Gen5 x16 CXL 2.0 Type-3 add-in card or 1U 'JBOM' holding 8-12 decommissioned DDR4-3200 RDIMMs behind a merchant DDR4-capable CXL controller (Marvell Structera X 2404-class or Microchip SMC 2000-class). A U.S. EMS (e.g. Sanmina) assembles it, and it ships with burn-in and qualification to operators moving to DDR5-only Xeon 6 / EPYC 9005 servers. The process 'materials' are DRAM that is already fabbed and paid for, and the capital is DIMMs that are already depreciated.

**Why it could work:** Hyperscalers reuse DDR4 behind CXL because reuse beats buying new DDR5. B's model gives the hyperscaler a +$2.0/GB advantage at the 2023 trough and +$13/GB in 4Q26, with the card at ~$0.49/GB and DDR4 dumped at ~50% of spot. Single-host Type-3 expansion is stabilizing in mainline Linux ([2]). Tiering is upstream (weighted interleave v6.9, DAMON migration v6.11). The added ~70-100 ns latency [UNVERIFIED-T, Pond] suits VM-density and in-memory DB capacity tiers.

**Evidence:** TRL 7 · Rule 1: SUPPORTED
  - [Pond: CXL-Based Memory Pooling Systems for Cloud Platforms (ASPLOS '23) artifact repo](https://github.com/vtess/Pond) — conference, 2023-03. Opened. Microsoft Azure/Virginia Tech CXL pooling paper. The repo holds the CXL-emulation scripts, and the paper preprint is linked at huaicheng.github.io/p/asplos23-pond.pdf (not opened).
  - [Linux CXL Subsystem Maturity Map (mainline, HEAD 2026-10-31)](https://github.com/torvalds/linux/blob/master/Documentation/driver-api/cxl/maturity-map.rst) — industry, 2026-10. Opened. Single-host Type-3 enumeration/HDM decoders are [2] stabilizing. Dynamic Capacity Devices, multi-host sharing and fabrics/G-FAM are [0] known gaps. PMEM GPF/dirty shutdown is [3] mature.
  - [SK hynix HMSDK README](https://github.com/skhynix/hmsdk) — company, 2025-11. Opened. HMSDK v4.0 (2025-11-03). CXL weighted-interleave landed in upstream Linux v6.9 and DAMON tier migration in v6.11. CXL tiering software is free and upstream.
  - [RAM market update (DRAMeXchange snapshot 2026-08-31)](https://www.buysellram.com/blog/ram-market-update/) — news, 2026-08-31. CROSS-REF (p1-backend.jsonl snippet). DDR4 8Gb avg $44.37 vs DDR5 16Gb avg $53.92: DDR4 is dearer per GB than DDR5.
  - [TrendForce DRAM spot price page](https://www.trendforce.com/price_dram.html) — industry, 2026-08-03. CROSS-REF (p1-backend.jsonl snippet). DDR4 8Gb spot avg $21.00 on 2026-08-03.
  - [Barclays via TechNews: DDR4 pricier than DDR5 in some channels](https://finance.technews.tw/2026/10/13/the-shortage-of-memory-chips-may-continue-for-another-two-years/) — news, 2026-10-13. CROSS-REF (p1-market.jsonl snippet). DDR4 increases outpace DDR5, and the two are price-inverted in some channels.
  - [KED Global: DDR4 8Gb bottomed at $1.30](https://www.kedglobal.com/korean-chipmakers/newsView/ked202310040013) — news, 2023-10-04. CROSS-REF (p1-market.jsonl snippet). 2023-trough DDR4 value anchor.

**Capital tier:** T2 | **Time to first revenue:** 18-30 months: board design + controller vendor access + qualification at one tier-2 cloud | **Gross margin estimate:** 15-30% (card without DRAM)

**US manufacturability:** Board assembly/test at any U.S. EMS (Sanmina, Kimball, SMTC). The controller silicon is TSMC (Taiwan). DIMMs are recovered from U.S. data centers. Only assembly and recovery are U.S.

**Who is already doing this:** Marvell (Structera X: DDR4 support, inline LZ4) [UNVERIFIED-T]; Astera Labs (Leo; Azure CXL instances) [UNVERIFIED-T]; Montage (MXC); Microchip (SMC 2000); SMART Modular/Penguin Solutions (4- and 8-DIMM CXL AICs) [UNVERIFIED-T]; Microsoft and Meta in-house DDR4 reuse programs [UNVERIFIED-T]

**Wins on which axis, for which buyer:** $/GB of added capacity from already-owned DIMMs; lifecycle length/Scope-3; supply security when DDR5 allocation is refused — for Tier-2/neocloud and large-enterprise operators with >=10k retired DDR4 RDIMMs and DDR5-only new servers (VM density, in-memory DB capacity tier)

**Survives a 2029 glut?:** no — B's model makes reuse lose for a small vendor in every scenario: -$0.34/GB (2023 trough), -$1.34/GB (4Q26, DDR4 resale ~$25/GB ≈ new DDR5), -$3.94/GB (glut, DDR5 $10.4 vs DDR4 sticky ~$12). The only owners who come out ahead (hyperscalers) build their own.

**Fatal-flaw candidate:** At small-vendor volume the card costs ~$2.3/GB. The owner's DDR4 is worth ~$21-44/GB at chip spot in Aug 2026, and DDR4 is dearer than DDR5 in some channels, so 'sell the DDR4, buy DDR5' beats reuse. The arbitrage exists only at hyperscaler scale, where buyers go direct to Marvell/Astera.

*Possible?* yes: deployed at hyperscalers with merchant controllers · *Profitable?* no: computed negative unit advantage for a small vendor in trough, shortage and glut · *Doable by this founder?* no: hardware/firmware team and controller allocation required

*Business-model lenses:* module/appliance; recert/brokerage (the profitable variant is reselling the DDR4: branch C)

### C-45 — KV Pool Node (shared DRAM+CXL KV-cache appliance)

*Sub-branch:* LLM inference KV-cache tiering - DRAM/CXL tier · *Materials sense:* c-capital

**What it is:** A 2U EPYC 9005 / Xeon 6 server (Supermicro or Dell OEM chassis) holding 3-6 TB of DDR5 plus E3.S CXL memory modules (Samsung CMM-D, Micron CZ122 or SK hynix CMM-DDR5), with 2x400G RDMA NICs. It ships with Mooncake Store / LMCache MP preconfigured to allocate KV on the CXL tier (/dev/dax). It is sold as a rack-shared 'KV memory node' that pools prefix and agent-session caches across GPU servers running vLLM/SGLang/Dynamo.

**Why it could work:** KV is large: Llama-3.1-70B is 320 KiB/token at BF16 (40 GiB per 128k context); DeepSeek-V3 MLA is 68.6 KiB/token. Reloading a 128k context (20 GiB FP8) over 400G RDMA takes ~0.5 s, against ~41 s to recompute on one H100. Holding KV in DDR5 pays if a prefix is reused at least once every ~1.35 h at 4Q26 prices (~3.4 h in the glut). Mooncake reports 75% more requests within SLO at Kimi. vLLM requires the CPU tier as the staging tier, and LMCache/Mooncake already speak CXL /dev/dax.

**Evidence:** TRL 8 · Rule 1: SUPPORTED
  - [Mooncake README + Mooncake Store deployment guide (Kimi serving platform)](https://github.com/kvcache-ai/Mooncake) — company, 2026-11. Opened. KV-cache-centric disaggregation lets Kimi handle 75% more requests within SLO. Store has CXL-aware allocation (--enable_cxl, /dev/dax, --allocation_strategy=cxl). Integrated into vLLM (May 2026) and TensorRT-LLM (Oct 2026).
  - [Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving (FAST '25)](https://www.usenix.org/system/files/fast25-qin.pdf) — conference, 2025-02. Peer-reviewed production KV-disaggregation design (link seen in the Mooncake README; PDF not opened).
  - [LMCache Device-DAX backend (CXL-attached memory as KV arena)](https://github.com/LMCache/LMCache/blob/dev/docs/source/kv_cache/storage_backends/dax.rst) — industry, 2026. Opened. LMCache mmaps /dev/dax (PMEM or CXL memory) as a KV-cache arena, and several servers can share one CXL device by disjoint ranges.
  - [vLLM KV Offloading Usage Guide](https://github.com/vllm-project/vllm/blob/main/docs/features/kv_offloading_usage.md) — industry, 2026-11. Opened. CPU host memory is the primary KV offload tier, and secondary tiers are staged through it. Host DRAM capacity is mandatory for KV tiering.
  - [NVIDIA Dynamo KVBM README + KV-cache offloading docs](https://github.com/ai-dynamo/dynamo) — company, 2026-11. Opened. GPU<->CPU<->Disk<->Remote KV tiering with GDS/NIXL transfers. LMCache, FlexKV and HiCache are interchangeable backends. Host/disk KV tiering is free open-source software.
  - [Meta llama-models sku_list.py](https://github.com/meta-llama/llama-models) — company, 2025-10. Opened. Llama-3.1 70B has 80 layers and 8 KV heads with head_dim 128, which gives 320 KiB/token KV at BF16 (40 GiB at 128k context).
  - [DeepSeek-V3 config_671B.json](https://github.com/deepseek-ai/DeepSeek-V3) — company, 2025-08. Opened. MLA latent KV (kv_lora_rank 512 + rope 64, 61 layers) is about 68.6 KiB/token at BF16, against 320 KiB/token for Llama-3.1-70B (computed by B).
  - [Counterpoint via EE Times Asia: 64GB RDIMM $450 to >$900](https://www.eetasia.com/memory-prices-surging-by-90-from-4q-2025/) — news, 2026-01. CROSS-REF (p1-market.jsonl snippet). Server RDIMM contract doubled 4Q25 to 1Q26.

**Capital tier:** T1 | **Time to first revenue:** 9-15 months: one demo node, then build-to-order to 2-3 neocloud/enterprise inference teams | **Gross margin estimate:** 12-25% hardware; 60%+ on an attached support/observability subscription

**US manufacturability:** Integration/burn-in on a U.S. bench (East Coast) or through Supermicro San Jose. CPUs, NICs and most DDR5 are imported. Micron Idaho DDR5 is not before mid-2027.

**Who is already doing this:** NVIDIA (Dynamo KVBM; Inference Context Memory Storage on BlueField-4 [UNVERIFIED-T]); WEKA Augmented Memory Grid (NVIDIA partnership Nov 2025); VAST Data; Pliops; Hammerspace Tier 0; Penguin Solutions (CXL KV server) [UNVERIFIED-T]; Enfabrica EMFASYS (now NVIDIA) [UNVERIFIED-T]; Moonshot/Mooncake in-house; Tensormesh (LMCache commercial)

**Wins on which axis, for which buyer:** $/GB-month of shared hot-KV capacity against GPU HBM (~$180-250/GB effective) and TTFT on cache hits — for Neocloud inference providers and enterprise private-inference teams with long system prompts, RAG and multi-turn agent sessions

**Survives a 2029 glut?:** partially — A 60% DRAM drop cuts the node BOM and stretches the DRAM break-even reuse interval from 1.35 h to 3.4 h. It also lets every OEM sell the same box, and flash tiers (break-even ~78 h) keep undercutting DRAM for warm KV.

**Fatal-flaw candidate:** No moat: a commodity server plus open-source software (Mooncake/LMCache) that Dell/Supermicro/NVIDIA reference designs replicate. A 4 TB node ties up ~$80-130k of DRAM at 4Q26 prices for a reseller-grade margin, and flash KV tiers take the warm data.

*Possible?* yes: production at Moonshot; all parts off-the-shelf · *Profitable?* marginal: VAR-grade hardware margin unless a subscription attaches · *Doable by this founder?* marginal: needs customer prepayment or financing for DRAM inventory

*Business-model lenses:* module/appliance; SaaS (support + KV observability subscription)

### C-46 — Flash KV Accelerator (U.S. Pliops-style NVMe KV engine)

*Sub-branch:* LLM inference KV-cache tiering - flash tier with hardware KV engine · *Materials sense:* a-material

**What it is:** A PCIe Gen5 card with an FPGA (AMD Versal / Altera Agilex) key-value engine fronting 8-24 Gen5 TLC NVMe SSDs (Micron 9550, Solidigm, Kioxia). It exposes a KV-block API to vLLM/Dynamo through a NIXL plugin and stores KV on NAND instead of DRAM: a U.S. competitor to Pliops XDP LightningAI.

**Why it could work:** The material swap is NAND for DRAM. Enterprise NVMe at ~$0.30-0.60/GB holds 1M tokens of Llama-70B FP8 KV (164 GB) for ~$0.003/h, so caching pays if reused once per ~78 h, against ~1.35 h for DDR5. One Gen5 SSD reloads a 128k context in ~1.8 s vs ~41 s recompute. NAND stopped rising in Oct 2026, with surplus forecast for 2H27.

**Evidence:** TRL 8 · Rule 1: SUPPORTED
  - [NVIDIA Dynamo KVBM README + KV-cache offloading docs](https://github.com/ai-dynamo/dynamo) — company, 2026-11. Opened. GPU<->CPU<->Disk<->Remote KV tiering with GDS/NIXL transfers. LMCache, FlexKV and HiCache are interchangeable backends. Host/disk KV tiering is free open-source software.
  - [WEKA partners with NVIDIA on KV cache storage for Dynamo (SC25)](https://siliconangle.com/2025/11/20/nvidia-weka-kv-cache-solution-ai-inferencing-sc25/) — news, 2025-11-20. Flash-based KV tier partnership between WEKA and NVIDIA (headline seen in the Dynamo README; body not opened).
  - [LMCache README](https://github.com/LMCache/LMCache) — industry, 2026-11. Opened. Vendor-neutral KV layer that tiers to CPU RAM, SSD and remote stores. Joined the PyTorch Foundation, and Tensormesh launched, in Oct 2025. Integrated in NVIDIA Dynamo (Sep 2025).
  - [NAND flat after 21 months while DRAM hits record](https://tech-insider.org/dram-record-high-nand-flat-21-months-october-2026/) — news, 2026-10. CROSS-REF (p1-market.jsonl snippet). NAND contract stopped rising in Oct 2026.
  - [TrendForce 2026-07-30 press release](https://www.trendforce.com/presscenter/news/20260730-13158.html) — industry, 2026-07-30. CROSS-REF (p1-market.jsonl snippet). NAND turns to surplus in 2H27 while the DRAM gap widens.

**Capital tier:** T2 | **Time to first revenue:** 24-36 months: FPGA prototype, software integration, design-ins | **Gross margin estimate:** 40-60% if differentiated

**US manufacturability:** FPGA silicon from TSMC. Board assembly at a U.S. EMS. SSD NAND comes from Micron (Singapore), Kioxia/SanDisk (Japan) and Solidigm (China fab). Little U.S. content.

**Who is already doing this:** Pliops (XDP LightningAI) [UNVERIFIED-T]; WEKA (Augmented Memory Grid, NVIDIA partner); VAST Data; DDN; Hammerspace; NVIDIA ICMS/BlueField-4 [UNVERIFIED-T]; DeepSeek 3FS (open source; an LMCache backend); NVIDIA GDS + plain NVMe via Dynamo KVBM

**Wins on which axis, for which buyer:** $/GB-month of warm KV and TTFT on long-context reuse — for Inference providers and enterprise RAG/agent platforms with long shared prefixes

**Survives a 2029 glut?:** yes — The axis is flash vs recompute, not DRAM price. A NAND surplus in 2H27 lowers BOM further. A DRAM glut narrows the DRAM-vs-flash gap but does not close it (3.4 h vs 78 h break-even).

**Fatal-flaw candidate:** NVIDIA is building this tier itself (Dynamo KVBM + GDS + BlueField-4 storage), and software-only stacks on plain NVMe (3FS, LMCache, HiCache) capture most of the benefit without a special card. A late U.S. entrant faces Pliops/WEKA/VAST with a 2-3 year head start.

*Possible?* yes: shipping from several vendors · *Profitable?* marginal: crowded and being absorbed by NVIDIA reference stacks · *Doable by this founder?* no

*Business-model lenses:* fabless->foundry (FPGA then ASIC); module/appliance

### C-47 — Compressed CXL Expander (licensed inline compression IP)

*Sub-branch:* Hardware memory compression · *Materials sense:* b-process

**What it is:** An FPGA CXL 2.0 Type-3 card (Altera Agilex 7 R-tile or AMD Versal Premium) that runs licensed inline memory-compression IP (ZeroPoint Technologies, Gothenburg, or an LZ4-class core) in front of 256-512 GB DDR5. It exposes ~2x the physical capacity to Redis/Valkey/Memcached and VM hosts and would later tape out as an ASIC.

**Why it could work:** The IBM MXT lineage and ZeroPoint claim 2-4x on compressible data [UNVERIFIED-T]. At $20-32/GB, a 2x ratio on 512 GB is worth ~$10-16k of DRAM per card in 4Q26. Linux already proves the demand: zswap plus Intel IAA hardware DEFLATE.

**Evidence:** TRL 6 · Rule 1: SUPPORTED
  - [Linux IAA Compression Accelerator crypto driver doc](https://github.com/torvalds/linux/blob/master/Documentation/driver-api/crypto/iaa/iaa-crypto.rst) — industry, 2026-10. Opened. Intel In-Memory Analytics Accelerator hardware DEFLATE ('deflate-iaa') is selectable as the zswap compressor. Hardware memory compression already ships in Xeon CPUs.
  - [Linux zswap doc](https://github.com/torvalds/linux/blob/master/Documentation/admin-guide/mm/zswap.rst) — industry, 2026-10. Opened. OS-level compressed RAM cache is free in every Linux kernel.
  - [Linux CXL Subsystem Maturity Map (mainline, HEAD 2026-10-31)](https://github.com/torvalds/linux/blob/master/Documentation/driver-api/cxl/maturity-map.rst) — industry, 2026-10. Opened. Single-host Type-3 enumeration/HDM decoders are [2] stabilizing. Dynamic Capacity Devices, multi-host sharing and fabrics/G-FAM are [0] known gaps. PMEM GPF/dirty shutdown is [3] mature.

**Capital tier:** T2 | **Time to first revenue:** 24-36 months: IP license, FPGA card, qualification with one cache operator | **Gross margin estimate:** 40-55%

**US manufacturability:** FPGA from TSMC; board at a U.S. EMS; IP from Sweden. Little U.S. content beyond assembly.

**Who is already doing this:** ZeroPoint Technologies (CXL compression IP) [UNVERIFIED-T]; Marvell Structera (inline LZ4) [UNVERIFIED-T]; Intel IAA in Xeon + zswap (upstream); Meta TMO / Google zswap far-memory (software) [UNVERIFIED-T]; Rambus (CXL controller IP)

**Wins on which axis, for which buyer:** Effective $/GB (capacity multiplier) for compressible in-memory data — for In-memory cache operators (Redis/Valkey/Memcached fleets) and VM hosts with cold pages

**Survives a 2029 glut?:** no — At $8-13/GB, the DRAM a 2x ratio saves on 512 GB is ~$4-6k, which no longer covers a $3-8k FPGA card plus the latency penalty.

**Fatal-flaw candidate:** Compression is being absorbed for free into CPUs (Intel IAA + zswap, upstream) and merchant CXL controllers (inline LZ4). The hottest 'need more RAM' data, FP8/INT4 weights and KV, is near-incompressible, and FPGA BOM eats most of the saved DRAM value.

*Possible?* yes: demonstrated on FPGA and in merchant controllers · *Profitable?* no: squeezed between free CPU/controller compression and a glut · *Doable by this founder?* no

*Business-model lenses:* IP licensing (in-license); fabless->foundry; module/appliance

### C-48 — On-prem MoE Box (DRAM-instead-of-HBM inference appliance)

*Sub-branch:* HBM alternatives at system level: CPU-DRAM-resident MoE inference · *Materials sense:* mixed:a+c

**What it is:** A U.S.-integrated 2-socket AMD EPYC 9005 server with 768 GB-1.5 TB of 12-channel DDR5 RDIMM and 1-2 NVIDIA RTX PRO 6000 / RTX 5090-class GPUs. It runs KTransformers/SGLang CPU-GPU hybrid inference of open frontier MoE models (Kimi K2.5, DeepSeek-V4-Flash, GLM-5) and is sold with a support and model-update subscription to firms that cannot send data to cloud APIs.

**Why it could work:** Holding ~1 TB of weights in HBM takes ~$240k of H200-class GPUs. In DDR5 it is ~$20k at 4Q26 prices (~$8k in the glut). KTransformers documents Kimi-K2.5 on 2x4090 + >=600 GB RAM and DeepSeek-V4-Flash on one RTX 5090 + >=200 GB RAM. Decode roofline: ~23 tok/s per socket (614 GB/s, 32B active INT4), ~46 tok/s NUMA-aware. Modelled BOM ~$56k (4Q26) / ~$44k (glut), list ~$72k / $56k at 22% hardware GM.

**Evidence:** TRL 8 · Rule 1: SUPPORTED
  - [KTransformers README + Kimi-K2.5 / DeepSeek-V4-Flash tutorials](https://github.com/kvcache-ai/ktransformers) — industry, 2026-10. Opened. CPU-GPU hybrid MoE inference: Kimi-K2.5 needs >=600GB system RAM + 48GB VRAM, DeepSeek-V4-Flash needs >=200GB RAM + one RTX 5090. DRAM replaces HBM for weight residency.
  - [DeepSeek-V3 config_671B.json](https://github.com/deepseek-ai/DeepSeek-V3) — company, 2025-08. Opened. MLA latent KV (kv_lora_rank 512 + rope 64, 61 layers) is about 68.6 KiB/token at BF16, against 320 KiB/token for Llama-3.1-70B (computed by B).
  - [Samsung seeks >3x HBM3E pricing for HBM4](https://www.sammyfans.com/2026/10/02/samsung-seeks-more-than-3x-hbm3e-pricing-for-hbm4/) — news, 2026-10-02. CROSS-REF (p1-market.jsonl snippet). HBM3E ~$1.50/Gb; 2027 HBM4 asks mid-to-high $4/Gb.
  - [Counterpoint via EE Times Asia: 64GB RDIMM $450 to >$900](https://www.eetasia.com/memory-prices-surging-by-90-from-4q-2025/) — news, 2026-01. CROSS-REF (p1-market.jsonl snippet). Server RDIMM contract doubled 4Q25 to 1Q26.
  - [ServNet DDR5 server memory price tracker 2026](https://www.servnetuk.com/research/ddr5-server-memory-price-tracker-2026) — industry, 2026-08. CROSS-REF (p1-market.jsonl snippet). Street 64GB DDR5 RDIMM ~$2,064 (~$32/GB).

**Capital tier:** T1 | **Time to first revenue:** 6-9 months: one demo unit, then build-to-order with 50% deposits | **Gross margin estimate:** 18-30% hardware; 60-80% on subscription; blended ~25-35% if subscription attaches

**US manufacturability:** Assembled and tested in the U.S. (East Coast bench). CPUs/GPUs are TSMC and DDR5 is Korea/Taiwan (Micron Idaho from 2027). 'Assembled in USA' only, though TAA-compliant integration is feasible.

**Who is already doing this:** Puget Systems, Exxact, Lambda, Bizon, Supermicro, Dell Pro Max/HPE; NVIDIA DGX Station GB300 (large coherent memory) [UNVERIFIED-T]; Apple Mac Studio (512 GB unified memory) [UNVERIFIED-T]; KTransformers community/Chinese appliance vendors [UNVERIFIED-T]

**Wins on which axis, for which buyer:** $/GB of model-resident memory (DDR5 ~$26/GB vs ~$180-250/GB HBM-in-GPU) plus data sovereignty — for 20-500-person regulated firms (law, healthcare, CMMC/ITAR defense subcontractors) and universities running private chat/RAG/agents on 600B-1T-parameter MoE models

**Survives a 2029 glut?:** yes — A glut cuts the DRAM BOM from ~$20k to ~$8k, so the box gets cheaper and easier to sell. The risks are model-architecture shifts and GPU vendors' desk-side products, not DRAM price.

**Fatal-flaw candidate:** Commodity integration with thin hardware margin. NVIDIA DGX Station, Apple unified-memory machines and big OEMs can undercut, and ~20-45 tok/s single-stream throughput disappoints multi-user deployments. The only moat is service quality, and it is a reseller business, not a memory venture.

*Possible?* yes: documented open-source configurations · *Profitable?* marginal: yes only if a recurring support/model subscription attaches · *Doable by this founder?* yes: integration + software, startable with deposits

*Business-model lenses:* module/appliance; SaaS (model-update/monitoring subscription); defense-first niche

### C-49 — TB-Class CXL Node for EDA/Genomics/HANA

*Sub-branch:* CXL memory expansion - vertical large-memory appliance · *Materials sense:* c-capital

**What it is:** Pre-validated single-socket Xeon 6 / EPYC 9005 servers carrying 8-16 E3.S CXL memory modules (Samsung CMM-D, Micron CZ122, SK hynix CMM-DDR5) that add 2-4 TB behind local DDR5. They are tuned with upstream weighted-interleave/DAMON tiering (SK hynix HMSDK) and Samsung SMDK, and sold to chip-design teams (full-chip Cadence/Synopsys runs), genome assemblers and SAP HANA shops that otherwise buy 4-socket boxes or cloud high-memory instances.

**Why it could work:** CXL breaks the DIMM-slot ceiling without the 4-socket premium. Weighted interleave adds bandwidth as well as capacity (HMSDK). Single-host Type-3 support is stabilizing in Linux ([2]). Capacity-bound EDA and genomics jobs care about TB per node more than latency.

**Evidence:** TRL 8 · Rule 1: SUPPORTED
  - [SK hynix HMSDK README](https://github.com/skhynix/hmsdk) — company, 2025-11. Opened. HMSDK v4.0 (2025-11-03). CXL weighted-interleave landed in upstream Linux v6.9 and DAMON tier migration in v6.11. CXL tiering software is free and upstream.
  - [Samsung SMDK v2.2 README (CXL Memory Expander software)](https://github.com/OpenMPDK/SMDK) — company, 2024-12. Opened. Samsung CMM software stack (memory-node/swap/cache interfaces, tiering engine), demoed at SC24, OCP 2024 and FMS 2024. Last commit 2024-12-09.
  - [Linux CXL Subsystem Maturity Map (mainline, HEAD 2026-10-31)](https://github.com/torvalds/linux/blob/master/Documentation/driver-api/cxl/maturity-map.rst) — industry, 2026-10. Opened. Single-host Type-3 enumeration/HDM decoders are [2] stabilizing. Dynamic Capacity Devices, multi-host sharing and fabrics/G-FAM are [0] known gaps. PMEM GPF/dirty shutdown is [3] mature.

**Capital tier:** T1 | **Time to first revenue:** 9-15 months: two validated reference configs, then sales through EDA/genomics channels | **Gross margin estimate:** 15-25%

**US manufacturability:** U.S. integration. The CMM modules are Samsung/SK hynix (Korea) and Micron (non-U.S. assembly [UNVERIFIED-T]).

**Who is already doing this:** Supermicro, Dell, HPE, Lenovo (CXL-ready platforms); Penguin Solutions/SMART Modular; Colfax, Silicon Mechanics; AWS/Azure high-memory instances [UNVERIFIED-T]

**Wins on which axis, for which buyer:** TB per socket and $/TB vs 4-socket servers or cloud high-memory instances — for EDA teams at fabless startups, genomics cores, SAP HANA operators

**Survives a 2029 glut?:** partially — Cheap DDR5 plus 128-256 GB RDIMM/MRDIMM give 3-6 TB per socket without CXL, so only workloads above the slot ceiling still need it.

**Fatal-flaw candidate:** Big OEMs already sell CXL-ready platforms with the same modules. At 2026 DRAM prices the binding constraint is dollars, not slots, so breaking the CXL ceiling is not the customer's pain point.

*Possible?* yes · *Profitable?* marginal: VAR margins against OEM incumbents · *Doable by this founder?* marginal

*Business-model lenses:* module/appliance (VAR); SaaS (tiering tuning/telemetry)

### C-50 — Rack-Scale CXL Pooling Appliance

*Sub-branch:* CXL switching / multi-host memory pooling · *Materials sense:* c-capital

**What it is:** A 2-4U memory appliance with a CXL 2.0/3.x switch (XConn Apollo or Panmnesia class) fanning 16-32 hosts into a shared DDR5/DDR4 pool behind Type-3 controllers, plus orchestration software. It is sold to VM-cloud operators to cut stranded memory.

**Why it could work:** Pond (Azure, ASPLOS '23) showed that pooling across ~16 sockets cuts fleet DRAM by single-digit-to-~10% and that a large share of rented memory is untouched [UNVERIFIED-T exact figures]. At 4Q26 prices a 7-9% fleet saving is very large money for a hyperscaler.

**Evidence:** TRL 5 · Rule 1: SUPPORTED
  - [Pond: CXL-Based Memory Pooling Systems for Cloud Platforms (ASPLOS '23) artifact repo](https://github.com/vtess/Pond) — conference, 2023-03. Opened. Microsoft Azure/Virginia Tech CXL pooling paper. The repo holds the CXL-emulation scripts, and the paper preprint is linked at huaicheng.github.io/p/asplos23-pond.pdf (not opened).
  - [Linux CXL Subsystem Maturity Map (mainline, HEAD 2026-10-31)](https://github.com/torvalds/linux/blob/master/Documentation/driver-api/cxl/maturity-map.rst) — industry, 2026-10. Opened. Single-host Type-3 enumeration/HDM decoders are [2] stabilizing. Dynamic Capacity Devices, multi-host sharing and fabrics/G-FAM are [0] known gaps. PMEM GPF/dirty shutdown is [3] mature.

**Capital tier:** T3 | **Time to first revenue:** 36-48 months: switch silicon access, OS support, hyperscaler qualification | **Gross margin estimate:** 30-45%

**US manufacturability:** Switch/controller silicon from TSMC; chassis assembly could be U.S.

**Who is already doing this:** Liqid (composable memory), GigaIO, XConn, Panmnesia (CXL 3.x switch), Unifabrix (status unknown), H3 Platform, Astera Labs, Enfabrica (NVIDIA acqui-hire Sep 2025) [all UNVERIFIED-T]

**Wins on which axis, for which buyer:** Stranded-memory reduction (fleet $/GB) — for Hyperscale and large VM cloud operators

**Survives a 2029 glut?:** no — Savings scale with DRAM price. At -60% a 7-9% fleet saving no longer funds switches, controllers and the latency penalty.

**Fatal-flaw candidate:** The OS is not ready: mainline Linux (2026-10-31) still lists Dynamic Capacity, multi-host sharing and fabrics as [0] known gaps. The only buyers big enough to benefit build their own, and Pond's own result was single-digit-percent savings.

*Possible?* marginal: hardware exists, OS/pooling stack immature in late 2026 · *Profitable?* no · *Doable by this founder?* no

*Business-model lenses:* module/appliance; fabless->foundry (switch)

### C-51 — Persistent CXL Log Card (post-Optane PMem for WAL/journals)

*Sub-branch:* Tiered memory - persistent CXL tier (NVDIMM-N/MRAM successor) · *Materials sense:* a-material · *Merged from:* B.08, A2.12

**What it is:** A 16-64 GB CXL Type-3 persistent-memory card: DDR5 backed by NAND plus supercapacitors (NVDIMM-N style), or a DRAM front fronted by Everspin STT-MRAM (Chandler AZ) for the hot journal. It is exposed as CXL PMEM with Global Persistent Flush and targets database write-ahead logs and storage-array journals that lost their home when Intel killed Optane PMem.

**Why it could work:** Linux's CXL subsystem scores PMEM GPF/dirty-shutdown [3] mature, so the software path exists. IBM FlashCore Module 5 replaced capacitors with Everspin MRAM for power-loss protection (Oct 2026), so persistent journaling memory has buyers. Sub-microsecond durable commits beat NVMe flush latency by 10-100x.

**Evidence:** TRL 6 · Rule 1: SUPPORTED
  - [Linux CXL Subsystem Maturity Map (mainline, HEAD 2026-10-31)](https://github.com/torvalds/linux/blob/master/Documentation/driver-api/cxl/maturity-map.rst) — industry, 2026-10. Opened. Single-host Type-3 enumeration/HDM decoders are [2] stabilizing. Dynamic Capacity Devices, multi-host sharing and fabrics/G-FAM are [0] known gaps. PMEM GPF/dirty shutdown is [3] mature.
  - [IBM uses Everspin MRAM in FlashCore Module 5](https://www.blocksandfiles.com/flash/2026/10/05/ibm-using-everspin-mram-in-5th-gen-flashcore-modules/5300966) — news, 2026-10-05. CROSS-REF (A2.jsonl snippet). Storage OEM builds its own MRAM-backed power-loss journal.
  - [Everspin 1Gb STT-MRAM distributor price](https://www.lcsc.com/product-image/C20342497.html) — industry, 2026. CROSS-REF (A2.jsonl snippet). $102.60 @500 for 1Gb, i.e. ~$821/GB.
  - [Intel 10-Q Q2-2022: Optane wind-down](https://www.sec.gov/Archives/edgar/data/50863/000005086322000030/intc-20220702.htm) — industry, 2022-07. CROSS-REF (A2.jsonl snippet). $559M Optane inventory impairment.
  - [World's First 1 Gb 28 nm STT-MRAM Product - by Everspin](https://www.techinsights.com/blog/memory/worlds-first-1-gb-28-nm-stt-mram-product-everspin) — industry, 2019. 1Gb die 105.1 mm2, cell 0.0396 um2, 9.75 Mb/mm2 on GF 28nm (via search snippet)
  - [IBM and Everspin announce 19TB NVMe SSD with MRAM write cache](https://www.anandtech.com/show/13174) — news, 2018-08. IBM chose MRAM over DRAM+supercaps because supercaps/batteries last only a few years (via search snippet)

**Capital tier:** T2 | **Time to first revenue:** 24-36 months: card + firmware, then a design-in at one database or storage OEM | **Gross margin estimate:** 45-60%

**US manufacturability:** Board assembly U.S.; Everspin Toggle MRAM is made in Chandler AZ (STT 1Gb via GF Singapore); DRAM/NAND imported

**Who is already doing this:** SMART Modular (CXL NV-CMM) [UNVERIFIED-T]; Samsung CMM-H (DRAM+NAND hybrid) [UNVERIFIED-T]; Netlist (NVDIMM history); Everspin (MRAM in IBM FCM); Kioxia XL-Flash

**Wins on which axis, for which buyer:** Non-volatility at memory latency (durable commit latency) — for Database vendors (log/commit path), storage-array OEMs (journals), low-latency trading

**Survives a 2029 glut?:** yes — Value is persistence, not $/GB, so a DRAM glut barely changes the price per card, but volume stays tiny.

**Fatal-flaw candidate:** The market is tiny. Optane PMem died for lack of volume (>$7B losses). NVMe with power-loss protection plus group commit is 'good enough', and storage OEMs build journals in-house (IBM uses MRAM). MRAM at ~$821/GB caps capacity to megabytes-gigabytes.

*Possible?* yes: NVDIMM-N and CXL NV-CMM demos exist · *Profitable?* marginal: niche volumes · *Doable by this founder?* no

*Business-model lenses:* module/appliance; IP licensing (firmware)

### C-52 — LPDDR 'HBM-lite' Memory Chiplet (UCIe/AIB-attached)

*Sub-branch:* HBM alternatives / chiplet memory · *Materials sense:* mixed:b+c

**What it is:** A fabless memory-controller chiplet with a UCIe or open AIB 2.0 die-to-die interface on one side and 4-8 LPDDR5X channels on the other. It would be taped out at GlobalFoundries 12LP+ (Malta, NY) or TSMC N6 and sold or licensed to AI-ASIC startups that cannot get HBM allocation, giving ~0.5-1 TB/s and 128-512 GB per package at LPDDR prices.

**Why it could work:** HBM takes ~22% of DRAM wafer starts for ~9% of bits and ~3x DDR5's wafer area per bit. HBM4 2027 asks of ~$4.5-4.9/Gb (~$36-39/GB) and allocation to the big GPU makers leave smaller ASIC teams short. LPDDR5X proves the bandwidth-per-pin path (NVIDIA Grace), and open AIB RTL lowers die-to-die IP cost.

**Evidence:** TRL 6 · Rule 1: SUPPORTED
  - [CHIPS Alliance AIB PHY RTL (open die-to-die interface)](https://github.com/chipsalliance/aib-phy-hardware) — industry, 2024-09. Opened. Open-source die-to-die PHY RTL (AIB 1.0/2.0, originally Intel), a royalty-free D2D path for chiplets.
  - [TrendForce via TechNews: HBM share of DRAM wafer starts](https://technews.tw/?p=1565421) — news, 2026. CROSS-REF (p1-market.jsonl snippet). HBM is ~22% of wafer starts in 2026 (30% in 2027) for ~9% of bits.
  - [Micron: HBM-vs-DDR5 silicon gap widening](https://www.tomshardware.com/tech-industry/semiconductors/micron-says-the-silicon-gap-between-hbm-and-ddr5-is-widening-with-every-generation) — news, 2026. CROSS-REF (p1-market.jsonl snippet). HBM takes ~3x the wafer area of DDR5 per bit.
  - [Samsung seeks >3x HBM3E pricing for HBM4](https://www.sammyfans.com/2026/10/02/samsung-seeks-more-than-3x-hbm3e-pricing-for-hbm4/) — news, 2026-10-02. CROSS-REF (p1-market.jsonl snippet). HBM3E ~$1.50/Gb; 2027 HBM4 asks mid-to-high $4/Gb.
  - [TrendForce 2Q26 mobile DRAM contract via China Times](https://wantrich.chinatimes.com/news/20260515900291-420101) — news, 2026-05-15. CROSS-REF (p1-market.jsonl snippet). LPDDR4X +70-75%, LPDDR5X +78-83% QoQ in 2Q26.

**Capital tier:** T3 | **Time to first revenue:** 36-48 months: architecture, tape-out, package qualification, first design-in | **Gross margin estimate:** 50-65% (chiplet/IP)

**US manufacturability:** GlobalFoundries Malta NY can fab a 12nm-class controller. Advanced packaging at Amkor Arizona (2027-28 [UNVERIFIED-T]). LPDDR5X dies are imported.

**Who is already doing this:** Eliyan (NuLink die-to-die PHY), Marvell (custom HBM/memory chiplets), Synopsys/Cadence (UCIe + LPDDR IP), Alphawave (Qualcomm), d-Matrix, Tenstorrent, Primemas, NVIDIA Grace LPDDR5X [UNVERIFIED-T for company specifics]

**Wins on which axis, for which buyer:** Bandwidth per dollar and allocation-free supply vs HBM for inference ASICs — for AI-inference ASIC startups, edge-AI SoC teams, defense ASIC programs

**Survives a 2029 glut?:** partially — A glut eases HBM allocation and removes the 'can't get HBM' motive, though LPDDR's lower $/GB keeps a cost niche. LPDDR prices themselves rose +70-90% QoQ in 1H26.

**Fatal-flaw candidate:** IP giants (Synopsys, Cadence, Alphawave, Eliyan) already sell UCIe+LPDDR PHY/controller IP, and serious ASIC teams integrate in-house. A startup chiplet faces a $20-60M tape-out for a handful of customers.

*Possible?* yes · *Profitable?* marginal: crowded IP market · *Doable by this founder?* no

*Business-model lenses:* fabless->foundry; IP licensing

### C-53 — High-Bandwidth Flash (HBF) Weight-Store Module

*Sub-branch:* HBM alternatives - stacked NAND with HBM-like interface · *Materials sense:* a-material

**What it is:** Accelerator boards or appliances that pair a GPU/ASIC with SanDisk/SK hynix High Bandwidth Flash stacks (TSV-stacked BiCS NAND dies behind an HBM-like interface) to hold read-mostly model weights at ~8-16x HBM capacity per stack. The NAND is made at Kioxia/SanDisk Yokkaichi/Kitakami.

**Why it could work:** Inference weights are read-mostly, and NAND $/GB is ~50-100x below DRAM. NAND is heading to surplus in 2H27 and contract prices were already flat in Oct 2026. SanDisk is diversifying into memory-class products (3D Matrix Memory nearing product specs).

**Evidence:** TRL 4 · Rule 1: SUPPORTED
  - [SanDisk Investor Day 2026](https://quartr.com/events/sandisk-corporation-sndk-investor-day-2026_F6lVAkBS) — company, 2026. CROSS-REF (A2.jsonl snippet). SanDisk memory roadmap beyond NAND (3D Matrix Memory nearing product specs).
  - [NAND flat after 21 months while DRAM hits record](https://tech-insider.org/dram-record-high-nand-flat-21-months-october-2026/) — news, 2026-10. CROSS-REF (p1-market.jsonl snippet). NAND contract stopped rising in Oct 2026.
  - [TrendForce 2026-07-30 press release](https://www.trendforce.com/presscenter/news/20260730-13158.html) — industry, 2026-07-30. CROSS-REF (p1-market.jsonl snippet). NAND turns to surplus in 2H27 while the DRAM gap widens.

**Capital tier:** T3 | **Time to first revenue:** 4+ years: HBF samples reportedly 2H26, devices 2027 [UNVERIFIED-T]; system integration after | **Gross margin estimate:** unknown; 30-50% for a system integrator

**US manufacturability:** None: NAND fabs in Japan, packaging in Asia; integration would happen inside GPU/ASIC packages at TSMC CoWoS.

**Who is already doing this:** SanDisk (HBF, announced 2025 [UNVERIFIED-T]); SK hynix (HBF standardization MoU with SanDisk, Aug 2025 [UNVERIFIED-T]); Samsung, Kioxia (reported)

**Wins on which axis, for which buyer:** Capacity per package and $/GB vs HBM for read-heavy inference weights — for GPU/ASIC vendors (NVIDIA, AMD, hyperscaler ASIC teams)

**Survives a 2029 glut?:** partially — Its competitor is HBM, not DDR5, but a DRAM/HBM glut narrows the capacity-cost gap that justifies flash's endurance and latency compromises.

**Fatal-flaw candidate:** Integration happens inside GPU/ASIC packages at TSMC, so there is no socket for a small company. NAND endurance rules out write-heavy KV, so HBF is a weights-only niche controlled by memory makers and GPU vendors.

*Possible?* marginal: TRL 4-5, samples not yet public · *Profitable?* no for a small entrant · *Doable by this founder?* no

*Business-model lenses:* module/appliance (theoretical)

### C-54 — PIM DIMM Accelerator Servers (UPMEM / AiM) for Scans and Genomics

*Sub-branch:* Processing-in-memory · *Materials sense:* b-process

**What it is:** Servers fitted with UPMEM PIM DIMMs (DDR4 DIMMs with in-order DPUs on each DRAM die) or SK hynix GDDR6-AiM/AiMX cards, sold for memory-bound kernels: genomic read alignment, database scans and filters, recommendation embedding lookups. The aim is less DRAM bandwidth and capacity per unit of work.

**Why it could work:** Moving compute to the DRAM die removes the memory-bus bottleneck. ETH SAFARI's PrIM suite shows large speedups on memory-bound kernels over CPUs on real UPMEM hardware (IEEE Access 2022; exact ratios [UNVERIFIED-T]). Samsung HBM-PIM/LPDDR5X-PIM and SK hynix AiM show vendor interest.

**Evidence:** TRL 7 · Rule 1: SUPPORTED
  - [PrIM benchmarks for UPMEM PIM (ETH SAFARI) + IEEE Access 2022 characterization](https://github.com/CMU-SAFARI/prim-benchmarks) — peer-reviewed, 2026-06. Opened. Real UPMEM PIM hardware (DRAM arrays + in-order DPUs) characterized on memory-bound kernels. Repo active Jun 2026. Paper at ieeexplore.ieee.org/abstract/document/9771457 (seen, not opened).

**Capital tier:** T1 | **Time to first revenue:** 12-24 months as a specialist integrator, if a PIM supplier is still selling | **Gross margin estimate:** 20-35%

**US manufacturability:** None for PIM silicon (foreign DRAM-process partners); U.S. integration only

**Who is already doing this:** UPMEM (France; current company status not verified this session); Samsung (HBM-PIM, LPDDR5X-PIM); SK hynix (GDDR6-AiM, AiMX); NeuroBlade (SQL accelerator); GSI Technology (SRAM APU, Sunnyvale) [UNVERIFIED-T]

**Wins on which axis, for which buyer:** Throughput and energy per byte moved for memory-bound kernels — for Genomics cores, analytics/database operators

**Survives a 2029 glut?:** partially — The value is bandwidth and energy, not $/GB, but cheap DRAM removes the 'less RAM per job' argument.

**Fatal-flaw candidate:** Hard programming model, single-vendor supply risk, and DDR4-based UPMEM DIMMs stranded as servers go DDR5-only. GPUs with HBM run the same kernels with a mature CUDA stack.

*Possible?* yes: real hardware characterized · *Profitable?* no: no commercial pull beyond research · *Doable by this founder?* no

*Business-model lenses:* module/appliance; university/lab patent license

### C-55 — Analog CIM Edge Module (DRAM-free defense edge inference)

*Sub-branch:* Compute-in-memory (analog/charge-domain) · *Materials sense:* b-process

**What it is:** Rugged M.2/PCIe edge-AI modules built around analog or charge-domain compute-in-memory accelerators (EnCharge AI EN100, Mythic next-gen, Sagence), where weights stay in on-chip memory arrays and little or no external LPDDR is needed. They would be sold to U.S. drone/ISR integrators and assembled in the U.S.

**Why it could work:** Weight-stationary in-memory compute removes most DRAM traffic and BOM. Edge boxes were hit by LPDDR4X/5X contract hikes of +70-90% QoQ in 1H26, and defense buyers value W/inference and a U.S.-assembled supply chain.

**Evidence:** TRL 6 · Rule 1: SUPPORTED
  - [IBM Analog Hardware Acceleration Kit](https://github.com/IBM/aihwkit) — industry, 2026-10. Opened. Analog in-memory computing toolkit, still labelled 'beta' in Oct 2026. AIMC is research-grade.
  - [TrendForce 2Q26 mobile DRAM contract via China Times](https://wantrich.chinatimes.com/news/20260515900291-420101) — news, 2026-05-15. CROSS-REF (p1-market.jsonl snippet). LPDDR4X +70-75%, LPDDR5X +78-83% QoQ in 2Q26.

**Capital tier:** T1 | **Time to first revenue:** 18-30 months: vendor partnership, ruggedized module, SBIR/defense pilot | **Gross margin estimate:** 25-40%

**US manufacturability:** CIM chips designed in the U.S. (EnCharge Santa Clara, Mythic Austin), fabbed at TSMC/foreign foundries [UNVERIFIED-T]; module assembly U.S.

**Who is already doing this:** EnCharge AI, Mythic, Sagence AI, IBM Research (analog AI), d-Matrix (digital IMC, datacenter), Axelera (EU); digital competitors Hailo, NVIDIA Jetson, Qualcomm [UNVERIFIED-T]

**Wins on which axis, for which buyer:** W per inference and a DRAM-free BOM at the edge — for Defense UAS/ISR integrators, industrial machine vision

**Survives a 2029 glut?:** yes — The axis is power, not DRAM price, so the glut weakens only the secondary 'avoid LPDDR cost' argument.

**Fatal-flaw candidate:** Edge AI is being won by digital NPUs with mature toolchains. Analog CIM carries accuracy/toolchain risk (IBM's kit is still 'beta') and startup-vendor fragility, and an integrator sits between two stronger parties: not a memory business.

*Possible?* yes: shipping silicon from at least one vendor [UNVERIFIED-T] · *Profitable?* marginal · *Doable by this founder?* marginal

*Business-model lenses:* module/appliance; defense-first niche

### C-56 — TrustedCXL: U.S.-Provenance DDR4 CXL Expander for DoD/DOE HPC

*Sub-branch:* CXL memory expansion - defense-first provenance · *Materials sense:* c-capital

**What it is:** A CXL Type-3 expander built from Micron Manassas-made 1-alpha DDR4 (the U.S.-fabbed DRAM ramping since May 2026 for defense, aero and auto) and a U.S.-HQ DDR4-capable controller (Microchip SMC 2000-class), assembled and tested at a DMEA-accredited U.S. trusted EMS. It is sold to DoD HPCMP centers, NNSA labs and defense primes needing capacity with TAA/Buy-American and trusted-supply provenance.

**Why it could work:** Manassas quadruples DDR4 wafer supply, with qualified output by end-2026, aimed at exactly these buyers. The DoD supply chain already pays for on-shore memory capability (Amentum's $40M Everspin MRAM deal). DDR4 behind CXL lets DDR5-only HPC nodes consume U.S.-fabbed DRAM.

**Evidence:** TRL 6 · Rule 1: SUPPORTED
  - [Micron advances Made-in-America memory in Virginia](https://www.hpcwire.com/off-the-wire/micron-advances-made-in-america-memory-with-manufacturing-expansion-in-virginia) — company, 2026-05-22. CROSS-REF (p1-fabs.jsonl snippet). Manassas 1-alpha DDR4/LP4 for defense/aero/auto/industrial; 4x DDR4 wafer supply; qualified output by end-2026.
  - [Everspin $40M MRAM deal for defense memory](https://electronics360.globalspec.com/article/23702/everspin-earns-40-million-mram-deal-for-defense-memory-services) — news, 2026-04. CROSS-REF (A2.jsonl snippet). The DoD supply chain pays for on-shore memory capability.
  - [Linux CXL Subsystem Maturity Map (mainline, HEAD 2026-10-31)](https://github.com/torvalds/linux/blob/master/Documentation/driver-api/cxl/maturity-map.rst) — industry, 2026-10. Opened. Single-host Type-3 enumeration/HDM decoders are [2] stabilizing. Dynamic Capacity Devices, multi-host sharing and fabrics/G-FAM are [0] known gaps. PMEM GPF/dirty shutdown is [3] mature.

**Capital tier:** T2 | **Time to first revenue:** 30-36 months: SBIR Phase I/II, trusted-EMS qualification, first lab buy | **Gross margin estimate:** 35-50%

**US manufacturability:** DRAM: Micron Manassas VA. Assembly/test: U.S. trusted EMS. Controller die: TSMC (Taiwan), the provenance gap.

**Who is already doing this:** Micron (direct to defense), SMART Modular (defense memory), Mercury Systems, Netlist, Microchip [UNVERIFIED-T for CXL-specific defense offerings]

**Wins on which axis, for which buyer:** Supply security/provenance and lifecycle length — for DoD HPC Modernization Program centers, DOE/NNSA labs, defense-prime on-prem HPC

**Survives a 2029 glut?:** yes — The provenance premium does not depend on price, and Manassas DDR4 serves long-lifecycle buyers whatever DDR5 does. Volume stays small.

**Fatal-flaw candidate:** The controller is fabbed in Taiwan, so 'all-U.S.' is only partly true. Buyers are few and slow (FAR procurement), and Micron/SMART can serve them directly. Manassas DDR4 is allocated to existing auto/defense customers first.

*Possible?* yes: each component exists · *Profitable?* marginal: premium pricing, tiny volume · *Doable by this founder?* marginal: only as an SBIR-led partnership

*Business-model lenses:* defense-first niche; module/appliance; SBIR/STTR (non-dilutive start)

### C-57 — Memory-Fabric SuperNIC (Ethernet-attached DRAM for GPUs) - acquired away

*Sub-branch:* Far memory over RDMA / custom memory-fabric silicon · *Materials sense:* c-capital

**What it is:** A custom NIC/switch ASIC that attaches pools of commodity DDR5 (behind CXL controllers) to GPU servers over 800G-3.2T Ethernet/RDMA, giving each GPU tens of TB of 'elastic' memory for KV cache and weights. This is the Enfabrica ACF-S/EMFASYS concept, taped out at TSMC.

**Why it could work:** GPUs need far more memory than HBM supplies (KV for a 128k Llama-70B context is 40 GiB at BF16). Ethernet/RDMA reloads a 128k context in ~0.5 s vs ~41 s recompute, and commodity DDR5 at ~$26/GB beats HBM-in-GPU at ~$180-250/GB.

**Evidence:** TRL 6 · Rule 1: SUPPORTED
  - [Mooncake README + Mooncake Store deployment guide (Kimi serving platform)](https://github.com/kvcache-ai/Mooncake) — company, 2026-11. Opened. KV-cache-centric disaggregation lets Kimi handle 75% more requests within SLO. Store has CXL-aware allocation (--enable_cxl, /dev/dax, --allocation_strategy=cxl). Integrated into vLLM (May 2026) and TensorRT-LLM (Oct 2026).
  - [vLLM KV Offloading Usage Guide](https://github.com/vllm-project/vllm/blob/main/docs/features/kv_offloading_usage.md) — industry, 2026-11. Opened. CPU host memory is the primary KV offload tier, and secondary tiers are staged through it. Host DRAM capacity is mandatory for KV tiering.
  - [Meta llama-models sku_list.py](https://github.com/meta-llama/llama-models) — company, 2025-10. Opened. Llama-3.1 70B has 80 layers and 8 KV heads with head_dim 128, which gives 320 KiB/token KV at BF16 (40 GiB at 128k context).

**Capital tier:** T3 | **Time to first revenue:** 4+ years for a new entrant | **Gross margin estimate:** 60%+ for merchant silicon if it wins

**US manufacturability:** TSMC silicon; U.S. design only

**Who is already doing this:** Enfabrica (team and technology licensed/acqui-hired by NVIDIA, Sep 2025 [UNVERIFIED-T]); NVIDIA (BlueField/ConnectX + Dynamo); Astera Labs, Broadcom, Marvell; Mooncake Transfer Engine (software over standard RDMA)

**Wins on which axis, for which buyer:** GPU-reachable memory capacity per dollar — for Hyperscalers and GPU cloud builders

**Survives a 2029 glut?:** partially — Cheaper DRAM makes pools cheaper, but the silicon economics depend on design wins at NVIDIA-scale customers, not DRAM price.

**Fatal-flaw candidate:** The leading independent attempt was absorbed by NVIDIA, and standard RDMA NICs plus open-source software (Mooncake Transfer Engine, NIXL) deliver most of the benefit. There is no room for a new custom-silicon entrant.

*Possible?* yes: demonstrated before acquisition [UNVERIFIED-T] · *Profitable?* no for a new entrant · *Doable by this founder?* no

*Business-model lenses:* fabless->foundry

## C. Manufacturing & supply chain (U.S.) (15 cards)

### C-58 — Legacy-DRAM fab in the U.S. on a licensed 25-46nm process (tempting, dead)

*Sub-branch:* Trailing-node DRAM wafer fab · *Materials sense:* mixed:b+c

**What it is:** License a mature stacked-capacitor DRAM flow (Winbond's Qimonda-derived 46/38nm buried-wordline lineage, a PSMC 2x-nm DRAM-foundry flow, or Qimonda's patent/document set as CXMT did in 2019 [UNVERIFIED-training]) and install it in a U.S. 300mm shell (new building or a distressed site) to make DDR3 4Gb / DDR4 8Gb / LPDDR4 dies at ~20k wafers per month. Product: JEDEC FBGA components and KGD sold as 'U.S.-made long-lifecycle DRAM'.

**Why it could work:** Legacy DRAM is the tightest segment: DDR4 8Gb contract $16/GB and DDR3 4Gb ~$20/GB (June 2026), DDR4 dearer than DDR5 in Oct 2026, and the majors are exiting DDR4. Second-tier legacy makers earn ~80% operating margins (Nanya 3Q26 GM 85.7%). Model (Appendix A): $2.0-3.5B capex at 20k wpm, 25nm-class 8Gb die ~73 mm2, ~714 good GB/wafer -> $5.5-7.2/GB cost vs $16/GB today.

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [Micron advances Made-in-America memory with manufacturing expansion in Virginia](https://www.hpcwire.com/off-the-wire/micron-advances-made-in-america-memory-with-manufacturing-expansion-in-virginia) — company, 2026-05-22. Micron Manassas Fab 6 began 1-alpha DDR4/LPDDR4 on 2026-05-22 for auto, defense, aerospace and industrial buyers, in a >$2B expansion that quadruples its DDR4 wafer supply (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Nanya 3Q26 results (TrendForce News)](https://www.trendforce.com/news/?p=65146) — news, 2026-10-12. Nanya 3Q26 gross margin 85.7%, operating margin 80%; LTAs expired end-June 2026 and repriced >60% higher in July (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [China's CXMT DDR5 reveals 3-year technology gap](https://semiwiki.com/forum/threads/chinas-cxmts-ddr5-reveals-3-year-technology-gap.23270/latest) — industry, 2025. CXMT 16Gb DDR5 at 0.239 Gb/mm2: the license-documents-and-hire path to DRAM took CXMT ~8 years and tens of $B (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [New DRAM value-per-area chart (Kurnal Insights)](https://www.kitguru.net/channel/generaltech/joao-silva/new-dram-value%E2%80%91per%E2%80%91area-chart-draws-attention-amid-rising-memory-prices/) — news, 2026-09. 1b DRAM ~0.436 Gb/mm2, ~4x the ~0.11 Gb/mm2 a licensed 25nm-class process would give (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Micron and SK hynix commit billions to memory capacity but almost nothing lands before 2028](https://www.storagereview.com/news/micron-and-sk-hynix-commit-billions-to-memory-capacity-but-almost-nothing-lands-before-2028) — news, 2026. New DRAM capacity mostly arrives 2028+; any new U.S. legacy fab would land later still (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Qimonda Richmond (Sandston VA) 300mm DRAM fab closure and tool sale; CXMT acquisition of ~10,000 Qimonda technical documents and Qimonda patent licence via WiLAN/Polaris]() — news, 2009 / 2019. [UNVERIFIED-training] citation from C's training data (to ~mid-2026). No URL could be opened or seen this session (WebSearch budget exhausted; WebFetch DNS-blocked). Verify agent: add a URL or downgrade. A U.S. 300mm DRAM fab was already stranded once, in good times; the Qimonda IP path was taken by CXMT, which still needed ~8 years, ex-Elpida/Hynix engineers and state money.

**Capital tier:** T4 | **Time to first revenue:** ~6 years (license + shell + tool install + yield ramp + customer qualification), i.e. ~2031, after the A-05 glut | **Gross margin estimate:** 60-65% at 2026 prices; ~0% in the A-05 glut ($7.2/GB vs $5.5-7.8/GB cost); deeply negative in a 2023-like trough ($1.30/GB)

**US manufacturability:** No host. No U.S. foundry has a DRAM capacitor module; the only U.S. DRAM fab is Micron Manassas Fab 6 (captive). 150/200mm distressed sites (Akoustis Canandaigua NY, Wolfspeed Durham NC, Microchip Tempe) cannot run competitive DRAM [UNVERIFIED-training site status].

**Who is already doing this:** Micron Manassas VA (1-alpha DDR4/LP4 since 2026-05-22, $275M CHIPS); Winbond, Nanya, PSMC (Taiwan); CXMT (China, ~320K wpm).

**Wins on which axis, for which buyer:** Supply security and U.S. origin for long-lifecycle DDR3/DDR4 — for Defense, automotive, industrial and medical OEMs needing DDR4 into the 2030s

**Survives a 2029 glut?:** no — Cost $5.5-7.8/GB (5-yr depreciation) vs $7.2/GB A-05 DDR4 and $1.30/GB 2023 trough; Micron's 1-alpha gets ~2.7x the bits per wafer, so the new fab is the marginal, highest-cost producer when prices fall.

**Fatal-flaw candidate:** Micron is already doing exactly this at Manassas on a denser node with CHIPS money, so a licensed 25-46nm U.S. fab would be the highest-cost producer, landing around 2031, after the glut - a T4 bet with no edge.

*Possible?* yes - Winbond/Nanya/PSMC/CXMT prove the process; no U.S. host exists · *Profitable?* no - high-cost producer arriving into a glut against Micron Manassas · *Doable by this founder?* no - billions of capital and a fab team

*Business-model lenses:* fabless->foundry (inverted: own fab), IP licensing (inbound)

### C-59 — U.S.-HQ fabless long-lifecycle DRAM brand on Taiwanese foundry wafers

*Sub-branch:* Fabless legacy DRAM (foundry-sourced) · *Materials sense:* c-capital

**What it is:** A U.S.-headquartered fabless DRAM brand on the Alliance Memory / Etron / Zentel model: design or license a DDR4 8Gb and LPDDR4 4Gb die, buy 300mm wafers from PSMC's DRAM-foundry service or Winbond KGD, package and test at a Taiwanese OSAT, and sell with a written 10-15-year longevity commitment. U.S. content is design, sales and optional final test only.

**Why it could work:** Long-lifecycle buyers pay 1.2-2x for supply guarantees and are being orphaned (Micron DDR4 EOL notices June 2025; Samsung/SK hynix extensions only into 2026; Advantech steering customers off Samsung DDR4). Model: $3,000 foundry wafer -> ~$5.4/GB cost; GM ~71% at 2026 contract, ~41% at a cycle-average $8/GB, ~35% at the A-05 glut, but -135% in a 2023-like trough.

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [Etron Memory ICs - KGDM](https://etron.com/kgdm/) — company, unknown. Etron, a fabless Taiwanese specialty-DRAM company, sells KGD memory (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Winbond KGD (customized memory solution)](https://winbond.com/hq/product/customized-memory-solution/kgd/) — company, unknown. Winbond sells DRAM known-good die to SiP makers: an open legacy KGD source (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [DDR4 exit timeline unfolds for top memory makers](https://www.trendforce.com/news/2025/07/09/news-ddr4-exit-timeline-unfolds-for-top-memory-makers-plans-for-samsung-sk-hynix-and-micron) — news, 2025-07-09. Samsung, SK hynix and Micron DDR4 EOL schedules (last orders 2025, final shipments 2025-26) (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Samsung, SK hynix reportedly delay phase-out to 2026 as DDR4 becomes unexpected cash cow](https://www.trendforce.com/news/2025/09/02/news-samsung-sk-hynix-reportedly-delay-phase-out-to-2026-as-ddr4-becomes-unexpected-cash-cow/) — news, 2025-09-02. Majors extended DDR4 only into 2026; Micron issued DDR4 EOL notices June 2025 (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Response measures to Samsung DDR4 IC EOL announcement (Advantech)](https://www.advantech.com/en/resources/news/response-measures-to-samsung-ddr4-ic-eol-announcement) — company, 2025. Industrial-PC maker tells customers DDR4 supply runs to ~end-2026 and to avoid Samsung DDR4 in new designs: long-lifecycle buyers are actively managing EOL (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Micron reportedly joins Samsung in cutting DDR4 output, spurring opportunities for Taiwanese suppliers](https://www.trendforce.com/news/2025/04/23/news-micron-reportedly-joins-samsung-in-cutting-ddr4-output-spurring-opportunities-for-taiwanese-suppliers/) — news, 2025-04-23. Legacy DDR4 demand shifts to Taiwanese suppliers (Nanya, Winbond, PSMC) (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)

**Capital tier:** T2 | **Time to first revenue:** 36-48 months (die design or license, foundry tape-out, JEDEC qualification, design-ins at industrial OEMs) | **Gross margin estimate:** 35-70% from 2026 to the A-05 glut; negative in a 2023-like trough

**US manufacturability:** Essentially none: wafers in Taiwan (PSMC Hsinchu/Tongluo [UNVERIFIED-training]), packaging and test in Asia. TAA-compliant through Taiwan wafer origin; cannot claim 'Made in USA'.

**Who is already doing this:** Alliance Memory (Kirkland WA), Etron, Zentel, ISSI (owned by Beijing Ingenic), Intelligent Memory, GigaDevice (CXMT-fabbed DDR4 [UNVERIFIED-training]).

**Wins on which axis, for which buyer:** Lifecycle length / supply security — for Industrial-PC, networking, medical-imaging and avionics OEMs with 10-20-year product lives

**Survives a 2029 glut?:** partially — Longevity contracts are sticky, but CXMT/Nanya/Winbond backfill collapses legacy ASPs; a foundry customer is first cut in a shortage and only cheap in a glut.

**Fatal-flaw candidate:** Foundry wafer allocation: in the 2026 shortage PSMC and Winbond sell every DRAM wafer under their own brands or to incumbents, so a newcomer with ~$15M of NRE gets wafers only when prices have already collapsed.

*Possible?* yes - Etron/Zentel/Alliance operate this model · *Profitable?* marginal - margins depend on wafer allocation the newcomer will not get in a shortage · *Doable by this founder?* no - T2 hardware program with Taiwan-centric operations

*Business-model lenses:* fabless->foundry

### C-60 — 'Assembled in USA' commodity DDR4/DDR5 module brand (tempting, dead)

*Sub-branch:* U.S. module assembly · *Materials sense:* none

**What it is:** Buy packaged DRAM components through franchised distribution or SpecTek, SMT them onto JEDEC UDIMM/SODIMM/RDIMM boards at a U.S. EMS line, and sell a U.S.-assembled module brand into the consumer and federal gap left by Crucial's exit.

**Why it could work:** Crucial left consumer modules (announced 2025-12-03), retail DDR5 sits near $18/GB, patriotic and federal buyers exist, and the Buy American Act gives a 20-30% (DoD 50%) price-evaluation preference on small buys under the TAA threshold [UNVERIFIED-training].

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [Micron announces exit from Crucial consumer business](https://www.storagenewsletter.com/2025/12/05/micron-announces-exit-from-crucial-consumer-business/) — news, 2025-12-05. Micron exited consumer modules (announced 2025-12-03), leaving no U.S.-HQ first-party consumer module brand (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Memory prices surging by 90% from 4Q 2025 (Counterpoint via EE Times Asia)](https://www.eetasia.com/memory-prices-surging-by-90-from-4q-2025/) — news, 2026-01. 64GB RDIMM contract $450 (4Q25) to >$900 (1Q26): DRAM die dominates module cost (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [DDR5 server memory price tracker 2026 (ServNet)](https://www.servnetuk.com/research/ddr5-server-memory-price-tracker-2026) — industry, 2026-08. Street 64GB DDR5 RDIMM ~$2,064 (Aug 2026), ~$32/GB (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [PC DRAM 1Q26: prices to surge over 80% on server supply prioritization (TrendForce abstract)](https://www.trendforce.com/research/download/RP260114IU) — industry, 2026-01-14. DRAM supply prioritized to strategic OEMs while module makers are limited (abstract only) (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [What U.S. tariff push means for Korea's semiconductor industry](https://www.koreatimes.co.kr/opinion/20260915/what-us-tariff-push-means-for-koreas-semiconductor-industry) — news, 2026-09-15. Korean memory excluded from Section 232 phase 1: no tariff-created U.S.-origin premium for memory today (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)

**Capital tier:** T1 | **Time to first revenue:** 6-12 months if components can be bought at all (they mostly cannot at contract prices in 2026) | **Gross margin estimate:** 5-15% (commodity module house norm), higher only from inventory revaluation in an upswing

**US manufacturability:** Easy: Kingston (Fountain Valley CA) and Virtium (Rancho Santa Margarita CA) assemble in the U.S., and any U.S. EMS can SMT a DIMM [UNVERIFIED-training].

**Who is already doing this:** Kingston (dominant independent), Virtium, SMART Modular (Penguin), PNY (NJ), OWC, plus Taiwanese houses (ADATA, TeamGroup, G.Skill).

**Wins on which axis, for which buyer:** None that is paid for: 'assembled in USA' is not an axis buyers reward — for Consumer upgraders and small federal buys (BAA)

**Survives a 2029 glut?:** no — Commodity module houses lose money on inventory write-downs in every glut (2019, 2022-23); a new entrant without allocation timing loses most.

**Fatal-flaw candidate:** Assembly is ~0.6-1.0% of a 2026 64GB RDIMM's cost (Appendix A), TAA treats Taiwan/Korea as compliant and the FTC bars an unqualified Made-in-USA claim on foreign die, while the 93-98% that matters - die - is allocated away from small module makers; Netlist's PMIC/rank patents also read on new DDR5 RDIMM brands.

*Possible?* yes - trivial to assemble · *Profitable?* no - no die allocation, no paid premium, patent exposure · *Doable by this founder?* marginal - doable operationally, pointless economically

*Business-model lenses:* module/appliance

### C-61 — DRAM Continuity Vault: consignment last-time-buy storage plus LTB-sizing software

*Sub-branch:* Long-lifecycle supply services (die bank / LTB) · *Materials sense:* none

**What it is:** For mid-size U.S. industrial, medical, rail and defense-supplier OEMs facing DDR3/DDR4/LPDDR4 EOL, size the last-time buy with demand-forecast software, then hold the OEM-owned (consignment) DRAM components or KGD in nitrogen dry cabinets under J-STD-033 moisture control with AS6081-style chain of custody, periodic sample re-test, and scheduled call-offs. Revenue: ~4% per year of inventory value plus ~$12k per year of software per OEM.

**Why it could work:** EOL pain is acute and documented: Advantech is steering customers off Samsung DDR4, auto/industrial DDR4 buffers fell from 31+ weeks to 6-8 weeks, and authorized stock of a mainstream Micron DDR4 part was zero in May 2026. The OEM owns the inventory, so the venture carries no DRAM price risk. Model: loss-making below ~8 OEMs, ~27% GM at 10 OEMs ($7.5M under management), ~70% GM at 25 OEMs ($25M, $1.3M revenue).

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [Response measures to Samsung DDR4 IC EOL announcement (Advantech)](https://www.advantech.com/en/resources/news/response-measures-to-samsung-ddr4-ic-eol-announcement) — company, 2025. Industrial-PC maker tells customers DDR4 supply runs to ~end-2026 and to avoid Samsung DDR4 in new designs: long-lifecycle buyers are actively managing EOL (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Memory shortage watch: DDR3L/DDR4, May 2026 (Findchips)](https://blog.findchips.com/memory-shortage-watch-ddr3l-ddr4-may-2026/) — industry, 2026-05. Zero authorized stock of a mainstream Micron DDR4 part at Newark, Avnet and Mouser; only independent-market stock at a premium (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Micron ramps US-made DDR4 production in Virginia (eeNews Europe)](https://www.eenewseurope.com/en/micron-ramps-us-made-ddr4-production-in-virginia/) — news, 2026-05. DDR4 buffers at auto/industrial customers fell from 31+ weeks to 6-8 weeks (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [DDR4 exit timeline unfolds for top memory makers](https://www.trendforce.com/news/2025/07/09/news-ddr4-exit-timeline-unfolds-for-top-memory-makers-plans-for-samsung-sk-hynix-and-micron) — news, 2025-07-09. Samsung, SK hynix and Micron DDR4 EOL schedules (last orders 2025, final shipments 2025-26) (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Samsung, SK hynix reportedly delay phase-out to 2026 as DDR4 becomes unexpected cash cow](https://www.trendforce.com/news/2025/09/02/news-samsung-sk-hynix-reportedly-delay-phase-out-to-2026-as-ddr4-becomes-unexpected-cash-cow/) — news, 2025-09-02. Majors extended DDR4 only into 2026; Micron issued DDR4 EOL notices June 2025 (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)

**Capital tier:** T1 | **Time to first revenue:** 9-15 months (software MVP + one pilot OEM consignment; AS6081/ISO 9001 groundwork in parallel) | **Gross margin estimate:** negative below ~8 OEMs; ~27% at 10; ~70% at 25 OEMs

**US manufacturability:** A 2,000-4,000 sq ft ESD- and climate-controlled vault on the East Coast; no fab dependency; U.S.-made DDR4 from Micron Manassas can be the stored part where OEMs want domestic origin.

**Who is already doing this:** Rochester Electronics (die/wafer banking and licensed re-creation, Newburyport MA), Micross (die banking), distributor bonded-inventory programs (Arrow, Avnet), HTV long-term storage (Germany) [UNVERIFIED-training]; lifecycle-data tools SiliconExpert and Z2Data.

**Wins on which axis, for which buyer:** Lifecycle length / supply security — for Mid-size OEMs with 10-30-year field lives (industrial PCs, rail signaling, grid-protection relays, medical imaging, avionics retrofit) too small for Rochester's re-creation programs

**Survives a 2029 glut?:** yes — Demand is EOL-driven, not price-driven; in a glut OEMs can afford bigger last-time buys, which raises inventory under management.

**Fatal-flaw candidate:** Trust and scale: OEMs hand $0.5-2M of critical inventory only to a vault with a track record and insurance, incumbents (Rochester, Micross, big distributors) already bank parts, and breakeven needs ~8-10 OEMs.

*Possible?* yes - component long-term storage and die banking exist · *Profitable?* marginal - ~70% GM at 25 OEMs, losses below ~8 · *Doable by this founder?* marginal - software-first start is feasible; the vault needs a partner or hire

*Business-model lenses:* SaaS + recert/brokerage (storage service), defense-first niche optional

### C-62 — ProvenRAM: graded, serialized recovered server RDIMMs

*Sub-branch:* Recertified / recovered DRAM (module level) · *Materials sense:* c-capital

**What it is:** Buy decommissioned DDR4 (and first-wave DDR5) RDIMM lots from R2v3/e-Stewards ITADs (Iron Mountain/ITRenew-Sesame, Sims Lifecycle, SK tes, regional R2 firms [UNVERIFIED-training]), test each module on owned DDR4 server beds (memtest86+ plus Google stressapptest at temperature) and a bench SPD/pattern tester, grade it, laser-label a serial, and sell with a public per-serial test record through B2B channels (third-party maintenance, refurbishers, small cloud/HPC operators, labs) and eBay. 'Cheaper capital' here is silicon someone else already paid for.

**Why it could work:** DRAM is volatile, so modules need no data destruction, and a used RDIMM sells far below new while new DDR4 chips trade at $16-44/GB. Model (Appendix A): at $4-10/GB used resale, contribution is $21-101 per 32GB module (17-32%, eBay vs B2B); $20k of inventory turned twice a month yields ~$12k/month contribution. The test stack is free and current (memtest86+ last commit 2026-10-28 with USB reports; stressapptest Apache-2.0).

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [memtest86plus/memtest86plus (GitHub; README, system/jedec_id.h, system/spd.c, app/reports.c)](https://github.com/memtest86plus/memtest86plus) — industry, 2026-10-28. OPENED by C via git clone: GPLv2 tester, active (last commit 2026-10-28); USB/serial reports log SPD vendor, SKU, ECC and per-test results; JEP106 table includes CXMT 0x0A11, YMTC 0x091B, GigaDevice 0x0648; reads the module-maker ID (DDR4 SPD 320-321, DDR5 512-513) but not the DRAM-die manufacturer field
  - [stressapptest/stressapptest (GitHub README)](https://github.com/stressapptest/stressapptest) — industry, 2024-08-05. OPENED by C via git clone: Google's Apache-2.0 memory-interface stress test, used at Google, for system-level burn-in
  - [RAM market update (BuySellRAM)](https://www.buysellram.com/blog/ram-market-update/) — industry, 2026-08-31. DRAMeXchange 2026-08-31: DDR4 8Gb avg $44.37, DDR5 16Gb avg $53.92; BuySellRAM is itself a U.S. used-memory buyer (comparable) (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [DDR4 fixed price bottoms (KED Global)](https://www.kedglobal.com/korean-chipmakers/newsView/ked202310040013) — news, 2023-10-04. DDR4 8Gb fixed price bottomed at $1.30 in Sep 2023: the trough a recovered-DRAM or legacy-supply business must survive (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [DDR4 memory prices now also rise as DRAM supply shortages intensify through 2028 (Barclays)](https://www.guru3d.com/story/ddr4-memory-prices-now-also-rise-as-dram-supply-shortages-intensify-through-2028/) — news, 2026-10. DDR4 contract +24% over 3 months to Oct 2026; shortage seen into 2028 (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Mobius Materials raises $3M (PR Newswire)](https://www.prnewswire.com/news-releases/mobius-materials-raises-3m-to-combat-one-of-manufacturings-biggest-issues-amid-us-china-trade-tariffs-302643403.html) — news, 2025-12. Richmond VA authenticated B2B secondary marketplace for components, ML-authentication patent filed: the closest venture-backed comparable (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)

**Capital tier:** T0 | **Time to first revenue:** 2-4 months (first ITAD lot, test bench, eBay and two B2B accounts) | **Gross margin estimate:** 17-32% now (eBay vs B2B); 13-28% in the A-05 glut only if buy prices reprice instantly; ~0% on eBay in a 2023-like trough

**US manufacturability:** U.S. test-and-grade bench in East Coast flex space; the U.S. value-add is testing and documentation, not manufacturing.

**Who is already doing this:** ServerMonkey, Memory4Less, TechMikeNY (NYC), BuySellRAM, Curvature/Park Place, ITADs selling direct, Mobius Materials (authenticated marketplace, Richmond VA) and thousands of eBay sellers.

**Wins on which axis, for which buyer:** $/GB (used at roughly 25-60% of new) plus documented test provenance — for Third-party maintenance firms keeping DDR4 fleets alive, small cloud/HPC/CPU-offload inference operators, university labs; not DoD (DFARS 252.246-7008 / FAR 52.211-5 bar used parts without contracting-officer approval [UNVERIFIED-training])

**Survives a 2029 glut?:** partially — Dollar contribution per module falls ~55-60% with resale prices and inventory loses value during the fall; the trading business shrinks to a niche unless the serialized test-record layer becomes the product (it feeds C-64).

**Fatal-flaw candidate:** No moat and a closing window: hyperscalers increasingly reuse DDR4 internally behind CXL, ITADs sell direct, and the margin is a bet on DDR4 prices that peak in 2026-27.

*Possible?* yes - an existing U.S. trade · *Profitable?* yes now / marginal in a glut - ~20-30% contribution in 2026, thin and volume-hungry later · *Doable by this founder?* yes - $20-40k start, evenings and weekends

*Business-model lenses:* recert/brokerage, SaaS (test-record ledger), data product (graded-price index)

### C-63 — Die harvesting and module rebuild from e-waste, Shenzhen-style (tempting, dead)

*Sub-branch:* Recovered DRAM (chip level) · *Materials sense:* c-capital

**What it is:** Desolder DRAM packages from scrapped DIMMs, laptops and phones, clean and reball them, re-test them, and mount them on new consumer UDIMM/SODIMM boards in a U.S. shop, copying the Huaqiangbei 'recycled chip' trade.

**Why it could work:** At 2026 prices a harvested DDR4 8Gb chip valued at 35% of new is worth ~$5.6-7.4 against ~$3.6 of rework cost (Appendix A), and high-density DDR3 is in acute shortage.

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [DDR4 reportedly leads legacy memory rally with Q1 prices up to 50%; DDR3 in tight supply](https://www.trendforce.com/news/2026/01/19/news-ddr4-reportedly-leads-legacy-memory-rally-with-q1-prices-up-to-50-ddr3-in-tight-supply/) — news, 2026-01-19. Makers preparing to exit DDR4 in 2026; high-density DDR3 in acute shortage (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [RAM market update (BuySellRAM)](https://www.buysellram.com/blog/ram-market-update/) — industry, 2026-08-31. DRAMeXchange 2026-08-31: DDR4 8Gb avg $44.37, DDR5 16Gb avg $53.92; BuySellRAM is itself a U.S. used-memory buyer (comparable) (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [DDR4 fixed price bottoms (KED Global)](https://www.kedglobal.com/korean-chipmakers/newsView/ked202310040013) — news, 2023-10-04. DDR4 8Gb fixed price bottomed at $1.30 in Sep 2023: the trough a recovered-DRAM or legacy-supply business must survive (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Champion Spark Plug Co. v. Sanders, 331 U.S. 125 (1947); 18 U.S.C. 2320; SAE AS6171]() — government, 1947 / 2011 / 2016. [UNVERIFIED-training] citation from C's training data (to ~mid-2026). No URL could be opened or seen this session (WebSearch budget exhausted; WebFetch DNS-blocked). Verify agent: add a URL or downgrade. Reconditioned goods may keep the original mark only if clearly disclosed as used/repaired; trafficking in counterfeit goods (incl. remarked parts sold as new) is a felony; AS6171 inspection flags reworked/reballed parts as suspect counterfeits.

**Capital tier:** T0 | **Time to first revenue:** 2-4 months technically; commercially blocked | **Gross margin estimate:** ~20-35% per chip at 2026 prices before module build cost and 5-10% reball fallout; negative in the A-05 glut

**US manufacturability:** Possible with a BGA rework station and X-ray in any U.S. shop; uncompetitive on labor versus Shenzhen.

**Who is already doing this:** Shenzhen/Huaqiangbei refurbishers; in the U.S. only disclosed board-level repair shops.

**Wins on which axis, for which buyer:** $/GB (nominal) — for Price-sensitive consumer and legacy-platform buyers

**Survives a 2029 glut?:** no — Harvested-chip value ($2.5 at the A-05 glut) falls below rework cost ($3.6).

**Fatal-flaw candidate:** Geometry and law: server RDIMMs carry x4 dies that only fit other RDIMMs, an intact tested 32GB module is worth ~2.7x its harvested chips ($192 vs ~$72), reballed parts read as counterfeits under AS6171, and selling them as new is a crime under 18 U.S.C. 2320. The only surviving fragment - disclosed BGA repair of failed RDIMMs with tested donor chips - is folded into C-62.

*Possible?* yes - done at scale in China · *Profitable?* no - in the U.S. at U.S. labor rates and legal standards · *Doable by this founder?* no - legal exposure outweighs any margin

*Business-model lenses:* recert/brokerage

### C-64 — CleanBOM-5949: memory-provenance verification for federal IT sellers

*Sub-branch:* Government preference as moat (NDAA Sec. 5949 compliance) · *Materials sense:* none · *Merged from:* C.07, D.11

**What it is:** A subscription service plus bootable fleet-scan tool that proves the DRAM and NAND in servers, PCs and appliances sold to federal agencies contain no CXMT/YMTC/SMIC silicon before the FY2023 NDAA Sec. 5949 ban takes effect (2027-12-23). It combines SPD scans (module and DRAM-die JEP106 IDs, part numbers, date codes), a module-part-number-to-die-source cross-reference, supplier attestations, and sampled X-ray/decap die identification at a partner AS6171 lab, packaged as a per-SKU attestation; priced $1.5k-12k per month by tier plus lab pass-through.

**Why it could work:** Sec. 5949 pays for 'verified non-Chinese', not 'U.S.-made'. CXMT reached ~9.5% of DRAM revenue in 2Q26 and is growing (320k to 420k wpm); Apple lobbied to buy CXMT and tested its DRAM; Chinese die also ships under other brands (GigaDevice DDR4 is CXMT-fabbed [UNVERIFIED-training]), so labels do not prove origin. The scan tool can start from memtest86+ (GPLv2), whose JEP106 table already includes CXMT (0x0A11) and YMTC (0x091B) but which reads only the module-maker ID, not the DRAM-die field - a concrete gap a software founder can fill. Model: 37 customers -> ~$1.7M revenue at ~72% GM; deadline 417 days away.

**Evidence:** TRL 7 · Rule 1: SUPPORTED
  - [Apple, China memory and the 2027 federal procurement ban (XenoSpectrum)](https://xenospectrum.com/en/apple-china-memory-federal-procurement-ban-2027/) — news, 2026-07. FY2023 NDAA Sec. 5949 bars federal procurement of products containing CXMT/YMTC/SMIC chips from Dec 2027 (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Apple lobbying U.S. for approval to buy blacklisted CXMT memory chips](https://thenextweb.com/news/apple-lobbying-us-approval-cxmt-blacklisted-memory-chips) — news, 2026-06-27. Apple lobbied Commerce to approve CXMT DRAM: CXMT silicon is entering U.S.-brand products (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Apple tests CXMT memory (Gigazine)](https://gigazine.net/gsc_news/en/20260810-apple-tests-cxmt/) — news, 2026-08-10. Apple reportedly testing CXMT DRAM (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [memtest86plus/memtest86plus (GitHub; README, system/jedec_id.h, system/spd.c, app/reports.c)](https://github.com/memtest86plus/memtest86plus) — industry, 2026-10-28. OPENED by C via git clone: GPLv2 tester, active (last commit 2026-10-28); USB/serial reports log SPD vendor, SKU, ECC and per-test results; JEP106 table includes CXMT 0x0A11, YMTC 0x091B, GigaDevice 0x0648; reads the module-maker ID (DDR4 SPD 320-321, DDR5 512-513) but not the DRAM-die manufacturer field
  - [TrendForce data: Samsung 39.4%, SK hynix 24.9% (Herald)](https://biz.heraldcorp.com/article/10866656) — news, 2026-09-07. CXMT reached 9.5% of DRAM revenue in 2Q26 (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Schumer demands Apple reject Chinese military-linked chips](https://www.schumer.senate.gov/newsroom/press-releases/citing-core-national-security-and-economic-reasons-schumer-demands-apple-reject-chinese-military-linked-chips) — government, 2026-07-30. Senators demand Apple commit not to use CXMT/YMTC: provenance is a live political issue (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [SpecTek PT040-56B DDR5 DRAM (Micron 1a) floorplan analysis (TechInsights)](https://www.techinsights.com/blog/spectek-pt040-56b-ddr5-dram-micron-1a-memory-floorplan-analysis) — industry, 2023. SpecTek parts carry current Micron 1-alpha die; die-level teardown identification is a commercial service (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [memtest86+ JEP106 table](https://raw.githubusercontent.com/memtest86plus/memtest86plus/main/system/jedec_id.h) — industry, 2026-09. Based on JEP106BP (Sep 2026): CXMT = 0x0A11, YMTC = 0x091B.
  - [memtest86+ SPD decoder](https://raw.githubusercontent.com/memtest86plus/memtest86plus/main/system/spd.c) — industry, 2026. Reads the manufacturer JEP106 ID from SPD (DDR5 bytes 512-513, DDR4 bytes 320-321) plus date code and part number.

**Capital tier:** T0 | **Time to first revenue:** 6-12 months (scan-tool MVP and pilot attestations for 3-5 GSA/SEWP resellers before the Dec 2027 effective date) | **Gross margin estimate:** 65-75% (software plus marked-up lab pass-through)

**US manufacturability:** Software and services; physical die-ID sampling at U.S. independent counterfeit-test labs; no fab dependency (rubric: software/services).

**Who is already doing this:** No memory-specific Sec. 5949 product known to C [UNVERIFIED]. Adjacent: supply-chain-illumination vendors (Exiger, Interos, Govini), component-risk data (SiliconExpert/Arrow, Z2Data), teardown die-ID (TechInsights), counterfeit-test labs, OEM self-attestation (Dell, HP, Lenovo), Mobius Materials (ML authentication).

**Wins on which axis, for which buyer:** Supply security / provenance assurance — for GSA MAS IT and NASA SEWP resellers, federal systems integrators and appliance OEMs selling to agencies; later critical-infrastructure buyers that copy the federal rule

**Survives a 2029 glut?:** yes — Demand is set by statute, not DRAM prices; in a glut CXMT's cheap bits gain share, which raises contamination risk and verification demand.

**Fatal-flaw candidate:** The FAR implementing rule may accept a plain supplier representation (as Section 889's FAR 52.204-24/-26 does), letting OEMs self-attest and leaving little paid demand for independent verification; big compliance-data vendors can also bolt on a CXMT flag.

*Possible?* yes - SPD reads and die-ID teardowns are routine; the integration is new · *Profitable?* marginal - ~70% GM, but willingness to pay hinges on the unpublished FAR rule text · *Doable by this founder?* yes - T0 software-plus-partner-lab start, part-time feasible

*Business-model lenses:* SaaS, data product, defense-first

### C-65 — U.S. hi-rel DDR4/LPDDR4 multi-chip memory design house

*Sub-branch:* Packaging-only: hi-rel MCM from purchased KGD · *Materials sense:* c-capital

**What it is:** Design rugged x72 ECC DDR4 (e.g. 8GB from 9 x 8Gb x8 KGD) and LPDDR4X memory MCMs in 20-30 mm BGAs for defense, space and rugged-industrial processors, buying known-good die from Winbond, ESMT or Micross (Micron silicon where SpecTek/Micross can supply) and assembling and screening at U.S. hi-rel OSATs (Micross Apopka FL / RTP NC, QP Technologies CA, Integra Wichita KS [UNVERIFIED-training sites]).

**Why it could work:** Hi-rel memory MCMs sell at 10-100x commodity $/bit, and die is under 15% of the price. Model: ~$457 unit cost vs $800-3,000 ASP (43-85% GM); ~$1.5M NRE recovered after ~1,400 units at $1,500. DoD keeps funding memory packaging (DARPA DV017, ~$1.2M Direct-to-Phase-II, 2026).

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [Micross die and wafer flyer](https://micross.com/uploads/05827c98-1b61-4d4d-bb3c-04dc1b207e5a/Die_and_Wafer_Flyer_Rev_1_WEB.pdf) — company, unknown. Micross is the largest authorized bare-die/wafer supplier, with DRAM on its die line card; also a U.S. hi-rel packager (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Winbond KGD (customized memory solution)](https://winbond.com/hq/product/customized-memory-solution/kgd/) — company, unknown. Winbond sells DRAM known-good die to SiP makers: an open legacy KGD source (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [ESMT Known Good Die](https://esmt.com.tw/en/Applications/Known-Good-Die) — company, unknown. ESMT offers DRAM KGD (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [JESD49B.01 Procurement Standard for Known Good Die](https://www.jedec.org/node/8358) — industry, 2023-10. JEDEC procurement standard governing KGD quality and test claims (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Non-Volatile Memory for Extreme Environments (DARPA SBIR DPA26BZ04-DV017)](https://www.darpa.mil/research/programs/non-volatile-memory-extreme-environments) — government, 2026-07. DoD funds co-packaged extreme-environment memory systems (~$1.2M Direct-to-Phase-II, opened 2026-07-22) (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)

**Capital tier:** T2 | **Time to first revenue:** 24-36 months (substrate design, SI/PI, environmental qualification, design-in at a prime) | **Gross margin estimate:** 43-85% depending on ASP ($800-3,000)

**US manufacturability:** Yes: U.S. hi-rel OSATs assemble and screen memory die today; die is imported (Taiwan) or Micron via SpecTek/Micross.

**Who is already doing this:** Micross, Mercury Systems (Phoenix), Data Device Corp (Bohemia NY), Frontgrade, Teledyne e2v, 3D Plus (HEICO), Intelligent Memory [UNVERIFIED-training].

**Wins on which axis, for which buyer:** Lifecycle length, environmental ruggedness, traceability — for Defense primes' mission computers, NewSpace avionics, rugged industrial system-on-modules

**Survives a 2029 glut?:** yes — Priced on qualification and heritage, not bits; die cost is a small share of ASP.

**Fatal-flaw candidate:** A 2-3-year qualification and design-in cycle at primes plus incumbents with flight and field heritage: a startup with no heritage sells nothing within 18 months.

*Possible?* yes - incumbents ship these · *Profitable?* yes - for incumbents with heritage · *Doable by this founder?* no - hardware team and qualification timeline

*Business-model lenses:* module/appliance, defense-first

### C-66 — High-capacity stacked-die legacy modules (32GB DDR3 RDIMM, 32GB DDR3L SODIMM)

*Sub-branch:* Packaging-only: stacked-die legacy capacity · *Materials sense:* mixed:b+c

**What it is:** Use wire-bonded dual-die packages of legacy 4Gb DDR3 (and 8Gb DDR4) KGD from Winbond or Nanya to build capacities the majors never made or have stopped making - e.g. 32GB DDR3 RDIMM for legacy Xeon E5 and telecom platforms, 32GB DDR3L SODIMM for industrial PCs - with DDP assembly at an Asian OSAT or Micross and module SMT at a U.S. EMS.

**Why it could work:** High-density DDR3 is in acute shortage (TrendForce, Jan 2026) and DDR3 4Gb costs ~$20/GB (June 2026 contract) to ~$25/GB (July spot). Model: a 32GB DDR3 RDIMM costs ~$788 (die $720, DDP $43) and sells ~$985 at a 25% markup.

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [DDR4 reportedly leads legacy memory rally with Q1 prices up to 50%; DDR3 in tight supply](https://www.trendforce.com/news/2026/01/19/news-ddr4-reportedly-leads-legacy-memory-rally-with-q1-prices-up-to-50-ddr3-in-tight-supply/) — news, 2026-01-19. Makers preparing to exit DDR4 in 2026; high-density DDR3 in acute shortage (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [TrendForce price page snapshot](https://www.trendforce.com/price) — industry, 2026-06-18. DDR3 4Gb $10.00 and DDR4 8Gb $16.00 (June 2026) - legacy DRAM is priced at $16-20/GB (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Memory shortages drive DDR4 prices over 50% in Q3 2026; DDR3 also impacted](https://wccftech.com/memory-shortages-drive-ddr4-prices-over-50-in-q3-2026-ddr3-also-impacted-by-higher-costs/) — news, 2026-07. Early-July 2026 spot DDR3 4Gb ~$3.19/Gb (~$25/GB), above DDR5 16Gb (~$2.94/Gb) (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Winbond KGD (customized memory solution)](https://winbond.com/hq/product/customized-memory-solution/kgd/) — company, unknown. Winbond sells DRAM known-good die to SiP makers: an open legacy KGD source (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)

**Capital tier:** T1 | **Time to first revenue:** 12-18 months (DDP qualification, per-platform BIOS/SI validation) | **Gross margin estimate:** 15-25%

**US manufacturability:** Partial: DDP stacking in the U.S. only at low-volume hi-rel houses (Micross); otherwise Asia; module SMT at any U.S. EMS.

**Who is already doing this:** Intelligent Memory (high-capacity DDR3/DDR4 via stacked dies [UNVERIFIED-training]), Alliance Memory, Virtium, ATP.

**Wins on which axis, for which buyer:** Density (GB per legacy slot) / platform-life extension — for Telecom/network-equipment operators, industrial-PC fleets, legacy-server owners

**Survives a 2029 glut?:** no — DDR3 platforms retire and DDR3 falls back toward ~$3/GB; the module's value drops ~75% (Appendix A stress case) and the premium disappears.

**Fatal-flaw candidate:** A shrinking installed base, an incumbent (Intelligent Memory), and per-platform signal-integrity/BIOS validation that a small team cannot amortize.

*Possible?* yes - Intelligent Memory ships the category · *Profitable?* marginal - thin margins on a shrinking base · *Doable by this founder?* no - hardware engineering and die access

*Business-model lenses:* module/appliance

### C-67 — Rugged and new-form-factor memory modules built at a U.S. EMS (LPCAMM2/CAMM2, wide-temp coated SODIMM)

*Sub-branch:* Packaging-only: custom module formats · *Materials sense:* c-capital

**What it is:** Design and qualify rugged memory modules - wide-temperature (-40 to 95 C) screened, conformal-coated and underfilled DDR5 SODIMMs and LPCAMM2/CAMM2 modules (JEDEC CAMM2 [UNVERIFIED-training]) - built at a U.S. EMS from authorized Micron industrial-temperature components (Manassas-made DDR4/LPDDR4 where possible) for rugged laptops, embedded SBCs and VPX mission computers.

**Why it could work:** Rugged buyers pay 1.3-1.6x commodity; Micron is steering its U.S.-made DDR4/LPDDR4 at exactly these defense, automotive and industrial buyers; CAMM-class modules are new and supplier-thin. Model: 16GB DDR5 rugged SODIMM GM 20-35% now, 10-27% in the A-05 glut.

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [Micron LPDDR4 components](https://micron.net/products/memory/dram-components/lpddr4) — company, unknown. Micron LPDDR4/4X in many packages and industrial/automotive temperature grades: authorized component supply for rugged modules (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Micron advances Made-in-America memory with manufacturing expansion in Virginia](https://www.hpcwire.com/off-the-wire/micron-advances-made-in-america-memory-with-manufacturing-expansion-in-virginia) — company, 2026-05-22. Micron Manassas Fab 6 began 1-alpha DDR4/LPDDR4 on 2026-05-22 for auto, defense, aerospace and industrial buyers, in a >$2B expansion that quadruples its DDR4 wafer supply (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Response measures to Samsung DDR4 IC EOL announcement (Advantech)](https://www.advantech.com/en/resources/news/response-measures-to-samsung-ddr4-ic-eol-announcement) — company, 2025. Industrial-PC maker tells customers DDR4 supply runs to ~end-2026 and to avoid Samsung DDR4 in new designs: long-lifecycle buyers are actively managing EOL (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)

**Capital tier:** T1 | **Time to first revenue:** 12-24 months (design, environmental qualification, first design win at a rugged-computer maker) | **Gross margin estimate:** 20-35% now; 10-27% in the A-05 glut

**US manufacturability:** U.S. EMS lines (any IPC-A-610 Class 3 shop) plus Micron Manassas components; conformal coating and screening are routine U.S. services.

**Who is already doing this:** Virtium, SMART Modular (Penguin), Mercury Systems, ATP, Innodisk, Swissbit, Cervoz; Micron, Samsung and SK hynix make LPCAMM2/SOCAMM-class modules themselves [UNVERIFIED-training].

**Wins on which axis, for which buyer:** Environmental reliability, lifecycle, form factor — for Rugged-computer makers (General Micro Systems, Crystal Group, Curtiss-Wright, Kontron-class) and defense primes

**Survives a 2029 glut?:** partially — The ruggedization premium persists, but the module price tracks DRAM down, so dollar margin shrinks ~55%.

**Fatal-flaw candidate:** Crowded by funded specialists (Virtium, SMART, ATP, Innodisk) that need the same component allocation, while design wins take 12-24 months and memory makers ship CAMM-class modules themselves.

*Possible?* yes - shipping category · *Profitable?* marginal - 20-35% against strong incumbents · *Doable by this founder?* marginal - needs one hardware cofounder

*Business-model lenses:* module/appliance, defense-first

### C-68 — HBM-adjacent U.S. test and rework services near Amkor Peoria / SK hynix West Lafayette (dead for this founder)

*Sub-branch:* Packaging-only: HBM adjacency · *Materials sense:* c-capital

**What it is:** Stand up known-good-stacked-die (KGSD) test, HBM-stack failure analysis and rework, or thermal-compression-bonding consumables near Amkor's Peoria AZ 2.5D campus and SK hynix's West Lafayette IN HBM packaging plant, to serve them as they ramp.

**Why it could work:** HBM takes ~3x DDR5 wafer area per bit, its prices keep rising (HBM4 2027 ~$4-5/Gb), and U.S. HBM packaging is coming: SK hynix Indiana targets HBM4E mass production in Q3 2029; Micron's U.S. HBM packaging follows its second Idaho fab (late 2028+).

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [SK hynix breaks ground on $4 billion packaging facility in Indiana](https://evertiq.com/news/2026-08-28-sk-hynix-breaks-ground-on-4-billion-packaging-facility-in-indiana) — news, 2026-08-28. SK hynix HBM packaging plant in West Lafayette IN; cleanroom target Oct 2028 (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [SK hynix Indiana plant (Herald Business)](https://mbiz.heraldcorp.com/article/10853891) — news, 2026-08. HBM4E mass production in Indiana from Q3 2029 (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Micron Technology Form 10-K FY2026](https://www.sec.gov/Archives/edgar/data/0000723125/000072312526000023/mu-20260903.htm) — company, 2026-10. Micron cites supply-allocation decisions that may affect some customers; plans U.S. HBM packaging (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Micron says the silicon gap between HBM and DDR5 is widening](https://www.tomshardware.com/tech-industry/semiconductors/micron-says-the-silicon-gap-between-hbm-and-ddr5-is-widening-with-every-generation) — news, 2026. HBM needs ~3x DDR5 wafer area per bit (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Lutnick memory tariff ultimatum (Taipei Times)](https://www.taipeitimes.com/News/biz/archives/2026/01/19/2003850817) — news, 2026-01-19. SK hynix Indiana is packaging only; no U.S. front-end DRAM from Korean makers (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Samsung HBM4 2027 pricing set to more than double (Silicon Analysts)](https://siliconanalysts.com/market/samsung-hbm4-2027-pricing-set-to-more-than-double-2026-10-07) — industry, 2026-10-07. HBM4 2027 forecast $4.00-5.00/Gb (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)

**Capital tier:** T3 | **Time to first revenue:** ~2029-30, when the captive plants ramp | **Gross margin estimate:** 20-40% (test-services norm)

**US manufacturability:** Arizona/Indiana from 2028-29, but both plants are captive and arrive with their own Advantest/Teradyne HBM testers ($3-5M each [ESTIMATE]) and Korean/Taiwanese supplier ecosystems.

**Who is already doing this:** SK hynix, Micron and Samsung in-house; Amkor, SPIL, ASE; Advantest, Teradyne, FormFactor; Hanmi, Hanwha and ASMPT for TC bonders [UNVERIFIED-training].

**Wins on which axis, for which buyer:** Bandwidth supply (HBM) via local proximity — for SK hynix Indiana, Micron Idaho, Amkor Arizona

**Survives a 2029 glut?:** partially — HBM demand is structural (AI), but a 2028-29 glut would hit HBM pricing too, and captive plants insource first.

**Fatal-flaw candidate:** Captive, capital-heavy and late: no outside customer exists before 2028-29, the first customers bring incumbent suppliers, and the ticket is tens of millions.

*Possible?* yes - for SK hynix/Amkor/Advantest · *Profitable?* marginal - only for incumbents · *Doable by this founder?* no

*Business-model lenses:* module/appliance (services), defense-first not applicable

### C-69 — U.S. known-good-die wafer-probe and die-processing house for legacy DRAM

*Sub-branch:* Packaging-only: KGD test · *Materials sense:* c-capital

**What it is:** Buy used DRAM ATE (older Advantest T55xx-class [UNVERIFIED-training]) and a 300mm prober, and offer wafer-level probe, speed-binning and burn-in that turns untested or partially tested legacy DRAM wafers (SpecTek, Winbond, ESMT) into JESD49B.01-compliant known-good die for U.S. hi-rel MCM and SiP makers.

**Why it could work:** Bare die is the U.S. back-end choke point and KGD carries a 15-40% premium over packaged $/GB. Model: ~$750k startup capex; losses below ~700 wafers per year at $600/wafer; ~$375k contribution at 1,500 wafers.

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [JESD49B.01 Procurement Standard for Known Good Die](https://www.jedec.org/node/8358) — industry, 2023-10. JEDEC procurement standard governing KGD quality and test claims (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [SpecTek support (Micron)](https://micron.net/sales-support/customer-support/spectek-support) — company, unknown. SpecTek sells Micron DRAM/LPDRAM in BGA packages and in wafer form (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Micross die and wafer flyer](https://micross.com/uploads/05827c98-1b61-4d4d-bb3c-04dc1b207e5a/Die_and_Wafer_Flyer_Rev_1_WEB.pdf) — company, unknown. Micross is the largest authorized bare-die/wafer supplier, with DRAM on its die line card; also a U.S. hi-rel packager (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Winbond KGD (customized memory solution)](https://winbond.com/hq/product/customized-memory-solution/kgd/) — company, unknown. Winbond sells DRAM known-good die to SiP makers: an open legacy KGD source (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Etron Memory ICs - KGDM](https://etron.com/kgdm/) — company, unknown. Etron, a fabless Taiwanese specialty-DRAM company, sells KGD memory (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)

**Capital tier:** T1 | **Time to first revenue:** 12-18 months (tool install, probe cards and test programs per die type) | **Gross margin estimate:** negative below ~700 wafers/yr; ~40% at 1,500

**US manufacturability:** Yes in principle: any U.S. light-industrial cleanroom; probe cards and test programs cost $50-150k per die type [ESTIMATE].

**Who is already doing this:** Micross (die processing, Apopka FL), Rochester Electronics, ISE Labs (Fremont, ASE), Integra, Silicon Turnkey Solutions, and the die vendors' own KGD programs [UNVERIFIED-training].

**Wins on which axis, for which buyer:** Supply security of tested die inside the U.S. — for Micross/Mercury/DDC-class MCM makers and SiP startups

**Survives a 2029 glut?:** partially — Defense demand is steady, but volume is tiny and vendors bundle KGD test themselves when capacity frees up in a glut.

**Fatal-flaw candidate:** Demand is a few hundred wafers a year, Winbond/ESMT/Etron already ship tested KGD, and untested DRAM wafers are mostly not sold to outsiders, so the house would sit idle.

*Possible?* yes · *Profitable?* no - below breakeven volume for the foreseeable market · *Doable by this founder?* no

*Business-model lenses:* module/appliance (test services), defense-first

### C-70 — All-domestic DRAM component: Micron Manassas wafer to U.S. package to U.S. module

*Sub-branch:* Module assembly and test in the U.S. (domestic-origin) · *Materials sense:* c-capital

**What it is:** Obtain Micron 1-alpha DDR4/LPDDR4 wafers or KGD made at Manassas Fab 6 (via SpecTek or a direct program), package and test them in the U.S. (Micross FL/NC, Integra KS or QP Technologies CA), and sell the only fully U.S.-origin DRAM component and module - eligible for an unqualified FTC 'Made in USA' claim and for programs that demand domestic end-to-end sourcing.

**Why it could work:** Manassas wafers are, as far as C knows, packaged offshore today, so no fully domestic DRAM component exists [UNVERIFIED-training]; Micron took $275M of CHIPS money to onshore exactly this silicon; the BAA domestic-content threshold for non-COTS items rises to 75% in 2029 [UNVERIFIED-training]; and SpecTek already sells Micron silicon in wafer form.

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [Micron advances Made-in-America memory with manufacturing expansion in Virginia](https://www.hpcwire.com/off-the-wire/micron-advances-made-in-america-memory-with-manufacturing-expansion-in-virginia) — company, 2026-05-22. Micron Manassas Fab 6 began 1-alpha DDR4/LPDDR4 on 2026-05-22 for auto, defense, aerospace and industrial buyers, in a >$2B expansion that quadruples its DDR4 wafer supply (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [CHIPS: Micron Manassas preliminary memorandum of terms](https://www.nist.gov/node/1869301) — government, 2024-12-10. Up to $275M CHIPS funding for Micron Manassas onshoring of 1-alpha DRAM (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [SpecTek support (Micron)](https://micron.net/sales-support/customer-support/spectek-support) — company, unknown. SpecTek sells Micron DRAM/LPDRAM in BGA packages and in wafer form (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Micross die and wafer flyer](https://micross.com/uploads/05827c98-1b61-4d4d-bb3c-04dc1b207e5a/Die_and_Wafer_Flyer_Rev_1_WEB.pdf) — company, unknown. Micross is the largest authorized bare-die/wafer supplier, with DRAM on its die line card; also a U.S. hi-rel packager (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [What U.S. tariff push means for Korea's semiconductor industry](https://www.koreatimes.co.kr/opinion/20260915/what-us-tariff-push-means-for-koreas-semiconductor-industry) — news, 2026-09-15. Korean memory excluded from Section 232 phase 1: no tariff-created U.S.-origin premium for memory today (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)

**Capital tier:** T2 | **Time to first revenue:** 24-36 months (Micron program agreement, U.S. FBGA package qualification, first program design-in) | **Gross margin estimate:** 20-40% if a domestic-origin premium of 1.5-3x exists; ~0% if not

**US manufacturability:** Fully U.S.: Manassas VA wafers, Micross/Integra packaging and test, U.S. EMS modules.

**Who is already doing this:** Micron (could do it itself at any time), Micross (hi-rel packaging of purchased die).

**Wins on which axis, for which buyer:** Supply security / domestic origin — for DoD programs with domestic or trusted-sourcing clauses, critical-infrastructure agencies, a 'Made in USA' consumer niche

**Survives a 2029 glut?:** partially — A domestic-origin premium is policy-driven and would survive, but the volume is small and commodity alternatives get cheaper.

**Fatal-flaw candidate:** Gatekeeper risk: Micron decides whether Manassas silicon reaches outsiders in wafer form, and a paid premium for U.S.-packaged COTS DRAM is unproven because TAA/BAA treat Taiwan and Korea as compliant and memory carries no Section 232 tariff.

*Possible?* marginal - depends entirely on Micron releasing Manassas wafers · *Profitable?* marginal - premium unproven · *Doable by this founder?* no

*Business-model lenses:* module/appliance, defense-first

### C-71 — Trusted low-density SDRAM (64-512Mb) on SkyWater Fab 25 with 1T1C MIM cells

*Sub-branch:* Trailing-node DRAM on a U.S. pure-play foundry · *Materials sense:* mixed:b+c

**What it is:** Develop a 256Mb SDR/DDR SDRAM using a 1T1C high-k MIM-capacitor module on SkyWater's 65nm-class 200mm Fab 25 (Austin, ex-Infineon) or its DMEA-trusted Bloomington line, packaged in JEDEC TSOP/FBGA at a U.S. OSAT, as a trusted, U.S.-fabbed DMSMS replacement for obsolete SDRAM in avionics and weapons systems.

**Why it could work:** DoD platforms run 30-50 years; SkyWater integrates outside memory modules (Weebit ReRAM qualified in S130) and bought Fab 25 cheaply (~400k wafer starts/yr); Infineon already keeps legacy Cypress parts in U.S. production there. Model: 116 mm2 die, ~137 good die per 200mm wafer, ~$30 per unit including package and test.

**Evidence:** TRL 3 · Rule 1: SUPPORTED
  - [SkyWater to acquire Infineon's Austin fab](https://www.businesswire.com/news/home/20250226773415/en/SkyWater-to-Acquire-Infineons-Austin-Fab-and-Establish-Strategic-Partnership-to-Expand-U.S.-Foundry-Capacity-for-Foundational-Chips) — company, 2025-02-26. SkyWater buys Infineon Fab 25 (200mm, 130-65nm) with a long-term supply agreement (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [SkyWater acquires Infineon's 200mm fab (LaPedus)](https://marklapedus.substack.com/p/skywater-acquires-infineons-200mm) — news, 2025. Fab 25 ~400k wafer starts/yr; deal closed 2025-06-30 (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Infineon retains U.S. manufacturing via SkyWater supply agreement](https://new-origin.infineon.com/cms/en/about-infineon/press/press-releases/2025/INFXX202502-066.html) — company, 2025-02-26. Legacy Cypress products keep U.S. wafer supply at SkyWater: precedent for U.S. legacy-part continuity on a pure-play foundry (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Weebit Nano ReRAM IP fully qualified in SkyWater S130](https://www.weebit-nano.com/news/press-releases/weebit-nanos-reram-ip-now-fully-qualified-in-skywater-technologys-s130-process/) — company, 2023-06. SkyWater integrates and qualifies outside memory modules (256Kb ReRAM in S130) (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Facing radiation challenges head on (Sandia)](https://www.sandia.gov/research/news/evolving-semiconductor-technology-for-national-security-applications/) — government, 2026-05-13. HZO FeRAM integrated into Sandia's trusted MESA fab: trusted-fab memory is done, but by the government for itself (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Winbond launches 32-bit SDR/DDR KGD for SiP applications](https://www.winbond.com/hq/about-winbond/news-and-events/news/winbond-launchs-32bit-sdr-ddr-kgd-for-SiP-application.html) — company, unknown. Low-density SDR/DDR DRAM is still made and sold (as KGD) by Winbond (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)

**Capital tier:** T2 | **Time to first revenue:** 36-60 months (capacitor-module development, design, qualification) | **Gross margin estimate:** ~50% unit gross margin at $60, but $0.3-1.5M/yr gross profit cannot repay $10-20M NRE

**US manufacturability:** SkyWater Fab 25 (Austin TX) or Bloomington MN (DMEA trusted); U.S. OSAT packaging.

**Who is already doing this:** Alliance Memory, ISSI and Winbond still sell commercial SDRAM at ~$2-5 [ESTIMATE]; Rochester (licensed re-creation); DMEA's ARMS foundry [UNVERIFIED-training]; rad-hard programs use SRAM/MRAM from Honeywell, BAE, Frontgrade instead.

**Wins on which axis, for which buyer:** Supply security / trust / lifecycle — for DoD DMSMS offices and avionics primes

**Survives a 2029 glut?:** yes — Trusted DMSMS pricing is insensitive to commodity cycles.

**Fatal-flaw candidate:** No buyer at the price: COTS SDRAM is still made at $2-5 and DoDI 5200.44 trust rules target custom ICs, not commodity memory, so the market is ~$0.3-1.5M per year of gross profit against $10-20M of NRE.

*Possible?* yes - 1T1C MIM eDRAM is production-proven elsewhere; unproven on this line · *Profitable?* no - NRE never paid back · *Doable by this founder?* no

*Business-model lenses:* fabless->foundry, defense-first, university/lab patent license (capacitor module)

### C-72 — Legacy-DRAM buying cooperative for mid-size U.S. OEMs

*Sub-branch:* Supply-chain arbitrage (demand aggregation) · *Materials sense:* none

**What it is:** An agency-model purchasing cooperative that pools 2027-2030 DDR3/DDR4/LPDDR4 forecasts from 30-100 mid-size U.S. OEMs and negotiates multi-year allocation agreements with Micron (Manassas DDR4), Winbond, Nanya and their franchised distributors, backed by member letters of credit, with a forecast and allocation web portal. Revenue: ~2.5% of pooled spend plus $10k per year membership.

**Why it could work:** In the shortage, allocation goes to strategic OEMs while module makers and small buyers are cut (TrendForce, Jan 2026); Nanya's long-term agreements expired in June 2026 and repriced >60%; firm, LC-backed, aggregated demand is what suppliers reward. Model: 40 members at $1.5M each = $60M pooled spend -> ~$1.9M revenue at ~85% gross margin (agency model).

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [PC DRAM 1Q26: prices to surge over 80% on server supply prioritization (TrendForce abstract)](https://www.trendforce.com/research/download/RP260114IU) — industry, 2026-01-14. DRAM supply prioritized to strategic OEMs while module makers are limited (abstract only) (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Nanya 3Q26 results (TrendForce News)](https://www.trendforce.com/news/?p=65146) — news, 2026-10-12. Nanya 3Q26 gross margin 85.7%, operating margin 80%; LTAs expired end-June 2026 and repriced >60% higher in July (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Memory shortage watch: DDR3L/DDR4, May 2026 (Findchips)](https://blog.findchips.com/memory-shortage-watch-ddr3l-ddr4-may-2026/) — industry, 2026-05. Zero authorized stock of a mainstream Micron DDR4 part at Newark, Avnet and Mouser; only independent-market stock at a premium (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Micron ramps US-made DDR4 production in Virginia (eeNews Europe)](https://www.eenewseurope.com/en/micron-ramps-us-made-ddr4-production-in-virginia/) — news, 2026-05. DDR4 buffers at auto/industrial customers fell from 31+ weeks to 6-8 weeks (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Response measures to Samsung DDR4 IC EOL announcement (Advantech)](https://www.advantech.com/en/resources/news/response-measures-to-samsung-ddr4-ic-eol-announcement) — company, 2025. Industrial-PC maker tells customers DDR4 supply runs to ~end-2026 and to avoid Samsung DDR4 in new designs: long-lifecycle buyers are actively managing EOL (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Mobius Materials (Y Combinator profile)](https://www.ycombinator.com/companies/mobius-materials) — company, unknown. Mobius describes itself as the spot market for semiconductors: a funded intermediary already aggregating component demand (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)

**Capital tier:** T1 | **Time to first revenue:** 6-12 months (membership fees from 5-10 founding OEMs; first pooled allocation in 9-15 months) | **Gross margin estimate:** ~80-90% on fee revenue (agency model); title model is distribution-like (3-8%)

**US manufacturability:** None (commercial structure); can steer pooled volume to U.S.-made Manassas DDR4.

**Who is already doing this:** Franchised distributors (Arrow, Avnet, WPG, Future), procurement consultancies, Mobius Materials, independent brokers; healthcare GPOs (Vizient, Premier) as the model [UNVERIFIED-training].

**Wins on which axis, for which buyer:** Supply security — for Mid-size OEMs buying $0.5-5M per year of legacy DRAM

**Survives a 2029 glut?:** partially — Allocation stops being scarce; value shrinks to price negotiation (the GPO model), so fees compress but the network persists.

**Fatal-flaw candidate:** Suppliers and franchised distributors may refuse an intermediary that takes neither title nor credit risk; taking title needs $8-27M of working capital (T2), and the allocation value evaporates in a glut.

*Possible?* marginal - depends on suppliers recognizing the co-op · *Profitable?* marginal - good margins if allocation materializes · *Doable by this founder?* marginal - needs a memory-sales veteran

*Business-model lenses:* recert/brokerage (procurement), SaaS (forecast portal), data product

## D. Software & virtual RAM (12 cards)

### C-73 — Memory FinOps Audit for Cloud SaaS

*Sub-branch:* Cloud memory right-sizing / FinOps · *Materials sense:* none · *Merged from:* D.01, D.04

**What it is:** A read-only web app with an AWS IAM role. It reads CUR plus CloudWatch-agent/Prometheus memory metrics across EC2 r/x/m-family, ElastiCache, RDS, K8s pods and JVM heaps. Output is a fixed-fee 'memory diet' report and a monitoring subscription, sold through AWS Marketplace to 20-500-engineer SaaS companies. The playbook levers are r->m family downsizing, K8s in-place pod resize (stable v1.35), JDK compact object headers and Redis->Valkey.

**Why it could work:** AWS list prices put marginal RAM at $2.56-2.62/GiB-month, and RAM is 28-43% of the m7i/r7i list price (computed). Clusters leave about 18% of memory unused (Sysdig via KRR). Take a $40k/month EC2 bill with RAM at 30%, of which half the unused 18% is realizable: that saves about $1.1k/month, so a 25% share-of-savings fee is about $270/month. Reaching $20k MRR needs about 74 customers (d_calcs.py in D_notes).

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [AWS Price List API, EC2 us-east-1 (versions 2025-09 and 2026-10)](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/20261029175634/us-east-1/index.csv) — company, 2026-10. Primary data. All 92 compared On-Demand Linux SKUs (c7i/m7i/m8g/r6i/r7g/r7i/r7iz/r8g/x2idn/u7i) had identical prices in Sep-2025 and Oct-2026. Marginal RAM computes to $2.56-2.62/GiB-month; x2idn.16xlarge (1 TiB) costs $6.669/h.
  - [AWS Price List API, EC2 us-east-1, version eff. 2025-09](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/20250930212021/us-east-1/index.csv) — company, 2025-09. The pre-spike baseline, used for the before/after diff.
  - [Robusta KRR README](https://github.com/robusta-dev/krr) — industry, 2026. Free MIT tool that right-sizes K8s memory (7-day max + 15%). Quotes Sysdig: 18% of memory unused on average.
  - [KEP-1287 in-place pod resize kep.yaml](https://github.com/kubernetes/enhancements/blob/master/keps/sig-node/1287-in-place-update-pod-resources/kep.yaml) — industry, 2025. In-place pod resource resize went stable in Kubernetes v1.35, so memory can be right-sized without pod restarts.
  - [OpenJDK PR: JEP 450 Compact Object Headers](https://github.com/openjdk/jdk/pull/20677) — industry, 2024-11. Compact object headers integrated into JDK mainline (experimental, JDK 24). No savings figure on the page; 10-20% heap reduction is [UNVERIFIED-T].
  - [CAST AI GitHub org](https://github.com/castai) — company, 2026-10-31. Well-resourced automation vendor, alive and shipping (114 repos, updates to 2026-10-31).
  - [OpenCost README](https://github.com/opencost/opencost) — industry, 2026. Free Apache-2.0 K8s and cloud cost monitoring, originally from Kubecost.
  - [AWS Price List API, ElastiCache us-east-1 (versions 2025-09 and 2026-10)](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonElastiCache/20261028192450/us-east-1/index.json) — company, 2026-10. cache.r7g.large: Redis OSS $0.219/h vs Valkey $0.1752/h, unchanged across both versions. New Redis OSS Extended Support SKUs: $0.175/h (Yr1-2) and $0.35/h (Yr3).
  - [AWS ElastiCache price list, version eff. 2025-09](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonElastiCache/20250915211737/us-east-1/index.json) — company, 2025-09. Pre-spike baseline: identical node prices.
  - [Dragonfly README](https://github.com/dragonflydb/dragonfly) — company, 2026. Vendor test: ~30% less memory than Redis idle; Redis peaks at ~3x Dragonfly memory during snapshot.
  - [Dragonfly BSL 1.1 license](https://github.com/dragonflydb/dragonfly/blob/main/LICENSE.md) — company, 2026. Third parties may not offer it as a managed in-memory store service until 2030-11-01.
  - [Valkey releases](https://github.com/valkey-io/valkey/releases) — industry, 2026-10-26. Active releases (9.1.3, 2026-10-26). 9.2.0-rc1 adds memory reductions (B+tree sorted sets, shared WATCH/pubsub keys).

**Capital tier:** T0 | **Time to first revenue:** 3-6 months: a first fixed-fee audit ($3-8k) for a SaaS company in the founder's network, then a monitoring subscription. | **Gross margin estimate:** 75-85%

**US manufacturability:** Pure software built and hosted in the U.S. (AWS us-east-1) and sold via AWS Marketplace. No fab or hardware.

**Who is already doing this:** CAST AI, ScaleOps, StormForge (CloudBolt), Kubecost/OpenCost (IBM [UNVERIFIED-T]), PerfectScale (DoiT [UNVERIFIED-T]), Sedai, Densify, and free tools: AWS Compute Optimizer, Robusta KRR, K8s VPA, Goldilocks. Intel Granulate reportedly shut down (2025) [UNVERIFIED: repo shows no notice].

**Wins on which axis, for which buyer:** $/GiB-month of rented cloud RAM (fewer GiB-months bought) — for Series A-C SaaS companies with $20k-200k/month AWS bills and no dedicated FinOps engineer

**Survives a 2029 glut?:** yes — AWS did not raise memory-instance list prices during the 2026 spike (92 SKUs unchanged), so the savings do not depend on DRAM prices and a glut changes nothing. The flip side: the shortage gives this product no new 'why now'.

**Fatal-flaw candidate:** The category is crowded and the floor is free (Compute Optimizer, KRR, VPA, OpenCost). The DRAM shortage never reached cloud list prices, so buyers feel no new urgency. A report-only product churns after the first audit.

*Possible?* yes - standard FinOps mechanics, shipping at many vendors · *Profitable?* marginal - ~$270/month ACV against free tools and funded automation vendors; churn after the savings are booked · *Doable by this founder?* yes - read-only AWS integration and reports; the first revenue could come from consulting in the founder's network

*Business-model lenses:* SaaS; services (fixed-fee audit) -> SaaS

### C-74 — Fleet Memory-Reclaim Autopilot (TMO for on-prem)

*Sub-branch:* Transparent memory compression / proactive reclaim / dedup · *Materials sense:* none

**What it is:** A per-node agent plus web control plane. It enables and tunes upstream Linux zswap (zsmalloc + zstd/lz4), Meta-Senpai-style PSI-driven proactive reclaim via cgroup2, KSM page dedup on Proxmox/KVM hosts, and Kubernetes 1.34 LimitedSwap, with per-workload SLO guardrails and a 'GB reclaimed = $ of DRAM not bought' ledger. It is sold per node to on-prem/colo operators who buy DRAM at 2026 prices.

**Why it could work:** On-prem buyers pay DRAM directly: $14-16/GB at contract, ~$32/GB street (64GB RDIMM $900-1,000 to $2,064). Take a 200-server x 512GB fleet with 20% cold memory at ~2:1 compression: it frees ~10 TB, which defers $154k (contract) to $328k (street) of DRAM. Kubernetes container swap went stable in v1.34, removing the old 'kubelet refuses swap' blocker. Meta reported 20-32% fleet memory savings from TMO [UNVERIFIED-T: paper not opened].

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [Meta Senpai README](https://github.com/facebookincubator/senpai) — industry, unknown. PSI plus cgroup2 memory.high proactive reclaim (TMO building block). Example: kernel-build peak fell from 804 MB to 348 MB.
  - [Linux zswap docs](https://github.com/torvalds/linux/blob/master/Documentation/admin-guide/mm/zswap.rst) — industry, 2026. Upstream compressed swap cache (zsmalloc) with per-cgroup writeback control and a shrinker.
  - [Linux zram docs](https://github.com/torvalds/linux/blob/master/Documentation/admin-guide/blockdev/zram.rst) — industry, 2026. Upstream compressed RAM device (lz4/zstd), with writeback and recompression; the docs expect about 2:1 compression.
  - [Linux KSM docs](https://github.com/torvalds/linux/blob/master/Documentation/admin-guide/mm/ksm.rst) — industry, 2026. Page dedup for KVM VM density, with a general_profit metric; costs CPU and COW latency.
  - [KEP-2400 node swap kep.yaml](https://github.com/kubernetes/enhancements/blob/master/keps/sig-node/2400-node-swap/kep.yaml) — industry, 2025. Kubernetes container swap (LimitedSwap) went stable in v1.34.
  - [Kubernetes swap memory management docs](https://github.com/kubernetes/website/blob/main/content/en/docs/concepts/cluster-administration/swap-memory-management.md) — industry, 2025. Operational caveats: encrypt swap, use fast NVMe, taint swap nodes. Swap degrades badly on throttled cloud disks, and the scheduler ignores swap.
  - [EE Times Asia / Counterpoint RDIMM prices (via p1-market)](https://www.eetasia.com/memory-prices-surging-by-90-from-4q-2025/) — news, 2026-01. 64GB RDIMM contract $450 (4Q25), above $900 (1Q26), possibly above $1,000 (2Q26).

**Capital tier:** T0 | **Time to first revenue:** 6-12 months: a paid pilot with a regional hosting provider, Proxmox MSP or on-prem K8s shop ($500-2k/month for 50-200 nodes). | **Gross margin estimate:** 80-90%

**US manufacturability:** Pure software. Target customers' fleets sit in U.S. colos (Ashburn VA, Secaucus NJ). Builds on upstream Linux mm, Proxmox VE (KSM) and Kubernetes 1.34+.

**Who is already doing this:** Meta (TMO/Senpai, internal), Google (zswap far memory, internal), Linux upstream (free), Red Hat/Canonical (tuned profiles), Proxmox (KSM built in). The cloud K8s optimizers (CAST AI, ScaleOps) focus on requests and instances, not swap [ESTIMATE]. MemVerge left the field.

**Wins on which axis, for which buyer:** Effective $/GB (usable GB per purchased GB), which defers DRAM capex — for Regional hosting providers, MSPs running Proxmox/KVM, on-prem Kubernetes and CI/build farms, and university HPC centers that must buy DDR5 RDIMMs at 2026 prices

**Survives a 2029 glut?:** partially — The deferred-DRAM value of the reference fleet falls from ~$154k to ~$61k at -60%. Density value remains but becomes a nice-to-have, and the price story behind the sale disappears.

**Fatal-flaw candidate:** It is configuration of free kernel features. Sophisticated operators already do it themselves, and conservative ones fear swap latency and OOM incidents. One production incident at an early customer ends the company.

*Possible?* yes - production-proven at Meta/Google, and every component is upstream · *Profitable?* marginal - real savings while DRAM is expensive, but buyers can DIY and the pain halves in a glut · *Doable by this founder?* marginal - needs a Linux-mm expert for SLO safety; the sales cycle to on-prem ops is slow

*Business-model lenses:* SaaS (per-node subscription); open-core agent

### C-75 — KV-Cache Tier Integration & Tuning for Self-Hosted LLMs

*Sub-branch:* LLM inference KV-cache management software · *Materials sense:* none

**What it is:** A productized integration service plus a benchmarking/monitoring dashboard. It deploys host-DRAM and NVMe KV-cache tiers (LMCache, NVIDIA Dynamo KVBM, Mooncake Store, SGLang HiCache) into mid-market vLLM/SGLang clusters and sizes the DRAM tier per workload from measured prefix-reuse rates. Recurring revenue comes from hit-rate, TTFT and $/token monitoring.

**Why it could work:** Llama-3.1-70B needs 320 KiB of KV per token, so 1 TB of host DRAM ($15k at 2026 contract) holds ~3.1M reusable prefix tokens. Mooncake reports Kimi serving 75% more requests within SLO, and Dynamo claims 2x TTFT from KV-aware routing. The stacks churn fast (LMCache shipped 65 PyPI releases from May 2025 to Oct 2026; vLLM 0.32.0 came out 2026-10-18), and teams running 8-64 GPUs lack staff to keep up.

**Evidence:** TRL 8 · Rule 1: SUPPORTED
  - [LMCache README](https://github.com/LMCache/LMCache) — industry, 2026. Open-source KV-cache layer (CPU/SSD/remote tiers) for vLLM, integrated into NVIDIA Dynamo (Sep 2025). Development supported by Tensormesh.
  - [NVIDIA Dynamo README](https://github.com/ai-dynamo/dynamo) — company, 2026. Free Apache-2.0 KVBM offloads KV GPU->CPU->SSD->remote. Claims 2x TTFT from KV-aware routing (Baseten).
  - [Mooncake README](https://github.com/kvcache-ai/Mooncake) — industry, 2026. KV-centric disaggregated serving at Kimi: 75% more requests within SLO. Integrated into vLLM, SGLang, LMCache, Dynamo and TensorRT-LLM (2026-10-10).
  - [tensormesh SDK on PyPI](https://pypi.org/pypi/tensormesh/json) — company, 2026-06. Tensormesh, the company around LMCache, ships a hosted serverless-inference and control-plane SDK (first release 2026-04-02).
  - [meta-llama/llama-models config (via B)](https://github.com/meta-llama/llama-models) — industry, 2026. Llama 3.1 70B: 80 layers, 8 KV heads, head_dim 128, so 320 KiB of KV per token at BF16.

**Capital tier:** T0 | **Time to first revenue:** 6-12 months: an integration engagement ($15-40k) with an enterprise AI team or small U.S. GPU cloud, then a monitoring retainer. | **Gross margin estimate:** 50-70% (services-heavy)

**US manufacturability:** Software and services. Customers' GPU clusters are in U.S. colos (Ashburn VA, NJ). Builds on Apache-2.0 LMCache, Dynamo and Mooncake.

**Who is already doing this:** Tensormesh (the LMCache creators: hosted inference plus control-plane SDK, first PyPI release 2026-04), NVIDIA (Dynamo, free), Moonshot (Mooncake), Red Hat llm-d [UNVERIFIED-T], WEKA Augmented Memory Grid, Pliops, VAST [UNVERIFIED-T], hosted inference providers (Baseten, Together, Fireworks).

**Wins on which axis, for which buyer:** $/token and TTFT: host DRAM ($/GB) substitutes for re-computing prefill on HBM GPUs — for Mid-market teams self-hosting 70B-class open models on 8-64 GPUs for data-residency reasons (legal-tech, healthcare, fintech)

**Survives a 2029 glut?:** yes — A glut makes host DRAM cheaper and the KV tier more attractive. The value is GPU-hours avoided, which does not depend on DRAM prices.

**Fatal-flaw candidate:** NVIDIA, the vLLM/SGLang maintainers and Tensormesh are turning this into defaults and SaaS, so the integration gap closes within 12-18 months. Buyers purchase GPU-infra credibility the founder does not have.

*Possible?* yes - shipping open source at Moonshot/Kimi and integrated into NVIDIA Dynamo · *Profitable?* marginal - large market but direct competition from free NVIDIA tooling and the LMCache company itself · *Doable by this founder?* marginal - needs GPU access for benchmarking and deep inference-stack knowledge

*Business-model lenses:* services -> SaaS; open-core

### C-76 — Software-Defined Memory Pooling / RAM-as-a-Service over CXL (tempting, dead)

*Sub-branch:* Software-defined memory (Kove/MemVerge model) · *Materials sense:* none

**What it is:** OS/hypervisor software that pools DRAM across servers (RDMA today, CXL 2.0/3.x switches later) and leases slices to applications on demand: the Kove:SDM / MemVerge Memory Machine model. It would be sold as an on-prem license to HPC, genomics and in-memory analytics shops.

**Why it could work:** Pooling recovers stranded memory (Azure's Pond work reported ~7-9% DRAM savings [UNVERIFIED-T]), and each stranded GB is worth 4x more in 2026. CXL switches (XConn, Astera Labs) are shipping in pilots.

**Evidence:** TRL 6 · Rule 1: SUPPORTED
  - [MemVerge GitHub org](https://github.com/MemVerge) — company, 2026-10-28. Recent work is LLM routing, LMCache/vLLM forks, the MMAI GPU cluster manager and cloud-HPC spot tools. No new memory-virtualization repos.
  - [MemVerge mmai-public](https://github.com/MemVerge/mmai-public) — company, 2026. Memory Machine AI is a GPU cluster manager (docs path /AI/GPU_Cluster_Manager), not a DRAM pooling product.
  - [Linux CXL maturity map (via B)](https://github.com/torvalds/linux/blob/master/Documentation/driver-api/cxl/maturity-map.rst) — industry, 2026-10-31. Upstream Linux: Dynamic Capacity Device, multi-host sharing and fabrics are all scored [0] (not implemented).
  - [SK hynix HMSDK (via B)](https://github.com/skhynix/hmsdk) — company, 2025-11-03. CXL tiering (weighted interleave, DAMON migration) is already upstream and free.

**Capital tier:** T2 | **Time to first revenue:** 24-36 months: needs CXL switch hardware partners, enterprise validation and a field sales team. | **Gross margin estimate:** 70-85% if it sells

**US manufacturability:** Software. Hardware would come from U.S. CXL switch/expander vendors (XConn, Astera Labs) in Supermicro/Dell servers; Montage (China) controllers would be avoided.

**Who is already doing this:** Kove (Kove:SDM, Chicago [UNVERIFIED-T status]), MemVerge (moved to AI/GPU cluster management), Liqid, GigaIO, Unifabrix, Panmnesia, plus free upstream Linux tiering (TPP, DAMON, weighted interleave).

**Wins on which axis, for which buyer:** $/GB through fewer DIMMs per cluster — for HPC centers and genomics/EDA farms with bursty per-job memory peaks

**Survives a 2029 glut?:** no — Stranded-memory savings of ~10% are worth little at ~$6/GB. Pooling was a hard sell even before the shortage.

**Fatal-flaw candidate:** The category's best-known startup (MemVerge) walked away from memory virtualization. Linux upstream still scores CXL Dynamic Capacity and multi-host sharing [0], and tiering is already free upstream. Enterprise hardware dependence far exceeds T0/T1.

*Possible?* marginal - RDMA far memory works at hyperscalers; CXL pooling software is immature upstream · *Profitable?* no - prior entrants pivoted out; savings are too small to carry the integration cost · *Doable by this founder?* no - requires systems-software depth and hardware partners

*Business-model lenses:* software licensing; fabless->OEM partnership

### C-77 — NVMe-as-RAM Virtual Memory Software (IMDT/ScaleMP revival, tempting, dead)

*Sub-branch:* Software 'virtual RAM' on flash · *Materials sense:* a-material

**What it is:** A thin hypervisor or kernel layer that presents NVMe SSDs as system RAM (the Intel Memory Drive Technology / ScaleMP vSMP MemoryONE approach), so a server with 256GB DRAM plus 4TB NVMe shows 4TB of 'memory'. It would be sold as a per-server license.

**Why it could work:** NAND $/GB is a small fraction of DRAM even after its own 2026 rise, NAND is forecast to turn to surplus in 2H27 (TrendForce via p1), and the arbitrage looks enormous on paper.

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [Linux zswap docs](https://github.com/torvalds/linux/blob/master/Documentation/admin-guide/mm/zswap.rst) — industry, 2026. Upstream compressed swap cache (zsmalloc) with per-cgroup writeback control and a shrinker.
  - [Kubernetes swap memory management docs](https://github.com/kubernetes/website/blob/main/content/en/docs/concepts/cluster-administration/swap-memory-management.md) — industry, 2025. Operational caveats: encrypt swap, use fast NVMe, taint swap nodes. Swap degrades badly on throttled cloud disks, and the scheduler ignores swap.
  - [Intel 10-Q Q2-2022 (via A2)](https://www.sec.gov/Archives/edgar/data/50863/000005086322000030/intc-20220702.htm) — company, 2022-07. Optane wind-down with a $559M inventory impairment. The media that made NVMe/PMem-as-RAM viable is gone.

**Capital tier:** T1 | **Time to first revenue:** 18-30 months: hypervisor development plus validation with an in-memory analytics vendor. | **Gross margin estimate:** 80% (license) if any sales

**US manufacturability:** Software running on commodity NVMe (Micron/Solidigm SSDs in U.S.-assembled servers).

**Who is already doing this:** Intel IMDT (end-of-life with Optane [UNVERIFIED-T]), ScaleMP (acquired by SAP [UNVERIFIED-T]), and free Linux swap + zswap writeback.

**Wins on which axis, for which buyer:** $/GB of capacity (NAND standing in for DRAM) — for In-memory analytics users who could tolerate microsecond-to-millisecond tail latency

**Survives a 2029 glut?:** no — At $6/GB DRAM nobody accepts a 1000x latency penalty, and the buyer goes back to DIMMs.

**Fatal-flaw candidate:** NAND reads take ~50-100 us vs ~100 ns for DRAM (~1000x). Without Optane-class media the trick only serves workloads that Linux swap + zswap already serve for free, and that media died with a $559M impairment.

*Possible?* yes - it shipped once (IMDT 2017-2022) · *Profitable?* no - Optane's death removed the only media that made it competitive · *Doable by this founder?* no

*Business-model lenses:* software licensing

### C-78 — Consumer 'Virtual RAM Booster' App (dead)

*Sub-branch:* Consumer memory software · *Materials sense:* none

**What it is:** A Windows/macOS utility marketed to PC owners priced out of upgrades (32GB DDR5 kits ~$450) that claims to 'add RAM' through compression, page-file tuning and 'RAM cleaning'. It would be sold at $19-39 via web and app stores.

**Why it could work:** Retail panic and search demand ('RAM prices', 'need more RAM') are high, and DIY buyers are giving up on upgrades (demand destruction).

**Evidence:** TRL 9 · Rule 1: UNSUPPORTED
  - [Linux zram docs](https://github.com/torvalds/linux/blob/master/Documentation/admin-guide/blockdev/zram.rst) — industry, 2026. Upstream compressed RAM device (lz4/zstd), with writeback and recompression; the docs expect about 2:1 compression.
  - [Digital Citizen 32GB kits $450 (via p1-market)](https://www.digitalcitizen.life/ddr5-ram-prices-surge-in-2026-as-32gb-kits-reach-450-amid-global-memory-shortage/) — news, 2026. 32GB DDR5 kits about $450 retail.
  - [TechRadar on retail demand destruction (via p1-market)](https://www.techradar.com/pro/good-news-ram-prices-seem-to-have-finally-stabilized-bad-news-its-probably-because-memory-prices-are-so-high-that-its-forcing-most-of-us-to-give-up-buying-anything) — news, 2026. Retail prices stabilized because buyers stopped buying.
  - [rampricesusa Sep-2026 (via p1-market)](https://rampricesusa.com/insights/monthly/2026-09) — industry, 2026-09. Free consumer tracker: typical DDR5 retail $18.04/GB.

**Capital tier:** T0 | **Time to first revenue:** 1-3 months to first sale; months 3-12 likely bring refunds and chargebacks. | **Gross margin estimate:** 85-95% before refunds

**US manufacturability:** Software; distributed via the web/Microsoft Store.

**Who is already doing this:** OS vendors do it for free (Windows memory compression, macOS compressed memory, Android/ChromeOS zram [UNVERIFIED-T for Windows/macOS]). Historic precedent: SoftRAM 1995 (FTC action [UNVERIFIED-T]) and 'RAM cleaner' scareware.

**Wins on which axis, for which buyer:** None real. Any gain over the OS default is unproven. — for Consumers with 8-16GB PCs

**Survives a 2029 glut?:** no — When a 32GB kit returns to ~$100-180, the reason to buy disappears.

**Fatal-flaw candidate:** Every modern OS already compresses memory, so the app can only deliver placebo. History says this ends in FTC or app-store action and reputational ruin.

*Possible?* marginal - the mechanism exists, but it is already in the OS, so the product claim is unsupported · *Profitable?* no - refunds, chargebacks, store bans and regulatory risk · *Doable by this founder?* yes technically; rejected on ethics and durability

*Business-model lenses:* consumer software

### C-79 — TB-RAM Bare-Metal Rental from Recovered DDR4 Servers

*Sub-branch:* RAM-as-a-service (physical, depreciated hardware) · *Materials sense:* c-capital

**What it is:** Buy off-lease dual-socket servers (Dell R740/R750- or HPE DL380 Gen10-class) and populate them with 1-1.5 TB of recovered DDR4 RDIMM from U.S. ITAD channels. Burn-in test them, place them in an East Coast retail colo (Ashburn VA / Secaucus NJ), and rent single-tenant high-memory boxes monthly through a self-serve web portal.

**Why it could work:** AWS charges $6.669/h for 1 TiB (x2idn.16xlarge, unchanged since 2025) = $4,868/month, or $4.75/GiB-month. A 1.5 TB box costs $6.1k-13.8k with recovered DDR4 at $3-8/GB. Renting at $1,200/month against $250 colo pays back in 6-15 months (d_calcs.py).

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [AWS Price List API, EC2 us-east-1 (versions 2025-09 and 2026-10)](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/20261029175634/us-east-1/index.csv) — company, 2026-10. Primary data. All 92 compared On-Demand Linux SKUs (c7i/m7i/m8g/r6i/r7g/r7i/r7iz/r8g/x2idn/u7i) had identical prices in Sep-2025 and Oct-2026. Marginal RAM computes to $2.56-2.62/GiB-month; x2idn.16xlarge (1 TiB) costs $6.669/h.
  - [BuySellRAM market update (via p1-market)](https://www.buysellram.com/blog/ram-market-update/) — industry, 2026-08-31. A U.S. used-RAM buyer publishes DRAMeXchange-based content as lead-gen (DDR4 8Gb avg $44.37).
  - [TweakTown DDR4 +50% Q3-26 (via p1-market)](https://www.tweaktown.com/news/112541/even-ddr4-ram-is-not-safe-from-the-rampocalypse-prices-rose-over-50-percent-in-q3-2026/index.html?type=News) — news, 2026-07. DDR4 contract quoted up to +50% QoQ in Q3-2026.
  - [Servnet DDR5 server memory tracker (via p1-market)](https://www.servnetuk.com/research/ddr5-server-memory-price-tracker-2026) — industry, 2026-08. Street price of a 64GB DDR5 RDIMM about $2,064 (Aug 2026).

**Capital tier:** T1 | **Time to first revenue:** 4-8 months: the first 2-3 boxes rented to genomics/EDA users found via forums and university labs. | **Gross margin estimate:** 55-70% after depreciation

**US manufacturability:** Hardware sourced from U.S. ITAD/off-lease dealers and hosted in U.S. colo (Ashburn VA or Secaucus NJ). No new manufacturing. Distinct from C-49, which sells new CXL appliances.

**Who is already doing this:** Hetzner and OVHcloud dedicated servers, PhoenixNAP, Latitude.sh, Cherry Servers, Vultr bare metal, used-server dealers [UNVERIFIED-T for 2026 pricing].

**Wins on which axis, for which buyer:** $/GB-month of rented RAM (about 4x cheaper than AWS on-demand) — for Genomics assembly labs, EDA/simulation contractors, in-memory analytics developers and academic groups that need 1 TB+ of RAM for weeks

**Survives a 2029 glut?:** partially — The AWS price umbrella ($4.75/GiB-month) did not move in the spike and will not in a glut, so the margin over cloud survives. But Hetzner-class competitors restock cheaply, and DDR4-era boxes age out on power and CPU.

**Fatal-flaw candidate:** This is commodity hosting against established low-cost players, with a hardware-failure/on-call burden incompatible with a day job. While prices are high, selling the recovered DDR4 outright may beat renting it.

*Possible?* yes - plain hosting · *Profitable?* marginal - real spread vs AWS, thin vs Hetzner/OVH · *Doable by this founder?* marginal - capital and on-call burden

*Business-model lenses:* recert/brokerage + hosting (RaaS); module/appliance (none)

### C-80 — DRAM Cost & Allocation Intelligence for SMB Hardware OEMs

*Sub-branch:* DRAM price intelligence / procurement data product · *Materials sense:* none

**What it is:** A subscription web app that maps memory exposure in a small OEM's BOMs (DDR4/DDR5/LPDDR4X/eMMC part numbers). It pulls distributor price and stock via the Nexar/Octopart, DigiKey and Mouser APIs, overlays free spot indicators and TrendForce press-release forecasts, and sends buy/hold/re-qualify alerts and EOL warnings (Micron DDR4 EOL, Samsung/SK hynix DDR4 exits).

**Why it could work:** Supply is being prioritized to strategic OEMs (TrendForce), so tier-2 buyers face allocation and 4x price moves without analyst seats. At $150-300 per account per month, 80 accounts give ~$24k MRR (d_calcs.py). The founder's day job (product development/operations at a manufacturer) is exactly this buyer.

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [TrendForce RP260114IU summary (via p1-micron)](https://www.trendforce.com/research/download/RP260114IU) — industry, 2026-01-14. DRAM supply prioritized to strategic OEMs; module makers limited (tier-2 allocation risk).
  - [Nexar developer org](https://github.com/NexarDeveloper) — company, 2026-02. GraphQL API with Octopart supply (price/stock) data; Excel and Power BI connectors.
  - [GitHub search 'dram price'](https://github.com/search?q=dram+price&type=repositories) — industry, 2026-11-01. 37 repos, many free DRAMeXchange/TrendForce spot scrapers and dashboards updated within days.
  - [nwfella/memory-price-index](https://github.com/nwfella/memory-price-index) — industry, 2026-11-01. Free index of RamRadar retail asks plus TrendForce spot, with analysis dated 2026-11-01. DDR4 8Gb spot record $47.04.
  - [Mobius Materials DRAM Market Report (via p1-market)](https://www.mobiusmaterials.com/whitepapers/dram-market-report-2026) — company, 2026. DRAM market report given away (gated) as lead-gen for the marketplace.
  - [TrendForce 4Q26 price forecast (via p1-market)](https://www.trendforce.com/presscenter/news/20260930-13258.html) — industry, 2026-09-30. Conventional DRAM contract +10-15% QoQ in 4Q26; free press release.

**Capital tier:** T0 | **Time to first revenue:** 4-8 months: an MVP on Nexar/DigiKey APIs, with 5-10 design-partner OEMs from the founder's manufacturing network converting at $150-300/month. | **Gross margin estimate:** 75-85% (API fees are the main COGS)

**US manufacturability:** Pure software built and hosted in the U.S.; data partners Nexar (Altium/Renesas), DigiKey and Mouser APIs.

**Who is already doing this:** TrendForce/DRAMeXchange, InSpectrum, Omdia, Gartner, Counterpoint (paid seats); Mobius Materials (free DRAM report as marketplace lead-gen); SiliconExpert (Arrow), Z2Data, Lytica, Supplyframe (Siemens) [UNVERIFIED-T]; free trackers (rampricesusa, RamRadar, Servnet, 37 GitHub scrapers).

**Wins on which axis, for which buyer:** Supply security: price and allocation foresight (cost avoidance) — for Procurement/supply-chain leads at U.S. industrial PC, medical device, test-equipment and small system-builder OEMs with $1-50M/year memory spend

**Survives a 2029 glut?:** partially — In a glut nobody pays for shortage alerts and churn spikes. Only the EOL/lifecycle and second-source module keeps its value.

**Fatal-flaw candidate:** There is no proprietary data. The free layer is fully scraped (37+ GitHub trackers; Mobius gives its report away), and the contract-price data belongs to TrendForce/InSpectrum and cannot be redistributed. SMB willingness to pay is low and falls with the cycle.

*Possible?* yes - all inputs available via APIs and free sources · *Profitable?* marginal - low ACV, cyclical churn, no data moat · *Doable by this founder?* yes - the best founder-fit in the branch, but a weak business

*Business-model lenses:* data product; SaaS

### C-81 — Secondary DRAM Marketplace for Excess Inventory

*Sub-branch:* Procurement & brokerage marketplace · *Materials sense:* c-capital

**What it is:** A B2B web marketplace where OEMs and CMs list excess DRAM/LPDDR/eMMC reels and trays and buyers bid. It adds escrow and third-party AS6081 lab authentication and takes a 5-10% fee.

**Why it could work:** A 4x price spike turns stranded inventory into cash, and liquidity is fragmented among phone-and-email brokers. Spot is thin and broker-driven, and DDR4 spot hit a record $47.04.

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [Mobius Materials $3M seed (via p1-market)](https://www.prnewswire.com/news-releases/mobius-materials-raises-3m-to-combat-one-of-manufacturings-biggest-issues-amid-us-china-trade-tariffs-302643403.html) — news, 2025-12. Richmond VA YC company running an authenticated B2B excess-semiconductor marketplace (ML authentication patent filed). $3M seed in Dec 2025.
  - [Mobius Materials DRAM Market Report (via p1-market)](https://www.mobiusmaterials.com/whitepapers/dram-market-report-2026) — company, 2026. DRAM market report given away (gated) as lead-gen for the marketplace.
  - [nwfella/memory-price-index](https://github.com/nwfella/memory-price-index) — industry, 2026-11-01. Free index of RamRadar retail asks plus TrendForce spot, with analysis dated 2026-11-01. DDR4 8Gb spot record $47.04.
  - [BuySellRAM market update (via p1-market)](https://www.buysellram.com/blog/ram-market-update/) — industry, 2026-08-31. A U.S. used-RAM buyer publishes DRAMeXchange-based content as lead-gen (DDR4 8Gb avg $44.37).

**Capital tier:** T1 | **Time to first revenue:** 6-12 months to first matched trade; needs escrow, authentication-lab partners and insurance. | **Gross margin estimate:** 60-75% of net revenue (5-10% take of GMV)

**US manufacturability:** Software marketplace; physical authentication at U.S. AS6081 test houses; logistics from U.S. CM warehouses.

**Who is already doing this:** Mobius Materials (Richmond VA, YC, $3M seed Dec 2025, authenticated excess-semiconductor marketplace with an ML-authentication patent filed), Sourceability/Sourcengine, Fusion Worldwide, America II, Smith, NetComponents, BrokerForum, ICsource, eBay [UNVERIFIED-T for most].

**Wins on which axis, for which buyer:** Supply security / liquidity — for OEM/CM buyers under allocation, and sellers holding excess memory

**Survives a 2029 glut?:** partially — Flow reverses to sellers dumping. Prices fall 60% and take-rate revenue falls with GMV, though volume may rise.

**Fatal-flaw candidate:** Counterfeit liability and a two-sided cold start against entrenched brokers. A funded East Coast YC company (Mobius Materials) already does exactly this, with an authentication patent and hundreds of OEM/CM users.

*Possible?* yes - brokers do it daily · *Profitable?* marginal - margin exists, but counterfeit risk and incumbents squeeze it · *Doable by this founder?* no - Mobius is ahead in the same region with funding and IP

*Business-model lenses:* recert/brokerage; marketplace SaaS

### C-82 — Consumer RAM Price Tracker + Upgrade Compatibility Advisor

*Sub-branch:* Module compatibility/QVL tools; consumer price tracking · *Materials sense:* none

**What it is:** A consumer web app with a small system scanner, filling the gap left by the Crucial System Scanner/Advisor after Crucial's Feb-2026 exit. It identifies compatible DDR4/DDR5 modules from motherboard QVLs, tracks prices across Amazon, Newegg, B&H and eBay, and earns affiliate commissions plus price-drop alerts.

**Why it could work:** Retail DDR5 runs $13-18/GB and 32GB kits ~$450. Confused upgraders lost the Crucial advisor, which was Micron's consumer lead-gen tool [UNVERIFIED-T whether it still runs].

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [Micron exits Crucial (via p1-micron)](https://www.storagenewsletter.com/2025/12/05/micron-announces-exit-from-crucial-consumer-business/) — news, 2025-12-05. Crucial consumer brand ended; shipments through Feb 2026.
  - [rampricesusa Sep-2026 (via p1-market)](https://rampricesusa.com/insights/monthly/2026-09) — industry, 2026-09. Free consumer tracker: typical DDR5 retail $18.04/GB.
  - [nwfella/memory-price-index](https://github.com/nwfella/memory-price-index) — industry, 2026-11-01. Free index of RamRadar retail asks plus TrendForce spot, with analysis dated 2026-11-01. DDR4 8Gb spot record $47.04.
  - [GitHub search 'dram price'](https://github.com/search?q=dram+price&type=repositories) — industry, 2026-11-01. 37 repos, many free DRAMeXchange/TrendForce spot scrapers and dashboards updated within days.
  - [TechRadar on retail demand destruction (via p1-market)](https://www.techradar.com/pro/good-news-ram-prices-seem-to-have-finally-stabilized-bad-news-its-probably-because-memory-prices-are-so-high-that-its-forcing-most-of-us-to-give-up-buying-anything) — news, 2026. Retail prices stabilized because buyers stopped buying.

**Capital tier:** T0 | **Time to first revenue:** 2-4 months to first affiliate payouts. | **Gross margin estimate:** 85-95% (affiliate)

**US manufacturability:** Software; U.S. retail affiliate programs.

**Who is already doing this:** PCPartPicker, Kingston configurator, rampricesusa, RamRadar, camelcamelcamel, Tom's Hardware price index, Servnet tracker, capitalandcompute.net, siliconanalysts.com, and 37+ GitHub trackers.

**Wins on which axis, for which buyer:** Consumer $/GB (find the cheapest compatible module) — for DIY PC builders and upgraders and small IT shops; affiliate merchants pay

**Survives a 2029 glut?:** partially — Traffic falls when panic ends, and affiliate revenue shrinks with ASP (-60%).

**Fatal-flaw candidate:** Affiliate economics: ~2-4% of a ~$150 order is ~$3-6 per sale [UNVERIFIED-T rates], so a salary needs thousands of sales a month. SEO is owned by PCPartPicker and incumbent trackers, and retail demand is being destroyed.

*Possible?* yes · *Profitable?* no - side income at best · *Doable by this founder?* yes

*Business-model lenses:* consumer web / affiliate; data product (weak)

### C-83 — Shortage Briefing: Paid Memory-Market Newsletter (bridge only)

*Sub-branch:* Content & education · *Materials sense:* none

**What it is:** A weekly paid newsletter and short podcast for hardware buyers and retail investors. It synthesizes TrendForce press releases, DRAMeXchange spot boards, Micron/SK hynix/Samsung/Nanya earnings and a founder-built dataset, with sponsorships from brokers and ITADs. It is explicitly a bridge and a funnel for C-80/C-64.

**Why it could work:** The shortage is front-page news and the free content is fragmented. Lead-gen content (Mobius, BuySellRAM) proves the audience exists. 200-500 paid subscribers at $10-12/month is $2-6k MRR (d_calcs.py).

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [Mobius Materials DRAM Market Report (via p1-market)](https://www.mobiusmaterials.com/whitepapers/dram-market-report-2026) — company, 2026. DRAM market report given away (gated) as lead-gen for the marketplace.
  - [BuySellRAM market update (via p1-market)](https://www.buysellram.com/blog/ram-market-update/) — industry, 2026-08-31. A U.S. used-RAM buyer publishes DRAMeXchange-based content as lead-gen (DDR4 8Gb avg $44.37).
  - [nwfella/memory-price-index](https://github.com/nwfella/memory-price-index) — industry, 2026-11-01. Free index of RamRadar retail asks plus TrendForce spot, with analysis dated 2026-11-01. DDR4 8Gb spot record $47.04.
  - [TrendForce 4Q26 price forecast (via p1-market)](https://www.trendforce.com/presscenter/news/20260930-13258.html) — industry, 2026-09-30. Conventional DRAM contract +10-15% QoQ in 4Q26; free press release.

**Capital tier:** T0 | **Time to first revenue:** 1-3 months to the first paid subscribers on Substack/Beehiiv. | **Gross margin estimate:** 85-95%

**US manufacturability:** Content; U.S. platforms (Substack/Beehiiv).

**Who is already doing this:** TrendForce (free press releases), Mobius Materials and BuySellRAM (free lead-gen reports), Tom's Hardware, Igor'sLAB, Objective Analysis (Jim Handy), SemiAnalysis and Fabricated Knowledge (paid) [UNVERIFIED-T].

**Wins on which axis, for which buyer:** None on memory itself; time-to-insight for buyers — for SMB OEM procurement teams and retail semiconductor investors; brokers/ITADs as sponsors

**Survives a 2029 glut?:** no — Audience interest tracks prices. In a 2028-29 glut the topic dies, apart from a 'when to buy' bump.

**Fatal-flaw candidate:** It has no proprietary data or insider expertise against SemiAnalysis-class analysts and free vendor reports, and the realistic ceiling is a few thousand dollars of MRR.

*Possible?* yes · *Profitable?* marginal - side income, cyclical · *Doable by this founder?* yes

*Business-model lenses:* content/data product (bridge)

### C-84 — Embedded RAM-Diet Profiler for Small Hardware OEMs

*Sub-branch:* Embedded memory-footprint optimization · *Materials sense:* none

**What it is:** A CLI plus web report that profiles the real memory footprint of an embedded Linux/Yocto/Android product image under worst-case load (PSS via smem, cgroup peaks, zram headroom). It produces an engineering case for dropping one LPDDR4/DDR4 density step (e.g., 2GB->1GB) or enabling zram, priced per product line for small OEMs whose BOMs ballooned in 2026.

**Why it could work:** LPDDR4X rose +70-75% QoQ in 2Q26, and mobile LTAs signed near $21/GB. At 20k units/year x 1GB saved x $8-21/GB, a product line saves $160k-420k/year in BOM cost. zram's expected ~2:1 compression gives headroom without new silicon.

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [Linux zram docs](https://github.com/torvalds/linux/blob/master/Documentation/admin-guide/blockdev/zram.rst) — industry, 2026. Upstream compressed RAM device (lz4/zstd), with writeback and recompression; the docs expect about 2:1 compression.
  - [Linux zswap docs](https://github.com/torvalds/linux/blob/master/Documentation/admin-guide/mm/zswap.rst) — industry, 2026. Upstream compressed swap cache (zsmalloc) with per-cgroup writeback control and a shrinker.
  - [China Times / TrendForce 2Q26 mobile DRAM (via p1-market)](https://wantrich.chinatimes.com/news/20260515900291-420101) — news, 2026-05-15. LPDDR4X +70-75% QoQ, LPDDR5X +78-83% QoQ in 2Q26.
  - [Wccftech mobile DRAM LTAs (via p1-market)](https://wccftech.com/mobile-dram-prices-expected-to-increase-by-100-quarter-over-quarter-as-long-term-agreements-now-getting-signed-at-prices-as-high-as-21-gb/amp/) — news, 2026-05. Mobile DRAM LTAs signed at up to about $21/GB.
  - [TweakTown DDR4 +50% Q3-26 (via p1-market)](https://www.tweaktown.com/news/112541/even-ddr4-ram-is-not-safe-from-the-rampocalypse-prices-rose-over-50-percent-in-q3-2026/index.html?type=News) — news, 2026-07. DDR4 contract quoted up to +50% QoQ in Q3-2026.

**Capital tier:** T0 | **Time to first revenue:** 6-12 months: paid footprint audits ($5-20k) with 2-3 industrial/IoT OEMs from the founder's manufacturing network. | **Gross margin estimate:** 70-85%

**US manufacturability:** Software and services; customers are U.S. industrial, IoT and medical OEMs and their SoM vendors.

**Who is already doing this:** Embedded consultancies (Bootlin, Witekio, Toradex services) [UNVERIFIED-T], SoM vendor application engineers, Yocto buildhistory and smem (free), device-observability SaaS (Memfault [UNVERIFIED-T]).

**Wins on which axis, for which buyer:** $/unit BOM (fewer GB of DRAM per device) — for Hardware product managers at U.S. industrial, IoT and medical-device OEMs shipping 5k-200k units/year

**Survives a 2029 glut?:** no — At glut prices a 1GB step saves ~$2.5/unit, below the cost of re-spin and re-qualification, so demand evaporates.

**Fatal-flaw candidate:** Dropping a density step means board re-spin, re-qualification and (for medical) regulatory re-validation that cost more than a year of savings. Embedded engineers decide, and they rarely buy SaaS from non-engineers.

*Possible?* yes - standard footprint tooling · *Profitable?* marginal - lumpy consulting that dies in a glut · *Doable by this founder?* marginal

*Business-model lenses:* services -> SaaS

## E. Business-model-first concepts (14 cards)

### C-85 — DIMM Health Subscription: predictive replacement + recovered-DDR4 spares pool

*Sub-branch:* SaaS + spares pool (third-party maintenance for memory only) · *Materials sense:* c-capital

**What it is:** A per-node agent built on the open-source rasdaemon/Linux EDAC stack streams corrected and uncorrected DRAM error counts per DIMM to a web console. It flags DIMMs trending toward failure (row/page corrected-error growth) and triggers next-business-day shipment of a burn-in-tested replacement from a spares pool of recovered DDR4 RDIMMs bought from U.S. R2 ITADs (Iron Mountain/ITRenew-Sesame, Sims, regional R2 firms). It sells at ~$0.75 per DIMM-month to operators keeping out-of-warranty Dell R740/HPE DL380 Gen10-class DDR4 fleets alive because 2026 DRAM and server prices make a refresh unaffordable.

**Why it could work:** High DRAM prices push enterprises, universities, regional colos and MSPs to stretch DDR4 server life: DDR4 contract prices rose 24% in the 3 months to Oct 2026, and a 64GB RDIMM went from $450 to >$900 on contract. Out-of-warranty fleets lose OEM DIMM replacement. Telemetry is free (rasdaemon logs CE/UE events to SQL and already supports per-page/per-row CE thresholds), so the product is integration plus logistics. Model (e_estimates §10): a 2,400-DIMM customer pays $21.6k/yr. COGS is $8.9k at 2026 recovered-DDR4 prices (58.6% GM) and $3.9k in a glut (81.9% GM), because spares get cheaper. The pool needs only ~$7k of capital per customer. 25 customers = $540k ARR.

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [rasdaemon README.rst and misc/rasdaemon.env](https://github.com/mchehab/rasdaemon) — industry, 2026-11. Opened by E (git clone, last commit 2026-11-01). Logs kernel memory CE/UE events to SQLite/MySQL/PostgreSQL and supports per-page/per-row corrected-error thresholds (example 50) with soft-offline actions. Free, mature DIMM-health telemetry.
  - [DDR4 prices rise as shortages intensify through 2028 (Barclays)](https://www.guru3d.com/story/ddr4-memory-prices-now-also-rise-as-dram-supply-shortages-intensify-through-2028/) — news, 2026-10. DDR4 contract +24% over the 3 months to Oct 2026; shortage into 2028 [cross-reference: URL from a sibling agent's log; not opened by E]
  - [Memory prices surging by 90% from 4Q25 (Counterpoint)](https://www.eetasia.com/memory-prices-surging-by-90-from-4q-2025/) — news, 2026-01. 64GB RDIMM contract $450 (4Q25) to >$900 (1Q26) [cross-reference: URL from a sibling agent's log; not opened by E]

**Capital tier:** T0 | **Time to first revenue:** 4-8 months: paid pilots with 2-3 regional colo / university research-computing fleets on monthly billing | **Gross margin estimate:** 59% at 2026 spares prices, 82% in a glut

**US manufacturability:** No fabrication. U.S. value-add is burn-in test of recovered RDIMMs on owned DDR4 server beds (memtest86+, stressapptest) in a small East Coast space, plus the software. Supply comes from U.S. R2/e-Stewards ITADs.

**Who is already doing this:** Third-party maintenance firms bundle DIMM replacement into whole-server contracts (Park Place Technologies/Curvature, Service Express [UNVERIFIED-training]). Hyperscalers retire DIMMs on error trends in-house. OEM support (Dell ProSupport, HPE) covers in-warranty fleets. No memory-only predictive subscription was found, but a web search was not possible this session [UNVERIFIED].

**Wins on which axis, for which buyer:** lifecycle length: $/GB-month of keeping installed DDR4 capacity running vs. refreshing at ~$20/GB DDR5 — for Operators of out-of-warranty DDR4 fleets: university research computing, regional colos and MSPs, on-prem SaaS/fintech shops. Also TPM providers as wholesale buyers of the prediction feed plus spares.

**Survives a 2029 glut?:** partially — Margin improves: recovered DDR4 spares fall from ~$4.7 to ~$1.25/GB and GM rises from 59% to 82%. But demand shrinks once cheap DDR5 servers make refresh attractive again and DDR4 fleets age out after ~2029. The fee is priced on uptime, not on DRAM $/GB.

**Fatal-flaw candidate:** Low spend per customer and bundling. DIMMs are a small slice of whole-server TPM contracts, so Park Place or Service Express can match it at no extra charge. Self-maintaining shops may just keep a box of spare DIMMs. The predictive layer is copyable from open-source rasdaemon.

*Possible?* yes - every component exists (EDAC telemetry, recovered RDIMMs, NBD shipping) · *Profitable?* marginal - 59-82% GM but ~$22k ACV; needs ~25+ customers for ~$0.5M ARR, and TPM bundling caps price · *Doable by this founder?* yes - T0, software-led, part-time start; first customers are reachable regionally

*Business-model lenses:* SaaS; recert/brokerage (spares supply)

### C-86 — Memory Cost Escalation Index + EPA clause kit

*Sub-branch:* Data product (contract indexation, steel/copper-surcharge model) · *Materials sense:* none

**What it is:** Publish a monthly, methodology-documented memory cost index family (DDR4, DDR5, LPDDR4X/5X, eMMC/NAND). It is computed from authorized-distributor quote APIs (Nexar/Octopart, DigiKey, Mouser) plus transaction data contributed by a marketplace partner such as Mobius Materials. License it with ready-to-use economic-price-adjustment (EPA) clauses and a calculator API, so system integrators, EMS houses and federal contractors can pass memory cost through in both directions, like steel and copper surcharges. Federal contracts already allow index-based material EPA (FAR 16.203-1(a)(3), FAR 52.216-4).

**Why it could work:** Memory moved about 6x on contract in five quarters (index 100 -> 601) and will probably fall ~60% in 2028-29. Fixed-price deals for servers, industrial PCs and embedded systems either bleed or carry fat contingencies; Samsung's own device division lost money on component costs in 3Q26. A neutral index lets both sides drop the contingency. Example (e_estimates §11): memory is 35% of a $500k deliverable, so +25% memory triggers a +$43.75k adjustment and -60% a -$105k refund. Revenue: 30 x $6k + 5 x $24k = $300k ARR at 89% GM if self-built, 57% if a contract-price feed must be licensed.

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [FAR 16.203-1 Fixed-price contracts with economic price adjustment](https://github.com/GSA/GSA-Acquisition-FAR/blob/master/dita/16.203-1.dita) — government, 2025-10-01. Opened by E. EPA can be based on 'cost indexes of labor or material ... specifically identified in the contract'
  - [FAR 52.216-4 Economic Price Adjustment - Labor and Material (Jan 2017)](https://github.com/GSA/GSA-Acquisition-FAR/blob/master/dita/52.216-4.dita) — government, 2017-01. Opened by E. A standard federal clause for material price adjustment already exists
  - [TrendForce DRAM spot price board](https://www.trendforce.com/price_dram.html) — industry, 2026-08. The de facto public DRAM price reference is proprietary survey/spot data, not a licensed settlement index [cross-reference: URL from a sibling agent's log; not opened by E]
  - [Samsung 3Q26 results](https://news.samsungsemiconductor.com/global/samsung-electronics-announces-third-quarter-2026-results/) — company, 2026-10-29. Samsung's device (DX) businesses lost money on component costs while memory set records: downstream makers need memory-cost pass-through [cross-reference: URL from a sibling agent's log; not opened by E]
  - [TechInsights DRAM market report Q2-2026](https://www.techinsights.com/blog/slides-dram-market-report-q2-2026) — industry, 2026-06-01. The paid DRAM-data tier is held by TechInsights/TrendForce/InSpectrum [cross-reference: URL from a sibling agent's log; not opened by E]
  - [Mobius Materials raises $3M (authenticated surplus-semiconductor marketplace)](https://www.prnewswire.com/news-releases/mobius-materials-raises-3m-to-combat-one-of-manufacturings-biggest-issues-amid-us-china-trade-tariffs-302643403.html) — news, 2025-12. Richmond VA marketplace with an ML authentication patent filing: incumbent in spot trading/authentication and a possible data partner [cross-reference: URL from a sibling agent's log; not opened by E]

**Capital tier:** T0 | **Time to first revenue:** 6-12 months: back-fill index history, then first paid licenses with 3-5 integrators/EMS | **Gross margin estimate:** 57-89% (depends on whether contract data must be licensed)

**US manufacturability:** Pure software/data; no fab dependency.

**Who is already doing this:** TrendForce/DRAMeXchange (public spot board plus paid contract data), InSpectrum, TechInsights and Omdia sell the data. Free retail trackers exist. No memory-specific escalation-clause/index-licensing product was found [UNVERIFIED: search unavailable]. Closest analogues are metals surcharge indexes (CRU, Fastmarkets/AMM) [UNVERIFIED-training].

**Wins on which axis, for which buyer:** contract-risk transfer: lower price contingency (cost certainty) on memory-heavy fixed-price contracts — for U.S. system integrators and federal IT contractors on multi-year fixed-price deliveries (servers, rugged computers), regional and tier-2 EMS houses, industrial-PC OEMs (Advantech/OnLogic class) and their procurement counterparts.

**Survives a 2029 glut?:** partially — Index use is two-sided: buyers demand down-adjustments in a glut, and clauses already embedded in multi-year contracts persist. New-license sales slow when prices stop moving.

**Fatal-flaw candidate:** Credibility. Counterparties default to TrendForce/DRAMeXchange as the reference, and an index built from distributor list quotes rather than transactions is easy to dismiss or game. Licensing real contract data for redistribution may cost more than early revenue.

*Possible?* yes - distributor APIs and index methodology are standard · *Profitable?* marginal - high GM, but ~$0.3M ARR ceiling unless it becomes the reference index · *Doable by this founder?* yes - T0, part-time; the founder's day job (manufacturing ops) is the buyer persona

*Business-model lenses:* data product; SaaS

### C-87 — DRAM futures/swap market (index-settled forwards) - tempting, dead

*Sub-branch:* Financial market infrastructure · *Materials sense:* none

**What it is:** Create cash-settled DRAM forwards or swaps (e.g., a quarterly DDR5 16Gb contract-price swap) so OEMs, clouds, module makers and second-tier DRAM makers can hedge. They would be listed on a CFTC-registered exchange or written OTC through a swap dealer, with the venture as index provider and introducing broker.

**Why it could work:** The exposure is huge and two-sided. DRAM industry revenue was $154.7B in 2Q26 alone. Annualized contract-price volatility is 44-55% (e_estimates §1). Makers are naturally long and buyers naturally short. The 2018-19 and 2022-23 downturns each fell ~60%.

**Evidence:** TRL 2 · Rule 1: SUPPORTED
  - [SK hynix 3Q26: 14 LTAs, supply booked to 2029](https://www.sammyfans.com/2026/10/28/sk-hynix-q3-margin-hits-record-80-secures-14-ltas-with-memory-supply-booked-to-2029/amp/) — news, 2026-10-28. Physical multi-year LTAs are how DRAM price/supply risk is actually transferred today [cross-reference: URL from a sibling agent's log; not opened by E]
  - [Nanya 3Q26 results; LTAs repriced](https://www.trendforce.com/news/?p=65146) — news, 2026-10-12. Nanya LTAs expired end-June 2026 and repriced >60% higher: LTAs re-price rather than hedge [cross-reference: URL from a sibling agent's log; not opened by E]
  - [TrendForce DRAM spot price board](https://www.trendforce.com/price_dram.html) — industry, 2026-08. The de facto public DRAM price reference is proprietary survey/spot data, not a licensed settlement index [cross-reference: URL from a sibling agent's log; not opened by E]
  - [Mobius Materials: the spot market for semiconductors](https://www.ycombinator.com/companies/mobius-materials) — company, unknown. The nearest thing to a DRAM 'exchange' is a physical surplus marketplace [cross-reference: URL from a sibling agent's log; not opened by E]
  - [TrendForce 2018 PC DRAM contract release](https://press.trendforce.com/node/view/3173.html) — industry, 2018-11. 2018-19 downturn: 8GB module contract $68 -> $61 in one quarter, on the way to -62.5% [cross-reference: URL from a sibling agent's log; not opened by E]

**Capital tier:** T3 | **Time to first revenue:** 36-60 months: index certification, CFTC product approval, and market-maker recruitment before any fee revenue | **Gross margin estimate:** n/a before liquidity (exchange-like margins only at scale)

**US manufacturability:** Financial product; no manufacturing. Would run on a U.S. CFTC-registered DCM/SEF or through a registered swap dealer.

**Who is already doing this:** No listed DRAM futures are known on CME, ICE, SGX or TAIFEX [UNVERIFIED-training; could not search]. The de facto hedge is physical LTAs with prepayments (SK hynix: 14 LTAs, booked to 2029; CSP multi-year deals). Mobius Materials runs a physical spot marketplace.

**Wins on which axis, for which buyer:** price-risk transfer (cost certainty) — for PC/phone OEMs, tier-2 clouds without LTAs, module makers (Kingston, ADATA class); second-tier DRAM makers (Nanya, Winbond) as natural sellers.

**Survives a 2029 glut?:** partially — Hedging demand persists through volatility in both directions, but no liquidity forms without a trusted index at any point in the cycle.

**Fatal-flaw candidate:** No settlement-grade, licensable, manipulation-resistant index exists. TrendForce contract data is proprietary and survey-based, and spot is thin and panic-priced at ~1.7x contract. The big players already hedge physically through LTAs that simply re-price (Nanya +60%), so nobody supplies liquidity. CFTC registration and clearing push it to T3.

*Possible?* marginal - the instrument type is standard, but the index and liquidity do not exist · *Profitable?* no - no fee revenue until liquidity; physical LTAs are the entrenched substitute · *Doable by this founder?* no - T3, regulatory, not software-led

*Business-model lenses:* data product (index); brokerage

### C-88 — DRAM price-cap / allocation-guarantee subscription ('memory insurance') - dead

*Sub-branch:* Risk transfer product · *Materials sense:* none

**What it is:** Sell SMB OEMs and system integrators a 12-month subscription that caps the $/GB they pay for DDR4/DDR5, with the venture paying the difference above the cap, and/or guarantees a monthly allocation. It would be funded by premiums and backed by inventory bought ahead or by a reinsurer.

**Why it could work:** Tier-2 buyers without LTAs bear the marginal price and allocation cuts (TrendForce Jan 2026; Micron 10-K allocation language) and would value certainty. Hyperscalers get that certainty through multi-year LTAs; SMBs cannot.

**Evidence:** TRL 3 · Rule 1: SUPPORTED
  - [CSPs lock supply with long-term deals (TrendForce 2Q26)](https://technews.tw/2026/03/31/ai-server-demand-drives-2q26-memory-contract-price-increase-csps-lock-supply-long-term-deals/) — news, 2026-03-31. Hyperscalers lock multi-year supply; tier-2 buyers pay the marginal price [cross-reference: URL from a sibling agent's log; not opened by E]
  - [TrendForce: supply prioritized to strategic OEMs, module makers limited](https://www.trendforce.com/research/download/RP260114IU) — industry, 2026-01-14. Allocation favours strategic customers; tier-2 buyers and module makers are limited [cross-reference: URL from a sibling agent's log; not opened by E]
  - [Micron FY2026 Form 10-K](https://www.sec.gov/Archives/edgar/data/0000723125/000072312526000023/mu-20260903.htm) — company, 2026-10. 'supply allocation decisions that may affect some customers': newcomers cannot buy at contract [cross-reference: URL from a sibling agent's log; not opened by E]
  - [SK hynix 3Q26: 14 LTAs, supply booked to 2029](https://www.sammyfans.com/2026/10/28/sk-hynix-q3-margin-hits-record-80-secures-14-ltas-with-memory-supply-booked-to-2029/amp/) — news, 2026-10-28. Physical multi-year LTAs are how DRAM price/supply risk is actually transferred today [cross-reference: URL from a sibling agent's log; not opened by E]

**Capital tier:** T2 | **Time to first revenue:** 12-18 months: insurance or swap structuring, capital/reinsurance before the first policy | **Gross margin estimate:** fair premium 9-21% of capped spend; underwriting margin ~0-10% before adverse selection

**US manufacturability:** Financial product; none.

**Who is already doing this:** No DRAM price-cap product was found [UNVERIFIED: search unavailable]. Market substitutes are LTAs with prepayment and distributor allocation programs.

**Wins on which axis, for which buyer:** cost certainty / supply security — for SMB hardware OEMs, system integrators and tier-2 clouds without LTAs

**Survives a 2029 glut?:** no — Nobody buys caps when prices are falling. During the shortage the writer is short a call on a commodity with 44-55% volatility.

**Fatal-flaw candidate:** The venture is short a call option. The fair premium for an at-the-money 12-month cap is ~17-21% of capped spend (Black-76, 44-55% vol; e_estimates §2), which buyers will not pay. A 99th-percentile year costs the writer $1.5-2.1M per $1M of capped spend. Structured as indemnity it falls under state insurance regulation; structured as a price swap it falls under CFTC swap rules.

*Possible?* marginal - structurally possible through a reinsurer, but no one will write it at a price buyers accept · *Profitable?* no - adverse selection plus fat-tailed price moves · *Doable by this founder?* no - capital and regulatory burden

*Business-model lenses:* financial/risk product; brokerage

### C-89 — Buy-and-hold DRAM inventory arbitrage - speculation, not a venture

*Sub-branch:* Inventory trading · *Materials sense:* none

**What it is:** Buy DDR5/DDR4 components or RDIMMs on the spot market from brokers or marketplaces (U.S. independents, Mobius Materials, Shenzhen spot), hold them in dry storage, and sell into the next price step.

**Why it could work:** Contract prices rose about 6x from 3Q25 to 4Q26. TrendForce still forecast +10-15% QoQ for 4Q26, and Micron says supply stays tight through 2028.

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [TrendForce 4Q26 contract price forecast](https://www.trendforce.com/presscenter/news/20260930-13258.html) — industry, 2026-09-30. Conventional DRAM contract +10-15% QoQ in 4Q26 (+15-20% incl. HBM); QoQ rate down from +93-98% in 1Q26 [cross-reference: URL from a sibling agent's log; not opened by E]
  - [RAM market update (DRAMeXchange data)](https://www.buysellram.com/blog/ram-market-update/) — industry, 2026-08-31. DDR5 16Gb spot avg $53.92 (~$27/GB), about 1.7x the Q4-2026 contract price [cross-reference: URL from a sibling agent's log; not opened by E]
  - [Micron FY2026 Form 10-K](https://www.sec.gov/Archives/edgar/data/0000723125/000072312526000023/mu-20260903.htm) — company, 2026-10. 'supply allocation decisions that may affect some customers': newcomers cannot buy at contract [cross-reference: URL from a sibling agent's log; not opened by E]
  - [Analyst cycle views incl. Bloomberg Intelligence bear case](https://www.kucoin.com/blog/2027-memory-chip-boom-sk-hynix-samsung) — news, 2026. BI: shortage peaked 2Q26, oversupply possible in 2028; others see tightness to 2Q28 [cross-reference: URL from a sibling agent's log; not opened by E]
  - [DDR4 8Gb fixed price bottomed at $1.30 (Sep 2023)](https://www.kedglobal.com/korean-chipmakers/newsView/ked202310040013) — news, 2023-10-04. Last-cycle trough anchor: contract prices fell roughly 60-65% peak-to-trough [cross-reference: URL from a sibling agent's log; not opened by E]

**Capital tier:** T1 | **Time to first revenue:** 1-3 months (first resale) | **Gross margin estimate:** expected -45% (resale vs. cost, buying at spot); -22% even if the spot premium persists

**US manufacturability:** None: storage only.

**Who is already doing this:** Independent brokers and traders worldwide; Mobius Materials (VA) as a marketplace. Module makers' real business is already inventory timing (p1-backend).

**Wins on which axis, for which buyer:** none (timing speculation) — for whoever is short that day: brokers, CMs, system builders

**Survives a 2029 glut?:** no — A 24-month hold into the A-05 glut, bought at spot, loses more than 100% after carry (e_estimates §3).

**Fatal-flaw candidate:** A newcomer can only buy at spot (~$27/GB, ~1.7x contract) because makers allocate contract supply to strategic customers. The QoQ rate has slowed from +95% to +12.5%, so the expected 12-month net return is -46% (-22% even if the spot premium persists; e_estimates §3). Only allocation holders buying at contract see ~+7%. It is speculation with no recurring revenue and no moat.

*Possible?* yes - anyone can buy spot inventory · *Profitable?* no - negative expected value at spot; positive only for holders of contract allocation · *Doable by this founder?* marginal - doable mechanically, imprudent financially

*Business-model lenses:* recert/brokerage (trading)

### C-90 — DIMM leasing / memory-as-a-service financing for neoclouds

*Sub-branch:* Hardware financing (lessor) · *Materials sense:* c-capital

**What it is:** A lessor buys new DDR5 RDIMMs (or CXL expanders) from Penguin/SMART Modular or Kingston and leases them for 36 months at $/GB-month to neoclouds, AI-inference startups and enterprises that lack LTAs. At lease end it takes the modules back for resale through ITAD channels.

**Why it could work:** Buyers without LTAs face peak prices and allocation limits. Leasing turns a $1,300-2,064 capex per 64GB RDIMM into ~$49/month ($0.76/GB-month), which gives the lessor a 14% IRR with a $260 residual (e_estimates §4). Lenders have shown willingness to finance compute hardware such as GPUs [UNVERIFIED-training].

**Evidence:** TRL 7 · Rule 1: SUPPORTED
  - [Memory prices surging by 90% from 4Q25 (Counterpoint)](https://www.eetasia.com/memory-prices-surging-by-90-from-4q-2025/) — news, 2026-01. 64GB RDIMM contract $450 (4Q25) to >$900 (1Q26) [cross-reference: URL from a sibling agent's log; not opened by E]
  - [DDR5 server memory price tracker 2026](https://www.servnetuk.com/research/ddr5-server-memory-price-tracker-2026) — industry, 2026-08. Street 64GB DDR5 RDIMM ~$2,064 (Aug 2026) [cross-reference: URL from a sibling agent's log; not opened by E]
  - [CSPs lock supply with long-term deals (TrendForce 2Q26)](https://technews.tw/2026/03/31/ai-server-demand-drives-2q26-memory-contract-price-increase-csps-lock-supply-long-term-deals/) — news, 2026-03-31. Hyperscalers lock multi-year supply; tier-2 buyers pay the marginal price [cross-reference: URL from a sibling agent's log; not opened by E]
  - [TrendForce: supply prioritized to strategic OEMs, module makers limited](https://www.trendforce.com/research/download/RP260114IU) — industry, 2026-01-14. Allocation favours strategic customers; tier-2 buyers and module makers are limited [cross-reference: URL from a sibling agent's log; not opened by E]
  - [DDR4 8Gb fixed price bottomed at $1.30 (Sep 2023)](https://www.kedglobal.com/korean-chipmakers/newsView/ked202310040013) — news, 2023-10-04. Last-cycle trough anchor: contract prices fell roughly 60-65% peak-to-trough [cross-reference: URL from a sibling agent's log; not opened by E]

**Capital tier:** T2 | **Time to first revenue:** 6-12 months to first lease once a credit facility exists (the facility is the hard part) | **Gross margin estimate:** lessor spread a few points over cost of funds; scenario IRR -58% to +15%

**US manufacturability:** None; financing. Modules are made in Asia or assembled in the U.S. by Kingston/Penguin from foreign die.

**Who is already doing this:** OEM captive finance (Dell Financial Services, HPE Financial Services), IT lessors, GPU-backed lenders to neoclouds [UNVERIFIED-training].

**Wins on which axis, for which buyer:** $/GB-month and cash-flow timing (no capex at peak prices) — for neoclouds and AI-inference startups, mid-size enterprises without memory LTAs

**Survives a 2029 glut?:** no — Once the 2028 glut makes a new 64GB RDIMM ~$520, a lessee facing 18 more payments ($879) has every reason to walk or renegotiate. Lessor IRR falls to -29% (walk at month 18) or -58% (month 12).

**Fatal-flaw candidate:** Residual-value and counterparty risk both sit on the cycle: the lessor is long DRAM bought at peak prices and short credit on neoclouds. OEM captives with cheaper capital already lease whole servers, memory included.

*Possible?* yes - IT leasing is mature · *Profitable?* no - for a small lessor buying at 2026 prices into a 2028 glut · *Doable by this founder?* no - capital-bound

*Business-model lenses:* financing (memory-as-a-service); recert/brokerage (end-of-lease resale)

### C-91 — Authorized-aftermarket die bank for EOL legacy DRAM (title-taking LTB aggregator)

*Sub-branch:* Authorized aftermarket / lifetime supply · *Materials sense:* c-capital

**What it is:** Become a DFARS-recognized authorized aftermarket manufacturer/authorized supplier for EOL legacy DRAM (DDR3/DDR4/LPDDR4) from a Taiwanese specialty maker (Winbond, ESMT, Etron or Nanya). Buy last-time-buy wafer lots, bank die in nitrogen at an East Coast site, and package and test on demand at U.S. OSATs (Micross Apopka FL / RTP NC, QP Technologies) for defense, avionics, rail and medical OEMs that need the parts for 10-20 years. Unlike C-61, a consignment vault for OEM-owned stock, this takes title and holds OCM authorization.

**Why it could work:** DFARS 252.246-7008 and 246.870-2 make DoD contractors buy from OCMs, authorized suppliers or authorized aftermarket manufacturers before anyone else, so OCM authorization is a regulatory moat. DDR4 EOL pain is documented: Advantech steering customers off Samsung DDR4, and zero authorized stock of a Micron DDR4 part in May 2026. Model (e_estimates §5): a $600k single-part bank returns 16% IRR in the base case (sold at 3.0x die cost, 90% sold in years 3-8), -7% in the bear case and 39% in the bull case. Unit GM is 33-66%.

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [DFARS 252.246-7008 Sources of Electronic Parts (JAN 2023)](https://github.com/GSA/GSA-Acquisition-DFARS/blob/master/dita/252.246-7008.dita) — government, 2023-01. Opened by E. DoD contractors must buy from OCMs, authorized suppliers or authorized aftermarket manufacturers first; else contractor-approved suppliers under industry counterfeit standards with contractor liability; if traceability cannot be established the contractor is 'responsible for inspection, testing, and authentication' and must keep the documentation
  - [DFARS 246.870-2 Policy (counterfeit electronic part avoidance)](https://github.com/GSA/GSA-Acquisition-DFARS/blob/master/dita/246.870-2.dita) — government, 2023-01. Opened by E. All tiers must source in-production/in-stock parts from original manufacturers, authorized suppliers or authorized aftermarket manufacturers
  - [Memory shortage watch: DDR3L/DDR4 (May 2026)](https://blog.findchips.com/memory-shortage-watch-ddr3l-ddr4-may-2026/) — news, 2026-05. Zero authorized stock of a mainstream Micron DDR4 part at Newark/Avnet/Mouser; independent-market premium [cross-reference: URL from a sibling agent's log; not opened by E]
  - [Advantech response to Samsung DDR4 IC EOL](https://www.advantech.com/en/resources/news/response-measures-to-samsung-ddr4-ic-eol-announcement) — company, 2025. Industrial OEM steers customers away from Samsung DDR4 in new designs: EOL-driven lifetime-buy demand [cross-reference: URL from a sibling agent's log; not opened by E]
  - [Micross Die and Wafer flyer](https://micross.com/uploads/05827c98-1b61-4d4d-bb3c-04dc1b207e5a/Die_and_Wafer_Flyer_Rev_1_WEB.pdf) — company, unknown. Micross bills itself as the largest authorized bare-die/wafer supplier, with DRAM on its line card: an incumbent die bank [cross-reference: URL from a sibling agent's log; not opened by E]
  - [Micron Manassas 1-alpha DDR4/LP4 for defense, auto, industrial](https://www.hpcwire.com/off-the-wire/micron-advances-made-in-america-memory-with-manufacturing-expansion-in-virginia) — news, 2026-05-22. U.S.-made long-lifecycle DDR4 from Micron since 2026-05-22: incumbent for any 'U.S.-made legacy DRAM' pitch [cross-reference: URL from a sibling agent's log; not opened by E]

**Capital tier:** T2 | **Time to first revenue:** 18-30 months: OCM authorization agreement, then the first banked part reaches post-EOL demand | **Gross margin estimate:** 33-66% on units

**US manufacturability:** Die from Taiwan (or Micron Manassas if it ever sells die). Banking, packaging and test in the U.S. at Micross FL/NC, QP Technologies CA or Integra KS [UNVERIFIED-training sites].

**Who is already doing this:** Rochester Electronics (Newburyport MA; authorized aftermarket for 70+ OCMs [UNVERIFIED-training]), Micross (largest authorized die supplier), Alliance Memory (long-lifecycle brand), distributors' bonded stock.

**Wins on which axis, for which buyer:** lifecycle length and supply security: authorized, traceable legacy DRAM after EOL — for DoD sustainment programs and DMSMS offices, avionics (DO-254), rail signaling, medical-device OEMs

**Survives a 2029 glut?:** yes — Demand is driven by EOL and requalification cost, not by DDR5 prices; a glut actually cheapens LTB wafers. The risk is inventory that never sells (bear-case IRR -7%).

**Fatal-flaw candidate:** OCMs grant aftermarket authorization to proven firms with capital and quality systems (Rochester, Micross). A startup can neither win the authorization nor fund $2M+ of inventory, and without it the venture is just an independent distributor, which DFARS ranks last.

*Possible?* yes - Rochester and Micross prove the model · *Profitable?* yes - for incumbents with authorization and scale · *Doable by this founder?* no - capital, authorization and relationships are the moat

*Business-model lenses:* recert/brokerage (authorized aftermarket); defense-first; module (packaging on demand)

### C-92 — AS6171 counterfeit-detection and authentication lab for memory lots

*Sub-branch:* Test and qualification services (defense-first) · *Materials sense:* none

**What it is:** An ISO/IEC 17025-accredited East Coast lab (NJ/PA/MD defense-EMS corridor) running SAE AS6171 test methods on DRAM, NAND and NOR lots bought outside authorized channels: external visual, X-ray, XRF, decap with die-marking verification, and electrical/functional memory test. Each lot gets die-origin identification (CXMT/YMTC flagging) and a serialized web report, with a later goal of DLA qualified-testing-supplier status.

**Why it could work:** DFARS 252.246-7008 makes contractors 'responsible for inspection, testing, and authentication' whenever they buy from non-authorized sources or cannot establish traceability. FAR 52.246-26 treats used-as-new as counterfeit. The 2026 shortage pushed buyers into the independent market (zero authorized DDR4 stock, May 2026). Model (e_estimates §6): $650k capex and $478k/yr fixed cost. Breakeven is 36 lots/month at $1,400 per lot. At 60 lots/month: $1.0M revenue, 41% lab GM, $314k operating profit.

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [DFARS 252.246-7008 Sources of Electronic Parts (JAN 2023)](https://github.com/GSA/GSA-Acquisition-DFARS/blob/master/dita/252.246-7008.dita) — government, 2023-01. Opened by E. DoD contractors must buy from OCMs, authorized suppliers or authorized aftermarket manufacturers first; else contractor-approved suppliers under industry counterfeit standards with contractor liability; if traceability cannot be established the contractor is 'responsible for inspection, testing, and authentication' and must keep the documentation
  - [FAR 52.246-26 Reporting Nonconforming Items (Aug 2024)](https://github.com/GSA/GSA-Acquisition-FAR/blob/master/dita/52.246-26.dita) — government, 2024-08. Opened by E. 'Counterfeit item' includes used items represented as new and false grade, lot or date-code identification
  - [Memory shortage watch: DDR3L/DDR4 (May 2026)](https://blog.findchips.com/memory-shortage-watch-ddr3l-ddr4-may-2026/) — news, 2026-05. Zero authorized stock of a mainstream Micron DDR4 part at Newark/Avnet/Mouser; independent-market premium [cross-reference: URL from a sibling agent's log; not opened by E]
  - [Mobius Materials raises $3M (authenticated surplus-semiconductor marketplace)](https://www.prnewswire.com/news-releases/mobius-materials-raises-3m-to-combat-one-of-manufacturings-biggest-issues-amid-us-china-trade-tariffs-302643403.html) — news, 2025-12. Richmond VA marketplace with an ML authentication patent filing: incumbent in spot trading/authentication and a possible data partner [cross-reference: URL from a sibling agent's log; not opened by E]

**Capital tier:** T1 | **Time to first revenue:** 9-15 months: equipment, 17025 accreditation, first broker/EMS customers; DLA listing later | **Gross margin estimate:** 22-54% depending on lot volume

**US manufacturability:** U.S. lab services; no fab.

**Who is already doing this:** Established independent AS6171 labs and distributors' in-house labs (e.g., SMT Corp, Integra Technologies, Alter Technology [UNVERIFIED-training]); the ERAI/GIDEP reporting ecosystem; Mobius Materials' ML authentication.

**Wins on which axis, for which buyer:** supply security / authenticity (counterfeit-risk reduction with documentation) — for AS6081 independent distributors, defense EMS and primes' purchasing departments, OEMs buying broker DRAM during the shortage

**Survives a 2029 glut?:** partially — Broker buying and counterfeit volume fall once authorized stock returns (lots down maybe 30-50% [ESTIMATE]). DFARS-driven testing of obsolete parts continues.

**Fatal-flaw candidate:** A crowded, accreditation-heavy services market with entrenched labs. Below ~36 lots/month the lab loses money, and the founder cannot run it without a hired AS6171 test engineer and ~$650k.

*Possible?* yes - routine lab methods · *Profitable?* marginal - breakeven at ~36 lots/month; 41% GM at 60 · *Doable by this founder?* marginal - needs a technical hire and ~$0.65M

*Business-model lenses:* defense-first; services; data product (test-report and die-ID database)

### C-93 — 'Compliant memory' federal reseller on GSA MAS / SEWP (compliance-as-a-product)

*Sub-branch:* Federal reseller (NDAA 5949 / TAA / BAA) · *Materials sense:* none

**What it is:** A small-business federal reseller that sells memory upgrades and memory-heavy servers to agencies through GSA's Multiple Award Schedule and NASA SEWP. The pitch is 'certified U.S.-supply-chain' memory: TAA-compliant, CXMT/YMTC-free under NDAA FY2023 §5949, Micron Manassas DDR4 where available, with provenance paperwork.

**Why it could work:** §5949 bans CXMT/YMTC/SMIC content in federal purchases from 2027-12-23, with rising political salience (Senate pressure on Apple, July 2026). The Buy American Act gives small businesses a 30% evaluation preference below the TAA threshold (FAR 25.106).

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [Apple, China memory and the 2027 federal procurement ban](https://xenospectrum.com/en/apple-china-memory-federal-procurement-ban-2027/) — news, 2026-07. NDAA FY2023 Sec. 5949 ban on CXMT/YMTC/SMIC-containing products in federal buys from Dec 2027 [cross-reference: URL from a sibling agent's log; not opened by E]
  - [GSA-Acquisition-FAR repository (FAR through FAC 2025-06)](https://github.com/GSA/GSA-Acquisition-FAR) — government, 2026-03-30. Opened by E (git clone). grep of all 3,945 FAR DITA files finds no text implementing NDAA FY2023 Sec. 5949 ('covered semiconductor', CXMT, YMTC, SMIC)
  - [GSA-Acquisition-DFARS repository](https://github.com/GSA/GSA-Acquisition-DFARS) — government, 2026-06-02. Opened by E (git clone). No Sec. 5949 implementing text in 3,320 DFARS DITA files as of the 2026-06-02 snapshot
  - [FAR 4.2101 'reasonable inquiry' (Section 889)](https://github.com/GSA/GSA-Acquisition-FAR/blob/master/dita/4.2101.dita) — government, 2025-10-01. Opened by E. 'Reasonable inquiry ... excludes the need to include an internal or third-party audit': the precedent a Sec. 5949 rule would likely copy
  - [FAR 25.402 trade-agreement thresholds](https://github.com/GSA/GSA-Acquisition-FAR/blob/master/dita/25.402.dita) — government, 2025-10-01. Opened by E. WTO GPA threshold $174,000: above it Korean/Taiwanese/Japanese memory competes equally with U.S.-made
  - [FAR 25.001 Buy American COTS waiver](https://github.com/GSA/GSA-Acquisition-FAR/blob/master/dita/25.001.dita) — government, 2025-10-01. Opened by E. The domestic content test is waived for COTS items, so U.S. die gets no extra BAA credit inside a COTS module
  - [FAR 25.106 BAA evaluation factors](https://github.com/GSA/GSA-Acquisition-FAR/blob/master/dita/25.106.dita) — government, 2025-10-01. Opened by E. 20% (large business) / 30% (small business) evaluation preference for domestic offers, applicable only where TAA does not apply
  - [FAR 52.211-5 Material Requirements](https://github.com/GSA/GSA-Acquisition-FAR/blob/master/dita/52.211-5.dita) — government, 2025-10-01. Opened by E. 'New' means previously unused components; used/reconditioned supplies need contracting-officer acceptance

**Capital tier:** T1 | **Time to first revenue:** 12-18 months: GSA MAS award (needs financials and past performance), then first task orders | **Gross margin estimate:** 6-10%

**US manufacturability:** Resale only; modules may be U.S.-assembled (Kingston, Penguin) from foreign die.

**Who is already doing this:** Hundreds of federal IT VARs and SEWP holders (CDW-G, Carahsoft, many small businesses) [UNVERIFIED-training]; Micron and Kingston through their channels.

**Wins on which axis, for which buyer:** supply security / compliance documentation — for federal civilian and DoD IT buyers; prime integrators

**Survives a 2029 glut?:** partially — Compliance demand persists, but VAR margins on cheaper memory compress further.

**Fatal-flaw candidate:** No pricing power. Above $174k, TAA lets Korean, Taiwanese and Japanese memory compete equally (FAR 25.402); the BAA component test is waived for COTS (FAR 25.001); and §5949 rewards 'not Chinese', which every Samsung, SK hynix or Micron reseller already meets. Neither the FAR (through FAC 2025-06) nor the DFARS (June 2026 snapshot) yet contains any §5949 text, and the §889 precedent accepts a 'reasonable inquiry' that excludes third-party audits (FAR 4.2101). Compliance is a free checkbox, leaving a 6-10% VAR margin on $1.5-2.5M of sales per $150k of gross profit (e_estimates §7).

*Possible?* yes - standard VAR model · *Profitable?* no - commodity margin; compliance confers no premium · *Doable by this founder?* marginal - slow vehicle access, working capital ~$185-310k

*Business-model lenses:* defense-first; recert/brokerage (resale); compliance-as-a-product

### C-94 — STTR vehicle on a national-lab / university memory patent (lab-patent studio)

*Sub-branch:* University/lab patent license -> STTR -> defense Phase III · *Materials sense:* mixed:a+c

**What it is:** A small business takes low-cost options on 2-3 lab memory technologies: Sandia's HZO FeRAM and ferroelectric tunnel junctions from its trusted MESA 200mm fab, the Penn/AFRL AlScN 600 C ferroelectric-diode NVM, and Purdue's ALD In2O3 BEOL ferroelectric transistors. It files DoD/NASA STTRs with the inventing researcher as STTR PI, aiming at Phase III sole-source sales or a sublicense to space/defense memory suppliers (Frontgrade, Honeywell SSEC, BAE).

**Why it could work:** STTR lets the PI be employed by the research institution, so the founder can keep his day job while the vehicle wins non-dilutive money. Defense topics for exotic NVM exist: DARPA DV017 (~$1.2M Direct-to-Phase-II, 2026) and USAF AF254-D0806 (500 C NVM). Options cost ~$1-10k (p1-ip), and Phase III awards can be sole-source with no dollar cap. Sandia's HZO FeRAM is already at 200mm wafer scale (TRL ~4-5).

**Evidence:** TRL 4 · Rule 1: SUPPORTED
  - [Sandia: Facing radiation challenges head on](https://www.sandia.gov/research/news/evolving-semiconductor-technology-for-national-security-applications/) — government, 2026-05-13. HfO2/HZO rad-hard FeRAM at 200mm and binary/32-state FTJs integrated in Sandia's trusted MESA fab (LDRD): TRL ~4-5 national-lab memory IP [cross-reference: URL from a sibling agent's log; not opened by E]
  - [Turning up the heat on data storage (Penn + AFRL AlScN)](https://www.engineering.upenn.edu/stories/turning-up-the-heat-on-data-storage/) — news, 2024-05. AlScN ferroelectric-diode NVM operating at 600C (Nature Electronics 2024); Penn/AFRL co-invention [cross-reference: URL from a sibling agent's log; not opened by E]
  - [Purdue 3-tier monolithic 3D ALD In2O3 platform on 200mm](https://engineering.purdue.edu/ECE/News/2026/purdue-researchers-build-3d-chip-platform-for-faster-more-efficient-ai-computing) — news, 2026-09-16. ALD In2O3 BEOL transistors incl. ferroelectric tiers on 200mm Si (>100,000 devices across 52 dies) [cross-reference: URL from a sibling agent's log; not opened by E]
  - [DARPA SBIR DPA26BZ04-DV017 Non-Volatile Memory for Extreme Environments](https://www.darpa.mil/research/programs/non-volatile-memory-extreme-environments) — government, 2026-07. ~$1.2M Direct-to-Phase-II memory topic, opened 2026-07-22 and closed 2026-08-19 [cross-reference: URL from a sibling agent's log; not opened by E]
  - [USAF SBIR AF254-D0806 500C-capable kB-scale NVM](https://www.sbir.gov/topics/12036) — government, 2025. USAF topic citing ferroelectric-diode memory stable to 600C [cross-reference: URL from a sibling agent's log; not opened by E]
  - [Everspin earns $40M MRAM deal for defense memory services](https://electronics360.globalspec.com/article/23702/everspin-earns-40-million-mram-deal-for-defense-memory-services) — news, 2026-04. Defense pays for on-shore memory capability through prime subcontracts (Amentum), awarded to an incumbent with a fab [cross-reference: URL from a sibling agent's log; not opened by E]

**Capital tier:** T1 | **Time to first revenue:** ~46 months to first Phase III/customer revenue if every step succeeds the first time; grants before that are funding, not revenue (A-04) | **Gross margin estimate:** n/a until product; Phase III device sales 50-70% if they come

**US manufacturability:** Sandia MESA (trusted, but a government fab not open for production); SkyWater S130 / Fab 25 for a commercial path. Bayh-Dole and DOE U.S.-manufacture preferences align with U.S. production.

**Who is already doing this:** C-06 (Sandia HZO FeRAM chip) and C-07 (AlScN license plus STTR) card the device plays. Incumbents: Infineon rad-hard F-RAM, Frontgrade/Everspin Toggle MRAM. Many university spinouts run this STTR pattern.

**Wins on which axis, for which buyer:** non-volatility plus radiation/temperature tolerance (supply security for space and hypersonics) — for AFRL/DARPA program offices, space primes, hypersonic and Venus/geothermal sensor integrators

**Survives a 2029 glut?:** yes — Rad-hard and extreme-environment NVM is priced per part to defense buyers and is indifferent to DDR5 prices.

**Fatal-flaw candidate:** It is the grant farm the founder says he does not want. The chance of customer revenue is ~3% per topic attempt and ~15% after five (e_estimates §8). First revenue lands ~46 months out, past the 36-month ceiling. The vehicle depends on a lab PI and a fab it does not control. Tech-transfer listings and patent numbers could not be verified this session.

*Possible?* yes - option/STTR/Phase III mechanics are routine; device TRL 3-5 · *Profitable?* marginal - niche defense NVM can be profitable for whoever reaches Phase III, rarely within 4 years · *Doable by this founder?* marginal - he can run the company shell and proposals, not the science

*Business-model lenses:* university/lab patent license; defense-first; fabless->foundry (later)

### C-95 — SBA/search-fund acquisition of a small memory reseller at peak earnings - tempting, dangerous

*Sub-branch:* Acquisition (ETA) of a memory business · *Materials sense:* c-capital

**What it is:** Buy an existing U.S. server-memory reseller, used-memory buyer or small module brand (the A-Tech / NEMIX / Memory4Less / TechMikeNY class [UNVERIFIED-training names; none confirmed for sale]) with ~$1.2M of 2026 EBITDA. Finance it 90% with an SBA 7(a) loan and 10% equity from the founder and co-investors, then grow it with software (pricing, provenance ledger, e-commerce).

**Why it could work:** Revenue is immediate: day-one recurring B2B customers, inventory and supplier relationships. A software operator can improve a sleepy business. The Crucial exit (announced Dec 2025) reshuffled the consumer/SMB memory channel, and DDR4 prices are still rising.

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [Micron announces exit from Crucial consumer business](https://www.storagenewsletter.com/2025/12/05/micron-announces-exit-from-crucial-consumer-business/) — news, 2025-12-05. Crucial exit announced 2025-12-03: the consumer/SMB memory channel is reshuffling [cross-reference: URL from a sibling agent's log; not opened by E]
  - [DDR4 prices rise as shortages intensify through 2028 (Barclays)](https://www.guru3d.com/story/ddr4-memory-prices-now-also-rise-as-dram-supply-shortages-intensify-through-2028/) — news, 2026-10. DDR4 contract +24% over the 3 months to Oct 2026; shortage into 2028 [cross-reference: URL from a sibling agent's log; not opened by E]
  - [DDR4 8Gb fixed price bottomed at $1.30 (Sep 2023)](https://www.kedglobal.com/korean-chipmakers/newsView/ked202310040013) — news, 2023-10-04. Last-cycle trough anchor: contract prices fell roughly 60-65% peak-to-trough [cross-reference: URL from a sibling agent's log; not opened by E]
  - [Analyst cycle views incl. Bloomberg Intelligence bear case](https://www.kucoin.com/blog/2027-memory-chip-boom-sk-hynix-samsung) — news, 2026. BI: shortage peaked 2Q26, oversupply possible in 2028; others see tightness to 2Q28 [cross-reference: URL from a sibling agent's log; not opened by E]

**Capital tier:** T2 | **Time to first revenue:** Revenue on day one after close, but sourcing, diligence and SBA close take ~6-9 months | **Gross margin estimate:** 15-25% (reseller margins)

**US manufacturability:** Existing U.S. operation (testing and resale); no fab.

**Who is already doing this:** Search funds and ETA buyers generally; ITAD consolidators such as Iron Mountain ALM (ITRenew) [UNVERIFIED-training].

**Wins on which axis, for which buyer:** time-to-revenue (acquired), not a product axis — for the target's existing customers: SMB IT, refurbishers, MSPs, homelab/gaming buyers

**Survives a 2029 glut?:** no — At 3.5x shortage EBITDA, debt service is ~$612k/yr. DSCR is 1.96 in 2026, 0.65 in a normal year and 0.33 in a glut (e_estimates §9), which means default with an SBA personal guarantee.

**Fatal-flaw candidate:** Buying cyclical peak earnings with leverage. Shortage-inflated EBITDA reverts, and the SBA personal guarantee ties the founder's personal assets to the 2028 glut.

*Possible?* yes - SBA acquisitions of small distributors are routine · *Profitable?* no - at 2026 prices; maybe yes if bought in the trough · *Doable by this founder?* no - equity gap and guarantee risk

*Business-model lenses:* recert/brokerage; module/appliance (acquired); SaaS (bolt-on)

### C-96 — Acquire the 3D XPoint/Optane IP estate and license it (business-model Optane revival) - tempting, dead

*Sub-branch:* IP-estate acquisition / licensing · *Materials sense:* c-capital

**What it is:** Buy or exclusively license the Intel/Micron 3D XPoint patent and know-how estate plus leftover Optane inventory, then run a licensing program aimed at CXL-memory and storage-class-memory makers, or revive a product through a foundry. The pitch: 'DRAM is 4-6x more expensive; the Optane tier is back.'

**Why it could work:** With DRAM at $16-27/GB, a ~$4-8/GB persistent tier looks attractive again, and the estate, which cost Intel more than $7B, is idle.

**Evidence:** TRL 5 · Rule 1: SUPPORTED
  - [Micron ends 3D XPoint (2021-03-16)](https://www.nasdaq.com/press-release/micron-updates-data-center-portfolio-strategy-to-address-growing-opportunity-for) — company, 2021-03-16. 'insufficient market validation to justify the ongoing high levels of investments required to commercialize 3D XPoint at scale' [cross-reference: URL from a sibling agent's log; not opened by E]
  - [Micron pulls the plug on 3D XPoint](https://www.theregister.com/2021/03/17/micron_pulls_the_plug_on/) — news, 2021-03-17. $545M of XPoint/Lehi underutilization charges over four quarters [cross-reference: URL from a sibling agent's log; not opened by E]
  - [Micron sells Lehi fab to Texas Instruments](https://www.anandtech.com/show/16800) — news, 2021-06-30. Only XPoint fab sold to TI for $900M cash plus ~$600M of tools, below book; converted to analog [cross-reference: URL from a sibling agent's log; not opened by E]
  - [Intel 10-Q Q2-2022 (Optane wind-down)](https://www.sec.gov/Archives/edgar/data/50863/000005086322000030/intc-20220702.htm) — company, 2022-07. Optane wind-down begun; $559M inventory impairment [cross-reference: URL from a sibling agent's log; not opened by E]
  - [Persistent memories without Optane (Coughlin/Handy, SNIA SDC22)](https://www.snia.org/sites/default/files/2025-05/SNIA-SDC22-Coughlin-Handy-Persistent-Memories-Without-Optane-Where-Would-We-Be.pdf) — conference, 2022. >$7B cumulative Intel Optane losses [cross-reference: URL from a sibling agent's log; not opened by E]
  - [Weebit Nano expands licensing agreements](https://www.weebit-nano.com/news/press-releases/weebit-nano-expands-licensing-agreements-with-key-customers-three-customer-chip-designs-taped-out-to-date/) — company, 2026-07. The best-run independent memory-IP licensor guides >=A$13.5M FY26 revenue after ~10 years: out-licensing is a decade-long path [cross-reference: URL from a sibling agent's log; not opened by E]

**Capital tier:** T3 | **Time to first revenue:** 60+ months; only via a licensee that would also need a new line | **Gross margin estimate:** licensing ~90% if a licensee existed; none expected

**US manufacturability:** No XPoint line exists anywhere: Lehi was sold to TI and converted to 65/45nm analog.

**Who is already doing this:** Nobody. SanDisk's 3D-matrix/HBF work and imec research are the nearest descendants (see C-25, C-25, C-53).

**Wins on which axis, for which buyer:** $/GB vs. DRAM plus persistence — for CXL memory-tier buyers (hyperscalers, SAP HANA/database hosts)

**Survives a 2029 glut?:** no — At glut DDR5 prices ($6.4/GB, $1.6 severe), the XPoint cost gap, which never paid off even against $3-5/GB DRAM, closes again.

**Fatal-flaw candidate:** IP without a line is worthless. No fab runs XPoint and rebuilding one is T3-T4. Micron and Intel both exited (Micron cited 'insufficient market validation'), and out-licensing memory IP takes a decade even for the best-run licensor (Weebit is still sub-scale).

*Possible?* marginal - the IP could be bought; the product cannot be made without a new line · *Profitable?* no · *Doable by this founder?* no

*Business-model lenses:* IP licensing (acquired estate); fabless->foundry (impossible)

### C-97 — CXL memory-tiering integration practice (consulting -> managed tuning)

*Sub-branch:* Services -> SaaS · *Materials sense:* c-capital

**What it is:** A services firm that assesses, deploys and tunes CXL Type-3 memory expansion and tiering on Granite Rapids/Turin servers. Hardware: Micron CZ-series, Samsung CMM-D or SK hynix CMM expanders, and Marvell Structera- or Astera Leo-based cards. Software: Linux weighted-interleave and DAMON tiering, SK hynix HMSDK. Clients are HPC centers, in-memory database hosts and EDA shops, and engagements convert into a managed tuning and monitoring subscription.

**Why it could work:** 1 TB of new DDR5 RDIMM costs ~$20.8k per node at 4Q26 prices (e_estimates §12). CXL lets buyers add cheaper or reused capacity, including DDR4 behind Structera-class controllers, without buying top-bin DIMMs. Mainline Linux still has CXL gaps (Dynamic Capacity, multi-host sharing), so integration know-how is scarce. Practice revenue: ~$83k/yr part-time, ~$248k full-time at $225/h.

**Evidence:** TRL 7 · Rule 1: SUPPORTED
  - [Linux CXL maturity map](https://github.com/torvalds/linux/blob/master/Documentation/driver-api/cxl/maturity-map.rst) — industry, 2026-10-31. Mainline Linux still lacks Dynamic Capacity Device support and multi-host sharing: CXL integration is real but early [cross-reference: URL from a sibling agent's log; not opened by E]
  - [SK hynix Heterogeneous Memory SDK (HMSDK) v4.0](https://github.com/skhynix/hmsdk) — industry, 2025-11-03. Free vendor CXL tiering SDK; weighted interleave upstream in Linux 6.9: tooling is free, value is in integration [cross-reference: URL from a sibling agent's log; not opened by E]
  - [Memory prices surging by 90% from 4Q25 (Counterpoint)](https://www.eetasia.com/memory-prices-surging-by-90-from-4q-2025/) — news, 2026-01. 64GB RDIMM contract $450 (4Q25) to >$900 (1Q26) [cross-reference: URL from a sibling agent's log; not opened by E]

**Capital tier:** T0 | **Time to first revenue:** 6-12 months: first paid assessment at an HPC or database shop | **Gross margin estimate:** 50-70% (services)

**US manufacturability:** Services; hardware from Micron/Samsung/SK hynix/Astera/Marvell; no fab dependency.

**Who is already doing this:** OEM professional services (Dell, HPE, Supermicro), memory vendors' field engineers, Liqid/GigaIO, HPC integrators; MemVerge has pivoted toward GPU cluster software (per B) [UNVERIFIED-training for the rest].

**Wins on which axis, for which buyer:** $/GB of usable capacity (cheaper or reused tier) for capacity-bound workloads — for university and DOE HPC centers, SAP HANA/in-memory database hosts, EDA and genomics shops

**Survives a 2029 glut?:** partially — The DRAM-saving pitch shrinks when DDR5 falls 60% (1 TB = $8.3k), but capacity and bandwidth expansion for >2 TB nodes remains.

**Fatal-flaw candidate:** The founder is not a Linux-kernel/CXL engineer, vendors give integration away to sell hardware, and CXL deployments are still early and lumpy. A practice earns consulting income, not a scalable product.

*Possible?* yes - CXL 2.0 expanders and Linux tiering ship today · *Profitable?* marginal - services margins, small and lumpy demand · *Doable by this founder?* marginal - needs a technical partner

*Business-model lenses:* services -> SaaS; module/appliance (VAR)

### C-98 — Memory patent expiry and litigation radar

*Sub-branch:* IP intelligence data product · *Materials sense:* none

**What it is:** A subscription web app that tracks memory-relevant U.S. patents (DRAM module/PMIC, MRAM, ReRAM, FeRAM, IGZO, 3D DRAM). It computes expiry dates (term adjustments, terminal disclaimers, maintenance-fee lapses), follows assignment changes and PTAB/ITC/district-court dockets (e.g., ITC 337-TA-1487 Avalanche v. Everspin; the Netlist RDIMM/PMIC cases), and provides FTO checklists per product type. It is built from free USPTO bulk data plus PACER/ITC EDIS.

**Why it could work:** Every hardware concept in this study has an FTO gate: Netlist PMIC for DDR5 modules, SEL for IGZO, the ITC case for Everspin STT. One FTO opinion costs $10-30k and NPE defense $0.6-4M (p1-ip). Everspin spent $6.0M on litigation in one quarter. Small module makers, recert firms and memory startups need cheap monitoring. 25 subscribers x $4.8k = $120k ARR at ~85% GM.

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [USITC institutes 337-TA-1487 (Avalanche v. Everspin, MRAM)](https://www.usitc.gov/press_room/news_release/2026/er0227_68226.htm) — government, 2026-02-27. Active memory patent fight: an exclusion order is sought against imported Everspin STT-MRAM [cross-reference: URL from a sibling agent's log; not opened by E]
  - [Everspin Q3 2026 results (8-K Ex 99.1)](https://www.sec.gov/Archives/edgar/data/0001438423/000162828026067890/mram-20260930xexx991.htm) — company, 2026-10-28. $6.0M litigation cost inside $18.5M of quarterly opex at a $20.6M-revenue memory company; licensing/services only $3.7M [cross-reference: URL from a sibling agent's log; not opened by E]

**Capital tier:** T0 | **Time to first revenue:** 6-12 months: first subscriptions from module makers / IP counsel | **Gross margin estimate:** 80-90%

**US manufacturability:** Software.

**Who is already doing this:** Unified Patents, RPX, Docket Navigator, Lex Machina, PatSnap, LexisNexis PatentSight, Google Patents (free) [UNVERIFIED-training].

**Wins on which axis, for which buyer:** risk reduction (lower FTO and litigation-monitoring cost) — for small U.S. module makers, recert/ITAD firms, CXL and memory startups, IP counsel, memory investors

**Survives a 2029 glut?:** partially — Litigation and FTO needs do not depend on the cycle, but the buyer set (small memory firms) shrinks in a glut.

**Fatal-flaw candidate:** Crowded by well-funded patent-analytics incumbents and free Google Patents. The memory niche is too small to pay, and buyers facing real risk hire counsel rather than a dashboard.

*Possible?* yes · *Profitable?* no - small niche against entrenched analytics vendors · *Doable by this founder?* yes - T0, but likely a feature of C-86 or an internal tool rather than a business

*Business-model lenses:* data product; SaaS; IP licensing (intelligence)
