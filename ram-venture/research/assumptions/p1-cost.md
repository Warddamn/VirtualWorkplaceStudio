# Assumptions — p1-cost (DRAM cost stack and alternative-memory cost inputs)

As of 2026-11-01. Every number below also appears in `research/phase1/cost_inputs.json` with low/base/high values.

## Method and access limits
- [p1-cost] **This agent could not search or fetch the web.** WebSearch returned "budget used up" on its first call (the shared 200-call budget was already spent). WebFetch failed with ENOTFOUND for semiwiki.com, kitguru.net, xenospectrum.com and anysilicon.com, and the proxy log shows 403s for trendforce.com, investors.micron.com and sec.gov. Facts therefore come from four places: (1) open-source repos opened via `git clone` (VERIFIED); (2) URLs other agents saw in search snippets (REPORTED, cross-referenced); (3) prior knowledge from training data up to about mid-2026 (UNVERIFIED: PK); (4) my own computations (ESTIMATE). — basis: tool errors in this session.
- [p1-cost] In `cost_inputs.json`, `confidence` takes only VERIFIED, REPORTED or ESTIMATE, as the task specified. UNVERIFIED prior-knowledge items are written as `confidence: ESTIMATE` with `tag: UNVERIFIED`. — basis: task schema plus the honest-labelling rule.

## Wafer cost
- [p1-cost] Greenfield DRAM capex per wafer-start-per-month: 1α $130k (110–150k), 1β $145k (120–180k), 1γ/1c $170k (140–210k). — basis: analyst rule of thumb of $1.1–2.1B per 10k wpm (PK); not verified.
- [p1-cost] Tools are 78% of capex (70–85%) and depreciate straight-line over 5 years (5–7). The building depreciates over 25 years. Utilization is 95% in 2026. — basis: Korean makers use ~5-year lives (PK); utilization from the current shortage.
- [p1-cost] Cash cost per wafer (materials, consumables, labor, utilities, spares; excludes depreciation and R&D): 1α $1,550, 1β $1,650, 1γ $1,850. — basis: bottom-up judgment. Prime 300mm wafer about $100–130 (PK).
- [p1-cost] Fully loaded front-end wafer cost: 1α $3,400 (3.0–4.0k), 1β $3,800 (3.2–5.5k), 1γ/1c $4,300 (3.7–6.0k). The 1β high of $5.5k covers the A1/A2 Phase-2 assumption of $5.5–6k. — basis: bottom-up formula in `cost_stack.md` §2, cross-checked top-down against 2023.
- [p1-cost] 2023 top-down check: DRAM revenue about $48–52B at roughly breakeven gross margin; capacity 1.65–1.75M wpm at 75–85% utilization; back-end 12–15% of COGS. Implied blended front-end cost is about $2.4–3.1k per wafer. — basis: PK revenue and capacity. Utilization comes from p1-market's TrendForce snippet (74–82% in 2Q23).
- [p1-cost] A fully depreciated legacy 300mm DRAM line has a cash cost of about $1,300 per wafer (1.0–1.8k). A new 2x/1x-nm line costs about $2,800 (2.3–3.5k). A PSMC-class DRAM foundry wafer costs about $1,600 (1.2–2.2k). — basis: judgment and PK. No public quote exists.
- [p1-cost] One EUV exposure costs about $62 per wafer, and a fully loaded EUV layer about $150 (100–250). — basis: NXE:3800E at ~$220M over 5 years, ~$12M/yr service, 80% uptime, 130 wph effective.
- [p1-cost] EUV layer counts by maker and node (Samsung 1a = 5, SK hynix 1a = 1, Micron 1β = 0, Micron 1γ = 1, Samsung/SK hynix 1b about 4–6, 1c about 5–7, CXMT = 0). — basis: company announcements and press, from PK. Only the CXMT zero (export controls) and the Samsung 1a five-layer claim are high-confidence.

## Die size, density and yield
- [p1-cost] DDR5 16Gb density: 1z 0.241 Gb/mm² (REPORTED), 1α 0.30 (0.28–0.33), 1β 0.39 (0.33–0.44), 1γ/1c 0.48 (0.44–0.55). — basis: CXMT/Micron teardown snippet (A1). Kurnal's 0.436 for 1b is the upper bound; 0.33 is back-calculated from the HBM die penalty. Micron's own claims (+40%, +35%, +30% per node) would imply higher values. I discounted them because company figures usually quote array or best-product density.
- [p1-cost] 24Gb and 32Gb DDR5 dies scale linearly with capacity at the same density; the 32Gb part gets a small array-efficiency gain (0.40 Gb/mm²). — basis: judgment.
- [p1-cost] LPDDR5X density is about the same as DDR5 on the same node. — basis: PK.
- [p1-cost] HBM3E 24Gb core die is about 110 mm² (95–125); HBM4 core die is about 125 mm² (110–140). An HBM die is about 1.40× a DDR5 die of the same capacity on the same node, and its yield is 20–30% lower. — basis: TrendForce 2024 note recalled from PK; Micron's ~3:1 trade ratio (REPORTED via p1-market snippet).
- [p1-cost] Mature DRAM die yield after repair is 0.90 (0.85–0.95). Ramp yield is 0.60 (0.30–0.80). 1γ/1c in 2026 yields 0.80. A 12-high HBM3E stack yields 0.75 (0.60–0.90). — basis: industry heuristic and SK hynix's "nearly 80%" HBM3E remark (FT, 2024-05; PK).
- [p1-cost] Edge exclusion is 3 mm (2–5) and the scribe lane 80 µm (60–200). — basis: PK for memory fabs; Chiplet Actuary uses 5 mm and 200 µm (VERIFIED) as conservative values.
- [p1-cost] Legacy die sizes (DDR4 8Gb: 20nm 80, 1x 55, 1y 45, 1z 39 mm²; DDR3 4Gb: 25nm 60, 3x-nm 80 mm²; DDR3 2Gb 38nm 50 mm²) are estimates from typical node densities and are not teardown-verified. — basis: PK.

## Back-end and module
- [p1-cost] Back-end per DDR5 16Gb component is about $0.45 ($0.30–0.75): probe $0.10, FBGA assembly $0.18, final test and burn-in $0.17. That is about $0.225/GB. — basis: judgment that back-end is roughly 10–15% of COGS at trough prices.
- [p1-cost] The TSV process adds about $650 per wafer (450–1,000). HBM stacking and test cost about $25 per 12-high stack (15–45). Base die: HBM3E $15, HBM4 $35 (logic process). — basis: judgment and PK.
- [p1-cost] 64GB RDIMM non-DRAM BOM: RCD $7, PMIC $3.5, SPD hub $0.7, 2 temperature sensors $0.35 each, PCB $4, passives $1.2. Total $17.1. Assembly and test cost $3.5 in Asia and about $12 in the U.S. (p1-backend). — basis: PK; p1-backend used about $25 for parts at U.S. low-volume pricing.
- [p1-cost] Module yield is 98.5%. — basis: judgment.

## Prices
- [p1-cost] A chip-level DDR5 16Gb contract price is not public. I back it out from 64GB RDIMM contract prices of $900–1,586 (base $1,250) minus about $20 of non-DRAM cost, divided by 40 devices. That gives about $30 per chip (22–39). — basis: Counterpoint via p1-market; Citi forecast UNVERIFIED.
- [p1-cost] DDR5 16Gb spot at the 2023 trough was about $3.2 per chip (2.8–3.6). — basis: PK.
- [p1-cost] The glut scenario is a 60% decline (mission rule 6). A severe case is an 85–90% decline back to 2023 cost-floor pricing. — basis: mission plus p1-market.

## Trailing node and alternative memory
- [p1-cost] The 2020-basis foundry wafer prices (TSMC-class: 28nm $2,891 and so on) are taken from the Chiplet Actuary parameter file (VERIFIED as published there). I attribute their origin to CSET's 2020 "AI Chips" report from PK. 2026 adjustments: 28nm $2,600 (1.8–3.2k), 40nm $2,100, 65nm $1,700, N3 $20k, N2 $30k. — basis: PK of the 2024–25 mature-node price war and 2025 advanced-node reports.
- [p1-cost] 200mm wafers: 180nm in Asia $700 (450–1,000); 90–130nm in Asia $1,000; SkyWater 130nm $1,400 (shared with p1-fabs, A1 and A2); U.S. 65–90nm $2,000. — basis: PK and cross-agent consistency.
- [p1-cost] Embedded NVM mask adders: eMRAM +4 masks (3–5) for about +$800 per wafer; eFlash +11 (9–14); RRAM +2 (1–3) for about +$250; CBRAM +1 (GF, REPORTED); FRAM +2 (TI 130nm, REPORTED). — basis: PK plus A1/A2 cross-references.
- [p1-cost] SRAM silicon $/GB assumes 60% macro array efficiency and 92% usable wafer area, and excludes test and packaging. — basis: judgment. Small macros are far worse (GF180 4-kbit macro is about 20 kbit/mm², VERIFIED).
- [p1-cost] NAND TLC costs $0.025/GB at the 2023 trough and $0.09/GB in 2026 (0.06–0.15). NOR costs about $40/GB (20–70). — basis: PK plus p1-market's NAND compounding.
- [p1-cost] An oxide-TFT backplane costs about $50/m² ($25–110), or $275 per Gen-8.5 sheet ($140–600). A1 used $500 per sheet. — basis: PK that the array is 20–30% of LCD panel cost. No U.S. line exists.
