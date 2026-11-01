# DD2 — Memory Lifecycle & Cost Intelligence for OEMs (`lifecycle-intel`)

Author: `p4w-lifecycle-intel` · As of 2026-11-01 · Model: `models/lifecycle-intel.py` (re-run 2026-11-01, exit 0, output identical to `research/phase4/lifecycle-intel_model_output.md`) · Research notes: `research/phase4/lifecycle-intel_notes.md` · Every web fact below is search-snippet grade, so the best tag it can carry is **[REPORTED]**. Model figures are **[ESTIMATE]** by construction.

---

## 0. Header

**Pitch.** A $249/month web app shows small U.S. hardware makers which memory chips in their products are about to go end-of-life or spike in price. It then pools their anonymised purchase prices into a Memory Cost Escalation Index, which buyers and sellers license to write fair memory surcharges and refunds into their contracts.

**Anchor and folded concepts**

| Role | ID | Concept | Why it is here (scorer quotes, `research/phase3/scores_raw/*.json`) |
|---|---|---|---|
| Anchor | C-80 | DRAM Cost & Allocation Intelligence for SMB OEMs | Veteran: "use it only as a free lead-gen front end." Founder scorer: "Best founder-fit and fastest to ship, with the worst durability." |
| Folded (feature) | C-29 | NVM-EOL Migration Finder | Founder scorer: "a feature for C-80 or lead-gen for C-12, not a standalone business." VC: "lead-gen for C-12/C-80, not a company." |
| Folded (the durable leg) | C-86 | Memory Cost Escalation Index + EPA clause kit | Veteran: "The best-shaped data product in my chunk because it is two-sided and its clauses persist through the glut." VC: "the ceiling is ~$0.3M ARR unless it wins that fight." |
| Folded (software only) | C-61 | DRAM Continuity Vault | Founder scorer: "The LTB-sizing software fits the founder, but the money is in a vault that loses money below ~8 OEMs." Only the last-time-buy (LTB) sizer and paid LTB studies are kept. **The vault is out.** |
| Folded (free feature + three phone calls) | C-72 | Legacy-DRAM buying co-op | Founder scorer: "Three supplier calls decide everything … A free kill test, not a venture." It becomes an unpriced pooled-forecast feature and three calls in §10. |

**Capital tier: T0.** The model's worst cash point is $21,951 at m10, a maximum draw of **$18,049** of the founder's $40k (`models/lifecycle-intel.py` §6).

**Scores and ranks** (`scores.csv`; consensus of three scorers; out of 100, rank in parentheses)

| ID | Tier | Default | Capital-constrained | Moonshot | Moat / competition / cycle (1–5) |
|---|---|---|---|---|---|
| C-80 | T0 | 79.0 (5) | 82.5 (4) | 75.8 (5) | 1 / 1 / 1 |
| C-29 | T0 | 79.0 (4) | 82.5 (3) | 75.8 (4) | 1 / 1 / 3 |
| C-86 | T0 | 75.0 (8) | 78.3 (9) | 74.2 (7) | 3 / 3 / 4 |
| C-61 | T1 | 70.0 (16) | 70.8 (16) | 66.7 (13) | 3 / 2 / 4 |
| C-72 | T1 | 64.0 (20) | 65.8 (19) | 65.0 (15) | 2 / 3 / 1 |

The anchor ranks high only because it is cheap, fast and founder-shaped. It scores the floor (1) on moat, competition and cycle. The bundle exists to borrow C-86's moat and cycle scores.

**Three verdicts**

- **POSSIBLE? Yes.** This is TRL 9 software on public APIs and public end-of-life notices. The two real unknowns are commercial, not technical: whether Nexar and DigiKey allow in-app price display, and whether OEMs will contribute purchase-order prices.
- **PROFITABLE? Marginal.** Gross margin reaches 74% by m36, and the business is cash-positive from m11 with the founder unpaid. But BASE ARR is only **$126k at m18 and $422k at m36**, a $10k/month founder salary is covered only from **m23 (2028-10)**, and a 30% miss on price or conversion means it **never** pays the founder within 36 months. It is a good side business, not a venture, unless the index becomes the reference that contracts cite.
- **DOABLE BY THIS FOUNDER? Yes.** It is pure software, part-time and T0, and the founder's day job (product development and operations at a manufacturer) is the buyer persona. The founder will need help in two places: credibility for the index methodology, and selling to procurement leads.

**Recommendation:** FALLBACK-grade, not PRIMARY. Run it index-first, with the SaaS as the data-collection funnel. Kill it on the 30-day test in §10.

---

## 1. How it works

Picture a 60-person company in upstate New York that builds rugged industrial PCs. Every board it ships carries 8–32 GB of DDR4, an eMMC chip and a small EEPROM [ESTIMATE: illustrative composite, not a real firm]. In 2026 three things happened to that company at once:

- Memory prices spiked 80–90% ([Luminovo](https://luminovo.com/resources/blog/memory-chip-shortage)) [REPORTED].
- Distributors started rationing DDR4 by purchase history: Avnet reports lead times of 25–45+ weeks against an 8–12-week norm ([Avnet, 2026](https://www.avnet.com/integrated/resources/article/memory-is-breaking-product-plans/)) [REPORTED].
- Chip makers announced end-of-life (EOL) for the exact parts on its bills of materials.

Nobody there has a full-time memory analyst. The procurement lead tracks it in a spreadsheet.

The product does four things for that company:

```
 Customer's bill of materials (CSV/Excel)        Data the product reads
            |                                     - DigiKey / Nexar APIs: live price, stock, lifecycle (cached <=24 h)
            v                                     - End-of-life notices (PDFs on distributor servers)
 [1] SCAN: find every memory part                 - Free DRAMeXchange spot prices (sanity check only)
     (DDR3/4/5, LPDDR, eMMC, NOR, EEPROM)
            |
            v
 [2] ALERTS: "Part X goes EOL; last order date is 6 months out; here are 3 alternates;
     this EEPROM can become an F-RAM; this module contains a Chinese die banned for federal sales"
            |
            v   (optional, 10% discount for joining)
 [3] POOL: customer shares anonymised memory purchase prices --> panel, >=5 companies per price cell
            |
            v
 [4] INDEX: monthly Memory Cost Escalation Index --> free headline number + paid licence
     + ready-to-sign contract clause: "memory surcharge moves with the index, up AND down"
```

**Steps 1–2 are the subscription** ($249 or $649/month). They save engineering hours and catch last-time-buy deadlines. Under the J-STD-048 practice, a chip maker usually gives a 6-month window to place final orders after it announces a discontinuance ([MaxLinear](https://www.maxlinear.com/support/quality/policy-and-procedure); [Boréas](https://boreas.ca/pages/product-life-cycle-policy)) [REPORTED]. Miss that window and you redesign the board. Step 2 also folds in two smaller ideas:

- C-29: suggesting F-RAM or MRAM replacements when an EEPROM or NOR flash part dies.
- C-61's software: sizing how many chips to stockpile before the last order date.

**Steps 3–4 are the part that is not just a feature.** Contract memory prices moved about 6× in five quarters (C-86 card, `research/phase2/concepts_master.json`). At swings like that, any fixed-price contract for computers either bleeds money or carries a fat contingency. Commodity markets solved this with licensed price references written into contracts ([Fastmarkets](https://www.fastmarkets.com/products/price-data-how-to-use-it/)) [REPORTED]. Memory has no such index:

- The U.S. Bureau of Labor Statistics publishes no DRAM-specific producer price index ([FRED](https://fred.stlouisfed.org/series/PCU334413334413)) [REPORTED].
- TrendForce's DXI is a spot-market index, not a contract-settlement index ([DRAMeXchange FAQ](https://dramexchange.com/Service/Faqs)) [REPORTED].

If a seller and buyer both agree to "surcharge = index change × memory content", the seller is protected when prices spike and the buyer gets a refund when prices crash. That two-way use is why this leg earns *more* in a glut, not less.

The memory-specific scope and the contributed-price panel are what differ from SiliconExpert or Octopart. Steps 1–2 alone are a feature those companies already sell.

---

## 2. Cost and unit-economics model

All figures come from `python3 models/lifecycle-intel.py` (BASE scenario unless stated). Model month 1 = 2026-12. The founder works ~15 h/week unpaid until the trailing three months of (gross profit − opex) reach $10k/month. Assumptions are logged in `research/assumptions/p4-lifecycle-intel.md`.

### 2.1 Pricing and unit economics per line (model §3)

| Line | Price | Variable COGS | Contribution margin | Price anchor |
|---|---|---|---|---|
| SaaS Team | $249/acct-mo | $59 | 76% | SiliconExpert BOM Manager Essentials $250/mo, 1 user, 1 BOM ≤500 parts ([SiliconExpert](https://www.siliconexpert.com/products/bom-manager/)) [REPORTED] |
| SaaS Pro (multi-BOM, LTB module) | $649/acct-mo | $97 | 85% | Accuris price match: minimum $6,000 ACV ([Accuris](https://accuristech.com/accuris-price-match-offer-terms/)) [REPORTED] |
| SaaS blended net | $335/acct-mo | $69 | 80% | 25% Pro mix; 10% discount for the 40% of accounts that contribute prices [ESTIMATE] |
| Index Standard licence | $6,000/yr ($500/mo) | $75/mo | 85% | DRAMeXchange Silver $5k, Gold $11k ([GII](https://giikorea.co.kr/annual/tdf225654-dramexchange-membership.html)) [REPORTED] |
| Index Enterprise (redistribution/API) | $24,000/yr | $180/mo | 91% | DRAMeXchange DRAM&NAND Platinum $30k (same listing) |
| LTB study (one-off) | $3,500 | $1,155 | 67% | 1.5–2 analyst-days [ESTIMATE] |

**Acquisition cost (model §3):**

| Measure | Value |
|---|---|
| Cash CAC | **$563** per account (marketing plus $35 per qualified trial) |
| Fully loaded CAC | **$1,188** (adds 1 founder-hour per trial at $75) |
| Lifetime at 2% monthly churn | ~50 months |
| LTV | $13,649 |
| LTV/CAC | 24.3 cash; **11.5 loaded** |
| Payback | 2.1 months cash; **4.4 months loaded** |

CAC is not the problem. **Volume and price are.**

**Fixed data and infrastructure costs (inputs):**

| Item | Cost | Basis |
|---|---|---|
| Hosting | $150/mo | [ESTIMATE] |
| Nexar API, Standard tier | ~$300/mo | Tier limits are published (Standard ≤2,000 matched parts) but prices are not ([Nexar](https://nexar.com/compare-plans)) [ESTIMATE] |
| Nexar API, Pro tier (from 60 accounts) | ~$1,000/mo | Same source [ESTIMATE] |
| Commercial display licence (from m12) | ~$1,000/mo | [ESTIMATE] |
| DRAMeXchange Silver, internal validation only (from m9) | $5,000/yr | GII listing above |

These sum to $1,867/month at m12–m24. **They are the largest COGS unknown and are UNVERIFIED.**

**Blended gross margin including fixed data costs (model §3):**

- m12 (2027-11): 45% on $5,787/month of revenue.
- m18 (2028-05): **65%** on $12,978.
- m24 (2028-11): 71% on $19,219.
- m36 (2029-11): **74%** on $40,811.

### 2.2 ARR, breakeven and cash under three price scenarios (model §6)

The DDR5 contract path is $20.37/GB in Q4-2026, rising to $21.79 through 2027. From 2028-01 it diverges by scenario:

- **BASE:** −15% by Dec-2028.
- **GLUT:** falls to $8.15 by Dec-2028 (−60%, ASSUMPTIONS A-05).
- **SEVERE:** falls to $2.04 (−90%).

The price inputs come from `models/dram_cost_stack.py` `ddr5_reference()`; the "rising through 2H27" path is TrendForce via [TechNews, 2026-07-09](https://finance.technews.tw/2026/07/09/long-term-agreements-price-cap-3q26-server-dram-contract-price-estimated-13-18-qoq-increase/) [REPORTED].

| Scenario | ARR m12 | ARR m18 | ARR m24 | ARR m36 | Breakeven, founder unpaid | Covers $10k/mo salary | Full-time from | Cash low point | Cash m36 |
|---|---|---|---|---|---|---|---|---|---|
| BASE | $49,391 | **$126,068** | $193,183 | **$421,548** | m11 (2027-10) | m23 (2028-10) | m26 (2029-01) | **$21,951 @ m10** | $214,697 |
| GLUT | $49,391 | $129,654 | $187,190 | $333,977 | m11 | m23 (2028-10) | m26 | $21,951 @ m10 | $187,144 |
| SEVERE | $49,391 | $127,315 | $172,694 | $281,815 | m11 | m24 (2028-11) | m26 | $21,951 @ m10 | $155,788 |

How to read the table:

- **First revenue lands at m5 (2027-04)**, inside the 18-month target.
- **Account counts:** BASE has 27 accounts and 2.0 licences at m18, and 88 accounts and 7.7 licences at m36. At m36 GLUT has 61 accounts and 10.1 licences; SEVERE has 48 and 10.3.
- **The cash low is the same in all three scenarios.** It falls at m10, before the price paths split at m14. Cash risk is front-loaded and independent of the cycle; revenue risk is back-loaded.
- **ARR counts subscriptions and licences only.** LTB studies are one-off and appear in cash, not ARR.

### 2.3 Sensitivity (model §7; each input ×0.7 / ×1.3, all else BASE)

| Driver | ARR m36 at ×0.7 | ARR m36 at ×1.3 | Salary covered (×0.7 / ×1.3) |
|---|---|---|---|
| Price, all lines | $195,857 | $604,111 | **never** / m19 |
| Conversion/close rate | $228,598 | $604,111 | **never** / m19 |
| Churn | $462,076 | $393,308 | m23 / m24 |
| COGS | $437,089 | $412,701 | m23 / m25 |

Price and close rate are the whole game.

- A 30% shortfall on either one means the founder is never paid within 36 months.
- Churn and COGS barely matter.
- The cash low stays between $17,096 and $24,795 in every case, so **the founder's $40k is never exhausted** (the worst draw is ~$23k). Their time is what is at risk.

### 2.4 What must be true (model §8)

- **To pay the founder $10k/month:** at least **52 paying accounts, or ~27 accounts plus 10 index licences**. BASE has 27 accounts and 2 licences at m18, so the founder stays part-time until m26.
- **To reach $1M ARR by m36:** SaaS trial inflow must be **2.3×** the modelled level (~57 qualified trials/month part-time). That means ~225 accounts by m36, about 3.7% of an estimated 6,000 U.S. SMB OEMs (an unsourced order-of-magnitude [ESTIMATE]).
- **To reach $2M:** inflow must be **4.7×**, with ~468 accounts.
- **Index-only equivalent:** 115 licences per $1M at $8,700/yr.
- **The kill test must show** at least 5 paid deposits from 25 qualified conversations (20%), which supports the model's 12% trial-to-paid conversion.

**Bottom line:** without the index becoming a reference, this is a **$0.3–0.6M ARR business** (notes §7).

---

## 3. Target customer and the first ten customers

**Buyer:** the procurement, supply-chain or component-engineering lead at a U.S. hardware maker with $1–50M a year of BOM spend, memory on every board, and 5–20-year product lives [ESTIMATE: buyer definition; model input `tam_us_smb_oems`]. Their pain is documented:

- **Medtech:** AdvaMed reports 75–80% of medtech products contain memory. Among its members, 75% report memory constraints, 88% price increases and 63% allocation problems ([AdvaMed, 2026-08-17](https://www.advamed.org/2026/08/17/memory-chip-shortages-implications-for-medtech-innovation-and-patient-care/)) [REPORTED].
- **Small buyers generally:** Luminovo cites 80–90% price spikes and says firms without cash to stockpile are squeezed out of allocation ([Luminovo](https://luminovo.com/resources/blog/memory-chip-shortage)) [REPORTED].

**Index buyer:** whoever must pass memory cost through a fixed-price contract. That means OEMs issuing surcharges, EMS houses repricing turnkey builds, and federal IT resellers. In March 2026 the Coalition for Common Sense in Government Procurement (CGP) asked GSA for weekly economic price adjustments ([CGP letter](https://thecgp.org/images/2026/03/Letter-to-Larry-Hale-on-Memory-Chips.pdf)) [REPORTED].

**None of the companies below has been contacted. Each one is a hypothesis for §10.**

| # | Customer | Line | Why they buy | How to reach |
|---|---|---|---|---|
| 1 | The founder's employer (design/manufacturing company) | Design partner (unpaid) | The persona itself | **Written conflict and IP clearance first** (§6). Then the founder's own procurement colleagues |
| 2 | OnLogic / Logic Supply (South Burlington, VT) | Team → Pro | Industrial PCs with DDR4/eMMC-heavy BOMs, on the East Coast ([Thomasnet](https://www.thomasnet.com/articles/top-suppliers/industrial-computer-manufacturers-suppliers/)); the rebrand is [UNVERIFIED] | Sales Navigator to the purchasing/supply-chain manager; offer a free BOM scan; drivable for an on-site demo |
| 3 | Amplicon USA (Fairport, NY) | Team | Industrial computers and panel PCs (Thomasnet, same list) | Same; regional visit |
| 4 | Trenton Systems (U.S.-made rugged servers) | Pro + index | DoD-facing server DRAM; §5949 exposure from 2027-12-23 ([Trenton list](https://www.trentonsystems.com/blog/list-of-rugged-server-manufacturers)) | Lead with the CXMT/YMTC flag and LTB sizer |
| 5 | CP Tech USA (ex-Chassis Plans) | Pro | Rugged computers built in the U.S. ([CPNA](https://cpnorthamerica.com/?p=67)) | Same pitch as #4 |
| 6 | Core Systems USA | Pro | Rugged servers (Trenton list) | Same |
| 7 | WINSYSTEMS | Team + LTB study | Long-lifecycle embedded SBCs with DDR, eMMC and NOR; the NVM cross-reference fits ([Arm catalog](https://www.arm.com/partners/catalog/winsystemsinc)) | Component engineer; lead with an EEPROM/NOR→F-RAM swap report |
| 8 | Industrial Computers Inc. (Ann Arbor, MI) | Team | High-reliability industrial PCs (Thomasnet) | Sales Navigator; free scan |
| 9 | Mid-size East Coast medtech OEM (patient monitors, imaging carts, IVD analysers with embedded PCs) | Pro + LTB study | 63% report allocation problems (AdvaMed); legacy phase-outs force costly redesigns ([PwC, 2026-06](https://www.pwc.com/us/en/industries/health-industries/library/medtech-semiconductor-memory-shortage.html)) | AdvaMed and MDMA member directories; supply-chain committee contacts |
| 10 | Tier-2/3 U.S. EMS ($50–500M revenue [ESTIMATE: segment definition]) | Pro + **index licence** | Reprices turnkey memory for its OEM customers. Lytica already sells into EMS through NEOTech, which proves the budget line exists ([PR](https://www.webull.com/news/15265411318440960)) | East Coast IPC/SMTA chapter meetings; the VP of materials |

**Index-licence shortlist.** All three are reached by direct email to the pricing or contracts lead, with the clause kit attached.

- **CGP-member GSA MAS IT hardware resellers.** They asked GSA for weekly adjustments. Find them on the GSA eLibrary hardware vendor lists.
- **Unipi (CZ).** Its two-part quote has carried a memory surcharge at cost since 2026-07-20, "reduced once memory prices normalize", with no named index ([Unipi](https://www.unipi.technology/ram-surcharge)) [REPORTED].
- **Revolution Pi/KUNBUS (DE).** It added an eMMC surcharge from 2026-07-10 ([notice](https://revolutionpi.com/fileadmin/downloads/Informationsschreiben/eMMC_surcharge_07-26-en.pdf)) [REPORTED].

**No U.S. OEM surcharge notice was found.** That is open gap #3 in the notes, and it is the single most worrying fact for the index.

---

## 4. Go-to-market

**Channel.** Content-led and founder-led.

- **Free layer:** a public "Memory Surcharge Reference" headline index and a monthly memory-shortage note. This copies the lead-generation pattern of Mobius Materials ([Mobius](https://www.mobiusmaterials.com/post/inside-the-memory-supercycle-second-act)) and of Luminovo's free 2026 EMS memory risk matrix ([Luminovo](https://luminovo.com/guides/2026-ems-memory-chip-risk-matrix)) [REPORTED].
- **Hook:** a free 2-minute "memory exposure scan" of a pasted BOM.
- **Associations:** AdvaMed/MDMA (medtech), IPC/SMTA (EMS) and CGP (federal resellers).
- **Trade show:** one per year (model: $2,500 at m10, m22, m34).

**Pricing** (model inputs; §2.1):

- **Free:** the scan and the headline index.
- **SaaS:** Team $249/mo; Pro $649/mo. Design partners get 40% off through m10, and price contributors get 10% off.
- **Index:** Standard $6,000/yr; Enterprise $24,000/yr.
- **LTB study:** $3,500.
- **Pooled forecast (C-72):** free inside Pro.

**Sales motion.**

- **SaaS:** scan → 14-day trial → founder demo (1 hour) → card payment. Monthly, cancel any time, matching SiliconExpert Essentials.
- **Index:** sold founder-to-procurement-lead, with a clause kit drafted by a government-contracts attorney. Every sale needs both contract parties' legal teams to accept it. That is why the model starts licences at m12 and sells only 0.6 a month at peak volatility.

**First 90 days of selling** (selling starts with the kill test):

| Days | Dates | Actions | Measurable output |
|---|---|---|---|
| 1–30 | 2026-11-02 → 12-01 | Kill test (§10): 60 contacts, 25 calls, deposits, index and panel commitments, supplier calls | ≥5 deposits; ≥2 index commitments; ≥5 panel commitments |
| 31–60 | 12-02 → 2027-01-01 | Turn deposits into 5 design partners with a written data-contribution agreement. Publish the first monthly memory note. Start the newsletter (target 150 subscribers) | 5 signed design-partner agreements; ≥3 BOMs uploaded |
| 61–90 | 2027-01-02 → 01-31 | Weekly design-partner calls on the MVP. Second note. Ask each partner for one referral. Build a waitlist for the m5 paid launch | ≥10 waitlist accounts; ≥3 partners sharing 24 months of PO history |

---

## 5. Competitors and why you would win

All rows are [REPORTED] (search-snippet grade) except the last, which is [ESTIMATE].

| Competitor (owner) | What it sells for memory | Price / position |
|---|---|---|
| SiliconExpert (Arrow) | Lifecycle status, PCN alerts, pin-to-pin alternates, BOM risk | **$250/mo** Essentials; Pro and Enterprise annual, on request ([SiliconExpert](https://www.siliconexpert.com/bom-manager/)) |
| Accuris (ex-IHS parts business) | Parts and BOM intelligence | **≥$6,000 ACV**; undercuts SiliconExpert by 20% in year one ([Accuris](https://accuristech.com/siliconexpert-offer-terms/)) |
| Z2Data | Part, lifecycle and supplier risk; in Gartner's 2026 Magic Quadrant | "Custom per month", usage-based ([Z2Data](https://www.z2data.com/pricing)) |
| Lytica (Ottawa) | Spend analytics on **real customer transaction prices** | Annual, unpublished ([CENGN](https://www.cengn.ca/wp-content/uploads/2020/06/Lytica-Success-Story.pdf)) |
| Supplyframe Commodity IQ (Siemens) | Rolling four-quarter DRAM/SRAM price and lead-time forecasts | Unpublished ([Supplyframe](https://intelligence.supplyframe.com/commodities-analyzed-sram-dram-specialty)) |
| Octopart/Nexar (Altium, owned by Renesas since 2024-08-01) | **Free** BOM Tool with Active/NRND/EOL flags; GraphQL API | Free ([Octopart](https://octopart.com/pulse/p/reducing-costs-efficient-bom-management)); Renesas is building lifecycle management ([Renesas](https://www.renesas.com/en/about/newsroom/renesas-completes-acquisition-altium)) |
| Luminovo (Munich) | EMS quoting; years-to-EOL predictions | Priced by procurement spend ([Luminovo FAQ](https://luminovo.com/faq/how-much-does-luminovo-cost)) |
| TrendForce / DRAMeXchange | Spot and contract DRAM prices; DXI spot index; the default reference | $5k–55k/yr (GII listing) |
| Counterpoint Memory Price Tracker | Monthly tracker and forecast | Unpublished ([Counterpoint](https://counterpointresearch.com/en/reports/memory-price-tracker-and-forecast-july-2026)) |
| Free trackers | 37+ GitHub DRAM-price scrapers; the nwfella memory price index | Free ([GitHub](https://github.com/search?q=dram+price&type=repositories); [nwfella](https://github.com/nwfella/memory-price-index)) |
| EMS procurement desk + spreadsheets | Most of what an SMB OEM actually uses | "Free" (bundled) |

**Where this venture would win (honest conditions):**

1. **Memory-only depth at an SMB price.** It would treat memory as a first-class category: DDR generation, die source, LTB deadline, F-RAM/MRAM swap, CXMT/YMTC flag. Its Team tier costs $249, and the general platforms' entry tiers are $250/mo (SiliconExpert) or ≥$6k/yr (Accuris). The gap is price point and focus, not capability; Phase 2 verification said the same.
2. **A two-sided contract index nobody else sells.** No memory escalation index or clause kit was found (one targeted search, 2026-11-01). TrendForce's DXI is a spot index without a contract-licensing programme. BLS has no DRAM PPI, which weakens the "use a BLS index first" default in federal contracting.
3. **Contributed transaction prices.** This is the Lytica pattern, applied only to memory. Lytica is the proof that "real customer pricing, not distributor list pricing" sells.

**Where it loses:**

- **On lifecycle alone.** SiliconExpert and Octopart already answer most of the question, and Octopart answers it for free. If a prospect has SiliconExpert, the SaaS is redundant.
- **On forecasts.** Supplyframe CIQ and Counterpoint have analysts and history; this venture would have neither.
- **On credibility.** Any counterparty can say "use TrendForce", and an index from a one-person company is easy to dismiss. Spot ran ~2× contract in 2026 (veteran scorer), so basis risk is real.
- **On distribution.** Arrow (SiliconExpert), Siemens (Supplyframe) and Renesas (Octopart) can bundle a memory module at zero marginal price.

The realistic upside exit is selling the panel and index to one of them (notes §7, path c).

---

## 6. IP position

**What the venture would own:**

1. **The contributed price panel.** Its value rests on contracts: each contributor grants a perpetual licence to use its anonymised, aggregated prices. This is the only real moat.
2. **The index methodology and the clause kit.** Both are protected by copyright. The methodology should be published, so it can be audited.
3. **The index name.** Register it as a trademark (~$350–1,000 per class at the USPTO [UNVERIFIED]).
4. **The code.**

**Nothing here is worth patenting.** Index methods and BOM scanning are prior art (Lytica since 2005, Fastmarkets, DXI).

**What it licenses (and the constraints):**

| Data source | Allowed use | Limits |
|---|---|---|
| Nexar/Octopart API | Can feed live in-app views ([Nexar legal](https://nexar.com/api/legal)) | Octopart's terms bar firms in component distribution, "including software developers building applications for that market", from using the API for pricing and availability. They also **prohibit historical pricing/inventory trend use and caching beyond 24 h** ([Octopart API legal](https://octopart.com/api/legal)) [REPORTED]. Nexar data **cannot** feed the index or historical charts |
| DigiKey API | Product information | 120 requests/min and 1,000/day; prices vary by locale and customer ID ([DigiKey](https://developer.digikey.com/documentation)). Redistribution and display terms were **not found** |
| DRAMeXchange Silver | Internal validation only | Not redistributable |
| End-of-life notices (PDN/PCN PDFs on distributor media servers, e.g. [NXP PDN via DigiKey](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/6778/PDN-202504001DN.pdf)) | Crawlable and attributable | No licence needed (notes §2) |

**What it cannot have:** TrendForce or InSpectrum contract data for redistribution. That is the reason the index has to be built from a contributed panel.

**Freedom-to-operate risks, ranked:**

1. **Octopart's "distribution-market software developer" clause.** It could be read to cover this product's price display. A written answer is kill item K5.
2. **Antitrust exposure from pooling competitors' prices.** Mitigation: aggregated, lagged data with ≥5 contributors per cell. The 1996 safety zones were withdrawn in 2023 [UNVERIFIED], so counsel must sign off (model: $7k at m8).
3. **The founder's employment agreement.** Most employers' IP-assignment and moonlighting clauses would claim or bar a side business that serves their own industry. The founder needs written clearance before writing code [ESTIMATE: standard practice; contract not seen].
4. **Lytica or SiliconExpert patents.** Not searched [UNVERIFIED]. Low risk given decades of prior art.

---

## 7. Regulatory and funding path

**Rules that matter:**

- **Federal price adjustment.**
  - FAR 16.203-1(a)(3) permits adjustment on "cost indexes of labor or material … specifically identified in the contract", and FAR 52.216-4 is the standard clause ([FAR 16.203-1](https://github.com/GSA/GSA-Acquisition-FAR/blob/master/dita/16.203-1.dita); [FAR 52.216-4](https://github.com/GSA/GSA-Acquisition-FAR/blob/master/dita/52.216-4.dita)) [VERIFIED by the Phase 2 E agent].
  - **But DLAD 16.203-4 tells contracting officers to pick the most appropriate BLS index first** and to document why BLS indices don't fit before using any other ([DLAD 16.2](https://www.acquisition.gov/index%2ephp/dlad/subpart-16.2-%E2%80%93-fixed%E2%80%93price-contracts)) [REPORTED].
  - PGI 216.203-4 asks for simple clauses with trigger bands ([PGI 216.2](https://www.acquisition.gov/index%2ephp/dfarspgi/pgi-216.2-fixed-price-contracts)).
  - GSA schedules run on GSAM 552.238-120, effective 2026-01-15 ([GSAM](https://www.acquisition.gov/gsam/552.238-120)). Whether that clause can reference a third-party index is **UNVERIFIED**.
  - Net effect: federal adoption is case by case, so the **commercial market comes first**.
- **Commercial contracts are weak on this point.** A May-2026 law-firm note says most IT price-variation clauses were written for 3–5% annual moves, not 35–50% jumps ([Lewis Silkin, 2026-05-11](https://www.lewissilkin.com/insights/2026/05/11/when-hardware-costs-spike-what-your-tech-contracts-should-say)) [REPORTED]. That gap is the index's opening.
- **§5949.** From 2027-12-23, federal agencies may not buy products containing CXMT, YMTC or SMIC chips. FAR Case 2023-008 was proposed on 2026-02-17 and accepts supplier self-certification after "reasonable inquiry" ([Federal Register](https://www.federalregister.gov/documents/2026/02/17/2026-03065/federal-acquisition-regulation-prohibition-on-certain-semiconductor-products-and-services)) [REPORTED]. A BOM-level flag is a cheap feature here. Do not build DD1's provenance business inside this one.
- **Antitrust** on contributed prices (§6). **Export:** EAR99 software, no constraint.

**Non-dilutive money.** Expect **$0 in the first 24 months.**

- **SBIR is closed to the founder.** SBIR/STTR is reauthorized through 2031-09-30 ([IEDC, 2026-04-15](https://www.iedconline.org/news/2026/04/15/federal-policy-updates/federal-policy-update-sbir-and-sttr-reauthorized/)). But **the SBIR principal investigator must spend more than half their time at the small business**, so a founder who keeps a day job cannot be PI ([NIST](https://www.nist.gov/tpo/small-business-innovation-research-program-sbir/resources/participation-eligibility-and)) [REPORTED].
- **STTR is the only plausible route,** with a university PI. The natural partner is UMD CALCE (Prof. Peter Sandborn), which teaches obsolescence forecasting and lifetime-buy optimisation ([CALCE](https://calce.umd.edu/event/20069/electronic-part-obsolescence-forecasting-mitigation-and-management)), for a DMSMS/LTB forecasting module. **No current DMSMS forecasting topic was found.** The Naval Postgraduate School's 2025-12 regression work shows the Navy is interested ([NPS](https://dair.nps.edu/handle/123456789/5619)).
- **CHIPS money: none.** It does not fit.

**Raise?** **No**, at least not before m18. The model never needs more than $18k, and investors will see a $0.4M-ARR ceiling. Reconsider only if, by 2028-05, the index has at least 10 licences or one enterprise redistribution deal with an EMS network or distributor. That would make the "reference index" path real, and a $0.5–1M angel round [ESTIMATE: ~2 years of founder plus seller at the model's $10k + $9k/mo loaded] could fund a full-time founder plus a seller. Otherwise the endgame is either a profitable side business or a sale of the panel to Lytica, Z2Data, Accuris, Supplyframe or Luminovo.

---

## 8. 18-month roadmap with milestones

Model month m1 = 2026-12. Account and MRR targets are the model's BASE path (§4 of the model output).

| Period | Build | Sell / data | Gate (date: measurable test) |
|---|---|---|---|
| **m0** (Nov 2026) | Scan prototype (~20 h) | Kill test (§10) | **2026-12-01:** K1–K5 pass, or kill the named leg |
| **Q1** m1–3 (Dec 2026–Feb 2027) | MVP: BOM upload, memory MPN classifier, PDN crawler, alerts on the DigiKey API | 5 design partners; contribution agreement; monthly note | **2027-02-28:** 5 partners active weekly; ≥3 sharing PO history |
| **Q2** m4–6 (Mar–May 2027) | Team/Pro billing | **Paid launch m5 (2027-04)**; 6–8 trials/month (model) | **2027-05-31:** ≥2 paying accounts (model: 1.7), with design partners at the 40% price; ≥3 of 5 partners still active |
| **Q3** m7–9 (Jun–Aug 2027) | LTB sizer; NVM cross-reference (EEPROM/NOR/NVSRAM → F-RAM/MRAM); §5949 flag | Legal review at m8 ($7k). **Index methodology plus 24-month back-fill published m9 (2027-08)** | **2027-08-31:** panel ≥10 contributors and ≥5 per DDR4/DDR5 cell; ~6 paying accounts |
| **Q4** m10–12 (Sep–Nov 2027) | Index API; clause-kit generator | Trade show m10. Free headline index monthly. **First licence m12** | **2027-11-30:** ≥9 accounts **and** MRR ≥$3k (75% of the model's 11.8 and ~$4.1k); ≥1 licence signed or LOI. Breakeven (founder unpaid) at m11 |
| **Q5** m13–15 (Dec 2027–Feb 2028) | Pooled-forecast portal (C-72, free in Pro) | §5949 goes live 2027-12-23: campaign to federal-adjacent OEMs | **2028-02-29:** ≥1 *paid* licence (else kill the index); ~19 accounts |
| **Q6** m16–18 (Mar–May 2028) | Down-adjustment calculator (the glut feature) | Push the index as the reference for refunds as prices turn | **2028-05-31:** BASE target 27 accounts, 2 licences, MRR ~$10.5k (ARR $126k). Full-time needs ≥52 accounts or 27 + 10 licences, **which the model does not reach until m26** |

---

## 9. Team required

| Role | When | Cost | Where to find |
|---|---|---|---|
| **Founder** (product, engineering, sales) | Now, ~15 h/week | Unpaid until the m26 full-time switch, then $10k/mo loaded | — |
| **Procurement advisor** (industrial-OEM or medtech supply-chain lead) | m0 | 0.25–0.5% equity [ESTIMATE] | Day-job network; AdvaMed supply-chain committees; East Coast ASCM/APICS chapters [UNVERIFIED chapter names]; kill-test interviewees |
| **Index-methodology advisor** (price statistician) | m6–9 | 0.5% equity or ~$2–5k [ESTIMATE] | Alumni of Fastmarkets, Platts/Argus or CRU (on LinkedIn), and former BLS PPI economists |
| **Government-contracts attorney** (contract) | m0 ($1k consult), m8 ($7k review) | $8k total (model) | Federal-procurement boutiques. Centre Law and Wiley publish on price adjustment and SBIR ([Centre Law](https://centrelawgroup.com/blog/gsa-flexibility-price-increases); [Wiley](https://www.wiley.law/alert-SBIR-STTR-Reauthorization-Brings-New-Opportunities-and-Obligations-to-Consider)) |
| **Part-time support contractor** (component-engineering literate) | From m5 | $60/h × 0.5 h per account-month (model) | Retired component engineers; CALCE alumni; contractor marketplaces |
| **LTB analyst** (contract) | From m6 | 30% of each $3,500 study (model) | Same pool; CALCE short-course alumni |
| **Sales/customer-success hire** | When MRR reaches $45k | $9k/mo loaded (model) | Ex-SiliconExpert, Z2Data or Supplyframe account reps. **BASE never reaches this trigger within 36 months** |

The team the bundle actually needs is **the founder plus two advisors and contractors**. That is both its strength (T0) and its ceiling.

---

## 10. The cheapest experiment that could kill it

**Budget ≈ $2,450 (cap $5,000). Duration 29 days: 2026-11-02 → decision on 2026-12-01. About 50 founder hours.**

**Step 0 (2026-11-02): write the thresholds below into a dated doc** and email it to the procurement advisor before any call. That locks them in.

**Step 1 (week 1, ~20 h): build two things.**

1. A "memory exposure scan" web page. It accepts a pasted BOM, classifies the memory part numbers (DDR3/4/5, LPDDR, eMMC, NOR, EEPROM), and pulls lifecycle and stock from the DigiKey API, whose 1,000 requests/day is enough. It flags CXMT/YMTC manufacturers for §5949 and computes 6-month LTB deadlines from any discontinuance notice.
2. A one-page "Memory Surcharge Reference v0": draft methodology plus a sample two-sided surcharge clause.

**Step 2 (weeks 1–3): outreach.**

- **Who:** 60 named contacts from §3 types (industrial/rugged PC, medtech, test equipment, EMS, CGP-member resellers) via Sales Navigator (~$100). Target **25 qualified 30-minute calls**, including **10 index prospects** (EMS, resellers, OEMs with surcharges).
- **On each call:** run the scan live, then make three asks:
  1. A **refundable $500 deposit, or a signed paid LOI**, for 6 months of Team at $249/mo.
  2. "Would you cite this index in a live surcharge or contract within 6 months?"
  3. "Will you contribute 24 months of anonymised memory PO prices?"
- **Also ask:** "What do you use today?"
- **Thank-you:** $50 per call ($1,250).

**Step 3 (days 2–10): data terms.** Send written questions to support@nexar.com and DigiKey's API team: may a third-party SaaS display your prices in-app, and may it use them historically?

**Step 4 (days 7–14): the C-72 calls.** Make three supplier calls (a Winbond or Nanya U.S. sales office, and a franchised Micron distributor). Ask: "Would you quote a pooled allocation agreement to a co-op that holds no title or credit?" A "yes" reopens C-72. A "no" closes it for good, at zero cost.

**Step 5 (days 14–24): legal.** A 2-hour consult with a government-contracts attorney (~$1,000) on two questions: can DLAD or GSAM price adjustments reference this index, and how should the contributed-price panel be designed to stay clear of antitrust risk?

**Step 6 (days 28–29): tally and decide.** Score each leg against the thresholds below. Domain and hosting ~$100.

**Pass/fail thresholds (decided now):**

| Test | Pass | Fail → action |
|---|---|---|
| K1: SaaS willingness to pay | ≥5 of 25 pay a deposit or sign a paid LOI at ≥$200/mo | **Kill the SaaS** |
| K2: substitution | <60% say SiliconExpert, Octopart or their EMS already covers it | Lifecycle becomes a free funnel only |
| K3: index adoption | ≥2 of 10 commit to cite it, and not all insist on TrendForce | **Kill the index** |
| K4: data moat | ≥5 OEMs commit PO history | **Kill the index** (no panel, no moat) |
| K5: data rights | Nexar or DigiKey permits in-app price display | Drop buy/hold pricing; lifecycle-only |
| K1 **and** K3 both fail | — | **Kill the whole bundle** |

---

## 11. Explicit kill criteria

1. **By 2026-12-01:** K1 fails (<5 of 25 deposits or paid LOIs at ≥$200/mo) → kill the SaaS.
2. **By 2026-12-01:** K3 fails (<2 of 10 index commitments) or K4 fails (<5 PO-history contributors) → kill the index.
3. **By 2026-12-01:** K1 and K3 both fail → **kill DD2 entirely**. Spend no more money.
4. **By 2026-12-15:** both Nexar and DigiKey refuse in-app price display in writing, or don't answer → drop all price features and keep lifecycle and index only.
5. **By 2026-12-01:** 0 of 3 suppliers will discuss a pooled allocation agreement → C-72 is closed permanently.
6. **By 2027-06-30 (m7):** fewer than 2 paying accounts (model: 2.8) → stop. The persona doesn't pay.
7. **By 2027-08-31 (m9):** fewer than 10 panel contributors, or counsel says the panel cannot be made antitrust-safe → kill the index.
8. **By 2027-11-30 (m12):** fewer than 9 paying accounts, or MRR below $3,000 → stop and put the code in maintenance. Either figure is ~75% of the model (11.8 accounts, ~$4.1k MRR); §2.3 shows a 30% shortfall never pays the founder.
9. **By 2028-02-29 (m15):** zero paid index licences → kill the index. The bundle reverts to C-80 + C-29, which the scorers rated "lead-gen, not a company".
10. **By 2028-05-31 (m18):**
    - Fewer than 20 accounts (75% of the model's 27) → open exit talks with Lytica, Z2Data, Accuris, Supplyframe or Luminovo.
    - Fewer than 35 accounts **and** fewer than 3 licences → no full-time switch at m18. This is the expected BASE outcome, and it stays a side business.
11. **By 2028-11-30 (m24):** ARR below $150,000 (22% under the model's BASE of $193,183 and 13% under its SEVERE path of $172,694) → sell or wind down.
12. **Any month from 2028-01:** price-motivated churn above 8%/month while lifecycle accounts are below 25 → the glut has broken the SaaS; go index-only.

---

## 12. Cycle test: the 2028–29 glut (DDR5 −60%) and the severe case

The model runs the same funnel through three DDR5 contract paths. All three start at $20.37/GB in Q4-2026 and reach $21.79 at end-2027. By Dec-2028 they reach $17.31 (BASE; $16.38 by Nov-2029), **$8.15 (GLUT, −60%, A-05)** and **$2.04 (SEVERE, −90%)**. At the glut price, incumbents still earn ~82% gross margin (`models/dram_cost_stack.py`; `01_LANDSCAPE.md` §0 item 5).

**Monthly revenue by module at m36 (2029-11)** (model §6):

| Module | BASE | GLUT | SEVERE | Mechanism |
|---|---|---|---|---|
| Buy/hold + allocation alerts (C-80 core) | $15,862 | $6,817 (**−57%**) | $2,300 (**−86%**) | Urgency falls with price; price-motivated accounts churn up to +8%/mo |
| EOL/lifecycle + NVM cross-ref + LTB sizer (C-80/C-29/C-61) | $13,696 | $13,696 (±0%) | $13,696 (±0%) | EOL-driven. Makers exit legacy lines faster in downturns (Nanya/Winbond in 2023, [DigiTimes, 2023-02-22](https://apps.digitimes.com/news/a20230222PD222/dram-nanya.html)), but budgets tighten, so it is held flat |
| Memory Cost Escalation Index (C-86) | $5,570 | $7,318 (**+31%**) | $7,488 (**+34%**) | Two-sided: buyers invoke down-adjustments; embedded clauses persist |
| LTB studies (C-61) | $5,682 | $5,331 (−6%) | $4,979 (−12%) | More EOL notices (+25%/+40%) offset by fewer accounts |
| Pooled forecast (C-72) | $0 | $0 | $0 | Allocation is free in a glut, so it is not monetised at all |

**Totals** (model §6):

- **ARR at m36:** $422k BASE, **$334k GLUT (−21%)**, **$282k SEVERE (−33%)**.
- **Accounts at m36:** 88, 61 and 48.
- **The revenue mix shifts:** price-driven SaaS falls from 39% of revenue (BASE) to 21% (GLUT) and 8% (SEVERE); the index share rises from 14% to 22% and 26%.
- **The salary is still covered** at m23 (GLUT) and m24 (SEVERE).
- **Cash at m36:** $187k (GLUT) and $156k (SEVERE).

**Verdict: the bundle survives a glut partially, and only because of the index and lifecycle legs.** C-80 alone (cycle score 1) would lose 57–86% of its revenue.

**Three honest caveats:**

1. **The full-time switch lands in the trough.** The model switches the founder to full-time at m26 (2029-01), exactly when GLUT bottoms. GLUT MRR at m26 is ~$18k and SEVERE ~$16k (model §5; unrounded $17,528 and $15,793, i.e. ARR ~$210k and ~$190k). Quitting a day job into a trough on that base is a judgment call the model cannot make.
2. **The index's glut upside is assumed, not observed.** No one has yet licensed a memory index. If counterparties revert to "no surcharge" once prices fall rather than claim refunds, the +31% becomes a loss. Licence churn also rises to 1.5%/month once prices go flat after m24.
3. **The flat lifecycle line may be generous.** OEM budgets shrink in downturns. A −20% lifecycle line in GLUT would cut m36 ARR by roughly a further $33k [ESTIMATE: 20% × $13,696 × 12].

---

## 13. Sources

Every URL below appears in `research/sources/*.jsonl`. Most entries were logged by `p4-lifecycle-intel`; the regulatory, SBIR and competitor-context entries were logged by `E`, `D`, `C`, `p3-audit-*`, `v1-policy` and `p4-provenance-recert`. All are search-snippet grade unless marked otherwise in the log.

**Competitors and pricing**
- https://www.siliconexpert.com/products/bom-manager/
- https://www.siliconexpert.com/bom-manager/
- https://accuristech.com/siliconexpert-offer-terms/
- https://accuristech.com/accuris-price-match-offer-terms/
- https://www.z2data.com/pricing
- https://www.cengn.ca/wp-content/uploads/2020/06/Lytica-Success-Story.pdf
- https://www.webull.com/news/15265411318440960
- https://intelligence.supplyframe.com/commodities-analyzed-sram-dram-specialty
- https://octopart.com/pulse/p/reducing-costs-efficient-bom-management
- https://www.renesas.com/en/about/newsroom/renesas-completes-acquisition-altium
- https://luminovo.com/faq/how-much-does-luminovo-cost
- https://luminovo.com/guides/2026-ems-memory-chip-risk-matrix
- https://luminovo.com/resources/blog/memory-chip-shortage
- https://giikorea.co.kr/annual/tdf225654-dramexchange-membership.html
- https://dramexchange.com/Service/Faqs
- https://counterpointresearch.com/en/reports/memory-price-tracker-and-forecast-july-2026
- https://github.com/search?q=dram+price&type=repositories
- https://github.com/nwfella/memory-price-index
- https://www.mobiusmaterials.com/post/inside-the-memory-supercycle-second-act

**Data access and lifecycle mechanics**
- https://nexar.com/compare-plans
- https://nexar.com/api/legal
- https://octopart.com/api/legal
- https://developer.digikey.com/documentation
- https://www.maxlinear.com/support/quality/policy-and-procedure
- https://boreas.ca/pages/product-life-cycle-policy
- https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/6778/PDN-202504001DN.pdf

**Buyer pain and surcharges**
- https://www.avnet.com/integrated/resources/article/memory-is-breaking-product-plans/
- https://www.advamed.org/2026/08/17/memory-chip-shortages-implications-for-medtech-innovation-and-patient-care/
- https://www.pwc.com/us/en/industries/health-industries/library/medtech-semiconductor-memory-shortage.html
- https://thecgp.org/images/2026/03/Letter-to-Larry-Hale-on-Memory-Chips.pdf
- https://www.unipi.technology/ram-surcharge
- https://revolutionpi.com/fileadmin/downloads/Informationsschreiben/eMMC_surcharge_07-26-en.pdf
- https://www.fastmarkets.com/products/price-data-how-to-use-it/

**Customers**
- https://www.thomasnet.com/articles/top-suppliers/industrial-computer-manufacturers-suppliers/
- https://www.trentonsystems.com/blog/list-of-rugged-server-manufacturers
- https://cpnorthamerica.com/?p=67
- https://www.arm.com/partners/catalog/winsystemsinc

**Regulation, contracts and funding**
- https://github.com/GSA/GSA-Acquisition-FAR/blob/master/dita/16.203-1.dita
- https://github.com/GSA/GSA-Acquisition-FAR/blob/master/dita/52.216-4.dita
- https://www.acquisition.gov/index%2ephp/dlad/subpart-16.2-%E2%80%93-fixed%E2%80%93price-contracts
- https://www.acquisition.gov/index%2ephp/dfarspgi/pgi-216.2-fixed-price-contracts
- https://www.acquisition.gov/gsam/552.238-120
- https://centrelawgroup.com/blog/gsa-flexibility-price-increases
- https://www.lewissilkin.com/insights/2026/05/11/when-hardware-costs-spike-what-your-tech-contracts-should-say
- https://fred.stlouisfed.org/series/PCU334413334413
- https://www.federalregister.gov/documents/2026/02/17/2026-03065/federal-acquisition-regulation-prohibition-on-certain-semiconductor-products-and-services
- https://www.iedconline.org/news/2026/04/15/federal-policy-updates/federal-policy-update-sbir-and-sttr-reauthorized/
- https://www.nist.gov/tpo/small-business-innovation-research-program-sbir/resources/participation-eligibility-and
- https://www.wiley.law/alert-SBIR-STTR-Reauthorization-Brings-New-Opportunities-and-Obligations-to-Consider
- https://calce.umd.edu/event/20069/electronic-part-obsolescence-forecasting-mitigation-and-management
- https://dair.nps.edu/handle/123456789/5619

**Price path and cycle**
- https://finance.technews.tw/2026/07/09/long-term-agreements-price-cap-3q26-server-dram-contract-price-estimated-13-18-qoq-increase/
- https://apps.digitimes.com/news/a20230222PD222/dram-nanya.html

**Models:** `models/lifecycle-intel.py` (this deep dive) and `models/dram_cost_stack.py` (DDR5 price deck).
