# Assumptions: dos-cell-wafer-foundry (2026-11-02)

- [dos-cell-wafer-foundry] Vertical-bitline pitch along the WL = 80 nm (2F at F = 40 nm) -- basis: concept's litho-light F ~40 nm, A3 s2.9 table (80 nm BL pitch).
- [dos-cell-wafer-foundry] 28 nm sense amp (offset-cancelled latch + precharge + column gate) occupies ~2.5 um2 (sensitivity 1-5 um2) -- basis: ~16-20 matched transistors vs ~0.13 um2 28 nm 6T SRAM cell; no layout done.
- [dos-cell-wafer-foundry] 3 V word-line driver ~3 um2 in 28 nm thick-oxide devices -- basis: judgment.
- [dos-cell-wafer-foundry] SA + WL-driver periphery may fill <=85% of the array footprint; fixed periphery 3 mm2 per die -- basis: judgment.
- [dos-cell-wafer-foundry] VBL capacitance 0.08 fF per tier, off selector 0.04 fF, global wire 0.15 fF/um, SA input 1.5 fF -- basis: A1 planar 0.06 fF/cell; B3-01 values.
- [dos-cell-wafer-foundry] Destructive-read 1T1C groups vertical bitlines along rows (global line spans M rows); gain cells cluster (line ~ sqrt(M x footprint)) -- basis: every bitline crossed by an active WL needs a sense amp for destructive read.
- [dos-cell-wafer-foundry] 1:8 oxide-TFT WL predecode on the cell wafer; WL segment 400 um; staircase step 0.5 um/tier -- basis: 3D NAND practice, WL RC.
- [dos-cell-wafer-foundry] Pad diameter = 0.5 x pitch; overlay budget = 50% of pad diameter -- basis: YAP+ (arXiv 2511.05506).
- [dos-cell-wafer-foundry] Bridges = 0.1 x opens; 25% of a signal pad's neighbours are unswitched supplies without the spec rule, 0% with it -- basis: judgment.
- [dos-cell-wafer-foundry] Residual non-linear run-out after scaling compensation = 10% (sensitivity 25%) -- basis: judgment; imec/EVG <40 nm on flat wafers is the best case.
- [dos-cell-wafer-foundry] Pre-bond surface energy 0.1-1 J/m2 and particle density 0.05/cm2 (>=0.5 um) on fab-grade surfaces -- basis: judgment; Tong-Gosele formula.
- [dos-cell-wafer-foundry] Cell wafer base $700, $30/tier (A1), 28 nm periphery $2,800 (ram-venture v4-cost), W2W bond+thin $400/pair, D2W +$300, monolithic CuA base $300 -- basis: estimates except where cited.
- [dos-cell-wafer-foundry] Cell-line capex per $ of processing = 0.8 x an EUV DRAM line -- basis: judgment (lower litho share).
- [dos-cell-wafer-foundry] Experiment costs (Purdue SRA $170k, bonding partner $280k) -- basis: concept's $300-400k partner estimate; no quotes obtained.
