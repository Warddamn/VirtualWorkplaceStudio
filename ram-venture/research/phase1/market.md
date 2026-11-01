# Phase 1 — Memory market: prices, margins, supply relief, cycle risk

**Agent:** `p1-market` · **As of:** 2026-11-01 · **Companion data:** `research/phase1/price_series.json` · **Sources:** `research/sources/p1-market.jsonl` · **Assumptions:** `research/assumptions/p1-market.md`

> **Method and limits, stated up front.** I ran about 46 web searches. WebFetch could not resolve `trendforce.com`, `technews.tw` or `koreatimes.co.kr` from this session, and the shared search budget ran out before I could run the planned follow-ups (Micron FQ3-26 detail, SK hynix 1Q26 detail, OEM price-hike announcements, automotive shortages). So **every fact below comes from search-result snippets**. A snippet of a primary release (TrendForce press center, SEC EDGAR, Samsung or SK hynix newsroom) is marked *(primary-source snippet)*. Under CONVENTIONS.md that is still at most **[REPORTED]**, because I opened no primary page. Section 11 lists what remains unverified. Anyone who can reach trendforce.com should spot-check the five TrendForce press releases cited in §2.1. They carry most of the load.

---

## 0. Verdict on mission §1 bullets 1, 2 and 4

| §1 bullet | Verdict | Corrected statement (dated, sourced) |
|---|---|---|
| **1a.** "DRAM and NAND prices roughly doubled or more from late 2025 through 2026" | **CORRECTED: understated by about 2×** | TrendForce's *conventional DRAM contract* price changes, compounded at midpoints, rise **≈4.1× from 4Q25 to 4Q26** (range 3.8–4.4×) and **≈6× from 3Q25**. Inputs: 1Q26 +93–98% actual; 2Q26 +58–63%, 3Q26 +13–18% and 4Q26 +10–15% are forecasts ([TrendForce 2026-06-01](https://www.trendforce.com/presscenter/news/20260601-13070.html); [TrendForce 2026-03-31 via TechNews](https://technews.tw/2026/03/31/ai-server-demand-drives-2q26-memory-contract-price-increase-csps-lock-supply-long-term-deals/); [Igor'sLAB on 3Q26](https://www.igorslab.de/en/dram-and-nand-remain-more-expensive-trendforce-sees-slowing-but-still-rising-memory-prices-q3-2026/); [TrendForce 2026-09-30](https://www.trendforce.com/presscenter/news/20260930-13258.html)). 4Q25 itself was +45–50% ([TrendForce 2026-02-26](https://www.trendforce.com/presscenter/news/20260226-12937.html)). DDR5 16Gb *spot* went from **$6.84 (2025-09-20) to ~$57 (Sep 2026), ≈8×** ([tech-insider](https://tech-insider.org/ddr5-ram-prices-2026/); [BuySellRAM/DRAMeXchange 2026-08-31](https://www.buysellram.com/blog/ram-market-update/)). NAND contract rose **≈3.2×** over 1Q26, 2Q26 and 4Q26 alone (+55–60%, +70–75%, +15–20%). I found no 3Q26 NAND figure. [REPORTED; compounding is ESTIMATE] |
| **1b.** "TrendForce has been forecasting further double-digit contract-price increases into Q4 2026" | **CONFIRMED, with one key nuance** | 2026-09-30 release: **conventional DRAM +10–15% QoQ in 4Q26, about +15–20% including HBM, NAND +15–20%**. Server DRAM stays undersupplied, and enterprise SSD is the only segment accelerating ([TrendForce 2026-09-30](https://www.trendforce.com/presscenter/news/20260930-13258.html); [Guru3D](https://www.guru3d.com/story/dram-and-nand-contract-prices-forecast-to-rise-as-much-as-in-q4-2026/)). PC DRAM: +13–18% ([PCMasterInsider](https://pcmasterinsider.com/pc-dram-contract-price-forecast-q4-2026/)). The reported Oct-20 revision to "~+20%" appears only in an AI-generated aggregator and one blog: **[UNVERIFIED]** ([StockHub](https://www.stockhub.kr/en/news/news_b7244c205001); [shattered.io](https://shattered.io/dram-prices-q4-2026-trendforce-ddr5-450-micron-54b-2026/)). **Nuance:** the *rate* of increase has fallen from +93–98% (1Q26) to +10–15% (4Q26). One secondary source reports that NAND contract prices did not rise in Oct 2026, the first pause in 21 months ([tech-insider](https://tech-insider.org/dram-record-high-nand-flat-21-months-october-2026/)) [UNVERIFIED]. |
| **1c.** "meaningful supply relief is widely called a late-2027-or-later story" | **CONFIRMED; the consensus has moved to 2028** | Micron (2026-09-30): industry DRAM bit growth in the low 20s% for both 2027 and 2028, tightness through 2028, new cleanroom output only from late 2028 ([Guru3D](https://www.guru3d.com/story/micron-expects-dram-and-nand-supply-to-tighten-further-through-2028/); [CIO](https://cio.com/article/4229625/memory-squeeze-set-to-tighten-through-2028-micron-says.html)). TrendForce (2026-07-30): the DRAM supply-demand gap *widens* in 2027, while NAND turns to surplus with price pressure in 2H27 ([TrendForce](https://www.trendforce.com/presscenter/news/20260730-13158.html)). SK hynix (2026-10-28): 14 LTAs, supply booked out to 2029 ([Sammy Fans](https://www.sammyfans.com/2026/10/28/sk-hynix-q3-margin-hits-record-80-secures-14-ltas-with-memory-supply-booked-to-2029/amp/)). Barclays: DRAM deficit of 13.9% in 4Q27 ([Guru3D](https://www.guru3d.com/story/ddr4-memory-prices-now-also-rise-as-dram-supply-shortages-intensify-through-2028/)). Minority view: Bloomberg Intelligence says the shortage peaked in 2Q26, the market balances around 4Q27 and may tip to oversupply in 2028 ([KuCoin summary](https://www.kucoin.com/blog/2027-memory-chip-boom-sk-hynix-samsung)). [REPORTED] |
| **1d.** "as AI/HBM demand absorbed wafer capacity and DDR4 lines were cut" | **CONFIRMED, with a correction on DDR4** | HBM's share of DRAM wafer starts is ~18% (2025), ~22% (2026) and ~30% (2027F), but only ~8%, 9% and 13% of bits ([TrendForce via TechNews](https://technews.tw/?p=1565421)). Each HBM bit takes about 3× the wafer of a DDR5 bit, and the ratio rises with each generation ([Tom's Hardware](https://www.tomshardware.com/tech-industry/semiconductors/micron-says-the-silicon-gap-between-hbm-and-ddr5-is-widening-with-every-generation)). DDR4: Micron issued EOL notices in Jun 2025. **Samsung and SK hynix pushed their DDR4 exits back into 2026** because DDR4 had become a cash cow ([TrendForce News 2025-09-02](https://www.trendforce.com/news/2025/09/02/news-samsung-sk-hynix-reportedly-delay-phase-out-to-2026-as-ddr4-becomes-unexpected-cash-cow/)). [REPORTED] |
| **2.** "Reported DRAM-maker operating margins on general-purpose DRAM have been extraordinary (70%+ reported for SK hynix). Margin … captured by three foreign-headquartered firms plus Micron." | **CORRECTED: the margins are higher than stated, the scope is wrong, and the list of who captures them is incomplete** | **SK hynix 3Q26 operating margin ≈80%** (KRW 83.3T OP on KRW 104.6T revenue = 79.7%), released 2026-10-28. 2Q26 was **76.3%** (KRW 60.5T / KRW 79.3T) ([SK hynix 3Q26 release via Placera](https://www.placera.se/pressmeddelanden/sk-hynix-announces-3q26-financial-results-20261028); [2Q26 release](https://www.placera.se/pressmeddelanden/sk-hynix-announces-2q26-financial-results-20260729)). This is a **company-wide** margin that includes HBM and NAND, not a "general-purpose DRAM" margin, which SK hynix does not disclose. The best pure-commodity proxy is **Nanya (Taiwan): 3Q26 gross margin 85.7%, operating margin 80.0%** ([TrendForce News 2026-10-12](https://www.trendforce.com/news/?p=65146)). **Micron: FQ4-26 non-GAAP gross margin ~87%, FQ1-27 guide 86.25%** ([Micron 2026-09-30](https://finviz.com/news/397277/micron-technology-inc-reports-record-fiscal-fourth-quarter-and-full-year-2026-results)); its FQ3-26 operating margin was reported at **81.2%**. **Samsung DS 3Q26: KRW 106.5T OP on KRW 147.1T = 72.4%**, and DS includes loss-making foundry ([Samsung 2026-10-29](https://news.samsungsemiconductor.com/global/samsung-electronics-announces-third-quarter-2026-results/)). Who captures the margin: Samsung 39.4%, SK hynix 24.9%, Micron 23.3% **and CXMT 9.5%** of 2Q26 DRAM revenue ([Evertiq/TrendForce](https://evertiq.com/news/2026-09-07-dram-industry-revenue-surges-595-in-q2-as-supply-lags-demand); [Herald](https://biz.heraldcorp.com/article/10866656)). Nanya and Winbond take the remainder. Micron's share has risen, and Micron is U.S.-headquartered. [REPORTED] |
| **4.** "Memory is brutally cyclical. Every prior shortage ended in a glut. A concept taking five years may land in a 2029 price crash." | **CONFIRMED; the timing may come sooner** | **2018→19:** the 8GB PC module contract average fell from $68 (3Q18) to $25.50 (Aug 2019), **−62.5% in about 4 quarters**. 1Q19 alone fell about −30% ([TrendForce 2018](https://press.trendforce.com/node/view/3173.html); [DigiTimes 2019](https://www.digitimes.com/tag/8gb/0034884.html); [KitGuru](https://www.kitguru.net/?p=406046)). **2022→23:** DRAM ASP fell −20% in 1Q23 and a further −10–15% in 2Q23. The DDR4 8Gb fixed price bottomed at **$1.30 in Sep 2023**. PC-OEM inventory stood at 9–13 weeks. SK hynix posted a KRW 3.4T operating loss in 1Q23 ([The Register](https://www.theregister.com/2023/03/29/dram_prices_crash/); [KED Global](https://www.kedglobal.com/korean-chipmakers/newsView/ked202310040013); [TrendForce 2023-01-09](https://www.trendforce.com/presscenter/news/20230109-11533.html); [The Register](https://www.theregister.com/2023/04/27/samsung_sk_hynix_losses/)). Analysts mostly place the turn in **2028**: BI sees possible oversupply in 2028, BofA expects about −10% ASP in 2028, Baird sees >30% bit growth in 2028, and UBS sees undersupply lasting to at least 2Q28. That puts a downturn **inside a 36-month window**, not after it. [REPORTED] |

**Net re-aim for the mission:** the premise holds, and it is stronger than written. Prices are 4–6× rather than 2×, and commodity-DRAM margins are about 80%. The calendar risk is the problem. Bit supply growth of 20–30%/yr in 2027–28, the first new Korean, U.S. and Chinese cleanrooms in 2027–28, and a NAND surplus already forecast for 2H27 all point to a **2028 inflection**. Any concept whose revenue depends on DRAM staying at 2026 prices has, at best, a 12–24-month window. Section 7 sizes the glut.

---

## 1. The most decision-relevant findings

1. **The price spike is about 4× in a year on contract (4Q25→4Q26) and about 8× on DDR5 spot (Sep-25→Sep-26).** It is also decelerating sharply: QoQ increases were +95.5% (1Q26), +60.5% (2Q26F), +15.5% (3Q26F) and +12.5% (4Q26F) (§2.1).
2. **Commodity DRAM now earns *more per bit* than HBM3E.** DDR5 16Gb spot is about $27–28/GB (Aug–Sep 2026). HBM3E sells for about $1.50/Gb ≈ **$12/GB**. Samsung said on its 1Q26 call that conventional DRAM was more profitable than HBM ([FN News 2026-04-30](https://en.fnnews.com/news/202604301057582454)). HBM4 2027 asks of about $4.5–4.9/Gb (≈$36–39/GB) and a forecast **+121% blended HBM ASP in 2027** are how suppliers plan to restore the premium ([Silicon Analysts on TrendForce](https://siliconanalysts.com/market/trendforce-2027-hbm-blended-asp-to-jump-121-as-hbm4-hbm4e-mix-shifts-2026-10-06); [Sammy Fans](https://www.sammyfans.com/2026/10/02/samsung-seeks-more-than-3x-hbm3e-pricing-for-hbm4/)).
3. **Margins are 72–87% across every DRAM maker,** including second-tier Nanya (80% operating). Micron's FY26 revenue was $133.19B against $37.38B in FY25 (3.6×) ([Pulse 2.0](https://pulse2.com/micron-reports-record-fiscal-q4-revenue-of-54-23-billion-and-fy2026-revenue-of-133-19-billion/)).
4. **Relief is a 2028 story, and it arrives on several fronts at once.** Samsung P4 (1c, 2027, much of it allocated to HBM) and P5 (2028). SK hynix M15X (ramping through 2026–27) and Yongin Y1 (cleanroom Feb–Mar 2027). Micron ID1 (first wafers mid-2027) and ID2 (late 2028). CXMT going from about 320K to 420K wafers/month by 2027 after an $8.5B IPO on 2026-07-27 (§4).
5. **HBM takes about 22% of DRAM wafer starts in 2026, heading to about 30% in 2027, for only 9–13% of bits.** That crowding-out is the structural reason conventional supply grows slowly even as capex explodes (§6).
6. **A 60% DDR5 fall in 2028–29 is plausible and historically ordinary:** 2018–19 saw −62.5% on modules. It would still leave DDR5 about 2.4× its 3Q25 contract level and about 3.3× its Sep-2025 spot level (§7).
7. **Retail is behind contract and spot.** A 32GB DDR5-6000 kit costs about $409–470 (Sep 2026) against $100–200 a year earlier, about $13–14/GB. That is *below* DDR5 chip spot ($27–28/GB). The spot market is thin and panic-priced, and channel prices can still move up (§8).
8. **Mobius Materials** is a Richmond, VA, YC-backed **secondary-market marketplace** for surplus semiconductors. It raised a $3M seed in Dec 2025. Its "DRAM Market Report" is content marketing for that marketplace, not a paid data product (§9).

---

## 2. Price history, Q1-2024 → Q4-2026

### 2.1 TrendForce quarterly contract-price changes (QoQ)

"F" = forecast; "A" = TrendForce's retrospective figure. All rows are [REPORTED]: primary-source snippets or secondary coverage of TrendForce.

| Quarter | Conventional DRAM | Blended DRAM incl. HBM | NAND Flash | Notable sub-segment | Source |
|---|---|---|---|---|---|
| 1Q24 | **+13–18%** F | — | — | Mobile DRAM led | [StorageNewsletter 2024-01-11](https://www.storagenewsletter.com/2024/01/11/dram-contract-prices-projected-to-increase-13-18-in-1q24/) |
| 2Q24 | **+13–18%** F (raised from +3–8% after the 2024-04-03 Taiwan quake) | — | — | — | [StorageNewsletter 2024-05-16](https://www.storagenewsletter.com/2024/05/16/dram-contract-prices-for-2q24-adjusted-to-13-18-increase/) |
| 3Q24 | **+8–13%** F (raised about 5 pp) | — | — | — | [TrendForce 2024-08-15](https://www.trendforce.com/presscenter/news/20240815-12254.html) |
| 4Q24 | **0–5%** F [UNVERIFIED repost] | — | — | LPDDR4X −5–10% (CXMT oversupply) | [TechPowerUp repost](https://techpowerup.com/forums/threads/329219) |
| 1Q25 | **decline** (DDR4 −10–15%, DDR3 −3–8%) F | — | — | Graphics DRAM −5–10% | [I-Connect007/TrendForce](https://mail.iconnect007.com/article/143527/passive-buyer-strategies-drive-dram-contract-prices-down-across-the-board-in-1q25/143524/ein) |
| 2Q25 | **0 to −5%** F | +3–8% | — | DDR4 EOL rally begins | [TechPowerUp repost](https://techpowerup.com/forums/threads/334591) |
| 3Q25 | **up**; magnitude not captured | — | — | "DDR4 surging" | DRAM revenue +30.9% QoQ to $41.4B ([China Times](https://wantrich.chinatimes.com/news/20251126900578-420201)) |
| 4Q25 | **+45–50%** A | **+50–55%** A | — | — | [TrendForce 2026-02-26](https://www.trendforce.com/presscenter/news/20260226-12937.html) |
| 1Q26 | **+93–98%** A (forecast had been raised from +55–60% to +90–95% on 2026-02-02) | +80–85% F | **+55–60%** F (raised from +33–38%) | PC DRAM >+100%, the largest on record; LPDDR4X/5X about +90% | [TrendForce 2026-02-02](https://www.trendforce.com/presscenter/news/20260202-12911.html); [TrendForce 2026-06-01](https://www.trendforce.com/presscenter/news/20260601-13070.html); [EE Times Asia](https://www.eetasia.com/?p=72392) |
| 2Q26 | **+58–63%** F (no retrospective found) | — | **+70–75%** F | LPDDR5X +78–83%; LPDDR4X +70–75%; consumer DRAM +45–50% | [TechNews 2026-03-31](https://technews.tw/2026/03/31/ai-server-demand-drives-2q26-memory-contract-price-increase-csps-lock-supply-long-term-deals/); [China Times 2026-05-15](https://wantrich.chinatimes.com/news/20260515900291-420101) |
| 3Q26 | **+13–18%** F. The Aug-31 PC DRAM update said gains exceeded that forecast | — | not captured | DDR4 8Gb module about +50% QoQ (DigiTimes). Nanya ASP **+>60%** QoQ as LTAs reset in July. SK hynix DRAM ASP about +22% (analyst estimate) | [Igor'sLAB](https://www.igorslab.de/en/dram-and-nand-remain-more-expensive-trendforce-sees-slowing-but-still-rising-memory-prices-q3-2026/); [Gizchina](https://www.gizchina.com/tech/ddr4-prices-are-jumping-50-this-quarter-and-it-wont-stop-until-2028); [TrendForce News](https://www.trendforce.com/news/?p=65146) |
| 4Q26 | **+10–15%** F (Sep-30). "~+20%" Oct-20 revision [UNVERIFIED] | **+15–20%** F | **+15–20%** F | PC DRAM +13–18%; enterprise SSD accelerating | [TrendForce 2026-09-30](https://www.trendforce.com/presscenter/news/20260930-13258.html); [PCMasterInsider](https://pcmasterinsider.com/pc-dram-contract-price-forecast-q4-2026/) |

**Consistency check.** TrendForce DRAM industry revenue: 3Q25 $41.4B, then 4Q25 $53.58B (+29.4%), then 1Q26 +81%, giving ≈$97.0B [ESTIMATE], then 2Q26 **$154.73B** (+59.5%). Compounding 53.58 × 1.81 × 1.595 = 154.7, which matches the reported 2Q26 figure ([TrendForce 2026-02-26](https://www.trendforce.com/presscenter/news/20260226-12937.html); [Evertiq 2026-09-07](https://evertiq.com/news/2026-09-07-dram-industry-revenue-surges-595-in-q2-as-supply-lags-demand)). 2Q26 revenue growth of +59.5% is consistent with the +58–63% price forecast plus roughly flat bits.

### 2.2 Cumulative conventional-DRAM contract index [ESTIMATE: midpoint compounding]

| Quarter | QoQ midpoint | Index (3Q25 = 100) |
|---|---|---|
| 3Q25 | — | 100 |
| 4Q25 | +47.5% (A) | 148 |
| 1Q26 | +95.5% (A) | 288 |
| 2Q26 | +60.5% (F) | 463 |
| 3Q26 | +15.5% (F) | 535 |
| 4Q26 | +12.5% (F) | **601** (range 550–657) |

So **4Q25→4Q26 ≈ 4.1×** (range 3.8–4.4×; 4.35× if the unverified +20% for 4Q26 holds). For comparison, the trough-to-trough 2024 run (1Q24–3Q24) was about +40% cumulative. Before late 2025 nothing resembled this.

### 2.3 Price levels and $/GB

All are [REPORTED] via snippets. "Spot" means DRAMeXchange session averages, which are small-lot and thin (see assumptions). Contract prices are rarely published at chip level outside TrendForce's paywall.

| Product | Date | Price | $/GB | Basis / source |
|---|---|---|---|---|
| DDR4 8Gb (1Gx8) PC DRAM, avg fixed (contract) | Sep 2023 (cycle bottom) | $1.30 | $1.30 | [KED Global](https://www.kedglobal.com/korean-chipmakers/newsView/ked202310040013) |
| DDR4 8Gb, avg fixed (contract) | Jun 2025 | $2.60 (+23.8% MoM) | $2.60 | [Asia Economy](https://view.asiae.co.kr/en/article/2025070108020310879) |
| DDR4 16Gb (1Gx16) 3200, spot | Jun 2025 | ~$12 ($12.3) | ~$6 | [TrendForce News 2025-06-24](https://www.trendforce.com/news/2025/06/24/news-historic-ddr4-spot-price-rally-reportedly-doubles-ddr5-propelling-nanya-techs-inventory-windfall/) |
| DDR5 16Gb (2Gx8) 4800/5600, spot | Jun 2025 | ~$6 ($6.05) | ~$3 | same |
| DDR4 16Gb vs DDR5 16Gb chip (DigiTimes) | Aug 2025 | $9.17 vs $5.99 | $4.6 vs $3.0 | [TechRadar](https://www.techradar.com/computing/memory/want-to-upgrade-the-ddr4-ram-in-your-pc-new-report-is-a-clear-signal-you-should-buy-sooner-rather-than-later) |
| DDR5 16Gb, spot | 2025-09-20 | $6.84 | $3.42 | [tech-insider](https://tech-insider.org/ddr5-ram-prices-2026/) |
| DDR5 contract (Samsung quote; unit ambiguous) | Dec 2025 | ~$19.20 | — | [Computing UK](https://www.computing.co.uk/news/2025/chips-and-components/samsung-doubles-ddr5-contract-prices) |
| DDR5 16Gb, spot | 2026-03-11 | $39.57 (range $26–52); eTT $21.15 | $19.8 (eTT $10.6) | [DRAMeXchange home](https://www.dramexchange.com/) |
| DDR5 16Gb, spot | early Jul 2026 | avg mid-$40s, high $61 | ~$22–23 | [tech-insider](https://tech-insider.org/ddr5-ram-prices-2026/) |
| DDR5 16Gb, spot | 2026-08-31 | $53.92 (range $37.20–67.50) | $26.96 | [BuySellRAM/DRAMeXchange](https://www.buysellram.com/blog/ram-market-update/) |
| DDR5 16Gb, spot | Sep 2026 | ~$57 | ~$28.5 | secondary blog via search snippet; page attribution uncertain (appeared alongside [tech-insider Canada](https://tech-insider.org/ca/ram-ddr5-ssd-price-shortage-canada-2026/)) [UNVERIFIED] |
| DDR4 8Gb (1Gx8), spot (TrendForce board) | 2026-06-05 / 06-24 / 08-03 | $16 / $16 / $21 | $16–21 | [TrendForce spot](https://www.trendforce.com/price/dram/dram_spot); [TrendForce board](https://www.trendforce.com/price_dram.html) |
| DDR4 8Gb, spot (alt. quote, likely branded 3200) | early Mar / Jul 28 / Aug 31 2026 | $33.02 / $42.08 / $44.37 | $33–44 | [Mobius Materials](https://www.mobiusmaterials.com/whitepapers/dram-market-report-2026); [BuySellRAM](https://www.buysellram.com/blog/ram-market-update/) |
| 64GB DDR5 RDIMM, contract | 4Q25 → 1Q26 | $450 → >$900 (possibly >$1,000 in 2Q26) | $7.0 → $14.1 | Counterpoint via [EE Times Asia](https://www.eetasia.com/memory-prices-surging-by-90-from-4q-2025/) |
| 64GB DDR5 RDIMM, contract (Citi forecast) | 1Q26 → 4Q26F | $873 → $1,586 | $13.6 → $24.8 | Citi note, May 2026 (via search snippet; underlying page not identified) [UNVERIFIED] |
| 64GB DDR5 RDIMM, retail street | Aug 2026 | ~$2,064 | ~$32 | [Servnet UK tracker](https://www.servnetuk.com/research/ddr5-server-memory-price-tracker-2026) |
| Mobile DRAM (LPDDR5X) LTA ceiling | ~May 2026 | up to ~$21/GB | ~$21 | [Wccftech](https://wccftech.com/mobile-dram-prices-expected-to-increase-by-100-quarter-over-quarter-as-long-term-agreements-now-getting-signed-at-prices-as-high-as-21-gb/amp/) |
| HBM3E (2026 contract) | 2026 | ~$1.50/Gb | ~$12 | [Sammy Fans 2026-10-02](https://www.sammyfans.com/2026/10/02/samsung-seeks-more-than-3x-hbm3e-pricing-for-hbm4/) |
| HBM4 (2027 ask, Samsung) | Oct 2026 | "mid-to-high $4/Gb" | ~$36–39 | same; [Silicon Analysts](https://siliconanalysts.com/market/samsung-hbm4-2027-pricing-set-to-more-than-double-2026-10-07) |
| NAND 512Gb TLC wafer, contract | Nov 2025 | +>65% MoM (level not captured) | — | [TrendForce 2025-12-01](https://www.trendforce.com/presscenter/news/20251201-12807.html) |
| NAND wafer | May 2026 | "high-price stagnation", TLC price deadlock | — | [TrendForce May-2026 report summary](https://www.trendforce.com/research/download/RP260529GY) |

**Reading the $/GB column.** A DRAM bit that sold for about $1.3–3/GB at contract in 2023–mid-2025 now trades at about **$14–25/GB at contract** (server RDIMM) and about **$27–28/GB at spot** (DDR5 chips). Retail sits at about **$13–18/GB** (§8). For the cost-stack agent, the gap between the ~$2/GB pre-spike price and about $14–25/GB today is all margin, because wafer costs did not move 5–10×.

### 2.4 The DDR4/DDR5 price inversion: yes, twice

- **First inversion, Jun–Aug 2025.** DDR4 16Gb spot reached about $12, roughly double DDR5 16Gb at about $6. TrendForce called this a first in DRAM history ([TrendForce News 2025-06-24](https://www.trendforce.com/news/2025/06/24/news-historic-ddr4-spot-price-rally-reportedly-doubles-ddr5-propelling-nanya-techs-inventory-windfall/)). Module prices crossed over in June 2025 ([TechPowerUp](https://www.techpowerup.com/338380/ddr4-module-prices-overtake-ddr5-for-the-first-time)). The trigger was the DDR4 EOL notices and output cuts from Samsung and Micron (§6).
- **Second inversion, 2026, persisting in Oct 2026.** Barclays: DDR4 contract +4% MoM and +24% over 3 months in Oct 2026, against DDR5 +3% and +20%. DDR4 is now dearer than DDR5 in some channels ([TechNews Finance 2026-10-13](https://finance.technews.tw/2026/10/13/the-shortage-of-memory-chips-may-continue-for-another-two-years/); [Guru3D](https://www.guru3d.com/story/ddr4-memory-prices-now-also-rise-as-dram-supply-shortages-intensify-through-2028/)). On the branded-spot line, DDR4 8Gb at $44.37 (=$44/GB) compares with DDR5 16Gb at $53.92 (=$27/GB), a **1.65× per-GB premium for the older part** [ESTIMATE from 2026-08-31 snapshot]. DDR3 is also rising ([Wccftech](https://wccftech.com/memory-shortages-drive-ddr4-prices-over-50-in-q3-2026-ddr3-also-impacted-by-higher-costs/)).
- **Why it matters to us:** legacy and long-lifecycle DRAM is now the *tightest* part of the market. This is the strongest price signal in the dataset for §3C trailing-node or legacy concepts. It is also the first thing to collapse once Samsung and SK hynix finish their DDR4 exits and CXMT, Nanya and Winbond backfill.

### 2.5 HBM premium inversion

TrendForce forecast in Oct 2025 that DDR5 profitability would surpass HBM3E from 1Q26, and that the HBM3E/DDR5 price multiple would shrink from 4–5× to 1–2× by end-2026 ([TrendForce 2025-10-29](https://www.trendforce.com/presscenter/news/20251029-12758.html)). By 2026 the multiple fell **below 1×** on a spot basis (HBM3E about $12/GB against DDR5 spot about $27/GB). Samsung confirmed on 2026-04-30 that conventional DRAM was more profitable than HBM, because annual HBM contracts lagged quarterly commodity resets ([FN News](https://en.fnnews.com/news/202604301057582454)). Suppliers responded by asking for 2027 HBM4 at about 3× the HBM3E price. TrendForce sees blended HBM ASP **+121%** in 2027, and HBM contract prices could rise 70–140%. Some LTAs signed after 2Q26 include price ceilings ([Silicon Analysts](https://siliconanalysts.com/market/trendforce-2027-hbm-blended-asp-to-jump-121-as-hbm4-hbm4e-mix-shifts-2026-10-06); [Herald](https://biz.heraldcorp.com/article/10852833)).

---

## 3. TrendForce's latest Q4-2026 forecast and 2027 outlook

**4Q26 (release 2026-09-30, [TrendForce](https://www.trendforce.com/presscenter/news/20260930-13258.html), [X post](https://x.com/trendforce/status/2105281618617274854)):**
- Conventional DRAM contract **+10–15% QoQ**. Including HBM, **+15–20%** ([Guru3D](https://www.guru3d.com/story/dram-and-nand-contract-prices-forecast-to-rise-as-much-as-in-q4-2026/)). PC DRAM +13–18%.
- NAND Flash contract **+15–20% QoQ**. Enterprise SSD is the only segment accelerating.
- Drivers: CSP AI-infrastructure procurement. Consumer-side (phone, PC) demand pressure persists, and phone makers are drawing down inventory.
- **Mission premise check:** the mission's "+10–15% conventional, +15–20% incl. HBM" matches. The "October update ~+20%" is **not confirmed**. It appears only in an AI-written StockHub summary (2026-10-20) and a blog (shattered.io). TrendForce did publish a DRAM Market Bulletin on 2026-10-21 ([listing](https://www.trendforce.com/research/download/RP261021BP)), but I could not see its contents. **Treat +10–15% as the official number.**

**2027 (TrendForce release 2026-07-30 and report RP260728GY):**
- **DRAM stays tight. The supply-demand gap *widens* in 2027** because demand growth outruns supply ([TrendForce 2026-07-30](https://www.trendforce.com/presscenter/news/20260730-13158.html)).
- **DRAM supply bit growth is about 24% in 2027** from new fabs and node migration. Relief from HBM crowding-out is "limited". The 2026 sufficiency ratio is about −1% to −2% ([report summary](https://www.trendforce.com/research/download/RP260728GY)).
- Demand drivers: more HBM per accelerator, **SOCAMM** and other new server memory specs, and server unit growth above 2026's +17%.
- **NAND diverges.** Its sufficiency ratio turns positive in 2027, with **downward price pressure in 2H27**. NAND is the leading indicator to watch for the DRAM turn.
- PC DRAM supply is reported to *contract* in 2027 ([TechEnclave](https://techenclave.com/news/items/trendforce-expects-pc-ram-supply-to-contract-in-2027)) [UNVERIFIED].
- HBM: blended ASP +121% (2027 vs 2026). HBM share of DRAM wafer starts about 30% by end-2027.

---

## 4. Supply relief: when and why

| Maker / site | What | Timing (latest reported) | Note | Source |
|---|---|---|---|---|
| **Samsung P4** (Pyeongtaek) | New 1c DRAM line, ~100–120K wafers/month | ~1Q27 | Much of P4 cleanroom reportedly allocated to next-gen **HBM** in 2027, which *tightens* conventional supply | [Borecraft](https://borecraft.com/2026/05/26/samsungs-p4-hbm-pivot-tightens-the-2027-dram-crunch/) |
| **Samsung P5** | DRAM + HBM | Phase-1 equipment move-in ~May–Jun 2027 (pulled in); full-scale 2028 | P5 plus P5 Fab 2 said to rival P1–P4 combined; Fab 2 ops 2029–30 | [Sammy Fans 2026-09-28](https://www.sammyfans.com/2026/09/28/samsung-accelerates-p5-expansion-for-dram-and-hbm-production/); [DigiTimes](https://www.digitimes.com/news/a20260526VL205.html) |
| Samsung capex | 2026 total ~KRW 84.4T, DS KRW 76.8T | 2026 | 3Q26 capex KRW 29T, 93.8% to DS | [Samsung 3Q26](https://news.samsungsemiconductor.com/global/samsung-electronics-announces-third-quarter-2026-results/); [XenoSpectrum](https://xenospectrum.com/en/samsung-q3-ds-profit-capex-share/) |
| **SK hynix M15X** (Cheongju) | DRAM/HBM | 1st cleanroom opened Oct 2025, ramping 2026–27; reported 40K → ~80K wpm in 2027 (TrendForce) or 35K → 55–60K (The Elec) | Mostly HBM-oriented | [TrendForce News](https://www.trendforce.com/news/?p=53638) (via snippet); [Reuters/Yahoo](https://finance.yahoo.com/news/exclusive-sk-hynix-speeds-chip-220217637.html) |
| **SK hynix Yongin Y1** | DRAM/HBM | Cleanroom/first tools Feb–Mar 2027 (pulled in ~2 months) | Volume output realistically 2028 [ESTIMATE: typical 9–12 months tool-in to volume] | [Cleanroom Technology](https://cleanroomtechnology.com/sk-hynix-to-open-cleanroom-at-yongin-fab) |
| SK hynix Yongin Y2 and further fabs | ~$38B approved | No output before Dec 2028; Y2 cleanroom Jun 2029 | Target ~1M DRAM wpm by 2030–31 | [Webull](https://www.webull.com/news/15408108739732480) |
| **Micron ID1** (Boise) | Leading-edge DRAM | First DRAM wafer output **mid-calendar 2027** | — | [Micron FY26 10-K](https://www.sec.gov/Archives/edgar/data/0000723125/000072312526000023/mu-20260903.htm) (primary-source snippet) |
| **Micron ID2** (Boise) | DRAM | Construction start 2026; initial output **late 2028** | — | [Micron 10-Q FQ3-26](https://www.sec.gov/Archives/edgar/data/0000723125/000072312526000015/mu-20260528.htm) |
| **Micron New York** (Clay) | DRAM | Groundbreaking Jan 2026; supply **2030+** | Slipped from 2029 in older reports | [Micron 10-Q FQ2-26](https://www.sec.gov/Archives/edgar/data/723125/000072312526000006/mu-20260226.htm) |
| Micron HBM capacity | HBM wafers | ~100K wpm by end-2026 (+60K) | Further crowds out conventional | [TrendForce News 2026-09-04](https://www.trendforce.com/news/2026/09/04/news-micron-reportedly-to-add-60k-hbm-wafersm-reaching-100k-by-year-end-to-narrow-gap-with-samsung-sk-hynix/) |
| **CXMT** (China) | DDR4/DDR5/LPDDR5 | ~320K → ~420K wpm by 2027 (Counterpoint); SemiAnalysis: +85K wpm in 2026, ~500K new wafer starts by end-2028 | IPO 2026-07-27 on STAR (688825), raised CNY 57.9B (~$8.5B), closed +466% on day 1; **no HBM project in prospectus**, so all of it is conventional bits; 2Q26 DRAM share 9.5% | [Tom's Hardware](https://www.tomshardware.com/tech-industry/cxmt-closes-up-466-percent-in-shanghai-debut-with-no-hbm-project-in-its-ipo-prospectus); [Counterpoint](https://counterpointresearch.com/en/insights/cxmt-stock-market-big-three-memory-club); [Herald](https://biz.heraldcorp.com/article/10866656) |
| **Nanya / Winbond** (Taiwan) | Legacy and specialty DRAM | Not captured (search budget exhausted) | Nanya bits fell mid-single-digit QoQ in 3Q26, so it is not adding much supply | [TrendForce News](https://www.trendforce.com/news/?p=65146) |

**Bit-growth forecasts:**

| Forecaster | 2026 | 2027 | 2028 | Source |
|---|---|---|---|---|
| Micron (industry DRAM bit shipments) | mid-20s% | low-20s% | low-20s% | [Guru3D](https://www.guru3d.com/story/micron-expects-dram-and-nand-supply-to-tighten-further-through-2028/); [Evertiq](https://evertiq.com/design/2026-10-06-microns-quarterly-revenue-nearly-quintuples-to-542-billion) |
| TrendForce (supply bits) | — | ~24% | — | [RP260728GY summary](https://www.trendforce.com/research/download/RP260728GY) |
| BofA | 25% | 19% | 19% | KuCoin news summary via search snippet [UNVERIFIED] |
| Baird | — | ~20% | **>30%** | [TMGM](https://www.tmgm.com/en/analysis/market-insight/micron-dram-supply-tightening) |

**Why relief is late.** (1) About 22–30% of wafers go to HBM, which yields about one-third the bits per wafer. (2) New cleanrooms take 18–36 months from shell to volume. The first new Korean and U.S. shells get tools in 2027, and volume follows in 2028. (3) Makers have locked in multi-year LTAs (SK hynix to 2029) and say they are disciplined. (4) CXMT is the wildcard. It is the only maker adding large *conventional* capacity in 2026–27, and that capacity could hit DDR4/DDR5/LPDDR5 prices before Korean supply arrives.

**Bottom line: a 2028 relief window.** Baird's >30% bit growth for 2028 coincides with ID2, P5, Yongin Y1 volume and CXMT's ~420–500K wpm. 2028 is the most likely year for contract prices to turn down. NAND turns first (2H27).

---

## 5. Reported margins

| Company | Period | Revenue | Operating profit | Op margin | Gross margin | Source |
|---|---|---|---|---|---|---|
| **SK hynix** | 3Q26 (reported 2026-10-28, preliminary, unaudited) | KRW 104.6T | KRW 83.3T | **79.7% (~80%)**, a record | — | [Placera/PRN](https://www.placera.se/pressmeddelanden/sk-hynix-announces-3q26-financial-results-20261028); [investingLive](https://investinglive.com/stocks/sk-hynix-q3-operating-profit-beats-at-83tn-won-unveils-100tn-won-shareholder-payout-plan/) |
| SK hynix | 2Q26 (2026-07-29) | KRW 79.3T | KRW 60.5T | **76.3%** | — | [Placera/PRN](https://www.placera.se/pressmeddelanden/sk-hynix-announces-2q26-financial-results-20260729) |
| SK hynix | 2Q25 → 3Q25 → 4Q25 → 1Q26 | — | — | 41% → 47% → 58% → 72% | — | Tracker in search summary [REPORTED, attribution uncertain] |
| **Samsung DS** | 3Q26 (2026-10-29) | KRW 147.1T | KRW 106.5T | **72.4%** [ESTIMATE from reported figures]; includes foundry/LSI | — | [Samsung newsroom](https://news.samsungsemiconductor.com/global/samsung-electronics-announces-third-quarter-2026-results/) |
| Samsung (consolidated) | 3Q26 | KRW 195.3T | KRW 107.4T (DS = ~99% of it) | 55% | — | same; [XenoSpectrum](https://xenospectrum.com/en/samsung-q3-ds-profit-capex-share/) |
| Samsung memory (pre-release estimate) | 3Q26 | — | ~KRW 110T (DRAM ~80T, NAND ~30T) | — | — | [SBS](https://news.sbs.co.kr/english/endPagePrintPopup.do?news_id=N1008818605) |
| **Micron** | FQ4-26 (qtr to ~2026-09-03; reported 2026-09-30) | $54.23B (+31% QoQ, +379% YoY) | ~$45B [ESTIMATE] | ~83% [ESTIMATE: 87% GM less ~$2B opex] | **~87% non-GAAP** | [Micron via Finviz](https://finviz.com/news/397277/micron-technology-inc-reports-record-fiscal-fourth-quarter-and-full-year-2026-results); [MarketBeat](https://www.marketbeat.com/instant-alerts/transcript-micron-technology-q4-earnings-call-highlights-2026-09-30/) |
| Micron | FQ3-26 (qtr to ~May 2026) | — | — | **81.2%** (as quoted in Korean press) | — | 2Q26 SK hynix coverage via search snippet [REPORTED] |
| Micron | **FQ1-27 guidance** | $61.5B ± 1.5B | — | ~83% [ESTIMATE: 86.25% GM less $2.06B opex] | **86.25% non-GAAP** (85.95% GAAP); "low point for FY27" | [Micron via Finviz](https://finviz.com/news/397277/micron-technology-inc-reports-record-fiscal-fourth-quarter-and-full-year-2026-results) |
| Micron | FY26 | $133.19B (vs $37.38B FY25) | — | — | — | [Pulse 2.0](https://pulse2.com/micron-reports-record-fiscal-q4-revenue-of-54-23-billion-and-fy2026-revenue-of-133-19-billion/) |
| **Nanya** | 3Q26 (2026-10-12) | NT$133.65B (+61.9% QoQ) | NT$106.89B | **80.0%** (+6.3 pp) | **85.7%** (+6.2 pp) | [TrendForce News](https://www.trendforce.com/news/?p=65146); [Focus Taiwan](https://focustaiwan.tw/business/202610120025) |
| Nanya | 2Q26 | — | — | ~73.7% [derived] | ~79.5% [derived] | same |
| *Cycle trough reference* | SK hynix 1Q23 | KRW 5.1T (−58% YoY) | **−KRW 3.4T** | about −67% | — | [The Register](https://www.theregister.com/2023/04/27/samsung_sk_hynix_losses/) |

**Interpretation.** The "70%+ SK hynix" claim is **confirmed and understated**. Every DRAM maker with disclosed results is at 72–87% gross margin and roughly 72–83% operating margin. Nanya, a mostly commodity and legacy DRAM maker with no HBM, earns 80% operating margin, which is the cleanest evidence that *general-purpose* DRAM itself carries these margins. The same companies posted operating losses of about −67% in 1Q23. A venture that prices against these margins is pricing against a peak.

---

## 6. The HBM allocation story

- **Wafer share.** TrendForce estimates HBM wafer starts at the big three as about **18% (2025), 22% (2026) and ~30% (2027)** of all DRAM wafer starts, measured at year-end. HBM's share of DRAM *bits* is only about **8%, 9% and 13%** ([TrendForce via TechNews](https://technews.tw/?p=1565421)). Samsung's Kim Taewoo (Sep 2026) put it at about 20% now and nearly 30% next year. Other citations give 23% for 2026.
- **Wafer-per-bit penalty.** Micron puts it at **about 3×** wafer area per bit against DDR5, the "3:1 trade ratio", and says the ratio is *rising* with each generation because of larger dies, TSV area and stack-yield loss ([Tom's Hardware](https://www.tomshardware.com/tech-industry/semiconductors/micron-says-the-silicon-gap-between-hbm-and-ddr5-is-widening-with-every-generation); [XenoSpectrum](https://xenospectrum.com/en/micron-hbm-ddr-silicon-gap/)). The HBM4 ratio is undisclosed; some sources cite 3–4×. Mobius cites about 4× ([Mobius](https://www.mobiusmaterials.com/post/the-first-semiconductor-memory-supercycle-in-seven-years)).
- **Implied crowding-out [ESTIMATE].** If HBM moves from 22% to 30% of wafers at 3× wafers/bit, conventional DRAM loses about 8 pp of wafer starts, about 10% of its base, in 2027. That cancels roughly half of the ~20–24% gross bit growth for conventional parts.
- **HBM4 ramp.** Samsung "significantly scaled up" HBM4 sales in 3Q26 ([Samsung](https://news.samsungsemiconductor.com/global/samsung-electronics-announces-third-quarter-2026-results/)). SK hynix's 3Q26 was helped by HBM4 shipments. Micron is adding about 60K HBM wpm to reach about 100K by end-2026 ([TrendForce News](https://www.trendforce.com/news/2026/09/04/news-micron-reportedly-to-add-60k-hbm-wafersm-reaching-100k-by-year-end-to-narrow-gap-with-samsung-sk-hynix/)). 2027 HBM4 supply talks began in 2Q26 ([TrendForce report summary](https://www.trendforce.com/research/download/RP260527UC)).
- **SOCAMM/LPDDR in servers.** TrendForce lists SOCAMM (LPDDR-based server modules) as a driver of 2027 DRAM demand ([TrendForce 2026-07-30](https://www.trendforce.com/presscenter/news/20260730-13158.html)). Server LPDDR competes directly with phones for LPDDR5X, which is part of why mobile LTAs reached about $21/GB.
- **DDR4 end-of-life:**
  - Samsung (original plan): last orders Jun 2025, final shipments mid-Dec 2025. SK hynix: orders end Oct 2025, final shipments Apr 2026. Micron: final shipments about 1Q26 ([TrendForce News 2025-07-09](https://www.trendforce.com/news/2025/07/09/news-ddr4-exit-timeline-unfolds-for-top-memory-makers-plans-for-samsung-sk-hynix-and-micron)).
  - Micron *did* issue DDR4/LPDDR4 EOL notices in **Jun 2025**. **Samsung and SK hynix extended DDR4 production through 2026** because of the price windfall ([TrendForce News 2025-09-02](https://www.trendforce.com/news/2025/09/02/news-samsung-sk-hynix-reportedly-delay-phase-out-to-2026-as-ddr4-becomes-unexpected-cash-cow/)).
  - Industrial buyers are told supply lasts to about end-2026 and to avoid Samsung DDR4 in new designs ([Advantech](https://www.advantech.com/en/resources/news/response-measures-to-samsung-ddr4-ic-eol-announcement)).
  - **Effect:** DDR4 became the tightest product, inverting against DDR5 in 2025 and again in 2026 (§2.4). Nanya and Winbond reaped inventory windfalls ([TrendForce News](https://www.trendforce.com/news/2025/06/24/news-historic-ddr4-spot-price-rally-reportedly-doubles-ddr5-propelling-nanya-techs-inventory-windfall/)).
  - Status of the 2026 extensions as of Nov 2026: **not verified**.

---

## 7. Cycle history, the turn, and the "DDR5 −60%" glut test

### 7.1 Historical downturns

| Cycle | Peak → trough | Duration | Contract-price decline | Inventory | Maker losses | Sources |
|---|---|---|---|---|---|---|
| **2018–19** | Peak 1H/3Q18 (after 9 straight quarters of increases) → trough mid/late 2019 | ~4–5 quarters | 8GB PC module $68 (3Q18) → $25.50 (Aug 2019), **−62.5%**. 1Q19 alone about −30% QoQ. 8Gb spot $6.95 (Nov 2018) → **<$3** (Jun 2019) | not captured | Makers stayed profitable but margins compressed | [TrendForce 2018](https://press.trendforce.com/node/view/3173.html); [DigiTimes](https://www.digitimes.com/tag/8gb/0034884.html); [KitGuru](https://www.kitguru.net/?p=406046); [Evertiq](https://evertiq.com/design/45079) (via snippet) |
| **2022–23** | Peak ~3Q21/1H22 → trough 3Q23 | ~6–8 quarters | DRAM revenue −~30% QoQ in 3Q22; ASP −20% in 1Q23 and −10–15% in 2Q23. DDR4 8Gb fixed price bottomed at **$1.30 (Sep 2023)** from roughly $3.4–3.9 at the 2021 peak [peak UNVERIFIED], **about −60–65%** | PC-OEM DRAM inventory 9–13 weeks entering 1Q23 (mobile 5–7); channel about 13 weeks | SK hynix 1Q23 op loss KRW 3.4T (~$2.5B); Samsung memory revenue −56% YoY in 1Q23; utilization cut to 74–82% in 2Q23 | [I-Connect007](https://www.iconnect007.com/article/134149/due-to-falling-shipments-and-prices-global-dram-revenue-for-3q22-showed-qoq-drop-of-almost-30/134152/ein); [The Register](https://www.theregister.com/2023/03/29/dram_prices_crash/); [KED Global](https://www.kedglobal.com/korean-chipmakers/newsView/ked202310040013); [TrendForce 2023-01-09](https://www.trendforce.com/presscenter/news/20230109-11533.html); [The Register](https://www.theregister.com/2023/04/27/samsung_sk_hynix_losses/) |
| Current upcycle, for scale | Trough 1Q–2Q25 → ? | 6+ quarters so far | +4× contract (4Q25→4Q26) | Inventories averaged 3.3 weeks at end-3Q25, matching 2018 lows ([TrendForce News 2025-09-30](https://www.trendforce.com/news/2025/09/30/news-record-low-memory-stock-could-signal-supercycle-ahead-likely-peaking-by-2027/)) | Record margins (§5) | — |

### 7.2 When does this upcycle turn? Analyst views (snippets)

- **Through 2028 (bull case):**
  - Micron: tight through 2028, with "no line of sight" to rebalancing.
  - SK hynix leadership: 2027 will be the worst shortage year ([tbreak](https://tbreak.com/memory-chip-crunch-gets-worse-sk-hynix-boss/)).
  - UBS: undersupply to at least 2Q28.
  - Barclays: deficit of 13.9% in 4Q27, shortage into 2028.
  - Blocks & Files (BISI): to at least 2028 ([Blocks & Files](https://blocksandfiles.com/2026/01/21/the-memory-supercycle/)).
- **Peak 2027, new supply early 2028:** Nomura; Morningstar (peak about early 2028); TrendForce in 2025 said "likely peaking by 2027".
- **Soft landing 2028:** BofA sees DRAM ASP about −10% in 2028 against 2027, with renewed growth in 2029–30.
- **Bear case:** Bloomberg Intelligence (Shuli Ren) argues the shortage peaked in 2Q26, the market balances about 4Q27, and oversupply is possible in 2028. Summaries of these views: [KuCoin](https://www.kucoin.com/blog/2027-memory-chip-boom-sk-hynix-samsung); [Stocktwits](https://stocktwits.com/news-articles/markets/equity/micron-s-blowout-q4-pushes-memory-peak-further-out-but-investors-still-see-a-cycle-risk/cZDiCnCRBiW).
- **Leading indicators already flashing:**
  - The QoQ rate is down from +95% to +12.5%.
  - NAND contract was reportedly flat in Oct 2026, and TrendForce forecasts NAND surplus in 2H27.
  - Retail kits "stabilized" because buyers gave up ([TechRadar](https://www.techradar.com/pro/good-news-ram-prices-seem-to-have-finally-stabilized-bad-news-its-probably-because-memory-prices-are-so-high-that-its-forcing-most-of-us-to-give-up-buying-anything)).
  - CXMT capital is flooding in.
  - Capex is exploding (Samsung KRW 84T in 2026).

**My call [ESTIMATE].** Contract prices peak between 4Q26 and 2Q27. They plateau through 2027 because LTAs and HBM crowding hold the floor. They turn down in 2028 as Baird's >30% bit growth, CXMT's capacity and the Korean and U.S. greenfields arrive together. A real glut, meaning prices below cash cost for second-tier makers, is a 2H28–2029 event *if* AI capex slows. If AI capex keeps compounding, 2028 is a soft landing (BofA).

### 7.3 Is "DDR5 falls 60% in 2028–29" plausible?

**Yes. It is close to the historical median for a full downturn.** It is *not* a worst case relative to how far prices have risen.

- **Analogs.** 2018–19: −62.5% (modules, about 4 quarters). 2022–23: about −60–65% (DDR4 8Gb fixed, about 8 quarters, peak level unverified). 2008 and 2011–12 are similar from training-memory recall [UNVERIFIED]: about −60–80%.
- **Where −60% lands [ESTIMATE].**
  - Contract index: 601 → **240** (3Q25 = 100), still **2.4× the pre-spike level**.
  - DDR5 16Gb spot: $57 → **$22.8/chip ≈ $11.4/GB**, still 3.3× the Sep-2025 spot of $6.84.
  - 64GB RDIMM: Citi's $1,586 (4Q26F) → about **$634 ≈ $9.9/GB**.
  - Getting back to 3Q25 prices would take an **83% fall**, which has happened for spot chips in past busts but is rare for contract.
- **Severe case [ESTIMATE].** A return to cost-floor pricing at about $2–4/GB for DDR5 (the 2023 and early-2025 level) is an 80–90% fall from the 2026 peak. It requires a demand air-pocket (AI capex pause) on top of 2028 capacity, and it is plausible for 2029.
- **What a glut looks like.**
  - Customer inventory weeks climb from 3 to 9–13 (the 2023 pattern).
  - Spot falls below contract.
  - LTAs get renegotiated.
  - Second-tier makers (Nanya, Winbond, CXMT) go negative on operating margin first.
  - Makers cut utilization to 75–80%.
  - DDR4 collapses first and hardest as the EOL premium unwinds and CXMT backfills.
  - NAND leads DRAM by 2–4 quarters.
- **Implication for concept screening:** run every concept at **DDR5 = $10–12/GB (the −60% case)** *and* **$3/GB (the severe case)**. A concept that needs more than about $10/GB DDR5 to compete dies in 2028–29.

---

## 8. Downstream effects

- **Retail modules (US):**
  - 32GB DDR5-6000 kits: about **$409** best price on 2026-09-14 (from $375 on 2026-06-03) and **$450–470** on Amazon on 2026-09-25, against **$100–200 in Oct 2025** (search summary citing Tom's Hardware's price index; underlying page not identified [REPORTED]). Kits are widely reported at about $450 ([Digital Citizen](https://www.digitalcitizen.life/ddr5-ram-prices-surge-in-2026-as-32gb-kits-reach-450-amid-global-memory-shortage/)).
  - Premium kits list at more than 10× their 2025 price, such as £1,199 for 32GB ([Club386](https://www.club386.com/g-skill-ddr5-ram-kits-10x-price/)).
  - Typical DDR5 sold for **$18.04/GB** on Amazon US in Sep 2026, +6% MoM ([rampricesusa](https://rampricesusa.com/insights/monthly/2026-09)). 32GB DDR4-3200: about $190 (Sep 2026).
  - **Retail $/GB ($13–18) is below DDR5 chip spot ($27–28).** The channel is still working through inventory bought at lower cost, so further retail increases are likely while contract prices keep rising.
- **Server:**
  - 64GB RDIMM contract went from $450 to more than $900 between 4Q25 and 1Q26 (Counterpoint). Street price is about $2,064.
  - A 4TB DDR5-6400 RDIMM configuration costs about €66,000 at retail ([Igor'sLAB](https://www.igorslab.de/en/memory-crisis-4-tb-ddr5-6400-rdimm-costs-around-66-000-euro/)).
  - From 3Q26, TrendForce expects server DRAM increases to fall mainly on **customers without LTAs**. Hyperscalers are locked in, and tier-2 clouds and enterprises pay the marginal price.
- **Smartphones/PCs:**
  - Samsung's DX division (phones and appliances) saw losses *widen* on component costs in 3Q26 ([Samsung](https://news.samsungsemiconductor.com/global/samsung-electronics-announces-third-quarter-2026-results/); [SBS](https://news.sbs.co.kr/english/endPagePrintPopup.do?news_id=N1008818605)).
  - TrendForce's 4Q26 release flags persistent "consumer-side pressure", and phone makers are burning inventory.
  - LPDDR5X increases are blamed for 2026 smartphone price rises ([Wccftech](https://wccftech.com/you-can-blame-lpddr5x-for-smartphone-price-increases-in-2026/amp/)).
  - Specific OEM list-price announcements (Dell, HP, Lenovo, Apple, Xiaomi) were **not captured** before the search budget ran out.
- **Allocation and lead times:**
  - SK hynix supply is booked to 2029 under 14 LTAs. Mobile LTAs run up to about $21/GB.
  - CSPs are locking multi-year supply ([TechNews 2026-03-31](https://technews.tw/2026/03/31/ai-server-demand-drives-2q26-memory-contract-price-increase-csps-lock-supply-long-term-deals/)).
  - Nanya's long-term agreements expired at end-June 2026 and repriced more than 60% higher in July.
- **Industrial/automotive legacy DRAM:**
  - Advantech DDR4 EOL guidance: supply to about end-2026, avoid Samsung DDR4 in new designs.
  - DDR4 up more than 50% in 3Q26, and DDR3 rising.
  - Specific automotive line-stoppage reports were **not captured** [gap].

---

## 9. Mobius Materials (mission §3D)

**Who they are [REPORTED]:**
- A Richmond, Virginia startup (PitchBook), founded 2020 by CEO **Margaret Upshur** and backed by Y Combinator. It calls itself "the spot market for semiconductors" ([YC](https://www.ycombinator.com/companies/mobius-materials)).
- It runs an **authenticated B2B secondary marketplace** where OEMs and contract manufacturers buy and sell certified excess and surplus electronic components. It has filed a patent on ML-based component authentication and claims "hundreds of OEMs and CMs" as users.
- **Funding:**
  - **$3M seed, Dec 2025**, led by Spero Ventures with Outsiders Fund and RefashionD ([PR Newswire](https://www.prnewswire.com/news-releases/mobius-materials-raises-3m-to-combat-one-of-manufacturings-biggest-issues-amid-us-china-trade-tariffs-302643403.html); [Digital Commerce 360](https://www.digitalcommerce360.com/2025/12/16/b2b-marketplace-mobius-materials-3-million-funding/); [PitchBook](https://pitchbook.com/profiles/company/442509-13)).
  - An earlier **$735K pre-seed extension** led by Undeterred Capital ([CityBiz](https://www.citybiz.co/?p=417805)).
- It is **not** a materials or wafer company, despite the name.

**What they publish:**
- **Blog posts:** "The first semiconductor memory supercycle in seven years" (2026-04-02) and "Inside the memory supercycle: second act" (2026). They cite DDR4 8Gb spot up about 20× in a year, HBM at about 4× wafer per GB, and DDR4 8Gb at $42.08 on 2026-07-28 (from $33.02 in early March), with quotes ranging $20.20–74.00 ([post 1](https://www.mobiusmaterials.com/post/the-first-semiconductor-memory-supercycle-in-seven-years); [post 2](https://www.mobiusmaterials.com/post/inside-the-memory-supercycle-second-act)).
- **A "DRAM Market Report" whitepaper** at `/whitepapers/dram-market-report-2026` ([link](https://www.mobiusmaterials.com/whitepapers/dram-market-report-2026)). I could not open it.

**Pricing:** I found none. A /whitepapers/ path on a marketplace site points to a **free, probably email-gated lead magnet**, not a subscription product [UNVERIFIED; assumption logged].

**Implication for §3D "DRAM price intelligence as a paid data product":**
- Mobius uses DRAM market content to drive **marketplace liquidity**. It does not sell the data.
- The paid tier is held by TrendForce/DRAMeXchange (daily spot and contract), inSpectrum (monthly contract data that the sell side cites ([Benzinga](https://benzinga.com/z/25312547))), TechInsights (monthly Memory Pricing Report and quarterly DRAM Market Report ([TechInsights](https://www.techinsights.com/blog/slides-dram-market-report-q2-2026))), Omdia and Counterpoint.
- The free tier is crowded with retail trackers: rampricesusa, capitalandcompute.net, siliconanalysts.com, Tom's Hardware's index, Servnet's server tracker.
- A standalone data product for this founder would sit between entrenched paid incumbents and free trackers. **Mobius's model, where data serves as a funnel into transactions, is the more defensible pattern.**
- Mobius is also a **direct comparable and potential competitor or partner** for any §3C "recertified or recovered DRAM brokerage" concept. It is East Coast-based like the founder.

---

## 10. What this means for American Memory

1. **Premise status: stronger than written on price and margin, and riskier on timing.** Re-aim every concept's economics around two price decks:
   - **Shortage deck (2026–27):** DDR5 contract about $14–25/GB.
   - **Glut deck (2028–29):** DDR5 about $10/GB (the −60% case) down to about $3/GB (the severe case).
2. **Legacy DDR4/DDR3 is the tightest and most inverted segment,** with industrial and automotive buyers facing EOL. It is also the segment most exposed to CXMT backfill and to the end of Samsung's and SK hynix's DDR4 extensions. Concepts serving long-lifecycle buyers need a *supply-security* value proposition that survives the price falling, not just a price arbitrage.
3. **Arbitrage concepts** (recovered or recertified DRAM, brokerage, module assembly) have a 12–24-month high-price window. They must be cash-positive before 2028.
4. **HBM's crowding-out is the durable structural force.** Wafers per bit are rising and HBM's wafer share heads to about 30%. Watch whether AI capex holds through 2027. That, more than new fabs, decides whether 2028 is a soft landing or a crash.
5. **NAND is the canary.** TrendForce already forecasts NAND surplus and price pressure in 2H27, and Oct 2026 NAND contract prices were reportedly flat. Track the TrendForce NAND monthly release as an early warning for DRAM.

---

## 11. Gaps and items to verify (search budget exhausted, primary pages unreachable)

- Primary TrendForce press-release text for 2026-02-02, 2026-02-26, 2026-03-31, 2026-06-01, 2026-07-30 and 2026-09-30. All were used via snippets.
- Whether TrendForce issued an October 2026 revision to "~+20%". **Unconfirmed.**
- Retrospective 2Q26 and 3Q26 conventional DRAM contract changes (only forecasts captured), and 3Q25 and 3Q26 NAND changes.
- Chip-level **contract** prices for DDR5 16Gb, DDR4 8Gb (2026) and LPDDR5X in $/Gb, from TrendForce or inSpectrum.
- NAND wafer price *levels* (512Gb/1Tb TLC) for 2026.
- Micron FQ3-26 full results and FQ4-26 GAAP operating income. SK hynix 1Q26 exact figures. Samsung 2Q26 DS.
- Status of Samsung's and SK hynix's DDR4 production after the 2026 extension.
- Nanya and Winbond capacity plans. Exact CXMT DDR5 share.
- OEM list-price increases (Dell, HP, Lenovo, Apple, Xiaomi) and automotive or industrial line stoppages from DRAM shortage.
- The 2021 DDR4 8Gb contract peak, needed to pin the 2022–23 peak-to-trough decline exactly.
- Mobius Materials report contents and whether it is gated or priced.
