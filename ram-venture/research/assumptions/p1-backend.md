# Assumptions — p1-backend (U.S. back-end, modules, die supply, mil/aero, recertification, test)

Session constraints affecting every fact: the shared WebSearch budget (200 calls per turn) was used up by sibling agents before this agent's first search. WebFetch could not resolve en.wikipedia.org or ir.amkor.com, and per tool guidance no further hosts were tried. The proxy log shows sec.gov, trendforce.com and investors.micron.com denied. No web page was opened by p1-backend.

## Evidence-handling assumptions
- [p1-backend] URLs cited in phase1/us_backend.md were copied programmatically from sibling logs (p1-micron, p1-market, A1, A2) and re-logged as CROSS-REFERENCE entries. Facts resting on them are at most [REPORTED]. — basis: CONVENTIONS source-logging rules; no independent access.
- [p1-backend] Facts from my training knowledge (through about mid-2026) are tagged [UNVERIFIED: PK] and carry no URL, because CONVENTIONS forbids citing URLs not opened or seen in search results. Regulations are cited by section number so they can be checked directly. — basis: CONVENTIONS "Never invent a URL".
- [p1-backend] Where PK figures conflict with my memory (e.g., Amkor AZ at $2B vs $7B, production 2027 vs early 2028), the later and larger figure is shown with a lower-confidence note. — basis: recency of recall; listed in §9 as a check.

## Company / capacity judgments
- [p1-backend] No U.S. facility packages commodity DDR4/DDR5 FBGA at volume as of 2026-11. — basis: PK of Micron, Samsung, SK hynix and OSAT back-end footprints (all Asia); sibling evidence that Micron's U.S. back-end plan is HBM after ID2 (late 2028) and SK hynix Indiana is HBM from 2028–29.
- [p1-backend] Amkor Peoria will not package commodity DRAM; its planned scope is logic 2.5D/fan-out plus test for Apple, NVIDIA and TSMC. — basis: PK of the 2023 announcement, the 2024 TSMC MOU and NVIDIA's Apr 2025 statement.
- [p1-backend] Kingston holds roughly 70–80% of third-party module-house revenue and assembles in Fountain Valley, CA. — basis: PK of TrendForce annual module-house rankings (2022–2024) and Kingston facility descriptions; UNVERIFIED.
- [p1-backend] Natcast's NSTC agreement was voided by Commerce in Aug 2025 and NSTC moved under NIST. Post-2025 NAPMP/APPF status is unknown. — basis: PK; flagged for the funding agent.
- [p1-backend] "Simms" in the task brief could not be matched to a U.S. module maker; treated as unidentified. — basis: no PK match except the UK distributor Simms International.

## Numeric assumptions (scratch script scratchpad/p1-backend/backend_estimates.py)
- [p1-backend] Servers retired per year ≈ 2020–21 global server shipments: 11.0M / 12.0M / 13.5M (low/mid/high). — basis: PK of TrendForce/IDC server shipment levels (~11–14M/yr); 5–6 year hyperscaler depreciation lives.
- [p1-backend] DRAM per retired DDR4-era server: 256 / 384 / 512 GB. — basis: 2-socket servers with 8–16 RDIMMs of 16–64GB; ESTIMATE.
- [p1-backend] U.S. share of retiring servers: 35% / 40% / 45%. — basis: U.S. share of global hyperscale capacity, PK; ESTIMATE.
- [p1-backend] Fraction of U.S. retired DRAM reaching the open secondary market: 20% / 35% / 50%. — basis: judgment; hyperscalers reuse internally (Microsoft Circular Centers, CXL-DDR4 reuse), some scrap and bulk export; ESTIMATE.
- [p1-backend] Global new DRAM bits 2024 ≈ 32 EB = $97B revenue ÷ $3/GB average. — basis: PK of 2024 DRAM revenue; ASP consistent with p1-market's pre-spike $1.3–3/GB contract range; ESTIMATE.
- [p1-backend] Used DDR4 RDIMM price, 2023–24: $0.8–1.2/GB. — basis: PK recall of eBay sold listings (32GB ~$25–40, 64GB ~$50–100); consistent with the DDR4 8Gb contract bottom of $1.30 (Sep 2023, KED Global via p1-market).
- [p1-backend] Used DDR4 RDIMM price, 2026: $3–8/GB. — basis: floor = 0.5 × consumer retail DDR4 32GB-3200 ≈ $190 (p1-market, Sep 2026) ≈ $3/GB, using the 2023 used-RDIMM/new-consumer ratio of ~0.5; ceiling bounded well below DDR4 8Gb spot of $21–44/GB (TrendForce board 2026-08-03; BuySellRAM 2026-08-31). Unverified. The kill check is eBay sold listings.
- [p1-backend] Used DDR4 RDIMM price in a 2028–29 glut: $0.5–1.5/GB. — basis: 2023 analog plus DDR4 EOL premium unwinding and CXMT backfill (p1-market §7); ESTIMATE.
- [p1-backend] Recert unit economics: buy at 60% of resale; fees 13.25% (marketplace plus payment); shipping $5; test 6 min at $25/hr; failure write-off 3%; returns 3% (cost = shipping + half the test time). — basis: typical eBay business-seller fee level and ITAD lot pricing norms; ESTIMATE.
- [p1-backend] DDR5 64GB 2Rx4 RDIMM build: 40 × 16Gb die (80 GB raw); RCD $8, PMIC $5, SPD hub and sensors $2, PCB $8, passives $2; U.S. assembly and test $12/module. — basis: JEDEC DDR5 RDIMM architecture (two 40-bit subchannels); component prices from PK; ESTIMATE.
- [p1-backend] DRAM $/GB scenarios for the BOM: 2023 trough $1.5, 2026 contract $14–25 (p1-market server RDIMM contract range), glut $6. — basis: p1-market §2.3 and §7.
- [p1-backend] KGD wafer math: 300mm gross-die formula; die areas DDR3 4Gb 55 mm², DDR4 8Gb 45 mm², DDR5 16Gb 70 mm²; 85% good-die yield; $/GB of $6 (legacy), $16 (DDR4), $14 (DDR5). — basis: PK of approximate die sizes by node; prices from p1-market; ESTIMATE.
- [p1-backend] KGD premium over packaged-equivalent $/GB: 15–40%. — basis: test-cost norms; ESTIMATE.
- [p1-backend] Program MOQ = one 25-wafer lot ⇒ ~$75k (legacy) to ~$550k (DDR4/DDR5). — basis: wafer math above; ESTIMATE.

## Regulatory assumptions (all [UNVERIFIED: PK]; verify against the eCFR)
- [p1-backend] TAA threshold ≈ $174,000 for supplies (FAR 25.402, 2024–25 adjustment). Taiwan, Korea and Japan are designated countries; China is not.
- [p1-backend] BAA: COTS items manufactured in the U.S. are domestic end products without a component test. Price evaluation factors are 20% (large business) and 30% (small business) for civilian agencies and 50% for DoD. The non-COTS domestic-content threshold is 65% for 2024–2028 and 75% from 2029.
- [p1-backend] FTC Made in USA Labeling Rule (16 CFR Part 323, 2021): an unqualified claim requires "all or virtually all" U.S. content; a module on foreign die may claim "Assembled in USA."
- [p1-backend] NDAA FY2023 §5949 bars federal procurement of products containing SMIC/YMTC/CXMT chips from Dec 2027 (also reported by p1-micron). Whether the FAR implementing rule reaches DIMMs inside servers is unverified.
- [p1-backend] DFARS 252.246-7007/-7008 and FAR 52.211-5 together effectively bar used or recovered DRAM from DoD deliverables absent contracting-officer approval.
- [p1-backend] NIST SP 800-88 treats power removal as sanitization for volatile DRAM, so recovered DIMMs need no data destruction.

## Judgment calls
- [p1-backend] Chip-level die harvesting is judged non-viable in the U.S. (x4 server die cannot go on consumer modules; reflow risk; counterfeit-inspection flags; labor cost). Module-level recert is the only U.S.-viable recovered-DRAM model. — basis: technical PK plus economics.
- [p1-backend] Hi-rel/space memory premium is set at 10–100× commodity $/bit and hi-rel MCM gross margins at 40–60%+. — basis: hi-rel component industry norms; ESTIMATE.
- [p1-backend] Commodity "U.S.-assembled" module premium is set at 0–10%, only in BAA-covered small federal buys. — basis: the regulatory analysis above; ESTIMATE.
- [p1-backend] Module-house gross margins: commodity 5–15% in normal years; industrial 20–35%; Netlist low single digits to ~10%. — basis: PK of Taiwanese listed module houses and Netlist filings; UNVERIFIED.
- [p1-backend] Test-equipment prices (new ATE $1–5M+; used DRAM ATE $20–300k; RAMCHECK LX ~$1.5–2k plus adapters; CST $5–50k; AS6171 lab $0.3–1M+) are order-of-magnitude recall and industry norms. — basis: PK; ESTIMATE.
