# MARGIN STACK dossier verification

Verifier `dosv-margin-stack`, 2026-11-02. Target: `dossiers/margin-stack.md`. Model: `models/margin-stack.py` (source of truth). WebSearch used: 0 of 2.

## Results

| Check | Result | Notes |
|---|---|---|
| (a) Model runs | PASS | `python3 models/margin-stack.py` exits 0; rewrites `research/stage3/margin-stack_model_output.md` |
| (b) Sections 0-10 | PASS | All present and substantive (plus header, idea list, verdicts) |
| (c) Number tracing | PASS after 6 fixes | ~70 numbers spot-checked against model output, model functions, source logs, A1/A2, raw-ber-contract model, FINAL_CONCEPTS; every dossier URL is in `research/sources/*.jsonl` |
| (d) Decisive experiment | PASS | $520k (8 model budget rows), M0-17, inside 24 months; pre-set GO σ_res ≤ 20 mV, pairs < 1%, tail ≤ 586 aA; NO-GO σ_res > 34 mV or pairs > 10% |
| (e) Prior art | PASS after additions | No bare "none" claim; delta is a hedged combination. One absolute ("ECC never used to shrink the capacitor") softened to Stage 2's "none found"; Stage 2 critic-named prior art added (rows below) |
| (f) Founder pronouns | PASS | None found ("Founder 1/2", first person only) |

## Spot-checks that matched

- Anchors: 62.8 fF/µm², 4.16 aF/nm, 1,302 nm / AR 62, 120 nm / AR 5.7 at 0.5 fF; Cbl 34.7 fF; 50.0 mV = (0.525-0.155) x 5.42/40.1; 7σ x 7.14 mV; 17,762 e- and 1,561 e-; Q⁻¹(1e-4) 3.719, 1.88x; kT/C 1.83 mV, floor 0.024 fF (20x below 0.5 fF).
- Cases A-I table (4.63 / 2.31 / 1.26 / 0.91 / 0.54 / 1.77 / 0.60 / 0.09-0.14-0.32 fF; cuts, heights, ARs).
- Residual: 1.89 / 0.33 / 4.0 / 2.4 → 5.0 mV; σVt 47 mV, 53% gm; kick 49 aF, 79 aC, 1.73 fF, 46 mV, 2.3 mV, 7.1 mV, D 8.1, random 2.4. Hand check row I central (36.7 → 29.4 → 20.7 vs 20.0 mV; D 8.63 mV at 1.62 fF from `kick_terms`).
- ECC: 2.3e-17, 0.9 server-years, 83% flagged at 3.9x false flags, 1.4e-4 / 1.7e-4, pairs 6.3e-5 / 1.7e-5 (0.90x). BCH-12 iid 3.3e-4 traces to `raw-ber-contract_model_output.md` (3.32e-04).
- Retention table (0.25/0.5/1.0 fF rows), 586 aA = 37.5 aC / 64 ms, 3.1 ms at 13 fA, 370 mV droop → 1.8 s, 47 s dielectric cap, 6,352 aA (K3), 1,172 aA.
- Energy 20.1 vs 0.99+3.00+2.40+2.0 = 8.8 fJ; refresh 12.2 vs 0.431 mW at 917 ms.
- Area/cost: +12.5% array, +8.8% die, 0.701 vs 0.762 (-8%) and 1.57x 0.447; +3.6/+0.4/-2.8%, $1.44-1.53; strap 1.2%; ALD x0.009 (~100x).
- 3D: 450 → 63 nm, 2.81x, ~26 → 9.8 tiers. Timing 62 ps + 2 x 0.72 + 0.5 + 1.60 = 3.6 ns.
- Sensitivity grid (12 cells), thresholds 23.5/20.5/14.5, 12.3/10.6/7.1, 34.3 mV; segment rows (64 cells 4.4%, 0.20 fF; 16 cells 17.5%, 0.11 fF). Zero-cancellation kick: D 42.9 mV, S 107 → 86 mV, needed 27.0 mV.
- MPW: 6 mm² x $17,997 = $107,982, +20% ≈ $130k; 42M cells, 5.46σ, ~210 errors/chip. Budget rows sum to $520k; plan $955k + $45k reserve = $1.0M.
- Source logs: OCTRAM Ioff < 1 aA / Ion > 15 uA; Kioxia 8-layer 3D OCTRAM; Samsung ISSCC 2026 16Gb VCT and 10a die; SK hynix VLSI 2026 shielded VG and 56.1% 5-layer yield; VS-DRAM back gate/shield; Hi-ECC ~93%; PaCRAM 388 chips; imec H+O ~30x; hafnium $5,000 → $13,115/kg (A2); Ru 26-176% (A2); Micron Clay 16 billion kWh/yr, 48 Mgal/day (A2); Micron Idaho late 2028 (A1); MOSIS-GF 2026-07; IonQ-SkyWater 2026-07-31; ChipFoundry $15k/100 chips; Micron "skipping 4F2" per notes (weak source, flagged). Rank 1, EV 75 (FINAL_CONCEPTS). Stage 2 ids, techniques, verdicts and consensus scores all match `stage2_results.jsonl`.

## Fixes applied (surgical edits)

1. §0 verdict: "The experiments cost $520k" clarified against the model's "Experiments alone: $675,000" line (which adds spin 2 and IP); $520k is the decisive-experiment subtotal.
2. §1: bitline "seven times the 5.4 fF cell" → "about 6.4 times" (34.7/5.42 = 6.4).
3. §2.8 and §9 K1: no-ECC (k = 7) Cs "~0.26 fF / ~0.8 fF [hand]" → "~0.25 / ~0.77 fF" from the model's own `solve_local_cs` at k = 7 (0.252 / 0.765).
4. §4 row 2: "10 mV [1/f] gives 0.32 fF" attributed the whole pessimistic scenario to 1/f. With only 1/f at 10 mV (central otherwise) the model functions give 0.247 fF; 0.32 fF needs α 0.15 and the 5.4 mV comparator term too. Text corrected.
5. §9 K2: tail > 1,172 aA "kills any cut beyond ~4.6x" → "~5.4x" (1,172 aA is the 64 ms limit at 1.0 fF; 5.42/1.0; matches §4 row 5 "still 5.4x").
6. §5 / §6: untagged portfolio-sharing figures ("~$260-320k" increment; "~$250k freed") tagged [ESTIMATE] with basis; freed range aligned to $200-260k so it matches the increment range.

## Prior-art edits (check e)

Stage 2 critics for I-00257, I-11559, I-11148, I-05218, I-11588, I-04613, I-07812, I-11545 and I-05154 named prior art missing from §3. Added or extended rows:
- Hierarchical/local-bitline sensing, selective bitline activation (Udipi ISCA 2010), FGDRAM (MICRO 2017).
- Gain-cell eDRAM: Si GC-eDRAM (BGU), UT Austin IGZO eDRAM, imec/Kioxia IGZO 2T0C.
- Hi-ECC row: added the ECC(552,512) gain-cell refresh study (arXiv 2607.16042, critic-named, not re-checked); "ECC never used to shrink the capacitor" → "no logged source spends it on capacitor size (Stage 2: 'none found')".
- Neutraliser row: electrophysiology headstage neutralisation; "No DRAM neutraliser" → "No DRAM neutraliser found".
- Sequential/M3D sense tiers: CEA-Leti CoolCube, M3D DRAM periphery tier (arXiv 2008.11367), Monolithic 3D ion-cut patents.
- Flag row: XED, static weak-cell erasure maps (US 8,898,544), Razor (MICRO 2003), Solar-DRAM, chipkill marking.
- "No oxide VCT program has published a capacitor cut" → "No logged snippet shows an oxide VCT program publishing a capacitor cut."

## Not changed (noted)

- §8 "22FDX made in GF Dresden" is [training knowledge; verify]-tagged and not decisive; no search spent.
- §2.3 hand check needed-signal 20.0 mV uses unrounded σ_res 5.04 mV (19.8 mV with 5.0); within rounding.
