# DD2 — Memory Lifecycle & Cost Intelligence for OEMs: research notes

Agent: `p4-lifecycle-intel` · As of 2026-11-01 · Anchor **C-80**; folded **C-29, C-86, C-61 (software only), C-72 (feature only)**.
Model: `models/lifecycle-intel.py` (exit 0); output: `research/phase4/lifecycle-intel_model_output.md`.
Sources: `research/sources/p4-lifecycle-intel.jsonl` (68 entries). Assumptions: `research/assumptions/p4-lifecycle-intel.md`.
Method note: 30 WebSearch calls (the full quota). Both WebFetch attempts failed DNS (accuristech.com, siliconexpert.com). **Every web fact below is snippet-grade, [REPORTED] at best**; nothing is [VERIFIED].

---

## 0. Verdict in one paragraph

**This is mostly a feature, with one non-feature part, and it caps at lifestyle scale unless the index becomes a reference.**

- **The lifecycle half is a feature.** EOL alerts, PCN feeds, pin-to-pin alternates and years-to-EOL forecasts already sell at $250/month. SiliconExpert's BOM Manager Essentials costs that much ([SiliconExpert](https://www.siliconexpert.com/products/bom-manager/), via snippet). Octopart gives lifecycle flags away free ([Octopart](https://octopart.com/pulse/p/reducing-costs-efficient-bom-management)). Z2Data, Accuris and Luminovo bundle the same capability.
- **The buy/hold half is a one-window feature.** Supplyframe Commodity IQ and Counterpoint already sell memory price forecasts, so these alerts are worth paying for only during the 2027 shortage window.
- **The non-feature part is the Memory Cost Escalation Index (C-86).** It would be built on a panel of OEMs' contributed memory PO prices, collected through the SaaS. It is two-sided, so it earns more in a glut. No memory escalation index product was found. BLS publishes no DRAM PPI. The index has to displace TrendForce's DXI and contract data as the default reference.
- **Base-case economics are a good side business, not a venture.** The modelled business:
  - pays the founder's first $10k/month at **m23 (2028-10)**;
  - reaches **$126k ARR at m18** and **$422k ARR at m36** in BASE ($334k in GLUT, $282k in SEVERE);
  - never drops below **$22k cash** (m10).
- **$1M ARR by m36 is a stretch.** It needs **2.3×** the modelled trial inflow and ~225 accounts (≈3.7% of an estimated 6,000 U.S. SMB OEMs). **$2M needs 4.7×** and ~470 accounts.
- **Recommendation: FALLBACK-grade, not PRIMARY.** Run it index-first, with the SaaS as the data-collection funnel. Kill it on the 30-day test in §9.

---

## 1. Q1 — Competitors and what they charge (dated, snippet-grade)

| Vendor (owner) | What it covers for memory | Price evidence | Tag |
|---|---|---|---|
| **SiliconExpert** (Arrow) | Parts search, **pin-to-pin alternates, lifecycle status, PCN alerts**, BOM risk | **BOM Manager Essentials $250/mo, cancel any time; 1 user, 1 BOM ≤500 parts** ([product page](https://www.siliconexpert.com/products/bom-manager/); [BOM Manager](https://www.siliconexpert.com/bom-manager/)). Professional (≤5,000 parts) and Enterprise are annual, quoted on request ([KI-Syndikat](https://www.ki-syndikat.de/tools/siliconexpert/), secondary). Inside Altium 365 it is priced by annual part queries ([Altium](https://www.altium.com/altium-365/supply-chain/siliconexpert)) | [REPORTED] 2026 |
| **Accuris** (ex-IHS Markit parts business) | Parts Intelligence: lifecycle, validated data, alternates; BOM Intelligence Starter/Pro/Elite (also called BOM Starter/Pro/Enterprise; **BOM Pro available from Oct-2026**) | **Minimum $6,000 ACV** for its price-match offer; **20% below the customer's current SiliconExpert ACV**, first year only ([Accuris offer terms](https://accuristech.com/siliconexpert-offer-terms/); [price match](https://accuristech.com/accuris-price-match-offer-terms/)) | [REPORTED] 2026 |
| **Z2Data** (Santa Clara; 201–500 staff) | Part risk, lifecycle, supplier risk; Gartner 2026 MQ for supplier risk management | **Starter (≤50K tracked components) and Enterprise are both listed as "custom per month"**: usage-based, no multi-year contract, 14-day trial ([Z2Data](https://www.z2data.com/pricing); [Capterra](https://www.capterra.co.uk/software/1014387/supply-chain-watch)) | [REPORTED] 2026 |
| **Lytica** (Ottawa, founded 2005) | SupplyLens spend analytics on **real customer transaction prices, not distributor list prices**; Negotiator/Validator/Mitigator/Trends modules; more OEM than EMS customers | Annual subscription, price unpublished ([Preqin](https://www.preqin.com/data/profile/asset/lytica-inc-/441739); [CENGN](https://www.cengn.ca/wp-content/uploads/2020/06/Lytica-Success-Story.pdf); [DigiTimes 2021-03-26](https://DigiTimes.com/news/a20210326PD213.html?chid=9)). EMS partner: NEOTech ([PR](https://www.webull.com/news/15265411318440960)) | [REPORTED] |
| **Supplyframe Commodity IQ** (Siemens) | Rolling four-quarter **DRAM/SRAM/specialty-memory price and lead-time forecasts** | Unpublished ([G2](https://g2.com/products/supplyframe-commodity-iq/pricing)); coverage per the [CIQ commodities page](https://intelligence.supplyframe.com/commodities-analyzed-sram-dram-specialty) | [REPORTED] |
| **Octopart / Nexar** (Altium → Renesas) | **Free BOM Tool** with Active/NRND/EOL flags; GraphQL API | BOM Tool free ([Octopart](https://octopart.com/pulse/p/reducing-costs-efficient-bom-management)). An Altium comparison says "30-day trial then $1,990/yr (Altium Develop)" ([Altium](https://www.altium.com/capabilities/upgrade-to-bom-portal); ambiguous). API tiers are in §2 | [REPORTED] |
| **Luminovo** (Munich) | EMS quoting and sourcing; **BOM alerts with years-to-EOL predictions**; publishes a free *2026 EMS memory chip risk matrix* | Starter/Advanced/Professional/Enterprise tiers, priced by procurement spend or assemblies per year; no list price ([FAQ](https://luminovo.com/faq/how-much-does-luminovo-cost); [features](https://luminovo.com/product/features); [guide](https://luminovo.com/guides/2026-ems-memory-chip-risk-matrix)) | [REPORTED] 2026 |
| **TrendForce / DRAMeXchange** | Spot (daily) and contract (monthly) DRAM/NAND prices; public **DXI**, a production-value-weighted spot index | **Silver $5,000/yr; Gold $11,000 (adds contract + spot downloads); DRAM Platinum $18,000; DRAM&NAND Platinum $30,000; DRAM Diamond $30,000; DRAM&NAND Diamond $55,000**, VAT extra ([GII](https://giikorea.co.kr/annual/tdf225654-dramexchange-membership.html); [GII](https://www.giiresearch.com/annual/tdf914490-dramexchange-market-intelligence-service-by.html); [2020 kit](https://img.trendforce.com/Package/2020/01/20200117_164702_DRAMeXchange%20Membership%20Introduction%20Kit_2020%20%28Silver%2B%29.pdf); [DXI FAQ](https://dramexchange.com/Service/Faqs)) | [REPORTED]; reseller list, kit dated 2020 |
| Counterpoint Memory Price Tracker; inSpectrum; TechInsights Memory Pricing Report | Monthly trackers and forecasts | Not found (gap). Phase 2 assumed $5k–50k+/yr [UNVERIFIED] | — |
| **Mobius Materials** (Richmond VA) | Free memory-market posts and a gated DRAM report, used as **lead-gen for its marketplace** | Free ([Mobius 2026](https://www.mobiusmaterials.com/post/inside-the-memory-supercycle-second-act)) | [REPORTED] |
| **AVCOM** (BAE Systems) | Web DMSMS tool suite "for organizations small to large" | Unpublished ([BAE](https://www.baesystems.com/en/product/avcom-products)). Government-owned alternative: **MORE** (AMRDEC; chosen by NAVAIR) ([Army](https://www.army.mil/article/192061/database_tool_improves_dod_obsolescence)). QTEC and PartsPlus: no results | [REPORTED] |
| Sourcengine; Cofactr | Marketplace and BOM sourcing | Not searched (quota) | gap |

**What SMB OEMs actually use [ESTIMATE from the above].** Most use the free Octopart BOM Tool, distributor BOM managers, spreadsheets and their EMS partner's procurement desk. Paying teams use SiliconExpert Essentials ($3k/yr) or an Accuris/Z2Data quote of ≥$6k/yr. Lytica's own history says OEMs buy before EMS. **Implication: $250/month is the price ceiling for a lifecycle tool sold to a small team, and a memory-only tool must price at or below it** (the model uses Team at $249).

---

## 2. Q2 — Data access and licensing constraints

- **Nexar/Octopart API.**
  - **Tiers:** Evaluation (≤100 matched parts), **Standard (≤2,000)**, **Pro (≤15,000, "recommended")**, Enterprise custom. Paid prices are not shown ([Nexar compare-plans](https://nexar.com/compare-plans)).
  - **Free allowance:** support documents describe a free 1,000 parts/month default. Supply queries count each part returned; design queries are free; limits reset monthly with no rollover ([Nexar glossary](https://support.nexar.com/support/solutions/articles/101000472520-the-nexar-glossary)).
  - **Binding terms ([Octopart API legal](https://octopart.com/api/legal), via snippet):**
    1. Firms in component distribution, "including software developers building applications for that market", **may not use the API for pricing and availability**.
    2. **Use for historical pricing and inventory trends is prohibited.**
    3. **Caching beyond 24 h is prohibited.**
  - **Display:** content may be shown through the licensee's own applications ([Nexar legal](https://nexar.com/api/legal)).
  - **Consequence:** Nexar data can feed live in-app lifecycle and stock views, but **it cannot be the raw material of a price index or historical charts.** A written answer from support@nexar.com is kill-test item K5.
- **DigiKey API.** Product Information: **120 requests/min and 1,000/day**. Keyword-search data may be up to 24 h stale. Price depends on locale and customer ID ([DigiKey developer](https://developer.digikey.com/documentation)). Redistribution and display terms were **not found** (gap).
- **Mouser API:** not checked (gap).
- **PCN/PDN feeds.**
  - **Standard:** **J-STD-048A** (product discontinuance, published Dec-2025, superseding JESD48) ([DIN Media](https://www.dinmedia.de/en/standard/ipc-j-std-048a/399577878)).
  - **Vendor practice:** a **6-month last-time-buy order window**, with last shipment at 12–18 months ([MaxLinear](https://www.maxlinear.com/support/quality/policy-and-procedure); [Boréas](https://boreas.ca/pages/product-life-cycle-policy)).
  - **Where the documents live:** PDN/PCN PDFs sit on distributor media servers, for example NXP PDN 202504001DN on [mm.digikey.com](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/6778/PDN-202504001DN.pdf). That gives a crawlable, attributable EOL source with no licence.
  - **Value:** the 6-month window is the reason an LTB sizer is valuable.
- **Spot and contract price data.** DXI and the daily spot notes are public on DRAMeXchange ([Daily Express 2026-06-16](https://www.dramexchange.com/WeeklyResearch/Post/3/12738.html): DDR4 8G 3200 spot $35.80). Contract data costs ≥$11k/yr (Gold), and **redistribution is not part of any listed tier** (Phase 2 cards; [UNVERIFIED] on exact terms).
- **Index data design (the answer to the licensing problem).** Build the index from a **panel of anonymised memory PO prices contributed by subscribers**, the Lytica pattern of "real customer pricing, not published distributor pricing" ([CENGN](https://www.cengn.ca/wp-content/uploads/2020/06/Lytica-Success-Story.pdf)).
  - **Cross-checks:** distributor quotes sampled with written permission, and the free DXI as a sanity check. The DRAMeXchange Silver subscription ($5k/yr) is used internally for validation only and is never redistributed.
  - **Antitrust hygiene:** aggregated, lagged data with ≥5 contributors per cell. U.S. agencies withdrew the 1996 information-exchange safety zones in 2023 [UNVERIFIED-training], so this needs counsel; the model budgets $7k of legal at m8.

## 3. Q3 — Willingness to pay and procurement pain (2026)

- **Price points actually charged for lifecycle and BOM risk:**
  - SiliconExpert **$250/mo** entry; Accuris **≥$6,000 ACV**.
  - Z2Data usage-based "custom per month"; DRAMeXchange **$5k–55k/yr**.
  - These are the anchors. No SMB-specific deal sizes were found beyond them (gap).
- **Allocation and lead-time pain (buyer side):**
  - **Lead times:** Avnet reports **25–45+ weeks against an 8–12-week norm**. DDR4/LPDDR4 allocation is "often quarterly", **favoring purchase history, early orders and pricing flexibility** ([Avnet 2026](https://www.avnet.com/integrated/resources/article/memory-is-breaking-product-plans/)).
  - **Squeeze on small buyers:** Luminovo cites **80–90% price spikes** and **>58-week** automotive memory lead times, and says firms without cash to stockpile are squeezed out of allocation ([Luminovo](https://luminovo.com/resources/blog/memory-chip-shortage)).
- **Medtech:** AdvaMed (2026-08-17) says **75–80% of medtech products contain memory**. In its survey, **75% of members reported memory constraints, 88% price increases and 63% allocation problems or scarce components** ([AdvaMed](https://www.advamed.org/2026/08/17/memory-chip-shortages-implications-for-medtech-innovation-and-patient-care/)). PwC (2026-06) calls this a structural risk, says legacy phase-outs mean costly redesigns, and notes past shortages resolved in ~5–11 quarters ([PwC](https://www.pwc.com/us/en/industries/health-industries/library/medtech-semiconductor-memory-shortage.html)).
- **Organized buyer coalitions:**
  - **CGP letter to GSA** (Mar-2026): asks for **weekly Economic Price Adjustments** by temporary deviation and cites a late-1990s precedent ([CGP letter](https://thecgp.org/images/2026/03/Letter-to-Larry-Hale-on-Memory-Chips.pdf)). CGP projects "triple-digit" increases for conventional memory ([CGP](https://thecgp.org/?p=40523)).
  - **Cross-sector coalition** (NCTA, TIA and others, Jun-2026) letter to Commerce and Treasury ([NCTA](https://www.ncta.com/wp-content/uploads/2026/06/Industry-Coalition-Letter-re-Memory-Shortage.pdf)).
- **OEMs already split out memory surcharges (the index's natural use).**
  - **Revolution Pi** (KUNBUS): device price plus a RAM surcharge plus an **eMMC surcharge from 2026-07-10**, passed through at cost ([notice](https://revolutionpi.com/fileadmin/downloads/Informationsschreiben/eMMC_surcharge_07-26-en.pdf)).
  - **Unipi:** a two-part quote from 2026-07-20 with a memory/storage surcharge at cost, **"reduced once memory prices normalize"** ([Unipi](https://www.unipi.technology/ram-surcharge); [price list](https://www.unipi.technology/news/price-list-update-571)). That is a two-sided EPA with no named reference index.
  - **Advantech:** reports margin squeeze from DDR4 tightness ([DigiTimes 2025-12-17](https://www.digitimes.com/news/a20251217PD223.html)). No U.S. OEM surcharge notice was found (gap; OnLogic and Crystal Group did not surface).
- **Defense DMSMS:** tools exist (AVCOM, government-owned MORE), and academic forecasting work is active. Examples are an NPS 2025-12 regression model on 1,821 observations ([NPS](https://dair.nps.edu/handle/123456789/5619)) and UMD CALCE's lifetime-buy optimization course ([CALCE](https://calce.umd.edu/event/20069/electronic-part-obsolescence-forecasting-mitigation-and-management)). **No 2025–26 SBIR topic for DMSMS forecasting was found** (gap).
- **Value per customer [ESTIMATE].** An OEM shipping 10k units/yr with 8 GB of DDR4 each buys ~80k GB/yr: ~$1.6M at the $20.37/GB contract deck, ~$0.65M at the $8.15 glut line.
  - **A $4k/yr tool** is <1% of that.
  - **One avoided spot buy** at the 1.69× spot/contract premium (E notes) on $100k of memory saves ~$69k.
  - **The problem is not ROI; it is substitution.** SiliconExpert, Octopart and the EMS desk already answer most of the lifecycle question.

## 4. Q4 — Escalation index: legal hooks, precedent, existing indices, buyers, pricing

- **Federal hooks (Phase 2, opened by branch E).**
  - FAR 16.203-1(a)(3) allows EPA on "cost indexes of labor or material … specifically identified in the contract", and **FAR 52.216-4** is the standard clause.
  - **DLAD 16.203-4** tells contracting officers to choose the most appropriate **BLS** index first and to document why BLS indices are unsuitable before using another. PGI 216.203-4 urges simple clauses with trigger bands (concept cards C-86 and E-02).
  - **GSAM 552.238-120** (MAS EPA clause; the version effective 2026-01-15) governs schedule price increases ([acquisition.gov](https://www.acquisition.gov/gsam/552.238-120)). GSA has added temporary flexibility, but increases face caps and backlog ([Centre Law](https://centrelawgroup.com/blog/gsa-flexibility-price-increases)).
  - Whether a MAS EPA can be tied to a third-party market index is **[UNVERIFIED]** (gap).
- **BLS gap:** BLS has no DRAM-specific PPI; FRED surfaced only PCU334413334413 (C-86 card). A product-level search this session found nothing either.
- **Licensed-index precedent:**
  - Fastmarkets prices are used "as price references … in physical spot and future contracts, as well as the settlement price of financial derivatives", and are licensed to CME/COMEX ([Fastmarkets](https://www.fastmarkets.com/products/price-data-how-to-use-it/); [CME disclaimers](https://www.cmegroup.com/rulebook/NYMEX/1/nymex-comex-disclaimers.pdf)).
  - A government list approves **Platts, Argus and ICIS** indicators for **public procurement contracts** ([Gov. of Ukraine](https://www.kmu.gov.ua/en/news/uriad-vyznachyv-perelik-mizhnarodnykh-tsinovykh-ahentstv-pokaznyky-iakykh-mozhna-zastosovuvaty-v-dohovorakh-pro-publichni-zakupivli)).
  - No PRA licence-fee schedule was published (gap).
- **Does a DRAM index exist?** **Yes, DXI**, but it is a production-value-weighted spot index ([DRAMeXchange FAQ](https://dramexchange.com/Service/Faqs)), not a contract-settlement or BOM-cost index, and no contract-licensing programme for it was found.
  - **No memory escalation index or EPA clause kit was found** (one targeted search, 2026-11-01).
  - The closest substitutes are an undefined "reasonable increase" or a vendor's own surcharge (Unipi, Revolution Pi).
- **Who would license it:**
  1. OEMs that issue memory surcharges and need a neutral reference their customers will accept (Unipi/Revolution Pi pattern).
  2. EMS houses repricing turnkey builds.
  3. Commercial system integrators on multi-year fixed-price deals.
  4. Federal IT contractors (CGP members), case by case under the DLAD justification.
- **Pricing:** $6k standard and $24k enterprise (redistribution/API), against DRAMeXchange Gold at $11k and Platinum at $18–30k (model inputs).
- **Glut logic:** a −60% move is a refund event for buyers, so licence demand **rises** in GLUT. The model shows index revenue **+31% (GLUT) and +34% (SEVERE)** against BASE at m36.

## 5. Q5 — First ten customers (names or precise types, and where to find them)

| # | Candidate | Why | Where to find / evidence |
|---|---|---|---|
| 1 | The founder's own employer (design/manufacturing company) | Buyer persona; design partner #1, if conflict-free | Written OK from the employer first |
| 2 | **OnLogic / Logic Supply** (South Burlington, VT) | East Coast industrial PCs; DDR4/eMMC-heavy BOMs | [Thomasnet](https://www.thomasnet.com/articles/top-suppliers/industrial-computer-manufacturers-suppliers/) (Logic Supply). The OnLogic rebrand is [UNVERIFIED-training] |
| 3 | **Amplicon USA** (Fairport, NY) | East Coast industrial computers and panel PCs | [Thomasnet](https://www.thomasnet.com/articles/top-suppliers/industrial-computer-manufacturers-suppliers/) |
| 4 | **Trenton Systems** (U.S.-made rugged servers) | DoD buyer; §5949 and DMSMS exposure; server DRAM | [Trenton list](https://www.trentonsystems.com/blog/list-of-rugged-server-manufacturers) |
| 5 | **CP Tech USA** (formerly Chassis Plans) | DoD/industrial rugged computers | Same list; [CPNA](https://cpnorthamerica.com/?p=67) |
| 6 | **Core Systems USA** | Rugged servers | Same list |
| 7 | **WINSYSTEMS** | Long-lifecycle embedded SBCs (DDR/eMMC/NOR) | [Arm catalog](https://www.arm.com/partners/catalog/winsystemsinc) |
| 8 | **Industrial Computers Inc.** (Ann Arbor, MI) | High-reliability industrial PCs | [Thomasnet](https://www.thomasnet.com/articles/top-suppliers/industrial-computer-manufacturers-suppliers/) |
| 9 | **Mid-size medtech OEMs** (patient monitors, imaging carts, IVD analyzers with embedded PCs), East Coast | AdvaMed: 63% report allocation problems | AdvaMed and MDMA member directories ([AdvaMed](https://www.advamed.org/2026/08/17/memory-chip-shortages-implications-for-medtech-innovation-and-patient-care/)) |
| 10 | **Tier-2/3 U.S. EMS** ($50–500M revenue) for Pro tier plus index-based customer surcharges | Repricing turnkey memory; Lytica already sells into EMS (NEOTech), which proves the budget line | IPC and SMTA chapter member lists |
| 11 | **GSA MAS IT hardware resellers** (CGP members), index licence | Asked GSA for weekly EPAs | [CGP letter](https://thecgp.org/images/2026/03/Letter-to-Larry-Hale-on-Memory-Chips.pdf); GSA eLibrary hardware SIN vendor lists |
| — | Reference licensees outside the U.S.: **Unipi** (CZ), **Revolution Pi/KUNBUS** (DE) | Already publish at-cost memory surcharges with no reference index | [Unipi](https://www.unipi.technology/ram-surcharge); [Revolution Pi](https://revolutionpi.com/fileadmin/downloads/Informationsschreiben/eMMC_surcharge_07-26-en.pdf) |

No customer above has been contacted. Each one is a hypothesis for the kill test.

## 6. Q6 — Glut behaviour: which modules lose value, which gain

| Module | GLUT (DDR5 $8.15/GB) | SEVERE ($2.04/GB) | Mechanism (model §6) |
|---|---|---|---|
| Buy/hold + allocation alerts (C-80 core) | **−57%** revenue vs BASE at m36 | **−86%** | Urgency falls with price, and price-motivated accounts churn up to +8%/month (C-80 audit: worthless in a glut) |
| EOL/lifecycle + NVM cross-reference + LTB sizer (C-80/C-29/C-61) | ±0% | ±0% | EOL-driven. Makers exit legacy lines under margin pressure: in 2023, Nanya/Winbond legacy DDR3/DDR4 fell until Oct-2023 ([DigiTimes 2023-02-22](https://apps.digitimes.com/news/a20230222PD222/dram-nanya.html)), and DDR5 fell *less* than DDR4 mid-2023 ([TrendForce 2023-07-05](https://trendforce.com/presscenter/news/20230705-11743.html)). But budgets tighten too, so it is held flat |
| Memory Cost Escalation Index (C-86) | **+31%** | **+34%** | Two-sided: buyers invoke down-adjustments, and embedded clauses persist. New sales slow only when prices go flat (2029; licence churn rises) |
| LTB studies (C-61 software/service) | −6% | −12% | More EOL notices (+25%/+40%) are offset by a smaller account base |
| Pooled forecast (C-72) | Worthless | Worthless | Allocation is free in a glut, so it is not monetized in the model |
| Consignment vault (C-61 physical) | Fee falls with inventory value | — | Not in scope |

**Overall:** ARR at m36 is $422k (BASE), $334k (GLUT, −21%) and $282k (SEVERE, −33%). The revenue mix shifts from 39% price-driven SaaS (BASE) to 8% (SEVERE), and the index share rises from 14% to 26%. **The bundle survives a glut partially, and only because of the index and lifecycle legs.**

## 7. Q7 — Path to >$1–2M ARR, or evidence it caps out

- **Modelled BASE:** $422k ARR at m36 with 88 accounts and 7.7 licences.
- **What $1M by m36 takes:** SaaS trial inflow **2.3×** the modelled level (~57 qualified trials/month part-time, ~136 full-time). That means ~63 paying accounts by m18 and ~225 by m36, ≈3.7% of an estimated 6,000 U.S. SMB OEMs [ESTIMATE, unsourced]. GLUT at the same funnel gives $748k.
- **What $2M takes:** **4.7×** inflow, ~468 accounts (7.8% penetration). GLUT gives $1.46M.
- **Pure-play equivalents:** 249 SaaS accounts per $1M at $4,020/yr; **115 index licences per $1M** at $8,700/yr.
- **Evidence it caps:**
  1. The $250/mo ceiling set by SiliconExpert's all-parts tier.
  2. Free substitutes: Octopart, distributor tools, EMS desks.
  3. A memory-only scope that is <10% of most BOM line items.
  4. The price-driven half decays after 2027.
  - **Conclusion:** without the index becoming a reference, this is a **$0.3–0.6M ARR business**.
- **Credible paths to $1–2M:**
  - (a) **Make the index the default memory surcharge reference.** Free public headline index, paid licences, enterprise redistribution deals with one EMS network or distributor. 115 licences is a big but bounded ask.
  - (b) **Broaden to an "electronic component cost index family"** (memory, MCUs, passives, power), which becomes a Lytica-lite. It competes with Lytica and SiliconExpert.
  - (c) **Exit as a data feature** to Lytica, Z2Data, Accuris, Supplyframe or Luminovo, at acqui-hire scale.
- **Sensitivity (model §7):**
  - **Price −30%** gives $196k ARR at m36, and the salary is **never covered**.
  - **Conversion −30%** gives $229k, and the salary is **never covered**.
  - **Churn ±30%** moves m36 ARR by only ±$30–40k.
  - **COGS +30%** delays salary coverage by 2 months.
  - **Price and close rate are the whole game.**

## 8. Model headline (`models/lifecycle-intel.py`, run 2026-11-01, exit 0)

- **Unit economics:**
  - SaaS Team $249/mo has 76% contribution margin; Pro $649 has 85%; blended net ARPA $335 has 80%.
  - Index standard licence ($500/mo) has 85%; enterprise ($2,000/mo) has 91%. An LTB study ($3,500) has 67%.
  - **Blended GM including fixed data and infrastructure:** 45% (m12), **65% (m18)**, 71% (m24), **74% (m36)**.
  - **CAC:** $563 cash, or **$1,188** fully loaded with founder time. LTV/CAC is 11.5 and payback is 4.4 months (fully loaded).

| Scenario | Breakeven, founder unpaid | Covers $10k/mo salary | Full-time from | Cash low | ARR m12 | ARR m18 | ARR m24 | ARR m36 |
|---|---|---|---|---|---|---|---|---|
| BASE | m11 (2027-10) | **m23 (2028-10)** | m26 (2029-01) | $21,951 @ m10 | $49k | **$126k** | $193k | **$422k** |
| GLUT | m11 | m23 | m26 | $21,951 @ m10 | $49k | **$130k** | $187k | **$334k** |
| SEVERE | m11 | m24 (2028-11) | m26 | $21,951 @ m10 | $49k | **$127k** | $173k | **$282k** |

- **First revenue:** m5 (2027-04), inside the 18-month target. The $40k is never exhausted.
- **What must be true:** to go full-time by m18 (2028-05), the founder needs **≥52 paying accounts, or ~27 accounts plus 10 index licences**. The model has 27 accounts and 2 licences, so it gets there at m23–26.

## 9. Kill experiment (<$10k, <30 days; November 2026)

**Build (week 1, ~20 founder hours):**
- A "memory exposure scan" that classifies a pasted BOM's memory MPNs (DDR3/4/5, LPDDR, eMMC, NOR, EEPROM). It shows lifecycle/PDN status from DigiKey API data, flags CXMT/YMTC manufacturers for §5949 (2027-12-23), and lists 6-month LTB deadlines.
- A one-page draft **Memory Surcharge Reference**: methodology v0 plus a sample EPA/surcharge clause.

**Outreach (weeks 1–3):**
- 60 targeted contacts from the §5 list (industrial/rugged PC, medtech, test equipment, EMS, CGP-member resellers), aiming for **25 qualified 30-minute calls**.
- **Offer:** a free scan in exchange for the call. Then ask for **(a)** a refundable $500 deposit, or a signed paid LOI, for 6 months of Team at $249/mo; **(b)** whether they would cite the index in a live surcharge or contract within 6 months; **(c)** whether they would contribute 24 months of anonymised memory PO prices.

**Legal and data (weeks 1–4):**
- Written questions to support@nexar.com and DigiKey on in-app price display and historical use.
- A 2-hour consult with a government-contracts attorney on DLAD/GSAM index use and on antitrust hygiene for contributed prices.

**Budget:** Sales Navigator ~$100, attorney ~$1,000, domain/hosting ~$100, interview thank-yous 25 × $50 = $1,250. **≈$2.5k**, plus ~50 founder hours.

**Kill criteria (any one kills the named leg; K1 and K3 together kill the bundle):**

- **K1:** fewer than **5 of 25** SaaS prospects pay a deposit or sign a paid LOI at ≥$200/mo (the model needs ~12% conversion). → Kill the SaaS.
- **K2:** at least 60% say SiliconExpert, Octopart or their EMS already covers it. → Kill lifecycle-as-product and keep it only as a free funnel.
- **K3:** fewer than **2 of 10** index prospects commit to cite it in a live contract or surcharge, or all insist on TrendForce. → Kill the index.
- **K4:** fewer than **5** OEMs agree to contribute PO history. → Kill the index, because it has no data moat.
- **K5:** both Nexar and DigiKey refuse in-app price display. → Drop buy/hold pricing and go lifecycle-only.

Later gates: m12 below 12 accounts or MRR below $4k means stop. At m18, below 35 accounts and below 3 licences means it stays a side business (no full-time switch).

## 10. Go-to-market, roadmap, team, IP, regulation and funding (for the deep dive)

- **GTM:**
  - **Free layer:** a public "Memory Surcharge Reference" headline index plus a monthly memory-shortage note. This is the Mobius lead-gen pattern, and Luminovo uses the same content play.
  - **Paid layer:** a free BOM exposure scan converts to trial, then Team/Pro.
  - **Channels:** association channels (AdvaMed/MDMA, IPC/SMTA chapters, CGP) and §5949 BOM flags for federal-adjacent OEMs.
  - **Index sales:** sold founder-to-procurement-lead, paired with a clause kit.
- **18-month roadmap:**
  - m1–4: MVP, 5 design partners.
  - m5: paid launch.
  - m6–9: LTB sizer, NVM cross-reference (EEPROM/NOR/NVSRAM → F-RAM/MRAM; e.g. Infineon's Excelon-based F-RAM revision delivering from 2026-10-30 per [Future](https://www.futureelectronics.com/es/p/semiconductors--memory--RAM--nvram--fram-mram/fm24c16b-gtr-infineon-technologies-4003630)), §5949 CXMT/YMTC flag, contributor panel of ≥10.
  - m8: legal review.
  - m9: index methodology plus 24-month back-fill.
  - m12: first licence and clause kit.
  - m13–18: free pooled-forecast portal; target 27+ accounts and 2+ licences; decide on full-time.
- **Team:**
  - The founder (product and engineering).
  - Advisors: an industrial-OEM procurement lead; an index-methodology advisor (ex-PRA or price-statistics background); a government-contracts attorney (contract work).
  - A part-time support contractor.
  - A sales/CS hire at $45k MRR (not reached in BASE within 36 months).
- **IP position:** nothing worth patenting. The moat is (i) the contributed price panel, (ii) index adoption written into contracts (lock-in for the contract's life) and (iii) a published, auditable methodology. Trademark the index name.
- **Regulation and funding:**
  - **§5949 (from 2027-12-23):** the proposed FAR Case 2023-008 (2026-02-17) accepts supplier self-certification. A BOM-level CXMT/YMTC flag is a cheap feature and overlaps with DD1.
  - **SBIR/STTR:** reauthorized through 2031-09-30. The founder **cannot be SBIR PI** while employed (>50% rule). **STTR with UMD CALCE** (lifetime-buy optimization; Prof. Sandborn) is the plausible non-dilutive route for an LTB/DMSMS forecasting module. No current topic was found.
  - **No CHIPS money and no fab dependency.**

## 11. Open gaps (ranked)

1. **Nexar Standard/Pro prices and written display/redistribution terms; DigiKey and Mouser terms.** These are the largest COGS and legal unknowns.
2. **Real SMB willingness to pay for a memory-only tool.** No deal-size data exists; only list anchors. The kill test resolves it.
3. **Whether any U.S. OEM, EMS or integrator would cite a non-TrendForce memory index.** No U.S. surcharge notice was found; the only examples are from the EU.
4. **Whether GSAM 552.238-120 allows a third-party market index for MAS EPAs.** Also open: PRA index-licence fee schedules.
5. **Prices for Counterpoint, inSpectrum, Supplyframe CIQ, Sourcengine and Cofactr.** Not found or not searched.
6. **Count of U.S. SMB OEMs with $1–50M BOM spend.** The 6,000 figure is unsourced.
7. **A current DoD DMSMS SBIR/STTR topic.** None found.
