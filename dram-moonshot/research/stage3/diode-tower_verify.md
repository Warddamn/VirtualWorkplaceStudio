# DIODE-TOWER dossier verification

Verifier `dosv-diode-tower`, 2026-11-02. Target: `dossiers/diode-tower.md`. Model: `models/diode-tower.py` (source of truth). WebSearch used: 0 of 2.

## Results

| Check | Result | Notes |
|---|---|---|
| (a) Model runs | PASS | `python3 models/diode-tower.py` exits 0; it rewrites `research/stage3/diode-tower_model_output.md` |
| (b) Sections 0-10 | PASS | All present and substantive |
| (c) Number tracing | PASS after 5 fixes | ~70 numbers spot-checked against model output, `dos-diode-tower.jsonl`, A1/A2 (and the A2 model), FINAL_CONCEPTS and concepts_*.json |
| (d) Decisive experiment | PASS | Coupon run, $225k ($135k without the reusable bench), GO/NO-GO at M7; whole plan $980k over 24 months. Pass/fail frozen before data: tail ≤422 aA at 85 °C / 0.7 V; ≥0.8 nA at ≤1.2 V, 0 °C, n ≤1.3; Δφ ≤30 meV at 1e12 pulses. FAIL: >422 aA in every split, Δφ >60 meV in 1e10 pulses, or σ >0.07 eV on every anode |
| (e) Prior art | PASS after 1 addition | The "none found" claim is limited to diode-steered linear-capacitor 1T-nC/1D1C DRAM. That matches both Stage 2 critics for I-10647, and the dossier says it is not an FTO opinion. Delta items 1-4 are hedged ("look new"). Added one row listing the prior art that Stage 2 critics named for the supporting ideas and that was missing from the table |
| (f) Founder pronouns | PASS | None found (word-boundary grep for he/she/his/her/him/himself/herself) |

## Spot-checks that matched

- Geometry: Cs = 2π·ε₀·40·14 nm/ln(50.5/45) = 0.270 fF (recomputed). 843 e⁻; ~17,700 e⁻ in 1-beta; ring 2π·30·14 = 2,639 nm²; 0.018 fF/tier; pillar 0.72/1.00/1.57 fF; pitch 121 nm; slit +12.4%; 0.0165 µm² = 1.5× 0.011.
- Signal: 106/85 mV; kT/C 1.97 mV; σ 7.33; z 5.8 at 32 tiers; 73/59 mV and z 4.1 at 64; z 3.1 at 96; the card's 76 mV from 0.27·0.5/1.77.
- CDS residual vs maximum tiers: 117/73/40/14, and 148 wrapped at 10 mV. 40 tiers = 2.39× (recomputed from `density()`).
- Density and cost: 0.867 (1.94×), 1.763 (3.94×), parity at 18 tiers, 3× at 50, AR 27/53, 0.55×/$0.81 and 0.35×/$0.52. Tier-yield grid 0.53/0.33, 0.61/0.42, 0.71/0.58 recomputed exactly from the model's `density()` and cost formula.
- Diode: 422/27/844 aA; prefactor 1.38e-4 A; kT 30.9 meV; 0.818/0.903 eV; 1.2 aA (23 s) at 1.00 eV; tail 94× = 0.14 eV; 0.96/1.04 eV; 0.87 MV/cm; image force 0.177/0.102 eV; TFE 0.07 eV; total lowering 0.18-0.25 eV (0.35-0.45 eV at 10 nm, 0.11-0.17 eV at 20 nm); bars 1.07-1.12 and 1.17-1.22 eV.
- Contact map: PKU 0.82 → 0.70-0.73 eV, 13-41 µs; KIT 0.92 → 0.78-0.82 eV, 0.2-0.8 ms; AgOx 1.10 → 0.94-0.98 eV, 35-140 ms.
- Sensitivity table: all 16 cells match model §6.
- Write and disturb: V_f 1.10 V at 0 °C (1.12 eV); swing ~1.8 V; 350 to 2.3e5 events; 0.45 ms at 1.0 eV; ZrO₂ ≤0.7 V; V_f shift ~0.1 V from 0 to 85 °C; plate energy 0.94 fJ.
- Endurance: 5.1e-6 C/cm² per pulse; 9.9e9 pulses; ~100×; hot row 1.4e14; 2.6×/7× drift multipliers.
- Escape geometry: 80 nm/30 nm wrapped, 0.90 fF, 0.96-0.97 eV, 3.0×; 100 nm: 0.96 eV, 2.3×.
- Energy: 28 vs 46 fJ (1.6×); refresh 4.1 vs 6.1 mW/GB; 0.26 at 1 s; 16× fewer refreshes.
- GO/NO-GO gates G1-G5 match model §11.
- Budget: Stage A 10+100+25+90 = 225; coupon fab 450×$150 + 60×$250 + $15k ≈ $98k; stacks 1,400×$150 + $45k = 255; allocation sums to 980; Stage B 255+30+25+25 = 335.
- Sources and Phase A: rank 6, EV 3×3×5 = 45; "2-4× at 16-32 tiers" and "≥48 tiers for 3×" (concepts_*.json); Kepler app 17/339,850 filed 2021-06-04; OCTRAM Ioff <1 aA; imec >1e12 cycles; 2T-64C team; Micron 32 Gb NVDRAM IEDM 2023; Sogang VDD/3; AgOx 1.00-1.20 eV; Pt-IGZO 0.92 eV, n 1.36; PKU 0.82 eV, n 1.35; PtOx/ZnO n 1.31. A1: 512 cells/BL, AR 60-75. A2: Hf 14-41%; Ru $17.98 → $56.21/g; Ga ~98% Chinese; suspension ends 2026-11-27; 1,300 kWh and 8 m³ per wafer; 0.42 kWh/GB; use phase ~16×; Micron 1β zero EUV.
- Materials arithmetic: RuOx ring 49,480 nm³ per tier; ~0.04 g Ru per wafer; 0.003 mg/GB; IGZO shell ~0.1 g (In 0.036 g, Ga 0.022 g); tower 0.12-0.2 kWh/GB at ~3.5× GB (3.94× × 0.88 tier yield).

## Fixes applied (surgical edits)

1. §1, cross-reference. "(the plate-swing rule, §2.5)" pointed to Sensitivity. The rule is in §2.4. Corrected.
2. §2.3, barrier gap. "0.15-0.3 eV short" mixed the two targets. 1.07-1.12 − 0.92 = 0.15-0.20 eV for 64 ms, and 1.17-1.22 − 0.92 = 0.25-0.30 eV for 1 s. Split accordingly.
3. §4 item 1, same gap. "Barrier gap: 0.15-0.3 eV. The design needs ≥1.07-1.12 eV" was arithmetically inconsistent (that bar gives 0.15-0.2 eV). Now reads "0.15-0.2 eV (64 ms), 0.25-0.3 eV (1 s)", with the 1 s bar added.
4. §2.4, write current. "13.5 nA ... ~512 A/cm²" → "~13.6 nA ... ~515 A/cm²", to match model §7/§11 and the dossier's own G4 line. Note: Cs·ΔV/t = 0.2702 fF × 0.5 V / 10 ns = 13.5 nA. The model hard-codes 13.6 nA (`section_write`, `section_go`), a 0.7% difference that changes no conclusion.
5. §8, ruthenium. "A2's Ru-electrode case is 0.10 mg/GB ... ~36× less: ~0.7-5%" did not trace. The A2 model (`research/models/A2_resource_intensity.py`) deposits 0.416 g Ru per wafer over 3,068 GB/wafer = 0.136 mg/GB (26.4% of world Ru at full utilization, 176% at 15%). The ring's 0.0033 mg/GB is ~41× less, which gives 0.64-4.3% of world Ru. Text now reads "~0.14 mg/GB ... ~40× less: ~0.6-4% of world Ru, just under A2's 5% flag".
6. §3, prior art (check e). Added a row with the Stage 2 critic-named prior art that was missing from the table: OCSA/CIS CDS (I-05218); Hi-ECC, DDR5 on-die ECC and NAND LDPC (I-11559); XED, Razor, US 8,898,544 and chipkill marking (I-11148); Chipkill and RAIN (I-00729); NEO 3D X-DRAM and Huawei CAA IGZO (I-03474, I-10833); Toshiba NAND-structured DRAM and US 12082391 (I-10664); NaMLab AFE ZrO₂ and MPB-HZO (I-02355); Macronix VG-NAND LSM and coded ROM decoders (I-11544). The delta claims were kept.

## Not changed (noted)

- §9 kill 8 (< 60 mV at emulated 32-tier load) and the Stage B pass (≥ 80 mV) leave a 60-80 mV grey zone. 60 mV is close to the z ≥ 3.72 floor at 7 mV residual (2 × 3.72 × 7.33 = 54.5 mV), so the zone looks intentional.
- §6, "remaining ~$650-700k" on a NO-GO at M7. A rough check gives ~$640-670k (980 − 225 Stage A − ~88 founders − ~15-20 IP/travel). This is approximate and not decision-relevant.
- §4 item 5, "fails in 1e2-1e5 accesses". The model gives 349 to 2.28e5, so this is an order-of-magnitude statement and acceptable.
