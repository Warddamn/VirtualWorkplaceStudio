# Phase 7 gate — round-2 deep dives (DD6, DD7) and the 05_REDTEAM narrative summary

Agent: `g-dd-round2-redteam` · 2026-11-01 · WebSearch used: 0 of 3 · No git commit.

## Method

- Re-ran `models/private-moe-appliance.py` and `models/legacy-dram-diebank.py` (exit 0). Compared every §0, §2, §12 and §14 number with the current output.
- Re-ran both models on their Phase 4 inputs: DD6 `run_with(P_PHASE4)`, and DD7 with `INPUTS = INPUTS_P4`, output kept in scratch only. This checks the "(Phase 4)" figures the deep dives keep for the record.
- Computed the unprinted figures directly from the model functions: kill-test GLUT/SEVERE, subscription share of revenue, LTV/CAC, the DD6 founder-hours check, exact residual ARR and the pull-yield IRR effect.
- Compared §14 objection tables with `research/phase5/rt2_*.json` (severity) and `responses_<slug>.json` (disposition). Checked final statuses against the JSON, `concepts_master.json` (C-48, C-65, C-91) and the 05_REDTEAM scoreboard.
- Checked every count and ARR figure in `research/phase5/summary.md` against `research/phase5/*.json`, the seven model outputs, `decision.json` and `concepts_master.json`.
- Ran an automated verbatim scan of every multi-digit number in both deep dives against the model outputs, the Phase 4 re-runs, the red-team JSON and SOURCES.md. It checked 1,551 tokens and flagged 29; each flag was resolved by hand: source-cited, rounding, arithmetic, or one of the fixes below.

## Numbers checked

| Scope | Checked by hand | Result |
|---|---|---|
| DD6 `private-moe-appliance.md`: §0, §2.1–2.6, §12, §14, plus model-derived figures in §1, §4, §8–§11 | ~150 | 10 fixes |
| DD7 `legacy-dram-diebank.md`: §0, §2.1–2.7, §12, §14, plus model-derived figures in §1, §3, §7–§11 | ~160 | 7 fixes (3 of them one stale claim in three places) |
| `research/phase5/summary.md` (05_REDTEAM narrative) | 45 (7 counts, 9 ARR figures, 29 other figures) | 2 fixes |
| **Total** | **~355** | |

**Confirmed matches:**
- §14 tables: all 32 DD6 rows and all 27 DD7 rows match the JSON severity and disposition. DD6: 1/19/12 by severity; 5 kill, 17 downgrade, 10 mitigated, 0 refuted. DD7: 3/12/12; 5 kill, 18 downgrade, 4 mitigated, 0 refuted. Statuses are KILLED everywhere.
- Summary counts: 186 = 127 + 59; 11 FATAL, 112 MAJOR, 63 MINOR; 0 refuted, 42 mitigated, 111 downgraded, 33 killed; five killed and two downgraded; 11 = 15 alive − 4 deep-dived.
- Summary ARR figures, each matching `revised_economics` and the model output: $58,335, $149,629, $39,890 ($2.7k recurring), $7,098, $65,678 ($164.1k run-rate), $63,873, $8,606.

## Fixes

**DD6 `04_DEEPDIVES/private-moe-appliance.md`**
1. §2: the Phase 4 64 GB RDIMM price was $1,898; the model gives $1,897 (64 × $29.648).
2. §2.4: the subscription-share row (17.0 / 21.1 / 24.2%) is not printed by the model. Tagged [ESTIMATE] with its basis (computed and correct).
3. §2.5: "$109,172 drop L" tagged with its run basis. §14.4 now points to §2.5.
4. §4: the channel bullet quoted Phase 4 terms and results (10%/15%, 3 a month, −44%, m30) unlabeled. They are now labeled Phase 4, and the Phase 5 terms and result are added: 15%/20%, 2 a month, $52,843 (−17%) and −$42,858 (model §7).
5. §9 team table: stale Phase 4 values are updated to the current model. Full-time is never (was m23). Support is a $500/month retainer with 0 contractor hours (was 24.5 h). Insurance is $900 (was $500). Partners take 15%/20% (was 10%/15%). The fleet is 8.2 boxes at m36 (was 22.3).
6. §12 table: the BASE L-box column was labeled "Jan-2028 quote", but $62,525, $12,105 and $40,366 are Nov-2026 values (Jan-2028 BASE would be $61,283). The label is fixed and the table's Phase 4 provenance is stated. A current-model (Phase 5) line is added: $78,708 / $36,752 / $26,240; GP $13,500 / $6,090 / $4,234; ARR and net from model §5.
7. §12: "23–28%" subscription share tagged [ESTIMATE] (Phase 4 run, verified at 23.1 / 27.8%).
8. §14.2: the kill-test GLUT and SEVERE cells ($93,260 / +$14,411; $96,299 / +$15,095) are verified but not printed. Tagged.
9. §1 SKU table: added the revised S GPU (RTX PRO 5000 48GB, $8,216) and the L 832 GB purchase. Pointed the S TTFT to model §2.
10. §10: the $9,500 hard cap had no trace. Tagged [ESTIMATE] (under the <$10k ceiling, notes §13); the ~$7k budget traces to the notes and the JSON `ev_note`.

**DD7 `04_DEEPDIVES/legacy-dram-diebank.md`**
11. §0, §10 and §14.1 (RT-VC-DD7-03) claimed "10 h/month diverted moves DD6 full-time m23→m33 (model §10h)". Model §10h now prints full-time **never** at 65 / 55 / 45 h, with m36 ARR $63.9k / $56.2k / $45.3k, because DD6's own red team revised its inputs. All three places now state the current figures and keep m23→m33 labeled as DD6 Phase 4, which was reproduced via `run_with(P_PHASE4)`: m23, m33 / $145,428, never / $122,847.
12. §2 note: stated where the Phase 4 table cells come from. Model §10a/d/e/g print the headline figures; every other cell matched an `INPUTS_P4` re-run.
13. §2.5: "BASE buys one at m20 (model §5)" pointed to the wrong place, since model §5 now buys no bank. Relabeled Phase 4 and pointed to model §10g.
14. §7: "qualification inside the $1.4M NRE" contradicted the $1.6M line before it; fixed. "Do not raise: 0.46×" became 0.29× of $11.49M (Phase 4: 0.46×).
15. §8: "a bank bought at the 2026–27 peak returns 6.5% at best (model §3)" is Phase 4. Added the revised −16.5% that model §3 now prints.
16. §9: "(in the $8.5k one-off)" became the $3,900 month-1 one-off (Phase 4: $8.5k).
17. §1 diagram: labeled Phase 4, with the revised L3 inputs (17 × 736 die, 2.0×) and the killed legs noted.

**Research files**
18. `research/phase4/legacy-dram-diebank_model_output.md`: the code block was stale in §10h ($67.6k / $59.7k / $48.2k). It is refreshed from a fresh run, now identical to the current output, with a dated note. The DD6 output file already matched a fresh run.
19. `research/phase5/responses_legacy-dram-diebank.json`: corrected the DD6 founder-hours claim in `revised_verdicts.doable`, in `ev_note`, and in the RT-VC-DD7-03 response, which gets a dated gate note and keeps the original text. JSON validated.
20. `research/phase5/summary.md`:
    - The PRIMARY test spend "~$2,950" now reads "~$1,950 planned (~$2,950 if the deferred $1,000 consult is spent)", per `decision.json` PRIMARY.spend.
    - "The only one a glut helps" is qualified with the DD6 deep dive's finding: GLUT $66,969 vs BASE $63,873.
    - `05_REDTEAM.md` was regenerated with `compile_redteam.py` (186 objections, 0 unanswered).

## Unresolved

None.

Caveat: several Phase 4 "for the record" figures trace only to a re-run of each model on its Phase 4 inputs. Examples are DD6 §8 and §12 and the DD7 Phase 4 tables. The current output files do not print them. They are verified and tagged as such, but not printed.

`python3 research/tools/gate_check.py` → **GATE: PASS** (run after the fixes).
