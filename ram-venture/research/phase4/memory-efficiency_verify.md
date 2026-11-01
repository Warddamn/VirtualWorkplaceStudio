# DD4 memory-efficiency — verification log

Verifier: `p4v-memory-efficiency` · 2026-11-01 · Targets: `04_DEEPDIVES/memory-efficiency.md` and `models/memory-efficiency.py`. WebSearch used: 1 of 3, to check whether TrendForce's "Dell +15–20%" applied to servers. Result: the report centers on PCs, and coverage of the server scope conflicts.

## (a) Model runs: PASS
- `python3 models/memory-efficiency.py` exits 0, both before and after the edits. It regenerates `research/phase4/memory-efficiency_model_output.md` with no diff. No code changes.

## (b) Sections 0–13 present and substantive: PASS
- §0 header (three verdicts, tier, scores, recommendation), §1 how it works, §2 cost and unit economics, §3 target customer and the first ten, §4 GTM, §5 competitors, §6 IP, §7 regulatory and funding, §8 18-month roadmap, §9 team, §10 kill experiment, §11 kill criteria, §12 cycle test, §13 sources.
- Every Phase-4 item in the mission is covered. Nothing needed filling from the notes.

## (c) Numbers trace: PASS after fixes (~80 checked)
Checked against model §2–§8:
- §2.1 value table (all 4 rows).
- §2.2 unit economics, including the pilot at $2,000/$2,100/−5%.
- Funnel 0.67% and 149 touches.
- §2.3 headline table, every cell.
- Caveats 18%/40% recurring share and $4.4k.
- §2.4 sensitivity (7 rows plus FT M20, $167.6k, $73.0k).
- §2.5 numbers 27/2,157/~7×/66/225/2.5/0.37.
- §8 gates against the model months (M5, M6, M9, M10, M20; cash $10,454 at M9).
- §9 costs against the INPUTS block: $175/h, $750/$2,000 on-call, $200/h × 45 h, $3k benchmark half, $1,500 legal, $200/mo E&O, $12k SOC 2, 38–86% founder hours.
- §11 $15.50 (= 0.6 × 25.78) and $40.3k.
- §12 table and monthly nets +$2,862/+$591/−$839 (negative from M29). −59%/−88% fee drop. ~38% C-74 share of SEVERE M36 ARR. 20% C-75 glut factor.

Checked against other files and sources:
- `scores.csv`: totals, ranks, moat 2/1/1, competition 3/1/1.
- `03_SCORING.md`: 15% moat+comp weight, ceiling bands under §6, §7.4 quotes.
- `concepts_master.json`: C-74 ~300 h, $45–60k.
- `01_LANDSCAPE.md` §4.3: $25.78/$10.31. `B_notes.md` §2.3: 1.35 h / 3.4 h.
- Source `supports` fields: 92 EC2 SKUs, TMO 20–32%, Google 20%/5%, 14.2→116.5 s, TTFT −75%/−80%/−27.8%, $4.45 and $3.9–5.8/GB, ProsperOps 30–35%, Zesty 25%, $255→$900, ~$3,000, ICER 4–5×, UCR 6–14 wk, Ubuntu Pro $500/$1,775, RHEL $349–1,499, ScaleOps $130M/>$800M/$210M, CAST $1,000+$5/vCPU, Kubecost $449, Tensormesh $24.5M, SBIR 2031-09-30.

Fixes:
1. §2 intro: the $2.58 severe RDIMM price was attributed to `01_LANDSCAPE.md` §4.3, which does not contain it. It is now tagged [ESTIMATE: $2.04 component × the model's 1.266 ratio].
2. §0: "T0 software scores 5 on capital, ttr, founder" was true only for C-73 (C-75 scores 5/4/3). It now names C-73.
3. §0: the 5–15% realistic reclaim range is now tagged [ESTIMATE] with its basis (notes §1.1).
4. §1: the 2:1 compression claim had no citation. Added the Linux zram docs (logged in `D.jsonl`).
5. §1: "50–80% faster first responses" now reads "wait for the first token falling 50–80%". The sources report TTFT reduction, not speed.
6. §3: "Dell raised server prices 15–20%" now reads "raised prices 15–20%, led by PCs". The source headline is about PCs.
7. §3 row 9: the ServerMonkey URL was cited for "sell 'dodge the memory shortage'", but its logged support is the TrendForce outlook. The claim is now cited to PC Server and Parts and Comtek, and ServerMonkey is kept for the outlook.
8. §3 row 10: the 70B-class / 8–64 GPU buyer definition is now tagged [ESTIMATE].
9. §5: StormForge "(unverified listing)" is now [UNVERIFIED]. Kove's "with Supermicro" is now cited to the Supermicro solution brief (logged in `p4-memory-efficiency.jsonl`).
10. §8 Q4/Q5: the gates of ≥2 and ≥3 customers sit above the model (1.4 at M12, 2.6 at M15). Added "model expected" notes so the stricter gates are visible.

## (d) URLs logged: PASS
- All 58 unique URLs in the doc appear verbatim in non-`p4w` `research/sources/*.jsonl` files: 56 originally, plus the 2 added (zram docs, Supermicro). No entries were needed in `p4v-memory-efficiency.jsonl`, and none were removed.

## (e) Rules: PASS
- No fab is proposed; "fab" does not appear.
- Named buyers: RichWeb, Petronella, Leaseweb, MSU ICER, UArizona, Rutgers/UMBC/UIC, UCR.
- Named channel: Advanced Clustering, PC Server and Parts, ServerMonkey.
- Named mechanisms: zswap, KSM, PSI/Senpai, DAMON, LMCache, Dynamo.
- The three verdicts are separate: POSSIBLE Yes / PROFITABLE No (marginal side business) / DOABLE Marginal.
- The glut answer in §12 has numbers: fee $7.36→$3.02/$0.88, ARR $37.9k/$16.9k, C-74 sub GM 21%/−3%.
- No gendered pronouns; the founder is "they/their".

## (f) Kill experiment: PASS after fix
- Itemized cost $5,975, under $10k. Added an overrun check: a 50% contractor overrun gives ~$8.2k, plus a hard $10k stop. The experiment is not in the model's cash flow; §2.3 already gives the $4.4k cash-low impact.
- Duration was stated as "30 days" (days 29–30 scoring), which does not meet "< 30 days". Tightened to 29 days, 2026-11-02 → 2026-11-30, with scoring on day 29 and the go/no-go recorded on 2026-12-01. §11 and §8 dates are unchanged; §8 Q1 now says "days 1–29".
- Pass/fail thresholds are fixed in advance (≥10% reclaim at ≤5% p99 with zero OOM kills; ≥5 scans; ≥2 LOIs at ≥$5/node/month from DDR5 fleets; fewer than half DDR4-dominant), plus a separate C-75 gate (≥2 of 10 at ≥$15k).
