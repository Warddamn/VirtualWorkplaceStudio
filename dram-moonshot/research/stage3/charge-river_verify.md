# CHARGE-RIVER dossier verification

Verifier `dosv-charge-river`, 2026-11-02. Target: `dossiers/charge-river.md`. Model: `models/charge-river.py` (source of truth). WebSearch used: 0 of 2.

## Results

| Check | Result | Notes |
|---|---|---|
| (a) Model runs | PASS | `python3 models/charge-river.py` exits 0 and rewrites `research/stage3/charge-river_model_output.md` |
| (b) Sections 0-10 | PASS | All present and substantive |
| (c) Number tracing | PASS after 5 fixes | ~50 numbers spot-checked against model output, `dos-charge-river.jsonl`, A1/A2, FINAL_CONCEPTS, Stage 2 results. All 38 dossier URLs are logged in `research/sources/*.jsonl` |
| (d) Decisive experiment | PASS | $990k total ($480k direct), DEMO M16-21 (inside 24 months). Pre-set table: CTE PASS >=0.9970 DFE / STRONG >=0.999 / FAIL <0.9934; loop BER <=5e-10 / FAIL >1e-8; read noise, k_ws, retention, cycling, schedulability all have numbers |
| (e) Prior art | PASS after edits | No blanket "none". The delta header said "none of these was found in prior art", but Stage 2 critics named art that narrows deltas 2 and 3 and that was missing from the table. Fixed (see 6-8) |
| (f) Founder pronouns | PASS | None found |

## Spot-checks that matched (model or source)

- Packet: Cox 6.91 fF/µm², π×88×25 nm = 0.0069 µm², C 0.048 fF, 447/313/47 e-, 4.5e12 cm⁻², 534 µV/e-, 167 mV, SNR 39.
- Density/cost: 32 stages, 64 b/hole, 98 transfers, 3.2 Gb/mm² raw, ×0.70×0.75×0.962 = 1.62 Gb/mm² (3.63x), 9.9 vs 35.8 mm², $5,280 wafer, $0.71/GB, $0.84 NAND cross-check, range $0.42-1.47 (1.0-3.5x).
- Reliability: 4.9e-10, Q 6.11; CTE table rows 50/98/194 transfers and 150/3,000 e- (0.9959/0.9942, 0.9979/0.9970, 0.9989/0.9985, 0.9992/0.9990, 0.9962/0.9926); (1-1.5×0.003)^98 = 0.64; DFE 1.4x; 15 e- → 0.998; 30 e- n/a; sensitivity span 0.9945-0.9993; k_ws 3 → 0.9985.
- Trap kinetics: drift 0.6 ps, diffusion 24 ps, ν0 1.1e11, 25.7 meV × ln(4,400) = 0.216 eV, 0.203/0.170 eV, 46 meV; imec table ranges 0.56-0.97, 0.92-0.995, ≥0.9992, ≥0.9999; 0.98^(1/568) = 0.99996; ~83x margin; 0.18x factor.
- CTE→density table (all five rows); NO-GO 0.9934 → ~$1.29/GB.
- Latency/bandwidth/energy: s ≥ 92.2%, 3.84 µs phase-clock lap (FINAL_CONCEPTS arbitration 5), 17/26 ns, 35/28 ns at 4/6.25 MHz, 1.01e6 nodes, 6.3 TB/s, 3.7 W, 113 GB/step, 56 dies, 0.9%; 90/45/28/72 fJ; 0.06 vs 11.5 mW, 191x.
- Endurance/retention/RC: 1.6e6 decisions/s, 37x, 7.9e15, 1.5e11, 15x, 1e12/200 MHz = 1.4 h; 0.25 aA; 41 nm, 145 Ω/µm, 0.73 fF/µm, 100 µm.
- Sources: imec 142 b/4-phase/>98%/>200 s/>1e10/6.25 MHz; MIT LL 4.6 e- at 2.5 MHz; ShiftsReduce 52.5%; JYX ~20%; HBF 512 GB/1.6 TB/s; imec ~5x claim; Penn $66-77/h door, $150/h staff, $0-495/h tools; sky130 ~$15k/100 chips; EUV 5-7 layers, $825-1,155/wafer (A1); 0.42 kWh/GB, 2.6 L/GB, 1,300 kWh/wafer, 16x use/fab (A2) → 0.42×2,300/1,300/2.9 = 0.26 kWh/GB; Ga 2026-11-27, ≥256-layer RE clause; "~10-90 traps per gate" (I-04670 physics critic). Rank 7, EV 40 = 4×2×5.
- Budget: direct $480k; allocation 330+300+140+40+45+55+80 = $990k.

## Fixes applied (surgical edits)

1. §4 row 1: mid-stack regenerator "every 10-16 stages, so a CTE ~0.99 device keeps its plate count". Model `max_transfers` at CTE 0.990 gives 28 transfers = 8 stages (0.993 → 13). Changed to "every ~8 stages at CTE 0.990 (~13 at 0.993)". (Model prose in §6 says "every 32 stages", which contradicts its own table; noted, model not edited.)
2. §4 row 4: MoE "0.7-1.5 µs at 6 MHz" → "at 4-6 MHz" (model: 715 ns at 6.25 MHz, 1,519 ns at 4 MHz).
3. §2.5 table: CTE 0.980 verdict "dead" → "NO-GO" (model verdict; 8 bits/hole is not zero).
4. §2.2 table: DDR5 "~45 ns tRC-class" had no source; tagged [UNVERIFIED].
5. §8 tungsten: "plates cost ~$3 per wafer (A2)" misattributed A2's whole-DRAM-wafer figure (~6.7 g W, ~$2.7). Recomputed: 200 × 25 nm plates deposit ~6.8 g W per wafer → ~$3-8 with deposition waste [ESTIMATE].
6. §3 table (check e): added one row listing Stage 2 critic-named prior art missing from the table: recirculating CCD loops with per-loop refresh amplifiers and major-minor loops (I-04245, I-04285); skipper CCD, Hitachi PLEDM, QIS jots (I-01381); soft-decision LDPC, Razor, XED, chipkill, US 8,898,544, Solar-DRAM (I-11148); Parkin racetrack, Schöbitz 2019 (I-11581). Tagged [UNVERIFIED].
7. §3 delta: header "none of these was found in prior art" → "none was found as stated, but the art above narrows each one"; delta 2 now names CTI-correction and decision-quality-sensing art; delta 3 notes per-loop regeneration is 1970s art.
8. §6 IP strategy "Prior art that narrows claims": added decision-quality sensing and 1970s recirculating loops.

## Not changed (noted)

- §5 pass/fail read-noise FAIL is > 15 e-, while kill 6 triggers at > 30 e- and GATE 2 passes at ≤ 15 e-. The 15-30 e- band is a test fail, not a program kill; consistent with the model (15 e- feasible at 0.9982, 30 e- infeasible) but could be stated more explicitly.
- Q4 gate uses 0.993 as the NO-GO line; §5/§9 use the model's 0.9934. Rounding only.
- Header agent `dosw-charge-river` vs model `dos-charge-river`: labels only.
