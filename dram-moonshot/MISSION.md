# MISSION: NEW DRAM — invent better ways to make working memory

Started 2026-11-01 as a follow-on to `../ram-venture/`. That study judged memory ideas as businesses for a part-time founder with under $50k. This one judges them as **inventions**.

## The question
What new ways of making **DRAM-class memory** could deliver a step change on at least one axis that matters? "DRAM-class" means byte-addressable working memory with ~10–100 ns access and effectively unlimited endurance, either natively or through architecture. The axes are:
- cost per bit;
- density;
- energy per bit, including refresh;
- manufacturing capital intensity (fab $, mask count, EUV dependence);
- material and resource intensity (scarce or concentrated inputs, energy, water, PFAS);
- U.S. manufacturability and supply-chain independence.

## Framing (the founder's)
- **"Anything is possible if executed correctly, and persistence is how breakthroughs happen."** Do NOT kill ideas for business reasons, time to revenue or founder fit.
- **Kill only for physics.** An idea dies only if it violates physics, or hits a known show-stopper with no plausible way around it.
- **Every kill names its revival condition:** what would have to be true for the idea to live.

## Capital frame
A Thiel-Fellow-style team:
- **Seed:** $1M.
- **Team:** two full-time founders, one of them a recruited device or circuit expert.
- **Demo:** a convincing one within 18–24 months, using MPW shuttles, university nanofabs and national-lab user facilities.
- **Raise:** then $10–50M.
- **Scale:** license to or partner with memory makers and foundries, or go fab-lite.
- **No limit:** the long-term ambition is unbounded.

## Rules
1. **Physics first.** Cite papers, patents or credible data wherever possible. Clearly label speculative physics as [SPECULATIVE], with the first-principles estimate.
2. **Compute numbers, don't vibe them.** Estimate density (bits/mm²), retention, energy/bit, speed and mask count with explicit arithmetic. Put reusable estimates in Python under `models/`.
3. **Novelty matters.** Distinguish known approaches (and who is pursuing them) from genuinely new combinations or twists. Prefer ideas a small team could *prove* at small scale.
4. **Reuse, don't redo.** Prior work lives in `../ram-venture/`: device cards in `research/phase2/A1-A3*.json`, the $/GB device model `models/device_cost_compare.py`, the landscape `01_LANDSCAPE.md` and the DRAM cost stack `models/dram_cost_stack.py`.
5. **Log everything.** Use the same source-logging and assumption-logging conventions as `../ram-venture/research/CONVENTIONS.md`, but write to `dram-moonshot/research/sources/` and `dram-moonshot/research/assumptions/`.

## Planned phases
- **A.** Bottleneck map: physics and scaling limits, materials and resources, the 2023–26 research frontier.
- **B.** Divergent ideation through five lenses.
- **C.** Physics adversarial triage.
- **D.** Ranking with the Thiel-Fellow lens.
- **E.** Technical dossiers: first experiments, the $1M budget, who to recruit and which labs to use.
- **F.** Physics red team, then final picks.
