# DD1 provenance-recert — verification log

Verifier: `p4v-provenance-recert` · 2026-11-01 · Targets: `04_DEEPDIVES/provenance-recert.md`, `models/provenance-recert.py`. WebSearch used: 0 of 3. No number looked suspicious enough to need a search. Every problem found was arithmetic, a citation pointer, or the kill-experiment budget and calendar.

## (a) Model runs: PASS
- `python3 models/provenance-recert.py` exits 0, before and after the edits. Its stdout matches `research/phase4/provenance-recert_model_output.md` line for line, apart from the markdown wrapper. No code changes.
- All six §2.6 variant runs were re-run through `simulate()`/`metrics()`. Full-time month, ARR m36 and cash m36 match on every row: $268,513/$273,766, $232,342/$247,443, $232,377/$166,962, $21,868/$127,548, $203,455/$237,161 (full-time m14–15, back at the day job at m16), and $115,358/$222,394.

## (b) Sections 0–13 present and substantive: PASS
- §0 header (three verdicts, tier, scores), §1 how it works, §2 cost and unit economics, §3 target customer and first ten (named), §4 GTM, §5 competitors, §6 IP, §7 regulatory and funding, §8 18-month roadmap, §9 team, §10 kill experiment, §11 kill criteria, §12 cycle test, §13 sources. Nothing needed filling from the notes.

## (c) Numbers trace to a source: PASS after fixes (more than 80 spot-checked)
- **Model, m§1:** $253→$37 (15%) with its $183/$22/$11 split, GLUT $101→$9 (9%), SEVERE $45→−$1 (−2%). Channel split $36/$38. Per SKU $12/$43/$167, with $679 of cash tied per DDR5 unit. PMem $46/$11/−$7. CleanBOM $1,362/$256/$1,295 (80%) and pack ~88%. DIMM-health $8,640, 64/78/81%, 4.5/8.5/10.8×. Inventory lag $25 (11%). CAC $2,550 at 25×.
- **Model, m§2–m§7:** every cell of the §2.2, §2.3 and §2.4 tables, including run-rates rounded to $M. The §2.5 numbers (78%, 364, $3,450, $64,624, 7.5, 25%/12, 61, 23.5). The §8 roadmap values (39/$15.1k/+$2.1k, 155/$45.1k/$6.8k, 272/$74.4k, 388/$106.3k/1.5/$25.3k, 3.1/$56.3k, 570/7.5/$140.0k/$67.9k). The library counts 18/45/63, derived from `lib_samples_*`. The §12 glut path (−$2.1k, $42.5k→$3.7k at index 0.55, $5.6k/$23.5k, 291 modules at 9%, $284,620/$1,361,633/$391,022, $16,297, index 0.70 in Apr-28). The §12 cash table. Synergy gaps $247k/$122k/$61k recomputed.
- **INPUTS:** $40k start, 70%→40% eBay share, $3k launch, ×0.88 B2B, lab $400 × 1.6 = $640, $2.5k/$4.2k/$4k/$6k/$10k/$3k, $25/h, 35 h → 175 modules, the ~54 h at m18, E&O $400 plus insurance $200, $12k/$25k full-time trigger, the 5% buy floor, and $69 (= 0.55 × $125).
- **External:** `scores.csv` scores and ranks for all 4 IDs, and the four verbatim quotes in `scores_raw` (vc_2 and others). 01_LANDSCAPE: ~4× contract price (§5.1), SBIR $323k/$2.15M and CRDO $10M (§7.1), EAR99 (§8), DMEA Integra/Micross (§7.3). Source `supports` fields: amcompute $100–150/$890–1,200, Iron Mountain ALM +88%, Exiger $12.7M on 2026-10-01, Interos ~$12M, OBSIDIA $34M on 2026-07-29, CXMT 1260H dates, the 26 ANAB labs, IMD $50–500 and 2–6 weeks, R2 $2,000, AS9120 $6–12k, Herald 9.5%, Mobius $3M, Accuris $6k ACV, and Crowell 2027-06-30.

Fixes:
1. §0: the cumulative EBITDA citation was m§3, but m§3 does not print it. Changed to m§3, m§4.
2. §2.7: "ARR at m36 roughly halves" overstated the early-glut case (−38%). Now reads "GLUT ARR at m36 falls 38–53%, from $434,012 to $268,513 or $203,455".
3. §4 pricing: "SiliconExpert ≈ $7.5k/yr" is derived, not reported. Tagged [ESTIMATE: $6,000 ÷ 0.8], since the source says Accuris prices 20% below SiliconExpert.
4. §5: "rebuild a ~63-part library in a quarter" tagged [ESTIMATE: 63 × ~$400 ≈ $25k].

## (d) URLs logged: PASS
- All 57 unique URLs in the doc appear verbatim in `research/sources/*.jsonl`, mostly `p4-provenance-recert`; the rest are in v1-policy, v3-backend, p3-audit-*, C, D and p1-*. Nothing was added to `p4v-provenance-recert.jsonl`, nothing was removed, and the edits add no URLs.

## (e) Rules: PASS
- No fab or foundry is proposed; neither word appears. Concrete materials, partners and buyers are named: AddOn, Axiom, Brute, SHI, xByte, TechMikeNY, PCSP, Park Place, Z2Data; Iron Mountain/ITRenew, Sims; SMT Corp, Integra, Micross, UMD CALCE, NQA.
- Three separate verdicts: POSSIBLE Yes / PROFITABLE Marginal / DOABLE Yes.
- Glut answer with numbers in §12, both GLUT and SEVERE.
- No gendered pronouns; the founder is "they/their".

## (f) Kill experiment: PASS after fixes
- Pre-set thresholds were already in place (75%/8%, $600/15 business days/2 of 4, 3 of 15 plus cash, the TPM yes/no) and were left unchanged.
- **Fix 5, time:** the plan said "30 days" with "Days 25–30", which is not under 30. Changed to 29 days: day 1 is 2026-11-02 and the decision is on 2026-11-30 (Days 25–29). Kill criteria 1–3 moved from 2026-12-01 to 2026-11-30, §4 says the decision is on day 29, and §12 now says "29-day test". 15 business days after the day-7 lab shipment, with Thanksgiving off, ends exactly on day 29. This is noted in the doc as having no slack.
- **Fix 6, cost:** the ~$8,000 was unitemized. Track B's $2,000 did not cover 4 lab samples plus two bought modules, and at the $600 pass ceiling the true cost was understated. Itemized as follows:
  - A ~$5,000: Gen10 server ~$1,500 [ESTIMATE from `capex_m1`] + a lot capped at $3,500 (~40 × $81, m§1a).
  - B ~$2,400: 4 × $400 lab + ≤$800 for samples [ESTIMATE from the ~$54 DDR5 16Gb spot in 01_LANDSCAPE §0].
  - C ~$1,000; D $0.
  - Totals: ~$8,400 gross, ~$9,200 worst case at the thresholds, **hard cap $9,500**, ~$3,000 net after resale.
