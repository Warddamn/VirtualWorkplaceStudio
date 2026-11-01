# DD1 — Provenance & Recertified Memory (`provenance-recert`)

**Author:** `p4w-provenance-recert` · **As of:** 2026-11-01 · **Model:** `models/provenance-recert.py` (re-run 2026-11-01, exit 0; output identical to `research/phase4/provenance-recert_model_output.md`) · **Notes:** `research/phase4/provenance-recert_notes.md` · **Judgment calls:** `research/assumptions/p4w-provenance-recert.md`

**How to read the citations.**
- **m§N** = section N of the model's printed output.
- **INPUTS** = the model's INPUTS dict, where each input carries its own source.
- **§2.6 variants** = re-runs of the same model, with the command given there.

All external facts are search-snippet grade, so nothing is [VERIFIED] except the open-source tools that Phase 2 cloned.

---

## 0. Header

**Name:** Provenance & Recertified Memory. Trading names: "ProvenRAM" for recert, "CleanBOM-5949" for the subscription.

**Pitch:** Buy, test and resell decommissioned server memory while the shortage pays. Use every module that crosses the bench to build a module-to-die-source library. Then sell federal IT suppliers a subscription that shows whether CXMT/YMTC DRAM is inside the memory they must certify under NDAA §5949 from 2027-12-23.

**Anchor and folded concepts.** Quotes are verbatim from `research/phase3/scores_raw/*.json`.

| Role | ID | Concept | Why it is in the bundle |
|---|---|---|---|
| Anchor | **C-64** | CleanBOM-5949 provenance verification | VC: "The best-shaped business in my batch (T0, ~70% GM, glut-proof, founder-fit), but … it is a feature for Exiger or SiliconExpert unless it owns die-source data." Recert is how it gets die-source data. |
| Folded | C-62 | ProvenRAM recovered RDIMMs | Veteran: "run it as a cash cow or a provenance-data feeder, not a venture." |
| Folded | C-26 | Optane PMem salvage | VC: "fine as a C-62 SKU, uninvestable on its own." |
| Folded | C-85 | DIMM-health + spares | Founder: "Sell it wholesale to TPMs or not at all." |

**Capital tier: T0.** It starts on $40k of the founder's money (INPUTS `start_cash`; ASSUMPTIONS A-03). CleanBOM on its own would need about $47k: its cash dips to −$6,529 at m15 (m§4).

**Scores and ranks** (`scores.csv`, 40 concepts scored):

| ID | Default | Capital-constrained | Moonshot |
|---|---|---|---|
| C-64 | 78.0 (#6) | 81.7 (#6) | 76.7 (#3) |
| C-26 | 74.0 (#9) | 78.3 (#7) | 66.7 (#12) |
| C-85 | 74.0 (#11) | 77.5 (#10) | 71.7 (#10) |
| C-62 | 71.0 (#14) | 75.0 (#11) | 64.2 (#16) |

**The honest summary: a small cash business, not a venture.**
- **BASE result:** $445,543 ARR at m36, $610,097 cash, and $662,971 of cumulative EBITDA on $40k (m§3).
- **Where the money comes from:** 85% of revenue is a moatless 15%-margin resale trade that dies in a glut.
- **The glut-proof part is small:** CleanBOM reaches 23.5 subscribers. $1M ARR would need ~61 (m§6f).
- **Its close rate, churn and price are all guesses,** and the proposed FAR rule lets sellers self-certify for free.
- **Recert's buy price is unverified:** at 75% of resale instead of 65%, ARR at m36 falls to $250,221 (m§5).

**POSSIBLE? — Yes.** Recert is an existing TRL-9 trade on free tools, and AS6171 die-ID is routine at 26 accredited labs. But the module assembler writes the SPD die bytes, so a scan proves nothing on its own. Only a lab-built cross-reference does.

**PROFITABLE? — Marginal.** It makes money in BASE, GLUT and SEVERE, but only at lifestyle scale ($434–446k ARR at m36). The cash engine is a 15% margin on an unverified buy price, and the subscription needs willingness to pay that nobody has tested against a free self-certification option.

**DOABLE BY THIS FOUNDER? — Yes.** T0, startable part-time, and the software and operations work fits their background. The limits are working capital (cash at or near the $5k reserve in m6–m10; m§2) and a federal sales motion they have never run.

---

## 1. How it works

Every server holds memory sticks called RDIMMs: a row of DRAM chips plus a tiny label chip called the SPD. When data centers retire servers, IT asset disposition firms (ITADs) such as Iron Mountain and Sims Lifecycle pull the sticks and sell them in lots. Contract DRAM prices have roughly quadrupled since late 2025 (01_LANDSCAPE §5.1). A used 32GB DDR4 stick now realizes $100–150, and a used 64GB DDR5 stick $890–1,200 ([amcompute, 2026-08](https://www.amcompute.com/appraisals/ddr4-32gb-rdimm); [amcompute](https://www.amcompute.com/appraisals/ddr5-64gb-rdimm)) [REPORTED].

**Line 1: recert, the cash engine.**
1. Buy lots.
2. Burn in each stick for hours in a used server with free software (memtest86+, Google's stressapptest).
3. Log its SPD data and apply a serial label and test record.
4. Sell good sticks on eBay and to refurbishers and maintenance firms, labeled "used/recertified."

Optane PMem rides along as one extra SKU.

**Line 2: the library, the asset.** The SPD says who made the DRAM chips, but the module assembler writes that field, and anyone can rewrite it ([Evetech](https://evezone.evetech.co.za/build-lab/spot-fake-relabelled-ram-used-market)) [REPORTED]. Real proof is physical: an accredited lab X-rays the chip, dissolves the package and photographs the die markings (SAE AS6171).
- The bench sends three sticks a month to such a lab.
- One result identifies the die source for every stick sharing that part number and date-code family.
- Over time this builds a cross-reference ("part X, date codes Y–Z = Samsung die; part W = CXMT die") that nobody holds at module level.

**Line 3: CleanBOM-5949, the company.** From 2027-12-23, federal agencies may not buy products containing SMIC, CXMT or YMTC chips. Sellers must certify after a "reasonable inquiry" ([Federal Register, 2026-02-17](https://www.federalregister.gov/documents/2026/02/17/2026-03065/federal-acquisition-regulation-prohibition-on-certain-semiconductor-products-and-services)) [REPORTED]. The firms that write the *first* certification need to know what is inside the module: third-party "OEM-compatible" memory makers and white-box server builders.
- **What CleanBOM sells them:** a subscription ($750 or $2,500 a month), per-SKU evidence packs ($900), and lab die-checks at cost × 1.6.
- **How it is framed:** an evidence-based assessment, never a legal certification.

**Line 4: the spares feed (DIMM-health, demoted).** Tested spares plus a corrected-error trend feed, sold wholesale to third-party maintenance (TPM) firms.

```
 ITAD lots --buy ~65% of resale--> [ Bench: burn-in, SPD log, serial ]
                                        |                   |
                              good sticks             3 lab decaps/month + SPD records
                                        v                   v
                          eBay + B2B (~15% margin)    Die-source library
                                        |                   |
                                        +--> cash buys ---> CleanBOM-5949 subscriptions
                                             founder time   (~80% GM, demand set by statute)
```

The logic is timing: recert pays **now** and fades in the 2028 glut; CleanBOM's demand switches **on** in 2027 and ignores DRAM prices. Recert must fund the founder's time and the library before it dies.

---

## 2. Cost and unit-economics model

### 2.1 Unit economics

| Line (per unit) | Today | GLUT (DDR5 −60%) | SEVERE (−90%) | Source |
|---|---|---|---|---|
| Recert RDIMM, mixed channel (60% 32GB DDR4 / 30% 64GB DDR4 / 10% 64GB DDR5) | $253 → **$37 (15%)**. Buy+fallout $183, fees+ship $22, returns+labor $11 | $101 → $9 (9%) | $45 → −$1 (−2%) | m§1a |
| … eBay only / B2B only | $36 (13%) / $38 (16%) | $7 / $10 | −$3 / $0 | m§1a |
| … by SKU, today | 32GB DDR4 $12 (10%); 64GB DDR4 $43 (15%); 64GB DDR5 $167 (17%), but ties up $679 of cash per unit | — | — | m§1a |
| Optane PMem 128GB | $200 → $46 (23%) | $11 (14%) | −$7 (−34%) | m§1b |
| CleanBOM, per subscriber-month (ARPA $1,362 + $256 lab pass-through) | **$1,295 GP (80%)**; a $900 pack earns ~88% | same | same | m§1c |
| DIMM-health, per 1,200-DIMM customer-year | $8,640 revenue, 64% GM, priced at **4.5×** the buyer's DIY spares cost | 78%, 8.5× | 81%, 10.8× | m§1d |

- **Inventory lag:** selling a month into the glut still earns $25 (11%) per module (m§1a). The damage comes from volume and margin over time.
- **CleanBOM CAC:** $2,550 at a 10% close (m§1e). Its "25× LTV/CAC" rests on untested inputs; do not quote it.

### 2.2 Scenario summary (bundle, all four lines; m§3, m§4)

| | BASE | GLUT | SEVERE |
|---|---|---|---|
| ARR (recurring) m12 / m18 / m24 / m36 | $25,334 / **$139,995** / $253,948 / **$445,543** | $25,334 / $139,232 / $250,679 / $434,012 | same as GLUT |
| Total run-rate m18 / m36 | $1.88M / $1.75M | $1.44M / $0.89M | $1.20M / $0.54M |
| Breakeven, founder unpaid | m3 (Jan-27) | m3 | m3 |
| Breakeven with a $10k/month founder salary | **m11 (Sep-27)** | m11 | m11 |
| Founder goes full-time | m14 (Dec-27) | m14 | m14 |
| Cash low point | **$5,000 at m10** (inventory reserve floor; working capital, not losses) | same | same |
| Cash at m36 (+ inventory) | $610,097 (+$70,850) | $392,118 (+$21,256) | $328,128 (+$953) |
| Cumulative EBITDA | $662,971 | $389,580 | $303,874 |
| Gross margin: blended / recert+PMem / CleanBOM | 25% / 15% / 81% | 30% / 13% / 81% | 36% / 13% / 81% |
| Recert share of cumulative revenue | 85% of $4.14M | 75% of $2.55M | 67% of $1.89M |

### 2.3 Is the whole better than the parts? (BASE, m§4)

| Configuration | ARR m36 | Cash m36 | Cumulative EBITDA |
|---|---|---|---|
| Full bundle | $445,543 | $610,097 | $662,971 |
| Recert + CleanBOM | $384,530 | $580,439 | $619,489 |
| Bundle without the library's close-rate lift (7% vs 10%) | $323,558 | $461,433 | $513,988 |
| Bundle, founder never full-time | $199,038 | $480,218 | $501,841 |
| CleanBOM standalone | $120,296 | $91,351 | $52,851 |
| Recert + PMem only | $0 | $169,467 | $208,516 |
| DIMM-health standalone | $27,187 | $583 | −$26,165 |

**Reading the table:**
- **The real synergy is recert cash buying founder time,** worth ~$247k of the ARR.
- **The library is worth ~$122k,** and that rests on an unmeasured 3-point lift in close rate.
- **DIMM-health adds ~$61k** and loses money on its own.

### 2.4 Sensitivity (BASE, one input at a time; m§5)

| Input moved | ARR m18 | ARR m36 | Cash m36 | Cash low |
|---|---|---|---|---|
| Base case | $139,995 | $445,543 | $610,097 | $5,000 |
| Recert resale −30% | $76,629 | $381,840 | $366,995 | $5,000 |
| Subscription price −30% | $97,997 | $311,880 | $461,565 | $5,000 |
| Close rate −30% | $97,997 | $311,880 | $473,893 | $5,000 |
| **COGS +30%** | $76,629 | $199,038 | $125,914 | **−$12,172** (needs more than $40k; breakeven m16) |
| Final FAR rule slips 6 months | $35,990 | $372,904 | $458,278 | $6,101 |
| **ITAD buy fraction 0.75** | $76,629 | **$250,221** | $163,673 | $6,469 |
| ITAD buy fraction 0.55 | $183,332 | $475,880 | $1,047,669 | $21,650 |

The buy fraction (what an ITAD charges for a lot, as a share of resale) is the most important input. It has **no published source** (notes §3.1).

### 2.5 What must be true (m§6)

1. **Lots cost under 78% of realized resale.** Above that, recert contributes nothing.
2. **Recert sells 364 good modules a month** to cover a $10k founder salary plus ~$3,450 of fixed opex. That needs ~$64,624 of inventory cash each month, and it only lasts until the 2028 turn.
3. **CleanBOM has ~10 paying subscribers by the turn (m15–18).** The model reaches **7.5 at m18**. Hitting 10 needs a 25% close at 5 conversations a month, or 12 conversations a month at 10%.
4. **$1M ARR needs ~61 subscribers.** The model reaches 23.5.

### 2.6 Variant runs (stress combinations the model does not print)

| Variant | Scenario | Founder full-time | ARR m36 | Cash m36 |
|---|---|---|---|---|
| Turn arrives early (Oct-27, `turn_month=12`) | GLUT | m31 | $268,513 | $273,766 |
| Turn arrives early (Oct-27) | SEVERE | m34 | $232,342 | $247,443 |
| Buy fraction 0.75 | GLUT | m34 | $232,377 | $166,962 |
| CleanBOM sells nothing (`cb_close_bundle=0, cb_close_standalone=0, cb_pack_rate=0`) | GLUT | never | $21,868 | $127,548 |
| FAR rule slips 6 months (`_cb_delay=6`) | GLUT | m14; back at the day job by Feb-28 | $203,455 | $237,161 |
| FAR slip + close −30% (`_close_mult=0.7`) | GLUT | m14; 2 months only | $115,358 | $222,394 |

Reproduce from the repo root, swapping the parameters per row:

```
python3 -c "import importlib.util as u,sys;sys.path.insert(0,'models');s=u.spec_from_file_location('pr','models/provenance-recert.py');pr=u.module_from_spec(s);s.loader.exec_module(pr);print(pr.metrics(pr.simulate('GLUT',dict(pr.P0,turn_month=12))))"
```

### 2.7 The honest read

**Generous in three places:** the unsourced buy fraction, while Iron Mountain's ALM revenue rose 88% YoY in Q2-26 as it kept the repricing ([MarketBeat, 2026-08-08](https://www.marketbeat.com/instant-alerts/iron-mountain-q2-earnings-call-highlights-2026-08-08/)) [REPORTED]; channel absorption of ~$70–100k of lots a month (m§2, "Inv buy"), never tested; and CleanBOM's close rate and churn. **Harsh in one:** no extra CleanBOM demand in a glut.

The result holds across all three price decks only because the founder goes full-time one month before the modeled turn. If the glut comes a quarter early, or the FAR rule slips, ARR at m36 roughly halves (§2.6).

---

## 3. Target customer and the first ten customers

**Who pays for CleanBOM.** The safe harbor moves liability upstream: whoever writes the first certification has to know the die source ([Mayer Brown, 2026-03-03](https://www.mayerbrown.com/en/insights/publications/2026/03/far-council-proposes-rule-to-prohibit-acquisition-of-semiconductors-from-china-and-countries-of-concern)) [REPORTED]. So the core buyer is the third-party "OEM-compatible" memory maker selling into federal channels, where CXMT is now the marginal open-market supplier. A U.S. reseller already markets a CXMT-made 64GB DDR5 RDIMM as compatible with Dell PowerEdge 16G and HPE Gen11 ([router-switch.com](https://www.router-switch.com/sw/faq/cxmt-ddr5-server-memory-cxmr4e464r8as-cb1c-dell-hpe-sizing.html)) [REPORTED, vendor claim].

**Who pays for recert:** refurbishers and TPM spares desks.

| # | Customer | Line | Why they buy | How to reach them |
|---|---|---|---|---|
| 1 | **AddOn Networks** (Irvine CA), OEM-compatible DDR5 RDIMMs sold through resellers ([LTT Partners](https://www.lttpartners.com/products/addon-cisco-reg-ucsx-mrx64g2re5-64gb-ddr5-6400mhz-registered-dual-rank-x4-1-1v-288-pin-rdimm)) | CleanBOM $2,500 | SEWP/GSA resellers rely on its certification; a wrong one carries False Claims Act-adjacent exposure | Federal channel team via LinkedIn; reseller listings |
| 2 | **Axiom Memory Solutions**, OEM-compatible memory sold into the TPM channel ([Axiom](https://www.axiomupgrades.com/inside-the-stack-detail/Third-party-maintenance-How-can-it-help-your-business-)) | CleanBOM $2,500 | Same | GSA Advantage listings; compliance contact |
| 3 | **Brute Networks**, OEM-compatible server memory ([Newegg](https://www.newegg.com/Brute-Networks-Server-Memory/BrandSubCat/ID-161080-541/Page-42)) | CleanBOM $2,500 | Same | Newegg Business / GSA listings |
| 4 | **SHI International public sector**, which sells RDIMMs and PMem to public buyers ([SHI](https://www.publicsector.shidirect.com/product/47547768/64GB-2RX4-DDR4-3200-ECC-RDIMM)) | $900 packs → $750 tier | Odd-lot, refurb and "compatible" SKUs carry no OEM certification | Supplier-compliance team; SEWP V holder list |
| 5 | **A small SEWP V / GSA MAS holder reselling refurbished servers** (type) | $750 tier + recert supply | Must certify refurb gear of unknown die content | sewp.nasa.gov holder list; GSA eLibrary |
| 6 | **xByte Technologies** (WV), refurbished Dell servers ([xByte](https://www.xbyte.com/products/cat-29137)) | Recert B2B | East Coast volume buyer | Purchasing desk |
| 7 | **TechMikeNY** (Bronx NY), refurbished servers | Recert B2B | Local pickup saves shipping | In person |
| 8 | **PC Server & Parts**, trades 24-module lots ([PCSP](https://pcserverandparts.com/lot-of-24-hynix-32gb-768gb-total-pc4-2666v-r-2rx4-ddr4-ecc-reg-rdimm-hma84gr7cjr4n-vk/)) | Recert B2B; price discovery | Buys and sells lots | Direct |
| 9 | **Park Place Technologies / Curvature** spares procurement | Wholesale spares + error-trend feed | Out-of-warranty DDR4 fleets need tested spares | Spares procurement |
| 10 | **Z2Data or Accuris/SiliconExpert** | Dataset license | Z2Data already markets 1260H screening ([Z2Data](https://www.z2data.com/insights/how-section-1260h-is-putting-teams-at-risk-of-violating-ndaa-compliance)), but its data stops at the component | BD / data partnerships |

**Alternates:** white-box federal server builders; Northeast university research-computing centers (spares); Mobius Materials (channel); OBSIDIA (partner or acquirer).

**Not first customers:**
- **Dell, HP, Lenovo, Supermicro.** They build compliance in-house or buy from Exiger-class vendors, and reports conflict on whether they use CXMT at all ([Pause Hardware](https://pausehardware.com/memoire-cxmt-oem-pc-penuries/); [Gazlog](https://gazlog.jp/entry/oem-going-for-cxmt/)) [REPORTED].
- **Defense primes.** They want data, not workflow.

---

## 4. Go-to-market

**Channels.**
- **Recert:** eBay first, then B2B accounts #6–9. eBay's share falls from 70% to 40% of sales by m12 (INPUTS `ebay_share_*`).
- **CleanBOM:** direct founder selling, plus SEWP/GSA vendor days from a $3k launch budget (INPUTS `cb_launch_marketing`).
- **Dataset:** business development with compliance-data vendors.

**Pricing** [ESTIMATE unless cited]:

| Item | Price | Basis |
|---|---|---|
| Recert module, eBay / B2B | Realized resale (e.g., $125 for 32GB DDR4) / 0.88× that | INPUTS (amcompute midpoints) |
| PMem 128GB | $200 | m§1b |
| CleanBOM integrator/reseller tier | $750/month | Above SiliconExpert-class entry: Accuris's $6,000 minimum ACV implies SiliconExpert ≈ $7.5k/yr ([Accuris](https://accuristech.com/siliconexpert-offer-terms/)) [REPORTED] |
| CleanBOM module-maker/ODM tier | $2,500/month (35% of customers) | m§1c |
| Evidence pack (per SKU family) | $900 | m§1c |
| Lab die-ID sample | Lab cost × 1.6 (≈$640) | INPUTS |
| Spares + feed to TPMs | Set in kill track D ($0.60/DIMM-month placeholder) | m§1d |

**Sales motion.**
- **Recert** is transactional.
- **CleanBOM** runs on design partners:
  1. A free die-check on one of the prospect's own SKUs.
  2. A $900 pack.
  3. A subscription.
- **The artifact sells it:** X-ray, die photo and SPD bytes side by side. Lead with a mismatch case if kill track B finds one.
- **Positioning:** "evidence for your reasonable inquiry."
- **Deadlines that create urgency:** the §805 indirect DoD ban (2027-06-30), then §5949 (2027-12-23) ([Crowell](https://crowell.com/en/insights/client-alerts/new-year-updated-list-the-us-department-of-defense-updates-its-list-of-chinese-military-companies-with-ancillary-supply-chain-and-usg-contracting-impacts)) [REPORTED].

**First 90 days of selling (Nov-26 to Jan-27):**

| Days | Actions | Measurable output |
|---|---|---|
| 1–30 | The kill experiment (§10) | Go/no-go per line |
| 31–60 | Buy the m2 lot (~$7.1k; m§2). Open an eBay store with per-serial test records. Pitch xByte, TechMikeNY and PCSP. Turn track C's yeses into design-partner LOIs | 2 B2B accounts; 3 signed LOIs |
| 61–90 | Sell ~39 modules (m§2 Jan-27). Deliver free die-checks. Get ITAD downstream questionnaires in writing | ≥$15k revenue in month 3 (model $15.1k); ≥1 paid pack |

CleanBOM subscriptions launch only in Aug-27 (m10, INPUTS `cb_launch`). Before then, the job is pre-selling.

---

## 5. Competitors and why you would win

| Competitor | Position / pricing | Threat |
|---|---|---|
| **Exiger** | $12.7M Army subscription, listed 2026-10-01 ([HigherGov](https://www.highergov.com/news/exiger-wins-13-million-army-1exiger-supply-chain-6490162/)) [REPORTED] | Could add a CXMT flag. Sells to agencies, not SMB module makers |
| **Interos** | ~$12M over 3 years from DLA via SEWP ([Orange Slices](https://orangeslices.ai/dla-inks-12m-contract-to-acquire-interos-ai-software/)) | Same as Exiger |
| **SiliconExpert / Accuris** | Component risk data; $6k minimum ACV at Accuris ([Accuris](https://accuristech.com/siliconexpert-offer-terms/)) | High. Customers already pay them |
| **Z2Data** | Markets 1260H screening; price unpublished | **Highest.** Likeliest to add a module-level CXMT flag |
| **OBSIDIA** | REELScan counterfeit scanning; $34M CHIPS LOI on 2026-07-29 ([NIST](https://nist.gov/news-events/news/2026/07/department-commerce-announces-letters-intent-7-companies-874-million); [SEMI](https://www.semi.org/en/blogs/rethinking-authenticity-in-the-semiconductor-supply-chain-a-conversation-with-obsidia-semiconductors)) | Funded and die-level, but aimed at defense reels. Partner or acquirer |
| **AS6171 labs** (SMT Corp, Integra, Micross); TechInsights | Per-sample tests at $50–500 per component (weak source: [Industrial Monitor Direct](https://industrialmonitordirect.com/blogs/knowledgebase/detecting-counterfeit-ics-in-industrial-electronics)) | Suppliers more than rivals: they sell tests, not a cross-reference |
| **Free self-certification** | Contractors may rely on lower-tier certifications ([Covington](https://www.insidegovernmentcontracts.com/2026/02/far-council-issues-notice-of-proposed-rulemaking-to-implement-prohibition-on-acquisition-of-certain-semiconductors/)) | **The biggest competitor. It costs $0, and buyers will hear "self-certify" from their govcon lawyers first** |
| **Recert sellers:** ServerMonkey, Memory4Less, TechMikeNY, BuySellRAM, PCSP, Curvature, thousands of eBay sellers | Transparent prices; warranties up to lifetime ([Rimlance/Newegg](https://www.newegg.com/rimlance-64gb/p/1X5-00FS-00788)) | Crowded commodity |
| **ITADs selling direct** | Sims redeploys recovered DIMMs into CXL memory ([Sims Lifecycle, 2025-04](https://www.simslifecycle.com/?p=13647)) | They own supply and keep the spread |
| **Mobius Materials** (Richmond VA) | Authenticated surplus marketplace; $3M raise; ML-authentication patent filed ([DC360](https://www.digitalcommerce360.com/2025/12/16/b2b-marketplace-mobius-materials-3-million-funding/)) | Closest venture comparable; also a channel |
| **DIMM-failure prediction:** Park Place ParkView, Lenovo MPFA ([Lenovo Press](https://lenovopress.lenovo.com/lp2326)), Intel MFP ([Intel/Tencent](https://www.intel.co.uk/content/dam/www/central-libraries/us/en/documents/2023-12/intel-memory-failure-prediction-at-tencent.pdf)) | Free or bundled | Why DIMM-health is demoted |

**Win conditions** (all must hold):
1. **Price.** $750–2,500 a month reaches SMB module makers that the Exiger/Interos price tier ignores.
2. **Depth.** A die-level cross-reference built from free bench flow (63 lab-confirmed part numbers by m36; m§3) goes inside the module, where component databases stop.
3. **Timing.** Being live before 2027-12-23.
4. **Recert discipline.** Per-serial records and strict "used" labeling, from an East Coast base.

**Where you lose:**
- Z2Data or SiliconExpert ships a module flag. A funded team could rebuild a ~63-part library in a quarter.
- The final rule keeps the safe harbor, so most sellers self-certify for free.
- OBSIDIA moves to modules.
- ITADs keep the recert spread.
- OEMs drop CXMT from U.S. SKUs.

The fraud evidence is also all consumer-channel. No case of CXMT die relabeled inside U.S. server RDIMMs was found (notes §2).

---

## 6. IP position

**What you would own.**
- **The die-source dataset**, held as a trade secret under subscription terms. Facts are generally not copyrightable in the U.S. [UNVERIFIED-training], so protection is contractual and a head start, not a moat.
- **The software:** grading, evidence-pack generation, and the test-record ledger.
- **The brands.** No trademark search has been done on "CleanBOM" or "ProvenRAM."

**What you use.**

| Component | License or status | Implication |
|---|---|---|
| memtest86+ ([GitHub](https://github.com/memtest86plus/memtest86plus)) | GPLv2 [VERIFIED in Phase 2] | Bench use is fine. Shipping a fleet-scan boot image built on it triggers source obligations |
| stressapptest ([GitHub](https://github.com/stressapptest/stressapptest)) | Apache-2.0 | — |
| rasdaemon ([GitHub](https://github.com/mchehab/rasdaemon)) | GPL | — |
| JEP106 vendor IDs | CXMT = 0x0A11, YMTC = 0x091B, via the memtest86+ table ([jedec_id.h](https://raw.githubusercontent.com/memtest86plus/memtest86plus/main/system/jedec_id.h)) | — |
| AS6171 test methods | Public SAE standard ([ANSI/CALCE](https://share.ansi.org/Shared%20Documents/Standards%20Activities/Microelectronics%20Supply%20Chain%20Security/October%2026-28,%202022%20Workshop/30%20September%202022%20Standards%20Briefings/AS6171%20Overview%20for%20ANSI%20Meeting_Azarian_30Sep2022.pdf)) | Run by outside labs |

**What you can't own.**
- **SPD scanning.** coreboot already reads DDR4 die-maker bytes 350–351 ([coreboot](https://review.coreboot.org/plugins/gitiles/coreboot/+/67c73110e96ec6f1ec90c12f1ed6aac95107e896/src/device/dram/ddr4.c)), and decode-dimms prints the DRAM manufacturer ([i2c-tools](https://github.com/mozilla-b2g/i2c-tools)).
- **Failure prediction from corrected errors.** It is published ([IBM Research](https://research.ibm.com/publications/memory-loss-in-commodity-hardware-predicting-dimm-failures-with-machine-learning); [arXiv 2212.10441](https://arxiv.org/pdf/2212.10441)).

**Freedom-to-operate risks.**
1. **US8468422** (predicting uncorrectable errors from corrected ones; [Google Patents](https://patents.google.com/patent/US8468422)). Status is unchecked. Ship raw trend data, not "predictions," until a ~$1–2k FTO read is done [ESTIMATE].
2. **Mobius's pending ML-authentication patent and OBSIDIA's scanning IP.** Use lab decap, not ML package imaging.
3. **Counterfeiting law.** Never re-mark a module or reprogram its SPD, and label everything used (18 U.S.C. §2320; *Champion Spark Plug*; C_notes §6) [UNVERIFIED-training].
4. **Netlist's PMIC patents** do not apply, because nothing is manufactured.

---

## 7. Regulatory and funding path

| Rule | Status, 2026-11-01 | Effect | Action |
|---|---|---|---|
| **§5949 / FAR Case 2023-008** | Proposed 2026-02-17; comments closed 2026-04-20; **no final rule**; effective **2027-12-23** ([Federal Register](https://www.federalregister.gov/documents/2026/02/17/2026-03065/federal-acquisition-regulation-prohibition-on-certain-semiconductor-products-and-services); [PSC](https://pscouncil.org/a/Resources/2026/PSC_Comments_2026Apr_Semiconductor_20260420.aspx)) [REPORTED] | Creates demand. But no third-party audit is required, supplier certifications may be relied on ([Mayer Brown](https://www.mayerbrown.com/en/insights/publications/2026/03/far-council-proposes-rule-to-prohibit-acquisition-of-semiconductors-from-china-and-countries-of-concern)), due-diligence tools are allowed but not required ([Reed Smith](https://www.reedsmith.com/articles/breaking-circuit-how-covered-semicon-ban-reshaping-supply-chain-usgovcon/)), and contractors' internal use is not covered ([Wiley](https://www.wiley.law/alert-FAR-Council-Proposes-Rule-to-Ban-Purchases-of-Certain-Semiconductor-Products-and-Services)) | Kill criterion 9 |
| **FY24 NDAA §805 / 1260H** | Indirect DoD ban from **2027-06-30** ([Crowell](https://crowell.com/en/insights/client-alerts/new-year-updated-list-the-us-department-of-defense-updates-its-list-of-chinese-military-companies-with-ancillary-supply-chain-and-usg-contracting-impacts)). CXMT was removed 2026-02-13, reinstated 2026-06-08, and **sued DoD 2026-08-28** ([Evertiq](https://evertiq.com/news/2026-08-31-cxmt-sues-pentagon-over-chinese-military-company-designation)). Reports conflict ([HWBusters](https://hwbusters.com/news/cxmt-ymt-pentagons-list-a-memory-war/)) | The earlier hook, but a COTS component exception may exempt memory inside servers | Ask counsel |
| DFARS 252.246-7007/-7008; FAR 52.246-26 | [UNVERIFIED-training] | Recovered DIMMs are barred from DoD deliverables; used-as-new is counterfeit | Never sell recert into DoD work; CleanBOM sells information |
| False Claims Act exposure | [UNVERIFIED-training] | Reliance on a wrong assessment could draw the vendor in | State confidence levels; cap liability; E&O at $400/month; $6k legal (INPUTS) |
| R2v3 | $2,000 per facility per year plus audit; 4+ month booking ([SERI](https://sustainableelectronics.org/wp-content/uploads/2021/03/Steps-to-Getting-Certified-2021.03.pdf)) | Not needed to buy tested, working modules [ESTIMATE] | Get each ITAD's downstream terms in writing |
| ISO 9001 / AS6081 | NQA is the sole AS6081 certification body ([NQA](https://www.nqa.com/certification/standards/as6081)); AS9120 proxy cost $6–12k ([Amtivo](https://amtivo.com/us/resources/insights/aerospace-certification-cost/)) | B2B credibility | ISO 9001 at m15 for $10k (INPUTS) |
| Export controls | Memory modules are EAR99 (01_LANDSCAPE §8) | Low | Screen buyers |

**Non-dilutive funding.**
- **SBIR is closed while the founder keeps the day job:** the PI must spend more than half their time at the small business ([NIST](https://www.nist.gov/tpo/small-business-innovation-research-program-sbir/resources/participation-eligibility-and)).
- **STTR works with a university PI.**
  - The program runs through 2031-09-30 ([IEDC](https://www.iedconline.org/news/2026/04/15/federal-policy-updates/federal-policy-update-sbir-and-sttr-reauthorized/)). Phase I is ~$323k and Phase II ~$2.15M (01_LANDSCAPE §7.1).
  - The natural partner is **UMD CALCE**, the group behind the AS6171 briefing.
  - DoD counterfeit and supply-chain topics recur [UNVERIFIED-training], but none is confirmed open.
  - Treat STTR as library funding, not revenue. It is not in the model.
- **NSF I-Corps** (~$50k) needs an academic lead [UNVERIFIED-M].
- **CHIPS money:** $0. The CRDO BAA reportedly has a ~$10M minimum (01_LANDSCAPE §7.1).
- **State programs** mostly multiply SBIR awards [UNVERIFIED].

**Raise?**
- **Not for recert.** Its constraint is working capital, which its own cash flow funds.
- **Consider a small raise only if all three hold by m18:** ≥10 paying subscribers, a data-licensing LOI from a compliance-data vendor, and a final rule that has not widened the safe harbor.
- **The realistic exit is a dataset sale** to Z2Data, Accuris or OBSIDIA. $446k ARR does not support a priced round.

---

## 8. 18-month roadmap with milestones

Model targets are BASE (m§2). Each gate must be met to continue.

| Quarter | Do | Model target | Gate |
|---|---|---|---|
| **Q1**: m1–3 (Nov-26–Jan-27) | Kill experiment; LLC and legal ($2.5k); two Gen10 beds ($4.2k); first lot in m2; eBay store; 3 LOIs | Jan-27: 39 modules, $15.1k revenue, EBITDA +$2.1k | Tracks A and C pass; lot-1 contribution ≥ 8% |
| **Q2**: m4–6 (Feb–Apr-27) | Library starts at 3 samples/month; DDR5 bed ($4k, m6); 2–3 B2B accounts; part-time technician once volume passes ~175 modules/month (35 founder-hours) | Apr-27: 155 modules, $45.1k revenue, cash $6.8k | Trailing contribution ≥ 12%; ≥2 B2B accounts buying monthly |
| **Q3**: m7–9 (May–Jul-27) | Flex space (above 250 modules); CleanBOM MVP (SPD scan + cross-reference + pack generator); attestation templates and E&O ($6k, m9); §805 takes effect 2027-06-30 | Jul-27: 272 modules, $74.4k revenue | E&O bound at ≤$400/month; ≥18 library part numbers; ≥3 LOIs live |
| **Q4**: m10–12 (Aug–Oct-27) | **CleanBOM launch**; first packs; spares feed offered to TPMs; stop PMem buying before 2027-10-11 | Oct-27: 388 modules, $106.3k revenue, 1.5 subscribers, ARR $25.3k | ≥1 paying subscriber + ≥3 paid packs |
| **Q5**: m13–15 (Nov-27–Jan-28) | **§5949 in force 2027-12-23**; founder goes full-time only through the §11 #7 gate; ISO 9001 ($10k, m15) | Dec-27: 3.1 subscribers, ARR $56.3k | Gate §11 #7; final rule has no COTS/module carve-out |
| **Q6**: m16–18 (Feb–Apr-28) | 12 conversations/month; dataset pitch to Z2Data/Accuris; slow lot buying as the price index falls | Apr-28: 570 modules, 7.5 subscribers, **ARR $140.0k**, cash $67.9k | **≥7 paying subscribers** (target 10); ≥45 library part numbers |

---

## 9. Team required

| Role | When | Cost (model) | Where to find them |
|---|---|---|---|
| **Founder:** product, CleanBOM sales, operations, lot buying | Part-time (35 ops-h/month) m1–13; full-time from m14 | $10k/month once full-time (INPUTS; A-03) | — |
| **Bench technician**, part-time, ESD-trained | From ~m6 | $25/h loaded (INPUTS); ~54 h/month at m18 (570 × 12 min − 60 founder-h) | Electronics programs at local community colleges; technicians from regional contract manufacturers; ServeTheHome and r/homelab members near the bench |
| **Govcon counsel** (contract) | m1 setup; m9 templates | $2,500 + $6,000 (INPUTS) | A boutique govcon firm (big-firm authors in §7 set the reference view) |
| **AS6171 lab partner** | m1, then 3 samples/month | $400/sample [ESTIMATE; track B quotes it] | ANAB list of 26 accredited labs ([ANSI](https://blog.ansi.org/anab/benefits-as-6171-suspect-counterfeit-eee-parts/)); SMT Corp; Integra and Micross (DMEA, 01_LANDSCAPE §7.3) |
| **E&O and liability broker** | m9 | $400 + $200/month (INPUTS) | Tech E&O brokers |
| **ISO consultant + certification body** | m12–15 | $10k, plus $3k surveillance at m27 (INPUTS) | NQA |
| **Federal channel advisor**, commission-only | m9–14 | No fixed cost [ESTIMATE] | Former SEWP/GSA reseller account managers (LinkedIn); NASA SEWP vendor days |
| **STTR PI** (optional) | After m12 | Non-dilutive | UMD CALCE |
| **Data engineer** | Only after ≥10 subscribers | Not modeled | — |

The founder's operations background fits receiving, test flow and supplier attestations. **The gap is federal selling**, which is why track C talks to 15 buyers before any CleanBOM code exists.

---

## 10. The cheapest experiment that could kill it

**Budget:** ~$8,000 gross, ~$3,000 net after resale. **Time:** 30 days (notes §9). All thresholds are fixed now, before any data comes in.

**Days 1–3: line everything up.**
- Request DDR4 RDIMM lot quotes, plus each firm's downstream questionnaire, from three ITADs: Iron Mountain/ITRenew (Sesame), Sims Lifecycle, and one regional R2 ITAD in NJ, PA or MD.
- Buy one used Gen10 server.
- From U.S. sellers, so delivery fits the window, buy two samples: a consumer DDR5 kit with CXMT die (KingBank or Lexar; [Outlook Respawn](https://respawn.outlookindia.com/gaming/gaming-news/pc-industry-turns-to-cxmt-as-dram-supply-crisis-persists)) [REPORTED], and the cheapest OEM-compatible RDIMM from AddOn, Axiom or Brute.
- Get price and turnaround quotes from three AS6171 labs.
- Draft a one-page sample evidence pack.
- List 15 targets: 5 compatible-memory makers, 5 GSA/SEWP resellers including SHI, and 5 integrators.

**Days 4–7: test and ship samples.**
- Test a lot of ~35–40 modules with memtest86+ and stressapptest.
- Log serials and SPD bytes: 320–321 and 350–351 on DDR4, 512–513 and 552–553 on DDR5.
- **By day 7, ship 4 samples to the lab:** 2 from the lot, the CXMT kit, and the compatible RDIMM.

**Days 5–24: test demand.**
- Hold the 15 conversations. Show the sample pack and ask for a paid pilot at $750–2,500 a month or a $900 pack.
- Sell half the lot on eBay and half to xByte, TechMikeNY or PCSP.
- Ask the Park Place and Service Express spares desks whether they would buy spares plus an error-trend feed wholesale.

**Days 25–30: decide.** Apply the thresholds below. No renegotiating.

| Track | Spend | Fail if… (decided now) |
|---|---|---|
| A. Buy side | ~$5,000, mostly recovered | Best ITAD quote > **75%** of realized resale (breakeven 78%; m§6a), **or** measured lot contribution < **8%** |
| B. Evidence | ~$2,000 | Lab > **$600/sample**, > **15 business days**, or die source unidentifiable on ≥2 of 4 samples. An SPD-to-die mismatch becomes the lead sales asset |
| C. Demand | ~$1,000 | Fewer than **3 of 15** sign an LOI or buy a pack, **or none of the three pays cash** [ESTIMATE: my tightening; an LOI costs the buyer nothing] |
| D. Spares feed | $0 | Park Place and Service Express both say no → drop C-85 |

**Decision rule:**

| Outcome | What happens |
|---|---|
| A passes, C fails | Harvest recert through 2027-12-31. (GLUT "CleanBOM sells nothing" ends at $127,548 cash; §2.6) |
| C passes, A fails | CleanBOM standalone (~$47k) |
| Both pass | The sequenced bundle |
| Both fail | Kill DD1 |

**Limits.** Four samples test lab cost, turnaround and feasibility, not library coverage (Phase 3 asked for 20; 03_SCORING §8). A 2–6 week turnaround ([Industrial Monitor Direct](https://industrialmonitordirect.com/blogs/knowledgebase/detecting-counterfeit-ics-in-industrial-electronics)) [REPORTED, weak] alone fails track B.

---

## 11. Explicit kill criteria

Months are model months (m1 = Nov-26).

1. **2026-12-01.** ITAD quote > 75% of resale, or lot contribution < 8% → stop recert. At 75%, ARR at m36 is $250,221 (m§5).
2. **2026-12-01.** Fewer than 3 of 15 commit, or none pays cash → do not build CleanBOM; harvest recert.
3. **2026-12-01.** Lab > $600/sample, > 15 business days, or die source unidentifiable → drop the lab library. Without the library's close-rate lift, ARR at m36 is $323,558 (m§4).
4. **2027-04-30 (m6).** Trailing-3-month recert contribution < 12%, or < 150 good modules sold in April (model 155) → freeze recert scaling.
5. **2027-07-31 (m9).** E&O cannot be bound at ≤ $400/month, or fewer than 3 LOIs are still live → do not launch attestations.
6. **2027-10-31 (m12).** Fewer than 1 paying subscriber and fewer than 3 paid packs (model: 1.5 subscribers) → stop CleanBOM.
7. **Full-time gate (from m13).** Quit the day job only if all three hold:
   - trailing-3-month pre-salary EBITDA ≥ $12k;
   - cash ≥ $25k;
   - **≥ 5 paying CleanBOM subscribers** [ESTIMATE: my addition; the model uses only the first two].

   Without the third condition, a FAR slip in a glut sends the founder back to the day job within two months (§2.6).
8. **2028-04-30 (m18).** Fewer than **7** paying subscribers (model 7.5; must-be-true 10) → stop CleanBOM sales spend, return to the day job if full-time, harvest recert, and try to sell the dataset.
9. **Any date.** The final FAR rule exempts COTS items or memory modules, or §5949 is pushed past 2028-12-31 → kill CleanBOM. If Z2Data or SiliconExpert ships a module-level CXMT flag under $750/month → license the dataset to them, or stop.
10. **Any date.** Expected recert contribution < 5% (INPUTS `min_margin_to_buy`). On the GLUT path this happens near a price index of 0.55, which is a 32GB DDR4 realizing ≈ $69 vs $125 (m§2 GLUT, Sep-28) → stop buying lots; keep a 10% trickle.
11. **2027-09-30.** Stop buying PMem ahead of vSphere 8 end of general support on 2027-10-11 ([Broadcom KB 459135](https://knowledge.broadcom.com/external/article/459135/end-of-general-support-for-vsphere-80.html); VCF 9 drops PMem, [KB 326910](https://knowledge.broadcom.com/external/article/326910)), unless trailing PMem contribution from non-VMware buyers is ≥ 20%.
12. **2027-10-31.** No wholesale spares order from any TPM or MSP → drop C-85.

---

## 12. Cycle test

**GLUT (DDR5 −60% over 2028).** The used-price index falls from 1.0 to 0.40 (m§2 GLUT):

| Month | What happens |
|---|---|
| Jan-28 | EBITDA dips to −$2.1k as the new founder salary meets falling recert margin |
| Sep-28 | Lot buying collapses at an index of 0.55: purchases fall from $42.5k to $3.7k a month |
| Oct-28 | Recert revenue is $5.6k; CleanBOM's is $23.5k |
| Feb-29 | Buying resumes once prices stop falling: 291 modules a month at 9% GM |

- **Last-12-month recert revenue:** $284,620 in GLUT vs $1,361,633 in BASE. CleanBOM is $391,022 in both (m§7).
- **Bundle at m36:** **$434,012 ARR and $392,118 cash** (m§3).

**SEVERE (−90%, DDR5 at $2.04/GB).**
- Recert margin goes to −2%, and lot buying stops in Apr-28 at an index of 0.70.
- Last-12-month recert revenue is $16,297.
- Cash never breaks the reserve. The bundle ends with **$434,012 ARR and $328,128 cash** (m§3, m§7).
- PMem runs at −34% GM, but VMware has already sunset it.

**Cash at m36 by configuration (m§4):**

| Configuration | BASE | GLUT | SEVERE |
|---|---|---|---|
| Full bundle | $610,097 | $392,118 | $328,128 |
| Recert + PMem only | $169,467 | **$22,058** | **−$7,604** |
| CleanBOM standalone | $91,351 | $91,351 | $91,351 |
| DIMM-health standalone | $583 | $5,248 | $7,412 |

**Verdict.** Recert dies in the glut, as all three C-62 scorers said (cycle score 1: "Resale contribution falls to ~1-6% in the glut"). The bundle survives only because CleanBOM has 13.5 subscribers by Oct-28. Their ~$17.5k a month of gross profit (13.5 × $1,295; m§1c) covers the $10k salary and ~$3.5k of opex.

That survival is conditional on three things:
- **Turn timing.** If the glut starts in Oct-27, the founder only goes full-time at m31, and GLUT ARR at m36 is $268,513.
- **The FAR rule's timing.** A 6-month slip during a glut leaves $203,455. Add a 30% lower close rate and it is $115,358 (§2.6).
- **CleanBOM demand holding up.** The model holds it flat, but the sign is unclear:
  - cheap Samsung, SK hynix and Micron bits could pull OEMs off CXMT and shrink the problem;
  - cheap CXMT bits (already 9.5% of 2Q26 DRAM revenue; [Herald](https://biz.heraldcorp.com/article/10866656)) could gain share and grow it.

**DD1 is glut-proof only if the subscription business is real by the end of 2027.** The day-30 test and the m18 gate exist to find that out before the founder quits their job.

---

## 13. Sources

All URLs are logged in `research/sources/*.jsonl`, mainly `p4-provenance-recert.jsonl`. All are search-snippet grade unless marked.

**Regulation and policy**
- https://www.federalregister.gov/documents/2026/02/17/2026-03065/federal-acquisition-regulation-prohibition-on-certain-semiconductor-products-and-services
- https://pscouncil.org/a/Resources/2026/PSC_Comments_2026Apr_Semiconductor_20260420.aspx
- https://www.mayerbrown.com/en/insights/publications/2026/03/far-council-proposes-rule-to-prohibit-acquisition-of-semiconductors-from-china-and-countries-of-concern
- https://www.insidegovernmentcontracts.com/2026/02/far-council-issues-notice-of-proposed-rulemaking-to-implement-prohibition-on-acquisition-of-certain-semiconductors/
- https://www.wiley.law/alert-FAR-Council-Proposes-Rule-to-Ban-Purchases-of-Certain-Semiconductor-Products-and-Services
- https://www.reedsmith.com/articles/breaking-circuit-how-covered-semicon-ban-reshaping-supply-chain-usgovcon/
- https://crowell.com/en/insights/client-alerts/new-year-updated-list-the-us-department-of-defense-updates-its-list-of-chinese-military-companies-with-ancillary-supply-chain-and-usg-contracting-impacts
- https://evertiq.com/news/2026-08-31-cxmt-sues-pentagon-over-chinese-military-company-designation
- https://hwbusters.com/news/cxmt-ymt-pentagons-list-a-memory-war/
- https://www.nist.gov/tpo/small-business-innovation-research-program-sbir/resources/participation-eligibility-and
- https://www.iedconline.org/news/2026/04/15/federal-policy-updates/federal-policy-update-sbir-and-sttr-reauthorized/
- https://nist.gov/news-events/news/2026/07/department-commerce-announces-letters-intent-7-companies-874-million
- https://knowledge.broadcom.com/external/article/459135/end-of-general-support-for-vsphere-80.html
- https://knowledge.broadcom.com/external/article/326910

**CXMT in the channel, counterfeits, die evidence**
- https://respawn.outlookindia.com/gaming/gaming-news/pc-industry-turns-to-cxmt-as-dram-supply-crisis-persists
- https://pausehardware.com/memoire-cxmt-oem-pc-penuries/
- https://gazlog.jp/entry/oem-going-for-cxmt/
- https://www.router-switch.com/sw/faq/cxmt-ddr5-server-memory-cxmr4e464r8as-cb1c-dell-hpe-sizing.html
- https://biz.heraldcorp.com/article/10866656
- https://evezone.evetech.co.za/build-lab/spot-fake-relabelled-ram-used-market
- https://blog.ansi.org/anab/benefits-as-6171-suspect-counterfeit-eee-parts/
- https://share.ansi.org/Shared%20Documents/Standards%20Activities/Microelectronics%20Supply%20Chain%20Security/October%2026-28,%202022%20Workshop/30%20September%202022%20Standards%20Briefings/AS6171%20Overview%20for%20ANSI%20Meeting_Azarian_30Sep2022.pdf
- https://industrialmonitordirect.com/blogs/knowledgebase/detecting-counterfeit-ics-in-industrial-electronics

**Tools and code** (the first three [VERIFIED in Phase 2 by clone])
- https://github.com/memtest86plus/memtest86plus
- https://github.com/stressapptest/stressapptest
- https://github.com/mchehab/rasdaemon
- https://raw.githubusercontent.com/memtest86plus/memtest86plus/main/system/jedec_id.h
- https://review.coreboot.org/plugins/gitiles/coreboot/+/67c73110e96ec6f1ec90c12f1ed6aac95107e896/src/device/dram/ddr4.c
- https://github.com/mozilla-b2g/i2c-tools

**Prices, supply, channels**
- https://www.amcompute.com/appraisals/ddr4-32gb-rdimm
- https://www.amcompute.com/appraisals/ddr5-64gb-rdimm
- https://pcserverandparts.com/lot-of-24-hynix-32gb-768gb-total-pc4-2666v-r-2rx4-ddr4-ecc-reg-rdimm-hma84gr7cjr4n-vk/
- https://www.marketbeat.com/instant-alerts/iron-mountain-q2-earnings-call-highlights-2026-08-08/
- https://www.simslifecycle.com/?p=13647
- https://www.xbyte.com/products/cat-29137
- https://www.publicsector.shidirect.com/product/47547768/64GB-2RX4-DDR4-3200-ECC-RDIMM
- https://www.lttpartners.com/products/addon-cisco-reg-ucsx-mrx64g2re5-64gb-ddr5-6400mhz-registered-dual-rank-x4-1-1v-288-pin-rdimm
- https://www.axiomupgrades.com/inside-the-stack-detail/Third-party-maintenance-How-can-it-help-your-business-
- https://www.newegg.com/Brute-Networks-Server-Memory/BrandSubCat/ID-161080-541/Page-42
- https://www.newegg.com/rimlance-64gb/p/1X5-00FS-00788

**Model INPUTS sources not cited inline above**
- https://www.amcompute.com/appraisals/ddr4-64gb-rdimm
- https://litcommerce.com/ebay-fee-calculator/
- https://www.ebay.de/itm/204762258263

**Competitors**
- https://accuristech.com/siliconexpert-offer-terms/
- https://www.highergov.com/news/exiger-wins-13-million-army-1exiger-supply-chain-6490162/
- https://orangeslices.ai/dla-inks-12m-contract-to-acquire-interos-ai-software/
- https://www.z2data.com/insights/how-section-1260h-is-putting-teams-at-risk-of-violating-ndaa-compliance
- https://www.semi.org/en/blogs/rethinking-authenticity-in-the-semiconductor-supply-chain-a-conversation-with-obsidia-semiconductors
- https://www.digitalcommerce360.com/2025/12/16/b2b-marketplace-mobius-materials-3-million-funding/
- https://lenovopress.lenovo.com/lp2326
- https://www.intel.co.uk/content/dam/www/central-libraries/us/en/documents/2023-12/intel-memory-failure-prediction-at-tencent.pdf

**IP and certification**
- https://patents.google.com/patent/US8468422
- https://research.ibm.com/publications/memory-loss-in-commodity-hardware-predicting-dimm-failures-with-machine-learning
- https://arxiv.org/pdf/2212.10441
- https://sustainableelectronics.org/wp-content/uploads/2021/03/Steps-to-Getting-Certified-2021.03.pdf
- https://www.nqa.com/certification/standards/as6081
- https://amtivo.com/us/resources/insights/aerospace-certification-cost/
