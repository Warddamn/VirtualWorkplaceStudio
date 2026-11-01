# OPEN QUESTIONS

As of 2026-11-01 · Phase 6 deliverable · Decision: `research/phase6/decision.json` (unchanged here)

**What this file is.** These are the questions this study could not answer, ranked by how much each one moves the decision. The study's finding stands: **no venture-scale opportunity survived.** The PRIMARY is a gated side business, the FALLBACK is a smaller side line, and the MOONSHOT slot holds no qualifying concept, only a ~$0 option. Most of the questions below decide whether even those side lines are worth the founder's evenings. They do not decide whether a venture exists.

**How to read the tables.**
- **Owner** is the founder unless a row says otherwise.
- **Dates** come from `decision.json` and the deep dives' §10–§11. `FIRST_90_DAYS.md` schedules them week by week. If its dates differ, `decision.json` governs.
- "Not in 90-day plan" means nobody is scheduled to answer the question before 2027-01-31.

**Source keys** used in the tables:

| Key | File |
|---|---|
| DEC | `research/phase6/decision.json` |
| J-EV / J-CEIL / J-INT | `research/phase6/judge_ev.json` / `judge_ceiling.json` / `judge_integrity.json` |
| LI / LI.py | `04_DEEPDIVES/lifecycle-intel.md` / `models/lifecycle-intel.py` (re-run 2026-11-01, exit 0) |
| OMI / OMI.py | `04_DEEPDIVES/open-memory-ip.md` / `models/open-memory-ip.py` (re-run 2026-11-01, exit 0) |
| LAND | `01_LANDSCAPE.md` |
| RT | `05_REDTEAM.md` |
| SCOR | `03_SCORING.md` |
| V1–V4 | `research/phase1/verify_v1-policy.md`, `verify_v2-fabs-ip.md`, `verify_v3-backend.md`, `verify_v4-cost.md` |

**LI.py BASE vs PLAN.** LI.py figures are the model's revised BASE unless marked PLAN. BASE charges no November test spend and books the $5k antitrust opinion at m2. The PLAN rows in LI.py §10 follow DEC: the $1,950 test is charged at m1 and the opinion and the $1,000 consult are deferred. On the plan the max founder draw is **$30,850** (cap $34k) and the cash low **$9,150** at m16 (floor $5k). If K3+K4 pass and the deferred $6k is spent, they are **$36,850** and **$3,150** (LI.py §10; DEC `PRIMARY.plan_cash`).

---

## 0. Ranked summary: the twelve questions that move the decision

| Rank | Question | What it decides | Cheapest way to answer | Date / gate | § |
|---|---|---|---|---|---|
| 1 | Will the employer sign a written carve-out for a product sold into its own industry? | Whether DD2 exists for this founder. A refusal makes the PRIMARY "NONE" (DEC; J-INT) | Read the agreement, pay for a ≤$500 attorney review, send a one-page request | K0, request 2026-11-02, signature by 2026-11-09 | 2 |
| 2 | Will ≥5 of 25 cold-sourced SMB-OEM buyers put down a refundable $500 deposit or paid LOI at ≥$200/mo, and can 25 calls be booked in 21 days? | Whether DD2 lives. This is the study's one test of willingness to pay | DD2 kill test: 60 contacts, 25 calls, ~$1,950 planned (~$2,950 if the $1,000 consult is not deferred), cap $5,000, ~55 h (LI §10; DEC) | K6 + K1, 2026-12-01 | 1, 2 |
| 3 | Will Nexar or DigiKey allow in-app price display in writing at ≤$1,000/mo? | DD2's price module and its COGS. Fail case on the plan: $69,289 ARR at m36, $3,997 cash low at m22 (LI.py §10 PLAN; $947 in BASE) | Two emails (LI §10 step 3) | K5, 2026-12-15 | 2 |
| 4 | Will UCSC VLSIDA and Open Circuit Design say in writing that they will not release free silicon-characterized ≥16 KB macros within 18 months? | Whether DD5 dies at $0. A full free release cuts m36 ARR to $34.0k (OMI.py §7) | Two emails; silence counts as FAIL (OMI §10 test iv) | Sent 2026-11-02; answer requested by 2026-11-20; no written answer by 2026-12-01 = FAIL (OMI §11 #1; `FIRST_90_DAYS.md`) | 3 |
| 5 | Does real trial-to-paid conversion reach ≥14.7%? | Whether DD2 can ever pay a $10k/mo salary within 36 months (LI.py §10) | Not answerable in 90 days. First evidence comes from the m6 launch (2027-05) | m9 gate 2027-08-31; m12 gate 2027-11-30 | 1, 7 |
| 6 | Will ≥2 commercial/SBIR teams commit ≥$10k on the open PDK, plus ≥3 deposits or ≥$15k of LOIs from distinct funded teams? | DD5 demand. The model's 40% willingness to pay and 15% close rate are invented (OMI.py inputs) | DD5 tests (i) and (ii), run only after DD2 dies | Only if DD2 fails; J-INT window 2027-01-11 → 02-10 | 3 |
| 7 | Can a 16 KB sky130 OpenRAM macro pass extracted-SPICE corners and a ≥1,000-point Monte Carlo? | DD5 buildability. No public ≥16 KB sky130 macro is silicon-verified (OMI §0) | 40 contract hours, $6.0k (OMI §10 test iii) | Same window as rank 6 | 3 |
| 8 | Will ≥2 buyers sign LOIs to cite an index in a live contract, and will ≥10 sign PO-price contribution agreements? | Whether the MOONSHOT option exists at all. Odds put at ~3% (J-CEIL) | Asks ride on DD2's 25 calls at $0 (LI §10) | K3 + K4, 2026-12-01; closes for good 2028-02-29 | 4 |
| 9 | Will SiliconExpert, Octopart/Nexar or Z2Data bundle a memory module at $0 marginal price? | DD2's ceiling and its exit path | K2 question on calls; quarterly check of pricing pages | Not in 90-day plan (K2 data only) | 2 |
| 10 | When does the DRAM price turn: 2028, or earlier? | DD2's price module (−57% in GLUT, −83% SEVERE) and the DD2 cash low at m16 (LI.py §6) | Free TrendForce quarterly releases; Micron earnings calls | Watch only | 5 |
| 11 | Does the final §5949 FAR rule keep supplier self-certification? | Whether C-64 reopens. It also bounds DD2's brand-level §5949 screen | Free Federal Register alert on FAR Case 2023-008 | Watch only | 5 |
| 12 | Are the 15 highest-weight external facts true? | Every model input that rests on a search snippet | A human with a browser can check most of them in one afternoon (§6) | Not scheduled | 6 |

---

## 1. The decisive unknown: does anyone pay?

**The question.** Will any memory-adjacent buyer pay this part-time founder, who is not a chip engineer, recurring cash? (DEC `biggest_unknown`; all three judges agree.)

**What the record holds.** It holds no deposit, no purchase order, no paid pilot and no signed LOI on any line, across 98 concepts and 7 deep dives (J-CEIL; J-INT). Every red-team round cut demand inputs that had been estimates:

| Input | Before red team | After | Source |
|---|---|---|---|
| DD2 trial conversion | 0.12 | 0.10 | LI §14.2 |
| DD2 U.S. SMB-OEM TAM | 6,000 | 3,000 | LI §14.2 |
| DD5 open-shuttle projects/yr | 298 | 228 | OMI §14.2 |
| DD6 close rate | 8% | 6% | J-INT `biggest_unknown` |

All seven deep dives died or were downgraded on willingness to pay, moat or channel, not on physics (J-EV). Objections: 186 raised, 0 refuted (RT scoreboard).

**How the 90-day plan answers it, and where it stops.**

| What the plan tests | Gate and threshold | Date | What a pass proves | What it does not prove |
|---|---|---|---|---|
| Can the founder legally sell to this buyer? | K0: a written carve-out covering the product, the SMB hardware-OEM industry and third-party PO contributions | 2026-11-09 | Permission to try | Anything about demand |
| Can a part-time founder reach buyers? | K6: 25 qualified calls booked in 21 days, from cold outreach outside the employer's network | 21-day window closes by 2026-11-29; gate 2026-12-01 (LI §11 #2) | That the funnel's ~20 trials/mo cap is reachable (LI.py `trials_cap_pt`) | That the calls convert |
| Will they put money down? | K1: ≥5 of 25 give a refundable $500 deposit or paid LOI at ≥$200/mo. J-INT tightens this to ≥3 of the 5 in cash | 2026-12-01 | Intent at a 20% call-to-deposit rate, which is the rate that supports the model's 10% conversion (LI.py §8) | Retention. **The deposits are refundable**, so a pass is a weak signal of recurring payment |
| Is it more than what they already have? | K2/K2b: <60% say an existing tool covers it, and ≥10 of 25 name a memory EOL, LTB deadline or die-revision PCN they missed in 2025–26 | 2026-12-01 | A real gap exists | Willingness to pay for closing the gap |
| Days 31–90 | Five design partners; ≥3 BOMs uploaded; ≥10 waitlist accounts; ≥3 partners sharing PO history (LI §4) | 2027-01-31 | Usage | Paid conversion. First revenue is m6 (2027-05) (LI.py §4) |

**What the plan cannot answer in 90 days.** It cannot measure real trial-to-paid conversion, churn (modelled at 2%/mo) or whether accounts survive the 2028 price turn. These first become observable at the m9 gate: ≥2 paying accounts by 2027-08-31 (model: 2.7). The m12 gate follows: ≥5 accounts and MRR ≥$1,700 by 2027-11-30; missing either stops the build (model: 6.7 accounts, $2,280) (LI §11 #7, #9).

**The judges' odds** [ESTIMATE] (J-EV; J-INT):

| Gate | J-EV | J-INT |
|---|---|---|
| P(K0) | ≈0.6 | ≈0.6 |
| P(K6 \| K0) | ≈0.5 | ≈0.45 |
| P(K1) | ≈0.35 | ≈0.35 |
| **P(pass)** | **≈0.10** | **≈0.09** |

**What each outcome does to the decision:**

| Outcome on 2026-12-01 | Action (DEC; J-INT) |
|---|---|
| K0 refused (by 2026-11-09) | The PRIMARY becomes NONE. Keep the day job and the $40k. DD5 needs its own written carve-out before it can run (J-CEIL) |
| K6 or K1 fails | Kill DD2. Run DD5's paid tests only if its $0 test (iv) has already passed |
| K1 passes at 5–7 of 25 | Run DD2 as a capped side business: ≤$34k ever, $5k cash floor, the stop rules in LI §11. Plan draw $30,850, cash low $9,150 at m16 (LI.py §10 PLAN) |
| K1 strong pass: ≥8 of 25 deposits, then ≥4 paying accounts at m9 | The only path to a salary inside 36 months. The conversion-0.15 run reaches $318,279 ARR at m36 and full-time at m33 in BASE, but **never in GLUT** (LI.py §10; J-EV) |

---

## 2. PRIMARY-specific open questions (DD2 lifecycle-intel)

| # | Question | Why it matters | Cheapest way to answer | Owner · date (90-day plan) |
|---|---|---|---|---|
| P1 | **Employer carve-out.** Will the employer sign one covering the product, the SMB hardware-OEM industry and third-party PO-price contributions? Can day-job peers be trial users? | The day job sits in the buyer's industry, and IP-assignment or moonlighting clauses can claim or bar the business (LI §6 FTO #3). The model already assumes no peer trials (`trials_at_launch` 6→4, LI §14.2). A refusal ends DD2 (LI §11 #1) | Read the agreement (60 min); ≤$500 flat-fee employment-attorney review covering DD2 and DD5; a one-page written request | Founder + employment attorney · request 2026-11-02 · K0 by 2026-11-09 |
| P2 | **Data terms (K5).** Octopart's API terms bar firms in component distribution, "including software developers building applications for that market", from pricing and availability use. They also bar historical trend use and caching beyond 24 h. Nexar tier prices are unpublished. DigiKey's display and redistribution terms were not found. Mouser was not checked (LI §6; `research/phase4/lifecycle-intel_notes.md` §11 #1) | The model assumes Nexar at $600/mo and a $2,000/mo display licence from m12; both are [ESTIMATE] with no quote. Fixed data costs total $3,167/mo from m12 and are UNVERIFIED (LI §2.1). Nexar at $1,000 plus display at $2,500 → BASE cash low −$1,884. K5 fails and the price line goes → $69,289 ARR, cash low $3,997 at m22 on the plan ($947 in BASE) (LI.py §10) | Written questions to support@nexar.com and DigiKey's API team: may a third-party SaaS display prices and stock in-app, may it use them historically, and at what monthly cost? (LI §10 step 3) | Founder · send days 2–10 · K5 by 2026-12-15. On fail, re-run K1 on a demo built from public prints; if that fails, kill (LI §11 #4) |
| P3 | **Real trial conversion.** Is it 10%, 8% or ≥14.7%? | Conversion ×0.7 → ARR m36 $104,740 and cash low −$4,943. 0.08 → $119,703 and a $486 cash low. A salary needs 14.7%, or 1.51× trial inflow (LI.py §7, §10) | K1 is only a proxy. Conversion is first measured after the m6 launch | Founder · K1 2026-12-01 (proxy) · measured 2027-05 → m9 gate 2027-08-31. Not answered in 90 days |
| P4 | **Substitution (K2/K2b).** Does free Octopart, $250/mo SiliconExpert or the EMS desk already cover the need? | "If a prospect has SiliconExpert, the SaaS is redundant" (LI §5). A K2 fail turns lifecycle into a free funnel only (LI §10) | Two questions on each of the 25 calls | Founder · 2026-12-01 |
| P5 | **Will OEMs contribute PO prices (K4)?** It needs ≥10 agreements signed by the legal function: 24 months of line-item POs, ≥$250k/yr of memory spend, not EMS-turnkey, no supplier-confidentiality conflict | It feeds the index option only. The SaaS funnel yields 9.3 contributors at m18 and 14.2 at m36, against the 15 needed (LI.py §6). The model's contributor share was cut 0.40→0.25 (LI §14.2) | Third ask on each call, plus a cell-map question (LI §10 step 2) | Founder · K4 2026-12-01 · m3 cell-map test 2027-02-28 (LI §11 #6) |
| P6 | **Antitrust and government-contracts opinions.** Are the cell rules safe? These are: ≥5 contributors per cell, ≥1-quarter lag, no contributor >25% of a cell, aggregates only. Can DLAD or GSAM price adjustments reference a third-party index? | The 1996 safety zones were withdrawn in 2023, and the 2024 RealPage complaint targets pooled pricing [UNVERIFIED-training] (LI §6). DLAD 16.203-4 says to use a BLS index first. Whether GSAM 552.238-120 allows a third-party index is UNVERIFIED (LI §7) | **Defer.** Commission the $1,000 consult and the $5,000 written opinion only if K3 and K4 pass (DEC MOONSHOT `spend`). On the plan (both deferred, the $1,950 test charged) the cash low is $9,150 at m16 and the max draw $30,850. Buying both after a K3+K4 pass gives $3,150 and $36,850: under the $5k floor and over the $34k cap unless results beat BASE (LI.py §10 PLAN rows) | Government-contracts attorney · only after 2026-12-01, and only on a K3+K4 pass |
| P7 | **Competitor responses.** SiliconExpert (Arrow): $250/mo Essentials. Z2Data: custom pricing; in Gartner's 2026 MQ. Lytica: real transaction prices, sold into EMS through NEOTech. Accuris: ≥$6,000 ACV, undercuts SiliconExpert by 20% in year one. Octopart/Nexar: free BOM tool, owned by Renesas, which is building lifecycle management (LI §5) | Arrow, Siemens and Renesas can bundle a memory module at zero marginal price (LI §5). The same names are the exit buyers if DD2 has <13 accounts at m18 (LI §11 #12). Nobody knows whether they would compete, ignore or acquire | K2 answers on the calls; a quarterly look at five pricing pages; no outreach to them before m18 | Founder · K2 data 2026-12-01; exit talks only at m18 (2028-05-31). Not otherwise in the 90-day plan |
| P8 | **C-72 supplier calls.** Will a Winbond or Nanya U.S. office, or a franchised Micron distributor, quote a pooled allocation agreement to a co-op holding no title or credit? | C-72 was killed as a standalone concept under Rule 1 at the Phase 7 gate. Its calls ride along at $0 (DEC `embedded_tests`). A "no" closes it for good (LI §11 #5) | Three calls (LI §10 step 4). **Use the same calls to ask about Micron Manassas DDR4 supply terms** (§5) | Founder · calls in week 3, 11-16 → 11-22 (`FIRST_90_DAYS.md`; LI §10 step 4 says days 7–14) · gate 2026-12-01 |
| P9 | **Is the TAM real?** The estimate is 3,000 U.S. SMB OEMs with $1–50M of BOM spend | $1M ARR needs ~238 accounts, which is 7.9% of 3,000 (LI.py §8). The 3,000 comes from a NAICS 334 count of 9,698 firms on an aggregator, seen only as a snippet and unchecked against Census (LI.py `tam_us_smb_oems`) | Census Statistics of U.S. Businesses (NAICS 334 by employment size), 1 hour | Not in 90-day plan |
| P10 | **Does the lifecycle line really hold flat in a glut?** | The model holds it at $5,774/mo in all scenarios. A 20% drop cuts GLUT m36 ARR by a further ~$14k (LI §12 caveat 3). It is the only cycle-proof module | Not testable before 2028. Proxy: ask callers whether EOL budgets were cut in 2023 | Not in 90-day plan |

---

## 3. FALLBACK-specific open questions (DD5 open-memory-ip)

DD5 runs **in sequence, never in parallel**. In November its only action is the two $0 letters. Its paid tests (≤$9.1k) run only if DD2 dies and test (iv) has passed (DEC).

| # | Question | Why it matters | Cheapest way to answer | Owner · date (90-day plan) |
|---|---|---|---|---|
| F1 | **Free large-macro release.** Will UCSC VLSIDA and Open Circuit Design state in writing that they do not plan silicon-characterized ≥16 KB open macros within 18 months? Will OCD sign a 12-month exclusivity as contractor? | Both are the likeliest free substitutes and the best contractors (OMI §3, §5). OCD's last commit was 2026-10-30, and Chips4Makers had 3 GF180 SRAM test chips by Jul-2026 (OMI §5). The model already assumes P = 0.6 of free GF180 macros, weighted from m24. Full shock → m36 ARR $34.0k; no release at all → $86.1k (OMI.py §4, §7). Pass probability is 15–25% by the author's estimate and ~10% by J-EV, because maintainers have little reason to promise | Two emails ($0, ~30 min). **No answer = FAIL** (OMI §10 test iv) | Founder · send 2026-11-02 · answer requested by 2026-11-20 · silence by 2026-12-01 = FAIL (OMI §11 #1; J-INT's day-14 reading noted in §8) |
| F2 | **16 KB buildability.** Can a 16 KB sky130 macro pass post-layout extracted SPICE at SS/1.62 V/125 °C and FF/1.98 V/−40 °C, plus a ≥1,000-point bitcell Monte Carlo, with ≤200 h to build the full line? Do the sky130 SRAM special-device models carry usable mismatch data? | No public ≥16 KB sky130 macro is silicon-verified. The published 16 KB attempt left only a log [VERIFIED-git]. The 2021 OpenRAM 4/8 KB test-chip configurations have no published measurements (OMI §0). Array efficiency is assumed at 30% (158.2 kbit/mm², 2.7× the 2 KB macro) until a real 32 KB macro is measured (OMI §2.1) | 40 contract hours at $150 = $6.0k (OMI §10 step 1). J-EV would commission it only after 2 LOIs of ≥$10k exist | Contract memory engineer · only if DD2 dies and F1 passes · not in the 90-day plan before 2026-12-01 |
| F3 | **Funded-team demand.** Will ≥3 distinct funded teams pay $500 deposits against ≥$2k orders, or sign ≥$15k of LOIs? Will ≥2 commercial/SBIR buyers commit ≥$10k, stay on the open PDK and accept "nominal lot measured, corners simulated, refund-capped warranty, no radiation data"? | Willingness to pay: "zero data" (`research/phase4/open-memory-ip_notes.md` §11). The model's 40% willingness to pay, 25% reply rate and 15% close rate are invented (OMI.py inputs). Close ×0.5 → m36 ARR $36.6k (OMI.py §7). Commercial S130 teams get SkyWater's bundled compilers, and many SBIR teams need SEE/TID data the plan does not fund (OMI §2.2, §3) | Landing page with real prices; 120 named contacts, ≥100 of them distinct funded teams; one hub event ≤$1.5k (OMI §10) | Founder · only if DD2 dies on 2026-12-01; J-INT window 2027-01-11 → 2027-02-10, never across the academic winter break |
| F4 | **GF180 non-U.S. fab.** Are wafer.space GF180MCU shuttle wafers fabbed in Singapore, and does any buyer care? Does the Synopsys–GF university pilot already give members free GF180 memory IP of ≥8 KB? | 148 of 228 projects/yr are GF180, so the supply-security axis covers only the 80 U.S.-fab projects (OMI §2.2). The Singapore fact is [REPORTED, via search snippet]. If the pilot gives free IP, its 40 projects leave the market and the model must be re-run (OMI §11 #9) | Read the wafer.space Run 3 page; one email to the Synopsys/GF University Partnership (OMI §10 step 4) | Founder · $0 letter in November (J-EV lists it) · answer by 2026-12-01 |
| F5 | **Exclusive contractor.** Will a memory engineer sign a 12-month exclusivity, or will a technical cofounder join, by m3? | The single point of failure. The founder cannot judge the timing sign-off they sell (OMI §9). No signature means kill (OMI §11 #2) | Ask OCD in the F1 email; fall back to OpenRAM alumni or Chips4Makers | Founder · OMI says 2027-02-28, but that date assumes a November start (§8) |
| F6 | **Shuttle cadence and academic procurement.** Will 2027 shuttles run on time, and will university POs land? | ChipFoundry runs a shuttle only when ≥50% full. TTSKY25b took ~8 months. wafer.space Run 3 has no dates (OMI §2.7). Academic POs lag ~2 months, and the m6 gate needs ≥2 university POs (OMI §11 #3) | Written calendar request to ChipFoundry and wafer.space (OMI §10 step 4) | Founder · $0 letter · not a gate in the 90-day plan |

---

## 4. MOONSHOT option (C-86 Memory Cost Escalation Index)

**Status.** No concept qualifies as a MOONSHOT. The red team killed C-86 as designed (RT-VC-DD2-01, FATAL). It survives only as a ~$0 option inside DD2's test (DEC). It is the only path in the study above $2M ARR: "<$0.5M (upside $2–10M)" if it displaces TrendForce in contract language (SCOR §6).

| # | Question | Why it matters | Cheapest way to answer | Owner · date |
|---|---|---|---|---|
| M1 | **Would anyone cite this index in a contract instead of TrendForce contract prints or open-book pass-through?** | DRAMeXchange's 8GB module contract price has been the de facto contract base since 2019. EMS houses pass memory through at invoice cost (LI §1). No U.S. OEM surcharge notice was found; the only examples are European (Unipi, Revolution Pi) (LI §3). No index-linked memory down-adjustment surfaced for 2018–19 or 2023 (LI §12). SGX's 2003 DRAM futures produced no market (J-CEIL; C-87) | K3: ≥2 of 10 index prospects sign LOIs that name a live contract or surcharge schedule and state why TrendForce and open-book do not serve it (LI §10) | Founder · 2026-12-01, on the DD2 calls |
| M2 | **Panel size.** Can a 15-member panel fill ≥3 grade-homogeneous cells with ≥5 independent buyers each? | SaaS funnel alone: 14.2 members at m36, so never published (LI.py §6). 10 seed contributors → published m20, 1.8 licences, $165,118 ARR at m36. With the gate lowered to 10 → m9, 2.8 licences, $174,279 (LI.py §10). $1M needs 115 licences at $8,700/yr (LI.py §8) | K4: ≥10 legal-signed contribution agreements, ≥70% of spend in ≤4 cells, ≥3 cells able to reach 5 contributors (LI §10) | Founder · K4 2026-12-01 · VET-01 publication test at m9 (2027-08-31) · hard close 2028-02-29 unless ≥15 members or an executed contract names the index (LI §11 #8, #11) |
| M3 | **Can the panel be made antitrust-safe, and can federal contracts use it?** | Covered under P6. Without counsel's sign-off the option closes at m9 (LI §11 #8) | Buy the $5k opinion only after K3+K4 pass (DEC) | Government-contracts attorney · after a K3+K4 pass only |
| M4 | **Is there demand when prices fall?** | The model now assumes none: `vol_down_weight` 1→0, and licences churn 3%/mo while prices fall (LI.py §0). So the index is no glut hedge (LI §12) | Unanswerable before 2028. Ask the K3 prospects whether their clause adjusts downward | Not in 90-day plan |

**Odds** [ESTIMATE]:
- P(K3+K4 pass) ≈ 5% (J-INT).
- P(passes and reaches an executed contract by m15) ≈ 3% (J-CEIL).
- P(venture scale) ≤ 1% (J-CEIL; J-INT).

---

## 5. Market and premise questions that could reopen killed concepts

### 5.1 The watch list (DEC `watch_list`)

Each trigger costs $0 to watch. None should be solicited while DD2's test runs: 15 h/week staffs one kill test at a time (J-EV `rejected`).

| ID | Killed concept | Reopen trigger | Honest ceiling if reopened | Source |
|---|---|---|---|---|
| C-64 | CleanBOM-5949 provenance software (DD1) | The final FAR rule in FAR Case 2023-008 drops reliance on supplier self-certification, or a module maker pays cash because its supplier refuses a die-source declaration. Then run DD1's $1.4k Stage-1 probe | ~$227k ARR at m36 (lifestyle scale) | DEC; J-INT; J-CEIL |
| C-48 | Private MoE inference appliance (DD6) | **Both** are needed. (a) A VAR or MSP commits in writing to ≥6 boxes/yr on its own paper. (b) A socket-pinned single-socket run shows ≥10 tok/s per user at **4** concurrent on a 1T-class MoE in a box quoting ≤$65k, or a blind evaluation shows regulated buyers prefer 200B–1T models | A pass still needs a 21% close rate to reach full-time | DEC `watch_list`; `04_DEEPDIVES/private-moe-appliance.md` §14.4 |
| C-91 | Authorized-aftermarket die bank (DD7) | A written OCM offer of authorized-aftermarket rights (wafers, test programs, marking) for a named EOL DRAM family, at an all-in pull cost ≤$1.53/die (the IRR break-even) | Plan B returned 0.29× of $11.49M in BASE. P(rights within 15 months) ≤5% | DEC; J-CEIL |
| C-12 | Battery-free MRAM backup card (DD3) | Unsolicited reseller sell-through or a commitment showing ≥33 cards/mo, the 36-month breakeven. BASE at 16/mo loses $29.8k | Best evidenced case nets $13–19k over 36 months | DEC; J-INT; `research/phase5/responses_nv-continuity-modules.json` |
| C-65 | Hi-rel DDR4/LPDDR4 MCM (DD7) | A hi-rel cofounder arrives with an existing x72 design-in and ≥3 evaluation LOIs at ≥$1,200/unit | BULL year-10 revenue $26.48M, but it needs $5.5–11.5M and is ~22%/yr gross before dilution | DEC; J-CEIL |

### 5.2 Premise questions the study could not close

| Question | Why it matters | What we know (dated) | Cheapest way to answer | Owner · date |
|---|---|---|---|---|
| **§5949 FAR final rule.** Text, date, COTS scope, the "reasonable inquiry" standard, any DFARS counterpart | It reopens C-64 if it requires third-party or die-level verification, and kills it for good if COTS is exempted or the date slips past 2028-12-31 (DD1 §11 #9). It also bounds DD2's brand-level screen, a Q5 feature (LI §8) | Proposed 2026-02-17 (FR Doc 2026-03065). Comments closed 2026-04-20. No final rule and no DFARS counterpart as of 2026-11-01. Effective 2027-12-23, confirmed. A 2028-12-23 commercial phase-in and a 72-hour reporting window each rest on a single source (LAND §7.2, §7.3, §10.5 #1; V1 1g) | A free Federal Register email alert on FAR Case 2023-008 | Founder · set up once; not a 90-day gate |
| **2027–28 DRAM turn timing** | GLUT cuts DD2's m36 ARR from $149,629 to $104,077, and SEVERE to $83,031. The price paths split at m14 (2028-01), just before DD2's m16 cash low (LI.py §6). Price-arbitrage concepts must be cash-positive by end-2027 (LAND §10.3) | House call: peak 4Q26–2Q27, turn 2028, glut 2H28–29 only if AI capex slows. NAND goes to surplus in 2H27 (TrendForce 2026-07-30). Forecasters disagree: Micron, UBS and Barclays see tight supply through 2028; Bloomberg Intelligence sees balance ~4Q27 and oversupply in 2028; BofA sees −10% ASP in 2028 (LAND §2.3, §10.4 #11) | Free TrendForce quarterly contract releases; Micron's quarterly calls. Signals: NAND contract declines, the first negative DRAM QoQ print, DDR4 spot falling | Founder · quarterly · not a 90-day gate |
| **Micron Manassas long-lifecycle DDR4 supply terms** | If SMB OEMs can buy Manassas DDR4/LP4 through distribution with multi-year supply commitments, EOL and LTB urgency falls further. That hits DD2's lifecycle line and LTB studies. `ltb_attach` was already cut 1.5%→1.25% because "Micron's ongoing DDR4 commitment blunts EOL panic" (LI.py inputs). It also bears on C-91 and C-61 | 1-alpha DDR4/LP4 since 2026-05-22. DDR4 is ~7% of Micron DRAM output. Micron is the only supplier publicly committed to ongoing DDR4/LP4, with Strategic Customer Agreements naming Ford, GM and seven auto Tier-1s. Whether SMB OEMs can get those terms is unknown (LAND §3.3) [REPORTED] | Ask the franchised Micron distributor on DD2's C-72 call (P8), $0 | Founder · week 3 of DD2's test (11-16 → 11-22) |
| **SpecTek wafer/KGD availability and MOQ** | Die access gates every die-dependent concept: C-91, C-65 and U.S. module plays. It was a Phase 3 scoring rule (LAND §10.3 #5) | **Still open.** No public MOQ, distributor list or allocation statement. "The email … has no search substitute" (LAND §10.5 #3; V3 2b). Micron's 10-K lists wafers as a sales form but no KGD program (LAND §0 item 10) | One email to SpecTek, $0 | Not in 90-day plan; optional |
| **100% memory tariff / Section 232 Phase 2** | The study found no "Made in USA" premium for memory. Memory pays 0% under Section 232 Phase 1, and TAA treats Korean, Taiwanese and Japanese DRAM as equal (LAND §0 item 7). A real U.S.-origin tariff would change the module and legacy-supply kills | The 100% threat (2026-01-16) was unimplemented as of 2026-11-01. No Phase 2 was found. The §301 treatment of memory from 2026-07-24 is unconfirmed (LAND §7.3) | Federal Register alert on Section 232 semiconductors | Not in 90-day plan |
| **SkyWater Fab 25 6T SRAM access for outside customers (C-36)** | It is the only live mission-literal "make memory in the U.S." concept. It is alive only because it was never red-teamed, its founder-fit is 1, and it is T2 (J-INT `rejected`) | The card marks outside access to a characterized 6T bitcell/PDK STILL-UNVERIFIED (J-INT) | One email to SkyWater; it matters only if a hardware cofounder appears | Not in 90-day plan |
| **BIS affiliates rule and CXMT status** | Shapes provenance demand (C-64) | The suspension runs to 2026-11-09. Without a BIS notice the rule returns 2026-11-10. CXMT was not on the Entity List as of 2026-08-31 and is on the 1260H list (LAND §7.2, §10.5 #8) | Federal Register check on 2026-11-10 | Not in 90-day plan |

---

## 6. Evidence-quality gaps

### 6.1 Why nearly every external fact is search-snippet grade

- **Search budget.** WebSearch had a 200-call per-turn budget shared by every agent. Several Phase 1 and Phase 2 agents found it spent before their first query (ASSUMPTIONS A-A3-1, A-p1-fabs-1, A-C-1; `research/phase1/funding_export.md`). Phase 4 deep dives had ~28–32 calls each (`research/phase4/*_notes.md`).
- **Blocked hosts.** WebFetch could not reach, among others:
  - trendforce.com, sec.gov and investors.micron.com (refused in the proxy log; `research/phase1/us_fabs.md`);
  - everspin.com and skywatertechnology.com (same file; ASSUMPTIONS A-p1-fabs-1);
  - nist.gov and en.wikipedia.org (`research/phase1/funding_export.md`);
  - sandia.gov (A-E-1) and arxiv.org (A-p3-audit-06-1, -08-8);
  - weebit-nano.com and govinfo.gov (A-A2-18; A-p4-provenance-recert-1);
  - accuristech.com and siliconexpert.com, DD2's two price anchors (`research/phase4/lifecycle-intel_notes.md`).
- **Phase 1b tally.** Phase 1b ran 114 searches. All 11 fetch attempts failed DNS. Of 113 items: 56 confirmed, 28 corrected, 1 refuted, 23 still unverified, 5 new. **None is [VERIFIED]** (LAND §10.5).
- **The exceptions.** Only git-hosted data was read first-hand:
  - DD5's macro sizes, wafer.space listings and Tiny Tapeout counts are [VERIFIED-git] (OMI §2);
  - DD6's KTransformers benchmarks;
  - FAR 16.203-1 via the GSA GitHub mirror (LI §7).
- **What that means.** The FALLBACK's core gap is better evidenced than the PRIMARY's. **Every external fact under DD2 is snippet-grade** (LI header).

These gaps come from the study's tooling, not from the facts being hard to find. A human with a normal browser can close most of the table below in one afternoon. LAND §10.5 lists the hosts a re-run would need to allow: federalregister.gov, govinfo.gov, congress.gov, nist.gov, sec.gov, techinsights.com, weebit-nano.com, amcompute.com, mayerbrown.com and wiley.law.

### 6.2 The 15 highest-weight facts to re-verify from primary sources

Ranked by the decision they feed. "If wrong" names the consequence.

| # | Fact as recorded | Grade | Feeds | Primary source to check | If wrong |
|---|---|---|---|---|---|
| 1 | Octopart's API terms bar distribution-market software developers from pricing and availability use, bar historical trend use, and cap caching at 24 h (LI §6) | [REPORTED] | K5; DD2 price module | Full text of octopart.com/api/legal and nexar.com/api/legal, plus a written answer from support@nexar.com | If looser, K5 risk falls. If stricter, the K5-fail case applies ($69,289 ARR) |
| 2 | Nexar Standard/Pro prices are unpublished; DigiKey display and redistribution terms not found (LI §2.1, §6) | gap; model uses [ESTIMATE] $600 and $2,000/mo | DD2 COGS ($3,167/mo fixed from m12) | nexar.com/compare-plans plus a Nexar sales quote; DigiKey API terms of use (developer.digikey.com) plus its API team | A COGS ×1.3 run already gives a −$6,383 cash low (LI.py §7) |
| 3 | SiliconExpert BOM Manager Essentials is $250/mo; Accuris's minimum is $6,000 ACV with a 20% year-one undercut (LI §2.1, §5) | [REPORTED]; WebFetch failed on both | DD2's $249 / $649 price anchors | siliconexpert.com BOM Manager page; accuristech.com offer terms; a sales quote from each | Price ×0.7 → cash low −$11,109 (LI.py §7) |
| 4 | AdvaMed: 75–80% of medtech products contain memory; 75% of members report constraints, 88% price increases, 63% allocation problems (LI §3) | [REPORTED] | DD2 buyer-pain case; medtech target #9 | AdvaMed's 2026-08-17 release and the survey's sample size and method | It weakens the only quantified evidence of pain |
| 5 | ~3,000 U.S. SMB hardware OEMs, from NAICS 334 = 9,698 firms via an aggregator (LI.py `tam_us_smb_oems`) | [ESTIMATE] on a snippet | DD2 ceiling: 7.9% penetration for $1M (LI.py §8) | Census Statistics of U.S. Businesses, NAICS 334 by employment size; bls.gov/iag/tgs/iag334.htm (logged) | Lower → the ceiling is below $0.1–0.3M |
| 6 | Micron Manassas has made 1-alpha DDR4/LP4 for long-lifecycle buyers since 2026-05-22. Micron is the only supplier publicly committed to DDR4/LP4, with SCAs naming Ford, GM and Tier-1s. DDR4 is ~7% of its output (LAND §3.3) | [REPORTED] | DD2 lifecycle/LTB demand; C-91; C-61 | Micron press release and FY2026 10-K (investors.micron.com and sec.gov were blocked) | If supply opens to SMB OEMs, lifecycle urgency falls (§5.2) |
| 7 | 4Q26 conventional DRAM contract +10–15%. The model anchors DDR5 at $20.37/GB and RDIMM at $1,650. The "~+20%" October revision rests only on an AI-generated summary (LAND §10.4 #2, #10; V4 5d, 5g) | [REPORTED-P] / [ESTIMATE] | Every model's price deck; DD2 price module | TrendForce press center, 2026-09-30 release and the DRAMeXchange contract table (trendforce.com was blocked) | It shifts the BASE path; the GLUT and SEVERE lines are relative |
| 8 | NAND turns to surplus in 2H27. 2028 bit growth is low-20s% to >30%. BofA sees −10% ASP in 2028 (LAND §2.3) | [REPORTED] | Timing of GLUT/SEVERE (m14 = 2028-01) | TrendForce 2026-07-30 release; Micron FQ1-FY27 earnings call (Dec 2026) | An earlier turn compresses DD2's price module before breakeven (m17) |
| 9 | §5949: FAR Case 2023-008 is only proposed (2026-02-17). Supplier certification after "reasonable inquiry" suffices. Part A covers COTS. Effective 2027-12-23 (LAND §0 item 8; V1 1g) | [REPORTED-P] | C-64 watch; DD2 §5949 screen | federalregister.gov FR Doc 2026-03065 (URL logged in LI §13); the regulations.gov docket; NDAA FY2023 §5949 statutory text on govinfo.gov | It changes whether C-64 reopens or dies for good |
| 10 | No "Made in USA" premium: TAA designated countries include Korea, Taiwan and Japan. Section 232 Proclamation 11002 does not name memory (0%). §301 memory treatment from 2026-07-24 unconfirmed (LAND §7.3) | [UNVERIFIED-H] / [REPORTED-P] | The kills of U.S. module and legacy-supply concepts (LAND §10.2) | FAR 25.003 designated-country list on acquisition.gov; the Proclamation 11002 annex HTS list; the USTR §301 notice | A real U.S.-origin premium would reopen killed module concepts |
| 11 | SBIR PI must spend >50% of their time at the small business, which excludes the founder. S.3971 was signed 2026-04-13 and runs to 2031-09-30; one source gives the public-law number (LAND §0 item 9; V1 2b) | [REPORTED] / [REPORTED-P] | Rejection of every SBIR path; DD5's T2 revival route | SBA SBIR/STTR Policy Directive; S.3971 text on congress.gov; nist.gov SBIR eligibility page (logged) | Non-dilutive funding paths would reopen for device concepts |
| 12 | The largest free macros are 4 KB on sky130 and 1 KB on GF180. Only a 1 KB sky130 macro is silicon-verified. The 16 KB attempt left only a log. OpenRAM is at v1.2.50 (A3) or v1.2.48 (snippets) (OMI §0, §5; V2 5c) | Sizes [VERIFIED-git]; silicon status [REPORTED]; version conflict | DD5's core gap and F2 | VLSIDA/OpenRAM GitHub releases and PyPI; UCSC's OpenRAM test-chip papers (arxiv.org was blocked); the F1 email | If larger silicon-proven macros exist, DD5 has no gap |
| 13 | wafer.space GF180MCU wafers are fabricated by GlobalFoundries in Singapore (OMI §2.2) | [REPORTED, via search snippet] | DD5 supply-security axis (80 of 228 projects) | crowdsupply.com/wafer-space/gf180mcu-run-3 (logged), plus written confirmation from wafer.space | If U.S.-fabbed, the axis covers ~3× more projects |
| 14 | SkyWater S130 "already offers SRAM compilers" (Infineon IP licence, 2025-07-29). What memory IP the Synopsys–GF pilot gives members is unknown. SkyWater's DMEA Category 1A status after the IonQ close is unconfirmed (OMI §2.2, §7) | [REPORTED] / unknown | DD5's commercial exclusion; market size; C-36 | SkyWater S130 PDK/IP pages (skywatertechnology.com was blocked) or SkyWater sales; the Synopsys/GF University Partnership; the DMEA Trusted Supplier list | Free IP on the pilot removes 40 projects/yr (OMI §11 #9) |
| 15 | Index premise: BLS has no DRAM-specific PPI. DLAD 16.203-4 says to use BLS first. Whether GSAM 552.238-120 allows a third-party index is unknown. DRAMeXchange's 8GB module contract base has been in use since 2019 (LI §1, §7) | [REPORTED] / [UNVERIFIED] | MOONSHOT (C-86) K3 | BLS PPI index list on bls.gov; GSAM 552.238-120 full text on acquisition.gov (logged); DLAD 16.2; TrendForce 2018-11-05 | A BLS DRAM index would remove the federal opening entirely |

### 6.3 Unverified items that change no pick

These stay open but move nothing. They are listed so nobody spends time on them first:
- the 2023 DDR5 contract trough of ~$1.60/GB (~$3.2 per 16Gb chip), which rests on prior knowledge with no URL found this session (01_LANDSCAPE.md §5.3 tags it [UNVERIFIED]); the severe-glut line uses the model's $2.04/GB, so it changes no pick — check TrendForce's 2023 DDR5 contract releases;
- the 1-beta/1-gamma DRAM wafer cost, which is "the largest model swing, but it changes no decision" (LAND §10.5 #6; V4 2a);
- Samsung and SK hynix 1b/1c die areas (V4 1f);
- Sandia HZO and Penn AlScN licensing (V2 3a, 3b);
- Nantero's status (V2 6b);
- Nanya, Etron and Intelligent Memory KGD programs (V3 3a–3e);
- SMART/Penguin U.S. assembly (V3 5c);
- SK tes (V3 6d);
- Micron's DMEA status (V1 7b);
- NAPMP status after Natcast (V1 3c);
- Weebit's fee for a fabless startup (`research/phase4/open-memory-ip_notes.md` §11).

All of them sit under concepts that are killed.

---

## 7. Model assumptions most likely to be wrong

### 7.1 DD2 — `models/lifecycle-intel.py` (BASE: ARR m36 $149,629; cash low $6,100 at m16. PLAN: cash low $9,150 at m16, max draw $30,850)

| Input (value) | Basis | Sensitivity (LI.py §7, §10) | How it gets measured |
|---|---|---|---|
| `trial_conversion` 0.10 | [ESTIMATE], cut from 0.12 by the red team | ×0.7 → $104,740, cash low −$4,943. 0.08 → $119,703, cash low $486. ×1.3 → $200,710. 0.15 → $318,279, salary at m31. The salary needs 14.7% | K1 (proxy); m9 and m12 gates |
| Price: Team $249, Pro $649, blended $340 | Anchored on SiliconExpert's $250 and Accuris's $6k ACV (snippet-grade) | ×0.7 → $104,740, cash low **−$11,109**. ×1.3 → $194,517 | K1 asks at ≥$200/mo; fact #3 |
| Data fees: Nexar $600/mo; display licence $2,000/mo from m12 | No quote exists | COGS ×1.3 → cash low −$6,383. Nexar $1,000 + display $2,500 → −$1,884. K5 fail → $69,289, cash low $947 (PLAN: $3,997) | K5 written quote by 2026-12-15 |
| `churn_base` 2%/mo; `churn_glut_extra` +8%/mo | SMB SaaS norm [ESTIMATE] | ×0.7 → $165,201. ×1.3 → $135,999 | Observable from m7 |
| Funnel: `trials_cap_pt` 20, `trials_growth` 2, `trials_at_launch` 4 | 15 h/week (ASSUMPTIONS A-03) | Restoring the Phase 4 funnel (0.12, 25, 6, m5) → $298,939 and full-time at m33, but never in GLUT | K6 (25 calls in 21 days) |
| `lifecycle_floor` 0.4; lifecycle line held flat in glut | AdvaMed allocation stat [ESTIMATE] | −20% lifecycle in GLUT → a further ~−$14k ARR (LI §12) | Only in 2028 |
| `tam_us_smb_oems` 3,000 | Aggregator snippet [ESTIMATE] | Sets penetration: 7.9% for $1M, 15.9% for $2M (LI.py §8) | Census check (fact #5) |
| `seed_contributors` 5; `panel_min_contributors` 15 | K4 bar | 0 seeds → no change. 10 seeds → $165,118, published m20 | K4 |
| `antitrust_opinion` $5,000 at m2, charged unconditionally in BASE | RT-HYP-DD2-07 | DEC defers it. LI.py §10 PLAN (opinion deferred, $1,950 test charged): cash low $9,150 at m16, max draw $30,850. PLAN + index option passes: $3,150 and $36,850 | Decided: defer (K3+K4) |
| DDR5 contract path as the demand driver | `models/dram_cost_stack.py` | These buyers mostly purchase industrial DDR3/DDR4, eMMC and NOR, whose prices move with EOL and allocation (LI §12 caveat 4) | Structural; untested |

### 7.2 DD5 — `models/open-memory-ip.py` (BASE: ARR m36 $65.7k; cash low $4.0k at m15)

| Input (value) | Basis | Sensitivity (OMI.py §7) | How it gets measured |
|---|---|---|---|
| `close_rate_of_replies` 0.15; `reply_rate` 0.25 | "Still invented" (OMI §2.3) | Close ×0.7 → $49.1k. ×0.5 → $36.6k. ×1.3 → $80.2k | Tests (i) and (ii) |
| `share_of_those_that_pay` 0.40; `share_needing_memory` 0.30 | No willingness-to-pay data; ~10 of 51 wafer.space Run 2 listings mention SRAM | Sets the 27 paying projects/yr and the $424.4k/yr ceiling (OMI.py §2) | Test (i) |
| Project counts: ChipFoundry 30, Cadence 20, MOSIS/Commons/other 30 | [ESTIMATE], halved by the red team | Sets 228/yr and an outreach cap of 19 teams/mo | F4 and F6 letters |
| `P_GF180_FREE` 0.6 from m24 | OCD and Chips4Makers already have silicon | No release → $86.1k. Full shock → $34.0k. GLUT + shock → $27.5k | Test (iv); §11 #7 |
| `academic_share` 0.70 | Red team, from 0.60 | 0.80 → $55.1k | Test (ii) |
| Price ×1.0 (sub $200/$800; service $3k/$10k; licence $12k) | [ESTIMATE] | ×0.7 → $46.0k. ×1.3 → $85.4k. Only price ×1.3 + close ×1.3 + no free release pays the founder (m22) | Test (i) deposits at list price |
| Contract rate $150/h and hours per job | Exclusivity premium [ESTIMATE] | COGS ×1.3 → cash low $2.8k | F5 SOW |
| Licence attach 0.15/yr; DoD channel 0.04/mo | Red team | Licences removed → run-rate $152.9k at m36 (ARR unchanged) | Test (ii) |
| Model calendar: m1 = Dec-2026, with the $9.1k kill-test spend at m1 | Assumes a November test | DEC runs the test only after DD2 fails, so every DD5 date slips ~1–2 months (§8) | Re-run before any DD5 spend |

### 7.3 Structural assumptions shared by both models

- **Founder time.** ~15 h/week and $40k deployable (ASSUMPTIONS A-03). Neither model charges for the founder's time. At $25/h, both picks have expected value at or below zero (J-EV; J-INT).
- **No income tax.** Neither model has an income-tax or self-employment-tax line (RT-VC-DD1-07, "same in DD2–DD5"). Cash at m36 is pre-tax.
- **Glut timing.** The glut starts at m14 (2028-01) in both (ASSUMPTIONS A-05). An earlier turn hurts DD2 more than DD5.

---

## 8. Inconsistencies found in the inputs (for the Phase 7 gate)

None of these changes a pick. Each should be corrected or footnoted.

*Phase 7 gate status (g-mission-critic, 2026-11-01): items 1–3 are now resolved in `research/phase6/decision.json`. `watch_list` C-48 reads "4 concurrent users". `MOONSHOT.confidence` gives the 0.7–0.8 confidence in NONE and labels 0.03 as the C-86 option's odds. `PRIMARY.spend` gives ~$1,950 planned (~$2,950 only if the consult is not deferred), and `PRIMARY.plan_cash` quotes the PLAN rows of `models/lifecycle-intel.py` §10. Items 4–8 are left as flagged.*

1. **C-48 trigger.** DEC `watch_list` reads "≥10 tok/s per user at **2** concurrent users on the L box". DD6 §14.4 and all three judges say "≥10 tok/s per user at **4** concurrent on a 1T-class MoE in a box quoting ≤$65k". "2 concurrent" is DD6's separate K5 U.S.-origin test.
2. **MOONSHOT confidence.** DEC says "0.03–0.8 that 'none qualifies' is the right call". The 0.03 is J-CEIL's probability that C-86 *passes and reaches an executed contract*, not confidence in NONE. Confidence in NONE is 0.7 (J-EV) and 0.8 (J-INT).
3. **DD2 test budget.** DEC PRIMARY cites "~$2,950 planned", which includes LI §10's ~$1,000 government-contracts consult. DEC MOONSHOT defers that consult until K3+K4 pass. If it is deferred, the planned pre-pass spend is ~$1,950.
4. **DD5 calendar.** OMI §10–§11 and OMI.py (m1 = Dec-2026, $9.1k at m1) assume the test runs 2026-11-02 → 12-01. DEC sequences it after DD2 fails; J-INT gives 2027-01-11 → 02-10. So OMI's m3 exclusivity date (2027-02-28), m6 gate (2027-05-31) and first revenue at m4 (Mar-2027) are early, and need re-dating and a model re-run.
5. **Test (iv) deadline.** J-INT says silence by **day 14** fails. J-EV asks for an answer by **2026-12-01**. OMI §10 schedules the letters for days 7–20. *Phase 7 (g-decision-docs): this file and `FIRST_90_DAYS.md` now use the deep dive's own date, OMI §11 #1: answer requested by 2026-11-20, and no written answer by 2026-12-01 = FAIL.*
6. **Small number drift in LI against LI.py.** *Phase 7: resolved. LI §2.3 now reads $200,710, LI §2.4 ~238 accounts (7.9%) and "at most 1.8 licences", matching LI.py §7, §8 and §10.* The original drift:

   | Item | LI (deep dive) | LI.py (model) |
   |---|---|---|
   | Conversion ×1.3, ARR at m36 | $201,001 (§2.3) | $200,710 |
   | Accounts for $1M ARR | ~235, 7.8% (§2.4) | ~238, 7.9% |
   | Licences by m36 if 10 seeds deliver | "at most 2.8" (§2.4) | 1.8; 2.8 needs the panel gate lowered to 10 |

7. **Role labels in the deep dives.** LI §0 recommends DD2 as a "side line, demoted from FALLBACK", run "alongside DD1/DD3 customer discovery" (both now killed). OMI §0/§14.5 says DD5 is "not PRIMARY, not FALLBACK". DEC overrides both by promoting them, which is a legitimate decision. Readers of the deep dives alone will see the opposite labels.
8. **DD5 expected value.** OMI §14.5's "+$5–15k" includes the founder's own $40k in end cash. J-INT corrects the gain if it passes to $48.4k in BASE, $20.4k in GLUT and $5.1k in SEVERE.
