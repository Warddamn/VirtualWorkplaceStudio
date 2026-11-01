# Phase 1b verification: cost inputs (agent `v4-cost`)

**As of:** 2026-11-01 · **Owner files edited:** `research/phase1/cost_stack.md`, `research/phase1/cost_inputs.json`, `models/dram_cost_stack.py` (re-run, exit 0, regenerated `research/phase1/cost_stack_output.md`) · **Sources:** `research/sources/v4-cost.jsonl` (50 entries) · **Assumptions:** `research/assumptions/v4-cost.md`

**Method and limits.**
- **Searches:** 24 WebSearch calls, the full quota.
- **Fetches:** 3 WebFetch attempts, and all failed DNS: techinsights.com, siliconanalysts.com and stockhub.kr.
- **What that means for the facts:** every new fact below comes from search-result snippets.
- **Tags:**
  - **[REPORTED-P]**: a primary document (TechInsights, Micron, Counterpoint, TrendForce, LCSC) seen only through a snippet.
  - **[REPORTED]**: secondary coverage.
- No paywalled report was read.

## Change log

| # | Item | OLD claim (as written in the notes) | NEW status | Corrected or confirmed fact (date) | Source |
|---|---|---|---|---|---|
| 1a | Micron 1z 16Gb DDR5 die | ~66.4 mm², 0.241 Gb/mm² [REPORTED] | **CONFIRMED** | 66.26 mm², 0.241 Gb/mm². Samsung D1y is 73.58 mm² / 0.217; SK hynix D1y is 75.21 mm² / 0.213 (TechInsights, 2022) [REPORTED-P] | https://www.techinsights.com/ja/node/37203 |
| 1b | 1α 16Gb DDR5 die | 53 mm² (48–57), 0.30 Gb/mm² [UNVERIFIED: PK] | **CONFIRMED** | SK hynix D1a EUV 16Gb DDR5 is 7.40 × 7.11 mm = **52.61 mm²** at the die seal (53.27 full), 0.30 Gb/mm² [REPORTED-P] | https://www.techinsights.com/blog/sk-hynix-d1a-euv-16-gb-ddr5-dram-transistor-characteristics |
| 1c | **1β 16Gb DDR5 die** | **41 mm² (36–49), 0.39 Gb/mm²** [ESTIMATE] | **CORRECTED** | Micron D1β (Y52K) 16Gb DDR5 is 6.33 × 5.66 mm = **35.83 mm²** (36.00 full), **0.447 Gb/mm²** [REPORTED-P]. Samsung D1b 16Gb LPDDR5X is **36.68 mm², 0.436 Gb/mm²** (TechInsights via ETN.fi) [REPORTED-P]. New base **36.5 mm² (35.8–41), 0.438 Gb/mm²** [ESTIMATE] | https://techinsights.com/ja/node/57875 ; https://etn.fi/index.php/embedded-conference-finland/13-news/16863-samsung-ahtaa-jo-dram-gigabitin-reiluun-2-nelioemilliin |
| 1d | 24Gb / 32Gb 1β DDR5 die | 61.5 mm² / 80 mm² (73–97) [ESTIMATE] | **CORRECTED (derived); area STILL-UNVERIFIED** | 54.8 mm² and 73 mm² from the new density. ISSCC 2024 paper 13.2 confirms Samsung's 32Gb DDR5 is on a "5th-gen 10nm" process (12nm-class, Sep 2023), but the snippets give no die area | https://allaboutcircuits.com/news/isscc-2024-samsung-doubles-ddr5-capacity-with-symmetric-mosaic-architecture |
| 1e | **1γ/1c 16Gb DDR5 die** | **33 mm² (29–36), 0.48 Gb/mm²** [ESTIMATE] | **CORRECTED (estimate); area STILL-UNVERIFIED** | Micron says 1γ 16Gb DDR5 gives **>30% more bits per wafer** than its 1β part [REPORTED-P], which implies ≤27.6 mm² (≥0.58 Gb/mm²). New base **29.1 mm² (27.6–33.3), 0.55 Gb/mm²**. TechInsights published a Micron Y62E D1γ full analysis (2026-05-14), but its die area was not visible | https://micron.cn/content/dam/micron/global/public/products/technical-marketing-brief/1-gamma-technology-brief.pdf ; https://techinsights.com/ko/node/61618 |
| 1f | Samsung / SK hynix 1b and 1c DDR5 die | (in the 1β/1γ ranges) | **STILL-UNVERIFIED** | Only Samsung D1b *LPDDR5X* was found. A Samsung 16Gb DDR5 die of 48.90 mm² appears, but its node is not stated (likely 1α-class) [REPORTED] | https://xenospectrum.com/ddr5-memory-chips-from-chinas-cxmt-40-larger-die-size-than-samsung-highlighting-challenges/ |
| 1g | CXMT 16Gb DDR5 die | G4: 66.99 mm², 0.239 Gb/mm² [REPORTED] | **CONFIRMED** | 66.99 mm² (8.19 × 8.18 mm), 0.239 Gb/mm², cell 0.0020 µm², F = 16.0 nm, cell ~20% smaller than G3. XenoSpectrum's 68.06 mm² is an outlier. **No newer (2025–26) CXMT DDR5 die found (STILL-UNVERIFIED)** | https://semiwiki.com/forum/threads/chinas-cxmts-ddr5-reveals-3-year-technology-gap.23270/latest ; https://www.techinsights.com/blog/cxmt-g4-16gb-ddr5-dram-process-analysis |
| 1h | 16Gb LPDDR5X 1β die | 40 mm² (35–48) [ESTIMATE] | **CORRECTED** | 36.68 mm² (Samsung D1b) [REPORTED-P]; 24Gb LPDDR5X becomes 55 mm² | (as 1c) |
| 1i | Micron 1β → 1γ gain | ">30% density" [UNVERIFIED: PK] | **CONFIRMED** (as bits per wafer) | ">30% increase in bits per wafer", 16Gb DDR5 [REPORTED-P] | (as 1e) |
| 2a | **DRAM wafer cost 1α/1β/1γ** | $3.4k / $3.8k / $4.3k fully loaded [ESTIMATE on UNVERIFIED capex/wpm] | **STILL-UNVERIFIED** | No public estimate from IC Knowledge, SemiAnalysis, TechInsights, Bernstein or Morgan Stanley appeared in snippets. Yole's paywalled LPDDR5X 2024 report contains a 1B wafer cost but no numbers were visible. **Cross-check:** with the smaller verified die, the model's 4Q26 GM (93%) sits 6–7 pp above Micron (87%) and Nanya (85.7%). That hints the 1β wafer may be closer to ~$4.5–5k (see notes) | https://www.yolegroup.com/product/report/lpddr5-x-comparison-2024/ |
| 2b | EUV scanner price / cost per exposure | ~$220M → ≈$62 per exposure [ESTIMATE] | **CORRECTED** | SK hynix is buying 30+ EUV tools for KRW 11.95T (~$8.8B) through 2027, ≈ **$290M per tool** (S&P Global, 2026-03) [REPORTED]. That gives ≈ **$78 per exposure** and $115–270 per EUV layer | https://www.spglobal.com/market-intelligence/en/news-insights/research/2026/03/sk-hynix-invests-in-euv-as-ai-boom-tightens-conventional-dram-supply |
| 2c | SK hynix 1c EUV layers | ~5–7 [UNVERIFIED] | **CONFIRMED** | Raising to a **6th** EUV layer (TechNews, 2025-08-12) [REPORTED] | https://technews.tw/2025/08/12/euv-sk-hynix-1c-dram/ |
| 2d | Micron 1γ EUV layers | 1 [UNVERIFIED: PK] | **STILL-UNVERIFIED** (count) | 1γ uses EUV with "reduced EUV use" (TrendForce News, 2025-03-11, title) [REPORTED] | https://www.trendforce.com/news/2025/03/11/news-micron-pioneers-1%ce%b3-ddr5-samples-with-reduced-euv-use-but-future-risks-loom/ |
| 2e | Micron cost-per-bit commentary | Backlog item | **STILL-UNVERIFIED** | No FY2026 figure found. Micron removed cost-per-bit from its quarterly slides in 2017 [REPORTED] | https://www.fool.com/investing/2017/12/28/micron-stopped-disclosing-this-key-metric.aspx |
| 2f | Kurnal "0.436 Gb/mm²" 1b density | Upper bound of the 1β range (via KitGuru) | **CLARIFIED** | 0.436 equals the Samsung D1b LPDDR5X teardown. Kurnal's $0.654/mm² for 1b is spot-price revenue potential, **not** wafer cost [REPORTED] | https://www.kitguru.net/channel/generaltech/joao-silva/new-dram-value%E2%80%91per%E2%80%91area-chart-draws-attention-amid-rising-memory-prices/ |
| 3a | 28nm 300mm wafer 2026 | $2,600 (1.8–3.2k); TSMC $2.5–3.0k [UNVERIFIED: PK] | **CONFIRMED / adjusted** | TSMC 28nm ≈ **$3,000** ($2,550–3,450), Silicon Analysts estimate, Apr 2026 [REPORTED]. Blended base raised to **$2,800** (1.9–3.45k) | https://siliconanalysts.com/data/wafer-pricing |
| 3b | 2026 mature-node price increases | Not stated in the notes | **NEW / CONFIRMED** | UMC, VIS and PSMC up to +10% from Apr 2026 (TrendForce, 2026-03-16). Mature nodes +5–15% from 1Q26 to 2Q26. TSMC up to +10% on 12/16/28nm in 2027 (Nikkei) [REPORTED] | https://www.trendforce.com/news/2026/03/16/news-umc-vis-psmc-reportedly-eye-mature-node-price-hikes-of-up-to-10-from-apr-ic-designers-may-follow/ ; https://aiweekly.co/alerts/tsmc-to-lift-chip-prices-up-to-10-from-2027-nikkei-reports |
| 3c | 40nm wafer 2026; GF 28/40nm | $2,100 (1.6–2.5k) [UNVERIFIED: PK] | **STILL-UNVERIFIED** | No 2026 40nm or GF price in snippets | — |
| 3d | 3nm / 2nm wafer | ~$20k (18–23k) / ~$30k (25–33k) [UNVERIFIED: PK] | **CONFIRMED** | Silicon Analysts: 3nm $19,500 ($17–22k), 2nm $28–30k (Apr 2026) [REPORTED] | https://siliconanalysts.com/data/wafer-pricing |
| 3e | 8-inch price rise 2026 | "+5–20% as TSMC/Samsung trim 8-inch" [UNVERIFIED: PK] | **CONFIRMED** | +5–20% notified. Utilization 85–90% in 2026 against 75–80% in 2025. 8-inch capacity −2.4% YoY (TrendForce press release, 2026-01-13) [REPORTED-P]. In 2Q26, VIS rose +10–15% QoQ and PSMC ~+5% (Omdia, Jul 2026) [REPORTED] | https://trendforce.com/presscenter/news/20260113-12877.html ; https://omdia.tech.informa.com/blogs/2026/july/ddic-price-rise-as-foundry-and-material-costs-increase |
| 3f | 200mm 180nm / 90–130nm wafer price | $700 (450–1,000) / $1,000 [UNVERIFIED: PK] | **STILL-UNVERIFIED** (absolute) | No public $/wafer found. High end raised to $1,150 for the confirmed hikes | — |
| 4a | Everspin 1Gb STT-MRAM price | $102.60 @500, $266 @1 (LCSC) [REPORTED] | **CONFIRMED** | LCSC EMD4E001G16G2-150CAS2R: ~$266 @1, ~$106 @200, ~$103 @500, ~$101 @1,000 [REPORTED-P]. That is ≈ $821/GB. No Digi-Key or Mouser price was visible | https://www.lcsc.com/product-detail/C20342497.html |
| 4b | Everspin 256Mb price | Not in the notes | **STILL-UNVERIFIED** | Not searched (quota) | — |
| 4c | SRAM $/MB reference (288Mb QDR) | Not in the notes | **STILL-UNVERIFIED** (288Mb); **NEW** (72Mb) | 72Mb QDR-II+ CY7C25652KV18: $12.36 @1,088 to $33.70 @1 at a broker, ≈ **$1.4–3.7/MB ($1,400–3,800/GB)**; Avnet $192 @4 [REPORTED] | https://www.lisleapex.com/product-cy7c25652kv18-550bzxi |
| 5a | 64GB RDIMM contract 1Q26 | ">$900" [REPORTED] | **CONFIRMED** | **$927** in 1Q26; March compensation price $1,135. Counterpoint expected ~$1,500 in 3Q26 (Apr-2026 tracker) [REPORTED-P] | https://counterpointresearch.com/de/reports/memory-price-tracker-april-2026 |
| 5b | 64GB RDIMM 4Q26F (Citi) | $1,586 [UNVERIFIED] | **CONFIRMED as REPORTED** | May-2026 Citi note: $873 (1Q26) → $1,586 (4Q26), +82%. Seen only through a secondary relay; primary note not found | https://www.servnetuk.com/research/ddr5-server-memory-price-tracker-2026 |
| 5c | **Model 4Q26 RDIMM contract anchor** | **$1,300** (1,200–1,586) (p1-model: "2Q26 ~$1,000 × TrendForce") | **CORRECTED** | **~$1,650** (1,500–1,930) [ESTIMATE]: Counterpoint 3Q26F ~$1,500 × TrendForce 4Q26 +10–15%. Counterpoint raised its 3Q26 DRAM forecast to +10–20% QoQ (Jul 2026). The 2Q26 "~$1,000" anchor was stale | https://counterpointresearch.com/en/reports/memory-price-tracker-and-forecast-july-2026 |
| 5d | DDR5 16Gb contract, Oct 2026 | Derived ~$31 ($22–39) [ESTIMATE] | **STILL-UNVERIFIED** (published figure); derived value **CORRECTED** | No DRAMeXchange or TrendForce Oct-2026 DDR5 16Gb contract figure found. Derived from the RDIMM anchor: **~$41 ($37–48)**. Reference points: spot $53.92 (2026-08-31); a Kalshi market prices ~51% odds that the Oct-26 average exceeds $51.50 | https://www.buysellram.com/blog/ram-market-update/ ; https://kalshi.com/markets/kxddr5ms/monthly-ddr5-16gb-2gx8-48005600/kxddr5ms-26oct |
| 5e | DDR4 16Gb contract / spot, Oct 2026 | Not in the notes (DDR4 8Gb spot $44.37 on Aug 31) | **STILL-UNVERIFIED** (16Gb Oct); **NEW** data | DDR4 8Gb (1Gx8 3200) spot **$46.357** on 2026-10-20, +0.84% WoW (TrendForce, 2026-10-21) [REPORTED-P]. DDR4 16Gb spot $91.78 on 2026-08-31 [REPORTED]. DDR4 contract +4% MoM in Oct 2026, +24% over 3 months (unnamed bank, Guru3D) [REPORTED] | https://www.trendforce.com/news/?p=65594 ; https://www.guru3d.com/story/ddr4-memory-prices-now-also-rise-as-dram-supply-shortages-intensify-through-2028/ |
| 5f | TrendForce 4Q26 conventional DRAM | +10–15% QoQ (2026-09-30) [REPORTED] | **CONFIRMED** | Same figure in several snippets; server DRAM undersupplied in 4Q26 | https://www.trendforce.com/presscenter/news/20260930-13258.html |
| 5g | **TrendForce Oct-2026 revision "~+20%"** | Per the task brief: "is '~+20%' real?" | **STILL-UNVERIFIED** (weak) | The only source is an AI-generated StockHub summary (2026-10-20); it does not say "conventional" and cites no TrendForce release. TrendForce's 2026-09-23 bulletin headline says it lifted the 4Q26 outlook. **Do not use +20% as the base.** It is kept as the high case of `contract_dram_qoq_4q26f` | https://www.stockhub.kr/en/news/news_b7244c205001 ; https://trendforce.com/research/download/RP260923EN |
| 6a | HBM3E price 2026 | $1.50/Gb = $12/GB [REPORTED] | **CONFIRMED** | $1.50–1.60/Gb ($12–12.8/GB), DigiTimes Jul 2026. Silicon Analysts is lower at $8.33/GB [REPORTED] | https://capitalandcompute.net/memory-prices/hbm/ ; https://siliconanalysts.com/data/hbm-pricing |
| 6b | HBM4 price | 2027F $32–40/GB [REPORTED] | **CONFIRMED as forecast/proposal**; **NEW** 2H26 | 2H26 ~$2.00/Gb (~$16/GB). SK hynix asked ~$600 per 12-high stack ($16.7/GB). Samsung proposes mid-to-high $4/Gb for 2027. Fubon puts buyer-side cost at HBM4 $31–32/GB vs HBM3E $17–18/GB (this conflicts) [REPORTED] | https://www.sammyfans.com/2026/10/02/samsung-seeks-more-than-3x-hbm3e-pricing-for-hbm4/ ; https://semiconsam.substack.com/p/a-memory-down-cycle-is-coming-but ; https://www.trendforce.com/news/?p=62555 |

## Model impact (`models/dram_cost_stack.py`, re-run 2026-11-01, exit 0)

Several inputs moved more than 15%:
- 1β density +12%; the 1β die high end −15%
- 1γ die −13%
- 4Q26 RDIMM anchor +27%
- derived 16Gb contract +33%
- EUV cost per exposure +26%

So `cost_inputs.json` was updated (224 inputs, 5 new keys) and the script's fallbacks and labels were fixed.

| Output (`ddr5_reference()`) | Before | After |
|---|---|---|
| DDR5 1β component cost, $/GB | 1.641 | **1.484** |
| 1γ cost, 2026 ramp / mature, $/GB | 1.690 / 1.522 | 1.505 / 1.357 |
| 1β cash-only cost, $/GB | 0.844 | 0.776 |
| 64GB RDIMM cost, $/user-GB (module) | 2.409 ($154) | 2.210 ($141) |
| 4Q26 contract, component $/GB / RDIMM $/user-GB | 15.99 / 20.31 | **20.37 / 25.78** |
| A-05 glut price, component $/GB | 6.40 | **8.15** |
| GM at 4Q26 / in glut / at 2023 trough | 89.7% / 74.4% / −2.6% | 92.7% / 81.8% / +7.3% |
| HBM3E cost, $/GB | 6.08 | 6.08 (unchanged) |

## Notes

1. **No venture decision flips.** Every verified change pushes the same way: incumbent cost is a bit lower and the contract price higher. The glut line rises from **~$6.4 to ~$8.1/GB**, and full cost moves from 3.9× to 5.5× below the glut price. "A glut kills entrants, not incumbents" gets stronger. Alternative memories still sit at $55 to $1,600+/GB and remain 7–200× off even the new glut line.
2. **Downstream consumers must pick up the new deck.**
   - Anything quoting $1.64 / $6.40 / $15.99 is stale; the new values are $1.48 / $8.15 / $20.37. That includes `01_LANDSCAPE.md` §1 and the tables at lines ~19–21, 102, 178, 206–220 and 266–275, plus Phase-3 scoring briefs.
   - `models/device_cost_compare.py` imports `ddr5_reference()` live. However, it hard-codes a "claim-parity density" of 16Gb/41 mm². The verified value is 16/36.5 = 0.438 Gb/mm². That file belongs to another agent; I have not edited it or re-run it.
3. **The wafer cost is now the dominant unknown.** Density is anchored by teardowns, so the residual GM gap (model 93% vs reported 86–87%) most plausibly means the $3.8k 1β wafer is understated. The higher EUV tool price (~$290M) points the same way. A ~$5k wafer would put 1β at ~$1.9/GB and the 4Q26 GM at ~91%. Neither changes a decision.
4. **The "+20%" TrendForce revision** should be treated as rumor until a TrendForce release is found. The +10–15% (2026-09-30) figure stays the base.
5. **Blocked hosts** this run: techinsights.com, siliconanalysts.com and www.stockhub.kr. All failed DNS through WebFetch.
