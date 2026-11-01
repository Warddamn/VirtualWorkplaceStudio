# Assumptions: agent p3-devmodel (device cost comparison, `models/device_cost_compare.py`)

Written 2026-11-01. No WebSearch was used (quota 0). All inputs come from files written by other agents. URLs are cross-references logged in `research/sources/p3-devmodel.jsonl`.

## Method
- [p3-devmodel] One area-based cost equation for every device: $/GB = wafer_cost / (usable_mm2 x density / 8 x yield) + test_pkg $/GB. Basis: the task spec (mission section 3A). The A2/A3 die-based scratch models give the same answers to within a few percent.
- [p3-devmodel] Usable wafer area = gross dies per wafer of a 100 mm2 reference die x 100 mm2, using the Chiplet Actuary GDPW form with edge 3 mm and scribe 0.08 mm from `cost_inputs.json`. That is 0.854 of a 300mm wafer and 0.790 of a 200mm wafer. Basis: matches A3's "85% usable" convention. A calibration row reproduces the dram_cost_stack DDR5 1b cost to within about 3%.
- [p3-devmodel] When a filing gives both a cell area and a die density, the filed die density is used and the array efficiency is back-solved (printed as eff_used). Basis: filed densities include measured die data (3D XPoint Gen1/Gen2, Everspin 1Gb) that the cell formula overstates by up to 1.75x.
- [p3-devmodel] Wafer cost, yield and test/package come from the branch filings unchanged. They are not harmonised to the canonical $/wafer. Basis: the filings are the assigned inputs. The -30% wafer sensitivity roughly harmonises branch DRAM-class wafers ($5.5-7k) with the canonical 1b wafer (about $3.8k).
- [p3-devmodel] Sensitivity is wafer cost x0.7/x1.3 and yield 0.50-0.95 (task spec). "Cannot win on $/GB under any sensitivity" means the best case (x0.7, 0.95) is at or above the A-05 glut price. Tiers: A <= DDR5 incumbent cost, B < glut, C < Q4-2026 contract, D above contract.
- [p3-devmodel] DDR5 reference numbers are imported live from `models/dram_cost_stack.py` `ddr5_reference()`. During this run, Phase-1b agent v4-cost was revising that model. The live values on 2026-11-01 17:5x UTC were cost $1.484, contract $20.367, glut $8.147 and severe $2.037 per GB, vs the brief's $1.641 / $15.993 / $6.397 / $1.599. Section 5 of the output reports verdicts under both decks and a list that holds on either deck. Basis: the task said to use the model's exact values.
- [p3-devmodel] Test and package stay fixed per GB across the yield sensitivity. Basis: simplicity. Probe cost scales weakly with yield, which is second-order next to wafer cost/yield.

## Defaults (used only where a filing lacked a value; each use is flagged in the PARAMETERS table)
- [p3-devmodel] A1-11 SunRise 3D NOR has no density filed. Default 0.39 Gb/mm2 (DDR5 1b, 16Gb/41 mm2), on the reading that the claim "DRAM-like $/GB" implies DRAM-parity density. Basis: no public silicon data. The concept is Rule-1 UNSUPPORTED anyway.
- [p3-devmodel] A3-12 2D-material gain cell has no wafer cost and no yield. Defaults: $1,400 SkyWater 200mm 130nm wafer + $1,000 2D-tier adder, yield 0.30, and test/package at $0.015/mm2 of die ($/GB = 0.12/density). Basis: TRL 2-3 with no production line. The concept is Rule-1 UNSUPPORTED.
- [p3-devmodel] A2-11 Optane salvage has no fab. The "wafer cost" is replaced by an acquisition cost of $1.40/GB (midpoint of A2's [UNVERIFIED] $0.8-2/GB), and yield is the health-test pass rate (0.9 as filed). Basis: A2 filing.
- [p3-devmodel] A3-13 printed labels: $/GB = $0.10 per 20-bit label / yield. Basis: the A3 filing's wafer_cost_basis.
- [p3-devmodel] A1-03 display glass uses 90% of a 5.5 m2 Gen-8.5 sheet at the filed $500 per sheet. Basis: A1 filing; utilisation is my estimate.
- [p3-devmodel] Embedded, compute and buyer rows keep the filed test+package of 0 (A1-01, A1-10, A2-08, A2-09, A2-14, A3-03, A3-04, A3-08, A3-10, A3-14), so their $/GB is an area-equivalent silicon cost. Basis: filings say the cost lands in the host SoC.

## Mapping and verdict choices
- [p3-devmodel] tmp_id variants map to their base id: A1-02 second row -> "A1-02s", A3-02b -> C-31, A3-06-nXX -> C-35. A2-12 maps to C-51 (absorbed into B-08). Basis: `tmp_to_id.json` and the dedup map.
- [p3-devmodel] Two variants are excluded from concept verdicts but still costed. A3-02b (Kilopass VLT) is excluded because the filing says "do not use as a live option". A1-02s (300mm 28nm BEOL) is excluded because no U.S. foundry offers that line and C-02 is defined on a U.S. 200mm line.
- [p3-devmodel] Added supplementary rows for silicon-making concepts outside branch A. C-58 uses dram_cost_stack ddr4_8g_1x_new, C-59 uses ddr3_4g_fdry, and C-71 uses the C_notes Appendix A figures: 116 mm2, 137/228 good dies, $2,000 wafer, $15 package+test per unit. Basis: "every device/material concept".
- [p3-devmodel] The non-$/GB axis is derived by keyword from each card's `wins_axis` text plus the device retention field. There are two overrides. C-02 is set to "standby power (refresh only)" because the card says "none for commodity buyers... refresh power only". C-05 is set to "none ($/GB-only bet)". Basis: card text.
- [p3-devmodel] F-RAM street reference is $1/Mbit = $8,192/GB, with a range up to $4/Mbit. Basis: A1-12 filing notes "~$1-4/Mbit" [ESTIMATE]. NOR reference is $40/GB [UNVERIFIED, cost_inputs].
- [p3-devmodel] Gb is decimal in A1/A3 and binary in A2 and in the DDR5 die capacities. I did not convert, because the difference (<=7.4%) is inside the yield and wafer sensitivity band.
