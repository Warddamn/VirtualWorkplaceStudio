# 10,000 IDEAS: brief for every ideation agent (read this, nothing else)

## The problem
The world is short of RAM. DRAM contract prices rose about 4× from Q4-2025 to Q4-2026. AI and HBM absorb wafer capacity, new fabs take 3–5 years and $15B+, and the U.S. makes about 1–2% of the world's DRAM.

We want new ways to make **DRAM-class memory**: byte-addressable working memory with ~10–100 ns access and effectively unlimited endurance, natively or through architecture. We also want new ways to **do DRAM's job with less of it**, and new **strategies** that raise the usable memory supply. A good idea delivers a step change on at least one of:
- cost per bit
- density
- energy per bit
- capital intensity (fab $, masks, EUV)
- scarce-resource intensity
- U.S. manufacturability

## Facts to aim at (from the Phase A bottleneck map)
1. **Capacitor charge wall.** Cs is ~4.5–5.4 fF in pillars with aspect ratios of 60–75:1. More charge needs AR ~115 or k ~70.
2. **No manufacturable 3D DRAM cell yet.** 3D needs ~26+ tiers to break even. The capacitor and the lateral transistor are the blockers.
3. **Access-transistor leakage tail forces refresh.** The tail is ≤13 fA. Refresh costs ~46 fJ/bit, 16–33% of idle power and 10–20% of bandwidth at 32–64 Gb.
4. **Litho-bound scaling and capital.** The cell is 6F² at F≈12 nm. It needs 5–7 EUV layers, and depreciation is ~55% of wafer cost. A node buys only ~10–20% cost per bit.
5. **Data-movement energy.** HBM is 3–4 pJ/bit and DDR5 ~10–20 pJ/bit. That is 20–25% of an accelerator's power.
6. **HBM TSV tax.** HBM uses ~3× the wafer area per bit of DDR5, and yield is down 20–30%.
7. **Periphery takes ~49% of the die.**
8. **Destructive read and 128× page overfetch.** A random read costs ~5.9 pJ per useful bit.
9. **Row hammer.** Rows now flip after ~1k activations.
10. **Voltage floor.** VARY ~1 V and wordline ~3 V, so CV² energy is stuck.

**Resources:** geology is not the limit. A GB holds ~42 mg of silicon. The limits are **concentrated chokepoints** and **capital, tools and time**:
- helium: Qatar ~30% of supply, offline since March 2026;
- high-purity quartz crucibles: Spruce Pine, >80%;
- tungsten: China ~80%;
- EUV: one supplier;
- also energy and water.

**Prior work:** in `../../../ram-venture/`, oxide-semiconductor (IGZO) gain cells, HZO ferroelectric, MRAM, ReRAM, PCM, capacitor-less, 3D DRAM, SRAM and exotics were already examined, so go beyond the obvious versions.

## Founder's framing
- Anything is possible if executed correctly. Persistence breaks through.
- Things are not done by being the same: try different approaches.
- Constraints and scarcity breed ingenuity.
- Wild ideas are welcome, but every idea needs a **concrete mechanism or concrete strategy**, not a slogan.

## Your job
You are assigned ONE cell, a **creativity technique × problem facet**, plus ONE **forced constraint**.
- Generate exactly the number of ideas you are given.
- The first half must be free; the second half must obey the forced constraint.
- Use the technique genuinely and visibly, so each idea shows the technique's fingerprint.
- Stay on your facet. It may touch others.
- Quantity with variety: **no two ideas may share the same core mechanism**. Vary the physics, materials, structures, scales and strategies.
- Avoid generic ideas such as "use AI", "use graphene" or "better ECC" unless you name a specific new mechanism.

## Output
Write one JSON object per line (JSONL) to the file path you are given. Use Python with `json.dumps` so the JSON is valid. Fields:

```json
{"cell": "T07-F03", "n": 1, "title": "<=12 words", "idea": "1-3 sentences: the concrete mechanism or strategy (what, how)", "why": "which bottleneck/axis it attacks and the rough gain claimed", "kind": "technology|material|process|architecture|system|strategy|policy|business", "constrained": false, "novelty": 3, "physics_risk": "low|medium|high|speculative"}
```

- `novelty` is your honest 1–5 self-rating: 1 means already done, 5 means you have never seen it.
- `constrained` is true for the second half of the ideas.

**Do not** use web search; this is pure generation. **Do not** git commit. After writing, check the line count and JSON validity with Python.
