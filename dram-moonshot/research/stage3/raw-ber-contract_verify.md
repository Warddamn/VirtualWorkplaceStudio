# RAW-BER CONTRACT dossier verification

Verifier `dosv-raw-ber-contract`, 2026-11-02. Target: `dossiers/raw-ber-contract.md`. Model: `models/raw-ber-contract.py` (source of truth). WebSearch used: 0 of 2.

## Results

| Check | Result | Notes |
|---|---|---|
| (a) Model runs | PASS | `python3 models/raw-ber-contract.py` exits 0; output matches `research/stage3/raw-ber-contract_model_output.md` |
| (b) Sections 0-10 | PASS | All present and substantive |
| (c) Number tracing | PASS after 2 fixes | ~70 numbers spot-checked against model output, model INPUTS, A1 `dram_cell_physics.py`, A2, source logs, FINAL_CONCEPTS. All 47 original URLs (and 4 added) are in `research/sources/*.jsonl` |
| (d) Decisive experiment | PASS | Phase 1 DRAM Bender study $96k, GO/NO-GO at M6; whole plan $943k (line items sum correctly; contingency 8.0%) in 24 months. Pre-set numbers: interval ≥0.5 s at 85 C vs <256 ms at 65 C; clusters ≤0.4% / >10% multi-byte; flaggable ≥50% / <25%; Poisson within 2x; soak 0 UE |
| (e) Prior art | PASS after fixes | Delta #1 said "No DRAM analogue was found" although Stage 2 critics of I-11148 named XED, Razor, FLY-DRAM, Solar-DRAM, US 8,898,544 and chipkill marking; delta #4 (typed pages) ignored Flikker, EDEN and Kelle (critics of I-10963). Other critic-named art (Frugal ECC, COP, CREAM, AVR/MemSZ, SECRET, arXiv 2607.16042, NAND RAIN) was missing |
| (f) Founder pronouns | PASS | None found |

## Spot-checks that matched

- Target: 1.56e8 reads/s, 4.93e15/yr, 2e-19, t=8 fails 2.3e-17 (0.099 UE/yr, ~100x short), t=9 = 90 bits 17.6%, fails 1.6e-19; code table rows 1e-5/1e-4/3e-4/1e-3 (t, bits, parity), page 1.46%/4.83%, Shannon 0.15%/1.15%.
- Margin: σ_eff 7.14 mV, z 3.72, 26.6 mV, 1.88x, Cbl 34.7 fF, Cs 5.42 → 2.68 fF, pillar 1,307 → 644 nm, 1e-3 gives 1.22x (22.1 mV, 2.20 fF).
- Flags: δ 0.5σ = 3.6 mV, 88%, 5.4 false flags; 131 at 1.5σ; 14-60% first-period; sensitivity rows (9/7/70/1.73e-4/25.6; 9/8/80/1.52e-4/26.3; 9/8/80/1.06e-4/27.7; 9/9/90/5.9e-5); 31.7 false flags at 1σ (kill #7 ">30").
- Bursts: 3.3e-4, 5.4e-5, 8.3e-7; 5.2e-5 / 8.5e-6 at 1% / 10% 3-bit; ≤1e-8 at 8-bit; 0.41% cluster limit; on-die SEC 0.53 miscorrection is an INPUTS ESTIMATE; internal 1.7e-4.
- Refresh: 40 × 16 Gb × 1.0625 = 6.8e11 cells; 45.9 fJ (A1 model) → 31 mJ, 0.488 W; scrub 0.57 mW; 295/3,900 ns = 7.56%; 64Gb 41% → 2.6% (tRFC 1.6 µs); interval table (3.6/2.0, 1.5/0.84, 0.72/0.50 s; 65/45 C ranges); power rows 0.063/0.032/0.016 W, 7.7/15.3/30x, 14/15/16%, 0.97/0.48/0.24%; VRT 375 ms and 1.3 s at 3.4 mW.
- Budget split 371 ms, 25.6 mV + 1.2 s (18x); value 0.456 W × 43,830 h × 1.3 = 26 kWh, $2.60, 2.7%, $0.041/GB, 7.1 MW/EB; density 0.404 vs 0.447 Gb/mm² (0.90x); $1.48/GB.
- Hammer/pages: 2.17e7 ACT, 21,739x; RFM 0.38%/8.2%; 129 → 2.3 transfers; break-even 0.67 reads/s; soak 5.6e14 reads/board; fleet 4.9e19 reads/yr.
- Sources: Hi-ECC 93%/2%, RAIDR 74.6%, ArchShield 1e-4 at 4%, PRAC <13%/94%, CnC-PRAC ~1%, PaCRAM 388 DDR4 chips, SHIELD 1e-4, Agilex ~€9k, CXL IP ~€192k (Jan 2025), sky130 $15k/100 chips, 22FDX $17,997/mm² 4 mm² min, tREFI/tRFC datasheet. A2: 6.6 kWh/GB, ~16x fab. Oxide 1e3-1e4x (notes). FINAL_CONCEPTS: rank 4, EV 60 = 3 × 4 × 5; Phase 1 ~$80k portfolio vs $96k standalone. Stage 2 scores and techniques of all 10 constituent ideas match.

## Fixes applied (surgical edits)

1. §6 Q7 gate pointed to "kill #8" (the CXL IP re-scope); the flag-latch criterion is kill #7. Corrected.
2. §9 kill #4 said VRT growth ">100x static BER per day, so a 10-minute scrub cannot hold ≥0.5 s". The model (`p_max_interval`, lognormal, 85 C) gives 1.29 s (BCH-12) and 0.72 s (RS-8) at 100x/day with a 10-minute scrub; the 0.5 s floor breaks only above ~700x/day (RS-8) or ~5,000x/day (BCH-12). Recast the criterion on the measured 10-minute-scrub interval, with the model thresholds as [ESTIMATE]. (Pessimistic pow5 + RS-8 sits at ~0.5 s already, consistent with the dossier's 0.50 s figure.)
3. §3 delta #1: replaced "No DRAM analogue was found" with the nearest precedents (XED, US 8,898,544, Solar-DRAM) and flagged Razor and NAND soft bits as obviousness/design-around risks.
4. §3 known list: added critic-named prior art (Kelle [REPORTED], Flikker, EDEN; Frugal ECC [REPORTED], COP, CREAM, AVR/MemSZ [REPORTED]; SECRET, arXiv 2607.16042 [REPORTED]; Razor, XED, FLY-DRAM, chipkill marking; NAND RAIN for tier-orthogonal codes). Moved XED out of the bare UNVERIFIED-PK list into the flag bullet.
5. §3 delta #4 and "Not new": typed pages now credit Flikker/EDEN/Kelle; reliability-typed data and compression-funded ECC added to "Not new".
6. §6 IP strategy: tier-orthogonal continuation marked weak (RAIN, chipkill precede it).
7. §10: added the 4 logged URLs (Kelle, arXiv 2607.16042, Frugal ECC, AVR) and the no-URL critic-named items; source-log note now mentions Stage 2 logs.

## Left as is (minor)

- §2.4 rounds RS-8 5.45e-5 as 5.4e-5 in the zero-cluster row (matching the model's own headline) but 5.5e-5 in the 0.1% 8-bit row. Within rounding.
- GO (≥0.5 s at 85 C) and NO-GO (<256 ms at 65 C) leave an intermediate zone; acceptable as a "conditional" band.
