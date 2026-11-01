# Phase 1: DRAM cost stack, plus trailing-node and alternative-memory cost inputs

**Agent:** `p1-cost` · **As of:** 2026-11-01 · **Machine-readable inputs:** `research/phase1/cost_inputs.json` (219 keys, each with low/base/high) · **Sources:** `research/sources/p1-cost.jsonl` · **Assumptions:** `research/assumptions/p1-cost.md`

> **Read this first: access limits.** This agent had **no working web access**. Its first WebSearch call returned "budget used up" because the shared 200-call budget had already been spent by other agents. WebFetch failed with DNS errors (semiwiki.com, kitguru.net, xenospectrum.com, anysilicon.com), and the proxy log shows 403s for trendforce.com, investors.micron.com and sec.gov. I did **not** reach TechInsights, IC Knowledge, SemiAnalysis, ISSCC or IEDM pages, so I cannot claim to have read them. The evidence therefore comes in four grades:
> - **[VERIFIED]**: open-source cost and design repos I opened via `git clone`. These are Chiplet Actuary (DAC 2022), ECO-CHIP, HP CACTI, the SkyWater sky130 SRAM bitcells and the GF180MCU SRAM macros.
> - **[REPORTED]**: URLs that another agent saw in a search snippet. I cite them as "via A1", "via A2" or "via p1-market". I did not open them myself.
> - **[UNVERIFIED: PK]**: prior knowledge from training data up to about mid-2026. Each item names its original publisher and date where I remember them, but has no URL, because the conventions forbid logging URLs I did not see.
> - **[ESTIMATE]**: my own computation, with the formula given.
>
> **Treat every UNVERIFIED die size and wafer cost as a range, not a point.** §11 lists the twelve checks to run first once web access is restored.
>
> **Phase-1b verification (agent `v4-cost`, 2026-11-01).** 24 web searches. All WebFetch attempts failed DNS (techinsights.com, siliconanalysts.com, stockhub.kr), so the new facts come from search snippets. **[REPORTED-P]** = a primary document (TechInsights, Micron, Counterpoint, TrendForce, LCSC) seen only through a search snippet. Changes: the 1β die is **36.5 mm², not 41** (TechInsights teardowns); the 1γ die is **~29 mm²**; the 4Q26 64GB RDIMM anchor is **~$1,650, not ~$1,300**; the EUV scanner costs **~$290M, not $220M**; the TSMC 28nm wafer is **~$3.0k**. Wafer cost per DRAM node is **still unverified**: no public estimate was found. Change log and sources: `research/phase1/verify_v4-cost.md`, `research/sources/v4-cost.jsonl`. The model was re-run (`models/dram_cost_stack.py`, exit 0).

---

## 1. Bottom line (the numbers the model needs)

| Quantity | Base | Range | Tag |
|---|---|---|---|
| Fully loaded 300mm wafer cost, 1α | **$3,400** | $3.0–4.0k | [ESTIMATE] §2 |
| Fully loaded 300mm wafer cost, 1β | **$3,800** | $3.2–5.5k | [ESTIMATE] §2 |
| Fully loaded 300mm wafer cost, 1γ/1c | **$4,300** | $3.7–6.0k | [ESTIMATE] §2 |
| Wafer cash cost (no depreciation), 1β | **$1,650** | $1.5–2.0k | [ESTIMATE] |
| DDR5 16Gb die, 1β | **36.5 mm²** (0.44 Gb/mm²) | 35.8–41 mm² | [ESTIMATE on REPORTED-P anchors: TechInsights Micron D1β 35.83 mm², Samsung D1b LPDDR5X 36.68 mm²] §3 (v4-cost; was 41 mm²) |
| DDR5 16Gb die, 1γ/1c | **29 mm²** (0.55 Gb/mm²) | 27.6–33.3 mm² | [ESTIMATE] from Micron's ">30% bits per wafer" 1γ claim [REPORTED-P] (v4-cost; was 33 mm²) |
| Gross die/wafer at 36.5 mm² | **1,705** | 1,514–1,739 | [ESTIMATE] formula §4 |
| Mature DRAM die yield | **0.90** | 0.85–0.95 | [UNVERIFIED: PK] |
| Back-end per 16Gb component | **$0.45** (=$0.225/GB) | $0.30–0.75 | [ESTIMATE] §5 |
| **DDR5 1β component cost** | **$1.46/GB** (model: $1.48) | **$1.15–2.54/GB** | [ESTIMATE] §6 (v4-cost; was $1.62) |
| DDR5 1β cash-only cost (glut floor) | **$0.74/GB** (model: $0.78) | $0.58–1.10/GB | [ESTIMATE] |
| **64GB DDR5 RDIMM full cost** | **$140** ($2.18/GB) | $107–238 | [ESTIMATE] §6 |
| 64GB DDR5 RDIMM contract price, 1Q26 → 4Q26 | **$927 → ~$1,650** (1,500–1,930; Citi $1,586) | — | 1Q26 [REPORTED-P] Counterpoint; 4Q26 [ESTIMATE on REPORTED] §7 |
| Implied maker gross margin on that RDIMM | **~85–92%** | 69–93% | [ESTIMATE]. Nanya reports 85.7% and Micron ~87%; the model now sits up to ~6 pp above them (see §2.3) |
| HBM3E 12-high 36GB stack cost | **$216** ($6.0/GB) | $125–514 | [ESTIMATE] §5.4 |
| DDR4 8Gb on a fully depreciated 1x/1z line | **$1.19–1.56/GB** | ±25–40% | [ESTIMATE] §9 |
| DDR4 8Gb on a *new* U.S.-style 1x line | **$3.34/GB** | $2.5–4.7/GB | [ESTIMATE] §9 |

**Decision-relevant findings**

1. **Leading-edge DDR5 costs about $1.15–2.5/GB to make, with a base of $1.5/GB** (v4-cost: smaller verified 1β die). It sells for **$14.5–26 per user-GB on server contract** (1Q26 $927 → 4Q26 ~$1,650 per 64GB RDIMM) and **$27/GB on spot**. Gross margin is about 85–90%. That agrees with the reported results of Nanya (85.7% GM, 3Q26) and Micron (~87% non-GAAP GM, FQ4-26) ([TrendForce News 2026-10-12, via p1-market](https://www.trendforce.com/news/?p=65146); [Micron via Finviz 2026-09-30, via p1-market](https://finviz.com/news/397277/micron-technology-inc-reports-record-fiscal-fourth-quarter-and-full-year-2026-results)). Two independent routes reach the same number, so the cost stack is about right.
2. **A 60% glut does not take DDR5 anywhere near cost.** A 60% fall from the ~$20/GB 4Q26 contract (raw GB; $25.8 per user-GB) leaves **~$8–10/GB, still 5.5–7× the 1β full cost.** To reach the 2023-style cost floor of about $1.3–1.8/GB, prices would have to fall **~90–94%**. **The implication is that a glut squeezes high-cost entrants long before it touches the incumbents.** Any alternative that costs more than about $8/GB in silicon plus packaging loses its price umbrella in a 2028–29 downturn (v4-cost: was $5–8/GB; the verification raised the contract anchor).
3. **New legacy DRAM capacity would be a shortage-only business.** DDR4 8Gb on a *new* line costs about **$3.3/GB**. That is about 13× below today's DDR4 spot (~$44/GB), but **2.6× above the Sep-2023 contract floor of $1.30/GB** ([KED Global 2023-10-04, via p1-market](https://www.kedglobal.com/korean-chipmakers/newsView/ked202310040013)). A depreciated Taiwanese or Korean line makes the same part for about $1.2–1.6/GB. A U.S. legacy-DRAM line is underwater in every trough.
4. **HBM3E is the *less* profitable product in 2026.** It costs about $6/GB (3× DDR5 wafer per bit) and sells for about $12/GB (re-confirmed by v4-cost; reported range $8.3–12.8/GB [REPORTED]), roughly 50% GM against 85–92% for DDR5. This matches Samsung's 1Q26 remark that conventional DRAM out-earns HBM (p1-market). HBM4 at a forecast $32–40/GB for 2027 restores the HBM premium.
5. **Back-end and module assembly are rounding errors in value terms.** Package and test are about $0.2/GB. The non-DRAM BOM plus assembly of an RDIMM is about $20, or **~1.5–2% of a $1,000+ module**. This agrees with p1-backend: U.S. assembly is not a value-capture point.
6. **Alternative memories are far off DDR5 on $/GB, and SRAM is cheaper than the folklore suggests.** Everspin's 1Gb STT-MRAM street price is about **$821/GB** (30× DDR5 spot; LCSC price re-confirmed by v4-cost [REPORTED-P]). Its silicon density is about **0.0095 Gb/mm², roughly 46× below 1β DDR5**. 28nm SRAM costs about **$78/GB in silicon**, which is about 53× DDR5's *cost* but **only ~2.9× DDR5's 2026 spot price**. Packaged discrete SRAM sells for far more: a 72Mb QDR-II+ part costs **~$1,400–3,800/GB** at broker prices [REPORTED]. SRAM on U.S. 130nm 200mm costs about $1,300/GB. IGZO-on-glass and 130nm BEOL memories are 2–5 orders of magnitude off (A1, p1-fabs).

---

## 2. Leading-edge DRAM wafer cost (300mm): 1α, 1β, 1γ/1c

### 2.1 Bottom-up build [ESTIMATE]

Formula: `wafer_cost = capex_per_wpm × tool_share / tool_years / (12 × util) + capex_per_wpm × (1 − tool_share) / bldg_years / (12 × util) + cash_cost`. It uses tool share 0.78, tool life 5 years, building life 25 years and utilization 0.95. Cash cost covers materials and consumables (prime wafer ~$100–130, resists including EUV, gases, chemicals, CMP, targets, mask amortization), labor and overhead, utilities and spares. It excludes R&D.

| Node | Greenfield capex per wpm | Depreciation per wafer | Cash cost per wafer | **Fully loaded** | Range used |
|---|---|---|---|---|---|
| 1α (1a, 14nm-class) | $130k (110–150k) | $1,879 | $1,550 | **$3,429** | $3.0–4.0k |
| 1β (1b, 12nm-class) | $145k (120–180k) | $2,096 | $1,650 | **$3,746** | $3.2–5.5k |
| 1γ/1c (11nm-class) | $170k (140–210k) | $2,458 | $1,850 | **$4,308** | $3.7–6.0k |

Notes:
- The capex-per-wpm inputs are analyst rules of thumb from memory ($1.1–2.1B per 10k wpm of new DRAM capacity) [UNVERIFIED: PK]. This is the softest input in the wafer cost. A ±$30k/wpm change moves the wafer cost by about ±$430.
- The 1β high case of $5.5k matches the Phase-2 assumptions in A1 ($5.5k) and A2 ($6.0k) (`research/phase2/A1_device_params.json`, `A2_device_params.json`). It represents a new fab running under-loaded, or a cost that includes start-up. **Recommendation:** model $3.8k as the steady-state incumbent cost and $5.5k as the "new entrant / new fab" cost.
- **Depreciation is about 55% of the leading-edge wafer cost.** That is why incumbents can keep running fully depreciated lines through a glut at about the cash cost, ~$1.5–2.0k per wafer, which is about $0.81/GB for 1β DDR5 (§6).

### 2.2 Top-down cross-check, 2023 [ESTIMATE on UNVERIFIED: PK inputs]

The 2023 inputs:
- DRAM industry revenue was about **$48–52B** [UNVERIFIED: PK].
- Makers ran at about breakeven gross margin. SK hynix's 1Q23 operating margin was about −67% (KRW −3.4T on KRW 5.1T) ([The Register 2023-04-27, via p1-market](https://www.theregister.com/2023/04/27/samsung_sk_hynix_losses/)).
- Industry capacity was about 1.65–1.75M wpm [UNVERIFIED: PK]. Utilization was cut to about 74–82% in 2Q23 (TrendForce via p1-market).

The arithmetic: about 16M wafers processed, so COGS ≈ **$2.8–3.2k per wafer**. Removing a 12–15% back-end share leaves a **blended front-end of ~$2.4–3.1k per wafer** across a fleet that was mostly 1x/1y/1z and part-depreciated. That fits a leading-edge (1α/1β) full cost of about $3.4–3.8k and an older-node cost of about $2.0–2.5k.

### 2.3 Margin cross-check, 2026

At the base 1β cost of $1.62/GB (§6), contract RDIMM pricing of $14–25 per user-GB implies a GM of about 85–90% (§7). The reported GMs are Nanya 85.7% (3Q26) and Micron about 87% (FQ4-26) (p1-market). **If my wafer cost were 2× too low, the implied GM would be about 75–80%, inconsistent with the reported margins.** This brackets the wafer cost from above more tightly than any single source.

**v4-cost update (2026-11-01).** With the verified 1β die (36.5 mm²), base cost falls to $1.46–1.48/GB. The 4Q26 contract anchor rises to ~$1,650 per RDIMM, or ~$20.4 per raw GB. The model GM is therefore **~93% at 4Q26 and ~92% at 3Q26**, about 5–6 pp above Micron (87%) and Nanya (85.7%). Part of that gap is expected: reported GMs trail the 4Q26 price and include HBM, NAND and older nodes. Part of it hints that the **$3.8k 1β wafer cost may be low**. A ~$5k wafer would close the gap, and the higher EUV scanner price below points the same way. This does not change any decision: GM stays above 88% either way.

### 2.4 EUV layers and the cost per layer

| Maker / node | EUV layers | Status / tag |
|---|---|---|
| Samsung 1a (14nm DDR5) | **5** | Samsung newsroom, Oct 2021 [UNVERIFIED: PK, high confidence] |
| SK hynix 1a | **1** | Jul 2021 [UNVERIFIED: PK] |
| Micron 1β | **0** (DUV multipatterning) | Nov 2022 [UNVERIFIED: PK, high confidence] |
| Micron 1γ | **1** (first Micron EUV node; samples Feb 2025) | EUV with "reduced EUV use" vs Korean peers ([TrendForce News 2025-03-11](https://www.trendforce.com/news/2025/03/11/news-micron-pioneers-1%ce%b3-ddr5-samples-with-reduced-euv-use-but-future-risks-loom/)) [REPORTED]; the exact count of 1 is [UNVERIFIED: PK] |
| Samsung 1b / SK hynix 1b | ~5–6 / ~3–5 | press [UNVERIFIED] |
| Samsung 1c / SK hynix 1c | ~6–7 / **6** | SK hynix is raising 1c EUV to a sixth layer ([TechNews 2025-08-12](https://technews.tw/2025/08/12/euv-sk-hynix-1c-dram/)) [REPORTED]. Samsung 1c is [UNVERIFIED] |
| CXMT (all nodes) | **0**: EUV cannot be shipped to China | [REPORTED: PK, export-control fact] |

Cost per EUV layer [ESTIMATE]:
- An EUV scanner costs **~$290M** (corrected by v4-cost from $220M). SK hynix is buying 30+ ASML EUV tools for KRW 11.95T, about $8.8B, with deliveries through 2027 ([S&P Global 2026-03](https://www.spglobal.com/market-intelligence/en/news-insights/research/2026/03/sk-hynix-invests-in-euv-as-ai-boom-tightens-conventional-dram-supply)) [REPORTED]. Over 5 years, plus about $12M a year in service and about $0.8M a year in power, at about 0.91M exposures a year (80% uptime × 130 wph effective), that is **≈ $78 per exposure** (was $62).
- Adding track, metrology, reticles and the dep/etch module around the exposure gives **≈ $115–270 per wafer per EUV layer** (base $165).
- One EUV layer usually *replaces* a DUV SAQP sequence of similar or greater cost. **EUV is therefore a yield and cycle-time lever, not a large wafer-cost adder.** At a 1c-class 6 layers it adds roughly $600–1,500 per wafer before netting off the DUV steps it removes.

### 2.5 Company density and productivity claims (for scaling the model)

| Transition | Claimed gain | Tag |
|---|---|---|
| Micron 1z → 1α | ~40% density | [UNVERIFIED: PK, Jan 2021] |
| Micron 1α → 1β | >35% density | [UNVERIFIED: PK, Nov 2022] |
| Micron 1β → 1γ | >30% more bits per wafer (16Gb DDR5), ~20% lower power | Bits-per-wafer claim confirmed ([Micron 1γ technology brief](https://micron.cn/content/dam/micron/global/public/products/technical-marketing-brief/1-gamma-technology-brief.pdf)) [REPORTED-P]; power claim [UNVERIFIED: PK, Feb 2025] |
| SK hynix 1b → 1c | >30% "productivity" (net die per wafer) | [UNVERIFIED: PK, Aug 2024] |

Applying these claims literally to the reported Micron 1z DDR5 density of 0.241 Gb/mm² gives 1α 0.34, 1β 0.46 and 1γ 0.59 Gb/mm². Teardown figures run lower, because company claims usually quote the best product or the array alone. I use 0.30, 0.39 and 0.48 as base values and keep the claim-implied values as the upper edge of the ranges (§3).

**v4-cost correction (2026-11-01):** the teardowns came in close to the claims. TechInsights measured Micron D1β 16Gb DDR5 at 35.83 mm², or 0.447 Gb/mm², and Samsung D1b 16Gb LPDDR5X at 0.436 Gb/mm² (§3.1). The base values are now **0.30 / 0.438 / 0.55 Gb/mm²**. **The net cost-per-bit decline is about 10–20% per node** [ESTIMATE]: roughly 25–30% density gain against 10–15% wafer-cost growth.

---

## 3. Die sizes and bit densities

### 3.1 DDR5

| Part | Node | Die (mm²) | Gb/mm² | Tag / source |
|---|---|---|---|---|
| CXMT 16Gb DDR5 | G4 (~16nm-class; F = 16.0 nm, cell 0.0020 µm²) | **66.99** (8.19 × 8.18 mm) | **0.239** | TechInsights teardown, reported ([SemiWiki, via A1](https://semiwiki.com/forum/threads/chinas-cxmts-ddr5-reveals-3-year-technology-gap.23270/latest); [TechInsights CXMT G4](https://www.techinsights.com/blog/cxmt-g4-16gb-ddr5-dram-process-analysis)) [REPORTED]. Re-confirmed by v4-cost. XenoSpectrum's 68.06 mm² is an outlier |
| Micron 16Gb DDR5 | 1z | **66.26** | **0.241** | [TechInsights](https://www.techinsights.com/ja/node/37203) [REPORTED-P]. Samsung D1y 73.58 mm² / 0.217; SK hynix D1y 75.21 mm² / 0.213 (same source) |
| SK hynix 16Gb DDR5 (D1a EUV) | 1α | **52.61** (die seal; 53.27 full) | **0.304** | [TechInsights](https://www.techinsights.com/blog/sk-hynix-d1a-euv-16-gb-ddr5-dram-transistor-characteristics) [REPORTED-P] |
| 16Gb DDR5 (Samsung/SK hynix/Micron) | 1α | **53** (48–57) | 0.30 (0.28–0.33) | Confirmed by the SK hynix D1a row (v4-cost). The low end matches a Samsung 16Gb DDR5 die of 48.90 mm², node not stated ([XenoSpectrum](https://xenospectrum.com/ddr5-memory-chips-from-chinas-cxmt-40-larger-die-size-than-samsung-highlighting-challenges/)) [REPORTED] |
| **Micron 16Gb DDR5 (Y52K, D1β)** | 1β | **35.83** (6.33 × 5.66 mm, die seal; 36.00 full) | **0.447** | [TechInsights](https://techinsights.com/ja/node/57875) [REPORTED-P] |
| Samsung 16Gb LPDDR5X (D1b) | 1b | **36.68** | **0.436** | TechInsights via [ETN.fi](https://etn.fi/index.php/embedded-conference-finland/13-news/16863-samsung-ahtaa-jo-dram-gigabitin-reiluun-2-nelioemilliin) [REPORTED-P]. This is the "0.436" in Kurnal's chart |
| 16Gb DDR5 | 1β | **36.5** (35.8–41) | **0.438** (0.39–0.447) | [ESTIMATE on REPORTED-P anchors] (v4-cost; was 41 mm² / 0.39) |
| 24Gb DDR5 (non-binary; 24/48/96GB modules) | 1β | **54.8** (53.7–61.5) | 0.438 | [ESTIMATE] linear (was 61.5) |
| 32Gb DDR5 (Samsung 12nm-class 32Gb, Sep 2023; ISSCC 2024 paper 13.2, "5th-gen 10nm"; 128GB RDIMMs without TSV) | 1β | **73** (71.6–80) | ~0.44 | [ESTIMATE] (was 80). Die area not public ([All About Circuits](https://allaboutcircuits.com/news/isscc-2024-samsung-doubles-ddr5-capacity-with-symmetric-mosaic-architecture); [Samsung](https://news.samsung.com/global/samsung-electronics-unveils-industrys-first-and-highest-capacity-12nm-class-32gb-ddr5-dram-ideal-for-the-ai-era)) |
| 16Gb DDR5 | 1γ/1c | **29.1** (27.6–33.3) | 0.55 (0.48–0.58) | [ESTIMATE] (was 33). Micron says 1γ gives >30% more bits per wafer than 1β ([Micron brief](https://micron.cn/content/dam/micron/global/public/products/technical-marketing-brief/1-gamma-technology-brief.pdf)) [REPORTED-P], which implies ≤27.6 mm². TechInsights published a Micron Y62E D1γ analysis (2026-05-14), but its die area was not visible. Samsung reportedly enlarged its 1c die to recover yield [UNVERIFIED: PK] |
| 32Gb DDR5 | 1γ/1c | **58** (55–67) | 0.55 | [ESTIMATE] (was 67) |

The original note had one teardown anchor, the CXMT/Micron 1z pair, reached only through a snippet. **v4-cost added 1α and 1β anchors from TechInsights** (via snippets). The **"3-year technology gap"** framing shows that CXMT's 2024-era DDR5 matched a 2021-era Western node in density [REPORTED]. **No die size for a newer (2025–26) CXMT DDR5 node was found** [STILL UNVERIFIED].

DDR5 overheads:
- On-die ECC adds 8 check bits per 128 data bits (6.25%). It is *already inside* the quoted die densities [UNVERIFIED: PK, JEDEC JESD79-5].
- An RDIMM adds 25% of bits as side-band ECC: 2 subchannels × (32 + 8) bits [UNVERIFIED: PK]. A 64GB RDIMM therefore carries 80GB of raw DRAM.

### 3.2 LPDDR5X

| Part | Node | Die (mm²) | Tag |
|---|---|---|---|
| 16Gb LPDDR5X | 1β | **36.7** (35.8–40) | Samsung D1b measured 36.68 mm² (TechInsights via [ETN.fi](https://etn.fi/index.php/embedded-conference-finland/13-news/16863-samsung-ahtaa-jo-dram-gigabitin-reiluun-2-nelioemilliin)) [REPORTED-P] (v4-cost; was 40) |
| 24Gb LPDDR5X (12GB phone packages) | 1β | **55** (53.7–60) | [ESTIMATE] at 0.436 Gb/mm² (was 60) |

### 3.3 HBM core dies and the TSV/IO penalty

| Item | Value | Tag |
|---|---|---|
| HBM3E 24Gb core die (1β/1b) | **~110 mm²** (95–125) → ~0.22 Gb/mm² | [UNVERIFIED: PK] |
| HBM4 core die (24–32Gb, 2048-bit IO) | **~125 mm²** (110–140) | [UNVERIFIED: PK] |
| HBM die area vs DDR5 of the same capacity and node | **1.35–1.45×** (TSV arrays and keep-out, wide IO, power delivery) | TrendForce 2024 note [UNVERIFIED: PK] |
| HBM yield vs DDR5 (including TSV/stacking) | **20–30% lower** | TrendForce 2024 note [UNVERIFIED: PK] |
| HBM3E wafer trade ratio (wafers per bit vs DDR5) | **~3:1**, "widening with every generation" | Micron ([Tom's Hardware 2026, via p1-market](https://www.tomshardware.com/tech-industry/semiconductors/micron-says-the-silicon-gap-between-hbm-and-ddr5-is-widening-with-every-generation); [XenoSpectrum, via p1-market](https://xenospectrum.com/en/micron-hbm-ddr-silicon-gap/)) [REPORTED] |
| HBM4 trade ratio | **~3.5:1** (3.0–4.5) | [ESTIMATE]: Micron says it rises; the HBM4 figure is undisclosed |
| HBM4 base die | moves to a logic process (TSMC 12nm/N5/N3 for SK hynix; Samsung 4nm in-house) | [UNVERIFIED: PK] |

The 3:1 trade ratio decomposes as about 1.4× area × about 1.3× yield loss × about 1.4× other factors (stack yield, test, slower bit growth). That is roughly consistent with the components above [ESTIMATE].

### 3.4 DDR4 / DDR3 (legacy). See also §9

| Part | Node | Die (mm²) | ~Gb/mm² | Tag |
|---|---|---|---|---|
| DDR4 8Gb | 20nm-class (2014–15) | 80 (70–90) | ~0.10 | [UNVERIFIED: PK] |
| DDR4 8Gb | 1x (18–19nm) | 55 (50–62) | ~0.15 | [UNVERIFIED: PK] |
| DDR4 8Gb, CXMT G1 19nm (2019) | 19nm | 62 (55–70) | ~0.13 | [UNVERIFIED: PK] |
| DDR4 8Gb, Nanya 10nm-class gen-1 ("1A") | ~1x | 58 (50–65) | ~0.14 | [UNVERIFIED: PK] |
| DDR4 8Gb | 1y | 45 (41–50) | ~0.18 | [UNVERIFIED: PK] |
| DDR4 8Gb | 1z | 39 (35–45) | ~0.21 | [UNVERIFIED: PK]; p1-backend used 45 |
| DDR4 16Gb | 1z | 76 (68–84) | ~0.21 | [UNVERIFIED: PK] |
| DDR3 4Gb | 25nm-class (Winbond/Nanya/PSMC) | 60 (50–70) | ~0.067 | [UNVERIFIED: PK] |
| DDR3 4Gb | 30–38nm-class | 80 (70–100) | ~0.05 | [UNVERIFIED: PK] |
| DDR3 2Gb | 38nm-class | 50 (44–60) | ~0.04 | [UNVERIFIED: PK] |

### 3.5 Cell-size reference (for device-comparison models)

- Commodity DRAM cell = **6F²**. CACTI's comm-DRAM cell is 0.0486 µm² at 90nm, 0.02535 at 65nm, 0.01215 at 45nm and 0.006144 at 32nm, and it projects 4F² (0.001936 µm²) at 22nm ([HP CACTI](https://github.com/HewlettPackard/cacti)) [VERIFIED]. Production 4F² vertical-channel DRAM is a roughly 2028+ roadmap item (A1).
- Embedded (logic-process) DRAM cell is about **21–31F²** in CACTI's LP-DRAM tables [VERIFIED].
- SRAM 6T cell is **146F²** in CACTI [VERIFIED]. The real sky130 130nm bitcell is **1.200 × 1.580 µm = 1.896 µm²** (dual-port 3.792 µm²) ([SkyWater sky130_fd_bd_sram LEF](https://github.com/google/skywater-pdk-libs-sky130_fd_bd_sram)) [VERIFIED]. 1.896 µm² is about 112F² at F = 130nm.

---

## 4. Gross dies per wafer, edge exclusion, yield

**Formula** (the form used in Chiplet Actuary's `exploration.py`, opened) [VERIFIED]:

`GDPW = π·(d_eff/2)² / S − π·d_eff / √(2·S)`, with `d_eff = 300 − 2·edge_exclusion` and `S = (√die_area + scribe)²`.

**Parameters:**
- Edge exclusion: **3 mm** base (2–5 mm). Chiplet Actuary uses 5 mm ([repo](https://github.com/Yinxiao-Feng/DAC2022)) [VERIFIED as its parameter].
- Scribe lane: **80 µm** base (60–200 µm). Chiplet Actuary uses 200 µm [VERIFIED].

| Die mm² | 30 | 35 | 40 | 45 | 50 | 55 | 60 | 70 | 80 | 100 | 110 | 125 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GDPW (3mm EE, 80µm scribe) | 2,081 | 1,779 | 1,553 | 1,377 | 1,236 | 1,121 | 1,025 | 874 | 761 | 603 | 546 | 477 |
| GDPW (5mm EE, 200µm scribe) | 1,936 | 1,660 | 1,453 | 1,291 | 1,161 | 1,054 | 965 | 825 | 719 | 572 | 518 | 453 |

**Yield models:**
- **Negative binomial:** `Y = (1 + A·D0/α)^−α` with α = 10. Both Chiplet Actuary and ECO-CHIP use this [VERIFIED].
- **Defect density D0:** ECO-CHIP gives **0.05–0.2 /cm²** across its nodes. Chiplet Actuary gives 0.07 /cm² at 28–55nm and 0.2 at 3nm ([ECO-CHIP](https://github.com/ASU-VDA-Lab/ECO-CHIP)) [VERIFIED].
- **DRAM uses redundancy repair:** spare rows and columns are programmed by laser or eFuse after wafer sort. The logic-style D0 model therefore applies only to the unrepairable (periphery) fraction. In the model, use die yield directly:
  - **mature 0.90** (0.85–0.95) [UNVERIFIED: PK heuristic];
  - **new-node ramp 0.60** (0.30–0.80);
  - **1c/1γ in 2026 at 0.80** [ESTIMATE];
  - Samsung's 1c was reported in Korean press at about 30–40% in 2024, rising to about 50–70% in 2025 [UNVERIFIED: PK].
- **HBM:** a 12-high HBM3E stack yields **0.75** (0.60–0.90). SK hynix said its HBM3E yield was "nearly 80%" (FT, May 2024) [UNVERIFIED: PK].
- **Bonding:** about 0.99 per bonded die (ECO-CHIP) [VERIFIED as a model parameter].
- **Module:** module yield 0.985 [ESTIMATE].

---

## 5. Back-end: test, packaging, modules, HBM stacking

### 5.1 Component back-end (DDR5 16Gb single-die FBGA) [ESTIMATE]

| Step | $/die | Notes |
|---|---|---|
| Wafer probe / sort (hot and cold) plus redundancy analysis and repair | **0.10** (0.05–0.15) | Massively parallel memory ATE (Advantest T5xxx, Teradyne Magnum class) |
| FBGA assembly (78/82/102-ball, BT substrate) | **0.18** (0.10–0.35) | p1-backend puts assembly-only at Asian scale below $0.10 |
| Final test plus burn-in (at speed) | **0.17** (0.10–0.30) | DDR5 test times are long |
| **Total** | **0.45** (0.30–0.75) | **≈ $0.225/GB** (0.15–0.40). About 10–15% of COGS at trough prices |
| Legacy DDR4 8Gb / DDR3 4Gb | ~$0.30/die | ≈ $0.30/GB / $0.60/GB |
| KGD premium over the packaged equivalent | +15–40% | p1-backend (`research/phase1/us_backend.md`) |

### 5.2 Module BOM [UNVERIFIED: PK unit prices; ESTIMATE totals]

| Item | 64GB DDR5 RDIMM (2Rx4) | 16GB DDR5 UDIMM (1Rx8) |
|---|---|---|
| DRAM devices | 40 × 16Gb x4 (80GB raw, incl. 25% ECC). With 32Gb dies: 20 | 8 × 16Gb x8 (no side-band ECC) |
| RCD (Renesas / Rambus / Montage) | $7 (4–12) | n/a |
| PMIC | $3.5 (12V server; 2–6) | $1.5 (5V client; 0.8–2.5) |
| SPD5118 hub with integrated temperature sensor | $0.7 (0.4–1.2) | $0.7 |
| Discrete temperature sensors | 2 × $0.35 | n/a |
| PCB | $4 (10–12 layer; 2.5–8) | $1.5 (8 layer) |
| Passives | $1.2 | $0.5 |
| **Non-DRAM parts** | **$17.1** (11–25) | **~$4.2** |
| Assembly and module test (incl. burn-in for server) | $3.5 in Asia (2–6); **~$12 in the U.S.** (p1-backend) | $1.5 |
| MRDIMM adder (MRCD + 10 MDB) | +$30 (20–45) | n/a |

p1-backend's RDIMM parts estimate is higher, at about $25 (RCD $8, PMIC $5, SPD and sensors $2, PCB $8, passives $2), because it assumes U.S. low-volume pricing. Both estimates agree that the parts are **under 3% of a 2026 module's price**.

### 5.3 TSV and stacking [ESTIMATE]

| Item | Value |
|---|---|
| TSV formation (via-middle) plus thinning, backside reveal and microbumps, per DRAM core wafer | **+$650/wafer** (450–1,000) |
| 12-high stacking (TC-NCF or MR-MUF), molding, stack test | **$25/stack** (15–45) |
| Base die: HBM3E (DRAM process) / HBM4 (logic process) | $15 (8–30) / $35 (15–60) |

### 5.4 HBM3E 12-high 36GB stack cost [ESTIMATE]

Formula: `(12 × (wafer + TSV adder) / (GDPW × core yield) + base die + stacking) / stack yield`

| Case | Core die | GDPW | $/core die | **Stack** | **$/GB** |
|---|---|---|---|---|---|
| Low | 100 mm², wafer $3.5k + $450 TSV, core yield 0.88, stack yield 0.90 | 603 | 7.44 | **$125** | **3.5** |
| Base | 110 mm², $3.8k + $650, 0.80, 0.75 | 546 | 10.19 | **$216** | **6.0** |
| High | 125 mm², $5.5k + $1,000, 0.70, 0.60 | 477 | 19.45 | **$514** | **14.3** |

Against these costs, HBM3E sold at about **$1.50/Gb = $12/GB** in 2026 ([Sammy Fans 2026-10-02, via p1-market](https://www.sammyfans.com/2026/10/02/samsung-seeks-more-than-3x-hbm3e-pricing-for-hbm4/)). HBM4 is forecast at **$4–5/Gb = $32–40/GB** for 2027 ([Silicon Analysts 2026-10-07, via p1-market](https://siliconanalysts.com/market/samsung-hbm4-2027-pricing-set-to-more-than-double-2026-10-07)) [REPORTED].

v4-cost re-check (2026-11-01, via search snippets) [REPORTED]:
- HBM3E is about $1.50–1.60/Gb, or **$12–12.8/GB**, per DigiTimes (Jul 2026) ([Capital & Compute](https://capitalandcompute.net/memory-prices/hbm/)). Silicon Analysts is lower at **$8.33/GB** for a 36GB stack ([Silicon Analysts](https://siliconanalysts.com/data/hbm-pricing)).
- **HBM4 is about $2.00/Gb (~$16/GB) in 2H26** ([Capital & Compute](https://capitalandcompute.net/memory-prices/hbm/)). SK hynix reportedly asked ~$600 per 12-high stack, or $16.7/GB ([SemiconSam](https://semiconsam.substack.com/p/a-memory-down-cycle-is-coming-but)).
- The $32–40/GB figure for 2027 is a **proposal or forecast**: Samsung is proposing a mid-to-high $4/Gb. It is not a transacted price.
- Fubon puts the buyer-side cost at $17–18/GB for HBM3E and $31–32/GB for HBM4 ([TrendForce News](https://www.trendforce.com/news/?p=62555)). That conflicts with the $12/GB figure.
- **HBM3E GM is therefore about 28–67%** ($8.3–18/GB against a $6/GB cost). It stays below DDR5 at every point. HBM3E therefore earns roughly 50% GM against 85–90% for DDR5. That explains why makers in 2026 have **not** been diverting more wafers to HBM3E, and why they are pushing HBM4 prices up about 3×.

---

## 6. The computed cost stack

### 6.1 Component cost per GB (16Gb DDR5; mature yield 0.90 unless noted) [ESTIMATE]

| Node / part | Die mm² | Gross die/wafer | Wafer $ | Front-end $/GB | + back-end | **Component $/GB** |
|---|---|---|---|---|---|---|
| 1z 16Gb DDR5 (reference) | 66.4 | 923 | 3,000 | 1.80 | 0.23 | **2.03** |
| 1α 16Gb DDR5, base | 53.3 | 1,157 | 3,400 | 1.63 | 0.23 | **1.86** |
| 1β 16Gb DDR5, low (0.447 Gb/mm², $3.2k, y 0.92) | 35.8 | 1,739 | 3,200 | 1.00 | 0.15 | **1.15** |
| **1β 16Gb DDR5, base** (v4-cost; was 41.0 mm² → $1.62) | **36.5** | **1,705** | **3,800** | **1.24** | **0.23** | **1.46** |
| 1β 16Gb DDR5, high (0.39 Gb/mm², $5.5k, y 0.85) | 41.0 | 1,514 | 5,500 | 2.14 | 0.40 | **2.54** |
| 1γ/1c 16Gb DDR5, base, mature (v4-cost; was 33.3 mm² → $1.50) | 29.1 | 2,146 | 4,300 | 1.11 | 0.23 | **1.34** |
| 1γ/1c 16Gb DDR5, 2026 ramp (y 0.80) | 29.1 | 2,146 | 4,300 | 1.25 | 0.23 | **1.48** |
| 1γ/1c 16Gb DDR5, high ($6k, y 0.70) | 33.3 | 1,872 | 6,000 | 2.29 | 0.40 | **2.69** |
| 1β cash cost only (no depreciation; glut floor) | 36.5 | 1,705 | 1,650 | 0.54 | 0.20 | **0.74** (0.58–1.10) |

The rows above use this note's simple formula. `models/dram_cost_stack.py` scales back-end cost by die capacity and applies yield per die area, so it gives slightly higher figures after the v4-cost update: 1β $1.48, 1γ ramp $1.51, 1γ mature $1.36, cash $0.78 per GB (`research/phase1/cost_stack_output.md`).

Reading the table:
- **The step from 1β to 1γ/1c saves only about 8% per GB at mature yield, and almost nothing during the 2026 ramp.** The node transition is about bits per wafer (capacity), not cost.
- **A wafer-cost error of ±$1k moves $/GB by about ±$0.33.** A density error of ±0.05 Gb/mm² moves it by about ±$0.13–0.16. Those two inputs dominate the uncertainty. Since v4-cost, density is anchored on teardowns, so **wafer cost is now the single dominant unknown**.

### 6.2 64GB DDR5 RDIMM [ESTIMATE]

| Case | DRAM (40 × 2GB) | Non-DRAM parts | Assembly and test | **Module cost** (÷0.985 yield) | $/user-GB |
|---|---|---|---|---|---|
| Low | $92 | $11 | $2 | **$107** | 1.67 |
| **Base** (v4-cost; was $152) | **$117** | **$17.1** | **$3.5** | **$140** | **2.18** |
| High | $203 | $25 | $6 | **$238** | 3.71 |

(The model gives $141 base, `cost_stack_output.md`.)

---

## 7. Market prices to compare, and implied margins

All prices below come through other agents' search snippets, so they are [REPORTED] at best. See `research/phase1/market.md` for the full series.

| Product | Date | Price | $/GB | Source |
|---|---|---|---|---|
| DDR5 16Gb spot (DRAMeXchange session avg; range) | 2026-08-31 | **$53.92** ($37.20–67.50) | ~27 | [BuySellRAM, via p1-market](https://www.buysellram.com/blog/ram-market-update/) |
| DDR5 16Gb spot, daily high | early Jul 2026 | $61.00 | 30.5 | [Tech-Insider, via p1-market](https://tech-insider.org/ddr5-ram-prices-2026/) |
| DDR5 16Gb spot, pre-spike | 2025-09-20 | $6.84 | 3.4 | same |
| DDR5 16Gb spot, 2023 trough | 2Q–3Q23 | ~$3.2 (2.8–3.6) | ~1.6 | [UNVERIFIED: PK] |
| **DDR5 16Gb contract, derived** | 4Q26 | **~$41** ($37–48) | ~20 | [ESTIMATE]: RDIMM contract ($1,650; 1,500–1,930) minus ~$20.6 non-DRAM, ÷40 dies (v4-cost; was ~$31). **No published Oct-2026 DDR5 16Gb contract price was found** [STILL UNVERIFIED] |
| DDR5 16Gb spot, Oct-2026 average (market expectation) | Oct 2026 | ~51% odds of >$51.50 | ~26 | Prediction market, not a reported price ([Kalshi](https://kalshi.com/markets/kxddr5ms/monthly-ddr5-16gb-2gx8-48005600/kxddr5ms-26oct)) |
| 64GB DDR5 RDIMM contract | 4Q25 | $450 | 7.0 | Counterpoint ([EE Times Asia, via p1-market](https://www.eetasia.com/memory-prices-surging-by-90-from-4q-2025/)) |
| 64GB DDR5 RDIMM contract | 1Q26 | **$927** (March compensation price $1,135) | 14.5 | Counterpoint ([Apr-2026 tracker](https://counterpointresearch.com/de/reports/memory-price-tracker-april-2026)) [REPORTED-P]; confirmed by v4-cost (was ">$900") |
| 64GB DDR5 RDIMM contract, forecast | 3Q26F | ~$1,500 | 23.4 | Counterpoint (Apr 2026), same tracker [REPORTED-P]. In July, Counterpoint raised its 3Q26 DRAM forecast to +10–20% QoQ ([Jul-2026 tracker](https://counterpointresearch.com/en/reports/memory-price-tracker-and-forecast-july-2026)) |
| 64GB DDR5 RDIMM contract, forecast | 4Q26F | $1,586 (from $873 in 1Q26) | 24.8 | Citi note, May 2026, via a secondary relay ([Servnet UK](https://www.servnetuk.com/research/ddr5-server-memory-price-tracker-2026)) [REPORTED]; was [UNVERIFIED] |
| **64GB DDR5 RDIMM contract, model anchor** | 4Q26 | **~$1,650** (1,500–1,930) | 25.8 | [ESTIMATE] v4-cost: the 3Q26F ~$1,500 × TrendForce 4Q26 +10–15%. High = $927 × TrendForce 2Q–4Q QoQ. Replaces p1-model's $1,300 |
| 64GB DDR5 RDIMM street | Aug 2026 | ~$2,064 | ~32 | [Servnet UK, via p1-market](https://www.servnetuk.com/research/ddr5-server-memory-price-tracker-2026) |
| DDR5 retail, typical | Sep 2026 | — | **18.04** | [rampricesusa, via p1-market](https://rampricesusa.com/insights/monthly/2026-09) |
| 32GB DDR5 retail kit | 2026 | ~$450 (409–470) | ~14 | [Digital Citizen, via p1-market](https://www.digitalcitizen.life/ddr5-ram-prices-surge-in-2026-as-32gb-kits-reach-450-amid-global-memory-shortage/) |
| DDR4 8Gb contract (cycle bottom) | Sep 2023 | **$1.30** | 1.30 | [KED Global, via p1-market](https://www.kedglobal.com/korean-chipmakers/newsView/ked202310040013) |
| DDR4 8Gb contract | Jun 2025 | $2.60 | 2.60 | [Asia Economy, via p1-market](https://view.asiae.co.kr/en/article/2025070108020310879) |
| DDR4 8Gb spot | 2026-08-31 | $44.37 (23.80–76.00) | 44 | [BuySellRAM, via p1-market](https://www.buysellram.com/blog/ram-market-update/) |
| DDR4 8Gb (1Gx8 3200) spot | 2026-10-20 | **$46.357** (+0.84% WoW) | 46 | [TrendForce News 2026-10-21](https://www.trendforce.com/news/?p=65594) [REPORTED-P] (v4-cost) |
| DDR4 16Gb 3200 spot | 2026-08-31 | $91.78 (eTT $11.53) | 45.9 | [BuySellRAM](https://www.buysellram.com/blog/ram-market-update/) [REPORTED]. **No Oct-2026 DDR4 16Gb contract or spot price was found** |
| DDR4 contract, MoM | Oct 2026 | +4% MoM, +24% over 3 months | — | An unnamed bank, via [Guru3D](https://www.guru3d.com/story/ddr4-memory-prices-now-also-rise-as-dram-supply-shortages-intensify-through-2028/) [REPORTED] |
| DDR3 4Gb spot | early Jul 2026 | $3.19/Gb | 25.5 | [Wccftech, via A2](https://wccftech.com/memory-shortages-drive-ddr4-prices-over-50-in-q3-2026-ddr3-also-impacted-by-higher-costs/) |
| HBM3E / HBM4 | 2026 / 2H26 / 2027F | $1.50/Gb / ~$2.00/Gb / $4–5/Gb | 12 (8.3–12.8) / ~16 / 32–40 | §5.4; re-checked by v4-cost [REPORTED] |
| Conventional DRAM contract, QoQ | 4Q26F | +10–15% | — | [TrendForce 2026-09-30, via p1-market](https://www.trendforce.com/presscenter/news/20260930-13258.html). Confirmed by v4-cost across several snippets |
| DRAM contract, QoQ (claimed October revision) | 4Q26F | "~+20%" | — | **Not confirmed.** The only source is an AI-generated summary dated 2026-10-20 ([StockHub](https://www.stockhub.kr/en/news/news_b7244c205001)); no TrendForce release was found. TrendForce's 2026-09-23 bulletin headline says it lifted the 4Q26 outlook ([TrendForce](https://trendforce.com/research/download/RP260923EN)) [REPORTED]. Kept only as the high case |

**Implied margins** (64GB RDIMM; base module cost $140 after v4-cost, was $152) [ESTIMATE]:

| RDIMM contract price | $/user-GB | Implied DRAM $/raw-GB | Implied 16Gb chip | Maker GM at base cost |
|---|---|---|---|---|
| $450 (4Q25) | 7.0 | 5.37 | $10.7 | 69% |
| $927 (1Q26, REPORTED-P) | 14.5 | 11.33 | $22.7 | 85% |
| $1,000 (2Q26) | 15.6 | 12.24 | $24.5 | 86% |
| $1,586 (4Q26F Citi, REPORTED) | 24.8 | 19.57 | $39.1 | 91% |
| $1,650 (4Q26 model anchor) | 25.8 | 20.37 | $40.7 | 92% |

Reported benchmarks:
- Nanya 3Q26 GM 85.7% ([TrendForce News, via p1-market](https://www.trendforce.com/news/?p=65146)).
- Micron FQ4-26 non-GAAP GM about 87% and FQ1-27 guide 86.25% ([Finviz, via p1-market](https://finviz.com/news/397277/micron-technology-inc-reports-record-fiscal-fourth-quarter-and-full-year-2026-results)).
- SK hynix 3Q26 operating margin about 79.7% ([Placera/SK hynix, via p1-market](https://www.placera.se/pressmeddelanden/sk-hynix-announces-3q26-financial-results-20261028)).
- At the trough, SK hynix posted a 1Q23 operating margin of about −67% (§2.2).

**The cost stack reproduces the reported margins**, which is the best validation available without TechInsights access. After v4-cost, the model sits ~5–6 pp above them (§2.3). Spot ($27/GB, Aug 2026) runs about **1.3×** the derived contract price (~$20/GB raw; was "~2× of ~$15"). Spot is thin and panic-priced (p1-market).

### 7.1 Glut test (mission rule 6) [ESTIMATE]

Updated by v4-cost (2026-11-01). Full cost is now $1.46, was $1.62; cash cost $0.74, was $0.81. The 4Q26 contract is ~$20/GB raw, was ~$15.

| Starting price (DDR5 $/GB) | After −60% | Multiple of 1β full cost ($1.46) | Multiple of 1β cash cost ($0.74) |
|---|---|---|---|
| $12 | $4.8 | 3.3× | 6.5× |
| $15 (p1-cost's original 4Q26 estimate) | $6.0 | 4.1× | 8.1× |
| $20 (≈ 4Q26 contract, raw GB; model $20.4) | $8.0 | 5.5× | 10.8× |
| $25 (Citi 4Q26F RDIMM; model RDIMM $25.8 per user-GB) | $10.0 | 6.8× | 13.5× |
| $27 (Aug-26 spot) | $10.8 | 7.4× | 14.6× |

From the ~$20/GB 4Q26 contract, a **−91–94%** fall is needed to reach the 2023 floor of about $1.3–1.8/GB (was −85–90% from $15). That has happened to spot chips in past busts (DDR4 8Gb fell about 65% from its 2021 peak to $1.30) but rarely to contract prices over two years (p1-market). **Design rule for the venture:** a concept that needs DDR5 above about $8/GB to stay profitable fails the mission's glut test. One that needs DDR5 above about $3/GB fails a 2023-style trough.

---

## 8. Trailing-node and alternative-memory cost inputs (for the device-comparison model)

### 8.1 Foundry 300mm wafer prices

| Node | 2020 basis (TSMC-class) | 2026 estimate | Tag |
|---|---|---|---|
| 90nm | $1,650 | — | CSET 2020 [UNVERIFIED: PK] |
| 55/65nm | **$1,937** | $1,700 (1.3–2.1k) | 2020: [VERIFIED as Chiplet Actuary parameter; origin CSET 2020]; 2026: [UNVERIFIED: PK] |
| 40nm | **$2,274** | $2,100 (1.6–2.5k) | same. v4-cost found no 2026 40nm price (STILL UNVERIFIED) |
| 28nm | **$2,891** | **$2,800** (1.9–3.45k). TSMC is ~$3,000 ($2,550–3,450), per a Silicon Analysts estimate as of Apr 2026 ([Silicon Analysts](https://siliconanalysts.com/data/wafer-pricing)) [REPORTED]. UMC/SMIC/Hua Hong are ~$2.0–2.5k after the 2026 hikes [ESTIMATE]. (v4-cost; was $2,600) | 2026 hikes: UMC/VIS/PSMC up to +10% from Apr 2026 ([TrendForce News 2026-03-16](https://www.trendforce.com/news/2026/03/16/news-umc-vis-psmc-reportedly-eye-mature-node-price-hikes-of-up-to-10-from-apr-ic-designers-may-follow/)). Mature nodes rose ~5–15% from 1Q26 to 2Q26 ([AnySilicon](https://anysilicon.com/news/semiconductor-foundry-prices-climb-as-capacity-tightens-across-all-nodes/)). TSMC plans up to +10% on 12/16/28nm in 2027 ([Nikkei via AI Weekly](https://aiweekly.co/alerts/tsmc-to-lift-chip-prices-up-to-10-from-2027-nikkei-reports)) [REPORTED] |
| 22FDX (GF) | — | $3,800 (3.2–4.5k) | [ESTIMATE], aligned with A2 and p1-fabs |
| 20nm | $3,677 | — | Chiplet Actuary [VERIFIED as parameter] |
| 14/16nm | **$3,984** | ~$4.5k | same |
| 10nm / 7nm / 5nm | $5,992 / $9,346 / **$16,988** | — | same |
| 3nm | $30,000 (repo flags it as "Inaccurate Assumptions") | ~$20k (17–22k) | Confirmed: Silicon Analysts puts it at $19,500 ($17–22k), Apr 2026 ([Silicon Analysts](https://siliconanalysts.com/data/wafer-pricing)) [REPORTED] |
| 2nm | — | ~$30k (28–33k) | Confirmed: Silicon Analysts puts it at $28–30k ([Silicon Analysts](https://siliconanalysts.com/data/wafer-pricing)) [REPORTED] |

Source for the 2020 column: Chiplet Actuary `parameter.ini` (Feng & Ma, DAC 2022; [repo](https://github.com/Yinxiao-Feng/DAC2022), opened 2026-11-01). The same figures appear in CSET's April 2020 "AI Chips" report [UNVERIFIED: PK attribution].

### 8.2 200mm wafer prices

| Process | Price | Tag |
|---|---|---|
| 180nm, Asian 8-inch foundry | **$700** (450–1,150) | The absolute price is still [UNVERIFIED: PK]: v4-cost found no public 180nm $/wafer. **The 2026 rise is confirmed.** 8-inch foundries notified customers of +5–20%. 2026 utilization is 85–90%, against 75–80% in 2025. Global 8-inch capacity falls 2.4% YoY as TSMC and Samsung cut ([TrendForce 2026-01-13](https://trendforce.com/presscenter/news/20260113-12877.html)) [REPORTED-P]. In 2Q26, VIS rose +10–15% QoQ and PSMC ~+5% ([Omdia 2026-07](https://omdia.tech.informa.com/blogs/2026/july/ddic-price-rise-as-foundry-and-material-costs-increase)) [REPORTED]. TrendForce (Mar 2026) expects the rises to diverge by foundry ([TrendForce](https://www.trendforce.com/presscenter/news/20260319-12979.html)). High end raised to $1,150 |
| 90–130nm, Asia | $1,000 (700–1,400) | [UNVERIFIED: PK] |
| SkyWater S130 (Bloomington MN), U.S. | **$1,400** (1,200–1,600) | [ESTIMATE], shared with p1-fabs, A1 and A2 |
| U.S. 65–90nm (SkyWater Fab 25 / RH90; trusted premium) | $2,000 (1,500–2,500) | [ESTIMATE] p1-fabs |

### 8.3 Mask sets and embedded-NVM adders

| Item | Value | Tag / source |
|---|---|---|
| 130nm mask set | **$500–600k** | [AnySilicon, via A1](https://anysilicon.com/130nm-wafer-mpw-cost/) [REPORTED] |
| 40nm / 28nm mask set | ~$0.9M (0.6–1.2M) / ~$1.5M (1.0–2.5M) | [UNVERIFIED: PK] |
| **eMRAM** (TSMC 22ULL/16FFC, GF 22FDX, Samsung 28FDS/14nm) | **+3–5 masks** (Samsung's "three additional masks" claim for 28FDS); **+$400–1,300/wafer**, base +$800 | [UNVERIFIED: PK]; $ adder [ESTIMATE], consistent with A2 |
| eFlash (split-gate, 40/28nm) for contrast | +9–14 masks | [UNVERIFIED: PK] |
| **RRAM** (TSMC, Weebit) | **+1–3 masks**; +$150–400/wafer | [UNVERIFIED: PK]; Weebit qualified in SkyWater S130 ([Weebit, via A2](https://www.weebit-nano.com/news/press-releases/weebit-nanos-reram-ip-now-fully-qualified-in-skywater-technologys-s130-process/)) |
| **CBRAM** (GF 22FDX, ex-Adesto) | **~1 extra mask** | [GlobalFoundries 2023-02-09, via A2](https://gf.com/gf-press-release/globalfoundries-acquires-renesas-non-volatile-resistive-ram-technology-to-proliferate-iot-and-5g-applications/) [REPORTED] |
| **FRAM** (TI 130nm embedded) | **+2 masks**; cell 0.54–0.71 µm² | [New Electronics, via A1](https://newelectronics.co.uk/content/features/fram-set-to-save-energy-in-write-intensive-mcu-applications) [REPORTED] |

### 8.4 MRAM, PCM and XPoint data points

| Item | Value | Source |
|---|---|---|
| TSMC 22nm eMRAM 1T1R cell | 0.046 µm² | [SemiWiki ISSCC 2020, via A2](https://semiwiki.com/semiconductor-manufacturers/tsmc/283868-tsmc-32mb-embedded-stt-mram-at-isscc2020/) [REPORTED] |
| Samsung eMRAM cell, 14nm / 8nm | 0.024 / 0.017 µm² (IEDM 2024) | [PC Watch, via A2](https://pc.watch.impress.co.jp/docs/column/semicon/1649812.html) [REPORTED] |
| IBM 14nm eMRAM cell | 0.0273 µm² | [IBM Research, via A2](https://research.ibm.com/publications/a-14-nm-embedded-stt-mram-cmos-technology) [REPORTED] |
| ST 18nm FD-SOI ePCM cell | 0.059 µm² (against MRAM 0.129 at 16nm and RRAM 0.174 at 12nm, per ST) | [Mynavi, via A2](https://news.mynavi.jp/techplus/article/20251120-3693534/) [REPORTED] |
| **Everspin 1Gb STT-MRAM (EMD4E001G, GF 28nm)** | die **105.1 mm²**, ~9.75 Mb/mm² (**0.0095 Gb/mm²**, ~46× below 1β DDR5 at 0.438) | [TechInsights, via A2](https://www.techinsights.com/blog/memory/worlds-first-1-gb-28-nm-stt-mram-product-everspin) [REPORTED] |
| Everspin 1Gb street price | **$102.60 @500** ($266 @1) → **$821/GB** (30× DDR5 spot) | [LCSC, via A2](https://www.lcsc.com/product-image/C20342497.html) [REPORTED]. Re-confirmed by v4-cost: EMD4E001G16G2-150CAS2R at ~$266 @1, ~$106 @200, ~$103 @500, ~$101 @1,000 ([LCSC](https://www.lcsc.com/product-detail/C20342497.html)) [REPORTED-P]. Mouser lists the part without a price in the snippet; no Digi-Key or Mouser price was found. 256Mb parts were not checked |
| Everspin gross margin | 51.4% (Q3-26) | [Everspin 8-K, via A2](https://www.sec.gov/Archives/edgar/data/0001438423/000162828026067890/mram-20260930xexx991.htm) [REPORTED] |
| Everspin 1Gb silicon cost (model) | ~$71/GB die + ~$20/GB test/package ≈ $91/GB | A2 scratch model (`phase2/A2_device_params.json`) [ESTIMATE] |
| 3D XPoint gen1 / gen2 density | 0.62 / 1.31 Gb/mm² | [TechInsights, via A2](https://www.techinsights.com/blog/intel-3d-xpoint-memory-die-removed-intel-optanetm-pcm-phase-change-memory); [gen2](https://www.techinsights.com/blog/memory/intel-2nd-generation-xpoint-memory) [REPORTED] |

### 8.5 SRAM cell sizes and silicon $/GB

| Node | HD 6T cell (µm²) | Macro Mb/mm² (×0.6 efficiency) | Wafer $ | **SRAM silicon $/GB** | **$/MB** |
|---|---|---|---|---|---|
| 180nm (200mm, Asia) | 4.6 (4.4–5.0) | 0.13 | 700 | **~1,600** | ~1.6 |
| 130nm (SkyWater 200mm, U.S.) | **1.896** [VERIFIED] | 0.32 | 1,400 | **~1,330** | ~1.3 |
| 65nm | 0.525 | 1.14 | 1,700 | **~195** | ~0.19 |
| 40nm | 0.242 | 2.48 | 2,100 | **~111** | ~0.11 |
| 28nm | 0.127 | 4.72 | 2,800 (v4-cost; was 2,600) | **~78** | ~0.08 |
| 16nm | 0.074 | 8.1 | 3,984 | **~64** | ~0.06 |
| 7nm | 0.027 | 22.2 | 9,346 | **~55** | ~0.05 |
| 5nm | 0.021 | 28.6 | 16,988 | **~78** | ~0.08 |
| 3nm | 0.0199 | 30.2 | 20,000 | **~87** | ~0.09 |
| 2nm | ~0.0175 | ~34 | ~30,000 | **~115** | ~0.11 |

Tags for this table:
- Cells other than 130nm are [UNVERIFIED: PK] (IEDM, ISSCC and foundry disclosures).
- $/GB is [ESTIMATE]: wafer $ ÷ (92% of the wafer area) ÷ macro density. It covers silicon only, excluding test and packaging.

Small macros are far worse. The GF180MCU 4-kbit macro is 431.86 × 484.88 µm = 0.2094 mm², or **19.6 kbit/mm²** ([GF180MCU SRAM IP](https://github.com/google/globalfoundries-pdk-ip-gf180mcu_fd_ip_sram)) [VERIFIED]. An OpenRAM sky130 2KB macro reaches 57.6 kbit/mm² (A3) [VERIFIED by A3].

**Takeaway:** SRAM silicon bottoms out at about **$55–78/GB at 7–28nm**. Below 7nm it gets *more* expensive per bit, because SRAM cell scaling has stalled while wafer prices keep rising. That is about 40–50× the cost of DDR5 but only about 2.5–5× the *price* of 2026 DDR5. At 2023 trough prices (~$1.6/GB) it was 45×.

**Discrete SRAM price reference** (v4-cost; no 288Mb QDR price was found):
- A 72Mb QDR-II+ (Infineon CY7C25652KV18-550BZXI) sells at broker prices of **$12.36 @1,088 to $33.70 @1**, or about **$1.4–3.7/MB ≈ $1,400–3,800/GB** ([Lisle Apex](https://www.lisleapex.com/product-cy7c25652kv18-550bzxi)). Avnet lists the -450BZXC at $192 @4 ([Avnet](https://www.avnet.com/americas/product/infineon/cy7c25652kv18-450bzxc/evolve-67999977/)) [REPORTED].
- That is **~7–20× the modeled 65nm silicon cost** ($195/GB). The gap is package, test and low-volume niche margin, so the **$/GB of a merchant SRAM product is set by volume, not silicon**.

### 8.6 NAND, NOR and display references

| Item | Value | Tag |
|---|---|---|
| NAND TLC contract, 2023 trough | ~$0.025/GB (0.018–0.035) | [UNVERIFIED: PK] |
| NAND TLC, 2026 | ~$0.09/GB (0.06–0.15). 512Gb TLC wafer contract +>65% MoM in Nov 2025 | [ESTIMATE]; [TrendForce 2025-12-01, via p1-market](https://www.trendforce.com/presscenter/news/20251201-12807.html) |
| SPI NOR | ~$40/GB (20–70) | [UNVERIFIED: PK] |
| Gen 8.5 glass sheet | 2,200 × 2,500 mm = 5.5 m² | A1 device params |
| Oxide-TFT backplane cost | **~$50/m²** (25–110) → **~$275 per Gen-8.5 sheet** (140–600); A1 used $500 | [UNVERIFIED: PK]: array ≈ 20–30% of LCD panel cost. No U.S. TFT fab exists (A1; Foxconn Wisconsin never built a panel fab) |
| Display design rule | 1.5–3 µm. At these rules IGZO memory on glass is ~10⁵× less dense than DRAM (p1-fabs §8) | [UNVERIFIED: PK] |

---

## 9. Legacy DRAM (DDR3/DDR4) costs on depreciated lines

Who makes it [UNVERIFIED: PK]:
- **Nanya** (Taiwan): 20nm, then 10nm-class 1A/1B. 3Q26 GM 85.7%.
- **Winbond** (Taiwan): 25nm and 20nm specialty DRAM.
- **CXMT** (China): 19 → 17 → 16nm-class. It is on the U.S. procurement-ban path (§5949, effective Dec 2027; p1-backend).
- **PSMC** (Taiwan): 25/38nm-class DRAM foundry for fabless specialty-DRAM vendors such as Etron, plus others whose sourcing I have not verified.
- **Alliance Memory and ISSI** (U.S.-headquartered): fabless resellers or designers that buy legacy DRAM from these fabs. I have not verified which fab supplies which product.
- **Samsung and SK hynix:** extended DDR4 into 2026. **Micron** issued DDR4/LPDDR4 EOL notices in Jun 2025 (p1-market).

| Part | Die mm² | GDPW | Wafer $ | Yield | Front-end $/die | **$/GB incl. back-end** |
|---|---|---|---|---|---|---|
| DDR4 8Gb, 1x, depreciated line | 55 | 1,121 | 1,300 | 0.92 | 1.26 | **1.56** |
| DDR4 8Gb, 1z, depreciated line | 39 | 1,594 | 1,300 | 0.92 | 0.89 | **1.19** |
| DDR3 4Gb, 25nm, depreciated line | 60 | 1,025 | 1,300 | 0.92 | 1.38 | **3.36** |
| DDR3 4Gb, 3x-nm, depreciated line | 80 | 761 | 1,100 | 0.92 | 1.57 | **3.74** |
| DDR3 4Gb, 25nm, PSMC-class foundry wafer ($1.6k) | 60 | 1,025 | 1,600 | 0.90 | 1.73 | **4.17** |
| **DDR4 8Gb, 1x, NEW line** (wafer $2.8k, y 0.85) | 55 | 1,121 | 2,800 | 0.85 | 2.94 | **3.34** |

Wafer-cost tags: depreciated cash cost $1,300 (1,000–1,800); new 2x/1x DUV line $2,800 (2,300–3,500), at about $80–110k/wpm capex; PSMC-class foundry $1,600 (1,200–2,200). All are [ESTIMATE / UNVERIFIED: PK].

What the table shows:
- **DDR3 costs more per GB than DDR4** because its dies hold fewer bits and back-end cost is per die.
- **DDR3 still sells at ~$25/GB spot (Jul 2026), and DDR4 at ~$44/GB (Aug 2026).** That is 7–35× its legacy cost. Legacy DRAM is the most over-priced memory relative to cost in 2026.
- **In 2023 DDR4 sold at $1.30/GB**, below even the depreciated-line cost for 1x parts.
- **A greenfield or retrofitted U.S. legacy line at about $3.3/GB is profitable only in shortage years.**
- p1-fabs found **no U.S. 22–65nm line with a DRAM capacitor module**, so even this cost assumes capability that does not exist in the U.S.

---

## 10. Implications for the mission premise (confirm / correct)

1. **Premise bullet 2 (margins exist and are captured by incumbents): confirmed and quantified.**
   - Cost is about $1.15–2.5/GB (base $1.5; v4-cost, was $1.2–2.9 with base $1.6). Price is $14.5–27/GB. That is 85–92% GM, consistent with Nanya, Micron and SK hynix filings or releases (p1-market). It sits up to ~6 pp above them at the 4Q26 anchor (§2.3).
   - **Correction:** the margin is a *price* phenomenon, not a technology moat. Wafer costs did not move. Price rose about 4–8× (p1-market) while cost per bit kept falling about 10–20% per node.
2. **Premise bullet 4 (cyclicality): sharpened.**
   - A 60% glut still leaves DDR5 5.5–7× above incumbent full cost and 11–14× above cash cost (v4-cost; was 3–6× and 6–13×). **Incumbents can absorb a 60% fall; entrants cannot.**
   - In 2023 the price fell below cash cost for some legacy parts (DDR4 $1.30/GB).
   - Every concept should be stress-tested at **$8–10/GB (−60% from the verified ~$20–26/GB 4Q26 contract; was $6–10)** and at **$1.5–2.5/GB (2023 floor)**.
3. **"Cheaper materials or processes" must beat about $1.5/GB at scale, or about $8–10/GB in a glut with a premium axis.**
   - Of the alternatives measured here, none comes within 10× of DDR5 *cost* on $/GB: MRAM is $90–820/GB, SRAM $55–1,600/GB, IGZO-on-glass and 130nm BEOL memories worse still.
   - Only 3D XPoint-class crosspoint (0.62–1.31 Gb/mm²) and 3D-stacked DRAM concepts had density that beats 1β DDR5. Optane failed on volume and cost absorption, not density (A2).
   - **Device concepts can only win on a non-$/GB axis:** non-volatility, retention, radiation hardness, supply security, or lifecycle.
4. **HBM is not automatically the best place for marginal wafers.** At 2026 HBM3E pricing, DDR5 earns more per wafer. HBM4's 2027 price (~3× HBM3E) restores the incentive. This bears on any "HBM-adjacent" packaging concept: its economics depend on the 2027–28 HBM4 price holding.
5. **U.S. back-end and module value is small.** Parts plus assembly are about $20–37 per 64GB RDIMM against $927–1,650 contract prices. **A U.S.-assembly premium must come from provenance (§5949, DoD), not cost.** This agrees with p1-backend.

---

## 11. Verification backlog (run first when web access returns)

**Phase-1b status (v4-cost, 2026-11-01; details in `verify_v4-cost.md`):**
- #1 is mostly done: the 1α and 1β die sizes are anchored. 1γ, SK hynix and Samsung 1b DDR5, and the CXMT 2025–26 node are still open.
- #2: no die area was found for the Samsung 32Gb DDR5.
- #3: no public DRAM wafer-cost estimate was found. **Still the top open item.**
- #4: the 8-inch outlook is confirmed. The DDR5 16Gb contract level was not found.
- #5: no Micron cost-per-bit commentary was found. Micron stopped disclosing it in 2017.
- #6: SK hynix 1c = 6 EUV layers [REPORTED].
- #8: the Everspin price is confirmed via LCSC.

1. **TechInsights** DDR5 16Gb die sizes for Samsung, SK hynix and Micron at 1α, 1β and 1γ/1c. These replace the UNVERIFIED densities in §3.1. Also the CXMT 2025–26 node (G5?) die.
2. **ISSCC 2024–2026** DRAM papers: Samsung 32Gb DDR5 (1b), SK hynix 1c DDR5/LPDDR5X, Samsung/SK hynix HBM4 core die areas.
3. **IC Knowledge / Scotten Jones** (SemiWiki) DRAM wafer-cost and cost-per-bit estimates by node, to replace the bottom-up §2.1.
4. **TrendForce press center:** "HBM die size 35–45% larger / yield 20–30% lower" (2024); 8-inch foundry price outlook for 2026; DDR5 16Gb contract price level.
5. **Micron 10-K FY2026:** depreciation lives, cost-per-bit commentary, HBM trade ratio wording.
6. **SK hynix / Samsung** EUV layer counts at 1b and 1c (company newsroom).
7. **Rambus and Montage IR:** RCD, PMIC and SPD ASPs or "content per DIMM" statements.
8. **Everspin 10-K:** product ASPs, GF Singapore wafer cost.
9. **TSMC / GF / Samsung** eMRAM mask-adder statements (IEDM / foundry tech symposium).
10. **CSET "AI Chips" (2020) PDF:** confirm the 2020 wafer-price table that Chiplet Actuary reuses.
11. 2023 DRAM industry revenue and capacity (TrendForce / Gartner) for the top-down check.
12. **Display cost:** Omdia/DSCC oxide-TFT backplane cost per m² at Gen 8.5/8.6.

---

## 12. Source index (all logged in `research/sources/p1-cost.jsonl`)

**Phase-1b additions (v4-cost, 2026-11-01):** 50 sources, all seen through search snippets, logged in `research/sources/v4-cost.jsonl`:
- TechInsights die pages: Micron D1β, SK hynix D1a, the DDR5 comparison, Micron D1γ Y62E, CXMT G4.
- Micron 1γ brief.
- ETN.fi on the Samsung D1b LPDDR5X.
- Counterpoint Apr/Jul-2026 trackers.
- TrendForce press releases and news: 2026-01-13, 2026-03-16, 2026-03-19, 2026-09-30, 2026-10-21.
- Silicon Analysts wafer and HBM pricing.
- Omdia, LCSC, S&P Global, Capital & Compute, SemiconSam and others.

**Opened by p1-cost (VERIFIED):**
- [Chiplet Actuary repo (Feng & Ma, DAC 2022)](https://github.com/Yinxiao-Feng/DAC2022): wafer costs by node, D0, GDPW and yield formulas.
- [ECO-CHIP repo](https://github.com/ASU-VDA-Lab/ECO-CHIP): D0 table, negative-binomial yield, bonding yield.
- [HP CACTI repo](https://github.com/HewlettPackard/cacti): cell areas in F².
- [SkyWater sky130 SRAM bitcells](https://github.com/google/skywater-pdk-libs-sky130_fd_bd_sram): 1.896 µm² 6T.
- [GF180MCU SRAM macros](https://github.com/google/globalfoundries-pdk-ip-gf180mcu_fd_ip_sram): 0.2094 mm² per 4 kbit.

**Cross-referenced from other agents' snippet logs (REPORTED):**
- Die and density: SemiWiki/TechInsights CXMT DDR5; KitGuru/Kurnal 1b density.
- HBM trade ratio: Tom's Hardware and XenoSpectrum (Micron).
- Prices: BuySellRAM/DRAMeXchange; Tech-Insider; EE Times Asia/Counterpoint; Servnet; rampricesusa; Digital Citizen; KED Global; Asia Economy; Wccftech; Sammy Fans; Silicon Analysts; TrendForce (2026-09-30; NAND 2025-12-01).
- Margins: TrendForce News/Nanya; Finviz/Micron; Placera/SK hynix; The Register.
- Alternative memory: TechInsights (Everspin, XPoint ×2); LCSC; Everspin 8-K; SemiWiki (TSMC eMRAM); PC Watch; IBM Research; Mynavi; GF CBRAM; New Electronics (TI FRAM); AnySilicon; Weebit.

**Prior knowledge (UNVERIFIED: PK, no URL logged):**
- Samsung (Oct 2021), SK hynix (Jul 2021, Aug 2024) and Micron (Jan 2021, Nov 2022, Feb 2025) node announcements.
- TrendForce 2024 HBM die-size/yield note; FT May 2024 (SK hynix HBM3E yield); CSET Apr 2020 wafer-price table; JEDEC JESD79-5.
- Industry rules of thumb flagged in `research/assumptions/p1-cost.md`.
