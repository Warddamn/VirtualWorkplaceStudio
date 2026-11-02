# HOT-SIDE MEMORY: dossier verification log

Verifier: `dosv-hot-side-memory`, 2026-11-02. Target: `dossiers/hot-side-memory.md`. WebSearch used: 0 of 2. No decisive fact looked suspicious enough to re-search: every cited URL is in `research/sources/*.jsonl`, and the logged snippets support each claim as worded.

## Results by check

| Check | Result | Notes |
|---|---|---|
| (a) Model runs | PASS | `python3 models/hot-side-memory.py` exits 0, before and after the edits. Output matches `research/stage3/hot-side-memory_model_output.md`. |
| (b) Sections 0-10 | PASS | All 11 sections are present and substantive: header with 9 merged ideas and 3 verdicts, mechanism plus stack diagram, physics and numbers, prior art (13 rows before fixes), 10 show-stoppers, decisive experiment with 3 gates, 24-month plan, scale path, resources, 8 dated kill criteria, and sources (all URLs logged). |
| (c) Number tracing | PASS (0 numeric mismatches) | 48 numbers spot-checked (list below). One framing was clarified: the card's ~205 W was 100% of traffic at 8 TB/s. |
| (d) Decisive experiment | PASS | Experiments cost $622k; the full plan, with salaries, IP and contingency, is $982k. Gate A is due at M10, Gate B at M18 and Gate C at M22, with the data room at M24. Pass and fail numbers are set in advance: drift sigma <=24 mV (2 b) or 24-80 mV (1 b), with >80 mV failing; window >=600 mV (<=13 mV at 400 mV); tail retention >=1 s at 125 C (tail leakage <=7.5 aA); RO shift <=1% and Vt shift <=10 mV; heater dT <=5 K with vias; drift increase >50% fails. |
| (e) Prior art not overstated | PASS after fixes | The dossier never claimed "none", and it already says "combinations, not new physics" and that Chip Scale Review 2022 bars broad claims. Several items the Stage 2 critics named were missing, so they were added. AP Memory VHM WoW (I-11538 critic). NUS all-BEOL 2T0C and imec BEOL 2T0C eDRAM (I-11532 critic). RAIN, Chipkill and NAND bad-block management (I-00729 critic), because delta #3, fail-soft binning with erasure codes, was listed as a genuine delta without them. The search-gap sentence was reworded to "this search found no...". "The stage-2 critics killed" was corrected to "flagged as the killer doubt", because I-11538 was an ADVANCE. NAND mode-switching and temperature-compensated refresh were added as analogues for delta #4 [training knowledge]. I-11554 (N-57) has no Stage 2 record. |
| (f) Founder pronouns | PASS | No he/she/his/her/him. The founders are "Founder A/B". |

## Fixes applied (surgical edits to the dossier)

1. Section 2, watts: "the card's ~205 W assumed 100% of traffic at full bandwidth" was changed to "...at Blackwell's full 8 TB/s (224 - 19 W)". The card's step_change gives exactly 8 TB/s: 224 W at HBM rates vs 19 W on the near tier. Without that, the 563 W bound reads as a contradiction.
2. Section 3 table: AP Memory VHM WoW was appended to the N3XT/Graphcore row.
3. Section 3 table: a new row covers imec BEOL IGZO 2T0C eDRAM and NUS all-BEOL IGZO/MoS2 2T0C. The NUS URL is in the source logs and was added to section 10.
4. Section 3 table: a new row covers Micron RAIN, Chipkill and 3D NAND bad-block management.
5. Delta #1: "killed on refresh" became "flagged as the killer doubt (refresh at 95-105 C)".
6. Delta #3: it now states that the codes and binning are established, and that the delta is applying them to logic-bonded tiers.
7. Delta #4: the closest analogues were added, with a [training knowledge] tag.
8. Search gap: it is now qualified as a result of this mostly-snippet search, and notes that BEOL-compatible 2T0C cells exist.

## Numbers spot-checked against the model output, sources or Phase A/B (all match)

1. 10F2 at F = 40 nm = 0.016 um2; 62.5 Mcells/mm2
2. 0.0278 Gb/mm2 per carrier tier-bit; 0.0167 for BEOL
3. 0.889 Gb/mm2 and 89 GB/die at 16 x 2 b
4. Density table: 0.222/0.444/0.889; 0.50x/0.99x/1.99x; 22/44/89 GB; 44/89/178 GB (15/31/62%)
5. BEOL adds +0.133 Gb/mm2, +13 GB/die, +27 GB/GPU; 7-13 GB
6. 1-beta density 0.447 Gb/mm2
7. Arrhenius: 200 s x e^-0.667 = 103 s at 105 C (recomputed)
8. 6,417x fewer refreshes; 16 ms Si
9. 30 s vs 4 ms at 125 C
10. Ea sweep: 80-132 s (105 C); 15-61 s (125 C)
11. Implied leakage 75 zA
12. 2 b: Q = 3.65, total sigma 27.4 mV, allowed 24 mV (sqrt recomputed)
13. 1 b: 80 mV; 3 b: 0 mV
14. Refresh interval 4.4 s (15 mV) and 1.8 s (20 mV)
15. Sensitivity table: 2.8e-10, 9.5e-6, 1.4e-4, 2.0e-2, 8.1e-2; max bits; 89/44 GB
16. Window sensitivity 13/52 (400 mV), 34/107 (800 mV)
17. Bitline 8.1 fF = 64 x 0.08 + 3; 5.7 / 8.1 / 2.8 fJ
18. Energy table: 0.087, 0.134, 0.097, 0.153, 3.5, 3.95 pJ/b
19. 56 fJ/mm NoC (0.2 pF/mm x 0.75^2 x 0.5)
20. 193 W (recomputed: 22e12 x 8 x 0.6 x 0.5 x 3.65 pJ)
21. 10,559 kWh, $845, $2,313
22. 77 / 193 / 347 W; 70 W at 8 TB/s
23. 563 W full-traffic bound; 205 W card value (224 - 19 W at 8 TB/s)
24. Refresh power 2.04 W Si vs 9.7 mW oxide
25. 5.5 TB/s, 0.11%, 44,000 bonds, 0.10 mm2, 5 mW/mm2
26. 2.0e9 writes/cell in 5 yr; 1e12 in 5.6 h
27. Latency 30-40 ns vs 100+ ns, tagged [ESTIMATE]
28. Thermal: +2.3 K / +22.9 K; k_eff 13.4 W/mK; 2.4 K (recomputed)
29. ~100 C average; ~114 C hotspot (+14 C, arXiv 2508.02284 with its attribution caveat)
30. Yield 1-(1-p)^6 = 0.6% at 0.1%, ~$5; 5.85% at 1%; 15% for 16 monolithic tiers; 2% carrier-only at 1%
31. Killer density 1.25e-4/cm2 (-ln(0.999)/8 cm2)
32. Cost: $1,800 + 16 x $300 + $500 - $150 = $6,950/wafer; 64 sites x 80 GB; $1.36/GB; $3.55/GB at 8 x 1 b
33. DDR5 $1.48/GB; HBM4 ~$16/GB (capitalandcompute)
34. 100 ms refresh: 24/0.63 = 38 mV; 0.43 W refresh (89 GB x 8e9 x 60 fJ / 0.1 s)
35. Kill 1: 80/0.631 = ~127 mV
36. Kill 2: 22.5 aA; Gate A 7.5 aA (model leakage ceilings)
37. Kill 5: 0.9 pJ/b gives 3.9x, below 4x
38. Kill 8: <20% share means <77 W
39. Experiment budget total 622 (summed); 22FDX 4 x $17,997 = $72k (CMC snippet)
40. sky130 $15k per 100 chips (eeNews Europe / ChipFoundry)
41. Plan budget 240 + 622 + 40 + 80 = 982; contingency 8.9%
42. Rank 2, EV 64 = 4 x 4 x 4; ranks 2-4 within noise (FINAL_CONCEPTS.md)
43. Fab energy: 1,300 kWh / 5,120 GB = 0.25 kWh/GB; 8 m3 gives 1.6 L/GB; DDR5 0.42 kWh and 2.6 L; HBM 1.0-1.3 kWh/GB (A2)
44. Making 178 GB takes 45 kWh (178 x 0.254)
45. In/Ga under 0.4% at 40 tiers; Ga ~98% Chinese [UNVERIFIED-PK]; ban suspension to 2026-11-27 (A2, Fastmarkets)
46. HBM3E ~3x DDR5 wafer area per bit (Micron, Hot Chips 2026, Tom's Hardware)
47. SeDRAM 0.88 pJ/bit (XMC, MDPI); SJTU >30,000 s; Michigan ZTO >1,500 s; imec >400 s (IEDM 2020); IMECAS VLSI 2026 3 b
48. H budget ~3 ppm of one PECVD SiN tier (TRIAGE.md, B3-17)

## Not changed (noted)

- "Gate A ~$200k" in section 5 and "~$150k on the shared coupon run" in section 6 describe two different scopes: standalone, and inside the portfolio seed. Both are consistent.
- The 0.4% gallium figure follows A2's summary line ("under 0.4%"). A2's table gives "x40 tiers: Ga 0.4%".
