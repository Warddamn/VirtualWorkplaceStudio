# Assumptions: A1-scaling (phase A bottleneck map)

Agent key `A1-scaling`, written 2026-11-01. Each numeric input is used in `models/dram_cell_physics.py` and `research/phaseA/A1_scaling_limits.md`.

## Network and evidence
- [A1-scaling] Used 25 of 25 WebSearch calls and no WebFetch. Every web fact comes from a search snippet and is tagged "(via search snippet)" in `research/sources/A1-scaling.jsonl` — basis: task network rules.
- [A1-scaling] Unless a fresh 2025–26 search says otherwise, density anchors, wafer costs, EUV $/layer and the device cards are reused from `../ram-venture/` (cost_stack.md §2–3, 01_LANDSCAPE §4/§9, phase2 A1–A3 device params) — basis: MISSION rule 4.
- [A1-scaling] Two snippet facts came back without a pinned URL, so they are tagged [UNVERIFIED] in the text and not attached to a URL: the row-hammer figure "HCfirst 139K (2014) → 4.8K (2020) → 3.2K (2022)" and "memory ~22% of server power, 75–100 W per HBM stack (citing Monolithic Power Systems)" — basis: CONVENTIONS rule "never invent a URL".

## Cell geometry
- [A1-scaling] The 1β cell area of ~1,070 nm² (6F² at F≈13.4 nm) is derived by assuming 1β has the same array efficiency (0.508) as CXMT G4, where the cell area (0.0020 µm²) and die (66.99 mm²) are both reported — basis: no public 1β cell area was found; array efficiency is similar across 6F² BCAT generations [ESTIMATE].
- [A1-scaling] The 1γ/1c cell is ~870 nm² (F≈12.0 nm), scaled by die area from the 29.1 mm² ram-venture estimate — basis: cost_stack.md §3.1 [ESTIMATE].
- [A1-scaling] Array efficiency for 4F² with periphery under the cell (PUC, wafer bonded) is 0.70 — basis: removing SA/SWD/decoder area from the array plane. Some stitch and contact area remains [ESTIMATE, wide range 0.6–0.8].
- [A1-scaling] Capacitors sit on a honeycomb lattice with one site per cell; pillar diameter = lattice pitch − 14 nm (2 × ~5.5 nm dielectric + ~3 nm top TiN) — basis: geometry; the dielectric thickness follows the "6–7 nm high-k" figure in TechInsights/Choe [ESTIMATE].
- [A1-scaling] Storage-node height is 1,300 nm, giving AR ≈ 60 at 1β — basis: aspect ratios of 50–100:1 claimed in Micron-style patents (US 12,193,208; US 2022/0238532), with "AR ≥70 = high" in US 8,962,437. No teardown height was found [ESTIMATE].
- [A1-scaling] EOT is 0.55 nm for the ZrO2-based stack. The pillar model uses the outer wall only — basis: 6–7 nm physical high-k with k_eff ~45–50 including interfaces. Cylinders became pillars ("quasi-cylinder") once the CD got too small for a double-sided electrode (TechInsights/Choe) [ESTIMATE].

## Array electrical
- [A1-scaling] VARY (bitline restore voltage) = 1.05 V; boosted WL = 2.9 V — basis: DDR5 VDD 1.1 V and VPP 1.8 V external rails, with an internal WL pump above VPP [ESTIMATE, training knowledge].
- [A1-scaling] 512 cells per bitline; Cbl = 0.06 fF per cell + 4 fF fixed ≈ 35 fF; so Cbl/Cs ≈ 6.4 at 1β — basis: the historical Cbl/Cs range is ~4–10. Coupling-dominated BL capacitance at tight pitch [ESTIMATE].
- [A1-scaling] Required end-of-retention sense signal = 50 mV (SA offset after compensation ~20 mV 3σ + coupling ~15 mV + guard) — basis: the margin = ΔVBL − (VOS + noise) framing in US 11,763,878; the mV values are [ESTIMATE]; no published offset number was found.
- [A1-scaling] WL capacitance = 0.15 fF per cell, VPP pump efficiency 0.45, VARY regulator efficiency 0.95, ×2 periphery overhead on array energy → ~46 fJ per refreshed bit [ESTIMATE].
- [A1-scaling] Retention halves per ~10 °C above 85 °C — basis: rule of thumb, consistent with JEDEC halving the refresh interval (64 → 32 ms) above 85 °C [ESTIMATE].
- [A1-scaling] A practical BCAT subthreshold swing of ~95 mV/dec at 85 °C (ideal 71.6) is used for the Ion/Ioff decade budget [ESTIMATE].
- [A1-scaling] The 16Gb weakest cell sits ~6.4σ into the retention tail (1 in 1.7e10) — basis: Gaussian-tail arithmetic only. Real retention tails are not Gaussian (VRT, trap-assisted GIDL) [ESTIMATE].

## Refresh, module, system
- [A1-scaling] DDR5 32Gb tRFC = 410 ns — basis: training knowledge; search did not confirm it [UNVERIFIED].
- [A1-scaling] 64GB DDR5 RDIMM draws ~12 W active, ~3 W idle — basis: training knowledge [UNVERIFIED].
- [A1-scaling] Overfetch case: a DDR5 RDIMM subchannel has 10 × x4 dies with 1 KB pages, so one ACT moves 10 KB to deliver one 64 B line + ECC (640 bits) — basis: DDR5 organisation [ESTIMATE, training knowledge].
- [A1-scaling] Accelerator bandwidths: H200 4.8 TB/s, B200-class 8 TB/s, B200-class TDP ~1,000 W — basis: training knowledge [UNVERIFIED]. The H200 700 W is cited (Micron blog).
- [A1-scaling] HBM total energy 3.5 pJ/bit as the central value — basis: 3.44 pJ/bit HBM3E (RPU paper) and 3–4 pJ/bit HBM4 (Dally/36Kr). The 5–7 pJ/bit figures are treated as different scope (host PHY included) [ESTIMATE].
- [A1-scaling] DDR5 off-package energy ~15 pJ/bit (10–20 range) — basis: training knowledge; not found in search [UNVERIFIED].
- [A1-scaling] "3D, no interposer" total energy of 1.3 pJ/bit = core ~0.9–1.0 + Dally's 0.35–0.4 I/O — basis: arithmetic on the cited figures [ESTIMATE].

## 3D DRAM economics
- [A1-scaling] Per-tier lateral 1T1C cell footprints: optimistic 40×300 nm, base 50×600 nm, pessimistic 60×1,000 nm (WL pitch × BL-contact + transistor + horizontal capacitor length) — basis: geometry; the horizontal capacitor must be ~0.3–1 µm long to reach a few fF at ≤60 nm tier thickness [ESTIMATE].
- [A1-scaling] Tier processing cost $20 / $30 / $45 per tier per wafer on top of a $2.8k / $3.0k / $3.4k base (periphery wafer + bonding + common BEOL) — basis: a 3D-NAND analogy scaled up for epi superlattice and lateral recess/fill; no public 3D DRAM cost data [ESTIMATE, low confidence].
- [A1-scaling] Implied per-tier yield 0.891 from SK hynix's 5-tier 56.1% test-wafer yield, assuming independent, unrepaired tiers — basis: arithmetic only. The real test vehicle was not a product die [ESTIMATE].

## Trends
- [A1-scaling] Row-hammer HCfirst extrapolated as log-linear from the 2012–2022 and 2014–2022 data points → ~500–950 by 2026 — basis: arithmetic only; no 2024–26 measurement was found [ESTIMATE].
- [A1-scaling] EUV $165 per wafer per layer ($115–270), $4,308 1c wafer — basis: ram-venture cost_stack.md §2.1/§2.4 [ESTIMATE, reused].
- [A1-scaling] DRAM greenfield capex is ~$145–170k per wpm — basis: ram-venture cost_stack.md §2.1 [UNVERIFIED rule of thumb, reused]. Cross-check: Samsung P5 ~$22B for ~150k wpm of investment ≈ $147k/wpm (secondary sources, unverified).

## Judgment calls
- [A1-scaling] Ranking the bottlenecks weighs cost/bit and density first, then energy/bit, then capital intensity. This follows the MISSION axis order, plus how many other bottlenecks each one gates. The capacitor ranks #1 because it gates 2D scaling, 3D stacking, the sense margin and the voltage floor at once.
- [A1-scaling] HBM is treated as an architecture/packaging bottleneck, not a cell bottleneck, so it ranks below the cell-physics items despite its very large market weight.
- [A1-scaling] White space 1 (sense amps under the array): one vertical connection per bitline at 64–128 cells/BL at the 1β cell size needs a ~0.26–0.37 µm bond pitch (~0.5 µm with 2:1 in-array muxing), and a ~10-transistor SA must fit in ~0.14–0.27 µm² — basis: geometry; production hybrid-bond pitches are understood to be several µm, and sub-µm is still research [UNVERIFIED: training knowledge].
- [A1-scaling] Wafer cost with periphery under cell (two bonded wafers) roughly doubles before the density gain is netted — basis: a second (logic-process) wafer plus bonding; no public cost [ESTIMATE].
