# Phase 1: U.S. memory back-end, modules, die supply, mil/aero, recertification and test

Agent: `p1-backend` · Written: 2026-11-01 · Mission scope: §3C (back-end and supply chain) · Sources: `research/sources/p1-backend.jsonl` · Assumptions: `research/assumptions/p1-backend.md`

> **Read this first: how far to trust this file.**
> When this agent started, sibling agents had already used up the session's shared web-search budget (200 calls; my first three searches were refused). WebFetch could not resolve `en.wikipedia.org` or `ir.amkor.com` either. The proxy log also shows `sec.gov`, `trendforce.com` and `investors.micron.com` denied. As the tool instructed, I stopped trying further hosts after two DNS failures. **I opened no web page this session.** The evidence therefore falls into three groups:
> 1. **[REPORTED]** facts cite a URL another agent in this engagement saw in a search snippet. Each is re-logged in my source file as a `CROSS-REFERENCE`, and I copied the URLs from those logs rather than retyping them.
> 2. **[UNVERIFIED: PK]** facts come from my own training knowledge, which runs to about mid-2026. They carry no URL, because CONVENTIONS forbids citing URLs I did not open or see. Regulations are cited by section number (for example DFARS 252.246-7008 or FAR 52.211-5), so they can be checked directly. **Most company facts in this file are PK.** Treat them as a well-informed starting map, not as evidence.
> 3. **[ESTIMATE]** numbers are computed in a scratch script (`scratchpad/p1-backend/backend_estimates.py`, not a deliverable; formulas reproduced in §6.6 and §3.4). Every input is logged in the assumptions file.
>
> **Nothing here is [VERIFIED].** §9 lists the 15 checks to run first once web access returns, ordered by how much a decision depends on each.
>
> **Phase 1b update (agent `v3-backend`, 2026-11-01).** Used-RDIMM prices, SpecTek, KGD suppliers, legacy suppliers, U.S. module assembly, Amkor, ITAD and counterfeits were re-checked through search snippets. Facts confirmed this way are tagged **[REPORTED]** (secondary source) or **[REPORTED-P]** (primary document seen via snippet), and facts that changed are marked "(v3)". The change log is in `phase1/verify_v3-backend.md`, and sources are in `research/sources/v3-backend.jsonl`.

---

## 0. Summary table: U.S. back-end capabilities and gaps (as of 2026-11-01)

"DRAM-relevant" asks whether the capability can handle **commodity DRAM die or modules** today. "Small customers" asks whether a company under $2M can realistically get service.

| # | Capability | Who does it in the U.S. today | DRAM-relevant? | Takes small customers? | Gap / what's missing | Tag |
|---|---|---|---|---|---|---|
| 1 | **High-volume commodity DRAM component packaging** (FBGA 78/96/102-ball, multi-die wire-bond, DDR4/DDR5/LPDDR) | **Nobody.** Micron, Samsung, SK hynix and the OSATs do this in Asia. | n/a | n/a | **Complete gap.** No U.S. line packages DDR4/DDR5 FBGA at volume. Micron's U.S. back-end plans are HBM, after 2028. | [UNVERIFIED: PK] + [REPORTED] ([The Manufacturer](https://www.themanufacturer.com/articles/micron-technology-announces-200bn-investment-in-semiconductor-manufacturing-and-rd-in-idaho-new-york-and-virginia/)) |
| 2 | **HBM TSV stacking** | None. SK hynix West Lafayette IN starts **2H 2028 to Q3 2029**. Micron's U.S. HBM packaging comes only after ID2 (late 2028), so no earlier than 2029. | Yes (HBM) | No | Gap until 2028–29. Captive to memory makers even then. | [REPORTED] ([Evertiq](https://evertiq.com/news/2026-08-28-sk-hynix-breaks-ground-on-4-billion-packaging-facility-in-indiana); [Herald](https://mbiz.heraldcorp.com/article/10853891)) |
| 3 | **2.5D integration** (CoWoS/InFO-class: HBM next to GPU on interposer) | Amkor Peoria AZ, under construction with production around **early 2028**. (v3) The plan is ~$7B in two phases, with ~$12B reported including phase 2 (2026-09). TSMC signed a 10-year InFO/CoWoS deal and NVIDIA a $1.5B capacity deal (2026-07). Intel (EMIB/Foveros, NM and AZ) is mostly captive. | Integrates HBM; does not make it (no HBM/DRAM packaging confirmed) | No (anchor customers: Apple, NVIDIA, TSMC) | U.S. CoWoS-class capacity is ~0 until 2028. | Amkor: [REPORTED] ([GPEC, 2026-09-08](https://www.gpec.org/?p=31279); [Startup Fortune, 2026-07](https://startupfortune.com/nvidia-bets-15-billion-on-amkor-to-break-its-chip-packaging-bottleneck/)). Intel: [UNVERIFIED: PK] |
| 4 | **Hi-rel / low-volume DRAM packaging and multi-chip modules** (plastic and ceramic BGA DDR MCMs, stacked die) | Micross (FL/NC), Mercury Systems (Phoenix AZ), Data Device Corp (Bohemia NY), Integra (Wichita KS), Frontgrade (Colorado Springs). In France: Teledyne e2v and 3D Plus. | **Yes, but defense and space only** | Yes (defense primes, small lots) | Exists, but is sized for thousands of units at $100s–$1,000s each, not millions at $5–50. | [UNVERIFIED: PK] |
| 5 | **Quick-turn prototype packaging** (wire-bond BGA/QFN, open-cavity, SiP) | QP Technologies / Promex (Escondido and Santa Clara CA), Golden Altos (Milpitas CA), Micross. | Yes, for prototypes of custom DRAM-die packages | **Yes, this is their core market** | Fine for engineering samples. Nobody does mid-volume (10k–1M/yr) JEDEC-compliant DRAM FBGA. | [UNVERIFIED: PK] |
| 6 | **3D / hybrid-bonding prototyping** | NHanced Semiconductors (NC), Texas Institute for Electronics (UT Austin, DARPA NGMM), SkyWater FL (fan-out), Intel. | Relevant to 3D-DRAM and custom stacks | NHanced and TIE: yes, at prototype scale | R&D scale only | [UNVERIFIED: PK] |
| 7 | **Memory module SMT assembly** (UDIMM/SODIMM/RDIMM) | **Kingston (Fountain Valley CA)**, Virtium (Rancho Santa Margarita CA), likely limited lines at SMART Modular (Newark CA) and Viking/Sanmina. Any U.S. EMS could build DIMMs. | **Yes** | Kingston and Virtium: no, they are brands. EMS: yes. | Not a capacity gap. **The gap is die allocation.** Assembly is about 1% of a 2026 DDR5 RDIMM's cost (§3.4). | Kingston FV and Virtium: [REPORTED] ([Hardware Secrets](https://hardwaresecrets.com/kingston-factory-tour-in-fountain-valley-ca-usa); [Built In](https://www.builtinsf.com/company/virtium)). SMART/Viking: [UNVERIFIED: PK]. Cost share: [ESTIMATE] |
| 8 | **Bare die / KGD supply to small buyers** | Micross (largest authorized die distributor), Rochester Electronics (MA), SpecTek (Micron division, wafers). Taiwanese KGD programs: Winbond, ESMT, Etron (Nanya KGD not found, v3). | Yes | Partly: wafer-lot MOQs factory-direct, NDA, end-use paperwork. (v3) Legacy ESMT DDR4 KGD is also stocked by distributors in lots of hundreds of die ([Suntsu, 2026-05-26](https://suntsu.com/product/integrated-circuits/memory/kgd-256mbx16-ddr4-1-2v/)) [REPORTED] | **The main choke point.** Micron sells little or no open KGD. Samsung and SK hynix sell KGD only to strategic MCP customers. Small buyers get legacy Taiwanese KGD. | [REPORTED] ([Micross](https://micross.com/uploads/05827c98-1b61-4d4d-bb3c-04dc1b207e5a/Die_and_Wafer_Flyer_Rev_1_WEB.pdf); [SpecTek](https://micron.net/sales-support/customer-support/spectek-support); [Winbond](https://winbond.com/hq/product/customized-memory-solution/kgd/)) |
| 9 | **Authorized aftermarket / die banking / EOL re-creation** | Rochester Electronics (Newburyport MA), Micross, Lansdale (AZ). | Yes, legacy DRAM/SRAM | Yes | Exists and is entrenched. A newcomer has little room. Rochester claims capacity for upwards of 30B die in two ISO-7 sites. | Rochester: [REPORTED] ([Electronic Specifier](https://www.electronicspecifier.com/around-the-industry/the-worlds-largest-wafer-bank-has-tripled-in-size-at-rochester-electronics)). Others: [UNVERIFIED: PK] |
| 10 | **U.S.-made DRAM wafers for long-lifecycle buyers** | Micron Manassas VA (1-alpha DDR4/LP4 since 2026-05-22) | Yes | Through distribution only | Micron is aiming its new U.S. DRAM at exactly the defense, auto and industrial buyer a small venture would target. | [REPORTED] ([HPCwire](https://www.hpcwire.com/off-the-wire/micron-advances-made-in-america-memory-with-manufacturing-expansion-in-virginia)) |
| 11 | **Rad-hard / space memory** | Honeywell SSEC (Plymouth MN), BAE Systems (Manassas VA), Frontgrade (CO), Infineon/Cypress (rad-hard SRAM, F-RAM), Everspin (rad-tolerant Toggle MRAM, Chandler AZ), GSI Technology (SRAM, CA), DDC (NY), Mercury (AZ). | Mostly SRAM/MRAM/NOR. DDR only as screened MCMs. | Partly | Crowded, qualification-gated (QML), and a 3–5 year sales cycle | [REPORTED] (Everspin: [Frontgrade](https://www.frontgrade.com/news/new-case-study-touts-everspins-toggle-mram-highly-reliable-memory-technology-space)) + [UNVERIFIED: PK] |
| 12 | **ITAD / server decommissioning** | Iron Mountain (ITRenew, Sesame), Sims Lifecycle Services, SK tes, ERI, Apto, Park Place/Curvature, many regional R2/e-Stewards firms. | Yes: the source of recovered DDR4 RDIMMs | Yes, as buyers of lots | Exists at scale and is growing fast. (v3) Iron Mountain ALM revenue was $288M in Q2 2026 (+88% YoY) and is guided toward ~$1B for FY2026. Sims redeploys recovered DIMMs into CXL. Hyperscalers increasingly **reuse DDR4 internally** (e.g., via CXL), which shrinks the open-market flow. | [REPORTED] ([MarketBeat, 2026-08-08](https://www.marketbeat.com/instant-alerts/iron-mountain-q2-earnings-call-highlights-2026-08-08/); [SLS](https://www.simslifecycle.com/?p=13647)) |
| 13 | **Used server-memory resale** | eBay, ServerMonkey, Memory4Less, Curvature, TechMikeNY, BuySellRAM, Mobius Materials (authenticated marketplace, VA). | Yes | Yes. **Low barrier, crowded.** | Fragmented. Testing and provenance quality is uneven, which is an opening for a trust/provenance layer. (v3) Realized used-RDIMM prices to Aug 2026: 32GB DDR4 $100–150, 64GB DDR4 $250–370, 64GB DDR5 $890–1,200 ([amcompute](https://www.amcompute.com/appraisals/ddr4-64gb-rdimm)). | [REPORTED] ([BuySellRAM](https://www.buysellram.com/blog/ram-market-update/); [Mobius PR](https://www.prnewswire.com/news-releases/mobius-materials-raises-3m-to-combat-one-of-manufacturings-biggest-issues-amid-us-china-trade-tariffs-302643403.html)) + [UNVERIFIED: PK] |
| 14 | **Counterfeit-avoidance certification and test labs** (AS6081, AS6171, AS9120, IDEA-1010) | Independent distributors and third-party test labs; dozens in the U.S. | Yes | Yes | Exists. Certification costs tens of $k and takes 6–12 months. | [UNVERIFIED: PK] + [ESTIMATE] |
| 15 | **Component-level memory ATE** (Advantest T55xx, Teradyne Magnum) | Only at memory makers, OSATs and test houses. Used older testers circulate. | Yes | **No.** New systems cost $1M+, and used ones cannot run DDR5 speeds. | A small shop must use test services (ISE Labs, Integra, STS, Golden Altos) or module-level system test. | [UNVERIFIED: PK] + [ESTIMATE] |
| 16 | **Module-level testers** (CST, Innoventions RAMCHECK) and server-based burn-in | Bench equipment available to anyone | Yes | **Yes: $3k–$50k** | Not a gap | [UNVERIFIED: PK] + [ESTIMATE] |

**What the table says.** The U.S. can **assemble modules**, **package small lots of hi-rel memory**, **prototype**, **decommission servers** and **resell used memory**. It cannot **package commodity DRAM die at volume**, **stack HBM** (before 2028–29) or **get leading-edge DRAM die as a small buyer**. The missing middle is a mid-volume, JEDEC-grade DRAM packaging and test line with open die supply. It is missing because die supply is captive, not because nobody has thought of building it.

---

## 1. The eight most decision-relevant findings

1. **Assembly is about 1% of the value of a 2026 server module, and DRAM die is 93–98%.** A 64GB DDR5 RDIMM carries roughly $1,120–2,000 of DRAM, about $25 of other parts (RCD, PMIC, SPD hub, PCB) and about $12 of assembly and test [ESTIMATE, §3.4, from Counterpoint's $450→>$900 contract move ([EE Times Asia](https://www.eetasia.com/memory-prices-surging-by-90-from-4q-2025/))]. **A U.S. module business is a die-allocation and inventory-timing business, not a manufacturing business.** "U.S. module assembly" without a die contract is not a concept.
2. **Bare die is the choke point, as the mission premise says.** Micron's FY2026 10-K speaks of "supply allocation decisions that may affect some customers" ([10-K](https://www.sec.gov/Archives/edgar/data/0000723125/000072312526000023/mu-20260903.htm)), and TrendForce says module makers are being limited ([TrendForce abstract, 2026-01-14](https://www.trendforce.com/research/download/RP260114IU)) [REPORTED]. Authorized stock of a mainstream Micron DDR4 part was zero at Newark, Avnet and Mouser in May 2026 ([Findchips](https://blog.findchips.com/memory-shortage-watch-ddr3l-ddr4-may-2026/)) [REPORTED]. The open doors are **SpecTek wafers** (terms unknown; SpecTek targets consumer-grade uses, [micron.net](https://micron.net/sales-support/customer-support/spectek-support) [REPORTED-P]) and **Taiwanese specialty-DRAM KGD** (Winbond and ESMT confirmed; Etron listed; Nanya KGD not found). Both are legacy densities, at **wafer-lot MOQs of roughly $3k–22k per wafer** factory-direct [ESTIMATE, §4.2]. (v3) Legacy KGD is also available from distributor stock in lots of **hundreds of die**: ESMT 4Gb DDR4 x16, 175 die on 2026-05-26 ([Suntsu](https://suntsu.com/product/integrated-circuits/memory/kgd-256mbx16-ddr4-1-2v/)) [REPORTED].
3. **There is almost no "U.S.-assembled" price premium for commodity memory.** TAA compliance requires a *designated country* such as Taiwan, Korea or Japan, not the U.S. The Buy American Act preference (20–30% civilian, 50% DoD evaluation factor) applies only below the TAA threshold (about $174k) or against non-designated countries. The FTC bars an unqualified "Made in USA" claim on a module built from foreign die ("all or virtually all" rule, 16 CFR Part 323) [UNVERIFIED: PK]. **The real premiums are elsewhere:** (a) hi-rel and space memory MCMs, at 10–100× commodity $/bit [ESTIMATE]; (b) **provenance**: the FY2023 NDAA §5949 ban on CXMT/YMTC/SMIC-containing products in federal buys from **Dec 2027** ([XenoSpectrum](https://xenospectrum.com/en/apple-china-memory-federal-procurement-ban-2027/)) [REPORTED].
4. **Amkor Arizona is not memory capacity and does not exist yet.** The Peoria campus has a CHIPS award of up to about $407M (final Dec 2024) [UNVERIFIED: PK]. The plan is about $7B in two phases, and GPEC reports **~$12B including phase 2** ([GPEC, 2026-09-08](https://www.gpec.org/?p=31279)). Amkor added 67 acres in May 2026 ([Amkor IR](https://amkortech.gcs-web.com/node/24366)). The campus targets **logic 2.5D/fan-out packaging for Apple, NVIDIA and TSMC**, with production around **early 2028**. TSMC signed a 10-year InFO/CoWoS deal (~2026-06), and NVIDIA a **$1.5B multi-year capacity deal (2026-07-23)** ([Startup Fortune](https://startupfortune.com/nvidia-bets-15-billion-on-amkor-to-break-its-chip-packaging-bottleneck/)) [REPORTED]. It will integrate HBM stacks next to GPUs but will not make them; no HBM/DRAM packaging is confirmed (v3). **Mission §3C's listing of "Amkor (Arizona packaging)" as memory-adjacent capacity needs that correction.**
5. **Recovered DRAM already has a U.S. industry at module level; chip-level harvesting does not pencil out in the U.S.** ITAD firms (Iron Mountain/ITRenew, Sims, SK tes, ERI) feed eBay, brokers and refurbishers. DRAM is volatile, so unlike drives it needs no data destruction, which makes DIMMs among the easiest parts to resell [UNVERIFIED: PK]. Desolder-and-reball harvesting is labor-heavy, raises reliability concerns, sits close to counterfeiting (18 U.S.C. §2320), and is blocked by geometry: x4 server die cannot go onto consumer x8/x16 modules [UNVERIFIED: PK].
6. **Recovered DDR4 is worth about 3–8× its 2023 value, and the margin is cyclical.** Used DDR4 RDIMMs sold at about **$0.8–1.2/GB in 2023–24**, consistent with the DDR4 8Gb contract bottom of $1.30 in Sep 2023 ([KED Global](https://www.kedglobal.com/korean-chipmakers/newsView/ked202310040013)). My 2026 estimate is **$3–8/GB**: a 32GB RDIMM at about $96–256 and a 64GB at about $192–512. **(v3) Confirmed, in the lower half of that range.** Realized resale over the 12 months to Aug 2026 was **$100–150 per 32GB (+~335% YoY)** and **$250–370 per 64GB (+~285%)**, i.e. **$3.1–5.8/GB** ([amcompute 32GB](https://www.amcompute.com/appraisals/ddr4-32gb-rdimm); [64GB](https://www.amcompute.com/appraisals/ddr4-64gb-rdimm)) [REPORTED]. That is bounded above by DDR4 8Gb spot at $21–44/GB ([TrendForce board](https://www.trendforce.com/price_dram.html); [BuySellRAM](https://www.buysellram.com/blog/ram-market-update/)) and below by half of consumer retail DDR4 (about $3/GB) [ESTIMATE, §6.5]. **A U.S. test-and-resell shop clears about 20% contribution at 2026 prices and about 1–6% in a glut** [ESTIMATE, §6.6]. It is a 12–24-month window business, not a venture.
7. **Decommissioned server DRAM is a large flow.** The DDR4 cohort retiring in 2026 holds about **2.8–6.9 EB/yr globally (mid ~4.6 EB)**, about 9–22% of 2024's ~32 EB of new DRAM bits. About **0.2–1.6 EB/yr** of U.S. supply reaches the open market, worth roughly **$0.6–12B/yr at 2026 prices (mid $1.9–5.2B)** and **$0.1–2.3B in a glut** [ESTIMATE, §6.4]. Every input is uncertain, so treat this as an order of magnitude. **Hyperscalers are moving to reuse DDR4 internally behind CXL controllers** (Microsoft GreenSKU research; Marvell Structera with DDR4 support) [UNVERIFIED: PK], which caps the open-market share. (v3) ITAD firms are doing the same: Sims Lifecycle redeployed recovered DIMMs into production CXL memory at scale in Apr 2025 ([SLS](https://www.simslifecycle.com/?p=13647)) [REPORTED-P].
8. **Legacy and long-lifecycle memory is the tightest segment, and Micron itself is now the U.S. incumbent there.** DDR4 inverted over DDR5 twice. Barclays has DDR4 contract prices up 24% over the three months to Oct 2026 ([Guru3D](https://www.guru3d.com/story/ddr4-memory-prices-now-also-rise-as-dram-supply-shortages-intensify-through-2028/)), and auto/industrial buffers fell from 31+ weeks to 6–8 weeks ([eeNews](https://www.eenewseurope.com/en/micron-ramps-us-made-ddr4-production-in-virginia/)) [REPORTED]. But **Micron Manassas began 1-alpha DDR4/LP4 for defense, auto and industrial buyers on 2026-05-22** ([HPCwire](https://www.hpcwire.com/off-the-wire/micron-advances-made-in-america-memory-with-manufacturing-expansion-in-virginia)) [REPORTED]. (v3) A >$2B investment quadruples Manassas DDR4 wafer supply, with qualified 1α output due by end-2026. Micron has **Strategic Customer Agreements with Ford, GM and seven auto Tier-1s/SoC vendors** and is the only supplier publicly committing to ongoing DDR4/LP4 ([Counterpoint, 2026](https://counterpointresearch.com/cn/reports/memory-crisis-automotive-industry-suppliers-automakers-response); [Tom's Hardware](https://www.tomshardware.com/tech-industry/micron-begins-producing-americas-most-advanced-dram-at-its-virginia-fab)) [REPORTED]. Rochester, Micross and Alliance Memory hold the aftermarket and long-lifecycle channels. A newcomer's opening is **services** (provenance, test, die banking for mid-size OEMs, §5949 compliance), not supply.

---

## 2. OSAT and packaging capacity in the U.S.

### 2.1 Company-by-company

| Company / site | What it is (date) | Memory capability | Small customers? | Tag |
|---|---|---|---|---|
| **Amkor Technology, Peoria AZ** | 2023-11-30: ~$2B plan announced, Apple named first and largest customer. 2024-07-26: CHIPS PMT up to $400M plus $200M loans. 2024-10: TSMC–Amkor MOU for InFO and CoWoS turnkey packaging in Arizona. **2024-12-20: final CHIPS award up to ~$407M.** 2025-04-14: NVIDIA said it would use **Amkor and SPIL in Arizona** for packaging and test of U.S.-built AI systems. 2025: plan expanded to **~$7B** across two phases, a larger site and ~2,000–3,000 jobs, with **production pushed to early 2028**; groundbreaking reported in Oct 2025. (v3) **2026-05:** a 67-acre parcel was added to the 104-acre campus. **~2026-06:** TSMC–Amkor 10-year deal for turnkey InFO/CoWoS in Peoria. **2026-07-23:** NVIDIA $1.5B multi-year deal to fund Peoria capacity. **2026-09-08:** GPEC reports phase 2 lifts the plan to **~$12B** (not yet confirmed by Amkor). Amkor's HQ is Tempe AZ. Amkor has no volume production in the U.S. today. | **2.5D (CoWoS-class) and fan-out (InFO-class) for logic, plus test.** Integrates HBM stacks with GPUs; does **not** stack HBM (memory makers do TSV stacking in-house). Amkor packages memory in Asia; **no DRAM FBGA line is planned for AZ**, and none of the 2026 deals names HBM (v3). | **No.** Anchor-customer model with large NRE and volume commitments. Prototypes go to Amkor's Asian engineering centers. | (v3) $7B/2028, land, TSMC and NVIDIA deals: [REPORTED] ([AnySilicon](https://anysilicon.com/news/amkor-technology-expands-u-s-advanced-packaging-footprint-with-additional-land-in-arizona/); [Amkor IR](https://amkortech.gcs-web.com/node/24366); [KuCoin](https://www.kucoin.com/news/flash/tsmc-and-amkor-sign-10-year-deal-to-expand-semiconductor-packaging-in-arizona); [Startup Fortune](https://startupfortune.com/nvidia-bets-15-billion-on-amkor-to-break-its-chip-packaging-bottleneck/); [GPEC](https://www.gpec.org/?p=31279)). CHIPS award and groundbreaking date: [UNVERIFIED: PK] |
| **SkyWater Technology: Florida (Kissimmee, Osceola County "Center for NeoVation")** | SkyWater has operated the county-owned former BRIDG facility since about 2021. It is building **fan-out wafer-level packaging** (licensed Deca M-Series and Adaptive Patterning) and silicon interposers, largely DoD-funded. SkyWater's fabs: Bloomington MN (200mm, ex-Cypress) and **Austin TX Fab 25** (ex-Infineon, purchase closed 2025-06-30, ~400k wafer starts/yr) ([LaPedus](https://marklapedus.substack.com/p/skywater-acquires-infineons-200mm)) [REPORTED]. | No DRAM. Memory relevance is embedded NVM (Weebit ReRAM qualified in S130) ([Weebit](https://www.weebit-nano.com/news/press-releases/weebit-nanos-reram-ip-now-fully-qualified-in-skywater-technologys-s130-process/)) [REPORTED]. FL could prototype chiplet/interposer memory concepts. | **Yes in principle.** SkyWater's development-contract model serves startups and DoD, but NRE starts in the six figures. | Florida details: [UNVERIFIED: PK] |
| **Intel: Rio Rancho NM (Fab 9) and Chandler AZ** | Fab 9 opened 2024-01-24 for **Foveros 3D** packaging (part of a $3.5B NM investment). Chandler hosts Assembly/Test Development. Intel Foundry markets **EMIB and Foveros as standalone packaging services**, positioned as a CoWoS alternative. Intel's CHIPS award ($7.86B final, Nov 2024) was converted into a ~10% U.S. government equity stake in Aug 2025. | Integrates HBM with logic (EMIB). Does not package commodity DRAM. | **No.** Large-customer engagements only. | [UNVERIFIED: PK] |
| **Micross Components** (HQ Orlando FL; die processing in Apopka FL, the ex-Chip Supply site; wafer bumping and 3D integration in RTP NC; plus other U.S. and UK sites) | Calls itself the **largest authorized bare-die and wafer supplier**. DRAM is on its die line card, and **Micron is not named as a franchise** ([Micross flyer](https://micross.com/uploads/05827c98-1b61-4d4d-bb3c-04dc1b207e5a/Die_and_Wafer_Flyer_Rev_1_WEB.pdf)) [REPORTED]. Also does hi-rel plastic and hermetic packaging, upscreening, and **hi-rel DDR SDRAM multi-chip packages** built from purchased die. | **Yes: the closest existing analog to a "U.S. DRAM packaging house."** Low volume, defense-grade. | **Yes.** Defense primes and small lots. | Line card: [REPORTED]. Sites and MCMs: [UNVERIFIED: PK] |
| **Integra Technologies, Wichita KS** | Hi-rel OSAT: wafer probe, plastic and ceramic assembly, test, qualification. 2023: proposed a **~$1.8B expansion in Bel Aire KS** contingent on CHIPS funding. **I know of no award**, so status is unknown. | Can assemble and test memory die in hi-rel packages at low to mid volume. | Yes (hi-rel, mid volume) | [UNVERIFIED: PK] |
| **Promex Industries (Santa Clara CA) / QP Technologies (Escondido CA; formerly Quik-Pak)** | Promex bought Quik-Pak in 2019 and later rebranded it QP Technologies. Quick-turn **die prep** (dicing, thinning), **wire bond**, flip chip, **open-cavity and over-molded QFN/BGA**, SiP. Medical and hi-rel focus. | Can build **prototype wire-bond BGA packages of DRAM die**, including multi-die. JEDEC-grade high-speed DDR4/DDR5 FBGA needs substrate design and SI work the customer supplies. | **Yes: core market** (1 to ~10k units) | [UNVERIFIED: PK] |
| **Golden Altos, Milpitas CA** | Failure analysis, prototype assembly (wire bond), test and reliability services | Prototype memory packaging, failure analysis of DRAM | Yes | [UNVERIFIED: PK] |
| **NHanced Semiconductors** (fab in Morrisville NC; Tezzaron lineage) | U.S. advanced-packaging foundry for **hybrid bonding**, 3D stacking and interposers, largely DoD-funded. Its Tezzaron predecessor demonstrated 3D-stacked "DiRAM". | Relevant to **3D DRAM / custom stacked memory prototypes**, not commodity | Yes (prototype) | [UNVERIFIED: PK] |
| **Silicon Turnkey Solutions (STS), Milpitas CA** | Test, burn-in, upscreening and die services for aerospace and defense | Memory screening and upscreening (COTS to hi-rel) | Yes | [UNVERIFIED: PK] |
| **GlobalFoundries: Malta NY and Essex Junction VT** | CHIPS award ~$1.5B (final Nov 2024) for Malta/Essex capacity. 2025: ~$16B U.S. investment pledge including **advanced packaging and silicon photonics**; packaging work reported at both NY and VT. | No DRAM. Foundry-side 2.5D/3D for GF logic and photonics. | Through GF foundry engagements only | [UNVERIFIED: PK]. The packaging-specific award amount is unconfirmed. |
| **ASE / SPIL** | **ISE Labs** (Fremont CA, an ASE company) offers test engineering, characterization and reliability in the U.S. **SPIL** was named by NVIDIA (Apr 2025) for Arizona packaging; **I know of no confirmed SPIL or ASE production site in the U.S.** | ISE Labs can develop memory test programs | ISE Labs: yes (engineering services) | [UNVERIFIED: PK] |
| **SK hynix, West Lafayette IN** | ~$3.87–4B HBM packaging and R&D plant. Ceremonial groundbreaking 2026-08-27; cleanroom target Oct 2028; HBM4E mass production from Q3 2029 per CEO ([Evertiq](https://evertiq.com/news/2026-08-28-sk-hynix-breaks-ground-on-4-billion-packaging-facility-in-indiana); [Herald](https://mbiz.heraldcorp.com/article/10853891)) [REPORTED]. CHIPS award up to $458M plus up to $500M in loans (Dec 2024) [UNVERIFIED: PK]. The plant is packaging only, with no front-end DRAM ([Taipei Times, 2026-01-19](https://www.taipeitimes.com/News/biz/archives/2026/01/19/2003850817)) [REPORTED]. | HBM stacking | No (captive) | [REPORTED] / [UNVERIFIED: PK] |
| **Micron (U.S. HBM packaging)** | Plans to bring HBM packaging to the U.S. after ID2 is complete (ID2 output late 2028) ([The Manufacturer](https://www.themanufacturer.com/articles/micron-technology-announces-200bn-investment-in-semiconductor-manufacturing-and-rd-in-idaho-new-york-and-virginia/); [10-K](https://www.sec.gov/Archives/edgar/data/0000723125/000072312526000023/mu-20260903.htm)) [REPORTED] | HBM | No (captive) | [REPORTED] |
| **Texas Institute for Electronics (TIE), UT Austin** | DARPA **NGMM** program (~$840M, announced Jul 2024): a U.S. prototyping center for 3D heterogeneous integration | Possible venue for stacked-memory prototypes | Intended for DoD, academia and startups eventually | [UNVERIFIED: PK] |
| **Mercury Systems (Phoenix AZ microelectronics; HQ Andover MA)** | Rugged and secure processing. Phoenix is the ex-White Electronic Designs / Microsemi memory business, acquired 2016. | **Hi-rel DDR multi-chip packages** and stacked memory for defense | Defense customers | [UNVERIFIED: PK] |
| **Data Device Corp (Bohemia NY; TransDigm)** | Absorbed Maxwell's RAD-PAK microelectronics (~2016) | **Rad-tolerant memory modules** (SDRAM/DDR in shielded packages) | Space and defense | [UNVERIFIED: PK] |

### 2.2 Which can package DRAM die, and in what form?

| Package type | Who in the U.S. | Volume reality | Notes |
|---|---|---|---|
| JEDEC FBGA, single die (DDR4 78/96-ball, DDR5 78/102-ball) | Prototype: QP Technologies, Golden Altos, Micross. Hi-rel: Micross, Integra. | Hundreds to low thousands per lot | No U.S. line is tuned for consumer/server DRAM cost (<$0.10 per package assembly) [ESTIMATE] |
| Multi-die wire-bond FBGA (DDP/QDP stacks) | Micross, Mercury, Integra; prototype at QP Technologies | Low volume | Stacking itself is mature; at volume it is an Asian commodity |
| Multi-chip DDR modules on substrate (x64/x72 MCM) | Micross, Mercury, DDC, Frontgrade. In France: Teledyne e2v and 3D Plus. | Thousands per year | Defense and space price points |
| TSV stacks (HBM, 3DS RDIMM die stacks) | None today. SK hynix IN from 2028–29; Micron after 2028. | — | Captive |
| Hybrid-bonded 3D stacks | NHanced, TIE, Intel (internal) | Prototype | R&D |
| Module SMT (DIMM/SODIMM/CAMM) | Kingston, Virtium, EMS houses | Kingston Fountain Valley: ~550k modules/month, about 6.6M/yr (undated tour; [Hardware Secrets](https://hardwaresecrets.com/kingston-factory-tour-in-fountain-valley-ca-usa)) [REPORTED] | Not a gap |

### 2.3 Government advanced-packaging programs (NSTC / NAPMP / Natcast): status

- **NAPMP** (National Advanced Packaging Manufacturing Program, CHIPS R&D): announced Nov 2023 with about $3B planned. Award rounds followed in 2024, including substrate R&D awards in Nov 2024. In Jan 2025 a **Tempe AZ (ASU) site was selected for the NAPMP Advanced Packaging Piloting Facility**, to be run by Natcast [UNVERIFIED: PK].
- **Natcast, the NSTC operator, was defunded.** In Aug 2025 Commerce Secretary Lutnick voided the roughly $7.4B Natcast agreement and moved NSTC functions to NIST. The CHIPS Program Office was reorganized under the "U.S. Investment Accelerator" (Mar 2025 executive order) [UNVERIFIED: PK]. **I could not confirm what happened afterwards to the Tempe piloting facility or the NAPMP grants.** The funding agent should verify.
- **What this means for us:** do not plan on NAPMP or NSTC packaging access within the 18-month window. Practical U.S. prototyping venues are TIE (Austin), NHanced (NC), SkyWater FL, ASU, and commercial quick-turn houses [ESTIMATE: judgment].
- **§48D:** the 35% advanced-manufacturing ITC requires construction to start by **2026-12-31**, so a new packaging line begun after that gets no credit under current law. Details are in `phase1/micron_us_makers.md` §1.6 (p1-micron) [REPORTED via sibling].

---

## 3. Module makers with U.S. operations

### 3.1 Who assembles in the U.S.?

| Company | HQ | U.S. assembly? | Focus / notes | Tag |
|---|---|---|---|---|
| **Kingston Technology** | Fountain Valley CA (founded 1987; private) | **Yes.** SMT and test lines in Fountain Valley, plus plants in Taiwan and China. (v3) An undated factory tour puts Fountain Valley at **~550k modules/month**, the smallest Kingston plant ([Hardware Secrets](https://hardwaresecrets.com/kingston-factory-tour-in-fountain-valley-ca-usa)) [REPORTED]. | Largest independent module maker. (v3, corrected) TrendForce shares: **78.7% on $14.2B (2021)**, **78.12% on $13.5B (2022)**, **68.8% (2023)**, when module sales fell 28%. No 2024 ranking found, and **">$15B/yr" is unsupported** ([Business Wire, 2024-11-13](https://www.businesswire.com/news/home/20241113299917/en/Kingston-Technology-Remains-Top-DRAM-Module-Supplier-for-2023); [Business Wire, 2022-09-06](https://www.businesswire.com/news/home/20220906005155/en/Kingston-Technology-Remains-Top-DRAM-Module-Supplier-for-2021)) [REPORTED-P]. Markets TAA-compliant products to government [UNVERIFIED: PK]. | [REPORTED] / [REPORTED-P] |
| **Penguin Solutions (formerly SMART Global Holdings; memory = SMART Modular Technologies)** | Milpitas/Newark CA. Nasdaq: PENG (renamed Oct 2024). | **Limited or specialty at most** [UNVERIFIED]. Volume manufacturing historically in Penang (Malaysia) and Atibaia (Brazil). SGH sold a majority stake in SMART Brazil in 2023. | Specialty DDR4/DDR5, **CXL add-in cards (4-DIMM and 8-DIMM AICs) and E3.S CXL modules**, NVDIMM, rugged and defense memory. SK Telecom invested ~$200M in 2024. | [UNVERIFIED: PK] |
| **Netlist** | Irvine CA | **No U.S. volume line found.** (v3, corrected) The FY2023 10-K still describes Netlist's **own Suzhou, PRC plant** (ISO 9001/14001, ≤1-week cycle times), and the FY2025 ARS mentions "new manufacturing facilities" at an unstated location ([10-K FY2023](https://www.sec.gov/Archives/edgar/data/1282631/000155837024001626/nlst-20231230x10k.htm); [ARS FY2025](https://www.sec.gov/Archives/edgar/data/0001282631/000110465926089262/nlst-20251227xars.pdf)) [REPORTED-P]. Q2 2026 revenue was **$109.85M** ([Panabee](https://www.panabee.com/news/netlist-earnings-q2-2026-report)) [REPORTED]. | **Patent-led company.** E.D. Tex. jury verdicts: **$303M vs Samsung (Apr 2023)**, **$445M vs Micron (May 2024)**, **$118M vs Samsung (Nov 2024)**. Several patents have been challenged or invalidated at the PTAB, with appeals ongoing. Revenue about $140–150M (2024) at low gross margin. SK hynix took a license in 2021. | [UNVERIFIED: PK] |
| **Virtium** | Rancho Santa Margarita CA | **Yes** (RSM CA), plus plants in Vietnam and China. It says it builds its products in the USA. | Industrial and long-lifecycle DDR modules, SSDs, embedded | [REPORTED] ([Built In](https://www.builtinsf.com/company/virtium); [OCBJ, undated](https://www.ocbj.com/?p=35756)) |
| **Viking Technology (Sanmina)** | Foothill Ranch CA | Possibly, at Sanmina U.S. plants [UNVERIFIED] | NVDIMM, DDR, flash | [UNVERIFIED: PK] |
| **PNY Technologies** | Parsippany NJ (East Coast) | Historically assembled in NJ; current status unknown | Consumer/workstation memory, NVIDIA professional boards | [UNVERIFIED: PK] |
| **OWC (Other World Computing)** | Woodstock IL | Unknown. Mainly a branded reseller of Mac upgrades. | Mac memory | [UNVERIFIED: PK] |
| **Corsair** | Fremont/Milpitas CA | **No.** Built at its own Taiwan factory and by contract manufacturers. | Gaming DDR4/DDR5 | [UNVERIFIED: PK] |
| **Patriot Memory** | Fremont CA | No (Taiwan) | Consumer | [UNVERIFIED: PK] |
| **G.Skill** | Taipei | No (Taiwan) | Enthusiast | [UNVERIFIED: PK] |
| **TeamGroup** | Taipei, with a U.S. office | No | Consumer/industrial | [UNVERIFIED: PK] |
| **ADATA / XPG** | Taipei | No | Consumer; #2–3 module house | [UNVERIFIED: PK] |
| **ATP Electronics** | Taipei, with a U.S. office (CA) | No (Taiwan) | Industrial long-lifecycle | [UNVERIFIED: PK] |
| **Innodisk** | New Taipei, with a U.S. office (CA) | No | Industrial | [UNVERIFIED: PK] |
| **Cervoz** | Taiwan | No | Industrial | [UNVERIFIED: PK] |
| "Simms" | Could not identify a U.S. module maker by this name. A UK distributor ("Simms International") exists. | — | — | [UNVERIFIED] |
| **Crucial (Micron)** | Boise ID | **Exited** consumer modules. Announced 2025-12-03, shipments through Feb 2026 ([StorageNewsletter](https://www.storagenewsletter.com/2025/12/05/micron-announces-exit-from-crucial-consumer-business/)) [REPORTED] | Micron modules were built in Asia | [REPORTED] |

**Answer to "who assembles in the U.S."** Kingston (Fountain Valley) and Virtium (RSM) are the clear cases. SMART, Viking and PNY may have limited or legacy U.S. capability. Everyone else builds in Taiwan, China or Malaysia. **Capacity to assemble modules is not the U.S. gap.** Any U.S. EMS (Sanmina, Jabil, Benchmark, Plexus, Kimball) can SMT a DIMM [UNVERIFIED: PK].

### 3.2 Non-DRAM module components: a second choke point for DDR5

DDR5 RDIMMs need an **RCD** (registering clock driver: Renesas, Rambus, Montage), a **PMIC** (Renesas, Monolithic Power Systems, Richtek and others), and an **SPD hub plus temperature sensors** (Renesas, Montage, Rambus). Montage is China-based. Whether §5949 or customers will treat Chinese RCDs and SPD hubs as a provenance problem is open [UNVERIFIED: PK]. **DIMM PCBs** are mostly Taiwanese or Chinese. U.S. PCB fabs (e.g., TTM) could build them at a premium [UNVERIFIED: PK].

### 3.3 Typical module-maker margins

| Type | Normal-year gross margin | Shortage-year behavior | Basis |
|---|---|---|---|
| Commodity module houses (ADATA, TeamGroup, Netlist-type resale) | **~5–15%** | Inventory revaluation lifts margins sharply (25–35%+). In gluts, write-downs push them to losses (2019, 2022–23). | [UNVERIFIED: PK]. Taiwanese listed module houses' reported GMs, recalled. |
| Industrial / long-lifecycle specialists (Innodisk, ATP, Virtium, SMART specialty) | **~20–35%** | Steadier; long-lifecycle pricing contracts | [UNVERIFIED: PK] |
| Hi-rel / defense memory MCMs (Micross, Mercury, DDC) | **~40–60%+** | Insensitive to the commodity cycle | [ESTIMATE: hi-rel component industry norms] |
| Netlist (reseller, 2023–24) | **low single digits to ~10%** | — | [UNVERIFIED: PK] |

**Why it matters:** module economics follow *die cost timing*, not manufacturing skill. Buying die early in an upswing makes money; buying at the top and selling into a glut destroys it. A small U.S. assembler has no die allocation to time [ESTIMATE: judgment].

### 3.4 How small is assembly's share? (DDR5 64GB 2Rx4 RDIMM) [ESTIMATE]

Construction: 2 ranks × 2 subchannels × 10 x4 chips = **40 × 16Gb die = 80 GB raw** (64GB plus ECC). Non-DRAM parts total about $25: RCD ~$8, PMIC ~$5, SPD hub and sensors ~$2, PCB ~$8, passives ~$2. Assembly and test cost about $12 (U.S. labor).

| DRAM $/GB scenario | DRAM | Other parts | Assembly + test | Total | DRAM share | Assembly share |
|---|---|---|---|---|---|---|
| 2023 trough ($1.5/GB) | $120 | $25 | $12 | $157 | 76% | 7.6% |
| 2026 contract low ($14/GB) | $1,120 | $25 | $12 | $1,157 | 97% | **1.0%** |
| 2026 contract high ($25/GB) | $2,000 | $25 | $12 | $2,037 | 98% | **0.6%** |
| Glut ($6/GB) | $480 | $25 | $12 | $517 | 93% | 2.3% |

The $14–25/GB range comes from p1-market's server RDIMM contract range (Counterpoint/Citi) ([EE Times Asia](https://www.eetasia.com/memory-prices-surging-by-90-from-4q-2025/)) [REPORTED inputs, ESTIMATE output].

### 3.5 Netlist's patents are a hazard for any new RDIMM maker

Netlist's asserted families cover rank multiplication, load reduction and **on-module power management (PMIC on DIMM)**. The PMIC claims read directly on DDR5 RDIMMs. A new U.S. DDR5 RDIMM brand would be the direct manufacturer, with no license, unless it sources modules or IP through a licensed party (SK hynix holds a 2021 license) [UNVERIFIED: PK; ESTIMATE: risk judgment]. (v3) 2026 headlines report a **Samsung–Netlist licensing deal plus a supply agreement**, and a **Samsung purchase of 10M Netlist shares** ([Panabee](https://www.panabee.com/news/netlist-earnings-q2-2026-report); [Finanztrends](https://www.finanztrends.de/news/netlist-samsung-kauft-zehn-millionen-aktien/)) [REPORTED, headline only; terms unseen]. If true, an unlicensed newcomer becomes a more isolated target. **Do a freedom-to-operate check before any module concept passes Phase 3.**

---

## 4. Bare die / KGD supply and the "U.S.-assembled" premium

### 4.1 Who sells DRAM die to small customers?

| Source | What | Small-buyer access | Tag |
|---|---|---|---|
| **Micron (direct)** | No public KGD catalog in 2026. Historic KGD vendor ([gov archive](https://corpora.tika.apache.org/base/docs/govdocs1/425/425118.pdf)). Allocation favors strategic customers. (v3) The FY2025 10-K lists Micron's sales forms as "components, modules, SSDs, managed NAND, multi-chip packages, and **wafers**", sold mainly through its direct sales force plus distributors. No KGD program is named ([10-K FY2025](https://www.sec.gov/Archives/edgar/data/723125/000072312525000028/mu-20250828.htm)) [REPORTED-P]. | **Effectively closed** | [REPORTED] / [REPORTED-P] |
| **SpecTek (Micron division)** | Sells NAND, DRAM and LPDRAM "in BGA packages, **wafers** and more" for **consumer-grade** uses: USB drives, cards, SSDs, entry-level tablets and phones ([SpecTek](https://micron.net/sales-support/customer-support/spectek-support)) [REPORTED-P]. Parts contain current Micron 1-alpha die ([TechInsights](https://www.techinsights.com/blog/spectek-pt040-56b-ddr5-dram-micron-1a-memory-floorplan-analysis)). Retail "SpecTek Select" DRAM is "manufactured and tested by Micron" ([Newegg](https://promotions.newegg.com/memory/13-1708/index.html)) [REPORTED]. | **The one door to Micron silicon in wafer form.** (v3) Search found no public MOQ, distributor list or 2026 allocation statement. **One email answers it** (kill test). | [REPORTED] |
| **Samsung, SK hynix** | KGD and wafer sales only to strategic MCP/SiP and HBM partners | Closed | [UNVERIFIED: PK] |
| **Winbond, ESMT, Etron, Nanya** (Taiwan) | Published KGD programs for SiP ([Winbond](https://winbond.com/hq/product/customized-memory-solution/kgd/); [ESMT](https://esmt.com.tw/en/Applications/Known-Good-Die); [Etron](https://etron.com/kgdm/)). Procurement follows JEDEC **JESD49B.01** ([JEDEC](https://www.jedec.org/node/8358)). | **Open, but legacy densities** (SDR to DDR4, LPDDR2–4, a few Gb per die). (v3) ESMT says it has KGD versions of its full DRAM range ([ESMT](https://esmt.com.tw/en/Applications/DRAM-Memory)), and distributors stock it in die-count lots: ESMT 4Gb DDR4 x16 KGD, **175 die available 2026-05-26**, lead time on request ([Suntsu](https://suntsu.com/product/integrated-circuits/memory/kgd-256mbx16-ddr4-1-2v/)). Neither Winbond nor ESMT publishes an MOQ. | [REPORTED] / [REPORTED-P]. Etron: no 2026 confirmation. Nanya KGD: **not found in v3 search**; treat as absent until confirmed. |
| **ISSI** (Milpitas; owned by Beijing Ingenic) | KGD for SiP from its DRAM/SRAM/NOR lines | Open; Chinese ownership (§5.1) | Ownership: [REPORTED] (§5.1). KGD: [UNVERIFIED: PK] |
| **Micross** (incl. ex-Chip Supply, Apopka FL) | Largest authorized die distributor; DRAM on its line card; Micron not named ([flyer](https://micross.com/uploads/05827c98-1b61-4d4d-bb3c-04dc1b207e5a/Die_and_Wafer_Flyer_Rev_1_WEB.pdf)) | Open. Waffle-pack and wafer quantities. Die processing (thinning, bumping) available. | [REPORTED] |
| **Rochester Electronics** (Newburyport MA) | Authorized aftermarket: die and wafer banking, EOL re-manufacture under license. (v3) Calls its die bank the world's largest, with capacity for upwards of 30B die in two ISO-7 sites; offers wafer saw, waffle/gel pack and T&R. Resells **Intelligent Memory** DRAM under a partnership ([Electronic Specifier](https://www.electronicspecifier.com/around-the-industry/the-worlds-largest-wafer-bank-has-tripled-in-size-at-rochester-electronics); [Electronics360](https://electronics360.globalspec.com/article/20892/rochester-electronics-and-intelligent-memory-ensure-the-availability-of-legacy-storage-solutions)). | Open, legacy. **No MOQ published.** | [REPORTED] |
| **SemiDice and other U.S. die brokers** | Die distribution and processing | Open, mostly analog and logic | [UNVERIFIED: PK] |

### 4.2 Minimum quantities and terms [ESTIMATE]

- **MOQ is usually one wafer**, and often one 25-wafer lot for a program. In dollars at 2026 prices (scratch script, section E):

| Die | Area (assumed) | Good die per 300mm wafer (85% yield) | GB per wafer | Value per wafer |
|---|---|---|---|---|
| DDR3 4Gb, legacy 3x-nm | 55 mm² | ~1,016 | ~508 | **~$3.0k** at $6/GB |
| DDR4 8Gb, 1z-class | 45 mm² | ~1,251 | ~1,251 | **~$20k** at $16/GB |
| DDR5 16Gb, 1a/1b-class | 70 mm² | ~791 | ~1,581 | **~$22k** at $14/GB |

- So **one 25-wafer lot costs roughly $75k (legacy) to $550k (DDR4/DDR5)** [ESTIMATE]. That is T1 working capital before any packaging.
- (v3) **Exception for legacy densities:** distributors hold KGD stock in **die-count lots** (ESMT 4Gb DDR4 x16, 175 die on 2026-05-26 at [Suntsu](https://suntsu.com/product/integrated-circuits/memory/kgd-256mbx16-ddr4-1-2v/)) [REPORTED]. Prototype and small-run builds of 4Gb-class parts therefore need not wait for a wafer lot. Price and lead time were not visible.
- KGD (tested, speed-binned, sometimes burned-in) carries a premium over packaged-equivalent $/GB of perhaps **15–40%** [ESTIMATE: KGD test-cost norms]. Unprobed or partially tested wafers are cheaper but push yield risk onto the packager.
- Typical terms: NDA, an **end-use / end-user statement** (export control), **prepayment or letter of credit** for new accounts in allocation, no returns on wafers, and KGD quality per JESD49B.01 [ESTIMATE: industry practice].

### 4.3 Is there a "U.S.-assembled" premium anyone pays?

| Rule | What it actually requires | Does it reward U.S. *assembly* of memory? | Tag |
|---|---|---|---|
| **Trade Agreements Act (TAA)** (FAR 25.4) | For federal buys above the threshold (**~$174k**, 2024–25), end products must come from the U.S. or a *designated country* (WTO-GPA/FTA). **Taiwan, Korea and Japan are designated; China is not.** | **No.** Taiwan-built modules are TAA-compliant. "TAA-compliant memory" in practice means "not assembled in China." | [UNVERIFIED: PK] |
| **Buy American Act (BAA)** (FAR 25.1; DFARS 225) | Applies **below the TAA threshold**, or to non-designated-country offers. A COTS end product manufactured in the U.S. counts as domestic; COTS items are exempt from the component-content test. Price evaluation factor: **20% (large business), 30% (small business), 50% DoD**. The non-COTS domestic-content threshold is 65% for 2024–2028 and 75% from 2029. | **Somewhat, for small federal buys under ~$174k.** Arguably fits a small company's reach (GSA, micro-purchases, SAP). | [UNVERIFIED: PK] |
| **FTC "Made in USA"** (16 CFR Part 323, 2021 labeling rule) | An unqualified claim requires "**all or virtually all**" U.S. content. A module built on Korean or Taiwanese die can say "**Assembled in USA**" at most. | Restricts marketing. **Only modules on Micron U.S. die (Manassas, later Boise) could approach an unqualified claim.** | [UNVERIFIED: PK] |
| **NDAA FY2019 §889** | Bans Huawei, ZTE, Hytera, Hikvision and Dahua telecom/video equipment and services | **Not memory-specific.** Irrelevant to DRAM except as supply-chain diligence. | [UNVERIFIED: PK] |
| **NDAA FY2023 §5949** | From **Dec 2027**, federal agencies may not buy products containing **SMIC, YMTC or CXMT** semiconductors (or affiliates') ([XenoSpectrum](https://xenospectrum.com/en/apple-china-memory-federal-procurement-ban-2027/)) | **Not assembly, but provenance.** Creates demand for verifying that memory in federal-bound systems is non-CXMT/YMTC. CXMT is the main source of new DDR4/DDR5 bits (see p1-market). | [REPORTED]. FAR implementing-rule status: [UNVERIFIED] |
| **DFARS 252.246-7007 / -7008** (counterfeit detection; sources of electronic parts) and **FAR 52.211-5** (new material) | DoD contractors must buy from the OCM or authorized sources, or from "contractor-approved suppliers" with testing per industry standards. Used or reconditioned parts are not allowed unless the contracting officer authorizes them. | Rewards **authorized, traceable** supply, not U.S. assembly. **Effectively bars recovered DRAM from DoD deliverables.** | [UNVERIFIED: PK] |
| **DMEA Trusted Foundry / Trusted Supplier** accreditation | For ASICs and trusted microelectronics: design, foundry, packaging, test | Not for COTS DRAM, but hi-rel memory MCM makers serving trusted programs benefit | [UNVERIFIED: PK] |

**Who actually pays a premium:** (1) **defense and space programs** for hi-rel, screened, traceable memory MCMs, at 10–100× commodity $/bit [ESTIMATE]; (2) **long-lifecycle industrial, medical and rail OEMs** for supply guarantees (§5.3); (3) **from Dec 2027, federal integrators** who need §5949-clean bills of materials. **Plain commodity modules assembled in the U.S. command roughly a 0–10% premium, and only in BAA-covered small buys** [ESTIMATE: judgment from the rules above]. The p1-micron agent found that memory currently pays **0% Section 232 tariff**, so tariffs add no U.S.-made premium today ([micron_us_makers.md §4](micron_us_makers.md)) [REPORTED via sibling].

---

## 5. Legacy / long-lifecycle and mil/aero memory suppliers with U.S. presence

### 5.1 Legacy commercial memory

| Company | HQ / ownership | Products | Notes | Tag |
|---|---|---|---|---|
| **Alliance Memory** | Kirkland WA; private (ownership not confirmed in v3) | Legacy SDRAM, DDR1–DDR4, LPDDR, SRAM, NOR. **Drop-in replacements for EOL parts** from the majors. | Fabless, specializing in legacy and long-life-cycle memory ([Arrow](https://www.arrow.com/en/manufacturers/a/alliance-memory.html)) [REPORTED]. Die from foundry and IDM partners (unnamed). Its pitch is "we don't EOL." Sold through Mouser, DigiKey and others. (v3) An undated vendor post says it raised DDR4 stock before a **30% price increase** and holds wafer-die inventory to avoid die shrinks ([DigiKey forum](https://forum.digikey.com/t/ddr4-sdrams-are-becoming-harder-to-source-not-with-alliance-memory/56709)). No 2026 news found. | [REPORTED] (basics); ownership [UNVERIFIED: PK] |
| **ISSI** | Milpitas CA. **Owned by Beijing Ingenic Semiconductor** (taken private 2015 for ~$765M by a Chinese consortium [UNVERIFIED: PK]; **merged into Ingenic with Lumissil in 2020** [REPORTED]) | Auto/industrial DRAM, SRAM, NOR; KGD. (v3) **DDR4 and LPDDR4/4X supported through at least 2038** ([AMD brief](https://www.amd.com/content/dam/amd/en/documents/products/adaptive-socs-and-fpgas/technologies/issi-memory-solution-brief.pdf)) [REPORTED-P] | **Chinese-owned.** Not on the §5949 list itself, but any SMIC-fabbed content would be caught from Dec 2027. A sourcing risk for defense. Its 2038 DDR4 commitment makes it Micron Manassas's main long-lifecycle rival for non-defense buyers. | [REPORTED] ([RISC-V Intl](https://riscv.org/?p=20050)) |
| **Intelligent Memory** | Hong Kong / Germany [UNVERIFIED: PK] | Long-lifecycle DRAM, ECC-integrated DRAM, high-density legacy (e.g., stacked DDR3). (v3) 16Gb x4 DDR4 components for RDIMMs ([Mouser](https://www.mouser.pe/new/intelligent-memory/im-16gb-x4-ddr4-dram-components)). **DDR4 32Gb x8/x16 parts return only from Q3 2026**, which IM blames on the HBM shift ([IM, Embedded World 2026](https://www.intelligentmemory.com/company/articles-news-events/intelligent-memory-to-exhibit-at-embedded-world-2026)) [REPORTED-P] | U.S. sales only. Also sold via Rochester (partnership) | Products: [REPORTED-P] |
| **Lansdale Semiconductor** | Tempe AZ | Licensed re-manufacture of obsolete ICs (ex-Intel, AMD, Motorola lines) | Mostly logic; little DRAM | [UNVERIFIED: PK] |
| **Rochester Electronics** | Newburyport MA (East Coast) | Authorized aftermarket: EOL stock, die and wafer banking, licensed re-creation for 70+ OCMs | Incumbent for "still exists in 2040". Die bank: [REPORTED] (§4.1) | OCM count: [UNVERIFIED: PK] |
| **Zentel** | Taiwan | Specialty DDR3/DDR4/LPDDR | Foundry-made | [UNVERIFIED: PK] |
| **Etron** | Taiwan | Specialty DRAM, KGDM ([Etron](https://etron.com/kgdm/)) | U.S. sales | [REPORTED] |
| **Winbond, Nanya, ESMT** | Taiwan | Legacy and specialty DRAM. Nanya and Winbond earned DDR4 windfalls in 2025–26 (see p1-market). Samsung and SK hynix pushed their DDR4 exits into 2026, and Micron issued DDR4 EOL notices in Jun 2025 ([TrendForce News, 2025-09-02](https://www.trendforce.com/news/2025/09/02/news-samsung-sk-hynix-reportedly-delay-phase-out-to-2026-as-ddr4-becomes-unexpected-cash-cow/)). | Backfilling Samsung/SK hynix DDR4 exits | [REPORTED] |
| **GSI Technology** | Sunnyvale CA (Nasdaq: GSIT) | High-performance and **rad-hard / rad-tolerant SRAM** | Fabless (TSMC) | [UNVERIFIED: PK] |
| **Micron Manassas** | Manassas VA | 1-alpha DDR4/LP4 for auto, defense, aerospace and industrial since 2026-05-22 ([HPCwire](https://www.hpcwire.com/off-the-wire/micron-advances-made-in-america-memory-with-manufacturing-expansion-in-virginia)) | **The U.S.-made long-lifecycle incumbent.** TrendForce still expects the DDR4 shortage to persist ([I-Connect007](https://iconnect007.com/article/150148/microns-fab-6-starts-lpddr4-and-ddr4-production-but-ddr4-shortage-is-expected-to-persist/150145/flex)). (v3) A >$2B investment quadruples Manassas DDR4 wafer supply, backed by $275M in CHIPS funding. Qualified 1α output is due by end-2026. Micron has Strategic Customer Agreements with Astemo, Denso, Harman, Hyundai Mobis, Joynext, Qualcomm, Visteon, Ford and GM. It is the only supplier publicly committed to ongoing DDR4/LP4; Samsung's auto DDR4/LP4 runway ends Q1 2027, and SK hynix has no commitment beyond 2026 ([Counterpoint](https://counterpointresearch.com/cn/reports/memory-crisis-automotive-industry-suppliers-automakers-response); [Tom's Hardware](https://www.tomshardware.com/tech-industry/micron-begins-producing-americas-most-advanced-dram-at-its-virginia-fab)) | [REPORTED] |

### 5.2 Mil/aero and rad-hard memory

| Company | U.S. site | Memory products | Tag |
|---|---|---|---|
| **Mercury Systems** | Phoenix AZ (microelectronics); HQ Andover MA | Rugged DDR multi-chip packages, secure memory/storage (ex-Microsemi / White Electronic Designs, acquired 2016) | [UNVERIFIED: PK] |
| **Frontgrade Technologies** (CAES's former space business, renamed 2023) | Colorado Springs CO; HQ Austin TX | Rad-hard SRAM, SDRAM, NOR and **MRAM modules on Everspin Toggle die** (>1 Mrad(Si) TID, QML-Q/Q+) ([Frontgrade](https://www.frontgrade.com/news/new-case-study-touts-everspins-toggle-mram-highly-reliable-memory-technology-space)) | [REPORTED] / corporate history [UNVERIFIED: PK] |
| **CAES** (defense electronics remainder) | Arlington VA | Acquired by **Honeywell** (~$1.9B, 2024) | [UNVERIFIED: PK] |
| **Honeywell SSEC** | Plymouth MN | DMEA-trusted rad-hard SOI fab; rad-hard SRAM and MRAM | [UNVERIFIED: PK] |
| **BAE Systems FAST Labs / trusted foundry** | Manassas VA | Rad-hard 150nm-class fab: rad-hard SRAM, RAD750/RAD5545 processors | [UNVERIFIED: PK] |
| **Teledyne e2v** | Grenoble, France (HiRel); U.S. sales and HiRel ops in CA | **Space-grade DDR4 multi-chip memory** (4GB/8GB class) | [UNVERIFIED: PK] |
| **3D Plus** (HEICO since 2011) | Buc, France | Stacked DDR3/DDR4/SDRAM/NAND modules for space | [UNVERIFIED: PK] |
| **Data Device Corp** (TransDigm) | Bohemia NY (East Coast) | RAD-PAK rad-tolerant SDRAM/SRAM/EEPROM modules (ex-Maxwell) | [UNVERIFIED: PK] |
| **Infineon (ex-Cypress)** | U.S. design; manufacturing partly at SkyWater MN historically | Rad-hard SRAM (RadStop), **rad-hard F-RAM**, NOR, QML-V | [UNVERIFIED: PK] |
| **Everspin** | Chandler AZ (magnetic BEOL, co-located at NXP) | **Rad-tolerant Toggle MRAM**. DoD rad-hard FPGA program with QuickLogic (2024) ([BusinessWire](https://www.businesswire.com/news/home/20240724863768/en/Everspin-Announces-Contract-to-Provide-MRAM-Technology-for-Strategic-Radiation-Hardened-FPGA)). $40M defense subcontract (2026-04) ([Electronics360](https://electronics360.globalspec.com/article/23702/everspin-earns-40-million-mram-deal-for-defense-memory-services)). Microchip Gresham OR second source from 2H-2027 ([Silicon Semiconductor](https://siliconsemiconductor.net/article/123971/Everspin_Technologies_expands_on-shore_MRAM_manufacturing_capacity)). | [REPORTED] |

DoD keeps funding exotic memory packaging. Example: the DARPA SBIR DPA26BZ04-DV017 Direct-to-Phase-II topic for a co-packaged −269 °C to +600 °C rad-tolerant NOR flash system (opened 2026-07-22) ([DARPA](https://www.darpa.mil/research/programs/non-volatile-memory-extreme-environments)) [REPORTED]. **This is a non-dilutive channel for a packaging-centric memory concept, but its timeline does not fit the founder (a 3–5 year qualification cycle).**

### 5.3 Who pays premiums for "still exists in 2040"?

| Buyer | Why lifecycle matters | What they pay for | Premium [ESTIMATE] |
|---|---|---|---|
| **DoD programs** (DMSMS) | Platforms sustained 30–50 years; requalification costs millions | LTB plus die banking (Rochester, Micross), emulation and re-creation, hi-rel MCMs | Authorized aftermarket at **~1.5–5×** original price. Broker market in shortages at **up to 10×+**. |
| **Avionics** (DO-254) | Recertification after a part change is expensive | Lifetime buys, long-lifecycle vendors | 1.5–3× |
| **Industrial automation, rail signaling, grid protection** | 15–30 year field life | Long-lifecycle DRAM (Alliance, Intelligent Memory, ATP, Innodisk, Virtium), 5–10 year supply commitments | 1.2–2× commodity in normal times. **Higher now:** Advantech tells customers to avoid Samsung DDR4 in new designs ([Advantech](https://www.advantech.com/en/resources/news/response-measures-to-samsung-ddr4-ic-eol-announcement)) [REPORTED]. |
| **Medical imaging / devices** | FDA re-validation | Lifetime buys | 1.2–2× |
| **Automotive** | 15-year service-parts obligation | Auto-grade legacy DRAM (ISSI, Micron Manassas, Winbond) | Contracted; modest premium |

Market evidence: in May 2026 authorized stock of a mainstream Micron DDR4 part was zero, and independent-market stock carried a premium ([Findchips](https://blog.findchips.com/memory-shortage-watch-ddr3l-ddr4-may-2026/)) [REPORTED]. The **"2040" guarantee itself is sold by Rochester (authorized re-creation) and by die banking**, not by new fabs. **A new entrant would compete with Rochester and Micross for die-bank customers.** The opening is mid-size OEMs those firms underserve, and software for DMSMS forecasting and LTB sizing [ESTIMATE: judgment].

---

## 6. Recertification, ITAD and recovered DRAM in the U.S.

### 6.1 ITAD players

| Player | What | Relevance | Tag |
|---|---|---|---|
| **Iron Mountain: Asset Lifecycle Management (ALM)** | Acquired **ITRenew** (announced Jan 2022; ~80% for ~$725M, remainder later). ITRenew decommissions hyperscale fleets, and **Sesame by ITRenew** resells decommissioned hyperscale OCP racks and servers. Iron Mountain has added more ITAD firms since 2024. | The largest U.S. channel from hyperscale decommissioning to reuse. A potential **supplier** of recovered RDIMM lots and a **competitor** in recert. (v3) ALM revenue: **$232M in Q1 2026 (+92% YoY, 77% organic)** and **$288M in Q2 2026 (+88%, 82% organic)**; data-center decommissioning grew >100% organic. **FY2026 ALM is guided toward ~$1B.** Management warned the YoY *pricing* tailwind will fade and plans more ITAD consolidation ([MarketBeat Q1](https://www.marketbeat.com/earnings/reports/2026-4-30-iron-mountain-incorporated-stock/); [MarketBeat Q2](https://www.marketbeat.com/instant-alerts/iron-mountain-q2-earnings-call-highlights-2026-08-08/)) [REPORTED]. | ITRenew deal terms: [UNVERIFIED: PK]. ALM 2026: [REPORTED] |
| **Sims Lifecycle Services** (Sims Ltd) | Data-center decommissioning and repurposing. (v3) Investor day 2026-03-25 presented a capital-light model earning from services and resale. SLS harvests and resells memory modules, SSDs and CPUs from hyperscale decommissioning, and **redeployed recovered DIMMs into production CXL memory at scale (Apr 2025)** ([Sims](https://www.simsltd.com/wp-content/uploads/sites/7/2026/03/SLS-Investor-Day-Presentation-FINAL.pdf); [SLS](https://www.simslifecycle.com/?p=13647); [Resource Recycling, 2026-02-18](https://dev.resource-recycling.com/e-scrap/2026/02/18/sims-lifecycle-leverages-hyperscale-decommissioning/)). | Supplier and competitor, **already in CXL-DDR4 reuse** (overlaps seed S6) | [REPORTED-P] |
| **SK tes** (ex-TES; SK ecoplant acquired 2022, ~$1B) | Global ITAD and battery recycling with U.S. sites | Supplier and competitor | [UNVERIFIED: PK] |
| **ERI** | Fresno CA; largest U.S. e-waste recycler; R2/e-Stewards/NAID | Supplier of mixed lots | [UNVERIFIED: PK] |
| **Others:** Apto Solutions, Ingram Micro ITAD, Park Place Technologies (owns Curvature: third-party maintenance plus used spares), Procurri, Dataserv, Exit Technologies | Mixed ITAD, third-party maintenance, resale | Buyers and sellers of server memory | [UNVERIFIED: PK] |

(v3) **Market size:** U.S. ITAD was **$5.3B in 2025** per GMI, or **$7.1B in 2024** per another firm; global was $17.5–20.8B ([GMI](https://www.gminsights.com/industry-analysis/IT-asset-disposition-market); [Supply Chain Digital](https://supplychaindigital.com/globenewswire/3376893)). An Iron Mountain executive is cited as putting the data-center decommissioning addressable market at **~$8B** ([Resource Recycling, 2026-06-18](https://resource-recycling.com/e-scrap/2026/06/18/data-center-boom-sets-up-itad-growth/)) [REPORTED]. Definitions differ across firms.

**Hyperscaler behavior** [UNVERIFIED: PK]:
- **Microsoft** runs **Circular Centers** (from 2020) and reported about 89–90% server and component reuse/recycling around FY2024, against a 90% target for 2025.
- **Google** reports reusing refurbished components in machine upgrades.
- Server depreciation lives were stretched to 5–6 years in 2022. Amazon shortened some to 5 years in 2025.
- **Hyperscalers are moving to reuse DDR4 behind CXL controllers.** Microsoft's GreenSKU research (ISCA 2024) proposed reusing DDR4 DIMMs via CXL in new servers, and Marvell's Structera CXL controllers (2024) support DDR4 for this purpose.
- **Inference:** during a shortage, hyperscalers keep more of their own DDR4, and less reaches ITAD resale [ESTIMATE: judgment].

### 6.2 Server-memory resale markets

- **eBay** is the largest U.S. venue for used server RDIMMs. Sold-listing data is the practical price index [UNVERIFIED: PK].
- Specialist resellers include **ServerMonkey, Memory4Less, Curvature/Park Place, TechMikeNY (NYC), NEMIX and A-Tech** (branded third-party server memory), plus many brokers [UNVERIFIED: PK]. I could not confirm a broker named "Smart Components" [UNVERIFIED].
- **BuySellRAM** is a U.S. used-memory buyer that publishes DRAMeXchange-based market updates as lead generation ([BuySellRAM](https://www.buysellram.com/blog/ram-market-update/)) [REPORTED]. **Servnet** (UK) publishes a server-memory price tracker ([Servnet](https://www.servnetuk.com/research/ddr5-server-memory-price-tracker-2026)) [REPORTED].
- **Mobius Materials** (Richmond VA; $3M seed, Dec 2025) runs an **authenticated** B2B secondary marketplace and has filed a patent on ML authentication ([PR Newswire](https://www.prnewswire.com/news-releases/mobius-materials-raises-3m-to-combat-one-of-manufacturings-biggest-issues-amid-us-china-trade-tariffs-302643403.html)) [REPORTED]. (v3) Confirmed: founder Margaret Upshur moved the company to Richmond from Silicon Valley. Trackers put total funding at **$3.0–4.1M**. Investors include Spero Ventures (reported lead), Outsiders Fund and Refashiond Ventures ([Digital Commerce 360, 2025-12-16](https://www.digitalcommerce360.com/2025/12/16/b2b-marketplace-mobius-materials-3-million-funding/amp/); [Mobius press](https://www.mobiusmaterials.com/press); [CB Insights](https://www.cbinsights.com/company/mobius-materials/financials)) [REPORTED]. The patent claim was not re-confirmed.
- (v3) **2026 used-memory price commentary** comes mostly from sellers:
  - Refurbishers say decommissioned-fleet DDR4 is now the main DDR4 source, and that used DDR4 server modules are up 30–50% from late-2025 lows ([PCSP](https://pcserverandparts.com/news/refurbished-ddr4-server-memory-2026-server-ram-price-crisis/)).
  - TechMikeNY and ITLDC blog about the surge, and ITLDC expects no DDR4 correction before the end of 2026 ([TechMikeNY](https://techmikeny.com/blogs/techtalk/rbc-the-2026-surge-in-ram-flash-pricing); [ITLDC](https://itldc.com/es/blog/server-ram-ssd-market-update-2026)).
  - These are [REPORTED] vendor claims. The only resale-price index found is **amcompute's** appraisal pages (§6.5). It is East Coast like the founder: **the closest venture-backed comparable, and a possible partner** for any recert or provenance concept.

### 6.3 Counterfeit risk, standards and legality

**Standards** (by identifier; all [UNVERIFIED: PK]):
- **SAE AS5553**: counterfeit-avoidance requirements for manufacturers and integrators.
- **SAE AS6081**: counterfeit-avoidance requirements for independent distributors (the certification a recertifier selling into aerospace or defense needs).
- **SAE AS6171**: test methods for suspect or counterfeit EEE parts (X-ray, XRF, decapsulation, SEM, electrical), with method slash sheets.
- **SAE AS6496**: authorized distribution.
- **AS9120**: QMS for aerospace distributors.
- **IDEA-STD-1010**: inspection standard for independent distributors.
- **GIDEP**: government-industry reporting of nonconforming and counterfeit parts. **ERAI** is the commercial counterpart.

**Counterfeit incidents in the 2026 shortage** (v3, [REPORTED]). Every documented case is a **consumer DDR5** module, not a server RDIMM:
- Dummy plastic "chips" relabeled as Samsung or SK hynix ([Tom's Hardware](https://www.tomshardware.com/pc-components/ddr5/scammers-are-selling-fake-ddr5-with-empty-plastic-chips-relabeled-to-pass-as-legit-fake-components-mounted-to-pcbs-are-yet-another-sign-of-the-rampocalypse)).
- **Re-soldered DDR4/DDR3 chips on fake DDR5 boards**, e.g. a fake Kingston Fury (2026-08-27) ([Profesional Review](https://www.profesionalreview.com/2026/08/27/un-comprador-descubre-una-estafa-de-memorias-ddr4-disfrazadas-de-ddr5-en-un-modulo-kingston-fury-y-advierte-es-casi-imposible-de-identificar/)).
- Cloned G.Skill and V-Color DDR5 on Chinese marketplaces, reported at Computex 2026 ([Tom's Hardware](https://www.tomshardware.com/pc-components/dram/counterfeit-g-skill-and-v-color-ddr5-modules-hit-chinese-marketplaces-impacting-company-sales-cheap-contraband-memory-using-identical-pcbs-and-heat-spreaders-almost-impossible-to-spot)).

ERAI reported a sharp uptick in counterfeit and nonconforming reports in 2024, but its **2025 annual report shows fewer parts reported than in 2024** ([ASM International](https://www.asminternational.org/news/49218564/); [ERAI](https://www.erai.com/erai_blog/page/3)). **No ERAI or GIDEP alert specific to memory in 2026 was found** [STILL-UNVERIFIED].

The re-soldered-chip cases show that the gap between used-module $/GB and chip-spot $/GB (§6.5) is already being arbitraged illicitly [ESTIMATE: judgment].

**DoD and federal rules** (all [UNVERIFIED: PK]):
- **DFARS 252.246-7007** requires a counterfeit detection and avoidance system, mainly for CAS-covered contractors.
- **DFARS 252.246-7008** governs sources of electronic parts: OCM or authorized first, else contractor-approved suppliers with testing. The statutory basis is FY2012 NDAA §818, as amended.
- **FAR 52.246-26** covers reporting of nonconforming items.
- **FAR 52.211-5** requires *new* material unless the contracting officer approves otherwise.
- **18 U.S.C. §2320** covers trafficking in counterfeit goods, with enhanced penalties for counterfeit military goods (up to 20 years).

**Legality of harvesting** (all [UNVERIFIED: PK]):
- Buying used equipment, removing modules or chips, testing them and **reselling them disclosed as used/refurbished** is legal in the U.S. under first-sale.
- **Remarking, sanding, relabeling or selling as new** is counterfeiting.
- Re-branding a module built on harvested die requires disclosure, and trademark risk applies if OEM marks are misused.
- DRAM is **volatile**: NIST SP 800-88 treats power removal as sanitizing volatile RAM, so unlike drives there is no data-destruction burden.
- Exporting e-waste to non-OECD countries is restricted by importing countries under the Basel framework. The U.S. is not a Party; the U.S. CRT rule is the main federal export rule.
- **Certifications that buyers and ITAD suppliers expect:** **R2v3** (SERI) or **e-Stewards** (Basel Action Network), and NAID AAA for data destruction. Cost is about $15–40k to certify plus annual audits [ESTIMATE].

**Why chip-level harvesting does not work in the U.S.** [ESTIMATE: judgment, with PK technical facts]:
1. A whole tested module is worth more than its chips, because DDR4 RDIMMs have a ready resale market.
2. **Most high-capacity server RDIMMs use x4 die**, which only fit RDIMM/LRDIMM. Consumer UDIMMs and SODIMMs need x8/x16. The Shenzhen practice of re-mounting recycled chips on new consumer modules relies on x8/x16 die.
3. Reflow and reball stresses the die, and the result looks like counterfeit to AS6171 inspection.
4. U.S. labor at $25+/hr against Shenzhen rework labor.

**Conclusion: do module-level recertification, not die harvesting.**

### 6.4 Decommissioning volume and value [ESTIMATE]

Model in scratch script, section A:

`retired DRAM (GB/yr) = servers retired × GB/server`, then × U.S. share × open-market fraction × $/GB.

| Input | Low | Mid | High | Basis |
|---|---|---|---|---|
| Servers retired per year (≈ 2020–21 shipments, 5–6 year life) | 11.0M | 12.0M | 13.5M | Global server shipments of ~11–14M/yr [UNVERIFIED: PK] |
| DRAM per retired server (DDR4 era) | 256 GB | 384 GB | 512 GB | 2-socket servers with 8–16 RDIMMs of 16–64GB [ESTIMATE] |
| U.S. share | 35% | 40% | 45% | U.S. share of global hyperscale/server installed base [ESTIMATE] |
| Fraction reaching the open market (not reused internally, scrapped or bulk-exported) | 20% | 35% | 50% | Judgment; falling with CXL reuse [ESTIMATE] |

| Output | Low | Mid | High |
|---|---|---|---|
| Global DDR4 retiring | 2.8 EB/yr | **4.6 EB/yr** | 6.9 EB/yr |
| … as % of 2024 new DRAM bits (~32 EB = $97B ÷ $3/GB) | 9% | **14%** | 22% |
| U.S. retiring | 1.0 EB | 1.8 EB | 3.1 EB |
| U.S. open-market flow | 0.20 EB | **0.65 EB** | 1.56 EB |
| Value at 2023–24 prices ($0.8–1.2/GB) | $0.16–0.24B | $0.52–0.77B | $1.2–1.9B |
| **Value at 2026 estimated prices ($3–8/GB)** | $0.6–1.6B | **$1.9–5.2B** | $4.7–12.4B |
| Value in a 2028–29 glut ($0.5–1.5/GB) | $0.1–0.3B | $0.3–1.0B | $0.8–2.3B |

**Reading it:** this is a multi-billion-dollar U.S. flow at shortage prices, but it is (a) DDR4-only, so it fits only DDR4 platforms and CXL-DDR4 expanders, (b) shrinking as the DDR4 cohort ages out after about 2028, and (c) collapsing 70–90% in value in a glut [ESTIMATE].

### 6.5 What do decommissioned-server DDR4 RDIMMs sell for?

| Period | 32GB DDR4 RDIMM (2Rx4/2Rx8, 2400–3200) | 64GB DDR4 RDIMM | $/GB | Basis | Tag |
|---|---|---|---|---|---|
| **2023–24** (cycle trough) | ~$25–40 | ~$50–100 | ~$0.8–1.2 | Recalled eBay sold listings. Consistent with DDR4 8Gb contract bottom of $1.30 (Sep 2023) ([KED Global](https://www.kedglobal.com/korean-chipmakers/newsView/ked202310040013)). | [UNVERIFIED: PK] + [REPORTED] anchor |
| **2026 (estimate)** | **~$96–256** | **~$192–512** | **~$3–8** | Floor: 0.5 × consumer retail DDR4 (32GB DDR4-3200 ≈ $190 in Sep 2026, p1-market §8) ≈ $3/GB, using the 2023 used-to-new ratio of ~0.5. Ceiling: DDR4 8Gb **spot** at $21 (TrendForce board, 2026-08-03) to $44 (branded, 2026-08-31) per GB ([TrendForce](https://www.trendforce.com/price_dram.html); [BuySellRAM](https://www.buysellram.com/blog/ram-market-update/)). Momentum: DDR4 contract +24% over 3 months to Oct 2026 ([Guru3D](https://www.guru3d.com/story/ddr4-memory-prices-now-also-rise-as-dram-supply-shortages-intensify-through-2028/)). | [ESTIMATE] |
| **2026 observed (v3)**: trailing 12 months to Aug 2026 | **~$100–150** (+~335% YoY) | **~$250–370** (+~285% YoY) | **~$3.1–5.8** | amcompute realized-resale appraisal ([32GB](https://www.amcompute.com/appraisals/ddr4-32gb-rdimm); [64GB](https://www.amcompute.com/appraisals/ddr4-64gb-rdimm)). Backing out the YoY rise implies year-ago prices of $23–45 and $65–130, which matches the 2023–24 row. A vendor quotes 512GB of refurbished DDR4 at $2,300–5,500 ($4.5–10.7/GB asking) ([PCSP](https://pcserverandparts.com/news/refurbished-ddr4-server-memory-2026-server-ram-price-crisis/)). | [REPORTED] |
| **2026 DDR5 RDIMM, used (v3)** | — | **64GB DDR5: ~$890–1,200** (+~310% YoY); one eBay sale at $1,798 (2026-04-07) | ~$14–19 | [amcompute](https://www.amcompute.com/appraisals/ddr5-64gb-rdimm); [eBay](https://www.ebay.com/itm/198212795656). New 64GB DDR5 RDIMM was $1,630 on 2026-09-08 versus $720 in Jan 2026 ([ChinaFlashMarket](https://www.chinaflashmarket.com/pricecenter/chart/ems/100263)), so used sells at **~55–74% of new** | [REPORTED] |
| **2028–29 glut** | ~$16–48 | ~$32–96 | ~$0.5–1.5 | The DDR4 EOL premium unwinds, CXMT backfills, and the DDR4 installed base retires | [ESTIMATE] |

**Kill-check (one hour, $0):** pull 90 days of eBay *sold* listings for "32GB PC4-2933Y RDIMM" and "64GB PC4-3200AA RDIMM". If the median is below $2/GB, the recert arbitrage is weaker than estimated here. **(v3) Passed on secondary data:** realized prices are $3.1–5.8/GB. A direct eBay sold-listing pull is still worth an hour to get the current point rather than a 12-month range.

**(v3) Module price versus chip price.** Used DDR4 RDIMMs sell at **~7–28% of the DDR4 8Gb chip spot price per GB** ($21–44/GB) [ESTIMATE: arithmetic]. Most of the gap is die format: server x4 die do not fit the consumer x8/x16 boards that the spot price reflects (§6.3). The 2026 counterfeits built from re-soldered DDR4 chips show the gap attracts illicit harvesting.

### 6.6 Unit economics of a T0 U.S. test-and-resell shop [ESTIMATE]

Scratch script, section C. Assumptions, per 32GB RDIMM:
- Buy from ITAD lots at **60% of resale price**.
- Marketplace and payment fees **13.25%**; shipping **$5**.
- Test labor **6 min at $25/hr**.
- Failures written off at **3%**; returns **3%**.

| Price regime | Sale price | Contribution / module | Margin | Modules/month for $5k contribution |
|---|---|---|---|---|
| 2026 shortage (~$4.7/GB) | $150 | **$29.7** | **19.8%** | **~168** |
| 2026 high (~$8/GB) | $256 | $56.2 | 21.9% | ~89 |
| 2023–24 (~$1/GB) | $32 | $0.3 | 0.9% | n/a |
| Glut (~$1.25/GB) | $40 | $2.3 | 5.7% | ~2,181 |
| (v3) Observed 2026 low, 32GB at $100 (~$3.1/GB) | $100 | $17.2 | 17.2% | ~290 |
| (v3) Observed 2026 mid, 32GB at $125 (~$3.9/GB) | $125 | $23.5 | 18.8% | ~213 |
| (v3) Observed 2026, 64GB DDR4 at $250–370 | $250–370 | $54.6–84.6 | 21.9–22.9% | ~59–91 |
| (v3) Observed 2026, 64GB DDR5 used at $890–1,200 | $890–1,200 | $214–292 | ~24% | ~17–23 |

(v3) The observed rows rerun the same model with amcompute prices (`scratchpad/v3/recheck.py`; it reproduces the original $29.7 at $150) [ESTIMATE]. **Caution on the buy side:** Iron Mountain's ALM grew 88–92% YoY in 1H 2026 on decommissioning volume *and* pricing (§6.1). ITAD incumbents are keeping the repricing, so lots at 60% of resale are optimistic. DDR5 pays far more per module, but its supply is thin because DDR5 fleets are only 2–3 years old.

**Verdict:** profitable and founder-doable now (T0: about $8–20k of equipment plus $10–30k of inventory). **It dies in a glut** and has no moat: eBay competition and ITAD firms selling direct. It survives only if it becomes a **trust/provenance layer**: AS6081-grade test reports, §5949 non-CXMT certification, and serialized test data. That layer sells to buyers who need documentation (federal integrators, regulated industries) regardless of price level [ESTIMATE: judgment].

---

## 7. Memory test equipment: access and costs for a small shop

| Tier | Equipment | What it can do | Indicative cost | Tag |
|---|---|---|---|---|
| **Component ATE (new)** | **Advantest** T5503HS2 (DDR5/HBM-class) and T58xx memory platforms; **Teradyne Magnum** family | Wafer-sort and final test of DRAM die and packages at speed, massively parallel | **$1M–$5M+ per system**, plus handler and probe/load boards | [ESTIMATE: industry norms]. Model names: [UNVERIFIED: PK] |
| **Component ATE (used)** | Older Advantest T55xx-series DRAM testers; older Magnum | DDR2/DDR3/DDR4-speed component test. **Cannot run DDR5 at speed.** | **~$20k–$300k** used, plus a handler ($20–100k), load boards ($10–50k each) and test-program development ($50–250k) | [ESTIMATE] |
| **Test services** | ISE Labs (Fremont CA, ASE), Integra (KS), STS (CA), Golden Altos (CA), Trio-Tech (CA) | Outsourced program development, characterization, screening, burn-in | NRE **$20k–$200k** plus per-unit fees | [UNVERIFIED: PK] / [ESTIMATE] |
| **Module testers** | **CST Inc.** (Texas) DIMM testers (DDR4 and DDR5 RDIMM/UDIMM, with automation options); **Innoventions RAMCHECK LX** (Houston TX) with per-type adapters | Functional, pattern and SPD test of modules; fast pass/fail | RAMCHECK LX: **~$1.5–2k base plus ~$0.7–1.5k per adapter**. CST: **~$5k–$50k** depending on automation. | [UNVERIFIED: PK] (prices are recall) |
| **System-level test / burn-in** | Used DDR4 servers as test beds running **MemTest86 Pro** (PassMark, commercial), **memtest86+** (open source), **Google stressapptest** (open source), plus thermal chambers | Real-platform stress, which catches what bench testers miss (training and margin failures). This is what hyperscalers and ITADs actually use. | Used DDR4 2-socket server **~$300–1,500 each**; thermal chamber **$5–20k used** | [ESTIMATE] |
| **Counterfeit-detection lab (AS6171)** | X-ray, XRF, decapsulation, optical/SEM, curve tracer | Required to *sell into* aerospace and defense as an independent distributor | **~$300k–$1M+** in-house; or outsource at **$500–3,000 per lot** | [ESTIMATE] |

**Small-shop starter kit (T0), about $8–20k** [ESTIMATE]: RAMCHECK LX with DDR4 RDIMM/UDIMM adapters (~$4k), 4–6 used DDR4 servers as burn-in beds (~$3–6k), an ESD bench, labeling and a serialized test-report database (software the founder can build), plus a used thermal chamber (~$5k). **Component-level work (KGD test, package test) is out of reach without outsourcing.** Plan on ISE Labs-type NRE of $20–200k per die type.

---

## 8. Implications for American Memory: seeds for Phase 2 (with kill tests)

| Seed | Tier | Founder fit | Survives a 2028–29 glut? | First kill test (<$10k, <30 days) |
|---|---|---|---|---|
| **S1. Provenance-certified recovered DDR4 RDIMMs** (module-level test, serialized reports, §5949 non-CXMT attestation) | T0 | **High** (software for the test database, ops background) | **Partially.** The resale margin collapses; the certification and service layer survives. | eBay sold-listing pull (§6.5), plus quotes for two ITAD lots (Sesame, an R2 recycler) and a 50-module test run |
| **S2. §5949 compliance service for federal integrators** (BOM scan plus memory-provenance test) | T0–T1 | High | **Yes.** Compliance-driven, starts Dec 2027 | Interview 10 GSA/defense IT integrators; confirm the FAR §5949 implementing rule's status and effective date |
| **S3. Die-bank / LTB-as-a-service for mid-size industrial OEMs** (DDR3/DDR4 KGD or packaged, stored under controlled atmosphere, with DMSMS forecasting software) | T1 | Medium | **Yes.** Lifecycle-driven | Ask Rochester and Micross for die-bank pricing; interview five industrial OEMs about DDR4 EOL pain |
| **S4. U.S. hi-rel DDR MCM design house** (Taiwanese KGD packaged at Micross or QP Technologies) | T1–T2 | Low (needs packaging and SI engineers) | Yes | Get KGD quotes from Winbond and ESMT, and an MCM prototype quote from QP Technologies. **Likely kill: a 2–3 year qualification cycle breaks the 18-month revenue target.** |
| **S5. "Assembled in USA" DDR4/DDR5 module brand** | T1 | Medium | **No.** Assembly is ~1% of value, die is unobtainable, and Netlist patents loom. | Email SpecTek for wafer/KGD MOQ. **If there is no allocation, kill.** |
| **S6. CXL-DDR4 reuse appliance** (recovered RDIMMs behind a CXL controller) | T1–T2 | Medium | Partially | Hand off to the architecture branch (B). Check controller availability (Marvell Structera, Astera Leo), avoiding Chinese controllers if §5949 is the pitch. |

**Corrections to the mission premise (§3C):**
1. **Amkor AZ is logic 2.5D packaging, starting around early 2028.** It is not current capacity and not memory capacity. (v3) The plan is ~$7B, with ~$12B reported including phase 2, and is anchored by Apple, TSMC (10-year InFO/CoWoS deal) and NVIDIA ($1.5B). No HBM/DRAM packaging is confirmed [REPORTED].
2. **Kingston as the largest independent module maker, with U.S. assembly in Fountain Valley: confirmed** (v3). Fountain Valley capacity is ~550k modules/month (undated). Market share was 68.8% in 2023 and ~78% in 2021–22, on revenue of $13.5–14.2B [REPORTED / REPORTED-P].
3. **"Is there a U.S.-assembled premium?" Mostly no** for commodity modules. TAA does not require the U.S., the BAA preference covers only small buys, and the FTC limits the claim to "Assembled in USA." The premium sits in hi-rel memory and, from Dec 2027, in **provenance** (§4.3).
4. **"Recovered DRAM: is there a U.S.-legal version?" It already exists at module level.** Chip harvesting is not viable in the U.S. Hyperscalers are internalizing DDR4 reuse. The margin is roughly 20% now and roughly 0–6% in a glut (§6.6).
5. **U.S. HBM packaging:** SK hynix starts 2H 2028 to Q3 2029, and Micron after 2028. Neither is open to outside customers.

---

## 9. Verification checklist (run first when web access returns)

Ordered by decision weight. (v3) Status after Phase 1b: items 1, 4, 6 and 9 were checked through search snippets; see `verify_v3-backend.md`. Item 2 still needs the email. Items 3, 5 and 8 belong to `v1-policy`.
1. **eBay sold listings** for 32GB and 64GB DDR4 RDIMMs (2026 versus 2024): validates §6.5 and §6.6. **(v3) Done via amcompute:** $3.1–5.8/GB realized. A direct eBay pull is optional.
2. **SpecTek** wafer/KGD availability and MOQ (an email, not a search). **(v3) Still open:** no public terms were found.
3. **FAR rule implementing NDAA §5949**: status and effective date; whether it covers subcomponents such as DIMMs inside servers.
4. **Amkor Peoria:** current investment ($2B or $7B), production date, and confirmed customers (Amkor IR, NIST CHIPS award page).
5. **Natcast / NSTC / NAPMP** status after Aug 2025; whether the Tempe piloting facility proceeds.
6. **Kingston's** TrendForce module-house ranking share (latest annual release) and U.S. manufacturing confirmation.
7. **Netlist** patent status (CAFC/PTAB outcomes 2025–26; any ITC case) and the PMIC-patent scope for DDR5 RDIMMs.
8. **TAA threshold** value for 2026 (FAR 25.402) and BAA evaluation factors (FAR 25.105).
9. **Iron Mountain ALM / ITRenew** revenue and volumes (Iron Mountain 10-K); Sims SLS restructuring status.
10. **Microsoft and Google** server and component reuse percentages (sustainability reports 2025–26); GreenSKU / CXL-DDR4 reuse deployment status.
11. **SkyWater Florida** packaging status and the Deca M-Series production date.
12. **Integra Technologies** Bel Aire expansion: did it get CHIPS money?
13. **Micross** ownership, sites and DRAM MCM product list.
14. Module tester prices (CST, Innoventions) from vendor quotes.
15. Global server shipments for 2020–21 (TrendForce/IDC press releases), to firm up the §6.4 inputs.
