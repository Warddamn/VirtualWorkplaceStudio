# Assumptions — p1-fabs (U.S. wafer fabs and TFT/display capacity)

Written 2026-11-01. One bullet per assumption or judgment call.

## Evidence-handling judgments
- [p1-fabs] My first WebSearch call returned "budget used up" (the 200-search limit per turn is shared by every agent, and other agents had used it all). WebFetch to www.everspin.com and www.skywatertechnology.com failed with "host not in allowed network domains". The proxy log also shows trendforce.com, sec.gov and investors.micron.com refused. Following the tool instructions, I stopped trying other sites. Everything in `phase1/us_fabs.md` therefore comes from one of two places: (a) snippets other agents logged (A1, A2, p1-micron), cross-referenced in `sources/p1-fabs.jsonl` and tagged so; or (b) my prior knowledge (training data through about mid-2026), tagged [UNVERIFIED]. — basis: tool error messages; proxy status `recentRelayFailures`.
- [p1-fabs] I logged URLs from other agents' logs in my jsonl with an explicit "CROSS-REFERENCE … p1-fabs did not independently open" note. I did this rather than leave them unlogged, so the merge tool can trace every URL my note cites. I added no URL that does not already appear in another agent's log. — basis: CONVENTIONS "never invent a URL" plus "log every source you rely on". This was the most transparent way to satisfy both.
- [p1-fabs] Where my prior-knowledge facts have no logged URL, I name the source document and date in prose with no link, and tag the fact [UNVERIFIED]. — basis: never invent URLs.
- [p1-fabs] I tag a snippet of a primary filing seen by another agent [REPORTED-P], matching the p1-micron convention. Nothing in this note is [VERIFIED], because no primary page was opened. — basis: CONVENTIONS tag definitions.

## Facility facts taken from prior knowledge (all need a re-check)
- [p1-fabs] GF's U.S. fabs (Malta Fab 8 at 12/14nm; Essex Junction Fab 9 at 90–350nm, 200mm) run no eMRAM or eReRAM in volume production. GF's eMRAM is on 22FDX in Dresden. — basis: prior knowledge, plus the A2 snippet that AutoPro150 eMRAM is produced at Dresden. Confidence ~75%.
- [p1-fabs] GF's 14HP (IBM-derived 14nm FinFET-on-SOI with deep-trench eDRAM) was built at Malta for IBM z15/POWER9. Whether it is still offered in 2026 is unknown. — basis: prior knowledge. Confidence that it existed is ~85%; that it is still running in 2026, ~40%.
- [p1-fabs] Everspin's Chandler line processes 200mm wafers only. Its STT-MRAM products (256Mb on 40nm, 1Gb on 28nm, xSPI family) are made front to back at GF Singapore (300mm), not in the U.S. — basis: A2 snippet of the FY2025 10-K; my prior knowledge for the 200mm-only detail. Confidence ~80%.
- [p1-fabs] SkyWater Bloomington holds DMEA Trusted Foundry accreditation (Category 1A, since ~2017) and is open to commercial customers. — basis: prior knowledge. Confidence ~90%.
- [p1-fabs] SkyWater Fab 25 (Austin) inherits Cypress/Infineon 65nm-class CMOS and SONOS embedded-NVM know-how. Whether SONOS is offered to foundry customers is unknown. — basis: prior knowledge of Cypress PSoC/SONOS at Fab 25. Confidence ~50% on the SONOS-as-foundry-offering point.
- [p1-fabs] TI runs no external foundry business. Its embedded FRAM (MSP430FR) and the Weebit ReRAM license are captive. — basis: prior knowledge plus the A2 snippet. Confidence ~90%.
- [p1-fabs] Polar Semiconductor is becoming a U.S.-owned commercial 200mm foundry for power and sensors, with ~$123M of CHIPS support and ~$175M of private equity (2024). — basis: prior knowledge. Confidence ~70% on the exact figures.
- [p1-fabs] Intel does not offer eMRAM or eReRAM to external foundry customers on Intel 16, Intel 3 or 18A, despite its 22FFL eMRAM/ReRAM ISSCC 2019 papers. — basis: prior knowledge; no public external offering seen. Confidence ~65%.
- [p1-fabs] No Gen-4-or-larger LCD, OLED or oxide-TFT panel fab operates in the U.S. as of 2026-11. — basis: prior knowledge (Foxconn Wisconsin Gen 10.5 never built) plus the A1 snippet that TrendForce TFT-capacity data shows no U.S. fabs. Confidence ~95%.
- [p1-fabs] The Twin Cities hold an unusual concentration of magnetic thin-film/MTJ wafer capability: Seagate Bloomington head-wafer fab, NVE Eden Prairie, Honeywell Plymouth, SkyWater and Polar. None of them offers MTJ foundry service to outsiders. — basis: prior knowledge. Confidence ~70%.

## Prices, rates and capex (all [ESTIMATE])
- [p1-fabs] Processed-wafer prices: 200mm 130–180nm foundry ≈ $900–1,600; 200mm 65–90nm ≈ $1,500–2,500; 300mm 22FDX ≈ $3,500–4,500; 300mm 12/14nm ≈ $4,000–6,000; Intel 18A not public. — basis: public foundry price lore, consistent with A1 ($1,200 for 200mm 130nm) and A2 ($1,400–1,600 for SkyWater S130 + ReRAM, $4,500 for 22FDX + eMRAM). ±30–50%.
- [p1-fabs] MPW/shuttle costs: SkyWater 130nm open-source-style shuttle ≈ $10–15k per ~10 mm² slot; commercial 130nm MPW ≈ $1–3k/mm² with a minimum of ~$15–40k; 22FDX MPW ≈ $10–25k/mm²; full 130nm mask set $500–600k (A1/AnySilicon snippet). — basis: pre-2026 shuttle price lore plus the A1-logged snippets. ±50%.
- [p1-fabs] University nanofab external rates: industrial users ≈ $75–250 per tool-hour plus ~$100–200 per staff-hour; academic users ≈ $30–90 per hour. A device-level IGZO or HZO learning program (3–6 months) ≈ $20–80k. — basis: memory of typical NNCI rate sheets; not re-verified for 2026.
- [p1-fabs] A minimal 200mm IGZO BEOL tool set (refurbished: oxide-target PVD, PECVD, ALD, anneal, ICP etch, wet bench, parametric test), dropped into an existing cleanroom, costs ≈ $4–10M in tools plus fit-out. That is tier T2. — basis: used-tool market lore. ±50%.
- [p1-fabs] Planar IGZO 2T0C cell = 20–40 F² with array efficiency 60%. At F = 130nm that is 0.9–1.8 Mb/mm² per tier, 250–490× less dense than DDR5 1b (0.436 Gb/mm², A1 basis). At F = 65nm it is 60–120× less dense. — basis: computed in scratch (igzo_density.py, not a deliverable). Cell size is an assumption.

## Judgment calls
- [p1-fabs] "Memory-relevant" here means the fab could make standalone or embedded memory (DRAM, SRAM, MRAM, ReRAM, CBRAM, FeRAM/FeFET, SONOS/flash, PCM, IGZO) or host a BEOL memory module. Pure SiC, GaN or GaAs fabs are listed only for completeness, as idle-capacity candidates.
- [p1-fabs] I treat the Everspin–Microchip exclusivity clause (A2 snippet) as closing Gresham Fab 4 to any third-party MTJ startup.
- [p1-fabs] I treat the §48D 35% ITC as practically unavailable to a new founder-led BEOL line, because construction must begin by 2026-12-31 (p1-micron), which is 2 months away.
