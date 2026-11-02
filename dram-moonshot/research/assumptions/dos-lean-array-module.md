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

## Red-team revisions (resp-lean-array-module, 2026-11-02)
- [resp-lean-array-module] H2 rotational/translational accommodation ratio r = 0.1-0.3, so the effective a_H2 prior is 0.27 x (4+2r)/6 = 0.19-0.21. Basis: ORNL graphite H2/D2 rotational accommodation 0.05-0.2 (search snippet); RT-DEV-01.
- [resp-lean-array-module] Lognormal 1-sigma factor 1.5 on the effective a_H2 prior; GO judged on the worst of four films, with 1-2 effectively independent draws. Basis: engineering judgement.
- [resp-lean-array-module] D2 at 300 K: k 0.141 W/m/K, mu 1.26e-5 Pa s, gamma 1.40; Baule translational a = He's 0.45; r 0.3-0.6. Basis: prior knowledge, not verified this session.
- [resp-lean-array-module] Radial H2 profile: H2-Ar D = 0.83 cm2/s at 1 atm, chamber 30-80 mTorr, 500-1,500 sccm, 3 cm gap; outer backside zone r > 130 mm. Basis: textbook diffusion; typical HAR etch chamber geometry.
- [resp-lean-array-module] Oxide-cell line: 10-25 % of chucked steps see an exposed or near-surface oxide channel; HAR etch is 30 % of chucked steps. Basis: engineering estimate.
- [resp-lean-array-module] Cryo case: gas at 220 K; He k 0.124, mu 1.61e-5; normal-H2 k 0.139, mu 7.26e-6, Cp 27.7 J/mol/K (gamma 1.43). Basis: prior knowledge, T^0.68-0.7 scaling.
- [resp-lean-array-module] Requalification: 30-80 chamber families x $0.5-3M; greenfield incremental 10 %; 0.5-3 %/yr chance of a 30-day binding cutoff [SPECULATIVE]. Basis: engineering and risk estimates; RT-PROC-05 and RT-IND-04.
- [resp-lean-array-module] AAO: ZrO2 k 40; few-nm TiN 300 uOhm cm; 5 nm TiN at 80 nm pitch; barrier 1.0-1.2 nm/V; ramp-down thinning to 3-5 nm. Basis: prior knowledge [UNVERIFIED-PK].
- [resp-lean-array-module] Fluorocarbon inventory per 1-beta wafer: capacitor mold 1,200 scc, other etches 2,000 scc; MARGIN STACK adds 340; a 3D cell adds 4,000; cryo HF/PF3 cuts FC by 80 % in deep etches. Basis: order-of-magnitude recipe estimates; HF/PF3 from Semiconductor Engineering (snippet).
- [resp-lean-array-module] IGZO 10 nm, 3x area factor, 5 tiers, 30 % utilisation, 6.4 g/cm3; Ga $700/kg. Basis: engineering estimate.
