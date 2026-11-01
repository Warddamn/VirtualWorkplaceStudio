# Phase 7 gate — g-decision-docs (decision docs slice)

As of 2026-11-01. Slice: `INVESTOR_MEMO.md`, `FIRST_90_DAYS.md`, `OPEN_QUESTIONS.md`, `research/phase6/decision.json`, plus `models/lifecycle-intel.py` and `research/phase4/lifecycle-intel_model_output.md`, which the first task required. WebSearch used: 0. No new sources were needed.

## Numbers checked

- **1,788 numeric tokens** were matched by script against the model outputs (LI.py, OM.py, both re-run with exit 0), the deep dives, decision.json, the judge files, 01_LANDSCAPE, SUMMARY_TABLE, 03_SCORING, the phase 4 notes, the phase 1 verify files and the phase 5 JSON. By file: memo 128, 90-days 801, open-questions 757, decision.json 102.
  - 45 tokens in FIRST_90_DAYS are running totals for spend, cash left and hours. They were re-added by hand from their cited line items and all are correct. Spend: $500 + $300 + $400 + $500 + $250 = $1,950. Branch A totals follow the model's PLAN m1/m2 cash ($37,400 / $36,750; A2 $36,400 / $30,750). Branch B totals follow OM §10's tranches.
  - 2 tokens in OPEN_QUESTIONS are not model values: "FAR 25.003" is a clause number, and "$201,001" is a historical drift value quoted as resolved.
- **About 75 key figures were checked by hand in context:** counts (98 concepts, 83 killed, 15 alive, 186 objections, 0 refuted, 5 killed and 2 downgraded, all from concepts_master.json, research/phase5/*.json and summary.md), every DD2/DD5 economics figure, all gates, thresholds, dates and budgets, the judge odds and confidences, and the LAND §0 facts.

## Fixes

1. **`models/lifecycle-intel.py`.**
   - Added inputs `kill_test_spend` (BASE 0) and `kill_test_month` (m1).
   - Added three section-10 rows: "PLAN (Phase 6 decision)", "PLAN + index option passes" and "PLAN, K5 fail".
   - Added a closing table of max founder draw against the $34k cap and cash low against the $5k floor.
   - BASE and every earlier row are unchanged (diffed). The script exits 0, and `research/phase4/lifecycle-intel_model_output.md` was regenerated and matches the run.
   - Results:

     | Run | Max draw | Cash low |
     |---|---|---|
     | PLAN BASE | $30,850 | $9,150 @ m16 |
     | PLAN GLUT | $30,216 | $9,784 |
     | PLAN SEVERE | $29,888 | $10,112 |
     | PLAN + index option passes, BASE | $36,850 (over the cap) | $3,150 (under the floor) |
     | PLAN, K5 fail, BASE | $36,003 | $3,997 @ m22 |

2. **decision.json.** Added `PRIMARY.plan_cash` with the PLAN figures. Added Supplyframe to the m18 exit-talk list in `post_pass_gates`, to match LI §11 #12. The picks are unchanged (asserted).
3. **INVESTOR_MEMO.md.**
   - Cash-low row → PLAN figures.
   - "$33,900 draw" → $30,850 against the $34k cap and $9,150 against the $5k floor, plus the index-pass case ($36,850 / $3,150).
   - Planned test spend "~$2,950" → "~$1,950 (~$2,950 if the consult is not deferred)".
   - Risk 4: the K5-fail cash low $947 → $3,997 on the plan.
   - Downside sensitivities labelled BASE.
   - K3 wording → "≥2 of 10 signed LOIs".
   - Added citations for the $3,500 LTB study and for the m6 / m17 timing.
   - Trimmed to 1,145 words outside the header box. Another agent's Insight edit had pushed it to 1,171.
4. **FIRST_90_DAYS.md.**
   - §0 now opens with the <$10k kill experiment, its gates and its dates.
   - §1: the budget row and a plan-cash row.
   - §0: DD2's draw → $30,850.
   - Week 7 and §3.2 #4: the K5-fail cash low → $3,997.
   - §6: A1 and A2 now carry model figures.
   - §9: the A1, A2 and K5 rows → LI.py §10 values, replacing the [ESTIMATE] figures ~$9.2k, ~$3,150 and ~$36.9k. The trough is labelled BASE.
   - §8: C-48 re-quoted verbatim from the current DEC (the stale "2 concurrent" quote is gone), and a C-72 watch row added because DEC lists it.
   - §10: items 1, 2 and 9 marked resolved.
5. **OPEN_QUESTIONS.md.**
   - Added a BASE-vs-PLAN note.
   - Rank 2: budget. Rank 3, P2 and §7.1: the K5-fail cash low on the plan.
   - Rank 4 and F1: the test (iv) deadline aligned to OMI §11 #1 (answer requested by 2026-11-20; silence by 2026-12-01 = FAIL).
   - §1: the K6 date, and the first-revenue pointer changed from LI.py §6 to §4.
   - **§1: the m12 gate changed from "or" to "and, missing either stops", a threshold error.**
   - P6 and §7.1: the antitrust deferral now cites the PLAN rows instead of "~$11k [ESTIMATE]".
   - C-48 source; C-72 call timing aligned to week 3; the $13–19k source pointer.
   - §8: items 5 and 6 marked resolved.
6. **`research/assumptions/g-decision-docs.md`.** Logged four modelling assumptions: m1 booking, seeds = 0 in PLAN, the index-pass charges, and the draw definition.

`python3 research/tools/gate_check.py` → GATE: PASS (all 10 models exit 0).

## Unresolved (5)

1. **LI deep dive, outside this slice.**
   - §10 headlines "Budget ≈ $2,950". §4 and §8 book the $5k opinion at m2 unconditionally. §11 #4 and #10 quote BASE cash lows ($947; $6,100 at m16).
   - These are correct as BASE but not plan-accurate. The slice docs quote both, with labels. Not edited because it is another agent's file.
2. **"PLAN + index option passes" breaks the $34k cap and the $5k floor in BASE, GLUT and SEVERE.**
   - This is a real finding, not a document error. It is stated in all four docs.
   - The decision does not say how the $6k would be funded if K3+K4 pass. The cap and floor still bind.
3. **The DD5 calendar is out of date.** OMI §10–§11 and OM.py assume a November test, but as FALLBACK it runs Jan–Feb 2027. It needs re-dating and a model re-run before any DD5 spend. It is flagged in DEC `timing_note`, FIRST_90_DAYS §10 #7 and OPEN_QUESTIONS §8 #4. The model is outside this slice, and the picks are unaffected.
4. **Two judge files misstate the m12 gate.** J-EV and J-INT write it as "≥5 accounts or MRR ≥$1,700". These are historical judge records and were left unedited. The slice docs use LI §11 #9.
5. **Sensitivity rows stay on BASE.** The LI.py §7 rows (price and conversion ×0.7) are quoted as BASE. PLAN versions were not computed, so they are labelled BASE rather than shifted.
