# DD3 nv-continuity-modules — verification log

Verifier: `p4v-nv-continuity-modules` · 2026-11-01 · Target: `04_DEEPDIVES/nv-continuity-modules.md`, `models/nv-continuity-modules.py`. WebSearch used: 0 of 3. No number looked suspicious enough to need it; every mismatch found was arithmetic or a missing citation.

## (a) Model runs: PASS
- `python3 models/nv-continuity-modules.py` exits 0, before and after the edits. Its stdout matches `research/phase4/nv-continuity-modules_model_output.md` line for line, apart from that file's markdown header. No code changes.

## (b) Sections 0–13 present and substantive: PASS
- §0 header (three verdicts, tier, TRL, axis, scores), §1 how it works, §2 cost and unit economics (with sensitivity, TAM, scale paths, C-16 option), §3 target customer and first ten, §4 GTM and first 90 days, §5 competitors and win/lose, §6 IP and FTO, §7 regulatory and funding, §8 18-month roadmap with dated gates, §9 team, §10 kill experiment, §11 kill criteria, §12 cycle test, §13 sources. Nothing needed filling from the notes.

## (c) Numbers trace to a source: PASS after fixes (40+ spot-checked)
Checked against a fresh model run, extra `simulate('BASE')` calls, `scores.csv`, `ASSUMPTIONS.md` and the `supports` field of the source logs:
- Unit-economics table (4 SKUs: list, net rev, COGS, GM, fees, contribution); 2MB COGS stack sums to $85.50; MRAM $42 = 49%; $21,504/GB and 1,056× ($21,504 / $20.37).
- Blended contribution $109/card, $3/DIP; fixed opex $900; 8 cards breakeven; 100 cards = 10%; 173 cards = 17%/67%; 733 units (183 + 550).
- Run-rate and recurring ARR at m12/18/24/36 for all three scenarios; no-LTSA $147.8k / $8.2k; $48k of $56.2k from LTSAs; m36 mix 59/12/25/4% (recomputed: 59.1/12.2/24.5/4.2).
- Breakeven 11/11/12; cash low $10.8k m6 / $11.6k m6 / $12.2k m7; cash m18 and m36; 36-mo revenue and net; peak need $29.2k.
- Net by year −$17.8k / +$34.3k / +$62.6k (recomputed: −17,846 / 34,344 / 62,641); $34/h and $80/h at 15 h/week (A-03).
- All 11 sensitivity rows; TAM chain 131,250 / 16,406 / 3,076 / 12,305 / $241 / $741.7k / $2.97M; scale paths S0–S4; C-16 premiums $362/$382/$394, p 0.32/0.19/0.11, EV −$44.8k/−$47.0k/−$48.3k, 3.1 design-ins, "$20–33" widening (20.4 / 32.6 unrounded).
- Scores 80.0/82.5/75.0 (#2/#2/#6) and 66.0/67.5/63.3 (#19/#18/#18) plus all ten criterion scores match `scores.csv`.
- External: $46.03, $37.67, 26 wk, $12.87, $239.39, $160–440, $403.81, $35–44, $51.21, $17.45, 5M Fanuc CNCs, >20,000 job shops, ITC dates 2026-02-27 and 2027-08-16, 37 claims / 4 patents, §5949 2027-12-23, FR 2026-02-17, SBIR to 2031-09-30, Memex ~1-yr retention, $102.60 @500 all match their logged sources.

Fixes:
1. §8 G3: "model: 34" DIPs by m6 → "model: 33" (unrounded 5.6 + 11.1 + 16.7 = 33.3; 34 came from summing rounded rows).
2. §9: "~$13k of contract engineering" had no basis. Model `one_time` gives $9k card + $1.5k DIP design = $10.5k; reworded with the source.
3. §5: "$5.25 board" was cited only to PCBWay, whose log entry has no price; added the OSH Park citation that supports it. "$43.70" for CY14B101 was cited only to Future ($17.45); added the logged Cytech source that supports $43.70, and listed it in §13.
4. §1: "about $5 of buffers" → the model's $5 line covers buffers + supervisor + ID EEPROM + passives; reworded.
5. §12: "all ramped over 2028-H1 (m15–20)" was wrong for BASE (the model eases BASE 10% over m15–26); reworded.
6. Tagged untraced judgment numbers [ESTIMATE]: §3 #10 "12–24 months to an approved source" (notes §4), §4 "~5 calls a week" (A-03), §10 Track A ~$1.2k (notes §8). Added the notes §8 breakdown to Track B ($2.5k + $0.8k + $0.2k + $2k).

## (d) URLs logged: PASS
- All 51 unique URLs in the doc (50 before, plus the Cytech URL added in fix 3) appear verbatim in `research/sources/*.jsonl`, mostly `p4-nv-continuity-modules` and `p4w-nv-continuity-modules`. The DLA DIBBS URL is logged in its `%20` form in `p4w`. Nothing added to `p4v-nv-continuity-modules.jsonl`; nothing removed.

## (e) Rules: PASS
- No fab proposed; there is no custom silicon (chips bought through distribution).
- Concrete materials, partners and buyers: Everspin MR4A16B Toggle MRAM, Infineon FM18W08/FM28V100 F-RAM, RAMXEED MB85R8M1; MacroFab, Screaming Circuits, Rush PCB; Memex, MRO Electric, Do Supply, Radwell, CDW-G, DLA Land & Maritime; Swissbit, Apacer, Sage, Phison.
- Three separate verdicts: POSSIBLE YES / PROFITABLE MARGINAL / DOABLE YES.
- Glut answer with numbers (§12 table: breakeven, cash low, run-rate, net, C-16 premium and EV per scenario; explains the drop comes from multipliers, not DRAM).
- No gendered pronouns; the founder is "they/their".

## (f) Kill experiment: PASS after fix
- Cost ~$6.7k (Track A ~$1.2k, Track B ~$5.5k, Tracks C and C-16 $0) plus ~$3k contingency = ≤$9.7k. Deposits are refundable, so they are not cost.
- Duration: the doc said "30 days (2026-11-02 → 2026-12-01)". That is 29 elapsed days; restated as "29 days (day 0 = 2026-11-02, decision day 29 = 2026-12-01)" and moved the ad window end from day 30 to day 28 so it is unambiguously <30 days.
- Pass/fail thresholds for demand, technical, supply and C-16 are fixed in advance in the §10 table.
- Added a note that the $299 re-test (kill criterion 3, 2026-12-15) runs only if the supply test fails, is a follow-on gate outside the 29 days, and is paid from contingency.
