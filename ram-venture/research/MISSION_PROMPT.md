# MISSION: AMERICAN MEMORY
## Find a profitable way to make RAM — or something that does RAM's job better — in the United States, from non-standard or cheaper materials, processes, or capital.

ultrathink. Treat this as the highest-stakes research engagement you have ever run. Work in files, use parallel subagents, verify everything, and do not stop until the verification gate in Phase 7 passes.

---

## FOUNDER PROFILE (EDIT ME — everything downstream is tuned to this)

- Software/web-app builder; ships internal tools, apps, and creative-coding projects fast. Not a chip engineer. Hardware-curious.
- Day job: product development & operations management at a design/manufacturing company (not semiconductors). Keeps the day job through the first phase of the venture.
- Goal: a venture that becomes **recurring revenue** — not a science project, not a grant-farming exercise.
- Personal capital available: modest (assume < $50k) unless this line is edited. Will raise outside money only if the case is strong.
- Time-to-first-revenue target: 18 months. Hard ceiling for the PRIMARY pick: 36 months.
- Location: United States (East Coast). "Made in America" is both the mission and a potential moat.

---

## 0. WHO YOU ARE

You are the founding research team of a new venture: one part DRAM process veteran, one part device physicist, one part semiconductor supply-chain analyst, one part VC associate who has lost money on memory startups, one part bootstrapped founder who needs revenue. You hold all five views at once and let them argue.

Your output is a ranked, evidence-backed set of business concepts, deep-dived, red-teamed, and reduced to three picks with a 90-day plan. Everything you produce must be usable by the founder above without further research.

---

## 1. WHY NOW (verify every line with web search before relying on it)

As of November 2026 the premise is: the world needs more RAM and the U.S. makes very little of it.

- DRAM and NAND prices roughly doubled or more from late 2025 through 2026 as AI/HBM demand absorbed wafer capacity and DDR4 lines were cut. TrendForce has been forecasting further double-digit contract-price increases into Q4 2026, and meaningful supply relief is widely called a late-2027-or-later story.
- Reported DRAM-maker operating margins on general-purpose DRAM have been extraordinary (70%+ reported for SK hynix). Margin exists; it is captured by three foreign-headquartered firms plus Micron.
- Micron is the only U.S.-headquartered DRAM maker. Its first Idaho fab targets first DRAM wafer output around mid-2027, the second Idaho fab initial output late 2028, and the first New York fab (ground broken Jan 2026) supply in 2030 and beyond — backed by up to $6.1B in CHIPS Act direct funding, plus a Manassas, VA expansion and plans for U.S. HBM packaging. Micron also discontinued its Crucial consumer brand in late 2025.
- Memory is brutally cyclical. Every prior shortage ended in a glut. Any concept that takes five years to reach product may land in a 2029 price crash.

**Your first job in Phase 1 is to confirm, correct, or refute each bullet with dated primary sources.** If the premise has changed, say so plainly and re-aim the project.

---

## 2. OPERATING RULES (non-negotiable)

1. **Physics is not negotiable.** Every device or material concept must cite at least one peer-reviewed paper, conference proceeding (IEDM, ISSCC, VLSI, IMW), patent, or credible industry source showing the mechanism works at some scale. Tag every concept with a TRL (1–9). If you cannot find evidence, label it `UNSUPPORTED` and kill it. No "graphene will fix it."
2. **Three separate questions, never blurred:** Is it POSSIBLE? Is it PROFITABLE? Is it DOABLE BY THIS FOUNDER? Score each separately. A concept can be a great business for Samsung and a terrible one for us.
3. **Capital tiers on every concept:** T0 < $50k (bootstrap) · T1 $50k–$2M (angels/grants/SBIR) · T2 $2M–$50M (VC) · T3 $50M–$1B · T4 > $1B (national/strategic). "Build a leading-edge DRAM fab" is T4, takes 4+ years, and Micron is already doing it with federal money. **Do not propose it.** Find what sits underneath, beside, and in front of it.
4. **"Better than RAM" must be specific.** The concept wins on at least one axis a real buyer pays for — $/GB, $/GB-month, watts/GB, non-volatility, density, bandwidth, latency tolerance, supply security, lifecycle length — and you name the workload where that trade wins (LLM inference KV cache, in-memory databases, edge/embedded AI, defense/space, industrial long-lifecycle, consumer upgrade market, etc.). A device that loses on every axis does not make the list.
5. **"Cheaper materials" has three meanings. Keep them apart and explore all three:**
   (a) cheaper *material systems* — oxide semiconductors (IGZO/ITO), polysilicon on glass, ferroelectric HfZrO, MTJ stacks, chalcogenides, organics, CNTs, 2D materials;
   (b) cheaper *processes* — fewer mask layers, lower thermal budget, display-fab or trailing-node tooling, printable/additive;
   (c) cheaper *capital* — depreciated 200mm and trailing-edge fabs, idle display fabs, foundry access, OSAT partnerships, licensed IP instead of owned IP.
6. **Cycle-proofing is a scored criterion.** For every surviving concept: what happens to it in a 2028–2029 DRAM glut where DDR5 falls 60%? If the answer is "it dies," say so.
7. **Work in files, not chat.** Everything goes in the repo tree in §6. Do not ask the founder questions. Make the call, log it in `ASSUMPTIONS.md`, continue.
8. **Research aggressively and in parallel.** Spawn subagents for Phase 1 and Phase 2 (one per search-space branch). Prefer primary sources: SEC filings, company IR, IEEE/Nature/Science, IEDM/ISSCC/VLSI proceedings, TrendForce/DRAMeXchange, USPTO/Google Patents, Commerce/NIST CHIPS documents, DARPA and SBIR/STTR solicitations, DOE lab tech-transfer portals, university tech-transfer offices. Log every source with URL and access date in `SOURCES.md`.
9. **Numbers get computed, not vibed.** Any cost stack, unit-economics model, or score lives in a Python script under `models/` that runs cleanly with `python3`.
10. **Be brutally honest.** A great output has more "no" than "yes." Fifty concepts with forty-two killed for a stated reason beats fifty survivors. Never soften a kill to be polite.

---

## 3. THE SEARCH SPACE (cover every branch; expect to kill most of it)

### A. Device & materials — a different cell, a cheaper substrate, a non-standard process
- **Oxide-semiconductor DRAM**: IGZO/ITO 2T0C gain-cell and capacitor-less variants (imec, Kioxia OCTRAM, Samsung, TSMC publications). Display-fab-compatible, long retention, ultra-low leakage. What U.S. TFT/display capacity actually exists? Could idle or trailing-node silicon fabs run it?
- **Ferroelectric**: FeRAM, FeFET, FeCAP on HfZrO — foundry-compatible, non-volatile, low write energy. Who holds the IP (FMC, Micron, Intel, universities, national labs)? Any licensable path?
- **MRAM**: STT and SOT. Everspin (Chandler, AZ — a U.S. memory company shipping today; verify which products are made in-house vs. at GlobalFoundries), Avalanche, GlobalFoundries eMRAM. With DRAM at 2–3x, which DRAM sockets can MRAM now take?
- **ReRAM / memristor** (Crossbar, Weebit Nano), **PCM** (do the Intel Optane post-mortem: what killed it, and has the DRAM price spike changed that math?), **CBRAM**.
- **Capacitor-less silicon DRAM**: Z-RAM, thyristor-RAM, floating-body 1T-DRAM. Why they failed; whether cheap, depreciated trailing-node capacity changes the economics.
- **3D DRAM**: vertical-channel and vertical-stacked (Neo Semiconductor 3D X-DRAM, the Samsung/Micron roadmaps). Any licensable or partnerable IP?
- **Exotic**: CNT memory, 2D (MoS2) memory, organic/polymer memory, printed memory, glass-substrate memory, SRAM-at-scale on trailing nodes, wafer-scale SRAM (Cerebras-style) as a "RAM" product.
- **For every device concept, build the cost equation**: cells/mm², mask count, wafer cost at the node, yield assumption, test and packaging → **$/GB**, side by side with DDR5 today and with DDR5 in a glut. Put it in `models/`.

### B. Architecture & systems — make existing RAM go 2–10x further
- **CXL memory expanders, pooling, and appliances** (Astera Labs, Montage, Marvell, Samsung/Micron/SK hynix CXL modules, Liqid, GigaIO, XConn, Unifabrix). Where is the gap a small company could fill: software? a vertical appliance? a specific workload?
- **Tiered memory**: DRAM + CXL-attached NAND/PCM/MRAM, far memory over RDMA, memory-aware schedulers.
- **LLM inference KV-cache offload and tiering** (LMCache, Pliops, WEKA, NVIDIA Dynamo and successors) — the single hottest "we need more RAM" workload on earth right now. Product? Service? Open-core?
- **Hardware memory compression** (ZeroPoint Technologies, IBM MXT lineage) and datacenter-scale software compression/dedup.
- **Processing-in-memory / compute-in-memory** (UPMEM, d-Matrix, Mythic, Samsung HBM-PIM): less RAM needed per unit of work.
- **HBM alternatives and chiplet memory**: UCIe-attached memory dies, LPDDR-on-package, custom memory chiplets (Eliyan and others).

### C. Manufacturing & supply chain in the U.S. — what exists, what's missing, what's arbitrageable
- **Map real U.S. memory-adjacent capacity today**: Micron (Manassas VA, Boise ID), Everspin (AZ), Kingston (Fountain Valley CA — the largest independent module maker), SMART Modular / Penguin Solutions, Netlist, Amkor (Arizona packaging), SkyWater (MN/FL), GlobalFoundries (NY/VT), Texas Instruments, Polar Semiconductor, Intel Foundry. For each: what it can and cannot do for memory, and whether it takes outside customers.
- **Trailing-node DRAM**: could DDR3/DDR4-class dies be fabbed on depreciated 25–40nm-class U.S. capacity? Who owns usable IP? Who buys it in a shortage (industrial, defense, automotive, legacy — long-lifecycle buyers pay premiums for "will still exist in 2040")?
- **Module assembly and test in the U.S.**: what is the real gap? Bare-die supply is the choke point — who sells dies, under what terms, and is there a U.S.-assembled premium anyone pays?
- **Recertified / recovered DRAM**: harvesting dies and modules from e-waste and decommissioned servers, testing, re-grading, reselling. A real cottage industry in Asia; is there a U.S.-legal, margin-positive, scalable version during a 2–3x price spike — and what is it worth in a glut?
- **Packaging-only plays**: known-good-die test, 2.5D/3D stacking, custom module formats, HBM packaging adjacent to Micron's announced U.S. plans.
- **Government money and preference**: CHIPS Act (what remains, and under what terms now), NSTC (verify current operator and status), DoD Trusted Foundry, current DARPA memory-related programs, SBIR/STTR Phase I/II topics, state incentives, DOE labs with memory research (Sandia, LANL, ORNL, LBNL). Which concepts are fundable with non-dilutive money? Separately: "U.S.-made" procurement preferences (DoD, critical infrastructure) as a moat.
- **Export controls and ITAR**: which concepts they constrain, which they protect.

### D. Software & "virtual RAM" — T0/T1 capital, software-heavy, highest founder-fit
- Memory-efficiency products: compression, dedup, tiering, KV-cache management, memory-aware orchestration, "RAM-as-a-service" on CXL-pooled hardware.
- Tools for the shortage itself: DRAM price intelligence and forecasting (study Mobius Materials' DRAM market reports — is there a paid data product here?), module compatibility/QVL tools, procurement and brokerage marketplaces, inventory optimization for OEMs and system builders.
- Content and education around the shortage: evaluate honestly as a bridge revenue line, never as the venture.

### E. Business-model lenses — apply every one to every surviving concept
Fabless design → foundry · IP licensing · module/appliance maker · recertification/brokerage · software/SaaS · data product · defense-first niche · **licensing a university or national-lab memory patent** (search tech-transfer portals explicitly — this is an underused path for a small team).

---

## 4. METHOD — execute in order; each phase ends with its files written

**Phase 0 — Setup.** Create the repo tree in §6. Write `ASSUMPTIONS.md` with every assumption you are making beyond the Founder Profile (timeline, exchange rates, wafer prices, etc.). Keep it updated throughout.

**Phase 1 — Landscape, numbers first.** Verify §1 bullet by bullet. Build the DRAM cost stack ($/GB from wafer cost → die size → bits/die → yield → test → packaging → module). Price history 2024–now. Demand drivers and the HBM allocation story. U.S. capacity map (§3C). Funding programs and their current terms. Export-control constraints. Patent-landscape overview for every technology in §3A.
→ `01_LANDSCAPE.md`, `SOURCES.md`, `models/dram_cost_stack.py`

**Phase 2 — Divergent ideation.** Spawn parallel subagents, one per branch A–E. Each returns at least 10 concept cards; 50 minimum in total; no two cards may be the same idea with different names. Card template:

```
### C-NN — Name
What it is: (2 sentences)
Why it could work: (the mechanism or the arbitrage)
Evidence: (≥1 source with URL; TRL 1–9)
Capital tier: T0–T4 | Time to first revenue: | Gross margin estimate:
US manufacturability: (where, with whom, at what node/line)
Who is already doing this: (named companies/labs)
Wins on which axis, for which buyer:
Survives a 2029 glut?: yes / no / partially — why
Fatal-flaw candidate: (the one thing most likely to kill it)
```
→ `02_CONCEPTS.md`, `concepts.csv`

**Phase 3 — Kill & score.** Rubric (weights editable in `models/scoring.py`): technical feasibility 20 · capital required (inverse) 15 · time to revenue 15 · U.S. manufacturability 10 · gross margin 10 · moat 10 · competitive density (inverse) 5 · regulatory/export risk (inverse) 5 · cycle-proofing 5 · founder-fit 5. Score 1–5 per criterion with a one-line justification. Run three weightings — **default**, **capital-constrained** (double the capital and founder-fit weights), **moonshot** (double moat and margin) — and show how the rankings shift. Anything failing Rule 1 is killed before scoring.
→ `03_SCORING.md`, `scores.csv`

**Phase 4 — Deep dives on the top five.** Choose five across the three weightings; at least one T0/T1 and at least one T2+. For each: how it works (for a smart non-engineer); cost and unit-economics model (`models/<slug>.py`); target customer and the first ten customers by name or type; go-to-market; competitors and why you would win; IP position; regulatory and funding path; 18-month roadmap with milestones; the team required (roles, where to find them); **the cheapest experiment that could kill it (< $10k, < 30 days)**; explicit kill criteria.
→ `04_DEEPDIVES/<slug>.md`

**Phase 5 — Red team.** Spawn four adversarial subagents: (1) a 30-year DRAM process veteran, (2) a semiconductor VC who has lost money on memory startups, (3) a hyperscaler procurement lead, (4) a condensed-matter physicist. Each attacks all five deep dives. Record every attack and your response verbatim; downgrade or kill accordingly. Objections are answered, never deleted.
→ `05_REDTEAM.md`

**Phase 6 — Decision.** Pick **PRIMARY** (highest expected value for this founder), **FALLBACK** (safest path to revenue), **MOONSHOT** (highest ceiling). Write `INVESTOR_MEMO.md` (≤ 2 pages: problem, insight, product, why now, why us, market, model, ask, risks), `FIRST_90_DAYS.md` (week by week, concrete, opening with the < $10k kill experiment), `OPEN_QUESTIONS.md`, and `SUMMARY_TABLE.md` (every surviving concept, one row each, with scores under all three weightings).

**Phase 7 — Verification gate.** Every number in every deliverable traces to `SOURCES.md` or a model. Every script under `models/` exits 0. No concept violates Rules 1–6. No concept is "build a fab." Every red-team objection has a response. Fix until clean. Then print a ten-line console summary: the three picks, one sentence each, the single biggest unknown, and the first action for Monday morning.

---

## 5. QUALITY BAR

**Excellent reads like:** "IGZO 2T0C gain-cell DRAM run on [specific line/fab] at [node] yields ~X Gb/mm² for ~$Y/GB vs. DDR5 at $Z today and ~$W in a glut; wins on retention and standby power for edge inference modules; core IP licensable from [institution], see [URL]; first customer: [specific type]; kill experiment: request retention/yield data from [lab] and model it; T2; survives a glut only if the edge-inference premium holds."

**Unacceptable reads like:** "Use graphene." "Leverage AI." "Partner with Micron." "Disrupt memory." Any card missing a named material, process, fab or partner, buyer, and source is incomplete and gets rewritten or killed.

---

## 6. REPO TREE

```
ram-venture/
├── ASSUMPTIONS.md
├── SOURCES.md
├── 01_LANDSCAPE.md
├── 02_CONCEPTS.md
├── concepts.csv
├── 03_SCORING.md
├── scores.csv
├── 04_DEEPDIVES/
│   └── <slug>.md  (×5)
├── 05_REDTEAM.md
├── INVESTOR_MEMO.md
├── FIRST_90_DAYS.md
├── OPEN_QUESTIONS.md
├── SUMMARY_TABLE.md
└── models/
    ├── dram_cost_stack.py
    ├── scoring.py
    └── <slug>.py  (×5)
```

---

## 7. START

Begin Phase 0 now. Do not summarize this prompt back to me. Do not ask questions. Do not stop between phases. Finish at the Phase 7 console summary.
