# PIXEL-STACK dossier verification

Verifier `dosv-pixel-stack`, 2026-11-02. Target: `dossiers/pixel-stack.md`. Model: `models/pixel-stack.py` (source of truth). WebSearch used: 0 of 2.

## Results

| Check | Result | Notes |
|---|---|---|
| (a) Model runs | PASS | `python3 models/pixel-stack.py` exits 0; output identical to `research/stage3/pixel-stack_model_output.md` |
| (b) Sections 0-10 | PASS | All present and substantive |
| (c) Number tracing | PASS after 6 fixes | ~60 numbers spot-checked against model output, source logs, A1/A2, FINAL_CONCEPTS |
| (d) Decisive experiment | PASS | Planar pixel-amp array, ~$300k by M9 (whole plan $1,000k, 24 months); pre-set GO <=15 mV, conditional 15-30, NO-GO >30 mV; leakage <=34 aA, NO-GO >101 aA |
| (e) Prior art | PASS after 1 addition | No "none" claim; delta is a hedged four-element combination. Added a row listing the Stage 2 critic-named prior art that was missing |
| (f) Founder pronouns | PASS | None found |

## Spot-checks that matched (model or source)

- Design point: 52 nm capacitor, 0.0110 µm², C_BL 3.00 fF / FD 0.35 fF, signal 50.3 mV (formula 0.425 × 0.45/3.80 matches code), 42 µV/e⁻, 1,194 e⁻, 0.0432 Gb/mm², 10.4 tiers, 2.76 Gb/mm² = 6.2×.
- Noise: 1.34/1.20/1.11/0.90/0.87/0.43 mV, σ 2.49 → 9.3 mV, RTN 4.2, coupling 8.05 → 1.2, residual 14.7 (21.5 without DFB), F ≈ 5.7 (model 5.74), ~60 e⁻ rms.
- Margin: 29.5 / 18.0 / 40.2 mV allowed; Cs min 0.20 fF; 0.26 fF at 15 mV.
- Retention: 24.8 + 6.5 = 31.3 aA vs 33.8 aA; 1.08 s; 101 aA ≈ 0.33 s; retention rows (2.25, 0.67, 0.38, 0.15, 0.04 s).
- Cost/system: $8,000, 0.862, $0.58, 0.40×; 1.7× Smart-Cut; tRC 55/106/210 ns; 89 fJ, SF 38 fJ; 17× refresh; 1.24% vs 7.6% busy; 5.8e15 accesses; amp area 0.034/0.022 µm²; 8-tier groups 3.74 Gb/mm², 0.51×.
- Sensitivity grid (12 cells) and residual → density rows (10/30/50/70 mV) match.
- A1: optimistic 6.7×; base 2.5× density, 0.52× $/bit (→ ~1.5× before yield vs PIXEL-STACK's 0.345×); 0.89/tier; 0.447 Gb/mm²; 5.4 fF / 35 fF. A2: 0.42 kWh/GB, 2.6 L/GB, Ga <0.4%, 2026-11-27.
- Source logs: Hf ~$13k/kg (+140%), W China ~80%, EUV ~10 GWh/yr, Fossum 0.21 e⁻, ND $124/h, Penn $70/h, TAMU $150/h, UW $495/h, wafer.space ~$7k/1,000 ICs, imec 1e12 at 95 °C, H+O anneal ~30×, Kioxia Ioff <1 aA, B2 k 56-62. Rank 5, EV 48 (FINAL_CONCEPTS).
- Budget lines sum to $1,000k; EOT 0.7 nm → ~76 nm capacitor (dossier ~75 nm, tagged).

## Fixes applied (surgical edits)

1. §0 verdict and §4 item 3, hydrogen tolerance. The dossier said retention needs "σVt ≤30 mV and H shift ≤~10 mV". In the model (`leak_tail_A`), at σVt 30 mV a 10 mV shift gives 0.85 s and 1 s needs ≤~3 mV; σVt 25 mV tolerates ~20 mV and σVt 20 mV ~40 mV. Text corrected.
2. §4 item 2, coupling. "16 mV at 0.2" mixed in the total residual with DFB (16.5 mV). The raw coupling at Cc/C_BL 0.2 is 2 × 0.2 × 50.3 = 20 mV. Changed to "Raw, 8 mV at 0.08 and 20 mV at 0.2".
3. §2.5 cost. The claim that "~$2,000 Smart-Cut layer per group gives 0.67-1.18×" conflated two model rows. One $2k layer per group = 0.67× ($13,600 wafer). The model's $2,000 column is per amp sub-layer (two per group) = 1.03-1.18×. Split accordingly.
4. §2.5 group size. "32-tier groups reach 0.28× if the residual is ≤10 mV" → the model's group table is "at the modelled readout" (14.7 mV). Corrected.
5. §6 allocation summed to $1,120k ($120k sponsored researcher counted in both Experiments and People). Rewritten to match the budget table: experiments $770k (incl. $120k researcher), founders $150k, IP $45k, contingency $35k = $1,000k.
6. §8 energy/water basis said "0.40× wafer-cost ratio". 0.40× is the $/bit ratio (wafer cost is 2.1× 1-beta). Label corrected.
7. §3 prior art (check e). Added one row with the prior art that Stage 2 critics named for I-05218, I-11559, I-00729, I-02936, I-11545 and I-01381 and that was missing from the table. The four-element delta claim was kept.

## Not changed (noted)

- The model prints a signal basis label "Cs/(Cs+Cbl) × Cbl/(Cbl+Cfd)". The code actually computes Cs/(Cs+Cbl+Cfd), which the dossier uses correctly. This is a cosmetic label issue in the model only.
- The notes file (`pixel-stack_notes.md`) gives "Experiments 770", which is consistent with fix 5. It was not edited.
