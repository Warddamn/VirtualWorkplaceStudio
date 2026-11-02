# Assumptions: dos-and-stack (AND-STACK dossier), 2026-11-02

- [dos-and-stack] Hole 90 nm on a 150 nm hex pitch with 15% slit overhead (0.0224 um2 per hole) — basis: concept card pitch; 90 nm (not 100 nm) keeps a 24 nm plate web after an 18 nm ring recess.
- [dos-and-stack] Tier = write plate + select plate, 80 nm pitch; ring 18 nm tall x 10 nm radial; IPD 6 nm Al2O3-rich (EOT 2.5 nm); read-gate EOT 3 nm; film 5 nm — basis: first-principles layer budget, NAND-class layer thicknesses.
- [dos-and-stack] "Sandwich" select plate (conductive sacrificial interlayer recessed between two plate metals) lets the select plate wrap the ring on three faces (wrap = 1); back-face-only (Micron FG-NAND-style) is wrap = 0 — basis: own process proposal, untested.
- [dos-and-stack] Topology closure: write with the BL and SL pillars at the same data voltage so one film can charge the ring through the write-plate channel — basis: own analysis; the concept card's "same film" wording does not close without it or without per-level film segmentation.
- [dos-and-stack] Hole-top pillar-select gate per select group (2 hole rows) cuts unselected blocks off the local BL; 75 nm top-BL pitch -> SADP — basis: NAND string-select practice.
- [dos-and-stack] Oxide FET: mobility 20 cm2/Vs, Vt 0.5 V, SS 90 mV/dec at 85 C, 100 nA x W/L at Vt — basis: typical a-IGZO; ALD In2O3 better.
- [dos-and-stack] Coupling-ratio spread sigma 0.03 — basis: judgment on recess-depth/IPD-thickness variation across tiers (Lam notes recess variation along the stack).
- [dos-and-stack] Random level-placement terms: verify 8 mV, read/RTN 8 mV, kick spread 5% of 130 mV — basis: judgment.
- [dos-and-stack] Wafer cost = $2.5k periphery + $0.5k bond + $1.0k array base + $30/tier; die yield = 0.95 x 0.97 x 0.97 x tier-erasure term; p_tier 1% per die, 10% of tier defects not confined, 64 erasure groups, 2 spares — basis: concept card cost ranges; A1 tier-yield framing; judgment.
- [dos-and-stack] Back-end (probe/test/package) adder = 1-beta's $0.24/GB scaled half by bit count and half by die area — basis: judgment.
- [dos-and-stack] University nanofab industrial cost $150-175/tool-hour + $150/staff-hour for budgeting — basis: found rates (Notre Dame $124/h access, UNM $250/h assisted, NUFAB ALD $37-77/h academic x2 for companies) and p1-fabs $75-250/tool-hour.
- [dos-and-stack] Used Keysight B1500A + WGFMU and a hot-chuck probe station ~ $85k with AWG and probe cards — basis: judgment, not quoted.
