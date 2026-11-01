# A2 research notes: MRAM, ReRAM/memristor/CBRAM, PCM

Agent A2 · Phase 2 divergent ideation · 2026-11-01
Outputs: `phase2/A2.json` (15 cards), `phase2/A2_device_params.json` (16 rows: 14 card devices + 2 DRAM references). Sources are in `sources/A2.jsonl` (101 entries) and assumptions in `assumptions/A2.md`.

## 0. Method and constraints (read first)

- I ran about 50 web searches covering Everspin, Avalanche, Weebit, TSMC/GF/Samsung eNVM, TetraMem, 4DS, Crossbar, NVE, Netsol, Numem, Antaios, CBRAM, Optane/XPoint, SanDisk, DRAM prices, IBM FlashCore and cell-size teardowns.
- **WebFetch was blocked by session network policy.** It failed for sec.gov, everspin.com, weebit-nano.com, mram-info.com and storagenewsletter.com. Every fact below therefore comes from search-result summaries and is tagged "(via search snippet)" in the source log.
- **The shared web-search budget ran out** (200 calls per turn across all agents) before I could check Avalanche product density, Chandler wafer capacity, Panasonic ReRAM status, used Optane PMem prices or the Everspin nvNITRO history. Those items are marked `[UNVERIFIED]` and listed in §9 as open checks.
- Confidence tags: `[REPORTED]` means a secondary source or search snippet of a primary filing; `[ESTIMATE]` means my own calculation; `[UNVERIFIED]` means training-data memory that I did not re-check in 2026.
- Cost numbers come from a scratch script whose method is described in `A2_device_params.json`. The downstream `models/device_cost_compare.py` should recompute them from that file.

## 1. Key numbers

| Fact | Value | Source / tag |
|---|---|---|
| DDR5 16Gb spot, 2026-08-31 | $53.92 avg (range $37.20–67.50), about $27/GB | [buysellram citing TrendForce](https://www.buysellram.com/?p=20058) [REPORTED] |
| DDR3 4Gb vs DDR5 16Gb spot, early Jul-2026 | $3.19/Gb vs $2.94/Gb | [Wccftech](https://wccftech.com/memory-shortages-drive-ddr4-prices-over-50-in-q3-2026-ddr3-also-impacted-by-higher-costs/) [REPORTED] |
| DDR4 contract, Q3-2026 | up to +50% QoQ | [TweakTown/DigiTimes](https://www.tweaktown.com/news/112541/even-ddr4-ram-is-not-safe-from-the-rampocalypse-prices-rose-over-50-percent-in-q3-2026/index.html?type=News) [REPORTED] |
| DDR5 contract used for the A2 models | about $20/GB today, about $8/GB in the glut (A-05) | [ESTIMATE] (assumptions/A2.md) |
| Everspin 1Gb STT-MRAM die | 105.1 mm², cell 0.0396 µm² (IEDM-2019 gives 0.036), 9.75 Mb/mm², GF 28nm | [TechInsights](https://www.techinsights.com/blog/memory/worlds-first-1-gb-28-nm-stt-mram-product-everspin) [REPORTED] |
| Everspin 1Gb street price | $102.60 @500 pcs → **~$821/GB** | [LCSC](https://www.lcsc.com/product-image/C20342497.html) [REPORTED] |
| Everspin 64Mb xSPI (EM064LX) | $39.38 @480 → ~$5,040/GB; 20-week lead time | [Future](https://futureelectronics.com/p/semiconductors--memory--RAM--nvram--mram/em064lxoab320is1t-everspin-technologies-4175573) [REPORTED] |
| Everspin 16Mb Toggle (MR4A16B) | $37.67 @1000 → ~$19,300/GB | [Future](https://www.futureelectronics.com/p/semiconductors--memory--RAM--nvram--mram/mr4a16bcys35-everspin-technologies-9216418) [REPORTED] |
| **MRAM vs DRAM per bit, street** | 1Gb MRAM is about 30x DDR5 spot and about 32x DDR3 spot. Toggle is about 715x. | computed |
| **MRAM vs DRAM density** | about 42x (9.75 Mb/mm² vs about 400 Mb/mm² for 1b DRAM) | computed. DRAM density is [UNVERIFIED] |
| MRAM vs DRAM manufacturing cost | about $91/GB (1Gb, 28nm) vs about $2.5/GB (1b DDR5) | [ESTIMATE] scratch model |
| Hypothetical 4Gb STT-MRAM at 14/16nm (0.024 µm² cell) | ~229 mm² die, ~$72/GB, about 3.6x the *peak* DDR5 contract price | [ESTIMATE] |
| Samsung eMRAM cell | 0.024 µm² (14nm), 0.017 µm² (8nm), IEDM-2024 | [PC Watch](https://pc.watch.impress.co.jp/docs/column/semicon/1649812.html) [REPORTED] |
| ST ePCM cell | 0.059 µm² at 18nm FD-SOI, vs MRAM 0.129 (16nm) and RRAM 0.174 (12nm), per ST | [Mynavi](https://news.mynavi.jp/techplus/article/20251120-3693534/) [REPORTED] |
| 3D XPoint Gen1 / Gen2 | 128Gb, 206.5 mm², 0.62 Gb/mm², 2 decks / 256Gb, 195.6 mm², 1.31 Gb/mm², 4 decks | [TechInsights G1](https://www.techinsights.com/blog/intel-3d-xpoint-memory-die-removed-intel-optanetm-pcm-phase-change-memory), [G2](https://www.techinsights.com/blog/memory/intel-2nd-generation-xpoint-memory) |
| XPoint die cost at full fab loading | about $1/GB (Gen2), about $1.9/GB (Gen1) | [ESTIMATE] |
| Optane PMem new price, 2019 | $6.6–7.0/GB (128GB), $10.4–11.1/GB (256GB) | [AnandTech](https://www.anandtech.com/show/14180) |

## 2. Company status (verified where possible, Nov-2026)

| Company | Status, with date | Notes |
|---|---|---|
| **Everspin** (Chandler AZ) | Alive and growing. Q3-26 revenue $20.6M (Q3-25: $14.1M); MRAM product sales $16.9M; licensing/royalty/services $3.7M; GM 51.4%; opex $18.5M, including $6.0M of litigation and a $2.7M regulatory provision; cash $43.0M ([8-K](https://www.sec.gov/Archives/edgar/data/0001438423/000162828026067890/mram-20260930xexx991.htm)). FY25 revenue $55.2M, GM 51.2%, GAAP net loss $0.6M ([BW](https://www.businesswire.com/news/home/20260304733194/en/Everspin-Reports-Unaudited-Fourth-Quarter-and-Full-Year-2025-Financial-Results)). | See §3 |
| **Avalanche Technology** (Fremont CA) | Alive. Finished phase 1 of a U.S.-government MTJ-scaling program toward 22nm space MRAM (target 16x density), Mar-2026 ([Avalanche](https://www.avalanche-technology.com/avalanche-technology-phase-one-magnetic-cell-scaling-space-grade-mram-us-government/)). Its 512Mb parts are made at UMC 22nm ([TechInsights](https://www.techinsights.com/blog/avalanche-as301g208-umc-22-nm-512mb-mram-process-analysis)). It is suing Everspin: ITC 337-TA-1487 was instituted 2026-02-27, the early-termination bid was denied in June 2026, and a result is expected around July 2027 ([USITC](https://www.usitc.gov/press_room/news_release/2026/er0227_68226.htm), [BGov](https://news.bgov.com/ip-law/avalanche-beats-early-bid-to-end-itc-patent-case-over-fee-errors)). | The ITC is a supply risk for any Everspin STT design-in, because the STT parts are imported GF Singapore wafers. Everspin says Toggle is not implicated. |
| **GlobalFoundries** | 22FDX+ AutoPro150 eMRAM: Auto Grade 1, 500k cycles, <10ns read, volume in 2H-2026 at **Dresden** ([GNW](https://www.globenewswire.com/news-release/2026/03/09/3251832/0/en/GlobalFoundries-Announces-Availability-of-AutoPro150-eMRAM-Technology-on-Enhanced-FDX-Platform-for-Advanced-Automotive-Applications.html)). Owns the Adesto/Dialog CBRAM technology, bought from Renesas in Feb-2023 and qualifying on 22FDX ([GF](https://gf.com/gf-press-release/globalfoundries-acquires-renesas-non-volatile-resistive-ram-technology-to-proliferate-iot-and-5g-applications/)). | eMRAM is not offered at a U.S. GF fab. |
| **TSMC** | 22RRAM passed 100K-cycle qualification in 2025; N12e RRAM is consumer-qualified ([TSMC AR](https://investor.tsmc.com/static/annualReports/2025/english/pdf/2025_tsmc_ar_e_ch5.pdf)). Infineon AURIX TC4x uses 28nm RRAM. Sanken has a 22ULL RRAM MCU in production since Q4-2025. Everspin will tape out its 256Mb xSPI on TSMC 16nm in 2H-2026 ([transcript](https://www.insidermonkey.com/blog/everspin-technologies-inc-nasdaqmram-q4-2025-earnings-call-transcript-1710559/)). | |
| **Samsung Foundry** | eMRAM roadmap: 14nm, then 8nm (2026), then 5nm ([MRAM-Info](https://mram-info.com/samsung-track-start-14-nm-emram-production-end-2024-8-nm-2026-and-5-nm-2027)). Co-developed 18nm FD-SOI ePCM with ST. | |
| **NVE Corp** (MN) | FY26 (to Mar-26) revenue $26.3M and net income about $15.2M ([NVE](https://www.nve.com/earningsreports/may62026)). | It sells spintronic sensors and couplers, **not memory**. Not a memory partner. |
| **Netsol** (Korea) | 1–64Mb STT-MRAM on Samsung 28FDS since 2022–23 ([MRAM-Info](https://mram-info.com/netsol-launches-stand-alone-stt-mram-product-fabricated-samsung-foundrys-28nm-fdsoi-process)). A 14nm 128Mb–1Gb part was planned for early 2026 [UNVERIFIED]. | Competitor in discrete MRAM. |
| **Numem** | MRAM (NuRAM) chiplets; sampling was planned for late Q4-2025 ([StorageNewsletter](https://www.storagenewsletter.com/2025/01/23/chiplet-summit-numem-unveils-next-gen-memory-solutions-with-nuram/)). No 2026 status found. | The 4TB/s claim is a vendor claim. |
| **Antaios** (SOT) | Raised $11M in 2020 and taped out a test chip in 2021. Dealroom lists it as "closed", undated ([Dealroom](https://app.dealroom.co/companies/antaios)) [UNVERIFIED]. | Independent SOT startups have not survived. |
| **Weebit Nano** | Licensees: SkyWater S130 (qualified 2023), onsemi Treo 65nm BCD (Jan-2025), DB HiTek 130nm BCD, TI (Dec-29-2025). Three customer tape-outs; FY26 revenue guidance ≥A$13.5M; cash A$167M (Jul-2026). New licensing was delayed by fab undercapacity ([Weebit](https://www.weebit-nano.com/news/press-releases/weebit-nano-expands-licensing-agreements-with-key-customers-three-customer-chip-designs-taped-out-to-date/)). | The best-run ReRAM licensor is still sub-scale after about 10 years. |
| **Crossbar** | Private and listed as active; a patent was granted Feb-2026; last raise about $5M around 2024 per CB Insights. | No product evidence. |
| **4DS Memory** | Suspended from ASX quotation 2026-04-29; market cap about $16M ([filings](https://financialfilings.com/companies/4ds-memory-limited/)). Announced PCMO "interface switching" ReRAM for AI in May-2026. | Effectively a zombie. |
| **TetraMem** | MLX200 at 22nm (TSMC) has validated silicon (May-2026). MLX300 at 12nm taped out Oct-27-2026, with 64M INT4 parameters on-chip ([BW](https://www.businesswire.com/news/home/20260516556464/en/TetraMem-Announces-22nm-Multi-Level-RRAM-Analog-In-Memory-Computing-SoC-Milestone)). Offers its RRAM IP for licensing. | Real progress in analog IMC. |
| **HPE memristor** | Dropped from The Machine in 2015 as "not economically viable for volume production". The SK hynix JV was starved of investment, and the product was shelved in Nov-2016 ([MIT TR](https://www.technologyreview.com/2015/06/04/167804/hp-puts-the-future-of-computing-on-hold/), [Register](https://www.theregister.com/2016/11/29/hp_labs_delivered_machine_proof_of_concept_prototype_but_machine_product_is_no_more/)). | Post-mortem: the partner had no incentive to cannibalize its own DRAM. |
| **Panasonic ReRAM** | Not verified in 2026 (no search budget left). From memory: TaOx ReRAM MCUs around 2013, a 40nm ReRAM joint program with UMC, and the semiconductor business sold to Nuvoton in 2020 [UNVERIFIED]. | Treat as inactive. |
| **CBRAM** (Adesto lineage) | Adesto (CBRAM Mavriq/Moneta) went to Dialog, then Renesas, and the technology went to GF in Feb-2023. Renesas serial EEPROM families have an EOL with last-time ship 2026-10-31 ([Renesas](https://www.renesas.cn/zh/document/gde/eol-plan-serial-eeprom-products)). These are conventional EEPROMs, not the CBRAM parts. Moneta status unknown. | |
| **ST ePCM** | 18nm FD-SOI ePCM with Samsung Foundry; STM32V8 announced Nov-18-2025; Stellar automotive on 28nm ([ST](https://newsroom.st.com/?p=17292)). | Captive to ST. Not licensable. |
| **Intel/Micron 3D XPoint** | Dead. See §5. | |
| **SanDisk** | "3D Matrix Memory": prototype multi-Gb chips on 300mm (Investor Day 2026), targeting about half DRAM's cost per bit; imec "Project Neo" since 2024; no dates given ([Notebookcheck](https://www.notebookcheck.net/SanDisk-makes-first-3D-Matrix-Memory-chips-aiming-for-half-the-cost-per-bit-of-DRAM.1374351.0.html), [eeNews](https://www.eenewseurope.com/en/does-phase-change-memory-ride-again-with-sandisk)). | This is the live XPoint revival, run by a T4 incumbent. |

## 3. Everspin deep-dive: what is made where

- **Chandler AZ** (co-located at NXP) makes **Toggle MRAM on 8-inch wafers end-to-end**. It also adds the **MTJ BEOL** on foundry CMOS for STT, and provides Toggle/STT foundry services to DoD ([BW 2024](https://www.businesswire.com/news/home/20240724863768/en/Everspin-Announces-Contract-to-Provide-MRAM-Technology-for-Strategic-Radiation-Hardened-FPGA), [10-K](https://www.sec.gov/Archives/edgar/data/1438423/000162828026014733/mram-20251231.htm)).
- **High-density STT products** (1Gb ST-DDR4 EMD4E001G, PERSYST/EMxxLX xSPI) use **GLOBALFOUNDRIES Singapore 300mm 28nm** CMOS. The 10-K calls this a single-source risk, since GF can discontinue on notice. The 1Gb was first built at GF 28nm (TechInsights). The next-generation monolithic 256Mb xSPI moves to **TSMC 16nm** (tape-out 2H-2026). Conclusion: Everspin's high-density STT is **not U.S.-fabbed CMOS**. Only Toggle and the BEOL are U.S.
- **Microchip Fab 4, Gresham OR**: 10-year foundry agreement signed 2026-04-08. It covers 8-inch wafers, minimum purchases ramping to at most 1,300 wafers per quarter, and first products in 2H-2027. Everspin keeps its IP. **Microchip may not make TMR devices for Everspin's competitors during the term plus 2 years** ([8-K](https://www.sec.gov/Archives/edgar/data/1438423/000162828026024696/mram-20260408xexx991.htm)). This closes the depreciated-200mm-fab route (card A2-06) for anyone else.
- **Defense**: a $40M, 2.5-year subcontract under a DoW prime contract to supply Toggle process technology and foundry services and build onshore Toggle capability. Amentum is reported as the prime, single-source ([Electronics360](https://electronics360.globalspec.com/article/23702/everspin-earns-40-million-mram-deal-for-defense-memory-services)). Everspin also has a rad-hard FPGA program with QuickLogic ($5.26M tranche) and a custom rad-hard STT program with Frontgrade.
- **Markets**: industrial, energy, aerospace/defense, data-center RAID (Dell, Supermicro per Q3-25 call), and IBM FlashCore (FCM4 used 1Gb; FCM5, Oct-2026, uses MRAM *instead of capacitors* ([B&F](https://www.blocksandfiles.com/flash/2026/10/05/ibm-using-everspin-mram-in-5th-gen-flashcore-modules/5300966))). LEO and GEO satellites (Astro Digital, PERSYST 64Mb). Lattice FPGA configuration up to 128Mb.
- **Risks**: Avalanche's ITC case against STT products; litigation cost of $6M per quarter; single-foundry dependence on GF Singapore.
- **Capacity numbers for Chandler were not found** (search budget ran out).

## 4. "With DRAM at 2–3x, which DRAM sockets can MRAM take?"

Answer: **almost none on $/GB.** MRAM takes only sockets where DRAM's job is tiny and its volatility forces extra parts.

1. **Price gap**: about $100/Gb for 1Gb MRAM street (perhaps $25–50/Gb OEM [ESTIMATE]) against about $3/Gb for DRAM spot at the 2026 peak. Even at OEM pricing and peak DRAM, MRAM is 8–30x. In the glut (DDR5 about $1/Gb) it is 25–100x.
2. **Density and cost**: the 1T-1MTJ cell is about 50 F² against 6 F² for DRAM, and periphery and array efficiency are worse (about 40%). That is about 42x less bits per mm². Moving to 14/16nm with a Samsung-class 0.024 µm² cell still leaves a die cost of about $72/GB, above peak DRAM *price*. **MRAM cannot reach DRAM $/GB on any visible roadmap.**
3. **Sockets that work** are those where 16 MB–1 GB of DRAM plus a supercap or battery is used for persistence:
   - SSD/RAID write cache and journal (IBM FCM, LSI/Broadcom RAID, Phison PLP).
   - Battery-backed SRAM in PLCs and metering.
   - FPGA configuration plus scratch.
   - Space, where radiation tolerance matters.
   
   These became *slightly* more attractive in 2026 because the DRAM half of the bill doubled. The capacitor-elimination argument does not depend on DRAM price. Cards A2-01 and A2-03 come from this.
4. **Legacy DDR3/DDR4 EOL sockets (A2-02)**: tempting, but dead. ST-DDR4 MRAM is not DDR3-compatible and holds at most 1Gb per die.

## 5. Optane / 3D XPoint post-mortem, and does 2026 change it?

**Facts**: Micron ended 3D XPoint in Mar-2021, citing "insufficient market validation" ([Micron](https://www.nasdaq.com/press-release/micron-updates-data-center-portfolio-strategy-to-address-growing-opportunity-for)). It had booked about $545M of XPoint/Lehi underutilization charges over the prior four quarters ([Register](https://www.theregister.com/2021/03/17/micron_pulls_the_plug_on/)). It sold Lehi to TI for $900M cash plus about $600M of tools, below book value ([AnandTech](https://www.anandtech.com/show/16800)). TI now runs 65/45nm analog there. Intel began winding Optane down in Q2-2022 and took a $559M inventory impairment ([10-Q](https://www.sec.gov/Archives/edgar/data/50863/000005086322000030/intc-20220702.htm)). Cumulative Intel losses were about $6.8B for 2015–2020 per Objective Analysis, and more than $7B per Coughlin/Handy ([SNIA](https://www.snia.org/sites/default/files/2025-05/SNIA-SDC22-Coughlin-Handy-Persistent-Memories-Without-Optane-Where-Would-We-Be.pdf)).

**Cost per bit**: the die economics were sound. Gen2 reached 1.31 Gb/mm², about 3.3x 1b-class DRAM and roughly 6x the 1z DRAM of 2019 [UNVERIFIED: 1z density from memory], with 91% array efficiency. At full loading I compute about $1–2/GB die cost [ESTIMATE].

**Why it lost**:
1. **Volume.** Lehi ran underloaded, so fixed cost of about $400M a year landed on a small number of bits. Handy's point: a new memory must reach NAND or DRAM-like volume before it is cheaper than DRAM.
2. **Ecosystem.** It needed Intel-only Xeons with DDR-T, and App Direct required software rewrites.
3. **Performance.** Read latency of about 300 ns against about 80 ns for DRAM, plus write power [UNVERIFIED figures].
4. **The 2019 DRAM glut.** It erased Optane's price advantage: PMem at about $6.6/GB sat near DDR4 contract prices after the 2019 drop.
5. **CXL** gave hyperscalers a way to add DRAM capacity without a new medium.

**Does DRAM at 2–3x change the math?** On paper it does: XPoint-class cost of about $1–2/GB against $20/GB DRAM. In practice, no, for a startup:
- **Capital**: T4, because no foundry offers crosspoint PCM.
- **Timing**: a 6-year build lands after the 2028–29 glut.
- **IP**: held by Intel and Micron.
- **Competition**: SanDisk and imec already have prototypes.
- **Volume**: the volume trap is unchanged.

Should a revival exist? Yes, at SanDisk scale (it does). **Not at this venture's scale.** That is card A2-10, killed.

**Spin-off insight**: Optane's death left **stranded inventory** of PMem modules that work in still-deployed Cascade Lake and Ice Lake servers. That is card A2-11, the only T0 arbitrage in this branch. Its main open question is the price of used PMem.

**ePCM survives as embedded NVM** (ST automotive and STM32V8), which is captive. No startup can access it.

## 6. ReRAM / CBRAM / memristor findings

- **Embedded ReRAM is real and in production at foundries**: TSMC 28/22/12nm, Infineon AURIX TC4x, Sanken. The independent IP model is slow. Weebit's ten-year path to about A$13.5M in annual revenue sets the benchmark. 4DS is suspended, Crossbar is quiet, and HPE abandoned the memristor.
- **ReRAM never competes with DRAM** on density or endurance: 1e4–1e5 cycles, against effectively unlimited for DRAM.
- **The U.S. angle that does exist is Weebit ReRAM in SkyWater S130** (Bloomington MN). It is qualified and in the PDK, giving a U.S.-made eNVM path for trusted or defense parts (card A2-07). It competes with Everspin Toggle, which is U.S.-made and has a DoW program.
- **CBRAM is owned by GF.** Expired early patents do not give a business (card A2-08).
- **Analog RRAM compute** (TetraMem) is credible but a T3 chip race (card A2-09).

## 7. Cost-equation summary (scratch model; inputs in `A2_device_params.json`)

| Device | die mm² | Gb/mm² | cost $/GB (die + test/pkg) | vs DDR5 contract today ($20) / glut ($8) |
|---|---|---|---|---|
| Everspin 1Gb STT-MRAM, GF28 | 105.1 | 0.0095 | ~91 | 4.5x / 11x (cost, not price) |
| Toggle 16Mb, Chandler 200mm | ~50 [UNV] | 0.0003 | ~3,400 | 170x / 430x |
| Hypothetical 4Gb STT-MRAM, 14/16nm | ~229 | 0.0175 | ~72 | 3.6x / 9x |
| Weebit ReRAM 4Mb, S130 | ~9.6 core | 0.0004 | ~3,300 | n/a (priced per chip) |
| 3D XPoint Gen1 / Gen2, full loading | 206.5 / 195.6 | 0.62 / 1.31 | ~1.9 / ~1.0 | 0.1x / 0.12–0.24x (cost-competitive at scale) |
| SOT-MRAM 1Gb, N5-class (hypothetical) | ~80 | 0.012 | ~262 | 13x / 33x |
| REF DDR5 16Gb 1b | 40 | 0.40 | ~2.5 | cost basis (price about 8x cost: the 87% GM era) |
| REF DDR3/DDR4 4Gb legacy | 33 | 0.12 | ~4.5 | |

The ±30% wafer-cost uncertainty does not change any conclusion, because the gaps are 4–700x.

## 8. Evidence behind each card (short)

- **A2-01** (PLP kit). Evidence: IBM FCM5 dropped capacitors for MRAM (Oct-2026), IBM FCM4 used 1Gb, LSI RAID journal since 2012, Phison PLP, Everspin supply expansion. Doubt: Everspin gives the same engineering away free.
- **A2-02** (DDR3 swap). Evidence: TrendForce DDR3/DDR4 exit and the 32x bit-price gap. The card's value is the computed kill.
- **A2-03** (NewSpace rad data). Evidence: Frontgrade >1 Mrad Toggle, Astro Digital PERSYST selection, 20–26-week lead times. Doubt: free NASA NEPP data and the founder's lack of credibility.
- **A2-04** (fabless MRAM vendor). Evidence: Netsol/Samsung, Avalanche/UMC, Everspin's scale ($16.9M per quarter of product), ITC war.
- **A2-05** (MRAM DIMM). Evidence: TechInsights density and the computed cost.
- **A2-06** (U.S. MTJ line). Evidence: the Microchip exclusivity clause and the $40M DoW program going to Everspin.
- **A2-07** (TrustNVM). Evidence: Weebit S130 qualification and PDK, the Renesas EEPROM EOL, SBIR fundability. SkyWater's trusted accreditation is [UNVERIFIED] this session.
- **A2-08** (CBRAM licensing). Evidence: GF ownership, Weebit's timeline, 4DS suspension.
- **A2-09** (RRAM IMC). Evidence: TetraMem silicon and tape-outs, the HPE post-mortem.
- **A2-10** (XPoint revival). Evidence: Intel 10-Q, Micron statement, Lehi sale, Handy, TechInsights, SanDisk.
- **A2-11** (PMem salvage). Evidence: 2019 PMem pricing, Intel's excess inventory, DDR4 +50% QoQ. Used price [UNVERIFIED]. Kill experiment: scrape 90 days of eBay sold listings for PMem 128/256/512GB against DDR4 RDIMM 64/128GB; proceed only if the price gap is at least 5x per GB and there are at least 200 sold units a month.
- **A2-12** (MRAM log card). Evidence: MRAM BOM math and the Optane discontinuation. nvNITRO history [UNVERIFIED].
- **A2-13** (SOT LLC). Evidence: imec IEDM-2023 and TED-2025, Antaios/eVaderis closures.
- **A2-14** (eMRAM MCU). Evidence: GF AutoPro150 (Dresden), TSMC RRAM, ST ePCM, Infineon RRAM.
- **A2-15** (NVM-EOL SaaS). Evidence: Renesas EOL, TrendForce DDR3/DDR4 EOL, lead-time data. The competitor set is from memory.

## 9. Ideas considered but NOT carded

- **Brokering or reselling Everspin parts during the shortage.** MRAM is not in shortage-driven price spikes; distributor margins are about 5–15%, and Everspin sells direct and through Mouser, Future and DigiKey. There is no edge.
- **A NVE Corp spintronics partnership for memory.** NVE sells sensors and isolators, not memory, and has no MRAM product.
- **Numem MRAM-chiplet HBM alternative.** These are vendor claims only (4TB/s), with no 2026 status. It belongs to the B-branch chiplet space, and a T3 chiplet startup is not founder-doable.
- **VCMA/VGSOT multi-bit MRAM.** TRL 3. It is folded into A2-13.
- **A selector-only memory (OTS chalcogenide) startup.** Samsung (64Gb, 16nm, IEDM-2023), Micron (256Gb, 4-deck) and SK hynix own the research. It is the same kill as A2-10.
- **Licensing ePCM from ST for a U.S. MCU.** It is captive (ST plus Samsung Foundry) with no licensing program. Folded into A2-14.
- **CBRAM Moneta last-time-buy brokerage.** Status unverified, and the market is tiny.
- **A Panasonic/Nuvoton ReRAM revival.** Status unverified; Nuvoton's interest in licensing is unknown.
- **PCM analog AI (IBM-style).** IBM Research only, TRL 4, no licensing path found. Folded into A2-09.
- **MRAM for LLM KV-cache.** Density about 40x too low and cost about 4x above peak DRAM *price*. Dead before it needs a card, since A2-05 covers it.
- **Acquiring or rolling up Avalanche.** Capital T3 and litigation. Not a founder concept.
- **A space-grade "MRAM SSD".** Avalanche and 3D-Plus-type module makers already do this, and it needs rad-hard controller design. Folded into A2-03.

## 10. Cross-cutting conclusions for Phase 3

1. **No device in this branch beats DRAM on $/GB in 2026 or in the glut.** XPoint could at scale but is T4. The DRAM spike creates no MRAM, ReRAM or PCM DRAM-replacement opportunity for a small company.
2. The device branch makes money in three ways:
   - persistence sockets (PLP, journaling, space, configuration NVM);
   - trusted/U.S.-made niches, where Everspin is already entrenched and DoW-funded;
   - salvage and software around the Optane corpse and the 2026 EOL wave.
3. **Most promising for this founder**:
   - A2-11 (T0, revenue in months, dies in the glut);
   - A2-01 (T1, survives the glut partially, capped size);
   - A2-03 or A2-15 (T0/T1, data/SaaS lever).
   
   The T2 option is A2-07 (SBIR-funded trusted ReRAM chip on SkyWater S130).
4. **Key risk to monitor**: the ITC 337-TA-1487 determination, around mid-2027. An exclusion order on Everspin STT-MRAM would disrupt the supply base of A2-01 and A2-12 and help Avalanche.

## 11. Open verification items (for the orchestrator / Phase 3)

- Used Optane PMem 100/200 prices and volumes (eBay sold listings). This decides A2-11.
- Chandler wafer capacity, and whether Toggle CMOS front-end is fully U.S.
- Avalanche 2026 product densities (1–8Gb space MRAM?) and its foundry (UMC, Taiwan/Singapore).
- SkyWater DMEA trusted-foundry accreditation scope for S130, and Weebit license and royalty terms for small fabless licensees.
- Everspin nvNITRO history (A2-12) and whether Everspin offers reference-design licensing (A2-01).
- 1b DDR5 die density and wafer cost: take these from Phase-1 `models/dram_cost_stack.py` when it exists.
