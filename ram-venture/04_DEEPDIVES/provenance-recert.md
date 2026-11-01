# DD1 — Provenance & Recertified Memory (`provenance-recert`)

**Author:** `p4w-provenance-recert`; Phase 5 red-team revision by `p5r-provenance-recert` · **As of:** 2026-11-01 · **Model:** `models/provenance-recert.py`, revised after the red team (RED-TEAM REVISIONS block), re-run 2026-11-01, exit 0; output in `research/phase4/provenance-recert_model_output.md` · **Notes:** `research/phase4/provenance-recert_notes.md` · **Red-team responses:** `research/phase5/responses_provenance-recert.json` · **Judgment calls:** `research/assumptions/p4w-provenance-recert.md`, `research/assumptions/p5r-provenance-recert.md`

> **FINAL STATUS after the Phase 5 red team: KILLED** as a venture candidate (§14). Sections 0, 2, 10 and 11 carry the revised numbers, marked "(revised after red team)". Sections 1, 3–9 and 12 describe the Phase 4 plan and are kept as the record; where the red team overturned a claim there, a note points to §14.

**How to read the citations.**
- **m§N** = section N of the model's printed output. m§0 lists every red-team input change; m§8 attributes the change and runs the variants.
- **INPUTS** = the model's INPUTS dict, where each input carries its own source. Phase 5 changes are in RED_TEAM_REVISIONS.
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

**(revised after red team)** The bundle logic failed. Recert flow cannot supply die-source data for the at-risk population (RT-HYP-DD1-02, RT-PHY-DD1-01, RT-VC-DD1-02). The module-maker buyer already owns that data (the three FATALs). C-85's predictive subscription is dropped (RT-PHY-DD1-04). See §14.

**Capital tier: T0.** It starts on $40k of the founder's money (INPUTS `start_cash`; ASSUMPTIONS A-03). **(revised after red team)** The revised bundle needs about $46k: its cash dips to −$5,863 at m18, from operating losses, not working capital (m§3). CleanBOM on its own dips to −$10,164 (m§4).

**Scores and ranks** (`scores.csv`, 40 concepts scored; Phase 3 scores, set before the red team):

| ID | Default | Capital-constrained | Moonshot |
|---|---|---|---|
| C-64 | 78.0 (#6) | 81.7 (#6) | 76.7 (#3) |
| C-26 | 74.0 (#9) | 78.3 (#7) | 66.7 (#12) |
| C-85 | 74.0 (#11) | 77.5 (#10) | 71.7 (#10) |
| C-62 | 71.0 (#14) | 75.0 (#11) | 64.2 (#16) |

**The honest summary (revised after red team): killed as a venture, not even a reliable cash business.**
- **The red team's three FATAL objections hold** (§14). The named core buyer, the OEM-compatible module maker, already knows its die source from POs, CoCs and package top marks. It may self-certify under the proposed FAR rule, and resellers may rely on that free certificate.
- **The library moat is gone.** Recert flow samples old OEM DDR4 with roughly zero CXMT. A module part number does not fix die identity. And per-lot top-mark images are cheap for anyone to rebuild.
- **The cash engine is gone at central inputs.** At a 0.70 buy fraction, 0.80× B2B pricing and 7% CE-inclusive fallout, recert earns **−$3 per module (−1%)**. It needs lots at ≤62% of resale for 8% (m§1a, m§6g).
- **Revised BASE (revised after red team):** **$58,335 ARR at m36** (was $445,543), $23,270 cash, −$3,473 cumulative EBITDA, the founder **never** goes full-time, and there is no breakeven at a $10k salary (m§3).
- **If both kill tracks pass** (lots ≤0.62 of resale, and a module maker that pays cash): $226,833 ARR at m36, full-time only at m32, and never in GLUT/SEVERE (m§8d).

**POSSIBLE? — Yes, with corrections (revised after red team).** Recert is an existing TRL-9 trade. CXMT die is identifiable at die level: TechInsights analysed a CXMT G4 die inside a Powev-marked package. But a module-P/N cross-reference is physically invalid, memtest86+ burn-in misses ECC-corrected faults (CE logging plus a heated soak is required), and X-ray die outline is only triage.

**PROFITABLE? — No (revised after red team).** At post-red-team central inputs recert loses money per module, and CleanBOM reaches 5.3 subscribers ($58,335 ARR) by m36 in all three price decks. The best case, with both tracks passing, is a $227k-ARR lifestyle business.

**DOABLE BY THIS FOUNDER? — Mechanically yes, but not worth doing (revised after red team).** It is T0 and startable part-time. But no central-input version puts the founder full-time inside 36 months, and the federal sales motion they have never run is still the gating skill.

---

## 1. How it works

Every server holds memory sticks called RDIMMs: a row of DRAM chips plus a tiny label chip called the SPD. When data centers retire servers, IT asset disposition firms (ITADs) such as Iron Mountain and Sims Lifecycle pull the sticks and sell them in lots. Contract DRAM prices have roughly quadrupled since late 2025 (01_LANDSCAPE §5.1). A used 32GB DDR4 stick now realizes $100–150, and a used 64GB DDR5 stick $890–1,200 ([amcompute, 2026-08](https://www.amcompute.com/appraisals/ddr4-32gb-rdimm); [amcompute](https://www.amcompute.com/appraisals/ddr5-64gb-rdimm)) [REPORTED].

**Line 1: recert, the cash engine.**
1. Buy lots.
2. Burn in each stick for hours in a used server with free software (memtest86+, Google's stressapptest). **(revised after red team)** memtest86+ cannot report ECC-corrected errors on a Xeon bed. The protocol is now Linux stressapptest with rasdaemon/EDAC per-DIMM CE logging (any CE = reject) and a 55–70°C soak (RT-VET-DD1-03, RT-PHY-DD1-03).
3. Log its SPD data and apply a serial label and test record.
4. Sell good sticks on eBay and to refurbishers and maintenance firms, labeled "used/recertified."

Optane PMem rides along as one extra SKU.

**Line 2: the library, the asset.** The SPD says who made the DRAM chips, but the module assembler writes that field, and anyone can rewrite it ([Evetech](https://evezone.evetech.co.za/build-lab/spot-fake-relabelled-ram-used-market)) [REPORTED]. Real proof is physical: an accredited lab X-rays the chip, dissolves the package and photographs the die markings (SAE AS6171).
- The bench sends three sticks a month to such a lab.
- One result identifies the die source for every stick sharing that part number and date-code family.
- Over time this builds a cross-reference ("part X, date codes Y–Z = Samsung die; part W = CXMT die") that nobody holds at module level.

> **Withdrawn after red team (§14).** Module P/Ns are multi-sourced, and the module date code is the assembly week, so one decap covers one build lot, not a family (RT-PHY-DD1-02, RT-VET-DD1-02, RT-HYP-DD1-03, RT-VC-DD1-03). Recert lots are old OEM DDR4 with roughly zero CXMT (RT-PHY-DD1-01). The library is redesigned as per-lot package top-mark images keyed on DRAM marking codes, plus X-ray die-outline triage and exception decap on new third-party DDR5 RDIMMs bought at market. That is a validation cost, not a moat.

**Line 3: CleanBOM-5949, the company.** From 2027-12-23, federal agencies may not buy products containing SMIC, CXMT or YMTC chips. Sellers must certify after a "reasonable inquiry" ([Federal Register, 2026-02-17](https://www.federalregister.gov/documents/2026/02/17/2026-03065/federal-acquisition-regulation-prohibition-on-certain-semiconductor-products-and-services)) [REPORTED]. The firms that write the *first* certification need to know what is inside the module: third-party "OEM-compatible" memory makers and white-box server builders.
- **What CleanBOM sells them:** a subscription ($750 or $2,500 a month), per-SKU evidence packs ($900), and lab die-checks at cost × 1.6.
- **How it is framed:** an evidence-based assessment, never a legal certification.

**Line 4: the spares feed (DIMM-health, demoted).** Tested spares plus a corrected-error trend feed, sold wholesale to third-party maintenance (TPM) firms. **(revised after red team)** The predictive feed is killed (RT-PHY-DD1-04): DDR5 on-die ECC thins the corrected-error signal, BMC prediction is free, and there are no precision/recall numbers. Tested spares sell only as recert B2B.

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

**(revised after red team)** Neither half of the timing logic survives at central inputs. Recert does not pay now: −1% per module at a 0.70 buy, 0.80× B2B and 7% fallout. CleanBOM's switched-on demand is mostly met by free supplier certifications (§14).

---

## 2. Cost and unit-economics model

All figures in this section are **(revised after red team)** unless a column says "Phase 4". The model applies Phase 4 INPUTS plus the RED-TEAM REVISIONS block (m§0). `P_PHASE4` still reproduces the Phase 4 run exactly (m§8a, first row).

### 2.1 Unit economics

| Line (per unit) | Today | GLUT (DDR5 −60%) | SEVERE (−90%) | Phase 4 (today) | Source |
|---|---|---|---|---|---|
| Recert RDIMM, mixed channel (65% 32GB DDR4 / 32% 64GB DDR4 / 3% 64GB DDR5; buy 0.70; 7% fallout; 3% returns) | $191 → **−$3 (−1%)**. Buy+fallout $159, fees+ship $20, returns+labor $13 | $76 → −$8 (−10%) | $40 → −$9 (−23%) | $253 → $37 (15%) | m§1a |
| … eBay only / B2B only (B2B at 0.80× eBay) | $4 (2%) / −$9 (−6%) | −$6 / −$9 | −$10 / −$9 | $36 / $38 | m§1a |
| … by SKU, today | 32GB DDR4 −$6 (−5%); 64GB DDR4 $1 (0%); 64GB DDR5 $31 (3%), with $732 of cash tied up per unit | — | — | $12 / $43 / $167 | m§1a |
| Optane PMem 128GB (10% locked/unsanitizable fallout, 5% returns) | $200 → $27 (14%) | $3 (4%) | −$9 (−46%) | $46 (23%) | m§1b |
| CleanBOM, per subscriber-month (ARPA $925 + $384 lab pass-through; 90% on $750, 10% on $2,500) | **$958 GP (73%)**; a $900 pack earns ~88% | same | same | $1,295 (80%) | m§1c |
| DIMM-health | **Dropped from the bundle** (RT-PHY-DD1-04) | — | — | 64% GM, 4.5× DIY | m§1d |

- **Inventory lag:** selling a month into the glut loses $11 (−6%) per module (m§1a).
- **CleanBOM CAC:** $5,100 at a 5% close (m§1e). The LTV/CAC ratio still rests on untested inputs, so do not quote it.
- **Breakeven buy fraction:** 69% of realized resale on the m12 channel mix (72% eBay-only, 66% B2B-only). The 8% contribution that track A requires needs **≤62%** (≤64% eBay-only), and the model's 5% buy/no-buy line is 65% (m§6a, m§6g). Phase 4's breakeven was 78%.

### 2.2 Scenario summary (bundle = recert + PMem + CleanBOM; m§3)

| | BASE | GLUT | SEVERE | Phase 4 BASE |
|---|---|---|---|---|
| ARR (recurring) m12 / m18 / m24 / m36 | $8,160 / **$23,067** / $36,274 / **$58,335** | same as BASE | same as BASE | $25,334 / $139,995 / $253,948 / $445,543 |
| Total run-rate m18 / m36 | $61,244 / $150,124 | $57,244 / $101,676 | $54,844 / $94,884 | $1.88M / $1.75M |
| Breakeven, founder unpaid | **m19 (May-28)** | m19 | m19 | m3 |
| Breakeven with a $10k/month founder salary | **never** | never | never | m11 |
| Founder goes full-time | **never** | never | never | m14 |
| Cash low point | **−$5,863 at m18** (operating losses: CleanBOM fixed costs plus ISO at m15, with no recert profit) | −$6,061 | −$6,179 | $5,000 reserve at m10 |
| Cash at m36 (+ inventory) | $23,270 (+$2,965) | $22,086 (+$890) | $21,588 (+$466) | $610,097 (+$70,850) |
| Cumulative EBITDA (tax provision) | −$3,473 ($0) | −$7,852 ($0) | −$8,998 ($0) | $662,971 (no tax line) |
| Gross margin: blended / recert+PMem / CleanBOM | 38% / 11% / 75% | 43% / 11% / 75% | 44% / 11% / 75% | 25% / 15% / 81% |
| Recert+PMem share of cumulative revenue | 57% of $273,517 (only 356 recert modules sold; PMem is most of it) | 49% of $231,157 | 47% of $222,072 | 85% of $4.14M |

Recert buying drops to the 10% trickle from month 2, because expected contribution is below the 5% buy line. From Jan-28 to Feb-29 cash sits below the reserve, so nothing is bought at all.

### 2.3 Is the whole better than the parts? (BASE, m§4)

| Configuration | ARR m36 | Cash m36 | Cumulative EBITDA | Phase 4 ARR m36 |
|---|---|---|---|---|
| Bundle (recert + PMem + CleanBOM) | $58,335 | $23,270 | −$3,473 | — |
| Bundle + DIMM-health (Phase 4 line-up, revised inputs) | $85,522 | $34,121 | $16,811 | $445,543 |
| Bundle without the library lift | $58,335 | $23,270 | −$3,473 | $323,558 |
| Bundle, founder never full-time | $58,335 | $23,270 | −$3,473 | $199,038 |
| CleanBOM standalone | $58,335 | $18,068 (low −$10,164) | −$20,432 | $120,296 |
| Recert + PMem only | $0 | $4,815 | −$26,398 | $0 |
| DIMM-health standalone | $27,187 | $83 | −$26,165 | $27,187 |

**Reading the table (revised after red team):**
- **No synergy is left.** Recert no longer buys founder time, because the founder never goes full-time in any configuration.
- **The library lift is zero by construction.** Bundle and standalone close at the same 5%, and the bundle pays for its sample modules.
- **The bundle beats CleanBOM standalone by only ~$5k of m36 cash.** That comes from PMem and the trickle, not from data.

### 2.4 Sensitivity (BASE, one input at a time; m§5)

| Input moved | ARR m18 | ARR m36 | Cash m36 | Cash low |
|---|---|---|---|---|
| Revised base | $23,067 | $58,335 | $23,270 | −$5,863 |
| Recert resale −30% | $23,067 | $58,335 | $18,076 | −$10,251 |
| Subscription price −30% | $16,147 | $40,835 | $4,862 | −$9,713 |
| Close rate −30% | $16,147 | $40,835 | $4,634 | −$9,066 |
| Close rate +30% | $29,988 | $75,836 | $43,198 | −$3,809 |
| COGS −30% (buy, fees, lab, hosting) | $45,243 | $132,970 | $257,903 | $5,652 |
| COGS +30% | $23,067 | $58,335 | −$7,748 | −$26,707 |
| Final FAR rule slips 6 months | $8,160 | $47,972 | $3,240 | −$12,889 |
| **ITAD buy fraction 0.62** (the track A pass line) | $23,067 | $58,335 | $41,777 | $5,000 |
| ITAD buy fraction 0.55 | $23,067 | $58,335 | $134,797 | $5,000 |
| ITAD buy fraction 0.75 | $23,067 | $58,335 | $19,750 | −$7,818 |
| B2B price factor 0.88 (the Phase 4 value) | $23,067 | $58,335 | $26,013 | −$4,197 |

The buy fraction is still the input that decides recert, and it still has **no published source**: a second search on 2026-11-01 found only asking prices. Even at 0.55, recert adds about $200k of cumulative EBITDA, but the founder never goes full-time. Monthly volume (capped at 300 part-time) times a $16–32 contribution never clears the $12k trigger.

### 2.5 What must be true (revised after red team; m§6)

1. **Lots cost ≤62% of realized resale** for 8% contribution (breakeven 69%). Phase 4 said under 78%.
2. **Recert cannot cover a founder salary at any volume** at a 0.70 buy (m§6b).
3. **CleanBOM has ~14 paying subscribers by the turn** at $958 GP each (m§6c). The model reaches **2.1 at m18 and 5.3 at m36**. Getting there needs a 34% close at 5 conversations a month, or 34 conversations a month at 5%.
4. **$1M ARR needs ~90 subscribers** at the revised $925 ARPA (m§6f). Phase 4 said ~61.

### 2.6 Variant runs (m§8d; all revised after red team)

| Variant | Scenario | Founder full-time | ARR m36 | Cash m36 |
|---|---|---|---|---|
| Turn arrives early (Oct-27, `turn_month=12`) | GLUT | never | $58,335 | $20,740 |
| FAR rule slips 6 months (`_cb_delay=6`) | BASE | never | $47,972 | $3,240 (low −$12,889) |
| CleanBOM sells nothing | BASE | never | $0 | −$59,798 |
| Track A passes (buy 0.62) | BASE / GLUT | never / never | $58,335 / $58,335 | $41,777 / $48,983 |
| Track C passes (close 10%, high tier 35%, packs 15%: the Phase 4 CleanBOM inputs) | BASE | never (salary breakeven m30) | $171,852 | $128,084 |
| **Tracks A (0.62) and C both pass** | BASE | **m32** | **$226,833** | $106,959 |
| Tracks A and C both pass | GLUT / SEVERE | never / never | $171,852 / $171,852 | $150,359 / $148,278 |

**Attribution (m§8a, BASE, revision groups applied cumulatively from Phase 4's $445,543 / full-time m14):**

| Step | ARR m36 | Founder full-time |
|---|---|---|
| + tax provision 30% (RT-VC-DD1-07) | $419,301 | m17 |
| + cash cycle: eBay limits and holds, B2B net-30 (RT-VC-DD1-04) | $340,928 | m24 |
| + buy 0.70, caps 300/450 (RT-HYP-DD1-04, RT-VC-DD1-05) | $308,396 | m26 |
| + B2B 0.80, eBay share 0.50 (RT-HYP-DD1-05, RT-VET-DD1-05) | $250,221 | m33 |
| + CE-logging protocol, 7%/3% (RT-VET-DD1-03, RT-PHY-DD1-03) | $237,798 | m34 |
| + DDR5 3%; PMem fallout (RT-VET-DD1-04; RT-PHY-DD1-05, RT-VET-DD1-07) | $237,798 | m34 |
| + DIMM-health dropped (RT-PHY-DD1-04) | $171,852 | never |
| + library re-keyed and bought at market, lab $600 | $183,297 | m36 |
| + CleanBOM demand: close 5%, high tier 10%, packs 10% (the three FATALs, RT-HYP-DD1-06, RT-HYP-DD1-07) | $58,335 | never |
| + E&O $600/month (RT-HYP-DD1-08) | **$58,335** | **never** |

Reproduce any row from the repo root, swapping the overrides:

```
python3 -c "import importlib.util as u,sys;sys.path.insert(0,'models');s=u.spec_from_file_location('pr','models/provenance-recert.py');pr=u.module_from_spec(s);s.loader.exec_module(pr);print(pr.metrics(pr.simulate('GLUT',dict(pr.P0,turn_month=12))))"
```

Use `pr.P_PHASE4` in place of `pr.P0` to reproduce Phase 4.

### 2.7 The honest read (revised after red team)

Phase 4 was generous in exactly the places the red team hit:
- the unsourced buy fraction;
- a B2B price above what the B2B accounts pay for the same lots;
- a burn-in that cannot see corrected errors;
- a DDR5 slice that is not in 2026–27 lots;
- a library sampled from the wrong population;
- a close rate that assumed module makers need evidence they already hold.

No single revision kills DD1. Together, they leave recert below zero margin and CleanBOM at 5 subscribers. The only path back runs through two cheap tests, and both pass conditions look unlikely (§10, §14).

---

## 3. Target customer and the first ten customers

**Who pays for CleanBOM.** The safe harbor moves liability upstream: whoever writes the first certification has to know the die source ([Mayer Brown, 2026-03-03](https://www.mayerbrown.com/en/insights/publications/2026/03/far-council-proposes-rule-to-prohibit-acquisition-of-semiconductors-from-china-and-countries-of-concern)) [REPORTED]. So the core buyer is the third-party "OEM-compatible" memory maker selling into federal channels, where CXMT is now the marginal open-market supplier. A U.S. reseller already markets a CXMT-made 64GB DDR5 RDIMM as compatible with Dell PowerEdge 16G and HPE Gen11 ([router-switch.com](https://www.router-switch.com/sw/faq/cxmt-ddr5-server-memory-cxmr4e464r8as-cb1c-dell-hpe-sizing.html)) [REPORTED, vendor claim].

> **(revised after red team)** This buyer analysis is overturned (RT-HYP-DD1-01, RT-VC-DD1-01, RT-VET-DD1-01, all ACCEPTED-KILL). The module maker is the party that *already* knows its die source: from POs and CoCs that name the DRAM maker, and from package top marks. It may certify on its supplier declaration, and the resellers downstream may rely on it. What remains is refurb/odd-lot resellers and white-box builders. Customers #1–3 move from "$2,500 tier" to "track C test subjects": the pass condition is that one of them pays cash and states in writing that its ODM or supplier refuses a die-source declaration (§10).

**Who pays for recert:** refurbishers and TPM spares desks. (revised after red team) They buy the same ITAD lots and test in-house, so they pay ~0.75–0.80× eBay, not 0.88× (RT-HYP-DD1-05, RT-VET-DD1-05).

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
- **Recert:** eBay first, then B2B accounts #6–9. eBay's share falls from 70% to 40% of sales by m12 (INPUTS `ebay_share_*`). (revised after red team) It falls to 50%, and B2B is planned only on written offers ≥0.85× eBay.
- **CleanBOM:** direct founder selling, plus SEWP/GSA vendor days from a $3k launch budget (INPUTS `cb_launch_marketing`).
- **Dataset:** business development with compliance-data vendors. (revised after red team) Removed unless a ≥$100k/yr licensing LOI appears (RT-VC-DD1-06).

**Pricing** [ESTIMATE unless cited]:

| Item | Price | Basis |
|---|---|---|
| Recert module, eBay / B2B | Realized resale (e.g., $125 for 32GB DDR4) / 0.88× that (revised after red team: 0.80×) | INPUTS (amcompute midpoints) / RED_TEAM_REVISIONS |
| PMem 128GB | $200 | m§1b |
| CleanBOM integrator/reseller tier | $750/month | Above SiliconExpert-class entry: Accuris prices 20% below SiliconExpert with a $6,000 minimum ACV ([Accuris](https://accuristech.com/siliconexpert-offer-terms/)) [REPORTED], which implies SiliconExpert ≈ $7.5k/yr [ESTIMATE: $6,000 ÷ 0.8] |
| CleanBOM high tier | $2,500/month. (revised after red team) White-box builders only, 10% of customers; module makers removed | m§1c |
| Evidence pack (per SKU family) | $900 | m§1c |
| Lab die-ID sample | Lab cost × 1.6 (≈$960 at the revised $600 all-in lab cost; revised after red team) | INPUTS / RED_TEAM_REVISIONS |
| Spares + feed to TPMs | (revised after red team) Feed dropped (RT-PHY-DD1-04); tested spares sell as recert B2B | — |

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
| 1–30 | The kill experiment (§10; decision on day 29, 2026-11-30) | Go/no-go per line |
| 31–60 | Buy the m2 lot (~$7.1k; m§2). Open an eBay store with per-serial test records. Pitch xByte, TechMikeNY and PCSP. Turn track C's yeses into design-partner LOIs | 2 B2B accounts; 3 signed LOIs |
| 61–90 | Sell ~39 modules (m§2 Jan-27). Deliver free die-checks. Get ITAD downstream questionnaires in writing | ≥$15k revenue in month 3 (model $15.1k); ≥1 paid pack |

CleanBOM subscriptions launch only in Aug-27 (m10, INPUTS `cb_launch`). Before then, the job is pre-selling.

> **(revised after red team)** This 90-day plan is superseded by the staged resurrection test in §10. Stage 1 is track C plus free written quotes ($1.4k). The lot is bought only if Stage 1 passes.

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
- Z2Data or SiliconExpert ships a module flag. A funded team could rebuild a ~63-part library in a quarter [ESTIMATE: 63 lab samples × ~$400 ≈ $25k].
- The final rule keeps the safe harbor, so most sellers self-certify for free.
- OBSIDIA moves to modules.
- ITADs keep the recert spread.
- OEMs drop CXMT from U.S. SKUs.

The fraud evidence is also all consumer-channel. No case of CXMT die relabeled inside U.S. server RDIMMs was found (notes §2).

> **(revised after red team)** Win condition 2 fails. The library comes from the wrong population, is keyed on module P/Ns that are multi-sourced, and its per-lot replacement is cheap for anyone to rebuild (§14). There is no data moat, so DD1 loses to Z2Data, SiliconExpert or plain self-certification on every axis except price.

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
- **(revised after red team)** There is no exit. A buyer will not pay more than the dataset's rebuild cost (~$25k or less; RT-VC-DD1-06), and revised m36 ARR is $58,335. The raise path is removed.

---

## 8. 18-month roadmap with milestones

> **(revised after red team)** This roadmap is the Phase 4 plan, and its model targets are Phase 4 BASE figures. After the red team DD1 is KILLED (§14). If the staged resurrection test in §10 passes, re-plan from the m§8d "tracks A and C both pass" row: $67,956 ARR at m18, $226,833 at m36, full-time at m32.

Model targets are BASE (m§2, Phase 4). Each gate must be met to continue.

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
| **AS6171 lab partner** | m1, then 3 samples/month (revised after red team: 1/month, exception and validation only) | $400/sample [ESTIMATE; track B quotes it] (revised after red team: $600 all-in, including minimum-lot and report fees) | ANAB list of 26 accredited labs ([ANSI](https://blog.ansi.org/anab/benefits-as-6171-suspect-counterfeit-eee-parts/)); SMT Corp; Integra and Micross (DMEA, 01_LANDSCAPE §7.3) |
| **E&O and liability broker** | m9 | $400 + $200/month (INPUTS) | Tech E&O brokers |
| **ISO consultant + certification body** | m12–15 | $10k, plus $3k surveillance at m27 (INPUTS) | NQA |
| **Federal channel advisor**, commission-only | m9–14 | No fixed cost [ESTIMATE] | Former SEWP/GSA reseller account managers (LinkedIn); NASA SEWP vendor days |
| **STTR PI** (optional) | After m12 | Non-dilutive | UMD CALCE |
| **Data engineer** | Only after ≥10 subscribers | Not modeled | — |

The founder's operations background fits receiving, test flow and supplier attestations. **The gap is federal selling**, which is why track C talks to 15 buyers before any CleanBOM code exists.

---

## 10. The cheapest experiment that could kill it — now a staged resurrection test (revised after red team)

**Status:** DD1 is KILLED (§14). This test is **optional**. Run it only if the founder's primary pick leaves spare hours, because it is the only route by which the red team could be proved wrong. Phase 4 ran tracks A–D in parallel for ~$8,400. The revised test is **staged**: a $1.4k Stage 1 decides whether anything else is worth buying.

**Budget (revised after red team):** Stage 1 is ~$1,400. Stage 2 is ~$8,100, and runs only if Stage 1 passes. **Hard cap: $9,500 in total.** Shrink the lot if any quote would breach it.

**Time:** Stage 1 runs 29 days (day 1 = 2026-11-02, decision on 2026-11-30). Stage 2 runs days 30–60 (decision on 2026-12-31). All thresholds are fixed now, before any data comes in.

### Stage 1: paper and conversations (~$1,400; days 1–29)

**Days 1–3: line everything up (no spend except one module).**
- **ITAD quotes, in writing** (RT-HYP-DD1-04, RT-VC-DD1-05). Ask Iron Mountain/ITRenew (Sesame), Sims Lifecycle and one regional R2 ITAD in NJ, PA or MD for: price as a share of trailing realized resale; **≥200 DDR4 RDIMMs a month with a 6-month supply commitment**; the share of 64GB DDR5 in each lot; manifests showing brand, DRAM package marks and date codes; downstream terms a non-R2 buyer can meet; and, for PMem, per-serial NIST SP 800-88 sanitization certificates.
- **B2B price sheets, in writing** from xByte, TechMikeNY and PCSP for tested 32GB DDR4 (RT-HYP-DD1-05, RT-VET-DD1-05).
- **AS6171 lab quotes, in writing, from 3 labs** (RT-VET-DD1-06). Each quote must be all-in: per-sample, minimum-lot and report charges, turnaround, and whether the lab holds CXMT DDR4/DDR5 reference die images.
- **Federal-channel count** (RT-HYP-DD1-06). From GSA Advantage and the SEWP catalogs, list the firms selling non-OEM-branded server memory.
- **One sample pack.** Buy the cheapest OEM-compatible DDR5 RDIMM from AddOn, Axiom or Brute (~$400). Build a one-page pack from its package top-mark images and SPD bytes (512–513 and 552–553). There is no lab work in Stage 1.

**Days 4–29: track C′, 15 conversations.** Talk to 5 compatible-memory makers, 5 GSA/SEWP resellers including SHI, and 5 white-box/appliance builders. Ask for a paid pilot at $750–2,500 a month or a $900 pack. Ask every module maker in writing: "For what share of the SKUs you ship federally can you **not** obtain a die-source declaration from your ODM or component supplier, or establish die source from your purchase records plus top-mark inspection?"

| Stage 1 track | Spend | Pass only if… (decided now) | Phase 4 rule |
|---|---|---|---|
| C′. Demand | ~$1,000 + $400 module | ≥3 of 15 sign an LOI or buy a pack, **and** ≥1 pays cash, **and** ≥1 **module maker** (not a reseller) pays cash and states in writing that for ≥20% of its federal SKUs it cannot get a die-source declaration (RT-HYP-DD1-01, RT-VC-DD1-01, RT-VET-DD1-01) | ≥3 of 15 LOIs and one cash payer |
| A′ (paper). Buy side | $0 | Written quotes from 2 of 3 ITADs at **≤62%** of trailing realized resale for ≥200 modules/month with 6-month supply (breakeven is now 69%; m§6g). The B2B channel is planned only if 2 written offers come in at ≥0.85× eBay for ≥100 modules/month; otherwise recert is planned eBay-only | One spot quote ≤75% |
| B′ (paper). Lab | $0 | ≥1 of 3 labs confirms in writing that it holds CXMT reference die images (or can identify CXMT die by logo or dimensions), with an all-in quote ≤$600/sample and ≤15 business days | Lab ≤$600/sample, ≤15 business days, die source identifiable |

**Stage 1 decision rule (revised after red team):**

| Outcome | What happens |
|---|---|
| C′ fails | **DD1 stays dead.** If A′ passes, the founder may run recert as a hobby-scale side trade. At 0.62 it adds ~$71k of cumulative EBITDA over 36 months and never funds full-time (m§5). It is not a venture. |
| C′ passes, A′ fails | Stage 2 runs track B only (~$3.6k). CleanBOM is planned standalone at the Phase 4 demand inputs. Standalone gives $171,852 ARR at m36, never full-time, salary breakeven at m31, and a cash low of $2,105 at m15 on $40k. The bundle row in m§8d is nearly identical ($3,326 low). |
| C′ and A′ pass | Stage 2 runs tracks A and B (~$8.1k). Re-plan from the m§8d "both pass" row. |

### Stage 2: physical tests (~$8,100; days 30–60; only if Stage 1 passes)

| Track | Spend | Fail if… (decided now) |
|---|---|---|
| A. Buy side and test escapes | ~$4,900: one used Gen10 server ~$1,500, a heated soak enclosure ~$500, and a lot capped at **$2,900** (~33 × 32GB DDR4 at the revised $88 buy) | Measured lot contribution < **8%**, **or** CE-inclusive fallout > **4%**. The test runs Linux stressapptest with rasdaemon/EDAC per-DIMM CE logging (any CE = reject) plus a 55–70°C soak (RT-VET-DD1-03, RT-PHY-DD1-03). 90-day returns ≤2% are tracked after the decision. For any PMem in the lot, ipmctl must read ≥90% "disabled/unlocked" (RT-VET-DD1-07, RT-PHY-DD1-05) |
| B. Evidence | ~$3,200: 4 samples × ≤$600 all-in, plus a **known CXMT server RDIMM** (CXMR4E464R8AS-class or a 16–32GB CXMT DDR5 RDIMM, ~$800 [ESTIMATE]) as the positive control in place of the consumer kit (RT-PHY-DD1-06). The Stage 1 compatible RDIMM is reused | Lab > $600/sample all-in, > 15 business days, or the CXMT server control is not identified. **Samples ship by day 35.** An X-ray die-dimension screen runs before any decap. It is triage only: CXMT G4 is ~67–68 mm² against ~49 mm² for current Samsung, but 2021 first-generation big-3 16Gb dies were ~66–72 mm² ([3DNews citing TechInsights](https://3dnews.ru/1116172)) [REPORTED] |
| D. Spares feed | — | **Retired.** The C-85 predictive subscription is killed (RT-PHY-DD1-04) |

**Limits.**
- The P/N-consistency tests the reviewers asked for need about 30 decaps (~$36k at $600 lab + $600 module): ≥3 samples per family across ≥10 families (RT-VC-DD1-03), or 3 lots of one third-party P/N (RT-VET-DD1-02).
- That is beyond T0, which is one more reason the library cannot be a moat. Stage 2 tests 2 modules of one P/N from different sellers where possible.

---

## 11. Explicit kill criteria (revised after red team)

Months are model months (m1 = Nov-26). Each criterion is marked "(revised after red team)" where it changed, "(unchanged)" where it did not, and "(new)" where the red team added it.

1. **2026-11-30 (revised after red team).** No written ITAD quotes from 2 of 3 at **≤62%** of resale for ≥200 modules/month with 6-month supply → do not buy lots. Was ">75% or lot contribution <8%". At 0.70, recert earns −$3/module (m§1a).
2. **2026-11-30 (revised after red team).** Fewer than 3 of 15 commit, or none pays cash, **or no module maker pays cash and states in writing that it cannot get die-source declarations for ≥20% of its federal SKUs** → do not build CleanBOM; DD1 stays killed.
3. **2026-12-31 (revised after red team).** Lab > $600/sample all-in (including minimums and report fees), > 15 business days, no lab with CXMT reference images, or the CXMT server control is not identified → no lab-backed packs; packs carry top-mark images and SPD bytes only.
4. **2027-04-30 (m6) (revised after red team).** Trailing-3-month recert contribution < **8%** (was 12%; the revised model at 0.62 earns 8%), or CE-inclusive fallout > 4%, or 90-day returns > 2% → stop recert.
5. **2027-07-31 (m9) (revised after red team).** No bound E&O quote that covers government-contract reliance claims **with no regulatory exclusion** at ≤ **$600/month** (was ≤$400 with no exclusion test), or fewer than 3 LOIs still live → no assessments; sell raw evidence only (images, SPD bytes, lab reports), with no "no CXMT" language.
6. **2027-10-31 (m12) (unchanged).** Fewer than 1 paying subscriber and fewer than 3 paid packs → stop CleanBOM.
7. **Full-time gate (from m13) (unchanged rule; revised outcome).** Quit the day job only if all three hold:
   - trailing-3-month pre-salary EBITDA ≥ $12k;
   - cash ≥ $25k, now tested **after** the tax provision;
   - ≥ 5 paying CleanBOM subscribers.

   The revised model never meets this gate in any scenario. If both tracks pass, it is met at m32 in BASE only (m§8d).
8. **2028-04-30 (m18) (revised after red team).** Fewer than **4** paying subscribers (the both-pass model has 4.2; was 7) → stop CleanBOM sales spend and harvest.
9. **Any date (revised after red team).** The final FAR rule exempts COTS items or memory modules, or §5949 is pushed past 2028-12-31 → kill CleanBOM. A final rule that keeps reliance on supplier certifications for COTS memory confirms the red team; CleanBOM is then limited to refurb/odd-lot packs. If Z2Data or SiliconExpert ships a module-level CXMT flag under $750/month → stop. The dataset-licensing fallback is removed (RT-VC-DD1-06).
10. **Any date (unchanged rule).** Expected recert contribution < 5% → stop buying lots and keep a 10% trickle. This now fires at any buy fraction above 65% at today's prices (m§6g).
11. **2027-09-30 (revised after red team).** Stop buying PMem ahead of vSphere 8 end of general support on 2027-10-11 unless trailing PMem contribution from non-VMware buyers is ≥ 20%; **also** stop if >5% of any lot is passphrase-locked or unsanitizable.
12. **(revised after red team)** Retired: C-85's predictive subscription is dropped (RT-PHY-DD1-04).
13. **(new)** No exit value is assumed. A dataset-licensing LOI at ≥$100k/yr from a compliance-data vendor is the only thing that would reinstate one (RT-VC-DD1-06).

---

## 12. Cycle test

> **(revised after red team)** The figures below are Phase 4's. After the red team, recert loses money in every deck (−1% today, −10% GLUT, −23% SEVERE per module). Revised ARR at m36 is $58,335 in BASE, GLUT and SEVERE alike, cash at m36 is $21.6–23.3k, and the founder is never full-time (m§3, m§7). DD1 is "glut-proof" only because it barely depends on recert any more, and that is no virtue. The closing claim "DD1 is glut-proof only if the subscription business is real by the end of 2027" still stands. The red team says it will not be real (§14).

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

**DD1 is glut-proof only if the subscription business is real by the end of 2027.** The 29-day test and the m18 gate exist to find that out before the founder quits their job.

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

**Phase 5 red-team sources** (logged in `research/sources/p5r-provenance-recert.jsonl`; snippet grade)
- https://www.techinsights.com/blog/cxmt-g4-16gb-ddr5-dram-process-analysis
- https://3dnews.ru/1117376/eksperti-izuchili-chipi-pamyati-ddr5-ot-cxmt
- https://3dnews.ru/1116172
- https://xenospectrum.com/ddr5-memory-chips-from-chinas-cxmt-40-larger-die-size-than-samsung-highlighting-challenges/
- https://datacenterdisk.com/best/32gb-ddr4-server-ram
- https://pcserverandparts.com/news/refurbished-ddr4-server-memory-2026-server-ram-price-crisis/
- https://insureon.com/small-business-insurance/errors-omissions/cost
- https://www.techinsurance.com/errors-omissions-insurance/cost
- Reviewer sources cited in the responses: `research/sources/p5-HYP.jsonl`, `p5-PHY.jsonl`, `p5-VC.jsonl`, `p5-VET.jsonl` (Meta Vistara/CXL DDR4 reuse, memtest86+ ECC discussion #248, eBay new-seller limits and holds, Micron design-ID-agnostic DRAM)

---

## 14. Red-team outcome

**Phase 5, agent `p5r-provenance-recert`, 2026-11-01.** Four adversarial reviewers raised 28 objections against DD1: VET (DRAM process veteran), VC (semiconductor VC), HYP (hyperscaler procurement lead) and PHY (condensed-matter physicist). The objections were 3 FATAL, 18 MAJOR and 7 MINOR. Every objection and its full response, verbatim, is in `research/phase5/responses_provenance-recert.json`. None is deleted.

**Dispositions:**
- **7 ACCEPTED-KILL.** Three legs die: CleanBOM as "the company" with its module-maker tier, the recert-fed die-source library, and the C-85 predictive subscription.
- **16 ACCEPTED-DOWNGRADE.**
- **5 ACCEPTED-MITIGATED.**
- **0 REFUTED.** I could not defeat any objection with evidence. The closest partial rebuttals were two: TechInsights found CXMT die inside a "Powev"-marked package, so a top mark is not always the die maker; and the $400/month E&O premium already sits above published small-firm averages. Neither changes a disposition.

| Objection | Severity | Disposition | Action |
|---|---|---|---|
| RT-HYP-DD1-01 | FATAL | ACCEPTED-KILL | Module makers already know die source and may self-certify; module-maker tier killed, track C tightened |
| RT-VC-DD1-01 | FATAL | ACCEPTED-KILL | Same: the party with liability holds the data free; close 10%→5%; kill criterion 2 requires a cash-paying module maker |
| RT-VET-DD1-01 | FATAL | ACCEPTED-KILL | Top mark + CoC is a $0 SOP; packs default to top-mark/SPD/X-ray triage, decap on exceptions only |
| RT-HYP-DD1-02 | MAJOR | ACCEPTED-KILL | Recert flow has ~zero CXMT; library lift removed; bundle pays for samples |
| RT-PHY-DD1-01 | MAJOR | ACCEPTED-KILL | Wrong population and $0 sample cost; samples are new DDR5 RDIMMs at $600; '63 part numbers' withdrawn |
| RT-VC-DD1-02 | MAJOR | ACCEPTED-KILL | Same; lot manifests recorded in track A; library is a validation cost, not a moat |
| RT-PHY-DD1-04 | MINOR | ACCEPTED-KILL | C-85 predictive subscription dropped (−$61k m36 ARR on Phase 4 inputs) |
| RT-HYP-DD1-03 | MAJOR | ACCEPTED-DOWNGRADE | Die vendor switches lot by lot; library keyed per lot; packs cover only the sampled lot |
| RT-PHY-DD1-02 | MAJOR | ACCEPTED-DOWNGRADE | Key changed to DRAM package marking + die outline; family inference withdrawn |
| RT-VET-DD1-02 | MAJOR | ACCEPTED-DOWNGRADE | Brand = die for maker modules; per-lot top-mark library re-costed (1 sample/month) |
| RT-VC-DD1-03 | MAJOR | ACCEPTED-DOWNGRADE | False-negative risk; no family inference; 30-sample consistency study unaffordable at T0 |
| RT-HYP-DD1-04 | MAJOR | ACCEPTED-DOWNGRADE | buy 0.65→0.70, caps 400/600→300/450; track A needs ≤0.62 for ≥200/month with 6-month supply |
| RT-VC-DD1-05 | MAJOR | ACCEPTED-DOWNGRADE | Same input change; recert reframed as an optional side trade |
| RT-HYP-DD1-05 | MAJOR | ACCEPTED-DOWNGRADE | B2B 0.88→0.80, eBay share 0.40→0.50; B2B planned only on written offers ≥0.85× |
| RT-VET-DD1-05 | MAJOR | ACCEPTED-DOWNGRADE | Same; signed POs or price sheets ≥0.85× required before B2B volume |
| RT-VET-DD1-03 | MAJOR | ACCEPTED-DOWNGRADE | CE-logging protocol + 55–70°C soak; fallout 3→7%, returns 2→3%, 12→15 min, +$500 |
| RT-PHY-DD1-03 | MAJOR | ACCEPTED-DOWNGRADE | Same protocol; test records state protocol, temperature and CE count |
| RT-VET-DD1-04 | MAJOR | ACCEPTED-DOWNGRADE | DDR5 share 10%→3%; DDR5 bed bought only if quotes show DDR5 |
| RT-VC-DD1-04 | MAJOR | ACCEPTED-DOWNGRADE | eBay new-seller caps, payout holds and B2B net-30 modeled; cash stays ≥$0 but full-time m14→m21 alone |
| RT-VC-DD1-07 | MINOR | ACCEPTED-DOWNGRADE | 30% tax provision; full-time m14→m17 and m36 cash −$231k on Phase 4 inputs |
| RT-HYP-DD1-06 | MAJOR | ACCEPTED-DOWNGRADE | High tier 35%→10% (white-box only); $1M path withdrawn; GSA/SEWP firm count added |
| RT-HYP-DD1-07 | MINOR | ACCEPTED-DOWNGRADE | Pack redesigned to a commodity top-mark/SPD check; pack rate 15%→10% |
| RT-VC-DD1-06 | MAJOR | ACCEPTED-DOWNGRADE | Dataset exit and raise path removed; ceiling is lifestyle at best |
| RT-HYP-DD1-08 | MINOR | ACCEPTED-MITIGATED | E&O $400→$600; criterion 5 requires no government-claims exclusion, else raw evidence only |
| RT-VET-DD1-06 | MAJOR | ACCEPTED-MITIGATED | Lab $400→$600 all-in; written CXMT reference-image confirmation; samples ship earlier |
| RT-PHY-DD1-06 | MINOR | ACCEPTED-MITIGATED | CXMT server RDIMM control replaces the consumer kit; X-ray die-outline triage added (not proof) |
| RT-PHY-DD1-05 | MINOR | ACCEPTED-MITIGATED | PMem fallout 0→10%, returns 2→5%; ipmctl security state and SP 800-88 certificates required |
| RT-VET-DD1-07 | MINOR | ACCEPTED-MITIGATED | Same; platform generation listed; ≥90% unlocked test adopted |

### 14.1 Changes made

1. **Model** (`models/provenance-recert.py`). A RED-TEAM REVISIONS (Phase 5) block changes 29 inputs, old → new, each with its objection id:
   - **buy side and channel:** buy 0.65→0.70, B2B 0.88→0.80, eBay share 0.40→0.50, caps 400/600→300/450;
   - **test protocol and SKU mix:** fallout 3→7%, returns 2→3%, 12→15 min/module, capex +$500, DDR5 mix 10→3%;
   - **cash cycle and tax:** eBay new-seller caps and holds, B2B net-30, 30% tax provision;
   - **PMem:** fallout 10%, returns 5%;
   - **library:** the bundle pays for samples, at $600 per module, 3→1 samples a month, lab $600;
   - **CleanBOM demand:** close 10%/7%→5%, high tier 35→10%, packs 15→10%;
   - **E&O:** $400→$600;
   - **DIMM-health:** dropped from the bundle.

   New mechanics: receivables, eBay ramp, tax with loss carry-forward, an optional ≥5-subscriber full-time gate. `P_PHASE4` reproduces Phase 4 exactly. Report sections 0 and 8 were added, and the model exits 0. The output is re-written to `research/phase4/provenance-recert_model_output.md`.
2. **CleanBOM.** The module-maker $2,500 tier is gone, and the high tier is white-box builders only. The default pack is top-mark images, SPD bytes and X-ray die-outline triage; decap is an exception add-on. There is no family-level inference and no "no CXMT" language without E&O that has no government-claims exclusion.
3. **Library.** It is re-keyed from module P/N + date code to per-lot DRAM package marking + die outline. Samples are new third-party DDR5 RDIMMs bought at market. The "63 lab-confirmed part numbers" and moat claims are withdrawn.
4. **Recert.** It is reframed from "cash engine" to "optional side trade only if lots are ≤62% of resale". The burn-in now logs ECC-corrected errors (rasdaemon/EDAC, any CE = reject) with a 55–70°C soak. B2B volume is planned only on written offers ≥0.85×. PMem modules get ipmctl security-state checks and SP 800-88 certificates.
5. **DIMM-health (C-85)** is killed, and track D is retired.
6. **Exit.** The dataset-sale exit and the m18 raise path are removed.
7. **Kill experiment** (§10). It is now a staged, optional resurrection test. Stage 1 ($1.4k) is track C′ with the HYP/VC/VET pass rule plus free written quotes. Stage 2 ($8.1k) is the physical tests. The CXMT server-RDIMM control replaces the consumer kit. The hard cap stays $9,500.
8. **Kill criteria** (§11). Criteria 1, 2, 3, 4, 5, 8, 9 and 11 are revised, 12 is retired, and 13 is new.

### 14.2 Revised headline economics (re-run model, m§3, m§8d)

| | BASE | GLUT | SEVERE | Phase 4 BASE |
|---|---|---|---|---|
| ARR m18 | **$23,067** | $23,067 | $23,067 | $139,995 |
| ARR m36 | **$58,335** | $58,335 | $58,335 | $445,543 |
| Breakeven (founder unpaid) | m19 (May-28) | m19 | m19 | m3 |
| Breakeven at a $10k founder salary | never | never | never | m11 |
| Founder full-time | **never** | never | never | m14 |
| Cash low / cash m36 | −$5,863 at m18 / $23,270 | −$6,061 / $22,086 | −$6,179 / $21,588 | $5,000 / $610,097 |
| Cumulative EBITDA | −$3,473 | −$7,852 | −$8,998 | $662,971 |
| **If tracks A (≤0.62) and C both pass** | $67,956 / **$226,833**; full-time **m32** | $171,852; never full-time | $171,852; never full-time | — |

### 14.3 Revised verdicts

- **POSSIBLE? — Yes, with corrections.** Recert is a TRL-9 trade. CXMT die is identifiable at die level ([TechInsights](https://www.techinsights.com/blog/cxmt-g4-16gb-ddr5-dram-process-analysis), snippet: a CXMT G4 16Gb die inside a Powev-marked package) [REPORTED]. But the module-P/N cross-reference is physically invalid, memtest86+ cannot see ECC-corrected faults, X-ray die outline is only triage, and ordinary AS6171 labs may lack CXMT reference images.
- **PROFITABLE? — No.** At post-red-team central inputs recert earns −$3/module (−1%), and CleanBOM reaches 5.3 subscribers and $58,335 ARR at m36 in every price deck. Cumulative EBITDA is −$3,473, and there is no breakeven at a founder salary. The best case, with both tests passing, is $226,833 ARR at m36: lifestyle scale, and only in BASE.
- **DOABLE BY THIS FOUNDER? — Mechanically yes, but not worth doing.** It is T0 and part-time, and the operations and software work fit them. But no central-input version gets them full-time inside the 36-month ceiling (both-pass BASE: m32), and the federal sale they have never run is still the gating skill.

### 14.4 FINAL STATUS: **KILLED**

**Reason.**
- **The three FATAL objections hold.** The named core buyer already knows its die source and may self-certify for free, and resellers may rely on that certificate.
- **The library cannot supply the missing moat.** It is sampled from the wrong population, keyed on multi-sourced P/Ns, and cheap to rebuild.
- **Recert's cash engine has no margin.** The red team's sourced corrections (buy fraction, B2B price, CE-inclusive fallout, no DDR5 in lots), stacked together, remove it.
- **What is left is not a venture.** The revised BASE ($58k ARR at m36, founder never full-time, cash below zero at m18) fails the founder's brief.
- **Only one path back, and it is narrow.** Stage 1 of §10 must find a cash-paying module maker that cannot get die-source declarations. Even then, the best case is a $227k-ARR lifestyle business.

**Role.** Drop it as a PRIMARY, FALLBACK or MOONSHOT candidate. At most, run the optional $1.4k Stage 1 probe as a side test if the primary pick leaves spare hours. Run recert only as hobby-scale side income, and only if written quotes come in at ≤62% of resale.
