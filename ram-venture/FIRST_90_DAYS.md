# FIRST 90 DAYS: Mon 2026-11-02 → Sun 2027-01-31

`FIRST_90_DAYS.md` · Phase 6 (Decision) · As of 2026-11-01 · This plan carries out `research/phase6/decision.json` and does not change it.

**Source abbreviations used below**

- **DEC**: `research/phase6/decision.json`. **J-EV / J-CEIL / J-INT**: the three judge files in `research/phase6/`.
- **LI**: `04_DEEPDIVES/lifecycle-intel.md` (DD2, PRIMARY). **LI.py**: the printed output of `python3 models/lifecycle-intel.py`, re-run 2026-11-01, exit 0.
- **OM**: `04_DEEPDIVES/open-memory-ip.md` (DD5, FALLBACK). **OM.py**: the output of `python3 models/open-memory-ip.py`, re-run 2026-11-01, exit 0.
- **LS**: `01_LANDSCAPE.md`. **RT**: `05_REDTEAM.md`.
- **[PLAN]** marks something this plan sets that the record does not: hours per call, some calendar dates, how money is split into tranches. Each one is logged in `research/assumptions/p6-first90.md`.

---

## 0. The kill experiment first: what these 90 days are for (read this first)

- **This is a test plan, not a launch plan. It opens with one kill experiment that costs well under $10k:** DD2's 29-day test, Mon 2026-11-02 → Tue 2026-12-01 (LI §10). It spends **$1,950** planned (~$2,950 only if the deferred $1,000 consult is spent; hard cap $5,000; DEC) and about **60 founder hours** to answer one question: will any memory buyer pay this part-time founder at all? DEC calls this the study's biggest unknown: "the study contains no deposit, PO or paid pilot."
  - **Gates:** K0 written employer carve-out by Mon 2026-11-09; K6 25 qualified calls booked within 21 days and K1 ≥5 of 25 refundable $500 deposits or paid LOIs at ≥$200/mo by Tue 2026-12-01; K5 data terms ≤$1,000/month by Tue 2026-12-15 (LI §10–§11; DEC). Weeks 1–5 below run it day by day; weeks 6–13 run the branch it picks.
- **The study found nothing venture-scale.** In DEC's words: "No venture-scale opportunity to make RAM, or something better than RAM, in the U.S. survived for a founder with under $50k." Seven deep dives drew 186 red-team objections and none was refuted. Five were killed and two downgraded (RT scoreboard).
- **Expect a no.** The judges put the chance of passing K0, K6 and K1 together at about **0.10 (J-EV)** and **0.09 (J-INT)**. DD5's test passes 15–25% of the time by its author's estimate (OM §10), or about 10% by J-EV's.
- **A pass buys a side business, not a company.**
  - BASE ARR is **$69,915 at m18** and **$149,629 at m36**. GLUT gives $104,077 and SEVERE $83,031.
  - Breakeven with the founder unpaid comes at m17 (2028-04).
  - The $10k/month salary is **never** covered within 36 months unless trial conversion reaches **≥14.7%** (LI.py §6, §10).
  - The first subscription revenue arrives at **m6 = 2027-05** (LI.py §4). **No branch earns subscription revenue inside these 90 days.**
- **One test at a time.** DD2 runs first. DD5 gets only $0 letters until DD2 has died. 15 hours a week cannot staff both tests. DD2's max draw on this plan ($30,850; LI.py §10 PLAN) and DD5's ~$36k draw (J-CEIL) also cannot both fit inside $40k (J-INT FALLBACK rationale, point 6).
- **The most likely ending is Branch C:** stop on 2026-12-01, keep the day job, and keep **$38,050** of the $40k.

## 1. Standing rules for all 13 weeks

| Rule | Source |
|---|---|
| About 15 h/week alongside the day job | Founder profile (MISSION); LI.py input `trials_cap_pt` ("15 h/wk = ~65 h/month") |
| ≤$500 before K0; DD2 test **~$1,950 planned** (~$2,950 if the $1,000 consult is not deferred), hard cap **$5,000**; **≤$34k ever**; **$5k cash floor** | DEC PRIMARY.spend |
| Plan cash check: max founder draw **$30,850** vs the $34k cap; cash low **$9,150** at m16 (2028-03) vs the $5k floor. If K3+K4 pass and the deferred $6k is spent: **$36,850** and **$3,150**, over the cap and under the floor unless results beat BASE — so the **funding rule** applies: the deferred $6k is spent only if index prepayments (≥$6k) or a ≤$10k note from an index LOI signer/strategic cover it; otherwise the index stays closed and the cap/floor hold | LI.py §10 PLAN rows; DEC PRIMARY.plan_cash; DEC MOONSHOT.funding_rule |
| $40,000 deployable | LI.py `founder_cash` (ASSUMPTIONS A-03) |
| The $1,000 government-contracts consult and the $5,000 antitrust opinion wait until K3 **and** K4 pass. November spend is therefore **$1,950**, with $1,000 held in reserve | DEC MOONSHOT.spend; LI §10 line items |
| DD5: $0 in November (letters only). Up to **$9.1k** only if DD2 fails on 2026-12-01 **and** both no-release statements arrive | DEC FALLBACK.spend |
| No code until K0 is signed. No domain, no Sales Navigator and no contact with any prospect before K0 either | LI §10 step 0b; J-INT and J-EV Monday actions |
| None of the 60 contacts may come from the employer's network | LI §10 step 2 |
| Collect **signed** contribution agreements, never PO data, until a written antitrust opinion approves the cell rules | LI §6, FTO risk #2 |
| The §5949 flag is brand-level only, labelled "not die-level; a negative is not evidence of compliance". It stays out of the pitch to rugged-server prospects | LI §10 step 1; LI §3 #4 |
| Deposits are refundable. Hold them in a separate account. They count as neither spend nor revenue | [PLAN] |
| Thresholds are locked on 2026-11-02 and never edited afterwards | LI §10 step 0 |

---

## 2. Week-1 checklist (one page)

**MONDAY 2026-11-02, morning: ≤2 hours, $0** (DEC `monday_action`, in this order)

- [ ] **1. (20 min) Lock the thresholds.** Copy DD2's K0–K6 pass/fail thresholds from LI §10 (the sheet in §3 below) into a dated document. Email it to an outside advisor, ideally the procurement advisor described in LI §9, so the thresholds are locked. *Decide before you send it* whether to adopt J-INT's stricter K1 reading: at least 3 of the 5 commitments in cash. DEC does not include that rule, so it binds only if it is in this email.
- [ ] **2. (60 min) Check the employment agreement and ask for the carve-out.** Read it for IP-assignment, moonlighting, non-compete/non-solicit and confidentiality clauses. Then send HR a written carve-out request covering:
  - the product: a memory lifecycle, EOL and cost SaaS;
  - the industry: U.S. SMB hardware OEMs;
  - the collection of third-party PO-price contributions;
  - the working terms: built on personal time and personal equipment, with no employer data, contacts or customers.

  Ask for a signature by **Mon 11-09**.
- [ ] **3. (20 min) Send DD5's $0 no-release question to UCSC VLSIDA and Open Circuit Design.** Draft: *"Do you plan to publish silicon-characterized SRAM macros of 16 KB or more for sky130 or GF180 under an open licence within the next 18 months? A one-line written answer by 2026-11-20 is all I need."* To OCD, add: *"Would you consider a 12-month contract engagement that includes exclusivity on free release of such macros?"* (OM §10 step 4.) **No answer counts as FAIL** (OM §10 (iv); DEC). If the employment agreement bans all outside business outright, hold this email until the attorney review (J-INT).
- [ ] *(20 min, inside the 2 h)* Book a one-hour employment-attorney review for this week, ≤$500 (LI §9; J-EV). Ask the attorney to cover DD5 as well (J-INT).

**Rest of week 1**

- [ ] **Tue 11-03 (day 2): data-terms emails (K5).** Send to support@nexar.com and to DigiKey's API team. Ask: "May a third-party SaaS display your prices and stock in-app? May it use them historically? What does that licence cost per month?" (LI §10 step 3)
- [ ] **Wed 11-04: the four remaining DD5 letters** (OM §10 step 4):
  - **ChipFoundry** and **wafer.space**: dated 2027 shuttle calendars, marketplace terms, and any plan for free large macros.
  - **Cadence**: the next SKY130 run, and whether it would bundle macros.
  - **Synopsys/GF University Partnership**: what memory IP the GF180MCU pilot gives its members.
- [ ] **By Fri 11-06:** the attorney review (≤$500). If the wording of Monday's request exposes the founder, send a corrected version before 11-09.
- [ ] **Templates** (no code; legal review comes later):
  - $500 refundable deposit or paid LOI for 6 months of Team at $249/mo.
  - Index LOI (K3 wording).
  - Contribution agreement (K4 terms plus the cell rules: ≥5 contributors per cell, a lag of at least one quarter, no contributor above 25% of a cell, aggregates only).
- [ ] **Prospect list: 60 named contacts from public sources only**, at least 10 of them index prospects (LI §3). Sources:
  - Thomasnet and Trenton rugged-server lists: OnLogic, Amplicon USA, Trenton Systems, CP Tech USA, Core Systems USA, WINSYSTEMS, Industrial Computers Inc.
  - AdvaMed and MDMA directories for medtech.
  - IPC/SMTA chapters for tier-2/3 EMS.
  - GSA eLibrary for CGP-member resellers.
  - Unipi and Revolution Pi/KUNBUS as index prospects.
- [ ] **Do NOT:** write code, buy a domain or Sales Navigator, contact a prospect, or accept any PO data.

**Friday 11-06 check:** HR has acknowledged the request in writing · 6 of 6 DD5 letters and 2 of 2 data-terms emails sent · spend ≤$500.

---

## 3. The locked threshold sheet (the document emailed on Monday)

### 3.1 DD2 pass/fail thresholds (LI §10, copied verbatim)

| Test | Pass | Fail → action |
|---|---|---|
| **K0: employer carve-out** | Written carve-out signed, covering product, industry and third-party PO contributions | **Kill DD2 for this founder**; build nothing |
| K1: SaaS willingness to pay | ≥5 of 25 pay a deposit or sign a paid LOI at ≥$200/mo | **Kill DD2** |
| K2: substitution | <60% say SiliconExpert, Octopart or their EMS already covers it, **and (K2b) ≥10 of 25 name a specific memory EOL, LTB deadline or die-revision PCN they missed in 2025–26** | Lifecycle becomes a free funnel only |
| K3: index adoption | ≥2 of 10 **signed LOIs naming a live contract or surcharge schedule**, each stating why TrendForce prints and open-book pass-through don't serve it | **Close the index option** |
| K4: data moat | **≥10 signed contribution agreements**. Each: signed by the legal function, line-item POs, ≥$250k/yr memory spend, not EMS-turnkey, no confidentiality conflict. **And** the cell map puts ≥70% of memory spend in ≤4 grade-homogeneous cells, ≥3 of which can reach 5 contributors | **Close the index option** (no panel, no moat) |
| K5: data rights | Nexar or DigiKey permits in-app price/stock display in writing, **with a quote of ≤$1,000/month** | Run the price line on public market prints only and re-run K1 on a demo without distributor prices; if K1 then fails, **kill DD2** |
| **K6: funnel volume** | 25 qualified calls booked within 21 days from cold outreach outside the employer's network | **Kill DD2**: the part-time funnel volume is not reachable |

Optional, J-INT only: "at least 3 of the 5 must be cash." It binds only if it was written into Monday's email.

### 3.2 DD2 dated kill criteria (LI §11, verbatim; the items inside or just after the 90 days)

1. "Before any code (target 2026-11-09): K0 fails (no written employer carve-out) → **kill DD2 for this founder**." DEC adds: "by 2026-11-09 (else stop)".
2. "By 2026-12-01: K1 fails (<5 of 25 deposits or paid LOIs at ≥$200/mo), or K6 fails (<25 qualified calls booked in 21 days) → **kill DD2 entirely**. Spend no more money."
3. "By 2026-12-01: K3 fails (<2 signed LOIs naming a live contract or surcharge schedule), or K4 fails (<10 legal-signed contribution agreements, or the cell map fails) → close the index option for good. The bundle continues as SaaS only, which is the revised BASE."
4. "By 2026-12-15: neither Nexar nor DigiKey grants in-app price display in writing at ≤$1,000/month → run the price line on public prints only and re-test K1 on that demo; if K1 then fails, kill DD2. The revised model's K5-fail case is $69,289 ARR at m36 with a $947 cash low." [On this plan: $3,997 cash low at m22, LI.py §10 "PLAN, K5 fail".]
5. "By 2026-12-01: 0 of 3 suppliers will discuss a pooled allocation agreement → C-72 is closed permanently." (DEC has since killed C-72 as a standalone concept. The three calls ride along at $0.)
6. "By 2027-02-28 (m3): two design-partner BOM tests. If <70% of memory spend falls in ≤4 grade-homogeneous cells → close the index option. If no BOM has an EOL NVM part with a pin-compatible F-RAM/MRAM alternate within 3× the price → drop the C-29 feature."
7. "By 2027-08-31 (m9): fewer than 2 paying accounts (model: 2.7) → stop. The persona doesn't pay."
8. "By 2027-11-30 (m12): fewer than 5 paying accounts, or MRR below $1,700 → stop and put the code in maintenance." (This is LI §11 item #9. Missing *either* figure stops the business.)
9. "Any month before breakeven: cash below $5,000 → stop, and put in no more than the $40k." (LI §11 item #10.)

Later items: LI §11 #8 (index test at m9), #11 (index option closes 2028-02-29), #12 (fewer than 13 accounts at m18 means exit talks) and #13 (ARR below $78,000 at m24 means sell or wind down).

### 3.3 DD5 pass/fail (OM §10, verbatim) and its kill criteria (OM §11)

PASS (continue as a side line) only if **all four** hold:

- **(i) Paid demand:** "at least 3 paid $500 deposits against orders of $2k or more each, **or** at least $15k in signed LOIs. Both count only from distinct funded teams, and at least 100 of the 120 contacts must be distinct funded teams."
- **(ii) Serious buyers:** "**at least 2** commercial or SBIR buyers commit at $10k or more each. Each must confirm in writing that they will stay on the open PDK for production, and must accept the restated licence: nominal-lot measured, corners simulated, refund-capped warranty, no radiation data."
- **(iii) Buildable, on evidence:** "the contractor-signed extracted-SPICE and Monte Carlo pass in step 1, with the reviewer's estimate that the full ≥16 KB sky130 line takes 200 h or less." Step 1 is defined as "at SS / 1.62 V / 125 °C and FF / 1.98 V / −40 °C; with a bitcell Monte Carlo of 1,000 points or more on the sky130 SRAM special-device models."
- **(iv) No free release coming, in writing:** "written statements from **both** UCSC VLSIDA and OCD that they do not plan silicon-characterized ≥16 KB open macros within 18 months, **or** a signed exclusivity/non-compete with whichever of them did not give one. **No answer = FAIL** … Also, no channel owner may confirm a free release."

"**KILL** if (i), (iii) or (iv) fails. **PIVOT** if only (ii) fails: run an academic-only GF180 side line with no sky130 slot and no full-time goal."

**Sequencing set by DEC and J-EV (overrides OM's single 30-day window).** The tests run in order: (iv) at $0 first, then (ii), and only after that the $6.0k contractor review for (iii). (i) runs alongside. The DD5 money is spent only after DD2 dies.

**OM §11 items that matter here:**

- **#2:** "No signed contractor SOW with a 12-month exclusivity / non-compete on free silicon-characterized ≥16 KB sky130 macros, and no technical cofounder with equity → **kill**" (dated 2027-02-28 in OM).
- **#3:** "No paying account, or under $4k invoiced … → **kill.** Fewer than 2 university POs or P-card subscriptions closed → the academic subscription becomes a free tier" (dated 2027-05-31 in OM).
- **#7:** "Any date. UCSC, OCD, ChipFoundry, Cadence or Chips4Makers releases free silicon-characterized ≥16 KB **sky130** macros → **stop one-time spend within 30 days**."
- **#9:** "The Synopsys–GF pilot gives members free GF180 memory IP of 8 KB or more → remove its 40 projects from the market, and re-run the model before any GF180 slot spend."

---

## 4. Weeks 1–5: the DD2 kill test, with the DD5 letters riding along

**The test as a whole** (LI §10):

- **Budget:** ~$2,950 with a $5,000 cap.
  - Line items: ~$500 attorney review, ~$100 Sales Navigator, $50 × 25 calls = $1,250, ~$1,000 government-contracts attorney, ~$100 domain and hosting.
  - This plan defers the $1,000 consult (DEC), so planned spend is **$1,950**.
- **Hours:** LI estimates ~55 founder hours. This plan's count is **~60 h through 12-01**, including the DD5 letters.
- **Call hours:** each 30-minute call is counted as 0.67 h including notes [PLAN].
- **K6 clock:** it starts with the first outreach message, which goes out the day K0 is signed and no later than Mon 11-09. The 21-day window therefore closes no later than **Sun 11-29**, and Thanksgiving (Thu 11-26) falls inside it.

### Week 1 · Mon 11-02 → Sun 11-08 · ~12.5 h · spend $500 (to date $500 · $4,500 under the $5k cap · $39,500 of $40k left)

- **Goals:** lock the thresholds; request K0; get every $0 question out (6 DD5 letters, 2 data-terms emails); prepare the outreach without touching anyone.
- **Tasks (hours):**
  - Monday block (2.0)
  - Nexar and DigiKey emails on day 2 (0.5)
  - four DD5 channel letters (1.0)
  - employment-attorney review (1.5)
  - deposit, paid LOI, index LOI and contribution-agreement templates (2.0)
  - 60-name public-source list with at least 10 index prospects (5.0)
  - carve-out follow-up (0.5)
- **Deliverables:** the dated threshold document (emailed); the carve-out request (sent 11-02); the attorney's notes; 8 outbound emails logged with dates; 4 templates; the 60-name sheet, with a source for each name and a "not employer network" check.
- **Checkpoints:** nothing is decided yet. If HR refuses outright this week, K0 fails early; go to the K0-fail box under week 2.

### Week 2 · Mon 11-09 → Sun 11-15 · ~15.3 h · spend $300 (to date $800 · $4,200 under cap · $39,200 left)

- **Goals:** K0 decided on Monday. If it passes, outreach starts and the scan gets built.
- **Tasks (hours), only after K0 is signed:**
  - Buy Sales Navigator (~$100), the domain and hosting (~$100) (0.5).
  - Send 60 personalized cold messages (3.0). **This starts the K6 clock.**
  - Build scan v0 (10.0): paste a BOM, classify the memory MPNs (DDR3/4/5, LPDDR, eMMC, NOR, EEPROM), and pull lifecycle and stock from the DigiKey API. Its 1,000 requests/day are enough (LI §10 step 1).
  - First 2 calls, discovery on the prototype (1.3).
  - Book the 3 C-72 supplier calls (0.25).
  - Chase Nexar and DigiKey if they have not replied by day 10, 11-11 (0.25).
- **Deliverables:** the signed carve-out, filed; the outreach log (the first send date is the K6 start); scan v0 running.
- **Checkpoint, Mon 11-09, K0:** pass = "Written carve-out signed, covering product, industry and third-party PO contributions". Fail → "**Kill DD2 for this founder**; build nothing" (LI §10; LI §11 #1; DEC "else stop").

> **K0-fail box (if K0 is not signed by end of Mon 11-09).** DD2 is dead and ≤$500 has been spent. Buy nothing else and contact none of the 60 names, but keep the list. The DD5 letters stay out. Spend $0 and ~1 h/week until 12-01, then apply the DD5 check in §5. Clean letters lead to Branch B, which also needs its own written DD5 carve-out (J-CEIL). Anything else leads to Branch C. DEC releases DD5 money only after 2026-12-01, so a K0 failure does not start DD5 any earlier.

### Week 3 · Mon 11-16 → Sun 11-22 · ~13.5 h · spend $400 (to date $1,200 · $3,800 under cap · $38,800 left)

- **Goals:** finish the scan and run the first 8 calls with it live; make the C-72 supplier calls.
- **Tasks (hours):**
  - Finish the scan (6.0): PDN and die-revision PCN lookup, 6-month LTB deadlines from any discontinuance notice, and the brand-level §5949 flag with its label (LI §10 step 1).
  - 8 calls (5.3). On each call, run the scan live, then make the **three asks** (LI §10 step 2):
    1. a $500 refundable deposit or a paid LOI;
    2. for index prospects, a signed LOI that names a live contract or surcharge schedule;
    3. a 24-month line-item PO contribution agreement signed by the company's legal function.
  - On each call, also ask the four questions in LI §10 step 2: what they use today; which EOL, LTB or PCN they missed in 2025–26 (K2b); whether their 2026 LTBs filled at ≥90%; and their cell mix.
  - 3 C-72 supplier calls (1.5): a Winbond or Nanya U.S. sales office and a franchised Micron distributor. The question: "Would you quote a pooled allocation agreement to a co-op that holds no title or credit?"
  - Second touch to non-responders (0.5).
  - DD5 reminder on Mon 11-16 (0.25).
- **Deliverables:** scan v1, live for demos; the call log, with K1–K4 tallies updated after each call; the C-72 answers.
- **Checkpoints:**
  - C-72: the LI §11 #5 rule above. Information only, because DEC has already killed C-72 standalone.
  - **Pace marker (not a threshold) [PLAN]:** about 17 calls booked by Sun 11-22 keeps K6 on a straight-line pace. Fewer than ~12 means K6 will probably fail.

### Week 4 · Mon 11-23 → Sun 11-29 (Thanksgiving Thu 11-26) · ~12.7 h · spend $500 (to date $1,700 · $3,300 under cap · $38,300 left)

- **Goals:** write the index one-pager; hold the largest block of calls; close the K6 window.
- **Tasks (hours):**
  - "Memory Surcharge Reference v0" (4.0): a draft methodology for ≤4 grade-homogeneous quarterly cells plus a sample two-sided surcharge clause (LI §10 step 1). The 10 index-prospect calls are scheduled after it exists.
  - 10 calls on Mon–Wed and Fri (6.7).
  - Follow-ups on deposits, LOIs and contribution agreements (2.0). Agreements need the prospect's legal function, so start them early.
- **Deliverables:** Surcharge Reference v0 (PDF); the K6 count, frozen at the end of Sun 11-29.
- **Checkpoint, Sun 11-29, K6:** pass = "25 qualified calls booked within 21 days from cold outreach outside the employer's network". Fail → "**Kill DD2**: the part-time funnel volume is not reachable". It is formally recorded on 12-01 under LI §11 #2. If K6 fails, pay the $50 thank-yous already promised and spend nothing else.

### Week 5 · Mon 11-30 → Sun 12-06 · ~5.8 h to the decision, plus the branch kick-off · spend $250 (to date **$1,950** · $3,050 under cap, $2,050 if the deferred $1,000 consult is later spent · **$38,050 left**)

- **Goals:** hold the last calls, tally on Tuesday evening, decide.
- **Tasks (hours):**
  - Last 5 calls on Mon 11-30 and Tue 12-01 morning (3.3).
  - **Tally on Tue 12-01** (2.0): score each leg against §3.1. Count only commitments received in writing by end of day 12-01, and only from the 25 qualified calls.
  - Decision note to the advisor (0.5).
  - From Wed 12-02: start the branch (§6–§8).
- **Deliverables:** a one-page result sheet giving K0–K6 pass or fail with counts, the DD5 letter status, and which branch follows.
- **Checkpoints, Tue 2026-12-01** (thresholds verbatim in §3.1 and §3.2):
  - K1: ≥5 of 25 deposits or paid LOIs at ≥$200/mo. A fail kills DD2.
  - K6, final. A fail kills DD2.
  - K2 and K2b decide whether lifecycle alerts are paid or a free funnel.
  - K3 and K4 decide whether the index option stays open.
  - C-72.
  - DD5 (iv): no written answer from both UCSC VLSIDA and OCD by 12-01 = FAIL (DEC "silence = fail"). The reply was requested by 11-20 [PLAN], inside OM §10's days 7–20.
  - K5 is still open until 12-15.

---

## 5. The 2026-12-01 decision

```
2026-11-09  K0 signed? ──── no ───► DD2 dead (≤$500 spent) ─────────────────────┐
     │ yes                                                                       │
2026-11-29  K6: 25 qualified calls booked in 21 days? ── no ──► DD2 dead ────────┤
     │ yes                                                                       │
2026-12-01  K1: ≥5 of 25 deposits / paid LOIs at ≥$200/mo? ── no ──► DD2 dead ───┤
     │ yes                                                                       ▼
     ▼                                              DD5 check on 2026-12-01: written no-release
 BRANCH A — DD2 continues                           statements from BOTH UCSC VLSIDA and OCD (or a
   K3 AND K4 pass → A2 (index option open,          signed exclusivity), and no channel owner
                    spend the deferred $1k + $5k)   confirms a free release?
   otherwise      → A1 (SaaS only = revised BASE)      yes ─► BRANCH B: DD5 test, Jan 2027, ≤$9.1k
   K5 decided 12-15; K2 decides paid vs free           no  ─► BRANCH C: stop
   lifecycle alerts
```

In Branches B and C, refund every DD2 deposit by Fri 12-04 [PLAN] and thank every caller in writing.

---

## 6. Branch A: DD2 passes K0, K6 and K1 (weeks 6–13)

**The honest frame.**

- Inside the 90 days the job is to turn deposits into design partners and build the MVP. No subscription revenue arrives: the model's first revenue is m6 (2027-05), and its first paying cohort pays 40% less through m10 (LI §4; LI.py §4). The m9 and m12 gates fall in August and November 2027. This branch only sets them up.
- **A1 (index closed)** is the model's "PLAN" row: the $1,950 test charged, no $5k opinion and no $1k consult. Max founder draw $30,850, cash low $9,150 at m16 (LI.py §10). **A2 (index open)** adds the $1,000 consult and the $5,000 opinion ("PLAN + index option passes"): max draw $36,850 and cash low $3,150 at m16, over the $34k cap and under the $5k floor unless results beat BASE.
- **If K2 failed,** lifecycle alerts become a free funnel. The paid line is then the price and allocation alerts, which fall 57% in GLUT and 83% in SEVERE (LI.py §6).
- **Spending caps after a pass:** "≤~$22k cumulative through the m9 gate" (J-INT, J-CEIL); "≤$34k ever, $5k cash floor" (DEC).
- **Monthly opex follows the model:** $650/month in Dec and Jan, made up of tools $250, marketing $300 and accounting $100 (LI.py §4 m1–m2; LI.py inputs).

### Week 6 · Mon 12-07 → Sun 12-13 · ~15 h · spend $650 (A2: $1,650) · to date $2,600 (A2: $3,600) · $37,400 left (A2: $36,400)

- **Goals:** convert the depositors into 5 design partners; freeze the MVP scope.
- **Tasks (hours):**
  - Send each depositor a design-partner agreement (3.0). Terms: 40% off through m10 (LI §4); a weekly 30-minute call; a BOM upload; the $500 deposit credited at the m6 paid launch [PLAN]. In A2 it also carries the written data-contribution agreement, and no data flows before the antitrust opinion.
  - MVP specification and repository (8.0) (LI §8, Q1): BOM upload, memory MPN classifier, PDN **and PCN** crawler, alerts on the DigiKey API.
  - Set up the newsletter (2.0).
  - **A2 only:** the 2-hour, ~$1,000 government-contracts consult on whether DLAD or GSAM price adjustments can reference the index, and on the cell rules (2.0) (LI §10 step 5).
- **Deliverables:** 5 or more agreements sent; the MVP scope document.
- **Checkpoint:** none this week. K5 is due Tuesday of week 7.

### Week 7 · Mon 12-14 → Sun 12-20 · ~15 h · spend $0 · to date $2,600 (A2: $3,600)

- **Goals:** decide K5; build the BOM upload and classifier; publish the first market note.
- **Tasks (hours):** BOM upload and memory MPN classifier, reusing the scan (10.0); first monthly memory note (3.0); K5 decision (0.5); if K5 failed, write the public-prints demo specification (1.5).
- **Deliverables:** classifier v0.1; Memory Note #1; the newsletter launched, with a target of 150 subscribers (LI §4).
- **Checkpoint, Tue 12-15, K5:** pass = "Nexar or DigiKey permits in-app price/stock display in writing, **with a quote of ≤$1,000/month**". Fail → "Run the price line on public market prints only and re-run K1 on a demo without distributor prices; if K1 then fails, **kill DD2**".
- **Honest note.** Even if the K1 re-test passes, the model's K5-fail case on this plan (test charged, opinion deferred) ends with $69,289 ARR at m36 and a **$3,997 cash low at m22** (LI.py §10 "PLAN, K5 fail"; $947 in the BASE model, which books the $5k opinion and no test spend). That is below the $5k floor. Plan to stop at the floor unless actual results beat the model.

### Week 8 · Mon 12-21 → Sun 12-27 (Christmas) · ~8 h · spend $0

- **Tasks (hours):** the PDN and PCN crawler, covering die-revision and fab-transfer notices (8.0).
- **If K5 failed:** show the public-prints demo to every depositor. Re-test K1 by **Fri 2027-01-08** [PLAN]: at least 5 deposits or paid LOIs at ≥$200/mo must still stand.
- **Deliverable:** crawler v0.1.

### Week 9 · Mon 12-28 → Sun 01-03 (New Year) · ~8 h · spend $0

- **Tasks (hours):** alerts on the DigiKey API (6.0); the days-31–60 tally (1.0).
- **Checkpoint, Fri 2027-01-01** (LI §4, output for days 31–60): "5 signed design-partner agreements; ≥3 BOMs uploaded." It is a measured output, not an LI §11 kill line. A miss is an early warning for the m9 gate.

### Week 10 · Mon 01-04 → Sun 01-10 · ~15 h · spend $650 (A2: $5,650) · to date $3,250 (A2: $9,250) · $36,750 left (A2: $30,750)

- **Tasks (hours):** ship MVP v0.1 to the partners (10.0); start weekly partner calls (2.5). **A2 only:** commission the written antitrust opinion on the cell rules, ~$5,000, the model's m2 item (1.0). Partner PO data arrives only after it is signed (LI §6).
- **Checkpoint:** the K1 re-test result on Fri 01-08 if K5 failed. A fail kills DD2 (LI §11 #4). Close down using the Branch C steps.

### Week 11 · Mon 01-11 → Sun 01-17 · ~15 h · spend $0

- **Tasks (hours):** fixes from partner feedback (9.0); partner calls (2.5); start the two m3 BOM tests (3.0). One is the cell map, the PHY-02 test (A2 only). The other is the NVM swap check, the VET-05 test: an EOL NVSRAM or high-write EEPROM part with a pin-compatible F-RAM/MRAM alternate within 3× the price.

### Week 12 · Mon 01-18 → Sun 01-24 · ~15 h · spend $0

- **Tasks (hours):** Memory Note #2 (3.0); ask each partner for one referral and put up the waitlist page for the m6 paid launch (3.0) (LI §4); build work (6.0); partner calls (2.5).

### Week 13 · Mon 01-25 → Sun 01-31 · ~15 h · spend $0 · to date $3,250 (A2: $9,250)

- **Tasks (hours):** build work (10.0); partner calls (2.5); the 90-day review and a note to the advisor (2.0).
- **Checkpoint, Sun 2027-01-31** (LI §4, output for days 61–90): "≥10 waitlist accounts; ≥3 partners sharing 24 months of PO history". The PO-history half applies only in A2, after the antitrust opinion.
- **Gates after the 90 days (LI §8 and §11, copied above):**
  - **2027-02-28 (m3):** "5 partners active weekly; ≥3 sharing PO history; cell map … and NVM swap check", plus LI §11 #6.
  - **2027-05-31 (m6):** "paid launch done; ≥3 of 5 partners still active".
  - **2027-08-31 (m9):** fewer than 2 paying accounts means stop.
  - **2027-11-30 (m12):** fewer than 5 paying accounts, or MRR below $1,700, means stop.
  - **Any month:** cash below $5,000 means stop.

---

## 7. Branch B: DD2 fails, DD5 letters clean (weeks 6–13; decision Wed 2027-02-10)

**The frame.**

- **Window:** DEC releases ≤$9.1k only now. J-INT sets the window at **2027-01-11 → 2027-02-10**, so the test never runs across the academic winter break.
- **Sequence** (J-EV, DEC):
  - **Tranche 1, $1.6k:** compute, page and Stripe, outreach, and the licence/warranty template (OM §10 line items).
  - **Tranche 2, $6.0k:** the 40-hour contractor review. It is spent **only after at least 2 commercial or SBIR buyers have committed at ≥$10k** (test ii).
  - **Tranche 3, ≤$1.5k:** one hub event, only after tranche 2.
- **What a pass buys:** DD5 economics are BASE ARR **$41.2k at m18** and **$65.7k at m36**, a cash low of $4.0k at m15, and the founder never paid. A full free release cuts m36 ARR to $34.0k (OM §14.3).
- **The model starts from $40k with the $9.1k test in m1** (OM.py one-time items). Branch B starts from **$38,050**, so the model's $2.5k cash gate will defer slots further [ESTIMATE].
- **Hard cap $10k** (J-INT).

### Week 5 tail · Wed 12-02 → Sun 12-06 · ~2 h · $0

- Send a separate written **DD5 carve-out request** (1.0) (J-CEIL). It covers an open-PDK SRAM macro service for university, startup and SBIR tapeout teams, built on personal time and equipment. Ask for a signature by **Fri 12-18** [PLAN]. Without it, go to Branch C.
- Thank the letter writers and confirm their statements in writing (1.0).

### Week 6 · Mon 12-07 → Sun 12-13 · ~10 h · $0 · to date $1,950 · $38,050 left

- **Tasks (hours):** build the 120-name list from public repositories, at least 100 of them distinct funded teams (10.0) (OM §10 step 3). It covers:
  - wafer.space Run 1 and Run 2 project owners;
  - Tiny Tapeout SoC builders;
  - U.S. GF-pilot instructors;
  - about 20 SBIR performers on SkyWater, each to be asked whether they need radiation data;
  - the NORDTECH and NEMC managers;
  - MOSIS 2.0.
- **Checkpoint:** the Synopsys–GF answer. If the pilot gives members ≥8 KB of free GF180 memory IP, remove its 40 projects from the market and re-run the model before any GF180 spend (OM §11 #9).

### Week 7 · Mon 12-14 → Sun 12-20 · ~10 h · spend $300 · to date $2,250 · $37,750 left

- **Checkpoint, Fri 12-18:** the DD5 carve-out is signed [PLAN], or go to Branch C.
- **Tasks (hours):**
  - Cloud OpenRAM runs ($0.3k compute) (8.0): DRC/LVS-clean 8, 16 and 32 KB sky130 macros and 2, 4 and 8 KB GF180 macros, with simulated Liberty files.
  - **Measure the real area of the 32 KB sky130 macro** (2.0). It replaces the 30% array-efficiency assumption (OM §10 step 1).

### Week 8 · Mon 12-21 → Sun 12-27 · ~5 h · spend $200 · to date $2,450

- **Tasks:** a landing page with the real prices: $200 or $800 a month; $3k or $10k per tapeout; a $12k licence (OM §4). LEF and datasheet previews are labelled "simulated, not silicon-proven". Stripe takes $500 refundable deposits ($0.2k).

### Week 9 · Mon 12-28 → Sun 01-03 · ~5 h · spend $1,000 · to date $3,450

- **Tasks:** licence and refund-capped warranty template ($1.0k), per OM §10 step 2: nominal-lot measured, corners simulated, yield on ≥50 die, a 12-month warranty limited to re-delivery or a refund of fees, no radiation data.

### Week 10 · Mon 01-04 → Sun 01-10 · ~12 h · spend $100 · to date **$3,550** (end of tranche 1) · $36,450 left

- **Tasks (hours):** outreach sequences and tooling ($0.1k) (6.0); a contractor shortlist and a written quote for 40 h at $150/h from OCD, OpenRAM/UCSC alumni or Chips4Makers (3.0) (OM §9); page go-live checks (3.0).

### Week 11 · Mon 01-11 → Sun 01-17 · ~13 h · spend $0

- **Day 1 is 01-11.** Contact all 120 names, as OM §10 step 3 schedules for days 3–25, i.e. 01-13 → 02-04 (8.0). First calls (5.0).

### Week 12 · Mon 01-18 → Sun 01-24 · ~12 h · spend $0

- **Tasks:** calls and deposits (12.0). Press every commercial or SBIR prospect for a ≥$10k commitment, with written confirmation that it stays on the open PDK for production and accepts the restated licence.

### Week 13 · Mon 01-25 → Sun 01-31 · ~12 h · spend $0 or $6,000 · to date $3,550 or **$9,550**

- **Checkpoint, Fri 2027-01-29 [PLAN], test (ii):** "**at least 2** commercial or SBIR buyers commit at $10k or more each …".
  - **Pass:** commission the contractor the same day ($6.0k). The 40 h buy a signed extracted-SPICE run on the 16 KB sky130 macro at SS/1.62 V/125 °C and FF/1.98 V/−40 °C, plus a ≥1,000-point Monte Carlo.
  - **Fail:** the $6k is not spent. Under DEC's sequence (iii) then cannot be shown, so DD5 cannot pass as specified. OM §10 allows an academic-only GF180 pivot "if only (ii) fails". This plan recommends **Branch C** instead, because GF180MCU wafers are fabbed in Singapore and the deep dive expects free GF180 macros (P = 0.6 by m24; OM §1, §5; OM.py R13).
- **Then, 02-01 → 02-10 (beyond week 13):**
  - The contractor delivers.
  - One hub or community event, ≤$1.5k (to date ≤$11,050). It converts deposits into LOIs and tests the warranty language with at least 2 buyers (OM §10 step 5).
  - **Decision on Wed 2027-02-10:** pass only if (i)–(iv) all hold; KILL if (i), (iii) or (iv) fails.
  - After a pass, the next gate is OM §11 #2 (an exclusive contractor SOW or a technical cofounder). OM dates it 2027-02-28, which assumed a November test. Re-date it on 02-10, before any further spend.

---

## 8. Branch C: both fail, so stop

**Close-out, Wed 12-02 → Fri 12-04, ~3 h, $0** [PLAN]:

- Refund every deposit.
- Send thank-you and decline notes to callers, suppliers and the six DD5 channel contacts.
- Cancel Sales Navigator.
- Write a one-page record of the K-data: the counts, the objections heard and the "what do you use today" answers. It is the study's only primary demand evidence.
- Tell the advisor.

**Keep:** the day job, and **$38,050** of the $40,000 ($39,500 if DD2 stopped at K0). If Branch C comes later, at Branch B's (ii) gate or its 02-10 decision, the remainder is **$36,450** or **≥$28,950**. The C-86 index option closes along with DD2.

**After that, weeks 6–13: ~1 hour a month watching the $0 list below.** Do not solicit any of these; act only if one fires.

| ID | Trigger (DEC, verbatim) | Where to watch ($0) | If it fires |
|---|---|---|---|
| C-64 | "Final FAR rule in FAR Case 2023-008 (§5949) drops reliance on supplier self-certification, or a module maker pays cash because its supplier refuses a die-source declaration" | Federal Register docket for FAR Case 2023-008, checked monthly. The rule was proposed 2026-02-17, the prohibition starts 2027-12-23, and no final rule existed on 2026-11-01 (LS §0 #8) | DD1's $1.4k Stage-1 track C' probe (J-EV, J-INT). The best case is still ~$227k ARR at m36 (J-CEIL) |
| C-48 | "Both needed (04_DEEPDIVES/private-moe-appliance.md §14.4): (a) a VAR/MSP commits in writing to >=6 boxes/yr on its own paper at <=15%/20%; and (b) a published or socket-pinned single-socket run showing >=10 tok/s per user at 4 concurrent users on a 1T-class MoE in a box quoting <=$65k (or the alternative proof listed there)" | Server-platform launches and public hybrid-inference benchmarks, checked quarterly (J-CEIL) | Reopen DD6 only on its §14.4 terms |
| C-72 | "Any of Winbond, Nanya, Micron (Manassas DDR4) or a franchised distributor agrees in writing to honor a pooled multi-year allocation agreement with a no-title buying co-op (one of DD2's three $0 supplier calls)" | Answered on the week-3 supplier calls if K0 passed (LI §10 step 4); otherwise passive only | Reopen C-72 only as a written-agreement case; it was killed standalone under Rule 1 (DEC `embedded_tests`) |
| C-91 | "A written OCM offer of authorized-aftermarket rights (wafers, test programs, marking) for a named EOL DRAM family" | Passive only. P ≤5% within 15 months; do not solicit (J-EV) | It must also come with an all-in pull cost of ≤$1.53/die (J-CEIL) |
| C-12 | "Unsolicited reseller sell-through or commitment showing >=33 MRAM backup cards/month" | Passive. 33/month is the 36-month breakeven (`04_DEEPDIVES/nv-continuity-modules.md` §0) | DD3's $1.2k, 28-day demand-only probe (J-EV) |
| C-65 | "A hi-rel cofounder arrives with an existing x72 design-in and >=3 evaluation LOIs at >=$1,200/unit" | Passive | Reopen only as a cofounder-led T2 raise of $5.5–11.5M (J-CEIL). Not a T0 path |

**The re-aim, if this branch ends it.** J-CEIL suggests moving the venture search outside memory, to operations and supply-chain software for hardware makers. There the founder's build speed is the edge, and the same employer carve-out applies. This study did **not** model that space.

---

## 9. Cash and time budget for all three branches

All dollar figures are cumulative from 2026-11-02 and come from the week tables above. The starting point is $40,000 deployable (LI.py `founder_cash`).

| Branch | Decided | Spent by 2027-01-31 | Spent by the branch's own decision | Left of $40k | Founder hours, weeks 1–13 | What the model says comes next | Next hard gate |
|---|---|---|---|---|---|---|---|
| Weeks 1–5 (shared) | Tue 2026-12-01 | $1,950 (+$1,000 held) | n/a | $38,050 | ~60 by 12-01 | n/a | 12-01 |
| K0 fails | Mon 2026-11-09 | $500 | n/a | $39,500 | ~13, then B or C | n/a | DD5 check 12-01 |
| **A1**: DD2 passes; K3 or K4 fails (SaaS only) | 12-01 | **$3,250** | n/a | **$36,750** | ~171 (60 + ~111) | LI.py §10 "PLAN": cash low **$9,150** at m16 (BASE $6,100 + the deferred $5k opinion − the $1,950 test); max draw **$30,850**, inside the $34k cap. Draw ≤~$22k through m9 (J-INT) | 2027-02-28 (m3); 2027-08-31 (m9) |
| **A2**: DD2 passes; K3 + K4 pass (index open) | 12-01 | **$9,250** | n/a | **$30,750** | ~171 | LI.py §10 "PLAN + index option passes": cash low **$3,150** at m16, **below the $5k floor**; max draw **$36,850**, over DEC's ≤$34k cap, unless results beat BASE | Same, plus the index VET-01 test at m9 |
| A with K5 failed | 12-15 → re-test 01-08 | as A1 or A2 | n/a | as A1 or A2 | as A | LI.py §10 "PLAN, K5 fail": $69,289 ARR at m36, **$3,997 cash low at m22**. The floor is breached | K1 re-test 2027-01-08 [PLAN] |
| **B**: DD2 dead, DD5 letters clean | Wed 2027-02-10 | $3,550 (tranche 1), or **$9,550** if (ii) passes and the contractor is commissioned 01-29 | **≤$11,050** (DD5 ≤$9,100) | ≥$28,950 | ~141 (60 + ~81), plus ~20 h to 02-10 | OM BASE: ARR $41.2k at m18, cash low $4.0k at m15 from $40k. Branch B starts it at $38,050 [ESTIMATE: further slot deferral] | 02-10, then the OM §11 #2 contractor SOW (re-dated) |
| B, with DD2 dead at K0 | 02-10 | $500 + DD5 | ≤$9,600 | ≥$30,400 | ~100 | as B | as B |
| B stops at (ii) | Fri 2027-01-29 | $3,550 | n/a | $36,450 | ~141 | none | none |
| **C**: stop | 12-01 | **$1,950** | n/a | **$38,050** | ~63, then ~1 h/month | $0 | Watch list only |

**How to read it.**

- **The worst case inside the 90 days is A2 at $9,250.** The largest committed path overall is Branch B at ≤$11,050 by 2027-02-10.
- **Every branch stays far inside $40k for these 13 weeks.** The real cash risk starts later, at DD2's m8–m16 trough (BASE model: cash $20,171 at m8 down to $6,100 at m16, LI.py §4; on this plan the low is $9,150 at m16, LI.py §10).
- **Branch C is the most probable outcome.** It costs about 4.9% of the capital ($1,950 of $40,000) and about 63 hours.

---

## 10. Inconsistencies found in the inputs (flagged here, not fixed)

*Phase 7 gate status (g-mission-critic, 2026-11-01): items 1, 2 and 4 are now resolved upstream. (1) `models/lifecycle-intel.py` §10 now has PLAN rows that charge the $1,950 test at m1: max draw $30,850 and cash low $9,150 at m16 in BASE. With the index option, the $2,950 case gives $36,850 and $3,150, and `decision.json` `PRIMARY.plan_cash` states that the cap and floor still bind. (2) `decision.json` `watch_list` C-48 now reads "4 concurrent users". (4) `decision.json` keeps C-72 killed standalone but lists a supplier "yes" as its reopen trigger, which matches LI §10. The other items are left as flagged.*

1. **DD2's model leaves out its own kill-test spend.** *(Resolved; see the note above. §1, §6 and §9 now quote the PLAN rows.)* The original finding:
   - `models/lifecycle-intel.py` starts m1 (2026-12) at $40,000, after the November test. OM.py, by contrast, books DD5's $9.1k test in its m1.
   - So DD2's "$33,900 max draw" plus the ~$2,950 test comes to ~$36,850, which breaks DEC's "≤$34k ever".
   - The BASE cash low becomes ~$3,150, below the $5k floor, once the $5k antitrust opinion is spent (A2).
   - The K5-fail case has a $947 cash low before any test spend.
2. **DEC's C-48 trigger was wrong.** *(Resolved; see the note above. §8 quotes the corrected trigger.)* DEC said "≥10 tok/s per user at **2** concurrent users on the L box". DD6 §14.4's reopen trigger (`04_DEEPDIVES/private-moe-appliance.md`) says **4** concurrent users on a 1T-class MoE in a ≤$65k box, or a blind evaluation. The "2 concurrent" wording belongs to DD6's K5 U.S.-origin test.
3. **LI points to dead deep dives.** LI §0 and §14.5 say to run the DD2 test "alongside DD1/DD3 customer discovery". Both are killed, and DEC runs DD2 alone.
4. **C-72's status conflicts.** LI §10 step 4 says a supplier "yes" reopens C-72. DEC says C-72 was killed standalone under Rule 1 at Phase 7.
5. **Two judges misstate the m12 gate.** J-EV and J-INT give it as "≥5 accounts **or** MRR ≥$1,700". LI §11 #9 stops the business if *either* figure is missed. J-CEIL states it correctly.
6. **The deadline for DD5 test (iv) differs between files.** J-INT says silence by day 14 fails. J-EV and J-CEIL request an answer by 2026-12-01. OM §10 schedules the questions for days 7–20. This plan requests 11-20 and uses 12-01 as the cut-off.
7. **OM §11's dates assume a November DD5 test.** They are m3 2027-02-28, m6 05-31 and m12 11-30. DEC's sequencing puts the DD5 decision about 71 days later, on 2027-02-10. The OM model also assumes a $40k start, against ~$38k in Branch B.
8. **The size of DD5's first tranche differs.** J-EV caps it at "$1.5k". OM §10's own line items for that tranche (compute $0.3k, web $0.2k, outreach $0.1k, template $1.0k) add up to $1.6k.
9. **The m2 antitrust opinion conflicts.** LI §4, LI §8 and the model's BASE book the $5k opinion unconditionally at m2. DEC defers it until K3 and K4 pass. *Resolved for this plan:* the model's PLAN rows (LI.py §10) defer it; BASE is left unchanged for comparability.
10. **The brief's "first paying accounts" in weeks 6–13 does not fit the model.** The model's first revenue is m6 (2027-05), and the m9 and m12 gates fall in August and November 2027, outside these 90 days.
