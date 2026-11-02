# Assumptions: dos-lean-array-module (2026-11-02)

- [dos-lean-array-module] Gas properties at 300 K (k, mu, cp, gamma) are CRC-handbook values from prior knowledge. Basis: standard tables; not web-verified this session.
- [dos-lean-array-module] H2 accommodation planning value 0.20 (range 0.05-0.45). Basis: Baule mass-ratio scaling of Sandia's measured He 0.45 gives 0.27, less a penalty for poorer rotational accommodation; "engineering surfaces 0.2-0.5" (UMich JCP snippet).
- [dos-lean-array-module] ESC gap 10 um, contact conductance 50 W/m2K. Basis: 5-20 um mesa/emboss class; contact through a few % of area.
- [dos-lean-array-module] He backside 15 Torr baseline; clamp-limited maximum 40 Torr; GO allows <=1.5x the He pressure. Basis: typical high-power etch; ESC clamp pressure ~50-100 Torr-equivalent.
- [dos-lean-array-module] 80 % of 2-5 kW bias deposited in the wafer as heat. Basis: engineering judgement.
- [dos-lean-array-module] Wafer-temperature window +/-2 K for HAR fluorocarbon etch. Basis: polymer/selectivity temperature sensitivity, engineering judgement.
- [dos-lean-array-module] Seal leak scales as p/sqrt(M) (molecular), with p^2/mu (viscous) as the upper bound. Basis: flow-regime physics anchored on 0.5 sccm He (US 9,753,463 snippet).
- [dos-lean-array-module] HAR etch recipe 500 sccm total, 420 sccm-equivalent F-atom feed; 50 slm dry-pump purge; 200 sccm RFO. Basis: typical orders of magnitude.
- [dos-lean-array-module] 150 chucked steps x 2.5 min per DRAM wafer, 20 sccm backside He per chamber, giving 7.5 L He/wafer (range 3-30 L). Basis: engineering estimate; it agrees in order of magnitude with Samsung HeRS (~22 L/wafer recovered).
- [dos-lean-array-module] World helium ~160 M m3/yr; DRAM ~17 % of semiconductor wafer starts. Basis: USGS-order value from prior knowledge, not verified this session.
- [dos-lean-array-module] Retrofit cost $50k per chamber, 1,500 chambers per 100k-wpm fab; DRAM revenue $9,500/wafer in the 2026 market. Basis: engineering and market estimates.
- [dos-lean-array-module] Paschen constants are textbook values (He A=3, B=34; H2 5, 130; N2 12, 342; Ar 12, 180), with gamma_se 0.01 for all gases. Basis: Lieberman & Lichtenberg / Raizer from prior knowledge.
- [dos-lean-array-module] AAO: pore = 0.65 x pitch, 11 nm liner + dielectric, ~2.5 nm/V interpore rule, 70 % anodization current efficiency. Basis: B2-01 geometry and the Masuda/O'Sullivan rule from prior knowledge.
- [dos-lean-array-module] IL overlay budget ~F/4, so 10 nm at F = 40 nm. Basis: Stage-2 I-07130 critique.
- [dos-lean-array-module] University nanofab industrial rates ~$100-300/h; NY CREATES 300 mm chamber campaign ~$300k with partner in-kind. Basis: estimate; rates not verified this session.
