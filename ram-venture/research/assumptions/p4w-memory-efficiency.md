# Assumptions — p4w-memory-efficiency (DD4 deep-dive author, as of 2026-11-01)

All model inputs are inherited from `research/assumptions/p4-memory-efficiency.md` and `models/memory-efficiency.py` (re-run, exit 0). Below are only the judgment calls added while writing `04_DEEPDIVES/memory-efficiency.md`.

- [p4w-memory-efficiency] Capital tier is stated as T0 as modeled (100 h contractor MVP, cash low $10.4k) and T1 as carded (~300 h, $45–60k) — basis: model §5; concepts_master.json C-74 verify correction.
- [p4w-memory-efficiency] The ~$6k kill experiment is treated as overlapping the model's M2–M5 build and test-infra spend; if fully additive, the cash low point falls to ~$4.4k ($10.4k − $6k) — basis: model §5 cash low; notes §11 budget.
- [p4w-memory-efficiency] The first 90 days of selling assume the kill experiment passes on 2026-12-01, which is faster than the model (outreach M5, first subscription M8); the model is the base case and the plan is upside — basis: model INPUTS c74_sell_start/c74_agent_ready.
- [p4w-memory-efficiency] Roadmap gates are set at or slightly above the model's BASE expected values (≥1 subscription by 2027-07-31 vs 0.55 expected at M9; ≥3 customers by 2028-01-31 vs 2.57 at M15; ARR ≥ $37.7k at M18), and a venture-continuation gate at 2× base ($75k ARR, ≥8 customers) — basis: model §4a; founder goal of recurring revenue.
- [p4w-memory-efficiency] Kill criterion for reclaim on pilot fleets is a median below 8% (between the 5% sensitivity case, $40.3k M36 ARR, and the 10% base) — basis: model §6.
- [p4w-memory-efficiency] Kill criterion on DRAM price: stop new C-74 acquisition if 64GB DDR5 RDIMM contract falls >40% below the 4Q26 peak (< ~$15.50/user-GB = 0.6 × $25.78) before 8 customers — basis: model §2 fee path; A-05.
- [p4w-memory-efficiency] A kernel cofounder for equity would save ~$24k/yr of on-call at 6+ customers (12 × $2,000) — basis: model INPUTS oncall_large.
- [p4w-memory-efficiency] A freedom-to-operate read by a lawyer is budgeted at ~$2–3k before the first subscription; it is not in the model — basis: ESTIMATE; no patent search was run for DD4.
- [p4w-memory-efficiency] University purchasing (quotes, POs, vendor registration) may add 30–90 days to a sale — basis: ESTIMATE, not researched [UNVERIFIED].
- [p4w-memory-efficiency] Senpai's license was not checked; the deep dive recommends re-implementing the PSI-feedback idea rather than copying code until it is confirmed — basis: no license data in the logged sources.
- [p4w-memory-efficiency] Channel partners (HPC integrators, refurbished-server resellers) are priced at a 20–30% revenue share — basis: research notes §8 [ESTIMATE].
