# Assumptions: B1-cellphysics (phase B, lens "NEW CELL PHYSICS")

Agent key `B1-cellphysics`. Written 2026-11-01. The numbers below feed `research/models/B1_cellphysics_estimates.py`, `research/phaseB/B1-cellphysics.json` and `research/phaseB/B1-cellphysics_notes.md`.

## Network and evidence
- [B1-cellphysics] I used 15 of my 15 WebSearch calls and no WebFetch. Every web fact is from a search snippet and carries "(via search snippet)" in `research/sources/B1-cellphysics.jsonl`. Basis: the task's network rules.
- [B1-cellphysics] Some snippet summaries attributed a result to "a Korean group", "one patent" or "an imec paper" while listing several records. Where I could not pin the record, the source log says "attribution not pinned". This applies to: the Hf0.3Zr0.7O2 1e10-cycle result (SKKU vs KAIST record), the imec capacitive-NDRO window (two imec records), the SFG density limit (MDPI record probable) and the bilayer-BN 1e11-cycle FeFET (lab named in the snippet uncertain).
- [B1-cellphysics] Some facts come from training knowledge with no URL found this session. They are tagged [UNVERIFIED] and never given a URL: NEC four-level 4 Gb DRAM (Okuda et al., JSSC 1997); 1970s CCD main-memory parts (Intel/Fairchild); Fujitsu direct-tunnel memory and KAIST URAM; NbO2 threshold-switch/neuristor work (HP Labs lineage); typical Schottky barrier heights on IGZO.
- [B1-cellphysics] Entries marked CROSS-REF in the source log are reused from the A1/A3 and ram-venture logs and were not re-searched. Basis: MISSION rule 4.

## Shared anchors (imported from models/dram_cell_physics.py, A1)
- [B1-cellphysics] The reference values are the A1 model's, not re-derived: 1β cell 1,070 nm², die density 0.447 Gb/mm², array efficiency 0.508, pillar d 21.1 nm × h 1,300 nm at EOT 0.55 nm (Cs 5.41 fF), Cbl = 0.06 fF/cell + 4 fF, VARY 1.05 V, refresh 46 fJ per bit-refresh. Basis: sibling model, imported directly.
- [B1-cellphysics] "Signal charge" means Cs·VARY/2, measured against a mid-rail reference: 2.84 fC, about 17,700 e⁻ at 1β. The areal signal of today's wall is 3.3 µC/cm². Basis: standard charge-sharing definition.

## Card-specific inputs
- [B1-cellphysics] B1-01: AFE ZrO2 induced polarization is 15–25 µC/cm² with 50–70% usable after domain spread. Film k 38 at 6 nm, write level 1.3 V, low precharge 0.35 V. Basis: typical published ranges for Zr-rich AFE films (no URL this session); the usable fraction is my judgement.
- [B1-cellphysics] B1-01: the plateau "retention stretch" assumes a sharp backward branch. A real distribution of switching fields gives less. Basis: idealisation flagged in the card.
- [B1-cellphysics] B1-01, B1-10, B1-11: DRAM endurance need is 1e12–1e15 cycles. A hot row at 1 activation/µs for 5 years gives 1.6e14; refresh alone at 64 ms over 10 years gives 4.9e9. Basis: arithmetic; A3 uses ~1e15 without wear-levelling.
- [B1-cellphysics] B1-02: the Curie–Weiss temperature of HZO-class films is T0 = 450 °C, and r is designed at 0.85 at −10 °C. Basis: judgement. Hafnia's Landau coefficients vary widely, so the hot-corner enhancement could be 1.5–3×.
- [B1-cellphysics] B1-03: gated-diode EOT 1.1 nm (HfO2/ZrO2 gate ~0.8 nm plus accumulation centroid ~0.3 nm); plate swing 2.5 V with 0.5 V threshold/flat-band offset; GAA strip 40 × 10 nm; local bitline 64 cells. Tier footprints of 70 × 230 and 60 × 180 nm are my layout estimates (WL 30 nm + plate 150–200 nm + contact 40 nm in-line; 60–70 nm in-tier pitch). The density break-even uses the A1 density formula only, not cost.
- [B1-cellphysics] B1-04: sense node 1.5 fF including transfer-gate parasitics; transfer-gate bias 100 nA; subthreshold ideality n = 1.3 at 85 °C; 30 ns transfer window. Basis: judgement for a 22–28 nm-class sense amp. The bias–mismatch cancellation is assumed achievable by self-biased precharge (Arimoto lineage), which is not verified.
- [B1-cellphysics] B1-05: four equally spaced levels; level-edge signal is VARY/6 × Cs/(Cs+Cbl); 15 mV level droop budget; IGZO leakage 1 aA. Basis: OCTRAM Ioff <1 aA (CROSS-REF); the budget is my judgement.
- [B1-cellphysics] B1-06: Richardson constant 41 A/cm²K² (m* ≈ 0.34 m0); diode 20 × 20 nm; floating-gate capacitance 0.3 fF; 0.2 V droop. Pure thermionic emission, ignoring tunnelling and defect leakage, so it is optimistic for real Schottky contacts.
- [B1-cellphysics] B1-07: each 16 Gb die has 1.7e10 cells (ECC included); 0.5 V across the latch; 25 nm diodes. Standby budgets are set equal to, and 4× above, today's refresh power (12.2 mW/die). TI's ~50 nW/cell is from a patent snippet citing van der Wagt.
- [B1-cellphysics] B1-08: hex hole pitch 150 nm, as in 3D NAND; channel hole 60 nm; 30 nm word planes; 6 nm gate oxide; 2 V clock swing; 4-phase clocking at 2 gates/bit; 1 ns per shift step; array efficiency 0.60; Dit 1e11–1e12 cm⁻²eV⁻¹. Basis: judgement scaled from 3D NAND geometry. CTE thresholds are pure arithmetic.
- [B1-cellphysics] B1-09: Fowler–Nordheim constants A = 1.54e-6 A·eV/V² and B = 6.83e9 eV^-1.5·V/m; emission area 10 × 10 nm; field enhancement β 2–3; node 0.2 fF. Hold current uses Simmons' low-voltage formula at 1 V across the gap. Work functions: 2.7 eV (LaB6-class), 3.5 eV, 4.5 eV (TiN). Basis: textbook formulas; β and the emission area are judgement.
- [B1-cellphysics] B1-10: per-tier cell 0.030–0.045 µm² in a 3D AND/NOR topology; array efficiency 0.60. Basis: judgement from 3D NAND hole pitch with two vertical S/D lines per channel.
- [B1-cellphysics] B1-11: C_cap 1 fF, read-gate capacitance 0.5 fF, read pulse 0.3 V, ΔC/C of 0.2–1.0. Basis: the imec "window ~8.7" units are ambiguous in the snippet, so I bracket ΔC/C conservatively.
- [B1-cellphysics] B1-12: sliding-FE effective polarization 0.68 µC/cm², converted from ~2.25 pC/m dipole density over 0.33 nm. Basis: typical bilayer-hBN value from training knowledge [UNVERIFIED].
- [B1-cellphysics] B1-13: congruent LiNbO3 coercive field ~21 V/µm. Basis: textbook value [UNVERIFIED]; Mg-doped LN is lower.
- [B1-cellphysics] B1-14: attempt time τ0 = 1 ns; Δ ≥ ln(N·t/τ0) with ≤1 expected flip per refresh interval across the die, before any σ_Δ margin. Basis: standard Néel–Arrhenius estimate.
- [B1-cellphysics] B1-15: at F = 20 nm, rail-group areas are 30F² (1 MTJ), 60F² (4 MTJ) and 100F² (8 MTJ); array efficiency 0.55; N2 SRAM macro ~0.04 Gb/mm² (A1). Basis: judgement.
- [B1-cellphysics] B1-16: PSG field ~1 V/nm (MIT snippet); WO3 density 7.16 g/cm³, M = 231.8 g/mol; reversible Δx = 0.1 H per W in a 2 nm film.
- [B1-cellphysics] B1-17: porphyrin footprint 1–2 nm²; one electron per molecule per redox state.
- [B1-cellphysics] B1-18: capacitor dielectric leakage 1e-8–1e-7 A/cm² at hold bias; cantilever E = 250 GPa, ρ = 3,200 kg/m³; f0 = 0.162·(t/L²)·√(E/ρ); switching ~1/(2 f0) plus pull-in delay; wordline at 1 V with no pump vs 2.9 V pumped at 45% efficiency.
- [B1-cellphysics] B1-19: NbO2 heat capacity 3 J/cm³K; local transition at 1,080 K from an 85 °C ambient; threshold σ of 1–5%. Basis: judgement and textbook transition temperature.
- [B1-cellphysics] Demo budgets: university nanofab time at ~$50–150k per multi-run study; a WGFMU-class pulse tester plus probe station at ~$120–150k; a small MPW tapeout (≤4 mm², 22–28 nm) at ~$80–120k; postdoc/engineer at ~$120k/yr fully loaded. Basis: judgement, not quotes.

## Judgement calls
- [B1-cellphysics] Ideas were judged on physics only (MISSION framing). Density "×1β" comparisons use the A1 die-level 0.447 Gb/mm² and ignore periphery-under-array gains unless a card says so.
- [B1-cellphysics] The "protonic nano-supercapacitor stub" was turned into a 3-terminal gain cell (B1-16). Reason: extracting the stored ionic charge needs the same ~1 V/nm field as writing, so a fast, low-field read is physically contradictory. The rejection is recorded in the notes with its revival condition.
- [B1-cellphysics] Mott insulators (VO2, NbO2) were rejected as storage-node isolators: their off-state conductivity is about 10 orders too high. NbO2 is kept only as a sensing element (B1-19).
- [B1-cellphysics] I wrote a model file under `research/models/` (`B1_cellphysics_estimates.py`). MISSION rule 2 asks for reusable estimates in Python; this follows the A3 precedent.
