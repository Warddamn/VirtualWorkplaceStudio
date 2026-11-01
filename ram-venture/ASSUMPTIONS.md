# ASSUMPTIONS

Every assumption this engagement makes beyond the Founder Profile in `research/MISSION_PROMPT.md`. Entries are numbered A-xx so deliverables can cite them. Assumptions logged by individual agents go first to `research/assumptions/*.md` and are folded in here at the end of each phase. Where a later phase revised an assumption, the revision is noted.

## Phase 0 — framing assumptions (orchestrator, 2026-11-01)

| ID | Assumption | Basis |
|---|---|---|
| A-01 | "Today" is **2026-11-01**. Every "now" price or status means the latest public data at or before this date. | Session date |
| A-02 | All money is **nominal USD**. Foreign figures are converted at a spot rate stated where used: KRW≈1,400/USD, TWD≈31/USD, JPY≈150/USD unless a source gives USD directly. | Convention; FX is immaterial at the precision of this study |
| A-03 | Founder's personal capital is **$40k deployable** (under the stated $50k ceiling), with roughly 15 hours a week until the day job is dropped. Full-time is assumed only once revenue or funding covers a modest salary (~$120k a year loaded). | Founder profile ("modest, < $50k", "keeps the day job") |
| A-04 | "First revenue" means a paying customer invoice, not grants. Grants (SBIR and similar) are treated as non-dilutive **funding**, not revenue. | Mission: "not a grant-farming exercise" |
| A-05 | **Glut scenario:** DDR5 contract $/GB falls 60% from its 2026 peak over 2028–29. Server DRAM falls about the same; legacy DDR4 falls less in % but stays above its 2023 trough. Each glut case is tested against this one scenario. | Mission rule 6 |
| A-06 | **Base scenario** for 2027: prices plateau near Q4-2026 levels through H1-2027, then soften as Micron ID1, SK hynix M15X/Yongin, Samsung P4/P5 and CXMT capacity ramp. Phase 1 revises this. | Mission §1 premise; to be verified |
| A-07 | Scoring is 1–5 per criterion, 5 = best for the venture, so "capital required" and "competitive density" are scored inversely: 5 = least capital, least crowded. | Mission Phase 3 rubric |
| A-08 | TRL follows the NASA/DoD 1–9 scale: 1–3 lab principle, 4–5 component validated in lab/relevant environment, 6–7 prototype in relevant/operational environment, 8–9 qualified/shipping. | Standard definition |
| A-09 | "U.S.-made" means a substantial-transformation step (wafer fab or die-level assembly/test) performed in the U.S. A module assembled in the U.S. from imported dies is "U.S.-assembled", not U.S.-made. | Common procurement usage (TAA/BAA "substantial transformation") — refined in Phase 1 |
| A-10 | Where agents cite paywalled market research (TrendForce, Yole, TechInsights, Omdia), they cite the free press release or news coverage of it. The underlying report is never claimed as read. | Integrity rule |
| A-11 | A concept dies under Rule 3 if it requires building or buying a leading-edge DRAM fab. It also dies if its minimum viable path needs more than $1B (T4), whatever the strategic merit. | Mission rule 3 |
| A-12 | Expected-value judgments use a 36-month horizon for the PRIMARY pick and an unconstrained horizon for the MOONSHOT. | Founder profile |

## Agent-logged assumptions

1013 assumptions logged by 62 agents, merged from `research/assumptions/*.md` by `research/tools/merge_assumptions.py`. IDs are `A-<agent>-<n>`. Where a later phase revised an earlier assumption, the later entry notes it, and the canonical numbers live in the models (`models/dram_cost_stack.py` `ddr5_reference()`).

### Phase 1 — landscape

<details><summary><b>p1-backend</b> (33)</summary>

- **A-p1-backend-1** [p1-backend] URLs cited in phase1/us_backend.md were copied programmatically from sibling logs (p1-micron, p1-market, A1, A2) and re-logged as CROSS-REFERENCE entries. Facts resting on them are at most [REPORTED]. — basis: CONVENTIONS source-logging rules; no independent access.
- **A-p1-backend-2** [p1-backend] Facts from my training knowledge (through about mid-2026) are tagged [UNVERIFIED: PK] and carry no URL, because CONVENTIONS forbids citing URLs not opened or seen in search results. Regulations are cited by section number so they can be checked directly. — basis: CONVENTIONS "Never invent a URL".
- **A-p1-backend-3** [p1-backend] Where PK figures conflict with my memory (e.g., Amkor AZ at $2B vs $7B, production 2027 vs early 2028), the later and larger figure is shown with a lower-confidence note. — basis: recency of recall; listed in §9 as a check.
- **A-p1-backend-4** [p1-backend] No U.S. facility packages commodity DDR4/DDR5 FBGA at volume as of 2026-11. — basis: PK of Micron, Samsung, SK hynix and OSAT back-end footprints (all Asia); sibling evidence that Micron's U.S. back-end plan is HBM after ID2 (late 2028) and SK hynix Indiana is HBM from 2028–29.
- **A-p1-backend-5** [p1-backend] Amkor Peoria will not package commodity DRAM; its planned scope is logic 2.5D/fan-out plus test for Apple, NVIDIA and TSMC. — basis: PK of the 2023 announcement, the 2024 TSMC MOU and NVIDIA's Apr 2025 statement.
- **A-p1-backend-6** [p1-backend] Kingston holds roughly 70–80% of third-party module-house revenue and assembles in Fountain Valley, CA. — basis: PK of TrendForce annual module-house rankings (2022–2024) and Kingston facility descriptions; UNVERIFIED.
- **A-p1-backend-7** [p1-backend] Natcast's NSTC agreement was voided by Commerce in Aug 2025 and NSTC moved under NIST. Post-2025 NAPMP/APPF status is unknown. — basis: PK; flagged for the funding agent.
- **A-p1-backend-8** [p1-backend] "Simms" in the task brief could not be matched to a U.S. module maker; treated as unidentified. — basis: no PK match except the UK distributor Simms International.
- **A-p1-backend-9** [p1-backend] Servers retired per year ≈ 2020–21 global server shipments: 11.0M / 12.0M / 13.5M (low/mid/high). — basis: PK of TrendForce/IDC server shipment levels (~11–14M/yr); 5–6 year hyperscaler depreciation lives.
- **A-p1-backend-10** [p1-backend] DRAM per retired DDR4-era server: 256 / 384 / 512 GB. — basis: 2-socket servers with 8–16 RDIMMs of 16–64GB; ESTIMATE.
- **A-p1-backend-11** [p1-backend] U.S. share of retiring servers: 35% / 40% / 45%. — basis: U.S. share of global hyperscale capacity, PK; ESTIMATE.
- **A-p1-backend-12** [p1-backend] Fraction of U.S. retired DRAM reaching the open secondary market: 20% / 35% / 50%. — basis: judgment; hyperscalers reuse internally (Microsoft Circular Centers, CXL-DDR4 reuse), some scrap and bulk export; ESTIMATE.
- **A-p1-backend-13** [p1-backend] Global new DRAM bits 2024 ≈ 32 EB = $97B revenue ÷ $3/GB average. — basis: PK of 2024 DRAM revenue; ASP consistent with p1-market's pre-spike $1.3–3/GB contract range; ESTIMATE.
- **A-p1-backend-14** [p1-backend] Used DDR4 RDIMM price, 2023–24: $0.8–1.2/GB. — basis: PK recall of eBay sold listings (32GB ~$25–40, 64GB ~$50–100); consistent with the DDR4 8Gb contract bottom of $1.30 (Sep 2023, KED Global via p1-market).
- **A-p1-backend-15** [p1-backend] Used DDR4 RDIMM price, 2026: $3–8/GB. — basis: floor = 0.5 × consumer retail DDR4 32GB-3200 ≈ $190 (p1-market, Sep 2026) ≈ $3/GB, using the 2023 used-RDIMM/new-consumer ratio of ~0.5; ceiling bounded well below DDR4 8Gb spot of $21–44/GB (TrendForce board 2026-08-03; BuySellRAM 2026-08-31). Unverified. The kill check is eBay sold listings.
- **A-p1-backend-16** [p1-backend] Used DDR4 RDIMM price in a 2028–29 glut: $0.5–1.5/GB. — basis: 2023 analog plus DDR4 EOL premium unwinding and CXMT backfill (p1-market §7); ESTIMATE.
- **A-p1-backend-17** [p1-backend] Recert unit economics: buy at 60% of resale; fees 13.25% (marketplace plus payment); shipping $5; test 6 min at $25/hr; failure write-off 3%; returns 3% (cost = shipping + half the test time). — basis: typical eBay business-seller fee level and ITAD lot pricing norms; ESTIMATE.
- **A-p1-backend-18** [p1-backend] DDR5 64GB 2Rx4 RDIMM build: 40 × 16Gb die (80 GB raw); RCD $8, PMIC $5, SPD hub and sensors $2, PCB $8, passives $2; U.S. assembly and test $12/module. — basis: JEDEC DDR5 RDIMM architecture (two 40-bit subchannels); component prices from PK; ESTIMATE.
- **A-p1-backend-19** [p1-backend] DRAM $/GB scenarios for the BOM: 2023 trough $1.5, 2026 contract $14–25 (p1-market server RDIMM contract range), glut $6. — basis: p1-market §2.3 and §7.
- **A-p1-backend-20** [p1-backend] KGD wafer math: 300mm gross-die formula; die areas DDR3 4Gb 55 mm², DDR4 8Gb 45 mm², DDR5 16Gb 70 mm²; 85% good-die yield; $/GB of $6 (legacy), $16 (DDR4), $14 (DDR5). — basis: PK of approximate die sizes by node; prices from p1-market; ESTIMATE.
- **A-p1-backend-21** [p1-backend] KGD premium over packaged-equivalent $/GB: 15–40%. — basis: test-cost norms; ESTIMATE.
- **A-p1-backend-22** [p1-backend] Program MOQ = one 25-wafer lot ⇒ ~$75k (legacy) to ~$550k (DDR4/DDR5). — basis: wafer math above; ESTIMATE.
- **A-p1-backend-23** [p1-backend] TAA threshold ≈ $174,000 for supplies (FAR 25.402, 2024–25 adjustment). Taiwan, Korea and Japan are designated countries; China is not.
- **A-p1-backend-24** [p1-backend] BAA: COTS items manufactured in the U.S. are domestic end products without a component test. Price evaluation factors are 20% (large business) and 30% (small business) for civilian agencies and 50% for DoD. The non-COTS domestic-content threshold is 65% for 2024–2028 and 75% from 2029.
- **A-p1-backend-25** [p1-backend] FTC Made in USA Labeling Rule (16 CFR Part 323, 2021): an unqualified claim requires "all or virtually all" U.S. content; a module on foreign die may claim "Assembled in USA."
- **A-p1-backend-26** [p1-backend] NDAA FY2023 §5949 bars federal procurement of products containing SMIC/YMTC/CXMT chips from Dec 2027 (also reported by p1-micron). Whether the FAR implementing rule reaches DIMMs inside servers is unverified.
- **A-p1-backend-27** [p1-backend] DFARS 252.246-7007/-7008 and FAR 52.211-5 together effectively bar used or recovered DRAM from DoD deliverables absent contracting-officer approval.
- **A-p1-backend-28** [p1-backend] NIST SP 800-88 treats power removal as sanitization for volatile DRAM, so recovered DIMMs need no data destruction.
- **A-p1-backend-29** [p1-backend] Chip-level die harvesting is judged non-viable in the U.S. (x4 server die cannot go on consumer modules; reflow risk; counterfeit-inspection flags; labor cost). Module-level recert is the only U.S.-viable recovered-DRAM model. — basis: technical PK plus economics.
- **A-p1-backend-30** [p1-backend] Hi-rel/space memory premium is set at 10–100× commodity $/bit and hi-rel MCM gross margins at 40–60%+. — basis: hi-rel component industry norms; ESTIMATE.
- **A-p1-backend-31** [p1-backend] Commodity "U.S.-assembled" module premium is set at 0–10%, only in BAA-covered small federal buys. — basis: the regulatory analysis above; ESTIMATE.
- **A-p1-backend-32** [p1-backend] Module-house gross margins: commodity 5–15% in normal years; industrial 20–35%; Netlist low single digits to ~10%. — basis: PK of Taiwanese listed module houses and Netlist filings; UNVERIFIED.
- **A-p1-backend-33** [p1-backend] Test-equipment prices (new ATE $1–5M+; used DRAM ATE $20–300k; RAMCHECK LX ~$1.5–2k plus adapters; CST $5–50k; AS6171 lab $0.3–1M+) are order-of-magnitude recall and industry norms. — basis: PK; ESTIMATE.

</details>

<details><summary><b>p1-cost</b> (30)</summary>

- **A-p1-cost-1** [p1-cost] **This agent could not search or fetch the web.** WebSearch returned "budget used up" on its first call (the shared 200-call budget was already spent). WebFetch failed with ENOTFOUND for semiwiki.com, kitguru.net, xenospectrum.com and anysilicon.com, and the proxy log shows 403s for trendforce.com, investors.micron.com and sec.gov. Facts therefore come from four places: (1) open-source repos opened via `git clone` (VERIFIED); (2) URLs other agents saw in search snippets (REPORTED, cross-referenced); (3) prior knowledge from training data up to about mid-2026 (UNVERIFIED: PK); (4) my own computations (ESTIMATE). — basis: tool errors in this session.
- **A-p1-cost-2** [p1-cost] In `cost_inputs.json`, `confidence` takes only VERIFIED, REPORTED or ESTIMATE, as the task specified. UNVERIFIED prior-knowledge items are written as `confidence: ESTIMATE` with `tag: UNVERIFIED`. — basis: task schema plus the honest-labelling rule.
- **A-p1-cost-3** [p1-cost] Greenfield DRAM capex per wafer-start-per-month: 1α $130k (110–150k), 1β $145k (120–180k), 1γ/1c $170k (140–210k). — basis: analyst rule of thumb of $1.1–2.1B per 10k wpm (PK); not verified.
- **A-p1-cost-4** [p1-cost] Tools are 78% of capex (70–85%) and depreciate straight-line over 5 years (5–7). The building depreciates over 25 years. Utilization is 95% in 2026. — basis: Korean makers use ~5-year lives (PK); utilization from the current shortage.
- **A-p1-cost-5** [p1-cost] Cash cost per wafer (materials, consumables, labor, utilities, spares; excludes depreciation and R&D): 1α $1,550, 1β $1,650, 1γ $1,850. — basis: bottom-up judgment. Prime 300mm wafer about $100–130 (PK).
- **A-p1-cost-6** [p1-cost] Fully loaded front-end wafer cost: 1α $3,400 (3.0–4.0k), 1β $3,800 (3.2–5.5k), 1γ/1c $4,300 (3.7–6.0k). The 1β high of $5.5k covers the A1/A2 Phase-2 assumption of $5.5–6k. — basis: bottom-up formula in `cost_stack.md` §2, cross-checked top-down against 2023.
- **A-p1-cost-7** [p1-cost] 2023 top-down check: DRAM revenue about $48–52B at roughly breakeven gross margin; capacity 1.65–1.75M wpm at 75–85% utilization; back-end 12–15% of COGS. Implied blended front-end cost is about $2.4–3.1k per wafer. — basis: PK revenue and capacity. Utilization comes from p1-market's TrendForce snippet (74–82% in 2Q23).
- **A-p1-cost-8** [p1-cost] A fully depreciated legacy 300mm DRAM line has a cash cost of about $1,300 per wafer (1.0–1.8k). A new 2x/1x-nm line costs about $2,800 (2.3–3.5k). A PSMC-class DRAM foundry wafer costs about $1,600 (1.2–2.2k). — basis: judgment and PK. No public quote exists.
- **A-p1-cost-9** [p1-cost] One EUV exposure costs about $62 per wafer, and a fully loaded EUV layer about $150 (100–250). — basis: NXE:3800E at ~$220M over 5 years, ~$12M/yr service, 80% uptime, 130 wph effective.
- **A-p1-cost-10** [p1-cost] EUV layer counts by maker and node (Samsung 1a = 5, SK hynix 1a = 1, Micron 1β = 0, Micron 1γ = 1, Samsung/SK hynix 1b about 4–6, 1c about 5–7, CXMT = 0). — basis: company announcements and press, from PK. Only the CXMT zero (export controls) and the Samsung 1a five-layer claim are high-confidence.
- **A-p1-cost-11** [p1-cost] DDR5 16Gb density: 1z 0.241 Gb/mm² (REPORTED), 1α 0.30 (0.28–0.33), 1β 0.39 (0.33–0.44), 1γ/1c 0.48 (0.44–0.55). — basis: CXMT/Micron teardown snippet (A1). Kurnal's 0.436 for 1b is the upper bound; 0.33 is back-calculated from the HBM die penalty. Micron's own claims (+40%, +35%, +30% per node) would imply higher values. I discounted them because company figures usually quote array or best-product density.
- **A-p1-cost-12** [p1-cost] 24Gb and 32Gb DDR5 dies scale linearly with capacity at the same density; the 32Gb part gets a small array-efficiency gain (0.40 Gb/mm²). — basis: judgment.
- **A-p1-cost-13** [p1-cost] LPDDR5X density is about the same as DDR5 on the same node. — basis: PK.
- **A-p1-cost-14** [p1-cost] HBM3E 24Gb core die is about 110 mm² (95–125); HBM4 core die is about 125 mm² (110–140). An HBM die is about 1.40× a DDR5 die of the same capacity on the same node, and its yield is 20–30% lower. — basis: TrendForce 2024 note recalled from PK; Micron's ~3:1 trade ratio (REPORTED via p1-market snippet).
- **A-p1-cost-15** [p1-cost] Mature DRAM die yield after repair is 0.90 (0.85–0.95). Ramp yield is 0.60 (0.30–0.80). 1γ/1c in 2026 yields 0.80. A 12-high HBM3E stack yields 0.75 (0.60–0.90). — basis: industry heuristic and SK hynix's "nearly 80%" HBM3E remark (FT, 2024-05; PK).
- **A-p1-cost-16** [p1-cost] Edge exclusion is 3 mm (2–5) and the scribe lane 80 µm (60–200). — basis: PK for memory fabs; Chiplet Actuary uses 5 mm and 200 µm (VERIFIED) as conservative values.
- **A-p1-cost-17** [p1-cost] Legacy die sizes (DDR4 8Gb: 20nm 80, 1x 55, 1y 45, 1z 39 mm²; DDR3 4Gb: 25nm 60, 3x-nm 80 mm²; DDR3 2Gb 38nm 50 mm²) are estimates from typical node densities and are not teardown-verified. — basis: PK.
- **A-p1-cost-18** [p1-cost] Back-end per DDR5 16Gb component is about $0.45 ($0.30–0.75): probe $0.10, FBGA assembly $0.18, final test and burn-in $0.17. That is about $0.225/GB. — basis: judgment that back-end is roughly 10–15% of COGS at trough prices.
- **A-p1-cost-19** [p1-cost] The TSV process adds about $650 per wafer (450–1,000). HBM stacking and test cost about $25 per 12-high stack (15–45). Base die: HBM3E $15, HBM4 $35 (logic process). — basis: judgment and PK.
- **A-p1-cost-20** [p1-cost] 64GB RDIMM non-DRAM BOM: RCD $7, PMIC $3.5, SPD hub $0.7, 2 temperature sensors $0.35 each, PCB $4, passives $1.2. Total $17.1. Assembly and test cost $3.5 in Asia and about $12 in the U.S. (p1-backend). — basis: PK; p1-backend used about $25 for parts at U.S. low-volume pricing.
- **A-p1-cost-21** [p1-cost] Module yield is 98.5%. — basis: judgment.
- **A-p1-cost-22** [p1-cost] A chip-level DDR5 16Gb contract price is not public. I back it out from 64GB RDIMM contract prices of $900–1,586 (base $1,250) minus about $20 of non-DRAM cost, divided by 40 devices. That gives about $30 per chip (22–39). — basis: Counterpoint via p1-market; Citi forecast UNVERIFIED.
- **A-p1-cost-23** [p1-cost] DDR5 16Gb spot at the 2023 trough was about $3.2 per chip (2.8–3.6). — basis: PK.
- **A-p1-cost-24** [p1-cost] The glut scenario is a 60% decline (mission rule 6). A severe case is an 85–90% decline back to 2023 cost-floor pricing. — basis: mission plus p1-market.
- **A-p1-cost-25** [p1-cost] The 2020-basis foundry wafer prices (TSMC-class: 28nm $2,891 and so on) are taken from the Chiplet Actuary parameter file (VERIFIED as published there). I attribute their origin to CSET's 2020 "AI Chips" report from PK. 2026 adjustments: 28nm $2,600 (1.8–3.2k), 40nm $2,100, 65nm $1,700, N3 $20k, N2 $30k. — basis: PK of the 2024–25 mature-node price war and 2025 advanced-node reports.
- **A-p1-cost-26** [p1-cost] 200mm wafers: 180nm in Asia $700 (450–1,000); 90–130nm in Asia $1,000; SkyWater 130nm $1,400 (shared with p1-fabs, A1 and A2); U.S. 65–90nm $2,000. — basis: PK and cross-agent consistency.
- **A-p1-cost-27** [p1-cost] Embedded NVM mask adders: eMRAM +4 masks (3–5) for about +$800 per wafer; eFlash +11 (9–14); RRAM +2 (1–3) for about +$250; CBRAM +1 (GF, REPORTED); FRAM +2 (TI 130nm, REPORTED). — basis: PK plus A1/A2 cross-references.
- **A-p1-cost-28** [p1-cost] SRAM silicon $/GB assumes 60% macro array efficiency and 92% usable wafer area, and excludes test and packaging. — basis: judgment. Small macros are far worse (GF180 4-kbit macro is about 20 kbit/mm², VERIFIED).
- **A-p1-cost-29** [p1-cost] NAND TLC costs $0.025/GB at the 2023 trough and $0.09/GB in 2026 (0.06–0.15). NOR costs about $40/GB (20–70). — basis: PK plus p1-market's NAND compounding.
- **A-p1-cost-30** [p1-cost] An oxide-TFT backplane costs about $50/m² ($25–110), or $275 per Gen-8.5 sheet ($140–600). A1 used $500 per sheet. — basis: PK that the array is 20–30% of LCD panel cost. No U.S. line exists.

</details>

<details><summary><b>p1-fabs</b> (22)</summary>

- **A-p1-fabs-1** [p1-fabs] My first WebSearch call returned "budget used up" (the 200-search limit per turn is shared by every agent, and other agents had used it all). WebFetch to www.everspin.com and www.skywatertechnology.com failed with "host not in allowed network domains". The proxy log also shows trendforce.com, sec.gov and investors.micron.com refused. Following the tool instructions, I stopped trying other sites. Everything in `phase1/us_fabs.md` therefore comes from one of two places: (a) snippets other agents logged (A1, A2, p1-micron), cross-referenced in `sources/p1-fabs.jsonl` and tagged so; or (b) my prior knowledge (training data through about mid-2026), tagged [UNVERIFIED]. — basis: tool error messages; proxy status `recentRelayFailures`.
- **A-p1-fabs-2** [p1-fabs] I logged URLs from other agents' logs in my jsonl with an explicit "CROSS-REFERENCE … p1-fabs did not independently open" note. I did this rather than leave them unlogged, so the merge tool can trace every URL my note cites. I added no URL that does not already appear in another agent's log. — basis: CONVENTIONS "never invent a URL" plus "log every source you rely on". This was the most transparent way to satisfy both.
- **A-p1-fabs-3** [p1-fabs] Where my prior-knowledge facts have no logged URL, I name the source document and date in prose with no link, and tag the fact [UNVERIFIED]. — basis: never invent URLs.
- **A-p1-fabs-4** [p1-fabs] I tag a snippet of a primary filing seen by another agent [REPORTED-P], matching the p1-micron convention. Nothing in this note is [VERIFIED], because no primary page was opened. — basis: CONVENTIONS tag definitions.
- **A-p1-fabs-5** [p1-fabs] GF's U.S. fabs (Malta Fab 8 at 12/14nm; Essex Junction Fab 9 at 90–350nm, 200mm) run no eMRAM or eReRAM in volume production. GF's eMRAM is on 22FDX in Dresden. — basis: prior knowledge, plus the A2 snippet that AutoPro150 eMRAM is produced at Dresden. Confidence ~75%.
- **A-p1-fabs-6** [p1-fabs] GF's 14HP (IBM-derived 14nm FinFET-on-SOI with deep-trench eDRAM) was built at Malta for IBM z15/POWER9. Whether it is still offered in 2026 is unknown. — basis: prior knowledge. Confidence that it existed is ~85%; that it is still running in 2026, ~40%.
- **A-p1-fabs-7** [p1-fabs] Everspin's Chandler line processes 200mm wafers only. Its STT-MRAM products (256Mb on 40nm, 1Gb on 28nm, xSPI family) are made front to back at GF Singapore (300mm), not in the U.S. — basis: A2 snippet of the FY2025 10-K; my prior knowledge for the 200mm-only detail. Confidence ~80%.
- **A-p1-fabs-8** [p1-fabs] SkyWater Bloomington holds DMEA Trusted Foundry accreditation (Category 1A, since ~2017) and is open to commercial customers. — basis: prior knowledge. Confidence ~90%.
- **A-p1-fabs-9** [p1-fabs] SkyWater Fab 25 (Austin) inherits Cypress/Infineon 65nm-class CMOS and SONOS embedded-NVM know-how. Whether SONOS is offered to foundry customers is unknown. — basis: prior knowledge of Cypress PSoC/SONOS at Fab 25. Confidence ~50% on the SONOS-as-foundry-offering point.
- **A-p1-fabs-10** [p1-fabs] TI runs no external foundry business. Its embedded FRAM (MSP430FR) and the Weebit ReRAM license are captive. — basis: prior knowledge plus the A2 snippet. Confidence ~90%.
- **A-p1-fabs-11** [p1-fabs] Polar Semiconductor is becoming a U.S.-owned commercial 200mm foundry for power and sensors, with ~$123M of CHIPS support and ~$175M of private equity (2024). — basis: prior knowledge. Confidence ~70% on the exact figures.
- **A-p1-fabs-12** [p1-fabs] Intel does not offer eMRAM or eReRAM to external foundry customers on Intel 16, Intel 3 or 18A, despite its 22FFL eMRAM/ReRAM ISSCC 2019 papers. — basis: prior knowledge; no public external offering seen. Confidence ~65%.
- **A-p1-fabs-13** [p1-fabs] No Gen-4-or-larger LCD, OLED or oxide-TFT panel fab operates in the U.S. as of 2026-11. — basis: prior knowledge (Foxconn Wisconsin Gen 10.5 never built) plus the A1 snippet that TrendForce TFT-capacity data shows no U.S. fabs. Confidence ~95%.
- **A-p1-fabs-14** [p1-fabs] The Twin Cities hold an unusual concentration of magnetic thin-film/MTJ wafer capability: Seagate Bloomington head-wafer fab, NVE Eden Prairie, Honeywell Plymouth, SkyWater and Polar. None of them offers MTJ foundry service to outsiders. — basis: prior knowledge. Confidence ~70%.
- **A-p1-fabs-15** [p1-fabs] Processed-wafer prices: 200mm 130–180nm foundry ≈ $900–1,600; 200mm 65–90nm ≈ $1,500–2,500; 300mm 22FDX ≈ $3,500–4,500; 300mm 12/14nm ≈ $4,000–6,000; Intel 18A not public. — basis: public foundry price lore, consistent with A1 ($1,200 for 200mm 130nm) and A2 ($1,400–1,600 for SkyWater S130 + ReRAM, $4,500 for 22FDX + eMRAM). ±30–50%.
- **A-p1-fabs-16** [p1-fabs] MPW/shuttle costs: SkyWater 130nm open-source-style shuttle ≈ $10–15k per ~10 mm² slot; commercial 130nm MPW ≈ $1–3k/mm² with a minimum of ~$15–40k; 22FDX MPW ≈ $10–25k/mm²; full 130nm mask set $500–600k (A1/AnySilicon snippet). — basis: pre-2026 shuttle price lore plus the A1-logged snippets. ±50%.
- **A-p1-fabs-17** [p1-fabs] University nanofab external rates: industrial users ≈ $75–250 per tool-hour plus ~$100–200 per staff-hour; academic users ≈ $30–90 per hour. A device-level IGZO or HZO learning program (3–6 months) ≈ $20–80k. — basis: memory of typical NNCI rate sheets; not re-verified for 2026.
- **A-p1-fabs-18** [p1-fabs] A minimal 200mm IGZO BEOL tool set (refurbished: oxide-target PVD, PECVD, ALD, anneal, ICP etch, wet bench, parametric test), dropped into an existing cleanroom, costs ≈ $4–10M in tools plus fit-out. That is tier T2. — basis: used-tool market lore. ±50%.
- **A-p1-fabs-19** [p1-fabs] Planar IGZO 2T0C cell = 20–40 F² with array efficiency 60%. At F = 130nm that is 0.9–1.8 Mb/mm² per tier, 250–490× less dense than DDR5 1b (0.436 Gb/mm², A1 basis). At F = 65nm it is 60–120× less dense. — basis: computed in scratch (igzo_density.py, not a deliverable). Cell size is an assumption.
- **A-p1-fabs-20** [p1-fabs] "Memory-relevant" here means the fab could make standalone or embedded memory (DRAM, SRAM, MRAM, ReRAM, CBRAM, FeRAM/FeFET, SONOS/flash, PCM, IGZO) or host a BEOL memory module. Pure SiC, GaN or GaAs fabs are listed only for completeness, as idle-capacity candidates.
- **A-p1-fabs-21** [p1-fabs] I treat the Everspin–Microchip exclusivity clause (A2 snippet) as closing Gresham Fab 4 to any third-party MTJ startup.
- **A-p1-fabs-22** [p1-fabs] I treat the §48D 35% ITC as practically unavailable to a new founder-led BEOL line, because construction must begin by 2026-12-31 (p1-micron), which is 2 months away.

</details>

<details><summary><b>p1-funding</b> (21)</summary>

- **A-p1-funding-1** [p1-funding] CHIPS manufacturing incentives ($39B) are effectively unavailable to a new small entrant in 2026–2028; model $0 CHIPS grant for every concept — basis: nearly all funds committed by Jan 2025, program moved under the U.S. Investment Accelerator (EO 2025-03-31) with renegotiation/equity-for-funding pattern (Intel Aug 2025); no open NOFO known (prior knowledge, conf. medium-high).
- **A-p1-funding-2** [p1-funding] Model 0% §48D ITC for all concepts — basis: 35% rate applies only if construction begins by 2026-12-31 (60 days from today); no concept is at that stage; BASIC Act extension not enacted (p1-micron cross-ref: Baker Tilly, Instead, Congress.gov).
- **A-p1-funding-3** [p1-funding] Treat NSTC funding, membership and facilities as unavailable until a 2026 operating model is confirmed — basis: Commerce voided Natcast operator agreement Aug 2025, NIST took control (prior knowledge, conf. medium).
- **A-p1-funding-4** [p1-funding] SBIR/STTR authority was restored by mid-2026 after lapsing 2025-10-01 — basis: inference from DoD SBIR topic DPA26BZ04-DV017 opening 2026-07-22 (A1 cross-ref); reauthorization terms unknown (conf. medium).
- **A-p1-funding-5** [p1-funding] The founder cannot serve as SBIR PI while keeping a full-time day job; STTR (university PI) or a hired full-time PI is required — basis: SBA SBIR/STTR Policy Directive primary-employment rule (>50% time with awardee) (prior knowledge, conf. high).
- **A-p1-funding-6** [p1-funding] SBIR award sizes for modelling: Phase I $150k–$315k; Phase II $1.0M–$2.1M; DoD Direct-to-Phase II ~$1.2M — basis: SBA guideline caps (prior knowledge, conf. low-medium) and DARPA DV017 ~$1.2M (A1 cross-ref via BWCO).
- **A-p1-funding-7** [p1-funding] SBIR Phase III sole-source production awards are the mechanism that can turn SBIR work into revenue (not grant farming) — basis: SBIR statute/Policy Directive (prior knowledge, conf. high).
- **A-p1-funding-8** [p1-funding] No general "U.S.-made memory" premium exists in federal procurement; price any U.S.-origin premium at $0 today — basis: TAA treats Korea/Taiwan/Japan as designated countries; BAA COTS waiver of component test; memory outside Section 232 phase 1 (p1-micron cross-ref) (prior knowledge, conf. high for TAA/BAA structure).
- **A-p1-funding-9** [p1-funding] NDAA FY2023 §5949 takes effect 2027-12-23 (5 years after 2022-12-23 enactment) and covers products containing SMIC, YMTC, CXMT semiconductors — basis: statute (prior knowledge, conf. high); "Dec 2027" corroborated by p1-micron cross-ref (XenoSpectrum).
- **A-p1-funding-10** [p1-funding] §5949 rewards "verified non-Chinese" memory, not "U.S.-made" memory; Korean/Taiwanese parts satisfy it — basis: statutory coverage is entity-based (judgment).
- **A-p1-funding-11** [p1-funding] CMMC Phase 2 (Level 2 C3PAO in solicitations) begins ~2026-11-10 — basis: DFARS CMMC rule effective ~2025-11-10 with one-year phase steps (prior knowledge, conf. medium).
- **A-p1-funding-12** [p1-funding] CMMC Level 2 first-year cost for a small firm ≈ $30k–$100k+; export-control compliance program for a rad-hard product ≈ $25k–$75k/yr — basis: judgment from typical small-business quotes; unsourced this session (conf. low).
- **A-p1-funding-13** [p1-funding] BIS "affiliates" (50%) rule was suspended for one year from ~2025-11-10 and may resume ~2026-11-10 — basis: prior knowledge of Nov 2025 U.S.–China truce (conf. medium); rule existence corroborated by p1-micron cross-ref (Simpson Thacher).
- **A-p1-funding-14** [p1-funding] CXMT is not on the BIS Entity List as of mid-2026 — basis: p1-micron cross-ref (TrendForce 2025-05-16; Schumer 2025-05-15; 2026 reporting) with conflicting reports noted.
- **A-p1-funding-15** [p1-funding] Dec 2024 BIS DRAM "advanced-node" metric: cell area <0.0019 µm² or density >0.288 Gb/mm²; HBM under 3A090.c at >2 GB/s/mm² bandwidth density — basis: prior knowledge of 89 FR 96790 (conf. medium).
- **A-p1-funding-16** [p1-funding] USML XV(d) five-parameter rad-hard threshold and 3A001.a.1 thresholds (5×10^3 Gy(Si) TID; 5×10^6 Gy(Si)/s dose-rate; 5×10^13 n/cm²) as stated in §11.3 — basis: prior knowledge of 22 CFR 121 / 15 CFR 774 (conf. medium); 9A515.d/.e thresholds not stated (conf. low).
- **A-p1-funding-17** [p1-funding] Microelectronics Commons sub-award slices to small team members are ~$0.1–2M per project — basis: judgment from ~$269M/33 projects (Sept 2024) average ~$8M per project split across teams (prior knowledge, conf. low).
- **A-p1-funding-18** [p1-funding] State programs accessible to a small company are SBIR-matching or job-based ($10k–$500k), not megaproject incentives (NY Green CHIPS, TX TSIF, OH JobsOhio) — basis: program design (prior knowledge, conf. medium); Micron NY $5.5B corroborated via p1-micron cross-ref.
- **A-p1-funding-19** [p1-funding] Micron is not a DMEA-accredited trusted supplier, so no trusted-accredited U.S. DRAM wafer source exists — basis: prior knowledge, conf. low; must verify on the DMEA list.
- **A-p1-funding-20** [p1-funding] Duty on imported used/recovered China-origin DRAM follows country of diffusion, so the 50% Section 301 China semiconductor duty applies — basis: CBP diffusion-origin practice for ICs (prior knowledge, conf. medium) + p1-micron cross-ref on the 50% duty.
- **A-p1-funding-21** [p1-funding] The Sandia HZO FeRAM integrated in MESA (2026-05-13) is potentially licensable/CRADA-able — basis: A1 cross-ref; licensing availability unknown (judgment).

</details>

<details><summary><b>p1-ip</b> (25)</summary>

- **A-p1-ip-1** [p1-ip] No live web evidence was gathered by this agent. My first WebSearch call returned "budget used up" (200-call per-turn cap shared by all agents). WebFetch failed DNS for every host tried (neosemitech.com, patents.google.com, en.wikipedia.org, techfinder.stanford.edu). Per the tool instructions I did not route around either block with curl/wget or third-party readers — basis: tool error messages, 2026-11-01.
- **A-p1-ip-2** [p1-ip] The evidence base is therefore (a) URLs other agents saw in search results (A1, A2, A3, B, p1-*), logged in `sources/p1-ip.jsonl` as CROSS-REFERENCE and tagged [REPORTED] at best; and (b) my training knowledge, tagged [UNVERIFIED-training] and not re-checked. No fact in `ip_landscape.md` is [VERIFIED] by me — basis: CONVENTIONS.md tag definitions.
- **A-p1-ip-3** [p1-ip] I cite patent numbers from memory only where I am fairly confident (Slonczewski US 5,695,864; Savtchenko US 6,545,906; Kozicki US 5,761,115; Ramtron/Eaton US 4,873,664; Nemati/Plummer US 6,229,161; Netlist US 7,619,912, US 11,016,918, US 11,232,054). All carry [UNVERIFIED-training] and sit in the verification queue. I gave no patent numbers for university dockets, because none could be retrieved — basis: no portal access.
- **A-p1-ip-4** [p1-ip] No URL in the deliverable was typed from memory. Every URL comes from another agent's log. Portals are named but not linked — basis: CONVENTIONS "Never invent a URL".
- **A-p1-ip-5** [p1-ip] Expiry estimate = 20 years from the earliest non-provisional US filing or PCT date. For filings before 1995-06-08: the later of 17 years from grant or 20 years from filing. Patent-term adjustment, terminal disclaimers and maintenance-fee lapses are ignored, so real expiry can be earlier (lapse) or later (PTA, typically 0–3 years) — basis: 35 U.S.C. §154 [UNVERIFIED-training].
- **A-p1-ip-6** [p1-ip] "Expired basics" means only the foundational concept claims are free. Improvement, integration and manufacturing patents filed 2006–2026 are assumed live and held by incumbents. This is why "expired basics" never scores as freedom-to-operate (FTO) — basis: standard patent practice; e.g., SEL's continuing CAAC-IGZO/DOSRAM filings in cross-ref sources.
- **A-p1-ip-7** [p1-ip] The HfO₂ ferroelectric base filing is assumed to have ~2007–2008 priority (Qimonda Dresden discovery 2007, published 2011). Estimated expiry ~2027–2028. The current owner is unverified (Qimonda insolvency estate; FMC/NaMLab licensing status unknown) — basis: training knowledge.
- **A-p1-ip-8** [p1-ip] The a-IGZO TFT base filings (JST/Hosono) are assumed to have 2003–2005 priority, so expiry ran ~2023–2025 — basis: Nomura et al., Nature 2004 timing [UNVERIFIED-training].
- **A-p1-ip-9** [p1-ip] Toggle MRAM (Motorola, filed ~2001) is treated as expired ~2021. The STT concept (IBM/Slonczewski, filed 1995) is treated as expired ~2015. The PMC/CBRAM base (ASU/Axon, filed 1996) is treated as expired ~2016 — basis: 20-year rule on remembered filing years.
- **A-p1-ip-10** [p1-ip] University startup license ranges used in §6.4: option $1k–$10k; issue fee $0–$50k, often deferred; past patent costs $10k–$150k, often deferred; equity 2–10% (≈5% typical); royalty 1–5% of net sales (1–3% typical for semiconductor components); sublicense share 10–50%; annual minimums $5k–$50k — basis: general AUTM-community practice from training. No 2025–26 survey was retrieved [UNVERIFIED-training].
- **A-p1-ip-11** [p1-ip] Deal timing used: option 2–8 weeks; exclusive startup license 2–6 months; national-lab license 3–9 months; CRADA 3–12 months — basis: training-knowledge ranges plus the extra federal approval steps at DOE labs [UNVERIFIED-training / ESTIMATE].
- **A-p1-ip-12** [p1-ip] FTO search plus opinion, one narrow product: $10k–$30k for a scoped search and memo; $30k–$100k for a full opinion — basis: law-firm norms from training [UNVERIFIED-training].
- **A-p1-ip-13** [p1-ip] Defense cost of one NPE patent suit through trial: ~$0.6M–$4M depending on stakes. Typical early settlements for small defendants: $50k–$500k — basis: recalled AIPLA economic-survey bands [UNVERIFIED-training].
- **A-p1-ip-14** [p1-ip] T0 IP budget computed as option $5k + scoped FTO $15k + provisional filings on own improvements $5k = $25k, i.e. ~half of the founder's <$50k — basis: midpoints of the ranges above [ESTIMATE].
- **A-p1-ip-15** [p1-ip] USPTO large-entity maintenance fees after the Jan-2025 fee rule: ~$2,150 / $4,040 / $8,280 at 3.5 / 7.5 / 11.5 years. Small entity pays 40% of these and micro entity 20% — basis: training knowledge [UNVERIFIED-training].
- **A-p1-ip-16** [p1-ip] "Closed" means no licensing program exists and no license to a non-IDM startup has been seen (Samsung, SK hynix, Micron, Kioxia, TSMC, Intel XPoint, ST ePCM, GF CBRAM). "Likely" means a licensing business or a tech-transfer office exists and has licensed to small firms before. "Open" means a published license (BSD/Apache) or a PDK-integrated commercial IP — basis: author definition.
- **A-p1-ip-17** [p1-ip] NEO Semiconductor and FMC are scored "closed to this founder". Both license only to fab-owning memory makers or foundries — basis: cross-ref sources (A1: NEO licenses to memory makers; eeNews 2017: FMC "ARM of memories" model aimed at foundries/IDMs).
- **A-p1-ip-18** [p1-ip] Everspin is scored "likely, but at defense-prime scale". The $40M Amentum process-transfer subcontract (Apr-2026) proves Everspin will license process tech. It does not show terms a <$2M company could meet — basis: cross-ref electronics360/MRAM-Info.
- **A-p1-ip-19** [p1-ip] Weebit ReRAM is scored "open" for a fabless U.S. startup through the SkyWater S130 PDK. Weebit's royalty/license terms for small fabless users are unknown and flagged — basis: cross-ref Weebit/SkyWater releases 2023.
- **A-p1-ip-20** [p1-ip] Sandia HZO FeRAM is scored "likely" via license plus CRADA. Its availability on Sandia's licensing portal is unverified — basis: cross-ref Sandia news 2026-05-13 plus DOE tech-transfer norms.
- **A-p1-ip-21** [p1-ip] The status of Nantero, Spin Memory's IP, Antaios, T-RAM's IP, Panasonic ReRAM and Kepler Computing is treated as UNKNOWN. None is used as a positive lead without verification — basis: no access.
- **A-p1-ip-22** [p1-ip] Litigation-risk grades: HIGH means an active suit or verdict in 2023–2026 directly on the product class. MEDIUM means a dense incumbent estate with an assertion history in adjacent products. LOW means no assertions seen and the estate mostly expired or held by non-practicing universities — basis: author definition.
- **A-p1-ip-23** [p1-ip] Netlist verdict amounts ($303M Samsung 2023-04; $445M Micron 2024-05; $118M Samsung 2024-11) are taken from training knowledge and match p1-backend's [UNVERIFIED: PK] figures. The 2025–26 appellate/PTAB outcomes are UNKNOWN — basis: no access.
- **A-p1-ip-24** [p1-ip] Bayh-Dole §204 (U.S.-manufacture preference for exclusive licensees) and DOE's 2021 Determination of Exceptional Circumstances (U.S. substantial manufacture for DOE-funded inventions) are assumed to still be in force as of 2026-11 [UNVERIFIED-training].
- **A-p1-ip-25** [p1-ip] I assume the founder will be a licensee (uses IP in a product), not a licensor. Memory-IP licensing businesses take 5–10 years to modest revenue (Weebit ~10 years to ≥A$13.5M FY26 guidance; FMC 9 years without a product). That is incompatible with the 18-month revenue target — basis: cross-ref A2/A1 sources.

</details>

<details><summary><b>p1-market</b> (15)</summary>

- **A-p1-market-1** [p1-market] All facts in `phase1/market.md` come from web-search result snippets. WebFetch could not resolve trendforce.com, technews.tw or koreatimes.co.kr from this session, and the shared web-search budget ran out after about 46 searches. So no primary page was opened, and no fact gets a tag higher than [REPORTED]. A snippet of a primary release (TrendForce press center, SEC EDGAR, company newsroom) is marked "primary-source snippet". — basis: session tool limits (WebFetch DNS failure; "web search budget is used up" message).
- **A-p1-market-2** [p1-market] Quarterly TrendForce ranges are reduced to their midpoint when compounded (for example, +93–98% is used as +95.5%). — basis: standard practice; TrendForce publishes ranges only.
- **A-p1-market-3** [p1-market] Unless I found a later "actual" figure, the TrendForce *forecast* for 2Q26, 3Q26 and 4Q26 stands in for the realized change. Only 4Q25 (+45–50%) and 1Q26 (+93–98%) have confirmed retrospective figures. — basis: TrendForce press releases of 2026-02-26 and 2026-06-01. The 2Q26 forecast is consistent with 2Q26 industry revenue +59.5% QoQ.
- **A-p1-market-4** [p1-market] "Late 2025" in mission §1 bullet 1 means the 4Q25 contract level, and "through 2026" means the 4Q26 forecast level. I also show a 3Q25 base. — basis: plain reading of the premise.
- **A-p1-market-5** [p1-market] Chip-to-$/GB conversion: 8Gb = 1 GB, 16Gb = 2 GB, 1 Gb = 0.125 GB, so $/Gb × 8 = $/GB. Module $/GB = module price / module GB. — basis: definition.
- **A-p1-market-6** [p1-market] DRAMeXchange "session average" spot quotes are treated as indicative of small-lot spot trading, not of the contract prices that OEMs and hyperscalers pay. The 2026 spot quotes sit above retail $/GB (DDR5 spot ~$27–28/GB vs retail kits ~$13–18/GB), which marks spot as a thin, panic-priced market. — basis: comparison of BuySellRAM/DRAMeXchange 2026-08-31 snapshot vs. rampricesusa Sep-2026 and retail kit prices.
- **A-p1-market-7** [p1-market] The two DDR4 8Gb spot series ($16–21 on TrendForce's board in Jun–Aug 2026, vs. $42–44 per Mobius/BuySellRAM in Jul–Aug 2026) are assumed to be different DRAMeXchange line items, probably eTT/generic vs. branded 3200. Neither is treated as authoritative. — basis: the values cannot be reconciled otherwise, and the snippets do not label the variant.
- **A-p1-market-8** [p1-market] SK hynix margins for 3Q25, 4Q25 and 1Q26 (47%, 58%, 72%) come from a tracker quoted in a search summary. I could not identify which result page the tracker was on, so they are [REPORTED, attribution uncertain]. 2Q26 (76.3%) and 3Q26 (~79.7–80%) come from the company release via news. — basis: search snippets.
- **A-p1-market-9** [p1-market] Micron operating margin for FQ4-26 (~83%) and the FQ1-27 guide (~83%) are my own estimates from reported non-GAAP gross margin minus reported or guided opex. Micron's FQ3-26 operating margin of 81.2% is as quoted in Korean press. — basis: arithmetic in scratch calc; [ESTIMATE].
- **A-p1-market-10** [p1-market] Samsung DS operating margin (72.4%, 3Q26) = DS OP KRW106.5T / DS revenue KRW147.1T. DS includes foundry and System LSI, so the memory-only margin is higher. — basis: Samsung 3Q26 release (via snippet).
- **A-p1-market-11** [p1-market] Glut test: "DDR5 falls 60%" is taken as 60% below the late-2026 peak contract/spot level, not below the 2025 level. — basis: mission §2 rule 6 wording ("DDR5 falls 60%").
- **A-p1-market-12** [p1-market] HBM3E 2026 price ≈ $1.50/Gb and HBM4 2027 ask "mid-to-high $4/Gb" (I use $4.5–4.9/Gb) are reported *asking or negotiated* prices, not confirmed transaction prices. — basis: Korean press (Oct 2026) via snippets.
- **A-p1-market-13** [p1-market] Mobius Materials' "DRAM Market Report" is assumed to be free (possibly email-gated) content marketing for its marketplace, not a paid subscription. I found no price for it. — basis: it is hosted under /whitepapers/ on a marketplace site; no pricing found; [UNVERIFIED].
- **A-p1-market-14** [p1-market] The 2018–19 peak-to-trough is measured on TrendForce's 8GB PC module contract average ($68 in 3Q18 → $25.50 in Aug 2019, −62.5%), because I could not retrieve the 2018 chip-level contract peak. — basis: TrendForce 2018 release and DigiTimes 2019 (via snippets).
- **A-p1-market-15** [p1-market] For the 2022–23 trough I have only the DDR4 8Gb fixed-price bottom ($1.30, Sep 2023). The ~2021 peak (~$3.4–3.9) is from my training memory and is tagged [UNVERIFIED]. — basis: no 2021 peak figure was retrieved before the search budget ran out.

</details>

<details><summary><b>p1-micron</b> (19)</summary>

- **A-p1-micron-1** [p1-micron] Snippets of Micron's FY2026 10-K (period ended 2026-09-03) quoted in search results are accurate to the filing. — basis: several independent searches returned the same quoted sentences (ID1 mid-CY2027, ID2 late CY2028, NY initial wafer output CY2030, CHIPS up to $6.1B unchanged).
- **A-p1-micron-2** [p1-micron] When the 10-K conflicts with press coverage (e.g., a NY "operations Q1 2029" figure), the 10-K wins. — basis: it is the most recent primary disclosure (filed ~Oct 2026).
- **A-p1-micron-3** [p1-micron] "First wafer output" ≠ meaningful supply. Volume qualified output from ID1 is assumed for 2028. — basis: a Micron marketing VP quoted by OC3D (2026); fab ramps typically take 12–18 months from first wafer to high-volume production.
- **A-p1-micron-4** [p1-micron] Total Micron CHIPS direct funding = $6.165B (ID/NY, final 2024-12-10) + $275M (Manassas, final June 2025) ≈ $6.44B. — basis: NIST/Commerce award announcements and Micron's June 2025 release, both via snippet. I found no reduction or equity conversion (unlike Intel's 2025 deal). Absence of evidence is not proof.
- **A-p1-micron-5** [p1-micron] Micron's global DRAM bit share is 22–26% in 2026. — basis: historical TrendForce/Counterpoint ranges (Micron about 20–25%). Not re-verified this session because the search budget ran out.
- **A-p1-micron-6** [p1-micron] Manassas = 3–8% of Micron's DRAM bit output in 2026. — basis: TrendForce says DDR4 is ~7% of Micron output in 2026 after the line transfer to Fab 6 (Manassas). Manassas also runs LP4. Older nodes yield fewer bits per wafer. This is a bounding assumption, not a measured value.
- **A-p1-micron-7** [p1-micron] The U.S. supplies 15–35% of Micron's DRAM bits in 2030 (ID1 ramped, ID2 ramping, NY1 at initial output, Manassas). — basis: company timelines. Micron's 40% U.S. goal is "long-term" and tied to the >$250B plan through 2035, so 2030 sits below 40%.
- **A-p1-micron-8** [p1-micron] The Boise R&D fab's output is negligible for national share. — basis: it is a development fab. Judgment call.
- **A-p1-micron-9** [p1-micron] 48D (35%) illustration: I assume $50–150B of 48D-qualifying property placed in service across ID1/ID2/NY1 over the decade. — basis: the $200–250B plan includes about $50B of R&D, which does not qualify, plus buildings and land. This is an order-of-magnitude illustration only.
- **A-p1-micron-10** [p1-micron] The 48D begin-construction deadline is 2026-12-31 and was not extended as of the latest snippets (Mar 2026). — basis: Baker Tilly, Instead and BASIC Act status. If Congress extends it after my sources, the conclusions on NY fabs 2–4 and on new entrants change.
- **A-p1-micron-11** [p1-micron] Memory ICs (HTS 8542.32) and memory modules (8473.30) are not subject to the Phase-1 Section 232 duty in practice. — basis: Phase-1 scope requires TPP plus DRAM-bandwidth thresholds tied to a logic IC (FedEx/White & Case), and Korea's trade minister said memory is excluded. The "+25%" footnote in HTS Rev. 11 is a Chapter-99 cross-reference, not a blanket duty.
- **A-p1-micron-12** [p1-micron] Under the 2025 IEEPA "reciprocal" regime, semiconductors (8542) and computer parts including memory modules (8473.30) and SSDs were exempt (Annex II, then CBP guidance of April 2025). — basis: prior knowledge, not re-verified this session.
- **A-p1-micron-13** [p1-micron] The Section 301 forced-labor tariffs in force since 2026-07-24 (10–12.5%) may or may not exempt memory. — basis: snippets say only that goods under Section 232 are excluded. Memory-specific treatment was not found, so it is flagged [UNVERIFIED].
- **A-p1-micron-14** [p1-micron] China-origin DRAM (8542.32) carries a 50% Section 301 duty. — basis: the 2024 four-year-review increase on Chinese semiconductors (prior knowledge) plus a tariff aggregator snippet showing 9903.91.05 +50%.
- **A-p1-micron-15** [p1-micron] SK hynix Indiana CHIPS award = up to $458M in grants plus up to $500M in loans (finalized Dec 2024). — basis: prior knowledge. Not re-verified this session because the search budget ran out. Tagged [UNVERIFIED].
- **A-p1-micron-16** [p1-micron] Kioxia, SanDisk, Western Digital, Solidigm, Nanya and Winbond have no U.S. memory wafer fabs. They have only U.S. HQs or sales offices. — basis: prior knowledge plus the absence of any U.S. fab in 2026 search coverage. Lutnick-era reporting says Micron is the only company producing or planning DRAM in the U.S.
- **A-p1-micron-17** [p1-micron] Micron HBM share in Q2 2026 is about 17%. — basis: subtraction from Counterpoint figures (SK hynix 50%, Samsung 33%) quoted in a SammyFans snippet. If a fourth supplier or rounding matters, the value is ±3 pts.
- **A-p1-micron-18** [p1-micron] Micron FY2025 revenue = $37.38B, used to check the reported +256% FY2026 growth (133.2/37.38 = 3.56x). — basis: prior knowledge. The check is internally consistent.
- **A-p1-micron-19** [p1-micron] Micron does not run an open, catalog-based bare-DRAM-die (KGD) program for small third parties in 2026. The realistic Micron-silicon die path is SpecTek (wafers, consumer grade) or a direct strategic agreement. — basis: no current KGD catalog page surfaced, the FY2026 10-K describes supply-allocation decisions, and SpecTek's support page lists wafers. Judgment call that a founder should test with one email to SpecTek sales.

</details>

<details><summary><b>p1-model</b> (42)</summary>

- **A-p1-model-1** [p1-model] **No first-hand web verification was possible.** WebSearch returned "budget used up": the shared 200-call budget was spent by earlier agents. WebFetch failed with ENOTFOUND for trendforce.com, eetasia.com and buysellram.com. Every market price in the model is therefore REPORTED (an URL another agent saw in a search snippet) or UNVERIFIED. — basis: tool errors in this session, 2026-11-01.
- **A-p1-model-2** [p1-model] **Die yield** is a negative-binomial model (alpha = 10).
- **A-p1-model-3** The effective defect density D0 is calibrated so that each node's reference die (16Gb DDR5, 8Gb DDR4, 4Gb DDR3) hits the stated yield.
- **A-p1-model-4** Larger dies on the same node (24Gb, 32Gb, DDR4 16Gb) and the ±20% die-size sensitivity therefore change yield as well as GDPW.
- **A-p1-model-5** With the 1-beta reference at 0.90 (41 mm²), 24Gb yields 0.854 and 32Gb yields 0.815.
- **A-p1-model-6** [p1-model] **Probe cost** is charged on every gross die, so it is divided by yield. Probe and final test/burn-in cost per die scale with (Gb / reference Gb)^0.5. Package cost is flat per die. — basis: parallel memory ATE amortizes test time sublinearly with density; the FBGA substrate does not depend on bits.
- **A-p1-model-7** [p1-model] **Final-test fallout** for packaged parts is 0.99 (0.97–0.995). — basis: judgment; it adds ~1% to component cost.
- **A-p1-model-8** [p1-model] **Legacy back-end per die** = $0.30 per 8Gb DDR4 die and $0.30 per 4Gb DDR3 die (p1-cost $/GB inputs × GB per die). It is split into probe, package and test in the same proportions as DDR5 (22% / 40% / 38%). — basis: p1-cost inputs; the split is p1-model's judgment.
- **A-p1-model-9** [p1-model] **DDR4 16Gb 1y die = 88 mm²** (range 76–107). — basis: 8Gb 1y (45 mm²) × 1.95, the 16Gb/8Gb area ratio at 1z (76/39). The low end is the 16Gb 1z die; the high end is 8Gb 1x × 1.95.
- **A-p1-model-10** [p1-model] **The DDR4 16Gb depreciated-line case** uses the legacy depreciated wafer ($1,300 cash cost) and a yield of 0.92 referenced to the 55 mm² 8Gb 1x die. — basis: p1-cost §9.
- **A-p1-model-11** [p1-model] **The trailing-node DDR5 case** uses CXMT's 16Gb G4 die (66.99 mm², REPORTED teardown) on a $3,000 DUV-only 1z-class wafer at mature yield (0.90 at its own area). — basis: p1-cost §6.1 1z reference row. CXMT's actual yield is unknown and may be lower.
- **A-p1-model-12** [p1-model] **HBM3E 12-high:**
- **A-p1-model-13** Core die yield 0.80, applied at the 110 mm² core-die area.
- **A-p1-model-14** Stack yield 0.75.
- **A-p1-model-15** Wafer = 1-beta + TSV adder $650.
- **A-p1-model-16** Each core die also carries a KGD probe cost.
- **A-p1-model-17** Base die $15 and stacking $25 make up the "package" column.
- **A-p1-model-18** The 12 core dies use 1-beta wafers; base-die wafer usage is ignored.
- **A-p1-model-19** [p1-model] **The GDPW formula assumes square dies.** Real DRAM dies are rectangular, roughly 1.5–2:1, which costs a few percent of GDPW. This is inside the die-size sensitivity. — basis: the standard formula.
- **A-p1-model-20** [p1-model] **Modules:**
- **A-p1-model-21** RDIMMs carry +25% raw bits for side-band ECC, so a 64GB module holds 80 GB raw.
- **A-p1-model-22** UDIMMs are non-ECC.
- **A-p1-model-23** The module yield of 0.985 applies to the whole module cost (DRAM + BOM + assembly).
- **A-p1-model-24** The 96GB RDIMM and the 48GB UDIMM use 24Gb dies.
- **A-p1-model-25** [p1-model] **The Q4-2026 64GB DDR5 RDIMM contract base is $1,300** (low $1,200, high $1,586).
- **A-p1-model-26** It is built from Counterpoint's "possibly >$1,000 in 2Q26" (EE Times Asia), compounded by TrendForce's 3Q26 (+15.5%) and 4Q26F (+12.5%) conventional-DRAM QoQ midpoints.
- **A-p1-model-27** The high end is Citi's 4Q26F of $1,586, which is UNVERIFIED (underlying page not identified).
- **A-p1-model-28** Compounding from 1Q26's $900 through TrendForce 2Q–4Q gives $1,877. That is printed as an upper cross-check, not used, because server RDIMM pricing apparently rose more slowly than the blended index in 2Q26 ($900 → ~$1,000).
- **A-p1-model-29** Using $1,300 instead of $1,586 makes margins and the glut price slightly conservative.
- **A-p1-model-30** [p1-model] **The DDR5 component contract price (per raw GB)** is backed out of the RDIMM: (module − $20.6 non-DRAM BOM and assembly) / 80 GB = **$15.99/GB**. That is about $32 per 16Gb chip, against p1-cost's derived $30.7. — basis: no chip-level contract price is public outside TrendForce's paywall.
- **A-p1-model-31** [p1-model] **Glut = −60% from the 2026 peak, taken as Q4-2026** (ASSUMPTIONS.md A-05).
- **A-p1-model-32** The rule is applied to both component and module $/GB.
- **A-p1-model-33** The severe case is −90% (the high of `glut_price_decline_fraction`).
- **A-p1-model-34** If the actual peak is 1H27 (p1-market's call: peak 4Q26–2Q27), the glut price would be proportionally higher.
- **A-p1-model-35** [p1-model] **The 2023 trough** is DDR5 16Gb at $3.2/chip ($1.60/GB, UNVERIFIED prior knowledge from p1-cost) and DDR4 8Gb contract at $1.30/GB (REPORTED, KED Global). The 64GB RDIMM trough price is derived as trough chip price × 80 GB plus non-DRAM BOM. — basis: cost_inputs.json.
- **A-p1-model-36** [p1-model] **The Q4-2026 DDR4/DDR3 contract is taken at parity with DDR5 per GB** (ratio 1.0, range 0.8–1.65).
- **A-p1-model-37** No legacy contract level was found.
- **A-p1-model-38** Barclays (Oct 2026, via p1-market) has DDR4 contract rising faster than DDR5 and dearer in some channels.
- **A-p1-model-39** The DDR4/DDR5 spot ratio per GB on 2026-08-31 was 1.65, which sets the high end.
- **A-p1-model-40** [p1-model] **The −60% glut applied to HBM3E is illustrative only.** HBM sells on annual LTAs, and A-05 is defined for DDR5. — basis: market.md §2.5.
- **A-p1-model-41** [p1-model] **UDIMM "market" price** = DDR5 chip contract × GB + client BOM and assembly, a contract-equivalent. U.S. retail ($14–18/GB, Sep 2026) is shown only as a reference. — basis: the inputs hold no PC-module contract series.
- **A-p1-model-42** [p1-model] The ±20% yield sensitivity caps die yield at 0.99, so the upside is asymmetric at mature yield. Wafer cost ±20% also scales the HBM TSV adder. Die size ±20% moves GDPW and the negative-binomial yield together. — basis: task spec ±20%; physical cap.

</details>

<details><summary><b>p1-synth</b> (17)</summary>

- **A-p1-synth-1** [p1-synth] No first-hand verification was possible. WebSearch returned "budget used up" (the shared 200-call budget was spent by earlier agents) on all three attempts, and WebFetch failed DNS for www.placera.se and www.trendforce.com, after which I stopped trying hosts as the tool instructed. 01_LANDSCAPE.md therefore synthesizes only what the Phase 1 notes and the model contain. Every URL in it was copied from a Phase 1 note. Nothing is upgraded to [VERIFIED]. — basis: tool errors this session.
- **A-p1-synth-2** [p1-synth] Where a researcher tagged a fact [REPORTED-P] (a primary filing seen only through a search snippet), I keep that tag. It counts as [REPORTED] under CONVENTIONS. — basis: CONVENTIONS tag definitions; p1-micron usage.
- **A-p1-synth-3** [p1-synth] **Canonical cost and price numbers are the model's** (`models/dram_cost_stack.py`, run 2026-11-01, exit 0): DDR5 16Gb 1-beta component cost $1.64/GB; cash cost $0.84/GB; 64GB RDIMM $154 ($2.41/user-GB); 4Q26 contract $15.99/GB component and $20.31/user-GB RDIMM ($1,300 module); glut $6.40/GB component and $8.12/user-GB; severe glut $1.60/GB. p1-cost's hand calculation ($1.62/GB, $152 RDIMM, $216 HBM stack) differs by 1–2% because the model adds final-test fallout. — basis: Mission rule 9 (numbers computed, not vibed).
- **A-p1-synth-4** [p1-synth] **Glut test line = $6.40/GB DDR5 component (contract-based, −60% from 4Q26)**, not p1-market's $10–12/GB (−60% from the thin, panic-priced Sep-2026 spot of ~$57/chip). The contract-based line is stricter and matches ASSUMPTIONS.md A-05, which is defined on contract $/GB. p1-market's $11.4/GB is kept as the upper bound. — basis: A-05; spot is about 1.7× contract in Aug-2026 (model §6).
- **A-p1-synth-5** [p1-synth] **Severe/trough test = $1.30–1.60/GB** (2023 DDR4 contract floor, REPORTED; 2023 DDR5 spot trough, UNVERIFIED), not p1-market's "$2–4/GB". — basis: the model's severe −90% case lands at $1.60, inside the 2023 band.
- **A-p1-synth-6** [p1-synth] **4Q26 64GB RDIMM contract = $1,300** (model base) rather than Citi's $1,586, which no researcher could trace to a page. — basis: p1-model assumption; Citi figure tagged UNVERIFIED in market.md.
- **A-p1-synth-7** [p1-synth] **1-beta wafer cost: $3.8k for an incumbent, $5.5k for a new entrant or new fab.** A1/A2's $5.5–6.0k is the entrant case, not a contradiction. — basis: cost_stack.md §2.1 recommendation.
- **A-p1-synth-8** [p1-synth] **Timing call: contract prices peak 4Q26–2Q27, plateau through 2027, turn down in 2028; a true glut is 2H28–2029 and only if AI capex slows.** I adopt p1-market's call because Micron, TrendForce, Barclays and UBS put tightness through 2027–28 while Baird (>30% bit growth in 2028), BofA (−10% ASP in 2028) and Bloomberg Intelligence (balance ~4Q27) mark 2028 as the turn. — basis: market.md §7.2.
- **A-p1-synth-9** [p1-synth] **SK hynix Indiana HBM output: plan on 2029** (CEO's "HBM4E from Q3 2029") rather than "2H 2028". **Micron NY1: CY2030** per the 10-K, overriding ConstructConnect's "Q1 2029". — basis: the primary or most senior source wins.
- **A-p1-synth-10** [p1-synth] **4Q26 TrendForce forecast = +10–15% conventional DRAM**; the "~+20% Oct-20 revision" stays UNVERIFIED and is not used. — basis: market.md §3.
- **A-p1-synth-11** [p1-synth] **"Micron is the only manufacturer of memory in the United States"** (Micron's own phrase) is read as "only U.S. DRAM wafer maker". Everspin makes Toggle MRAM in Chandler AZ, Honeywell makes rad-hard SRAM/MRAM in Plymouth MN, and TI makes embedded FRAM captively. — basis: us_fabs.md §1 vs micron_us_makers.md §0.
- **A-p1-synth-12** [p1-synth] **Legacy DDR4 contract price is at parity with DDR5 per GB in the model**, although spot shows a 1.65× DDR4 premium. I flag it as a weak input and do not use DDR4 spot ($44/GB) for any concept's base case. — basis: p1-model assumption; no legacy contract series was found.
- **A-p1-synth-13** [p1-synth] **Premise verdict: intact and stronger on price and margin, but the project should re-aim its search, not its mission.** The "make cheaper RAM in the U.S." reading is closed (no U.S. DRAM foundry, no display fab, no die supply, no U.S.-origin premium, CHIPS/§48D closed). The open reading is "sell supply security, provenance and memory efficiency, plus niche non-volatile parts, and be cash-positive before the 2028 turn". — basis: §1 and §10 of 01_LANDSCAPE.md.
- **A-p1-synth-14** [p1-synth] **The "Made in America" moat is re-scoped to "verified non-Chinese plus trusted/rad-hard".** TAA treats Korean, Taiwanese and Japanese memory as equal to U.S. memory; memory pays 0% under Section 232 Phase 1; only China-origin chips pay 50% (Section 301). — basis: funding_export.md §10; micron_us_makers.md §4.
- **A-p1-synth-15** [p1-synth] **A byte of DRAM saved or supplied is worth ~$16/GB of contract value now and ~$6.4/GB in the glut**, which I use as the value anchor for memory-efficiency and recertification concepts in §10. It is a contract-level number; retail ($14–18/GB) and spot ($27/GB) are higher today. — basis: model §6.
- **A-p1-synth-16** [p1-synth] **The four "malformed" lines in research/sources/p1-model.jsonl are valid JSON whose `url` field is a local repo path** (research/phase1/*.json/.md), not an http URL. merge_sources.py skips them as "(no url)". I left them unchanged: the task allows only JSON-syntax fixes without changing meaning, and CONVENTIONS forbids editing other agents' files. — basis: task instruction; CONVENTIONS "Files and git".
- **A-p1-synth-17** [p1-synth] **Sources logged in p1-synth.jsonl are cross-references**: every URL cited in 01_LANDSCAPE.md appears in at least one Phase 1 note and was logged by the researcher who used it. I log them again with a CROSS-REFERENCE note and the fact I used, and I opened none of them. — basis: CONVENTIONS logging rule; task rule on cited-but-unlogged URLs.

</details>

### Phase 1b — verification

<details><summary><b>p1b-patch</b> (5)</summary>

- **A-p1b-patch-1** [p1b-patch] Phase 1b tally (113 items: 56 confirmed, 28 corrected, 1 refuted, 23 still unverified, 5 new) counts one verdict per verifier-log row. Mixed labels go to the main verdict: "CONFIRMED + CORRECTED" → corrected; "CONFIRMED (X); STILL-UNVERIFIED (Y)" → confirmed; v4 5d "STILL-UNVERIFIED (published); derived CORRECTED" → still unverified; v4 2f "CLARIFIED" → corrected; v3 1d "PASSED" → confirmed — basis: verify_v1..v4 change tables.
- **A-p1b-patch-2** [p1b-patch] Treated the §5949 "reasonable inquiry" standard as moving O1's core product from die-level lab screening to attestation and BOM-traceability workflow, with lab screening as an add-on — basis: verify_v1-policy.md items 1d–1f and note 1.
- **A-p1b-patch-3** [p1b-patch] Moved Weebit-on-S130 entry from T0 to T1 — basis: verify_v2-fabs-ip.md items 1b–1d, 1i and notes 2–3. The fabless-startup fee is unknown, and existing licensees paid an estimated $0.1–2.6M upfront.
- **A-p1b-patch-4** [p1b-patch] Adopted v4-cost's re-run deck as canonical: cost $1.48/GB, contract $20.37/GB, glut $8.15/GB, RDIMM $25.78/$10.31 per user-GB — basis: models/dram_cost_stack.py re-run 2026-11-01, exit 0, output identical to cost_stack_output.md.
- **A-p1b-patch-5** [p1b-patch] Kept the market.md "85–90% fall to the 2023 floor" and added ~92% on the 1b contract deck, i.e. $1.60 / $20.37 — basis: arithmetic.

</details>

### Phase 2 — ideation (devices)

<details><summary><b>A1</b> (22)</summary>

- **A-A1-1** [A1] DDR5 price anchor is ~$27/GB (DRAMeXchange 2026-08-31 DDR5 16Gb avg $53.92, taken from the p1-market source log, contract vs spot label unclear); glut anchor is ~$10.8/GB (A-05, -60%) — basis: p1-market log + A-05.
- **A-A1-2** [A1] DDR5 1b manufacturing cost is ~$2.7/GB (wafer $5,500, 0.436 Gb/mm2, 88% yield, $0.8/GB test+pkg). In a real glut, incumbents can price toward this cost, not just to -60% — basis: scratch model in A1_notes.md; wafer cost unverified (Yole/TechInsights paywalled).
- **A-A1-3** [A1] Processed 1b-class DRAM wafer costs $5,500 (range $5-6K) — basis: industry rule of thumb; no public primary figure found.
- **A-A1-4** [A1] 200mm 130nm-class logic processed wafer costs ~$1,200 (±50%) — basis: no public quote found; Silicon Analysts gives only a node-agnostic $2.5K-20K direct-foundry range; 130nm mask set $500-600K (AnySilicon).
- **A-A1-5** [A1] Each IGZO BEOL tier adds ~4-6 masks and ~$300 per 200mm wafer — basis: device-flow judgment (active, gate, contact, S/D metal, via); no published adder found.
- **A-A1-6** [A1] An HZO FeCAP module adds 2-3 masks (~$200/200mm wafer) — basis: analogy to TI's 2-mask PZT FRAM on 130nm (New Electronics, 2010).
- **A-A1-7** [A1] A planar 2T0C IGZO cell at 130nm design rules is ~30F2 (~0.5 um2) — basis: two-TFT gain cell layout judgment; vertical CAA cells (4-8F2) not demonstrated on 200mm.
- **A-A1-8** [A1] 6T SRAM at 130nm is ~2.0-2.5 um2/bit — basis: textbook/industry value (not re-verified this session).
- **A-A1-9** [A1] Display oxide-TFT design rule is ~2 um, and processed backplane cost is ~$500 per Gen 8.5 sheet — basis: display-industry judgment; unverified.
- **A-A1-10** [A1] 300mm 28nm logic processed wafer costs ~$3,000 — basis: industry rule of thumb; used only for the A1-02 sensitivity row.
- **A-A1-11** [A1] 200+-layer 3D-NAND-class 300mm wafer costs ~$7,000 — basis: rule of thumb; NEO density uses its own '10x' claim (UNVERIFIED).
- **A-A1-12** [A1] Usable wafer area uses 3mm edge exclusion and 90% die-fit efficiency — basis: standard die-per-wafer approximation.
- **A-A1-13** [A1] Yields: mature DRAM 0.88; embedded macro 0.9; new standalone oxide 0.65; PoC-stage tech 0.5 — basis: judgment.
- **A-A1-14** [A1] F-RAM distribution price is ~$1-4/Mbit (=> ~$8-30K/GB) — basis: recollection of distributor pricing; not re-verified this session (search budget exhausted).
- **A-A1-15** [A1] The F-RAM/FeRAM market is ~hundreds of $M per year — basis: judgment; no sourced market size found.
- **A-A1-16** [A1] Qualifying a new oxide BEOL module at a foundry costs ~$10-30M and 3+ years — basis: judgment from typical eNVM qualification programs (e.g., multi-year ReRAM/MRAM foundry quals).
- **A-A1-17** [A1] Silicon DRAM/flash fail well below 300C — basis: general device physics; used to frame A1-07.
- **A-A1-18** [A1] No volume 3D NAND or NAND-class fab operates in the U.S. — basis: training knowledge (Micron NAND in Singapore/Japan; Intel NAND went to SK hynix/Solidigm, Dalian); not re-verified this session.
- **A-A1-19** [A1] SkyWater Bloomington is a DMEA-accredited Trusted Foundry — basis: training knowledge; UNVERIFIED this session.
- **A-A1-20** [A1] GlobalFoundries 22FDX runs mainly in Dresden — basis: training knowledge; UNVERIFIED for a U.S. 22FDX FeFET flow.
- **A-A1-21** [A1] Treat company-reported numbers (NEO PoC, FMC DRAM+ targets, SEL patent retention claims) as [REPORTED], not verified — basis: no independent peer-reviewed data seen.
- **A-A1-22** [A1] Research limits: WebFetch failed for every host tried (domains not allowed in this session), and the shared WebSearch budget ran out after ~37 A1 searches. All facts are therefore "(via search snippet)" at [REPORTED] confidence, even when the underlying source is primary.

</details>

<details><summary><b>A2</b> (18)</summary>

- **A-A2-1** [A2] DDR5 contract price "today" (Q4-2026) ≈ $20/GB; glut (A-05, −60%) ≈ $8/GB — basis: DDR5 16Gb spot avg $53.92 on 2026-08-31 (≈$27/GB, buysellram citing TrendForce) and ≈$2.94/Gb early-July 2026 (Wccftech); contract lags spot in upswing. Phase-1 `models/dram_cost_stack.py` supersedes this when it exists.
- **A-A2-2** [A2] Legacy DDR3/DDR4 4Gb ≈ $3.19/Gb (≈$25.5/GB) spot early-July 2026 — basis: Wccftech/Gizchina citing TrendForce; used only for MRAM-vs-legacy-DRAM ratio.
- **A-A2-3** [A2] Reference DRAM die density for 1b-class DDR5 16Gb = 0.40 Gb/mm² (≈40 mm² die) — basis: [UNVERIFIED: training-data recollection of TechInsights teardowns, ~0.35–0.45 Gb/mm²]; the conclusion (MRAM ~40x less dense) holds anywhere in 0.3–0.5.
- **A-A2-4** [A2] Legacy 2x-nm DDR3/DDR4 4Gb density = 0.12 Gb/mm² — basis: [ESTIMATE: training-data recollection]; only used for reference row.
- **A-A2-5** [A2] Wafer prices (all [ESTIMATE], pre-2026 foundry pricing + module adders): 300mm 28nm logic + MTJ module ≈ $4,300; 300mm 16nm FinFET + MTJ ≈ $6,500; 300mm 22FDX + eMRAM ≈ $4,500; 200mm 130nm (SkyWater S130) + 2-mask ReRAM ≈ $1,600; 200mm Toggle MRAM at Chandler (CMOS + Toggle BEOL, low-volume fab) ≈ $2,500; 300mm 3D XPoint at full loading ≈ $5,500–6,000; 300mm 1b DRAM ≈ $6,000; 300mm N5-class + SOT module ≈ $17,000 — basis: public foundry price lore (28nm ~$3k, 16nm ~$5.5–6k, 5nm ~$16–17k) plus 3–6 extra masks and PVD/IBE steps for MTJ. Accuracy ±30%; conclusions are robust because the gaps are 10–700x.
- **A-A2-6** [A2] Yields: mature MRAM 80%, Toggle 85%, XPoint 70%, DRAM 90%, novel SOT 70% — basis: [ESTIMATE].
- **A-A2-7** [A2] Test+package per die: 1Gb MRAM BGA ≈ $2.50; 16Mb Toggle TSOP ≈ $1.50; DRAM ≈ $1.00 — basis: [ESTIMATE: OSAT lore for small BGA/TSOP plus long NVM retention/endurance test].
- **A-A2-8** [A2] Toggle 16Mb die area ≈ 50 mm² — basis: [UNVERIFIED: no teardown found; 180/130nm 1T1MTJ Toggle cell ≈ 1–1.5 µm² from training memory]. Only affects the Toggle cost row, which is already ~700x DRAM by street price.
- **A-A2-9** [A2] Weebit ReRAM 1T1R cell on 130nm ≈ 0.8 µm² (≈47 F²), 2 extra masks — basis: [ESTIMATE: transistor-limited 1T1R at 130nm; Weebit "few extra masks" claim from training memory].
- **A-A2-10** [A2] Street prices of Everspin parts are distributor reference quotes (LCSC, Future, DigiKey via Findchips) of uncertain date; OEM contract prices (e.g., IBM) are likely 2–4x lower — basis: distributor-vs-OEM norms [ESTIMATE]. Even at 4x lower, 1Gb MRAM ≈ $200/GB ≫ DRAM $20/GB.
- **A-A2-11** [A2] Used Optane PMem 100/200 module prices on the secondary market are UNKNOWN (search budget exhausted); card A2-11 assumes $0.8–2.0/GB used, to be verified by the kill experiment (scrape eBay sold listings) — basis: [UNVERIFIED].
- **A-A2-12** [A2] Everspin nvNITRO (MRAM NVMe accelerator, ~2017) was discontinued without volume — basis: [UNVERIFIED: training-data memory; not re-verified in 2026 because the web-search budget ran out].
- **A-A2-13** [A2] Toggle MRAM / ReRAM radiation tolerance (>1 Mrad TID for Toggle) — basis: Frontgrade/Cobham case study; ReRAM intrinsic rad tolerance is [UNVERIFIED: training literature].
- **A-A2-14** [A2] Everspin–Microchip agreement bars Microchip from making TMR devices for Everspin competitors during term + 2 years — basis: Everspin 8-K 2026-04-08 (via search snippet). Treated as blocking any startup from using Gresham Fab 4 for MTJ.
- **A-A2-15** [A2] Avalanche v. Everspin ITC 337-TA-1487 final determination ≈ mid-2027 — basis: Panabee/Getquin summaries + ITC norm of 14–16 months from 2026-02-27 institution.
- **A-A2-16** [A2] SanDisk "3D Matrix Memory" is chalcogenide crosspoint (PCM/OTS-like) — basis: eeNews Europe inference; SanDisk has not confirmed [UNVERIFIED].
- **A-A2-17** [A2] Founder can hire a contract hardware engineer at ~$120–150/hr for ~200–400 hours in year 1 (≈$30–60k) for any design-in card — basis: [ESTIMATE: U.S. contract EE rates]; this pushes hardware cards to T1.
- **A-A2-18** [A2] Web research constraint: sec.gov, everspin.com, weebit-nano.com, mram-info.com and storagenewsletter.com fetches were blocked by the session network policy, and the shared web-search budget was exhausted after ~50 searches; all such facts are tagged "(via search snippet)" in sources/A2.jsonl.

</details>

<details><summary><b>A3</b> (33)</summary>

- **A-A3-1** [A3] The shared WebSearch budget (200 calls per turn, shared by every agent) was already used up when A3 started. Every A3 WebSearch call was refused. General web hosts returned proxy 403 or failed DNS (en.wikipedia.org; www.gsitechnology.com tested once). The only reachable primary sources were public GitHub repositories (anonymous git) and the PyPI JSON API — basis: tool errors 2026-11-01; `$HTTPS_PROXY/__agentproxy/status` showed 403s for trendforce/micron/sec.gov.
- **A-A3-2** [A3] Company-status facts (alive, acquired, shipping, revenue) for GSI Technology, Nantero, Groq, Cerebras, d-Matrix, RAAAM, Thinfilm/Ensurge, Innovative Silicon, T-RAM Semiconductor, Kilopass and Efabless come from training data that ends around mid-2026. They are tagged [UNVERIFIED-training] and are NOT confirmed as of 2026-11-01. Phase-3 verify agents should re-check them first — basis: no web access.
- **A-A3-3** [A3] Cross-referenced URLs taken from other agents' logs (A1, A2) are logged with a CROSS-REFERENCE tag. A3 did not open them — basis: CONVENTIONS source rule; p1-fabs precedent.
- **A-A3-4** [A3] DDR5 today: contract ≈ $14–25/GB, spot ≈ $27/GB (Aug–Sep 2026). Glut (A-05, −60%): ≈ $10–12/GB. Severe glut: ≈ $3/GB — basis: research/phase1/market.md §2.3 and §glut.
- **A-A3-5** [A3] Incumbent DRAM *cost* ≈ $2.7/GB. Computed from A1's reference row (0.436 Gb/mm², $5,500 1b wafer, 88% yield, $0.8/GB test+pkg) with A3's usable-area rule — basis: A1_device_params REF-DDR5-1b, scratch calc.
- **A-A3-6** [A3] Usable die area = 85% of gross wafer area (300mm: 60,083 mm²; 200mm: 26,704 mm²), covering edge exclusion and scribe — basis: common rule of thumb [ESTIMATE].
- **A-A3-7** [A3] die_density_Gb_per_mm2 = (1/cell_area_um2) × 1e6 × array_efficiency × layers × bits_per_cell / 1e9 (same formula as A1) — basis: consistency with A1_device_params.
- **A-A3-8** [A3] Test+package cost per die: $1.5 for a DRAM-like 100 mm² standalone die; $3 for a 200 mm² SRAM die; $1.5 for a small 16Mb SRAM in TSOP/BGA. $/GB = per-die cost / GB per die — basis: [ESTIMATE: OSAT lore; consistent with A2's $1.0–2.5/die].
- **A-A3-9** [A3] Array efficiency: 0.70 for large standalone SRAM, 0.65 for gain-cell macros, 0.50 for capacitor-less standalone DRAM, 0.45 for 1T1C eDRAM — basis: [ESTIMATE: typical sense-amp/decoder overheads; DRAM ~0.55 in A1].
- **A-A3-10** [A3] 300mm: 65nm $1,600; 40nm $2,000; 28nm $3,000 (gain-cell variant $3,200); 16/12nm $5,500; N5 $17,000; N2 $30,000; 45nm PD-SOI + floating-body adder $3,700; 32nm SOI + thyristor adder $4,500; 14nm SOI + deep-trench eDRAM (IBM 14HP class) $7,500. Fully depreciated cash-cost case: $2,500 — basis: A2 assumptions use 28nm ≈ $3k base and 1b DRAM ≈ $6k. N2 ≈ $30k is widely reported but unverified here.
- **A-A3-11** [A3] 200mm: 130nm (SkyWater S130 class) $1,300–1,500; 65nm (SkyWater Fab 25 class) $1,800 — basis: A1 used $1,200 for 200mm 130nm. Fab 25 node range 130–65nm per the cross-referenced SkyWater/Infineon release.
- **A-A3-12** [A3] Published 6T SRAM bitcells: 65nm 0.525 µm²; 40nm 0.242 µm²; 28nm 0.127 µm²; 16nm 0.074 µm²; N5 0.021 µm²; N2 macro density 38.1 Mb/mm² (TSMC IEDM 2024) — basis: [UNVERIFIED-training: foundry and IEDM disclosures]. Only the SkyWater 130nm cell (1.896 µm²) was verified from the PDK LEF.
- **A-A3-13** [A3] 130nm 200mm SRAM for long-lifecycle parts uses a 2.0 µm² cell — basis: close to the verified sky130 1.896 µm² cell.
- **A-A3-14** [A3] Floating-body 1T-DRAM cell is 8F² at 45nm PD-SOI (0.0162 µm²) — basis: [ESTIMATE; ISi and Toshiba FBC claimed 4–8F² in planar SOI]. In ultra-thin FD-SOI (<10 nm Si) the body holds too little charge for reliable sensing — basis: [UNVERIFIED-training; device-physics argument].
- **A-A3-15** [A3] Thyristor RAM (TCCT) cell is 10F² at 32nm SOI. Kilopass VLT claimed 4F² — basis: [UNVERIFIED-training: T-RAM and Kilopass marketing claims]. Holding current is 1–100 pA/cell in the ON state, so a 1 Gb array idles at 1–110 mA — basis: [ESTIMATE, computed].
- **A-A3-16** [A3] Si 2T/3T gain cell at 28nm is ≈0.065 µm² (≈50% of HD 6T). Retention is ≈10–100 µs at 85°C, rising to ms at 25°C — basis: [UNVERIFIED-training: RAAAM "~2x denser than SRAM" claim; Teman/Giterman/Burg gain-cell literature].
- **A-A3-17** [A3] IBM 14nm SOI eDRAM cell is 0.0174 µm² (IEDM 2014). Intel 22nm eDRAM cell is 0.029 µm², and the 128MB Crystalwell die is ≈77 mm² — basis: [UNVERIFIED-training].
- **A-A3-18** [A3] Nantero NRAM is 1T1R at 28nm, transistor-limited at ≈30F² — basis: [ESTIMATE]. Nantero claims of 5 ns switching, >1e11 cycles and >10-year retention at high temperature are [UNVERIFIED-training].
- **A-A3-19** [A3] Cryogenic leakage reduction raises Si gain-cell retention by ≥100–1000× at 77 K and 4 K — basis: [UNVERIFIED-training: cryo-CMOS eDRAM literature 2020–2024].
- **A-A3-20** [A3] Thinfilm printed memory label holds 20 bits and costs ≈ $0.10, i.e. ≈ $4e7/GB — basis: [ESTIMATE; Thinfilm 20-bit Memory product from training data].
- **A-A3-21** [A3] Innovative Silicon (Z-RAM) licensed AMD (2006) and Hynix (2007), closed in 2010, and its patents went to Micron.
- **A-A3-22** [A3] T-RAM Semiconductor licensed AMD (2006) and partnered with GlobalFoundries (2009, 32/22nm SOI). It was defunct by about 2010–11.
- **A-A3-23** [A3] Kilopass announced the VLT thyristor DRAM in 2016. Synopsys acquired Kilopass in early 2018, and VLT was never commercialized.
- **A-A3-24** [A3] IBM POWER7/8/9 and z-series used deep-trench eDRAM on 45/32/22/14nm SOI. POWER10 and z16 (Samsung 7nm) dropped eDRAM for SRAM. GF sold East Fishkill (ex-IBM 300mm) to onsemi, completed end-2022.
- **A-A3-25** [A3] Groq's first-gen LPU is ≈230 MB SRAM on GlobalFoundries 14nm (Malta, NY), ≈725 mm². In December 2025 Groq and NVIDIA announced a non-exclusive technology license plus executive hires, reported at ≈ $20B; GroqCloud continues.
- **A-A3-26** [A3] Cerebras WSE-3: 44 GB on-chip SRAM, TSMC 5nm, 46,225 mm² (Mar 2024). Cerebras withdrew its IPO filing in Oct 2025 after a $1.1B raise. Large OpenAI compute deal in Jan 2026.
- **A-A3-27** [A3] d-Matrix Corsair: SRAM-based digital in-memory compute cards with ≈2 GB SRAM plus LPDDR5 capacity memory. Raised ≈ $275M in Nov 2025.
- **A-A3-28** [A3] GSI Technology (Sunnyvale): FY2025 revenue ≈ $20M, operating losses, funded by equity raises. Gemini-I APU (TSMC 28nm) and Gemini-II (TSMC 16nm). A Cornell study in Oct 2025 drew attention to APU energy efficiency on retrieval workloads.
- **A-A3-29** [A3] RAAAM Memory Technologies (Israel) is commercializing Si gain-cell "GCRAM" IP and claims ≈2x SRAM density and much lower leakage.
- **A-A3-30** [A3] ISSI is owned by China's Ingenic Semiconductor (since 2020). This matters for U.S. defense second-source buyers.
- **A-A3-31** [A3] Efabless shut down in early 2025. ChipFoundry runs Caravel/SkyWater 130nm shuttles and a marketplace — partially VERIFIED from the ChipFoundry GitHub README (last commit 2026-04-23).
- **A-A3-32** [A3] SkyWater MPW slot via ChipFoundry costs ≈ $10–15k for ≈10 mm² user area — basis: [UNVERIFIED-training: Efabless chipIgnite ≈ $9,750].
- **A-A3-33** [A3] Contract memory/analog IC designer costs $150–200/hr — basis: [ESTIMATE]. A2 used $120–150/hr for general hardware EEs.

</details>

### Phase 2 — ideation (architecture)

<details><summary><b>B</b> (25)</summary>

- **A-B-1** [B] Vendor-status facts that I could not re-open this session are tagged `[UNVERIFIED-T]` (training knowledge, roughly mid-2026) and carry no URL. This covers Astera Leo, Marvell Structera, Montage, Microchip SMC 2000, Samsung/Micron/SK hynix CMMs, Liqid, GigaIO, XConn, Panmnesia, Unifabrix, Enfabrica, ZeroPoint, Pliops, VAST, Hammerspace, NVIDIA ICMS, d-Matrix, Mythic, EnCharge, Sagence, GSI, UPMEM, Eliyan and SanDisk HBF — basis: the shared WebSearch budget (200 per turn) was already exhausted when B started, and WebFetch could not resolve arxiv.org, asteralabs.com or zeropoint-tech.com (network allowlist). Only public GitHub repos (git clone) were reachable.
- **A-B-2** [B] A URL another agent logged from a search snippet is cited as CROSS-REFERENCE and was not opened by B — basis: CONVENTIONS.md source-logging rule.
- **A-B-3** [B] DDR5 server RDIMM costs about $20–32/GB in 4Q26 (midpoint $26) — basis: Counterpoint's 64GB RDIMM contract went from >$900 in 1Q26 (≈$14/GB), then rose with TrendForce's +58–63%, +13–18% and +10–15% QoQ in 2Q–4Q26; street price was about $2,064 per 64GB (≈$32/GB) in Aug 2026 (ServNet). It is an ESTIMATE.
- **A-B-4** [B] In the 2028–29 glut, DDR5 RDIMM costs about $8–12.8/GB (midpoint $10.4) — basis: mission assumption A-05 (−60%) applied to the 4Q26 range.
- **A-B-5** [B] Recovered DDR4 RDIMM resale value (the opportunity cost of reusing it) is about $25/GB in 4Q26, about $12/GB in the glut and about $1/GB at the 2023 trough — basis: DDR4 8Gb spot was $21 (TrendForce, 2026-08-03) to $44 (DRAMeXchange via BuySellRAM, 2026-08-31), and 8Gb = 1GB per chip, less a 20–40% discount for used modules. The glut case assumes DDR4 stays "sticky" because supply is EOL. Trough: DDR4 8Gb was $1.30 in Sep 2023 (KED).
- **A-B-6** [B] GPU-attached HBM costs about $180–250 per GB of HBM when bought as an H200/B200-class GPU — basis: ESTIMATE of roughly $30k per 141GB GPU. This is not a verified list price. HBM3E at the die level is about $12/GB ($1.50/Gb, SammyFans 2026-10-02).
- **A-B-7** [B] Enterprise TLC NVMe costs about $0.30–0.60/GB in 4Q26 — basis: ESTIMATE from about $0.15/GB in early 2025, compounded by the NAND contract increases of 1H26 (+55–60%, +70–75%). NAND turned flat in Oct 2026 and is forecast to reach surplus in 2H27.
- **A-B-8** [B] H100 SXM dense BF16 peak is 989 TFLOPS at 45% MFU in prefill — basis: the NVIDIA datasheet figure from training knowledge [UNVERIFIED-T]; the MFU is an ESTIMATE.
- **A-B-9** [B] An H100-hour costs $2.50 at a neocloud in 2026 — basis: ESTIMATE.
- **A-B-10** [B] Production serving uses an FP8 KV cache, which halves the BF16 KV bytes — basis: ESTIMATE / common practice.
- **A-B-11** [B] Reload bandwidth: 12 GB/s for one Gen5 x4 NVMe, about 50 GB/s for a CXL x16 Gen5 expander, about 45 GB/s for 400G RDMA, and about 55 GB/s for host DDR5 to GPU over PCIe Gen5 x16 — basis: interface line rates minus about 20% overhead (ESTIMATE).
- **A-B-12** [B] Dense-model prefill costs 2×P FLOPs per token — basis: the standard transformer approximation.
- **A-B-13** [B] An EPYC 9005 socket has 12 channels of DDR5-6400 (614 GB/s peak), with 60% achievable — basis: platform spec [UNVERIFIED-T] and an ESTIMATE for efficiency.
- **A-B-14** [B] A Kimi-K2-class MoE has about 32B active parameters per token, with routed experts in INT4 (0.5 B/param) — basis: model card [UNVERIFIED-T]. KTransformers documents native INT4 for Kimi K2.5.
- **A-B-15** [B] A CXL Type-3 expander adds about 70–100 ns over local DRAM (one hop) — basis: the Pond paper (ASPLOS '23) as I recall it [UNVERIFIED-T].
- **A-B-16** [B] A low-volume CXL add-in card without DRAM (controller, PCB, firmware and qualification amortized) costs about $1,200 per 512GB card (≈$2.34/GB). At hyperscaler volume an in-house board costs about $250 (≈$0.49/GB) — basis: ESTIMATE. Merchant controller prices are not public.
- **A-B-17** [B] A hyperscaler dumping DDR4 into the market realizes about 50% of spot — basis: ESTIMATE. Selling millions of DIMMs would move the price.
- **A-B-18** [B] The on-prem MoE appliance platform (2S EPYC board, CPUs, chassis, PSU, 2 workstation GPUs) costs about $36k excluding DRAM, and the hardware gross-margin target is 22% — basis: ESTIMATE.
- **A-B-19** [B] Holding about 1TB of model weights entirely in HBM takes 8 H200-class GPUs at about $30k each (≈$240k) — basis: ESTIMATE.
- **A-B-20** [B] An FPGA-based CXL compression card (Agilex 7 R-tile or Versal Premium class) has a BOM of about $3–8k before DRAM — basis: ESTIMATE from FPGA dev-kit pricing [UNVERIFIED-T].
- **A-B-21** [B] Tape-out of an N6/12nm memory-controller chiplet, including masks, IP and packaging NRE, costs $20–60M — basis: ESTIMATE.
- **A-B-22** [B] Branch B cards stay hardware/system/IP. Anything mostly software (KV-cache SaaS, memory-tiering daemons, RAM-as-a-service brokerage, price data) was left to Branch D and listed as "considered, not carded" in B_notes.md.
- **A-B-23** [B] A vendor's CXL product counts as "shipping" only where B has a primary source. Otherwise it is "announced/[UNVERIFIED-T]".
- **A-B-24** [B] The DDR4-in-CXL reuse economics are scored from the owner's point of view: reuse beats resale only if card $/GB + DDR4 resale $/GB < new DDR5 $/GB.
- **A-B-25** [B] For the founder, "doable" means startable with <$50k, a day job, and no hardware engineering team in the first 12 months.

</details>

### Phase 2 — ideation (supply chain)

<details><summary><b>C</b> (31)</summary>

- **A-C-1** [C] No fact in Branch C is [VERIFIED] from a primary page opened by C, except the two GitHub repositories (memtest86plus, stressapptest), which were cloned and read. — basis: the shared WebSearch budget (200 per turn) was exhausted before C started (3 queries refused), and WebFetch could not resolve www.acquisition.gov, www.alliancememory.com or www.powerchip.com (outside the session's allowed network domains). C stopped trying more hosts after those 3 failures, as instructed by the tool.
- **A-C-2** [C] URLs that sibling agents logged from search snippets are reused as CROSS-REFERENCE with the sibling's title and date, and are flagged as not opened by C. — basis: CONVENTIONS.md source-logging rule.
- **A-C-3** [C] Company facts from training knowledge (to about mid-2026) are tagged `[UNVERIFIED-training]` and carry no URL. Examples: Qimonda Richmond fab closure (2009), CXMT's use of Qimonda documents and patents (2019), PSMC's DRAM-foundry service, Etron/Zentel sourcing, Intelligent Memory's stacked DDR3, CAMM2 (JEDEC), Iron Mountain/ITRenew (2022), Champion Spark Plug v. Sanders (1947), BAA domestic-content thresholds, SPD byte offsets. — basis: no web access.
- **A-C-4** [C] DDR4 8Gb contract = $16/GB "now" — basis: TrendForce price page snapshot, June 2026 (cross-ref A2).
- **A-C-5** [C] DDR4 8Gb spot = $21–44/GB — basis: TrendForce spot 2026-08-03 ($21.00) and DRAMeXchange via BuySellRAM 2026-08-31 ($44.37) (cross-ref p1-backend/B).
- **A-C-6** [C] DDR3 4Gb contract = $10 per chip = $20/GB — basis: TrendForce price page snapshot, June 2026 (cross-ref A2).
- **A-C-7** [C] DDR5 16Gb spot = $26.96/GB — basis: $53.92 average on 2026-08-31 (BuySellRAM, cross-ref).
- **A-C-8** [C] Glut (A-05): DDR5 at 40% of now; legacy DDR4 at 45% of now ($7.2/GB contract), DDR3 at 45% of now — basis: ASSUMPTIONS A-05 says DDR4 falls less in % than DDR5's 60%. A separate "stress" case ($2/GB DDR4, $1/GB used RDIMM) mimics 2023 (DDR4 8Gb fixed price bottomed at $1.30, KED Global Sep 2023).
- **A-C-9** [C] Used DDR4 RDIMM resale = $4–10/GB in 2026 (mid $6) — basis: ESTIMATE; p1-backend estimated $3–8/GB, but new DDR4 chips at $16–44/GB imply used modules could trade higher. **Kill-check: 90 days of eBay sold listings for 32GB PC4-2933Y / 64GB PC4-3200AA RDIMMs.**
- **A-C-10** [C] 25nm-class DDR4 density = 0.11 Gb/mm² (8Gb die ≈ 73 mm²) — basis: ESTIMATE, between 3x-nm DDR3 (~0.07) and 1z DDR4 (~0.18) used by p1-backend; Micron 1-alpha ≈ 0.3 Gb/mm² class [ESTIMATE], 1b ≈ 0.436 (Kurnal via KitGuru, cross-ref).
- **A-C-11** [C] Capex $2.0–3.5B for 10–20k wafers/month at 300mm with refurbished tools; 5-year straight-line depreciation; cash opex $1,800/wafer; 80% yield; $0.60/GB package and test — basis: ESTIMATE anchored on Micron's >$2B Manassas expansion (HPCwire, cross-ref) for a smaller, existing-shell project.
- **A-C-12** [C] Foundry DRAM wafer price $3,000 (25nm-class, 300mm); package and test $1.20/GB; brand longevity premium 15% over contract; NRE ≈ $15M (design $10M, masks and qualification $3M, test programs $2M) — basis: ESTIMATE; no PSMC price list could be opened.
- **A-C-13** [C] DDR5 64GB RDIMM = 80 GB raw DRAM + $25 other parts + $12 U.S. assembly and test — basis: p1-backend §3.4 construction; prices from Counterpoint via EE Times Asia and ServNet (cross-ref).
- **A-C-14** [C] Fee 4% per year of consigned inventory value + $12k/yr software per OEM; space $60k/yr (3,000 sq ft); one nitrogen dry cabinet (~$5k, 7-year life) per $400k of DRAM; insurance 0.3% of inventory; staff $90k (≤8 OEMs) or $180k; audits and certifications $30k/yr — basis: ESTIMATE from general warehousing and component-storage norms; no vendor quotes.
- **A-C-15** [C] Acquisition at 60% of resale price; eBay fees 13.25% vs B2B 3%; shipping $5 (eBay) vs $1.50 (B2B bulk); 6 min test labor at $28/hr loaded; $0.50 test-bed amortization; 3% failures written off; 2% returns — basis: p1-backend §6.6 inputs, adjusted for a B2B channel [ESTIMATE].
- **A-C-16** [C] In a glut, acquisition prices reprice at the same ratio (optimistic); real inventory losses during the fall add ~3 points of margin loss — basis: judgment.
- **A-C-17** [C] Starter kit $8–20k (bench SPD tester, 4–6 used DDR4 servers, ESD bench, thermal chamber) — basis: p1-backend §7.
- **A-C-18** [C] Rework cost $3.60 per chip (6 min labor at $28/hr + $0.30 materials + $0.50 X-ray share); harvested-die value 35% of new — basis: ESTIMATE.
- **A-C-19** [C] Tiers: reseller $1.5k/month (25 customers), integrator $5k/month (10), OEM/ODM $12k/month (2); 6 lab samples per customer-year at $1,200 pass-through +30%; software and support cost 15% of ARR — basis: ESTIMATE; Section 889 compliance-tool pricing as analog [UNVERIFIED-training].
- **A-C-20** [C] §5949 takes effect 2027-12-23 (417 days from 2026-11-01) — basis: p1-funding (enactment 2022-12-23 + 5 years) and XenoSpectrum "Dec 2027" (cross-ref). The FAR implementing rule's status and text are UNVERIFIED and are the single biggest swing factor for C-07.
- **A-C-21** [C] DDR4 SPD bytes 350–351 and DDR5 SPD bytes 552–553 hold the DRAM-die manufacturer JEP106 ID — basis: [UNVERIFIED-training] JEDEC SPD annexes; memtest86+ source confirms the module-maker offsets (320–321 / 512–513) only.
- **A-C-22** [C] GigaDevice-branded DDR4 is CXMT-fabbed — basis: [UNVERIFIED-training]; used only to argue that module/package labels cannot prove die origin.
- **A-C-23** [C] 9 × 8Gb x8 KGD at contract +30% KGD premium; $120 U.S. substrate and assembly; $150 screening and data pack; ASP $800–3,000; NRE $1.5M — basis: ESTIMATE; hi-rel memory 10–100x commodity $/bit (p1-backend §4.3).
- **A-C-24** [C] 32GB DDR3 RDIMM = 72 × 4Gb in 36 DDPs; DDP packaging $1.20 each; $25 PCB/register/assembly; 25% markup — basis: ESTIMATE.
- **A-C-25** [C] 16GB DDR5 SODIMM: industrial-temp component premium 5%; $15 PCB/PMIC/SPD + $25 U.S. EMS assembly, conformal coat and screen; commodity module = 1.10 × chip value; rugged premium 1.3–1.6× commodity — basis: ESTIMATE.
- **A-C-26** [C] Startup capex $750k (used ATE $250k, prober $150k, two probe cards $100k each, program development $150k); $600 per wafer probe revenue; $150 per wafer variable cost; $300k/yr fixed (2 engineers + facility) — basis: ESTIMATE from p1-backend §7 ranges.
- **A-C-27** [C] 1T1C MIM cell 0.25 µm² at 65nm, array efficiency 55%, 200mm wafer $2,000 incl. extra capacitor masks, 60% yield, $15 package and test, NRE $10–20M, DoD DMSMS demand 10–100k units/yr at $40–60 — basis: ESTIMATE; no SkyWater quote.
- **A-C-28** [C] Agency model fee 2.5% of pooled spend + $10k/yr membership; opex $150k + $2k per member; title model needs ~50 days of GMV as working capital — basis: ESTIMATE; distributor gross margins on memory 3–8% [UNVERIFIED-training].
- **A-C-29** [C] Optane/PCM revival and CXL-DDR4 reuse are not re-carded in Branch C because A2-10, A2-11, B-01, B-09 and B-14 already cover them — basis: avoid cross-branch duplicates; kill reasons are recorded in C_notes.md §6.
- **A-C-30** [C] "U.S.-made" premium is priced at zero for commodity memory today — basis: TAA treats Taiwan/Korea/Japan as designated countries; memory is excluded from Section 232 phase 1 (Korea Times 2026-09-15, cross-ref); the 100% memory-tariff threat was not implemented (TrendForce 2026-01-19, cross-ref).
- **A-C-31** [C] DoD channel is closed to recovered DRAM (DFARS 252.246-7008 / FAR 52.211-5 new-material rule) unless a contracting officer approves — basis: [UNVERIFIED-training], consistent with p1-backend and p1-funding.

</details>

### Phase 2 — ideation (software)

<details><summary><b>D</b> (23)</summary>

- **A-D-1** [D] AWS list prices are a fair proxy for "cloud memory prices" for SMB SaaS buyers. — basis: AWS has the largest share; the Azure retail-price API was blocked (403); GCP was not tried.
- **A-D-2** [D] AWS on-demand list prices for 92 EC2 SKUs and ElastiCache node SKUs in us-east-1 did not change between the Sep-2025 and Oct-2026 price-list versions. — basis: D downloaded both versions from the AWS Price List API and diffed them. This does not rule out changes to Savings Plan or Reserved Instance discounts, Spot prices, or capacity availability, none of which D checked.
- **A-D-3** [D] Marginal cloud RAM costs $2.56–2.62 per GiB-month. — basis: (r7i.large − c7i.large)/12 GiB × 730 h, and (r8g.large − m8g.large)/8 GiB × 730 h, using AWS list prices.
- **A-D-4** [D] On-prem DDR5 RDIMM costs $14–16/GB at contract and ~$32/GB at street (2026). It is amortized straight-line over 60 months, giving $0.23–0.54 per GB-month. — basis: Counterpoint via EE Times Asia ($900–1,000 per 64GB); Servnet ($2,064 per 64GB), both via p1-market. The 60-month life is D's own ESTIMATE.
- **A-D-5** [D] Glut scenario: DDR5 and server DRAM $/GB fall 60% from the 2026 peak in 2028–29 (root ASSUMPTIONS A-05). Glut on-prem DRAM is taken as about $6/GB. — basis: A-05 applied to ~$15/GB.
- **A-D-6** [D] Reference SMB SaaS customer: $40k/month EC2 bill, with RAM about 30% of the bill. — basis: ESTIMATE. RAM is 28% of m7i.large and 43% of r7i.large list price (computed from AWS prices).
- **A-D-7** [D] 18% of provisioned Kubernetes memory is unused, and only about 50% of it can be realized because instance sizes couple CPU and RAM. — basis: the Sysdig figure quoted in the robusta-dev/krr README; the 50% realizable share is an ESTIMATE.
- **A-D-8** [D] A right-sizing or audit vendor can charge about 25% of verified monthly savings. — basis: ESTIMATE, the common FinOps "share of savings" model; no vendor price list was opened.
- **A-D-9** [D] Fleet-reclaim reference: 200 servers × 512 GB, 20% cold memory, zram/zswap at about 2:1 compression, giving ~10 TB of deferred DRAM purchase. — basis: 2:1 is the expectation stated in the Linux zram docs. The 20% cold fraction is an ESTIMATE, consistent with the 20–32% savings Meta reported for TMO (ASPLOS'22) [UNVERIFIED-T: paper not opened].
- **A-D-10** [D] Recovered DDR4 RDIMM sells at $3–8/GB in 2026. — basis: p1-backend estimate (us_backend.md §6). A 1.5 TB dual-socket chassis without RAM costs about $1,500 [ESTIMATE], and East Coast retail colo costs about $250/month per 2U server [ESTIMATE].
- **A-D-11** [D] A TB-RAM rental can be priced at about $1,200/month, roughly 25% of the AWS x2idn.16xlarge on-demand price of $4,868/month. — basis: ESTIMATE, priced below cloud to compete with Hetzner/OVH-class hosts. Hetzner and OVH 2026 prices were NOT verified.
- **A-D-12** [D] The ElastiCache Redis OSS Extended Support SKU ($0.175/h Yr1–2, $0.35/h Yr3 on cache.r7g.large) is charged on top of the base node-hour price. — basis: the SKUs are separate usage types in the AWS price list. Treating them as additive is D's interpretation [ESTIMATE].
- **A-D-13** [D] AWS lets customers move an ElastiCache Redis OSS cluster to Valkey in place with little effort. — basis: [UNVERIFIED-T] training knowledge of the 2024 ElastiCache Valkey launch.
- **A-D-14** [D] KV cache for Llama-3.1-70B is 320 KiB per token at BF16 (80 layers × 8 KV heads × 128 dim × 2 × 2 bytes). — basis: model config via B's GitHub source; arithmetic by D.
- **A-D-15** [D] SMB OEM memory-intelligence SaaS sells at $150–300 per account per month. — basis: ESTIMATE, priced below analyst-firm seats. TrendForce, Gartner and Omdia subscription prices were NOT verified; they are believed to be $5k–$50k+ per year [UNVERIFIED-T].
- **A-D-16** [D] A memory-shortage newsletter reaches 200–500 paid subscribers at $10–12/month. — basis: ESTIMATE for a niche B2B newsletter without proprietary data.
- **A-D-17** [D] Embedded OEM reference: 20k units/year, 1 GB of LPDDR4/DDR4 saved per unit, at $8–21/GB in 2026 and ~$2.5/GB in a glut. — basis: the $21/GB mobile LTA ceiling (Wccftech via p1). The $8/GB low end and the glut figure are ESTIMATES.
- **A-D-18** [D] Amazon Associates pays roughly 2–4% commission on computer components. — basis: [UNVERIFIED-T] training knowledge.
- **A-D-19** [D] The NDAA FY2023 §5949 ban takes effect in Dec 2027 and could cover DIMMs inside federal-bound servers. — basis: XenoSpectrum via p1-backend. The FAR implementing rule and whether it covers subcomponents are [UNVERIFIED].
- **A-D-20** [D] In DDR4/DDR5 SPD, the DRAM-die manufacturer ID bytes sit next to the module-manufacturer bytes (DDR4 bytes 350–351, DDR5 bytes 552–553). — basis: [UNVERIFIED-T] JEDEC SPD spec knowledge. The memtest86+ source D opened reads only the module-manufacturer bytes (320–321 and 512–513).
- **A-D-21** [D] Software concepts get materials_sense "none" because they trade CPU cycles, NAND or cloud dollars for DRAM bits and do not change memory materials. Concepts that reuse depreciated hardware get "c-capital". — basis: mission rule 5.
- **A-D-22** [D] Software TRL is the TRL of the underlying mechanism in production somewhere (for example zswap at Meta/Google = 9). Product maturity for a newcomer is described in the text. — basis: rule 1 asks for mechanism evidence.
- **A-D-23** [D] Founder time is about 15 h/week and deployable capital about $40k (root A-03). Any concept that needs 24/7 on-call or more than $50k of hardware is "marginal" at best for founder-fit. — basis: A-03.

</details>

### Phase 2 — ideation (business models)

<details><summary><b>E</b> (28)</summary>

- **A-E-1** [E] The shared WebSearch budget was exhausted before E ran a single search, and WebFetch to rochesterelectronics.com, sandia.gov and technology.nasa.gov failed DNS resolution (host not allowed in this session). E stopped trying further hosts, as the session rules require. Basis: tool errors at 2026-11-01.
- **A-E-2** [E] Primary sources E actually opened: the official GSA FAR and DFARS DITA repositories on GitHub, plus the rasdaemon repository. Every other URL is a CROSS-REFERENCE to a sibling agent's log, flagged as such in `sources/E.jsonl`. Basis: CONVENTIONS.md logging rules.
- **A-E-3** [E] Tech-transfer portal listings (Sandia, LANL, ORNL, LBNL, ANL, PNNL, NASA T2, AFRL/TechLink, NRL, UMN, Purdue, Penn State, Notre Dame, GT, MIT, Stanford, Cornell, UCSD, Michigan, NC State, ASU, RPI, SUNY Albany) could NOT be queried. No patent number in E's files is verified. Basis: network policy. Queries are listed as a verification queue in `E_notes.md` §6.
- **A-E-4** [E] The FAR repo covers FAC 2025-06 (2025-10-01; last commit 2026-03-30) and the DFARS repo's last commit is 2026-06-02. "No §5949 text" holds for those snapshots. A later interim rule, or a Revolutionary FAR Overhaul (RFO) deviation published only on acquisition.gov, could exist unseen. Basis: repo README and commit dates.
- **A-E-5** [E] DDR5 component contract $15.99/GB (Q4-2026); 64GB RDIMM $20.31/user-GB; glut (−60%) $6.40/GB component and $8.13/user-GB RDIMM; severe glut $1.60/GB; cost floor RDIMM $2.41/user-GB. Basis: `models/dram_cost_stack.py` `ddr5_reference()`.
- **A-E-6** [E] DDR5 spot $26.96/GB (DRAMeXchange 16Gb avg $53.92, 2026-08-31), so spot runs about 1.69× contract. Basis: BuySellRAM/DRAMeXchange via p1-backend/B.
- **A-E-7** [E] Annualized contract-price volatility is 44% (from 2024–26 TrendForce QoQ midpoints) or 55% (adding the 4Q18, 1Q19, 1Q23 and 2Q23 downturn quarters). It is computed from quarterly log changes × √4. Missing 2025-Q1/Q3 points are skipped. Basis: `research/phase1/price_series.json`; p1-market §7.1.
- **A-E-8** [E] The cap premium uses Black-76 with the forward equal to the Q4-2026 contract price (flat forward = "plateau" consensus), a 4.5% discount rate and T = 1 year. Basis: standard option pricing; consensus plateau (p1-market §7.2).
- **A-E-9** [E] A newcomer buys at spot + 5% (broker ask) and sells at spot − 5%. Carry is 15%/yr (12% cost of capital, 2% storage/insurance/test, 1% shrink/counterfeit loss). Basis: judgment; broker-market norms.
- **A-E-10** [E] Scenario weights for Nov-2027: squeeze 25% (contract ×1.25, spot/contract 1.6), plateau 40% (×1.05, 1.2), soft turn 25% (×0.90, 1.0), early turn 10% (×0.65, 0.9). Basis: p1-market §7.2 analyst spread; spot premiums normally compress as panic fades [ESTIMATE].
- **A-E-11** [E] A small lessor pays $1,600 for a 64GB DDR5 RDIMM (between the $1,300 contract price and the $2,064 street price) and carries a 14%/yr cost of capital (non-investment-grade). Basis: judgment.
- **A-E-12** [E] Residual at end of 2029 is 50% of the glut new price ($260), or 50% of the cost floor in a severe glut ($77). A lessee who walks in the 2028 glut returns the module for 60% of the glut new price, less 15% remarketing cost. Basis: used/new ratio ≈0.5 in 2023 (p1-backend §6.5); judgment.
- **A-E-13** [E] A single-part bank costs $600k (about 30 legacy 300mm wafers at ~$20k; p1-backend gives a $3k–22k/wafer range). Storage, insurance and re-test run 1.5%/yr of basis; U.S. OSAT packaging and test add 35% of die cost. Base case: sell at 3.0× die cost, 15%/yr in years 3–8. Bear: 2.0×, 50% sells. Bull: 4.0×, 95% sells in years 2–6. Basis: authorized-aftermarket pricing of about 1.5–5× original (p1-backend §5.3); judgment.
- **A-E-14** [E] Capex is $650k (X-ray, XRF, decap, used SEM/optical, curve tracer, memory functional tester, ISO/IEC 17025 setup). Fixed costs: 3 FTE at $95k loaded, $60k facility, $40k accreditation and calibration, 7-year depreciation. Revenue is $1,400 per lot against $300 variable cost. Basis: p1-backend §7 ($300k–$1M in-house lab; $500–3,000 per lot outsourced); judgment.
- **A-E-15** [E] Federal IT reseller gross margin is 6–10% on commodity memory/servers, with 45-day working capital. Basis: judgment from VAR norms [UNVERIFIED].
- **A-E-16** [E] Probabilities: DoD STTR Phase I award 20% per proposal, Phase II given Phase I 45%, Phase III or customer revenue given Phase II 35%. Timeline: option 2 months + proposal-to-award 5 + Phase I 9 + Phase II 24 + Phase III contracting 6 = 46 months. Basis: judgment from commonly reported DoD SBIR/STTR rates [UNVERIFIED-training].
- **A-E-17** [E] The STTR rule lets the PI be employed by the partner research institution. That makes the vehicle compatible with a founder who keeps a day job, but grants are funding, not revenue (A-04). Basis: p1-funding §7.3 [UNVERIFIED-H there].
- **A-E-18** [E] The target is a U.S. server-memory reseller/ITAD buyer with $1.2M EBITDA in 2026 (shortage-inflated), $0.4M in a normal year and $0.2M in a glut. Price is 3.5× trailing EBITDA. Financing: SBA 7(a) with a 10% equity injection, 10-year amortization, 10.5% rate (about Prime + 3). Basis: judgment; SBA terms from training [UNVERIFIED-training].
- **A-E-19** [E] A typical customer has 200 out-of-warranty DDR4 servers × 12 DIMMs = 2,400 DIMMs of 32GB, at $0.75/DIMM-month. Replacements: 1.5%/DIMM-yr (predictive at CE thresholds plus reactive). Spares pool is 2% of covered DIMMs, carried at 20%/yr. Shipping $18 per replacement; hosting/support $0.05/DIMM-month. Recovered DDR4 costs $4.7/GB now and $1.25/GB in a glut. Basis: field-study ranges recalled from training (Google 2009 SIGMETRICS "DRAM errors in the wild": ~8% of DIMMs see a correctable error per year; uncorrectable ~0.2%/DIMM-yr) [UNVERIFIED-training]; p1-backend §6.5–6.6 for recovered prices.
- **A-E-20** [E] 30 licensees at $6k/yr plus 5 enterprise licensees at $24k/yr. Data cost: $25k/yr self-built from distributor APIs, or $120k/yr if a contract-price feed must be licensed for redistribution. Basis: judgment [UNVERIFIED: TrendForce redistribution pricing unknown].
- **A-E-21** [E] Memory is 35% of the cost of a memory-heavy industrial/server deliverable. Basis: judgment; p1-backend §3.4 (DRAM is 93–98% of an RDIMM's value).
- **A-E-22** [E] CXL integration bills at $225/hr: 8 billable h/week part-time, or 1,100 h/yr full-time. Basis: judgment.
- **A-E-23** [E] Patent radar: 25 subscribers at $4,800/yr. Basis: judgment; an FTO opinion costs $10–30k (p1-ip §4).
- **A-E-24** [E] The LTB/die-banking seed was carded as a title-taking, authorized-aftermarket die bank (E-07). This differs from C-04, a consignment vault holding OEM-owned stock.
- **A-E-25** [E] The GPO/co-op seed was not re-carded because C-15 covers it.
- **A-E-26** [E] §5949 compliance was carded as a reseller model (E-09). This differs from C-07 (verification subscription) and D-11 (SPD scanner).
- **A-E-27** [E] The Optane seed was carded as an IP-estate acquisition (E-12) to avoid duplicating A2-10, A2-11 and B-09.
- **A-E-28** [E] A used-memory residual-value index was considered but not carded, because it overlaps C-05's graded-price index.

</details>

### Phase 3 — kill pass, device model & scoring

<details><summary><b>p3-audit-01</b> (6)</summary>

- **A-p3-audit-01-1** [p3-audit-01] Canonical decks for $/GB ratios: DDR5 4Q26 contract $15.99/GB, glut $6.40/GB, incumbent full cost $1.64/GB. Card figures that used $27 spot, an ~$11 glut and a $2.7 cost were restated — basis: 01_LANDSCAPE.md §4.3 and §10.4 #1.
- **A-p3-audit-01-2** [p3-audit-01] A practical IGZO/IWO 2T0C gain cell at 130nm is 30-60F2 (0.51-1.01 um2) against a sky130 6T SRAM cell of 1.896 um2, giving a 1.9-3.7x density advantage, not 4-5x — basis: geometry; consistent with 01_LANDSCAPE §4.4 (250-490x below DDR5 1b).
- **A-p3-audit-01-3** [p3-audit-01] Infineon Excelon F-RAM die is fabbed at TI Dallas DMOS6 (130nm, 300mm) as of the cited qualification document. Current-generation fab assignments could differ — basis: Infineon qual doc (via search snippet).
- **A-p3-audit-01-4** [p3-audit-01] No Penn AlScN license or spin-out exists publicly as of 2026-11-01 (two searches found none). This is unconfirmed, not proven absent — basis: search results.
- **A-p3-audit-01-5** [p3-audit-01] No SkyWater oxide-semiconductor or HZO module was announced as of 2026-11-01 — basis: one targeted search found none.
- **A-p3-audit-01-6** [p3-audit-01] Early revenue for device-IP and hi-rel eval-part ventures is blended NRE or small-lot sales at lower margin than steady-state royalties or qualified parts — basis: auditor judgment.

</details>

<details><summary><b>p3-audit-02</b> (11)</summary>

- **A-p3-audit-02-1** [p3-audit-02] Used 8 of 8 WebSearch calls; both WebFetch attempts failed (memex.ca, nano.stanford.edu not resolvable), so new evidence is search-snippet grade — basis: session network limits.
- **A-p3-audit-02-2** [p3-audit-02] No research/phase2/device_cost_output.md existed; no card in this batch is pitched on $/GB, so the canonical decks in 01_LANDSCAPE §4 were sufficient — basis: file check.
- **A-p3-audit-02-3** [p3-audit-02] C-09 killed as FACT-COLLAPSE (no product, seat taken by Neumonda) rather than R1, because the HfO2 1T1C mechanism itself is supported (Micron NVDRAM IEDM 2023) — basis: rule definitions.
- **A-p3-audit-02-4** [p3-audit-02] C-11 primary rule R3-FAB/T4 (certain from the card's own T4) with R1 as secondary, consistent with batch_01's C-05 handling — basis: consistency.
- **A-p3-audit-02-5** [p3-audit-02] C-12 revenue ceiling low-$100ks/yr — basis: judgment; legacy Fanuc/Mitsubishi PCMCIA-SRAM MRO volume assumed in the low thousands of cards/yr at $150-400.
- **A-p3-audit-02-6** [p3-audit-02] C-13 U.S. outsourced-reliability customer pool 10-30 — basis: judgment from the count of U.S. emerging-memory startups, SBIR/STTR performers and primes; universities own Radiant/aixACCT testers.
- **A-p3-audit-02-7** [p3-audit-02] C-13 gross margin 30-45% — basis: one ~$150-180k reliability engineer plus equipment carrying cost at low early utilization.
- **A-p3-audit-02-8** [p3-audit-02] C-14 treated as content under mission 'bridge, never the venture' because its asset is curated public literature; free Stanford Memory Trends/NVMDB remove the cost axis — basis: search snippets.
- **A-p3-audit-02-9** [p3-audit-02] C-14 buyer pool 'a few hundred seats' — basis: judgment (memory-focused VCs/CVCs, DoD/DOE PMs, OEM strategists).
- **A-p3-audit-02-10** [p3-audit-02] C-15: vertical-channel (VCT) and stacked 3D IGZO require conformal ALD rather than PVD sputtering — basis: device-physics judgment (replacement-type stacks and vertical holes are not line-of-sight); not source-verified.
- **A-p3-audit-02-11** [p3-audit-02] C-15: 'Micron skipping 4F2' rests on a weak blog snippet (sammyfans 2026-10-22); the kill does not depend on it alone (incumbent non-Chinese supply already meets the supply-security axis).

</details>

<details><summary><b>p3-audit-03</b> (7)</summary>

- **A-p3-audit-03-1** [p3-audit-03] Canonical comparison decks are the 4Q26 DDR5 contract ($15.99/GB), glut ($6.40/GB) and incumbent cost ($1.64/GB) from 01_LANDSCAPE 4.3; spot-based ratios on cards were restated against them — basis: 01_LANDSCAPE 10.4 #1.
- **A-p3-audit-03-2** [p3-audit-03] A heavy-ion RLAT campaign costs ~$30-70k (8-16 beam-hours, boards, rad engineer, travel) — basis: training-knowledge beam rates ~$1-2k/hr, UNVERIFIED this session.
- **A-p3-audit-03-3** [p3-audit-03] C-22 capital to production revenue ~$1.5-3M (2 MPW iterations, ~$0.5-0.6M mask set per 01_LANDSCAPE 6.2, qual/packaging ~$0.3-0.5M, 2-3 yrs of IC designer + test engineer ~$0.6-1M, Weebit license fee unknown) — basis: sum of listed components, ESTIMATE.
- **A-p3-audit-03-4** [p3-audit-03] A me-too product that at best ties incumbents on every buyer axis and loses on heritage/lead time is killed under R4 — basis: consistency with the batch_06 C-40 precedent.
- **A-p3-audit-03-5** [p3-audit-03] ICs rated/certified to >=5e3 Gy(Si) TID fall under ECCN 3A001.a.1 — basis: training knowledge, UNVERIFIED this session.
- **A-p3-audit-03-6** [p3-audit-03] 1-4 Mb NVM cannot hold most modern FPGA bitstreams (tens to hundreds of Mb) — basis: training knowledge.
- **A-p3-audit-03-7** [p3-audit-03] WebSearch quota used: 8 of 8.

</details>

<details><summary><b>p3-audit-04</b> (7)</summary>

- **A-p3-audit-04-1** [p3-audit-04] Used Optane PMem trades at ~$0.5-3/GB (128GB) and ~$0.6-1/GB (256GB) — basis: undated eBay/refurb listings in a 2026-11 search summary; listing dates and monthly volume unverified.
- **A-p3-audit-04-2** [p3-audit-04] VMware demand for PMem ends at vSphere 8 end of general support (2027-10-11) — basis: Broadcom KB 459135 and KB 326910 (PMem dropped in VCF 9.0); Broadcom has extended dates before.
- **A-p3-audit-04-3** [p3-audit-04] TSMC N5 HD SRAM bitcell = 0.021 um2 — basis: prior knowledge (TSMC IEDM 2019); used to show the 0.03 um2 SOT cell loses on density.
- **A-p3-audit-04-4** [p3-audit-04] 512MB LPDDR4X ≈ $10.5 now and ≈ $4 in the A-05 glut — basis: ~$21/GB mobile LTA cited in batch_12 (C-84), minus 60%.
- **A-p3-audit-04-5** [p3-audit-04] A new RRAM analog-IMC SoC entrant needs ~$50-150M (T3) to reach revenue — basis: edge-AI chip startup raises (Mythic, EnCharge) [ESTIMATE, prior knowledge].
- **A-p3-audit-04-6** [p3-audit-04] Treated C-26 as a SKU of C-62, not as a DUPLICATE kill, because C-62's verdict is not yet known and the buyer pitch (capacity expansion vs like-for-like replacement) differs.
- **A-p3-audit-04-7** [p3-audit-04] Octopart/Nexar are Altium properties — basis: prior knowledge; the Renesas-Altium completion itself is via search snippet.

</details>

<details><summary><b>p3-audit-05</b> (6)</summary>

- **A-p3-audit-05-1** [p3-audit-05] Canonical decks for all batch-05 $/GB comparisons: contract $15.99/GB, glut $6.40/GB, incumbent cost $1.64/GB; A3's $10-12 glut, $2.7 cost and $27 spot framings were corrected. Basis: 01_LANDSCAPE s4.3, s10.4 #1.
- **A-p3-audit-05-2** [p3-audit-05] A latency advantage of a standalone die (C-30/C-31/C-34/C-35) is treated as nil behind a DDR/CXL interface (~50-100 ns controller path). Basis: A3 card C-35 reasoning.
- **A-p3-audit-05-3** [p3-audit-05] C-31 cache-macro variant has no buyer at the named U.S. SOI flows (GF RF-SOI, SkyWater 90nm FD-SOI rad-hard), and dense-cache buyers get zero-mask gain cells (C-32). Judgment call that tipped C-31 to KILL under R4.
- **A-p3-audit-05-4** [p3-audit-05] RAAAM figures ($17.5M NXP-led Series A; 180nm-5nm silicon; GF FDX test vehicle; early-2027 design access; TSMC 2nm qualification) taken from search snippets only; WebFetch to techtime.news and anysilicon.com failed DNS.
- **A-p3-audit-05-5** [p3-audit-05] C-32/C-36 time-to-revenue raised to 36 months on ~6-month SkyWater MPW turns (Cadence/SkyWater 2026 run: Jan submission, July die) plus respin and qualification.
- **A-p3-audit-05-6** [p3-audit-05] C-36 gating unknown: whether SkyWater offers outside customers a characterized high-density 6T bitcell/PDK at Fab 25 65nm (Cypress-proprietary heritage). Left STILL-UNVERIFIED.

</details>

<details><summary><b>p3-audit-06</b> (8)</summary>

- **A-p3-audit-06-1** [p3-audit-06] Search snippets count as evidence only when tagged "(via search snippet)"; no primary page was opened (arxiv.org failed DNS; one WebFetch attempt, then stopped) — basis: task network rules.
- **A-p3-audit-06-2** [p3-audit-06] Accession 000117184326005079 is mapped to GSI's Q1 FY2027 release by filing sequence; the snippet gave the Q1 FY2027 figures — basis: search result set.
- **A-p3-audit-06-3** [p3-audit-06] Nantero is treated as "dormant, status unverified", not dead: two searches found no 2024-2026 news; C-40 is killed on R4, not FACT-COLLAPSE — basis: search results 2026-11-01.
- **A-p3-audit-06-4** [p3-audit-06] In a 1T1R cell on bulk 130nm CMOS, the access transistor and periphery cap operating temperature (~125-150 C) and set SEE/TID, so CNT-element tolerance gives no product-level edge — basis: standard device physics; not separately sourced.
- **A-p3-audit-06-5** [p3-audit-06] Minimum viable path for a new SRAM-only inference chip company ~$150-400M to first rack revenue (T3, not T4) — basis: Groq ~$300M raised by 2021, d-Matrix $110M+ 2023 (card evidence).
- **A-p3-audit-06-6** [p3-audit-06] GF 12LP+ SRAM density is ~2-3x below TSMC N4/Samsung SF4 — basis: training-data cell sizes (16nm-class 0.074 um2 vs N5 0.021 um2 in A3 notes).
- **A-p3-audit-06-7** [p3-audit-06] 4 K characterization of an existing gain-cell macro costs ~$50-150k (rented dilution-fridge time plus test board) — basis: estimate; university fridge time is typically priced per day/week.
- **A-p3-audit-06-8** [p3-audit-06] C-43 is marked DUPLICATE of C-32 on the assumption C-32 survives its own audit; if not, C-43 should be re-scored as KEEP_WITH_CORRECTIONS — basis: same cell, same nodes, same license model.

</details>

<details><summary><b>p3-audit-07</b> (8)</summary>

- **A-p3-audit-07-1** [p3-audit-07] A retired DDR4 RDIMM's opportunity cost is its used-module resale value ($4-11/GB in 4Q26, from amcompute $250-370 per 64GB and PCSP $2,300-5,500 per 512 GB), not DDR4 chip spot ($21-44/GB) — basis: x4 RDIMMs cannot be sold as consumer chips; 01_LANDSCAPE 10.4 #4 bars chip spot as a base case.
- **A-p3-audit-07-2** [p3-audit-07] Glut recovered-DDR4 value is $0.5-1.5/GB and severe-trough value $0.3-0.8/GB — basis: 01_LANDSCAPE 5.2 (us_backend.md 6.5 estimate) plus the 2023 DDR4 chip floor of $1.30.
- **A-p3-audit-07-3** [p3-audit-07] The small-vendor CXL card costs $2.34/GB (~$1.8k for 12x64GB) — basis: branch B model, not re-derived.
- **A-p3-audit-07-4** [p3-audit-07] A Pond-scale pod is 8 dual-socket servers with 1.5 TB each (12 TB); a 7-9% gross saving is valued at the canonical $20.31 (4Q26) and $8.12 (glut) RDIMM decks — basis: Pond 16-socket result; 01_LANDSCAPE 4.3.
- **A-p3-audit-07-5** [p3-audit-07] KTransformers decode scales roughly linearly with socket memory bandwidth (307 -> 614 GB/s) and inversely with active parameters (37B -> 32B) — basis: memory-bound MoE decode; measured R1 numbers in the KTransformers tutorial. Result ~20 tok/s (1 socket) and ~26 tok/s (2 sockets), vs the card's 23/46 roofline.
- **A-p3-audit-07-6** [p3-audit-07] Gen5 enterprise SSD sequential read is ~12 GB/s — basis: branch B's own 1.79 s to reload 20 GiB; so 8 SSDs roughly match 2x400G RDMA (~100 GB/s).
- **A-p3-audit-07-7** [p3-audit-07] R4 compares a card against every alternative its named buyer can actually get, including free software already in the buyer's stack (the same test batch 11 applied to C-77). An identical competitor product alone is scored as competition, not killed under R4.
- **A-p3-audit-07-8** [p3-audit-07] EPYC 9005 supports up to ~6 TB per socket at 2 DPC — basis: training knowledge [UNVERIFIED-T]; no search spent.

</details>

<details><summary><b>p3-audit-08</b> (8)</summary>

- **A-p3-audit-08-1** [p3-audit-08] LPDDR5X-8533 gives 68.3 GB/s per x64 package (8.533 GT/s x 64 b / 8), so 4-8 packages give 0.27-0.55 TB/s and 1 TB/s needs ~15 packages - basis: JEDEC LPDDR5X max rate; NVIDIA Grace 512-bit interface (~546 GB/s).
- **A-p3-audit-08-2** [p3-audit-08] C-52 minimum path to first revenue ~$50-90M (T3) - basis: N6/12LP mask set plus UCIe and LPDDR5X PHY/controller licences plus ~40 engineers for ~3 years plus package qualification [ESTIMATE].
- **A-p3-audit-08-3** [p3-audit-08] C-51 gross margin 25-40% - basis: 32-64 GB DRAM BOM is $512-1,023 at the $15.99/GB 4Q26 contract (01_LANDSCAPE 4.3), and an incumbent (SMART NV-CMM) sets the price.
- **A-p3-audit-08-4** [p3-audit-08] C-54 treats Qualcomm's 2025-06 acquisition of UPMEM as ending merchant PIM DIMM supply - basis: no evidence of post-acquisition third-party sales found; AiMX still a prototype at CES 2026. Reopen only if a vendor quotes PIM DIMMs or cards to an integrator.
- **A-p3-audit-08-5** [p3-audit-08] C-53 HBF attaches in-package over UCIe, so no board-level integration exists - basis: HBF spec coverage (TechRadar 2026, via snippet).
- **A-p3-audit-08-6** [p3-audit-08] C-56 is ruled the same as C-70 (batch_10): no evidence of a U.S.-origin DRAM premium - basis: 01_LANDSCAPE 0 item 7 and 7.3.
- **A-p3-audit-08-7** [p3-audit-08] C-55: Hailo-8 runs without external DRAM - basis: training knowledge [UNVERIFIED-T]; used only as context, not as a kill basis.
- **A-p3-audit-08-8** [p3-audit-08] WebSearch: 8 of 8 quota used. WebFetch attempts (arxiv.org, ir.penguinsolutions.com) both failed with DNS blocks; all new evidence is search-snippet grade.

</details>

<details><summary><b>p3-audit-09</b> (7)</summary>

- **A-p3-audit-09-1** [p3-audit-09] Alliance Memory is treated as a U.S.-based fabless legacy-DRAM incumbent running C-59's exact model; its Kirkland WA HQ (from the card) was not re-confirmed in search — basis: distributor line cards (via search snippet) confirm fabless, long-term support, DDR4 8Gb AS4C1G8D4.
- **A-p3-audit-09-2** [p3-audit-09] Micron's purchase of PSMC's Tongluo P5 fab is treated as signed (LOI, Jan-2026) but its closing is unconfirmed — basis: The Register 2026-01-20 (via search snippet); expected close 2Q26 not verified.
- **A-p3-audit-09-3** [p3-audit-09] The Sec. 5949 FAR rule is read from law-firm summaries of the 2026-02-17 proposed rule (certification after reasonable inquiry, no third-party audit, safe harbor for supplier certifications); no final rule found as of 2026-11-01 — basis: Crowell, Covington, Wiley, Mayer Brown snippets; FR text not opened.
- **A-p3-audit-09-4** [p3-audit-09] Used 32GB DDR4 RDIMM asking prices ($24-$319) are treated as noisy asking data, not sold medians; the O3 eBay sold-median kill test is still open — basis: listings via search snippet, dates mostly unclear.
- **A-p3-audit-09-5** [p3-audit-09] C-62 glut contribution set to the canonical 01_LANDSCAPE O3 1-6% rather than the card's instant-repricing 13-28% — basis: landscape is canonical per task.
- **A-p3-audit-09-6** [p3-audit-09] C-61 mid gross margin set to 25% because the card's own model is negative below ~8 OEMs and 27% at 10 OEMs; 25 OEMs treated as a year-4+ outcome — basis: C_notes.md Appendix A vault() function.
- **A-p3-audit-09-7** [p3-audit-09] DDR4 SPD bytes 350-351 = DRAM manufacturer ID — basis: Samsung RDIMM datasheet SPD table and coreboot ddr4.c (via search snippet).

</details>

<details><summary><b>p3-audit-10</b> (8)</summary>

- **A-p3-audit-10-1** [p3-audit-10] DDR3 JEDEC device density tops out at 8Gb and a DDR3 SO-DIMM carries at most 16 devices / 2 chip-selects, so 16GB is the practical DDR3 SO-DIMM ceiling — basis: training knowledge of JESD79-3 plus PCWorld snippet on the 16-chip SO-DIMM cap; used to kill C-66's 32GB DDR3L SO-DIMM.
- **A-p3-audit-10-2** [p3-audit-10] A me-too module maker buying 4Gb KGD + OSAT DDP is at a structural cost disadvantage to Intelligent Memory, which owns its 8Gb DDR3 component — basis: card model ($788 cost) vs incumbent vertical integration (flyer 10.2024).
- **A-p3-audit-10-3** [p3-audit-10] HBM stacks and HBM-on-interposer assemblies are scrapped on failure rather than reworked at production volume — basis: practitioner judgment [ESTIMATE]; secondary to the captive-customer kill of C-68.
- **A-p3-audit-10-4** [p3-audit-10] Micross Apopka's ~850 wafers/yr probe capacity (snippet) is treated as enough to cover the few-hundred-wafer U.S. legacy-DRAM KGD demand the card itself estimates — basis: card C-69 estimate and Micross facility page snippet.
- **A-p3-audit-10-5** [p3-audit-10] Without a written program requirement, U.S. buyers will not pay a premium for fully U.S.-origin COTS DRAM — basis: 01_LANDSCAPE.md §0 item 7 and §7.3 (TAA, BAA COTS exemption, Section 232 at 0%); used for the C-70 R1 kill.
- **A-p3-audit-10-6** [p3-audit-10] SkyWater's July 2026 acquisition by IonQ does not end its outside foundry service; it is a partner-priority risk, not a fact-collapse — basis: IonQ completion release snippet (2026-07-31).
- **A-p3-audit-10-7** [p3-audit-10] C-67 first revenue is moved to 24 months because a new module maker must win authorized die allocation on top of the 12–24-month rugged design-win cycle — basis: card text, plus zero authorized DDR4 stock (Findchips 2026-05, cited by C-72).
- **A-p3-audit-10-8** [p3-audit-10] C-72 first revenue is moved to 12 months because members are unlikely to pay fees before any supplier or distributor LOI — basis: no electronics GPO precedent found (search 2026-11-01); Suntsu snippet that authorized distributors follow makers' allocation.

</details>

<details><summary><b>p3-audit-11</b> (6)</summary>

- **A-p3-audit-11-1** [p3-audit-11] C-79 COGS uses 36-month straight-line depreciation, $250/month colo (the card's figure) and $100/month for IPs, bandwidth and spares — basis: typical small-colo line items; computed in scratchpad audit11_calcs.py
- **A-p3-audit-11-2** [p3-audit-11] C-79 glut case assumes a 40% rent cut as Hetzner/OVH reverse their 2026 RAM-driven price increases — basis: 2026 increases of up to 37% (heise) plus the DRAM glut line in 01_LANDSCAPE §10.3
- **A-p3-audit-11-3** [p3-audit-11] Used 64GB DDR4 RDIMM priced at $250-370 ($3.9-5.8/GB) — basis: amcompute appraisal data to Aug-2026 (via search snippet)
- **A-p3-audit-11-4** [p3-audit-11] C-74 kernel contractor ≈300 h at $150-200/h ≈ $45-60k, which pushes it from T0 to T1 — basis: market contractor rates [ESTIMATE]
- **A-p3-audit-11-5** [p3-audit-11] C-76 judged a DUPLICATE of C-50: the same stranded-memory pooling mechanism and axis; software license vs appliance is a business-model lens (mission §E), not a separate concept
- **A-p3-audit-11-6** [p3-audit-11] C-77 killed on R4: the named buyer's real alternative is free Linux swap/zswap writeback on the same NVMe, so a paid NAND-as-RAM license wins no axis

</details>

<details><summary><b>p3-audit-12</b> (8)</summary>

- **A-p3-audit-12-1** [p3-audit-12] C-81 killed under R4-NO-WINNING-AXIS, not as "weak business": a marketplace's buyer pays for liquidity and trust; Mobius Materials (VA, $3M seed Dec-2025, hundreds of OEM/CM users, in-house inspection VA/HK) already offers every card feature, so a cold-start clone wins no axis — basis: Digital Commerce 360 (via search snippet).
- **A-p3-audit-12-2** [p3-audit-12] C-82 and C-83 killed under NOT-A-VENTURE: affiliate price-tracker and paid newsletter are shortage content monetization, which mission §3E limits to "a bridge revenue line, never the venture" — basis: MISSION_PROMPT.md line 90; cards' own "no business at the end" / "bridge only".
- **A-p3-audit-12-3** [p3-audit-12] C-85 DIY comparison uses E's own model inputs (2,400 DIMMs, 1.5%/DIMM-yr replacements, 32GB at $4.7/GB, $18 ship, 2% pool): ~$6.1k/yr + $7.2k one-time pool vs $21.6k/yr fee (3.6x) — basis: E_notes.md §10 script, recomputed in python3.
- **A-p3-audit-12-4** [p3-audit-12] C-84 audit margin set to 45-65% assuming a contracted embedded-Linux engineer at ~$120-180/h — basis: founder is not an embedded engineer (card's own founder note); rate is an ESTIMATE.
- **A-p3-audit-12-5** [p3-audit-12] C-80 GM midpoint lowered 80->75 for data-licence risk (distributor/Nexar API terms vs re-display in third-party SaaS) — basis: UNVERIFIED-training; terms not checked this session.
- **A-p3-audit-12-6** [p3-audit-12] C-86 time-to-revenue raised 9->12 months because each license needs both contract parties (and federally a pricing office under DLAD 16.203-4's BLS-first rule) to accept a new index — basis: acquisition.gov DLAD/PGI text (via search snippet).
- **A-p3-audit-12-7** [p3-audit-12] Crucial System Scanner/Advisor post-exit status left STILL-UNVERIFIED (no search spent); C-82 kill does not depend on it.
- **A-p3-audit-12-8** [p3-audit-12] Search budget: 8/8 WebSearch calls used; 1 WebFetch attempted (lewissilkin.com, host not allowed).

</details>

<details><summary><b>p3-audit-13</b> (6)</summary>

- **A-p3-audit-13-1** [p3-audit-13] C-87 is killed under R1-UNSUPPORTED because its value claim (that hedgers will trade a DRAM derivative) is contradicted by failed precedents (SGX 2003, Semicon Exchange, SFX, CBOT/NYMEX/PSE studies). The SGX contract's actual fate is unconfirmed — basis: Risk.net, Mondo Visione and EDN search snippets; no 2026 DRAM price contract surfaced.
- **A-p3-audit-13-2** [p3-audit-13] C-88 and C-89 are killed as NOT-A-VENTURE because their P&L is a pure function of the DRAM price path (a short call and a long spot position) — basis: e_estimates sections 2-3; Black-76 ATM premium reproduced by hand (2N(0.22)-1 = 17.4% before discounting).
- **A-p3-audit-13-3** [p3-audit-13] C-90 is killed under R4 because the lessor has no allocation and a higher cost of capital than the GPU-backed lenders that already finance neocloud servers, memory included — basis: 2026 CoreWeave, Lambda, Nebius and Sharon AI facilities (search snippets); the card's 14% lessor IRR.
- **A-p3-audit-13-4** [p3-audit-13] C-90's "15% gross margin" was an IRR. Re-estimated at ~8% net spread from the e_estimates section 4 inputs ($1,600 buy, $48.83 x 36, $260 residual) and an assumed ~10% startup facility cost — basis: [ESTIMATE].
- **A-p3-audit-13-5** [p3-audit-13] C-91 and C-92 are kept because founder-fit, capital and crowding are scoring matters, not kill rules (task instruction). Whether a Taiwanese specialty OCM would authorize a startup as an aftermarket manufacturer is STILL-UNVERIFIED.
- **A-p3-audit-13-6** [p3-audit-13] C-92's planning volume is 20-40 lots/month in years 1-2 (mid GM 22%), not 60 — basis: entrenched accredited incumbents (SMT Corp CT, Micross FL) and e_estimates section 6 volume rows.

</details>

<details><summary><b>p3-audit-14</b> (7)</summary>

- **A-p3-audit-14-1** [p3-audit-14] A newcomer cannot join NASA SEWP VI before an on-ramp; none was found scheduled as of 2026-11-01 — basis: SEWP VI awarded Jun-2026 with ordering from 2026-11-01 (Federal News Network, via snippet); the on-ramp is mentioned in NASA's deck without a date.
- **A-p3-audit-14-2** [p3-audit-14] GSA MAS normally needs 2 years of corporate experience or a Startup Springboard waiver — basis: training knowledge [UNVERIFIED-training]; drives the C-93 TTR correction to 20 months.
- **A-p3-audit-14-3** [p3-audit-14] STTR requires the small business to perform >=40% of the work and the research institution >=30%, and FFRDCs such as Sandia qualify as research institutions — basis: training knowledge of SBA SBIR/STTR policy [UNVERIFIED-training].
- **A-p3-audit-14-4** [p3-audit-14] The SOP 50 10 8.1 'limited sources' treatment (seller notes plus <20% minority-investor equity sharing a 50% cap on the 10% injection) is taken from one secondary blog — basis: Beancount 2026-09-23 (via snippet); not checked against SBA text.
- **A-p3-audit-14-5** [p3-audit-14] A new 20nm-class crosspoint PCM production line costs >$1B — basis: TI bought the used Lehi fab for ~$1.5B (cash plus tools) in 2021 (card/AnandTech cross-ref); a new line costs more.
- **A-p3-audit-14-6** [p3-audit-14] Treating a services packaging of an existing surviving card's opportunity as DUPLICATE (C-97 vs C-49) — basis: the C-76/C-50 precedent in batch_11 and batch_07's own overlap flag.
- **A-p3-audit-14-7** [p3-audit-14] Google Patents and USPTO Patent Center show patent status, maintenance-fee and anticipated-expiry data free — basis: training knowledge [UNVERIFIED-training]; Unified Portal free tier verified via snippet.

</details>

<details><summary><b>p3-devmodel</b> (19)</summary>

- **A-p3-devmodel-1** [p3-devmodel] One area-based cost equation for every device: $/GB = wafer_cost / (usable_mm2 x density / 8 x yield) + test_pkg $/GB. Basis: the task spec (mission section 3A). The A2/A3 die-based scratch models give the same answers to within a few percent.
- **A-p3-devmodel-2** [p3-devmodel] Usable wafer area = gross dies per wafer of a 100 mm2 reference die x 100 mm2, using the Chiplet Actuary GDPW form with edge 3 mm and scribe 0.08 mm from `cost_inputs.json`. That is 0.854 of a 300mm wafer and 0.790 of a 200mm wafer. Basis: matches A3's "85% usable" convention. A calibration row reproduces the dram_cost_stack DDR5 1b cost to within about 3%.
- **A-p3-devmodel-3** [p3-devmodel] When a filing gives both a cell area and a die density, the filed die density is used and the array efficiency is back-solved (printed as eff_used). Basis: filed densities include measured die data (3D XPoint Gen1/Gen2, Everspin 1Gb) that the cell formula overstates by up to 1.75x.
- **A-p3-devmodel-4** [p3-devmodel] Wafer cost, yield and test/package come from the branch filings unchanged. They are not harmonised to the canonical $/wafer. Basis: the filings are the assigned inputs. The -30% wafer sensitivity roughly harmonises branch DRAM-class wafers ($5.5-7k) with the canonical 1b wafer (about $3.8k).
- **A-p3-devmodel-5** [p3-devmodel] Sensitivity is wafer cost x0.7/x1.3 and yield 0.50-0.95 (task spec). "Cannot win on $/GB under any sensitivity" means the best case (x0.7, 0.95) is at or above the A-05 glut price. Tiers: A <= DDR5 incumbent cost, B < glut, C < Q4-2026 contract, D above contract.
- **A-p3-devmodel-6** [p3-devmodel] DDR5 reference numbers are imported live from `models/dram_cost_stack.py` `ddr5_reference()`. During this run, Phase-1b agent v4-cost was revising that model. The live values on 2026-11-01 17:5x UTC were cost $1.484, contract $20.367, glut $8.147 and severe $2.037 per GB, vs the brief's $1.641 / $15.993 / $6.397 / $1.599. Section 5 of the output reports verdicts under both decks and a list that holds on either deck. Basis: the task said to use the model's exact values.
- **A-p3-devmodel-7** [p3-devmodel] Test and package stay fixed per GB across the yield sensitivity. Basis: simplicity. Probe cost scales weakly with yield, which is second-order next to wafer cost/yield.
- **A-p3-devmodel-8** [p3-devmodel] A1-11 SunRise 3D NOR has no density filed. Default 0.39 Gb/mm2 (DDR5 1b, 16Gb/41 mm2), on the reading that the claim "DRAM-like $/GB" implies DRAM-parity density. Basis: no public silicon data. The concept is Rule-1 UNSUPPORTED anyway.
- **A-p3-devmodel-9** [p3-devmodel] A3-12 2D-material gain cell has no wafer cost and no yield. Defaults: $1,400 SkyWater 200mm 130nm wafer + $1,000 2D-tier adder, yield 0.30, and test/package at $0.015/mm2 of die ($/GB = 0.12/density). Basis: TRL 2-3 with no production line. The concept is Rule-1 UNSUPPORTED.
- **A-p3-devmodel-10** [p3-devmodel] A2-11 Optane salvage has no fab. The "wafer cost" is replaced by an acquisition cost of $1.40/GB (midpoint of A2's [UNVERIFIED] $0.8-2/GB), and yield is the health-test pass rate (0.9 as filed). Basis: A2 filing.
- **A-p3-devmodel-11** [p3-devmodel] A3-13 printed labels: $/GB = $0.10 per 20-bit label / yield. Basis: the A3 filing's wafer_cost_basis.
- **A-p3-devmodel-12** [p3-devmodel] A1-03 display glass uses 90% of a 5.5 m2 Gen-8.5 sheet at the filed $500 per sheet. Basis: A1 filing; utilisation is my estimate.
- **A-p3-devmodel-13** [p3-devmodel] Embedded, compute and buyer rows keep the filed test+package of 0 (A1-01, A1-10, A2-08, A2-09, A2-14, A3-03, A3-04, A3-08, A3-10, A3-14), so their $/GB is an area-equivalent silicon cost. Basis: filings say the cost lands in the host SoC.
- **A-p3-devmodel-14** [p3-devmodel] tmp_id variants map to their base id: A1-02 second row -> "A1-02s", A3-02b -> C-31, A3-06-nXX -> C-35. A2-12 maps to C-51 (absorbed into B-08). Basis: `tmp_to_id.json` and the dedup map.
- **A-p3-devmodel-15** [p3-devmodel] Two variants are excluded from concept verdicts but still costed. A3-02b (Kilopass VLT) is excluded because the filing says "do not use as a live option". A1-02s (300mm 28nm BEOL) is excluded because no U.S. foundry offers that line and C-02 is defined on a U.S. 200mm line.
- **A-p3-devmodel-16** [p3-devmodel] Added supplementary rows for silicon-making concepts outside branch A. C-58 uses dram_cost_stack ddr4_8g_1x_new, C-59 uses ddr3_4g_fdry, and C-71 uses the C_notes Appendix A figures: 116 mm2, 137/228 good dies, $2,000 wafer, $15 package+test per unit. Basis: "every device/material concept".
- **A-p3-devmodel-17** [p3-devmodel] The non-$/GB axis is derived by keyword from each card's `wins_axis` text plus the device retention field. There are two overrides. C-02 is set to "standby power (refresh only)" because the card says "none for commodity buyers... refresh power only". C-05 is set to "none ($/GB-only bet)". Basis: card text.
- **A-p3-devmodel-18** [p3-devmodel] F-RAM street reference is $1/Mbit = $8,192/GB, with a range up to $4/Mbit. Basis: A1-12 filing notes "~$1-4/Mbit" [ESTIMATE]. NOR reference is $40/GB [UNVERIFIED, cost_inputs].
- **A-p3-devmodel-19** [p3-devmodel] Gb is decimal in A1/A3 and binary in A2 and in the DDR5 die capacities. I did not convert, because the difference (<=7.4%) is inside the yield and wafer sensitivity band.

</details>

<details><summary><b>p3-writer</b> (11)</summary>

- **A-p3-writer-1** [p3-writer] Kill-rule definitions in 03_SCORING.md §1.1 are reconstructed from how the 14 auditors applied them, because no file defines them in one place — basis: research/phase3/verify/*.json, research/assumptions/p3-audit-*.md.
- **A-p3-writer-2** [p3-writer] Kill reasons in §2 are condensed from `kill_reason` in concepts_master.json; numbers keep the deck the auditor used ($15.99 / $6.40 / $1.64 per GB), not the live device-model deck — basis: concepts_master.json; device_cost_output.md §5.
- **A-p3-writer-3** [p3-writer] Concept names in the §2 register drop editorial suffixes such as "(tempting, dead)"; short names are used in §4–§7 tables for width — basis: readability only; ids are unchanged.
- **A-p3-writer-4** [p3-writer] Per-criterion justifications in §4.1 are condensed from the scores.csv `*_why` text, and the founder is referred to as they/them even where the source text says "he" — basis: task instruction.
- **A-p3-writer-5** [p3-writer] The "side/feature/lifestyle/SKU/gig/lead-gen/not a venture" flag in §6 is a regex over all three lenses' `one_line_view` text; 12 of the top 15 match — basis: research/phase3/scores_raw/*.json.
- **A-p3-writer-6** [p3-writer] The 5-year revenue-ceiling bands in §6 are my own estimates, not scores. They are built from card pricing and customer counts (C-64 $1.5–12k/month × 37 customers; C-86 $0.3M ARR; C-80 ~$24k MRR; C-85 25 × $21.6k; C-74 $500–2k/month per 50–200 nodes) and from scorer ceilings (C-12 "low $100ks/yr"; C-33 "<$0.5-1M ARR") — basis: concepts_master.json, scores_raw one_line_view, verify batch_02.
- **A-p3-writer-7** [p3-writer] C-75 services ceiling assumes ~6–12 engagements per year at $15–40k for a part-time founder — basis: C-75 card ttr text ($15–40k engagement); capacity is my judgment.
- **A-p3-writer-8** [p3-writer] C-48 revenue band assumes 20–50 boxes per year at ~$25–45k each — basis: the card's DRAM BOM of $15.6–31.2k per box plus CPU/GPU; volume is my judgment.
- **A-p3-writer-9** [p3-writer] The "commodity software" and "ideal T2 device" profiles in §5 are hypothetical, used only to show the structural bias of the weights — basis: arithmetic with models/scoring.py `weighted()`.
- **A-p3-writer-10** [p3-writer] The coverage proof uses the union of the three top-10 lists (11 ids), which is stricter than selection.json's wording — basis: scores.csv ranks.
- **A-p3-writer-11** [p3-writer] All URLs cited in 03_SCORING.md come from auditors' `new_evidence` entries and are [REPORTED] (search snippets), except the VLSIDA GitHub repository, which an auditor opened via git — basis: research/phase3/verify/*.json; logged in research/sources/p3-writer.jsonl.

</details>

### Phase 4 — deep dives

<details><summary><b>p4-legacy-dram-diebank</b> (29)</summary>

- **A-p4-legacy-dram-diebank-1** [p4-legacy-dram-diebank] Month 1 of every model = 2026-11; m15 = 2028-01 (start of the A-05 glut); m36 = 2029-10; the 10-year view runs to m120 = 2036-10 — basis: task spec and ASSUMPTIONS A-05.
- **A-p4-legacy-dram-diebank-2** [p4-legacy-dram-diebank] Legacy DDR4/DDR3 packaged price tracks the DDR5 contract deck at parity ($20.37/GB in Q4-2026) — basis: 01_LANDSCAPE §10.4 #4 keeps parity in the cost model; DDR4 spot ($46/GB, 2026-10-20) is never used as a base case.
- **A-p4-legacy-dram-diebank-3** [p4-legacy-dram-diebank] BASE legacy price: flat to m14, then −35% linear to m26 ($13.24/GB), flat to m36 — basis: house call "turn 2028"; DDR4 collapses first and hardest (01_LANDSCAPE §3.3); BofA −10% blended ASP is a floor on the decline, not the legacy number.
- **A-p4-legacy-dram-diebank-4** [p4-legacy-dram-diebank] GLUT: legacy price falls to $8.15/GB (−60%) over m15–m17; SEVERE: to $2.04/GB over m15–m20 — basis: ddr5_reference() glut/severe decks applied to legacy at parity.
- **A-p4-legacy-dram-diebank-5** [p4-legacy-dram-diebank] Long-run legacy price (all scenarios) moves linearly from the m36 level to $3.00/GB by m60 and holds — basis: ~2.3× the 2023 DDR4 trough ($1.30/GB) and ~2.3× depreciated DDR4 cost ($1.284/GB, models/dram_cost_stack.py), i.e. a ~57% cycle-average gross margin for the maker. No source gives a long-run legacy price; this is the most consequential judgment in the 10-year view.
- **A-p4-legacy-dram-diebank-6** [p4-legacy-dram-diebank] Bank die cost (wafer purchase) = 0.75 × packaged $/GB per good die; market KGD = 0.85 × packaged $/GB — basis: wafer < KGD < packaged; no OCM quote obtained (kill-experiment item).
- **A-p4-legacy-dram-diebank-7** [p4-legacy-dram-diebank] Bank = 10 × 300 mm DDR4 8Gb wafers, 1,251 good die/wafer (45 mm², 85% yield) — basis: research/phase1/us_backend.md §4.2 table.
- **A-p4-legacy-dram-diebank-8** [p4-legacy-dram-diebank] U.S. low-volume pull cost per die: re-probe $1.50 + package $6.00 + memory test $4.00, pull yield 95% — basis: no OSAT quote found (QP Technologies publishes none); Asian volume packaging is <$1, U.S. quick-turn hi-rel is far higher; ±30% in sensitivity.
- **A-p4-legacy-dram-diebank-9** [p4-legacy-dram-diebank] Aftermarket price = 2.5× the part's packaged price at EOL (bank purchase), compressed ×0.9 in GLUT and ×0.8 in SEVERE — basis: 1.5–5× authorized-aftermarket range (research/phase1/us_backend.md §5.3, itself an estimate); centre-low because JEDEC DRAM is substitutable (DSPO 2024: 2,809 simple substitutes vs 1,268 life-of-need buys).
- **A-p4-legacy-dram-diebank-10** [p4-legacy-dram-diebank] Bank sell-through starts 18 months after purchase and runs 15%/yr of the initial bank (BASE), 11% (GLUT), 8% (SEVERE) — basis: E-07 base case (90% over years 3–8, research/phase2/E_notes.md §5); cheaper substitutes in a glut shrink the locked-buyer pool.
- **A-p4-legacy-dram-diebank-11** [p4-legacy-dram-diebank] Bank storage = max(3%/yr of remaining basis, $5k/yr) at a Micross-type consignment vault — basis: Micross publishes an annual carrying-fee model but no rates; E-07 used 1.5%/yr; doubled for small-customer pricing.
- **A-p4-legacy-dram-diebank-12** [p4-legacy-dram-diebank] Managed die-bank program (consignment, OEM owns die): $4,000 LTB study, $750/month program fee, 4% agency fee on LTB die value, $1.00/unit pull-coordination margin on 80 units/program/month, $60/program/month direct cost, 1%/month program churn — basis: DD2 priced LTB studies at $3,500 and software at $249/month; Micross sells the vault directly, so the founder's fee must sit below the OEM's in-house cost; no buyer quote.
- **A-p4-legacy-dram-diebank-13** [p4-legacy-dram-diebank] Funnel: 4 qualified DMSMS/OEM conversations per month part-time (15 h prospecting at ~4 h each), ×2.5 full-time; 10% buy a study; 35% of studies become programs (one-month lag) — basis: DD2's 12% trial conversion was attacked as optimistic (RT-VC-DD2-06); held lower.
- **A-p4-legacy-dram-diebank-14** [p4-legacy-dram-diebank] New-business demand multiplier: BASE 1.0 (0.9 from m27), GLUT 0.75 and SEVERE 0.60 from m15 — basis: fewer LTBs when supply is abundant, partly offset by more EOL notices in a downturn (Z2Data 2026: record EOL rates).
- **A-p4-legacy-dram-diebank-15** [p4-legacy-dram-diebank] Channel (rep) agreement with a long-lifecycle DRAM OCM signed at m9; 0.3 new accounts/month part-time (×2.5 FT); $40k/yr purchases per account at 2026 prices, scaling with legacy price; 5% commission paid 2 months in arrears; 1.5%/month account churn — basis: Intelligent Memory signed Sourceability and Flip as partners in 2026 (Evertiq 2026-10-06), so OCMs are adding channels; commission rate is a typical rep rate, unsourced.
- **A-p4-legacy-dram-diebank-16** [p4-legacy-dram-diebank] Founder capacity 65 h/month part-time, 170 h full-time; service load 2 h/program/month, 10 h/study, 0.5 h/account/month; ops hire adds 80 h after Stage-1 — basis: ASSUMPTIONS A-03 (~15 h/week).
- **A-p4-legacy-dram-diebank-17** [p4-legacy-dram-diebank] Part-time fixed costs $680/month (CRM/Sales Navigator, E&O ~$110, accounting, web, travel accrual) plus $2,500 per DMSMS-conference trip at m10/m22/m34 and $8,500 one-off in m1 (kill experiment $6,000, LLC and rep-agreement legal $2,500) — basis: E&O per sources/p5r-memory-efficiency.jsonl (Insureon ~$67–110/month); others estimates.
- **A-p4-legacy-dram-diebank-18** [p4-legacy-dram-diebank] Plan A full-time trigger: trailing-3-month contribution ≥ $10,000/month and cash ≥ $30,000; salary $10,000 + 10% burden — basis: consistent with round-1 models.
- **A-p4-legacy-dram-diebank-19** [p4-legacy-dram-diebank] Plan B Stage-1 raise $1.5M at m18 and Stage-2 raise $4.0M at m30, both conditional on gates (OCM letter + ≥3 locked-die LOIs; ≥1 MCM evaluation LOI); bridges are injected automatically to keep $50k cash and are reported as extra external capital — basis: judgment; no investor conversation.
- **A-p4-legacy-dram-diebank-20** [p4-legacy-dram-diebank] Plan B staff: founder FT from m18 ($11k loaded), quality/ops manager m19+ ($11k), test-engineering contractor m19–m30 ($6k), 2 MCM engineers m30+ ($36k), BD m31+ ($16k), ops tech m38+ ($8k), second BD and production/quality engineer m60+ ($30k); overhead $4k/month from m18, insurance $1.5k/month from m20, ITAR registration $250/month from m30, AS9120B certification $35k (m21–m25) plus $8k/yr surveillance — basis: estimates; ITAR fee from prior knowledge, not verified this session.
- **A-p4-legacy-dram-diebank-21** [p4-legacy-dram-diebank] Bank package/test NRE $120k for the first family (FBGA package qualification, memory-ATE test program, JEDEC qual lot), $40k for each later bank — basis: no OSAT quote; kill-experiment item.
- **A-p4-legacy-dram-diebank-22** [p4-legacy-dram-diebank] Hi-rel x72 ECC DDR4 MCM: NRE $1.4M over 18 months from m30; 100 evaluation units at $1,200 in m48; design-ins from m60 at 2/yr (×0.85 GLUT, ×0.70 SEVERE), each 300 units/yr for 8 years with 0.5%/month attrition; ASP $900; unit cost = (9 die + $60 substrate + $80 assembly + $150 screening/burn-in/test) ÷ 0.91 module yield — basis: C-65 card (~$457 unit cost, $800–3,000 ASP), scorers' view that an entrant sits at the ~$800 end, veteran_3 compounded yield (99% KGD → ~91% module).
- **A-p4-legacy-dram-diebank-23** [p4-legacy-dram-diebank] Tax: 30% on positive taxable income with loss carry-forward; inventory capitalised and expensed on sale; unsold bank die written off at m120 — basis: red-team RT-VC-DD1-07.
- **A-p4-legacy-dram-diebank-24** [p4-legacy-dram-diebank] Collections: services net-30 (1-month lag); commissions 2-month lag; hardware net-45 (2-month lag) — basis: red-team RT-VC-DD1-04 cash-cycle finding.
- **A-p4-legacy-dram-diebank-25** [p4-legacy-dram-diebank] Year-10 enterprise value = 1.5× year-10 revenue — basis: judgment for a sub-scale hi-rel component business; no transaction multiple was found this session.
- **A-p4-legacy-dram-diebank-26** [p4-legacy-dram-diebank] Acquisition variant: target like Resurgent (≈30 staff) at ~$200k revenue/employee → $6.0M revenue, 15% EBITDA (10% GLUT, 6% SEVERE), 5.0× EBITDA price, 80% SBA 7(a) at 10.5% over 10 years, 10% seller note, 10% equity — basis: Resurgent headcount (Business Wire 2023-02-21); revenue/employee, margin, multiple and SBA terms are estimates (SBA 7(a) $5M cap from prior knowledge, not verified this session).
- **A-p4-legacy-dram-diebank-27** [p4-legacy-dram-diebank] DMSMS memory share: ~10% of DSPO-tracked cases are memory — basis: judgment; used only for the ceiling sanity check.
- **A-p4-legacy-dram-diebank-28** [p4-legacy-dram-diebank] Judgment: the DFARS moat is real but does not bind for commodity JEDEC DRAM, because most DMSMS DRAM cases resolve as simple substitutes; the die bank only has value where the die is locked (hi-rel MCM, DO-254 avionics, FDA-validated devices).
- **A-p4-legacy-dram-diebank-29** [p4-legacy-dram-diebank] Judgment: Taiwanese specialty makers (Winbond, ESMT, Etron, Nanya) are beneficiaries of the 2026–27 legacy shortage, not exiters (Winbond sold out through 2027; customers seek LTAs to 2030), so no EOL-driven authorization opportunity from them is expected before the glut; the near-term EOL wave comes from Samsung, SK hynix and Micron, which have not authorized startups.

</details>

<details><summary><b>p4-lifecycle-intel</b> (19)</summary>

- **A-p4-lifecycle-intel-1** [p4-lifecycle-intel] Model month 1 = 2026-12; the kill experiment runs in Nov 2026 — basis: today is 2026-11-01; experiment is <30 days.
- **A-p4-lifecycle-intel-2** [p4-lifecycle-intel] Founder deploys $40k and ~15 h/week until trailing-3-month (gross profit − opex) covers a $10k/month loaded salary — basis: ASSUMPTIONS A-03.
- **A-p4-lifecycle-intel-3** [p4-lifecycle-intel] The physical consignment vault from C-61 is NOT part of the venture; only LTB-sizing software and paid LTB studies are — basis: C-61 card's own model loses money below ~8 OEMs, needs AS6081 operator and insurance; Rochester/Micross/Semitron/Astute and a ~$5k N2 cabinet cap the fee.
- **A-p4-lifecycle-intel-4** [p4-lifecycle-intel] C-72 pooled forecasting is a free Pro-tier feature with zero modelled revenue — basis: supplier acceptance of a no-title co-op LTA is unverified and no electronics GPO exists (C-72 audit); Avnet says allocation favors purchase history and commitments.
- **A-p4-lifecycle-intel-5** [p4-lifecycle-intel] C-29 NVM cross-reference is a feature of the lifecycle module, scoped to EEPROM/NOR/NVSRAM -> F-RAM/MRAM; DRAM EOLs get same-technology alternates only — basis: C-29 audit (no emerging NVM replaces DDR3/DDR4; Everspin ~$821/GB).
- **A-p4-lifecycle-intel-6** [p4-lifecycle-intel] SaaS Team $249/mo, Pro $649/mo, 25% Pro mix, blended net ARPA $335/mo after a 10% contributor discount on 40% of accounts — basis: SiliconExpert BOM Manager Essentials $250/mo (via search snippet); Accuris $6,000 ACV minimum; a memory-only tool cannot price above SiliconExpert's all-parts entry tier.
- **A-p4-lifecycle-intel-7** [p4-lifecycle-intel] Index licences $6k (standard) / $24k (enterprise, redistribution/API), 15% enterprise mix — basis: E-02 model; DRAMeXchange Silver $5k, Gold $11k, Platinum $18-30k, Diamond $30-55k/yr (GII reseller listings, via search snippet).
- **A-p4-lifecycle-intel-8** [p4-lifecycle-intel] The index is built from contributed memory PO prices (panel) plus distributor quotes sampled under written permission, NOT from the Nexar/Octopart API — basis: Octopart API terms prohibit historical-trend use and caching >24h (via search snippet); TrendForce data is not redistributable.
- **A-p4-lifecycle-intel-9** [p4-lifecycle-intel] Trial->paid conversion 12%; qualified trials start at 6/month, +2/month, capped at 25 (part-time) / 60 (full-time) — basis: B2B opt-in trial norms 10-25%; low end because of SiliconExpert/Octopart substitutes; capacity of a 15 h/week founder.
- **A-p4-lifecycle-intel-10** [p4-lifecycle-intel] 40% of SaaS demand is lifecycle-driven (price-insensitive); 60% is price/allocation-driven and scales with DDR5 price relative to Q4-2026 — basis: AdvaMed survey (63% allocation/scarcity, 88% price increases); C-80 audit (buy/hold alerts worthless in glut).
- **A-p4-lifecycle-intel-11** [p4-lifecycle-intel] Base churn 2.0%/month; price-motivated accounts add up to +8%/month at zero urgency — basis: SMB SaaS norms; scorers' cycle score of 1 for C-80.
- **A-p4-lifecycle-intel-12** [p4-lifecycle-intel] Index demand scales with the 3-month absolute DDR5 price move (saturating at 15%) with a 35% floor; licence churn 0.8%/month, 1.5% when the market is flat after m24 — basis: E-02 two-sided logic; Lewis Silkin 2026-05 (clauses built for 3-5%/yr moves); clauses embedded in multi-year contracts persist.
- **A-p4-lifecycle-intel-13** [p4-lifecycle-intel] EOL/PDN intensity rises 25% (glut) / 40% (severe) from 2028, lifting LTB study demand — basis: 2023 downturn pressure on legacy DRAM makers (Nanya/Winbond, DigiTimes 2023-02-22); makers exit legacy lines faster when margins fall.
- **A-p4-lifecycle-intel-14** [p4-lifecycle-intel] BASE price path: Q4-2026 $20.37/GB, +4/+6/+7/+7% through 2027, then -15% by Dec-2028 and -20% by Dec-2029; GLUT reaches $8.15 by Dec-2028; SEVERE reaches $2.04 by Dec-2028 — basis: canonical ddr5_reference(); TrendForce via TechNews 2026-07-09 (rises through 2H27, narrowing); landscape house call (turn 2028).
- **A-p4-lifecycle-intel-15** [p4-lifecycle-intel] Nexar Standard ~$300/mo and Pro ~$1,000/mo; display/redistribution licence ~$1,000/mo from m12 — basis: Nexar publishes tier limits (100/2,000/15,000 matched parts) but not prices; Octopart terms restrict pricing use by distribution-market software developers. UNVERIFIED; the largest COGS risk.
- **A-p4-lifecycle-intel-16** [p4-lifecycle-intel] Support is a cash cost ($60/h contractor, 0.5 h/account-month) even while the founder is part-time — basis: conservative; keeps GM honest.
- **A-p4-lifecycle-intel-17** [p4-lifecycle-intel] U.S. SMB OEM/EMS universe with memory in BOM and $1-50M BOM spend ≈ 6,000 firms — basis: order-of-magnitude judgment (NAICS 334/3345/3391 firms with ~20-500 staff); unsourced.
- **A-p4-lifecycle-intel-18** [p4-lifecycle-intel] LTB study $3,500, 30% COGS, attach 1.5% of accounts/month + 0.3 inbound/month — basis: 1.5-2 analyst-days; J-STD-048-style 6-month LTB windows (MaxLinear, Boréas policies) create recurring deadlines.
- **A-p4-lifecycle-intel-19** [p4-lifecycle-intel] Founder sales time imputed at 1 h/trial x $75/h for a fully loaded CAC — basis: demo + follow-up per trial; reported alongside the cash CAC.

</details>

<details><summary><b>p4-memory-efficiency</b> (19)</summary>

- **A-p4-memory-efficiency-1** [p4-memory-efficiency] Month 1 of the model is 2026-11 and month 36 is 2029-10. The DRAM turn starts in 2028-01, which is month 15, so it lands *before* month 18. — basis: 01_LANDSCAPE F2 (downturn most likely 2028); task spec (GLUT from 2028-Q1).
- **A-p4-memory-efficiency-2** [p4-memory-efficiency] BASE scenario: the 64GB DDR5 RDIMM holds at $25.78 per user-GB through 2027, then falls 30% over 2028 and stays flat. — basis: midpoint between BofA's −10% 2028 ASP call and the A-05 −60% glut.
- **A-p4-memory-efficiency-3** [p4-memory-efficiency] GLUT scenario: the price ramps over 12 months from 2028-01 down to $10.31 per user-GB (A-05). SEVERE scenario: the same ramp, down to $2.04/GB component, which is $2.58 per user-GB at the RDIMM/component ratio of 1.266 from `ddr5_reference()`. — basis: 2018-19 analog, −62.5% in about 4 quarters.
- **A-p4-memory-efficiency-4** [p4-memory-efficiency] Used DDR4 RDIMM is worth $4.45/GB (midpoint of $3.1–5.8). It falls 30% in BASE, 50% in GLUT (floored at the $1.30 trough) and to $1.30 in SEVERE. — basis: amcompute via p3-audit-11; A-05 (DDR4 falls less in %).
- **A-p4-memory-efficiency-5** [p4-memory-efficiency] C-74 frees **10% of installed RAM** on a third-party fleet. That sits between Google's ~5% of fleet RAM from zswap and Meta TMO's 20–32%. TMO's figure relies on in-house application tuning plus SSD offload, which a vendor working on a stranger's fleet will not get on day one. — basis: Google ASPLOS'19/LPC talk; TMO ASPLOS'22; DAMON_RECLAIM lab results of 32–40% (not production).
- **A-p4-memory-efficiency-6** [p4-memory-efficiency] The reference node has 512 GB of RAM, of which 60% of node-GB is DDR5 (the targeting rule) and 40% is DDR4 valued at used-DIMM prices. A customer has 80 nodes on average. — basis: the C-74 card's reference fleet and the p3-audit DDR4 correction.
- **A-p4-memory-efficiency-7** [p4-memory-efficiency] The C-74 price is a **30% share** of the deferred-DRAM value spread over a 36-month term, capped at a $10/node/month list price. Repricing lags the DRAM price by 6 months because contracts are annual. — basis: ProsperOps (~30–35%) and Zesty (25%) savings-share rates; the per-node comparables are Kubecost (~$4.5/node), StormForge ($3/vCPU), CAST AI ($5/vCPU) and Datadog ($15/host).
- **A-p4-memory-efficiency-8** [p4-memory-efficiency] The C-74 funnel converts reply 8% → scan 35% → pilot 40% → close 60%, about 0.67% of outbound touches. The founder sends 40 touches/month part-time or 120 full-time. An open-source scanner adds inbound leads that ramp to 4 conversations/month between months 9 and 15. A "pain" multiplier of 0.4 + 0.6 × (RDIMM price ÷ peak) scales conversion. — basis: ESTIMATE; no on-prem benchmark was found.
- **A-p4-memory-efficiency-9** [p4-memory-efficiency] C-74 churn is 1.5%/month at base, plus 2.0% × (1 − price ÷ peak) once DRAM gets cheap. — basis: card glut_reason ("buyers just buy RAM").
- **A-p4-memory-efficiency-10** [p4-memory-efficiency] C-74 COGS: $0.25/node/month hosting; 10% of subscription revenue for support; a kernel-savvy on-call retainer of $750/month (1–5 customers) or $2,000/month (6+ customers); $2,100 of contractor time per pilot against a $2,000 pilot fee. Free scans ($200 each) are booked as sales and marketing. — basis: ESTIMATE; the card says one incident ends the company, so on-call is not optional.
- **A-p4-memory-efficiency-11** [p4-memory-efficiency] The C-74 build takes 100 h of a kernel contractor at $175/h ($17.5k) over months 2–5. The card's ~300 h was scoped down to an MVP that fits inside $40k. — basis: the p3-audit-11 capital-tier correction.
- **A-p4-memory-efficiency-12** [p4-memory-efficiency] C-73: a $3,000 audit, with the first one in month 5. The part-time rate is 0.33 audits/month and the full-time rate is 1/month. 10% of audits convert to $250/month monitoring, which churns at 6%/month. — basis: p3-audit-11 (4–8 months to the first audit; the founder's network is in manufacturing, not SaaS; AWS list prices unchanged, so no pain).
- **A-p4-memory-efficiency-13** [p4-memory-efficiency] C-75: a $25k engagement whose COGS is $10k of contractor and GPU time. The first engagement can close in month 9. The deal rate is 0.15/month part-time and 0.35 full-time, decaying linearly to 30% of that by month 24. 60% of engagements convert to a $1,500/month retainer with 4% monthly churn. Deal flow falls 20% in GLUT and SEVERE. — basis: Red Hat AI 3.5 CPU KV offload GA (2026-09-09), Tensormesh Platform (2026-10-15) and NVIDIA Dynamo (free) are commoditizing the integration.
- **A-p4-memory-efficiency-14** [p4-memory-efficiency] The founder goes full-time only once trailing-3-month (gross profit − non-salary opex) is at least the $10k/month loaded salary. — basis: A-03.
- **A-p4-memory-efficiency-15** [p4-memory-efficiency] SOC 2 Type I costs $12k, triggered at the 5th cumulative C-74 customer. — basis: ESTIMATE. On-prem buyers ask for it later than SaaS buyers, but they do ask.
- **A-p4-memory-efficiency-16** [p4-memory-efficiency] The model works in expected values, so customers can be fractional. Taxes, payment terms and bad debt are ignored. — basis: simplicity. Read the output as a central case.
- **A-p4-memory-efficiency-17** [p4-memory-efficiency] Judgment call: **C-73 is not a lead magnet for C-74.** Cloud SaaS buyers and on-prem operators are different people. C-73 is modeled as a small cash bridge that yields only 0.25 C-74 conversations per audit. The real lead magnet for on-prem buyers is a free, read-only "cold-memory scan" (DAMON/PSI/idle-page statistics, no changes made).
- **A-p4-memory-efficiency-18** [p4-memory-efficiency] Judgment call: §5949 may also stop federal *grant/loan* funds from buying CXMT-containing products from 2027-12-23, which would keep "clean" DRAM dearer for federally funded university clusters in a CXMT-led glut. This is **[UNVERIFIED]**; it is noted as a lead and not modeled.
- **A-p4-memory-efficiency-19** [p4-memory-efficiency] Judgment call: reaching hosting providers' renters (OVHcloud and Hetzner customers, who now pay RAM pass-through increases) through a C-73-style audit is an untested variant. It is not modeled.

</details>

<details><summary><b>p4-nv-continuity-modules</b> (23)</summary>

- **A-p4-nv-continuity-modules-1** [p4-nv-continuity-modules] Month 1 of the model = 2026-11. 2028-Q1 = months 15-17. — basis: A-01, task spec.
- **A-p4-nv-continuity-modules-2** [p4-nv-continuity-modules] Founder stays part-time with no salary draw. They go full-time ($10k/mo, A-03) only when trailing-3-month operating profit is at least $12k/mo. — basis: A-03 plus a 20% buffer.
- **A-p4-nv-continuity-modules-3** [p4-nv-continuity-modules] The PC-card product uses Everspin MR4A16B Toggle MRAM, not F-RAM. — basis: the veteran scorer's /CE-latch objection to FM18W08-class F-RAM. Toggle has true async-SRAM timing, is U.S.-fabbed (Chandler AZ, per the Everspin 10-K via Phase 1/2 notes) and, per Everspin (A2 notes), is not implicated in ITC 337-TA-1487.
- **A-p4-nv-continuity-modules-4** [p4-nv-continuity-modules] Legacy PC Card slots signal at 5V, so the 3.3V-only MRAM needs 5V-tolerant LVC buffers (~$5/card). The card straps BVD1/BVD2 to "battery good" so the host raises no battery alarm. — basis: design judgment, not validated on a control [UNVERIFIED].
- **A-p4-nv-continuity-modules-5** [p4-nv-continuity-modules] MR4A16B costs $42 at our 100-500 pcs/yr. — basis: between $37.67 @1k (Future) and $46.03 qty 1 (DigiKey).
- **A-p4-nv-continuity-modules-6** [p4-nv-continuity-modules] PC Card frame kit plus 68-pin connector costs $12/card. — basis: no small-quantity price found. ITT StarCard kits exist, and one connector is Last Time Buy. This is a top open gap.
- **A-p4-nv-continuity-modules-7** [p4-nv-continuity-modules] U.S. EMS assembly costs $14/card, plus $4 setup amortization and $4 test/pack, at 100-card lots. — basis: anecdotal $415-1,300 per 10 turnkey boards; Screaming Circuits is cheapest at 25+ units.
- **A-p4-nv-continuity-modules-8** [p4-nv-continuity-modules] List prices: 2MB card $249, 4MB card $349, DS1230-class DIP $34, DS1245-class DIP $59. Resellers take 30% on cards and 20% on DIPs. — basis: Synchrotech 2MB battery card $239.39 (CDW-G), used 2MB cards $160-440, Q2MEM-2MBSN $403.81, DS1230Y-85 $35-44, Glitch Works ~$30.
- **A-p4-nv-continuity-modules-9** [p4-nv-continuity-modules] Channel mix: cards 25% eBay / 35% own store / 40% resellers; DIPs 40/40/20. — basis: judgment. Maintenance techs buy from MRO catalogs and eBay.
- **A-p4-nv-continuity-modules-10** [p4-nv-continuity-modules] eBay fee is 13.6% + $0.40; card processing is 2.9% + $0.30. — basis: typical 2025 fee schedules, not re-verified.
- **A-p4-nv-continuity-modules-11** [p4-nv-continuity-modules] CAC is $30 per own-store card order and $6 per DIP order. Direct orders ship free ($9 card, $5 DIP). Warranty/returns cost 3% of revenue. — basis: niche part-number search terms, judgment.
- **A-p4-nv-continuity-modules-12** [p4-nv-continuity-modules] Launch timing: DIPs in month 4 (FM18W08 in stock, 8-week lead time). Cards in month 9, after design, validation and the 20-26-week MRAM lead time. — basis: distributor lead times.
- **A-p4-nv-continuity-modules-13** [p4-nv-continuity-modules] Steady-state BASE volumes: 40 cards/mo (~4% of the estimated global demand) and 50 DIPs/mo. Cards ramp over 12 months, DIPs over 9. — basis: TAM chain below, judgment.
- **A-p4-nv-continuity-modules-14** [p4-nv-continuity-modules] TAM chain: 5M Fanuc CNCs produced (2022) x 15% in the U.S. x 35% on SRAM-card-era controls x 50% still running = ~131k machines. At 8 machines per shop that is ~16k shops. One card per shop every 8 years, x1.5 for other families (Mitsubishi Q, robots, other) = ~3.1k cards/yr in the U.S., and x4 = ~12k/yr globally. — basis: ESTIMATE on one REPORTED anchor. Demand is per shop, not per machine.
- **A-p4-nv-continuity-modules-15** [p4-nv-continuity-modules] Cloud line: $29/shop/month, 6% attach among direct card buyers, 2.5% monthly churn, $3/mo COGS, launch in month 15. — basis: judgment. DNC/backup software competitors were not researched.
- **A-p4-nv-continuity-modules-16** [p4-nv-continuity-modules] LTSA/DMSMS: two $2k/mo blanket orders at 50% GM, starting months 27 and 33. — basis: judgment. DLA buys 5962 memory by NSN through DIBBS, but no DS12xx NSN demand was found.
- **A-p4-nv-continuity-modules-17** [p4-nv-continuity-modules] One-time spend: ~$15.3k (LLC $0.8k, DIP designs $1.5k, contract card design $9k, used Fanuc control + Mitsubishi Q CPU + reader $2.5k, prototype run $1.5k). — basis: judgment.
- **A-p4-nv-continuity-modules-18** [p4-nv-continuity-modules] Inventory: 3 months of forward cover, with first lots of 100 cards and 200 DIPs. — basis: the 26-week MRAM lead time.
- **A-p4-nv-continuity-modules-19** [p4-nv-continuity-modules] Scenario multipliers on the core. Demand: 1.00 / 0.95 / 0.85. Price: 1.00 / 1.00 / 0.90 (copycats in SEVERE). COGS: 1.00 / 0.95 / 0.90. Order is BASE / GLUT / SEVERE. — basis: judgment. The core sells against batteries and obsolete NVSRAM, not DRAM.
- **A-p4-nv-continuity-modules-20** [p4-nv-continuity-modules] BASE DRAM path: flat at $20.37/GB through 2027-12, then -10% over 2028. GLUT and SEVERE ramp to $8.15 and $2.04 over 2028-H1. — basis: ddr5_reference() and the 01_LANDSCAPE BofA call.
- **A-p4-nv-continuity-modules-21** [p4-nv-continuity-modules] C-16 PLP option: $45k contract EE plus $5k eval boards. Design-in fee $40k at 40% GM. p(paid design-in by month 36) = 0.35 at the Q4-2026 DRAM price, scaled by the computed (DRAM+supercap saving / MRAM cost) ratio. The DRAM-less design replaces 2GB DRAM plus $12 of supercaps with 512MB STT-MRAM at $102.60/Gb chip. — basis: C-16 card, LCSC price, judgment.
- **A-p4-nv-continuity-modules-22** [p4-nv-continuity-modules] Removing the lithium cell removes lithium-metal battery shipping rules (UN3090/3091), and a memory-card subassembly needs no UL/FCC certification for U.S. sale. CE/RoHS matter only for EU sales. — basis: general regulatory knowledge [UNVERIFIED].
- **A-p4-nv-continuity-modules-23** [p4-nv-continuity-modules] Claims are "Assembled in USA", never "Made in USA" (FTC all-or-virtually-all standard). Toggle die is U.S.-fabbed, but package and assembly origin are unverified. — basis: A-09, 01_LANDSCAPE §10.3 rule 6.

</details>

<details><summary><b>p4-open-memory-ip</b> (20)</summary>

- **A-p4-open-memory-ip-1** [p4-open-memory-ip] Month 1 of the model is Dec-2026; the glut starts at month 14 (Jan-2028) per A-05 — basis: study date 2026-11-01; A-05 "from 2028-Q1".
- **A-p4-open-memory-ip-2** [p4-open-memory-ip] DRAM scenarios move only the commercial segment, through design-start budgets: demand x(1 − 0.33·drop), price x(1 − 0.15·drop), churn x(1 + 0.5·drop); academic demand is unaffected — basis: macros are priced per design, not per GB (sky130 SRAM ~$1,330/GB is 73–653x DDR5 in every scenario); NSF/DoD budgets are not tied to DRAM prices.
- **A-p4-open-memory-ip-3** [p4-open-memory-ip] BASE 2028 DDR5 drop = 10% — basis: 01_LANDSCAPE §1 row 4b (BofA −10% ASP 2028).
- **A-p4-open-memory-ip-4** [p4-open-memory-ip] Full-chip projects/yr on U.S.-fab open/academic shuttles ≈ 298 (wafer.space 2×54, ChipFoundry 60, Cadence 30, GF university pilot 40, MOSIS 2.0/Commons/other 60) — basis: wafer.space G802 repo (54 slots); Synopsys–GF pilot (40 universities); ChipFoundry, Cadence and other counts are estimates (no published counts found).
- **A-p4-open-memory-ip-5** [p4-open-memory-ip] Tiny Tapeout tiles (899 projects across SKY26a, SKY26b, IHP26a and GF0p2) are a funnel, not macro buyers — basis: a tile is far too small to host an 8KB+ macro, and TT designs pay about €70 per tile.
- **A-p4-open-memory-ip-6** [p4-open-memory-ip] 30% of full-chip projects need memory beyond the free macros, and 40% of those pay — basis: ~10 of 51 wafer.space Run 2 listings mention SRAM/RAM; the willingness-to-pay share is a judgment and the kill experiment tests it.
- **A-p4-open-memory-ip-7** [p4-open-memory-ip] Active-account cap = paying projects/yr × 2.0 years (≈72: 43 academic, 29 commercial) — basis: labs and startups tape out repeatedly across a grant or funding cycle.
- **A-p4-open-memory-ip-8** [p4-open-memory-ip] Prices: academic subscription $200/mo, commercial $800/mo; tapeout service $3k academic, $10k commercial; characterized macro license $20k — basis: these are pegged to MPW slot prices ($7–15k) and sit far below commercial compilers. Foundry-sponsored compilers are free to NDA-PDK customers, so open-PDK teams are the only market.
- **A-p4-open-memory-ip-9** [p4-open-memory-ip] Contract VLSI rate $125/h; service jobs take 12 h (academic) or 30 h (commercial); licenses take 30 h plus a 10% warranty reserve — basis: U.S. freelance memory/analog layout rates [ESTIMATE].
- **A-p4-open-memory-ip-10** [p4-open-memory-ip] Acquisition: 30 contacts/mo part-time (60 full-time) × 25% reply × 15% close, plus inbound ramping to 1.2 accounts/mo from month 4 — basis: named, public tapeout teams (wafer.space/TT repo owners, GF pilot universities). The close rate is unverified.
- **A-p4-open-memory-ip-11** [p4-open-memory-ip] Churn: 3%/mo academic, 2.5%/mo commercial — basis: student turnover and startup mortality [ESTIMATE].
- **A-p4-open-memory-ip-12** [p4-open-memory-ip] Characterization timeline: GF180 half slot at m4, characterized by m10; ChipFoundry sky130 slot at m7, characterized by m13 — basis: wafer.space Run 1 spent 12 weeks at GF; the Cadence/SkyWater MPW ran from a January submission to July die.
- **A-p4-open-memory-ip-13** [p4-open-memory-ip] The founder goes full-time when trailing-3-month gross profit ≥ $11.85k/mo (salary $10k plus full-time opex) and cash ≥ $25k — basis: A-03.
- **A-p4-open-memory-ip-14** [p4-open-memory-ip] Free-bundle shock (the biggest risk) is modeled from m18: close rate ×0.5, churn ×2, subscription price ×0.8, licenses ×0.5 — basis: the C-33 fatal flaw. OCD (Apache-2.0 GF180 SRAM, last commit 2026-10-30), Chips4Makers (Arrakeen generator, wafer.space G802) and UCSC OpenRAM (116 commits in 12 months) are all actively closing the gap for free.
- **A-p4-open-memory-ip-15** [p4-open-memory-ip] Gain-cell density advantage at mature nodes is 1.25–1.43x the 6T bitcell (65nm silicon, Teman group), with vendor claims of 1.67–2.0x (RAAAM/GF), not the 2–4x in the DD5 hypothesis. At sky130 a logic-rule gain cell may be near parity with the 1.896 µm² pushed-rule SRAM cell [ESTIMATE, untested]. Chips4Makers' "regular vs SRAM design rules" test chips on G802 show the same rule gap.
- **A-p4-open-memory-ip-16** [p4-open-memory-ip] Larger, banked SRAM macros (32–64KB at ~60% array efficiency ≈ 316 kbit/mm²) give ~5.5x the density of today's 2KB OpenRAM macro (57.6 kbit/mm²) with no new cell. That is the near-term density lever and needs software, not physics — basis: computed from VERIFIED LEF sizes.
- **A-p4-open-memory-ip-17** [p4-open-memory-ip] STTR Phase I $305k (NSF) awarded at m15 if submitted m6–m9 with a university PI; only the ~7% fee is free cash; ≥30% goes to the university — basis: NSF 26-510 summary; STTR split rule not re-verified this session.
- **A-p4-open-memory-ip-18** [p4-open-memory-ip] T2 overlay: one gain-cell evaluation license ($75k) at m34; seed $2.5M at m28, conditional on ≥$250k ARR and gain-cell silicon; circuit cofounder $220k/yr loaded; Weebit fee anchored at the ~$100k first-ever fee — basis: estimates; Weebit's fee for a fabless startup is unknown.
- **A-p4-open-memory-ip-19** [p4-open-memory-ip] The Cadence SKY130 MPW ReRAM-enabled option ($10–12k per block) is treated as a live cheap ReRAM prototype path, but a run after Jul-2026 is unconfirmed — basis: SkyWater/Cadence page via snippet. This corrects 01_LANDSCAPE §10.3 rule 8 ("no T0 path to a ReRAM test chip") for 2026. Whether die from that path may be used commercially without a Weebit licence is unknown.
- **A-p4-open-memory-ip-20** [p4-open-memory-ip] SkyWater's DMEA Category 1A Trusted status is assumed to survive the IonQ ownership — basis: IonQ/SkyWater statements only; no post-close DMEA confirmation was found.

</details>

<details><summary><b>p4-private-moe-appliance</b> (24)</summary>

- **A-p4-private-moe-appliance-1** [p4-private-moe-appliance] Two SKUs only: L "Team-1T" (1S EPYC 9005 48C, 768 GB = 12 x 64GB RDIMM, 1x RTX PRO 6000 96GB) and S "Team-S" (1S EPYC 9005 32C, 384 GB = 12 x 32GB, 1x RTX 5090 32GB); 50/50 order mix — basis: Kimi-K2.5 needs >=600 GB RAM + 48 GB VRAM and DeepSeek-V4-Flash >=200 GB + one RTX 5090 (KTransformers docs, HEAD 2026-10-28); 12-channel SP5 with 1 DIMM per channel gives 768 GB with 64GB RDIMMs.
- **A-p4-private-moe-appliance-2** [p4-private-moe-appliance] Platform is single-socket EPYC 9005, not dual-socket and not Xeon 6 6700P — basis: KTransformers keeps a weight copy per NUMA node and the measured dual-socket decode gain is only 29% (8.73 -> 11.26 tok/s); Xeon 6 6700P parts are 8-channel (technical.city snippet: 6767P "8 of 12 channels"); 12-channel Xeon 6 needs a 6900P part [UNVERIFIED price]; KTransformers now prefills long prompts layerwise on the GPU, so AMX matters less (Native-Precision tutorial; AVX2 path supports Kimi-K2.5 RAWINT4).
- **A-p4-private-moe-appliance-3** [p4-private-moe-appliance] EPYC 9455 ~$5.5k and EPYC 9355 ~$3.7k — basis: 1k-unit list prices recalled from training [UNVERIFIED]; no search budget left to confirm; Xeon 6747P MSRP $6,497 / Newegg $8,731 (snippet) used as cross-check.
- **A-p4-private-moe-appliance-4** [p4-private-moe-appliance] DRAM cost = ddr5_reference() 64GB RDIMM contract per user-GB ($25.78) x 1.15 small-buyer premium — basis: an integrator buying through distribution pays between contract and the ~$32/GB street price (ServNet tracker, Aug-2026, via C-48 card).
- **A-p4-private-moe-appliance-5** [p4-private-moe-appliance] GPU prices: RTX PRO 6000 $16,000 and RTX 5090 $5,000 today — basis: tech-insider (NVIDIA US store $16,000, Sep-2026) and GPUPrix ($17,987 low, 2026-10-22); RTX 5090 Micro Center $4,299-5,300 (online $8.5-10k). Chose the low end of the observed range.
- **A-p4-private-moe-appliance-6** [p4-private-moe-appliance] BASE price path: DRAM and GPU hold to Dec-2027, then -30% linear across 2028; GLUT: DRAM -60% (ddr5_reference glut deck) and GPU to 55% from Jan-2028; SEVERE: DRAM component $2.04/GB and GPU to 50% from Jan-2028 — basis: ASSUMPTIONS A-05, task spec, DD4's BASE shape; GPU glut factor = return to the $8,565 launch MSRP.
- **A-p4-private-moe-appliance-7** [p4-private-moe-appliance] Hardware priced cost-plus at a 22% gross-margin target (19% after 2% warranty reserve and shipping) — basis: C-48 card's own BOM model; Supermicro FY26 GAAP GM 10.8% (FQ4 17.5%) is the scale floor.
- **A-p4-private-moe-appliance-8** [p4-private-moe-appliance] Subscription $1,250/month (L) and $650/month (S), billed annually in advance, mandatory in year 1, 20% annual churn — basis: Lemony $499/month for 5 users (TechCrunch snippet), MSP AI add-on $25-75/user/month, managed private AI $12-20/user/month; churn is a judgment that small orgs drop support and self-maintain the open-source stack (DD4 red-team pattern).
- **A-p4-private-moe-appliance-9** [p4-private-moe-appliance] Business-hours, next-business-day SLA only; no 24/7 on-call in BASE — basis: DD4 was killed partly by $2.5-3k/month on-call cost; a 24/7 retainer is run as a sensitivity (it delays full-time to m35).
- **A-p4-private-moe-appliance-10** [p4-private-moe-appliance] Conversion 8% of qualified conversations, 4-month sales cycle, 5 qualified conversations/month part-time and 14 full-time, 3/month from an MSP/RPO channel from m13 — basis: judgment; C-48 verify_corrections (3-6 month security reviews). The kill experiment measures conversion directly.
- **A-p4-private-moe-appliance-11** [p4-private-moe-appliance] Single-stream decode 17 tok/s (L, Kimi-K2.5 INT4) and 25 tok/s (S, MiniMax-M2.x FP8) — basis: scaled from KTransformers DeepSeek-R1 8.73 tok/s (1S Xeon 6454S, 8ch DDR5-4800) x2.0 bandwidth x37/32 active params, derated 0.85; S from MiniMax-M2.1 32.1 tok/s on 2S EPYC 9355 + 1x RTX 5090 / 1.29.
- **A-p4-private-moe-appliance-12** [p4-private-moe-appliance] Concurrency curve aggregate = single x min(c^0.62, 2.4) — basis: KTransformers balance_serve +130% at 4-way; Xeon 6 + MRDIMM-8800 aggregate 17 -> 40 tok/s.
- **A-p4-private-moe-appliance-13** [p4-private-moe-appliance] Acceptable per-user speed 10 tok/s; 15% of named users generating at peak — basis: judgment; yields 27 named users (L) and 40 (S).
- **A-p4-private-moe-appliance-14** [p4-private-moe-appliance] L-box prefill = 2x the measured 1x 48GB-GPU PCIe 4.0 Kimi numbers (53/184 tok/s at 2k/8k) because PCIe 5.0 doubles layerwise weight-streaming bandwidth — basis: judgment; gives ~19-22 s time-to-first-token for 2-8k-token prompts.
- **A-p4-private-moe-appliance-15** [p4-private-moe-appliance] Substitute capacities: Mac Studio M5 Ultra 512GB ~5 named users; DGX Station GB300 ~80 named users — basis: judgment from M3 Ultra Kimi-K2.5 5-15 tok/s (snippet) and GB300 memory layout (288 GB HBM3e + 496 GB LPDDR5X).
- **A-p4-private-moe-appliance-16** [p4-private-moe-appliance] M365 Copilot GCC High ~$35/user/month — basis: [UNVERIFIED-training] commercial Copilot ~$30/user/month; GCC High GA Dec-2025 confirmed by snippet, price not found.
- **A-p4-private-moe-appliance-17** [p4-private-moe-appliance] CMMC Level 2 does NOT require on-prem AI; cloud AI for CUI needs FedRAMP Moderate or equivalent (DFARS 252.204-7012), and M365 Copilot GCC High and Claude on Bedrock GovCloud qualify — basis: Secureframe, Coalfire Federal, Daymark, Anthropic/AWS snippets. So the defense segment is narrowed to orgs with on-prem/air-gapped CUI enclaves or ITAR engineering networks.
- **A-p4-private-moe-appliance-18** [p4-private-moe-appliance] Defense buyers will want U.S.-origin weights; the L box is sized so Inkling 975B-A41B (Apache 2.0, Jul-2026) and Nemotron 3 Ultra 550B-A55B (Jun-2026) fit at 4-bit — basis: open-weights index snippets; KTransformers documents neither (llama.cpp GGUF exists for Nemotron 3 Ultra), so support is a dependency.
- **A-p4-private-moe-appliance-19** [p4-private-moe-appliance] Parts are bought in the order month; 50% deposit at order, balance + setup fee + first-year subscription at delivery (order + 1) — basis: C-48 card (50% deposits). Expected-value cash hides lumpiness; the model prints a whole-box check (two simultaneous L orders need a ~$25k bridge).
- **A-p4-private-moe-appliance-20** [p4-private-moe-appliance] Demo capacity is rented ($1,200/month) until an S-class demo box can be bought while keeping $15k cash — basis: judgment; rental availability of 768GB+/GPU hosts not confirmed (open gap).
- **A-p4-private-moe-appliance-21** [p4-private-moe-appliance] ESP compliance set-up $8k (m9) + $400/month — basis: judgment; remote support into a customer's CUI enclave can put the vendor in the customer's CMMC scope, so support is designed as customer-escorted sessions and offline signed update bundles.
- **A-p4-private-moe-appliance-22** [p4-private-moe-appliance] 30% tax on positive cumulative taxable income with loss carry-forward — basis: 05_REDTEAM.md RT-VC-DD1-07 (applied to all round-2 models).
- **A-p4-private-moe-appliance-23** [p4-private-moe-appliance] Founder full-time trigger: trailing 3-month (GP - recurring opex) >= $10k and post-tax cash >= $30k — basis: A-03 salary; buffer judgment.
- **A-p4-private-moe-appliance-24** [p4-private-moe-appliance] Buy only from OCMs/authorized distributors (no gray-market GPUs during the shortage) and only Samsung/SK hynix/Micron DRAM — basis: DFARS 252.246-7008 counterfeit-avoidance preference and NDAA §5949 (2027-12-23) CXMT/YMTC/SMIC exclusion for federal buyers (01_LANDSCAPE §0 item 8).

</details>

<details><summary><b>p4-provenance-recert</b> (26)</summary>

- **A-p4-provenance-recert-1** [p4-provenance-recert] I used all 30 WebSearch calls. My single WebFetch (govinfo.gov) failed DNS, and per the tool's instruction I stopped trying more hosts. Every external fact here is therefore a search snippet, and nothing is [VERIFIED] — basis: tool limits.
- **A-p4-provenance-recert-2** [p4-provenance-recert] Month 1 is Nov-2026 and month 36 is Oct-2029. §5949 takes effect in month 14 (Dec-2027), and the DRAM turn starts in month 15 (Jan-2028) — basis: 01_LANDSCAPE §0 item 4 and §7.2.
- **A-p4-provenance-recert-3** [p4-provenance-recert] In BASE, used-module prices stay flat at their trailing-12-month midpoints through Dec-2027. They fall 10% across 2028, then another 10% by Oct-2029 — basis: BofA −10% 2028 ASP (01_LANDSCAPE §1 row 4b). I hold prices flat rather than extending the 2026 rise, which is conservative.
- **A-p4-provenance-recert-4** [p4-provenance-recert] In GLUT, used-module resale falls to 0.40× of today over the 12 months of 2028, using the ratio of glut to contract price from `ddr5_reference()`. In SEVERE it falls to 0.10×. Both scenarios floor used resale at $1.0/GB, the 2023-like trough from C_notes — basis: A-05, the 2018–19 analog of −62.5% in about 4 quarters, and the canonical $2.04/GB severe deck.
- **A-p4-provenance-recert-5** [p4-provenance-recert] Used-module prices follow the DDR5 contract index one-for-one. Used DDR4 rose 285–335% YoY into Aug-2026 (amcompute), so a 60% fall would only take it back to about late-2025 levels — basis: amcompute appraisals.
- **A-p4-provenance-recert-6** [p4-provenance-recert] Resale midpoints are $125 for a 32GB DDR4 RDIMM, $310 for 64GB DDR4 and $1,045 for 64GB DDR5. The unit mix is 60/30/10 — basis: amcompute realized ranges for the 12 months to Aug-2026; DDR5 decommission supply is thin.
- **A-p4-provenance-recert-7** [p4-provenance-recert] Lots are bought at **65%** of realized resale. 01_LANDSCAPE's 60% was flagged as optimistic: Iron Mountain ALM is capturing the repricing, and lot listings run near resale (PCSP: 24×32GB at ~$140 each). **This is the single most important unverified input in the recert line.** The kill experiment exists to measure it.
- **A-p4-provenance-recert-8** [p4-provenance-recert] B2B buyers (TPMs, refurbishers) pay 0.88× the eBay realized price, with 3% payment fees. The eBay fee is 13.6% plus $0.40 per order. I used the higher of two conflicting fee sources — basis: LitCommerce calculator (13.6%) vs EcomCalcTools (10.9%).
- **A-p4-provenance-recert-9** [p4-provenance-recert] Labor is 12 minutes per module, covering receiving, SPD read and log, loading and unloading burn-in, labels, photos and listing, and packing. Founder ops time is 35 h/month part-time and 60 h/month full-time. Hours beyond that go to a technician at $25/h loaded — basis: C_notes used 6 minutes for testing alone; I doubled it for handling.
- **A-p4-provenance-recert-10** [p4-provenance-recert] Test fallout is 3% of purchases and returns are 2% of revenue — basis: C_notes Appendix A. Warranties in the channel run from 90 days to lifetime (Reboot IT, Rimlance), so I assume a 1-year warranty.
- **A-p4-provenance-recert-11** [p4-provenance-recert] Inventory is bought in month t and sold in t+1. Purchases are capped by cash minus a $5k reserve. The operator buys only 10% of target when expected contribution falls below 5%, judged on the trailing price trend rather than a forecast — basis: rational wind-down. Inventory held through a falling month still takes the loss.
- **A-p4-provenance-recert-12** [p4-provenance-recert] Volume ramps by 40 modules a month, capped at 400 per month part-time and 800 full-time — basis: channel absorption across eBay plus 3–5 B2B accounts; not tested.
- **A-p4-provenance-recert-13** [p4-provenance-recert] Optane PMem 128GB resells at $200 and is bought at 55% of that, 25 units a month, all through eBay. Volume drops to 40% after vSphere 8 end of general support (2027-10-11), and price follows the DDR4 index — basis: listings show $290 new on eBay.de (undated) and $65–380 used (C-26). Broadcom KB 459135.
- **A-p4-provenance-recert-14** [p4-provenance-recert] Launch is month 10 (Aug-2027). §805's indirect ban starts 2027-06-30 and §5949 on 2027-12-23, but buyers are waiting on the final FAR rule — basis: C-64 verify correction; Crowell on §805.
- **A-p4-provenance-recert-15** [p4-provenance-recert] There are two tiers: $750/month for integrators and resellers and $2,500/month for module makers, OEMs and ODMs, with 35% of customers on the high tier. That blends to $1,362/month. One-off evidence packs sell at $900, bought by 15% of conversations — basis: priced below SiliconExpert-class ACVs (Accuris offer floor of $6k/yr) and far below Exiger's ($12.7M Army) and Interos's ($12M DLA/3 yr) enterprise deals. The C-64 card's $1.5–12k/month tiers were cut for the safe harbor.
- **A-p4-provenance-recert-16** [p4-provenance-recert] The founder holds 5 qualified conversations a month part-time and 12 full-time. Close rate is 10% in the bundle and 7% standalone, where die-source evidence is thinner; that 3-point lift *is* the bundle hypothesis and is not measured. Churn is 2% a month — basis: B2B SMB SaaS norms; untested.
- **A-p4-provenance-recert-17** [p4-provenance-recert] Die-ID lab work (X-ray, decap and die-marking photo) costs $400 a sample and is resold at 1.6×. Each subscriber orders 0.4 samples a month. The library builds at 3 samples a month from month 4 to 18, then 1 a month. Standalone CleanBOM also buys each sample module ($150) — basis: weak blog ranges of $50–500 per component and $150–500 per SEM sample; ANAB lists 26 AS6171 labs; no lab quote was obtained.
- **A-p4-provenance-recert-18** [p4-provenance-recert] CleanBOM demand is the same in all three price scenarios, because it is set by statute, not by DRAM prices. A glut raises CXMT share, which arguably *raises* demand. I do not credit that.
- **A-p4-provenance-recert-19** [p4-provenance-recert] Launch is month 12. Price is $0.60 per DIMM-month, below the card's $0.75, because Lenovo MPFA, Intel MFP (in AMI and Insyde BMC firmware) and Park Place ParkView already provide prediction. A customer has 1,200 DIMMs. Sales add 0.15 new customers a month part-time and 0.35 full-time. Churn is 1.5% a month, rising to 3.5% after Jan-2028 in GLUT and SEVERE as refresh gets cheaper — basis: C-85 verify (DIY sparing is ~3.6× cheaper); Lenovo Press LP2326; Intel MFP case studies.
- **A-p4-provenance-recert-20** [p4-provenance-recert] Replacements run at 1.5% per DIMM-year. The spare pool is 2% of covered DIMMs, carrying cost is 20% a year, and shipping is $18 a swap. In the bundle, spares cost the recert buy price; standalone, they cost the eBay resale price — basis: C-85 card; Google 2009 (~8% of DIMMs see errors each year).
- **A-p4-provenance-recert-21** [p4-provenance-recert] The founder goes full-time on a $10k/month salary ($120k loaded, A-03) once trailing-3-month EBITDA before salary is at least $12k and cash is at least $25k. They return to the day job, and salary goes to 0, if cash falls below $8k — basis: A-03.
- **A-p4-provenance-recert-22** [p4-provenance-recert] Fixed opex is tools $150/month (+$350 once CleanBOM is live), insurance $200 (+$400 E&O for attestations), bookkeeping $150 and marketing $300. Flex space costs $1,500/month above 250 modules a month or once the founder is full-time. Legal is $2.5k at setup and $6k before CleanBOM launch. ISO 9001/AS6081 readiness is $10k in month 15, plus $3k for surveillance in month 27 — basis: Amtivo's AS9120 $6–12k as a proxy; NQA is the AS6081 certification body.
- **A-p4-provenance-recert-23** [p4-provenance-recert] Capex is $4.2k in month 1 (two used Gen10 DDR4 servers without memory, plus ESD bench and label printer) and $4k in month 6 (a DDR5 platform). No RAMCHECK is bought: memtest86+ plus stressapptest on server beds is assumed enough. RAMCHECK LX DDR4 is about $2.5k if a buyer demands one.
- **A-p4-provenance-recert-24** [p4-provenance-recert] **R2v3 is not required** to buy tested, working RDIMMs for reuse from R2 ITADs. The ITAD's downstream due diligence covers it. R2v3 would be needed only to take untested or scrap circuit-board lots, which are Focus Materials — basis: [UNVERIFIED-training] reading of R2v3; SERI license is $2k/facility/yr plus CB audit if ever needed.
- **A-p4-provenance-recert-25** [p4-provenance-recert] Recovered DIMMs are never sold into DoD deliverables, and every module is labeled "used/recertified" — basis: DFARS 252.246-7007/-7008 and FAR 52.246-26 [UNVERIFIED-training]; 18 U.S.C. §2320 (C_notes §6).
- **A-p4-provenance-recert-26** [p4-provenance-recert] Founder time is imputed at $75/h, used only for CAC, never as cash. A CleanBOM sales conversation takes 3 hours — basis: estimate.

</details>

<details><summary><b>p4w-legacy-dram-diebank</b> (13)</summary>

- **A-p4w-legacy-dram-diebank-1** [p4w-legacy-dram-diebank] No new web research: WebSearch quota 0 and no WebFetch used. Every URL in 04_DEEPDIVES/legacy-dram-diebank.md was already logged in research/sources/*.jsonl (checked by script, 50/50 present) and is carried into research/sources/p4w-legacy-dram-diebank.jsonl with its original log named — basis: task instruction; CONVENTIONS source-logging rule.
- **A-p4w-legacy-dram-diebank-2** [p4w-legacy-dram-diebank] All economics are taken unchanged from models/legacy-dram-diebank.py (re-run 2026-11-01, exit 0; figures match research/phase4/legacy-dram-diebank_model_output.md) — basis: Rule 8.
- **A-p4w-legacy-dram-diebank-3** [p4w-legacy-dram-diebank] Bank break-even aftermarket multiples (1.5x bought m20 BASE, 2.3x GLUT, 4.8x long-run) = model §3 cost/unit divided by the packaged $/GB at purchase ($25.37/$16.80, $18.54/$8.15, $14.47/$3.00) — basis: arithmetic on model output.
- **A-p4w-legacy-dram-diebank-4** [p4w-legacy-dram-diebank] A bank bought at the 2026 peak would need ~$311k (12,510 die x 0.75 x $20.37/GB + $120k set-up) — basis: arithmetic on model inputs bank_wafers, good_die_per_wafer, wafer_factor, bank_nre_first.
- **A-p4w-legacy-dram-diebank-5** [p4w-legacy-dram-diebank] "4 design-ins x 1,000 units is 6.7x the modelled volume" = 4,000 / (2 x 300) units per year — basis: model §6 grid inputs.
- **A-p4w-legacy-dram-diebank-6** [p4w-legacy-dram-diebank] Later Plan A gates sit at ~75% of the model's BASE path: m12 recurring ARR >= $9.5k (model $12.6k); m18 >= $16.5k (model $22.0k); m5 >= 1 paid study (model ~$4.4k cumulative one-off revenue); m9 >= 1 program contracted (model 0.8) — basis: same convention as the round-1 DD2 author (p4w-lifecycle-intel), so the expected case passes.
- **A-p4w-legacy-dram-diebank-7** [p4w-legacy-dram-diebank] Cash floor kill: stop below $20,000 of cash in any month — basis: model cash low is $30.2k at m3; a ~$10k cushion before the founder's $40k is exhausted. Judgment.
- **A-p4w-legacy-dram-diebank-8** [p4w-legacy-dram-diebank] Kill experiment runs 2026-11-02 to a 2026-12-01 decision; OCM written answers may run to 2026-12-15, with fewer than 3 of 6 answers counting as a track-A fail — basis: <30-day rule; OCM response times unknown.
- **A-p4w-legacy-dram-diebank-9** [p4w-legacy-dram-diebank] Added kill track C3 (Micross or an equal vault must quote white-label consignment for a third-party program manager, else kill L1) — basis: Plan A's L1 product depends on it; notes §1.1 say Micross publishes no rates and sells the vault direct.
- **A-p4w-legacy-dram-diebank-10** [p4w-legacy-dram-diebank] Added gate: no Stage-1 raise without a signed hi-rel hardware co-founder by 2028-04-30, even if the m15 OCM/LOI gate passes — basis: all three scorers gave founder fit 1; C-65 card says doable_by_founder "no - hardware team"; the founder is not a chip engineer.
- **A-p4w-legacy-dram-diebank-11** [p4w-legacy-dram-diebank] DMSMS advisor at 0.25–0.5% equity; hi-rel co-founder paid in equity until Stage 1 — basis: common early-stage practice; unsourced judgment. Post-government employment rules for ex-DoD advisors not checked.
- **A-p4w-legacy-dram-diebank-12** [p4w-legacy-dram-diebank] Status recommended into the round-2 red team: SIDE LINE, not MOONSHOT — basis: model §6 EV/capital 0.46x BASE (0.36x GLUT, 0.28x SEVERE); Plan A never pays the founder; venture returns need ~4 design-ins/yr x ~1,000 units against Teledyne/Mercury/Frontgrade heritage.
- **A-p4w-legacy-dram-diebank-13** [p4w-legacy-dram-diebank] Kill criterion 13 threshold ("fewer than 4 design-ins a year at ~1,000 units" by ~m72 = 2032-10) — basis: notes §12 #4; model §6 grid shows <=2.42x capital below that point.

</details>

<details><summary><b>p4w-lifecycle-intel</b> (12)</summary>

- **A-p4w-lifecycle-intel-1** [p4w-lifecycle-intel] No new web research: WebSearch quota 0 and no WebFetch used; every URL in 04_DEEPDIVES/lifecycle-intel.md was already logged in research/sources/*.jsonl (checked by script, 53/53 present), so no new sources file is written — basis: task instruction; CONVENTIONS source-logging rule.
- **A-p4w-lifecycle-intel-2** [p4w-lifecycle-intel] All economics are taken unchanged from models/lifecycle-intel.py (re-run 2026-11-01, exit 0, output byte-identical to research/phase4/lifecycle-intel_model_output.md) — basis: Rule 8.
- **A-p4w-lifecycle-intel-3** [p4w-lifecycle-intel] Later kill gates are set at ~75% of the model's BASE path (m7: <2 paying accounts vs model 2.8; m12: <9 accounts or <$3,000 MRR vs model 11.8 / ~$4.1k; m18: <20 accounts vs 27 opens exit talks), not at the model path itself — basis: the notes' m12 gate (12 accounts / $4k) equals the model, so the expected case would trip it; model §7 shows a x0.7 miss on price or conversion never covers the salary.
- **A-p4w-lifecycle-intel-4** [p4w-lifecycle-intel] m24 kill: ARR < $150,000 at 2028-11-30 — basis: ~22% below the model's SEVERE m24 ARR of $172,694.
- **A-p4w-lifecycle-intel-5** [p4w-lifecycle-intel] Kill experiment runs 2026-11-02 to a 2026-12-01 decision; the Nexar/DigiKey written-answer deadline (K5) is extended to 2026-12-15 — basis: <30-day rule; vendor support response times unknown.
- **A-p4w-lifecycle-intel-6** [p4w-lifecycle-intel] The three C-72 supplier calls (Winbond or Nanya U.S. sales office, a Micron franchised distributor) are added to the kill test at zero cost — basis: 03_SCORING.md §8 DD2 row ("make the three C-72 supplier calls").
- **A-p4w-lifecycle-intel-7** [p4w-lifecycle-intel] The founder's employer is an unpaid design partner only, after written conflict-of-interest and IP-assignment clearance — basis: standard moonlighting/IP-assignment practice; employment contract not seen.
- **A-p4w-lifecycle-intel-8** [p4w-lifecycle-intel] Advisor compensation: procurement advisor 0.25–0.5% equity; index-methodology advisor 0.5% equity or ~$2–5k cash — basis: common early-stage advisor grants; unsourced judgment.
- **A-p4w-lifecycle-intel-9** [p4w-lifecycle-intel] Raise only if by 2028-05 the index has >=10 licences or one enterprise redistribution deal; then a $0.5–1M angel round — basis: model §8 (27 accounts + 10 licences pays the founder); scorers' ~$0.3M ARR ceiling otherwise.
- **A-p4w-lifecycle-intel-10** [p4w-lifecycle-intel] Trademark filing ~$350–1,000 per class at USPTO — basis: training knowledge, UNVERIFIED.
- **A-p4w-lifecycle-intel-11** [p4w-lifecycle-intel] Stress test: lifecycle SaaS −20% in GLUT would cut m36 ARR by ~$33k — basis: 0.2 x $13,696/month (model §6 lifecycle line) x 12.
- **A-p4w-lifecycle-intel-12** [p4w-lifecycle-intel] First-90-day selling targets (5 signed design partners and >=3 BOMs uploaded by 2027-01-01; >=10 waitlist accounts and >=3 partners sharing 24 months of PO history by 2027-01-31; 150 newsletter subscribers) — basis: judgment consistent with the model's 6 trials at launch (m5) and 40% contributor share.

</details>

<details><summary><b>p4w-memory-efficiency</b> (11)</summary>

- **A-p4w-memory-efficiency-1** [p4w-memory-efficiency] Capital tier is stated as T0 as modeled (100 h contractor MVP, cash low $10.4k) and T1 as carded (~300 h, $45–60k) — basis: model §5; concepts_master.json C-74 verify correction.
- **A-p4w-memory-efficiency-2** [p4w-memory-efficiency] The ~$6k kill experiment is treated as overlapping the model's M2–M5 build and test-infra spend; if fully additive, the cash low point falls to ~$4.4k ($10.4k − $6k) — basis: model §5 cash low; notes §11 budget.
- **A-p4w-memory-efficiency-3** [p4w-memory-efficiency] The first 90 days of selling assume the kill experiment passes on 2026-12-01, which is faster than the model (outreach M5, first subscription M8); the model is the base case and the plan is upside — basis: model INPUTS c74_sell_start/c74_agent_ready.
- **A-p4w-memory-efficiency-4** [p4w-memory-efficiency] Roadmap gates are set at or slightly above the model's BASE expected values (≥1 subscription by 2027-07-31 vs 0.55 expected at M9; ≥3 customers by 2028-01-31 vs 2.57 at M15; ARR ≥ $37.7k at M18), and a venture-continuation gate at 2× base ($75k ARR, ≥8 customers) — basis: model §4a; founder goal of recurring revenue.
- **A-p4w-memory-efficiency-5** [p4w-memory-efficiency] Kill criterion for reclaim on pilot fleets is a median below 8% (between the 5% sensitivity case, $40.3k M36 ARR, and the 10% base) — basis: model §6.
- **A-p4w-memory-efficiency-6** [p4w-memory-efficiency] Kill criterion on DRAM price: stop new C-74 acquisition if 64GB DDR5 RDIMM contract falls >40% below the 4Q26 peak (< ~$15.50/user-GB = 0.6 × $25.78) before 8 customers — basis: model §2 fee path; A-05.
- **A-p4w-memory-efficiency-7** [p4w-memory-efficiency] A kernel cofounder for equity would save ~$24k/yr of on-call at 6+ customers (12 × $2,000) — basis: model INPUTS oncall_large.
- **A-p4w-memory-efficiency-8** [p4w-memory-efficiency] A freedom-to-operate read by a lawyer is budgeted at ~$2–3k before the first subscription; it is not in the model — basis: ESTIMATE; no patent search was run for DD4.
- **A-p4w-memory-efficiency-9** [p4w-memory-efficiency] University purchasing (quotes, POs, vendor registration) may add 30–90 days to a sale — basis: ESTIMATE, not researched [UNVERIFIED].
- **A-p4w-memory-efficiency-10** [p4w-memory-efficiency] Senpai's license was not checked; the deep dive recommends re-implementing the PSI-feedback idea rather than copying code until it is confirmed — basis: no license data in the logged sources.
- **A-p4w-memory-efficiency-11** [p4w-memory-efficiency] Channel partners (HPC integrators, refurbished-server resellers) are priced at a 20–30% revenue share — basis: research notes §8 [ESTIMATE].

</details>

<details><summary><b>p4w-nv-continuity-modules</b> (20)</summary>

- **A-p4w-nv-continuity-modules-1** [p4w-nv-continuity-modules] The PROFITABLE verdict is MARGINAL, not the research notes' "yes, as a small business". — basis: BASE never triggers a founder salary (model §[5]). The 36-month net of $79.1k is ~$34 per part-time hour at A-03's 15 h/week. 25% of m36 revenue is two LTSAs with no DLA demand evidence. The card's unit economics are strong (57–61% GM), so it is not a NO.
- **A-p4w-nv-continuity-modules-2** [p4w-nv-continuity-modules] The kill-test deposit page states a target ship date of 2027-07 (model card launch m9), not the notes' 120 days. — basis: the 20–26-week MRAM lead time makes 120 days unreliable. A longer promised wait makes 15 deposits a stronger signal.
- **A-p4w-nv-continuity-modules-3** [p4w-nv-continuity-modules] The kill test adds a 72-hour magnetic-field storage check (card next to a spindle motor or magnetic chuck). — basis: Toggle MRAM's tolerance of shop-floor magnetic fields was not researched [UNVERIFIED risk]. The check costs nothing.
- **A-p4w-nv-continuity-modules-4** [p4w-nv-continuity-modules] The kill test pulls forward ~$5.3k of model spend from m2–5 and adds ~$1.4k of new spend, so the BASE cash low falls from $10.8k to ~$9.4k. — basis: arithmetic on model §[9] `one_time` against the notes §8 budget.
- **A-p4w-nv-continuity-modules-5** [p4w-nv-continuity-modules] Supply-failure path: reprice to $299 and re-test demand for 14 days; <10 deposits at $299 means kill. — basis: the +30% price sensitivity (model §[6]) and the notes' reprice-or-kill rule.
- **A-p4w-nv-continuity-modules-6** [p4w-nv-continuity-modules] Kill thresholds after launch are judgment calls anchored on model rows:
- **A-p4w-nv-continuity-modules-7** <20 cumulative cards by 2027-10-31, against 33 modeled
- **A-p4w-nv-continuity-modules-8** no breakeven by m17, the worst modeled case
- **A-p4w-nv-continuity-modules-9** realized blended card price <$175 for 3 months, against the price −30% case
- **A-p4w-nv-continuity-modules-10** m18 run-rate <$85k (conversion −30%) or <$60k (wind down)
- **A-p4w-nv-continuity-modules-11** returns >10% / >20%
- **A-p4w-nv-continuity-modules-12** [p4w-nv-continuity-modules] Roadmap gates take model values with ~10–25% slack, e.g. ≥30 DIPs by m6 against 34 modeled, and ≥25 cards by m12 against 33. — basis: model §[4].
- **A-p4w-nv-continuity-modules-13** [p4w-nv-continuity-modules] Warranty is 2 years, matching MRO Electric's on its Fanuc SRAM modules. — basis: the MRO Electric listing; the model carries 3% of revenue for warranty and returns.
- **A-p4w-nv-continuity-modules-14** [p4w-nv-continuity-modules] A Mitsubishi-format card may later test $299. — basis: the Q2MEM-2MBSN eBay listing at $403.81. Not in the model.
- **A-p4w-nv-continuity-modules-15** [p4w-nv-continuity-modules] Outbound sales are capped at ~5 calls a week while the founder keeps the day job. — basis: A-03 (15 h/week).
- **A-p4w-nv-continuity-modules-16** [p4w-nv-continuity-modules] Part-time fulfilment help (~$500/month) appears only on the S1 path (>100 orders/month). A DMSMS business-development advisor works on commission only, from m24. Neither is in BASE. — basis: judgment.
- **A-p4w-nv-continuity-modules-17** [p4w-nv-continuity-modules] A 10%/yr installed-base shrink over 3 years (0.9³ ≈ 0.73) is proxied by the model's "conversion −30%" case. — basis: the model holds demand flat, and the decline rate is unknown.
- **A-p4w-nv-continuity-modules-18** [p4w-nv-continuity-modules] The founder must check the day-job invention-assignment clause before any design work. — basis: standard employment-agreement risk for a founder in product development at a manufacturer.
- **A-p4w-nv-continuity-modules-19** [p4w-nv-continuity-modules] Equity is never raised for C-12 alone. Reconsider only above a $0.5M run-rate with >30% recurring revenue. — basis: scorer verdicts and model §[6b] (only the S4 stretch path exceeds $0.5M).
- **A-p4w-nv-continuity-modules-20** [p4w-nv-continuity-modules] PC Card standard licence/logo status and export classification are not assessed [UNVERIFIED]. Mitigations: no PCMCIA logo, and confirm the classification before the first non-U.S. sale. — basis: not researched.

</details>

<details><summary><b>p4w-open-memory-ip</b> (11)</summary>

- **A-p4w-open-memory-ip-1** [p4w-open-memory-ip] All model numbers are taken from a re-run of models/open-memory-ip.py on 2026-11-01 (exit 0). "fte_be" (first month GP >= $11.85k: m18/m23/m28) and the m14 new-account rate (BASE 1.55, GLUT 1.45/mo) come from the model's simulate()/summarize() in the same run but are not printed — basis: scratch import of the model, no model edits.
- **A-p4w-open-memory-ip-2** [p4w-open-memory-ip] "Breakeven" is reported two ways: cash-flow breakeven with the founder unpaid (m8) and founder-paid breakeven (GP >= salary + full-time opex) — basis: model's FT trigger; m8 alone overstates profitability.
- **A-p4w-open-memory-ip-3** [p4w-open-memory-ip] The kill experiment runs 2026-11-02 to 2026-12-01 (before model m1 = Dec-2026) to avoid the academic winter break; ~$3k of its ~$5.1k overlaps the model's m1 templates ($1k) and m2 contractor ($2.5k), and the ~$2.1k remainder lowers the model cash low from $20.4k to ~$18.3k — basis: arithmetic on model §6 and notes §9 budget.
- **A-p4w-open-memory-ip-4** [p4w-open-memory-ip] Kill-test PASS needs all of: >=3 paid $500 deposits against >=$2k orders OR >=$15k signed LOIs; >=1 commercial/SBIR buyer at >=$10k; reviewer confirms <=200 h to timing-clean >=16 KB sky130; no channel owner confirms free characterized >=16 KB within 12 months. Failing only the $10k-buyer test means pivot to an academic side line, not kill — basis: notes §9 thresholds reconciled with model §8 kill line.
- **A-p4w-open-memory-ip-5** [p4w-open-memory-ip] Dated kill thresholds are set at roughly half the BASE model values (m6: 2 accounts/$8k vs 2.5/$15.9k; m12: ARR $20k/run-rate $64k vs $40.7k/$127.9k; m18: 9 accounts/$8k GP vs 12.7/$12.2k) — basis: judgment; half-of-plan is a conventional kill line for an unverified close rate.
- **A-p4w-open-memory-ip-6** [p4w-open-memory-ip] Silicon gates: >=2 of 3 macro sizes functional on >=80% of tested die and access time <=1.5x simulated; gain-cell kill if <1.2x density vs the 1.896 um2 6T cell — basis: judgment; 1.2x sits just below the 1.25x low end of 65nm silicon results.
- **A-p4w-open-memory-ip-7** [p4w-open-memory-ip] C-22 kill if Weebit fabless evaluation > $100k, MPW die not usable in product, or no defense/security buyer signs a >= $25k paid-evaluation LOI by 2028-05-31 — basis: $100k = Weebit first-ever fee anchor; $25k LOI threshold is judgment.
- **A-p4w-open-memory-ip-8** [p4w-open-memory-ip] Seed gate is read as revenue run-rate >= $250k (model §9 says ">=$250k ARR wedge"); recurring ARR never reaches $250k by m36 in any modeled case — basis: model §6-7 outputs.
- **A-p4w-open-memory-ip-9** [p4w-open-memory-ip] FTO patent landscape read on gain cells costs ~$10-20k and is not in the model — basis: judgment for a focused U.S. landscape read; to be funded from STTR/seed.
- **A-p4w-open-memory-ip-10** [p4w-open-memory-ip] Commercial subscription anchor corrected: $9.6k/yr is about two contract-engineer weeks at the model's own $125/h, not "< one week" as the model input text says; academic $2.4k/yr is 16-34% of a $7-15k slot, not "<25%" — basis: arithmetic on model inputs.
- **A-p4w-open-memory-ip-11** [p4w-open-memory-ip] Open-MPW die are not trusted-flow parts by default, and most open-shuttle customers publish their GDS (only 11 of 51 wafer.space Run 2 listings are private), so the sellable asset is characterization, support and warranty rather than secret layout — basis: ws-run2 git listing; trusted-flow point is judgment.

</details>

<details><summary><b>p4w-private-moe-appliance</b> (15)</summary>

- **A-p4w-private-moe-appliance-1** [p4w-private-moe-appliance] Added kill gate K0 (written employer carve-out before any build or outreach) — basis: the founder's employer is customer candidate #1 and the round-1 red team made the same gate mandatory for DD2 (05_REDTEAM.md RT-VC-DD2-05).
- **A-p4w-private-moe-appliance-2** [p4w-private-moe-appliance] Added kill gate K7 (>=20 qualified conversations held within 28 days of part-time outreach) — basis: the model assumes 5 qualified conversations/month sustained; a founder who cannot hold 20 in a one-month sprint is unlikely to sustain 5/month for 18 months (same logic as DD2's K6).
- **A-p4w-private-moe-appliance-3** [p4w-private-moe-appliance] Roadmap and kill gates are set at ~75% of the model's BASE path (rounded) — basis: the convention used by the round-1 DD2 revision; expected-value boxes are fractional, so gates use whole-box floors.
- **A-p4w-private-moe-appliance-4** [p4w-private-moe-appliance] Subscription renewal kill threshold 70% at first anniversaries (model assumes 80%, i.e. 20% annual churn) — basis: judgment; a 10-point miss is the earliest measurable sign the recurring line is weaker than modelled.
- **A-p4w-private-moe-appliance-5** [p4w-private-moe-appliance] GPU supply kill threshold: authorized-channel lead time >12 weeks for two consecutive quarters suspends the L SKU — basis: judgment; RTX PRO 6000 showed out of stock at NVIDIA's US store (notes §15 gap 9) and the model buys parts in the order month with delivery the next month.
- **A-p4w-private-moe-appliance-6** [p4w-private-moe-appliance] Substitute kill threshold: a <=$25k desktop running a 1T-class model at INT4 at >=15 tok/s for 4 concurrent users removes the L box's reason to exist — basis: judgment; Mac Studio M5 Ultra 512GB is $22,299 and cannot hold 1T at INT4 today (LLM Configurator snippet).
- **A-p4w-private-moe-appliance-7** [p4w-private-moe-appliance] Roofline sanity check: 12-channel DDR5-6400 = 614 GB/s theoretical; Kimi-K2.5 ~32B active parameters at INT4 = ~16 GB read per token, so ~38 tok/s ceiling; the model's 17 tok/s is ~45% of it — basis: arithmetic (12 x 6,400 MT/s x 8 B); used only to show the model figure is not above physics.
- **A-p4w-private-moe-appliance-8** [p4w-private-moe-appliance] The workload that most needs 1T-class quality (agentic coding, long multi-step legal reasoning) is the one that strains a CPU-decode box most, because agent loops make many long-context calls that each pay the ~20 s TTFT floor — basis: judgment from model §2 TTFT and concurrency rows.
- **A-p4w-private-moe-appliance-9** [p4w-private-moe-appliance] Recurring share of revenue computed by summing the model's monthly rows (BASE 18.4% of 36-month revenue; GLUT 23.1%; SEVERE 27.8%; 25.7% of m36 BASE revenue) — basis: `simulate()` in models/private-moe-appliance.py, scratch probe, no model change.
- **A-p4w-private-moe-appliance-10** [p4w-private-moe-appliance] Recurring share of m36 gross profit ~43% — basis: m36 BASE fleet 22.3 boxes x blended subscription cost ~$286/box-month (L $317, S $255) gives ~$6.4k cost against $21.1k subscription revenue, so ~$14.7k of $33.5k GP; ignores partner commission.
- **A-p4w-private-moe-appliance-11** [p4w-private-moe-appliance] A later T1 raise is sized at ~$0.5M — basis: a seller plus a field tech for ~2 years at the model's $10k and $7.5k/month loaded costs (~$420k) plus buffer; only after >=3 MSP/RPO partners each close a box a month (notes §9).
- **A-p4w-private-moe-appliance-12** [p4w-private-moe-appliance] Third-party equipment leasing offered to buyers as a GTM option, not modelled — basis: HPE sells its Private Cloud AI bundle on a 36-month FMV lease (HPE snippet); the model books cash sales only.
- **A-p4w-private-moe-appliance-13** [p4w-private-moe-appliance] Licence status of SGLang (Apache 2.0), llama.cpp (MIT), DeepSeek weights (MIT), Kimi K2.x weights (modified MIT with attribution threshold) and Nemotron (NVIDIA Open Model License) is from training data [UNVERIFIED-training]; only KTransformers (Apache 2.0) was opened, and Inkling's Apache 2.0 is snippet-grade.
- **A-p4w-private-moe-appliance-14** [p4w-private-moe-appliance] Vendor staff who touch a customer's ITAR technical data during support must be U.S. persons, so any contractor must be a U.S. person — basis: standard ITAR practice [UNVERIFIED-training]; consistent with AWS GovCloud restricting ITAR inference to U.S. persons (AWS ML blog snippet).
- **A-p4w-private-moe-appliance-15** [p4w-private-moe-appliance] Business-hours support during the founder's day job needs a named backup contractor before the first delivery (m8), even though the model uses only 24 contractor hours in BASE — basis: judgment; the model treats founder hours as a monthly budget, not as availability during the working day.

</details>

<details><summary><b>p4w-provenance-recert</b> (11)</summary>

- **A-p4w-provenance-recert-1** [p4w-provenance-recert] Verdicts are POSSIBLE yes / PROFITABLE marginal / DOABLE yes — basis: m§3–m§6. 85% of BASE revenue is 15%-GM recert, ARR at m36 is $434–446k across decks, and CleanBOM close rate, churn and the ITAD buy fraction are all unmeasured.
- **A-p4w-provenance-recert-2** [p4w-provenance-recert] Variant runs (early turn `turn_month=12`; `buy_frac=0.75` in GLUT; CleanBOM close = 0; `_cb_delay=6` in GLUT; `_close_mult=0.7` with the slip) use `simulate()`/`metrics()` from the unmodified model — basis: these stress combinations are not printed by the model. The reproduction command is in §2.6 of the deep dive.
- **A-p4w-provenance-recert-3** [p4w-provenance-recert] Full-time gate adds ">= 5 paying CleanBOM subscribers" to the model's EBITDA >= $12k and cash >= $25k trigger. The model does not include this condition — basis: in the GLUT + 6-month FAR-slip variant the founder quits in Dec-27 and is back at the day job by Feb-28.
- **A-p4w-provenance-recert-4** [p4w-provenance-recert] Kill track C requires at least one of the three commitments to be cash (a $900 pack or a prepaid pilot) — basis: an LOI costs the buyer nothing.
- **A-p4w-provenance-recert-5** [p4w-provenance-recert] Kill track B passes only if the die source is identified on at least 3 of 4 samples. Its cost ($600/sample) and time (15 business days) lines are carried from the notes §9.
- **A-p4w-provenance-recert-6** [p4w-provenance-recert] Intermediate kill lines are my settings, set at or just below the model path (m§2 BASE): m6 trailing recert contribution 12% (model 15%) and 150 modules (model 155); m12 at least 1 subscriber plus 3 packs (model 1.5 subscribers); m18 at least 7 subscribers (model 7.5; must-be-true 10).
- **A-p4w-provenance-recert-7** [p4w-provenance-recert] Glut stop-line of a 32GB DDR4 at ~$69 = $125 x 0.55. This is the index at which GLUT lot buying collapses in m§2 (Sep-28).
- **A-p4w-provenance-recert-8** [p4w-provenance-recert] PMem buying continues past 2027-09-30 only if trailing contribution from non-VMware buyers is at least 20% — basis: m§1b today GM is 23%; vSphere 8 EoGS is 2027-10-11.
- **A-p4w-provenance-recert-9** [p4w-provenance-recert] A US8468422 FTO read costs ~$1–2k — basis: judgment for a single-patent attorney read; not sourced.
- **A-p4w-provenance-recert-10** [p4w-provenance-recert] The federal channel advisor is commission-only, so the model carries no fixed cost for the role — basis: keeps the T0 budget intact; not sourced.
- **A-p4w-provenance-recert-11** [p4w-provenance-recert] The CleanBOM glut-demand sign is treated as ambiguous. Cheaper Korean and U.S. bits could pull OEMs off CXMT and shrink demand; cheaper CXMT bits could gain share and grow it. The model holds demand flat — basis: Phase 3 scorers argued only the "raises demand" side.

</details>

### Phase 5 — red team

<details><summary><b>p5-PHY</b> (8)</summary>

- **A-p5-PHY-1** [p5-PHY] Shop-floor permanent magnets (dial-indicator bases, magnetic chucks, NdFeB trays) reach ~0.1-1 T (80-800 kA/m) at contact — basis: typical ferrite/NdFeB surface fields; not measured; compared with Everspin 16Mb parallel Hmax_write 8,000 A/m (AN 02049, via snippet).
- **A-p5-PHY-2** [p5-PHY] 2026-27 U.S. ITAD RDIMM flow contains essentially no CXMT die — basis: 2018-22 server vintage, OEM DIMM qualification lists, CXMT server-grade parts arriving 2024-26; to be falsified by kill-track B.
- **A-p5-PHY-3** [p5-PHY] Step-crossing probability for a 10% reclaim ≈ 22-33% for homogeneous fleets — basis: P ≈ r/(1−r) × S_k/(S_{k+1}−S_k) with 1.33-1.5× channel-balanced DIMM steps, uniform requirement within a step.
- **A-p5-PHY-4** [p5-PHY] ~1-2 agent-attributable panics/yr on a 2,157-node book — basis: Schroeder et al. 2009 ~1.3% machines/yr with UEs × ~5% of RAM in the zswap pool (10% reclaim at 2:1).
- **A-p5-PHY-5** [p5-PHY] Swap writeback 100-200 GB/day/node and ~1 DWPD boot M.2 — basis: 51 GB reclaimed × 2-4 cold-set turnovers/day; typical boot-class SSD rating (verify per SKU).
- **A-p5-PHY-6** [p5-PHY] Heavy-ion SEE campaign ~$10-30k — basis: beam time at TAMU/LBNL plus boards and travel; order of magnitude only.
- **A-p5-PHY-7** [p5-PHY] 32 KB macro at 99% yield needs per-bit failure <~4e-8 (~5.4σ) — basis: 1−0.99^(1/262,144).
- **A-p5-PHY-8** [p5-PHY] Llama-3-70B KV ≈ 0.33 MB/token — basis: 80 layers × 8 KV heads × 128 dim × 2 (K,V) × 2 B (fp16).

</details>

<details><summary><b>p5-VC</b> (7)</summary>

- **A-p5-VC-1** [p5-VC] DD1 CleanBOM addressable buyers that cannot rely on an upstream certification ≈ 20–40 compatible-module/white-box builders plus a few hundred SEWP/GSA resellers; 40 × $30k + 300 × $9k ≈ $3.9M at 100% share — basis: DD1 §3 buyer list and $750/$2,500 tiers; no census of these firms exists in the repo.
- **A-p5-VC-2** [p5-VC] DD1 working-capital gap at m10 ≈ $40k B2B receivables (net-30 on ~55% B2B share of $82.3k recert revenue) + $20–30k held eBay payouts — basis: models/provenance-recert.py BASE m10 row; eBay new-seller hold ~14–30 days and ~10 item/$500 limits (snippets logged in p5-VC.jsonl).
- **A-p5-VC-3** [p5-VC] Combined income + self-employment tax on pass-through EBITDA ≈ 25–35% — basis: general U.S. pass-through rates; none of the five models provisions tax.
- **A-p5-VC-4** [p5-VC] DD2 price-driven module removal would cut BASE m36 ARR toward ~$250k — basis: 39% price-driven share of m36 revenue in models/lifecycle-intel.py §6 applied to $421,548.
- **A-p5-VC-5** [p5-VC] DD3 i-series Fanuc controls (0i/16i/18i/21i) accept CF-in-PCMCIA for SRAM backup; pre-i controls are the ones needing true SRAM cards — basis: IMD 0i-Mate CF backup procedure and Memex 16/18-B/C manual (snippets); not confirmed against a Fanuc maintenance manual.
- **A-p5-VC-6** [p5-VC] DD4 credible 1-hour-response kernel on-call costs "several thousand $/month" — basis: judgment; $750/month buys ~4 h at the model's $175/h.
- **A-p5-VC-7** [p5-VC] DD5: 204 of 298 funnel projects rest on estimates (150 pure ESTIMATE rows + 54 from an estimated second wafer.space run/yr) — basis: models/open-memory-ip.py INPUTS.

</details>

<details><summary><b>p5-VET</b> (7)</summary>

- **A-p5-VET-1** [p5-VET] Stress variants for DD1 (fail_rate 0.08 / return_rate 0.05; mix_ddr5_64 0; buy_frac 0.70; b2b_price_factor 0.75; lab_cost $1,200) are plausible downside values, not point estimates — basis: decommissioned-DIMM CE-driven retirement, absence of ECC-corrected reporting in memtest86+ on Xeon Scalable, DDR5 platform age (2022-23 launch), B2B buyers' own lot+test cost.
- **A-p5-VET-2** [p5-VET] Pre-i Fanuc share of the installed base ≈ 0.15 (vs DD3's 0.35 incl. i-series) — basis: i-series (16i/18i/21i/0i) accept CF-in-PCMCIA for boot-menu SRAM backup (IMD, snippet); rough split, not sourced.
- **A-p5-VET-3** [p5-VET] Credible 24/7 kernel on-call with 1–2 h SLA ≈ $3k/month — basis: ~15 reserved hours at $175/h plus availability premium; judgment.
- **A-p5-VET-4** [p5-VET] Outside-lab ESD/temperature/insertion qualification for a PC Card ≈ $5–10k — basis: typical small-lot qual-lab pricing; judgment, unsourced.
- **A-p5-VET-5** [p5-VET] FM18W08 cycle time ≈ 130 ns vs 70 ns access, address latched on /CE falling — basis: recollection of Infineon/Cypress datasheet; flagged "verify" in the objection.
- **A-p5-VET-6** [p5-VET] GF180MCU open-PDK wafers likely run in Singapore — basis: wafer.space Singapore-based (Crowd Supply snippet) and 01_LANDSCAPE §6 listing no GF180MCU at GF's U.S. fabs; UNVERIFIED.
- **A-p5-VET-7** [p5-VET] Flip Feng Shui (Razavi et al., USENIX Security 2016) cited from training knowledge; URL not opened, so not logged as a source.

</details>

<details><summary><b>p5r-legacy-dram-diebank</b> (22)</summary>

- **A-p5r-legacy-dram-diebank-1** [p5r-legacy-dram-diebank] L1 managed die-bank programs are switched off (l1_enabled 1 -> 0) because the OEM's all-in cost of banking die ($186k-347k) is 2.9-5.4x a packaged LTB plus dry storage (~$64k) — basis: model §10b on Phase 4 inputs; RT-HYP/VC/VET-DD7-01.
- **A-p5r-legacy-dram-diebank-2** [p5r-legacy-dram-diebank] Packaged-part LTB plus dry or N2 storage at the CM costs the part price plus ~$3,000 over the program life — basis: reviewer VET "a few thousand dollars"; GEIA-STD-0003B practice; no quote.
- **A-p5r-legacy-dram-diebank-3** [p5r-legacy-dram-diebank] U.S. package and test for an L1 pull is $10-12.11/die — basis: Phase 4 pull_margin_unit note ($10 OSAT) and the L3 stack ($11.50 / 0.95).
- **A-p5r-legacy-dram-diebank-4** [p5r-legacy-dram-diebank] Study-to-program conversion 0.35 -> 0.10, because Micross sells LTB procurement, N2 storage and pulls direct (EDSP) — basis: Micross EDSP pages via search 2026-11-01; RT-VC-DD7-02.
- **A-p5r-legacy-dram-diebank-5** [p5r-legacy-dram-diebank] Burn-in plus hot/cold at-speed insertions add $10/die to the L3 pull stack (low end of the reviewer's $10-20) — basis: RT-VET-DD7-03; Mercury 100% burn-in datasheet.
- **A-p5r-legacy-dram-diebank-6** [p5r-legacy-dram-diebank] Pull yield of bare die stored 10+ years in N2 is 0.90 (was 0.95) — basis: no published bondability/yield data; Infineon 36-month wafer limit; RT-PHY-DD7-03.
- **A-p5r-legacy-dram-diebank-7** [p5r-legacy-dram-diebank] Storage surveillance (annual sample assembly, test, bond pull/shear) costs $5,000 per bank per year — basis: judgment, ~one small OSAT lot plus lab work a year.
- **A-p5r-legacy-dram-diebank-8** [p5r-legacy-dram-diebank] Opened wafers are packaged whole and stored as packaged parts — basis: thinning and saw are whole-wafer steps; Rochester's 17-year data covers packaged parts; RT-PHY-DD7-04.
- **A-p5r-legacy-dram-diebank-9** [p5r-legacy-dram-diebank] Blended aftermarket multiple 2.0x = 50/50 of 2.5x (DFARS-bound buyers) and ~1.5x (non-DFARS buyers capped by recovered hyperscaler DDR4 in 2028-30) — basis: RT-HYP-DD7-04; the 50/50 split follows 5 of the 10 named customers being non-DFARS.
- **A-p5r-legacy-dram-diebank-10** [p5r-legacy-dram-diebank] A legacy-OCM 8Gb DDR4 die is ~75 mm2 (range 60-90), giving 736 good die per 300 mm wafer at 85% yield; a 12,500-die bank is 17 wafers — basis: RT-PHY-DD7-05; gross-die formula in model §10f.
- **A-p5r-legacy-dram-diebank-11** [p5r-legacy-dram-diebank] A stacked/RDL 8 GB x72 build costs $90 substrate + $160 assembly — basis: RT-PHY-DD7-01 estimate; no OSAT quote.
- **A-p5r-legacy-dram-diebank-12** [p5r-legacy-dram-diebank] MCM module yield 0.76 (3% per-die fallout at a 125 C screen/bin on unburned distributor KGD, 0.97^9) — basis: RT-VET-DD7-04 lower bound, combined with RT-PHY-DD7-02.
- **A-p5r-legacy-dram-diebank-13** [p5r-legacy-dram-diebank] Building at a QML-38534 line adds $200k to MCM NRE ($1.4M -> $1.6M) — basis: judgment for line audit and qualification plus competitor margin; RT-VET-DD7-06.
- **A-p5r-legacy-dram-diebank-14** [p5r-legacy-dram-diebank] Per-lot TID/SEL/hot-retention requalification costs $75k/yr from the evaluation lot — basis: judgment (one heavy-ion + Co-60 campaign a year with test boards and analysis); RT-VET-DD7-04.
- **A-p5r-legacy-dram-diebank-15** [p5r-legacy-dram-diebank] Probability that a DRAM OCM grants a new U.S. entity authorized-aftermarket rights within 15 months is <=5% — basis: likely OCMs are extending lines (Winbond LTAs to 2030, ISSI to 2038); Micron placed continuity with e2v/ATP/Alliance; judgment.
- **A-p5r-legacy-dram-diebank-16** [p5r-legacy-dram-diebank] Probability of a written rep offer to a part-time solo rep is 0.25 — basis: Intelligent Memory filled its 2026 EOL channel with Sourceability and Flip; judgment.
- **A-p5r-legacy-dram-diebank-17** [p5r-legacy-dram-diebank] The 5% L2 commission is kept but unverified; search found only generic 5-15% rep ranges (technology/manufacturing) — basis: smallbiztrends via search 2026-11-01.
- **A-p5r-legacy-dram-diebank-18** [p5r-legacy-dram-diebank] NIST SP 800-171 / CUI compliance for DoD-facing study work costs ~$35k one-off + ~$500/month (reviewer figure from DoD's regulatory cost model via Secureframe); the reported 2026-07-13 CMMC Phase-2 suspension was not verified — basis: RT-HYP-DD7-02.
- **A-p5r-legacy-dram-diebank-19** [p5r-legacy-dram-diebank] AS9120B in year 1 costs $35k over m2-m6 plus $8k/yr surveillance — basis: Phase 4 Plan B inputs moved earlier; RT-HYP-DD7-03.
- **A-p5r-legacy-dram-diebank-20** [p5r-legacy-dram-diebank] Residual Plan A keeps the Phase 4 fixed cost base ($680/month + $2,500/yr conference); a lean $300/month variant is shown separately — basis: no objection asked for lower costs; avoids tuning the residual upward.
- **A-p5r-legacy-dram-diebank-21** [p5r-legacy-dram-diebank] The month-1 one-off becomes $3,900 ($500 employer review + $900 rep-agreement review + $2,500 LLC/legal); the $6,000 kill test is not run — basis: concept killed; RT-HYP-DD7-06, RT-VC-DD7-03.
- **A-p5r-legacy-dram-diebank-22** [p5r-legacy-dram-diebank] Automotive-grade DRAM above 95 C exists with derated refresh, so 125 C is a bin-and-derate problem, not an impossibility — basis: prior knowledge [UNVERIFIED-training]; did not change the disposition.

</details>

<details><summary><b>p5r-lifecycle-intel</b> (14)</summary>

- **A-p5r-lifecycle-intel-1** [p5r-lifecycle-intel] contributor_share 0.40 -> 0.25: only line-item memory buyers (not EMS-turnkey) whose legal function signs off despite supplier-confidentiality terms contribute PO prices — basis: RT-VET-DD2-04, RT-HYP-DD2-02; no survey data exists.
- **A-p5r-lifecycle-intel-2** [p5r-lifecycle-intel] seed_contributors = 5 from m3: the revised K4 pass bar is >=10 signed non-subscriber agreements; assume half deliver usable 24-month line-item history — basis: judgment; RT-VC-DD2-01.
- **A-p5r-lifecycle-intel-3** [p5r-lifecycle-intel] panel_min_contributors = 15: minimum for >=3 grade-homogeneous cells with >=5 independent buyers per quarter, allowing cross-cell overlap — basis: RT-VET-DD2-01, RT-PHY-DD2-02; not statistically derived; the VET bootstrapped-noise test is the real gate.
- **A-p5r-lifecycle-intel-4** [p5r-lifecycle-intel] index_rate 0.60 -> 0.40 licences/month at full volatility: TrendForce contract prints and open-book pass-through are the default; scope narrowed to SMB OEM->customer surcharges — basis: TrendForce 2018-11-05 (8GB module contract base), TrendForce 2025-12-05 (Dell/Lenovo list-price hikes), via snippet.
- **A-p5r-lifecycle-intel-5** [p5r-lifecycle-intel] vol_down_weight = 0: a falling price adds no index demand beyond the floor — basis: no index-linked down-adjustment found for 2018-19 or 2023 (one search, 2026-11-01); Unipi surcharge "reduced once memory prices normalize".
- **A-p5r-lifecycle-intel-6** [p5r-lifecycle-intel] index_churn_falling = 3%/month while the 3-month move is below -5% — basis: judgment; surcharges withdrawn in a falling market (RT-VET-DD2-03).
- **A-p5r-lifecycle-intel-7** [p5r-lifecycle-intel] trial_conversion 0.12 -> 0.10 — basis: free Octopart BOM tool and distributor PDN e-mails substitute for plain EOL alerts (RT-HYP-DD2-04); HYP's 0.08 run as a variant.
- **A-p5r-lifecycle-intel-8** [p5r-lifecycle-intel] trials_cap_pt 25 -> 20 qualified trials/month — basis: 15 h/week ~ 65 h/month; 20 demo hours leaves ~45 h for product, crawler, panel, content (RT-VC-DD2-06).
- **A-p5r-lifecycle-intel-9** [p5r-lifecycle-intel] trials_at_launch 6 -> 4 and saas_launch_month 5 -> 6 — basis: no day-job-peer trials without a written carve-out; carve-out before code and PCN parsing in MVP (RT-VC-DD2-05, RT-PHY-DD2-05).
- **A-p5r-lifecycle-intel-10** [p5r-lifecycle-intel] Nexar Standard $600/mo, Pro $2,000/mo, display licence $2,000/mo — basis: prices unpublished (Nexar compare-plans, 2026-11-01, via snippet); midpoint of Phase 4 guesses and HYP stress values.
- **A-p5r-lifecycle-intel-11** [p5r-lifecycle-intel] Antitrust: $5,000 written opinion at m2 plus $400/month compliance retainer from index publication — basis: judgment on boutique-counsel rates; DOJ/FTC 2023 withdrawal of information-exchange safety zones and DOJ 2024 RealPage complaint [UNVERIFIED-training].
- **A-p5r-lifecycle-intel-12** [p5r-lifecycle-intel] LTB study COGS 30% -> 35% of price and ltb_attach 1.5% -> 1.25%/month — basis: storage/attrition/solderability section per study (J-STD-033, GEIA-STD-0003); 2026 LTBs filled subject to allocation (RT-PHY-DD2-04, RT-VET-DD2-06).
- **A-p5r-lifecycle-intel-13** [p5r-lifecycle-intel] U.S. SMB OEM TAM 6,000 -> 3,000 (range 2,000-4,500) — basis: NAICS 334 = 9,698 firms all sizes (Mewayz aggregator, via snippet, not Census-verified) x ~35% with 20-499 staff + ~600 electronic medical-device firms, x ~70% buying memory line-item = ~2,400; the share assumptions are judgment.
- **A-p5r-lifecycle-intel-14** [p5r-lifecycle-intel] Kill-test budget +$500 for the founder's own attorney to review the employment agreement before requesting the carve-out (K0) — basis: judgment.

</details>

<details><summary><b>p5r-memory-efficiency</b> (15)</summary>

- **A-p5r-memory-efficiency-1** [p5r-memory-efficiency] Incremental reclaim over a stock Proxmox baseline (KSM on via ksmtuned, ballooning on) is 6% of installed RAM, not 10% — basis: KSM default-on on Proxmox (forum snippets); Google fleet zswap ~5%; HYP's 6% run; zswap-only on boot media and ~0 on hugepage/SEV/TDX hosts.
- **A-p5r-memory-efficiency-2** [p5r-memory-efficiency] Savings share negotiated to 20% (from 30%) — basis: on-prem "DIMMs not bought" is a counterfactual, not an invoice line; procurement benchmarks against Ubuntu Pro/RHEL support (RT-HYP-DD4-01).
- **A-p5r-memory-efficiency-3** [p5r-memory-efficiency] Value realization 0.75 of linear GB x $/GB — basis: rental-equivalent of 36 months of freed capacity = P0 - PV(40% residual of 3-yr-old DIMMs at P36) at 8%/yr = 68% (flat prices) to 78% (BASE -30% turn). VC's pure-deferral P0 - PV(P36) = 44% in BASE ignores the extra life of later-bought DIMMs.
- **A-p5r-memory-efficiency-4** [p5r-memory-efficiency] DIMM-step quantization is mean-neutral across buyers: with requirements uniform between steps, E[saving] = P(cross) x step = (r x S/dS) x dS = r x S. It is modeled as a conversion loss (pilot_to_sub 0.60 -> 0.40), not as a value cut.
- **A-p5r-memory-efficiency-5** [p5r-memory-efficiency] DDR5 share of node-GB at target fleets 0.40 (from 0.60) — basis: SMB MSP fleets on 4-6-yr refresh still mostly DDR4 in late 2026; DDR5 is ~40-65% of server DRAM *revenue* (higher $/GB), so installed GB share is lower; reviewers proposed 0.30.
- **A-p5r-memory-efficiency-6** [p5r-memory-efficiency] Credible on-call (named rotation, 1-2 h SLA) costs $2,500/mo at 1-5 customers and $3,000/mo at 6+ — basis: midpoint of HYP $2,000 and VET ~$3,000; no quote obtained.
- **A-p5r-memory-efficiency-7** [p5r-memory-efficiency] Tech E&O covering production-impact claims $400/mo — basis: Insureon $67-110/mo average, Vouch startup median $308/mo, x1.3 for higher limits; HYP's $600 treated as an upper bound.
- **A-p5r-memory-efficiency-8** [p5r-memory-efficiency] scan_to_pilot 0.30 (from 0.40) — basis: DIY admin with free upstream features is the competitor; no SOC 2; HPC segment removed (RT-VC-DD4-05, RT-PHY-DD4-03, RT-VET-DD4-03).
- **A-p5r-memory-efficiency-9** [p5r-memory-efficiency] SOC 2 Type I is asked for at 2 customers, not 5 (RT-VC-DD4-05).
- **A-p5r-memory-efficiency-10** [p5r-memory-efficiency] Kill criterion 9 (stop new C-74 acquisition below 60% of peak DDR5 price before 8 customers) is wired into the model; it fires at M22 in GLUT and M20 in SEVERE, never in BASE (-30% turn).
- **A-p5r-memory-efficiency-11** [p5r-memory-efficiency] C-75 is off in the revised headline because the DD's own recommendation drops it; shown as a sensitivity only.
- **A-p5r-memory-efficiency-12** [p5r-memory-efficiency] C-73 audits at 0.17/month part-time (~2/yr) from a manufacturing (not SaaS) network (RT-VC-DD4-06).
- **A-p5r-memory-efficiency-13** [p5r-memory-efficiency] Channel threshold: a partner would need ~4,500 (10% reclaim) to ~7,900 (6% reclaim) pure-DDR5 VM-host nodes at a 25% revenue share to carry one $10k/mo salary plus fixed ops at BASE peak prices — computed in models/memory-efficiency.py §7. An operator that large has its own kernel staff, so the condition contradicts the target buyer.
- **A-p5r-memory-efficiency-14** [p5r-memory-efficiency] Uncorrectable-error panics attributable to zswap: rate ~ nodes x 1.3%/yr (Schroeder 2009, per PHY) x pool share (3% of RAM at 6% reclaim, 2:1) = ~0.18/yr at the revised M36 book of ~456 nodes; ~1.4/yr at PHY's 2,157-node, 5% pool case.
- **A-p5r-memory-efficiency-15** [p5r-memory-efficiency] DD4 final status KILLED: the 29-day ~$6k experiment is cancelled because no PASS outcome changes the ceiling (revised model: kill-test best case BASE ARR M36 $14.8k, cash -$85.4k).

</details>

<details><summary><b>p5r-nv-continuity-modules</b> (21)</summary>

- **A-p5r-nv-continuity-modules-1** [p5r-nv-continuity-modules] Pre-i Fanuc controls (15, 16/18-A/B/C, 20/21-B; RJ-2 robots) are 15% of 5M cumulative Fanuc CNCs, and 40% are still running. — basis: VET's ~0.15 estimate; these controls are 26–38 years old. Series 0-C may have no card slot [UNVERIFIED], which would push the share lower.
- **A-p5r-nv-continuity-modules-2** [p5r-nv-continuity-modules] i-series residual demand = 20% share (i-A, early i-B, 0i-A/B) × 60% still running × 20% residual SRAM-card need. — basis: boot-menu backup works on CF (IMD), but an 18i-T needs SRAM for normal-mode I/O and a 16iA user hit an NMI when formatting a CF card (CNCzone). There is no OEM manual excerpt either way.
- **A-p5r-nv-continuity-modules-3** [p5r-nv-continuity-modules] The other-families multiplier is 1.35, down from 1.5. — basis: Mitsubishi FA-A-0184 points High-speed Universal QCPU users to SD cards.
- **A-p5r-nv-continuity-modules-4** [p5r-nv-continuity-modules] The addressable market is U.S. × 1.10 (Canada) plus 15% of non-U.S. demand. — basis: a plain memory card with no cryptography is very likely EAR99 [ESTIMATE, unconfirmed], so eBay and a web store can reach some foreign buyers. Every named reseller is North American.
- **A-p5r-nv-continuity-modules-5** [p5r-nv-continuity-modules] BASE volume is 16 cards/month steady state (7% of SAM, 14% of U.S. demand). — basis: a part-time new entrant's share; Phase 4's 40/month would be 36% of revised U.S. demand.
- **A-p5r-nv-continuity-modules-6** [p5r-nv-continuity-modules] Card demand decays 10%/yr after launch. — basis: ~6%/yr pre-i retirement plus ~4%/yr self-depletion, since each battery-free card removes an 8-year replacement.
- **A-p5r-nv-continuity-modules-7** [p5r-nv-continuity-modules] Logic rises to $9 (2MB) / $10 (4MB), up from $5/$6. — basis: dual-supply 74LVC16T245-class translators (~$1 each), a small CPLD (~$2–3), a supervisor and a hold-up cap.
- **A-p5r-nv-continuity-modules-8** [p5r-nv-continuity-modules] A magnetic shield costs $3 per card. — basis: Ni-Fe/mu-metal foil die-cut to the MRAM footprint, or a ferritic-steel cover. Whether it fits inside the Type I envelope must be bench-checked.
- **A-p5r-nv-continuity-modules-9** [p5r-nv-continuity-modules] Connector and frame cost $15, and a 350-set lifetime buy is made at m9. — basis: no current-production card-side quote found; 350 = 288 modeled cards m11–m36 × 1.2.
- **A-p5r-nv-continuity-modules-10** [p5r-nv-continuity-modules] Outside-lab qualification costs $7.5k. — basis: midpoint of VET's $5–10k (IEC 61000-4-2 ESD, temperature, insertion life).
- **A-p5r-nv-continuity-modules-11** [p5r-nv-continuity-modules] Bench time on two more control families costs $3k. — basis: rental at CNC repair houses instead of buying two more controls.
- **A-p5r-nv-continuity-modules-12** [p5r-nv-continuity-modules] Product liability with a $1–2M COI costs ~$250/month. — basis: small-business general and product-liability policy [ESTIMATE].
- **A-p5r-nv-continuity-modules-13** [p5r-nv-continuity-modules] No ISO 9001 certification is budgeted. — basis: $5–10k plus audits is unjustified at this volume; resellers that require it are treated as unreachable.
- **A-p5r-nv-continuity-modules-14** [p5r-nv-continuity-modules] A CNC field-service technician is retained at $150/month from launch, and returns are 6%. — basis: VC-06; the founder has no Fanuc service knowledge.
- **A-p5r-nv-continuity-modules-15** [p5r-nv-continuity-modules] Card launch moves from m9 to m11. — basis: pre-i bench, three-family qualification, outside lab and rev-B respin before the first 100-card lot.
- **A-p5r-nv-continuity-modules-16** [p5r-nv-continuity-modules] Only ~$4 of the $12 PLP capacitor BOM is removable with an MRAM journal. — basis: PHY-07 paired-page hold-up requirement; the founder owns no FTL.
- **A-p5r-nv-continuity-modules-17** [p5r-nv-continuity-modules] Disposition rule: ACCEPTED-DOWNGRADE when an accepted objection alone lowers 36-month net by ≥$5k or narrows scope; ACCEPTED-MITIGATED otherwise. — basis: the marginal-impact runs (revert each revision group from the revised model).
- **A-p5r-nv-continuity-modules-18** [p5r-nv-continuity-modules] FINAL STATUS is KILLED, not DOWNGRADED. — basis: revised BASE 36-month net −$29.8k, peak cash $49.2k > $40k, founder never paid, recurring ARR $2.7k. Breakeven needs 33 cards/month with no supporting evidence. The reviewers rated it "side business at best"; the re-run model is harsher than they were.
- **A-p5r-nv-continuity-modules-19** [p5r-nv-continuity-modules] A $1.2k demand-only reopen probe is kept, at ≥30 full-list deposits plus a ≥100-card/yr reseller LOI, or a ≥200-card/yr white-label commitment. — basis: 36-month breakeven needs ~33 cards/month. A probe costs little against the TAM chain's wide uncertainty (one reported anchor × eight estimates).
- **A-p5r-nv-continuity-modules-20** [p5r-nv-continuity-modules] The reprice-to-$299 supply-failure path is dropped. — basis: price ×1.2 still loses $16.9k in revised BASE.
- **A-p5r-nv-continuity-modules-21** [p5r-nv-continuity-modules] Four of five WebSearch calls were used (connector supply, Fanuc pre-i cards, battery-free competitor, DLA/NSN demand). — basis: shared budget of 5.

</details>

<details><summary><b>p5r-open-memory-ip</b> (19)</summary>

- **A-p5r-open-memory-ip-1** [p5r-open-memory-ip] ChipFoundry sky130 full-chip projects ~30/yr (was 60) — basis: the Phase 4 input note's own "2-3 shuttles/yr at >=50% fill ~20-30 paid slots"; Efabless chipIgnite peak ~43/yr (RT-VC-DD5-01).
- **A-p5r-open-memory-ip-2** [p5r-open-memory-ip] Cadence SKY130 MPW ~20 projects/yr (was 30) — basis: only one 2026 run documented (RT-VC-DD5-01).
- **A-p5r-open-memory-ip-3** [p5r-open-memory-ip] MOSIS 2.0 / Commons / other open-PDK full-chip projects ~30/yr (was 60) — basis: no published count; halved (RT-VC-DD5-01).
- **A-p5r-open-memory-ip-4** [p5r-open-memory-ip] Academic share of accounts 0.70 (was 0.60); 0.80 run as sensitivity — basis: named commercial targets are microfirms; SBIR teams going to production move to S130 NDA + bundled compiler (RT-HYP-DD5-03, RT-VC-DD5-05).
- **A-p5r-open-memory-ip-5** [p5r-open-memory-ip] Characterized licence restated as "nominal MPW lot measured at V/T, corners simulated, yield on >=50 die, warranty = re-delivery or refund of fees", priced $12k (was $20k, 1.2x the commercial service fee) and bought at 0.15/commercial account/yr (was 0.25) — basis: MPW slots carry no skew-corner wafers (RT-HYP-DD5-02, RT-PHY-DD5-01, RT-VET-DD5-02, RT-VC-DD5-06).
- **A-p5r-open-memory-ip-6** [p5r-open-memory-ip] DoD/SBIR licence channel 0.04/month (was 0.08) — basis: no SEE/TID data will be funded; U.S.-fab axis covers sky130 only (RT-PHY-DD5-07, RT-VET-DD5-04, RT-HYP-DD5-05).
- **A-p5r-open-memory-ip-7** [p5r-open-memory-ip] Contract VLSI rate $150/h (was $125) — basis: ~20% retainer premium for a 12-month exclusivity / non-compete on free large sky130 macros (RT-VC-DD5-03).
- **A-p5r-open-memory-ip-8** [p5r-open-memory-ip] GF180 characterized m11 (was m10); sky130 characterized m16 before the cash gate (was m13) — basis: TTSKY25b on ChipFoundry CI2511 took ~8 months from submission close (2025-11-10) to expected chips (Jul-2026) (RT-VET-DD5-06, RT-VC-DD5-04).
- **A-p5r-open-memory-ip-9** [p5r-open-memory-ip] Outbound contacts capped at distinct new teams = full-chip projects/yr / 12 (~19/month) — basis: the 120-name list is spent in the m0 kill test; re-contacting the same names does not create new buyers (RT-HYP-DD5-01).
- **A-p5r-open-memory-ip-10** [p5r-open-memory-ip] Academic procurement lag 2 months; academic offer sold as a per-term course pack at $1.2k/term — basis: university vendor registration and POs (RT-HYP-DD5-06; DD4 s7).
- **A-p5r-open-memory-ip-11** [p5r-open-memory-ip] P(free silicon-characterized >=16 KB GF180 macros by m24) = 0.6; expected-value haircut weight = GF180 share of projects (0.65) x 0.6 = 0.39, applied from m24 to close, churn, sub price and licences in every scenario — basis: OCD and Chips4Makers already have GF180 SRAM silicon; DD s5 already conceded GF180 within ~12 months (RT-HYP-DD5-04, RT-VC-DD5-01).
- **A-p5r-open-memory-ip-12** [p5r-open-memory-ip] Large sky130 macro array efficiency 30% (was 60%), context only — basis: OpenRAM 1 KB -> 2 KB adds ~11.5 um2 per added bit, ~6x the bitcell (RT-PHY-DD5-06).
- **A-p5r-open-memory-ip-13** [p5r-open-memory-ip] On-chip BIST + programmable delay-line timing structures: 20 contract h per test chip (GF180 m3, sky130 m6) — basis: ns access time cannot be measured through pins (RT-PHY-DD5-02).
- **A-p5r-open-memory-ip-14** [p5r-open-memory-ip] Thermal-forcing rental ~$2.5k per characterization campaign (ThermoStream-class, ~1 week) — basis: [ESTIMATE] typical rental $2-4k/week; not quoted (RT-PHY-DD5-02, RT-VET-DD5-02).
- **A-p5r-open-memory-ip-15** [p5r-open-memory-ip] Kill test budget ~$9.1k (40 h extracted-SPICE + 1,000-pt Monte Carlo review at $150 = $6.0k; compute $0.3k; web $0.2k; outreach $0.1k; template $1.0k; event $1.5k); $8.1k of it added to the model at m1 — basis: RT-VET-DD5-01.
- **A-p5r-open-memory-ip-16** [p5r-open-memory-ip] Cash gate: deferrable one-time spends wait until cash after the spend stays >= $2.5k — basis: the Phase 4 schedule plus the added spends drives BASE cash to -$8.2k at m11, beyond the $40k deployable (A-03).
- **A-p5r-open-memory-ip-17** [p5r-open-memory-ip] A logic-rule (no SRAM waivers) NMOS-only 3T sky130 gain cell is ~2.0-2.5 um2 before refresh periphery, i.e. no denser than the 1.896 um2 pushed-rule 6T — basis: rough count of ~3 contacted poly pitches x two diffusion rows on sky130 logic rules [ESTIMATE, not a layout]; RT-PHY-DD5-03, RT-VET-DD5-03.
- **A-p5r-open-memory-ip-18** [p5r-open-memory-ip] T2 (C-32 gain cell, C-22 ReRAM chiplet) killed; ReRAM qualification line would be ~$1.0M (was $0.4M) if ever revived — basis: JESD47 on 3 lots (RT-VET-DD5-05).
- **A-p5r-open-memory-ip-19** [p5r-open-memory-ip] P(the strengthened day-30 kill test passes) ~15-25% — basis: judgment; (iv) now needs written no-release statements from UCSC VLSIDA and OCD, (iii) needs extracted-SPICE corners + Monte Carlo, (ii) needs 2 commercial/SBIR LOIs >= $10k that confirm staying on the open PDK.

</details>

<details><summary><b>p5r-private-moe-appliance</b> (27)</summary>

- **A-p5r-private-moe-appliance-1** [p5r-private-moe-appliance] Small-buyer authorized RDIMM price pre-turn = contract $25.78 x 1.65 = $42.5 per user-GB ($2,722 per 64 GB) — basis: DD6's own street $32/GB (Servnet, Aug-26) x reviewer-cited ServerMonkey +35% Aug-Oct = $43; Origin Storage 64GB-6400 GBP 2,516 special (~$52/GB, avoira.com snippet); Fusion $46-58/GB reviewer-cited but not confirmed by me (price not visible in snippet).
- **A-p5r-private-moe-appliance-2** [p5r-private-moe-appliance] The small-buyer premium is a shortage premium; it unwinds to 1.15 across 2028 in BASE and is 1.15 from the 2028 turn in GLUT/SEVERE — basis: judgment; distribution loosens in a glut.
- **A-p5r-private-moe-appliance-3** [p5r-private-moe-appliance] S-SKU GPU = RTX PRO 5000 Blackwell 48GB at $8,216 (SHI listing, MSRP $8,999) — basis: search snippet, undated listing; replaces a $5,000 GeForce RTX 5090 from Micro Center retail.
- **A-p5r-private-moe-appliance-4** [p5r-private-moe-appliance] Decode capacity model: step time = t_fix + distinct-expert multiple x routed GB/token / (peak GB/s x efficiency), uniform independent routing — basis: RT-VET-DD6-01 and RT-PHY-DD6-01 arithmetic; routing skew would lower the distinct-expert multiple slightly (upside not modelled).
- **A-p5r-private-moe-appliance-5** [p5r-private-moe-appliance] Peak bandwidth 576 GB/s (12 x DDR5-6000) — basis: AMD 58462 platform max as cited by RT-VET-DD6-01 [REPORTED via red team]; a 6400-validated board (614 GB/s) is shown as a variant.
- **A-p5r-private-moe-appliance-6** [p5r-private-moe-appliance] Engine bandwidth efficiency 0.50 (0.55 bracket) — basis: P1 (8.73 tok/s on 307 GB/s with ~12.2 GB routed) implies 0.35-0.47 depending on fixed time; newer kt-kernel assumed better; STREAM-class ~0.8 not reachable while syncing a GPU per layer.
- **A-p5r-private-moe-appliance-7** [p5r-private-moe-appliance] Fixed per-step time 20 ms (L, Kimi 61 layers) and 18 ms (S, MiniMax 62 layers) — basis: S value calibrated to reproduce P2 (2S EPYC 9355 + 5090, 32.1 tok/s) at ~0.5 x 1,152 GB/s; L set slightly higher for MLA attention.
- **A-p5r-private-moe-appliance-8** [p5r-private-moe-appliance] Routed bytes per token: Kimi-K2.5 11.9 GB (21.1B routed params at ~4.5 bits), MiniMax-M2.x 7.0 GB (7.0B at FP8) — basis: RT-PHY-DD6-01 config arithmetic.
- **A-p5r-private-moe-appliance-9** [p5r-private-moe-appliance] U.S.-origin models on L scaled by active-parameter ratio on routed bytes (Inkling x41/32, Nemotron 3 Ultra x55/32) — basis: no expert configs found; crude [ESTIMATE].
- **A-p5r-private-moe-appliance-10** [p5r-private-moe-appliance] 2S L variant: 1,152 GB/s at efficiency 0.45 and t_fix 22 ms, +$6.5k BOM for a second CPU and board — basis: RT-PHY-DD6-02 (+~$8.3k quote); LMSYS 'up to 63%' NUMA-aware gain has an unstated baseline.
- **A-p5r-private-moe-appliance-11** [p5r-private-moe-appliance] GPU KV memory: S on 48 GB has 34.8 GB free after 13.2 GB fixed; 124 KB/token FP8 KV; 32k-token design context -> 8 users — basis: RT-PHY-DD6-03 method.
- **A-p5r-private-moe-appliance-12** [p5r-private-moe-appliance] Subscription capped at $50 per named user per month — basis: Phase-4's own anchor (~25 users x $50 = $1,250).
- **A-p5r-private-moe-appliance-13** [p5r-private-moe-appliance] L SKU mix 0 in BASE (not quoted until a socket-pinned measurement passes); re-admission tested at mix 0.25 with efficiency 0.55 — basis: RT-VET-DD6-01 plus the Mac-cluster and U.S.-origin objections.
- **A-p5r-private-moe-appliance-14** [p5r-private-moe-appliance] Close rate 6% (from 8%) — basis: unmeasured; new single-member LLC faces supplier onboarding; CMMC Phase 2 suspended 2026-07-13 (Jenner, McGuireWoods, HSToday snippets).
- **A-p5r-private-moe-appliance-15** [p5r-private-moe-appliance] Sales cycle 7 months (from 4) — basis: section 4's own motion: discovery, 60-day paid pilot, 3-6 month security review, PO.
- **A-p5r-private-moe-appliance-16** [p5r-private-moe-appliance] 50% of founder-sourced orders go on a VAR/MSP contract vehicle at a 5% fee — basis: RT-HYP-DD6-01; judgment on regulated-buyer procurement.
- **A-p5r-private-moe-appliance-17** [p5r-private-moe-appliance] Insurance $900/month (from $500) for $1-2M cyber/E&O + GL + product liability — basis: judgment; cf. RT-HYP-DD1-08 response ($600 for E&O alone).
- **A-p5r-private-moe-appliance-18** [p5r-private-moe-appliance] Channel partners take 15% of hardware and 20% of subscription and bring 2 conversations a month from m13 — basis: RT-VC-DD6-06 (MSP incentive vs building its own box).
- **A-p5r-private-moe-appliance-19** [p5r-private-moe-appliance] Annual subscription churn 30% (from 20%) — basis: RT-VC-DD6-04; air-gapped patches/model refreshes are work the buyer's MSP can do.
- **A-p5r-private-moe-appliance-20** [p5r-private-moe-appliance] Business-hours backup technician retainer $500/month from first delivery — basis: RT-VC-DD6-03 sensitivity range ($500-1,000).
- **A-p5r-private-moe-appliance-21** [p5r-private-moe-appliance] 4 founder hours per qualified conversation (from 3) — basis: adds security questionnaires, SSP inserts, pilot support.
- **A-p5r-private-moe-appliance-22** [p5r-private-moe-appliance] Spare pool: one spare RDIMM per 5 boxes plus one 48 GB loaner GPU at 5 boxes, held as inventory; parts reserve 4%/yr — basis: RT-VET-DD6-06, RT-HYP-DD6-06.
- **A-p5r-private-moe-appliance-23** [p5r-private-moe-appliance] Demand elasticity to price rises 0.5 against the Phase-4 card ($62,525 L / $30,622 S) — basis: low end of RT-VC-DD6-01's -0.5..-1.0 range because OEM servers inflate with the same DRAM; copy-cat integrators would make it higher.
- **A-p5r-private-moe-appliance-24** [p5r-private-moe-appliance] 3% of BOM drift absorbed between approved quote and purchase, with a DRAM/GPU index clause covering the rest — basis: RT-HYP-DD6-07.
- **A-p5r-private-moe-appliance-25** [p5r-private-moe-appliance] Install 12 h per box (from 8) for electrical/thermal survey and closet/colo placement — basis: RT-PHY-DD6-04.
- **A-p5r-private-moe-appliance-26** [p5r-private-moe-appliance] Founder economic profit = 36-month net after tax minus unpaid part-time hours x $85, treating a full-time salary as equal to the day-job wage forgone — basis: RT-VC-DD6-05 method.
- **A-p5r-private-moe-appliance-27** [p5r-private-moe-appliance] 'Kill-test pass' case = close rate 8%, 6-month cycle, 3 channel conversations a month — basis: what K1/K3 passing with cash would plausibly show.

</details>

<details><summary><b>p5r-provenance-recert</b> (16)</summary>

- **A-p5r-provenance-recert-1** [p5r-provenance-recert] Central buy fraction moved 0.65 -> 0.70 of realized resale — basis: no published ITAD lot price (re-searched 2026-11-01, none found); open-market lots list near 1.0x resale (PCSP); Iron Mountain keeps the spread; hyperscalers redeploy DDR4 (RT-HYP-DD1-04). 0.70 is the reviewers' own test value; nothing found points below 0.65.
- **A-p5r-provenance-recert-2** [p5r-provenance-recert] B2B price 0.88 -> 0.80 of eBay realized — basis: B2B accounts buy the same lots and test in-house; their ceiling is their landed cost (~0.75-0.80, RT-HYP-DD1-05). Top of the range because per-serial test records add some value.
- **A-p5r-provenance-recert-3** [p5r-provenance-recert] eBay share at m12 0.40 -> 0.50 — basis: with B2B at 0.80 the operator keeps more volume on eBay; capped at 0.50 for single-seller absorption.
- **A-p5r-provenance-recert-4** [p5r-provenance-recert] CE-reject protocol fallout 7%, returns 3%, 15 min/module, +$500 soak box — basis: between C_notes (3%/2%) and VET's 8%/5% (which applied to the old memtest-only protocol, where escapes become returns).
- **A-p5r-provenance-recert-5** [p5r-provenance-recert] DDR5 share of lots 3% — basis: DDR5 servers shipped from Nov-22/Jan-23; 5-6-year lives; residual = excess/new-pull stock.
- **A-p5r-provenance-recert-6** [p5r-provenance-recert] Monthly unit caps 300 part-time / 450 full-time — basis: HYP-04 supply retention; still above HYP's 200/month test threshold.
- **A-p5r-provenance-recert-7** [p5r-provenance-recert] eBay new-seller caps 20/50/100 units in the first three selling months, eBay payout held one month in those months, B2B net-30 — basis: VC-04 snippets (nifty.ai, closo, auctionnudge).
- **A-p5r-provenance-recert-8** [p5r-provenance-recert] Tax provision 30% on positive taxable income (EBITDA after salary, capex expensed, loss carry-forward), paid monthly — basis: VC-07; pass-through LLC with federal + state + SE tax.
- **A-p5r-provenance-recert-9** [p5r-provenance-recert] PMem fallout 10%, returns 5% — basis: PHY-05/VET-07 (passphrase-locked modules, platform mismatch); no data.
- **A-p5r-provenance-recert-10** [p5r-provenance-recert] Library samples must be NEW third-party DDR5 RDIMMs at ~$600 each (16-32GB at ~$25/GB contract), 1 sample/month m4-18 then 0.5 — basis: recert flow is OEM DDR4 with ~zero CXMT (PHY-01, HYP-02, VC-02); library re-keyed on package marking (PHY-02, VET-02).
- **A-p5r-provenance-recert-11** [p5r-provenance-recert] Lab $600/sample all-in — basis: VET-06 minimum-lot and report charges; plan at the track-B ceiling until written quotes exist.
- **A-p5r-provenance-recert-12** [p5r-provenance-recert] CleanBOM close 5% (both bundle and standalone), high tier 10%, packs 10% — basis: the three FATAL objections are accepted: the module-maker buyer already holds die source and may self-certify, so the remaining buyers are refurb/odd-lot resellers and white-box builders; no library lift remains.
- **A-p5r-provenance-recert-13** [p5r-provenance-recert] E&O $600/month — basis: published tech E&O range ~$500-9,000+/yr (Insureon snippet); premium for government-reliance exposure without a regulatory exclusion is unquoted.
- **A-p5r-provenance-recert-14** [p5r-provenance-recert] "Track C passes" variant restores the Phase 4 CleanBOM demand inputs (close 10%, high tier 35%, packs 15%); "track A passes" uses buy 0.62, the 8%-contribution line at revised inputs.
- **A-p5r-provenance-recert-15** [p5r-provenance-recert] FINAL STATUS = KILLED as a venture candidate: at post-red-team central inputs recert earns -1%/module and CleanBOM reaches 5.3 subscribers ($58k ARR) by m36 with the founder never full-time; even if both kill tracks pass, BASE reaches $227k ARR with full-time only at m32, and GLUT/SEVERE never pay the founder.
- **A-p5r-provenance-recert-16** [p5r-provenance-recert] X-ray die outline is triage only — basis: CXMT G4 16Gb DDR5 die ~67-68 mm2 vs current Samsung ~49 mm2, but 2021 first-generation big-3 16Gb DDR5 dies were ~66-72 mm2 (3DNews citing TechInsights, snippet).

</details>

### Phase 6 — decision

<details><summary><b>p6-first90</b> (15)</summary>

- **A-p6-first90-1** [p6-first90] Each 30-minute qualified call costs 0.67 founder-hours including prep and notes — basis: LI §10 says 30-minute calls; 10 min notes/follow-up added.
- **A-p6-first90-2** [p6-first90] No prospect outreach, domain or Sales Navigator before K0 is signed; the K6 21-day clock starts at the first outreach message (no later than 2026-11-09, so the window closes no later than 2026-11-29) — basis: J-INT/J-EV Monday actions ("no code, domain or Sales Navigator until K0"); LI §10 K6 wording.
- **A-p6-first90-3** [p6-first90] Building the 60-name list from public sources in week 1 (before K0) is allowed on personal time/equipment — basis: it is not code and contacts nobody; judges bar code, domain, Sales Navigator and contact only.
- **A-p6-first90-4** [p6-first90] The $1,000 government-contracts consult is deferred until K3+K4 pass, so planned November spend is $1,950 of the ~$2,950 LI §10 budget — basis: DEC MOONSHOT.spend.
- **A-p6-first90-5** [p6-first90] Call distribution 2/8/10/5 across weeks 2–5 (25 total, $50 each) — basis: scan ready end of week 3; Surcharge Reference v0 written in week 4 before index-prospect calls.
- **A-p6-first90-6** [p6-first90] Pace marker of ~17 calls booked by 2026-11-22 (day 14 of a 21-day window) — basis: linear pace of 25/21 days; a warning only, not a threshold.
- **A-p6-first90-7** [p6-first90] DD5 no-release reply requested by 2026-11-20 (day 19, inside OM §10's days 7–20); final cut-off 2026-12-01 — basis: DEC "silence = fail"; J-INT (day 14) and J-EV/J-CEIL (12-01) differ.
- **A-p6-first90-8** [p6-first90] Holiday weeks (2026-12-21, 2026-12-28) carry ~8 h (Branch A) or ~5 h (Branch B) — basis: Christmas and New Year.
- **A-p6-first90-9** [p6-first90] Branch A: deposits credited to the first invoice at the m6 paid launch; K1 re-test (if K5 fails) by 2027-01-08 — basis: LI §11 #4 gives no re-test date.
- **A-p6-first90-10** [p6-first90] Branch A monthly opex $650 in Dec and Jan (tools $250, marketing $300, accounting $100) — basis: LI.py §4 rows m1–m2 and inputs.
- **A-p6-first90-11** [p6-first90] Branch B: separate written DD5 carve-out requested 2026-12-02, required by 2026-12-18 — basis: J-CEIL ("first get a separate written carve-out for DD5").
- **A-p6-first90-12** [p6-first90] Branch B tranches: $1.6k (compute, web/Stripe, outreach, licence template) → $6.0k contractor only after test (ii) passes, cut-off 2027-01-29 → ≤$1.5k hub event; decision 2027-02-10 — basis: OM §10 line items; J-EV sequencing; J-INT window 2027-01-11 → 02-10.
- **A-p6-first90-13** [p6-first90] Branch B, if (ii) fails, recommend Branch C rather than OM §10's academic-only GF180 pivot — basis: GF180MCU is Singapore-fabbed (OM §1) and free GF180 macros are expected (P = 0.6 by m24, OM §5).
- **A-p6-first90-14** [p6-first90] Branches B/C refund all DD2 deposits by 2026-12-04 — basis: deposits are refundable (LI §10).
- **A-p6-first90-15** [p6-first90] Branch A cash-low estimates subtract the November test spend from LI.py's cash low because LI.py starts m1 at $40,000 excluding the test — basis: LI.py §4 (m1 cash $39,350 = $40,000 − $650 opex).

</details>

### Other

<details><summary><b>v1-policy</b> (11)</summary>

- **A-v1-policy-1** [v1-policy] The §5949 FAR rule is still only a proposed rule (FAR Case 2023-008, 2026-02-17) on 2026-11-01 — basis: no final rule turned up in two searches; the latest coverage is about the April 2026 comment period. A final rule could have been published without being indexed.
- **A-v1-policy-2** [v1-policy] The 2027-12-23 §5949 effective date holds — basis: it is set by statute (5 years after enactment) and repeated by the FR notice and every law-firm summary. A final rule cannot move it, but it can add phase-ins or exceptions (LexBlog mentions a 2028-12-23 phase-in for commercial items, unconfirmed).
- **A-v1-policy-3** [v1-policy] Part A of §5949 reaches memory chips inside servers, PCs and DIMMs that agencies buy — basis: the proposed rule covers "electronic parts, products or services that include covered semiconductor products" and explicitly applies to COTS and micro-purchases (Clark Hill snippet). This is my reading of the snippets; I did not read the rule text.
- **A-v1-policy-4** [v1-policy] Under the "reasonable inquiry" standard, contractors can mostly satisfy §5949 with supplier certifications. Independent die-level testing will therefore be bought for exceptions and risk cases, not as a blanket requirement — basis: Wiley and LexBlog snippets say no third-party audits are required and reliance on certifications is reasonable. Judgment: this shifts §5949 demand toward attestation and BOM-traceability software and away from lab screening.
- **A-v1-policy-5** [v1-policy] SBIR Phase I/II guideline caps are about $323k and $2.15M — basis: one secondary guide (GovDash). Agencies set their own ceilings, and NSF lists $305k for Phase I.
- **A-v1-policy-6** [v1-policy] Public Law 119-83 is the number of the SBIR/STTR reauthorization — basis: a single secondary source (Inside Government Contracts tag page). Not checked on congress.gov. Kept as STILL-UNVERIFIED.
- **A-v1-policy-7** [v1-policy] The CHIPS Program Office NOFO for materials/equipment facilities (concept-plan deadline 2026-11-01) is effectively closed to this venture — basis: the deadline is today, and the NOFO targets capex facility projects.
- **A-v1-policy-8** [v1-policy] The CRDO BAA is not a realistic T0/T1 funding route — basis: a blog title cites a $10M minimum for white papers (unverified), and 2026 CRDO awards come with an equity stake (NIST 2026-07-29 LOIs).
- **A-v1-policy-9** [v1-policy] The Affiliates Rule cliff most likely moves to 2027-01-10 — basis: Bessent's 2026-09-23 statement and the truce extension. BIS had published no implementing notice by about mid-October 2026, so the rule legally returns on 2026-11-10 unless a notice appears in the next 8 days.
- **A-v1-policy-10** [v1-policy] Memory chips and modules (HTS 8542.32, 8473.30) are not covered by Section 232 Phase 1 unless they are part of an article that meets the TPP/DRAM-bandwidth thresholds — basis: the proclamation is described as "narrowly targeted" at advanced computing chips. DRAM appears only as a bandwidth parameter. I did not see the annex HTS list.
- **A-v1-policy-11** [v1-policy] As of 2026-11-01 no Section 232 Phase 2 (broader semiconductor or memory tariff) has been implemented — basis: no proclamation found after 2026-01-14, and the 2026-07-01 data-center review outcome was not found. Lutnick's 100% memory threat remains rhetoric.

</details>

<details><summary><b>v2-fabs-ip</b> (10)</summary>

- **A-v2-fabs-ip-1** [v2-fabs-ip] Facts from SEC, USITC, Sandia and company releases seen only in search snippets are tagged [REPORTED-P], not [VERIFIED]: no primary document was opened (sec.gov blocked; weebit-nano.com and cse.umn.edu failed DNS) — basis: CONVENTIONS tagging rules plus the task's network note.
- **A-v2-fabs-ip-2** [v2-fabs-ip] Gresham timing: "Toggle/sensor ~18 months, STT ~30 months from effective date" is anchored to 2026-04-08, so ~Q4-2027 and ~Q4-2028 — basis: 10-Q Q1-26 snippet; the effective date may differ slightly from the signing date.
- **A-v2-fabs-ip-3** [v2-fabs-ip] The Microchip TMR non-compete runs to at least 2038 (10-year term + 2 years, longer if renewed) — basis: 8-K snippet wording "during the term ... and for two (2) years thereafter".
- **A-v2-fabs-ip-4** [v2-fabs-ip] Weebit upfront fees ($0.29M DB HiTek, $1.8–2.6M onsemi) are broker estimates (MST Access), not disclosed terms. A fabless startup's fee is assumed to be lower than an IDM's but not T0 (<$50k) — basis: no startup term sheet found; Weebit's smallest known fee was $100k (first licence).
- **A-v2-fabs-ip-5** [v2-fabs-ip] Weebit ReRAM is assumed NOT to be in the ChipFoundry sky130 shuttle offer until shown otherwise — basis: the access path found was Efabless chipIgnite (2024-06), and Efabless closed in early 2025; no successor mention found.
- **A-v2-fabs-ip-6** [v2-fabs-ip] The neutrality risk to memory customers from IonQ owning SkyWater is rated low-moderate — basis: the press concern is specific to rival quantum firms; the CEO statement says customer access and IP protections are unchanged; IonQ could reprioritise capacity toward quantum.
- **A-v2-fabs-ip-7** [v2-fabs-ip] Sandia HZO is downgraded from "likely licensable" to "unconfirmed" — basis: 2 targeted searches found no IP-portal listing or CRADA offer, and the 2026-05-13 article describes internal LDRD; absence of a search hit is not proof of non-availability.
- **A-v2-fabs-ip-8** [v2-fabs-ip] Nantero "leans defunct" rests on one third-party directory tag plus absence of 2025–26 news — basis: apis.io snippet; weak evidence.
- **A-v2-fabs-ip-9** [v2-fabs-ip] OpenRAM version conflict (A3: v1.2.50 on 2026-10-27; snippets: last push 2026-04-17, PyPI 1.2.48) is left unresolved. The snippet aggregators may be stale, so A3's direct GitHub view is likely more current — basis: gittrend/PyPI snippets carry no capture date.
- **A-v2-fabs-ip-10** [v2-fabs-ip] The ChipFoundry price of ~$15k per 100 chips comes from a 2025 eeNews article and is assumed still current in 2026 — basis: no 2026 price list found.

</details>

<details><summary><b>v3-backend</b> (8)</summary>

- **A-v3-backend-1** [v3-backend] I read amcompute's "sold for ~$X–Y over the last 12 months" as realized resale prices for the trailing 12 months to Aug 2026, not as asking prices. Because it is a 12-month window, the current price is probably near or above the top of each range. — basis: amcompute appraisal pages (via search snippet); the page could not be opened (DNS-blocked)
- **A-v3-backend-2** [v3-backend] "Up ~335%" / "~285%" YoY is ambiguous: it could mean ×4.35 or ×3.35. I therefore bracket the implied year-ago prices: 32GB at $23–45, 64GB at $65–130. Both readings agree with the old 2023–24 recall of $25–40 and $50–100. — basis: arithmetic in scratchpad/v3/recheck.py
- **A-v3-backend-3** [v3-backend] I re-ran the §6.6 resale unit-economics model unchanged (buy at 60% of resale, 13.25% fees, $5 shipping, 6 minutes of testing at $25/hr, 3% failures, 3% returns) at the amcompute prices. The model reproduces the original $29.7 contribution at $150, so the inputs were transcribed correctly. — basis: scratchpad/v3/recheck.py (exit 0)
- **A-v3-backend-4** [v3-backend] I kept the 60% buy-in ratio for ITAD lots, but treat it as optimistic. Iron Mountain ALM grew 88–92% YoY in 1H 2026 on decommissioning and pricing. ITAD incumbents are capturing the repricing themselves, so lot prices offered to small buyers are probably above 60% of resale. — basis: Iron Mountain Q1/Q2 2026 call coverage (MarketBeat, via snippet); judgment
- **A-v3-backend-5** [v3-backend] A single distributor listing (Suntsu: ESMT 4Gb DDR4 x16 KGD, 175 die, 2026-05-26) is evidence that legacy KGD can be bought in die-count lots. It is NOT evidence of price, or of lead time ("Contact Us"). — basis: Suntsu listing (via snippet)
- **A-v3-backend-6** [v3-backend] I treat the "Samsung licensing deal" with Netlist as reported but unconfirmed: I saw only headlines (Panabee, Finanztrends). Its terms and scope (which patents, whether DDR5 PMIC claims are covered) are unknown. — basis: headline-only snippets
- **A-v3-backend-7** [v3-backend] I attribute the Amkor "~$12B" figure to GPEC (2026-09-08) only. It is not confirmed by an Amkor release, so I report the $7B two-phase plan as the confirmed figure and ~$12B as the latest reported one. — basis: GPEC snippet; AnySilicon/Amkor IR snippets
- **A-v3-backend-8** [v3-backend] Used DDR4 RDIMMs at $3.1–5.8/GB sit at roughly 7–28% of the DDR4 8Gb chip spot price ($21–44/GB). I read the gap as mostly a die-format mismatch: server x4 die cannot go onto the consumer x8/x16 boards that the spot price reflects. The 2026 counterfeit cases of re-soldered DDR4 chips on fake DDR5 boards show the gap is being arbitraged illicitly. — basis: arithmetic plus Tom's Hardware/Profesional Review snippets; judgment

</details>

<details><summary><b>v4-cost</b> (18)</summary>

- **A-v4-cost-1** [v4-cost] The industry 1β 16Gb DDR5 die base is 36.5 mm² (0.438 Gb/mm²), the mean of Micron D1β DDR5 (35.83 mm², die seal) and Samsung D1b LPDDR5X (36.68 mm²). SK hynix 1b is assumed similar — basis: TechInsights figures seen in search snippets; ETN.fi says the Samsung D1b cell is "similar to SK hynix D1b".
- **A-v4-cost-2** [v4-cost] The 1β high case keeps the old 41 mm² (0.39 Gb/mm²) to cover possibly larger Samsung/SK hynix DDR5 periphery. LPDDR5X and DDR5 are treated as equal density on the same node — basis: no SK hynix or Samsung 1b DDR5 die size found.
- **A-v4-cost-3** [v4-cost] "Die seal" area is used, not full-die area (35.83 vs 36.00 mm²). The ~0.5% difference is ignored — basis: TechInsights reports both, and the model's scribe lane covers the rest.
- **A-v4-cost-4** [v4-cost] 1γ/1c 16Gb base density is 0.55 Gb/mm² (29.1 mm²). Micron's ">30% bits per wafer over 1β" implies ≥0.58. The base is discounted for Samsung's reportedly larger 1c die — basis: Micron 1-gamma brief via snippet; Samsung enlargement is p1-cost prior knowledge [UNVERIFIED].
- **A-v4-cost-5** [v4-cost] Micron's "bits per wafer" claim is read as a gross-die ratio, ignoring yield differences — basis: standard usage in Micron node announcements.
- **A-v4-cost-6** [v4-cost] 24Gb and 32Gb dies scale linearly with 16Gb density, with no array-efficiency gain for larger dies — basis: no 24/32Gb die area found (Samsung 32Gb ISSCC 2024 paper 13.2 gives no area in snippets).
- **A-v4-cost-7** [v4-cost] The Samsung 16Gb DDR5 die of 48.90 mm² (XenoSpectrum/3DNews; node not stated) is used only as the low end of the 1α range — basis: its density (0.327 Gb/mm²) fits 1α, not 1β.
- **A-v4-cost-8** [v4-cost] The 4Q26 64GB RDIMM contract anchor is $1,650 (low $1,500, high $1,930) — basis: Counterpoint's Apr-2026 3Q26 forecast (~$1,500) × TrendForce 4Q26 conventional DRAM +10–15% gives $1,650–1,725; Citi 4Q26F is $1,586. Low = 3Q26 flat (buyers sought flat 2H26). High = Counterpoint 1Q26 actual $927 × TrendForce 2Q (+60.5%), 3Q (+15.5%) and 4Q (+12.5%) midpoints.
- **A-v4-cost-9** [v4-cost] Blended conventional-DRAM QoQ forecasts apply to server RDIMM contract prices — basis: same convention as p1-model. Server DRAM was the tightest segment in 2026, so this is if anything conservative.
- **A-v4-cost-10** [v4-cost] Derived DDR5 16Gb 4Q26 contract price = (RDIMM anchor − $20.6 non-DRAM BOM and assembly) / 40 dies — basis: p1-cost method (cost_stack.md §7) with the model's non-DRAM BOM.
- **A-v4-cost-11** [v4-cost] The claimed October TrendForce revision of 4Q26 DRAM contract prices to "~+20%" is unconfirmed. It is used only as the high end of `contract_dram_qoq_4q26f` — basis: the only source is an AI-generated StockHub summary (2026-10-20); no TrendForce release was found.
- **A-v4-cost-12** [v4-cost] EUV scanner price is ~$290M, from SK hynix's KRW 11.95T (~$8.8B) order for "30+" tools. The "+" is ignored, and service or High-NA mix in the package is not separated — basis: S&P Global 2026-03 via snippet. If the order holds more than 30 tools, the unit price is lower.
- **A-v4-cost-13** [v4-cost] The 2026 28nm 300mm foundry base is $2,800, a blend of TSMC ~$3.0k (Silicon Analysts estimate) and UMC/SMIC/Hua Hong ~$2.0–2.5k after the 2026 hikes of up to +10% — basis: no non-TSMC 28nm absolute price found.
- **A-v4-cost-14** [v4-cost] The 200mm 180nm absolute price stays at $700; only the high end rises to $1,150 for the confirmed 2026 hikes of +5–20% — basis: no public 180nm $/wafer found. The hikes are relative and diverge by foundry (TrendForce Mar-2026).
- **A-v4-cost-15** [v4-cost] HBM3E 2026 price range is $8.33–12.8/GB. Fubon's $17–18/GB is treated as buyer-side system cost and kept out of the range — basis: DigiTimes via Capital & Compute; Silicon Analysts; TrendForce News (Fubon).
- **A-v4-cost-16** [v4-cost] The 72Mb QDR-II+ broker price ($12.36 @1,088 to $33.70 @1) stands in for discrete SRAM $/MB, with 72Mb = 9 MB — basis: no 288Mb QDR price found; broker prices are volatile and quote-based.
- **A-v4-cost-17** [v4-cost] Wafer-cost inputs ($3.4k/$3.8k/$4.3k) are left unchanged, although the model's 4Q26 GM (93%) now sits 6–7 pp above reported Micron/Nanya GMs — basis: no public DRAM wafer-cost estimate found, so changing them would trade one guess for another. The gap is flagged instead.
- **A-v4-cost-18** [v4-cost] A new confidence tag, REPORTED-P (primary document seen only through a search snippet), is added to cost_inputs.json. `models/dram_cost_stack.py` treats it like REPORTED when it displays a source — basis: task instruction for Phase 1b.

</details>

