# Phase 7 gate — final consistency critic (`p7-critic`)

As of 2026-11-01. Fresh-eyes cross-document pass over: `research/CONVENTIONS.md`; `01_LANDSCAPE.md` §0 and "What changed in Phase 1b"; the `02_CONCEPTS.md` header; `03_SCORING.md` §0, §7 and §9; §0 and §14 of all seven deep dives (plus DD2 §8, §10–§12 and DD5 §10–§11 as the source of truth for gates); `05_REDTEAM.md` summary and scoreboard; `FIRST_90_DAYS.md`; `OPEN_QUESTIONS.md`; `SUMMARY_TABLE.md`; the `ASSUMPTIONS.md` framing table; `research/phase6/decision.json`. `INVESTOR_MEMO.md` was read only, because another editor was working on it. WebSearch: 0. No sources were added.

## What was checked and matched (no edit needed)

- **Picks and labels.** PRIMARY DD2 (C-80, C-29, C-61), FALLBACK DD5 (C-33) and MOONSHOT "NONE; C-86 held as a ~$0 option" match across DEC, SUMMARY_TABLE (generated from DEC), the memo, FIRST_90_DAYS, OPEN_QUESTIONS, 05_REDTEAM and the DD2/DD5 header notes. All three judge files give the same picks. Confidences are 0.2–0.45 and 0.2–0.3, as DEC states.
- **Final statuses.** DD1 KILLED, DD2 DOWNGRADED, DD3 KILLED, DD4 KILLED, DD5 DOWNGRADED, DD6 KILLED and DD7 KILLED. Each deep dive's §0/header and §14 agree with the 05_REDTEAM scoreboard. Per-DD objection counts and severity/disposition tallies also match: 28/24/25/24/26/32/27 = 186, with 11 FATAL, 112 MAJOR and 63 MINOR, and 0 refuted, 42 mitigated, 111 downgraded, 33 killed.
- **Deck.** $1.48 / $20.37 / $8.15 / $2.04 per GB holds in LAND §0, §4.3 and §5.3, the 03_SCORING appendix, every model header and the deep-dive cycle tests. The pre-1b deck ($15.99 / $6.40 / $1.64) appears only where it is labeled pre-1b or as kill-reason history.
- **DD2.** ARR $69,915 / $149,629, GLUT $104,077 and SEVERE $83,031. Plan draw $30,850, cash low $9,150 @ m16; GLUT $9,784, SEVERE $10,112; index-pass $36,850 / $3,150; K5-fail $3,997 @ m22. All of these match `models/lifecycle-intel.py` (re-run, exit 0).
- **DD5.** ARR $41.2k / $65.7k, GLUT $54.9k, SEVERE $49.3k, breakeven m12 and cash low $4.0k @ m15. All match `models/open-memory-ip.py` (re-run, exit 0).
- **Counts** (concepts.csv and the phase-5 JSON): 98 concepts, 58 kill-pass kills, 40 scored, 9 SCORE<55 kills, 15 RED-TEAM kills + C-72 = 83 killed, 15 alive. The 15 red-team ids listed in 03_SCORING §0 match the CSV. The SUMMARY_TABLE kill tally sums to 83. SOURCES lists 1,613 sources. 03_SCORING's Phase-3 counts (67 killed, 31 alive, 17 in deep dives) are labeled as a snapshot, so they are legitimate.
- **DD2 gates against LI §10–§11.** K0 2026-11-09. K6+K1 2026-12-01. K5 2026-12-15. m9 2027-08-31: ≥2 paying accounts. m12 2027-11-30: ≥5 accounts AND MRR ≥$1,700. m18: ≥13 accounts or exit talks with all five named buyers. m24: ARR ≥$78k. FIRST_90_DAYS' ~60 h, against LI's ~55 h, is explained in the plan as including the DD5 letters, so it is not a conflict.
- **DD5 gates against OMI §10–§11.** Tests (i)–(iv), the $9.1k budget and its tranche split ($1.6k + $6.0k + ≤$1.5k) all match. The Jan–Feb 2027 shift is stated in the OMI note, the DEC `timing_note` and FIRST_90_DAYS.
- **Pronouns.** No gendered founder pronouns in any deliverable (gate G8 also passes).
- **Generated files.** All five generators were re-run in a scratch copy, then in place. 02_CONCEPTS.md, concepts.csv, SUMMARY_TABLE.md, 05_REDTEAM.md, SOURCES.md and the ASSUMPTIONS agent section reproduce byte for byte, so no generated file carries hand edits.

## Contradictions found and fixed (7)

1. **The severe line in `01_LANDSCAPE.md` §10.3 rule 1 read "$1.60/GB"**, while §4.3, §5.3 and the canonical deck (`ddr5_reference()`; 03_SCORING appendix) use $2.04. It now reads $2.04 (−90%), with the 2023 trough (~$1.60 DDR5 [UNVERIFIED], $1.30 DDR4) as the lower bracket.
2. **The DD2 role and plan conflicted with DEC** (`04_DEEPDIVES/lifecycle-intel.md` header note).
   - **Role.** The note covered only §14. §0 ("run the ~$2,950 kill test only alongside DD1/DD3") and §8 ("die-level referral to DD1") also contradict DEC. The note now covers §0, §8 and §14, and says DD2 runs alone.
   - **Plan spend and cash.** A paragraph now reconciles the §10 budget of ~$2,950 with DEC's planned ~$1,950 (the consult and the $5k opinion are deferred, under the funding rule). It gives the plan cash ($30,850 / $9,150; K5-fail $3,997), sets DEC's ≤$34k draw cap against §11 #10's "no more than the $40k", and keeps the BASE figures labeled. §10–§11 thresholds are unchanged.
   - **C-72.** The note claimed C-72 survives "only" as three calls, but §0, §8 and §12 keep an unpriced pooled-forecast feature. The note now says so.
3. **DD5's role conflicted with DEC.** The header note covered only §14, but §0's "Not a PRIMARY, and not a FALLBACK either" also contradicts DEC. The note now covers §0 too.
4. **DD7 still called DD6 "the PRIMARY"** (§14.4 "Any hours diverted from DD6 delay the PRIMARY"; §0 "hours that DD6 needs"). DD6 is killed and the PRIMARY is DD2 (DEC). Both lines now say "round 2's PRIMARY candidate", note that DD6 was killed, and name DD2 as the Phase 6 PRIMARY.
5. **A2 left out DEC's funding rule in `FIRST_90_DAYS.md`.** The §5 decision chart, the §6 A2 definition, the §1 deferral rule and the §9 A2 row all spent the deferred $6k on a K3+K4 pass alone. DEC `MOONSHOT.funding_rule` also requires ≥$6k of index prepayments or a ≤$10k note. All four places now carry the rule, and the §9 A2 figures are marked gross. §10 item 3 is marked resolved.
6. **P6 and M3 in `OPEN_QUESTIONS.md` had the same omission.** Both now cite `funding_rule`. §8 items 7 and 8 are marked resolved; item 8 cites OMI §14.5's correction note.
7. **The revision to A-06 in the `ASSUMPTIONS.md` framing table was not recorded.** A-06 said "Phase 1 revises this" without saying how. The Phase 1 house call is now noted: peak 4Q26–2Q27, plateau through 2027, turn in 2028 (LAND §2.3).

## Left as is (with reason)

- **The DD5 calendar** (OMI §10–§11 and OM.py assume a November test). Re-dating needs a model re-run, which is beyond a surgical fix. The shift is disclosed in the OMI note, DEC and FIRST_90_DAYS, and it changes no pick.
- **Two judge files misstate the m12 gate as "or"** (J-EV, J-INT). They are historical judge records. Every deliverable uses LI §11 #9 ("and"; missing either stops the build).
- **Verbatim Phase 5 records** in 05_REDTEAM and `responses_*.json` (e.g., "30-day kill test", "not a PRIMARY" verdicts, the RT-VC-DD2-04 "~235 accounts"). They are the record. 05_REDTEAM's summary already says these predate round 2.
- **INVESTOR_MEMO.md.** It was not edited, by instruction. On read it agrees with every figure and gate above, and it already carries the funding rule.

`python3 research/tools/gate_check.py` → **GATE: PASS** (G1–G9, run after all edits: 10 models exit 0, 186/186 objections answered, 1,613 sources, 15 alive and 83 killed).
