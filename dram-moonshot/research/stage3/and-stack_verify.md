# AND-STACK: dossier verification log

Verifier: `dosv-and-stack`, 2026-11-02. Target: `dossiers/and-stack.md`. WebSearch used: 0 of 2. Every decisive fact traced to the model or a logged source, so no search was needed.

## Results by check

| Check | Result | Notes |
|---|---|---|
| (a) Model runs | PASS | `python3 models/and-stack.py` exits 0 and rewrites `research/stage3/and-stack_model_output.md`. |
| (b) Sections 0-10 | PASS | All 11 sections are present and substantive: a header with three verdicts, the mechanism with a diagram, physics §2.1-2.10, a prior-art table, 11 show-stoppers, the decisive experiment with a budget, a quarterly 24-month plan, the scale path, resources, 9 dated kill criteria and sources. |
| (c) Number tracing | PASS after 6 fixes | 52 numbers spot-checked against the model output, `FINAL_CONCEPTS.*`, `and-stack_notes.md`, Phase A/B files and `research/sources/*.jsonl`. Six numbers disagreed with the model or with arithmetic and were fixed (below). |
| (d) Decisive experiment | PASS | Phases 0-1 cost ~$205-230k and give GO/NO-GO #1 at month 11. The full standalone plan is $985k, with GO/NO-GO #2 at month 22-23. Pass/fail numbers are set in advance: CR >= 0.53 with sigma <= 0.03 over >= 50 cells, <= 142 fA per unselected cell, <= 30 mV disturb after 1e9 writes, and the 1e-4 tail drifting <= 86 mV over 1 s at 85 C. NO-GO is CR < 0.40, > 100 aA or > 1 LSB. Stack #2 needs tier sigma_CR <= 0.03 and tails within 2x of planar. |
| (e) Prior art not overstated | PASS after fixes | The dossier never says "none". Its delta claim, that nothing found combines all four elements, is hedged and matches the critics. But Stage-2 critics named prior art that §3 left out: Huawei vertical CAA IGZO 2T0C (I-03474, I-10833), Toshiba NAND-structured DRAM (I-10664), Chipkill and Micron RAIN (I-00729, innovation DROP) and Macronix LSM (I-11544). Section 3 also listed tier-orthogonal erasure as a claimable piece without saying I-00729 was DROPped on innovation. Fixed (below). |
| (f) Founder pronouns | PASS | No gendered pronouns. The founders are "Founder A/B". |

## Fixes applied (model is the source of truth)

1. **§2.8, pitch sensitivity.** Bits/$ was "~3.4x" at 160 nm and "~3.1x" at 170 nm. Re-running `usd_per_gb(64,2)` at those pitches gives 3.51x and 3.21x, so the text now reads ~3.5x and ~3.2x. Density (7.1x, 6.3x) and webs (34, 44 nm) were already correct.
2. **§2.8, leakage.** "That is still 19x DDR5's interval" read as if it covered 2 b. It is true only for 1 b (0.62 s / 32 ms). 2 b gets 0.21 s, which is 6.6x. Both ratios are now stated.
3. **§4 #1.** "0.25 s refresh, still 128x rarer than DDR5" was wrong: 0.25 s / 32 ms = 7.8x. It now reads ~8x, with the 85 aA 2-b budget added.
4. **§4 #11.** "> $80/tier gives < 2.5x" was wrong. At 1% defects the model gives 2.85x at $80/tier and drops below 2.5x only above ~$105/tier. The text now reads "> ~$105/tier gives < 2.5x at 1% defects ($80 gives 2.9x; 1.8x at 10%)".
5. **§9 kill criterion 8.** The trigger was "> 30% non-confined and > 2% per-tier killer rate -> 64 x 2 b < 2.5x". At 30% and 2% the model gives yield 0.61 and 3.09x, not < 2.5x. It crosses 2.5x at a per-tier rate of ~3.5% (2.49x). The threshold is now > 3.5%.
6. **§6, allocation.** The budget said "~39% fab", but the fab lines are $150k + $330k = $480k of $985k = 49%. With 39% the percentages summed to 91%. It now reads ~49%.
7. **§2.4, headroom.** "A few hundred zA" became "<= ~250 zA", the model's figure.
8. **§0, constituent ideas.** Stage-2 verdicts were added where they existed but were missing: I-00729 ADVANCE physics / DROP innovation (Chipkill, RAIN), I-00869 ADVANCE/HOLD, I-01312 ADVANCE/ADVANCE, I-02936 ADVANCE/ADVANCE, I-11544 HOLD/HOLD (Macronix LSM) and I-11559 ADVANCE/ADVANCE.
9. **§3, prior art.** Five rows were added: Huawei vertical CAA IGZO 2T0C (logged at dc.engconfintl.org), Micron US6246083 vertical gain cell (logged in dos-and-stack.jsonl), Toshiba NAND-structured DRAM, Chipkill / Micron RAIN and Macronix LSM. The last three are tagged [UNVERIFIED-PK], critic-named. The tier-orthogonal-erasure claim is now marked the weakest; only the tier mapping and the raw-BER contract are candidates. Both logged URLs were added to §10.

## Numbers spot-checked (match unless listed above)

1. Area per hole 0.0224 um2 (sqrt3/2 x 150^2 x 1.15)
2. Raw 0.0446 Gb/mm2 per bit-tier
3. 0.0284 Gb/mm2 after 0.7/1.1
4. Parity at 15.7 bit-tiers
5. 32 x 2 b: 1.82 Gb/mm2, 4.1x, 2.86 um, 32:1
6. 64 x 2 b: 3.63 Gb/mm2, 8.1x, 5.42 um, 60:1
7. 64 x 3 b: 5.45 Gb/mm2, 12.2x
8. Staircase 4.7%
9. Web 24 nm
10. C_IPD 0.173, C_gate 0.059, C_par 0.015, C_SN 0.246 fF, CR 0.70
11. Back-face-only CR 0.54
12. 142 fA (0.89 uA / 1e5 / 63)
13. I(Vt) 39 nA (100 nA x W/L 0.39); 5.4 decades; 0.49 V; +0.01 V
14. 1.09 V pull-down
15. 1.79 V swing and 1.15 MV/cm at CR 0.70
16. CR >= 0.53 bar
17. CR table: 0.40 -> 3.51 V, 4.0 MV/cm; 0.55 -> 2.37 V, 2.1; 0.70 -> 1.79 V, 1.2
18. Neighbour 8 mV, kickback 130 mV, kTC 4.5 mV
19. 333 mV = 512 electrons (0.333 V x 0.246 fF / q)
20. Read current 0.89 uA (20 x 1.15 uF/cm2 x 0.39 x 1 x 0.1)
21. C_BL 8.9 fF; 298 nA; 1.5 ns
22. ~15 ns read; 1.5 fJ; ~90 fJ and ~100 ns 2-b write
23. Random sigma 13.8 mV; raw BER 1e-8; 86 mV max drift
24. 3 b margin -19 mV; 1.5 V window, 10 mV coupling, 48 mV
25. 21 aA at 1 s; 0.33 aA at 64 s; 1.2e-7 and 1.8e-9 A/cm2
26. Refresh 11.5 / 0.37 / 0.006 mW per GB; 31x; ~2,000x (1998x)
27. 1.3e9 pulses, 780x inside 1e12
28. Hot row 2.8e14, ~280x short
29. No-erasure yield 0.47 (0.99^64 x 0.95 x 0.97 x 0.97)
30. Erasure yield 0.84 (10% non-confined) and 0.74 (30%)
31. Wafer $5,920; 1.56x; 7.7x GB (23,708 / 3,069)
32. Cost table 0.99/1.5x, 0.56/2.7x, 0.65/2.3x, 0.39/3.8x, wafer 0.25/5.0x
33. Break-even 19 tiers (1 b) and 9 tiers (2 b)
34. Sensitivity grid at $15, $30 and $80 (9 cells)
35. Pitch 160/170 nm density 7.1x/6.3x (bits/$ fixed, item 1)
36. 0.21 s and 0.62 s at 100 aA
37. 62 ms at 1 fA (1 b); 62 aA at 1 s (1 b)
38. IPD EOT 2.0 nm -> CR 0.75
39. 10 decades of write-FET suppression (model 10.1)
40. 0.998^300 = 55%
41. Endurance kill 1e10 = ~8x 1.3e9
42. 1e12 cycles in ~28 h at 10 MHz
43. Budget total $985k; founders 19%, bench 9%, analysis 8%, IP 5%, design 3%, overhead 8%
44. Phases 0-1 ~$230k (notes: includes bench and IP shares)
45. Card values 4.5-8.9x, 3-12x and 0.6, read ~3.8 uA / 0.3 ns, A3 ~1.56x at 3 b x 8, EV 5 x 3 x 4 = 60, rank 3 (FINAL_CONCEPTS)
46. N-56 4-8x less H (Phase B); imec H+O anneal ~30x; SJTU 100x passivation (sources)
47. Kioxia OCTRAM 8 layers, Ioff < 1 aA; NEO > 1e14 (sources)
48. tRFC 295 ns; Samsung 1c 6-7 EUV layers; Micron 1-gamma 1 layer; AR 60-90:1 (sources)
49. Notre Dame $124/h; UNM $88-250/h; NUFAB $37-77/h x2 (sources)
50. Ga/Ge suspension to 2026-11-27; hafnium ~$5,000 -> ~$13,115/kg; ZTO > 1,500 s (sources)
51. EUV 10.2-12.2 GWh/yr, ~10% of fab electricity; >= 256-layer rare-earth review (sources)
52. SK hynix ~$4B on 2026-08-27; Micron Manassas 2026-05-22; second Idaho fab late 2028 (sources)
