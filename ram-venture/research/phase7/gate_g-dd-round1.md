# Phase 7 gate: round-1 deep dives (agent `g-dd-round1`, 2026-11-01)

**Slice:** `04_DEEPDIVES/provenance-recert.md` (DD1), `lifecycle-intel.md` (DD2), `nv-continuity-modules.md` (DD3), `memory-efficiency.md` (DD4), `open-memory-ip.md` (DD5).

**Method.**
1. Re-ran every model: `python3 models/<slug>.py`. All five exit 0. Each output matches the saved `research/phase4/<slug>_model_output.md` apart from its markdown wrapper.
2. Recovered the Phase 4 outputs from git (first commit of each output file, `0ee8f09`) to check the "Phase 4 / was" columns.
3. Ran the models' own functions where a number in the text is not printed in the output:
   - `P_PHASE4` / `--phase4` / `phase4_inputs()` runs;
   - year-by-year nets;
   - variant overrides.
4. Compared every §14 disposition and severity row with `research/phase5/responses_<slug>.json` and `rt_*.json` (scripted).
5. Checked the §0 score tables against `scores.csv`.
6. Checked that FINAL STATUS in §0 and §14 agrees with the JSON `final_status`.

No WebSearch was used, so there is no sources log.

## Numbers checked: ~1,150, plus 127 disposition rows

Each count below covers §0, §2, §12 and §14, plus spot checks in §8, §10 and §11.

| DD | Numbers checked | §14 rows checked vs JSON | FINAL STATUS §0 / §14 / JSON |
|---|---|---|---|
| DD1 provenance-recert | ~250 | 28 (3 FATAL / 18 MAJOR / 7 MINOR; 7 KILL / 16 DOWNGRADE / 5 MITIGATED) | KILLED / KILLED / KILLED |
| DD2 lifecycle-intel | ~180 | 24 (1 / 14 / 9; 2 / 15 / 7) | DOWNGRADED / DOWNGRADED / DOWNGRADED |
| DD3 nv-continuity-modules | ~235 | 25 (0 / 15 / 10; 3 / 14 / 8) | KILLED / KILLED / KILLED |
| DD4 memory-efficiency | ~235 | 24 (1 / 17 / 6; 4 / 15 / 5) | KILLED / KILLED / KILLED |
| DD5 open-memory-ip | ~245 | 26 (2 / 17 / 7; 7 / 16 / 3) | DOWNGRADED / DOWNGRADED / DOWNGRADED |

- **Objection counts.** The round-1 `rt_*.json` files hold 127 objections, which equals 28 + 24 + 25 + 24 + 26.
- **Dispositions and severities.** Every disposition and severity in the five §14 tables matches the JSON. No objection is missing from any table.
- **Scores.** Every §0 score and rank matches `scores.csv` (40 scored concepts), including the DD3 sub-scores.

## Fixes (10, all surgical)

1. **DD1 §2.2.** "only 356 recert modules sold" changed to **355**, to match model §3 ("recert modules sold 355").
2. **DD1 §10, Stage 1 decision table (C′ fails row).** The old text said recert "adds ~$71k of cumulative EBITDA". $71,494 is the cumulative EBITDA of the whole *bundle* at a 0.62 buy (m§5), not what recert adds. Recert + PMem alone at 0.62 earn **$60,097** (re-run `simulate('BASE', dict(P0, buy_frac=0.62), lines=('recert','pmem'))`). The text now gives both.
3. **DD1 §12.**
   - The Phase 4 sub-blocks are now labelled **"(Phase 4, superseded)"**: GLUT, SEVERE, cash at m36 by configuration, and the Verdict.
   - The stale "(§2.6)" pointer for the $268,513 / $203,455 / $115,358 Phase 4 variants is replaced with the `P_PHASE4` re-run that reproduces them. All three values were verified (turn-early full-time m31).
4. **DD2 §2.4.** The $1M-ARR line now reads ~**238** accounts and **7.9%** of the market (was ~235 and 7.8%). The $2M line reads ~**478** accounts (was ~476). Source: model §8. This is the open item in `OPEN_QUESTIONS.md` §8 #6.
5. **DD2 §14.1, RT-VC-DD2-04 row.** "7.8% penetration" changed to **7.9%** (model §8).
6. **DD2 §14.2.**
   - The text says "model §10 shows 29 scenario runs". The Phase 7 gate g-decision-docs has since appended 8 PLAN-variant rows to `models/lifecycle-intel.py`, so §10 now has 37 rows.
   - The text now notes this. BASE and model sections 0–9 were re-run and are identical.
7. **DD3 §2.3.** "about $6 per part-time hour in year 3" had no basis. It now carries [ESTIMATE: ~$365/month model net ÷ ~65 founder-hours/month at ~15 h/week, A-03].
8. **DD5 §2.4.**
   - The old text said "about $7k a month of gross profit".
   - It now says **$8.0k** gross profit at m36 (model §5), or ~$6.9k after the $1.1k monthly opex.
9. **DD5 §11 #12.**
   - The old text gave "(model: $7.6k)", which is the m30 GP alone.
   - The criterion tests trailing-3-month GP, which averages **$7.5k** over m28–m30 ($7,475, re-run). The text now says so.
10. **DD5 §14.5, EV correction note.**
    - **The error.** The "+$5–15k" EV multiplies p by $88.4k of end cash, and that end cash includes the founder's own $40k.
    - **The corrected gain.** If the test passes, the gain is $48.4k in BASE ($88.4k − $40k; the $9.1k test is already inside it).
    - **The corrected EV.** At the same 15–25% pass probability, EV is about **−$0.5k to +$5.3k** [ESTIMATE: p × $48.4k − (1 − p) × $9.1k].
    - **Cross-check.** J-INT (`research/phase6/judge_integrity.json`) puts it at about −$4k to +$1k. This closes `OPEN_QUESTIONS.md` §8 #8.

**Verified unchanged** (selected): every §0 / §2 / §12 / §14 headline figure in all five deep dives, including:
- **DD1:** $58,335 / $23,270 / −$3,473 / never; both-pass $226,833 at m32.
- **DD2:** $69,915 / $149,629 / m17 / never / $6,100 at m16.
- **DD3:** $29.4k / $39.9k / −$29.8k / −$9.2k at m13 / m19; year nets −$33.5k / −$0.6k / +$4.4k.
- **DD4:** $1.66 per node; $3.8k / $7.1k; −$95.7k; cash below $0 from M12.
- **DD5:** $41.2k / $65.7k / $4.0k at m15 / m12 / never.
- Every Phase 4 comparison value, checked against the git Phase 4 outputs.

## Unresolved (3; all outside a surgical fix in this slice)

1. **The RT-VC-DD2-04 response record still quotes the old values.** `research/phase5/responses_lifecycle-intel.json` and its compiled copy in `05_REDTEAM.md` (line ~498) say "~235 accounts, 7.8% … ~476 accounts". The model gives ~238 / 7.9% / ~478.
   - **Why not fixed:** that file is the verbatim Phase 5 record, and `05_REDTEAM.md` is outside this slice.
   - **Suggested fix:** the owner of `05_REDTEAM.md` adds a footnote. Only the deep dive was corrected here.
2. **The DD5 ev_note keeps the uncorrected EV.** `research/phase5/responses_open-memory-ip.json` still says "+$5–15k". It is left verbatim as the Phase 5 record; the deep dive now carries the correction (fix 10).
3. **The DD5 calendar is not re-dated** (`OPEN_QUESTIONS.md` §8 #4).
   - DD5 §10–§11 and `models/open-memory-ip.py` assume the kill test runs 2026-11-02 → 12-01, with m1 = Dec-2026.
   - Phase 6 sequences DD5 after DD2.
   - The DD5 header's Phase 6 note already says the paid steps shift ~2 months. Re-dating the model is a modelling change, not a surgical number fix.

**Out-of-slice follow-up:** `OPEN_QUESTIONS.md` §8 items #6 (LI accounts row) and #8 (DD5 EV) are now fixed in the deep dives, and their owner may mark them closed.

**Gate script:** `python3 research/tools/gate_check.py` was re-run after the fixes and printed **GATE: PASS** (G1–G9).
