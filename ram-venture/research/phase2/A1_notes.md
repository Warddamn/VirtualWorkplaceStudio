# A1 research notes: oxide-semiconductor DRAM, ferroelectric memory, 3D DRAM

Agent A1 · Phase 2 divergent ideation · 2026-11-01
Outputs: `phase2/A1.json` (15 cards), `phase2/A1_device_params.json` (15 device rows incl. a DDR5 reference and one sensitivity row), `sources/A1.jsonl` (102 sources), `assumptions/A1.md`.

## 0. Method and limits (read first)

- **Searches:** I ran about 37 WebSearch queries covering imec, Kioxia, SEL, Samsung, SK hynix, NEO, FMC, Micron NVDRAM, SunRise, Infineon/Cypress/Ramtron, TI, RAMXEED, GF FeFET, SkyWater Fab 25, NY CREATES, Sandia, Penn/AFRL AlScN, Purdue In2O3, Georgia Tech IWO, DARPA/AF SBIR topics, Optane, wafer and DRAM cost, display capacity and Foxconn.
- **Blocked:** WebFetch failed with ENOTFOUND on every host I tried (blocksandfiles, kioxia, imec, eenewseurope, heise), so the domains are not allowed in this session. I stopped trying more hosts, as the tool instructs. The shared per-turn WebSearch budget (200 across all agents) then ran out, so I could not finish 4-5 planned checks:
  - Kepler Computing status
  - Penn AlScN licensing status
  - NEO's licensing terms
  - imec 2025 3D IGZO density roadmap
  - Stanford ITO 2T0C
- **Consequence:** every fact below comes from search-result summaries, logged "(via search snippet)". Treat it as **[REPORTED]** even when the underlying source is primary (an IEDM paper or a company release). Nothing is tagged [VERIFIED].
- **Numbers:** $/GB figures come from a scratch script over `A1_device_params.json`, using the same inputs the downstream `models/device_cost_compare.py` will use. Every wafer cost is an **[ESTIMATE]**, because no public primary wafer-cost figure turned up (Yole/TechInsights are paywalled).

## 1. Scratch $/GB comparison [ESTIMATE: computed from A1_device_params.json]

Price anchors:
- DDR5 today: ~$27/GB (DRAMeXchange 2026-08-31, DDR5 16Gb avg $53.92, from the p1-market log).
- DDR5 in the glut: ~$10.8/GB (A-05).
- DDR5 estimated manufacturing cost: ~$2.7/GB. This is the floor incumbents can price toward in a real glut.

| id | device | GB/wafer | $/GB incl. test/pkg | × DDR5 price now | × glut price |
|---|---|---:|---:|---:|---:|
| REF | DDR5 1b (0.436 Gb/mm², $5.5K wafer) | 2,930 | **2.7** | 0.10 | 0.25 |
| A1-01 | IGZO 2T0C eDRAM macro @130nm (embedded; $/GB is only a yardstick) | 3.0 | 506 | 19 | 47 |
| A1-02 | Standalone 4-tier 2T0C @200mm/130nm | 7.6 | **336** | 12.5 | 31 |
| A1-02s | Same on hypothetical 300mm/28nm BEOL | 410 | 11.8 | 0.44 | 1.09 |
| A1-03 | 2T0C on Gen-8.5 glass (per sheet) | 2.3 | 266 | 9.9 | 25 |
| A1-04 | OCTRAM 4F² at demo pitch (DRAM fab) | 733 | 8.4 | 0.31 | 0.78 |
| A1-05 | NEO 3D X-DRAM *if* 10× density claim holds | 16,800 | 1.2 | 0.05 | 0.11 |
| A1-06 | HZO FeRAM @200mm/130nm (Mb parts) | 2.3 | 769 | 29 | 71 |
| A1-08 | NVDRAM-class (DRAM fab) | 2,062 | 4.2 | 0.15 | 0.39 |
| A1-09 | FMC DRAM+ first Gb part (est.) | 382 | 14.6 | 0.54 | 1.35 |
| A1-10 | FeFET eNVM @22FDX | 110 | 36 | 1.3 | 3.4 |
| A1-12 | Off-the-shelf 16Mb F-RAM | 4.6 | 693 | 26 | 64 |
| A1-15 | Samsung 4F² VCT IGZO-channel DRAM | 3,315 | 2.9 | 0.11 | 0.27 |

What the table says:
1. **Every route that is cheaper than DDR5 runs in a DRAM or 3D-NAND fab** (A1-04, -05, -08, -15). Only Samsung, SK hynix, Micron, Kioxia/Nanya and CXMT can play there (rule 3).
2. **Every route a small team could reach is 10-70× DDR5's price on $/GB** (A1-01, -02, -03, -06, -12). They can only win on a non-$/GB axis: standby power, non-volatility, temperature, radiation, or supply security.
3. The A1-02 sensitivity row shows that **the line, not the material, sets the economics**. The same 4-tier IGZO 2T0C on a 300mm ~28nm BEOL lands near the glut price (~$12/GB), but that is still ~4× DRAM cost, and no U.S. foundry offers the module.

## 2. Key verified-by-snippet facts (dated)

### Oxide-semiconductor DRAM

**imec IGZO 2T0C:**
- IEDM 2020: retention >400 s, extracted Ioff 3×10⁻¹⁹ A/µm, Lg 45nm, 300mm wafers ([eeNews Europe, 2020-12](https://www.eenewseurope.com/news/imec-shows-capacitor-free-dram)).
- IEDM 2021: fully 300mm BEOL-compatible cell with >10³ s retention and >10¹¹ cycles. Lg scaled to 14nm with >100 s retention. PBTI lifetime improved from ~20 days to ~1 year against a 5-year target ([TechXplore, 2021-12](https://techxplore.com/news/2021-12-capacitor-less-igzo-based-dram-cell-excellent.html)).
- A section on imec 2T0C reportedly ran at IEDM 2025 (LinkedIn mention only; not used).

**SEL DOSRAM (CAAC-IGZO):**
- Leakage ≤200 zA, seven orders below Si; 1.8 V operation ([ECI ULSIC-TFT 7, 2019](https://dc.engconfintl.org/ulsic_tft_vii/34)).
- SEL patent text reportedly claims 10⁵ s retention and ~50% refresh-power saving. The specific patent was not confirmed ([Justia 11404107](https://patents.justia.com/patent/11404107)).
- SEL is the dominant oxide-semiconductor IP holder and licenses CAAC-IGZO to display makers (JDI co-development, LG Display renewal) ([Display Daily](https://displaydaily.com/jdi-enters-agreement-with-sel/)).
- **Any U.S. oxide-memory venture needs SEL freedom-to-operate work.**

**Kioxia + Nanya OCTRAM:**
- IEDM 2024: 4F² cell with a vertical InGaZnO transistor on top of a high-aspect-ratio capacitor (capacitor-first). Ion >15 µA/cell, Ioff <1 aA/cell ([BusinessWire, 2024-12-09](https://www.businesswire.com/news/home/20241209099702/en/Kioxia-Develops-OCTRAM-Oxide-Semiconductor-Channel-Transistor-DRAM-Technology)).
- 275 Mbit array at WL 54nm / BL 63nm pitch ([Blocks & Files, 2024-10](https://blocksandfiles.com/2024/10/22/kioxia-developing-new-dram-scm-and-nand-tech/)).
- IEDM 2025: 8-layer horizontally stacked IGZO transistors (SiN replaced by IGZO), Ion >30 µA, Ioff <1 aA ([Kioxia, 2025-12-12](https://www.kioxia.com/en-jp/about/news/2025/20251212-1.html)).
- No production date announced.

**Samsung:**
- 10a DRAM working die in Mar 2026 with 4F² VCT. The channel reportedly moved to IGZO. Development completes 2026, qualification 2027, mass-production transfer 2028 ([TrendForce, 2026-04-24](https://www.trendforce.com/news/2026/04/24/news-samsung-reportedly-produces-sub-10nm-10a-dram-working-die-using-4f-square-and-vct-targets-2028-production/)).
- 16-tier vertically stacked DRAM with GAA cells at VLSI 2026 ([VLSI tipsheet, 2026-04](https://www.vlsisymposium.org/wp-content/uploads/2026/04/2026-VLSI-Technical-Tipsheet-REVISED-FINAL-NO-IMAGES-4.24.26.docx)).

**SK hynix:**
- 5-layer 3D DRAM at 56.1% yield (VLSI 2024). Products need 32-192 layers ([TrendForce, 2024-06](https://trendforce.com/news/?p=10820)).
- 4F² vertical-gate DRAM, VLSI 2026 paper T8.5.

**IMECAS (VLSI 2026):** 4-layer 3D 2T0C, 400 s retention, 3 bits/cell ([IT Home, 2026-06](https://www.ithome.com/0/966/543.htm)).

**U.S. academic oxide work (licensable IP pool):**
- Purdue (Ye, Li): three monolithic layers of ALD In₂O₃ transistors, including ferroelectric FETs, on a **200mm** wafer; >100,000 devices on 52 dies ([Purdue, 2026-09-16](https://engineering.purdue.edu/ECE/News/2026/purdue-researchers-build-3d-chip-platform-for-faster-more-efficient-ai-computing); [arXiv 2608.09508](https://arxiv.org/pdf/2608.09508)).
- Georgia Tech (Shimeng Yu): 3T IWO BEOL eDRAM ([GT, 2024](https://hg.gatech.edu/node/675050)).
- IWO 2T gain cell: 1 s at 25 °C, 0.3 s at 85 °C ([2020](https://investigadores.uandes.cl/en/publications/double-gate-w-doped-amorphous-indium-oxide-transistors-for-monoli/)).
- Limitation: IGZO-2T is slow because of low mobility ([DATE 2026](https://past.date-conference.com/proceedings-archive/2026/DATA/154.pdf)).

**U.S. TFT/display capacity: effectively none.**
- Foxconn's Wisconsin Gen 10.5 (later Gen 6) LCD fab was never built. The 2020 state report found no LCD manufacturing ([Sixteen:Nine](https://www.sixteen-nine.net/?p=20827); [UpNorthNews, 2020-10](https://upnorthnewswi.com/2020/10/22/state-report-foxconns-project-cant-possibly-be-a-factory)).
- Oxide-TFT capacity is in Asia and running underutilized ([Omdia via TelecomLead, 2025](https://telecomlead.com/electronics/display-panel-industry-faces-utilization-decline-amid-tariff-uncertainty-120613)).
- Pragmatic's IGZO FlexIC 300mm fab is in Durham, UK ([Semiconductor Today, 2024-03](https://www.semiconductor-today.com/news_items/2024/mar/pragmatic-280324.shtml)).

**U.S. 200mm silicon that could host IGZO BEOL:**
- SkyWater bought Infineon's Austin Fab 25 (200mm, 130-65nm, ~400k wafer starts/yr). It closed 2025-06-30 for ~$73M plus ~$20M working capital, with an Infineon long-term supply agreement and conversion to a foundry ([BusinessWire, 2025-02-26](https://www.businesswire.com/news/home/20250226773415/en/SkyWater-to-Acquire-Infineons-Austin-Fab-and-Establish-Strategic-Partnership-to-Expand-U.S.-Foundry-Capacity-for-Foundational-Chips); [LaPedus](https://marklapedus.substack.com/p/skywater-acquires-infineons-200mm)).
- No SkyWater oxide or ferroelectric module was found. Its known embedded NVM is Weebit ReRAM on S130.
- Purdue proves oxide BEOL works on 200mm. NY CREATES Albany (300mm) has a HfO₂ ferroelectric memory JDA with Fraunhofer IPMS ([idw, 2025-05-16](https://nachrichten.idw-online.de/2025/05/16/ny-creates-and-fraunhofer-ipms-announce-joint-development-agreement-to-advance-memory-devices-at-300mm-wafer-scale)).

### Ferroelectric

**Micron NVDRAM:**
- 32Gb dual-layer stacked ferroelectric 1T1C with a 5.7nm FE capacitor, IEDM 2023 paper 15.7 ([eeNews Europe, 2023-11](https://www.eenewseurope.com/en/iedm-micron-to-present-dram-like-non-volatile-memory-for-ai/)).
- Never productized: "might never become a product" ([Blocks & Files, 2024-01-09](https://blocksandfiles.com/2024/01/09/micron-nvdram-might-never-become-a-product/)), and still no commitment in 2025 ([Design & Reuse, 2025-01](https://www.design-reuse.com/news/202501939-ferroelectric-ram-looking-rusty-and-stuck-/)).
- No cancellation notice found either. The status is "shelved in practice".

**FMC (Dresden):**
- Founded 2016. $20M Series B in 2020 (M Ventures, imec.xpand, SK hynix, Bosch, TEL).
- €100M in Nov 2025: €77M equity plus €23M public money including the EIC, for DRAM+ and 3D CACHE+ ([HPCwire, 2025-11-13](https://www.hpcwire.com/off-the-wire/fmc-raises-e100m-to-set-new-standards-for-memory-chips/); [BeBeez](https://bebeez.eu/2025/11/14/fmc-raises-e100m-for-its-hafnium-oxide-based-memory-chips/)).
- Works with "two major DRAM manufacturers and an advanced logic foundry in Asia".
- **No FMC memory chips on the market as of 2026** ([heise](https://heise.de/-11151026)). It is pursuing a fab at Sülzetal near Magdeburg (the former Intel site), with a reported €1.3B funding ask ([CIO.de, 2025-07](https://www.cio.de/article/4026335/kommt-die-erste-chip-fabrik-von-fmc-nach-magdeburg.html)).
- DRAM+ test partner is Neumonda ([TrendForce, 2025-04](https://www.trendforce.com/news/?p=37749)).
- **No U.S. presence found.**

**HZO 1T1C arrays:**
- Sony/Fraunhofer, IEDM 2023: 1 Mb, 1.8 V, 10¹¹ cycles, **1-month retention at 85 °C** ([TU Dresden](https://fis.tu-dresden.de/portal/en/publications/a-highly-reliable-18-v-1-mb-hf05zr05o2based-1t1c-feram-array-with-3d-capacitors%28e6411421-d8d0-4f39-97d3-03a6d18e3513%29.html)).
- 64 kbit array at VLSI 2020.
- Intel holds patents on FE capacitors over BEOL transistors ([US11751402](https://patents.google.com/patent/US11751402)). No Intel IEDM FeRAM paper surfaced in my searches.

**Sandia (2026-05-13):** HfO₂/HZO rad-hard FeRAM integrated into the trusted MESA rad-hard fab, at 200mm scale, plus binary and 32-state FTJs. Follow-on work targets the circuitry ([Sandia](https://www.sandia.gov/research/news/evolving-semiconductor-technology-for-national-security-applications/)). **This is a U.S. lab IP and partnership path (CRADA or license).**

**Incumbent PZT F-RAM:**
- Infineon EXCELON 1-16 Mb, QSPI 108 MHz, 10¹⁴ cycles, AEC-Q100 ([Infineon](https://infineon.com/cms/en/product/memories/f-ram-ferroelectric-ram/excelon-f-ram)).
- Rad-hard 2Mb QML-V: >150 krad, 10¹³ cycles, >100 years at 85 °C ([Infineon](https://infineon.com/cms/en/product/memories/radiation-hardened-high-reliability-memories/space-memories/5962r1821601vxc)).
- Manufacturing history: Ramtron used TI Dallas and IBM Burlington lines, then Cypress bought it (2012), then Infineon (2020).
- 130nm F-RAM was transferred to a TI Dallas 300mm line, and Cypress qualified **Fab 25 Austin** as an alternate fab for 4/16/64 Kb F-RAM ([Cypress PCN](https://community.infineon.com/gfawx74859/attachments/gfawx74859/NonVolatileRAM/1143/1/002-18474_00_V.pdf); [EE Times Japan, 2018](https://eetimes.itmedia.co.jp/ee/spv/1811/15/news033.html)).
- **So incumbent F-RAM is already partly U.S.-fabbed, and "Made in USA" is not a moat against Infineon.**
- TI embedded FRAM: 130nm plus 2 masks, cell 0.54-0.71 µm², in-house ([New Electronics](https://newelectronics.co.uk/content/features/fram-set-to-save-energy-in-write-intensive-mcu-applications)).
- RAMXEED is the ex-Fujitsu FeRAM/ReRAM company, renamed 2025-01-01 ([eeNews Europe](https://www.eenewseurope.com/en/fujitsu-memory-spin-off-renames-as-ramxeed/)).

**GF FeFET:**
- FMC FeFET integrated on GF 28nm HKMG (around 2016) ([eeNews Europe](https://www.eenewseurope.com/en/ferroelectric-memory-startup-aims-at-glofos-22fdx/)).
- 22FDX FE memory still "upcoming" in 2026 ([Fraunhofer IPMS FAMES](https://www.ipms.fraunhofer.de/en/press-media/press/2026/FAMES-wafer-exchange.html)).

**AlScN (Penn + AFRL):**
- Ni/Al₀.₆₈Sc₀.₃₂N(45nm)/Pt ferro-diodes on 4-inch Si switch at 600 °C for >60 h at <15 V (Nature Electronics, 2024-04-29) ([Physics Today](https://physicstoday.aip.org/news/new-memory-circuit-can-handle-the-heat)).
- Scaled devices reach >100 Mbit/mm² ([arXiv 2504.13283](https://arxiv.org/pdf/2504.13283)).

**DoD demand signals:**
- DARPA DPA26BZ04-DV017, -269 to +600 °C NVM, Direct-to-Phase II, ~$1.2M, closed 2026-08-19 ([DARPA](https://www.darpa.mil/research/programs/non-volatile-memory-extreme-environments)).
- AF254-D0806, 500 °C kB-scale NVM manufacturing scale-up, closed ([SBIR.gov](https://www.sbir.gov/topics/12036)).

**SunRise Memory (3D NOR):** founded 2016, San Jose. Still patenting in 2024-26. No 2025-26 product or funding news found ([CB Insights](https://www.cbinsights.com/company/sunrise-memory); [US12052867](https://patents.google.com/patent/US12052867)).

### 3D DRAM

**NEO Semiconductor 3D X-DRAM:**
- May 2025: 1T1C and 3T0C IGZO variants announced, with TCAD-simulated 10 ns and >450 s retention ([eeNews Europe](https://www.eenewseurope.com/en/neo-semiconductor-adds-igzo-to-3d-dram-designs/)).
- 2026-04-23 PoC (company-reported): >1 s at 85 °C, >10¹⁴ cycles, <10 ns. Test chips were built with NYCU and fabbed at TSRI Taiwan. The next steps are array-level and multi-layer chips plus talks with memory companies. A strategic investment was led by Stan Shih ([StorageNewsletter](https://www.storagenewsletter.com/2026/05/13/neo-semiconductor-demonstrates-3d-x-dram-proof-of-concept-secures-strategic-investment-to-advance-ai-memory/)).
- **Measured retention (>1 s) is 450× below the earlier simulation (>450 s).** That gap is a useful calibration for company claims.
- NEO's model is licensing to memory companies.

## 3. Post-mortems used

- **Intel Optane (3D XPoint, PCM):** lost $576M in 2020 alone, then took a $559M impairment when Intel wound it down in Q2 2022 ([TechTarget](https://www.techtarget.com/it-infrastructure/news/252523339/Intel-pulls-the-plug-on-Optane); [AnandTech](https://www.anandtech.com/show/17515)). It was slower than DRAM, costlier than NAND, and never reached the volume needed to cut cost; the IM Flash fab was sold. **Lesson for A1-08:** a persistent tier must be cheaper per GB than DRAM *and* have a CPU/OS ecosystem. The 2026 price spike does not change this, because the glut returns DRAM below any startup's persistent-tier cost.
- **Micron NVDRAM:** technically done (32Gb), commercially shelved. If the only U.S. DRAM maker, which owns the IP and the fab, won't ship ferroelectric DRAM in a shortage, a startup can't.
- **FMC:** about 9 years and €120M+ raised with no product shipped yet, now asking for a €1.3B fab. **Lesson:** even a well-funded HfO₂ memory company ends up needing a fab or a DRAM partner. A licensing model alone has not reached product in 9 years.
- **SunRise Memory:** about $75M+ (Series C 2019 per Pitchbook, via snippet; conflicting profile data) and roughly 8 years with no public silicon.
- **Foxconn Wisconsin:** a promised U.S. LCD fab that became storage. **Lesson for A1-03:** U.S. display-fab capacity for IGZO does not exist and won't appear for memory.
- **Ramtron to Cypress to Infineon:** F-RAM has been a niche of hundreds of $M per year [ESTIMATE] for about 30 years. Its density never scaled past ~16 Mb standalone because PZT doesn't scale. HZO fixes scaling but not (yet) endurance and retention.

## 4. Evidence and reasoning per card

- **A1-01 OS-eDRAM IP (T2, TRL 4).**
  - Evidence: imec 2020/21 cells; IWO 2T and Georgia Tech 3T eDRAM; DATE 2026 speed caveat; granted 2T IGZO patent US12191135 (FTO risk); SkyWater Fab 25 as a hungry U.S. 200mm foundry; Purdue 200mm oxide BEOL.
  - Upside: always-on edge AI is SRAM-limited, and a ~4-5× denser, near-zero-leakage BEOL memory is a real axis.
  - Kill risks: SkyWater has no oxide module; PBTI lifetime; SEL patents; ReRAM and MRAM already qualified at U.S. foundries.
  - Ranked **#3 most promising** for its venture ceiling, but not founder-doable.
- **A1-02 standalone 2T0C (dead).** Scratch model gives $336/GB, which is 12× DDR5's price and about 125× its cost. The sensitivity row shows a 300mm 28nm BEOL would be needed.
- **A1-03 display-fab glass (dead).** There is no U.S. TFT fab, and the ~2 µm design rule makes it about 100,000× less dense than DRAM.
- **A1-04 OCTRAM (dead for us).** Kioxia/Nanya IP plus a required DRAM capacitor fab means rule 3.
- **A1-05 NEO 3D X-DRAM (dead for us).** Only a single-cell PoC exists, it needs a 3D-NAND-class fab, and NEO licenses to IDMs.
- **A1-06 U.S. HZO FeRAM (T2, TRL 5).**
  - Evidence: 1Mb HZO arrays; Sandia 200mm HZO FeRAM in a trusted fab; hafnia radiation hardness; Infineon's near-sole-source rad-hard F-RAM.
  - Kill risks: HZO's endurance and retention gap versus PZT, and Infineon already has some U.S. fab content.
  - Ranked **#2 most promising**: the supply-security and rad-hard axis is real, it is glut-proof, and a Sandia/SkyWater path exists.
- **A1-07 AlScN 600 °C NVM (T1, TRL 4).**
  - Evidence: Nature Electronics 2024 via Physics Today and Penn; arXiv scaling to >100 Mb/mm²; two DoD topics (AF254-D0806, DARPA DPA26BZ04-DV017).
  - Ranked **#1 most promising** for this founder among device cards. It is the only device path with a credible <$50k entry (STTR plus a university license option), a U.S.-made moat, and zero DRAM-cycle exposure.
  - Still carries a high risk of becoming grant-dependent, with revenue at roughly 36 months.
- **A1-08 Optane-slot FE persistent memory (tempting, dead).** See post-mortems.
- **A1-09 FMC DRAM+ U.S. channel (marginal).** Entirely gated by FMC shipping a chip, and there is no moat.
- **A1-10 FeFET in GF 22FDX (dead for us).** It is FMC/GF's IP and line, it is NVM rather than RAM, and it is not qualified.
- **A1-11 SunRise 3D NOR (UNSUPPORTED).** No public silicon or peer-reviewed array data was found.
- **A1-12 F-RAM NV-cache modules (T0, founder-doable, small).** This card also records the key negative finding: at ~$8-30K/GB [ESTIMATE], F-RAM is 300-1,000× DDR5, so ferroelectric parts cannot take DRAM sockets in the shortage.
- **A1-13 test and qualification lab (T1, marginal).** Reliability is every A1 device's bottleneck, and FMC and Neumonda show the service model works. Demand is small and lumpy.
- **A1-14 MemTech Atlas data product (T0, founder yes, small).** It reuses this engagement's device_params and cost model, and the "claims vs silicon" tracker is a distinctive feature (NEO's 450 s simulated vs 1 s measured).
- **A1-15 oxide-channel materials supply (T2).** Samsung's reported IGZO channel and Kioxia's OCTRAM create demand. Qualification cycles favor incumbents.

## 5. Who holds IP and whether a small team can license it

| Technology | IP holders (from evidence) | Licensable by a small U.S. team? |
|---|---|---|
| IGZO/oxide memory | SEL (dominant estate; licenses to display makers), Kioxia/Nanya (OCTRAM), Samsung/SK hynix/Micron (4F² VCT, e.g. [US11653487](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11653487), assignee not verified), imec (partner program) | Corporate IP: **no**. University IP: **plausible** (Purdue In₂O₃ 200mm M3D, Georgia Tech/Notre Dame IWO). Status of each university's licensing is unverified. |
| HZO FeRAM/FeFET | FMC (FeFET/FeCAP, Germany), Micron (NVDRAM), Intel (BEOL FeCAP patents), Sony/Fraunhofer/NaMLab, Sandia (rad-hard HZO, FTJ) | **Sandia via CRADA or license: plausible** (DOE tech-transfer path). FMC: licenses to foundries and IDMs, not startups. |
| AlScN ferro-diode | Penn (Jariwala, Olsson) + AFRL | **Plausible** via Penn tech transfer plus an STTR. Whether it is already licensed is unverified. |
| PZT F-RAM | Infineon (Ramtron/Cypress estate), RAMXEED, TI (licensed) | Mature, so no license is needed to *use* parts; making PZT parts is not attractive. |
| 3D DRAM | NEO (licensing to memory makers), Samsung, SK hynix, Micron, Kioxia | **No** (needs a fab-owning licensee). |

## 6. Ideas considered but NOT carded (one-line reasons)

- **IGZO 2T1C/2T0C analog compute-in-memory accelerator chiplet (imec AIMC):** this is processing-in-memory, which belongs to branch B; the device evidence sits in A1-01.
- **Licensing SEL DOSRAM to U.S. MCU makers as SEL's agent:** SEL licenses directly to large firms. The FTO issue is folded into A1-01's fatal flaw.
- **3D IGZO DRAM for AI KV-cache built by a startup:** the same T4 fab problem as A1-04/A1-05, so it would duplicate them.
- **Cryogenic IGZO/HZO memory for quantum control:** no evidence was found this session, so it would be UNSUPPORTED. Not worth a card without a source.
- **Kepler Computing (U.S. ferroelectric, Intel-linked) partnership:** I could not verify its 2025-26 status before the search budget ran out. Flagged as an open question.
- **Reviving PZT F-RAM production at SkyWater Fab 25:** the line has F-RAM history, but PZT doesn't scale, Infineon already holds the supply agreement, and HZO (A1-06) is the better material bet.
- **HZO FeRAM as a DRAM substitute at 200mm:** this is A1-06's device used for a DRAM job, which fails at ~$770/GB (folded into A1-06 and A1-12).
- **FTJ multi-level (32-state, Sandia) analog memory product:** TRL 3 and lab-only; noted inside A1-06 as a Sandia capability.
- **Display-fab IGZO as a bring-up foundry via Pragmatic's "Fab-in-a-Box":** it is UK-based, targets RFID-class logic rather than memory, and has no U.S. footprint.
- **Using the idle Foxconn Wisconsin building:** it was never tooled for TFT and is now storage.

## 7. Open questions for later phases

1. Does SkyWater (Bloomington or Fab 25) have, or would it build, an oxide-semiconductor or HZO module? A direct inquiry costs nothing.
2. Has Penn licensed the AlScN ferro-diode IP or spun it out? Purdue's In₂O₃ M3D IP? Georgia Tech's IWO eDRAM IP? These need tech-transfer portal checks, which were blocked this session.
3. What are Sandia's CRADA and licensing terms for MESA HZO FeRAM, and is there a follow-on program a small company could join?
4. What is Kepler Computing's 2026 status (U.S. ferroelectric memory/logic)? Not checked.
5. What are real 200mm 130nm processed wafer prices at SkyWater? Every A1 $/GB row is sensitive to this ±50%.
6. Were DPA26BZ04-DV017 or AF254-D0806 awarded, and to whom? That shows who the competitors are for A1-07.
