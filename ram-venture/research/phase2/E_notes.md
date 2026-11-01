# Phase 2, Branch E: business-model-first concepts (research notes)

Agent: `E` · Written: 2026-11-01 · Cards: `research/phase2/E.json` (14 cards, E-01 to E-14) · Sources: `research/sources/E.jsonl` (58 entries) · Assumptions: `research/assumptions/E.md` · Numbers: Appendix A (scratch script `e_estimates.py`, exits 0)

---

## 0. Read this first: what I could and could not research

- **WebSearch: 0 searches.** The per-turn budget of 200 searches, shared by every agent, was already spent when this branch started. I did not route around it.
- **WebFetch: blocked.** `www.rochesterelectronics.com`, `www.sandia.gov` and `technology.nasa.gov` all failed DNS resolution because those hosts are not allowed in this session. After three failures I stopped trying new hosts, as the session rules require. The proxy log shows the same policy denials for trendforce.com, sec.gov, investors.micron.com and others.
- **What I did open (primary, via anonymous `git clone`):**
  - GSA's official FAR repository (DITA XML through FAC 2025-06, last commit 2026-03-30).
  - GSA's official DFARS repository (last commit 2026-06-02).
  - The `rasdaemon` repository (last commit 2026-11-01).
  
  These give **[VERIFIED]** procurement-law facts that no sibling agent had (§1).
- **Everything else is cross-referenced.** Other facts come from URLs that sibling agents logged from search snippets. Each is flagged `CROSS-REFERENCE` in `sources/E.jsonl` and treated as **[REPORTED]** at best.
  - Training-memory claims are tagged **[UNVERIFIED-training]**.
- **Tech-transfer portals were not reached.** The orchestrator asked for listed technologies with URLs and patent numbers from Sandia, LANL, ORNL, LBNL, ANL, PNNL, NASA, AFRL/TechLink, NRL, UMN, Purdue, Penn State, Notre Dame, GT, MIT, Stanford, Cornell, UCSD, Michigan, NC State, ASU, RPI and SUNY Albany. **I could not deliver this.** No patent number in my files is verified. §6 gives the exact queries to run once the hosts are allowed. I name no URL I did not see.
- **Target vs. actual.** The target was 40–80 searches and fetches. Actual: 0 searches, 3 failed fetches, 3 successful repository clones, and about 25 file-level reads of FAR/DFARS clauses. This branch is therefore weaker on fresh market facts and stronger on regulatory mechanics and computed unit economics.

---

## 1. Primary findings (VERIFIED: official GSA FAR/DFARS text, opened via git)

1. **NDAA FY2023 §5949 is not yet in the FAR or DFARS** [VERIFIED for these snapshots].
   - A grep of all 3,945 FAR DITA files (through FAC 2025-06, 2025-10-01; [repo](https://github.com/GSA/GSA-Acquisition-FAR)) and all 3,320 DFARS files ([repo](https://github.com/GSA/GSA-Acquisition-DFARS), snapshot 2026-06-02) finds no "covered semiconductor", CXMT, YMTC, SMIC or 5949 text.
   - The statute takes effect **2027-12-23** ([XenoSpectrum](https://xenospectrum.com/en/apple-china-memory-federal-procurement-ban-2027/), cross-ref).
   - With ~13 months to go, there was no implementing clause as of these snapshots. **Caveat:** an interim rule, or a Revolutionary FAR Overhaul deviation posted only on acquisition.gov, could postdate or bypass the repository.
   - This weakens every concept that depends on paid §5949 verification: C-07, D-11 and my E-09.
2. **The §889 precedent cuts against paid verification** [VERIFIED].
   - FAR 4.2101 defines "reasonable inquiry" as an inquiry into information "in the entity's possession" that "excludes the need to include an internal or third-party audit" ([FAR 4.2101](https://github.com/GSA/GSA-Acquisition-FAR/blob/master/dita/4.2101.dita)).
   - If the FAR Council copies the §889 pattern for §5949, as it did for the drone ban in FAR Part 40 / 52.240-1, Nov 2024 ([FAR 40.202](https://github.com/GSA/GSA-Acquisition-FAR/blob/master/dita/40.202.dita)), compliance becomes a self-representation. Independent die-level testing would then be optional, not mandated.
3. **"U.S.-made" earns no general premium in federal procurement** [VERIFIED].
   - TAA: the WTO GPA threshold is **$174,000** ([FAR 25.402](https://github.com/GSA/GSA-Acquisition-FAR/blob/master/dita/25.402.dita)). Above it, Korean, Taiwanese and Japanese memory competes on equal terms.
   - BAA domestic content: **65% for 2024–2028, 75% from 2029** ([FAR 25.101](https://github.com/GSA/GSA-Acquisition-FAR/blob/master/dita/25.101.dita)). But the content test **is waived for COTS** ([FAR 25.001](https://github.com/GSA/GSA-Acquisition-FAR/blob/master/dita/25.001.dita)).
   - Civilian BAA evaluation factor: **20% (large business) / 30% (small business)** ([FAR 25.106](https://github.com/GSA/GSA-Acquisition-FAR/blob/master/dita/25.106.dita)), and only below the TAA threshold.
   - This confirms p1-funding's §10 reading, which that agent had tagged UNVERIFIED-H. It is now verified.
4. **Recovered/recert memory is constrained in federal supply** [VERIFIED].
   - FAR 52.211-5 defines "New" as "composed of previously unused components" ([FAR 52.211-5](https://github.com/GSA/GSA-Acquisition-FAR/blob/master/dita/52.211-5.dita)).
   - FAR 52.246-26 counts "used items represented as new" as counterfeit ([FAR 52.246-26](https://github.com/GSA/GSA-Acquisition-FAR/blob/master/dita/52.246-26.dita)).
5. **DFARS creates two real moats and one real demand** [VERIFIED] ([DFARS 252.246-7008](https://github.com/GSA/GSA-Acquisition-DFARS/blob/master/dita/252.246-7008.dita), [DFARS 246.870-2](https://github.com/GSA/GSA-Acquisition-DFARS/blob/master/dita/246.870-2.dita)).
   - **Moat 1, authorized sources first.** Contractors must buy from OCMs, authorized suppliers or **authorized aftermarket manufacturers** before anyone else. This is the moat for E-07 and the reason Rochester Electronics exists.
   - **Moat 2, contractor-approved suppliers.** These must use "established counterfeit prevention industry standards" and the contractor "assumes responsibility for the authenticity".
   - **The demand.** When traceability cannot be established, the contractor is "responsible for inspection, testing, and authentication" and must keep the documentation. That is paid demand for E-08.
6. **Index-based escalation is already legal in federal contracts** [VERIFIED].
   - FAR 16.203-1(a)(3) allows economic price adjustment on "cost indexes of labor or material ... specifically identified in the contract" ([FAR 16.203-1](https://github.com/GSA/GSA-Acquisition-FAR/blob/master/dita/16.203-1.dita)).
   - FAR 52.216-4 (Jan 2017) is the standard clause ([link](https://github.com/GSA/GSA-Acquisition-FAR/blob/master/dita/52.216-4.dita)).
   - This is the legal hook for E-02.
7. **DIMM-health telemetry is free and mature** [VERIFIED].
   - `rasdaemon` logs kernel memory CE/UE events to SQLite, MySQL, MariaDB or PostgreSQL.
   - It already ships `PAGE_CE_THRESHOLD` and `ROW_CE_THRESHOLD` with soft-offline actions ([rasdaemon](https://github.com/mchehab/rasdaemon)).
   - That makes E-01 buildable fast. It also means the predictive layer is no moat.

---

## 2. Key numbers (all computed in Appendix A; inputs in `assumptions/E.md`)

| Quantity | Value | Used by |
|---|---|---|
| Annualized DRAM contract-price volatility | **44%** (2024–26 TrendForce QoQ midpoints); **55%** with the 2018–19 and 2022–23 bust quarters | E-03, E-04 |
| Fair premium, 12-month ATM price cap (Black-76) | **16.7–20.7% of capped spend**; 9–13% for a cap at 1.25× | E-04 |
| Cap writer's 99th-percentile loss per $1M capped | **$1.5–2.1M** | E-04 |
| Expected 12-month return, buy DDR5 at spot+5% and hold | **−46%**; −22% if the spot premium (1.69×) persists; +7% only at contract (unavailable to newcomers) | E-05 |
| 36-month lease of a 64GB RDIMM at 14% IRR | **$48.83/month = $0.76/GB-month**; lessor IRR **−29%** if the lessee walks at m18 in the glut, **−58%** at m12 | E-06 |
| Single-part die bank ($600k) | IRR **16%** base / **−7%** bear / **39%** bull; unit GM 33–66% | E-07 |
| AS6171 lab | Breakeven **36 lots/month** at $1,400; 60 lots/month gives $1.0M revenue, 41% GM, $314k operating profit | E-08 |
| Federal reseller | $1.5–2.5M of sales per $150k gross profit (6–10% GM) | E-09 |
| STTR path to customer revenue | **3.1%** per topic attempt; 14.8% after 5; **46 months** if every step succeeds first time | E-10 |
| SBA acquisition at 3.5× shortage EBITDA ($1.2M) | Debt service $612k/yr; **DSCR 1.96 → 0.65 (normal) → 0.33 (glut)** | E-11 |
| DIMM Health Subscription (2,400-DIMM customer at $0.75/DIMM-month) | $21.6k/yr; GM **59%** at 2026 spares prices and **82%** in a glut; 25 customers = $540k ARR | E-01 |
| Memory escalation index | $300k ARR at 89% GM self-built, 57% with licensed contract data | E-02 |

**Cross-check against inherited numbers.** DDR5 contract is $15.99/GB, RDIMM $20.31/user-GB, glut $6.40/$8.13, severe $1.60, from `models/dram_cost_stack.py`. Spot is $26.96/GB on 2026-08-31 ([BuySellRAM/DRAMeXchange](https://www.buysellram.com/blog/ram-market-update/), cross-ref). Spot at 1.69× contract is the single most important number for E-05: a newcomer buys at the panic price.

---

## 3. Lens-by-lens evaluation (mission §3E) and the orchestrator's seeds

Recurring revenue (Rec.) means the customer pays again without a new sale: subscription, retainer or index license.

| Lens / seed | Card | Recurring? | Capital | Glut behaviour | Verdict |
|---|---|---|---|---|---|
| SaaS + spares, a seed the orchestrator did not list | **E-01** | **Yes** (per DIMM-month) | T0 | Margin up, demand down | **Best founder fit in E** |
| Data product: memory escalation index | **E-02** | **Yes** (annual index license) | T0 | Two-sided use survives; new sales slow | Promising but small |
| Price hedging: futures/swaps | E-03 | Would be (fees) | T3 | Volatility persists | **Dead**: no index, no liquidity, CFTC |
| Memory "insurance" / allocation guarantee | E-04 | Yes (premium) | T2 | Product disappears | **Dead**: short a 44–55%-vol call |
| Buy-and-hold inventory arbitrage | E-05 | **No** | T1 | Wiped out | **Dead**: speculation, −46% EV at spot |
| Memory leasing / MaaS financing | E-06 | Yes (lease) | T2 | Lessee walks; −29% to −58% IRR | **Dead for founder** |
| LTB aggregator / die banking (Rochester model) | **E-07** | Partly (repeat call-offs) | T2 | Glut-proof | Real business, but only for incumbents |
| Test and qualification lab (AS6171) | **E-08** | Partly (repeat brokers/EMS) | T1 | Volume falls, DFARS floor stays | Marginal; needs a hire |
| §5949/TAA/BAA compliance-as-a-product | E-09 (reseller form) | Contract-vehicle repeat orders | T1 | Margin compresses | **Kill**: compliance is a free checkbox (§1) |
| University/lab patent license → SBIR/STTR → defense | **E-10** | No (grants), later yes | T1 | Glut-proof | Marginal; grant-farm risk; 46 months |
| Acquire a small memory company | E-11 | Yes (acquired customers) | T2 | DSCR 0.33 → default | **Dead now**; revisit in the 2028–29 trough |
| Acquire a distressed IP estate (Optane) | E-12 | Would be (royalties) | T3 | Dies | **Dead** |
| CXL consulting/integration | **E-13** | Partly (managed tuning) | T0 | Pitch halves | Marginal; needs a kernel cofounder |
| IP licensing → intelligence product | E-14 | Yes | T0 | Buyer set shrinks | Likely kill (crowded) |
| DRAM procurement co-op / GPO | not carded | — | — | — | Already C-15. My addition: GPOs work where members can commit volume; small OEMs can't post the letters of credit (C-15's fatal flaw) |
| Defense/space rad-hard memory module | not carded | — | — | — | Already C-08 (hi-rel MCM house), A2-03 (rad data/upscreen), B-14 (TrustedCXL) and A1-06 (HZO FeRAM) |
| Fabless design → foundry | not carded | — | — | — | Covered by A1/A2/A3/C-02/C-14. No new business-model angle beyond E-07's aftermarket variant |

**Why a business-model branch produced mostly kills.** Every financial-engineering lens (E-03, E-04, E-06, E-11) is long or short DRAM price risk at the top of a 6× move with a likely 2028 turn. Under rule 6 these die: they are bets on the cycle wearing a business model. The survivors (E-01, E-02, E-07, E-08, E-10) earn on lifecycle, compliance or contract mechanics, which are indifferent to the cycle.

---

## 4. Evidence behind each card (short)

- **E-01 DIMM Health Subscription.**
  - Telemetry: rasdaemon [VERIFIED].
  - Demand driver: DDR4 contract +24% in 3 months to Oct 2026 ([Guru3D/Barclays](https://www.guru3d.com/story/ddr4-memory-prices-now-also-rise-as-dram-supply-shortages-intensify-through-2028/), cross-ref); 64GB RDIMM $450 → >$900 ([EE Times Asia](https://www.eetasia.com/memory-prices-surging-by-90-from-4q-2025/), cross-ref).
  - Failure rates: field studies (Google "DRAM errors in the wild", SIGMETRICS 2009; Meta/Facebook DSN 2015) report ~8% of DIMMs with a correctable error per year and ~0.2%/DIMM-yr uncorrectable [UNVERIFIED-training; no URL seen this session]. I model 1.5%/DIMM-yr replacements, including predictive pulls.
  - Supply: recovered DDR4 at $3–8/GB (p1-backend §6.5, ESTIMATE).
  - **Kill experiment (<$2k, <30 days):** interview 10 out-of-warranty fleet operators (university research computing, two regional colos, two MSPs). Ask what they pay TPM per server-year and how many DIMMs they replaced last year. Kill if fewer than 3 would pay ≥$0.50/DIMM-month, or if TPM quotes already include unlimited DIMM swaps under $5/server-month.
- **E-02 Memory Cost Escalation Index.**
  - Legal hook: FAR 16.203-1 and 52.216-4 [VERIFIED].
  - Downstream pain: Samsung DX losses on component costs ([Samsung 3Q26](https://news.samsungsemiconductor.com/global/samsung-electronics-announces-third-quarter-2026-results/), cross-ref).
  - Incumbent data: [TrendForce board](https://www.trendforce.com/price_dram.html), [TechInsights](https://www.techinsights.com/blog/slides-dram-market-report-q2-2026) (cross-ref).
  - Possible transaction-data partner: [Mobius Materials](https://www.prnewswire.com/news-releases/mobius-materials-raises-3m-to-combat-one-of-manufacturings-biggest-issues-amid-us-china-trade-tariffs-302643403.html) (cross-ref).
  - **Kill experiment:** show a draft clause plus 12 months of back-filled index to 8 integrators/EMS procurement leads. Kill if fewer than 2 would put it in a live contract or if all insist on TrendForce as the reference.
- **E-03 DRAM futures.**
  - The incumbent "forward market" is physical LTAs: SK hynix 14 LTAs to 2029 ([Sammy Fans](https://www.sammyfans.com/2026/10/28/sk-hynix-q3-margin-hits-record-80-secures-14-ltas-with-memory-supply-booked-to-2029/amp/)); Nanya LTAs re-priced >60% ([TrendForce News](https://www.trendforce.com/news/?p=65146)) (cross-ref).
  - Prior exchange attempts: I recall DRAMeXchange starting (c. 2000) as an online spot-trading venue before becoming TrendForce's price service, and no DRAM futures contract on CME/ICE/SGX/TAIFEX [UNVERIFIED-training; could not search].
  - **Verification queue:** CFTC product filings for "DRAM" or "memory chip" swaps; whether any GPU-compute index (2025-era compute-futures startups) has been licensed for derivatives, as a template [UNVERIFIED-training].
- **E-04 price cap.** Black-76 pricing (Appendix A §2). Allocation reality: TrendForce RP260114IU, Micron 10-K and TechNews 2026-03-31 (cross-ref).
- **E-05 inventory arbitrage.**
  - Rate deceleration from +95% to +12.5% QoQ (TrendForce series in p1 `price_series.json`).
  - Spot/contract ratio 1.69×.
  - Bear case: Bloomberg Intelligence oversupply in 2028 ([KuCoin summary](https://www.kucoin.com/blog/2027-memory-chip-boom-sk-hynix-samsung), cross-ref).
- **E-06 leasing.** Prices from EE Times Asia and [Servnet](https://www.servnetuk.com/research/ddr5-server-memory-price-tracker-2026) (cross-ref); 2023 trough from [KED Global](https://www.kedglobal.com/korean-chipmakers/newsView/ked202310040013) (cross-ref).
- **E-07 die bank.**
  - Moat: DFARS 252.246-7008 / 246.870-2 [VERIFIED].
  - Demand: [Findchips May 2026](https://blog.findchips.com/memory-shortage-watch-ddr3l-ddr4-may-2026/) and [Advantech DDR4 EOL](https://www.advantech.com/en/resources/news/response-measures-to-samsung-ddr4-ic-eol-announcement) (cross-ref).
  - Incumbents: [Micross](https://micross.com/uploads/05827c98-1b61-4d4d-bb3c-04dc1b207e5a/Die_and_Wafer_Flyer_Rev_1_WEB.pdf) (cross-ref); Rochester [UNVERIFIED-training: Newburyport MA, 70+ OCMs].
  - U.S.-made long-lifecycle competitor: [Micron Manassas](https://www.hpcwire.com/off-the-wire/micron-advances-made-in-america-memory-with-manufacturing-expansion-in-virginia) (cross-ref).
- **E-08 AS6171 lab.** DFARS 252.246-7008 and FAR 52.246-26 [VERIFIED]. Lab costs and per-lot fees from p1-backend §7 (ESTIMATE). Lab names [UNVERIFIED-training].
- **E-09 reseller.** All of §1. The pull is real ([Schumer 2026-07-30](https://www.schumer.senate.gov/newsroom/press-releases/citing-core-national-security-and-economic-reasons-schumer-demands-apple-reject-chinese-military-linked-chips), cross-ref), but the rules give no price premium.
- **E-10 STTR vehicle.**
  - Technologies: [Sandia HZO FeRAM/FTJ](https://www.sandia.gov/research/news/evolving-semiconductor-technology-for-national-security-applications/), [Penn/AFRL AlScN](https://www.engineering.upenn.edu/stories/turning-up-the-heat-on-data-storage/), [Purdue In₂O₃](https://engineering.purdue.edu/ECE/News/2026/purdue-researchers-build-3d-chip-platform-for-faster-more-efficient-ai-computing).
  - Topics: [DARPA DV017](https://www.darpa.mil/research/programs/non-volatile-memory-extreme-environments), [AF254-D0806](https://www.sbir.gov/topics/12036).
  - How defense actually pays for on-shore memory: [Everspin–Amentum $40M](https://electronics360.globalspec.com/article/23702/everspin-earns-40-million-mram-deal-for-defense-memory-services). All cross-ref.
  - STTR PI rule: p1-funding §7.3 [UNVERIFIED-H there].
- **E-11 acquisition.** [Crucial exit](https://www.storagenewsletter.com/2025/12/05/micron-announces-exit-from-crucial-consumer-business/) (cross-ref). SBA 7(a) terms [UNVERIFIED-training]. DSCR model in Appendix A §9.
- **E-12 Optane estate.**
  - Post-mortem: [Micron exit](https://www.nasdaq.com/press-release/micron-updates-data-center-portfolio-strategy-to-address-growing-opportunity-for); [$545M charges](https://www.theregister.com/2021/03/17/micron_pulls_the_plug_on/); [Lehi to TI](https://www.anandtech.com/show/16800); [Intel $559M impairment](https://www.sec.gov/Archives/edgar/data/50863/000005086322000030/intc-20220702.htm); [>$7B losses](https://www.snia.org/sites/default/files/2025-05/SNIA-SDC22-Coughlin-Handy-Persistent-Memories-Without-Optane-Where-Would-We-Be.pdf).
  - Licensing timeline benchmark: [Weebit](https://www.weebit-nano.com/news/press-releases/weebit-nano-expands-licensing-agreements-with-key-customers-three-customer-chip-designs-taped-out-to-date/). All cross-ref.
- **E-13 CXL practice.** [Linux CXL maturity map](https://github.com/torvalds/linux/blob/master/Documentation/driver-api/cxl/maturity-map.rst) and [SK hynix HMSDK](https://github.com/skhynix/hmsdk) (cross-ref from B).
- **E-14 patent radar.** [ITC 337-TA-1487](https://www.usitc.gov/press_room/news_release/2026/er0227_68226.htm); [Everspin's $6.0M quarterly litigation cost](https://www.sec.gov/Archives/edgar/data/0001438423/000162828026067890/mram-20260930xexx991.htm) (cross-ref). Netlist cases [UNVERIFIED-training via p1-ip].

---

## 5. Post-mortems and precedents that shaped the verdicts

- **Optane (E-12).** The technology worked: it shipped at TRL 9. It lost on $/GB against DRAM that kept getting cheaper, and on ecosystem (software had to change). Intel lost more than $7B. **Lesson for business-model plays:** buying the estate buys none of the missing pieces, which were a fab, a cost curve and software adoption.
- **Memory-IP licensors (E-12, E-14).**
  - Weebit is the best-run independent and is still sub-scale after ~10 years.
  - Everspin's licensing line is $3.7M of $20.6M quarterly revenue, while a single ITC defense cost it $6.0M in one quarter.
  - Rambus succeeded only with decades of litigation stamina [UNVERIFIED-training].
  - **Out-licensing fails the 36-month test.**
- **Rochester Electronics model (E-07)** [UNVERIFIED-training]. Authorization by OCMs plus die and wafer banking plus licensed re-manufacture. Its moat is regulatory (DFARS authorized-source preference, verified) and relational, not technical. It cannot be replicated without capital and OCM trust.
- **Mobius Materials (E-02, E-05, E-08).**
  - A YC-backed Richmond VA marketplace that gives away its DRAM report to drive transactions (p1-market §9).
  - It is the nearest thing to a DRAM "exchange", and it is physical.
  - It is a partner candidate for E-02's transaction data and a competitor for any trading or authentication play.
- **Physical LTAs as the incumbent hedge (E-03, E-04).** SK hynix has 14 LTAs booked to 2029, and Nanya's re-priced >60% at expiry. Makers and big buyers already transfer risk bilaterally, and the LTAs themselves re-price, which shows how little appetite exists for fixed-price risk transfer at the top of a cycle.
- **Search-fund acquisitions in cyclical sectors (E-11)** [judgment]. ETA works on stable cash flows. A memory reseller's 2026 EBITDA is a price windfall, not a run-rate. The DSCR math (1.96 → 0.33) is the post-mortem in advance.

---

## 6. University and national-lab licensing lens: what is known and what to run

**Status.** No portal query ran: search budget exhausted, hosts DNS-blocked. What follows is the evidence siblings found plus a query plan. **No portal URL or patent number below is claimed as seen.**

| Institution | Candidate technology | Evidence available (cross-ref) | Already carded as a device play | Business-model fit (E view) |
|---|---|---|---|---|
| Sandia (NM) | HZO FeRAM + binary/32-state FTJs in trusted MESA 200mm fab | Sandia news 2026-05-13 | A1-06 | **Best lab lead** for E-10. A DOE license plus CRADA keeps manufacture in the U.S.; first-of-kind rad-hard NVM sells to space primes |
| Penn + AFRL (via TechLink for the AFRL share) | AlScN ferroelectric-diode NVM at 600 °C | Penn 2024-05; USAF AF254-D0806 | A1-07 | Defense niche (hypersonics, Venus/geothermal); STTR-shaped |
| Purdue (Purdue Research Foundation OTC) | ALD In₂O₃ BEOL transistors incl. FeFET tiers, 200mm M3D | Purdue ECE 2026-09-16 | A1-01 | Long-dated; option only |
| Georgia Tech | 3T IWO BEOL gain-cell eDRAM | GT 2024 | A1-01 | Option only |
| ASU (Skysong) | PMC/CBRAM, base patent expired ~2016 [UNVERIFIED-training]; dendritic anti-counterfeit tags [UNVERIFIED-training] | none this session | A2-08 (CBRAM) | Tag idea could feed E-08 provenance. Unverified, so not carded |
| UMN, Notre Dame, Penn State, Cornell, MIT, Stanford, Michigan, UCSD, NC State, RPI, SUNY Albany, LANL, ORNL, LBNL, ANL, PNNL, NASA, NRL | See p1-ip §6.2–6.3 (inventor-level leads, all UNVERIFIED-training) | none this session | — | Unknown until the portals are queried |

**Query plan (run when the hosts are allowed; search each office's own portal):**
- **Terms to use:** "ferroelectric", "hafnium", "HZO", "FeRAM", "tunnel junction", "MRAM", "spin-orbit", "memory cell", "radiation hardened memory", "non-volatile", "gain cell", "oxide semiconductor", "SRAM", "error correction memory".
- **Fields to record:** technology ID, patent or application number, status (available / optioned / licensed), and whether startup-friendly terms exist (UMN's MN-IP, NASA's startup license program, DOE lab option agreements) [program names UNVERIFIED-training].
- **Specific asks:**
  - Sandia: is the HZO FTJ/FeRAM work patented and listed?
  - AFRL via TechLink: the AlScN ferro-diode co-ownership.
  - NASA T2: any radiation-tolerant memory controller or EDAC patents, as a software-founder-friendly license.

**E's judgment on the lens.**
- Licensing is cheap: options run $1–10k (p1-ip §6.4).
- Licensing is not the binding constraint. A technical PI, a fab and Phase III timing are, which is what E-10's 46-month, ~3%-per-attempt math says.
- The one founder-compatible structural insight: STTR lets the PI sit at the lab, so a day-job founder can run the company.
- The vehicle fits the founder, the timeline does not.

---

## 7. Ideas considered but NOT carded (one line each)

- **Used-server-memory residual-value index for lessors/ITAD/auditors.** It overlaps C-05's graded-price index, and the buyers (OEM captives, big ITADs) keep their own remarketing data.
- **DRAM procurement GPO/co-op (current-gen DDR5).** Same model as C-15. Small OEMs cannot post the LCs suppliers want, and allocation value evaporates in a glut.
- **Memory prepayment/trade finance for SMB OEMs securing LTAs.** It is E-06's balance-sheet risk moved upstream: T2–T3, long DRAM at the peak.
- **"Allocation broker" retainer (outsourced memory buyer for integrators).** No supply access a newcomer can broker. It overlaps D-09 and C-15.
- **Federal "Made in USA" memory module brand.** FTC "all or virtually all" limits the claim, and TAA/BAA give no premium (§1). Same idea as C-03 (killed).
- **FPGA/FFF emulation boards for obsolete SRAM/SDRAM (DMSMS).** C considered it. Alliance, ISSI and Winbond still make most legacy parts, and DMEA/Rochester re-creation covers true orphans; also an FPGA-engineering business, not software.
- **COTS DDR4/LPDDR4 radiation lot-acceptance test consortium for NewSpace.** Same business model as A2-03 (MRAM rad data). Beam time and qualification take years.
- **Rad-hard memory module for long-lifecycle programs (seed).** Covered by C-08, B-14 and A2-03. A 2–3-year qualification cycle breaks the 18-month target.
- **Buy GSI Technology (Nasdaq GSIT) or carve out its rad-hard SRAM line.** T3 public-company acquisition. Status and price could not be checked (gsitechnology.com is blocked, per the proxy log).
- **Buy the Crucial brand or trademark from Micron.** No evidence Micron would sell, and the brand without Micron die supply is just another module label.
- **Memory-subsystem redesign services for OEMs hit by DDR4 EOL.** Needs board-level EEs, so it is an engineering consultancy; adjacent to D-14.
- **Anti-counterfeit physical tags (ASU dendritic PUF, DNA marking) for memory reels/modules.** No verified evidence this session (rule 1), and DLA's existing DNA-marking precedent [UNVERIFIED-training] suggests incumbency.
- **Paid DRAM newsletter or forecasting service.** Already D-13 (bridge only). Mobius gives the same content away.
- **Netlist-style patent assertion (buy memory patents and sue).** T2+ litigation finance with a 5–10-year horizon (p1-ip §5); not a founder business.
- **"Memory credits" on CXL-pooled hardware (RAM-as-a-service).** Already D-05 and D-08.
- **Consignment VMI of DRAM at system integrators.** It is C-04 plus E-06's capital risk.

---

## 8. Cross-branch overlap map (for the Phase 3 merger)

| E card | Nearest sibling cards | Distinction |
|---|---|---|
| E-01 | D-02 (memory reclaim), C-05 (recert RDIMMs), D-08 (TB-RAM rental) | E-01 sells uptime and predictive replacement per DIMM-month. C-05 could be its spares supplier; D-02 frees memory rather than replacing it |
| E-02 | D-09 (cost intelligence for SMB OEMs), A1-14 | E-02 licenses an index for contract escalation clauses (two-sided, federal-EPA-compatible). D-09 sells buy/hold alerts to one side |
| E-07 | C-04 (consignment vault), C-02 (fabless long-lifecycle brand) | E-07 takes title and needs OCM authorization (DFARS AAM). C-04 stores OEM-owned stock; C-02 designs its own die |
| E-08 | A1-13 (emerging-memory R&D lab), C-12 (KGD probe) | E-08 does counterfeit authentication of purchased commercial lots under DFARS, not R&D characterization or wafer probe |
| E-09 | C-07, D-11 | E-09 is a reseller; C-07 and D-11 are verification tools. §1 findings weaken all three |
| E-10 | A1-06, A1-07, A1-01, A2-08 | E-10 is the company vehicle and portfolio (STTR structure, Phase III path, probability math), not a device |
| E-12 | A2-10, B-09, A2-11 | E-12 is an IP-estate acquisition, not a device revival or salvage |
| E-13 | B-06 (TB-class CXL node), D-03 (KV-cache integration), D-05 | E-13 is a services practice, not an appliance or software product |

---

## 9. Ranking inside Branch E

**Most promising (for THIS founder):**
1. **E-01 DIMM Health Subscription.** T0, software-led, recurring per-DIMM revenue. Margin *rises* in a glut (59% → 82%). First revenue in 4–8 months. Weakness: small ACV and TPM bundling.
2. **E-02 Memory Cost Escalation Index.** T0, recurring index licenses. Legal hook verified in FAR 16.203-1/52.216-4; two-sided use survives a glut. Weakness: credibility against TrendForce.
3. **E-08 AS6171 memory lab.** DFARS-mandated demand (verified), T1, 41% GM at 60 lots/month. Not a solo-founder business; needs a test engineer.

E-07 (die bank) is the best *business* in the branch, but only for incumbents. E-10 is the only route to licensed lab IP, but it is a grant-funded 46-month path.

**Most important kills / negative findings:**
1. **§5949 compliance is a free checkbox so far.** No FAR/DFARS text yet, and the §889 precedent excludes third-party audits. TAA/BAA give U.S.-made memory no premium over allied memory. This weakens E-09, C-07 and D-11.
2. **Every financial-engineering lens is a disguised bet on the cycle:**
   - Futures (no index or liquidity, T3).
   - Price caps (premium 17–21%; writer loses $1.5–2.1M per $1M at the 99th percentile).
   - Leasing (lessor IRR −29% to −58% when lessees walk in the glut).
   - Inventory arbitrage (−46% expected at spot).
3. **Acquiring a memory business now means buying peak earnings with leverage** (DSCR 1.96 → 0.33). The right time is the 2028–29 trough. Optane-estate and IP-licensing plays fail on "IP without a line is worthless."

---

## Appendix A: scratch estimates script (`python3 e_estimates.py`, exits 0)

The script lives in my scratchpad because this agent owns only `E.json`, `E_notes.md` and its sources and assumptions files. Lift it to `models/` if an E card reaches Phase 4.

```python
"""Branch E (business-model-first) scratch estimates for Phase 2 concept cards.

Run: python3 e_estimates.py   (stdlib only; exits 0)
Every input is either taken from models/dram_cost_stack.py reference values /
research/phase1/price_series.json (cited in E_notes.md) or is an [ESTIMATE]
logged in research/assumptions/E.md. Outputs feed the numbers quoted in
research/phase2/E.json and E_notes.md.
"""
import math
import statistics as st

# ---------------------------------------------------------------------------
# Shared price deck (models/dram_cost_stack.py ddr5_reference(), 2026-11-01)
# ---------------------------------------------------------------------------
DDR5_CONTRACT_GB = 15.993        # Q4-2026 DDR5 component contract, $/GB
RDIMM64_CONTRACT_USERGB = 20.312 # Q4-2026 64GB RDIMM contract, $/user-GB
GLUT_COMPONENT_GB = 6.397        # -60% glut (A-05)
GLUT_RDIMM_USERGB = 8.125
SEVERE_COMPONENT_GB = 1.599
SEVERE_RDIMM_USERGB = 2.409      # cost floor (cost_rdimm64_usd_per_user_gb)
SPOT_DDR5_GB = 26.96             # DRAMeXchange DDR5 16Gb spot avg 2026-08-31
RDIMM64_STREET = 2064.0          # Servnet street price Aug 2026

def hdr(t):
    print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)

def npv(rate, cfs):
    return sum(cf / (1 + rate) ** i for i, cf in enumerate(cfs))

def irr(cfs, lo=-0.6, hi=5.0):
    f_lo, f_hi = npv(lo, cfs), npv(hi, cfs)
    if f_lo * f_hi > 0:
        return float("nan")
    for _ in range(300):
        mid = (lo + hi) / 2
        f_mid = npv(mid, cfs)
        if f_lo * f_mid <= 0:
            hi, f_hi = mid, f_mid
        else:
            lo, f_lo = mid, f_mid
    return (lo + hi) / 2

def pmt(rate, n, pv, fv=0.0):
    """Payment (end of period) that amortizes pv to fv over n periods."""
    if rate == 0:
        return (pv - fv) / n
    return (pv - fv / (1 + rate) ** n) * rate / (1 - (1 + rate) ** -n)

def ncdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))

# ---------------------------------------------------------------------------
# 1. DRAM contract-price volatility (E-03, E-04)
# ---------------------------------------------------------------------------
hdr("1. Contract-price volatility (TrendForce conventional DRAM QoQ midpoints)")
qoq_2024_26 = [15.5, 15.5, 10.5, 2.5, -2.5, 47.5, 95.5, 60.5, 15.5, 12.5]
# through-cycle adds documented downturn quarters (p1-market §7.1):
# 4Q18 -10% ($68->$61), 1Q19 -30%, 1Q23 -20%, 2Q23 -12.5%
qoq_cycle = qoq_2024_26 + [-10.0, -30.0, -20.0, -12.5]
def ann_vol(qs):
    lr = [math.log(1 + q / 100) for q in qs]
    return st.stdev(lr) * 2.0   # quarterly -> annual (sqrt(4))
SIG_2426 = ann_vol(qoq_2024_26)
SIG_CYCLE = ann_vol(qoq_cycle)
print(f"annualized vol, 2024-26 points only : {SIG_2426:.1%}")
print(f"annualized vol, incl. 2018-23 busts : {SIG_CYCLE:.1%}")
print(f"index 3Q25=100 -> 4Q26 = 601 (x{601.4/100:.1f}); glut -60% -> 240")

# ---------------------------------------------------------------------------
# 2. Price-cap ('memory insurance') premium: Black-76 call on contract $/GB (E-04)
# ---------------------------------------------------------------------------
hdr("2. Price-cap subscription: fair premium of a 12-month cap (Black-76)")
def black76_call(F, K, T, sig, r=0.045):
    d1 = (math.log(F / K) + 0.5 * sig * sig * T) / (sig * math.sqrt(T))
    d2 = d1 - sig * math.sqrt(T)
    return math.exp(-r * T) * (F * ncdf(d1) - K * ncdf(d2))
F = DDR5_CONTRACT_GB
for sig in (SIG_2426, SIG_CYCLE):
    for k_mult in (1.00, 1.10, 1.25):
        prem = black76_call(F, F * k_mult, 1.0, sig)
        print(f"sigma {sig:.0%}  cap at {k_mult:.2f}xF : premium = {prem/F:5.1%} of annual spend")
# capital a cap-writer must hold on $1M/yr of capped spend, 99th pct move
for sig in (SIG_2426, SIG_CYCLE):
    z99 = 2.326
    f99 = F * math.exp(-0.5 * sig * sig + sig * z99)
    loss = (f99 - F) / F
    print(f"sigma {sig:.0%}: 99th-pct 12-mo price = {f99/F:.2f}xF -> loss on $1M capped spend at ATM = ${loss*1e6:,.0f}")

# ---------------------------------------------------------------------------
# 3. Buy-and-hold inventory arbitrage (E-05)
# ---------------------------------------------------------------------------
hdr("3. Buy-and-hold DDR5 inventory, 12-month hold from Nov-2026")
buy_spot = SPOT_DDR5_GB * 1.05   # newcomer pays broker ask ~5% over spot avg [ESTIMATE]
carry = 0.12 + 0.02 + 0.01       # capital + storage/insurance/test + shrink/counterfeit [ESTIMATE]
sell_haircut = 0.95              # sell at 5% under spot to a broker [ESTIMATE]
# scenarios: (name, prob, contract multiple at Nov-2027, spot/contract ratio at Nov-2027)
scen = [("squeeze continues", 0.25, 1.25, 1.60),
        ("plateau",           0.40, 1.05, 1.20),
        ("soft turn",         0.25, 0.90, 1.00),
        ("early turn",        0.10, 0.65, 0.90)]
ev = 0.0
for name, p, cm, ratio in scen:
    sale = DDR5_CONTRACT_GB * cm * ratio * sell_haircut
    ret = sale / buy_spot - 1 - carry
    ev += p * ret
    print(f"{name:18s} p={p:.2f} sale ${sale:6.2f}/GB  net return {ret:+.1%}")
print(f"buy at ${buy_spot:.2f}/GB (spot+5%) -> expected 12-mo net return {ev:+.1%}")
# 24-month hold into the A-05 glut
sale24 = GLUT_COMPONENT_GB * 1.0 * sell_haircut
print(f"24-mo hold into glut: sale ${sale24:.2f}/GB -> return {sale24/buy_spot-1-2*carry:+.1%}")
# if one could buy at contract (one cannot without an allocation)
ev_c = sum(p * (DDR5_CONTRACT_GB * cm * ratio * sell_haircut / DDR5_CONTRACT_GB - 1 - carry)
           for _, p, cm, ratio in scen)
ratio_now = SPOT_DDR5_GB / DDR5_CONTRACT_GB
ev_keep = sum(p * (DDR5_CONTRACT_GB * cm * ratio_now * sell_haircut / buy_spot - 1 - carry)
              for _, p, cm, _r in scen)
print(f"sensitivity: spot premium stays at {ratio_now:.2f}x contract -> expected 12-mo net return {ev_keep:+.1%}")
print(f"(counterfactual) buy at contract ${DDR5_CONTRACT_GB:.2f}/GB -> expected 12-mo return {ev_c:+.1%}")

# ---------------------------------------------------------------------------
# 4. DIMM leasing / memory-as-a-service financing (E-06)
# ---------------------------------------------------------------------------
hdr("4. 36-month lease of a 64GB DDR5 RDIMM (lessor view)")
P0 = 1600.0           # small lessor's buy price: between contract $1,300 and street $2,064 [ESTIMATE]
coc = 0.14 / 12       # lessor cost of capital 14%/yr [ESTIMATE]
n = 36
res_base = GLUT_RDIMM_USERGB * 64 * 0.5      # used = 50% of glut new price
res_sev = SEVERE_RDIMM_USERGB * 64 * 0.5
pay = pmt(coc, n, P0, res_base)
print(f"buy ${P0:,.0f}; base residual ${res_base:,.0f}; severe residual ${res_sev:,.0f}")
print(f"payment for 14% IRR at base residual: ${pay:,.2f}/mo = ${pay/64:.2f}/GB-month")
def lessor_irr(months_paid, recovery):
    cfs = [-P0] + [pay] * months_paid
    cfs[-1] += recovery
    return (1 + irr(cfs)) ** 12 - 1
print(f"full term, base residual   : IRR {lessor_irr(36, res_base):6.1%}")
print(f"full term, severe residual : IRR {lessor_irr(36, res_sev):6.1%}")
rec18 = GLUT_RDIMM_USERGB * 64 * 0.6 * 0.85   # lessee returns at m18 in glut; 15% remarketing cost
print(f"lessee walks at month 18 (glut), recovery ${rec18:,.0f}: IRR {lessor_irr(18, rec18):6.1%}")
rec12 = GLUT_RDIMM_USERGB * 64 * 0.6 * 0.85
print(f"lessee walks at month 12,         recovery ${rec12:,.0f}: IRR {lessor_irr(12, rec12):6.1%}")
new_2028 = GLUT_RDIMM_USERGB * 64
print(f"lessee's alternative in 2028: buy new 64GB at ${new_2028:,.0f} vs remaining 18 payments ${pay*18:,.0f}")

# ---------------------------------------------------------------------------
# 5. Authorized-aftermarket die bank (E-07)
# ---------------------------------------------------------------------------
hdr("5. Title-taking die bank for one legacy DRAM part (10-year horizon)")
basis = 600_000.0     # e.g. ~30 x 300mm legacy DDR4 wafers at ~$20k (p1-backend $3k-22k range) [ESTIMATE]
store = 0.015         # nitrogen storage, insurance, periodic re-test, % of basis per yr [ESTIMATE]
pkg = 0.35            # packaging+final test at U.S. OSAT, as fraction of die cost [ESTIMATE]
for label, mult, sell in [("base: 3.0x, 90% sells yrs3-8", 3.0, [0, 0] + [0.15] * 6 + [0, 0]),
                          ("bear: 2.0x, 50% sells yrs3-8", 2.0, [0, 0] + [0.0833] * 6 + [0, 0]),
                          ("bull: 4.0x, 95% sells yrs2-6", 4.0, [0] + [0.19] * 5 + [0] * 4)]:
    cfs = [-basis]
    for f in sell:
        die = basis * f
        cfs.append(die * mult - die * pkg - basis * store)
    print(f"{label:32s} IRR {irr(cfs):6.1%}  gross margin on units {(mult-1-pkg)/mult:5.1%}")

# ---------------------------------------------------------------------------
# 6. AS6171 memory counterfeit-test lab (E-08)
# ---------------------------------------------------------------------------
hdr("6. AS6171 / DFARS 252.246-7008 test lab for memory lots")
capex = 650_000.0     # X-ray, XRF, decap, optical/SEM(used), curve tracer, memory functional tester, ISO 17025 [ESTIMATE]
fixed = 3 * 95_000 + 60_000 + 40_000 + capex / 7    # staff, facility, accreditation/cal, depreciation
price_lot, var_lot = 1_400.0, 300.0
be = fixed / (price_lot - var_lot)
print(f"fixed cost/yr ${fixed:,.0f}; breakeven {be:,.0f} lots/yr = {be/12:,.0f} lots/month")
for lots_m in (20, 40, 60, 90):
    rev = lots_m * 12 * price_lot
    gm = (rev - lots_m * 12 * var_lot - (3 * 95_000) - capex / 7) / rev
    op = rev - lots_m * 12 * var_lot - fixed
    print(f"{lots_m:3d} lots/mo: revenue ${rev:,.0f}  lab gross margin {gm:5.1%}  operating profit ${op:,.0f}")

# ---------------------------------------------------------------------------
# 7. Federal 'compliant memory' reseller (E-09)
# ---------------------------------------------------------------------------
hdr("7. GSA MAS / SEWP memory reseller")
gm_vars = (0.06, 0.10)
target_gp = 150_000.0
for g in gm_vars:
    sales = target_gp / g
    print(f"GM {g:.0%}: ${sales:,.0f} of sales for ${target_gp:,.0f} gross profit; 45-day working capital ${sales*45/365:,.0f}")

# ---------------------------------------------------------------------------
# 8. STTR vehicle on a lab memory patent (E-10)
# ---------------------------------------------------------------------------
hdr("8. STTR path to first customer revenue (per topic attempt)")
p1, p2, p3 = 0.20, 0.45, 0.35   # P(Ph I award), P(Ph II | I), P(Ph III/customer | II) [ESTIMATE]
p_one = p1 * p2 * p3
for k in (1, 3, 5):
    print(f"{k} independent topic attempts: P(reach customer revenue) = {1-(1-p_one)**k:5.1%}")
months = 2 + 5 + 9 + 24 + 6   # option + proposal-to-award + Ph I + Ph II + Ph III contracting
print(f"months to first Phase III/customer revenue if every step succeeds first time: {months}")

# ---------------------------------------------------------------------------
# 9. SBA-financed acquisition of a small memory reseller at peak earnings (E-11)
# ---------------------------------------------------------------------------
hdr("9. Buy a server-memory reseller at 2026 earnings with SBA 7(a) debt")
ebitda_2026, multiple = 1_200_000.0, 3.5     # [ESTIMATE]
price = ebitda_2026 * multiple
equity = 0.10 * price
loan = price - equity
rate = 0.105                                 # Prime + ~3% [ESTIMATE]
ds = pmt(rate / 12, 120, loan) * 12
print(f"price ${price:,.0f}; equity injection ${equity:,.0f}; loan ${loan:,.0f}; annual debt service ${ds:,.0f}")
for label, e in [("2026 shortage EBITDA", 1_200_000.0), ("normal-year EBITDA", 400_000.0),
                 ("glut EBITDA (2028-29)", 200_000.0)]:
    print(f"{label:24s} ${e:>10,.0f}  DSCR {e/ds:4.2f}")

# ---------------------------------------------------------------------------
# 10. DIMM Health Subscription (E-01)
# ---------------------------------------------------------------------------
hdr("10. DIMM Health Subscription: predictive replacement + spares pool")
dimms = 2_400            # 200 out-of-warranty DDR4 servers x 12 DIMMs [ESTIMATE]
gb = 32
fee = 0.75               # $/DIMM-month [ESTIMATE]
repl_rate = 0.015        # predictive + reactive replacements per DIMM-year [ESTIMATE]
pool_frac = 0.02         # spares stocked as % of covered DIMMs [ESTIMATE]
ship = 18.0
sw = 0.05                # hosting/support $/DIMM-month [ESTIMATE]
for label, usd_gb in [("2026 recovered DDR4 ($4.7/GB)", 4.7), ("glut recovered DDR4 ($1.25/GB)", 1.25)]:
    rev = dimms * fee * 12
    dimm_cost = usd_gb * gb
    cogs = dimms * repl_rate * (dimm_cost + ship) + dimms * sw * 12 \
        + dimms * pool_frac * dimm_cost * 0.20   # 20%/yr carrying+obsolescence on pool
    print(f"{label:32s} revenue/customer ${rev:,.0f}/yr  COGS ${cogs:,.0f}  GM {1-cogs/rev:5.1%}  pool capital ${dimms*pool_frac*dimm_cost:,.0f}")
for ncust in (10, 25, 50):
    print(f"{ncust} customers -> ARR ${ncust*dimms*fee*12:,.0f}")

# ---------------------------------------------------------------------------
# 11. Memory Cost Escalation Index (E-02)
# ---------------------------------------------------------------------------
hdr("11. Memory cost escalation index + EPA clause kit")
arr = 30 * 6_000 + 5 * 24_000
for label, data_cost in [("self-built from distributor APIs", 25_000.0),
                         ("with a licensed contract-price feed", 120_000.0)]:
    print(f"{label:38s} ARR ${arr:,.0f}  GM {(arr-data_cost-8_000)/arr:5.1%}")
# what the index does to a $500k/yr memory-bearing contract when prices move
for move in (+0.25, -0.60):
    print(f"memory share 35% of a $500k contract, memory cost {move:+.0%}: adjustment ${500_000*0.35*move:+,.0f}")

# ---------------------------------------------------------------------------
# 12. CXL tiering integration practice (E-13)
# ---------------------------------------------------------------------------
hdr("12. CXL tiering integration practice")
rate_hr = 225.0
for label, hrs in [("part-time, 8 billable h/wk x 46 wk", 8 * 46), ("full-time, 1,100 billable h", 1_100)]:
    print(f"{label:36s} revenue ${hrs*rate_hr:,.0f}")
# value to a client: DDR4 reuse behind CXL vs buying DDR5 for 1 TB extra per node
for label, ddr5 in [("4Q26", RDIMM64_CONTRACT_USERGB), ("glut", GLUT_RDIMM_USERGB)]:
    print(f"{label}: 1 TB of new DDR5 RDIMM = ${ddr5*1024:,.0f} per node")

# ---------------------------------------------------------------------------
# 13. Memory patent expiry & litigation radar (E-14)
# ---------------------------------------------------------------------------
hdr("13. Memory patent expiry & litigation radar")
subs, price_sub = 25, 4_800.0
print(f"{subs} subscribers x ${price_sub:,.0f} = ARR ${subs*price_sub:,.0f}; one FTO opinion costs $10-30k (p1-ip)")

print("\nall sections done")
```

### Output (2026-11-01 run)

```text

==============================================================================
1. Contract-price volatility (TrendForce conventional DRAM QoQ midpoints)
==============================================================================
annualized vol, 2024-26 points only : 44.0%
annualized vol, incl. 2018-23 busts : 55.1%
index 3Q25=100 -> 4Q26 = 601 (x6.0); glut -60% -> 240

==============================================================================
2. Price-cap subscription: fair premium of a 12-month cap (Black-76)
==============================================================================
sigma 44%  cap at 1.00xF : premium = 16.7% of annual spend
sigma 44%  cap at 1.10xF : premium = 13.1% of annual spend
sigma 44%  cap at 1.25xF : premium =  9.1% of annual spend
sigma 55%  cap at 1.00xF : premium = 20.7% of annual spend
sigma 55%  cap at 1.10xF : premium = 17.3% of annual spend
sigma 55%  cap at 1.25xF : premium = 13.2% of annual spend
sigma 44%: 99th-pct 12-mo price = 2.53xF -> loss on $1M capped spend at ATM = $1,526,555
sigma 55%: 99th-pct 12-mo price = 3.09xF -> loss on $1M capped spend at ATM = $2,092,505

==============================================================================
3. Buy-and-hold DDR5 inventory, 12-month hold from Nov-2026
==============================================================================
squeeze continues  p=0.25 sale $ 30.39/GB  net return -7.7%
plateau            p=0.40 sale $ 19.14/GB  net return -47.4%
soft turn          p=0.25 sale $ 13.67/GB  net return -66.7%
early turn         p=0.10 sale $  8.89/GB  net return -83.6%
buy at $28.31/GB (spot+5%) -> expected 12-mo net return -45.9%
24-mo hold into glut: sale $6.08/GB -> return -108.5%
sensitivity: spot premium stays at 1.69x contract -> expected 12-mo net return -22.5%
(counterfactual) buy at contract $15.99/GB -> expected 12-mo return +7.3%

==============================================================================
4. 36-month lease of a 64GB DDR5 RDIMM (lessor view)
==============================================================================
buy $1,600; base residual $260; severe residual $77
payment for 14% IRR at base residual: $48.83/mo = $0.76/GB-month
full term, base residual   : IRR  14.9%
full term, severe residual : IRR   9.1%
lessee walks at month 18 (glut), recovery $265: IRR -28.6%
lessee walks at month 12,         recovery $265: IRR -58.1%
lessee's alternative in 2028: buy new 64GB at $520 vs remaining 18 payments $879

==============================================================================
5. Title-taking die bank for one legacy DRAM part (10-year horizon)
==============================================================================
base: 3.0x, 90% sells yrs3-8     IRR  16.4%  gross margin on units 55.0%
bear: 2.0x, 50% sells yrs3-8     IRR  -6.8%  gross margin on units 32.5%
bull: 4.0x, 95% sells yrs2-6     IRR  38.8%  gross margin on units 66.2%

==============================================================================
6. AS6171 / DFARS 252.246-7008 test lab for memory lots
==============================================================================
fixed cost/yr $477,857; breakeven 434 lots/yr = 36 lots/month
 20 lots/mo: revenue $336,000  lab gross margin -33.9%  operating profit $-213,857
 40 lots/mo: revenue $672,000  lab gross margin 22.3%  operating profit $50,143
 60 lots/mo: revenue $1,008,000  lab gross margin 41.1%  operating profit $314,143
 90 lots/mo: revenue $1,512,000  lab gross margin 53.6%  operating profit $710,143

==============================================================================
7. GSA MAS / SEWP memory reseller
==============================================================================
GM 6%: $2,500,000 of sales for $150,000 gross profit; 45-day working capital $308,219
GM 10%: $1,500,000 of sales for $150,000 gross profit; 45-day working capital $184,932

==============================================================================
8. STTR path to first customer revenue (per topic attempt)
==============================================================================
1 independent topic attempts: P(reach customer revenue) =  3.1%
3 independent topic attempts: P(reach customer revenue) =  9.2%
5 independent topic attempts: P(reach customer revenue) = 14.8%
months to first Phase III/customer revenue if every step succeeds first time: 46

==============================================================================
9. Buy a server-memory reseller at 2026 earnings with SBA 7(a) debt
==============================================================================
price $4,200,000; equity injection $420,000; loan $3,780,000; annual debt service $612,065
2026 shortage EBITDA     $ 1,200,000  DSCR 1.96
normal-year EBITDA       $   400,000  DSCR 0.65
glut EBITDA (2028-29)    $   200,000  DSCR 0.33

==============================================================================
10. DIMM Health Subscription: predictive replacement + spares pool
==============================================================================
2026 recovered DDR4 ($4.7/GB)    revenue/customer $21,600/yr  COGS $8,946  GM 58.6%  pool capital $7,219
glut recovered DDR4 ($1.25/GB)   revenue/customer $21,600/yr  COGS $3,912  GM 81.9%  pool capital $1,920
10 customers -> ARR $216,000
25 customers -> ARR $540,000
50 customers -> ARR $1,080,000

==============================================================================
11. Memory cost escalation index + EPA clause kit
==============================================================================
self-built from distributor APIs       ARR $300,000  GM 89.0%
with a licensed contract-price feed    ARR $300,000  GM 57.3%
memory share 35% of a $500k contract, memory cost +25%: adjustment $+43,750
memory share 35% of a $500k contract, memory cost -60%: adjustment $-105,000

==============================================================================
12. CXL tiering integration practice
==============================================================================
part-time, 8 billable h/wk x 46 wk   revenue $82,800
full-time, 1,100 billable h          revenue $247,500
4Q26: 1 TB of new DDR5 RDIMM = $20,799 per node
glut: 1 TB of new DDR5 RDIMM = $8,320 per node

==============================================================================
13. Memory patent expiry & litigation radar
==============================================================================
25 subscribers x $4,800 = ARR $120,000; one FTO opinion costs $10-30k (p1-ip)

all sections done
```
