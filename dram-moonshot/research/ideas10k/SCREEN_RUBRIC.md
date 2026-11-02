# Screening rubric: 11,597 ideas → shortlist

*(Written for the first-round pool of 11,597. The 1,260 novelty top-up ideas were later screened with the same rubric, so all 12,857 ideas in `scored_ideas.jsonl` carry these scores.)*

You are a screener. Score every idea in your batch on four 1–5 scales, using these anchors. Judge each idea as an **invention or strategy**, not as a business for a particular founder.

The founder's framing: anything is possible if executed correctly, and persistence breaks through. So don't punish boldness. But be honest about physics, and about whether a $1M team could prove the idea.

Context: DRAM-class memory means byte-addressable working memory with ~10–100 ns access and effectively unlimited endurance. The bottlenecks are:
- the capacitor charge wall;
- no 3D DRAM cell;
- the leakage tail that forces refresh;
- litho/EUV capital;
- data-movement pJ/bit;
- the HBM TSV tax;
- 49% of the die going to periphery;
- destructive read and overfetch;
- row hammer;
- the voltage floor.

Resource chokepoints: helium, high-purity quartz, tungsten, EUV, energy and water. Canonical DDR5 is about $1.48/GB to make and $20/GB contract price.

| Key | Scale | 1 | 3 | 5 |
|---|---|---|---|---|
| **P** | Physics / feasibility plausibility | Violates physics or needs a miracle | Plausible, with real unknowns or a TRL-2–3 mechanism | Known physics; engineering only. Strategy and policy ideas: clearly executable |
| **S** | Step change if it works | <10% gain, or a niche | 2–3× on one axis, or a big gain in a sizeable segment | ≥10× on cost/bit, density, energy/bit or capital intensity, or a change in how the world gets memory |
| **N** | Novelty vs known art | Already done or widely pursued | A twist on known work, or a new application | Not seen before, or a new combination with a non-obvious insight |
| **D** | Demo-ability with $1M in 24 months | Needs a fab, $100M+ or a decade before any proof | A partial proof (simulation plus test structures, or a pilot) | A convincing demo or pilot fits in $1M: an MPW shuttle, a university nanofab run, an FPGA or software prototype, a policy pilot |

## Rules
- **Use the whole scale.** Most ideas are 2–3. Reserve 5s.
- **Duplicates:** if two ideas in your batch share the same core mechanism, put the earlier id in the later one's `dup_of`, and don't inflate either.
- **`theme`:** 2–4 words naming the mechanism family, for example "IGZO gain cell", "refresh-aware OS", "helium recycling", "DIMM reuse market".
- **`note`:** ≤25 words. It is required when S≥4 or N≥5: say the key insight, or the key doubt.

## Output
JSONL, one object per idea in the batch, written with Python `json.dumps`:

```json
{"id": "I-00001", "P": 3, "S": 2, "N": 3, "D": 4, "dup_of": "", "theme": "...", "note": "..."}
```

**Validate before finishing:** the number of lines must equal the batch size, and the ids must match the batch exactly.
