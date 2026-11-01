# 02 — CONCEPTS

**98 concept cards** generated in Phase 2 by parallel ideation agents (one per branch A–E; branch A split three ways because it is the largest), then deduplicated. Merges are noted on each card. Current status (after the Phase 3 kill pass and scoring, both Phase 5 red-team rounds, and the Phase 7 gate): **15 alive, 83 killed**; each killed card shows its rule and reason. Scores are in `03_SCORING.md`. The machine-readable copy is `concepts.csv`. Device $/GB comparisons are in `models/device_cost_compare.py`.

Legend: TRL = technology readiness level 1–9 · Tier T0 <$50k, T1 $50k–$2M, T2 $2M–$50M, T3 $50M–$1B, T4 >$1B · materials sense: (a) material system, (b) process, (c) capital (mission rule 5).

## Deduplication log

- Reviewed and kept SEPARATE (distinct business model, buyer or technology): C-94 (working id E.10) lab-patent STTR studio vs C-06 (working id A1.06) HZO FeRAM and C-07 (working id A1.07) AlScN (portfolio/option vehicle vs single-device company); C-61 (working id C.04) consignment LTB vault vs C-91 (working id E.07) title-taking die bank vs C-72 (working id C.15) buying co-op (service vs inventory owner vs agency); C-85 (working id E.01) DIMM health subscription vs C-62 (working id C.05) graded recovered RDIMM sales vs C-79 (working id D.08) TB-RAM rental (subscription vs product vs rental); C-93 (working id E.09) compliant-memory federal reseller vs C-64 (working id C.07) provenance verification (reseller margin vs verification software); C-96 (working id E.12) Optane IP-estate licensing vs C-25 (working id A2.10) Optane device revival; C-44 (working id B.01) recovered-DDR4 CXL expander vs C-56 (working id B.14) Manassas-DDR4 trusted CXL expander; C-80 (working id D.09) OEM cost alerts vs C-86 (working id E.02) licensed escalation index vs C-83 (working id D.13) newsletter; C-13 (working id A1.13) emerging-memory qual lab vs C-92 (working id E.08) AS6171 counterfeit lab vs C-18 (working id A2.03) MRAM radiation data; C-97 (working id E.13) CXL tiering practice vs C-75 (working id D.03) KV-cache integration vs C-45 (working id B.02) KV pool appliance; C-12 (working id A1.12) F-RAM NVSRAM-replacement modules vs C-16 (working id A2.01) MRAM PLP reference design; C-55 (working id B.13) CIM module integration vs C-24 (working id A2.09) RRAM CIM chip design.
- Evidence caveat carried into Phase 3: the session's shared WebSearch budget (200/turn) was exhausted during ideation; branches C, D, E and parts of A3/B ran with zero or few searches, citing other agents' logged URLs, GitHub/PyPI, and training knowledge tagged UNVERIFIED. The Phase 3 adversarial audit re-checks evidence under explicit search quotas.
- C-64 (working id C.07) + C-64 (working id D.11) → kept C-64 (working id C.07) (CleanBOM-5949: memory-provenance verification for federal IT sellers): Same product: SPD/JEP106 fleet scan + attestation + lab confirmation for NDAA FY2023 §5949 memory provenance. C-64 (working id C.07) kept (adds the partner-lab and attestation layer); C-64 (working id D.11)'s open-core scanner becomes its acquisition funnel.
- C-25 (working id A2.10) + C-25 (working id B.09) → kept C-25 (working id A2.10) (3D XPoint / PCM Crosspoint Revival for the CXL Memory Tier): Same idea: rebuild a 3D XPoint/PCM crosspoint storage-class memory as a CXL tier. Kept the device-branch card (fuller device physics + cost inputs).
- C-51 (working id B.08) + C-51 (working id A2.12) → kept C-51 (working id B.08) (Persistent CXL Log Card (post-Optane PMem for WAL/journals)): Same product category and buyer: post-Optane persistent write-ahead-log/journal card (MRAM or DRAM+NAND+supercap behind PCIe/CXL). C-51 (working id B.08) kept as the broader formulation; C-51 (working id A2.12)'s MRAM-only variant is one implementation option.
- C-73 (working id D.01) + C-73 (working id D.04) → kept C-73 (working id D.01) (Memory FinOps Audit for Cloud SaaS): C-73 (working id D.04) (Redis->Valkey/Dragonfly cache sizing) is a narrower instance of C-73 (working id D.01) (cloud memory FinOps audit for SaaS); same buyer, same motion. Merged.

## A. Device & materials (43 cards)

### C-01 — OS-eDRAM: IGZO/IWO 2T0C gain-cell memory IP on a U.S. 200mm foundry — ☠ KILLED (SCORE<55: Scored 48.0/100 default (rank 36/40), 51.7 moonshot. Weakest: time to revenue 1/5 (48 months (36-60): 18-24 mo module development plus 12-18 mo PBTI/retention qualification before first NRE, past the 36-month hard ceiling.); founder-fit 1/5 (Process-module development and reliability qualification need a device/process CTO and a SkyWater JDA from day one; the founder only adds a ); tech feasibility 2/5 (TRL 4: imec 2T0C cells (IEDM 2020/21) only; PBTI reaches 5-yr at 95C in lab (IEDM 2025 snippet), no 10-yr lifetime, and IWO retention falls ). Scorer verdicts — founder: A $15-40M process-module science project with revenue around 2030 that a pure-CMOS gain cell undercuts; not this founder's venture. | vc: A process-module science project with $15-40M and 48 months to first revenue to win small 130nm royalties, while C-32 serves the same buyer with no new module: pass. | veteran: Real physics on the wrong substrate: no U.S. fab has an oxide module, contamination rules force a dedicated tool set, PBTI is still lab-grade, and a zero-mask Si gain cell serves the same buyer, so it's a 5-year)

*Sub-branch:* Oxide-semiconductor DRAM (embedded gain cell) · *Materials sense:* mixed:a+b+c

**What it is:** Replace '~4-5x the bit density of 130nm SRAM' with '~2-4x the bit density of 130nm SRAM'

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
  - [imec IEDM 2025 IGZO PBTI paper record (H/O anneal; 5-yr lifetime at 95C, 1.2 V overdrive for eDRAM)](https://imec-publications.be/handle/20.500.12860/59908) — conference, 2025-12. PBTI lifetime reaches the 5-yr target at 95C in lab (via search snippet; attribution of the abstract to this handle is likely but not confirmed; fetch blocked)
  - [imec: Capacitor-less IGZO-based DRAM cell with excellent retention, endurance and gate length scaling](https://www.imec-int.com/en/articles/capacitor-less-igzo-based-dram-cell-excellent-retention-endurance-and-gate-length-scaling) — industry, 2021-12. Primary imec write-up of the IEDM 2021 2T0C results (via search snippet)

**Capital tier:** T2 | **Time to first revenue:** 36-60 months: dedicated BEOL tool set and module development at SkyWater (18-24 mo), test chip and 5-10 yr PBTI/retention qualification (12-18 mo), then first NRE/license from an edge-AI or defense ASIC customer | **Gross margin estimate:** 65-85% blended (early revenue is NRE/test-chip support at lower margin; royalties on 130nm volumes come later)

**US manufacturability:** SkyWater Bloomington MN (S130) or Fab 25 Austin TX (130-65nm), 200mm. No oxide-semiconductor module exists at either (no announcement found 2026-11). Needs dedicated IGZO sputter or In2O3 ALD tools (~$4-10M) because of In/Ga/Zn contamination policy. Prototyping at Purdue Birck (200mm oxide BEOL, 2026-09) or NY CREATES Albany.

**Who is already doing this:** imec (2T0C program since IEDM 2020), Kioxia, IMECAS, Macronix (3D 2T0C), Georgia Tech/Shimeng Yu (IWO eDRAM), Notre Dame/Datta (IWO 2T), Purdue/Ye & Li (ALD In2O3 3-layer 200mm), SEL (DOSRAM / OS-LSI; dominant oxide-semiconductor patent estate). Competing embedded memories already at U.S. foundries: Weebit ReRAM (SkyWater S130), MRAM at GlobalFoundries.

**Wins on which axis, for which buyer:** standby power per bit vs SRAM; ~2-4x on-die density vs 130nm SRAM; write endurance (>1e11) and write energy vs SkyWater-qualified ReRAM for scratchpad/activation memory — for Always-on edge-AI ASICs (keyword spotting, vision wake-up, sensor fusion) and DoD/onshore sensor ASICs on 130-65nm U.S. nodes that are SRAM-limited

**Survives a 2029 glut?:** yes — Priced against on-die SRAM/MRAM/ReRAM, not DDR5; a DDR5 price collapse does not change an ASIC's on-die memory choice.

**Fatal-flaw candidate:** No U.S. foundry offers an oxide-semiconductor module. Adding one means dedicated tools ($4-10M) plus ~$10-30M and 3+ years of qualification [ESTIMATE]. PBTI is improving (imec IEDM 2025 abstract: 5-yr lifetime at 95C, 1.2 V overdrive, via snippet), but no 10-yr lifetime is shown, and IWO retention falls to ~300 ms at 85C, so refresh is mandatory. ASIC teams can already pick qualified Weebit ReRAM on S130, or a pure-CMOS Si gain cell (C-32) that needs no new module. SEL's estate is an FTO risk. Royalties on 130nm volumes are small.

*Possible?* yes - cells demonstrated on 300mm, oxide BEOL demonstrated on a U.S. 200mm line (Purdue) · *Profitable?* marginal - royalties on low-volume 130nm ASICs are small; the real money needs a 28nm-or-better foundry partner · *Doable by this founder?* no - process-module development and reliability qualification are far beyond <$50k and a day job

*Business-model lenses:* IP licensing; fabless->foundry; university/lab patent license (Georgia Tech/Notre Dame IWO, Purdue In2O3); defense-first

### C-02 — Standalone IGZO 2T0C DRAM die on a depreciated U.S. 200mm line (commodity DRAM substitute) — ☠ KILLED (R4-NO-WINNING-AXIS: The card's own model puts standalone 4-tier IGZO 2T0C on 130nm at ~$336/GB. Against the canonical decks that is 21x the 4Q26 DDR5 contract price ($15.99), 52x the glut price ($6.40) and ~205x incumbent cost ($1.64). The card's '12x' used $27 spot. Its named buyer (industrial/legacy DDR4) pays for $/GB, and the card's wins_axis is 'none'. It would also take T3 capital to try. Even the hypothetical 300mm 28nm 4-tier version ($11.8/GB) is 1.8x the glut price and 7x incumbent cost, on a line no U.S. foundry offers.)

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

**Survives a 2029 glut?:** no — At ~$336/GB it is 21x the 4Q26 contract price ($15.99/GB) and 52x the canonical glut price ($6.40/GB), against an incumbent cost of $1.64/GB (~205x).

**Fatal-flaw candidate:** 130nm lithography gives ~120x lower bit density than 1b DRAM (0.0035 vs 0.436 Gb/mm2 with 4 tiers); stacking recovers only linear factors.

*Possible?* yes - physics works (2T0C cells and 4-tier stacks are demonstrated) · *Profitable?* no - $/GB ~21x the DDR5 contract price today, ~52x the glut price, ~205x incumbent cost · *Doable by this founder?* no

*Business-model lenses:* module maker; fabless->foundry (both fail)

### C-03 — IGZO memory printed on idle display-fab glass — ☠ KILLED (R4-NO-WINNING-AXIS: The card's own scratch model gives ~2.3 GB per Gen 8.5 sheet and ~$266/GB before bonding, with microsecond access. That is 17x the 4Q26 contract price and 42x the glut price, and the card lists wins_axis 'none for RAM' and buyer 'none'. The premise also collapses in the U.S.: there is no Gen-scale LCD/OLED/oxide-TFT panel fab (01_LANDSCAPE 6.1 row 17; Foxconn Wisconsin never built), so 'idle display fab' means an Asian fab. That is a secondary FACT-COLLAPSE.)

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

**Survives a 2029 glut?:** no — ~$266/GB before bonding is 17x the 4Q26 contract price ($15.99) and 42x the glut price ($6.40), with microsecond latency.

**Fatal-flaw candidate:** Micrometer design rules => ~100,000x lower density than DRAM, plus no U.S. line exists.

*Possible?* marginal - TFT memory on glass is feasible but useless as RAM · *Profitable?* no · *Doable by this founder?* no

*Business-model lenses:* module maker; display-fab partnership (none in U.S.)

### C-04 — OCTRAM-class 4F2 IGZO-on-capacitor low-refresh DRAM as a U.S. second source — ☠ KILLED (R3-FAB/T4: OCTRAM is a 4F2 IGZO transistor built on a high-aspect-ratio DRAM capacitor, so it needs a DRAM capacitor process. In the U.S. only Micron (Boise, Manassas, Clay) has one, and all of it is captive (01_LANDSCAPE 6.1 rows 1-3). The card itself sets capital at T4 and 84+ months, and Kioxia/Nanya do not offer the IP for license. Even at demo pitch the card's $8.4/GB is 5.1x incumbent cost ($1.64) and 1.3x the glut price.)

*Sub-branch:* Oxide-semiconductor DRAM (4F2 1T1C) · *Materials sense:* a-material

**What it is:** License Kioxia and Nanya's OCTRAM (a vertical cylindrical InGaZnO access transistor built on top of a high-aspect-ratio DRAM capacitor, 4F2) and have it produced for U.S. low-power DRAM buyers. The product would be a low-refresh LPDDR-class part for defense and IoT.

**Why it could work:** Replace '~3x DDR5's estimated ~$2.7/GB cost' with '~5.1x incumbent DDR5 1-beta cost ($1.64/GB) and 1.3x the $6.40 glut price'

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

### C-05 — License NEO Semiconductor 3D X-DRAM and build it in the U.S. — ☠ KILLED (R3-FAB/T4: Producing 3D X-DRAM needs a 3D-NAND-class fab ($10B-class, T4). No volume 3D NAND fab operates in the U.S., and NEO licenses to memory makers, so a startup cannot take the licensee seat. The evidence is also weak on R1. It is a single-cell, company-reported PoC (NYCU/TSRI test chips) with no peer-reviewed array data, and measured retention (>1 s at 85C) is ~450x below NEO's own earlier TCAD claim (>450 s).)

*Sub-branch:* 3D DRAM (vertically stacked, IGZO variants) · *Materials sense:* mixed:a+b

**What it is:** Take a license to NEO Semiconductor's (San Jose) 3D X-DRAM (1T1C, or 3T0C with IGZO channels), built with a modified 3D-NAND flow, and stand up or partner on a U.S. 3D-NAND-class line to make it. This is the '3D NAND economics for DRAM' bet.

**Why it could work:** NEO claims ~10x DRAM density (up to 512Gb), <10 ns, >1e14 endurance and >1 s retention at 85C (company-reported PoC, Apr 2026). At the claimed density the scratch model gives ~$1.2/GB, which would be transformative if real. The big IDMs are converging on 3D: Samsung 16-tier VS-DRAM (VLSI 2026), SK hynix 5-layer at 56.1% yield (2024, needs 32-192 layers), Kioxia 8-layer IGZO stack, IMECAS 4-layer 2T0C.

**Evidence:** TRL 3 · Rule 1: SUPPORTED-WEAK (company-reported single-cell PoC; no peer-reviewed array data)
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

*Possible?* unproven - single-cell PoC only; the 10x-density claim rests on unbuilt multi-layer arrays · *Profitable?* no - not for us · *Doable by this founder?* no

*Business-model lenses:* IP licensing (wrong side of the table); fabless->foundry (no foundry)

### C-06 — U.S.-made HZO FeRAM family (1-16 Mb, rad-hard option) via SkyWater + Sandia — ☠ KILLED (SCORE<55: Scored 50.0/100 default (rank 34/40), 53.3 moonshot. Weakest: time to revenue 1/5 (54 months (42-72) to first industrial/eval sales; QML-V for the space buyer adds another 1-2 years.); founder-fit 1/5 (Needs a memory designer, a reliability engineer and $10-30M; the card itself rates founder-doability 'no'.); capital 2/5 (T2: an HZO module at SkyWater plus a memory design and reliability team, ~$10-30M before the first sale.). Scorer verdicts — founder: A third-source FeRAM chip company in an incumbent-owned niche whose 'onshore' pitch fails because Infineon's die is already made in Dallas; it cannot be funded from a day job. | vc: Optane-style capital burn for a third-source slot in a hundreds-of-$M niche where Infineon already ships U.S.-fabbed QML-V F-RAM and HZO still trails PZT on endurance and hot retention. | veteran: HZO is the right ferroelectric and the physics is sound, but the 'onshore second source' story collapses because Infineon's F-RAM is already fabbed in Dallas, and a 54-month T2 module build makes this a funded-t)

*Sub-branch:* Ferroelectric (HfZrO 1T1C FeRAM) · *Materials sense:* mixed:a+c

**What it is:** A fabless company designs a family of hafnium-zirconium-oxide 1T1C FeRAM chips (SPI/QSPI and parallel, 1-16 Mb, plus rad-hard variants). The HZO capacitor module would be built on SkyWater's 130nm line (Bloomington MN or Fab 25 Austin), with rad-hard variants co-developed with or licensed from Sandia, which integrated HZO FeRAM into its trusted MESA fab at 200mm (May 2026). It sells an onshore second source to Infineon's PZT F-RAM.

**Why it could work:** HZO is ALD-deposited and CMOS-friendly (no PZT lead contamination; ~2-3 extra masks, by analogy to TI's 2-mask FRAM on 130nm) and radiation hard (heavy-ion data; Sandia program). Space/defense F-RAM is close to sole-source (Infineon QML-V 2Mb). Wafers: ~$1,400 per 200mm [ESTIMATE]. This is a supply-security play, not a $/GB play: the scratch model is ~$770/GB because these are Mb-class parts.

**Evidence:** TRL 4 · Rule 1: SUPPORTED
  - [A highly reliable 1.8 V 1 Mb Hf0.5Zr0.5O2-based 1T1C FeRAM array with 3-D capacitors (IEDM 2023)](https://fis.tu-dresden.de/portal/en/publications/a-highly-reliable-18-v-1-mb-hf05zr05o2based-1t1c-feram-array-with-3d-capacitors%28e6411421-d8d0-4f39-97d3-03a6d18e3513%29.html) — conference, 2023-12. 1 Mb HZO 1T1C FeRAM: 1e11 endurance, 1-month retention at 85C
  - [Sandia: Facing radiation challenges head on](https://www.sandia.gov/research/news/evolving-semiconductor-technology-for-national-security-applications/) — government, 2026-05. HfO2/HZO rad-hard FeRAM integrated into Sandia's trusted MESA fab; FeRAM at 200mm scale; binary and 32-state FTJs
  - [Heavy-ion irradiation of ferroelectric hafnia NVM](https://publica.fraunhofer.de/handle/publica/456991) — peer-reviewed, unknown. Ferroelectric hafnia NVM devices show excellent radiation hardness
  - [Infineon 5962R1821601VXC rad-hard 2Mb serial F-RAM (QML-V)](https://infineon.com/cms/en/product/memories/radiation-hardened-high-reliability-memories/space-memories/5962r1821601vxc) — company, 2022-04. Incumbent PZT F-RAM: TID >150 krad(Si), SEL immune, 1e13 cycles, >100-yr retention at 85C
  - [Infineon EXCELON F-RAM family](https://infineon.com/cms/en/product/memories/f-ram-ferroelectric-ram/excelon-f-ram) — company, unknown. Shipping F-RAM 1-16 Mb, SPI/QSPI 108 MHz, 1e14 endurance, AEC-Q100
  - [FRAM set to save energy in write-intensive MCU applications](https://newelectronics.co.uk/content/features/fram-set-to-save-energy-in-write-intensive-mcu-applications) — news, 2010. TI embedded FRAM on 130nm adds 2 masks; cell 0.54-0.71 um2; made in-house
  - [Cypress PCN: Fab 25 Austin qualified as alternate wafer fab for 4/16/64Kb F-RAM](https://community.infineon.com/gfawx74859/attachments/gfawx74859/NonVolatileRAM/1143/1/002-18474_00_V.pdf) — company, unknown. F-RAM has history at Austin Fab 25 (now SkyWater); 130nm F-RAM transferred to TI Dallas 300mm
  - [Infineon qualification document (F-RAM die fab: Texas Instruments Dallas DMOS6, 130nm, 300mm)](https://community.infineon.com/gfawx74859/attachments/gfawx74859/NonVolatileRAM/1505/1/INF224203.pdf) — company, unknown. Incumbent F-RAM die is fabbed in the U.S. at TI Dallas DMOS6 (via search snippet; doc attribution between this and the 002-18474 PCN is not certain)
  - [RAMXEED: Research and Development of HZO FeRAM for Higher-Capacity FeRAM](https://www.ramxeed.com/tech-column/hzo-feram-development-for-high-capacity/) — company, unknown. The incumbent FeRAM maker is developing HZO for higher capacity (6.4Gb illustrative on 5mm chip; cites 1e14 HZO capacitor endurance, VLSI 2021) (via search snippet)
  - [RAMXEED: high-reliability FeRAM 125C 10 years](https://www.ramxeed.com/tech-column/high-reliability-feram-125c-10-years/) — company, unknown. PZT FeRAM guarantees 10-yr retention at continuous 125C; 4Mb MB85RS4MTY (via search snippet)
  - [CEA-Leti demonstrates embedded FeRAM platform compatible with 22nm FD-SOI node (IEDM 2024)](https://www.eejournal.com/industry_news/cea-leti-demonstrates-embedded-feram-platform-compatible-with-22nm-fd-soi-node/) — news, 2024-12. HZO FeRAM: 16-kbit arrays at 130nm and an embedded platform at 22nm FD-SOI, so competitors are on the same path (via search snippet)

**Capital tier:** T2 | **Time to first revenue:** 42-72 months: Sandia CRADA/license plus SkyWater HZO module (24 mo), product design and samples (12 mo), first industrial/eval sales ~month 48-54; QML-V adds 1-2 years for the space buyer | **Gross margin estimate:** 50-65% (high-rel ASPs); low volume

**US manufacturability:** SkyWater Bloomington MN (S130; DMEA trusted [UNVERIFIED]) or Fab 25 Austin (historic Cypress alternate fab for small PZT F-RAM); no HZO module at either. Sandia MESA for rad-hard pilot (CRADA/SPP, Ltd access). Note that the incumbent's Excelon die is already made in Dallas TX (TI DMOS6).

**Who is already doing this:** Infineon (PZT F-RAM incl. QML-V rad-hard; Excelon die at TI Dallas DMOS6 300mm/130nm), RAMXEED (ex-Fujitsu; PZT 10-yr at 125C; active HZO R&D aimed at Gb-class FeRAM), TI (embedded FRAM), CEA-Leti (16-kb HZO FeRAM at 130nm; eFeRAM on 22nm FD-SOI, IEDM 2024), FMC (Germany), Sony/Fraunhofer/NaMLab, Sandia (MESA HZO). U.S.-made rad-tolerant alternatives: Everspin toggle MRAM (Chandler AZ) in Frontgrade modules; Honeywell/BAE trusted MRAM/SRAM.

**Wins on which axis, for which buyer:** second/third source in the rad-hard NVM niche, plus density headroom above PZT F-RAM's ~4-16Mb ceiling, in a DMEA-trusted flow. Not 'onshore': the incumbent Excelon die is already U.S.-fabbed (TI Dallas DMOS6), and Everspin toggle MRAM is U.S.-made. — for Space/defense primes (satellite bus controllers, munitions/flight data recorders) and industrial/automotive event-data recorders wanting an onshore second source

**Survives a 2029 glut?:** yes — Mb-class NVM priced on reliability and supply security; unrelated to DDR5 $/GB.

**Fatal-flaw candidate:** HZO still trails PZT on what F-RAM buyers pay for. Research arrays reach ~1e11 cycles and ~10-yr retention at 85C, versus 1e13-1e14 cycles and 10 yr at 125C (RAMXEED) or >100 yr at 85C (Infineon). The 'onshore second source' story is weak because Infineon's F-RAM die is already U.S.-fabbed (TI Dallas DMOS6) and U.S.-made toggle MRAM serves space. RAMXEED and CEA-Leti are pursuing HZO density themselves. The niche is ~hundreds of $M/yr [ESTIMATE] and incumbent-dominated.

*Possible?* yes - 1 Mb HZO arrays exist; Sandia has 200mm FeRAM · *Profitable?* marginal - small, incumbent-dominated niche with a reliability gap to close · *Doable by this founder?* no - T2 chip company with qualification burden

*Business-model lenses:* fabless->foundry; university/lab patent license (Sandia CRADA/license); defense-first

### C-07 — AlScN ferro-diode memory for 500-600C electronics (Penn/AFRL license + STTR) — ☠ KILLED (SCORE<55: Scored 52.0/100 default (rank 33/40), 53.3 moonshot. Weakest: time to revenue 1/5 (42 months (36-48); AF254-D0806 and DV017 are both closed, and STTR money is funding, not revenue (A-04).); tech feasibility 2/5 (Diodes switch at 600C for >60 h (Nature Electronics 2024) and kB crossbars exist only as a preprint (arXiv 2506.05452), but 500C periphery (); founder-fit 2/5 (STTR lets the founder start part-time as CEO/BD with a Penn PI for <$50k, but a device CTO is required and revenue lands past 36 months.). Scorer verdicts — founder: The best-moated device card, but it is an STTR grant program with first sales around 2030: right for a professor's spinout, wrong for a founder who needs revenue in 18 months. | vc: Real physics in a tiny grant-shaped market with no 500C periphery and first sale near month 42: an SBIR mill, not a venture. | veteran: The most interesting physics in my chunk and a genuinely empty niche, but 60 hours at 600C with 1e6 read cycles and no 500C periphery is a DoD research program, not a product; at best a grant-shaped side bet.)

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
  - [Kilobyte-Scale, Selector-Free, Temperature-Hard AlScN Ferroelectric Diode Crossbar Arrays (Pradhan, Moore et al.)](https://arxiv.org/pdf/2506.05452) — preprint, 2025-06. Array-level (kB) AlScN ferro-diode crossbars from the Penn/AFRL group, supporting TRL 4 (title/authors via search snippet only; details not verified)
  - [APS March Meeting 2025: A scalable ferroelectric non-volatile memory operating at high temperature](https://archive.aps.org/smt/2025/mar-t20/12) — conference, 2025-03. 600C operation, 1e6 read cycles, On/Off >1 for >60 h, <15 V (via search snippet)
  - [TechXplore: storage memory device paves way for AI in extreme environments](https://techxplore.com/news/2024-04-storage-memory-device-paves-ai.html) — news, 2024-04. Nature Electronics 7, 348-355 (2024), DOI 10.1038/s41928-024-01148-6 (via search snippet)

**Capital tier:** T1 | **Time to first revenue:** 36-48 months: Penn option + STTR Phase I in the next DoD/NASA cycle (6-12 mo), Phase II arrays + HT packaging (24 mo), then first paid eval-part sales to primes/downhole OEMs; STTR money is funding, not revenue (A-04) | **Gross margin estimate:** 40-60% on early low-volume prototype/eval lots (fab-lot and HT-packaging costs dominate); 55-70% only once qualified parts ship

**US manufacturability:** Prototype at Penn Singh Center (open to industry users per 01_LANDSCAPE 6.1 row 16, $75-250/tool-hr); scale on a U.S. 200mm line with AlN/AlScN sputter (MEMS/RF foundries; which U.S. foundry offers AlScN to outsiders today is [UNVERIFIED]); high-temperature ceramic packaging from U.S. hybrid houses.

**Who is already doing this:** Penn (Jariwala, Olsson) + AFRL (Moore); unknown performer(s) on AF254-D0806 and DPA26BZ04-DV017 (no award found, 2026-11); Univ. of Florida (AlScN ferroelectrics for in-memory compute); SiC high-temperature IC efforts (NASA Glenn JFET ICs) [UNVERIFIED]. No Penn spin-out or license found (2 searches, 2026-11).

**Wins on which axis, for which buyer:** operating temperature / survival in extreme environments (no incumbent RAM or flash works at 500C+) — for AFRL and hypersonic/engine programs; aero-engine OEMs (health monitoring); downhole tool makers (oilfield services, geothermal); planetary-probe teams

**Survives a 2029 glut?:** yes — Completely decoupled from commodity memory pricing.

**Fatal-flaw candidate:** A tiny, grant-shaped market that can easily turn into an SBIR mill (the mission bars grant farming). It needs a 500C periphery that barely exists commercially (SiC CMOS/JFET ICs are lab or program-only) and drive voltages of ~10-15 V at temperature. Penn's licensing status is unknown, and AFRL has already solicited a manufacturing scale-up performer (AF254-D0806) who may own the commercial seat. Revenue comes after the 18-month target and close to the 36-month ceiling.

*Possible?* yes - devices work at 600C; arrays early · *Profitable?* marginal - high ASP but very low volume; depends on DoD program pull · *Doable by this founder?* marginal - best founder-entry among device cards via STTR, but not an 18-month revenue path

*Business-model lenses:* university/lab patent license; defense-first; fabless->foundry

### C-08 — Ferroelectric 'Optane-slot' persistent memory (NVDRAM-class HZO 1T1C NVDIMM/CXL) — ☠ KILLED (R3-FAB/T4: A 32Gb-class HZO 1T1C NVDRAM die needs a DRAM-class capacitor process. In the U.S. only Micron has one, and it is captive (01_LANDSCAPE 6.1). The card itself sets T4 and 'never for a startup'. The one company that built the die (Micron, IEDM 2023) never made it a product, and Optane's ~$576M 2020 loss plus $559M impairment show the persistent tier fails on cost absorption. The remaining startup-scale angles are covered by C-09 (FMC DRAM+ design-in) and C-51 (persistent CXL log card).)

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

### C-09 — U.S. design-in and module partner for FMC DRAM+ (HfO2 non-volatile DRAM) — ☠ KILLED (FACT-COLLAPSE: The card sells a channel seat for a product that does not exist, and the seat is already filled. As of 2026 FMC has no chips on the market (heise 2026). It has not disclosed full chip specs, a process or a mass-production timeline, and it is still bidding for the ex-Intel Magdeburg site (cnyes, via snippet). Neumonda already 'helps design, test and market' DRAM+ (Embedded Computing, via snippet). FMC's model since 2017 has been licensing to DRAM makers and foundries, whose parts move through established distribution, so no evidence shows FMC wants a one-person U.S. module partner. Revenue is 30-54+ months away and entirely in FMC's hands, past the 36-month ceiling. The HfO2 1T1C mechanism is real (Micron 32Gb NVDRAM, IEDM 2023), so this is not an R1 kill.)

*Sub-branch:* Ferroelectric (HfO2 FeCAP DRAM, channel/module) · *Materials sense:* c-capital

**What it is:** Become FMC's U.S. application channel: eval boards, reference designs and small-volume non-volatile memory modules (U.S.-assembled at an East Coast EMS) around FMC's DRAM+ (ferroelectric HfO2 replacing the DRAM capacitor). Customers would be U.S. industrial PLC, medical-device and automotive data-logging OEMs.

**Why it could work:** FMC raised EUR100M (Nov 2025) with two DRAM-maker partners and an Asian logic foundry and wants global presence. U.S. OEMs value instant-on NV working memory that removes supercaps and batteries. A small partner can earn design-in services plus module margin, with capital limited to boards and inventory.

**Evidence:** TRL 4 · Rule 1: SUPPORTED
  - [FMC raises EUR100M to set new standards for memory chips](https://www.hpcwire.com/off-the-wire/fmc-raises-e100m-to-set-new-standards-for-memory-chips/) — company, 2025-11. EUR100M (EUR77M equity + EUR23M public) for DRAM+ and 3D CACHE+; works with two DRAM makers and an Asian logic foundry
  - [FMC + Neumonda DRAM+ (TrendForce)](https://www.trendforce.com/news/?p=37749) — news, 2025-04. DRAM+ replaces DRAM capacitor with ferroelectric HfO2 (non-volatile), Gb-class target; Neumonda provides test platforms
  - [Memory chip company FMC keeps working on semiconductor plant near Magdeburg](https://heise.de/-11151026) — news, 2026. FMC has no ferroelectric memory chips on the market yet; pursuing a fab near Magdeburg
  - [FMC and Neumonda Team Up to Bring DRAM Manufacturing Back to Germany](https://embeddedcomputing.com/technology/storage/fmc-and-neumonda-team-up-to-bring-dram-manufacturing-back-to-germany) — news, 2025. Neumonda helps design, test and market FMC's non-volatile DRAM+ and provides its test platforms (via search snippet)
  - [FMC among bidders for former Intel Magdeburg site (Chinese-language report)](https://hao.cnyes.com/post/259683) — news, 2026. FMC is one of several bidders for the ex-Intel Magdeburg site, decision expected late summer 2026; FMC has not publicly disclosed full chip specifications, manufacturing process or mass-production timeline (via search snippet)

**Capital tier:** T1 | **Time to first revenue:** >54 months; no DRAM+ sample date, spec or process public as of 2026-11; gated entirely by FMC and its DRAM-maker partners | **Gross margin estimate:** 25-35% (modules + services)

**US manufacturability:** U.S.-assembled only (dies from FMC's Asian DRAM partner) => 'U.S.-assembled', not U.S.-made (A-09)

**Who is already doing this:** FMC (Dresden) with two unnamed DRAM-maker partners; Neumonda (Munich) already designs, tests and markets DRAM+; Arrow/Avnet-class distributors would carry any shipping part

**Wins on which axis, for which buyer:** non-volatility at DRAM-like speed (instant-on, no backup power) — for industrial automation (PLC/CNC), medical devices, automotive event recorders

**Survives a 2029 glut?:** partially — The NV premium persists, but DRAM+ priced against DRAM gets squeezed by a 60% DDR5 drop.

**Fatal-flaw candidate:** No product (no chips, specs, process or timeline as of 2026), and the go-to-market partner role is already held by Neumonda. FMC licenses to DRAM makers, who sell through established distribution. A one-person channel partner has neither a product nor a seat.

*Possible?* no inside the window - there is no product to channel · *Profitable?* marginal - thin channel margins · *Doable by this founder?* no

*Business-model lenses:* module/appliance; distribution/brokerage

### C-10 — FeFET embedded NVM licensing on GlobalFoundries 22FDX for U.S. MCU/edge SoCs — ☠ KILLED (FACT-COLLAPSE: There is no intermediary seat to fill. FMC's stated model is to license FeFET directly to foundries and IDMs ('Arm of memories', eeNews 2017), and a foundry delivers eNVM to SoC designers through its own PDK and IP catalog. On GF's FDX platform the qualified eNVM today is eMRAM (AutoPro150, run in Dresden; 01_LANDSCAPE 6.1 row 8), while HfO2 FE memory on 22FDX is still 'upcoming' in Fraunhofer's 2026 FAMES release. The card itself records 0% margin for us, 60+ months and 'no value add', and the product is NVM, not RAM. GF Malta runs 12/14nm FinFET, not 22FDX, so even the U.S. angle is absent.)

*Sub-branch:* Ferroelectric (FeFET eNVM) · *Materials sense:* mixed:a+b

**What it is:** Act as licensing/design-services intermediary for HfO2 FeFET embedded NVM (FMC technology) on GlobalFoundries 22FDX, selling it to U.S. MCU and edge-AI SoC makers as an eFlash replacement needing only 1-3 extra masks.

**Why it could work:** FeFET puts the ferroelectric in the HKMG gate stack (sub-5nm films, low write energy), and FMC/GF integrated it on 28nm HKMG years ago. Embedded NVM below 28nm is scarce.

**Evidence:** TRL 5 · Rule 1: SUPPORTED
  - [Ferroelectric memory startup aims at GloFo's 22FDX](https://www.eenewseurope.com/en/ferroelectric-memory-startup-aims-at-glofos-22fdx/) — news, 2016. FMC FeFET integrated on GF 28nm HKMG; licensing model
  - [Ferroelectric memory startup aims to be the Arm of memories](https://www.eenewseurope.com/en/ferroelectric-memory-startup-aims-to-be-the-arm-of-memories/) — news, 2017. FMC plans licensing to foundries/IDMs plus validation/qualification services
  - [CEA-Leti and Fraunhofer IPMS validate wafer exchange for FE memory materials (FAMES)](https://www.ipms.fraunhofer.de/en/press-media/press/2026/FAMES-wafer-exchange.html) — industry, 2026. HfO2 FE stacks to be evaluated embedded in upcoming GF 22nm FDX memory -- not yet qualified

**Capital tier:** T3 | **Time to first revenue:** 60+ months; 22FDX FE memory is still 'upcoming' per FAMES 2026 | **Gross margin estimate:** n/a for us (FMC/GF capture it)

**US manufacturability:** None: 22FDX runs only at GF Dresden; GF Malta NY is 12/14nm FinFET and RF-SOI (01_LANDSCAPE 6.1 row 8)

**Who is already doing this:** FMC (licensor), GlobalFoundries Dresden (foundry IP channel), Fraunhofer IPMS and CEA-Leti (FAMES pilot line); GF already sells qualified eMRAM (AutoPro150) on FDX

**Wins on which axis, for which buyer:** embedded NVM write energy and scalability vs eFlash (NVM, not RAM) — for MCU/edge SoC designers on 22FDX

**Survives a 2029 glut?:** yes — eNVM is unrelated to DDR5 pricing, which is also why it isn't a 'RAM' answer.

**Fatal-flaw candidate:** We would own nothing: FMC and GF own the IP and the line. It is NVM not RAM, and it is not yet qualified.

*Possible?* yes for FMC/GF; no for an intermediary · *Profitable?* no - not for an intermediary · *Doable by this founder?* no

*Business-model lenses:* IP licensing (as intermediary - no value add); fabless->foundry

### C-11 — SunRise-style 3D NOR 'quasi-volatile' memory as a DRAM substitute — ☠ KILLED (R3-FAB/T4: The minimum viable path is a licensee building thin-film 3D NOR in a NAND-class fab, which the card itself rates T4. No volume 3D NAND fab runs in the U.S. (01_LANDSCAPE 6). R1 fails as well. After ~10 years and ~$75M+ there is no public array silicon or peer-reviewed DRAM-substitute data, and my search found no 2026 product or funding news. SunRise's newest grant (Aug 2025) covers thin-film ferroelectric transistor strings, and an Apr-2025 report says it is moving to 3D ferroelectric RAM for AI (via snippet), so even the 'quasi-volatile NOR as DRAM substitute' premise looks abandoned.)

*Sub-branch:* 3D DRAM alternatives (3D NOR charge-trap) · *Materials sense:* b-process

**What it is:** Thin-film 3D NOR charge-trap arrays with minutes-to-days retention, proposed by SunRise Memory (Eli Harari, San Jose) as a cheaper-than-DRAM tier refreshed rarely. A licensee would build it on NAND-class tooling.

**Why it could work:** If 3D NOR offered DRAM-like latency at NAND-like cost per bit, it would sit under DRAM for AI/KV-cache capacity. SunRise has kept patenting into 2024-2026.

**Evidence:** TRL 2 · Rule 1: UNSUPPORTED
  - [SanDisk founder has his next memory chip startup](https://www.eenewseurope.com/en/sandisk-founder-has-his-next-memory-chip-startup) — news, 2018. SunRise Memory (Eli Harari) 3D NOR positioned as DRAM-alternative tier
  - [SunRise Memory profile](https://www.cbinsights.com/company/sunrise-memory) — industry, unknown. Founded 2016, San Jose; Seagate investor; no product news found 2025-26
  - [US12052867B2 3D NOR memory array with very fine pitch](https://patents.google.com/patent/US12052867) — patent, 2024. SunRise still patenting; no silicon density data public
  - [Patents by Inventor Eli Harari (page 3)](https://patents.justia.com/inventor/eli-harari?page=3) — patent, 2025-08. SunRise/Harari 3D NOR string patents; most recent grant (Aug 2025) covers a 3D memory string array of thin-film ferroelectric transistors; a separate Apr-2025 report (URL not identified) said SunRise is developing 3D ferroelectric RAM for AI; no 2026 product/funding news found (via search snippet)

**Capital tier:** T4 | **Time to first revenue:** unknown; no public silicon after ~8 years | **Gross margin estimate:** n/a

**US manufacturability:** Would need a NAND-class fab (none in U.S. [UNVERIFIED])

**Who is already doing this:** SunRise Memory (no public silicon; reportedly moving to 3D ferroelectric RAM, Apr 2025, via snippet); Macronix (3D NOR flash, not quasi-volatile)

**Wins on which axis, for which buyer:** $/GB below DRAM with refresh-tolerant retention (claimed) — for (claimed) AI/datacenter memory tier

**Survives a 2029 glut?:** no — A sub-DRAM tier is squeezed from both sides when DRAM and NAND both fall.

**Fatal-flaw candidate:** No public silicon or peer-reviewed array data found for the DRAM-substitute claim. Patents do not show it works at scale, so it is UNSUPPORTED under rule 1.

*Possible?* marginal - unproven publicly · *Profitable?* no · *Doable by this founder?* no

*Business-model lenses:* IP licensing (as licensee)

### C-12 — Battery-free NV-cache / NVSRAM-replacement modules from off-the-shelf F-RAM — ☠ KILLED (RED-TEAM: DD3 (Drop-in Non-Volatile Continuity Modules) was KILLED by the four-persona red team: After the red team, the revised BASE loses $29.8k over 36 months (Phase 4: +$79.1k). It breaks even only in m19, never pays the founder, and needs about $49k of peak cash (cash low -$9.2k), above the $40k deployable. The main cause is the market: once i-series controls (which take a $20 CF card) and the unfound DMSMS contracts are removed, addressable demand is about 2,591 cards/yr (~$0.62M/yr), and a 36-month cumula See 05_REDTEAM.md (DD3) and 04_DEEPDIVES/nv-continuity-modules.md §14.)

*Sub-branch:* Ferroelectric (PZT F-RAM, module) · *Materials sense:* c-capital

**What it is:** Design and sell battery-free, controller-validated PCMCIA SRAM cards (256KB-2MB) and DIP NVSRAM drop-ins built on shipping parallel F-RAM (Infineon FM18W08/FM28V-class, RAMXEED MB85R8M2T 8Mbit), assembled at an East Coast EMS. Sold to industrial MRO for legacy Fanuc/Mitsubishi CNC, PLCs and data loggers whose battery-backed SRAM cards and Dallas DS12xx modules are failing or unobtainable.

**Why it could work:** Shipping F-RAM offers 1e14 writes, zero write delay and >100-year retention, with no battery to fail, maintain or ship as hazmat. Legacy machines with battery-backed SRAM cards need maintenance-free replacements [ESTIMATE of demand]. Capital is just PCB design, contract EMS assembly and inventory. Key negative finding: F-RAM at ~$1-4/Mbit [ESTIMATE] is ~$8,000-30,000/GB, ~300-1,000x DDR5, so F-RAM cannot take DRAM sockets during the shortage, only battery-backed-SRAM sockets.

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [Infineon EXCELON F-RAM family](https://infineon.com/cms/en/product/memories/f-ram-ferroelectric-ram/excelon-f-ram) — company, unknown. Shipping F-RAM 1-16 Mb, SPI/QSPI 108 MHz, 1e14 endurance, AEC-Q100
  - [Infineon 5962R1821601VXC rad-hard 2Mb serial F-RAM (QML-V)](https://infineon.com/cms/en/product/memories/radiation-hardened-high-reliability-memories/space-memories/5962r1821601vxc) — company, 2022-04. Incumbent PZT F-RAM: TID >150 krad(Si), SEL immune, 1e13 cycles, >100-yr retention at 85C
  - [FRAM set to save energy in write-intensive MCU applications](https://newelectronics.co.uk/content/features/fram-set-to-save-energy-in-write-intensive-mcu-applications) — news, 2010. TI embedded FRAM on 130nm adds 2 masks; cell 0.54-0.71 um2; made in-house
  - [Dallas DS1230Y DS1235YW NVRAM FRAM Replacement Adapter](https://www.pcbway.com/project/shareproject/Dallas_DS1230Y_DS1235YW_NVRAM_FRAM_Replacement_Adapter_79f70ace.html) — other, unknown. Open-source adapter puts a Ramtron/Cypress FM18W08 F-RAM in place of DS1230Y/DS1235YW battery-backed NVSRAM; sealed lithium cells fail after ~10-15 years (via search snippet)
  - [Fanuc SRAM PCMCIA Cards](https://memex.ca/?p=596) — company, unknown. Memex sells Fanuc-compatible PCMCIA SRAM cards with rechargeable lithium battery (not battery-free); most capacities listed unavailable; 'We DO NOT have PCMCIA cards - they are hard to get' (via search snippet; WebFetch failed: host not allowed)
  - [The optimal solution to eliminate batteries for SRAM in industrial machinery](https://www.radiolocman.com/news/new.html?di=514081) — news, unknown. Fujitsu (now RAMXEED) MB85R8M2T 8Mbit parallel FRAM marketed to replace SRAM and remove the backup battery in control units and robots (via search snippet)

**Capital tier:** T0 | **Time to first revenue:** 6-12 months (first module SKUs sold online and to MRO buyers) | **Gross margin estimate:** 40-55%

**US manufacturability:** U.S. EMS assembly of packaged F-RAM bought through authorized distribution; Infineon F-RAM is partly U.S.-fabbed historically (TI Dallas 130nm; Cypress qualified Fab 25 Austin for Kb parts, per A1) [REPORTED]; RAMXEED parts are Japanese

**Who is already doing this:** Open-source DS1230-to-FM18W08 adapters (PCBWay/OSH Park, free); Memex and other Fanuc-card resellers (rechargeable-battery SRAM cards, mostly out of stock); Infineon (parallel F-RAM, nvSRAM chips); RAMXEED (MB85R8M2T pitched to remove SRAM batteries); Everspin (parallel MRAM drop-ins); ADI/Maxim legacy DS12xx NVSRAM [UNVERIFIED status]

**Wins on which axis, for which buyer:** non-volatility without batteries; lifecycle (maintenance-free) — for industrial MRO for legacy CNC/PLC with battery-backed SRAM; data-logger and metering OEMs

**Survives a 2029 glut?:** yes — Sold against batteries and NVSRAM, not DDR5.

**Fatal-flaw candidate:** Tiny, fragmented MRO market. Each controller family (Fanuc 0i/16i/18i, Mitsubishi, Okuma) needs card-attribute and timing validation, and free open-source adapters already serve the DIP NVSRAM niche. It does not do 'RAM's job' at scale; at best it is a profitable side product line with revenue in the low $100ks/yr [ESTIMATE].

*Possible?* yes - parts ship today · *Profitable?* marginal - a niche product line (low-$100ks/yr ceiling [ESTIMATE]), not a venture-scale business · *Doable by this founder?* yes

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
  - [Ferroelectric Test Systems (KIT INT)](https://www.int.kit.edu/2746.php) — other, unknown. University lab owns aixACCT and Radiant RT66B testers covering hysteresis, remanent hysteresis, retention, fatigue, imprint, leakage and PUND (via search snippet)
  - [Radiant PE loop tracer (shared equipment listing)](https://www.istem.gov.in/equipment-info/61705/Radient-PE-loop-tracer) — government, unknown. Radiant ferroelectric P-E loop testers are common shared-facility instruments; no Radiant contract-testing service found in search (via search snippet)

**Capital tier:** T1 | **Time to first revenue:** 12-24 months: hire a full-time reliability engineer, lease/finance used Radiant/aixACCT tester + probe station + parametric analyzer; first projects can be run asset-light on university shared tools ($75-250/tool-hr) before owning gear | **Gross margin estimate:** 30-45% (labor-heavy services at low utilization)

**US manufacturability:** Lab only (no fab); located near NY CREATES Albany (300mm HfO2 memory JDA with Fraunhofer IPMS) or Penn (Philadelphia)

**Who is already doing this:** Neumonda and Fraunhofer IPMS (Germany); aixACCT (Germany) and Radiant Technologies (Albuquerque NM) sell testers, with no contract service found; university shared facilities that own those testers; NY CREATES (member characterization); Sandia (CRADA, slow); EAG/Eurofins (materials analysis, not device reliability) [no U.S. commercial specialist found: STILL-UNVERIFIED]

**Wins on which axis, for which buyer:** time-to-reliability-data and independence (enabling service, not a RAM axis) — for device startups, SBIR/STTR performers, defense primes evaluating new NVM, VCs doing tech diligence

**Survives a 2029 glut?:** partially — Startup funding shrinks in a memory glut, but defense and university demand continues.

**Fatal-flaw candidate:** Small, lumpy demand. Customers with money (Samsung, Micron, Infineon, Intel) test in-house, and universities own Radiant/aixACCT testers for the basic measurements. That leaves maybe 10-30 U.S. startups, SBIR performers and primes buying wafer-level statistics and qualification. Device-physicist labor is the bottleneck, and the founder is not one.

*Possible?* yes · *Profitable?* marginal - services margin, small market · *Doable by this founder?* marginal - only with a full-time reliability-engineer cofounder

*Business-model lenses:* services; defense-first; data product (test database)

### C-14 — MemTech Atlas: emerging-memory device-parameter and $/GB cost-model data product — ☠ KILLED (NOT-A-VENTURE: Without the UI, this is a research-content subscription: curated public literature plus an analyst's cost model. The mission allows that only as a bridge revenue line, and the card's own fatal_flaw admits it. Its claimed axis (cheaper, more transparent technology intelligence) also loses at both ends. The device-parameter layer already exists for free in Stanford Memory Trends (RRAM/PCM/CBRAM/STT-MRAM tables from IEDM/VLSI/ISSCC since 2001, 2024 release) and UCSD's NVMDB (340 papers). The authoritative teardown data belongs to TechInsights and Yole. With a few hundred potential buyer seats [ESTIMATE], keep this engagement's device_params and cost model as a funnel or bridge asset, not the venture.)

*Sub-branch:* Cross-cutting (oxide/ferroelectric/3D DRAM data product) · *Materials sense:* none

**What it is:** A subscription web app that curates published device parameters (cell area, retention, endurance, layers, mask adders, demonstrated vs simulated) for IGZO/IWO, HZO, FeFET, AlScN, MRAM, ReRAM and 3D DRAM. It pairs them with an open, auditable $/GB cost model and a 'claims vs silicon' tracker, sold to memory investors, corporate strategy teams, defense program offices and procurement.

**Why it could work:** It plays to the founder's software skill. This branch's research shows the data is scattered across press releases, IEDM/VLSI papers and paywalled TechInsights/Yole reports. Claims diverge sharply (NEO: 450 s simulated vs >1 s measured), and simple per-area analyses go viral (Kurnal Insights, Sep 2026). A transparent, cheaper tool for non-Yole budgets gives recurring revenue at ~80%+ margin.

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [DRAM value-per-area chart (Kurnal Insights)](https://www.kitguru.net/channel/generaltech/joao-silva/new-dram-value%E2%80%91per%E2%80%91area-chart-draws-attention-amid-rising-memory-prices/) — news, 2026-09. 1b DRAM bit density ~0.436 Gb/mm2 (baseline for density comparison)
  - [NEO adds IGZO to 3D DRAM designs](https://www.eenewseurope.com/en/neo-semiconductor-adds-igzo-to-3d-dram-designs/) — news, 2025-05. 1T1C and 3T0C IGZO variants: TCAD-simulated 10 ns and >450 s retention, not silicon; modified 3D NAND process
  - [NEO Semiconductor demonstrates 3D X-DRAM proof-of-concept](https://www.storagenewsletter.com/2026/05/13/neo-semiconductor-demonstrates-3d-x-dram-proof-of-concept-secures-strategic-investment-to-advance-ai-memory/) — company, 2026-04. Company-reported PoC: retention >1 s at 85C, endurance >1e14, <10 ns; test chips by NYCU, fabbed at TSRI Taiwan; next: arrays, multi-layer
  - [Capacitor-less IGZO-based DRAM cell with excellent retention, endurance and gate length scaling (IEDM 2021)](https://techxplore.com/news/2021-12-capacitor-less-igzo-based-dram-cell-excellent.html) — conference, 2021-12. Fully 300mm BEOL-compatible 2T0C: >1e3 s retention, >1e11 endurance, Lg 14nm with >100 s; PBTI lifetime ~1 yr vs 5-yr target
  - [Stanford Memory Trends](https://nano.stanford.edu/downloads/stanford-memory-trends) — dataset, 2024. Free downloadable tables of RRAM, PCM, CBRAM and STT-MRAM device parameters covering most IEDM, VLSI and ISSCC works from 2001; latest listed release 2024 (via search snippet; WebFetch failed: host not allowed)
  - [NVMDB: a database of non-volatile memory technology papers (TR2015)](https://cseweb.ucsd.edu/~swanson/papers/TR2015-NVMDB.pdf) — dataset, 2015. NVMDB covers 340 NVM technology papers from ISSCC, VLSI and IEDM, 2000-2014; available at nvmdb.ucsd.edu (via search snippet)

**Capital tier:** T0 | **Time to first revenue:** 6-9 months (MVP from this engagement's device_params + cost model; first annual subscriptions) | **Gross margin estimate:** 60-75% (curation needs device-physics analyst labor)

**US manufacturability:** Software; no fab

**Who is already doing this:** Free: Stanford Memory Trends (Wong group, 2001-2024 IEDM/VLSI/ISSCC tables), UCSD NVMDB; paid: TechInsights, Yole/System Plus, Objective Analysis, Coughlin Associates; free commentary: Kurnal Insights

**Wins on which axis, for which buyer:** none against free academic databases on cost, none against TechInsights on authority; only a $/GB cost-model view (content) — for memory-focused VCs/CVCs, DoD/DOE program managers, SBIR applicants, OEM component strategists

**Survives a 2029 glut?:** partially — Technology diligence continues in a glut, but customer budgets shrink.

**Fatal-flaw candidate:** Small TAM, and incumbents with teardown access (TechInsights) own the authoritative data. It risks becoming content or consulting, which the mission treats as a bridge only.

*Possible?* yes · *Profitable?* no as a venture; small bridge/funnel revenue only · *Doable by this founder?* yes

*Business-model lenses:* SaaS; data product

### C-15 — Onshore In-Ga-Zn oxide sputter-target and ALD-precursor supply for IGZO-channel DRAM — ☠ KILLED (R4-NO-WINNING-AXIS: The card's only axis is supply security, and an unqualified U.S. startup improves it for none of the named buyers. Target incumbents are already non-Chinese: Materion holds IGZO-target patents via its ex-Heraeus unit (US9051646, snippet), and Japanese makers lead display IGZO. Research-grade IGZO targets already sell from the U.S. (American Elements, snippet), and the real chokepoint, primary gallium and indium refining, sits upstream of any target or precursor maker. Demand is soft too. Samsung's IGZO channel is only 'reported' (TrendForce 2026-04), and an Oct-2026 report says there is no fixed mass-production timetable. Micron, the only U.S. DRAM maker, is reported to be skipping 4F2 (snippets), so there is no onshore volume customer. Vertical-channel and stacked 3D IGZO also need conformal ALD, which makes 'DRAM-grade sputter targets' largely the wrong product [ESTIMATE: device-physics judgment].)

*Sub-branch:* Oxide-semiconductor DRAM (materials supply chain) · *Materials sense:* a-material

**What it is:** Supply DRAM-grade IGZO/ITO/IWO sputter targets and indium/gallium/zinc ALD precursors to DRAM makers moving to oxide channels: Samsung 10a 4F2 VCT with a reportedly IGZO channel targeted for 2028, Kioxia OCTRAM, imec and IMECAS 3D 2T0C. U.S. research lines (Purdue ALD In2O3 on 200mm, NY CREATES) would be early customers, positioned as a non-Chinese indium chain.

**Why it could work:** If oxide channels enter mainstream DRAM, every such wafer needs oxide-semiconductor deposition, and the materials play wins whichever cell architecture wins. Micron's U.S. fabs (Boise, Manassas, NY) and CHIPS-funded supply-chain localization favor onshore materials.

**Evidence:** TRL 6 · Rule 1: SUPPORTED
  - [Samsung reportedly produces 10a DRAM working die using 4F2 and VCT, targets 2028](https://www.trendforce.com/news/2026/04/24/news-samsung-reportedly-produces-sub-10nm-10a-dram-working-die-using-4f-square-and-vct-targets-2028-production/) — news, 2026-04. Samsung 4F2 VCT working die Mar 2026; channel reportedly shifted to IGZO; mass production transfer 2028
  - [Kioxia develops OCTRAM (with Nanya), IEDM 2024](https://www.businesswire.com/news/home/20241209099702/en/Kioxia-Develops-OCTRAM-Oxide-Semiconductor-Channel-Transistor-DRAM-Technology) — company, 2024-12. 4F2 DRAM: vertical InGaZnO transistor on high-aspect-ratio capacitor; Ion >15 uA/cell, Ioff <1 aA/cell
  - [Kioxia core technology for high-density low-power 3D DRAM (IEDM 2025)](https://www.kioxia.com/en-jp/about/news/2025/20251212-1.html) — company, 2025-12. 8-layer horizontally stacked InGaZnO transistors (SiN replaced by IGZO); Ion >30 uA, Ioff <1 aA
  - [Purdue: 3D chip platform, three layers of ALD indium-oxide transistors on 200mm](https://engineering.purdue.edu/ECE/News/2026/purdue-researchers-build-3d-chip-platform-for-faster-more-efficient-ai-computing) — industry, 2026-09. >100,000 oxide devices on 52 dies of a 200mm wafer incl. ferroelectric FETs; BEOL-compatible; U.S. university IP
  - [US9051646 Sputtering target with mixture of In, Ga, Zn oxides (Materion Advanced Materials Germany, ex-Heraeus)](https://patents.google.com/patent/US9051646) — patent, unknown. Materion Advanced Materials Germany GmbH (formerly Heraeus) is assignee of an IGZO sputtering-target patent: Materion is an IGZO-target incumbent (via search snippet; current product line not confirmed)
  - [Indium Gallium Zinc Oxide (IGZO) Sputtering Target](https://americanelements.com/indium-gallium-zinc-oxide-igzo-sputtering-target) — company, unknown. U.S.-based catalog supplier sells IGZO sputtering targets (2N, research grade) (via search snippet)
  - [Changxin Memory plans to launch its first 4F2 server DDR5 memory](https://finance.technews.tw/2026/10/14/changxin-memory-plans-to-launch-its-first-4f%c2%b2-server-ddr5-memory/) — news, 2026-10-14. Oct-2026 Taiwanese report: Samsung showed a 16Gb 4F2 VCT design at ISSCC 2026; despite the earlier 2028 10a target, later reports indicate no fixed mass-production timetable; CXMT targets a 4F2 server DDR5 RDIMM by end-2026 (via search snippet; attribution between this page and uanalyze.com.tw not confirmed)
  - [Samsung, SK hynix, Micron, CXMT 4F2 DRAM technology](https://www.sammyfans.com/2026/10/22/samsung-sk-hynix-micron-cxmt-4f2-dram-technology/amp/) — blog, 2026-10-22. Micron reportedly will skip the 4F2 layout; SK hynix plans 4F2/VCT at 10b rather than 10a (via search snippet; weak source)

**Capital tier:** T2 | **Time to first revenue:** 24-48 months (research-line sales first; fab qualification 2-3 years) | **Gross margin estimate:** 35-50% (specialty materials)

**US manufacturability:** Specialty-chemical/target plant on the East Coast; incumbents include Japanese target makers and U.S. firms such as Materion and Indium Corporation (current oxide-target/precursor product lines UNVERIFIED)

**Who is already doing this:** IGZO targets: Materion (ex-Heraeus, IGZO target patents), JX Advanced Metals, Mitsui Kinzoku, Tosoh [last three UNVERIFIED], American Elements (U.S. research grade); In/Ga/Zn ALD precursors: Merck/EMD Electronics, Entegris, Air Liquide, Adeka, SK Trichem, DNF [UNVERIFIED]

**Wins on which axis, for which buyer:** supply security of a critical material for next-generation DRAM — for Samsung / Kioxia-Nanya (Korea, Japan, Taiwan) if oxide channels reach volume; U.S. research lines buy grams

**Survives a 2029 glut?:** partially — Volumes track DRAM capex (down in a glut) but follow the technology transition, not DDR5 price.

**Fatal-flaw candidate:** DRAM makers qualify materials over 2-3 years with incumbent Japanese/Korean suppliers, and a startup without chemistry pedigree won't get qualified. Samsung's IGZO choice is only 'reported' and could revert to silicon.

*Possible?* yes · *Profitable?* marginal - real market if IGZO channels win, but incumbents are strong · *Doable by this founder?* no

*Business-model lenses:* materials supplier; defense/supply-security (CHIPS supply-chain programs)

### C-16 — Supercap-Killer PLP Kit (MRAM write-cache reference design) — ☠ KILLED (RED-TEAM: DD3 (Drop-in Non-Volatile Continuity Modules) was KILLED by the four-persona red team: After the red team, the revised BASE loses $29.8k over 36 months (Phase 4: +$79.1k). It breaks even only in m19, never pays the founder, and needs about $49k of peak cash (cash low -$9.2k), above the $40k deployable. The main cause is the market: once i-series controls (which take a $20 CF card) and the unfound DMSMS contracts are removed, addressable demand is about 2,591 cards/yr (~$0.62M/yr), and a 36-month cumula See 05_REDTEAM.md (DD3) and 04_DEEPDIVES/nv-continuity-modules.md §14.)

*Sub-branch:* STT-MRAM design-in: power-loss-protection write cache · *Materials sense:* mixed:a+c

**What it is:** A licensed reference design (schematic/layout, FPGA or RISC-V controller RTL, Linux/Zephyr journaling driver, validation suite) that replaces the DRAM + supercapacitor power-loss-protection block in SSD, computational-storage, RAID/HBA and industrial data-logger boards with Everspin PERSYST 1Gb ST-DDR4 or 64-256Mb xSPI STT-MRAM. Parts come from Everspin (GF 28nm CMOS + Chandler AZ MTJ BEOL; Microchip Gresham OR line from 2H-2027); revenue is design-package fee + per-unit royalty + design-in services.

**Why it could work:** Replace 'IBM moved its 5th-gen FlashCore Module to Everspin MRAM instead of capacitors (Oct-2026)' with 'IBM has used Everspin MRAM as the FCM write cache/journal for several generations (FCM3 up to 128 MB Toggle; FCM4 1Gb PERSYST, 2024; FCM5 MRAM-instead-of-capacitors, reported 2026-10)'. Replace '~30x $/bit penalty (~$100/Gb street vs ~$3/Gb DRAM)' with '~51x the 4Q26 DDR5 contract ($821 vs $15.99/GB) and ~128x the $6.40 glut price'.

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [IBM using Everspin MRAM in 5th-gen FlashCore Modules](https://www.blocksandfiles.com/flash/2026/10/05/ibm-using-everspin-mram-in-5th-gen-flashcore-modules/5300966) — news, 2026-10. IBM FCM5 (QLC SSD) uses a few hundred MB of Everspin MRAM as write cache/journal instead of supercapacitors for power-loss protection; production product (via search snippet)
  - [Next-Generation IBM FlashCore Modules Feature Everspin's PERSYST 1Gb STT-MRAM](https://businesswire.com/news/home/20240430370312/en/Next-Generation-IBM-FlashCore-Modules-Feature-Everspins-PERSYST-1-Gigabit-STT-MRAM-Enhancing-Reliability) — company, 2024-04. IBM FCM4 design-in of EMD4E001G 1Gb STT-MRAM (via search snippet)
  - [IBM and Everspin announce 19TB NVMe SSD with MRAM write cache](https://www.anandtech.com/show/13174) — news, 2018-08. IBM chose MRAM over DRAM+supercaps because supercaps/batteries last only a few years (via search snippet)
  - [Phison brings Everspin 1Gb STT-MRAM to next-gen SSD controllers](https://www.3dtested.com/news/phison-ssd-controller-everspin-mram,40022.html) — news, 2018. SSD controller support for MRAM-based PLP without supercaps (via search snippet)
  - [Everspin 8-K: Foundry Services Agreement with Microchip](https://www.sec.gov/Archives/edgar/data/1438423/000162828026024696/mram-20260408xexx991.htm) — company, 2026-04. 10-yr deal: Microchip Fab 4 (Gresham OR) 8-inch MRAM/TMR/STT wafers, ramp to max 1,300 wafers/qtr, first products 2H-2027; Microchip barred from making TMR devices for Everspin competitors (via search snippet)
  - [EMD4E001G16G2-150CAS2R listing](https://www.lcsc.com/product-image/C20342497.html) — industry, 2026. 1Gb STT-MRAM reference price $102.60 @500 (~$821/GB) (via search snippet)
  - [Sage Microelectronics and Everspin partner to bring STT-MRAM to next-generation enterprise SSD devices](https://dev007.embeddedcomputing.com/technology/storage/sage-microelectronics-and-everspin-partner-to-bring-spin-transfer-torque-mram-to-next-generation-enterprise-ssd-devices) — news, 2019. A second SSD-controller vendor (Sage) paired its controller ASIC with Everspin 1Gb STT-MRAM, in addition to Phison (via search snippet)
  - [Teledyne HiRel Semiconductors and Everspin Technologies Partner to Accelerate MRAM Adoption in Aerospace and Defense Applications](https://www.teledyne-ade.com/en-us/news/Pages/Teledyne-HiRel-Semiconductors-and-Everspin-Technologies-Partner-to-Accelerate-MRAM-Adoption-in-Aerospace-and-Defense-Applic.aspx) — company, 2026-09-02. Teledyne HiRel (Milpitas CA) will sell Everspin PERSYST 256/128/64Mb STT-MRAM to mil/aero and satellite customers with screening flows, qualification documentation, procurement support and obsolescence management; availability expected 4Q-2026 (via search snippet)

**Capital tier:** T1 | **Time to first revenue:** 18-24 months to the first paid design-in (services) after a 6-9-month reference-board build; royalties 30-42 months, only if an OEM ships | **Gross margin estimate:** 35-45% for years 1-3 (services-dominated); 60%+ only if royalties materialize after year 3

**US manufacturability:** MRAM die: Everspin Chandler AZ (MTJ BEOL, co-located at NXP) on GF Singapore 28nm CMOS today; Microchip Fab 4 Gresham OR 200mm from 2H-2027 for lower densities. Board assembly at any U.S. EMS. Not fully U.S.-made at 1Gb density until a U.S. CMOS source exists.

**Who is already doing this:** IBM (in-house FCM MRAM journals since FCM3), Phison and Sage Microelectronics (SSD controllers paired with Everspin 1Gb, 2019), Broadcom/LSI RAID journals, Everspin application engineering (no public PLP reference design found in a 2026-11-01 search), and Teledyne HiRel (Everspin PERSYST plus screening and qualification support for mil/aero from 4Q-2026) for the rugged/defense variant

**Wins on which axis, for which buyer:** lifecycle length and non-volatility of the write cache (no supercap aging), board area, PLP reliability — NOT $/GB — for Tier-2 enterprise/industrial and rugged/defense SSD makers, computational-storage startups, RAID/HBA card makers, flight/data-recorder and PLC OEMs with 10-20-year field life

**Survives a 2029 glut?:** partially — The reliability/supercap-elimination case is independent of DRAM price, but a 60% DDR5/DDR4 drop makes the DRAM+supercap alternative ~$20-50 cheaper per board, so marginal designs revert to DRAM.

**Fatal-flaw candidate:** PLP architecture is chosen by the SSD controller vendor (Phison, Sage, Marvell, Microchip) or done in-house (IBM). A third-party kit sits between them and Everspin with no IP, and new PLP designs per year number in the dozens, so the kit caps below ~$1M/yr. 1Gb ST-DDR4 is single-source Everspin, made on GF Singapore CMOS, and exposed to an ITC 337-TA-1487 exclusion order (~Jul-2027). At ~$51-410 of MRAM per board (64-512 MB at $821/GB), most enterprise SSDs keep supercaps.

*Possible?* yes — the mechanism ships today in IBM FCM5 and LSI RAID journals · *Profitable?* marginal — real but small niche; Everspin captures most of the value · *Doable by this founder?* marginal — T1 and needs an EE partner; no fab, no chip design

*Business-model lenses:* module/appliance (reference design), IP licensing (design package + royalty), design services, defense-first variant (rugged SSDs)

### C-17 — DDR3-EOL Socket Swap to ST-DDR4 MRAM — ☠ KILLED (R4-NO-WINNING-AXIS: The named buyer, an industrial, medical or rail OEM facing a DDR3 EOL, pays for continuity at the lowest respin cost, and MRAM loses on every axis of that purchase. On price, 1Gb ST-DDR4 sells at ~$821/GB street ($102.60 @500), ~32x DDR3 4Gb spot (~$25.5/GB). Modeled silicon is ~$95/GB, ~23x the $4.12/GB foundry DDR3 cost (01_LANDSCAPE 4.1). On density, one die is 1Gb. On compatibility, ST-DDR4 is not pin- or protocol-compatible with DDR3 (the card says so itself), so the 'swap' is a full respin, and a respin to DDR4/LPDDR4 is cheaper. That respin target is now U.S.-made: Micron Manassas 1-alpha DDR4, shipping since 2026-05-22, is aimed at exactly the long-lifecycle buyer and takes away the card's 'U.S. vendor roadmap' axis. Non-volatility is not needed for working DRAM; where it is needed (battery-backed SRAM), C-12 F-RAM or xSPI MRAM is the right part. The card itself says profitable: no.)

*Sub-branch:* STT-MRAM as small-density DRAM replacement (industrial long-lifecycle) · *Materials sense:* a-material

**What it is:** Redesign service and drop-in mezzanine that replace end-of-life 1-4Gb DDR3/DDR4 chips on long-lifecycle industrial, medical and rail controllers with Everspin 1Gb ST-DDR4 STT-MRAM (GF 28nm + Chandler BEOL), selling instant-on non-volatility as the bonus. Target boards that need <=256 MB of working memory.

**Why it could work:** DDR3/DDR4 are being exited by Samsung/SK hynix/Micron in 2026 and DDR4 contract rose >50% QoQ in Q3-2026, so long-lifecycle OEMs face forced respins anyway; a respin to MRAM removes battery-backed SRAM/supercaps and gives a part with a 10+-year roadmap from a U.S. vendor. COMPUTED REALITY: MRAM street ~$100/Gb vs DDR3 4Gb spot ~$3.19/Gb = ~32x per bit; manufacturing cost ~$91/GB (MRAM, 28nm) vs ~$2.5-4.5/GB (DRAM). Doubling DRAM prices does not close a 30x gap.

**Evidence:** TRL 7 · Rule 1: SUPPORTED
  - [DDR4 reportedly leads legacy memory rally; DDR3 in tight supply](https://www.trendforce.com/news/2026/01/19/news-ddr4-reportedly-leads-legacy-memory-rally-with-q1-prices-up-to-50-ddr3-in-tight-supply/) — industry, 2026-01. Makers exiting DDR4 in 2026; DDR3 supply tight (via search snippet)
  - [Memory shortages drive DDR4 prices over 50% in Q3 2026; DDR3 also impacted](https://wccftech.com/memory-shortages-drive-ddr4-prices-over-50-in-q3-2026-ddr3-also-impacted-by-higher-costs/) — news, 2026-07. DDR3 4Gb spot ~$3.19/Gb vs DDR5 16Gb ~$2.94/Gb early July 2026 (via search snippet)
  - [EMD4E001G16G2-150CAS2R listing](https://www.lcsc.com/product-image/C20342497.html) — industry, 2026. 1Gb STT-MRAM reference price $102.60 @500 (~$821/GB) (via search snippet)
  - [World's First 1 Gb 28 nm STT-MRAM Product - by Everspin](https://www.techinsights.com/blog/memory/worlds-first-1-gb-28-nm-stt-mram-product-everspin) — industry, 2019. 1Gb die 105.1 mm2, cell 0.0396 um2, 9.75 Mb/mm2 on GF 28nm (via search snippet)
  - [Winbond says customers seek LTAs through 2030; ADATA expects even tighter DRAM supply in 2027](https://www.trendforce.com/news/2026/08/07/news-winbond-says-customers-seek-ltas-through-2030-adata-expects-even-tighter-dram-supply-in-2027/) — industry, 2026-08-07. Legacy-DRAM buyers are chasing multi-year LTAs; Winbond capacity sold out; no DDR3-specific supply pledge found (via search snippet)

**Capital tier:** T0 | **Time to first revenue:** 6-12 months for a paid redesign study; product revenue only on boards needing <=256 MB | **Gross margin estimate:** 15-35% (services; part resale is distributor-thin)

**US manufacturability:** Everspin Chandler AZ BEOL on GF Singapore CMOS; board work at U.S. EMS

**Who is already doing this:** Micron Manassas (U.S.-made 1-alpha DDR4 for long-lifecycle buyers since 2026-05-22), Rochester/Alliance/Intelligent Memory (legacy DDR3 continuity), Everspin FAEs

**Wins on which axis, for which buyer:** non-volatility + supply longevity (U.S. vendor roadmap) for boards needing <=256 MB — for industrial PLC, medical-device and rail-signalling OEMs with DDR3 EOL exposure

**Survives a 2029 glut?:** no — In a glut DDR3/DDR4 last-time-buy and broker stock gets cheap and plentiful; the only reason to swap (forced EOL respin at shortage prices) disappears and the 30x bit-cost gap widens to ~100x.

**Fatal-flaw candidate:** 30x $/bit gap, 1Gb max per MRAM die (a 1GB board needs 8 dies), and ST-DDR4 is not pin/protocol compatible with DDR3, so a respin to LPDDR4/DDR4 is cheaper for almost everyone.

*Possible?* yes — parts exist · *Profitable?* no — loses on $/GB by ~30x except in rare <=256 MB sockets · *Doable by this founder?* marginal — consulting-only form is T0 but needs an EE

*Business-model lenses:* design services, recert/brokerage (part resale), module (mezzanine)

### C-18 — NewSpace MRAM Radiation-Data & Upscreen Service

*Sub-branch:* Defense/space-first MRAM (data product + screened parts) · *Materials sense:* mixed:a+c

**What it is:** Lead with (a), the lot-specific radiation (TID/SEE/proton) test campaigns and the subscription database with SEE-rate tooling. Demote (b), upscreened serialized parts, to an optional add-on for Toggle parts not covered by Teledyne HiRel's PERSYST program.

**Why it could work:** NewSpace demand is pulling non-volatile MRAM into orbit: Everspin's 64Mb HR xSPI reached full production on LEO demand and Astro Digital picked it for a GEO bus (Q2-2026). Toggle MRAM shows >1 Mrad(Si) TID (Frontgrade/Cobham). Smallsat builders cannot pay QML-V prices or wait 20-26-week lead times (EM064LX 20 wks, EM128LX 26 wks) and want lot-specific COTS+ data. A report sells for ~$5-25k [ESTIMATE]; screened parts carry 2-4x markup on ~$40-60 parts.

**Evidence:** TRL 8 · Rule 1: SUPPORTED
  - [Case study touts Everspin Toggle MRAM for space](https://www.frontgrade.com/news/new-case-study-touts-everspins-toggle-mram-highly-reliable-memory-technology-space) — company, 2020. Toggle MRAM >1 Mrad(Si) TID, QML-Q/Q+ products via Cobham/Frontgrade (via search snippet)
  - [Everspin Q2-2026 earnings call highlights](https://www.marketbeat.com/instant-alerts/everspin-tech-q2-earnings-call-highlights-2026-08-05/) — news, 2026-08. Q2-2026 rev $18.7M (+42%); Astro Digital picked PERSYST 64Mb STT-MRAM for GEO Raven bus; LEO demand drove 64Mb HR production (via search snippet)
  - [EM064LX Future Electronics listing](https://futureelectronics.com/p/semiconductors--memory--RAM--nvram--mram/em064lxoab320is1t-everspin-technologies-4175573) — industry, 2026. 64Mb xSPI STT-MRAM $39.38 @480, 20-week lead time (via search snippet)
  - [EM128LXQAB313IS2T DigiKey listing](https://punchouttest.digikey.hk/en/products/detail/everspin-technologies-inc/EM128LXQAB313IS2T/24375470) — industry, 2026. Everspin 128Mb xSPI MRAM manufacturer lead time 26 weeks (via search snippet)
  - [Everspin earns $40 million MRAM deal for defense memory services](https://electronics360.globalspec.com/article/23702/everspin-earns-40-million-mram-deal-for-defense-memory-services) — news, 2026-04. $40M/2.5-yr subcontract to provide Toggle MRAM process tech and foundry services for DoW Defense Industrial Base; onshore Toggle capability (via search snippet)
  - [Teledyne HiRel Semiconductors and Everspin Technologies Partner to Accelerate MRAM Adoption in Aerospace and Defense Applications](https://www.teledyne-ade.com/en-us/news/Pages/Teledyne-HiRel-Semiconductors-and-Everspin-Technologies-Partner-to-Accelerate-MRAM-Adoption-in-Aerospace-and-Defense-Applic.aspx) — company, 2026-09-02. Teledyne HiRel (Milpitas CA) will sell Everspin PERSYST 256/128/64Mb STT-MRAM to mil/aero and satellite customers with screening flows, qualification documentation, procurement support and obsolescence management; availability expected 4Q-2026 (via search snippet)
  - [Partnership to accelerate MRAM adoption in aerospace and defence applications](https://www.electropages.com/2026/09/partnership-accelerate-mram-adoption-aerospace-and-defence-applications) — news, 2026-09. Trade coverage of the Teledyne HiRel / Everspin PERSYST partnership (via search snippet)
  - [HXNV01600 16 Megabit Non-Volatile Magneto-Resistive RAM datasheet (Honeywell)](https://static6.arrow.com/aropdfconversion/c3d384dea67007fda227b1cda3ffb5a81ac3da9c/hxnv01600_16_megabit_non-volatile_magneto-resistive_ram.pdf) — company, unknown. Honeywell 16Mb rad-hard MRAM on 150nm SOI: 1e6 rad(Si) TID, no latch-up, 15-yr retention at 105C (via search snippet)
  - [What is MRAM and why is it critical to mission success (Honeywell Aerospace blog)](https://www.honeywellaerospace.com/us/en/about-us/blogs/what-is-mram-why-is-it-critical-to-mission-success) — company, unknown. Honeywell offers 1Mb and 16Mb rad-hard monolithic MRAM and a 64Mb rad-hard MRAM MCM; 64Mb monolithic planned (via search snippet)
  - [Radiation Effects and COTS Parts in SmallSats (NASA GSFC)](https://s3vi.ndc.nasa.gov/ssri-kb/static/resources/Radiation%20Effects%20and%20COTS%20Parts%20in%20SmallSats.pdf) — government, unknown. COTS radiation sensitivity can vary more lot to lot, and COTS traceability is often missing, which casts doubt on one-time qualification versus recurring lot acceptance testing (via search snippet)
  - [ESA activity 4000135313 (laser SEE screening of COTS lots)](https://activities.esa.int/4000135313) — government, unknown. A SEE test on one COTS procurement lot is not representative of the next lot, so per-lot screening is needed (via search snippet)

**Capital tier:** T1 | **Time to first revenue:** 15-21 months: first paid lot-acceptance campaign or report for a smallsat bus maker, after a self-funded seed campaign | **Gross margin estimate:** 30-50% (campaign costs are pass-through-heavy; higher only if datasets resell across many buyers)

**US manufacturability:** Parts: Everspin Chandler AZ Toggle line (onshore Toggle program under $40M DoW subcontract), PERSYST on GF CMOS + Chandler BEOL; testing at U.S. beam lines; screening at a U.S. test house (East Coast lab feasible).

**Who is already doing this:** Teledyne HiRel (Milpitas CA; screened PERSYST 64-256Mb with qualification docs from 4Q-2026), Frontgrade (ex-Cobham/Aeroflex, QML Toggle MRAM on Everspin BEOL), Honeywell Plymouth MN (DoD-trusted 1Mb/16Mb rad-hard MRAM and a 64Mb MCM, BEOL by Everspin), Avalanche (1-8Gb space-grade STT-MRAM, UMC 22nm), Everspin HR line, NASA GSFC/NEPP and ESA ESCIES (free radiation data), and European lot-qualified COTS services such as TRAD R2COTS (via search snippet)

**Wins on which axis, for which buyer:** radiation tolerance + non-volatility + data/lot traceability (supply security for NewSpace) — for LEO/GEO smallsat bus and payload makers (Astro Digital-type buyers, constellation primes), university cubesat programs, defense small-launch payload integrators

**Survives a 2029 glut?:** yes — Space buyers price on radiation data and heritage, not on DRAM $/GB; a DDR5 glut does not change rad-hard NVM demand.

**Fatal-flaw candidate:** Credibility and channel: NASA/ESA publish part-type data free, Teledyne HiRel and Frontgrade sell screened MRAM with heritage through authorized channels, and a non-engineer founder has no radiation-effects reputation. Export control is a second gate: parts rated or certified to >=5e3 Gy(Si) (500 krad) TID fall under ECCN 3A001.a.1 [training knowledge, UNVERIFIED], so certifying Toggle MRAM to >1 Mrad can turn screened parts and some data into licensed exports to non-U.S. smallsat builders.

*Possible?* yes — standard industry practice · *Profitable?* marginal — small, credibility-gated market · *Doable by this founder?* marginal — T1 with a rad-effects partner; data platform is the founder's lever

*Business-model lenses:* data product (subscription rad database), defense-first niche, recert/upscreen of parts, SaaS (SEE calculators)

### C-19 — New Fabless Discrete STT-MRAM Vendor — ☠ KILLED (R4-NO-WINNING-AXIS: A me-too fabless STT-MRAM vendor at best ties the incumbents on every axis its named buyer pays for, and it loses on qualification heritage, lead time and scale. Its one possible differentiator, density above Everspin's 1Gb, is already sold. Avalanche (Fremont CA) ships 1, 2, 4 and 8Gb space-grade STT-MRAM on UMC 22nm with >1e16 endurance and 10-yr/125C retention (2024 release, via snippet), and has U.S.-government money to scale the MTJ further (2026-03). The card's flagship 4Gb is half of what is already on the market. Everspin (64Mb-1Gb, IBM/Teledyne HiRel heritage) and Netsol (Samsung 28FDS) cover the NOR/FRAM/PLP sockets, and the card's own model puts a 4Gb 14nm die at ~$72/GB, only ~24% below Everspin's modeled ~$95/GB. Arriving 42 months out, with no U.S. MRAM foundry and FTO exposure to the live Avalanche v. Everspin patent war (ITC 337-TA-1487), it gives a buyer no reason to switch. Same logic as the C-40 kill.)

*Sub-branch:* Discrete STT-MRAM chips (fabless on foundry eMRAM) · *Materials sense:* c-capital

**What it is:** Start a fabless U.S. company selling 128Mb-4Gb discrete STT-MRAM (CoFeB/MgO pMTJ) built on a foundry MRAM module (Samsung 28FDS/14nm, UMC 22nm or TSMC 16nm), competing with Everspin, Netsol and Avalanche in SPI/xSPI and ST-DDR4 sockets.

**Why it could work:** Foundry eMRAM is now standard (Samsung 14/8nm cells 0.024/0.017 um2; GF AutoPro150; TSMC 16nm), so a fabless entrant needs no MTJ fab. COMPUTED: a 4Gb die at 14/16nm with a 0.024 um2 cell is ~229 mm2 and costs ~$72/GB — still ~3.6x the PEAK DDR5 contract price before margin — so the only markets are NOR/FRAM/nvSRAM replacement and PLP, which Everspin already serves.

**Evidence:** TRL 7 · Rule 1: SUPPORTED
  - [IEDM 2024 Samsung eMRAM (PC Watch)](https://pc.watch.impress.co.jp/docs/column/semicon/1649812.html) — conference, 2024-12. Samsung eMRAM cell 0.024 um2 (14nm) and 0.017 um2 (8nm), IEDM 2024 paper 11-4 (via search snippet)
  - [Netsol launches standalone STT-MRAM on Samsung 28nm FDSOI](https://mram-info.com/netsol-launches-stand-alone-stt-mram-product-fabricated-samsung-foundrys-28nm-fdsoi-process) — news, 2023-08. Netsol 1-64Mb parallel/serial STT-MRAM via Samsung Foundry (via search snippet)
  - [Avalanche AS301G208 UMC 22nm 512Mb MRAM Process Analysis](https://www.techinsights.com/blog/avalanche-as301g208-umc-22-nm-512mb-mram-process-analysis) — industry, unknown. Avalanche 512Mb STT-MRAM manufactured at UMC 22nm (via search snippet)
  - [Everspin Q3-2026 results (8-K Ex.99.1)](https://www.sec.gov/Archives/edgar/data/0001438423/000162828026067890/mram-20260930xexx991.htm) — company, 2026-10. Q3-2026 revenue $20.6M, MRAM product $16.9M, GM 51.4%, $6.0M litigation cost, cash $43.0M (via search snippet)
  - [USITC institutes Section 337 investigation 337-TA-1487](https://www.usitc.gov/press_room/news_release/2026/er0227_68226.htm) — government, 2026-02. Avalanche seeks exclusion order against Everspin STT-MRAM imports (via search snippet)
  - [Avalanche Technology: two new densities of 3rd-gen space-grade parallel x32 P-SRAM](https://storagenewsletter.com/2024/04/05/avalanche-technology-two-new-densities-of-3rd-gen-space-grade-parallel-asynchronous-x32-interface-high-reliability-p-sram-memory-devices) — news, 2024-04-05. Avalanche space-grade STT-MRAM family in 1, 2, 4 and 8Gb; 45 ns read/write; >1e16 write endurance; 10-yr retention at 125C; -40 to 125C (via search snippet)
  - [Avalanche Technology and UMC announce 22nm production of high-density MRAM-based devices for aerospace](https://www.avalanche-technology.com/?p=3491) — company, 2023-11. Avalanche high-density MRAM in production on UMC 22nm (via search snippet)
  - [Avalanche Technology phase-one milestone: magnetic cell scaling for space-grade MRAM for the US government](https://www.avalanche-technology.com/avalanche-technology-phase-one-magnetic-cell-scaling-space-grade-mram-us-government/) — company, 2026-03-02. U.S.-government-funded MTJ scaling at 22nm (40 nm CD, <=100 nm pitch) toward higher-density space-grade MRAM (via search snippet)

**Capital tier:** T2 | **Time to first revenue:** 36-48 months (design, MPW, qualification, AEC/JEDEC reliability, design-in cycles) | **Gross margin estimate:** 40-50% at scale (Everspin runs ~51%)

**US manufacturability:** Poor: foundry MRAM modules are at Samsung (Korea/Austin for logic only), UMC (Taiwan/Singapore), TSMC (Taiwan), GF 22FDX (Dresden). No U.S. 300mm MRAM foundry offering; Everspin-Microchip Gresham line is exclusive.

**Who is already doing this:** Avalanche (Fremont CA; 1-8Gb space-grade STT-MRAM on UMC 22nm, U.S.-gov-funded MTJ scaling), Everspin (64Mb-1Gb PERSYST; Teledyne HiRel aerospace channel), Netsol (Samsung 28FDS), Honeywell and Frontgrade (rad-hard MRAM), Renesas/Infineon

**Wins on which axis, for which buyer:** non-volatility + endurance vs NOR/EEPROM (not vs DRAM) — for industrial/automotive NOR/FRAM replacement sockets, FPGA configuration, storage PLP

**Survives a 2029 glut?:** partially — Not priced against DRAM, so the glut does not kill it, but it never wins DRAM sockets in either regime.

**Fatal-flaw candidate:** Crowded tiny market (the category leader books ~$17M/qtr of MRAM product) plus a live patent war (Avalanche v. Everspin ITC 337-TA-1487) — a new entrant buys litigation risk for a market already served.

*Possible?* yes — Netsol did it in ~5 years · *Profitable?* no — crowded, sub-scale, litigious · *Doable by this founder?* no — T2 chip company

*Business-model lenses:* fabless->foundry; IP licensing (unlikely); defense-first variant

### C-20 — MRAM Main-Memory DIMM / CXL Module — ☠ KILLED (R4-NO-WINNING-AXIS: Main memory is bought on $/GB, density, bandwidth and W/GB, and MRAM loses all four. The device model (models/device_cost_compare.py) gives ~$94.9/GB silicon+package. That is 5.9x the $15.99 4Q26 DDR5 contract, 14.8x the $6.40 glut and ~58x incumbent cost ($1.64). Street price ($821/GB) is ~51x contract. Density is 0.0095 vs ~0.40-0.44 Gb/mm2 (~42-46x), so a 32GB RDIMM needs 256 1Gb dies (~26,900 mm2 of silicon). The card itself lists buyer 'none at scale' and wins_axis 'non-volatility only'. The persistence buyer is better served by C-51 (persistent CXL log card), which needs MRAM only for the journal.)

*Sub-branch:* STT-MRAM as DRAM replacement · *Materials sense:* a-material

**What it is:** A persistent DDR4/DDR5 RDIMM or CXL Type-3 module populated with STT-MRAM dies (Everspin 1Gb ST-DDR4 today, hypothetical 4Gb 16nm dies later) sold as non-volatile main memory for servers during the DRAM shortage.

**Why it could work:** Tempting because DRAM is 2-3x and MRAM is non-volatile with no refresh. COMPUTED KILL: Everspin 1Gb density 9.75 Mb/mm2 vs ~400 Mb/mm2 for 1b DRAM (~42x less silicon-efficient). A 32GB RDIMM needs 256 MRAM dies (~27,000 mm2) vs 16 DRAM dies (~640 mm2). Cost ~$91/GB (28nm) or ~$72/GB (16nm) vs DDR5 ~$20/GB peak and ~$8/GB glut; street MRAM ~$821/GB.

**Evidence:** TRL 4 · Rule 1: SUPPORTED
  - [World's First 1 Gb 28 nm STT-MRAM Product - by Everspin](https://www.techinsights.com/blog/memory/worlds-first-1-gb-28-nm-stt-mram-product-everspin) — industry, 2019. 1Gb die 105.1 mm2, cell 0.0396 um2, 9.75 Mb/mm2 on GF 28nm (via search snippet)
  - [EMD4E001G16G2-150CAS2R listing](https://www.lcsc.com/product-image/C20342497.html) — industry, 2026. 1Gb STT-MRAM reference price $102.60 @500 (~$821/GB) (via search snippet)
  - [DRAM spot price snapshot (citing TrendForce)](https://www.buysellram.com/?p=20058) — news, 2026-08. DDR5 16Gb spot avg $53.92 on 2026-08-31 (~$27/GB) (via search snippet)
  - [IEDM 2024 Samsung eMRAM (PC Watch)](https://pc.watch.impress.co.jp/docs/column/semicon/1649812.html) — conference, 2024-12. Samsung eMRAM cell 0.024 um2 (14nm) and 0.017 um2 (8nm), IEDM 2024 paper 11-4 (via search snippet)

**Capital tier:** T2 | **Time to first revenue:** Never at a price any main-memory buyer pays | **Gross margin estimate:** negative at DRAM-parity pricing (~-355% at $20/GB)

**US manufacturability:** Dies: Everspin Chandler AZ + GF Singapore; module assembly U.S. possible (SMART Modular-type assemblers)

**Who is already doing this:** Nobody at volume; Everspin demonstrated ST-MRAM DIMMs ~2013-2016 [UNVERIFIED: training] and moved to niche PLP

**Wins on which axis, for which buyer:** non-volatility only; loses on $/GB, density, bandwidth and power per GB — for none at scale (in-memory DB persistence is better served by DRAM + NVMe logging)

**Survives a 2029 glut?:** no — At $8/GB DRAM the gap becomes ~10x on cost and ~100x on street price.

**Fatal-flaw candidate:** ~40x density deficit and ~4x-plus cost above peak DRAM price; physics of 50 F2 1T1MTJ cells vs 6 F2 1T1C.

*Possible?* marginal — buildable but absurdly sized · *Profitable?* no — loses on every buyer axis except persistence · *Doable by this founder?* no

*Business-model lenses:* module/appliance

### C-21 — Second U.S. MTJ BEOL Line on a Depreciated 200mm Fab — ☠ KILLED (FACT-COLLAPSE: The card's concept, a second U.S. MTJ line in a depreciated 200mm fab for DoD, is already being built by the incumbent in the obvious host. Everspin's 10-year agreement puts 8-inch MRAM/TMR/STT wafers in Microchip Fab 4, Gresham OR (first products 2H-2027, up to 1,300 wafers/qtr), and bars Microchip from making TMR devices for Everspin's competitors. DoD's onshore Toggle need is funded through Everspin's $40M/2.5-yr DIB subcontract. Honeywell Plymouth, one of two U.S. rad-hard foundries with DoD Accreditation of Trust, already sells 1Mb/16Mb rad-hard MRAM and a 64Mb MCM (MTJ BEOL by Everspin). The demand gap and the host are taken, and no MTJ process-IP source is open to a startup: Everspin is the competitor, and Avalanche is fabless at UMC and in litigation with Everspin. The card also names no host fab ('an idle 200mm line in the Northeast or Texas'), which would separately fail QB-INCOMPLETE.)

*Sub-branch:* MRAM manufacturing capacity (cheaper capital) · *Materials sense:* c-capital

**What it is:** Install an MTJ back-end module (multi-target PVD such as Canon Anelva/Applied Endura-class, ion-beam etch, magnetic anneal) in an idle or depreciated U.S. 200mm fab and offer Toggle/STT MRAM foundry services as a second U.S. source to DoD and IoT customers.

**Why it could work:** Depreciated 200mm capacity is cheap capital and DoD wants onshore Toggle MRAM ($40M DoW subcontract to Everspin, Apr-2026). But Everspin already locked the obvious partner: Microchip Fab 4 Gresham OR, 10-year deal, up to 1,300 wafers/qtr, and Microchip is barred from making TMR devices for Everspin competitors. Minimal MTJ module capex ~$20-50M [ESTIMATE] for a market whose leader books ~$65-70M/yr of MRAM product.

**Evidence:** TRL 8 · Rule 1: SUPPORTED
  - [Everspin 8-K: Foundry Services Agreement with Microchip](https://www.sec.gov/Archives/edgar/data/1438423/000162828026024696/mram-20260408xexx991.htm) — company, 2026-04. 10-yr deal: Microchip Fab 4 (Gresham OR) 8-inch MRAM/TMR/STT wafers, ramp to max 1,300 wafers/qtr, first products 2H-2027; Microchip barred from making TMR devices for Everspin competitors (via search snippet)
  - [Everspin earns $40 million MRAM deal for defense memory services](https://electronics360.globalspec.com/article/23702/everspin-earns-40-million-mram-deal-for-defense-memory-services) — news, 2026-04. $40M/2.5-yr subcontract to provide Toggle MRAM process tech and foundry services for DoW Defense Industrial Base; onshore Toggle capability (via search snippet)
  - [Everspin Form 10-K FY2025](https://www.sec.gov/Archives/edgar/data/1438423/000162828026014733/mram-20251231.htm) — company, 2026-03. Everspin buys foundry CMOS wafers and adds MTJ BEOL in Chandler AZ; single foundry GLOBALFOUNDRIES Singapore for higher-density products (via search snippet)
  - [Everspin Q3-2026 results (8-K Ex.99.1)](https://www.sec.gov/Archives/edgar/data/0001438423/000162828026067890/mram-20260930xexx991.htm) — company, 2026-10. Q3-2026 revenue $20.6M, MRAM product $16.9M, GM 51.4%, $6.0M litigation cost, cash $43.0M (via search snippet)
  - [Honeywell develops non-volatile magnetic solid-state memory for strategic space applications](https://www.militaryaerospace.com/computers/article/16724564/honeywell-develops-nonvolatile-magnetic-solidstate-memory-for-strategic-space-applications) — news, 2007. Honeywell Plymouth MN is one of two U.S. rad-hard wafer foundries with DoD Accreditation of Trust (0.15/0.35/0.8 um) (via search snippet)
  - [HXNV01600 16 Megabit Non-Volatile Magneto-Resistive RAM datasheet (Honeywell)](https://static6.arrow.com/aropdfconversion/c3d384dea67007fda227b1cda3ffb5a81ac3da9c/hxnv01600_16_megabit_non-volatile_magneto-resistive_ram.pdf) — company, unknown. Honeywell 16Mb rad-hard MRAM on 150nm SOI: 1e6 rad(Si) TID, no latch-up, 15-yr retention at 105C (via search snippet)
  - [What is MRAM and why is it critical to mission success (Honeywell Aerospace blog)](https://www.honeywellaerospace.com/us/en/about-us/blogs/what-is-mram-why-is-it-critical-to-mission-success) — company, unknown. Honeywell offers 1Mb and 16Mb rad-hard monolithic MRAM and a 64Mb rad-hard MRAM MCM; 64Mb monolithic planned (via search snippet)
  - [NASA NTRS 20140011394 (MRAM reliability study)](https://ntrs.nasa.gov/api/citations/20140011394/downloads/20140011394.pdf) — government, 2014. Everspin Chandler AZ does the back-end magnetic processing for both Aeroflex (Frontgrade) and Honeywell MRAM (via search snippet)

**Capital tier:** T2 | **Time to first revenue:** 36-60 months (tool install, process transfer/licensing, qualification) | **Gross margin estimate:** 20-40% foundry services at low loading

**US manufacturability:** By design U.S. (e.g., an idle 200mm line in the Northeast or Texas) — but needs MTJ process IP that only Everspin/Avalanche/foundries hold

**Who is already doing this:** Everspin (Chandler AZ BEOL in NXP's fab, plus the Microchip Fab 4 Gresham OR 200mm second line from 2H-2027, Everspin-exclusive for TMR), Honeywell Plymouth MN (DoD-trusted rad-hard MRAM, BEOL by Everspin), foundry eMRAM offshore (GF Dresden, TSMC, Samsung, UMC)

**Wins on which axis, for which buyer:** supply security / trusted U.S. source — for DoD primes and the Defense Industrial Base

**Survives a 2029 glut?:** partially — Defense demand is price-insensitive, but commercial loading collapses and a sub-scale line cannot absorb fixed cost.

**Fatal-flaw candidate:** No process IP and no demand gap: Everspin's onshore expansion with Microchip and DoW money already fills the U.S. trusted-MRAM need.

*Possible?* yes · *Profitable?* no — sub-scale vs Everspin+Microchip · *Doable by this founder?* no

*Business-model lenses:* foundry services; defense-first

### C-22 — TrustNVM: U.S.-Made ReRAM Secure-NVM Chiplet on SkyWater S130 — ☠ KILLED (RED-TEAM: the ReRAM T2 leg was killed (magnet-immunity axis shared by OTP/eFuse/S130 eNVM, no named buyer; RT-VET-DD5-05, RT-PHY-DD5-05) while C-33 survives as a side line. See 05_REDTEAM.md (DD5) and 04_DEEPDIVES/open-memory-ip.md §14.)

*Sub-branch:* Embedded ReRAM (oxide 1T1R) via licensed IP at a U.S. trusted foundry · *Materials sense:* mixed:a+c

**What it is:** A fabless 1-4 Mb serial NVM / secure-boot key-store and FPGA-configuration chip using Weebit Nano's JEDEC-qualified 1T1R oxide ReRAM module in SkyWater's S130 130nm process (Bloomington MN), sold to DoD primes and rugged-board makers that need domestic, trusted, radiation-tolerant NVM to replace imported SPI NOR/EEPROM (e.g., Renesas serial EEPROM, last-time ship 2026-10-31).

**Why it could work:** The ReRAM module is already qualified (256Kb, 3 lots, 10-yr retention, 125C) and sits in the S130 PDK, so IP risk is low and capital is licensed, not owned. SkyWater is a U.S. foundry used for DoD work [trusted-foundry accreditation: UNVERIFIED in this session]. Oxide ReRAM is reported to be intrinsically radiation tolerant [UNVERIFIED: literature]. Chips price per part ($20-200 in defense), so the ~$3,300/GB bit cost is irrelevant. SBIR/STTR topics for trusted microelectronics can fund the design.

**Evidence:** TRL 6 · Rule 1: SUPPORTED (commercial NVM); PARTIAL for the radiation-tolerant variant
  - [Weebit Nano's ReRAM IP now fully qualified in SkyWater S130](https://www.weebit-nano.com/news/press-releases/weebit-nanos-reram-ip-now-fully-qualified-in-skywater-technologys-s130-process/) — company, 2023-06. 256Kb 1T1R ReRAM module JEDEC-qualified (3 lots), 10-yr retention at industrial temp, in SkyWater S130 PDK (via search snippet)
  - [Weebit ReRAM IP achieves high-temperature qualification in SkyWater S130](https://www.skywatertechnology.com/weebit-nano-reram-ip-achieves-high-temperature-qualification-in-skywater-s130-process/) — company, 2023-11. Qualified to 125C, ready for production tape-out at SkyWater (via search snippet)
  - [Weebit Nano secures a license agreement with Texas Instruments](https://www.weebit-nano.com/news/press-releases/weebit-nano-secures-a-license-agreement-with-texas-instruments/) — company, 2025-12. TI licenses Weebit embedded ReRAM (tech transfer, design enablement, qualification) (via search snippet)
  - [Renesas EOL plan: serial EEPROM products](https://www.renesas.cn/zh/document/gde/eol-plan-serial-eeprom-products) — company, 2025-11. Renesas serial EEPROM families EOL, last-time shipment 2026-10-31 (via search snippet)
  - [TSMC 2025 Annual Report ch.5](https://investor.tsmc.com/static/annualReports/2025/english/pdf/2025_tsmc_ar_e_ch5.pdf) — company, 2026. TSMC N12e RRAM consumer-qualified; 22RRAM passed 100K-cycle qualification in 2025 (via search snippet)
  - [Weebit ReRAM NVM in SkyWater 130nm CMOS (product page)](https://www.weebit-nano.com/products/embedded-reram-ip/weebit-reram-nvm-in-skywater-130nm-cmos/) — company, 2026. Weebit ReRAM module proven in S130 silicon, qualified at industrial temperature, 'ready for production'; SkyWater holds a non-exclusive license, and Weebit earns license fees plus volume royalties (via search snippet)
  - [Weebit Nano expands licensing agreements with key customers; three customer chip designs taped out to date](https://www.weebit-nano.com/news/press-releases/weebit-nano-expands-licensing-agreements-with-key-customers-three-customer-chip-designs-taped-out-to-date/) — company, 2026-07. Three customer designs taped out (foundries not named); Weebit expects 12-18 months of characterisation and qualification after tape-out (via search snippet)
  - [Initial studies confirm ReRAM's tolerance to high levels of gamma radiation](https://www.weebit-nano.com/?p=13325) — company, 2023-03. University of Florida / CEA-Leti study: Weebit ReRAM kept data and function after high gamma doses (via search snippet)
  - [ReRAM NVM Shines, Even in High-Rad Applications](https://embeddedcomputing.com/technology/storage/reram-nvm-shines-even-in-in-high-rad-applications) — news, 2023. Only 16-kbit arrays were characterized; gamma only, no heavy-ion SEE data; described as a starting point (via search snippet)
  - [Honeywell develops non-volatile magnetic solid-state memory for strategic space applications](https://www.militaryaerospace.com/computers/article/16724564/honeywell-develops-nonvolatile-magnetic-solidstate-memory-for-strategic-space-applications) — news, 2007. Honeywell Plymouth MN is one of two U.S. rad-hard wafer foundries with DoD Accreditation of Trust (0.15/0.35/0.8 um) (via search snippet)

**Capital tier:** T2 | **Time to first revenue:** ~36 months to production revenue; token engineering-sample sales possible at 24-30 months; SBIR Phase I/II funds design but does not count | **Gross margin estimate:** 50-65% (defense pricing) after Weebit royalty

**US manufacturability:** SkyWater Technology (IonQ subsidiary since 2026-07-31), Bloomington MN, S130 200mm 130nm with Weebit ReRAM in the PDK; DMEA Trusted Foundry status per 2022 DoD award coverage (via snippet). U.S. OSAT: Integra, Promex/QP Technologies, or SkyWater Florida.

**Who is already doing this:** Weebit (IP; first product licensee is a U.S. company for security applications; three customer tape-outs by 2026-07, foundries not named), SkyWater (foundry), Everspin Toggle MRAM (U.S.-made, $40M DoW onshore program), Honeywell Plymouth (DoD-trusted rad-hard MRAM), Teledyne HiRel (screened PERSYST MRAM for mil/aero from 4Q-2026), Frontgrade, Infineon/Cypress rad-hard NOR/F-RAM, Microchip serial EEPROM

**Wins on which axis, for which buyer:** Supply security (DMEA-trusted U.S. foundry flow), magnetic-field immunity versus MRAM and no stored charge versus floating-gate EEPROM for secure-boot/key storage, and EOL replacement. Radiation tolerance is STILL-UNVERIFIED at array level. Not $/GB. — for DoD primes and subsystem makers needing trusted NVM for secure boot, key storage, parameter/config storage for small FPGAs and CPLDs, and anti-tamper modules; rugged industrial board makers

**Survives a 2029 glut?:** yes — Defense trusted-NVM demand is not tied to DRAM pricing.

**Fatal-flaw candidate:** Incumbent U.S.-made rad-tolerant NVM (Everspin Toggle, Honeywell trusted MRAM) beats a 1-4 Mb ReRAM chip on density (16-32 Mb), endurance (MRAM effectively unlimited vs ReRAM ~1e4-1e5 cycles [training knowledge]) and heritage. The radiation claim rests on 16-kbit gamma tests with bulk-CMOS periphery. Modeled bit cost is ~$3,539/GB, which ties Toggle's ~$3,797/GB, so cost is no lever. The one clean axis is trusted-flow, magnet-immune key storage, and DoDI 5200.44 trust requirements target custom ICs, not COTS memory (C-71 audit), so demand at defense volumes is small.

*Possible?* yes — qualified IP in a U.S. PDK · *Profitable?* marginal — small defense volumes, incumbent MRAM · *Doable by this founder?* no — needs an IC design co-founder and SBIR money

*Business-model lenses:* fabless->foundry, IP licensing (in-licensed), defense-first, SBIR-funded

### C-23 — University / Expired-Patent CBRAM-ReRAM IP Licensor — ☠ KILLED (R4-NO-WINNING-AXIS: For the named buyer (second-tier foundries and IDMs that want eNVM at 40-130nm), every alternative is already qualified and on offer. Weebit ReRAM is JEDEC-qualified in SkyWater S130 (2023) and DB HiTek 130nm BCD (2026-01), and licensed to onsemi (2025-01) and TI (2025-12). TSMC sells RRAM at 40/28/22/12nm, and GF owns the production CBRAM (bought from Renesas, 2023-02) and also offers eMRAM. Expired PMC/CBRAM patents are public domain, so the startup has nothing exclusive to license, no process recipe and no qualification data. It wins on none of the axes the buyer pays for: qualification, mask adder (GF holds the 1-mask CBRAM know-how), exclusivity or support. The card itself says the axis is 'not RAM', the business is not profitable and the founder cannot do it. Its TRL 8 is borrowed from Adesto/GF; this venture would restart at TRL 3.)

*Sub-branch:* ReRAM/CBRAM IP licensing (university tech-transfer path) · *Materials sense:* c-capital

**What it is:** License (or design around expired) early CBRAM/PMC patents (Ag/Cu-GeS conductive-bridge lineage from ASU -> Axon -> Adesto) or oxide ReRAM patents from a university tech-transfer office, package them with a test-chip on an MPW, and license the eNVM module to second-tier foundries/IDMs.

**Why it could work:** CBRAM needs ~1 extra mask on logic (GF statement), and the oldest PMC patents date to the late 1990s so freedom-to-operate may be cheap. But the production-proven CBRAM now belongs to GlobalFoundries (bought from Renesas, 2023); TSMC has in-house RRAM at 28/22/12nm; Weebit, the best-funded independent ReRAM licensor (A$167M cash), took ~10+ years to reach ~A$13.5M FY26 revenue; 4DS was suspended from ASX quotation in Apr-2026.

**Evidence:** TRL 3 · Rule 1: SUPPORTED (cell mechanism); core value claim (foundries license an unqualified expired-patent module) UNSUPPORTED
  - [GlobalFoundries acquires Renesas' non-volatile resistive RAM (CBRAM) technology](https://gf.com/gf-press-release/globalfoundries-acquires-renesas-non-volatile-resistive-ram-technology-to-proliferate-iot-and-5g-applications/) — company, 2023-02. Adesto->Dialog->Renesas CBRAM now owned by GF; being qualified on 22FDX; ~1 extra mask (via search snippet)
  - [New Adesto memory takes 25 years to consume a battery](https://spectrum.ieee.org/new-adesto-memory-takes-25-years-to-consume-a-battery) — news, 2016. Adesto CBRAM ultra-low-energy products shipped (Moneta/Mavriq) (via search snippet)
  - [Weebit Nano expands licensing agreements; three customer chip designs taped out](https://www.weebit-nano.com/news/press-releases/weebit-nano-expands-licensing-agreements-with-key-customers-three-customer-chip-designs-taped-out-to-date/) — company, 2026-07. 3 customer tape-outs; FY26 revenue guide >=A$13.5M; cash A$167M; licensing slowed by fab undercapacity (via search snippet)
  - [4DS Memory filings index (suspension from quotation 2026-04-29)](https://financialfilings.com/companies/4ds-memory-limited/) — other, 2026-04. 4DS (PCMO interface-switching ReRAM) suspended from ASX quotation Apr-2026 (via search snippet)
  - [TSMC 2025 Annual Report ch.5](https://investor.tsmc.com/static/annualReports/2025/english/pdf/2025_tsmc_ar_e_ch5.pdf) — company, 2026. TSMC N12e RRAM consumer-qualified; 22RRAM passed 100K-cycle qualification in 2025 (via search snippet)

**Capital tier:** T2 | **Time to first revenue:** 6+ years: qualify a module in a foundry first, then sell licenses into fabs that already have Weebit, TSMC RRAM or GF CBRAM/eMRAM | **Gross margin estimate:** 80-90% on license revenue, but revenue tiny

**US manufacturability:** Test chips at SkyWater MN or via MPW; licensees are foundries anywhere

**Who is already doing this:** Weebit Nano (qualified in SkyWater S130 and DB HiTek 130nm BCD; licensed to onsemi Treo 65nm and TI), GlobalFoundries (owns Adesto CBRAM; eMRAM on 22FDX), TSMC (RRAM 40/28/22/12nm), Infineon (RRAM MCUs on TSMC), Crossbar (private, status unverified), 4DS (suspended 2026-04)

**Wins on which axis, for which buyer:** eNVM cost (masks) for MCUs — not RAM — for second-tier foundries and IDMs wanting eNVM at 40-130nm

**Survives a 2029 glut?:** yes — Unrelated to DRAM price; but irrelevant to the DRAM shortage too.

**Fatal-flaw candidate:** Decade-long licensing sales cycles in a field where the strongest independent (Weebit) is still sub-scale and foundries own their own RRAM/CBRAM.

*Possible?* yes for the cell; no for the business (expired patents confer nothing licensable) · *Profitable?* no — revenue too slow and small · *Doable by this founder?* no

*Business-model lenses:* university/lab patent license, IP licensing

### C-24 — RRAM Analog In-Memory-Compute Edge AI Chip — ☠ KILLED (R4-NO-WINNING-AXIS: The card describes TetraMem's existing product line: multi-level HfOx/TaOx RRAM analog-IMC SoCs on TSMC 22nm/12nm with on-chip INT4 weights. TetraMem, a California company, validated 22nm MLX200 silicon (2026-05, sampling 2H-2026) and taped out the 12nm MLX300 with 64M INT4 params and a 50-80 TOPS/W target (2026-10-27). It also licenses the RRAM IP. A new entrant reaches silicon around 2029-30 after T3 money (~$50-150M [ESTIMATE]). It would run the same TSMC Taiwan wafers with the same U.S. HQ, so it offers the named buyer nothing TetraMem does not: no better TOPS/W, no supply-security axis, and later maturity and support. The 'less DRAM' axis does not apply to its named hearing-aid and industrial-sensor buyers, whose SoCs carry no external DRAM. The surviving form of this idea is C-55, a T1 module integrator that buys CIM chips.)

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

**Who is already doing this:** TetraMem (MLX200 22nm silicon, MLX300 12nm tape-out, RRAM IP licensing), Mythic (analog flash), EnCharge AI (charge-domain SRAM analog), Sagence AI, IBM Research (PCM analog AI), plus digital edge NPUs (Syntiant, Hailo, Ambiq) [non-TetraMem names UNVERIFIED-training, cross-ref C-55]

**Wins on which axis, for which buyer:** TOPS/W and DRAM bandwidth avoided for always-on edge inference — for wearable, hearing-aid, industrial-sensor and always-on vision module makers

**Survives a 2029 glut?:** partially — Irrelevant to the DRAM cycle in both directions. The named hearing-aid and sensor buyers have no external DRAM, so the card has no DRAM-shortage relevance to lose or gain

**Fatal-flaw candidate:** Analog drift/accuracy plus a software stack war against digital NPUs; TetraMem is already two tape-outs ahead with TSMC access.

*Possible?* yes (TetraMem silicon); no as a differentiated new entrant · *Profitable?* marginal — crowded edge-AI market · *Doable by this founder?* no

*Business-model lenses:* fabless->foundry, IP licensing (TetraMem offers multi-level RRAM IP)

### C-25 — 3D XPoint / PCM Crosspoint Revival for the CXL Memory Tier — ☠ KILLED (R3-FAB/T4: The card's own minimum viable path is a new 300mm crosspoint fab (T4). No foundry offers PCM/OTS crosspoint, and the only U.S. XPoint fab (Lehi) now runs TI 65/45nm analog. Benchmarks: Micron sold Lehi for $900M cash plus ~$600M of tools, below book, after ~$545M of underutilization charges in four quarters, and Intel lost >$7B and wrote off $559M of Optane inventory. That puts any new entrant well above the $1B line (A-11). The device model computes $0.99/GB at full loading (device_cost_output, C-25 row), the only alternative under DDR5 cost. Reaching that loading is exactly what killed Optane, and the process IP stays with Intel/Micron, while SanDisk and imec are already prototyping 3D Matrix Memory. C-96 covers the IP-estate variant.)

*Sub-branch:* Phase-change crosspoint storage-class memory (Optane post-mortem) · *Materials sense:* a-material · *Merged from:* A2.10, B.09

**What it is:** Rebuild Optane-class memory: Ge-Sb-Te phase-change (or OTS selector-only) cells in a 4-deck 20nm-half-pitch crosspoint, sold as CXL Type-3 persistent/capacity memory at a fraction of DRAM $/GB during the shortage.

**Why it could work:** The math looks great in Nov-2026: XPoint Gen2 was 1.31 Gb/mm2 (~3.3x 1b DRAM density) and at full fab loading the die cost computes to ~$1/GB vs DDR5 at ~$20/GB. But Optane died anyway: Intel lost >$7B, took a $559M inventory write-off (Q2-2022); Micron cited 'insufficient market validation', booked ~$545M underutilization in 4 quarters and sold Lehi to TI for $900M (below book). The killers were volume (Lehi underloaded), an Intel-only DDR-T ecosystem, ~3-4x DRAM latency, and the 2019 DRAM glut erasing Optane's ~$6.6/GB price advantage. SanDisk + imec are now prototyping '3D Matrix Memory' (target ~half DRAM cost/bit, no dates).

**Evidence:** TRL 5 · Rule 1: SUPPORTED
  - [Intel 10-Q Q2-2022](https://www.sec.gov/Archives/edgar/data/50863/000005086322000030/intc-20220702.htm) — company, 2022-07. Optane wind-down; $559M inventory impairment (via search snippet)
  - [Micron sells Lehi 3D XPoint fab to Texas Instruments for $900M](https://www.anandtech.com/show/16800) — news, 2021-06. Lehi sold to TI for $900M cash (+~$600M tools), below book value (via search snippet)
  - [Micron updates data center portfolio strategy (ends 3D XPoint)](https://www.nasdaq.com/press-release/micron-updates-data-center-portfolio-strategy-to-address-growing-opportunity-for) — company, 2021-03. 'insufficient market validation' to keep investing in 3D XPoint; CXL pivot (via search snippet)
  - [Persistent Memories Without Optane: Where Would We Be? (Coughlin & Handy)](https://www.snia.org/sites/default/files/2025-05/SNIA-SDC22-Coughlin-Handy-Persistent-Memories-Without-Optane-Where-Would-We-Be.pdf) — conference, 2022. Intel Optane losses >$7B; emerging memory moving to foundry embedded (via search snippet)
  - [Intel 2nd generation XPoint memory](https://www.techinsights.com/blog/memory/intel-2nd-generation-xpoint-memory) — industry, 2020. 256Gb 4-deck die 195.6 mm2, 1.31 Gb/mm2 (via search snippet)
  - [SanDisk makes first 3D Matrix Memory chips aiming for half the cost per bit of DRAM](https://www.notebookcheck.net/SanDisk-makes-first-3D-Matrix-Memory-chips-aiming-for-half-the-cost-per-bit-of-DRAM.1374351.0.html) — news, 2026-08. SanDisk crosspoint-class prototypes on 300mm, multi-Gb, target ~half DRAM cost/bit, no dates (via search snippet)
  - [Does phase change memory ride again with SanDisk?](https://www.eenewseurope.com/en/does-phase-change-memory-ride-again-with-sandisk) — news, 2025. 3D Matrix Memory resembles 3D XPoint; imec 'Project Neo' since 2024 (via search snippet)
  - [Pricing of Intel's Optane DC Persistent Memory Modules Leaks](https://www.anandtech.com/show/14180) — news, 2019-04. PMem 128GB ~$842-893 ($6.6-7.0/GB), 256GB ~$10.4-11.1/GB (via search snippet)
  - [SanDisk Investor Day 2026](https://quartr.com/events/sandisk-corporation-sndk-investor-day-2026_F6lVAkBS) — company, 2026. CROSS-REF (A2.jsonl snippet). SanDisk memory roadmap beyond NAND (3D Matrix Memory nearing product specs).
  - [Intel Optane DIMM Pricing: $695 for 128GB, $2595 for 256GB, $7816 for 512GB](https://www.tomshardware.com/uk/news/intel-optane-dimm-pricing-performance,39007.html) — news, 2019-04. Launch pricing of Optane PMem (via search snippet)

**Capital tier:** T4 | **Time to first revenue:** 6+ years for a new entrant (tech hit TRL 9 at Intel/Micron 2017-22, but process IP stays with them; new entrants restart near TRL 4-6) | **Gross margin estimate:** theoretical 75-85% at full loading vs $8/GB glut DRAM; deeply negative during ramp (Intel/Micron history)

**US manufacturability:** Lehi UT (the only U.S. XPoint fab) now runs TI analog/embedded at 65/45nm; a new 300mm fab is T4

**Who is already doing this:** SanDisk + imec (3D Matrix Memory prototypes on 300mm); Samsung/SK hynix/Micron selector-only memory research (IEDM 2022-24); see C-96 for the IP-estate variant

**Wins on which axis, for which buyer:** $/GB and capacity vs DRAM for a CXL capacity tier (in theory) — for hyperscaler CXL memory-tier and in-memory database buyers (who already chose CXL DRAM + NVMe/KV-cache offload instead)

**Survives a 2029 glut?:** no — A fab started now ships ~2030 into the cycle after the 2028-29 glut; Optane already showed a DRAM glut erases the price gap that justifies the latency penalty.

**Fatal-flaw candidate:** T4 capital and 6-year timeline, IP owned by Intel/Micron, and the exact volume/ecosystem trap that cost Intel >$7B; incumbents (SanDisk/imec) are ahead.

*Possible?* yes — it shipped 2017-2022 · *Profitable?* no — for anyone below SanDisk/Samsung scale · *Doable by this founder?* no

*Business-model lenses:* fabless->foundry (impossible: no foundry offers it), IP licensing (Intel/Micron unlikely to license)

### C-26 — Optane PMem Salvage: Cheap Memory-Mode Capacity for Cascade/Ice Lake Fleets — ☠ KILLED (RED-TEAM: DD1 (Provenance & Recertified Memory) was KILLED by the four-persona red team: The three FATAL objections hold: the named core buyer (OEM-compatible module makers) already knows its die source from POs, CoCs and package top marks and may self-certify under the proposed FAR rule, and resellers may rely on that free certificate. The die-source library was sampled from the wrong population (old OEM DDR4), keyed wrongly (module P/N) and replicable, so the moat is gone; the C-85 predictive subscript See 05_REDTEAM.md (DD1) and 04_DEEPDIVES/provenance-recert.md §14.)

*Sub-branch:* Optane post-mortem arbitrage (recovered XPoint modules) · *Materials sense:* c-capital

**What it is:** Buy decommissioned Intel Optane PMem 100/200 modules (128/256/512 GB, 3D XPoint Gen1 media) from U.S. ITAD/recyclers, health-test them (ipmctl SMART/percentage-used, burn-in), and sell validated kits plus a web sizing tool that configures Memory Mode or App Direct for VMware/KVM, SAP HANA, Redis and HPC nodes on 2nd/3rd-gen Xeon Scalable servers.

**Why it could work:** DDR4 RDIMMs rose >50% QoQ in Q3-2026 and DDR4 is being exited, so owners of still-useful Cascade Lake/Ice Lake fleets cannot cheaply add memory. New PMem cost $6.6-11/GB in 2019 and Intel exited with ~2 years of excess XPoint inventory; recovered modules may trade at ~$0.8-2/GB [UNVERIFIED] vs DDR4 RDIMM ~$25+/GB. Memory Mode uses DRAM as cache in front of 4-8x more PMem capacity. Software (sizing, health certificates, config scripts) is the founder's edge.

**Evidence:** TRL 9 · Rule 1: SUPPORTED (price gap evidenced via search snippet: used 256GB ~$0.6-1/GB vs $15.99/GB DDR contract)
  - [Pricing of Intel's Optane DC Persistent Memory Modules Leaks](https://www.anandtech.com/show/14180) — news, 2019-04. PMem 128GB ~$842-893 ($6.6-7.0/GB), 256GB ~$10.4-11.1/GB (via search snippet)
  - [Intel kills off Optane memory, writes off $559M inventory](https://www.datacenterdynamics.com/en/news/intel-kills-off-optane-memory-writes-off-559-million-inventory) — news, 2022-07. Optane wind-down; reports of ~2 years of excess XPoint inventory (via search snippet)
  - [Intel 10-Q Q2-2022](https://www.sec.gov/Archives/edgar/data/50863/000005086322000030/intc-20220702.htm) — company, 2022-07. Optane wind-down; $559M inventory impairment (via search snippet)
  - [Memory shortages drive DDR4 prices over 50% in Q3 2026; DDR3 also impacted](https://wccftech.com/memory-shortages-drive-ddr4-prices-over-50-in-q3-2026-ddr3-also-impacted-by-higher-costs/) — news, 2026-07. DDR3 4Gb spot ~$3.19/Gb vs DDR5 16Gb ~$2.94/Gb early July 2026 (via search snippet)
  - [DDR4 reportedly leads legacy memory rally; DDR3 in tight supply](https://www.trendforce.com/news/2026/01/19/news-ddr4-reportedly-leads-legacy-memory-rally-with-q1-prices-up-to-50-ddr3-in-tight-supply/) — industry, 2026-01. Makers exiting DDR4 in 2026; DDR3 supply tight (via search snippet)
  - [vSphere/vSAN Support update for Intel's Optane Persistent Memory (PMem)](https://knowledge.broadcom.com/external/article/326910) — company, unknown (pre-VCF 9.0). PMem support, both Memory Mode and App Direct, discontinued starting VCF 9.0 (via search snippet)
  - [End of General Support for vSphere 8.0](https://knowledge.broadcom.com/external/article/459135/end-of-general-support-for-vsphere-80.html) — company, unknown. vSphere 8.x end of general support 2027-10-11 (via search snippet)
  - [VCF 9 deprecated features (vSphere/NSX)](https://www.starwindsoftware.com/blog/vcf9-deprecated-vsphere-nsx/) — blog, 2025. ESX 9.0 ended support for Intel Optane PMem (via search snippet)
  - [SAP HANA support update for Intel Optane persistent memory](https://blogs.sap.com/2022/10/10/sap-hana-support-update-for-intel-optane-persistent-memory/) — company, 2022-10-10. SAP continues PMem support per SAP Note 2618154 / 2954515 (via search snippet)
  - [Intel 128GB DDR4-2666 DDR-T Optane persistent memory module (refurb listing)](https://www.itcreations.com/product/128717) — other, unknown. A U.S. refurb-server seller already lists PMem modules (via search snippet; page unreachable)
  - [Uvation Marketplace: Intel memory](https://marketplace.uvation.com/datacenter-campus/memory/intel) — other, unknown. A marketplace listing PMem 200-series modules (via search snippet; currency of listing unclear)

**Capital tier:** T0 | **Time to first revenue:** 2-6 months: first kits sold on eBay/own storefront to refurb-server buyers and homelab/SMB | **Gross margin estimate:** 20-35% on kits; used-PMem prices are public on eBay and ipmctl health checks are free to replicate

**US manufacturability:** No fabrication; U.S. sourcing from ITAD firms and testing in an East Coast garage/lab (Xeon Cascade Lake test server ~$1-3k)

**Who is already doing this:** Refurb-server sellers already list PMem 100/200 modules (ITCreations, Uvation marketplace), plus many eBay US/DE sellers with transparent used prices (~$0.5-3/GB); ITADs sell lots direct

**Wins on which axis, for which buyer:** $/GB of usable memory capacity for legacy Intel platforms (plus persistence in App Direct) — for KVM/Proxmox/Linux SMBs and MSPs on Cascade/Ice Lake, SAP HANA hosts (PMem still supported per SAP Notes 2618154/2954515), research HPC labs, refurb-server resellers, homelab. VMware shops only until vSphere 8 EoGS (2027-10-11); VCF/ESX 9.0 dropped PMem

**Survives a 2029 glut?:** no — Dies twice. VMware support ends 2027-10-11 (before the glut), and when DDR4 falls ~60% in 2028-29 the price gap shrinks just as Cascade/Ice Lake fleets retire

**Fatal-flaw candidate:** Finite and shrinking supply and installed base (Intel exited 2022; only 2nd/3rd-gen Xeon Scalable). VMware dropped PMem in VCF 9.0 with vSphere 8 EoGS 2027-10-11. Memory Mode latency penalty. Used prices already transparent on eBay. A 2-year bridge line, best run as a SKU of C-62

*Possible?* yes — the parts and platforms exist · *Profitable?* marginal: real but small, a ~2-year window ending with vSphere 8 EoGS and Cascade/Ice Lake retirement · *Doable by this founder?* yes — the most founder-doable card in A2

*Business-model lenses:* recert/brokerage, SaaS (sizing/health tool), data product (PMem health/price index)

### C-27 — SOT-MRAM Last-Level-Cache Chiplet — ☠ KILLED (QB-INCOMPLETE: The card names no fab or partner that could make the product, and none exists. Its own us_manufacturability says no foundry offers a leading-edge SOT-MRAM module. A 2026-11 search found SOT-MRAM still at the imec/TSMC research stage (300mm manufacturability demos, a 1ns TSMC result), with no foundry PDK. The independent SOT startup Antaios has had no news since its 2021 tier-1-foundry test chip, and Dealroom lists it as closed. imec is an R&D programme, not a production partner, so the gap cannot be fixed within any venture horizon. The card's claimed density axis also fails on its own numbers: a 0.03 um2 2T1R cell is ~1.4x the 0.021 um2 N5 HD SRAM bitcell, and the device model puts it at ~$280/GB (14x contract, 34x glut). That leaves only standby leakage, which matters little to always-on AI accelerators.)

*Sub-branch:* SOT-MRAM (moonshot SRAM replacement) · *Materials sense:* a-material

**What it is:** A UCIe-attached cache chiplet using spin-orbit-torque MRAM (beta-W/Ta SOT track under CoFeB/MgO MTJ, 2T1R) to replace SRAM last-level cache in AI accelerators at N5-class nodes.

**Why it could work:** imec reports SOT switching <100 fJ/bit and >1e15 endurance (IEDM-2023) and a 2025 IEEE TED study shows BEOL read selectors shrink bitcells 10-40% toward sub-N3 SRAM area; multi-bit VGSOT claims ~3x SRAM density. COMPUTED: even at 0.03 um2 a 1Gb die is ~80 mm2 at ~$262/GB — an SRAM-replacement play, not a DRAM one.

**Evidence:** TRL 4 · Rule 1: SUPPORTED
  - [Why SOT-MRAM can replace SRAM in future cache memories](https://imec-int.com/en/articles/bringing-sot-mram-technology-closer-last-level-cache-memory-specifications) — industry, 2023. imec SOT-MRAM <100 fJ/bit, >1e15 endurance (IEDM 2023) (via search snippet)
  - [SOT-MRAM bitcell scaling with BEOL read selectors (IEEE TED)](https://imec-publications.be/handle/20.500.12860/59271) — peer-reviewed, 2025. BEOL read selectors cut SOT bitcell area 10-40%, approaching sub-N3 SRAM (via search snippet)
  - [MRAM startup makes progress as rival closes (Antaios)](https://www.eenewseurope.com/en/mram-startup-makes-progress-as-rival-closes/) — news, 2021-09. Antaios SOT-MRAM test chip at tier-1 foundry 28/22nm; eVaderis closed (via search snippet)
  - [Antaios company profile](https://app.dealroom.co/companies/antaios) — other, unknown. Antaios listed as 'closed' (undated, unverified) (via search snippet)
  - [imec demonstrates manufacturability of state-of-the-art SOT-MRAM devices on 300mm Si wafers](https://www.eejournal.com/industry_news/imec-demonstrates-manufacturability-of-state-of-the-art-spin-orbit-torque-mram-devices-on-300mm-si-wafers/) — industry, unknown. SOT-MRAM manufacturability demo at imec R&D scale (via search snippet)
  - [36Kr: MRAM industrialization 2026 (TSMC 1ns SOT-MRAM, Qingdao 8-inch MRAM line)](https://eu.36kr.com/en/p/3806128847675144) — news, 2026-05. Trade-press view that SOT-MRAM signals in 2026 are research breakthroughs, not foundry products (via search snippet)
  - [SOT MRAM Pioneer Antaios Secures 11 Million Dollars in Funding](https://www.businesswire.com/news/home/20200916005720/en/SOT-MRAM-Pioneer-Antaios-Secures-11-Million-Dollars-in-Funding) — company, 2020-09-16. Antaios last funding ($11M, 2020); no later round found (via search snippet)

**Capital tier:** T3 | **Time to first revenue:** 7+ years | **Gross margin estimate:** unknown; 50% if achieved

**US manufacturability:** Requires a leading-edge foundry MTJ/SOT module (TSMC/Samsung/Intel); none offered commercially

**Who is already doing this:** imec (300mm SOT demos), TSMC/ITRI, Samsung, Intel R&D; JST/AIST cache project in Japan; Antaios (no news since 2021, listed closed); eVaderis closed 2017

**Wins on which axis, for which buyer:** standby leakage only; cache density loses (0.03 um2 SOT 2T1R vs 0.021 um2 N5 HD SRAM) — for AI accelerator and CPU designers

**Survives a 2029 glut?:** partially — Not tied to DRAM price, but irrelevant to the DRAM shortage.

**Fatal-flaw candidate:** TRL 4 plus dependence on a leading-edge foundry module that only the foundries/IDMs control; independent SOT startups have folded.

*Possible?* marginal — lab-proven, not product-proven · *Profitable?* no · *Doable by this founder?* no

*Business-model lenses:* IP licensing, fabless->foundry

### C-28 — eMRAM-Unified-Memory Edge MCU (no external DRAM) — ☠ KILLED (SCORE<55: Scored 45.0/100 default (rank 37/40), 45.8 moonshot. Weakest: time to revenue 1/5 (48 months: SoC design, AEC/industrial qualification and an ecosystem.); U.S. mfg 1/5 (GF 22FDX eMRAM is made in Dresden and TSMC RRAM in Taiwan; no U.S. line offers 22nm eNVM.); competition 1/5 (Renesas RA8P1, Infineon PSoC Edge (RRAM), ST STM32V8 (ePCM), SEMIFIVE/ICY Tech on Samsung 8nm eMRAM and Everspin UNISYST already do exactly ). Scorer verdicts — founder: Head-on against four MCU giants, fabbed offshore and four years from revenue: the worst founder fit in my chunk. | vc: Head-on against Renesas, ST, Infineon and NXP with a die-area trick that loses to $4 of LPDDR in a glut, fabbed in Dresden: the classic memory-startup graveyard pitch. | veteran: A me-too edge MCU against four incumbents that already ship eNVM AI parts, made offshore, with a differentiator a glut erases; no.)

*Sub-branch:* Embedded NVM (eMRAM/RRAM/ePCM) SoC · *Materials sense:* mixed:a+b

**What it is:** A fabless edge-AI MCU on GF 22FDX+ AutoPro150 eMRAM (alt: TSMC 22RRAM) holding 16-64 MB of weights and code on-die, with working data and activations in on-die SRAM, so the board needs no external DRAM/PSRAM or NOR for small-to-mid models

**Why it could work:** Foundry eNVM is mature: GF AutoPro150 (Auto Grade 1, 500k cycles, <10ns read, volume 2H-2026 Dresden, PDK self-serve), TSMC 22RRAM (100K cycles), ST/Samsung 18nm ePCM (0.059 um2 cell, smallest). Removing an external LPDDR4 (now ~2x price) saves BOM and standby power.

**Evidence:** TRL 7 · Rule 1: SUPPORTED
  - [GlobalFoundries announces AutoPro150 eMRAM on FDX](https://www.globenewswire.com/news-release/2026/03/09/3251832/0/en/GlobalFoundries-Announces-Availability-of-AutoPro150-eMRAM-Technology-on-Enhanced-FDX-Platform-for-Advanced-Automotive-Applications.html) — company, 2026-03. Auto Grade 1 eMRAM, 500k cycles, <10ns read; volume 2H-2026 at Dresden; PDK via GF Connect (via search snippet)
  - [ST first 18nm FD-SOI + ePCM MCU (STM32V8)](https://news.mynavi.jp/techplus/article/20251120-3693534/) — news, 2025-11. ST ePCM 0.059 um2 vs MRAM 0.129 um2 (16nm) vs RRAM 0.174 um2 (12nm) per ST; co-developed with Samsung Foundry (via search snippet)
  - [TSMC 2025 Annual Report ch.5](https://investor.tsmc.com/static/annualReports/2025/english/pdf/2025_tsmc_ar_e_ch5.pdf) — company, 2026. TSMC N12e RRAM consumer-qualified; 22RRAM passed 100K-cycle qualification in 2025 (via search snippet)
  - [Infineon and TSMC to introduce RRAM for automotive MCUs](https://www.eenewseurope.com/en/infineon-and-tsmc-to-introduce-rram-for-automotive-mcus) — news, 2022. AURIX TC4x on TSMC 28nm RRAM (via search snippet)
  - [IEDM 2024 Samsung eMRAM (PC Watch)](https://pc.watch.impress.co.jp/docs/column/semicon/1649812.html) — conference, 2024-12. Samsung eMRAM cell 0.024 um2 (14nm) and 0.017 um2 (8nm), IEDM 2024 paper 11-4 (via search snippet)
  - [Renesas RA8P1 Integrates MRAM, Elevating Edge AI](https://www.techinsights.com/blog/renesas-ra8p1-integrates-mram-elevating-edge-ai) — industry, 2025. RA8P1: 1GHz Cortex-M85 + NPU + up to 1MB eMRAM on TSMC 22nm ULL, for edge AI (via search snippet)
  - [Renesas launched a new AI MCU that has 1 MB of embedded on-chip MRAM](https://www.mram-info.com/renesas-launched-new-ai-mcu-has-1-mb-embedded-chip-mram) — news, 2025. Renesas eMRAM AI MCU shipping (via search snippet)
  - [PSoC Edge MCU brings RRAM to AI at the edge](https://cdn.eenewseurope.com/en/psoc-edge-mcu-brings-rram-to-ai-at-the-edge/) — news, unknown. Infineon edge-AI MCU with RRAM (via search snippet)
  - [SEMIFIVE and ICY Tech edge-AI SoC on Samsung 8nm eMRAM](https://tirto.id/c-o-r-r-e-c-t-i-o-n-semifive-hvHD) — news, unknown. Edge-AI SoC taped out on Samsung 8nm eMRAM; target up to 2B parameters (via search snippet)
  - [Everspin launches new generation of unified memory for embedded systems](https://www.yolegroup.com/industry-news/everspin-launches-new-generation-of-unified-memory-for-embedded-systems/) — industry, unknown. Everspin UNISYST standalone MRAM unifying code and data for edge AI (via search snippet)

**Capital tier:** T2 | **Time to first revenue:** 4+ years (SoC design, AEC/industrial qual, ecosystem) | **Gross margin estimate:** 40-55%

**US manufacturability:** Weak: GF 22FDX eMRAM is in Dresden (not Malta NY); TSMC RRAM in Taiwan; ST ePCM captive (Crolles/Samsung). No U.S. line offers this eNVM at 22nm.

**Who is already doing this:** Renesas RA8P1/RA8M2/RA8D2 (up to 1MB eMRAM, TSMC 22ULL, NPU), Infineon PSoC Edge and AURIX TC4x (RRAM), ST STM32V8 (ePCM), NXP eMRAM MCUs [UNVERIFIED], SEMIFIVE + ICY Tech edge-AI SoC on Samsung 8nm eMRAM (taped out), Everspin UNISYST standalone unified MRAM, Ambiq/Alif/GreenWaves MRAM MCUs [UNVERIFIED-training]

**Wins on which axis, for which buyer:** BOM and standby power (no external DRAM/NOR), instant-on — for industrial/automotive edge-AI module makers

**Survives a 2029 glut?:** partially — The 'avoid DRAM' pitch weakens when 512MB LPDDR4X falls from ~$10.5 to ~$4. Standby power and instant-on remain

**Fatal-flaw candidate:** Head-on competition with Renesas, ST, Infineon and NXP, which already ship eNVM edge-AI MCUs. The only differentiator (16-64MB on-die) costs die area and loses to cheap LPDDR in a glut. Not manufacturable in the U.S. (GF eMRAM is in Dresden, TSMC in Taiwan)

*Possible?* yes · *Profitable?* no — for a startup vs ST/Infineon/NXP/Renesas · *Doable by this founder?* no

*Business-model lenses:* fabless->foundry

### C-29 — NVM-EOL Migration Finder (MRAM/FeRAM/ReRAM cross-reference SaaS)

*Sub-branch:* Software tool for the shortage, grounded in emerging-NVM device data · *Materials sense:* none

**What it is:** A web app that ingests PCN/EOL notices and distributor data for serial/parallel EEPROM, NOR and NVSRAM/BBSRAM parts and recommends pin- and protocol-compatible F-RAM/MRAM/ReRAM replacements with BOM-cost, lead-time and qualification deltas. DRAM EOLs are out of scope (no emerging NVM matches DDR3/DDR4 density, pinout or cost)

**Why it could work:** 2026 is an EOL wave (DDR3/DDR4 exits, serial EEPROM EOLs) during a shortage, and emerging-NVM parts are under-known by component engineers. The founder can build it with no hardware capital; device knowledge from this branch becomes the data moat (density, endurance, interface compatibility).

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [Renesas EOL plan: serial EEPROM products](https://www.renesas.cn/zh/document/gde/eol-plan-serial-eeprom-products) — company, 2025-11. Renesas serial EEPROM families EOL, last-time shipment 2026-10-31 (via search snippet)
  - [DDR4 reportedly leads legacy memory rally; DDR3 in tight supply](https://www.trendforce.com/news/2026/01/19/news-ddr4-reportedly-leads-legacy-memory-rally-with-q1-prices-up-to-50-ddr3-in-tight-supply/) — industry, 2026-01. Makers exiting DDR4 in 2026; DDR3 supply tight (via search snippet)
  - [EM128LXQAB313IS2T DigiKey listing](https://punchouttest.digikey.hk/en/products/detail/everspin-technologies-inc/EM128LXQAB313IS2T/24375470) — industry, 2026. Everspin 128Mb xSPI MRAM manufacturer lead time 26 weeks (via search snippet)
  - [EM064LX Future Electronics listing](https://futureelectronics.com/p/semiconductors--memory--RAM--nvram--mram/em064lxoab320is1t-everspin-technologies-4175573) — industry, 2026. 64Mb xSPI STT-MRAM $39.38 @480, 20-week lead time (via search snippet)
  - [Renesas Completes Acquisition of Altium](https://www.renesas.com/en/about/newsroom/renesas-completes-acquisition-altium) — company, 2024-08-01. Altium (owner of Octopart/Nexar, prior knowledge) is a wholly owned Renesas subsidiary; goal includes component lifecycle management (via search snippet)
  - [Everspin MR1A16A 2Mb parallel MRAM (Mouser)](https://www.mouser.in/en/new/everspin-technologies/everspin-mr1a16a-mram-memory/) — industry, unknown. Everspin positions MRAM as replacing Flash, SRAM, EEPROM and BBSRAM; no cross-reference tool found (via search snippet)
  - [F-RAM for Smart E Meters (DigiKey PTM)](https://www.digikey.com/en/ptm/c/cypress/f-ram-for-smart-e-meters) — industry, unknown. Vendor training on swapping EEPROM for F-RAM (via search snippet)

**Capital tier:** T0 | **Time to first revenue:** 6-9 months: first paid seats from mid-size industrial OEMs; referral revenue later | **Gross margin estimate:** 75-85%

**US manufacturability:** n/a (software); promotes U.S.-made parts (Everspin Chandler) as a filter

**Who is already doing this:** SiliconExpert (Arrow), Z2Data, Octopart/Nexar (Altium, a Renesas subsidiary since 2024-08-01, building component lifecycle management), Accuris, Supplyframe/Findchips (Siemens), distributor parametric search, vendor training (Infineon F-RAM-for-EEPROM PTMs; Everspin 'drop-in replacement' positioning)

**Wins on which axis, for which buyer:** time-to-replacement for NVM (EEPROM/NOR/NVSRAM) EOLs only, where endurance or speed justifies a 10-100x per-bit premium — for component/reliability engineers at industrial, medical and defense OEMs facing NVM/DRAM EOL

**Survives a 2029 glut?:** partially — EOLs continue in a glut, but shortage urgency and willingness to pay fall.

**Fatal-flaw candidate:** Incumbent lifecycle databases (one now owned by Renesas) already provide cross-references. The DRAM half of the pitch is false. The emerging-NVM slice is probably too narrow for standalone SaaS and fits better as lead-gen inside C-12 or C-80

*Possible?* yes · *Profitable?* no to marginal: narrow slice, free alternatives (Octopart, distributor parametric search) and a Renesas-owned incumbent · *Doable by this founder?* yes

*Business-model lenses:* SaaS, data product, referral/brokerage

### C-30 — Floating-body 1T-DRAM (Z-RAM lineage) on U.S. SOI — ☠ KILLED (R4-NO-WINNING-AXIS: The card's own model puts the cell at 0.031 Gb/mm2 (14x below 1b DRAM's 0.436) and ~$24/GB. That is 1.5x the $15.99/GB 4Q26 contract, 3.8x the canonical $6.40 glut and ~15x the $1.64 incumbent cost; the card's 'below $27 spot' framing compares against spot, not contract. The named buyer (legacy DDR3/DDR4 industrial) can already buy foundry DDR3 costing ~$4.12/GB (LANDSCAPE s4.1) and U.S.-made Micron Manassas DDR4. The cell still refreshes (ms-class retention at 85C), so it offers no retention, non-volatility or latency edge behind a DDR interface. The LLC-macro variant serves the same buyer as C-32 with a worse integration path (SOI-only, impact-ionization writes).)

*Sub-branch:* Capacitor-less silicon DRAM: floating body · *Materials sense:* mixed:b+c

**What it is:** Recreate a Z-RAM/Toshiba-FBC-style floating-body 1T cell (charge held in the body of an SOI MOSFET and read as a threshold-voltage shift) on a GlobalFoundries SOI flow (45RFSOI-class at a U.S. GF fab [UNVERIFIED-training]; note 22FDX is made in Dresden, not the U.S.). Product: standalone 2-4 Gb DDR3/DDR4-interface dies for legacy-DRAM buyers, or last-level-cache macros.

**Why it could work:** No storage capacitor, so only 1-2 extra masks on a logic SOI flow instead of a DRAM stack-capacitor module. Depreciated SOI capacity exists in the U.S. On paper an 8F2 cell at 45nm gives 0.031 Gb/mm2 and about $24/GB including test (A3_device_params C-30), which is below today's DDR5 spot (~$27/GB). The 2026 capacitor-less revival (NEO 3D X-DRAM PoC) shows the industry still wants capacitor-less DRAM.

**Evidence:** TRL 4 · Rule 1: SUPPORTED-WEAK (training-only citation, no URL verified in Phase 3)
  - [NEO Semiconductor demonstrates 3D X-DRAM proof of concept](https://www.storagenewsletter.com/2026/05/13/neo-semiconductor-demonstrates-3d-x-dram-proof-of-concept-secures-strategic-investment-to-advance-ai-memory/) — news, 2026-04. 2026 capacitor-less DRAM revival: PoC retention >1 s at 85C, >1e14 cycles, <10 ns, fabbed at TSRI (IGZO/3D-NAND-style, not Si floating body) (CROSS-REFERENCE: seen in another agent's search results, not opened by A3)
  - [DRAM value-per-area chart (Kurnal Insights)](https://www.kitguru.net/channel/generaltech/joao-silva/new-dram-value%E2%80%91per%E2%80%91area-chart-draws-attention-amid-rising-memory-prices/) — news, 2026-09. 1b DRAM bit density ~0.436 Gb/mm2, the reference against which A3 densities are compared (CROSS-REFERENCE: seen in another agent's search results, not opened by A3)
  - [Innovative Silicon Z-RAM (AMD 2006, Hynix 2007 licenses; company closed 2010; patents to Micron) and Toshiba FBC ISSCC/IEDM papers 2002-2008]() — conference, 2002-2010. [UNVERIFIED-training] citation from A3 training data (<= mid-2026). No URL could be opened or seen this session: the shared WebSearch budget was exhausted and web hosts returned proxy 403. Verify agent: add a URL or downgrade. Shows floating-body cells worked in 128Mb-class SOI test chips but never reached a qualified product.

**Capital tier:** T3 | **Time to first revenue:** >60 months (needs foundry JDA, array-scale reliability, then qualification) | **Gross margin estimate:** negative in glut; ~10-20% at 2026 spot if it worked

**US manufacturability:** A U.S. GlobalFoundries SOI line (Malta NY / Essex VT; which SOI flows run in the U.S. in 2026 is [UNVERIFIED-training]) under a JDA. GF offers no capacitor-less DRAM today, and A3 knows no U.S. line running one.

**Who is already doing this:** Nobody in Si floating-body production. Micron reportedly holds the ISi Z-RAM patents [UNVERIFIED-training]. NEO Semiconductor (3D X-DRAM, see C-05) and Unisantis (Dynamic Flash Memory) [UNVERIFIED-training] are the capacitor-less revivals. Samsung and SK hynix publish capacitor-less 3D DRAM research.

**Wins on which axis, for which buyer:** None. $/GB loses even at the 2026 contract price; still needs refresh; latency advantage is irrelevant behind DDR3/DDR4 I/O. — for Hypothetical legacy DDR3/DDR4 industrial buyers; SoC teams wanting dense LLC on SOI.

**Survives a 2029 glut?:** no — Computed ~$24/GB vs canonical glut $6.40/GB (3.8x), 4Q26 contract $15.99/GB (1.5x) and incumbent cost $1.64/GB (~15x). Dies in the glut and is already underwater at today's contract.

**Fatal-flaw candidate:** Physics at scale: body charge is a few hundred electrons at 45nm and tens in thin FD-SOI, so sense margin, retention and disturb immunity collapse with variability. AMD and Hynix both licensed Z-RAM and dropped it (2006-2010) [UNVERIFIED-training].

*Possible?* marginal — demonstrated in test chips 15-20 years ago, never qualified; scaling makes it harder · *Profitable?* no — 14x density gap vs 1b DRAM; ~$24/GB vs glut ~$11/GB · *Doable by this founder?* no — T3 device program

*Business-model lenses:* university/lab patent license (expired/expiring 2002-2008 filings); fabless->foundry; IP licensing — all fail on cost

### C-31 — Thyristor RAM revival (T-RAM TCCT / Kilopass VLT) — ☠ KILLED (R4-NO-WINNING-AXIS: The only variant that beats DRAM on $/GB (Kilopass VLT 4F2, 'DRAM cost minus 45%') was never shown in an array, so it is UNSUPPORTED. Planar TCCT computes to ~$18/GB: above the $15.99 contract today, 2.8x the $6.40 glut and ~11x the $1.64 incumbent cost, and its 1-2 ns read is erased behind a DDR interface. The cache-macro variant has no real buyer at the U.S. nodes named. GF's U.S. SOI flows are RF-SOI and SkyWater 90nm FD-SOI is a rad-hard flow, neither of which hosts cache-hungry SoCs, and neither offers the 2-4-mask thyristor module. GF/AMD's own patent (US7630235) records TCCT-DRAM write-0 charge-loss disturb. A buyer who wants denser-than-SRAM cache at a U.S. node gets it with zero masks from gain cells (C-32), which RAAAM is now qualifying with GF.)

*Sub-branch:* Capacitor-less silicon DRAM: thyristor · *Materials sense:* b-process

**What it is:** Revive the thin capacitively-coupled thyristor (TCCT) T-RAM cell, or Kilopass's vertical-layered-thyristor (VLT) cross-point cell, as a capacitor-less SRAM/DRAM replacement on a U.S. line (a GF U.S. SOI flow or SkyWater 90nm FD-SOI [UNVERIFIED-training]). Product: cache macros, or a standalone DRAM-replacement die.

**Why it could work:** A PNPN latch stores the bit with built-in gain, so it reads fast (1-2 ns claimed) and needs no capacitor. The VLT marketing claim (4F2, no refresh, 'DRAM cost minus 45%') computes to ~$2.8/GB, DRAM-cost parity (A3-02b). A planar TCCT at 10F2/32nm computes to ~$18/GB. The earliest Stanford NDR-cell patents (~1998) have expired, so IP is no longer the barrier [UNVERIFIED-training].

**Evidence:** TRL 4 · Rule 1: SUPPORTED for planar TCCT (patents; test arrays [UNVERIFIED-training]); UNSUPPORTED for the VLT 4F2 variant
  - [DRAM value-per-area chart (Kurnal Insights)](https://www.kitguru.net/channel/generaltech/joao-silva/new-dram-value%E2%80%91per%E2%80%91area-chart-draws-attention-amid-rising-memory-prices/) — news, 2026-09. 1b DRAM bit density ~0.436 Gb/mm2, the reference against which A3 densities are compared (CROSS-REFERENCE: seen in another agent's search results, not opened by A3)
  - [T-RAM Semiconductor TCCT (AMD license 2006, GlobalFoundries 32/22nm SOI partnership 2009; company defunct ~2010-11) and Kilopass VLT announcement (2016; Kilopass acquired by Synopsys 2018)]() — conference, 1998-2018. [UNVERIFIED-training] citation from A3 training data (<= mid-2026). No URL could be opened or seen this session: the shared WebSearch budget was exhausted and web hosts returned proxy 403. Verify agent: add a URL or downgrade. Shows TCCT SRAM test arrays on SOI; VLT never shown in an array.
  - [US7630235B2 Memory cells, memory devices and integrated circuits incorporating the same](https://patents.google.com/patent/US7630235) — patent, 2009. GF/AMD TCCT-based TRAM and access-less TCCT-DRAM cells; TCCT-DRAM suffers disturbance such as charge loss during write-zero (via search snippet)
  - [US6778435B1 Memory architecture for TCCT-based memory cells](https://patents.google.com/patent/US6778435) — patent, 2004. T-RAM Semiconductor TCCT cell architecture (current-mode bit line) (via search snippet)

**Capital tier:** T3 | **Time to first revenue:** >60 months | **Gross margin estimate:** negative

**US manufacturability:** A GF U.S. SOI flow or SkyWater Bloomington MN 90nm FD-SOI [UNVERIFIED-training]. Neither offers a thyristor module.

**Who is already doing this:** Nobody commercially. GF dropped T-RAM. Synopsys owns the Kilopass assets and has not marketed VLT [UNVERIFIED-training]. There is some academic TCAD work on 3D thyristor DRAM.

**Wins on which axis, for which buyer:** Read latency (SRAM-class) and density vs SRAM. It does not win on $/GB vs DRAM except in the never-demonstrated VLT claim. — for None identified: U.S. SOI flows (GF RF-SOI, SkyWater 90nm FD-SOI) serve RF and rad-hard parts, not cache-limited SoCs

**Survives a 2029 glut?:** no — ~$18/GB planar TCCT vs canonical glut $6.40/GB (2.8x) and 4Q26 contract $15.99/GB; VLT parity claim is unsupported marketing.

**Fatal-flaw candidate:** The ON state needs a holding current. At 1-100 pA/cell a 1 Gb array idles at ~1-110 mA, and the bistable window shrinks at 85-125C. Three serious attempts failed to productize: AMD 2006, GlobalFoundries 2009, Kilopass 2016 [UNVERIFIED-training].

*Possible?* marginal — TCCT arrays demonstrated, temperature/standby problems unsolved · *Profitable?* no · *Doable by this founder?* no

*Business-model lenses:* expired-patent practice; IP licensing; fabless->foundry

### C-32 — Si gain-cell eDRAM (GCRAM) IP for U.S. trailing-node SoCs — ☠ KILLED (RED-TEAM: the gain-cell T2 leg was killed (no density/leakage case on sky130, no named buyer; RT-VET-DD5-03, RT-PHY-DD5-03/04) while C-33 survives as a side line. See 05_REDTEAM.md (DD5) and 04_DEEPDIVES/open-memory-ip.md §14.)

*Sub-branch:* Capacitor-less silicon DRAM: 2T/3T gain-cell eDRAM in logic · *Materials sense:* b-process

**What it is:** A memory-IP company that builds and licenses a logic-compatible (zero extra masks) 2T/3T silicon gain-cell eDRAM compiler, first for SkyWater S130/S90 FD-SOI and GlobalFoundries 12LP+ (Malta NY). It replaces 6T SRAM in edge-AI activation buffers, image-sensor line buffers and FPGA block RAM. Revenue is a per-node license fee plus royalty, sold through the foundry IP catalog, as SkyWater already does for Weebit ReRAM.

**Why it could work:** SRAM scaling has stalled. 6T SRAM silicon costs ~$55-72/GB at 7-28nm, ~$195/GB at 65nm and ~$1,330/GB at SkyWater 130nm (01_LANDSCAPE s4.4), so a gain cell at ~50-60% of 6T area saves ~40% of memory area. Foundries pay for differentiated embedded memory (GF-RAAAM 2026; SkyWater-Weebit).

**Evidence:** TRL 5 · Rule 1: SUPPORTED (industry sources: RAAAM/GF GCRAM, via search snippets)
  - [Disrupting the DRAM roadmap with capacitor-less IGZO DRAM technology](https://www.imec-int.com/en/articles/disrupting-dram-roadmap-capacitor-less-igzo-dram-technology) — industry, 2023. 2T0C gain-cell concept: charge stored on the read-transistor gate capacitance — the same topology as Si gain cells (CROSS-REFERENCE: seen in another agent's search results, not opened by A3)
  - [IGZO-2T eDRAM: hybrid IGZO/Si gain cells (DATE 2026)](https://past.date-conference.com/proceedings-archive/2026/DATA/154.pdf) — conference, 2026. IGZO 2T eDRAM is slow (low mobility); hybrid IGZO/Si gain cells proposed — Si read devices give speed, oxide gives retention (CROSS-REFERENCE: seen in another agent's search results, not opened by A3)
  - [Weebit Nano ReRAM IP achieves high-temperature qualification in SkyWater S130](https://www.skywatertechnology.com/weebit-nano-reram-ip-achieves-high-temperature-qualification-in-skywater-s130-process/) — company, 2023-11. SkyWater's S130 PDK hosts third-party memory IP — precedent for licensing a memory macro into a U.S. 130nm foundry (CROSS-REFERENCE: seen in another agent's search results, not opened by A3)
  - [GlobalFoundries acquires Renesas CBRAM technology](https://gf.com/gf-press-release/globalfoundries-acquires-renesas-non-volatile-resistive-ram-technology-to-proliferate-iot-and-5g-applications/) — company, 2023-02. Foundries pay for differentiated embedded-memory IP (GF bought CBRAM, ~1 extra mask, qualifying on 22FDX) (CROSS-REFERENCE: seen in another agent's search results, not opened by A3)
  - [Georgia Tech (Shimeng Yu) 3T IWO eDRAM for in-memory compute](https://hg.gatech.edu/node/675050) — industry, 2024. U.S. university gain-cell eDRAM work (oxide-channel 3T) for compute-in-memory (CROSS-REFERENCE: seen in another agent's search results, not opened by A3)
  - [OpenRAM open-source SRAM compiler (GitHub README; v1.2.50 commit 2026-10-27)](https://github.com/VLSIDA/OpenRAM) — industry, 2026-10. Opened via git: BSD-3 SRAM compiler, generates GDS/LEF/Liberty/SPICE for sky130 (SkyWater) and gf180mcu; actively maintained (last commit 2026-10-27)
  - [Si gain-cell eDRAM literature: Intel 2T gain cell 65nm (Somasekhar, ISSCC 2008/JSSC 2009); Teman/Giterman/Burg 28nm FD-SOI gain cells; RAAAM Memory Technologies GCRAM]() — conference, 2008-2025. [UNVERIFIED-training] citation from A3 training data (<= mid-2026). No URL could be opened or seen this session: the shared WebSearch budget was exhausted and web hosts returned proxy 403. Verify agent: add a URL or downgrade. Shows silicon-proven gain-cell macros at 65-16nm in academia and one startup.
  - [GlobalFoundries and RAAAM: GCRAM technology and test chip on the FDX platform](https://silicon-saxony.de/en/globalfoundries-and-raaam-memory-technologies-development-of-next-generation-gcram-technology-and-a-test-chip-on-the-fdx-platform/) — news, 2026. GF-RAAAM collaboration to develop and qualify Si gain-cell RAM; GCRAM test vehicle taped out on GF FDX; lead-customer design access early 2027; projected ~40% area / up to 60% power reduction vs SRAM (via search snippet)
  - [RAAAM moving toward 2nm qualification at TSMC](https://techtime.news/2025/11/05/raaam/) — news, 2025-11-05. RAAAM heading to TSMC 2nm qualification; search summary reports $17.5M Series A led by NXP and GCRAM demonstrated from 180nm to 5nm FinFET (via search snippet; page not opened, figure attribution within result set unconfirmed)
  - [Memory startup pitches space-efficient GCRAM as SRAM drop-in](https://www.allaboutcircuits.com/news/memory-startup-pitches-space-efficient-gcram-as-sram-drop-in/) — news, unknown. 3T gain cell with background refresh positioned as SRAM drop-in (via search snippet)
  - [IonQ Completes Acquisition of SkyWater Technology](https://thequantuminsider.com/2026/07/31/ionq-completes-skywater-acquisition-quantum-manufacturing/) — news, 2026-07-31. SkyWater is now a wholly owned IonQ subsidiary; states it continues serving all foundry customers; MN/FL/TX sites stay active (via search snippet)
  - [Cadence and SkyWater Detail Next Open Multi-Project Wafer Shuttle Program](https://www.electronics-lab.com/cadence-and-skywater-detail-next-open-multi-project-wafer-shuttle-program/) — news, 2025. SKY130 open MPW: submissions to 2026-01-16, die July 2026 (~6-month fab turn) (via search snippet)

**Capital tier:** T2 | **Time to first revenue:** 30-42 months (design 6-9 mo; two MPW spins at ~6-month turns; characterization; first evaluation license). Foundry IP-catalog listing needs qualification data, which comes later. | **Gross margin estimate:** 80-90% (IP license/royalty)

**US manufacturability:** SkyWater (an IonQ subsidiary since 2026-07-31; says it continues serving all foundry customers): Bloomington MN S130 / 90nm FD-SOI and Fab 25 Austin (65-130nm). GF Fab 8 Malta NY (12LP+). Test chips via ChipFoundry (buyer of Efabless's assets) or the Cadence/SkyWater open MPW. GF's own gain-cell program (RAAAM) is on FDX, which is made in Dresden, not the U.S.

**Who is already doing this:** RAAAM Memory Technologies (Israel/Switzerland): $17.5M Series A led by NXP (2025); GF strategic collaboration with a GCRAM test vehicle taped out on FDX and lead-customer design access in early 2027; moving toward TSMC 2nm qualification; GCRAM reported from 180nm to 5nm (via search snippets). Academic groups at Bar-Ilan/EPFL (RAAAM's lineage) and Georgia Tech (oxide 3T). Incumbent SRAM compilers from Synopsys/Arm. C-01 covers oxide gain cells and C-43 covers cryo gain cells.

**Wins on which axis, for which buyer:** On-chip memory density (bits/mm2) and standby leakage per bit vs 6T SRAM at equal process cost. — for Edge-AI and sensor SoC teams on U.S. trailing nodes; DoD trusted-foundry ASIC programs; FPGA vendors needing denser block RAM.

**Survives a 2029 glut?:** yes — Embedded memory is priced in die area inside someone else's SoC, so it is decoupled from DRAM contract prices.

**Fatal-flaw candidate:** RAAAM already holds the commercial Si gain-cell position, with NXP money, GF and TSMC programs and silicon down to 180nm, and can address SkyWater S130 whenever it chooses. A new entrant starts with no silicon and must clear FTO against RAAAM/Bar-Ilan/EPFL patents. Trailing-node royalty pools are small (MoSys precedent), and 85-125C retention of ~10-100 us forces refresh that erodes the power claim.

*Possible?* yes — silicon-proven in academia and at one startup · *Profitable?* no to marginal: high-margin IP, but a small trailing-node royalty pool contested by a funded incumbent with foundry partnerships · *Doable by this founder?* no: needs a full-time memory-circuit cofounder, ~$2-5M and an FTO opinion before the founder's compiler/web tooling matters

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
  - [OpenRAM SkyWater 130nm test chips (NSF PAR)](https://par.nsf.gov/servlets/purl/10495552) — peer-reviewed, unknown. First sky130 OpenRAM silicon verified a 32-bit 1 KB dual-port SRAM; IO-limited testing (via search snippet)
  - [Caravel lecture slides (Tampere University, spring 2026)](https://plus.tuni.fi/graderA/static/compce250-compce250-spring-2026/lec/survey/5-Caravel.pdf) — other, 2026. Umbralogic Technologies LLC dba ChipFoundry acquired Efabless assets after Efabless shut down (2025); ChipFoundry continues MPW shuttles (Caravel/Caravan/OpenFrame) (via search snippet; secondary)
  - [Cadence and SkyWater Detail Next Open Multi-Project Wafer Shuttle Program](https://www.electronics-lab.com/cadence-and-skywater-detail-next-open-multi-project-wafer-shuttle-program/) — news, 2025. SKY130 open MPW: submissions to 2026-01-16, die July 2026 (~6-month fab turn) (via search snippet)
  - [IonQ Completes Acquisition of SkyWater Technology](https://thequantuminsider.com/2026/07/31/ionq-completes-skywater-acquisition-quantum-manufacturing/) — news, 2026-07-31. SkyWater is now a wholly owned IonQ subsidiary; states it continues serving all foundry customers; MN/FL/TX sites stay active (via search snippet)

**Capital tier:** T0 | **Time to first revenue:** 9-15 months: paid macro generation/support can start before silicon, but silicon-characterized libraries arrive at ~month 12-15 given ~6-month SkyWater MPW turns. One shuttle slot cost ~$9,750 for 10 mm2 in 2021 (chipIgnite); current ChipFoundry pricing is UNVERIFIED. | **Gross margin estimate:** 55-75% (per-tapeout support, contract layout/characterization labor and shuttle slots are COGS; SaaS share small early)

**US manufacturability:** Customer silicon is made at SkyWater Bloomington MN (S130; SkyWater has been an IonQ subsidiary since 2026-07-31 and says it keeps serving foundry customers) via ChipFoundry MPW or the Cadence/SkyWater open MPW (2026: Jan submission, July die). The venture itself is U.S. software/services.

**Who is already doing this:** VLSIDA/UC Santa Cruz (OpenRAM, free; first sky130 silicon verified a 1 KB dual-port macro); ChipFoundry (Umbralogic Technologies dba ChipFoundry, which bought Efabless's assets in 2025 and runs Caravel/Caravan/OpenFrame MPWs plus a marketplace); Cadence + SkyWater open SKY130 MPW (2026 run), where an EDA vendor could bundle memory; Synopsys/Arm commercial compilers; standard-cell RAM generators such as DFFRAM [UNVERIFIED-training].

**Wins on which axis, for which buyer:** Supply security and access: time and cost to get characterized on-chip RAM in a U.S.-fabbed ASIC. Not $/GB. — for University VLSI labs, DoD SBIR/STTR ASIC teams needing U.S.-only fabrication, hardware startups on ChipFoundry/SkyWater shuttles.

**Survives a 2029 glut?:** yes — Demand tracks ASIC tapeout activity and U.S.-fab policy, not DRAM prices.

**Fatal-flaw candidate:** Tiny market (hundreds of MPW projects/yr) with low willingness to pay for BSD-licensed macros. The funnel is fragile: Efabless already failed financially in 2025, and SkyWater's new owner is a quantum company. ChipFoundry, Cadence/SkyWater or UCSC could bundle larger macros for free. It is on-chip memory IP, not 'RAM' in the mission's main sense.

*Possible?* yes — compiler and PDK exist; needs larger, better-characterized macros · *Profitable?* marginal to no: likely <$0.5-1M ARR ceiling unless it becomes a broader open-PDK IP/characterization house (gf180mcu, IHP, gain-cell IP) · *Doable by this founder?* yes — T0, software-led, starts alongside the day job

*Business-model lenses:* SaaS; IP licensing (support/indemnity on open IP); fabless->foundry (MPW); defense-first (U.S.-only fab flows)

### C-34 — Depreciated-fab revival of IBM-heritage deep-trench eDRAM — ☠ KILLED (R4-NO-WINNING-AXIS: Even at depreciated cash-cost wafers the card computes ~$20/GB standalone (~$50/GB at a normal wafer price). That compares with the $15.99 contract, the $6.40 glut and the $1.64 incumbent cost, because density is 0.026 vs 0.436 Gb/mm2 (17x). Its one axis, a ~2 ns macro cycle, disappears behind a DDR interface for the standalone die (the C-35 logic). The LLC-chiplet buyer is self-labeled 'hypothetical', and SRAM chiplets and 3D-stacked SRAM already serve it. There is also no host: IBM moved POWER10/z16 to Samsung 7nm without eDRAM, East Fishkill is an onsemi fab, and GF no longer offers 14HP [UNVERIFIED-training], so a restart is a T3 process rebuild with the tool set and know-how dispersed.)

*Sub-branch:* 1T1C eDRAM at foundries; depreciated trailing-edge capacity · *Materials sense:* c-capital

**What it is:** Restart IBM-heritage 1T1C deep-trench eDRAM (32SOI/14HP class) on a depreciated U.S. 300mm line: onsemi East Fishkill NY (the former IBM/GF Fab 10) or GF Fab 8 Malta. Sell standalone 'fast DRAM' dies or LLC chiplets to U.S. HPC/ASIC buyers.

**Why it could work:** The 0.0174 um2 14HP cell (IBM, IEDM 2014) is the densest logic-compatible DRAM ever shipped. It was used in POWER8/9 and z15. A fully depreciated line might sell wafers near cash cost (~$2.5k), which computes to ~$20/GB standalone including test (C-34), below today's ~$27/GB DDR5 spot.

**Evidence:** TRL 5 · Rule 1: SUPPORTED
  - [DRAM value-per-area chart (Kurnal Insights)](https://www.kitguru.net/channel/generaltech/joao-silva/new-dram-value%E2%80%91per%E2%80%91area-chart-draws-attention-amid-rising-memory-prices/) — news, 2026-09. 1b DRAM bit density ~0.436 Gb/mm2, the reference against which A3 densities are compared (CROSS-REFERENCE: seen in another agent's search results, not opened by A3)
  - [DRAM vs N2 wafer value comparison](https://xenospectrum.com/dram-n2-wafer-price-comparison/) — news, 2026-09. Kurnal: 1b DRAM sales value per mm2 ~54% above TSMC N2 — logic-process memory cannot match DRAM bits per wafer dollar (CROSS-REFERENCE: seen in another agent's search results, not opened by A3)
  - [IBM 14nm SOI FinFET with 0.0174 um2 eDRAM (IEDM 2014); Intel 22nm eDRAM 0.029 um2 (VLSI 2013, Crystalwell 128MB); IBM POWER10/z16 moved to Samsung 7nm without eDRAM; GF sold East Fishkill to onsemi (2019-2022)]() — conference, 2013-2022. [UNVERIFIED-training] citation from A3 training data (<= mid-2026). No URL could be opened or seen this session: the shared WebSearch budget was exhausted and web hosts returned proxy 403. Verify agent: add a URL or downgrade. Shows deep-trench eDRAM shipped in volume (TRL 9) and then was retired.

**Capital tier:** T3 | **Time to first revenue:** 48-60 months (re-establish DT module, requalify) | **Gross margin estimate:** negative vs glut

**US manufacturability:** No U.S. line runs deep-trench eDRAM (East Fishkill is onsemi's; GF 14HP not offered [UNVERIFIED-training]). Would require a T3 module rebuild.

**Who is already doing this:** Nobody. IBM exited eDRAM with POWER10/z16. Intel ended Crystalwell-class eDRAM. GF no longer offers 14HP [UNVERIFIED-training].

**Wins on which axis, for which buyer:** None for a real buyer. Latency is lost behind DDR I/O, and the LLC-chiplet buyer is hypothetical and served by SRAM/3D-SRAM. — for HPC/ASIC teams wanting a fast on-package cache tier (hypothetical).

**Survives a 2029 glut?:** no — ~$20/GB at cash-cost wafers and ~$50/GB at normal wafer prices vs canonical glut $6.40/GB (3-8x), 4Q26 contract $15.99/GB and incumbent cost $1.64/GB (12-30x).

**Fatal-flaw candidate:** Depreciation cannot close a 17x density gap: wafer cost is a minor term once density is 0.026 vs 0.436 Gb/mm2. The tool set and know-how are likely gone [UNVERIFIED-training].

*Possible?* marginal — it shipped before, but the process is retired · *Profitable?* no — density gap dominates even at cash-cost wafers · *Doable by this founder?* no

*Business-model lenses:* c-capital arbitrage of a depreciated fab; fabless->foundry — both fail

### C-35 — Trailing-node bulk SRAM as a DRAM substitute (SRAM-DIMM/CXL) — ☠ KILLED (R4-NO-WINNING-AXIS: The card itself names no winning axis and no buyer. SRAM silicon is ~$55-72/GB at 7-28nm (01_LANDSCAPE s4.4), or ~$80-120/GB with test per A3. That is 3.5-7.5x the $15.99/GB contract, 9-19x the $6.40 glut and 35-70x the $1.64 incumbent cost. Refresh-free operation and latency are lost behind a DDR4/CXL controller (~50-100 ns). A 1 Gb SRAM die needs ~181 mm2 at 28nm, and the only U.S. option (GF Malta 12/14nm) does not change the cost floor.)

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

**Survives a 2029 glut?:** no — COGS ~$60-120/GB (7-40nm) vs 4Q26 contract $15.99/GB, glut $6.40/GB and incumbent cost $1.64/GB.

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
  - [SkyWater Completes Acquisition of Fab 25](https://www.businesswire.com/news/home/20250630358336/en/SkyWater-Completes-Acquisition-of-Fab-25-Expanding-U.S.-Pure-Play-Foundry-Capacity-for-Critical-Semiconductor-Technologies) — company-IR, 2025-06-30. Fab 25: ~400k wafer starts/yr, 65-130nm, ~1,000 staff; memory listed among target markets (via search snippet)
  - [IonQ Completes Acquisition of SkyWater Technology](https://thequantuminsider.com/2026/07/31/ionq-completes-skywater-acquisition-quantum-manufacturing/) — news, 2026-07-31. SkyWater is now a wholly owned IonQ subsidiary; states it continues serving all foundry customers; MN/FL/TX sites stay active (via search snippet)
  - [Renesas SRAM EOL 2026](https://globx.eu/blog/component-lifecycle/renesas-sram-eol-2026) — blog, 2026-06. Renesas EOL260016 (2026-06-01) discontinues 92 async SRAM codes, mapping some to Infineon codes (via search snippet; notice not opened)
  - [Infineon SRAM (Static RAM) product page](https://infineon.com/cms/en/product/memories/sram-static-ram) — company-IR, 2026. Infineon still markets async SRAM 256K-64M and QDR SRAM; no 2025-26 Infineon SRAM EOL found (via search snippet)

**Capital tier:** T2 | **Time to first revenue:** 30-42 months to first production revenue (industrial grade first; defense/QML later) | **Gross margin estimate:** 45-60%

**US manufacturability:** SkyWater Fab 25 Austin TX (200mm, 65-130nm, ~400k wafer starts/yr; SkyWater has been an IonQ subsidiary since 2026-07-31 and says it keeps serving all foundry customers) and SkyWater Bloomington MN. STILL-UNVERIFIED: whether Fab 25 offers outside customers a characterized high-density 6T SRAM bitcell and 65nm PDK, since the SRAM flows were Cypress/Infineon-proprietary. The rad-tolerant 90nm FD-SOI option is DoD-program-linked [UNVERIFIED].

**Who is already doing this:** Infineon (ex-Cypress; still markets async SRAM 256K-64M and QDR; U.S. wafers via SkyWater Fab 25), Renesas (EOL260016, 2026-06-01, discontinued 92 async SRAM codes with mappings to Infineon parts), ISSI (Ingenic-owned), GSI Technology (TSMC-fabbed), Alliance Memory, Rochester Electronics (licensed EOL continuation). Rad-hard: Honeywell, BAE Systems, Frontgrade [UNVERIFIED-training for current status].

**Wins on which axis, for which buyer:** Lifecycle length (written 15-20-year commitments beyond Infineon's) and non-PRC ownership vs ISSI. 'U.S.-fab' alone is not unique, because Infineon is supplied from the same fab. Not $/GB. — for Defense primes (avionics, radar, EW), DMSMS/obsolescence programs, industrial controls, networking line cards using QDR SRAM.

**Survives a 2029 glut?:** yes — SRAM ASPs are decoupled from DRAM contract prices; long-lifecycle buyers pay for availability through cycles.

**Fatal-flaw candidate:** Infineon is the incumbent and the anchor customer of the same fab, and Renesas EOLs funnel customers to Infineon's existing parts. The standalone SRAM market is small and shrinking. Revenue needs 2-3 years of design and qualification, and SkyWater's new quantum-company parent adds capacity-priority risk.

*Possible?* yes — mature technology at a willing U.S. foundry · *Profitable?* marginal — real margins per part, but a small market with a strong incumbent at the same fab · *Doable by this founder?* no — T2 hardware team required

*Business-model lenses:* fabless->foundry; defense-first; module/component maker

### C-37 — Compute-in-SRAM vector-search appliance on GSI Gemini APU

*Sub-branch:* SRAM-at-scale: compute-in-SRAM as a DRAM-bandwidth substitute · *Materials sense:* none

**What it is:** An on-prem retrieval and vector-search appliance plus software (FAISS/Milvus-compatible API, index build pipeline, monitoring) built on GSI Technology's Gemini APU PCIe cards. The APU does associative processing inside SRAM bit-lines (Gemini-I on TSMC 28nm, Gemini-II on 16nm) [UNVERIFIED-training]. It is sold to air-gapped defense/IC RAG and SIEM buyers as hardware plus an annual software subscription.

**Why it could work:** GSI revenue is ~$6.1-6.3M per quarter (~$25M/yr) in FY2026-27 with rising losses, not '~$20M'. The 2025 Cornell study is MICRO '25 (GSI co-author).

**Evidence:** TRL 7 · Rule 1: SUPPORTED
  - [D-Matrix AI chip promises efficient transformer processing](https://www.forbes.com/sites/karlfreund/2022/06/21/d-matrix-ai-chip-promises-efficient-transformer-processing/) — news, 2022-06. URL + excerpt seen in basicmi/AI-Chip README (not opened): digital in-memory (SRAM) compute + chiplets for datacenter inference
  - [Startup Runs AI in Novel SRAM](https://www.eetimes.com/document.asp?doc_id=1334947) — news, 2019. URL + excerpt seen in basicmi/AI-Chip README (not opened): another compute-in-SRAM startup (Areanna AI)
  - [GSI Technology Gemini APU (Sunnyvale CA; FY2025 revenue ~$20M; Cornell/MICRO-2025 energy-efficiency study of APU retrieval)]() — company, 2025. [UNVERIFIED-training] citation from A3 training data (<= mid-2026). No URL could be opened or seen this session: the shared WebSearch budget was exhausted and web hosts returned proxy 403. Verify agent: add a URL or downgrade. Status as of 2026-11-01 not verified.
  - [Characterizing and Optimizing Realistic Workloads on a Commercial Compute-in-SRAM Device (MICRO '25)](https://www.csl.cornell.edu/~zhiruz/pdfs/apu-micro2025.pdf) — conference, 2025-10. (via search snippet) Cornell-led team measured GSI Gemini-I APU on RAG retrieval over 10-200 GB corpora: throughput comparable to an NVIDIA A6000 at 54.4-117.9x lower energy; retrieval 4.8-6.6x faster than an optimized CPU baseline. One co-author is a GSI employee (not independent).
  - [Compute-In-Memory APU Achieves GPU-Class AI Performance at a Fraction of the Energy Cost (GSI press release)](https://ir.gsitechnology.com/news-releases/news-release-details/compute-memory-apu-achieves-gpu-class-ai-performance-fraction) — company-IR, 2025-10-20. (via search snippet) GSI announcement of the Cornell MICRO '25 result; claims >98% less energy than a GPU on RAG at comparable throughput
  - [GSI Technology Form 8-K Ex. 99.1 earnings release (2026 filing)](https://www.sec.gov/Archives/edgar/data/0001126741/000117184326005079/exh_991.htm) — primary-filing, 2026. (via search snippet; filing-to-quarter mapping inferred) Q1 FY2027 (quarter to Jun-2026) net revenue $6.3M vs $6.3M a year earlier; GM 53.4% (58.1%); opex $8.8M (5.8M); operating loss $5.4M; Q2 FY2027 guide $5.7-6.5M
  - [GSI Technology Inc Announces Third Quarter Fiscal 2026 Results](https://www.globenewswire.com/news-release/2026/01/29/3229090/0/en/GSI-Technology-Inc-Announces-Third-Quarter-Fiscal-2026-Results.html) — company-IR, 2026-01-29. (via search snippet) Q3 FY2026 revenue $6.1M (+12% YoY), net loss $3.0M; SRAM business funds APU development
  - [GSI Technology Q4 earnings call: key points](https://finance.yahoo.com/markets/stocks/articles/gsi-technology-q4-earnings-call-021329121.html) — news, 2026-05. (via search snippet) Q4 FY2026 revenue $6.3M at 52.4% GM; opex mostly Plato APU R&D; Plato tape-out targeted early 2027; Gemini-II pursuing initial defense design wins
  - [OpenSearch partner page: GSI Technology](https://www.opensearch.org/partners/gsi-technology.html) — other, 2021-2026. (via search snippet) GSI offers an OpenSearch neural/k-NN search plugin on the Gemini APU (since the OpenSearch 1.0 launch, 2021). The vendor already sells the software layer C-37 proposes to build.
  - [GSI Technology Announces Production Release of Two Gemini-I APU Servers](https://ir.gsitechnology.com/news-releases/news-release-details/gsi-technology-announces-production-release-two-gemini-ir-apu) — company-IR, unknown. (via search snippet; date not shown) GSI sells complete Gemini-I APU servers itself, i.e. it already offers the appliance form factor

**Capital tier:** T1 | **Time to first revenue:** 18-24 months (eval units early; first paid defense/enterprise pilot needs a sponsor and an ATO) | **Gross margin estimate:** 20-40% blended (APU card/server resale at ~10-20% VAR margin; subscription small in years 1-2)

**US manufacturability:** APU silicon is TSMC (Taiwan) and boards are GSI-sourced. Integration and software are in the U.S., so the product is U.S.-assembled, not U.S.-made.

**Who is already doing this:** GSI Technology itself: production Gemini-I APU servers plus an OpenSearch neural/k-NN plugin (OpenSearch partner since 2021). Its 2026 APU focus is Gemini-II defense-edge design wins and Plato (tape-out early 2027). Also GPU/CPU vector search (NVIDIA cuVS/CAGRA, quantized CPU search in Milvus/Zilliz, Qdrant, Weaviate, Pinecone), d-Matrix (LLM), Areanna (historical).

**Wins on which axis, for which buyer:** Energy per retrieval query at matched throughput (54-118x below an NVIDIA A6000 on RAG retrieval, MICRO '25, GSI-coauthored). NOT DRAM GB per QPS. — for Air-gapped defense/intelligence RAG deployments; on-prem enterprise search with power or DRAM constraints.

**Survives a 2029 glut?:** partially — The DRAM-savings pitch was never the real win (the index stays in DRAM) and vanishes at the $6.40/GB glut. The energy and air-gap pitch does not depend on DRAM price. Vendor-survival risk rises if GSI's SRAM base weakens in a downturn.

**Fatal-flaw candidate:** Single-source dependence on a ~$25M/yr vendor losing ~$5M+ per quarter (Q1 FY2027 operating loss $5.4M) and spending on Plato. The vendor already sells the same servers and plugin direct, so the reseller adds a thin layer. The energy win is GSI-coauthored, and GPU/CPU quantized search improves yearly. In RAG, retrieval energy is a small share next to LLM inference on GPUs.

*Possible?* yes — the APU ships · *Profitable?* marginal-to-no — thin VAR margin on a vendor that sells the same product direct · *Doable by this founder?* marginal — software-led but needs a hardware partner that stays alive

*Business-model lenses:* module/appliance maker (VAR); SaaS (software subscription); defense-first

### C-38 — Memory-only wafer-scale SRAM ('Cerebras for RAM') — ☠ KILLED (R4-NO-WINNING-AXIS: The card itself names no winning axis and no buyer. A 28nm memory-only wafer holds ~27 GB at ~$111/GB in silicon and ~$1,000/GB packaged. That is ~63x the $15.99/GB 4Q26 DDR5 contract price and ~156x the $6.40/GB glut. On-wafer bandwidth must leave through an ~860 mm perimeter of SerDes/CXL, so the host sees CXL-class latency and bandwidth: no latency, bandwidth or density gain. It even holds less SRAM than Cerebras WSE-3 (44 GB, with compute on the same wafer). Wafer-scale yield via redundancy is real (Cerebras), but that is not the issue.)

*Sub-branch:* Wafer-scale SRAM as a RAM product · *Materials sense:* c-capital

**What it is:** A whole 300mm 28nm wafer of redundant, stitched SRAM (~27 GB) packaged with power delivery and cooling as an ultra-low-latency memory appliance, attached to hosts through edge SerDes/CXL links. Wafers would come from a 28nm-class foundry (GF Malta 12/14nm is the U.S. option).

**Why it could work:** Cerebras proved wafer-scale yield through redundancy (WSE-2 '100% yield' on 7nm; WSE-3 holds 44 GB SRAM on 46,225 mm2 [UNVERIFIED-training]). 28nm wafers are cheap, and on-wafer bandwidth is enormous.

**Evidence:** TRL 4 · Rule 1: SUPPORTED
  - [Cerebras Unveils Wafer Scale Engine Two (WSE2): 2.6 Trillion Transistors, 100% Yield](https://www.anandtech.com/show/16626/cerebras-unveils-wafer-scale-engine-two-wse2-26-trillion-transistors-100-yield) — news, 2021-04. URL + excerpt seen in basicmi/AI-Chip README (not opened): wafer-scale engine on TSMC 7nm (WSE1 on 16nm); redundancy gives '100% yield'
  - [Cerebras Unveils Andromeda, a 13.5 Million Core AI Supercomputer](https://www.cerebras.net/press-release/cerebras-unveils-andromeda-a-13.5-million-core-ai-supercomputer-that-delivers-near-perfect-linear-scaling-for-large-language-models) — company, 2022-11. URL seen in basicmi/AI-Chip README (not opened): wafer-scale systems clustered for LLM work
  - [The Cerebras CS-1 computes deep learning AI problems by being bigger](https://techcrunch.com/2019/11/19/the-cerebras-cs-1-computes-deep-learning-ai-problems-by-being-bigger-bigger-and-bigger-than-any-other-chip/) — news, 2019-11. URL + excerpt seen in basicmi/AI-Chip README (not opened): CS-1 launch; first customer Argonne National Laboratory

**Capital tier:** T3 | **Time to first revenue:** ~48 months | **Gross margin estimate:** negative

**US manufacturability:** No U.S. 28nm host. GF Malta offers 12/14nm FinFET (higher wafer cost). U.S. wafer-scale packaging is unproven [UNVERIFIED].

**Who is already doing this:** Cerebras (compute + SRAM on one wafer, TSMC). Nobody sells memory-only wafers.

**Wins on which axis, for which buyer:** None for a host: on-wafer bandwidth cannot leave the wafer through an ~860 mm perimeter. — for None identified. Latency-critical buyers buy Cerebras/Groq compute instead.

**Survives a 2029 glut?:** no — ~$1,000/GB packaged vs $6.40/GB glut DDR5 (~156x) and $1.60/GB severe; dies in any market.

**Fatal-flaw candidate:** Cerebras's economics come from co-locating compute with SRAM. A memory-only wafer exports its bandwidth through edge I/O, so it is DRAM at 40-100x the price with no latency advantage visible to the host.

*Possible?* yes — engineering-feasible · *Profitable?* no · *Doable by this founder?* no

*Business-model lenses:* module/appliance maker — fails

### C-39 — U.S.-fabbed SRAM-only LLM inference accelerator (Groq pattern) — ☠ KILLED (SCORE<55: Scored 45.0/100 default (rank 38/40), 44.2 moonshot. Weakest: capital 1/5 (The minimum path is ~$150-400M to first rack revenue (T3; Groq raised ~$300M by 2021, d-Matrix $110M+ in 2023).); time to revenue 1/5 (48-60 months: ~24-30 months to first silicon, then the compiler and rack integration; Groq took 4+ years to meaningful revenue.); competition 1/5 (Groq, NVIDIA (Groq license plus its founder), Cerebras, d-Matrix, SambaNova, Etched, MatX and Positron are all well funded and doing exactly). Scorer verdicts — founder: A $150-400M chip company against Groq, NVIDIA and Cerebras: impossible for this founder, and a poor bet for anyone entering on 12nm. | vc: Upper-T3 chip program against Groq, NVIDIA-with-Groq-IP and Cerebras with a 2-3x SRAM-density handicap on 12LP+: the textbook way to burn $300M; hard pass. | veteran: A $150-400M chip program entering a market where NVIDIA just licensed the leader's architecture, on a node 2-3x behind on SRAM density; dead for this founder.)

*Sub-branch:* SRAM-instead-of-DRAM for inference · *Materials sense:* c-capital

**What it is:** A fabless startup building a deterministic SRAM-only LLM-decode accelerator (the Groq LPU pattern) on GlobalFoundries 12LP+ at Fab 8 Malta, NY. It would be sold as U.S.-made inference racks or cloud tokens, replacing HBM/DRAM with on-chip SRAM for low-latency decode.

**Why it could work:** NVIDIA-Groq licensing deal is verified (Dec-2025, ~$20B reported, non-exclusive). 'Groq v1 at GF 14nm Malta' remains [UNVERIFIED-training]; a search for it returned nothing.

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [Groq Demonstrates Fast LLMs on 4-Year-Old Silicon](https://www.eetimes.com/groq-demos-fast-llms-on-4-year-old-silicon/) — news, 2023-09. URL + excerpt seen in basicmi/AI-Chip README (not opened): first-gen SRAM-only LPU ran Llama-2 70B at 240 tokens/s/user
  - [AI Chip Startup Groq Raises $300 Million](https://www.forbes.com/sites/amyfeldman/2021/04/14/ai-chip-startup-groq-founded-by-ex-googlers-raises-300-million-to-power-autonomous-vehicles-and-data-centers/) — news, 2021-04. URL + excerpt seen in basicmi/AI-Chip README (not opened): Groq raised $300M in 2021 (T3 capital intensity)
  - [D-Matrix AI chip promises efficient transformer processing](https://www.forbes.com/sites/karlfreund/2022/06/21/d-matrix-ai-chip-promises-efficient-transformer-processing/) — news, 2022-06. URL + excerpt seen in basicmi/AI-Chip README (not opened): digital in-memory (SRAM) compute + chiplets for datacenter inference
  - [AI chip startup d-Matrix raises $110 million with backing from Microsoft](https://www.reuters.com/technology/ai-chip-startup-d-matrix-raises-110-mln-with-backing-microsoft-2023-09-06/) — news, 2023-09. URL + excerpt seen in basicmi/AI-Chip README (not opened): $110M raise incl. Microsoft
  - [Graphcore Supercharges IPU with Wafer-on-Wafer](https://www.eetimes.com/graphcore-supercharges-ipu-with-wafer-on-wafer/) — news, 2022-03. URL + excerpt seen in basicmi/AI-Chip README (not opened): SRAM-heavy IPU (no HBM) using 3D wafer-on-wafer
  - [Untether AI nabs $125M for AI acceleration chips](https://venturebeat.com/2021/07/20/untether-ai-nabs-125m-for-ai-acceleration-chips/) — news, 2021-07. URL + excerpt seen in basicmi/AI-Chip README (not opened): at-memory (SRAM) inference startup raised $125M
  - [Nvidia's Groq deal: Acquisition, acquihire or creative licensing deal?](https://www.constellationr.com/insights/news/nvidias-groq-deal-acquisition-acquihire-or-creative-licensing-deal) — news, 2025-12. (via search snippet) Groq announced a non-exclusive license of its inference technology to NVIDIA; founder Jonathan Ross, president Sunny Madra and team join NVIDIA; Groq stays independent under CEO Simon Edwards, GroqCloud continues; ~$20B per CNBC reporting
  - [Nvidia closes licensing agreement with Groq for 20 billion dollars](https://itdaily.com/news/security/nvidia-closes-licensing-agreement-with-groq) — news, 2025-12. (via search snippet) ~$20B NVIDIA-Groq licensing deal, announced ~2025-12-24

**Capital tier:** T3 | **Time to first revenue:** 48-60 months | **Gross margin estimate:** 20-50% even for a winner (hundreds of SRAM dies per model; token pricing set by GPU clouds)

**US manufacturability:** GF Fab 8 Malta NY (12LP+/14nm; takes outside customers, Trusted) plus U.S. OSAT. 'U.S.-fabbed' is not unique: Groq's next gen was announced for Samsung Taylor TX 4nm [UNVERIFIED-training]. GF 12LP+ costs ~2-3x SRAM density vs 4-5nm rivals [ESTIMATE].

**Who is already doing this:** Groq (independent under CEO Simon Edwards; GroqCloud), NVIDIA (non-exclusive license to Groq inference tech plus the Groq founder/president, ~2025-12-24, ~$20B reported), Cerebras, d-Matrix, SambaNova, Etched, MatX, Positron; attrition: Graphcore (SoftBank), Untether AI.

**Wins on which axis, for which buyer:** Tokens/s/user (decode latency) and energy per bit moved (no off-chip DRAM I/O). — for Latency-sensitive inference (agents, voice, real-time trading) and sovereign/U.S.-made AI clouds.

**Survives a 2029 glut?:** partially — The latency premium persists for agents and voice, but in a glut ($6.40/GB DDR5, cheaper HBM) SRAM at ~$375/GB chip-level is ~30x+ HBM-class price, so the 'no DRAM needed' cost story inverts.

**Fatal-flaw candidate:** Upper-T3 capital against 5+ funded incumbents, with NVIDIA now licensing Groq's architecture and hiring its leaders. A 70B 8-bit model needs ~300+ SRAM dies, and a 12nm U.S. entrant starts 2-3x behind on SRAM density.

*Possible?* yes — shipping at incumbents · *Profitable?* no for a new entrant — marginal only for the category winner · *Doable by this founder?* no

*Business-model lenses:* fabless->foundry; appliance; cloud service

### C-40 — Nantero NRAM (carbon-nanotube) license and U.S. second source — ☠ KILLED (R4-NO-WINNING-AXIS: For the card's own buyer (space primes buying rad-hard NVM), a 1T1R NRAM in SkyWater S130 wins no axis. The cell's claimed high-temperature and radiation tolerance is hidden behind the bulk-CMOS access transistor and periphery (~125-150 C, not rad-hard-by-process). On density, speed and endurance it at best ties qualified Toggle MRAM, rad-hard F-RAM and Weebit 1T1R ReRAM, which is already qualified in the same S130 process (C-22), while being ~48 months and a T2 qualification program behind. The licensor looks dormant. Two searches found no Nantero product, license or funding news after the 2016 Fujitsu/Mie Fujitsu deal, whose end-2018 product never appeared. The 'DDR-class' pitch is ~$31/GB even at a hypothetical 28nm (no U.S. host), vs $6.40/GB glut DDR5.)

*Sub-branch:* Exotic: carbon-nanotube memory · *Materials sense:* mixed:a+b

**What it is:** License Nantero's (Woburn, MA) carbon-nanotube NRAM 1T1R BEOL module and run it at SkyWater Bloomington MN (200mm, already hosting third-party BEOL memory). The first product would be rad-hard, high-temperature non-volatile RAM for space and defense; the long-term pitch is DDR-class persistent memory.

**Why it could work:** The CNT fabric is spin-coated at room temperature, which is CMOS-compatible and uses cheap tooling (materials sense a+b). Nantero claims ns switching, high endurance, multi-year retention at high temperature and radiation tolerance [UNVERIFIED-training]. A hypothetical 1T1R at 28nm computes to ~$31/GB (C-40), cheap for rad-hard NVM.

**Evidence:** TRL 4 · Rule 1: SUPPORTED
  - [Weebit Nano ReRAM IP achieves high-temperature qualification in SkyWater S130](https://www.skywatertechnology.com/weebit-nano-reram-ip-achieves-high-temperature-qualification-in-skywater-s130-process/) — company, 2023-11. SkyWater's S130 PDK hosts third-party memory IP — precedent for licensing a memory macro into a U.S. 130nm foundry (CROSS-REFERENCE: seen in another agent's search results, not opened by A3)
  - [Frontgrade case study: Everspin Toggle MRAM for space](https://www.frontgrade.com/news/new-case-study-touts-everspins-toggle-mram-highly-reliable-memory-technology-space) — company, 2020. Qualified hi-rel/space memory reaches primes through channels like Frontgrade — the buyer channel for U.S.-made long-lifecycle memory (CROSS-REFERENCE: seen in another agent's search results, not opened by A3)
  - [Nantero NRAM: Fujitsu Semiconductor + Mie Fujitsu licenses (2016, 55nm target product ~2018-19, not known to have shipped); Nantero IEDM/company disclosures]() — company, 2016-2020. [UNVERIFIED-training] citation from A3 training data (<= mid-2026). No URL could be opened or seen this session: the shared WebSearch budget was exhausted and web hosts returned proxy 403. Verify agent: add a URL or downgrade. Status of Nantero in 2026 unknown.
  - [Nantero exits stealth: carbon nanotubes for non-volatile memory with DRAM performance, unlimited endurance (AnandTech)](https://at-web1.www.anandtech.com/show/9314/nantero-exits-stealth-using-carbon-nanotubes-for-nonvolatile-memory-with-dram-performance-unlimited-endurance) — news, 2015-06. (via search snippet) Nantero's NRAM claims and licensing-only model; the mechanism is shown only at company/industry-claim level
  - [Fujitsu Semiconductor and Mie Fujitsu Semiconductor license Nantero NRAM](https://us.design-reuse.com/news/40435/fujitsu-nantero-nram.html) — news, 2016-08. (via search snippet) 2016 license; Fujitsu planned an NRAM-embedded custom LSI product by end-2018 (no shipment found)
  - [Nantero takes funding above $110 million (eeNews Europe)](https://www.eenewseurope.com/en/nantero-takes-funding-above-110-million/) — news, unknown. (via search snippet; undated in results) cumulative funding >$110M
  - [Nantero timeline (IDTechEx)](https://www.idtechex.com/en/timeline/nantero/c36003) — market-research, unknown. (via search snippet) profile still describes NRAM development; two 2026-11-01 searches found NO Nantero license, product, funding or shutdown news dated 2024-2026

**Capital tier:** T2 | **Time to first revenue:** ~48 months (module transfer, rad testing, QML-style qualification) | **Gross margin estimate:** 40-60% in a rad-hard niche if it worked

**US manufacturability:** SkyWater Bloomington MN (S130 BEOL) or Fab 25 Austin. The licensor is in Massachusetts (East Coast).

**Who is already doing this:** Nantero (no public license, product or funding news found for 2024-2026; STILL-UNVERIFIED whether operating). Fujitsu/Mie Fujitsu licensees (2016; no product). Same-fab competitor: Weebit ReRAM qualified in SkyWater S130 (C-22). Rad-hard incumbents: Everspin Toggle MRAM via Frontgrade, Infineon rad-hard F-RAM, Honeywell/BAE.

**Wins on which axis, for which buyer:** None verified. Claimed CNT temperature and radiation tolerance cannot be exploited in a bulk-CMOS 1T1R; density and endurance tie Toggle MRAM/ReRAM at 130nm. — for Space primes and rad-hard component distributors (Frontgrade-type channel); downhole/high-temperature industrial.

**Survives a 2029 glut?:** partially — The rad-hard niche is independent of DRAM prices, but the 'DRAM replacement' story dies at $10/GB DDR5.

**Fatal-flaw candidate:** 20+ years and >$100M [UNVERIFIED-training] without a known volume product; the Fujitsu-licensed product apparently never shipped. In rad-hard it must displace qualified Toggle MRAM and F-RAM incumbents.

*Possible?* marginal — demonstrated by licensees, never productized · *Profitable?* no — no evidence of a cost or performance win that incumbents can't match · *Doable by this founder?* no

*Business-model lenses:* university/lab-style patent license (from Nantero); defense-first; fabless->foundry

### C-41 — 2D-material (MoS2/WSe2) gain-cell DRAM or 2D flash — ☠ KILLED (QB-INCOMPLETE: The card names no buyer ('None until TRL 6+') and no production partner. Penn State 2DCC and NY CREATES are research venues, and neither gap can be closed within the >96-month horizon. The card also misreads its evidence. Fudan's 400 ps PoX (Nature 641:90-97, 2025) is a graphene-channel flash, not MoS2/WSe2. Its Oct-2025 2D-flash+CMOS chip is a small demonstrator (94.3% cell yield) with MB scale targeted in 3-5 years, at a Chinese university. Mechanism evidence exists at device and small-array scale (TRL 3-4), so R1 is not the reason. The reason is no buyer, no U.S. fab and no shown axis over IGZO 2T0C (R4 also applies).)

*Sub-branch:* Exotic: 2D semiconductor memory · *Materials sense:* a-material

**What it is:** BEOL 2T0C gain cells or 2D-channel flash built from wafer-scale MoS2/WSe2, under a university license (Penn State 2D Crystal Consortium, MIT, or the Fudan 'PoX' line of work). Pilot fabrication would be at the Penn State 2DCC user facility or NY CREATES Albany 300mm.

**Why it could work:** Atomically thin, wide-gap channels give ultra-low off-current (long retention, like IGZO) with higher mobility than IGZO. Lab papers report sub-ns 2D flash programming (Fudan PoX, ~400 ps, Nature 2025) and 2D logic circuits of a few thousand transistors [UNVERIFIED-training].

**Evidence:** TRL 3 · Rule 1: SUPPORTED at device/small-array scale; UNSUPPORTED at product scale
  - [NY CREATES + Fraunhofer IPMS JDA on memory devices at 300mm (Albany NY)](https://nachrichten.idw-online.de/2025/05/16/ny-creates-and-fraunhofer-ipms-announce-joint-development-agreement-to-advance-memory-devices-at-300mm-wafer-scale) — news, 2025-05. Venue evidence only: Albany NY 300mm hosts external memory-device JDAs (HfO2 FE), a possible pilot site; does NOT show 2D-memory mechanism (CROSS-REFERENCE: seen in another agent's search results, not opened by A3)
  - [2D-material memory literature: Fudan quasi-non-volatile 2D memory (Nature Nanotech 2018), Fudan PoX 400-ps 2D flash (Nature 2025), Penn State 2D CMOS computer (Nature 2025)]() — peer-reviewed, 2018-2025. [UNVERIFIED-training] citation from A3 training data (<= mid-2026). No URL could be opened or seen this session: the shared WebSearch budget was exhausted and web hosts returned proxy 403. Verify agent: add a URL or downgrade. No array-scale (>1 Mb) 2D memory known to A3.
  - [World's fastest flash memory, writable in 400 picoseconds (Gigazine, on Fudan Nature 641:90-97, 2025)](https://gigazine.net/gsc_news/en/20250422-fastest-flash-memory) — news, 2025-04-22. (via search snippet) Fudan 'PoX' 400 ps 2D flash is a Dirac GRAPHENE-channel device (Nature 641, 90-97, 2025), not MoS2/WSe2
  - [Breakthrough in 2D flash chip achieved (Fudan University news)](https://shuangyiliu.fudan.edu.cn/syl/a4/66/c29574a762982/page.htm) — other, 2025-10. (via search snippet) 2D flash integrated with Si CMOS, taped out; 8-bit instruction ops, 32-bit parallel ops, random access; 94.3% cell yield; small-scale chip (Nature s41586-025-09621-8); MB-level system targeted in 3-5 years; pilot line planned
  - [Fudan University 2D flash chip breakthrough (Interesting Engineering)](https://interestingengineering.com/energy/fudan-university-2d-flash-chip-breakthrough) — news, 2025-10. (via search snippet) coverage of the Oct-2025 Fudan 2D-flash/CMOS chip

**Capital tier:** T3 | **Time to first revenue:** >8 years | **Gross margin estimate:** not modelable

**US manufacturability:** No U.S. production line; research only (Penn State 2DCC, NY CREATES Albany).

**Who is already doing this:** Academic groups (Fudan, Penn State, MIT, Stanford); TSMC/imec/Intel 2D-channel logic research [UNVERIFIED-training].

**Wins on which axis, for which buyer:** Retention per area (speculative) — not demonstrated at array scale. — for None until TRL 6+.

**Survives a 2029 glut?:** no — Too far from product to matter. A product landing in the 2030s competes with mature IGZO 2T0C (A1) and cheap DRAM.

**Fatal-flaw candidate:** No defect-controlled, wafer-scale 2D growth at BEOL-compatible temperature, and no array-scale demonstration. Contact resistance and variability are unsolved. IGZO (C-01..04) already delivers the low-leakage benefit on 300mm today.

*Possible?* no (not within the venture horizon) — lab devices only; UNSUPPORTED at array scale · *Profitable?* no · *Doable by this founder?* no

*Business-model lenses:* university/lab patent license — premature

### C-42 — Printed organic ferroelectric memory (Thinfilm post-mortem) — ☠ KILLED (R4-NO-WINNING-AXIS: ~$4x10^7/GB by label cost (A3 model) is ~6.8 orders of magnitude above $6.40/GB glut DDR5. It also has ms latency, 10^3-10^5 endurance and high-voltage programming. It wins no axis any RAM buyer pays for. Its only market is anti-counterfeit labels storing a few bits, which is not memory. The pioneer (Thin Film Electronics) left printed memory for NFC and then microbatteries as Ensurge [UNVERIFIED-training; not re-checked, quota spent on survival-relevant cards]. The mechanism is real for bit-level labels, so the rule is R4, not R1.)

*Sub-branch:* Exotic: organic/polymer and printed memory · *Materials sense:* mixed:a+b

**What it is:** Roll-to-roll printed P(VDF-TrFE) ferroelectric-polymer passive-matrix memory, the Thinfilm Electronics lineage, built on a U.S. printed-electronics pilot line (e.g. NextFlex, San Jose CA) [UNVERIFIED-training]. Product: printed memory labels, pitched here as 'printable RAM'.

**Why it could work:** No lithography and no vacuum: gravure or inkjet printing of a ferroelectric polymer between printed electrodes costs cents per label. Thinfilm did ship 20-bit printed memory labels (~2010s) [UNVERIFIED-training].

**Evidence:** TRL 2 · Rule 1: SUPPORTED for few-bit printed labels (TRL 8 as labels); UNSUPPORTED for any RAM role
  - [Thin Film Electronics ASA printed ferroelectric polymer memory (20-bit labels); pivot to NFC (Kovio fab, 2014), then to microbatteries as Ensurge Micropower (2021); insolvency ~2024]() — company, 2009-2024. [UNVERIFIED-training] citation from A3 training data (<= mid-2026). No URL could be opened or seen this session: the shared WebSearch budget was exhausted and web hosts returned proxy 403. Verify agent: add a URL or downgrade.

**Capital tier:** T2 | **Time to first revenue:** never as RAM | **Gross margin estimate:** n/a

**US manufacturability:** NextFlex pilot lines (San Jose CA) or university printed-electronics labs. The former Thinfilm/Kovio San Jose line is closed [UNVERIFIED-training].

**Who is already doing this:** Nobody for RAM. Thinfilm exited memory.

**Wins on which axis, for which buyer:** Cost per label for a few bits (anti-counterfeit tags) — not any RAM axis. — for None for RAM; brand-protection labels at most.

**Survives a 2029 glut?:** no — ~$4e7/GB vs $6.40/GB glut (~6e6x); irrelevant to any DRAM price.

**Fatal-flaw candidate:** Density, latency and endurance are each 6-10 orders of magnitude from RAM. The company that pioneered it abandoned memory twice and later failed [UNVERIFIED-training].

*Possible?* no as RAM (UNSUPPORTED for any RAM role; 20-bit labels did ship, no URL retrievable this session) · *Profitable?* no · *Doable by this founder?* no

*Business-model lenses:* none viable

### C-43 — Cryo-CMOS gain-cell eDRAM IP for quantum-computer control — ☠ KILLED (DUPLICATE: Same idea as C-32: a zero-extra-mask Si 2T/3T gain-cell eDRAM compiler/IP on SkyWater S90 FD-SOI and GF 12LP+, licensed for NRE plus royalty. The only difference is a 4 K characterization deck and a quantum-controller buyer list. That is a C-32 product line costing ~$50-150k of dilution-fridge time [ESTIMATE], not a separate venture, and its market is a few dozen quantum teams, most designing in-house. Physics is better than the card says (TRL 4): a 16 Kb 4T gain cell keeps >16.6 s at 4.2 K (ISCAS 2023 / US 12412613), a 4 Kb 40nm cell keeps 66.5 s (arXiv 2311.11572), and a 28nm 3T1C runs at 4 K (ISOCC 2024). If C-32 is killed elsewhere, re-score C-43 as KEEP_WITH_CORRECTIONS with the corrections below; it does not fail on physics.)

*Sub-branch:* Exotic/cryogenic memory (vs superconducting memory) · *Materials sense:* b-process

**What it is:** A memory-IP and test-chip business offering Si gain-cell eDRAM macros characterized at 4 K and 77 K for cryo-CMOS qubit-controller ASICs, fabbed on GF 12LP+ (Malta NY) or SkyWater 90nm FD-SOI. Revenue is NRE plus licenses from quantum hardware teams and national-lab programs.

**Why it could work:** At cryogenic temperatures subthreshold leakage collapses, so Si gain-cell retention rises from microseconds to seconds or more [UNVERIFIED-training]. That makes refresh nearly free while keeping ~2x SRAM density and very low static power. This matters because the 4 K stage has only ~1 W of cooling budget. Superconducting memories (SFQ/JMRAM) remain far less dense.

**Evidence:** TRL 4 · Rule 1: SUPPORTED
  - [Disrupting the DRAM roadmap with capacitor-less IGZO DRAM technology](https://www.imec-int.com/en/articles/disrupting-dram-roadmap-capacitor-less-igzo-dram-technology) — industry, 2023. 2T0C gain-cell concept: charge stored on the read-transistor gate capacitance — the same topology as Si gain cells (CROSS-REFERENCE: seen in another agent's search results, not opened by A3)
  - [OpenRAM open-source SRAM compiler (GitHub README; v1.2.50 commit 2026-10-27)](https://github.com/VLSIDA/OpenRAM) — industry, 2026-10. Opened via git: BSD-3 SRAM compiler, generates GDS/LEF/Liberty/SPICE for sky130 (SkyWater) and gf180mcu; actively maintained (last commit 2026-10-27)
  - [Cryogenic CMOS eDRAM/gain-cell characterization papers (2020-2024) and Intel Horse Ridge cryo-CMOS controller]() — conference, 2020-2024. [UNVERIFIED-training] citation from A3 training data (<= mid-2026). No URL could be opened or seen this session: the shared WebSearch budget was exhausted and web hosts returned proxy 403. Verify agent: add a URL or downgrade.
  - [Energy-efficient memory for cryogenic computing (US patent 12412613)](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12412613) — patent, unknown. (via search snippet) 16 Kb 4T gain-cell eDRAM; data retention time 16.67 s at 4.2 K (2.6x prior cryo eDRAM); same chip reported at ISCAS 2023 (>16.6 s, 49.23 uW/Kb)
  - [CQS-eDRAM: cryogenic 4T transmission-gate gain-cell eDRAM, 4 Kb, 40 nm (arXiv 2311.11572)](https://arxiv.org/pdf/2311.11572) — peer-reviewed, 2023-11. (via search snippet) measured retention 66.5 s at cryogenic temperature (exact T not confirmed from snippet)
  - [A 28-nm 10.4-fJ/b Cryogenic embedded DRAM with 3T1C Gain Cell and MBIST at 4-Kelvin (ISOCC 2024)](https://kms.shanghaitech.edu.cn/handle/2MSLDSTB/452410?mode=full) — conference, 2024. (via search snippet) 28nm 3T1C gain-cell eDRAM at 4 K for qubit readout; median retention 4.8 ms, refresh eliminated; 61.4 Gb/s
  - [Gain-Cell Embedded DRAM under Cryogenic Operation - A First Study (Bar-Ilan / BGU)](https://cris.biu.ac.il/en/publications/gain-cell-embedded-dram-under-cryogenic-operation-a-first-study/) — peer-reviewed, 2021. (via search snippet) Bar-Ilan gain-cell group's cryogenic study; transistor models measured down to 77 K

**Capital tier:** T1 | **Time to first revenue:** 24-36 months (NRE/research contracts) | **Gross margin estimate:** 60-80% (IP/NRE)

**US manufacturability:** GF Fab 8 Malta NY (12LP+) or SkyWater Bloomington MN (90nm FD-SOI). Cryo test needs a dilution refrigerator, rented from a university or national lab.

**Who is already doing this:** In-house cryo-CMOS teams (Intel Horse Ridge, IBM, Google, imec); academic cryo gain-cell groups (ShanghaiTech and other Chinese groups; Bar-Ilan/BGU, the academic lineage of RAAAM [UNVERIFIED-training]); SEEQC (SFQ). RAAAM, the C-32 competitor, is the natural owner of this extension.

**Wins on which axis, for which buyer:** Static power at the 4 K stage and memory density for cryo control electronics. — for Quantum computing hardware teams (IBM Quantum NY, Google Quantum AI), DARPA/IARPA quantum programs.

**Survives a 2029 glut?:** yes — Unrelated to DRAM pricing.

**Fatal-flaw candidate:** The market is a few dozen teams, most of which design memory in-house. Quantum roadmaps may keep control at room temperature for years. It needs a cryo test lab and a circuit designer.

*Possible?* yes — physics favorable · *Profitable?* no as a standalone company — the market is a few dozen teams · *Doable by this founder?* no

*Business-model lenses:* IP licensing; defense/government NRE; university/lab patent license

## B. Architecture & systems (14 cards)

### C-44 — DDR4 Second-Life CXL Expander — ☠ KILLED (SCORE<55: Scored 50.0/100 default (rank 35/40), 48.3 moonshot. Weakest: capital 2/5 (T2 ($2M+): board design, controller access, firmware/SI team and CXL compliance before the first tier-2 qualification.); time to revenue 2/5 (24 months (18-30): board, controller-vendor access and qualification at one tier-2 cloud.); margin 2/5 (15-30% on the card (mid 22%), i.e. ~$270-540 of gross profit per ~$1.8k card; it needs thousands of cards a year.). Scorer verdicts — founder: The buyer math works (+$7-14/GB in 4Q26), but it is a T2 hardware program that needs Marvell allocation and SI talent; this founder should resell the DDR4 instead (C-62). | vc: The buyer math works, but the vendor keeps ~$270-540 per card, Marvell sells the controller to hyperscalers that already do this in-house, and it needs a T2 hardware team: sub-scale hardware with no edge. | veteran: The unit economics flip positive once used DDR4 is valued at $3.9-5.8/GB resale, but a no-name cannot get Structera allocation or qualify mixed used DIMMs at 3 DPC on a T2 budget, and hyperscalers already do thi)

*Sub-branch:* CXL memory expansion / DIMM reuse (Microsoft-Meta style DDR4 recycling) · *Materials sense:* mixed:b+c

**What it is:** A PCIe Gen5 x16 CXL 2.0 Type-3 add-in card or 1U 'JBOM' holding 8-12 decommissioned DDR4-3200 RDIMMs behind a merchant DDR4-capable CXL controller (Marvell Structera X 2404-class or Microchip SMC 2000-class). A U.S. EMS (e.g. Sanmina) assembles it, and it ships with burn-in and qualification to operators moving to DDR5-only Xeon 6 / EPYC 9005 servers. The process 'materials' are DRAM that is already fabbed and paid for, and the capital is DIMMs that are already depreciated.

**Why it could work:** Reuse beats buying DDR5 for any owner at used-RDIMM resale values, not only at hyperscaler scale. Card $2.34/GB plus recovered DDR4 $4-11/GB = $6.3-13.3/GB against a $20.31/GB DDR5 RDIMM (4Q26 canonical), a +$7-14/GB advantage. In the glut it is $2.84-3.84 against $8.12, a +$4.3-5.3/GB advantage. Structera X 2404 runs 12 DDR4-3200 DIMMs (3 DPC) with inline LZ4 (sampling since Q4 2024).

**Evidence:** TRL 7 · Rule 1: SUPPORTED
  - [Pond: CXL-Based Memory Pooling Systems for Cloud Platforms (ASPLOS '23) artifact repo](https://github.com/vtess/Pond) — conference, 2023-03. Opened. Microsoft Azure/Virginia Tech CXL pooling paper. The repo holds the CXL-emulation scripts, and the paper preprint is linked at huaicheng.github.io/p/asplos23-pond.pdf (not opened).
  - [Linux CXL Subsystem Maturity Map (mainline, HEAD 2026-10-31)](https://github.com/torvalds/linux/blob/master/Documentation/driver-api/cxl/maturity-map.rst) — industry, 2026-10. Opened. Single-host Type-3 enumeration/HDM decoders are [2] stabilizing. Dynamic Capacity Devices, multi-host sharing and fabrics/G-FAM are [0] known gaps. PMEM GPF/dirty shutdown is [3] mature.
  - [SK hynix HMSDK README](https://github.com/skhynix/hmsdk) — company, 2025-11. Opened. HMSDK v4.0 (2025-11-03). CXL weighted-interleave landed in upstream Linux v6.9 and DAMON tier migration in v6.11. CXL tiering software is free and upstream.
  - [RAM market update (DRAMeXchange snapshot 2026-08-31)](https://www.buysellram.com/blog/ram-market-update/) — news, 2026-08-31. CROSS-REF (p1-backend.jsonl snippet). DDR4 8Gb avg $44.37 vs DDR5 16Gb avg $53.92: DDR4 is dearer per GB than DDR5.
  - [TrendForce DRAM spot price page](https://www.trendforce.com/price_dram.html) — industry, 2026-08-03. CROSS-REF (p1-backend.jsonl snippet). DDR4 8Gb spot avg $21.00 on 2026-08-03.
  - [Barclays via TechNews: DDR4 pricier than DDR5 in some channels](https://finance.technews.tw/2026/10/13/the-shortage-of-memory-chips-may-continue-for-another-two-years/) — news, 2026-10-13. CROSS-REF (p1-market.jsonl snippet). DDR4 increases outpace DDR5, and the two are price-inverted in some channels.
  - [KED Global: DDR4 8Gb bottomed at $1.30](https://www.kedglobal.com/korean-chipmakers/newsView/ked202310040013) — news, 2023-10-04. CROSS-REF (p1-market.jsonl snippet). 2023-trough DDR4 value anchor.
  - [Marvell Introduces Breakthrough Structera CXL Product Line](https://investor.marvell.com/2024-07-30-Marvell-Introduces-Breakthrough-Structera-CXL-Product-Line-to-Address-Server-Memory-Bandwidth-and-Capacity-Challenges-in-Cloud-Data-Centers) — company-IR, 2024-07-30. (via search snippet) Structera X 2404 supports DDR4 at 3 DPC (12 DIMMs per controller), with four inline LZ4 engines at full DDR4-3200 bandwidth; CXL 2.0 x16 or x8+x8 dual host; samples in Q4 2024.
  - [Marvell Structera X 2404 memory expansion controller product brief](https://www.marvell.com/content/dam/marvell/en/public-collateral/assets/marvell-structera-x-2404-memory-expansion-controller-product-brief.pdf) — company-IR, 2024. (via search snippet) Product brief for the DDR4 CXL expander controller.
  - [DDR4 64GB RDIMM server memory appraisal](https://www.amcompute.com/appraisals/ddr4-64gb-rdimm) — market-research, 2026-08. CROSS-REF (sources/v3-backend.jsonl, search snippet). Used 64GB DDR4 RDIMMs sold for ~$250-370 over the trailing 12 months (~$3.9-5.8/GB).
  - [Refurbished DDR4 server memory 2026: server RAM price crisis](https://pcserverandparts.com/news/refurbished-ddr4-server-memory-2026-server-ram-price-crisis/) — blog, 2026. CROSS-REF (sources/v3-backend.jsonl, search snippet). 512 GB of refurbished DDR4 costs $2,300-5,500 in modules (~$4.5-10.7/GB).

**Capital tier:** T2 | **Time to first revenue:** 18-30 months: board design + controller vendor access + qualification at one tier-2 cloud | **Gross margin estimate:** 15-30% (card without DRAM)

**US manufacturability:** Board assembly/test at any U.S. EMS (Sanmina, Kimball, SMTC). The controller silicon is TSMC (Taiwan). DIMMs are recovered from U.S. data centers. Only assembly and recovery are U.S.

**Who is already doing this:** Marvell Structera X 2404 [VERIFIED via search snippet: DDR4-3200, 12 DIMMs at 3 DPC, four inline LZ4 engines, CXL 2.0 x16, sampling Q4 2024]; Microchip SMC 2000 [UNVERIFIED-T]; Astera Labs Leo [UNVERIFIED-T]; Penguin Solutions/SMART CXL add-in cards (CXA-8F2W, 1 TB class; DDR type UNVERIFIED); Microsoft/Meta in-house DDR4 reuse [UNVERIFIED-T]

**Wins on which axis, for which buyer:** $/GB of added capacity from already-owned DIMMs; lifecycle length/Scope-3; supply security when DDR5 allocation is refused — for Tier-2/neocloud and large-enterprise operators with >=10k retired DDR4 RDIMMs and DDR5-only new servers (VM density, in-memory DB capacity tier)

**Survives a 2029 glut?:** partially — At glut prices (DDR5 RDIMM $8.12/user-GB; recovered DDR4 $0.5-1.5/GB) reuse still saves ~$4.3-5.3/GB. At a 2023-style trough ($2.32/GB) it loses $0.3-0.8/GB. The larger glut risk is that DDR5 allocation frees up and buyers stop tolerating a CXL latency tier, so volumes shrink even though the unit case holds.

**Fatal-flaw candidate:** Controller access and qualification, not unit economics. Marvell Structera X sells to hyperscalers that already run in-house DDR4 reuse, and Microchip SMC 2000 DDR4 support is UNVERIFIED. A small vendor must qualify mixed used DIMMs at 3 DPC and pass CXL compliance on a T2 budget. The buyer set (tier-2 operators with >=10k retired DDR4 RDIMMs and DDR5-only new servers) is narrow, and selling those DIMMs into the hot recert market (C-62) is the easy alternative.

*Possible?* yes: deployed at hyperscalers with merchant controllers · *Profitable?* marginal: the buyer case is positive (+$7-14/GB in 4Q26, +$4-5/GB in the glut), but the vendor keeps only 15-30% of a ~$1.8k card (~$270-540 per card), so profit needs thousands of cards a year · *Doable by this founder?* no: hardware/firmware team and controller allocation required

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
  - [Penguin Solutions Introduces Industry's First Production-Ready CXL-Based KV Cache Server](https://www.businesswire.com/news/home/20260316416248/en/penguin-solutions-introduces-industrys-first-production-ready-cxl-based-kv-cache-server) — news, 2026-03-16. (via search snippet) MemoryAI KV cache server: Altus 4U, dual AMD EPYC, up to 11 TB (3 TB DDR5 + 8x1 TB SMART CXA-8F2W CXL AICs); Dynamo-compatible; vendor claims of 3.8x vs RDMA and 10x vs NVMe are unverified.
  - [NVIDIA BlueField-4 Powers New Class of AI-Native Storage Infrastructure](https://nvidianews.nvidia.com/news/nvidia-bluefield-4-powers-new-class-of-ai-native-storage-infrastructure-for-the-next-frontier-of-ai) — company-IR, 2026-01. (via search snippet) Inference Context Memory Storage platform on BlueField-4; early builders AIC, Cloudian, DDN, Dell, HPE, Hitachi Vantara, IBM, Nutanix, Pure Storage, Supermicro, VAST, WEKA.
  - [Nvidia standardizes GPU cluster KV cache offload to NVMe SSDs](https://blocksandfiles.com/2026/01/06/nvidia-standardizes-gpu-cluster-kv-cache-offload-to-nvme-ssds/) — news, 2026-01-06. (via search snippet) BlueField-4 and ICMS expected to ship 2H26. Dell, IBM, VAST and WEKA said they will support it.

**Capital tier:** T1 | **Time to first revenue:** 12-18 months: demo node, then 1-2 design wins against Penguin MemoryAI and OEM reference boxes | **Gross margin estimate:** 10-20% hardware (CXL modules bought at a competitor's or memory maker's price); 60%+ on a subscription if one ever attaches

**US manufacturability:** Integration/burn-in on a U.S. bench (East Coast) or through Supermicro San Jose. CPUs, NICs and most DDR5 are imported. Micron Idaho DDR5 is not before mid-2027.

**Who is already doing this:** Penguin Solutions MemoryAI KV cache server [VERIFIED via snippet: launched 2026-03-16 at GTC; dual EPYC, 3 TB DDR5 + up to 8x1 TB SMART CXA-8F2W CXL AICs = 11 TB; Dynamo-compatible; part of OriginAI]; NVIDIA BlueField-4 ICMS -> CMX/STX reference (CES 2026; GTC Mar-2026; ships 2H26; Dell, HPE, IBM, VAST, WEKA, DDN, Pure, Supermicro, Nutanix, Hitachi Vantara, Cloudian, AIC) [VERIFIED via snippet]; WEKA; VAST; Pliops; Hammerspace; Moonshot/Mooncake in-house; Tensormesh

**Wins on which axis, for which buyer:** $/GB-month of shared hot-KV capacity against GPU HBM (~$180-250/GB effective) and TTFT on cache hits — for Neocloud inference providers and enterprise private-inference teams with long system prompts, RAG and multi-turn agent sessions

**Survives a 2029 glut?:** partially — A 60% DRAM drop cuts the node BOM and stretches the DRAM break-even reuse interval from 1.35 h to 3.4 h. It also lets every OEM sell the same box, and flash tiers (break-even ~78 h) keep undercutting DRAM for warm KV.

**Fatal-flaw candidate:** The identical product already ships from Penguin Solutions (MemoryAI, Mar-2026), and Penguin owns the SMART CXL card line, so a new entrant buys its key part from a competitor and has no cost or capability edge. Beyond that, it is a commodity server plus open-source software (Mooncake/LMCache) that OEM reference designs replicate. A 4 TB node ties up ~$80-130k of DRAM at 4Q26 prices for reseller margin, and NVIDIA's BlueField-4 flash tier plus 8-SSD nodes match its reload bandwidth over 2x400G for warm KV.

*Possible?* yes: production at Moonshot; all parts off-the-shelf · *Profitable?* no for a new entrant: Penguin sells the same box with captive CXL card supply, leaving 10-20% reseller margin on ~$100k of DRAM per node; the subscription attach is unproven · *Doable by this founder?* no: ~$100k DRAM working capital per node exceeds T0, and neocloud buyers want GPU-infrastructure credibility the founder lacks (the same gap noted on C-75)

*Business-model lenses:* module/appliance; SaaS (support + KV observability subscription)

### C-46 — Flash KV Accelerator (U.S. Pliops-style NVMe KV engine) — ☠ KILLED (R4-NO-WINNING-AXIS: The card's named axes ($/GB-month of warm KV, TTFT on long-context reuse) come from NAND flash, not from the card, and the buyer already gets them free. Dynamo KVBM's GDS disk tier, LMCache and 3FS run on plain NVMe, and the card's own fatal_flaw concedes they 'capture most of the benefit without a special card'. The one hardware-specific gain, an offloaded KV engine, already ships in Pliops' custom XDP Pro1 ASIC plus SSD array, integrated with vLLM and Dynamo (StorageReview; Blocks & Files 2025-05-14), and an FPGA card loses to that ASIC on BOM and power. NVIDIA has since made the flash KV tier a reference architecture (BlueField-4 ICMS at CES 2026, renamed CMX/STX at GTC 2026, shipping 2H26 with 12+ storage vendors). Against every alternative its buyer can actually get, free or purchasable, the FPGA card wins no axis. That is the same test that killed C-77.)

*Sub-branch:* LLM inference KV-cache tiering - flash tier with hardware KV engine · *Materials sense:* a-material

**What it is:** Pliops XDP LightningAI uses a custom XDP (Pro1) ASIC card plus an SSD array served over NVMe-oF, not an FPGA, so an FPGA-based U.S. entrant starts a silicon generation behind on cost and power.

**Why it could work:** The material swap is NAND for DRAM. Enterprise NVMe at ~$0.30-0.60/GB holds 1M tokens of Llama-70B FP8 KV (164 GB) for ~$0.003/h, so caching pays if reused once per ~78 h, against ~1.35 h for DDR5. One Gen5 SSD reloads a 128k context in ~1.8 s vs ~41 s recompute. NAND stopped rising in Oct 2026, with surplus forecast for 2H27.

**Evidence:** TRL 8 · Rule 1: SUPPORTED
  - [NVIDIA Dynamo KVBM README + KV-cache offloading docs](https://github.com/ai-dynamo/dynamo) — company, 2026-11. Opened. GPU<->CPU<->Disk<->Remote KV tiering with GDS/NIXL transfers. LMCache, FlexKV and HiCache are interchangeable backends. Host/disk KV tiering is free open-source software.
  - [WEKA partners with NVIDIA on KV cache storage for Dynamo (SC25)](https://siliconangle.com/2025/11/20/nvidia-weka-kv-cache-solution-ai-inferencing-sc25/) — news, 2025-11-20. Flash-based KV tier partnership between WEKA and NVIDIA (headline seen in the Dynamo README; body not opened).
  - [LMCache README](https://github.com/LMCache/LMCache) — industry, 2026-11. Opened. Vendor-neutral KV layer that tiers to CPU RAM, SSD and remote stores. Joined the PyTorch Foundation, and Tensormesh launched, in Oct 2025. Integrated in NVIDIA Dynamo (Sep 2025).
  - [NAND flat after 21 months while DRAM hits record](https://tech-insider.org/dram-record-high-nand-flat-21-months-october-2026/) — news, 2026-10. CROSS-REF (p1-market.jsonl snippet). NAND contract stopped rising in Oct 2026.
  - [TrendForce 2026-07-30 press release](https://www.trendforce.com/presscenter/news/20260730-13158.html) — industry, 2026-07-30. CROSS-REF (p1-market.jsonl snippet). NAND turns to surplus in 2H27 while the DRAM gap widens.
  - [Pliops XDP LightningAI supercharges KV cache to optimize LLM inference with NVIDIA Dynamo](https://www.storagereview.com/review/pliops-xdp-lightningai-supercharges-kv-cache-to-optimize-llm-inference-with-nvidia-dynamo) — news, 2025. (via search snippet) Dedicated appliance with a PCIe card powered by a custom XDP ASIC and an array of SSDs; FusIOnX KV Store over NVMe-oF; Dynamo integration.
  - [Pliops bypasses HBM limits for GPU servers](https://blocksandfiles.com/2025/05/14/pliops-bypasses-hbm-limits-for-gpu-servers/) — news, 2025-05-14. (via search snippet) Pliops KV-cache memory tier below HBM is a shipping product.
  - [Nvidia standardizes GPU cluster KV cache offload to NVMe SSDs](https://blocksandfiles.com/2026/01/06/nvidia-standardizes-gpu-cluster-kv-cache-offload-to-nvme-ssds/) — news, 2026-01-06. (via search snippet) NVIDIA ICMS on BlueField-4 standardizes flash KV offload; ships 2H26.

**Capital tier:** T2 | **Time to first revenue:** 24-36 months: FPGA prototype, software integration, design-ins | **Gross margin estimate:** 40-60% if differentiated

**US manufacturability:** FPGA silicon from TSMC. Board assembly at a U.S. EMS. SSD NAND comes from Micron (Singapore), Kioxia/SanDisk (Japan) and Solidigm (China fab). Little U.S. content.

**Who is already doing this:** Pliops XDP LightningAI [VERIFIED via snippet: ASIC + SSDs, vLLM and Dynamo integration, Dell Tech World 2025 showcase]; NVIDIA BlueField-4 ICMS -> CMX/STX [VERIFIED via snippet; ships 2H26] with Dell, HPE, IBM, VAST, WEKA, DDN, Pure, Supermicro, Nutanix, Hitachi Vantara, Cloudian, AIC; IBM Storage Scale + Dynamo; DeepSeek 3FS; LMCache/Dynamo KVBM on plain NVMe (free)

**Wins on which axis, for which buyer:** $/GB-month of warm KV and TTFT on long-context reuse — for Inference providers and enterprise RAG/agent platforms with long shared prefixes

**Survives a 2029 glut?:** yes — The axis is flash vs recompute, not DRAM price. A NAND surplus in 2H27 lowers BOM further. A DRAM glut narrows the DRAM-vs-flash gap but does not close it (3.4 h vs 78 h break-even).

**Fatal-flaw candidate:** NVIDIA is building this tier itself (Dynamo KVBM + GDS + BlueField-4 storage), and software-only stacks on plain NVMe (3FS, LMCache, HiCache) capture most of the benefit without a special card. A late U.S. entrant faces Pliops/WEKA/VAST with a 2-3 year head start.

*Possible?* yes: shipping from several vendors · *Profitable?* no: a late FPGA entrant against a shipping ASIC, NVIDIA's reference architecture and free NVMe tiering · *Doable by this founder?* no

*Business-model lenses:* fabless->foundry (FPGA then ASIC); module/appliance

### C-47 — Compressed CXL Expander (licensed inline compression IP) — ☠ KILLED (SCORE<55: Scored 45.0/100 default (rank 39/40), 42.5 moonshot. Weakest: moat 1/5 (The compression IP is licensed non-exclusively (ZeroPoint sells to SoC makers), so the venture is a downstream FPGA integrator of IP its com); cycle-proofing 1/5 (Glut kills it: at the ~$8.1/GB RDIMM deck, 2x on 512 GB saves ~$4.2k, which no longer covers a $3-8k FPGA card plus the latency penalty.); founder-fit 1/5 (Needs a full-time RTL/FPGA team, CXL compliance expertise and a later ASIC tape-out; nothing about it is a part-time software job.). Scorer verdicts — founder: Merchant silicon (Structera X) and ZeroPoint's ASIC licensee already do this more cheaply, and the glut wipes out the savings; dead for this founder. | vc: An FPGA integrator of non-exclusive compression IP fighting Marvell's ASIC that already does the job, and the savings stop covering the card in a glut: dead on arrival. | veteran: An FPGA integrator of non-exclusive IP that Marvell already put in merchant silicon; the DRAM saving that pays for the card is gone at the $8.15 glut.)

*Sub-branch:* Hardware memory compression · *Materials sense:* b-process

**What it is:** An FPGA CXL 2.0 Type-3 card (Altera Agilex 7 R-tile or AMD Versal Premium) that runs licensed inline memory-compression IP (ZeroPoint Technologies, Gothenburg, or an LZ4-class core) in front of 256-512 GB DDR5. It exposes ~2x the physical capacity to Redis/Valkey/Memcached and VM hosts and would later tape out as an ASIC.

**Why it could work:** The IBM MXT lineage and ZeroPoint claim 2-4x on compressible data [UNVERIFIED-T]. At $20-32/GB, a 2x ratio on 512 GB is worth ~$10-16k of DRAM per card in 4Q26. Linux already proves the demand: zswap plus Intel IAA hardware DEFLATE.

**Evidence:** TRL 7 · Rule 1: SUPPORTED
  - [Linux IAA Compression Accelerator crypto driver doc](https://github.com/torvalds/linux/blob/master/Documentation/driver-api/crypto/iaa/iaa-crypto.rst) — industry, 2026-10. Opened. Intel In-Memory Analytics Accelerator hardware DEFLATE ('deflate-iaa') is selectable as the zswap compressor. Hardware memory compression already ships in Xeon CPUs.
  - [Linux zswap doc](https://github.com/torvalds/linux/blob/master/Documentation/admin-guide/mm/zswap.rst) — industry, 2026-10. Opened. OS-level compressed RAM cache is free in every Linux kernel.
  - [Linux CXL Subsystem Maturity Map (mainline, HEAD 2026-10-31)](https://github.com/torvalds/linux/blob/master/Documentation/driver-api/cxl/maturity-map.rst) — industry, 2026-10. Opened. Single-host Type-3 enumeration/HDM decoders are [2] stabilizing. Dynamic Capacity Devices, multi-host sharing and fabrics/G-FAM are [0] known gaps. PMEM GPF/dirty shutdown is [3] mature.
  - [ZeroPoint Technologies Signs Global Customer to Bring Hardware-Accelerated Compression to Hyperscale Data Centers](https://us.design-reuse.com/news/55960/zeropoint-hardware-accelerated-compression-hyperscale-data-centers.html) — news, 2024-03-26. (via search snippet) DenseMem CXL Type-3 compression IP licensed to an unnamed 'major global semiconductor manufacturer'.
  - [ZeroPoint aims to tackle AI memory bottlenecks with compression IP](https://www.blocksandfiles.com/ai-ml/2024/09/09/zeropoint-aims-to-tackle-ai-memory-bottlenecks-with-compression-ip/1617379) — news, 2024-09-09. (via search snippet) ZeroPoint earns royalties licensing IP cores and drivers to SoC customers; 24-36 month sales processes.
  - [ZeroPoint's DenseMem compression saves power in the datacenter](https://www.eenewseurope.com/en/zeropoints-densemem-compression-saves-power-in-the-datacenter/) — news, 2024. (via search snippet) DenseMem gives 2-4x effective capacity on CXL Type-3; implemented in TSMC 5nm; vendor claims ~50% better perf/W.
  - [Marvell Introduces Breakthrough Structera CXL Product Line](https://investor.marvell.com/2024-07-30-Marvell-Introduces-Breakthrough-Structera-CXL-Product-Line-to-Address-Server-Memory-Bandwidth-and-Capacity-Challenges-in-Cloud-Data-Centers) — company-IR, 2024-07-30. (via search snippet) Inline LZ4 compression engines in merchant CXL memory controllers; sampling Q4 2024.

**Capital tier:** T2 | **Time to first revenue:** 30-42 months: IP license (24-36 month licensor cycle), FPGA card, CXL compliance, qualification with one cache operator | **Gross margin estimate:** 20-40% (FPGA BOM $3-8k against ~$10.4k of DRAM saved in 4Q26; priced against Structera-based ASIC cards)

**US manufacturability:** FPGA from TSMC; board at a U.S. EMS; IP from Sweden. Little U.S. content beyond assembly.

**Who is already doing this:** Marvell Structera X 2404 four inline LZ4 engines [VERIFIED via snippet; sampling Q4 2024] (compression on other Structera parts [UNVERIFIED-T]); ZeroPoint DenseMem [VERIFIED via snippet: licensed to an unnamed major semiconductor maker Mar-2024, TSMC 5nm, licenses IP and drivers to SoC makers]; Intel IAA + zswap (upstream); Meta TMO / Google zswap far memory (software); Rambus (CXL controller IP)

**Wins on which axis, for which buyer:** Effective $/GB (capacity multiplier) for compressible in-memory data — for In-memory cache operators (Redis/Valkey/Memcached fleets) and VM hosts with cold pages

**Survives a 2029 glut?:** no — At the canonical glut deck ($8.12/GB RDIMM), 2x on 512 GB saves ~$4.2k of DRAM, which no longer covers a $3-8k FPGA card plus the latency penalty.

**Fatal-flaw candidate:** The job is already done in merchant silicon (Structera X with four inline LZ4 engines) and in licensed ASIC IP. ZeroPoint licenses to SoC makers, so the venture would be a downstream FPGA integrator of IP its competitors put in ASICs at lower cost and power. Free CPU compression (IAA + zswap) covers colder pages. The hottest 'need more RAM' data (FP8/INT4 weights, KV) barely compresses, and at glut prices the DRAM saved (~$4.2k per 512 GB card) no longer pays for a $3-8k FPGA BOM.

*Possible?* yes: demonstrated on FPGA and in merchant controllers · *Profitable?* no: squeezed between free CPU/controller compression and a glut · *Doable by this founder?* no

*Business-model lenses:* IP licensing (in-license); fabless->foundry; module/appliance

### C-48 — On-prem MoE Box (DRAM-instead-of-HBM inference appliance) — ☠ KILLED (RED-TEAM: DD6 (Private MoE Inference Appliance (DRAM instead of HBM)) was KILLED by the four-persona red team: The FATAL objection holds. Four concurrent users touch 3.88x one user's expert bytes, so the 1-socket L box serves 1-2 users at >=10 tok/s (6.7-13.3 named), not 4 (27). At authorized-channel RDIMM prices the L box quotes $78,708. A $44.6k two-node Mac Studio cluster matches its single-stream speed with a ~10x faster first token, and U.S.-origin 1T models make it a one-user box for defense. So the L SKU, which carried See 05_REDTEAM.md (DD6) and 04_DEEPDIVES/private-moe-appliance.md §14.)

*Sub-branch:* HBM alternatives at system level: CPU-DRAM-resident MoE inference · *Materials sense:* mixed:a+c

**What it is:** Prefer 1-2 socket Intel Xeon 6 (AMX; 12ch DDR5-6400/MRDIMM) or accept slow CPU prefill on EPYC. Size 1.5 TB if Kimi-K2.5 must run in dual-socket mode, or 768 GB and run single-socket.

**Why it could work:** Decode estimate from measured KTransformers data, not the roofline: DeepSeek-R1 Q4 ran 8.73 tok/s (1 socket) and 11.26 tok/s (2 sockets) on Xeon 6454S with 8ch DDR5-4800. Scaled to 12ch DDR5-6400 and 32B active, that is ~20 tok/s (1 socket) and ~26 tok/s (2 sockets, which needs a second weight copy and ~1.5 TB). DRAM: 768 GB = $15.6k and 1.5 TB = $31.2k at the $20.31/GB 4Q26 deck; $6.2k/$12.5k in the glut.

**Evidence:** TRL 8 · Rule 1: SUPPORTED
  - [KTransformers README + Kimi-K2.5 / DeepSeek-V4-Flash tutorials](https://github.com/kvcache-ai/ktransformers) — industry, 2026-10. Opened. CPU-GPU hybrid MoE inference: Kimi-K2.5 needs >=600GB system RAM + 48GB VRAM, DeepSeek-V4-Flash needs >=200GB RAM + one RTX 5090. DRAM replaces HBM for weight residency.
  - [DeepSeek-V3 config_671B.json](https://github.com/deepseek-ai/DeepSeek-V3) — company, 2025-08. Opened. MLA latent KV (kv_lora_rank 512 + rope 64, 61 layers) is about 68.6 KiB/token at BF16, against 320 KiB/token for Llama-3.1-70B (computed by B).
  - [Samsung seeks >3x HBM3E pricing for HBM4](https://www.sammyfans.com/2026/10/02/samsung-seeks-more-than-3x-hbm3e-pricing-for-hbm4/) — news, 2026-10-02. CROSS-REF (p1-market.jsonl snippet). HBM3E ~$1.50/Gb; 2027 HBM4 asks mid-to-high $4/Gb.
  - [Counterpoint via EE Times Asia: 64GB RDIMM $450 to >$900](https://www.eetasia.com/memory-prices-surging-by-90-from-4q-2025/) — news, 2026-01. CROSS-REF (p1-market.jsonl snippet). Server RDIMM contract doubled 4Q25 to 1Q26.
  - [ServNet DDR5 server memory price tracker 2026](https://www.servnetuk.com/research/ddr5-server-memory-price-tracker-2026) — industry, 2026-08. CROSS-REF (p1-market.jsonl snippet). Street 64GB DDR5 RDIMM ~$2,064 (~$32/GB).
  - [KTransformers Kimi-K2.5 tutorial (hardware requirements)](https://github.com/kvcache-ai/ktransformers/blob/main/doc/en/Kimi-K2.5.md) — other, 2026-10. Opened via git. Minimum: 2x RTX 4090 (48 GB VRAM), AVX512F x86 CPU, >=600 GB system RAM, ~600 GB native INT4 weights.
  - [KTransformers DeepSeek-V4-Flash tutorial](https://github.com/kvcache-ai/ktransformers/blob/main/doc/en/DeepSeek-V4-Flash.md) — other, 2026-10. Opened via git. 1x RTX 5090 (32 GB), >=200 GB RAM; decode 20+ tok/s on a single RTX 5090.
  - [KTransformers DeepSeek-R1/V3 tutorial](https://github.com/kvcache-ai/ktransformers/blob/main/doc/en/DeepseekR1_V3_tutorial.md) — other, 2025-02. Opened via git. Single socket 382 GB DRAM vs dual socket 1 TB DRAM. Decode 8.73 (32 cores) -> 11.26 (2x32 cores) -> 13.69 tok/s. Prefill 54 -> 74 -> 255-286 tok/s with the AMX kernel, on Xeon Gold 6454S with 8x DDR5-4800 per socket.
  - [Kimi-K2.5 deploy guidance (Hugging Face mirror)](https://huggingface.co/SinterForge/Kimi-K2.5/blob/main/docs/deploy_guidance.md) — other, 2026. (via search snippet; third-party mirror) KTransformers+SGLang on 8x L20 + 2x Xeon 6454S: ~640 tok/s prefill, ~24.5 tok/s decode at 48-way concurrency.

**Capital tier:** T1 | **Time to first revenue:** 8-14 months: demo unit and published benchmark, then build-to-order with 50% deposits after buyer security review | **Gross margin estimate:** 18-25% hardware (the card's own model prices at 22%); 60-80% on a subscription whose attach rate is unproven

**US manufacturability:** Assembled and tested in the U.S. (East Coast bench). CPUs/GPUs are TSMC and DDR5 is Korea/Taiwan (Micron Idaho from 2027). 'Assembled in USA' only, though TAA-compliant integration is feasible.

**Who is already doing this:** Puget Systems, Exxact, Lambda, Bizon, Supermicro, Dell Pro Max/HPE; NVIDIA DGX Station GB300 (large coherent memory) [UNVERIFIED-T]; Apple Mac Studio (512 GB unified memory) [UNVERIFIED-T]; KTransformers community/Chinese appliance vendors [UNVERIFIED-T]

**Wins on which axis, for which buyer:** $/GB of model-resident memory (DDR5 ~$26/GB vs ~$180-250/GB HBM-in-GPU) plus data sovereignty — for 20-500-person regulated firms (law, healthcare, CMMC/ITAR defense subcontractors) and universities running private chat/RAG/agents on 600B-1T-parameter MoE models

**Survives a 2029 glut?:** yes — A glut cuts the DRAM BOM from ~$20k to ~$8k, so the box gets cheaper and easier to sell. The risks are model-architecture shifts and GPU vendors' desk-side products, not DRAM price.

**Fatal-flaw candidate:** Commodity integration with thin hardware margin. NVIDIA DGX Station, Apple unified-memory machines and big OEMs can undercut it. Measured-scaled decode is ~20-26 tok/s single-stream, and the published Kimi-K2.5 multi-user reference used 8x L20 GPUs for ~24.5 tok/s decode at 48-way concurrency (via snippet, unverified). A 1-2 GPU box therefore serves only a handful of concurrent users, and long RAG prompts wait on CPU prefill. The only moat is service quality. It is a reseller business, not a memory venture.

*Possible?* yes: documented open-source configurations · *Profitable?* marginal: yes only if a recurring support/model subscription attaches · *Doable by this founder?* yes: integration + software, startable with deposits

*Business-model lenses:* module/appliance; SaaS (model-update/monitoring subscription); defense-first niche

### C-49 — TB-Class CXL Node for EDA/Genomics/HANA

*Sub-branch:* CXL memory expansion - vertical large-memory appliance · *Materials sense:* c-capital

**What it is:** Pre-validated single-socket Xeon 6 / EPYC 9005 servers carrying 8-16 E3.S CXL memory modules (Samsung CMM-D, Micron CZ122, SK hynix CMM-DDR5) that add 2-4 TB behind local DDR5. They are tuned with upstream weighted-interleave/DAMON tiering (SK hynix HMSDK) and Samsung SMDK, and sold to chip-design teams (full-chip Cadence/Synopsys runs), genome assemblers and SAP HANA shops that otherwise buy 4-socket boxes or cloud high-memory instances.

**Why it could work:** CXL adds capacity and bandwidth beyond the 1-DPC slot ceiling without dropping to 2-DPC speeds, and weighted interleave (Linux v6.9) uses the extra bandwidth. Single-host Type-3 enumeration works in mainline Linux. It matters only for jobs above ~3-6 TB per socket, or for bandwidth-bound single-socket nodes.

**Evidence:** TRL 8 · Rule 1: SUPPORTED
  - [SK hynix HMSDK README](https://github.com/skhynix/hmsdk) — company, 2025-11. Opened. HMSDK v4.0 (2025-11-03). CXL weighted-interleave landed in upstream Linux v6.9 and DAMON tier migration in v6.11. CXL tiering software is free and upstream.
  - [Samsung SMDK v2.2 README (CXL Memory Expander software)](https://github.com/OpenMPDK/SMDK) — company, 2024-12. Opened. Samsung CMM software stack (memory-node/swap/cache interfaces, tiering engine), demoed at SC24, OCP 2024 and FMS 2024. Last commit 2024-12-09.
  - [Linux CXL Subsystem Maturity Map (mainline, HEAD 2026-10-31)](https://github.com/torvalds/linux/blob/master/Documentation/driver-api/cxl/maturity-map.rst) — industry, 2026-10. Opened. Single-host Type-3 enumeration/HDM decoders are [2] stabilizing. Dynamic Capacity Devices, multi-host sharing and fabrics/G-FAM are [0] known gaps. PMEM GPF/dirty shutdown is [3] mature.
  - [Penguin Solutions: CXL memory expansion servers](https://www.penguinsolutions.com/products/cxl-memory-expansion-servers) — company-IR, 2026. (via search snippet; title and URL only) Penguin markets CXL memory-expansion servers built on SMART CXL add-in cards.

**Capital tier:** T1 | **Time to first revenue:** 12-18 months: two validated reference configs, then first sale through EDA/genomics channels against OEM incumbents | **Gross margin estimate:** 15-25%

**US manufacturability:** U.S. integration. The CMM modules are Samsung/SK hynix (Korea) and Micron (non-U.S. assembly [UNVERIFIED-T]).

**Who is already doing this:** Penguin Solutions CXL memory expansion servers (product page seen via search; Altus 4U line, SMART CXL AICs); Supermicro, Dell, HPE, Lenovo CXL-ready platforms; Colfax, Silicon Mechanics; AWS/Azure high-memory instances [UNVERIFIED-T]

**Wins on which axis, for which buyer:** TB and memory bandwidth per socket above the native slot ceiling (~3 TB/socket at 1 DPC with 256 GB RDIMMs; ~6 TB at 2 DPC on EPYC 9005 [UNVERIFIED-T]). Below that, plain RDIMMs are cheaper per TB and lower-latency. — for EDA teams at fabless startups, genomics cores, SAP HANA operators

**Survives a 2029 glut?:** partially — Cheap DDR5 plus 128-256 GB RDIMM/MRDIMM give 3-6 TB per socket without CXL, so only workloads above the slot ceiling still need it.

**Fatal-flaw candidate:** Big OEMs already sell CXL-ready platforms with the same modules. At 2026 DRAM prices the binding constraint is dollars, not slots, so breaking the CXL ceiling is not the customer's pain point.

*Possible?* yes · *Profitable?* marginal: VAR margins against OEM incumbents · *Doable by this founder?* marginal

*Business-model lenses:* module/appliance (VAR); SaaS (tiering tuning/telemetry)

### C-50 — Rack-Scale CXL Pooling Appliance — ☠ KILLED (R4-NO-WINNING-AXIS: The card's only axis is fleet $/GB from recovering stranded memory, and its own literature says a switch-based design loses money on that axis. Pond (ASPLOS '23) gets ~7% gross DRAM saving at 16 sockets (7-9% on the poster), from emulation on Azure traces, and uses an external memory controller specifically to avoid switch latency. Octopus (Azure plus universities, arXiv 2501.09020) finds CXL switches produce a net server-cost increase and only 3-5.4% net saving for the best switchless topology. Google's HotNets '23 'A Case Against CXL Memory Pooling' argues cabling and switching cost more than multiplexing saves (all via search snippet). For a 16-socket, 12 TB pod, 7-9% is ~$17-22k at the 4Q26 deck and ~$7-9k in the glut, before switch, controllers, cables and a 1-5% slowdown [ESTIMATE]. Mainline Linux (opened, 2026-10-31) still scores Dynamic Capacity, multi-host sharing and fabrics [0], so the dynamic reallocation the saving depends on is unsupported. C-76 was already killed as a duplicate of this card, so this verdict covers the pooling idea in both forms.)

*Sub-branch:* CXL switching / multi-host memory pooling · *Materials sense:* c-capital

**What it is:** A 2-4U memory appliance with a CXL 2.0/3.x switch (XConn Apollo or Panmnesia class) fanning 16-32 hosts into a shared DDR5/DDR4 pool behind Type-3 controllers, plus orchestration software. It is sold to VM-cloud operators to cut stranded memory.

**Why it could work:** Pond showed ~7% gross DRAM saving at 16 sockets (emulated), using a switchless EMC design; switch-based pooling is a net cost increase (Octopus).

**Evidence:** TRL 5 · Rule 1: SUPPORTED
  - [Pond: CXL-Based Memory Pooling Systems for Cloud Platforms (ASPLOS '23) artifact repo](https://github.com/vtess/Pond) — conference, 2023-03. Opened. Microsoft Azure/Virginia Tech CXL pooling paper. The repo holds the CXL-emulation scripts, and the paper preprint is linked at huaicheng.github.io/p/asplos23-pond.pdf (not opened).
  - [Linux CXL Subsystem Maturity Map (mainline, HEAD 2026-10-31)](https://github.com/torvalds/linux/blob/master/Documentation/driver-api/cxl/maturity-map.rst) — industry, 2026-10. Opened. Single-host Type-3 enumeration/HDM decoders are [2] stabilizing. Dynamic Capacity Devices, multi-host sharing and fabrics/G-FAM are [0] known gaps. PMEM GPF/dirty shutdown is [3] mature.
  - [Pond: CXL-Based Memory Pooling Systems for Cloud Platforms (arXiv)](https://arxiv.org/pdf/2203.00241) — conference, 2023-03. (via search snippet) Reduces DRAM needs by 7% with a pool spanning 16 sockets; 8-16 sockets capture most of the benefit; emulation on Azure production servers.
  - [Octopus: Scalable Low-Cost CXL Memory Pooling](https://arxiv.org/html/2501.09020v1) — peer-reviewed, 2025-01. (via search snippet) In simulation, Octopus gives 3-5.4% net server cost savings, while CXL switches give a net cost increase.
  - [A Case Against CXL Memory Pooling (HotNets '23)](https://research.google/pubs/a-case-against-cxl-memory-pooling/) — conference, 2023-11. (via search snippet) Pooling's multiplexing savings are outweighed by the cost of the required cabling and switching, plus complexity and limited utility.

**Capital tier:** T3 | **Time to first revenue:** 36-48 months: switch silicon access, OS support, hyperscaler qualification | **Gross margin estimate:** 30-45%

**US manufacturability:** Switch/controller silicon from TSMC; chassis assembly could be U.S.

**Who is already doing this:** Liqid (composable memory), GigaIO, XConn, Panmnesia (CXL 3.x switch), Unifabrix (status unknown), H3 Platform, Astera Labs, Enfabrica (NVIDIA acqui-hire Sep 2025) [all UNVERIFIED-T]

**Wins on which axis, for which buyer:** Stranded-memory reduction (fleet $/GB) — for Hyperscale and large VM cloud operators

**Survives a 2029 glut?:** no — Savings scale with DRAM price. At -60% a 7-9% fleet saving no longer funds switches, controllers and the latency penalty.

**Fatal-flaw candidate:** The OS is not ready: mainline Linux (2026-10-31) still lists Dynamic Capacity, multi-host sharing and fabrics as [0] known gaps. The only buyers big enough to benefit build their own, and Pond's own result was single-digit-percent savings.

*Possible?* marginal: switches exist (XConn, Panmnesia), but dynamic multi-host capacity has no mainline OS support (DCD/sharing [0]) and switch-based pooling is net-cost-negative in Azure's own Octopus analysis · *Profitable?* no · *Doable by this founder?* no

*Business-model lenses:* module/appliance; fabless->foundry (switch)

### C-51 — Persistent CXL Log Card (post-Optane PMem for WAL/journals) — ☠ KILLED (SCORE<55: Scored 53.0/100 default (rank 32/40), 50.8 moonshot. Weakest: capital 2/5 (T2: card design, power-fail firmware and CXL compliance (12-18 months), then OEM qualification.); time to revenue 2/5 (30-42 months (card 36): SMART needed ~10 months from sampling to compliance alone, and storage/DB OEM design-ins take another 12-24 months.); margin 2/5 (25-40% (mid 30%): DRAM dominates the BOM and an incumbent with Tier-1 OEM channels sets the persistence premium.). Scorer verdicts — founder: SMART/Penguin's NV-CMM already is this card, compliance-listed and sampling at Tier-1 OEMs; this would be a T2 entrant arriving 36 months late into the niche that killed Optane. | vc: Optane's >$7B write-off proves the market is tiny, and Penguin/SMART's NV-CMM is already compliance-listed and sampling to Tier-1 OEMs: an entrant 3 years late with FTO exposure; pass. | veteran: Optane's niche without Optane's volume, and SMART/Penguin's compliance-listed NV-CMM already is this card; a late entrant has nothing new to sell OEMs.)

*Sub-branch:* Tiered memory - persistent CXL tier (NVDIMM-N/MRAM successor) · *Materials sense:* a-material · *Merged from:* B.08, A2.12

**What it is:** A 16-64 GB CXL Type-3 persistent-memory card: DDR5 backed by NAND plus supercapacitors (NVDIMM-N style), or a DRAM front fronted by Everspin STT-MRAM (Chandler AZ) for the hot journal. It is exposed as CXL PMEM with Global Persistent Flush and targets database write-ahead logs and storage-array journals that lost their home when Intel killed Optane PMem.

**Why it could work:** Linux CXL PMEM GPF/dirty-shutdown support is mature [3], so the software path exists. Storage OEMs pay for persistent journal memory: IBM has put Everspin MRAM in every FlashCore generation since 2018, including FCM5 (2026-10). Sub-microsecond durable commits beat NVMe flush latency by 10-100x.

**Evidence:** TRL 7 · Rule 1: SUPPORTED
  - [Linux CXL Subsystem Maturity Map (mainline, HEAD 2026-10-31)](https://github.com/torvalds/linux/blob/master/Documentation/driver-api/cxl/maturity-map.rst) — industry, 2026-10. Opened. Single-host Type-3 enumeration/HDM decoders are [2] stabilizing. Dynamic Capacity Devices, multi-host sharing and fabrics/G-FAM are [0] known gaps. PMEM GPF/dirty shutdown is [3] mature.
  - [IBM uses Everspin MRAM in FlashCore Module 5](https://www.blocksandfiles.com/flash/2026/10/05/ibm-using-everspin-mram-in-5th-gen-flashcore-modules/5300966) — news, 2026-10-05. CROSS-REF (A2.jsonl snippet). Storage OEM builds its own MRAM-backed power-loss journal.
  - [Everspin 1Gb STT-MRAM distributor price](https://www.lcsc.com/product-image/C20342497.html) — industry, 2026. CROSS-REF (A2.jsonl snippet). $102.60 @500 for 1Gb, i.e. ~$821/GB.
  - [Intel 10-Q Q2-2022: Optane wind-down](https://www.sec.gov/Archives/edgar/data/50863/000005086322000030/intc-20220702.htm) — industry, 2022-07. CROSS-REF (A2.jsonl snippet). $559M Optane inventory impairment.
  - [World's First 1 Gb 28 nm STT-MRAM Product - by Everspin](https://www.techinsights.com/blog/memory/worlds-first-1-gb-28-nm-stt-mram-product-everspin) — industry, 2019. 1Gb die 105.1 mm2, cell 0.0396 um2, 9.75 Mb/mm2 on GF 28nm (via search snippet)
  - [IBM and Everspin announce 19TB NVMe SSD with MRAM write cache](https://www.anandtech.com/show/13174) — news, 2018-08. IBM chose MRAM over DRAM+supercaps because supercaps/batteries last only a few years (via search snippet)
  - [SMART Modular Technologies Introduces its Non-Volatile CXL E3.S Memory Module](https://www.nasdaq.com/press-release/smart-modular-technologies-introduces-its-non-volatile-cxl-e3s-memory-module-2025-03) — company, 2025-03. NV-CMM E3.S 2T CXL module sampling to Tier-1 OEMs and offered to enterprise customers and integrators (via search snippet)
  - [Penguin Solutions SMART Modular CXL NV-CMM E3.S 2T Memory Module Achieves CXL Compliance](https://www.businesswire.com/news/home/20260114434969/en/Penguin-Solutions-SMART-Modular-CXL-NV-CMM-E3.S-2T-Memory-Module-Achieves-CXL-Compliance) — company, 2026-01-14. NV-CMM passed CXL compliance testing and is listed on the CXL Consortium Integrators List (via search snippet; ir.penguinsolutions.com DNS-blocked)
  - [CXL Memory Module NV-CMM E3.S (product page)](https://www.penguinsolutions.com/products/smart-modular/cxl-memory-module-nv-cmm-e3s) — company, 2026. CXL 2.0 x8 controller, 2Rx4 DDR4, onboard Energy Source Module that backs DRAM up to NAND on power loss, AES-256, 32GB (via search snippet)

**Capital tier:** T2 | **Time to first revenue:** 30-42 months: card, power-fail firmware and CXL compliance (12-18), then OEM qualification against an incumbent already on the Integrators List (12-24) | **Gross margin estimate:** 25-40%

**US manufacturability:** Board assembly U.S.; Everspin Toggle MRAM is made in Chandler AZ (STT 1Gb via GF Singapore); DRAM/NAND imported

**Who is already doing this:** Penguin Solutions/SMART Modular NV-CMM: CXL 2.0, E3.S 2T, DDR4 with NAND backup and an onboard Energy Source Module, AES-256. 32GB listed, 128GB variant reported. Sampling to Tier-1 OEMs since 2025-03; on the CXL Consortium Integrators List since 2026-01 [REPORTED via snippet]. Samsung CMM-H [UNVERIFIED-T]. NVDIMM-N history at Netlist, Micron, Viking and SMART. IBM builds its own Everspin-MRAM journal into FlashCore (since 2018; FCM5 2026). Kioxia XL-Flash.

**Wins on which axis, for which buyer:** Non-volatility at memory latency (durable commit latency) — for Database vendors (log/commit path), storage-array OEMs (journals), low-latency trading

**Survives a 2029 glut?:** yes — Value is persistence, not $/GB, so the price per card holds. A glut lowers the DRAM BOM (64GB: $1,023 at 4Q26 vs $410 at the $6.40 glut) for the incumbent as much as for an entrant. Volume stays tiny.

**Fatal-flaw candidate:** SMART/Penguin's NV-CMM already is this product (CXL 2.0, DRAM+NAND+energy source, compliance-listed 2026-01, Tier-1 OEM sampling), so an entrant arrives 3+ years late with no OEM qualification and worse DRAM purchasing. The market is tiny: Optane PMem died for lack of volume (>$7B losses), and NVMe with power-loss protection plus group commit is good enough for most WAL. Storage OEMs build journals in-house (IBM FCM MRAM). MRAM at ~$821/GB caps the MRAM variant at a few GB ($821-3,284 of MRAM for 1-4 GB).

*Possible?* yes: SMART/Penguin NV-CMM (CXL 2.0 E3.S, DRAM+NAND+energy source) passed CXL compliance in 2026-01 · *Profitable?* no for a new entrant: the incumbent ships the same card through Tier-1 OEMs, and demand is capped at the Optane PMem niche · *Doable by this founder?* no

*Business-model lenses:* module/appliance; IP licensing (firmware)

### C-52 — LPDDR 'HBM-lite' Memory Chiplet (UCIe/AIB-attached) — ☠ KILLED (SCORE<55: Scored 40.0/100 default (rank 40/40), 41.7 moonshot. Weakest: capital 1/5 (T3: a ~$50-90M program for architecture, tape-out, package qualification and the first design-in.); time to revenue 1/5 (36-48 months (card 42) to the first design-in revenue.); founder-fit 1/5 (A T3 silicon program that needs a veteran SoC, PHY and packaging team from day one.). Scorer verdicts — founder: A $50-90M silicon program selling an extra die-to-die hop that buyers already avoid by licensing LPDDR5X PHYs directly, at only 0.27-0.55 TB/s; not for this founder. | vc: A $50-90M chip program delivering 0.27-0.55 TB/s, under half an HBM3E stack, to buyers who already attach LPDDR5X with Synopsys/Cadence IP: no pull, no founder fit; hard pass. | veteran: A $50-90M chip program delivering under half an HBM3E stack of bandwidth to buyers who already bolt LPDDR5X on directly with Synopsys/Cadence IP; nothing here for this founder.)

*Sub-branch:* HBM alternatives / chiplet memory · *Materials sense:* mixed:b+c

**What it is:** Same, but performance is ~0.27-0.55 TB/s and 128-512 GB per package: 4-8 x64 LPDDR5X-8533 packages at 68.3 GB/s each, the same 512-bit width as NVIDIA Grace (~546 GB/s). 1 TB/s needs ~15 x64 LPDDR5X packages or ~23 LPDDR6 x24 channels at 14.4 Gb/s.

**Why it could work:** HBM takes ~22% of DRAM wafer starts for ~9% of bits and ~3x DDR5's wafer area per bit. HBM4 2027 asks of ~$4.5-4.9/Gb (~$36-39/GB) and allocation to the big GPU makers leave smaller ASIC teams short. LPDDR5X proves the bandwidth-per-pin path (NVIDIA Grace), and open AIB RTL lowers die-to-die IP cost.

**Evidence:** TRL 5 · Rule 1: SUPPORTED
  - [CHIPS Alliance AIB PHY RTL (open die-to-die interface)](https://github.com/chipsalliance/aib-phy-hardware) — industry, 2024-09. Opened. Open-source die-to-die PHY RTL (AIB 1.0/2.0, originally Intel), a royalty-free D2D path for chiplets.
  - [TrendForce via TechNews: HBM share of DRAM wafer starts](https://technews.tw/?p=1565421) — news, 2026. CROSS-REF (p1-market.jsonl snippet). HBM is ~22% of wafer starts in 2026 (30% in 2027) for ~9% of bits.
  - [Micron: HBM-vs-DDR5 silicon gap widening](https://www.tomshardware.com/tech-industry/semiconductors/micron-says-the-silicon-gap-between-hbm-and-ddr5-is-widening-with-every-generation) — news, 2026. CROSS-REF (p1-market.jsonl snippet). HBM takes ~3x the wafer area of DDR5 per bit.
  - [Samsung seeks >3x HBM3E pricing for HBM4](https://www.sammyfans.com/2026/10/02/samsung-seeks-more-than-3x-hbm3e-pricing-for-hbm4/) — news, 2026-10-02. CROSS-REF (p1-market.jsonl snippet). HBM3E ~$1.50/Gb; 2027 HBM4 asks mid-to-high $4/Gb.
  - [TrendForce 2Q26 mobile DRAM contract via China Times](https://wantrich.chinatimes.com/news/20260515900291-420101) — news, 2026-05-15. CROSS-REF (p1-market.jsonl snippet). LPDDR4X +70-75%, LPDDR5X +78-83% QoQ in 2Q26.

**Capital tier:** T3 | **Time to first revenue:** 36-48 months: architecture, tape-out, package qualification, first design-in | **Gross margin estimate:** 40-60% (chiplet at low volume)

**US manufacturability:** GlobalFoundries Malta NY can fab a 12nm-class controller die (rubric 4 at best for the die). Amkor Peoria AZ is logic 2.5D with anchor customers, production ~early 2028, and not open to a small customer (01_LANDSCAPE 6.1 row 21), so packaging and LPDDR5X dies are offshore in practice.

**Who is already doing this:** IP vendors selling UCIe plus LPDDR5X controller/PHY: Synopsys, Cadence, Alphawave (Qualcomm). Eliyan (NuLink D2D). Marvell (custom memory/HBM base dies). Buyers integrating LPDDR directly: Qualcomm AI200 (LPDDR per card), d-Matrix Corsair (LPDDR5X), NVIDIA Grace (512-bit LPDDR5X). Tenstorrent (GDDR6). All [UNVERIFIED-T] except Grace's published width.

**Wins on which axis, for which buyer:** Bandwidth per dollar and allocation-free supply vs HBM for inference ASICs — for AI-inference ASIC startups, edge-AI SoC teams, defense ASIC programs

**Survives a 2029 glut?:** partially — A glut eases HBM allocation and removes the 'can't get HBM' motive, though LPDDR's lower $/GB keeps a cost niche. LPDDR prices themselves rose +70-90% QoQ in 1H26.

**Fatal-flaw candidate:** Serious ASIC teams already integrate LPDDR5X with licensed controller/PHY IP (Synopsys, Cadence, Alphawave), and Qualcomm AI200 and d-Matrix show LPDDR inference without a third-party chiplet [UNVERIFIED-T]. A separate chiplet adds a die-to-die hop and package cost. Its real bandwidth (0.27-0.55 TB/s) is below half an HBM3E stack. A startup needs a ~$50-90M program for a handful of customers, and Amkor AZ is closed to it.

*Possible?* yes: all components ship. The chiplet itself is unbuilt (TRL 5) · *Profitable?* marginal at best: buyers integrate LPDDR IP directly and IP giants own the PHY/controller market · *Doable by this founder?* no

*Business-model lenses:* fabless->foundry; IP licensing

### C-53 — High-Bandwidth Flash (HBF) Weight-Store Module — ☠ KILLED (FACT-COLLAPSE: The card's product, accelerator boards or appliances that pair a GPU/ASIC with HBF stacks, has no attach point open to an outsider. The SanDisk/SK hynix HBF spec (published via OCP in 2026) connects 512GB-class stacks to the processor over UCIe inside the package, at 0.4-3.0 TB/s grades (via search snippet), the same way HBM attaches. Only package owners can integrate it, and those are the card's own named buyers (NVIDIA, AMD, hyperscaler ASIC teams), who buy HBF directly from SanDisk/SK hynix. Samples were promised for 2H26 (no shipment confirmed as of 2026-11) and devices for early 2027. The only way in is a custom accelerator ASIC with CoWoS-class packaging (T3, 48+ months), and the card concedes 'no socket for a small company'.)

*Sub-branch:* HBM alternatives - stacked NAND with HBM-like interface · *Materials sense:* a-material

**What it is:** Accelerator boards or appliances that pair a GPU/ASIC with SanDisk/SK hynix High Bandwidth Flash stacks (TSV-stacked BiCS NAND dies behind an HBM-like interface) to hold read-mostly model weights at ~8-16x HBM capacity per stack. The NAND is made at Kioxia/SanDisk Yokkaichi/Kitakami.

**Why it could work:** Inference weights are read-mostly, and NAND $/GB is ~50-100x below DRAM. NAND is heading to surplus in 2H27 and contract prices were already flat in Oct 2026. SanDisk is diversifying into memory-class products (3D Matrix Memory nearing product specs).

**Evidence:** TRL 4 · Rule 1: SUPPORTED (mechanism); the business premise collapses (no outsider integration seat)
  - [SanDisk Investor Day 2026](https://quartr.com/events/sandisk-corporation-sndk-investor-day-2026_F6lVAkBS) — company, 2026. CROSS-REF (A2.jsonl snippet). SanDisk memory roadmap beyond NAND (3D Matrix Memory nearing product specs).
  - [NAND flat after 21 months while DRAM hits record](https://tech-insider.org/dram-record-high-nand-flat-21-months-october-2026/) — news, 2026-10. CROSS-REF (p1-market.jsonl snippet). NAND contract stopped rising in Oct 2026.
  - [TrendForce 2026-07-30 press release](https://www.trendforce.com/presscenter/news/20260730-13158.html) — industry, 2026-07-30. CROSS-REF (p1-market.jsonl snippet). NAND turns to surplus in 2H27 while the DRAM gap widens.
  - [Sandisk to Collaborate with SK hynix to Drive Standardization of High Bandwidth Flash Memory Technology](https://www.businesswire.com/news/home/20250806259749/en/Sandisk-to-Collaborate-with-SK-hynix-to-Drive-Standardization-of-High-Bandwidth-Flash-Memory-Technology) — company, 2025-08-06. HBF MoU. Samples 2H26, first AI-inference devices early 2027 (via search snippet)
  - [SK hynix and SanDisk reveal first specs for High Bandwidth Flash](https://techradar.com/pro/sk-hynix-and-sandisk-reveal-first-specs-for-high-bandwidth-flash-but-dont-get-too-excited-you-probably-wont-be-able-to-buy-it-anytime-soon) — news, 2026. Spec via OCP: up to 512GB packages (8/16-high), 0.4-3.0 TB/s grades, UCIe connection to the processor; not buyable soon (via search snippet)

**Capital tier:** T3 | **Time to first revenue:** 4+ years: HBF samples reportedly 2H26, devices 2027 [UNVERIFIED-T]; system integration after | **Gross margin estimate:** unknown; 30-50% for a system integrator

**US manufacturability:** None: NAND fabs in Japan, packaging in Asia; integration would happen inside GPU/ASIC packages at TSMC CoWoS.

**Who is already doing this:** SanDisk and SK hynix (MoU to standardize HBF, 2025-08-06; samples 2H26, first AI-inference devices early 2027; spec published via OCP with UCIe attach, up to 512GB 8/16-high, 0.4-3.0 TB/s) [REPORTED]. Samsung and Kioxia reported. Integration only by GPU/ASIC package owners.

**Wins on which axis, for which buyer:** Capacity per package and $/GB vs HBM for read-heavy inference weights — for GPU/ASIC vendors (NVIDIA, AMD, hyperscaler ASIC teams)

**Survives a 2029 glut?:** partially — Its competitor is HBM, not DDR5, but a DRAM/HBM glut narrows the capacity-cost gap that justifies flash's endurance and latency compromises.

**Fatal-flaw candidate:** Integration happens inside GPU/ASIC packages at TSMC, so there is no socket for a small company. NAND endurance rules out write-heavy KV, so HBF is a weights-only niche controlled by memory makers and GPU vendors.

*Possible?* yes for memory makers and GPU/ASIC package owners. No for a board or appliance integrator, because attach is in-package over UCIe · *Profitable?* no for a small entrant · *Doable by this founder?* no

*Business-model lenses:* module/appliance (theoretical)

### C-54 — PIM DIMM Accelerator Servers (UPMEM / AiM) for Scans and Genomics — ☠ KILLED (FACT-COLLAPSE: The integrator needs a merchant PIM supplier, and none is selling. UPMEM, the only vendor that ever sold PIM DIMMs, was acquired by Qualcomm in 2025-06: CB Insights lists it as acquired, and an Oct-2025 arXiv paper calls the platform 'recently acquired by Qualcomm' (both via search snippet). No evidence was found that the DDR4 PIM DIMMs are still sold to third parties. SK hynix still described AiMX as an 'accelerator card prototype' at CES 2026, with no price, launch or named customer (via search snippet). Samsung HBM-PIM and LPDDR5X-PIM are not open-market parts [UNVERIFIED-T]. The card itself rated profitability 'no: no commercial pull beyond research'. The active PrIM repo shows academic use of legacy boards, not a supply chain.)

*Sub-branch:* Processing-in-memory · *Materials sense:* b-process

**What it is:** Servers fitted with UPMEM PIM DIMMs (DDR4 DIMMs with in-order DPUs on each DRAM die) or SK hynix GDDR6-AiM/AiMX cards, sold for memory-bound kernels: genomic read alignment, database scans and filters, recommendation embedding lookups. The aim is less DRAM bandwidth and capacity per unit of work.

**Why it could work:** Moving compute to the DRAM die removes the memory-bus bottleneck. ETH SAFARI's PrIM suite shows large speedups on memory-bound kernels over CPUs on real UPMEM hardware (IEEE Access 2022; exact ratios [UNVERIFIED-T]). Samsung HBM-PIM/LPDDR5X-PIM and SK hynix AiM show vendor interest.

**Evidence:** TRL 7 · Rule 1: SUPPORTED
  - [PrIM benchmarks for UPMEM PIM (ETH SAFARI) + IEEE Access 2022 characterization](https://github.com/CMU-SAFARI/prim-benchmarks) — peer-reviewed, 2026-06. Opened. Real UPMEM PIM hardware (DRAM arrays + in-order DPUs) characterized on memory-bound kernels. Repo active Jun 2026. Paper at ieeexplore.ieee.org/abstract/document/9771457 (seen, not opened).
  - [UPMEM company profile (CB Insights)](https://www.cbinsights.com/company/upmem) — industry, 2026. Lists UPMEM as acquired by Qualcomm, June 2025; total raised ~$13.55M (via search snippet)
  - [UPMEM Unleashed: Software Secrets for Speed (arXiv 2510.15927)](https://arxiv.org/html/2510.15927v1) — peer-reviewed, 2025-10. Describes the UPMEM platform as recently acquired by Qualcomm (via search snippet; arxiv.org DNS-blocked in this session; preprint, not peer-reviewed)
  - [News posts matching #AiMX (TechPowerUp)](https://techpowerup.com/news-tags/AiMX) — news, 2024. AiMX shown as an upgraded prototype at OCP 2024. A search summary also described AiMX at CES 2026 as an 'accelerator card prototype' without naming the page (via search snippet)

**Capital tier:** T1 | **Time to first revenue:** n/a: no supplier | **Gross margin estimate:** 20-35%

**US manufacturability:** None for PIM silicon (foreign DRAM-process partners); U.S. integration only

**Who is already doing this:** UPMEM (Grenoble) was acquired by Qualcomm in 2025-06 [REPORTED via snippet: CB Insights; arXiv 2510.15927]; no evidence of continued merchant sales. SK hynix AiMX is still a prototype (CES 2026). Samsung HBM-PIM/LPDDR5X-PIM are not open-market [UNVERIFIED-T]. NeuroBlade [UNVERIFIED-T]. GSI Gemini APU (see C-37).

**Wins on which axis, for which buyer:** Throughput and energy per byte moved for memory-bound kernels — for Genomics cores, analytics/database operators

**Survives a 2029 glut?:** partially — The value is bandwidth and energy, not $/GB, but cheap DRAM removes the 'less RAM per job' argument.

**Fatal-flaw candidate:** Hard programming model, single-vendor supply risk, and DDR4-based UPMEM DIMMs stranded as servers go DDR5-only. GPUs with HBM run the same kernels with a mature CUDA stack.

*Possible?* no as a business: research hardware exists, but there is no merchant PIM supply to integrate · *Profitable?* no: no commercial pull beyond research · *Doable by this founder?* no

*Business-model lenses:* module/appliance; university/lab patent license

### C-55 — Analog CIM Edge Module (DRAM-free defense edge inference)

*Sub-branch:* Compute-in-memory (analog/charge-domain) · *Materials sense:* b-process

**What it is:** Rugged M.2/PCIe edge-AI modules built on U.S.-designed analog CIM accelerators (Mythic M1076/M2000, EnCharge EN100, Sagence), sold to U.S. drone/ISR integrators with U.S. assembly and environmental qualification. External DRAM is eliminated only on Mythic-class parts running models that fit on-chip. EnCharge EN100 modules carry up to 128 GB of LPDDR (272 GB/s).

**Why it could work:** Weight-stationary in-memory compute removes most DRAM traffic and BOM. Edge boxes were hit by LPDDR4X/5X contract hikes of +70-90% QoQ in 1H26, and defense buyers value W/inference and a U.S.-assembled supply chain.

**Evidence:** TRL 7 · Rule 1: SUPPORTED
  - [IBM Analog Hardware Acceleration Kit](https://github.com/IBM/aihwkit) — industry, 2026-10. Opened. Analog in-memory computing toolkit, still labelled 'beta' in Oct 2026. AIMC is research-grade.
  - [TrendForce 2Q26 mobile DRAM contract via China Times](https://wantrich.chinatimes.com/news/20260515900291-420101) — news, 2026-05-15. CROSS-REF (p1-market.jsonl snippet). LPDDR4X +70-75%, LPDDR5X +78-83% QoQ in 2Q26.
  - [EnCharge AI Announces EN100, First-of-its-Kind AI Accelerator for On-Device Computing](https://www.businesswire.com/news/home/20250529108055/en) — company, 2025-05-29. EN100 M.2: 200+ TOPS in 8.25 W. PCIe: 4 NPUs, ~1 POPS. Up to 128 GB LPDDR at 272 GB/s (via search snippet)
  - [Mythic to challenge AI's GPU pantheon with energy efficiency and oversubscribed $125M raise](https://www.hpcwire.com/off-the-wire/mythic-to-challenge-ais-gpu-pantheon-with-energy-efficiency-and-oversubscribed-125m-raise/) — company, 2025-12. Mythic oversubscribed $125M raise. The date comes from aggregators; the body was not seen (via search snippet)
  - [Mythic Launches Second AI Chip](https://www.eetasia.com/mythic-launches-second-ai-chip/) — news, 2021. M1076: 25 TOPS INT8 at ~3 W, weights held on-chip (via search snippet)
  - [Mythic Raises $13 Million to Bring Its Next generation Analog Computing Solution to Market](https://www.businesswire.com/news/home/20230309005131/en/Mythic-Raises-$13-Million-to-Bring-Its-Next-generation-Analog-Computing-Solution-to-Market) — company, 2023-03-09. Rescue round after running out of cash in Nov-2022; M2000 next-gen. Search summary says M1076 shipped to customers including Lockheed Martin; page attribution unconfirmed (via search snippet)

**Capital tier:** T1 | **Time to first revenue:** 18-30 months: vendor partnership, ruggedized module, SBIR/defense pilot | **Gross margin estimate:** 25-40%

**US manufacturability:** Chips designed in the U.S. (Mythic Austin, EnCharge Santa Clara), die fabbed offshore [UNVERIFIED-T], module assembly and environmental test at a U.S. EMS (rubric 3: U.S. assembly of imported die).

**Who is already doing this:** Mythic (Austin) sells M.2/PCIe M1076 cards directly. It reportedly raised $125M in 2025-12 and reportedly acquired videantis in 2026-05 [UNVERIFIED]. EnCharge AI (EN100 M.2 and 4-NPU PCIe card). Sagence AI. IBM Research. Digital DRAM-free competitor Hailo-8 (M.2, no external DRAM) [UNVERIFIED-T]. NVIDIA Jetson, Qualcomm. Rugged-module houses (Aitech, Curtiss-Wright, Mercury) [UNVERIFIED-T].

**Wins on which axis, for which buyer:** W per inference on U.S.-designed silicon (EnCharge claims up to ~20x perf/W, a vendor claim). DRAM-free BOM only for small CNN-class models on Mythic M1076-class parts. — for Defense UAS/ISR integrators, industrial machine vision

**Survives a 2029 glut?:** yes — The axis is power, not DRAM price, so the glut weakens only the secondary 'avoid LPDDR cost' argument.

**Fatal-flaw candidate:** The chip vendors already sell M.2/PCIe modules (Mythic ships to Lockheed Martin), so the integrator adds only ruggedization and qualification: C-67's rugged-module economics with a different chip, and not a memory business. 'DRAM-free' holds only on Mythic-class parts for small models. EN100 needs LPDDR. Digital NPUs with mature toolchains (Hailo-8, Jetson) own edge AI, and the integrator depends on venture-funded chip vendors (Mythic nearly folded in 2022-23).

*Possible?* yes: Mythic M1076 shipping; EnCharge EN100 announced 2025-05 · *Profitable?* marginal · *Doable by this founder?* marginal

*Business-model lenses:* module/appliance; defense-first niche

### C-56 — TrustedCXL: U.S.-Provenance DDR4 CXL Expander for DoD/DOE HPC — ☠ KILLED (R1-UNSUPPORTED: The core value claim has no evidence. The card says DoD HPCMP centers and NNSA labs will pay a premium for CXL expanders because they carry U.S.-fabbed Manassas DDR4. C-70 was killed for this same claim (batch_10, R1). The canonical landscape finds no U.S.-origin memory premium: TAA treats Korean, Taiwanese and Japanese DRAM as compliant, COTS is BAA-exempt, and memory pays 0% under Section 232 (01_LANDSCAPE 0 item 7, 7.3). The card's buyer evidence is misread. The Everspin $40M deal is an Amentum subcontract to stand up on-shore Toggle-MRAM process capability, not a premium on COTS DRAM. The provenance is thin too. Micron's back-end hubs are Malaysia and India, the controller is TSMC-made, Manassas output goes first to Micron's auto Strategic Customer Agreements (logged snippets), and SMART/Penguin already ships DDR4 behind CXL. Bandwidth-bound HPC nodes are the worst fit for a DDR4-over-CXL tier.)

*Sub-branch:* CXL memory expansion - defense-first provenance · *Materials sense:* c-capital

**What it is:** A CXL Type-3 expander built from Micron Manassas-made 1-alpha DDR4 (the U.S.-fabbed DRAM ramping since May 2026 for defense, aero and auto) and a U.S.-HQ DDR4-capable controller (Microchip SMC 2000-class), assembled and tested at a DMEA-accredited U.S. trusted EMS. It is sold to DoD HPCMP centers, NNSA labs and defense primes needing capacity with TAA/Buy-American and trusted-supply provenance.

**Why it could work:** Manassas quadruples DDR4 wafer supply, with qualified output by end-2026, aimed at exactly these buyers. The DoD supply chain already pays for on-shore memory capability (Amentum's $40M Everspin MRAM deal). DDR4 behind CXL lets DDR5-only HPC nodes consume U.S.-fabbed DRAM.

**Evidence:** TRL 6 · Rule 1: UNSUPPORTED (value claim): no evidence any HPC/defense buyer pays a premium for U.S.-fabbed DRAM. 01_LANDSCAPE 7.3 finds none
  - [Micron advances Made-in-America memory in Virginia](https://www.hpcwire.com/off-the-wire/micron-advances-made-in-america-memory-with-manufacturing-expansion-in-virginia) — company, 2026-05-22. CROSS-REF (p1-fabs.jsonl snippet). Manassas 1-alpha DDR4/LP4 for defense/aero/auto/industrial; 4x DDR4 wafer supply; qualified output by end-2026.
  - [Everspin $40M MRAM deal for defense memory](https://electronics360.globalspec.com/article/23702/everspin-earns-40-million-mram-deal-for-defense-memory-services) — news, 2026-04. CROSS-REF (A2.jsonl snippet). The DoD supply chain pays for on-shore memory capability.
  - [Linux CXL Subsystem Maturity Map (mainline, HEAD 2026-10-31)](https://github.com/torvalds/linux/blob/master/Documentation/driver-api/cxl/maturity-map.rst) — industry, 2026-10. Opened. Single-host Type-3 enumeration/HDM decoders are [2] stabilizing. Dynamic Capacity Devices, multi-host sharing and fabrics/G-FAM are [0] known gaps. PMEM GPF/dirty shutdown is [3] mature.

**Capital tier:** T2 | **Time to first revenue:** 30-36 months: SBIR Phase I/II, trusted-EMS qualification, first lab buy | **Gross margin estimate:** 35-50%

**US manufacturability:** U.S. wafer only. Micron's assembly/test hubs are Malaysia and India (TrendForce 2026-05-27, via snippet), so Manassas die are very likely packaged offshore. The controller is TSMC-made. Module assembly could be U.S.

**Who is already doing this:** Micron (direct to defense; Manassas output committed to Strategic Customer Agreements with auto Tier-1s first, via Counterpoint snippet). SMART/Penguin (NV-CMM already puts DDR4 behind a CXL 2.0 controller in E3.S; defense memory line). Mercury, Netlist. Microchip SMC 2000 [UNVERIFIED-T].

**Wins on which axis, for which buyer:** Supply security/provenance and lifecycle length — for DoD HPC Modernization Program centers, DOE/NNSA labs, defense-prime on-prem HPC

**Survives a 2029 glut?:** yes — The provenance premium does not depend on price, and Manassas DDR4 serves long-lifecycle buyers whatever DDR5 does. Volume stays small.

**Fatal-flaw candidate:** The controller is fabbed in Taiwan, so 'all-U.S.' is only partly true. Buyers are few and slow (FAR procurement), and Micron/SMART can serve them directly. Manassas DDR4 is allocated to existing auto/defense customers first.

*Possible?* unknown: Micron sells Manassas parts only through distribution, with no public fab-of-origin SKU [UNVERIFIED]. Output prioritized to SCA customers · *Profitable?* no: no evidenced premium, tiny FAR-paced volume · *Doable by this founder?* marginal: only as an SBIR-led partnership

*Business-model lenses:* defense-first niche; module/appliance; SBIR/STTR (non-dilutive start)

### C-57 — Memory-Fabric SuperNIC (Ethernet-attached DRAM for GPUs) - acquired away — ☠ KILLED (R4-NO-WINNING-AXIS: The only independent product of this kind is gone. Enfabrica's ACF-S/EMFASYS used CXL controllers to pool up to 18 TB behind an Ethernet SuperNIC, and NVIDIA took it in 2025-09 for a reported >$900M in cash and stock, hiring the CEO and staff and licensing the technology (Blocks & Files, StorageNewsletter, via search snippet). For the named buyer (hyperscalers and GPU clouds), a new custom ASIC wins no axis. Commodity RDMA NICs, open-source Mooncake Transfer Engine/NIXL and CXL-backed memory servers already deliver GPU-reachable capacity per dollar (the card's own evidence, productized as C-45). NVIDIA owns the silicon version and bundles it with ConnectX/BlueField and Dynamo. An entrant spends a T3 (~$50M+) program and 4+ years just to reach parity. None of the card's three sources shows the silicon mechanism; all are software.)

*Sub-branch:* Far memory over RDMA / custom memory-fabric silicon · *Materials sense:* c-capital

**What it is:** A custom NIC/switch ASIC that attaches pools of commodity DDR5 (behind CXL controllers) to GPU servers over 800G-3.2T Ethernet/RDMA, giving each GPU tens of TB of 'elastic' memory for KV cache and weights. This is the Enfabrica ACF-S/EMFASYS concept, taped out at TSMC.

**Why it could work:** GPUs need far more memory than HBM supplies (KV for a 128k Llama-70B context is 40 GiB at BF16). Ethernet/RDMA reloads a 128k context in ~0.5 s vs ~41 s recompute, and commodity DDR5 at ~$26/GB beats HBM-in-GPU at ~$180-250/GB.

**Evidence:** TRL 6 · Rule 1: SUPPORTED (mechanism, via Enfabrica's EMFASYS announcement); none of the card's own cited evidence covers the silicon
  - [Mooncake README + Mooncake Store deployment guide (Kimi serving platform)](https://github.com/kvcache-ai/Mooncake) — company, 2026-11. Opened. KV-cache-centric disaggregation lets Kimi handle 75% more requests within SLO. Store has CXL-aware allocation (--enable_cxl, /dev/dax, --allocation_strategy=cxl). Integrated into vLLM (May 2026) and TensorRT-LLM (Oct 2026).
  - [vLLM KV Offloading Usage Guide](https://github.com/vllm-project/vllm/blob/main/docs/features/kv_offloading_usage.md) — industry, 2026-11. Opened. CPU host memory is the primary KV offload tier, and secondary tiers are staged through it. Host DRAM capacity is mandatory for KV tiering.
  - [Meta llama-models sku_list.py](https://github.com/meta-llama/llama-models) — company, 2025-10. Opened. Llama-3.1 70B has 80 layers and 8 KV heads with head_dim 128, which gives 320 KiB/token KV at BF16 (40 GiB at 128k context).
  - [Nvidia buys Enfabrica](https://blocksandfiles.com/2025/09/19/nvidia-buys-enfabrica/) — news, 2025-09-19. NVIDIA hires CEO Rochan Sankar and staff and licenses Enfabrica technology for >$900M cash and stock; EMFASYS pools up to 18 TB via CXL controllers (via search snippet)
  - [Nvidia swallowed Enfabrica for $900 million](https://www.storagenewsletter.com/2025/09/30/nvidia-swallowed-enfabrica-for-900-million/) — news, 2025-09-30. Corroborates the ~$900M deal (via search snippet)

**Capital tier:** T3 | **Time to first revenue:** 4+ years for a new entrant | **Gross margin estimate:** 60%+ for merchant silicon if it wins

**US manufacturability:** TSMC silicon; U.S. design only

**Who is already doing this:** Enfabrica (EMFASYS, up to 18 TB of CXL-pooled memory). Team hired and technology licensed by NVIDIA for a reported >$900M, 2025-09 [REPORTED via snippet]. NVIDIA (ConnectX/BlueField + Dynamo). Astera Labs, Broadcom, Marvell. Mooncake Transfer Engine/NIXL over standard RDMA.

**Wins on which axis, for which buyer:** GPU-reachable memory capacity per dollar — for Hyperscalers and GPU cloud builders

**Survives a 2029 glut?:** partially — Cheaper DRAM makes pools cheaper, but the silicon economics depend on design wins at NVIDIA-scale customers, not DRAM price.

**Fatal-flaw candidate:** The leading independent attempt was absorbed by NVIDIA, and standard RDMA NICs plus open-source software (Mooncake Transfer Engine, NIXL) deliver most of the benefit. There is no room for a new custom-silicon entrant.

*Possible?* yes: EMFASYS was announced and demonstrated before NVIDIA absorbed it · *Profitable?* no for a new entrant · *Doable by this founder?* no

*Business-model lenses:* fabless->foundry

## C. Manufacturing & supply chain (U.S.) (15 cards)

### C-58 — Legacy-DRAM fab in the U.S. on a licensed 25-46nm process (tempting, dead) — ☠ KILLED (R3-FAB/T4: The card is a new U.S. 300mm DRAM fab: about 20k wpm on a licensed 25-46nm flow, with $2.0-3.5B of capex by its own model. That is T4, which mission rule 3 and A-11 forbid. It also loses on its only axis. Micron Manassas has shipped 1-alpha DDR4/LPDDR4 to the same long-lifecycle buyers since 2026-05-22 at ~2.7x the bits per wafer. The card's own $5.5-7.8/GB cost matches or exceeds the $7.2/GB A-05 glut DDR4 price it would meet on landing (~2031). The licensable legacy-flow route is going to Micron too: Micron signed to buy PSMC's 25/38nm-capable Tongluo fab for $1.8B, and PSMC is taking a Micron 1Y license (via search snippet).)

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
  - [Micron finds a way to make more DRAM with $1.8bn chip plant purchase](https://www.theregister.com/2026/01/20/micron_powerchip_fab_acquisition/) — news, 2026-01-20. Micron signed an LOI to buy PSMC's Tongluo P5 300mm fab for $1.8B cash, completion expected 2Q26 (closing not confirmed in results); PSMC to join Micron's DRAM supply chain (via search snippet)
  - [Micron Acquires PSMC Fab in Tongluo, Taiwan](https://www.all-about-industries.com/micron-acquires-psmc-fab-in-tongluo-taiwan-a-5efad0a188c7b546054c4d0c2a7c8e81/?cflt=rel) — news, 2026-01. PSMC's existing DRAM capacity is 25nm/38nm (TrendForce); PSMC expected to receive a Micron 1Y license; PSMC scaling back non-AI business and phasing out low-margin products (via search snippet)

**Capital tier:** T4 | **Time to first revenue:** ~6 years (license + shell + tool install + yield ramp + customer qualification), i.e. ~2031, after the A-05 glut | **Gross margin estimate:** 60-65% at 2026 prices; ~0% in the A-05 glut ($7.2/GB vs $5.5-7.8/GB cost); deeply negative in a 2023-like trough ($1.30/GB)

**US manufacturability:** No host. No U.S. foundry has a DRAM capacitor module; the only U.S. DRAM fab is Micron Manassas Fab 6 (captive). 150/200mm distressed sites (Akoustis Canandaigua NY, Wolfspeed Durham NC, Microchip Tempe) cannot run competitive DRAM [UNVERIFIED-training site status].

**Who is already doing this:** Micron Manassas VA (1-alpha DDR4/LP4 since 2026-05-22, $275M CHIPS). Micron is also absorbing PSMC's Tongluo P5 fab ($1.8B LOI, Jan-2026), and PSMC is taking a Micron 1Y license. Winbond, Nanya (Taiwan); CXMT (China).

**Wins on which axis, for which buyer:** Supply security and U.S. origin for long-lifecycle DDR3/DDR4 — for Defense, automotive, industrial and medical OEMs needing DDR4 into the 2030s

**Survives a 2029 glut?:** no — Cost $5.5-7.8/GB (5-yr depreciation) vs $7.2/GB A-05 DDR4 and $1.30/GB 2023 trough; Micron's 1-alpha gets ~2.7x the bits per wafer, so the new fab is the marginal, highest-cost producer when prices fall.

**Fatal-flaw candidate:** Micron is already doing exactly this at Manassas on a denser node with CHIPS money, so a licensed 25-46nm U.S. fab would be the highest-cost producer, landing around 2031, after the glut - a T4 bet with no edge.

*Possible?* yes - Winbond/Nanya/PSMC/CXMT prove the process; no U.S. host exists · *Profitable?* no - high-cost producer arriving into a glut against Micron Manassas · *Doable by this founder?* no - billions of capital and a fab team

*Business-model lenses:* fabless->foundry (inverted: own fab), IP licensing (inbound)

### C-59 — U.S.-HQ fabless long-lifecycle DRAM brand on Taiwanese foundry wafers — ☠ KILLED (R4-NO-WINNING-AXIS: The card's business is a U.S.-based fabless DRAM brand selling DDR4/LPDDR4 with long-term support on foundry or KGD silicon. Alliance Memory already runs exactly that model. It describes itself as a fabless maker of pin-for-pin drop-in DRAM/SRAM with long-term support, and its DDR4 8Gb AS4C1G8D4 is in distribution (via search snippets). Intelligent Memory, Etron and Zentel do the same. A newcomer sells the same lifecycle axis with no track record, ~$15M of NRE and first revenue at 36-48 months, past the 36-month ceiling, so the named industrial/avionics buyer gets worse price, availability and longevity credibility. The supply premise is also weakening: PSMC, the named DRAM foundry, is selling its Tongluo fab to Micron ($1.8B LOI, Jan-2026), taking a Micron 1Y license and phasing out low-margin legacy products (via search snippet).)

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
  - [Micron finds a way to make more DRAM with $1.8bn chip plant purchase](https://www.theregister.com/2026/01/20/micron_powerchip_fab_acquisition/) — news, 2026-01-20. Micron signed an LOI to buy PSMC's Tongluo P5 300mm fab for $1.8B cash, completion expected 2Q26 (closing not confirmed in results); PSMC to join Micron's DRAM supply chain (via search snippet)
  - [Micron Acquires PSMC Fab in Tongluo, Taiwan](https://www.all-about-industries.com/micron-acquires-psmc-fab-in-tongluo-taiwan-a-5efad0a188c7b546054c4d0c2a7c8e81/?cflt=rel) — news, 2026-01. PSMC's existing DRAM capacity is 25nm/38nm (TrendForce); PSMC expected to receive a Micron 1Y license; PSMC scaling back non-AI business and phasing out low-margin products (via search snippet)
  - [Alliance Memory line card](https://www.ibselectronics.com/manufacturers/alliance-memory/?page=1) — other, unknown. Fabless legacy/new memory, pin-for-pin drop-in replacements, long-term support; DDR4 8Gb AS4C1G8D4-75BCN listed (via search snippet)
  - [Introducing our partner Alliance Memory](https://www.alantys.com/introducing-our-partner-alliance-memory/) — other, unknown. Up to 10 years of product support (reseller claim); stock in U.S., Shanghai and Taiwan (via search snippet)

**Capital tier:** T2 | **Time to first revenue:** 36-48 months (die design or license, foundry tape-out, JEDEC qualification, design-ins at industrial OEMs) | **Gross margin estimate:** 35-70% from 2026 to the A-05 glut; negative in a 2023-like trough

**US manufacturability:** Essentially none: wafers in Taiwan (PSMC Hsinchu/Tongluo [UNVERIFIED-training]), packaging and test in Asia. TAA-compliant through Taiwan wafer origin; cannot claim 'Made in USA'.

**Who is already doing this:** Alliance Memory (U.S.-based fabless legacy DRAM brand; 'long-term support'; DDR4 8Gb AS4C1G8D4 in distribution; stock in U.S./Shanghai/Taiwan), Intelligent Memory, Etron, Zentel, ISSI. PSMC's DRAM foundry capacity is shifting toward Micron (Tongluo sale, 1Y license).

**Wins on which axis, for which buyer:** none vs incumbents: the same lifecycle/supply-security axis Alliance Memory and Intelligent Memory already sell, with no track record and worse wafer access — for Industrial-PC, networking, medical-imaging and avionics OEMs with 10-20-year product lives

**Survives a 2029 glut?:** partially — Longevity contracts are sticky, but CXMT/Nanya/Winbond backfill collapses legacy ASPs; a foundry customer is first cut in a shortage and only cheap in a glut.

**Fatal-flaw candidate:** This is Alliance Memory's business model with no history, ~$15M NRE and 36-48 months to revenue. Its named foundry (PSMC) is pivoting its DRAM capacity to Micron and phasing out low-margin legacy work, so a newcomer gets wafers only after prices collapse.

*Possible?* yes technically; newcomer wafer supply doubtful as PSMC's DRAM capacity moves to Micron · *Profitable?* marginal - margins depend on wafer allocation the newcomer will not get in a shortage · *Doable by this founder?* no - T2 hardware program with Taiwan-centric operations

*Business-model lenses:* fabless->foundry

### C-60 — 'Assembled in USA' commodity DDR4/DDR5 module brand (tempting, dead) — ☠ KILLED (R4-NO-WINNING-AXIS: The card itself gives wins_axis as 'None that is paid for'. Per 01_LANDSCAPE: U.S. assembly adds $8.63 per 64GB RDIMM, 0.7% of a $1,300 contract module (4.2). TAA treats Korean and Taiwanese DRAM as compliant, Section 232 charges memory 0%, and the FTC allows only 'Assembled in USA' on foreign die (7.3). Without die allocation the brand buys components at street prices and competes with Kingston, PNY and the Taiwanese module houses at a 5-15% margin. Landscape 10.2 lists this path as closed, and C-70, the all-domestic variant, was already killed.)

*Sub-branch:* U.S. module assembly · *Materials sense:* none

**What it is:** Buy packaged DRAM components through franchised distribution or SpecTek, SMT them onto JEDEC UDIMM/SODIMM/RDIMM boards at a U.S. EMS line, and sell a U.S.-assembled module brand into the consumer and federal gap left by Crucial's exit.

**Why it could work:** Crucial left consumer modules (announced 2025-12-03), retail DDR5 sits near $18/GB, patriotic and federal buyers exist, and the Buy American Act gives a 20-30% (DoD 50%) price-evaluation preference on small buys under the TAA threshold [UNVERIFIED-training].

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [Micron announces exit from Crucial consumer business](https://www.storagenewsletter.com/2025/12/05/micron-announces-exit-from-crucial-consumer-business/) — news, 2025-12-05. Micron exited consumer modules (announced 2025-12-03), leaving no U.S.-HQ first-party consumer module brand (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Memory prices surging by 90% from 4Q 2025 (Counterpoint via EE Times Asia)](https://www.eetasia.com/memory-prices-surging-by-90-from-4q-2025/) — news, 2026-01. 64GB RDIMM contract $450 (4Q25) to >$900 (1Q26): DRAM die dominates module cost (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [DDR5 server memory price tracker 2026 (ServNet)](https://www.servnetuk.com/research/ddr5-server-memory-price-tracker-2026) — industry, 2026-08. Street 64GB DDR5 RDIMM ~$2,064 (Aug 2026), ~$32/GB (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [PC DRAM 1Q26: prices to surge over 80% on server supply prioritization (TrendForce abstract)](https://www.trendforce.com/research/download/RP260114IU) — industry, 2026-01-14. DRAM supply prioritized to strategic OEMs while module makers are limited (abstract only) (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [What U.S. tariff push means for Korea's semiconductor industry](https://www.koreatimes.co.kr/opinion/20260915/what-us-tariff-push-means-for-koreas-semiconductor-industry) — news, 2026-09-15. Korean memory excluded from Section 232 phase 1: no tariff-created U.S.-origin premium for memory today (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)

**Capital tier:** T1 | **Time to first revenue:** 6-12 months only at street-priced components. Contract-price die allocation is unavailable to a new module brand in 2026 (TrendForce: supply prioritized to strategic OEMs) | **Gross margin estimate:** 5-15% (commodity module house norm), higher only from inventory revaluation in an upswing

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

**Why it could work:** As the card says, plus a caveat: Micron's Manassas fab now makes 1-alpha DDR4/LPDDR4 for auto, industrial, medical and defense buyers. That reduces LTB need for Micron-designed parts, so demand is concentrated in Samsung/SK hynix DDR4 and DDR3/DDR3L EOLs.

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [Response measures to Samsung DDR4 IC EOL announcement (Advantech)](https://www.advantech.com/en/resources/news/response-measures-to-samsung-ddr4-ic-eol-announcement) — company, 2025. Industrial-PC maker tells customers DDR4 supply runs to ~end-2026 and to avoid Samsung DDR4 in new designs: long-lifecycle buyers are actively managing EOL (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Memory shortage watch: DDR3L/DDR4, May 2026 (Findchips)](https://blog.findchips.com/memory-shortage-watch-ddr3l-ddr4-may-2026/) — industry, 2026-05. Zero authorized stock of a mainstream Micron DDR4 part at Newark, Avnet and Mouser; only independent-market stock at a premium (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Micron ramps US-made DDR4 production in Virginia (eeNews Europe)](https://www.eenewseurope.com/en/micron-ramps-us-made-ddr4-production-in-virginia/) — news, 2026-05. DDR4 buffers at auto/industrial customers fell from 31+ weeks to 6-8 weeks (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [DDR4 exit timeline unfolds for top memory makers](https://www.trendforce.com/news/2025/07/09/news-ddr4-exit-timeline-unfolds-for-top-memory-makers-plans-for-samsung-sk-hynix-and-micron) — news, 2025-07-09. Samsung, SK hynix and Micron DDR4 EOL schedules (last orders 2025, final shipments 2025-26) (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Samsung, SK hynix reportedly delay phase-out to 2026 as DDR4 becomes unexpected cash cow](https://www.trendforce.com/news/2025/09/02/news-samsung-sk-hynix-reportedly-delay-phase-out-to-2026-as-ddr4-becomes-unexpected-cash-cow/) — news, 2025-09-02. Majors extended DDR4 only into 2026; Micron issued DDR4 EOL notices June 2025 (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Long-Term Packaging for Electronic Components](https://www.semitron.de/en/test-house-services/long-term-packaging/) — company, unknown. Nitrogen-purged long-term packaging; accepts products from customer supply sources (via search snippet)
  - [Astute Group long-term storage](https://www.astutegroup.com/?p=47448) — company, 2022-10-25. Humidity- and nitrogen-controlled storage with access control (via search snippet)
  - [Micross Technical Booklet: Long-Term Storage](https://shop.micross.com/pdf/Micross_Technical_Booklet-Long-Term_Storage_Can_o_Worms.pdf) — company, unknown. Incumbent die banker publishes long-term-storage guidance (via search snippet)
  - [Super Dry Totech expands long-term storage solutions offering](https://circuitsassembly.com/ca/current/33568-super-dry-totech-expands-long-term-storage-solutions-offering.html) — news, unknown. Dry-storage systems OEMs can run in-house (via search snippet)
  - [IEC 62435-4 Long-term storage of electronic semiconductor devices: Storage](https://www.vde-verlag.de/iec-normen/preview-pdf/info_iec62435-4{ed1.0}b.pdf) — standard, unknown. Long-term storage practice standardized, incl. nitrogen positive-pressure storage (via search snippet)

**Capital tier:** T1 | **Time to first revenue:** 9-12 months for paid LTB-sizing software pilots; 15-18 months for the first consignment storage contract (insurance, quality system, first OEM LTB actually placed) | **Gross margin estimate:** negative below ~8 OEMs; ~27% at 10 OEMs ($7.5M under management); ~70% only at 25 OEMs ($25M), realistically year 4+

**US manufacturability:** A 2,000-4,000 sq ft ESD- and climate-controlled vault on the East Coast; no fab dependency; U.S.-made DDR4 from Micron Manassas can be the stored part where OEMs want domestic origin.

**Who is already doing this:** Rochester Electronics (die/wafer banking, Newburyport MA), Micross (die banking; long-term storage guidance), Semitron (DE, nitrogen long-term packaging of customer-supplied stock), Astute Group (nitrogen/humidity-controlled storage), Super Dry/Totech (OEM in-house dry-storage systems), distributor bonded inventory (Arrow, Avnet), HTV (DE); lifecycle data from SiliconExpert and Z2Data

**Wins on which axis, for which buyer:** Lifecycle length / supply security — for Mid-size OEMs with 10-30-year field lives (industrial PCs, rail signaling, grid-protection relays, medical imaging, avionics retrofit) too small for Rochester's re-creation programs

**Survives a 2029 glut?:** yes — Demand is EOL-driven, not price-driven; in a glut OEMs can afford bigger last-time buys, which raises inventory under management.

**Fatal-flaw candidate:** Trust, scale and cheap substitutes. OEMs hand $0.5-2M of critical inventory only to an insured vault with a record. Incumbents (Rochester, Micross, distributor bonded stock, Semitron/Astute) already store parts. An OEM can buy an N2 dry cabinet for ~$5k and store in-house, which caps the 4%/yr fee. Breakeven needs ~8-10 OEMs.

*Possible?* yes - component long-term storage and die banking exist · *Profitable?* marginal-to-no until ~10+ OEMs; ~27% GM at 10 · *Doable by this founder?* marginal - software-first start is feasible; the vault needs a partner or hire

*Business-model lenses:* SaaS + recert/brokerage (storage service), defense-first niche optional

### C-62 — ProvenRAM: graded, serialized recovered server RDIMMs — ☠ KILLED (RED-TEAM: DD1 (Provenance & Recertified Memory) was KILLED by the four-persona red team: The three FATAL objections hold: the named core buyer (OEM-compatible module makers) already knows its die source from POs, CoCs and package top marks and may self-certify under the proposed FAR rule, and resellers may rely on that free certificate. The die-source library was sampled from the wrong population (old OEM DDR4), keyed wrongly (module P/N) and replicable, so the moat is gone; the C-85 predictive subscript See 05_REDTEAM.md (DD1) and 04_DEEPDIVES/provenance-recert.md §14.)

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
  - [i2c-tools mirror: eeprom/decode-dimms](https://github.com/mozilla-b2g/i2c-tools) — code, 2018-09-27. Opened via git clone. decode-dimms prints 'Assembly Serial Number' and 'DRAM Manufacturer' from SPD, so a serial-keyed ledger is commodity code
  - [eBay listing: used Samsung 32GB 2Rx4 PC4-2933Y RDIMM](https://www.ebay.com/itm/405909777866) — listing, unknown. Asking $24 (asking, not sold; date unclear) (via search snippet)
  - [eBay product page: Samsung 32GB PC4-23400 RDIMM](https://www.ebay.com/p/22059250442) — listing, unknown. Asking $225 for 32GB (via search snippet)
  - [Samsung 32GB 2Rx4 PC4-2933Y-R refurbished](https://pcserverandparts.com/samsung-32gb-2rx4-pc4-2933y-r-ddr4-ecc-rdimm-memory-m393a4k40db2-cvfby-refurbished/) — listing, 2026. Refurbished 32GB listed at $318.99 (via search snippet)
  - [1X 32GB PC4-2933Y 2Rx4 Micron MTA36ASF4G72PZ-2G9](https://www.ubbcentral.com/store/item/1X-32GB-PC4-2933Y-2Rx4-Crucial-Micron-MTA36ASF4G72PZ-2G9-ECC-REG-23400_166719454663.html) — listing, unknown. Used 32GB at $46 each, 46 available, date unclear (via search snippet)

**Capital tier:** T0 | **Time to first revenue:** 2-4 months (first ITAD lot, test bench, eBay and two B2B accounts) | **Gross margin estimate:** 17-32% contribution in 2026 if ITAD lots can be bought at ~60% of resale (buy side UNVERIFIED; ITADs also sell direct); ~1-6% in the A-05 glut (01_LANDSCAPE O3); negative on eBay in a 2023-like trough

**US manufacturability:** U.S. test-and-grade bench in East Coast flex space; the U.S. value-add is testing and documentation, not manufacturing.

**Who is already doing this:** ServerMonkey, Memory4Less, TechMikeNY (NYC), BuySellRAM, Curvature/Park Place, ITADs selling direct, Mobius Materials (authenticated marketplace, Richmond VA) and thousands of eBay sellers.

**Wins on which axis, for which buyer:** $/GB (used at roughly 25-60% of new) plus documented test provenance — for Third-party maintenance firms keeping DDR4 fleets alive, small cloud/HPC/CPU-offload inference operators, university labs; not DoD (DFARS 252.246-7008 / FAR 52.211-5 bar used parts without contracting-officer approval [UNVERIFIED-training])

**Survives a 2029 glut?:** no — Resale contribution drops to ~1-6% (01_LANDSCAPE O3), and DDR4 bought at 2026-27 peak prices loses value in transit. Only the serialized test-record layer survives, and only if it becomes part of a provenance or authentication service (C-64, C-92).

**Fatal-flaw candidate:** No moat and a closing window. The resale spread is a bet on DDR4 prices that peak in 2026-27, so the line must be cash-positive by end-2027 (01_LANDSCAPE F2). ITADs sell direct, and hyperscalers reuse DDR4 behind CXL. The serialized ledger is copyable because SPD already holds an assembly serial that decode-dimms prints. DoD is closed (DFARS 252.246-7008).

*Possible?* yes - an existing U.S. trade · *Profitable?* yes in 2026-27 / no in a glut - ~20% contribution now, ~1-6% in the A-05 glut · *Doable by this founder?* yes - $20-40k start, evenings and weekends

*Business-model lenses:* recert/brokerage, SaaS (test-record ledger), data product (graded-price index)

### C-63 — Die harvesting and module rebuild from e-waste, Shenzhen-style (tempting, dead) — ☠ KILLED (R4-NO-WINNING-AXIS: The card's own model says rebuilding destroys value. An intact, tested 32GB RDIMM is worth ~$192, against ~$72 of harvested x4 chips before a new PCB, RCD, assembly and 5-10% reball fallout. At the A-05 glut a harvested chip ($2.5) is worth less than its rework cost ($3.6). For the named price-sensitive buyer, an intact used module (C-62) beats a rebuilt one on price, reliability and legality. Reballed parts read as suspect counterfeits under AS6171, and x4 server die fit only RDIMMs (01_LANDSCAPE 6.3, 10.2). The only viable fragment, disclosed BGA repair, is already folded into C-62.)

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

### C-64 — CleanBOM-5949: memory-provenance verification for federal IT sellers — ☠ KILLED (RED-TEAM: DD1 (Provenance & Recertified Memory) was KILLED by the four-persona red team: The three FATAL objections hold: the named core buyer (OEM-compatible module makers) already knows its die source from POs, CoCs and package top marks and may self-certify under the proposed FAR rule, and resellers may rely on that free certificate. The die-source library was sampled from the wrong population (old OEM DDR4), keyed wrongly (module P/N) and replicable, so the moat is gone; the C-85 predictive subscript See 05_REDTEAM.md (DD1) and 04_DEEPDIVES/provenance-recert.md §14.)

*Sub-branch:* Government preference as moat (NDAA Sec. 5949 compliance) · *Materials sense:* none · *Merged from:* C.07, D.11

**What it is:** A subscription service plus bootable fleet-scan tool that proves the DRAM and NAND in servers, PCs and appliances sold to federal agencies contain no CXMT/YMTC/SMIC silicon before the FY2023 NDAA Sec. 5949 ban takes effect (2027-12-23). It combines SPD scans (module and DRAM-die JEP106 IDs, part numbers, date codes), a module-part-number-to-die-source cross-reference, supplier attestations, and sampled X-ray/decap die identification at a partner AS6171 lab, packaged as a per-SKU attestation; priced $1.5k-12k per month by tier plus lab pass-through.

**Why it could work:** Sec. 5949 pays for certified non-Chinese after a reasonable inquiry, not for verified non-Chinese. Demand comes from (1) False Claims Act exposure on the certification, (2) the proposed 72-hour reporting window, which needs continuous monitoring, and (3) OEM/ODM and module makers who certify upstream but cannot see the die source from module labels (CXMT die inside third-party modules). Drop the 'concrete gap a software founder can fill' claim: coreboot and decode-dimms already read the SPD DRAM-manufacturer field.

**Evidence:** TRL 7 · Rule 1: PARTIAL - statute and FAR Case 2023-008 confirmed; demand for independent verification is NOT supported by the proposed rule (certification after reasonable inquiry, no third-party audit, no affirmative proof, safe harbor for reliance on supplier certifications)
  - [Apple, China memory and the 2027 federal procurement ban (XenoSpectrum)](https://xenospectrum.com/en/apple-china-memory-federal-procurement-ban-2027/) — news, 2026-07. FY2023 NDAA Sec. 5949 bars federal procurement of products containing CXMT/YMTC/SMIC chips from Dec 2027 (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Apple lobbying U.S. for approval to buy blacklisted CXMT memory chips](https://thenextweb.com/news/apple-lobbying-us-approval-cxmt-blacklisted-memory-chips) — news, 2026-06-27. Apple lobbied Commerce to approve CXMT DRAM: CXMT silicon is entering U.S.-brand products (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Apple tests CXMT memory (Gigazine)](https://gigazine.net/gsc_news/en/20260810-apple-tests-cxmt/) — news, 2026-08-10. Apple reportedly testing CXMT DRAM (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [memtest86plus/memtest86plus (GitHub; README, system/jedec_id.h, system/spd.c, app/reports.c)](https://github.com/memtest86plus/memtest86plus) — industry, 2026-10-28. OPENED by C via git clone: GPLv2 tester, active (last commit 2026-10-28); USB/serial reports log SPD vendor, SKU, ECC and per-test results; JEP106 table includes CXMT 0x0A11, YMTC 0x091B, GigaDevice 0x0648; reads the module-maker ID (DDR4 SPD 320-321, DDR5 512-513) but not the DRAM-die manufacturer field
  - [TrendForce data: Samsung 39.4%, SK hynix 24.9% (Herald)](https://biz.heraldcorp.com/article/10866656) — news, 2026-09-07. CXMT reached 9.5% of DRAM revenue in 2Q26 (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Schumer demands Apple reject Chinese military-linked chips](https://www.schumer.senate.gov/newsroom/press-releases/citing-core-national-security-and-economic-reasons-schumer-demands-apple-reject-chinese-military-linked-chips) — government, 2026-07-30. Senators demand Apple commit not to use CXMT/YMTC: provenance is a live political issue (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [SpecTek PT040-56B DDR5 DRAM (Micron 1a) floorplan analysis (TechInsights)](https://www.techinsights.com/blog/spectek-pt040-56b-ddr5-dram-micron-1a-memory-floorplan-analysis) — industry, 2023. SpecTek parts carry current Micron 1-alpha die; die-level teardown identification is a commercial service (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [memtest86+ JEP106 table](https://raw.githubusercontent.com/memtest86plus/memtest86plus/main/system/jedec_id.h) — industry, 2026-09. Based on JEP106BP (Sep 2026): CXMT = 0x0A11, YMTC = 0x091B.
  - [memtest86+ SPD decoder](https://raw.githubusercontent.com/memtest86plus/memtest86plus/main/system/spd.c) — industry, 2026. Reads the manufacturer JEP106 ID from SPD (DDR5 bytes 512-513, DDR4 bytes 320-321) plus date code and part number.
  - [FAR Case 2023-008: Prohibition on Certain Semiconductor Products and Services (proposed rule)](https://www.govinfo.gov/content/pkg/FR-2026-02-17/html/2026-03065.htm) — government, 2026-02-17. Proposed FAR implementation of Sec. 5949, effective 2027-12-23; certification provision 52.240-XX and clause 52.240-YY (via search snippet)
  - [Section 5949 Proposed Rule Puts the FAR Council's Chips on the Table](https://www.crowell.com/en/insights/client-alerts/section-5949-proposed-rule-puts-the-far-councils-chips-on-the-table) — legal-analysis, 2026-02. Reasonable inquiry needs no formal third-party audit; Council declined to require proof artifacts; 72-hour reporting (via search snippet)
  - [FAR Council issues NPRM to implement prohibition on acquisition of certain semiconductors](https://www.insidegovernmentcontracts.com/2026/02/far-council-issues-notice-of-proposed-rulemaking-to-implement-prohibition-on-acquisition-of-certain-semiconductors/) — legal-analysis, 2026-02. Covered products include products incorporating covered semiconductors; no affirmative obligation to provide proof; safe harbor for reliance on supplier certifications (via search snippet)
  - [FAR Council Proposes Rule to Ban Purchases of Certain Semiconductor Products and Services](https://www.wiley.law/alert-FAR-Council-Proposes-Rule-to-Ban-Purchases-of-Certain-Semiconductor-Products-and-Services) — legal-analysis, 2026-02. Prospective application; waivers; safe harbor per 5949(h) (via search snippet)
  - [PSC Urges Clarity and Balance in FAR Semiconductor Prohibition Proposed Rule](https://pscouncil.org/a/Resources/2026/PSC_Comments_2026Apr_Semiconductor_20260420.aspx) — industry, 2026-04-20. Comment period closed 2026-04-20; contractors seeking clarity (via search snippet)
  - [Breaking circuit: how the covered semiconductor ban is reshaping the supply chain](https://www.reedsmith.com/articles/breaking-circuit-how-covered-semicon-ban-reshaping-supply-chain-usgovcon/) — legal-analysis, 2026. Due-diligence tools are part of a reasonable inquiry. That is partial evidence of tool demand (via search snippet)
  - [coreboot src/device/dram/ddr4.c](https://review.coreboot.org/plugins/gitiles/coreboot/+/67c73110e96ec6f1ec90c12f1ed6aac95107e896/src/device/dram/ddr4.c) — code, unknown. Reads manufacturer ID from DDR4 SPD bytes 350-351 (via search snippet)
  - [Samsung M393A4K40CB1-CRC40 datasheet (SPD table)](https://download.semiconductor.samsung.com/resources/data-sheet/M393A4K40CB1-CRC40.pdf) — company, unknown. DDR4 SPD bytes 350-351 = DRAM manufacturer ID; 320-321 = module manufacturer ID (via search snippet)
  - [i2c-tools mirror: eeprom/decode-dimms](https://github.com/mozilla-b2g/i2c-tools) — code, 2018-09-27. Opened via git clone. decode-dimms prints 'DRAM Manufacturer' (DDR3 bytes 148-149); DDR4/DDR5 decode is in later i2c-tools releases [UNVERIFIED]

**Capital tier:** T0 | **Time to first revenue:** 9-15 months: SPD-scan plus supplier-attestation 'reasonable inquiry' package piloted with 2-3 OEM/ODM or module makers once the final rule is published; lab die-ID offered only as an optional add-on | **Gross margin estimate:** 65-75% (software plus marked-up lab pass-through)

**US manufacturability:** Software and services; physical die-ID sampling at U.S. independent counterfeit-test labs; no fab dependency (rubric: software/services).

**Who is already doing this:** No memory-specific Sec. 5949 product found in a 2026-11-01 search [UNVERIFIED]. Adjacent: government-contracts law firms advising on 5949 (Crowell, Wiley, Covington, Mayer Brown, DLA Piper, Reed Smith), supply-chain-illumination vendors (Exiger, Interos, Govini), component-risk data (SiliconExpert, Z2Data), teardown die-ID (TechInsights), counterfeit-test labs (SMT Corp, Micross), OEM self-certification (Dell, HP, Lenovo).

**Wins on which axis, for which buyer:** Supply security / provenance assurance — for Primary: server/PC/appliance OEMs and ODMs, DIMM/SSD module makers and federal systems integrators that must certify upstream and need die-level knowledge. Secondary: GSA MAS/SEWP resellers, who under the 5949(h) safe harbor will mostly rely on OEM certifications and pay little.

**Survives a 2029 glut?:** yes — Demand is set by statute, not DRAM prices; in a glut CXMT's cheap bits gain share, which raises contamination risk and verification demand.

**Fatal-flaw candidate:** Now largely confirmed. The proposed FAR rule (2026-02-17) is certification-based, requires no third-party audit or proof artifacts, and gives a safe harbor for relying on supplier certifications, as Section 889 did. Most sellers can self-attest at near-zero cost. Paid demand shrinks to OEM/module makers and risk-averse integrators. Large compliance-data vendors can add a CXMT flag, and the SPD scanner is commodity code. The final rule could tighten or loosen this.

*Possible?* yes - SPD reads and die-ID teardowns are routine; the integration is new · *Profitable?* marginal-to-no - ~70% GM on software, but the certification-based rule and safe harbor cut the paying population well below the card's 37 customers · *Doable by this founder?* yes - T0 software-plus-partner-lab start, part-time feasible

*Business-model lenses:* SaaS, data product, defense-first

### C-65 — U.S. hi-rel DDR4/LPDDR4 multi-chip memory design house — ☠ KILLED (RED-TEAM: DD7 (Authorized-Aftermarket Legacy DRAM Die Bank (+ hi-rel MCMs)) was KILLED by the four-persona red team: No objection was refuted. All three FATALs were confirmed by the model, and they kill L1, the managed die-bank program and the only line this founder could run. Banking bare die costs a board OEM $186k-347k to manage ~$52k of die, 2.9-5.4x a packaged last-time buy plus dry storage. Board OEMs qualify packaged part numbers, and Micross sells the whole bundle direct (EDSP). L3, the title-taking bank, is killed by the c See 05_REDTEAM.md (DD7) and 04_DEEPDIVES/legacy-dram-diebank.md §14.)

*Sub-branch:* Packaging-only: hi-rel MCM from purchased KGD · *Materials sense:* c-capital

**What it is:** Design rugged x72 ECC DDR4 (e.g. 8GB from 9 x 8Gb x8 KGD) and LPDDR4X memory MCMs in 20-30 mm BGAs for defense, space and rugged-industrial processors, buying known-good die from Winbond, ESMT or Micross (Micron silicon where SpecTek/Micross can supply) and assembling and screening at U.S. hi-rel OSATs (Micross Apopka FL / RTP NC, QP Technologies CA, Integra Wichita KS [UNVERIFIED-training sites]).

**Why it could work:** Hi-rel memory MCMs sell at 10-100x commodity $/bit and die is <15% of ASP (model: ~$457 unit cost vs $800-3,000). The opening is narrower than the card says: a lower-cost, U.S.-assembled, screened-but-not-NASA-Level-1 DDR4/LPDDR4X MCM for NewSpace and rugged-industrial SoMs, where Teledyne e2v's space-grade pricing overshoots. Drop DARPA DV017 as evidence; it is an NVM topic.

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [Micross die and wafer flyer](https://micross.com/uploads/05827c98-1b61-4d4d-bb3c-04dc1b207e5a/Die_and_Wafer_Flyer_Rev_1_WEB.pdf) — company, unknown. Micross is the largest authorized bare-die/wafer supplier, with DRAM on its die line card; also a U.S. hi-rel packager (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Winbond KGD (customized memory solution)](https://winbond.com/hq/product/customized-memory-solution/kgd/) — company, unknown. Winbond sells DRAM known-good die to SiP makers: an open legacy KGD source (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [ESMT Known Good Die](https://esmt.com.tw/en/Applications/Known-Good-Die) — company, unknown. ESMT offers DRAM KGD (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [JESD49B.01 Procurement Standard for Known Good Die](https://www.jedec.org/node/8358) — industry, 2023-10. JEDEC procurement standard governing KGD quality and test claims (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Non-Volatile Memory for Extreme Environments (DARPA SBIR DPA26BZ04-DV017)](https://www.darpa.mil/research/programs/non-volatile-memory-extreme-environments) — government, 2026-07. DoD funds co-packaged extreme-environment memory systems (~$1.2M Direct-to-Phase-II, opened 2026-07-22) (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Radiation tolerant DDR4 memory chip DDR4T04G72M](https://signalintegrityjournal.com/articles/1749-radiation-tolerant-ddr4-memory-chip-ddr4t04g72m) — news, 2020-05. Teledyne e2v 4GB DDR4 MCM, 72-bit (64+8 ECC), Micron-based die, 15x20x1.92 mm, SEL >60 MeV.cm2/mg (via search snippet)
  - [Teledyne e2v Introduces First Radiation-Tolerant DDR4 Memory for Space Applications](https://www.guru3d.com/story/teledyne-e2v-introduces-first-radiation-tolerant-ddr4-memory-for-space-applications/) — news, 2020-05. -55 to 125 C, NASA Level 1 / ECSS Class 1 (via search snippet)
  - [Teledyne e2v DDR4T04G72M (Avnet Silica NPI)](https://my.avnet.com/silica/products/new-products/npi/2020/teledyne-e2v-ddr4t04g72m/) — distributor, 2020. DDR4T04G72 4GB/8GB series in distribution (via search snippet)
  - [High-Density Space-Grade DDR4 Data Storage Devices](https://www.epdtonthenet.net/article/214852/High-Density-Space-Grade-DDR4-Data-Storage-Devices.aspx) — news, unknown. 2.4 GT/s; compatible with most processors, SoCs and FPGAs (via search snippet)

**Capital tier:** T2 | **Time to first revenue:** 30-42 months: design and SI/PI, environmental qualification and radiation data, then a first design-in; NewSpace/rugged-industrial first, primes later | **Gross margin estimate:** 43-85% depending on ASP ($800-3,000)

**US manufacturability:** U.S. assembly and screening at hi-rel OSATs (Micross, QP Technologies, Integra) of imported die. Winbond/ESMT KGD is open. Micron die reaches established hi-rel houses (Teledyne e2v uses it), but startup access through Micross/SpecTek is UNVERIFIED (Micross line card does not name Micron, 01_LANDSCAPE row 23).

**Who is already doing this:** Teledyne e2v DDR4T04G72 (4GB/8GB x72 ECC rad-tolerant DDR4 MCM on Micron die, 15x20 mm, -55 to 125 C, NASA Level 1/ECSS Class 1, since 2020), Micross, Mercury Systems, Data Device Corp, Frontgrade, 3D Plus (HEICO), Intelligent Memory

**Wins on which axis, for which buyer:** Lifecycle length, environmental ruggedness, traceability — for Defense primes' mission computers, NewSpace avionics, rugged industrial system-on-modules

**Survives a 2029 glut?:** yes — Priced on qualification and heritage, not bits; die cost is a small share of ASP.

**Fatal-flaw candidate:** The flagship SKU already ships. Teledyne e2v has sold an x72 ECC 4/8GB DDR4 MCM with NASA Level 1 heritage since 2020, and Micross, DDC, Mercury, Frontgrade and 3D Plus hold flight and field heritage. Qualification plus design-in takes 30-42 months, and Micross is both a die/OSAT supplier and a competitor.

*Possible?* yes - incumbents ship these · *Profitable?* yes for incumbents with heritage; unproven for a no-heritage entrant · *Doable by this founder?* no - hardware team and qualification timeline

*Business-model lenses:* module/appliance, defense-first

### C-66 — High-capacity stacked-die legacy modules (32GB DDR3 RDIMM, 32GB DDR3L SODIMM) — ☠ KILLED (FACT-COLLAPSE: The card says it will build DDR3 capacities 'the majors never made or have stopped making'. That is false for both SKUs. Intelligent Memory's Oct-2024 DDR3 flyer and its product page list 32GB DDR3 RDIMM and LRDIMM modules built on its own 8Gb DDR3 parts, plus 16GB SO-DIMMs, which it has shipped since 2014. Samsung, SK hynix and Micron made the 8Gb dual-die DDR3 that 32GB RDIMMs use before those parts went EOL, so new and recovered supply of this exact module already exists (all via search snippets). The flagship 32GB DDR3L SO-DIMM cannot be built. JEDEC caps a SO-DIMM at 16 devices (PCWorld), and DDR3 devices top out at 8Gb [training: JESD79-3], so 16GB is the ceiling. What is left is a me-too module line. It would pay ~$788 per module for 4Gb KGD plus OSAT DDP, against an incumbent that owns the 8Gb component.)

*Sub-branch:* Packaging-only: stacked-die legacy capacity · *Materials sense:* mixed:b+c

**What it is:** Drop the 32GB DDR3L SO-DIMM: not buildable within JEDEC (16-device SO-DIMM cap x 8Gb max DDR3 density = 16GB). The 32GB DDR3 RDIMM is not a new capacity.

**Why it could work:** High-density DDR3 is in acute shortage (TrendForce, Jan 2026) and DDR3 4Gb costs ~$20/GB (June 2026 contract) to ~$25/GB (July spot). Model: a 32GB DDR3 RDIMM costs ~$788 (die $720, DDP $43) and sells ~$985 at a 25% markup.

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [DDR4 reportedly leads legacy memory rally with Q1 prices up to 50%; DDR3 in tight supply](https://www.trendforce.com/news/2026/01/19/news-ddr4-reportedly-leads-legacy-memory-rally-with-q1-prices-up-to-50-ddr3-in-tight-supply/) — news, 2026-01-19. Makers preparing to exit DDR4 in 2026; high-density DDR3 in acute shortage (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [TrendForce price page snapshot](https://www.trendforce.com/price) — industry, 2026-06-18. DDR3 4Gb $10.00 and DDR4 8Gb $16.00 (June 2026) - legacy DRAM is priced at $16-20/GB (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Memory shortages drive DDR4 prices over 50% in Q3 2026; DDR3 also impacted](https://wccftech.com/memory-shortages-drive-ddr4-prices-over-50-in-q3-2026-ddr3-also-impacted-by-higher-costs/) — news, 2026-07. Early-July 2026 spot DDR3 4Gb ~$3.19/Gb (~$25/GB), above DDR5 16Gb (~$2.94/Gb) (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Winbond KGD (customized memory solution)](https://winbond.com/hq/product/customized-memory-solution/kgd/) — company, unknown. Winbond sells DRAM known-good die to SiP makers: an open legacy KGD source (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Intelligent Memory DDR3 flyer (digital, 10.2024)](https://intelligentmemory.com/fileadmin/user_upload/Intelligent_Memory_DDR3_Flyer_digital_10.2024.pdf) — company, 2024-10. 16GB DDR3 UDIMM/SO-DIMM and 32GB DDR3 RDIMM built on 8Gb components, up to DDR3L-2133 (via search snippet)
  - [Intelligent Memory DDR3 DRAM modules product page](https://www.intelligentmemory.com/products/dram-modules/ddr3) — company, unknown. 32GB DDR3 LRDIMM and RDIMM options in the current catalog (via search snippet)
  - [I'M Intelligent Memory to release 16GB unregistered DDR3 modules](https://www.anandtech.com/show/7742) — news, 2014-02. First 16GB DDR3 UDIMM and SO-DIMM on 8Gb parts (via search snippet)
  - [Want 32GB of RAM in your laptop or NUC? You can finally do it](https://www.pcworld.com/article/432319/want-32gb-of-ram-in-your-laptop-or-nuc-you-can-finally-do-it.html) — news, unknown. JEDEC SO-DIMM rules cap a module at 16 chips. 32GB laptop modules came only with DDR4 stacking (via search snippet)
  - [DDR3 8Gbit memory components EOL from Samsung, Hynix, Micron (Intel community)](https://forums.intel.com/s/question/0D50P00004905gISAQ/ddr3-8gbit-memorycomponents-eol-from-samsung-hynix-micron?) — other, unknown. The majors made 8Gb DDR3 (dual-die, 2-CS) parts, now EOL (via search snippet)

**Capital tier:** T1 | **Time to first revenue:** 12-18 months (DDP qualification, per-platform BIOS/SI validation) | **Gross margin estimate:** 15-25%

**US manufacturability:** Partial: DDP stacking in the U.S. only at low-volume hi-rel houses (Micross); otherwise Asia; module SMT at any U.S. EMS.

**Who is already doing this:** Intelligent Memory ships 32GB DDR3 RDIMM/LRDIMM and 16GB DDR3(L) SO-DIMM/UDIMM on its own 8Gb DDR3 components (flyer 10.2024; first 16GB modules in 2014). Majors made 8Gb dual-die DDR3 (Samsung/SK hynix/Micron, now EOL), so recovered 32GB DDR3 RDIMMs circulate. Alliance, Virtium and ATP sell legacy modules.

**Wins on which axis, for which buyer:** none vs. incumbent: the same density and lifecycle, at a worse cost position (bought 4Gb KGD + OSAT DDP vs. an incumbent-owned 8Gb part) — for Telecom/network-equipment operators, industrial-PC fleets, legacy-server owners

**Survives a 2029 glut?:** no — DDR3 platforms retire and DDR3 falls back toward ~$3/GB; the module's value drops ~75% (Appendix A stress case) and the premium disappears.

**Fatal-flaw candidate:** A shrinking installed base, an incumbent (Intelligent Memory), and per-platform signal-integrity/BIOS validation that a small team cannot amortize.

*Possible?* no for 32GB DDR3L SO-DIMM; yes for 32GB DDR3 RDIMM, but the incumbent already ships it · *Profitable?* marginal - thin margins on a shrinking base · *Doable by this founder?* no - hardware engineering and die access

*Business-model lenses:* module/appliance

### C-67 — Rugged and new-form-factor memory modules built at a U.S. EMS (LPCAMM2/CAMM2, wide-temp coated SODIMM)

*Sub-branch:* Packaging-only: custom module formats · *Materials sense:* c-capital

**What it is:** Same, but JEDEC CAMM2 is a published standard (shipping products from Innodisk and congatec; drop the [UNVERIFIED-training] tag). Manassas components apply only to DDR4/LPDDR4 SKUs, never to DDR5 SODIMM or LPDDR5X LPCAMM2.

**Why it could work:** Rugged buyers pay 1.3-1.6x commodity, and Micron is steering U.S.-made DDR4/LPDDR4 at defense, auto and industrial buyers. The opening is a U.S.-assembled, MIL-environment-qualified variant for U.S. defense rugged-computer makers. CAMM2 itself is NOT supplier-thin (Innodisk, congatec).

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [Micron LPDDR4 components](https://micron.net/products/memory/dram-components/lpddr4) — company, unknown. Micron LPDDR4/4X in many packages and industrial/automotive temperature grades: authorized component supply for rugged modules (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Micron advances Made-in-America memory with manufacturing expansion in Virginia](https://www.hpcwire.com/off-the-wire/micron-advances-made-in-america-memory-with-manufacturing-expansion-in-virginia) — company, 2026-05-22. Micron Manassas Fab 6 began 1-alpha DDR4/LPDDR4 on 2026-05-22 for auto, defense, aerospace and industrial buyers, in a >$2B expansion that quadruples its DDR4 wafer supply (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Response measures to Samsung DDR4 IC EOL announcement (Advantech)](https://www.advantech.com/en/resources/news/response-measures-to-samsung-ddr4-ic-eol-announcement) — company, 2025. Industrial-PC maker tells customers DDR4 supply runs to ~end-2026 and to avoid Samsung DDR4 in new designs: long-lifecycle buyers are actively managing EOL (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Innodisk introduces DDR5 and LPDDR5X CAMM2 memory modules for rugged industrial applications](https://www.eejournal.com/industry_news/innodisk-introduces-ddr5-and-lpddr5x-camm2-memory-modules-for-rugged-industrial-applications/) — news, 2025-08. Screw-lock CAMM2/LPCAMM2 (LPDDR5X-8533) for rugged industrial use. Sampling Q4-2025 (via search snippet)
  - [congatec conga-TC1000r COM Express Type 6 rugged module (Mouser)](https://www.mouser.in/new/congatec/congatec-conga-tc1000r-rugged-modules/) — company, 2026-04-14. Rugged module with screw-locked LPCAMM2 (LPDDR5, up to 96GB), -40 to +85 C (via search snippet)
  - [Micron begins producing America's most advanced DRAM at its Virginia fab](https://www.tomshardware.com/tech-industry/micron-begins-producing-americas-most-advanced-dram-at-its-virginia-fab) — news, 2026-05. Manassas 1-alpha is DDR4-class; qualified production by end-2026 (via search snippet)

**Capital tier:** T1 | **Time to first revenue:** 18-30 months: design and JEDEC raw-card layout (3-6), environmental qualification (3-6), allocation agreement, then a first design win at a rugged-computer maker (12-24 months after sampling) | **Gross margin estimate:** 20-35% now; 10-27% in the A-05 glut

**US manufacturability:** U.S. assembly of imported die (rubric 3). DDR5 and LPDDR5X die come from Asian fabs. Only DDR4/LPDDR4 SKUs can carry U.S.-fabbed Manassas die, and Micron's back-end is in Malaysia/India, so even those die are packaged offshore [REPORTED via snippet]. Conformal coat, screening and SMT are routine at U.S. Class-3 EMS.

**Who is already doing this:** Virtium, SMART Modular (Penguin), Mercury Systems, ATP, Swissbit, Cervoz. Innodisk ships rugged screw-lock DDR5 and LPDDR5X CAMM2 (launched 2025-08). congatec ships rugged COM Express with screw-locked LPCAMM2 at -40 to +85 C (2026-04). Micron, Samsung and SK hynix make LPCAMM2/SOCAMM themselves.

**Wins on which axis, for which buyer:** Environmental reliability, lifecycle, form factor — for Rugged-computer makers (General Micro Systems, Crystal Group, Curtiss-Wright, Kontron-class) and defense primes

**Survives a 2029 glut?:** partially — The ruggedization premium persists, but the module price tracks DRAM down, so dollar margin shrinks ~55%.

**Fatal-flaw candidate:** Crowded by funded specialists (Virtium, SMART, ATP, Innodisk, which already ships rugged CAMM2) that compete for the same scarce component allocation. Design wins take 12-24 months. Memory makers ship CAMM-class modules themselves. U.S. content is limited to DDR4/LPDDR4 SKUs.

*Possible?* yes - shipping category · *Profitable?* marginal - 20-35% against strong incumbents · *Doable by this founder?* marginal - needs one hardware cofounder

*Business-model lenses:* module/appliance, defense-first

### C-68 — HBM-adjacent U.S. test and rework services near Amkor Peoria / SK hynix West Lafayette (dead for this founder) — ☠ KILLED (FACT-COLLAPSE: Every named customer is captive and closed to outside vendors. 01_LANDSCAPE.md 6.1 marks SK hynix West Lafayette (cleanroom Oct-2028, HBM4E from Q3-2029) and Micron's U.S. HBM packaging (2029+) as 'No' for outside customers (rows 19-20). Amkor Peoria integrates HBM into logic 2.5D packages but does not stack it, so it has no HBM-stack test or rework flow to serve (row 21) [UNVERIFIED]. The card admits both plants arrive with their own Advantest/Teradyne testers and Korean/Taiwanese suppliers. It gives no evidence that any HBM maker outsources KGSD test, and it puts first revenue at ~48 months, past the 36-month ceiling, on a T3 ticket. HBM 'rework' is also not a production flow: a failed TC-bonded stack or HBM-on-interposer assembly is scrapped [ESTIMATE: practitioner judgment]. 01_LANDSCAPE.md 10.2 already lists HBM packaging as closed.)

*Sub-branch:* Packaging-only: HBM adjacency · *Materials sense:* c-capital

**What it is:** Stand up known-good-stacked-die (KGSD) test, HBM-stack failure analysis and rework, or thermal-compression-bonding consumables near Amkor's Peoria AZ 2.5D campus and SK hynix's West Lafayette IN HBM packaging plant, to serve them as they ramp.

**Why it could work:** HBM takes ~3x DDR5 wafer area per bit, its prices keep rising (HBM4 2027 ~$4-5/Gb), and U.S. HBM packaging is coming: SK hynix Indiana targets HBM4E mass production in Q3 2029; Micron's U.S. HBM packaging follows its second Idaho fab (late 2028+).

**Evidence:** TRL 9 · Rule 1: UNSUPPORTED (value claim): no evidence that HBM makers outsource KGSD test, FA or rework
  - [SK hynix breaks ground on $4 billion packaging facility in Indiana](https://evertiq.com/news/2026-08-28-sk-hynix-breaks-ground-on-4-billion-packaging-facility-in-indiana) — news, 2026-08-28. SK hynix HBM packaging plant in West Lafayette IN; cleanroom target Oct 2028 (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [SK hynix Indiana plant (Herald Business)](https://mbiz.heraldcorp.com/article/10853891) — news, 2026-08. HBM4E mass production in Indiana from Q3 2029 (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Micron Technology Form 10-K FY2026](https://www.sec.gov/Archives/edgar/data/0000723125/000072312526000023/mu-20260903.htm) — company, 2026-10. Micron cites supply-allocation decisions that may affect some customers; plans U.S. HBM packaging (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Micron says the silicon gap between HBM and DDR5 is widening](https://www.tomshardware.com/tech-industry/semiconductors/micron-says-the-silicon-gap-between-hbm-and-ddr5-is-widening-with-every-generation) — news, 2026. HBM needs ~3x DDR5 wafer area per bit (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Lutnick memory tariff ultimatum (Taipei Times)](https://www.taipeitimes.com/News/biz/archives/2026/01/19/2003850817) — news, 2026-01-19. SK hynix Indiana is packaging only; no U.S. front-end DRAM from Korean makers (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Samsung HBM4 2027 pricing set to more than double (Silicon Analysts)](https://siliconanalysts.com/market/samsung-hbm4-2027-pricing-set-to-more-than-double-2026-10-07) — industry, 2026-10-07. HBM4 2027 forecast $4.00-5.00/Gb (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)

**Capital tier:** T3 | **Time to first revenue:** ~2029-30, when the captive plants ramp | **Gross margin estimate:** 20-40% (test-services norm)

**US manufacturability:** Arizona/Indiana from 2028-29, but both plants are captive and arrive with their own Advantest/Teradyne HBM testers ($3-5M each [ESTIMATE]) and Korean/Taiwanese supplier ecosystems.

**Who is already doing this:** SK hynix, Micron and Samsung in-house; Amkor, SPIL, ASE; Advantest, Teradyne, FormFactor; Hanmi, Hanwha and ASMPT for TC bonders [UNVERIFIED-training].

**Wins on which axis, for which buyer:** Bandwidth supply (HBM) via local proximity — for SK hynix Indiana and Micron Idaho (both captive, in-house test). Remove Amkor Peoria: logic 2.5D that integrates HBM and does not stack it.

**Survives a 2029 glut?:** partially — HBM demand is structural (AI), but a 2028-29 glut would hit HBM pricing too, and captive plants insource first.

**Fatal-flaw candidate:** Captive, capital-heavy and late: no outside customer exists before 2028-29, the first customers bring incumbent suppliers, and the ticket is tens of millions.

*Possible?* no for an outside vendor (captive flows); yes only in-house for SK hynix/Micron · *Profitable?* marginal - only for incumbents · *Doable by this founder?* no

*Business-model lenses:* module/appliance (services), defense-first not applicable

### C-69 — U.S. known-good-die wafer-probe and die-processing house for legacy DRAM — ☠ KILLED (FACT-COLLAPSE: The gap this card would fill is already filled by the company it names as its buyer. Micross in Apopka, FL offers wafer probe, wafer mapping and inking, and die processing: ~850 wafers probed a year and over 37M die probed a year, in 29,000 sq ft of Class H/K cleanroom, AS9100 (Micross facility page and die/wafer flyer, via search snippets). That capacity exceeds both the card's own ~700-wafer/yr breakeven and the few hundred wafers a year of U.S. demand it estimates. The real choke point is die supply, not probe capacity (01_LANDSCAPE.md 6.3). Winbond, ESMT and Etron already ship JESD49B.01-tested KGD, and untested DRAM wafers are mostly not sold to outsiders (the card's own fatal flaw), so a second house would have no input and no winning axis.)

*Sub-branch:* Packaging-only: KGD test · *Materials sense:* c-capital

**What it is:** Buy used DRAM ATE (older Advantest T55xx-class [UNVERIFIED-training]) and a 300mm prober, and offer wafer-level probe, speed-binning and burn-in that turns untested or partially tested legacy DRAM wafers (SpecTek, Winbond, ESMT) into JESD49B.01-compliant known-good die for U.S. hi-rel MCM and SiP makers.

**Why it could work:** Bare die is the U.S. back-end choke point and KGD carries a 15-40% premium over packaged $/GB. Model: ~$750k startup capex; losses below ~700 wafers per year at $600/wafer; ~$375k contribution at 1,500 wafers.

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [JESD49B.01 Procurement Standard for Known Good Die](https://www.jedec.org/node/8358) — industry, 2023-10. JEDEC procurement standard governing KGD quality and test claims (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [SpecTek support (Micron)](https://micron.net/sales-support/customer-support/spectek-support) — company, unknown. SpecTek sells Micron DRAM/LPDRAM in BGA packages and in wafer form (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Micross die and wafer flyer](https://micross.com/uploads/05827c98-1b61-4d4d-bb3c-04dc1b207e5a/Die_and_Wafer_Flyer_Rev_1_WEB.pdf) — company, unknown. Micross is the largest authorized bare-die/wafer supplier, with DRAM on its die line card; also a U.S. hi-rel packager (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Winbond KGD (customized memory solution)](https://winbond.com/hq/product/customized-memory-solution/kgd/) — company, unknown. Winbond sells DRAM known-good die to SiP makers: an open legacy KGD source (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Etron Memory ICs - KGDM](https://etron.com/kgdm/) — company, unknown. Etron, a fabless Taiwanese specialty-DRAM company, sells KGD memory (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Micross Apopka, FL facility](https://www.micross.com/about-us/facilities-and-locations/apopka-fl) — company, unknown. Bare die/wafer distribution, processing and assembly. ~850 wafers probed/yr, >37M die probed/yr, 29,000 sq ft Class H/K cleanroom (via search snippet)

**Capital tier:** T1 | **Time to first revenue:** 12-18 months (tool install, probe cards and test programs per die type) | **Gross margin estimate:** negative below ~700 wafers/yr; ~40% at 1,500

**US manufacturability:** Yes in principle: any U.S. light-industrial cleanroom; probe cards and test programs cost $50-150k per die type [ESTIMATE].

**Who is already doing this:** Micross Apopka FL (wafer probe ~850 wafers/yr, >37M die probed/yr, mapping/inking, AS9100) plus Rochester, ISE Labs (ASE), Integra and STS. The die vendors (Winbond, ESMT, Etron) ship tested KGD themselves.

**Wins on which axis, for which buyer:** none: U.S. location, AS9100 and probe capacity are already offered by Micross — for Remove Micross: it is the incumbent provider, not a buyer. Mercury, DDC and SiP startups already buy tested KGD.

**Survives a 2029 glut?:** partially — Defense demand is steady, but volume is tiny and vendors bundle KGD test themselves when capacity frees up in a glut.

**Fatal-flaw candidate:** Demand is a few hundred wafers a year, Winbond/ESMT/Etron already ship tested KGD, and untested DRAM wafers are mostly not sold to outsiders, so the house would sit idle.

*Possible?* yes · *Profitable?* no - below breakeven volume for the foreseeable market · *Doable by this founder?* no

*Business-model lenses:* module/appliance (test services), defense-first

### C-70 — All-domestic DRAM component: Micron Manassas wafer to U.S. package to U.S. module — ☠ KILLED (R1-UNSUPPORTED: The core value claim is that DoD and critical-infrastructure buyers will pay 1.5-3x for end-to-end U.S.-origin COTS DRAM. The card cites no evidence for it, and the canonical landscape contradicts it. TAA treats Korean and Taiwanese DRAM as compliant, COTS is exempt from the BAA component test, memory pays 0% under Section 232, and hi-rel buyers already pay 10-100x for MCMs built on foreign die (01_LANDSCAPE.md 0 item 7, 7.3). The card itself puts GM at ~0% without the premium. The supply side is unproven too. Manassas takes no outside customers (6.1 row 2). SpecTek lists wafers as a format but gives no availability or terms (via search snippet). Micron runs its back-end in Malaysia and India and could add U.S. packaging itself. The concept comes back only if two things happen: a written program requirement for U.S.-fabbed and U.S.-packaged DRAM, and a SpecTek 'yes' on Manassas wafers.)

*Sub-branch:* Module assembly and test in the U.S. (domestic-origin) · *Materials sense:* c-capital

**What it is:** Obtain Micron 1-alpha DDR4/LPDDR4 wafers or KGD made at Manassas Fab 6 (via SpecTek or a direct program), package and test them in the U.S. (Micross FL/NC, Integra KS or QP Technologies CA), and sell the only fully U.S.-origin DRAM component and module - eligible for an unqualified FTC 'Made in USA' claim and for programs that demand domestic end-to-end sourcing.

**Why it could work:** Manassas wafers are, as far as C knows, packaged offshore today, so no fully domestic DRAM component exists [UNVERIFIED-training]; Micron took $275M of CHIPS money to onshore exactly this silicon; the BAA domestic-content threshold for non-COTS items rises to 75% in 2029 [UNVERIFIED-training]; and SpecTek already sells Micron silicon in wafer form.

**Evidence:** TRL 9 · Rule 1: UNSUPPORTED (value claim): no buyer evidence for a domestic-origin premium. Landscape 7.3 finds none
  - [Micron advances Made-in-America memory with manufacturing expansion in Virginia](https://www.hpcwire.com/off-the-wire/micron-advances-made-in-america-memory-with-manufacturing-expansion-in-virginia) — company, 2026-05-22. Micron Manassas Fab 6 began 1-alpha DDR4/LPDDR4 on 2026-05-22 for auto, defense, aerospace and industrial buyers, in a >$2B expansion that quadruples its DDR4 wafer supply (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [CHIPS: Micron Manassas preliminary memorandum of terms](https://www.nist.gov/node/1869301) — government, 2024-12-10. Up to $275M CHIPS funding for Micron Manassas onshoring of 1-alpha DRAM (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [SpecTek support (Micron)](https://micron.net/sales-support/customer-support/spectek-support) — company, unknown. SpecTek sells Micron DRAM/LPDRAM in BGA packages and in wafer form (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Micross die and wafer flyer](https://micross.com/uploads/05827c98-1b61-4d4d-bb3c-04dc1b207e5a/Die_and_Wafer_Flyer_Rev_1_WEB.pdf) — company, unknown. Micross is the largest authorized bare-die/wafer supplier, with DRAM on its die line card; also a U.S. hi-rel packager (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [What U.S. tariff push means for Korea's semiconductor industry](https://www.koreatimes.co.kr/opinion/20260915/what-us-tariff-push-means-for-koreas-semiconductor-industry) — news, 2026-09-15. Korean memory excluded from Section 232 phase 1: no tariff-created U.S.-origin premium for memory today (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Micron begins producing America's most advanced DRAM at its Virginia fab](https://www.tomshardware.com/tech-industry/micron-begins-producing-americas-most-advanced-dram-at-its-virginia-fab) — news, 2026-05. 1-alpha DRAM at Manassas; qualified production expected by end-2026 (via search snippet)
  - [Inside Micron's $1T market-cap leap: a global fab expansion overview](https://www.trendforce.com/news/2026/05/27/news-inside-microns-1-trillion-market-cap-leap-a-global-fab-expansion-overview-across-the-u-s-and-asia/) — news, 2026-05-27. Micron leans on India and Malaysia as key back-end assembly/test hubs (via search snippet)
  - [Micron Technology Form 10-K FY2026](https://www.sec.gov/Archives/edgar/data/0000723125/000072312526000023/mu-20260903.htm) — primary-filing, 2026-10. 1-alpha DDR4 at Manassas supports legacy product needs of auto, industrial, medical, aerospace and defense customers. Gujarat A&T ramping 2026 (via search snippet)

**Capital tier:** T2 | **Time to first revenue:** 24-36 months (Micron program agreement, U.S. FBGA package qualification, first program design-in) | **Gross margin estimate:** 20-40% if a domestic-origin premium of 1.5-3x exists; ~0% if not

**US manufacturability:** Fully U.S. only if Micron releases Manassas wafers. Today Micron's assembly/test hubs are Malaysia and India (TrendForce 2026-05-27, via snippet).

**Who is already doing this:** Micron itself (U.S. fab, CHIPS-funded, could add domestic back-end at any time); Micross (U.S. hi-rel packaging of purchased die)

**Wins on which axis, for which buyer:** Supply security / domestic origin — for DoD programs with domestic or trusted-sourcing clauses, critical-infrastructure agencies, a 'Made in USA' consumer niche

**Survives a 2029 glut?:** partially — A domestic-origin premium is policy-driven and would survive, but the volume is small and commodity alternatives get cheaper.

**Fatal-flaw candidate:** Gatekeeper risk: Micron decides whether Manassas silicon reaches outsiders in wafer form, and a paid premium for U.S.-packaged COTS DRAM is unproven because TAA/BAA treat Taiwan and Korea as compliant and memory carries no Section 232 tariff.

*Possible?* unknown - gated by Micron/SpecTek releasing Manassas wafers (no public terms) · *Profitable?* marginal - premium unproven · *Doable by this founder?* no

*Business-model lenses:* module/appliance, defense-first

### C-71 — Trusted low-density SDRAM (64-512Mb) on SkyWater Fab 25 with 1T1C MIM cells — ☠ KILLED (R4-NO-WINNING-AXIS: For the named buyer (DoD DMSMS offices and avionics primes) the part loses on price: ~$30 unit cost and a $40-60 ASP against $2-5 COTS SDRAM that Winbond, ISSI and Alliance still make. It also loses on lifecycle, because SDRAM is still in production and Rochester re-creates EOL parts. The one axis it adds, a trusted U.S. fab, is not required for commodity memory: DoDI 5200.44 targets custom ICs, and COTS memory is bought commercially (01_LANDSCAPE.md 7.3). Where DoD does pay for trusted memory at SkyWater, it funds SRAM (Mobile Semiconductor SRAM compilers for the RH90 rad-hard process, BusinessWire 2022-06-09), not DRAM. So no buyer pays for this trade, which would also cost $10-20M of NRE, take 36-60 months to revenue, and need a TRL-3 capacitor module SkyWater does not have. Partner note: SkyWater has been an IonQ subsidiary since 2026-07-31; IonQ says it will keep serving foundry customers.)

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
  - [SkyWater announces availability of SRAM memory compiler for 90 nm Strategic Rad Hard by Process offering](https://www.businesswire.com/news/home/20220609005390/en/SkyWater-Announces-Availability-of-SRAM-Memory-Compiler-for-90-nm-Strategic-Rad-Hard-by-Process-Offering/) — news, 2022-06-09. DoD-funded trusted memory at SkyWater is SRAM (Mobile Semiconductor compilers on RH90), not DRAM (via search snippet)
  - [DoD awards SkyWater a $27M option to facilitate American-made semiconductors](https://www.businesswire.com/news/home/20220712005448/en/U.S.-Department-of-Defense-Awards-SkyWater-a-27M-Option-to-Facilitate-American-Made-Semiconductors-Critical-to-National-Security-and-Domestic-Supply-Chains) — news, 2022-07-12. T&AM funding for RH90; SkyWater is a DMEA Category 1A Trusted Foundry (via search snippet)
  - [IonQ completes acquisition of SkyWater Technology](https://ionq.com/news/ionq-completes-acquisition-of-skywater-technology) — company-IR, 2026-07-31. SkyWater is now an IonQ subsidiary. IonQ says it will keep serving foundry customers; Fab 25 adds ~400k wafer starts/yr (via search snippet)

**Capital tier:** T2 | **Time to first revenue:** 36-60 months (capacitor-module development, design, qualification) | **Gross margin estimate:** ~50% unit gross margin at $60, but $0.3-1.5M/yr gross profit cannot repay $10-20M NRE

**US manufacturability:** SkyWater Fab 25 (Austin TX) or Bloomington MN (DMEA Category 1A Trusted); SkyWater has been an IonQ subsidiary since 2026-07-31. U.S. OSAT packaging.

**Who is already doing this:** Alliance, ISSI and Winbond sell commercial SDRAM at ~$2-5; Rochester does licensed re-creation. DoD's trusted-memory route at SkyWater is SRAM (RH90 SRAM compilers from Mobile Semiconductor), and rad-hard programs use SRAM/MRAM from Honeywell, BAE and Frontgrade.

**Wins on which axis, for which buyer:** none for the named buyer: trust is not required for COTS SDRAM, and price and lifecycle are already met by COTS — for DoD DMSMS offices and avionics primes

**Survives a 2029 glut?:** yes — Trusted DMSMS pricing is insensitive to commodity cycles.

**Fatal-flaw candidate:** No buyer at the price: COTS SDRAM is still made at $2-5 and DoDI 5200.44 trust rules target custom ICs, not commodity memory, so the market is ~$0.3-1.5M per year of gross profit against $10-20M of NRE.

*Possible?* yes - 1T1C MIM eDRAM is production-proven elsewhere; unproven on this line · *Profitable?* no - NRE never paid back · *Doable by this founder?* no

*Business-model lenses:* fabless->foundry, defense-first, university/lab patent license (capacitor module)

### C-72 — Legacy-DRAM buying cooperative for mid-size U.S. OEMs — ☠ KILLED (R1-UNSUPPORTED (Phase 7 gate): As a standalone concept its core value claim — that Winbond/Nanya/Micron or franchised distributors will honor a multi-year allocation agreement with a no-title, no-credit buying co-op — has no evidence and no precedent in electronics (Phase 3 audit batch_10; 04_DEEPDIVES/lifecycle-intel.md §0 folds it in only as an unpriced feature plus three supplier calls). Under a strict Rule 1 it is killed as a concept; the three supplier calls remain a $0 test inside DD2's kill experiment.)

*Sub-branch:* Supply-chain arbitrage (demand aggregation) · *Materials sense:* none

**What it is:** An agency-model purchasing cooperative that pools 2027-2030 DDR3/DDR4/LPDDR4 forecasts from 30-100 mid-size U.S. OEMs and negotiates multi-year allocation agreements with Micron (Manassas DDR4), Winbond, Nanya and their franchised distributors, backed by member letters of credit, with a forecast and allocation web portal. Revenue: ~2.5% of pooled spend plus $10k per year membership.

**Why it could work:** In the shortage, allocation goes to strategic OEMs while module makers and small buyers are cut (TrendForce, Jan 2026); Nanya's long-term agreements expired in June 2026 and repriced >60%; firm, LC-backed, aggregated demand is what suppliers reward. Model: 40 members at $1.5M each = $60M pooled spend -> ~$1.9M revenue at ~85% gross margin (agency model).

**Evidence:** TRL 9 · Rule 1: UNSUPPORTED
  - [PC DRAM 1Q26: prices to surge over 80% on server supply prioritization (TrendForce abstract)](https://www.trendforce.com/research/download/RP260114IU) — industry, 2026-01-14. DRAM supply prioritized to strategic OEMs while module makers are limited (abstract only) (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Nanya 3Q26 results (TrendForce News)](https://www.trendforce.com/news/?p=65146) — news, 2026-10-12. Nanya 3Q26 gross margin 85.7%, operating margin 80%; LTAs expired end-June 2026 and repriced >60% higher in July (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Memory shortage watch: DDR3L/DDR4, May 2026 (Findchips)](https://blog.findchips.com/memory-shortage-watch-ddr3l-ddr4-may-2026/) — industry, 2026-05. Zero authorized stock of a mainstream Micron DDR4 part at Newark, Avnet and Mouser; only independent-market stock at a premium (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Micron ramps US-made DDR4 production in Virginia (eeNews Europe)](https://www.eenewseurope.com/en/micron-ramps-us-made-ddr4-production-in-virginia/) — news, 2026-05. DDR4 buffers at auto/industrial customers fell from 31+ weeks to 6-8 weeks (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Response measures to Samsung DDR4 IC EOL announcement (Advantech)](https://www.advantech.com/en/resources/news/response-measures-to-samsung-ddr4-ic-eol-announcement) — company, 2025. Industrial-PC maker tells customers DDR4 supply runs to ~end-2026 and to avoid Samsung DDR4 in new designs: long-lifecycle buyers are actively managing EOL (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Mobius Materials (Y Combinator profile)](https://www.ycombinator.com/companies/mobius-materials) — company, unknown. Mobius describes itself as the spot market for semiconductors: a funded intermediary already aggregating component demand (CROSS-REFERENCE: URL seen in a sibling agent's search results; not opened by C)
  - [Navigating the 2026 memory and NAND flash price surge (Suntsu)](https://suntsu.com/blog/navigating-the-2026-memory-and-nand-flash-price-surge/) — blog, 2026. Authorized distribution channels follow the same allocation rules as manufacturers, so small buyers cannot rely on them alone (via search snippet; attribution between two Suntsu 2026 posts not confirmed)

**Capital tier:** T1 | **Time to first revenue:** 9-15 months: founding memberships sign only alongside a first supplier or distributor LOI. First pooled allocation at 12-18 months (late 2027-2028), as allocation tightness begins to ease (01_LANDSCAPE.md F2). | **Gross margin estimate:** ~80-90% on fee revenue (agency model); title model is distribution-like (3-8%)

**US manufacturability:** None (commercial structure); can steer pooled volume to U.S.-made Manassas DDR4.

**Who is already doing this:** Franchised distributors (Arrow, Avnet, WPG, Future), which follow makers' allocation rules. EMS turnkey procurement (contract manufacturers already pool component buying for their OEM customers). Procurement consultancies, brokers, Mobius Materials. Healthcare GPOs (Vizient, Premier) are an analogy only: no electronics GPO was found (search 2026-11-01).

**Wins on which axis, for which buyer:** Supply security — for Mid-size OEMs buying $0.5-5M per year of legacy DRAM

**Survives a 2029 glut?:** partially — In a glut allocation is free, so the 2.5% fee must be justified on price alone against distributor volume pricing and EMS buying. Expect fees to compress to <=1% and members to churn. The network survives only if it has become the members' outsourced commodity desk.

**Fatal-flaw candidate:** Suppliers and franchised distributors may refuse an intermediary that takes neither title nor credit risk. Taking title needs $8-27M of working capital (T2). The value window is ~2027 only: allocation scarcity, the whole product, starts to ease in 2028 and is gone in a glut.

*Possible?* marginal - hinges on one supplier honoring a pooled LTA; untested · *Profitable?* marginal - good margins if allocation materializes · *Doable by this founder?* marginal - needs a memory-sales veteran

*Business-model lenses:* recert/brokerage (procurement), SaaS (forecast portal), data product

## D. Software & virtual RAM (12 cards)

### C-73 — Memory FinOps Audit for Cloud SaaS — ☠ KILLED (RED-TEAM: DD4 (Memory Efficiency for On-Prem & Self-Hosted Fleets) was KILLED by the four-persona red team: After the accepted objections, the value-supported C-74 fee falls 77%, from $7.36 to $1.66 per node per month. The causes compound: Proxmox already runs KSM, fleets hold less DDR5, the saving is a rental equivalent rather than a purchase avoided, and the vendor's share of a counterfactual is smaller. Meanwhile credible 24/7 on-call plus E&O costs ~$2,900-3,400 a month. The re-run BASE never breaks even, burns through See 05_REDTEAM.md (DD4) and 04_DEEPDIVES/memory-efficiency.md §14.)

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
  - [AWS raises GPU prices 15% on a Saturday](https://www.theregister.com/2026/01/05/aws_price_increase/) — news, 2026-01-05. AWS's Jan-2026 increase hit EC2 Capacity Blocks for ML (GPU reservations), not general EC2 (via search snippet).
  - [AWS EC2 Capacity Blocks price hike 2026](https://tech-insider.org/aws-ec2-capacity-blocks-price-hike-2026) — news, 2026-07. Capacity Blocks up ~20% from 2026-07-01; AWS says other EC2 prices are unchanged (via search snippet).
  - [Intel closes Granulate, lays off dozens](https://en.globes.co.il/en/article-intel-closes-granulate-lays-off-dozens-1001492599) — news, 2024-10. Intel shut Granulate (Tiber App-Level Optimization) after failing to sell it (via search snippet).

**Capital tier:** T0 | **Time to first revenue:** 4-8 months to a first fixed-fee audit ($3-8k), done as NDA consulting in the founder's network. A recurring monitoring subscription needs SOC 2-style assurance before buyers grant a standing IAM role, so expect it at ~9-12 months. | **Gross margin estimate:** 60-80% (the audit phase is founder labor; the software subscription runs 80%+)

**US manufacturability:** Pure software built and hosted in the U.S. (AWS us-east-1) and sold via AWS Marketplace. No fab or hardware.

**Who is already doing this:** CAST AI, ScaleOps, StormForge (CloudBolt), Kubecost/OpenCost (IBM [UNVERIFIED-T]), PerfectScale (DoiT [UNVERIFIED-T]), Sedai, Densify, plus free tools: AWS Compute Optimizer, Robusta KRR, K8s VPA, Goldilocks. Intel closed Granulate (Tiber App-Level Optimization) in Oct-2024 after failing to find a buyer for a ~$650M acquisition (Globes, via search snippet).

**Wins on which axis, for which buyer:** $/GiB-month of rented cloud RAM (fewer GiB-months bought) — for Series A-C SaaS companies with $20k-200k/month AWS bills and no dedicated FinOps engineer

**Survives a 2029 glut?:** yes — AWS's 2026 increases hit only EC2 Capacity Blocks for ML (+~15% Jan-2026, +~20% Jul-2026), and other EC2 prices were reported unchanged, matching D's 92-SKU diff. Savings therefore do not depend on DRAM prices, so a glut changes nothing. The flip side is that the shortage gives no new 'why now'. Analyst forecasts of 5-10% memory-instance increases are unconfirmed.

**Fatal-flaw candidate:** Crowded category with a free floor (Compute Optimizer, KRR, VPA, OpenCost). The DRAM shortage never reached general EC2 list prices (only ML Capacity Blocks rose), so buyers feel no new urgency. A report-only product churns once the savings are booked, and standing read access to customer AWS accounts gates the subscription behind SOC 2 (cost and time not modeled).

*Possible?* yes - standard FinOps mechanics, shipping at many vendors · *Profitable?* marginal - ~$270/month ACV against free tools and funded automation vendors; churn after the savings are booked · *Doable by this founder?* yes - read-only AWS integration and reports; the first revenue could come from consulting in the founder's network

*Business-model lenses:* SaaS; services (fixed-fee audit) -> SaaS

### C-74 — Fleet Memory-Reclaim Autopilot (TMO for on-prem) — ☠ KILLED (RED-TEAM: DD4 (Memory Efficiency for On-Prem & Self-Hosted Fleets) was KILLED by the four-persona red team: After the accepted objections, the value-supported C-74 fee falls 77%, from $7.36 to $1.66 per node per month. The causes compound: Proxmox already runs KSM, fleets hold less DDR5, the saving is a rental equivalent rather than a purchase avoided, and the vendor's share of a counterfactual is smaller. Meanwhile credible 24/7 on-call plus E&O costs ~$2,900-3,400 a month. The re-run BASE never breaks even, burns through See 05_REDTEAM.md (DD4) and 04_DEEPDIVES/memory-efficiency.md §14.)

*Sub-branch:* Transparent memory compression / proactive reclaim / dedup · *Materials sense:* none

**What it is:** A per-node agent plus web control plane. It enables and tunes upstream Linux zswap (zsmalloc + zstd/lz4), Meta-Senpai-style PSI-driven proactive reclaim via cgroup2, KSM page dedup on Proxmox/KVM hosts, and Kubernetes 1.34 LimitedSwap, with per-workload SLO guardrails and a 'GB reclaimed = $ of DRAM not bought' ledger. It is sold per node to on-prem/colo operators who buy DRAM at 2026 prices.

**Why it could work:** On-prem buyers pay for DRAM directly: DDR5 RDIMMs cost $14-16/GB at contract and ~$32/GB street, and used 64GB DDR4 RDIMMs cost $250-370 ($3.9-5.8/GB, amcompute 12-month data to Aug-2026). Take a 200-server x 512GB fleet with 20% cold memory at ~2:1 compression: it frees ~10 TB. That defers $154k (DDR5 contract) to $328k (DDR5 street) of purchases, but only ~$40-59k on a DDR4 fleet topped up with used DIMMs. Kubernetes container swap went GA in v1.34. Meta's TMO saves 20-32% of total memory fleet-wide (ASPLOS 2022, confirmed via snippet). Hetzner's 2026 price increases (up to 37% from Apr-1, citing RAM/NVMe) show hosting providers feel the cost.

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [Meta Senpai README](https://github.com/facebookincubator/senpai) — industry, unknown. PSI plus cgroup2 memory.high proactive reclaim (TMO building block). Example: kernel-build peak fell from 804 MB to 348 MB.
  - [Linux zswap docs](https://github.com/torvalds/linux/blob/master/Documentation/admin-guide/mm/zswap.rst) — industry, 2026. Upstream compressed swap cache (zsmalloc) with per-cgroup writeback control and a shrinker.
  - [Linux zram docs](https://github.com/torvalds/linux/blob/master/Documentation/admin-guide/blockdev/zram.rst) — industry, 2026. Upstream compressed RAM device (lz4/zstd), with writeback and recompression; the docs expect about 2:1 compression.
  - [Linux KSM docs](https://github.com/torvalds/linux/blob/master/Documentation/admin-guide/mm/ksm.rst) — industry, 2026. Page dedup for KVM VM density, with a general_profit metric; costs CPU and COW latency.
  - [KEP-2400 node swap kep.yaml](https://github.com/kubernetes/enhancements/blob/master/keps/sig-node/2400-node-swap/kep.yaml) — industry, 2025. Kubernetes container swap (LimitedSwap) went stable in v1.34.
  - [Kubernetes swap memory management docs](https://github.com/kubernetes/website/blob/main/content/en/docs/concepts/cluster-administration/swap-memory-management.md) — industry, 2025. Operational caveats: encrypt swap, use fast NVMe, taint swap nodes. Swap degrades badly on throttled cloud disks, and the scheduler ignores swap.
  - [EE Times Asia / Counterpoint RDIMM prices (via p1-market)](https://www.eetasia.com/memory-prices-surging-by-90-from-4q-2025/) — news, 2026-01. 64GB RDIMM contract $450 (4Q25), above $900 (1Q26), possibly above $1,000 (2Q26).
  - [TMO: Transparent Memory Offloading in Datacenters (ASPLOS 2022, Meta)](https://par.nsf.gov/servlets/purl/10332477) — conference, 2022-02-28. Saves 20-32% of total memory across millions of Meta servers; PSI-based offloading upstreamed into Linux (via search snippet).
  - [Hetzner increases prices from April 1](https://heise.de/-11185981) — news, 2026-02. Hetzner announced increases of up to 37% on cloud, dedicated and object storage from 2026-04-01; setup fees rose earlier, citing RAM and NVMe costs (via search snippet).
  - [DDR4 64GB RDIMM server memory appraisal](https://www.amcompute.com/appraisals/ddr4-64gb-rdimm) — industry, 2026-08. Used 64GB DDR4 RDIMM ~$250-370 over the last 12 months, up ~285% YoY (via search snippet).

**Capital tier:** T1 | **Time to first revenue:** 9-15 months: build the guarded agent, run the volunteer-host SLO test, then a paid pilot with a Proxmox MSP or regional host ($500-2k/month for 50-200 nodes). | **Gross margin estimate:** 75-85%

**US manufacturability:** Pure software. Target customers' fleets sit in U.S. colos (Ashburn VA, Secaucus NJ). Builds on upstream Linux mm, Proxmox VE (KSM) and Kubernetes 1.34+.

**Who is already doing this:** Meta (TMO/Senpai, internal), Google (zswap far memory, internal), Linux upstream (free), Red Hat/Canonical (tuned profiles), Proxmox (KSM built in). The cloud K8s optimizers (CAST AI, ScaleOps) focus on requests and instances, not swap [ESTIMATE]. MemVerge left the field.

**Wins on which axis, for which buyer:** Effective $/GB (usable GB per purchased GB), which defers DRAM capex — for Regional hosting providers, MSPs running Proxmox/KVM, on-prem Kubernetes and CI/build farms, and university HPC centers that must buy DDR5 RDIMMs at 2026 prices

**Survives a 2029 glut?:** partially — The deferred-DRAM value of the reference fleet falls from ~$154k to ~$61k at -60% for DDR5 fleets. DDR4 fleets that can buy used RDIMMs at $3.9-5.8/GB are already near that level (~$40-59k) today. Density value remains but becomes a nice-to-have, and the price story behind the sale disappears.

**Fatal-flaw candidate:** It is configuration of free kernel features. Sophisticated operators already do it themselves, and conservative ones fear swap latency and OOM incidents. One production incident at an early customer ends the company.

*Possible?* yes - production-proven at Meta/Google, and every component is upstream · *Profitable?* marginal - real savings mainly for DDR5 fleets; DDR4 fleets can add used RDIMMs at ~$4-6/GB, buyers can DIY with free upstream features, and the pain halves in a glut · *Doable by this founder?* marginal - needs a Linux-mm expert for SLO safety; the sales cycle to on-prem ops is slow

*Business-model lenses:* SaaS (per-node subscription); open-core agent

### C-75 — KV-Cache Tier Integration & Tuning for Self-Hosted LLMs — ☠ KILLED (RED-TEAM: DD4 (Memory Efficiency for On-Prem & Self-Hosted Fleets) was KILLED by the four-persona red team: After the accepted objections, the value-supported C-74 fee falls 77%, from $7.36 to $1.66 per node per month. The causes compound: Proxmox already runs KSM, fleets hold less DDR5, the saving is a rental equivalent rather than a purchase avoided, and the vendor's share of a counterfactual is smaller. Meanwhile credible 24/7 on-call plus E&O costs ~$2,900-3,400 a month. The re-run BASE never breaks even, burns through See 05_REDTEAM.md (DD4) and 04_DEEPDIVES/memory-efficiency.md §14.)

*Sub-branch:* LLM inference KV-cache management software · *Materials sense:* none

**What it is:** A productized integration service plus a benchmarking/monitoring dashboard. It deploys host-DRAM and NVMe KV-cache tiers (LMCache, NVIDIA Dynamo KVBM, Mooncake Store, SGLang HiCache) into mid-market vLLM/SGLang clusters and sizes the DRAM tier per workload from measured prefix-reuse rates. Recurring revenue comes from hit-rate, TTFT and $/token monitoring.

**Why it could work:** Llama-3.1-70B needs 320 KiB of KV per token, so 1 TB of host DRAM ($15k at 2026 contract) holds ~3.1M reusable prefix tokens. Mooncake reports Kimi serving 75% more requests within SLO, and Dynamo claims 2x TTFT from KV-aware routing. The stacks churn fast (LMCache shipped 65 PyPI releases from May 2025 to Oct 2026; vLLM 0.32.0 came out 2026-10-18), and teams running 8-64 GPUs lack staff to keep up.

**Evidence:** TRL 8 · Rule 1: SUPPORTED
  - [LMCache README](https://github.com/LMCache/LMCache) — industry, 2026. Open-source KV-cache layer (CPU/SSD/remote tiers) for vLLM, integrated into NVIDIA Dynamo (Sep 2025). Development supported by Tensormesh.
  - [NVIDIA Dynamo README](https://github.com/ai-dynamo/dynamo) — company, 2026. Free Apache-2.0 KVBM offloads KV GPU->CPU->SSD->remote. Claims 2x TTFT from KV-aware routing (Baseten).
  - [Mooncake README](https://github.com/kvcache-ai/Mooncake) — industry, 2026. KV-centric disaggregated serving at Kimi: 75% more requests within SLO. Integrated into vLLM, SGLang, LMCache, Dynamo and TensorRT-LLM (2026-10-10).
  - [tensormesh SDK on PyPI](https://pypi.org/pypi/tensormesh/json) — company, 2026-06. Tensormesh, the company around LMCache, ships a hosted serverless-inference and control-plane SDK (first release 2026-04-02).
  - [meta-llama/llama-models config (via B)](https://github.com/meta-llama/llama-models) — industry, 2026. Llama 3.1 70B: 80 layers, 8 KV heads, head_dim 128, so 320 KiB of KV per token at BF16.
  - [Tensormesh: $20 Million Raised To Scale KV Caching Infrastructure For Enterprise AI Inference](https://pulse2.com/tensormesh-20-million-raised-to-scale-kv-caching-infrastructure-for-enterprise-ai-inference/) — news, 2026-05-27. $20M extension (total $24.5M) from AMD Ventures, CoreWeave, NVentures and others; Tensormesh Inference GA with cache-hit and token-cost visibility (via search snippet).
  - [Tensormesh taps Nvidia, AMD, CoreWeave funding to fix LLM memory problems](https://siliconangle.com/2026/05/27/tensormesh-taps-nvidia-amd-coreweave-funding-fix-llm-memory-problems/) — news, 2026-05-27. Same round, independent coverage (via search snippet).

**Capital tier:** T0 | **Time to first revenue:** 9-15 months: publish a vLLM+LMCache/Dynamo benchmark on rented 8xH100, land one discounted reference deployment, then a $15-40k integration engagement and a monitoring retainer. | **Gross margin estimate:** 50-70% (services-heavy)

**US manufacturability:** Software and services. Customers' GPU clusters are in U.S. colos (Ashburn VA, NJ). Builds on Apache-2.0 LMCache, Dynamo and Mooncake.

**Who is already doing this:** Tensormesh (the LMCache creators): $4.5M seed Oct-2025 plus a $20M extension 2026-05-27 from NVIDIA NVentures, AMD Ventures and CoreWeave; Tensormesh Inference is GA with cache-hit-rate, KV-usage and token-cost dashboards. Also NVIDIA (Dynamo/KVBM, free), Moonshot (Mooncake), Red Hat llm-d [UNVERIFIED-T], WEKA Augmented Memory Grid, Pliops, VAST [UNVERIFIED-T], Phison aiDAPTIV+ (flash KV tier, 2026), Kove:SDM (pitches remote-DRAM KV tiering), and hosted inference providers (Baseten, Together, Fireworks).

**Wins on which axis, for which buyer:** $/token and TTFT: host DRAM ($/GB) substitutes for re-computing prefill on HBM GPUs — for Mid-market teams self-hosting 70B-class open models on 8-64 GPUs for data-residency reasons (legal-tech, healthcare, fintech)

**Survives a 2029 glut?:** yes — A glut makes host DRAM cheaper and the KV tier more attractive. The value is GPU-hours avoided, which does not depend on DRAM prices.

**Fatal-flaw candidate:** The LMCache company itself (Tensormesh, $24.5M, backed by NVIDIA/AMD/CoreWeave) sells the exact hit-rate/$-per-token observability this card wants as recurring revenue. NVIDIA and the vLLM/SGLang maintainers keep folding KV tiering into defaults, so the integration gap closes within ~12 months. Buyers are paying for GPU-infra credibility the founder does not have.

*Possible?* yes - shipping open source at Moonshot/Kimi and integrated into NVIDIA Dynamo · *Profitable?* marginal-to-no - services margin only. The SaaS monitoring line competes with Tensormesh Inference (GA May-2026, NVIDIA/AMD/CoreWeave-backed) and free NVIDIA tooling · *Doable by this founder?* marginal - needs GPU access for benchmarking and deep inference-stack knowledge

*Business-model lenses:* services -> SaaS; open-core

### C-76 — Software-Defined Memory Pooling / RAM-as-a-Service over CXL (tempting, dead) — ☠ KILLED (DUPLICATE: This is the same idea as C-50 (Rack-Scale CXL Pooling Appliance): pool DRAM across hosts through a CXL 2.0/3.x switch (XConn class) plus orchestration software to recover stranded memory, sold on fleet $/GB. C-76 is the software-license packaging aimed at an HPC buyer, which is a business-model lens, not a separate concept. Its 'RDMA today' path is exactly Kove:SDM, which is alive and selling: Redis/Valkey benchmarks announced Sep-2025 and a Supermicro solution brief. So the card's 'category is dead, prior entrants pivoted' premise is half wrong: MemVerge pivoted, Kove did not. Upstream Linux still scores CXL Dynamic Capacity and multi-host sharing [0], and the card's own verdicts are possible: marginal, profitable: no, doable: no.)

*Sub-branch:* Software-defined memory (Kove/MemVerge model) · *Materials sense:* none

**What it is:** OS/hypervisor software that pools DRAM across servers (RDMA today, CXL 2.0/3.x switches later) and leases slices to applications on demand: the Kove:SDM / MemVerge Memory Machine model. It would be sold as an on-prem license to HPC, genomics and in-memory analytics shops.

**Why it could work:** Pooling recovers stranded memory (Azure's Pond work reported ~7-9% DRAM savings [UNVERIFIED-T]), and each stranded GB is worth 4x more in 2026. CXL switches (XConn, Astera Labs) are shipping in pilots.

**Evidence:** TRL 6 · Rule 1: SUPPORTED
  - [MemVerge GitHub org](https://github.com/MemVerge) — company, 2026-10-28. Recent work is LLM routing, LMCache/vLLM forks, the MMAI GPU cluster manager and cloud-HPC spot tools. No new memory-virtualization repos.
  - [MemVerge mmai-public](https://github.com/MemVerge/mmai-public) — company, 2026. Memory Machine AI is a GPU cluster manager (docs path /AI/GPU_Cluster_Manager), not a DRAM pooling product.
  - [Linux CXL maturity map (via B)](https://github.com/torvalds/linux/blob/master/Documentation/driver-api/cxl/maturity-map.rst) — industry, 2026-10-31. Upstream Linux: Dynamic Capacity Device, multi-host sharing and fabrics are all scored [0] (not implemented).
  - [SK hynix HMSDK (via B)](https://github.com/skhynix/hmsdk) — company, 2025-11-03. CXL tiering (weighted interleave, DAMON migration) is already upstream and free.
  - [Software-Defined Memory: Kove Announces Benchmarks](https://www.storagenewsletter.com/2025/09/12/software-defined-memory-kove-announces-benchmarks/) — news, 2025-09-12. Kove:SDM active in 2025; vendor benchmarks for Redis/Valkey on pooled remote memory (via search snippet).
  - [Supermicro Solution Brief: KoveSDM](https://www.Supermicro.com/solutions/Solution_Brief_KoveSDM.pdf) — company, unknown. Kove:SDM sold through a Supermicro solution brief (via search result title/snippet).

**Capital tier:** T2 | **Time to first revenue:** 24-36 months: needs CXL switch hardware partners, enterprise validation and a field sales team. | **Gross margin estimate:** 70-85% if it sells

**US manufacturability:** Software. Hardware would come from U.S. CXL switch/expander vendors (XConn, Astera Labs) in Supermicro/Dell servers; Montage (China) controllers would be avoided.

**Who is already doing this:** Kove (Kove:SDM, Chicago): active, with Sep-2025 Redis/Valkey benchmarks, a Supermicro solution brief, and AI-infra conference sponsorship. MemVerge moved to AI/GPU cluster management. Also Liqid, GigaIO, Unifabrix, Panmnesia, and free upstream Linux tiering (TPP, DAMON, weighted interleave).

**Wins on which axis, for which buyer:** $/GB through fewer DIMMs per cluster — for HPC centers and genomics/EDA farms with bursty per-job memory peaks

**Survives a 2029 glut?:** no — Stranded-memory savings of ~10% are worth little at ~$6/GB. Pooling was a hard sell even before the shortage.

**Fatal-flaw candidate:** The category's best-known startup (MemVerge) walked away from memory virtualization. Linux upstream still scores CXL Dynamic Capacity and multi-host sharing [0], and tiering is already free upstream. Enterprise hardware dependence far exceeds T0/T1.

*Possible?* marginal - RDMA far memory works at hyperscalers; CXL pooling software is immature upstream · *Profitable?* no - one prior entrant (MemVerge) pivoted out, and the survivor (Kove) already holds the RDMA software-defined-memory position with OEM distribution; ~7-10% stranded-memory savings do not carry CXL switch and integration cost · *Doable by this founder?* no - requires systems-software depth and hardware partners

*Business-model lenses:* software licensing; fabless->OEM partnership

### C-77 — NVMe-as-RAM Virtual Memory Software (IMDT/ScaleMP revival, tempting, dead) — ☠ KILLED (R4-NO-WINNING-AXIS: The pitch is $/GB, with NAND standing in for DRAM, to in-memory analytics users. But the same capacity at NAND prices is already free through Linux swap plus zswap writeback on the same NVMe (and Kubernetes LimitedSwap, GA in v1.34), so a paid license wins no axis against the buyer's real alternative. Meanwhile NAND reads (~50-100 us) run ~1000x slower than DRAM (~100 ns). The card's TRL 9 belongs to Intel IMDT, which ran on Optane media that Intel wrote off ($559M impairment, Q2-2022). The one place flash-as-memory has traction in 2026, AI working memory and KV cache, is being productized by Phison (aiDAPTIV+ bundled with its own Pascari SSDs; GTC Mar-2026, Computex 2026) and is covered on the hardware side by C-46 and C-53.)

*Sub-branch:* Software 'virtual RAM' on flash · *Materials sense:* a-material

**What it is:** A thin hypervisor or kernel layer that presents NVMe SSDs as system RAM (the Intel Memory Drive Technology / ScaleMP vSMP MemoryONE approach), so a server with 256GB DRAM plus 4TB NVMe shows 4TB of 'memory'. It would be sold as a per-server license.

**Why it could work:** NAND $/GB is a small fraction of DRAM even after its own 2026 rise, NAND is forecast to turn to surplus in 2H27 (TrendForce via p1), and the arbitrage looks enormous on paper.

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [Linux zswap docs](https://github.com/torvalds/linux/blob/master/Documentation/admin-guide/mm/zswap.rst) — industry, 2026. Upstream compressed swap cache (zsmalloc) with per-cgroup writeback control and a shrinker.
  - [Kubernetes swap memory management docs](https://github.com/kubernetes/website/blob/main/content/en/docs/concepts/cluster-administration/swap-memory-management.md) — industry, 2025. Operational caveats: encrypt swap, use fast NVMe, taint swap nodes. Swap degrades badly on throttled cloud disks, and the scheduler ignores swap.
  - [Intel 10-Q Q2-2022 (via A2)](https://www.sec.gov/Archives/edgar/data/50863/000005086322000030/intc-20220702.htm) — company, 2022-07. Optane wind-down with a $559M inventory impairment. The media that made NVMe/PMem-as-RAM viable is gone.
  - [Nvidia GTC 2026: Phison Rescales Local AI Inferencing with Flash Memory Expansion](https://www.storagenewsletter.com/2026/03/17/nvidia-gtc-2026-phison-rescales-local-ai-inferencing-with-flash-memory-expansion/) — news, 2026-03-17. aiDAPTIV extends AI working memory across GPU memory, system RAM and Pascari flash (vendor claims; via search snippet).
  - [Phison extends aiDAPTIV+ to boost AI inference on PCs](https://www.blocksandfiles.com/ai-ml/2026/01/07/phison-extends-aidaptiv-to-boost-ai-inference-on-pcs/4090377) — news, 2026-01-07. aiDAPTIV+ moved from small-scale training to KV-cache workloads (via search snippet).

**Capital tier:** T1 | **Time to first revenue:** 18-30 months: hypervisor development plus validation with an in-memory analytics vendor. | **Gross margin estimate:** 80% (license) if any sales

**US manufacturability:** Software running on commodity NVMe (Micron/Solidigm SSDs in U.S.-assembled servers).

**Who is already doing this:** Intel IMDT (Optane-only, end-of-life with Optane [UNVERIFIED-T]), ScaleMP (acquired by SAP [UNVERIFIED-T]), free Linux swap + zswap writeback, Phison aiDAPTIV+ (SSD-backed AI memory extension bundled with Pascari SSDs; KV-cache extension Jan-2026, GTC Mar-2026), and Kove:SDM (remote DRAM, not flash).

**Wins on which axis, for which buyer:** $/GB of capacity (NAND standing in for DRAM) — for In-memory analytics users who could tolerate microsecond-to-millisecond tail latency

**Survives a 2029 glut?:** no — At $6/GB DRAM nobody accepts a 1000x latency penalty, and the buyer goes back to DIMMs.

**Fatal-flaw candidate:** NAND reads take ~50-100 us vs ~100 ns for DRAM (~1000x). Without Optane-class media the trick only serves workloads that Linux swap + zswap already serve for free, and that media died with a $559M impairment.

*Possible?* yes on Optane media (IMDT 2017-2022); on NAND only as swap-class paging, which Linux already does for free · *Profitable?* no - Optane's death removed the only media that made it competitive · *Doable by this founder?* no

*Business-model lenses:* software licensing

### C-78 — Consumer 'Virtual RAM Booster' App (dead) — ☠ KILLED (R1-UNSUPPORTED: The core value claim, an app that 'adds RAM' beyond what the OS already does, has no evidence. Windows 10+ memory compression, macOS compressed memory (since 10.9) and Android/ChromeOS zram already do this by default [training knowledge]. The only mechanism source cited (Linux zram docs) documents the OS feature, not a third-party gain. The card itself marks rule1_status UNSUPPORTED and wins_axis 'none real'. Selling it would mean a misleading consumer claim with the SoftRAM 95 FTC precedent [UNVERIFIED-T], and it dies the moment 32GB kits fall back toward $100-180.)

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

**Why it could work:** AWS charges $6.669/h for 1 TiB (x2idn.16xlarge, unchanged since 2025) = $4,868/month, or $4.75/GiB-month on-demand. A 1.5 TB box (24 x 64GB used DDR4 RDIMM at $250-370 each, amcompute) costs ~$7.5-10.4k. Renting at $1,200/month against $250 colo and ~$100/month for IPs and spares pays back in ~9-12 months. Hetzner's 2026 increases (up to 37%, citing RAM/NVMe) raise the low-cost competitor's restocking cost while DRAM stays tight.

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [AWS Price List API, EC2 us-east-1 (versions 2025-09 and 2026-10)](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/20261029175634/us-east-1/index.csv) — company, 2026-10. Primary data. All 92 compared On-Demand Linux SKUs (c7i/m7i/m8g/r6i/r7g/r7i/r7iz/r8g/x2idn/u7i) had identical prices in Sep-2025 and Oct-2026. Marginal RAM computes to $2.56-2.62/GiB-month; x2idn.16xlarge (1 TiB) costs $6.669/h.
  - [BuySellRAM market update (via p1-market)](https://www.buysellram.com/blog/ram-market-update/) — industry, 2026-08-31. A U.S. used-RAM buyer publishes DRAMeXchange-based content as lead-gen (DDR4 8Gb avg $44.37).
  - [TweakTown DDR4 +50% Q3-26 (via p1-market)](https://www.tweaktown.com/news/112541/even-ddr4-ram-is-not-safe-from-the-rampocalypse-prices-rose-over-50-percent-in-q3-2026/index.html?type=News) — news, 2026-07. DDR4 contract quoted up to +50% QoQ in Q3-2026.
  - [Servnet DDR5 server memory tracker (via p1-market)](https://www.servnetuk.com/research/ddr5-server-memory-price-tracker-2026) — industry, 2026-08. Street price of a 64GB DDR5 RDIMM about $2,064 (Aug 2026).
  - [DDR4 64GB RDIMM server memory appraisal](https://www.amcompute.com/appraisals/ddr4-64gb-rdimm) — industry, 2026-08. Used 64GB DDR4 RDIMM ~$250-370 over the last 12 months, up ~285% YoY (via search snippet).
  - [Hetzner increases prices from April 1](https://heise.de/-11185981) — news, 2026-02. Up to 37% on cloud, dedicated and object storage from 2026-04-01, citing RAM/NVMe costs (via search snippet).
  - [Hetzner Price Increase 2026 (Capital & Compute)](https://capitalandcompute.net/blog/hetzner-price-increase-2026/) — blog, 2026. Hetzner raised prices in several 2026 waves (via search snippet; per-SKU figures UNVERIFIED).

**Capital tier:** T1 | **Time to first revenue:** 4-8 months: the first 2-3 boxes rented to genomics/EDA users found via forums and university labs. | **Gross margin estimate:** 45-55% at $1,200/month rent with 3-year depreciation; ~10-25% if a glut cuts rents 40%

**US manufacturability:** Hardware sourced from U.S. ITAD/off-lease dealers and hosted in U.S. colo (Ashburn VA or Secaucus NJ). No new manufacturing. Distinct from C-49, which sells new CXL appliances.

**Who is already doing this:** Hetzner (dedicated and auction servers; 2026 increases of up to 37% citing RAM/NVMe) and OVHcloud dedicated servers (US: VA/OR), PhoenixNAP, Latitude.sh, Cherry Servers, Vultr bare metal, used-server dealers. For academic buyers: campus HPC centers and NSF ACCESS allocations provide large-memory nodes free or subsidized [UNVERIFIED-T]. AWS x2idn on Savings Plans/Spot is well below on-demand [UNVERIFIED].

**Wins on which axis, for which buyer:** $/GB-month of rented RAM (about 4x cheaper than AWS on-demand) — for Genomics assembly labs, EDA/simulation contractors, in-memory analytics developers and academic groups that need 1 TB+ of RAM for weeks

**Survives a 2029 glut?:** partially — The AWS on-demand umbrella ($4.75/GiB-month) did not move in the spike and will not move in a glut. But the real competitors are Hetzner/OVH-class hosts, which raised prices in 2026 on RAM costs and will restock cheaply and cut prices when DRAM falls. A 40% rent cut drops gross margin to ~11-22%. DDR4 bought at $3.9-5.8/GB in 2026 is worth a fraction of that in 2028, and the DDR4-era boxes age out on power and CPU.

**Fatal-flaw candidate:** Commodity hosting against established low-cost players, with a hardware-failure and on-call burden incompatible with a day job (remote-hands fees eat margin). Capex is bought at peak DDR4 prices: each box must pay back before end-2027 (landscape F2), and a 2028 glut compresses rents while Hetzner/OVH restock cheaply. Academic buyers often have free campus or ACCESS big-memory nodes.

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
  - [Supplyframe Intelligence: commodities analyzed - SRAM, DRAM, specialty memory](https://intelligence.supplyframe.com/commodities-analyzed-sram-dram-specialty) — company, unknown. Commodity IQ tracks and forecasts DRAM/SRAM/specialty-memory market dynamics, prices and lead times on rolling four-quarter horizons (via search snippet).
  - [Counterpoint Memory Price Tracker and Forecast, July 2026](https://counterpointresearch.com/en/reports/memory-price-tracker-and-forecast-july-2026) — market-research, 2026-07. A paid monthly memory price tracker and forecast. Q3-26 DRAM forecast raised to +10-20% QoQ (via search snippet).

**Capital tier:** T0 | **Time to first revenue:** 4-8 months to an MVP on the Nexar/DigiKey APIs, with 5-10 design-partner OEMs from the founder's network at $150-300/month. First revenue lands around 2Q27, near the forecast price peak, which leaves ~12-18 months of shortage-driven demand before the 2028 turn. | **Gross margin estimate:** 70-85%. COGS is API fees plus a likely commercial licence: Nexar/Octopart and distributor API terms are written for buyers, not for re-display of pricing inside a third-party SaaS [UNVERIFIED-T].

**US manufacturability:** Pure software built and hosted in the U.S.; data partners Nexar (Altium/Renesas), DigiKey and Mouser APIs.

**Who is already doing this:** Paid memory price/lead-time intelligence: Supplyframe Commodity IQ (Siemens; rolling four-quarter DRAM/SRAM/specialty forecasts, via search snippet), Counterpoint Memory Price Tracker and Forecast (monthly, via search snippet), TrendForce/DRAMeXchange, InSpectrum, TechInsights, Omdia, Gartner. BOM-risk and EOL platforms: SiliconExpert (Arrow), Z2Data, Lytica [UNVERIFIED-T]. Free: Mobius Materials report (marketplace lead-gen), rampricesusa, RamRadar, Servnet, nwfella index, 37+ GitHub scrapers.

**Wins on which axis, for which buyer:** Supply security: price and allocation foresight (cost avoidance) — for Procurement/supply-chain leads at U.S. industrial PC, medical device, test-equipment and small system-builder OEMs with $1-50M/year memory spend

**Survives a 2029 glut?:** no — In a 2028-29 glut (DDR5 contract at ~$6.40/GB) buy/hold alerts lose their value and churn spikes. The EOL/lifecycle feature that keeps value is an incumbent commodity (SiliconExpert, Z2Data), so the revenue line dies with the shortage.

**Fatal-flaw candidate:** There is no proprietary data and the forecast layer is already sold. Free trackers cover spot and retail. Supplyframe CIQ and Counterpoint sell memory price and lead-time forecasts. TrendForce/InSpectrum contract data cannot be redistributed. SMB willingness to pay is low and falls with the cycle, and revenue starts near the peak with ~12-18 months before the 2028 turn.

*Possible?* yes - all inputs available via APIs and free sources · *Profitable?* marginal-to-no - an ~$24k MRR ceiling (80 accounts x $300) during the shortage, paid incumbents above, free trackers below, churn at the 2028 turn · *Doable by this founder?* yes - the best founder-fit in the branch, but a weak business

*Business-model lenses:* data product; SaaS

### C-81 — Secondary DRAM Marketplace for Excess Inventory — ☠ KILLED (R4-NO-WINNING-AXIS: Mobius Materials already runs every differentiator on this card as a live product: B2B listing of excess components, authentication, a take-rate model and a spot market for OEMs and CMs. Mobius is in Richmond VA, closed a $3M seed led by Spero Ventures in Dec-2025, reports hundreds of OEM/CM users, and physically inspects every batch at its own Virginia and Hong Kong facilities (Digital Commerce 360, via search snippet). The named buyer pays a marketplace for liquidity and trust, and a cold-start entrant has neither. Its outsourced third-party AS6081 labs are slower and costlier than Mobius's in-house inspection, and Sourcengine, Fusion Worldwide and NetComponents hold the broker flow, so it wins no axis for that buyer. In the shortage the sell side is thin because OEMs hoard, and in a glut the flow turns into a falling-price dump. The only live variant is supplying authentication or data to Mobius, which C-92 (AS6171 lab) and C-86 (index) already cover.)

*Sub-branch:* Procurement & brokerage marketplace · *Materials sense:* c-capital

**What it is:** A B2B web marketplace where OEMs and CMs list excess DRAM/LPDDR/eMMC reels and trays and buyers bid. It adds escrow and third-party AS6081 lab authentication and takes a 5-10% fee.

**Why it could work:** A 4x price spike turns stranded inventory into cash, and liquidity is fragmented among phone-and-email brokers. Spot is thin and broker-driven, and DDR4 spot hit a record $47.04.

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [Mobius Materials $3M seed (via p1-market)](https://www.prnewswire.com/news-releases/mobius-materials-raises-3m-to-combat-one-of-manufacturings-biggest-issues-amid-us-china-trade-tariffs-302643403.html) — news, 2025-12. Richmond VA YC company running an authenticated B2B excess-semiconductor marketplace (ML authentication patent filed). $3M seed in Dec 2025.
  - [Mobius Materials DRAM Market Report (via p1-market)](https://www.mobiusmaterials.com/whitepapers/dram-market-report-2026) — company, 2026. DRAM market report given away (gated) as lead-gen for the marketplace.
  - [nwfella/memory-price-index](https://github.com/nwfella/memory-price-index) — industry, 2026-11-01. Free index of RamRadar retail asks plus TrendForce spot, with analysis dated 2026-11-01. DDR4 8Gb spot record $47.04.
  - [BuySellRAM market update (via p1-market)](https://www.buysellram.com/blog/ram-market-update/) — industry, 2026-08-31. A U.S. used-RAM buyer publishes DRAMeXchange-based content as lead-gen (DDR4 8Gb avg $44.37).
  - [B2B marketplace Mobius Materials raises $3 million](https://www.digitalcommerce360.com/2025/12/16/b2b-marketplace-mobius-materials-3-million-funding/) — news, 2025-12-16. Spero Ventures-led $3M seed; hundreds of OEMs/CMs trade excess parts; every batch inspected at Mobius facilities in Virginia and Hong Kong (via search snippet).

**Capital tier:** T1 | **Time to first revenue:** 6-12 months to first matched trade; needs escrow, authentication-lab partners and insurance. | **Gross margin estimate:** 60-75% of net revenue (5-10% take of GMV)

**US manufacturability:** Software marketplace; physical authentication at U.S. AS6081 test houses; logistics from U.S. CM warehouses.

**Who is already doing this:** Mobius Materials (Richmond VA; $3M seed led by Spero Ventures, Dec-2025; hundreds of OEM/CM users; in-house inspection of every batch in Virginia and Hong Kong; ML-authentication patent filed), plus Sourceability/Sourcengine, Fusion Worldwide, America II, Smith, NetComponents, BrokerForum, ICsource, eBay [UNVERIFIED-T for the brokers].

**Wins on which axis, for which buyer:** Supply security / liquidity — for OEM/CM buyers under allocation, and sellers holding excess memory

**Survives a 2029 glut?:** no — Flow reverses to sellers dumping. Prices fall 60% and take-rate revenue falls with GMV, though volume may rise.

**Fatal-flaw candidate:** An identical, funded incumbent (Mobius) operates in the same region with in-house inspection and hundreds of users. A new marketplace has zero liquidity, which is the only thing its buyer pays for, plus counterfeit liability and two-sided cold-start costs. It wins no axis.

*Possible?* yes - brokers do it daily · *Profitable?* marginal - margin exists, but counterfeit risk and incumbents squeeze it · *Doable by this founder?* no - Mobius is ahead in the same region with funding and IP

*Business-model lenses:* recert/brokerage; marketplace SaaS

### C-82 — Consumer RAM Price Tracker + Upgrade Compatibility Advisor — ☠ KILLED (NOT-A-VENTURE: This is an affiliate/SEO content property that monetizes shortage traffic. The mission allows that only as a bridge revenue line, never the venture, and the card itself says 'no business at the end' and 'side income at best'. At ~$3-6 per affiliate sale [UNVERIFIED-T rates], $10k/month needs ~1,700-3,300 attributed sales a month, while retail demand is being destroyed (TechRadar) at ~$18/GB DDR5 retail (rampricesusa, Sep-2026). It also has no winning axis for its user. PCPartPicker already gives free multi-retailer price history, alerts and compatibility filtering [UNVERIFIED-T], Kingston runs a system configurator, and rampricesusa, RamRadar and 37+ GitHub trackers cover price. Whether Crucial's System Scanner/Advisor stopped after the Feb-2026 exit is still unverified, so even the 'gap' is unproven.)

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

**Survives a 2029 glut?:** no — Traffic falls when panic ends, and affiliate revenue shrinks with ASP (-60%).

**Fatal-flaw candidate:** Affiliate economics: ~2-4% of a ~$150 order is ~$3-6 per sale [UNVERIFIED-T rates], so a salary needs thousands of sales a month. SEO is owned by PCPartPicker and incumbent trackers, and retail demand is being destroyed.

*Possible?* yes · *Profitable?* no - affiliate side income; ~1,700-3,300 attributed sales/month for $10k/month · *Doable by this founder?* yes

*Business-model lenses:* consumer web / affiliate; data product (weak)

### C-83 — Shortage Briefing: Paid Memory-Market Newsletter (bridge only) — ☠ KILLED (NOT-A-VENTURE: The card is a paid newsletter and podcast that labels itself 'bridge only'. The mission says content and education around the shortage is 'a bridge revenue line, never the venture'. Its own numbers ($2-6k MRR at 200-500 subscribers) and its glut answer ('the topic dies') confirm it cannot be the primary pick. The free and paid substitutes are strong: TrendForce press releases, Mobius's free DRAM report, BuySellRAM's DRAMeXchange-based updates, Counterpoint's monthly Memory Price Tracker, SemiAnalysis and Objective Analysis. If used at all, it belongs as a customer-discovery funnel attached to the chosen venture (e.g. C-64), not as a scored concept.)

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

*Possible?* yes · *Profitable?* no - $2-6k MRR bridge income that disappears in a glut · *Doable by this founder?* yes

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
  - [Nordic Semiconductor acquires Memfault](https://www.nordicsemi.com/Nordic-news/2025/06/Nordic-Semiconductor-acquires-Memfault) — company, 2025-06. Memfault (embedded device observability + OTA) acquired and integrated into Nordic's nRF Cloud chip-to-cloud platform (via search snippet).

**Capital tier:** T0 | **Time to first revenue:** 9-15 months: line up an embedded-Linux contractor, then sell 2-3 paid footprint audits ($5-20k) through the founder's manufacturing network. A SaaS tier comes only after repeat audits show demand. | **Gross margin estimate:** 45-65%. Audits are delivered by a contracted embedded-Linux engineer at ~$120-180/h [ESTIMATE]; the founder supplies access, tooling and the report.

**US manufacturability:** Software and services; customers are U.S. industrial, IoT and medical OEMs and their SoM vendors.

**Who is already doing this:** Memfault, acquired by Nordic Semiconductor in Jun-2025 and folded into nRF Cloud as a chip-to-cloud observability/OTA platform (via search snippet). Embedded consultancies (Bootlin, Witekio, Toradex services) [UNVERIFIED-T]. SoM vendor application engineers. Free tooling: Yocto buildhistory, smem, /proc/pressure, upstream zram/zswap.

**Wins on which axis, for which buyer:** $/unit BOM (fewer GB of DRAM per device) — for Hardware product managers at U.S. industrial, IoT and medical-device OEMs shipping 5k-200k units/year

**Survives a 2029 glut?:** no — At glut prices a 1GB step saves ~$2.5/unit, below the cost of re-spin and re-qualification, so demand evaporates.

**Fatal-flaw candidate:** Re-qualification cost and buyer type. A density step-down needs re-validation, including regulatory re-validation for medical. A board re-spin is needed unless the design uses a SoM with a lower-RAM SKU [UNVERIFIED-T]. Low-density (1GB/8Gb) LPDDR4/DDR4 parts are legacy, EOL-pressured and priced at a $/GB premium, so savings are less than linear. Embedded engineers decide, they can run smem/zram themselves for free, and they rarely buy from non-engineers. Revenue is one audit per product line.

*Possible?* yes - standard footprint tooling · *Profitable?* no as a standalone - one-off $5-20k audits per product line, no proven recurring layer, and demand vanishes at glut prices (~$2.5/unit per 1GB step) · *Doable by this founder?* marginal-to-no - needs an embedded-Linux contractor or cofounder to be credible; the day-job network provides access only

*Business-model lenses:* services -> SaaS

## E. Business-model-first concepts (14 cards)

### C-85 — DIMM Health Subscription: predictive replacement + recovered-DDR4 spares pool — ☠ KILLED (RED-TEAM: DD1 (Provenance & Recertified Memory) was KILLED by the four-persona red team: The three FATAL objections hold: the named core buyer (OEM-compatible module makers) already knows its die source from POs, CoCs and package top marks and may self-certify under the proposed FAR rule, and resellers may rely on that free certificate. The die-source library was sampled from the wrong population (old OEM DDR4), keyed wrongly (module P/N) and replicable, so the moat is gone; the C-85 predictive subscript See 05_REDTEAM.md (DD1) and 04_DEEPDIVES/provenance-recert.md §14.)

*Sub-branch:* SaaS + spares pool (third-party maintenance for memory only) · *Materials sense:* c-capital

**What it is:** A per-node agent built on the open-source rasdaemon/Linux EDAC stack streams corrected and uncorrected DRAM error counts per DIMM to a web console. It flags DIMMs trending toward failure (row/page corrected-error growth) and triggers next-business-day shipment of a burn-in-tested replacement from a spares pool of recovered DDR4 RDIMMs bought from U.S. R2 ITADs (Iron Mountain/ITRenew-Sesame, Sims, regional R2 firms). It sells at ~$0.75 per DIMM-month to operators keeping out-of-warranty Dell R740/HPE DL380 Gen10-class DDR4 fleets alive because 2026 DRAM and server prices make a refresh unaffordable.

**Why it could work:** High DRAM prices push enterprises, universities, regional colos and MSPs to stretch DDR4 server life: DDR4 contract prices rose 24% in the 3 months to Oct 2026, and a 64GB RDIMM went from $450 to >$900 on contract. Out-of-warranty fleets lose OEM DIMM replacement. Telemetry is free (rasdaemon logs CE/UE events to SQL and already supports per-page/per-row CE thresholds), so the product is integration plus logistics. Model (e_estimates §10): a 2,400-DIMM customer pays $21.6k/yr. COGS is $8.9k at 2026 recovered-DDR4 prices (58.6% GM) and $3.9k in a glut (81.9% GM), because spares get cheaper. The pool needs only ~$7k of capital per customer. 25 customers = $540k ARR.

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [rasdaemon README.rst and misc/rasdaemon.env](https://github.com/mchehab/rasdaemon) — industry, 2026-11. Opened by E (git clone, last commit 2026-11-01). Logs kernel memory CE/UE events to SQLite/MySQL/PostgreSQL and supports per-page/per-row corrected-error thresholds (example 50) with soft-offline actions. Free, mature DIMM-health telemetry.
  - [DDR4 prices rise as shortages intensify through 2028 (Barclays)](https://www.guru3d.com/story/ddr4-memory-prices-now-also-rise-as-dram-supply-shortages-intensify-through-2028/) — news, 2026-10. DDR4 contract +24% over the 3 months to Oct 2026; shortage into 2028 [cross-reference: URL from a sibling agent's log; not opened by E]
  - [Memory prices surging by 90% from 4Q25 (Counterpoint)](https://www.eetasia.com/memory-prices-surging-by-90-from-4q-2025/) — news, 2026-01. 64GB RDIMM contract $450 (4Q25) to >$900 (1Q26) [cross-reference: URL from a sibling agent's log; not opened by E]
  - [Memory Loss in Commodity Hardware: Predicting DIMM Failures with Machine Learning (IBM Research)](https://research.ibm.com/publications/memory-loss-in-commodity-hardware-predicting-dimm-failures-with-machine-learning) — peer-reviewed, unknown. DIMM failures can be predicted from error logs with ML (via search snippet).
  - [First CE Matters: On the Importance of Long Term Properties on Memory Failure Prediction](https://arxiv.org/pdf/2212.10441) — peer-reviewed, 2022-12. Correctable-error history, including long-term properties, predicts memory failures (arXiv preprint, via search snippet).
  - [From Correctable Memory Errors to Uncorrectable Memory Errors: What Error Bits Tell (SC22)](https://sc22.supercomputing.org/presentation/index-423.htm) — conference, 2022-11. CE bit patterns indicate which DIMMs progress to UEs (via search snippet).
  - [US8468422B2 Prediction and prevention of uncorrectable memory errors](https://patents.google.com/patent/US8468422) — patent, unknown. Patent family on predicting UEs from CEs (via search snippet). An FTO check is needed for a predictive-replacement product.
  - [Park Place Technologies launches ParkView platform for automated hardware triage support](https://prnewswire.co.uk/news-releases/park-place-technologies-launches-parkview-platform-for-automated-hardware-triage-support-662036543.html) — company, 2017. Predictive fault detection plus auto-ticketing, integrated with Park Place TPM contracts (via search snippet).

**Capital tier:** T0 | **Time to first revenue:** 6-12 months: build the agent and console, burn in an initial spares pool on 4-6 used servers, then run paid pilots with 2-3 regional colo or university research-computing fleets. Universities buy on slow procurement cycles. | **Gross margin estimate:** 59% at 2026 spares prices, 82% in a glut. Assumes 1.5%/DIMM-yr replacements including predictive pulls [ESTIMATE]; field studies put uncorrectable errors near ~0.2%/DIMM-yr [UNVERIFIED-T].

**US manufacturability:** No fabrication. U.S. value-add is burn-in test of recovered RDIMMs on owned DDR4 server beds (memtest86+, stressapptest) in a small East Coast space, plus the software. Supply comes from U.S. R2/e-Stewards ITADs.

**Who is already doing this:** Park Place Technologies ParkView Hardware Monitoring / Automated Support (since 2017): 24/7 predictive fault detection with ML and automatic ticket creation, integrated with Park Place maintenance agreements across server OEMs (company PR, via search snippet). Service Express and other TPMs bundle DIMM swaps [UNVERIFIED-T]. Dell iDRAC and HPE iLO raise correctable-error-threshold alerts on in-band hardware [UNVERIFIED-T]. Hyperscalers retire DIMMs on CE trends in-house (IBM, arXiv 2212.10441, SC22 literature). No memory-only predictive subscription found.

**Wins on which axis, for which buyer:** lifecycle length: $/GB-month of keeping installed DDR4 capacity running vs. refreshing at ~$20/GB DDR5 — for Operators of out-of-warranty DDR4 fleets: university research computing, regional colos and MSPs, on-prem SaaS/fintech shops. Also TPM providers as wholesale buyers of the prediction feed plus spares.

**Survives a 2029 glut?:** partially — Margin improves: recovered DDR4 spares fall from ~$4.7 to ~$1.25/GB and GM rises from 59% to 82%. But demand shrinks once cheap DDR5 servers make refresh attractive again and DDR4 fleets age out after ~2029. The fee is priced on uptime, not on DRAM $/GB.

**Fatal-flaw candidate:** It costs more than doing it yourself and loses to bundling. On E's own inputs a 2,400-DIMM fleet self-spares for ~$6.1k/yr (36 x 32GB at $4.7/GB plus shipping) plus a one-time ~$7.2k pool, against a $21.6k/yr fee (~3.6x). rasdaemon and BMC alerts make the predictive layer free, and Park Place ParkView bundles predictive detection and replacement into whole-server TPM, which also covers the disks, PSUs and fans that fail more often than DIMMs.

*Possible?* yes - every component exists (EDAC telemetry, recovered RDIMMs, NBD shipping) · *Profitable?* marginal-to-no - 59-82% GM, but ~$22k ACV is ~3.6x the buyer's DIY spares cost, and ParkView-bundled TPM caps price · *Doable by this founder?* yes - T0, software-led, part-time start; first customers are reachable regionally

*Business-model lenses:* SaaS; recert/brokerage (spares supply)

### C-86 — Memory Cost Escalation Index + EPA clause kit — ☠ KILLED (RED-TEAM: the SaaS-fed Memory Cost Escalation Index leg was killed (panel never reaches the 15 contributors needed to publish; RT-HYP-DD2-01, RT-VC-DD2-01) while the rest of DD2 survives as a downgraded side line. See 05_REDTEAM.md (DD2) and 04_DEEPDIVES/lifecycle-intel.md §14.)

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
  - [DLAD Subpart 16.2 Fixed-Price Contracts (index selection for EPA)](https://www.acquisition.gov/index%2ephp/dlad/subpart-16.2-%E2%80%93-fixed%E2%80%93price-contracts) — government, 2026. The contracting officer selects the most appropriate BLS index after coordinating with the pricing office. A non-BLS index needs documentation of why BLS indices were unsuitable. Combining indices is allowed (via search snippet).
  - [PGI 216.2 Fixed-Price Contracts (216.203-4 EPA guidance)](https://www.acquisition.gov/index%2ephp/dfarspgi/pgi-216.2-fixed-price-contracts) — government, 2026-05. EPA clauses should be simple, use trigger bands, and name the index revision used. COs should use caution because EPA can cause large unanticipated increases (via search snippet).
  - [When hardware costs spike: what your tech contracts should say (Lewis Silkin)](https://www.lewissilkin.com/insights/2026/05/11/when-hardware-costs-spike-what-your-tech-contracts-should-say) — other, 2026-05-11. Most IT procurement price-variation clauses contemplate 3-5% annual moves, not 35-50% jumps. Undefined 'reasonable increase' clauses give vendors latitude (via search snippet).
  - [FRED: PPI by Industry, Semiconductor and Related Device Manufacturing (PCU334413334413)](https://fred.stlouisfed.org/series/PCU334413334413) — government, 2026. The BLS semiconductor PPI exists only at industry and broad product level. No DRAM-specific BLS series surfaced (via search snippet).

**Capital tier:** T0 | **Time to first revenue:** 9-15 months: back-fill 12+ months of index history and publish the methodology, then sign first paid licenses with 2-3 commercial integrators/EMS houses. Federal use follows contract by contract after pricing-office review (DLAD 16.203-4). | **Gross margin estimate:** 57-89% (depends on whether contract data must be licensed)

**US manufacturability:** Pure software/data; no fab dependency.

**Who is already doing this:** TrendForce/DRAMeXchange (public spot board plus paid contract data; the default reference), InSpectrum, TechInsights, Omdia, Supplyframe Commodity IQ and Counterpoint Memory Price Tracker (paid forecasts, via search snippet). BLS PPI covers semiconductors only at the industry level (PCU334413334413), with no DRAM-specific series found. No memory-specific escalation-clause or index-licensing product found [still UNVERIFIED: one targeted search]. Closest analogues are metals surcharge indexes (CRU, Fastmarkets/AMM) [UNVERIFIED-T].

**Wins on which axis, for which buyer:** contract-risk transfer: lower price contingency (cost certainty) on memory-heavy fixed-price contracts — for U.S. system integrators and federal IT contractors on multi-year fixed-price deliveries (servers, rugged computers), regional and tier-2 EMS houses, industrial-PC OEMs (Advantech/OnLogic class) and their procurement counterparts.

**Survives a 2029 glut?:** partially — Index use is two-sided: buyers demand down-adjustments in a glut, and clauses already embedded in multi-year contracts persist. New-license sales slow when prices stop moving.

**Fatal-flaw candidate:** Credibility and adoption mechanics. Commercial counterparties default to TrendForce/DRAMeXchange. Federal contracting officers must pick the most appropriate BLS index first, coordinate with the pricing office, and document why each BLS index is unsuitable (DLAD 16.203-4), so every federal adoption is a case-by-case decision. An index built from distributor list quotes carries basis risk against contract prices and is easy to dismiss or game. Mobius transaction data is a hope, not a deal. Licensing real contract data for redistribution may cost more than early revenue.

*Possible?* yes - distributor APIs and index methodology are standard · *Profitable?* marginal - high GM but a ~$0.3M ARR ceiling unless it becomes the reference index, which requires displacing TrendForce in contract language · *Doable by this founder?* yes - T0, part-time; the founder's day job (manufacturing ops) is the buyer persona

*Business-model lenses:* data product; SaaS

### C-87 — DRAM futures/swap market (index-settled forwards) - tempting, dead — ☠ KILLED (R1-UNSUPPORTED: The core value claim is that OEMs, clouds and makers will trade a cash-settled DRAM contract and so supply liquidity. No evidence supports that, and the precedents point the other way. SGX announced the 'world's first DRAM futures' for 1Q, then 2Q, 2003 (contract cut from 10,000 to 1,000 pieces). Semicon Exchange and Semiconductor Futures Exchange tried the same in 2003, and CBOT, NYMEX and the Pacific Stock Exchange studied memory-chip futures in the late 1980s and early 1990s. No traded DRAM price contract surfaced in a 2026 search (Risk.net, Mondo Visione, EDN, via search snippets). The card itself concedes there is no settlement-grade index, and the incumbent hedge is physical LTAs that simply re-price. The only path below T3 is licensing an index to an existing exchange, and that collapses into C-86 (Memory Cost Escalation Index).)

*Sub-branch:* Financial market infrastructure · *Materials sense:* none

**What it is:** Create cash-settled DRAM forwards or swaps (e.g., a quarterly DDR5 16Gb contract-price swap) so OEMs, clouds, module makers and second-tier DRAM makers can hedge. They would be listed on a CFTC-registered exchange or written OTC through a swap dealer, with the venture as index provider and introducing broker.

**Why it could work:** The exposure is huge and two-sided. DRAM industry revenue was $154.7B in 2Q26 alone. Annualized contract-price volatility is 44-55% (e_estimates §1). Makers are naturally long and buyers naturally short. The 2018-19 and 2022-23 downturns each fell ~60%.

**Evidence:** TRL 2 · Rule 1: UNSUPPORTED (value claim): no evidence that hedgers will trade a DRAM derivative, and prior SGX, Semicon Exchange, SFX and CBOT/NYMEX/PSE efforts did not produce one
  - [SK hynix 3Q26: 14 LTAs, supply booked to 2029](https://www.sammyfans.com/2026/10/28/sk-hynix-q3-margin-hits-record-80-secures-14-ltas-with-memory-supply-booked-to-2029/amp/) — news, 2026-10-28. Physical multi-year LTAs are how DRAM price/supply risk is actually transferred today [cross-reference: URL from a sibling agent's log; not opened by E]
  - [Nanya 3Q26 results; LTAs repriced](https://www.trendforce.com/news/?p=65146) — news, 2026-10-12. Nanya LTAs expired end-June 2026 and repriced >60% higher: LTAs re-price rather than hedge [cross-reference: URL from a sibling agent's log; not opened by E]
  - [TrendForce DRAM spot price board](https://www.trendforce.com/price_dram.html) — industry, 2026-08. The de facto public DRAM price reference is proprietary survey/spot data, not a licensed settlement index [cross-reference: URL from a sibling agent's log; not opened by E]
  - [Mobius Materials: the spot market for semiconductors](https://www.ycombinator.com/companies/mobius-materials) — company, unknown. The nearest thing to a DRAM 'exchange' is a physical surplus marketplace [cross-reference: URL from a sibling agent's log; not opened by E]
  - [TrendForce 2018 PC DRAM contract release](https://press.trendforce.com/node/view/3173.html) — industry, 2018-11. 2018-19 downturn: 8GB module contract $68 -> $61 in one quarter, on the way to -62.5% [cross-reference: URL from a sibling agent's log; not opened by E]
  - [SGX to launch world's first DRAM futures](https://www.risk.net/exchanges/1505681/sgx-launch-worlds-first-dram-futures) — news, 2002. SGX planned a DRAM futures contract after consulting chip makers and users (via search snippet)
  - [Singapore Exchange to launch world's first DRAM futures in first quarter 2003](https://mondovisione.com/media-and-resources/news/singapore-exchange-to-launch-worlds-first-dram-futures-in-first-quarter-2003-2011124/) — news, 2002-09. USD-denominated contract of 10,000 DRAM pieces planned for 1Q 2003 (via search snippet)
  - [SGX to launch DRAM futures in 2Q of this year](https://mondovisione.com/news/sgx-to-launch-dram-futures-in-2q-of-this-year-2011124/) — news, 2003-03. Launch slipped to 2Q 2003 and contract size was cut to 1,000 pieces (via search snippet)
  - [EDN coverage of DRAM futures efforts (one of three EDN results)](https://www.edn.com/?p=4043711) — news, 2003. An analyst said the idea 'just doesn't work'; SFX offered DRAM hedging software and Semicon Exchange planned DRAM futures; CBOT, PSE and NYMEX explored memory futures in the late 1980s and early 1990s (via search snippet; attribution among the three EDN results not confirmed)
  - [KuCoin Futures will list DRAMUSDT and HIMSUSDT stock index perpetual contracts](https://www.kucoin.com/announcement/en-kucoin-futures-will-list-dramusdt-and-himsusdt-stock-index-perpetual-contracts-2026-05-11) — other, 2026-05-11. The 2026 'DRAM' crypto perpetuals are stock-index contracts, not DRAM price futures (via search snippet)

**Capital tier:** T3 | **Time to first revenue:** 36-60 months: index certification, CFTC product approval, and market-maker recruitment before any fee revenue | **Gross margin estimate:** n/a before liquidity (exchange-like margins only at scale)

**US manufacturability:** Financial product; no manufacturing. Would run on a U.S. CFTC-registered DCM/SEF or through a registered swap dealer.

**Who is already doing this:** No traded DRAM price contract was found in 2026, but the idea has repeatedly failed: SGX announced DRAM futures for 1Q to 2Q 2003 (USD, 1,000-piece contract); Semicon Exchange and Semiconductor Futures Exchange (SFX) attempted DRAM futures and hedging platforms in 2003; CBOT, NYMEX and the Pacific Stock Exchange studied memory-chip futures in the late 1980s and early 1990s. The SGX contract's fate is unconfirmed. 'DRAMUSDT' perpetuals listed on KuCoin and BloFin in 2026 are stock-index crypto contracts, not DRAM price contracts. The working hedge is physical LTAs with prepayment (SK hynix: 14 LTAs to 2029).

**Wins on which axis, for which buyer:** price-risk transfer (cost certainty) — for PC/phone OEMs, tier-2 clouds without LTAs, module makers (Kingston, ADATA class); second-tier DRAM makers (Nanya, Winbond) as natural sellers.

**Survives a 2029 glut?:** partially — Hedging demand persists through volatility in both directions, but no liquidity forms without a trusted index at any point in the cycle.

**Fatal-flaw candidate:** No settlement-grade, manipulation-resistant index exists (TrendForce contract data is proprietary and survey-based, and spot is thin at ~1.7x contract). Big players already hedge physically through LTAs that re-price (Nanya +60%). Exchanges have tried DRAM futures since the late 1980s (SGX 2003 most visibly) without creating a market. A DCM or SEF route is T3; the T1 index-licensing route is C-86.

*Possible?* no as a liquid market: the instrument type is standard, but at least four exchange attempts since the late 1980s left no lasting DRAM contract · *Profitable?* no - no fee revenue until liquidity; physical LTAs are the entrenched substitute · *Doable by this founder?* no - T3, regulatory, not software-led

*Business-model lenses:* data product (index); brokerage

### C-88 — DRAM price-cap / allocation-guarantee subscription ('memory insurance') - dead — ☠ KILLED (NOT-A-VENTURE: The venture's whole P&L is a short call on the DRAM contract price. Fair premium for a 12-month at-the-money cap is 16.7-20.7% of capped spend (Black-76 at 44-55% volatility; reproduced by hand: 2N(0.22)-1 = 17.4% before discounting). The 99th-percentile loss is $1.5-2.1M per $1M capped, so profit depends only on which way the price moves. Buyers self-select: they buy caps when they expect increases and skip them when they expect falls, so the product disappears in the 2028 turn. The allocation-guarantee leg needs physical stock the venture can only buy at spot (~1.7x contract), which is C-89's negative-EV trade. This is a financial bet on the cycle that needs a fronting insurer or swap dealer, not an operating business.)

*Sub-branch:* Risk transfer product · *Materials sense:* none

**What it is:** Sell SMB OEMs and system integrators a 12-month subscription that caps the $/GB they pay for DDR4/DDR5, with the venture paying the difference above the cap, and/or guarantees a monthly allocation. It would be funded by premiums and backed by inventory bought ahead or by a reinsurer.

**Why it could work:** Tier-2 buyers without LTAs bear the marginal price and allocation cuts (TrendForce Jan 2026; Micron 10-K allocation language) and would value certainty. Hyperscalers get that certainty through multi-year LTAs; SMBs cannot.

**Evidence:** TRL 3 · Rule 1: SUPPORTED
  - [CSPs lock supply with long-term deals (TrendForce 2Q26)](https://technews.tw/2026/03/31/ai-server-demand-drives-2q26-memory-contract-price-increase-csps-lock-supply-long-term-deals/) — news, 2026-03-31. Hyperscalers lock multi-year supply; tier-2 buyers pay the marginal price [cross-reference: URL from a sibling agent's log; not opened by E]
  - [TrendForce: supply prioritized to strategic OEMs, module makers limited](https://www.trendforce.com/research/download/RP260114IU) — industry, 2026-01-14. Allocation favours strategic customers; tier-2 buyers and module makers are limited [cross-reference: URL from a sibling agent's log; not opened by E]
  - [Micron FY2026 Form 10-K](https://www.sec.gov/Archives/edgar/data/0000723125/000072312526000023/mu-20260903.htm) — company, 2026-10. 'supply allocation decisions that may affect some customers': newcomers cannot buy at contract [cross-reference: URL from a sibling agent's log; not opened by E]
  - [SK hynix 3Q26: 14 LTAs, supply booked to 2029](https://www.sammyfans.com/2026/10/28/sk-hynix-q3-margin-hits-record-80-secures-14-ltas-with-memory-supply-booked-to-2029/amp/) — news, 2026-10-28. Physical multi-year LTAs are how DRAM price/supply risk is actually transferred today [cross-reference: URL from a sibling agent's log; not opened by E]

**Capital tier:** T2 | **Time to first revenue:** 18-30 months: fronting carrier or swap-dealer partner, regulatory filings, and $1.5-2.1M of risk capital per $1M of capped spend before the first policy | **Gross margin estimate:** fair premium 9-21% of capped spend; underwriting margin ~0-10% before adverse selection

**US manufacturability:** Financial product; none.

**Who is already doing this:** No DRAM price-cap product was found [UNVERIFIED: search unavailable]. Market substitutes are LTAs with prepayment and distributor allocation programs.

**Wins on which axis, for which buyer:** cost certainty / supply security — for SMB hardware OEMs, system integrators and tier-2 clouds without LTAs

**Survives a 2029 glut?:** no — Nobody buys caps when prices are falling. During the shortage the writer is short a call on a commodity with 44-55% volatility.

**Fatal-flaw candidate:** The writer is short a call. The fair ATM 12-month premium is ~17-21% of capped spend (9-13% for a cap at 1.25x), which buyers will not pay, and the 99th-percentile year costs $1.5-2.1M per $1M capped. Buyers adversely select on their own price view. The allocation-guarantee leg requires inventory bought at spot (~1.7x contract), i.e. C-89. As indemnity it is state-regulated insurance; as a price swap it falls under CFTC rules.

*Possible?* marginal: only as a reinsurer-backed product at premiums buyers reject · *Profitable?* no - adverse selection plus fat-tailed price moves · *Doable by this founder?* no - capital and regulatory burden

*Business-model lenses:* financial/risk product; brokerage

### C-89 — Buy-and-hold DRAM inventory arbitrage - speculation, not a venture — ☠ KILLED (NOT-A-VENTURE: This is pure price-cycle speculation with no recurring revenue and no moat; the card's own title says so. A newcomer without allocation buys at spot (~$27/GB on 2026-08-31, about 1.69x the $15.99/GB contract). The QoQ contract increase has slowed from +95.5% (1Q26) to +12.5% (4Q26F), so the expected 12-month net return is -46% (-22% if the spot premium persists). A 24-month hold into the A-05 glut ($6.40/GB) loses 108% after carry (e_estimates section 3). The mission names exactly this category, speculation on the price cycle, as never the venture.)

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

*Possible?* yes - anyone can buy spot inventory · *Profitable?* no - negative expected value at spot; positive only for holders of contract allocation · *Doable by this founder?* no: mechanically doable, but negative expected value at the only price the founder can buy (spot)

*Business-model lenses:* recert/brokerage (trading)

### C-90 — DIMM leasing / memory-as-a-service financing for neoclouds — ☠ KILLED (R4-NO-WINNING-AXIS: The lessor has no allocation, so it buys the same street-priced RDIMMs the lessee could buy (the model assumes $1,600 against $1,300 contract and $2,064 street). Its only product is money, and the named buyers already get that money more cheaply inside server-level financing. In 2026 CoreWeave closed an $8.5B A3-rated GPU-backed facility, Lambda a $926M Baa2 term loan (reported at about SOFR+3%), Nebius $775M, and Sharon AI $356M at 9.95% fixed, all at ~60-70% LTV (via search snippets). That is below the card's 14% lessor IRR, and these loans already fund the DRAM inside the servers. A memory-only lessor would therefore lose on $/GB-month, offer no supply security, and match cash-flow timing only at a higher price. It would also be left with the weakest credits that cannot raise GPU-backed debt. On top of that it holds peak-priced residuals into the glut (-29% to -58% IRR if lessees walk at months 18 or 12) and is exposed to a reported neocloud refinancing wall in 2026-28.)

*Sub-branch:* Hardware financing (lessor) · *Materials sense:* c-capital

**What it is:** A lessor buys new DDR5 RDIMMs (or CXL expanders) from Penguin/SMART Modular or Kingston and leases them for 36 months at $/GB-month to neoclouds, AI-inference startups and enterprises that lack LTAs. At lease end it takes the modules back for resale through ITAD channels.

**Why it could work:** Buyers without LTAs face peak prices and allocation limits. Leasing turns a $1,300-2,064 capex per 64GB RDIMM into ~$49/month ($0.76/GB-month), which gives the lessor a 14% IRR with a $260 residual (e_estimates §4). Lenders have shown willingness to finance compute hardware such as GPUs [UNVERIFIED-training].

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [Memory prices surging by 90% from 4Q25 (Counterpoint)](https://www.eetasia.com/memory-prices-surging-by-90-from-4q-2025/) — news, 2026-01. 64GB RDIMM contract $450 (4Q25) to >$900 (1Q26) [cross-reference: URL from a sibling agent's log; not opened by E]
  - [DDR5 server memory price tracker 2026](https://www.servnetuk.com/research/ddr5-server-memory-price-tracker-2026) — industry, 2026-08. Street 64GB DDR5 RDIMM ~$2,064 (Aug 2026) [cross-reference: URL from a sibling agent's log; not opened by E]
  - [CSPs lock supply with long-term deals (TrendForce 2Q26)](https://technews.tw/2026/03/31/ai-server-demand-drives-2q26-memory-contract-price-increase-csps-lock-supply-long-term-deals/) — news, 2026-03-31. Hyperscalers lock multi-year supply; tier-2 buyers pay the marginal price [cross-reference: URL from a sibling agent's log; not opened by E]
  - [TrendForce: supply prioritized to strategic OEMs, module makers limited](https://www.trendforce.com/research/download/RP260114IU) — industry, 2026-01-14. Allocation favours strategic customers; tier-2 buyers and module makers are limited [cross-reference: URL from a sibling agent's log; not opened by E]
  - [DDR4 8Gb fixed price bottomed at $1.30 (Sep 2023)](https://www.kedglobal.com/korean-chipmakers/newsView/ked202310040013) — news, 2023-10-04. Last-cycle trough anchor: contract prices fell roughly 60-65% peak-to-trough [cross-reference: URL from a sibling agent's log; not opened by E]
  - [Lambda Closes $926 Million Senior Secured Term Loan B Facility](https://www.storagenewsletter.com/2026/09/22/lambda-closes-926-million-senior-secured-term-loan-b-facility-backing-gpu-deployment-for-an-investment-grade-customer/) — news, 2026-09-22. GPU-server-secured term loan for a neocloud (via search snippet)
  - [Lambda Secures $926 Million GPU Term Loan With Baa2 Investment-Grade Rating](https://pulse2.com/lambda-secures-926-million-gpu-term-loan-with-baa2-investment-grade-rating/) — news, 2026-09. Baa2 rating; reported maturity 2030-12-31 at SOFR+3% (via search snippet; terms conflict across sources)
  - [Lambda, Sharon AI raise $1.36B in GPU-backed debt on same day](https://baxtel.com/news/lambda-sharon-ai-raise-1-36b-in-gpu-backed-debt-on-same-day) — news, 2026. Sharon AI US$356M GPU-backed SPV facility at 9.95% fixed (via search snippet)
  - [GPU Cluster Financing Data Room (2026)](https://www.peony.ink/blog/gpu-cluster-financing-data-room) — blog, 2026. CoreWeave $8.5B A3-rated facility closed 2026-03-31, described as the first investment-grade GPU-backed financing (via search snippet; vendor blog)
  - [CoreWeave's debt hits $35bn](https://capacityglobal.com/news/coreweaves-debt-hits-35bn/) — news, 2026. LTVs ~60-70% on GPU-backed facilities; 'neocloud refinancing wall' 2026-2028; residual values drive amortization (via search snippet)
  - [Nvidia 9.3% stake in Nebius; GPU-backed debt 2026](https://noqta.tn/en/news/nvidia-9-3-percent-stake-nebius-gpu-backed-debt-2026) — news, 2026. Nebius $775M senior secured facility backed by GPUs it operates (via search snippet)

**Capital tier:** T2 | **Time to first revenue:** 6-12 months to first lease once a credit facility exists (the facility is the hard part) | **Gross margin estimate:** ~21% of lease receipts before cost of funds; ~5-10% net spread after a ~10% facility; scenario lessor IRR -58% to +15%

**US manufacturability:** None; financing. Modules are made in Asia or assembled in the U.S. by Kingston/Penguin from foreign die.

**Who is already doing this:** GPU-backed lenders finance neocloud servers, memory included: CoreWeave $8.5B A3-rated facility (2026-03-31), Lambda $926M Baa2 senior secured term loan B (Sep 2026, reported ~SOFR+3%), Nebius $775M senior secured facility, Sharon AI $356M SPV at 9.95% fixed, Nscale multiple 2026 facilities; LTVs ~60-70% (search snippets). OEM captive finance (Dell Financial Services, HPE Financial Services) leases whole servers [training].

**Wins on which axis, for which buyer:** none against incumbents: server-level GPU-backed debt at ~SOFR+3% to ~10% already funds the DRAM inside the server, below the card's 14% lessor IRR. With no allocation the lessor has no supply-security edge. — for neoclouds and AI-inference startups, mid-size enterprises without memory LTAs

**Survives a 2029 glut?:** no — Once the glut makes a new 64GB RDIMM ~$520, a lessee facing 18 more payments ($879) has every reason to walk or renegotiate, and lessor IRR falls to -29% (walk at month 18) or -58% (month 12). Credit risk is correlated: analysts flag a neocloud refinancing wall for 2026-28 just as the glut would arrive.

**Fatal-flaw candidate:** Residual-value and counterparty risk both sit on the cycle: the lessor is long DRAM bought at peak prices and short credit on neoclouds. OEM captives with cheaper capital already lease whole servers, memory included.

*Possible?* yes - IT leasing is mature · *Profitable?* no - for a small lessor buying at 2026 prices into a 2028 glut · *Doable by this founder?* no - capital-bound

*Business-model lenses:* financing (memory-as-a-service); recert/brokerage (end-of-lease resale)

### C-91 — Authorized-aftermarket die bank for EOL legacy DRAM (title-taking LTB aggregator) — ☠ KILLED (RED-TEAM: DD7 (Authorized-Aftermarket Legacy DRAM Die Bank (+ hi-rel MCMs)) was KILLED by the four-persona red team: No objection was refuted. All three FATALs were confirmed by the model, and they kill L1, the managed die-bank program and the only line this founder could run. Banking bare die costs a board OEM $186k-347k to manage ~$52k of die, 2.9-5.4x a packaged last-time buy plus dry storage. Board OEMs qualify packaged part numbers, and Micross sells the whole bundle direct (EDSP). L3, the title-taking bank, is killed by the c See 05_REDTEAM.md (DD7) and 04_DEEPDIVES/legacy-dram-diebank.md §14.)

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
  - [The world's largest wafer bank has tripled in size at Rochester Electronics](https://www.electronicspecifier.com/around-the-industry/the-worlds-largest-wafer-bank-has-tripled-in-size-at-rochester-electronics) — news, unknown. >10B die in stock on 2-12 inch wafers back to 1968; expansion to ~30B die capacity (via search snippet)
  - [Rochester Electronics and Intelligent Memory ensure the availability of legacy storage solutions](https://www.silicon.co.uk/press-release/rochester-electronics-and-intelligent-memory-ensure-the-availability-of-legacy-storage-solutions) — news, unknown. Partnership covers DRAM ICs and modules from SDRAM to DDR5 plus LPDDR4(x) and managed NAND for industrial use (via search snippet)
  - [Rochester Electronics and SkyHigh Memory: continued support for legacy NAND](https://www.businesswire.com/news/home/20230815306980/en) — company, 2023-08-15. Rochester focuses on 100% authorized legacy/EOL semiconductors; agreement with SkyHigh for mature NAND (via search snippet)
  - [Rochester Electronics Ltd company profile (ADS Group)](https://www.adsgroup.org.uk/members/rochester-electronics-ltd-2//) — other, unknown. Described as authorized by over 70 leading semiconductor manufacturers (via search snippet; directory self-description)

**Capital tier:** T2 | **Time to first revenue:** 30-48 months: 6-18 months to win an OCM authorization (unproven for a startup) and an AS9120/AS6496 quality system; then banked die sell only after OCM and distributor stock runs out (base case: years 3-8) | **Gross margin estimate:** 33-66% on units

**US manufacturability:** Die from Taiwanese specialty makers (Winbond, ESMT, Etron, Nanya KGD programs, open per 01_LANDSCAPE.md 6.1 row 29). Banking, packaging and test in the U.S. at Integra (KS), QP Technologies (CA) or Micross (Apopka FL, verified in batch 10), though Micross is also a direct competitor in authorized die.

**Who is already doing this:** Rochester Electronics (Newburyport MA): world's largest wafer/die bank (>10B die, expansion to ~30B), described as authorized by 70+ OCMs, 15B devices and 200k part numbers in stock; legacy DRAM (SDRAM to DDR5, LPDDR4x) through an Intelligent Memory partnership and legacy NAND through SkyHigh Memory (2023). Micross (authorized die/wafer distributor, DRAM on line card, its own AS6171 lab). Intelligent Memory and Alliance Memory (long-lifecycle DRAM OCM brands). Micron Manassas long-lifecycle DDR4/LP4 via distribution since 2026-05-22. Distributors' bonded stock.

**Wins on which axis, for which buyer:** lifecycle length and supply security: authorized, traceable legacy DRAM after EOL — for DoD sustainment programs and DMSMS offices, avionics (DO-254), rail signaling, medical-device OEMs

**Survives a 2029 glut?:** yes — Demand is driven by EOL and requalification cost, not DDR5 prices, and a glut cheapens LTB wafers. But a glut also lowers the independent-market price that caps aftermarket pricing (DMSMS aftermarket at 1.5-5x, 01_LANDSCAPE.md 7.3) and brings more authorized DDR4 (Micron Manassas, Winbond). The main risk is inventory that never sells (bear IRR -7%).

**Fatal-flaw candidate:** OCMs grant aftermarket authorization to proven firms with capital and quality systems. Rochester already holds >10B banked die, 70+ OCM authorizations and a legacy-DRAM partnership with Intelligent Memory, so it is the firm OCMs call first. A startup can neither win the authorization nor fund $0.6M per part ($2M+ for a portfolio). Without authorization the venture is just an independent distributor, which DFARS ranks last.

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
  - [SMT Corp expands ISO/IEC 17025 and SAE AS6171 accreditations to UK laboratory](https://www.newswire.ca/news-releases/smt-corp-expands-iso-iec-17025-and-sae-as6171-accreditations-to-uk-laboratory-strengthening-global-counterfeit-detection-capabilities-831055324.html) — company, 2025-12-08. Sandy Hook CT lab: ANAB 17025 + AS6171 HRL2; DLA QTSL-recognized; UK lab MRL2 (via search snippet; company release)
  - [Micross Clearwater FL ISO/IEC 17025:2017 AS6171 accreditation](https://www.micross.com/uploads/817a2759-d1b0-4f06-a3ea-1512595fd67d/Clearwater-FL_ISO-IEC-17025-20170-AS6171.pdf) — company, unknown. Scope includes a 'RAM Tester' under electrical test (AS6171/7, AS6081) (via search snippet)
  - [Micross Counterfeit Mitigation](https://www.micross.com/advanced-services/counterfeit-mitigation) — company, unknown. ITAR-registered lab, 17025/AS6171/AS6081; full-lot AS6171 testing as fast as 2 weeks (via search snippet)
  - [A2 Global Electronics USA AS6171 / ISO/IEC 17025 scope](https://a2globalelectronics.com/wp-content/uploads/2025/12/A2GlobalElectronicsUSACertScope22Dec2027.pdf) — company, 2025-12. Accredited AS6171 lab incl. AS6171/7 electrical test with ATE (via search snippet)
  - [Vyrian (CB Insights profile)](https://www.cbinsights.com/company/vyrian) — other, unknown. ISO 17025 lab in Houston and Hong Kong running at-speed AS6171 test flows (via search snippet)
  - [White Horse Laboratories Cleveland facility achieves DLA certification](https://www.emsnow.com/?p=45202) — news, unknown. DoD/DLA Qualified Commercial Test Laboratory for AS6171 counterfeit testing on FSC 5961/5962 (via search snippet)
  - [APC Technology Group and SMT Corp: component procurement and testing to AS6171](https://apctech.com/news/apc-technology-and-smt-corp.html) — company, unknown. AS6171 mandated by DLA since January 2022 (via search snippet)

**Capital tier:** T1 | **Time to first revenue:** 12-18 months: equipment install, quality system, proficiency testing and ANAB 17025/AS6171 scope assessment; first broker/EMS lots; DLA listing later | **Gross margin estimate:** -34% at 20 lots/month, 22% at 40, 41% at 60, 54% at 90 (e_estimates section 6)

**US manufacturability:** U.S. lab services; no fab.

**Who is already doing this:** SMT Corp (Sandy Hook CT, 72,000 sq ft; ANAB ISO/IEC 17025 + AS6171 HRL2; DLA QTSL-recognized; UK lab accredited Dec 2025). Micross Clearwater FL (17025, AS6171, AS6081, ITAR; RAM tester in its electrical scope; full-lot AS6171 in ~2 weeks). A2 Global Electronics (FL/Singapore/Netherlands; AS6171/7 ATE electrical). Vyrian (Houston/Hong Kong 17025 lab, at-speed AS6171 flows). White Horse Laboratories (Cleveland; DLA-approved Qualified Commercial Test Laboratory for FSC 5961/5962). Integra Technologies and Alter Technology [UNVERIFIED-training]. Mobius Materials' ML authentication; the ERAI/GIDEP ecosystem.

**Wins on which axis, for which buyer:** supply security / authenticity (counterfeit-risk reduction with documentation) — for AS6081 independent distributors, defense EMS and primes' purchasing departments, OEMs buying broker DRAM during the shortage

**Survives a 2029 glut?:** partially — Broker buying and counterfeit volume fall once authorized stock returns (lots down maybe 30-50% [ESTIMATE]). DFARS-driven testing of obsolete parts continues.

**Fatal-flaw candidate:** Crowded, accreditation-heavy services market. SMT Corp (CT, AS6171 HRL2, DLA QTSL) is in the target corridor and Micross offers full-lot AS6171 with RAM test in ~2 weeks. Below 36 lots/month the lab loses money (-34% GM at 20). The founder cannot run it without a hired AS6171 test engineer and ~$650k; at-speed DDR5 component test equipment could push capex higher [STILL-UNVERIFIED]. Die-origin flagging uses standard AS6171 decap/die-marking methods incumbents already run, so it is not a moat.

*Possible?* yes - routine lab methods · *Profitable?* marginal-to-no: loses money below 36 lots/month and must take share from accredited, DLA-recognized incumbents · *Doable by this founder?* marginal - needs a technical hire and ~$0.65M

*Business-model lenses:* defense-first; services; data product (test-report and die-ID database)

### C-93 — 'Compliant memory' federal reseller on GSA MAS / SEWP (compliance-as-a-product) — ☠ KILLED (R4-NO-WINNING-AXIS: The card's only differentiator, 'compliant memory', is something every reseller of Samsung, SK hynix, Micron or Kingston product already meets at no cost. TAA treats Korean, Taiwanese and Japanese memory as equal above $174k (FAR 25.402). The BAA component test is waived for COTS (FAR 25.001). The FAR Council's proposed rule (FAR Case 2023-008, FR 2026-03065, 2026-02-17; not final; statutory effect 2027-12-23) puts the same duty on every offeror and offers a disclosure safe harbor (law-firm alerts, via search snippet). So compliance is a feature everyone has, not a product. Against CDW-G, Carahsoft and the 2,115 SEWP VI holders (awarded Jun-2026, ordering from 2026-11-01, no on-ramp schedule found), a new entrant has no SEWP seat, no MAS track record and no volume pricing. It loses on price and access and only ties on compliance and small-business status, so it wins no axis. Whatever §5949 creates that buyers would pay for is verification (C-64), not resale margin.)

*Sub-branch:* Federal reseller (NDAA 5949 / TAA / BAA) · *Materials sense:* none

**What it is:** A small-business federal reseller that sells memory upgrades and memory-heavy servers to agencies through GSA's Multiple Award Schedule and NASA SEWP. The pitch is 'certified U.S.-supply-chain' memory: TAA-compliant, CXMT/YMTC-free under NDAA FY2023 §5949, Micron Manassas DDR4 where available, with provenance paperwork.

**Why it could work:** §5949 bans CXMT/YMTC/SMIC content in federal purchases from 2027-12-23, with rising political salience (Senate pressure on Apple, July 2026). The Buy American Act gives small businesses a 30% evaluation preference below the TAA threshold (FAR 25.106).

**Evidence:** TRL 9 · Rule 1: SUPPORTED for VAR mechanics; the core value claim (a compliance premium) is contradicted by FAR 25.402/25.001 and the 2026 proposed rule
  - [Apple, China memory and the 2027 federal procurement ban](https://xenospectrum.com/en/apple-china-memory-federal-procurement-ban-2027/) — news, 2026-07. NDAA FY2023 Sec. 5949 ban on CXMT/YMTC/SMIC-containing products in federal buys from Dec 2027 [cross-reference: URL from a sibling agent's log; not opened by E]
  - [GSA-Acquisition-FAR repository (FAR through FAC 2025-06)](https://github.com/GSA/GSA-Acquisition-FAR) — government, 2026-03-30. Opened by E (git clone). grep of all 3,945 FAR DITA files finds no text implementing NDAA FY2023 Sec. 5949 ('covered semiconductor', CXMT, YMTC, SMIC)
  - [GSA-Acquisition-DFARS repository](https://github.com/GSA/GSA-Acquisition-DFARS) — government, 2026-06-02. Opened by E (git clone). No Sec. 5949 implementing text in 3,320 DFARS DITA files as of the 2026-06-02 snapshot
  - [FAR 4.2101 'reasonable inquiry' (Section 889)](https://github.com/GSA/GSA-Acquisition-FAR/blob/master/dita/4.2101.dita) — government, 2025-10-01. Opened by E. 'Reasonable inquiry ... excludes the need to include an internal or third-party audit': the precedent a Sec. 5949 rule would likely copy
  - [FAR 25.402 trade-agreement thresholds](https://github.com/GSA/GSA-Acquisition-FAR/blob/master/dita/25.402.dita) — government, 2025-10-01. Opened by E. WTO GPA threshold $174,000: above it Korean/Taiwanese/Japanese memory competes equally with U.S.-made
  - [FAR 25.001 Buy American COTS waiver](https://github.com/GSA/GSA-Acquisition-FAR/blob/master/dita/25.001.dita) — government, 2025-10-01. Opened by E. The domestic content test is waived for COTS items, so U.S. die gets no extra BAA credit inside a COTS module
  - [FAR 25.106 BAA evaluation factors](https://github.com/GSA/GSA-Acquisition-FAR/blob/master/dita/25.106.dita) — government, 2025-10-01. Opened by E. 20% (large business) / 30% (small business) evaluation preference for domestic offers, applicable only where TAA does not apply
  - [FAR 52.211-5 Material Requirements](https://github.com/GSA/GSA-Acquisition-FAR/blob/master/dita/52.211-5.dita) — government, 2025-10-01. Opened by E. 'New' means previously unused components; used/reconditioned supplies need contracting-officer acceptance
  - [Federal Acquisition Regulation: Prohibition on Certain Semiconductor Products and Services (FAR Case 2023-008, proposed rule)](https://www.federalregister.gov/documents/2026/02/17/2026-03065/federal-acquisition-regulation-prohibition-on-certain-semiconductor-products-and-services) — government, 2026-02-17. Proposed FAR 40.20X with a solicitation provision and contract clause implementing NDAA FY2023 §5949. Not final. Statutory effective date 2027-12-23 (via search snippet; page not reachable).
  - [FAR Council Proposes Rule to Prohibit Acquisition of Semiconductors from China and Countries of Concern (Mayer Brown)](https://www.mayerbrown.com/en/insights/publications/2026/03/far-council-proposes-rule-to-prohibit-acquisition-of-semiconductors-from-china-and-countries-of-concern) — other, 2026-03-03. Comments due 2026-04-20. Applies to COTS and micro-purchases. Safe harbor for timely, accurate disclosure. Prospective, with no rip-and-replace (via search snippet).
  - [Section 5949 Proposed Rule Puts the FAR Council's Chips on the Table (Crowell)](https://www.crowell.com/en/insights/client-alerts/section-5949-proposed-rule-puts-the-far-councils-chips-on-the-table) — other, 2026-02. Law-firm analysis of the proposed rule, including disclosure duties that extend to non-federal customers (via search snippet).
  - [More SEWP for contractors as NASA expands total awards (Federal News Network)](https://federalnewsnetwork.com/contractsawards/2026/06/more-sewp-for-contractors-as-nasa-expands-total-awards/) — news, 2026-06. SEWP VI awarded to ~2,115 holders, $60B ceiling, ordering 2026-11-01 to 2036-10-31. SEWP V extended while protests resolved (via search snippet).

**Capital tier:** T1 | **Time to first revenue:** 18-24 months: GSA MAS only (SEWP VI awarded Jun-2026, no on-ramp scheduled), then first small-business set-aside orders against hundreds of incumbent small-business VARs | **Gross margin estimate:** 6-10%

**US manufacturability:** Resale only; modules may be U.S.-assembled (Kingston, Penguin) from foreign die.

**Who is already doing this:** 2,115 NASA SEWP VI contract holders (awarded Jun-2026, ordering from 2026-11-01; via search snippet), including many small, 8(a), SDVOSB and HUBZone VARs; CDW-G, Carahsoft and GSA MAS IT schedule holders [UNVERIFIED-training]; Micron and Kingston through their channels

**Wins on which axis, for which buyer:** supply security / compliance documentation — for federal civilian and DoD IT buyers; prime integrators

**Survives a 2029 glut?:** partially — Compliance demand persists, but VAR margins on cheaper memory compress further.

**Fatal-flaw candidate:** No winning axis. §5949 rewards 'not Chinese', and every Samsung, SK hynix, Micron or Kingston reseller already meets it. The FAR Council's proposed rule (FAR Case 2023-008, 2026-02-17; not final; effective 2027-12-23 by statute) puts the same duty on every offeror and gives a disclosure safe harbor. TAA lets allied memory compete equally above $174k (FAR 25.402), and the BAA component test is waived for COTS (FAR 25.001). SEWP VI was awarded to 2,115 holders in Jun-2026 and is closed to a newcomer until an unscheduled on-ramp. The result is a 6-10% VAR margin with no vehicle and no price edge: $1.5-2.5M of sales per $150k of gross profit (e_estimates §7).

*Possible?* yes - standard VAR model, but SEWP VI is closed to newcomers until an on-ramp and MAS needs a track record · *Profitable?* no - commodity margin; compliance confers no premium · *Doable by this founder?* marginal - slow vehicle access, working capital ~$185-310k

*Business-model lenses:* defense-first; recert/brokerage (resale); compliance-as-a-product

### C-94 — STTR vehicle on a national-lab / university memory patent (lab-patent studio) — ☠ KILLED (DUPLICATE: The card itself says C-06 (Sandia HZO FeRAM) and C-07 (Penn/AFRL AlScN license plus STTR) card the device plays, and both survived audit (batch_01, KEEP_WITH_CORRECTIONS). This vehicle options the same technologies, bids the same topics (DARPA DV017, AF254-D0806) and sells to the same buyers (AFRL/DARPA program offices, space primes). The portfolio wrapper adds no product a buyer pays for. Revenue arrives only when one of those device plays reaches Phase III, ~46 months out, and A-04 does not count grants as revenue. The Purdue In2O3 option is a TRL 3-4 research result that belongs with C-01. The one transferable insight should be folded into C-06/C-07 as their funding structure: STTR lets the lab or university PI lead while the founder keeps their day job. SBIR/STTR has been reauthorized through 2031-09-30 (S.3971, signed 2026-04-13, via search snippet), so that structure is live.)

*Sub-branch:* University/lab patent license -> STTR -> defense Phase III · *Materials sense:* mixed:a+c

**What it is:** A small business takes low-cost options on 2-3 lab memory technologies: Sandia's HZO FeRAM and ferroelectric tunnel junctions from its trusted MESA 200mm fab, the Penn/AFRL AlScN 600 C ferroelectric-diode NVM, and Purdue's ALD In2O3 BEOL ferroelectric transistors. It files DoD/NASA STTRs with the inventing researcher as STTR PI, aiming at Phase III sole-source sales or a sublicense to space/defense memory suppliers (Frontgrade, Honeywell SSEC, BAE).

**Why it could work:** STTR lets the PI be employed by the research institution (Penn and Purdue as universities; Sandia as an FFRDC [UNVERIFIED-training that FFRDCs qualify]), so the founder can keep their day job while the vehicle wins non-dilutive money. SBIR/STTR were reauthorized through 2031-09-30 (S.3971, signed 2026-04-13, after a ~6-month lapse). Defense topics for exotic NVM exist: DARPA DV017 (~$1.2M Direct-to-Phase-II, 2026) and USAF AF254-D0806 (500 C NVM). Options cost ~$1-10k (p1-ip), and Phase III awards can be sole-source. Sandia's HZO FeRAM is at 200mm wafer scale (TRL ~4-5).

**Evidence:** TRL 4 · Rule 1: SUPPORTED
  - [Sandia: Facing radiation challenges head on](https://www.sandia.gov/research/news/evolving-semiconductor-technology-for-national-security-applications/) — government, 2026-05-13. HfO2/HZO rad-hard FeRAM at 200mm and binary/32-state FTJs integrated in Sandia's trusted MESA fab (LDRD): TRL ~4-5 national-lab memory IP [cross-reference: URL from a sibling agent's log; not opened by E]
  - [Turning up the heat on data storage (Penn + AFRL AlScN)](https://www.engineering.upenn.edu/stories/turning-up-the-heat-on-data-storage/) — news, 2024-05. AlScN ferroelectric-diode NVM operating at 600C (Nature Electronics 2024); Penn/AFRL co-invention [cross-reference: URL from a sibling agent's log; not opened by E]
  - [Purdue 3-tier monolithic 3D ALD In2O3 platform on 200mm](https://engineering.purdue.edu/ECE/News/2026/purdue-researchers-build-3d-chip-platform-for-faster-more-efficient-ai-computing) — news, 2026-09-16. ALD In2O3 BEOL transistors incl. ferroelectric tiers on 200mm Si (>100,000 devices across 52 dies) [cross-reference: URL from a sibling agent's log; not opened by E]
  - [DARPA SBIR DPA26BZ04-DV017 Non-Volatile Memory for Extreme Environments](https://www.darpa.mil/research/programs/non-volatile-memory-extreme-environments) — government, 2026-07. ~$1.2M Direct-to-Phase-II memory topic, opened 2026-07-22 and closed 2026-08-19 [cross-reference: URL from a sibling agent's log; not opened by E]
  - [USAF SBIR AF254-D0806 500C-capable kB-scale NVM](https://www.sbir.gov/topics/12036) — government, 2025. USAF topic citing ferroelectric-diode memory stable to 600C [cross-reference: URL from a sibling agent's log; not opened by E]
  - [Everspin earns $40M MRAM deal for defense memory services](https://electronics360.globalspec.com/article/23702/everspin-earns-40-million-mram-deal-for-defense-memory-services) — news, 2026-04. Defense pays for on-shore memory capability through prime subcontracts (Amentum), awarded to an incumbent with a fab [cross-reference: URL from a sibling agent's log; not opened by E]
  - [Trump signs SBIR/STTR reauthorization bill into law (UW Federal Relations)](https://www.washington.edu/federalrelations/2026/04/14/trump-signs-sbir-sttr-reauthorization-bill-into-law/) — other, 2026-04-14. Small Business Innovation and Economic Security Act (S.3971) signed 2026-04-13, reauthorizing SBIR/STTR through 2031-09-30 (via search snippet).
  - [SBIR/STTR programs reauthorized after six-month lapse (Mondaq)](https://www.mondaq.com/unitedstates/government-contracts-procurement-ppp/1774902/sbirsttr-programs-reauthorized-after-six-month-lapse) — other, 2026-04. Lapse from 2025-09-30. Agencies resumed solicitations. Annual proposal caps in FY2027 (via search snippet).

**Capital tier:** T1 | **Time to first revenue:** ~46 months to first Phase III/customer revenue if every step succeeds the first time; grants before that are funding, not revenue (A-04) | **Gross margin estimate:** n/a until product; Phase III device sales 50-70% if they come

**US manufacturability:** Sandia MESA (trusted, but a government fab not open for production); SkyWater S130 / Fab 25 for a commercial path. Bayh-Dole and DOE U.S.-manufacture preferences align with U.S. production.

**Who is already doing this:** C-06 (Sandia HZO FeRAM chip) and C-07 (AlScN license plus STTR) card the device plays. Incumbents: Infineon rad-hard F-RAM, Frontgrade/Everspin Toggle MRAM. Many university spinouts run this STTR pattern.

**Wins on which axis, for which buyer:** non-volatility plus radiation/temperature tolerance (supply security for space and hypersonics) — for AFRL/DARPA program offices, space primes, hypersonic and Venus/geothermal sensor integrators

**Survives a 2029 glut?:** yes — Rad-hard and extreme-environment NVM is priced per part to defense buyers and is indifferent to DDR5 prices.

**Fatal-flaw candidate:** It duplicates C-06 and C-07, and it is the grant farm the founder says they do not want. The chance of customer revenue is ~3% per topic attempt and ~15% after five (e_estimates §8). First revenue lands ~46 months out, past the 36-month ceiling. STTR also requires the small business itself to perform >=40% of the work [UNVERIFIED-training], so the vehicle needs its own technical staff or paid lab time, not just a lab PI. It depends on a PI and a fab it does not control.

*Possible?* yes - option/STTR/Phase III mechanics are routine; device TRL 3-5 · *Profitable?* marginal - niche defense NVM can be profitable for whoever reaches Phase III, rarely within 4 years · *Doable by this founder?* marginal - they can run the company shell and proposals, not the science or the small business's required >=40% work share

*Business-model lenses:* university/lab patent license; defense-first; fabless->foundry (later)

### C-95 — SBA/search-fund acquisition of a small memory reseller at peak earnings - tempting, dangerous — ☠ KILLED (NOT-A-VENTURE: On the card's own terms ($4.2M price = 3.5x $1.2M shortage EBITDA, 90% SBA 7(a) debt, ~$612k/yr debt service), DSCR is 1.96 in 2026, 0.65 in a normal year and 0.33 in the glut (e_estimates §9). The loan is repaid only if shortage pricing lasts most of a 10-year term. That makes it a leveraged, personally guaranteed long position on DRAM prices, not a venture with a product axis, and no software upside closes a 0.65 DSCR. It also fails QB-INCOMPLETE: no target is named or confirmed for sale. Under SOP 50 10 8/8.1 the 10% injection (~$420k) may draw at most half from 'limited sources' such as full-standby seller notes and <20% minority investors (via search snippet). The founder, with under $50k, would therefore need a controlling co-buyer bringing ~$210k+ cash and a guarantee. Buying the same business at trough multiples in 2028-29 would be a different, later concept.)

*Sub-branch:* Acquisition (ETA) of a memory business · *Materials sense:* c-capital

**What it is:** Buy an existing U.S. server-memory reseller, used-memory buyer or small module brand (the A-Tech / NEMIX / Memory4Less / TechMikeNY class [UNVERIFIED-training names; none confirmed for sale]) with ~$1.2M of 2026 EBITDA. Finance it 90% with an SBA 7(a) loan and 10% equity from the founder and co-investors, then grow it with software (pricing, provenance ledger, e-commerce).

**Why it could work:** Revenue is immediate: day-one recurring B2B customers, inventory and supplier relationships. A software operator can improve a sleepy business. The Crucial exit (announced Dec 2025) reshuffled the consumer/SMB memory channel, and DDR4 prices are still rising.

**Evidence:** TRL 9 · Rule 1: N/A (financial structure); the value claim depends on shortage EBITDA persisting
  - [Micron announces exit from Crucial consumer business](https://www.storagenewsletter.com/2025/12/05/micron-announces-exit-from-crucial-consumer-business/) — news, 2025-12-05. Crucial exit announced 2025-12-03: the consumer/SMB memory channel is reshuffling [cross-reference: URL from a sibling agent's log; not opened by E]
  - [DDR4 prices rise as shortages intensify through 2028 (Barclays)](https://www.guru3d.com/story/ddr4-memory-prices-now-also-rise-as-dram-supply-shortages-intensify-through-2028/) — news, 2026-10. DDR4 contract +24% over the 3 months to Oct 2026; shortage into 2028 [cross-reference: URL from a sibling agent's log; not opened by E]
  - [DDR4 8Gb fixed price bottomed at $1.30 (Sep 2023)](https://www.kedglobal.com/korean-chipmakers/newsView/ked202310040013) — news, 2023-10-04. Last-cycle trough anchor: contract prices fell roughly 60-65% peak-to-trough [cross-reference: URL from a sibling agent's log; not opened by E]
  - [Analyst cycle views incl. Bloomberg Intelligence bear case](https://www.kucoin.com/blog/2027-memory-chip-boom-sk-hynix-samsung) — news, 2026. BI: shortage peaked 2Q26, oversupply possible in 2028; others see tightness to 2Q28 [cross-reference: URL from a sibling agent's log; not opened by E]
  - [Best practices: a review of equity injection requirements under SOP 50 10 8 (Starfield & Smith)](https://starfieldsmith.com/2025/05/best-practices-a-review-of-equity-injection-requirements-under-sop-50-10-8/) — other, 2025-05. 10% minimum injection of total project cost for changes of ownership. Seller note at most half, on full standby for the loan term (via search snippet).
  - [SBA SOP 50 10 8.1 change-of-ownership equity, DSCR and QoE guide (Beancount blog)](https://beancount.io/blog/2026/09/23/sba-sop-50-10-8-1-change-of-ownership-equity-dscr-qoe-guide) — blog, 2026-09-23. SOP 50 10 8.1, effective 2026-10-01, keeps the 10% injection and treats <20% non-controlling investor equity as a limited source under the shared 50% cap (via search snippet; secondary).

**Capital tier:** T2 | **Time to first revenue:** Revenue on day one after close, but sourcing, diligence and SBA close take ~6-9 months | **Gross margin estimate:** 15-25% (reseller margins)

**US manufacturability:** Existing U.S. operation (testing and resale); no fab.

**Who is already doing this:** Search funds and ETA buyers generally; ITAD consolidators such as Iron Mountain ALM (ITRenew) [UNVERIFIED-training].

**Wins on which axis, for which buyer:** time-to-revenue (acquired), not a product axis — for the target's existing customers: SMB IT, refurbishers, MSPs, homelab/gaming buyers

**Survives a 2029 glut?:** no — At 3.5x shortage EBITDA, debt service is ~$612k/yr. DSCR is 1.96 in 2026, 0.65 in a normal year and 0.33 in a glut (e_estimates §9), which means default with an SBA personal guarantee.

**Fatal-flaw candidate:** Buying cyclical peak earnings with leverage. Shortage-inflated EBITDA reverts, and the SBA personal guarantee ties the founder's personal assets to the 2028 glut.

*Possible?* yes - SBA acquisitions of small distributors are routine · *Profitable?* no - at 2026 prices the deal cannot service its debt even in a normal year (DSCR 0.65); maybe yes if bought at trough multiples · *Doable by this founder?* no - equity gap (SOP 50 10 8.1 caps seller notes plus minority-investor equity at half the 10% injection) and guarantee risk

*Business-model lenses:* recert/brokerage; module/appliance (acquired); SaaS (bolt-on)

### C-96 — Acquire the 3D XPoint/Optane IP estate and license it (business-model Optane revival) - tempting, dead — ☠ KILLED (R3-FAB/T4: The card concedes that IP without a line is worthless. The only XPoint line (Lehi) went to TI in 2021 for $900M cash plus ~$600M of tools and now runs analog. Micron quit, citing 'insufficient market validation' after ~$545M of underutilization charges, and Intel lost >$7B. Any product path therefore needs a new 20nm-class crosspoint PCM fab, which is >$1B (T4, A-11). The licensing-only path fails on its premise. There is no single estate to buy: the IP reportedly passed to Micron with royalty-free licenses to Intel, and an Ovshinsky bankruptcy trust sued both over title in 2020 (Blocks & Files, via snippet). A 2026 search found no revival or licensing activity. At the canonical $6.40/GB glut the cost gap that sank Optane closes again.)

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
  - [3D XPoint patent suit against Intel and Micron (Blocks & Files)](https://blocksandfiles.com/2020/10/05/3d-xpoint-patent-suit-intel-micron/) — news, 2020-10-05. Ovshinsky estate trust lawsuit alleging Intel lacks rights to core 3D XPoint IP and that IP was moved to Micron with royalty-free licenses to Intel. The estate's title is contested (via search snippet).
  - [Intel Optane: A Restrictive Licensing Model and the Half Billion Dollar Operating Loss in 2020 (Koutoupis)](https://koutoupis.com/2022/02/21/intel-optane-a-restrictive-licensing-model-and-the-half-billion-dollar-operating-loss-in-2020/) — blog, 2022-02-21. Restrictive licensing contributed to Optane's failure (via search snippet).

**Capital tier:** T4 | **Time to first revenue:** 60+ months; only via a licensee that would also need a new line | **Gross margin estimate:** licensing ~90% if a licensee existed; none expected

**US manufacturability:** No XPoint line exists anywhere: Lehi was sold to TI and converted to 65/45nm analog.

**Who is already doing this:** Nobody. A 2026-11-01 search found no XPoint revival or licensing program. SanDisk's 3D-matrix/HBF work and imec selector-only-memory research are the nearest descendants (see C-25, C-53).

**Wins on which axis, for which buyer:** $/GB vs. DRAM plus persistence — for CXL memory-tier buyers (hyperscalers, SAP HANA/database hosts)

**Survives a 2029 glut?:** no — At glut DDR5 prices ($6.4/GB, $1.6 severe), the XPoint cost gap, which never paid off even against $3-5/GB DRAM, closes again.

**Fatal-flaw candidate:** IP without a line is worthless, and the line is T4. No fab runs XPoint: Lehi went to TI and was converted. There is no clean estate to buy, because the IP sits with Micron with royalty-free licenses to Intel, and an Ovshinsky bankruptcy trust contested title in 2020. Micron and Intel both exited. Out-licensing memory IP takes a decade even for the best-run licensor.

*Possible?* marginal - the technology shipped (2017-22), but there is no clean estate for sale and no line to use it on without a >$1B fab · *Profitable?* no · *Doable by this founder?* no

*Business-model lenses:* IP licensing (acquired estate); fabless->foundry (impossible)

### C-97 — CXL memory-tiering integration practice (consulting -> managed tuning) — ☠ KILLED (DUPLICATE: This is the services packaging of C-49 (TB-Class CXL Node, KEEP_WITH_CORRECTIONS in batch_07). It has the same buyers (EDA, genomics, SAP HANA/in-memory DB, HPC), the same hardware (Samsung CMM-D, Micron CZ122, SK hynix CMM-DDR5) and the same tuning stack (weighted interleave, DAMON, HMSDK). Its own lens list includes 'module/appliance (VAR)', and batch_07 already flagged the overlap. The cheaper-capacity leg is C-44 (DDR4 second-life CXL expander). DDR5 CXL modules carry the same DRAM plus a controller, so they do not win on $/GB. Marvell's DDR4-reuse Structera X 3406 only samples in Q1 2027 (HPCwire 2026-10-12, via snippet). This follows the C-76/C-50 precedent, where a different packaging of the same opportunity is a duplicate. C-49 should take the assessment and managed-tuning subscription as its T0 entry path and recurring line.)

*Sub-branch:* Services -> SaaS · *Materials sense:* c-capital

**What it is:** A services firm that assesses, deploys and tunes CXL Type-3 memory expansion and tiering on Granite Rapids/Turin servers. Hardware: Micron CZ-series, Samsung CMM-D or SK hynix CMM expanders, and Marvell Structera- or Astera Leo-based cards. Software: Linux weighted-interleave and DAMON tiering, SK hynix HMSDK. Clients are HPC centers, in-memory database hosts and EDA shops, and engagements convert into a managed tuning and monitoring subscription.

**Why it could work:** 1 TB of new DDR5 RDIMM costs ~$20.8k per node at 4Q26 prices (e_estimates §12). CXL lets buyers add cheaper or reused capacity, including DDR4 behind Structera-class controllers, without buying top-bin DIMMs. Mainline Linux still has CXL gaps (Dynamic Capacity, multi-host sharing), so integration know-how is scarce. Practice revenue: ~$83k/yr part-time, ~$248k full-time at $225/h.

**Evidence:** TRL 7 · Rule 1: SUPPORTED
  - [Linux CXL maturity map](https://github.com/torvalds/linux/blob/master/Documentation/driver-api/cxl/maturity-map.rst) — industry, 2026-10-31. Mainline Linux still lacks Dynamic Capacity Device support and multi-host sharing: CXL integration is real but early [cross-reference: URL from a sibling agent's log; not opened by E]
  - [SK hynix Heterogeneous Memory SDK (HMSDK) v4.0](https://github.com/skhynix/hmsdk) — industry, 2025-11-03. Free vendor CXL tiering SDK; weighted interleave upstream in Linux 6.9: tooling is free, value is in integration [cross-reference: URL from a sibling agent's log; not opened by E]
  - [Memory prices surging by 90% from 4Q25 (Counterpoint)](https://www.eetasia.com/memory-prices-surging-by-90-from-4q-2025/) — news, 2026-01. 64GB RDIMM contract $450 (4Q25) to >$900 (1Q26) [cross-reference: URL from a sibling agent's log; not opened by E]
  - [Marvell unveils 2nd-gen Structera X with six-channel CXL 3.2 memory expanders for AI inference (HPCwire)](https://hpcwire.com/off-the-wire/marvell-unveils-2nd-gen-structera-x-with-six-channel-cxl-3-2-memory-expanders-for-ai-inference) — news, 2026-10-12. Structera X 3406 (DDR4, 18 RDIMMs/9 TB) and 3506 (DDR5, 6 TB) sample in Q1 2027 (via search snippet).
  - [Marvell Scales AI Memory to 48TB Behind a Single CXL Switch at FMS 2026 (Futurum)](https://futurumgroup.com/insights/marvell-scales-ai-memory-to-48tb-behind-a-single-cxl-switch-at-fms-2026/) — market-research, 2026-08. Structera X 2404 pitched for reusing existing DDR4 at a fraction of new DDR5 cost. Architecture figures, not deployments (via search snippet).
  - [Micron CMM CZ122 256GB E3.S CXL2.0 Memory Expander (Red Hat certified hardware catalog)](https://catalog.redhat.com/hardware/components/detail/259267) — other, 2026. CXL Type-3 expander certified for RHEL. Enterprise-available hardware (via search snippet).
  - [Memory vendors outsource/scale back CXL controller development (XenoSpectrum)](https://xenospectrum.com/en/cxl-controller-outsourcing-memory-vendors/) — news, 2026-07. Samsung, SK hynix and Micron reportedly scaled back in-house CXL expander controller work; not officially announced (via search snippet).

**Capital tier:** T0 | **Time to first revenue:** 6-12 months: first paid assessment at an HPC or database shop | **Gross margin estimate:** 50-70% (services)

**US manufacturability:** Services; hardware from Micron/Samsung/SK hynix/Astera/Marvell; no fab dependency.

**Who is already doing this:** Penguin Solutions (CXL memory-expansion servers, SMART CXL AICs; per batch_07); Supermicro, Dell, HPE and Lenovo professional services; Marvell, Astera, Samsung, Micron and SK hynix field engineers (free, to sell silicon); Red Hat certified CXL hardware (CZ122); Colfax, Silicon Mechanics; MemVerge [UNVERIFIED-T for the rest]

**Wins on which axis, for which buyer:** Capacity and bandwidth per node above the native DIMM-slot ceiling, plus reuse of already-owned DDR4 once Structera-class cards reach non-hyperscaler buyers (3406 samples Q1 2027). Not $/GB for new CXL DRAM, which costs the same DRAM plus a controller. — for university and DOE HPC centers, SAP HANA/in-memory database hosts, EDA and genomics shops

**Survives a 2029 glut?:** partially — The DRAM-saving pitch shrinks when DDR5 falls 60% (1 TB = $8.3k), but capacity and bandwidth expansion for >2 TB nodes remains.

**Fatal-flaw candidate:** It duplicates C-49, and demand is thin. Memory makers reportedly scaled back CXL controller development (Jul-2026). The DDR4-reuse controller for mid-market buyers only samples in Q1 2027. Vendors give integration away to sell hardware. Every billable hour is kernel or platform work the founder cannot do.

*Possible?* yes - CXL 2.0 expanders and Linux tiering ship today · *Profitable?* marginal - services margins, small and lumpy demand · *Doable by this founder?* no as a solo founder; marginal only with a kernel/CXL cofounder who delivers all billable work

*Business-model lenses:* services -> SaaS; module/appliance (VAR)

### C-98 — Memory patent expiry and litigation radar — ☠ KILLED (R4-NO-WINNING-AXIS: The card's only axis is cheaper FTO and litigation monitoring, and free tools already win it. Unified Patents' Portal offers free PTAB and district-court search plus free daily litigation alerts, and its data has been in Google Patents since 2019 (via search snippet). Google Patents and USPTO Patent Center also show status, maintenance fees and anticipated expiry free [UNVERIFIED-training]. Precision for counsel sits with Docket Navigator, Lex Machina and RPX. What the named buyers actually need, a reliable FTO opinion, must come from an attorney ($10-30k), and a dashboard cannot give legal reliance. The card's own evidence (ITC 337-TA-1487; Everspin's $6.0M litigation quarter) shows demand for counsel, not for a $4.8k/yr memory dashboard. The card calls itself 'likely a feature ... or an internal tool', consistent with the C-14 kill of a curated public-data subscription.)

*Sub-branch:* IP intelligence data product · *Materials sense:* none

**What it is:** A subscription web app that tracks memory-relevant U.S. patents (DRAM module/PMIC, MRAM, ReRAM, FeRAM, IGZO, 3D DRAM). It computes expiry dates (term adjustments, terminal disclaimers, maintenance-fee lapses), follows assignment changes and PTAB/ITC/district-court dockets (e.g., ITC 337-TA-1487 Avalanche v. Everspin; the Netlist RDIMM/PMIC cases), and provides FTO checklists per product type. It is built from free USPTO bulk data plus PACER/ITC EDIS.

**Why it could work:** Every hardware concept in this study has an FTO gate: Netlist PMIC for DDR5 modules, SEL for IGZO, the ITC case for Everspin STT. One FTO opinion costs $10-30k and NPE defense $0.6-4M (p1-ip). Everspin spent $6.0M on litigation in one quarter. Small module makers, recert firms and memory startups need cheap monitoring. 25 subscribers x $4.8k = $120k ARR at ~85% GM.

**Evidence:** TRL 9 · Rule 1: SUPPORTED
  - [USITC institutes 337-TA-1487 (Avalanche v. Everspin, MRAM)](https://www.usitc.gov/press_room/news_release/2026/er0227_68226.htm) — government, 2026-02-27. Active memory patent fight: an exclusion order is sought against imported Everspin STT-MRAM [cross-reference: URL from a sibling agent's log; not opened by E]
  - [Everspin Q3 2026 results (8-K Ex 99.1)](https://www.sec.gov/Archives/edgar/data/0001438423/000162828026067890/mram-20260930xexx991.htm) — company, 2026-10-28. $6.0M litigation cost inside $18.5M of quarterly opex at a $20.6M-revenue memory company; licensing/services only $3.7M [cross-reference: URL from a sibling agent's log; not opened by E]
  - [Free patent litigation alerts now available via Unified's Portal (Unified Patents support)](https://support.unifiedpatents.com/hc/en-us/articles/360019405153-Free-patent-litigation-alerts-now-available-via-Unified-s-Portal) — other, 2019-03. Free daily alerts on every new PTAB and district-court case (via search snippet).
  - [Google Patents now includes Unified PTAB and District Court litigation data (Unified Patents)](https://www.unifiedpatents.com/news/2019/3/7/google-patents-integrates-unifieds-ptab-and-district-court-litigation-data) — other, 2019-03-07. Litigation and PTAB data shown free on Google Patents patent pages (via search snippet).

**Capital tier:** T0 | **Time to first revenue:** 6-12 months: first subscriptions from module makers / IP counsel | **Gross margin estimate:** 80-90%

**US manufacturability:** Software.

**Who is already doing this:** Unified Patents Portal (free PTAB and district-court search plus free daily litigation alerts; data integrated into Google Patents since 2019, via search snippet); Google Patents and USPTO Patent Center (free status, maintenance-fee and expiry data [UNVERIFIED-training]); Docket Navigator, Lex Machina, RPX, PatSnap, LexisNexis PatentSight (paid) [UNVERIFIED-training]

**Wins on which axis, for which buyer:** risk reduction (lower FTO and litigation-monitoring cost) — for small U.S. module makers, recert/ITAD firms, CXL and memory startups, IP counsel, memory investors

**Survives a 2029 glut?:** partially — Litigation and FTO needs do not depend on the cycle, but the buyer set (small memory firms) shrinks in a glut.

**Fatal-flaw candidate:** No winning axis. Litigation and PTAB monitoring is free (Unified Portal, Google Patents), expiry and maintenance status is free (USPTO, Google Patents), and the deliverable with real value, a relied-upon FTO opinion, must come from counsel. The memory-only niche (~25 subscribers x $4.8k = $120k ARR, with no demand evidence) cannot outspend free tools or entrenched paid platforms.

*Possible?* yes · *Profitable?* no - free tools cover monitoring, and counsel captures the FTO spend · *Doable by this founder?* yes - T0, but at most an internal FTO-gate tool for this study's hardware concepts, not a business

*Business-model lenses:* data product; SaaS; IP licensing (intelligence)
