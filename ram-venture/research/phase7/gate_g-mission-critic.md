# Phase 7 gate — mission completeness critic (`g-mission-critic`)

As of 2026-11-01. Scope: `research/MISSION_PROMPT.md` checked line by line against the repo. No web searches were used (quota 3, 0 spent), so no sources file was written. `python3 research/tools/gate_check.py` printed **GATE: PASS** before and after these edits.

## Numbers checked: 707

| Block | Count | Result |
|---|---|---|
| Study counts (98 concepts, 102 raw cards, 4 merges, 83 killed, 15 alive, 40 scored, 58 pre-score kills, 9 SCORE<55 kills, Phase-3 67 killed / 31 alive) vs `concepts_master.json`, `concepts.csv`, `scores.csv` | 10 | match |
| Branch card counts A 43 / B 14 / C 15 / D 12 / E 14 (02_CONCEPTS headers vs master) | 5 | match |
| SUMMARY_TABLE kill tally (10 rules) vs master `kill_rule` | 10 | match |
| Red team: 186 / 127 / 59 objections; severity 11 / 112 / 63; dispositions 42 / 111 / 33, 0 refuted; 28 persona × deep-dive cells all > 0 (`research/phase5/rt*.json`, `responses_*.json`) | 36 | match |
| SUMMARY_TABLE: 15 rows × 3 weighted totals + 3 ranks vs `scores.csv`; 15 rows × tier, TRL, TTR, GM, glut vs `concepts.csv` | 165 | match |
| `scores.csv`: 40 concepts × 10 criteria, score in 1–5 and a non-empty one-line `*_why` | 400 | all present |
| Device model (`models/device_cost_compare.py`, re-run, exit 0): DDR5 live deck 1.484 / 20.367 / 8.147 / 2.037; pre-1b deck 1.641 / 15.993 / 6.397; C-04 $8.50, 5.73×, 1.04×; C-59 $4.12; C-26 $2.06; C-09 $14.8; MRAM $821 ratios 51× / 128× / 40× / 101×; C-03 ~$266; C-38 40–100× | 22 | match after fixes 4 and 6 |
| Rule 5 sense counts (27 / 20 / 49 / 23) and survivor senses | 5 | computed from master |
| §3E lens counts among survivors | 8 | computed from master |
| INVESTOR_MEMO model figures vs `models/lifecycle-intel.py` (re-run, exit 0): ARR m18/m36 all three scenarios, accounts 37/25/20, PLAN cash lows and draws, $69,289 / $3,997, 14.7%, $318,279, m33, −$11,109 / −$4,943, 238 / 7.9%, 57%, 3.3×, $5,774, $340, 14.2 | 25 | match |
| Deep-dive first-ten customer lists (7) and kill-test budget and duration (7 × 2) | 21 | present (see note on DD1) |

## Requirement checklist

| Mission requirement | Status | Evidence / action |
|---|---|---|
| §1 premise verified bullet by bullet with dated sources, re-aim stated | PASS | `01_LANDSCAPE.md` §1: 20 rows with verdicts and dated citations, plus the re-aim paragraph |
| Phase 0 `ASSUMPTIONS.md` kept updated | PASS | All 63 `research/assumptions/*.md` files are fully merged (bullet counts match per agent tag) |
| Phase 1 cost stack model | PASS | `models/dram_cost_stack.py` exits 0; `01_LANDSCAPE.md` §4 |
| Phase 1 price history 2024–now | PASS | §2.1 runs 1Q24 → 4Q26F; §2.2 has $/GB levels |
| Phase 1 demand / HBM allocation | PASS | §3 |
| Phase 1 U.S. capacity map (§3C list) | **FIXED** | Netlist was missing from the §6.1 table, so row 34 was added from `research/phase1/us_backend.md`, citing its 10-K and ARS. All other §3C names are present |
| Phase 1 funding programs | **FIXED** | §7.1 named only Sandia among the DOE labs, so a LANL / ORNL / LBNL pointer to `funding_export.md` §9.1 was added. CHIPS, NSTC, DMEA Trusted, DARPA, SBIR/STTR and state programs were already covered |
| Phase 1 export controls | PASS | §8 |
| Phase 1 patent landscape for every §3A technology | **FIXED** | §9.1 had no rows for glass-substrate memory or wafer-scale SRAM (Cerebras-style). Two rows were added, citing URLs already in `SOURCES.md` and pointing to C-03 / C-38 |
| Phase 2: ≥50 cards, ≥10 per branch | PASS | 98 cards; A 43, B 14, C 15, D 12, E 14 |
| Phase 2 card template fields | **FIXED** | All 98 cards carry every template field. Three cards held verify-instruction text instead of content: C-01 *What it is*, and *Why it could work* on C-04 and C-16 each read "Replace 'X' with 'Y'". The raw card text (`research/phase2/A1.json`, `A2.json`) was restored with the correction applied, in both `02_CONCEPTS.md` and `concepts_master.json` |
| Phase 2: no duplicate ideas | PASS | Dedup log: 4 merges, 4 DUPLICATE kills, separations justified |
| `concepts.csv` | PASS | 98 rows; status and tier match the master |
| §3A cost equation for every device concept, $/GB beside DDR5 today and in a glut | PASS | `device_cost_compare.py` covers every Branch-A device card (C-01–C-43 except service/data cards C-13, C-14, C-29) plus C-51, C-58, C-59, C-71. It has xcontract and xglut columns and maps C-52, C-53, C-70 and C-96 to reference rows |
| Rule 5: all three senses explored | **FIXED** (visibility) | Coverage was there (a 27, b 20, c 49 cards), but no deliverable stated it. Counts were added to the `02_CONCEPTS.md` legend |
| §3E business-model lenses applied to every survivor | **GAP** | See Unresolved 1. Coverage counts and a gap note were added to `02_CONCEPTS.md` |
| Phase 3: weights editable in `models/scoring.py` | PASS | `CRITERIA` / `WEIGHTINGS` dicts, documented "edit weights here" |
| Phase 3: three weightings with rank shifts | PASS | `03_SCORING.md` §5 and SUMMARY_TABLE |
| Phase 3: 1–5 with a one-line justification per criterion | PASS | `scores.csv` has 10 `*_why` columns, 400/400 filled |
| Phase 4: ≥1 T0/T1 and ≥1 T2+ | PASS | `03_SCORING.md` §7.7; DD7 (T2) and DD5 (T2 legs) |
| Phase 4 required sections (how it works … kill experiment, kill criteria) | PASS | All 7 deep dives have §0–§14. Each has a 10-entry first-customer list, a team (§9), a kill test (§10) and kill criteria (§11) |
| Phase 4 kill experiment < $10k and < 30 days | PASS (note) | PRIMARY DD2: $1,950 planned, ≤ $5k cap, 29 days. FALLBACK DD5: $9.1k, 2026-11-02 → 12-01. DD1's revised staged test is 29 days for Stage 1 but 60 days and $9.5k with Stage 2; DD1 is killed, so this is moot |
| Phase 4 `models/<slug>.py` ×5+ | PASS | 7 models, all exit 0 |
| Phase 5: four named personas, each attacks every deep dive | PASS | VET, VC, HYP, PHY; 28/28 persona × DD cells non-empty |
| Phase 5: every attack and response recorded verbatim; downgrades and kills | PASS | 186/186 answered (G3); 33 ACCEPTED-KILL, 111 downgrades |
| Phase 6: PRIMARY / FALLBACK / MOONSHOT | PASS (note) | MOONSHOT is "NONE honestly qualifies", with C-86 held as a labeled ~$0 option. This is an explicit, reasoned decision (Rule 10), and G9 accepts it |
| INVESTOR_MEMO headings, ≤ 2 pages | PASS (note) | All 9 headings present. ~1,300 words plus two tables is borderline for 2 pages (Unresolved 4) |
| FIRST_90_DAYS week by week, opening with the kill experiment | PASS | Weeks 1–5 are the DD2 kill test; then branches A, B and C week by week |
| OPEN_QUESTIONS | PASS | Present, ranked |
| SUMMARY_TABLE: every survivor, all three weightings | PASS | 15 rows; 165 numbers verified |
| Repo tree §6 | PASS | G1 |
| SOURCES.md with URL and access date | PASS | 1,613 sources, all with an Accessed column; G4 |
| Founder never "he/his" | **FIXED** | Deliverables were already clean (G8). 13 gendered references to the founder were left in research inputs and were changed to they/them: `research/phase1/funding_export.md` (2), `research/phase1/verify_v1-policy.md` (1), `research/phase2/A1.json` (2), `D.json` (3), `E.json` (5) |
| Phase 7 ten-line console summary | PENDING | This is the orchestrator's final step. Its inputs exist in `decision.json` (`biggest_unknown`, `monday_action`) |

## Fixes made (list)

1. `01_LANDSCAPE.md` §6.1: added row 34 (Netlist). It is in the mission §3C list but was absent from the capacity map. Source: Netlist 10-K FY2023 and ARS FY2025, both already in `SOURCES.md`.
2. `01_LANDSCAPE.md` §7.1, DOE-labs row: added a LANL (LANSCE single-event testing), ORNL and LBNL (user facilities, LEEP) pointer to `research/phase1/funding_export.md` §9.1, tagged [UNVERIFIED-M] as in the source.
3. `01_LANDSCAPE.md` §9.1: added patent-landscape rows for glass-substrate / display-fab oxide memory and for wafer-scale SRAM / SRAM-only accelerators. Both are §3A technologies; all cited URLs were already logged.
4. `02_CONCEPTS.md` and `research/phase2/concepts_master.json`: restored C-01 `what_it_is`, C-04 `why_it_could_work` and C-16 `why_it_could_work`, which had been overwritten with "Replace 'X' with 'Y'" instruction text. The verify correction is now applied inside the original text. C-04 and C-16 also carry the live-deck values from `models/device_cost_compare.py`: C-04 $8.50/GB = 5.73× cost and 1.04× glut; MRAM $821/GB = ~40× contract and ~101× glut.
5. `02_CONCEPTS.md` legend: added Rule 5 sense counts and survivors by sense, plus §3E lens coverage counts and the gap note.
6. The claim "No alternative memory comes within 10× of DDR5 cost" contradicted `device_cost_compare.py` §4, where C-05 and C-25 sit at or below DDR5 cost and eight Tier-B rows are under 10×. It was qualified to "a small entrant could make or buy new", with the sub-10× rows named (T4 fab-scale, foundry DRAM C-59, salvaged Optane C-26, other firms' die C-09 / C-15). Locations: `01_LANDSCAPE.md` §0 item 5, the §4.4 rule and the §10.2 row, and the `INVESTOR_MEMO.md` Insight.
7. Founder pronouns: 13 replacements in research inputs (listed above). The JSON files re-validated.
8. `OPEN_QUESTIONS.md` §8 and `FIRST_90_DAYS.md` §10: added status lines recording the items now resolved upstream. These are OQ items 1–3 and 90D items 1, 2 and 4: `decision.json` watch_list C-48 = 4 users, MOONSHOT confidence relabeled, PRIMARY.spend and plan_cash, and the PLAN rows in `models/lifecycle-intel.py` §10.

## Unresolved (4)

1. **§3E lenses are not applied to every survivor.** The mission says "apply every one to every surviving concept". The repo has only each card's author-selected lenses (1–4 of 8 per survivor). Missing: a 15 × 8 matrix (C-13, C-18, C-29, C-33, C-36, C-37, C-45, C-49, C-55, C-61, C-67, C-79, C-80, C-84, C-92 × fabless→foundry, IP licensing, module/appliance, recert/brokerage, SaaS, data product, defense-first, university/lab-patent licence). Each cell needs a fit / no-fit verdict and a one-line reason. Notably, the lab-patent lens is named by 0 survivors (it was tested on 12 killed concepts and in `01_LANDSCAPE.md` §9.2). This needs 120 new judgments, too large for a surgical gate fix. Natural home: a new `03_SCORING.md` section, or a column in `research/tools/build_summary_table.py`.
2. **The Phase 7 ten-line console summary** has not been produced yet. It is the orchestrator's step.
3. **Cross-file inconsistencies still flagged.** `FIRST_90_DAYS.md` §10 items 3 and 5–10 and `OPEN_QUESTIONS.md` §8 items 4–8 remain open: the DD5 calendar needs re-dating and an `open-memory-ip.py` re-run, two judges misstate the m12 gate, there is LI vs LI.py drift ($201,001 vs $200,710; 235 vs 238 accounts), and LI still references the killed DD1/DD3. These belong to the files' owners and the number-tracing slices. `lifecycle-intel.md` and its model were being edited concurrently by another agent during this pass.
4. **INVESTOR_MEMO length** is ~1,300 words plus two tables, borderline for the "≤ 2 pages" rule. It was not trimmed, because that would be a rewrite.

## Notes (no action)

- The pre-Phase-1b deck ($15.99 / $6.40 / $1.64) still appears in kill reasons (27 places in `02_CONCEPTS.md`, 13 in `concepts.csv`). It is traceable: `device_cost_output.md` §5 prints both decks, `03_SCORING.md` §1.2 documents the two-deck convention, and the "cannot beat the glut" list is identical on both decks.
- `research/phase1/micron_us_makers.md` contains "he-wrote" only inside a URL; it was not changed.
