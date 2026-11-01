# DD2 — Memory Lifecycle & Cost Intelligence for OEMs (`lifecycle-intel`)

Author: `p4w-lifecycle-intel` · As of 2026-11-01 · Model: `models/lifecycle-intel.py` (Phase 5 red-team revisions applied and re-run 2026-11-01, exit 0; output in `research/phase4/lifecycle-intel_model_output.md`) · Red-team responses: `research/phase5/responses_lifecycle-intel.json` (§14) · Research notes: `research/phase4/lifecycle-intel_notes.md` · Every web fact below is search-snippet grade, so the best tag it can carry is **[REPORTED]**. Model figures are **[ESTIMATE]** by construction.


> **Phase 6 decision note (added after both red-team rounds).** The red team downgraded this deep dive to a side line, and that characterization stands. Because every other deep dive was killed (DD1, DD3, DD4, DD6, DD7) or downgraded (DD5), the Phase 6 judge panel selected it as **PRIMARY — the best available option, not a venture** (`research/phase6/decision.json`). Statements in §14 such as "side line, demoted from FALLBACK" or "run alongside DD1/DD3" predate that decision; DD1 and DD3 are now killed. The C-72 co-op is killed as a standalone concept (Rule 1, Phase 7 gate) and survives only as three $0 supplier calls inside §10.

---

## 0. Header

**Pitch.** A $249/month web app shows small U.S. hardware makers which memory chips in their products are about to go end-of-life, change die revision or spike in price. The Phase 4 plan then pooled their anonymised purchase prices into a licensed Memory Cost Escalation Index. **After the red team that index is only an option the kill test must earn: the SaaS funnel cannot fill its panel within 36 months (revised after red team, §14).**

**Anchor and folded concepts**

| Role | ID | Concept | Why it is here (scorer quotes, `research/phase3/scores_raw/*.json`) |
|---|---|---|---|
| Anchor | C-80 | DRAM Cost & Allocation Intelligence for SMB OEMs | Veteran: "use it only as a free lead-gen front end." Founder scorer: "Best founder-fit and fastest to ship, with the worst durability." |
| Folded (feature) | C-29 | NVM-EOL Migration Finder | Founder scorer: "a feature for C-80 or lead-gen for C-12, not a standalone business." VC: "lead-gen for C-12/C-80, not a company." |
| Folded (the durable leg; **killed as designed after red team, now an option**) | C-86 | Memory Cost Escalation Index + EPA clause kit | Veteran: "The best-shaped data product in my chunk because it is two-sided and its clauses persist through the glut." VC: "the ceiling is ~$0.3M ARR unless it wins that fight." |
| Folded (software only) | C-61 | DRAM Continuity Vault | Founder scorer: "The LTB-sizing software fits the founder, but the money is in a vault that loses money below ~8 OEMs." Only the last-time-buy (LTB) sizer and paid LTB studies are kept. **The vault is out.** |
| Folded (free feature + three phone calls) | C-72 | Legacy-DRAM buying co-op | Founder scorer: "Three supplier calls decide everything … A free kill test, not a venture." It becomes an unpriced pooled-forecast feature and three calls in §10. |

**Capital tier: T0, barely (revised after red team).** The revised model's worst cash point is $6,100 at m16, a maximum draw of **$33,900** of the founder's $40k (`models/lifecycle-intel.py` §6; Phase 4 had $18,049). A 30% miss on price, conversion or COGS, or Nexar and display fees of $1,000 and $2,500 a month, would exhaust the $40k (§2.3).

**Scores and ranks** (`scores.csv`; consensus of three scorers; out of 100, rank in parentheses)

| ID | Tier | Default | Capital-constrained | Moonshot | Moat / competition / cycle (1–5) |
|---|---|---|---|---|---|
| C-80 | T0 | 79.0 (5) | 82.5 (4) | 75.8 (5) | 1 / 1 / 1 |
| C-29 | T0 | 79.0 (4) | 82.5 (3) | 75.8 (4) | 1 / 1 / 3 |
| C-86 | T0 | 75.0 (8) | 78.3 (9) | 74.2 (7) | 3 / 3 / 4 |
| C-61 | T1 | 70.0 (16) | 70.8 (16) | 66.7 (13) | 3 / 2 / 4 |
| C-72 | T1 | 64.0 (20) | 65.8 (19) | 65.0 (15) | 2 / 3 / 1 |

The anchor ranks high only because it is cheap, fast and founder-shaped. It scores the floor (1) on moat, competition and cycle. The bundle existed to borrow C-86's moat and cycle scores. **The red team showed the index cannot be computed on the SaaS funnel and has no glut upside, so that borrowing failed (revised after red team).**

**Three verdicts (revised after red team; the Phase 4 verdicts are kept in §14.5)**

- **POSSIBLE? Yes for the SaaS; no for the index as designed (revised after red team).** The SaaS is TRL 9 software on public APIs and public PDN/PCN documents. The index needs a 15-member contributed-price panel to fill three grade-homogeneous cells, and the SaaS funnel supplies only 14 members by m36. It becomes possible only if the kill test signs at least 10 contributors who are not subscribers. Data rights for in-app prices (K5) remain the other open question.
- **PROFITABLE? No as a venture; marginal as a side business (revised after red team).**
  - BASE ARR is **$69,915 at m18 and $149,629 at m36** (GLUT $104,077, SEVERE $83,031).
  - Breakeven with the founder unpaid comes at **m17 (2028-04)**.
  - The $10k/month founder salary is **never** covered within 36 months, in any scenario.
  - By m36 the business earns ~$6.5k/month of profit for an unpaid part-time founder.
  - A 30% miss on price, conversion or COGS exhausts the $40k.
- **DOABLE BY THIS FOUNDER? Yes, conditionally (revised after red team).** It is pure software, part-time and T0. Two conditions apply:
  - Nothing may be built before the employer signs a written carve-out (K0).
  - The founder must book 25 qualified calls in 21 days from cold outreach outside the employer's network (K6).

  Part-time hours cap the funnel at ~20 trials a month. The founder still needs help with index methodology and with selling to procurement leads.

**Recommendation (revised after red team): side line, demoted from FALLBACK. FINAL STATUS: DOWNGRADED (§14).** No red-team objection was refuted, and the index leg as designed was killed. Run the ~$2,950 kill test in §10 only alongside DD1/DD3 customer discovery with the same SMB-OEM buyers. Stop if K0, K1 or K6 fails.

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
            v                                     - PDN and PCN notices (PDFs on distributor servers)
 [1] SCAN: find every memory part                 - Free DRAMeXchange spot prices (sanity check only)
     (DDR3/4/5, LPDDR, eMMC, NOR, EEPROM)
            |
            v
 [2] ALERTS: "Part X goes EOL; last order date is 6 months out; here are 3 alternates;
     part Y changed die revision under the same MPN (PCN); F-RAM candidate for this NVSRAM,
     validation required; brand-level §5949 screen only, not die-level"   <- revised after red team
            |
            v   (optional, 10% discount for joining)
 [3] POOL (an option only, after red team): line-item buyers share anonymised memory PO prices
     --> panel, >=5 companies per grade-homogeneous cell, >=15 members before publication
            |
            v
 [4] INDEX (an option only): quarterly Memory Cost Escalation Index, <=4 cells
     --> free headline number + paid licence
     + clause: "memory surcharge moves with the index, up AND down"
```

**Steps 1–2 are the subscription** ($249 or $649/month). They save engineering hours and catch last-time-buy deadlines. Under the J-STD-048 practice, a chip maker usually gives a 6-month window to place final orders after it announces a discontinuance ([MaxLinear](https://www.maxlinear.com/support/quality/policy-and-procedure); [Boréas](https://boreas.ca/pages/product-life-cycle-policy)) [REPORTED]. Miss that window and you redesign the board. Step 2 also folds in two smaller ideas:

- C-29: listing F-RAM or MRAM *candidates*, after parametric checks, when an NVSRAM or high-write EEPROM part dies. It never makes a drop-in recommendation, and NOR code storage is out of scope (revised after red team; RT-PHY-DD2-03, RT-VET-DD2-05).
- C-61's software: sizing how many chips to stockpile before the last order date, including storage, bake and attrition losses (revised after red team; RT-PHY-DD2-04).

**Steps 3–4 were the part that is not just a feature. After the red team they are an unproven option (revised after red team, §14).** Contract memory prices moved about 6× in five quarters (C-86 card, `research/phase2/concepts_master.json`). At swings like that, any fixed-price contract for computers either bleeds money or carries a fat contingency. Commodity markets solved this with licensed price references written into contracts ([Fastmarkets](https://www.fastmarkets.com/products/price-data-how-to-use-it/)) [REPORTED]. Memory has no *licensed contract-settlement* index, but it does have a de facto reference (revised after red team):

- The U.S. Bureau of Labor Statistics publishes no DRAM-specific producer price index ([FRED](https://fred.stlouisfed.org/series/PCU334413334413)) [REPORTED].
- TrendForce's DXI is a spot-market index, not a contract-settlement index ([DRAMeXchange FAQ](https://dramexchange.com/Service/Faqs)) [REPORTED].
- **But TrendForce/DRAMeXchange contract prints are what suppliers, module houses and large OEMs already negotiate against.** DRAMeXchange has used the 8GB module contract price as its contract-trend base since 2019 ([TrendForce, 2018-11-05](https://www.trendforce.com/presscenter/news/20181105-10065.html)) [REPORTED]. EMS houses pass turnkey memory through at invoice cost. Any index from this venture has to beat both (RT-HYP-DD2-03, RT-VET-DD2-02).

If a seller and buyer both agree to "surcharge = index change × memory content", the seller is protected when prices spike and the buyer gets a refund when prices crash. The Phase 4 plan claimed that two-way use makes this leg earn *more* in a glut. **The red team found no precedent: no index-linked memory down-adjustment surfaced for 2018–19 or 2023, so the model no longer assumes a glut uplift (revised after red team).** The only use that survives is an SMB OEM passing its own distribution-channel memory cost through to a customer who refuses open-book pass-through.

The memory-specific scope is what differs from SiliconExpert or Octopart. It includes die-revision PCNs under unchanged part numbers, which free lifecycle flags miss. The contributed-price panel would differ too, if it ever exists. Steps 1–2 alone are a feature those companies already sell.

---

## 2. Cost and unit-economics model

All figures come from `python3 models/lifecycle-intel.py` (BASE scenario unless stated) **with the Phase 5 red-team revisions applied (revised after red team)**. The Phase 4 figures are reproduced exactly in model §10 and summarised in §14.3. Model month 1 = 2026-12. The founder works ~15 h/week unpaid until the trailing three months of (gross profit − opex) reach $10k/month; in the revised model that never happens within 36 months. Phase 4 assumptions are in `research/assumptions/p4-lifecycle-intel.md`. The red-team changes are in the model's RED-TEAM REVISIONS block and `research/assumptions/p5r-lifecycle-intel.md`.

### 2.1 Pricing and unit economics per line (model §3)

| Line | Price | Variable COGS | Contribution margin | Price anchor |
|---|---|---|---|---|
| SaaS Team | $249/acct-mo | $59 | 76% | SiliconExpert BOM Manager Essentials $250/mo, 1 user, 1 BOM ≤500 parts ([SiliconExpert](https://www.siliconexpert.com/products/bom-manager/)) [REPORTED] |
| SaaS Pro (multi-BOM, LTB module) | $649/acct-mo | $97 | 85% | Accuris price match: minimum $6,000 ACV ([Accuris](https://accuristech.com/accuris-price-match-offer-terms/)) [REPORTED] |
| SaaS blended net | $340/acct-mo (revised after red team; was $335) | $69 | 80% | 25% Pro mix; 10% discount for the 25% of accounts that contribute prices (revised after red team; was 40%) [ESTIMATE] |
| Index Standard licence | $6,000/yr ($500/mo) | $75/mo | 85% | DRAMeXchange Silver $5k, Gold $11k ([GII](https://giikorea.co.kr/annual/tdf225654-dramexchange-membership.html)) [REPORTED]. **Not sold in the revised BASE: the index is never published within 36 months (revised after red team)** |
| Index Enterprise (redistribution/API) | $24,000/yr | $180/mo | 91% | DRAMeXchange DRAM&NAND Platinum $30k (same listing). Same caveat |
| LTB study (one-off) | $3,500 | $1,330 (revised after red team; was $1,155) | 62% (revised; was 67%) | 1.5–2 analyst-days plus a storage, bake and attrition section (RT-PHY-DD2-04) [ESTIMATE] |

**Acquisition cost (model §3; revised after red team):**

| Measure | Value |
|---|---|
| Cash CAC | **$911** per account (was $563): marketing plus $35 per qualified trial, spread over fewer conversions |
| Fully loaded CAC | **$1,661** (was $1,188; adds 1 founder-hour per trial at $75) |
| Lifetime at 2% monthly churn | ~50 months |
| LTV | $13,903 |
| LTV/CAC | 15.3 cash; **8.4 loaded** |
| Payback | 3.3 months cash; **6.0 months loaded** |

CAC is still not the problem. **Volume, price and the founder's part-time hours are.**

**Fixed data and infrastructure costs (inputs; revised after red team):**

| Item | Cost | Basis |
|---|---|---|
| Hosting | $150/mo | [ESTIMATE] |
| Nexar API, Standard tier | ~$600/mo (revised after red team; was $300) | Tier limits are published (Standard ≤2,000 matched parts) but prices still were not on 2026-11-01 ([Nexar](https://nexar.com/compare-plans)) [ESTIMATE: midpoint of $300 and the HYP stress value of $1,000] |
| Nexar API, Pro tier (from 60 accounts) | ~$2,000/mo (revised; was $1,000) | Same source; never triggered in the revised BASE [ESTIMATE] |
| Commercial display licence (from m12) | ~$2,000/mo (revised; was $1,000) | No quote exists; K5 now requires one of ≤$1,000 [ESTIMATE] |
| DRAMeXchange Silver, internal validation only (from m9) | $5,000/yr | GII listing above |
| Antitrust opinion and compliance (new after red team) | $5,000 once at m2; $400/mo from index publication | RT-HYP-DD2-07 [ESTIMATE]. The retainer never triggers in BASE, because the index is never published |

The recurring items sum to **$3,167/month from m12 (revised after red team; was $1,867)**. They are the largest COGS unknown and are UNVERIFIED.

**Blended gross margin including fixed data costs (model §3; revised after red team):**

- m12 (2027-11): **−13%** on $3,623/month of revenue (was 45% on $5,787).
- m18 (2028-05): **36%** on $7,625 (was 65% on $12,978).
- m24 (2028-11): 49% on $10,834 (was 71% on $19,219).
- m36 (2029-11): **57%** on $15,122 (was 74% on $40,811).

### 2.2 ARR, breakeven and cash under three price scenarios (model §6)

The DDR5 contract path is $20.37/GB in Q4-2026, rising to $21.79 through 2027. From 2028-01 it diverges by scenario:

- **BASE:** −15% by Dec-2028.
- **GLUT:** falls to $8.15 by Dec-2028 (−60%, ASSUMPTIONS A-05).
- **SEVERE:** falls to $2.04 (−90%).

The price inputs come from `models/dram_cost_stack.py` `ddr5_reference()`; the "rising through 2H27" path is TrendForce via [TechNews, 2026-07-09](https://finance.technews.tw/2026/07/09/long-term-agreements-price-cap-3q26-server-dram-contract-price-estimated-13-18-qoq-increase/) [REPORTED].

| Scenario | ARR m12 | ARR m18 | ARR m24 | ARR m36 | Breakeven, founder unpaid | Covers $10k/mo salary | Full-time from | Cash low point | Cash m36 |
|---|---|---|---|---|---|---|---|---|---|
| BASE | $27,359 | **$69,915** | $104,031 | **$149,629** | m17 (2028-04) | **never** | never | **$6,100 @ m16** | $76,410 |
| GLUT | $27,359 | $66,411 | $86,196 | $104,077 | m17 (2028-04) | never | never | $6,734 @ m16 | $46,779 |
| SEVERE | $27,359 | $63,862 | $75,607 | $83,031 | m17 (2028-04) | never | never | $7,062 @ m16 | $31,060 |

Every figure in this table is revised after red team. Phase 4 had BASE ARR of $126,068 at m18 and $421,548 at m36, salary coverage at m23 and a full-time switch at m26 (§14.3).

How to read the table:

- **First revenue lands at m6 (2027-05)** (revised after red team; was m5), inside the 18-month target.
- **Account counts:** BASE has 17 accounts at m18 and 37 at m36; at m36 GLUT has 25 and SEVERE 20.
- **No scenario sells an index licence.** The contributed-price panel reaches 9.3 members at m18 and 14.2 at m36, short of the 15 needed to publish (model §6).
- **The cash low falls at m16 in all three scenarios**, just after the price paths split at m14, so it barely moves with the cycle. The founder draws up to $33,900 of the $40k, and BASE cash is back above $40k only at m30.
- **ARR counts subscriptions and licences only.** LTB studies are one-off and appear in cash, not ARR.

### 2.3 Sensitivity (model §7; each input ×0.7 / ×1.3, all else BASE; revised after red team)

| Driver | ARR m36 at ×0.7 | ARR m36 at ×1.3 | Salary covered (×0.7 / ×1.3) | Cash low (×0.7 / ×1.3) |
|---|---|---|---|---|
| Price, all lines | $104,740 | $194,517 | never / never | **−$11,109** / $13,156 |
| Conversion/close rate | $104,740 | $200,710 | never / never | **−$4,943** / $10,770 |
| Churn | $165,201 | $135,999 | never / never | $6,412 / $5,788 |
| COGS | $149,629 | $149,629 | never / never | $13,852 / **−$6,383** |

- **No single ±30% move gets the founder paid within 36 months.** Covering the salary needs 1.51× the revised trial inflow, or 14.7% trial conversion instead of 10% (model §10).
- **The founder's $40k runs out on a 30% miss in price or conversion, or on 30% higher COGS** (revised after red team; Phase 4 said it was never exhausted). Nexar and display fees of $1,000 and $2,500 a month do the same (cash low −$1,884). The m9 and m12 kill criteria and the cash floor in §11 exist to stop before that point.

### 2.4 What must be true (model §8 and §10; revised after red team)

- **To pay the founder $10k/month:** at least **55 paying accounts, or ~31 accounts plus 10 index licences**. BASE has 17 accounts and no licences at m18 and 37 accounts at m36, so the founder stays part-time throughout.
- **To reach $1M ARR by m36:** SaaS trial inflow must be **3.3×** the revised level (~65 qualified trials/month part-time). That means ~238 accounts by m36 (model §8). The base is now an estimated 3,000 U.S. SMB OEMs, replacing the unsourced 6,000 (revised after red team), so that is **7.9% of the market**. The 3,000 is a bottom-up [ESTIMATE] from a third-party NAICS 334 firm count (RT-VC-DD2-04).
- **To reach $2M:** inflow must be **6.4×**, with ~478 accounts (15.9%).
- **Index-only equivalent:** 115 licences per $1M at $8,700/yr. The revised model sells at most 1.8 licences by m36 if 10 seed contributors deliver (2.8 only if the publication gate is also lowered to 10 contributors).
- **The kill test must show** at least 5 paid deposits from 25 qualified conversations (20%), which supports the revised 10% trial-to-paid conversion. It must also pass K0, K2b, K5 and K6 (§10).

**Bottom line (revised after red team):** in the expected case the index produces nothing. Without it, this is a **$0.1–0.3M ARR part-time side business**: $150k ARR in BASE at m36, $182k at 12% conversion and $318k at 15%.

---

## 3. Target customer and the first ten customers

**Buyer:** the procurement, supply-chain or component-engineering lead at a U.S. hardware maker with $1–50M a year of BOM spend, memory on every board, and 5–20-year product lives [ESTIMATE: buyer definition; model input `tam_us_smb_oems`]. Their pain is documented:

- **Medtech:** AdvaMed reports 75–80% of medtech products contain memory. Among its members, 75% report memory constraints, 88% price increases and 63% allocation problems ([AdvaMed, 2026-08-17](https://www.advamed.org/2026/08/17/memory-chip-shortages-implications-for-medtech-innovation-and-patient-care/)) [REPORTED].
- **Small buyers generally:** Luminovo cites 80–90% price spikes and says firms without cash to stockpile are squeezed out of allocation ([Luminovo](https://luminovo.com/resources/blog/memory-chip-shortage)) [REPORTED].

**Index buyer (narrowed after red team).** The core buyer is now an SMB OEM that passes its own distribution-channel memory cost through to customers who refuse open-book pass-through. Two former buyer groups are out (RT-VET-DD2-02, RT-HYP-DD2-02):

- EMS houses normally pass turnkey memory through at invoice cost under open-book terms.
- Large buyers negotiate against TrendForce contract prints.

Federal IT resellers remain a case-by-case prospect. In March 2026 the Coalition for Common Sense in Government Procurement (CGP) asked GSA for weekly economic price adjustments ([CGP letter](https://thecgp.org/images/2026/03/Letter-to-Larry-Hale-on-Memory-Chips.pdf)) [REPORTED].

**None of the companies below has been contacted. Each one is a hypothesis for §10.**

| # | Customer | Line | Why they buy | How to reach |
|---|---|---|---|---|
| 1 | The founder's employer (design/manufacturing company) | Design partner (unpaid), **only if the K0 carve-out names it** (revised after red team) | The persona itself | **Written carve-out first, before any code (K0, §10).** No day-job-peer trials unless the carve-out allows them |
| 2 | OnLogic / Logic Supply (South Burlington, VT) | Team → Pro | Industrial PCs with DDR4/eMMC-heavy BOMs, on the East Coast ([Thomasnet](https://www.thomasnet.com/articles/top-suppliers/industrial-computer-manufacturers-suppliers/)); the rebrand is [UNVERIFIED] | Sales Navigator to the purchasing/supply-chain manager; offer a free BOM scan; drivable for an on-site demo |
| 3 | Amplicon USA (Fairport, NY) | Team | Industrial computers and panel PCs (Thomasnet, same list) | Same; regional visit |
| 4 | Trenton Systems (U.S.-made rugged servers) | Pro | DoD-facing server DRAM on long-life programmes; §5949 exposure from 2027-12-23 ([Trenton list](https://www.trentonsystems.com/blog/list-of-rugged-server-manufacturers)) | Lead with the LTB sizer and die-revision PCN monitoring. The §5949 screen is brand-level only and is **not** part of the pitch (revised after red team, RT-PHY-DD2-01) |
| 5 | CP Tech USA (ex-Chassis Plans) | Pro | Rugged computers built in the U.S. ([CPNA](https://cpnorthamerica.com/?p=67)) | Same pitch as #4 |
| 6 | Core Systems USA | Pro | Rugged servers (Trenton list) | Same |
| 7 | WINSYSTEMS | Team + LTB study | Long-lifecycle embedded SBCs with DDR, eMMC and NOR; the NVM cross-reference fits ([Arm catalog](https://www.arm.com/partners/catalog/winsystemsinc)) | Component engineer; lead with an EEPROM/NOR→F-RAM swap report |
| 8 | Industrial Computers Inc. (Ann Arbor, MI) | Team | High-reliability industrial PCs (Thomasnet) | Sales Navigator; free scan |
| 9 | Mid-size East Coast medtech OEM (patient monitors, imaging carts, IVD analysers with embedded PCs) | Pro + LTB study | 63% report allocation problems (AdvaMed); legacy phase-outs force costly redesigns ([PwC, 2026-06](https://www.pwc.com/us/en/industries/health-industries/library/medtech-semiconductor-memory-shortage.html)) | AdvaMed and MDMA member directories; supply-chain committee contacts |
| 10 | Tier-2/3 U.S. EMS ($50–500M revenue [ESTIMATE: segment definition]) | Pro only (index removed after red team: open-book pass-through needs no index) | Reprices turnkey memory for its OEM customers. Lytica already sells into EMS through NEOTech, which proves the budget line exists ([PR](https://www.webull.com/news/15265411318440960)) | East Coast IPC/SMTA chapter meetings; the VP of materials |

**Index-licence shortlist.** All three are reached by direct email to the pricing or contracts lead, with the clause kit attached.

- **CGP-member GSA MAS IT hardware resellers.** They asked GSA for weekly adjustments. Find them on the GSA eLibrary hardware vendor lists.
- **Unipi (CZ).** Its two-part quote has carried a memory surcharge at cost since 2026-07-20, "reduced once memory prices normalize", with no named index ([Unipi](https://www.unipi.technology/ram-surcharge)) [REPORTED].
- **Revolution Pi/KUNBUS (DE).** It added an eMMC surcharge from 2026-07-10 ([notice](https://revolutionpi.com/fileadmin/downloads/Informationsschreiben/eMMC_surcharge_07-26-en.pdf)) [REPORTED].

**No U.S. OEM surcharge notice was found.** That is open gap #3 in the notes, and it is the single most worrying fact for the index. A Phase 5 search found only U.S. list-price hike notices that cite no index: Dell +15–20% from mid-December 2025, and Lenovo quotes expiring 2026-01-01 ([TrendForce, 2025-12-05](https://www.trendforce.com/news/2025/12/05/exclusive-memory-crunch-hits-pcs-dell-hikes-prices-15-20-mid-december-lenovo-from-january-2026/)) [REPORTED].

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
- **Index:** Standard $6,000/yr; Enterprise $24,000/yr. Offered only if the K4-gated index option re-opens (revised after red team).
- **LTB study:** $3,500.
- **Pooled forecast (C-72):** free inside Pro.

**Sales motion.**

- **SaaS:** scan → 14-day trial → founder demo (1 hour) → card payment. Monthly, cancel any time, matching SiliconExpert Essentials.
- **Index:** sold founder-to-procurement-lead, with a clause kit drafted by a government-contracts attorney. Every sale needs both contract parties' legal teams to accept it. That is why the revised model sells licences only after a 15-member panel exists, which never happens within 36 months in BASE, and then at most 0.4 a month at peak volatility (revised after red team; was from m12 at 0.6).

**First 90 days of selling** (selling starts with the kill test):

| Days | Dates | Actions | Measurable output |
|---|---|---|---|
| 1–30 | 2026-11-02 → 12-01 | K0 employer carve-out first. Then the kill test (§10): 60 contacts outside the employer's network, 25 calls booked within 21 days, deposits, index LOIs, contribution agreements, supplier calls | K0 signed; ≥5 deposits; ≥2 signed index LOIs; ≥10 signed contribution agreements (revised after red team) |
| 31–60 | 12-02 → 2027-01-01 | Turn deposits into 5 design partners with a written data-contribution agreement. Commission the written antitrust opinion on the cell rules (m2, $5k). Publish the first monthly memory note. Start the newsletter (target 150 subscribers) | 5 signed design-partner agreements; ≥3 BOMs uploaded |
| 61–90 | 2027-01-02 → 01-31 | Weekly design-partner calls on the MVP. Second note. Ask each partner for one referral. Build a waitlist for the m6 paid launch (revised after red team; was m5) | ≥10 waitlist accounts; ≥3 partners sharing 24 months of PO history |

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
2. **A two-sided contract index nobody else sells.** No memory escalation index or clause kit was found (one targeted search, 2026-11-01). TrendForce's DXI is a spot index without a contract-licensing programme. BLS has no DRAM PPI, which weakens the "use a BLS index first" default in federal contracting. **This condition is much weaker than it looked (revised after red team).** DRAMeXchange has used the 8GB module contract price as its contract-trend base since 2019 ([TrendForce, 2018-11-05](https://www.trendforce.com/presscenter/news/20181105-10065.html)) [REPORTED], and large buyers negotiate against those prints. EMS houses use open-book pass-through. The index must beat both, and on the SaaS funnel it cannot even be computed within 36 months (§14).
3. **Contributed transaction prices.** This is the Lytica pattern, applied only to memory. Lytica is the proof that "real customer pricing, not distributor list pricing" sells.

**Where it loses:**

- **On lifecycle alone.** SiliconExpert and Octopart already answer most of the question, and Octopart answers it for free. If a prospect has SiliconExpert, the SaaS is redundant.
- **On forecasts.** Supplyframe CIQ and Counterpoint have analysts and history; this venture would have neither.
- **On credibility.** Any counterparty can say "use TrendForce" or "pass it through at invoice cost", and an index from a one-person company is easy to dismiss. A panel of SMB distributor prices also mixes temperature grades and buyers unless it is cut into narrow cells (RT-PHY-DD2-02, RT-VET-DD2-01). Spot ran ~2× contract in 2026 (veteran scorer), so basis risk is real.
- **On distribution.** Arrow (SiliconExpert), Siemens (Supplyframe) and Renesas (Octopart) can bundle a memory module at zero marginal price.

The realistic upside exit is selling the panel and index to one of them (notes §7, path c).

---

## 6. IP position

**What the venture would own:**

1. **The contributed price panel.** Its value rests on contracts: each contributor grants a perpetual licence to use its anonymised, aggregated prices. This is the only real moat. **On the SaaS funnel the panel never reaches the 15 members needed to publish within 36 months, so the moat exists only if the kill test signs ≥10 non-subscriber contributors (revised after red team, §14).**
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
2. **Antitrust exposure from pooling competitors' prices.**
   - **Mitigation (revised after red team):** a written opinion approves the cell rules before any data arrives. The rules are ≥5 contributors per cell, a lag of at least one quarter, no contributor above 25% of a cell's weight, aggregates only, and no forward-looking data.
   - **Why counsel must sign off:** the 1996 safety zones were withdrawn in 2023, and DOJ's 2024 RealPage complaint targets pooled pricing data [UNVERIFIED-training].
   - **Model:** a $5k opinion at m2, the $7k review at m8, and $400/month of compliance from index publication.
3. **The founder's employment agreement.** Most employers' IP-assignment and moonlighting clauses would claim or bar a side business that serves their own industry. The founder needs written clearance before writing code [ESTIMATE: standard practice; contract not seen]. **This is now kill gate K0 (revised after red team, RT-VC-DD2-05).**
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
- **§5949.** From 2027-12-23, federal agencies may not buy products containing CXMT, YMTC or SMIC chips. FAR Case 2023-008 was proposed on 2026-02-17 and accepts supplier self-certification after "reasonable inquiry" ([Federal Register](https://www.federalregister.gov/documents/2026/02/17/2026-03065/federal-acquisition-regulation-prohibition-on-certain-semiconductor-products-and-services)) [REPORTED]. A BOM-level flag is a cheap feature here. But it reads the manufacturer field, so it is **a brand-level screen only, not die-level**: modules, eMMC and SSDs sold under Western brands can carry CXMT or YMTC die (revised after red team, RT-PHY-DD2-01). Do not build DD1's provenance business inside this one.
- **Antitrust** on contributed prices (§6). **Export:** EAR99 software, no constraint.

**Non-dilutive money.** Expect **$0 in the first 24 months.**

- **SBIR is closed to the founder.** SBIR/STTR is reauthorized through 2031-09-30 ([IEDC, 2026-04-15](https://www.iedconline.org/news/2026/04/15/federal-policy-updates/federal-policy-update-sbir-and-sttr-reauthorized/)). But **the SBIR principal investigator must spend more than half their time at the small business**, so a founder who keeps a day job cannot be PI ([NIST](https://www.nist.gov/tpo/small-business-innovation-research-program-sbir/resources/participation-eligibility-and)) [REPORTED].
- **STTR is the only plausible route,** with a university PI. The natural partner is UMD CALCE (Prof. Peter Sandborn), which teaches obsolescence forecasting and lifetime-buy optimisation ([CALCE](https://calce.umd.edu/event/20069/electronic-part-obsolescence-forecasting-mitigation-and-management)), for a DMSMS/LTB forecasting module. **No current DMSMS forecasting topic was found.** The Naval Postgraduate School's 2025-12 regression work shows the Navy is interested ([NPS](https://dair.nps.edu/handle/123456789/5619)).
- **CHIPS money: none.** It does not fit.

**Raise?** **No.** The revised model draws up to $33.9k of the $40k, and investors will see a $0.15M-ARR BASE (revised after red team; Phase 4 said $18k and a $0.4M ceiling). Reconsider only if, by 2028-05, the index has at least 10 licences or one enterprise redistribution deal with an EMS network or distributor. That would make the "reference index" path real, and a $0.5–1M angel round [ESTIMATE: ~2 years of founder plus seller at the model's $10k + $9k/mo loaded] could fund a full-time founder plus a seller. Otherwise the endgame is either a profitable side business or a sale of the panel to Lytica, Z2Data, Accuris, Supplyframe or Luminovo.

---

## 8. 18-month roadmap with milestones

Model month m1 = 2026-12. Account and MRR targets are the model's BASE path (§4 of the model output).

| Period | Build | Sell / data | Gate (date: measurable test) |
|---|---|---|---|
| **m0** (Nov 2026) | Nothing until K0 is signed; then the scan prototype (~20 h) | Kill test (§10) | **2026-12-01:** K0–K6 pass, or kill the named leg (revised after red team) |
| **Q1** m1–3 (Dec 2026–Feb 2027) | MVP: BOM upload, memory MPN classifier, PDN **and PCN (die-revision, fab-transfer)** crawler, alerts on the DigiKey API | 5 design partners; contribution agreements; written antitrust opinion (m2, $5k) | **2027-02-28:** 5 partners active weekly; ≥3 sharing PO history; **cell map of the partners' memory spend (PHY-02 test) and NVM swap check (VET-05 test)** (revised after red team) |
| **Q2** m4–6 (Mar–May 2027) | Team/Pro billing | **Paid launch m6 (2027-05)** (revised; was m5); 4–8 trials/month | **2027-05-31:** paid launch done; ≥3 of 5 partners still active |
| **Q3** m7–9 (Jun–Aug 2027) | LTB sizer with storage and attrition inputs, back-tested on one partner's past LTB; NVM candidate filter (NVSRAM and high-write EEPROM only); brand-level §5949 screen | Legal review at m8 ($7k). **Index methodology published only if the VET-01 test passes on the K4 histories** (revised; was unconditional at m9) | **2027-08-31:** ≥2 paying accounts (model: 2.7) (revised) |
| **Q4** m10–12 (Sep–Nov 2027) | Index API and clause-kit generator, only if the index is published | Trade show m10. Free monthly market note | **2027-11-30:** ≥5 accounts **and** MRR ≥$1,700, ~75% of the model's 6.7 accounts and $2,280 (revised; was 9 accounts and $3k) |
| **Q5** m13–15 (Dec 2027–Feb 2028) | Pooled-forecast portal (C-72, free in Pro) | §5949 goes live 2027-12-23: brand-level screen campaign, with die-level referral to DD1 | **2028-02-29:** the index option closes unless the panel has ≥15 members with usable histories (model: 8.0) **or** one executed contract or published surcharge schedule names the index (revised) |
| **Q6** m16–18 (Mar–May 2028) | Down-adjustment calculator, only if the index is live | Breakeven with the founder unpaid expected at m17 | **2028-05-31:** BASE target 17 accounts, MRR ~$5.8k (ARR $70k) (revised). Full-time needs ≥55 accounts, **which the revised model never reaches within 36 months** |

---

## 9. Team required

| Role | When | Cost | Where to find |
|---|---|---|---|
| **Founder** (product, engineering, sales) | Now, ~15 h/week | Unpaid throughout: the revised model never reaches the full-time switch within 36 months (revised after red team; was m26) | — |
| **Procurement advisor** (industrial-OEM or medtech supply-chain lead) | m0 | 0.25–0.5% equity [ESTIMATE] | Day-job network; AdvaMed supply-chain committees; East Coast ASCM/APICS chapters [UNVERIFIED chapter names]; kill-test interviewees |
| **Index-methodology advisor** (price statistician) | m6–9 | 0.5% equity or ~$2–5k [ESTIMATE] | Alumni of Fastmarkets, Platts/Argus or CRU (on LinkedIn), and former BLS PPI economists |
| **Government-contracts attorney** (contract) | m0 ($1k consult), m2 ($5k written antitrust opinion), m8 ($7k review); $400/mo retainer if the index launches | $13k plus the retainer (revised after red team; was $8k) | Federal-procurement boutiques. Centre Law and Wiley publish on price adjustment and SBIR ([Centre Law](https://centrelawgroup.com/blog/gsa-flexibility-price-increases); [Wiley](https://www.wiley.law/alert-SBIR-STTR-Reauthorization-Brings-New-Opportunities-and-Obligations-to-Consider)) |
| **Part-time support contractor** (component-engineering literate) | From m6 (revised after red team; was m5) | $60/h × 0.5 h per account-month (model) | Retired component engineers; CALCE alumni; contractor marketplaces |
| **LTB analyst** (contract) | From m7, after the sizer back-test (revised after red team) | 30% of each $3,500 study (model) | Same pool; CALCE short-course alumni |
| **Founder's own employment attorney** (new after red team) | m0 | ~$500 | Reviews the employment agreement before the K0 carve-out request |
| **Sales/customer-success hire** | When MRR reaches $45k | $9k/mo loaded (model) | Ex-SiliconExpert, Z2Data or Supplyframe account reps. **BASE never reaches this trigger within 36 months** |

The team the bundle actually needs is **the founder plus two advisors and contractors**. That is both its strength (T0) and its ceiling.

---

## 10. The cheapest experiment that could kill it

**Budget ≈ $2,950 (cap $5,000) (revised after red team; was $2,450). Duration 29 days: 2026-11-02 → decision on 2026-12-01. About 55 founder hours.**

**Step 0 (2026-11-02): write the thresholds below into a dated doc** and email it to the procurement advisor before any call. That locks them in.

**Step 0b (2026-11-02 → 11-09): employer carve-out, K0 (new after red team, RT-VC-DD2-05).**

- Have the employment agreement reviewed (~$500).
- Ask the employer for a written carve-out covering the product, the target industry and third-party PO contributions.
- **No code is written until the carve-out is signed.** If it is refused, DD2 is dead for this founder and every later step is cancelled.

**Step 1 (week 2, ~20 h): build two things.**

1. A "memory exposure scan" web page.
   - It accepts a pasted BOM and classifies the memory part numbers (DDR3/4/5, LPDDR, eMMC, NOR, EEPROM).
   - It pulls lifecycle and stock from the DigiKey API, whose 1,000 requests/day is enough.
   - For each part it lists any PDN or die-revision PCN found, and computes 6-month LTB deadlines from any discontinuance notice.
   - It runs a **brand-level** §5949 screen labelled "not die-level; a negative is not evidence of compliance" (revised after red team).
2. A one-page "Memory Surcharge Reference v0": a draft methodology for ≤4 grade-homogeneous quarterly cells plus a sample two-sided surcharge clause (revised after red team).

**Step 2 (weeks 1–3): outreach.**

- **Who:** 60 named contacts from §3 types (industrial/rugged PC, medtech, test equipment, EMS, CGP-member resellers) via Sales Navigator (~$100).
  - **None may come from the employer's network** (revised after red team).
  - Target **25 qualified 30-minute calls booked within 21 days** (K6), including **10 index prospects** (OEMs with surcharges, resellers).
- **On each call:** run the scan live, then make three asks:
  1. A **refundable $500 deposit, or a signed paid LOI**, for 6 months of Team at $249/mo.
  2. For index prospects, a **signed LOI naming a live contract or surcharge schedule** that would cite the index. It must state why TrendForce contract prints and open-book pass-through don't serve that contract (revised after red team).
  3. A **contribution agreement for 24 months of line-item memory PO prices** (revised after red team). The company's legal or contracts function must sign it, confirm there is no supplier-confidentiality conflict, and accept the antitrust cell rules.
- **Also ask:**
  - "What do you use today?"
  - "Name a memory EOL, LTB deadline or die-revision PCN you missed in 2025–26 with your current tools." (K2b)
  - "Did your 2026 DRAM last-time buys fill at ≥90% of the quantity you asked for?"
  - For contributors: which part, density and temperature-grade cells make up their memory spend.
- **Contributors need not be subscribers.** The target is ≥10 signed agreements independent of SaaS deposits (revised after red team).
- **Thank-you:** $50 per call ($1,250).

**Step 3 (days 2–10): data terms.** Send written questions to support@nexar.com and DigiKey's API team (revised after red team):

- May a third-party SaaS display your prices and stock in-app?
- May it use them historically?
- **What does that licence cost per month?**

**Step 4 (days 7–14): the C-72 calls.** Make three supplier calls (a Winbond or Nanya U.S. sales office, and a franchised Micron distributor). Ask: "Would you quote a pooled allocation agreement to a co-op that holds no title or credit?" A "yes" reopens C-72. A "no" closes it for good, at zero cost.

**Step 5 (days 14–24): legal.** A 2-hour consult with a government-contracts attorney (~$1,000) on two questions (revised after red team):

- Can DLAD or GSAM price adjustments reference this index?
- Will the proposed cell rules keep the panel clear of antitrust risk? The rules are ≥5 contributors per cell, a lag of at least one quarter, no contributor above 25% of a cell, and aggregates only.

**Step 6 (days 28–29): tally and decide.** Score each leg against the thresholds below. Domain and hosting ~$100.

**Pass/fail thresholds (decided now; revised after red team):**

| Test | Pass | Fail → action |
|---|---|---|
| **K0: employer carve-out** (new) | Written carve-out signed, covering product, industry and third-party PO contributions | **Kill DD2 for this founder**; build nothing |
| K1: SaaS willingness to pay | ≥5 of 25 pay a deposit or sign a paid LOI at ≥$200/mo | **Kill DD2** (revised: an index-only business sells ≤3 licences by m36, so K1 failing alone now kills the bundle) |
| K2: substitution | <60% say SiliconExpert, Octopart or their EMS already covers it, **and (K2b, new) ≥10 of 25 name a specific memory EOL, LTB deadline or die-revision PCN they missed in 2025–26** | Lifecycle becomes a free funnel only |
| K3: index adoption | ≥2 of 10 **signed LOIs naming a live contract or surcharge schedule**, each stating why TrendForce prints and open-book pass-through don't serve it (revised; was a verbal "would cite") | **Close the index option** |
| K4: data moat | **≥10 signed contribution agreements** (revised; was ≥5 verbal commitments). Each: signed by the legal function, line-item POs, ≥$250k/yr memory spend, not EMS-turnkey, no confidentiality conflict. **And** the cell map puts ≥70% of memory spend in ≤4 grade-homogeneous cells, ≥3 of which can reach 5 contributors | **Close the index option** (no panel, no moat) |
| K5: data rights | Nexar or DigiKey permits in-app price/stock display in writing, **with a quote of ≤$1,000/month** (revised) | Run the price line on public market prints only and re-run K1 on a demo without distributor prices; if K1 then fails, **kill DD2** (revised) |
| **K6: funnel volume** (new) | 25 qualified calls booked within 21 days from cold outreach outside the employer's network | **Kill DD2**: the part-time funnel volume is not reachable |

---

## 11. Explicit kill criteria (revised after red team)

1. **Before any code (target 2026-11-09):** K0 fails (no written employer carve-out) → **kill DD2 for this founder**.
2. **By 2026-12-01:** K1 fails (<5 of 25 deposits or paid LOIs at ≥$200/mo), or K6 fails (<25 qualified calls booked in 21 days) → **kill DD2 entirely**. Spend no more money.
3. **By 2026-12-01:** K3 fails (<2 signed LOIs naming a live contract or surcharge schedule), or K4 fails (<10 legal-signed contribution agreements, or the cell map fails) → close the index option for good. The bundle continues as SaaS only, which is the revised BASE.
4. **By 2026-12-15:** neither Nexar nor DigiKey grants in-app price display in writing at ≤$1,000/month → run the price line on public prints only and re-test K1 on that demo; if K1 then fails, kill DD2. The revised model's K5-fail case is $69,289 ARR at m36 with a $947 cash low.
5. **By 2026-12-01:** 0 of 3 suppliers will discuss a pooled allocation agreement → C-72 is closed permanently.
6. **By 2027-02-28 (m3):** two design-partner BOM tests.
   - If <70% of memory spend falls in ≤4 grade-homogeneous cells → close the index option.
   - If no BOM has an EOL NVM part with a pin-compatible F-RAM/MRAM alternate within 3× the price → drop the C-29 feature.
7. **By 2027-08-31 (m9):** fewer than 2 paying accounts (model: 2.7) → stop. The persona doesn't pay. (Revised; this was m7 with a model figure of 2.8, before launch moved to m6.)
8. **By 2027-08-31 (m9):** applies only if the index option is still open. Close it if either:
   - the K4 histories fail the VET-01 test: ≥3 cells with ≥5 independent buyers in ≥80% of quarters, and bootstrapped noise below one-third of the TrendForce contract move; or
   - counsel says the panel cannot be made antitrust-safe.
9. **By 2027-11-30 (m12):** fewer than 5 paying accounts, or MRR below $1,700 → stop and put the code in maintenance. Either figure is ~75% of the revised model (6.7 accounts, $2,280 MRR). (Revised; was 9 accounts and $3,000.)
10. **Any month before breakeven:** cash below $5,000 → stop, and put in no more than the $40k (new; the revised cash low is $6,100 at m16).
11. **By 2028-02-29 (m15):** the index option closes unless the panel has ≥15 members with usable histories (model: 8.0), **or** one executed contract or published surcharge schedule between unaffiliated parties names the index (RT-HYP-DD2-03).
12. **By 2028-05-31 (m18):** fewer than 13 accounts (75% of the revised model's 17) → open exit talks with Lytica, Z2Data, Accuris, Supplyframe or Luminovo. No full-time switch is expected: the revised model never covers the salary within 36 months.
13. **By 2028-11-30 (m24):** ARR below $78,000 (75% of the revised BASE of $104,031) → sell or wind down. (Revised; was $150,000.)
14. **Any month from 2028-01:** price-motivated churn above 8%/month while lifecycle accounts are below 15 (model at m24: 10.7) → the glut has broken the price line. Run lifecycle-only and check that it still covers its costs. (Revised; this used to say "go index-only", and that path no longer exists.)

---

## 12. Cycle test: the 2028–29 glut (DDR5 −60%) and the severe case (revised after red team)

The model runs the same funnel through three DDR5 contract paths. All three start at $20.37/GB in Q4-2026 and reach $21.79 at end-2027. By Dec-2028 they reach $17.31 (BASE; $16.38 by Nov-2029), **$8.15 (GLUT, −60%, A-05)** and **$2.04 (SEVERE, −90%)**. At the glut price, incumbents still earn ~82% gross margin (`models/dram_cost_stack.py`; `01_LANDSCAPE.md` §0 item 5).

**Monthly revenue by module at m36 (2029-11)** (model §6; revised after red team):

| Module | BASE | GLUT | SEVERE | Mechanism |
|---|---|---|---|---|
| Buy/hold + allocation alerts (C-80 core) | $6,695 | $2,899 (**−57%**) | $1,145 (**−83%**) | Urgency falls with price; price-motivated accounts churn up to +8%/mo |
| EOL/lifecycle + die-revision PCNs + NVM candidates + LTB sizer (C-80/C-29/C-61) | $5,774 | $5,774 (±0%) | $5,774 (±0%) | EOL-driven. Makers exit legacy lines faster in downturns (Nanya/Winbond in 2023, [DigiTimes, 2023-02-22](https://apps.digitimes.com/news/a20230222PD222/dram-nanya.html)), but budgets tighten, so it is held flat |
| Memory Cost Escalation Index (C-86) | $0 | $0 | $0 | **Never published within 36 months** (panel 14.2 < 15). Where seeded, falling prices now add no demand and licences churn 3%/month while prices fall (RT-VET-DD2-03) |
| LTB studies (C-61) | $2,653 | $2,706 (+2%) | $2,715 (+2%) | More EOL notices (+25%/+40%) offset by fewer accounts |
| Pooled forecast (C-72) | $0 | $0 | $0 | Allocation is free in a glut, so it is not monetised at all |

**Totals** (model §6; revised after red team):

- **ARR at m36:** $150k BASE, **$104k GLUT (−30%)**, **$83k SEVERE (−45%)**. Phase 4 had $422k, $334k and $282k.
- **Accounts at m36:** 37, 25 and 20.
- **Revenue mix at m36:** price-driven SaaS falls from 44% of revenue (BASE) to 25% (GLUT) and 12% (SEVERE). The index share is 0% in all three.
- **The salary is never covered** in any scenario.
- **Cash at m36:** $76k (BASE), $47k (GLUT) and $31k (SEVERE).

**Verdict (revised after red team): the bundle does not survive a glut as a business that pays the founder.** It survives only as part-time side income of ~$100k ARR, held up by the lifecycle line and LTB studies. The index is no glut hedge (RT-HYP-DD2-05, RT-VET-DD2-03):

- On the Phase 4 inputs alone, removing the assumed glut uplift cuts GLUT m36 ARR from $334k to $247k.
- Removing the index entirely gives $156k, with the founder never paid.

**Four honest caveats (revised after red team):**

1. **The founder never goes full-time**, so the Phase 4 worry about quitting a day job into the trough is moot. The new worry is the opposite: three years of unpaid part-time work for ~$6.5k/month of profit by m36 in BASE, and ~$3.5k in GLUT (model §5, m35→m36 cash change).
2. **The index's glut upside was assumed, not observed, and it has now been removed.** No index-linked memory down-adjustment was found for 2018–19 or 2023 ([TrendForce, 2018-11-05](https://www.trendforce.com/presscenter/news/20181105-10065.html); [TechNews, 2019-08-01](https://finance.technews.tw/2019/08/01/dram-july-contract-price-fell-more-than-10percent/)) [REPORTED].
3. **The flat lifecycle line may still be generous.** A −20% lifecycle line in GLUT would cut m36 ARR by a further ~$14k [ESTIMATE: 20% × $5,774 × 12].
4. **The DDR5 contract path is only a proxy** for these buyers. They mostly buy industrial DDR3/DDR4, eMMC and NOR, whose prices move with EOL and allocation (RT-PHY-DD2-02).

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

**Red team (Phase 5), logged by `p5r-lifecycle-intel`**
- https://www.trendforce.com/news/2025/12/05/exclusive-memory-crunch-hits-pcs-dell-hikes-prices-15-20-mid-december-lenovo-from-january-2026/
- https://revolutionpi.com/shop/en/ram-surcharge/
- https://www.trendforce.com/presscenter/news/20181105-10065.html
- https://finance.technews.tw/2019/08/01/dram-july-contract-price-fell-more-than-10percent/
- https://data.mewayz.com/industry/334
- https://www.bls.gov/iag/tgs/iag334.htm
- https://nexar.com/compare-plans (re-checked 2026-11-01: prices still unpublished)

**Models:** `models/lifecycle-intel.py` (this deep dive) and `models/dram_cost_stack.py` (DDR5 price deck).

---

## 14. Red-team outcome

Phase 5, 2026-11-01. Owner: `p5r-lifecycle-intel`. Four adversarial reviewers attacked this deep dive:

- **VET:** a 30-year DRAM process veteran.
- **VC:** a semiconductor VC who lost money on memory startups.
- **HYP:** a hyperscaler procurement lead.
- **PHY:** a condensed-matter physicist.

They raised **24 objections against DD2: 1 FATAL, 14 MAJOR, 9 MINOR**. The objections are in `research/phase5/rt_*.json`, and every response is recorded verbatim in `research/phase5/responses_lifecycle-intel.json`. Each quantitative objection was re-run in the model. Model §10 reproduces the Phase 4 output exactly and shows each reviewer's variant.

**Dispositions: 0 REFUTED · 7 ACCEPTED-MITIGATED · 15 ACCEPTED-DOWNGRADE · 2 ACCEPTED-KILL.**

### 14.1 Objections and dispositions

| Objection | Severity | Disposition | One-line action |
|---|---|---|---|
| RT-VC-DD2-01 | FATAL | ACCEPTED-KILL | SaaS-fed index killed: the 15-member panel gate is never met in 36 months; the index survives only as a K4-gated option |
| RT-HYP-DD2-01 | MAJOR | ACCEPTED-KILL | Same finding: index sales gated on panel size; the old m9 gate was replaced |
| RT-HYP-DD2-02 | MAJOR | ACCEPTED-DOWNGRADE | Index re-scoped to distribution-channel OEM surcharges; EMS-turnkey buyers excluded; contributor share 0.40→0.25 |
| RT-HYP-DD2-03 | MAJOR | ACCEPTED-DOWNGRADE | "No such index" corrected to TrendForce contract prints; K3 needs signed LOIs; m15 executed-contract test; index rate 0.60→0.40 |
| RT-HYP-DD2-04 | MAJOR | ACCEPTED-DOWNGRADE | Trial conversion 0.12→0.10; new K2b missed-EOL/PCN test |
| RT-HYP-DD2-05 | MAJOR | ACCEPTED-DOWNGRADE | Glut verdict changed: no index glut hedge; GLUT m36 ARR $104k and the founder is never paid |
| RT-HYP-DD2-06 | MINOR | ACCEPTED-DOWNGRADE | Nexar $300→$600, display licence $1,000→$2,000; K5 needs a quote of ≤$1,000/mo |
| RT-HYP-DD2-07 | MINOR | ACCEPTED-MITIGATED | $5k written antitrust opinion at m2, $400/mo compliance, cell rules built into K4 |
| RT-PHY-DD2-01 | MAJOR | ACCEPTED-MITIGATED | §5949 flag relabelled brand-level only and removed from the pitch to customers #4–6 |
| RT-PHY-DD2-02 | MAJOR | ACCEPTED-DOWNGRADE | Index limited to ≤4 grade-homogeneous quarterly cells; m3 cell-map test |
| RT-PHY-DD2-03 | MINOR | ACCEPTED-MITIGATED | Parametric checks and a "candidate only" disclaimer on every NVM pair |
| RT-PHY-DD2-04 | MINOR | ACCEPTED-MITIGATED | LTB sizer gains storage and attrition inputs; study COGS 30%→35%; back-test before selling |
| RT-PHY-DD2-05 | MINOR | ACCEPTED-MITIGATED | Die-revision PCN parsing in the MVP; launch m5→m6; "PDN only" claim until back-tested |
| RT-VC-DD2-02 | MAJOR | ACCEPTED-DOWNGRADE | Pre-licence back-test against TrendForce; K3 needs both contract parties' written agreement |
| RT-VC-DD2-03 | MAJOR | ACCEPTED-DOWNGRADE | K5 tightened; K5-fail variant ($69k ARR at m36) means K1 is re-tested or DD2 dies |
| RT-VC-DD2-04 | MAJOR | ACCEPTED-DOWNGRADE | TAM 6,000→3,000 [ESTIMATE]; $1M ARR needs 7.9% penetration (model §8); ceiling $0.1–0.3M |
| RT-VC-DD2-05 | MAJOR | ACCEPTED-DOWNGRADE | New K0 employer carve-out before any code; launch trials 6→4 |
| RT-VC-DD2-06 | MINOR | ACCEPTED-DOWNGRADE | Part-time trial cap 25→20; new K6 call-booking test |
| RT-VET-DD2-01 | MAJOR | ACCEPTED-DOWNGRADE | Quarterly index; the VET publication test replaces the m9 gate |
| RT-VET-DD2-02 | MAJOR | ACCEPTED-DOWNGRADE | EMS removed as an index target; K3 LOIs must say why TrendForce and open-book don't serve |
| RT-VET-DD2-03 | MAJOR | ACCEPTED-DOWNGRADE | Falling prices add no index demand; licences churn 3%/mo while prices fall |
| RT-VET-DD2-04 | MINOR | ACCEPTED-DOWNGRADE | Contributor share 0.40→0.25; K4 needs legal-function signatures |
| RT-VET-DD2-05 | MINOR | ACCEPTED-MITIGATED | C-29 narrowed to NVSRAM and high-write EEPROM; m3 swap test, else drop |
| RT-VET-DD2-06 | MINOR | ACCEPTED-MITIGATED | LTB studies re-scoped to allocation split and storage; attach rate 1.5%→1.25% |

### 14.2 Changes made

**Model** (`models/lifecycle-intel.py`, RED-TEAM REVISIONS (Phase 5) block; re-run with exit 0; output overwritten in `research/phase4/lifecycle-intel_model_output.md`)

- **Inputs changed (old → new):**
  - Funnel: trial_conversion 0.12→0.10; trials_cap_pt 25→20; trials_at_launch 6→4; saas_launch_month 5→6.
  - Index panel: contributor_share 0.40→0.25; seed_contributors 0→5; panel_min_contributors 0→15.
  - Index demand: index_rate 0.60→0.40; vol_down_weight 1.0→0.0; index_churn_falling 0.008→0.03.
  - Data costs: nexar_standard $300→$600; nexar_pro $1,000→$2,000; display_licence $1,000→$2,000.
  - Antitrust: antitrust_opinion $0→$5,000 (m2); antitrust_compliance_month $0→$400.
  - LTB: ltb_cogs_share 0.30→0.35; ltb_attach 0.015→0.0125.
  - Market: tam_us_smb_oems 6,000→3,000.
- **Structural changes:**
  - A panel gate on index publication and sales.
  - A signed price move, so falls are weighted separately from rises.
  - Higher licence churn while prices fall.
  - A price-line switch for the K5-fail case.
  - `ov=` overrides, so model §10 shows 29 scenario runs: the Phase 4 inputs (identical to the old output), the revised baseline, and the reviewer and stress variants. (The Phase 7 gate later appended 8 PLAN-variant rows for the Phase 6 decision, so §10 now has 37 rows; BASE and the 29 Phase 5 rows are unchanged.)

**Plan**

- **The index (C-86) as designed is killed.** It is now an option, re-opened only by the revised K4 and closed for good at m15 unless a panel or an executed contract exists (§10, §11).
- **Index scope narrowed** to ≤4 grade-homogeneous quarterly cells for OEM-to-customer surcharges. EMS, LTA and most federal uses are dropped (§1, §3, §5).
- **Kill test reworked:**
  - New gates: K0 (employer carve-out before any code), K2b (missed EOL or PCN), K6 (call booking).
  - K1 failing alone now kills DD2.
  - K3, K4 and K5 are tightened (§10).
- **Kill criteria** re-based on the revised model, with a new cash floor (§11).
- **Features corrected** (§1, §3, §8):
  - The §5949 flag is relabelled brand-level only.
  - The NVM cross-reference gets parametric checks and a narrower scope.
  - The LTB sizer gets storage physics.
  - Die-revision PCN parsing is added to the MVP.
- **Recommendation** demoted from FALLBACK to side line (§0).

### 14.3 Revised headline economics (model §6, §9, §10)

| Scenario | ARR m18 | ARR m36 | Breakeven, founder unpaid | Covers $10k salary | Founder full-time | Cash low | Phase 4 ARR m18 / m36 |
|---|---|---|---|---|---|---|---|
| BASE | $69,915 | $149,629 | m17 (2028-04) | never | never | $6,100 @ m16 | $126,068 / $421,548 |
| GLUT | $66,411 | $104,077 | m17 (2028-04) | never | never | $6,734 @ m16 | $129,654 / $333,977 |
| SEVERE | $63,862 | $83,031 | m17 (2028-04) | never | never | $7,062 @ m16 | $127,315 / $281,815 |

- **First revenue:** m6 (2027-05). No scenario sells an index licence.
- **What would pay the founder inside 36 months:** trial conversion of ≥14.7%, or 1.51× the revised trial inflow. With the Phase 4 funnel restored (12% conversion, 25-trial cap), the revised model covers the salary at m31.
- **Stress cases:**
  - K5 fails (no price line): $69,289 ARR at m36, cash low $947.
  - Conversion 0.08: $119,703, cash low $486.
  - Nexar $1,000 + display $2,500: cash low −$1,884.

### 14.4 Revised verdicts

- **POSSIBLE:** Yes for the SaaS. No for the index as designed: the panel reaches 14 members by m36, below the 15 needed.
- **PROFITABLE:** No as a venture; marginal as a side business. BASE reaches $150k ARR at m36, the founder is never paid within 36 months, and the cash low is $6.1k.
- **DOABLE BY THIS FOUNDER:** Yes, conditional on the K0 employer carve-out and the K6 call-booking test.

### 14.5 FINAL STATUS: DOWNGRADED

**Reason.** No objection was refuted. The FATAL objection, confirmed by the model, killed the SaaS-fed index. That was the leg the bundle existed to borrow its moat and cycle robustness from. Fifteen further downgrades cut BASE m36 ARR from $421,548 to $149,629 and leave the founder unpaid through m36 in every scenario. The SaaS still reaches first revenue at m6 and breaks even (founder unpaid) at m17, so DD2 is not killed. It is **demoted from FALLBACK to side line**. The ~$2,950 kill test, run alongside DD1/DD3 customer discovery, decides whether it lives.

**Phase 4 verdicts, kept for the record:** POSSIBLE Yes · PROFITABLE Marginal (BASE $126k ARR at m18 and $422k at m36; salary covered from m23) · DOABLE Yes · Recommendation FALLBACK-grade.
