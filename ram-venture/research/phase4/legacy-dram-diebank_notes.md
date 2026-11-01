# DD7 — Authorized-Aftermarket Legacy DRAM Die Bank (+ hi-rel MCMs): research notes

Agent: `p4-legacy-dram-diebank` · As of 2026-11-01 · Round 2 · Anchor **C-91** (title-taking authorized-aftermarket die bank); folded **C-65** (hi-rel x72 ECC DDR4/LPDDR4 MCM). MOONSHOT candidate (T2, no horizon limit).
Model: `models/legacy-dram-diebank.py` (exit 0); output: `research/phase4/legacy-dram-diebank_model_output.md`.
Sources: `research/sources/p4-legacy-dram-diebank.jsonl` (77 entries). Assumptions: `research/assumptions/p4-legacy-dram-diebank.md`.
Method note: 30 WebSearch calls (the full quota). All 3 WebFetch attempts failed DNS (supplychainconnect.com, electropages.com, dsp.dla.mil). **Every web fact below is snippet-grade: [REPORTED] at best, and nothing is [VERIFIED].** Prices for hi-rel memory, OCM authorization terms, die-bank storage fees and OSAT NRE are **not public**. Where a number has no source it is tagged [ESTIMATE] and pointed to the model.

---

## 0. Verdict

**The MOONSHOT test fails for this founder. Downgrade the bundle to a side line, and kill it as a venture unless the 30-day experiment in §11 passes on all three tracks.**

Three separate questions (mission rule 2):

| Question | Answer | Why |
|---|---|---|
| **POSSIBLE?** | **Yes (TRL 9)** | Rochester banks >10B die and re-makes OCM parts under licence. Micross stores die and wafers in nitrogen for 20+ years. Teledyne e2v, Mercury and Frontgrade ship x72 ECC DDR4 MCMs (§1, §4, §5). |
| **PROFITABLE?** | **For incumbents, yes. For a new entrant, no in BASE.** | The staged plan needs **$8.11M** of outside capital and reaches **$2.49M** of year-10 revenue. At 1.5× revenue that is **0.46× the capital** in BASE, **0.36×** in GLUT and **0.28×** in SEVERE (`models/legacy-dram-diebank.py` §6). |
| **DOABLE BY THIS FOUNDER?** | **Only the wedge, and the wedge is a side line** | The part-time wedge (managed die-bank programs plus channel commissions) reaches **$42.6k recurring ARR at m36** in BASE ($33.5k GLUT, $26.4k SEVERE). It never pays the founder (model §4). |

**Five findings drive the verdict:**

1. **The DFARS moat is real, but it rarely binds for commodity DRAM.**
   - DFARS 252.246-7008 ranks authorized aftermarket manufacturers ahead of independents (verified by Phase-2 agent E).
   - But JEDEC DRAM is substitutable. DSPO's 2024 DMSMS case mix shows **2,809 "simple substitute" resolutions against 1,268 life-of-need buys and only 24 complex substitutes**, with **99.3% resolved without redesign** ([DSPO 2024-08-08](https://www.dsp.dla.mil/Portals/26/Documents/Conference/2024%20Briefings/Day%203%20-%20August%208/Brown%20-%20Program%20Update.pdf), via snippet) [REPORTED-P].
   - A banked DRAM die only earns a premium where the die is *locked*: inside a hi-rel MCM, a DO-254 avionics board or an FDA-validated device.
2. **The firms exiting DRAM don't authorize startups, and the firms that might authorize aren't exiting.**
   - Samsung, SK hynix and Micron are the ones issuing DDR3/DDR4/LPDDR4 EOL notices. Micron's precedents are e2v (2013) and ATP (2018), both established houses.
   - The Taiwanese specialty makers are *beneficiaries* of the shortage. Winbond's capacity is sold out through 2027, and its customers are asking for LTAs to 2030 ([TrendForce 2026-08-07](https://www.trendforce.com/news/2026/08/07/news-winbond-says-customers-seek-ltas-through-2030-adata-expects-even-tighter-dram-supply-in-2027/), via snippet).
   - Winbond is moving DDR4 8Gb to 16 nm for industrial customers ([DigiTimes 2025-12](https://digitimes.com/tag/winbond/001585.html), via snippet).
   - So no EOL-driven authorization from them is likely before the glut [ESTIMATE: judgment].
3. **A die bank bought at peak prices or normal prices both lose, because U.S. low-volume package and test is a fixed ~$11.5/die.**
   - **Bought in BASE at m20** (2028-06, $16.80/GB): unit GM **39.6%**, 10-year IRR only **2.6%**.
   - **Bought in GLUT:** unit GM **−1.1%**, IRR **−32.8%**.
   - **Bought at the ~$3/GB long-run price:** unit GM **−93%** (model §3).
   - **Scale is the moat.** At Rochester-scale pull costs (~$2/die) the unit GM recovers to 40%. A 10-wafer bank still cannot pay back a $120k package/test NRE.
4. **The MCM carries the whole venture, and it walks into heritage incumbents.**
   - The x72 MCM's unit cost is ~$490 at 2026 die prices and ~$344 at long-run prices, so GM at a $900 ASP is 46–62%.
   - **Venture-grade returns (≥3× capital) need about 4 design-ins a year at ~1,000 units each** (4.0×), or 6 a year at 600 units (3.6×). The modelled 2 a year at 300 units returns 0.46× (model §6 grid).
   - The incumbents are Teledyne e2v (DDR4T04G72, shipping since 2020) and Teledyne HiRel (16GB DDR4, 2025-07-24) ([Business Wire](https://www.businesswire.com/news/home/20250724928807/en/Teledyne-HiRel-Semiconductors-Announces-High-Density-16-GByte-DDR4-Module)); Mercury (rad-tolerant 8GB, 2022-11-08); and Frontgrade (18GB, 2024-11-05) ([Frontgrade](https://frontgrade.com/news/frontgrade-unveils-highest-density-available-rad-tolerant-18-gb-ddr4-memory-space)).
5. **The "Rochester-scale" ceiling is not a DRAM ceiling.**
   - Rochester's estimated $200–500M of revenue comes from 70+ OCMs and >20,000 device types.
   - Its only public DRAM program is a *distribution* partnership with Intelligent Memory (2024-03-25), not DRAM die re-manufacture ([Business Wire](https://www.businesswire.com/news/home/20240325645193/en), via snippet).
   - The DMSMS-tracked memory life-of-need market sanity-checks at **$6–25M/yr** [ESTIMATE, model §6].

**Cycle-proofing (rule 6).** "Lifecycle-driven, so glut-proof" is only partly true:
- The bank **dies** in GLUT and SEVERE: no bank passes the model's ≥20% unit-GM purchase rule.
- The MCM mostly **survives**: die cost falls and only NewSpace demand softens (design-ins ×0.85).
- The service wedge **shrinks 21–38%** (m36 ARR $33.5k / $26.4k against $42.6k).

**Recommendation.** Move the bundle off the MOONSHOT slot. Keep the founder-doable piece, managed die-bank programs on Micross-type consignment vaults, as an optional add-on to DD2's LTB-service side line. Revisit the MCM only if a hardware co-founder with hi-rel heritage and ~$5M appears, and §11 track B shows locked-die demand.

---

## 1. Q1 — How OCM authorization for aftermarket manufacturing works

### 1.1 The models that exist (all [REPORTED], snippet-grade)

| Model | Who | What the OCM hands over | Evidence (dated) |
|---|---|---|---|
| **Licensed re-manufacture** (Authorized Aftermarket Manufacturer, AAM) | Rochester Electronics (Newburyport MA) | Design/test archive, tooling, remaining wafers and die. Parts are sold **under the OCM part number with the OCM's approval**. A "low touch" path needs OCM engineering after the archive transfer | Rochester brochure: licensed to make parts the OCM has dropped, using "information and technology transferred directly from the OCM"; >20,000 device types made, capability for >70,000; **>12B die in stock**; ISO-7 storage ([electronica brochure](https://exhibitors.electronica.de/download/1121_11_2_2823_2_1_809/electronica_re_solutions-brochure_en_flipbookpdf.pdf); [GlobalSpec](https://www.globalspec.com/Supplier/Profile/RochesterElectronics)). >10B die, some from 1968 ([Electronic Specifier](https://www.electronicspecifier.com/around-the-industry/the-worlds-largest-wafer-bank-has-tripled-in-size-at-rochester-electronics)). "Authorized by over 70" OCMs (ADS directory, cross-ref p3-audit-13) |
| **Definition** | ERAI glossary | An AAM is authorized by the OCM to make and sell replacement parts, usually after the OCM stops. Parts come from transferred OCM material or OCM tooling/IP, and are marked so they are not mistaken for OCM parts | [ERAI](https://www.erai.com/glossary/Authorized%20Aftermarket%20Manufacturer/) |
| **Authorized distribution** (the lighter tier) | Mouser, Flip, Sourceability | A franchise agreement. SAE **AS6496** is the counterfeit-avoidance standard for authorized distributors (AS6081 covers independents) | [RF Essentials](https://rfessentials.com/resources/rf-glossary/as6496/); Mouser was the first AS6496-accredited distributor in 2018 ([Mouser](https://www.mouser.in/newsroom/publicrelations_mouser_as6496_certification_2018final)) |
| **Wafer banking plus hi-rel re-packaging under a DRAM OCM's longevity program** | e2v (now Teledyne) for Micron | Micron SDR/DDR portfolio extended through e2v's SLiM program: wafer banking, re-engineering, hi-rel test and packaging, supplementing Micron's Product Longevity Program | 2013-08-13 ([GlobeNewswire](https://www.globenewswire.com/news-release/2013/08/13/1235643/0/en/e2v-aerospace-and-defense-Inc-Launches-a-Program-to-Provide-Extended-Life-for-Certain-SDR-and-DDR-Memory-Products-of-Micron-Technology-Inc.html?print=1)). Micron PLP launched 2011 ([NBC mirror](https://www.nbcnews.com/id/wbna42901258)) |
| **Module continuity** (no die transfer) | ATP for Micron DDR2 | ATP builds Micron-equivalent DDR2 modules to Micron's specs and validation after Micron's EOL | 2018-10 ([PR Newswire](https://prnewswire.co.uk/news-releases/micron-and-atp-to-collaborate-on-ddr2-continuity-program-694766761.html)) |
| **Consignment / white-label vault** | Micross EDSP | The customer keeps the customer relationship. Micross holds inventory for an **annual carrying fee** and processes and packages on demand. A pre-pay variant also exists. Die banks can come from a single diffusion run | [Micross long-term storage](https://www.micross.com/sustainment-solutions/program-sustainment-management/long-term-die-and-wafer-storage); [EDSP flyer](https://www.micross.com/uploads/806a7ab8-585d-4e8b-8608-4464e5cadfd4/EDSP_Rev_1_WEB.pdf). No rates are published |

### 1.2 What wins an authorization

No OCM publishes its criteria, so this is [ESTIMATE: synthesis of the precedents above].

1. **Capital to take title** of the remaining wafers, WIP and finished goods at EOL.
2. **Test capability.** That means at-speed memory ATE programs, which are DRAM-specific and expensive.
3. **A quality system.** AS9120B and AS6496 for distribution; **MIL-PRF-38535 QML** for hi-rel re-manufacture. Lansdale is a DSCC-approved QML manufacturer ([Military & Aerospace directory](https://militaryaerospace.com/directory/components-power-electronics-sensors/integrated-circuits-digital-a-d-converters/company/14060051/lansdale-semiconductor-inc)).
4. **A defense and aerospace channel** that keeps the OCM's customers served without the OCM's cost.
5. **Longevity.** The OCM's brand rides on the partner for 10–20 years.

A part-time founder with $40k has none of the five. That is why all three Phase-3 scorers gave founder fit a 1.

### 1.3 Has a small firm ever won one?

- **Flip Electronics** is the best precedent.
  - It has been an authorized distributor of obsolete parts since **2015** and holds **22 OCM relationships** and 20,000+ SKUs.
  - On **2023-02-21** it bought **Resurgent Semiconductor**, a ~30-person licensed EOL manufacturer, renamed Flip Manufacturing Services ([Business Wire](https://www.businesswire.com/news/home/20230221005100/en); [I-Connect007](https://iconnect007.com/article/146219/flip-electronics-unifies-manufacturing-operations-under-new-flip-manufacturing-services-brand/146216/aep)).
  - It is PE-backed by O2 Investment Partners ([PrivSource](https://www.privsource.com/acquisitions/deal/wySWZM)).
  - Resurgent's model is to take over the foundry arrangement, or buy and store the wafers when a line is decommissioned ([Electropages podcast](https://www.electropages.com/the-hub/podcast/flip-electronics-resurgent-acquisition-solving-obsolescence-challenges-semiconductors), via snippet).
  - **The lesson:** a newer firm *can* win authorizations, but it took ~8 years, private equity and an acquisition. No Flip DRAM line was found.
- **Lansdale Semiconductor.** Founded in 1964 on Philco-Ford lines, it moved to Phoenix in 1976 after buying a Motorola line. It is licensed for "thousands of ICs" and supplies >3,000 parts ([Lansdale](https://lansdale.com/mission_statement.php)). It is small, but old.
- **Intelligent Memory is adding channel partners in 2026.** It signed Sourceability (2026-10-06) and Flip to reach DDR3/DDR4 EOL customers ([Evertiq](https://evertiq.com/design/2026-10-06-intelligent-memory-signs-sourceability-as-global-distributor)). So a **rep or distribution agreement** with a long-lifecycle DRAM OCM is the realistic first relationship. Aftermarket-manufacturing authorization is not.

### 1.4 What the Taiwanese DRAM makers require

No public aftermarket-authorization program was found for Winbond, ESMT, Etron or Nanya [UNVERIFIED; kill-experiment track A].

What *was* found:
- **ESMT** has KGD versions of its full DRAM range: DDR3, DDR4 and LPDDR ([ESMT](https://www.esmt.com.tw/cn/Applications/DRAM-Memory)). A distributor showed 175 ESMT 4Gb DDR4 KGD on 2026-05-26 ([Suntsu](https://suntsu.com/product/integrated-circuits/memory/kgd-256mbx16-ddr4-1-2v/)). ESMT will focus its PSMC allotment on DDR2 after Winbond's DDR2 exit ([NetEase citing TrendForce, 2026-06](https://c.m.163.com/news/a/L01J8VNT05119RSA.html)).
- **Etron** lists DDR3 KGD, with no terms ([Etron](https://etron.com/zh-hans/kgdm-pl/ddr3-sdram-zh-hans)).
- **Winbond** is sold out and extending (§0).

The specialty makers sell KGD to SiP makers. That makes them a **die source for the MCM**, not a source of aftermarket authorization.

### 1.5 The four wedge routes the brief asked about

| Route | Verdict | Evidence |
|---|---|---|
| Narrow-family OCM authorization | **Unlikely before the glut**: the makers able to authorize are not exiting, and the exiters have only authorized established houses | §1.3–1.4 |
| DoD DMSMS contract | **Possible later via SBIR**, which needs a >50%-employed PI. DLA funded legacy-part re-creation by SBIR Phase II on 2026-06-18 | §6 |
| Sub-arrangement with Rochester or Micross | **Yes, as a white-label front end on Micross consignment**. This is the only route open to a part-time founder in year 1 (Plan A, line L1) | Micross storage page |
| Buy a small aftermarket manufacturer or test house | **Feasible only with a full-time founder plus ~$410k of outside equity, and only in BASE** (DSCR 1.50; 0.85 GLUT; 0.45 SEVERE) | Model §7; Flip/Resurgent precedent |

---

## 2. Q2 — Demand

**DMSMS volume and resolution mix**
- DSPO's 2024 case outcomes: **4,143 no issue, 2,809 simple substitute, 24 complex substitute, 1,268 life-of-need buy**, plus redesigns. **99.3% were resolved without redesign** (DSPO 2024-08-08, above) [REPORTED-P].
- Navy NSWC Crane: obsolescence costs "hundreds of millions of dollars each year" ([NAVSEA](https://www.navsea.navy.mil/Portals/103/Documents/NSWC_Crane/SD-18/PDFs/Resources/ResourcesDMSMS.pdf)). A 2007 DSPO brief put DMSMS resolution NRE at **$1–10B/yr** ([DSPO 2007](https://www.dsp.dla.mil/Portals/26/Documents/Publications/Conferences/2007/2007%20Briefs/2007-DSPConferenceBriefings-Melnikow.pdf)). That figure is dated.
- **GIDEP:** no count of notices per year was found. The 2024 briefing charts "batch match requests" of up to ~14M/yr ([NDIA/GIDEP 2024-10](https://ndia.dtic.mil/wp-content/uploads/2024/systems/Thurs_IPM_1860112_Olness.pdf)) [gap].
- **Sanity ceiling** [ESTIMATE, model §6]: if ~10% of DSPO-tracked cases are memory, that is ~127 memory life-of-need buys a year. At $50–200k each, that is **$6.3–25.4M/yr**.

**Legacy DRAM EOL notices, 2025–26**

| Maker | Event | Source |
|---|---|---|
| Micron | DDR4/LPDDR4 EOL notices to PC/DC customers (Jun 2025); continues for auto/industrial/networking | [TrendForce 2025-06-13](https://www.trendforce.com/news/2025/06/13/news-micron-confirms-ddr4-phase-out-with-eol-notices-reportedly-hints-at-price-hikes-ahead/) |
| Micron | **PCN 36146** (2025-09-30): LPDDR4 8Gb SDP x32 non-auto, **last order 2026-03-30, last ship 2026-09-30**; replacements may not be drop-in | [Mouser PCN](https://www.mouser.com/PCN/Micron_Technology_PCN_36146.pdf) [REPORTED-P] |
| Samsung / SK hynix | DDR4 exits pushed into 2026 | [TrendForce 2025-09-02](https://www.trendforce.com/news/2025/09/02/news-samsung-sk-hynix-reportedly-delay-phase-out-to-2026-as-ddr4-becomes-unexpected-cash-cow/) |
| DDR3 | Samsung stopped Q2 2024, SK hynix end-2023; Micron produces past 2026; Nanya and ISSI second sources; LTB decisions within 18–24 months for many industrial and medical designs | [GlobX 2026](https://globx.eu/blog/supply-chain-insight/ddr3-last-time-buy-2026) |
| Advantech (module OEM) | DDR3 module EOL with LTB **2026-11-30** (another version says 2026-06-30) | [Advantech](https://www.advantech.com/en-us/resources/news/【phase-out】selected-d3-dram-module-part-numbers-and-ddr3-dram-module-eol) |
| Industry | Vendors exiting DDR4 by end-2026/early-2027 (TrendForce via Sourceability); record EOL rates in 2025, with 2026 likely matching | [Sourceability](https://sourceability.com/post/how-ddr4-end-of-life-threatens-long-term-designs); [Z2Data 2026](https://www.z2data.com/insights/how-chip-obsolescence-is-making-dmsms-worseand-where-we-re-headed-in-2027) |

Renesas makes no commodity DRAM. Its 2025–26 memory EOLs are serial EEPROM (cross-ref research/sources/A2.jsonl) and are not relevant here.

**Counter-evidence: authorized DDR4 supply is being *extended*, which shrinks the window for aftermarket supply**
- **Micron Manassas.** 1-alpha DDR4/LP4 in production since 2026-05-22. It quadruples DDR4 wafer supply, targets defense, aerospace and medical, and expects qualified output by end-2026 ([Micron](https://micron.gcs-web.com/news-releases/news-release-details/micron-advances-made-america-memory-manufacturing-expansion); [Potomac Local](https://www.potomaclocal.com/?p=250463)).
- **ISSI** supports DDR4 and LPDDR4/4X through at least 2038 ([AMD/ISSI](https://www.amd.com/content/dam/amd/en/documents/products/adaptive-socs-and-fpgas/technologies/issi-memory-solution-brief.pdf)).
- **Intelligent Memory** brings its 32Gb DDR4 back from Q3 2026 ([IM](https://www.intelligentmemory.com/company/articles-news-events/intelligent-memory-to-exhibit-at-embedded-world-2026)).
- **Viking** cites Nanya and Winbond as the basis of long-term DDR4 supply ([Viking 2025-07](https://www.vikingtechnology.com/wp-content/uploads/2025/07/Viking-Technology-DDR4-Module-Support-Plans.pdf)).

**What buyers pay, and order sizes**
- **Authorized aftermarket premium:** ~1.5–5× the original price; brokers up to 10×+ in shortages. This is research/phase1/us_backend.md §5.3, itself an [ESTIMATE]. **No primary price was found this session.**
- **Hi-rel MCMs are RFQ-only.**
  - Avnet lists Teledyne e2v DDR4T08G72MZR2BE3 at **MOQ 25** and DDR4T04G72AZR1B-N1 at **MOQ 5**, with no price ([Avnet](https://www.avnet.com/americas/manufacturers/m/c/teledyne-e2v/memory)).
  - Findchips shows no pricing ([Findchips](https://www.findchips.com/search/ddr4t)).
- **Order sizes:**
  - Mercury took an **$8.2M single order for SWaP-optimized memory** for a C2I application ([ICN](https://intelligencecommunitynews.com/mercury-systems-receives-8-2m-order-for-swap-optimized-memory-for-c2i-application/)).
  - Typical DMSMS life-of-need buys: [UNVERIFIED]; the model assumes $50–200k.

---

## 3. Q3 — Capital

| Item | Number | Basis |
|---|---|---|
| LTB wafer value, DDR4 8Gb, 300 mm | ~1,251 good die/wafer; ~$20k/wafer at $16/GB; 25-wafer lot **$75k (DDR3) to $550k (DDR4/DDR5)** | research/phase1/us_backend.md §4.2 [ESTIMATE] |
| Model bank (10 wafers, wafer price = 0.75 × packaged $/GB) | m20 BASE **$158k** of die + $120k NRE = **$278k per part family**; GLUT $76k + NRE; SEVERE $19k + NRE | Model §3 [ESTIMATE]. E-07 used ~$0.6M for ~30 wafers |
| Die-bank storage | Micross: annual carrying fee, no rates; model **3%/yr of basis, minimum $5k/yr** | [Micross](https://www.micross.com/sustainment-solutions/program-sustainment-management/long-term-die-and-wafer-storage) [ESTIMATE rate] |
| Package/test NRE at a U.S. OSAT | No public pricing (QP Technologies quotes only); model **$120k** for the first family, $40k for later ones | [AnySilicon/QP](https://anysilicon.com/vendors/qp-technologies/) [ESTIMATE] |
| Per-die pull cost (U.S., low volume) | Re-probe $1.50 + package $6.00 + test $4.00, at 95% yield ≈ **$12.1 per good die** before the die | [ESTIMATE]; the largest single sensitivity on bank IRR after price |
| Qualification | MIL-PRF-38535 Class Q/N steps confirmed ([NSWC Crane SD-18](https://www.navsea.navy.mil/Home/Warfare-Centers/NSWC-Crane/Resources/SD-18/Products/Microcircuits/Facility-Assessment-Quality/)); **no cost found**. Model: AS9120B $35k + $8k/yr; MCM qual inside the **$1.4M NRE** | [ESTIMATE] |
| Inventory carrying risk | Bank IRR **2.6%** (BASE, bought m20) / **−32.8%** (GLUT) / n/a (SEVERE); **6.5%** if bought at the 2026 peak; **unit GM −93%** if bought at the $3/GB long-run price | Model §3 |
| Hi-rel MCM | NRE $1.4M over 18 months; unit cost **$490** (2026 die) → **$344** (long-run die); 1.0 design-in of 300 units/yr × 8 years repays the NRE in gross profit | Model §3; C-65 card ($457) |

**Why the bank fails in a glut.** The sale price is anchored to the part's price at EOL, but the U.S. pull cost does not fall. The broker market and cheap substitutes also compress the multiple. So a cheaper LTB wafer is *not* a net gain at startup scale. That contradicts the C-91 card's "a glut cheapens LTB wafers" upside.

---

## 4. Q4 — Competitors

| Competitor | What it does in legacy/hi-rel DRAM | Scale or price evidence | Tag |
|---|---|---|---|
| **Rochester Electronics** (Newburyport MA) | AAM; >10–12B die; >20,000 device types; legacy DRAM through an Intelligent Memory distribution partnership (2024-03-25); legacy NAND through SkyHigh (2023) | Private. Revenue estimates **$200–500M** ([Similarweb](https://www.similarweb.com/company/rocelec.com)), $275.3M ([Bitscale](https://bitscale.ai/directory/rochester-electronics-llc)), $310M ([Clodura](https://www.clodura.ai/directory/company/rochester-electronics-llc)). ~864 staff in 2025 ([Revelio](https://www.reveliolabs.com/companies/rochester-electronics/employees)), ~850 ([Supply Chain Connect](https://www.supplychainconnect.com/rankings-research/whitepaper/55290409/top-50-electronics-distributors-2025-rochester-electronics)), ~711 in Jun 2026 ([LeadIQ](https://leadiq.com/c/rochester-electronics-llc/5a1d83d524000024005e57dd/employee-directory)) | [REPORTED], modeled |
| **Micross** (FL/NC) | EDSP die sustainment; N2 storage 20+ years; ~15M die stored at Apopka; DMEA Trusted; IBAS RESHAPE award (ceiling **$134.3M**, $45.6M obligated) | [Apopka](https://www.micross.com/about-us/facilities-and-locations/apopka-fl); [I-Connect007](https://iconnect007.com/article/138727/1343m-dod-contract-expands-micross-advanced-interconnect-osat-capabilities-in-the-us/138724/aep). Both a partner (vault, OSAT) and a competitor | [REPORTED] |
| **Flip Electronics / Flip Manufacturing Services** | 22 OCMs; licensed EOL manufacturing (ex-Resurgent); IM distribution partner | PE-backed; Resurgent ~30 staff | [REPORTED] |
| **Lansdale Semiconductor** (Phoenix) | Licensed aftermarket ICs, QML; no DRAM found | >3,000 ICs | [REPORTED] |
| **Teledyne e2v / Teledyne HiRel** | DDR4T04G72 4/8GB x72 rad-tolerant MCM (Micron die, since 2020; NASA Level 1/ECSS Class 1 per C-65 card); 16GB DDR4 TDD416Y12NEPBM01 (2025-07-24); Micron life-extension program since 2013 | **RFQ-only**; Avnet MOQ 5–25 | [REPORTED] |
| **Mercury Systems** | Rad-tolerant 8GB DDR4 (2,666 Mb/s, −55 to 125 °C, 13×20 mm; 2022-11-08); 16GB 1Gx72 military DDR4 with 100% burn-in | **$8.2M** memory order; no unit price ([SIJ](https://www.signalintegrityjournal.com/articles/2899-mercury-introduces-radiation-tolerant-8gb-ddr4-memory-component-to-power-enhanced-edge-processing-for-space-missions); [datasheet](https://www.mrcy.com/siteassets/product-datasheets/ddr/high-density-secure-memory-16gb-ddr4-builtsecure.pdf)) | [REPORTED] |
| **Frontgrade** | 18GB (2Gx72) rad-tolerant DDR4 (2024-11-05) | No price | [REPORTED] |
| **Data Device Corp; 3D Plus (HEICO)** | Rugged/space DDR modules (C-65 card) | Nothing found this session | [UNVERIFIED] |
| **Intelligent Memory** | Long-lifecycle DRAM OCM (SDRAM–DDR5, LPDDR4x, ECC DRAM); 32Gb DDR4 back Q3 2026; new distributors in 2026 | — | [REPORTED-P] |
| **Alliance Memory** (Kirkland WA) | Fabless pin-for-pin legacy DRAM; up to ~10 years of support | Cross-ref p3-audit-09 | [REPORTED] |
| **ISSI** | DDR4/LPDDR4/4X through ≥2038 | — | [REPORTED-P] |
| **Micron Manassas** | U.S.-made long-lifecycle DDR4/LP4 since 2026-05-22; Strategic Customer Agreements with Ford, GM and Tier-1s (01_LANDSCAPE) | >$2B; 4× DDR4 wafer supply | [REPORTED] |
| **Winbond, Nanya, ESMT, Etron** | KGD and long-lifecycle DDR3/DDR4; Winbond 16 nm DDR4 8Gb for industrial (2026 shipment) | Winbond sold out through 2027 | [REPORTED] |

**Why we would not win.**
- On the bank, Rochester and Micross already hold the vaults, the OCM relationships and the in-house pull economics.
- On the MCM, Teledyne, Mercury and Frontgrade hold the heritage, and the same Winbond/ESMT KGD is open to all of them.
- The only defensible angle is a cheaper, U.S.-assembled, screened-but-not-Level-1 DDR4/LPDDR4X MCM for NewSpace and rugged industrial buyers (C-65 verify note). No evidence was found that buyers will pay for it [UNVERIFIED].

---

## 5. Q5 — Die storage physics

- **Standards.** IEC/BS EN **62435-5** covers long-term storage (>12 months) of die and wafers, including bumped and RDL wafers ([BSI](https://knowledge.bsigroup.com/products/electronic-components-long-term-storage-of-electronic-semiconductor-devices-die-and-wafer-devices)). **GEIA-STD-0003B** (revised Dec 2025) covers long-term storage of dice, wafers, packaged parts and assemblies, and *does not address built-in failure mechanisms* ([SAE](https://saemobilus.sae.org/standards/geiastd0003b-long-term-storage-lts-electronic-devices)).
- **Manufacturer limits.** Infineon gives **36 months for unsawn wafers in an N2 cabinet** (15–30 °C), **6 months for sawn wafers on film frame** and 36 months for die in waffle packs ([Infineon](https://www.infineon.com/dgdl/Storage_of_Products_Supplied_by_Infineon_Technologie.pdf)). Central Semiconductor specifies inert gas, dry air or N2 at RH 7–30% beyond one month ([Central](https://media.digikey.com/pdf/Data%20Sheets/Central%20Semiconductor/Wafer_Chip_Handling.pdf)).
- **Long-horizon practice.** Micross claims 20+ years in N2 and "40+ years of viable die storage". Rochester holds die back to 1968. A Rochester study found packaged parts stored up to **17 years** kept their functionality and connection integrity ([DigiKey blog](https://www.digikey.com/en/blog/testing-confirms-that-component-reliability-remains-with-proper-long-term-storage)).
- **Mechanisms and what they imply** [ESTIMATE: standard reliability physics, no new data this session]:
  - Unpowered die see none of the wear-out mechanisms that need bias and current: no BTI, HCI, TDDB or electromigration.
  - The storage risks are bond-pad Al oxidation and contamination (wire-bondability), moisture and ionic contamination, and ESD. Film-frame adhesive ageing is also a risk, so **bank unsawn wafers** and singulate at pull.
  - DRAM retention and refresh behaviour is a property of the design, not of storage age.
- **Re-qualification at pull.** Re-probe the wafer on memory ATE, run sample bond pull/shear, and build a package qualification lot for hi-rel. **The often-missed DRAM risk is the obsolescence of the test program and tester**: legacy DDR3 test programs live on ageing memory ATE. This is why the model carries $120k of first-family NRE.
- **Yield of aged die:** no measured data found [gap]. The model assumes 95% at pull.
- **Rule 1 status:** SUPPORTED by industry practice at scale. TRL 9.

---

## 6. Q6 — Funding

| Program | Fit | Evidence |
|---|---|---|
| SBIR/STTR (reauthorized to 2031-09-30) | Phase I/II for MCM qualification or legacy-part re-creation. **The founder cannot be SBIR PI with a day job**; STTR with a university PI, or a full-time hire after Stage-1, is the route | 01_LANDSCAPE §0 #9. Precedent: **DLA Phase II SBIR to Phoenix Semiconductor (2026-06-18)** to design, fab and validate a replacement for the Signetics 82S100 (Nimitz-class) ([SamSearch](https://samsearch.co/government-contracting-news/dla-awards-phase-ii-sbir-contract-to-phoenix-semiconductor-for-legacy-chip-solutions-118673)) |
| DoW obsolescence money | Reverse engineering of obsolete parts: ~$1.8M over two years to Great Plains Innovation Network (awarded 2025-08-27) | [war.gov](https://www.war.gov/News/Releases/Release/Article/4401952/dow-addresses-material-obsolescence-through-reverse-engineering-training) |
| IBAS | Flows to incumbents (Micross RESHAPE, $134.3M ceiling) | above |
| DPA Title III | $16M to BAE for rad-hard components (2026-07-02); five DPA III awards totalling $102.6M in FY2026. **LOW confidence: unofficial repost** | [Google Groups repost](https://groups.google.com/g/world_wide_with_god_minstry4/c/LGphnGE611Y) |
| DRAM-specific SBIR topic | **None found** | [gap] |
| State programs | Not searched (quota) | [gap] |
| Strategic and PE money | PE backs EOL roll-ups (O2 → Flip). Strategic acquirers or partners: Rochester, Micross, Flip, Teledyne, Mercury, Frontgrade, HEICO | §1.3 |
| Acquisition targets | Small licensed manufacturers or test houses of the Resurgent type (Resurgent itself now belongs to Flip). U.S. hi-rel test/OSATs: Integra (DMEA-trusted for test), QP Technologies (Promex division), Golden Altos. **Ownership and availability not checked** | Model §7 at Resurgent scale: price **$4.5M**, SBA loan $3.6M, debt service $598.5k/yr, **DSCR 1.50 BASE / 0.85 GLUT / 0.45 SEVERE**, outside equity **$410k**, founder full-time |

---

## 7. First ten customer candidates

None has been contacted. Names come from 2026 solicitations and round-1 lists. The "line" column maps each to the model.

| # | Candidate | Type | Trigger / evidence | What they would buy | Line |
|---|---|---|---|---|---|
| 1 | **NAVSUP Weapon Systems Support** | Navy DMSMS buyer | DMSMS health-assessment requirement, 120-day reports, responses due 2026-06-18 ([Cleat](https://www.cleat.ai/government/contracts/dmsms-and-obsolescence-management-reporting-sqml)) | LTB sizing and managed die-bank planning as a subcontractor to the awardee | L1 |
| 2 | **Tobyhanna Army Depot** (PA) | Army depot | Subcontract to mitigate obsolete microelectronics in legacy systems, responses due 2026-08-07 ([Cleat](https://www.cleat.ai/government/contracts/dmsms-mitigation-and-reverse-engineering-gbao)) | Memory LTB/aftermarket sourcing plan | L1 |
| 3 | **NAWC China Lake** | Navy test center | Sole-source FFP memory upgrade, SPE7M5-26-T-400W, FSC 5962 ([Cleat](https://www.cleat.ai/government/contracts/memory-upgrade-so4p)) | Authorized-source memory; shows live memory obsolescence | L1/L3 |
| 4 | **DLA Land and Maritime** | Supply-chain buyer | Recurring memory microcircuit solicitations (search results) | Authorized aftermarket parts (needs L3 + authorization) | L3 |
| 5 | **NSWC Crane** | Navy DMSMS/SD-18 hub | Publishes DMSMS resources and SD-18 | Gatekeeper and SBIR sponsor, not a cash buyer | SBIR |
| 6 | **Trenton Systems** | Rugged/defense server OEM | Named in DD2; DDR4 RDIMM-dependent | Managed die-bank program for a DDR4 module BOM | L1 |
| 7 | **CP Technologies / Core Systems** | Rugged defense computing | Named in DD2 | Same | L1 |
| 8 | **U.S. mid-size industrial PC/SBC makers** with Advantech-type DDR3/DDR4 EOLs | Industrial OEM | DDR3 LTB 2026-06/11 at Advantech; DDR3 LTB within 18–24 months for many industrial/medical designs | LTB study + program; IM/Alliance parts (commission) | L1/L2 |
| 9 | **NewSpace bus and avionics makers on AMD/Xilinx SoCs** | NewSpace | ISSI's DDR4/LPDDR4 commitment for AMD platforms shows the socket exists; no named buyer found | Cheaper screened x72 DDR4/LPDDR4X MCM | L4 [UNVERIFIED] |
| 10 | **Medical-imaging and rail-signaling OEMs** (FDA revalidation, SIL certification lock the die) | Regulated industrial | No evidence found this session | Locked-die program; bank parts | L1/L3 [UNVERIFIED] |

**Channel partners (not customers):** Intelligent Memory and Alliance Memory (rep/distribution, L2), Micross (vault and OSAT), QP Technologies and Integra (package/test).

---

## 8. Honest ceiling, staged path and what a part-time founder can do in year 1

### 8.1 Ceiling (model §6)

| Case | Year-10 revenue | Outside capital | EV/capital (1.5× revenue) |
|---|---|---|---|
| BASE (2 design-ins/yr × 300 units, one bank) | **$2.49M** (EBITDA −$276k) | **$8.11M** (incl. $2.61M bridges) | **0.46×** |
| GLUT | $2.06M | $8.50M | 0.36× |
| SEVERE | $1.69M | $9.08M | 0.28× |
| Grid: 4 design-ins/yr × 1,000 units | $14.8M | — | **4.04×** |
| BULL what-if (4 × 1,000 units at $1,500; aftermarket 4.0×; first design-in m54) | **$26.8M** (EBITDA $13.9M) | $5.5M | **7.3×** |

**Rochester-scale ($200–500M) is not on the table.** It would take a *general* authorized aftermarket business across many part types: 22 OCMs took Flip ~8 years plus PE money plus an acquisition. DRAM alone is a **$2–27M/yr** business for an entrant, depending entirely on MCM design-ins.

### 8.2 Staged path with gates

| Stage | Months | Money | What happens | Gate to the next stage |
|---|---|---|---|---|
| 0 | m1–m15 | Founder $40k, ~15 h/week | §11 kill experiment; Plan A: managed die-bank programs on Micross consignment (L1) plus a rep agreement with IM or Alliance (L2) | A DRAM OCM letter (distribution or aftermarket) **and** ≥3 locked-die LOIs at ≥2.5× EOL price |
| 1 | m18 | **$1.5M** outside | Founder full-time; AS9120B quality system; bank #1 (one DDR4 8Gb family, 10 wafers) at a Micross-type vault; package/test NRE | ≥1 MCM evaluation LOI from a NewSpace or rugged program |
| 2 | m30 | **$4.0M** outside | MCM NRE $1.4M, 2 engineers + BD; evaluation lot m48; design-ins from m60 | ≥4 design-ins/yr at ~1,000 units by ~m72, or stop |
| 3 | m60+ | Bridges / acquisition | Resurgent-type acquisition (DSCR 1.50 BASE only) or merger into an incumbent | — |

### 8.3 Does a software-led entry (DMSMS demand data) help?

**Marginally.**
- **What it does:** it finds the *locked-die* subset of DRAM DMSMS cases, which no public data set separates out. It also builds the aggregated demand book an OCM or financier would want before selling LTB wafers to a newcomer.
- **What it doesn't do:** it does not create authorization. OCMs authorize capital, quality systems and channel.
- **Overlap with round 1:** it is DD2's product (lifecycle intelligence), which the red team downgraded: "a $249 feature distributors give away" (05_REDTEAM, DD2 verdicts).
- **Best use:** as the *sales instrument* for Plan A, not as a product.

### 8.4 Year 1, part-time, concretely

1. **Days 1–30:** run the §11 kill experiment.
2. **If it passes:**
   - form the LLC;
   - sign a rep agreement with Intelligent Memory or Alliance;
   - agree a white-label consignment arrangement with Micross;
   - sell LTB studies ($4,000) and managed programs ($750/month) to mid-size defense, rugged and industrial OEMs facing DDR3/DDR4 LTBs before end-2027.
3. **Expected result** (model §4, BASE): **$12.6k recurring ARR at m12, $22.0k at m18, $29.5k at m24, $42.6k at m36**. Cash low **$30.2k (m3)**. The founder is never paid.
4. **Do not buy wafers in year 1.** A bank bought at 2026–27 peak prices returns 6.5% at best (model §3), on capital the founder does not have.

---

## 9. Model economics headline (`models/legacy-dram-diebank.py`)

**Plan A, bootstrap wedge (founder's $40k, part-time)**

| Scenario | Recurring ARR m12 | m18 | m24 | m36 | Breakeven | Founder paid? | Cash low | Cash m36 |
|---|---|---|---|---|---|---|---|---|
| BASE | $12.6k | $22.0k | $29.5k | **$42.6k** | m3 (no founder pay) | **never** | $30.2k (m3) | $90.2k |
| GLUT | $12.6k | $18.1k | $23.6k | $33.5k | m3 | never | $30.2k | $77.4k |
| SEVERE | $12.6k | $17.4k | $19.7k | $26.4k | m3 | never | $30.2k | $69.3k |

**Plan B, staged moonshot.**
- **First 36 months:** recurring ARR m36 is **$81.4k BASE**, $61.4k GLUT and $46.1k SEVERE. **$5.5M is raised by m36**, and there is no post-raise breakeven inside 36 months. The bank and MCM book no revenue before m36.
- **10 years:** see §8.1.

**Unit economics (model §3)**
- **Managed program:** $770/month gross profit; $79k lifetime gross profit; ~136 founder hours to win one.
- **Channel commission:** $2,000/yr per account at 2026 prices, but only $295/yr at the long-run price.
- **Bank and MCM:** as in §3.

**Sensitivity (±30%, model §8)**
- **Plan A m36 ARR:** price moves it $29.8k–$55.4k; conversion $32.4k–$52.8k. **No knob makes the founder full-time.**
- **Plan B EV/capital:** price 0.29–0.70×; conversion 0.31–0.62×.
- **Bank IRR:** most sensitive to the aftermarket multiple (−9.6% to +11.7%).

---

## 10. Facing round 1's recurring failure modes (05_REDTEAM)

| Failure mode the red team found | Where it bit | How DD7 handles it |
|---|---|---|
| Unsourced buy price decides the model | RT-VC-DD1-05, RT-HYP-DD1-04 | Bank cost = p1 wafer table × the scenario's price deck × 0.75. No OCM quote exists, and getting one is kill track A. A sensitivity is shown. **The bank is not the venture's engine**, so a wrong number cannot carry the conclusion |
| Cash cycle not simulated | RT-VC-DD1-04 | Services net-30, commissions and hardware 2-month lag, inventory capitalised; bridges reported as external capital |
| No income tax | RT-VC-DD1-07 | 30% with loss carry-forward |
| The customer already has the answer, or gets it free | RT-HYP-DD1-01; DD2 verdicts | Named here: **Micross sells the vault direct** and **JEDEC substitutes resolve most DRAM DMSMS cases**. Conversion is held at 10% × 35%, and kill track B tests locked-die demand explicitly |
| Lifestyle ceiling dressed as a venture | RT-VC-DD1-06; DD3/DD5 verdicts | The ceiling is computed, with a grid of what the MCM must achieve. Verdict: side line |
| Optimistic funnel | RT-VC-DD2-06 | 6-month ramp, 4 conversations/month part-time, founder-hours capacity cap |
| Founder time and on-call unrealistic | DD4 verdicts | Hours budget enforced; Plan B forces full-time and hires the quality, test and engineering staff explicitly |
| Physics hand-waved | PHY on DD1/DD3/DD5 | §5: unsawn wafers, re-probe at pull, test-program obsolescence named; aged-die yield flagged as unmeasured |
| Incumbent heritage ignored | C-65 scorers (competition = 1) | MCM priced at the low end ($900); design-ins gate Stage 2; grid shows what it takes |

---

## 11. Kill experiment (<$10k, <30 days)

**Budget about $6k:** one trip to a DMSMS or defense-electronics event or one OEM visit ~$2.5k; LinkedIn Sales Navigator ~$100; buy ~100 ESMT/Winbond DDR4 KGD from distributor stock plus a quick-turn package-and-test quote run ~$2.5k; legal review of a rep agreement ~$900.

**Track A — will any DRAM OCM deal with a new entity?** Send structured RFIs to **Winbond, ESMT, Etron, Nanya, Alliance Memory and Intelligent Memory**. Ask:
1. Will you sign an authorized distribution, rep or aftermarket agreement with a new U.S. entity?
2. What wafer or KGD MOQ, price and payment terms apply to an LTB-style bank of one DDR3/DDR4 part?
3. Which certifications do you require (AS9120B, AS6496)?

**KILL** if 0 of 6 will discuss anything beyond a stocking distributorship needing >$250k of inventory. **PASS** if ≥1 offers a rep or distribution agreement and ≥1 quotes wafer/KGD terms.

**Track B — is there locked-die DRAM demand?** Run 10 interviews with DMSMS managers and mid-size OEMs (§7 #1–3 and #6–8). Ask:
1. In the last 24 months, how many DRAM DMSMS cases did you have where a JEDEC substitute was **not** acceptable?
2. What did you pay, and from whom?
3. Would you sign an LOI for a managed bank or an authorized part at ≥2.5× the EOL price?

**KILL** if fewer than 3 of 10 report a locked-die DRAM case with ≥$50k life-of-need value, or if all would buy from Rochester or Micross by default.

**Track C — supply-side costs.** Get written quotes for:
- Micross EDSP consignment storage (annual fee for one 10-wafer bank);
- QP Technologies or Integra for package plus at-speed test of a DDR4 x16 FBGA-96 (NRE and per-unit at 2,000 units);
- an x72 MCM substrate design and assembly.

**KILL the bank line** if the per-die pull cost is >$15. **KILL the MCM line** if NRE is >$2M or the unit build is >$400 before die.

**Result mapping:** the quotes replace model inputs `storage_pct_yr`, `pack_unit`, `test_unit`, `bank_nre_first`, `mcm_nre_total`, `aftermarket_mult` and `p_program`. Re-run the model and re-score.

---

## 12. Explicit kill criteria

1. Any track in §11 fails → stop C-91. Keep at most the L1 managed-program service inside DD2.
2. By m15, no OCM letter and fewer than 3 locked-die LOIs → no Stage-1 raise.
3. By m30, no MCM evaluation LOI → no Stage-2. The bank continues only if it is cash-positive standalone.
4. By ~m72, fewer than 4 design-ins a year at ~1,000 units → stop MCM investment. The model shows below ~1× capital otherwise.
5. Never buy a bank when the projected unit GM at purchase is below 20% (the model's rule), which rules out GLUT and SEVERE purchases at startup pull costs.

---

## 13. Open gaps (ranked by decision weight)

1. **OCM willingness and terms** for a new entity (Winbond, ESMT, Etron, Nanya, Alliance, IM). No public program exists; it can only be learned by asking (§11 A).
2. **Share of DRAM DMSMS cases with locked die**, and what those buyers pay. DSPO gives only the overall mix (§11 B).
3. **Hi-rel x72 DDR4 MCM prices** (Teledyne, Mercury, Frontgrade, DDC, 3D Plus): RFQ-only.
4. **U.S. OSAT package/test NRE and per-unit cost at 1–2k units; Micross storage fee** (§11 C).
5. **Aged-die yield data** after 10+ years in N2. No paper was found, and the Rochester study covers packaged parts only.
6. **GIDEP notice counts per year; DoD DMSMS spend on memory.** dsp.dla.mil failed DNS.
7. **DRAM-specific SBIR/DPA topics; state programs** (not searched).
8. **Ownership and availability of acquisition targets** (Lansdale, Integra, Golden Altos, small licensed manufacturers); OCM-licence change-of-control terms.
9. **The long-run legacy price ($3/GB)** is a judgment. It drives every 10-year bank number.
10. Hosts to allow for verification: supplychainconnect.com, electropages.com, dsp.dla.mil (all failed DNS this session).
