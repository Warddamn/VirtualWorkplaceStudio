# Assumptions: p1-model (models/dram_cost_stack.py)

As of 2026-11-01. Each item below is also an `INPUTS` entry in `models/dram_cost_stack.py`, with its source string and tag. Inputs taken from `research/phase1/cost_inputs.json` keep p1-cost's assumptions, which are listed in `research/assumptions/p1-cost.md`.

## Access limits
- [p1-model] **No first-hand web verification was possible.** WebSearch returned "budget used up": the shared 200-call budget was spent by earlier agents. WebFetch failed with ENOTFOUND for trendforce.com, eetasia.com and buysellram.com. Every market price in the model is therefore REPORTED (an URL another agent saw in a search snippet) or UNVERIFIED. — basis: tool errors in this session, 2026-11-01.

## Model structure
- [p1-model] **Die yield** is a negative-binomial model (alpha = 10).
  - The effective defect density D0 is calibrated so that each node's reference die (16Gb DDR5, 8Gb DDR4, 4Gb DDR3) hits the stated yield.
  - Larger dies on the same node (24Gb, 32Gb, DDR4 16Gb) and the ±20% die-size sensitivity therefore change yield as well as GDPW.
  - With the 1-beta reference at 0.90 (41 mm²), 24Gb yields 0.854 and 32Gb yields 0.815.
  — basis: Chiplet Actuary / ECO-CHIP yield form; DRAM redundancy means the stated yield already reflects repair.
- [p1-model] **Probe cost** is charged on every gross die, so it is divided by yield. Probe and final test/burn-in cost per die scale with (Gb / reference Gb)^0.5. Package cost is flat per die. — basis: parallel memory ATE amortizes test time sublinearly with density; the FBGA substrate does not depend on bits.
- [p1-model] **Final-test fallout** for packaged parts is 0.99 (0.97–0.995). — basis: judgment; it adds ~1% to component cost.
- [p1-model] **Legacy back-end per die** = $0.30 per 8Gb DDR4 die and $0.30 per 4Gb DDR3 die (p1-cost $/GB inputs × GB per die). It is split into probe, package and test in the same proportions as DDR5 (22% / 40% / 38%). — basis: p1-cost inputs; the split is p1-model's judgment.
- [p1-model] **DDR4 16Gb 1y die = 88 mm²** (range 76–107). — basis: 8Gb 1y (45 mm²) × 1.95, the 16Gb/8Gb area ratio at 1z (76/39). The low end is the 16Gb 1z die; the high end is 8Gb 1x × 1.95.
- [p1-model] **The DDR4 16Gb depreciated-line case** uses the legacy depreciated wafer ($1,300 cash cost) and a yield of 0.92 referenced to the 55 mm² 8Gb 1x die. — basis: p1-cost §9.
- [p1-model] **The trailing-node DDR5 case** uses CXMT's 16Gb G4 die (66.99 mm², REPORTED teardown) on a $3,000 DUV-only 1z-class wafer at mature yield (0.90 at its own area). — basis: p1-cost §6.1 1z reference row. CXMT's actual yield is unknown and may be lower.
- [p1-model] **HBM3E 12-high:**
  - Core die yield 0.80, applied at the 110 mm² core-die area.
  - Stack yield 0.75.
  - Wafer = 1-beta + TSV adder $650.
  - Each core die also carries a KGD probe cost.
  - Base die $15 and stacking $25 make up the "package" column.
  - The 12 core dies use 1-beta wafers; base-die wafer usage is ignored.
  — basis: p1-cost §5.4. The computed trade ratio of 2.8:1 matches Micron's REPORTED ~3:1.
- [p1-model] **The GDPW formula assumes square dies.** Real DRAM dies are rectangular, roughly 1.5–2:1, which costs a few percent of GDPW. This is inside the die-size sensitivity. — basis: the standard formula.
- [p1-model] **Modules:**
  - RDIMMs carry +25% raw bits for side-band ECC, so a 64GB module holds 80 GB raw.
  - UDIMMs are non-ECC.
  - The module yield of 0.985 applies to the whole module cost (DRAM + BOM + assembly).
  - The 96GB RDIMM and the 48GB UDIMM use 24Gb dies.
  — basis: p1-cost BOM and formula.

## Market prices
- [p1-model] **The Q4-2026 64GB DDR5 RDIMM contract base is $1,300** (low $1,200, high $1,586).
  - It is built from Counterpoint's "possibly >$1,000 in 2Q26" (EE Times Asia), compounded by TrendForce's 3Q26 (+15.5%) and 4Q26F (+12.5%) conventional-DRAM QoQ midpoints.
  - The high end is Citi's 4Q26F of $1,586, which is UNVERIFIED (underlying page not identified).
  - Compounding from 1Q26's $900 through TrendForce 2Q–4Q gives $1,877. That is printed as an upper cross-check, not used, because server RDIMM pricing apparently rose more slowly than the blended index in 2Q26 ($900 → ~$1,000).
  - Using $1,300 instead of $1,586 makes margins and the glut price slightly conservative.
  — basis: REPORTED snippets via p1-market.
- [p1-model] **The DDR5 component contract price (per raw GB)** is backed out of the RDIMM: (module − $20.6 non-DRAM BOM and assembly) / 80 GB = **$15.99/GB**. That is about $32 per 16Gb chip, against p1-cost's derived $30.7. — basis: no chip-level contract price is public outside TrendForce's paywall.
- [p1-model] **Glut = −60% from the 2026 peak, taken as Q4-2026** (ASSUMPTIONS.md A-05).
  - The rule is applied to both component and module $/GB.
  - The severe case is −90% (the high of `glut_price_decline_fraction`).
  - If the actual peak is 1H27 (p1-market's call: peak 4Q26–2Q27), the glut price would be proportionally higher.
  — basis: A-05; market.md §7.
- [p1-model] **The 2023 trough** is DDR5 16Gb at $3.2/chip ($1.60/GB, UNVERIFIED prior knowledge from p1-cost) and DDR4 8Gb contract at $1.30/GB (REPORTED, KED Global). The 64GB RDIMM trough price is derived as trough chip price × 80 GB plus non-DRAM BOM. — basis: cost_inputs.json.
- [p1-model] **The Q4-2026 DDR4/DDR3 contract is taken at parity with DDR5 per GB** (ratio 1.0, range 0.8–1.65).
  - No legacy contract level was found.
  - Barclays (Oct 2026, via p1-market) has DDR4 contract rising faster than DDR5 and dearer in some channels.
  - The DDR4/DDR5 spot ratio per GB on 2026-08-31 was 1.65, which sets the high end.
  — basis: market.md §2.4.
- [p1-model] **The −60% glut applied to HBM3E is illustrative only.** HBM sells on annual LTAs, and A-05 is defined for DDR5. — basis: market.md §2.5.
- [p1-model] **UDIMM "market" price** = DDR5 chip contract × GB + client BOM and assembly, a contract-equivalent. U.S. retail ($14–18/GB, Sep 2026) is shown only as a reference. — basis: the inputs hold no PC-module contract series.

## Sensitivity
- [p1-model] The ±20% yield sensitivity caps die yield at 0.99, so the upside is asymmetric at mature yield. Wafer cost ±20% also scales the HBM TSV adder. Die size ±20% moves GDPW and the negative-binomial yield together. — basis: task spec ±20%; physical cap.
