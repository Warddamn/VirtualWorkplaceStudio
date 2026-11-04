# Outreach: getting the Oxide Tail Spec run

*The front door to the outreach folder of the [dram-moonshot](../README.md) study. As of 2026-11-04. Written for you: a software builder on the US East Coast, not a chip engineer.*

**Why this folder exists.** The study's biggest unknown is the worst-case behaviour of small oxide transistors. It comes down to two numbers: the 1e-4 to 2e-5 quantile of attoamp off-state leakage (1 aA = 1e-18 A), and the 1e-4 quantile of random telegraph noise (RTN), after a ≤400 °C hydrogen, heat and bonding budget ([report §1](../DRAM_MOONSHOT_REPORT.md#1-the-answer-in-one-page)) [ESTIMATE, study judgment]. A home bench cannot measure it ([home lab](../home-lab/README.md)). A university nanofab or faculty group can. This folder is how you ask them. It also holds the ask to a DRAM test partner for the FASTEST PROOF.

**Evidence tags.**
- [DATASHEET]: a maker's or facility's published spec.
- [REPORTED]: a paper, press item or official page, with its URL in [Sources](#sources). Here these come from [LAB_TARGETS.md](LAB_TARGETS.md), which read them as search snippets. They were not re-fetched in this pass.
- [ESTIMATE]: arithmetic or judgment. It is either done here or taken from the study's own models and plans, with the file named. None of it is a measurement.
- [UNVERIFIED]: not confirmed by any source found.
- Statements about what this repo's own files say were checked directly in this pass. They are cited by link and carry no tag.

**Acronyms.**
- DRAM: dynamic random-access memory. ECC: error-correcting code. RAW-BER: the study's FASTEST PROOF, which relaxes DRAM refresh and lets ECC absorb the weak bits (BER = bit error rate).
- IGZO: indium gallium zinc oxide. TFT: thin-film transistor. 2T0C: a gain cell with two transistors and no capacitor.
- NDA: non-disclosure agreement. IP: intellectual property. PI: principal investigator, the faculty member who leads a lab. F&A: facilities and administrative overhead. IMS / IEN: Georgia Tech's Institute for Matter and Systems / Institute for Electronics and Nanotechnology.

---

## What's here

| File | What it is | What you do with it |
|---|---|---|
| [OXIDE_TAIL_SPEC_onepage.md](OXIDE_TAIL_SPEC_onepage.md) | Page 1 of the spec. It has 9 rows of test structures, each with splits, conditions and every concept's pass/kill line, plus three asks | Export it to a one-page landscape PDF and attach it |
| [OXIDE_TAIL_SPEC.md](OXIDE_TAIL_SPEC.md) | Page 1 plus pages 2-4: why one measurement decides seven concepts, methods, statistics, data formats, budget and schedule, and GO / KILL / REVIVE per concept | Read it yourself. Share pages 2-4 only under an NDA |
| [LAB_TARGETS.md](LAB_TARGETS.md) | 16 facilities, 8 verified faculty groups plus leads, and 8 DRAM test partners and vendors. Also rates, onboarding steps, an ask list and a ranked shortlist | Pick who to email |
| [EMAIL_DRAFTS.md](EMAIL_DRAFTS.md) | Five drafts of 200 words or fewer, what to attach, and what not to promise | Send |
| README.md (this file) | Order of use, a reply tracker, and how the home lab fits in | Track |

---

## Order of use

**Step 0. Make three decisions (15 minutes)** [ESTIMATE]. They are in [EMAIL_DRAFTS, "Before you send"](EMAIL_DRAFTS.md#before-you-send-three-decisions):
- **Disclosure route.** File the provisionals first, send under an NDA, or send page 1 as written.
- **Entity.** Name your company, or say "incorporating".
- **Money words.** Ask for a "budgetary quote" and promise no purchase order.

**Step 1. Read the spec (about an hour)** [ESTIMATE].
- Read page 1 first. Then read pages 2-4, [§2](OXIDE_TAIL_SPEC.md#2-why-one-measurement-decides-seven-concepts) (why it matters) and [§8](OXIDE_TAIL_SPEC.md#8-decision-rule-per-concept-go--kill--revive) (the decision rule).
- Know its three asks by heart:
  1. Can you build and measure these structures on one shared lot from January 2027, and at what cost?
  2. Do you hold per-device leakage or RTN distributions on ≥1e4 devices that you could share under an NDA?
  3. Can you host the bond split, or name a partner who can?

**Step 2. Pick targets.** Use [LAB_TARGETS Part 4](LAB_TARGETS.md#part-4--ranked-shortlist) for week 1:
- **Facilities:** Purdue Birck first, Georgia Tech second.
- **Faculty groups:** Peide Ye, Suman Datta, Muhammad Ashraful Alam, Shimeng Yu.
- **DRAM partner:** Minesh Patel (Rutgers).
- **Hold back:** RIT and Cornell. They are the East Coast second sources until your device co-founder can write a process traveler (a step-by-step recipe). Next in line for groups: Becky Peterson, Karl Hirschman, Moinuddin Qureshi, Xun (Steve) Jian.

**Step 3. Send.**
- Send everything in the same week ([LAB_TARGETS §0](LAB_TARGETS.md#0-the-answer-in-one-screen)).
- Send emails 1 and 2 on the day you open the Purdue and Georgia Tech external-user files (LAB_TARGETS Part 4, order of operations).
- Send email 3 four times, using the fill-in table. Send email 4 to Patel.
- Log each email in the tracker below as soon as it goes out.

**Step 4. Track replies.**
- Follow up with [email 5a](EMAIL_DRAFTS.md#5a-two-line-follow-up) after 5 business days, and again 7 days later. After three tries with no reply, move to the next name [ESTIMATE].
- On calls, use the [90-second pitch](EMAIL_DRAFTS.md#5b-90-second-phone-or-video-pitch).
- Put every quote into the comparison table on the same basis.

**Step 5. Compare quotes and decide.**
- **Normalise each quote:** staff hours × rate, entry or cleanroom fees, tool hours, materials and overhead. Purdue's external rates include 57% F&A [REPORTED]. Georgia Tech's industry rates exclude indirect costs [REPORTED].
- **Compare with the study's own lines** [ESTIMATE, [decision.json](../research/stage3/decision.json) judge budgets]:
  - shared lot: $210k (operator, one lot), $220k (physicist, two lots), or $140k fab plus $35k D₂O bond (investor);
  - HOT-SIDE Gate A+: ~$240k standalone ([hot-side-memory §5](../dossiers/hot-side-memory.md#5-the-decisive-experiment-revised-after-red-team));
  - RAW-BER Phase 1: ~$124k standalone ([raw-ber-contract §5.R](../dossiers/raw-ber-contract.md#5r-revised-decisive-experiment-revised-after-red-team)), or $90-120k in the judges' budgets.
- **If a group shares ≥1e4-device tail data,** check it against the spec's GO / KILL lines before you spend anything. Existing data could re-rank the portfolio ([judge_physicist.json](../research/stage3/judge_physicist.json), monday_action) [ESTIMATE, study judgment].
- **Target date:** the plan has the Birck and Georgia Tech agreements signed in weeks 9-10, which is month 0, January 2027 ([report §9](../DRAM_MOONSHOT_REPORT.md#9-first-90-days-for-the-best-bet)) [ESTIMATE, study plan].

---

## Reply tracker (template)

Copy this table into a spreadsheet, or edit it here. Use one row per contact. Rows 1-7 are the week-1 list. Rows 8-9 are held back.

**Status codes:** Not sent, Sent, FU1, FU2 (follow-ups), Replied, Call booked, Quote in, NDA in review, Declined, Referred.

| # | Contact | Track | Send via | Draft | Sent | Next follow-up | Reply (date, who) | Can run it? (Y / N / part) | Route (staff / group / referral) | Lead time | Quote (US$; what it covers) | ≥1e4-device data? | NDA / IP terms | Next step | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Purdue Birck external-user office | Oxide lot | [become-a-user](https://birck.research.purdue.edu/equipment/become-a-user/) | 1 | | | | | | | | | | | Not sent |
| 2 | Georgia Tech cleanroom (IMS; older pages say IEN) | Oxide lot | [become-user](https://matter-systems.research.gatech.edu/cleanroom/getting-started/become-user) | 2 | | | | | | | | | | | Not sent |
| 3 | Peide Ye, Purdue ECE | Oxide PI | [group papers](https://engineering.purdue.edu/~yep/Papers/EDL_2024_In2O3%20600C_Lin.pdf) | 3b | | | | | | | | | | | Not sent |
| 4 | Suman Datta, Georgia Tech ECE | Oxide PI | [directory](https://www.ece.gatech.edu/faculty-staff-directory/suman-datta) | 3a | | | | | | | | | | | Not sent |
| 5 | Muhammad Ashraful Alam, Purdue ECE | Oxide PI | [CRISP profile](https://engineering.purdue.edu/CRISP/people/affiliate-faculty-expertise/ashraf-alam) | 3a | | | | | | | | | | | Not sent |
| 6 | Shimeng Yu, Georgia Tech ECE | Oxide PI | [group page](https://shimeng.ece.gatech.edu/?p=916) | 3a | | | | | | | | | | | Not sent |
| 7 | Minesh Patel, Rutgers CS | RAW-BER | [Rutgers profile](https://www.researchwithrutgers.com/en/persons/minesh-patel/) | 4 | | | | | | | | | | | Not sent |
| 8 | RIT Semiconductor Nanofabrication Lab (hold) | Oxide lot, East Coast second source | [external customers](https://www.rit.edu/nanofab/external-customers) | 2, adapted | | | | | | | | | | | Not sent |
| 9 | Cornell CNF (hold) | Oxide lot, East Coast second source | [rates overview](https://cnf.cornell.edu/node/642) | 2, adapted | | | | | | | | | | | Not sent |

**Quote comparison (template).** One row per quote.

| Source | Lots | Splits | Cells per split | Staff hours × rate | Entry, cleanroom and tool fees | Materials | Overhead included? | Total (US$) | Lead time to first data | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | |

**Published rates to sanity-check quotes against** (from [LAB_TARGETS §1.1](LAB_TARGETS.md#11-network-access-mode-and-published-rates); confirm before you budget):

| Facility | Rate basis | 100 staff hours | Tag |
|---|---|---|---|
| RIT, dedicated staff, FY24 | $95/h | $9,500 | [REPORTED] rate; [ESTIMATE] total |
| Georgia Tech, industry, effective 2025-09-01 | $100/h staff, plus $850/month entry and $39/h cleanroom | $10,000 | [REPORTED] rate; [ESTIMATE] total |
| Purdue Birck, external non-profit and small business | $144/h (iLab undated; a 2023-06-01 memo marked pending approval) | $14,400 | [REPORTED] rate; [ESTIMATE] total |
| Purdue Birck, external for-profit | $166/h (same sources) | $16,600 | [REPORTED] rate; [ESTIMATE] total |

---

## How this connects to the home lab

The [home lab](../home-lab/README.md) cannot measure the oxide tail. It builds the method, the analysis code and the data package for the spec (home-lab README, "The short answer"). In outreach that gives you two things to attach: code now, and rehearsal data later.

| Home-lab item | What it shows a lab | Attach to | Status on 2026-11-04 |
|---|---|---|---|
| [leakage_tail.py](../home-lab/code/T2_analysis/leakage_tail.py) | Turns floating-node droop logs into leakage currents. It handles blanks, distribution-free and bootstrap intervals, a lognormal check and per-device activation energy ([spec §7](OXIDE_TAIL_SPEC.md#7-what-you-bring)) | Emails 1-3 (optional zip) | Self-tested on synthetic data only |
| [retention_map.py](../home-lab/code/T3_dram/retention_map.py) | Turns write-wait-read logs into retention CDFs, tail quantiles from 1e-7 to 1e-2, Arrhenius fits, VRT (variable retention time) statistics and an ECC-safe refresh interval | Emails 3-4 | Self-tested on synthetic data only |
| [check_home_lab.py](../home-lab/tools/check_home_lab.py) | Runs every self-test and link check. Run it before you attach the code | Not attached | PASS, 10/10 checks, with `--quick` (run in this pass) |
| [E6](../home-lab/E6_retention_tail_real_dram.md): retention map of a real 64 Mbit DRAM chip on a ~$30-63 board | The FASTEST PROOF mechanism on real silicon: your tail spread, VRT, clustering and ECC relaxation factor | Email 4, and calls with DRAM partners | Not measured yet. Its firmware has never run on hardware |
| [E4](../home-lab/E4_femtoamp_leakage_bench.md): off-leakage distribution of 30-120 discrete transistors | That you can run droop, blanks and quantile intervals the way the spec asks ([E4 §12](../home-lab/E4_femtoamp_leakage_bench.md#12-rehearsing-the-oxide-tail-spec)) | Emails 1-3 | Not measured yet |
| [E7](../home-lab/E7_make_your_own_oxide_transistor.md) and [E8](../home-lab/E8_your_own_oxide_gain_cell_memory.md): a home-made zinc-oxide transistor and gain cell | A smaller Birck training request: a few hundred devices. [E8 §13](../home-lab/E8_your_own_oxide_gain_cell_memory.md#13-from-this-demo-to-a-nanofab-your-ticket) has its own short template | A separate Birck request, not the lot | Not measured yet |

**Rules for using home-lab material.**
- **Call it method, not result.** Home floors are ~1-10 fA (1 fA = 1e-15 A). The spec needs attoamps ([home-lab README, "Honest limits"](../home-lab/README.md#honest-limits)).
- **Ask for data in the spec's formats** ([spec §5](OXIDE_TAIL_SPEC.md#5-deliverables-and-data-format)). Format A feeds retention_map.py and Format B feeds leakage_tail.py. Format C, for RTN, is proposed and has no parser yet. If the lab delivers in these formats, your code runs the day the data arrives.
- **Fix one thing before fab data arrives.** leakage_tail.py hard-codes the home bench window (0.45-2.04 V, ≤0.5 V droop), so fab nodes outside it are dropped. Add a window option first (spec §5).
- **The code holds no planned filing.** A search of both scripts found no servo, grade or chip-marking logic. Those are the RAW-BER filing topics; the oxide topics are bond-hydrogen control and cross-temperature multi-level cells ([report §9](../DRAM_MOONSHOT_REPORT.md#9-first-90-days-for-the-best-bet); [raw-ber-contract §11.2](../dossiers/raw-ber-contract.md#112-redesigns-adopted)) [ESTIMATE: a text search, not a legal review].
- **E8's smaller ask, priced.** About $1.1k of day fees plus $2-5k of tool time, at Birck's 2023 for-profit rates, turns 4 home cells into a few hundred devices: the median and the 1-10% tail ([E8 §13](../home-lab/E8_your_own_oxide_gain_cell_memory.md#13-from-this-demo-to-a-nanofab-your-ticket)) [ESTIMATE]. It does not replace the lot.

---

## Limits

- Every fact about a lab, person or rate comes from [LAB_TARGETS.md](LAB_TARGETS.md), which rests on web-search snippets from 2026-11-04. This pass ran no web search and fetched no pages.
- Rates change every fiscal year. Purdue's staff rates trace to a 2023 memo marked pending approval [REPORTED].
- No result in the study is measured. The models are first-order arithmetic with no lab data ([README, "Honest limits"](../README.md#honest-limits)).
- These files are not legal advice. Have a lawyer read any NDA or sponsored-research agreement before you sign [ESTIMATE].

---

## Sources

**Repo files** (links relative to this file): [OXIDE_TAIL_SPEC_onepage.md](OXIDE_TAIL_SPEC_onepage.md); [OXIDE_TAIL_SPEC.md](OXIDE_TAIL_SPEC.md) (§2, §5, §7, §8); [LAB_TARGETS.md](LAB_TARGETS.md) (§0, §1.1, Part 4); [EMAIL_DRAFTS.md](EMAIL_DRAFTS.md); [DRAM_MOONSHOT_REPORT.md](../DRAM_MOONSHOT_REPORT.md) §1, §9; [README.md](../README.md); [decision.json](../research/stage3/decision.json); [judge_physicist.json](../research/stage3/judge_physicist.json); [hot-side-memory](../dossiers/hot-side-memory.md) §5; [raw-ber-contract](../dossiers/raw-ber-contract.md) §5.R, §11.2; home lab [README](../home-lab/README.md), [E4](../home-lab/E4_femtoamp_leakage_bench.md) §12, [E6](../home-lab/E6_retention_tail_real_dram.md), [E8](../home-lab/E8_your_own_oxide_gain_cell_memory.md) §13, [leakage_tail.py](../home-lab/code/T2_analysis/leakage_tail.py), [retention_map.py](../home-lab/code/T3_dram/retention_map.py), [check_home_lab.py](../home-lab/tools/check_home_lab.py).

**External** [REPORTED]. These are from LAB_TARGETS.md's Sources, read as search snippets on 2026-11-04 and not re-fetched here.
- Purdue Birck, become a user: https://birck.research.purdue.edu/equipment/become-a-user/
- Purdue Birck iLab rates: https://purdue.ilab.agilent.com/service_center/show_external/4127/1000
- Purdue Birck FY24 rates vs current (memo): https://mailman.ecn.purdue.edu/archives/list/bnc-all@ecn.purdue.edu/message/QV6GR6XQBKTW7PU5OCDG7VQOPHRKJ2JN/attachment/6/BRKFY24RatesvsCurrent.pdf
- Georgia Tech cleanroom rates (effective 2025-09-01): https://matter-systems.gatech.edu/cleanroom/getting-started/rates
- Georgia Tech, become a user: https://matter-systems.research.gatech.edu/cleanroom/getting-started/become-user
- RIT external customers: https://www.rit.edu/nanofab/external-customers
- Cornell CNF rates overview: https://cnf.cornell.edu/node/642
- Ye group papers (EDL 2024): https://engineering.purdue.edu/~yep/Papers/EDL_2024_In2O3%20600C_Lin.pdf
- Datta, Georgia Tech directory: https://www.ece.gatech.edu/faculty-staff-directory/suman-datta
- Alam, Purdue CRISP profile: https://engineering.purdue.edu/CRISP/people/affiliate-faculty-expertise/ashraf-alam
- Yu group page: https://shimeng.ece.gatech.edu/?p=916
- Patel, Rutgers profile: https://www.researchwithrutgers.com/en/persons/minesh-patel/
