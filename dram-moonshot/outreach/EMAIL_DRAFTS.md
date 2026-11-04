# Email drafts: asking labs to run the Oxide Tail Spec

*Outreach file for the [dram-moonshot](../README.md) study. As of 2026-11-04. Ready-to-edit drafts for you to send in your own name. Start with the folder's front door, [README.md](README.md).*

**How to use this file.**
- Fill every `[bracket]` and delete any line that is not true for you.
- Each draft is 200 words or fewer, counting the subject line and signature. The counts are listed under each draft.
- Send each one through the official contact page named above it. This repo lists no personal email addresses ([LAB_TARGETS.md](LAB_TARGETS.md)).
- Every fact in a draft is listed in the "Fact check" table under it, with its tag and source. The facts about labs come from [LAB_TARGETS.md](LAB_TARGETS.md), which rests on web-search snippets. Confirm rates and names by email before you budget.

**Evidence tags.**
- [DATASHEET]: a maker's or facility's published spec.
- [REPORTED]: a paper, press item or official page, with its URL in [Sources](#sources). Here these are taken from LAB_TARGETS.md and were not re-fetched in this pass.
- [ESTIMATE]: arithmetic or judgment. It is either done in this file or taken from the study's own models and plans, with the file named. None of it is a measurement.
- [UNVERIFIED]: not confirmed by any source found.
- Statements about what this repo's own files say were checked directly in this pass. They are cited by link and carry no tag.

**Acronyms.**
- DRAM: dynamic random-access memory. HBM: high-bandwidth memory. RDIMM: registered memory module. CXL: Compute Express Link, a memory-expansion link.
- IGZO: indium gallium zinc oxide. IGO: indium gallium oxide. ZTO: zinc tin oxide. In₂O₃ (In2O3 in plain-text email): indium oxide. TFT: thin-film transistor. ALD: atomic layer deposition.
- RTN: random telegraph noise, when one trapped charge makes a transistor's threshold jump back and forth.
- ECC: error-correcting code. Chipkill: an ECC that survives a whole dead memory chip. SEC: single-error correction, the ECC built into each DDR5 die. ECS: DDR5's error check and scrub mode, which counts codewords with errors. VRT: variable retention time. JEDEC: the memory standards body. BER: bit error rate.
- NDA: non-disclosure agreement. IP: intellectual property. PI: principal investigator, the faculty member who leads a lab. PO: purchase order. F&A: facilities and administrative overhead.

---

## Before you send: three decisions

1. **The disclosure route.** The study's rule is to file the provisional patents before any disclosure ([report §9](../DRAM_MOONSHOT_REPORT.md#9-first-90-days-for-the-best-bet), "One rule") [ESTIMATE, study plan]. But the plan files them in weeks 9-10, and the Monday action sends the spec on day 1. Pick one route ([OXIDE_TAIL_SPEC.md, "Before you send page 1"](OXIDE_TAIL_SPEC.md#before-you-send-page-1)):
   - file early, then send;
   - send only under an NDA;
   - send page 1 as written. It shows test structures and pass lines only, and it says "chemistry under NDA" for the bond.
2. **Your entity.** Every site will want a legal entity, a PO or other payment method, and insurance certificates if your own people enter the cleanroom ([LAB_TARGETS §1.3](LAB_TARGETS.md#13-onboarding-steps-found)) [ESTIMATE]. If you have not incorporated yet, write "an early-stage startup (incorporating)". Do not name a company that does not exist yet.
3. **Money words.** Ask for a "budgetary quote" or a "rough cost range". Do not promise a PO or a start date unless the money is in the bank.

---

## What to attach

| Email | Attach | Optional | Do not attach yet |
|---|---|---|---|
| 1. Purdue Birck | [OXIDE_TAIL_SPEC_onepage.md](OXIDE_TAIL_SPEC_onepage.md) as a one-page PDF. The file says "Print landscape, one page" | None | Spec pages 2-4; any dossier; the models; [decision.json](../research/stage3/decision.json) |
| 2. Georgia Tech | The same one-page PDF | None | The same |
| 3. Faculty PI | The same one-page PDF | The two analysis scripts as a zip, with the line "self-tested on synthetic data only": [leakage_tail.py](../home-lab/code/T2_analysis/leakage_tail.py) and [retention_map.py](../home-lab/code/T3_dram/retention_map.py) | The same |
| 4. DRAM partner | None. The Phase 1 plan is in the email body | [retention_map.py](../home-lab/code/T3_dram/retention_map.py); your E6 retention map, once you have one ([E6](../home-lab/E6_retention_tail_real_dram.md)) | The [raw-ber-contract dossier](../dossiers/raw-ber-contract.md); its model |
| 5. Follow-up | The same attachment as the first email, if it had one | None | None |

**Why page 1 only.** Pages 2-4 are marked "For you, and for the lab under NDA" ([OXIDE_TAIL_SPEC.md](OXIDE_TAIL_SPEC.md)). They hold the provisional topics, the judges' budgets and the disclosure notes.

**One fix before you export.** Page 1's "Sources" line cites repo files that a lab cannot open, such as `research/stage3/decision.json`. Either leave it, or change it to "internal study files" in your PDF copy only. Keep the repo file unchanged, because page 1 is kept byte-identical to the start of the full spec.

**Home-lab data.** None exists yet. On 2026-11-04 there were no data files in home-lab/ ([OXIDE_TAIL_SPEC.md §7](OXIDE_TAIL_SPEC.md#7-what-you-bring); re-checked in this pass). Attach code now and data later. See [README.md, "How this connects to the home lab"](README.md#how-this-connects-to-the-home-lab).

---

## What not to promise

**IP and confidentiality.**
- Before an NDA is signed, do not offer ownership, a licence, co-inventorship, royalties or exclusivity, in writing or on a call. The safe line: "We would set IP terms in an NDA or a sponsored-research agreement."
- Do not accept a university's IP terms by email. Ask for them in writing, and have a lawyer read them [ESTIMATE].
- Before the provisionals are filed or an NDA is signed, keep these back:
  - **Oxide track:** the carrier architecture, the cross-temperature reference scheme and the bond chemistry ([report §9](../DRAM_MOONSHOT_REPORT.md#9-first-90-days-for-the-best-bet); spec page 1 key) [ESTIMATE, study plan].
  - **RAW-BER track:** the per-module refresh servo, the 1-hour grade test and first-read chip marking. The planned filings are the grade and test method and the servoed refresh ([raw-ber-contract §11.2](../dossiers/raw-ber-contract.md#112-redesigns-adopted), item 9) [ESTIMATE, study plan].
- Offer joint publication only "on terms set in the agreement". Publishing before filing can cost patent rights [UNVERIFIED: general patent practice, not checked here].

**Claims.** Say nothing stronger than dossier section 11, which overrides each dossier's body. Every number below is a model output, not a measurement.

| Pick | Safe to say (from §11) | Do not say |
|---|---|---|
| [HOT-SIDE](../dossiers/hot-side-memory.md#11-red-team-outcome) (BEST BET) | ~10x lower energy per bit moved than HBM in our model (0.37 vs 3.95 pJ/bit delivered; 5.5-15x depending on placement). ~90 W saved per GPU in the 16-tier, 1-bit planning case (48-169 W). "Refresh-light": ~225x fewer refreshes than silicon at 105 °C. A premium near tier at $4.6-12/GB, not cheaper bits [ESTIMATE, HS §11] | "12x", "190 W", "refresh-free", "2 bits per cell" as the plan, "cheaper than DRAM", "it works" (Gate A+ decides that) |
| [RAW-BER](../dossiers/raw-ber-contract.md#113-revised-step-change-claim) (FASTEST PROOF) | ~9x less refresh energy on DDR5 RDIMMs at 85 °C with chipkill kept, in our model (6.1-20x); on retired DDR4 behind CXL, ~11x with two memory channels in lockstep or ~4x on one channel (corrected 2026-11-04, raw-ber §12.1); 2.9x in degraded mode on DDR5 (7x on DDR4 in lockstep, none on one DDR4 channel). Worth ~$3.9 per module over 5 years [ESTIMATE, raw-ber §11.3, §12.1] | "15x", "~13x on DDR4" (it assumed DDR5's 128 check bits per line), "no chipkill needed", the sense-amp flag (that leg was killed), "proven" |
| [AND-STACK](../dossiers/and-stack.md#11-red-team-outcome) (MOONSHOT) | 64 tiers × 2 bits = 5.9x the density of today's leading DRAM node in our model, with no EUV lithography. ~2.3x bits per dollar vs 2026, but only 1.1-1.4x vs a projected 2032 incumbent. The chance the key process closes is ~20% [ESTIMATE, AS §11] | "8.1x", "3.8x bits per dollar", single-film single-etch (killed), "cheap DRAM" |
| The whole study | 10 concepts survived 181 red-team objections, and all 10 were downgraded ([report §1](../DRAM_MOONSHOT_REPORT.md#1-the-answer-in-one-page)) | "validated", "peer-reviewed", "expert-reviewed" |

**Results, data and people.**
- No result in the study is measured. The models are first-order arithmetic with no lab data ([README, "Honest limits"](../README.md#honest-limits)). Write "our model says", never "we measured" or "we showed".
- "Ideas, scores, critiques and verdicts all came from language-model agents" (same source), and that includes the judges. Do not describe the red team or the judges as outside experts.
- Do not describe planned home-lab data as done.
- Do not say a device co-founder is on board until one is. Do not name another lab as a partner before it agrees.
- Do not say Purdue's three-tier In₂O₃ stack was built at Birck. That is [UNVERIFIED] in [LAB_TARGETS.md](LAB_TARGETS.md).
- Do not share the judges' lot budgets ($210-280k) with a facility before it quotes [ESTIMATE: it anchors the price].

---

## 1. Purdue Birck: can staff run the lot?

**Send through:** the Birck external-user page, [birck.research.purdue.edu/equipment/become-a-user](https://birck.research.purdue.edu/equipment/become-a-user/), or the [partner page](https://birck.research.purdue.edu/partner-with-us). The study names Birck as the first facility and plans to submit the external-user application the same morning ([report §9](../DRAM_MOONSHOT_REPORT.md#9-first-90-days-for-the-best-bet)).

```text
Subject: Quote request: staff-run oxide TFT lot (one-page spec attached)

Dear Birck external-user team,

I am [Your name], founder of [Company / "an early-stage startup (incorporating)"], in [City, State]. We are exploring DRAM-class memory built on amorphous-oxide transistors (IGZO, IGO, ZTO, In2O3) processed below 400 °C.

The attached one-page Oxide Tail Spec describes one shared lot (two if needed) starting January 2027. It targets the worst devices, not the median: the 1e-4 quantile of off-state leakage and random telegraph noise, on at least 1e5 cells per split, at 85-125 °C, after hydrogen, anneal and bond splits.

Could you tell me:
1. Can Birck staff run this lot as fee-for-service processing and measurement? If not, which campus group might take it on?
2. Lead time from order to first measured die, and earliest start?
3. A rough cost range at external small-business or for-profit rates?
4. Whether you support 350-400 °C forming-gas anneals, 0.01-0.02 µm² devices and hot-chuck probing to 125 °C?
5. Your IP terms for staff-processed work?

We do not yet have a step-by-step process traveler. Tell me if you need one to quote.

Could we have a 20-minute call?

[Your name]
[Title], [Company] | [Email] | [Phone]
```

**Fact check.**

| Fact in the draft or behind it | Tag | Source |
|---|---|---|
| Most Birck users run the tools themselves, but staff offer processing or measurement services | [REPORTED] | Birck become-a-user page, via LAB_TARGETS §1.1 |
| Engineering staff time: $144/h for external non-profit and small business, $166/h for external for-profit. The same rates appear in a rate memo effective 2023-06-01 that is marked pending approval | [REPORTED] | Birck iLab rates; Birck FY24 memo; LAB_TARGETS §1.1 |
| External rates include 57% F&A | [REPORTED] | LAB_TARGETS §1.1 |
| 100 staff hours cost $14,400-16,600, before tool fees, materials and overhead | [ESTIMATE] | LAB_TARGETS §1.1 |
| Onboarding: make contact, complete two forms, set up accounts, train | [REPORTED] | Birck become-a-user page |
| Lot from January 2027, at least 1e5 cells per split, 85-125 °C, 1e-4 quantile | [ESTIMATE, study plan] | [Spec page 1](OXIDE_TAIL_SPEC_onepage.md); [decision.json](../research/stage3/decision.json) |
| Ask for ≥1.5e5 cells per split if they want the 2e-5 leakage line, since a p-quantile needs N ≳ 3/p | [ESTIMATE] | LAB_TARGETS §1 |
| Fee-for-service work needs a written process traveler, which only a device engineer can write | [ESTIMATE] | LAB_TARGETS §0 |
| Whether Birck has the anneals, fine patterning and 125 °C hot chuck | [UNVERIFIED]: "Ask" in LAB_TARGETS §1.2 | Asked in question 4 |
| Purdue is on Eastern Time | [UNVERIFIED] | LAB_TARGETS, unverified list |

**Word count:** 199 [ESTIMATE, counted by script on 2026-11-04].

---

## 2. Georgia Tech IEN (second source)

**Send through:** the cleanroom's become-a-user page, [matter-systems.research.gatech.edu/cleanroom/getting-started/become-user](https://matter-systems.research.gatech.edu/cleanroom/getting-started/become-user). The study calls the site Georgia Tech IEN (Institute for Electronics and Nanotechnology). Current pages list the cleanroom under IMS, the Institute for Matter and Systems [REPORTED]. How the two relate was not confirmed [UNVERIFIED]. Use whichever name the page shows.

```text
Subject: Quote request: staff-run oxide TFT lot at Georgia Tech (spec attached)

Dear Georgia Tech cleanroom staff,

I am [Your name], founder of [Company / "an early-stage startup (incorporating)"], in [City, State]. We are exploring DRAM-class memory built on amorphous-oxide transistors (IGZO, IGO, ZTO, In2O3) processed below 400 °C.

The attached one-page Oxide Tail Spec describes one shared lot starting January 2027. It targets the worst devices, not the median: the 1e-4 quantile of off-state leakage and random telegraph noise, on at least 1e5 cells per split, at 85-125 °C, after hydrogen, anneal and bond splits.

Could you tell me:
1. Can your staff process and measure this lot as billable work? If not, could a Georgia Tech oxide-device group take it on?
2. Do you deposit oxide channels (ALD or sputter) on site today?
3. Lead time from order to first measured die, and earliest start?
4. A rough cost range at industry rates, including indirect costs?
5. Your IP terms for staff-processed work?

We do not yet have a step-by-step process traveler. Tell me if you need one to quote.

Could we have a 20-minute call?

[Your name]
[Title], [Company] | [Email] | [Phone]
```

**Fact check.**

| Fact in the draft or behind it | Tag | Source |
|---|---|---|
| Georgia Tech IEN is the study's second source after Purdue Birck | [ESTIMATE, study plan] | [decision.json](../research/stage3/decision.json) (facility_first); [report §8](../DRAM_MOONSHOT_REPORT.md#8-the-1m-portfolio-and-gates) |
| Staff time is billable. Academic and government users pay internal rates | [REPORTED] | Georgia Tech rates page, via LAB_TARGETS §1.1 |
| Industry rates effective 2025-09-01: $850/month entry, $39/h cleanroom use, $100/h staff, excluding indirect costs | [REPORTED] | Georgia Tech rates page |
| One month of 100 cleanroom hours, 100 staff hours and the entry fee is $14,750, before indirect costs | [ESTIMATE] | LAB_TARGETS §1.1 |
| NNCI site (SENIC, with JSNN at NC A&T/UNCG). NNCI is the NSF network of open-access university nanofabs | [REPORTED] | LAB_TARGETS §1.1 |
| Onboarding: contact an IMS staff member, join a billing group and an equipment group in SUMS (the booking system), then orientation and entrance tests | [REPORTED] | Georgia Tech become-user page |
| The Datta, Yu and Khan oxide-memory groups are on campus | [REPORTED] | LAB_TARGETS §2.1 |
| Whether oxide devices are fabricated on site | [UNVERIFIED] | Asked in question 2 |

**Word count:** 196 [ESTIMATE, counted by script on 2026-11-04].

---

## 3. A faculty PI: sponsored research or collaboration

**Send through:** the official faculty page in [LAB_TARGETS §2.1](LAB_TARGETS.md#21-groups-that-fit-verified). The study's ask is the same for every group ([report §9](../DRAM_MOONSHOT_REPORT.md#9-first-90-days-for-the-best-bet), Day 1). Do they already hold per-device leakage or RTN data on ≥1e4 devices that they would share under an NDA? And what would a quote be? Any existing tail data could re-rank the portfolio before you spend a dollar ([judge_physicist.json](../research/stage3/judge_physicist.json), monday_action) [ESTIMATE, study judgment].

### 3a. Template

```text
Subject: [Their topic] tail statistics: a sponsored-research question

Dear Professor [Surname],

I am [Your name], founder of [Company / "an early-stage startup (incorporating)"]. We are working on DRAM-class memory built from oxide transistors processed below 400 °C.

Your [paper: first author, topic, venue, year] is among the closest work we found to what we need, because [one line: the channel split, structure or test it matches].

We need the tail, not the median: the 1e-4 to 2e-5 quantile of attoamp off-state leakage, and the 1e-4 quantile of random telegraph noise, on at least 1e5 cells per split at 85-125 °C, after hydrogen, anneal and bond splits. The attached one-page spec lists the structures and pass lines. Our search did not find such a dataset in print.

Two questions:
1. Does your group hold per-device leakage or noise distributions on at least 1e4 devices that you could share under an NDA?
2. Would you consider sponsored research on [their row or split] from January 2027? A rough scope and cost would help us plan.

Could we have a 20-minute call in the next two weeks?

Best regards,
[Your name]
[Title], [Company] | [Email] | [Phone]
```

**Word count:** 194 [ESTIMATE, counted by script on 2026-11-04].

**Fill-ins for the first four groups.** Use only these facts, all from [LAB_TARGETS.md](LAB_TARGETS.md) §2.1 and Part 4.

| PI | "Your [paper]…" line | "because…" line | "[their row or split]" | Tag (paper; row choice) |
|---|---|---|---|---|
| Peide Ye, Purdue ECE | The EDL 2024 paper by Lin et al. on top-gate enhancement-mode ALD In₂O₃ FETs with a 600 °C thermal budget for DRAM applications | It matches the spec's In₂O₃ channel split and its hydrogen and heat budget | An In₂O₃ split of the shared lot | [REPORTED]; [ESTIMATE] |
| Suman Datta, Georgia Tech ECE | The IEDM 2020 paper by H. Ye et al. on double-gate W-doped amorphous indium oxide transistors for capacitorless gain-cell eDRAM (done at Notre Dame) | It measured gain-cell leakage and retention at 25 and 85 °C | The 2T0C gain-cell arrays (spec row 2) | [REPORTED]; [ESTIMATE] |
| Muhammad Ashraful Alam, Purdue ECE | Your group's IEEE EDL 2022 paper on PBTI and hot-carrier degradation in ultrathin ALD In₂O₃ TFTs, which flagged self-heating | The tail question is a reliability and statistics question at 105-125 °C | Drift and 1,000-hour stress statistics (spec rows 2 and 8) | [REPORTED]; [ESTIMATE] |
| Shimeng Yu, Georgia Tech ECE | The Waqar et al. paper in IEEE Transactions on Computers (vol. 75, no. 3, March 2026) on optimizing and benchmarking monolithically stackable gain-cell memory for last-level cache | Our ≥1e5-cell arrays need the right readout design | Design of the ≥1e5-cell test arrays and their readout (spec row 2) | [REPORTED]; [ESTIMATE] |

PBTI is positive bias-temperature instability: a slow threshold drift under voltage and heat. 2T0C is a gain cell with two transistors and no capacitor.

### 3b. Filled example: Peide Ye (the top-ranked group)

**Send through:** Ye's official Purdue pages ([group papers](https://engineering.purdue.edu/~yep/Papers/EDL_2024_In2O3%20600C_Lin.pdf); [Purdue ECE news, 2026](https://engineering.purdue.edu/ECE/News/2026/purdue-researchers-build-3d-chip-platform-for-faster-more-efficient-ai-computing)).

```text
Subject: In2O3 FET tail statistics: a sponsored-research question

Dear Professor Ye,

I am [Your name], founder of [Company / "an early-stage startup (incorporating)"]. We are working on DRAM-class memory built from oxide transistors processed below 400 °C.

Your group's EDL 2024 paper (Lin et al.) on top-gate ALD In2O3 FETs with a 600 °C budget for DRAM, and Purdue's September 2026 three-tier In2O3 platform on 200 mm wafers, are among the closest work we found.

We need the tail, not the median: the 1e-4 to 2e-5 quantile of attoamp off-state leakage, and the 1e-4 quantile of random telegraph noise, on at least 1e5 cells per split at 85-125 °C, after hydrogen, anneal and bond splits. The attached one-page spec lists the structures and pass lines. Our search did not find such a dataset in print.

Two questions:
1. Does your group hold per-device leakage or noise distributions on at least 1e4 devices that you could share under an NDA?
2. Would you consider sponsored research on an In2O3 split of this lot from January 2027? A rough scope and cost would help.

Could we have a 20-minute call?

Best regards,
[Your name]
[Title], [Company] | [Email] | [Phone]
```

**Fact check.**

| Fact in the draft or behind it | Tag | Source |
|---|---|---|
| Peide Ye is at Purdue University, ECE | [REPORTED] | LAB_TARGETS §2.1 (✔ name, institution, topic) |
| Lin et al., top-gate enhancement-mode ALD In₂O₃ FETs with a 600 °C thermal budget "for DRAM applications", IEEE EDL 2024 | [REPORTED] | Ye group papers; UNIST record (vol. 45, no. 10) |
| Purdue's ECE news item of 2026-09-16 on the three-tier In₂O₃ platform on 200 mm wafers names Ye as lead | [REPORTED] | Purdue ECE news, 2026 |
| Where that stack was built (Birck or elsewhere) | [UNVERIFIED] | So the draft says "Purdue reported", not "at Birck" |
| Purdue reported >100,000 devices over 52 dies (2026). Not used in the draft; you can mention it on a call | [REPORTED] | LAB_TARGETS §1.2 |
| No US group was found that publishes RTN tail statistics on oxide transistors. The draft's "Our search did not find such a dataset in print" rests on this | [REPORTED as a negative result] | LAB_TARGETS §0 |
| Sponsored research is the recommended route for a non-engineer: the group's students fabricate and measure | [ESTIMATE] | LAB_TARGETS §0, Route A |

**Word count:** 198 [ESTIMATE, counted by script on 2026-11-04].

---

## 4. A DRAM characterization partner for RAW-BER Phase 1

**Who.** The top DRAM partner in [LAB_TARGETS Part 3](LAB_TARGETS.md#part-3--dram-characterization-partners-raw-ber-contract) is Minesh Patel, Rutgers Computer Science, New Jersey. The draft is filled for Patel. For Moinuddin Qureshi (Georgia Tech), Xun (Steve) Jian (Virginia Tech) or the SAFARI group (ETH Zürich), swap the "Your work" sentence for that row of LAB_TARGETS Part 3. **Send through:** [researchwithrutgers.com/en/persons/minesh-patel](https://www.researchwithrutgers.com/en/persons/minesh-patel/).

```text
Subject: DRAM error profiling: a subaward question

Dear Professor Patel,

I am [Your name], founder of [Company / "an early-stage startup (incorporating)"]. We want to measure how far DRAM refresh can be relaxed when chipkill error correction absorbs the weak-cell tail.

Your BEER and HARP work on on-die ECC, and the 2026 study of read-disturb thresholds in 212 real DDR4 chips, are the closest match we found.

Phase 1 runs six months from January 2027:
- a 150-module DDR4 screen from ≥30 date-code lots per vendor, then deep retention maps at 45, 65 and 85 °C;
- ≥24 DDR5 RDIMMs on open Antmicro testers, with ECS counts and post-on-die-ECC error maps inverted to raw bit error rate;
- 1,000 hours of variable-retention-time tracking, and a census of multi-chip error events.

The kill line: a chipkill-safe refresh interval under 4x the JEDEC window at 65 °C.

Two questions:
1. Does your lab run DRAM Bender or similar FPGA test rigs?
2. Would you consider a paid subaward or collaboration, from rig advice to running part of the DDR5 leg? A rough scope and cost would help.

Could we have a 20-minute call?

[Your name]
[Title], [Company] | [Email] | [Phone]
```

**Fact check.**

| Fact in the draft or behind it | Tag | Source |
|---|---|---|
| Minesh Patel is at Rutgers University, Computer Science (New Jersey). The 2024 joining year was not re-checked | [REPORTED] | Rutgers profile; LAB_TARGETS Part 3 |
| BEER infers on-die ECC from post-correction errors. HARP profiles errors with on-die ECC present | [REPORTED] | Patel CV; LAB_TARGETS Part 3 |
| DiscoRD (2026): read-disturb thresholds in 212 real DDR4 chips, with Rutgers and ETH co-authors | [REPORTED] | Semiconductor Engineering summary; arXiv citation from search results only |
| Phase 1 population: a 150-module DDR4 quick screen at 85 °C over ≥30 lots per vendor; deep retention maps on 60 modules at 45/65/85 °C; ≥24 DDR5 1a/1b RDIMMs on open Antmicro testers; ECS counts plus post-on-die-ECC maps inverted to raw BER; hourly re-maps for 1,000 h; failure-mode census | [ESTIMATE, study plan] | [raw-ber-contract §5.R](../dossiers/raw-ber-contract.md#5r-revised-decisive-experiment-revised-after-red-team) |
| Phase 1 costs ~$124k standalone and gives a yes/no at month 6 (2027-06-30) | [ESTIMATE, study plan] | raw-ber §5.R; [decision.json](../research/stage3/decision.json) |
| NO-GO if the chipkill-safe interval, including VRT, is <4x the JEDEC window at 65 °C (DDR5 <128 ms; DDR4 <256 ms) | [ESTIMATE, study plan] | raw-ber §9 kill #1; decision.json |
| GO needs ≥6x the window at 85 °C and ≥24x at 65 °C, multi-chip events ≤10%, and a grade that holds on ≥95% of modules. Only the kill line is in the draft, because the grade test is a planned filing | [ESTIMATE, study plan] | raw-ber §11.4 |
| The Antmicro RDIMM DDR5 tester is open hardware (Apache-2.0) on an AMD Artix UltraScale+ FPGA, Google-funded | [REPORTED] | Antmicro blog; LAB_TARGETS Part 3 |
| Whether Patel's lab runs DRAM Bender rigs. The dossier lists Rutgers as such a lab, but LAB_TARGETS did not confirm it | [UNVERIFIED] | Asked in question 1 |
| No US commercial lab was found that sells DDR5 retention characterization as a service, so a university subaward is the route | [REPORTED as a negative result] | LAB_TARGETS Part 3 |
| The standalone RAW-BER plan carries $60k for collaborator subawards. The judges' $1M budgets give RAW-BER Phase 1 $90-120k. Neither number is in the draft | [ESTIMATE, study plan] | raw-ber §5.R line 11; [report §8](../DRAM_MOONSHOT_REPORT.md#8-the-1m-portfolio-and-gates) |

**Word count:** 199 [ESTIMATE, counted by script on 2026-11-04].

---

## 5. Follow-up and pitch

### 5a. Two-line follow-up

Send it 5 business days after the first email, and once more 7 days after that. After three tries with no reply, move to the next name on the list [ESTIMATE: a common cadence, not from a source].

```text
Subject: Re: [original subject]

Hello [Name], I am following up on my note of [date] about [the oxide tail lot / DRAM error profiling]. [Oxide emails only: The one-page spec is attached again.]
Is there a better person to ask, or a time for a 15-minute call in the next two weeks?
```

**Word count:** 52, including the subject line [ESTIMATE, counted by script on 2026-11-04].

**If the answer is "no".** "Thank you for the quick answer. Could you name a group or facility that might take this on?"

### 5b. 90-second phone or video pitch

Read it aloud once with a timer. Without the time marks it is about 188 spoken words. At 130-150 spoken words a minute that takes 75-87 seconds [ESTIMATE]. The time marks are cues, not lines to recite.

```text
[0-15 s] Thanks for the time. I'm [Your name], founder of [Company]. I come from software. [If true: I'm recruiting a device-physicist co-founder.]

[15-35 s] We ran an invention study on new ways to make DRAM. Ten concepts came out. Seven depend on one number published data do not give: how bad the worst one-in-ten-thousand oxide transistors are, not the median.

[35-55 s] Concretely: off-state leakage at the one-in-ten-thousand to one-in-fifty-thousand level, in attoamps, and random telegraph noise at one-in-ten-thousand, in IGZO-class transistors near 0.01 square microns, at 85 to 125 °C, after a 400 °C hydrogen, anneal and bond budget.

[55-70 s] Our lead concept is oxide gain cells bonded next to a GPU. Our model says about 10x lower energy per bit than HBM, from short wires. Whether the cell holds its bit at 105-125 °C depends on that tail. Either answer is worth publishing.

[70-90 s] The ask: one shared lot from January 2027, at least 100,000 cells per split. The spec lists every structure and pass line. Can you run it, or part of it? What cost and lead time? Do you hold tail data on over 10,000 devices we could see under NDA?
```

**Word count:** 198 [ESTIMATE, counted by script on 2026-11-04].

**RAW-BER swap-in** (replace the 35-70 s part for a DRAM partner): "We want to know how far DRAM refresh can be relaxed when chipkill ECC absorbs the weak cells. Our model says about 9x less refresh energy on DDR5 server modules at 85 °C. It dies if the safe interval is under 4x the JEDEC window at 65 °C."

**Pitch facts.**

| Fact | Tag | Source |
|---|---|---|
| 10 concepts survived 181 objections; all 10 were downgraded | [ESTIMATE, study result] | [decision.json](../research/stage3/decision.json) headline |
| 7 of the 10 concepts depend on the oxide tail | [ESTIMATE, study judgment] | [README](../README.md); spec page 1 |
| Published data describe medians, while every pass line sits in the tail | [ESTIMATE, study judgment] | [report §1](../DRAM_MOONSHOT_REPORT.md#1-the-answer-in-one-page) |
| ~10x lower energy per bit than HBM (0.37 vs 3.95 pJ/bit), which comes from geometry, not cell physics | [ESTIMATE, study model] | decision.json BEST_BET; HS §11 |
| The capacity claim dies if every split fails retention ≥1 s at 105 °C, drift σ ≤75 mV or RTN ≤100 mV | [ESTIMATE, study plan] | decision.json BEST_BET kill |
| ~9x refresh energy on DDR5 RDIMMs at 85 °C, with chipkill | [ESTIMATE, study model] | raw-ber §11.3 |

---

## Sources

**Repo files** (links relative to this file): [LAB_TARGETS.md](LAB_TARGETS.md) (§0, §1, §1.1-1.4, §2.1, Part 3, Part 4, unverified list); [OXIDE_TAIL_SPEC_onepage.md](OXIDE_TAIL_SPEC_onepage.md); [OXIDE_TAIL_SPEC.md](OXIDE_TAIL_SPEC.md) ("Before you send page 1", §7); [DRAM_MOONSHOT_REPORT.md](../DRAM_MOONSHOT_REPORT.md) §1, §8, §9; [README.md](../README.md) ("Honest limits"); [decision.json](../research/stage3/decision.json); [judge_physicist.json](../research/stage3/judge_physicist.json), [judge_investor.json](../research/stage3/judge_investor.json), [judge_operator.json](../research/stage3/judge_operator.json) (monday_action); dossiers §11: [hot-side-memory](../dossiers/hot-side-memory.md), [raw-ber-contract](../dossiers/raw-ber-contract.md) (also §5.R, §9), [and-stack](../dossiers/and-stack.md); home lab: [README](../home-lab/README.md), [E6](../home-lab/E6_retention_tail_real_dram.md), [leakage_tail.py](../home-lab/code/T2_analysis/leakage_tail.py), [retention_map.py](../home-lab/code/T3_dram/retention_map.py).

**External** [REPORTED]. These are taken from LAB_TARGETS.md's Sources, which were read as search snippets on 2026-11-04. They were not re-fetched for this file, and no web search was run for it.
- Purdue Birck, become a user: https://birck.research.purdue.edu/equipment/become-a-user/
- Purdue Birck, partner with us: https://birck.research.purdue.edu/partner-with-us
- Purdue Birck iLab rates: https://purdue.ilab.agilent.com/service_center/show_external/4127/1000
- Purdue Birck FY24 rates vs current (memo): https://mailman.ecn.purdue.edu/archives/list/bnc-all@ecn.purdue.edu/message/QV6GR6XQBKTW7PU5OCDG7VQOPHRKJ2JN/attachment/6/BRKFY24RatesvsCurrent.pdf
- Georgia Tech cleanroom rates (effective 2025-09-01): https://matter-systems.gatech.edu/cleanroom/getting-started/rates
- Georgia Tech, become a user: https://matter-systems.research.gatech.edu/cleanroom/getting-started/become-user
- SENIC (Georgia Tech NNCI site) renewal with JSNN: https://ncat.edu/news/2020/09/jsnn-georgia-tech-senic-grant-renewal.php
- Ye, EDL 2024 In₂O₃ 600 °C paper: https://engineering.purdue.edu/~yep/Papers/EDL_2024_In2O3%20600C_Lin.pdf ; UNIST record: https://scholarworks.unist.ac.kr/handle/201301/85599
- Purdue ECE news (2026-09-16), 3D In₂O₃ platform: https://engineering.purdue.edu/ECE/News/2026/purdue-researchers-build-3d-chip-platform-for-faster-more-efficient-ai-computing
- Datta, Georgia Tech directory: https://www.ece.gatech.edu/faculty-staff-directory/suman-datta ; IEDM 2020 abstract record: https://investigadores.uandes.cl/en/publications/double-gate-w-doped-amorphous-indium-oxide-transistors-for-monoli/
- Alam, Purdue CRISP profile: https://engineering.purdue.edu/CRISP/people/affiliate-faculty-expertise/ashraf-alam
- Yu, gain-cell last-level-cache paper (IEEE TC 75(3), 2026): https://faaiqgwaqar.github.io/assets/gain-cell-llc-paper.pdf ; group page: https://shimeng.ece.gatech.edu/?p=916
- Patel, Rutgers profile: https://www.researchwithrutgers.com/en/persons/minesh-patel/ ; CV: https://people.cs.rutgers.edu/~mp2099/files/minesh_patel_cv.pdf
- DiscoRD, 212 DDR4 chips (Semiconductor Engineering summary): https://semiengineering.com/identifying-read-disturbance-threshold-of-dram-chips-eth-zurich-rutgers/
- Antmicro RDIMM DDR5 tester 2.0: https://antmicro.com/blog/2024/12/data-center-rdimm-ddr5-tester-2-0/ ; repo: https://github.com/antmicro/ddr5-tester
- Negative RTN-tail search (example result): https://researchonline.ljmu.ac.uk/id/eprint/23450/
