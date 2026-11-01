# DD6 private-moe-appliance — verification log

Verifier: `p4v-private-moe-appliance` · 2026-11-01 · Targets: `04_DEEPDIVES/private-moe-appliance.md`, `models/private-moe-appliance.py`. WebSearch used: 1 of 3, to source the "Gemma 4 31B on one GPU" claim, which had no logged source.

## (a) Model runs: PASS
- `python3 models/private-moe-appliance.py` exits 0. Stdout is byte-identical before and after the doc edits, and it matches `research/phase4/private-moe-appliance_model_output.md` apart from the markdown header and wrapper. No code changes.
- A helper script loaded the model module with `importlib` and recomputed the numbers the doc derives but the model does not print (listed under (c)).

## (b) Sections 0–13 present and substantive: PASS
- §0 header (pitch, tier T1, scores, three verdicts, recommendation), §1 how it works, §2 cost and unit economics (2.1–2.6), §3 buyer and ten named targets, §4 GTM and first 90 days, §5 competitors, §6 IP, §7 regulatory and funding, §8 roadmap with dated gates, §9 team, §10 kill experiment, §11 fourteen kill criteria, §12 glut test, §13 sources. Nothing needed filling in.

## (c) Numbers trace to a source: PASS after fixes (more than 90 spot-checked)
- **Model §1:** every cell of §2.1 (L and S, BASE/GLUT/SEVERE). DRAM 47% + GPU 33% ≈ 80% of the L BOM. $25.78/GB contract RDIMM.
- **Model §2:** 17/25 tok/s, 4/6 concurrent, 27/40 users, 19/22 s and 5/7 s TTFT. The 37-user reference: 1.25 tok/s, 41 s at ~23 concurrent.
- **Model §3:** $12,105/19%, $5,724/19%, $1,250/$317/75%, $650/$255/61%, $40,366, $18,238, CAC $5,188 (12.5 × 3 × $85 + $2,000). LTV/CAC 7.78 and 3.52, shown as 7.8 and 3.5.
- **Model §4:** $116, $40, $124, $31, $35, $16, $104.
- **Model §5:** every cell of §2.4, including $13,734 at m7, −$13,314, $21,700 and the ~$25k bridge. §12 deltas: −16%/−22% ARR; −43%/−58% box price; 44–60% less HW GP per L box; full-time slips 5–7 months.
- **Model §7:** every row of §2.5, plus "no channel −44%" (43.7%) and "ARR $143k" (K3).
- **Model §8:** 24.5% (×3.06), 11.8%, ×2.91, $559,144.
- **Roadmap (§8):** 1.2 orders by m9, 2.4 by m12, ARR $22.8k/$36.5k/$53.1k, 4.7 boxes at m18, demo box m14. Gates at ~75%: $17k, $27k, $40k.
- **Recomputed from model rows:**
  - Subscription share of 36-month revenue: 18.42% / 23.08% / 27.76%.
  - m36 subscription share of monthly revenue: 25.66%.
  - Conversations by m18: 96.3, of which 78.3 founder-sourced.
  - Contractor hours over 36 months: 24.5.
- **Arithmetic:**
  - 12 × 6400 MT/s × 8 B = 614.4 GB/s; at 16 GB per token that is 38.4 tok/s, and 17 tok/s is 44%.
  - 8.73 → 11.26 is +29%.
  - 7–8 × $16–18k = $112–144k.
  - $166.7/GB vs $25.78 = 6.5×; $91.7 vs $10.31 = 8.9×.
  - DGX Station: 1.44× the price, 2.96× the users.
- **External, from `supports` fields:** $16,000 and $17,987 RTX PRO 6000, launch MSRP $8,565; 5090 at $4,299–5,300; SMCI 10.8%; Mac Studio $22,299; DGX Spark $6,950/$4,999; Puget $43,357/$84,652; AVADirect $94,749; Petronella $8–12k; Iternal $697; Lemony $499; First Focus $25–75; CoCounsel $104–639; Copilot GCC High GA Dec-2025; Phase 2 2026-11-10 and Phase 3 2027-11-10; ~80,000 / ~80 C3PAOs; NDAA §5949 2027-12-23; SBIR to 2031-09-30; SBIR PI >½ employed; Netlist–Samsung licence; Inkling 975B-A41B and Nemotron 550B-A55B.

Fixes:
1. §2.4: "about 43% of gross profit" changed to **about 42%**. Recomputed as $21.1k subscription revenue − $6.4k fleet subscription cost − $0.6k partner share = $14.1k of $33.5k GP (42.2%). Without the partner share it is 44.1%, so 43% sat between the two.
2. §9: "BASE uses only 24 h" changed to "~25 h (24.5 h)", per the model's contractor-hour sum.
3. §7: "1,717 certified by Jul-2026" was cited to Infonaligy, which supports only ~80,000 and ~80 C3PAOs. Added the CyberSheath citation, which carries 1,717.
4. §5 Mac row: the LLM Configurator snippet supports "2.8T-class does not fit/serve well", not the 1T INT4 claim. Now: 1T INT4 (~600 GB) does not fit in 512 GB [ESTIMATE: arithmetic], and 2.8T-class models do not serve well (LLM Configurator).
5. §5 DGX Station row: "$85–100k" tightened to **$87–95k** (STH $87,411.50; Exxact $94,930 via Tom's). "748 GB" was cited to STH and Tom's, but only Wccftech (already logged in p4) supports it, so it is now cited to Wccftech.
6. §5 small-models row: "Gemma 4 31B" had no logged source; Ertas supports only GPT-OSS. One WebSearch found Yotta Labs (2026-10-05): it fits one 24 GB card at 4-bit. Cited and logged.
7. §3 #6: "lack an air-gapped option" is not in the Summit 7 snippet. Reworded and tagged [ESTIMATE: judgment from search, not confirmed].
8. §13: added the Wccftech and Yotta URLs and the p4v log note.

## (d) URLs logged: PASS
- All 53 unique URLs in the edited doc appear verbatim in `research/sources/*.jsonl`. 45 are in `p4-private-moe-appliance`; the rest are in p4w-private-moe-appliance, B, p3-audit-07, E/p4-legacy-dram-diebank, v1-policy, v3-backend and p4v.
- One new entry was written to `research/sources/p4v-private-moe-appliance.jsonl` (Yotta Labs).
- Nothing was removed: no cited URL was missing from the logs.

## (e) Rules: PASS
- No fab or foundry appears anywhere.
- Concrete partners and buyers are named: Petronella, Daymark, CyberSheath, Summit 7, Corsica, VT ARC, UD UDSecCom, mid-size iManage law firms in Philadelphia, Baltimore and Richmond, plus OCM/authorized-distributor supply rules.
- Three separate verdicts: POSSIBLE Yes (TRL 8–9) / PROFITABLE Marginal / DOABLE Yes to build, unproven to sell.
- The glut answer in §12 has numbers for BASE, GLUT and SEVERE, plus the elasticity-1.0 case, and gives a clear verdict: it survives and shrinks 16–22%. It also refutes the "benefits from a glut" claim in `selection.json`.
- No gendered pronouns. The founder is referred to without pronouns or as "they".

## (f) Kill experiment: PASS after fixes
- The test runs 29 days (2026-11-02 → 2026-11-30). Its pre-set thresholds K0–K7 are written down and emailed before any call (Step 0), with numeric pass and fail values: ≥3 LOIs or ≥1 pilot; ≥40%/≥60%; ≥12 and ≥8 tok/s, TTFT ≤25 s and >40 s; ≥20 conversations in 28 days.
- **Fix 9:** the ~$7,000 was only partly itemized. Added:
  - the Track A breakdown: $100 + 20 × $50 + ~$1,400 travel contingency;
  - the Track B basis: a one-week rental at ~2.5× the model's $1,200/month input, [ESTIMATE: no quote];
  - a total line of $500 + $2,500 + $3,000 + $500 + $500 = ~$7,000, with a **hard cap of $9,500** and a fallback (borrow a demo unit or log K4 as unmeasured).
- **Fix 10:** in the §4 first-90-days table, "Days 1–30" for 11-02 → 11-30 contradicted the 29-day test. Relabelled to 1–29 / 30–60 / 61–91 to match the dates.
