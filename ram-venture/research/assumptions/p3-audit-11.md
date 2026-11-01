# p3-audit-11 assumptions (Phase 3 kill pass, batch 11: C-73..C-79), 2026-11-01
- [p3-audit-11] C-79 COGS uses 36-month straight-line depreciation, $250/month colo (the card's figure) and $100/month for IPs, bandwidth and spares — basis: typical small-colo line items; computed in scratchpad audit11_calcs.py
- [p3-audit-11] C-79 glut case assumes a 40% rent cut as Hetzner/OVH reverse their 2026 RAM-driven price increases — basis: 2026 increases of up to 37% (heise) plus the DRAM glut line in 01_LANDSCAPE §10.3
- [p3-audit-11] Used 64GB DDR4 RDIMM priced at $250-370 ($3.9-5.8/GB) — basis: amcompute appraisal data to Aug-2026 (via search snippet)
- [p3-audit-11] C-74 kernel contractor ≈300 h at $150-200/h ≈ $45-60k, which pushes it from T0 to T1 — basis: market contractor rates [ESTIMATE]
- [p3-audit-11] C-76 judged a DUPLICATE of C-50: the same stranded-memory pooling mechanism and axis; software license vs appliance is a business-model lens (mission §E), not a separate concept
- [p3-audit-11] C-77 killed on R4: the named buyer's real alternative is free Linux swap/zswap writeback on the same NVMe, so a paid NAND-as-RAM license wins no axis
