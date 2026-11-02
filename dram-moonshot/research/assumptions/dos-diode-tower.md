# Assumptions: dos-diode-tower (DIODE-TOWER dossier, 2026-11-02)

- [dos-diode-tower] Cell topology is plate | ZrO2 | recessed node ring (Schottky anode) | thin IGZO shell | metal core pillar, with one IGZO access transistor and one IGZO gain FET (plus read select) per pillar — basis: FINAL_CONCEPTS.json decisive-experiment stack "TiN plates / ZrO2 / recessed node / oxide Schottky / pillar".
- [dos-diode-tower] Hole 60 nm, node recess 15 nm, plate 25 nm, ILD 25 nm, plate web 20 nm, slit 60 nm every 4 rows — basis: critic-corrected planning case plus 3D-NAND-like block slits; gives 121 nm pitch, 0.0165 um2 per pillar.
- [dos-diode-tower] IGZO shell 15 nm (default), fully depleted, ohmic core — basis: concept unspecified; 15 nm keeps anode field ~0.9 MV/cm; thinner shells raise image-force and TFE lowering sharply (model section 4).
- [dos-diode-tower] Image-force permittivity = optical (~4); static (~12) used as optimistic bound — basis: transit to barrier maximum ~10 fs, faster than lattice polarisation; IGZO refractive index ~2 (training knowledge).
- [dos-diode-tower] TFE lowering from triangular-barrier WKB optimum (dE*/3), uncertain +/-50% — basis: first-principles estimate; must be measured on thin-shell coupons.
- [dos-diode-tower] Barrier inhomogeneity: Gaussian patches, sigma 0.05 eV default, patch size = shell thickness (pinch-off scale) — basis: Werner-Guttler/Tung picture; literature sigma ~0.03-0.15 eV [UNVERIFIED range, training knowledge].
- [dos-diode-tower] a-IGZO m* = 0.34 m0 (A* = 40.9 A/cm2K2), static eps 12 — basis: training knowledge, not searched.
- [dos-diode-tower] Literature barrier values are low-field (~0.2 MV/cm) apparent barriers from thick films — basis: diode structures in cited works are thick-film rectifiers.
- [dos-diode-tower] Retention spec = 100 mV droop on a 0.5 V data swing; tail quantile 1e-4 per tier (RAW-BER contract) — basis: FINAL_CONCEPTS and stage2 I-11559.
- [dos-diode-tower] Post-CDS residual 7 mV (midpoint of 5-10 mV) — basis: concept; the real number is PIXEL-STACK/MARGIN-STACK's key unknown.
- [dos-diode-tower] Cost: base wafer $3,000 + $25/tier, tier yield 0.998 after repair — basis: A1 section 6 scenarios ($20-45/tier) and A1 yield requirement.
- [dos-diode-tower] Energy: read/write bitlines 15 fF each, x2 periphery overhead; DDR5 reference 46 fJ/bit from dram_cell_physics.py — basis: ESTIMATE, same overhead convention as A1 model.
- [dos-diode-tower] Plate-swing rule: swing >= Vdata + Vf(0 C) + 0.2 V guard so stored levels sit below the lowest pillar level — basis: model section 7 (pillar-hammer otherwise fails in ~1e2-1e5 accesses).
- [dos-diode-tower] University nanofab industrial rates $75-250/tool-hour; DOE NSRC access free for non-proprietary work — basis: ram-venture 01_LANDSCAPE.md row 16 (rates there marked ESTIMATE), not re-verified.
- [dos-diode-tower] PtOx and AgOx anodes may decompose below ~400 C — basis: [UNVERIFIED: training knowledge]; IrOx/RuOx assumed stable. Coupon run must include post-anneal splits.
- [dos-diode-tower] Founders' lean salaries $75k each per year for 24 months — basis: ESTIMATE consistent with portfolio seed plan (~$265k for two lean salaries across the portfolio).
