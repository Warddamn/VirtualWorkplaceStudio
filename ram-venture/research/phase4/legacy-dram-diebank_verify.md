# DD7 legacy-dram-diebank: verification log

Verifier: `p4v-legacy-dram-diebank` · 2026-11-01 · Targets: `04_DEEPDIVES/legacy-dram-diebank.md` and `models/legacy-dram-diebank.py`.

WebSearch used: 3 of 3.
1. The DSPO 2024 99.3% no-redesign figure: confirmed. The case counts were not in the snippet.
2. Teledyne DDR4T04G72: the 2020 part is 4 GB. The 8 GB DDR4T08G72 appears only in later listings.
3. Micron Manassas: 1-alpha production started 2026-05-22, qualified output is expected by end-2026, and the expansion "will" quadruple DDR4 wafer supply.

## (a) Model runs: PASS
- `python3 models/legacy-dram-diebank.py` exits 0, both before and after the edits.
- A fresh run matches `research/phase4/legacy-dram-diebank_model_output.md` apart from that file's markdown header.
- The model code is unchanged.

## (b) Sections 0–13 present and substantive: PASS
- §0 header (pitch, anchor C-91 + folded C-65, tier T2, scores, three verdicts, recommendation)
- §1 how it works
- §2 cost and unit economics (2.1–2.7)
- §3 target customer and first ten
- §4 GTM with first 90 days
- §5 competitors
- §6 IP and FTO
- §7 regulatory and funding
- §8 18-month roadmap with dated gates
- §9 team
- §10 kill experiment
- §11 kill criteria (13)
- §12 cycle test
- §13 sources

## (c) Numbers trace: PASS after fixes (~110 checked)
**Against model output (§2–§9):**
- Price deck: $20.37, $13.24, $8.15 at m17, $2.04 at m20, $3.00 at m60, $16.80 at m20.
- §2.1 L1: $770/mo, 100 mo, $79.1k, $11.4k, 28.6 conversations, ~136 h.
- §2.1 L2: $2,000 and $295. L3: 12,510 die, $12.11/die, $120k.
- §2.1 L4: $490 and $344, GM 45.6–61.8%, $1.4M NRE.
- §2.2: every cell of the six-row bank table. Break-even multiples 1.5×, 2.3× and 4.8× recomputed as cost/unit ÷ $/GB (25.37/16.80, 18.54/8.15, 14.47/3.00).
- §2.3: $1.33M per design-in, every cell of the 3×3 grid, BULL $26.8M / $13.9M / 7.3×. "6.7× volume" = 4,000/600.
- §2.4: Plan A table, all 24 cells. Mix 3.8/6.6, $8.6k commissions, $8,500 = $6,000 + $2,500.
- §2.5: Plan B table, all cells. Bank bought at m20, skipped at m44/m68. Plan C $6.0M / $4.5M / $3.6M / $598.5k / $410k, DSCR 1.50/0.85/0.45.
- §2.6: sensitivity, all 16 ranges plus bank IRR −9.6%/+11.7% and −4.7%/+3.8%.
- "EBITDA negative every year from y2": y2 is printed; for y3–y10 the model reports "1st EBITDA+ yr: never".
- §4: "~0.7 study-equivalents by m4" (model: $2,958 cumulative one-off = 0.74). Funnel 4 conversations/mo, 10%/35%, conferences at m10/22/34.
- §8 gates: 0.8 programs at m9, $12.6k → $9.5k (75%), 1.1 programs at m12, $22.0k → $16.5k, 1.9 programs / 2.8 accounts at m18. $311k = 12,510 × 0.75 × $20.37 + $120k.
- §9: costs match the INPUTS block ($11k, $6k, $36k, $16k, $8k, $30k, 15 h/wk).
- §7: $35k AS9120B over m21–m25, $8k/yr, $250/mo ITAR from m30, $1.5M at m18, $4.0M at m30.
- §11 and §12: $9.5k, $20k floor vs $30.2k low, ≤2.4× grid (4×600 = 2.42×). GM 52.2/57.0/62.7%. Commissions $8.6k/$4.4k/$928. −21%/−38%. Demand ×0.75/×0.60, multiples ×0.9/×0.8, design-ins ×0.85/×0.70 (from the INPUTS code). EBITDA $900k/$510k/$270k = $6.0M × (1/0.85/0.75) × (15/10/6%).
- DMSMS ceiling $6.3–25.4M (model $6.34–25.36M).

**Against other files:**
- `scores.csv`: C-91 57.0/53.3/59.2 (#28/#30/#23), moat 4, comp 1, cycle 3, founder 1, n = 3. C-65 57.0/53.3/57.5 (#30/#31/#25), 3/1/4/1. 40 scored rows. C-91 is the only concept with moat 4. Competition and founder means are both 1.0, so all three scorers gave 1.
- `03_SCORING.md` §9: the round-2 rationale.
- `01_LANDSCAPE.md` §7.3: 1.5–5×.
- DD2: $3,500 study.
- `05_REDTEAM.md`: "$249 feature that distributors give away".

**Against `supports` fields:**
- Micron EOL 2025-06-13; PCN 36146 last order 2026-03-30; Samsung DDR3 stop Q2 2024.
- DSPO 2,809/1,268/24/99.3%.
- Infineon 36 months; Micross 20+ yr; 17-yr study.
- Cleat dates and SPE7M5-26-T-400W.
- AdvaMed 63%; ISSI to 2038.
- Similarweb $200–500M; Revelio ~864.
- IBAS $134.3M; Flip 22 OCMs, 2023-02-21, ~30 staff.
- Avnet MOQ 5–25; Mercury $8.2M; Frontgrade 2024-11-05.
- Winbond sold out through 2027, LTAs to 2029–30.
- SBIR to 2031-09-30; DLA SBIR 2026-06-18; ~$1.8M; Suntsu 175 die on 2026-05-26.

**Fixes (surgical Edit):**
1. §8 m2–m5 gate: "~$4.4k cumulative one-off revenue by m5" is now "~$4.5k ... $4.0k of it studies". The model sums m1–m5 to $4,484.
2. §1: "Teledyne e2v has sold exactly this since 2020" was wrong. The 2020 DDR4T04G72 is 4 GB, not the 8 GB part described. It now names the 4 GB part and cites the Avnet DDR4T08G72 listing for 8 GB (search 2).
3. §5 Micron Manassas: "since 2026-05-22; quadruples DDR4 wafer supply" now reads "production started 2026-05-22, qualified output expected by end-2026; expansion *will* quadruple (Micron's own figure)" (search 3).
4. §5 had facts with no citation. Added nine URLs that were already logged:
   - Rochester >10B die (Electronic Specifier) and "over 70" OCMs (ADS directory).
   - Micross ~15M die (Apopka page) and DMEA (3D InCites, Raleigh).
   - Teledyne HiRel 16GB (Business Wire 2025-07-24).
   - Mercury 8GB 2022-11-08 (SIJ) and 100% burn-in (datasheet).
   - IM 32Gb DDR4 Q3 2026 (IM page).
   - Winbond 16 nm (DigiTimes 2025-12).
   - Cited the AMD/ISSI URL in the row too.
5. §7: §5949 now notes that the implementing FAR rule was still a proposed rule as of 2026-11, with statutory effect 2027-12-23.
6. §13: listed the nine added URLs and a note on the verifier's additions.

## (d) URLs logged: PASS
- 59 unique URLs (50 before the edits, plus the 9 added). Every URL in the body is listed in §13, and §13 lists nothing extra.
- 58 appear verbatim in non-`p4w` logs.
- The ERAI glossary URL is logged in `p4-legacy-dram-diebank.jsonl` with literal spaces. It is the same URL, differing only in percent-encoding, so it was accepted.
- The DSPO URL had the same encoding issue. It is now also logged verbatim in `p4v-legacy-dram-diebank.jsonl`, since it was re-checked by search.
- `p4v-legacy-dram-diebank.jsonl` holds 3 entries actually used: DSPO, SIJ Teledyne, Micron IR.
- No URL was removed. None was unlogged.

## (e) Rules: PASS
- No fab is proposed. "fab" does not appear in the doc. Micron Manassas appears only as a competitor.
- Concrete partners and buyers are named:
  - OCMs: Winbond, ESMT, Etron, Nanya, Alliance, Intelligent Memory.
  - Vault and OSAT: Micross, QP Technologies, Integra.
  - Buyers: NAVSUP WSS, Tobyhanna, NAWC China Lake, DLA L&M, NSWC Crane, Trenton, CP Technologies/Core Systems, WINSYSTEMS.
  - Two buyer rows are honestly tagged [UNVERIFIED]: NewSpace and medical/rail.
- Three separate verdicts: POSSIBLE Yes (TRL 9) / PROFITABLE no for an entrant / DOABLE only the side-line wedge.
- The glut answer in §12 has numbers:
  - Bank GM 39.6% → −1.1% → −236.6%, not bought in GLUT or SEVERE.
  - MCM GM 52.2/57.0/62.7%.
  - Commissions $8.6k → $928.
  - Plan A −21%/−38%.
  - Plan B 0.46/0.36/0.28×.
  - DSCR 1.50/0.85/0.45.
- No gendered pronouns. The founder is "they".

## (f) Kill experiment: PASS after fix
- Cost was itemized as $100 + $2,500 + $2,500 + $900 = $6,000, under $10k. Added a 50% overrun check ($9,000) and a hard $10k stop. The $2,500 of LLC legal is clarified as spent only after a pass. The model's m1 one-off of $8,500 is unchanged.
- Duration was "2026-11-02 → 2026-12-01" with "days 29–30" scoring. That is 30 days, which fails "< 30 days". The §11 #4 extension to 2026-12-15 for unanswered OCMs pushed track A to about 44 days.
  - Tightened to 29 days: 2026-11-02 → 2026-11-30, scored on day 29, go/no-go recorded 2026-12-01.
  - §11 #4 now counts fewer than 3 written OCM answers by day 29 as a fail. Non-replies no longer extend the test.
  - §4 row 1 now reads "1–29 / → 11-30", and §0 now says "29-day".
- Thresholds are fixed in advance and emailed on day 0. The track A and B fail columns were made exhaustive: "pass not met" and "fewer than 3 of 10 meet the pass test", so no outcome falls between pass and fail. The C1 (≤$15/die), C2 (NRE ≤$2M and build ≤$400) and C3 (vault white-label) thresholds are unchanged.

No git commit made.
