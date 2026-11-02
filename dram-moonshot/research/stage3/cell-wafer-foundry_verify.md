# CELL-WAFER FOUNDRY dossier verification

Verifier `dosv-cell-wafer-foundry`, 2026-11-02. Target: `dossiers/cell-wafer-foundry.md`. Model: `models/cell-wafer-foundry.py` (source of truth). WebSearch used: 0 of 2 (no decisive fact looked suspicious; all 51 dossier URLs are present in `research/sources/*.jsonl`).

## Results

| Check | Result | Notes |
|---|---|---|
| (a) Model runs | PASS | `python3 models/cell-wafer-foundry.py` exits 0; output identical to `research/stage3/cell-wafer-foundry_model_output.md` |
| (b) Sections 0-10 | PASS | All present and substantive |
| (c) Number tracing | PASS after 3 fixes | ~70 numbers spot-checked against model output, source logs, A1/A2, FINAL_CONCEPTS, concepts_device.json, Stage 2 critics |
| (d) Decisive experiment | PASS | $700k + $90k contingency = $790k (plan $990k incl. founder pay), M1-M24; pre-set GO (opens <=1e-5 95% UCL over >=1e7 links, <=83 fails; bridges <=1e-7 over >=3e7 pairs; overlay <=0.30 um; >=95% void-free; dVt <=20 mV, retention change <=2x) and NO-GO (opens >=1e-4 at 2.0 um, bridges >=1e-6, overlay >0.5 um) |
| (e) Prior art | PASS after 1 qualification | "Not new" list already concedes the split, cross-node stacking and IL. The one "none found" claim (open bitline-group spec) matches the I-04714 critics ("No open bitline-level standard found"), but omitted that the critic named UCIe as the die-level open interface; added |
| (f) Founder pronouns | PASS | None found |

## Spot-checks that matched

- Model s2: M 146 (SA-limited; bond allows 101 at 1.5 um, 41 at 1.0 um), 0.66 avail fill (0.85 - ~0.19 WLD) reproduces 146; Cbl 19.9 = 0.43 + 7.1 + 5.8 + 5.1 + SA; Cs 1.16 fF, 123 nm; 50 mV -> 2.11 fF; footprint 80 x 323 nm = 0.0258 um2; stair 8%, edge 8%; die 15.9 mm2; arr eff 0.86; 2.01 Gb/mm2 = 4.5x; gain 15.5 fF, 0.78 ns, 2.60 Gb/mm2, 5.8x.
- Energy 11.0 / 8.6 / 19.3 fJ, 1.8x / 2.3x.
- Cost: pair $5,820; 0.998^64 = 0.880 x 0.992 x 0.965 = 0.842; 10,804 GB; $0.54 = 0.36x; gain $0.41; tiers 16/32/128 $1.32 (0.89x)/$0.77/$0.49; break-even 16 / 12 tiers; $20/$45 tier $0.48/$0.63; $1.9k periphery $0.46; $3.45k -> $0.60 and $4.5k -> $0.70 (recomputed, tagged); periphery 36-64%; ~30 tiers; N-36 <=$115 (2.0%).
- Null hypothesis +$800; $25.0 / $12.5 / $6.2 per tier (83/42/21%).
- Capex $158k -> $61; $87k -> $8.0 (7.6x by arithmetic; model rounds to 8x); 93 wafers/month; $5.6-9.3; EUV $825-1,155, 19-27% of $4,308.
- Bonds: 3.64e6 + 0.85e6 = 4.49e6; ~45 dead links; >0.9 to ~6e-3 with 1% spares; bridge yield exp(-1.12) = 0.33; <0.95 above 5e-7.
- Pitch: 1.86/1.57/1.31 Gb/mm2, Cs 1.40/2.01/2.78 fF; kill ~2.5 um (1T1C) / ~3.0 um (gain); SA 1-5 um2 -> 1.69-2.16 Gb/mm2.
- Sensitivity no-rule 0.89/0.33/~0, $0.60/$1.65/>$100; particles W2W 0.97/0.70/0.24, D2W 0.99/0.92/0.73; bow 311-1,557 um; budget 0.375 um; 726/290 um tolerable bow; anneal 0.09-0.36 yr at 250 C.
- Stats: 1e7 links <=83 fails; 3e7 comb pairs, 34 mm2.
- FINAL_CONCEPTS: rank 9, EV 36 = 3x3x4; array eff 0.51; 0.97 x 0.95 x 0.99 = 0.91; ~220 dead segments on 50 mm2; ~$735k portfolio seed. concepts_device.json: ~$900k I-04714 critic tape-out; FPD steppers 1.2-1.5 um. Stage 2: I-02936 50-100 mV drift.
- A1: 1b Cs 5.4 fF, Cbl 35 fF. A2: 1,300 kWh, 8 m3, 0.42 kWh/GB, 2.6 L/GB, In/Ga <0.4%, Ga ~98% Chinese.
- Source logs: imec 1.08 um / 70,866 links; imec D2W 2 um daisy-chain >70%; imec+EVG 200 nm, <40 nm overlay; SoIC 9 -> 6 um; Xtacking <=10 um, 12.66 Gb/mm2; SeDRAM 0.88 pJ/bit; 3D NAND bow +300/-550 um; YAP+ 50% pad rule; litho pre-compensation halves residual; IGZO >300 C rearrangement; 180 C Cu/SiCN; OCTRAM Ion >15 uA, Ioff <1 aA; Purdue 3 tiers, >100k devices; SUSS XBC300 at NeoVation; ~65 low-NA EUV; SK hynix "five or more"; Samsung 6-7; Ga/Ge suspension to 2026-11-27; Qatar helium March 2026; OCP HBF Aug 2026; Micron Clay 48 MGD.
- Budget lines A-I sum to $700k; +$90k = $790k (12.9%); plan $990k = 71/20/9%; A+H+I = $75k; B-G = $625k; month mapping M8 Aug 2027 ... M24 Dec 2028.

## Fixes applied (surgical edits)

1. s2 sensitivity table, "Opens, with switched supplies | up to ~6e-3 | Yield 1.00". Model s5/s7: yield is 1.000 through 3e-3 and only >0.9 at ~6e-3 (spares exhausted at 1e-2). Changed to "up to 3e-3 (>0.9 to ~6e-3) | Yield 1.00; $0.54 (spares exhausted at 1e-2)".
2. s2 corrections, "Word-line bonds ... with it they are ~19%". Ambiguous (19% of signal bonds would be wrong; model 0.85e6/3.64e6 = 23%). Clarified as "~19% of all bonds (0.85e6 of 4.49e6)".
3. s8 energy. "~0.24 kWh/GB (~1.7x lower)" compared the model's 10,804 GB/pair against A2's 0.42 kWh/GB (which implies ~3,100 GB/wafer), while "break-even ~4.2x" used the model's 2,568 GB basis. Restated on the model basis: ~2.1x below ~0.51 kWh/GB (1,300 kWh / 2,568 GB), with ~1.75x on A2's basis noted.
4. s3 genuine delta 1 (prior art). "None was found" qualified to "No open bitline-level spec was found", adding UCIe (die-level, named by the I-04714 Stage 2 critic) and noting the in-house splits are proprietary versions of the same cut.

No git commit made.
