# Assumptions: dosw-and-stack (AND-STACK dossier writer), 2026-11-02

All model assumptions are inherited from `research/assumptions/dos-and-stack.md` and `models/and-stack.py` INPUTS. New judgment calls made while writing `dossiers/and-stack.md`:

- [dosw-and-stack] Program month 1 = January 2027; kill-criteria dates are computed from that start — basis: seed close assumed ~2 months after this dossier.
- [dosw-and-stack] Hole-pitch sensitivity (160/170 nm) scales density by (150/p)^2 at fixed wafer cost; component $/GB rescales the back-end adder half by bits and half by die area, as the model does — basis: model structure; gives 7.1x/3.4x and 6.3x/3.1x.
- [dosw-and-stack] Replacement-gate route to the sandwich select plate (SiN/X/SiN select level, X recessed from the hole, SiN replaced by W from slits) — basis: own process reasoning [SPECULATIVE], untested.
- [dosw-and-stack] Doped-poly plates at ~300 ohm/sq would need ~50 um plates (RC ~4 ns) and the I-11544 staircase-free decoder — basis: Elmore 0.38RC with the model's 13 fF/um.
- [dosw-and-stack] Kill thresholds not in the model: 1 fA tail (1 b holds <62 ms, no better than DDR5 32 ms), on/off <1e4 at <=3.5 V swing, sigma_CR >0.06 planar / >0.05 tier-to-tier, endurance <1e10 at 85 C (~8x the 1.3e9 refresh need), non-confined defects >30% with per-tier killer >2% — basis: model sensitivity tables and judgment.
- [dosw-and-stack] Process energy and water per GB fall ~3-5x if they track wafer cost per GB (1.56x wafer cost for 7.7x GB) — basis: cost-as-proxy [SPECULATIVE].
- [dosw-and-stack] $10-50M round contents (16-tier Albany JDA lot, 1-4 Mb bonded test array, 32/64-tier short loops, 15-25 people) — basis: judgment.
