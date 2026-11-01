# Assumptions — p3-audit-04 (Phase 3 kill pass, batch 04: C-23..C-29)

- [p3-audit-04] Used Optane PMem trades at ~$0.5-3/GB (128GB) and ~$0.6-1/GB (256GB) — basis: undated eBay/refurb listings in a 2026-11 search summary; listing dates and monthly volume unverified.
- [p3-audit-04] VMware demand for PMem ends at vSphere 8 end of general support (2027-10-11) — basis: Broadcom KB 459135 and KB 326910 (PMem dropped in VCF 9.0); Broadcom has extended dates before.
- [p3-audit-04] TSMC N5 HD SRAM bitcell = 0.021 um2 — basis: prior knowledge (TSMC IEDM 2019); used to show the 0.03 um2 SOT cell loses on density.
- [p3-audit-04] 512MB LPDDR4X ≈ $10.5 now and ≈ $4 in the A-05 glut — basis: ~$21/GB mobile LTA cited in batch_12 (C-84), minus 60%.
- [p3-audit-04] A new RRAM analog-IMC SoC entrant needs ~$50-150M (T3) to reach revenue — basis: edge-AI chip startup raises (Mythic, EnCharge) [ESTIMATE, prior knowledge].
- [p3-audit-04] Treated C-26 as a SKU of C-62, not as a DUPLICATE kill, because C-62's verdict is not yet known and the buyer pitch (capacity expansion vs like-for-like replacement) differs.
- [p3-audit-04] Octopart/Nexar are Altium properties — basis: prior knowledge; the Renesas-Altium completion itself is via search snippet.
