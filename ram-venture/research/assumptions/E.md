# Assumptions — agent E (Phase 2, Branch E: business-model-first)

Written 2026-11-01. Each bullet is one number or judgment call used in `research/phase2/E.json` or `E_notes.md`. The numbers run in the scratch script `e_estimates.py` (reproduced in `E_notes.md` Appendix A; exits 0).

## Research-environment limits (judgment calls)
- [E] The shared WebSearch budget was exhausted before E ran a single search, and WebFetch to rochesterelectronics.com, sandia.gov and technology.nasa.gov failed DNS resolution (host not allowed in this session). E stopped trying further hosts, as the session rules require. Basis: tool errors at 2026-11-01.
- [E] Primary sources E actually opened: the official GSA FAR and DFARS DITA repositories on GitHub, plus the rasdaemon repository. Every other URL is a CROSS-REFERENCE to a sibling agent's log, flagged as such in `sources/E.jsonl`. Basis: CONVENTIONS.md logging rules.
- [E] Tech-transfer portal listings (Sandia, LANL, ORNL, LBNL, ANL, PNNL, NASA T2, AFRL/TechLink, NRL, UMN, Purdue, Penn State, Notre Dame, GT, MIT, Stanford, Cornell, UCSD, Michigan, NC State, ASU, RPI, SUNY Albany) could NOT be queried. No patent number in E's files is verified. Basis: network policy. Queries are listed as a verification queue in `E_notes.md` §6.
- [E] The FAR repo covers FAC 2025-06 (2025-10-01; last commit 2026-03-30) and the DFARS repo's last commit is 2026-06-02. "No §5949 text" holds for those snapshots. A later interim rule, or a Revolutionary FAR Overhaul (RFO) deviation published only on acquisition.gov, could exist unseen. Basis: repo README and commit dates.

## Price deck (inherited)
- [E] DDR5 component contract $15.99/GB (Q4-2026); 64GB RDIMM $20.31/user-GB; glut (−60%) $6.40/GB component and $8.13/user-GB RDIMM; severe glut $1.60/GB; cost floor RDIMM $2.41/user-GB. Basis: `models/dram_cost_stack.py` `ddr5_reference()`.
- [E] DDR5 spot $26.96/GB (DRAMeXchange 16Gb avg $53.92, 2026-08-31), so spot runs about 1.69× contract. Basis: BuySellRAM/DRAMeXchange via p1-backend/B.

## E-03 / E-04 volatility and option pricing
- [E] Annualized contract-price volatility is 44% (from 2024–26 TrendForce QoQ midpoints) or 55% (adding the 4Q18, 1Q19, 1Q23 and 2Q23 downturn quarters). It is computed from quarterly log changes × √4. Missing 2025-Q1/Q3 points are skipped. Basis: `research/phase1/price_series.json`; p1-market §7.1.
- [E] The cap premium uses Black-76 with the forward equal to the Q4-2026 contract price (flat forward = "plateau" consensus), a 4.5% discount rate and T = 1 year. Basis: standard option pricing; consensus plateau (p1-market §7.2).

## E-05 inventory arbitrage
- [E] A newcomer buys at spot + 5% (broker ask) and sells at spot − 5%. Carry is 15%/yr (12% cost of capital, 2% storage/insurance/test, 1% shrink/counterfeit loss). Basis: judgment; broker-market norms.
- [E] Scenario weights for Nov-2027: squeeze 25% (contract ×1.25, spot/contract 1.6), plateau 40% (×1.05, 1.2), soft turn 25% (×0.90, 1.0), early turn 10% (×0.65, 0.9). Basis: p1-market §7.2 analyst spread; spot premiums normally compress as panic fades [ESTIMATE].

## E-06 leasing
- [E] A small lessor pays $1,600 for a 64GB DDR5 RDIMM (between the $1,300 contract price and the $2,064 street price) and carries a 14%/yr cost of capital (non-investment-grade). Basis: judgment.
- [E] Residual at end of 2029 is 50% of the glut new price ($260), or 50% of the cost floor in a severe glut ($77). A lessee who walks in the 2028 glut returns the module for 60% of the glut new price, less 15% remarketing cost. Basis: used/new ratio ≈0.5 in 2023 (p1-backend §6.5); judgment.

## E-07 die bank
- [E] A single-part bank costs $600k (about 30 legacy 300mm wafers at ~$20k; p1-backend gives a $3k–22k/wafer range). Storage, insurance and re-test run 1.5%/yr of basis; U.S. OSAT packaging and test add 35% of die cost. Base case: sell at 3.0× die cost, 15%/yr in years 3–8. Bear: 2.0×, 50% sells. Bull: 4.0×, 95% sells in years 2–6. Basis: authorized-aftermarket pricing of about 1.5–5× original (p1-backend §5.3); judgment.

## E-08 AS6171 lab
- [E] Capex is $650k (X-ray, XRF, decap, used SEM/optical, curve tracer, memory functional tester, ISO/IEC 17025 setup). Fixed costs: 3 FTE at $95k loaded, $60k facility, $40k accreditation and calibration, 7-year depreciation. Revenue is $1,400 per lot against $300 variable cost. Basis: p1-backend §7 ($300k–$1M in-house lab; $500–3,000 per lot outsourced); judgment.

## E-09 reseller
- [E] Federal IT reseller gross margin is 6–10% on commodity memory/servers, with 45-day working capital. Basis: judgment from VAR norms [UNVERIFIED].

## E-10 STTR vehicle
- [E] Probabilities: DoD STTR Phase I award 20% per proposal, Phase II given Phase I 45%, Phase III or customer revenue given Phase II 35%. Timeline: option 2 months + proposal-to-award 5 + Phase I 9 + Phase II 24 + Phase III contracting 6 = 46 months. Basis: judgment from commonly reported DoD SBIR/STTR rates [UNVERIFIED-training].
- [E] The STTR rule lets the PI be employed by the partner research institution. That makes the vehicle compatible with a founder who keeps a day job, but grants are funding, not revenue (A-04). Basis: p1-funding §7.3 [UNVERIFIED-H there].

## E-11 acquisition
- [E] The target is a U.S. server-memory reseller/ITAD buyer with $1.2M EBITDA in 2026 (shortage-inflated), $0.4M in a normal year and $0.2M in a glut. Price is 3.5× trailing EBITDA. Financing: SBA 7(a) with a 10% equity injection, 10-year amortization, 10.5% rate (about Prime + 3). Basis: judgment; SBA terms from training [UNVERIFIED-training].

## E-01 DIMM Health Subscription
- [E] A typical customer has 200 out-of-warranty DDR4 servers × 12 DIMMs = 2,400 DIMMs of 32GB, at $0.75/DIMM-month. Replacements: 1.5%/DIMM-yr (predictive at CE thresholds plus reactive). Spares pool is 2% of covered DIMMs, carried at 20%/yr. Shipping $18 per replacement; hosting/support $0.05/DIMM-month. Recovered DDR4 costs $4.7/GB now and $1.25/GB in a glut. Basis: field-study ranges recalled from training (Google 2009 SIGMETRICS "DRAM errors in the wild": ~8% of DIMMs see a correctable error per year; uncorrectable ~0.2%/DIMM-yr) [UNVERIFIED-training]; p1-backend §6.5–6.6 for recovered prices.

## E-02 index
- [E] 30 licensees at $6k/yr plus 5 enterprise licensees at $24k/yr. Data cost: $25k/yr self-built from distributor APIs, or $120k/yr if a contract-price feed must be licensed for redistribution. Basis: judgment [UNVERIFIED: TrendForce redistribution pricing unknown].
- [E] Memory is 35% of the cost of a memory-heavy industrial/server deliverable. Basis: judgment; p1-backend §3.4 (DRAM is 93–98% of an RDIMM's value).

## E-13 / E-14
- [E] CXL integration bills at $225/hr: 8 billable h/week part-time, or 1,100 h/yr full-time. Basis: judgment.
- [E] Patent radar: 25 subscribers at $4,800/yr. Basis: judgment; an FTO opinion costs $10–30k (p1-ip §4).

## Judgment calls on scope and overlap
- [E] The LTB/die-banking seed was carded as a title-taking, authorized-aftermarket die bank (E-07). This differs from C-04, a consignment vault holding OEM-owned stock.
- [E] The GPO/co-op seed was not re-carded because C-15 covers it.
- [E] §5949 compliance was carded as a reseller model (E-09). This differs from C-07 (verification subscription) and D-11 (SPD scanner).
- [E] The Optane seed was carded as an IP-estate acquisition (E-12) to avoid duplicating A2-10, A2-11 and B-09.
- [E] A used-memory residual-value index was considered but not carded, because it overlaps C-05's graded-price index.
