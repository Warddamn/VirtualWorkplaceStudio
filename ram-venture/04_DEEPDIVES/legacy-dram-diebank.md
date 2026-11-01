# DD7 — Authorized-Aftermarket Legacy DRAM Die Bank (+ hi-rel MCMs) (`legacy-dram-diebank`)

Author: `p4w-legacy-dram-diebank` · Red-team owner: `p5r-legacy-dram-diebank` · As of 2026-11-01 · **Round 2 · FINAL STATUS: KILLED (§14)** · Model: `models/legacy-dram-diebank.py` (re-run 2026-11-01 with the RED-TEAM REVISIONS (Phase 5) block, exit 0; output `research/phase4/legacy-dram-diebank_model_output.md`; responses `research/phase5/responses_legacy-dram-diebank.json`) · Notes: `research/phase4/legacy-dram-diebank_notes.md` · Assumptions: `research/assumptions/p4-legacy-dram-diebank.md`, `research/assumptions/p4w-legacy-dram-diebank.md`.

Web facts are search-snippet grade (every WebFetch failed), so the best tag they carry is **[REPORTED]**; the DFARS text, opened by Phase-2 agent E, is the exception. Model figures are **[ESTIMATE]**. Model m1 = 2026-11, so m15 = 2028-01 (glut start, A-05), m18 = 2028-04, m36 = 2029-10.

---

## 0. Header

**Pitch.** Become the authorized "last source" for legacy DRAM after the big makers stop making it: buy the last wafers of an end-of-life (EOL) DDR3/DDR4/LPDDR4 chip, store the die in nitrogen for 10–20 years, and package and test them on demand for defense, avionics, rail and medical programs that cannot change their memory. Use the same die supply to build rugged 8 GB x72 ECC DDR4 multi-chip modules (MCMs) for NewSpace and rugged-industrial computers.

**This is a ROUND-2 deep dive.** It was added after round 1's red team (`05_REDTEAM.md`) killed DD1, DD3 and DD4 and downgraded DD2 and DD5, refuting none of 127 objections. That left no PRIMARY-grade venture and no MOONSHOT candidate. DD7 was selected as the MOONSHOT candidate, which has no time-to-revenue limit (`03_SCORING.md` §9). The selection cited three reasons: a "Rochester-scale" ceiling, moat 4 and glut-proof lifecycle demand. DD7 runs alongside DD6 (the PRIMARY candidate). **This deep dive finds all three reasons overstated (§2, §5, §12).** **The round-2 red team (27 objections: 3 FATAL, 12 MAJOR, 12 MINOR; none refuted) then killed L1, L3 and Plan C and confirmed that the moat cannot be obtained. DD7 is KILLED (§14) (revised after red team).**

**Anchor and folded concepts**

| Role | ID | Concept | Why it is here (scorer quotes from `research/phase3/scores_raw/*.json`) |
|---|---|---|---|
| Anchor | C-91 | Authorized-aftermarket die bank for EOL legacy DRAM (title-taking last-time-buy aggregator) | It is the only scored concept with a moat score of 4 (`03_SCORING.md` §5): DFARS ranks authorized aftermarket manufacturers ahead of every independent. VC: "Rochester's business with none of Rochester's assets: the DFARS moat is real, but OCMs authorize the firm that has >10B banked die and 70+ OCM ties." |
| Folded | C-65 | U.S. hi-rel DDR4/LPDDR4 MCM design house | It uses the same die (Winbond and ESMT known-good die, KGD) and the same U.S. assembly houses. It is also the one product where qualification *locks* a die, so a premium survives. The model shows that it, not the bank, carries any venture-scale outcome (§2.3). Veteran: "a product line for Micross, not a venture for this founder." |

**Capital tier: T2 (revised after red team).** The staged venture (Plan B) now needs **$11.49M** of outside capital in BASE, $11.64M in GLUT and $11.77M in SEVERE (model §6; Phase 4: $8.11M / $8.50M / $9.08M). The higher figures come from the stacked MCM build, the 125 °C yield loss, per-lot requalification and the QML-38534 line cost. Nothing in this concept remains at T0. The Phase 4 T0 wedge (managed die-bank programs plus rep commissions on the founder's $40k) lost its program line, L1, to the red team. The leftover rep line (L2) reaches $8.6k of recurring ARR at m36 and falls below the $20k cash floor at m22 (model §10j).

**Scores and ranks** (`scores.csv`; consensus of three scorers; out of 100; rank among 40 scored concepts in parentheses)

| ID | Tier | Default | Capital-constrained | Moonshot | Moat / competition / cycle / founder (1–5) |
|---|---|---|---|---|---|
| C-91 | T2 | 57.0 (28) | 53.3 (30) | 59.2 (23) | 4 / 1 / 3 / 1 |
| C-65 | T2 | 57.0 (30) | 53.3 (31) | 57.5 (25) | 3 / 1 / 4 / 1 |

All three scorers gave both concepts the floor score (1) on competition and on founder fit. Doubling moat and margin lifts C-91 only from #28 to #23.

**Three verdicts (revised after red team; the Phase 4 verdicts are kept in §14.5)**

- **POSSIBLE? Only for incumbents (revised after red team).**
  - Rochester, Micross and Teledyne e2v, Mercury and Frontgrade prove each business at scale (§5). For an entrant, every leg fails a physics or qualification test.
  - **Storage.** 10–20-year storage of bare DRAM die is **TRL 6–7, not 9**. No published bond-pull or yield data exist past ~3 years, and Infineon's own limit is 36 months for unsawn wafers (RT-PHY-DD7-03).
  - **MCM fit.** The 8 GB x72 MCM as described **does not fit** 15×20 mm. Nine die are 405–675 mm² of silicon, so the part needs die stacking with a whole-wafer redistribution layer (RDL) (RT-PHY-DD7-01).
  - **125 °C.** JEDEC specifies no DDR4 refresh above 95 °C. A 125 °C part needs a hot-retention bin on every die and a 23–72% refresh tax (RT-PHY-DD7-02).
  - **Locked parts.** On DO-254 and FDA-locked boards the qualified item is the *packaged* part. An unauthorized re-packaged die is a new part number, so it cannot serve that lock (RT-VET-DD7-02).
- **PROFITABLE? No (revised after red team).**
  - **L1.** One managed program costs the OEM **$186k–347k to manage ~$52k of die**, 2.9–5.4× a packaged last-time buy plus dry storage (model §10b).
  - **L3.** With the full pull-cost stack, the bank bought at m20 in BASE has **unit GM −12.8% and IRR −26.6%**, and **no bank is bought in any scenario**. IRR break-even needs ≤$1.53/die all-in (model §10d).
  - **Plan B.** It returns **0.29× of $11.49M** (0.24× GLUT, 0.19× SEVERE). Year-10 EBITDA is −$1.10M, and MCM GM is 18.7/26.7/38.2% at m1/m36/m60. BULL reaches 7.2×, ~22% a year gross over 10 years before dilution (model §10g).
- **DOABLE BY THIS FOUNDER? No (revised after red team).**
  - **L1** has no rational buyer.
  - **DoD study work** needs NIST SP 800-171 (~$35k + $500/month), and **defense-OEM agency** needs AS9120B (~$35k). Each breaks the $20k cash floor by m6 (model §10c).
  - **Bank and MCM** need OCM authorization, a hi-rel co-founder and ~$11.5M.
  - **Founder hours.** On DD6's revised (Phase 5) model, DD6 never goes full-time even at 65 h/month, and every 10 h/month diverted to DD7 cuts DD6's m36 ARR from $63.9k to $56.2k (20 h/month: $45.3k) (model §10h). On DD6's Phase 4 inputs, 10 h/month moved its full-time switch from m23 to m33, and 20 h/month meant never [ESTIMATE: DD6 `run_with(P_PHASE4)`; `responses_legacy-dram-diebank.json` RT-VC-DD7-03].
  - **Residual rep line.** It reaches $5.0k ARR at m18 and $8.6k at m36 in BASE ($4.4k GLUT, $928 SEVERE). It never breaks even and needs an employer carve-out.

**Recommendation (revised after red team): DROP. FINAL STATUS: KILLED (§14).** Do not fill any slot with DD7, and do not keep it as a DD2 SKU (RT-VET-DD7-01). **Do not run the 29-day kill test**: that saves ~$6k and ~50 founder hours that DD6, then round 2's PRIMARY candidate, needed (RT-VC-DD7-03; DD6 was later killed too, and the Phase 6 PRIMARY is DD2). Two things remain, both at $0:
- one paragraph of packaged-part dry-storage advice inside DD2's LTB study;
- a passive reopen watch (§10, §11). Reopen C-91 only on a written OCM offer of authorized-aftermarket rights for a named EOL DRAM part. Reopen C-65 only if a hi-rel co-founder brings an existing x72 design-in plus ≥3 evaluation LOIs at ≥$1,200.

*Phase 4 recommendation, kept for the record:* "not a MOONSHOT. Status going into the round-2 red team: SIDE LINE … keep the founder-doable piece (managed die-bank programs on a Micross-type consignment vault) only as an optional SKU of DD2's LTB study line, and run the 29-day kill test (§10) only alongside DD2."

---

## 1. How it works

**Chips die before the products that use them.** Micron sent DDR4/LPDDR4 EOL notices to PC and data-center customers in June 2025 ([TrendForce, 2025-06-13](https://www.trendforce.com/news/2025/06/13/news-micron-confirms-ddr4-phase-out-with-eol-notices-reportedly-hints-at-price-hikes-ahead/)). One notice set a last order date of 2026-03-30 for an LPDDR4 8Gb part and warned that replacements may not be drop-in ([Mouser PCN 36146](https://www.mouser.com/PCN/Micron_Technology_PCN_36146.pdf)). Samsung stopped DDR3 in Q2 2024 ([GlobX](https://globx.eu/blog/supply-chain-insight/ddr3-last-time-buy-2026)) [all REPORTED]. A Navy radar processor or a rail-signal controller may stay in service for 20 years [ESTIMATE: illustrative]. When its memory chip is discontinued, the owner can swap in an equivalent chip, buy a lifetime supply before the last order date (a "last-time buy", LTB), or redesign the board.

**Most DRAM owners simply swap.** DRAM follows JEDEC standards, so another maker's DDR4 8Gb usually fits. In DoD's 2024 obsolescence case mix, **2,809 cases were resolved by a simple substitute, 1,268 by a life-of-need buy and only 24 by a complex substitute; 99.3% needed no redesign** ([DSPO, 2024-08-08](https://www.dsp.dla.mil/Portals/26/Documents/Conference/2024%20Briefings/Day%203%20-%20August%208/Brown%20-%20Program%20Update.pdf)) [REPORTED]. This single fact shapes the whole venture.

**A minority cannot swap: the die is "locked".** That happens when the chip sits inside a qualified hi-rel module, on a DO-254 avionics board, or in an FDA-validated device where any change triggers re-qualification [ESTIMATE: notes §0 finding 1]. Those buyers pay a premium. Authorized aftermarket parts are estimated at **1.5–5× the original price** (`01_LANDSCAPE.md` §7.3, itself an estimate) [ESTIMATE].

> **Correction (revised after red team, RT-VET-DD7-02).** On a DO-254 board or in an FDA-validated device, the qualified item is the *packaged* part number: package, substrate, mold compound, wire, MSL rating, marking and the OCM's final test. A banked die re-packaged at a U.S. OSAT is therefore a different part. It triggers the delta qualification the buyer wanted to avoid, unless the maker holds OCM-transferred package designs and test programs, which come only with authorization. Unauthorized die banking can serve only hybrids and MCMs, and their makers (Teledyne, Mercury, Frontgrade, Micross) run their own banks.

**Who is allowed to sell to DoD.** DFARS 252.246-7008 and 246.870-2 tell defense contractors to buy from the original manufacturer, its authorized distributors or "authorized aftermarket manufacturers" before anyone else. Only then may they buy from independents, and the contractor then carries the testing and liability ([DFARS 252.246-7008](https://github.com/GSA/GSA-Acquisition-DFARS/blob/master/dita/252.246-7008.dita); [246.870-2](https://github.com/GSA/GSA-Acquisition-DFARS/blob/master/dita/246.870-2.dita)) [VERIFIED by Phase-2 agent E]. An authorized aftermarket manufacturer holds the OCM's permission to keep making or selling a part after the OCM stops, using transferred wafers, tooling or test data ([ERAI](https://www.erai.com/glossary/Authorized%20Aftermarket%20Manufacturer/)) [REPORTED]. **That permission is the moat, and only an OCM can grant it.**

**The die bank.**
- **Buy and store.** At EOL, buy finished wafers (cheaper per die than packaged chips) and keep them **unsawn** in nitrogen. An unpowered die suffers none of the wear-out mechanisms that need voltage and current; the risks are bond-pad oxidation, moisture and handling [ESTIMATE: notes §5]. Infineon's own limit is 36 months for unsawn wafers in nitrogen ([Infineon](https://www.infineon.com/dgdl/Storage_of_Products_Supplied_by_Infineon_Technologie.pdf)); Micross claims 20+ years ([Micross](https://www.micross.com/sustainment-solutions/program-sustainment-management/long-term-die-and-wafer-storage)); a Rochester study found packaged parts still worked after up to 17 years ([DigiKey](https://www.digikey.com/en/blog/testing-confirms-that-component-reliability-remains-with-proper-long-term-storage)) [REPORTED].
- **Pull.** On an order, re-probe the wafer, saw it, package the die, run at-speed tests and ship. The often-missed risk is the *test program*: legacy DDR3/DDR4 programs live on ageing memory testers, hence $120k of set-up per part family (model §1, `bank_nre_first`).

**The MCM.** Put nine 8Gb x8 DRAM die on one small substrate: eight give 8 GB and the ninth stores error-correction bits ("x72 ECC"). Seal it in a 15–20 mm ball-grid package, burn it in and screen it across −55 to 125 °C, and a defense or space computer gets its whole memory in one part. Teledyne e2v has sold this kind of part since 2020: first a 4 GB x72 version, the DDR4T04G72 ([Signal Integrity Journal, 2020-05](https://signalintegrityjournal.com/articles/1749-radiation-tolerant-ddr4-memory-chip-ddr4t04g72m)). Avnet now also lists an 8 GB DDR4T08G72 ([Avnet](https://www.avnet.com/americas/manufacturers/m/c/teledyne-e2v/memory)) [REPORTED].

> **Correction (revised after red team, RT-PHY-DD7-01/-02/-05, RT-VET-DD7-04/-06).**
> - **Fit.** Nine 8Gb die are 405 mm² (45 mm² big-three die) to 675 mm² (75 mm² legacy-OCM die) of silicon, more than a 15×20 mm (300 mm²) package. Teledyne's DDR4T04G72 fits 4 GB *and* 8 GB in 15×20×1.92 mm, 391 balls, on Micron die ([GDM, 2020-05-26](https://www.gdm.or.jp/pressrelease/2020/0526/349733)) [REPORTED]. That implies stacking or 16Gb die. A stacked build needs whole-wafer RDL, which distributor KGD cannot provide.
> - **125 °C.** JEDEC DDR4 refresh is defined only to 95 °C, at 3.9 µs ([SK hynix datasheet](https://html.alldatasheet.net/html-pdf/533530/HYNIX/HMT312S6DFR6A-H9/1644/10/HMT312S6DFR6A-H9.html)) [REPORTED]. A 125 °C grade needs a per-die hot-retention bin and a stated refresh derate.
> - **Qualification standard.** A QML part of this kind is a MIL-PRF-38534 hybrid, not a MIL-PRF-38535 monolithic part.
> - **Revised cost.** Revised unit cost is $731/$660/$557 (m1/m36/m60), and GM is 18.7/26.7/38.2% (model §3, §10e).

**The four business lines and three plans the model tests**

```
 L1 MANAGED PROGRAM  OEM owns its LTB die in a Micross-type N2 vault; founder manages it
 L2 REP AGREEMENT    5% commission selling long-lifecycle DRAM (Intelligent Memory, Alliance...)
 L3 TITLE-TAKING BANK  needs OCM authorization + capital: 10 wafers -> vault -> re-probe,
                       package, test at a U.S. OSAT -> sold at 2.5x the part's EOL price
 L4 x72 ECC MCM      9 KGD + substrate + assembly + screening -> NewSpace/rugged design-ins

 Plan A = L1 + L2, part-time on $40k.   Plan B = A + L3 (m20) + L4 (NRE from m30) on $1.5M (m18)
 + $4.0M (m30) + bridges.   Plan C = buy a ~30-person licensed manufacturer with SBA debt.
```

*(Diagram shows the Phase 4 inputs. Revised after red team: the L3 bank is 17 wafers × 736 good die sold at 2.0×; L1, L3 and Plan C are killed (§14).)*

---

## 2. Cost and unit-economics model

> **Revised after red team (model re-run 2026-11-01 with the RED-TEAM REVISIONS (Phase 5) block; the Phase 4 figures below are reproduced exactly in model §10a and kept for the record).** Model §10a, §10d, §10e and §10g print the Phase 4 headline figures. The other Phase 4 table cells come from running the same model on `INPUTS_P4`; the Phase 7 gate re-ran it on 2026-11-01 and every cell matched [ESTIMATE: Phase 4 re-run, not printed in the current output]. Each line's revised standing:
>
> | Line | Phase 4 | Revised | Driver (objection) |
> |---|---|---|---|
> | L1 managed program | $770/month GP; ~$34k of BASE m36 ARR | **KILLED.** The OEM pays $186k–347k to manage ~$52k of die (2.9–5.4× a packaged LTB) | RT-HYP/VC/VET-DD7-01, RT-VC-DD7-02 |
> | L2 rep commission | $8.6k of BASE m36 ARR | $8.6k BASE / $4.4k GLUT / $928 SEVERE. Never breaks even at $680/month fixed cost; ~$2.2k probability-weighted | RT-VC-DD7-08 |
> | L3 bank (m20, BASE) | unit GM 39.6%, IRR 2.6% | **KILLED.** Unit GM −12.8%, IRR −26.6%, 0.10× cash. No bank is bought in any scenario; IRR break-even needs ≤$1.53/die all-in pull cost | RT-VET-DD7-03, RT-PHY-DD7-03/-04, RT-HYP-DD7-04 |
> | L4 MCM | unit cost $490→$344; GM 45.6–61.8%; NRE $1.4M | Unit cost $731→$557; **GM 18.7–38.2%**; NRE $1.6M + $75k/yr lot requalification | RT-PHY-DD7-01/-02, RT-VET-DD7-04/-06 |
> | Plan B (10-year) | 0.46× of $8.11M | **0.29× of $11.49M** (GLUT 0.24×, SEVERE 0.19×); year-10 EBITDA −$1.10M | all of the above |
> | Plan C | DSCR 1.50 / 0.85 / 0.45 | **KILLED.** Not executable by this founder | RT-VC-DD7-07 |

All figures come from `python3 models/legacy-dram-diebank.py` (BASE unless stated). The legacy DDR4 price starts at the DDR5 contract deck of **$20.37/GB** (`models/dram_cost_stack.py`, imported). It then follows three paths (model §2):
- **BASE:** −35% over 2028 to $13.24/GB.
- **GLUT:** $8.15/GB by m17.
- **SEVERE:** $2.04/GB by m20.

All three converge on a long-run **$3.00/GB by m60** [ESTIMATE: ~2.3× the 2023 DDR4 trough; the most consequential judgment in the 10-year view].

### 2.1 Unit economics per line (model §3)

*Revised after red team:* L1 is killed. The L3 pull cost is now $1.50 + $6.00 + $4.00 + **$10.00 burn-in and hot/cold test** = $21.50 per die. At 0.90 pull yield that is **$23.89 per good die before the die itself**, plus $5k/yr of surveillance per bank. The aftermarket multiple is 2.0×, and the bank is 17 wafers × 736 good die (75 mm² die). The L4 build is a stacked/RDL part: $90 substrate, $160 assembly, 0.76 module yield, $1.6M NRE plus $75k a year of lot requalification. Revised MCM unit cost is $731 (m1) to $557 (m60), and GM is 18.7–38.2%. One design-in now earns $824k of gross profit, so ~1.9 design-ins repay the NRE (model §3). The Phase 4 table follows unchanged.

| Line | Price | Unit result | Key inputs and basis |
|---|---|---|---|
| L1 managed program | $4,000 LTB study + $750/month + 4% agency fee on die value + $1/unit pull margin | **$770/month gross profit**; ~100-month life; **$79.1k lifetime gross profit** + $11.4k study revenue per program won | 10% of qualified conversations buy a study, 35% of studies become programs, so **28.6 conversations (~136 founder hours) per program** [ESTIMATE; Micross sells the vault direct] |
| L2 rep commission | 5% of ~$40k/yr of long-lifecycle DRAM per account | **$2,000/yr per account** at 2026 prices; **$295/yr** at the $3/GB long-run price | Commission rate unsourced [ESTIMATE] |
| L3 bank (10 × 300 mm DDR4 8Gb wafers = 12,510 good die) | 2.5× the packaged part price at purchase | Unit GM 39.6% if bought in BASE at m20 (below) | Die = 0.75 × packaged $/GB; pull = $1.50 re-probe + $6.00 package + $4.00 test at 95% yield = **$12.11 per good die before the die itself**; $120k first-family set-up [ESTIMATE: no quote exists; §10 track C] |
| L4 x72 MCM | $900 ASP (low end of the C-65 card's $800–3,000) | Unit cost **$490** (2026 die) to **$344** (long-run die); GM **45.6–61.8%** | 9 KGD at 0.85 × packaged $/GB + $60 substrate + $80 assembly + $150 screening, ÷ 91% module yield; **$1.4M NRE** over 18 months [ESTIMATE] |

### 2.2 The bank loses unless it is bought high and sold scarce (model §3)

*Revised after red team (model §3, §10d):* with the full pull-cost stack the bank loses money at every purchase date:
- **Bought m20:** BASE unit GM −12.8% (IRR −26.6%); GLUT −109.2% (IRR −99.4%); SEVERE −685.1%.
- **Bought at the 2026 peak:** unit GM −0.3% (IRR −16.5%).
- **Bought at the long-run price:** unit GM −339.8%.
- **Break-even pull cost (Phase 4 inputs):** IRR reaches 0 at $14.48/die all-in, so the old C1 pass line of $15 would have passed a losing bank.
- **Break-even pull cost (revised inputs):** unit GM reaches 0 at $17.64/die and IRR reaches 0 at $1.53/die.

The Phase 4 table follows unchanged.

| Bought at | $/GB at buy | Outlay | Sale/unit | Cost/unit | Unit GM | 10-yr IRR | Cash multiple |
|---|---|---|---|---|---|---|---|
| BASE m20 (2028-06) | 16.80 | $277.7k | $42.01 | $25.37 | **39.6%** | **2.6%** | 1.13× |
| GLUT m20 | 8.15 | $196.4k | $18.33 | $18.54 | **−1.1%** | **−32.8%** | 0.07× |
| SEVERE m20 | 2.04 | $139.1k | $4.07 | $13.71 | −236.6% | n/a | −0.68× |
| 2026 peak (m1), BASE sell-through | 20.37 | — | $50.92 | $28.18 | 44.6% | 6.5% | — |
| Long-run (m60) | 3.00 | — | $7.50 | $14.47 | −93.0% | n/a | — |
| m60 at Rochester-scale $2/die pull, incl. $120k set-up | 3.00 | — | $7.50 | $4.47 | 40.4% | −26.3% | — |

**Why it fails.** The U.S. pull cost (~$11.50 per die) does not fall with DRAM prices, but the sale price is anchored to the part's EOL price. To break even the bank must sell at **1.5× the EOL price if bought at m20 in BASE, 2.3× if bought in GLUT and 4.8× if bought at the long-run price** [ESTIMATE: model §3 cost/unit ÷ $/GB]. So the C-91 card's "a glut cheapens LTB wafers" is backwards at startup scale. **Scale is the real moat:** at a Rochester-scale pull cost unit GM recovers to 40%, but a 10-wafer bank still cannot repay its set-up cost.

### 2.3 The MCM carries any venture outcome (model §3 and §6 grid)

*Revised after red team (model §6, §10g).* Revised grid, EV/capital at 1.5× year-10 revenue:

| Design-ins per year | 300 units/yr | 600 units/yr | 1,000 units/yr |
|---|---|---|---|
| 2 | **0.29×** [$2.18M] | 0.61× [$4.36M] | 1.12× [$7.26M] |
| 4 | 0.61× [$4.36M] | 1.42× [$8.71M] | **2.73×** [$14.50M] |
| 6 | 0.98× [$6.53M] | 2.40× [$13.05M] | 4.38× [$21.75M] |

The "4 × 1,000" venture case no longer clears 3×. BULL is 7.22× (Phase 4: 7.31×), which is ~22% a year gross over 10 years before dilution (RT-VC-DD7-06). The Phase 4 analysis follows unchanged.

One design-in of 300 units a year for 8 years earns $1.33M of gross profit at long-run die prices. That is about one design-in to repay the $1.4M NRE. The question is how many design-ins a no-heritage entrant wins. EV/capital at 1.5× year-10 revenue, BASE prices, $900 ASP:

| Design-ins per year | 300 units/yr each | 600 units/yr each | 1,000 units/yr each |
|---|---|---|---|
| 2 (the model's case) | **0.46×** [$2.49M] | 1.08× [$4.66M] | 1.97× [$7.56M] |
| 4 | 1.08× [$4.66M] | 2.42× [$9.01M] | **4.04×** [$14.81M] |
| 6 | 1.75× [$6.84M] | 3.64× [$13.36M] | 6.01× [$22.05M] |

The BULL what-if (4 design-ins a year of 1,000 units at $1,500, the first at m54; aftermarket 4.0×) reaches **$26.8M** of year-10 revenue, **$13.9M** EBITDA and **7.3×** on $5.5M (model §6). That is the moonshot, and it requires a no-heritage entrant to out-sell Teledyne, Mercury and Frontgrade on volume and price.

### 2.4 Plan A, the bootstrap wedge (model §4)

*Revised after red team (model §4, §10j): with L1 killed, the residual Plan A is L2 rep commissions only.*

| Scenario | Recurring ARR m12 | m18 | m24 | m36 | Founder paid? | Breakeven | Cash low | Cash below the $20k floor |
|---|---|---|---|---|---|---|---|---|
| BASE | $2.3k | **$5.0k** | $6.1k | **$8.6k** | never | never | $15.4k (m36) | m22 |
| GLUT | $2.3k | $2.0k | $2.9k | $4.4k | never | never | $10.2k (m36) | m22 |
| SEVERE | $2.3k | $1.9k | $0.6k | $0.9k | never | never | $7.0k (m36) | m22 |

The month-1 one-off is now $3,900: the kill test is withdrawn, and $500 of employer review is added. A lean set-up at $300/month with no conference breaks even (founder unpaid) at m15 in BASE, with a $32.3k cash low, but earns only ~$8.6k a year. The Phase 4 table follows unchanged.

| Scenario | Recurring ARR m12 | m18 | m24 | m36 | Founder paid? | Cash low | Cash m36 | Cumulative revenue m36 |
|---|---|---|---|---|---|---|---|---|
| BASE | $12.6k | $22.0k | $29.5k | **$42.6k** | **never** | $30.2k (m3) | $90.2k | $129.0k |
| GLUT | $12.6k | $18.1k | $23.6k | $33.5k | never | $30.2k (m3) | $77.4k | $107.7k |
| SEVERE | $12.6k | $17.4k | $19.7k | $26.4k | never | $30.2k (m3) | $69.3k | $93.6k |

The BASE m36 mix is 3.8 managed programs and 6.6 rep accounts (commissions $8.6k of the $42.6k). "Breakeven" at m3 means little because the founder is unpaid. Month 1 carries a one-off $8,500: the $6,000 kill test plus $2,500 of LLC and rep legal.

### 2.5 Plan B (staged venture) and Plan C (acquisition)

*Revised after red team (model §5, §6, §10g):*

| Plan B, revised | Recurring ARR m36 | Year-10 revenue | Year-10 EBITDA | Total outside capital (bridges) | EV/capital |
|---|---|---|---|---|---|
| BASE | $17.8k | $2.18M | −$1.10M | **$11.49M** ($5.99M) | **0.29×** |
| GLUT | $8.9k | $1.86M | −$1.16M | $11.64M ($6.14M) | 0.24× |
| SEVERE | $1.8k | $1.53M | −$1.22M | $11.77M ($6.27M) | 0.19× |

No bank is bought in any scenario. Plan C is **killed**: it needs a full-time founder, a personal guarantee on ~$3.6M of SBA debt, $410k of outside equity and an unnamed target (RT-VC-DD7-07). The Phase 4 table follows unchanged.

| Plan B | Recurring ARR m36 | Outside capital by m36 | Year-10 revenue | Year-10 EBITDA | Total outside capital (of which bridges) | EV/capital |
|---|---|---|---|---|---|---|
| BASE | $81.4k | $5.50M | **$2.49M** | −$276k | **$8.11M** ($2.61M) | **0.46×** |
| GLUT | $61.4k | $5.50M | $2.06M | −$460k | $8.50M ($3.00M) | 0.36× |
| SEVERE | $46.1k | $5.50M | $1.69M | −$635k | $9.08M ($3.58M) | 0.28× |

- The bank and the MCM book **no revenue before m36**, and there is no post-raise breakeven inside 36 months.
- GLUT and SEVERE **buy no bank at all**: none passes the model's rule that projected unit GM at purchase must be ≥20%. On Phase 4 inputs BASE buys one at m20 and skips m44 and m68 (model §10g, "banks bought"; on revised inputs no scenario buys one, model §5).
- **Plan C** buys a Resurgent-type licensed manufacturer (~30 staff, $6.0M revenue) for $4.5M with a $3.6M SBA loan ($598.5k/yr debt service), $410k of outside equity and a full-time founder. **Debt-service coverage (DSCR) is 1.50 BASE, 0.85 GLUT, 0.45 SEVERE** (model §7); lenders want ~1.25 [ESTIMATE].

### 2.6 Sensitivity (±30%, model §8)

*Revised after red team (model §8):*
- **Residual Plan A m36 ARR (base $8.6k):** price ±30% gives $6.0k–$11.2k; conversion has no effect (L1 is off); churn gives $9.1k–$8.1k.
- **Plan B EV/capital (base 0.29×):** price gives 0.18–0.42×; conversion 0.20–0.38×; COGS 0.32–0.26×.
- **Revised bank IRR:** the aftermarket multiple at ±30% moves IRR between −83.2% and −11.2%.
- **Conclusion:** no ±30% knob makes any line profitable. The Phase 4 table follows unchanged.

| Output | Price | Conversion | Churn | COGS |
|---|---|---|---|---|
| Plan A m36 ARR (base $42.6k) | $29.8k–$55.4k | $32.4k–$52.8k | $44.8k–$40.6k | unchanged |
| Plan B EV/capital (base 0.46×) | 0.29–0.70× | 0.31–0.62× | 0.49–0.43× | 0.52–0.42× |

Bank IRR is most sensitive to the aftermarket multiple (−9.6% to +11.7%), then sell-through (−4.7% to +3.8%). **No ±30% knob makes the Plan A founder full-time, or takes Plan B above 1× capital.**

### 2.7 What must be true (model §9)

*Revised after red team:* conditions (1) and (2) were never tested by the Phase 4 kill test (RT-HYP-DD7-05, RT-VC-DD7-04, RT-VET-DD7-05). The evidence says (1) is unlikely: the OCMs that would talk are extending their lines, and Micron has placed EOL continuity with established houses. (2) cannot be served by an unauthorized die bank at all (RT-VET-DD7-02). (3) is now ≤$17.64/die for unit GM 0 and ≤$1.53/die for IRR 0. (4) clears only 2.73× even at 4 × 1,000. (5) is now ~$11.5M. The Phase 4 list follows for the record.

1. A DRAM OCM (Winbond, ESMT, Etron, Nanya, Alliance or Intelligent Memory) signs an authorized aftermarket or distribution agreement with a new entity by m15.
2. At least 3 programs show **locked-die** demand at ≥2.5× the EOL price.
3. U.S. re-probe, package and test costs ≤ ~$12 per die, and banks are bought only while the EOL price is high.
4. The MCM wins ~4 design-ins a year of ~1,000 units each against Teledyne e2v, Mercury and Frontgrade heritage.
5. ~$8M of outside capital arrives on those gates, with a full-time founder from Stage 1.

**Fail (1) or (2) and DD7 collapses into DD2's LTB-service side line.**

---

## 3. Target customer and first ten customers

**Buyers.** L1: the obsolescence (DMSMS) manager or component engineer at a mid-size U.S. defense, rugged-computing or industrial OEM facing a DDR3/DDR4 LTB before end-2027, with no vault of its own. L3: DoD sustainment buyers who must buy authorized parts. L4: NewSpace avionics and rugged system-on-module makers, for whom Teledyne e2v's space-grade pricing overshoots (C-65 card).

**Demand is real but mostly substitutable.** EOL rates hit records in 2025, and 2026 is likely to match ([Z2Data, 2026](https://www.z2data.com/insights/how-chip-obsolescence-is-making-dmsms-worseand-where-we-re-headed-in-2027)). Advantech set a DDR3 module LTB for 2026-11-30 ([Advantech](https://www.advantech.com/en-us/resources/news/【phase-out】selected-d3-dram-module-part-numbers-and-ddr3-dram-module-eol)) [REPORTED]. The sanity ceiling for DoD-tracked memory life-of-need demand is **$6.3–25.4M a year** (~10% of DSPO cases at $50–200k each; model §6) [ESTIMATE]. **Revised after red team (RT-HYP-DD7-07, RT-VC-DD7-05):** this is part value with an unsourced 10% memory share, not die-bank demand and not the founder's fee pool. As a fee pool it is ≤$1.14M of new program ARR a year at 100% national share, and $34–57k a year at a 3–5% share (model §10i). With L1 killed, none of it is addressable here. Customers #1–3 also need NIST SP 800-171 (RT-HYP-DD7-02), and #6–#8 need AS9120B (RT-HYP-DD7-03).

**None of the ten below has been contacted. Each is a hypothesis for §10 track B.**

| # | Customer | Type | Trigger / evidence | Line | How to reach |
|---|---|---|---|---|---|
| 1 | NAVSUP Weapon Systems Support | Navy DMSMS buyer | DMSMS health-assessment requirement, responses due 2026-06-18 ([Cleat](https://www.cleat.ai/government/contracts/dmsms-and-obsolescence-management-reporting-sqml)) | L1, as subcontractor | Find the awardee on SAM.gov; offer LTB sizing and die-bank planning |
| 2 | Tobyhanna Army Depot (PA) | Army depot | Obsolete-microelectronics subcontract, responses due 2026-08-07 ([Cleat](https://www.cleat.ai/government/contracts/dmsms-mitigation-and-reverse-engineering-gbao)) | L1 | Via the prime; drivable from the East Coast |
| 3 | NAWC China Lake | Navy test center | Sole-source memory upgrade, SPE7M5-26-T-400W, FSC 5962 ([Cleat](https://www.cleat.ai/government/contracts/memory-upgrade-so4p)) | L1 / L3 | Track FSC 5962 memory buys; demand evidence only, as this one is placed |
| 4 | DLA Land and Maritime | Supply-chain buyer | Recurring memory microcircuit solicitations (notes §7) | L3, after authorization | Unreachable without an OCM letter |
| 5 | NSWC Crane | DMSMS / SD-18 hub | Publishes DMSMS resources ([NAVSEA](https://www.navsea.navy.mil/Portals/103/Documents/NSWC_Crane/SD-18/PDFs/Resources/ResourcesDMSMS.pdf)) | Gatekeeper and SBIR sponsor | DMSMS conference (model: m10); ask for locked-die memory cases |
| 6 | Trenton Systems | U.S. rugged server OEM | DDR4-dependent, DoD-facing ([Trenton](https://www.trentonsystems.com/blog/list-of-rugged-server-manufacturers)) | L1 + L2 | Sales Navigator to the supply-chain manager; lead with an LTB study |
| 7 | CP Technologies / Core Systems USA | U.S. rugged computing | Built in the U.S. ([CP North America](https://cpnorthamerica.com/?p=67)) | L1 + L2 | As #6 |
| 8 | Mid-size U.S. industrial SBC makers facing DDR3/DDR4 LTBs (e.g. WINSYSTEMS) | Industrial OEM | Long-lifecycle DDR boards ([Arm catalog](https://www.arm.com/partners/catalog/winsystemsinc)); DDR3 LTBs due within 18–24 months ([GlobX](https://globx.eu/blog/supply-chain-insight/ddr3-last-time-buy-2026)) | L1 + L2 | Component engineer; offer a drop-in part first, a bank only where none exists |
| 9 | NewSpace avionics makers on AMD/Xilinx SoCs | NewSpace | ISSI supports DDR4/LPDDR4 for AMD platforms to 2038 ([AMD/ISSI](https://www.amd.com/content/dam/amd/en/documents/products/adaptive-socs-and-fpgas/technologies/issi-memory-solution-brief.pdf)); **no named buyer** [UNVERIFIED] | L4 | Only through a hi-rel co-founder's network |
| 10 | Medical-imaging and rail-signaling OEMs (revalidation locks the die) | Regulated industrial | 63% of AdvaMed members report memory allocation problems ([AdvaMed, 2026-08-17](https://www.advamed.org/2026/08/17/memory-chip-shortages-implications-for-medtech-innovation-and-patient-care/)); **no locked-die case found** [UNVERIFIED] | L1 / L3 | AdvaMed supply-chain committee; ask for one locked-die case |

All triggers are [REPORTED].

**Channel partners, not customers:** Intelligent Memory and Alliance Memory (rep or distribution); Micross (vault and assembly); QP Technologies and Integra (package and test).

---

## 4. Go-to-market

*Revised after red team: superseded. DD7 is KILLED (§14), L1 has no buyer, and Micross sells the vault direct. The Phase 4 go-to-market below is kept for the record and will not be executed.*

**Only Plan A is go-to-market-ready. Plans B and C are gated (§8).**

**Channel.** Founder-led outbound to DMSMS managers and OEM component engineers; one DMSMS or defense-electronics event a year (model: $2,500 at m10, m22, m34); co-selling with whichever long-lifecycle DRAM maker signs a rep agreement; Micross as the white-label vault behind every program. Intelligent Memory added Sourceability and Flip as channel partners in 2026 to reach DDR3/DDR4 EOL customers ([Evertiq, 2026-10-06](https://evertiq.com/design/2026-10-06-intelligent-memory-signs-sourceability-as-global-distributor)) [REPORTED], so a rep slot is plausible.

**Pricing (model §1):** LTB study $4,000 (DD2 priced its study at $3,500); managed program $750/month plus a 4% agency fee on die bought and $1/unit on pulls; rep commission 5%. Bank parts and MCMs are not offered until Stages 1–2.

**Sales motion.** Find a DMSMS case or EOL notice on the prospect's bill of materials → offer a drop-in long-lifecycle part first (commission, trust) → where none exists, sell the LTB study → convert it into a managed program in which the OEM owns the die, Micross stores it, and the founder manages quantities, pulls and paperwork. The model's part-time funnel is **4 qualified conversations a month**, fully ramped from m6; 10% buy a study and 35% of those become programs (model §1).

**First 90 days**

| Days | Dates | Actions | Measurable output |
|---|---|---|---|
| 1–29 | 2026-11-02 → 11-30 | Kill test, tracks A–C (§10) | Pass/fail on each track, scored on day 29 against pre-set thresholds; go/no-go recorded 12-01 |
| 31–60 | 12-02 → 2027-01-01 | If passed: form the LLC; negotiate the rep agreement; get Micross white-label consignment terms in writing; draft the LTB study template | Signed term sheet with ≥1 DRAM maker; written Micross terms |
| 61–90 | 2027-01-02 → 01-31 | 12 qualified conversations from the §3 list; deliver the first study | ≥1 paid study (model: ~0.7 study-equivalents of one-off revenue by m4) |

---

## 5. Competitors and why you would win (honest)

All rows are [REPORTED] (search-snippet grade).

| Competitor | Legacy / hi-rel DRAM position | Scale or price evidence |
|---|---|---|
| **Rochester Electronics** (Newburyport MA) | Authorized aftermarket manufacturer; >10B die banked ([Electronic Specifier](https://www.electronicspecifier.com/around-the-industry/the-worlds-largest-wafer-bank-has-tripled-in-size-at-rochester-electronics)); "authorized by over 70" OCMs ([ADS directory](https://www.adsgroup.org.uk/members/rochester-electronics-ltd-2//), self-description); legacy DRAM through an Intelligent Memory distribution partnership (2024-03-25) | Private; revenue estimates **$200–500M** ([Similarweb](https://www.similarweb.com/company/rocelec.com)); ~864 staff in 2025 ([Revelio](https://www.reveliolabs.com/companies/rochester-electronics/employees)); [Business Wire](https://www.businesswire.com/news/home/20240325645193/en) |
| **Micross** (FL/NC) | Die sustainment and consignment vault; ~15M die stored at Apopka ([Micross Apopka](https://www.micross.com/about-us/facilities-and-locations/apopka-fl)); DMEA-accredited ([3D InCites, 2020-01](https://www.3dincites.com/2020/01/micross-raleigh-facility-receives-dmea-microelectronics-trusted-source-certification/), Raleigh site); also an assembly house | IBAS RESHAPE award, ceiling **$134.3M** ([I-Connect007](https://iconnect007.com/article/138727/1343m-dod-contract-expands-micross-advanced-interconnect-osat-capabilities-in-the-us/138724/aep)). It is a partner and a competitor at once |
| **Flip Electronics** | 22 OCM relationships; licensed EOL manufacturing since buying Resurgent (2023-02-21); Intelligent Memory channel partner. Lansdale (Phoenix) is a similar licensed house with no DRAM ([Lansdale](https://lansdale.com/mission_statement.php)) | PE-backed ([Business Wire](https://www.businesswire.com/news/home/20230221005100/en)) |
| **Teledyne e2v / Teledyne HiRel** | DDR4T04G72 x72 MCM on Micron die since 2020 ([SIJ](https://signalintegrityjournal.com/articles/1749-radiation-tolerant-ddr4-memory-chip-ddr4t04g72m)); 16GB DDR4 module (2025-07-24; [Business Wire](https://www.businesswire.com/news/home/20250724928807/en/Teledyne-HiRel-Semiconductors-Announces-High-Density-16-GByte-DDR4-Module)); Micron life-extension program since 2013 | RFQ-only; Avnet MOQ 5–25 ([Avnet](https://www.avnet.com/americas/manufacturers/m/c/teledyne-e2v/memory)) |
| **Mercury Systems** | Rad-tolerant 8GB DDR4 (2022-11-08; [SIJ](https://www.signalintegrityjournal.com/articles/2899-mercury-introduces-radiation-tolerant-8gb-ddr4-memory-component-to-power-enhanced-edge-processing-for-space-missions)); 16GB military DDR4 with 100% burn-in ([datasheet](https://www.mrcy.com/siteassets/product-datasheets/ddr/high-density-secure-memory-16gb-ddr4-builtsecure.pdf)) | **$8.2M** single memory order ([ICN](https://intelligencecommunitynews.com/mercury-systems-receives-8-2m-order-for-swap-optimized-memory-for-c2i-application/)) |
| **Frontgrade** | 18GB rad-tolerant DDR4 (2024-11-05) | No price ([Frontgrade](https://frontgrade.com/news/frontgrade-unveils-highest-density-available-rad-tolerant-18-gb-ddr4-memory-space)) |
| **Long-lifecycle DRAM makers** | Intelligent Memory (32Gb DDR4 back from Q3 2026; [IM](https://www.intelligentmemory.com/company/articles-news-events/intelligent-memory-to-exhibit-at-embedded-world-2026)); Alliance Memory; ISSI (DDR4/LPDDR4 to ≥2038; [AMD/ISSI](https://www.amd.com/content/dam/amd/en/documents/products/adaptive-socs-and-fpgas/technologies/issi-memory-solution-brief.pdf)); Winbond 16 nm DDR4 8Gb for industrial, 2026 shipment ([DigiTimes, 2025-12](https://digitimes.com/tag/winbond/001585.html)) | Winbond sold out through 2027, and customers are asking for LTAs to 2030 ([TrendForce, 2026-08-07](https://www.trendforce.com/news/2026/08/07/news-winbond-says-customers-seek-ltas-through-2030-adata-expects-even-tighter-dram-supply-in-2027/)) |
| **Micron Manassas** | U.S.-made 1-alpha DDR4/LP4 for defense, aerospace and medical: production started 2026-05-22, with qualified output expected by end-2026; the >$2B expansion *will* quadruple DDR4 wafer supply (Micron's own figure) | [Micron](https://micron.gcs-web.com/news-releases/news-release-details/micron-advances-made-america-memory-manufacturing-expansion) |

**Why you would mostly not win:**
- **The exiting makers don't authorize startups, and the makers who might are not exiting.** Micron's precedents are e2v ([GlobeNewswire, 2013-08-13](https://www.globenewswire.com/news-release/2013/08/13/1235643/0/en/e2v-aerospace-and-defense-Inc-Launches-a-Program-to-Provide-Extended-Life-for-Certain-SDR-and-DDR-Memory-Products-of-Micron-Technology-Inc.html?print=1)) and ATP ([PR Newswire, 2018-10](https://prnewswire.co.uk/news-releases/micron-and-atp-to-collaborate-on-ddr2-continuity-program-694766761.html)), both established houses. Winbond, ESMT, Etron and Nanya profit from the shortage and are *extending* legacy lines. Flip, the best precedent for a newer firm, took ~8 years, private equity and an acquisition to reach 22 OCMs.
- **Authorized DDR4 supply is growing** (Manassas, ISSI to 2038, Intelligent Memory), which pushes out the date banked die are needed.
- **Micross sells the vault direct,** so a program manager in between is a layer the OEM can remove.
- **On the MCM,** Teledyne, Mercury and Frontgrade have flight heritage and the same open KGD.

**Where an entrant could win (narrow, unproven):**
1. **Small locked-die programs below Rochester's attention:** a few thousand die per OEM, managed rather than owned. A service, not a moat, and only if §10 track B finds ≥3 locked-die cases in 10 interviews.
2. **A cheaper, U.S.-assembled, screened-but-not-NASA-Level-1 x72 MCM** for NewSpace and rugged industrial buyers (C-65 card). No evidence that buyers will pay for it [UNVERIFIED].
3. **Software-led LTB sizing as the door-opener.** That is DD2's product, which the red team called "a $249 feature distributors give away" (`05_REDTEAM.md`).

---

## 6. IP position

**What the venture would own:**
- **An OCM authorization or rep agreement, if won.** A contract, not IP, and the only real asset in C-91. It may carry change-of-control clauses (not checked; notes §13 gap 8), which matters for Plan C and any exit.
- **Transferred design and test archives,** licensed rather than owned, if an OCM hands them over with the wafers as Rochester's licences do ([electronica brochure](https://exhibitors.electronica.de/download/1121_11_2_2823_2_1_809/electronica_re_solutions-brochure_en_flipbookpdf.pdf)) [REPORTED].
- **MCM substrate design, signal-integrity models, screening flows and test programs:** trade secrets. Nothing is patentable; multi-die DRAM packaging has decades of prior art.
- **Software:** LTB sizer, program tracker, customer portal.

**Freedom to operate:**
1. **Marking.** Without authorization, banked die cannot carry the OCM part number; aftermarket parts must be marked so they are not mistaken for OCM parts ([ERAI](https://www.erai.com/glossary/Authorized%20Aftermarket%20Manufacturer/)) [REPORTED]. Unauthorized re-marking is counterfeit territory under DFARS.
2. **Test programs** belong to the OCM or the test house. Re-creating one is the $120k set-up item (model §1).
3. **KGD terms.** JEDEC JESD49B.01 governs KGD quality claims ([JEDEC](https://www.jedec.org/node/8358)) [REPORTED]. Winbond or ESMT supply agreements may restrict resale into some markets [UNVERIFIED].
4. **Competitor MCM patents** (Teledyne, 3D Plus, Mercury): not searched [UNVERIFIED]; low risk for a conventional side-by-side 9-die substrate. **Revised after red team (RT-PHY-DD7-01): not cleared.** A side-by-side nine-die layout does not fit the package, and stacked-memory packaging (3D Plus, Teledyne, the Irvine Sensors lineage) is a patented field that has not been searched.

---

## 7. Regulatory and funding path

**Rules that matter:**
- **DFARS 252.246-7008 / 246.870-2** create the moat only for an *authorized* aftermarket manufacturer. Without the letter, the venture is an independent distributor, which DFARS ranks last (§1).
- **Quality systems:** AS9120B for distribution (model: $35k over m21–m25, then $8k/yr); AS6496 for authorized distributors ([RF Essentials](https://rfessentials.com/resources/rf-glossary/as6496/)); MIL-PRF-38535 QML for hi-rel re-manufacture ([NSWC Crane SD-18](https://www.navsea.navy.mil/Home/Warfare-Centers/NSWC-Crane/Resources/SD-18/Products/Microcircuits/Facility-Assessment-Quality/)) [REPORTED]. **Revised after red team (RT-VET-DD7-06):** a nine-die x72 module is a hybrid microcircuit under **MIL-PRF-38534** (Class H/K), or a plastic part screened to NASA EEE-INST-002. 38534 certification attaches to a DLA-audited line, and those lines are largely owned by the §5 competitors [UNVERIFIED]. The model now carries $1.6M of NRE (was $1.4M) for line access. No QML cost was found; the model carries MCM qualification inside the $1.6M NRE (Phase 4: $1.4M).
- **Storage standards:** IEC 62435-5 ([BSI](https://knowledge.bsigroup.com/products/electronic-components-long-term-storage-of-electronic-semiconductor-devices-die-and-wafer-devices)) and GEIA-STD-0003B, revised Dec 2025 ([SAE](https://saemobilus.sae.org/standards/geiastd0003b-long-term-storage-lts-electronic-devices)) [REPORTED]. Customers will audit the vault against them.
- **Export:** ITAR registration once defense technical data is handled (model: $250/month from m30) [ESTIMATE: prior knowledge, not verified]. Rad-tolerant MCMs may fall under 9A515 or USML XV, which limits foreign NewSpace sales (VC and veteran scorers).
- **§5949** (statutory effect 2027-12-23; the implementing FAR rule was still a proposed rule as of 2026-11) bars CXMT, YMTC and SMIC chips from federal buys ([Federal Register](https://www.federalregister.gov/documents/2026/02/17/2026-03065/federal-acquisition-regulation-prohibition-on-certain-semiconductor-products-and-services)) [REPORTED]. Taiwanese and U.S. die are clean. That is a minor selling point, not a moat.

**Non-dilutive money:**
- **SBIR is closed to the founder while they keep the day job.** The SBIR principal investigator must be employed more than half-time by the small business ([NIST](https://www.nist.gov/tpo/small-business-innovation-research-program-sbir/resources/participation-eligibility-and)); SBIR/STTR is reauthorized to 2031-09-30 ([IEDC](https://www.iedconline.org/news/2026/04/15/federal-policy-updates/federal-policy-update-sbir-and-sttr-reauthorized/)) [REPORTED].
- **Precedent:** DLA awarded a Phase II SBIR on 2026-06-18 to re-create a legacy Signetics part ([SamSearch](https://samsearch.co/government-contracting-news/dla-awards-phase-ii-sbir-contract-to-phoenix-semiconductor-for-legacy-chip-solutions-118673)) [REPORTED]. **No DRAM-specific topic was found.**
- **STTR:** possible with a university PI, for example UMD CALCE on lifetime-buy optimisation ([CALCE](https://calce.umd.edu/event/20069/electronic-part-obsolescence-forecasting-mitigation-and-management)).
- **Other DoD money flows to incumbents.** IBAS went to Micross ($134.3M ceiling). DoW reverse-engineering money was ~$1.8M over two years to one network ([war.gov](https://www.war.gov/News/Releases/Release/Article/4401952/dow-addresses-material-obsolescence-through-reverse-engineering-training)). DPA Title III figures come only from a low-confidence repost.
- **Expect $0 non-dilutive money in the first 24 months.**

**Equity.** Plan B assumes $1.5M at m18 and $4.0M at m30, with no investor conversation behind either (model §1). **On these numbers, do not raise:** 0.29× of $11.49M (Phase 4: 0.46× of $8.11M; model §6, §10g) is not fundable venture equity. The realistic capital is private equity rolling up EOL houses (O2 Investment Partners → Flip; [PrivSource](https://www.privsource.com/acquisitions/deal/wySWZM)) or SBA 7(a) debt for Plan C, which fails the ~1.25 DSCR test in GLUT (0.85).

---

## 8. 18-month roadmap with measurable gates

*Revised after red team: superseded. No roadmap is executed. The m15 "DRAM OCM letter" gate is void (RT-VET-DD7-05); see the §10.0 reopen gates and §11.*

Plan A only; "model" figures are BASE (model §4). Gates sit at ~75% of the model path, so the expected case passes them.

| Period | Build / do | Gate (date: measurable test) |
|---|---|---|
| **m1** (Nov 2026) | Kill test (§10); no LLC until it passes | **2026-12-01:** each track passes, or its line is killed (§11 #1–4) |
| **m2–m5** (Dec 2026–Mar 2027) | LLC; rep agreement; Micross white-label terms; LTB study template (reuse DD2 code); 4 conversations/month | **2027-03-31:** ≥1 paid LTB study (model: ~$4.5k cumulative one-off revenue by m5, $4.0k of it studies) |
| **m6–m9** (Apr–Jul 2027) | Full funnel; first managed program at a vault | **2027-07-31:** rep agreement live (model: commissions from m9); ≥1 program contracted (model 0.8) |
| **m10–m12** (Aug–Oct 2027) | DMSMS conference; ask every contact for locked-die cases | **2027-10-31:** recurring ARR ≥ **$9.5k** (model $12.6k); ≥1 program billing (model 1.1) |
| **m13–m15** (Nov 2027–Jan 2028) | Assemble the Stage-1 file; watch the glut signal (A-05) | **2028-01-31 (Stage-1 gate):** a DRAM OCM letter **and** ≥3 locked-die LOIs at ≥2.5× the EOL price; otherwise no raise, and Plan A stays a side line inside DD2 |
| **m16–m18** (Feb–Apr 2028) | If the gate passed: recruit the hi-rel co-founder and quality manager; open investor talks. **Buy no wafers** | **2028-04-30:** recurring ARR ≥ **$16.5k** (model $22.0k: 1.9 programs, 2.8 rep accounts). Raise $1.5M only if the m15 gate passed **and** a hi-rel co-founder has signed |

**No bank purchase with founder money at any point.** A bank bought at the 2026–27 peak returns 6.5% at best on Phase 4 inputs, and −16.5% on revised inputs (model §3), on ~$0.3M of die plus set-up cost that the founder does not have [ESTIMATE: 12,510 die × 0.75 × $20.37 + $120k ≈ $311k].

---

## 9. Team required

| Role | When | Cost (model input unless noted) | Where to find |
|---|---|---|---|
| **Founder** (sales, program management, software) | Now, ~15 h/week | Unpaid in Plan A; Plan B full-time from m18 at $11k/month loaded | — |
| **Contracts attorney** | m1–m2 | $900 rep-agreement review + $2,500 LLC/rep legal (in the $3,900 month-1 one-off, with the $500 employer review; Phase 4: in the $8.5k one-off) | Government-contracts boutiques (as in DD2) |
| **DMSMS advisor** (retired DoD obsolescence manager) | m1 | 0.25–0.5% equity [ESTIMATE] | DMSMS conference; NSWC Crane and DLA alumni on LinkedIn (post-government employment rules not checked) |
| **Hi-rel hardware co-founder** (package/SI or memory reliability, flight heritage) | Before any raise (m16–m18) | Equity; salary from Stage 1 [ESTIMATE] | Teledyne e2v/HiRel, Mercury, Frontgrade, DDC, 3D Plus alumni |
| **Quality / operations manager** (AS9120B, AS6081, AS6496) | m19+ (Plan B) | $11k/month loaded | Rochester (Newburyport MA), Flip, Micross alumni |
| **Memory test engineer** (contract) | m19–m30 | $6k/month | Integra (Wichita KS) and Micross test alumni |
| **2 MCM package / SI engineers** | m30+ | $36k/month for both | Same pool as the co-founder |
| **Defense business developer** | m31+ | $16k/month loaded | Ex-Mercury, Teledyne or Micross sales staff |
| **Operations technician** (bank pulls) | m38+ | $8k/month | Local hire near the vault |
| **Second BD + production / quality engineer** | m60+ | $30k/month | — |

Plan A needs only the founder, an attorney and an advisor: its virtue and its ceiling. Plan B needs a hardware company built around someone the founder does not yet know.

---

## 10. Cheapest experiment that could kill it

**Revised after red team: the 29-day kill test is WITHDRAWN and will not be run.** The red team killed L1, L3 and Plan C with evidence and model re-runs (§14), so the test has nothing left to decide. It would have cost ~$6,000 and ~50 founder hours in the same weeks as DD6's and DD2's tests. Every 10 h/month diverted from DD6 cuts DD6's revised m36 ARR from $63.9k to $56.2k (model §10h); on DD6's Phase 4 inputs it moved DD6's full-time switch from m23 to m33 (RT-VC-DD7-03).

The test was also mis-specified:
- Track A could pass on a rep agreement without testing the moat (RT-HYP-DD7-05, RT-VC-DD7-04, RT-VET-DD7-05).
- Track B could pass on demand that a re-packaged die cannot serve (RT-VET-DD7-02).
- C1's $15 line could pass a losing bank (RT-VET-DD7-03).
- C4 bought the wrong die, a 4Gb x16 (RT-PHY-DD7-05).
- ~42% of the budget bought evidence for the shelved L4 line (RT-VET-DD7-07).

### 10.0 Reopen conditions (revised after red team; $0 passive watch, no founder hours scheduled)

DD7 is reopened only if one of the triggers below arrives unsolicited, or after DD6 has failed its K1. Step 0b applies before any rep or OEM conversation.

| Gate | What must arrive, in writing | Source |
|---|---|---|
| **K0 / Step 0b: employer** | A ~$500 employment-agreement review and a written employer carve-out covering component representation and LTB services. **Refusal → kill on the spot** | RT-HYP-DD7-06 |
| **A′: moat (C-91)** | ≥1 OCM states it would license EOL wafers or die, test programs and part-number marking rights for a **named EOL DDR3/DDR4 part** to a new U.S. entity as an authorized aftermarket manufacturer, with indicative terms. A rep or distribution offer scores only as L2 | RT-HYP-DD7-05, RT-VC-DD7-04, RT-VET-DD7-05 |
| **B′: demand** | ≥3 of 10 interviewees answer in writing "yes, with no more than a paper delta qualification" to: *"Would you accept a part built by a third party from banked die in a new package, without re-qualifying the board, and what delta qualification would you require?"* At least 3 must be die-consuming hybrid/SiP/MCM makers without their own vault | RT-VET-DD7-02, RT-VET-DD7-01 |
| **C1′: pull cost (L3)** | U.S. OSAT and test-house quotes for wafer re-probe on the OCM sort program, window-BGA assembly, 3-temperature at-speed test and burn-in, plus a 300 mm backgrind and saw quote, **≤$17.64/die all-in** (unit-GM break-even). A positive IRR needs ≤$1.53/die, so no entrant quote will do. Also bond-pull and yield data on die stored ≥10 years in N2, and a vault quote that includes surveillance | RT-VET-DD7-03, RT-PHY-DD7-03/-04 |
| **C2′: MCM (C-65)** | A hi-rel co-founder who brings an **existing** x72 design-in; ≥3 evaluation LOIs at ≥$1,200; a ≤15×20 mm floorplan quote stating the stack and RDL steps; a KGD supply agreement for the exact 8Gb x8 die with revision notice and lot traceability; ≤1% per-die fallout at a 125 °C screen on ≥100 die; an independent QML-38534 or EEE-INST-002 house with NRE ≤$2M and assembly + screen ≤$290 | RT-PHY-DD7-01/-02/-05, RT-VET-DD7-04/-06/-07, RT-VC-DD7-06 |
| **D: DoD study work** | A prime's written statement that LTB-study inputs are not CUI/CTI, **or** ~$35k + $500/month of NIST SP 800-171 cost in a plan that keeps cash ≥$20k; SAM/CAGE and DD 2345 in place | RT-HYP-DD7-02 |
| **E: defense OEM agency** | Two of #6–#8 confirm in writing that they would contract an uncertified program manager, **or** AS9120B is funded without breaking the $20k floor | RT-HYP-DD7-03 |

### Phase 4 test (superseded; not run; kept for the record)

**Budget ≈ $6,000: $100 Sales Navigator + ~$2,500 event or OEM visit + ~$2,500 KGD lot and quote run + $900 legal review. A 50% overrun is $9,000, so spending stops hard at $10,000. The model books its m1 one-off at $8,500, which adds $2,500 of LLC and rep legal; that $2,500 is spent only after a pass. Duration: 29 days, 2026-11-02 → 2026-11-30 (scored on day 29), with the go/no-go recorded 2026-12-01. About 50 founder hours.**

**Step 0 (2026-11-02).** Write the thresholds below into a dated document and email it to one outside person before any call.

**Step 1 (days 1–10). Track A: will any DRAM OCM deal with a new entity?** Send structured RFIs to the U.S. sales offices of **Winbond, ESMT, Etron, Nanya, Alliance Memory and Intelligent Memory**; phone on day 7. Ask: (1) Will you sign an authorized distribution, rep or aftermarket agreement with a new U.S. entity? (2) What wafer or KGD minimum order, price and payment terms apply to an LTB-style bank of one DDR3/DDR4 part? (3) Which certifications do you require (AS9120B, AS6496)?

**Step 2 (days 3–25). Track B: is there locked-die DRAM demand?** Run 10 thirty-minute interviews with DMSMS managers and mid-size OEMs from §3 (#1–3, #6–8, #10), via Sales Navigator (~$100) and one event or OEM visit (~$2,500). Ask: (1) In the last 24 months, how many DRAM obsolescence cases had **no** acceptable JEDEC substitute? (2) What did you pay, and to whom? (3) Would you sign an LOI for a managed bank or an authorized part at ≥2.5× the EOL price?

**Step 3 (days 3–25). Track C: written supply-side quotes.**
1. Micross consignment storage for one 10-wafer bank, plus whether Micross will accept a third-party program manager.
2. QP Technologies or Integra: package plus at-speed test of a DDR4 x16 FBGA-96, set-up cost and unit price at 2,000 units.
3. An x72 MCM substrate design and assembly quote.
4. Buy a small lot of ESMT or Winbond DDR4 KGD from distributor stock to test availability and price ([Suntsu](https://suntsu.com/product/integrated-circuits/memory/kgd-256mbx16-ddr4-1-2v/) listed 175 ESMT die on 2026-05-26) (~$2,500 including a quick-turn quote run).

**Step 4 (days 20–28).** Have a $900 legal review of any rep-agreement draft received.

**Step 5 (day 29, 2026-11-30).** Score each track; put the quotes into model inputs `storage_pct_yr`, `pack_unit`, `test_unit`, `bank_nre_first`, `mcm_nre_total`, `aftermarket_mult` and `p_program`; re-run and re-score.

**Pre-set pass/fail**

| Track | Pass | Fail → action |
|---|---|---|
| A: OCM willingness | ≥1 of 6 offers a rep or distribution agreement **and** ≥1 quotes wafer or KGD terms, in writing by day 29 | Pass not met (for example, 0 of 6 will discuss anything beyond a stocking distributorship needing >$250k of inventory, or <3 of 6 reply in writing) → **kill C-91** (bank and authorization path) |
| B: locked-die demand | ≥3 of 10 report a locked-die DRAM case worth ≥$50k life-of-need, and they would not default to Rochester or Micross | Fewer than 3 of 10 meet the pass test (for example, all default to Rochester/Micross) → **kill DD7 entirely** (no premium anywhere) |
| C1: bank pull cost | Quoted re-probe + package + test ≤ $15 per die | > $15 → **kill the bank line** (L3) |
| C2: MCM economics | MCM NRE ≤ $2M **and** unit build ≤ $400 before die | Either fails → **kill the MCM line** (L4) |
| C3: vault access | Micross (or an equal vault) quotes white-label consignment for a third-party program manager | Refused → **kill L1**; Plan A has no product |

---

## 11. Explicit kill criteria

**Revised after red team: DD7 is KILLED as of 2026-11-01 (§14).** The Phase 4 criteria below are superseded and kept for the record. The rules that still apply:

1. **Now (2026-11-01):** DD7 gets **zero founder hours and $0**. The 29-day test is not run, and no LLC is formed for DD7.
2. **Residual L2 rep line:** it may be considered **only after DD6 fails its K1**, and only after K0 (written employer carve-out; refusal kills it). It also needs a written rep offer at ≥5% that includes house accounts in a named territory (RT-VC-DD7-08). If it ever runs, fixed costs stay ≤$300/month, and it stops the first month cash would fall below $20k.
3. **No title-taking bank, ever, at startup pull costs.** Rule #11 is rewritten: buy only if projected unit GM is ≥20% **and** the 10-year IRR clears the hurdle at a pull yield of 0.85 with surveillance cost included. On revised inputs no purchase date passes (RT-PHY-DD7-03, RT-VET-DD7-03).
4. **No DoD-facing study work** without gate D, and **no defense-OEM agency work** without gate E (§10.0).
5. **No reopening of C-91 or C-65** except on the §10.0 A′ or C2′ triggers. B′ must also pass before any money is spent.
6. **Any outside raise** needs A′ **and** B′ **and** a signed hi-rel co-founder. The Phase 4 m15 gate ("a DRAM OCM letter") is void, because a rep letter would have satisfied it (RT-VET-DD7-05).

**Phase 4 kill criteria (superseded):**

1. **2026-12-01:** track B fails → **kill DD7**, every line.
2. **2026-12-01:** track A fails → kill C-91's bank and authorization path. At most, keep L1 inside DD2.
3. **2026-12-01:** track C1 fails → kill L3. Track C2 fails → kill L4. Track C3 fails → kill L1.
4. **2026-12-01:** OCM non-replies do not extend the test. Fewer than 3 written answers out of 6 by day 29 (2026-11-30) counts as a track A fail.
5. **2027-03-31 (m5):** zero paid LTB studies → stop Plan A.
6. **2027-07-31 (m9):** no signed rep agreement → drop L2. The model's m36 ARR falls by the $8.6k of commissions.
7. **2027-10-31 (m12):** recurring ARR < $9.5k (75% of the model's $12.6k), or no program billing → stop Plan A and fold any live program into DD2.
8. **Any month:** cash below $20,000 (model low $30.2k at m3) → stop and put in no more founder money.
9. **2028-01-31 (m15):** no OCM letter **or** fewer than 3 locked-die LOIs at ≥2.5× the EOL price → no Stage-1 raise, ever, on this thesis.
10. **2028-04-30 (m18):** no hi-rel co-founder signed → no Stage-1 raise, even if #9 passed.
11. **Every bank decision:** projected unit GM at purchase < 20% → do not buy. This rule blocks every GLUT and SEVERE purchase at startup pull costs (model §5).
12. **2029-04-30 (m30, Plan B only):** no MCM evaluation LOI → no Stage 2. The bank continues only if it is cash-positive on its own.
13. **2032-10-31 (~m72, Plan B only):** fewer than 4 design-ins a year at ~1,000 units → stop MCM investment. Below that, the grid shows ≤2.4× capital (§2.3).

---

## 12. Cycle test (glut and severe, with model numbers)

*Revised after red team (model §3–§6, §10):*
- **L3 bank:** not bought even in BASE (unit GM −12.8% at m20).
- **L4 MCM GM at m36:** 26.7% BASE / 32.4% GLUT / 39.2% SEVERE. Cheaper die still raise margin.
- **Residual L2:** m36 ARR $8.6k / $4.4k / $928.
- **Plan B:** 0.29× / 0.24× / 0.19× of capital.
- **ITAD supply:** recovered hyperscaler DDR4 (2019–22 fleets) reaches ITAD in 2028–30, the bank's sell window. It caps non-DFARS prices in every scenario, BASE included (RT-HYP-DD7-04).

The Phase 4 table follows.

Legacy DDR4 falls from $20.37/GB to $16.80 (BASE), $8.15 (GLUT, −60%, A-05) or $2.04 (SEVERE) by m20, and all three reach $3.00 by m60 (model §2).

| Line | BASE | GLUT | SEVERE | Mechanism |
|---|---|---|---|---|
| L3 bank (bought m20) | Unit GM 39.6%, IRR 2.6% | **Not bought** (unit GM −1.1%, IRR −32.8% if forced) | **Not bought** (unit GM −236.6%) | Sale price falls, the ~$11.50/die U.S. pull cost does not, and multiples compress (×0.9, ×0.8) |
| L4 MCM unit GM at m36 | 52.2% | **57.0%** | **62.7%** | Cheaper die *raise* margin, but design-ins fall ×0.85 / ×0.70 as NewSpace buyers revert to upscreened commercial DDR4 |
| L2 commissions at m36 | $8.6k/yr | $4.4k/yr | **$928/yr** | Commission scales with the DRAM price |
| Plan A recurring ARR m36 | $42.6k | $33.5k (**−21%**) | $26.4k (**−38%**) | Fewer LTBs when supply is abundant (demand ×0.75 GLUT, ×0.60 SEVERE) and smaller commissions |
| Plan B year-10 revenue / EV ÷ capital | $2.49M / 0.46× | $2.06M / 0.36× | $1.69M / 0.28× | No bank revenue at all in GLUT/SEVERE; MCM revenue only |
| Plan B total outside capital | $8.11M | $8.50M | $9.08M | Bridges grow ($2.61M → $3.58M) |
| Plan C acquisition DSCR | 1.50 | **0.85** | **0.45** | EBITDA $900k → $510k → $270k (revenue −15% / −25%; margin 15% → 10% → 6%) |

**Verdict.** **The bank dies in a glut**; it survives only as a decision not to buy. **The MCM mostly survives**, because margin improves while volume softens. **The service wedge shrinks 21–38%.** "Lifecycle-driven, so glut-proof" is only half true: EOL demand persists, but every line priced off DRAM (bank sales, commissions, agency fees) falls with it. The glut also arrives before any Plan B hardware revenue (first MCM design-in m60), so a funded company would burn through the trough on outside money, and a severe trough leaves a Plan C acquisition unable to service its debt.

---

## 13. Sources

Every URL below is in `research/sources/*.jsonl` (mostly `p4-legacy-dram-diebank`; others from `E`, `C`, `p3-audit-09/13`, `v1-policy`, `p4-lifecycle-intel`) and is carried into `research/sources/p4w-legacy-dram-diebank.jsonl`. The verifier added nine §5 URLs that were already logged (`p4-legacy-dram-diebank`, `p3-audit-13`, `v1-policy`), and re-checked the DSPO 99.3%, the Teledyne DDR4T04G72 and Micron Manassas by search (`research/sources/p4v-legacy-dram-diebank.jsonl`). All are search-snippet grade unless the log says otherwise.

**Authorization model and aftermarket precedents**
- https://github.com/GSA/GSA-Acquisition-DFARS/blob/master/dita/252.246-7008.dita
- https://github.com/GSA/GSA-Acquisition-DFARS/blob/master/dita/246.870-2.dita
- https://www.erai.com/glossary/Authorized%20Aftermarket%20Manufacturer/
- https://rfessentials.com/resources/rf-glossary/as6496/
- https://exhibitors.electronica.de/download/1121_11_2_2823_2_1_809/electronica_re_solutions-brochure_en_flipbookpdf.pdf
- https://www.globenewswire.com/news-release/2013/08/13/1235643/0/en/e2v-aerospace-and-defense-Inc-Launches-a-Program-to-Provide-Extended-Life-for-Certain-SDR-and-DDR-Memory-Products-of-Micron-Technology-Inc.html?print=1
- https://prnewswire.co.uk/news-releases/micron-and-atp-to-collaborate-on-ddr2-continuity-program-694766761.html
- https://www.businesswire.com/news/home/20230221005100/en
- https://www.privsource.com/acquisitions/deal/wySWZM
- https://lansdale.com/mission_statement.php
- https://evertiq.com/design/2026-10-06-intelligent-memory-signs-sourceability-as-global-distributor

**Demand, EOL and DMSMS**
- https://www.dsp.dla.mil/Portals/26/Documents/Conference/2024%20Briefings/Day%203%20-%20August%208/Brown%20-%20Program%20Update.pdf
- https://www.navsea.navy.mil/Portals/103/Documents/NSWC_Crane/SD-18/PDFs/Resources/ResourcesDMSMS.pdf
- https://www.z2data.com/insights/how-chip-obsolescence-is-making-dmsms-worseand-where-we-re-headed-in-2027
- https://www.trendforce.com/news/2025/06/13/news-micron-confirms-ddr4-phase-out-with-eol-notices-reportedly-hints-at-price-hikes-ahead/
- https://www.mouser.com/PCN/Micron_Technology_PCN_36146.pdf
- https://globx.eu/blog/supply-chain-insight/ddr3-last-time-buy-2026
- https://www.advantech.com/en-us/resources/news/【phase-out】selected-d3-dram-module-part-numbers-and-ddr3-dram-module-eol
- https://www.advamed.org/2026/08/17/memory-chip-shortages-implications-for-medtech-innovation-and-patient-care/

**Customers and solicitations**
- https://www.cleat.ai/government/contracts/dmsms-and-obsolescence-management-reporting-sqml
- https://www.cleat.ai/government/contracts/dmsms-mitigation-and-reverse-engineering-gbao
- https://www.cleat.ai/government/contracts/memory-upgrade-so4p
- https://www.trentonsystems.com/blog/list-of-rugged-server-manufacturers
- https://cpnorthamerica.com/?p=67
- https://www.arm.com/partners/catalog/winsystemsinc
- https://www.amd.com/content/dam/amd/en/documents/products/adaptive-socs-and-fpgas/technologies/issi-memory-solution-brief.pdf

**Competitors and supply**
- https://www.businesswire.com/news/home/20240325645193/en
- https://www.similarweb.com/company/rocelec.com
- https://www.reveliolabs.com/companies/rochester-electronics/employees
- https://iconnect007.com/article/138727/1343m-dod-contract-expands-micross-advanced-interconnect-osat-capabilities-in-the-us/138724/aep
- https://www.avnet.com/americas/manufacturers/m/c/teledyne-e2v/memory
- https://intelligencecommunitynews.com/mercury-systems-receives-8-2m-order-for-swap-optimized-memory-for-c2i-application/
- https://frontgrade.com/news/frontgrade-unveils-highest-density-available-rad-tolerant-18-gb-ddr4-memory-space
- https://signalintegrityjournal.com/articles/1749-radiation-tolerant-ddr4-memory-chip-ddr4t04g72m
- https://www.trendforce.com/news/2026/08/07/news-winbond-says-customers-seek-ltas-through-2030-adata-expects-even-tighter-dram-supply-in-2027/
- https://micron.gcs-web.com/news-releases/news-release-details/micron-advances-made-america-memory-manufacturing-expansion
- https://suntsu.com/product/integrated-circuits/memory/kgd-256mbx16-ddr4-1-2v/
- https://www.jedec.org/node/8358
- https://www.electronicspecifier.com/around-the-industry/the-worlds-largest-wafer-bank-has-tripled-in-size-at-rochester-electronics
- https://www.adsgroup.org.uk/members/rochester-electronics-ltd-2//
- https://www.micross.com/about-us/facilities-and-locations/apopka-fl
- https://www.3dincites.com/2020/01/micross-raleigh-facility-receives-dmea-microelectronics-trusted-source-certification/
- https://www.businesswire.com/news/home/20250724928807/en/Teledyne-HiRel-Semiconductors-Announces-High-Density-16-GByte-DDR4-Module
- https://www.signalintegrityjournal.com/articles/2899-mercury-introduces-radiation-tolerant-8gb-ddr4-memory-component-to-power-enhanced-edge-processing-for-space-missions
- https://www.mrcy.com/siteassets/product-datasheets/ddr/high-density-secure-memory-16gb-ddr4-builtsecure.pdf
- https://www.intelligentmemory.com/company/articles-news-events/intelligent-memory-to-exhibit-at-embedded-world-2026
- https://digitimes.com/tag/winbond/001585.html

**Storage physics and standards**
- https://www.infineon.com/dgdl/Storage_of_Products_Supplied_by_Infineon_Technologie.pdf
- https://www.micross.com/sustainment-solutions/program-sustainment-management/long-term-die-and-wafer-storage
- https://www.digikey.com/en/blog/testing-confirms-that-component-reliability-remains-with-proper-long-term-storage
- https://knowledge.bsigroup.com/products/electronic-components-long-term-storage-of-electronic-semiconductor-devices-die-and-wafer-devices
- https://saemobilus.sae.org/standards/geiastd0003b-long-term-storage-lts-electronic-devices
- https://www.navsea.navy.mil/Home/Warfare-Centers/NSWC-Crane/Resources/SD-18/Products/Microcircuits/Facility-Assessment-Quality/

**Regulation and funding**
- https://www.federalregister.gov/documents/2026/02/17/2026-03065/federal-acquisition-regulation-prohibition-on-certain-semiconductor-products-and-services
- https://www.nist.gov/tpo/small-business-innovation-research-program-sbir/resources/participation-eligibility-and
- https://www.iedconline.org/news/2026/04/15/federal-policy-updates/federal-policy-update-sbir-and-sttr-reauthorized/
- https://samsearch.co/government-contracting-news/dla-awards-phase-ii-sbir-contract-to-phoenix-semiconductor-for-legacy-chip-solutions-118673
- https://calce.umd.edu/event/20069/electronic-part-obsolescence-forecasting-mitigation-and-management
- https://www.war.gov/News/Releases/Release/Article/4401952/dow-addresses-material-obsolescence-through-reverse-engineering-training

**Phase 5 red-team sources (`research/sources/p5r-legacy-dram-diebank.jsonl`; search-snippet grade)**
- https://www.micross.com/uploads/806a7ab8-585d-4e8b-8608-4464e5cadfd4/EDSP_Rev_1_WEB.pdf
- https://www.micross.com/products-and-services/eol-dmsms-sustainment/original-qualified-product/eol-die-sustainment-program-edsp
- https://www.micross.com/components-and-services/eol-dmsms-sustainment/program-sustainment-management
- https://www.micross.com/about-us/news-and-info/newsletters/august-2024-life-cycle-management-with-die-wafer-sustainment
- https://knowledge.bsigroup.com/products/electronic-components-long-term-storage-of-electronic-semiconductor-devices-deterioration-mechanisms
- https://www.guru3d.com/story/teledyne-e2v-introduces-first-radiation-tolerant-ddr4-memory-for-space-applications/
- https://www.gdm.or.jp/pressrelease/2020/0526/349733
- https://snapeda.com/parts/DDR4T04G72/Teledyne%20e2v/view-part
- https://html.alldatasheet.net/html-pdf/533530/HYNIX/HMT312S6DFR6A-H9/1644/10/HMT312S6DFR6A-H9.html
- https://patents.google.com/patent/US9412433
- https://smallbiztrends.com/sales-commission-rates-by-industry/
- https://repfabric.com/industries/electronics/

**Models:** `models/legacy-dram-diebank.py` (this deep dive) and `models/dram_cost_stack.py` (DDR5 price deck, imported). DD6's model (`models/private-moe-appliance.py`) is imported read-only by model §10h.

---

## 14. Red-team outcome

Phase 5, round 2, 2026-11-01. Owner: `p5r-legacy-dram-diebank`. Four adversarial reviewers attacked this deep dive:

- **VET:** a 30-year DRAM process veteran.
- **VC:** a semiconductor VC who lost money on memory startups.
- **HYP:** a hyperscaler procurement lead.
- **PHY:** a condensed-matter physicist.

They raised **27 objections against DD7: 3 FATAL, 12 MAJOR, 12 MINOR**. The objections are in `research/phase5/rt2_*.json`. Every response is recorded verbatim in `research/phase5/responses_legacy-dram-diebank.json`. Each quantitative objection was re-run in the model. Model §10 reproduces the Phase 4 output exactly from `INPUTS_P4` and then shows each reviewer's variant. Five web searches were used (`research/sources/p5r-legacy-dram-diebank.jsonl`).

**Dispositions: 0 REFUTED · 4 ACCEPTED-MITIGATED · 18 ACCEPTED-DOWNGRADE · 5 ACCEPTED-KILL.** The kills hit three named legs: **L1** (three FATALs), **L3** (RT-VET-DD7-03) and **Plan C** (RT-VC-DD7-07).

### 14.1 Objections and dispositions

| Objection | Severity | Disposition | One-line action |
|---|---|---|---|
| RT-HYP-DD7-01 | FATAL | ACCEPTED-KILL | **L1 killed.** Bare-die banking costs the OEM 2.9–5.4× a packaged LTB; no die supply for Micron/Samsung boards (`l1_enabled` 1→0; model §10b) |
| RT-HYP-DD7-02 | MAJOR | ACCEPTED-DOWNGRADE | DoD DMSMS customers #1–3 dropped. CUI/NIST 800-171 (~$35k + $500/mo) breaks the $20k floor at m6 (§10c); gate D |
| RT-HYP-DD7-03 | MAJOR | ACCEPTED-DOWNGRADE | Defense OEMs dropped from founder-funded plans. AS9120B in year 1 breaks the floor at m3 (§10c); gate E |
| RT-HYP-DD7-04 | MINOR | ACCEPTED-DOWNGRADE | `aftermarket_mult` 2.5→2.0 (DFARS / non-DFARS blend). ITAD DDR4 caps non-DFARS prices; BASE bank no longer bought |
| RT-HYP-DD7-05 | MINOR | ACCEPTED-DOWNGRADE | Track A and the m15 gate rewritten to need written aftermarket rights on a named part (gate A′) |
| RT-HYP-DD7-06 | MINOR | ACCEPTED-MITIGATED | K0 / Step 0b: $500 employment-agreement review and written carve-out; kill on refusal |
| RT-HYP-DD7-07 | MINOR | ACCEPTED-DOWNGRADE | $6.3–25.4M "ceiling" withdrawn; restated as a fee pool of ≤$1.14M ARR at 100% share (§10i) |
| RT-PHY-DD7-01 | MAJOR | ACCEPTED-DOWNGRADE | MCM does not fit 15×20 mm. Stacked/RDL build: substrate $60→$90, assembly $80→$160; FTO #4 "not cleared" |
| RT-PHY-DD7-02 | MAJOR | ACCEPTED-DOWNGRADE | No JEDEC refresh above 95 °C; 23–72% refresh tax at 125 °C. Per-die hot bin; lead grade −40 to 105 °C |
| RT-PHY-DD7-03 | MAJOR | ACCEPTED-DOWNGRADE | Bare-die storage TRL 9→6–7. `pull_yield` 0.95→0.90; +$5k/yr surveillance; bank rule needs IRR at 0.85 yield |
| RT-PHY-DD7-04 | MINOR | ACCEPTED-MITIGATED | Whole wafer packaged at opening (`pull_whole_wafer`); IRR effect 2.64%→2.57%; 300 mm saw quote added to C1′ |
| RT-PHY-DD7-05 | MINOR | ACCEPTED-MITIGATED | Die basis 45→75 mm²: 736 good die/wafer, 17 wafers per bank; C4's wrong-die purchase withdrawn |
| RT-VC-DD7-01 | FATAL | ACCEPTED-KILL | **L1 killed.** Founder billing alone ($85k) exceeds the die value ($52k); Phase 4 pull-billing bug fixed |
| RT-VC-DD7-02 | MAJOR | ACCEPTED-DOWNGRADE | Micross EDSP sells the whole bundle direct (confirmed by search). `p_program` 0.35→0.10 |
| RT-VC-DD7-03 | MAJOR | ACCEPTED-DOWNGRADE | DD7 gets zero hours. On DD6's Phase 4 inputs, full-time slips m23→m33 at −10 h/month; on DD6's revised model it is never full-time and m36 ARR falls $63.9k→$56.2k (model §10h). The kill test is withdrawn |
| RT-VC-DD7-04 | MAJOR | ACCEPTED-DOWNGRADE | Moat untested and likely unobtainable (OCMs extending, not exiting); P(rights in 15 months) ≤5% [ESTIMATE] |
| RT-VC-DD7-05 | MINOR | ACCEPTED-DOWNGRADE | Ceiling restated as a fee pool; 3–5% share = $34–57k of new ARR a year |
| RT-VC-DD7-06 | MINOR | ACCEPTED-DOWNGRADE | Plan B 0.46×→0.29×; the 4×1,000 cell falls 4.04×→2.73×; BULL ≈22%/yr gross; 3D Plus added to competitors |
| RT-VC-DD7-07 | MINOR | ACCEPTED-KILL | **Plan C killed**: full-time founder, a personal guarantee on ~$3.6M, no named target |
| RT-VC-DD7-08 | MINOR | ACCEPTED-DOWNGRADE | L2 is a contingent residual only: $8.6k BASE m36, ~$2.2k probability-weighted, never breaks even at $680/mo |
| RT-VET-DD7-01 | FATAL | ACCEPTED-KILL | **L1 killed**; "optional DD2 SKU" withdrawn. Named buyers use packaged FBGA or DIMMs, not die |
| RT-VET-DD7-02 | MAJOR | ACCEPTED-DOWNGRADE | DO-254/FDA locks are on the packaged part, so an unauthorized die bank cannot serve them. Track B rewritten (gate B′) |
| RT-VET-DD7-03 | MAJOR | ACCEPTED-KILL | **L3 killed.** +$10/die burn-in and hot/cold test. Revised m20 BASE IRR −26.6%; no bank in any scenario; IRR break-even ≤$1.53/die |
| RT-VET-DD7-04 | MAJOR | ACCEPTED-DOWNGRADE | `mcm_yield` 0.91→0.76; +$75k/yr per-lot requalification; revised MCM GM 18.7–38.2% |
| RT-VET-DD7-05 | MAJOR | ACCEPTED-DOWNGRADE | Track A and the m15 gate need written licence terms for wafers, test programs and marking; a rep offer counts only as L2 |
| RT-VET-DD7-06 | MINOR | ACCEPTED-DOWNGRADE | MIL-PRF-38534 (not 38535); NRE $1.4M→$1.6M for line access; assembly + screen $310 > the $290 bar |
| RT-VET-DD7-07 | MINOR | ACCEPTED-MITIGATED | Kill test withdrawn ($6k and ~50 h saved); any L4 reopen starts with a 125 °C screen of the right die |

### 14.2 Changes made

**Model** (`models/legacy-dram-diebank.py`, RED-TEAM REVISIONS (Phase 5) block). It was re-run with exit 0, and the output was overwritten in `research/phase4/legacy-dram-diebank_model_output.md`. `INPUTS_P4` keeps the Phase 4 inputs, so model §10a reproduces $42.6k / 39.6% / 2.6% / 45.6–61.8% / 0.46× exactly.

- **Inputs changed (old → new, objection):**
  - **L1:** `l1_enabled` 1→0 (HYP/VC/VET-DD7-01); `p_program` 0.35→0.10 (VC-02); `pull_cap_to_ltb` off→on (VC-01; fixes 8,000 pulls billed from a 4,000-die program).
  - **One-off cost:** `oneoff_m1` $8,500→$3,900 (kill test withdrawn; +$500 employer review, HYP-06).
  - **L3 bank:**
    - `burnin_hotcold_unit` $0→$10/die (VET-03); `pull_yield` 0.95→0.90 (PHY-03); `surveillance_yr` $0→$5,000 per bank (PHY-03); `pull_whole_wafer` off→on (PHY-04).
    - `aftermarket_mult` 2.5→2.0 (HYP-04).
    - `good_die_per_wafer` 1,251→736 and `bank_wafers` 10→17 (PHY-05).
  - **L4 MCM:** `mcm_substrate` $60→$90 and `mcm_assembly` $80→$160 (PHY-01); `mcm_yield` 0.91→0.76 (VET-04, PHY-02); `mcm_nre_total` $1.4M→$1.6M (VET-06); `mcm_lot_requal_yr` $0→$75k/yr (VET-04).
- **Structural changes:**
  - New functions: `pull_cost()`, `pull_charge()` (whole-wafer opening), `pull_breakeven()`, `l1_buyer_cost()` and `dd6_hours_check()`. The last one imports DD6's model to test RT-VC-DD7-03.
  - Variant hooks (`planA_extra_*`) for the CUI and AS9120B cases.
  - A sturdier IRR bracket: a tiny negative cash-flow tail no longer hides the root. It changes no Phase 4 number.
  - New model §10 (10a–10k) with every reviewer variant.

**Plan**
- **L1, L3 and Plan C killed.** L4 is reduced to a $0 reopen watch. L2 is a contingent residual outside DD7.
- **The 29-day kill test is withdrawn.** Its tracks are rewritten as reopen gates K0, A′, B′, C1′, C2′, D and E (§10.0).
- **Kill criteria replaced (§11):** zero founder hours now; L2 only after DD6 fails and K0 passes; a stricter bank-purchase rule; no raise without A′, B′ and a co-founder.
- **Corrections to the text:**
  - "Locked die" (§1, VET-02).
  - The MCM fit, 125 °C and qualification-standard description (§1, PHY-01/-02, VET-06).
  - FTO #4 (§6) and MIL-PRF-38534 (§7).
  - The demand "ceiling" is now stated as a fee pool (HYP-07, VC-05).
  - 3D Plus is added as an MCM competitor.
  - Micross is recorded as a direct L1 competitor (EDSP), not a white-label partner.

### 14.3 Revised headline economics (model §4–§6, §10)

| Scenario | Residual Plan A (L2 only) ARR m18 | ARR m36 | Breakeven (founder unpaid) | Founder full-time | Cash low / below $20k | Bank m20 unit GM / IRR | MCM GM m36 | Plan B EV / capital |
|---|---|---|---|---|---|---|---|---|
| BASE | **$4,956** | **$8,606** | never | never | $15.4k (m36) / m22 | −12.8% / −26.6% (not bought) | 26.7% | **0.29×** of $11.49M |
| GLUT | $2,010 | $4,389 | never | never | $10.2k (m36) / m22 | −109.2% / −99.4% (not bought) | 32.4% | 0.24× of $11.64M |
| SEVERE | $1,869 | $928 | never | never | $7.0k (m36) / m22 | −685.1% / n/a (not bought) | 39.2% | 0.19× of $11.77M |

Phase 4 for comparison: Plan A (L1 + L2) $22.0k / $42.6k BASE; bank 39.6% / 2.6%; MCM GM 52.2% at m36; Plan B 0.46× of $8.11M.

- **The residual L2 line:**
  - A lean $300/month set-up breaks even at m15 (BASE) but never pays the founder.
  - A 3% commission gives $5.2k of m36 ARR; 0.20 accounts a month gives $5.7k.
  - Probability-weighted at p(rep offer) = 0.25, it is ~$2.2k.
- **L1 as a what-if** (Phase 4 inputs): p_program 0.10 alone cuts Plan A m36 ARR to $18.3k. Adding CUI or AS9120B cost takes cash to −$3.7k / −$3.2k (−$40.5k combined).

### 14.4 Revised verdicts

- **POSSIBLE: Only for incumbents.** Bare-die storage for 10–20 years is TRL 6–7, and the MCM as described does not fit its package. A 125 °C rating needs a per-die bin and a refresh derate, and an unauthorized re-packaged die cannot serve DO-254 or FDA locks.
- **PROFITABLE: No.**
  - L1 costs the buyer 2.9–5.4× a packaged LTB.
  - The bank loses money at every purchase date and scenario.
  - Plan B returns 0.29× of $11.49M in BASE, and the BULL case is ~22% a year gross over 10 years before dilution.
  - The residual rep line never breaks even at the Phase 4 cost base.
- **DOABLE BY THIS FOUNDER: No.**
  - The only founder-sized line (L1) has no rational buyer.
  - DoD and defense routes need ~$35k of compliance each, and either one breaks the cash floor.
  - Any hours diverted from DD6, round 2's PRIMARY candidate, delay it. (DD6 was killed by the same red team; the Phase 6 PRIMARY is DD2, `research/phase6/decision.json`.)

### 14.5 FINAL STATUS: KILLED

**Reason.** No objection was refuted.
- **L1.** The three FATALs, confirmed by the model, kill the managed die-bank program, the only line this founder could run. Banking bare die costs a board OEM $186k–347k to manage ~$52k of die, against ~$64k for a packaged LTB with dry storage. Board OEMs qualify packaged part numbers, and Micross sells the whole bundle direct.
- **L3.** The completed pull-cost stack kills the title-taking bank. Bare-die storage yield and surveillance, whole-wafer pulls and a 2.0× blended multiple make it worse: no bank is bought in any scenario, and IRR break-even needs ≤$1.53/die.
- **Plan C.** It fails on founder constraints.
- **L4.** The MCM survives only as a capital-heavy option that must first be redesigned, returning 0.29× of $11.49M.
- **The moat.** OCM authorized-aftermarket rights were never tested, and the OCMs that would talk are extending their legacy lines.
- **What is left.** L2 rep commissions ($8.6k BASE m36 ARR) are not this concept, do not cover their own fixed costs and would take hours from DD6.

**Role: DROP.** It is not a MOONSHOT, FALLBACK or side line. Do not run the 29-day test. The only residue, at $0, is the §10.0 reopen watch and one paragraph of packaged-part dry-storage advice inside DD2's LTB study.

**Phase 4 verdicts, kept for the record:**
- **POSSIBLE:** Yes (TRL 9), with no published 10+ year DRAM die yield data and no −55 to 125 °C or radiation data for entrant KGD.
- **PROFITABLE:** For incumbents yes, for an entrant no. Plan B was 0.46× of $8.11M; the bank earned 2.6% IRR bought in BASE at m20 and −32.8% in GLUT; ≥3× needed ~4 MCM design-ins a year of ~1,000 units; DRAM alone was a $2–27M a year business.
- **DOABLE:** Only the wedge, and the wedge was a side line: $42.6k recurring ARR at m36 in BASE, never paying the founder.
- **Status going into the red team:** SIDE LINE (optional SKU of DD2's LTB study line).
