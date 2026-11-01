# DD1: Provenance & Recertified Memory (research notes)

**Agent:** `p4-provenance-recert` · **As of:** 2026-11-01 · **Bundle:** anchor C-64 (CleanBOM-5949), with C-62 (ProvenRAM recert), C-85 (DIMM-health) and C-26 (Optane PMem salvage) folded in.
**Model:** `models/provenance-recert.py` (exits 0); its output is in `research/phase4/provenance-recert_model_output.md`.
**Sources:** `research/sources/p4-provenance-recert.jsonl` (76 entries). **Assumptions:** `research/assumptions/p4-provenance-recert.md`.

> **Evidence grade.** I used all 30 of my WebSearch calls. My one WebFetch (govinfo.gov) failed DNS, and per the tool's instruction I stopped there. **Every external fact below is search-snippet grade, so nothing is [VERIFIED].**
> - [REPORTED-P] means a primary page (Federal Register, company page, contract record) seen only as a snippet. [REPORTED] means secondary coverage. [UNVERIFIED-training] means my own prior knowledge with no URL found this session. [ESTIMATE] means a model input or output.
> - Facts carried over from 01_LANDSCAPE and the Phase 2/3 cards keep their original tags.

---

## 0. Verdict in one screen

**The whole is better than any single part, but for a different reason than the hypothesis says.** The model runs each part separately and in combinations, with the same founder and the same $40k (model §4):

| BASE scenario, 36 months | ARR m36 | Cash m36 | Cumulative EBITDA |
|---|---|---|---|
| Full bundle | $445,543 | $610,097 | $662,971 |
| Bundle **without** the evidence lift (CleanBOM closes at the standalone 7%) | $323,558 | $461,433 | $513,988 |
| Bundle with the founder **never** going full-time | $199,038 | $480,218 | $501,841 |
| CleanBOM standalone | $120,296 | $91,351 (cash dips to −$6.5k at m15) | $52,851 |
| Recert + PMem only | $0 recurring ($1.21M run-rate) | $169,467 | $208,516 |
| DIMM-health standalone | $27,187 | $583 | −$26,165 |

The table shows three things:

1. **The real synergy is cash buying founder time.** Recert profits let the founder quit the day job in month 14 (Dec-2027). That more than doubles CleanBOM selling capacity, and it is worth about $247k of the $446k base ARR at m36.
2. **The die-source library is a smaller synergy, and an unproven one.** It is worth about $122k ARR at m36, and it rests entirely on an assumed 3-point close-rate lift (10% vs 7%) that nobody has measured.
3. **DIMM-health and PMem add little.** DIMM-health adds about $61k ARR at m36, and PMem is a small two-year SKU.

**Glut-proofing is real only for the recurring lines.** In GLUT the bundle still ends with $392k cash and $434k ARR. Recert-only ends with $22k cash. In SEVERE, recert-only ends at −$7.6k cash and the bundle at $328k. Recert is a 14-to-20-month cash bridge that must turn into CleanBOM customers before the 2028 turn.

**Recommendation:**
- Run it as a **sequenced bundle**: recert is the cash engine, and CleanBOM-5949 is the company.
- Keep PMem as an opportunistic SKU until 2027-10-11.
- **Demote DIMM-health from a product line to a wholesale spares-plus-CE-feed offer to TPMs.** Standalone it never covers its costs, and the buyer can self-spare for about a quarter of the fee.
- What decides the venture: **about 10 paying provenance subscribers by month 18**. The model reaches 7.5 at 5 conversations a month and a 10% close.

---

## 1. Question 1: §5949 demand after the proposed rule's self-certification safe harbor

### 1.1 Where the rule stands (2026-11-01)
- **FAR Case 2023-008 is still a proposed rule.** It was published 2026-02-17 (91 FR 7223), comments closed 2026-04-20, and a search on 2026-11-01 found no final rule. The statute required a final rule by 2025-12-23, a deadline that was missed. The prohibition still takes effect on **2027-12-23** ([Federal Register](https://www.federalregister.gov/documents/2026/02/17/2026-03065/federal-acquisition-regulation-prohibition-on-certain-semiconductor-products-and-services); [PSC comments 2026-04-20](https://pscouncil.org/a/Resources/2026/PSC_Comments_2026Apr_Semiconductor_20260420.aspx)) [REPORTED-P].
- **The proof standard is light.** A "reasonable inquiry" does **not** require independent third-party audits, and contractors "may in good faith rely on certifications provided by lower-tier subcontractors" ([Mayer Brown 2026-03-03](https://www.mayerbrown.com/en/insights/publications/2026/03/far-council-proposes-rule-to-prohibit-acquisition-of-semiconductors-from-china-and-countries-of-concern); [Covington](https://www.insidegovernmentcontracts.com/2026/02/far-council-issues-notice-of-proposed-rulemaking-to-implement-prohibition-on-acquisition-of-certain-semiconductors/)) [REPORTED].
  - The listed inquiry methods include "asking suppliers, checking supplier websites, or using other supply chain due diligence tools" ([Reed Smith](https://www.reedsmith.com/articles/breaking-circuit-how-covered-semicon-ban-reshaping-supply-chain-usgovcon/)) [REPORTED]. Tools are allowed, but no vendor is named and none is required.
- **Scope.**
  - Part B does **not** reach contractors' private use.
  - The rule is prospective, so no rip-and-replace.
  - Commercial *services* are excepted, except IT and telecom ([Wiley](https://www.wiley.law/alert-FAR-Council-Proposes-Rule-to-Ban-Purchases-of-Certain-Semiconductor-Products-and-Services)) [REPORTED].
  - Coverage is still SMIC, CXMT and YMTC plus affiliates; no further designations have been made [REPORTED].
- **New lever: FY2024 NDAA §805.** DoD's ban on *direct* contracting with §1260H "Chinese military companies" took effect 2026-06-30. The ban on goods that *incorporate* their products starts **2027-06-30**, six months before §5949 ([Crowell](https://crowell.com/en/insights/client-alerts/new-year-updated-list-the-us-department-of-defense-updates-its-list-of-chinese-military-companies-with-ancillary-supply-chain-and-usg-contracting-impacts); [Z2Data](https://www.z2data.com/insights/how-section-1260h-is-putting-teams-at-risk-of-violating-ndaa-compliance); waiver process at [businessdefense.gov](https://www.businessdefense.gov/805-waiver-request.html)) [REPORTED].
  - **Caveats:** §805 is DoD-only, and the snippet mentions an exception for components "bought generally and as part of an end product", which may exempt memory inside COTS servers.
  - **CXMT/YMTC §1260H status is contradictory.** One report says a provisional Feb-13-2026 update removed both ([HWBusters](https://hwbusters.com/news/cxmt-ymt-pentagons-list-a-memory-war/)). Another says DoD listed them on 2026-06-10 ([SamSearch](https://samsearch.co/government-contracting-news/federal-agencies-brace-for-restrictions-on-chinese-semiconductor-procurement-143279)). 01_LANDSCAPE says CXMT is listed and has sued [REPORTED, conflicting]. **Open item #1.**
- **Possible private-market lever.** In July 2026, House China Committee leaders asked Commerce to restrict U.S. companies from buying from CXMT and YMTC ([Kyungbuk Maeil citing FT, 2026-07-17](https://kbmaeil.com/article/20260717500103)) [REPORTED]. If adopted, "no-China memory" demand would move from federal procurement into all commerce. It is not adopted, and I do not model it.
- **State and local "no-China" procurement laws.** I found **no** state statute aimed at Chinese *semiconductor content* (search 2026-11-01). Several states restrict "foreign adversary" *vendors and apps* in state contracts or critical infrastructure [UNVERIFIED-training], but none reaches die-level content. Treat this as zero demand.

### 1.2 Who still pays for verification under the safe harbor (ranked)
The safe harbor moves liability *upstream*: whoever writes the first certification needs the die-level knowledge. My ranking of willingness to pay:

| # | Buyer | Why they pay | Willingness to pay |
|---|---|---|---|
| 1 | **Third-party "OEM-compatible" memory makers** that sell into federal through resellers: AddOn Networks ([listing](https://www.lttpartners.com/products/addon-cisco-reg-ucsx-mrx64g2re5-64gb-ddr5-6400mhz-registered-dual-rank-x4-1-1v-288-pin-rdimm)), Axiom ([site](https://www.axiomupgrades.com/inside-the-stack-detail/Third-party-maintenance-How-can-it-help-your-business-)), Brute Networks ([Newegg](https://www.newegg.com/Brute-Networks-Server-Memory/BrandSubCat/ID-161080-541/Page-42)); also Edge, Total Micro, Origin Storage [UNVERIFIED-training] | They buy DRAM on the open market, where CXMT is now the marginal supplier. Their certification is the one resellers rely on, and a false one carries False Claims Act-adjacent exposure. | **Highest.** The $2,500/mo tier |
| 2 | **White-box server, appliance and industrial-PC builders** on GSA/SEWP | They certify their own BOMs and cannot see die source behind module labels | Medium. $750–2,500/mo |
| 3 | **OEMs and ODMs** (Dell, HP, Lenovo, Supermicro) | Reports conflict: Dell reportedly banned CXMT while HP accepts it only for China-market PCs ([Pause Hardware](https://pausehardware.com/memoire-cxmt-oem-pc-penuries/)), yet Dell, HP, Lenovo and Apple reportedly hold CXMT allocation through end-2027 ([Gazlog](https://gazlog.jp/entry/oem-going-for-cxmt/); [Pause Hardware](https://pausehardware.com/cxmt-memoire-stocks-dram-oem/)). OEMs are avoiding making CXMT a fixed BOM item because of government-sales eligibility [REPORTED] | Big budgets, but they build in-house or buy from Exiger-class vendors. **Not a founder's first customer** |
| 4 | **Federal resellers**: SHI public sector, which sells DDR4/DDR5 RDIMMs and PMem ([SHI](https://www.publicsector.shidirect.com/product/47547768/64GB-2RX4-DDR4-3200-ECC-RDIMM)), and small SEWP V / GSA MAS holders | Will mostly pass OEM certifications through, as the safe harbor allows | Low. One-off evidence packs for odd lots, refurb and "compatible" SKUs ($900) |
| 5 | **Defense primes** | They already run AS6081/AS6171 supply chains, and DFARS counterfeit rules apply | Would buy *die-source data*, not workflow |
| 6 | **Compliance-data vendors** (Z2Data, SiliconExpert/Accuris, Exiger) | They need memory die-source data they do not have; Z2Data already markets NDAA 1260H screening | A licensee or acquirer for the dataset; B2B2B upside, not in the base model |

**Section 889 analog.** Huawei/ZTE Part B produced a reps-and-certs plus supply-chain-illumination software market, not a lab-testing market [UNVERIFIED-training]. The 2026 awards fit that pattern: Exiger got $12.7M from the Army for a 1Exiger subscription (listed 2026-10-01) ([HigherGov](https://www.highergov.com/news/exiger-wins-13-million-army-1exiger-supply-chain-6490162/)), and Interos got about $12M over 3 years from DLA via SEWP ([Orange Slices](https://orangeslices.ai/dla-inks-12m-contract-to-acquire-interos-ai-software/)) [REPORTED]. These are enterprise *agency* buys, so the SMB integrator and module-maker tier is still open.

### 1.3 What comparable compliance tools charge

| Vendor | What it does | Price evidence | Tag |
|---|---|---|---|
| SiliconExpert (Arrow) | Component lifecycle, risk and compliance data | No list price. Accuris's switching offer is 20% below a customer's SE ACV with a **$6,000 minimum ACV**, which implies SE contracts start around $7.5k/yr ([Accuris](https://accuristech.com/siliconexpert-offer-terms/)) | [REPORTED-P] |
| Exiger (1Exiger) | Supply-chain illumination and risk | $12.7M Army subscription (2026-10-01); $75M GSA software vehicle ceiling | [REPORTED] |
| Interos | Supply-chain risk mapping | ~$12M over 3 years via DLA/SEWP (~$4M/yr) | [REPORTED] |
| Z2Data | Part and supplier risk; markets 1260H compliance | Not published | [REPORTED] (product), price gap |
| Assent, Sourcemap | Supplier compliance, mapping | **Not found** (gap) | — |
| OBSIDIA | REELScan non-destructive reel scanning to catch recycled, cloned or remarked parts; founded 2025, San Leandro CA; $34M CHIPS R&D LOI ([SEMI](https://www.semi.org/en/blogs/rethinking-authenticity-in-the-semiconductor-supply-chain-a-conversation-with-obsidia-semiconductors); [Dealroom](https://app.dealroom.co/companies/obsidia_semiconductor); 01_LANDSCAPE §7.1) | Not published. Aimed at defense and aerospace reels, not module die-source | [REPORTED] |
| Mobius Materials (Richmond VA) | Authenticated surplus-component marketplace building ML authentication (patent filed); claims memory RFQs in Q1-26 were 32× all of 2024 and bid prices rose 19× in six months ([Mobius blog](https://mobiusmaterials.com/post/the-memory-market-has-structurally-changed-heres-what-that-means-for-buyers-and-sellers); [DC360](https://www.digitalcommerce360.com/2025/12/16/b2b-marketplace-mobius-materials-3-million-funding/)) | Marketplace take rate, not published | [REPORTED, company claims] |

**Pricing call** [ESTIMATE]:
- Integrator/reseller tier: **$750/mo**.
- Module-maker/ODM die-source tier: **$2,500/mo**, with 35% of customers on it, for a blended ARPA of $1,362.
- One-off evidence pack: **$900**.
- Die-ID samples: lab cost × 1.6.

That sits above SiliconExpert's entry floor and two to three orders of magnitude below the enterprise awards. CleanBOM gross margin is **80%** (model §1c).

---

## 2. Question 2: Can SPD/JEP106 die bytes be trusted? What does physical proof cost?

- **Who writes the bytes.** The module assembler programs the SPD EEPROM, both the module-maker ID (DDR4 bytes 320–321, DDR5 512–513) and the DRAM-maker ID (DDR4 350–351, DDR5 552–553). memtest86+ maps CXMT as JEP106 `0x0A11` and YMTC as `0x091B` (C_notes §7.7, from a clone of memtest86+ [VERIFIED in Phase 2]; die-byte offsets from the Samsung datasheet and coreboot, via snippet).
  - SPD fields can be rewritten and labels copied, and counterfeiters program whatever SPD they like ([Evetech](https://evezone.evetech.co.za/build-lab/spot-fake-relabelled-ram-used-market); [Igor'sLAB](https://www.igorslab.de/en/counterfeit-ddr5-modules-china-brand-ram-trust/)) [REPORTED].
  - **So the SPD die byte is the module maker's self-declaration.** As evidence it is worth exactly what a supplier certificate is worth, and the safe harbor already accepts those for free. The scanner therefore adds nothing on its own. Value comes only from (a) a part-number-to-die cross-reference built from physical evidence and (b) exception testing.
- **CXMT die is inside Western-brand modules in 2026** [REPORTED]:
  - Corsair Vengeance DDR5 (China-exclusive kit; CPU-Z shows CXMT) ([Tom's Hardware](https://www.tomshardware.com/pc-components/ddr5/chinese-memory-maker-cxmt-enters-the-mainstream-consumer-memory-with-corsair-vengeance-ddr5-kit-chinese-made-dram-emerges-as-an-antidote-for-crushing-shortages)).
  - Lexar and KingBank kits ([Outlook Respawn](https://respawn.outlookindia.com/gaming/gaming-news/pc-industry-turns-to-cxmt-as-dram-supply-crisis-persists)).
  - HP, Asus and Acer notebooks sold outside the U.S. (TrendForce citing Nikkei, via [3DNews](https://3dnews.ru/1146214/hp-inc-asus-i-acer-nachali-ispolzovat-kitayskuyu-pamyat-proizvodstva-cxmt/print)).
  - Gigabyte supports CXMT dies across its DDR5 boards.
  - A reseller markets a **CXMT-made 64GB DDR5 RDIMM (CXMR4E464R8AS-CB1C) as compatible with Dell PowerEdge 16G and HPE ProLiant Gen11** ([router-switch.com](https://www.router-switch.com/sw/faq/cxmt-ddr5-server-memory-cxmr4e464r8as-cb1c-dell-hpe-sizing.html), vendor claim). CXMT server memory is reaching the U.S. "compatible" channel.
- **Relabeling and counterfeits in 2026** [REPORTED]:
  - Dummy plastic "chips" relabeled as legitimate ([Tom's Hardware](https://www.tomshardware.com/pc-components/ddr5/scammers-are-selling-fake-ddr5-with-empty-plastic-chips-relabeled-to-pass-as-legit-fake-components-mounted-to-pcbs-are-yet-another-sign-of-the-rampocalypse)).
  - A module labeled Samsung carrying SK hynix chips ([Digital Citizen](https://www.digitalcitizen.life/5-ram-scams-to-watch-for-as-memory-prices-keep-rising/)).
  - DDR4 chips on fake DDR5 boards (01_LANDSCAPE §6.3).
  - **Gap:** I found **no documented case of CXMT die relabeled as Samsung, Micron or SK hynix in U.S.-channel server RDIMMs**, and no 2026 ERAI or GIDEP memory alert (01_LANDSCAPE). The fraud evidence so far is consumer-channel.
- **Physical verification methods and costs** [REPORTED, weak]:
  - AS6171/5 radiological (X-ray) and AS6171/4 delid/decap physical analysis, run at ISO/IEC 17025 + AS6171 labs ([ANSI/CALCE slides](https://share.ansi.org/Shared%20Documents/Standards%20Activities/Microelectronics%20Supply%20Chain%20Security/October%2026-28,%202022%20Workshop/30%20September%202022%20Standards%20Briefings/AS6171%20Overview%20for%20ANSI%20Meeting_Azarian_30Sep2022.pdf)). **ANAB has accredited 26 such labs** ([ANSI blog](https://blog.ansi.org/anab/benefits-as-6171-suspect-counterfeit-eee-parts/)).
  - Price indications: **$50–500 per component** for verification and **$150–500 per sample for SEM**, with turnaround of 5–10 business days to 2–6 weeks ([Industrial Monitor Direct](https://industrialmonitordirect.com/blogs/knowledgebase/detecting-counterfeit-ics-in-industrial-electronics), weak blog source).
  - A typical lot plan samples 30 pieces per 1,000. Decap compares die marking and logo against a reference ([USBid](https://usbid.com/blog/integrated-circuit-ic-decapsulation-and-die-verification)).
  - **No price was found** for SMT Corp, Integra (DMEA-trusted for test), Micross (DMEA) or ERAI member labs. The model uses **$400 per die-ID sample** [ESTIMATE], and the kill experiment gets a real quote.
- **What the library buys.** One decap of one module part number and date-code family identifies the die source for every unit of that family. That is the economics of a reference library: a per-part-number fixed cost spread across many scans. The recert flow puts hundreds of distinct part numbers on the bench for free. The model's library reaches **63 lab-confirmed part numbers by month 36**, plus SPD records on roughly 15k recert modules.

---

## 3. Question 3: Recert economics now

### 3.1 Prices
| Item | Evidence | Tag |
|---|---|---|
| Used DDR4 32GB RDIMM | $100–150 realized, 12 months to Aug-2026, +335% YoY ([amcompute](https://www.amcompute.com/appraisals/ddr4-32gb-rdimm)) | [REPORTED] |
| Used DDR4 64GB RDIMM | $250–370, +285% YoY ([amcompute](https://www.amcompute.com/appraisals/ddr4-64gb-rdimm)). 64GB LRDIMM is only $100–170 | [REPORTED] |
| Used DDR4 8/16/128GB | $22–28 / $47–60 / $260–370 ([amcompute](https://www.amcompute.com/appraisals/memory)) | [REPORTED] |
| Used DDR5 64GB RDIMM | $890–1,200, +310% YoY ([amcompute](https://www.amcompute.com/appraisals/ddr5-64gb-rdimm)). One used sale hit $1,798 in Apr-2026 ([eBay](https://www.ebay.com/itm/198212795656)). The model check puts used at **63% of the new $25.78/GB** contract deck | [REPORTED] / model |
| New DDR5 ECC RDIMM retail | $29.56–39.06/GB, median $35.70 (2026-08-14) ([Capital & Compute](https://capitalandcompute.net/memory-prices/server/)). ChinaFlashMarket 64GB was $1,630 on 2026-09-08 | [REPORTED] |
| Lot listings (buy-side proxy) | 24×32GB Hynix lot listed at $3,359.52, about $140/module, which is ≈ resale ([PCSP](https://pcserverandparts.com/lot-of-24-hynix-32gb-768gb-total-pc4-2666v-r-2rx4-ddr4-ecc-reg-rdimm-hma84gr7cjr4n-vk/)). An undated lot of 6×32GB at $18 each is probably stale ([UBB Central](https://ubbcentral.com/store/item/Lot-of-6-Micron-32GB-2Rx4-PC4-2400T-RB2-11-Server-Memory-ECC-RDIMM-DDR4-288-pin_276559352415.html)) | [REPORTED] |
| ITAD buy price | **No published ITAD lot price found.** Iron Mountain ALM nearly doubled on volume and pricing (01_LANDSCAPE), so incumbents keep the spread | **Gap: the binding input** |

### 3.2 Cost stack per module (model §1a; buy at 65% of realized resale)

| Deck | eBay | B2B | Mixed (m12) |
|---|---|---|---|
| Today | $36 (13%) | $38 (16%) | **$37 (15%)** on a $253 average price |
| GLUT ×0.40 | $7 (7%) | $10 (11%) | $9 (9%) |
| SEVERE ×0.10 | −$3 (−6%) | $0 (1%) | −$1 (−2%) |

- **By SKU (today):** 32GB DDR4 earns $12 (10%), 64GB DDR4 earns $43 (15%), and 64GB DDR5 earns $167 (17%), but ties up $679 of cash per unit.
- **Breakeven buy fraction: 78% of realized resale.** Above that there is no contribution at today's prices (model §6a). At 70% the founder's full-time start slips from m14 to m21. At 75% it slips to m33, and ARR at m36 drops from $446k to $250k (model §5).
- **Inventory lag:** buying at today's price and selling one GLUT month later still earns $25 (11%) per module. The damage in a glut comes from shrinking volume and margin, not from a one-month price drop.
- **Fees:** the eBay final-value fee for RAM is 13.6% + $0.30–0.40 per order ([LitCommerce](https://litcommerce.com/ebay-fee-calculator/)) or 10.9% ([EcomCalcTools](https://ecomcalctools.com/blog/fees-ebay/ebay-computers-fees/)). These conflict, so the model uses 13.6%. B2B pays about 3% in processing.
- **Test equipment:**
  - **Used** Gen10 DDR4 servers as burn-in beds, running memtest86+ (GPLv2, last commit 2026-10-28) and stressapptest (Apache-2.0), both [VERIFIED in Phase 2 by clone].
  - Innoventions RAMCHECK LX DDR4 is $2,495 and DDR4 Pro $3,850 (undated forum post, [TechPowerUp](https://techpowerup.com/forums/posts/3849792)). The $13–41 "DDR5 testers" on Walmart and Newegg are slot checkers, not testers.
  - No CST price was found.
  - Capex: $4.2k in month 1 and $4k for a DDR5 bed in month 6 [ESTIMATE].
- **Labor:** 12 minutes per module covering receive, SPD log, burn-in load/unload, label, list and pack [ESTIMATE]. A founder working 35 h/month handles about 175 modules; above that a technician costs $25/h.
- **Returns and warranty:** the model assumes 2% returns and 3% test fallout (C_notes). Channel warranties run from 90 days to 1 year ([Reboot IT](https://reboot-it.com.au/products/samsung-16gb-1x16gb-pc3-12800r-1600-ddr-rdimm-server-memory-3mth-wty-129778)) up to lifetime replacement ([Rimlance/Newegg](https://www.newegg.com/rimlance-64gb/p/1X5-00FS-00788)). Some sellers charge a 20% restocking fee on non-defective returns ([PCSP](https://pcserverandparts.com/16gb-pc4-ddr4-2666v-r-1rx4-memory-m393a2k40bb2-ctd6q-samsung-refurbished/)).
- **Channels (named):**
  - eBay.
  - Refurbishers and B2B buyers: xByte Technologies (WV; lists DDR5 RDIMMs, [xByte](https://www.xbyte.com/products/cat-29137)), TechMikeNY (Bronx), PC Server & Parts, UBB Central, ServerMonkey, Memory4Less.
  - TPM spares desks: Park Place Technologies, Service Express, Curvature.
  - Marketplace: Mobius Materials.
  - Several of these also compete as sellers.
- **Working capital is the binding constraint.** The operator buys down to a $5k reserve, so cash sits at the reserve in months 7–10. Recert volume is capital-limited to about 390 modules a month by month 12 (~$71k of lots a month).

### 3.3 Optane PMem (C-26 SKU)
- **Price evidence** [REPORTED, all undated or stale]:
  - New 128GB PMem 200 at about US$290 ([eBay.de](https://www.ebay.de/itm/204762258263)).
  - 256GB open-box at $999 ([eBay](https://www.ebay.com/itm/356158359970)).
  - Uvation lists 128GB at $997 and 256GB at $4,093 (2024 pages).
  - Dasenic 128GB at $781 for 50+.
  - 2019 launch was $695/128GB.
  - **No sold-volume data was found** (gap).
- **Model** [ESTIMATE]: $200 resale for 128GB, 55% buy, 25 units a month. Contribution is $46 per unit (23%) today, 14% in GLUT and −34% in SEVERE. Volume falls to 40% after vSphere 8 end of general support on 2027-10-11. It is a small SKU worth keeping only while it lasts.

---

## 4. Question 4: DIMM-health subscription

- **Incumbents already predict DIMM failures:**
  - **Lenovo AI-based Memory Predictive Failure Analysis (MPFA)** ingests DIMM error telemetry in real time to predict cell and row faults ([Lenovo Press LP2326](https://lenovopress.lenovo.com/lp2326)).
  - **Intel Memory Failure Prediction (MFP)** is vendor-agnostic ML on DIMM, bank, row and cell errors, built into AMI Aptio/MegaRAC and Insyde BIOS/BMC firmware. Intel claims a 5× gain in DIMM-level prediction at Tencent and up to 40% fewer server hardware failures at Meituan ([Intel/Tencent](https://www.intel.co.uk/content/dam/www/central-libraries/us/en/documents/2023-12/intel-memory-failure-prediction-at-tencent.pdf); [Intel/Meituan](https://www.intel.com/content/dam/www/central-libraries/us/en/documents/2023-12/intel-memory-failure-prediction-improves-reliability-meituan.pdf); [AMI](https://salestechstar.com/privacy-and-regulations/ami-announces-support-for-intel-memory-failure-prediction-capabilities-in-aptio-v-uefi-firmware-and-megarac-bmc-firmware/)).
  - **Park Place ParkView** has bundled predictive detection with auto-ticketing into TPM since 2017 (C-85 verify).
  - All [REPORTED].
- **What TPMs charge:** no per-server list price is published. Vendors say TPM runs **30–70% below OEM** post-warranty pricing ([Park Place](https://www.parkplacetechnologies.com/blog/oem-support-vs-third-party-maintenance/)) [REPORTED, vendor].
- **Failure base rate:** about 8% of DIMMs see errors each year ([Google, SIGMETRICS 2009](https://research.google/pubs/dram-errors-in-the-wild-a-large-scale-field-study/)). The 1.5%/DIMM-year replacement rate is the C-85 card's estimate; no 2023–26 fleet study was found.
- **Unit economics** (model §1d; 1,200 DIMMs at $0.60/DIMM-month = $8,640/yr):

| Deck | GM with spares from recert | GM standalone | Fee vs DIY sparing |
|---|---|---|---|
| Today | 64% | 54% | **4.5×** |
| GLUT | 78% | 73% | 8.5× |

  - Margin rises in a glut, but the buyer's reason to pay disappears.
  - Standalone, the line ends 36 months at −$26k cumulative EBITDA (model §4).
- **Willingness to pay:** untested. Prediction is free from OEM and BMC firmware, and a 100-server fleet can self-spare for about $1.9k/yr.
- **Verdict:** **do not run as a product line.** Offer TPMs and regional MSPs *tested recovered spares plus a CE-trend data feed* wholesale, from recert stock. Revenue then lands in the recert line at better-than-eBay margins.

---

## 5. Question 5: Counterfeit and legal exposure, and certifications

| Rule / standard | What it means here | Action | Cost / time |
|---|---|---|---|
| DFARS 252.246-7007 / -7008 | Contractors need a counterfeit detection and avoidance system and must buy from OCMs or authorized channels, or else from contractor-approved suppliers with testing and traceability [UNVERIFIED-training; 01_LANDSCAPE §7.3]. **Recovered DIMMs effectively cannot go into DoD deliverables** | Never sell recert modules into DoD deliverables. CleanBOM *evidence* is sold as information, not parts | $0 |
| FAR 52.246-26 (reporting nonconforming items) | Used-as-new counterfeits get reported to GIDEP (C-62/C-85 scorers) | Label every module "used/recertified" with its serial and test record | $0 |
| 18 U.S.C. §2320; Champion Spark Plug (1947) | Remarking, or selling used as new, is counterfeiting. Reconditioned goods may keep their marks only if clearly labeled (C_notes §6) | Disclosure language in listings; never relabel or reprogram SPD | $2.5k legal setup |
| SAE AS6081 (distributors) | Expected by A&D buyers of open-market parts. NQA claims to be the only certification body ([NQA](https://www.nqa.com/certification/standards/as6081)) | Get it only if a distributor or prime customer requires it | No price found. AS9120 proxy is $6–12k for small distributors ([Amtivo](https://amtivo.com/us/resources/insights/aerospace-certification-cost/)); 3–6 months [ESTIMATE] |
| SAE AS6171 (test labs) | X-ray and decap methods; ANAB lists 26 accredited labs | Outsource. Never claim AS6171 in-house | Per sample ($400 model) |
| R2v3 (SERI) | ITAD suppliers do downstream due diligence. Buying *tested, working* modules for reuse should not require R2. Taking untested or scrap board lots (Focus Materials) would [UNVERIFIED-training] | Buy tested/working lots only; get the ITAD's downstream questionnaire in writing | If needed: $2,000/facility/yr license plus CB audit; CBs book 4+ months out ([SERI](https://sustainableelectronics.org/wp-content/uploads/2021/03/Steps-to-Getting-Certified-2021.03.pdf)) |
| ISO 9001 | Credibility for B2B TPM/OEM buyers and the base for AS6081 | Month 15 in the model | $10k + $3k surveillance [ESTIMATE] |
| Attestation liability (FCA-adjacent) | A wrong "no CXMT" attestation that a contractor relies on could pull the vendor into False Claims Act litigation [UNVERIFIED-training] | Sell an "evidence-based assessment" with stated confidence and sample basis, not a certification. Cap liability. Carry E&O ($400/mo in the model) | $6k legal before launch |

**Export controls:** memory modules are EAR99 for commercial resale (01_LANDSCAPE §8). Screen buyers for prohibited end uses.

---

## 6. Question 6: Glut behavior of each line (model §1 and §7)

| Line | Today GM | GLUT GM | SEVERE GM | Demand in a glut | Verdict |
|---|---|---|---|---|---|
| Recert RDIMM | 15% | 9% steady state (volume cap falls to ~50%) | −2% | Falls: new DDR5 becomes the cheap upgrade | **Dies as a profit line in 2028.** It must have funded the founder's time and the library by then |
| PMem SKU | 23% | 14% | −34% | Dies on 2027-10-11 (VMware) regardless | Harvest until Oct-2027 |
| CleanBOM-5949 | 80% | 80% | 80% | Statutory. A glut raises CXMT share, which arguably raises demand (not credited) | **Glut-proof.** This is the company |
| DIMM-health | 64% | 78% | 81% | Churn rises (3.5%/mo) as refresh gets cheap | Margin up, base shrinks. Make it a wholesale add-on |

**Scenario results (bundle; model §3):**

| | BASE | GLUT | SEVERE |
|---|---|---|---|
| Blended GM, 36 months | 25% | 30% | 36% |
| Recert+PMem GM | 15% | 13% | 13% |
| CleanBOM GM | 81% | 81% | 81% |
| DIMM-health GM | 68% | 76% | 79% |
| Breakeven, founder unpaid | m3 (Jan-27) | m3 | m3 |
| **Breakeven charging a $10k/mo founder salary** | **m11 (Sep-27)** | m11 | m11 |
| Founder goes full-time | m14 (Dec-27) | m14 | m14 |
| Cash low | $5,000 reserve floor @m10 (working capital, not losses) | same | same |
| ARR (recurring) m12 / m18 / m24 / m36 | $25k / **$140k** / $254k / **$446k** | $25k / **$139k** / $251k / **$434k** | $25k / **$139k** / $251k / **$434k** |
| Total run-rate m18 / m36 | $1.88M / $1.75M | $1.44M / $0.89M | $1.20M / $0.54M |
| Cash at m36 (+ inventory) | $610k (+$71k) | $392k (+$21k) | $328k (+$1k) |
| Recert share of cumulative revenue | 85% | 75% | 67% |

---

## 7. Question 7: First ten customers (names, and where to find them)

| # | Customer | Line | Why them | How to reach |
|---|---|---|---|---|
| 1 | **AddOn Networks** (Irvine CA; OEM-compatible DDR5 RDIMMs sold via resellers) | CleanBOM high tier | Must certify die source upstream of SEWP/GSA resellers | Federal channel team; LinkedIn "government sales"; reseller listings ([LTT Partners](https://www.lttpartners.com/products/addon-cisco-reg-ucsx-mrx64g2re5-64gb-ddr5-6400mhz-registered-dual-rank-x4-1-1v-288-pin-rdimm)) |
| 2 | **Axiom Memory Solutions** (OEM-compatible memory; TPM/upgrade channel) | CleanBOM high tier | Same exposure | axiomupgrades.com; GSA Advantage listings |
| 3 | **Brute Networks** (OEM-compatible server memory) | CleanBOM high tier | Same | Newegg Business / GSA listings |
| 4 | **SHI International, public sector** (sells RDIMMs and Optane PMem to public buyers) | CleanBOM evidence packs / low tier | Reseller certifying compatible and odd-lot SKUs | SHI public-sector supplier-compliance team; SEWP V contract holder list |
| 5 | **A small SEWP V / GSA MAS IT holder that resells refurbished servers** (several dozen exist [UNVERIFIED-training]) | CleanBOM low tier + recert supply | Refurb gear has unknown die content and the holder must certify | SEWP V holder list (sewp.nasa.gov); GSA eLibrary SIN 33411 |
| 6 | **xByte Technologies** (WV refurbished Dell servers, DDR5 RDIMMs) | Recert B2B buyer | East Coast, volume buyer of tested modules | Purchasing desk |
| 7 | **TechMikeNY** (Bronx NY refurb servers) | Recert B2B buyer | East Coast; local pickup cuts shipping | Direct |
| 8 | **PC Server & Parts** (refurb parts; lists 24-module lots) | Recert B2B buyer | Buys and sells lots, so it is a price-discovery partner | Direct |
| 9 | **Park Place Technologies / Curvature** (TPM spares) | Wholesale spares + CE feed (the demoted C-85) | Needs tested DDR4 spares for out-of-warranty fleets | Supply-chain/spares procurement |
| 10 | **Z2Data or Accuris/SiliconExpert** (compliance data; Z2Data markets 1260H screening) | Die-source dataset license | Its data stops at the component; ours reaches the die inside the module | BD / data partnerships; Accuris's switching program shows appetite for share |

**Alternates:**
- White-box federal server builders on GSA/SEWP [UNVERIFIED-training].
- Northeast university research-computing centers, as wholesale spares buyers.
- Mobius Materials (channel partner for graded memory).
- OBSIDIA (die-level partner or acquirer).

---

## 8. Regulatory and funding facts that matter
- §5949 takes effect 2027-12-23 (month 14). The FAR rule is still proposed; there is no final rule and no DFARS counterpart (§1.1).
- §805's indirect DoD ban starts 2027-06-30, but CXMT's §1260H status is contradictory and the component exception may cover COTS memory (§1.1).
- **SBIR/STTR** is reauthorized through 2031-09-30. The founder cannot be SBIR PI while keeping the day job. STTR with a university PI works (01_LANDSCAPE §7.1).
  - The natural East Coast STTR partner is **UMD CALCE**, the counterfeit-electronics group behind the AS6171 briefing ([ANSI/CALCE](https://share.ansi.org/Shared%20Documents/Standards%20Activities/Microelectronics%20Supply%20Chain%20Security/October%2026-28,%202022%20Workshop/30%20September%202022%20Standards%20Briefings/AS6171%20Overview%20for%20ANSI%20Meeting_Azarian_30Sep2022.pdf)).
  - DoD counterfeit and supply-chain-illumination topics recur [UNVERIFIED-training]. I did not check whether any specific topic is open (gap). STTR is non-dilutive funding, not revenue, and is not in the model.
- CHIPS money is $0 for this concept. OBSIDIA's $34M LOI marks the funded competitor and possible acquirer (01_LANDSCAPE §7.1).

---

## 9. The kill experiment (<$10k, <30 days, run in parallel)

| Track | Spend | What to do | Kill line (from the model) |
|---|---|---|---|
| **A. Buy side** (the cash engine) | ~$5,000, mostly recovered by resale | Get lot quotes from 3 ITADs: Iron Mountain/ITRenew (Sesame), Sims Lifecycle, and one regional R2 ITAD in NJ, PA or MD. Buy one mixed DDR4 RDIMM lot of ~35–40 modules. Test on one used Gen10 server with memtest86+ and stressapptest. Log SPD module and die bytes and serials. Sell half on eBay and half to xByte, TechMikeNY or PCSP | **Kill recert if the buy price exceeds 75% of realized resale, or if measured contribution is below 8%.** Breakeven is 78%. At 75% the founder's full-time start slips to m33 and m36 ARR falls from $446k to $250k |
| **B. Evidence** (the library) | ~$2,000 | Send 4 modules to an ANAB-accredited AS6171 lab (SMT Corp, Integra or an ERAI-member lab) for X-ray plus decap die-marking: 2 from the lot, 1 CXMT-die module (e.g., KingBank/Lexar CXMT kit or a CXMT RDIMM), and 1 third-party "compatible" RDIMM (AddOn/Axiom/Brute) bought on eBay. Compare die marks with the SPD bytes 350–351 / 552–553 | **Kill the lab-backed library if cost exceeds $600/sample, turnaround exceeds 15 business days, or die source cannot be identified.** A mismatch between SPD and die on the compatible module would be the single best sales asset |
| **C. Demand** (the company) | ~$1,000 for data, travel and a one-page sample report | Hold 15 conversations: 5 compatible-memory makers (AddOn, Axiom, Brute + 2), 5 GSA/SEWP resellers (incl. SHI public sector), 5 integrators or white-box builders. Show a sample evidence pack. Ask for a paid pilot at $750–2,500/mo or a $900 pack | **Kill CleanBOM if fewer than 3 of 15 sign an LOI or buy a paid pack.** The model needs about 10 subscribers by m18, which means a 25% close at 5 conversations/mo, or 12 conversations/mo at 10% |
| **D. DIMM-health** | $0 | Ask Park Place and Service Express spares desks whether they buy tested spares plus a CE-trend feed wholesale | Drop the C-85 line entirely if both say no |

**Decision rule:**
- A passes, C fails: run recert as a cash harvest through end-2027 and do not build CleanBOM.
- C passes, A fails: run CleanBOM standalone, which needs about $47k including buffer (model §4: cash dips to −$6.5k at m15 on $40k).
- Both pass: run the sequenced bundle.
- Both fail: kill DD1.

**Total:** about $8k gross and about $3k net after resale.

---

## 10. Open gaps (ranked by decision weight)
1. **Willingness to pay under the safe harbor.** No customer has been asked; this is kill track C.
2. **ITAD lot buy fraction.** No published price exists; this is kill track A. The model's 0.65 is the most important unverified input in the recert line.
3. **Final FAR rule text and date; any DFARS counterpart; CXMT/YMTC §1260H status and the scope of §805's component exception.** These three determine the 2027 demand calendar.
4. **Lab die-ID price and turnaround** at named U.S. labs (SMT Corp, Integra, Micross, ERAI members). Only weak blog ranges were found.
5. **SMB pricing at Z2Data, Assent, Sourcemap and Exiger,** to see whether any of them already sells a CXMT/die-source flag cheaply.
6. **Documented CXMT-die-in-server-RDIMM relabeling in the U.S. channel.** None was found; all fraud evidence so far is consumer-channel.
7. **Current (Oct-2026) used prices and eBay sold volumes.** amcompute data ends Aug-2026, and there is no PMem volume data.
8. **eBay RAM fee** (13.6% vs 10.9%); the R2v3 downstream rule for tested reuse modules; DIMM replacement rates in 2024–26 DDR4 fleets.
9. **Channel absorption.** The model caps recert at 400 modules/month part-time and 600 full-time (×0.5 at glut prices). That means sourcing about $70–100k a month of lots, which has not been tested.
