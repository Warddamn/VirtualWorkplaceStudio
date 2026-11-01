# DD5 open-memory-ip — verification log

Verifier: `p4v-open-memory-ip` · 2026-11-01 · Targets: `04_DEEPDIVES/open-memory-ip.md` and `models/open-memory-ip.py`. WebSearch used: 0 of 3. No number looked suspicious. Every mismatch found was arithmetic or a citation pointer, and the model or a logged `supports` field settled each one.

## (a) Model runs: PASS
- `python3 models/open-memory-ip.py` exits 0, both before and after the edits.
- Its stdout matches `research/phase4/open-memory-ip_model_output.md` apart from that file's 4-line markdown header.
- No code changes.
- I also imported the module to read values it computes but does not print:
  - `fte_be`: m18, m23 and m28.
  - `new` at m14: 1.551 and 1.448.
  - `new` at m4: 1.185.
  - Cumulative revenue at m6: $16,015.
  - Trailing-3-month GP: $11,608 at m18 and $12,189 at m19.
  - FT threshold: 10,000 + 600 + 1,000 + 250 = $11,850.

## (b) Sections 0–13 present and substantive: PASS
- The doc has all of them:
  - §0 header (three verdicts, tier, scores)
  - §1 how it works
  - §2 cost and unit economics
  - §3 target customer and the first ten
  - §4 GTM
  - §5 competitors
  - §6 IP
  - §7 regulatory and funding
  - §8 18-month roadmap
  - §9 team
  - §10 kill experiment
  - §11 kill criteria
  - §12 cycle test
  - §13 sources
- Every Phase-4 item in the mission is covered. Nothing needed filling from the notes.

## (c) Numbers trace: PASS after fixes (~90 checked)
**Against the model:**
- §2.1 densities: 527.4, 43.0/57.6, 316.5 (5.5×) and 19.6/52.7 kbit/mm². DDR5 $18.33/$8.15/$2.04 per GB and 73×/163×/653×.
- §2.2 funnel: 298, 899, 30%/40%, 36, 72 (43/29) and $747.3k.
- §2.3: every price, COGS and GM figure. 1.12 accounts/mo, CAC $0.2k/$1.3k, LTV $5.4k/$31.4k, 12.3×.
- §2.4 scenario table, every cell.
- §2.5 revenue mix, including the 30/30/37% recurring share.
- §2.6: all 10 sensitivity rows.
- §2.7: 18 accounts (11+7), 25%, 12.7, 2.0/0.9.
- §2.8: the T2 rows, $788.9k and $161.6k.
- §8: every one-time spend and gate.
- §11: the model values.
- §12: multipliers and the −20/−33%, −19/−31% and −18/−29% changes (recomputed). Commercial accounts 12/10/8.

**Against other files and sources:**
- `scores.csv`: all 9 score/rank cells for C-33/C-32/C-22. TRL 6/5/6 match `concepts_master.json` and the phase-3 verify corrections.
- All 9 scorer quotes were found verbatim in `scores_raw` or `03_SCORING.md`.
- `01_LANDSCAPE.md`: $1,330/GB (§4.4); $25–75k/yr (§8); MA START $100–500k, SBIR to 2031-09-30, Strategic Breakthrough/caps/foreign screening (§7); Weebit $0.1M/$0.29M/$1.8–2.6M (§0, Phase 1b item 3).
- C-22 card: $0.6–1M.
- Source `supports` fields:
  - 15 issued + 3 pending patents; $17.5M NXP; N2 Mar-2026; GF FDX early 2027; $40M Everspin.
  - 116 commits; v1.2.50 on 2026-10-27; OCD 2026-10-30; 11 of 51 private; 9.5 kB TinyQV.
  - 54/40 slots; TT 289+275+283+52; DFFRAM 2,048 words; Chips4Makers Jul-2026; 256 Kb Weebit.
  - eMemory −15.9%; 61,000 chips; DV017 closed 2026-08-19; IonQ close 2026-07-31; DMEA 1A; $305k NSF.

**Fixes:**
1. §11 #2: model cumulative revenue at m6 is $16.0k ($16,015), not $15.9k (the sum of rounded months). §8 m5–m6 now gives the model values (2.5 accounts, $16.0k).
2. §11 #7: "$12.2k" was the m18 single-month GP, but the criterion is trailing-3-month GP. The model value is $11.6k, so it now reads "$11.6k trailing GP, with $12.2k in m18 alone".
3. §8 m18 gate: "GP ≥$11.85k/mo for 3 months" did not hold in BASE at m18 (trailing GP $11.6k). It is now the trailing-3-month gate, with the model's values at m18 ($11.6k) and m19 ($12.2k), which is how the model sets full-time at m20.
4. §8 m4 gate: "≥2 paying accounts" was far above the model (0.8 subscribers, 1.2 new customers), even though the footnote says gates sit near BASE. Changed to "≥1 paying customer (model: 1.2 new customers…)".
5. §4 days 61–90: "≥5 paying or committed accounts by m4" is now tagged [ESTIMATE target], with the model's 1.2 for contrast.
6. §2.8: the "Total external ~$4,305k" row sat under a column that sums to $5.8M. The model total is STTR I + seed + STTR II only. The row is relabeled, with a one-line note.
7. §9: the contract VLSI row said "$22.5k one-time". That figure also contains the $15k of characterization contractor already listed in the next row. Corrected to the $7.5k build-out (m2–m3).
8. §6: the Weebit fee figures pointed to 01_LANDSCAPE §9. They are in §0 (Phase 1b item 3); the pointer and the §13 internal-source line are updated.
9. §1: "8–64 KB" for a small RISC-V MCU is now tagged [ESTIMATE] with the TinyQV 9.5 kB data point. The Weebit "256 Kb" claim now carries its (already logged) press-release citation.
10. §2.1 gain-cell row: the silicon figure (1.25–1.43×) cited only Silicon Saxony, which supports the vendor figure. Added the BIU CRIS (silicon) and arXiv 2507.10849 (50%) citations, both already in the doc and logged.
11. §7: the STTR-PI and the Strategic Breakthrough/foreign-screening claims now also point to 01_LANDSCAPE §7. The cited NIH and Wiley snippets only partly support them; 01_LANDSCAPE §7 backs them in full.

## (d) URLs logged: PASS
- All 53 unique URLs in the doc appear verbatim in `research/sources/*.jsonl`, checked with an exact-match script after the edits.
- Most are in `p4-open-memory-ip`/`p4w-open-memory-ip`; the rest are in A1–A3, C, E, `p1-*`, `p3-audit-*` and `v1-policy`/`v2-fabs-ip`.
- No new URLs were added and none were removed, so `p4v-open-memory-ip.jsonl` was not needed.

## (e) Rules: PASS
- **No fab is proposed.** "Fab" appears only as SkyWater's existing fab and U.S.-fab shuttles.
- **Concrete names throughout:**
  - Materials and processes: sky130 6T, GF180, Weebit ReRAM, 3T gain cell.
  - Partners: OCD, UCSC VLSIDA, Chips4Makers, Integra/Promex.
  - Buyers: Brown ENGN2912e, Avalon, Sandia MESA, NORDTECH/NEMC.
  - Channels: ChipFoundry, Cadence MPW, MOSIS 2.0.
- **Three separate verdicts** (POSSIBLE / PROFITABLE / DOABLE), each split between the wedge and T2.
- **Glut answer with numbers** (§12): ARR m36 −20%/−33%, full-time date +5/+10 months, cash low unchanged at $20.4k, GLUT + free shock $39.1k, SEVERE + adverse −$14.7k.
- **Pronouns:** no gendered pronouns; the founder is "they".

## (f) Kill experiment: PASS (clarified)
- **Cost:** about $5.1k, under $10k. The step budgets are $2.3k + $1.2k + $0.1k + $0 + ≤$1.5k. The $500 deposits are refundable, so they are not cost.
- **Duration:** 2026-11-02 (day 1) to 2026-12-01 (day 30) is 29 elapsed days. The doc said "over 30 days", which was ambiguous against the < 30-day rule, so it now states the elapsed time.
- **Thresholds are set in advance:**
  - (i) ≥3 paid $500 deposits on ≥$2k orders, or ≥$15k in LOIs (matches the model's §8 kill line);
  - (ii) ≥1 buyer at ≥$10k;
  - (iii) ≥16 KB macros reachable in ≤200 h;
  - (iv) no free release coming.
- **Decision rule:** kill if (i), (iii) or (iv) fails; pivot if only (ii) fails.

## Not changed (noted)
- The model's INPUTS text for `weebit_first_ever_license_fee_usd` also says "via 01_LANDSCAPE s9". This is a comment only, with no effect on numbers, so the model was left untouched.
