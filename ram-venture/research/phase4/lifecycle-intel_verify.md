# DD2 lifecycle-intel — verification log

Verifier: `p4v-lifecycle-intel` · 2026-11-01 · Target: `04_DEEPDIVES/lifecycle-intel.md`, `models/lifecycle-intel.py`. WebSearch used: 0 of 3. No number looked suspicious enough to need it; every mismatch found was arithmetic.

## (a) Model runs: PASS
- `python3 models/lifecycle-intel.py` exits 0 (run before and after the edits). Its stdout matches `research/phase4/lifecycle-intel_model_output.md` line for line, apart from that file's markdown wrapper. No code changes.

## (b) Sections 0–13 present and substantive: PASS
- §0 header (three verdicts, tier, scores), §1 how it works, §2 cost and unit economics, §3 target customer and first ten, §4 GTM, §5 competitors, §6 IP, §7 regulatory and funding, §8 18-month roadmap, §9 team, §10 kill experiment, §11 kill criteria, §12 cycle test, §13 sources. Every Phase-4 item in the mission is covered. Nothing needed filling from the notes.

## (c) Numbers trace to a source: PASS after fixes (more than 40 spot-checked)
Checked against the model output (§3, §5, §6, §7, §8), `scores.csv`, `01_LANDSCAPE.md` and the source logs:
- Unit-economics table: prices, COGS and margins for all six lines. CAC $563/$1,188, LTV $13,649, LTV/CAC 24.3/11.5, payback 2.1/4.4.
- Gross margin and revenue: 45%/$5,787 (m12), 65%/$12,978 (m18), 71%/$19,219 (m24), 74%/$40,811 (m36). Fixed data cost $1,867.
- Scenario table: ARR at m12/m18/m24/m36, breakeven, salary-cover months, full-time month, cash low $21,951 at m10, cash at m36. All 3 scenarios.
- Sensitivity: all 8 ARR values and salary-cover months; the cash-low range $17,096–$24,795.
- What must be true: 52 accounts, 27 + 10, 2.3×/57, 225 accounts, 3.7%, 4.7×/468, 115 licences, 5 of 25.
- Glut modules: $15,862/$6,817/$2,300, $13,696, $5,570/$7,318/$7,488, $5,682/$5,331/$4,979, and the percentages. Mix 39/21/8% and 14/22/26%. ARR change −21%/−33%.
- Price deck $20.37/$21.79/$17.31/$16.38/$8.15/$2.04. Max draw $18,049. Roadmap gates 1.7, 5.8, 11.8, $4,116 MRR, 19.5. Kill criteria 2.8 and 27.
- Scores (79.0/82.5/75.8 …; moat, competition and cycle scores) match `scores.csv`. The 82% glut margin and 6× in five quarters match `01_LANDSCAPE.md`. AdvaMed 75–80/75/88/63%, Avnet 25–45 weeks vs 8–12, Luminovo 80–90%, DigiKey 120/min and 1,000/day, GSAM 2026-01-15, SBIR to 2031-09-30, §5949 2027-12-23, Lewis Silkin 3–5% vs 35–50%, and DRAMeXchange $5k/$11k/$30k all match the `supports` field of their logged sources.

Fixes:
1. §11 item 11: "$150,000 (22% under the model's SEVERE path of $172,694)" was wrong. $150k is 13% under SEVERE ($172,694) and 22% under BASE ($193,183). Reworded to give both.
2. §12 caveat 1: ARR at m26 was ~$216k (GLUT) and ~$192k (SEVERE), computed from rounded MRR. The unrounded model values are $17,528 and $15,793 MRR, so ARR is ~$210k and ~$190k.
3. §8 Q6 gate: MRR "~$11k" → "~$10.5k" ($126,068 / 12 = $10,506).
4. §8 Q2: "6–10 trials/month" → "6–8 trials/month (model)". In m4–6 the model has 0, 6 and 8 trials; the 10 falls in m7.
5. Tagged untraced numbers [ESTIMATE]: the §1 illustrative company (8–32 GB), the §3 buyer definition (5–20-year lives), customer #10 EMS ($50–500M revenue), and the §7 $0.5–1M angel round.

## (d) URLs logged: PASS
- All 53 unique URLs in the doc appear verbatim in `research/sources/*.jsonl`, mostly `p4-lifecycle-intel`; the rest are in E, D, C, `p3-audit-*`, `v1-policy` and `p4-provenance-recert`. No entries added to `p4v-lifecycle-intel.jsonl`. None removed.

## (e) Rules: PASS
- No fab is proposed (the word does not appear). Named materials, partners and buyers: F-RAM/MRAM swaps; Nexar, DigiKey, DRAMeXchange, UMD CALCE; OnLogic, Amplicon, Trenton, WINSYSTEMS, Unipi, KUNBUS and others.
- The three verdicts are separate (POSSIBLE Yes / PROFITABLE Marginal / DOABLE Yes).
- The glut answer has numbers (§12: −57%/−86% price-driven, +31%/+34% index, ARR −21%/−33%).
- No gendered pronouns; the founder is "they/their".

## (f) Kill experiment: PASS
- Cost ≈ $2,450: Sales Navigator $100, attorney $1,000, thank-yous $1,250, domain $100. Deposits are refundable, so they are not cost. The cap is $5,000, well under $10k.
- Duration 29 days (2026-11-02 → 2026-12-01).
- Thresholds K1–K5 are fixed in advance and emailed to the advisor on day 0.
- Note, not changed: §11 item 4 lets the Nexar/DigiKey data-rights answer run to 2026-12-15. That is a follow-on gate; the experiment's own decision is still on 12-01.
