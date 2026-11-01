# 01 — LANDSCAPE (Phase 1 deliverable)

**American Memory · as of 2026-11-01 · lead analyst `p1-synth` · Phase 1b patch `p1b-patch` (2026-11-01)**
**Built from:** `research/phase1/` (market.md, micron_us_makers.md, us_fabs.md, us_backend.md, funding_export.md, cost_stack.md, ip_landscape.md, cost_stack_output.md, price_series.json, cost_inputs.json), the Phase 1b verification logs (`research/phase1/verify_v1-policy.md`, `verify_v2-fabs-ip.md`, `verify_v3-backend.md`, `verify_v4-cost.md`) and `models/dram_cost_stack.py` (re-run 2026-11-01 after the Phase 1b input corrections, exit 0). **Sources:** `SOURCES.md`. **Assumptions:** `research/assumptions/p1-*.md`, synthesis calls in `research/assumptions/p1-synth.md`, verifier calls in `research/assumptions/v*-*.md`.

> **Evidence grade. Read this before quoting any number.** The engagement's shared web-search budget (200 calls) ran out early in Phase 1. Two researchers (p1-market, p1-micron) worked from search snippets; the other five and the modeler had no live web access at all, and the proxy blocked sec.gov, trendforce.com, nist.gov and investors.micron.com. My own three searches were refused, and fetches of placera.se and trendforce.com failed DNS.
>
> **Phase 1b (quota-limited verification pass, 2026-11-01).** Four verifiers (`v1-policy`, `v2-fabs-ip`, `v3-backend`, `v4-cost`) re-checked the decision-critical claims. They used their full quotas (114 WebSearch calls in total). All 11 WebFetch attempts failed DNS, so every check rests on search-result snippets. **Result across 113 checked items: 56 confirmed, 28 corrected, 1 refuted, 23 still unverified, plus 5 new facts** (counts by verifier-log row; rows with mixed labels are counted by their main verdict). Confirmed items were upgraded from [UNVERIFIED] to [REPORTED-P] or [REPORTED]. None became [VERIFIED]. Claims that Phase 1b changed are marked **(1b)**. The summary of what changed is right after §0, and §10.5 gives the item-by-item status.
>
> As a result:
> - **Nothing here is [VERIFIED]** from a primary page opened this session, except the open-source cost repos p1-cost cloned.
> - **[REPORTED-P]** = a primary filing or release (SEC, NIST, Federal Register, company newsroom, TrendForce press center) seen only through a search snippet. **[REPORTED]** = secondary coverage. **[UNVERIFIED]** = researcher's prior knowledge, no URL. **[ESTIMATE]** = computed (mostly `models/dram_cost_stack.py`).
> - The structural conclusions hold up across independent routes. For example, the cost stack lands within 6–7 pp of the reported 86–87% margins. The dated 2026 specifics are the weak points. §10.5 lists what is still open.

---

## 0. Executive summary

**Is the premise intact? Yes, and it is stronger on price and margin than the mission wrote. But the window is shorter, and three implicit assumptions are wrong. Re-aim the search, not the mission.**

1. **Prices rose about 4×, not about 2×.** Conventional DRAM contract prices compound to **≈4.1× from 4Q25 to 4Q26** and **≈6× from 3Q25**. DDR5 16Gb spot went from **$6.84 (Sep-2025) to ~$54–57 (Aug–Sep 2026), ≈8×** (§2) [REPORTED; compounding ESTIMATE].
2. **Margins are ~80%, not "70%+".** SK hynix posted **79.7%** operating margin in 3Q26 (company-wide). Nanya, a commodity maker with no HBM, posted **80.0%** operating and 85.7% gross. Micron's non-GAAP gross margin is **~87%** (§1) [REPORTED].
3. **The cost stack confirms it is a price spike, not a cost moat.** Leading-edge DDR5 costs **$1.48/GB** to make against a **$20.37/GB** 4Q26 contract price, a **93%** gross margin (`models/dram_cost_stack.py`) [ESTIMATE]. (1b) The die-size input is now anchored on a teardown, and the 4Q26 price anchor was raised. Before 1b the figures were $1.64, $15.99 and 90%.
4. **The turn is a 2028 story, inside the founder's 36-month window.** The rate of increase has already fallen from +95.5% QoQ (1Q26) to +12.5% (4Q26F). NAND is forecast to go into surplus in 2H27. 2028 brings bit growth of 20–30%+, Micron ID2, Samsung P5, SK hynix Yongin and CXMT at ~420–500K wpm (§2.3, §5).
5. **A 60% glut barely touches incumbents.** At **$8.15/GB** they still earn ~82% gross margin. It kills **entrants** whose cost sits above ~$8/GB. **No alternative memory measured comes within 10× of DDR5's cost per GB** (§4). (1b) Before 1b these were $6.40/GB and 74%; the conclusion is now stronger.
6. **The U.S. has no DRAM foundry, no display/TFT fab and no open DRAM die supply.** Micron Manassas is the only U.S. DRAM production and takes no outside customers. "Trailing-node DRAM on depreciated U.S. capacity" has no host (§6).
7. **There is no general "Made in USA" premium for memory.** TAA treats Korean, Taiwanese and Japanese DRAM as equal to U.S. DRAM. Memory pays 0% under Section 232 Phase 1. The 100% memory-tariff threat is unimplemented (§7, §8).
8. **The policy lever that does create a buyer is provenance, but the product it pays for is mostly paperwork software, not a lab.** NDAA FY2023 §5949 bars federal agencies from buying products containing **CXMT, YMTC or SMIC** chips from **2027-12-23** (417 days out). It rewards "verified non-Chinese", not "U.S.-made" (§7). (1b) The FAR rule is only a **proposed rule** (FAR Case 2023-008, published 2026-02-17), with no final rule as of 2026-11-01.
   - **Scope is wide.** The rule covers COTS products, so memory inside servers, PCs and DIMMs is included.
   - **The proof standard is light.** Contractors meet it by "reasonable inquiry" and may rely on supplier certifications, with no third-party audit required. The rule applies prospectively, and Part B reaches only "critical systems".
   - **What that means for a product.** The paid need is mostly certification and BOM-traceability workflow. X-ray and decap screening becomes an exception-driven add-on.
   - **A funded competitor exists.** OBSIDIA holds a $34M CHIPS R&D letter of intent for counterfeit-component identification [REPORTED-P/REPORTED].
9. **Big federal money is closed to a new entrant.** CHIPS is ≈$0 for us. (1b) Two CHIPS funding opportunities are open, so the old "no open NOFO" claim was wrong. Neither fits: one is a facilities NOFO, and the other is the equity-linked CRDO BAA, with a reported ~$10M minimum. The 35% §48D credit requires construction to start by **2026-12-31** (60 days). Commerce voided the agreement with the NSTC operator, Natcast, in Aug 2025, and NIST has since taken over NSTC operations without publishing a membership model [REPORTED]. Only SBIR/STTR, lab licensing and small state matches remain. (1b) **SBIR/STTR was reauthorized through 2031-09-30** (signed 2026-04-13) [REPORTED-P]. **The SBIR PI rule (confirmed) excludes a founder who keeps their day job** (§7).
10. **Die supply is the choke point; assembly is ~1% of module value.** Micron sells no open KGD (its 10-K lists wafers, not KGD). The only doors are SpecTek wafers (terms still unknown) and Taiwanese specialty KGD from Winbond and ESMT (both confirmed) and Etron (unconfirmed). All are legacy densities. (1b) Legacy 4Gb DDR4 KGD can be bought from distributors in lots of a few hundred die (§6.3).
11. **DDR4 is the tightest segment now and will be the first to collapse.** It inverted over DDR5 twice. Micron's new U.S. DDR4 (Manassas, 1-alpha, since 2026-05-22) targets exactly the long-lifecycle buyer a small venture would chase. (1b) Micron has signed Strategic Customer Agreements with Ford, GM and seven auto Tier-1s, and it is the only supplier publicly committed to ongoing DDR4/LP4 (§3.3).
12. **Licensable, U.S.-manufacturable memory IP exists only for embedded or niche NVM.** All DRAM-class IP is closed to a startup (§9). (1b) The three leads have each changed:
    - **Weebit ReRAM in SkyWater S130:** qualified (confirmed), but it is **not a T0 path**. SkyWater has been IonQ-owned since 2026-07-31. The cheap Efabless prototype route died with Efabless. Weebit's existing licensees paid an estimated $0.1–2.6M upfront, plus NRE and royalties.
    - **Sandia HZO FeRAM:** downgraded to an *unconfirmed* lead, because no licensing listing or CRADA offer was found.
    - **OpenRAM SRAM:** still open.

**The five facts that matter most for picking a venture:**

| # | Fact | Why it decides the pick |
|---|---|---|
| F1 | Incumbent DDR5 cost is $1.48/GB (1b; was $1.64). The glut price is $8.15/GB (1b; was $6.40). Alternatives cost $55–1,600/GB (SRAM) and ~$90/GB (MRAM, model), with MRAM street prices at ~$821/GB (confirmed) | Any device concept must win on a **non-$/GB axis** (retention, non-volatility, radiation, lifecycle, provenance) or it dies |
| F2 | The downturn most likely starts in 2028; NAND leads in 2H27 | Price-arbitrage concepts (recert, brokerage, legacy supply) must be **cash-positive by end-2027** |
| F3 | No U.S. DRAM foundry or display fab; die closed (small legacy KGD lots excepted); assembly ~1% of value | Kills U.S. fab, foundry and "assembled in USA module" concepts; pushes toward **services and software** |
| F4 | §5949 (2027-12-23; FAR rule still *proposed*) plus DFARS counterfeit rules create paid demand for **provenance and traceability**. (1b) Supplier certification after "reasonable inquiry" satisfies the rule, so the demand is mostly **attestation/BOM-traceability workflow**; lab test is an exception-driven add-on | The only policy-made buyer that fits T0–T1 capital and a software founder, and it is **glut-proof**. (1b) The fit with a software founder got *better*; the ticket size got *smaller*; one funded competitor (OBSIDIA) exists |
| F5 | Non-dilutive money = SBIR/STTR (reauthorized to 2031-09-30; full-time or university PI), university license, state matches. (1b) Sandia licensing is unconfirmed | A device path needs a **technical co-founder or university PI**; the founder alone can't be PI |

### What changed in Phase 1b

Four verifiers re-checked the decision-critical facts on 2026-11-01. Their change logs are `research/phase1/verify_v1-policy.md`, `verify_v2-fabs-ip.md`, `verify_v3-backend.md` and `verify_v4-cost.md`. These are the changes that matter for the pick:

1. **§5949: the scope and date held, but the product shape changed.** (Conclusion revised.)
   - **What held:** the prohibition date (2027-12-23) and the COTS coverage, which includes memory inside servers, PCs and DIMMs.
   - **What changed:** the FAR rule is only proposed (2026-02-17), and no final rule existed as of 2026-11-01, so the statutory deadline was missed. "Reasonable inquiry" lets contractors rely on supplier certifications without third-party audits. The rule applies prospectively, with no rip-and-replace. There is no Section-889-style ban on contractors' internal use.
   - **What that means:** O1's core product becomes certification and traceability workflow for federal resellers and integrators. X-ray and decap screening becomes a smaller add-on.
   - **New competitor:** OBSIDIA ($34M CHIPS R&D LOI, 2026-07-29) is a funded competitor, and also a possible partner or acquirer ([Federal Register](https://www.federalregister.gov/documents/2026/02/17/2026-03065/federal-acquisition-regulation-prohibition-on-certain-semiconductor-products-and-services); [Wiley](https://www.wiley.law/alert-FAR-Council-Proposes-Rule-to-Ban-Purchases-of-Certain-Semiconductor-Products-and-Services); [NIST](https://nist.gov/news-events/news/2026/07/department-commerce-announces-letters-intent-7-companies-874-million)) [REPORTED-P/REPORTED].
2. **SBIR/STTR is back through 2031-09-30.** (Status confirmed; the conclusion holds.)
   - **The law:** S. 3971 was signed on 2026-04-13. The PI rule is confirmed, so the founder cannot be SBIR PI while keeping their day job; STTR with a university PI is still the route.
   - **What is new:** Strategic Breakthrough awards (up to $30M, which require a prior Phase II and a 1:1 match); per-firm proposal caps from FY2027; heavier foreign-ownership screening ([IEDC](https://www.iedconline.org/news/2026/04/15/federal-policy-updates/federal-policy-update-sbir-and-sttr-reauthorized/); [Wiley](https://www.wiley.law/alert-SBIR-STTR-Reauthorization-Brings-New-Opportunities-and-Obligations-to-Consider)).
3. **Weebit ReRAM on SkyWater is no longer a cheap entry.** (Conclusion revised: entry moves from T0 to T1.)
   - **Ownership:** IonQ closed its acquisition of SkyWater on 2026-07-31.
   - **Prototype route:** the Efabless chipIgnite ReRAM shuttle died with Efabless, and nothing shows that ChipFoundry carries the block.
   - **Fees:** existing licensees paid analyst-estimated upfront fees of ~$0.1M (first-ever licence) to $0.29M (DB HiTek) and $1.8–2.6M (onsemi), plus NRE and royalties.
   - **Tape-outs:** none of Weebit's three customer tape-outs is tied to S130.
   - **Sandia:** downgraded from best lead to unconfirmed lead.
   - **Cheapest open silicon now:** GF180 via wafer.space (~$7k for 1,000 dies), which offers no NVM ([Quantum Insider](https://thequantuminsider.com/2026/07/31/ionq-completes-skywater-acquisition-quantum-manufacturing/); [StorageNewsletter](https://www.storagenewsletter.com/2024/06/05/weebit-nano-and-efabless-collaborate-to-enable-prototyping-of-soc-designs/); [MST](https://www.weebit-nano.com/wp-content/uploads/2025/09/250901.-MST-Access-Report_WBT.AX-Not-just-play-money-090125.pdf); [Crowd Supply](https://www.crowdsupply.com/wafer-space/gf180mcu-run-2)).
4. **The used-DDR4 kill check passed.** (O3's open test is resolved.)
   - **Prices:** realized resale over the trailing 12 months to Aug 2026 was $3.1–5.8/GB: $100–150 for 32GB and $250–370 for 64GB. That is above the $2/GB kill line, and the recert contribution re-computes to 17–23%.
   - **Cautions:** Iron Mountain's ITAD arm nearly doubled on volume *and* pricing, so incumbents are capturing the repricing and buy-side lots will cost more. The glut verdict (~1–6%) is unchanged.
   - **New:** used 64GB DDR5 RDIMMs resell at $890–1,200 ($14–19/GB, 55–74% of new) ([amcompute](https://www.amcompute.com/appraisals/ddr4-64gb-rdimm); [MarketBeat](https://www.marketbeat.com/instant-alerts/iron-mountain-q2-earnings-call-highlights-2026-08-08/)) [REPORTED].
5. **Cost-stack decks moved, and no decision flips.**
   - **Inputs:** the 1-beta 16Gb die is 35.8 mm² per teardown, versus 41 mm² assumed. The 4Q26 RDIMM anchor rose from $1,300 to $1,650.
   - **Outputs:** incumbent cost went from $1.64 to $1.48/GB, the contract deck from $15.99 to $20.37/GB and the glut line from $6.40 to $8.15/GB. Gross margin went from 90% to 93%, and glut gross margin from 74% to 82%.
   - **Remaining gap:** the model now sits 6–7 pp above reported margins, which hints that the $3.8k 1-beta wafer is understated. A ~$5k wafer would give ~$1.9/GB and change no decision (§4).
6. **CHIPS: wrong reason, same answer.** Two opportunities are open, but both are capex-scale or equity-linked. Kepler's $245M LOI shows Commerce funds ferroelectric AI memory, but at T3 scale in exchange for equity.
7. **Smaller corrections:**
   - **Everspin:** U.S.-made STT-MRAM slips to ~late 2028, and Gresham stays exclusive to Everspin until at least 2038.
   - **Micron:** has locked up the auto long-lifecycle buyers, which pushes O4 toward mid-size industrial and medical OEMs and services.
   - **BIS affiliates rule:** legally returns on 2026-11-10 unless BIS publishes the announced extension to 2027-01-10.
   - **CXMT:** still not on the Entity List (as of 2026-08-31).
   - **Netlist:** reportedly licensed Samsung in 2026, so the hazard for an unlicensed DDR5 RDIMM maker grew.

**What did not change:** the re-aim (§1), the closed list (§10.2), the 2028 turn, "no Made-in-USA premium for memory" (§232 Phase 1 confirmed; Phase 2 not found) and the glut logic.

---

## 1. Premise verification (mission §1, bullet by bullet)

| # | Claim in mission §1 | Verdict | Corrected wording, with dated sources |
|---|---|---|---|
| 0 | "The world needs more RAM and the U.S. makes very little of it." | **CONFIRMED** | U.S. share of global DRAM bits is **~1–2% in 2026** (bounds 0.7–2.1%), rising to **~5–6% by 2030** and **~9–10% by 2035** if Micron hits its 40%-in-U.S. goal [ESTIMATE, micron_us_makers.md §5]. TrendForce (2026-07-30) says the DRAM supply-demand gap **widens** in 2027 ([TrendForce](https://www.trendforce.com/presscenter/news/20260730-13158.html)) [REPORTED-P]. |
| 1a | "DRAM and NAND prices roughly doubled or more from late 2025 through 2026" | **CORRECTED: understated ~2×** | Conventional DRAM contract **≈4.1× 4Q25→4Q26** (range 3.8–4.4×) and **≈6× from 3Q25**. Inputs: 1Q26 +93–98% actual ([TrendForce 2026-06-01](https://www.trendforce.com/presscenter/news/20260601-13070.html)); 2Q26 +58–63% F ([TechNews 2026-03-31](https://technews.tw/2026/03/31/ai-server-demand-drives-2q26-memory-contract-price-increase-csps-lock-supply-long-term-deals/)); 3Q26 +13–18% F ([Igor'sLAB](https://www.igorslab.de/en/dram-and-nand-remain-more-expensive-trendforce-sees-slowing-but-still-rising-memory-prices-q3-2026/)); 4Q26 +10–15% F ([TrendForce 2026-09-30](https://www.trendforce.com/presscenter/news/20260930-13258.html)). DDR5 16Gb spot **$6.84 → $53.92 (2026-08-31), ≈8×** ([tech-insider](https://tech-insider.org/ddr5-ram-prices-2026/); [BuySellRAM](https://www.buysellram.com/blog/ram-market-update/)). NAND ≈**3.2×** over 1Q, 2Q and 4Q26 alone [REPORTED; compounding ESTIMATE]. |
| 1b | "…as AI/HBM demand absorbed wafer capacity…" | **CONFIRMED** | HBM takes **~18% / 22% / ~30%** of big-3 DRAM wafer starts in 2025 / 2026 / 2027F, but only **~8% / 9% / 13%** of bits ([TechNews/TrendForce](https://technews.tw/?p=1565421)). Micron puts the HBM-to-DDR5 wafer trade ratio at **~3:1, widening with every generation** ([Tom's Hardware](https://www.tomshardware.com/tech-industry/semiconductors/micron-says-the-silicon-gap-between-hbm-and-ddr5-is-widening-with-every-generation)) [REPORTED]. |
| 1c | "…and DDR4 lines were cut." | **CORRECTED** | Micron issued DDR4 EOL notices in **Jun 2025**. **Samsung and SK hynix pushed their DDR4 exits into 2026** because DDR4 became a cash cow ([TrendForce News 2025-09-02](https://www.trendforce.com/news/2025/09/02/news-samsung-sk-hynix-reportedly-delay-phase-out-to-2026-as-ddr4-becomes-unexpected-cash-cow/)). Micron then **started 1-alpha DDR4/LP4 in Manassas on 2026-05-22** for auto, defense and industrial buyers ([HPCwire/Micron](https://www.hpcwire.com/off-the-wire/micron-advances-made-in-america-memory-with-manufacturing-expansion-in-virginia)) [REPORTED]. Commodity DDR4 was cut; long-lifecycle DDR4 is being re-made in the U.S. |
| 1d | "TrendForce has been forecasting further double-digit contract-price increases into Q4 2026" | **CONFIRMED, decelerating** | Release of 2026-09-30: conventional DRAM **+10–15% QoQ**, **+15–20% including HBM**, NAND **+15–20%** ([TrendForce](https://www.trendforce.com/presscenter/news/20260930-13258.html); [Guru3D](https://www.guru3d.com/story/dram-and-nand-contract-prices-forecast-to-rise-as-much-as-in-q4-2026/)) [REPORTED-P]. A reported Oct-20 revision to "~+20%" is **[UNVERIFIED]**. (1b) The only source for it is an AI-generated summary that cites no TrendForce release ([StockHub](https://www.stockhub.kr/en/news/news_b7244c205001)), so it is kept only as the model's high case. The QoQ rate fell from +95.5% (1Q26) to +12.5% (4Q26F). NAND contract was reportedly **flat in Oct 2026** ([tech-insider](https://tech-insider.org/dram-record-high-nand-flat-21-months-october-2026/)) [UNVERIFIED]. |
| 1e | "…meaningful supply relief is widely called a late-2027-or-later story." | **CONFIRMED; consensus has moved to 2028** | Micron (2026-09-30): tight through 2028; new cleanroom output only from late 2028 ([Guru3D](https://www.guru3d.com/story/micron-expects-dram-and-nand-supply-to-tighten-further-through-2028/)). SK hynix: 14 LTAs, supply booked to 2029 ([Sammy Fans 2026-10-28](https://www.sammyfans.com/2026/10/28/sk-hynix-q3-margin-hits-record-80-secures-14-ltas-with-memory-supply-booked-to-2029/amp/)). Barclays: 13.9% deficit in 4Q27 ([Guru3D](https://www.guru3d.com/story/ddr4-memory-prices-now-also-rise-as-dram-supply-shortages-intensify-through-2028/)). Minority view: Bloomberg Intelligence says the shortage peaked in 2Q26 and balances ~4Q27 ([KuCoin summary](https://www.kucoin.com/blog/2027-memory-chip-boom-sk-hynix-samsung)) [REPORTED]. |
| 2a | "Operating margins on general-purpose DRAM have been extraordinary (70%+ reported for SK hynix)." | **CORRECTED upward and re-scoped** | SK hynix 3Q26: **KRW 83.3T OP on KRW 104.6T = 79.7%**; 2Q26 76.3% ([3Q26](https://www.placera.se/pressmeddelanden/sk-hynix-announces-3q26-financial-results-20261028); [2Q26](https://www.placera.se/pressmeddelanden/sk-hynix-announces-2q26-financial-results-20260729)) [REPORTED-P]. These are **company-wide** margins including HBM and NAND. The cleanest pure-commodity proxy is **Nanya 3Q26: 85.7% GM, 80.0% OM** ([TrendForce News](https://www.trendforce.com/news/?p=65146)). **Micron FQ4-26 non-GAAP GM ~87%; FQ1-27 guide 86.25%** ([Finviz/Micron](https://finviz.com/news/397277/micron-technology-inc-reports-record-fiscal-fourth-quarter-and-full-year-2026-results)). **Samsung DS 3Q26 72.4%**, including loss-making foundry ([Samsung](https://news.samsungsemiconductor.com/global/samsung-electronics-announces-third-quarter-2026-results/)) [REPORTED]. |
| 2b | "Margin is captured by three foreign-headquartered firms plus Micron." | **CORRECTED** | 2Q26 DRAM revenue shares: Samsung 39.4%, SK hynix 24.9%, Micron 23.3%, **CXMT 9.5%**, with Nanya and Winbond taking the rest ([Evertiq/TrendForce](https://evertiq.com/news/2026-09-07-dram-industry-revenue-surges-595-in-q2-as-supply-lags-demand); [Herald](https://biz.heraldcorp.com/article/10866656)) [REPORTED]. CXMT raised ~$8.5B in a July 2026 IPO with **no HBM project**, so all of its growth is conventional bits ([Tom's Hardware](https://www.tomshardware.com/tech-industry/cxmt-closes-up-466-percent-in-shanghai-debut-with-no-hbm-project-in-its-ipo-prospectus)). |
| 3a | "Micron is the only U.S.-headquartered DRAM maker." | **CONFIRMED (nuance)** | Micron is also the only company making DRAM wafers on U.S. soil ([eeNews Europe 2026-05](https://www.eenewseurope.com/en/micron-ramps-us-made-ddr4-production-in-virginia/); [Taipei Times 2026-01-19](https://www.taipeitimes.com/News/biz/archives/2026/01/19/2003850817)) [REPORTED]. It is not the only U.S. *memory* maker: Everspin (Toggle MRAM, Chandler AZ), Honeywell (rad-hard SRAM/MRAM) and TI (embedded FRAM, captive) also make memory here (§6). |
| 3b | "First Idaho fab targets first DRAM wafer output around mid-2027." | **CONFIRMED (pulled in); meaningful output 2028** | FY2026 10-K: "first DRAM wafer output in mid-calendar 2027" ([Micron 10-K](https://www.sec.gov/Archives/edgar/data/0000723125/000072312526000023/mu-20260903.htm)) [REPORTED-P]. A Micron VP said meaningful, customer-qualified output comes in **2028** ([OC3D](https://overclock3d.net/?p=304658)) [REPORTED]. |
| 3c | "Second Idaho fab initial output late 2028." | **CONFIRMED** | Construction began 2026; initial wafer output late CY2028 ([Micron 10-Q FQ3-26](https://www.sec.gov/Archives/edgar/data/0000723125/000072312526000015/mu-20260528.htm)) [REPORTED-P]. |
| 3d | "First New York fab (ground broken Jan 2026)." | **CONFIRMED** | Groundbreaking **2026-01-16**, Clay NY ([The Register](https://www.theregister.com/2026/01/16/micron_fab_breaks_ground/)). First concrete July 2026, ahead of plan ([W.Media](https://w.media/micron-begins-vertical-construction-at-clay-fab-ahead-of-schedule/)) [REPORTED]. |
| 3e | "…supply in 2030 and beyond." | **CONFIRMED after a slip** | 10-K: initial wafer output **CY2030** [REPORTED-P]. The Nov-2025 EIS moved fab 2 to late 2033 and fab 4 to 2041 ([Construction Dive](https://www.constructiondive.com/news/micron-delay-construction-new-york-megafab/805622/)) [REPORTED]. |
| 3f | "…backed by up to $6.1B in CHIPS Act direct funding." | **CONFIRMED, refined** | Final award **up to $6.165B** (2024-12-10; ~$4.6B NY, ~$1.5B ID), amended Jun-2025 to add ID2 ([NIST](https://www.nist.gov/node/1855121)), plus **$275M** for Manassas ([NIST PMT](https://www.nist.gov/node/1869301)) [REPORTED-P]. Total ≈**$6.44B** [ESTIMATE]. No equity conversion found. **The 35% §48D credit is worth 3–8× more to Micron** ($17.5–52.5B on $50–150B of property) [ESTIMATE, micron_us_makers.md §1.6]. |
| 3g | "…plus a Manassas, VA expansion…" | **CONFIRMED; producing** | 1-alpha DRAM production started **2026-05-22**. The project is >$2B, quadruples DDR4 wafer supply and targets qualified output by end-2026 ([HPCwire](https://www.hpcwire.com/off-the-wire/micron-advances-made-in-america-memory-with-manufacturing-expansion-in-virginia); [Evertiq](https://evertiq.com/design/2026-05-26-micron-starts-1a-dram-production-at-virginia-fab-in-usd-2-billion-expansion)) [REPORTED]. (1b) This is confirmed. Micron also has Strategic Customer Agreements with Ford, GM and Tier-1s ([Counterpoint](https://counterpointresearch.com/cn/reports/memory-crisis-automotive-industry-suppliers-automakers-response)) [REPORTED]. |
| 3h | "…and plans for U.S. HBM packaging." | **CONFIRMED as intent only** | No site, date or capacity. Planned "following the completion of" ID2 ([The Manufacturer](https://www.themanufacturer.com/articles/micron-technology-announces-200bn-investment-in-semiconductor-manufacturing-and-rd-in-idaho-new-york-and-virginia/)), so **not before 2029–30** [ESTIMATE]. Micron's actual new HBM packaging is in Singapore, from early CY2027 (10-K) [REPORTED-P]. |
| 3i | "Micron discontinued its Crucial consumer brand in late 2025." | **CONFIRMED, timing corrected** | Announced **2025-12-03**; consumer shipments continued **through late Feb 2026**; Micron-branded enterprise channel products continue ([StorageNewsletter](https://www.storagenewsletter.com/2025/12/05/micron-announces-exit-from-crucial-consumer-business/)) [REPORTED]. |
| 4a | "Memory is brutally cyclical. Every prior shortage ended in a glut." | **CONFIRMED** | 2018–19: 8GB module contract **$68 → $25.50, −62.5% in ~4 quarters** ([TrendForce 2018](https://press.trendforce.com/node/view/3173.html); [DigiTimes](https://www.digitimes.com/tag/8gb/0034884.html)). 2022–23: DDR4 8Gb fixed price bottomed at **$1.30 (Sep 2023)** ([KED Global](https://www.kedglobal.com/korean-chipmakers/newsView/ked202310040013)); SK hynix posted a **−KRW 3.4T (≈−67%)** operating loss in 1Q23 ([The Register](https://www.theregister.com/2023/04/27/samsung_sk_hynix_losses/)) [REPORTED]. |
| 4b | "Any concept that takes five years to reach product may land in a 2029 price crash." | **CORRECTED: sharper** | The turn is most likely **2028**: BofA −10% ASP, Baird >30% bit growth, BI possible oversupply ([TMGM/Baird](https://www.tmgm.com/en/analysis/market-insight/micron-dram-supply-tightening); [KuCoin](https://www.kucoin.com/blog/2027-memory-chip-boom-sk-hynix-samsung)) [REPORTED]. **Even an 18-month concept lands at the turn.** |
| — | *Implicit:* "'Made in America' is … a potential moat." | **CORRECTED** | No tariff, TAA or BAA premium for U.S.-made memory today (§7.3, §8). The paying needs are **provenance** (§5949) and **trusted/rad-hard** supply. |
| — | *Implicit:* CHIPS money and cheap U.S. capital are available to an entrant | **REFUTED** | CHIPS ≈$0 for new entrants; §48D closes 2026-12-31; NSTC unavailable; no idle U.S. display fab (§6, §7). (1b) Two CHIPS opportunities *are* open: a facilities NOFO with concept plans due 2026-11-01, and the CRDO BAA, paused since 2026-09-15. Both are capex-scale or equity-linked ([Mayer Brown 2026-08-10](https://www.mayerbrown.com/en/insights/publications/2026/08/chips-act-funding-opportunities-what-companies-in-the-semiconductor-ecosystem-need-to-know)) [REPORTED]. The verdict stands. |
| — | *Mission §3C capacity list* | **CORRECTED** | Amkor AZ is logic 2.5D packaging starting ~early 2028, not memory capacity. (1b) This is now confirmed: the plan is ~$12B including phase 2, with TSMC and NVIDIA deals attached and no HBM or DRAM packaging ([GPEC 2026-09-08](https://www.gpec.org/?p=31279)) [REPORTED]. SkyWater is MN + FL + **TX**, and since 2026-07-31 it is an **IonQ subsidiary** (1b). Everspin makes only Toggle MRAM in the U.S.; its STT-MRAM comes from GF Singapore. TI Lehi kept no 3D XPoint capability ([AnandTech](https://www.anandtech.com/show/16800)) (§6). |

**Re-aim, plainly stated.** The mission ("find a profitable way to make RAM, or something that does RAM's job better, in the U.S.") stands. Its literal reading, *make cheaper DRAM bits in the U.S.*, is closed. It needs a fab or foundry that does not exist for outsiders, die that is not sold to small buyers, and capital programs that have closed, and it would land in the 2028 turn at a cost above the glut price. **Re-aim the search toward four things:** (1) provenance and supply-security services; (2) memory-efficiency software that makes existing DRAM go further; (3) niche non-volatile parts on licensable U.S. IP that win on a non-$/GB axis; (4) short-window arbitrage only if it turns into (1) before 2028.

---

## 2. Price history, 2024 → Nov 2026, and the relief timeline

### 2.1 TrendForce quarterly contract-price changes (midpoints; from `price_series.json`)

| Quarter | Conv. DRAM QoQ | Status | Incl. HBM | NAND | Index (3Q25=100) [ESTIMATE] | Source |
|---|---|---|---|---|---|---|
| 1Q24 | +15.5% (13–18) | F | — | — | — | [StorageNewsletter](https://www.storagenewsletter.com/2024/01/11/dram-contract-prices-projected-to-increase-13-18-in-1q24/) |
| 2Q24 | +15.5% (13–18) | F | — | — | — | [StorageNewsletter](https://www.storagenewsletter.com/2024/05/16/dram-contract-prices-for-2q24-adjusted-to-13-18-increase/) |
| 3Q24 | +10.5% (8–13) | F | — | — | — | [TrendForce](https://www.trendforce.com/presscenter/news/20240815-12254.html) |
| 4Q24 | +2.5% (0–5) | F, [UNVERIFIED] | — | — | — | [TechPowerUp repost](https://techpowerup.com/forums/threads/329219) |
| 1Q25 | decline (DDR4 −10–15%) | F | — | — | — | [I-Connect007](https://mail.iconnect007.com/article/143527/passive-buyer-strategies-drive-dram-contract-prices-down-across-the-board-in-1q25/143524/ein) |
| 2Q25 | −2.5% (−5–0) | F | +5.5% | — | — | [TechPowerUp repost](https://techpowerup.com/forums/threads/334591) |
| 3Q25 | up (size not captured); industry revenue +30.9% to $41.4B | — | — | — | **100** | [China Times](https://wantrich.chinatimes.com/news/20251126900578-420201) |
| 4Q25 | **+47.5%** (45–50) | A | +52.5% | — | 148 | [TrendForce](https://www.trendforce.com/presscenter/news/20260226-12937.html) |
| 1Q26 | **+95.5%** (93–98) | A | +82.5% F | +57.5% | 288 | [TrendForce](https://www.trendforce.com/presscenter/news/20260601-13070.html); [TrendForce](https://www.trendforce.com/presscenter/news/20260202-12911.html) |
| 2Q26 | **+60.5%** (58–63) | F | — | +72.5% | 463 | [TechNews](https://technews.tw/2026/03/31/ai-server-demand-drives-2q26-memory-contract-price-increase-csps-lock-supply-long-term-deals/) |
| 3Q26 | **+15.5%** (13–18) | F (Aug PC update: above forecast) | — | — | 535 | [Igor'sLAB](https://www.igorslab.de/en/dram-and-nand-remain-more-expensive-trendforce-sees-slowing-but-still-rising-memory-prices-q3-2026/) |
| 4Q26 | **+12.5%** (10–15) | F | +17.5% | +17.5% | **601** (550–657) | [TrendForce](https://www.trendforce.com/presscenter/news/20260930-13258.html) |

Consistency check: TrendForce DRAM industry revenue goes $53.58B (4Q25) → ≈$97.0B (1Q26) → **$154.73B (2Q26)**, matching the price path with roughly flat bits ([Evertiq](https://evertiq.com/news/2026-09-07-dram-industry-revenue-surges-595-in-q2-as-supply-lags-demand)) [REPORTED].

### 2.2 Price levels in $/GB

| Product | 2023 trough | Jun–Sep 2025 | 2026 | Source |
|---|---|---|---|---|
| DDR4 8Gb contract (=$/GB) | **$1.30** (Sep-23) | $2.60 (Jun-25) | — (no legacy contract series; model assumes parity with DDR5) | [KED Global](https://www.kedglobal.com/korean-chipmakers/newsView/ked202310040013); [Asia Economy](https://view.asiae.co.kr/en/article/2025070108020310879) |
| DDR5 16Gb spot | ~$1.6 [UNVERIFIED] | $3.0 (Jun-25); **$3.42** (2025-09-20) | $19.8 (Mar-26); **$26.96** (2026-08-31); ~$28.5 (Sep-26) [UNVERIFIED] | [TrendForce News](https://www.trendforce.com/news/2025/06/24/news-historic-ddr4-spot-price-rally-reportedly-doubles-ddr5-propelling-nanya-techs-inventory-windfall/); [tech-insider](https://tech-insider.org/ddr5-ram-prices-2026/); [DRAMeXchange](https://www.dramexchange.com/); [BuySellRAM](https://www.buysellram.com/blog/ram-market-update/) |
| DDR4 16Gb vs DDR5 16Gb chip | — | $4.6 vs $3.0 (Aug-25): **first inversion** | — | [TechRadar/DigiTimes](https://www.techradar.com/computing/memory/want-to-upgrade-the-ddr4-ram-in-your-pc-new-report-is-a-clear-signal-you-should-buy-sooner-rather-than-later) |
| DDR4 8Gb spot | <$3 (Jun-19, prior cycle) | — | $16 (Jun-26) → $21 (Aug-26, board); branded **$44.37** (2026-08-31); (1b) **$46.36** (2026-10-20, +0.84% WoW) [REPORTED-P] | [TrendForce board](https://www.trendforce.com/price_dram.html); [Mobius](https://www.mobiusmaterials.com/whitepapers/dram-market-report-2026); [BuySellRAM](https://www.buysellram.com/blog/ram-market-update/); [TrendForce 2026-10-21](https://www.trendforce.com/news/?p=65594) |
| 64GB DDR5 RDIMM contract (per user GB) | — | $450 = $7.0 (4Q25) | (1b) **$927 = $14.5 (1Q26 actual)** [REPORTED-P]; Counterpoint 3Q26F ~$1,500; model 4Q26 base **$1,650 = $25.78** (was $1,300); Citi 4Q26F $1,586 [REPORTED, secondary relay only] | [EE Times Asia/Counterpoint](https://www.eetasia.com/memory-prices-surging-by-90-from-4q-2025/); [Counterpoint Apr-26](https://counterpointresearch.com/de/reports/memory-price-tracker-april-2026); [Counterpoint Jul-26](https://counterpointresearch.com/en/reports/memory-price-tracker-and-forecast-july-2026); [Servnet](https://www.servnetuk.com/research/ddr5-server-memory-price-tracker-2026); `models/dram_cost_stack.py` |
| 64GB DDR5 RDIMM street | — | — | ~$2,064 = ~$32 (Aug-26) | [Servnet](https://www.servnetuk.com/research/ddr5-server-memory-price-tracker-2026) |
| (1b) **Used server RDIMMs, realized resale** (12 months to Aug-26) | 2023–24: 32GB DDR4 ~$23–45; 64GB DDR4 ~$65–130 (implied from YoY change) [ESTIMATE] | — | 32GB DDR4 **$100–150 ($3.1–4.7/GB)**; 64GB DDR4 **$250–370 ($3.9–5.8/GB)**; 64GB DDR5 **$890–1,200 ($14–19/GB**, ~55–74% of new) [REPORTED] | [amcompute 32GB](https://www.amcompute.com/appraisals/ddr4-32gb-rdimm); [amcompute 64GB](https://www.amcompute.com/appraisals/ddr4-64gb-rdimm); [amcompute DDR5](https://www.amcompute.com/appraisals/ddr5-64gb-rdimm) |
| Mobile LPDDR5X LTA ceiling | — | — | up to ~$21 (~May-26) | [Wccftech](https://wccftech.com/mobile-dram-prices-expected-to-increase-by-100-quarter-over-quarter-as-long-term-agreements-now-getting-signed-at-prices-as-high-as-21-gb/amp/) |
| HBM3E contract / HBM4 2027 ask | — | — | **$12** ($1.50/Gb; 1b: $1.50–1.60/Gb confirmed, DigiTimes Jul-26) / $36–39; (1b) HBM4 2H26 ~$16/GB [REPORTED] | [Sammy Fans](https://www.sammyfans.com/2026/10/02/samsung-seeks-more-than-3x-hbm3e-pricing-for-hbm4/); [Capital & Compute](https://capitalandcompute.net/memory-prices/hbm/) |
| U.S. retail DDR5 | — | 32GB kit $100–200 (Oct-25) | **$18.04/GB** typical (Sep-26); 32GB kit ~$450 = $14 | [rampricesusa](https://rampricesusa.com/insights/monthly/2026-09); [Digital Citizen](https://www.digitalcitizen.life/ddr5-ram-prices-surge-in-2026-as-32gb-kits-reach-450-amid-global-memory-shortage/) |
| DDR3 4Gb spot | — | — | $25.5/GB (Jul-26) | [Wccftech](https://wccftech.com/memory-shortages-drive-ddr4-prices-over-50-in-q3-2026-ddr3-also-impacted-by-higher-costs/) |

Reading the table:
- Pre-spike DRAM sold at **$1.3–3.4/GB**. 2026 contract is **~$14–20/GB** at the component level, or ~$26 per RDIMM user-GB in 4Q26, and spot is **~$27/GB**.
- (1b) **Used DDR4 RDIMMs sell at $3.1–5.8/GB**, only ~7–28% of DDR4 chip spot per GB. Server x4 die do not fit the consumer boards the spot price reflects. In 2026, counterfeiters re-soldered DDR4 chips onto fake DDR5 boards (us_backend.md §6.3, §6.5).
- **Retail ($14–18/GB) is below chip spot ($27/GB).** The channel is still selling inventory bought cheaper, so retail has room to rise while contract keeps rising [REPORTED; market.md §8].
- **DDR4 sells above DDR5 per GB** in branded spot ($44 vs $27, 1.65×). Barclays has DDR4 contract up 24% over the three months to Oct 2026 against DDR5's 20% ([TechNews Finance](https://finance.technews.tw/2026/10/13/the-shortage-of-memory-chips-may-continue-for-another-two-years/)) [REPORTED].

### 2.3 Forecast and relief timeline

| When | Event | Effect on supply/price | Source |
|---|---|---|---|
| 4Q26 | Contract +10–15% (conv.), NAND +15–20%; enterprise SSD the only accelerating segment | Still rising, decelerating | [TrendForce](https://www.trendforce.com/presscenter/news/20260930-13258.html) |
| Oct 2026 | NAND contract reportedly flat, the first pause in 21 months | Leading indicator | [tech-insider](https://tech-insider.org/dram-record-high-nand-flat-21-months-october-2026/) [UNVERIFIED] |
| ~1Q27 | Samsung P4 (1c, ~100–120K wpm), much of it allocated to HBM | Tightens conventional DRAM | [Borecraft](https://borecraft.com/2026/05/26/samsungs-p4-hbm-pivot-tightens-the-2027-dram-crunch/) |
| Feb–Mar 2027 | SK hynix Yongin Y1 cleanroom, first tools; volume ~2028 | — | [Cleanroom Technology](https://cleanroomtechnology.com/sk-hynix-to-open-cleanroom-at-yongin-fab) |
| May–Jun 2027 | Samsung P5 phase-1 equipment move-in; full scale 2028 | — | [Sammy Fans](https://www.sammyfans.com/2026/09/28/samsung-accelerates-p5-expansion-for-dram-and-hbm-production/) |
| Mid-2027 | Micron ID1 first wafers (meaningful output 2028) | — | [Micron 10-K](https://www.sec.gov/Archives/edgar/data/0000723125/000072312526000023/mu-20260903.htm) |
| 2027 | DRAM bit supply +~24%; gap still **widens**; HBM ~30% of wafers; HBM blended ASP +121%; CXMT ~320K → ~420K wpm | Tight | [TrendForce RP260728GY](https://www.trendforce.com/research/download/RP260728GY); [Silicon Analysts](https://siliconanalysts.com/market/trendforce-2027-hbm-blended-asp-to-jump-121-as-hbm4-hbm4e-mix-shifts-2026-10-06); [Counterpoint](https://counterpointresearch.com/en/insights/cxmt-stock-market-big-three-memory-club) |
| 2H27 | **NAND turns to surplus with downward price pressure** | DRAM's canary | [TrendForce](https://www.trendforce.com/presscenter/news/20260730-13158.html) |
| 2027-12-23 | §5949 federal ban on CXMT/YMTC/SMIC-containing products (1b: date confirmed; FAR rule still proposed) | Provenance demand | [XenoSpectrum](https://xenospectrum.com/en/apple-china-memory-federal-procurement-ban-2027/); [Federal Register](https://www.federalregister.gov/documents/2026/02/17/2026-03065/federal-acquisition-regulation-prohibition-on-certain-semiconductor-products-and-services) |
| 2028 | Bit growth low-20s% (Micron) to >30% (Baird); BofA DRAM ASP −10%; BI possible oversupply; Micron ID2 late 2028; SK hynix Indiana cleanroom Oct 2028 | **Most likely turn** | [Guru3D](https://www.guru3d.com/story/micron-expects-dram-and-nand-supply-to-tighten-further-through-2028/); [TMGM](https://www.tmgm.com/en/analysis/market-insight/micron-dram-supply-tightening) |
| 2029–30 | SK hynix supply booked to 2029; Indiana HBM4E from Q3 2029; Micron NY1 output CY2030; ~35% of Micron revenue locked under LTAs through 2030 | LTAs push the downturn onto spot and channel buyers | [Sammy Fans](https://www.sammyfans.com/2026/10/28/sk-hynix-q3-margin-hits-record-80-secures-14-ltas-with-memory-supply-booked-to-2029/amp/); [Herald](https://mbiz.heraldcorp.com/article/10853891); [TrendForce](https://www.trendforce.com/news/2026-10-01/news-micron-fy2026-revenue-surges-256-to-133-2b-locks-in-35-of-revenue-through-2030/) |

**House call [ESTIMATE; p1-market, adopted]:** contract prices peak between 4Q26 and 2Q27, then plateau through 2027 on LTAs and HBM crowding. They turn down in 2028. A true glut (prices below second-tier cash cost) is a 2H28–2029 event, and only if AI capex slows.

---

## 3. Demand drivers, the HBM allocation story, and DDR4 EOL

### 3.1 Demand drivers (2026–27)

| Driver | Evidence | Source |
|---|---|---|
| CSP AI-infrastructure procurement locks multi-year supply | CSPs signing long-term deals; from 3Q26 increases fall mainly on buyers **without** LTAs (tier-2 clouds, enterprises) | [TechNews](https://technews.tw/2026/03/31/ai-server-demand-drives-2q26-memory-contract-price-increase-csps-lock-supply-long-term-deals/) [REPORTED] |
| More HBM per accelerator; SOCAMM (LPDDR server modules); server units above 2026's +17% | TrendForce 2027 outlook | [TrendForce 2026-07-30](https://www.trendforce.com/presscenter/news/20260730-13158.html) [REPORTED-P] |
| Server LPDDR competes with phones for LPDDR5X | Mobile LTAs up to ~$21/GB | [Wccftech](https://wccftech.com/mobile-dram-prices-expected-to-increase-by-100-quarter-over-quarter-as-long-term-agreements-now-getting-signed-at-prices-as-high-as-21-gb/amp/) |
| Inventory had nowhere to go | Supplier inventories averaged **3.3 weeks** at end-3Q25, matching 2018 lows | [TrendForce News](https://www.trendforce.com/news/2025/09/30/news-record-low-memory-stock-could-signal-supercycle-ahead-likely-peaking-by-2027/) |
| Demand destruction at the consumer end | Retail kits "stabilized" because buyers gave up; Samsung's phone/appliance division losses widened on component costs | [TechRadar](https://www.techradar.com/pro/good-news-ram-prices-seem-to-have-finally-stabilized-bad-news-its-probably-because-memory-prices-are-so-high-that-its-forcing-most-of-us-to-give-up-buying-anything); [Samsung](https://news.samsungsemiconductor.com/global/samsung-electronics-announces-third-quarter-2026-results/) |
| Allocation away from small buyers | Micron 10-K: "supply allocation decisions that may affect some customers"; module makers limited | [Micron 10-K](https://www.sec.gov/Archives/edgar/data/0000723125/000072312526000023/mu-20260903.htm); [TrendForce abstract](https://www.trendforce.com/research/download/RP260114IU) [REPORTED-P] |

### 3.2 The HBM allocation story

1. **Wafers vs bits.** HBM takes ~22% of DRAM wafer starts in 2026 and ~30% in 2027, but only 9–13% of bits ([TechNews/TrendForce](https://technews.tw/?p=1565421)) [REPORTED].
2. **The trade ratio is ~3:1 and rising.** The causes are larger dies (1.35–1.45× area), TSV area and stack-yield loss ([Tom's Hardware](https://www.tomshardware.com/tech-industry/semiconductors/micron-says-the-silicon-gap-between-hbm-and-ddr5-is-widening-with-every-generation)). The model computes **2.77:1** for HBM3E 12-high, consistent with that (`models/dram_cost_stack.py` §4).
3. **Crowding-out [ESTIMATE].** Moving HBM from 22% to 30% of wafers removes ~8 pp of starts, about 10% of conventional DRAM's base. That cancels roughly half of 2027's 20–24% gross bit growth for conventional parts.
4. **The 2026 twist: HBM3E earned less than DDR5.** HBM3E sold at ~$12/GB against a model cost of **$6.08/GB (49% GM)**. DDR5 earned ~90% (model §7). Samsung said on 2026-04-30 that conventional DRAM was more profitable than HBM ([FN News](https://en.fnnews.com/news/202604301057582454)). Suppliers responded by asking ~3× for HBM4 in 2027 ($36–39/GB) ([Sammy Fans](https://www.sammyfans.com/2026/10/02/samsung-seeks-more-than-3x-hbm3e-pricing-for-hbm4/)) [REPORTED].
5. **Capacity is still being pointed at HBM.** Micron is adding ~60K HBM wpm to reach ~100K by end-2026 ([TrendForce News](https://www.trendforce.com/news/2026/09/04/news-micron-reportedly-to-add-60k-hbm-wafersm-reaching-100k-by-year-end-to-narrow-gap-with-samsung-sk-hynix/)). Samsung P4 is reportedly HBM-heavy. **Implication:** if HBM4 pricing holds in 2027–28, conventional supply stays tight. If AI capex slows, HBM capacity swings back to conventional bits and accelerates the glut.

### 3.3 DDR4 end-of-life

| Item | Status | Source |
|---|---|---|
| Original EOL plans | Samsung last orders Jun-25, final ship Dec-25; SK hynix orders end Oct-25, final ship Apr-26; Micron final ship ~1Q26 | [TrendForce News 2025-07-09](https://www.trendforce.com/news/2025/07/09/news-ddr4-exit-timeline-unfolds-for-top-memory-makers-plans-for-samsung-sk-hynix-and-micron) |
| Actual | Samsung and SK hynix extended DDR4 through 2026 (cash cow). (1b) Samsung's auto DDR4/LP4 runway ends in Q1 2027, and SK hynix has made no commitment beyond 2026. TrendForce says several makers exit DDR4 in 2026, with DDR4 ~10% short through 2026 [REPORTED] | [TrendForce News 2025-09-02](https://www.trendforce.com/news/2025/09/02/news-samsung-sk-hynix-reportedly-delay-phase-out-to-2026-as-ddr4-becomes-unexpected-cash-cow/); [Counterpoint](https://counterpointresearch.com/cn/reports/memory-crisis-automotive-industry-suppliers-automakers-response); [TrendForce 2026-01-19](https://www.trendforce.com/news/2026/01/19/news-ddr4-reportedly-leads-legacy-memory-rally-with-q1-prices-up-to-50-ddr3-in-tight-supply/) |
| Micron U.S. | Manassas 1-alpha DDR4/LP4 for long-lifecycle buyers since 2026-05-22; DDR4 is ~7% of Micron DRAM output in 2026; Micron will not resume consumer DDR4 supply. (1b) Micron is the **only supplier publicly committed to ongoing DDR4/LP4**, with Strategic Customer Agreements covering Astemo, Denso, Harman, Hyundai Mobis, Joynext, Qualcomm, Visteon, **Ford and GM** [REPORTED] | [I-Connect007/TrendForce](https://iconnect007.com/article/150148/microns-fab-6-starts-lpddr4-and-ddr4-production-but-ddr4-shortage-is-expected-to-persist/150145/flex); [TrendForce abstract](https://www.trendforce.com/research/download/RP260525NN); [Counterpoint](https://counterpointresearch.com/cn/reports/memory-crisis-automotive-industry-suppliers-automakers-response) |
| (1b) Other long-lifecycle suppliers | ISSI supports DDR4 and LPDDR4/4X through at least 2038. Intelligent Memory's DDR4 32Gb parts return only from Q3 2026, which it blames on the HBM shift [REPORTED-P] | [AMD/ISSI brief](https://www.amd.com/content/dam/amd/en/documents/products/adaptive-socs-and-fpgas/technologies/issi-memory-solution-brief.pdf); [Intelligent Memory](https://www.intelligentmemory.com/company/articles-news-events/intelligent-memory-to-exhibit-at-embedded-world-2026) |
| Buyer pain | Auto/industrial DDR4 buffers fell from **31+ weeks to 6–8 weeks**; Advantech says avoid Samsung DDR4 in new designs; **zero authorized stock** of a mainstream Micron DDR4 at Newark, Avnet and Mouser (May-26) | [eeNews Europe](https://www.eenewseurope.com/en/micron-ramps-us-made-ddr4-production-in-virginia/); [Advantech](https://www.advantech.com/en/resources/news/response-measures-to-samsung-ddr4-ic-eol-announcement); [Findchips](https://blog.findchips.com/memory-shortage-watch-ddr3l-ddr4-may-2026/) |
| Prices | DDR4 8Gb module ~+50% QoQ in 3Q26; DDR3 also rising | [Gizchina](https://www.gizchina.com/tech/ddr4-prices-are-jumping-50-this-quarter-and-it-wont-stop-until-2028); [Wccftech](https://wccftech.com/memory-shortages-drive-ddr4-prices-over-50-in-q3-2026-ddr3-also-impacted-by-higher-costs/) |

**Why it matters:** legacy DRAM is the most over-priced memory relative to cost in 2026. DDR4 costs **$1.28/GB** on a depreciated line (model) and sells at $16–46/GB. It is also the most exposed segment: when Samsung and SK hynix finish exiting, CXMT, Nanya and Winbond backfill, and the EOL premium unwinds, **DDR4 collapses first and hardest** (§5).

---

## 4. The DRAM cost stack (`models/dram_cost_stack.py`)

All figures are [ESTIMATE] outputs of the model. It was re-run 2026-11-01 after `v4-cost`'s Phase 1b input corrections (exit 0; full output in `research/phase1/cost_stack_output.md`; change log in `research/phase1/verify_v4-cost.md`). Inputs come from `research/phase1/cost_inputs.json` (224 records, low/base/high). Component $/GB is per raw GB. Module $/GB is per user GB; an RDIMM carries +25% ECC bits.

**(1b) What moved the model.** Each of these changed by more than 15%:
- **1-beta 16Gb die:** 41.0 → **36.5 mm²**, anchored on teardowns of Micron's D1β DDR5 (35.83 mm², 0.447 Gb/mm²) and Samsung's D1b LPDDR5X (36.68 mm²) [REPORTED-P].
- **1-gamma die:** 33.3 → 29.1 mm², derived from Micron's ">30% more bits per wafer" claim. The area itself is still unverified.
- **4Q26 RDIMM anchor:** $1,300 → **$1,650**, from Counterpoint's 3Q26 forecast (~$1,500) × TrendForce's 4Q26 +10–15% ([Counterpoint Jul-26](https://counterpointresearch.com/en/reports/memory-price-tracker-and-forecast-july-2026)).
- **EUV tool price:** ~$220M → ~$290M ([S&P Global 2026-03](https://www.spglobal.com/market-intelligence/en/news-insights/research/2026/03/sk-hynix-invests-in-euv-as-ai-boom-tightens-conventional-dram-supply)).
- **Not moved:** the 1-alpha die (52.6 mm², confirmed), the CXMT G4 die (66.99 mm², confirmed) and the HBM3E price (confirmed).

### 4.1 Wafer → die → $/GB

| Case | Wafer $ | Die mm² | Good dies/wafer | Component $/GB | 4Q26 GM | Glut GM | 2023-trough GM |
|---|---|---|---|---|---|---|---|
| DDR5 16Gb 1-alpha | 3,400 | 53.3 | 1,042 | 1.88 | 91% | 77% | −18% |
| **DDR5 16Gb 1-beta (BASE)** | **3,800** | **36.5** | **1,534** | **1.48** | **93%** | **82%** | **7%** |
| DDR5 16Gb 1-beta, cash cost only | 1,650 | 36.5 | 1,534 | 0.78 | 96% | 90% | 52% |
| DDR5 16Gb 1-gamma (2026 ramp, y 0.80) | 4,300 | 29.1 | 1,717 | 1.50 | 93% | 82% | 6% |
| DDR5 16Gb 1-gamma (mature) | 4,300 | 29.1 | 1,931 | 1.36 | 93% | 83% | 15% |
| HBM3E 12-high 36GB | 4,450 | 110 | 437 | **6.08** ($219/stack) | 49% (at $12) | n/a | n/a |
| DDR5 16Gb on CXMT G4 die (1z-class) | 3,000 | 67.0 | 823 | 2.07 | 90% | 75% | −30% |
| DDR4 16Gb 1y, depreciated line | 1,300 | 88 | 604 | 1.28 | 94% | 84% | 1% |
| **DDR4 8Gb 1x, NEW U.S.-style line** | 2,800 | 55 | 953 | **3.28** | 84% | 60% | **−153%** |
| DDR3 4Gb 25nm, PSMC-class foundry | 1,600 | 60 | 922 | 4.12 | 80% | 49% | −217% |

Wafer cost (1-beta, $3,746 bottom-up) is **56% depreciation**. Incumbents can therefore run through a glut at cash cost (~$0.78/GB). Legacy rows use the legacy price deck, which assumes DDR5 parity at 4Q26. Their 4Q26 and glut GMs rose with the new contract anchor.

### 4.2 Modules (64GB DDR5 RDIMM, 1-beta)

| Item | Value |
|---|---|
| DRAM (40 × 16Gb, 80 GB raw) | $118.69 |
| Non-DRAM BOM (RCD, PMIC, SPD hub, PCB, passives) | $17.10 |
| Assembly + test, Asia / U.S. | $3.50 / $12.00 |
| **Module cost, Asia / U.S. assembly** | **$141 ($2.21/user-GB) / $150 ($2.34)** |
| U.S. assembly penalty | **+$8.63** = +6.1% of cost, **0.5% of a $1,650 contract module** |
| 4Q26 contract / glut / 2023-trough price | $25.78 / $10.31 / $2.32 per user-GB |
| Module GM at those prices | 91% / 79% / 5% |

### 4.3 Cost vs price vs glut (the three decks every concept is scored against)

| Deck | DDR5 component $/GB | 64GB RDIMM $/user-GB | Basis |
|---|---|---|---|
| **Shortage (4Q26)** | **20.37** | **25.78** | (1b) $1,650 RDIMM = Counterpoint 3Q26F ~$1,500 × TrendForce 4Q26 +10–15% ([Counterpoint Jul-26](https://counterpointresearch.com/en/reports/memory-price-tracker-and-forecast-july-2026); [TrendForce](https://www.trendforce.com/presscenter/news/20260930-13258.html)). Cross-checks: Citi $1,586; 1Q26 actual $927 compounded through 4Q26 gives $1,933. The old $1,300 anchor (2Q26 ~$1,000) was stale |
| Spot reference (2026-08-31) | 26.96 | — | [BuySellRAM](https://www.buysellram.com/blog/ram-market-update/) |
| **Glut (A-05: −60% from 4Q26)** | **8.15** | **10.31** | ASSUMPTIONS.md A-05 applied to the 1b deck (was 6.40 / 8.12) |
| **Severe (−90%)** / 2023 trough | **2.04** / 1.60 (DDR4 2023: 1.30) | — / 2.32 | [KED Global](https://www.kedglobal.com/korean-chipmakers/newsView/ked202310040013); 2023 DDR5 trough [UNVERIFIED] |
| Incumbent full cost / cash cost | 1.48 / 0.78 | 2.21 | model |

- **A −60% glut leaves DDR5 at 5.5× incumbent full cost** (it was 3.9× before 1b). Prices must fall ~93% before 1-beta full cost bites, and ~96% before cash cost does.
- **Margin is set by price, not cost.** Across all ±20% cost cases, gross margin stays at 91–94% at the 4Q26 price and 78–85% in the glut (model §10).
- **Validation:** the model's 93% component GM sits **6–7 pp above** Micron's ~87% and Nanya's 85.7% reported GMs, which include older nodes, NAND and period costs ([Finviz/Micron](https://finviz.com/news/397277/micron-technology-inc-reports-record-fiscal-fourth-quarter-and-full-year-2026-results); [TrendForce News](https://www.trendforce.com/news/?p=65146)). (1b) Before 1b the gap was 3–4 pp. Density is now anchored by teardowns, so the wider gap most plausibly means the $3.8k 1-beta wafer is understated. The higher EUV tool price points the same way. A ~$5k wafer would put 1-beta at ~$1.9/GB and 4Q26 GM at ~91%. **No decision changes** (verify_v4-cost.md, note 3) [ESTIMATE].

### 4.4 Alternatives on the same $/GB axis (from cost_stack.md §8; for the Phase 2 device models)

| Memory | $/GB | Basis |
|---|---|---|
| DDR5 1-beta (cost / glut price / 4Q26 price) | 1.48 / 8.15 / 20.37 (1b; was 1.64 / 6.40 / 15.99) | model |
| Everspin 1Gb STT-MRAM (GF 28nm, 105.1 mm², 0.0095 Gb/mm², ~46× below 1-beta DDR5 at the 1b density) | ~91 silicon+package (A2 model); **~$821 street** (1b confirmed: ~$103 @500, ~$101 @1,000, $266 @1) | [TechInsights](https://www.techinsights.com/blog/memory/worlds-first-1-gb-28-nm-stt-mram-product-everspin); [LCSC](https://www.lcsc.com/product-image/C20342497.html); [LCSC detail](https://www.lcsc.com/product-detail/C20342497.html) [REPORTED-P] |
| SRAM silicon, 7–28nm / 65nm / U.S. 130nm (sky130 cell 1.896 µm², VERIFIED) | ~55–72 / ~195 / ~1,330; (1b) street 72Mb QDR-II+ ≈ 1,400–3,800 | cost_stack.md §8.5 [ESTIMATE]; [sky130 SRAM](https://github.com/google/skywater-pdk-libs-sky130_fd_bd_sram); [broker listing](https://www.lisleapex.com/product-cy7c25652kv18-550bzxi) [REPORTED] |
| IGZO 2T0C on U.S. 130nm / 65nm BEOL | 250–490× / 60–120× less dense than DDR5 1b per tier | us_fabs.md §8.3 [ESTIMATE] |
| 3D XPoint gen1 / gen2 density | 0.62 / 1.31 Gb/mm² (beats 1-beta DDR5 on density; died on volume and cost absorption) | [TechInsights](https://www.techinsights.com/blog/intel-3d-xpoint-memory-die-removed-intel-optanetm-pcm-phase-change-memory) [REPORTED] |
| NAND TLC 2026 | ~0.09 | cost_stack.md §8.6 [ESTIMATE] |

**Rule from this table:** no non-DRAM memory available to us comes within 10× of DDR5 *cost*: SRAM at 7–28nm is ~37–49× the 1-beta cost. SRAM is only ~3× the 4Q26 DDR5 *price*, but ~7–9× the 1b glut price.

### 4.5 Weakest inputs (fix these first)

| Input | Current value | Why weak | Effect |
|---|---|---|---|
| Fully loaded 1-beta wafer cost | $3,800 ($3.2–5.5k) | Capex/wpm rules of thumb [UNVERIFIED]. (1b) No public IC Knowledge, SemiAnalysis, TechInsights or broker estimate was found. The GM gap of 6–7 pp and the ~$290M EUV tool hint it is understated | **Now the dominant unknown and the largest swing**: $1.29–2.04/GB over its range (model §10e) |
| 1-beta / 1-gamma die sizes | 36.5 / 29.1 mm² (1b; were 41 / 33.3) | (1b) 1-beta is anchored on TechInsights teardowns (Micron D1β 35.83 mm²) [REPORTED-P] ([TechInsights](https://techinsights.com/ja/node/57875)). 1-gamma is derived from Micron's >30% bits-per-wafer gain ([Micron brief](https://micron.cn/content/dam/micron/global/public/products/technical-marketing-brief/1-gamma-technology-brief.pdf)), and its area is still unverified | ±20% die → $1.21–1.77/GB |
| 4Q26 contract level | $1,650 RDIMM (1,500–1,930) (1b; was $1,300) | No public chip-level contract. Citi $1,586 is REPORTED through a secondary relay only. The derived 16Gb contract is ~$41 ($37–48), against $53.92 spot (2026-08-31) | Sets the margin and the glut line |
| 2023 DDR5 trough | $3.2/chip ($1.60/GB) | Prior knowledge | Sets the severe-case test |
| DDR4 4Q26 contract | Parity with DDR5 | No legacy contract series; spot shows a 1.65× premium. (1b) DDR4 contract was +4% MoM in Oct 2026 and +24% over three months (bank note via [Guru3D](https://www.guru3d.com/story/ddr4-memory-prices-now-also-rise-as-dram-supply-shortages-intensify-through-2028/)) [REPORTED] | Understates legacy margins today, overstates them in a glut |
| HBM core die and stack yield | 110 mm², 0.75 | [UNVERIFIED] | HBM $/GB $5.0–7.3 under ±20% |

---

## 5. Cycle history and what a 2028–29 glut looks like

### 5.1 Analogs

| Cycle | Peak → trough | Duration | Price decline | Inventory | Maker P&L | Source |
|---|---|---|---|---|---|---|
| **2018–19** | Peak 1H/3Q18 after 9 straight quarterly rises | ~4–5 qtrs | 8GB module $68 → $25.50, **−62.5%**; 1Q19 alone ~−30%; 8Gb spot $6.95 → <$3 | n/a | Margins compressed; makers stayed profitable | [TrendForce](https://press.trendforce.com/node/view/3173.html); [DigiTimes](https://www.digitimes.com/tag/8gb/0034884.html); [KitGuru](https://www.kitguru.net/?p=406046); [Evertiq](https://evertiq.com/design/45079) |
| **2022–23** | Peak ~3Q21/1H22 → trough 3Q23 | ~6–8 qtrs | DRAM revenue −~30% QoQ in 3Q22; ASP −20% (1Q23), −10–15% (2Q23); DDR4 8Gb fixed → **$1.30**, ≈−60–65% | PC-OEM 9–13 weeks | SK hynix −KRW 3.4T (≈−67% OM) in 1Q23; utilization cut to 74–82% | [I-Connect007](https://www.iconnect007.com/article/134149/due-to-falling-shipments-and-prices-global-dram-revenue-for-3q22-showed-qoq-drop-of-almost-30/134152/ein); [The Register](https://www.theregister.com/2023/03/29/dram_prices_crash/); [TrendForce](https://www.trendforce.com/presscenter/news/20230109-11533.html); [The Register](https://www.theregister.com/2023/04/27/samsung_sk_hynix_losses/) |
| **2025–?** (now) | Trough 1Q–2Q25 → ? | 6+ qtrs up | **≈+4× contract** (4Q25→4Q26) | 3.3 weeks (end-3Q25) | 72–87% margins | §2 |

**Is "DDR5 −60% in 2028–29" plausible? Yes. It is the historical median, not a worst case.** Because prices rose 4–8×, a 60% fall still leaves DDR5 at ~2.4× its 3Q25 contract level. A return to the 2023 floor would take an **85–90% fall**, which has happened to spot chips but rarely to contract prices within two years [ESTIMATE, market.md §7.3].

### 5.2 How a glut unfolds (sequence to watch)

1. NAND turns first, 2–4 quarters ahead of DRAM. TrendForce already forecasts a NAND surplus in 2H27.
2. Customer inventory climbs from ~3 weeks to 9–13 weeks.
3. Spot falls below contract, and LTAs get renegotiated. **Micron (35% of revenue locked through 2030) and SK hynix (booked to 2029) push the pain onto the spot and channel market**, which is where small buyers and sellers live.
4. Second-tier makers (Nanya, Winbond, CXMT) go negative first, and utilization is cut to 75–80%.
5. **DDR4 collapses first and hardest** as the EOL premium unwinds and CXMT backfills. Recovered DDR4 RDIMMs fall from an observed **$3.1–5.8/GB** (1b: realized resale over the 12 months to Aug 2026 ([amcompute](https://www.amcompute.com/appraisals/ddr4-32gb-rdimm)) [REPORTED]) to $0.5–1.5/GB (us_backend.md §6.5) [ESTIMATE].

### 5.3 The stress test every concept faces

| Test | DDR5 $/GB | A concept fails if… |
|---|---|---|
| Shortage base (4Q26) | 20.37 (contract; 1b, was 15.99) / 27 (spot) | It only works at spot prices |
| **Glut (A-05)** | **8.15** component / 10.31 RDIMM user-GB (1b; was 6.40 / 8.12) | **Its cost or value proposition needs DDR5 above ~$8/GB** |
| Spot-based −60% (upper bound) | ~11.4 | — (use only as a sensitivity) |
| Severe / 2023-style trough | 2.04 (−90%) / 1.30–1.60 (2023 actuals) | It needs DDR5 above ~$1.6–2/GB; most device concepts fail here |
| Timing | Turn in 2028 | Arbitrage revenue is not cash-positive by end-2027 |

Worked examples [ESTIMATE]:
- A **new U.S. legacy DDR4 line** costs $3.28/GB. That beats the glut price, but it runs at **−153% GM at the 2023 trough**. It is a shortage-only business.
- A **U.S. recert shop** clears **17–23% contribution** at the observed used prices ($3.1–5.8/GB realized; 1b) and **~1–6% in a glut** (us_backend.md §6.6). The model assumes lots are bought at 60% of resale. ITAD incumbents are keeping the 2026 repricing, so that is optimistic.
- A **memory-efficiency tool** saves DRAM worth ~$20/GB of contract value today and ~$8/GB in the glut. Its ROI falls 60% but does not vanish.

---

## 6. U.S. capacity map: front end and back end

Legend for "Outside customers?": **Yes** = open to a small company; **Ltd** = programs, strategic deals or defense only; **No** = captive. Tags: most fab and OSAT details beyond the cited rows are [UNVERIFIED] researcher prior knowledge (us_fabs.md, us_backend.md).

### 6.1 Consolidated table

| # | Facility (owner) | FE/BE | Memory-relevant capability | Outside customers? | Status / source |
|---|---|---|---|---|---|
| 1 | Boise ID R&D fab + ID1/ID2 (Micron) | FE | Leading-edge DRAM R&D; ID1 first wafers mid-2027, ID2 late 2028 | **No** | [Micron 10-K](https://www.sec.gov/Archives/edgar/data/0000723125/000072312526000023/mu-20260903.htm) [REPORTED-P] |
| 2 | Manassas VA Fab 6 (Micron) | FE | **Only U.S. DRAM production**: 1-alpha DDR4/LP4 since 2026-05-22 | **No** (parts via distribution; SpecTek sells wafers and down-binned parts) | [HPCwire](https://www.hpcwire.com/off-the-wire/micron-advances-made-in-america-memory-with-manufacturing-expansion-in-virginia); [NIST PMT](https://www.nist.gov/node/1869301) |
| 3 | Clay NY NY1 (Micron) | FE | Leading-edge DRAM, output CY2030 | **No** | [The Register](https://www.theregister.com/2026/01/16/micron_fab_breaks_ground/) |
| 4 | Chandler AZ, inside NXP's fab (Everspin) | FE (magnetic BEOL) | **Toggle MRAM only** (≤16–32 Mb) on purchased 200mm CMOS; STT-MRAM is made at GF Singapore | **Ltd** (DoD program foundry services) | [Everspin 10-K](https://www.sec.gov/Archives/edgar/data/1438423/000162828026014733/mram-20251231.htm) [REPORTED-P] |
| 5 | Gresham OR Fab 4 (Microchip for Everspin) | FE | 200mm MRAM/TMR, first products 2H-2027, max 1,300 wafers/qtr | **No** (TMR exclusivity for Everspin) | [Everspin 8-K](https://www.sec.gov/Archives/edgar/data/1438423/000162828026024696/mram-20260408xexx991.htm) [REPORTED-P] |
| 6 | Bloomington MN (SkyWater) | FE | 200mm 350–90nm; **Weebit ReRAM qualified in S130 PDK**; DARPA 3DSoC low-temperature BEOL precedent [UNVERIFIED]; DMEA Trusted [UNVERIFIED] | **Yes** (pure-play) | [Weebit](https://www.weebit-nano.com/news/press-releases/weebit-nanos-reram-ip-now-fully-qualified-in-skywater-technologys-s130-process/); [SkyWater](https://www.skywatertechnology.com/weebit-nano-reram-ip-achieves-high-temperature-qualification-in-skywater-s130-process/) |
| 7 | Austin TX Fab 25 (SkyWater, ex-Infineon) | FE | 200mm 130–65nm, ~400k wafer starts/yr; bought for ~$73M + ~$20M (closed 2025-06-30); SONOS heritage [UNVERIFIED] | **Yes** (converting; Infineon anchor) | [LaPedus](https://marklapedus.substack.com/p/skywater-acquires-infineons-200mm) |
| 8 | Malta NY Fab 8 / Essex Jct VT Fab 9 (GlobalFoundries) | FE | 12/14nm FinFET, RF-SOI; no U.S. eMRAM/ReRAM volume; 14HP eDRAM status unknown [UNVERIFIED]. GF eMRAM (AutoPro150) runs in Dresden | **Yes** (Trusted) | [GF](https://www.globenewswire.com/news-release/2026/03/09/3251832/0/en/GlobalFoundries-Announces-Availability-of-AutoPro150-eMRAM-Technology-on-Enhanced-FDX-Platform-for-Advanced-Automotive-Applications.html) |
| 9 | Sherman / Richardson TX, Lehi UT (TI) | FE | Captive embedded FRAM; Weebit ReRAM licensed Dec-2025; Lehi kept no XPoint | **No** | [Weebit-TI](https://www.weebit-nano.com/news/press-releases/weebit-nano-secures-a-license-agreement-with-texas-instruments/); [AnandTech](https://www.anandtech.com/show/16800) |
| 10 | Bloomington MN (Polar Semiconductor) | FE | 200mm power/BCD; candidate BEOL host [UNVERIFIED] | **Yes, emerging** | us_fabs.md §2.6 |
| 11 | AZ / OR / NM (Intel Foundry) | FE | No memory product; eMRAM/ReRAM/BEOL-TFT R&D only | **Yes** (large engagements) | [Intel patent](https://patents.google.com/patent/US11751402) |
| 12 | Tower (Newport Beach, San Antonio, Rio Rancho), Samsung Austin/Taylor, TSMC AZ/WaferTech, X-FAB Lubbock | FE | Logic, RF, power; no BEOL memory module in the U.S. | **Yes** | us_fabs.md §2.8 [UNVERIFIED] |
| 13 | Plymouth MN (Honeywell), Manassas VA (BAE Systems) | FE | Trusted rad-hard SRAM/MRAM | **Ltd** (DoD) | [UNVERIFIED] |
| 14 | Albuquerque NM MESA (Sandia) | FE | **HZO FeRAM + binary/32-state FTJs in a trusted 200mm flow (2026-05-13)** | **Ltd** (CRADA/SPP) | [Sandia](https://www.sandia.gov/research/news/evolving-semiconductor-technology-for-national-security-applications/) |
| 15 | Albany NY (NY CREATES / Albany NanoTech) | FE R&D | 300mm EUV; **HfO₂ FE memory JDA with Fraunhofer (2025-05)** | **Yes** (JDA/membership, $0.25–2M+) | [IDW](https://nachrichten.idw-online.de/2025/05/16/ny-creates-and-fraunhofer-ipms-announce-joint-development-agreement-to-advance-memory-devices-at-300mm-wafer-scale) |
| 16 | University nanofabs (Cornell CNF, Penn Singh, Harvard CNS, MIT.nano, GT IEN, **Purdue Birck**, Penn State, RIT) + DOE NSRCs | FE R&D | Oxide-TFT/2T0C/HZO device prototyping; Purdue ran 3 stacked In₂O₃ tiers on 200mm (2026-09) | **Yes** ($75–250/tool-hr industry; NSRC free for open work) | [Purdue](https://engineering.purdue.edu/ECE/News/2026/purdue-researchers-build-3d-chip-platform-for-faster-more-efficient-ai-computing); rates [ESTIMATE] |
| 17 | Display / TFT | FE | **No Gen-scale LCD/OLED/oxide-TFT panel fab in the U.S.** Only microdisplays (eMagin/Samsung Display, Kopin), glass (Corning), tools (Applied) | n/a | [TrendForce abstract](https://www.trendforce.com/research/download/RP260831UV) |
| 18 | Seagate (Bloomington MN), NVE (Eden Prairie MN) | FE | Volume MTJ/TMR sputter and etch for HDD heads; spintronic sensors (MTJ talent pool, not foundry) | **No** | [UNVERIFIED]; [NVE](https://www.nve.com/earningsreports/may62026) |
| 19 | West Lafayette IN (SK hynix) | BE | HBM packaging; groundbreaking 2026-08-27, cleanroom Oct-2028, HBM4E from Q3-2029 | **No** | [Evertiq](https://evertiq.com/news/2026-08-28-sk-hynix-breaks-ground-on-4-billion-packaging-facility-in-indiana); [Herald](https://mbiz.heraldcorp.com/article/10853891) |
| 20 | Micron U.S. HBM packaging | BE | Intent only; after ID2 → 2029+ | **No** | [The Manufacturer](https://www.themanufacturer.com/articles/micron-technology-announces-200bn-investment-in-semiconductor-manufacturing-and-rd-in-idaho-new-york-and-virginia/) |
| 21 | Peoria AZ (Amkor) | BE | **Logic** 2.5D/fan-out (integrates HBM, does not stack it); production ~early 2028 | **No** (anchor customers) | [UNVERIFIED] |
| 22 | Rio Rancho NM (Intel Fab 9, Foveros), Kissimmee FL (SkyWater fan-out) | BE | Advanced packaging; no commodity DRAM | Intel: No; SkyWater FL: Yes in principle | [UNVERIFIED] |
| 23 | **Micross** (FL/NC) | BE + die | Largest authorized die distributor (DRAM on line card, **Micron not named**); hi-rel DDR MCMs | **Yes** | [Micross flyer](https://micross.com/uploads/05827c98-1b61-4d4d-bb3c-04dc1b207e5a/Die_and_Wafer_Flyer_Rev_1_WEB.pdf) |
| 24 | Integra (Wichita KS); QP Technologies/Promex, Golden Altos (CA) | BE | Hi-rel OSAT; quick-turn wire-bond BGA prototypes of DRAM die (1–10k units) | **Yes** | [UNVERIFIED] |
| 25 | NHanced (NC), Texas Institute for Electronics (UT Austin, DARPA NGMM) | BE | Hybrid bonding, 3D stacking prototypes | **Yes** (prototype) | [UNVERIFIED] |
| 26 | Mercury (Phoenix AZ), Data Device Corp (Bohemia NY), Frontgrade (CO) | BE | Rugged/rad-tolerant DDR MCMs; MRAM modules on Everspin Toggle die | **Ltd** (defense) | [Frontgrade](https://www.frontgrade.com/news/new-case-study-touts-everspins-toggle-mram-highly-reliable-memory-technology-space) |
| 27 | Kingston (Fountain Valley CA), Virtium (RSM CA); SMART/Penguin, Viking, PNY (limited) | BE | DIMM SMT and test; Kingston is the largest independent module maker | Brands: **No**; any U.S. EMS: **Yes** | [UNVERIFIED] |
| 28 | SpecTek (Micron) | Die | DRAM/LPDRAM in BGA, **wafers**; contains current Micron 1-alpha die | **Unknown** (one email answers it) | [SpecTek](https://micron.net/sales-support/customer-support/spectek-support); [TechInsights](https://www.techinsights.com/blog/spectek-pt040-56b-ddr5-dram-micron-1a-memory-floorplan-analysis) |
| 29 | Winbond, ESMT, Etron KGD (Taiwan; U.S. sales) | Die | Open KGD programs, legacy densities (SDR–DDR4, LPDDR2–4), per JESD49B.01 | **Yes** | [Winbond](https://winbond.com/hq/product/customized-memory-solution/kgd/); [ESMT](https://esmt.com.tw/en/Applications/Known-Good-Die); [Etron](https://etron.com/kgdm/); [JEDEC](https://www.jedec.org/node/8358) |
| 30 | Rochester Electronics (MA), Alliance Memory (WA), Lansdale (AZ) | Die/legacy | Authorized aftermarket, die banking, EOL re-creation; drop-in legacy DRAM | **Yes** (entrenched) | [UNVERIFIED] |
| 31 | Test: ISE Labs (Fremont), STS, Golden Altos, Trio-Tech; module testers CST, Innoventions | BE | Test-program NRE $20–200k; module testers $3–50k | **Yes** | [ESTIMATE] |
| 32 | ITAD: Iron Mountain/ITRenew (Sesame), Sims, SK tes, ERI | Recert source | Decommissioned DDR4 RDIMM lots | **Yes** (as suppliers) | [UNVERIFIED] |
| 33 | Resale: Mobius Materials (Richmond VA, $3M seed Dec-25), BuySellRAM, eBay brokers | Recert channel | Authenticated B2B surplus marketplace; used-memory buying | **Yes** (crowded) | [Mobius PR](https://www.prnewswire.com/news-releases/mobius-materials-raises-3m-to-combat-one-of-manufacturings-biggest-issues-amid-us-china-trade-tariffs-302643403.html); [BuySellRAM](https://www.buysellram.com/blog/ram-market-update/) |

### 6.2 Front-end verdicts

| Question (mission §3A/§3C) | Answer |
|---|---|
| Can a U.S. trailing-node fab run DDR3/DDR4-class DRAM? | **No host.** No U.S. 22–65nm foundry line has a DRAM capacitor module. A new line costs $3.28/GB and is underwater at the trough (§4). |
| What U.S. TFT/display capacity exists for IGZO? | **None at Gen scale.** IGZO in the U.S. means a BEOL module on a 200mm silicon fab (SkyWater, Polar) or a university pilot. Both are ≥60× less dense than DDR5 per tier. |
| Could idle or trailing silicon fabs run IGZO BEOL? | **Technically yes** (≤400 °C, sputter/ALD). The blockers are In/Ga/Zn contamination policy, which means dedicated tools (~$4–10M, T2), plus PBTI reliability and density [ESTIMATE]. |
| Cheapest real prototype path | University fab with an oxide-TFT group, **$20–80k**, 3–6 months. Next step: SkyWater S130 shuttle plus university BEOL post-processing, $15–60k per iteration. Full 130nm run **$0.55–0.65M** (mask set $500–600k: [AnySilicon](https://anysilicon.com/130nm-wafer-mpw-cost/)) [ESTIMATE/REPORTED]. |
| Depreciated U.S. capacity | Cheap to **rent**, not to buy. Fab 25 sold for ~$230 per annual wafer start [ESTIMATE]. |

### 6.3 Back-end verdicts

- **The missing middle is a mid-volume, JEDEC-grade DRAM packaging and test line with open die supply.** It is missing because die supply is captive, not because nobody has thought of building it.
- **Assembly is ~0.6–1% of a 2026 RDIMM's price.** DRAM is 93–98% (us_backend.md §3.4; model §5).
- **Die MOQs** are usually one wafer and often a 25-wafer lot. A lot costs **~$75k (legacy DDR3) to ~$550k (DDR4/DDR5)** at 2026 prices [ESTIMATE, us_backend.md §4.2].
- **Recovered DRAM.** A U.S. industry already exists at module level. Chip-level harvesting does not work here: x4 server die don't fit consumer modules, U.S. labor is expensive, and reballed parts look counterfeit under AS6171. The U.S. open-market DDR4 flow is roughly **0.65 EB/yr, worth ~$1.9–5.2B at 2026 prices and $0.3–1.0B in a glut** (mid case; order-of-magnitude estimate) [ESTIMATE, us_backend.md §6.4].

---

## 7. Funding programs and procurement preferences

### 7.1 What a small company can realistically get (late 2026)

| Program | Status | Realistic $ for us | Fits | Tag / source |
|---|---|---|---|---|
| CHIPS manufacturing incentives ($39B) | Nearly all committed by Jan-2025; now under the U.S. Investment Accelerator, which trades money for equity (Intel ~9.9%, Aug-2025); no open NOFO | **≈$0** | — | [UNVERIFIED-M]; Micron awards [NIST](https://www.nist.gov/node/1855121) |
| §48D ITC | **35%**, refundable via elective pay, but **construction must begin by 2026-12-31** (60 days). BASIC Act (H.R. 3204) extension to 2030 not enacted | **Model 0%** (watch item) | Packaging/test capex if extended | [Baker Tilly](https://www.bakertilly.com/insights/advanced-manufacturing-credits-section-48d); [Instead](https://instead.com/resources/blog/section-48d-credit-rises-to-35-and-why-you-must-act-before-2027); [Congress.gov](https://www.congress.gov/119/bills/hr3204/BILLS-119hr3204ih.htm) |
| NSTC / NAPMP / SMART USA | Natcast agreement voided Aug-2025; NIST took control; 2026 model unpublished | **Assume $0**; sub-awards $0.1–1M if open | Packaging; fab software (SMART USA) | [UNVERIFIED-M] |
| DoD Microelectronics Commons (8 hubs, $2B FY23–27) | Running to FY2027; via NSTXL consortium. NORDTECH (Albany) and Northwest-AI-Hub most memory-relevant | $0.1–2M sub-award per project [ESTIMATE] | eNVM, CIM prototyping | [UNVERIFIED-M] |
| **SBIR/STTR** | Lapsed 2025-10-01; DoD topics reopened Jul-2026, so authority was evidently restored; **terms unverified** | Phase I ~$150–315k; Phase II ~$1–2.1M; DoD Direct-to-Phase II ~$1.2M | Device R&D, provenance/test tooling, memory-efficiency software (NSF) | DV017 ([DARPA](https://www.darpa.mil/research/programs/non-volatile-memory-extreme-environments); [BWCO](https://www.bwcoconsulting.com/fod/dpa26bz04-dv017)); rules [UNVERIFIED-H] |
| — **SBIR PI rule** | PI must be >50% employed by the awardee | **Excludes the founder while he keeps his day job** → use STTR with a university PI, or hire a full-time PI | — | [UNVERIFIED-H] |
| Memory-specific DoD topics confirmed | DARPA DPA26BZ04-DV017 (−269 to +600 °C NVM, ~$1.2M, closed 2026-08-19); USAF AF254-D0806 (500 °C NVM, 2025, closed) | Next cycles | Extreme-environment NVM | [DARPA](https://www.darpa.mil/research/programs/non-volatile-memory-extreme-environments); [SBIR.gov](https://www.sbir.gov/topics/12036) |
| DOE labs: license, CRADA, SPP, TCF, LEEP | CRADA/SPP: company pays; option fees $1–10k; LEEP needs a full-time technical founder | Option ~$1–10k; CRADA is a cost, not money | **Sandia HZO FeRAM** license | [Sandia](https://www.sandia.gov/research/news/evolving-semiconductor-technology-for-national-security-applications/) |
| NSF I-Corps / NNCI | I-Corps ~$50k (needs an academic lead); NNCI cleanroom access | ~$50k | Customer discovery; device prototypes | [UNVERIFIED-M] |
| State programs | NY Green CHIPS is megaproject-only (Micron up to $5.5B); MA START $100–500k (SBIR Phase II cos.); NC One NC ~$12k + $100–150k match; VA CCF $50–100k; AZ Innovation Challenge ~$100–150k | **$10k–500k, mostly multiplying SBIR** | East Coast: VA (Manassas cluster), NY (Albany), MA (START) | [eeNews Europe](https://www.eenewseurope.com/en/micron-new-york-megafab-breaks-ground-2026/); rest [UNVERIFIED-L/M] |
| DPA Title III / Office of Strategic Capital | No memory award found / debt for operating capex | $0 near term | Later T2+ | [UNVERIFIED-L] |

**Bottom line:** in the first 24 months a non-technical founder can expect **$0 of direct federal grant money on his own**. With a university PI (STTR) or a full-time technical co-founder, a device or provenance concept can reach **$0.15–2M** through STTR/SBIR, DoD Direct-to-Phase II and state matches. SBIR **Phase III sole-source** contracts are how SBIR turns into revenue rather than grant farming [UNVERIFIED-H].

### 7.2 Dated cliffs

| Date | Event | Days from 2026-11-01 |
|---|---|---|
| ~2026-11-10 | CMMC Phase 2 (third-party Level 2 assessments, ~$30–100k first-year cost) | 9 |
| ~2026-11-10 | BIS affiliates ("50%") rule suspension may lapse | 9 |
| 2026-12-31 | §48D construction-start deadline | 60 |
| ~2027-07 | ITC 337-TA-1487 (Avalanche v. Everspin) target date | ~240 |
| **2027-12-23** | **§5949 effective** | **417** |
| 2029 | BAA domestic content 65% → 75% | — |

### 7.3 Procurement: does anyone pay for "U.S.-made memory"?

| Rule | What it rewards | Premium for U.S.-made memory? |
|---|---|---|
| Trade Agreements Act (above ~$174k) | U.S. **or designated country**: Korea, Taiwan, Japan, EU qualify; China and Malaysia don't | **No** [UNVERIFIED-H] |
| Buy American Act (below TAA threshold) | 20% / 30% (small business) / 50% (DoD) evaluation factor; **COTS exempt from the component test** | Small buys only; a U.S.-assembled COTS module from foreign die can still count [UNVERIFIED-H] |
| FTC "Made in USA" (16 CFR 323) | "All or virtually all" U.S. content | A module on foreign die can say "Assembled in USA" only [UNVERIFIED] |
| **NDAA FY2023 §5949** (2027-12-23) | Products **without** CXMT/YMTC/SMIC chips | **Rewards verified non-Chinese**, not U.S. origin. Creates a paid compliance need for die-level provenance. FAR implementing rule status unverified ([XenoSpectrum](https://xenospectrum.com/en/apple-china-memory-federal-procurement-ban-2027/)) |
| DFARS 252.246-7007/-7008; FAR 52.211-5 | Authorized, traceable, new parts | **Bars recovered DRAM from DoD deliverables** unless authorized; rewards AS6081-grade traceability [UNVERIFIED-H] |
| DMEA Trusted accreditation | Trusted custom/ASIC parts; COTS memory normally bought commercially | Premium for trusted/rad-hard only; Micron not known to be accredited [UNVERIFIED-L] |
| Section 232 (Phase 1, from 2026-01-15) | 25% on a narrow class of advanced accelerators; **memory ICs and modules pay 0%** | **No** ([CRS](https://www.everycrsreport.com/reports/LSB11409.html); [Korea Times](https://www.koreatimes.co.kr/opinion/20260915/what-us-tariff-push-means-for-koreas-semiconductor-industry)) |
| 100% memory tariff threat (Lutnick, 2026-01-16) | "Build in America" | **Not implemented** ([TrendForce](https://www.trendforce.com/news/2026/01/19/news-lutnick-reportedly-signals-100-memory-tariff-on-non-u-s-output-pressuring-samsung-and-sk-hynix/)) |
| Section 301 | **50%** on China-origin chips; 10–12.5% "forced-labor" 301 on 60 economies from 2026-07-24, with memory treatment unconfirmed | Tilts against CXMT, not toward U.S. ([UHY](https://uhy-us.com/insights/news/2026/july/tariff-reset-section-122-expires-as-section-301-duties-expand); [Wove](https://tariffs.wove.com/us/tariff/8542.32.00.02/16mb-dram-chip/from/CN)) |

**Where premiums are actually paid [ESTIMATE, us_backend.md §4.3, §5.3]:**
- Defense and space hi-rel memory MCMs earn **10–100×** commodity $/bit.
- DoD DMSMS authorized aftermarket parts sell at **1.5–5×**.
- Industrial, rail and medical long-lifecycle parts earn **1.2–2×**.
- From Dec-2027, federal integrators need §5949-clean BOMs.
- Commodity modules assembled in the U.S. earn **0–10%**, and only in BAA-covered small buys.

---

## 8. Export controls and ITAR: constrain vs protect

| Date | Rule | Memory content | Tag |
|---|---|---|---|
| 2022-10-07 | Advanced computing/SME rule | Licences for China fabs making DRAM ≤18nm half-pitch, NAND ≥128 layers | [UNVERIFIED-H] |
| 2024-12-02 | HBM and SME controls | **HBM controlled (3A090.c)**; advanced-DRAM test redefined as cell <0.0019 µm² or >0.288 Gb/mm²; **CXMT left off the Entity List** | [UNVERIFIED-M]; CXMT ([TrendForce](https://www.trendforce.com/news/2025/05/16/news-u-s-rumored-to-mull-adding-dram-giant-cxmt-and-more-chinese-tech-firms-to-entity-list)) |
| 2025-08-29 | VEU revoked for Samsung/SK hynix China fabs (effective 2025-12-31) | Status-quo operation licensed; no expansion or upgrades | [UNVERIFIED-M] |
| 2025-09-29 | Affiliates (50%) rule; reportedly suspended one year from ~2025-11-10 | May resume ~2026-11-10 | [Simpson Thacher](https://www.stblaw.com/about-us/publications/view/2025/10/17/simpson-thacher-attorneys-author-i-law360-i-article-on-bis-50-rule-for-entity-list-and-other-export-restrictive-lists) |
| mid-2026 | **CXMT not on the Entity List** (reports conflict); **on DoD 1260H list** (re-added ~Jun-2026); Apple lobbied to buy CXMT, senators objected | — | [The Next Web](https://thenextweb.com/news/apple-lobbying-us-approval-cxmt-blacklisted-memory-chips); [Schumer](https://www.schumer.senate.gov/newsroom/press-releases/citing-core-national-security-and-economic-reasons-schumer-demands-apple-reject-chinese-military-linked-chips) |
| Rad-hard | ITAR USML XV(d) if all five rad thresholds are met; else EAR 9A515.d/.e or 3A001.a.1 (≥500 krad TID, etc.); deemed exports; CFIUS critical-technology status | Licences for most exports; U.S.-person-only tech data; ~$25–75k/yr compliance | [UNVERIFIED-M]; cost [ESTIMATE] |

**Net effect:** the controls slow CXMT/YMTC technology and freeze capacity at the Korean firms' China fabs, which prolongs the shortage and helps incumbents. **They do not stop CXMT's mature-node DDR4/DDR5 exports to the U.S.**, which are handled by tariffs and §5949, not by export controls.

| Concept family | Exposure | Protection | Net |
|---|---|---|---|
| Memory-efficiency software (KV-cache, tiering, compression), price intel, QVL tools | EAR99 / mass-market 5D992 | None needed | **Unconstrained** |
| CXL memory appliances/pooling | Generally EAR99/4A994; bundling with controlled GPUs to China adds risk | None | Lightly constrained |
| **§5949 provenance / test / compliance** | EAR99 services | **§5949 creates the demand** | **Protected by policy demand** |
| Recertified / recovered DRAM | EAR99; MEU screening | DFARS **constrains** DoD sales; 50% duty on China-origin dies | Open commercially, constrained in defense |
| U.S. legacy DRAM | Not controlled | §5949 and the China tariff tilt toward non-Chinese supply; no U.S.-origin premium; competes with Micron Manassas | Weakly protected |
| HBM / advanced stacking | 3A090.c to China | Benefits from China being cut off | Irrelevant at our scale |
| **Rad-hard / extreme-environment NVM** (HZO FeRAM, ReRAM on S130) | **3A001.a.1 / 9A515 / possibly ITAR XV(d)**; deemed exports | DoD trusted-supply preference; SBIR topics | **Exports constrained; U.S. defense market protected**. Competes with European "ITAR-free" parts (3D Plus, Teledyne e2v) |
| Device IP licensing | Controlled only if the item is | None | Mostly unconstrained |

---

## 9. Patent landscape and tech-transfer opportunities

### 9.1 By technology

| Technology | Key holders | Licensable to a small U.S. startup? | Base patents expired? | Litigation risk | Best path |
|---|---|---|---|---|---|
| Oxide-semiconductor DRAM (IGZO/ITO/IWO/In₂O₃; 2T0C, OCTRAM, 4F² VCT) | **SEL** (DOSRAM/NOSRAM; [USPTO 10,276,578](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10276578)), Kioxia+Nanya ([OCTRAM](https://www.businesswire.com/news/home/20241209099702/en/Kioxia-Develops-OCTRAM-Oxide-Semiconductor-Channel-Transistor-DRAM-Technology)), Samsung (4F² VCT IGZO, 2028 target: [TrendForce](https://www.trendforce.com/news/2026/04/24/news-samsung-reportedly-produces-sub-10nm-10a-dram-working-die-using-4f-square-and-vct-targets-2028-production/)), SK hynix, Micron, imec (members only) | Corporate **closed**; SEL possible but costly; **universities likely** (Purdue In₂O₃, GT IWO 3T: [GT](https://hg.gatech.edu/node/675050)) | a-IGZO TFT base ~2023–25 yes; memory cells no (a 2T IGZO gain cell was granted 2025: [USPTO 12,191,135](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12191135)) | **MED-HIGH** | University option on a non-VCT BEOL gain cell plus an SEL FTO ($15–30k) |
| Ferroelectric (HZO FeRAM/FeFET/FTJ; PZT; AlScN) | FMC (€100M raise Nov-25, DRAM+, licenses to IDMs only: [HPCwire](https://www.hpcwire.com/off-the-wire/fmc-raises-e100m-to-set-new-standards-for-memory-chips/)), Micron NVDRAM ("might never become a product": [Blocks & Files](https://blocksandfiles.com/2024/01/09/micron-nvdram-might-never-become-a-product/)), Intel, **Sandia**, **Penn/AFRL AlScN** (600 °C: [Penn](https://www.engineering.upenn.edu/stories/turning-up-the-heat-on-data-storage/)) | FMC/Micron/Intel **closed**; **Sandia, Penn likely** | PZT yes; **HfO₂-FE base ~2027–28** [ESTIMATE] | LOW-MED | **Sandia HZO license + CRADA + STTR** (rad-hard NVM); Penn AlScN + STTR (>500 °C NVM) |
| MRAM (Toggle, STT, SOT) | Everspin, Avalanche (UMC 22nm: [TechInsights](https://www.techinsights.com/blog/avalanche-as301g208-umc-22-nm-512mb-mram-process-analysis)), IBM, foundries; universities (UMN, Cornell, UCLA, Northwestern) | Everspin at defense-prime scale only ($40M Amentum: [Electronics360](https://electronics360.globalspec.com/article/23702/everspin-earns-40-million-mram-deal-for-defense-memory-services)) | STT concept ~2015, Toggle ~2021, MgO ~2021–25; pMTJ to ~2029–30 | **HIGH**: ITC 337-TA-1487 Avalanche v. Everspin, instituted 2026-02-27, target ~Jul-2027 ([USITC](https://www.usitc.gov/press_room/news_release/2026/er0227_68226.htm)); Everspin $6.0M litigation cost in Q3-26 ([8-K](https://www.sec.gov/Archives/edgar/data/0001438423/000162828026067890/mram-20260930xexx991.htm)) | **Buy and design in** (patent exhaustion); keep Toggle or a second source |
| ReRAM / CBRAM | **Weebit** (in SkyWater S130 PDK; licensees TI, onsemi, DB HiTek; FY26 ≥A$13.5M: [Weebit](https://www.weebit-nano.com/news/press-releases/weebit-nano-expands-licensing-agreements-with-key-customers-three-customer-chip-designs-taped-out-to-date/)), TetraMem (licensable: [BusinessWire](https://www.businesswire.com/news/home/20260516556464/en/TetraMem-Announces-22nm-Multi-Level-RRAM-Analog-In-Memory-Computing-SoC-Milestone)), Crossbar, GF CBRAM (closed) | **Weebit open via S130** (terms unknown); TetraMem open | PMC/CBRAM base ~2016 | LOW-MED | **Weebit ReRAM on SkyWater S130**: the only qualified, U.S.-fab, PDK-resident memory IP found |
| PCM / 3D XPoint | Intel & Micron (stranded estate), ST/Samsung (ePCM), SanDisk 3D Matrix Memory ([Notebookcheck](https://www.notebookcheck.net/SanDisk-makes-first-3D-Matrix-Memory-chips-aiming-for-half-the-cost-per-bit-of-DRAM.1374351.0.html)) | **Closed** | Ovshinsky-era yes | LOW now; latent NPE risk | None. Reselling Optane needs no license |
| Capacitor-less Si DRAM (Z-RAM, T-RAM, FBC) | Mostly expired; Unisantis (VCT claims) | Effectively open | 2018–26 | LOW | Free but physics-dead. **Nothing worth licensing** |
| 3D DRAM (VCT, VS-DRAM, 3D X-DRAM) | Samsung, SK hynix, Micron, CXMT, NEO (IDMs only; PoC 2026-04: [StorageNewsletter](https://www.storagenewsletter.com/2026/05/13/neo-semiconductor-demonstrates-3d-x-dram-proof-of-concept-secures-strategic-investment-to-advance-ai-memory/)) | **Closed** | No | HIGH from ~2028 | None |
| NRAM (CNT) | Nantero (status unknown) | Unknown, possibly distressed | Early filings ~2021–24 | LOW | Check assignments only |
| 2D / organic / printed | Universities | Likely, cheap | — | LOW | TRL 2–4; kill for a revenue founder |
| SRAM / open-source | OpenRAM BSD-3, sky130 open PDK ([OpenRAM](https://github.com/VLSIDA/OpenRAM)) | **Open, free** | n/a | LOW | Use freely |
| *Adjacent:* DIMM / PMIC / interface | **Netlist** (E.D. Tex.: $303M v Samsung 2023, $445M v Micron 2024, $118M v Samsung 2024; PMIC-on-DIMM claims read on DDR5 RDIMMs), Rambus, Polaris | Netlist unlikely | Older DIMM patents yes; PMIC family live | **HIGH** | Buy finished modules from licensed makers; FTO before any DDR5 RDIMM [UNVERIFIED] |

### 9.2 Tech-transfer targets (ranked for this founder)

| Rank | Target | What | Mechanism | Fit |
|---|---|---|---|---|
| 1 | **SkyWater + Weebit** | ReRAM qualified in S130 (256 Kb, 125 °C) | Commercial IP license plus foundry | U.S.-made secure/eNVM/long-lifecycle part; T1–T2; IP cost known after one call |
| 2 | **Sandia** | HZO FeRAM + FTJ in the trusted MESA flow | License + CRADA (+ STTR) | Rad-hard NVM for DoD/space; trusted provenance; T1; needs a technical PI |
| 3 | **Penn + AFRL** (via TechLink) | AlScN ferro-diode NVM at 600 °C | License + STTR; DARPA/USAF demand exists | Extreme-temperature niche; TRL ~3–4 |
| 4 | **Purdue / Georgia Tech** | ALD In₂O₃ BEOL tiers on 200mm / 3T IWO eDRAM | Option ($1–10k) | Keeps an IGZO door open; exercise only if a fab agrees in writing |
| 5 | Distressed estates | 4DS (ASX-suspended 2026-04-29: [filings](https://financialfilings.com/companies/4ds-memory-limited/)), Spin Memory, Nantero, HPE memristor | Assignment-record search; purchase | Litigation/defensive assets, not a business |

**Typical university terms** [UNVERIFIED-training]: option $1–10k; exclusive license in 2–6 months; 2–10% equity; 1–3% royalty for semiconductor components; past patent costs $10–150k (usually the largest cash item, often deferred). National-lab licenses take 3–9 months and CRADAs 3–12 months. **Bayh-Dole §204 / DOE rules require substantial U.S. manufacture** of licensed products. That aligns with "American Memory", but offshore fabbing needs a waiver. **A T0 IP path (option, scoped FTO, provisionals) costs ≈$25k, about half the founder's budget** [ESTIMATE, ip_landscape.md §6.6].

**Being a licensor is slow:** Weebit took ~10 years to reach ≥A$13.5M/yr, Everspin's licensing line was $6.9M in FY2025 ([BusinessWire](https://www.businesswire.com/news/home/20260304733194/en/Everspin-Reports-Unaudited-Fourth-Quarter-and-Full-Year-2025-Financial-Results)), and FMC raised €120M+ over ~9 years with no product ([heise](https://heise.de/-11151026)) [REPORTED]. **The founder should be a licensee who builds a product, not a licensor.**

---

## 10. Implications for ideation and scoring

### 10.1 Where the openings are (ranked for this founder: T0–T1, software/ops strength, 18-month revenue)

| # | Opening | Why it is open | Glut test | First kill test (<$10k, <30 days) |
|---|---|---|---|---|
| O1 | **§5949 provenance, screening and "verified non-Chinese memory" service** for federal integrators and regulated buyers (BOM scan, supplier attestation, sample X-ray/marking analysis, serialized reports) | Hard date (2027-12-23); CXMT (9.5% of 2Q26 DRAM revenue) is the main source of new conventional bits; Chinese die often hides inside third-party modules; software- and ops-heavy; DoD SBIR angle (supply-chain illumination) | **Passes**: regulatory, not price-driven | Interview 10 federal/defense IT integrators; confirm the FAR implementing rule's status and scope |
| O2 | **Memory-efficiency software** (KV-cache tiering, CXL orchestration, compression, memory-aware scheduling) | Each GB saved is worth ~$16 of contract DRAM now and ~$6.4 in a glut; export-unconstrained; no fab, die or CHIPS dependence | **Partially**: ROI falls ~60% but stays positive | Hand off to Phase 2 branches B/D for workload evidence |
| O3 | **Module-level recertification of decommissioned DDR4 RDIMMs that evolves into a trust layer** (AS6081-style test reports, §5949 attestation) | ~20% contribution at 2026 prices; T0 starter kit $8–20k plus $10–30k inventory | **Fails as resale** (1–6%); survives only as the provenance layer of O1 | Pull 90 days of eBay sold listings for 32GB/64GB DDR4 RDIMMs; if the median is below $2/GB, kill |
| O4 | **Long-lifecycle / DMSMS services for mid-size OEMs** (LTB sizing, EOL forecasting software, die-bank brokering via Rochester/Micross) | Buffers at 6–8 weeks; zero authorized stock; Rochester/Micross serve big primes | **Passes**: lifecycle-driven | Interview five industrial OEMs; get Rochester/Micross die-bank pricing |
| O5 | **Niche NVM on licensable U.S. IP**: Weebit ReRAM on SkyWater S130; Sandia HZO FeRAM; Penn AlScN | Only open, U.S.-fab memory IP; DoD demand and SBIR topics; glut-indifferent | **Passes** | Ask SkyWater/Weebit for startup license terms and MPW access; ask Sandia about HZO licensing/CRADA. **Requires a technical PI** |
| O6 | **Data products** (price intelligence, QVL, patent-expiry/assignment intelligence) | Software-only | Partial | Crowded at both ends (TrendForce/inSpectrum paid; trackers free). Mobius shows **data as a funnel to transactions** is the defensible pattern ([YC](https://www.ycombinator.com/companies/mobius-materials)) |

### 10.2 What looks closed (kill or downgrade in Phase 3 unless new evidence appears)

| Closed path | Reason (section) |
|---|---|
| Any U.S. DRAM fab or trailing-node DRAM line (T3/T4) | No host; $3.28/GB new-line cost; −153% GM at trough; Micron Manassas already serves the long-lifecycle buyer with CHIPS money (§4, §6) |
| IGZO on display fabs; IGZO or ReRAM as "cheaper DRAM" | No U.S. display fab; 60–490× density gap; SEL estate (§6.2, §9) |
| "Assembled in USA" commodity DDR4/DDR5 module brand | Die unobtainable; assembly ~1% of value; FTC limits the claim; Netlist PMIC patents (§6.3, §9) |
| Licensing in DRAM-class IP; becoming a memory-IP licensor | Closed to non-IDMs; 5–10 years to revenue (§9) |
| Any alternative memory pitched on $/GB | Nothing within 10× of DDR5 cost; MRAM ~$821/GB street (§4.4) |
| HBM packaging or stacking | Captive to SK hynix/Micron; 2028–29; Amkor AZ is logic (§6) |
| Anything whose model needs CHIPS grants or §48D | Closed or closing in 60 days (§7) |
| Chip-level DRAM harvesting | x4 geometry, labor, counterfeit exposure (§6.3) |

### 10.3 Scoring rules to carry into Phase 3

1. **Glut line: $6.40/GB DDR5 contract; severe line: $1.60/GB.** Score cycle-proofing against both, and say which a concept fails.
2. **Timing:** price-arbitrage revenue must be cash-positive by **end-2027**.
3. **FTO gates:** DDR5 module/appliance → Netlist PMIC; IGZO cell → SEL; Everspin STT design-in → ITC 337-TA-1487 outcome (~Jul-2027); VCT-like device → Samsung/Micron/Unisantis.
4. **Funding realism:** score SBIR only if the concept names a full-time PI or a university STTR partner. CHIPS and §48D = 0.
5. **Die-supply kill test** for any concept that needs Micron silicon: one email to SpecTek about wafer/KGD availability and MOQ.
6. **"U.S.-made" claims must be specific:** trusted foundry, §5949-clean or BAA small-buy. Never "Made in USA" on foreign die.

### 10.4 Contradictions between researchers and how I resolved them

| # | Contradiction | Resolution |
|---|---|---|
| 1 | Glut price: p1-market −60% from **spot** → ~$11.4/GB (severe $2–4) vs p1-cost/model −60% from **contract** → $6.40/GB (severe $1.60) | **Model contract deck is canonical** (matches A-05, stricter). $11.4 kept as an upper-bound sensitivity |
| 2 | 4Q26 RDIMM contract: Citi $1,586 vs model $1,300 vs compounded $1,877 | **$1,300** (traceable to Counterpoint × TrendForce); Citi is UNVERIFIED |
| 3 | 1-beta wafer cost: p1-cost $3.8k vs A1/A2 $5.5–6.0k | $3.8k = incumbent steady state; $5.5k = new entrant or new fab. Both used, for different questions |
| 4 | DDR4 price: branded spot $44/GB (1.65× DDR5) vs model's legacy contract parity ($16/GB) | Parity kept in the model and flagged as a weak input. DDR4 spot is never used as a concept's base case |
| 5 | Cost figures: p1-cost $1.62/GB, $152 RDIMM, $216 HBM stack vs model $1.64, $154, $219 | **Model wins** (it adds final-test fallout); differences are 1–2% |
| 6 | Module economics: p1-backend $25 parts + $12 U.S. assembly vs p1-cost $17.1 + $3.5 Asia | Model: U.S. assembly adds $8.63 (0.7% of price). **Same conclusion**: assembly is not a value-capture point |
| 7 | "Micron is the only manufacturer of memory in the U.S." (Micron's own phrase, via p1-micron) vs p1-fabs (Everspin, Honeywell, TI make memory) | Micron is the only U.S. **DRAM** wafer maker. Others make niche NVM |
| 8 | SK hynix Indiana: "2H 2028" (some outlets) vs "HBM4E from Q3 2029" (CEO) | **Plan 2029** |
| 9 | Micron NY1: ConstructConnect "Q1 2029" vs 10-K "CY2030" | **10-K wins** |
| 10 | TrendForce 4Q26: official +10–15% vs "~+20%" Oct-20 revision (AI aggregator, blog) | **+10–15%**; revision UNVERIFIED |
| 11 | Relief timing: Micron/UBS/Barclays (tight through 2028) vs Bloomberg Intelligence (balance ~4Q27, oversupply 2028) vs BofA (soft −10% in 2028) | House call: peak 4Q26–2Q27, turn 2028, glut 2H28–29 only if AI capex slows. Score against the glut regardless |
| 12 | Mission: "HBM absorbs capacity" (implies HBM is the profit center) vs the model and Samsung (HBM3E less profitable than DDR5 in 2026) | Both true. HBM gets wafers because of 2027 HBM4 pricing (~3×) and LTAs, not 2026 margins |

### 10.5 Verification queue (highest decision weight first; ~30 searches or a few emails)

1. **§5949 FAR implementing rule**: status, effective date, and whether it reaches DIMMs inside servers. O1 depends on it.
2. **SBIR/STTR reauthorization terms** (public law, caps, PI rule).
3. **SpecTek wafer/KGD availability and MOQ** (an email).
4. **eBay sold-listing medians** for 32GB/64GB DDR4 RDIMMs (one hour).
5. **TrendForce press center**: 4Q26 forecast text, any October revision, 3Q26 actuals, NAND October.
6. **SkyWater/Weebit startup license terms** and post-Efabless shuttle access.
7. **Sandia HZO FeRAM licensing/CRADA availability** (Sandia IP portal).
8. **CXMT Entity List status** and the affiliates-rule restart (~2026-11-10).
9. **Section 232 Phase 2** and Section 301 treatment of HTS 8542.32/8473.30 from Korea and Taiwan.
10. **TechInsights 1-beta/1-gamma DDR5 die sizes** and an IC Knowledge wafer-cost estimate. These are the two weakest model inputs.
