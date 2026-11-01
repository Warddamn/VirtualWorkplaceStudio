# Assumptions: p5r-nv-continuity-modules (DD3 Phase 5 red-team responses)

Model inputs changed in Phase 5 live in the `RED-TEAM REVISIONS (Phase 5)` block of `models/nv-continuity-modules.py`. This file logs the judgment calls behind them.

## Market and demand
- [p5r-nv-continuity-modules] Pre-i Fanuc controls (15, 16/18-A/B/C, 20/21-B; RJ-2 robots) are 15% of 5M cumulative Fanuc CNCs, and 40% are still running. — basis: VET's ~0.15 estimate; these controls are 26–38 years old. Series 0-C may have no card slot [UNVERIFIED], which would push the share lower.
- [p5r-nv-continuity-modules] i-series residual demand = 20% share (i-A, early i-B, 0i-A/B) × 60% still running × 20% residual SRAM-card need. — basis: boot-menu backup works on CF (IMD), but an 18i-T needs SRAM for normal-mode I/O and a 16iA user hit an NMI when formatting a CF card (CNCzone). There is no OEM manual excerpt either way.
- [p5r-nv-continuity-modules] The other-families multiplier is 1.35, down from 1.5. — basis: Mitsubishi FA-A-0184 points High-speed Universal QCPU users to SD cards.
- [p5r-nv-continuity-modules] The addressable market is U.S. × 1.10 (Canada) plus 15% of non-U.S. demand. — basis: a plain memory card with no cryptography is very likely EAR99 [ESTIMATE, unconfirmed], so eBay and a web store can reach some foreign buyers. Every named reseller is North American.
- [p5r-nv-continuity-modules] BASE volume is 16 cards/month steady state (7% of SAM, 14% of U.S. demand). — basis: a part-time new entrant's share; Phase 4's 40/month would be 36% of revised U.S. demand.
- [p5r-nv-continuity-modules] Card demand decays 10%/yr after launch. — basis: ~6%/yr pre-i retirement plus ~4%/yr self-depletion, since each battery-free card removes an 8-year replacement.

## Costs and plan
- [p5r-nv-continuity-modules] Logic rises to $9 (2MB) / $10 (4MB), up from $5/$6. — basis: dual-supply 74LVC16T245-class translators (~$1 each), a small CPLD (~$2–3), a supervisor and a hold-up cap.
- [p5r-nv-continuity-modules] A magnetic shield costs $3 per card. — basis: Ni-Fe/mu-metal foil die-cut to the MRAM footprint, or a ferritic-steel cover. Whether it fits inside the Type I envelope must be bench-checked.
- [p5r-nv-continuity-modules] Connector and frame cost $15, and a 350-set lifetime buy is made at m9. — basis: no current-production card-side quote found; 350 = 288 modeled cards m11–m36 × 1.2.
- [p5r-nv-continuity-modules] Outside-lab qualification costs $7.5k. — basis: midpoint of VET's $5–10k (IEC 61000-4-2 ESD, temperature, insertion life).
- [p5r-nv-continuity-modules] Bench time on two more control families costs $3k. — basis: rental at CNC repair houses instead of buying two more controls.
- [p5r-nv-continuity-modules] Product liability with a $1–2M COI costs ~$250/month. — basis: small-business general and product-liability policy [ESTIMATE].
- [p5r-nv-continuity-modules] No ISO 9001 certification is budgeted. — basis: $5–10k plus audits is unjustified at this volume; resellers that require it are treated as unreachable.
- [p5r-nv-continuity-modules] A CNC field-service technician is retained at $150/month from launch, and returns are 6%. — basis: VC-06; the founder has no Fanuc service knowledge.
- [p5r-nv-continuity-modules] Card launch moves from m9 to m11. — basis: pre-i bench, three-family qualification, outside lab and rev-B respin before the first 100-card lot.
- [p5r-nv-continuity-modules] Only ~$4 of the $12 PLP capacitor BOM is removable with an MRAM journal. — basis: PHY-07 paired-page hold-up requirement; the founder owns no FTL.

## Judgment calls
- [p5r-nv-continuity-modules] Disposition rule: ACCEPTED-DOWNGRADE when an accepted objection alone lowers 36-month net by ≥$5k or narrows scope; ACCEPTED-MITIGATED otherwise. — basis: the marginal-impact runs (revert each revision group from the revised model).
- [p5r-nv-continuity-modules] FINAL STATUS is KILLED, not DOWNGRADED. — basis: revised BASE 36-month net −$29.8k, peak cash $49.2k > $40k, founder never paid, recurring ARR $2.7k. Breakeven needs 33 cards/month with no supporting evidence. The reviewers rated it "side business at best"; the re-run model is harsher than they were.
- [p5r-nv-continuity-modules] A $1.2k demand-only reopen probe is kept, at ≥30 full-list deposits plus a ≥100-card/yr reseller LOI, or a ≥200-card/yr white-label commitment. — basis: 36-month breakeven needs ~33 cards/month. A probe costs little against the TAM chain's wide uncertainty (one reported anchor × eight estimates).
- [p5r-nv-continuity-modules] The reprice-to-$299 supply-failure path is dropped. — basis: price ×1.2 still loses $16.9k in revised BASE.
- [p5r-nv-continuity-modules] Four of five WebSearch calls were used (connector supply, Fanuc pre-i cards, battery-free competitor, DLA/NSN demand). — basis: shared budget of 5.
