# LEAN ARRAY MODULE: dossier verification log

Verifier: `dosv-lean-array-module`, 2026-11-02. Target: `dossiers/lean-array-module.md`. WebSearch used: 1 of 2.

## Results by check

| Check | Result | Notes |
|---|---|---|
| (a) Model runs | PASS | `python3 models/lean-array-module.py` exits 0. Output matches `research/stage3/lean-array-module_model_output.md` apart from one trailing blank line. |
| (b) Sections 0-10 | PASS | All 11 sections are present and substantive: header with verdicts, mechanism, physics, prior art, 11 show-stoppers, decisive experiment, 24-month plan, post-demo, resources, 8 kill criteria, sources. |
| (c) Number tracing | PASS (0 numeric mismatches) | 45 numbers spot-checked; list below. Three attribution wordings fixed. |
| (d) Decisive experiment | PASS | Steps 1, 1b and 2 cost $590k and end by month 20. Pass/fail is pre-set: a_H2 >=0.17 GO, 0.10-0.17 CONDITIONAL, <0.10 NO-GO; +/-2 K; ER drift <=2%; selectivity drift <=5%; <=10% LFL in single fault; zero arcs. The full plan totals $995k over 24 months. |
| (e) Prior art not overstated | PASS after fixes | The "no production H2 backside use" claim matches both Stage-2 critics, and the dossier discloses US 10,395,963. Prior art the critics named was missing from section 3 and has been added. "No H2 TAC exists" has been softened to "was found". |
| (f) Founder pronouns | PASS | No gendered pronouns. Every "He" in the dossier means helium. |

## Numbers spot-checked against the model output (all match)

1. 34.0 kW/m2
2. Jump distance 63.6 um
3. Effective gap ~137 um
4. h = 1,180 W/m2K
5. dT = 28.8 K
6. FM per-gas factors 2.0 and 4.18
7. FM ratio 2.09x
8. Continuum ratio 1.17x
9. Gas table: He, H2 at 15 and 22.5 Torr, N2, Ar (h, dT, spread)
10. N2 spread "6x" (11.9/2.0)
11. Baule ratio 0.200/0.333 = 0.60
12. Baule prior a_H2 ~0.27
13. Break-even 0.241
14. Break-even 0.168
15. Break-even 0.098
16. Gap invariance 0.168/0.166/0.163
17. Asymmetric parity 23 Torr (model 23.1)
18. Sensitivity rows at 0.05/0.10/0.16/0.20/0.25 (dT shift, parity pressure, leak)
19. Bias rows: 16.1/19.2, 40.3/48.0, 80.6/95.9 K
20. Paschen minima 142 and 326 V
21. Paschen ratio 2.3x
22. Seal leak 1.06-2.50 sccm (arithmetic re-done)
23. H/F 0.5-1.2% on the 420 sccm F feed
24. Foreline 2.1% LFL; 42 sccm = 41.2 dump + leak
25. Single fault 10% LFL
26. 7.5 L/wafer
27. HeRS 22 L/wafer
28. Fleet 166k m3/yr
29. ~3% (1-11%) of DRAM He; 160M x 22.5% x 17% = 6.1M m3
30. $0.32/wafer
31. 104 u$/GB
32. H2 $0.007/wafer
33. $32M/day (100k/30 x $9,500)
34. Retrofit $75M
35. Payback 2.4 days
36. AAO pitch 35.2 nm, 14 V, mid-plane d 11.9 nm
37. Cs 5.84/7.01 fF, 76/88 mV, 67/81 ms
38. Anodization 34 Wh/wafer and 0.0026%; B2-01 8.4 Wh
39. IL 39 nm per 0.1 K
40. IL 6.3 nm at 0.3 ppm
41. 0.109 Gb/mm2 per tier, 0.24x, >=5 tiers
42. EUV $825-1,155/wafer, 19-27% (A1)
43. H2 ~1.7 t/yr, ~95 MWh, 0.006% of 1.56 TWh (1,300 kWh x 1.2M)
44. Budgets: 590 and 995 $k, both sums correct
45. Rank 8, EV 40 = 2x4x5 (FINAL_CONCEPTS)

Phase A traces confirmed:
- EUV $290M, ~10 GWh/yr, ~65 tools in 2026, 5% of DRAM wafer kWh (A2)
- Ga ~98% Chinese; ban suspension ends 2026-11-27 (A2)
- Helium: Qatar ~30%, Korea 64.7%, ~6 weeks of storage, spot $1,000-1,200 vs $500, no restart date as of June (A2 and sources)
- AR 60-75 capacitor (A1)
- 3-4 nm imprint-to-pad overlay (B2-01)
- Sandia "up to 0.10" (sources)

## Fixes applied to the dossier (surgical)

1. **Section 3, US 10,395,963 row.** Added "carrier patent within the result set not pinned". The source entry says the carrier patent is not pinned.
2. **Section 3, ASML clamp row.** "ESC with gas-gap cooling in low-pressure H2-rich EUV tools" now says the backfill gas aids cooling and that "whether that gas is H2 is not confirmed". The notes say exactly this.
3. **Section 3, Sandia row.** "No H2, no coated backsides" became "No H2; no CFx-residue backsides". The verifier search shows Sandia measured SiN and polysilicon surfaces, with He/N2/Ar only.
4. **Section 3, prior art named by the Stage-2 critics was missing.** Added:
   - Intel/Borodovsky complementary lithography and Phase B N-32 (critics on I-07130);
   - IBM SOI eDRAM micro sense amp, Barth ISSCC 2007-08 (critics on I-00257);
   - microchannel plates and photonic-crystal-fibre stack-and-draw (critics on I-11235).
5. **Section 3, delta 2.** "No measured H2 accommodation ... exists. The Step-1 dataset is new science" became "... was found (Stage 2, Stage 3 and a verifier search). The Step-1 dataset would be new science".
6. **Section 4, show-stopper 1.** "Plasma contamination cut He's value by up to 0.10" was inverted relative to the source. The source says an in-situ Ar-plasma *clean* lowered He TAC by up to 0.10. Also added the 1932 Phys. Rev. H2-on-tungsten result (0.54 bare vs 0.14 under an adsorbed-H film) [REPORTED]. It shows that adsorbates can move a_H2 across the GO/NO-GO band.
7. **Section 2.3.** "0.5 sccm seal leak at 15 Torr [REPORTED]" became "0.5 sccm [REPORTED], taken at 15 Torr [ESTIMATE]". The patent snippet gives no pressure, and the model tags 15 Torr as an ESTIMATE.
8. **Section 10.** Added the Phys. Rev. 40, 78 DOI. It is logged in `research/sources/dosv-lean-array-module.jsonl`, along with the refined Sandia surface list.

## WebSearch (1 used)

- Query: H2 thermal accommodation on SiO2, measured by the gas-gap method. No direct measurement on SiO2, SiN or poly turned up. This supports the key unknown, so the claim was softened, not removed. The search also yielded the Sandia surface list and the 1932 H2/W adsorbate result.

## Residual notes (not changed)

- **Paschen constants and world helium of 160M m3 are unverified.** Both are already tagged ESTIMATE in the model. The dossier conservatively carries the critics' measured 1.8x, not the model's 2.3x.
- **Two test leaks are used.** Step 1b and kill criterion 3 use a 2.5 sccm bleed (the viscous upper bound). The model's GO text uses 2x 1.1 sccm. They are consistent: 2.5 is the stricter value.
- **The notes say 22 months; the dossier says month 20 for the experiment and 24 for the plan.** The dossier is internally consistent.
