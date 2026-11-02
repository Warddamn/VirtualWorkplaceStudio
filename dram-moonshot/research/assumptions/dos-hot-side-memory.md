# Assumptions: dos-hot-side-memory (HOT-SIDE MEMORY dossier, 2026-11-02)

- [dos-hot-side-memory] Vertical oxide 2T0C cell is 10F2 at F = 40 nm (0.016 um2), ArFi single exposure — basis: A3 s2.1 (vertical 8-12F2); concept card.
- [dos-hot-side-memory] Carrier array efficiency 0.50 (CMOS periphery under the array in the carrier CMOS wafer); BEOL all-oxide periphery 0.30 — basis: 1-beta DDR5 0.51 (A1 model); Stage 2 critique of I-02936 (25-35%).
- [dos-hot-side-memory] ECC/erasure parity 12.5% (RS(36,32) tier-orthogonal) — basis: I-00729.
- [dos-hot-side-memory] Accelerator = 2 x 800 mm2 compute dies; HBM 288 GB and 22 TB/s per GPU (19.2 TB/s alternative) — basis: Rubin coverage via search snippet; two-die layout is training knowledge.
- [dos-hot-side-memory] Oxide retention scales with Ea = 0.8 eV (swept 0.5-1.1) from imec's >200 s at 95 C; the reported time corresponds to a 100 mV level loss; the 1e-4 tail leaks 3x the reported cell — basis: no 125 C oxide 2T0C data found (search 2026-11-02).
- [dos-hot-side-memory] Usable storage-node window 600 mV (swept 300-800); write-verify placement sigma 10 mV; sense residual 8 mV; raw BER target 1e-4 — basis: RAW-BER CONTRACT and MARGIN STACK budgets; IMECAS 3 b/cell suggests a larger window is possible in dual-gate cells.
- [dos-hot-side-memory] Level drift grows as t^0.2 — basis: BTI-type power-law exponents 0.1-0.3.
- [dos-hot-side-memory] HBM energy 3.5 pJ/bit at the PHY/controller; on-die NoC from HBM PHY to SM 8 mm vs 1 mm for near-tier data placed above its consumer — basis: arXiv 2602.18568 (3.44 pJ/b HBM3E), 36Kr (HBM4 3-4 pJ/b); floorplan estimate.
- [dos-hot-side-memory] Near-tier energy uses a 2x overhead factor on modeled array/data-path energy plus 50 fJ/bit controller/SRAM; delivered energy is floored at the card's 0.3 pJ/b for savings — conservative choice.
- [dos-hot-side-memory] HBM utilization 60% and near-tier traffic share 50% (swept 0.2-0.9) — basis: decode-heavy inference with tensor-parallel weight slice + hot KV on the near tier; needs a trace study.
- [dos-hot-side-memory] Power $0.08/kWh, PUE 1.25, DC build $12/W, 5-year life — basis: U.S. industrial power and AI-DC build-cost rules of thumb.
- [dos-hot-side-memory] Memory sits ~5 K below Tj (10 um front BEOL at k_eff 2 W/mK, 1 W/mm2); BSPDN hotspots +14 C — basis: arXiv 2508.02284 snippet (attribution uncertain).
- [dos-hot-side-memory] Tier thickness 0.2 um, dielectric k 1.4 W/mK, 3% Cu thermal-via fill — basis: IMECAS channel height ~120 nm; SiO2.
- [dos-hot-side-memory] Logic-killing short probability 0.1% per tier and per bond; logic die worth ~$800 — basis: concept spec; ~$30k N2-class wafer / ~38 good dies (training knowledge).
- [dos-hot-side-memory] Carrier cost: 65 nm-class CMOS wafer $1,800 + $300 per oxide tier + $500 hybrid-bond/test - $150 blank carrier; BEOL tier $450; 90% capacity yield after binning — basis: order-of-magnitude fab-cost estimates.
- [dos-hot-side-memory] Seed plan salaries $5k/month per founder for 24 months — basis: lean Thiel-style seed.
- [dos-hot-side-memory] University nanofab and national-lab rates are not verified this session; DOE NSRC user time is free for non-proprietary work under peer-reviewed proposals — basis: training knowledge.
- [dos-hot-side-memory] GF 22FDX MPW is fabricated in Dresden, not Malta (Fraunhofer IIS snippet; ram-venture notes) — the card's "GF Malta 22FDX" is corrected; U.S.-made logic hosts are SkyWater S130/sky130 (Bloomington MN) or GF Malta 12/14 nm via a partner.
