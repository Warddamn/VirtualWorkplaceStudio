# A2: Materials, resources and energy. Is DRAM running out of *stuff*?

**Agent:** `A2-resources` · **As of:** 2026-11-01 · **Model:** `dram-moonshot/research/models/A2_resource_intensity.py` (stdlib; `python3` exits 0) · **Sources:** `research/sources/A2-resources.jsonl` (61 entries) · **Assumptions:** `research/assumptions/A2-resources.md`

> **Evidence grade.** I used all 25 of my WebSearch calls and no WebFetch. Every web fact here comes from a **search snippet** (tagged `[REPORTED]`, and "(via search snippet)" in the source log). Prior knowledge without a URL is tagged `[UNVERIFIED-PK]`. My own arithmetic is tagged `[ESTIMATE]` and lives in the model. DDR5 anchors are reused from `ram-venture/models/dram_cost_stack.py` and not re-derived: 1-beta 16Gb die 36.5 mm², 1,534 good dies per wafer (**3,068 GB/wafer**), **$3,800/wafer**, **$1.48/GB**, ~56% of wafer cost is depreciation.

---

## 0. VERDICT: **PARTLY TRUE, but not in the way the premise states it**

The premise is: "we don't have the natural resources to continue the way we are currently doing it."

**1. Running out of geology: NOT SUPPORTED.** A GB of DRAM holds about **42 mg of silicon**. Making it takes about **0.42 kWh of fab electricity** and **~2.6 L of gross water** [ESTIMATE, model §1]. Across the whole DRAM fleet (~22M wafers/yr), consumption is a rounding error against world supply:

| Input | Fleet use | Share of world supply |
|---|---|---|
| Tungsten | ~150 t | ~0.17% |
| Copper | ~44 t | <0.001% |
| Zirconium | ~19 t | <0.01% |
| Electricity | ~29 TWh | ~0.1% of world electricity |

All the listed metals (W, Hf, Zr, Cu, Co, Mo) **together** cost under $25 per $3,800 wafer, even at 2026's record prices. The prime silicon wafer itself is ~$115 (3%). No DRAM output loss from a raw-material shortage was found in 2022–2026, through the neon spike (2022), Hurricane Helene (2024), the tungsten and hafnium spikes (2025–26) and the Qatar helium shock (2026).

**2. Concentrated chokepoints: TRUE, and the risk is live.** The problem is *where things are processed*, not how much exists:

| Chokepoint | Concentration | Price signal |
|---|---|---|
| Helium | Qatar ~30% of supply, and **offline since March 2026**. Korea took **64.7%** of its helium from Qatar in 2025 | Spot price ~2× |
| High-purity quartz for crucibles | Spruce Pine, NC: **>80%** of HPQ, 70–90% of crucibles | — |
| Tungsten | China ~80% | APT **+350% YTD** in 2026 |
| Hafnium | China export controls | **~$5k → ~$13k/kg** |
| Rare earths, Ga/Ge/Sb | Chinese controls | Suspensions **expire in November 2026** |
| EUV scanners | ASML is the only supplier, ~65 per year | — |
| Photoresist | Japan ~90% | — |
| Semiconductor coolant fluids | 3M (~90% in 2022) exited PFAS at end-2025 | — |
| PFAS chemistry | The EU PFAS restriction will act on it from ~2028 | — |

These produce price shocks and policy risk. None has yet cut DRAM wafer starts.

**3. What actually binds DRAM supply in 2026–2028: capital × cleanroom-time × tools.**
- **Cleanroom and time.** Micron sees DRAM bit growth only in the **low-20s %** in 2027–28. It expects **no meaningful output from new cleanrooms until late 2028 or later** ([CIO/Computerworld, 2026-09](https://cio.com/article/4229625/memory-squeeze-set-to-tighten-through-2028-micron-says.html)) [REPORTED].
- **Capital.** Industry DRAM capex is **$61.3B in 2026** ([TrendForce, 2025-11-13](https://trendforce.com/presscenter/news/20251113-12780.html)) [REPORTED]. New capacity costs ~$145–170k per wafer-start-per-month (ram-venture).
- **Tools.** ASML ships ~65 low-NA EUV tools in 2026 and 80 in 2027 ([MarketBeat, 2026-07-15](https://www.marketbeat.com/instant-alerts/asml-q2-earnings-call-highlights-2026-07-15/)) [REPORTED].
- **HBM.** It uses **~2.5–3× the wafer area per GB** of DDR5 [ESTIMATE from dram_cost_stack].
- **Local power and water at megafab sites.**
  - Yongin needs **~15 GW**, against **<2 GW** of local supply.
  - Micron Clay needs **16 TWh/yr** and **48 million gallons/day**.

**4. "The current way can't continue" is TRUE in an economic-physics sense.** Each node cuts cost per bit by only ~10–20% while wafer cost rises 10–15% (ram-venture §2.5). It also adds EUV layers, each at ~11 kWh per exposure. Planar scaling is ending, and that forces 3D architectures. 3D brings new element appetites (Ge, Hf, possibly Ru and Sc; see §4).

**Which intensities a new approach could most valuably reduce, ranked:**
1. **Capital and cleanroom-time per bit** (GB per wafer-pass, $ per wafer-start). This is the real binding constraint.
2. **Use-phase energy per bit, especially refresh.** A server GB burns ~6.6 kWh over 5 years, **~16× its fab electricity** [ESTIMATE].
3. **EUV and lithography intensity, and fab kWh per GB.** EUV tools are $290M each, draw ~10 GWh/yr each, and are supply-capped.
4. **Exposure to specific chokepoints:** helium, PFAS fluids and resists, Spruce Pine crucibles, and Chinese-processed W, rare earths, Ga and Ge.

**Not worth optimizing:** Cu, W, Zr and silicon mass. Each is under 0.2% of world supply and under 0.1% of wafer cost.

> **A warning the invention team needs.** Several "new DRAM" chemistries would *create* real resource constraints that today's DRAM does not have (model §4):
> - **Ru capacitor electrodes** fleet-wide would need **26–176% of world ruthenium**.
> - **HZO ferroelectric capacitors** would need **14–41% of separated world hafnium**.
> - **3D DRAM Si/SiGe superlattices** would need **6–38% of refined germanium**, mostly Chinese.
> - **AlScN on 3D capacitor area** would need **~13% of world scandium**.
>
> IGZO is fine on quantity (In and Ga under 0.4%), but gallium is ~98% Chinese and export-licensed.

---

## 1. Scale: how much stuff is in a GB of DRAM

Output of `A2_resource_intensity.py` (1-beta DDR5; ranges in brackets):

| Quantity | Per 300mm wafer | Per GB | Share of wafer cost | Fleet (22.2M wafers/yr) |
|---|---|---|---|---|
| Fab electricity | **1,300 kWh** [900–2,000] | **0.42 kWh** [0.29–0.65] | **3.4%** ($130 at $0.10/kWh) | **~29 TWh/yr** (~0.1% of world electricity) |
| EUV electricity (6 layers, 1c-class) | 67 kWh | 0.02 kWh | in the above | ~5% of DRAM wafer kWh (vs ~1/3 for 3–7nm logic per [Silicon Analysts 2026](https://siliconanalysts.com/analysis/chip-manufacturing-energy-cost)) |
| Water, gross withdrawal | **8 m³** [5–25] | **2.6 L** | 0.4% | ~178 Mm³/yr gross (before ~66% reuse) |
| Silicon (775 µm wafer) | 128 g | **42 mg** | 3.0% (prime wafer ~$115) | ~5,700 t polysilicon ≈ 13% of semi-grade poly |
| Capacitor dielectric area | **3.3 m²** (the wafer is 0.071 m²; the array has ~92× surface enhancement) | — | — | — |
| W (consumed incl. WF6 waste) | ~6.7 g | 2 mg | 0.07% even at record APT | ~150 t = 0.17% of world W |
| Cu | ~2 g | 0.7 mg | ~0% | ~44 t |
| Zr (ZrO2 capacitor dielectric) | ~0.8 g consumed (0.08 g in film) | — | ~0% | ~19 t, <0.01% of Zr |

**Energy cross-checks.**
- Micron reported **11 billion kWh** for all its fabs ([NYRWA/Micron 2023 SR, via snippet](https://nyruralwater.org/node/3506)) [REPORTED]. Divided by ~7–8M wafers/yr, that gives **~1,300–1,500 kWh/wafer** company-wide [ESTIMATE].
- Silicon Analysts gives **800–1,500 kWh/wafer** for advanced logic ([2026](https://siliconanalysts.com/analysis/chip-manufacturing-energy-cost)) [REPORTED].
- **Conflict:** the literature value of **63–65 gCO2e/GB** for DRAM embodied carbon ([arXiv 2306.13177](https://arxiv.org/pdf/2306.13177); [arXiv 2504.18980](https://arxiv.org/pdf/2504.18980)) [REPORTED] implies only ~0.1–0.15 kWh/GB. That is 3–4× below both company-total cross-checks. I keep 0.42 kWh/GB and flag the conflict.
- **HBM** has roughly 2.5–3× fewer GB per wafer, so it costs **~1.0–1.3 kWh/GB** [ESTIMATE]. The AI-driven HBM mix shift raises the energy and wafer intensity of the average DRAM GB.

**Use phase vs fab.** At ~0.15 W/GB in servers [UNVERIFIED-PK], a GB uses **~6.6 kWh over 5 years, ~16× its fab electricity** [ESTIMATE]. For DRAM, *operating* energy (refresh plus I/O plus background) is the larger energy lever, not manufacturing energy.

---

## 2. Input-by-input map

"Binding" means the input has limited, or credibly will limit, DRAM wafer starts. A price shock under ~1% of wafer cost counts as non-binding.

| Input | What DRAM uses it for | Concentration (dated) | Price trend (dated) | Binding on DRAM output? |
|---|---|---|---|---|
| **High-purity quartz / silicon** | CZ crucibles for ingot pulling; 128 g Si per wafer | Spruce Pine **>80%** of commercial HPQ (BNEF via 2024 press); **70–90% of crucibles** ([AP, 2024-10-10](https://abcnews.go.com/US/wireStory/north-carolina-maker-high-purity-quartz-back-operating-114699814)). Five wafer makers **>80%** of 300mm ([Averroes 2026](https://averroes.ai/blog/silicon-wafer-manufacturers)) [REPORTED] | Wafer makers' **second 2026 price hike on May 10** ([SunSirs, 2026-06](https://www.sunsirs.com/commodity-news/petail-35761.html)) [REPORTED] | **No.** Helene halted mines 2024-09-26; Sibelco restarted **2024-10-10** ([Sibelco](https://www.sibelco.com/en/news/sibelco-restarts-production-and-customer-shipments-at-spruce-pine-following-hurricane-helene)). Buffers held ([Jabil](https://stg-gpi.jabil.com/commodity/alerts/alert-update-on-quartz-supply-chain-disruptions.html)). Low-probability, high-impact tail |
| **Neon** | ArF/KrF excimer laser gas (DRAM is heavy on ArFi multipatterning) | Ukraine **50–70%** pre-2022 ([SPIE, 2023-05](https://amp.spie.org/news/photonics-focus/mayjune-2023/supplying-noble-gases-for-photonics-in-war-time)). Ukraine had already lost ~20 pts after 2014 and China added capacity ([USITC](https://www.usitc.gov/publications/332/executive_briefings/ebot_decarlo_goodman_ukraine_neon_and_semiconductors.pdf)) | **~10×** in China, Mar 2022 (SPIE). No 2025–26 series found | **No.** Micron sourced from EU/US/Asia; ASML <20% Russia/Ukraine ([Reuters, 2022-02-24](https://www.nippon.com/en/news/reu20220224KBN2KT0T5/)). Laser-gas recycling and Korean domestic neon since 2022 [UNVERIFIED-PK] |
| **Krypton / xenon** | KrF lasers (Kr); some etch and implant (Xe) | Air-separation by-products; Russia/Ukraine historically material [UNVERIFIED-PK] | Xe **~$2,900/kg Q1-2026, easing**; Korea $3,180/kg ([price tracker, 2026-03](https://globalriskcommunity.com/notes/xenon-latest-prices-trend-demand-index-uses-march-2026)) [REPORTED, low-quality source]. Kr/Xe +~50% in 2022 (SPIE) | **No** |
| **Helium** | Wafer backside cooling in etch and CVD chucks (DRAM's 50:1 capacitor and contact etches), purge, leak check [UNVERIFIED-PK] | Qatar **~30%** (USGS via [AP, 2026-03-21](https://wtop.com/news/2026/03/iran-war-halts-qatar-helium-output-threatening-global-tech-supply-chains/)). **Korea 64.7% from Qatar in 2025** (AP). Semis are **20–25%** of world helium demand ([Tom's Hardware 2026](https://tomshardware.com/tech-industry/semiconductors/the-global-helium-shortage-is-a-direct-threat-to-chipmaking)) | Ras Laffan halted March 2026 after Iranian strikes ([Caixin, 2026-03-16](https://www.caixinglobal.com/2026-03-16/qatar-helium-shutdown-adds-new-risk-to-chip-supply-chain-102423361.html)). Spot +50% ([TrendForce, 2026-03-27](https://www.trendforce.com/news/2026/03/27/news-iran-conflict-reportedly-drives-50-helium-spot-price-surge-samsung-sk-hynix-on-high-alert/)), then ~$1,000–1,200/Mcf vs ~$500 pre-war (Tom's Hardware). **No restart date as of June 2026** ([IUMI](https://iumi.com/newsletter-june-2026/qatari-helium-shortages/)) | **Not so far, but the highest live risk.** About 6 weeks of on-site storage (AP). Samsung and SK hynix signed long-term contracts with Linde and Air Products at higher prices (AP via snippet). No output cut found through mid-2026. Status after June is unknown |
| **Hafnium** | Periphery HKMG gate oxide; some capacitor stacks; HZO in ferroelectric concepts (FeRAM, NVDRAM, DRAM+) | By-product of nuclear-grade Zr separation. **China export controls from 2H25** ([SMM, 2026-04](https://news.metal.com/newscontent/103938701-from-stability-to-surge-the-overseas-hafnium-market-caught-between-ai-demand-and-supply-controls)) | **~$5,000 → ~$13,115/kg** (Nov-25 → Apr-26; SMM). ~$12,000/kg Q2-26 avg ([IMARC](https://www.imarcgroup.com/hafnium-metal-price-trend)) [REPORTED] | **No today** (<$1/wafer). **Would bind** a fleet-wide HZO capacitor: 11–33 t/yr = **14–41%** of ~80 t separated world Hf (model). It is separation-limited, not geology-limited: zircon contains ~100× more Hf than is separated [ESTIMATE] |
| **Zirconium** | ZrO2/Al2O3/ZrO2 capacitor dielectric | Zircon: Australia and South Africa lead [UNVERIFIED-PK] | n/a | **No** (<0.01% of Zr) |
| **Tungsten** | Buried word lines, contacts, plugs (via WF6) | China **~80%** of ~85 kt mining; **70–85%** of APT refining; 15 licensed exporters for 2026–27 ([Oregon Group, 2026-05](https://theoregongroup.com/commodities/tungsten/why-tungsten-prices-are-rising-so-fast-inside-the-supply-crunch/); [Mining Reporters, 2026-04](https://www.miningreporters.com/noticia/news/2026/04/tungsten-prices-record-china-export-controls-defence-demand)) | APT **~$3,000–3,185/mtu, +350% YTD, ~+900% in 12 months** (Oregon Group; [Fastmarkets](https://www.fastmarkets.com/?p=139045)) [REPORTED] | **No.** ~$2.7/wafer at the record price; 0.17% of world W [ESTIMATE]. Mo (Lam ALD Mo) is a drop-in candidate [UNVERIFIED-PK] |
| **Ruthenium** | Not in volume DRAM today. Candidate capacitor electrode (enables higher-k) and ≤10 nm interconnect | PGM by-product, **largely South Africa** ([Kitco, 2026-03-16](https://www.kitco.com/news/off-the-wire/2026-03-16/ruthenium-prices-hit-record-high-ai-boom-squeezes-supply)) | **$17.98 → $56.21/g** (Mar-25 → Mar-26; [Discovery Alert](https://discoveryalert.com.au/ruthenium-demand-modern-computing-2026/)) [REPORTED] | **Not today. Would bind** if adopted: 2 × 5 nm electrodes fleet-wide = **9 t (100% utilization) to 62 t (15%)**, vs ~35 t/yr world supply. ~$156/wafer (4%) at 15% utilization [ESTIMATE]. Recovery services exist ([Heraeus](https://heraeus.com/en/landingspages/lp_hpm/ruthenium_semiconductor/lp_ruthenium_semiconductor.html)) |
| **Cobalt / molybdenum** | Liners, caps, contacts; Mo as a W/Cu successor | Co: DRC ~70% of mining, with export restrictions in 2025. Mo: China, Chile, US; on China's Feb-2025 control list [all UNVERIFIED-PK] | Not searched | **No** (milligrams to grams per wafer) |
| **Copper** | Periphery BEOL (2–4 levels) | Chile/Peru mining; China refining [UNVERIFIED-PK] | Not searched | **No.** ~2 g/wafer, ~$0.02–0.04 [ESTIMATE] |
| **Fluorochemicals / PFAS** | Fluorocarbon etch gases (C4F6, C4F8, CHF3, CF4) for high-AR etch; NF3 chamber clean; PAGs and top coats in ArFi resists; PFA/PTFE wetted parts and FFKM seals; chiller fluids (Novec/Galden-class) [UNVERIFIED-PK on the list] | **3M ~90% of chip-industry coolant (2022)** ([Barron's/Resilinc](https://resilinc.com/wp-content/uploads/2022/04/Barrons_ChipSector2022.pdf)). **3M completed its PFAS manufacturing exit at end-2025**, with replacements "not completed" ([3M](https://www.3m.com/3M/en_US/pfas-stewardship/uses-applications/)) | EU: SEAC draft-opinion consultation Mar–May 2026; final opinion targeted end-2026; draft ban applies **18 months after entry into force** ([SGS, 2026-04](https://www.sgs.com/news/2026/04/safeguards-05026-echa-consults-over-seacs-draft-opinion-on-pfas-restrictions-under-reach); [ChemRadar, 2026-06](https://www.chemradar.com/en/service/detail/fop1tsgjw45c)). Semiconductor derogations still under review | **Not yet.** No volume DRAM fab sits in the EU, but tool, part and chemical supply chains do. Medium-term regulatory risk (~2028+). "No fully equivalent substitutes" for resists and etch gases (ChemRadar) |
| **Water** | UPW rinses, scrubbers, cooling towers | Local | n/a | **Local siting constraint.** Clay **48 MGD** at full build, double the 2022 estimate ([WSKG, 2023-08-06](https://www.wskg.org/news/2023-08-06/micron-estimates-needing-up-to-48-million-gallons-of-water-a-day-aiming-to-achieve-100-water-conservation)). Yongin's 10 fabs = **94% of the Han River allocation** ([Asia Economy, 2026-10-07](https://view.asiae.co.kr/en/article/2026100713000673909)). Micron reuses 66% ([Micron 2024 SR](https://www.nasdaq.com/press-release/micron-releases-2024-sustainability-report-highlighting-progress-and-long-term-vision)) |
| **Electricity** | ~1,300 kWh/wafer; 0.42 kWh/GB | Local grid | ~3.4% of wafer cost [ESTIMATE] | **Local siting constraint.** Yongin needs **~15–16 GW vs <2 GW** local ([Tom's Hardware 2026](https://www.tomshardware.com/tech-industry/power-and-water-lag-the-fabs-in-south-koreas-880-billion-chip-and-ai-plan)). Clay **16 TWh/yr**, more than Micron's whole 2023 fleet (11 TWh) ([NYRWA](https://nyruralwater.org/node/3506)) |
| **EUV scanners** | 0 layers (Micron 1β, CXMT) up to ~6–7 (SK hynix and Samsung 1c) | **ASML 100%.** ~65 low-NA in 2026 (44 in 2025); 80 in 2027; capacity +30% in 2027; memory system sales +75% ([MarketBeat](https://www.marketbeat.com/instant-alerts/asml-q2-earnings-call-highlights-2026-07-15/); [Quartz, 2026-04-15](https://qz.com/asml-2026-sales-forecast-raised-ai-chip-demand-041526)) | ~$290M per tool (ram-venture, S&P 2026-03) | **Paces node migration, not bit supply directly.** Micron's 1β (0.447 Gb/mm², the densest teardown in the repo) uses **zero EUV**. CXMT ships DDR5 with none. At today's density EUV is a yield and cycle-time lever, not a gate |
| **Tin and hydrogen for EUV** | LPP source fuel; H2 debris mitigation and collector cleaning | Tin is widely mined; H2 is made on site | n/a | **No.** ~95 kg Sn per tool-yr before recovery; 300 tools ≈ 28 t ≈ 0.01% of world tin [ESTIMATE]. imec recovers ~70% of EUV hydrogen ([Cleanroom Technology](https://cleanroomtechnology.com/research-hub-presents-modelling-platform-to-assess-environmental-impact-of-fabs-207137)) [REPORTED]. Real cost is energy: <2% of source energy reaches the wafer ([TechInsights](https://www.techinsights.com/blog/euv-lithography-power-hungry-path-innovation)) |
| **Photoresist** | ArFi (multipatterning) and EUV resists | **Japan ~90%**: JSR, TOK, Shin-Etsu, Fujifilm, Sumitomo ([Asia Times](https://asiatimes.com/?p=655728)). Top 3 ~90% of EUV resist ([Valuates](https://prnewswire.co.uk/news-releases/euv-photoresists-market-to-reach-1-4-billion-by-2031--key-growth-insights--trends---valuates-reports-302420650.html)) [REPORTED] | Not found | **No.** Concentration is in an allied country. Precedent: Japan's 2019 curbs on Korea (resist, HF, fluorinated PI), lifted 2023 [UNVERIFIED-PK] |
| **China: Ga / Ge / Sb / graphite / rare earths** | Si DRAM uses almost no Ga. Ge goes into SiGe periphery and 3D DRAM superlattices. Sb is a minor dopant. Graphite goes into CZ hot zones and implant parts. Rare earths: NdFeB magnets in tools, Y2O3/YF3 chamber coatings, CeO2 CMP slurry [UNVERIFIED-PK on uses] | Ban on Ga/Ge/Sb exports to the US (Dec 2024) **suspended until 2026-11-27**; dual-use licensing remains ([Fastmarkets](https://fastmarkets.com/insights/china-suspends-export-prohibition-on-superhard-materials-us); [Engineering News, 2025-11-10](https://www.engineeringnews.co.za/article/china-halts-ban-on-gallium-germanium-antimony-exports-to-us-but-controls-remain-2025-11-10)). The 2025-10-09 rare-earth package (0.1% de minimis; case-by-case review for **≤14nm logic and ≥256-layer memory**) was suspended for one year ([TrendForce, 2025-10-09](https://www.trendforce.com/news/2025/10/09/news-china-expands-rare-earth-curbs-subjects-14nm-logic-and-256-layer-memory-chips-to-case-by-case-review/); [Freshfields](https://www.freshfields.com/en/our-thinking/blogs/risk-and-compliance/china-intensifies-export-controls-over-rare-earths-and-related-technologies-102lpyn)) | Cliffs in November 2026 | **Not for today's Si DRAM.** "≥256-layer" targets NAND. The real exposure is in tools (RE magnets; ASML, AMAT, Lam and KLA were named by analysts ([SCMP](https://scmp.com/tech/tech-war/article/3328582/chinas-new-rare-earth-export-controls-will-impact-global-chip-supply-chain-analysts-say))) and in **new** cells: IGZO (Ga, In), 3D DRAM (Ge), AlScN (Sc) |

---

## 3. What actually binds DRAM supply (evidence)

1. **Cleanroom floor space × construction time.**
   - Micron: bit growth mid-20s % in 2026 and low-20s % in 2027–28, with "no clear line of sight" to balance. New cleanrooms are not meaningful before late 2028 ([CIO](https://cio.com/article/4229625/memory-squeeze-set-to-tighten-through-2028-micron-says.html)).
   - Korean reporting: expansion is limited by cleanroom square footage, with new fabs arriving 1H27 and utilization above 90% ([JoongAng Daily](https://www.koreajoongangdaily.com/business/samsung-and-sk-are-expanding-fast-but-why-is-memory-still-in-short-supply/12526698)) [REPORTED].
   - Fab lead time (3–4 years) is the dominant constant [UNVERIFIED-PK].
2. **Capital.**
   - DRAM capex was $53.7B in 2025 and is **$61.3B in 2026**: Micron $13.5B, SK hynix $20.5B, Samsung $20B. Most of it goes to node conversion and HBM, not new wafer starts ([TrendForce](https://trendforce.com/presscenter/news/20251113-12780.html)).
   - Depreciation is ~56% of the leading-edge wafer cost (ram-venture). All materials and consumables together are ~$700–900 of a $3,800 wafer (ram-venture cost_inputs). Of that, the scarce-element portion is under $25 [ESTIMATE].
3. **Tools.** About 65 EUV tools per year are shared by logic and memory. Memory system sales are +75% in 2026 as DRAM moves from DUV multipatterning to single-expose EUV (MarketBeat). Deposition and etch tools for 50:1 capacitor holes are also lead-time items [UNVERIFIED-PK].
4. **HBM's wafer appetite.** At ~$6.08/GB HBM cost vs $1.48 DDR5 (ram-venture), each HBM GB displaces ~2.5–3 DDR5 GB of wafer capacity [ESTIMATE]. This is the main reason 2026 bit supply lags.
5. **Site infrastructure.** Yongin's ~15 GW vs <2 GW local supply, and water pipes not due until ~2034 (Tom's Hardware). Clay's 16 TWh/yr and 48 MGD. These gate *where* and *how fast* capacity lands, not whether the materials exist.
6. **Specific inputs: not binding in 2022–26 on available evidence.** The one to watch is **helium**: Qatar has been offline since March 2026 with no restart date as of June. If inventories and US long-term contracts fall short, etch and CVD throughput would be first hit.

---

## 4. Resource exposure of *new* DRAM concepts (design rules for Phases B–C)

These are hypothetical rows from the model. Each assumes the **entire** DRAM fleet (22.2M wafers/yr) adopts the cell, so it bounds exposure at full scale.

| Concept element | Consumed per wafer | Fleet t/yr | % of world supply | $/wafer (2026 prices) | Physics verdict | Revival / mitigation condition |
|---|---|---|---|---|---|---|
| **Ru capacitor electrodes** (2 × 5 nm on 3.3 m²) | 2.8 g (15% ALD utilization) | 62 | **176%** | 156 (4.1%) | Physics OK; **resource-killed at fleet scale** | Lives if ≥90% of precursor and chamber Ru is recovered (100% utilization → 26%), or if electrodes go ≤2 nm, or Ru is used only in a niche/high-margin tier |
| **HZO ferroelectric capacitor** (10 nm) | 0.5–1.5 g Hf | 11–33 | **14–41%** | 6–18 (0.2–0.5%) | OK; supply must grow | Hf is separation-limited: needs new Zr/Hf solvent-extraction capacity (~100× more Hf sits in mined zircon), or HZO → Zr-rich/Hf-lean ferroelectrics |
| **3D DRAM Si/SiGe superlattice** (100–200 pairs) | 0.4–2.4 g Ge | 9–53 | **6–38%** | 1–7 | OK; China ~2/3 of refined Ge [UNVERIFIED-PK] | Germane recovery from epi exhaust; thinner or lower-Ge sacrificial layers; non-SiGe sacrificial stacks (oxide/nitride, NAND-style) |
| **AlScN ferroelectric on 3D capacitor area** | 0.11 g Sc | 2.5 | **~13%** | — | OK; Sc supply is tiny and concentrated | Planar crossbar AlScN uses ~0.3% of world Sc: keep AlScN planar or BEOL, or lower the Sc fraction |
| **IGZO channel** (×5 area) | 26 mg In, 16 mg Ga | 0.6 In, 0.4 Ga | 0.06% / 0.05% (×40 tiers: Ga 0.4%) | — | **OK on quantity** | The risk is licensing, not depletion: Ga is ~98% Chinese [UNVERIFIED-PK] and the US-ban suspension expires 2026-11-27. Prefer In–Sn–Zn or In–W–O channels, or an allied Ga stockpile |
| **Today's ZrO2 / TiN / W / Cu** | — | 19 / – / 150 / 44 | <0.2% | <3 | Fine | — |

**Rule for ideation:** prefer cells built from **Si, O, N, Al, Ti, Zr, W/Mo, Cu, In (small)**. Flag any concept whose fleet-scale demand exceeds **5% of world supply** of an element (Ru, Hf, Ge, Sc today). Each such concept must carry a recovery plan.

---

## 5. White spaces: where a new approach would be worth the most

Ranked by (size of the binding intensity it attacks) × (physics plausibility) × (can a small team prove it at MPW / nanofab scale).

1. **Bits per cleanroom-hour and per capex dollar.** This is the real binding constraint.
   - **Today:** 3,068 GB per 1-beta wafer at ~$145–170k per wafer-start-per-month of capacity, plus a 3–4-year build.
   - **Target physics:** add bits by *deposition* rather than *lithography*, with layers defined in one etch the way 3D NAND does it. Two routes are monolithic BEOL-stackable cells (oxide-channel gain cells over periphery) and multi-level cells.
   - **Arithmetic** [ESTIMATE]: an N-tier array where each tier adds ~10–15% of wafer cost gives ~N/(1+0.125N) × bits per $. For N = 8 that is **~4× bits per $** and ~8× bits per wafer start. If tool time scales with wafer cost, that is ~4× bits per cleanroom-hour on the same floor.
   - **Constraint:** the element rules in §4. Avoid Ge-heavy SiGe stacks and Ru electrodes unless recovered.
2. **Use-phase energy: refresh and retention.**
   - **Lifetime energy:** ~6.6 kWh per GB over 5 years in a server, against 0.42 kWh/GB to make it. **Operating energy is ~16× manufacturing energy** [ESTIMATE].
   - **Refresh:** it grows with density. RAIDR (ISCA 2012) projected refresh at up to ~40–50% of DRAM power for 64Gb-class devices [UNVERIFIED-PK].
   - **Candidate cells:** retention 100–10,000× longer than a 64 ms DRAM cell. Oxide channels reach Ioff ~1e-19 A/µm and >400 s retention (imec IEDM 2020, via ram-venture A1).
   - **Architecture route:** retention-aware refresh.
   - **Why it fits a small team:** a retention or refresh-energy claim can be proven on a small array.
3. **EUV-free, helium-light, PFAS-light patterning and process for perfectly periodic arrays.**
   - **Why now:** the densest DRAM node in the repo (Micron 1β, 0.447 Gb/mm²) uses **zero EUV**. EUV tools cost ~$290M each, draw ~10 GWh/yr each and ship ~65/yr. DRAM arrays are periodic, so self-aligned multipatterning, nanoimprint and directed self-assembly suit them better than they suit logic.
   - **Chemistry:** pair this with chemistries that drop the live chokepoints:
     - PFAS-free resists (metal-oxide or dry resist);
     - non-fluorocarbon or low-GWP high-AR etch;
     - helium-recapture or helium-free chuck cooling;
     - Ru, Hf and Ge recovery loops.
   - **Size of the prize:** smaller per wafer (EUV ≈ 5% of DRAM wafer kWh; electricity 3.4% of cost). It does reduce single-supplier (ASML, 3M legacy, Qatar) exposure, and it is the most U.S.-manufacturable of the three.

Lower-ranked:
- Crucible-quartz substitution (synthetic or alternative HPQ for CZ crucibles): a tail risk only.
- Fab-water intensity: a siting enabler, but under 1% of cost.
- W → Mo: already underway by incumbents.

---

## 6. Dated cliffs to watch

| Date | Event | DRAM relevance |
|---|---|---|
| ~2026-11-10 | One-year suspension of China's 2025-10-09 rare-earth package lapses unless extended [date UNVERIFIED-PK] | Tool magnets (0.1% de minimis); ≥256-layer memory review hits NAND, not DRAM |
| 2026-11-27 | Suspension of the Ga/Ge/Sb export ban to the US ends ([Fastmarkets](https://fastmarkets.com/insights/china-suspends-export-prohibition-on-superhard-materials-us)) | IGZO and 3D-DRAM (Ge) concepts; dual-use licensing continues regardless |
| End-2026 | SEAC final opinion on the EU universal PFAS restriction; draft ban 18 months after entry into force ([SGS](https://www.sgs.com/news/2026/04/safeguards-05026-echa-consults-over-seacs-draft-opinion-on-pfas-restrictions-under-reach)) | Resists, etch gases, fluoropolymer parts, chiller fluids; derogation scope still open |
| 2026–27+ | Ras Laffan helium restart: no date as of June 2026; "years" of repair possible (AP, IUMI) | Etch and CVD backside cooling; Korea most exposed |
| 2027 | ASML ~80 low-NA EUV tools; SK hynix Yongin first cleanroom (~Feb-2027) and Micron ID1 (~mid-2027) per trackers (via CIO/JoongAng snippets) | First relief on cleanroom space |
| Late 2028+ | Micron's new cleanroom output becomes meaningful (CIO) | The end of the capital and time bottleneck |

---

## 7. What I could not verify

- A **primary** DRAM-specific kWh/wafer, or a vendor water-per-wafer figure. Both are triangulated.
- A neon price series for 2025–26.
- Helium status after June 2026.
- Whether the November 2026 Chinese suspensions will be extended.
- Final EU PFAS semiconductor derogations.
- Copper and cobalt 2026 prices (irrelevant at grams per wafer).
- World Hf, Ru, Ge and Sc production figures (all UNVERIFIED-PK). The element table's "% of world" column scales directly with them and with the assumed ALD and epi utilization, which is the largest single uncertainty.
