# DD5 — U.S. Open Memory IP (compiler service → gain-cell & ReRAM macros)

`04_DEEPDIVES/open-memory-ip.md` · Author `p4w-open-memory-ip` · Phase 5 red-team revisions `p5r-open-memory-ip` · As of 2026-11-01

- **Phase 5 status: DOWNGRADED (revised after red team).** All 26 red-team objections are answered in §14 and in `research/phase5/responses_open-memory-ip.json`. 7 were accepted as kills, 16 as downgrades, 3 as mitigated, and none was refuted. The T2 legs (C-32 gain cell, C-22 ReRAM) are **killed**. The C-33 wedge survives only as a **part-time side line**: in the revised model it never pays the founder within 36 months.
- **Model:** `models/open-memory-ip.py`, re-run 2026-11-01 after the red team, exit 0. Its "RED-TEAM REVISIONS (Phase 5)" block lists every changed input (old → new, objection id). Output is captured in `research/phase4/open-memory-ip_model_output.md`; section 0 there prints the Phase 4 and Phase 5 headlines side by side.
- **Research notes:** `research/phase4/open-memory-ip_notes.md`.
- **Sources:** `research/sources/p4-open-memory-ip.jsonl`, plus cross-references in `p4w-open-memory-ip.jsonl`.
- **Model calendar:** m1 = Dec-2026. The glut scenario starts at m14 (Jan-2028).
- **Tags:** [VERIFIED-git] marks primary data read directly from a public git repository. Other tags follow `research/CONVENTIONS.md`.


> **Phase 6 decision note (added after both red-team rounds).** The red team cut this deep dive to the C-33 wedge as a side line (the C-32 and C-22 T2 legs are killed), and that characterization stands. Because every other deep dive was killed or downgraded, the Phase 6 judge panel selected it as **FALLBACK — sequenced after DD2, never in parallel** (`research/phase6/decision.json`). Statements in §14 such as "side line only, not PRIMARY, FALLBACK or MOONSHOT" predate that decision. As FALLBACK, its paid kill-test steps shift ~2 months later than the §10 dates (to Jan–Feb 2027, after DD2's 2026-12-01 decision); its $0 written questions still go out in week 1 (see `FIRST_90_DAYS.md`).

---

## 0. Header

**Name:** U.S. Open Memory IP.

**Pitch (revised after red team):** Sell SRAM macros bigger than anything available free to university labs, startups and SBIR teams taping out on SkyWater 130nm and GF180 open shuttles. The macros are measured on one nominal shuttle lot at voltage and temperature points, with process corners simulated and correlated to that lot. The warranty covers re-delivery or a refund of fees. Charge a subscription plus a fee per tapeout. *Phase 4 also promised "measured PVT corners" and an option on gain-cell and ReRAM macros. The red team showed a shuttle slot cannot deliver the first, and the second is killed (§14).*

**Anchor and folded concepts.** The quotes are exact text from `03_SCORING.md` §7.5 and `research/phase3/scores_raw/*.json`.

| Role | ID | Concept | Tier | Why it is in this bundle |
|---|---|---|---|---|
| Anchor | C-33 | OpenRAM macro service for U.S. open-PDK tapeouts (SkyWater S130) | T0 | Founder scorer: "a credible part-time wedge, not an endgame." Card: "unless it becomes a broader open-PDK IP/characterization house (gf180mcu, IHP, gain-cell IP)" |
| Folded | C-32 | Si gain-cell eDRAM (GCRAM) IP for U.S. trailing-node SoCs | T2 | Veteran scorer: "Better engineering than C-01 (zero masks, no contamination fight)". Same PDK and the same compiler skills as C-33. |
| Folded | C-22 | TrustNVM: U.S.-made ReRAM secure-NVM chiplet on SkyWater S130 | T2 | Founder scorer: "The cleanest U.S.-made device path in the set". Weebit ReRAM is already qualified in S130. |

**Why folded:** one PDK, with the anchor as the wedge into the other two. The same scorers warn against the product stage: "RAAAM already owns the commercial Si gain-cell seat" (veteran, C-32), "a non-exclusive license buys no moat" (VC, C-22), and on the anchor, "likely a <$0.5-1M ARR lifestyle business." (VC). Phase 4 kept C-32 and C-22 as a gated option. **The red team killed both legs (revised after red team; §14):**
- **C-32:** a gain cell drawn to sky130 logic rules is unlikely to beat the pushed-rule 1.896 µm² 6T cell. There is also no leakage case at 130 nm.
- **C-22:** magnet immunity is shared by OTP, eFuse and S130's own embedded-NVM options.
- **Neither has a named buyer.**

**Capital tier:** the wedge is **T0**, run on the founder's $40k. Cash low is **$4.0k at m15 (revised after red team; Phase 4 had $20.4k at m7)**. That holds only because the model now gates one-time spends on cash, which pushes the first sky130 slot from m7 to m15 (model §0, §6). The T2 product stage is **killed**, so no external capital is planned.

**Scores and ranks** (`scores.csv`, 40 scored concepts):

| ID | Default | Capital-constrained | Moonshot |
|---|---|---|---|
| C-33 (anchor) | 80.0 (#3) | 82.5 (#5) | 76.7 (#2) |
| C-32 (folded) | 59.0 (#25) | 55.8 (#28) | 60.8 (#22) |
| C-22 (folded) | 57.0 (#31) | 54.2 (#29) | 59.2 (#24) |

**Three separate verdicts**

| Question | Verdict | One line |
|---|---|---|
| **POSSIBLE?** | **Yes, at simulation level** (wedge); **no on this PDK** (T2, revised after red team) | The compiler and PDKs exist, and a 1 KB sky130 macro is silicon-verified (TRL 6). No public sky130 macro of 16 KB or more is silicon-verified; the published 16 KB attempt left only a log [VERIFIED-git], and 4/8 KB OpenRAM test-chip configurations from 2021 have no published measurements. An MPW slot gives one nominal lot, so "measured PVT corners" cannot be delivered; "measured at nominal, corners simulated" can. On sky130, gain cells have no density or leakage case, and ReRAM's magnet axis is shared by OTP and S130 eNVM. |
| **PROFITABLE?** | **No, as a job; marginal, as a side line** (revised after red team) | 57% gross margin. Cash-positive from m12 with the founder unpaid. **The founder is never paid within 36 months in BASE, GLUT or SEVERE.** Peak monthly GP is $8.0k against the $11.85k needed. ARR at m36 is $65.7k (run-rate $164.1k) against a ~$0.42M/yr serviceable ceiling. A full free release cuts ARR at m36 to $34.0k (model §6–7). |
| **DOABLE BY THIS FOUNDER?** | **Yes, but only with a signed memory contractor** (wedge); **no** (T2) | Automation, CI, the portal and sales are the founder's skills. The founder cannot judge the timing sign-off they sell, so the business is only as good as one contract memory engineer, who must sign a 12-month exclusivity by m3 (new kill criterion). T2 is killed. |

**Brutal summary (revised after red team)**
- **Real gap, cheap test, glut-proof.** The largest free macros are 4 KB on sky130 and 1 KB on GF180 [VERIFIED-git]. A 60% DDR5 glut cuts m36 ARR by only 16%.
- **Smaller than Phase 4 said.** Half of the 298 projects a year were the author's estimates. The revised count is 228 projects a year, which gives 27 paying projects a year, an active-account cap of 55 and a ceiling of about **$0.42M/yr**. Only 80 of the 228 are U.S.-fab; GF180MCU shuttle wafers are made in Singapore.
- **Mostly services.** Subscriptions are only 29–40% of revenue, and every service sale burns $150/h contract hours.
- **Paying the founder would need about 27 accounts by m18,** 48% of every account that could exist. The revised BASE has 8.7.
- **"Free" is now in the base case.** OCD and Chips4Makers already have GF180 SRAM silicon, so every scenario carries an expected-value free-release haircut from m24. A full free release cuts ARR at m36 to $34.0k.
- **"Characterized" was oversold.** A shuttle slot gives one nominal lot, so the licence is re-scoped to "measured at nominal, corners simulated", repriced to $12k, and carries a warranty limited to re-delivery or a refund of fees.
- **T2 is dead.** No buyer, no density case on sky130 logic rules, no leakage case at 130 nm, and C-22's only axis is shared by OTP and S130 eNVM.

**Verdict (revised after red team): a part-time side line. Not a PRIMARY, and not a FALLBACK either, because it never pays the founder within 36 months. Run the strengthened day-30 test only if the founder wants side income from it.**

---

## 1. How it works (for a smart non-engineer)

**Every useful chip needs a scratchpad,** a block of fast on-chip memory (SRAM). Designers don't draw it by hand. They drop in a pre-built block called a *macro*.

A macro is like a pre-engineered roof truss. Someone has drawn it, checked it against the factory's rules and, ideally, built one and measured how fast it runs and when it fails. Big chip companies get these trusses free from their foundry, or they buy compilers from Synopsys or Cadence under NDA.

**A second, open world now exists.** Public design rules (PDKs) cover SkyWater's 130nm fab in Bloomington, MN ("sky130") and GlobalFoundries' 180nm process ("GF180"). Cheap shared wafer runs ("shuttles") let dozens of projects split one wafer at about $7–15k a slot. About 230 full-chip projects a year use these open or academic shuttles (model §2; revised after red team from ~300). Only about 80 of them are U.S.-fab: the wafer.space GF180MCU runs are fabricated by GlobalFoundries in Singapore ([Crowd Supply, Run 3](https://www.crowdsupply.com/wafer-space/gf180mcu-run-3)) [REPORTED].

**The free memory blocks for these processes are small:**
- The largest are 4 KB on sky130 and 1 KB on GF180.
- Only a 1 KB sky130 macro has been proven in silicon.
- A small RISC-V microcontroller wants 8–64 KB [ESTIMATE: the TinyQV variant on wafer.space Run 2 already carries 9.5 kB of scratch RAM ([ws-run2](https://github.com/wafer-space/ws-run2))].

**Small blocks also waste space.** A 2 KB sky130 macro packs 57.6 kbit/mm², while the cell itself allows 527 kbit/mm². Most of the block is "plumbing": decoders and sense amplifiers around a tiny array. Phase 4 claimed a properly banked 32–64 KB macro would reach about 316 kbit/mm² (5.5×). **Revised after red team: about 158 kbit/mm², roughly 2.7×.** Going from the 1 KB to the 2 KB OpenRAM macro adds 11.5 µm² per added bit, six times the bitcell, so OpenRAM's periphery does not amortise the way a commercial compiler's does. The kill test measures a real 32 KB macro (model §1).

**What the company does:**

```
 OpenRAM (free) ──► founder's automation: generate 8–64 KB, DRC/LVS check, timing models, CI
                                   │
                                   ▼
             contract VLSI engineer reviews ──► test macros ride a shuttle slot ($3.75–15k)
                                                         │   3–6 months in the fab
                                                         ▼
          bench measurement on one nominal lot: on-chip BIST/delay-line timing,
          voltage, temperature (rented thermal forcing), yield on ≥50 die
                                                         │
                                                         ▼
   customer gets: layout + nominal-lot measured timing + simulated corners
                  + integration help + re-delivery/refund warranty
   pays: $200 or $800/month · $3k or $10k per tapeout · $12k licence (revised after red team; was $20k)
```

**Why pay when the code is free?** A failed block wastes the $7–15k slot and 3–6 months. The customer buys confidence.

**The later options (T2): killed after the red team (§14).** Kept here only to explain what was dropped.
- **A gain cell (C-32)** uses 2–3 transistors instead of SRAM's 6. It holds a tiny charge that leaks away in microseconds to milliseconds, so it must be rewritten ("refreshed") like DRAM. The payoff is lower idle leakage and 1.25–1.43× density in measured silicon ([BIU CRIS](https://cris.biu.ac.il/en/publications/4t-gain-cell-providing-unlimited-availability-through-hidden-refr/)) [REPORTED].
- **ReRAM (C-22)** stores data by switching a thin oxide's resistance, so it keeps the data with the power off. Weebit Nano has already qualified a 256 Kb ReRAM block in SkyWater's 130nm process ([Weebit](https://www.weebit-nano.com/news/press-releases/weebit-nanos-reram-ip-now-fully-qualified-in-skywater-technologys-s130-process/)) [REPORTED]. We would license it to build a small key-storage chip.

**Where it beats "RAM" (Rule 4).** Not on $/GB: sky130 SRAM costs about $1,330/GB, 73× DDR5's base price (model §1).
- **Wedge axis, sky130: supply security and access.** That is the time and cost to get silicon-correlated on-chip memory into a U.S.-fabbed ASIC, for open-shuttle teams with no NDA compiler (about 80 projects a year).
- **Wedge axis, GF180: access only (revised after red team).** GF180MCU shuttle wafers are made in Singapore, so the supply-security axis does not apply to about 148 of the 228 projects a year.
- **C-22 axis (killed):** a trusted U.S. flow plus magnet immunity. OTP, eFuse and S130's own embedded-NVM options share the magnet immunity, and no named buyer needs more than Toggle MRAM's 8,000 A/m.

---

## 2. Cost and unit-economics model

All figures come from `models/open-memory-ip.py` (section numbers refer to its printed output) unless another source is cited. Every price, rate and conversion assumption is an [ESTIMATE]; the basis for each is listed in the model's INPUTS block and in `research/assumptions/p4-open-memory-ip.md`.

### 2.1 The axis is not $/GB

| Item | Value | Source |
|---|---|---|
| sky130 6T bitcell (1.896 µm²) | 527.4 kbit/mm² limit | [SkyWater bitcell lib](https://github.com/google/skywater-pdk-libs-sky130_fd_bd_sram) [VERIFIED-git] |
| Largest free sky130 macros (OpenRAM 1 KB / 2 KB) | 43.0 / 57.6 kbit/mm² | [efabless macros](https://github.com/efabless/sky130_sram_macros), [VLSIDA macros](https://github.com/VLSIDA/sky130_sram_macros) [VERIFIED-git] |
| Banked 32–64 KB macro, 30% array efficiency (revised after red team; Phase 4 used 60% = 316.5 kbit/mm², 5.5×) | **158.2 kbit/mm² (2.7×)** | model §1 [ESTIMATE]. OpenRAM's 1 KB → 2 KB step adds 11.5 µm² per added bit (6.0× the bitcell). Measured in the day 1–7 run (§10) |
| Largest free GF180 macros (GF 512 B / OCD 1 KB) | 19.6 / 52.7 kbit/mm² | [GF IP](https://github.com/google/globalfoundries-pdk-ip-gf180mcu_fd_ip_sram), [OCD](https://github.com/RTimothyEdwards/gf180mcu_ocd_ip_sram) [VERIFIED-git] |
| Gain cell vs 6T density (C-32, **killed**) | 1.25–1.43× (silicon, same-rule comparison); 1.67–2.0× (vendor) | Silicon: [BIU CRIS](https://cris.biu.ac.il/en/publications/4t-gain-cell-providing-unlimited-availability-through-hidden-refr/). Vendor: [Silicon Saxony 2026-09](https://silicon-saxony.de/en/globalfoundries-and-raaam-memory-technologies-development-of-next-generation-gcram-technology-and-a-test-chip-on-the-fdx-platform/), [arXiv 2507.10849](https://arxiv.org/html/2507.10849v1) [REPORTED]. Against sky130's pushed-rule 6T a logic-rule gain cell is ~0.75–0.95× [ESTIMATE, §14] |
| sky130 SRAM vs DDR5 (BASE $18.33 / GLUT $8.15 / SEVERE $2.04 per GB, from `models/dram_cost_stack.py`) | ~$1,330/GB = 73× / 163× / 653× | model §1; 01_LANDSCAPE §4.4 [ESTIMATE] |

Macros are priced per design. The DRAM cycle reaches this business only through design-start budgets.

### 2.2 Market (revised after red team)

| Funnel step | Count | Source |
|---|---|---|
| Full-chip projects/yr on open/academic shuttles | **228** (Phase 4: 298) | model §2. wafer.space 2×54 ([ws-run2](https://github.com/wafer-space/ws-run2)) [VERIFIED-git]; GF university pilot 40 ([Synopsys 2025-09-04](https://news.synopsys.com/2025-09-04-Synopsys-and-GlobalFoundries-Establish-Pilot-Program-to-Bring-Chip-Design-and-Manufacturing-to-University-Classrooms?asPDF=1)). ChipFoundry **30** (was 60), Cadence **20** (was 30) and MOSIS/Commons/other **30** (was 60) are [ESTIMATE], cut per RT-VC-DD5-01 |
| … of which GF180MCU, fabbed by GF in Singapore | 148 | wafer.space Run 3 page ([Crowd Supply](https://www.crowdsupply.com/wafer-space/gf180mcu-run-3)) [REPORTED, via search snippet] |
| … of which U.S.-fab (sky130, MOSIS, Commons) | **80** | The only projects to which the supply-security axis applies |
| Tiny Tapeout tiles in 2026 (a funnel, not buyers) | 899 | [TT sky-26a](https://github.com/TinyTapeout/tinytapeout-sky-26a), [sky-26b](https://github.com/TinyTapeout/tinytapeout-sky-26b), [ihp-26a](https://github.com/TinyTapeout/tinytapeout-ihp-26a), [gf-0p2](https://github.com/TinyTapeout/tinytapeout-gf-0p2) [VERIFIED-git] |
| × need memory beyond free macros | 30% | About 10 of 51 wafer.space Run 2 listings mention SRAM/RAM [VERIFIED-git] |
| × willing to pay | 40% | [ESTIMATE]; there is no willingness-to-pay data, and the kill test measures it |
| **Paying projects/yr** | **27** (Phase 4: 36) | model §2 |
| Active-account cap (×2 years per group) | **55** (38 academic, 16 commercial) (Phase 4: 72) | model §2; academic share 0.70 (was 0.60, RT-HYP-DD5-03) |
| **Serviceable ceiling at 100% share** | **$424.4k/yr** (Phase 4: $747.3k) | model §2 |

**Commercial NDA customers are out of reach.** SkyWater's S130 "already offers… SRAM compilers" and embedded-NVM options ([Business Wire, 2025-07-29](https://secure.businesswire.com/news/home/20250729379892/en/SkyWater-Technology-Expands-Leadership-in-U.S.-Semiconductor-Manufacturing-With-Infineon-IP-License-Agreement); [Silicon UK](https://www.silicon.co.uk/press-release/skywater-technology-expands-leadership-in-u-s-semiconductor-manufacturing-with-infineon-ip-license-agreement)), and mature-node compilers are traditionally foundry-sponsored ([D&R](https://www.design-reuse.com/news/9192/analysis-arm-artisan-merger-defining-moment.html)) [REPORTED]. Funded SBIR teams that go to production move there too, so the commercial share of accounts is cut to 30% (revised after red team).

### 2.3 Unit economics (BASE prices, model §3; revised after red team)

| Product line | Price | COGS | GM | Phase 4 |
|---|---|---|---|---|
| A1 Subscription, academic (sold as a $1.2k per-term course pack; POs lag 2 months) | $200/mo | $66 | 67% | $58, 71% |
| A2 Subscription, commercial | $800/mo | $114 | 86% | $102, 87% |
| B1 Tapeout service, academic (12 contract h at **$150**) | $3,000 | $1,990 | 34% | $1,690, 44% |
| B2 Tapeout service, commercial (30 contract h) | $10,000 | $4,900 | 51% | $4,150, 58% |
| C Licence: nominal-lot measured, corners simulated, refund-capped warranty (30 h + 10% reserve) | **$12,000** | $6,060 | 50% | $20,000 / $6,350 / 68% |

The contract rate rises from $125 to $150/h to pay for a 12-month exclusivity / non-compete from the memory contractor (RT-VC-DD5-03).

**Acquisition (revised after red team):**
- **Outbound:** capped at the number of distinct new project teams, 228/12 = **19 contacts a month** (was 30). 19 × 25% reply × 15% close = **0.71 accounts a month**. Going full-time adds no new names.
- **Inbound:** ramps to 1.2 accounts a month.
- **CAC:** $0.4k cash, or $2.0k loaded with founder time.
- **Lifetime GP:** $5.0k academic and $30.5k commercial, for a blended LTV/CAC of **6.2×** (was 12.3×).

The 15% close rate is still invented. The kill test measures it.

### 2.4 ARR, breakeven and cash low point (model §6; revised after red team)

| | BASE (DDR5 −10% in 2028) | GLUT (−60% from m14) | SEVERE (−90%) |
|---|---|---|---|
| First revenue | m4 (Mar-2027) | m4 | m4 |
| **Cash low point** (from $40.0k, with the cash gate) | **$4.0k at m15** (Feb-2028) | $2.8k at m15 | $3.6k at m18 |
| Cash-flow breakeven, **founder unpaid** (first of 3 positive months) | m12 (Nov-2027) | m12 | m12 |
| First month with GP ≥ $11.85k (founder-paid breakeven) | **never** (peak GP $8.0k at m36) | never ($6.4k) | never ($5.5k) |
| **Founder full-time** | **never** | never | never |
| Gross margin, 36 months | 57% | 55% | 53% |
| **Recurring ARR m12 / m18 / m24 / m36** | **$23.1k / $41.2k / $54.0k / $65.7k** | $23.1k / $36.8k / $46.8k / $54.9k | $23.1k / $34.3k / $42.9k / $49.3k |
| Run-rate incl. services m12 / m18 / m24 / m36 | $72.6k / $111.5k / $148.1k / $164.1k | $72.6k / $98.3k / $128.3k / $137.9k | $72.6k / $91.0k / $115.7k / $123.9k |
| 36-month revenue | $316.9k | $278.6k | $256.5k |
| Accounts at m36 (academic + commercial) | 11 + 5 | 11 + 4 | 11 + 3 |
| Characterized silicon: GF180 / sky130 | m11 / **m24** | m11 / m24 | m11 / m27 |
| End cash at m36 | $88.4k | $60.4k | $45.1k |

Phase 4 had BASE ARR of $66.6k at m18 and $157.6k at m36, breakeven at m8, the founder full-time at m20, and a cash low of $20.4k at m7.

**The cash gate.** On the Phase 4 schedule, the added spends (test structures, thermal forcing, a 40 h kill-test review, $150/h) drive BASE cash to −$8.2k at m11. That is beyond the $40k deployable (A-03). The model therefore defers each test chip, slot, bench or characterization spend until cash after paying it stays at $2.5k or more. The first sky130 slot waits from m7 to m15, so sky130 silicon arrives at m24.

**"Cash-positive from m12" means the business stops eating the founder's savings while the founder works for free.** By m36 it builds about $7k a month of gross profit for about 15 hours a week. That is side income, not a salary.

### 2.5 Revenue mix: a services business (BASE, model §5; revised after red team)

| Month | Subscriptions | Tapeout services | Licences | Total/month | Recurring share |
|---|---|---|---|---|---|
| m12 (Nov-2027) | $1.9k | $4.6k | $0.1k | $6.7k | 29% |
| m18 (May-2028) | $3.4k | $6.2k | $0.2k | $9.8k | 35% |
| m36 (Nov-2029) | $5.5k | $7.4k | $0.9k | $13.8k | 40% |

Every service and licence sale consumes contract VLSI hours. "SaaS" overstates it. "Staffing agency for OpenRAM" (RT-VC-DD5-03) is close to the truth.

### 2.6 Sensitivity (BASE, one input at a time; model §7; revised after red team)

| Case | Cash low | 3-mo cash-positive from | Founder full-time | ARR m18 | ARR m36 | Run-rate m36 |
|---|---|---|---|---|---|---|
| Base (revised) | $4.0k | m12 | never | $41.2k | $65.7k | $164.1k |
| Price ×0.7 | $2.6k | m10 | never | $28.8k | $46.0k | $109.4k |
| Price ×1.3 | $2.6k | m13 | never | $53.5k | $85.4k | $213.4k |
| Close rate ×0.7 | $3.4k | m13 | never | $29.6k | $49.1k | $124.4k |
| Close rate ×1.3 | $4.3k | m17 | never | $52.2k | $80.2k | $198.3k |
| Close rate ×0.5 (RT-HYP-DD5-01) | $2.6k | m10 | never | $21.5k | $36.6k | $88.1k |
| Churn ×1.3 | $3.6k | m12 | never | $39.4k | $58.4k | $152.4k |
| COGS ×1.3 | $2.8k | m12 | never | $41.2k | $65.7k | $164.1k |
| Academic share 0.80 (RT-HYP-DD5-03) | $2.9k | m12 | never | $34.1k | $55.1k | $136.4k |
| Licences removed (RT-HYP-DD5-02) | $4.9k | m12 | never | $41.2k | $65.7k | $152.9k |
| sky130 slot slips 6 months (RT-VC-DD5-04)¹ | $4.0k | m5 | never | $41.2k | $65.7k | $164.1k |
| No free release at all | $4.0k | m12 | never | $41.2k | $86.1k | $203.7k |
| **Full free-bundle shock at m18** | $3.4k | m12 | never | $31.1k | **$34.0k** | $96.3k |
| GLUT + full free shock | $2.8k | m12 | never | $27.7k | $27.5k | $79.0k |
| Upside: price ×1.3, close ×1.3, no free release | $6.1k | m12 | **m22** | $67.8k | $135.6k | $317.0k |
| SEVERE + all adverse 30% | $0.2k | never | never | $16.3k | $22.1k | $55.3k |

¹ The cash gate already holds the first sky130 slot to m15, so a 6-month slip from m7 changes nothing in revised BASE. The m5 cash-positive date is an artifact: with the m6 design spend deferred, months 5–7 have no one-time spend. On Phase 4 inputs the same slip still paid the founder at m21.

**Only the combined upside case pays the founder inside 36 months.** It needs prices 30% higher, a 30% better close rate and no free release, all at once.

### 2.7 What must be true (model §8; revised after red team)

1. **At least 27 paying projects a year:** 228 × 30% × 40%.
2. **Prices hold.** Even at ×1.3, the founder is not paid within 36 months unless close rates also beat plan and no free release arrives.
3. **Reply rate ≥25% and close rate ≥15%,** measured on distinct funded teams, not recycled names.
4. **To pay the founder: about 27 active paying accounts (≈19 academic + 8 commercial) by m18.** That is **48% of the 55-account cap**; revised BASE reaches 8.7. Equivalently, 2.3 commercial services a month or 2.0 licences a month. **This will not happen in any modeled case except the combined upside.**
5. **Large macros can be built.** A 16 KB sky130 macro must pass post-layout extracted SPICE at SS/1.62 V/125 °C and FF/1.98 V/−40 °C, with a 1,000-point bitcell Monte Carlo, in ≤200 contract hours. This is untested; only a log and unmeasured 4/8 KB test-chip configurations exist.
6. **No free release on sky130** of silicon-characterized macros of 16 KB or more for at least 18 months. A GF180 release is already in the base case.
7. **Shuttles keep running, and someone pays for them.**
   - ChipFoundry runs a shuttle only when it is ≥50% full, and it moves an under-filled run to the next shuttle ([Tiny Tapeout](https://tinytapeout.com/news/chipfoundry-sponsor/)).
   - TTSKY25b took about 8 months from submission close (2025-11-10) to expected chips (Jul-2026) ([Tiny Tapeout](https://tinytapeout.com/chips/ttsky25b/)) [REPORTED].
   - wafer.space Run 3 has no published dates.
8. **A memory contractor signs a 12-month exclusivity** (or a technical cofounder joins with equity) by m3.

### 2.8 The T2 overlay: **killed** (revised after red team)

The Phase 4 overlay was STTR Phase I ($305k), a Cadence ReRAM probe ($12k), a Weebit fee (~$100k), a $2.5M seed, STTR Phase II ($1.5M), a circuit cofounder ($440k) and a ReRAM chiplet. It is **killed** by RT-VC-DD5-02, RT-HYP-DD5-07, RT-PHY-DD5-03/04/05 and RT-VET-DD5-03/05 (§14):
- no named buyer;
- no density case for a logic-rule gain cell against sky130's pushed-rule 6T;
- no leakage case at 130 nm, and retention at 85 °C sets the refresh cost;
- magnet immunity is shared by OTP, eFuse and S130 embedded-NVM options;
- JESD47 qualification needs three lots, so the ReRAM chiplet line rises from $0.95M to ~$1.55M [ESTIMATE].

The model still prints the overlay in §9, for reference only. It is not part of any verdict or headline. **No external capital is planned.**

---

## 3. Target customer and the first ten customers

**Beachhead:** funded open-shuttle teams with a real memory need. These are university labs and courses that tape out repeatedly, small commercial aggregators, open SoC and FPGA builders, and SBIR teams on SkyWater. Tiny Tapeout hobbyists are the free funnel, not buyers.

| # | Customer | Why they buy | How to reach |
|---|---|---|---|
| 1 | **Brown University ENGN2912e (Saligane lab)**, project BRWN on wafer.space Run 1 ([ws-run1](https://github.com/wafer-space/ws-run1)) [VERIFIED-git] | Repeat course tapeout on GF180 (free macros max out at 1 KB). East Coast. (Its STTR PI role is dropped with T2.) | Email the instructor: a $200/mo course pack plus a $3k service each term. |
| 2 | **U.S. members of the Synopsys–GF GF180MCU pilot** (40 universities) ([Synopsys](https://news.synopsys.com/2025-09-04-Synopsys-and-GlobalFoundries-Establish-Pilot-Program-to-Bring-Chip-Design-and-Manufacturing-to-University-Classrooms?asPDF=1)) | A tapeout every term, with the same 1 KB ceiling. | Course pages and GF University Partnership contacts; a per-course licence. |
| 3 | **Avalon Semiconductors** (AS03/AS04 multi-project dies with RISC-V cores and a DRAM controller) ([ws-run1](https://github.com/wafer-space/ws-run1), [ws-run2](https://github.com/wafer-space/ws-run2)) | Repeat commercial customer; several designs share each die. | Through the project listing; commercial subscription plus a $10k service. |
| 4 | **TinyQV / TQVE builders** (RISC-V SoC, 9.5 kB scratch RAM on GF180) ([ws-run2](https://github.com/wafer-space/ws-run2)) | Already past the free 1 KB macro. | GitHub and the Tiny Tapeout community; a free preview to win the reference design. |
| 5 | **FABulous eFPGA (mole99)** ([ws-run2](https://github.com/wafer-space/ws-run2)) | FPGA configuration memory built from SRAM macros, so density is the product. | GitHub. Academic licence. |
| 6 | **Cloneless** (tamper-resistant ASICs) and the **Tillitis/Zedulo eFUSE + SRAM** chip ([ws-run1](https://github.com/wafer-space/ws-run1)) | Secure key storage. (They were the natural first C-22 ReRAM partners; C-22 is killed, so they are SRAM buyers only.) | Project listings. SRAM service offer. |
| 7 | **Sandia National Laboratories (MESA)**, which licensed Mobile Semiconductor's 180nm compilers ([D&R](https://us.design-reuse.com/news/45774/mobile-semiconductor-180nm-memory-compilers-sandia-national-laboratories.html)) [REPORTED] | Has already paid for trailing-node memory IP. | After sky130 silicon data exists (m24+ after the cash gate; revised after red team). Procurement-led; a long shot, and likely to ask for radiation data the plan does not fund. |
| 8 | **DoD SBIR/STTR performers on SkyWater 130/90nm** (precise type) | Funded; need U.S.-fab memory with a warranty; can expense $10–20k. Many will need SEE/TID radiation data, which is out of scope (revised after red team). | SBIR.gov award search on "SkyWater", "130nm", "sky130" and "ASIC", then email the PIs (method; not yet run). |
| 9 | **NORDTECH (NY) and NEMC (MA) hub project teams** ([Cornell 2026-04-29](https://research-and-innovation.cornell.edu/?p=6460); [MassTech](https://masstech.org/news/northeast-microelectronics-coalition-hub-celebrates-3725-million-federal-funding-power)) | East Coast prototyping; PROPEL subsidizes lab and fab time. | Hub events. Ask to be listed as a hub IP resource. |
| 10 | **Channels: ChipFoundry Marketplace, Cadence SKY130 MPW, MOSIS 2.0** ([ChipFoundry](https://github.com/chipfoundry/caravel_user_project); [SkyWater/Cadence](https://www.skywatertechnology.com/lowering-barriers-to-silicon-cadence-launches-mpw-aggregation-service-for-sky130/); [USC ISI](https://www.isi.edu/news/80945/mosis-2-0-revives-a-legacy-rehan-kapadia-outlines-a-bold-future-for-rapid-microelectronics-prototyping/)) | They resell per shuttle. **They are also the parties best placed to bundle macros for free.** | Partnership calls in the kill test (§10). Offer a revenue share. |

**Partners to approach first:**
- **Open Circuit Design LLC (Tim Edwards)** as contract characterization partner. A 12-month exclusivity on free large sky130 macros is now required; if OCD will not sign, look to OpenRAM alumni or Chips4Makers.
- **UCSC VLSIDA** as upstream. A written statement on its large-macro roadmap is now a pass condition (§10). The STTR PI role is dropped with T2.

Both are also the likeliest free substitutes (§5).

---

## 4. Go-to-market

**Channel**
1. **Direct technical outreach** to named owners of public shuttle projects, taken from the wafer.space and Tiny Tapeout repositories.
2. **Open core.** Free previews (LEF plus a datasheet) on GitHub and PyPI; characterized data and support are paid.
3. **Listings.** ChipFoundry Marketplace and MOSIS 2.0, with NSF Chip Design Hub awardees as academic distributors ([NSF](https://www.nsf.gov/funding/opportunities/chip-design-hub-enabling-access-semiconductor-chip-ecosystem-design)).

**Pricing (model §3)**

| Offer | Academic | Commercial / SBIR | Anchor |
|---|---|---|---|
| Subscription: hosted generator, library, CI regression, support | $200/mo | $800/mo | $2.4k/yr is a sixth to a third of one $7–15k slot; $9.6k/yr is about two contract-engineer weeks at $125/h |
| Tapeout service: configuration, DRC/LVS, timing sign-off, integration review | $3,000 | $10,000 | 20–100% of a slot; the buyer is de-risking the whole spin |
| Licence (revised after red team): one nominal MPW lot measured at voltage/temperature points, process corners simulated and correlated to that lot, yield on ≥50 die, 12-month warranty limited to re-delivery or a refund of fees, no radiation data | — | $12,000 (was $20,000) | 1.2× the commercial service fee. Below Weebit's ~$0.1M first-ever eNVM licence ([MST Access](https://www.weebit-nano.com/wp-content/uploads/2025/09/250901.-MST-Access-Report_WBT.AX-Not-just-play-money-090125.pdf)); Virage listed a compiler at $300k in 2001 ([Design World](https://www.designworldonline.com/synopsys-enters-embedded-memory-market/)) |

**Sales motion:**
- **Founder-led and asynchronous, so it fits the day job:** a technical email, a 20-minute call, then a deposit.
- **The closing event is the next ChipFoundry or wafer.space submission date.**
- **Tiny Tapeout designers** get free macros and convert when they move to full-chip slots.

**First 90 days of selling** (from 2026-11-02, before the academic winter break; days 1–30 are the §10 experiment)

| Days | Actions | Measurable output |
|---|---|---|
| 1–30 | Landing page with real prices and $500 refundable deposits; 120 named contacts (≥100 distinct funded teams); channel calls; 40 h extracted-SPICE + Monte Carlo review of a 16 KB macro | The §10 pass rules (revised after red team): deposits/LOIs, 2 commercial/SBIR LOIs ≥$10k, a signed simulation pass, written no-release statements |
| 31–60 | Convert deposits into signed orders. Publish preview library v0.1 (8/16/32 KB sky130; 2/4/8 KB GF180), labelled "simulated, not silicon-proven". Sign a contractor statement of work (SOW) with a 12-month exclusivity. Apply for the ChipFoundry Marketplace. | ≥3 signed orders; exclusive SOW signed; ≥200 PyPI downloads [ESTIMATE target] |
| 61–90 | Schedule first deliveries against the next shuttle deadline. Follow-up sequence. Start university vendor registration for each academic buyer (POs lag ~2 months). The NSF Project Pitch is dropped with T2. | ≥5 paying or committed accounts by m4 (Mar-2027) [ESTIMATE target: "committed" includes the day-30 deposits; the revised model expects only 0.23 new paying accounts in m4, because academic POs lag] |

---

## 5. Competitors and why you would win

| Competitor | Offer | Price / position | Threat |
|---|---|---|---|
| **OpenRAM (UCSC VLSIDA)** | Open SRAM compiler for sky130 and gf180mcu | Free (BSD-3). v1.2.50 on 2026-10-27; 116 commits in 12 months ([OpenRAM](https://github.com/VLSIDA/OpenRAM)) [VERIFIED-git] | **High.** It can publish large characterized macros at any time. |
| **Open Circuit Design LLC** | GF180 SRAM, 64 B–1 KB, on wafer.space silicon | Free (Apache-2.0); last commit 2026-10-30 ([repo](https://github.com/RTimothyEdwards/gf180mcu_ocd_ip_sram)) [VERIFIED-git] | **High on GF180.** Also the best contractor. |
| **Chips4Makers (Arrakeen)** | GF180 SRAM generator; 3 test chips on wafer.space G802 (Jul-2026) | Free ([GitLab](https://gitlab.com/Chips4Makers/arrakeen-sram-testchip)) [VERIFIED-git] | **High on GF180** |
| DFFRAM / GF `fd_ip_sram` | Flip-flop RAM up to 2,048 words; 64–512 B macros | Free; DFFRAM is flagged for hold violations on gf180mcuD ([DFFRAM](https://github.com/AUCOHL/DFFRAM)) [VERIFIED-git] | Medium / low |
| **SkyWater S130 compilers** | NDA SRAM compilers | Bundled ([Silicon UK](https://www.silicon.co.uk/press-release/skywater-technology-expands-leadership-in-u-s-semiconductor-manufacturing-with-infineon-ip-license-agreement)) [REPORTED] | Closes off all commercial S130 work |
| **Mobile Semiconductor** | SkyWater RH90 rad-hard SRAM compilers; 180nm compilers licensed to Sandia | Price not public ([SkyWater 2022-06-09](https://www.skywatertechnology.com/skywater-announces-availability-of-sram-memory-compiler-for-90-nm-strategic-rad-hard-by-process-offering/)) [REPORTED] | **High in DoD/trusted** |
| Cadence (ex-Arm Artisan), Synopsys | Commercial and foundry-sponsored compilers | The designer often pays $0 ([Silicon UK](https://www.silicon.co.uk/press-release/cadence-to-acquire-arm-artisan-foundation-ip-business)) [REPORTED]; Cadence also runs the SKY130 MPW | Medium; could bundle |
| **RAAAM** (C-32) | Proprietary 3T Si gain cell | $17.5M Series A led by NXP, Nov-2025 ([AnySilicon](https://anysilicon.com/news/raaam-memory-technologies-raises-17-5-million-in-oversubscribed-series-a-led-by-nxp-semiconductors/)); TSMC N2 test chip taped out Mar-2026 ([AnySilicon](https://anysilicon.com/news/raaam-selects-avnet-asic-as-its-vca-partner-for-tsmcs-2nm-gcram-development-and-qualification/)); GF FDX lead-customer access early 2027 ([Silicon Saxony](https://silicon-saxony.de/en/globalfoundries-and-raaam-memory-technologies-development-of-next-generation-gcram-technology-and-a-test-chip-on-the-fdx-platform/)) [REPORTED] | **Decisive for C-32** |
| **OpenGCRAM (Stanford)** | Open gain-cell compiler (TSMC N40) | Free with the final paper ([arXiv 2507.10849](https://arxiv.org/html/2507.10849v1); [arXiv 2602.21278](https://arxiv.org/abs/2602.21278v1)) [REPORTED] | Removes "compiler" as a moat |
| **Everspin Toggle MRAM**, Honeywell trusted MRAM (C-22) | 16–32 Mb U.S.-made rad-tolerant NVM | Everspin: $40M DoW onshore program ([Electronics360 2026-04](https://electronics360.globalspec.com/article/23702/everspin-earns-40-million-mram-deal-for-defense-memory-services)) [REPORTED] | **Decisive for C-22**, except where magnet immunity matters |

**Win conditions (honest)**
1. **Be first with silicon-measured sky130 macros of 16 KB or more.** Revised after red team: the "one shuttle cycle (about 6 months)" head start is withdrawn. The cash gate puts sky130 silicon at m24, and shuttle turns run about 8 months. What remains is "first with nominal-lot measured timing and simulated corners", if no one publishes first.
2. **Sell what free code lacks:** sign-off, integration review, a named person on deadline day, and a refund-capped warranty. The layout files will leak by design, since only 11 of 51 listed wafer.space Run 2 projects are private [VERIFIED-git].
3. **Hire a free author under a 12-month exclusivity** (new kill criterion at m3).
4. **Serve the SBIR and Commons teams** on open sky130 that do not need radiation data. Mobile Semiconductor serves the rad-hard ones.

**Where you lose:**
- **GF180,** probably within 12 months, because OCD and Chips4Makers already have silicon. The revised model now assumes this in every scenario (P = 0.6 by m24).
- **Commercial S130,** where the foundry compiler is free.
- **DoD rad-hard.**
- **Gain cells,** against RAAAM.
- **ReRAM,** against Toggle MRAM.
- **Whenever a channel owner makes memory a loss leader.**

---

## 6. IP position

**What you own:** almost nothing foundational.
- **The base is open.** OpenRAM is BSD-3, OCD is Apache-2.0, and the PDKs are open ([Google, 2023-11](https://opensource.googleblog.com/2023/11/open-source-pdks-joining-linux-foundation-chips-alliance.html?m=0)) [REPORTED].
- **What you would own:**
  - measured characterization data and test-chip designs;
  - banking, timing and CI automation, kept as trade secrets;
  - customer relationships and a warranty brand;
  - possibly weak patents on the periphery [ESTIMATE].
- **The moat** is "a first-mover lead that takes one shuttle cycle to copy" (VC scorer).

**What you license** (C-22 and C-32 are killed after the red team; kept for the record):
- **For C-22: Weebit ReRAM.** SkyWater's licence is non-exclusive, with fees "not material" and contingent on customers ([Weebit](https://www.weebit-nano.com/news/press-releases/weebit-nanos-reram-ip-now-fully-qualified-in-skywater-technologys-s130-process/)). A product needs its own licence. Analysts estimate past upfront fees at about $0.1M (first ever), $0.29M and $1.8–2.6M (01_LANDSCAPE §0, "What changed in Phase 1b" #3; [MST Access](https://www.weebit-nano.com/wp-content/uploads/2025/09/250901.-MST-Access-Report_WBT.AX-Not-just-play-money-090125.pdf)) [REPORTED]. The fee for a fabless startup is unknown.
- **For C-32:** STTR or university IP, from UCSC VLSIDA or Stanford.

**What you can't own or use:** RAAAM's GCRAM (Bar-Ilan/EPFL lineage), SkyWater's NDA compilers, or Mobile Semiconductor's RH90 compilers.

**FTO risks, ranked**
1. **Gain-cell patents (C-32).** RAAAM and its Bar-Ilan/EPFL lineage hold an active estate, and the area is crowded: for example, 2T-cell retention scaling is described in [US 11,127,455](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11127455) [REPORTED]. Get a landscape read before any C-32 spend (§11 #10).
2. **Efabless platform patents.** ChipFoundry acquired 15 issued and 3 pending patents ([Minster/GlobeNewswire 2025-09-03](https://business.minstercommunitypost.com/minstercommunitypost/article/gnwcq-2025-9-3-chipfoundry-acquires-efabless-assets-to-propel-custom-silicon-innovation)) [REPORTED]. Their scope is [UNVERIFIED]. Check them before building an Efabless-like hosted generator or marketplace.
3. **Open-source licence terms.** BSD-3 needs attribution. Apache-2.0 needs notices and carries a patent-termination clause. Low risk if followed.
4. **ReRAM resale.** Weebit's terms may bar selling parts made from Cadence-MPW die [UNVERIFIED]. This is a kill-test question.

---

## 7. Regulatory and funding path

**Rules that matter**
- **Export controls.**
  - **The wedge is EAR99-class.** Scorer: "Negligible; BSD open-source tooling, EAR99".
  - **The C-22 rad variant is controlled.** It falls under 3A001.a.1 / 9A515, possibly ITAR XV(d), which means U.S.-person-only data and about $25–75k/yr of compliance (01_LANDSCAPE §8) [UNVERIFIED-M].
  - **Screen customers at onboarding.** Tiny Tapeout users are global.
- **Trusted foundry.**
  - SkyWater is a DMEA Category 1A Trusted Foundry ([BusinessWire 2026-01-26](https://www.businesswire.com/news/home/20260125927336/en/IonQ-to-Acquire-SkyWater-Technology-Creating-the-Only-Vertically-Integrated-Full-Stack-Quantum-Platform-Company)).
  - IonQ, which closed its acquisition on 2026-07-31, says SkyWater "remains fully committed to all of our semiconductor foundry customers" ([IonQ](https://ionq.com/news/ionq-completes-acquisition-of-skywater-technology)) [REPORTED]. There is no post-close DMEA confirmation.
  - Open-MPW die are not trusted-flow parts [ESTIMATE].
- **Warranty.** E&O insurance at $250/mo from the first licence (model).

**Non-dilutive funding** (revised after red team: this route existed only for T2, which is killed. It is kept for the record and for the §11 #10–11 revival conditions.)
- **SBIR PI constraint.**
  - The SBIR PI must spend more than half their time with the small business, at award and for the whole project ([NIST](https://www.nist.gov/tpo/small-business-innovation-research-program-sbir/resources/participation-eligibility-and)). **That excludes the founder while they keep the day job.**
  - The STTR PI may be employed by the research institution ([NIH GPS 18.5](https://grants.nih.gov/grants/policy/nihgps/html5/section_18/18.5_small_business_innovation_research_and_small_business_technology_transfer_programs.htm); 01_LANDSCAPE §7) [REPORTED-P].
  - **So the route is STTR with a university PI:** UCSC VLSIDA (Guthaus), the Stanford OpenGCRAM group, or the Brown Saligane lab.
- **STTR terms.**
  - NSF Phase I is up to $305k (NSF 26-510). The Semiconductors topic includes an IC Design subtopic ([NSF Seed Fund](https://seedfund.nsf.gov/topics/semiconductors/); [summary](https://grantedai.com/grants/semiconductors-s-sbir-sttr-program-national-science-foundation-nsf-small-bu-ef99bad7)) [REPORTED]. A Project Pitch comes first.
  - The program is reauthorized through 2031-09-30 ([IEDC 2026-04-15](https://www.iedconline.org/news/2026/04/15/federal-policy-updates/federal-policy-update-sbir-and-sttr-reauthorized/)).
  - New rules: per-firm proposal caps from FY2027, foreign-ownership screening, and Strategic Breakthrough awards that need a prior Phase II and a 1:1 match ([Wiley](https://www.wiley.law/alert-SBIR-STTR-Reauthorization-Brings-New-Opportunities-and-Obligations-to-Consider); 01_LANDSCAPE §7).
  - At least 30% of the award goes to the university [UNVERIFIED].
  - **Grants are funding, not revenue** (A-04).
- **DoD.** No 2026 topic on memory compilers or trusted NVM was found. The only one found, DARPA DV017 on extreme-environment NVM, closed 2026-08-19 ([DARPA](https://www.darpa.mil/research/programs/non-volatile-memory-extreme-environments)).
- **Other programs.**
  - Microelectronics Commons hubs: NORDTECH, and NEMC with PROPEL. The Commons has fabricated more than 61,000 chips ([NSTXL 2026-03](https://nstxl.org/microelectronics-commons-delivering-results-2026/)).
  - NSF Chip Design Hub, and MOSIS 2.0 ([AAC 2026-07](https://allaboutcircuits.com/news/mosis-partners-with-globalfoundries-extending-40-year-prototyping-legacy)), as channels.
  - MA START ($100–500k), but only after a Phase II [UNVERIFIED-L/M].

**When and whether to raise (revised after red team)**
- **Never.** The wedge runs on the founder's $40k with a gated cash low of $4.0k at m15. The STTR and the $2.5M seed existed only to fund T2, which is killed. Revised BASE run-rate is $148.1k at m24 and $164.1k at m36, far below the old $250k seed gate.
- **Stay T0 and harvest the cash.** The STTR route above remains available only if a T2 revival condition in §11 is ever met.

---

## 8. 18-month roadmap with milestones

Revised after red team. The schedule follows the model's cash gate: a test chip, slot, bench or characterization spend happens only when cash after paying it stays at $2.5k or more.

| Month | Calendar | Milestone | Gate (measurable) |
|---|---|---|---|
| m0 | Nov-2026 | Kill experiment (§10, strengthened) | §10 pass rules |
| m1 | Dec-2026 | Form the LLC; licence and refund-capped warranty templates ($1k); kill-test spend booked ($8.1k) | Terms reviewed |
| m2–m3 | Jan–Feb-2027 | Contract build-out, 60 h at $150 ($9k); GF180 test chip with on-chip BIST and delay-line timing structures (20 h, $3k); library v0.1 in CI | ≥6 macros DRC/LVS-clean in CI; **exclusive contractor SOW or technical cofounder signed by 2027-02-28** |
| **m4** | Mar-2027 | **First invoices.** wafer.space GF180 half slot with test macros + BIST ($3.75k) | ≥1 paying customer (model: 0.23 new accounts, revenue $1.6k) |
| m5–m6 | Apr–May-2027 | sky130 test-chip structures (20 h, $3k); academic POs start landing | ≥1 paying account and ≥$4k invoiced (model: 0.9 accounts, $6.8k cumulative); ≥2 university POs or P-card subscriptions |
| m7 | Jun-2027 | ChipFoundry sky130 slot **only if cash allows** ($15k) | Model: cash $11.8k → **deferred to m15** |
| m9 | Aug-2027 | Test bench ($4k) | — |
| m11 | Oct-2027 | GF180 silicon characterized ($6k contractor + $2.5k thermal forcing); first GF180 licence | ≥2 of 3 sizes working on ≥80% of ≥50 tested die; BIST-measured access time ≤1.5× simulated |
| **m12** | Nov-2027 | One-year review | ARR ≥$12k and run-rate ≥$36k (model $23.1k / $72.6k); ≥3 accounts (model 4.6) |
| m14 | Jan-2028 | The glut scenario starts | ≥1.0 new accounts/month (model `new` field: BASE 1.17, GLUT 1.11) |
| m15 | Feb-2028 | ChipFoundry sky130 slot paid (gated) | Cash ≥$17.5k before paying |
| m17 | Apr-2028 | wafer.space GF180 full slot with 8–32 KB production macros ($7.25k; gated from m16) | Second-spin yield ≥ first |
| **m18** | May-2028 | Side-line review (the full-time decision is moot in every modeled scenario) | ≥5 accounts and ARR ≥$20k (model 8.7 and $41.2k). Full-time only if trailing-3-month GP ≥$11.85k (model $5.3k) |
| m24 | Nov-2028 | sky130 silicon characterized ($6k + $2.5k), sky130 licences open | The ≥16 KB sky130 macro passes the m11 test |
| m27 | Feb-2029 | Second ChipFoundry sky130 slot, 16–64 KB ($15k; gated from m19) | — |

The STTR proposal (m6–m9), STTR decision (m15) and Cadence ReRAM probe (m18) rows are removed: T2 is killed.

Dollar amounts are the model's one-time spends. The gates are this author's [ESTIMATE], set near BASE values.

---

## 9. Team required

| Role | When | Cost | Where to find |
|---|---|---|---|
| **Founder (CEO):** automation, CI, portal, sales | m0 onward; 15 h/week throughout (full-time never reached in the revised model) | $0 (A-03) | — |
| **Contract memory/VLSI engineer:** macro review, extracted-SPICE/Monte Carlo sign-off, test structures, integration. **Must sign a 12-month exclusivity by m3** | m0 (40 h), m2–m3 (60 h + 20 h), m6 (20 h), then 12–30 h per job | $150/h (revised after red team; was $125) [ESTIMATE]; $9k build-out plus $6k test structures plus service COGS (model) | Open Circuit Design LLC; OpenRAM/UCSC VLSIDA alumni; Chips4Makers; the FOSSi (ORConf, Latch-Up) and Tiny Tapeout communities |
| **Characterization contractor** with bench access and rented thermal forcing | m11, m24 (sky130), m24 (second campaign) | $6k each + $2.5k thermal each + $4k bench (model; revised after red team) | University labs (Brown; NEMC/NORDTECH members through PROPEL) |
| ~~University STTR PI~~ (T2 killed) | — | — | — |
| Bookkeeper and attorney (licence, warranty, export screening) | m1 onward | $350/mo inside $600/mo fixed opex (model) | Local small-business firms |
| ~~FTO patent counsel, full-time circuit cofounder, C-22 designer and test engineer~~ | T2 killed (revised after red team) | — | — |
| **Alternative to the exclusive contractor:** a technical cofounder with equity | Before m3 | Equity, no cash | OpenRAM alumni, FOSSi community |

**The single point of failure** is the contract memory engineer. The best candidate (OCD) is also the likeliest free competitor. Revised after red team: without a signed exclusivity or a technical cofounder by m3, the venture is killed (§11 #2).

---

## 10. The cheapest experiment that could kill it (revised after red team)

**Hypothesis to kill:** "Funded open-PDK teams will pay for larger, silicon-correlated macros; OpenRAM can make a 16 KB sky130 macro that passes extracted-SPICE corners and Monte Carlo; and the two parties who could release such macros free will say in writing that they won't within 18 months."

**Budget and timing (revised after red team):** about **$9.1k** (was $5.1k), still under the $10k limit. It runs 2026-11-02 (day 1) to the decision on 2026-12-01 (day 30), before the academic winter break. Deposits are refundable, so they are not cost.
- Contractor: 40 h at $150 = $6.0k.
- Compute $0.3k, web/Stripe $0.2k, outreach $0.1k.
- Licence and refund-capped warranty template $1.0k.
- One hub event ≤$1.5k.

The model now carries this spend: $1k at m1 as the template item, and $8.1k at m1 as "kill-test spend not elsewhere in model" (model R15).

**Steps**
1. **Days 1–20 ($6.3k): build the previews and prove buildability.**
   - Run OpenRAM in the cloud for DRC/LVS-clean 8/16/32 KB sky130 and 2/4/8 KB GF180 macros with simulated Liberty files ($0.3k).
   - **Measure the real area of the 32 KB sky130 macro.** This replaces the 30% array-efficiency assumption (RT-PHY-DD5-06).
   - The contract memory designer spends **40 h ($6.0k)** on a post-layout extracted SPICE read/write of the 16 KB sky130 macro:
     - at SS / 1.62 V / 125 °C and FF / 1.98 V / −40 °C;
     - with a bitcell Monte Carlo of 1,000 points or more on the sky130 SRAM special-device models;
     - signed by the contractor (RT-VET-DD5-01).

     If those models carry no usable mismatch data, the contractor says so in writing, and that fails (iii).
2. **Days 3–7 ($1.2k): put up the offer.**
   - A landing page with real prices and LEF/datasheet previews labelled "simulated, not silicon-proven".
   - Stripe **$500 refundable deposits** ($0.2k).
   - Licence terms ($1k): measured at nominal, corners simulated, yield on ≥50 die, a 12-month warranty limited to re-delivery or a refund of fees, and no radiation data.
3. **Days 3–25 ($0.1k): contact about 120 named people, at least 100 of them distinct funded teams** (not hobby tiles; RT-HYP-DD5-01):
   - all public wafer.space Run 1/2 project owners;
   - Tiny Tapeout SoC builders;
   - U.S. GF-pilot instructors;
   - about 20 SBIR performers on SkyWater, each asked whether they need radiation data;
   - the NORDTECH and NEMC managers;
   - MOSIS 2.0.
4. **Days 7–20 ($0): written channel questions.**
   - **UCSC VLSIDA and Open Circuit Design:** a written statement on whether they plan to publish silicon-characterized ≥16 KB macros under an open licence within 18 months. **Silence counts as "yes".** OCD is also asked whether it will sign a 12-month exclusivity as contractor.
   - **ChipFoundry and wafer.space:** dated 2027 shuttle calendars, marketplace terms, and any plan for free large macros.
   - **Cadence:** next SKY130 run, and would they bundle macros?
   - **Synopsys / GF University Partnership:** what memory IP the GF180MCU pilot gives its members (RT-VC-DD5-05).
   - The Weebit question is dropped with C-22.
5. **Days 20–30 (≤$1.5k): one hub or community event.** Convert deposits into LOIs. Test the refund-capped warranty language with at least 2 buyers (RT-VC-DD5-06).

**Pass/fail, decided now (revised after red team)**

PASS (continue as a side line) only if **all four** hold:
- **(i) Paid demand:** at least 3 paid $500 deposits against orders of $2k or more each, **or** at least $15k in signed LOIs. Both count only from distinct funded teams, and at least 100 of the 120 contacts must be distinct funded teams.
- **(ii) Serious buyers:** **at least 2** commercial or SBIR buyers commit at $10k or more each. Each must confirm in writing that they will stay on the open PDK for production, and must accept the restated licence: nominal-lot measured, corners simulated, refund-capped warranty, no radiation data.
- **(iii) Buildable, on evidence:** the contractor-signed extracted-SPICE and Monte Carlo pass in step 1, with the reviewer's estimate that the full ≥16 KB sky130 line takes 200 h or less.
- **(iv) No free release coming, in writing:** written statements from **both** UCSC VLSIDA and OCD that they do not plan silicon-characterized ≥16 KB open macros within 18 months, **or** a signed exclusivity/non-compete with whichever of them did not give one. **No answer = FAIL** (RT-HYP-DD5-04). Also, no channel owner may confirm a free release.

**KILL** if (i), (iii) or (iv) fails. **PIVOT** if only (ii) fails: run an academic-only GF180 side line with no sky130 slot and no full-time goal.

**Expected outcome:** pass probability is about 15–25% [ESTIMATE]. Test (iv) asks open-source maintainers for a written commitment they have little reason to give.

---

## 11. Explicit kill criteria (revised after red team)

"Model" means the revised BASE value in `models/open-memory-ip.py`. The Phase 4 thresholds were set near the Phase 4 model; the revised BASE would trip the Phase 4 m6 gate (2 accounts / $8k), so every gate is re-set near half the revised model.

1. **2026-12-01 (day 30).** The experiment fails (i), (iii) or (iv) → **kill DD5.**
2. **2027-02-28 (m3).** No signed contractor SOW with a 12-month exclusivity / non-compete on free silicon-characterized ≥16 KB sky130 macros, and no technical cofounder with equity → **kill** (RT-VC-DD5-03; new).
3. **2027-05-31 (m6).** No paying account, or under $4k invoiced (model: 0.9 accounts, $6.8k) → **kill.** Fewer than 2 university POs or P-card subscriptions closed → the academic subscription becomes a free tier and academics buy services only (RT-HYP-DD5-06; new).
4. **2027-11-30 (m12).** GF180 silicon: fewer than 2 of 3 sizes working on ≥80% of ≥50 tested die, or BIST-measured access time more than 1.5× simulated → **stop selling GF180 licences**, and kill if operating cash cannot fund a re-spin. *(Moved from m11 because characterization is now at m11. It is now evaluable, since the test chip carries on-chip BIST and delay-line timing and the bench has thermal forcing.)*
5. **2027-11-30 (m12).** ARR under $12k, or run-rate under $36k (about half the model's $23.1k / $72.6k) → **kill.**
6. **2028-12-31 (m25).** The ≥16 KB sky130 macro fails test #4 → **kill the sky130 line**, the only line with SBIR and U.S.-fab buyers. *(Was m14; sky130 silicon now arrives at m24 after the cash gate.)*
7. **Any date.** UCSC, OCD, ChipFoundry, Cadence or Chips4Makers releases free silicon-characterized ≥16 KB **sky130** macros → **stop one-time spend within 30 days**, harvest, or sell the contracts to the releaser (model full shock: ARR at m36 $34.0k). A **GF180** release is already in the base case: it stops GF180 one-time spend only.
8. **2028-05-31 (m18).** Fewer than 5 paying accounts, or ARR under $20k (model: 8.7 accounts, $41.2k) → **kill.** The founder does not quit the day job unless trailing-3-month GP reaches $11.85k (model: $5.3k; never reached in any modeled scenario except the combined upside).
9. **Kill-test answer (VC-05).** The Synopsys–GF pilot gives members free GF180 memory IP of 8 KB or more → remove its 40 projects from the market, and re-run the model before any GF180 slot spend.
10. **C-32 (gain cell): killed now.** It revives only if all of these exist:
    - a sky130 gain-cell layout clean on the **standard logic DRC deck** at ≤1.58 µm², including its share of read-reference and refresh periphery;
    - ≥1 ms worst-bit retention at 85 °C (post-layout Monte Carlo);
    - refresh plus leakage power below measured sky130 6T standby at ≥16 KB;
    - a named buyer LOI of $75k or more;
    - a clean FTO read.

    Checking the layout costs ~16 contract hours (~$2.4k) and is not funded.
11. **C-22 (ReRAM): killed now.** It revives only if all of these exist:
    - a named defense secure-boot program states a magnetic-field requirement above 8,000 A/m;
    - it needs rewrites that rule out OTP, eFuse and S130's own embedded NVM;
    - an LOI of $75k or more;
    - a SkyWater quote for three S130+ReRAM engineering lots plus a JESD47 qual-house quote.
12. **2029-05-31 (m30).** Trailing-3-month GP under $11.85k (model: $7.6k) → DD5 is permanently a side line. Seed and T2 are already off.

---

## 12. Cycle test: the 2028–29 glut (DDR5 −60%) and the severe case

**How the DRAM price reaches this business.** Macros are priced per design, so DRAM prices matter only through commercial design-start budgets:
- One-third of the DDR5 drop passes through to commercial demand.
- 0.15 of it passes to commercial price, and 0.5 to commercial churn.
- Academic demand is held flat [ESTIMATE; `research/assumptions/p4-open-memory-ip.md`].
- The glut starts at m14. The cash low point is $4.0k (BASE), $2.8k (GLUT) and $3.6k (SEVERE), all held above zero by the cash gate (revised after red team).

| | BASE (−10%) | GLUT (−60%, DDR5 $8.15/GB) | SEVERE (−90%, $2.04/GB) |
|---|---|---|---|
| Commercial demand / price / churn | ×0.97 / ×0.98 / ×1.05 | ×0.80 / ×0.91 / ×1.30 | ×0.70 / ×0.87 / ×1.45 |
| ARR m36 (revised after red team) | $65.7k | $54.9k (−16%) | $49.3k (−25%) |
| Run-rate m36 (revised) | $164.1k | $137.9k (−16%) | $123.9k (−25%) |
| 36-month revenue (revised) | $316.9k | $278.6k (−12%) | $256.5k (−19%) |
| Founder full-time (revised) | never | never | never |
| Commercial accounts at m36 (revised) | 5 | 4 | 3 |
| Phase 4 ARR m36 / founder full-time | $157.6k / m20 | $125.8k / m25 | $105.7k / m30 |
| sky130 SRAM $/GB vs DDR5 | 73× | 163× | 653× |

(Model §1, §4 and §6. The percentages are computed from those values.)

**What hurts is the glut combined with something else.** GLUT plus a full free-bundle shock leaves ARR at m36 at $27.5k. SEVERE with every input 30% adverse ends at $0.2k cash with ARR of $22.1k, and the cash gate defers sky130 silicon to m46. The founder is not paid in any of these, nor in the revised BASE.

**T2 in a glut** (killed after the red team; kept for the record):
- **Gain cells:** priced in die area, but trailing-node royalties track wafer prices. eMemory's 8-inch royalties fell 15.9% year on year ([Yahoo Finance](https://finance.yahoo.com/markets/stocks/articles/ememory-technology-inc-roco-3529-030030531.html)) [REPORTED].
- **C-22:** defense NVM demand is decoupled from DRAM.
- **Seed money** is scarcer in a downturn [ESTIMATE].

**Verdict (revised after red team): it survives the glut but not "free", and it never reaches a salary.** The DRAM cycle cuts m36 ARR by 16–25%. The free-release risk and the small market already keep the founder unpaid in BASE.

---

## 13. Sources

All URLs below are logged in `research/sources/p4-open-memory-ip.jsonl` or other `research/sources/*.jsonl` files, with cross-references in `p4w-open-memory-ip.jsonl`.

**Market, shuttles and channels**
- https://github.com/TinyTapeout/tinytapeout-sky-26a
- https://github.com/TinyTapeout/tinytapeout-sky-26b
- https://github.com/TinyTapeout/tinytapeout-ihp-26a
- https://github.com/TinyTapeout/tinytapeout-gf-0p2
- https://github.com/wafer-space/ws-run1
- https://github.com/wafer-space/ws-run2
- https://www.crowdsupply.com/wafer-space/gf180mcu-run-2
- https://www.eenewseurope.com/en/tiny-tapeout-sees-industrial-boost-as-it-recovers-from-efabless-closure/
- https://business.minstercommunitypost.com/minstercommunitypost/article/gnwcq-2025-9-3-chipfoundry-acquires-efabless-assets-to-propel-custom-silicon-innovation
- https://github.com/chipfoundry/caravel_user_project
- https://www.skywatertechnology.com/lowering-barriers-to-silicon-cadence-launches-mpw-aggregation-service-for-sky130/
- https://opensource.googleblog.com/2023/11/open-source-pdks-joining-linux-foundation-chips-alliance.html?m=0
- https://news.synopsys.com/2025-09-04-Synopsys-and-GlobalFoundries-Establish-Pilot-Program-to-Bring-Chip-Design-and-Manufacturing-to-University-Classrooms?asPDF=1
- https://www.isi.edu/news/80945/mosis-2-0-revives-a-legacy-rehan-kapadia-outlines-a-bold-future-for-rapid-microelectronics-prototyping/
- https://allaboutcircuits.com/news/mosis-partners-with-globalfoundries-extending-40-year-prototyping-legacy
- https://nstxl.org/microelectronics-commons-delivering-results-2026/
- https://research-and-innovation.cornell.edu/?p=6460
- https://masstech.org/news/northeast-microelectronics-coalition-hub-celebrates-3725-million-federal-funding-power
- https://www.nsf.gov/funding/opportunities/chip-design-hub-enabling-access-semiconductor-chip-ecosystem-design

**Memory IP, macros and competitors**
- https://github.com/VLSIDA/OpenRAM
- https://github.com/VLSIDA/sky130_sram_macros
- https://github.com/efabless/sky130_sram_macros
- https://github.com/google/skywater-pdk-libs-sky130_fd_bd_sram
- https://github.com/RTimothyEdwards/gf180mcu_ocd_ip_sram
- https://github.com/google/globalfoundries-pdk-ip-gf180mcu_fd_ip_sram
- https://gitlab.com/Chips4Makers/arrakeen-sram-testchip
- https://github.com/AUCOHL/DFFRAM
- https://www.silicon.co.uk/press-release/skywater-technology-expands-leadership-in-u-s-semiconductor-manufacturing-with-infineon-ip-license-agreement
- https://www.design-reuse.com/news/9192/analysis-arm-artisan-merger-defining-moment.html
- https://www.silicon.co.uk/press-release/cadence-to-acquire-arm-artisan-foundation-ip-business
- https://www.designworldonline.com/synopsys-enters-embedded-memory-market/
- https://www.skywatertechnology.com/skywater-announces-availability-of-sram-memory-compiler-for-90-nm-strategic-rad-hard-by-process-offering/
- https://us.design-reuse.com/news/45774/mobile-semiconductor-180nm-memory-compilers-sandia-national-laboratories.html
- https://finance.yahoo.com/markets/stocks/articles/ememory-technology-inc-roco-3529-030030531.html

**Gain cell (C-32)**
- https://arxiv.org/html/2507.10849v1
- https://arxiv.org/abs/2602.21278v1
- https://cris.biu.ac.il/en/publications/4t-gain-cell-providing-unlimited-availability-through-hidden-refr/
- https://silicon-saxony.de/en/globalfoundries-and-raaam-memory-technologies-development-of-next-generation-gcram-technology-and-a-test-chip-on-the-fdx-platform/
- https://anysilicon.com/news/raaam-memory-technologies-raises-17-5-million-in-oversubscribed-series-a-led-by-nxp-semiconductors/
- https://anysilicon.com/news/raaam-selects-avnet-asic-as-its-vca-partner-for-tsmcs-2nm-gcram-development-and-qualification/
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11127455

**ReRAM, SkyWater and C-22 incumbents**
- https://www.weebit-nano.com/news/press-releases/weebit-nanos-reram-ip-now-fully-qualified-in-skywater-technologys-s130-process/
- https://www.weebit-nano.com/wp-content/uploads/2025/09/250901.-MST-Access-Report_WBT.AX-Not-just-play-money-090125.pdf
- https://ionq.com/news/ionq-completes-acquisition-of-skywater-technology
- https://www.businesswire.com/news/home/20260125927336/en/IonQ-to-Acquire-SkyWater-Technology-Creating-the-Only-Vertically-Integrated-Full-Stack-Quantum-Platform-Company
- https://electronics360.globalspec.com/article/23702/everspin-earns-40-million-mram-deal-for-defense-memory-services

**Funding and regulation**
- https://seedfund.nsf.gov/topics/semiconductors/
- https://grantedai.com/grants/semiconductors-s-sbir-sttr-program-national-science-foundation-nsf-small-bu-ef99bad7
- https://www.nist.gov/tpo/small-business-innovation-research-program-sbir/resources/participation-eligibility-and
- https://grants.nih.gov/grants/policy/nihgps/html5/section_18/18.5_small_business_innovation_research_and_small_business_technology_transfer_programs.htm
- https://www.iedconline.org/news/2026/04/15/federal-policy-updates/federal-policy-update-sbir-and-sttr-reauthorized/
- https://www.wiley.law/alert-SBIR-STTR-Reauthorization-Brings-New-Opportunities-and-Obligations-to-Consider
- https://www.darpa.mil/research/programs/non-volatile-memory-extreme-environments

**Internal sources:**
- `models/open-memory-ip.py` and `models/dram_cost_stack.py`
- `research/phase4/open-memory-ip_notes.md`
- `research/phase2/concepts_master.json` (C-33, C-32, C-22)
- `research/phase3/selection.json` and `research/phase3/scores_raw/*.json`
- `scores.csv`, `03_SCORING.md` §7.5, `01_LANDSCAPE.md` §0 (Phase 1b #3), §4.4, §7, §8 and §9
- `ASSUMPTIONS.md` A-03, A-04 and A-05

**Added in Phase 5 (red team; logged in `research/sources/p5r-open-memory-ip.jsonl`)**
- https://www.crowdsupply.com/wafer-space/gf180mcu-run-3
- https://tinytapeout.com/chips/ttsky25b/
- https://tinytapeout.com/news/chipfoundry-sponsor/
- https://tinytapeout.com/news/sky130-confirmed/
- https://par.nsf.gov/servlets/purl/10495552
- https://platform.efabless.com/projects/187
- https://foss-eda-tools.googlesource.com/third_party/shuttle/sky130/mpw-003/slot-015/
- https://foss-eda-tools.googlesource.com/third_party/shuttle/sky130/mpw-003/slot-010/+/5be26416e2a88200062567acd3085ad1cbdaf13e/OpenRAM/myconfig_sky130.py
- https://secure.businesswire.com/news/home/20250729379892/en/SkyWater-Technology-Expands-Leadership-in-U.S.-Semiconductor-Manufacturing-With-Infineon-IP-License-Agreement
- https://www.mouser.lt/pdfDocs/magnetic-field.pdf (Everspin AN02049, via `p5-PHY.jsonl`)
- `research/phase5/rt_VET.json`, `rt_VC.json`, `rt_HYP.json`, `rt_PHY.json`; `research/phase5/responses_open-memory-ip.json`

---

## 14. Red-team outcome

Phase 5, agent `p5r-open-memory-ip`, 2026-11-01. Four reviewers raised 26 objections against DD5: VET (DRAM process veteran), VC (semiconductor VC), HYP (hyperscaler procurement) and PHY (condensed-matter physicist). Every objection and its full response is recorded in `research/phase5/responses_open-memory-ip.json`, and none was deleted.

**Tally:** 7 ACCEPTED-KILL (all on the T2 legs) · 16 ACCEPTED-DOWNGRADE · 3 ACCEPTED-MITIGATED · 0 REFUTED. Two factual corrections to the objections are noted in their responses: the Cadence SKY130 MPW did offer a Weebit-ReRAM option in 2026 (VET-05), and a 6-month slip on Phase 4 inputs still paid the founder at m21 (VC-04). Neither changes a disposition.

### 14.1 Objections and dispositions

| Objection | Severity | Disposition | Action |
|---|---|---|---|
| RT-VET-DD5-01 | MAJOR | ACCEPTED-MITIGATED | Kill-test (iii) now needs signed extracted-SPICE corners + 1,000-pt Monte Carlo; 40 h review; kill test $9.1k |
| RT-VET-DD5-02 | MAJOR | ACCEPTED-DOWNGRADE | Licence restated 'TT measured, corners simulated', $20k → $12k; thermal forcing + BIST in model |
| RT-VET-DD5-03 | MAJOR | ACCEPTED-KILL | C-32 killed; logic-DRC ≤1.58 µm² + retention test is the first revival gate |
| RT-VET-DD5-04 | MAJOR | ACCEPTED-DOWNGRADE | GF180MCU confirmed Singapore-fabbed; supply-security axis limited to 80 U.S.-fab projects/yr |
| RT-VET-DD5-05 | MAJOR | ACCEPTED-KILL | C-22 killed; qual line $0.4M → $1.0M (reference); Cadence 2026 ReRAM option noted as a correction |
| RT-VET-DD5-06 | MINOR | ACCEPTED-DOWNGRADE | sky130 characterized m13 → m16 (m24 after cash gate) |
| RT-VC-DD5-01 | FATAL | ACCEPTED-DOWNGRADE | Market 298 → 228 projects/yr, ceiling $747k → $424k; free release in base case; 'FALLBACK' withdrawn |
| RT-VC-DD5-02 | FATAL | ACCEPTED-KILL | T2 (C-32 + C-22) killed; no external capital planned |
| RT-VC-DD5-03 | MAJOR | ACCEPTED-DOWNGRADE | Contract rate $125 → $150 for exclusivity; new m3 kill criterion (exclusive SOW or technical cofounder) |
| RT-VC-DD5-04 | MAJOR | ACCEPTED-DOWNGRADE | Shuttle timing revised; slip variant run (P4: FT m21; revised: no change); head-start claim withdrawn |
| RT-VC-DD5-05 | MAJOR | ACCEPTED-DOWNGRADE | Academic share 0.60 → 0.70; Synopsys–GF memory-IP question + market-removal rule |
| RT-VC-DD5-06 | MINOR | ACCEPTED-MITIGATED | Warranty limited to re-delivery/refund of fees; ≥2 buyers must accept in kill test |
| RT-HYP-DD5-01 | MAJOR | ACCEPTED-DOWNGRADE | Outreach capped at 19 distinct teams/mo; share of cap 42% → 28%; (i) counts distinct funded teams only |
| RT-HYP-DD5-02 | MAJOR | ACCEPTED-DOWNGRADE | Licence repriced $12k, attach 0.25 → 0.15; licences-off case added |
| RT-HYP-DD5-03 | MAJOR | ACCEPTED-DOWNGRADE | Academic share 0.70 (0.80 sensitivity); (ii) needs 2 open-PDK LOIs ≥$10k |
| RT-HYP-DD5-04 | MAJOR | ACCEPTED-DOWNGRADE | Test (iv): silence = FAIL, written statements from UCSC + OCD; partial free release in every scenario |
| RT-HYP-DD5-05 | MINOR | ACCEPTED-DOWNGRADE | Singapore fab confirmed; 'U.S.' scope = sky130 only; DoD channel halved |
| RT-HYP-DD5-06 | MINOR | ACCEPTED-MITIGATED | Per-term course pack; 2-month PO lag modeled; m6 university-PO gate |
| RT-HYP-DD5-07 | MINOR | ACCEPTED-KILL | T2 killed (no buyer); revival needs a named ≥$75k LOI |
| RT-PHY-DD5-01 | MAJOR | ACCEPTED-DOWNGRADE | Licence: nominal lot measured, corners simulated, yield on ≥50 die, refund-capped warranty |
| RT-PHY-DD5-02 | MAJOR | ACCEPTED-DOWNGRADE | BIST/delay-line structures + thermal rental costed; cash gate added; cash low $4.0k@m15 |
| RT-PHY-DD5-03 | MAJOR | ACCEPTED-KILL | C-32 killed: logic-rule cell ~2.0–2.5 µm² ≥ pushed-rule 6T [ESTIMATE] |
| RT-PHY-DD5-04 | MAJOR | ACCEPTED-KILL | C-32 killed: no leakage case at 130 nm; retention/power added to revival gate |
| RT-PHY-DD5-05 | MAJOR | ACCEPTED-KILL | C-22 killed: magnet axis shared by OTP/eFuse/S130 eNVM; no >8,000 A/m buyer |
| RT-PHY-DD5-06 | MINOR | ACCEPTED-DOWNGRADE | Array efficiency 60% → 30% (158 kbit/mm², 2.7×) until the 32 KB macro is measured |
| RT-PHY-DD5-07 | MINOR | ACCEPTED-DOWNGRADE | No SEE campaign; rad scope excluded; DoD channel halved; (ii) buyers accept no rad data |

### 14.2 Changes made

**Model** (`models/open-memory-ip.py`, "RED-TEAM REVISIONS (Phase 5)" block; output §0 prints each change):
- **Market.**
  - R1–R3: ChipFoundry 60 → 30, Cadence 30 → 20, MOSIS/Commons/other 60 → 30 projects/yr. Total 298 → 228; paying 36 → 27; cap 72 → 55; ceiling $747k → $424k.
  - R4: academic share 0.60 → 0.70.
- **Licence.**
  - R5: price $20k → $12k.
  - R6: attach 0.25 → 0.15 licences per commercial account per year.
  - R7: DoD channel 0.08 → 0.04 licences per month.
- **Cost and timing.**
  - R8: contract rate $125 → $150/h.
  - R9: GF180 characterized m10 → m11.
  - R10: sky130 characterized m13 → m16.
- **New mechanics.**
  - R11: outbound contacts capped at distinct new teams (19 a month).
  - R12: 2-month academic procurement lag.
  - R13: expected-value free release, weight 0.39 from m24, in every scenario.
  - R16: cash gate at a $2.5k floor; deferrable spends wait and characterization dates move with them.
- **Context only.** R14: array efficiency 60% → 30%.
- **One-time spends.** R15: $68.5k → $94.6k, adding the kill-test review, BIST/delay-line test structures, thermal forcing and $150/h hours.
- **T2 reference.** R17: qualification line $0.4M → $1.0M.
- **New sensitivity cases:** no free release, close ×0.5, licences removed, sky130 slip of 6 months, academic share 0.80, and the combined upside.
- **Check:** with the old inputs swapped back, the same code reproduces every Phase 4 number exactly (output §0).

**Plan:**
- **T2 (C-32 gain cell, C-22 ReRAM chiplet) is killed.** STTR, seed and cofounder rows are removed. §11 #10–11 are now revival conditions.
- **The licence is restated:** nominal lot measured, corners simulated, yield on ≥50 die, warranty limited to re-delivery or a refund of fees, and no radiation data.
- **The supply-security axis is limited to U.S.-fab sky130.** GF180MCU is fabbed in Singapore.
- **Kill test (§10) is stronger**, at ~$9.1k:
  - (i) counts only distinct funded teams;
  - (ii) needs 2 open-PDK commercial/SBIR LOIs of $10k or more;
  - (iii) needs a signed extracted-SPICE corner and Monte Carlo pass;
  - (iv) needs written no-release statements from UCSC VLSIDA and OCD, and silence fails.
- **Kill criteria (§11) are re-set** near half the revised model. Two are new: an exclusive contractor or technical cofounder by m3, and a university-PO gate at m6. A third rule removes the Synopsys–GF pilot's 40 projects from the market if it already gives members free memory IP.
- **Sections 0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11 and 12 are updated** and marked "(revised after red team)".

### 14.3 Revised headline economics (re-run model, 2026-11-01)

| | BASE | GLUT | SEVERE | Phase 4 BASE |
|---|---|---|---|---|
| Recurring ARR m18 | **$41.2k** | $36.8k | $34.3k | $66.6k |
| Recurring ARR m36 | **$65.7k** | $54.9k | $49.3k | $157.6k |
| Run-rate m36 (incl. services) | $164.1k | $137.9k | $123.9k | $423.9k |
| Cash-flow breakeven, founder unpaid (first of 3 positive months) | **m12** (Nov-2027) | m12 | m12 | m8 |
| Founder-paid breakeven (GP ≥ $11.85k/mo) | **never** (peak $8.0k) | never | never | m18 |
| **Founder full-time** | **never** | never | never | m20 |
| Cash low (from $40k, gated) | $4.0k at m15 | $2.8k at m15 | $3.6k at m18 | $20.4k at m7 |
| 36-month revenue / gross margin | $316.9k / 57% | $278.6k / 55% | $256.5k / 53% | $713.9k / 66% |
| End cash m36 | $88.4k | $60.4k | $45.1k | $219.3k |

Only the combined upside case (price ×1.3, close ×1.3, no free release) pays the founder, at m22. A full free release cuts BASE ARR at m36 to $34.0k.

### 14.4 Revised verdicts

| Question | Revised verdict |
|---|---|
| **POSSIBLE?** | **Yes at simulation level** for the C-33 wedge: a 1 KB sky130 macro is silicon-verified (TRL 6), while 16 KB+ is unproven and gated on signed extracted-SPICE corners and Monte Carlo. An MPW delivers "nominal lot measured, corners simulated", not "measured PVT corners". **No for T2 on this PDK.** |
| **PROFITABLE?** | **No as a job; marginal as a side line.** 57% GM and cash-positive from m12 with the founder unpaid. ARR is $41.2k at m18 and $65.7k at m36, and the founder is never paid in BASE, GLUT or SEVERE. |
| **DOABLE BY THIS FOUNDER?** | **Yes, part-time, for the wedge**, but only with an exclusive contract memory engineer or a technical cofounder signed by m3. **No for T2 (killed).** |

### 14.5 FINAL STATUS: **DOWNGRADED**

**Reason:** the red team killed both T2 legs. Neither has a named buyer, a gain cell has no density or leakage case on sky130, and ReRAM's magnet axis is shared by OTP, eFuse and S130 eNVM. The C-33 wedge survives only as a part-time **side line**. On revised inputs it never pays the founder within 36 months, so it is withdrawn as a FALLBACK candidate. It is not KILLED because it needs no outside capital, is cash-positive from m12 with a gated cash low of $4.0k, and a ~$9.1k day-30 test decides it.

**Role for Phase 6:** side line only. Not PRIMARY, not FALLBACK, not MOONSHOT. EV for this founder is about +$5–15k over three years, before the founder's time, at an estimated 15–25% pass probability on the strengthened kill test [ESTIMATE].
